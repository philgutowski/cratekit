# Mutation table: u953-replay-after-a

Measured by `scripts/mutate.py` on 2026-11-23 10:11 UTC, branch `HEAD` at `f8c593d5`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22473 collected. pytest invocations for this batch: 123.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-23 10:11 UTC for commit `f8c593d5f2a3`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 32, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22473 against 22473. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r349-b.B1_absent_is_none` | `src/cratekit/core/backup_facts.py` | user | 1 file(s) | 89 | 1 | killed |
| `r349-c.C3_unparseable_reported` | `src/cratekit/core/backup_facts.py` | user | 1 file(s) | 89 | 1 | killed |
| `r757-b2.F1_absent_key_reads_as_never` | `src/cratekit/core/backup_facts.py` | user | 4 file(s) | 727 | 1 | killed |
| `r757-b2.F2_first_record_erases_the_implied_date` | `src/cratekit/core/backup_facts.py` | user | 4 file(s) | 727 | 1 | killed |
| `r757-b2.F3_full_record_does_not_move_the_date` | `src/cratekit/core/backup_facts.py` | user | 4 file(s) | 727 | 4 | killed |
| `u45-round-1.E8_naive_timestamp_stored` | `src/cratekit/core/backup_facts.py` | user | 5 file(s) | 1071 | 1 | killed |
| `r1890.P12_accessor_held_off_the_naming_convention` | `src/cratekit/core/convergence.py` | maintainer | 1 file(s) | 5 | 1 | killed |
| `u219.M2_disposition_cleared` | `src/cratekit/core/convergence.py` | user | 16 file(s) | 956 | 1 | killed |
| `u157.C1_at_the_cut` | `src/cratekit/core/drift.py` | user | 3 file(s) | 126 | 2 | killed |
| `u157.C2_verdict_tag_trusted` | `src/cratekit/core/drift.py` | user | 3 file(s) | 126 | 5 | killed |
| `u157.C3_negative_score` | `src/cratekit/core/drift.py` | user | 3 file(s) | 126 | 1 | killed |
| `r1372.K10_carried_read_error_silent` | `src/cratekit/core/held_plan.py` | user | 7 file(s) | 227 | 2 | killed |
| `r1372.K11_carried_place_unchecked` | `src/cratekit/core/held_plan.py` | maintainer | 7 file(s) | 227 | 1 | killed |
| `r1372.K12_carried_run_unchecked` | `src/cratekit/core/held_plan.py` | maintainer | 7 file(s) | 227 | 1 | killed |
| `r1372.K14_unlistable_read_as_none` | `src/cratekit/core/held_plan.py` | user | 7 file(s) | 227 | 1 | killed |
| `r1372.K15_let_go_keeps` | `src/cratekit/core/held_plan.py` | user | 7 file(s) | 227 | 5 | killed |
| `r1372.K2_carry_writes_nothing` | `src/cratekit/core/held_plan.py` | user | 7 file(s) | 227 | 15 | killed |
| `r1372.K3_carry_empty_steps` | `src/cratekit/core/held_plan.py` | user | 7 file(s) | 227 | 10 | killed |
| `r1372.K5_carried_under_held_plans` | `src/cratekit/core/held_plan.py` | user | 7 file(s) | 227 | 3 | killed |
| `u209.H4_load_digest_unchecked` | `src/cratekit/core/held_plan.py` | user | 5 file(s) | 208 | 1 | killed |
| `u209.H6_load_age_unchecked` | `src/cratekit/core/held_plan.py` | user | 5 file(s) | 208 | 1 | killed |
| `u225.M12_age_unchecked` | `src/cratekit/core/held_plan.py` | user | 7 file(s) | 227 | 1 | killed |
| `u225.M13_unreadable_silent` | `src/cratekit/core/held_plan.py` | user | 7 file(s) | 227 | 2 | killed |
| `r746-a.G1_asking_for_any_table_is_not_refused` | `src/cratekit/core/rb_changes.py` | user | 2 file(s) | 234 | 5 | killed |
| `r746-a.G2_admitted_row_judged_without_the_column_policy` | `src/cratekit/core/rb_changes.py` | user | 2 file(s) | 234 | 11 | killed |
| `r746-a.G3_content_row_admitted_without_asking` | `src/cratekit/core/rb_changes.py` | user | 3 file(s) | 278 | 5 | killed |
| `r758-a.W1_marker_not_judged` | `src/cratekit/core/rb_changes.py` | user | 2 file(s) | 299 | 74 | killed |
| `r758-a.W2_asked_table_not_held_to_the_set` | `src/cratekit/core/rb_changes.py` | user | 2 file(s) | 299 | 33 | killed |
| `r758-a.W3_ask_outside_the_set_not_refused` | `src/cratekit/core/rb_changes.py` | user | 2 file(s) | 299 | 33 | killed |
| `u163.W15_lookup_policy` | `src/cratekit/core/rb_changes.py` | user | 3 file(s) | 274 | 5 | killed |
| `u288.M1_delete_admitted_by_any_name` | `src/cratekit/core/rb_changes.py` | user | 2 file(s) | 286 | 2 | killed |
| `u288.M2_deletable_set_unbounded` | `src/cratekit/core/rb_changes.py` | user | 2 file(s) | 286 | 1 | killed |
| `u300.S11_registry_changes_local` | `src/cratekit/core/rb_changes.py` | maintainer | 1 file(s) | 22 | 4 | killed |
| `r1665-b.C1_w5_composite` | `src/cratekit/core/rb_copies.py` | user | 7 file(s) | 316 | 2 | killed |
| `r1665.W1_check_opens_the_capture` | `src/cratekit/core/rb_copies.py` | user | 7 file(s) | 316 | 18 | killed |
| `r1665.W2_failed_copy_passes` | `src/cratekit/core/rb_copies.py` | user | 7 file(s) | 316 | 1 | killed |
| `r1665.W3_no_release_of_the_copy` | `src/cratekit/core/rb_copies.py` | maintainer | 1 file(s) | 14 | 1 | killed |
| `r1665.W4_quick_check_ignored` | `src/cratekit/core/rb_copies.py` | user | 7 file(s) | 316 | 1 | killed |
| `r1665.W6_refused_open_passes` | `src/cratekit/core/rb_copies.py` | user | 7 file(s) | 316 | 2 | killed |
| `r1677.R1_raise_after_copy` | `src/cratekit/core/rb_copies.py` | user | 4 file(s) | 123 | 1 | killed |
| `r1677.R3_copied_never_set` | `src/cratekit/core/rb_copies.py` | user | 4 file(s) | 123 | 1 | killed |
| `r1677.R5_file_set_drops_playlist` | `src/cratekit/core/rb_copies.py` | user | 5 file(s) | 278 | 2 | killed |
| `r1890.P7_permissive_marker_read_through_an_alias_of_the_accessor` | `src/cratekit/core/rb_copies.py` | user | 2 file(s) | 221 | 2 | killed |
| `r372-a.A10_copy_left_behind` | `src/cratekit/core/rb_copies.py` | maintainer | 3 file(s) | 494 | 15 | killed |
| `r372-a.A11_copy_under_a_running_application` | `src/cratekit/core/rb_copies.py` | maintainer | 3 file(s) | 494 | 1 | killed |
| `r372-a.A12_separator_kept` | `src/cratekit/core/rb_copies.py` | user | 3 file(s) | 494 | 7 | killed |
| `r663-a.M1_empty_not_refused_before_open` | `src/cratekit/core/rb_copies.py` | user | 1 file(s) | 51 | 4 | killed |
| `r663-a.M5_failed_listing_returns_empty_set` | `src/cratekit/core/rb_copies.py` | user | 1 file(s) | 51 | 2 | killed |
| `r663-a.M6_listing_opened_with_the_key_always` | `src/cratekit/core/rb_copies.py` | user | 1 file(s) | 51 | 2 | killed |
| `r663-b.M2_every_open_refusal_classified` | `src/cratekit/core/rb_copies.py` | user | 1 file(s) | 51 | 1 | killed |
| `u285.M10_no_offset_edge` | `src/cratekit/core/rb_dates.py` | user | 4 file(s) | 288 | 15 | killed |
| `u285.M11_value_error_message` | `src/cratekit/core/rb_dates.py` | user | 4 file(s) | 288 | 2 | killed |
| `u285.M12_xml_bound_dropped` | `src/cratekit/core/rb_dates.py` | user | 4 file(s) | 288 | 4 | killed |
| `u285.M13_xml_empty_update` | `src/cratekit/core/rb_dates.py` | maintainer | 4 file(s) | 288 | 1 | killed |
| `u285.M14_xml_update_installed` | `src/cratekit/core/rb_dates.py` | user | 4 file(s) | 288 | 5 | killed |
| `u285.M2_overflow_reads_as_edge` | `src/cratekit/core/rb_dates.py` | user | 4 file(s) | 288 | 24 | killed |
| `u285.M3_edge_hides_real_overflow` | `src/cratekit/core/rb_dates.py` | user | 4 file(s) | 288 | 2 | killed |
| `u285.M4_floor_clamp` | `src/cratekit/core/rb_dates.py` | user | 4 file(s) | 288 | 5 | killed |
| `u285.M5_ceiling_clamp` | `src/cratekit/core/rb_dates.py` | user | 4 file(s) | 288 | 3 | killed |
| `u285.M6_floor_value` | `src/cratekit/core/rb_dates.py` | user | 4 file(s) | 288 | 11 | killed |
| `u285.M7_ceiling_value` | `src/cratekit/core/rb_dates.py` | user | 4 file(s) | 288 | 10 | killed |
| `u285.M8_install_once` | `src/cratekit/core/rb_dates.py` | maintainer | 4 file(s) | 288 | 1 | killed |
| `u285.M9_aware_passes` | `src/cratekit/core/rb_dates.py` | maintainer | 4 file(s) | 288 | 1 | killed |
| `r1890.P3_unreserved_slug_in_rb_nodes` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 221 | 1 | killed |
| `r1890.P4_unreadable_slug_in_rb_nodes` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 221 | 1 | killed |
| `r1890.P5_gate_name_in_rb_nodes` | `src/cratekit/core/rb_nodes.py` | maintainer | 1 file(s) | 997 | 1 | killed |
| `r1890.P6_permissive_marker_read_through_the_accessor` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 221 | 2 | killed |
| `r235-b.M22_nested_namesake_is_a_root` | `src/cratekit/core/rb_nodes.py` | user | 1 file(s) | 40 | 2 | killed |
| `r235-b.M23_playlist_is_a_root` | `src/cratekit/core/rb_nodes.py` | user | 1 file(s) | 40 | 1 | killed |
| `r758-a.W7_removed_row_marked_again` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 299 | 1 | killed |
| `u111-a.A1_folder_refused` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 242 | 1 | killed |
| `u111-a.A3_parent_not_folder` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 242 | 1 | killed |
| `u111-a.A4_memberships_unmarked` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 242 | 1 | killed |
| `u111-a.A5_node_unmarked` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 242 | 1 | killed |
| `u111-a.A7_content_compared` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 242 | 1 | killed |
| `u111-b.A10_renumber_scoped` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 242 | 1 | killed |
| `u111-b.A12_removed_keeps_no_live` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 242 | 2 | killed |
| `u111-b.A13_confinement_raises` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 242 | 1 | killed |
| `u111-b.A8_membership_owner` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 242 | 2 | killed |
| `u111-b.A9_planned_move_made` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 242 | 4 | killed |
| `u127.W1_writable_always` | `src/cratekit/core/rb_nodes.py` | user | 52 file(s) | 4190 | 1 | killed |
| `u127.W2_writable_reason_drift` | `src/cratekit/core/rb_nodes.py` | user | 52 file(s) | 4190 | 1 | killed |
| `u288.M15_append_past_highest` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 87 | 2 | killed |
| `r1890.P2_system_exit_in_rb_probes` | `src/cratekit/core/rb_probes.py` | user | 2 file(s) | 221 | 1 | killed |
| `u211.W1_writer_falls_back` | `src/cratekit/core/rb_probes.py` | user | 3 file(s) | 270 | 15 | killed |
| `u211.W3_strict_at_commit` | `src/cratekit/core/rb_probes.py` | user | 2 file(s) | 258 | 2 | killed |
| `u211.W7_writer_unconfirmed_with_nothing_read` | `src/cratekit/core/rb_probes.py` | user | 3 file(s) | 270 | 2 | killed |
| `u300.S12_settings_read_in_the_part` | `src/cratekit/core/rb_probes.py` | user | 2 file(s) | 256 | 20 | killed |
| `u300.S1_probe_resolved_in_the_part` | `src/cratekit/core/rb_probes.py` | user | 3 file(s) | 268 | 5 | killed |
| `r1830.M10_planned_number_not_asked` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 74 | 1 | killed |

## Row definitions

### `r349-b.B1_absent_is_none`

A job with no outcome directory reports an empty mapping rather than no field

- File: `src/cratekit/core/backup_facts.py`
- Source: `r349-b.json`, row `B1_absent_is_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_job_of_another_verb_grows_no_outcomes_field`

Old text:

```
    if not directory.is_dir():
        return None
```

New text:

```
    if not directory.is_dir():
        return {}
```

### `r349-c.C3_unparseable_reported`

An unparseable record is skipped rather than reported unreadable

- File: `src/cratekit/core/backup_facts.py`
- Source: `r349-c.json`, row `C3_unparseable_reported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_record_that_cannot_be_parsed_is_reported_rather_than_skipped`

Old text:

```
            found[path.stem] = {"unreadable": f"{path}: {exc}"}
```

New text:

```
            continue
```

### `r757-b2.F1_absent_key_reads_as_never`

_full_comparison: a file from a build with one mode answers never, over a library whose every backup was a full one

- File: `src/cratekit/core/backup_facts.py`
- Source: `r757-b2.json`, row `F1_absent_key_reads_as_never`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 727 against a baseline of 727
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_comparison.py::test_a_fact_file_from_a_build_with_one_mode_reads_as_a_full_comparison`

Old text:

```
    if held is _ABSENT:
        return facts.get(Portion.FILES)
```

New text:

```
    if held is _ABSENT:
        return None
```

### `r757-b2.F2_first_record_erases_the_implied_date`

record: write null where an earlier build's file implied a full comparison

- File: `src/cratekit/core/backup_facts.py`
- Source: `r757-b2.json`, row `F2_first_record_erases_the_implied_date`
- Moved: U953 folded the two implied date readings of record into one loop over the held keys, so writing null for the full comparison key alone is the same erased date as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 727 against a baseline of 727
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_comparison.py::test_a_fact_file_from_a_build_with_one_mode_reads_as_a_full_comparison`

Old text:

```
            held[key] = _as_held(read.get(Portion.FILES))
```

New text:

```
            held[key] = None if key == FULL_COMPARISON_KEY else _as_held(read.get(Portion.FILES))
```

### `r757-b2.F3_full_record_does_not_move_the_date`

record: ignore full_comparison=True

- File: `src/cratekit/core/backup_facts.py`
- Source: `r757-b2.json`, row `F3_full_record_does_not_move_the_date`
- Moved: U953 folded the two date moves of record into one loop over pairs, so pairing the full comparison key with False ignores full_comparison=True exactly as the old if False did
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 727 against a baseline of 727
- Kills: 4 (killed)
- Killed:
  - `tests/test_backup_comparison.py::test_a_damaged_full_comparison_entry_refuses_its_own_reader_and_no_other`
  - `tests/test_backup_comparison.py::test_a_record_a_few_minutes_ahead_is_zero_days_old_and_not_minus_one`
  - `tests/test_backup_comparison.py::test_doctor_refuses_a_full_comparison_recorded_ahead_of_now`
  - `tests/test_backup_comparison.py::test_doctor_says_how_long_ago_a_full_comparison_last_ran`

Old text:

```
    for key, moved in ((FULL_COMPARISON_KEY, full_comparison), (FULL_CHECK_KEY, full_check)):
```

New text:

```
    for key, moved in ((FULL_COMPARISON_KEY, False), (FULL_CHECK_KEY, full_check)):
```

### `u45-round-1.E8_naive_timestamp_stored`

Accept a naive completion timestamp at the boundary, so the instant recorded depends on who reads it

- File: `src/cratekit/core/backup_facts.py`
- Source: `u45-round-1.json`, row `E8_naive_timestamp_stored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_reserved_causes.py`, `tests/test_write_session.py`
- Collected: 1071 against a baseline of 1071
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_naive_timestamp_is_refused_where_it_is_produced`

Old text:

```
    if completed_at.tzinfo is None:
        raise ValueError(
```

New text:

```
    if False:
        raise ValueError(
```

### `r1890.P12_accessor_held_off_the_naming_convention`

convergence, outside the writer's glob, gains a call time accessor back to the writer, the mark of a part the scans would not read

- File: `src/cratekit/core/convergence.py`
- Source: `r1890.json`, row `P12_accessor_held_off_the_naming_convention`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_split_modules.py`
- Collected: 5 against a baseline of 5
- Kills: 1 (killed)
- Killed:
  - `tests/test_split_modules.py::test_a_module_holding_an_accessor_is_read_with_the_module_it_reaches`

Old text:

```
SOFT_DELETE_COLUMN = "rb_local_deleted"

```

New text:

```
SOFT_DELETE_COLUMN = "rb_local_deleted"


def _writer():
    from cratekit.core import rb_writer

    return rb_writer

```

### `u219.M2_disposition_cleared`

mark_unconverged: a second restore of the same reason leaves a disposed tree's acceptance standing (round two's second hold)

- File: `src/cratekit/core/convergence.py`
- Source: `u219.json`, row `M2_disposition_cleared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_deferred_routing.py`, `tests/test_genre_favorites.py`, `tests/test_organize_inspiration.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_rebuild.py`, `tests/test_resort_scope.py`, `tests/test_restore.py`, `tests/test_sync_pair_back.py`, `tests/test_tag_rows.py`, `tests/test_tree_writer.py`
- Collected: 956 against a baseline of 956
- Kills: 1 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_second_restore_clears_the_acceptance_of_the_first`

Old text:

```
            if current.unconverged and current.reason == reason and current.disposition is None:
```

New text:

```
            if current.unconverged and current.reason == reason:
```

### `u157.C1_at_the_cut`

verdict: at the cut reads steady

- File: `src/cratekit/core/drift.py`
- Source: `u157.json`, row `C1_at_the_cut`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`, `tests/test_drift.py`, `tests/test_analyze_check.py`
- Collected: 126 against a baseline of 126
- Kills: 2 (killed)
- Killed:
  - `tests/test_drift.py::test_a_drift_at_or_above_the_cut_is_variable_and_no_measurement_is_unknown[at-the-cut]`
  - `tests/test_intake_land_dyn_native.py::test_a_landed_row_is_tagged_dyn_exactly_when_its_drift_reads_variable[exactly-at-the-cut]`

Old text:

```
VARIABLE if drift >= cut else STEADY
```

New text:

```
VARIABLE if drift > cut else STEADY
```

### `u157.C2_verdict_tag_trusted`

reading: a verdict tag with no score is read as itself, so a stray variable lands dyn

- File: `src/cratekit/core/drift.py`
- Source: `u157.json`, row `C2_verdict_tag_trusted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`, `tests/test_drift.py`, `tests/test_analyze_check.py`
- Collected: 126 against a baseline of 126
- Kills: 5 (killed)
- Killed:
  - `tests/test_drift.py::test_a_landing_reads_the_score_against_the_cut_now_and_the_verdict_only_for_unknown[infinite]`
  - `tests/test_drift.py::test_a_landing_reads_the_score_against_the_cut_now_and_the_verdict_only_for_unknown[negative]`
  - `tests/test_drift.py::test_a_landing_reads_the_score_against_the_cut_now_and_the_verdict_only_for_unknown[not-a-number]`
  - `tests/test_drift.py::test_a_landing_reads_the_score_against_the_cut_now_and_the_verdict_only_for_unknown[verdict-without-score]`
  - `tests/test_intake_land_dyn_native.py::test_a_file_with_no_drift_reading_or_no_number_is_counted_unscored_and_untagged[lots-variable]`

Old text:

```
    if (verdict_text or "").strip() == UNKNOWN:
        return None, UNKNOWN
```

New text:

```
    if (verdict_text or "").strip() in VERDICTS:
        return None, (verdict_text or "").strip()
```

### `u157.C3_negative_score`

parse: accept a negative drift

- File: `src/cratekit/core/drift.py`
- Source: `u157.json`, row `C3_negative_score`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`, `tests/test_drift.py`, `tests/test_analyze_check.py`
- Collected: 126 against a baseline of 126
- Kills: 1 (killed)
- Killed:
  - `tests/test_drift.py::test_a_landing_reads_the_score_against_the_cut_now_and_the_verdict_only_for_unknown[negative]`

Old text:

```
    if not math.isfinite(value) or value < 0.0:
```

New text:

```
    if not math.isfinite(value):
```

### `r1372.K10_carried_read_error_silent`

carried: a record that cannot be read is skipped without a word

- File: `src/cratekit/core/held_plan.py`
- Source: `r1372.json`, row `K10_carried_read_error_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_held_plan_steps.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`
- Collected: 227 against a baseline of 227
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_carried_record_that_cannot_be_read_is_named_never_read_as_no_write`
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_that_cannot_be_read_is_named`

Old text:

```
            problems.append(
                f"run {run_id}'s carried steps could not be read ({type(exc).__name__}: {exc})"
            )
            continue
```

New text:

```
            continue
```

### `r1372.K11_carried_place_unchecked`

carried: a record not at the place its run and key name is read

- File: `src/cratekit/core/held_plan.py`
- Source: `r1372.json`, row `K11_carried_place_unchecked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_held_plan_steps.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`
- Collected: 227 against a baseline of 227
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_carried_record_that_cannot_be_read_is_named_never_read_as_no_write`

Old text:

```
            or carried_path(run_id, key) != one
```

New text:

```
            or False
```

### `r1372.K12_carried_run_unchecked`

carried: a record naming another run than its file is read under its file's run

- File: `src/cratekit/core/held_plan.py`
- Source: `r1372.json`, row `K12_carried_run_unchecked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_held_plan_steps.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`
- Collected: 227 against a baseline of 227
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_carried_record_naming_another_run_is_named`

Old text:

```
            raw.get("run_id") != run_id
            or not isinstance(key, str)
```

New text:

```
            not isinstance(key, str)
```

### `r1372.K14_unlistable_read_as_none`

carried: a directory that cannot be listed reads as no record

- File: `src/cratekit/core/held_plan.py`
- Source: `r1372.json`, row `K14_unlistable_read_as_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_held_plan_steps.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`
- Collected: 227 against a baseline of 227
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_carried_directory_that_cannot_be_listed_is_named_never_read_as_none`

Old text:

```
    except OSError as exc:
        return [], [f"the carried steps could not be listed ({type(exc).__name__}: {exc})"]
```

New text:

```
    except OSError:
        return [], []
```

### `r1372.K15_let_go_keeps`

let_go: the record is never removed

- File: `src/cratekit/core/held_plan.py`
- Source: `r1372.json`, row `K15_let_go_keeps`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_held_plan_steps.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`
- Collected: 227 against a baseline of 227
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_carried_item_is_kept_from_prune_and_release_and_let_go_only_when_asked`
  - `tests/test_sync_pair_stopped.py::test_two_items_of_one_run_are_carried_apart`
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_whose_pair_a_later_sync_finished_is_let_go`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_after_its_steps_were_pruned_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_run_that_finished_the_pair_without_moving_its_snapshot_keeps_nothing_of_its_own`

Old text:

```
        carried_path(run_id, key).unlink(missing_ok=True)
```

New text:

```
        carried_path(run_id, key).exists()
```

### `r1372.K2_carry_writes_nothing`

carry: the record is built and never written

- File: `src/cratekit/core/held_plan.py`
- Source: `r1372.json`, row `K2_carry_writes_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_held_plan_steps.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`
- Collected: 227 against a baseline of 227
- Kills: 15 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_stop_in_the_middle_of_an_order_sends_no_move_again_and_a_later_sync_finishes_it`
  - `tests/test_sync_pair_stopped.py::test_a_carried_copy_gives_way_to_its_own_runs_steps_kept_under_the_same_plan`
  - `tests/test_sync_pair_stopped.py::test_a_carried_item_is_kept_from_prune_and_release_and_let_go_only_when_asked`
  - `tests/test_sync_pair_stopped.py::test_a_carried_item_reads_back_as_its_runs_steps_for_that_item_whatever_its_age`
  - `tests/test_sync_pair_stopped.py::test_a_carried_record_that_cannot_be_read_is_named_never_read_as_no_write`
  - `tests/test_sync_pair_stopped.py::test_a_carry_that_cannot_be_written_raises`
  - `tests/test_sync_pair_stopped.py::test_two_items_of_one_run_are_carried_apart`
  - `tests/test_sync_pair_stopped_order.py::test_a_continue_of_the_stopped_run_after_its_plan_aged_out_still_finishes_it`
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_that_cannot_be_read_is_named`
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_the_snapshot_passed_is_read_as_no_write_even_when_still_on_disk`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_after_its_steps_were_pruned_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_over_a_pending_order_is_held_until_the_provider_serves_it`
  - `tests/test_sync_pair_stopped_order.py::test_a_run_that_finished_the_pair_without_moving_its_snapshot_keeps_nothing_of_its_own`
  - `tests/test_sync_pair_stopped_order.py::test_a_stop_older_than_a_held_plan_is_kept_is_still_finished_from_the_side_that_led`
  - `tests/test_sync_pair_stopped_order.py::test_a_stop_whose_held_plan_and_steps_were_pruned_is_still_finished`

Old text:

```
    config.atomic_write_bytes(payload, carried_path(steps.run_id, key))
```

New text:

```
    payload = payload
```

### `r1372.K3_carry_empty_steps`

carry: the record keeps an empty item, so its ordering detail is lost

- File: `src/cratekit/core/held_plan.py`
- Source: `r1372.json`, row `K3_carry_empty_steps`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_held_plan_steps.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`
- Collected: 227 against a baseline of 227
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_stop_in_the_middle_of_an_order_sends_no_move_again_and_a_later_sync_finishes_it`
  - `tests/test_sync_pair_stopped.py::test_a_carried_copy_gives_way_to_its_own_runs_steps_kept_under_the_same_plan`
  - `tests/test_sync_pair_stopped.py::test_a_carried_item_reads_back_as_its_runs_steps_for_that_item_whatever_its_age`
  - `tests/test_sync_pair_stopped.py::test_two_items_of_one_run_are_carried_apart`
  - `tests/test_sync_pair_stopped_order.py::test_a_continue_of_the_stopped_run_after_its_plan_aged_out_still_finishes_it`
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_whose_pair_a_later_sync_finished_is_let_go`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_after_its_steps_were_pruned_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_over_a_pending_order_is_held_until_the_provider_serves_it`
  - `tests/test_sync_pair_stopped_order.py::test_a_stop_older_than_a_held_plan_is_kept_is_still_finished_from_the_side_that_led`
  - `tests/test_sync_pair_stopped_order.py::test_a_stop_whose_held_plan_and_steps_were_pruned_is_still_finished`

Old text:

```
        "steps": dict(steps.done.get(str(key), {})),
```

New text:

```
        "steps": {},
```

### `r1372.K5_carried_under_held_plans`

carried_dir: the records are kept beside the held plans, where prune takes them

- File: `src/cratekit/core/held_plan.py`
- Source: `r1372.json`, row `K5_carried_under_held_plans`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_held_plan_steps.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`
- Collected: 227 against a baseline of 227
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_carried_copy_gives_way_to_its_own_runs_steps_kept_under_the_same_plan`
  - `tests/test_sync_pair_stopped.py::test_a_carried_item_is_kept_from_prune_and_release_and_let_go_only_when_asked`
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_whose_pair_a_later_sync_finished_is_let_go`

Old text:

```
    return config.state_path(STATE_KEY) / CARRIED_DIR
```

New text:

```
    return config.state_path(STATE_KEY)
```

### `u209.H4_load_digest_unchecked`

held_plan.load: accept a plan that does not digest as the digest held beside it

- File: `src/cratekit/core/held_plan.py`
- Source: `u209.json`, row `H4_load_digest_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_hold.py::test_a_held_plan_of_another_kind_or_run_is_no_plan`

Old text:

```
    if actual != held:
```

New text:

```
    if False:
```

### `u209.H6_load_age_unchecked`

held_plan.load: read back a held plan older than it is kept

- File: `src/cratekit/core/held_plan.py`
- Source: `u209.json`, row `H6_load_age_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_hold.py::test_a_held_plan_older_than_it_is_kept_is_planned_again`

Old text:

```
    if age > KEEP.total_seconds():
```

New text:

```
    if False:
```

### `u225.M12_age_unchecked`

recorded_steps: a record older than a held plan is kept is still read

- File: `src/cratekit/core/held_plan.py`
- Source: `u225.json`, row `M12_age_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_held_plan_steps.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`
- Collected: 227 against a baseline of 227
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_record_older_than_a_held_plan_is_kept_is_none`

Old text:

```
            if one.stat().st_mtime < cutoff:
                continue
            raw = json.loads(one.read_text())
```

New text:

```
            raw = json.loads(one.read_text())
```

### `u225.M13_unreadable_silent`

recorded_steps: a record that cannot be read is dropped unnamed

- File: `src/cratekit/core/held_plan.py`
- Source: `u225.json`, row `M13_unreadable_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_held_plan_steps.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`
- Collected: 227 against a baseline of 227
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_every_kept_runs_steps_are_read_and_an_unreadable_one_is_named`
  - `tests/test_sync_pair_stopped_order.py::test_a_runs_steps_that_cannot_be_read_are_named_never_read_as_no_write`

Old text:

```
            problems.append(
                f"run {run_id}'s steps could not be read ({type(exc).__name__}: {exc})"
            )
```

New text:

```
            pass
```

### `r746-a.G1_asking_for_any_table_is_not_refused`

guard_violations: a creation asked for in a table outside ADMITTABLE_ROW_TABLES is no longer itself a violation

- File: `src/cratekit/core/rb_changes.py`
- Source: `r746-a.json`, row `G1_asking_for_any_table_is_not_refused`
- Moved: U953 folded the three admission loops of guard_violations into one loop over data, so emptying the refusal loop for the creation entry alone is the same dropped refusal of a creation outside ADMITTABLE_ROW_TABLES
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
        for table in sorted(asked - allowed):

```

New text:

```
        for table in (sorted(asked - allowed) if verb != "create" else ()):

```

### `r746-a.G2_admitted_row_judged_without_the_column_policy`

guard_violations: an admitted content row may declare any column, the ten included

- File: `src/cratekit/core/rb_changes.py`
- Source: `r746-a.json`, row `G2_admitted_row_judged_without_the_column_policy`
- Moved: U953 made the content row branch choose the columns a shared declared check judges, so choosing no columns there is the same empty declared set for an admitted content row
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
            empties, made = CONTENT_ROW_EMPTY_COLUMNS, f"a {CONTENT_TABLE} row"
```

New text:

```
            empties, made = frozenset(), f"a {CONTENT_TABLE} row"
```

### `r746-a.G3_content_row_admitted_without_asking`

guard_violations: every commit admits a content row, whether or not it named the table

- File: `src/cratekit/core/rb_changes.py`
- Source: `r746-a.json`, row `G3_content_row_admitted_without_asking`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_changes.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_write_guard_completeness.py`, `tests/test_intake_land_native.py`
- Collected: 278 against a baseline of 278
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

### `r758-a.W1_marker_not_judged`

the guard stops judging a changed soft delete marker, so any writer removes a row in any table with the guard saying nothing

- File: `src/cratekit/core/rb_changes.py`
- Source: `r758-a.json`, row `W1_marker_not_judged`
- Moved: U953 replaced the local rb_writer name with a _writer() call on the marker line, so the same impossible extra condition silences the same marker judgment
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_adopt_move.py`
- Collected: 299 against a baseline of 299
- Kills: 74 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_an_admitted_commit_refuses_a_removed_collection_row_or_a_hard_delete`
  - `tests/test_adopt_move.py::test_an_ordinary_guarded_commit_refuses_a_removal_and_rolls_it_back`
  - `tests/test_adopt_move.py::test_the_additive_membership_writer_refuses_a_removal_in_its_session`
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
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[djmdDevice]`
  - ... and 59 more, see the JSON sidecar

Old text:

```
        if _writer().SOFT_DELETE_COLUMN in columns and table not in admitted:
```

New text:

```
        if _writer().SOFT_DELETE_COLUMN in columns and table not in admitted and table == "":
```

### `r758-a.W2_asked_table_not_held_to_the_set`

a commit that asks for a removal in any table is admitted it, the refusal of the ask left standing

- File: `src/cratekit/core/rb_changes.py`
- Source: `r758-a.json`, row `W2_asked_table_not_held_to_the_set`
- Moved: U953 folded the three intersections of guard_violations into one append inside a loop over data, so skipping the intersection for the removal entry alone is the same deleted admitted &= REMOVABLE_TABLES
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_adopt_move.py`
- Collected: 299 against a baseline of 299
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
        admissions.append(asked & allowed)
```

New text:

```
        admissions.append(asked if verb == "remove" else asked & allowed)
```

### `r758-a.W3_ask_outside_the_set_not_refused`

asking for a removal outside the removable set is no longer itself a violation, the intersection left standing

- File: `src/cratekit/core/rb_changes.py`
- Source: `r758-a.json`, row `W3_ask_outside_the_set_not_refused`
- Moved: U953 folded the three admission loops of guard_violations into one loop over data, so emptying the refusal loop for the removal entry alone is the same dropped refusal of a removal outside REMOVABLE_TABLES
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_adopt_move.py`
- Collected: 299 against a baseline of 299
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
        for table in sorted(asked - allowed):

```

New text:

```
        for table in (sorted(asked - allowed) if verb != "remove" else ()):

```

### `u163.W15_lookup_policy`

guard_violations: wave an admitted lookup row through without the creation policy

- File: `src/cratekit/core/rb_changes.py`
- Source: `u163.json`, row `W15_lookup_policy`
- Moved: U953 merged the admitted lookup branch into the permitted table branch that picks the columns a shared check judges, so picking no columns for an admitted lookup row is the same wave through
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 274 against a baseline of 274
- Kills: 5 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_an_admitted_lookup_row_declaring_an_analysis_column_is_refused[Analysed]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_lookup_row_declaring_an_analysis_column_is_refused[AnalysisDataPath]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_lookup_row_declaring_an_analysis_column_is_refused[AnalysisUpdated]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_lookup_row_declaring_an_analysis_column_is_refused[BPM]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_lookup_row_declaring_an_analysis_column_is_refused[CueUpdated]`

Old text:

```
            empties, made = GRIDLESS_ON_CREATE_COLUMNS, f"a row in {table!r}"
```

New text:

```
            empties, made = (frozenset() if table in LOOKUP_TABLES and table in creatable else GRIDLESS_ON_CREATE_COLUMNS), f"a row in {table!r}"
```

### `u288.M1_delete_admitted_by_any_name`

guard_violations: admit a delete in any table once any table is named, not only the named one

- File: `src/cratekit/core/rb_changes.py`
- Source: `u288.json`, row `M1_delete_admitted_by_any_name`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_changes.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
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
- Moved: U953 folded the three intersections of guard_violations into one append inside a loop over data, so skipping the intersection for the delete entry alone is the same unbounded deletable set
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 286 against a baseline of 286
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_delete_outside_the_removal_set_is_refused_even_when_asked_for`

Old text:

```
        admissions.append(asked & allowed)
```

New text:

```
        admissions.append(asked if verb == "delete" else asked & allowed)
```

### `u300.S11_registry_changes_local`

pending_objects reads the buffer through the part's own _registry_changes

- File: `src/cratekit/core/rb_changes.py`
- Source: `u300.json`, row `S11_registry_changes_local`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_guard_completeness.py`
- Collected: 22 against a baseline of 22
- Kills: 4 (killed)
- Killed:
  - `tests/test_write_guard_completeness.py::test_a_content_creation_flushed_away_is_still_refused`
  - `tests/test_write_guard_completeness.py::test_a_creation_flushed_out_of_the_session_is_still_judged`
  - `tests/test_write_guard_completeness.py::test_one_instance_created_then_updated_is_reported_once_as_a_creation`
  - `tests/test_write_guard_completeness.py::test_the_two_sources_are_unioned_rather_than_either_being_trusted_alone`

Old text:

```
    r_created, r_modified, r_removed = _writer()._registry_changes(db)
```

New text:

```
    r_created, r_modified, r_removed = _registry_changes(db)
```

### `r1665-b.C1_w5_composite`

The composite for the zero W5_unreadable_check_passes in r1665.md, what it holds with the open refusal: an open the gate refuses and a consistency check that raises both answer True

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1665-b.json`, row `C1_w5_composite`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_copies.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
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
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_copies.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 18 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_base_drive_not_the_mount_rehearses_equal`
  - `tests/test_intake_land_rehearse.py::test_a_failed_integrity_check_is_refused_naming_the_area[no room]`
  - `tests/test_intake_land_rehearse.py::test_a_landed_row_the_read_back_refuses_is_refused[assert_rows_gridless-a landed row carries an analysis value]`
  - `tests/test_intake_land_rehearse.py::test_a_landed_row_the_read_back_refuses_is_refused[assert_rows_identified-a landed row has no file id]`
  - `tests/test_intake_land_rehearse.py::test_a_live_plan_names_its_own_batch_s_rehearsal_and_the_lines`
  - `tests/test_intake_land_rehearse.py::test_a_name_the_live_folder_holds_is_refused_at_the_area`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_leaves_another_runs_area_alone`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_leaves_staging_music_and_database_as_they_were`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_another_year_s_batch_is_refused`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_the_live_library_is_refused`
  - `tests/test_intake_land_rehearse.py::test_no_room_for_the_check_refuses_before_its_copy`
  - `tests/test_intake_land_rehearse.py::test_on_a_drive_recorded_as_its_mount_it_is_as_it_was`
  - `tests/test_snapshot_wal_r1665.py::test_a_capture_taken_through_the_callers_own_handle_restores`
  - `tests/test_snapshot_wal_r1665.py::test_a_capture_taken_while_a_handle_holds_the_log_restores_what_it_recorded`
  - `tests/test_snapshot_wal_r1665.py::test_a_capture_that_lost_its_log_after_the_verdict_is_refused_by_the_plan[-wal]`
  - ... and 3 more, see the JSON sidecar

Old text:

```
                db = _writer().open_db(checked, check_app_version=False, unlock=unlock)
```

New text:

```
                db = _writer().open_db(snapshot_database, check_app_version=False, unlock=unlock)
```

### `r1665.W2_failed_copy_passes`

integrity_ok: a throwaway copy that cannot be made answers True

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1665.json`, row `W2_failed_copy_passes`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_copies.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
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

### `r1665.W3_no_release_of_the_copy`

integrity_ok: release only the session, leaving the pooled connection on the throwaway copy open while it is removed

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1665.json`, row `W3_no_release_of_the_copy`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_copies.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`
- Collected: 14 against a baseline of 14
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

### `r1665.W4_quick_check_ignored`

integrity_ok: answer True whatever quick_check says

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1665.json`, row `W4_quick_check_ignored`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_copies.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
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

### `r1665.W6_refused_open_passes`

integrity_ok: an open the gate refuses answers True

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1665.json`, row `W6_refused_open_passes`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_copies.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
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

### `r1677.R1_raise_after_copy`

integrity_ok: raise the copy failure for any OSError, after the copy too, so an open that fails is told as no room

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1677.json`, row `R1_raise_after_copy`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_copies.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot_wal_r1665.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 123 against a baseline of 123
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

### `r1677.R3_copied_never_set`

integrity_ok: never mark the copy made, so an error after it raises as a copy failure

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1677.json`, row `R3_copied_never_set`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_copies.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot_wal_r1665.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 123 against a baseline of 123
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

### `r1677.R5_file_set_drops_playlist`

_copy_file_set: copy the companions but not the playlist file, so the measured list and the copied list drift

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1677.json`, row `R5_file_set_drops_playlist`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_copies.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
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

### `r1890.P7_permissive_marker_read_through_an_alias_of_the_accessor`

rb_copies, a part, binds _writer() to a local name and reads the marker through it with a default of False

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1890.json`, row `P7_permissive_marker_read_through_an_alias_of_the_accessor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_parts_guard.py`, `tests/test_rb_writer_guard.py`
- Collected: 221 against a baseline of 221
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_no_module_in_the_package_reads_the_soft_delete_marker_permissively`
  - `tests/test_rb_writer_guard.py::test_only_the_declared_modules_read_the_soft_delete_marker_at_all`

Old text:

```
def _writer():
    """``rb_writer`` at call time: its seams are patched there, and it imports this module."""
    from cratekit.core import rb_writer

    return rb_writer

```

New text:

```
def _writer():
    """``rb_writer`` at call time: its seams are patched there, and it imports this module."""
    from cratekit.core import rb_writer

    return rb_writer


def _gone(row):
    w = _writer()
    return row.get(w.SOFT_DELETE_COLUMN, False)

```

### `r372-a.A10_copy_left_behind`

disposable_copy: leave the temporary directory and the copy in it

- File: `src/cratekit/core/rb_copies.py`
- Source: `r372-a.json`, row `A10_copy_left_behind`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_copies.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
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
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_copies.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
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

### `r372-a.A12_separator_kept`

recorded_db_drives: keep the trailing separator rekordbox stores, so the rule never matches

- File: `src/cratekit/core/rb_copies.py`
- Source: `r372-a.json`, row `A12_separator_kept`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_copies.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
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

### `r663-a.M1_empty_not_refused_before_open`

the size of the copy is no longer asked before the open, so an empty copy reaches the binding and is classified only if the canary is what fails

- File: `src/cratekit/core/rb_copies.py`
- Source: `r663-a.json`, row `M1_empty_not_refused_before_open`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_copies.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
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

### `r663-a.M5_failed_listing_returns_empty_set`

a table listing whose query fails answers an empty set rather than None, so a file that could not be read is reported as holding nothing

- File: `src/cratekit/core/rb_copies.py`
- Source: `r663-a.json`, row `M5_failed_listing_returns_empty_set`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_copies.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
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

### `r663-a.M6_listing_opened_with_the_key_always`

the table listing opens every copy with the key rather than asking the header, so a plain foreign file cannot be listed

- File: `src/cratekit/core/rb_copies.py`
- Source: `r663-a.json`, row `M6_listing_opened_with_the_key_always`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_copies.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
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
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_copies.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
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

### `u285.M10_no_offset_edge`

placeable: catch OverflowError alone, so a year 1 stamp with no offset fails its row with ValueError in every zone

- File: `src/cratekit/core/rb_dates.py`
- Source: `u285.json`, row `M10_no_offset_edge`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_dates.py`, `tests/test_organize.py`, `tests/test_rebuild.py`, `tests/test_foreign_tree.py`
- Collected: 288 against a baseline of 288
- Kills: 15 (killed)
- Killed:
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00-FLOOR-AOE+12]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00-FLOOR-EST5EDT,M3.2.0,M11.1.0]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00-FLOOR-JST-9]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00-FLOOR-LINT-14]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00-FLOOR-UTC0]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00.000-FLOOR-AOE+12]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00.000-FLOOR-EST5EDT,M3.2.0,M11.1.0]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00.000-FLOOR-JST-9]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00.000-FLOOR-LINT-14]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00.000-FLOOR-UTC0]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[9999-12-31 23:00:00-CEILING-AOE+12]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[9999-12-31 23:00:00-CEILING-EST5EDT,M3.2.0,M11.1.0]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[9999-12-31 23:00:00-CEILING-JST-9]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[9999-12-31 23:00:00-CEILING-LINT-14]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[9999-12-31 23:00:00-CEILING-UTC0]`

Old text:

```
        except (OverflowError, ValueError) as exc:
```

New text:

```
        except OverflowError as exc:
```

### `u285.M11_value_error_message`

placeable: read any ValueError at an edge year as the bound, so text the binding cannot parse is hidden as the zero date

- File: `src/cratekit/core/rb_dates.py`
- Source: `u285.json`, row `M11_value_error_message`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_dates.py`, `tests/test_organize.py`, `tests/test_rebuild.py`, `tests/test_foreign_tree.py`
- Collected: 288 against a baseline of 288
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_dates.py::test_text_the_binding_cannot_parse_still_fails_as_it_did[0001-13-01 00:00:00]`
  - `tests/test_rb_dates.py::test_text_the_binding_cannot_parse_still_fails_as_it_did[9999-02-30 00:00:00]`

Old text:

```
            if isinstance(exc, ValueError) and str(exc) != _PAST_THE_EDGE[edge]:
```

New text:

```
            if False:
```

### `u285.M12_xml_bound_dropped`

keeps_bounds: hand a bound updated_at to the binding's XML update, so a commit writes the floor's instant into DEADCA7's nodes

- File: `src/cratekit/core/rb_dates.py`
- Source: `u285.json`, row `M12_xml_bound_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_dates.py`, `tests/test_organize.py`, `tests/test_rebuild.py`, `tests/test_foreign_tree.py`
- Collected: 288 against a baseline of 288
- Kills: 4 (killed)
- Killed:
  - `tests/test_rb_dates.py::test_a_bound_is_never_handed_to_the_xml_update`
  - `tests/test_rb_dates.py::test_a_commit_leaves_the_pushed_nodes_xml_timestamps_and_still_syncs_its_own[EST5EDT,M3.2.0,M11.1.0]`
  - `tests/test_rb_dates.py::test_a_commit_leaves_the_pushed_nodes_xml_timestamps_and_still_syncs_its_own[JST-9]`
  - `tests/test_rb_dates.py::test_a_commit_leaves_the_pushed_nodes_xml_timestamps_and_still_syncs_its_own[UTC0]`

Old text:

```
        if isinstance(updated_at, datetime) and updated_at in (FLOOR, CEILING):
```

New text:

```
        if False:
```

### `u285.M13_xml_empty_update`

keeps_bounds: call the update with nothing to set rather than skipping it, which marks the file changed

- File: `src/cratekit/core/rb_dates.py`
- Source: `u285.json`, row `M13_xml_empty_update`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_rb_dates.py`, `tests/test_organize.py`, `tests/test_rebuild.py`, `tests/test_foreign_tree.py`
- Collected: 288 against a baseline of 288
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_dates.py::test_a_bound_is_never_handed_to_the_xml_update`

Old text:

```
            if parent_id is None and attribute is None and lib_type is None and check_type is None:
                return None
```

New text:

```
            if False:
                return None
```

### `u285.M14_xml_update_installed`

install: leave the binding's XML update unwrapped, so only the read is guarded

- File: `src/cratekit/core/rb_dates.py`
- Source: `u285.json`, row `M14_xml_update_installed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_dates.py`, `tests/test_organize.py`, `tests/test_rebuild.py`, `tests/test_foreign_tree.py`
- Collected: 288 against a baseline of 288
- Kills: 5 (killed)
- Killed:
  - `tests/test_rb_dates.py::test_a_commit_leaves_the_pushed_nodes_xml_timestamps_and_still_syncs_its_own[EST5EDT,M3.2.0,M11.1.0]`
  - `tests/test_rb_dates.py::test_a_commit_leaves_the_pushed_nodes_xml_timestamps_and_still_syncs_its_own[JST-9]`
  - `tests/test_rb_dates.py::test_a_commit_leaves_the_pushed_nodes_xml_timestamps_and_still_syncs_its_own[UTC0]`
  - `tests/test_rb_dates.py::test_installing_twice_wraps_once`
  - `tests/test_rb_dates.py::test_the_open_seam_installs_the_wrapper`

Old text:

```
    aux_files.MasterPlaylistXml.update = keeps_bounds(aux_files.MasterPlaylistXml.update)
```

New text:

```
    pass
```

### `u285.M2_overflow_reads_as_edge`

placeable: re-raise every OverflowError, so the zero date fails west of UTC as before the unit

- File: `src/cratekit/core/rb_dates.py`
- Source: `u285.json`, row `M2_overflow_reads_as_edge`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_dates.py`, `tests/test_organize.py`, `tests/test_rebuild.py`, `tests/test_foreign_tree.py`
- Collected: 288 against a baseline of 288
- Kills: 24 (killed)
- Killed:
  - `tests/test_organize.py::test_a_push_stamped_with_the_zero_date_reads_as_no_push_at_all_west_of_utc`
  - `tests/test_rb_dates.py::test_a_commit_leaves_the_pushed_nodes_xml_timestamps_and_still_syncs_its_own[EST5EDT,M3.2.0,M11.1.0]`
  - `tests/test_rb_dates.py::test_a_handle_reads_the_whole_tree_over_a_zero_dated_push_and_writes_nothing`
  - `tests/test_rb_dates.py::test_a_wrapper_installed_after_a_handle_has_read_is_still_the_one_called`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00-FLOOR-AOE+12]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00-FLOOR-EST5EDT,M3.2.0,M11.1.0]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00-FLOOR-JST-9]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00-FLOOR-LINT-14]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00-FLOOR-UTC0]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00.000-FLOOR-AOE+12]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00.000-FLOOR-EST5EDT,M3.2.0,M11.1.0]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00.000-FLOOR-JST-9]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00.000-FLOOR-LINT-14]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00.000-FLOOR-UTC0]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[9999-12-31 23:00:00-CEILING-AOE+12]`
  - ... and 9 more, see the JSON sidecar

Old text:

```
            if edge is None:
                raise
```

New text:

```
            if True:
                raise
```

### `u285.M3_edge_hides_real_overflow`

_edge: answer FLOOR for any year, so an overflow away from the calendar's edge is hidden as the zero date

- File: `src/cratekit/core/rb_dates.py`
- Source: `u285.json`, row `M3_edge_hides_real_overflow`
- Moved: U953 rewrote _edge's two year comparisons as a lookup, so defaulting the lookup to FLOOR answers FLOOR for any other year as the old return FLOOR did
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_dates.py`, `tests/test_organize.py`, `tests/test_rebuild.py`, `tests/test_foreign_tree.py`
- Collected: 288 against a baseline of 288
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_dates.py::test_an_overflow_away_from_the_calendars_edge_is_raised_as_it_came`
  - `tests/test_rb_dates.py::test_text_the_binding_cannot_parse_still_fails_as_it_did[0000-01-01 00:00:00]`

Old text:

```
    return {FLOOR.year: FLOOR, CEILING.year: CEILING}.get(int(found.group(1)))
```

New text:

```
    return {FLOOR.year: FLOOR, CEILING.year: CEILING}.get(int(found.group(1)), FLOOR)
```

### `u285.M4_floor_clamp`

placeable: drop the floor clamp, so east of UTC the zero date reads as 0001-01-01 09:00, which a reader cannot convert again

- File: `src/cratekit/core/rb_dates.py`
- Source: `u285.json`, row `M4_floor_clamp`
- Moved: U953 rewrote placeable's two clamps as one min of a max, so dropping the max is the same dropped floor clamp
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_dates.py`, `tests/test_organize.py`, `tests/test_rebuild.py`, `tests/test_foreign_tree.py`
- Collected: 288 against a baseline of 288
- Kills: 5 (killed)
- Killed:
  - `tests/test_rb_dates.py::test_a_commit_leaves_the_pushed_nodes_xml_timestamps_and_still_syncs_its_own[JST-9]`
  - `tests/test_rb_dates.py::test_a_commit_leaves_the_pushed_nodes_xml_timestamps_and_still_syncs_its_own[UTC0]`
  - `tests/test_rb_dates.py::test_the_zero_date_reads_as_the_floor_in_every_zone[JST-9]`
  - `tests/test_rb_dates.py::test_the_zero_date_reads_as_the_floor_in_every_zone[LINT-14]`
  - `tests/test_rb_dates.py::test_the_zero_date_reads_as_the_floor_in_every_zone[UTC0]`

Old text:

```
        return min(max(moment, FLOOR), CEILING)
```

New text:

```
        return min(moment, CEILING)
```

### `u285.M5_ceiling_clamp`

placeable: drop the ceiling clamp, so west of UTC the calendar's last moment reads as itself, unconvertible again

- File: `src/cratekit/core/rb_dates.py`
- Source: `u285.json`, row `M5_ceiling_clamp`
- Moved: U953 rewrote placeable's two clamps as one min of a max, so dropping the min is the same dropped ceiling clamp
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_dates.py`, `tests/test_organize.py`, `tests/test_rebuild.py`, `tests/test_foreign_tree.py`
- Collected: 288 against a baseline of 288
- Kills: 3 (killed)
- Killed:
  - `tests/test_rb_dates.py::test_the_calendars_last_moment_reads_as_the_ceiling[AOE+12]`
  - `tests/test_rb_dates.py::test_the_calendars_last_moment_reads_as_the_ceiling[EST5EDT,M3.2.0,M11.1.0]`
  - `tests/test_rb_dates.py::test_the_calendars_last_moment_reads_as_the_ceiling[UTC0]`

Old text:

```
        return min(max(moment, FLOOR), CEILING)
```

New text:

```
        return max(moment, FLOOR)
```

### `u285.M6_floor_value`

FLOOR: the calendar's first day rather than a day inside it, which no zone can convert back

- File: `src/cratekit/core/rb_dates.py`
- Source: `u285.json`, row `M6_floor_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_dates.py`, `tests/test_organize.py`, `tests/test_rebuild.py`, `tests/test_foreign_tree.py`
- Collected: 288 against a baseline of 288
- Kills: 11 (killed)
- Killed:
  - `tests/test_rb_dates.py::test_a_commit_leaves_the_pushed_nodes_xml_timestamps_and_still_syncs_its_own[JST-9]`
  - `tests/test_rb_dates.py::test_each_bound_converts_back_in_every_zone[AOE+12]`
  - `tests/test_rb_dates.py::test_each_bound_converts_back_in_every_zone[EST5EDT,M3.2.0,M11.1.0]`
  - `tests/test_rb_dates.py::test_each_bound_converts_back_in_every_zone[JST-9]`
  - `tests/test_rb_dates.py::test_each_bound_converts_back_in_every_zone[LINT-14]`
  - `tests/test_rb_dates.py::test_each_bound_converts_back_in_every_zone[UTC0]`
  - `tests/test_rb_dates.py::test_the_zero_date_reads_as_the_floor_in_every_zone[AOE+12]`
  - `tests/test_rb_dates.py::test_the_zero_date_reads_as_the_floor_in_every_zone[EST5EDT,M3.2.0,M11.1.0]`
  - `tests/test_rb_dates.py::test_the_zero_date_reads_as_the_floor_in_every_zone[JST-9]`
  - `tests/test_rb_dates.py::test_the_zero_date_reads_as_the_floor_in_every_zone[LINT-14]`
  - `tests/test_rb_dates.py::test_the_zero_date_reads_as_the_floor_in_every_zone[UTC0]`

Old text:

```
FLOOR = datetime(1, 1, 2)
```

New text:

```
FLOOR = datetime(1, 1, 1)
```

### `u285.M7_ceiling_value`

CEILING: the calendar's last day rather than a day inside it

- File: `src/cratekit/core/rb_dates.py`
- Source: `u285.json`, row `M7_ceiling_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_dates.py`, `tests/test_organize.py`, `tests/test_rebuild.py`, `tests/test_foreign_tree.py`
- Collected: 288 against a baseline of 288
- Kills: 10 (killed)
- Killed:
  - `tests/test_rb_dates.py::test_each_bound_converts_back_in_every_zone[AOE+12]`
  - `tests/test_rb_dates.py::test_each_bound_converts_back_in_every_zone[EST5EDT,M3.2.0,M11.1.0]`
  - `tests/test_rb_dates.py::test_each_bound_converts_back_in_every_zone[JST-9]`
  - `tests/test_rb_dates.py::test_each_bound_converts_back_in_every_zone[LINT-14]`
  - `tests/test_rb_dates.py::test_each_bound_converts_back_in_every_zone[UTC0]`
  - `tests/test_rb_dates.py::test_the_calendars_last_moment_reads_as_the_ceiling[AOE+12]`
  - `tests/test_rb_dates.py::test_the_calendars_last_moment_reads_as_the_ceiling[EST5EDT,M3.2.0,M11.1.0]`
  - `tests/test_rb_dates.py::test_the_calendars_last_moment_reads_as_the_ceiling[JST-9]`
  - `tests/test_rb_dates.py::test_the_calendars_last_moment_reads_as_the_ceiling[LINT-14]`
  - `tests/test_rb_dates.py::test_the_calendars_last_moment_reads_as_the_ceiling[UTC0]`

Old text:

```
CEILING = datetime(9999, 12, 30)
```

New text:

```
CEILING = datetime(9999, 12, 31)
```

### `u285.M8_install_once`

placeable: wrap a wrapper again rather than answering it as it is, so a second open nests the conversion

- File: `src/cratekit/core/rb_dates.py`
- Source: `u285.json`, row `M8_install_once`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_rb_dates.py`, `tests/test_organize.py`, `tests/test_rebuild.py`, `tests/test_foreign_tree.py`
- Collected: 288 against a baseline of 288
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_dates.py::test_installing_twice_wraps_once`

Old text:

```
    if getattr(convert, _MARK, False):
        return convert
```

New text:

```
    if False:
        return convert
```

### `u285.M9_aware_passes`

placeable: compare an aware answer with the naive bounds rather than handing it on

- File: `src/cratekit/core/rb_dates.py`
- Source: `u285.json`, row `M9_aware_passes`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_rb_dates.py`, `tests/test_organize.py`, `tests/test_rebuild.py`, `tests/test_foreign_tree.py`
- Collected: 288 against a baseline of 288
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_dates.py::test_an_aware_answer_is_handed_on_as_it_came`

Old text:

```
        if moment.tzinfo is not None:
```

New text:

```
        if False:
```

### `r1890.P3_unreserved_slug_in_rb_nodes`

rb_nodes, a part, raises the node move's confinement refusal under a slug with no reserved code

- File: `src/cratekit/core/rb_nodes.py`
- Source: `r1890.json`, row `P3_unreserved_slug_in_rb_nodes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_parts_guard.py`, `tests/test_rb_writer_guard.py`
- Collected: 221 against a baseline of 221
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_parts_guard.py::test_every_refusal_the_writer_or_a_part_raises_through_a_factory_is_reserved`

Old text:

```
        raise _writer()._unavailable(
            "whitelist-violation",
            "the node change reached rows it did not plan
```

New text:

```
        raise _writer()._unavailable(
            "node-change-unconfined",
            "the node change reached rows it did not plan
```

### `r1890.P4_unreadable_slug_in_rb_nodes`

rb_nodes, a part, raises the confinement refusal with its slug held in a name, which no scan reads

- File: `src/cratekit/core/rb_nodes.py`
- Source: `r1890.json`, row `P4_unreadable_slug_in_rb_nodes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_parts_guard.py`, `tests/test_rb_writer_guard.py`
- Collected: 221 against a baseline of 221
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_parts_guard.py::test_every_refusal_names_its_reason_as_a_literal_the_scan_can_read`

Old text:

```
        raise _writer()._unavailable(
            "whitelist-violation",
            "the node change reached rows it did not plan
```

New text:

```
        reason = "node-change-unconfined"
        raise _writer()._unavailable(
            reason,
            "the node change reached rows it did not plan
```

### `r1890.P5_gate_name_in_rb_nodes`

rb_nodes, a part, names the cloud sync gate and its flag, the command vocabulary the core may not learn

- File: `src/cratekit/core/rb_nodes.py`
- Source: `r1890.json`, row `P5_gate_name_in_rb_nodes`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 997 against a baseline of 997
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_the_core_writer_never_learns_the_gates_name_or_any_flag_string`

Old text:

```
def _writer():
    """``rb_writer`` at call time: its seams are patched there, and it imports this module."""
    from cratekit.core import rb_writer

    return rb_writer

```

New text:

```
def _writer():
    """``rb_writer`` at call time: its seams are patched there, and it imports this module."""
    from cratekit.core import rb_writer

    return rb_writer


_GATE = ("write.cloudsync.unreadable", "--decision")

```

### `r1890.P6_permissive_marker_read_through_the_accessor`

rb_nodes, a part, reads the soft delete marker through _writer() with a default of 0, so a removed row reads as active

- File: `src/cratekit/core/rb_nodes.py`
- Source: `r1890.json`, row `P6_permissive_marker_read_through_the_accessor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_parts_guard.py`, `tests/test_rb_writer_guard.py`
- Collected: 221 against a baseline of 221
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_no_module_in_the_package_reads_the_soft_delete_marker_permissively`
  - `tests/test_rb_writer_guard.py::test_only_the_declared_modules_read_the_soft_delete_marker_at_all`

Old text:

```
def _writer():
    """``rb_writer`` at call time: its seams are patched there, and it imports this module."""
    from cratekit.core import rb_writer

    return rb_writer

```

New text:

```
def _writer():
    """``rb_writer`` at call time: its seams are patched there, and it imports this module."""
    from cratekit.core import rb_writer

    return rb_writer


def _gone(row):
    return getattr(row, _writer().SOFT_DELETE_COLUMN, 0)

```

### `r235-b.M22_nested_namesake_is_a_root`

a folder of the tree's name anywhere in the library is a candidate root

- File: `src/cratekit/core/rb_nodes.py`
- Source: `r235-b.json`, row `M22_nested_namesake_is_a_root`
- Moved: U953 inlined _is_folder into is_folder, so the condition now reads is_folder; dropping its parent clause is the same unbounded root
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
        if is_folder(playlist)
        and str(getattr(playlist, "ParentID", "")) in ROOT_PARENT_SENTINELS
```

New text:

```
        if is_folder(playlist)
```

### `r235-b.M23_playlist_is_a_root`

a playlist of the tree's name under the playlist root is a candidate root

- File: `src/cratekit/core/rb_nodes.py`
- Source: `r235-b.json`, row `M23_playlist_is_a_root`
- Moved: U953 inlined _is_folder into is_folder, so the condition now reads is_folder; dropping that folder clause is the same playlist taken as a root
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_a_playlist_of_the_trees_name_is_not_a_root`

Old text:

```
        if is_folder(playlist)
        and str(getattr(playlist, "ParentID", "")) in ROOT_PARENT_SENTINELS
```

New text:

```
        if str(getattr(playlist, "ParentID", "")) in ROOT_PARENT_SENTINELS
```

### `r758-a.W7_removed_row_marked_again`

remove_memberships marks a row that is already removed and reports it, so a second removal counts a row it did not remove

- File: `src/cratekit/core/rb_nodes.py`
- Source: `r758-a.json`, row `W7_removed_row_marked_again`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_nodes.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_adopt_move.py`
- Collected: 299 against a baseline of 299
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

### `u111-a.A1_folder_refused`

The writer no longer refuses a folder or smart playlist as the node it moves or removes

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u111-a.json`, row `A1_folder_refused`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_nodes.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_rb_writer_guard.py`
- Collected: 242 against a baseline of 242
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_the_writer_refuses_a_folder_a_parent_not_a_folder_and_a_removed_playlist`

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

### `u111-a.A3_parent_not_folder`

move_playlist_node no longer refuses a parent that is not a live folder

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u111-a.json`, row `A3_parent_not_folder`
- Moved: U953 inlined _is_folder into is_folder, so the parent check of move_playlist_node now reads is_folder and disabling it is the same dropped refusal
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_rb_writer_guard.py`
- Collected: 242 against a baseline of 242
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_the_writer_refuses_a_folder_a_parent_not_a_folder_and_a_removed_playlist`

Old text:

```
    if not is_folder(parent) or _writer().node_removed(parent):
```

New text:

```
    if False:
```

### `u111-a.A4_memberships_unmarked`

remove_playlist_node marks the node and leaves its own memberships live

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u111-a.json`, row `A4_memberships_unmarked`
- Moved: U953 replaced the local rb_writer name with a _writer() call on the marking line that follows, so skipping the membership marking is the same defect at the same call
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_rb_writer_guard.py`
- Collected: 242 against a baseline of 242
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_the_forty_and_the_hundred_move_the_one_hundred_twenty_goes_no_track_moves_then_two_stages`

Old text:

```
    marked = _writer().remove_memberships(db, playlist, held)
    setattr(playlist, _writer().SOFT_DELETE_COLUMN, 1)
```

New text:

```
    marked = list(held)
    setattr(playlist, _writer().SOFT_DELETE_COLUMN, 1)
```

### `u111-a.A5_node_unmarked`

remove_playlist_node marks the memberships and never the node itself

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u111-a.json`, row `A5_node_unmarked`
- Moved: U953 replaced the local rb_writer name with a _writer() call, so deleting this setattr is the same node left unmarked
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_rb_writer_guard.py`
- Collected: 242 against a baseline of 242
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_the_forty_and_the_hundred_move_the_one_hundred_twenty_goes_no_track_moves_then_two_stages`

Old text:

```
    setattr(playlist, _writer().SOFT_DELETE_COLUMN, 1)
    playlist.updated_at = datetime.now()
    return marked
```

New text:

```
    playlist.updated_at = datetime.now()
    return marked
```

### `u111-a.A7_content_compared`

The node judge no longer compares the content table

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u111-a.json`, row `A7_content_compared`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_nodes.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_rb_writer_guard.py`
- Collected: 242 against a baseline of 242
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
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_nodes.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_rb_writer_guard.py`
- Collected: 242 against a baseline of 242
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
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_nodes.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_rb_writer_guard.py`
- Collected: 242 against a baseline of 242
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
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_nodes.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_rb_writer_guard.py`
- Collected: 242 against a baseline of 242
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
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_nodes.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_rb_writer_guard.py`
- Collected: 242 against a baseline of 242
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
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_nodes.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_rb_writer_guard.py`
- Collected: 242 against a baseline of 242
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
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_nodes.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_favorites_colour_read.py`, `tests/test_favorites_placement.py`, `tests/test_genre_favorites.py`, `tests/test_genre_favorites_adoption.py`, `tests/test_genre_retag.py`, `tests/test_head_agreement.py`, `tests/test_inbox_rotate.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_metadata_policy.py`, `tests/test_naming_apply_cli.py`, `tests/test_organize.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_process_guard.py`, `tests/test_queued_resume_contract.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_snapshot.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_whitelist_membership.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 4190 against a baseline of 4190
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
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_nodes.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_favorites_colour_read.py`, `tests/test_favorites_placement.py`, `tests/test_genre_favorites.py`, `tests/test_genre_favorites_adoption.py`, `tests/test_genre_retag.py`, `tests/test_head_agreement.py`, `tests/test_inbox_rotate.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_metadata_policy.py`, `tests/test_naming_apply_cli.py`, `tests/test_organize.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_process_guard.py`, `tests/test_queued_resume_contract.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_snapshot.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_whitelist_membership.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 4190 against a baseline of 4190
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
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_nodes.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
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

### `r1890.P2_system_exit_in_rb_probes`

rb_probes, a part, exits the process with SystemExit when a listed process has no probe

- File: `src/cratekit/core/rb_probes.py`
- Source: `r1890.json`, row `P2_system_exit_in_rb_probes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_parts_guard.py`, `tests/test_rb_writer_guard.py`
- Collected: 221 against a baseline of 221
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
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_probes.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`, `tests/test_rb_writer_guard.py`
- Collected: 270 against a baseline of 270
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
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_probes.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_rb_writer_guard.py`
- Collected: 258 against a baseline of 258
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
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_probes.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`, `tests/test_rb_writer_guard.py`
- Collected: 270 against a baseline of 270
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
- Collected: 256 against a baseline of 256
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
- Collected: 268 against a baseline of 268
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
        f'WHERE "ID" = :key AND "{TRACK_NUMBER_COLUMN}" = :before'
```

New text:

```
        f'WHERE "ID" = :key AND :before = :before'
```

