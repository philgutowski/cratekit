# Mutation table: u953-replay-before-b

Measured by `scripts/mutate.py` on 2026-11-23 07:20 UTC, branch `HEAD` at `5113ee10`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22473 collected. pytest invocations for this batch: 135.

Full baseline: measured by this driver (the battery's verdict was not read: it is for commit `f9d2886f2fdd`, and this tree is at `5113ee10f744`).

Subset baselines: 34, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22473 against 22473. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r1830.M11_held_object_left_stale` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 74 | 1 | killed |
| `r1830.M13_planned_rows_admitted_unjudged` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 286 | 1 | killed |
| `r1830.M14_other_columns_not_compared` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 286 | 1 | killed |
| `r1830.M15_number_not_compared` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 286 | 1 | killed |
| `r1830.M16_marker_change_not_compared` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 286 | 1 | killed |
| `r1830.M17_positions_never_read` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 74 | 15 | killed |
| `r1830.M1_tie_counted_as_below` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 212 | 1 | killed |
| `r1830.M23_unreadable_marker_passed_over` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 74 | 1 | killed |
| `r1830.M2_marked_removed_row_counted` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 286 | 3 | killed |
| `r1830.M3_marked_survivor_moved` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 286 | 1 | killed |
| `r1830.M4_one_place_whatever_removed` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 286 | 2 | killed |
| `r1830.M5_any_playlist_counts` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 286 | 16 | killed |
| `r1830.M8_renumbering_stamps_updated_at` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 74 | 15 | killed |
| `r1830.M9_moved_row_not_refused` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 74 | 1 | killed |
| `r1890.P1_bare_runtime_error_in_rb_removal` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 221 | 1 | killed |
| `u288.M10_changed_rows` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 286 | 7 | killed |
| `u288.M11_added_rows` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 286 | 2 | killed |
| `u288.M12_still_names` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 286 | 1 | killed |
| `u288.M13_counter_forward` | `src/cratekit/core/rb_removal.py` | maintainer | 2 file(s) | 286 | 1 | killed |
| `u288.M3_unmeasured_tables_skipped` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 74 | 3 | killed |
| `u288.M4_target_id_not_asked` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 74 | 1 | killed |
| `u288.M8_memberships_kept` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 74 | 19 | killed |
| `u288.M9_whose_row_disappeared` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 286 | 1 | killed |
| `a32.A6_policy_left_behind` | `src/cratekit/core/rb_tables.py` | maintainer | 2 file(s) | 113 | 4 | killed |
| `a32.V4_policy_unrestricted` | `src/cratekit/core/rb_tables.py` | user | 1 file(s) | 60 | 1 | killed |
| `r746-a.G8_key_dropped_from_the_content_policy` | `src/cratekit/core/rb_tables.py` | user | 2 file(s) | 233 | collection error | collect-error |
| `r923.N18_policy_owns_the_fields` | `src/cratekit/core/rb_tables.py` | user | 41 file(s) | 3779 | 1 | killed |
| `r923.N19_default_is_an_analysis_column` | `src/cratekit/core/rb_tables.py` | user | 41 file(s) | 3779 | 35 | killed |
| `u111-a.A6_playlist_not_removable` | `src/cratekit/core/rb_tables.py` | user | 2 file(s) | 243 | collection error | collect-error |
| `u115.F3_file_id_policy_fill_if_empty` | `src/cratekit/core/rb_tables.py` | user | 41 file(s) | 3779 | 3 | killed |
| `u115.F4_binding_limit_coefficient` | `src/cratekit/core/rb_tables.py` | maintainer | 41 file(s) | 3779 | 1 | killed |
| `u163.W16_admittable_key` | `src/cratekit/core/rb_tables.py` | user | 3 file(s) | 274 | 2 | killed |
| `r1830.M21_record_omits_the_rows` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 74 | 1 | killed |
| `r1830.M6_prepare_plans_no_renumbering` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 74 | 17 | killed |
| `r1830.M7_commit_skips_the_renumbering` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 74 | 17 | killed |
| `r1890.P11_process_name_typed_in_the_writer` | `src/cratekit/core/rb_writer.py` | maintainer | 1 file(s) | 12 | 1 | killed |
| `r239-a.A1_probe_to_true` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 706 | 122 | killed |
| `r239-a.A2_probe_to_false` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 706 | 7 | killed |
| `r239-a.A3_probe_removed` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 706 | 7 | killed |
| `r239-a.A4_open_default_true` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 706 | 121 | killed |
| `r239-a.A7_needed_always_true` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 706 | 122 | killed |
| `r239-a.A8_needed_always_false` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 706 | 8 | killed |
| `r239-a.A9_header_nearby_value` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 706 | 122 | killed |
| `r375-c.W1_listener_left_on_the_handle` | `src/cratekit/core/rb_writer.py` | maintainer | 2 file(s) | 86 | 1 | killed |
| `r375-c.W2_witness_listens_one_event_early` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 86 | 2 | killed |
| `r663-a.M10_detail_size_pinned` | `src/cratekit/core/rb_writer.py` | maintainer | 1 file(s) | 51 | 1 | killed |
| `r663-a.M3_unlistable_read_as_empty` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 51 | 2 | killed |
| `r663-a.M4_one_canary_table_not_enough` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 51 | 2 | killed |
| `r663-a.M7_message_drops_the_size` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 51 | 3 | killed |
| `r663-a.M8_message_names_the_copy` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 51 | 5 | killed |
| `r663-a.M9_remedy_restore` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 51 | 3 | killed |
| `r746-a.G4_read_back_walks_session_new_only` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 66 | 2 | killed |
| `r746-a.G6_analysis_tables_not_checked` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 66 | 1 | killed |
| `r746-a.G7_sql_value_check_disarmed` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 22473 | 0 (promoted) | zero |
| `r746-d.G5_content_row_read_back_against_five_not_ten` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 22473 | 0 (promoted) | zero |
| `u185.G1_commit_guard_called` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 287 | 13 | killed |
| `u185.G2_unread_refuses` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 31 | 2 | killed |
| `u185.G3_pending_leg` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 31 | 7 | killed |
| `u185.G4_second_reading_leg` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 31 | 2 | killed |
| `u185.G5_reading_at_open` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 75 | 20 | killed |
| `u211.W4_probe_wrapped_at_commit` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 334 | 20 | killed |
| `u211.W5_probe_wrapped_at_open` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 334 | 76 | killed |
| `u267.M10_done_reading_leaks_own` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 111 | 3 | killed |
| `u267.M4_handle_opens_every_time` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 89 | 6 | killed |
| `u267.M5_handle_after_close` | `src/cratekit/core/rb_writer.py` | maintainer | 1 file(s) | 14 | 1 | killed |
| `u267.M6_release_keeps_rows` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 149 | 1 | killed |
| `u267.M7_release_any_handle` | `src/cratekit/core/rb_writer.py` | maintainer | 1 file(s) | 14 | 1 | killed |
| `u267.M8_close_closes_nothing` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 111 | 5 | killed |
| `u267.M9_done_reading_closes_shared` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 149 | 60 | killed |
| `u27-round-8-independent.W2_composite_wrong_file` | `src/cratekit/core/rb_writer.py` | user | 11 file(s) | 22473 | 0 (promoted) | zero |
| `u27-round-8-independent.W3_canary_no_name_the_database` | `src/cratekit/core/rb_writer.py` | user | 11 file(s) | 22473 | 0 (promoted) | zero |
| `u27-round-8-independent.W5_canary_message_no_path` | `src/cratekit/core/rb_writer.py` | user | 11 file(s) | 22473 | 0 (promoted) | zero |
| `u285.M1_seam_installs` | `src/cratekit/core/rb_writer.py` | user | 4 file(s) | 288 | 6 | killed |
| `u288.M14_confinement_not_called` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 74 | 2 | killed |
| `u288.M5_prepare_liveness` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 74 | 1 | killed |
| `u288.M6_prepare_unmeasured_refusal` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 74 | 3 | killed |
| `u288.M7_prepare_identity` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 74 | 1 | killed |
| `u59.M9_column_repointed` | `src/cratekit/core/rb_writer.py` | user | 22 file(s) | 2716 | 176 | killed |
| `u162.R10_latest_verb` | `src/cratekit/core/rehearsal.py` | user | 2 file(s) | 69 | 1 | killed |
| `u162.R1_area_exists` | `src/cratekit/core/rehearsal.py` | user | 2 file(s) | 69 | 1 | killed |
| `u162.R2_rekordbox_closed` | `src/cratekit/core/rehearsal.py` | user | 2 file(s) | 69 | 1 | killed |
| `u162.R3_clone_is_a_link` | `src/cratekit/core/rehearsal.py` | user | 2 file(s) | 69 | 1 | killed |
| `u162.R4_snapshots_copied` | `src/cratekit/core/rehearsal.py` | maintainer | 2 file(s) | 69 | 1 | killed |
| `u162.R5_locks_copied` | `src/cratekit/core/rehearsal.py` | maintainer | 2 file(s) | 69 | 1 | killed |
| `u162.R7_witness_database` | `src/cratekit/core/rehearsal.py` | user | 2 file(s) | 69 | 1 | killed |
| `u162.R8_witness_folders` | `src/cratekit/core/rehearsal.py` | user | 2 file(s) | 69 | 3 | killed |
| `u162.R9_latest_key` | `src/cratekit/core/rehearsal.py` | user | 2 file(s) | 69 | 2 | killed |
| `u188.M14_mapped_in_given_order` | `src/cratekit/core/rehearsal.py` | user | 1 file(s) | 25 | 1 | killed |
| `u188.M15_mapped_shortest_first` | `src/cratekit/core/rehearsal.py` | user | 1 file(s) | 25 | 1 | killed |
| `u188.M16_mapped_by_live_length` | `src/cratekit/core/rehearsal.py` | user | 1 file(s) | 25 | 1 | killed |
| `u188.M17_empty_scratch_kept` | `src/cratekit/core/rehearsal.py` | user | 1 file(s) | 25 | 1 | killed |
| `u206.M20_rehearsal_cache_not_kept_live` | `src/cratekit/core/rehearsal.py` | user | 9 file(s) | 1130 | 1 | killed |
| `r1665.R1_log_not_restored` | `src/cratekit/core/restore.py` | user | 7 file(s) | 316 | 4 | killed |
| `u27-restore-cli-independent.X6_the_rekordbox_guard_itself_is_neutered` | `src/cratekit/core/restore.py` | user | 2 file(s) | 253 | 1 | killed |

## Zero rows and what they owe

- `r746-a.G7_sql_value_check_disarmed` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r746-d.G5_content_row_read_back_against_five_not_ten` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u27-round-8-independent.W2_composite_wrong_file` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u27-round-8-independent.W3_canary_no_name_the_database` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u27-round-8-independent.W5_canary_message_no_path` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `r1830.M11_held_object_left_stale`

renumber_memberships: leave the session's mapped rows holding the old number

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1830.json`, row `M11_held_object_left_stale`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_removal.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_renumbering_writes_trackno_alone_and_a_held_row_reads_the_new_number`

Old text:

```
            session.expire(held)
```

New text:

```
            pass
```

### `r1830.M13_planned_rows_admitted_unjudged`

collection_removal_violations: admit any change to a row the rule renumbers

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1830.json`, row `M13_planned_rows_admitted_unjudged`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_removal.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 286 against a baseline of 286
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_the_confinement_admits_the_planned_renumbering_and_nothing_beside_it`

Old text:

```
                violations.extend(_renumbering_violations(key, planned[key], before, after))
```

New text:

```
                pass
```

### `r1830.M14_other_columns_not_compared`

_renumbering_violations: a renumbered row may change any other column

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1830.json`, row `M14_other_columns_not_compared`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_removal.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 286 against a baseline of 286
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_the_confinement_admits_the_planned_renumbering_and_nothing_beside_it`

Old text:

```
    if (now[0], now[1], now[3], now[4]) != (then[0], then[1], then[3], then[4]):
```

New text:

```
    if False:
```

### `r1830.M15_number_not_compared`

_renumbering_violations: a renumbered row may hold any number

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1830.json`, row `M15_number_not_compared`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_removal.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 286 against a baseline of 286
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_the_confinement_admits_the_planned_renumbering_and_nothing_beside_it`

Old text:

```
    if now[2] != wanted:
```

New text:

```
    if False:
```

### `r1830.M16_marker_change_not_compared`

_renumbering_violations: a renumbered row's marker may move

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1830.json`, row `M16_marker_change_not_compared`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_removal.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 286 against a baseline of 286
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_the_confinement_admits_the_planned_renumbering_and_nothing_beside_it`

Old text:

```
    if (now[0], now[1], now[3], now[4]) != (then[0], then[1], then[3], then[4]):
```

New text:

```
    if (now[0], now[1], now[3]) != (then[0], then[1], then[3]):
```

### `r1830.M17_positions_never_read`

database_reading: read no membership positions, so the confinement plans nothing

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1830.json`, row `M17_positions_never_read`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_removal.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 15 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_commit_that_lands_and_then_raises_still_records_every_row`
  - `tests/test_sync_removed.py::test_a_history_list_holding_others_keeps_its_numbers`
  - `tests/test_sync_removed.py::test_a_position_the_pass_holds_is_kept_and_the_collection_not_walked`
  - `tests/test_sync_removed.py::test_a_read_back_that_disagrees_refuses_as_unverified`
  - `tests/test_sync_removed.py::test_a_removed_member_in_the_middle_of_three_leaves_one_and_two_and_nothing_else_moved`
  - `tests/test_sync_removed.py::test_a_removed_row_the_database_holds_again_is_not_offered_by_delete_review`
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`
  - `tests/test_sync_removed.py::test_a_track_only_marked_out_of_a_playlist_renumbers_none_of_its_live_members`
  - `tests/test_sync_removed.py::test_an_append_after_a_renumbering_takes_the_next_position`
  - `tests/test_sync_removed.py::test_apply_takes_out_exactly_the_offered_rows_and_every_row_naming_them`
  - `tests/test_sync_removed.py::test_delete_review_after_the_apply_offers_the_removed_file_and_none_other`
  - `tests/test_sync_removed.py::test_the_last_member_removed_renumbers_nothing_in_its_playlist`
  - `tests/test_sync_removed.py::test_the_removal_writes_no_beat_grid_and_no_tempo`
  - `tests/test_sync_removed.py::test_the_session_record_names_every_row_removed_and_restore_list_reads_it`
  - `tests/test_sync_removed.py::test_two_removed_members_of_one_playlist_and_a_member_on_two_playlists`

Old text:

```
            if placed is not None:
```

New text:

```
            if False:
```

### `r1830.M1_tie_counted_as_below`

renumbered_positions: a removed row tying a survivor lowers it too

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1830.json`, row `M1_tie_counted_as_below`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_removal.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`
- Collected: 212 against a baseline of 212
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_tie_between_a_removed_row_and_a_survivor_lowers_nothing_at_that_place`

Old text:

```
        below = sum(1 for one in deleted.get(playlist, ()) if one < int(number))
```

New text:

```
        below = sum(1 for one in deleted.get(playlist, ()) if one <= int(number))
```

### `r1830.M23_unreadable_marker_passed_over`

removal_renumbering: plan around a NULL marker rather than refusing it, review round two's X1

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1830.json`, row `M23_unreadable_marker_passed_over`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_removal.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_an_unreadable_marker_in_a_playlist_to_renumber_refuses_with_nothing_written`

Old text:

```
    if unreadable:
```

New text:

```
    if False:
```

### `r1830.M2_marked_removed_row_counted`

renumbered_positions: a removed row marked removed counts, review round one's B1

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1830.json`, row `M2_marked_removed_row_counted`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_removal.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 286 against a baseline of 286
- Kills: 3 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_marked_row_is_neither_counted_nor_moved_so_live_numbers_stay_distinct`
  - `tests/test_rb_writer_guard.py::test_the_confinement_refuses_a_marked_row_renumbered`
  - `tests/test_sync_removed.py::test_a_track_only_marked_out_of_a_playlist_renumbers_none_of_its_live_members`

Old text:

```
        if content in gone and live and number is not None:
```

New text:

```
        if content in gone and number is not None:
```

### `r1830.M3_marked_survivor_moved`

renumbered_positions: a marked surviving row is lowered too

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1830.json`, row `M3_marked_survivor_moved`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_removal.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 286 against a baseline of 286
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_marked_row_is_neither_counted_nor_moved_so_live_numbers_stay_distinct`

Old text:

```
        if content in gone or not live or number is None:
```

New text:

```
        if content in gone or number is None:
```

### `r1830.M4_one_place_whatever_removed`

renumbered_positions: a row moves one place however many removed rows sit below it

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1830.json`, row `M4_one_place_whatever_removed`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_removal.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 286 against a baseline of 286
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_two_removed_members_of_one_playlist_lower_each_row_by_those_below_it`
  - `tests/test_sync_removed.py::test_two_removed_members_of_one_playlist_and_a_member_on_two_playlists`

Old text:

```
            moved[key] = (playlist, int(number), int(number) - below)
```

New text:

```
            moved[key] = (playlist, int(number), int(number) - 1)
```

### `r1830.M5_any_playlist_counts`

renumbered_positions: a removed row in any playlist lowers rows in every playlist

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1830.json`, row `M5_any_playlist_counts`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_removal.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 286 against a baseline of 286
- Kills: 16 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_member_on_two_playlists_renumbers_each_by_its_own_place_and_no_other`
  - `tests/test_sync_removed.py::test_a_commit_that_lands_and_then_raises_still_records_every_row`
  - `tests/test_sync_removed.py::test_a_history_list_holding_others_keeps_its_numbers`
  - `tests/test_sync_removed.py::test_a_position_the_pass_holds_is_kept_and_the_collection_not_walked`
  - `tests/test_sync_removed.py::test_a_read_back_that_disagrees_refuses_as_unverified`
  - `tests/test_sync_removed.py::test_a_removed_member_in_the_middle_of_three_leaves_one_and_two_and_nothing_else_moved`
  - `tests/test_sync_removed.py::test_a_removed_row_the_database_holds_again_is_not_offered_by_delete_review`
  - `tests/test_sync_removed.py::test_a_renumbering_that_moved_between_the_gate_and_the_write_refuses_as_stale`
  - `tests/test_sync_removed.py::test_a_track_only_marked_out_of_a_playlist_renumbers_none_of_its_live_members`
  - `tests/test_sync_removed.py::test_an_append_after_a_renumbering_takes_the_next_position`
  - `tests/test_sync_removed.py::test_apply_takes_out_exactly_the_offered_rows_and_every_row_naming_them`
  - `tests/test_sync_removed.py::test_delete_review_after_the_apply_offers_the_removed_file_and_none_other`
  - `tests/test_sync_removed.py::test_the_last_member_removed_renumbers_nothing_in_its_playlist`
  - `tests/test_sync_removed.py::test_the_removal_writes_no_beat_grid_and_no_tempo`
  - `tests/test_sync_removed.py::test_the_session_record_names_every_row_removed_and_restore_list_reads_it`
  - ... and 1 more, see the JSON sidecar

Old text:

```
        below = sum(1 for one in deleted.get(playlist, ()) if one < int(number))
```

New text:

```
        below = sum(1 for numbers in deleted.values() for one in numbers if one < int(number))
```

### `r1830.M8_renumbering_stamps_updated_at`

renumber_memberships: write updated_at beside TrackNo, a byte rekordbox did not write

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1830.json`, row `M8_renumbering_stamps_updated_at`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_removal.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 15 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_commit_that_lands_and_then_raises_still_records_every_row`
  - `tests/test_sync_removed.py::test_a_history_list_holding_others_keeps_its_numbers`
  - `tests/test_sync_removed.py::test_a_position_the_pass_holds_is_kept_and_the_collection_not_walked`
  - `tests/test_sync_removed.py::test_a_read_back_that_disagrees_refuses_as_unverified`
  - `tests/test_sync_removed.py::test_a_removed_member_in_the_middle_of_three_leaves_one_and_two_and_nothing_else_moved`
  - `tests/test_sync_removed.py::test_a_removed_row_the_database_holds_again_is_not_offered_by_delete_review`
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`
  - `tests/test_sync_removed.py::test_a_track_only_marked_out_of_a_playlist_renumbers_none_of_its_live_members`
  - `tests/test_sync_removed.py::test_an_append_after_a_renumbering_takes_the_next_position`
  - `tests/test_sync_removed.py::test_apply_takes_out_exactly_the_offered_rows_and_every_row_naming_them`
  - `tests/test_sync_removed.py::test_delete_review_after_the_apply_offers_the_removed_file_and_none_other`
  - `tests/test_sync_removed.py::test_the_last_member_removed_renumbers_nothing_in_its_playlist`
  - `tests/test_sync_removed.py::test_the_removal_writes_no_beat_grid_and_no_tempo`
  - `tests/test_sync_removed.py::test_the_session_record_names_every_row_removed_and_restore_list_reads_it`
  - `tests/test_sync_removed.py::test_two_removed_members_of_one_playlist_and_a_member_on_two_playlists`

Old text:

```
        f'UPDATE "{MEMBERSHIP_TABLE}" SET "{TRACK_NUMBER_COLUMN}" = :after '
```

New text:

```
        f'UPDATE "{MEMBERSHIP_TABLE}" SET "{TRACK_NUMBER_COLUMN}" = :after, "updated_at" = CURRENT_TIMESTAMP '
```

### `r1830.M9_moved_row_not_refused`

renumber_memberships: a row that moved since the prepare is passed over silently

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1830.json`, row `M9_moved_row_not_refused`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_removal.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_member_that_moved_after_the_prepare_refuses_its_renumbering_with_nothing_written`

Old text:

```
        if result.rowcount != 1:
```

New text:

```
        if False:
```

### `r1890.P1_bare_runtime_error_in_rb_removal`

rb_removal, a part, raises a bare RuntimeError where the binding maps no class, so the refusal has no code downstream

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1890.json`, row `P1_bare_runtime_error_in_rb_removal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_parts_guard.py`, `tests/test_rb_writer_guard.py`
- Collected: 221 against a baseline of 221
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_parts_guard.py::test_no_part_of_the_writer_raises_a_bare_runtime_error_or_system_exit`

Old text:

```
    raise _writer()._unavailable(
        "whitelist-violation",
        f"the binding maps no class for {table!r}
```

New text:

```
    raise RuntimeError(
        f"the binding maps no class for {table!r}
```

### `u288.M10_changed_rows`

collection_removal_violations: read a changed row as unchanged

- File: `src/cratekit/core/rb_removal.py`
- Source: `u288.json`, row `M10_changed_rows`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_removal.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 286 against a baseline of 286
- Kills: 7 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_confined_removal_reads_clean_and_every_stray_difference_is_named`
  - `tests/test_rb_writer_guard.py::test_a_reading_with_no_positions_admits_no_membership_change`
  - `tests/test_rb_writer_guard.py::test_the_confinement_admits_the_planned_renumbering_and_nothing_beside_it`
  - `tests/test_rb_writer_guard.py::test_the_confinement_refuses_a_marked_row_renumbered`
  - `tests/test_rb_writer_guard.py::test_the_read_back_after_the_commit_admits_only_the_counter_moving_forward`
  - `tests/test_sync_removed.py::test_a_renumbering_that_moves_any_other_membership_is_refused_with_nothing_written`
  - `tests/test_sync_removed.py::test_commit_proves_the_removal_confined_before_it_commits`

Old text:

```
            if old[key] == new[key]:
                continue
```

New text:

```
            if True:
                continue
```

### `u288.M11_added_rows`

collection_removal_violations: read an added row as nothing

- File: `src/cratekit/core/rb_removal.py`
- Source: `u288.json`, row `M11_added_rows`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_removal.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 286 against a baseline of 286
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_confined_removal_reads_clean_and_every_stray_difference_is_named`
  - `tests/test_rb_writer_guard.py::test_the_read_back_after_the_commit_admits_only_the_counter_moving_forward`

Old text:

```
        for key in sorted(set(new) - set(old)):
            violations.append(f"an unplanned {table} row {key!r} was added")
```

New text:

```
        for key in sorted(set(new) - set(old)):
            pass
```

### `u288.M12_still_names`

collection_removal_violations: drop the check that every row naming a removed track is gone

- File: `src/cratekit/core/rb_removal.py`
- Source: `u288.json`, row `M12_still_names`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_removal.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 286 against a baseline of 286
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_planned_removal_that_was_not_made_is_refused`

Old text:

```
            if names in gone and key in new:
```

New text:

```
            if False:
```

### `u288.M13_counter_forward`

collection_removal_violations: accept a read back whose update count did not move

- File: `src/cratekit/core/rb_removal.py`
- Source: `u288.json`, row `M13_counter_forward`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_removal.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 286 against a baseline of 286
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_the_read_back_after_the_commit_admits_only_the_counter_moving_forward`

Old text:

```
        before.counter is None or after.counter is None or after.counter <= before.counter
```

New text:

```
        before.counter is None or after.counter is None or after.counter < before.counter
```

### `u288.M3_unmeasured_tables_skipped`

content_references: ask no table, so a My Tag, sampler or unknown table naming the row is never refused nor kept

- File: `src/cratekit/core/rb_removal.py`
- Source: `u288.json`, row `M3_unmeasured_tables_skipped`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_removal.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
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

- File: `src/cratekit/core/rb_removal.py`
- Source: `u288.json`, row `M4_target_id_not_asked`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_removal.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
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

### `u288.M8_memberships_kept`

remove_from_collection: delete from the five tables after the membership table only, so the track's memberships stay naming a row that is gone

- File: `src/cratekit/core/rb_removal.py`
- Source: `u288.json`, row `M8_memberships_kept`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_removal.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
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

### `u288.M9_whose_row_disappeared`

collection_removal_violations: let any row of any table disappear

- File: `src/cratekit/core/rb_removal.py`
- Source: `u288.json`, row `M9_whose_row_disappeared`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_removal.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 286 against a baseline of 286
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_confined_removal_reads_clean_and_every_stray_difference_is_named`

Old text:

```
            if table not in DELETABLE_TABLES or naming.get(key) not in gone:
```

New text:

```
            if False:
```

### `a32.A6_policy_left_behind`

The commit's policies are left registered after the body, in the shared context manager

- File: `src/cratekit/core/rb_tables.py`
- Source: `a32.json`, row `A6_policy_left_behind`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_tables.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`, `tests/test_repair_rows.py`
- Collected: 113 against a baseline of 113
- Kills: 4 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_policy_registered_before_the_apply_survives_it`
  - `tests/test_repair_link.py::test_the_two_acts_write_each_triple_and_move_no_other_column`
  - `tests/test_repair_rows.py::test_a_policy_registered_before_the_apply_survives_it`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
    finally:
        reset_field_policies()
        for policy in was.values():
            register_field_policy(policy)
```

New text:

```
    finally:
        for policy in was.values():
            register_field_policy(policy)
```

### `a32.V4_policy_unrestricted`

The probe policy builder admits a column outside the probe set

- File: `src/cratekit/core/rb_tables.py`
- Source: `a32.json`, row `V4_policy_unrestricted`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_tables.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_the_probe_policy_names_exactly_the_columns_asked_and_refuses_any_other`

Old text:

```
    outside = wanted - set(ROW_PROBE_COLUMNS)
    if outside:
```

New text:

```
    outside = wanted - set(ROW_PROBE_COLUMNS)
    if False:
```

### `r746-a.G8_key_dropped_from_the_content_policy`

CONTENT_ROW_EMPTY_COLUMNS: KeyID is no longer a column a new content row must leave empty

- File: `src/cratekit/core/rb_tables.py`
- Source: `r746-a.json`, row `G8_key_dropped_from_the_content_policy`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_tables.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_write_guard_completeness.py`
- Collected: 233 against a baseline of 234
- Kills: 1 (collect-error)
- Note: collection changed: 233 collected against a baseline of 234. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_rb_writer_guard.py::test_the_wider_content_policy_contains_the_playlist_policy`

Old text:

```
        "KeyID",
        "SampleRate",
```

New text:

```
        "SampleRate",
```

### `r923.N18_policy_owns_the_fields`

The defaults policy owns its fields outright instead of filling only an empty one

- File: `src/cratekit/core/rb_tables.py`
- Source: `r923.json`, row `N18_policy_owns_the_fields`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_tables.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_export_collection.py`, `tests/test_genre_retag.py`, `tests/test_head_agreement.py`, `tests/test_inbox_rotate.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_metadata_policy.py`, `tests/test_naming_apply_cli.py`, `tests/test_organize.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_process_guard.py`, `tests/test_queued_resume_contract.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_snapshot.py`, `tests/test_tag_rows.py`, `tests/test_tree_writer.py`, `tests/test_whitelist_membership.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 3779 against a baseline of 3779
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_every_default_is_a_real_column_and_none_is_an_analysis_column`

Old text:

```
    fields=MappingProxyType(dict.fromkeys(CONTENT_ROW_DEFAULTS, Ownership.FILL_IF_EMPTY)),
```

New text:

```
    fields=MappingProxyType(dict.fromkeys(CONTENT_ROW_DEFAULTS, Ownership.OWNED)),
```

### `r923.N19_default_is_an_analysis_column`

A tempo joins the defaults table, so the landing would declare an analysis column

- File: `src/cratekit/core/rb_tables.py`
- Source: `r923.json`, row `N19_default_is_an_analysis_column`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_tables.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_export_collection.py`, `tests/test_genre_retag.py`, `tests/test_head_agreement.py`, `tests/test_inbox_rotate.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_metadata_policy.py`, `tests/test_naming_apply_cli.py`, `tests/test_organize.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_process_guard.py`, `tests/test_queued_resume_contract.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_snapshot.py`, `tests/test_tag_rows.py`, `tests/test_tree_writer.py`, `tests/test_whitelist_membership.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 3779 against a baseline of 3779
- Kills: 35 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists_native.py::test_a_job_queued_with_no_name_lands_in_the_batch_playlist_as_before`
  - `tests/test_intake_land_account_playlists_native.py::test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_an_undated_playlist_from_before_u175_is_left_as_it_is`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_two_swept_playlists_land_as_two_playlist_rows_under_their_exact_names`
  - `tests/test_intake_land_native.py::test_a_failure_after_the_commit_landed_is_recorded_and_still_refuses`
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_file_whose_tags_resolve_to_no_sub_stays_in_staging_on_the_native_medium_too`
  - ... and 20 more, see the JSON sidecar

Old text:

```
        "Rating": 0,
        "ColorID": "0",
```

New text:

```
        "Rating": 0,
        "BPM": 0,
        "ColorID": "0",
```

### `u111-a.A6_playlist_not_removable`

REMOVABLE_TABLES loses the playlist table, so the rotation's commit cannot carry a removed node

- File: `src/cratekit/core/rb_tables.py`
- Source: `u111-a.json`, row `A6_playlist_not_removable`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_tables.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_rb_writer_guard.py`
- Collected: 243 against a baseline of 242
- Kills: 4 (collect-error)
- Note: collection changed: 243 collected against a baseline of 242. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_inbox_rotate.py::test_a_commit_naming_the_rotation_tables_admits_a_node_marker_and_no_content_marker`
  - `tests/test_inbox_rotate.py::test_old_is_created_once_a_second_run_plans_nothing_and_still_asks_and_old_is_reused`
  - `tests/test_inbox_rotate.py::test_the_forty_and_the_hundred_move_the_one_hundred_twenty_goes_no_track_moves_then_two_stages`
  - `tests/test_rb_writer_guard.py::test_the_removable_tables_are_exactly_the_membership_and_playlist_tables`

Old text:

```
REMOVABLE_TABLES = frozenset({MEMBERSHIP_TABLE, PLAYLIST_TABLE})
```

New text:

```
REMOVABLE_TABLES = frozenset({MEMBERSHIP_TABLE})
```

### `u115.F3_file_id_policy_fill_if_empty`

The file id policy fills only an empty column, so a random id present on the row is never replaced

- File: `src/cratekit/core/rb_tables.py`
- Source: `u115.json`, row `F3_file_id_policy_fill_if_empty`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_tables.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_export_collection.py`, `tests/test_genre_retag.py`, `tests/test_head_agreement.py`, `tests/test_inbox_rotate.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_metadata_policy.py`, `tests/test_naming_apply_cli.py`, `tests/test_organize.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_process_guard.py`, `tests/test_queued_resume_contract.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_snapshot.py`, `tests/test_tag_rows.py`, `tests/test_tree_writer.py`, `tests/test_whitelist_membership.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 3779 against a baseline of 3779
- Kills: 3 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_policy_registered_before_the_apply_survives_it`
  - `tests/test_repair_rows.py::test_the_file_id_is_a_real_column_owned_by_its_policy_and_hidden_from_no_guard`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
    fields=MappingProxyType({FILE_ID_COLUMN: Ownership.OWNED}),
```

New text:

```
    fields=MappingProxyType({FILE_ID_COLUMN: Ownership.FILL_IF_EMPTY}),
```

### `u115.F4_binding_limit_coefficient`

The binding's id limit is taken as 32 bits rather than 28

- File: `src/cratekit/core/rb_tables.py`
- Source: `u115.json`, row `F4_binding_limit_coefficient`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_tables.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_export_collection.py`, `tests/test_genre_retag.py`, `tests/test_head_agreement.py`, `tests/test_inbox_rotate.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_metadata_policy.py`, `tests/test_naming_apply_cli.py`, `tests/test_organize.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_process_guard.py`, `tests/test_queued_resume_contract.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_snapshot.py`, `tests/test_tag_rows.py`, `tests/test_tree_writer.py`, `tests/test_whitelist_membership.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 3779 against a baseline of 3779
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_the_file_id_is_a_real_column_owned_by_its_policy_and_hidden_from_no_guard`

Old text:

```
BINDING_ID_LIMIT = 1 << 28
```

New text:

```
BINDING_ID_LIMIT = 1 << 32
```

### `u163.W16_admittable_key`

ADMITTABLE_ROW_TABLES: admit djmdKey beside the lookups

- File: `src/cratekit/core/rb_tables.py`
- Source: `u163.json`, row `W16_admittable_key`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_tables.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 274 against a baseline of 274
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_creation_naming_the_key_table_is_refused`
  - `tests/test_rb_writer_guard.py::test_the_admittable_tables_are_exactly_the_content_table_and_the_three_lookups`

Old text:

```
ADMITTABLE_ROW_TABLES = frozenset({CONTENT_TABLE, *LOOKUP_TABLES})
```

New text:

```
ADMITTABLE_ROW_TABLES = frozenset({CONTENT_TABLE, *LOOKUP_TABLES, "djmdKey"})
```

### `r1830.M21_record_omits_the_rows`

write_into: name no renumbered row in the session record

- File: `src/cratekit/core/rb_writer.py`
- Source: `r1830.json`, row `M21_record_omits_the_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_removed_member_in_the_middle_of_three_leaves_one_and_two_and_nothing_else_moved`

Old text:

```
        if self.renumbered:
```

New text:

```
        if False:
```

### `r1830.M6_prepare_plans_no_renumbering`

CollectionRemoval.prepare: plan no renumbering, so the gap stays

- File: `src/cratekit/core/rb_writer.py`
- Source: `r1830.json`, row `M6_prepare_plans_no_renumbering`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 17 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_commit_that_lands_and_then_raises_still_records_every_row`
  - `tests/test_sync_removed.py::test_a_history_list_holding_others_keeps_its_numbers`
  - `tests/test_sync_removed.py::test_a_member_that_moved_after_the_prepare_refuses_its_renumbering_with_nothing_written`
  - `tests/test_sync_removed.py::test_a_position_the_pass_holds_is_kept_and_the_collection_not_walked`
  - `tests/test_sync_removed.py::test_a_read_back_that_disagrees_refuses_as_unverified`
  - `tests/test_sync_removed.py::test_a_removed_member_in_the_middle_of_three_leaves_one_and_two_and_nothing_else_moved`
  - `tests/test_sync_removed.py::test_a_removed_row_the_database_holds_again_is_not_offered_by_delete_review`
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`
  - `tests/test_sync_removed.py::test_a_track_only_marked_out_of_a_playlist_renumbers_none_of_its_live_members`
  - `tests/test_sync_removed.py::test_an_append_after_a_renumbering_takes_the_next_position`
  - `tests/test_sync_removed.py::test_an_unreadable_marker_in_a_playlist_to_renumber_refuses_with_nothing_written`
  - `tests/test_sync_removed.py::test_apply_takes_out_exactly_the_offered_rows_and_every_row_naming_them`
  - `tests/test_sync_removed.py::test_delete_review_after_the_apply_offers_the_removed_file_and_none_other`
  - `tests/test_sync_removed.py::test_the_last_member_removed_renumbers_nothing_in_its_playlist`
  - `tests/test_sync_removed.py::test_the_removal_writes_no_beat_grid_and_no_tempo`
  - ... and 2 more, see the JSON sidecar

Old text:

```
        return cls(db, ids, identity, columns, database_reading(db), removal_renumbering(db, ids))
```

New text:

```
        return cls(db, ids, identity, columns, database_reading(db), {})
```

### `r1830.M7_commit_skips_the_renumbering`

CollectionRemoval.commit: delete and never write the renumbering

- File: `src/cratekit/core/rb_writer.py`
- Source: `r1830.json`, row `M7_commit_skips_the_renumbering`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 17 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_commit_that_lands_and_then_raises_still_records_every_row`
  - `tests/test_sync_removed.py::test_a_history_list_holding_others_keeps_its_numbers`
  - `tests/test_sync_removed.py::test_a_member_that_moved_after_the_prepare_refuses_its_renumbering_with_nothing_written`
  - `tests/test_sync_removed.py::test_a_position_the_pass_holds_is_kept_and_the_collection_not_walked`
  - `tests/test_sync_removed.py::test_a_read_back_that_disagrees_refuses_as_unverified`
  - `tests/test_sync_removed.py::test_a_removed_member_in_the_middle_of_three_leaves_one_and_two_and_nothing_else_moved`
  - `tests/test_sync_removed.py::test_a_removed_row_the_database_holds_again_is_not_offered_by_delete_review`
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`
  - `tests/test_sync_removed.py::test_a_track_only_marked_out_of_a_playlist_renumbers_none_of_its_live_members`
  - `tests/test_sync_removed.py::test_an_append_after_a_renumbering_takes_the_next_position`
  - `tests/test_sync_removed.py::test_apply_takes_out_exactly_the_offered_rows_and_every_row_naming_them`
  - `tests/test_sync_removed.py::test_delete_review_after_the_apply_offers_the_removed_file_and_none_other`
  - `tests/test_sync_removed.py::test_only_the_collection_removal_renumbers_memberships`
  - `tests/test_sync_removed.py::test_the_last_member_removed_renumbers_nothing_in_its_playlist`
  - `tests/test_sync_removed.py::test_the_removal_writes_no_beat_grid_and_no_tempo`
  - ... and 2 more, see the JSON sidecar

Old text:

```
        renumber_memberships(self.db, self.renumbered)

```

New text:

```
(empty)
```

### `r1890.P11_process_name_typed_in_the_writer`

rb_writer, no longer exempt, compares the running list against a typed process name instead of the shared list

- File: `src/cratekit/core/rb_writer.py`
- Source: `r1890.json`, row `P11_process_name_typed_in_the_writer`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_process_guard.py`
- Collected: 12 against a baseline of 12
- Kills: 1 (killed)
- Killed:
  - `tests/test_process_guard.py::test_no_module_hardcodes_a_rekordbox_process_name_outside_the_one_list`

Old text:

```
    running = rekordbox_processes_running()
    if running:

```

New text:

```
    running = rekordbox_processes_running()
    if running in ("rekordbox", "rekordboxAgent") or running:

```

### `r239-a.A1_probe_to_true`

open_db answers every unnamed open with the key on, the old default, instead of asking the file

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A1_probe_to_true`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`
- Collected: 706 against a baseline of 706
- Kills: 122 (killed)
- Killed:
  - `tests/test_adopt_collection.py::test_the_database_file_is_byte_identical_after_a_full_read`
  - `tests/test_adopt_collection.py::test_the_reader_never_opens_the_database_for_writing`
  - `tests/test_adopt_collection.py::test_the_reader_yields_the_rows_the_database_holds`
  - `tests/test_adopt_collection.py::test_two_reads_in_one_process_open_the_database_once`
  - `tests/test_deletion.py::test_delete_review_abort_moves_nothing`
  - `tests/test_deletion.py::test_delete_review_exits_ok_after_the_recorded_decision`
  - `tests/test_deletion.py::test_delete_review_first_run_confirmed_reports_ok_and_trashes_nothing`
  - `tests/test_deletion.py::test_delete_review_honours_a_reject_recorded_before_the_gate`
  - `tests/test_deletion.py::test_delete_review_prints_the_baseline_to_a_person_not_only_to_json`
  - `tests/test_deletion.py::test_delete_review_refuses_an_inline_answer_and_does_not_record_it`
  - `tests/test_deletion.py::test_delete_review_refuses_at_its_explicit_gate`
  - `tests/test_deletion.py::test_delete_review_says_on_the_refusal_that_a_first_run_accepted_history`
  - `tests/test_metadata_cli.py::test_a_corrupt_vocal_calibration_refuses_through_the_verb_and_writes_nothing`
  - `tests/test_metadata_cli.py::test_a_library_with_no_tag_category_refuses_through_the_verb`
  - `tests/test_metadata_cli.py::test_a_plan_only_run_leaves_no_record`
  - ... and 107 more, see the JSON sidecar

Old text:

```
    if unlock is None:
        unlock = unlock_needed(target)

```

New text:

```
    if unlock is None:
        unlock = True

```

### `r239-a.A2_probe_to_false`

open_db answers every unnamed open with the key off, the constant the five verb sites used to pass

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A2_probe_to_false`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`
- Collected: 706 against a baseline of 706
- Kills: 7 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_a_snapshot_check_that_names_no_key_verifies_either_kind[encrypted]`
  - `tests/test_rb_writer_db.py::test_an_open_that_names_no_key_opens_either_kind_of_database[encrypted]`
  - `tests/test_routing_workers.py::test_a_queued_job_runs_its_item_and_the_tree_holds_the_track[rebuild-encrypted]`
  - `tests/test_routing_workers.py::test_a_queued_job_runs_its_item_and_the_tree_holds_the_track[resort-encrypted]`
  - `tests/test_routing_workers.py::test_converge_compares_a_native_tree_on_an_encrypted_library`
  - `tests/test_routing_workers.py::test_the_confirmed_inbox_applies_and_the_declined_one_does_not[encrypted]`
  - `tests/test_routing_workers.py::test_unplaced_reports_the_rows_no_governed_tree_holds[encrypted]`

Old text:

```
    if unlock is None:
        unlock = unlock_needed(target)

```

New text:

```
    if unlock is None:
        unlock = False

```

### `r239-a.A3_probe_removed`

Delete the probe block, so None reaches the binding, which reads it as no key

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A3_probe_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`
- Collected: 706 against a baseline of 706
- Kills: 7 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_a_snapshot_check_that_names_no_key_verifies_either_kind[encrypted]`
  - `tests/test_rb_writer_db.py::test_an_open_that_names_no_key_opens_either_kind_of_database[encrypted]`
  - `tests/test_routing_workers.py::test_a_queued_job_runs_its_item_and_the_tree_holds_the_track[rebuild-encrypted]`
  - `tests/test_routing_workers.py::test_a_queued_job_runs_its_item_and_the_tree_holds_the_track[resort-encrypted]`
  - `tests/test_routing_workers.py::test_converge_compares_a_native_tree_on_an_encrypted_library`
  - `tests/test_routing_workers.py::test_the_confirmed_inbox_applies_and_the_declined_one_does_not[encrypted]`
  - `tests/test_routing_workers.py::test_unplaced_reports_the_rows_no_governed_tree_holds[encrypted]`

Old text:

```
    if unlock is None:
        unlock = unlock_needed(target)

```

New text:

```
(empty)
```

### `r239-a.A4_open_default_true`

open_db's unlock default back to True, so the probe branch never fires for an unnamed open

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A4_open_default_true`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`
- Collected: 706 against a baseline of 706
- Kills: 121 (killed)
- Killed:
  - `tests/test_adopt_collection.py::test_the_database_file_is_byte_identical_after_a_full_read`
  - `tests/test_adopt_collection.py::test_the_reader_never_opens_the_database_for_writing`
  - `tests/test_adopt_collection.py::test_the_reader_yields_the_rows_the_database_holds`
  - `tests/test_adopt_collection.py::test_two_reads_in_one_process_open_the_database_once`
  - `tests/test_deletion.py::test_delete_review_abort_moves_nothing`
  - `tests/test_deletion.py::test_delete_review_exits_ok_after_the_recorded_decision`
  - `tests/test_deletion.py::test_delete_review_first_run_confirmed_reports_ok_and_trashes_nothing`
  - `tests/test_deletion.py::test_delete_review_honours_a_reject_recorded_before_the_gate`
  - `tests/test_deletion.py::test_delete_review_prints_the_baseline_to_a_person_not_only_to_json`
  - `tests/test_deletion.py::test_delete_review_refuses_an_inline_answer_and_does_not_record_it`
  - `tests/test_deletion.py::test_delete_review_refuses_at_its_explicit_gate`
  - `tests/test_deletion.py::test_delete_review_says_on_the_refusal_that_a_first_run_accepted_history`
  - `tests/test_metadata_cli.py::test_a_corrupt_vocal_calibration_refuses_through_the_verb_and_writes_nothing`
  - `tests/test_metadata_cli.py::test_a_library_with_no_tag_category_refuses_through_the_verb`
  - `tests/test_metadata_cli.py::test_a_plan_only_run_leaves_no_record`
  - ... and 106 more, see the JSON sidecar

Old text:

```
    force_cloud_canary: bool = False,
    unlock: bool | None = None,

```

New text:

```
    force_cloud_canary: bool = False,
    unlock: bool | None = True,

```

### `r239-a.A7_needed_always_true`

unlock_needed answers encrypted for every readable file, the U55 row that read zero with no encrypted input

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A7_needed_always_true`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`
- Collected: 706 against a baseline of 706
- Kills: 122 (killed)
- Killed:
  - `tests/test_adopt_collection.py::test_the_database_file_is_byte_identical_after_a_full_read`
  - `tests/test_adopt_collection.py::test_the_reader_never_opens_the_database_for_writing`
  - `tests/test_adopt_collection.py::test_the_reader_yields_the_rows_the_database_holds`
  - `tests/test_adopt_collection.py::test_two_reads_in_one_process_open_the_database_once`
  - `tests/test_deletion.py::test_delete_review_abort_moves_nothing`
  - `tests/test_deletion.py::test_delete_review_exits_ok_after_the_recorded_decision`
  - `tests/test_deletion.py::test_delete_review_first_run_confirmed_reports_ok_and_trashes_nothing`
  - `tests/test_deletion.py::test_delete_review_honours_a_reject_recorded_before_the_gate`
  - `tests/test_deletion.py::test_delete_review_prints_the_baseline_to_a_person_not_only_to_json`
  - `tests/test_deletion.py::test_delete_review_refuses_an_inline_answer_and_does_not_record_it`
  - `tests/test_deletion.py::test_delete_review_refuses_at_its_explicit_gate`
  - `tests/test_deletion.py::test_delete_review_says_on_the_refusal_that_a_first_run_accepted_history`
  - `tests/test_metadata_cli.py::test_a_corrupt_vocal_calibration_refuses_through_the_verb_and_writes_nothing`
  - `tests/test_metadata_cli.py::test_a_library_with_no_tag_category_refuses_through_the_verb`
  - `tests/test_metadata_cli.py::test_a_plan_only_run_leaves_no_record`
  - ... and 107 more, see the JSON sidecar

Old text:

```
            return not handle.read(len(SQLITE_HEADER)).startswith(SQLITE_HEADER)
```

New text:

```
            return True
```

### `r239-a.A8_needed_always_false`

unlock_needed answers plain for every readable file, the other U55 zero row, now with an encrypted input to fail on

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A8_needed_always_false`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`
- Collected: 706 against a baseline of 706
- Kills: 8 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_a_snapshot_check_that_names_no_key_verifies_either_kind[encrypted]`
  - `tests/test_rb_writer_db.py::test_an_encrypted_database_does_not_open_with_the_key_withheld`
  - `tests/test_rb_writer_db.py::test_an_open_that_names_no_key_opens_either_kind_of_database[encrypted]`
  - `tests/test_routing_workers.py::test_a_queued_job_runs_its_item_and_the_tree_holds_the_track[rebuild-encrypted]`
  - `tests/test_routing_workers.py::test_a_queued_job_runs_its_item_and_the_tree_holds_the_track[resort-encrypted]`
  - `tests/test_routing_workers.py::test_converge_compares_a_native_tree_on_an_encrypted_library`
  - `tests/test_routing_workers.py::test_the_confirmed_inbox_applies_and_the_declined_one_does_not[encrypted]`
  - `tests/test_routing_workers.py::test_unplaced_reports_the_rows_no_governed_tree_holds[encrypted]`

Old text:

```
            return not handle.read(len(SQLITE_HEADER)).startswith(SQLITE_HEADER)
```

New text:

```
            return False
```

### `r239-a.A9_header_nearby_value`

The plain header constant to a realistic nearby value, SQLite format 4, so no plain file matches it

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A9_header_nearby_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`
- Collected: 706 against a baseline of 706
- Kills: 122 (killed)
- Killed:
  - `tests/test_adopt_collection.py::test_the_database_file_is_byte_identical_after_a_full_read`
  - `tests/test_adopt_collection.py::test_the_reader_never_opens_the_database_for_writing`
  - `tests/test_adopt_collection.py::test_the_reader_yields_the_rows_the_database_holds`
  - `tests/test_adopt_collection.py::test_two_reads_in_one_process_open_the_database_once`
  - `tests/test_deletion.py::test_delete_review_abort_moves_nothing`
  - `tests/test_deletion.py::test_delete_review_exits_ok_after_the_recorded_decision`
  - `tests/test_deletion.py::test_delete_review_first_run_confirmed_reports_ok_and_trashes_nothing`
  - `tests/test_deletion.py::test_delete_review_honours_a_reject_recorded_before_the_gate`
  - `tests/test_deletion.py::test_delete_review_prints_the_baseline_to_a_person_not_only_to_json`
  - `tests/test_deletion.py::test_delete_review_refuses_an_inline_answer_and_does_not_record_it`
  - `tests/test_deletion.py::test_delete_review_refuses_at_its_explicit_gate`
  - `tests/test_deletion.py::test_delete_review_says_on_the_refusal_that_a_first_run_accepted_history`
  - `tests/test_metadata_cli.py::test_a_corrupt_vocal_calibration_refuses_through_the_verb_and_writes_nothing`
  - `tests/test_metadata_cli.py::test_a_library_with_no_tag_category_refuses_through_the_verb`
  - `tests/test_metadata_cli.py::test_a_plan_only_run_leaves_no_record`
  - ... and 107 more, see the JSON sidecar

Old text:

```
SQLITE_HEADER = b"SQLite format 3"
```

New text:

```
SQLITE_HEADER = b"SQLite format 4"
```

### `r375-c.W1_listener_left_on_the_handle`

commit_witness: never remove the listener, so a handle that outlives the write keeps marking a witness nobody reads

- File: `src/cratekit/core/rb_writer.py`
- Source: `r375-c.json`, row `W1_listener_left_on_the_handle`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_the_commit_witness_leaves_the_handle_as_it_found_it`

Old text:

```
        event.remove(target, "after_commit", witness._mark)
```

New text:

```
        pass
```

### `r375-c.W2_witness_listens_one_event_early`

commit_witness: listen for before_commit, so a transaction refused on its way in is witnessed as landed

- File: `src/cratekit/core/rb_writer.py`
- Source: `r375-c.json`, row `W2_witness_listens_one_event_early`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 2 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_the_commit_witness_does_not_read_a_commit_that_never_landed_as_landed`
  - `tests/test_tree_writer.py::test_the_commit_witness_leaves_the_handle_as_it_found_it`

Old text:

```
    event.listen(target, "after_commit", witness._mark)
    try:
        yield witness
    finally:
        event.remove(target, "after_commit", witness._mark)
```

New text:

```
    event.listen(target, "before_commit", witness._mark)
    try:
        yield witness
    finally:
        event.remove(target, "before_commit", witness._mark)
```

### `r663-a.M10_detail_size_pinned`

the detail's size is written as zero whatever the copy measured

- File: `src/cratekit/core/rb_writer.py`
- Source: `r663-a.json`, row `M10_detail_size_pinned`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`
- Collected: 51 against a baseline of 51
- Kills: 1 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_the_copy_names_a_file_holding_none_of_the_canary_tables`

Old text:

```
        detail={"path": str(source), "size": size, "tables_read": list(CANARY_TABLES)},
```

New text:

```
        detail={"path": str(source), "size": 0, "tables_read": list(CANARY_TABLES)},
```

### `r663-a.M3_unlistable_read_as_empty`

a copy whose tables could not be listed is no longer kept apart from one with none, so the None check is dropped

- File: `src/cratekit/core/rb_writer.py`
- Source: `r663-a.json`, row `M3_unlistable_read_as_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`
- Collected: 51 against a baseline of 51
- Kills: 2 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_a_file_that_is_not_sqlite_at_all_keeps_the_canarys_refusal`
  - `tests/test_paths_resolved.py::test_setup_leaves_a_damaged_library_to_the_notes_and_doctor`

Old text:

```
        if tables is None or tables.intersection(CANARY_TABLES):
```

New text:

```
        if tables and tables.intersection(CANARY_TABLES):
```

### `r663-a.M4_one_canary_table_not_enough`

a copy holding one of the two canary tables is classified as not a library, so schema drift is sent to setup

- File: `src/cratekit/core/rb_writer.py`
- Source: `r663-a.json`, row `M4_one_canary_table_not_enough`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`
- Collected: 51 against a baseline of 51
- Kills: 2 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_a_file_holding_one_canary_table_is_drift_and_keeps_the_canarys_refusal[agentRegistry]`
  - `tests/test_paths_resolved.py::test_a_file_holding_one_canary_table_is_drift_and_keeps_the_canarys_refusal[djmdContent]`

Old text:

```
        if tables is None or tables.intersection(CANARY_TABLES):
```

New text:

```
        if tables is None or tables.issuperset(CANARY_TABLES):
```

### `r663-a.M7_message_drops_the_size`

the empty file's message no longer names the size

- File: `src/cratekit/core/rb_writer.py`
- Source: `r663-a.json`, row `M7_message_drops_the_size`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`
- Collected: 51 against a baseline of 51
- Kills: 3 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_doctor_reports_an_empty_database_path_under_the_same_cause`
  - `tests/test_paths_resolved.py::test_setup_refuses_a_database_path_that_is_not_a_library_and_records_nothing[empty]`
  - `tests/test_paths_resolved.py::test_the_copy_names_an_empty_file_by_its_size_and_its_configured_path`

Old text:

```
        what = "is empty, 0 bytes"
```

New text:

```
        what = "is not a database"
```

### `r663-a.M8_message_names_the_copy`

the message names the temporary copy rather than the configured path

- File: `src/cratekit/core/rb_writer.py`
- Source: `r663-a.json`, row `M8_message_names_the_copy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`
- Collected: 51 against a baseline of 51
- Kills: 5 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_doctor_reports_an_empty_database_path_under_the_same_cause`
  - `tests/test_paths_resolved.py::test_setup_refuses_a_database_path_that_is_not_a_library_and_records_nothing[empty]`
  - `tests/test_paths_resolved.py::test_setup_refuses_a_database_path_that_is_not_a_library_and_records_nothing[foreign]`
  - `tests/test_paths_resolved.py::test_the_copy_names_a_file_holding_none_of_the_canary_tables`
  - `tests/test_paths_resolved.py::test_the_copy_names_an_empty_file_by_its_size_and_its_configured_path`

Old text:

```
        f"the file configured as the rekordbox database, {source}, {what}, so it "
```

New text:

```
        f"the file configured as the rekordbox database, {copied}, {what}, so it "
```

### `r663-a.M9_remedy_restore`

the refusal carries the snapshot restore remedy instead of setup

- File: `src/cratekit/core/rb_writer.py`
- Source: `r663-a.json`, row `M9_remedy_restore`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`
- Collected: 51 against a baseline of 51
- Kills: 3 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_doctor_reports_an_empty_database_path_under_the_same_cause`
  - `tests/test_paths_resolved.py::test_the_copy_names_a_file_holding_none_of_the_canary_tables`
  - `tests/test_paths_resolved.py::test_the_copy_names_an_empty_file_by_its_size_and_its_configured_path`

Old text:

```
        remedy=Remedy.RUN_SETUP,
```

New text:

```
        remedy=Remedy.RESTORE_FROM_SNAPSHOT,
```

### `r746-a.G4_read_back_walks_session_new_only`

assert_created_rows_are_gridless: the R-760 blind spot put back, a flushed creation is never read from SQL

- File: `src/cratekit/core/rb_writer.py`
- Source: `r746-a.json`, row `G4_read_back_walks_session_new_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_guard_completeness.py`, `tests/test_intake_land_native.py`
- Collected: 66 against a baseline of 66
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_an_analysis_value_reaching_the_row_is_refused_from_sql_before_the_commit[sql2-djmdMixerParam]`
  - `tests/test_write_guard_completeness.py::test_a_flushed_creation_is_read_back_from_both_sources`

Old text:

```
    instances = {**_registry_created_instances(db), **pending}
```

New text:

```
    instances = {**pending}
```

### `r746-a.G6_analysis_tables_not_checked`

assert_created_rows_are_gridless: no cue, mixer or file row is looked for on the new content row

- File: `src/cratekit/core/rb_writer.py`
- Source: `r746-a.json`, row `G6_analysis_tables_not_checked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_write_guard_completeness.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_an_analysis_value_reaching_the_row_is_refused_from_sql_before_the_commit[sql2-djmdMixerParam]`

Old text:

```
        if table == CONTENT_TABLE and len(keys) == 1:
```

New text:

```
        if False:
```

### `r746-a.G7_sql_value_check_disarmed`

assert_created_rows_are_gridless: a value read from SQL is never a violation

- File: `src/cratekit/core/rb_writer.py`
- Source: `r746-a.json`, row `G7_sql_value_check_disarmed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_write_guard_completeness.py`, `tests/test_rb_writer_db.py`
- Collected: 22473 against a baseline of 22473
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            if value not in EMPTY_ON_CREATE:
                violations.append(f"{table}.{name} = {value!r}")
```

New text:

```
            if False:
                violations.append(f"{table}.{name} = {value!r}")
```

### `r746-d.G5_content_row_read_back_against_five_not_ten`

assert_created_rows_are_gridless: a content row is held to the playlist tables' five columns, so a key or a rate rides in. Measured again after the key taint test its zero bought

- File: `src/cratekit/core/rb_writer.py`
- Source: `r746-d.json`, row `G5_content_row_read_back_against_five_not_ten`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_write_guard_completeness.py`, `tests/test_rb_writer_guard.py`
- Collected: 22473 against a baseline of 22473
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        policy = CONTENT_ROW_EMPTY_COLUMNS if table == CONTENT_TABLE else GRIDLESS_ON_CREATE_COLUMNS
```

New text:

```
        policy = GRIDLESS_ON_CREATE_COLUMNS
```

### `u185.G1_commit_guard_called`

commit_guarded: drop the foreign folder guard from the commit

- File: `src/cratekit/core/rb_writer.py`
- Source: `u185.json`, row `G1_commit_guard_called`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`
- Collected: 287 against a baseline of 287
- Kills: 13 (killed)
- Killed:
  - `tests/test_foreign_tree.py::test_a_handle_with_no_reading_at_open_refuses_rather_than_assuming_nothing_is_there`
  - `tests/test_foreign_tree.py::test_a_playlist_of_ones_own_moved_into_the_folder_is_refused`
  - `tests/test_foreign_tree.py::test_a_push_that_lands_while_a_handle_is_open_refuses_that_handles_commit`
  - `tests/test_foreign_tree.py::test_a_pushed_playlist_moved_out_of_the_folder_is_refused`
  - `tests/test_foreign_tree.py::test_a_reading_that_failed_at_open_is_kept_as_unread_and_refuses`
  - `tests/test_foreign_tree.py::test_a_second_folder_of_the_name_at_the_top_is_refused`
  - `tests/test_foreign_tree.py::test_a_soft_delete_of_a_pushed_playlist_is_refused_even_where_the_commit_admits_removals`
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[folder-renamed]`
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[membership-added]`
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[membership-rewritten-to-another-owner]`
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[playlist-made-inside]`
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[position-named-at-the-top]`
  - `tests/test_foreign_tree.py::test_raw_sql_into_the_folder_is_seen_by_the_reading_again_from_sql`

Old text:

```
            assert_created_rows_are_gridless(db)
            assert_foreign_untouched(db)
```

New text:

```
            assert_created_rows_are_gridless(db)
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
  - `tests/test_foreign_tree.py::test_a_playlist_of_ones_own_moved_into_the_folder_is_refused`
  - `tests/test_foreign_tree.py::test_a_second_folder_of_the_name_at_the_top_is_refused`
  - `tests/test_foreign_tree.py::test_a_soft_delete_of_a_pushed_playlist_is_refused_even_where_the_commit_admits_removals`
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[folder-renamed]`
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[membership-added]`
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[membership-rewritten-to-another-owner]`
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[playlist-made-inside]`

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

### `u185.G5_reading_at_open`

open_db: keep no reading of the subtree as the handle opens

- File: `src/cratekit/core/rb_writer.py`
- Source: `u185.json`, row `G5_reading_at_open`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`, `tests/test_rb_writer_db.py`
- Collected: 75 against a baseline of 75
- Kills: 20 (killed)
- Killed:
  - `tests/test_foreign_tree.py::test_a_handle_with_no_reading_at_open_refuses_rather_than_assuming_nothing_is_there`
  - `tests/test_foreign_tree.py::test_a_playlist_of_ones_own_moved_into_the_folder_is_refused`
  - `tests/test_foreign_tree.py::test_a_push_that_lands_while_a_handle_is_open_refuses_that_handles_commit`
  - `tests/test_foreign_tree.py::test_a_pushed_playlist_moved_out_of_the_folder_is_refused`
  - `tests/test_foreign_tree.py::test_a_second_folder_of_the_name_at_the_top_is_refused`
  - `tests/test_foreign_tree.py::test_a_write_beside_the_folder_commits_and_leaves_every_row_the_push_wrote`
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[membership-added]`
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[membership-rewritten-to-another-owner]`
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[playlist-made-inside]`
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[position-named-at-the-top]`
  - `tests/test_foreign_tree.py::test_raw_sql_into_the_folder_is_seen_by_the_reading_again_from_sql`
  - `tests/test_foreign_tree.py::test_the_reading_at_open_names_the_push_and_not_a_namesake_below_the_top`
  - `tests/test_rb_writer_db.py::test_a_playlist_creation_commits_because_the_table_is_whitelisted`
  - `tests/test_rb_writer_db.py::test_a_registered_column_write_commits_and_persists`
  - `tests/test_rb_writer_db.py::test_a_registration_widens_the_gate_by_exactly_its_own_fields`
  - ... and 5 more, see the JSON sidecar

Old text:

```
    foreign_tree.remember(db)
    return db
```

New text:

```
    return db
```

### `u211.W4_probe_wrapped_at_commit`

commit: run the binding's commit without the careful probe, so its own walk meets the dying process

- File: `src/cratekit/core/rb_writer.py`
- Source: `u211.json`, row `W4_probe_wrapped_at_commit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_rb_writer_guard.py`, `tests/test_sync_pair.py`
- Collected: 334 against a baseline of 334
- Kills: 20 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`
  - `tests/test_sync_pair.py::test_a_landed_track_is_found_in_the_inbox_playlist_landed_for_the_account`
  - `tests/test_sync_pair.py::test_a_pair_whose_playlist_is_gone_does_not_hold_every_other_pair`
  - `tests/test_sync_pair.py::test_a_skipped_rekordbox_side_is_finished_by_the_next_sync`
  - `tests/test_sync_pair.py::test_a_track_added_on_the_account_only_lands_in_rekordbox_in_place`
  - `tests/test_sync_pair.py::test_a_track_another_account_playlist_landed_is_added_and_never_queued`
  - `tests/test_sync_pair.py::test_a_track_another_account_playlist_landed_with_its_isrc_in_the_row_is_added`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_intake_job_found_owned_is_added`
  - `tests/test_sync_pair.py::test_a_track_held_twice_that_lost_one_copy_is_not_read_as_put_back`
  - `tests/test_sync_pair.py::test_a_track_removed_on_the_account_leaves_the_playlist_and_stays_in_the_collection`
  - `tests/test_sync_pair.py::test_an_account_track_found_by_isrc_is_linked_and_the_link_is_kept`
  - `tests/test_sync_pair.py::test_one_row_landed_in_two_inbox_playlists_is_one_row`
  - `tests/test_sync_pair.py::test_the_first_sync_marks_the_pair_and_adds_only`
  - `tests/test_sync_pair.py::test_the_first_sync_removes_nothing_on_either_side`
  - ... and 5 more, see the JSON sidecar

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
- Collected: 334 against a baseline of 334
- Kills: 76 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_a_rekordbox_running_refusal_still_ends_the_run_as_failed`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`
  - `tests/test_sync_pair.py::test_a_first_sync_with_a_side_skipped_records_no_snapshot_and_stays_first`
  - `tests/test_sync_pair.py::test_a_folder_is_not_a_pair`
  - `tests/test_sync_pair.py::test_a_job_naming_no_playlist_is_named_by_its_account_playlist`
  - `tests/test_sync_pair.py::test_a_label_playlist_is_not_a_pair`
  - `tests/test_sync_pair.py::test_a_landed_track_is_found_in_the_inbox_playlist_landed_for_the_account`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[cache-off]`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[kept]`
  - `tests/test_sync_pair.py::test_a_pair_whose_playlist_is_gone_does_not_hold_every_other_pair`
  - `tests/test_sync_pair.py::test_a_plan_with_every_landing_record_readable_warns_nothing_of_them`
  - `tests/test_sync_pair.py::test_a_playlist_under_one_of_cratekits_trees_is_not_a_pair`
  - `tests/test_sync_pair.py::test_a_rekordbox_change_between_the_gates_and_the_write_refuses_as_stale`
  - `tests/test_sync_pair.py::test_a_rekordbox_row_with_no_isrc_column_is_matched_on_its_files_isrc`
  - ... and 61 more, see the JSON sidecar

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

### `u267.M10_done_reading_leaks_own`

done_reading: never close a reader's own handle, so every reader of the run that answers a gate leaks one

- File: `src/cratekit/core/rb_writer.py`
- Source: `u267.json`, row `M10_done_reading_leaks_own`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_organize.py`
- Collected: 111 against a baseline of 111
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_a_reader_with_no_shared_read_closes_its_own_handle`
  - `tests/test_organize_one_read.py::test_the_applying_run_opens_exactly_as_it_did`
  - `tests/test_organize_one_read.py::test_the_report_opens_the_database_once_and_closes_it_once`

Old text:

```
    if shared is None:
        close_db(db)
```

New text:

```
    if shared is None:
        pass
```

### `u267.M4_handle_opens_every_time`

SharedRead.handle: open again on every call, keeping the last, so the report pays an open per reader and leaks the rest

- File: `src/cratekit/core/rb_writer.py`
- Source: `u267.json`, row `M4_handle_opens_every_time`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_organize_inspiration.py`, `tests/test_organize_mirror_edits_u204.py`
- Collected: 89 against a baseline of 89
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_report_reads_inspiration_twice_through_one_handle_and_locks_nothing_meanwhile`
  - `tests/test_organize_one_read.py::test_a_failure_nobody_expected_still_closes_the_handle`
  - `tests/test_organize_one_read.py::test_a_shared_read_opens_at_its_first_read_and_once`
  - `tests/test_organize_one_read.py::test_a_step_that_refuses_after_the_open_leaves_no_handle_open`
  - `tests/test_organize_one_read.py::test_the_report_opens_the_database_once_and_closes_it_once`
  - `tests/test_organize_one_read.py::test_the_sets_step_reads_inspiration_through_the_one_handle`

Old text:

```
        if self._db is None:
            self._db = open_db(
```

New text:

```
        if True:
            self._db = open_db(
```

### `u267.M5_handle_after_close`

SharedRead.handle: drop the refusal after close, so a closed shared read reopens silently

- File: `src/cratekit/core/rb_writer.py`
- Source: `u267.json`, row `M5_handle_after_close`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`
- Collected: 14 against a baseline of 14
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_a_shared_read_refuses_a_handle_not_its_own_and_a_read_after_close`

Old text:

```
        if self._closed:
            raise _defect("a read handle was asked of a shared read that was already closed")
```

New text:

```
        if False:
            raise _defect("a read handle was asked of a shared read that was already closed")
```

### `u267.M6_release_keeps_rows`

SharedRead.release: keep the identity map, so the next reader takes a row an earlier reader loaded as the row the database holds now

- File: `src/cratekit/core/rb_writer.py`
- Source: `u267.json`, row `M6_release_keeps_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_organize.py`, `tests/test_organize_inspiration.py`
- Collected: 149 against a baseline of 149
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

### `u267.M7_release_any_handle`

SharedRead.release: drop the refusal of a handle that is not its own

- File: `src/cratekit/core/rb_writer.py`
- Source: `u267.json`, row `M7_release_any_handle`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`
- Collected: 14 against a baseline of 14
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_a_shared_read_refuses_a_handle_not_its_own_and_a_read_after_close`

Old text:

```
        if db is not self._db:
            raise _defect("a handle that is not the shared read's own was released through it")
```

New text:

```
        if False:
            raise _defect("a handle that is not the shared read's own was released through it")
```

### `u267.M8_close_closes_nothing`

SharedRead.close: forget the handle without close_db, so its engine and pooled connection stay open

- File: `src/cratekit/core/rb_writer.py`
- Source: `u267.json`, row `M8_close_closes_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_organize.py`
- Collected: 111 against a baseline of 111
- Kills: 5 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_a_failure_nobody_expected_still_closes_the_handle`
  - `tests/test_organize_one_read.py::test_a_shared_read_opens_at_its_first_read_and_once`
  - `tests/test_organize_one_read.py::test_a_step_that_refuses_after_the_open_leaves_no_handle_open`
  - `tests/test_organize_one_read.py::test_the_report_opens_the_database_once_and_closes_it_once`
  - `tests/test_organize_one_read.py::test_the_sets_step_reads_inspiration_through_the_one_handle`

Old text:

```
        if db is not None:
            close_db(db)
```

New text:

```
        if db is not None:
            pass
```

### `u267.M9_done_reading_closes_shared`

done_reading: close the handle whatever its owner, so the first reader closes the shared handle under the rest

- File: `src/cratekit/core/rb_writer.py`
- Source: `u267.json`, row `M9_done_reading_closes_shared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_organize.py`, `tests/test_organize_inspiration.py`
- Collected: 149 against a baseline of 149
- Kills: 60 (killed)
- Killed:
  - `tests/test_organize.py::test_a_label_playlist_is_the_label_steps_and_a_set_the_archives`
  - `tests/test_organize.py::test_a_mark_put_back_is_no_mark_and_the_playlist_stays`
  - `tests/test_organize.py::test_a_marked_playlist_already_in_a_folder_is_left_where_it_is[False]`
  - `tests/test_organize.py::test_a_marked_playlist_already_in_a_folder_is_left_where_it_is[True]`
  - `tests/test_organize.py::test_a_marked_playlist_at_the_root_moves_into_its_year_folder`
  - `tests/test_organize.py::test_a_missing_year_folder_is_created_once_and_reused`
  - `tests/test_organize.py::test_a_playlist_of_the_sets_name_outside_inspiration_or_removed_proves_nothing`
  - `tests/test_organize.py::test_a_playlist_of_yours_already_in_a_folder_of_yours_is_not_listed`
  - `tests/test_organize.py::test_a_prefixed_playlist_no_sync_recorded_is_still_filed_in_mine`
  - `tests/test_organize.py::test_a_push_stamped_with_the_zero_date_reads_as_no_push_at_all_west_of_utc`
  - `tests/test_organize.py::test_a_second_run_after_a_full_apply_plans_nothing`
  - `tests/test_organize.py::test_a_set_already_prefixed_in_its_downloaded_sets_folder_plans_nothing`
  - `tests/test_organize.py::test_a_set_archived_by_its_inspiration_proof_stays_archived_once_that_playlist_goes`
  - `tests/test_organize.py::test_a_set_found_prefixed_by_the_migration_is_still_filed_by_the_archive`
  - `tests/test_organize.py::test_a_set_in_its_folder_with_its_built_title_is_taken_and_not_moved`
  - ... and 45 more, see the JSON sidecar

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

### `u27-round-8-independent.W2_composite_wrong_file`

COMPOSITE for W2: the canary names a file that is not the one it opened

- File: `src/cratekit/core/rb_writer.py`
- Source: `u27-round-8-independent.json`, row `W2_composite_wrong_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_metadata_policy.py`, `tests/test_process_guard.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 22473 against a baseline of 22473
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        named = path if path is not None else handle_path(db)
```

New text:

```
        named = (str(path) + "-not-this-file") if path is not None else handle_path(db)
```

### `u27-round-8-independent.W3_canary_no_name_the_database`

Drop the name_the_database hand-off in the canary, so a chmod 000 database is unclassifiable

- File: `src/cratekit/core/rb_writer.py`
- Source: `u27-round-8-independent.json`, row `W3_canary_no_name_the_database`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_metadata_policy.py`, `tests/test_process_guard.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 22473 against a baseline of 22473
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if named is not None:
            name_the_database(exc, named)
```

New text:

```
(empty)
```

### `u27-round-8-independent.W5_canary_message_no_path`

Reword the canary refusal so its sentence no longer names the database file

- File: `src/cratekit/core/rb_writer.py`
- Source: `u27-round-8-independent.json`, row `W5_canary_message_no_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_metadata_policy.py`, `tests/test_process_guard.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 22473 against a baseline of 22473
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            f"the rekordbox database{where} opened but could not be read as "
            f"expected: {exc}",
```

New text:

```
            f"the rekordbox database could not be read as expected after it "
            f"opened: {exc}",
```

### `u285.M1_seam_installs`

open_db: drop the install, so a handle reads with the binding's own conversion and a zero dated push fails its row west of UTC

- File: `src/cratekit/core/rb_writer.py`
- Source: `u285.json`, row `M1_seam_installs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_dates.py`, `tests/test_organize.py`, `tests/test_rebuild.py`, `tests/test_foreign_tree.py`
- Collected: 288 against a baseline of 288
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize.py::test_a_push_stamped_with_the_zero_date_reads_as_no_push_at_all_west_of_utc`
  - `tests/test_rb_dates.py::test_a_commit_leaves_the_pushed_nodes_xml_timestamps_and_still_syncs_its_own[EST5EDT,M3.2.0,M11.1.0]`
  - `tests/test_rb_dates.py::test_a_commit_leaves_the_pushed_nodes_xml_timestamps_and_still_syncs_its_own[JST-9]`
  - `tests/test_rb_dates.py::test_a_commit_leaves_the_pushed_nodes_xml_timestamps_and_still_syncs_its_own[UTC0]`
  - `tests/test_rb_dates.py::test_a_handle_reads_the_whole_tree_over_a_zero_dated_push_and_writes_nothing`
  - `tests/test_rb_dates.py::test_the_open_seam_installs_the_wrapper`

Old text:

```
    rb_dates.install()

```

New text:

```
    pass

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

### `u59.M9_column_repointed`

Point SOFT_DELETE_COLUMN at a neighbouring bookkeeping column

- File: `src/cratekit/core/rb_writer.py`
- Source: `u59.json`, row `M9_column_repointed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`, `tests/test_process_guard.py`, `tests/test_queued_resume_contract.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 2716 against a baseline of 2716
- Kills: 176 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_a_library_of_tombstones_and_an_empty_one_both_census_to_nothing`
  - `tests/test_adopt_apply_cli.py::test_the_census_is_the_library_and_every_row_of_it_is_carried`
  - `tests/test_adopt_collection.py::test_a_null_location_and_a_null_genre_are_empty_strings_not_none`
  - `tests/test_adopt_collection.py::test_a_tombstone_is_carried_rather_than_dropped`
  - `tests/test_adopt_collection.py::test_every_field_comes_off_the_row_it_belongs_to`
  - `tests/test_adopt_collection.py::test_the_reader_yields_the_rows_the_database_holds`
  - `tests/test_adopt_workers.py::test_a_configured_volume_rewrite_reaches_the_census`
  - `tests/test_adopt_workers.py::test_a_plan_with_nothing_applicable_queues_nothing`
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item[tombstoned]`
  - `tests/test_adopt_workers.py::test_an_empty_library_queues_nothing_and_says_so[True]`
  - `tests/test_deferred_routing.py::test_content_rows_reads_the_soft_delete_marker_off_the_row`
  - `tests/test_deletion.py::test_a_binding_that_cannot_say_how_many_memberships_it_holds_refuses`
  - `tests/test_deletion.py::test_a_collection_row_with_no_id_reaches_the_pass_as_unidentifiable`
  - `tests/test_deletion.py::test_a_confirmed_ambiguous_row_is_refused_at_move_time_too`
  - `tests/test_deletion.py::test_a_confirmed_file_is_trashed_and_leaves_a_tombstone`
  - ... and 161 more, see the JSON sidecar

Old text:

```
SOFT_DELETE_COLUMN = "rb_local_deleted"
```

New text:

```
SOFT_DELETE_COLUMN = "rb_local_synced"
```

### `u162.R10_latest_verb`

latest: match a record by key alone, so another verb's rehearsal is compared

- File: `src/cratekit/core/rehearsal.py`
- Source: `u162.json`, row `R10_latest_verb`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_two_areas_are_apart_and_copy_library_state_only`

Old text:

```
            and body.get("verb") == verb

```

New text:

```
(empty)
```

### `u162.R1_area_exists`

open_area: drop the refusal of an area that already exists, so one area is shared

- File: `src/cratekit/core/rehearsal.py`
- Source: `u162.json`, row `R1_area_exists`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_two_areas_are_apart_and_copy_library_state_only`

Old text:

```
        if path.exists():
```

New text:

```
        if False:
```

### `u162.R2_rekordbox_closed`

open_area: drop the closed rekordbox check before the copy

- File: `src/cratekit/core/rehearsal.py`
- Source: `u162.json`, row `R2_rekordbox_closed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_empty_staging_rehearses_nothing_and_rekordbox_refuses`

Old text:

```
    rb_writer.assert_rekordbox_closed("copying the database for a rehearsal")

```

New text:

```
(empty)
```

### `u162.R3_clone_is_a_link`

clone: a hard link where the volume does not clone

- File: `src/cratekit/core/rehearsal.py`
- Source: `u162.json`, row `R3_clone_is_a_link`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_clone_is_never_a_hard_link_and_the_plan_lines_name_every_leaf`

Old text:

```
    shutil.copy2(source, destination)
```

New text:

```
    os.link(source, destination)
```

### `u162.R4_snapshots_copied`

_NOT_COPIED: copy the snapshots directory into the area

- File: `src/cratekit/core/rehearsal.py`
- Source: `u162.json`, row `R4_snapshots_copied`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_two_areas_are_apart_and_copy_library_state_only`

Old text:

```
        "snapshots",

```

New text:

```
(empty)
```

### `u162.R5_locks_copied`

_copy_library_state: copy lock files into the area

- File: `src/cratekit/core/rehearsal.py`
- Source: `u162.json`, row `R5_locks_copied`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_two_areas_are_apart_and_copy_library_state_only`

Old text:

```
        if entry.key in _NOT_COPIED or entry.key.endswith("_lock"):
```

New text:

```
        if entry.key in _NOT_COPIED:
```

### `u162.R7_witness_database`

assert_untouched: drop the live database hash comparison

- File: `src/cratekit/core/rehearsal.py`
- Source: `u162.json`, row `R7_witness_database`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_the_witness_refuses_a_live_change`

Old text:

```
    if _hashes(before.database) != before.hashes:
```

New text:

```
    if False:
```

### `u162.R8_witness_folders`

assert_untouched: drop the live folder listing comparison

- File: `src/cratekit/core/rehearsal.py`
- Source: `u162.json`, row `R8_witness_folders`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_another_year_s_batch_is_refused`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_the_live_library_is_refused`
  - `tests/test_intake_land_rehearse.py::test_the_witness_refuses_a_live_change`

Old text:

```
        if _listed(Path(folder)) != listing:
```

New text:

```
        if False:
```

### `u162.R9_latest_key`

latest: match a record by verb alone, so another batch's rehearsal is compared

- File: `src/cratekit/core/rehearsal.py`
- Source: `u162.json`, row `R9_latest_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_live_plan_names_its_own_batch_s_rehearsal_and_the_lines`
  - `tests/test_intake_land_rehearse.py::test_two_areas_are_apart_and_copy_library_state_only`

Old text:

```
            and body.get("key") == dict(key)

```

New text:

```
(empty)
```

### `u188.M14_mapped_in_given_order`

rehearsal.mapped: apply the pairs in the order given, so a scratch spelling holding another's is half mapped

- File: `src/cratekit/core/rehearsal.py`
- Source: `u188.json`, row `M14_mapped_in_given_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_mapped_applies_the_longest_spelling_first_and_the_refusal_names_each_field_once`

Old text:

```
            key=lambda pair: len(pair[0]),
            reverse=True,
```

New text:

```
            key=lambda pair: 0,
            reverse=True,
```

### `u188.M15_mapped_shortest_first`

rehearsal.mapped: shortest scratch spelling first

- File: `src/cratekit/core/rehearsal.py`
- Source: `u188.json`, row `M15_mapped_shortest_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_mapped_applies_the_longest_spelling_first_and_the_refusal_names_each_field_once`

Old text:

```
            key=lambda pair: len(pair[0]),
            reverse=True,
```

New text:

```
            key=lambda pair: len(pair[0]),
            reverse=False,
```

### `u188.M16_mapped_by_live_length`

rehearsal.mapped: order by the live spelling's length rather than the scratch one's

- File: `src/cratekit/core/rehearsal.py`
- Source: `u188.json`, row `M16_mapped_by_live_length`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_mapped_applies_the_longest_spelling_first_and_the_refusal_names_each_field_once`

Old text:

```
            key=lambda pair: len(pair[0]),
```

New text:

```
            key=lambda pair: len(pair[1]),
```

### `u188.M17_empty_scratch_kept`

rehearsal.mapped: keep an empty scratch spelling, which inserts the live one between every character

- File: `src/cratekit/core/rehearsal.py`
- Source: `u188.json`, row `M17_empty_scratch_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_mapped_applies_the_longest_spelling_first_and_the_refusal_names_each_field_once`

Old text:

```
            ((scratch, live) for scratch, live in replacements if scratch),
```

New text:

```
            ((scratch, live) for scratch, live in replacements),
```

### `u206.M20_rehearsal_cache_not_kept_live`

rehearsal.redirected: do not point the ISRC cache at the live directory, so a rehearsal's answers are thrown away

- File: `src/cratekit/core/rehearsal.py`
- Source: `u206.json`, row `M20_rehearsal_cache_not_kept_live`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1130 against a baseline of 1130
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_rehearsal_keeps_the_live_isrc_cache_and_restores_the_environment`

Old text:

```
    os.environ[config.ENV_ISRC_CACHE_DIR] = saved[config.ENV_ISRC_CACHE_DIR] or str(
        config.state_path("isrc_cache").parent
    )
```

New text:

```
    os.environ.pop(config.ENV_ISRC_CACHE_DIR, None)
```

### `r1665.R1_log_not_restored`

restore._file_steps: never write back a restored companion, so the log's rows are lost

- File: `src/cratekit/core/restore.py`
- Source: `r1665.json`, row `R1_log_not_restored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 4 (killed)
- Killed:
  - `tests/test_restore.py::test_only_the_companion_the_inventory_declares_restored_is_written_back`
  - `tests/test_restore.py::test_round3_a_staged_log_is_counted_as_permanent_growth`
  - `tests/test_restore.py::test_round3_a_volume_between_the_two_rules_is_refused`
  - `tests/test_snapshot_wal_r1665.py::test_a_capture_taken_while_a_handle_holds_the_log_restores_what_it_recorded`

Old text:

```
        if entry.source in restored_companions:
            if entry.captured is not None:
```

New text:

```
        if entry.source in restored_companions:
            if False:
```

### `u27-restore-cli-independent.X6_the_rekordbox_guard_itself_is_neutered`

What the process-lister zeros DO leave held: make the restore engine's rekordbox-closed assertion return without asking. Paired with I_A6 and I_A7, which stopped threading that guard's injected seam and killed nothing

- File: `src/cratekit/core/restore.py`
- Source: `u27-restore-cli-independent.json`, row `X6_the_rekordbox_guard_itself_is_neutered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_a_restore_refuses_while_rekordbox_holds_the_database`

Old text:

```
    running = processes.rekordbox_processes_running(lister=process_lister)
    if not running:
        return
```

New text:

```
    running = processes.rekordbox_processes_running(lister=process_lister)
    if running or not running:
        return
```

