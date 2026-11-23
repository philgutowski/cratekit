# Mutation table: u309-replay-after-d

Measured by `scripts/mutate.py` on 2026-11-22 22:39 UTC, branch `HEAD` at `05751e50`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22910 collected. pytest invocations for this batch: 165.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py baseline` at 2026-11-22 22:39 UTC for commit `05751e501e76`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 59, each measured by this driver.

Known failures: 249 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22910 against 22910. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r835-a.L1_load_carries_the_label_map` | `src/cratekit/modules/outbound/ledger.py` | user | 4 file(s) | 356 | 28 | killed |
| `r229.L8_a_living_legacy_record_is_freed` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 1 | killed |
| `r229.L9_an_empty_list_is_a_legacy_record` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 1 | killed |
| `r356-b.B5_export_plan_hands_on_the_display_title` | `src/cratekit/modules/outbound/export.py` | user | 1 file(s) | 64 | 2 | killed |
| `r1394.A5_any_failure_brought_down` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1305 | 3 | killed |
| `r1411.A1_agreed_order_always_stands` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1305 | 11 | killed |
| `r1411.A2_removed_tracks_asked_of_the_reading` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1305 | 3 | killed |
| `u234.O18_snapshot_keeps_the_reading` | `src/cratekit/modules/outbound/pairs.py` | maintainer | 23 file(s) | 1765 | 4 | killed |
| `u142.S2_plan_reads_the_year_key` | `src/cratekit/modules/outbound/sets.py` | user | 3 file(s) | 228 | 3 | killed |
| `r837-b.B5_unmatched_warning` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 60 | 2 | killed |
| `r879-b.S7_library_before_a_persons_answer` | `src/cratekit/export/set_match.py` | user | 1 file(s) | 60 | 1 | killed |
| `r1017.M2_recorded_before_frozen` | `src/cratekit/export/set_rename.py` | user | 4 file(s) | 195 | 1 | killed |
| `u140.B6_mark_refusal_dropped` | `src/cratekit/export/set_rename.py` | user | 2 file(s) | 102 | 2 | killed |
| `u140.B2_ledger_moves_another_id` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 1 file(s) | 29 | 1 | killed |
| `u214.M11_frozen_carries` | `src/cratekit/organize/mirror_frozen.py` | user | 6 file(s) | 199 | 6 | killed |
| `r290-author.S13_outbound_shell_call_removed` | `src/cratekit/modules/outbound/shell.py` | user | 2 file(s) | 249 | 18 | killed |
| `u143-e.C1_yours_empties` | `src/cratekit/organize/account.py` | user | 2 file(s) | 117 | 1 | killed |
| `u143-c.A1_kind_named` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 446 | 1 | killed |
| `r835-c.F1_recorded_folder_must_be_listed_again` | `src/cratekit/modules/outbound/folders.py` | user | 1 file(s) | 56 | 1 | killed |
| `r835-c.F8_marked_title_matches_by_name_again` | `src/cratekit/modules/outbound/folders.py` | user | 1 file(s) | 56 | 1 | killed |
| `u230.M3_lift_not_in_held` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 11 file(s) | 209 | 5 | killed |
| `u230.M23_short_lifted` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 11 file(s) | 209 | 1 | killed |
| `u227.R8_reader_not_passed` | `src/cratekit/organize/account_mirror.py` | user | 7 file(s) | 184 | 2 | killed |
| `u236.M16_settle_any_favourite` | `src/cratekit/organize/mirror_edits.py` | user | 8 file(s) | 223 | 1 | killed |
| `u236.M7_placed_after_keeps_all` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 8 file(s) | 223 | 4 | killed |
| `u201.E13_snapshot_word` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 5 file(s) | 185 | 2 | killed |
| `u201.E1_never_agreed_base` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 5 file(s) | 185 | 1 | killed |
| `u201.E11_later_strict` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 5 file(s) | 185 | 1 | killed |
| `u204.O5_batch_live` | `src/cratekit/organize/mirror_edits.py` | user | 6 file(s) | 222 | 1 | killed |
| `u204.O6_inbox_latch` | `src/cratekit/organize/mirror_edits.py` | user | 6 file(s) | 222 | 1 | killed |
| `u143-b.F1_debris_first` | `src/cratekit/organize/filing.py` | user | 3 file(s) | 164 | 16 | killed |
| `u142.S13_unread_reads_as_none` | `src/cratekit/organize/account.py` | user | 1 file(s) | 95 | 1 | killed |
| `u116.M2_set_rule_dropped` | `src/cratekit/organize/filing.py` | user | 1 file(s) | 95 | 1 | killed |
| `u142.S12_undeclared_reads_as_empty` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 95 | 1 | killed |
| `u142.S23_prefix_only_said_as_a_move` | `src/cratekit/organize/account.py` | user | 1 file(s) | 95 | 1 | killed |
| `u112.R4_job_without_gate_run` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 95 | 1 | killed |
| `u112.A3_retired_unnumbered` | `src/cratekit/organize/account.py` | user | 1 file(s) | 95 | 1 | killed |
| `u137.C3_choices_dropped` | `src/cratekit/organize/cli.py` | user | 1 file(s) | 95 | 1 | killed |
| `u137.R1_adopt_gate` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 95 | 3 | killed |
| `u246.S6_inspiration_planned_live` | `src/cratekit/organize/inspiration.py` | user | 4 file(s) | 327 | 1 | killed |
| `u144-a.A2_two_of_one_name` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 1 | killed |
| `u144-c.C7_folder_warning` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 38 | 1 | killed |
| `r1295.M9_misses_unsorted` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 1 | killed |
| `u144-c.C5_export_module` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 38 | 1 | killed |
| `u144-a.A1_skip_rule` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 2 | killed |
| `u144-c.C6_native_only` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 38 | 1 | killed |
| `u147-a.M1_two_root_folders` | `src/cratekit/modules/outbound/mirror.py` | user | 1 file(s) | 34 | 1 | killed |
| `r1289.M14_mirror_unread_branch` | `src/cratekit/organize/mirror_downloads.py` | user | 3 file(s) | 103 | 1 | killed |
| `r1031.M15_seen_not_seeded` | `src/cratekit/organize/account_mirror.py` | user | 3 file(s) | 166 | 3 | killed |
| `r1031.M11_filter_removed` | `src/cratekit/modules/outbound/ledger.py` | user | 2 file(s) | 71 | 1 | killed |
| `r1031.M12_link_keeps_its_miss` | `src/cratekit/modules/outbound/ledger_settle.py` | maintainer | 2 file(s) | 71 | 1 | killed |
| `u222.M25_steps_not_frozen` | `src/cratekit/organize/account_mirror.py` | user | 6 file(s) | 251 | 6 | killed |
| `u222.M11_decided_freeze_shown` | `src/cratekit/organize/account_mirror.py` | user | 6 file(s) | 251 | 2 | killed |
| `u222.M3_overlay_any_remote_id` | `src/cratekit/organize/mirror_frozen.py` | user | 6 file(s) | 251 | 1 | killed |
| `u222.M14_moved_new_step_silent` | `src/cratekit/organize/mirror_frozen.py` | user | 6 file(s) | 251 | 1 | killed |
| `u150.A4_listed_step` | `src/cratekit/organize/account_mirror.py` | user | 3 file(s) | 161 | 1 | killed |
| `u150.M5_apply_removes` | `src/cratekit/modules/outbound/mirror.py` | user | 3 file(s) | 103 | 4 | killed |
| `u150.L1_forget_checks_id` | `src/cratekit/modules/outbound/ledger_settle.py` | user | 2 file(s) | 66 | 1 | killed |
| `u267.M1_report_shares_nothing` | `src/cratekit/organize/cli.py` | user | 3 file(s) | 147 | 5 | killed |
| `u143-e.P1_still_at_root` | `src/cratekit/organize/root.py` | user | 1 file(s) | 55 | 1 | killed |
| `u143-b.L1_nested_stays` | `src/cratekit/organize/root.py` | user | 1 file(s) | 55 | 1 | killed |
| `u255.S1_member_already_on` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 338 | 2 | killed |
| `u255.S2_read_back_trusts_the_cache` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 338 | 3 | killed |
| `u270.E2_landed_only_what_was_answered` | `src/cratekit/modules/outbound/export.py` | user | 3 file(s) | 169 | 4 | killed |
| `u270.C2_stop_while_planning` | `src/cratekit/export/cli.py` | user | 2 file(s) | 145 | 1 | killed |
| `u220.A23_pause_index` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 283 | 1 | killed |
| `r1308.M6_after_by_length` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 388 | 4 | killed |
| `r1032.A9_album_narrow_unfolded` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 2 file(s) | 118 | 1 | killed |
| `r227.A2_never_stale` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 371 | 13 | killed |
| `r1032.A2_tie_always_broken` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 4 file(s) | 316 | 15 | killed |
| `u208.M22_adapter_hearts_half` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 2 file(s) | 134 | 1 | killed |
| `r356-a.A8_first_billed_artist_not_required` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 1 file(s) | 113 | 1 | killed |
| `r356-b.B9_export_item_report_drops_the_reason` | `src/cratekit/export/cli.py` | user | 1 file(s) | 113 | 1 | killed |
| `r358-round-2.A7_empty_title_message` | `src/cratekit/modules/outbound/tidal_account.py` | maintainer | 1 file(s) | 113 | 3 | killed |
| `r356-a.A11_row_title_read_one_way_only` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 1 file(s) | 113 | 1 | killed |
| `r358.A6_retry_coefficient` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 113 | 1 | killed |
| `u226.M7_reading_takes_window` | `src/cratekit/modules/outbound/tidal_account.py` | user | 9 file(s) | 442 | 5 | killed |
| `r850-a.E10_concluded_not_called` | `src/cratekit/modules/outbound/shell.py` | user | 2 file(s) | 236 | 4 | killed |
| `u51-item-derivation.D2_ambiguous_playlist` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 143 | 1 | killed |
| `u131.K13_unfiled_warning` | `src/cratekit/export/cli.py` | user | 1 file(s) | 123 | 2 | killed |
| `r227.S4_utc_instant_in_the_block` | `src/cratekit/modules/outbound/shell.py` | user | 1 file(s) | 123 | 1 | killed |
| `r227.S5_envelope_drops_the_age` | `src/cratekit/modules/outbound/shell.py` | user | 1 file(s) | 123 | 2 | killed |
| `u131.K5_recorded_folder` | `src/cratekit/modules/outbound/kinds.py` | user | 2 file(s) | 109 | 2 | killed |
| `r1305.A4_account_reads_its_own_link_only` | `src/cratekit/modules/outbound/account.py` | user | 3 file(s) | 197 | 7 | killed |
| `u261.A4_refusal_drops_no_session` | `src/cratekit/modules/outbound/account.py` | user | 2 file(s) | 143 | 1 | killed |
| `r836-c.F1_build_skips_pruned` | `src/cratekit/modules/outbound/folders.py` | user | 5 file(s) | 404 | 1 | killed |
| `r836-b.L4_pruned_leaves_added` | `src/cratekit/modules/outbound/ledger_settle.py` | user | 5 file(s) | 404 | 5 | killed |
| `r836-d.P1_only_created_years` | `src/cratekit/modules/outbound/prune.py` | user | 5 file(s) | 404 | 1 | killed |
| `u174.O2_seen_skips_a_filed_pass` | `src/cratekit/organize/account.py` | user | 2 file(s) | 164 | 1 | killed |
| `u216.M22_write_drops_held` | `src/cratekit/modules/outbound/pairs.py` | user | 12 file(s) | 383 | 12 | killed |
| `u221.R15_mark_drops_the_hold` | `src/cratekit/modules/outbound/pairs.py` | user | 3 file(s) | 84 | 14 | killed |
| `u221.R18_release_writes_nothing` | `src/cratekit/modules/outbound/pairs.py` | user | 1 file(s) | 32 | 6 | killed |
| `r837-a.A14_not_listed_not_blamed` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 60 | 1 | killed |
| `r228-operator.D10_pink_warning_gone` | `src/cratekit/modules/outbound/shell.py` | user | 1 file(s) | 13 | 1 | killed |
| `u123.T1_adapter_vouching` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 151 | 1 | killed |
| `u230.M2_lift_not_in_was` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 11 file(s) | 209 | 6 | killed |
| `u236.M20_agreed_never_drops` | `src/cratekit/modules/outbound/ledger_settle.py` | user | 8 file(s) | 223 | 3 | killed |
| `u236.M12_reader_short_branch` | `src/cratekit/organize/account_mirror.py` | user | 8 file(s) | 223 | 1 | killed |
| `u204.P2_acquire_only_unknown` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 6 file(s) | 222 | 2 | killed |
| `u147-c.M14_made_in_mirror` | `src/cratekit/modules/outbound/ledger.py` | user | 1 file(s) | 34 | 1 | killed |
| `u255.S3_answer_absent_passes` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 338 | 1 | killed |
| `r1308.M24_positions_count` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 388 | 2 | killed |
| `r1032.A10_reason_words_reworded` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 3 file(s) | 241 | 6 | killed |
| `u226.M8_unpaged_first` | `src/cratekit/modules/outbound/tidal_account.py` | user | 9 file(s) | 442 | 3 | killed |
| `u51-item-derivation.D1_unknown_playlist` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 143 | 2 | killed |

## Row definitions

### `r835-a.L1_load_carries_the_label_map`

ledger._load: the label map is dropped on load, so any other write to the ledger forgets every label's folder and year playlists

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r835-a.json`, row `L1_load_carries_the_label_map`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 356 against a baseline of 356
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

### `r229.L8_a_living_legacy_record_is_freed`

A legacy record under a living path is freed with no contents to say the path was reused

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L8_a_living_legacy_record_is_freed`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
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

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L9_an_empty_list_is_a_legacy_record`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
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

### `r356-b.B5_export_plan_hands_on_the_display_title`

The export engine hands the account the title with its naming head on

- File: `src/cratekit/modules/outbound/export.py`
- Source: `r356-b.json`, row `B5_export_plan_hands_on_the_display_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`
- Collected: 64 against a baseline of 64
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_the_export_plan_hands_the_account_the_files_album_tag`
  - `tests/modules/test_outbound.py::test_the_export_plan_hands_the_account_the_release_title_and_not_the_display_one`

Old text:

```
            title=track.release_title,
```

New text:

```
            title=track.title,
```

### `r1394.A5_any_failure_brought_down`

adapter order: a move that failed any way, a dropped connection included, is told as not landed

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1394.json`, row `A5_any_failure_brought_down`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1305 against a baseline of 1305
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_move_spent_on_its_412s_is_told_as_not_landed`
  - `tests/test_outbound_order.py::test_a_move_that_failed_another_way_is_left_as_maybe_landed`
  - `tests/test_outbound_order.py::test_a_stop_in_the_pause_after_a_412_is_recorded_as_no_move_in_flight`

Old text:

```
                    if not _stale_tag(exc):
                        raise
                    if told is not None:
```

New text:

```
                    if told is not None:
                        told(number - 1, number - 1)
                    if not _stale_tag(exc):
                        raise
                    if told is not None:
```

### `r1411.A1_agreed_order_always_stands`

the agreed order check passes every reading, so a reading in the order from before the stopped moves is planned from

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `A1_agreed_order_always_stands`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1305 against a baseline of 1305
- Kills: 11 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_agreed_order_after_an_add_refuses_with_nothing_moved`
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_agreed_order_once_is_read_again_and_takes_the_order`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading1-agreed1-False]`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading5-agreed5-False]`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading7-agreed7-False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_planned_again_in_the_writing_command_is_held_to_its_own_reading`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_removes_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`

Old text:

```
    return [one for one in dict.fromkeys(reading) if one in named] == [
        one for one in dict.fromkeys(str(one) for one in agreed) if one in held
    ]
```

New text:

```
    return bool(named or held or True)
```

### `r1411.A2_removed_tracks_asked_of_the_reading`

the agreed order check asks every agreed track of the reading, so a track this write took off refuses the finish

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `A2_removed_tracks_asked_of_the_reading`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1305 against a baseline of 1305
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_track_this_write_took_off_is_not_asked_of_the_reading`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading6-agreed6-True]`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading9-agreed9-True]`

Old text:

```
        one for one in dict.fromkeys(str(one) for one in agreed) if one in held
```

New text:

```
        one for one in dict.fromkeys(str(one) for one in agreed)
```

### `u234.O18_snapshot_keeps_the_reading`

a snapshot that moved keeps the reading after the stop, so it outlives the stop it was read after

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u234.json`, row `O18_snapshot_keeps_the_reading`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_intake_land_twins.py`, `tests/test_outbound_order.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 1765 against a baseline of 1765
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_the_person_reordered_after_a_sync_read_it_is_merged_as_their_change`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_stopped.py::test_a_reading_after_a_stop_round_trips_and_goes_when_the_snapshot_moves`
  - `tests/test_sync_pair_stopped_order.py::test_an_account_the_stop_left_off_its_path_is_never_written_into_rekordbox`

Old text:

```
                stop_seen=None if moved else held.stop_seen,
```

New text:

```
                stop_seen=held.stop_seen,
```

### `u142.S2_plan_reads_the_year_key`

plan_archive: read the ledger's folder record under the year, so the filing's plain year folder is reused for a set

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u142.json`, row `S2_plan_reads_the_year_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`, `tests/test_organize.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 228 against a baseline of 228
- Kills: 3 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_year_folder_deleted_on_the_account_is_made_again`
  - `tests/test_organize.py::test_a_downloaded_sets_folder_made_by_hand_is_adopted_and_the_filing_keeps_its_year`
  - `tests/test_organize.py::test_a_year_record_whose_folder_now_carries_the_sets_name_is_not_the_filings`

Old text:

```
    recorded = ledger.set_folder(cfg, name)
```

New text:

```
    recorded = ledger.set_folder(cfg, year)
```

### `r837-b.B5_unmatched_warning`

set_cli._unmatched_warnings: a set that left tracks out answers with no warning naming them (R-850)

- File: `src/cratekit/export/set_cli.py`
- Source: `r837-b.json`, row `B5_unmatched_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 60 against a baseline of 60
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set.py::test_approved_the_account_holds_a_private_playlist_of_four_in_order`
  - `tests/test_export_set.py::test_five_rows_with_one_unmatched_plan_four_and_name_the_fifth`

Old text:

```
    if not planned.unmatched:
        return []
    return [
```

New text:

```
    if True:
        return []
    return [
```

### `r879-b.S7_library_before_a_persons_answer`

match_rows: let the library's file pre-empt a person's answer in review

- File: `src/cratekit/export/set_match.py`
- Source: `r879-b.json`, row `S7_library_before_a_persons_answer`
- Moved: the same text, now in src/cratekit/export/set_match.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_persons_answer_in_review_wins_over_the_librarys_file`

Old text:

```
            answered = candidates.settled(items, one)
```

New text:

```
            answered = None if not one.isrc and library.file_isrc(one)[0] else candidates.settled(items, one)
```

### `r1017.M2_recorded_before_frozen`

Rename: rank the landing names ahead of the frozen name an earlier rename chose

- File: `src/cratekit/export/set_rename.py`
- Source: `r1017.json`, row `M2_recorded_before_frozen`
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
            for one in (set_name(frozen) if frozen else "", *recorded, *_names_for_job(job))
```

New text:

```
            for one in (*recorded, set_name(frozen) if frozen else "", *_names_for_job(job))
```

### `u140.B6_mark_refusal_dropped`

plan_rename retitles a playlist the archive marked

- File: `src/cratekit/export/set_rename.py`
- Source: `u140.json`, row `B6_mark_refusal_dropped`
- Moved: the same text, now in src/cratekit/export/set_rename.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_playlist_the_archive_marked_is_refused_rather_than_retitled`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_refuses_a_playlist_a_legacy_archive_prefixed`

Old text:

```
        if mark is not None:
            raise _rename_unresolved(

```

New text:

```
        if False:
            raise _rename_unresolved(

```

### `u140.B2_ledger_moves_another_id`

rename_set_playlist drops its refusal when the old name records a different playlist

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `u140.json`, row `B2_ledger_moves_another_id`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_the_ledger_refuses_to_fold_a_rename_into_another_playlist`

Old text:

```
        if recorded != remote_id:

```

New text:

```
        if False:

```

### `u214.M11_frozen_carries`

mirror_frozen: rebuild every folder with no unmirrored node, so the run that applies loses the lines

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u214.json`, row `M11_frozen_carries`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 199 against a baseline of 199
- Kills: 6 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_rebuild_from_the_frozen_plan_still_names_them`
  - `tests/test_inbox_unmirrored.py::test_frozen_unmirrored_nodes_that_are_not_pairs_of_text_are_not_read[not text]`
  - `tests/test_inbox_unmirrored.py::test_frozen_unmirrored_nodes_that_are_not_pairs_of_text_are_not_read[one part]`
  - `tests/test_inbox_unmirrored.py::test_frozen_unmirrored_nodes_that_are_not_pairs_of_text_are_not_read[text]`
  - `tests/test_inbox_unmirrored.py::test_frozen_unmirrored_nodes_that_are_not_pairs_of_text_are_not_read[three parts]`
  - `tests/test_inbox_unmirrored.py::test_the_frozen_plan_carries_the_unmirrored_nodes`

Old text:

```
                unmirrored=_unmirrored(folder["unmirrored"]),
```

New text:

```
                unmirrored=(),
```

### `r290-author.S13_outbound_shell_call_removed`

Remove the one jobs.raise_for_state call from modules/outbound/shell.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/modules/outbound/shell.py`
- Source: `r290-author.json`, row `S13_outbound_shell_call_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_outbound_workers.py`
- Collected: 249 against a baseline of 249
- Kills: 18 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[export.playlist]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[sync.favorites]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[export.playlist]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[sync.favorites]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[export.playlist]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[sync.favorites]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[export.playlist]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[sync.favorites]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[export.playlist]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[sync.favorites]`
  - `tests/test_job_outcome.py::test_every_function_that_drives_a_job_maps_its_ending_afterwards`
  - `tests/test_outbound_workers.py::test_a_cancelled_job_does_not_report_a_clean_resume`
  - `tests/test_outbound_workers.py::test_a_failed_favourite_leaves_the_sweep_resumable`
  - `tests/test_outbound_workers.py::test_a_failed_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/test_outbound_workers.py::test_a_track_the_provider_would_not_add_fails_its_item_alone_and_is_never_recorded`
  - ... and 3 more, see the JSON sidecar

Old text:

```
jobs.raise_for_state(job)
```

New text:

```
jobs.get  # the mapping call, removed
```

### `u143-e.C1_yours_empties`

Account: list an empty root playlist the root step removes as one of the author's

- File: `src/cratekit/organize/account.py`
- Source: `u143-e.json`, row `C1_yours_empties`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`, `tests/test_organize.py`
- Collected: 117 against a baseline of 117
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_the_full_verb_lists_the_working_custom_and_never_the_root_steps_removals`

Old text:

```
        _yours(cfg, area, labels, catalogue_of, remote_of, moving | _empties(filed_of))
```

New text:

```
        _yours(cfg, area, labels, catalogue_of, remote_of, moving)
```

### `u143-c.A1_kind_named`

Adapter: drop the refusal of a kind other than debris or empty

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u143-c.json`, row `A1_kind_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_root.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`
- Collected: 446 against a baseline of 446
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_ledger_claimed_playlist_or_another_kind_is_refused_with_no_provider_call`

Old text:

```
        if kind not in kinds.ROOT_REMOVALS:
```

New text:

```
        if False:
```

### `r835-c.F1_recorded_folder_must_be_listed_again`

folders.plan: a recorded folder the account no longer lists is reused, so year playlists are moved into a folder that is gone

- File: `src/cratekit/modules/outbound/folders.py`
- Source: `r835-c.json`, row `F1_recorded_folder_must_be_listed_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_label_folder_deleted_on_the_account_is_made_again_and_recorded`

Old text:

```
    if shape.folder_id and shape.folder_id in root:
```

New text:

```
    if shape.folder_id:
```

### `r835-c.F8_marked_title_matches_by_name_again`

folders.plan: a year playlist in the folder carrying the mark prefix is not matched by name, so an unrecorded marked year is created a second time

- File: `src/cratekit/modules/outbound/folders.py`
- Source: `r835-c.json`, row `F8_marked_title_matches_by_name_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_an_unrecorded_marked_year_in_the_folder_is_matched_by_its_marked_name`

Old text:

```
            pid for pid, title in inside.items() if title in (name, MARK_PREFIX + name)
```

New text:

```
            pid for pid, title in inside.items() if title == name
```

### `u230.M3_lift_not_in_held`

landed check: the lifted playlist's base still counts as a snapshot holding the track

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u230.json`, row `M3_lift_not_in_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 209 against a baseline of 209
- Kills: 5 (killed)
- Killed:
  - `tests/test_mirror_edits_u230.py::test_a_folder_edit_on_a_never_agreed_derived_playlist_is_carried_too`
  - `tests/test_mirror_edits_u230.py::test_a_never_agreed_playlist_whose_account_side_holds_the_track_carries_it`
  - `tests/test_organize_mirror_edits_u230.py::test_a_drag_back_into_the_landings_band_after_the_batch_left_inbox_stands`
  - `tests/test_organize_mirror_edits_u230.py::test_a_move_in_rekordbox_after_the_carry_still_stands`
  - `tests/test_organize_mirror_edits_u230.py::test_a_never_agreed_playlist_holding_the_track_files_it_where_the_account_put_it`

Old text:

```
bool(held_by.get(track, frozenset()) - lifted)
```

New text:

```
bool(held_by.get(track, frozenset()))
```

### `u230.M23_short_lifted`

_as_queued: lift a short listing, so an edit is read off an account side nobody read (round one's row 3)

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u230.json`, row `M23_short_lifted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 209 against a baseline of 209
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits_u230.py::test_a_short_listing_of_the_queuing_playlist_lifts_nothing`

Old text:

```
        and not one.short

```

New text:

```
        and True

```

### `u227.R8_reader_not_passed`

_read_edits: decide without the landing places

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u227.json`, row `R8_reader_not_passed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 184 against a baseline of 184
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u227.py::test_a_queued_track_filed_elsewhere_by_its_tags_is_filed_where_the_account_put_it`
  - `tests/test_organize_mirror_edits_u227.py::test_the_landings_filing_by_the_real_producer_is_read_as_the_landings`

Old text:

```
        read, {remote: sorted(rows) for remote, rows in owner.items()}, landings
```

New text:

```
        read, {remote: sorted(rows) for remote, rows in owner.items()}
```

### `u236.M16_settle_any_favourite`

settle: record a placement for a favourite put in a month on the account too

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u236.json`, row `M16_settle_any_favourite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 223 against a baseline of 223
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_put_in_another_month_on_the_account_leaves_the_placed_month`

Old text:

```
            and decision.to.primary
            and month_of.get(decision.content_id)
```

New text:

```
            and month_of.get(decision.content_id)
```

### `u236.M7_placed_after_keeps_all`

placed_after: never drop a placement, so a later hand membership could outlast it

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u236.json`, row `M7_placed_after_keeps_all`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 223 against a baseline of 223
- Kills: 4 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_a_placement_is_dropped_once_the_account_holds_its_track_with_no_hold`
  - `tests/test_mirror_edits_u236.py::test_the_ledger_keeps_a_placement_until_the_mirror_finished_its_playlist`
  - `tests/test_organize_mirror_edits_u236.py::test_a_hand_addition_after_the_placement_is_dropped_is_read_as_one`
  - `tests/test_organize_mirror_edits_u236.py::test_the_organize_after_the_favourite_puts_it_in_the_accounts_month`

Old text:

```
    return {track: at for track, at in placed.items() if track in kept or track not in now}
```

New text:

```
    return dict(placed)
```

### `u201.E13_snapshot_word`

agreed_after: a held track takes the account's word rather than the snapshot's

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u201.json`, row `E13_snapshot_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 185 against a baseline of 185
- Kills: 2 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_the_snapshot_after_keeps_its_word_on_a_held_track`
  - `tests/test_organize_mirror_edits.py::test_the_ledger_keeps_a_snapshot_apart_from_none_and_only_on_its_own_playlist`

Old text:

```
    before = now if base is None else frozenset(base)
```

New text:

```
    before = now
```

### `u201.E1_never_agreed_base`

Mirrored.base: a playlist never agreed reads an empty snapshot, so every account track reads as an edit on the first run

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u201.json`, row `E1_never_agreed_base`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 185 against a baseline of 185
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_a_playlist_never_agreed_reads_every_difference_as_rekordboxs`

Old text:

```
        return self.account if self.agreed is None else self.agreed
```

New text:

```
        return frozenset() if self.agreed is None else self.agreed
```

### `u201.E11_later_strict`

_later: equal times let the account's move win

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u201.json`, row `E11_later_strict`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 185 against a baseline of 185
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_two_moves_at_one_moment_keep_rekordboxs`

Old text:

```
    if account_at > rekordbox_at:
```

New text:

```
    if account_at >= rekordbox_at:
```

### `u204.O5_batch_live`

_plan_inbox: a batch no longer directly under INBOX is written as if it were

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u204.json`, row `O5_batch_live`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 222 against a baseline of 222
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_batch_moved_into_old_since_the_plan_is_never_touched`

Old text:

```
        if len(found) != 1:
```

New text:

```
        if False:
```

### `u204.O6_inbox_latch`

write: an INBOX edit asks no intake tree latch

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u204.json`, row `O6_inbox_latch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 222 against a baseline of 222
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_an_inbox_edit_over_a_latched_intake_tree_writes_nothing`

Old text:

```
    if edits.INBOX in touched:
```

New text:

```
    if False:
```

### `u143-b.F1_debris_first`

Filing: drop the debris branch, so a debris copy is left as the label step's and the root step never sees it

- File: `src/cratekit/organize/filing.py`
- Source: `u143-b.json`, row `F1_debris_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`, `tests/test_organize_root.py`, `tests/test_playlist_kinds.py`
- Collected: 164 against a baseline of 164
- Kills: 16 (killed)
- Killed:
  - `tests/test_organize.py::test_only_root_removes_debris_and_empties_on_the_gate_and_files_the_legacy_folder`
  - `tests/test_organize.py::test_the_full_verb_lists_the_working_custom_and_never_the_root_steps_removals`
  - `tests/test_organize_root.py::test_a_debris_copy_given_a_track_since_the_plan_is_kept_and_the_rest_removed`
  - `tests/test_organize_root.py::test_a_debris_copy_whose_tracks_could_not_all_be_read_is_left`
  - `tests/test_organize_root.py::test_a_debris_copy_with_a_track_the_label_folder_lacks_is_left_naming_it`
  - `tests/test_organize_root.py::test_a_debris_copy_with_no_listed_count_is_left_before_any_read`
  - `tests/test_organize_root.py::test_a_followed_labels_recorded_folder_is_read_whatever_it_is_called_now`
  - `tests/test_organize_root.py::test_a_label_folder_that_cannot_be_read_leaves_its_debris_and_refuses_nothing_else`
  - `tests/test_organize_root.py::test_a_label_folder_with_no_downloaded_playlist_proves_nothing`
  - `tests/test_organize_root.py::test_a_refusal_part_way_stops_and_names_what_was_removed`
  - `tests/test_organize_root.py::test_a_second_run_on_a_clean_root_plans_nothing`
  - `tests/test_organize_root.py::test_a_year_playlist_held_as_taken_with_no_prefix_proves_its_tracks_downloaded`
  - `tests/test_organize_root.py::test_an_empty_debris_copy_is_removed_as_empty`
  - `tests/test_organize_root.py::test_debris_with_no_label_folder_or_two_of_them_is_left_with_why`
  - `tests/test_organize_root.py::test_four_identical_debris_copies_with_every_track_filed_plan_four_removals`
  - ... and 1 more, see the JSON sidecar

Old text:

```
        if not claimed and is_library_debris(name):
```

New text:

```
        if False:
```

### `u142.S13_unread_reads_as_none`

organize set step: read a database that cannot answer as holding no INSPIRATION playlist, so the set waits instead of refusing

- File: `src/cratekit/organize/account.py`
- Source: `u142.json`, row `S13_unread_reads_as_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_two_inspiration_folders_refuse_the_unproven_set_alone`

Old text:

```
            try:
                held = inspired.get()
            except CratekitError as exc:
                area.steps.append(refused(key, title, exc.cause))
                continue
```

New text:

```
            try:
                held = inspired.get()
            except CratekitError:
                held = frozenset()
```

### `u116.M2_set_rule_dropped`

plan: a set playlist is no longer left to the archive

- File: `src/cratekit/organize/filing.py`
- Source: `u116.json`, row `M2_set_rule_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_label_playlist_is_the_label_steps_and_a_set_the_archives`

Old text:

```
        if identity in set_built:
            rows.append(Placement(identity, name, LEFT, why=SET_STEP))
```

New text:

```
        if False:
            rows.append(Placement(identity, name, LEFT, why=SET_STEP))
```

### `u142.S12_undeclared_reads_as_empty`

inspiration_names: answer an empty set when no INSPIRATION folder is declared, so the wait says no playlist rather than no folder

- File: `src/cratekit/export/set_cli.py`
- Source: `u142.json`, row `S12_undeclared_reads_as_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_taxonomy_with_no_inspiration_folder_waits_and_says_why`

Old text:

```
    if declared.inspiration is None:
        return None
    return frozenset(
```

New text:

```
    if declared.inspiration is None:
        return frozenset()
    return frozenset(
```

### `u142.S23_prefix_only_said_as_a_move`

organize set step: say file it in the folder for a set already there with its built title, a prefix and no move

- File: `src/cratekit/organize/account.py`
- Source: `u142.json`, row `S23_prefix_only_said_as_a_move`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_set_in_its_folder_with_its_built_title_is_taken_and_not_moved`

Old text:

```
        if archived.writes and planned.move:
```

New text:

```
        if archived.writes:
```

### `u112.R4_job_without_gate_run`

The adoption job is queued with no gate run, so its resume can never be answered

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u112.json`, row `R4_job_without_gate_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_the_adoption_job_carries_a_run_its_own_resume_can_answer`

Old text:

```
                    jobs.GATE_RUN_KEY: gate_run,

```

New text:

```
(empty)
```

### `u112.A3_retired_unnumbered`

Every retired intake file ranks alike, so the first read wins rather than the latest

- File: `src/cratekit/organize/account.py`
- Source: `u112.json`, row `A3_retired_unnumbered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_the_latest_retired_landing_wins_by_number_and_a_bracket_is_no_pattern`

Old text:

```
    return int(number) if number.isdigit() else 1
```

New text:

```
    return 1
```

### `u137.C3_choices_dropped`

Let the parser take any word as a kind

- File: `src/cratekit/organize/cli.py`
- Source: `u137.json`, row `C3_choices_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_an_unknown_kind_is_refused_by_name_before_anything_is_read`

Old text:

```
        choices=KINDS,

```

New text:

```
(empty)
```

### `u137.R1_adopt_gate`

Plan the adoption whatever the selection

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u137.json`, row `R1_adopt_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize.py::test_a_mixed_selection_plans_the_named_kinds_on_each_side_and_no_other`
  - `tests/test_organize.py::test_only_yours_lists_on_each_side_exactly_what_the_full_verb_lists`
  - `tests/test_organize.py::test_only_yours_shows_a_refused_rotation_since_it_is_why_the_listing_is_short`

Old text:

```
    if area.wants(ADOPT):
```

New text:

```
    if True:
```

### `u246.S6_inspiration_planned_live`

assert_read_back (inspiration): the planned set built from the live rows, so the refusal names no unplanned row

- File: `src/cratekit/organize/inspiration.py`
- Source: `u246.json`, row `S6_inspiration_planned_live`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`, `tests/test_u242_taken.py`, `tests/test_write_session.py`, `tests/test_organize.py`
- Collected: 327 against a baseline of 327
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

### `u144-a.A2_two_of_one_name`

Plan: drop the two account sets of one name check, so both are read and planned

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-a.json`, row `A2_two_of_one_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_two_account_sets_of_one_name_are_both_left`

Old text:

```
        if named[name] > 1:
```

New text:

```
        if False:
```

### `u144-c.C7_folder_warning`

Area: warn only for an unread set, not for an unread sets folder

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u144-c.json`, row `C7_folder_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_sets_folder_that_cannot_be_listed_is_named_and_the_rest_still_plan`

Old text:

```
        if row.action in (inspiration.UNREAD, inspiration.FOLDER_UNREAD)
```

New text:

```
        if row.action == inspiration.UNREAD
```

### `r1295.M9_misses_unsorted`

_matched: misses kept unread first rather than in set order

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M9_misses_unsorted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_miss_the_library_lacks_ahead_of_an_unread_track_keeps_set_order`

Old text:

```
tuple(sorted(misses, key=lambda miss: miss.position))
```

New text:

```
tuple(misses)
```

### `u144-c.C5_export_module`

Area: plan the step with the export module off

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u144-c.json`, row `C5_export_module`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_profile_without_the_export_module_lists_the_step`

Old text:

```
    if available is not None and EXPORT_MODULE not in available:
```

New text:

```
    if False:
```

### `u144-a.A1_skip_rule`

Plan: drop the skip of a set INSPIRATION already holds, so it is read and planned again

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-a.json`, row `A1_skip_rule`
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
            rows.append(SetRow(name, playlist_id, folder, SKIP))
```

New text:

```
        if False:
            rows.append(SetRow(name, playlist_id, folder, SKIP))
```

### `u144-c.C6_native_only`

Area: drop the refusal of an intake tree still on the xml bridge

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u144-c.json`, row `C6_native_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_an_intake_tree_on_the_bridge_refuses_the_step`

Old text:

```
        set_playlist.assert_native(ingest.intake_medium(cfg), landing=False)
```

New text:

```
        pass
```

### `u147-a.M1_two_root_folders`

mirror.plan: drop the refusal of two root folders of the mirror's name, so the first is adopted

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u147-a.json`, row `M1_two_root_folders`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_two_root_folders_of_the_name_refuse_that_genre_and_the_rest_proceeds`

Old text:

```
        if len(named) > 1:
            raise ambiguous(folder.name, named)

```

New text:

```
(empty)
```

### `r1289.M14_mirror_unread_branch`

mirror_downloads.plan: drop the unread branch, so an unread wanted track is named as one the provider did not list

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `r1289.json`, row `M14_mirror_unread_branch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`
- Collected: 103 against a baseline of 103
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_an_untitled_track_on_a_mirrored_playlist_is_named_and_the_others_queue`

Old text:

```
            if track in unread:
```

New text:

```
            if False:
```

### `r1031.M15_seen_not_seeded`

add_steps: rebuild from the frozen library with no frozen matches, the review's row one

- File: `src/cratekit/organize/account_mirror.py`
- Source: `r1031.json`, row `M15_seen_not_seeded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`, `tests/test_organize.py`
- Collected: 166 against a baseline of 166
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_rematch_on_the_run_that_answers_asks_nothing_and_says_so`
  - `tests/test_organize_mirror_frozen.py::test_the_frozen_matches_answer_a_row_the_ledger_could_not_remember`
  - `tests/test_organize_mirror_frozen.py::test_the_frozen_matches_stand_over_a_link_recorded_between_the_acts`

Old text:

```
        seen=frozen.matches if frozen is not None else None,
```

New text:

```
        seen=None,
```

### `r1031.M11_filter_removed`

ledger._load: keep a miss of a row the ledger links

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r1031.json`, row `M11_filter_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_ledger_holding_a_link_and_a_miss_of_one_row_reads_the_link`

Old text:

```
            and str(content_id) not in linked
```

New text:

```
            and True
```

### `r1031.M12_link_keeps_its_miss`

ledger.record_mirror_links: leave the row's miss in the document when it is linked

- File: `src/cratekit/modules/outbound/ledger_settle.py`
- Source: `r1031.json`, row `M12_link_keeps_its_miss`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_settle.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_linking_a_row_takes_its_miss_out_of_the_document`

Old text:

```
                document["mirror_misses"].pop(str(content_id), None)
```

New text:

```
                pass
```

### `u222.M25_steps_not_frozen`

_record: freeze no step, so a stale answer names every step as one the gate did not show

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u222.json`, row `M25_steps_not_frozen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 251 against a baseline of 251
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize.py::test_an_account_change_between_the_mirrors_acts_is_stale_and_says_what_moved`
  - `tests/test_organize.py::test_the_gate_freezes_every_step_of_the_full_account_area`
  - `tests/test_organize_mirror_frozen_u222.py::test_a_write_outside_any_mirrored_playlist_between_the_acts_is_not_stale`
  - `tests/test_organize_mirror_frozen_u222.py::test_an_account_change_between_the_acts_is_stale_and_names_its_folder_and_playlist`
  - `tests/test_organize_mirror_frozen_u222.py::test_an_older_record_or_an_unreadable_snapshot_or_step_is_planned_afresh`
  - `tests/test_organize_mirror_frozen_u222.py::test_with_nothing_between_the_acts_the_apply_rebuilds_the_frozen_plan`

Old text:

```
            steps=area.steps,
```

New text:

```
            steps=(),
```

### `u222.M11_decided_freeze_shown`

_record: freeze a decided run's fresh plan as shown by its gate (review round one's BLOCKING)

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u222.json`, row `M11_decided_freeze_shown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 251 against a baseline of 251
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_decided_run_with_no_frozen_plan_says_it_planned_afresh`
  - `tests/test_organize_mirror_frozen_u222.py::test_a_plan_made_afresh_by_a_decided_run_is_never_read_as_what_the_gate_showed`

Old text:

```
            shown=not run.decided,
```

New text:

```
            shown=True,
```

### `u222.M3_overlay_any_remote_id`

overlay: take the frozen snapshot for a playlist made again under another remote id

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222.json`, row `M3_overlay_any_remote_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 251 against a baseline of 251
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_playlist_made_again_between_the_acts_reads_its_snapshot_now`

Old text:

```
            if held is not None and held[0] == one.remote_id:
```

New text:

```
            if held is not None:
```

### `u222.M14_moved_new_step_silent`

moved: say nothing of a step the gate did not show

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222.json`, row `M14_moved_new_step_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 251 against a baseline of 251
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_step_new_since_the_gate_and_one_gone_are_named`

Old text:

```
            said.append(f"{step.title}, which the gate did not show")
            continue
```

New text:

```
            continue
```

### `u150.A4_listed_step`

account_mirror.add_steps: show no listed step for an INBOX not mirrored, so the gate is silent about it

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u150.json`, row `A4_listed_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror.py`, `tests/test_organize.py`
- Collected: 161 against a baseline of 161
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_an_inbox_that_cannot_be_read_is_listed_and_nothing_of_it_is_removed`

Old text:

```
    if library.inbox:
        area.steps.append(
```

New text:

```
    if False:
        area.steps.append(
```

### `u150.M5_apply_removes`

mirror.apply: skip the playlist removal, so the gate names a removal the apply never performs

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u150.json`, row `M5_apply_removes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 103 against a baseline of 103
- Kills: 4 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_a_batch_the_rotation_moved_into_old_plans_the_removal_of_its_playlist_and_nothing_else`
  - `tests/test_organize_mirror_inbox.py::test_a_deleted_inbox_folder_with_only_removals_left_is_not_made_again`
  - `tests/test_organize_mirror_inbox.py::test_a_playlist_removal_refused_for_any_other_reason_is_raised`
  - `tests/test_organize_mirror_inbox.py::test_a_playlist_removal_refused_with_nothing_sent_is_kept_named_and_planned_again`

Old text:

```
            account.remove_playlist(remote_id)
        except CratekitError as exc:
```

New text:

```
            pass
        except CratekitError as exc:
```

### `u150.L1_forget_checks_id`

ledger.forget_mirror_playlist: drop the identifier check, so a playlist recorded under the title since is forgotten in its place

- File: `src/cratekit/modules/outbound/ledger_settle.py`
- Source: `u150.json`, row `L1_forget_checks_id`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_settle.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_forgetting_a_mirrored_playlist_drops_only_the_record_of_that_identifier`

Old text:

```
        if not entry or str(entry.get("remote_id") or "") != str(remote_id):
            return
```

New text:

```
        if not entry:
            return
```

### `u267.M1_report_shares_nothing`

organize: the report makes no shared read, so every reader opens its own handle again, seven opens

- File: `src/cratekit/organize/cli.py`
- Source: `u267.json`, row `M1_report_shares_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_organize.py`, `tests/test_organize_inspiration.py`
- Collected: 147 against a baseline of 147
- Kills: 5 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_report_reads_inspiration_twice_through_one_handle_and_locks_nothing_meanwhile`
  - `tests/test_organize_one_read.py::test_a_failure_nobody_expected_still_closes_the_handle`
  - `tests/test_organize_one_read.py::test_a_step_that_refuses_after_the_open_leaves_no_handle_open`
  - `tests/test_organize_one_read.py::test_the_report_opens_the_database_once_and_closes_it_once`
  - `tests/test_organize_one_read.py::test_the_sets_step_reads_inspiration_through_the_one_handle`

Old text:

```
    one_read = rb_writer.SharedRead(cfg) if report else None
```

New text:

```
    one_read = None
```

### `u143-e.P1_still_at_root`

Apply: remove a playlist moved into a folder since the gate was answered

- File: `src/cratekit/organize/root.py`
- Source: `u143-e.json`, row `P1_still_at_root`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_root.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_playlist_moved_into_a_folder_since_the_plan_is_kept`

Old text:

```
    if row.target in in_folders:
```

New text:

```
    if False:
```

### `u143-b.L1_nested_stays`

Legacy: plan a folder's removal when it holds a folder but no playlist

- File: `src/cratekit/organize/root.py`
- Source: `u143-b.json`, row `L1_nested_stays`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_root.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_legacy_folder_holding_a_folder_stays_and_its_folder_is_not_moved`

Old text:

```
    if not held and not nested:
```

New text:

```
    if not held:
```

### `u255.S1_member_already_on`

add_to_playlist: send the add for a track the membership already holds, an existing guard

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `S1_member_already_on`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 338 against a baseline of 338
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_a_track_already_on_the_playlist_makes_no_request_at_all`
  - `tests/test_outbound_tidal_account.py::test_a_member_already_on_the_playlist_makes_no_write`

Old text:

```
        if identifier in members:
            return
        self._held
```

New text:

```
        if False:
            return
        self._held
```

### `u255.S2_read_back_trusts_the_cache`

add_to_playlist: an answer without the track is checked against the cached membership, not read back, an existing guard

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `S2_read_back_trusts_the_cache`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 338 against a baseline of 338
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_a_track_added_elsewhere_meanwhile_lands_once_and_is_read_back`
  - `tests/test_outbound_add_requests.py::test_an_add_answered_without_the_track_reads_the_playlist_back_and_refuses`
  - `tests/test_outbound_tidal_account.py::test_an_empty_answer_for_a_track_the_playlist_now_holds_is_not_a_failure`

Old text:

```
            del self._members[playlist_id]
            if identifier not in self._membership(playlist_id):
```

New text:

```
            if identifier not in self._membership(playlist_id):
```

### `u270.E2_landed_only_what_was_answered`

apply: record every track sent, answered or not, so the ledger names a track the playlist does not hold

- File: `src/cratekit/modules/outbound/export.py`
- Source: `u270.json`, row `E2_landed_only_what_was_answered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_export_batches.py`, `tests/test_outbound_workers.py`, `tests/test_outbound_add_requests.py`
- Collected: 169 against a baseline of 169
- Kills: 4 (killed)
- Killed:
  - `tests/test_outbound_export_batches.py::test_a_batch_answered_in_part_on_the_real_client_is_settled_by_one_read_back`
  - `tests/test_outbound_export_batches.py::test_a_batch_answered_in_part_records_only_what_the_answer_names`
  - `tests/test_outbound_export_batches.py::test_two_rows_matched_to_one_refused_track_are_both_refused`
  - `tests/test_outbound_workers.py::test_a_track_the_provider_would_not_add_fails_its_item_alone_and_is_never_recorded`

Old text:

```
    landed = {local: remote for local, remote in lacking.items() if remote in answered}
```

New text:

```
    landed = {local: remote for local, remote in lacking.items()}
```

### `u270.C2_stop_while_planning`

run_export_items: never ask stop while a batch is planned, so a signal still sends the batch's add

- File: `src/cratekit/export/cli.py`
- Source: `u270.json`, row `C2_stop_while_planning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_export_batches.py`, `tests/test_outbound_workers.py`
- Collected: 145 against a baseline of 145
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_export_batches.py::test_a_stop_asked_while_a_batch_is_planned_writes_none_of_it`

Old text:

```
        if stop():
            return None
```

New text:

```
        if False:
            return None
```

### `u220.A23_pause_index`

_pause: index the pauses by the attempt with no repeat of the last

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u220.json`, row `A23_pause_index`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 283 against a baseline of 283
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_more_412s_than_pauses_repeat_the_last_pause`

Old text:

```
    return ORDER_PAUSES[min(attempt, len(ORDER_PAUSES)) - 1]
```

New text:

```
    return ORDER_PAUSES[attempt - 1]
```

### `r1308.M6_after_by_length`

_removal_read_back: judge the tracks after by their number, not their content

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M6_after_by_length`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 388 against a baseline of 388
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

### `r1032.A9_album_narrow_unfolded`

_on_album: compare the album unfolded, so case and spacing defeat the narrowing

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r1032.json`, row `A9_album_narrow_unfolded`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_organize_mirror_tie.py`
- Collected: 118 against a baseline of 118
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_the_files_album_narrows_a_tie_under_the_products_own_fold`

Old text:

```
        remote for remote in remotes if wanted and match.fold(_album_name(tracks[remote])) == wanted
```

New text:

```
        remote for remote in remotes if wanted and _album_name(tracks[remote]) == album
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

### `r1032.A2_tie_always_broken`

_among: break the tie whatever the caller asked, so a heart or a pair takes a release R-572 refuses

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r1032.json`, row `A2_tie_always_broken`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_sync_pair.py`, `tests/test_organize_mirror_tie.py`
- Collected: 316 against a baseline of 316
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
        if any_agreeing and not unreadable:
```

New text:

```
        if not unreadable:
```

### `u208.M22_adapter_hearts_half`

_among: drop the hearts half of the tie flag, so two hearts the album narrows to one are not a tie

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `u208.json`, row `M22_adapter_hearts_half`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_tie.py`
- Collected: 134 against a baseline of 134
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

### `r356-a.A8_first_billed_artist_not_required`

A row naming only the guest agrees

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r356-a.json`, row `A8_first_billed_artist_not_required`
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
    return bool(first) and first <= ours and ours - billed <= _JOINERS
```

New text:

```
    return bool(first) and ours - billed <= _JOINERS
```

### `r356-b.B9_export_item_report_drops_the_reason`

The export item report writes no reason, so neither the artifact nor the envelope can say it

- File: `src/cratekit/export/cli.py`
- Source: `r356-b.json`, row `B9_export_item_report_drops_the_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_an_export_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`

Old text:

```
                "reason": row.reason,

```

New text:

```
(empty)
```

### `r358-round-2.A7_empty_title_message`

Reword the empty-title refusal, never append to it

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r358-round-2.json`, row `A7_empty_title_message`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_rename_with_no_title_is_refused_before_the_client_sees_it[   ]`
  - `tests/test_outbound_tidal_account.py::test_a_rename_with_no_title_is_refused_before_the_client_sees_it[\n]`
  - `tests/test_outbound_tidal_account.py::test_a_rename_with_no_title_is_refused_before_the_client_sees_it[]`

Old text:

```
                f"a rename of the playlist {playlist_id} was asked for with no "
                f"title; the client reads a falsy title as keep the current one "
                f"and answers that it succeeded, so nothing was sent",
```

New text:

```
                f"the playlist {playlist_id} was given a blank title, which the "
                f"client would read as an instruction to keep the current one",
```

### `r356-a.A11_row_title_read_one_way_only`

Only the first reading of the row's title is compared

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r356-a.json`, row `A11_row_title_read_one_way_only`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_title_that_reads_two_ways_agrees_under_either_and_still_needs_one`

Old text:

```
for one in row.readings}
```

New text:

```
for one in (row,)}
```

### `r358.A6_retry_coefficient`

Take the rename's retry to zero, the way a create takes it

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r358.json`, row `A6_retry_coefficient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_rename_the_provider_refuses_once_is_retried_once_into_the_same_title`

Old text:

```
        accepted = self._call(doing, lambda: retitle(title=wanted))
```

New text:

```
        accepted = self._call(doing, lambda: retitle(title=wanted), retries=0)
```

### `u226.M7_reading_takes_window`

_reading: the window read is the reading even when the unpaged read is whole

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u226.json`, row `M7_reading_takes_window`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`
- Collected: 442 against a baseline of 442
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

### `r850-a.E10_concluded_not_called`

shell.resume: never ask the verb what its finished run says, so the unmatched warning is never given

- File: `src/cratekit/modules/outbound/shell.py`
- Source: `r850-a.json`, row `E10_concluded_not_called`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_outbound_tidal_account.py`
- Collected: 236 against a baseline of 236
- Kills: 4 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_filing_failure_is_a_warning_on_a_finished_export`
  - `tests/test_outbound_workers.py::test_a_folder_changed_after_the_queue_leaves_the_playlist_at_the_root_with_a_warning`
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`
  - `tests/test_outbound_workers.py::test_an_export_with_an_unmatched_track_counts_and_names_it_on_both_renderers`

Old text:

```
        said = concluded(data["progress"]["outbound"]) if concluded is not None else ()
```

New text:

```
        said = ()
```

### `u51-item-derivation.D2_ambiguous_playlist`

Take the first match instead of refusing when several carry the name

- File: `src/cratekit/modules/outbound/source.py`
- Source: `u51-item-derivation.json`, row `D2_ambiguous_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_name_two_playlists_carry_refuses_and_names_both_paths`

Old text:

```
    if len(matched) > 1:
```

New text:

```
    if False:
```

### `u131.K13_unfiled_warning`

export concluded: drop the unfiled warning, so a playlist left at the root is never said

- File: `src/cratekit/export/cli.py`
- Source: `u131.json`, row `K13_unfiled_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 123 against a baseline of 123
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_filing_failure_is_a_warning_on_a_finished_export`
  - `tests/test_outbound_workers.py::test_a_folder_changed_after_the_queue_leaves_the_playlist_at_the_root_with_a_warning`

Old text:

```
        for reason in outbound.get("unfiled") or ()
```

New text:

```
        for reason in ()
```

### `r227.S4_utc_instant_in_the_block`

The shown block spells the instant in UTC rather than in the machine's zone

- File: `src/cratekit/modules/outbound/shell.py`
- Source: `r227.json`, row `S4_utc_instant_in_the_block`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_the_date_is_the_persons_own_and_not_greenwichs`

Old text:

```
            age.written.astimezone().replace(microsecond=0).isoformat()
```

New text:

```
            age.written.replace(microsecond=0).isoformat()
```

### `r227.S5_envelope_drops_the_age`

queue_warnings takes the age and says nothing about it

- File: `src/cratekit/modules/outbound/shell.py`
- Source: `r227.json`, row `S5_envelope_drops_the_age`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 123 against a baseline of 123
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_the_queueing_envelope_warns_that_the_export_is_old[export.playlist]`
  - `tests/test_outbound_workers.py::test_the_queueing_envelope_warns_that_the_export_is_old[sync.favorites]`

Old text:

```
    warnings: list[dict[str, str]] = [*age_warnings(age)]
```

New text:

```
    warnings: list[dict[str, str]] = []
```

### `u131.K5_recorded_folder`

kinds.decide: ignore the recorded folder, so a folder a person renamed is replaced by a new one

- File: `src/cratekit/modules/outbound/kinds.py`
- Source: `u131.json`, row `K5_recorded_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_playlist_kinds.py`, `tests/test_organize.py`
- Collected: 109 against a baseline of 109
- Kills: 2 (killed)
- Killed:
  - `tests/test_playlist_kinds.py::test_a_playlist_marked_after_it_was_filed_in_mine_reaches_its_year`
  - `tests/test_playlist_kinds.py::test_a_renamed_playlist_and_a_renamed_folder_stay_where_they_are`

Old text:

```
    if recorded.folder_id and recorded.folder_id in root:
```

New text:

```
    if False:
```

### `r1305.A4_account_reads_its_own_link_only`

_session_refused: read the failure alone and no link of it, so a rejection the client rewraps is told to wait

- File: `src/cratekit/modules/outbound/account.py`
- Source: `r1305.json`, row `A4_account_reads_its_own_link_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_rejection_bodies.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`
- Collected: 197 against a baseline of 197
- Kills: 7 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_rejection_the_client_rewraps_is_still_read_as_a_rejected_session`
  - `tests/test_provider_rejection_bodies.py::test_a_login_failure_that_is_no_rejection_is_a_wait[outage]`
  - `tests/test_provider_rejection_bodies.py::test_a_rejection_whose_body_is_not_json_drops_the_held_account`
  - `tests/test_provider_rejection_bodies.py::test_a_rejection_whose_body_is_not_json_rewrapped_by_the_client_still_asks_for_a_login`
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

### `u261.A4_refusal_drops_no_session`

account._forget_refused: drop the adapter and keep the shared session it was built over, so a 401 on the account leaves the catalogue the refused client

- File: `src/cratekit/modules/outbound/account.py`
- Source: `u261.json`, row `A4_refusal_drops_no_session`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`
- Collected: 143 against a baseline of 143
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

### `r836-c.F1_build_skips_pruned`

folders.plan: a track a prune took off is added again by the next label build

- File: `src/cratekit/modules/outbound/folders.py`
- Source: `r836-c.json`, row `F1_build_skips_pruned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 404 against a baseline of 404
- Kills: 1 (killed)
- Killed:
  - `tests/test_prune.py::test_a_pruned_track_is_not_put_back_by_the_next_build`

Old text:

```
            asked = recorded.added | recorded.refused | recorded.pruned
```

New text:

```
            asked = recorded.added | recorded.refused
```

### `r836-b.L4_pruned_leaves_added`

ledger._moved_to_pruned: a taken track stays in added, so the next prune asks the account for it again

- File: `src/cratekit/modules/outbound/ledger_settle.py`
- Source: `r836-b.json`, row `L4_pruned_leaves_added`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_settle.py, was in src/cratekit/modules/outbound/ledger.py
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

### `u174.O2_seen_skips_a_filed_pass`

_mark_steps: plan a pass with an intake file a second time by its native record

- File: `src/cratekit/organize/account.py`
- Source: `u174.json`, row `O2_seen_skips_a_filed_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`
- Collected: 164 against a baseline of 164
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_pass_with_an_intake_file_is_planned_once_by_its_file`

Old text:

```
        if name in seen:
            continue
```

New text:

```
        if False:
            continue
```

### `u216.M22_write_drops_held`

_write: the folder record is written without what it held

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u216.json`, row `M22_write_drops_held`
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
                    **({"held": sorted(one.held)} if one.held is not None else {}),
```

New text:

```
                    **({}),
```

### `u221.R15_mark_drops_the_hold`

PairStore.mark: record no hold on a new pair, so a backfilled twin falls to the time rule

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u221.json`, row `R15_mark_drops_the_hold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 84 against a baseline of 84
- Kills: 14 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_backfilled_pair_merges_both_ways_and_queues_the_added_track_once`
  - `tests/test_sync_twins_hold.py::test_a_held_track_whose_linked_row_left_the_library_is_still_counted_and_released`
  - `tests/test_sync_twins_hold.py::test_a_landing_twin_records_an_empty_hold`
  - `tests/test_sync_twins_hold.py::test_a_name_that_is_no_twin_is_refused_and_nothing_is_planned`
  - `tests/test_sync_twins_hold.py::test_a_second_twin_stays_held_when_the_first_is_released`
  - `tests/test_sync_twins_hold.py::test_a_track_added_later_on_the_account_is_queued_and_the_held_stay_held`
  - `tests/test_sync_twins_hold.py::test_a_twin_paired_again_since_the_plan_is_left_held`
  - `tests/test_sync_twins_hold.py::test_a_twin_with_three_missing_tracks_queues_none_and_names_three_on_hold`
  - `tests/test_sync_twins_hold.py::test_an_abort_lets_nothing_go`
  - `tests/test_sync_twins_hold.py::test_release_hold_passes_over_a_pair_that_is_no_twin_and_one_holding_nothing`
  - `tests/test_sync_twins_hold.py::test_release_needs_names_or_all_and_not_both[args0]`
  - `tests/test_sync_twins_hold.py::test_release_needs_names_or_all_and_not_both[args1]`
  - `tests/test_sync_twins_hold.py::test_releasing_the_twin_queues_its_three_at_the_next_sync`
  - `tests/test_sync_twins_hold.py::test_the_hold_survives_a_recorded_snapshot_and_a_mark_of_the_same_pair`

Old text:

```
                on_hold=(
                    None
                    if on_hold is None
                    else MappingProxyType({str(k): str(v) for k, v in on_hold.items() if k})
                ),
```

New text:

```
                on_hold=None,
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

### `r837-a.A14_not_listed_not_blamed`

sets.apply_archive: a playlist the folder does not list yet is read as retitled by somebody

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `r837-a.json`, row `A14_not_listed_not_blamed`
- Moved: the same NOT_LISTED guard in sets.apply_archive's recheck; its comment was shortened to one line, so the anchor carries the new comment and the condition is reverted the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_playlist_the_folder_does_not_list_yet_is_not_renamed_or_blamed`

Old text:

```
    if now is None:
        # NOT A RETITLE: a listing without it says nothing about its title.
```

New text:

```
    if False:
        # NOT A RETITLE: a listing without it says nothing about its title.
```

### `r228-operator.D10_pink_warning_gone`

queue_warnings: drop the pink missing warning

- File: `src/cratekit/modules/outbound/shell.py`
- Source: `r228-operator.json`, row `D10_pink_warning_gone`
- Moved: queue_warnings now builds its warnings from one table of (due, code, message) entries rather than an if and append per warning, so the pink missing warning is dropped by deleting its entry from that table
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_pink.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_pink.py::test_pink_missing_is_warned_beside_dangling`

Old text:

```
        (
            resolved.pink_missing, "favorites-pink-export-missing",
            f"{len(resolved.pink_missing)} pink row(s) the library carries are not in the "
            f"export's collection and are not queued: {', '.join(resolved.pink_missing)}",
        ),

```

New text:

```
(empty)
```

### `u123.T1_adapter_vouching`

Drop the adapter's ledger check before a playlist removal

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u123.json`, row `T1_adapter_vouching`
- Moved: the same ledger check at the head of remove_playlist in tidal_account.py; the refusal is now raised through the shared _refused helper instead of refuse, so the text differs and the condition is reverted the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_outbound_tidal_account.py`
- Collected: 151 against a baseline of 151
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_heard.py::test_the_adapter_refuses_a_playlist_the_ledger_does_not_vouch_for_unasked`

Old text:

```
        if self._cfg is None or not ledger.product_made(self._cfg, identifier):
            raise _refused(
                f"the outbound ledger does not record the playlist {identifier} as "
                f"one this product created, so it was not removed and the provider "
```

New text:

```
        if False:
            raise _refused(
                f"the outbound ledger does not record the playlist {identifier} as "
                f"one this product created, so it was not removed and the provider "
```

### `u230.M2_lift_not_in_was`

placed: the lift is ignored in the base places, so the account side still reads as no change

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u230.json`, row `M2_lift_not_in_was`
- Moved: decide's inner placed closure became the module function mirror_edits._placed, which takes lifted as an argument, so the same condition sits four spaces shallower and is reverted the same way
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
        and not (side == "base" and one.place.title in lifted)
    )
```

New text:

```
        and True
    )
```

### `u236.M20_agreed_never_drops`

record_mirror_agreed: never drop a placement the account now holds

- File: `src/cratekit/modules/outbound/ledger_settle.py`
- Source: `u236.json`, row `M20_agreed_never_drops`
- Moved: record_mirror_agreed moved from ledger.py into ledger_settle.py and reads the mirrored folder's record once into record, so the same placed_after call is written shorter there and is bypassed the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 223 against a baseline of 223
- Kills: 3 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_the_ledger_keeps_a_placement_until_the_mirror_finished_its_playlist`
  - `tests/test_organize_mirror_edits_u236.py::test_a_hand_addition_after_the_placement_is_dropped_is_read_as_one`
  - `tests/test_organize_mirror_edits_u236.py::test_the_organize_after_the_favourite_puts_it_in_the_accounts_month`

Old text:

```
            _place(record, name, mirror_edits.placed_after(
                _placements(record.get("placed")).get(name, {}), after, held
            ))
```

New text:

```
            _place(record, name, _placements(record.get("placed")).get(name, {}))
```

### `u236.M12_reader_short_branch`

read edits: drop the placements of a month whose listing failed (round one, finding 4)

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u236.json`, row `M12_reader_short_branch`
- Moved: the reader's two Mirrored constructions, one for a failed listing and one for a read listing, were merged into one that tests listing is None per field, so dropping the failed listing's placements is now placed left empty only when listing is None
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 223 against a baseline of 223
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u236.py::test_a_month_whose_listing_fails_at_the_unfavourite_still_reads_its_placement`

Old text:

```
                rekordbox_added=added,
                placed=ours,
```

New text:

```
                rekordbox_added=added,
                placed=ours if listing is not None else frozenset(),
```

### `u204.P2_acquire_only_unknown`

_carry: an addition the library lacks is queued whatever the snapshots held

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u204.json`, row `P2_acquire_only_unknown`
- Moved: _carry's two held Decisions were folded into one whose acquire flag is computed first, so the same condition now assigns acquire instead of opening an if, and is reverted the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 222 against a baseline of 222
- Kills: 2 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_an_addition_the_library_lacks_is_queued_in_favorites_and_inbox_and_a_known_one_never`
  - `tests/test_organize_mirror_edits_u204.py::test_a_track_a_snapshot_once_held_is_never_queued_again`

Old text:

```
        acquire = kind in ADDITIONS and track not in known
```

New text:

```
        acquire = kind in ADDITIONS
```

### `u147-c.M14_made_in_mirror`

ledger._made_in: a mirrored playlist is no longer vouched for, so no track may come off it (R-836)

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u147-c.json`, row `M14_made_in_mirror`
- Moved: ledger._made_in's loop over every mirrored playlist's record became one any() over the shared _mirrored iterator, so the mirrored vouching is removed by returning False in its place
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_a_track_added_by_hand_to_a_mirrored_playlist_is_removed_and_named`

Old text:

```
    # U147. A mirrored playlist is only ever created, never adopted.
    return any(str(entry.get("remote_id") or "") == wanted for entry in _mirrored(document))
```

New text:

```
    return False
```

### `u255.S3_answer_absent_passes`

add_to_playlist: a playlist gone mid add is not refused, an existing guard

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `S3_answer_absent_passes`
- Moved: the same guard in add_to_playlist; its provider failure is now built by the shared _gone helper, also used by add_tracks, so the anchor takes the call line before it to stay unique and the condition is reverted the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 338 against a baseline of 338
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_an_add_to_a_playlist_deleted_mid_run_is_the_items_cause`

Old text:

```
        added = self._call(doing, attempt)
        if added is _ABSENT:
            raise _gone(playlist_id, doing)
```

New text:

```
        added = self._call(doing, attempt)
        if False:
            raise _gone(playlist_id, doing)
```

### `r1308.M24_positions_count`

_positions: drop the declared count's match with the tracks read, the guard _reading was split from

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M24_positions_count`
- Moved: the same count check in _positions, whose four conditions were joined onto one line, so the declared count's match is dropped from that line instead of deleting a line of its own
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 388 against a baseline of 388
- Kills: 2 (killed)
- Killed:
  - `tests/test_prune.py::test_a_playlist_with_a_track_the_account_cannot_see_is_refused_with_nothing_sent`
  - `tests/test_prune.py::test_a_settled_track_the_listing_hides_is_not_recorded_as_off`

Old text:

```
        if not _count(declared) or declared != len(members) or not _count(videos) or videos != 0:
```

New text:

```
        if not _count(declared) or not _count(videos) or videos != 0:
```

### `r1032.A10_reason_words_reworded`

_among: reword the tie reason away from the constant the mirror reads

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r1032.json`, row `A10_reason_words_reworded`
- Moved: _among moved from tidal_account.py into the Reads mixin in tidal_reads.py, which reads the constant as service.AGREEING_RELEASES, so the same sentence is reworded the same way there
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_organize_mirror_tie.py`, `tests/test_outbound_workers.py`
- Collected: 241 against a baseline of 241
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize_mirror_tie.py::test_a_tie_beside_a_release_that_cannot_be_read_is_left_out_and_asked_again`
  - `tests/test_outbound_tidal_account.py::test_a_file_with_no_album_tag_stays_unmatched_and_says_the_tag_is_missing`
  - `tests/test_outbound_tidal_account.py::test_a_sweep_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_tidal_account.py::test_an_unreadable_release_beside_the_tie_still_refuses_with_any_agreeing`
  - `tests/test_outbound_tidal_account.py::test_releases_spelled_alike_stay_unmatched_and_the_reason_counts_them`
  - `tests/test_outbound_tidal_account.py::test_without_any_agreeing_the_same_tie_still_refuses_in_the_words_the_mirror_reads`

Old text:

```
            f"{named}{aside}, {len(agreeing)} {service.AGREEING_RELEASES} and the "
```

New text:

```
            f"{named}{aside}, {len(agreeing)} of them match this row's artist, title and version and the "
```

### `u226.M8_unpaged_first`

_reading: the unpaged read taken before the window, so the window's tag is carried

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u226.json`, row `M8_unpaged_first`
- Moved: _reading in tidal_account.py now reads the window into paged in one line instead of through a tracks name, so the same two reads are swapped there, the unpaged one taken first
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`
- Collected: 442 against a baseline of 442
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_removal_past_the_first_hundred_takes_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_a_removal_planned_from_a_lagging_window_takes_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_an_order_past_the_first_hundred_moves_the_track_where_it_stands`

Old text:

```
        paged = [listing.row_id(track) for track in self._listed(playlist_id, playlist)]
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
        paged = [listing.row_id(track) for track in self._listed(playlist_id, playlist)]
```

### `u51-item-derivation.D1_unknown_playlist`

Drop the refusal for a playlist name the document does not carry

- File: `src/cratekit/modules/outbound/source.py`
- Source: `u51-item-derivation.json`, row `D1_unknown_playlist`
- Moved: the same refusal in source.resolve, rewrapped to longer lines with its origin read from the module's _ORIGIN, so the whole if block is deleted at its new text
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 143 against a baseline of 143
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_name_that_is_a_folder_refuses_rather_than_resolving`
  - `tests/test_outbound_workers.py::test_an_export_naming_a_playlist_the_document_lacks_queues_nothing`

Old text:

```
    if not matched:
        raise refuse(
            "export-playlist-unknown",
            f"no playlist in {library.path.name} is named {wanted!r}. A folder of that name is "
            f"not a match either, because a folder holds playlists rather than tracks",
            steps=("name the playlist by its display name, or by its full path joined with /",),
            scope=Scope.RUN,
            origin=_ORIGIN,
            detail={"playlist": wanted},
        )

```

New text:

```
(empty)
```

