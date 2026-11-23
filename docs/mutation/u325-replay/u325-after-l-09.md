# Mutation table: u325-after-l-09

Measured by `scripts/mutate.py` on 2026-11-23 00:28 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 124.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:21 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 7, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u99-a.A2_malformed_id_seed` | `src/cratekit/label/registry.py` | user | 3 file(s) | 293 | 7 | killed |
| `u99-a.A3_id_prefix_case` | `src/cratekit/label/registry.py` | user | 3 file(s) | 293 | 1 | killed |
| `u99-a.A4_id_digits_optional` | `src/cratekit/label/registry.py` | user | 3 file(s) | 293 | 1 | killed |
| `u99-a.A5_id_prefix_match` | `src/cratekit/label/registry.py` | user | 3 file(s) | 293 | 2 | killed |
| `u99-a.A7_add_unchecked_seeds` | `src/cratekit/label/registry.py` | user | 3 file(s) | 293 | 7 | killed |
| `u99-a.A8_edit_unchecked_seeds` | `src/cratekit/label/registry.py` | user | 3 file(s) | 293 | 1 | killed |
| `u99-b.A6r_store_limit_floor` | `src/cratekit/label/registry.py` | maintainer | 3 file(s) | 293 | 1 | killed |
| `u287-m11.M11_gone_offers_nothing` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 3 | killed |
| `u287.M13_folder_separator` | `src/cratekit/sync/removed.py` | maintainer | 1 file(s) | 74 | 1 | killed |
| `u287.M14_twin_is_own_filing` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 32 | killed |
| `u287.M17_gone_with_no_record_is_not_whole` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 2 | killed |
| `u287.M18_set_aside_rows_count` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 1 | killed |
| `u287.M19_old_prefix_is_synced` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 1 | killed |
| `u287.M1_partial_read_stops_offers` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 8 | killed |
| `u287.M20_unreadable_record_is_not_whole` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 1 | killed |
| `u287.M2_held_by_isrc` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 3 | killed |
| `u287.M3_held_by_recording` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 2 | killed |
| `u287.M4_held_before_the_pass` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 2 | killed |
| `u287.M5_not_this_pass_file` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 2 | killed |
| `u287.M6_on_another_synced` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 8 | killed |
| `u287.M7_in_a_playlist_of_yours` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 3 | killed |
| `u287.M8_empty_read_untrusted` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 1 | killed |
| `u287.M9_short_read_untrusted` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 1 | killed |
| `u288.M16_stale_digest` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 2 | killed |
| `u288.M17_only_the_offered` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 8 | killed |
| `u288.M18_unmeasured_kept` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 1 | killed |
| `u288.M19_first_position` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 1 | killed |
| `u288.M20_read_back_refusal` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 1 | killed |
| `u288.M14_confinement_not_called` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 74 | 2 | killed |
| `u288.M3_unmeasured_tables_skipped` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 74 | 3 | killed |
| `u288.M4_target_id_not_asked` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 74 | 1 | killed |
| `u288.M5_prepare_liveness` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 74 | 1 | killed |
| `u288.M6_prepare_unmeasured_refusal` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 74 | 3 | killed |
| `u288.M7_prepare_identity` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 74 | 1 | killed |
| `u288.M8_memberships_kept` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 74 | 19 | killed |
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
| `r923.N11_digest_drops_items` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 2 | killed |
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
| `u115.F21_other_volume_compared` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 1 | killed |
| `u115.F22_off_apfs_decides` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 1 | killed |
| `u115.F23_loose_digits` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 3 | killed |
| `u115.F5_bound_boundary` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 2 | killed |
| `u115.F6_every_id_above` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 12 | killed |
| `u115.F7_zero_is_not_zero` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 4 | killed |
| `u115.F9_unreadable_file_dropped_silently` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 5 | killed |
| `r923.N14_verb_writes_on_abort` | `src/cratekit/write/row_defaults_cli.py` | user | 1 file(s) | 53 | 7 | killed |
| `r923.N15_verb_writes_empty_plan` | `src/cratekit/write/row_defaults_cli.py` | user | 1 file(s) | 53 | 2 | killed |
| `r923.N16_ack_not_read` | `src/cratekit/write/row_defaults_cli.py` | user | 1 file(s) | 53 | 1 | killed |
| `r923.N17_write_handle_not_closed` | `src/cratekit/write/row_defaults_cli.py` | maintainer | 1 file(s) | 53 | 1 | killed |
| `u115.F18_undecidable_unsaid` | `src/cratekit/write/row_defaults_cli.py` | user | 1 file(s) | 53 | 1 | killed |
| `u115.F19_unrenumbered_unsaid` | `src/cratekit/write/row_defaults_cli.py` | user | 1 file(s) | 53 | 2 | killed |
| `r289-c.B9r_children_unreadable_raises` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
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
| `r289-a.A1_appledouble_gone` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 1 | killed |
| `r289-a.A2_appledouble_one_dot` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 1 | killed |
| `r289-a.A3_staging_dirs_gone` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 4 | killed |
| `r289-a.A4_staging_dirs_acquire_only` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 2 | killed |
| `r289-a.A5_staging_dirs_absolute` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 1 | killed |
| `r650-a.B3_engine_drops_the_flag_on_the_write` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 3 | killed |

## Zero rows and what they owe

- `r289-c.B9r_children_unreadable_raises` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `u99-a.A2_malformed_id_seed`

check_seed: drop the malformed id: refusal, so id:12a is stored and later searched for as a name

- File: `src/cratekit/label/registry.py`
- Source: `u99-a.json`, row `A2_malformed_id_seed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_a_malformed_id_seed_on_a_new_label_creates_no_entry`
  - `tests/test_label_registry_verbs.py::test_a_malformed_id_seed_on_set_refuses_and_writes_nothing`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[ID:12]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id: 12]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id:-4]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id:12a]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id:]`

Old text:

```
    if text[:3].casefold() == "id:" and not _ID_SEED.fullmatch(text):
```

New text:

```
    if False:
```

### `u99-a.A3_id_prefix_case`

check_seed: compare the id: prefix case sensitively, so ID:12 is stored as a name

- File: `src/cratekit/label/registry.py`
- Source: `u99-a.json`, row `A3_id_prefix_case`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[ID:12]`

Old text:

```
    if text[:3].casefold() == "id:" and not _ID_SEED.fullmatch(text):
```

New text:

```
    if text[:3] == "id:" and not _ID_SEED.fullmatch(text):
```

### `u99-a.A4_id_digits_optional`

_ID_SEED: allow zero digits, so a bare id: is stored

- File: `src/cratekit/label/registry.py`
- Source: `u99-a.json`, row `A4_id_digits_optional`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id:]`

Old text:

```
_ID_SEED = re.compile(r"id:[0-9]+")
```

New text:

```
_ID_SEED = re.compile(r"id:[0-9]*")
```

### `u99-a.A5_id_prefix_match`

check_seed: match the identifier as a prefix rather than whole, so id:12a is stored

- File: `src/cratekit/label/registry.py`
- Source: `u99-a.json`, row `A5_id_prefix_match`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_a_malformed_id_seed_on_set_refuses_and_writes_nothing`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id:12a]`

Old text:

```
not _ID_SEED.fullmatch(text):
```

New text:

```
not _ID_SEED.match(text):
```

### `u99-a.A7_add_unchecked_seeds`

add: store the seeds unchecked, so a malformed seed on add is written

- File: `src/cratekit/label/registry.py`
- Source: `u99-a.json`, row `A7_add_unchecked_seeds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_a_malformed_id_seed_on_a_new_label_creates_no_entry`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[   ]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[ID:12]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id: 12]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id:-4]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id:12a]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id:]`

Old text:

```
        seeds = _checked_seeds(seed_artists)

```

New text:

```
        seeds = tuple(seed_artists)

```

### `u99-a.A8_edit_unchecked_seeds`

edit: store the seeds unchecked, so a malformed seed on set is written

- File: `src/cratekit/label/registry.py`
- Source: `u99-a.json`, row `A8_edit_unchecked_seeds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_a_malformed_id_seed_on_set_refuses_and_writes_nothing`

Old text:

```
        seeds = _checked_seeds(seed_artists) if seed_artists is not None else None
```

New text:

```
        seeds = tuple(seed_artists) if seed_artists is not None else None
```

### `u99-b.A6r_store_limit_floor`

check_track_limit: accept zero, measured again after the store level test the A6 zero bought

- File: `src/cratekit/label/registry.py`
- Source: `u99-b.json`, row `A6r_store_limit_floor`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_the_store_refuses_a_limit_below_one_from_a_python_caller[0]`

Old text:

```
or limit < 1:
```

New text:

```
or limit < 0:
```

### `u287-m11.M11_gone_offers_nothing`

removals: read a playlist not read whole as removing every track, measured again after the zero of the first table was given a test

- File: `src/cratekit/sync/removed.py`
- Source: `u287-m11.json`, row `M11_gone_offers_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_synced_playlist_not_read_whole_offers_nothing_from_any_playlist[empty]`
  - `tests/test_sync_removed.py::test_a_synced_playlist_not_read_whole_offers_nothing_from_any_playlist[short]`
  - `tests/test_sync_removed.py::test_a_synced_playlist_not_read_whole_offers_nothing_from_any_playlist[unreadable]`

Old text:

```
        if one.account in reads and reads[one.account].state == READ
```

New text:

```
        if one.account in reads
```

### `u287.M13_folder_separator`

_under: compare the folder as a bare prefix, so a sibling folder sharing its name's start reads as the pass's

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M13_folder_separator`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_path_is_under_a_folder_only_past_a_separator_and_in_one_unicode_form`

Old text:

```
        if root and (held.startswith(root + "/") or held.startswith(root + "\\")):
```

New text:

```
        if root and held.startswith(root):
```

### `u287.M14_twin_is_own_filing`

plan_removed: leave the recorded twins out of the pass's own filing, so the landing's own twin keeps a track

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M14_twin_is_own_filing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 32 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_commit_that_lands_and_then_raises_still_records_every_row`
  - `tests/test_sync_removed.py::test_a_damaged_job_of_another_playlist_never_refuses_the_verb[False]`
  - `tests/test_sync_removed.py::test_a_damaged_job_of_another_playlist_never_refuses_the_verb[True]`
  - `tests/test_sync_removed.py::test_a_genre_playlist_of_a_native_routing_tree_keeps_nothing`
  - `tests/test_sync_removed.py::test_a_gone_downloaded_playlist_holds_what_its_pass_recorded`
  - `tests/test_sync_removed.py::test_a_gone_playlist_a_pass_swept_and_never_landed_holds_what_it_recorded`
  - `tests/test_sync_removed.py::test_a_new_track_taken_off_is_offered_and_an_owned_one_is_kept_as_held_before`
  - `tests/test_sync_removed.py::test_a_plan_that_moved_before_the_write_refuses_with_nothing_written`
  - `tests/test_sync_removed.py::test_a_playlist_the_account_list_omits_and_its_id_opens_is_read_and_keeps_its_tracks`
  - `tests/test_sync_removed.py::test_a_playlist_the_account_says_holds_none_is_read_empty_and_every_new_track_offered`
  - `tests/test_sync_removed.py::test_a_position_the_pass_holds_is_kept_and_the_collection_not_walked`
  - `tests/test_sync_removed.py::test_a_read_back_that_disagrees_refuses_as_unverified`
  - `tests/test_sync_removed.py::test_a_refused_removal_gives_the_deletion_pass_no_position`
  - `tests/test_sync_removed.py::test_a_removed_row_the_database_holds_again_is_not_offered_by_delete_review`
  - `tests/test_sync_removed.py::test_a_renumbering_that_moved_between_the_gate_and_the_write_refuses_as_stale`
  - ... and 17 more, see the JSON sidecar

Old text:

```
            own = own_nodes.union(
                *(made.get(account, frozenset()) for account in held.accounts),
            )
```

New text:

```
            own = own_nodes
```

### `u287.M17_gone_with_no_record_is_not_whole`

read_one: read a playlist neither read finds and nothing records as gone, holding nothing, rather than not read whole

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M17_gone_with_no_record_is_not_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_damaged_job_of_another_playlist_never_refuses_the_verb[False]`
  - `tests/test_sync_removed.py::test_a_synced_playlist_nothing_records_that_neither_read_finds_offers_nothing`

Old text:

```
            if not known:
                return Listing(
```

New text:

```
            if False:
                return Listing(
```

### `u287.M18_set_aside_rows_count`

read_one: leave the reader's set aside rows out of the identity sets

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M18_set_aside_rows_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_row_the_reader_set_aside_keeps_a_track_by_its_isrc`

Old text:

```
        for one in readable.unread.values()
    )
```

New text:

```
        for one in ()
    )
```

### `u287.M19_old_prefix_is_synced`

synced: leave a playlist still titled with the retired swept prefix out of the synced set

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M19_old_prefix_is_synced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_playlist_still_titled_with_the_old_prefix_is_synced`

Old text:

```
                    if playlists.is_swept_name(one.name)
```

New text:

```
                    if False
```

### `u287.M1_partial_read_stops_offers`

plan_removed: never read a synced listing as partial, so an unreadable, short or empty playlist or hearts no longer stops any offer

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M1_partial_read_stops_offers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_damaged_job_of_another_playlist_never_refuses_the_verb[False]`
  - `tests/test_sync_removed.py::test_a_synced_playlist_not_read_whole_offers_nothing_from_any_playlist[empty]`
  - `tests/test_sync_removed.py::test_a_synced_playlist_not_read_whole_offers_nothing_from_any_playlist[short]`
  - `tests/test_sync_removed.py::test_a_synced_playlist_not_read_whole_offers_nothing_from_any_playlist[unreadable]`
  - `tests/test_sync_removed.py::test_a_synced_playlist_nothing_records_that_neither_read_finds_offers_nothing`
  - `tests/test_sync_removed.py::test_hearts_not_read_whole_offer_nothing[empty]`
  - `tests/test_sync_removed.py::test_hearts_not_read_whole_offer_nothing[short]`
  - `tests/test_sync_removed.py::test_hearts_not_read_whole_offer_nothing[unreadable]`

Old text:

```
    partial = any(one.state in NOT_WHOLE for one in listings)
```

New text:

```
    partial = False
```

### `u287.M20_unreadable_record_is_not_whole`

recorded_contents: read a gone playlist whose job reports cannot be read as holding nothing recorded, refusing the verb

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M20_unreadable_record_is_not_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_damaged_job_of_another_playlist_never_refuses_the_verb[False]`

Old text:

```
        except CratekitError:
            return None
        return tuple(found) or None
```

New text:

```
        except ZeroDivisionError:
            return None
        return tuple(found) or None
```

### `u287.M2_held_by_isrc`

Listing.holds: drop the ISRC test, so a track relisted under another id with its ISRC reads as removed

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M2_held_by_isrc`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_listing_holds_a_track_by_any_of_three_tests_and_only_a_read_or_gone_one_holds`
  - `tests/test_sync_removed.py::test_a_row_the_reader_set_aside_keeps_a_track_by_its_isrc`
  - `tests/test_sync_removed.py::test_a_track_still_on_another_synced_playlist_is_kept_by_id_isrc_and_recording`

Old text:

```
        if wanted.isrc and wanted.isrc.strip().upper() in self.isrcs:
```

New text:

```
        if False and wanted.isrc and wanted.isrc.strip().upper() in self.isrcs:
```

### `u287.M3_held_by_recording`

Listing.holds: drop the folded recording test, so a relinked track with its artist and title reads as removed

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M3_held_by_recording`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_listing_holds_a_track_by_any_of_three_tests_and_only_a_read_or_gone_one_holds`
  - `tests/test_sync_removed.py::test_a_track_still_on_another_synced_playlist_is_kept_by_id_isrc_and_recording`

Old text:

```
        return recording(wanted) in self.recordings
```

New text:

```
        return False
```

### `u287.M4_held_before_the_pass`

_answer: drop the held before the pass keep, so a track the library owned when the job ran can be offered

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M4_held_before_the_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_new_track_taken_off_is_offered_and_an_owned_one_is_kept_as_held_before`
  - `tests/test_sync_removed.py::test_a_playlist_the_account_says_holds_none_is_read_empty_and_every_new_track_offered`

Old text:

```
    if not held.carried:
        return replace(shown, why=HELD_BEFORE)
```

New text:

```
    if False:
        return replace(shown, why=HELD_BEFORE)
```

### `u287.M5_not_this_pass_file`

_answer: drop the filed folder keep, so a hand brought file the match found can be offered

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M5_not_this_pass_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_file_another_pass_filed_is_not_this_pass_s_file`
  - `tests/test_sync_removed.py::test_a_match_on_a_file_the_pass_did_not_file_is_kept`

Old text:

```
    if not held.brought:
        return replace(shown, why=NOT_THIS_PASS)
```

New text:

```
    if False:
        return replace(shown, why=NOT_THIS_PASS)
```

### `u287.M6_on_another_synced`

_answer: drop the still on another synced playlist keep

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M6_on_another_synced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_gone_downloaded_playlist_holds_what_its_pass_recorded`
  - `tests/test_sync_removed.py::test_a_gone_playlist_a_pass_swept_and_never_landed_holds_what_it_recorded`
  - `tests/test_sync_removed.py::test_a_playlist_a_later_pass_swept_and_never_landed_still_keeps_its_tracks`
  - `tests/test_sync_removed.py::test_a_playlist_still_titled_with_the_old_prefix_is_synced`
  - `tests/test_sync_removed.py::test_a_playlist_the_account_list_omits_and_its_id_opens_is_read_and_keeps_its_tracks`
  - `tests/test_sync_removed.py::test_a_row_the_reader_set_aside_keeps_a_track_by_its_isrc`
  - `tests/test_sync_removed.py::test_a_track_hearted_on_the_account_is_kept_by_the_hearts`
  - `tests/test_sync_removed.py::test_a_track_still_on_another_synced_playlist_is_kept_by_id_isrc_and_recording`

Old text:

```
    if still:
        return replace(shown, why=ON_ANOTHER, kept_by=still)
```

New text:

```
    if False:
        return replace(shown, why=ON_ANOTHER, kept_by=still)
```

### `u287.M7_in_a_playlist_of_yours`

_answer: drop the playlist of yours keep, so a track in a hand made playlist or All Favorites can be offered

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M7_in_a_playlist_of_yours`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_genre_playlist_of_a_native_routing_tree_keeps_nothing`
  - `tests/test_sync_removed.py::test_a_plan_that_moved_before_the_write_refuses_with_nothing_written`
  - `tests/test_sync_removed.py::test_a_track_in_a_playlist_of_yours_is_kept_and_its_own_filing_keeps_nothing`

Old text:

```
    if yours:
        return replace(shown, why=IN_YOURS, kept_by=yours)
```

New text:

```
    if False:
        return replace(shown, why=IN_YOURS, kept_by=yours)
```

### `u287.M8_empty_read_untrusted`

read_one: trust an empty read with an unknown count, so a provider fault reads every track removed

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M8_empty_read_untrusted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_synced_playlist_not_read_whole_offers_nothing_from_any_playlist[empty]`

Old text:

```
    if not readable.order and (shown is None or shown.tracks != 0):
```

New text:

```
    if False:
```

### `u287.M9_short_read_untrusted`

read_one: trust a listing short of its declared count

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M9_short_read_untrusted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_synced_playlist_not_read_whole_offers_nothing_from_any_playlist[short]`

Old text:

```
    if readable.short is not None:
        block = readable.short.block()
```

New text:

```
    if False:
        block = readable.short.block()
```

### `u288.M16_stale_digest`

apply_removed: never refuse a plan that moved between the gate and the write

- File: `src/cratekit/sync/removed.py`
- Source: `u288.json`, row `M16_stale_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_plan_that_moved_before_the_write_refuses_with_nothing_written`
  - `tests/test_sync_removed.py::test_a_renumbering_that_moved_between_the_gate_and_the_write_refuses_as_stale`

Old text:

```
    if again.digest != plan.digest:
```

New text:

```
    if False:
```

### `u288.M17_only_the_offered`

apply_removed: take out every answered row that has one, kept rows included, not only the offered

- File: `src/cratekit/sync/removed.py`
- Source: `u288.json`, row `M17_only_the_offered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_commit_that_lands_and_then_raises_still_records_every_row`
  - `tests/test_sync_removed.py::test_a_removed_row_the_database_holds_again_is_not_offered_by_delete_review`
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`
  - `tests/test_sync_removed.py::test_a_track_only_marked_out_of_a_playlist_renumbers_none_of_its_live_members`
  - `tests/test_sync_removed.py::test_apply_takes_out_exactly_the_offered_rows_and_every_row_naming_them`
  - `tests/test_sync_removed.py::test_delete_review_after_the_apply_offers_the_removed_file_and_none_other`
  - `tests/test_sync_removed.py::test_the_removal_writes_no_beat_grid_and_no_tempo`
  - `tests/test_sync_removed.py::test_the_session_record_names_every_row_removed_and_restore_list_reads_it`

Old text:

```
    offered = plan.offered
    if not offered:
```

New text:

```
    offered = tuple(one for one in plan.answers if one.content_id)
    if not offered:
```

### `u288.M18_unmeasured_kept`

_answer: drop the keep of a row an unmeasured table names, so a vox tagged track is offered and then refuses the apply

- File: `src/cratekit/sync/removed.py`
- Source: `u288.json`, row `M18_unmeasured_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`

Old text:

```
    if unmeasured:
        return replace(shown, why=UNMEASURED, kept_by=tuple(sorted(unmeasured)))
```

New text:

```
    if False:
        return replace(shown, why=UNMEASURED, kept_by=tuple(sorted(unmeasured)))
```

### `u288.M19_first_position`

apply_removed: give the deletion pass no first position, so a first delete review accepts the removal as history

- File: `src/cratekit/sync/removed.py`
- Source: `u288.json`, row `M19_first_position`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_delete_review_after_the_apply_offers_the_removed_file_and_none_other`

Old text:

```
        first = _first_deletion_position(cfg, db)
```

New text:

```
        first = None
```

### `u288.M20_read_back_refusal`

apply_removed: report a read back that disagrees as success

- File: `src/cratekit/sync/removed.py`
- Source: `u288.json`, row `M20_read_back_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_read_back_that_disagrees_refuses_as_unverified`

Old text:

```
        violations = removal.read_back()
        if violations:
```

New text:

```
        violations = removal.read_back()
        if False:
```

### `u288.M14_confinement_not_called`

CollectionRemoval.commit: skip the SQL confinement before the commit

- File: `src/cratekit/core/rb_writer.py`
- Source: `u288.json`, row `M14_confinement_not_called`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_renumbering_that_moves_any_other_membership_is_refused_with_nothing_written`
  - `tests/test_sync_removed.py::test_commit_proves_the_removal_confined_before_it_commits`

Old text:

```
        assert_collection_removal_confined(self.db, self.before, removed=self.content_ids)
        commit_guarded(
```

New text:

```
        commit_guarded(
```

### `u288.M3_unmeasured_tables_skipped`

content_references: ask no table, so a My Tag, sampler or unknown table naming the row is never refused nor kept

- File: `src/cratekit/core/rb_writer.py`
- Source: `u288.json`, row `M3_unmeasured_tables_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`
  - `tests/test_sync_removed.py::test_the_writer_refuses_a_row_an_unmeasured_table_names_with_nothing_written[CREATE TABLE "someFutureTable" (ID TEXT PRIMARY KEY, ContentID TEXT)-INSERT INTO "someFutureTable" (ID, ContentID) VALUES ('x-1', ?)]`
  - `tests/test_sync_removed.py::test_the_writer_refuses_a_row_an_unmeasured_table_names_with_nothing_written[None-INSERT INTO "djmdSongSampler" (ID, ContentID) VALUES ('x-1', ?)]`

Old text:

```
        asked = [CONTENT_REFERENCE_COLUMN] if CONTENT_REFERENCE_COLUMN in names else []
```

New text:

```
        asked = []
```

### `u288.M4_target_id_not_asked`

content_references: drop the TargetID column, so an image row naming the track is left naming a row that is gone

- File: `src/cratekit/core/rb_writer.py`
- Source: `u288.json`, row `M4_target_id_not_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_the_writer_refuses_a_row_an_unmeasured_table_names_with_nothing_written[None-INSERT INTO "imageFile" (ID, TargetID) VALUES ('x-1', ?)]`

Old text:

```
        if TARGET_REFERENCE_COLUMN in names:
```

New text:

```
        if False:
```

### `u288.M5_prepare_liveness`

CollectionRemoval.prepare: drop the soft delete check, so a row rekordbox already removed is taken out as live

- File: `src/cratekit/core/rb_writer.py`
- Source: `u288.json`, row `M5_prepare_liveness`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_prepare_refuses_a_row_not_live_and_a_database_with_no_identity`

Old text:

```
            if row is None or soft_deleted(
                row,
                message=(
                    f"the collection row {key!r} cannot say whether rekordbox removed it, "
```

New text:

```
            if row is None or False and soft_deleted(
                row,
                message=(
                    f"the collection row {key!r} cannot say whether rekordbox removed it, "
```

### `u288.M6_prepare_unmeasured_refusal`

CollectionRemoval.prepare: drop the refusal of a row an unmeasured table names

- File: `src/cratekit/core/rb_writer.py`
- Source: `u288.json`, row `M6_prepare_unmeasured_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_the_writer_refuses_a_row_an_unmeasured_table_names_with_nothing_written[CREATE TABLE "someFutureTable" (ID TEXT PRIMARY KEY, ContentID TEXT)-INSERT INTO "someFutureTable" (ID, ContentID) VALUES ('x-1', ?)]`
  - `tests/test_sync_removed.py::test_the_writer_refuses_a_row_an_unmeasured_table_names_with_nothing_written[None-INSERT INTO "djmdSongSampler" (ID, ContentID) VALUES ('x-1', ?)]`
  - `tests/test_sync_removed.py::test_the_writer_refuses_a_row_an_unmeasured_table_names_with_nothing_written[None-INSERT INTO "imageFile" (ID, TargetID) VALUES ('x-1', ?)]`

Old text:

```
        held = content_references(db, ids)
        if held:
```

New text:

```
        held = content_references(db, ids)
        if False:
```

### `u288.M7_prepare_identity`

CollectionRemoval.prepare: drop the refusal of a database with no identity, so the record is bound to nothing

- File: `src/cratekit/core/rb_writer.py`
- Source: `u288.json`, row `M7_prepare_identity`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_prepare_refuses_a_row_not_live_and_a_database_with_no_identity`

Old text:

```
        identity = database_id(db)
        if not identity:
```

New text:

```
        identity = database_id(db)
        if False:
```

### `u288.M8_memberships_kept`

remove_from_collection: delete from the five tables after the membership table only, so the track's memberships stay naming a row that is gone

- File: `src/cratekit/core/rb_writer.py`
- Source: `u288.json`, row `M8_memberships_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 19 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_commit_that_lands_and_then_raises_still_records_every_row`
  - `tests/test_sync_removed.py::test_a_history_list_holding_others_keeps_its_numbers`
  - `tests/test_sync_removed.py::test_a_member_that_moved_after_the_prepare_refuses_its_renumbering_with_nothing_written`
  - `tests/test_sync_removed.py::test_a_position_the_pass_holds_is_kept_and_the_collection_not_walked`
  - `tests/test_sync_removed.py::test_a_read_back_that_disagrees_refuses_as_unverified`
  - `tests/test_sync_removed.py::test_a_removal_that_changes_anything_it_did_not_plan_is_refused_before_its_commit`
  - `tests/test_sync_removed.py::test_a_removed_member_in_the_middle_of_three_leaves_one_and_two_and_nothing_else_moved`
  - `tests/test_sync_removed.py::test_a_removed_row_the_database_holds_again_is_not_offered_by_delete_review`
  - `tests/test_sync_removed.py::test_a_renumbering_that_moves_any_other_membership_is_refused_with_nothing_written`
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`
  - `tests/test_sync_removed.py::test_a_track_only_marked_out_of_a_playlist_renumbers_none_of_its_live_members`
  - `tests/test_sync_removed.py::test_an_append_after_a_renumbering_takes_the_next_position`
  - `tests/test_sync_removed.py::test_apply_takes_out_exactly_the_offered_rows_and_every_row_naming_them`
  - `tests/test_sync_removed.py::test_commit_proves_the_removal_confined_before_it_commits`
  - `tests/test_sync_removed.py::test_delete_review_after_the_apply_offers_the_removed_file_and_none_other`
  - ... and 4 more, see the JSON sidecar

Old text:

```
    for table in COLLECTION_REMOVAL_TABLES[1:]:
```

New text:

```
    for table in COLLECTION_REMOVAL_TABLES[2:]:
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

### `r923.N11_digest_drops_items`

The digest no longer covers the rows and columns the plan fills

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N11_digest_drops_items`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_the_digest_moves_when_a_planned_column_is_filled_elsewhere`
  - `tests/test_repair_rows.py::test_the_digest_moves_when_a_random_id_is_replaced_elsewhere`

Old text:

```
                "items": [item.to_json() for item in self.items],
```

New text:

```
                "items": [],
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

### `r289-c.B9r_children_unreadable_raises`

Let an unlistable directory raise out of the sweep and fail the verb

- File: `src/cratekit/acquire/cli.py`
- Source: `r289-c.json`, row `B9r_children_unreadable_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    try:
        return tuple(sorted(directory.iterdir()))
    except OSError:
        return ()
```

New text:

```
    return tuple(sorted(directory.iterdir()))
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

