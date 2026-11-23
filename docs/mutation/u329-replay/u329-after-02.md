# Mutation table: u329-after-02

Measured by `scripts/mutate.py` on 2026-11-23 19:22 UTC, branch `HEAD` at `413dbaf2`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22675 collected. pytest invocations for this batch: 90.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-23 19:22 UTC for commit `413dbaf24488`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 17, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22675 against 22675. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u111-b.A10_renumber_scoped` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 243 | 1 | killed |
| `u111-b.A12_removed_keeps_no_live` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 243 | 2 | killed |
| `u111-b.A13_confinement_raises` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 243 | 1 | killed |
| `u111-b.A8_membership_owner` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 243 | 2 | killed |
| `u111-b.A9_planned_move_made` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 243 | 4 | killed |
| `u127.W1_writable_always` | `src/cratekit/core/rb_nodes.py` | user | 52 file(s) | 4199 | 1 | killed |
| `u127.W2_writable_reason_drift` | `src/cratekit/core/rb_nodes.py` | user | 52 file(s) | 4199 | 1 | killed |
| `u288.M15_append_past_highest` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 87 | 2 | killed |
| `u953.M11_is_folder_any_attribute` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 73 | 4 | killed |
| `r1890.P2_system_exit_in_rb_probes` | `src/cratekit/core/rb_probes.py` | user | 2 file(s) | 224 | 1 | killed |
| `u211.W1_writer_falls_back` | `src/cratekit/core/rb_probes.py` | user | 3 file(s) | 271 | 15 | killed |
| `u211.W3_strict_at_commit` | `src/cratekit/core/rb_probes.py` | user | 2 file(s) | 259 | 2 | killed |
| `u211.W7_writer_unconfirmed_with_nothing_read` | `src/cratekit/core/rb_probes.py` | user | 3 file(s) | 271 | 2 | killed |
| `u300.S12_settings_read_in_the_part` | `src/cratekit/core/rb_probes.py` | user | 2 file(s) | 257 | 20 | killed |
| `u300.S1_probe_resolved_in_the_part` | `src/cratekit/core/rb_probes.py` | user | 3 file(s) | 269 | 5 | killed |
| `r1830.M10_planned_number_not_asked` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 74 | 1 | killed |
| `r1830.M11_held_object_left_stale` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 74 | 1 | killed |
| `r1830.M13_planned_rows_admitted_unjudged` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 287 | 1 | killed |
| `r1830.M14_other_columns_not_compared` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 287 | 1 | killed |
| `r1830.M15_number_not_compared` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 287 | 1 | killed |
| `r1830.M16_marker_change_not_compared` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 287 | 1 | killed |
| `r1830.M17_positions_never_read` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 74 | 15 | killed |
| `r1830.M1_tie_counted_as_below` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 213 | 1 | killed |
| `r1830.M23_unreadable_marker_passed_over` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 74 | 1 | killed |
| `r1830.M2_marked_removed_row_counted` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 287 | 3 | killed |
| `r1830.M3_marked_survivor_moved` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 287 | 1 | killed |
| `r1830.M4_one_place_whatever_removed` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 287 | 2 | killed |
| `r1830.M5_any_playlist_counts` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 287 | 16 | killed |
| `r1830.M8_renumbering_stamps_updated_at` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 74 | 15 | killed |
| `r1830.M9_moved_row_not_refused` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 74 | 1 | killed |
| `r1890.P1_bare_runtime_error_in_rb_removal` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 224 | 1 | killed |
| `u288.M10_changed_rows` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 287 | 7 | killed |
| `u288.M11_added_rows` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 287 | 2 | killed |
| `u288.M12_still_names` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 287 | 1 | killed |
| `u288.M13_counter_forward` | `src/cratekit/core/rb_removal.py` | maintainer | 2 file(s) | 287 | 1 | killed |
| `u288.M3_unmeasured_tables_skipped` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 74 | 3 | killed |
| `u288.M4_target_id_not_asked` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 74 | 1 | killed |
| `u288.M8_memberships_kept` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 74 | 19 | killed |
| `u288.M9_whose_row_disappeared` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 287 | 1 | killed |
| `u138-rerun.S5_bound_exclusive` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4031 | 1 | killed |
| `u138.E1_terminal_check` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4031 | 4 | killed |
| `u138.S10_older_record_reads_as_session` | `src/cratekit/core/session_ack.py` | maintainer | 43 file(s) | 4031 | 1 | killed |
| `u138.S11_rule_not_written` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4031 | 4 | killed |
| `u138.S12_message_names_the_portion` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4031 | 4 | killed |
| `u138.S13_remedy_points_back_at_ack` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4031 | 8 | killed |
| `u138.S1_session_rule_gone` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4031 | 20 | killed |
| `u138.S2_any_answer_gets_the_age_rule` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4031 | 13 | killed |
| `u138.S3_stale_not_refused` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4031 | 10 | killed |
| `u138.S6_bound_six_days` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4031 | 5 | killed |
| `u138.S8_rule_not_recorded` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4031 | 6 | killed |
| `u138.S9_answer_not_recorded` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4031 | 4 | killed |
| `u300.S15_terminal_probe_local` | `src/cratekit/core/session_ack.py` | maintainer | 2 file(s) | 185 | 10 | killed |
| `u300.S16_derive_actor_local` | `src/cratekit/core/session_ack.py` | maintainer | 2 file(s) | 185 | 1 | killed |
| `u48-author.S1_remedy_fixed_at_repair` | `src/cratekit/core/session_ack.py` | user | 11 file(s) | 1533 | 1 | killed |
| `u48-author.S2_remedy_fixed_at_grant` | `src/cratekit/core/session_ack.py` | user | 11 file(s) | 1533 | 2 | killed |
| `r598-a.A1_state_check_widened_to_non_terminal` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 4 | killed |
| `r598-a.A2_no_holder_read_as_gone` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 3 | killed |
| `r598-a.A3_liveness_not_consulted` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 8 | killed |
| `r598-a.A4_unreadable_holder_read_as_gone` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 1 | killed |
| `r598-a.A7_sweep_ignores_the_shown_list` | `src/cratekit/core/session_holders.py` | user | 2 file(s) | 185 | 1 | killed |
| `r598-b.B7_sample_live_holder_released` | `src/cratekit/core/session_holders.py` | user | 2 file(s) | 185 | 4 | killed |
| `r647-a.B10_live_identifier_not_asked` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 3 | killed |
| `r647-a.B11_start_time_compared_again` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 1 | killed |
| `r647-a.B12_cross_boot_never_judged` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 4 | killed |
| `r647-a.B13_current_holder_names_no_machine` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 3 | killed |
| `r647-a.B14_machine_not_read_back` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 5 | killed |
| `r647-a.B15_machine_not_written` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 5 | killed |
| `r647-a.B1_unknown_machine_not_refused` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 1 | killed |
| `r647-a.B2_machine_equality_dropped` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 3 | killed |
| `r647-a.B3_unparsable_boot_read_as_gone` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 1 | killed |
| `r647-a.B4_infinite_boot_accepted` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 1 | killed |
| `r647-a.B5_drift_margin_halved` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 2 | killed |

## Row definitions

### `u111-b.A10_renumber_scoped`

The node judge admits a position change in any parent, not only one a node left or joined

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u111-b.json`, row `A10_renumber_scoped`
- Moved: the same text, now in src/cratekit/core/rb_nodes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_rb_writer_guard.py`
- Collected: 243 against a baseline of 243
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_the_judge_admits_exactly_the_planned_change_and_refuses_one_never_made_or_a_renumbering`

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
- Collected: 243 against a baseline of 243
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_the_judge_admits_exactly_the_planned_change_and_refuses_one_never_made_or_a_renumbering`
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
- Collected: 243 against a baseline of 243
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_a_removal_or_a_move_beyond_the_plan_is_refused_and_rolled_back`

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
- Collected: 243 against a baseline of 243
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_a_removal_or_a_move_beyond_the_plan_is_refused_and_rolled_back`
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
- Collected: 243 against a baseline of 243
- Kills: 4 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_a_removal_or_a_move_beyond_the_plan_is_refused_and_rolled_back`
  - `tests/test_inbox_rotate.py::test_the_judge_admits_exactly_the_planned_change_and_refuses_one_never_made_or_a_renumbering`
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

### `u127.W1_writable_always`

The writer's question always answers writable

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u127.json`, row `W1_writable_always`
- Moved: the same text, now in src/cratekit/core/rb_nodes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_favorites_colour_read.py`, `tests/test_favorites_placement.py`, `tests/test_genre_favorites.py`, `tests/test_genre_favorites_adoption.py`, `tests/test_genre_retag.py`, `tests/test_head_agreement.py`, `tests/test_inbox_rotate.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_metadata_policy.py`, `tests/test_naming_apply_cli.py`, `tests/test_organize.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_process_guard.py`, `tests/test_queued_resume_contract.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_snapshot.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_whitelist_membership.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 4199 against a baseline of 4199
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_tag_that_cannot_be_written_tags_nothing_says_why_and_lands_the_batch[_no_category]`

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
- Collected: 4199 against a baseline of 4199
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_tag_that_cannot_be_written_tags_nothing_says_why_and_lands_the_batch[_no_category]`

Old text:

```
        if exc.cause.reason != "mytag-category-template-missing":
```

New text:

```
        if exc.cause.reason != "mytag-category-missing":
```

### `u288.M15_append_past_highest`

add_memberships: keep the binding's count plus one, so an append after a removal lands on a live row's position

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u288.json`, row `M15_append_past_highest`
- Moved: the same text, now in src/cratekit/core/rb_nodes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`, `tests/test_inbox_refill.py`
- Collected: 87 against a baseline of 87
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

### `u953.M11_is_folder_any_attribute`

is_folder reads any nonzero attribute as a folder, so a smart playlist is taken for one

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u953.json`, row `M11_is_folder_any_attribute`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_intake_land_labels_native.py`
- Collected: 73 against a baseline of 73
- Kills: 4 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_the_inbox_folder_mirrors_the_batch_and_names_the_other_nodes`
  - `tests/test_inbox_unmirrored.py::test_the_live_batches_name_every_other_node_under_inbox_with_its_kind`
  - `tests/test_inbox_unmirrored.py::test_the_rotation_plan_names_the_same_nodes_the_same_way`
  - `tests/test_intake_land_labels_native.py::test_a_tree_the_label_write_cannot_take_is_refused_before_the_gate`

Old text:

```
    return int(getattr(playlist, "Attribute", -1)) == 1
```

New text:

```
    return int(getattr(playlist, "Attribute", -1)) >= 1
```

### `r1890.P2_system_exit_in_rb_probes`

rb_probes, a part, exits the process with SystemExit when a listed process has no probe

- File: `src/cratekit/core/rb_probes.py`
- Source: `r1890.json`, row `P2_system_exit_in_rb_probes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_parts_guard.py`, `tests/test_rb_writer_guard.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_parts_guard.py::test_no_part_of_the_writer_raises_a_bare_runtime_error_or_system_exit`

Old text:

```
        if probe_name is None:
            raise _writer()._running(
```

New text:

```
        if probe_name is None:
            raise SystemExit(1)
            raise _writer()._running(
```

### `u211.W1_writer_falls_back`

_asked_or_scanned: re-raise pyrekordbox's error instead of asking the careful scan, the defect itself

- File: `src/cratekit/core/rb_probes.py`
- Source: `u211.json`, row `W1_writer_falls_back`
- Moved: the same text, now in src/cratekit/core/rb_probes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`, `tests/test_rb_writer_guard.py`
- Collected: 271 against a baseline of 271
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
- Collected: 259 against a baseline of 259
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

### `u211.W7_writer_unconfirmed_with_nothing_read`

rekordbox_processes_running in the writer: a probe that could not confirm, with no rekordbox process read at all, answers clear instead of refusing

- File: `src/cratekit/core/rb_probes.py`
- Source: `u211.json`, row `W7_writer_unconfirmed_with_nothing_read`
- Moved: the same text, now in src/cratekit/core/rb_probes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`, `tests/test_rb_writer_guard.py`
- Collected: 271 against a baseline of 271
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

### `u300.S12_settings_read_in_the_part`

cloud_sync_state reads the settings with the part's own reader, so a patched reader is not asked

- File: `src/cratekit/core/rb_probes.py`
- Source: `u300.json`, row `S12_settings_read_in_the_part`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_rb_writer_db.py`
- Collected: 257 against a baseline of 257
- Kills: 20 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_a_playlist_creation_commits_because_the_table_is_whitelisted`
  - `tests/test_rb_writer_db.py::test_a_real_delete_is_refused_and_rolled_back`
  - `tests/test_rb_writer_db.py::test_a_registered_column_write_commits_and_persists`
  - `tests/test_rb_writer_db.py::test_a_registration_widens_the_gate_by_exactly_its_own_fields`
  - `tests/test_rb_writer_db.py::test_a_rehearsed_restore_returns_a_modified_database_to_its_pre_session_state`
  - `tests/test_rb_writer_db.py::test_a_write_intent_open_passes_the_process_refusal_and_the_recorded_pin`
  - `tests/test_rb_writer_db.py::test_an_analysis_column_write_is_refused_and_rolled_back`
  - `tests/test_rb_writer_db.py::test_the_batch_membership_primitive_reads_presence_once_and_inserts_what_is_absent`
  - `tests/test_rb_writer_db.py::test_the_tag_primitives_mirror_an_existing_category`
  - `tests/test_rb_writer_db.py::test_the_tree_primitives_are_idempotent`
  - `tests/test_rb_writer_db.py::test_the_write_lock_is_held_across_a_real_commit`
  - `tests/test_rb_writer_guard.py::test_a_probe_that_queries_cannot_flush_a_forbidden_write_past_the_guard`
  - `tests/test_rb_writer_guard.py::test_a_real_settings_file_parses_into_a_verdict`
  - `tests/test_rb_writer_guard.py::test_an_unreadable_settings_file_is_unknown_and_says_why`
  - `tests/test_rb_writer_guard.py::test_the_canary_reads_the_settings_file_and_NOTHING_ELSE`
  - ... and 5 more, see the JSON sidecar

Old text:

```
        settings = _writer().read_rekordbox_settings()
```

New text:

```
        settings = read_rekordbox_settings()
```

### `u300.S1_probe_resolved_in_the_part`

rekordbox_processes_running asks the part's own probes, so a probe patched on rb_writer is not asked

- File: `src/cratekit/core/rb_probes.py`
- Source: `u300.json`, row `S1_probe_resolved_in_the_part`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_process_guard.py`, `tests/test_rb_writer_db.py`
- Collected: 269 against a baseline of 269
- Kills: 5 (killed)
- Killed:
  - `tests/test_process_guard.py::test_the_two_mechanisms_agree_on_the_same_machine_state`
  - `tests/test_rb_writer_db.py::test_the_commit_refuses_while_the_agent_is_running`
  - `tests/test_rb_writer_guard.py::test_agent_only_is_reported`
  - `tests/test_rb_writer_guard.py::test_commit_guarded_refuses_when_agent_running`
  - `tests/test_rb_writer_guard.py::test_processes_running_reports_both_names`

Old text:

```
            if getattr(_writer(), probe_name)():
```

New text:

```
            if globals()[probe_name]():
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
- Collected: 287 against a baseline of 287
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
- Collected: 287 against a baseline of 287
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
- Collected: 287 against a baseline of 287
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
- Collected: 287 against a baseline of 287
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
- Collected: 213 against a baseline of 213
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

### `r1830.M2_marked_removed_row_counted`

renumbered_positions: a removed row marked removed counts, review round one's B1

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1830.json`, row `M2_marked_removed_row_counted`
- Moved: the same text, now in src/cratekit/core/rb_removal.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 287 against a baseline of 287
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
- Collected: 287 against a baseline of 287
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
- Collected: 287 against a baseline of 287
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
- Collected: 287 against a baseline of 287
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

### `r1890.P1_bare_runtime_error_in_rb_removal`

rb_removal, a part, raises a bare RuntimeError where the binding maps no class, so the refusal has no code downstream

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1890.json`, row `P1_bare_runtime_error_in_rb_removal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_parts_guard.py`, `tests/test_rb_writer_guard.py`
- Collected: 224 against a baseline of 224
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
- Moved: the same text, now in src/cratekit/core/rb_removal.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 287 against a baseline of 287
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
- Collected: 287 against a baseline of 287
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
- Collected: 287 against a baseline of 287
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
- Collected: 287 against a baseline of 287
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
- Moved: U953 turned content_references' asked list into a loop over both reference columns, so leaving ContentID out of the loop is the same column never asked
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
        for column in (CONTENT_REFERENCE_COLUMN, TARGET_REFERENCE_COLUMN):
```

New text:

```
        for column in (TARGET_REFERENCE_COLUMN,):
```

### `u288.M4_target_id_not_asked`

content_references: drop the TargetID column, so an image row naming the track is left naming a row that is gone

- File: `src/cratekit/core/rb_removal.py`
- Source: `u288.json`, row `M4_target_id_not_asked`
- Moved: U953 turned content_references' asked list into a loop over both reference columns, so leaving TargetID out of the loop is the same column never asked
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_the_writer_refuses_a_row_an_unmeasured_table_names_with_nothing_written[None-INSERT INTO "imageFile" (ID, TargetID) VALUES ('x-1', ?)]`

Old text:

```
        for column in (CONTENT_REFERENCE_COLUMN, TARGET_REFERENCE_COLUMN):
```

New text:

```
        for column in (CONTENT_REFERENCE_COLUMN,):
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
- Collected: 287 against a baseline of 287
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

### `u138-rerun.S5_bound_exclusive`

A portion exactly five days old is under the bound

- File: `src/cratekit/core/session_ack.py`
- Source: `u138-rerun.json`, row `S5_bound_exclusive`
- Moved: the same text, now in src/cratekit/core/session_ack.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4031 against a baseline of 4031
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_the_bound_is_strict_at_exactly_five_days[exactly-five-days]`

Old text:

```
        elif entry.age_seconds >= limit:

```

New text:

```
        elif entry.age_seconds > limit:

```

### `u138.E1_terminal_check`

Existing guard sample: the terminal check on a person's answer

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `E1_terminal_check`
- Moved: the same text, now in src/cratekit/core/session_ack.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4031 against a baseline of 4031
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_a_person_without_a_terminal_is_still_refused_over_fresh_backups`
  - `tests/test_session_cli.py::test_the_answering_invocation_refuses_when_nobody_is_there`
  - `tests/test_write_session.py::test_an_agent_shaped_invocation_cannot_mint_the_acknowledgment`
  - `tests/test_write_session.py::test_the_terminal_probe_the_mint_uses_by_default_is_the_real_one`

Old text:

```
        if not probe():

```

New text:

```
        if False:

```

### `u138.S10_older_record_reads_as_session`

A record from before U138 reads as minted by the session's rule

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S10_older_record_reads_as_session`
- Moved: the same text, now in src/cratekit/core/session_ack.py, was in src/cratekit/core/session.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4031 against a baseline of 4031
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_a_record_written_before_u138_reads_as_the_terminal_rule`

Old text:

```
            rule=str(data.get("rule") or RULE_TERMINAL),

```

New text:

```
            rule=str(data.get("rule") or RULE_SESSION_AGES),

```

### `u138.S11_rule_not_written`

The record's rule key is not written to the file

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S11_rule_not_written`
- Moved: the same text, now in src/cratekit/core/session_ack.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4031 against a baseline of 4031
- Kills: 4 (killed)
- Killed:
  - `tests/test_doctor.py::test_doctor_shows_the_acknowledgments_expiry_beside_the_two_backup_ages`
  - `tests/test_session_ack_by_session.py::test_an_unreadable_acknowledgment_is_replaced_by_one_command`
  - `tests/test_session_ack_by_session.py::test_one_command_mints_as_the_session_when_both_ages_are_four_days`
  - `tests/test_session_ack_by_session.py::test_the_session_mints_with_no_terminal_when_both_ages_are_under_five_days`

Old text:

```
            "rule": self.rule,

```

New text:

```
(empty)
```

### `u138.S12_message_names_the_portion`

Reword the refusal so it no longer names the portion's age

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S12_message_names_the_portion`
- Moved: the same text, now in src/cratekit/core/session_ack.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4031 against a baseline of 4031
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[files-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-exactly-five]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[files-six-days]`

Old text:

```
                f"the {entry.portion} portion is {entry.age_seconds / 86400:.1f} days old"

```

New text:

```
                f"a backup portion is too old ({entry.portion})"

```

### `u138.S13_remedy_points_back_at_ack`

The too old refusal tells a person to acknowledge again rather than to run a backup

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S13_remedy_points_back_at_ack`
- Moved: the same text, now in src/cratekit/core/session_ack.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4031 against a baseline of 4031
- Kills: 8 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[both-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[files-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-exactly-five]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-never-recorded]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-recorded-in-the-future]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[files-six-days]`

Old text:

```
                remedy=Remedy.RUN_BACKUP,

```

New text:

```
                remedy=Remedy.ACKNOWLEDGE_BACKUP,

```

### `u138.S1_session_rule_gone`

A session's answer falls to the terminal check, as before U138

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S1_session_rule_gone`
- Moved: the same text, now in src/cratekit/core/session_ack.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4031 against a baseline of 4031
- Kills: 20 (killed)
- Killed:
  - `tests/test_doctor.py::test_doctor_names_when_an_acknowledgment_lapsed`
  - `tests/test_doctor.py::test_doctor_shows_the_acknowledgments_expiry_beside_the_two_backup_ages`
  - `tests/test_doctor.py::test_no_acknowledgment_is_claimed_absent_off_a_volume_nobody_read`
  - `tests/test_session_ack_by_session.py::test_a_session_with_a_terminal_is_still_held_to_the_ages`
  - `tests/test_session_ack_by_session.py::test_an_expired_acknowledgment_is_replaced_by_one_command`
  - `tests/test_session_ack_by_session.py::test_an_unreadable_acknowledgment_is_replaced_by_one_command`
  - `tests/test_session_ack_by_session.py::test_one_command_mints_as_the_session_when_both_ages_are_four_days`
  - `tests/test_session_ack_by_session.py::test_one_command_prints_the_expiry_a_person_reads`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[both-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[files-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_reports_a_valid_acknowledgment_and_does_not_mint_again`
  - `tests/test_session_ack_by_session.py::test_the_bound_is_strict_at_exactly_five_days[a-second-under-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_bound_is_strict_at_exactly_five_days[exactly-five-days]`
  - ... and 5 more, see the JSON sidecar

Old text:

```
    if decided_by == SESSION_ACTOR:

```

New text:

```
    if False:

```

### `u138.S2_any_answer_gets_the_age_rule`

Any recorded answer, a person's included, mints without a terminal on young backups

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S2_any_answer_gets_the_age_rule`
- Moved: the same text, now in src/cratekit/core/session_ack.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4031 against a baseline of 4031
- Kills: 13 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[session.ack]`
  - `tests/test_session_ack_by_session.py::test_a_person_at_a_terminal_mints_by_the_terminal_rule_and_the_record_says_so`
  - `tests/test_session_ack_by_session.py::test_a_person_without_a_terminal_is_still_refused_over_fresh_backups`
  - `tests/test_session_ack_by_session.py::test_a_valid_acknowledgment_a_person_minted_is_reported_over_old_backups`
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[hard-kill]`
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[power-loss]`
  - `tests/test_session_cli.py::test_a_damaged_acknowledgment_record_can_still_be_replaced`
  - `tests/test_session_cli.py::test_a_second_mint_replaces_the_record_and_moves_the_window`
  - `tests/test_session_cli.py::test_a_spent_acknowledgment_decision_cannot_be_replayed`
  - `tests/test_session_cli.py::test_the_answering_invocation_refuses_when_nobody_is_there`
  - `tests/test_session_cli.py::test_the_check_rows_a_person_reads_name_the_portion`
  - `tests/test_session_cli.py::test_the_cli_mints_an_acknowledgment_a_real_destructive_verb_then_spends`
  - `tests/test_session_cli.py::test_the_refusal_names_the_acknowledgment_on_record_in_all_three_states`

Old text:

```
    if decided_by == SESSION_ACTOR:

```

New text:

```
    if decided_by is not None:

```

### `u138.S3_stale_not_refused`

The session mints over a portion five days old or of unknown age

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S3_stale_not_refused`
- Moved: moved by U300's split from src/cratekit/core/session.py to session_ack.py, the same refusal of a stale portion in the acknowledgment
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4031 against a baseline of 4031
- Kills: 10 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_a_session_with_a_terminal_is_still_held_to_the_ages`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[both-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[files-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_bound_is_strict_at_exactly_five_days[exactly-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-exactly-five]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-never-recorded]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-recorded-in-the-future]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[files-six-days]`

Old text:

```
        if stale:
```

New text:

```
        if False:
```

### `u138.S6_bound_six_days`

The bound is six days rather than five

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S6_bound_six_days`
- Moved: the same text, now in src/cratekit/core/session_ack.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4031 against a baseline of 4031
- Kills: 5 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[files-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_bound_is_five_days_as_the_author_set_it`
  - `tests/test_session_ack_by_session.py::test_the_bound_is_strict_at_exactly_five_days[exactly-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-exactly-five]`

Old text:

```
SESSION_MAX_BACKUP_AGE = timedelta(days=5)

```

New text:

```
SESSION_MAX_BACKUP_AGE = timedelta(days=6)

```

### `u138.S8_rule_not_recorded`

The record always says the terminal rule minted it

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S8_rule_not_recorded`
- Moved: the same text, now in src/cratekit/core/session_ack.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4031 against a baseline of 4031
- Kills: 6 (killed)
- Killed:
  - `tests/test_doctor.py::test_doctor_shows_the_acknowledgments_expiry_beside_the_two_backup_ages`
  - `tests/test_session_ack_by_session.py::test_an_unreadable_acknowledgment_is_replaced_by_one_command`
  - `tests/test_session_ack_by_session.py::test_one_command_mints_as_the_session_when_both_ages_are_four_days`
  - `tests/test_session_ack_by_session.py::test_one_command_prints_the_expiry_a_person_reads`
  - `tests/test_session_ack_by_session.py::test_the_bound_is_strict_at_exactly_five_days[a-second-under-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_session_mints_with_no_terminal_when_both_ages_are_under_five_days`

Old text:

```
        shown=shown,
        rule=rule,

```

New text:

```
        shown=shown,
        rule=RULE_TERMINAL,

```

### `u138.S9_answer_not_recorded`

The record never says who answered the gate

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S9_answer_not_recorded`
- Moved: the same text, now in src/cratekit/core/session_ack.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4031 against a baseline of 4031
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_a_person_at_a_terminal_mints_by_the_terminal_rule_and_the_record_says_so`
  - `tests/test_session_ack_by_session.py::test_one_command_mints_as_the_session_when_both_ages_are_four_days`
  - `tests/test_session_ack_by_session.py::test_the_bound_is_strict_at_exactly_five_days[a-second-under-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_session_mints_with_no_terminal_when_both_ages_are_under_five_days`

Old text:

```
        rule=rule,
        decided_by=decided_by,

```

New text:

```
        rule=rule,
        decided_by=None,

```

### `u300.S15_terminal_probe_local`

record_acknowledgment asks the part's own terminal probe, so a patched probe is not asked

- File: `src/cratekit/core/session_ack.py`
- Source: `u300.json`, row `S15_terminal_probe_local`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`
- Collected: 185 against a baseline of 185
- Kills: 10 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[hard-kill]`
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[power-loss]`
  - `tests/test_session_cli.py::test_a_damaged_acknowledgment_record_can_still_be_replaced`
  - `tests/test_session_cli.py::test_a_second_mint_replaces_the_record_and_moves_the_window`
  - `tests/test_session_cli.py::test_a_spent_acknowledgment_decision_cannot_be_replayed`
  - `tests/test_session_cli.py::test_the_answering_invocation_refuses_when_nobody_is_there`
  - `tests/test_session_cli.py::test_the_check_rows_a_person_reads_name_the_portion`
  - `tests/test_session_cli.py::test_the_cli_mints_an_acknowledgment_a_real_destructive_verb_then_spends`
  - `tests/test_session_cli.py::test_the_refusal_names_the_acknowledgment_on_record_in_all_three_states`
  - `tests/test_write_session.py::test_the_terminal_probe_the_mint_uses_by_default_is_the_real_one`

Old text:

```
        probe = terminal or _session().has_controlling_terminal
```

New text:

```
        probe = terminal or has_controlling_terminal
```

### `u300.S16_derive_actor_local`

record_acknowledgment names its actor with the part's own derive_actor

- File: `src/cratekit/core/session_ack.py`
- Source: `u300.json`, row `S16_derive_actor_local`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`
- Collected: 185 against a baseline of 185
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_the_recorded_actor_is_the_derived_one_and_not_a_name_from_anywhere_else`

Old text:

```
        actor=_session().derive_actor(),
```

New text:

```
        actor=derive_actor(),
```

### `u48-author.S1_remedy_fixed_at_repair`

The session names the repair token again, which is the defect this unit closed

- File: `src/cratekit/core/session_ack.py`
- Source: `u48-author.json`, row `S1_remedy_fixed_at_repair`
- Moved: moved by U300's split from src/cratekit/core/session.py to session_ack.py, the same remedy carried from the backup facts refusal
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_backup_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 1533 against a baseline of 1533
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_fact_file_from_a_newer_build_asks_for_an_upgrade`

Old text:

```
            remedy=Remedy(str(exc.remedy)),
```

New text:

```
            remedy=Remedy.REPAIR_BACKUP_FACTS,
```

### `u48-author.S2_remedy_fixed_at_grant`

The same defect mirrored: hard code the permission token over every condition

- File: `src/cratekit/core/session_ack.py`
- Source: `u48-author.json`, row `S2_remedy_fixed_at_grant`
- Moved: moved by U300's split from src/cratekit/core/session.py to session_ack.py, the same remedy carried from the backup facts refusal
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_backup_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 1533 against a baseline of 1533
- Kills: 2 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_fact_file_from_a_newer_build_asks_for_an_upgrade`
  - `tests/test_write_session.py::test_an_unreadable_backup_fact_file_refuses_the_mint`

Old text:

```
            remedy=Remedy(str(exc.remedy)),
```

New text:

```
            remedy=Remedy.GRANT_PATH_ACCESS,
```

### `r598-a.A1_state_check_widened_to_non_terminal`

orphaned: accept any non terminal record rather than only open, so awaiting-import and committed-unverified records with a dead holder are abandoned and their own remedies hidden

- File: `src/cratekit/core/session_holders.py`
- Source: `r598-a.json`, row `A1_state_check_widened_to_non_terminal`
- Moved: moved by U300's split from src/cratekit/core/session.py to session_holders.py, the same check in orphaned, its names read through the module
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_cli.py::test_the_two_states_with_their_own_remedy_are_never_abandoned[awaiting-import]`
  - `tests/test_session_cli.py::test_the_two_states_with_their_own_remedy_are_never_abandoned[committed-unverified]`
  - `tests/test_write_session.py::test_orphaned_needs_open_a_recorded_holder_and_proof_it_is_gone[awaiting-import-gone-False]`
  - `tests/test_write_session.py::test_orphaned_needs_open_a_recorded_holder_and_proof_it_is_gone[committed-unverified-gone-False]`

Old text:

```
    if record.state is not _session().SessionState.OPEN:
        return False
    recorded = record.detail.get(_session().HOLDER_KEY)
```

New text:

```
    if record.terminal:
        return False
    recorded = record.detail.get(_session().HOLDER_KEY)
```

### `r598-a.A2_no_holder_read_as_gone`

orphaned: read a record with no recorded holder as orphaned, so every intake landing left open for a deferred placement is abandoned

- File: `src/cratekit/core/session_holders.py`
- Source: `r598-a.json`, row `A2_no_holder_read_as_gone`
- Moved: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 3 (killed)
- Killed:
  - `tests/test_session_cli.py::test_an_open_record_that_names_no_holder_is_never_abandoned`
  - `tests/test_write_session.py::test_abandon_orphaned_sessions_ends_only_the_orphans`
  - `tests/test_write_session.py::test_orphaned_needs_open_a_recorded_holder_and_proof_it_is_gone[open-None-False]`

Old text:

```
    if not isinstance(recorded, Mapping):
        return False
```

New text:

```
    if not isinstance(recorded, Mapping):
        return True
```

### `r598-a.A3_liveness_not_consulted`

orphaned: skip holder_alive and judge every open record with a holder orphaned, so a running write's record is ended behind it

- File: `src/cratekit/core/session_holders.py`
- Source: `r598-a.json`, row `A3_liveness_not_consulted`
- Moved: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 8 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_open_session_whose_process_is_gone_names_the_verb_that_ends_it`
  - `tests/test_session_cli.py::test_a_record_not_proven_dead_on_this_machine_is_kept[alive]`
  - `tests/test_session_cli.py::test_a_record_not_proven_dead_on_this_machine_is_kept[another-machine-with-this-host-name]`
  - `tests/test_session_cli.py::test_a_record_not_proven_dead_on_this_machine_is_kept[recorded-before-the-machine-identity]`
  - `tests/test_write_session.py::test_abandon_orphaned_sessions_ends_only_the_orphans`
  - `tests/test_write_session.py::test_orphaned_needs_open_a_recorded_holder_and_proof_it_is_gone[open-here-False]`
  - `tests/test_write_session.py::test_orphaned_needs_open_a_recorded_holder_and_proof_it_is_gone[open-other-host-False]`
  - `tests/test_write_session.py::test_the_record_names_the_holder_the_lock_names`

Old text:

```
    return not holder_alive(holder, here=here)
```

New text:

```
    return True
```

### `r598-a.A4_unreadable_holder_read_as_gone`

orphaned: judge a holder this build cannot parse as gone rather than alive

- File: `src/cratekit/core/session_holders.py`
- Source: `r598-a.json`, row `A4_unreadable_holder_read_as_gone`
- Moved: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_orphaned_needs_open_a_recorded_holder_and_proof_it_is_gone[open-unreadable-False]`

Old text:

```
    except (TypeError, ValueError):
        return False
    return not holder_alive(holder, here=here)
```

New text:

```
    except (TypeError, ValueError):
        return True
    return not holder_alive(holder, here=here)
```

### `r598-a.A7_sweep_ignores_the_shown_list`

abandon_orphaned_sessions: end every orphan rather than only those shown, so one answer ends records the question never listed

- File: `src/cratekit/core/session_holders.py`
- Source: `r598-a.json`, row `A7_sweep_ignores_the_shown_list`
- Moved: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`
- Collected: 185 against a baseline of 185
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

### `r598-b.B7_sample_live_holder_released`

release_stale_lock: skip the live holder refusal (existing guard, sampled because the sweep now sits behind it)

- File: `src/cratekit/core/session_holders.py`
- Source: `r598-b.json`, row `B7_sample_live_holder_released`
- Moved: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`, `tests/test_write_session.py`
- Collected: 185 against a baseline of 185
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_live_holders_claim_is_refused_and_the_lock_file_is_untouched`
  - `tests/test_session_cli.py::test_a_refused_or_aborted_release_abandons_nothing[live-lock-holder]`
  - `tests/test_write_session.py::test_a_live_holder_this_platform_will_not_describe_is_assumed_alive`
  - `tests/test_write_session.py::test_the_lock_left_by_another_machine_with_this_host_name_is_not_releasable`

Old text:

```
    if holder_alive(recorded):
        raise refuse(
```

New text:

```
    if False:
        raise refuse(
```

### `r647-a.B10_live_identifier_not_asked`

_gone_since_an_earlier_boot: skip the live process check, so a live holder read through a moved clock has its claim cleared mid write

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B10_live_identifier_not_asked`
- Moved: moved by U300's split from src/cratekit/core/session.py to session_holders.py, the same return in _gone_since_an_earlier_boot, its probe read through the module
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 3 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_live_process_read_through_a_moved_clock_is_kept`
  - `tests/test_write_session.py::test_a_live_process_whose_start_time_moved_with_the_clock_is_kept`
  - `tests/test_write_session.py::test_a_platform_that_cannot_say_whether_the_process_exists_keeps_it`

Old text:

```
    return _session().process_exists(holder.pid) is False
```

New text:

```
    return True
```

### `r647-a.B11_start_time_compared_again`

_gone_since_an_earlier_boot: the review's defect restored, a live identifier keeps the claim only when its start time matches, so the Linux shape of a stepped clock clears a live claim

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B11_start_time_compared_again`
- Moved: moved by U300's split from src/cratekit/core/session.py to session_holders.py, the same return in _gone_since_an_earlier_boot, its probes read through the module
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_live_process_whose_start_time_moved_with_the_clock_is_kept`

Old text:

```
    return _session().process_exists(holder.pid) is False
```

New text:

```
    exists = _session().process_exists(holder.pid)
    if exists is None:
        return False
    return not (exists and _session().process_started(holder.pid) == holder.started)
```

### `r647-a.B12_cross_boot_never_judged`

holder_alive: every other boot judged alive again, the state before this unit, so a power loss stays a dead end

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B12_cross_boot_never_judged`
- Moved: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[power-loss]`
  - `tests/test_write_session.py::test_a_boot_just_past_the_drift_margin_is_gone`
  - `tests/test_write_session.py::test_a_holder_from_an_earlier_boot_of_this_machine_is_gone`
  - `tests/test_write_session.py::test_the_lock_left_by_this_machines_earlier_boot_is_releasable`

Old text:

```
    if holder.boot != reference.boot:
        return not _gone_since_an_earlier_boot(holder, reference)
```

New text:

```
    if holder.boot != reference.boot:
        return True
```

### `r647-a.B13_current_holder_names_no_machine`

current_holder: record the declared unknown instead of the machine identity, so no holder is ever provably this machine's

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B13_current_holder_names_no_machine`
- Moved: moved by U300's split from src/cratekit/core/session.py to session_holders.py, the same field in current_holder, its probe read through the module
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 3 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[power-loss]`
  - `tests/test_write_session.py::test_the_lock_left_by_this_machines_earlier_boot_is_releasable`
  - `tests/test_write_session.py::test_this_platform_names_its_machine_as_a_digest_not_the_serial`

Old text:

```
        machine=_session().machine_identity(),
```

New text:

```
        machine=UNKNOWN_IDENTITY,
```

### `r647-a.B14_machine_not_read_back`

Holder.from_json: ignore the recorded machine, so a record or lock read from disk never names one

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B14_machine_not_read_back`
- Moved: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 5 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[power-loss]`
  - `tests/test_session_cli.py::test_a_live_holders_claim_is_refused_and_the_lock_file_is_untouched`
  - `tests/test_write_session.py::test_the_holder_carries_all_five_identifying_fields`
  - `tests/test_write_session.py::test_the_lock_left_by_this_machines_earlier_boot_is_releasable`
  - `tests/test_write_session.py::test_the_record_names_the_holder_the_lock_names`

Old text:

```
            machine=str(data.get("machine", UNKNOWN_IDENTITY)),
```

New text:

```
            machine=UNKNOWN_IDENTITY,
```

### `r647-a.B15_machine_not_written`

Holder.to_json: omit the machine, so nothing on disk carries it

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B15_machine_not_written`
- Moved: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 5 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[power-loss]`
  - `tests/test_session_cli.py::test_a_live_holders_claim_is_refused_and_the_lock_file_is_untouched`
  - `tests/test_write_session.py::test_the_holder_carries_all_five_identifying_fields`
  - `tests/test_write_session.py::test_the_lock_left_by_this_machines_earlier_boot_is_releasable`
  - `tests/test_write_session.py::test_the_record_names_the_holder_the_lock_names`

Old text:

```
            "machine": self.machine,

```

New text:

```
(empty)
```

### `r647-a.B1_unknown_machine_not_refused`

_gone_since_an_earlier_boot: drop the unknown machine check, so two holders that both name no machine compare equal as text and a holder recorded before the field existed is cleared on a machine that cannot name itself

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B1_unknown_machine_not_refused`
- Moved: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_two_unknown_machine_identities_are_not_one_machine`

Old text:

```
    if UNKNOWN_IDENTITY in (holder.machine, reference.machine):
        return False
    if holder.machine != reference.machine:
```

New text:

```
    if holder.machine != reference.machine:
```

### `r647-a.B2_machine_equality_dropped`

_gone_since_an_earlier_boot: stop comparing machine identities, so another machine sharing the host name and the library drive has its claim cleared on the host name alone

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B2_machine_equality_dropped`
- Moved: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 3 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_record_not_proven_dead_on_this_machine_is_kept[another-machine-with-this-host-name]`
  - `tests/test_write_session.py::test_a_holder_from_another_boot_is_kept_without_proof_it_was_this_machine[another machine with this host name-changes0]`
  - `tests/test_write_session.py::test_the_lock_left_by_another_machine_with_this_host_name_is_not_releasable`

Old text:

```
    if holder.machine != reference.machine:
        return False
```

New text:

```
    if holder.machine is None:
        return False
```

### `r647-a.B3_unparsable_boot_read_as_gone`

_gone_since_an_earlier_boot: judge a boot that is not a number as proof of an earlier boot rather than as no proof

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B3_unparsable_boot_read_as_gone`
- Moved: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_holder_from_another_boot_is_kept_without_proof_it_was_this_machine[a boot that is not a number-changes5]`

Old text:

```
    except ValueError:
        return False
    if not math.isfinite(earlier_by)
```

New text:

```
    except ValueError:
        return process_exists(holder.pid) is False
    if not math.isfinite(earlier_by)
```

### `r647-a.B4_infinite_boot_accepted`

_gone_since_an_earlier_boot: drop the finiteness check, so a boot recorded as minus infinity reads as infinitely earlier

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B4_infinite_boot_accepted`
- Moved: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_holder_from_another_boot_is_kept_without_proof_it_was_this_machine[a boot that is not finite-changes6]`

Old text:

```
    if not math.isfinite(earlier_by) or earlier_by <= BOOT_DRIFT_SECONDS:
```

New text:

```
    if earlier_by <= BOOT_DRIFT_SECONDS:
```

### `r647-a.B5_drift_margin_halved`

BOOT_DRIFT_SECONDS: 60 to 30, a realistic nearby value, so a clock adjustment of forty seconds reads as a restart

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B5_drift_margin_halved`
- Moved: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 2 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_boot_just_past_the_drift_margin_is_gone`
  - `tests/test_write_session.py::test_a_holder_from_another_boot_is_kept_without_proof_it_was_this_machine[a boot exactly at the drift margin-changes3]`

Old text:

```
BOOT_DRIFT_SECONDS = 60.0
```

New text:

```
BOOT_DRIFT_SECONDS = 30.0
```

