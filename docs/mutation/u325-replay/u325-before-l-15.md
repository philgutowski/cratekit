# Mutation table: u325-before-l-15

Measured by `scripts/mutate.py` on 2026-11-22 22:15 UTC, branch `HEAD` at `539638eb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22663 collected. pytest invocations for this batch: 134.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:15 UTC for commit `539638ebe629`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 19, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22663 against 22663. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u161.P6_screen_drops_path` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 59 | 3 | killed |
| `u161.P1_path_back_in_digest` | `src/cratekit/intake/native.py` | user | 1 file(s) | 59 | 5 | killed |
| `u161.P2_parent_in_digest` | `src/cratekit/intake/native.py` | user | 1 file(s) | 59 | 4 | killed |
| `u161.P3_file_name_in_digest` | `src/cratekit/intake/native.py` | user | 1 file(s) | 59 | 2 | killed |
| `u161.P4_device_out` | `src/cratekit/intake/native.py` | user | 1 file(s) | 59 | 2 | killed |
| `u161.P5_master_out` | `src/cratekit/intake/native.py` | user | 1 file(s) | 59 | 2 | killed |
| `u161.S1_playlist_out` | `src/cratekit/intake/native.py` | user | 1 file(s) | 59 | 1 | killed |
| `u161.S2_columns_out` | `src/cratekit/intake/native.py` | user | 1 file(s) | 59 | 1 | killed |
| `u238.M10_question_drops_the_split` | `src/cratekit/label/sync_cli.py` | user | 3 file(s) | 319 | 3 | killed |
| `u238.M11_saved_question_drops_the_split` | `src/cratekit/label/sync_cli.py` | user | 3 file(s) | 319 | 3 | killed |
| `u238.M7_old_question_read_as_count` | `src/cratekit/label/sync_cli.py` | user | 3 file(s) | 319 | 5 | killed |
| `u238.M8_bound_said_as_the_labels` | `src/cratekit/label/sync_cli.py` | user | 3 file(s) | 319 | 8 | killed |
| `u238.M9_nothing_line_loses_the_split` | `src/cratekit/label/sync_cli.py` | user | 3 file(s) | 319 | 2 | killed |
| `r318.P1_withdrawn_branch_removed` | `src/cratekit/write/routing_pass.py` | user | 4 file(s) | 437 | 5 | killed |
| `r318.P2_withdrawn_on_single_tombstone_only` | `src/cratekit/write/routing_pass.py` | user | 4 file(s) | 437 | 1 | killed |
| `r318.P3_unresolved_branch_removed` | `src/cratekit/write/routing_pass.py` | user | 4 file(s) | 437 | 3 | killed |
| `r318.P4_ambiguous_reads_not_imported` | `src/cratekit/write/routing_pass.py` | user | 4 file(s) | 437 | 3 | killed |
| `u51-item-derivation.A2_default_favorites_playlist` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 145 | 27 | killed |
| `u51-item-derivation.D1_unknown_playlist` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 145 | 2 | killed |
| `u51-item-derivation.D2_ambiguous_playlist` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 145 | 1 | killed |
| `u51-item-derivation.D3_empty_playlist` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 145 | 1 | killed |
| `u51-item-derivation.D4_dangling_reported` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 145 | 2 | killed |
| `u51-item-derivation.D5_repeated_deduped` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 145 | 2 | killed |
| `u51-item-derivation.D6_export_required` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 145 | 2 | killed |
| `u79-c.C2_owned_row_searched` | `src/cratekit/intake/missing_cli.py` | user | 3 file(s) | 144 | 2 | killed |
| `u79-c.C3_accepted_held_listed_again` | `src/cratekit/intake/missing_cli.py` | user | 3 file(s) | 144 | 1 | killed |
| `u79-c.C4_nothing_found_is_a_no_op` | `src/cratekit/intake/missing_cli.py` | user | 3 file(s) | 144 | 2 | killed |
| `u79-c.C5_foreign_ref_names_a_row` | `src/cratekit/intake/missing_cli.py` | user | 3 file(s) | 144 | 2 | killed |
| `u79-c.C6_isrc_named_keeps_origin` | `src/cratekit/intake/missing_cli.py` | user | 3 file(s) | 144 | 1 | killed |
| `u79-c.C7_fixed_name` | `src/cratekit/intake/missing_cli.py` | user | 3 file(s) | 144 | 10 | killed |
| `u79-c.C8_asked_is_a_no_op` | `src/cratekit/intake/missing_cli.py` | user | 3 file(s) | 144 | 1 | killed |
| `u100-b.C10_added_message` | `src/cratekit/label/cli.py` | user | 2 file(s) | 47 | 1 | killed |
| `u100-b.C1_name_accepted` | `src/cratekit/label/cli.py` | user | 2 file(s) | 47 | 1 | killed |
| `u100-b.C2_to_accepted` | `src/cratekit/label/cli.py` | user | 2 file(s) | 47 | 1 | killed |
| `u100-b.C3_outcome_always_ok` | `src/cratekit/label/cli.py` | user | 2 file(s) | 47 | 2 | killed |
| `u100-b.C4_empty_says_nothing` | `src/cratekit/label/cli.py` | user | 2 file(s) | 47 | 1 | killed |
| `u100-b.C5_nameless_unreported` | `src/cratekit/label/cli.py` | user | 2 file(s) | 47 | 1 | killed |
| `u100-b.C6_held_name_hidden` | `src/cratekit/label/cli.py` | user | 2 file(s) | 47 | 1 | killed |
| `u100-b.C7_refused_reads_as_note` | `src/cratekit/label/cli.py` | user | 2 file(s) | 47 | 1 | killed |
| `u100-b.C9_dispatch` | `src/cratekit/label/cli.py` | user | 2 file(s) | 47 | 12 | killed |
| `u149.T10_any_year_folder` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 46 | 1 | killed |
| `u149.T11_excluded_read` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 46 | 1 | killed |
| `u149.T13_paired_planned_again` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 46 | 1 | killed |
| `u149.T15_unplanned_membership` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 46 | 1 | killed |
| `u149.T16_unplanned_playlist_row` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 46 | 2 | killed |
| `u149.T20_short_snapshot` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 46 | 1 | killed |
| `u149.T7_ambiguous_takes_first` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 46 | 2 | killed |
| `u149.T8_mirror_link_skipped` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 46 | 1 | killed |
| `u149.T9_removed_row_linked` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 46 | 1 | killed |
| `u164.H1_watch_recorded` | `src/cratekit/intake/land_cli.py` | maintainer | 1 file(s) | 36 | 1 | killed |
| `u164.H2_scratch_folder` | `src/cratekit/intake/land_cli.py` | maintainer | 1 file(s) | 36 | 20 | killed |
| `u188.M10_detail_mapped_dropped` | `src/cratekit/intake/land_cli.py` | maintainer | 1 file(s) | 36 | 1 | killed |
| `u188.M11_fields_last_part` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 36 | 2 | killed |
| `u188.M12_fields_keep_indices` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 36 | 2 | killed |
| `u188.M13_fields_repeated` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 36 | 2 | killed |
| `u188.M7_signs_swapped` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 36 | 2 | killed |
| `u188.M8_fields_left_out` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 36 | 1 | killed |
| `u188.M9_pairs_left_out` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 36 | 1 | killed |
| `r375-b.T3_a_noop_claims_a_commit` | `src/cratekit/write/trees.py` | user | 3 file(s) | 196 | 1 | killed |
| `r375-b.T4_noop_bound_off_by_one` | `src/cratekit/write/trees.py` | user | 3 file(s) | 196 | 4 | killed |
| `r375-b.T5_witnessed_commit_not_recorded` | `src/cratekit/write/trees.py` | user | 3 file(s) | 196 | 1 | killed |
| `r375-b.T7_commit_recorded_after_the_fingerprint` | `src/cratekit/write/trees.py` | user | 3 file(s) | 196 | 1 | killed |
| `r375-b.T8_counts_filed_as_updates` | `src/cratekit/write/trees.py` | user | 3 file(s) | 196 | 3 | killed |
| `r375-c.T6_every_raise_read_as_a_commit_again` | `src/cratekit/write/trees.py` | user | 3 file(s) | 196 | 1 | killed |
| `u201-composites.C5_leave_nothing` | `src/cratekit/organize/mirror_edits.py` | user | 5 file(s) | 195 | 6 | killed |
| `u201.O1_latch` | `src/cratekit/organize/mirror_edits.py` | user | 5 file(s) | 195 | 1 | killed |
| `u201.O2_stale` | `src/cratekit/organize/mirror_edits.py` | user | 5 file(s) | 195 | 1 | killed |
| `u201.O3_target_bucket` | `src/cratekit/organize/mirror_edits.py` | user | 5 file(s) | 195 | 6 | killed |
| `u201-composites.C4_settle_none` | `src/cratekit/modules/outbound/ledger.py` | user | 5 file(s) | 195 | 3 | killed |
| `u201.L1_agreed_own_playlist` | `src/cratekit/modules/outbound/ledger.py` | user | 5 file(s) | 195 | 1 | killed |
| `u100-a.R1_slug_only_presence` | `src/cratekit/label/registry.py` | user | 4 file(s) | 22663 | 0 (promoted) | zero |
| `u100-a.R2_no_presence_check` | `src/cratekit/label/registry.py` | user | 4 file(s) | 401 | 6 | killed |
| `u100-a.R3_presence_before_the_batch` | `src/cratekit/label/registry.py` | user | 4 file(s) | 401 | 1 | killed |
| `u100-a.R4_slug_refusal_aborts` | `src/cratekit/label/registry.py` | user | 4 file(s) | 401 | 1 | killed |
| `u239.L01_remember_land_only` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 275 | 1 | killed |
| `u239.L02_remember_owner` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 275 | 2 | killed |
| `u239.L03_remember_called` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 275 | 6 | killed |
| `u239.L05_commands_added` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 275 | 3 | killed |
| `u239.L06_unrecorded_warning` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 275 | 1 | killed |
| `u322.M21_suggest_uses_folder_binder` | `src/cratekit/tagging/suggest_cli.py` | user | 6 file(s) | 392 | 1 | killed |
| `u322.M20_backlog_uses_folder_binder` | `src/cratekit/tagging/backlog_cli.py` | user | 6 file(s) | 392 | 1 | killed |
| `u322.M22_backlog_partly_clause_gone` | `src/cratekit/tagging/backlog_cli.py` | user | 6 file(s) | 392 | 1 | killed |
| `u322.M24_backlog_line_gone` | `src/cratekit/tagging/backlog_cli.py` | user | 6 file(s) | 392 | 2 | killed |
| `r1032.A11_empty_album_narrows` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 116 | 1 | killed |
| `r1032.A1_adapter_ignores_any_agreeing` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 116 | 13 | killed |
| `r1032.A3_unreadable_tie_broken` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 116 | 3 | killed |
| `r1032.A6_first_listed_not_lowest` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 116 | 7 | killed |
| `r1032.A7_lowest_by_characters` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 116 | 1 | killed |
| `r1032.A8_album_narrow_drops_all` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 116 | 11 | killed |
| `r1032.A9_album_narrow_unfolded` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 116 | 1 | killed |
| `u216.M21_reserve_adopt_empty` | `src/cratekit/modules/outbound/pairs.py` | user | 12 file(s) | 383 | 9 | killed |
| `u216.M22_write_drops_held` | `src/cratekit/modules/outbound/pairs.py` | user | 12 file(s) | 383 | 12 | killed |
| `u216.M23_read_drops_held` | `src/cratekit/modules/outbound/pairs.py` | user | 12 file(s) | 383 | 12 | killed |
| `u216.M24_read_unvalidated` | `src/cratekit/modules/outbound/pairs.py` | user | 12 file(s) | 383 | 4 | killed |
| `r259.L1_job_cache_read` | `src/cratekit/label/cli.py` | maintainer | 4 file(s) | 551 | 1 | killed |
| `r504-a.A11_boundary_refuses` | `src/cratekit/label/cli.py` | user | 4 file(s) | 551 | 5 | killed |
| `r504-a.A12_boundary_drops_short` | `src/cratekit/label/cli.py` | user | 4 file(s) | 551 | 5 | killed |
| `u242.M11_strip_skips_the_held_check` | `src/cratekit/sync/strip_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u242.M12_composite` | `src/cratekit/sync/strip_cli.py` | user | 1 file(s) | 46 | 11 | killed |
| `u242.M12_strip_skips_the_migration` | `src/cratekit/sync/strip_cli.py` | user | 1 file(s) | 46 | 14 | killed |
| `u242.M13_strip_no_collision_with_others` | `src/cratekit/sync/strip_cli.py` | user | 1 file(s) | 46 | 2 | killed |
| `u242.M14_strip_no_collision_between_strips` | `src/cratekit/sync/strip_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u242.M15_strip_collision_case_exact` | `src/cratekit/sync/strip_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u242.M17_strip_no_recheck` | `src/cratekit/sync/strip_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u242.M18_strip_records_no_old_title` | `src/cratekit/sync/strip_cli.py` | user | 1 file(s) | 46 | 4 | killed |
| `r1372.K19_passed_by_strict` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 1 | killed |
| `r1372.K20_passed_by_any_pair` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 1 | killed |
| `r1372.K21_made_pair_unmapped` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 2 | killed |
| `r1376.F14_finished_filter_gone` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 1 | killed |
| `u225.M6_front_keeps_nothing` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 26 | killed |
| `u225.M8_reached_strict_membership` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 3 | killed |
| `u225.M9_finish_ignored` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 3 | killed |
| `r1056.N10_pass_not_required` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 33 | 1 | killed |

## Zero rows and what they owe

- `u100-a.R1_slug_only_presence` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `u161.P6_screen_drops_path`

collection_facts: show the root's name where the database path was, so the screen no longer says which file is written

- File: `src/cratekit/intake/land_cli.py`
- Source: `u161.json`, row `P6_screen_drops_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 59 against a baseline of 59
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_an_answer_given_over_one_file_is_stale_when_the_continuation_opens_another`
  - `tests/test_intake_land_native.py::test_the_gate_screen_names_every_row_its_columns_the_playlist_and_the_database`
  - `tests/test_intake_land_native.py::test_the_same_files_against_a_copy_at_another_path_digest_equal_and_each_screen_names_its_path`

Old text:

```
        "reads and writes": str(rows.database),
```

New text:

```
        "reads and writes": str(rows.root_name),
```

### `u161.P1_path_back_in_digest`

native.identity: digest str(plan.database) again, the line U161 removed, so a copy rehearsal can never match

- File: `src/cratekit/intake/native.py`
- Source: `u161.json`, row `P1_path_back_in_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 59 against a baseline of 59
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_decision_recorded_against_the_path_bearing_digest_is_stale_and_writes_nothing`
  - `tests/test_intake_land_native.py::test_an_answer_given_over_one_file_is_stale_when_the_continuation_opens_another`
  - `tests/test_intake_land_native.py::test_the_engine_digest_moves_with_one_row_and_one_playlist_and_not_with_the_path`
  - `tests/test_intake_land_native.py::test_the_engine_identity_names_the_device_and_master_id_and_no_database_path`
  - `tests/test_intake_land_native.py::test_the_same_files_against_a_copy_at_another_path_digest_equal_and_each_screen_names_its_path`

Old text:

```
        "device": plan.device_id,
        "master_db_id": plan.master_db_id,
```

New text:

```
        "database": str(plan.database),
        "device": plan.device_id,
        "master_db_id": plan.master_db_id,
```

### `u161.P2_parent_in_digest`

native.identity: digest the database's folder under another key, a path the old key's name check would not see

- File: `src/cratekit/intake/native.py`
- Source: `u161.json`, row `P2_parent_in_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 59 against a baseline of 59
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_an_answer_given_over_one_file_is_stale_when_the_continuation_opens_another`
  - `tests/test_intake_land_native.py::test_the_engine_digest_moves_with_one_row_and_one_playlist_and_not_with_the_path`
  - `tests/test_intake_land_native.py::test_the_engine_identity_names_the_device_and_master_id_and_no_database_path`
  - `tests/test_intake_land_native.py::test_the_same_files_against_a_copy_at_another_path_digest_equal_and_each_screen_names_its_path`

Old text:

```
        "device": plan.device_id,
        "master_db_id": plan.master_db_id,
```

New text:

```
        "where": str(plan.database.parent),
        "device": plan.device_id,
        "master_db_id": plan.master_db_id,
```

### `u161.P3_file_name_in_digest`

native.identity: digest the database's file name alone, which a copy named differently from master.db would not share

- File: `src/cratekit/intake/native.py`
- Source: `u161.json`, row `P3_file_name_in_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 59 against a baseline of 59
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_an_answer_given_over_one_file_is_stale_when_the_continuation_opens_another`
  - `tests/test_intake_land_native.py::test_the_same_files_against_a_copy_at_another_path_digest_equal_and_each_screen_names_its_path`

Old text:

```
        "device": plan.device_id,
        "master_db_id": plan.master_db_id,
```

New text:

```
        "file": plan.database.name,
        "device": plan.device_id,
        "master_db_id": plan.master_db_id,
```

### `u161.P4_device_out`

native.identity: drop the device, so an answer for one library is not stale for another with the same master id

- File: `src/cratekit/intake/native.py`
- Source: `u161.json`, row `P4_device_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 59 against a baseline of 59
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_engine_digest_moves_with_one_row_and_one_playlist_and_not_with_the_path`
  - `tests/test_intake_land_native.py::test_the_engine_identity_names_the_device_and_master_id_and_no_database_path`

Old text:

```
        "device": plan.device_id,
        "master_db_id": plan.master_db_id,
```

New text:

```
        "master_db_id": plan.master_db_id,
```

### `u161.P5_master_out`

native.identity: drop the master id, the other half of the library identity that replaced the path

- File: `src/cratekit/intake/native.py`
- Source: `u161.json`, row `P5_master_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 59 against a baseline of 59
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_engine_digest_moves_with_one_row_and_one_playlist_and_not_with_the_path`
  - `tests/test_intake_land_native.py::test_the_engine_identity_names_the_device_and_master_id_and_no_database_path`

Old text:

```
        "device": plan.device_id,
        "master_db_id": plan.master_db_id,
```

New text:

```
        "device": plan.device_id,
```

### `u161.S1_playlist_out`

native.identity: drop the batch playlist's name from the engine digest (sample of an existing guard)

- File: `src/cratekit/intake/native.py`
- Source: `u161.json`, row `S1_playlist_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_engine_digest_moves_with_one_row_and_one_playlist_and_not_with_the_path`

Old text:

```
        "playlist": plan.playlist,
        "batch_playlist": plan.batch_playlist_id,
```

New text:

```
        "batch_playlist": plan.batch_playlist_id,
```

### `u161.S2_columns_out`

native.identity: drop each row's columns from the engine digest (sample of an existing guard)

- File: `src/cratekit/intake/native.py`
- Source: `u161.json`, row `S2_columns_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_engine_digest_moves_with_one_row_and_one_playlist_and_not_with_the_path`

Old text:

```
                "content_id": row.content_id,
                "columns": row.columns(),
```

New text:

```
                "content_id": row.content_id,
```

### `u238.M10_question_drops_the_split`

_question_for: build the question without the listing's unchecked count

- File: `src/cratekit/label/sync_cli.py`
- Source: `u238.json`, row `M10_question_drops_the_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`, `tests/test_sync_all.py`
- Collected: 319 against a baseline of 319
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_newly_followed_label_is_offered_at_most_its_offer_per_sweep_newest`
  - `tests/test_label_sync.py::test_a_question_counts_only_the_labels_own_releases_past_its_window`
  - `tests/test_label_sync.py::test_an_unread_listing_still_says_so_beside_the_count_past_the_window`

Old text:

```
            beyond_unchecked=listing.beyond_unchecked,

```

New text:

```
(empty)
```

### `u238.M11_saved_question_drops_the_split`

Question.to_json: save no unchecked count, so a saved question reread says its own as a bound

- File: `src/cratekit/label/sync_cli.py`
- Source: `u238.json`, row `M11_saved_question_drops_the_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`, `tests/test_sync_all.py`
- Collected: 319 against a baseline of 319
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_newly_followed_label_is_offered_at_most_its_offer_per_sweep_newest`
  - `tests/test_label_sync.py::test_a_question_counts_only_the_labels_own_releases_past_its_window`
  - `tests/test_label_sync.py::test_an_unread_listing_still_says_so_beside_the_count_past_the_window`

Old text:

```
            "beyond_unchecked": self.beyond_unchecked,

```

New text:

```
(empty)
```

### `u238.M7_old_question_read_as_count`

Question.from_json: a question saved before the split reads none as unchecked, so 414 is said as the label's

- File: `src/cratekit/label/sync_cli.py`
- Source: `u238.json`, row `M7_old_question_read_as_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`, `tests/test_sync_all.py`
- Collected: 319 against a baseline of 319
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_question_saved_before_the_count_was_split_reads_as_a_bound`
  - `tests/test_label_sync.py::test_a_saved_split_that_cannot_be_read_reads_as_a_bound[-1]`
  - `tests/test_label_sync.py::test_a_saved_split_that_cannot_be_read_reads_as_a_bound[9]`
  - `tests/test_label_sync.py::test_a_saved_split_that_cannot_be_read_reads_as_a_bound[None]`
  - `tests/test_label_sync.py::test_a_saved_split_that_cannot_be_read_reads_as_a_bound[True]`

Old text:

```
            beyond_unchecked=beyond if unchecked is None else min(beyond, unchecked),
```

New text:

```
            beyond_unchecked=0 if unchecked is None else min(beyond, unchecked),
```

### `u238.M8_bound_said_as_the_labels`

sync_cli._past_window: say the unchecked alone as the label's releases rather than as a bound

- File: `src/cratekit/label/sync_cli.py`
- Source: `u238.json`, row `M8_bound_said_as_the_labels`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`, `tests/test_sync_all.py`
- Collected: 319 against a baseline of 319
- Kills: 8 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_newly_followed_label_is_offered_at_most_its_offer_per_sweep_newest`
  - `tests/test_label_sync.py::test_a_question_saved_before_the_count_was_split_reads_as_a_bound`
  - `tests/test_label_sync.py::test_a_saved_split_larger_than_its_figure_is_held_to_the_figure`
  - `tests/test_label_sync.py::test_a_saved_split_that_cannot_be_read_reads_as_a_bound[-1]`
  - `tests/test_label_sync.py::test_a_saved_split_that_cannot_be_read_reads_as_a_bound[9]`
  - `tests/test_label_sync.py::test_a_saved_split_that_cannot_be_read_reads_as_a_bound[None]`
  - `tests/test_label_sync.py::test_a_saved_split_that_cannot_be_read_reads_as_a_bound[True]`
  - `tests/test_label_sync.py::test_the_phrase_past_the_window_is_a_count_or_a_bound_and_never_zero`

Old text:

```
        said = f"up to {unchecked} more past this run's window, not yet checked"
```

New text:

```
        said = f"{unchecked} more of the label's release(s) past this run's window"
```

### `u238.M9_nothing_line_loses_the_split`

sync_cli._nothing_check: pass no unchecked count, so the nothing new line says every release as the label's

- File: `src/cratekit/label/sync_cli.py`
- Source: `u238.json`, row `M9_nothing_line_loses_the_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`, `tests/test_sync_all.py`
- Collected: 319 against a baseline of 319
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync.py::test_nothing_new_after_an_answer_says_the_count_past_the_window`
  - `tests/test_label_sync.py::test_nothing_new_says_the_count_past_the_window_the_same_way`

Old text:

```
        past = _past_window(listed.listing.beyond, listed.listing.beyond_unchecked)
```

New text:

```
        past = _past_window(listed.listing.beyond, 0)
```

### `r318.P1_withdrawn_branch_removed`

row_placement: never answer withdrawn, so a track imported then removed in rekordbox is reported as never imported and the person is sent to import it again

- File: `src/cratekit/write/routing_pass.py`
- Source: `r318.json`, row `P1_withdrawn_branch_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`, `tests/test_intake_imported.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 437 against a baseline of 437
- Kills: 5 (killed)
- Killed:
  - `tests/test_deferred_routing.py::test_a_location_reaching_only_soft_deleted_rows_is_withdrawn`
  - `tests/test_deferred_routing.py::test_a_track_deleted_after_import_is_surfaced`
  - `tests/test_routing_workers.py::test_a_row_rekordbox_removed_is_reported_withdrawn_not_unimported`
  - `tests/test_routing_workers.py::test_the_placement_of_a_row_answer_is_one_rule[withdrawn-twice]`
  - `tests/test_routing_workers.py::test_the_placement_of_a_row_answer_is_one_rule[withdrawn]`

Old text:

```
    if removed.outcome in (trees.MatchOutcome.MATCHED, trees.MatchOutcome.AMBIGUOUS):
        # A row exists and every one of them is a tombstone: imported once, then
```

New text:

```
    if False:
        # A row exists and every one of them is a tombstone: imported once, then
```

### `r318.P2_withdrawn_on_single_tombstone_only`

row_placement: withdrawn only when exactly one tombstone claims the location, two tombstones read as not imported

- File: `src/cratekit/write/routing_pass.py`
- Source: `r318.json`, row `P2_withdrawn_on_single_tombstone_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`, `tests/test_intake_imported.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 437 against a baseline of 437
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_placement_of_a_row_answer_is_one_rule[withdrawn-twice]`

Old text:

```
    if removed.outcome in (trees.MatchOutcome.MATCHED, trees.MatchOutcome.AMBIGUOUS):
        # A row exists and every one of them is a tombstone: imported once, then
```

New text:

```
    if removed.outcome in (trees.MatchOutcome.MATCHED,):
        # A row exists and every one of them is a tombstone: imported once, then
```

### `r318.P3_unresolved_branch_removed`

row_placement: drop the unresolved answer, so a location no prefix maps falls through to not imported, a configuration failure reported as a missing import

- File: `src/cratekit/write/routing_pass.py`
- Source: `r318.json`, row `P3_unresolved_branch_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`, `tests/test_intake_imported.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 437 against a baseline of 437
- Kills: 3 (killed)
- Killed:
  - `tests/test_deferred_routing.py::test_a_location_that_resolves_to_no_path_is_not_reported_as_a_missing_import`
  - `tests/test_deferred_routing.py::test_a_run_whose_locations_all_resolve_to_nothing_is_not_told_to_import`
  - `tests/test_routing_workers.py::test_the_placement_of_a_row_answer_is_one_rule[unresolved]`

Old text:

```
    if alive.outcome is trees.MatchOutcome.UNRESOLVED:
        return Placement.UNRESOLVED

```

New text:

```
(empty)
```

### `r318.P4_ambiguous_reads_not_imported`

row_placement: two live rows claiming a location answer not imported instead of ambiguous

- File: `src/cratekit/write/routing_pass.py`
- Source: `r318.json`, row `P4_ambiguous_reads_not_imported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`, `tests/test_intake_imported.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 437 against a baseline of 437
- Kills: 3 (killed)
- Killed:
  - `tests/test_deferred_routing.py::test_two_active_rows_on_one_location_are_ambiguous_and_never_written`
  - `tests/test_routing_workers.py::test_a_file_two_rows_claim_is_reported_ambiguous_with_both_rows`
  - `tests/test_routing_workers.py::test_the_placement_of_a_row_answer_is_one_rule[ambiguous]`

Old text:

```
    if alive.outcome is trees.MatchOutcome.AMBIGUOUS:
        return Placement.AMBIGUOUS
```

New text:

```
    if alive.outcome is trees.MatchOutcome.AMBIGUOUS:
        return Placement.NOT_IMPORTED
```

### `u51-item-derivation.A2_default_favorites_playlist`

Default the sweep to the FOLDER name the live library uses

- File: `src/cratekit/modules/outbound/source.py`
- Source: `u51-item-derivation.json`, row `A2_default_favorites_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 145 against a baseline of 145
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

### `u51-item-derivation.D1_unknown_playlist`

Drop the refusal for a playlist name the document does not carry

- File: `src/cratekit/modules/outbound/source.py`
- Source: `u51-item-derivation.json`, row `D1_unknown_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 145 against a baseline of 145
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_name_that_is_a_folder_refuses_rather_than_resolving`
  - `tests/test_outbound_workers.py::test_an_export_naming_a_playlist_the_document_lacks_queues_nothing`

Old text:

```
    if not matched:
        raise refuse(
            "export-playlist-unknown",
            f"no playlist in {library.path.name} is named {wanted!r}. A folder "
            f"of that name is not a match either, because a folder holds "
            f"playlists rather than tracks",
            steps=(
                "name the playlist by its display name, or by its full path "
                "joined with /",
            ),
            scope=Scope.RUN,
            origin=("outbound", "source"),
            detail={"playlist": wanted},
        )

```

New text:

```
(empty)
```

### `u51-item-derivation.D2_ambiguous_playlist`

Take the first match instead of refusing when several carry the name

- File: `src/cratekit/modules/outbound/source.py`
- Source: `u51-item-derivation.json`, row `D2_ambiguous_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 145 against a baseline of 145
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

### `u51-item-derivation.D3_empty_playlist`

THE ZERO ITEM RULE: let a playlist with no writable track queue

- File: `src/cratekit/modules/outbound/source.py`
- Source: `u51-item-derivation.json`, row `D3_empty_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 145 against a baseline of 145
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

### `u51-item-derivation.D4_dangling_reported`

Stop reporting a TrackID the playlist names and the collection lacks

- File: `src/cratekit/modules/outbound/source.py`
- Source: `u51-item-derivation.json`, row `D4_dangling_reported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 145 against a baseline of 145
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

### `u51-item-derivation.D5_repeated_deduped`

Queue a repeated identifier twice instead of once

- File: `src/cratekit/modules/outbound/source.py`
- Source: `u51-item-derivation.json`, row `D5_repeated_deduped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 145 against a baseline of 145
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

### `u51-item-derivation.D6_export_required`

Let a verb queue with no export document named

- File: `src/cratekit/modules/outbound/source.py`
- Source: `u51-item-derivation.json`, row `D6_export_required`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 145 against a baseline of 145
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

### `u79-c.C2_owned_row_searched`

A row the library holds is counted missing and searched for

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u79-c.json`, row `C2_owned_row_searched`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 144 against a baseline of 144
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_list_the_library_holds_entirely_is_a_no_op_that_spends_no_login`
  - `tests/test_intake_missing_search.py::test_an_owned_row_is_never_searched_for`

Old text:

```
    for settled in resolved.matches:
        if settled.state is match.MatchState.MATCHED:
            counts["owned"] += 1
        elif settled.state is match.MatchState.NEEDS_REVIEW:
            counts["offered"] += 1
        elif settled.state is match.MatchState.SUPPRESSED:
            counts["suppressed"] += 1
        else:
            counts["missing"] += 1
            # THE SAME LINE TWICE
```

New text:

```
    for settled in resolved.matches:
        if False:
            counts["owned"] += 1
        elif settled.state is match.MatchState.NEEDS_REVIEW:
            counts["offered"] += 1
        elif settled.state is match.MatchState.SUPPRESSED:
            counts["suppressed"] += 1
        else:
            counts["missing"] += 1
            # THE SAME LINE TWICE
```

### `u79-c.C3_accepted_held_listed_again`

An accepted candidate the library now holds is listed for download again

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u79-c.json`, row `C3_accepted_held_listed_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 144 against a baseline of 144
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_an_accepted_candidate_the_library_now_holds_is_not_listed_again`

Old text:

```
            if now.state in (match.MatchState.MATCHED, match.MatchState.SUPPRESSED):
                proposals[n]
```

New text:

```
            if False:
                proposals[n]
```

### `u79-c.C4_nothing_found_is_a_no_op`

Missing rows with no route to any of them end as nothing to do

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u79-c.json`, row `C4_nothing_found_is_a_no_op`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 144 against a baseline of 144
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_an_acceptance_naming_none_of_several_candidates_lists_nothing`
  - `tests/test_intake_missing_search.py::test_no_candidate_for_any_row_refuses_rather_than_reading_as_nothing_to_do`

Old text:

```
    if unfound and not listed and not asked:
```

New text:

```
    if False:
```

### `u79-c.C5_foreign_ref_names_a_row`

Another service's identifier is read as the provider's, and the row is in no file

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u79-c.json`, row `C5_foreign_ref_names_a_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 144 against a baseline of 144
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_missing_row_of_another_services_list_is_searched_for_and_not_dropped`
  - `tests/test_intake_missing_search.py::test_rows_asked_by_isrc_and_rows_searched_for_share_one_catalogue`

Old text:

```
    return str(wanted.ref or "").strip() if wanted.origin == match.TIDAL else ""
```

New text:

```
    return str(wanted.ref or "").strip()
```

### `u79-c.C6_isrc_named_keeps_origin`

A foreign row named by ISRC keeps its origin, so the emitter takes the ref off again

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u79-c.json`, row `C6_isrc_named_keeps_origin`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 144 against a baseline of 144
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_rows_asked_by_isrc_and_rows_searched_for_share_one_catalogue`

Old text:

```
                named.append(replace(one, ref=answer, origin=match.TIDAL))
```

New text:

```
                named.append(replace(one, ref=answer))
```

### `u79-c.C7_fixed_name`

The found list takes one fixed name, so the run after an answer is refused

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u79-c.json`, row `C7_fixed_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 144 against a baseline of 144
- Kills: 10 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_one_exact_candidate_is_listed_without_review`
  - `tests/test_intake_missing_search.py::test_the_found_list_is_named_for_its_input[.txt-txt-found]`
  - `tests/test_intake_missing_search.py::test_the_found_list_is_named_for_its_input[\xa7\xa7\xa7.txt-tracklist-found]`
  - `tests/test_intake_missing_search.py::test_the_found_list_is_named_for_its_input[friday set (2026).txt-friday-set-2026-found]`
  - `tests/test_intake_missing_search.py::test_the_found_list_is_named_for_its_input[intake-j1.unlisted.json-intake-j1-found]`
  - `tests/test_intake_missing_search.py::test_the_found_list_is_named_for_its_input[notes-notes-found]`
  - `tests/test_intake_missing_search.py::test_the_found_list_is_named_for_its_input[warmup.list.json-warmup-found]`
  - `tests/test_intake_missing_search.py::test_the_run_after_an_answer_lists_more_than_the_first_and_is_not_refused`
  - `tests/test_intake_missing_search.py::test_the_unlisted_list_is_read_and_its_found_list_sits_beside_the_jobs`
  - `tests/test_intake_missing_search.py::test_two_tracklists_of_one_file_name_in_two_folders_do_not_collide`

Old text:

```
    return f"{stem or 'tracklist'}{FOUND_SUFFIX}-{digest}"
```

New text:

```
    return f"{stem or 'tracklist'}{FOUND_SUFFIX}"
```

### `u79-c.C8_asked_is_a_no_op`

A run that only put a question to a person ends as nothing to do

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u79-c.json`, row `C8_asked_is_a_no_op`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 144 against a baseline of 144
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_two_exact_candidates_are_offered_and_neither_is_picked`

Old text:

```
        outcome=Outcome.OK if listed or asked else Outcome.NO_OP,
```

New text:

```
        outcome=Outcome.OK if listed else Outcome.NO_OP,
```

### `u100-b.C10_added_message`

reword the added detail a person reads

- File: `src/cratekit/label/cli.py`
- Source: `u100-b.json`, row `C10_added_message`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`
- Collected: 47 against a baseline of 47
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_a_person_reading_the_default_output_sees_what_was_added`

Old text:

```
        status, detail = "ok", f"{result.name}: added as {result.label_id}"
```

New text:

```
        status, detail = "ok", f"{result.name}: now followed as {result.label_id}"
```

### `u100-b.C1_name_accepted`

adopt no longer refuses a name argument and silently ignores it

- File: `src/cratekit/label/cli.py`
- Source: `u100-b.json`, row `C1_name_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`
- Collected: 47 against a baseline of 47
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_adopt_with_a_name_or_a_field_refuses_and_writes_nothing[name]`

Old text:

```
    if ctx.args.name or ctx.args.new_name is not None:
```

New text:

```
    if ctx.args.new_name is not None:
```

### `u100-b.C2_to_accepted`

adopt no longer refuses --to and silently ignores it

- File: `src/cratekit/label/cli.py`
- Source: `u100-b.json`, row `C2_to_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`
- Collected: 47 against a baseline of 47
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_adopt_with_a_name_or_a_field_refuses_and_writes_nothing[to]`

Old text:

```
    if ctx.args.name or ctx.args.new_name is not None:
```

New text:

```
    if ctx.args.name:
```

### `u100-b.C3_outcome_always_ok`

adopt reports ok when it added nothing

- File: `src/cratekit/label/cli.py`
- Source: `u100-b.json`, row `C3_outcome_always_ok`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`
- Collected: 47 against a baseline of 47
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_an_accepted_label_is_added_once_and_a_second_run_adds_none`
  - `tests/test_label_registry_adopt.py::test_nothing_accepted_writes_nothing_and_says_what_is_waiting`

Old text:

```
        outcome=Outcome.OK if added else Outcome.NO_OP,
```

New text:

```
        outcome=Outcome.OK,
```

### `u100-b.C4_empty_says_nothing`

adopt over a queue with nothing accepted emits no check, so a person reads a blank answer

- File: `src/cratekit/label/cli.py`
- Source: `u100-b.json`, row `C4_empty_says_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`
- Collected: 47 against a baseline of 47
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_nothing_accepted_writes_nothing_and_says_what_is_waiting`

Old text:

```
    if not checks:
        checks.append(
```

New text:

```
    if False:
        checks.append(
```

### `u100-b.C5_nameless_unreported`

adopt drops the failing check for an accepted item that names no label

- File: `src/cratekit/label/cli.py`
- Source: `u100-b.json`, row `C5_nameless_unreported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`
- Collected: 47 against a baseline of 47
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_an_accepted_item_naming_no_label_is_reported_not_skipped`

Old text:

```
        for item_id in found.nameless
```

New text:

```
        for item_id in ()
```

### `u100-b.C6_held_name_hidden`

the already held check no longer names the spelling the label is held under

- File: `src/cratekit/label/cli.py`
- Source: `u100-b.json`, row `C6_held_name_hidden`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`
- Collected: 47 against a baseline of 47
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_a_carried_over_accented_label_is_not_filed_twice`

Old text:

```
        if result.held_name != result.name:
```

New text:

```
        if False:
```

### `u100-b.C7_refused_reads_as_note`

a name that yields no identifier is shown as a note rather than a failure

- File: `src/cratekit/label/cli.py`
- Source: `u100-b.json`, row `C7_refused_reads_as_note`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`
- Collected: 47 against a baseline of 47
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_a_name_with_no_identifier_fails_alone_and_the_rest_land`

Old text:

```
        status = "fail"
        detail = (
```

New text:

```
        status = "info"
        detail = (
```

### `u100-b.C9_dispatch`

the adopt action is never dispatched and falls through to the named actions

- File: `src/cratekit/label/cli.py`
- Source: `u100-b.json`, row `C9_dispatch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`
- Collected: 47 against a baseline of 47
- Kills: 12 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_a_carried_over_accented_label_is_not_filed_twice`
  - `tests/test_label_registry_adopt.py::test_a_label_held_under_a_folded_name_is_reported_not_duplicated[case]`
  - `tests/test_label_registry_adopt.py::test_a_label_held_under_a_folded_name_is_reported_not_duplicated[padding]`
  - `tests/test_label_registry_adopt.py::test_a_label_release_on_the_same_queue_is_not_adopted`
  - `tests/test_label_registry_adopt.py::test_a_name_with_no_identifier_fails_alone_and_the_rest_land`
  - `tests/test_label_registry_adopt.py::test_a_person_reading_the_default_output_sees_what_was_added`
  - `tests/test_label_registry_adopt.py::test_a_rejected_or_open_label_is_not_added`
  - `tests/test_label_registry_adopt.py::test_an_accepted_item_naming_no_label_is_reported_not_skipped`
  - `tests/test_label_registry_adopt.py::test_an_accepted_label_is_added_once_and_a_second_run_adds_none`
  - `tests/test_label_registry_adopt.py::test_an_adopt_that_adds_nothing_does_not_rewrite_the_registry`
  - `tests/test_label_registry_adopt.py::test_nothing_accepted_writes_nothing_and_says_what_is_waiting`
  - `tests/test_label_registry_adopt.py::test_two_spellings_accepted_in_one_run_add_the_label_once`

Old text:

```
    if action == "adopt":
```

New text:

```
    if action == "adopted":
```

### `u149.T10_any_year_folder`

candidates: read every root folder, not only one titled as a year

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T10_any_year_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_only_downloaded_own_playlists_in_a_year_folder_are_read`

Old text:

```
        if not YEAR.fullmatch(year):
            continue
```

New text:

```
        if False:
            continue
```

### `u149.T11_excluded_read`

candidates: drop the label, set and mirror exclusion

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T11_excluded_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_set_playlist_in_a_year_folder_gets_no_twin`

Old text:

```
            if name is None or playlist_id in kept or playlist_id in seen:
```

New text:

```
            if name is None or playlist_id in seen:
```

### `u149.T13_paired_planned_again`

plan_backfill: plan a twin for an already paired playlist, so a second run plans again

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T13_paired_planned_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_an_existing_folder_is_reused_and_two_of_one_year_place_nothing`

Old text:

```
    wanted = [one for one in listed if one[1] not in held]
```

New text:

```
    wanted = list(listed)
```

### `u149.T15_unplanned_membership`

addition_violations: admit a membership no twin planned

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T15_unplanned_membership`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_the_confinement_refuses_what_no_twin_explains[changes4]`

Old text:

```
        if row[m_marker] or wanted is None or content_id not in wanted[2]:
```

New text:

```
        if row[m_marker] or wanted is None:
```

### `u149.T16_unplanned_playlist_row`

addition_violations: admit a playlist row no twin made

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T16_unplanned_playlist_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_the_confinement_refuses_an_unplanned_playlist_read_from_sql`
  - `tests/test_sync_twins.py::test_the_confinement_refuses_what_no_twin_explains[changes0]`

Old text:

```
    for key in sorted(set(after.playlists) - set(before.playlists) - set(made)):
```

New text:

```
    for key in sorted(set()):
```

### `u149.T20_short_snapshot`

pair_backfilled: record the account snapshot when the listing was short

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T20_short_snapshot`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_short_listing_pairs_the_twin_with_no_snapshot`

Old text:

```
            account=list(one.account) if one.whole else None,
```

New text:

```
            account=list(one.account),
```

### `u149.T7_ambiguous_takes_first`

matched: take the first of several library rows, so an ambiguous track is guessed

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T7_ambiguous_takes_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_an_account_track_two_library_rows_carry_is_named_and_neither_is_guessed`
  - `tests/test_sync_twins.py::test_an_untitled_track_two_library_rows_carry_is_ambiguous_not_unreadable`

Old text:

```
        if len(found) == 1:
```

New text:

```
        if found:
```

### `u149.T8_mirror_link_skipped`

Library.find: skip the mirror's link to the very track, so the database ISRC decides

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T8_mirror_link_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_the_mirrors_link_to_a_track_wins_and_a_link_to_a_removed_row_falls_through`

Old text:

```
            self.by_remote.get(remote_id, ()),
```

New text:

```
            (),
```

### `u149.T9_removed_row_linked`

_grouped: drop the live filter, so a mirror link to a removed row is an answer

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T9_removed_row_linked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_the_mirrors_link_to_a_track_wins_and_a_link_to_a_removed_row_falls_through`

Old text:

```
        if key and content_id in alive and content_id not in found.setdefault(key, []):
```

New text:

```
        if key and content_id not in found.setdefault(key, []):
```

### `u164.H1_watch_recorded`

_filed_watch: watch today's year folder alone, never the recorded folder

- File: `src/cratekit/intake/land_cli.py`
- Source: `u164.json`, row `H1_watch_recorded`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 36 against a baseline of 36
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_a_batch_filed_in_another_year_is_refused`

Old text:

```
        watched.extend((Path(again).parent, Path(again)))
```

New text:

```
        pass
```

### `u164.H2_scratch_folder`

_rehearse_in: map the scratch plan back from the live folder instead of its own

- File: `src/cratekit/intake/land_cli.py`
- Source: `u164.json`, row `H2_scratch_folder`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 36 against a baseline of 36
- Kills: 20 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_batch_whose_name_is_not_ascii_rehearses_equal_and_the_gate_says_so`
  - `tests/test_intake_land_rehearse.py::test_a_copy_that_fails_its_integrity_check_is_refused_naming_the_area`
  - `tests/test_intake_land_rehearse.py::test_a_landed_row_read_back_with_a_grid_is_refused_and_never_reported_gridless`
  - `tests/test_intake_land_rehearse.py::test_a_landed_row_whose_file_id_did_not_take_is_refused_in_the_rehearsal`
  - `tests/test_intake_land_rehearse.py::test_a_library_whose_base_drive_is_not_its_mount_rehearses_equal_and_the_gate_says_so`
  - `tests/test_intake_land_rehearse.py::test_a_live_plan_that_differs_names_the_rehearsal_and_prints_the_differing_lines`
  - `tests/test_intake_land_rehearse.py::test_a_name_the_live_batch_folder_holds_is_refused_at_the_area_as_it_will_be_live`
  - `tests/test_intake_land_rehearse.py::test_a_refusal_inside_the_rehearsal_keeps_its_reason_and_names_the_area`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_beside_another_runs_area_lands_and_leaves_that_area_alone`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_check_whose_copy_fails_otherwise_is_still_a_failed_check`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_check_whose_copy_finds_no_room_is_refused_under_the_room_slug`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_leaves_staging_the_music_folder_and_the_database_as_they_were`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_of_another_batch_is_not_the_one_compared`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_a_batch_filed_in_another_year_is_refused`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_the_live_library_is_refused_as_a_defect`
  - ... and 5 more, see the JSON sidecar

Old text:

```
        scratch_target = _folder(scratch_rows)
```

New text:

```
        scratch_target = landing.target_dir(area.cfg, planned.batch)
```

### `u188.M10_detail_mapped_dropped`

_rehearse_in: carry no mapped pairs in the refusal's detail

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M10_detail_mapped_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 36 against a baseline of 36
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_file_name_that_differs_still_refuses_and_names_the_line`

Old text:

```
                detail={"differs": differ, "mapped": [list(pair) for pair in pairs]},
```

New text:

```
                detail={"differs": differ},
```

### `u188.M11_fields_last_part`

_fields_of: name a field by its last part alone, so a vox row's path reads as rows

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M11_fields_last_part`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 36 against a baseline of 36
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_file_name_that_differs_still_refuses_and_names_the_line`
  - `tests/test_intake_land_rehearse.py::test_the_refusal_names_each_field_once_and_strips_every_index`

Old text:

```
        names.append(path.split(".", 1)[-1])
```

New text:

```
        names.append(path.rsplit(".", 1)[-1])
```

### `u188.M12_fields_keep_indices`

_fields_of: keep the indices, so one field is named once per row

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M12_fields_keep_indices`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 36 against a baseline of 36
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_file_name_that_differs_still_refuses_and_names_the_line`
  - `tests/test_intake_land_rehearse.py::test_the_refusal_names_each_field_once_and_strips_every_index`

Old text:

```
        path = re.sub(r"\[\d+\]", "", line[2:].split(" = ", 1)[0])
```

New text:

```
        path = line[2:].split(" = ", 1)[0]
```

### `u188.M13_fields_repeated`

_fields_of: keep every repeat, so a field ten rows differ in is named ten times

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M13_fields_repeated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 36 against a baseline of 36
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_file_name_that_differs_still_refuses_and_names_the_line`
  - `tests/test_intake_land_rehearse.py::test_the_refusal_names_each_field_once_and_strips_every_index`

Old text:

```
    return list(dict.fromkeys(names))


def _place_owned(
```

New text:

```
    return names


def _place_owned(
```

### `u188.M7_signs_swapped`

_rehearse_in: compare live first, so a minus line is the live plan's and the refusal's legend is false

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M7_signs_swapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 36 against a baseline of 36
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_scratch_plan_that_is_not_the_live_plan_applies_nothing`
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_file_name_that_differs_still_refuses_and_names_the_line`

Old text:

```
        differ = rehearsal.differing(back, lines)
```

New text:

```
        differ = rehearsal.differing(lines, back)
```

### `u188.M8_fields_left_out`

_rehearse_in: name no field in the refusal

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M8_fields_left_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 36 against a baseline of 36
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_file_name_that_differs_still_refuses_and_names_the_line`

Old text:

```
f"{len(differ)} line(s), in {', '.join(_fields_of(differ))}, so nothing "
```

New text:

```
f"{len(differ)} line(s), in the plan, so nothing "
```

### `u188.M9_pairs_left_out`

_rehearse_in: state no pair in the refusal, so the spellings compared are not named

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M9_pairs_left_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 36 against a baseline of 36
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_file_name_that_differs_still_refuses_and_names_the_line`

Old text:

```
                + ", ".join(f"{scratch} to {live}" for scratch, live in pairs)
```

New text:

```
                + "the area's paths"
```

### `r375-b.T3_a_noop_claims_a_commit`

_record_membership_commit: record a commit for a pass that added nothing, so a restore refuses over sessions that created nothing

- File: `src/cratekit/write/trees.py`
- Source: `r375-b.json`, row `T3_a_noop_claims_a_commit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tree_writer.py`, `tests/test_rebuild.py`, `tests/test_adopt_apply_cli.py`
- Collected: 196 against a baseline of 196
- Kills: 1 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_a_pass_that_added_nothing_claims_no_commit`

Old text:

```
    if added <= 0:
        return
    session.record_commit(
```

New text:

```
    session.record_commit(
```

### `r375-b.T4_noop_bound_off_by_one`

_record_membership_commit: move the no-op bound by one, so a pass that added exactly one membership claims no commit

- File: `src/cratekit/write/trees.py`
- Source: `r375-b.json`, row `T4_noop_bound_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tree_writer.py`, `tests/test_rebuild.py`, `tests/test_adopt_apply_cli.py`
- Collected: 196 against a baseline of 196
- Kills: 4 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_a_commit_that_lands_and_then_raises_is_still_recorded_as_committed`
  - `tests/test_tree_writer.py::test_a_failure_after_the_commit_still_reads_as_committed_work`
  - `tests/test_tree_writer.py::test_a_grid_rewritten_during_a_membership_write_refuses_the_session`
  - `tests/test_tree_writer.py::test_a_pass_that_added_nothing_claims_no_commit`

Old text:

```
    if added <= 0:
        return
    session.record_commit(
```

New text:

```
    if added <= 1:
        return
    session.record_commit(
```

### `r375-b.T5_witnessed_commit_not_recorded`

write_tree_membership: ignore the witness, so a commit that landed and then raised closes as though nothing landed

- File: `src/cratekit/write/trees.py`
- Source: `r375-b.json`, row `T5_witnessed_commit_not_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tree_writer.py`, `tests/test_rebuild.py`, `tests/test_adopt_apply_cli.py`
- Collected: 196 against a baseline of 196
- Kills: 1 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_a_commit_that_lands_and_then_raises_is_still_recorded_as_committed`

Old text:

```
            if witness.landed:
                _record_membership_commit(record, tree_id, added, cfg)
```

New text:

```
            if False:
                _record_membership_commit(record, tree_id, added, cfg)
```

### `r375-b.T7_commit_recorded_after_the_fingerprint`

write_tree_membership: record the commit AFTER the fingerprint write, so a failure there closes a committed write as empty

- File: `src/cratekit/write/trees.py`
- Source: `r375-b.json`, row `T7_commit_recorded_after_the_fingerprint`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tree_writer.py`, `tests/test_rebuild.py`, `tests/test_adopt_apply_cli.py`
- Collected: 196 against a baseline of 196
- Kills: 1 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_a_failure_after_the_commit_still_reads_as_committed_work`

Old text:

```
        _record_membership_commit(record, tree_id, added, cfg)

        # THE FINGERPRINT IS TAKEN AT THE CLOSE, AFTER THE COMMIT. It is what
        # lets the next run tell a database recovered out of band from one this
        # product changed itself, and taking it before the commit would record a
        # database this session then moved, so the next run would read its own
        # write as somebody else's restore. It sits outside the try above because
        # by here the commit has landed and there is nothing pending to roll
        # back; a failure now is a state write that failed, not a database write
        # that half happened.
        convergence.record_fingerprint(cfg, db)

```

New text:

```
        # THE FINGERPRINT IS TAKEN AT THE CLOSE, AFTER THE COMMIT. It is what
        # lets the next run tell a database recovered out of band from one this
        # product changed itself, and taking it before the commit would record a
        # database this session then moved, so the next run would read its own
        # write as somebody else's restore. It sits outside the try above because
        # by here the commit has landed and there is nothing pending to roll
        # back; a failure now is a state write that failed, not a database write
        # that half happened.
        convergence.record_fingerprint(cfg, db)
        _record_membership_commit(record, tree_id, added, cfg)

```

### `r375-b.T8_counts_filed_as_updates`

_record_membership_commit: file the added memberships as updated rather than created

- File: `src/cratekit/write/trees.py`
- Source: `r375-b.json`, row `T8_counts_filed_as_updates`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tree_writer.py`, `tests/test_rebuild.py`, `tests/test_adopt_apply_cli.py`
- Collected: 196 against a baseline of 196
- Kills: 3 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_a_commit_that_lands_and_then_raises_is_still_recorded_as_committed`
  - `tests/test_tree_writer.py::test_a_failure_after_the_commit_still_reads_as_committed_work`
  - `tests/test_tree_writer.py::test_a_membership_write_is_listed_as_restorable_with_its_per_tree_counts`

Old text:

```
session.TreeChange(tree=tree_id, created=added)
```

New text:

```
session.TreeChange(tree=tree_id, updated=added)
```

### `r375-c.T6_every_raise_read_as_a_commit_again`

write_tree_membership: record a commit on every raise. Batch B read this as ZERO; measured again after test_a_write_that_fails_after_counting_a_membership_still_claims_no_commit

- File: `src/cratekit/write/trees.py`
- Source: `r375-c.json`, row `T6_every_raise_read_as_a_commit_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tree_writer.py`, `tests/test_rebuild.py`, `tests/test_adopt_apply_cli.py`
- Collected: 196 against a baseline of 196
- Kills: 1 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_a_write_that_fails_after_counting_a_membership_still_claims_no_commit`

Old text:

```
            if witness.landed:
                _record_membership_commit(record, tree_id, added, cfg)
```

New text:

```
            if True:
                _record_membership_commit(record, tree_id, added, cfg)
```

### `u201-composites.C5_leave_nothing`

plan: a move leaves no tree playlist, the thing O4 narrows

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u201-composites.json`, row `C5_leave_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 195 against a baseline of 195
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

### `u201.O1_latch`

write: the tree's convergence latch is not asked

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u201.json`, row `O1_latch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 195 against a baseline of 195
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

### `u201.O2_stale`

_stale: a library moved since the plan is written

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u201.json`, row `O2_stale`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 195 against a baseline of 195
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

### `u201.O3_target_bucket`

target_tags: a genre word filing into another bucket is taken

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u201.json`, row `O3_target_bucket`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 195 against a baseline of 195
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

### `u201-composites.C4_settle_none`

settle_mirror_tracks: the library step settles nothing, the thing L2 narrows

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u201-composites.json`, row `C4_settle_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 195 against a baseline of 195
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_a_move_in_rekordbox_after_an_edit_was_taken_is_rekordboxs`
  - `tests/test_organize_mirror_edits.py::test_a_track_moved_on_the_account_is_retagged_refiled_and_the_next_run_plans_nothing`
  - `tests/test_organize_mirror_edits.py::test_the_ledger_keeps_a_snapshot_apart_from_none_and_only_on_its_own_playlist`

Old text:

```
    wanted = list(settled)
```

New text:

```
    wanted = []
```

### `u201.L1_agreed_own_playlist`

record_mirror_agreed: a snapshot lands on a playlist recorded under the title with another identifier

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u201.json`, row `L1_agreed_own_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 195 against a baseline of 195
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

### `u100-a.R1_slug_only_presence`

RegistryStore.adopt checks presence by slug alone, the R-381 hazard: a label held under sueno is filed again as sue-o

- File: `src/cratekit/label/registry.py`
- Source: `u100-a.json`, row `R1_slug_only_presence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                held = Registry(labels=current).resolve(name)
```

New text:

```
                held = Registry(labels=current).by_id(label_id)
```

### `u100-a.R2_no_presence_check`

RegistryStore.adopt never finds a label present, so every accepted name is written over the held entry

- File: `src/cratekit/label/registry.py`
- Source: `u100-a.json`, row `R2_no_presence_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 401 against a baseline of 401
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_a_carried_over_accented_label_is_not_filed_twice`
  - `tests/test_label_registry_adopt.py::test_a_label_held_under_a_folded_name_is_reported_not_duplicated[case]`
  - `tests/test_label_registry_adopt.py::test_a_label_held_under_a_folded_name_is_reported_not_duplicated[padding]`
  - `tests/test_label_registry_adopt.py::test_an_accepted_label_is_added_once_and_a_second_run_adds_none`
  - `tests/test_label_registry_adopt.py::test_an_adopt_that_adds_nothing_does_not_rewrite_the_registry`
  - `tests/test_label_registry_adopt.py::test_two_spellings_accepted_in_one_run_add_the_label_once`

Old text:

```
                if held is not None:
                    results.append(
```

New text:

```
                if False:
                    results.append(
```

### `u100-a.R3_presence_before_the_batch`

RegistryStore.adopt resolves against the file as loaded, not the entries this run already added, so two spellings in one run both add

- File: `src/cratekit/label/registry.py`
- Source: `u100-a.json`, row `R3_presence_before_the_batch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 401 against a baseline of 401
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_two_spellings_accepted_in_one_run_add_the_label_once`

Old text:

```
                held = Registry(labels=current).resolve(name)
```

New text:

```
                held = self.load().resolve(name)
```

### `u100-a.R4_slug_refusal_aborts`

a name that yields no identifier is no longer caught per name, so it aborts the whole adopt

- File: `src/cratekit/label/registry.py`
- Source: `u100-a.json`, row `R4_slug_refusal_aborts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 401 against a baseline of 401
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_a_name_with_no_identifier_fails_alone_and_the_rest_land`

Old text:

```
                except CratekitError as exc:
                    results.append(
```

New text:

```
                except KeyError as exc:
                    results.append(
```

### `u239.L01_remember_land_only`

_remember: record a gate stop at any step as the landing, so a restamp gate is taken for it

- File: `src/cratekit/cli/label_sync.py`
- Source: `u239.json`, row `L01_remember_land_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 275 against a baseline of 275
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_stop_at_a_gate_before_the_landing_records_no_landing_and_the_next_go_runs_the_tail`

Old text:

```
    if not (stop.step == tail.LAND and stop.cause.reason == tail.GATE_STOP and landed):
```

New text:

```
    if not (stop.cause.reason == tail.GATE_STOP and landed):
```

### `u239.L02_remember_owner`

_remember: record on whichever run ran the tail, the round one blocking shape

- File: `src/cratekit/cli/label_sync.py`
- Source: `u239.json`, row `L02_remember_owner`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 275 against a baseline of 275
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_fresh_go_that_landed_another_runs_download_records_it_on_that_run`
  - `tests/test_label_sync_go.py::test_a_landing_another_runs_record_cannot_keep_is_a_warning_and_the_go_still_ends_at_it`

Old text:

```
    if owner == ctx.run.run_id:
```

New text:

```
    if True:
```

### `u239.L03_remember_called`

label_sync: never record the landing, so a later go runs the tail again

- File: `src/cratekit/cli/label_sync.py`
- Source: `u239.json`, row `L03_remember_called`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 275 against a baseline of 275
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_fresh_go_that_landed_another_runs_download_records_it_on_that_run`
  - `tests/test_label_sync_go.py::test_a_go_that_ran_its_tail_once_names_its_landing_when_run_again`
  - `tests/test_label_sync_go.py::test_a_go_whose_tail_reached_its_landing_names_that_landing_and_runs_nothing_again`
  - `tests/test_label_sync_go.py::test_a_landing_another_runs_record_cannot_keep_is_a_warning_and_the_go_still_ends_at_it`
  - `tests/test_label_sync_go.py::test_a_stop_at_a_gate_before_the_landing_records_no_landing_and_the_next_go_runs_the_tail`
  - `tests/test_label_sync_go.py::test_a_walk_under_a_landed_run_that_records_an_answer_is_not_a_no_op`

Old text:

```
        warnings.extend(_remember(ctx, stop, land))
```

New text:

```
        pass
```

### `u239.L05_commands_added`

_with_commands: never name the tail commands on the go's refusal

- File: `src/cratekit/cli/label_sync.py`
- Source: `u239.json`, row `L05_commands_added`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 275 against a baseline of 275
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_landed_while_the_fresh_go_downloaded_refuses_its_tail`
  - `tests/test_label_sync_go.py::test_a_later_gos_download_in_the_same_folder_refuses_the_tail_and_names_its_commands`
  - `tests/test_label_sync_go.py::test_a_plain_download_into_the_folder_refuses_the_runs_own_tail`

Old text:

```
    land = _land_in(cause.detail) if _GO_ORIGIN in cause.origin else None
```

New text:

```
    land = None
```

### `u239.L06_unrecorded_warning`

_remember: drop the warning when another run's record cannot keep the landing

- File: `src/cratekit/cli/label_sync.py`
- Source: `u239.json`, row `L06_unrecorded_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 275 against a baseline of 275
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_landing_another_runs_record_cannot_keep_is_a_warning_and_the_go_still_ends_at_it`

Old text:

```
    except Exception as exc:  # noqa: BLE001 - see below
```

New text:

```
    except ZeroDivisionError as exc:  # noqa: BLE001 - see below
```

### `u322.M21_suggest_uses_folder_binder`

suggest_cli.read_plan: tag suggest asks through tag folder's binder

- File: `src/cratekit/tagging/suggest_cli.py`
- Source: `u322.json`, row `M21_suggest_uses_folder_binder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_published_genre.py`, `tests/test_beatport_refusal.py`
- Collected: 392 against a baseline of 392
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_tag_suggest_asks_deezer_past_a_refusing_beatport_by_each_files_isrc`

Old text:

```
            searchers.for_taxonomy(declared), published.for_suggestions(declared)
```

New text:

```
            searchers.for_taxonomy(declared), published.for_taxonomy(declared)
```

### `u322.M20_backlog_uses_folder_binder`

backlog_cli.read_plan: the backlog asks through tag folder's binder, so Deezer is held behind a refusing Beatport

- File: `src/cratekit/tagging/backlog_cli.py`
- Source: `u322.json`, row `M20_backlog_uses_folder_binder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_published_genre.py`, `tests/test_beatport_refusal.py`
- Collected: 392 against a baseline of 392
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_backlog.py::test_a_refusing_beatport_beside_an_answering_discogs_asks_every_row_and_counts_them`

Old text:

```
            searchers.for_taxonomy(declared), published.for_suggestions(declared)
```

New text:

```
            searchers.for_taxonomy(declared), published.for_taxonomy(declared)
```

### `u322.M22_backlog_partly_clause_gone`

backlog_cli.advisories: the partly read clause is dropped, so the campaign's gate says nothing of Beatport

- File: `src/cratekit/tagging/backlog_cli.py`
- Source: `u322.json`, row `M22_backlog_partly_clause_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_published_genre.py`, `tests/test_beatport_refusal.py`
- Collected: 392 against a baseline of 392
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_backlog.py::test_a_refusing_beatport_beside_an_answering_discogs_asks_every_row_and_counts_them`

Old text:

```
    if unread.partly:
        parts.append(
            f"{unread.partly_by} could not be read for {len(unread.partly)} row(s) "
            f"another catalogue answered, {_named(list(unread.partly))}, so those were "
```

New text:

```
    if False:
        parts.append(
            f"{unread.partly_by} could not be read for {len(unread.partly)} row(s) "
            f"another catalogue answered, {_named(list(unread.partly))}, so those were "
```

### `u322.M24_backlog_line_gone`

backlog_cli.checks: no catalogue line

- File: `src/cratekit/tagging/backlog_cli.py`
- Source: `u322.json`, row `M24_backlog_line_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_published_genre.py`, `tests/test_beatport_refusal.py`
- Collected: 392 against a baseline of 392
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_backlog.py::test_a_refusing_beatport_beside_an_answering_discogs_asks_every_row_and_counts_them`
  - `tests/test_tag_backlog.py::test_the_catalogue_line_names_the_rows_the_walk_stopped_before`

Old text:

```
    if plan.catalogue:
        found.append(_check("backlog.catalogue"
```

New text:

```
    if False:
        found.append(_check("backlog.catalogue"
```

### `r1032.A11_empty_album_narrows`

_on_album: drop the empty tag guard, so a file with no album narrows a tie to the releases the provider left unnamed

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1032.json`, row `A11_empty_album_narrows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_organize_mirror_tie.py`
- Collected: 116 against a baseline of 116
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

### `r1032.A1_adapter_ignores_any_agreeing`

match_track: drop any_agreeing on its way to _among, so the adapter refuses the tie for the mirror too

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1032.json`, row `A1_adapter_ignores_any_agreeing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_organize_mirror_tie.py`
- Collected: 116 against a baseline of 116
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

### `r1032.A3_unreadable_tie_broken`

_among: break a tie beside a candidate that could not be read

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1032.json`, row `A3_unreadable_tie_broken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_organize_mirror_tie.py`
- Collected: 116 against a baseline of 116
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

### `r1032.A7_lowest_by_characters`

_lowest: order the identifiers as text, so 100 sorts before 99

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1032.json`, row `A7_lowest_by_characters`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_organize_mirror_tie.py`
- Collected: 116 against a baseline of 116
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

### `r1032.A8_album_narrow_drops_all`

_on_album: when the album names none, answer the named list alone, empty

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1032.json`, row `A8_album_narrow_drops_all`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_organize_mirror_tie.py`
- Collected: 116 against a baseline of 116
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

### `r1032.A9_album_narrow_unfolded`

_on_album: compare the album unfolded, so case and spacing defeat the narrowing

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1032.json`, row `A9_album_narrow_unfolded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_organize_mirror_tie.py`
- Collected: 116 against a baseline of 116
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

### `u216.M21_reserve_adopt_empty`

reserve_folder: an adoption records an empty set whatever the plan listed

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u216.json`, row `M21_reserve_adopt_empty`
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
                before = (
                    None if held is None else frozenset(str(one) for one in held if str(one))
                )
```

New text:

```
                before = frozenset()
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

### `r259.L1_job_cache_read`

The worker never reuses the job's library view, one walk per label

- File: `src/cratekit/label/cli.py`
- Source: `r259.json`, row `L1_job_cache_read`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_sync_all.py`
- Collected: 551 against a baseline of 551
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_sweep_of_two_labels_walks_the_library_once`

Old text:

```
        held = _JOB_LIBRARY.get(key)
```

New text:

```
        held = None
```

### `r504-a.A11_boundary_refuses`

The verb boundary no longer catches the shortfall, so it is refused as an unreadable listing

- File: `src/cratekit/label/cli.py`
- Source: `r504-a.json`, row `A11_boundary_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_sync_all.py`
- Collected: 551 against a baseline of 551
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`
  - `tests/test_label_tidal_catalogue.py::test_the_verb_boundary_keeps_the_rows_and_hands_back_the_shortfall`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`

Old text:

```
    except catalogue.HeartsShortfall as short:
        return list(short.rows), short

```

New text:

```
(empty)
```

### `r504-a.A12_boundary_drops_short`

The verb boundary keeps the rows and drops the shortfall, passing the short listing off as the account

- File: `src/cratekit/label/cli.py`
- Source: `r504-a.json`, row `A12_boundary_drops_short`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_sync_all.py`
- Collected: 551 against a baseline of 551
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`
  - `tests/test_label_tidal_catalogue.py::test_the_verb_boundary_keeps_the_rows_and_hands_back_the_shortfall`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`

Old text:

```
        return list(short.rows), short
```

New text:

```
        return list(short.rows), None
```

### `u242.M11_strip_skips_the_held_check`

strip: rename without confirming the record holds each planned playlist

- File: `src/cratekit/sync/strip_cli.py`
- Source: `u242.json`, row `M11_strip_skips_the_held_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_no_rename_is_made_for_a_playlist_the_record_does_not_hold`

Old text:

```
    unheld = [identity for identity in planned if identity not in held]
```

New text:

```
    unheld = []
```

### `u242.M12_composite`

strip: neither record first nor confirm the hold, so a stripped playlist is in no record

- File: `src/cratekit/sync/strip_cli.py`
- Source: `u242.json`, row `M12_composite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`
- Collected: 46 against a baseline of 46
- Kills: 11 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_a_ceiling_stop_names_what_landed_and_a_second_run_resumes`
  - `tests/test_u242_taken.py::test_a_collision_is_refused_and_named_and_the_rest_strip`
  - `tests/test_u242_taken.py::test_a_cratekit_marked_playlist_is_never_offered_once_stripped`
  - `tests/test_u242_taken.py::test_a_hand_prefixed_playlist_is_recorded_stripped_and_never_offered`
  - `tests/test_u242_taken.py::test_a_release_whose_title_was_retitled_since_stamps_the_pass_mark`
  - `tests/test_u242_taken.py::test_a_stripped_playlist_named_like_a_followed_label_is_still_filed_by_its_mark`
  - `tests/test_u242_taken.py::test_every_old_title_is_restored_by_unmark_of_the_strip`
  - `tests/test_u242_taken.py::test_filing_after_a_real_strip_reads_every_playlist_as_it_did_before`
  - `tests/test_u242_taken.py::test_no_rename_is_made_for_a_playlist_the_record_does_not_hold`
  - `tests/test_u242_taken.py::test_unmark_of_a_legacy_pass_after_the_strip_releases_and_stamps_it`
  - `tests/test_u242_taken.py::test_unmark_of_the_migration_lets_nothing_go_and_nothing_is_offered`

Old text:

```
    taken_cli.migrate(cfg, listed)
    held = record.taken_ids()
    unheld = [identity for identity in planned if identity not in held]
```

New text:

```
    held = record.taken_ids()
    unheld = []
```

### `u242.M12_strip_skips_the_migration`

strip: rename without recording the prefixed playlists as taken first

- File: `src/cratekit/sync/strip_cli.py`
- Source: `u242.json`, row `M12_strip_skips_the_migration`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`
- Collected: 46 against a baseline of 46
- Kills: 14 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_a_ceiling_stop_names_what_landed_and_a_second_run_resumes`
  - `tests/test_u242_taken.py::test_a_collision_is_refused_and_named_and_the_rest_strip`
  - `tests/test_u242_taken.py::test_a_cratekit_marked_playlist_is_never_offered_once_stripped`
  - `tests/test_u242_taken.py::test_a_hand_prefixed_playlist_is_recorded_stripped_and_never_offered`
  - `tests/test_u242_taken.py::test_a_release_whose_title_was_retitled_since_stamps_the_pass_mark`
  - `tests/test_u242_taken.py::test_a_stripped_playlist_named_like_a_followed_label_is_still_filed_by_its_mark`
  - `tests/test_u242_taken.py::test_a_title_changed_since_the_plan_is_not_renamed`
  - `tests/test_u242_taken.py::test_every_old_title_is_restored_by_unmark_of_the_strip`
  - `tests/test_u242_taken.py::test_filing_after_a_real_strip_reads_every_playlist_as_it_did_before`
  - `tests/test_u242_taken.py::test_playlist_narrows_and_refuses_a_playlist_with_no_prefix`
  - `tests/test_u242_taken.py::test_the_strip_records_each_old_title_before_its_rename`
  - `tests/test_u242_taken.py::test_unmark_of_a_legacy_pass_after_the_strip_is_put_back_renames_back`
  - `tests/test_u242_taken.py::test_unmark_of_a_legacy_pass_after_the_strip_releases_and_stamps_it`
  - `tests/test_u242_taken.py::test_unmark_of_the_migration_lets_nothing_go_and_nothing_is_offered`

Old text:

```
    taken_cli.migrate(cfg, listed)
    held = record.taken_ids()
```

New text:

```
    held = record.taken_ids()
```

### `u242.M13_strip_no_collision_with_others`

strip plan: never refuse a stripped title another playlist already carries

- File: `src/cratekit/sync/strip_cli.py`
- Source: `u242.json`, row `M13_strip_no_collision_with_others`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`
- Collected: 46 against a baseline of 46
- Kills: 2 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_a_collision_is_refused_and_named_and_the_rest_strip`
  - `tests/test_u242_taken.py::test_the_gate_screen_lists_every_rename_and_every_refusal`

Old text:

```
        clash = others.get(to.casefold())
```

New text:

```
        clash = None
```

### `u242.M14_strip_no_collision_between_strips`

strip plan: never refuse two prefixed playlists stripped to one title

- File: `src/cratekit/sync/strip_cli.py`
- Source: `u242.json`, row `M14_strip_no_collision_between_strips`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_a_collision_is_refused_and_named_and_the_rest_strip`

Old text:

```
        twins = sorted(prefixed[one] for one in writes[to.casefold()] if one != identity)
```

New text:

```
        twins = []
```

### `u242.M15_strip_collision_case_exact`

strip plan: compare titles case exactly, so Techno beside techno is renamed

- File: `src/cratekit/sync/strip_cli.py`
- Source: `u242.json`, row `M15_strip_collision_case_exact`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_the_gate_screen_lists_every_rename_and_every_refusal`

Old text:

```
            others.setdefault(name.strip().casefold(), name)
```

New text:

```
            others.setdefault(name.strip(), name)
```

### `u242.M17_strip_no_recheck`

strip apply: rename a playlist retitled since the plan was shown

- File: `src/cratekit/sync/strip_cli.py`
- Source: `u242.json`, row `M17_strip_no_recheck`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_a_title_changed_since_the_plan_is_not_renamed`

Old text:

```
            if now.get(identity) != item["name"]:
                changed.append(identity)
                continue
            # RECORDED BEFORE THE RENAME
```

New text:

```
            if False:
                changed.append(identity)
                continue
            # RECORDED BEFORE THE RENAME
```

### `u242.M18_strip_records_no_old_title`

strip apply: rename without recording the old title, so unmark cannot put it back

- File: `src/cratekit/sync/strip_cli.py`
- Source: `u242.json`, row `M18_strip_records_no_old_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`
- Collected: 46 against a baseline of 46
- Kills: 4 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_every_old_title_is_restored_by_unmark_of_the_strip`
  - `tests/test_u242_taken.py::test_filing_after_a_real_strip_reads_every_playlist_as_it_did_before`
  - `tests/test_u242_taken.py::test_the_strip_records_each_old_title_before_its_rename`
  - `tests/test_u242_taken.py::test_unmark_of_a_legacy_pass_after_the_strip_is_put_back_renames_back`

Old text:

```
            record.record_marked(PASS, {identity: (item["name"], item["to"])})
            remote.rename_playlist(identity, item["to"])
```

New text:

```
            remote.rename_playlist(identity, item["to"])
```

### `r1372.K19_passed_by_strict`

passed_by: a write that began at the snapshot's very moment is not passed

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1372.json`, row `K19_passed_by_strict`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_snapshot_passes_the_carried_records_of_its_pair_that_began_before_it`

Old text:

```
            if began is not None and not began > moment:
```

New text:

```
            if began is not None and began < moment:
```

### `r1372.K20_passed_by_any_pair`

passed_by: a snapshot lets go of every pair's carried records, not its own

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1372.json`, row `K20_passed_by_any_pair`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_snapshot_passes_the_carried_records_of_its_pair_that_began_before_it`

Old text:

```
            if _account_of(key, steps, new=new, made=made) != account_id:
                continue
            began = placeholders.parse_hearted(steps.get(account))
            if began is not None
```

New text:

```
            began = placeholders.parse_hearted(steps.get(account))
            if began is not None
```

### `r1372.K21_made_pair_unmapped`

_account_of: a made pair is read under its key, not the account playlist it was made as

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1372.json`, row `K21_made_pair_unmapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`
- Collected: 89 against a baseline of 89
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_made_pair_is_read_under_the_account_playlist_it_was_made_as`
  - `tests/test_sync_pair_stopped.py::test_a_snapshot_passes_the_carried_records_of_its_pair_that_began_before_it`

Old text:

```
    if key.startswith(new):
        return steps.get(made) if isinstance(steps.get(made), str) else ""
    return key
```

New text:

```
    return key
```

### `r1376.F14_finished_filter_gone`

stopped_writes (sample, U225): a stop a later run finished is still read, by a first sync among others

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1376.json`, row `F14_finished_filter_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_later_run_that_finished_the_pair_hides_the_stopped_write_in_either_order`

Old text:

```
        if account_id not in finished or not finished[account_id] > began
```

New text:

```
        if True
```

### `u225.M6_front_keeps_nothing`

front_moves: no tail is kept, every asked track is moved

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `u225.json`, row `M6_front_keeps_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`
- Collected: 89 against a baseline of 89
- Kills: 26 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_orders_on_the_path_that_differ_only_by_a_track_taken_off_all_count`
  - `tests/test_sync_pair_stopped.py::test_the_copied_front_rule_is_the_adapters_on_every_order_of_four[before0]`
  - `tests/test_sync_pair_stopped.py::test_the_copied_front_rule_is_the_adapters_on_every_order_of_four[before10]`
  - `tests/test_sync_pair_stopped.py::test_the_copied_front_rule_is_the_adapters_on_every_order_of_four[before11]`
  - `tests/test_sync_pair_stopped.py::test_the_copied_front_rule_is_the_adapters_on_every_order_of_four[before12]`
  - `tests/test_sync_pair_stopped.py::test_the_copied_front_rule_is_the_adapters_on_every_order_of_four[before13]`
  - `tests/test_sync_pair_stopped.py::test_the_copied_front_rule_is_the_adapters_on_every_order_of_four[before14]`
  - `tests/test_sync_pair_stopped.py::test_the_copied_front_rule_is_the_adapters_on_every_order_of_four[before15]`
  - `tests/test_sync_pair_stopped.py::test_the_copied_front_rule_is_the_adapters_on_every_order_of_four[before16]`
  - `tests/test_sync_pair_stopped.py::test_the_copied_front_rule_is_the_adapters_on_every_order_of_four[before17]`
  - `tests/test_sync_pair_stopped.py::test_the_copied_front_rule_is_the_adapters_on_every_order_of_four[before18]`
  - `tests/test_sync_pair_stopped.py::test_the_copied_front_rule_is_the_adapters_on_every_order_of_four[before19]`
  - `tests/test_sync_pair_stopped.py::test_the_copied_front_rule_is_the_adapters_on_every_order_of_four[before1]`
  - `tests/test_sync_pair_stopped.py::test_the_copied_front_rule_is_the_adapters_on_every_order_of_four[before20]`
  - `tests/test_sync_pair_stopped.py::test_the_copied_front_rule_is_the_adapters_on_every_order_of_four[before21]`
  - ... and 11 more, see the JSON sidecar

Old text:

```
            keep += 1
    return list(reversed(wanted[: len(wanted) - keep]))
```

New text:

```
            keep += 0
    return list(reversed(wanted[: len(wanted) - keep]))
```

### `u225.M8_reached_strict_membership`

reached: a track added or taken off since is compared too

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `u225.json`, row `M8_reached_strict_membership`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`
- Collected: 89 against a baseline of 89
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_track_added_or_taken_off_since_is_left_out_of_the_comparison`
  - `tests/test_sync_pair_stopped.py::test_orders_on_the_path_that_differ_only_by_a_track_taken_off_all_count`
  - `tests/test_sync_pair_stopped.py::test_positions_counts_the_moves_that_leave_each_order_on_the_path`

Old text:

```
    common = set(current) & set(start)
```

New text:

```
    common = set(current) | set(start)
```

### `u225.M9_finish_ignored`

stopped_writes: a later run that finished the pair does not hide the stopped write

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `u225.json`, row `M9_finish_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`
- Collected: 89 against a baseline of 89
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_carried_copy_gives_way_to_its_own_runs_steps_kept_under_the_same_plan`
  - `tests/test_sync_pair_stopped.py::test_a_finished_or_unordered_write_is_no_stopped_one`
  - `tests/test_sync_pair_stopped.py::test_a_later_run_that_finished_the_pair_hides_the_stopped_write_in_either_order`

Old text:

```
            if done in steps:
                if account_id not in finished
```

New text:

```
            if False:
                if account_id not in finished
```

### `r1056.N10_pass_not_required`

build_mark: neither --xml nor --pass required, so a bare mark reaches the handler

- File: `src/cratekit/label/mark_cli.py`
- Source: `r1056.json`, row `N10_pass_not_required`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_the_pass_is_named_by_exactly_one_of_the_file_and_the_name[neither]`

Old text:

```
    proof = parser.add_mutually_exclusive_group(required=True)
```

New text:

```
    proof = parser.add_mutually_exclusive_group(required=False)
```

