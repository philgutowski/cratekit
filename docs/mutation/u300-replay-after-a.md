# Mutation table: u300-replay-after-a

Measured by `scripts/mutate.py` on 2026-11-23 00:11 UTC, branch `HEAD` at `056cd877`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 153.

Full baseline: measured by this driver (the battery's verdict was not read: it is for commit `8b809bd22ca3`, and this tree is at `056cd877e91d`).

Subset baselines: 35, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `/tmp/kf.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `a32.A6_policy_left_behind` | `src/cratekit/core/rb_tables.py` | maintainer | 2 file(s) | 112 | 4 | killed |
| `a32.V4_policy_unrestricted` | `src/cratekit/core/rb_tables.py` | user | 1 file(s) | 59 | 1 | killed |
| `r1665.W2_failed_copy_passes` | `src/cratekit/core/rb_copies.py` | user | 7 file(s) | 327 | 1 | killed |
| `r1665.W4_quick_check_ignored` | `src/cratekit/core/rb_copies.py` | user | 7 file(s) | 327 | 1 | killed |
| `r1677.R1_raise_after_copy` | `src/cratekit/core/rb_copies.py` | user | 4 file(s) | 134 | 1 | killed |
| `r1677.R5_file_set_drops_playlist` | `src/cratekit/core/rb_copies.py` | user | 5 file(s) | 278 | 2 | killed |
| `r1830.M10_planned_number_not_asked` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 74 | 1 | killed |
| `r1830.M11_held_object_left_stale` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 74 | 1 | killed |
| `r1830.M13_planned_rows_admitted_unjudged` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 286 | 1 | killed |
| `r1830.M14_other_columns_not_compared` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 286 | 1 | killed |
| `r1830.M15_number_not_compared` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 286 | 1 | killed |
| `r1830.M16_marker_change_not_compared` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 286 | 1 | killed |
| `r1830.M17_positions_never_read` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 74 | 15 | killed |
| `r1830.M1_tie_counted_as_below` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 212 | 1 | killed |
| `r1830.M21_record_omits_the_rows` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 74 | 1 | killed |
| `r1830.M2_marked_removed_row_counted` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 286 | 3 | killed |
| `r1830.M3_marked_survivor_moved` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 286 | 1 | killed |
| `r1830.M4_one_place_whatever_removed` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 286 | 2 | killed |
| `r1830.M5_any_playlist_counts` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 286 | 16 | killed |
| `r1830.M6_prepare_plans_no_renumbering` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 74 | 17 | killed |
| `r1830.M7_commit_skips_the_renumbering` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 74 | 17 | killed |
| `r1830.M8_renumbering_stamps_updated_at` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 74 | 15 | killed |
| `r1830.M9_moved_row_not_refused` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 74 | 1 | killed |
| `r235-b.M22_nested_namesake_is_a_root` | `src/cratekit/core/rb_nodes.py` | user | 1 file(s) | 40 | 2 | killed |
| `r235-b.M23_playlist_is_a_root` | `src/cratekit/core/rb_nodes.py` | user | 1 file(s) | 40 | 1 | killed |
| `r239-a.A1_probe_to_true` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 706 | 124 | killed |
| `r239-a.A2_probe_to_false` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 706 | 7 | killed |
| `r239-a.A3_probe_removed` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 706 | 7 | killed |
| `r239-a.A4_open_default_true` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 706 | 123 | killed |
| `r239-a.A7_needed_always_true` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 706 | 124 | killed |
| `r239-a.A8_needed_always_false` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 706 | 8 | killed |
| `r239-a.A9_header_nearby_value` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 706 | 124 | killed |
| `r372-a.A12_separator_kept` | `src/cratekit/core/rb_copies.py` | user | 3 file(s) | 494 | 7 | killed |
| `r375-c.W1_listener_left_on_the_handle` | `src/cratekit/core/rb_writer.py` | maintainer | 2 file(s) | 87 | 1 | killed |
| `r375-c.W2_witness_listens_one_event_early` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 87 | 2 | killed |
| `r663-a.M10_detail_size_pinned` | `src/cratekit/core/rb_writer.py` | maintainer | 1 file(s) | 51 | 1 | killed |
| `r663-a.M3_unlistable_read_as_empty` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 51 | 2 | killed |
| `r663-a.M4_one_canary_table_not_enough` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 51 | 2 | killed |
| `r663-a.M5_failed_listing_returns_empty_set` | `src/cratekit/core/rb_copies.py` | user | 1 file(s) | 51 | 2 | killed |
| `r663-a.M7_message_drops_the_size` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 51 | 3 | killed |
| `r663-a.M8_message_names_the_copy` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 51 | 5 | killed |
| `r663-a.M9_remedy_restore` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 51 | 3 | killed |
| `r746-a.G1_asking_for_any_table_is_not_refused` | `src/cratekit/core/rb_changes.py` | user | 2 file(s) | 234 | 5 | killed |
| `r746-a.G2_admitted_row_judged_without_the_column_policy` | `src/cratekit/core/rb_changes.py` | user | 2 file(s) | 234 | 11 | killed |
| `r746-a.G3_content_row_admitted_without_asking` | `src/cratekit/core/rb_changes.py` | user | 3 file(s) | 293 | 5 | killed |
| `r746-a.G4_read_back_walks_session_new_only` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 81 | 2 | killed |
| `r746-a.G6_analysis_tables_not_checked` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 81 | 1 | killed |
| `r746-a.G8_key_dropped_from_the_content_policy` | `src/cratekit/core/rb_tables.py` | user | 2 file(s) | 233 | collection error | collect-error |
| `r758-a.W2_asked_table_not_held_to_the_set` | `src/cratekit/core/rb_changes.py` | user | 2 file(s) | 324 | 33 | killed |
| `r758-a.W3_ask_outside_the_set_not_refused` | `src/cratekit/core/rb_changes.py` | user | 2 file(s) | 324 | 33 | killed |
| `r923.N18_policy_owns_the_fields` | `src/cratekit/core/rb_tables.py` | user | 41 file(s) | 3914 | 1 | killed |
| `r923.N19_default_is_an_analysis_column` | `src/cratekit/core/rb_tables.py` | user | 41 file(s) | 3914 | 45 | killed |
| `u111-a.A1_folder_refused` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 253 | 1 | killed |
| `u111-a.A6_playlist_not_removable` | `src/cratekit/core/rb_tables.py` | user | 2 file(s) | 254 | collection error | collect-error |
| `u111-a.A7_content_compared` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 253 | 1 | killed |
| `u111-b.A10_renumber_scoped` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 253 | 1 | killed |
| `u111-b.A12_removed_keeps_no_live` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 253 | 2 | killed |
| `u111-b.A13_confinement_raises` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 253 | 2 | killed |
| `u111-b.A8_membership_owner` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 253 | 2 | killed |
| `u111-b.A9_planned_move_made` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 253 | 4 | killed |
| `u115.F3_file_id_policy_fill_if_empty` | `src/cratekit/core/rb_tables.py` | user | 41 file(s) | 3914 | 3 | killed |
| `u115.F4_binding_limit_coefficient` | `src/cratekit/core/rb_tables.py` | maintainer | 41 file(s) | 3914 | 1 | killed |
| `u127.W1_writable_always` | `src/cratekit/core/rb_nodes.py` | user | 52 file(s) | 4352 | 1 | killed |
| `u127.W2_writable_reason_drift` | `src/cratekit/core/rb_nodes.py` | user | 52 file(s) | 4352 | 1 | killed |
| `u163.W15_lookup_policy` | `src/cratekit/core/rb_changes.py` | user | 3 file(s) | 294 | 5 | killed |
| `u163.W16_admittable_key` | `src/cratekit/core/rb_tables.py` | user | 3 file(s) | 294 | 2 | killed |
| `u185.G1_commit_guard_called` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 287 | 13 | killed |
| `u185.G2_unread_refuses` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 31 | 2 | killed |
| `u185.G3_pending_leg` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 31 | 7 | killed |
| `u185.G4_second_reading_leg` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 31 | 2 | killed |
| `u185.G5_reading_at_open` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 75 | 20 | killed |
| `u211.W1_writer_falls_back` | `src/cratekit/core/rb_probes.py` | user | 3 file(s) | 273 | 15 | killed |
| `u211.W3_strict_at_commit` | `src/cratekit/core/rb_probes.py` | user | 2 file(s) | 261 | 2 | killed |
| `u211.W4_probe_wrapped_at_commit` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 336 | 20 | killed |
| `u211.W5_probe_wrapped_at_open` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 336 | 76 | killed |
| `u211.W7_writer_unconfirmed_with_nothing_read` | `src/cratekit/core/rb_probes.py` | user | 3 file(s) | 273 | 2 | killed |
| `u267.M10_done_reading_leaks_own` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 115 | 3 | killed |
| `u267.M4_handle_opens_every_time` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 92 | 6 | killed |
| `u267.M5_handle_after_close` | `src/cratekit/core/rb_writer.py` | maintainer | 1 file(s) | 15 | 1 | killed |
| `u267.M6_release_keeps_rows` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 154 | 1 | killed |
| `u267.M7_release_any_handle` | `src/cratekit/core/rb_writer.py` | maintainer | 1 file(s) | 15 | 1 | killed |
| `u267.M8_close_closes_nothing` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 115 | 5 | killed |
| `u267.M9_done_reading_closes_shared` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 154 | 64 | killed |
| `u285.M1_seam_installs` | `src/cratekit/core/rb_writer.py` | user | 4 file(s) | 289 | 6 | killed |
| `u288.M10_changed_rows` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 286 | 7 | killed |
| `u288.M11_added_rows` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 286 | 2 | killed |
| `u288.M12_still_names` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 286 | 1 | killed |
| `u288.M13_counter_forward` | `src/cratekit/core/rb_removal.py` | maintainer | 2 file(s) | 286 | 1 | killed |
| `u288.M14_confinement_not_called` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 74 | 2 | killed |
| `u288.M15_append_past_highest` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 96 | 2 | killed |
| `u288.M1_delete_admitted_by_any_name` | `src/cratekit/core/rb_changes.py` | user | 2 file(s) | 286 | 2 | killed |
| `u288.M2_deletable_set_unbounded` | `src/cratekit/core/rb_changes.py` | user | 2 file(s) | 286 | 1 | killed |
| `u288.M3_unmeasured_tables_skipped` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 74 | 3 | killed |
| `u288.M4_target_id_not_asked` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 74 | 1 | killed |
| `u288.M5_prepare_liveness` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 74 | 1 | killed |
| `u288.M6_prepare_unmeasured_refusal` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 74 | 3 | killed |
| `u288.M7_prepare_identity` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 74 | 1 | killed |
| `u288.M8_memberships_kept` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 74 | 19 | killed |
| `u288.M9_whose_row_disappeared` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 286 | 1 | killed |
| `u59.M9_column_repointed` | `src/cratekit/core/rb_writer.py` | user | 22 file(s) | 2759 | 173 | killed |
| `r1665-b.C1_w5_composite` | `src/cratekit/core/rb_copies.py` | user | 7 file(s) | 327 | 2 | killed |
| `r1665.W1_check_opens_the_capture` | `src/cratekit/core/rb_copies.py` | user | 7 file(s) | 327 | 21 | killed |
| `r1665.W3_no_release_of_the_copy` | `src/cratekit/core/rb_copies.py` | maintainer | 1 file(s) | 15 | 1 | killed |
| `r1665.W6_refused_open_passes` | `src/cratekit/core/rb_copies.py` | user | 7 file(s) | 327 | 2 | killed |
| `r1677.R3_copied_never_set` | `src/cratekit/core/rb_copies.py` | user | 4 file(s) | 134 | 1 | killed |
| `r1830.M23_unreadable_marker_passed_over` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 74 | 1 | killed |
| `r372-a.A10_copy_left_behind` | `src/cratekit/core/rb_copies.py` | maintainer | 3 file(s) | 494 | 15 | killed |
| `r372-a.A11_copy_under_a_running_application` | `src/cratekit/core/rb_copies.py` | maintainer | 3 file(s) | 494 | 1 | killed |
| `r663-a.M1_empty_not_refused_before_open` | `src/cratekit/core/rb_copies.py` | user | 1 file(s) | 51 | 4 | killed |
| `r663-a.M6_listing_opened_with_the_key_always` | `src/cratekit/core/rb_copies.py` | user | 1 file(s) | 51 | 2 | killed |
| `r663-b.M2_every_open_refusal_classified` | `src/cratekit/core/rb_copies.py` | user | 1 file(s) | 51 | 1 | killed |
| `r758-a.W1_marker_not_judged` | `src/cratekit/core/rb_changes.py` | user | 2 file(s) | 324 | 75 | killed |
| `r758-a.W7_removed_row_marked_again` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 324 | 1 | killed |
| `u111-a.A3_parent_not_folder` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 253 | 1 | killed |
| `u111-a.A4_memberships_unmarked` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 253 | 2 | killed |
| `u111-a.A5_node_unmarked` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 253 | 2 | killed |

## Row definitions

### `a32.A6_policy_left_behind`

The commit's policies are left registered after the body, in the shared context manager

- File: `src/cratekit/core/rb_tables.py`
- Source: `a32.json`, row `A6_policy_left_behind`
- Moved: the same text, now in src/cratekit/core/rb_tables.py, was in src/cratekit/core/rb_writer.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`, `tests/test_repair_rows.py`
- Collected: 112 against a baseline of 112
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
- Moved: the same text, now in src/cratekit/core/rb_tables.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
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

### `r1665.W2_failed_copy_passes`

integrity_ok: a throwaway copy that cannot be made answers True

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1665.json`, row `W2_failed_copy_passes`
- Moved: the same text, now in src/cratekit/core/rb_copies.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 327 against a baseline of 327
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_wal_r1665.py::test_a_check_whose_copy_cannot_be_made_has_not_passed`

Old text:

```
            exc,
        )
        return False
```

New text:

```
            exc,
        )
        return True
```

### `r1665.W4_quick_check_ignored`

integrity_ok: answer True whatever quick_check says

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1665.json`, row `W4_quick_check_ignored`
- Moved: the same text, now in src/cratekit/core/rb_copies.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 327 against a baseline of 327
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_wal_r1665.py::test_damage_only_the_consistency_check_sees_fails_the_check`

Old text:

```
                return str(result).lower() == "ok"
```

New text:

```
                return True
```

### `r1677.R1_raise_after_copy`

integrity_ok: raise the copy failure for any OSError, after the copy too, so an open that fails is told as no room

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1677.json`, row `R1_raise_after_copy`
- Moved: the same text, now in src/cratekit/core/rb_copies.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot_wal_r1665.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 134 against a baseline of 134
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_check_room_r1677.py::test_an_open_that_fails_after_the_copy_is_a_failed_check_not_a_copy_failure`

Old text:

```
        if raise_copy_failure and not copied:
```

New text:

```
        if raise_copy_failure:
```

### `r1677.R5_file_set_drops_playlist`

_copy_file_set: copy the companions but not the playlist file, so the measured list and the copied list drift

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1677.json`, row `R5_file_set_drops_playlist`
- Moved: the same text, now in src/cratekit/core/rb_copies.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot_wal_r1665.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`
- Collected: 278 against a baseline of 278
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_snapshot.py::test_the_legacy_playlist_file_travels_with_the_database`
  - `tests/test_snapshot_check_room_r1677.py::test_the_file_set_measured_is_the_one_the_check_copies`

Old text:

```
    for companion in companions:
        if companion.exists():
```

New text:

```
    for companion in companions[:-1]:
        if companion.exists():
```

### `r1830.M10_planned_number_not_asked`

renumber_memberships: write the new number whatever the row holds now

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1830.json`, row `M10_planned_number_not_asked`
- Moved: the same text, now in src/cratekit/core/rb_removal.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_member_that_moved_after_the_prepare_refuses_its_renumbering_with_nothing_written`

Old text:

```
        f'WHERE "ID" = :key AND "{TRACK_NUMBER_COLUMN}" = :before'
```

New text:

```
        f'WHERE "ID" = :key AND :before = :before'
```

### `r1830.M11_held_object_left_stale`

renumber_memberships: leave the session's mapped rows holding the old number

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1830.json`, row `M11_held_object_left_stale`
- Moved: the same text, now in src/cratekit/core/rb_removal.py, was in src/cratekit/core/rb_writer.py
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
- Moved: the same text, now in src/cratekit/core/rb_removal.py, was in src/cratekit/core/rb_writer.py
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
- Moved: the same text, now in src/cratekit/core/rb_removal.py, was in src/cratekit/core/rb_writer.py
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
- Moved: the same text, now in src/cratekit/core/rb_removal.py, was in src/cratekit/core/rb_writer.py
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
- Moved: the same text, now in src/cratekit/core/rb_removal.py, was in src/cratekit/core/rb_writer.py
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
- Moved: the same text, now in src/cratekit/core/rb_removal.py, was in src/cratekit/core/rb_writer.py
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
- Moved: the same text, now in src/cratekit/core/rb_removal.py, was in src/cratekit/core/rb_writer.py
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

### `r1830.M2_marked_removed_row_counted`

renumbered_positions: a removed row marked removed counts, review round one's B1

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1830.json`, row `M2_marked_removed_row_counted`
- Moved: the same text, now in src/cratekit/core/rb_removal.py, was in src/cratekit/core/rb_writer.py
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
- Moved: the same text, now in src/cratekit/core/rb_removal.py, was in src/cratekit/core/rb_writer.py
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
- Moved: the same text, now in src/cratekit/core/rb_removal.py, was in src/cratekit/core/rb_writer.py
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
- Moved: the same text, now in src/cratekit/core/rb_removal.py, was in src/cratekit/core/rb_writer.py
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

### `r1830.M8_renumbering_stamps_updated_at`

renumber_memberships: write updated_at beside TrackNo, a byte rekordbox did not write

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1830.json`, row `M8_renumbering_stamps_updated_at`
- Moved: the same text, now in src/cratekit/core/rb_removal.py, was in src/cratekit/core/rb_writer.py
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
- Moved: the same text, now in src/cratekit/core/rb_removal.py, was in src/cratekit/core/rb_writer.py
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

### `r235-b.M22_nested_namesake_is_a_root`

a folder of the tree's name anywhere in the library is a candidate root

- File: `src/cratekit/core/rb_nodes.py`
- Source: `r235-b.json`, row `M22_nested_namesake_is_a_root`
- Moved: the same text, now in src/cratekit/core/rb_nodes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_a_namesake_nested_under_another_folder_is_not_a_root`
  - `tests/test_cutover_cli.py::test_a_nested_namesake_alone_is_no_root_at_all`

Old text:

```
        if _is_folder(playlist)
        and str(getattr(playlist, "ParentID", "")) in ROOT_PARENT_SENTINELS
```

New text:

```
        if _is_folder(playlist)
```

### `r235-b.M23_playlist_is_a_root`

a playlist of the tree's name under the playlist root is a candidate root

- File: `src/cratekit/core/rb_nodes.py`
- Source: `r235-b.json`, row `M23_playlist_is_a_root`
- Moved: the same text, now in src/cratekit/core/rb_nodes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_a_playlist_of_the_trees_name_is_not_a_root`

Old text:

```
        if _is_folder(playlist)
        and str(getattr(playlist, "ParentID", "")) in ROOT_PARENT_SENTINELS
```

New text:

```
        if str(getattr(playlist, "ParentID", "")) in ROOT_PARENT_SENTINELS
```

### `r239-a.A1_probe_to_true`

open_db answers every unnamed open with the key on, the old default, instead of asking the file

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A1_probe_to_true`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`
- Collected: 706 against a baseline of 706
- Kills: 124 (killed)
- Killed:
  - `tests/test_adopt_collection.py::test_a_dangling_genre_reference_reads_as_no_genre`
  - `tests/test_adopt_collection.py::test_a_row_whose_file_is_absent_is_still_a_row`
  - `tests/test_adopt_collection.py::test_both_composition_forms_come_back_exactly_as_recorded`
  - `tests/test_adopt_collection.py::test_the_database_file_is_byte_identical_after_a_full_read`
  - `tests/test_adopt_collection.py::test_the_reader_never_opens_the_database_for_writing`
  - `tests/test_adopt_collection.py::test_the_reader_yields_the_rows_the_database_holds`
  - `tests/test_adopt_collection.py::test_two_reads_in_one_process_open_the_database_once`
  - `tests/test_deletion.py::test_delete_review_abort_moves_nothing`
  - `tests/test_deletion.py::test_delete_review_exits_ok_after_the_recorded_decision`
  - `tests/test_deletion.py::test_delete_review_first_run_confirmed_reports_ok_and_trashes_nothing`
  - `tests/test_deletion.py::test_delete_review_prints_the_baseline_to_a_person_not_only_to_json`
  - `tests/test_deletion.py::test_delete_review_refuses_an_inline_answer_and_does_not_record_it`
  - `tests/test_deletion.py::test_delete_review_refuses_at_its_explicit_gate`
  - `tests/test_deletion.py::test_delete_review_says_on_the_refusal_that_a_first_run_accepted_history`
  - `tests/test_metadata_cli.py::test_a_corrupt_vocal_calibration_refuses_through_the_verb_and_writes_nothing`
  - ... and 109 more, see the JSON sidecar

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
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_applies_on_an_encrypted_library`
  - `tests/test_routing_workers.py::test_a_queued_rebuild_and_resort_run_on_an_encrypted_library[rebuild]`
  - `tests/test_routing_workers.py::test_a_queued_rebuild_and_resort_run_on_an_encrypted_library[resort]`
  - `tests/test_routing_workers.py::test_converge_compares_a_native_tree_on_an_encrypted_library`
  - `tests/test_routing_workers.py::test_unplaced_compares_on_an_encrypted_library`

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
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_applies_on_an_encrypted_library`
  - `tests/test_routing_workers.py::test_a_queued_rebuild_and_resort_run_on_an_encrypted_library[rebuild]`
  - `tests/test_routing_workers.py::test_a_queued_rebuild_and_resort_run_on_an_encrypted_library[resort]`
  - `tests/test_routing_workers.py::test_converge_compares_a_native_tree_on_an_encrypted_library`
  - `tests/test_routing_workers.py::test_unplaced_compares_on_an_encrypted_library`

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
- Kills: 123 (killed)
- Killed:
  - `tests/test_adopt_collection.py::test_a_dangling_genre_reference_reads_as_no_genre`
  - `tests/test_adopt_collection.py::test_a_row_whose_file_is_absent_is_still_a_row`
  - `tests/test_adopt_collection.py::test_both_composition_forms_come_back_exactly_as_recorded`
  - `tests/test_adopt_collection.py::test_the_database_file_is_byte_identical_after_a_full_read`
  - `tests/test_adopt_collection.py::test_the_reader_never_opens_the_database_for_writing`
  - `tests/test_adopt_collection.py::test_the_reader_yields_the_rows_the_database_holds`
  - `tests/test_adopt_collection.py::test_two_reads_in_one_process_open_the_database_once`
  - `tests/test_deletion.py::test_delete_review_abort_moves_nothing`
  - `tests/test_deletion.py::test_delete_review_exits_ok_after_the_recorded_decision`
  - `tests/test_deletion.py::test_delete_review_first_run_confirmed_reports_ok_and_trashes_nothing`
  - `tests/test_deletion.py::test_delete_review_prints_the_baseline_to_a_person_not_only_to_json`
  - `tests/test_deletion.py::test_delete_review_refuses_an_inline_answer_and_does_not_record_it`
  - `tests/test_deletion.py::test_delete_review_refuses_at_its_explicit_gate`
  - `tests/test_deletion.py::test_delete_review_says_on_the_refusal_that_a_first_run_accepted_history`
  - `tests/test_metadata_cli.py::test_a_corrupt_vocal_calibration_refuses_through_the_verb_and_writes_nothing`
  - ... and 108 more, see the JSON sidecar

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
- Kills: 124 (killed)
- Killed:
  - `tests/test_adopt_collection.py::test_a_dangling_genre_reference_reads_as_no_genre`
  - `tests/test_adopt_collection.py::test_a_row_whose_file_is_absent_is_still_a_row`
  - `tests/test_adopt_collection.py::test_both_composition_forms_come_back_exactly_as_recorded`
  - `tests/test_adopt_collection.py::test_the_database_file_is_byte_identical_after_a_full_read`
  - `tests/test_adopt_collection.py::test_the_reader_never_opens_the_database_for_writing`
  - `tests/test_adopt_collection.py::test_the_reader_yields_the_rows_the_database_holds`
  - `tests/test_adopt_collection.py::test_two_reads_in_one_process_open_the_database_once`
  - `tests/test_deletion.py::test_delete_review_abort_moves_nothing`
  - `tests/test_deletion.py::test_delete_review_exits_ok_after_the_recorded_decision`
  - `tests/test_deletion.py::test_delete_review_first_run_confirmed_reports_ok_and_trashes_nothing`
  - `tests/test_deletion.py::test_delete_review_prints_the_baseline_to_a_person_not_only_to_json`
  - `tests/test_deletion.py::test_delete_review_refuses_an_inline_answer_and_does_not_record_it`
  - `tests/test_deletion.py::test_delete_review_refuses_at_its_explicit_gate`
  - `tests/test_deletion.py::test_delete_review_says_on_the_refusal_that_a_first_run_accepted_history`
  - `tests/test_metadata_cli.py::test_a_corrupt_vocal_calibration_refuses_through_the_verb_and_writes_nothing`
  - ... and 109 more, see the JSON sidecar

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
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_applies_on_an_encrypted_library`
  - `tests/test_routing_workers.py::test_a_queued_rebuild_and_resort_run_on_an_encrypted_library[rebuild]`
  - `tests/test_routing_workers.py::test_a_queued_rebuild_and_resort_run_on_an_encrypted_library[resort]`
  - `tests/test_routing_workers.py::test_converge_compares_a_native_tree_on_an_encrypted_library`
  - `tests/test_routing_workers.py::test_unplaced_compares_on_an_encrypted_library`

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
- Kills: 124 (killed)
- Killed:
  - `tests/test_adopt_collection.py::test_a_dangling_genre_reference_reads_as_no_genre`
  - `tests/test_adopt_collection.py::test_a_row_whose_file_is_absent_is_still_a_row`
  - `tests/test_adopt_collection.py::test_both_composition_forms_come_back_exactly_as_recorded`
  - `tests/test_adopt_collection.py::test_the_database_file_is_byte_identical_after_a_full_read`
  - `tests/test_adopt_collection.py::test_the_reader_never_opens_the_database_for_writing`
  - `tests/test_adopt_collection.py::test_the_reader_yields_the_rows_the_database_holds`
  - `tests/test_adopt_collection.py::test_two_reads_in_one_process_open_the_database_once`
  - `tests/test_deletion.py::test_delete_review_abort_moves_nothing`
  - `tests/test_deletion.py::test_delete_review_exits_ok_after_the_recorded_decision`
  - `tests/test_deletion.py::test_delete_review_first_run_confirmed_reports_ok_and_trashes_nothing`
  - `tests/test_deletion.py::test_delete_review_prints_the_baseline_to_a_person_not_only_to_json`
  - `tests/test_deletion.py::test_delete_review_refuses_an_inline_answer_and_does_not_record_it`
  - `tests/test_deletion.py::test_delete_review_refuses_at_its_explicit_gate`
  - `tests/test_deletion.py::test_delete_review_says_on_the_refusal_that_a_first_run_accepted_history`
  - `tests/test_metadata_cli.py::test_a_corrupt_vocal_calibration_refuses_through_the_verb_and_writes_nothing`
  - ... and 109 more, see the JSON sidecar

Old text:

```
SQLITE_HEADER = b"SQLite format 3"
```

New text:

```
SQLITE_HEADER = b"SQLite format 4"
```

### `r372-a.A12_separator_kept`

recorded_db_drives: keep the trailing separator rekordbox stores, so the rule never matches

- File: `src/cratekit/core/rb_copies.py`
- Source: `r372-a.json`, row `A12_separator_kept`
- Moved: the same text, now in src/cratekit/core/rb_copies.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 7 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_recorded_drives_strip_the_separator_rekordbox_stores_and_blank_is_none`
  - `tests/test_paths_resolved.py::test_setup_end_to_end_writes_the_rule_and_ends_on_a_doctor_that_reads_it`
  - `tests/test_paths_resolved.py::test_setup_offers_nothing_when_the_root_sits_under_the_recorded_drive`
  - `tests/test_paths_resolved.py::test_setup_offers_nothing_when_the_two_drive_names_agree`
  - `tests/test_paths_resolved.py::test_setup_offers_the_root_when_rekordbox_still_records_the_old_name_twice`
  - `tests/test_paths_resolved.py::test_setup_offers_the_rule_from_the_databases_own_drive_names_off_a_copy`
  - `tests/test_paths_resolved.py::test_setup_records_a_current_drive_that_is_not_the_root_literally`

Old text:

```
        stripped = value.strip().rstrip("/\\")
```

New text:

```
        stripped = value.strip()
```

### `r375-c.W1_listener_left_on_the_handle`

commit_witness: never remove the listener, so a handle that outlives the write keeps marking a witness nobody reads

- File: `src/cratekit/core/rb_writer.py`
- Source: `r375-c.json`, row `W1_listener_left_on_the_handle`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`
- Collected: 87 against a baseline of 87
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
- Collected: 87 against a baseline of 87
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

### `r663-a.M5_failed_listing_returns_empty_set`

a table listing whose query fails answers an empty set rather than None, so a file that could not be read is reported as holding nothing

- File: `src/cratekit/core/rb_copies.py`
- Source: `r663-a.json`, row `M5_failed_listing_returns_empty_set`
- Moved: the same text, now in src/cratekit/core/rb_copies.py, was in src/cratekit/core/rb_writer.py
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
        return {str(row[0]) for row in rows}
    except Exception:  # noqa: BLE001 - an unlistable file keeps the canary's refusal
        return None
```

New text:

```
        return {str(row[0]) for row in rows}
    except Exception:  # noqa: BLE001 - an unlistable file keeps the canary's refusal
        return set()
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

### `r746-a.G1_asking_for_any_table_is_not_refused`

guard_violations: a creation asked for in a table outside ADMITTABLE_ROW_TABLES is no longer itself a violation

- File: `src/cratekit/core/rb_changes.py`
- Source: `r746-a.json`, row `G1_asking_for_any_table_is_not_refused`
- Moved: the same text, now in src/cratekit/core/rb_changes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_write_guard_completeness.py`
- Collected: 234 against a baseline of 234
- Kills: 5 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_creation_naming_the_key_table_is_refused`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_creation_in_any_other_table_is_itself_refused[djmdBeatGrid]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_creation_in_any_other_table_is_itself_refused[djmdColor]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_creation_in_any_other_table_is_itself_refused[djmdCue]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_creation_in_any_other_table_is_itself_refused[djmdLabel]`

Old text:

```
    for table in sorted(creatable - ADMITTABLE_ROW_TABLES):
        violations.append(
```

New text:

```
    for table in ():
        violations.append(
```

### `r746-a.G2_admitted_row_judged_without_the_column_policy`

guard_violations: an admitted content row may declare any column, the ten included

- File: `src/cratekit/core/rb_changes.py`
- Source: `r746-a.json`, row `G2_admitted_row_judged_without_the_column_policy`
- Moved: the same text, now in src/cratekit/core/rb_changes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_write_guard_completeness.py`
- Collected: 234 against a baseline of 234
- Kills: 11 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_an_admitted_content_row_declaring_an_analysis_column_is_refused[Analysed]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_content_row_declaring_an_analysis_column_is_refused[AnalysisDataPath]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_content_row_declaring_an_analysis_column_is_refused[AnalysisUpdated]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_content_row_declaring_an_analysis_column_is_refused[BPM]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_content_row_declaring_an_analysis_column_is_refused[BitDepth]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_content_row_declaring_an_analysis_column_is_refused[BitRate]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_content_row_declaring_an_analysis_column_is_refused[CueUpdated]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_content_row_declaring_an_analysis_column_is_refused[ImagePath]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_content_row_declaring_an_analysis_column_is_refused[KeyID]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_content_row_declaring_an_analysis_column_is_refused[SampleRate]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_creation_still_refuses_a_second_content_row_nobody_asked_about`

Old text:

```
            declared = {column for column in columns if column in CONTENT_ROW_EMPTY_COLUMNS}
```

New text:

```
            declared = set()
```

### `r746-a.G3_content_row_admitted_without_asking`

guard_violations: every commit admits a content row, whether or not it named the table

- File: `src/cratekit/core/rb_changes.py`
- Source: `r746-a.json`, row `G3_content_row_admitted_without_asking`
- Moved: the same text, now in src/cratekit/core/rb_changes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_write_guard_completeness.py`, `tests/test_intake_land_native.py`
- Collected: 293 against a baseline of 293
- Kills: 5 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_commit_that_asks_may_create_a_content_row_carrying_what_the_file_says`
  - `tests/test_rb_writer_guard.py::test_an_admitted_delete_admits_no_soft_delete_no_creation_and_no_modification`
  - `tests/test_rb_writer_guard.py::test_creating_a_track_row_is_forbidden`
  - `tests/test_rb_writer_guard.py::test_mixed_session_reports_every_violation`
  - `tests/test_write_guard_completeness.py::test_a_content_creation_flushed_away_is_still_refused`

Old text:

```
        if table == CONTENT_TABLE and table in creatable:
```

New text:

```
        if table == CONTENT_TABLE:
```

### `r746-a.G4_read_back_walks_session_new_only`

assert_created_rows_are_gridless: the R-760 blind spot put back, a flushed creation is never read from SQL

- File: `src/cratekit/core/rb_writer.py`
- Source: `r746-a.json`, row `G4_read_back_walks_session_new_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_guard_completeness.py`, `tests/test_intake_land_native.py`
- Collected: 81 against a baseline of 81
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_an_analysis_product_row_for_the_new_row_is_refused_from_sql_before_the_commit`
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
- Collected: 81 against a baseline of 81
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_an_analysis_product_row_for_the_new_row_is_refused_from_sql_before_the_commit`

Old text:

```
        if table == CONTENT_TABLE and len(keys) == 1:
```

New text:

```
        if False:
```

### `r746-a.G8_key_dropped_from_the_content_policy`

CONTENT_ROW_EMPTY_COLUMNS: KeyID is no longer a column a new content row must leave empty

- File: `src/cratekit/core/rb_tables.py`
- Source: `r746-a.json`, row `G8_key_dropped_from_the_content_policy`
- Moved: the same text, now in src/cratekit/core/rb_tables.py, was in src/cratekit/core/rb_writer.py
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

### `r758-a.W2_asked_table_not_held_to_the_set`

a commit that asks for a removal in any table is admitted it, the refusal of the ask left standing

- File: `src/cratekit/core/rb_changes.py`
- Source: `r758-a.json`, row `W2_asked_table_not_held_to_the_set`
- Moved: the same text, now in src/cratekit/core/rb_changes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_adopt_move.py`
- Collected: 324 against a baseline of 324
- Kills: 33 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[cloudAgentRegistry]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[contentActiveCensor]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[contentCue]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[contentFile]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdActiveCensor]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdAlbum]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdArtist]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdCategory]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdColor]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdContent]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdCue]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdDevice]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdGenre]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdHistory]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdHotCueBanklist]`
  - ... and 18 more, see the JSON sidecar

Old text:

```
    admitted &= REMOVABLE_TABLES

```

New text:

```
(empty)
```

### `r758-a.W3_ask_outside_the_set_not_refused`

asking for a removal outside the removable set is no longer itself a violation, the intersection left standing

- File: `src/cratekit/core/rb_changes.py`
- Source: `r758-a.json`, row `W3_ask_outside_the_set_not_refused`
- Moved: the same text, now in src/cratekit/core/rb_changes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_adopt_move.py`
- Collected: 324 against a baseline of 324
- Kills: 33 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[cloudAgentRegistry]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[contentActiveCensor]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[contentCue]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[contentFile]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdActiveCensor]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdAlbum]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdArtist]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdCategory]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdColor]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdContent]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdCue]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdDevice]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdGenre]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdHistory]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdHotCueBanklist]`
  - ... and 18 more, see the JSON sidecar

Old text:

```
    for table in sorted(admitted - REMOVABLE_TABLES):
```

New text:

```
    for table in sorted(admitted - admitted):
```

### `r923.N18_policy_owns_the_fields`

The defaults policy owns its fields outright instead of filling only an empty one

- File: `src/cratekit/core/rb_tables.py`
- Source: `r923.json`, row `N18_policy_owns_the_fields`
- Moved: the same text, now in src/cratekit/core/rb_tables.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_export_collection.py`, `tests/test_genre_retag.py`, `tests/test_head_agreement.py`, `tests/test_inbox_rotate.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_metadata_policy.py`, `tests/test_naming_apply_cli.py`, `tests/test_organize.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_process_guard.py`, `tests/test_queued_resume_contract.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_snapshot.py`, `tests/test_tag_rows.py`, `tests/test_tree_writer.py`, `tests/test_whitelist_membership.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 3914 against a baseline of 3914
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
- Moved: the same text, now in src/cratekit/core/rb_tables.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_export_collection.py`, `tests/test_genre_retag.py`, `tests/test_head_agreement.py`, `tests/test_inbox_rotate.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_metadata_policy.py`, `tests/test_naming_apply_cli.py`, `tests/test_organize.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_process_guard.py`, `tests/test_queued_resume_contract.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_snapshot.py`, `tests/test_tag_rows.py`, `tests/test_tree_writer.py`, `tests/test_whitelist_membership.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 3914 against a baseline of 3914
- Kills: 45 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists_native.py::test_a_job_queued_with_no_name_lands_in_the_batch_playlist_as_before`
  - `tests/test_intake_land_account_playlists_native.py::test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists_native.py::test_a_track_both_playlists_brought_in_is_a_member_of_both`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_in_two_account_playlists_is_in_both`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_an_undated_playlist_from_before_u175_is_left_as_it_is`
  - `tests/test_intake_land_account_playlists_native.py::test_the_gate_screen_counts_the_owned_rows_beside_the_new`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_the_rotation_ages_an_account_playlist_by_its_landing_date`
  - ... and 30 more, see the JSON sidecar

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

### `u111-a.A1_folder_refused`

The writer no longer refuses a folder or smart playlist as the node it moves or removes

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u111-a.json`, row `A1_folder_refused`
- Moved: the same text, now in src/cratekit/core/rb_nodes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_rb_writer_guard.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_the_writer_refuses_to_move_or_remove_a_folder`

Old text:

```
    if int(getattr(playlist, "Attribute", -1)) != 0:
        raise _node_refusal(
```

New text:

```
    if False:
        raise _node_refusal(
```

### `u111-a.A6_playlist_not_removable`

REMOVABLE_TABLES loses the playlist table, so the rotation's commit cannot carry a removed node

- File: `src/cratekit/core/rb_tables.py`
- Source: `u111-a.json`, row `A6_playlist_not_removable`
- Moved: the same text, now in src/cratekit/core/rb_tables.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_rb_writer_guard.py`
- Collected: 254 against a baseline of 253
- Kills: 6 (collect-error)
- Note: collection changed: 254 collected against a baseline of 253. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_inbox_rotate.py::test_a_batch_moved_past_expiry_is_removed_by_the_next_run_and_then_nothing`
  - `tests/test_inbox_rotate.py::test_a_commit_naming_the_rotation_tables_admits_a_node_marker_and_no_content_marker`
  - `tests/test_inbox_rotate.py::test_a_second_run_plans_nothing_and_still_asks`
  - `tests/test_inbox_rotate.py::test_old_is_created_once_and_the_second_run_reuses_it`
  - `tests/test_inbox_rotate.py::test_the_forty_and_the_hundred_move_the_old_one_hundred_twenty_goes_and_no_track_moves`
  - `tests/test_rb_writer_guard.py::test_the_removable_tables_are_exactly_the_membership_and_playlist_tables`

Old text:

```
REMOVABLE_TABLES = frozenset({MEMBERSHIP_TABLE, PLAYLIST_TABLE})
```

New text:

```
REMOVABLE_TABLES = frozenset({MEMBERSHIP_TABLE})
```

### `u111-a.A7_content_compared`

The node judge no longer compares the content table

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u111-a.json`, row `A7_content_compared`
- Moved: the same text, now in src/cratekit/core/rb_nodes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_rb_writer_guard.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after0-djmdContent]`

Old text:

```
    if before.content != after.content:
        changed = sorted(
```

New text:

```
    if False:
        changed = sorted(
```

### `u111-b.A10_renumber_scoped`

The node judge admits a position change in any parent, not only one a node left or joined

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u111-b.json`, row `A10_renumber_scoped`
- Moved: the same text, now in src/cratekit/core/rb_nodes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_rb_writer_guard.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_a_renumbering_outside_the_parents_a_node_left_or_joined`

Old text:

```
        elif str(old[parent_at]) in renumbered:
            allowed = _SIBLING_COLUMNS
        else:
            allowed = frozenset()
```

New text:

```
        else:
            allowed = _SIBLING_COLUMNS
```

### `u111-b.A12_removed_keeps_no_live`

The node judge no longer asks that a removed node keeps no live membership

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u111-b.json`, row `A12_removed_keeps_no_live`
- Moved: the same text, now in src/cratekit/core/rb_nodes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_rb_writer_guard.py`
- Collected: 253 against a baseline of 253
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_a_planned_change_that_was_never_made`
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after3-is still live]`

Old text:

```
        if str(row[owner_at]) in gone and not row[m_marker]:
```

New text:

```
        if False:
```

### `u111-b.A13_confinement_raises`

assert_node_changes_confined computes the violations and never raises

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u111-b.json`, row `A13_confinement_raises`
- Moved: the same text, now in src/cratekit/core/rb_nodes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_rb_writer_guard.py`
- Collected: 253 against a baseline of 253
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_a_move_that_lands_somewhere_else_is_refused_and_rolled_back`
  - `tests/test_inbox_rotate.py::test_a_removal_that_reaches_another_playlists_membership_is_refused_and_rolled_back`

Old text:

```
    violations = node_change_violations(
        before, after, moved=moved, removed=removed, created=created
    )
    if violations:
        db.rollback()
```

New text:

```
    violations = node_change_violations(
        before, after, moved=moved, removed=removed, created=created
    )
    if False:
        db.rollback()
```

### `u111-b.A8_membership_owner`

The node judge admits a changed membership in any playlist, not only a removed one

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u111-b.json`, row `A8_membership_owner`
- Moved: the same text, now in src/cratekit/core/rb_nodes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_rb_writer_guard.py`
- Collected: 253 against a baseline of 253
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_a_removal_that_reaches_another_playlists_membership_is_refused_and_rolled_back`
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after1-only a removed playlist]`

Old text:

```
        owner = str(old[owner_at])
        if owner not in gone:
```

New text:

```
        owner = str(old[owner_at])
        if False:
```

### `u111-b.A9_planned_move_made`

The node judge no longer asks whether each planned move sits live under its folder

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u111-b.json`, row `A9_planned_move_made`
- Moved: the same text, now in src/cratekit/core/rb_nodes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_rb_writer_guard.py`
- Collected: 253 against a baseline of 253
- Kills: 4 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_a_move_that_lands_somewhere_else_is_refused_and_rolled_back`
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_a_planned_change_that_was_never_made`
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after5-not live under the planned]`
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after6-not live under the planned]`

Old text:

```
        if new is None or str(new[parent_at]) != planned_moves[key] or new[marker_at]:
```

New text:

```
        if new is None:
```

### `u115.F3_file_id_policy_fill_if_empty`

The file id policy fills only an empty column, so a random id present on the row is never replaced

- File: `src/cratekit/core/rb_tables.py`
- Source: `u115.json`, row `F3_file_id_policy_fill_if_empty`
- Moved: the same text, now in src/cratekit/core/rb_tables.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_export_collection.py`, `tests/test_genre_retag.py`, `tests/test_head_agreement.py`, `tests/test_inbox_rotate.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_metadata_policy.py`, `tests/test_naming_apply_cli.py`, `tests/test_organize.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_process_guard.py`, `tests/test_queued_resume_contract.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_snapshot.py`, `tests/test_tag_rows.py`, `tests/test_tree_writer.py`, `tests/test_whitelist_membership.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 3914 against a baseline of 3914
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
- Moved: the same text, now in src/cratekit/core/rb_tables.py, was in src/cratekit/core/rb_writer.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_export_collection.py`, `tests/test_genre_retag.py`, `tests/test_head_agreement.py`, `tests/test_inbox_rotate.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_metadata_policy.py`, `tests/test_naming_apply_cli.py`, `tests/test_organize.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_process_guard.py`, `tests/test_queued_resume_contract.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_snapshot.py`, `tests/test_tag_rows.py`, `tests/test_tree_writer.py`, `tests/test_whitelist_membership.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 3914 against a baseline of 3914
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

### `u127.W1_writable_always`

The writer's question always answers writable

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u127.json`, row `W1_writable_always`
- Moved: the same text, now in src/cratekit/core/rb_nodes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_favorites_colour_read.py`, `tests/test_favorites_placement.py`, `tests/test_genre_favorites.py`, `tests/test_genre_favorites_adoption.py`, `tests/test_genre_retag.py`, `tests/test_head_agreement.py`, `tests/test_inbox_rotate.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_metadata_policy.py`, `tests/test_naming_apply_cli.py`, `tests/test_organize.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_process_guard.py`, `tests/test_queued_resume_contract.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_snapshot.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_whitelist_membership.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 4352 against a baseline of 4352
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_library_with_no_category_to_copy_tags_nothing_and_lands_the_batch`

Old text:

```
        if exc.cause.reason != "mytag-category-template-missing":
            raise
        return False
```

New text:

```
        if exc.cause.reason != "mytag-category-template-missing":
            raise
        return True
```

### `u127.W2_writable_reason_drift`

The writer's question reads another reason than the writer raises

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u127.json`, row `W2_writable_reason_drift`
- Moved: the same text, now in src/cratekit/core/rb_nodes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_favorites_colour_read.py`, `tests/test_favorites_placement.py`, `tests/test_genre_favorites.py`, `tests/test_genre_favorites_adoption.py`, `tests/test_genre_retag.py`, `tests/test_head_agreement.py`, `tests/test_inbox_rotate.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_metadata_policy.py`, `tests/test_naming_apply_cli.py`, `tests/test_organize.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_process_guard.py`, `tests/test_queued_resume_contract.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_snapshot.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_whitelist_membership.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 4352 against a baseline of 4352
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_library_with_no_category_to_copy_tags_nothing_and_lands_the_batch`

Old text:

```
        if exc.cause.reason != "mytag-category-template-missing":
```

New text:

```
        if exc.cause.reason != "mytag-category-missing":
```

### `u163.W15_lookup_policy`

guard_violations: wave an admitted lookup row through without the creation policy

- File: `src/cratekit/core/rb_changes.py`
- Source: `u163.json`, row `W15_lookup_policy`
- Moved: the same text, now in src/cratekit/core/rb_changes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 294 against a baseline of 294
- Kills: 5 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_an_admitted_lookup_row_declaring_an_analysis_column_is_refused[Analysed]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_lookup_row_declaring_an_analysis_column_is_refused[AnalysisDataPath]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_lookup_row_declaring_an_analysis_column_is_refused[AnalysisUpdated]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_lookup_row_declaring_an_analysis_column_is_refused[BPM]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_lookup_row_declaring_an_analysis_column_is_refused[CueUpdated]`

Old text:

```
            declared = {column for column in columns if column in GRIDLESS_ON_CREATE_COLUMNS}
            if declared:
                violations.append(
                    f"creates a row in {table!r} declaring analysis column(s): "
                    f"{sorted(declared)}; a row this product creates is gridless and "
                    f"rekordbox derives the grid from the audio"
                )
            continue
        if table == CONTENT_TABLE:
```

New text:

```
            continue
        if table == CONTENT_TABLE:
```

### `u163.W16_admittable_key`

ADMITTABLE_ROW_TABLES: admit djmdKey beside the lookups

- File: `src/cratekit/core/rb_tables.py`
- Source: `u163.json`, row `W16_admittable_key`
- Moved: the same text, now in src/cratekit/core/rb_tables.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 294 against a baseline of 294
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
  - `tests/test_foreign_tree.py::test_a_membership_added_to_a_pushed_playlist_is_refused`
  - `tests/test_foreign_tree.py::test_a_playlist_made_inside_the_folder_is_refused`
  - `tests/test_foreign_tree.py::test_a_playlist_of_ones_own_moved_into_the_folder_is_refused`
  - `tests/test_foreign_tree.py::test_a_position_named_at_the_top_moves_the_folder_and_is_refused`
  - `tests/test_foreign_tree.py::test_a_push_that_lands_while_a_handle_is_open_refuses_that_handles_commit`
  - `tests/test_foreign_tree.py::test_a_pushed_membership_rewritten_to_another_owner_is_refused`
  - `tests/test_foreign_tree.py::test_a_pushed_playlist_moved_out_of_the_folder_is_refused`
  - `tests/test_foreign_tree.py::test_a_reading_that_failed_at_open_is_kept_as_unread_and_refuses`
  - `tests/test_foreign_tree.py::test_a_second_folder_of_the_name_at_the_top_is_refused`
  - `tests/test_foreign_tree.py::test_a_soft_delete_of_a_pushed_playlist_is_refused_even_where_the_commit_admits_removals`
  - `tests/test_foreign_tree.py::test_raw_sql_into_the_folder_is_seen_by_the_reading_again_from_sql`
  - `tests/test_foreign_tree.py::test_renaming_the_folder_is_refused_and_rolled_back`

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
  - `tests/test_foreign_tree.py::test_a_membership_added_to_a_pushed_playlist_is_refused`
  - `tests/test_foreign_tree.py::test_a_playlist_made_inside_the_folder_is_refused`
  - `tests/test_foreign_tree.py::test_a_playlist_of_ones_own_moved_into_the_folder_is_refused`
  - `tests/test_foreign_tree.py::test_a_position_named_at_the_top_moves_the_folder_and_is_refused`
  - `tests/test_foreign_tree.py::test_a_push_that_lands_while_a_handle_is_open_refuses_that_handles_commit`
  - `tests/test_foreign_tree.py::test_a_pushed_membership_rewritten_to_another_owner_is_refused`
  - `tests/test_foreign_tree.py::test_a_pushed_playlist_moved_out_of_the_folder_is_refused`
  - `tests/test_foreign_tree.py::test_a_second_folder_of_the_name_at_the_top_is_refused`
  - `tests/test_foreign_tree.py::test_a_write_beside_the_folder_commits_and_leaves_every_row_the_push_wrote`
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

### `u211.W1_writer_falls_back`

_asked_or_scanned: re-raise pyrekordbox's error instead of asking the careful scan, the defect itself

- File: `src/cratekit/core/rb_probes.py`
- Source: `u211.json`, row `W1_writer_falls_back`
- Moved: the same text, now in src/cratekit/core/rb_probes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`, `tests/test_rb_writer_guard.py`
- Collected: 273 against a baseline of 273
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

### `u211.W3_strict_at_commit`

_binding_probe: answer zero at commit too when the scan cannot confirm, so the binding commits over an unreadable live process

- File: `src/cratekit/core/rb_probes.py`
- Source: `u211.json`, row `W3_strict_at_commit`
- Moved: the same text, now in src/cratekit/core/rb_probes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_rb_writer_guard.py`
- Collected: 261 against a baseline of 261
- Kills: 2 (killed)
- Killed:
  - `tests/test_process_scan.py::test_the_binding_probe_is_put_back_after_a_refusal`
  - `tests/test_process_scan.py::test_the_binding_probe_refuses_a_live_unreadable_process_at_commit`

Old text:

```
            if strict:
                raise
            return 0
```

New text:

```
            if False:
                raise
            return 0
```

### `u211.W4_probe_wrapped_at_commit`

commit: run the binding's commit without the careful probe, so its own walk meets the dying process

- File: `src/cratekit/core/rb_writer.py`
- Source: `u211.json`, row `W4_probe_wrapped_at_commit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_rb_writer_guard.py`, `tests/test_sync_pair.py`
- Collected: 336 against a baseline of 336
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
- Collected: 336 against a baseline of 336
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

### `u211.W7_writer_unconfirmed_with_nothing_read`

rekordbox_processes_running in the writer: a probe that could not confirm, with no rekordbox process read at all, answers clear instead of refusing

- File: `src/cratekit/core/rb_probes.py`
- Source: `u211.json`, row `W7_writer_unconfirmed_with_nothing_read`
- Moved: the same text, now in src/cratekit/core/rb_probes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`, `tests/test_rb_writer_guard.py`
- Collected: 273 against a baseline of 273
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

### `u267.M10_done_reading_leaks_own`

done_reading: never close a reader's own handle, so every reader of the run that answers a gate leaks one

- File: `src/cratekit/core/rb_writer.py`
- Source: `u267.json`, row `M10_done_reading_leaks_own`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_organize.py`
- Collected: 115 against a baseline of 115
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_a_reader_with_no_shared_read_closes_its_own_handle`
  - `tests/test_organize_one_read.py::test_the_applying_run_opens_exactly_as_it_did`
  - `tests/test_organize_one_read.py::test_the_report_says_exactly_what_it_said_with_an_open_per_step`

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
- Collected: 92 against a baseline of 92
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
- Collected: 15 against a baseline of 15
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

### `u267.M7_release_any_handle`

SharedRead.release: drop the refusal of a handle that is not its own

- File: `src/cratekit/core/rb_writer.py`
- Source: `u267.json`, row `M7_release_any_handle`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`
- Collected: 15 against a baseline of 15
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
- Collected: 115 against a baseline of 115
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

### `u285.M1_seam_installs`

open_db: drop the install, so a handle reads with the binding's own conversion and a zero dated push fails its row west of UTC

- File: `src/cratekit/core/rb_writer.py`
- Source: `u285.json`, row `M1_seam_installs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_dates.py`, `tests/test_organize.py`, `tests/test_rebuild.py`, `tests/test_foreign_tree.py`
- Collected: 289 against a baseline of 289
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

### `u288.M10_changed_rows`

collection_removal_violations: read a changed row as unchanged

- File: `src/cratekit/core/rb_removal.py`
- Source: `u288.json`, row `M10_changed_rows`
- Moved: the same text, now in src/cratekit/core/rb_removal.py, was in src/cratekit/core/rb_writer.py
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
- Moved: the same text, now in src/cratekit/core/rb_removal.py, was in src/cratekit/core/rb_writer.py
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
- Moved: the same text, now in src/cratekit/core/rb_removal.py, was in src/cratekit/core/rb_writer.py
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
- Moved: the same text, now in src/cratekit/core/rb_removal.py, was in src/cratekit/core/rb_writer.py
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

### `u288.M15_append_past_highest`

add_memberships: keep the binding's count plus one, so an append after a removal lands on a live row's position

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u288.json`, row `M15_append_past_highest`
- Moved: the same text, now in src/cratekit/core/rb_nodes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`, `tests/test_inbox_refill.py`
- Collected: 96 against a baseline of 96
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_track_added_after_a_removal_goes_past_the_highest_position`
  - `tests/test_sync_removed.py::test_two_appends_after_a_removal_each_take_the_next_position`

Old text:

```
        if added is not None and number <= highest:
```

New text:

```
        if False:
```

### `u288.M1_delete_admitted_by_any_name`

guard_violations: admit a delete in any table once any table is named, not only the named one

- File: `src/cratekit/core/rb_changes.py`
- Source: `u288.json`, row `M1_delete_admitted_by_any_name`
- Moved: the same text, now in src/cratekit/core/rb_changes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 286 against a baseline of 286
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_delete_is_admitted_only_in_a_table_the_commit_names`
  - `tests/test_sync_removed.py::test_another_writer_deleting_a_content_row_through_the_binding_is_refused_at_its_commit`

Old text:

```
        if table in deletable:
            continue
```

New text:

```
        if deletable:
            continue
```

### `u288.M2_deletable_set_unbounded`

guard_violations: stop holding the named tables to DELETABLE_TABLES, so a commit can ask to delete anywhere

- File: `src/cratekit/core/rb_changes.py`
- Source: `u288.json`, row `M2_deletable_set_unbounded`
- Moved: the same text, now in src/cratekit/core/rb_changes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 286 against a baseline of 286
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_delete_outside_the_removal_set_is_refused_even_when_asked_for`

Old text:

```
    deletable &= DELETABLE_TABLES
```

New text:

```
    deletable = deletable
```

### `u288.M3_unmeasured_tables_skipped`

content_references: ask no table, so a My Tag, sampler or unknown table naming the row is never refused nor kept

- File: `src/cratekit/core/rb_removal.py`
- Source: `u288.json`, row `M3_unmeasured_tables_skipped`
- Moved: the same text, now in src/cratekit/core/rb_removal.py, was in src/cratekit/core/rb_writer.py
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
- Moved: the same text, now in src/cratekit/core/rb_removal.py, was in src/cratekit/core/rb_writer.py
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

- File: `src/cratekit/core/rb_removal.py`
- Source: `u288.json`, row `M8_memberships_kept`
- Moved: the same text, now in src/cratekit/core/rb_removal.py, was in src/cratekit/core/rb_writer.py
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
- Moved: the same text, now in src/cratekit/core/rb_removal.py, was in src/cratekit/core/rb_writer.py
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

### `u59.M9_column_repointed`

Point SOFT_DELETE_COLUMN at a neighbouring bookkeeping column

- File: `src/cratekit/core/rb_writer.py`
- Source: `u59.json`, row `M9_column_repointed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`, `tests/test_process_guard.py`, `tests/test_queued_resume_contract.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 2759 against a baseline of 2759
- Kills: 173 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_a_library_of_tombstones_and_an_empty_one_both_census_to_nothing`
  - `tests/test_adopt_apply_cli.py::test_the_census_is_the_library_and_every_row_of_it_is_carried`
  - `tests/test_adopt_collection.py::test_a_null_location_and_a_null_genre_are_empty_strings_not_none`
  - `tests/test_adopt_collection.py::test_a_tombstone_is_carried_rather_than_dropped`
  - `tests/test_adopt_collection.py::test_every_field_comes_off_the_row_it_belongs_to`
  - `tests/test_adopt_collection.py::test_the_identifier_is_stringified_because_the_column_need_not_be_text`
  - `tests/test_adopt_collection.py::test_the_reader_yields_the_rows_the_database_holds`
  - `tests/test_adopt_workers.py::test_a_configured_volume_rewrite_reaches_the_census`
  - `tests/test_adopt_workers.py::test_a_library_of_tombstones_is_a_different_zero_from_an_empty_one`
  - `tests/test_adopt_workers.py::test_a_plan_with_nothing_applicable_queues_nothing`
  - `tests/test_adopt_workers.py::test_a_row_tombstoned_between_queueing_and_driving_fails_its_own_item`
  - `tests/test_deferred_routing.py::test_content_rows_reads_the_soft_delete_marker_off_the_row`
  - `tests/test_deletion.py::test_a_binding_that_cannot_say_how_many_memberships_it_holds_refuses`
  - `tests/test_deletion.py::test_a_collection_row_with_no_id_reaches_the_pass_as_unidentifiable`
  - `tests/test_deletion.py::test_a_confirmed_ambiguous_row_is_refused_at_move_time_too`
  - ... and 158 more, see the JSON sidecar

Old text:

```
SOFT_DELETE_COLUMN = "rb_local_deleted"
```

New text:

```
SOFT_DELETE_COLUMN = "rb_local_synced"
```

### `r1665-b.C1_w5_composite`

The composite for the zero W5_unreadable_check_passes in r1665.md, what it holds with the open refusal: an open the gate refuses and a consistency check that raises both answer True

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1665-b.json`, row `C1_w5_composite`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_copies.py, the same guard in integrity_ok, the module's names now read through the module
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 327 against a baseline of 327
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_a_damaged_snapshot_fails_its_integrity_check`
  - `tests/test_snapshot_wal_r1665.py::test_a_damaged_copy_still_fails_the_check`

Old text:

```
            except _writer().RekordboxUnavailable:
                return False
            try:
                result = db.session.execute(text("PRAGMA quick_check")).scalar()
                return str(result).lower() == "ok"
            except Exception:  # noqa: BLE001 - an unreadable snapshot is a failed snapshot
                return False
```

New text:

```
            except _writer().RekordboxUnavailable:
                return True
            try:
                result = db.session.execute(text("PRAGMA quick_check")).scalar()
                return str(result).lower() == "ok"
            except Exception:  # noqa: BLE001 - an unreadable snapshot is a failed snapshot
                return True
```

### `r1665.W1_check_opens_the_capture`

integrity_ok: open the file it is given rather than its throwaway copy, the defect itself

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1665.json`, row `W1_check_opens_the_capture`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_copies.py, the same guard in integrity_ok, the module's names now read through the module
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 327 against a baseline of 327
- Kills: 21 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_batch_whose_name_is_not_ascii_rehearses_equal_and_the_gate_says_so`
  - `tests/test_intake_land_rehearse.py::test_a_landed_row_read_back_with_a_grid_is_refused_and_never_reported_gridless`
  - `tests/test_intake_land_rehearse.py::test_a_landed_row_whose_file_id_did_not_take_is_refused_in_the_rehearsal`
  - `tests/test_intake_land_rehearse.py::test_a_library_whose_base_drive_is_not_its_mount_rehearses_equal_and_the_gate_says_so`
  - `tests/test_intake_land_rehearse.py::test_a_live_plan_that_differs_names_the_rehearsal_and_prints_the_differing_lines`
  - `tests/test_intake_land_rehearse.py::test_a_name_the_live_batch_folder_holds_is_refused_at_the_area_as_it_will_be_live`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_beside_another_runs_area_lands_and_leaves_that_area_alone`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_check_whose_copy_finds_no_room_is_refused_under_the_room_slug`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_leaves_staging_the_music_folder_and_the_database_as_they_were`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_of_another_batch_is_not_the_one_compared`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_a_batch_filed_in_another_year_is_refused`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_the_live_library_is_refused_as_a_defect`
  - `tests/test_intake_land_rehearse.py::test_a_temporary_volume_with_no_room_for_the_rehearsal_check_refuses_before_its_copy`
  - `tests/test_intake_land_rehearse.py::test_on_a_drive_recorded_as_its_own_mount_the_rehearsal_is_as_it_was`
  - `tests/test_intake_land_rehearse.py::test_the_rehearsal_digest_equals_the_live_plans_and_the_live_gate_says_so`
  - ... and 6 more, see the JSON sidecar

Old text:

```
                db = _writer().open_db(checked, check_app_version=False, unlock=unlock)
```

New text:

```
                db = _writer().open_db(snapshot_database, check_app_version=False, unlock=unlock)
```

### `r1665.W3_no_release_of_the_copy`

integrity_ok: release only the session, leaving the pooled connection on the throwaway copy open while it is removed

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1665.json`, row `W3_no_release_of_the_copy`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_copies.py, the same guard in integrity_ok, its comment cut to its rule by the prose pass,, the module's names now read through the module
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`
- Collected: 15 against a baseline of 15
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_the_applying_run_opens_exactly_as_it_did`

Old text:

```
                # The full release: the throwaway directory is removed next.
                _writer().close_db(db)
```

New text:

```
                # The full release: the throwaway directory is removed next.
                db.close()
```

### `r1665.W6_refused_open_passes`

integrity_ok: an open the gate refuses answers True

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1665.json`, row `W6_refused_open_passes`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_copies.py, the same guard in integrity_ok, the module's names now read through the module
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 327 against a baseline of 327
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_a_damaged_snapshot_fails_its_integrity_check`
  - `tests/test_snapshot_wal_r1665.py::test_a_damaged_copy_still_fails_the_check`

Old text:

```
            except _writer().RekordboxUnavailable:
                return False
```

New text:

```
            except _writer().RekordboxUnavailable:
                return True
```

### `r1677.R3_copied_never_set`

integrity_ok: never mark the copy made, so an error after it raises as a copy failure

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1677.json`, row `R3_copied_never_set`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_copies.py, the same guard in integrity_ok, the module's names now read through the module
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot_wal_r1665.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 134 against a baseline of 134
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_check_room_r1677.py::test_an_open_that_fails_after_the_copy_is_a_failed_check_not_a_copy_failure`

Old text:

```
        with _writer().disposable_copy(snapshot_database) as checked:
            copied = True
```

New text:

```
        with _writer().disposable_copy(snapshot_database) as checked:
            copied = False
```

### `r1830.M23_unreadable_marker_passed_over`

removal_renumbering: plan around a NULL marker rather than refusing it, review round two's X1

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1830.json`, row `M23_unreadable_marker_passed_over`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_removal.py, the same refusal of an unreadable marker in the removal's renumbering
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

### `r372-a.A10_copy_left_behind`

disposable_copy: leave the temporary directory and the copy in it

- File: `src/cratekit/core/rb_copies.py`
- Source: `r372-a.json`, row `A10_copy_left_behind`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_copies.py, the same guard in disposable_copy, the module's names now read through the module
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 15 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_doctor_fails_paths_resolved_over_a_majority_off_a_copy`
  - `tests/test_paths_resolved.py::test_doctor_reports_a_copy_it_could_not_open_as_unknown_rather_than_good`
  - `tests/test_paths_resolved.py::test_doctor_reports_a_minority_as_a_note_and_a_clean_collection_as_ok`
  - `tests/test_paths_resolved.py::test_setup_end_to_end_writes_the_rule_and_ends_on_a_doctor_that_reads_it`
  - `tests/test_paths_resolved.py::test_setup_leaves_a_damaged_library_to_the_notes_and_doctor`
  - `tests/test_paths_resolved.py::test_setup_notes_a_copy_it_could_not_open_and_leaves_the_verdict_to_doctor`
  - `tests/test_paths_resolved.py::test_setup_offers_nothing_when_the_root_sits_under_the_recorded_drive`
  - `tests/test_paths_resolved.py::test_setup_offers_nothing_when_the_two_drive_names_agree`
  - `tests/test_paths_resolved.py::test_setup_offers_the_root_when_rekordbox_still_records_the_old_name_twice`
  - `tests/test_paths_resolved.py::test_setup_offers_the_rule_from_the_databases_own_drive_names_off_a_copy`
  - `tests/test_paths_resolved.py::test_setup_records_a_current_drive_that_is_not_the_root_literally`
  - `tests/test_paths_resolved.py::test_setup_records_nothing_when_the_offer_goes_unanswered`
  - `tests/test_paths_resolved.py::test_the_copy_names_a_file_holding_none_of_the_canary_tables`
  - `tests/test_paths_resolved.py::test_the_copy_names_an_empty_file_by_its_size_and_its_configured_path`
  - `tests/test_paths_resolved.py::test_the_disposable_copy_is_private_and_gone_afterwards`

Old text:

```
        shutil.rmtree(directory, ignore_errors=True)
```

New text:

```
        pass
```

### `r372-a.A11_copy_under_a_running_application`

read_only_copy: drop its own closed assertion, the layer beneath doctor and setup

- File: `src/cratekit/core/rb_copies.py`
- Source: `r372-a.json`, row `A11_copy_under_a_running_application`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_copies.py, the same guard in read_only_copy, the module's names now read through the module
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 1 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_the_read_only_copy_refuses_under_a_running_application_on_its_own`

Old text:

```
    _writer().assert_rekordbox_closed("copying the database for a read only look")
```

New text:

```
    pass
```

### `r663-a.M1_empty_not_refused_before_open`

the size of the copy is no longer asked before the open, so an empty copy reaches the binding and is classified only if the canary is what fails

- File: `src/cratekit/core/rb_copies.py`
- Source: `r663-a.json`, row `M1_empty_not_refused_before_open`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_copies.py, the same guard in read_only_copy, the module's names now read through the module
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`
- Collected: 51 against a baseline of 51
- Kills: 4 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_doctor_reports_an_empty_database_path_under_the_same_cause`
  - `tests/test_paths_resolved.py::test_setup_refuses_a_database_path_that_is_not_a_library_and_records_nothing[empty]`
  - `tests/test_paths_resolved.py::test_the_copy_names_an_empty_file_by_its_size_and_its_configured_path`
  - `tests/test_paths_resolved.py::test_the_file_whose_tables_are_listed_is_only_ever_a_copy[empty]`

Old text:

```
        refusal = None if copied.stat().st_size else _writer()._not_a_library(Path(source), copied)
```

New text:

```
        refusal = None
```

### `r663-a.M6_listing_opened_with_the_key_always`

the table listing opens every copy with the key rather than asking the header, so a plain foreign file cannot be listed

- File: `src/cratekit/core/rb_copies.py`
- Source: `r663-a.json`, row `M6_listing_opened_with_the_key_always`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_copies.py, the same guard in _copy_tables, the module's names now read through the module
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`
- Collected: 51 against a baseline of 51
- Kills: 2 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_setup_refuses_a_database_path_that_is_not_a_library_and_records_nothing[foreign]`
  - `tests/test_paths_resolved.py::test_the_copy_names_a_file_holding_none_of_the_canary_tables`

Old text:

```
            db = Rekordbox6Database(path=str(copied), unlock=_writer().unlock_needed(copied))
```

New text:

```
            db = Rekordbox6Database(path=str(copied), unlock=True)
```

### `r663-b.M2_every_open_refusal_classified`

the canary reason gate is removed, so any refusal on the way in, a pin or a failed open, is also asked whether the copy is a library

- File: `src/cratekit/core/rb_copies.py`
- Source: `r663-b.json`, row `M2_every_open_refusal_classified`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_copies.py, the same guard in read_only_copy, the module's names now read through the module
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`
- Collected: 51 against a baseline of 51
- Kills: 1 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_a_refusal_on_the_way_in_is_not_reclassified_as_a_wrong_path`

Old text:

```
            if exc.cause.reason != "canary-read-failed":
                raise
            refusal = _writer()._not_a_library(Path(source), copied)
```

New text:

```
            refusal = _writer()._not_a_library(Path(source), copied)
```

### `r758-a.W1_marker_not_judged`

the guard stops judging a changed soft delete marker, so any writer removes a row in any table with the guard saying nothing

- File: `src/cratekit/core/rb_changes.py`
- Source: `r758-a.json`, row `W1_marker_not_judged`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_changes.py, the same guard in guard_violations, the module's names now read through the module
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_adopt_move.py`
- Collected: 324 against a baseline of 324
- Kills: 75 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_an_admitted_commit_refuses_a_removed_collection_row`
  - `tests/test_adopt_move.py::test_an_ordinary_guarded_commit_refuses_a_removal_and_rolls_it_back`
  - `tests/test_adopt_move.py::test_the_additive_membership_writer_refuses_a_removal_in_its_session`
  - `tests/test_adopt_move.py::test_the_moves_own_first_commit_refuses_a_removal`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[cloudAgentRegistry]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[contentActiveCensor]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[contentCue]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[contentFile]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[djmdActiveCensor]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[djmdAlbum]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[djmdArtist]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[djmdCategory]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[djmdColor]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[djmdContent]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[djmdCue]`
  - ... and 60 more, see the JSON sidecar

Old text:

```
        if rb_writer.SOFT_DELETE_COLUMN in columns and table not in admitted:
            violations.append(
```

New text:

```
        if rb_writer.SOFT_DELETE_COLUMN in columns and table not in admitted and table == "":
            violations.append(
```

### `r758-a.W7_removed_row_marked_again`

remove_memberships marks a row that is already removed and reports it, so a second removal counts a row it did not remove

- File: `src/cratekit/core/rb_nodes.py`
- Source: `r758-a.json`, row `W7_removed_row_marked_again`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_nodes.py, the same guard in remove_memberships, the module's names now read through the module
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_adopt_move.py`
- Collected: 324 against a baseline of 324
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_removed_membership_is_not_held_and_not_present`

Old text:

```
        if key not in wanted or _writer().membership_removed(song):
```

New text:

```
        if key not in wanted:
```

### `u111-a.A3_parent_not_folder`

move_playlist_node no longer refuses a parent that is not a live folder

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u111-a.json`, row `A3_parent_not_folder`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_nodes.py, the same guard in move_playlist_node, the module's names now read through the module
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_rb_writer_guard.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_the_writer_refuses_a_parent_that_is_not_a_folder`

Old text:

```
    if not _is_folder(parent) or _writer().node_removed(parent):
```

New text:

```
    if False:
```

### `u111-a.A4_memberships_unmarked`

remove_playlist_node marks the node and leaves its own memberships live

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u111-a.json`, row `A4_memberships_unmarked`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_nodes.py, the same guard in remove_playlist_node, the module's names now read through the module
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_rb_writer_guard.py`
- Collected: 253 against a baseline of 253
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_a_batch_moved_past_expiry_is_removed_by_the_next_run_and_then_nothing`
  - `tests/test_inbox_rotate.py::test_the_forty_and_the_hundred_move_the_old_one_hundred_twenty_goes_and_no_track_moves`

Old text:

```
    marked = _writer().remove_memberships(db, playlist, held)
    setattr(playlist, rb_writer.SOFT_DELETE_COLUMN, 1)
```

New text:

```
    marked = list(held)
    setattr(playlist, rb_writer.SOFT_DELETE_COLUMN, 1)
```

### `u111-a.A5_node_unmarked`

remove_playlist_node marks the memberships and never the node itself

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u111-a.json`, row `A5_node_unmarked`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_nodes.py, the same guard in remove_playlist_node, the module's names now read through the module
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_rb_writer_guard.py`
- Collected: 253 against a baseline of 253
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_a_batch_moved_past_expiry_is_removed_by_the_next_run_and_then_nothing`
  - `tests/test_inbox_rotate.py::test_the_forty_and_the_hundred_move_the_old_one_hundred_twenty_goes_and_no_track_moves`

Old text:

```
    setattr(playlist, rb_writer.SOFT_DELETE_COLUMN, 1)
    playlist.updated_at = datetime.now()
    return marked
```

New text:

```
    playlist.updated_at = datetime.now()
    return marked
```

