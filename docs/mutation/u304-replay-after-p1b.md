# Mutation table: u304-replay-after-p1b

Measured by `scripts/mutate.py` on 2026-11-23 03:09 UTC, branch `HEAD` at `fd78d188`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22911 collected. pytest invocations for this batch: 133.

Full baseline: measured by this driver (the battery's verdict was not read: no battery verdict at `.cloud-battery/verdict.json`).

Subset baselines: 18, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `/tmp/claude-0/-home-user-cratekit/9c4fb6d1-21a5-58b2-b145-6b7e9e36fc05/scratchpad/u304-replay-after-known-failures.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22911 against 22911. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r1264.M19_warning` | `src/cratekit/sync/pair_screen.py` | user | 1 file(s) | 20 | 1 | killed |
| `r1264.M1_unread_dropped` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 95 | 17 | killed |
| `r1264.M20_item` | `src/cratekit/sync/pair_screen.py` | user | 1 file(s) | 20 | 7 | killed |
| `r1264.M2_unread_isrc_on_account` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 87 | 1 | killed |
| `r1264.M3_account_keys_listing_order` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 117 | 3 | killed |
| `r1264.M4_account_keys_filter` | `src/cratekit/sync/pair_plan.py` | user | 2 file(s) | 96 | 12 | killed |
| `r1264.M5_unread_keys_empty` | `src/cratekit/sync/pair_plan.py` | user | 2 file(s) | 66 | 4 | killed |
| `r1264.M6_base_strip` | `src/cratekit/sync/pair_plan.py` | user | 2 file(s) | 66 | 3 | killed |
| `r1264.M8_order_after_listing` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 117 | 3 | killed |
| `r1264.M9_firsts_keep_unread` | `src/cratekit/sync/pair_plan.py` | user | 2 file(s) | 96 | 2 | killed |
| `r1372.K17_no_let_go_at_snapshot` | `src/cratekit/sync/pair_write.py` | user | 19 file(s) | 664 | 2 | killed |
| `r1372.K1_no_carry` | `src/cratekit/sync/pair_write.py` | user | 19 file(s) | 664 | 9 | killed |
| `r1372.K22_mark_guard_gone` | `src/cratekit/sync/pair_read.py` | user | 19 file(s) | 664 | 2 | killed |
| `r1372.K23_mark_guard_inclusive` | `src/cratekit/sync/pair_read.py` | user | 19 file(s) | 664 | 1 | killed |
| `r1372.K4_carry_unwritten_not_refused` | `src/cratekit/sync/pair_write.py` | user | 19 file(s) | 664 | 1 | killed |
| `r1372.K6_reader_ignores_carried` | `src/cratekit/sync/pair_read.py` | user | 19 file(s) | 664 | 7 | killed |
| `r1372.K7_copy_never_gives_way` | `src/cratekit/sync/pair_read.py` | user | 19 file(s) | 664 | 1 | killed |
| `r1372.K8_copy_gives_way_to_any_plan` | `src/cratekit/sync/pair_read.py` | user | 19 file(s) | 664 | 1 | killed |
| `r1372.K9_carried_unread_unsaid` | `src/cratekit/sync/pair_read.py` | user | 19 file(s) | 664 | 1 | killed |
| `r1376.F11_leader_lost` | `src/cratekit/sync/pair_plan.py` | user | 19 file(s) | 664 | 4 | killed |
| `r1376.F13_snapshot_guard_inclusive` | `src/cratekit/sync/pair_read.py` | user | 19 file(s) | 664 | 34 | killed |
| `r1376.F1_first_stop_none` | `src/cratekit/sync/pair_read.py` | user | 19 file(s) | 664 | 7 | killed |
| `r1376.F3_call_site_gone` | `src/cratekit/sync/pair_plan.py` | user | 19 file(s) | 664 | 6 | killed |
| `r1376.F4_first_sync_unrecorded_only` | `src/cratekit/sync/pair_plan.py` | user | 19 file(s) | 664 | 1 | killed |
| `r1376.F5_first_sync_marked_only` | `src/cratekit/sync/pair_plan.py` | user | 19 file(s) | 664 | 318 | killed |
| `r1376.F6_every_sync_first` | `src/cratekit/sync/pair_plan.py` | user | 19 file(s) | 664 | 4 | killed |
| `r1383-digest.M8_digest_drops_hold` | `src/cratekit/sync/pair_model.py` | user | 5 file(s) | 162 | 1 | killed |
| `r1383-digest.M9_digest_always_keyed` | `src/cratekit/sync/pair_model.py` | maintainer | 5 file(s) | 162 | 1 | killed |
| `r1383.M10_warning_never_said` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 137 | 5 | killed |
| `r1383.M12_unlisted_said_as_records` | `src/cratekit/sync/pair_screen.py` | user | 1 file(s) | 76 | 1 | killed |
| `r1383.M13_records_unnamed` | `src/cratekit/sync/pair_screen.py` | user | 1 file(s) | 76 | 2 | killed |
| `r1383.M14_hold_before_awaiting` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 137 | 2 | killed |
| `r1383.M15_hold_before_twin` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 137 | 1 | killed |
| `r1383.M16_zero_said_as_count` | `src/cratekit/sync/pair_screen.py` | user | 1 file(s) | 76 | 1 | killed |
| `r1383.M17_total_uncounted` | `src/cratekit/sync/pair_screen.py` | user | 2 file(s) | 108 | 2 | killed |
| `r1383.M18_sampled_own_landed_step` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 137 | 1 | killed |
| `r1383.M19_sampled_mirrors_empty` | `src/cratekit/sync/pair_read.py` | user | 3 file(s) | 137 | 11 | killed |
| `r1383.M1_scan_drops_unread` | `src/cratekit/sync/pair_read.py` | user | 4 file(s) | 183 | 5 | killed |
| `r1383.M2_hold_branch_removed` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 137 | 4 | killed |
| `r1383.M3_hold_without_isrc` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 137 | 1 | killed |
| `r1383.M4_hold_while_readable` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 137 | 27 | killed |
| `r1383.M5_hold_dropped_from_plan` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 137 | 2 | killed |
| `r1383.M6_gate_item_dropped` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 137 | 2 | killed |
| `r1383.M7_gate_item_side` | `src/cratekit/sync/pair_screen.py` | user | 2 file(s) | 108 | 2 | killed |
| `r1385.M10_reason_dropped` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 293 | 7 | killed |
| `r1385.M11_name_fallback` | `src/cratekit/sync/pair_read.py` | user | 8 file(s) | 293 | 1 | killed |
| `r1385.M12_check_reads_no_job` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 293 | 2 | killed |
| `r1385.M13_warning_unsplit` | `src/cratekit/sync/pair_screen.py` | user | 8 file(s) | 293 | 1 | killed |
| `r1385.M14_warning_here_dropped` | `src/cratekit/sync/pair_screen.py` | user | 8 file(s) | 293 | 2 | killed |
| `r1385.M15_failed_jobs_hold` | `src/cratekit/sync/pair_read.py` | user | 8 file(s) | 293 | 2 | killed |
| `r1385.M1_no_job_holds_anything` | `src/cratekit/sync/pair_read.py` | user | 8 file(s) | 293 | 13 | killed |
| `r1385.M2_other_jobs_not_asked` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 293 | 6 | killed |
| `r1385.M4_plan_not_asked` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 293 | 3 | killed |
| `r1385.M6_ask_not_registered` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 293 | 3 | killed |
| `r1385.M8_own_reads_every_job` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 293 | 6 | killed |
| `r1385.M9_own_reads_no_job` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 293 | 8 | killed |
| `r1394.P1_counts_never_written` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 752 | 4 | killed |
| `r1394.P2_counts_not_carried` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 752 | 1 | killed |
| `r1394.P3_begun_answers_no_recorder` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 752 | 5 | killed |
| `r1394.P4_finish_from_landed` | `src/cratekit/sync/pair_plan.py` | user | 20 file(s) | 752 | 2 | killed |
| `r1394.P5_finish_from_any_path_reading` | `src/cratekit/sync/pair_plan.py` | user | 20 file(s) | 752 | 6 | killed |
| `r1394.P6_off_path_held` | `src/cratekit/sync/pair_plan.py` | user | 20 file(s) | 752 | 10 | killed |
| `r1394.P7_unknown_named_as_landed` | `src/cratekit/sync/pair_model.py` | user | 20 file(s) | 752 | 1 | killed |
| `r1394.P8_every_move_named_as_a_stop` | `src/cratekit/sync/pair_model.py` | user | 20 file(s) | 752 | 1 | killed |
| `r1394.P9_finish_not_held_to_the_agreed_reading` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 752 | 2 | killed |
| `r1404.S3_scope_every_pair` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 764 | 13 | killed |
| `r1411.W1_finish_passes_no_agreed` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 752 | 10 | killed |
| `r1411.W2_finish_passes_agreed_only_with_nothing_else` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 752 | 7 | killed |
| `r1411.W3_agreed_is_the_asked_order` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 752 | 10 | killed |
| `r1411.W4_agreed_is_the_checks_listing` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 752 | 2 | killed |
| `r1416.M10_cli_account_write_kept` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 764 | 12 | killed |
| `r1416.M7_cli_tells_kept` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 764 | 4 | killed |
| `r1416.M8_cli_tells_not_kept` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 764 | 2 | killed |
| `r1416.M9_cli_scope_key_only` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 764 | 119 | killed |
| `r1416.S3_scope_under_the_folder` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 764 | 119 | killed |
| `r1418.F1_agreed_is_the_readable_tracks` | `src/cratekit/sync/pair_write.py` | user | 10 file(s) | 394 | 1 | killed |
| `r1418.F2_agreed_passed_for_an_empty_reading` | `src/cratekit/sync/pair_write.py` | maintainer | 10 file(s) | 394 | 1 | killed |
| `r1418.F3_agreed_passed_only_for_an_empty_reading` | `src/cratekit/sync/pair_write.py` | user | 10 file(s) | 394 | 11 | killed |
| `r1418.F4_agreed_only_without_adds_or_removes` | `src/cratekit/sync/pair_write.py` | user | 10 file(s) | 394 | 7 | killed |
| `r1418.F5_plans_reading_without_unread_ids` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 4 | killed |
| `r1420-b.B2_beyond_tail_unread_pinned` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 764 | 1 | killed |
| `r1420.B1_beyond_order_unread` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 764 | 8 | killed |
| `r1420.B3_beyond_removals_asked` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 764 | 3 | killed |
| `r1420.C1_continued_ignored` | `src/cratekit/sync/pair_write.py` | user | 21 file(s) | 764 | 4 | killed |
| `r1420.C3_continued_read_after_the_mark` | `src/cratekit/sync/pair_write.py` | user | 21 file(s) | 764 | 1 | killed |
| `r1420.C4_carried_record_unread` | `src/cratekit/sync/pair_write.py` | user | 21 file(s) | 764 | 2 | killed |
| `r1420.E2_finish_agreed_dropped` | `src/cratekit/sync/pair_write.py` | user | 21 file(s) | 764 | 10 | killed |
| `r1420.N1_fix_reverted` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 764 | 7 | killed |
| `r1420.N2_moves_begun_ignored` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 764 | 4 | killed |
| `r1420.N3_finish_read_too` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 764 | 2 | killed |
| `r1420.N5_order_always_read` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 764 | 6 | killed |
| `r1420.N6_call_site_never_reads_order` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 764 | 8 | killed |
| `r1432-composites.C4_finish_reads_the_listing_unfinished` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 61 | killed |
| `r1432.E1_listed_rule_puts_it_first` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 18 | killed |
| `r1432.P10_warning_says_it_stays` | `src/cratekit/sync/pair_screen.py` | user | 10 file(s) | 394 | 2 | killed |
| `r1432.P3_target_id_no_longer_listed_put_back` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 3 | killed |
| `r1432.P4_target_id_already_held_put_twice` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 8 | killed |
| `r1432.P5_target_placed_by_the_listing` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 11 | killed |
| `r1432.P6_target_behind_the_first_held` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 19 | killed |
| `r1432.P7_none_held_goes_last` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 2 | killed |
| `r1432.P8_placed_in_front_of_its_neighbour` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 22 | killed |
| `r1434.F7_ordering_start_from_the_readable_tracks` | `src/cratekit/sync/pair_write.py` | user | 10 file(s) | 394 | 3 | killed |
| `r1434.M1_write_that_sent_nothing_read_on_its_whole_path` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 2 | killed |
| `r1434.M2_plan_reads_a_write_that_sent_nothing_on_its_whole_path` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 1 | killed |
| `r1434.M3_readable_move_after_a_write_that_sent_nothing_read_on_its_whole_path` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 1 | killed |
| `r1434.M4_hold_promises_the_accounts_order_for_an_unread_move` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 1 | killed |
| `r1434.M5_hold_withholds_the_lead_from_a_readable_reorder` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 1 | killed |
| `r1434.S1_sent_nothing_off_path_waits_for_settled_readings` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 7 | killed |
| `r1434.S3_unread_track_placed_at_the_front` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 22 | killed |
| `r1434.S5_folded_base_keeps_unread_keys` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 4 | killed |
| `r1446-b.C1_composite_no_unread_left_out` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 155 | 6 | killed |
| `r1446-c.F1_every_unread_kept_its_place` | `src/cratekit/sync/pair_plan.py` | user | 5 file(s) | 264 | 2 | killed |
| `r1446-c.F2_no_unread_id_read_as_moved` | `src/cratekit/sync/pair_plan.py` | user | 5 file(s) | 264 | 3 | killed |

## Row definitions

### `r1264.M19_warning`

_warnings: say nothing of the unread tracks

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1264.json`, row `M19_warning`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_an_untitled_track_never_stops_its_pair_and_the_rest_syncs_both_ways`

Old text:

```
    unread = [(one, named) for one in planned.pairs for named in one.unread]
    if unread:
```

New text:

```
    unread = [(one, named) for one in planned.pairs for named in one.unread]
    if False:
```

### `r1264.M1_unread_dropped`

plan_pair: read no unread tracks off the listing, so an untitled track the base holds reads as taken off the account and its linked row is removed from rekordbox

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1264.json`, row `M1_unread_dropped`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_hold.py`
- Collected: 95 against a baseline of 95
- Kills: 17 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_first_sync_never_offers_the_account_an_unread_track_it_already_lists`
  - `tests/test_sync_pair_unread.py::test_a_plan_whose_unread_tracks_differ_digests_differently`
  - `tests/test_sync_pair_unread.py::test_a_rekordbox_reorder_while_a_track_is_unread_reaches_the_account_and_stands`
  - `tests/test_sync_pair_unread.py::test_a_rekordbox_row_carrying_an_unread_tracks_isrc_is_not_added_to_the_account`
  - `tests/test_sync_pair_unread.py::test_a_release_turning_unread_beside_a_readable_one_moves_nothing[listing0-t4]`
  - `tests/test_sync_pair_unread.py::test_a_release_turning_unread_beside_a_readable_one_moves_nothing[listing1-t24]`
  - `tests/test_sync_pair_unread.py::test_a_row_held_only_as_an_unread_release_stays_where_the_account_lists_it`
  - `tests/test_sync_pair_unread.py::test_a_row_read_through_its_second_release_moves_on_the_account_with_rekordbox`
  - `tests/test_sync_pair_unread.py::test_a_row_read_through_its_second_release_removed_in_rekordbox_leaves_the_account`
  - `tests/test_sync_pair_unread.py::test_a_row_whose_listed_release_is_its_unread_second_stays_in_rekordbox`
  - `tests/test_sync_pair_unread.py::test_a_track_naming_no_artist_is_unread_the_same_way`
  - `tests/test_sync_pair_unread.py::test_a_track_synced_across_and_then_removed_in_rekordbox_is_not_put_back`
  - `tests/test_sync_pair_unread.py::test_a_track_synced_across_and_then_removed_on_the_account_is_not_put_back`
  - `tests/test_sync_pair_unread.py::test_an_unread_track_the_twin_holds_is_never_removed_or_added_again`
  - `tests/test_sync_pair_unread.py::test_an_untitled_track_never_stops_its_pair_and_the_rest_syncs_both_ways`
  - ... and 2 more, see the JSON sidecar

Old text:

```
            listing.unread,
            listing.order,
```

New text:

```
            {},
            listing.order,
```

### `r1264.M20_item`

_items: list no unread track among the gate's items

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1264.json`, row `M20_item`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`
- Collected: 20 against a baseline of 20
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_first_sync_never_offers_the_account_an_unread_track_it_already_lists`
  - `tests/test_sync_pair_unread.py::test_a_row_held_only_as_an_unread_release_stays_where_the_account_lists_it`
  - `tests/test_sync_pair_unread.py::test_a_row_read_through_its_second_release_moves_on_the_account_with_rekordbox`
  - `tests/test_sync_pair_unread.py::test_a_row_read_through_its_second_release_removed_in_rekordbox_leaves_the_account`
  - `tests/test_sync_pair_unread.py::test_a_row_whose_listed_release_is_its_unread_second_stays_in_rekordbox`
  - `tests/test_sync_pair_unread.py::test_a_track_naming_no_artist_is_unread_the_same_way`
  - `tests/test_sync_pair_unread.py::test_an_untitled_track_never_stops_its_pair_and_the_rest_syncs_both_ways`

Old text:

```
        items.append(row("account", "unread", named))
```

New text:

```
        pass
```

### `r1264.M2_unread_isrc_on_account`

plan_pair: do not join an unread track's ISRC to the account's codes, so a rekordbox row carrying it asks the provider, which may name another release

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1264.json`, row `M2_unread_isrc_on_account`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_twins.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_rekordbox_row_carrying_an_unread_tracks_isrc_is_not_added_to_the_account`

Old text:

```
        code = match.isrc_token(one.isrc)
        if code:
```

New text:

```
        code = match.isrc_token(one.isrc)
        if False:
```

### `r1264.M3_account_keys_listing_order`

plan_pair: read the account's keys in the readable tracks' order, so a row's key sits at its readable release's place

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1264.json`, row `M3_account_keys_listing_order`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`
- Collected: 117 against a baseline of 117
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_release_turning_unread_beside_a_readable_one_moves_nothing[listing0-t4]`
  - `tests/test_sync_pair_unread.py::test_a_release_turning_unread_beside_a_readable_one_moves_nothing[listing1-t24]`
  - `tests/test_sync_pair_unread.py::test_a_row_read_through_its_second_release_moves_on_the_account_with_rekordbox`

Old text:

```
            for remote_id in (listed_order or account_now)
            if alias(remote_id) in readable_keys
```

New text:

```
            for remote_id in account_now
            if alias(remote_id) in readable_keys
```

### `r1264.M4_account_keys_filter`

plan_pair: keep an unread track's own key among the account's keys, so it reads as held on the account

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1264.json`, row `M4_account_keys_filter`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_pair.py`
- Collected: 96 against a baseline of 96
- Kills: 12 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_plan_whose_unread_tracks_differ_digests_differently`
  - `tests/test_sync_pair_unread.py::test_a_rekordbox_reorder_while_a_track_is_unread_reaches_the_account_and_stands`
  - `tests/test_sync_pair_unread.py::test_a_row_held_only_as_an_unread_release_stays_where_the_account_lists_it`
  - `tests/test_sync_pair_unread.py::test_a_row_read_through_its_second_release_removed_in_rekordbox_leaves_the_account`
  - `tests/test_sync_pair_unread.py::test_a_row_whose_listed_release_is_its_unread_second_stays_in_rekordbox`
  - `tests/test_sync_pair_unread.py::test_a_track_naming_no_artist_is_unread_the_same_way`
  - `tests/test_sync_pair_unread.py::test_a_track_synced_across_and_then_removed_in_rekordbox_is_not_put_back`
  - `tests/test_sync_pair_unread.py::test_a_track_synced_across_and_then_removed_on_the_account_is_not_put_back`
  - `tests/test_sync_pair_unread.py::test_a_track_turning_unreadable_between_the_plan_and_the_write_refuses_stale`
  - `tests/test_sync_pair_unread.py::test_an_untitled_track_never_stops_its_pair_and_the_rest_syncs_both_ways`
  - `tests/test_sync_pair_unread.py::test_unread_tracks_trading_places_after_the_plan_is_not_stale`
  - `tests/test_sync_pair_unread.py::test_while_a_track_is_unread_a_rekordbox_removal_still_lands_on_the_account`

Old text:

```
            for remote_id in (listed_order or account_now)
            if alias(remote_id) in readable_keys
```

New text:

```
            for remote_id in (listed_order or account_now)
            if True
```

### `r1264.M5_unread_keys_empty`

plan_pair: no unread keys, so nothing is stripped from the base or kept from the account's additions

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1264.json`, row `M5_unread_keys_empty`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_twins.py`
- Collected: 66 against a baseline of 66
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_first_sync_never_offers_the_account_an_unread_track_it_already_lists`
  - `tests/test_sync_pair_unread.py::test_a_row_held_only_as_an_unread_release_stays_where_the_account_lists_it`
  - `tests/test_sync_pair_unread.py::test_a_row_whose_listed_release_is_its_unread_second_stays_in_rekordbox`
  - `tests/test_sync_pair_unread.py::test_an_unread_track_the_twin_holds_is_never_removed_or_added_again`

Old text:

```
    unread_keys = {alias(remote_id) for remote_id in unread} - readable_keys
```

New text:

```
    unread_keys: set[str] = set()
```

### `r1264.M6_base_strip`

plan_pair: leave unread keys in the base account, so a row linked to an unread track reads as removed on the account

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1264.json`, row `M6_base_strip`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_twins.py`
- Collected: 66 against a baseline of 66
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_row_held_only_as_an_unread_release_stays_where_the_account_lists_it`
  - `tests/test_sync_pair_unread.py::test_a_row_whose_listed_release_is_its_unread_second_stays_in_rekordbox`
  - `tests/test_sync_pair_unread.py::test_an_unread_track_the_twin_holds_is_never_removed_or_added_again`

Old text:

```
        if unread_keys:
            unseen |=
```

New text:

```
        if False:
            unseen |=
```

### `r1264.M8_order_after_listing`

plan_pair: compute the account order over the readable tracks only

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1264.json`, row `M8_order_after_listing`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`
- Collected: 117 against a baseline of 117
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_release_turning_unread_beside_a_readable_one_moves_nothing[listing0-t4]`
  - `tests/test_sync_pair_unread.py::test_a_release_turning_unread_beside_a_readable_one_moves_nothing[listing1-t24]`
  - `tests/test_sync_pair_unread.py::test_a_row_read_through_its_second_release_moves_on_the_account_with_rekordbox`

Old text:

```
        after = pair_merge.appended(listed_order or account_now, account_removes, account_adds)
```

New text:

```
        after = pair_merge.appended(account_now, account_removes, account_adds)
```

### `r1264.M9_firsts_keep_unread`

plan_pair: count unread keys among the account's order keys, so the order differs from the merge's whenever one is unread

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1264.json`, row `M9_firsts_keep_unread`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_pair.py`
- Collected: 96 against a baseline of 96
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_row_held_only_as_an_unread_release_stays_where_the_account_lists_it`
  - `tests/test_sync_pair_unread.py::test_a_row_whose_listed_release_is_its_unread_second_stays_in_rekordbox`

Old text:

```
            alias(one) for one in after if alias(one) not in unread_keys
```

New text:

```
            alias(one) for one in after
```

### `r1372.K17_no_let_go_at_snapshot`

_record: a snapshot recorded whole lets go of no carried record of its pair

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1372.json`, row `K17_no_let_go_at_snapshot`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_whose_pair_a_later_sync_finished_is_let_go`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_after_its_steps_were_pruned_never_takes_the_scramble`

Old text:

```
    if whole:
        _let_go_passed(one.target.account_id, recorded.synced)
```

New text:

```
    if False:
        _let_go_passed(one.target.account_id, recorded.synced)
```

### `r1372.K1_no_carry`

write: the pair's steps are not carried past the run as its order begins

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1372.json`, row `K1_no_carry`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 9 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_whose_steps_cannot_be_read_still_agrees_with_the_checks_listing_first[gone]`
  - `tests/test_sync_pair_order.py::test_a_continue_whose_steps_cannot_be_read_still_agrees_with_the_checks_listing_first[unreadable]`
  - `tests/test_sync_pair_stopped_order.py::test_a_continue_of_the_stopped_run_after_its_plan_aged_out_still_finishes_it`
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_that_cannot_be_read_is_named`
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_the_snapshot_passed_is_read_as_no_write_even_when_still_on_disk`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_after_its_steps_were_pruned_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_run_that_finished_the_pair_without_moving_its_snapshot_keeps_nothing_of_its_own`
  - `tests/test_sync_pair_stopped_order.py::test_a_stop_older_than_a_held_plan_is_kept_is_still_finished_from_the_side_that_led`
  - `tests/test_sync_pair_stopped_order.py::test_a_stop_whose_held_plan_and_steps_were_pruned_is_still_finished`

Old text:

```
        # whatever its age until the pair's snapshot passes it.
        steps.carry()
```

New text:

```
        # whatever its age until the pair's snapshot passes it.
        pass
```

### `r1372.K22_mark_guard_gone`

stopped_write: a stop that began before the pair was marked is read as the pair's

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1372.json`, row `K22_mark_guard_gone`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_first_sync_reads_the_stop_on_its_account_playlist_whatever_the_mark`
  - `tests/test_sync_pair_stopped.py::test_a_stop_from_before_the_pair_was_marked_again_is_not_its_stop`

Old text:

```
        if marked is not None and began < marked:
            return None
```

New text:

```
        if False:
            return None
```

### `r1372.K23_mark_guard_inclusive`

stopped_write: a stop that began at the very moment the pair was marked is refused

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1372.json`, row `K23_mark_guard_inclusive`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_stop_from_before_the_pair_was_marked_again_is_not_its_stop`

Old text:

```
        if marked is not None and began < marked:
```

New text:

```
        if marked is not None and began <= marked:
```

### `r1372.K4_carry_unwritten_not_refused`

PairSteps.carry: a carry that cannot be written is swallowed and the moves go on

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1372.json`, row `K4_carry_unwritten_not_refused`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_stop_that_cannot_be_kept_past_its_run_moves_nothing`

Old text:

```
            held_plan.carry(self.steps, self.key)
        except OSError as exc:
            raise steps_unwritten(self.steps.run_id, exc) from None
```

New text:

```
            held_plan.carry(self.steps, self.key)
        except OSError as exc:
            exc = exc
```

### `r1372.K6_reader_ignores_carried`

reader: the carried records are not read, only the kept steps

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1372.json`, row `K6_reader_ignores_carried`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_stop_in_the_middle_of_an_order_sends_no_move_again_and_a_later_sync_finishes_it`
  - `tests/test_sync_pair_stopped.py::test_a_carried_copy_gives_way_to_its_own_runs_steps_kept_under_the_same_plan`
  - `tests/test_sync_pair_stopped_order.py::test_a_continue_of_the_stopped_run_after_its_plan_aged_out_still_finishes_it`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_after_its_steps_were_pruned_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_over_a_pending_order_is_held_until_the_provider_serves_it`
  - `tests/test_sync_pair_stopped_order.py::test_a_stop_older_than_a_held_plan_is_kept_is_still_finished_from_the_side_that_led`
  - `tests/test_sync_pair_stopped_order.py::test_a_stop_whose_held_plan_and_steps_were_pruned_is_still_finished`

Old text:

```
        records = [*records, *(one for one in kept if (one.run_id, one.digest) not in current)]
```

New text:

```
        records = [*records]
```

### `r1372.K7_copy_never_gives_way`

reader: a carried copy is read beside its own run's steps kept under the same plan

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1372.json`, row `K7_copy_never_gives_way`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_carried_copy_gives_way_to_its_own_runs_steps_kept_under_the_same_plan`

Old text:

```
        current = {(one.run_id, one.digest) for one in records}
```

New text:

```
        current = set()
```

### `r1372.K8_copy_gives_way_to_any_plan`

reader: a carried copy gives way to its run's steps under any plan, so a replanned run's fresh steps hide it

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1372.json`, row `K8_copy_gives_way_to_any_plan`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_carried_copy_gives_way_to_its_own_runs_steps_kept_under_the_same_plan`

Old text:

```
        current = {(one.run_id, one.digest) for one in records}
        records = [*records, *(one for one in kept if (one.run_id, one.digest) not in current)]
```

New text:

```
        current = {one.run_id for one in records}
        records = [*records, *(one for one in kept if one.run_id not in current)]
```

### `r1372.K9_carried_unread_unsaid`

reader: a carried record that cannot be read is not named

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1372.json`, row `K9_carried_unread_unsaid`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_that_cannot_be_read_is_named`

Old text:

```
        problems = [*problems, *unread]
```

New text:

```
        problems = [*problems]
```

### `r1376.F11_leader_lost`

plan_pair: the stop is read as led by the account whatever side led it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1376.json`, row `F11_leader_lost`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_pair_released_after_a_stop_and_paired_again_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_at_the_root_never_takes_the_scramble_on_its_first_sync`
  - `tests/test_sync_pair_stopped_order.py::test_the_gate_names_the_pair_as_finishing_the_stopped_run`
  - `tests/test_sync_pair_stopped_order.py::test_the_gate_says_the_account_was_read_off_the_moves_path`

Old text:

```
            leader=stopped_write.leader,
```

New text:

```
            leader=pair_merge.ACCOUNT,
```

### `r1376.F13_snapshot_guard_inclusive`

stopped_write (sample, U225): a stop that began after the snapshot by a hair is read as passed

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1376.json`, row `F13_snapshot_guard_inclusive`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 34 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_stop_in_the_middle_of_an_order_sends_no_move_again_and_a_later_sync_finishes_it`
  - `tests/test_sync_pair_stopped.py::test_a_stop_from_before_the_pair_was_marked_again_is_not_its_stop`
  - `tests/test_sync_pair_stopped_order.py::test_a_continue_of_the_stopped_run_after_its_plan_aged_out_still_finishes_it`
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_that_moves_again_before_it_settles_is_held_again`
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_waits_the_agreement_window`
  - `tests/test_sync_pair_stopped_order.py::test_a_fresh_sync_orders_the_account_to_rekordbox_and_plans_no_rekordbox_order`
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_reading_that_never_settled_shows_no_reorder`
  - `tests/test_sync_pair_stopped_order.py::test_a_later_reading_still_on_the_moves_path_is_finished_never_read_as_a_reorder`
  - `tests/test_sync_pair_stopped_order.py::test_a_later_run_that_failed_before_its_order_began_does_not_hide_the_stopped_write`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_off_the_path_no_sync_read_before_is_not_read_as_the_persons`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_the_person_made_on_the_account_after_a_sync_read_it_still_leads`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_kept_before_the_stop_shows_no_reorder`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_kept_for_another_run_shows_no_reorder`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_on_the_path_is_never_the_baseline_so_the_partial_state_after_it_finishes`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_that_moved_before_it_settled_starts_again`
  - ... and 19 more, see the JSON sidecar

Old text:

```
            if synced is None or not began > synced:
```

New text:

```
            if synced is None or True:
```

### `r1376.F1_first_stop_none`

first_stop: a first sync is never handed the stop on its account playlist

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1376.json`, row `F1_first_stop_none`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_first_sync_reads_the_stop_on_its_account_playlist_whatever_the_mark`
  - `tests/test_sync_pair_stopped_order.py::test_a_first_sync_whose_account_side_was_skipped_still_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_pair_released_after_a_stop_and_paired_again_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_after_its_steps_were_pruned_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_at_the_root_never_takes_the_scramble_on_its_first_sync`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_over_a_pending_order_is_held_until_the_provider_serves_it`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_read_off_the_path_on_its_first_sync_keeps_rekordboxs_order`

Old text:

```
        _began, write = self.stopped[0].get(account_id, (None, None))
        return write
```

New text:

```
        _began, write = self.stopped[0].get(account_id, (None, None))
        return None
```

### `r1376.F3_call_site_gone`

plan_pair: a first sync never asks for the stop on its account playlist

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1376.json`, row `F3_call_site_gone`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_first_sync_whose_account_side_was_skipped_still_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_pair_released_after_a_stop_and_paired_again_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_after_its_steps_were_pruned_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_at_the_root_never_takes_the_scramble_on_its_first_sync`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_over_a_pending_order_is_held_until_the_provider_serves_it`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_read_off_the_path_on_its_first_sync_keeps_rekordboxs_order`

Old text:

```
    if stopped_write is None and first_sync:
        stopped_write = reader.first_stop(target.account_id)
```

New text:

```
    if False:
        stopped_write = reader.first_stop(target.account_id)
```

### `r1376.F4_first_sync_unrecorded_only`

plan_pair: a pair marked with no snapshot is not read as a first sync, so its earlier stop is kept out by the mark

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1376.json`, row `F4_first_sync_unrecorded_only`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_first_sync_whose_account_side_was_skipped_still_never_takes_the_scramble`

Old text:

```
    first_sync = held is None or held.first
```

New text:

```
    first_sync = held is None
```

### `r1376.F5_first_sync_marked_only`

plan_pair: a pair with no record at all, a hand pairing before its mark, is not read as a first sync

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1376.json`, row `F5_first_sync_marked_only`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 318 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_a_rekordbox_running_refusal_still_ends_the_run_as_failed`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`
  - `tests/test_sync_pair.py::test_a_first_sync_with_a_side_skipped_records_no_snapshot_and_stays_first`
  - `tests/test_sync_pair.py::test_a_job_naming_no_playlist_is_named_by_its_account_playlist`
  - `tests/test_sync_pair.py::test_a_landed_track_is_found_in_the_inbox_playlist_landed_for_the_account`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[cache-off]`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[kept]`
  - `tests/test_sync_pair.py::test_a_pair_whose_playlist_is_gone_does_not_hold_every_other_pair`
  - `tests/test_sync_pair.py::test_a_plan_with_every_landing_record_readable_warns_nothing_of_them`
  - `tests/test_sync_pair.py::test_a_rekordbox_change_between_the_gates_and_the_write_refuses_as_stale`
  - `tests/test_sync_pair.py::test_a_rekordbox_row_with_no_isrc_column_is_matched_on_its_files_isrc`
  - `tests/test_sync_pair.py::test_a_row_with_no_isrc_anywhere_is_named_and_the_provider_is_not_asked`
  - `tests/test_sync_pair.py::test_a_second_rekordbox_playlist_for_a_paired_account_playlist_is_refused`
  - `tests/test_sync_pair.py::test_a_session_log_that_cannot_be_listed_holds_the_track`
  - ... and 303 more, see the JSON sidecar

Old text:

```
    first_sync = held is None or held.first
```

New text:

```
    first_sync = held is not None and held.first
```

### `r1376.F6_every_sync_first`

plan_pair: every sync reads the stop whatever its snapshot, so a stop the snapshot passed is finished again

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1376.json`, row `F6_every_sync_first`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_the_snapshot_passed_is_read_as_no_write_even_when_still_on_disk`
  - `tests/test_sync_pair_stopped_order.py::test_a_pair_released_after_a_stop_and_paired_again_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_stopped_write_a_fresh_sync_finished_is_left_behind_by_the_snapshot`
  - `tests/test_sync_pair_stopped_order.py::test_a_stopped_write_its_continue_holds_is_finished_by_the_next_sync_and_leaves_nothing`

Old text:

```
    if stopped_write is None and first_sync:
```

New text:

```
    if stopped_write is None:
```

### `r1383-digest.M8_digest_drops_hold`

PairPlan.identity: leave the held tracks out of the digest, so a plan whose hold moved is not stale at its gate

- File: `src/cratekit/sync/pair_model.py`
- Source: `r1383-digest.json`, row `M8_digest_drops_hold`
- Moved: the same text, now in src/cratekit/sync/pair_model.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`
- Collected: 162 against a baseline of 162
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_the_pairs_digest_moves_with_the_landing_hold_and_only_when_any`

Old text:

```
                {"landing_unread": sorted(named.remote_id for named in self.landing_unread)}
                if self.landing_unread
                else {}
```

New text:

```
                {}
```

### `r1383-digest.M9_digest_always_keyed`

PairPlan.identity: put the key in every digest, so a plan reading every record no longer digests as it did (round one's zero)

- File: `src/cratekit/sync/pair_model.py`
- Source: `r1383-digest.json`, row `M9_digest_always_keyed`
- Moved: the same text, now in src/cratekit/sync/pair_model.py, was in src/cratekit/sync/pair_cli.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`
- Collected: 162 against a baseline of 162
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_the_pairs_digest_moves_with_the_landing_hold_and_only_when_any`

Old text:

```
                if self.landing_unread
                else {}
```

New text:

```
                if True
                else {}
```

### `r1383.M10_warning_never_said`

plan: carry no unread entry to the warning, so the hold is silent

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1383.json`, row `M10_warning_never_said`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_hold.py`
- Collected: 137 against a baseline of 137
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_session_log_that_cannot_be_listed_holds_the_track`
  - `tests/test_sync_pair.py::test_a_track_an_earlier_sync_queued_is_awaiting_beside_an_unreadable_record`
  - `tests/test_sync_pair.py::test_a_track_no_landing_brought_in_is_held_while_a_record_is_unread`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[torn]`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[unknown-state]`

Old text:

```
                _landings_said(cfg, reader.landings[1]) if "landings" in reader.__dict__ else ()
```

New text:

```
                ()
```

### `r1383.M12_unlisted_said_as_records`

_landings_said: never say the log is unlisted, so a refused listing is named as a record to repair

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1383.json`, row `M12_unlisted_said_as_records`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_session_log_that_cannot_be_listed_holds_the_track`

Old text:

```
    if session.log_unlisted(unread, cfg):
        return (
```

New text:

```
    if False:
        return (
```

### `r1383.M13_records_unnamed`

_landings_said: name no record, so the warning cannot say which record to look at

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1383.json`, row `M13_records_unnamed`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 76 against a baseline of 76
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[torn]`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[unknown-state]`

Old text:

```
        f"the record {Path(path).name} in {Path(path).parent}, which reads under the "
```

New text:

```
        f"a record in {Path(path).parent}, which reads under the "
```

### `r1383.M14_hold_before_awaiting`

plan_pair: decide the landing hold before awaiting, so a track an earlier sync queued is shown held with the wrong remedy

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1383.json`, row `M14_hold_before_awaiting`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_hold.py`
- Collected: 137 against a baseline of 137
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_track_an_earlier_sync_queued_is_awaiting_beside_an_unreadable_record`
  - `tests/test_sync_twins_hold.py::test_a_twins_held_track_stays_on_hold_beside_an_unreadable_landing_record`

Old text:

```
        if remote_id in queued_before:
            awaiting.append(names[key])
```

New text:

```
        if match.isrc_token((tracks.get(remote_id) or {}).get("isrc")) and reader.landings[1]:
            landing_unread.append(names[key])
        elif remote_id in queued_before:
            awaiting.append(names[key])
```

### `r1383.M15_hold_before_twin`

plan_pair: decide the landing hold before a twin's hold, so a twin's held track loses its sync release remedy

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1383.json`, row `M15_hold_before_twin`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_hold.py`
- Collected: 137 against a baseline of 137
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_a_twins_held_track_stays_on_hold_beside_an_unreadable_landing_record`

Old text:

```
        elif held_for_choice(held, remote_id, dates):
```

New text:

```
        elif match.isrc_token((tracks.get(remote_id) or {}).get("isrc")) and reader.landings[1]:
            landing_unread.append(names[key])
        elif held_for_choice(held, remote_id, dates):
```

### `r1383.M16_zero_said_as_count`

_warnings: say a scan nothing waited on as zero tracks held, round one's finding 7

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1383.json`, row `M16_zero_said_as_count`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_track_an_earlier_sync_queued_is_awaiting_beside_an_unreadable_record`

Old text:

```
                        if waiting
                        # THE SCAN
```

New text:

```
                        if True
                        # THE SCAN
```

### `r1383.M17_total_uncounted`

payload: count no held track in the totals

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1383.json`, row `M17_total_uncounted`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`
- Collected: 108 against a baseline of 108
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[torn]`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[unknown-state]`

Old text:

```
            "landing_unread": count("library", LANDING_UNREAD_ACTION),
```

New text:

```
            "landing_unread": 0,
```

### `r1383.M18_sampled_own_landed_step`

sampled U128 guard: _owned asks no landing made for this account playlist, so its own landed track is found only by the widened step

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1383.json`, row `M18_sampled_own_landed_step`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_hold.py`
- Collected: 137 against a baseline of 137
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_this_account_playlists_own_landing_wins_over_anothers`

Old text:

```
        landed = _mirror_isrcs(reader, account_id)
```

New text:

```
        landed = {}
```

### `r1383.M19_sampled_mirrors_empty`

sampled: _Reader.mirrors answers no INBOX playlist, so every landed track is queued again, the half R-1383 keeps beside it

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1383.json`, row `M19_sampled_mirrors_empty`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_hold.py`
- Collected: 137 against a baseline of 137
- Kills: 11 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_landed_track_is_found_in_the_inbox_playlist_landed_for_the_account`
  - `tests/test_sync_pair.py::test_a_track_an_earlier_sync_queued_is_awaiting_beside_an_unreadable_record`
  - `tests/test_sync_pair.py::test_a_track_another_account_playlist_landed_is_added_and_never_queued`
  - `tests/test_sync_pair.py::test_each_landed_file_is_read_once_per_plan`
  - `tests/test_sync_pair.py::test_one_row_landed_in_two_inbox_playlists_is_one_row`
  - `tests/test_sync_pair.py::test_the_same_plan_with_the_record_readable_adds_the_row[torn]`
  - `tests/test_sync_pair.py::test_the_same_plan_with_the_record_readable_adds_the_row[unknown-state]`
  - `tests/test_sync_pair.py::test_this_account_playlists_own_landing_wins_over_anothers`
  - `tests/test_sync_pair.py::test_two_landed_rows_carrying_the_code_are_ambiguous_and_queue_nothing`
  - `tests/test_sync_pair_hold.py::test_a_track_found_by_another_landing_costs_the_plan_no_call[by another account playlist's landing]`
  - `tests/test_sync_twins_hold.py::test_a_held_track_another_account_playlist_landed_is_added_and_the_rest_stay_held`

Old text:

```
        return self.landings[0]
```

New text:

```
        return {}
```

### `r1383.M1_scan_drops_unread`

landed_inbox_playlists: answer no unread entry, the defect the card closes, so an unreadable landing record is read as no landing and its track queued

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1383.json`, row `M1_scan_drops_unread`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_hold.py`
- Collected: 183 against a baseline of 183
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_session_log_that_cannot_be_listed_holds_the_track`
  - `tests/test_sync_pair.py::test_a_track_an_earlier_sync_queued_is_awaiting_beside_an_unreadable_record`
  - `tests/test_sync_pair.py::test_a_track_no_landing_brought_in_is_held_while_a_record_is_unread`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[torn]`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[unknown-state]`

Old text:

```
    return {account_id: frozenset(ids) for account_id, ids in found.items()}, tuple(unreadable)
```

New text:

```
    return {account_id: frozenset(ids) for account_id, ids in found.items()}, ()
```

### `r1383.M2_hold_branch_removed`

plan_pair: never hold, so a track an unreadable landing record may have brought in is queued with the warning beside it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1383.json`, row `M2_hold_branch_removed`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_hold.py`
- Collected: 137 against a baseline of 137
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_session_log_that_cannot_be_listed_holds_the_track`
  - `tests/test_sync_pair.py::test_a_track_no_landing_brought_in_is_held_while_a_record_is_unread`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[torn]`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[unknown-state]`

Old text:

```
            match.isrc_token((tracks.get(remote_id) or {}).get("isrc")) and reader.landings[1]
        ):
```

New text:

```
            False
        ):
```

### `r1383.M3_hold_without_isrc`

plan_pair: hold a track carrying no ISRC as well, so a track no landing could name waits on the record forever

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1383.json`, row `M3_hold_without_isrc`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_hold.py`
- Collected: 137 against a baseline of 137
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_track_carrying_no_isrc_is_still_queued_beside_an_unreadable_record`

Old text:

```
            match.isrc_token((tracks.get(remote_id) or {}).get("isrc")) and reader.landings[1]
        ):
```

New text:

```
            reader.landings[1]
        ):
```

### `r1383.M4_hold_while_readable`

plan_pair: hold whenever the track carries an ISRC, so every new track waits though every record reads

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1383.json`, row `M4_hold_while_readable`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_hold.py`
- Collected: 137 against a baseline of 137
- Kills: 27 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_job_naming_no_playlist_is_named_by_its_account_playlist`
  - `tests/test_sync_pair.py::test_a_plan_with_every_landing_record_readable_warns_nothing_of_them`
  - `tests/test_sync_pair.py::test_a_track_an_earlier_sync_queued_is_awaiting_beside_an_unreadable_record`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[blocked]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[queued]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[running]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[succeeded]`
  - `tests/test_sync_pair.py::test_a_track_no_landing_brought_in_is_still_queued`
  - `tests/test_sync_pair.py::test_a_track_only_a_failed_or_cancelled_job_held_is_queued[cancelled]`
  - `tests/test_sync_pair.py::test_a_track_only_a_failed_or_cancelled_job_held_is_queued[failed]`
  - `tests/test_sync_pair.py::test_a_track_this_pair_alone_lists_is_queued_once_beside_anothers_job`
  - `tests/test_sync_pair.py::test_an_account_track_the_library_lacks_is_queued_once_and_never_written_as_a_row`
  - `tests/test_sync_pair.py::test_another_pairs_job_queued_since_the_plan_refuses_the_write_as_stale`
  - `tests/test_sync_pair.py::test_another_pairs_job_that_no_longer_reads_stops_no_plan`
  - `tests/test_sync_pair.py::test_skipping_the_first_pairs_rekordbox_side_says_nothing_was_queued`
  - ... and 12 more, see the JSON sidecar

Old text:

```
            match.isrc_token((tracks.get(remote_id) or {}).get("isrc")) and reader.landings[1]
        ):
```

New text:

```
            match.isrc_token((tracks.get(remote_id) or {}).get("isrc"))
        ):
```

### `r1383.M5_hold_dropped_from_plan`

plan_pair: build the pair with no held tracks, so the gate names none and the total counts none

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1383.json`, row `M5_hold_dropped_from_plan`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_hold.py`
- Collected: 137 against a baseline of 137
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[torn]`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[unknown-state]`

Old text:

```
        landing_unread=tuple(landing_unread),
```

New text:

```
        landing_unread=(),
```

### `r1383.M6_gate_item_dropped`

_items: name no held track on the gate, so a person approving sees nothing of what waits

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1383.json`, row `M6_gate_item_dropped`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_hold.py`
- Collected: 137 against a baseline of 137
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[torn]`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[unknown-state]`

Old text:

```
    for named in one.landing_unread:
        items.append(row("library", LANDING_UNREAD_ACTION, named))
```

New text:

```
    for named in ():
        items.append(row("library", LANDING_UNREAD_ACTION, named))
```

### `r1383.M7_gate_item_side`

_items: name a held track on the rekordbox side rather than the library's

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1383.json`, row `M7_gate_item_side`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`
- Collected: 108 against a baseline of 108
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[torn]`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[unknown-state]`

Old text:

```
        items.append(row("library", LANDING_UNREAD_ACTION, named))
```

New text:

```
        items.append(row("rekordbox", LANDING_UNREAD_ACTION, named))
```

### `r1385.M10_reason_dropped`

plan_pair: name a track another pair holds awaiting with no reason, so the gate never says which pair holds it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1385.json`, row `M10_reason_dropped`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_job_naming_no_playlist_is_named_by_its_account_playlist`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[blocked]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[queued]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[running]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[succeeded]`
  - `tests/test_sync_pair.py::test_skipping_the_first_pairs_rekordbox_side_says_nothing_was_queued`
  - `tests/test_sync_pair.py::test_two_pairs_listing_one_lacking_track_queue_it_once`

Old text:

```
            awaiting.append(_with_reason(names[key], why))
```

New text:

```
            awaiting.append(names[key])
```

### `r1385.M11_name_fallback`

_Reader.held_by_jobs: no fallback to the account playlist for a job naming no playlist, so its reason names nothing

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1385.json`, row `M11_name_fallback`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_job_naming_no_playlist_is_named_by_its_account_playlist`

Old text:

```
            name = str(payload.get(intake_cli.PLAYLIST_NAME) or "") or source
```

New text:

```
            name = str(payload.get(intake_cli.PLAYLIST_NAME) or "")
```

### `r1385.M12_check_reads_no_job`

check: read no job at apply time, so a job another sync queued since the plan is queued again beside it

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1385.json`, row `M12_check_reads_no_job`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_another_pairs_job_queued_since_the_plan_refuses_the_write_as_stale`
  - `tests/test_sync_pair_hold.py::test_tracks_another_sync_queued_before_the_write_refuse_stale_not_twice`

Old text:

```
            for job in pair_jobs(cfg, store)
            for item in (job.payload or {}).get(intake_cli.TRACKS) or {}
        }
```

New text:

```
            for job in ()
            for item in (job.payload or {}).get(intake_cli.TRACKS) or {}
        }
```

### `r1385.M13_warning_unsplit`

_warnings: say every awaited track was queued, so a skip that queued nothing is reported as queued (round one's finding)

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1385.json`, row `M13_warning_unsplit`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_skipping_the_first_pairs_rekordbox_side_says_nothing_was_queued`

Old text:

```
        before = [row for row in awaiting if not row.reason.startswith(QUEUED_HERE)]
```

New text:

```
        before = awaiting
```

### `r1385.M14_warning_here_dropped`

_warnings: never say a track another pair of this sync is to queue

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1385.json`, row `M14_warning_here_dropped`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_skipping_the_first_pairs_rekordbox_side_says_nothing_was_queued`
  - `tests/test_sync_pair.py::test_two_pairs_listing_one_lacking_track_queue_it_once`

Old text:

```
        if here:
            parts.append(
```

New text:

```
        if False:
            parts.append(
```

### `r1385.M15_failed_jobs_hold`

pair_jobs: read a failed or cancelled job as holding its tracks, so a track whose download failed is never queued again (sampled guard)

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1385.json`, row `M15_failed_jobs_hold`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_track_only_a_failed_or_cancelled_job_held_is_queued[cancelled]`
  - `tests/test_sync_pair.py::test_a_track_only_a_failed_or_cancelled_job_held_is_queued[failed]`

Old text:

```
        and job.state not in (jobs.JobState.FAILED, jobs.JobState.CANCELLED)
    )
```

New text:

```
    )
```

### `r1385.M1_no_job_holds_anything`

_Reader.held_by_jobs: read no job's tracks, so every track a job holds is queued again, a pair's own included

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1385.json`, row `M1_no_job_holds_anything`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 13 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_job_naming_no_playlist_is_named_by_its_account_playlist`
  - `tests/test_sync_pair.py::test_a_track_an_earlier_sync_queued_is_awaiting_beside_an_unreadable_record`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[blocked]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[queued]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[running]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[succeeded]`
  - `tests/test_sync_pair.py::test_an_account_track_the_library_lacks_is_queued_once_and_never_written_as_a_row`
  - `tests/test_sync_pair.py::test_two_pairs_listing_one_lacking_track_queue_it_once`
  - `tests/test_sync_pair_back.py::test_a_missing_track_is_queued_once_and_then_awaits`
  - `tests/test_sync_pair_discover.py::test_an_unowned_track_added_on_the_account_is_queued_once_and_then_awaiting`
  - `tests/test_sync_twins.py::test_a_backfilled_pair_merges_both_ways_and_queues_the_added_track_once`
  - `tests/test_sync_twins_hold.py::test_a_track_an_earlier_sync_queued_is_awaiting_not_on_hold`
  - `tests/test_sync_twins_hold.py::test_a_twins_held_track_another_pairs_job_holds_is_still_held`

Old text:

```
        return {remote_id: tuple(held) for remote_id, held in found.items()}
```

New text:

```
        return {}
```

### `r1385.M2_other_jobs_not_asked`

_queued_elsewhere: ask no other pair's job, so a track another pair's pending job holds is queued again (the card's second scenario)

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1385.json`, row `M2_other_jobs_not_asked`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_job_naming_no_playlist_is_named_by_its_account_playlist`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[blocked]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[queued]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[running]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[succeeded]`
  - `tests/test_sync_pair.py::test_two_pairs_listing_one_lacking_track_queue_it_once`

Old text:

```
    for source, name in reader.held_by_jobs.get(remote_id, ()):
```

New text:

```
    for source, name in ():
```

### `r1385.M4_plan_not_asked`

_queued_elsewhere: ask nothing of this plan, so two pairs listing one lacking track queue it twice (the card's first scenario)

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1385.json`, row `M4_plan_not_asked`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_skipping_the_first_pairs_rekordbox_side_says_nothing_was_queued`
  - `tests/test_sync_pair.py::test_the_runs_own_job_for_an_earlier_pair_stops_no_later_command`
  - `tests/test_sync_pair.py::test_two_pairs_listing_one_lacking_track_queue_it_once`

Old text:

```
    asked = reader.asked.get(remote_id)
```

New text:

```
    asked = None
```

### `r1385.M6_ask_not_registered`

plan_pair: register nothing this pair asks to acquire, so a later pair of the plan queues it again

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1385.json`, row `M6_ask_not_registered`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_skipping_the_first_pairs_rekordbox_side_says_nothing_was_queued`
  - `tests/test_sync_pair.py::test_the_runs_own_job_for_an_earlier_pair_stops_no_later_command`
  - `tests/test_sync_pair.py::test_two_pairs_listing_one_lacking_track_queue_it_once`

Old text:

```
        reader.asked.setdefault(remote_id, (target.key, name))
```

New text:

```
        pass
```

### `r1385.M8_own_reads_every_job`

_queued: read every pair's job as this pair's own, so another pair's job is named with no pair and asked before a twin's hold

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1385.json`, row `M8_own_reads_every_job`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_job_naming_no_playlist_is_named_by_its_account_playlist`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[blocked]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[queued]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[running]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[succeeded]`
  - `tests/test_sync_twins_hold.py::test_a_twins_held_track_another_pairs_job_holds_is_still_held`

Old text:

```
        if any(source == account_id for source, _name in held)
```

New text:

```
        if held
```

### `r1385.M9_own_reads_no_job`

_queued: read none of this pair's own jobs, so its own queued track is named for no pair or held on a twin

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1385.json`, row `M9_own_reads_no_job`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_track_an_earlier_sync_queued_is_awaiting_beside_an_unreadable_record`
  - `tests/test_sync_pair.py::test_an_account_track_the_library_lacks_is_queued_once_and_never_written_as_a_row`
  - `tests/test_sync_pair.py::test_two_pairs_listing_one_lacking_track_queue_it_once`
  - `tests/test_sync_pair_back.py::test_a_missing_track_is_queued_once_and_then_awaits`
  - `tests/test_sync_pair_discover.py::test_an_unowned_track_added_on_the_account_is_queued_once_and_then_awaiting`
  - `tests/test_sync_twins.py::test_a_backfilled_pair_merges_both_ways_and_queues_the_added_track_once`
  - `tests/test_sync_twins_hold.py::test_a_track_an_earlier_sync_queued_is_awaiting_not_on_hold`
  - `tests/test_sync_twins_hold.py::test_a_twins_held_track_another_pairs_job_holds_is_still_held`

Old text:

```
        if any(source == account_id for source, _name in held)
```

New text:

```
        if False
```

### `r1394.P1_counts_never_written`

pair write: the recorder writes the moving step with no progress, sent and landed always 0

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1394.json`, row `P1_counts_never_written`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_the_adapter_refuses_leaves_the_stopped_write_pending`
  - `tests/test_sync_pair_settle.py::test_a_move_whose_fate_is_unknown_holds_the_order_before_it_and_finishes_the_one_after`
  - `tests/test_sync_pair_settle.py::test_a_stop_after_one_of_three_moves_read_as_the_old_order_is_held_however_long_it_agrees`
  - `tests/test_sync_pair_settle.py::test_a_stopped_writes_counts_are_carried_past_its_runs_steps`

Old text:

```
                        at=at, start=start, end=end, sent=sent, landed=landed
```

New text:

```
                        at=at, start=start, end=end, sent=0, landed=0
```

### `r1394.P2_counts_not_carried`

pair write: the recorder's counts are marked in the run's steps but not carried past the run

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1394.json`, row `P2_counts_not_carried`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_stopped_writes_counts_are_carried_past_its_runs_steps`

Old text:

```
                steps.carry()

            return sending
```

New text:

```
                pass

            return sending
```

### `r1394.P3_begun_answers_no_recorder`

pair write: begun answers no recorder, so the adapter tells the record nothing between moves

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1394.json`, row `P3_begun_answers_no_recorder`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_the_adapter_refuses_leaves_the_stopped_write_pending`
  - `tests/test_sync_pair_settle.py::test_a_move_whose_fate_is_unknown_holds_the_order_before_it_and_finishes_the_one_after`
  - `tests/test_sync_pair_settle.py::test_a_pending_stop_agreed_off_its_path_is_finished_from_rekordbox`
  - `tests/test_sync_pair_settle.py::test_a_stop_after_one_of_three_moves_read_as_the_old_order_is_held_however_long_it_agrees`
  - `tests/test_sync_pair_settle.py::test_a_stopped_writes_counts_are_carried_past_its_runs_steps`

Old text:

```
            return sending
```

New text:

```
            return None
```

### `r1394.P4_finish_from_landed`

pending order: an agreed reading at the moves the provider accepted is finished from even with a move whose landing is not known after it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1394.json`, row `P4_finish_from_landed`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_move_whose_fate_is_unknown_holds_the_order_before_it_and_finishes_the_one_after`
  - `tests/test_sync_pair_settle.py::test_a_stopped_write_recorded_with_no_counts_is_finished_only_from_the_order_it_leaves`

Old text:

```
        if not at or max(at) >= write.sent:
```

New text:

```
        if not at or max(at) >= write.landed:
```

### `r1394.P5_finish_from_any_path_reading`

pending order: any agreed reading on the moves' path is finished from, R-1394's own defect

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1394.json`, row `P5_finish_from_any_path_reading`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_the_adapter_refuses_leaves_the_stopped_write_pending`
  - `tests/test_sync_pair_settle.py::test_a_move_whose_fate_is_unknown_holds_the_order_before_it_and_finishes_the_one_after`
  - `tests/test_sync_pair_settle.py::test_a_stop_after_one_of_three_moves_read_as_the_old_order_is_held_however_long_it_agrees`
  - `tests/test_sync_pair_settle.py::test_a_stopped_write_recorded_with_no_counts_is_finished_only_from_the_order_it_leaves`
  - `tests/test_sync_pair_settle.py::test_a_stopped_writes_counts_are_carried_past_its_runs_steps`
  - `tests/test_sync_pair_settle.py::test_every_move_accepted_and_an_agreed_reading_short_of_their_end_is_still_a_lag`

Old text:

```
        if not at or max(at) >= write.sent:
```

New text:

```
        if not at or max(at) >= 0:
```

### `r1394.P6_off_path_held`

pending order: an agreed reading off the moves' path, the person's change, is held instead of merged as theirs

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1394.json`, row `P6_off_path_held`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_hand_move_of_the_unread_track_read_first_after_the_stop_is_finished_by_the_target`
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_agreed_once_off_the_path_keeps_rekordboxs_order`
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_the_person_reordered_after_a_sync_read_it_is_merged_as_their_change`
  - `tests/test_sync_pair_settle.py::test_a_pending_stop_agreed_off_its_path_is_finished_from_rekordbox`
  - `tests/test_sync_pair_settle.py::test_a_reorder_settled_readings_show_keeps_the_unread_track_where_the_person_put_it`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_a_readable_track_beside_an_unread_one_still_leads`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`

Old text:

```
        if not at or max(at) >= write.sent:
```

New text:

```
        if at and max(at) >= write.sent:
```

### `r1394.P7_unknown_named_as_landed`

held message: a reading at a move whose landing is not known is named as before the moves accepted

- File: `src/cratekit/sync/pair_model.py`
- Source: `r1394.json`, row `P7_unknown_named_as_landed`
- Moved: the same text, now in src/cratekit/sync/pair_model.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_move_whose_fate_is_unknown_holds_the_order_before_it_and_finishes_the_one_after`

Old text:

```
    elif at < write.landed:
```

New text:

```
    elif at <= write.landed:
```

### `r1394.P8_every_move_named_as_a_stop`

held message: every move accepted is named as a write that stopped part way

- File: `src/cratekit/sync/pair_model.py`
- Source: `r1394.json`, row `P8_every_move_named_as_a_stop`
- Moved: the same text, now in src/cratekit/sync/pair_model.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_every_move_accepted_and_an_agreed_reading_short_of_their_end_is_still_a_lag`

Old text:

```
    elif write is None or write.moved:
```

New text:

```
    elif write is None:
```

### `r1394.P9_finish_not_held_to_the_agreed_reading`

pair write: a write that finishes a stopped order lets the adapter plan its moves from any reading holding the same tracks, round one's row 1

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1394.json`, row `P9_finish_not_held_to_the_agreed_reading`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_the_adapter_refuses_leaves_the_stopped_write_pending`
  - `tests/test_sync_pair_settle.py::test_a_stop_after_one_of_three_moves_read_as_that_move_leaves_it_is_finished`

Old text:

```
                or (one.finishing_order and not (one.account_removes or one.account_adds))
```

New text:

```
                or False
```

### `r1404.S3_scope_every_pair`

sample, U231: every pair keeps the account's order, so a root pair's account is written rekordbox's order

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1404.json`, row `S3_scope_every_pair`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 13 (killed)
- Killed:
  - `tests/test_sync_pair_root_order.py::test_a_hand_pairs_first_sync_outside_gig_ready_keeps_rekordbox_s_order`
  - `tests/test_sync_pair_root_order.py::test_a_rekordbox_reorder_outside_gig_ready_stays_sync_after_sync`
  - `tests/test_sync_pair_root_order.py::test_a_track_only_rekordbox_holds_is_appended_to_the_account_and_nothing_else_moves`
  - `tests/test_sync_pair_root_order.py::test_a_track_only_tidal_holds_lands_after_its_neighbour_in_rekordbox_s_order`
  - `tests/test_sync_pair_root_order.py::test_a_track_placed_in_rekordbox_outside_gig_ready_keeps_its_place`
  - `tests/test_sync_pair_root_order.py::test_after_the_first_sync_a_tidal_reorder_still_leads_and_a_rekordbox_reorder_stands`
  - `tests/test_sync_pair_root_order.py::test_an_account_addition_outside_gig_ready_is_placed_in_rekordbox_s_order`
  - `tests/test_sync_pair_settle.py::test_a_pair_outside_gig_ready_gets_no_order_write_and_its_membership_still_syncs`
  - `tests/test_sync_pair_settle.py::test_a_rekordbox_side_to_be_made_is_under_gig_ready_only_inside_the_folder`
  - `tests/test_sync_pair_settle.py::test_a_root_playlist_named_gig_ready_is_not_under_gig_ready`
  - `tests/test_sync_pair_stopped_order.py::test_a_first_sync_of_an_account_playlist_with_no_stop_is_planned_as_before`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_at_the_root_never_takes_the_scramble_on_its_first_sync`
  - `tests/test_sync_pair_stopped_order.py::test_an_account_left_off_its_path_outside_gig_ready_leaves_rekordbox_untouched`

Old text:

```
    if cfg.outbound.pair_order_every_pair:
        return True
```

New text:

```
    if True:
        return True
```

### `r1411.W1_finish_passes_no_agreed`

the pair write passes no agreed reading at a finish, the measured cost R-1411 names

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1411.json`, row `W1_finish_passes_no_agreed`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_planned_again_in_the_writing_command_is_held_to_its_own_reading`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_served_as_the_moves_left_it_finishes`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_removes_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_pending_stop_agreed_off_its_path_is_finished_from_rekordbox`
  - `tests/test_sync_pair_stopped_order.py::test_an_account_the_stop_left_off_its_path_is_never_written_into_rekordbox`

Old text:

```
            if one.finishing_order and one.account_before
```

New text:

```
            if False
```

### `r1411.W2_finish_passes_agreed_only_with_nothing_else`

the pair write passes agreed only at a finish that adds and removes nothing, as before this card

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1411.json`, row `W2_finish_passes_agreed_only_with_nothing_else`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_planned_again_in_the_writing_command_is_held_to_its_own_reading`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_served_as_the_moves_left_it_finishes`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_removes_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`

Old text:

```
            if one.finishing_order and one.account_before
```

New text:

```
            if one.finishing_order
            and one.account_before
            and not (one.account_removes or one.account_adds)
```

### `r1411.W3_agreed_is_the_asked_order`

the pair write passes the order it asks as the agreed reading rather than the plan's reading

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1411.json`, row `W3_agreed_is_the_asked_order`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_planned_again_in_the_writing_command_is_held_to_its_own_reading`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_served_as_the_moves_left_it_finishes`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_removes_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_pending_stop_agreed_off_its_path_is_finished_from_rekordbox`
  - `tests/test_sync_pair_stopped_order.py::test_an_account_the_stop_left_off_its_path_is_never_written_into_rekordbox`

Old text:

```
            {"agreed": tuple(one.account_before)}
```

New text:

```
            {"agreed": tuple(one.account_order)}
```

### `r1411.W4_agreed_is_the_checks_listing`

round one's BLOCKING shape: the pair write passes the check's listing as the agreed reading when there is one

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1411.json`, row `W4_agreed_is_the_checks_listing`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`

Old text:

```
            {"agreed": tuple(one.account_before)}
```

New text:

```
            {"agreed": tuple(account_listed or one.account_before)}
```

### `r1416.M10_cli_account_write_kept`

pair_cli: the account write reads the order as always kept, so a root pair's first sync writes rekordbox's order onto the account

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1416.json`, row `M10_cli_account_write_kept`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 12 (killed)
- Killed:
  - `tests/test_sync_pair_root_order.py::test_a_hand_pairs_first_sync_outside_gig_ready_keeps_rekordbox_s_order`
  - `tests/test_sync_pair_root_order.py::test_a_rekordbox_reorder_outside_gig_ready_stays_sync_after_sync`
  - `tests/test_sync_pair_root_order.py::test_a_track_only_rekordbox_holds_is_appended_to_the_account_and_nothing_else_moves`
  - `tests/test_sync_pair_root_order.py::test_a_track_only_tidal_holds_lands_after_its_neighbour_in_rekordbox_s_order`
  - `tests/test_sync_pair_root_order.py::test_a_track_placed_in_rekordbox_outside_gig_ready_keeps_its_place`
  - `tests/test_sync_pair_root_order.py::test_after_the_first_sync_a_tidal_reorder_still_leads_and_a_rekordbox_reorder_stands`
  - `tests/test_sync_pair_root_order.py::test_an_account_addition_outside_gig_ready_is_placed_in_rekordbox_s_order`
  - `tests/test_sync_pair_settle.py::test_a_pair_outside_gig_ready_gets_no_order_write_and_its_membership_still_syncs`
  - `tests/test_sync_pair_settle.py::test_a_root_playlist_named_gig_ready_is_not_under_gig_ready`
  - `tests/test_sync_pair_stopped_order.py::test_a_first_sync_of_an_account_playlist_with_no_stop_is_planned_as_before`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_at_the_root_never_takes_the_scramble_on_its_first_sync`
  - `tests/test_sync_pair_stopped_order.py::test_an_account_left_off_its_path_outside_gig_ready_leaves_rekordbox_untouched`

Old text:

```
        order_unkept = wanted_keys != firsts and not order_kept
```

New text:

```
        order_unkept = False
```

### `r1416.M7_cli_tells_kept`

pair_cli: the merge is always told the order is kept, so a root pair's first sync puts rekordbox in the account's order again

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1416.json`, row `M7_cli_tells_kept`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_root_order.py::test_a_hand_pairs_first_sync_outside_gig_ready_keeps_rekordbox_s_order`
  - `tests/test_sync_pair_root_order.py::test_a_track_only_rekordbox_holds_is_appended_to_the_account_and_nothing_else_moves`
  - `tests/test_sync_pair_root_order.py::test_a_track_only_tidal_holds_lands_after_its_neighbour_in_rekordbox_s_order`
  - `tests/test_sync_pair_stopped_order.py::test_a_first_sync_of_an_account_playlist_with_no_stop_is_planned_as_before`

Old text:

```
        order_kept=order_kept,
```

New text:

```
        order_kept=True,
```

### `r1416.M8_cli_tells_not_kept`

pair_cli: the merge is always told the order is not kept, so a GIG READY pair's first sync keeps rekordbox's order

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1416.json`, row `M8_cli_tells_not_kept`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_root_order.py::test_a_hand_pairs_first_sync_with_every_pairs_order_kept_follows_tidal`
  - `tests/test_sync_pair_stopped_order.py::test_a_first_sync_of_an_account_playlist_with_no_stop_under_gig_ready_follows_the_account`

Old text:

```
        order_kept=order_kept,
```

New text:

```
        order_kept=False,
```

### `r1416.M9_cli_scope_key_only`

pair_cli: the flag read before the merge is the config key alone, so a GIG READY pair reads as not kept

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1416.json`, row `M9_cli_scope_key_only`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 119 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_after_a_change_no_move_of_the_run_recorded_holds_it_as_moved`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_holds_a_reorder_made_on_the_account_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_finishes_it`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_a_reorder_made_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_the_added_track_moved_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_the_account_still_stands_in_finishes_it`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since[credential-missing]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since[parked]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_that_moved_nothing_hands_the_adapter_the_checks_listing[credential-missing]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_that_moved_nothing_hands_the_adapter_the_checks_listing[parked]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_that_moved_nothing_hands_the_adapter_the_checks_listing[refused]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_the_run_puts_the_refused_pair_in_order_and_moves_nothing_else`
  - `tests/test_sync_pair_order.py::test_a_continue_whose_steps_cannot_be_read_still_agrees_with_the_checks_listing_first[gone]`
  - `tests/test_sync_pair_order.py::test_a_continue_whose_steps_cannot_be_read_still_agrees_with_the_checks_listing_first[unreadable]`
  - `tests/test_sync_pair_order.py::test_a_first_order_is_asked_with_nothing_to_agree_with_but_what_the_adapter_wrote`
  - ... and 104 more, see the JSON sidecar

Old text:

```
    order_kept = _keeps_order(cfg, rekordbox, home)
```

New text:

```
    order_kept = cfg.outbound.pair_order_every_pair
```

### `r1416.S3_scope_under_the_folder`

sample, U231: a playlist under GIG READY is no longer read as kept, so its first sync is led by rekordbox

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1416.json`, row `S3_scope_under_the_folder`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 119 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_after_a_change_no_move_of_the_run_recorded_holds_it_as_moved`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_holds_a_reorder_made_on_the_account_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_finishes_it`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_a_reorder_made_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_the_added_track_moved_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_the_account_still_stands_in_finishes_it`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since[credential-missing]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since[parked]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_that_moved_nothing_hands_the_adapter_the_checks_listing[credential-missing]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_that_moved_nothing_hands_the_adapter_the_checks_listing[parked]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_that_moved_nothing_hands_the_adapter_the_checks_listing[refused]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_the_run_puts_the_refused_pair_in_order_and_moves_nothing_else`
  - `tests/test_sync_pair_order.py::test_a_continue_whose_steps_cannot_be_read_still_agrees_with_the_checks_listing_first[gone]`
  - `tests/test_sync_pair_order.py::test_a_continue_whose_steps_cannot_be_read_still_agrees_with_the_checks_listing_first[unreadable]`
  - `tests/test_sync_pair_order.py::test_a_first_order_is_asked_with_nothing_to_agree_with_but_what_the_adapter_wrote`
  - ... and 104 more, see the JSON sidecar

Old text:

```
        return bool(rekordbox.ancestors) and rekordbox.top[1] == ORDER_FOLDER
```

New text:

```
        return False
```

### `r1418.F1_agreed_is_the_readable_tracks`

the brief's row: a finish is held to the tracks the provider could read, so a lag differing only by where an unread track stands is planned from

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1418.json`, row `F1_agreed_is_the_readable_tracks`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`

Old text:

```
            {"agreed": tuple(one.account_before)}
```

New text:

```
            {"agreed": tuple(one.account_now)}
```

### `r1418.F2_agreed_passed_for_an_empty_reading`

the clause for an empty plan reading dropped, so a finish whose plan read no account passes an empty agreed order to an adapter that may not take it

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1418.json`, row `F2_agreed_passed_for_an_empty_reading`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_plan_read_no_account_passes_no_agreed_reading`

Old text:

```
            if one.finishing_order and one.account_before
            else {}
```

New text:

```
            if one.finishing_order
            else {}
```

### `r1418.F3_agreed_passed_only_for_an_empty_reading`

the clause inverted, so a finish whose plan read the account passes no agreed order and is held to membership alone

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1418.json`, row `F3_agreed_passed_only_for_an_empty_reading`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 11 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_planned_again_in_the_writing_command_is_held_to_its_own_reading`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_served_as_the_moves_left_it_finishes`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_removes_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_plan_read_no_account_passes_no_agreed_reading`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_pending_stop_agreed_off_its_path_is_finished_from_rekordbox`
  - `tests/test_sync_pair_stopped_order.py::test_an_account_the_stop_left_off_its_path_is_never_written_into_rekordbox`

Old text:

```
            if one.finishing_order and one.account_before
            else {}
```

New text:

```
            if one.finishing_order and not one.account_before
            else {}
```

### `r1418.F4_agreed_only_without_adds_or_removes`

existing guard, R-1411: a finish that also adds or removes passes no agreed order, as before R-1411

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1418.json`, row `F4_agreed_only_without_adds_or_removes`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_planned_again_in_the_writing_command_is_held_to_its_own_reading`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_served_as_the_moves_left_it_finishes`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_removes_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`

Old text:

```
            if one.finishing_order and one.account_before
            else {}
```

New text:

```
            if one.finishing_order
            and one.account_before
            and not (one.account_removes or one.account_adds)
            else {}
```

### `r1418.F5_plans_reading_without_unread_ids`

existing guard, R-1264: the plan's reading of an account it orders is the readable tracks alone, unread ids left out of it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1418.json`, row `F5_plans_reading_without_unread_ids`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - `tests/test_sync_pair_settle.py::test_a_track_unread_at_the_stop_and_read_since_is_read_as_the_persons_when_moved`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_before_the_first_send_is_kept_where_it_was_put`

Old text:

```
            account_before = tuple(listed_order or account_now)
```

New text:

```
            account_before = tuple(account_now)
```

### `r1420-b.B2_beyond_tail_unread_pinned`

sample: the part written check reads the kept tracks' order but not that this write's additions stand after them, measured again once a test pins it

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1420-b.json`, row `B2_beyond_tail_unread_pinned`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_the_added_track_moved_since`

Old text:

```
        if kept != [track for track in one.account_now if track in held] or (
            list(now) != kept + tail
        ):
```

New text:

```
        if kept != [track for track in one.account_now if track in held] or (
            list(now) != list(now)
        ):
```

### `r1420.B1_beyond_order_unread`

sample: the part written check never reads the order, whatever ordering says

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1420.json`, row `B1_beyond_order_unread`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_after_a_change_no_move_of_the_run_recorded_holds_it_as_moved`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_holds_a_reorder_made_on_the_account_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_a_reorder_made_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_the_added_track_moved_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since[credential-missing]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since[parked]`
  - `tests/test_sync_pair_resume_one.py::test_a_reorder_by_hand_on_the_part_written_playlist_refuses_stale`
  - `tests/test_sync_pair_stopped_order.py::test_a_stopped_write_its_continue_holds_is_finished_by_the_next_sync_and_leaves_nothing`

Old text:

```
    if not parts and not ordering:
```

New text:

```
    if not parts and ordering is None:
```

### `r1420.B3_beyond_removals_asked`

sample: the kept order is compared to the whole plan's reading, so a track this write took off reads as a reorder

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1420.json`, row `B3_beyond_removals_asked`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_rekordbox_playlist_changed_after_this_run_wrote_it_refuses_stale`
  - `tests/test_sync_pair_resume_one.py::test_a_stop_inside_the_account_write_is_finished_without_writing_rekordbox_twice`
  - `tests/test_sync_pair_resume_one.py::test_a_track_withheld_on_the_part_written_playlist_refuses_stale`

Old text:

```
        if kept != [track for track in one.account_now if track in held] or (
```

New text:

```
        if kept != [track for track in one.account_now] or (
```

### `r1420.C1_continued_ignored`

a continue of an order parked or stopped with the whole write before any move passes the adapter no listing to agree with

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1420.json`, row `C1_continued_ignored`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_that_moved_nothing_hands_the_adapter_the_checks_listing[credential-missing]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_that_moved_nothing_hands_the_adapter_the_checks_listing[parked]`
  - `tests/test_sync_pair_order.py::test_a_continue_whose_steps_cannot_be_read_still_agrees_with_the_checks_listing_first[gone]`
  - `tests/test_sync_pair_order.py::test_a_continue_whose_steps_cannot_be_read_still_agrees_with_the_checks_listing_first[unreadable]`

Old text:

```
                or (continued and not one.finishing_order)
```

New text:

```
                or (continued and one.finishing_order and False)
```

### `r1420.C3_continued_read_after_the_mark`

whether an earlier command began the order is read as always yes, so a first order is asked to agree with the check's listing

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1420.json`, row `C3_continued_read_after_the_mark`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_first_order_is_asked_with_nothing_to_agree_with_but_what_the_adapter_wrote`

Old text:

```
        continued = steps.has(STEP_ORDERING)
```

New text:

```
        continued = steps.has(STEP_ORDERING) or True
```

### `r1420.C4_carried_record_unread`

a continue whose run's steps cannot be read does not read the carried record, so its order of a pair that moved nothing is asked with no listing to agree with

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1420.json`, row `C4_carried_record_unread`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_whose_steps_cannot_be_read_still_agrees_with_the_checks_listing_first[gone]`
  - `tests/test_sync_pair_order.py::test_a_continue_whose_steps_cannot_be_read_still_agrees_with_the_checks_listing_first[unreadable]`

Old text:

```
        continued = steps.has(STEP_ORDERING) or steps.carried(STEP_ORDERING) is not None
```

New text:

```
        continued = steps.has(STEP_ORDERING) or steps.carried(STEP_ORDERING) is None and False
```

### `r1420.E2_finish_agreed_dropped`

sample: a finish of a stopped order is not held to the plan's reading at the adapter

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1420.json`, row `E2_finish_agreed_dropped`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_planned_again_in_the_writing_command_is_held_to_its_own_reading`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_served_as_the_moves_left_it_finishes`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_removes_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_pending_stop_agreed_off_its_path_is_finished_from_rekordbox`
  - `tests/test_sync_pair_stopped_order.py::test_an_account_the_stop_left_off_its_path_is_never_written_into_rekordbox`

Old text:

```
            if one.finishing_order and one.account_before
            else {}
```

New text:

```
            if False and one.finishing_order and one.account_before
            else {}
```

### `r1420.N1_fix_reverted`

the check leaves the order unread once ordering is marked, as before R-1420, so a person's reorder after an order that moved nothing is written over

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1420.json`, row `N1_fix_reverted`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_after_a_change_no_move_of_the_run_recorded_holds_it_as_moved`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_holds_a_reorder_made_on_the_account_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_a_reorder_made_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_the_added_track_moved_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since[credential-missing]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since[parked]`
  - `tests/test_sync_pair_stopped_order.py::test_a_stopped_write_its_continue_holds_is_finished_by_the_next_sync_and_leaves_nothing`

Old text:

```
    return steps.has(STEP_ORDERING) and (steps.has(STEP_MOVING) or one.finishing_order)
```

New text:

```
    return steps.has(STEP_ORDERING)
```

### `r1420.N2_moves_begun_ignored`

a pair whose moves began has its order read, so a continue of a stop part way through the moves refuses the moves' own order as moved

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1420.json`, row `N2_moves_begun_ignored`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_stop_in_the_middle_of_an_order_sends_no_move_again_and_a_later_sync_finishes_it`
  - `tests/test_sync_pair_settle.py::test_a_continues_settle_window_is_counted_from_when_the_moves_began`
  - `tests/test_sync_pair_settle.py::test_a_stop_part_way_then_a_continue_sends_no_move_again`
  - `tests/test_sync_pair_settle.py::test_a_stop_part_way_whose_moves_all_landed_finishes_on_the_continue`

Old text:

```
    return steps.has(STEP_ORDERING) and (steps.has(STEP_MOVING) or one.finishing_order)
```

New text:

```
    return steps.has(STEP_ORDERING) and one.finishing_order
```

### `r1420.N3_finish_read_too`

a finish of a stopped order has its order read by the check, so a continue of a refused finish whose check lists the lag is held as moved rather than refused at the adapter

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1420.json`, row `N3_finish_read_too`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`

Old text:

```
    return steps.has(STEP_ORDERING) and (steps.has(STEP_MOVING) or one.finishing_order)
```

New text:

```
    return steps.has(STEP_ORDERING) and steps.has(STEP_MOVING)
```

### `r1420.N5_order_always_read`

every part written pair has its order read, the moves' own included

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1420.json`, row `N5_order_always_read`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_stop_in_the_middle_of_an_order_sends_no_move_again_and_a_later_sync_finishes_it`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_continues_settle_window_is_counted_from_when_the_moves_began`
  - `tests/test_sync_pair_settle.py::test_a_stop_part_way_then_a_continue_sends_no_move_again`
  - `tests/test_sync_pair_settle.py::test_a_stop_part_way_whose_moves_all_landed_finishes_on_the_continue`

Old text:

```
    return steps.has(STEP_ORDERING) and (steps.has(STEP_MOVING) or one.finishing_order)
```

New text:

```
    return False and steps.has(STEP_ORDERING)
```

### `r1420.N6_call_site_never_reads_order`

the check passes ordering as true for every part written pair, so no order is read once an account write began

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1420.json`, row `N6_call_site_never_reads_order`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_after_a_change_no_move_of_the_run_recorded_holds_it_as_moved`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_holds_a_reorder_made_on_the_account_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_a_reorder_made_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_the_added_track_moved_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since[credential-missing]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since[parked]`
  - `tests/test_sync_pair_resume_one.py::test_a_reorder_by_hand_on_the_part_written_playlist_refuses_stale`
  - `tests/test_sync_pair_stopped_order.py::test_a_stopped_write_its_continue_holds_is_finished_by_the_next_sync_and_leaves_nothing`

Old text:

```
                why = _beyond(one, now, ordering=_ordered_by_this_run(one, of(one)))
```

New text:

```
                why = _beyond(one, now, ordering=True)
```

### `r1432-composites.C4_finish_reads_the_listing_unfinished`

what E4 holds: at a finish the readable tracks are read as the account lists them, with the stopped write's remaining moves not applied, so its half done order is read as the account's

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1432-composites.json`, row `C4_finish_reads_the_listing_unfinished`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 61 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_keeps_an_unread_track_the_stopped_write_did_not_move_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_finish_planned_again_in_the_writing_command_is_held_to_its_own_reading`
  - `tests/test_sync_pair_settle.py::test_a_finish_puts_an_unread_track_the_stopped_move_put_in_front_where_the_write_was_taking_it`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_served_as_the_moves_left_it_finishes`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_removes_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_the_adapter_refuses_leaves_the_stopped_write_pending`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_finish_with_no_unread_track_is_put_in_rekordboxs_order`
  - `tests/test_sync_pair_settle.py::test_a_first_move_refused_on_its_412s_is_sent_again_from_the_start_once`
  - `tests/test_sync_pair_settle.py::test_a_hand_move_of_the_unread_track_read_first_after_the_stop_is_finished_by_the_target`
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - ... and 46 more, see the JSON sidecar

Old text:

```
                for one in pair_stopped.finished(
                    listed_order or account_now, stopped_write.target
                )
```

New text:

```
                for one in (listed_order or account_now)
```

### `r1432.E1_listed_rule_puts_it_first`

existing guard, R-1264: an unread track not named by a target goes to the front rather than behind the track listed before it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1432.json`, row `E1_listed_rule_puts_it_first`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 18 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_keeps_an_unread_track_the_stopped_write_did_not_move_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_finish_puts_an_unread_track_the_stopped_move_put_in_front_where_the_write_was_taking_it`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_hand_move_of_the_unread_track_read_first_after_the_stop_is_finished_by_the_target`
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - `tests/test_sync_pair_settle.py::test_a_reorder_settled_readings_show_keeps_the_unread_track_where_the_person_put_it`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_a_readable_track_beside_an_unread_one_still_leads`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_a_stop_before_the_first_send_with_nothing_moved_is_finished_from_its_start`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_before_the_first_send_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_taken_off_the_account_after_the_stop_is_never_put_back`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered5-listed5-target5-expected5]`
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`
  - ... and 3 more, see the JSON sidecar

Old text:

```
        placed.insert(behind(listed[:index]), one)
```

New text:

```
        placed.insert(0, one)
```

### `r1432.P10_warning_says_it_stays`

the sync-pair-unread warning at a finish says only that each stays where it is

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1432.json`, row `P10_warning_says_it_stays`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_puts_an_unread_track_the_stopped_move_put_in_front_where_the_write_was_taking_it`
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`

Old text:

```
                        if finished_unread
```

New text:

```
                        if False
```

### `r1432.P3_target_id_no_longer_listed_put_back`

an unread id the target names and the account no longer lists is put back into the asked order

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1432.json`, row `P3_target_id_no_longer_listed_put_back`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_an_unread_track_taken_off_the_account_after_the_stop_is_never_put_back`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered3-listed3-target3-expected3]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered6-listed6-target6-expected6]`

Old text:

```
        if one in held or one not in holding:
```

New text:

```
        if one in held:
```

### `r1432.P4_target_id_already_held_put_twice`

a target id the order already holds, a readable track, is inserted again, so the asked order holds it twice

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1432.json`, row `P4_target_id_already_held_put_twice`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered0-listed0-target0-expected0]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered1-listed1-target1-expected1]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered2-listed2-target2-expected2]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered3-listed3-target3-expected3]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered4-listed4-target4-expected4]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered5-listed5-target5-expected5]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered6-listed6-target6-expected6]`
  - `tests/test_sync_pair_stopped_order.py::test_rekordbox_reordered_since_the_stop_leads`

Old text:

```
        if one in held or one not in holding:
```

New text:

```
        if one not in holding:
```

### `r1432.P5_target_placed_by_the_listing`

each unread id the target names is placed behind the track the listing shows before it, not the one the target puts before it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1432.json`, row `P5_target_placed_by_the_listing`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 11 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_puts_an_unread_track_the_stopped_move_put_in_front_where_the_write_was_taking_it`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_hand_move_of_the_unread_track_read_first_after_the_stop_is_finished_by_the_target`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered0-listed0-target0-expected0]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered1-listed1-target1-expected1]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered2-listed2-target2-expected2]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered3-listed3-target3-expected3]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered4-listed4-target4-expected4]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered5-listed5-target5-expected5]`
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`

Old text:

```
        placed.insert(behind(target[:index]), one)
```

New text:

```
        placed.insert(behind(listed[: list(listed).index(one)]), one)
```

### `r1432.P6_target_behind_the_first_held`

an unread id is placed behind the first track the target puts before it that the order holds, not the nearest

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1432.json`, row `P6_target_behind_the_first_held`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 19 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_keeps_an_unread_track_the_stopped_write_did_not_move_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_finish_puts_an_unread_track_the_stopped_move_put_in_front_where_the_write_was_taking_it`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_hand_move_of_the_unread_track_read_first_after_the_stop_is_finished_by_the_target`
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - `tests/test_sync_pair_settle.py::test_a_reorder_settled_readings_show_keeps_the_unread_track_where_the_person_put_it`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_a_readable_track_beside_an_unread_one_still_leads`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_a_stop_before_the_first_send_with_nothing_moved_is_finished_from_its_start`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_before_the_first_send_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_taken_off_the_account_after_the_stop_is_never_put_back`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered0-listed0-target0-expected0]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered1-listed1-target1-expected1]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered2-listed2-target2-expected2]`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        for one in reversed(before):
```

New text:

```
        for one in before:
```

### `r1432.P7_none_held_goes_last`

an unread id with no held track before it goes to the end rather than the front

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1432.json`, row `P7_none_held_goes_last`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered4-listed4-target4-expected4]`
  - `tests/test_sync_pair_settle.py::test_with_no_stopped_write_an_unread_track_follows_the_one_listed_before_it[ordered0-listed0-expected0]`

Old text:

```
                return placed.index(one) + 1
        return 0
```

New text:

```
                return placed.index(one) + 1
        return len(placed)
```

### `r1432.P8_placed_in_front_of_its_neighbour`

an unread id is put in front of the track it follows rather than behind it, the target's and the listing's alike (R-1418's F6, in this unit's shape)

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1432.json`, row `P8_placed_in_front_of_its_neighbour`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 22 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_keeps_an_unread_track_the_stopped_write_did_not_move_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_finish_puts_an_unread_track_the_stopped_move_put_in_front_where_the_write_was_taking_it`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_hand_move_of_the_unread_track_read_first_after_the_stop_is_finished_by_the_target`
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - `tests/test_sync_pair_settle.py::test_a_reorder_settled_readings_show_keeps_the_unread_track_where_the_person_put_it`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_a_readable_track_beside_an_unread_one_still_leads`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_a_stop_before_the_first_send_with_nothing_moved_is_finished_from_its_start`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_before_the_first_send_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_taken_off_the_account_after_the_stop_is_never_put_back`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered0-listed0-target0-expected0]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered1-listed1-target1-expected1]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered2-listed2-target2-expected2]`
  - ... and 7 more, see the JSON sidecar

Old text:

```
                return placed.index(one) + 1
```

New text:

```
                return placed.index(one)
```

### `r1434.F7_ordering_start_from_the_readable_tracks`

R-1418's zero row, now the card's pin: the ordering step records its start from the readable tracks, so a track unread at the stop and read since is left out of the path read and its move by the person is put back

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1434.json`, row `F7_ordering_start_from_the_readable_tracks`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - `tests/test_sync_pair_settle.py::test_a_track_unread_at_the_stop_and_read_since_is_read_as_the_persons_when_moved`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_before_the_first_send_is_kept_where_it_was_put`

Old text:

```
                    one.account_before or one.account_now, removed, added
```

New text:

```
                    one.account_now, removed, added
```

### `r1434.M1_write_that_sent_nothing_read_on_its_whole_path`

round two's shape: a write known to have sent no move is read against its whole path, so a person's drag of one track to the top, where its first move would have put it, is finished over

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1434.json`, row `M1_write_that_sent_nothing_read_on_its_whole_path`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_drag_to_the_top_after_a_write_that_sent_no_move_leads[all-read]`
  - `tests/test_sync_pair_settle.py::test_a_drag_to_the_top_after_a_write_that_sent_no_move_leads[t9-unread]`

Old text:

```
    return tuple(write.start) if write.sent_nothing else tuple(write.target)
```

New text:

```
    return tuple(write.target)
```

### `r1434.M2_plan_reads_a_write_that_sent_nothing_on_its_whole_path`

the plan's path read alone back on the whole path for a write that sent no move, R-1446's check of a readable move keeping the start

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1434.json`, row `M2_plan_reads_a_write_that_sent_nothing_on_its_whole_path`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_drag_to_the_top_after_a_write_that_sent_no_move_leads[all-read]`

Old text:

```
            stopped_write.start, _toward(stopped_write), reading
```

New text:

```
            stopped_write.start, stopped_write.target, reading
```

### `r1434.M3_readable_move_after_a_write_that_sent_nothing_read_on_its_whole_path`

R-1446's check of a readable move alone back on the whole path for a write that sent no move, so a drag of a readable track to the top with an unread track listed reads as an unread move

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1434.json`, row `M3_readable_move_after_a_write_that_sent_nothing_read_on_its_whole_path`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_drag_to_the_top_after_a_write_that_sent_no_move_leads[t9-unread]`

Old text:

```
        return not pair_stopped.reached(write.start, _toward(write), readable)
```

New text:

```
        return not pair_stopped.reached(write.start, write.target, readable)
```

### `r1434.M4_hold_promises_the_accounts_order_for_an_unread_move`

the hold while a move of unread tracks alone settles says the account's order is then read as the person's, though the others are finished in the stopped order

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1434.json`, row `M4_hold_promises_the_accounts_order_for_an_unread_move`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`

Old text:

```
            if unread and not _readable_moved(write, kept, reading, unread, moved_nothing=False)
```

New text:

```
            if False
```

### `r1434.M5_hold_withholds_the_lead_from_a_readable_reorder`

the hold while a reorder of readable tracks settles says the others are finished in the stopped order, though the account's order then leads

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1434.json`, row `M5_hold_withholds_the_lead_from_a_readable_reorder`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_reorder_seen_changing_between_two_syncs_after_the_stop_leads`

Old text:

```
            if unread and not _readable_moved(write, kept, reading, unread, moved_nothing=False)
```

New text:

```
            if True
```

### `r1434.S1_sent_nothing_off_path_waits_for_settled_readings`

existing guard, U234: an order off the path of a write known to have sent no move no longer leads at once

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1434.json`, row `S1_sent_nothing_off_path_waits_for_settled_readings`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_holds_a_reorder_made_on_the_account_since`
  - `tests/test_sync_pair_settle.py::test_a_drag_to_the_top_after_a_write_that_sent_no_move_leads[all-read]`
  - `tests/test_sync_pair_settle.py::test_a_drag_to_the_top_after_a_write_that_sent_no_move_leads[t9-unread]`
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - `tests/test_sync_pair_settle.py::test_a_reorder_after_a_finish_stopped_before_its_first_send_leads`
  - `tests/test_sync_pair_settle.py::test_a_reorder_after_a_track_read_at_the_stop_turned_unread_leads`
  - `tests/test_sync_pair_stopped_order.py::test_a_stop_this_version_recorded_with_no_move_sent_leaves_a_reorder_the_persons`

Old text:

```
        moved_nothing = off_path and stopped_write.sent_nothing
```

New text:

```
        moved_nothing = False
```

### `r1434.S3_unread_track_placed_at_the_front`

existing guard, R-1264: an unread track a reorder does not move is put at the front rather than behind the track listed before it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1434.json`, row `S3_unread_track_placed_at_the_front`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 22 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_keeps_an_unread_track_the_stopped_write_did_not_move_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_finish_puts_an_unread_track_the_stopped_move_put_in_front_where_the_write_was_taking_it`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_hand_move_of_the_unread_track_read_first_after_the_stop_is_finished_by_the_target`
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - `tests/test_sync_pair_settle.py::test_a_reorder_settled_readings_show_keeps_the_unread_track_where_the_person_put_it`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_a_readable_track_beside_an_unread_one_still_leads`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_a_stop_before_the_first_send_with_nothing_moved_is_finished_from_its_start`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_before_the_first_send_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_taken_off_the_account_after_the_stop_is_never_put_back`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered0-listed0-target0-expected0]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered1-listed1-target1-expected1]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered2-listed2-target2-expected2]`
  - ... and 7 more, see the JSON sidecar

Old text:

```
                return placed.index(one) + 1
```

New text:

```
                return 0
```

### `r1434.S5_folded_base_keeps_unread_keys`

existing guard, R-1264: the base keeps an unread track's key, so it is read as taken off the account

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1434.json`, row `S5_folded_base_keeps_unread_keys`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_reorder_after_a_track_read_at_the_stop_turned_unread_leads`
  - `tests/test_sync_pair_unread.py::test_a_row_held_only_as_an_unread_release_stays_where_the_account_lists_it`
  - `tests/test_sync_pair_unread.py::test_a_row_whose_listed_release_is_its_unread_second_stays_in_rekordbox`
  - `tests/test_sync_pair_unread.py::test_an_unread_track_the_twin_holds_is_never_removed_or_added_again`

Old text:

```
            base_account = tuple(key for key in base_account if key not in unread_keys)
```

New text:

```
            base_account = tuple(base_account)
```

### `r1446-b.C1_composite_no_unread_left_out`

the composite of r1446 rows M10 and M11, what they hold together: the settled reading and the reading now both compared with their unread ids in place, so a move of an unread track alone reads as a reorder again; either filter alone is equivalent, since reordered reads only the tracks both readings hold

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1446-b.json`, row `C1_composite_no_unread_left_out`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`
- Collected: 155 against a baseline of 155
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_a_settled_reorder_moved_a_readable_track_only_when_one_moved[kept0-reading0-unread0-False]`
  - `tests/test_sync_pair_settle.py::test_a_settled_reorder_moved_a_readable_track_only_when_one_moved[kept4-reading4-unread4-False]`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`

Old text:

```
        [one for one in kept.order if one not in left_out], readable
```

New text:

```
        list(kept.order), list(reading)
```

### `r1446-c.F1_every_unread_kept_its_place`

round one's BLOCKING reverted: once only unread tracks moved, no target at all, so an unread track nobody moved keeps the interrupted move's place

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1446-c.json`, row `F1_every_unread_kept_its_place`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`
- Collected: 264 against a baseline of 264
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`

Old text:

```
                    else tuple(one for one in stopped_write.target if one not in moved_unread)
```

New text:

```
                    else ()
```

### `r1446-c.F2_no_unread_id_read_as_moved`

every unread id read as unmoved, so the one the person moved is put where the stopped order was taking it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1446-c.json`, row `F2_no_unread_id_read_as_moved`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`
- Collected: 264 against a baseline of 264
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_the_unread_tracks_moved_since_the_stop_are_those_off_the_order_both_readings_share`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`

Old text:

```
    return frozenset(one for one in now if one in left_out and one not in held)
```

New text:

```
    return frozenset()
```

