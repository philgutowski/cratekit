# Mutation table: u300-replay-after-d

Measured by `scripts/mutate.py` on 2026-11-22 23:11 UTC, branch `HEAD` at `fff6aa63`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 84.

Full baseline: measured by this driver (the battery's verdict was not read: it is for commit `8b809bd22ca3`, and this tree is at `fff6aa634f04`).

Subset baselines: 16, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `/tmp/kf.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r349-b.B1_absent_is_none` | `src/cratekit/core/backup_facts.py` | user | 1 file(s) | 99 | 1 | killed |
| `r349-c.C3_unparseable_reported` | `src/cratekit/core/backup_facts.py` | user | 1 file(s) | 99 | 1 | killed |
| `r757-b2.F1_absent_key_reads_as_never` | `src/cratekit/core/backup_facts.py` | user | 4 file(s) | 758 | 1 | killed |
| `r757-b2.F2_first_record_erases_the_implied_date` | `src/cratekit/core/backup_facts.py` | user | 4 file(s) | 758 | 1 | killed |
| `r757-b2.F3_full_record_does_not_move_the_date` | `src/cratekit/core/backup_facts.py` | user | 4 file(s) | 758 | 4 | killed |
| `u45-round-1.E8_naive_timestamp_stored` | `src/cratekit/core/backup_facts.py` | user | 5 file(s) | 1102 | 1 | killed |
| `u219.M2_disposition_cleared` | `src/cratekit/core/convergence.py` | user | 16 file(s) | 1014 | 1 | killed |
| `u157.C1_at_the_cut` | `src/cratekit/core/drift.py` | user | 3 file(s) | 129 | 2 | killed |
| `u157.C2_verdict_tag_trusted` | `src/cratekit/core/drift.py` | user | 3 file(s) | 129 | 5 | killed |
| `u157.C3_negative_score` | `src/cratekit/core/drift.py` | user | 3 file(s) | 129 | 1 | killed |
| `r1372.K10_carried_read_error_silent` | `src/cratekit/core/held_plan.py` | user | 7 file(s) | 227 | 2 | killed |
| `r1372.K11_carried_place_unchecked` | `src/cratekit/core/held_plan.py` | maintainer | 7 file(s) | 227 | 1 | killed |
| `r1372.K12_carried_run_unchecked` | `src/cratekit/core/held_plan.py` | maintainer | 7 file(s) | 227 | 1 | killed |
| `r1372.K14_unlistable_read_as_none` | `src/cratekit/core/held_plan.py` | user | 7 file(s) | 227 | 1 | killed |
| `r1372.K15_let_go_keeps` | `src/cratekit/core/held_plan.py` | user | 7 file(s) | 227 | 5 | killed |
| `r1372.K2_carry_writes_nothing` | `src/cratekit/core/held_plan.py` | user | 7 file(s) | 227 | 15 | killed |
| `r1372.K3_carry_empty_steps` | `src/cratekit/core/held_plan.py` | user | 7 file(s) | 227 | 10 | killed |
| `r1372.K5_carried_under_held_plans` | `src/cratekit/core/held_plan.py` | user | 7 file(s) | 227 | 3 | killed |
| `u209.H4_load_digest_unchecked` | `src/cratekit/core/held_plan.py` | user | 5 file(s) | 206 | 1 | killed |
| `u209.H6_load_age_unchecked` | `src/cratekit/core/held_plan.py` | user | 5 file(s) | 206 | 1 | killed |
| `u225.M12_age_unchecked` | `src/cratekit/core/held_plan.py` | user | 7 file(s) | 227 | 1 | killed |
| `u225.M13_unreadable_silent` | `src/cratekit/core/held_plan.py` | user | 7 file(s) | 227 | 2 | killed |
| `u285.M10_no_offset_edge` | `src/cratekit/core/rb_dates.py` | user | 4 file(s) | 289 | 15 | killed |
| `u285.M11_value_error_message` | `src/cratekit/core/rb_dates.py` | user | 4 file(s) | 289 | 2 | killed |
| `u285.M12_xml_bound_dropped` | `src/cratekit/core/rb_dates.py` | user | 4 file(s) | 289 | 4 | killed |
| `u285.M13_xml_empty_update` | `src/cratekit/core/rb_dates.py` | maintainer | 4 file(s) | 289 | 1 | killed |
| `u285.M14_xml_update_installed` | `src/cratekit/core/rb_dates.py` | user | 4 file(s) | 289 | 5 | killed |
| `u285.M2_overflow_reads_as_edge` | `src/cratekit/core/rb_dates.py` | user | 4 file(s) | 289 | 24 | killed |
| `u285.M3_edge_hides_real_overflow` | `src/cratekit/core/rb_dates.py` | user | 4 file(s) | 289 | 2 | killed |
| `u285.M4_floor_clamp` | `src/cratekit/core/rb_dates.py` | user | 4 file(s) | 289 | 5 | killed |
| `u285.M5_ceiling_clamp` | `src/cratekit/core/rb_dates.py` | user | 4 file(s) | 289 | 3 | killed |
| `u285.M6_floor_value` | `src/cratekit/core/rb_dates.py` | user | 4 file(s) | 289 | 11 | killed |
| `u285.M7_ceiling_value` | `src/cratekit/core/rb_dates.py` | user | 4 file(s) | 289 | 10 | killed |
| `u285.M8_install_once` | `src/cratekit/core/rb_dates.py` | maintainer | 4 file(s) | 289 | 1 | killed |
| `u285.M9_aware_passes` | `src/cratekit/core/rb_dates.py` | maintainer | 4 file(s) | 289 | 1 | killed |
| `u162.R10_latest_verb` | `src/cratekit/core/rehearsal.py` | user | 2 file(s) | 95 | 1 | killed |
| `u162.R1_area_exists` | `src/cratekit/core/rehearsal.py` | user | 2 file(s) | 95 | 1 | killed |
| `u162.R2_rekordbox_closed` | `src/cratekit/core/rehearsal.py` | user | 2 file(s) | 95 | 1 | killed |
| `u162.R3_clone_is_a_link` | `src/cratekit/core/rehearsal.py` | user | 2 file(s) | 95 | 1 | killed |
| `u162.R4_snapshots_copied` | `src/cratekit/core/rehearsal.py` | maintainer | 2 file(s) | 95 | 1 | killed |
| `u162.R5_locks_copied` | `src/cratekit/core/rehearsal.py` | maintainer | 2 file(s) | 95 | 1 | killed |
| `u162.R7_witness_database` | `src/cratekit/core/rehearsal.py` | user | 2 file(s) | 95 | 1 | killed |
| `u162.R8_witness_folders` | `src/cratekit/core/rehearsal.py` | user | 2 file(s) | 95 | 3 | killed |
| `u162.R9_latest_key` | `src/cratekit/core/rehearsal.py` | user | 2 file(s) | 95 | 2 | killed |
| `u188.M14_mapped_in_given_order` | `src/cratekit/core/rehearsal.py` | user | 1 file(s) | 36 | 1 | killed |
| `u188.M15_mapped_shortest_first` | `src/cratekit/core/rehearsal.py` | user | 1 file(s) | 36 | 1 | killed |
| `u188.M16_mapped_by_live_length` | `src/cratekit/core/rehearsal.py` | user | 1 file(s) | 36 | 1 | killed |
| `u188.M17_empty_scratch_kept` | `src/cratekit/core/rehearsal.py` | user | 1 file(s) | 36 | 1 | killed |
| `u206.M20_rehearsal_cache_not_kept_live` | `src/cratekit/core/rehearsal.py` | user | 9 file(s) | 1135 | 1 | killed |
| `r431-a.A1_a_plain_row_gains_a_companion` | `src/cratekit/core/tombstone.py` | user | 6 file(s) | 1270 | 21 | killed |
| `r431-a.A2_one_kind_for_both` | `src/cratekit/core/tombstone.py` | user | 6 file(s) | 1270 | 17 | killed |
| `r1255.T1_tree_registry_clause` | `src/cratekit/core/tree_registry.py` | user | 3 file(s) | 125 | 2 | killed |
| `r235-a.M13_snapshot_check_dropped` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 11 | killed |
| `r235-a.M1_unreadable_log_skipped` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 2 | killed |
| `r235-a.M2_margin_zero` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 1 | killed |
| `r235-a.M3_margin_two_days` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 1 | killed |
| `r235-a.M4_unparseable_start_predates` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 1 | killed |
| `r235-a.M5_updates_not_counted` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 1 | killed |
| `r235-a.M6_any_tree_counts` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 2 | killed |
| `r235-a.M7_zero_count_counts` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 2 | killed |
| `r235-a.M8_open_run_reverts` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 1 | killed |
| `r235-a.M9_library_guard_removed` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 4 | killed |
| `r235-b.M14_empty_export_accepted` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 1 | killed |
| `r501-a.T1_precheck_excusal` | `src/cratekit/core/tree_registry.py` | user | 5 file(s) | 175 | 4 | killed |
| `r787.S1_set_drops_intake` | `src/cratekit/core/tree_registry.py` | user | 20 file(s) | 2697 | 7 | killed |
| `r235-a.M12_second_record_replaces` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 1 | killed |

## Row definitions

### `r349-b.B1_absent_is_none`

A job with no outcome directory reports an empty mapping rather than no field

- File: `src/cratekit/core/backup_facts.py`
- Source: `r349-b.json`, row `B1_absent_is_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
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
- Collected: 99 against a baseline of 99
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
- Collected: 758 against a baseline of 758
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
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 758 against a baseline of 758
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_comparison.py::test_a_fact_file_from_a_build_with_one_mode_reads_as_a_full_comparison`

Old text:

```
        held = _as_held(read.get(Portion.FILES))
```

New text:

```
        held = None
```

### `r757-b2.F3_full_record_does_not_move_the_date`

record: ignore full_comparison=True

- File: `src/cratekit/core/backup_facts.py`
- Source: `r757-b2.json`, row `F3_full_record_does_not_move_the_date`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 758 against a baseline of 758
- Kills: 4 (killed)
- Killed:
  - `tests/test_backup_comparison.py::test_a_damaged_full_comparison_entry_refuses_its_own_reader_and_no_other`
  - `tests/test_backup_comparison.py::test_a_record_a_few_minutes_ahead_is_zero_days_old_and_not_minus_one`
  - `tests/test_backup_comparison.py::test_doctor_refuses_a_full_comparison_recorded_ahead_of_now`
  - `tests/test_backup_comparison.py::test_doctor_says_how_long_ago_a_full_comparison_last_ran`

Old text:

```
    if full_comparison:
        held = _as_held(facts[portion])
```

New text:

```
    if False:
        held = _as_held(facts[portion])
```

### `u45-round-1.E8_naive_timestamp_stored`

Accept a naive completion timestamp at the boundary, so the instant recorded depends on who reads it

- File: `src/cratekit/core/backup_facts.py`
- Source: `u45-round-1.json`, row `E8_naive_timestamp_stored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_reserved_causes.py`, `tests/test_write_session.py`
- Collected: 1102 against a baseline of 1102
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

### `u219.M2_disposition_cleared`

mark_unconverged: a second restore of the same reason leaves a disposed tree's acceptance standing (round two's second hold)

- File: `src/cratekit/core/convergence.py`
- Source: `u219.json`, row `M2_disposition_cleared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_deferred_routing.py`, `tests/test_genre_favorites.py`, `tests/test_organize_inspiration.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_rebuild.py`, `tests/test_resort_scope.py`, `tests/test_restore.py`, `tests/test_sync_pair_back.py`, `tests/test_tag_rows.py`, `tests/test_tree_writer.py`
- Collected: 1014 against a baseline of 1014
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
- Collected: 129 against a baseline of 129
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
- Collected: 129 against a baseline of 129
- Kills: 5 (killed)
- Killed:
  - `tests/test_drift.py::test_a_landing_reads_the_score_against_the_cut_now_and_the_verdict_only_for_unknown[infinite]`
  - `tests/test_drift.py::test_a_landing_reads_the_score_against_the_cut_now_and_the_verdict_only_for_unknown[negative]`
  - `tests/test_drift.py::test_a_landing_reads_the_score_against_the_cut_now_and_the_verdict_only_for_unknown[not-a-number]`
  - `tests/test_drift.py::test_a_landing_reads_the_score_against_the_cut_now_and_the_verdict_only_for_unknown[verdict-without-score]`
  - `tests/test_intake_land_dyn_native.py::test_a_score_that_is_not_a_number_is_unscored_whatever_its_verdict_says`

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
- Collected: 129 against a baseline of 129
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
- Collected: 206 against a baseline of 206
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
- Collected: 206 against a baseline of 206
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

### `u285.M10_no_offset_edge`

placeable: catch OverflowError alone, so a year 1 stamp with no offset fails its row with ValueError in every zone

- File: `src/cratekit/core/rb_dates.py`
- Source: `u285.json`, row `M10_no_offset_edge`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_dates.py`, `tests/test_organize.py`, `tests/test_rebuild.py`, `tests/test_foreign_tree.py`
- Collected: 289 against a baseline of 289
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
- Collected: 289 against a baseline of 289
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
- Collected: 289 against a baseline of 289
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
- Collected: 289 against a baseline of 289
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
- Collected: 289 against a baseline of 289
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
- Collected: 289 against a baseline of 289
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
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_dates.py`, `tests/test_organize.py`, `tests/test_rebuild.py`, `tests/test_foreign_tree.py`
- Collected: 289 against a baseline of 289
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_dates.py::test_an_overflow_away_from_the_calendars_edge_is_raised_as_it_came`
  - `tests/test_rb_dates.py::test_text_the_binding_cannot_parse_still_fails_as_it_did[0000-01-01 00:00:00]`

Old text:

```
    if year == CEILING.year:
        return CEILING
    return None
```

New text:

```
    if year == CEILING.year:
        return CEILING
    return FLOOR
```

### `u285.M4_floor_clamp`

placeable: drop the floor clamp, so east of UTC the zero date reads as 0001-01-01 09:00, which a reader cannot convert again

- File: `src/cratekit/core/rb_dates.py`
- Source: `u285.json`, row `M4_floor_clamp`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_dates.py`, `tests/test_organize.py`, `tests/test_rebuild.py`, `tests/test_foreign_tree.py`
- Collected: 289 against a baseline of 289
- Kills: 5 (killed)
- Killed:
  - `tests/test_rb_dates.py::test_a_commit_leaves_the_pushed_nodes_xml_timestamps_and_still_syncs_its_own[JST-9]`
  - `tests/test_rb_dates.py::test_a_commit_leaves_the_pushed_nodes_xml_timestamps_and_still_syncs_its_own[UTC0]`
  - `tests/test_rb_dates.py::test_the_zero_date_reads_as_the_floor_in_every_zone[JST-9]`
  - `tests/test_rb_dates.py::test_the_zero_date_reads_as_the_floor_in_every_zone[LINT-14]`
  - `tests/test_rb_dates.py::test_the_zero_date_reads_as_the_floor_in_every_zone[UTC0]`

Old text:

```
        if moment < FLOOR:
            return FLOOR
```

New text:

```
        if False:
            return FLOOR
```

### `u285.M5_ceiling_clamp`

placeable: drop the ceiling clamp, so west of UTC the calendar's last moment reads as itself, unconvertible again

- File: `src/cratekit/core/rb_dates.py`
- Source: `u285.json`, row `M5_ceiling_clamp`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_dates.py`, `tests/test_organize.py`, `tests/test_rebuild.py`, `tests/test_foreign_tree.py`
- Collected: 289 against a baseline of 289
- Kills: 3 (killed)
- Killed:
  - `tests/test_rb_dates.py::test_the_calendars_last_moment_reads_as_the_ceiling[AOE+12]`
  - `tests/test_rb_dates.py::test_the_calendars_last_moment_reads_as_the_ceiling[EST5EDT,M3.2.0,M11.1.0]`
  - `tests/test_rb_dates.py::test_the_calendars_last_moment_reads_as_the_ceiling[UTC0]`

Old text:

```
        if moment > CEILING:
            return CEILING
```

New text:

```
        if False:
            return CEILING
```

### `u285.M6_floor_value`

FLOOR: the calendar's first day rather than a day inside it, which no zone can convert back

- File: `src/cratekit/core/rb_dates.py`
- Source: `u285.json`, row `M6_floor_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_dates.py`, `tests/test_organize.py`, `tests/test_rebuild.py`, `tests/test_foreign_tree.py`
- Collected: 289 against a baseline of 289
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
- Collected: 289 against a baseline of 289
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
- Collected: 289 against a baseline of 289
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
- Collected: 289 against a baseline of 289
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

### `u162.R10_latest_verb`

latest: match a record by key alone, so another verb's rehearsal is compared

- File: `src/cratekit/core/rehearsal.py`
- Source: `u162.json`, row `R10_latest_verb`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_land_cli_reads_the_newest_rehearsal_of_its_folder_and_batch`

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
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_two_rehearsals_use_two_areas_and_one_area_is_never_shared`

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
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_with_rekordbox_running_refuses_and_copies_nothing`

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
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_clone_is_never_a_hard_link`

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
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_the_area_copies_library_state_but_no_lock_snapshot_or_session`

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
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_the_area_copies_library_state_but_no_lock_snapshot_or_session`

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
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_the_witness_refuses_a_live_database_that_changed`

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
- Collected: 95 against a baseline of 95
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_a_batch_filed_in_another_year_is_refused`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_the_live_library_is_refused_as_a_defect`
  - `tests/test_intake_land_rehearse.py::test_the_witness_refuses_a_live_folder_that_changed`

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
- Collected: 95 against a baseline of 95
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_of_another_batch_is_not_the_one_compared`
  - `tests/test_intake_land_rehearse.py::test_land_cli_reads_the_newest_rehearsal_of_its_folder_and_batch`

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
- Collected: 36 against a baseline of 36
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_mapped_applies_the_longest_scratch_spelling_first_and_ignores_an_empty_one`

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
- Collected: 36 against a baseline of 36
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_mapped_applies_the_longest_scratch_spelling_first_and_ignores_an_empty_one`

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
- Collected: 36 against a baseline of 36
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_mapped_applies_the_longest_scratch_spelling_first_and_ignores_an_empty_one`

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
- Collected: 36 against a baseline of 36
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_mapped_applies_the_longest_scratch_spelling_first_and_ignores_an_empty_one`

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
- Collected: 1135 against a baseline of 1135
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

### `r431-a.A1_a_plain_row_gains_a_companion`

uncredited_title answers the stripped title even when nothing was stripped, so a plain deletion writes a companion

- File: `src/cratekit/core/tombstone.py`
- Source: `r431-a.json`, row `A1_a_plain_row_gains_a_companion`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_deletion.py`, `tests/test_label_workers.py`, `tests/test_match_states.py`, `tests/test_tombstones.py`, `tests/test_uncredited_tombstone.py`
- Collected: 1270 against a baseline of 1270
- Kills: 21 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_confirmed_removal_the_person_deleted_in_the_finder_does_not_block_the_next_one`
  - `tests/test_deletion.py::test_a_file_moved_by_hand_after_the_confirmation_is_recorded_rather_than_retired_silently`
  - `tests/test_deletion.py::test_a_listing_says_which_suppressions_moved_no_file`
  - `tests/test_deletion.py::test_a_run_interrupted_after_trashing_resumes_without_re_offering`
  - `tests/test_deletion.py::test_a_tombstone_that_cannot_be_written_puts_the_file_back`
  - `tests/test_deletion.py::test_an_interrupt_during_the_store_write_still_puts_the_file_back[ctrl-c]`
  - `tests/test_deletion.py::test_an_interrupt_during_the_store_write_still_puts_the_file_back[sigterm]`
  - `tests/test_deletion.py::test_one_file_deleted_by_hand_under_a_healthy_anchor_is_still_settled`
  - `tests/test_deletion.py::test_the_listing_carries_the_column_value_a_missed_tombstone_was_built_from`
  - `tests/test_deletion.py::test_tombstone_list_revokes_and_then_shows_the_lifted_record`
  - `tests/test_deletion.py::test_tombstone_list_shows_what_the_deletion_pass_suppressed`
  - `tests/test_match_states.py::test_a_deletion_of_the_plain_record_writes_no_companion`
  - `tests/test_match_states.py::test_the_two_copies_of_the_tombstone_identity_agree_once_both_exist`
  - `tests/test_tombstones.py::test_a_revoked_tombstone_stays_listable_so_the_two_cases_can_be_told_apart`
  - `tests/test_uncredited_tombstone.py::test_a_credited_deletion_is_two_records_and_a_plain_one_is_one`
  - ... and 6 more, see the JSON sidecar

Old text:

```
    return stripped if dropped else ""
```

New text:

```
    return stripped
```

### `r431-a.A2_one_kind_for_both`

The companion is recorded under the tombstone's own kind, where every verbatim lookup lands on it

- File: `src/cratekit/core/tombstone.py`
- Source: `r431-a.json`, row `A2_one_kind_for_both`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_deletion.py`, `tests/test_label_workers.py`, `tests/test_match_states.py`, `tests/test_tombstones.py`, `tests/test_uncredited_tombstone.py`
- Collected: 1270 against a baseline of 1270
- Kills: 17 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_held_file_crediting_somebody_else_never_calls_the_companion_stale`
  - `tests/test_match_states.py::test_the_two_copies_of_the_tombstone_identity_agree_once_both_exist`
  - `tests/test_uncredited_tombstone.py::test_a_companion_already_lifted_keeps_the_lift_it_was_given`
  - `tests/test_uncredited_tombstone.py::test_a_companion_is_never_the_answer_to_a_verbatim_lookup`
  - `tests/test_uncredited_tombstone.py::test_a_companion_lifted_alone_does_not_come_back_behind_a_persons_back`
  - `tests/test_uncredited_tombstone.py::test_a_companion_never_says_a_run_recorded_a_different_rows_deletion`
  - `tests/test_uncredited_tombstone.py::test_a_companion_two_deletions_share_outlives_the_first_lift_and_not_the_second`
  - `tests/test_uncredited_tombstone.py::test_a_credited_deletion_is_two_records_and_a_plain_one_is_one`
  - `tests/test_uncredited_tombstone.py::test_a_second_deletion_leaves_the_shared_companion_exactly_as_it_stood`
  - `tests/test_uncredited_tombstone.py::test_a_shared_companion_survives_a_lift_even_when_the_stripping_rule_has_moved`
  - `tests/test_uncredited_tombstone.py::test_a_tombstone_with_no_pointer_still_accounts_for_the_companion_it_strips_to`
  - `tests/test_uncredited_tombstone.py::test_deleting_again_after_a_full_lift_suppresses_both_halves_again`
  - `tests/test_uncredited_tombstone.py::test_lifting_a_credited_tombstone_lifts_its_companion`
  - `tests/test_uncredited_tombstone.py::test_lifting_a_plain_tombstone_touches_no_companion_it_does_not_own`
  - `tests/test_uncredited_tombstone.py::test_lifting_the_companion_alone_leaves_the_tombstone_standing`
  - ... and 2 more, see the JSON sidecar

Old text:

```
KIND_VERSION_UNCREDITED = "version-uncredited"
```

New text:

```
KIND_VERSION_UNCREDITED = "version"
```

### `r1255.T1_tree_registry_clause`

tree_registry._whole_log: word the refusal with the old count, not the clause

- File: `src/cratekit/core/tree_registry.py`
- Source: `r1255.json`, row `T1_tree_registry_clause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_tree_registry.py`, `tests/test_cutover_precheck.py`
- Collected: 125 against a baseline of 125
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_an_unreadable_record_keeps_its_own_refusal`
  - `tests/test_session_log_unlisted.py::test_the_tree_registry_refuses_rather_than_read_no_open_run`

Old text:

```
            f"{session.unread_clause(unreadable, cfg)}, so {so}; refusing rather than "
```

New text:

```
            f"the session log holds {len(unreadable)} entries this build cannot read, so {so}; refusing rather than "
```

### `r235-a.M13_snapshot_check_dropped`

the verified snapshot check is no longer in the precheck table

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M13_snapshot_check_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 11 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_each_precheck_failure_refuses_before_anything_is_recorded[_leave_intake_xml-cutover-xml-pending-no-pending-intake-xml]`
  - `tests/test_cutover_cli.py::test_each_precheck_failure_refuses_before_anything_is_recorded[_open_a_run-cutover-open-run-no-open-run]`
  - `tests/test_cutover_cli.py::test_each_precheck_failure_refuses_before_anything_is_recorded[_remove_the_export-cutover-export-missing-fresh-export]`
  - `tests/test_cutover_cli.py::test_each_precheck_failure_refuses_before_anything_is_recorded[_remove_the_snapshot-cutover-snapshot-missing-verified-snapshot]`
  - `tests/test_cutover_cli.py::test_the_plan_names_the_root_and_approval_records_that_tree_alone`
  - `tests/test_cutover_cli.py::test_two_failing_prechecks_are_both_named_on_one_run`
  - `tests/test_cutover_precheck.py::test_a_missing_snapshot_blocks_the_flip`
  - `tests/test_cutover_precheck.py::test_an_unverified_capture_does_not_count_as_a_snapshot`
  - `tests/test_cutover_precheck.py::test_the_report_and_the_assertion_refuse_with_one_cause`
  - `tests/test_cutover_precheck.py::test_the_report_carries_each_refusal_and_does_not_stop_at_the_first`
  - `tests/test_cutover_precheck.py::test_the_report_names_every_check_in_the_order_the_assertion_refuses`

Old text:

```
    ("fresh-export", _export_refusal),
    ("verified-snapshot", _snapshot_refusal),
)
```

New text:

```
    ("fresh-export", _export_refusal),
)
```

### `r235-a.M1_unreadable_log_skipped`

the registry gates no longer refuse on a session record they cannot read, so a torn record reads as no open run and no native write

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M1_unreadable_log_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 2 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_a_record_nobody_can_read_refuses_the_flip_rather_than_reading_as_no_open_run`
  - `tests/test_cutover_precheck.py::test_a_record_nobody_can_read_refuses_the_revert_rather_than_reading_as_no_write`

Old text:

```
    parsed, unreadable = session.scan_log(cfg)
    if unreadable:
```

New text:

```
    parsed, unreadable = session.scan_log(cfg)
    if False:
```

### `r235-a.M2_margin_zero`

the native write margin is no days, so a write whose universal time date is the day before the cutover day is left out

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M2_margin_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_a_write_that_cannot_be_shown_to_predate_the_cutover_counts[2026-07-31T23:50:00Z]`

Old text:

```
NATIVE_WRITE_MARGIN = timedelta(days=1)
```

New text:

```
NATIVE_WRITE_MARGIN = timedelta(days=0)
```

### `r235-a.M3_margin_two_days`

the native write margin is two days, so a write two days before the cutover day still counts

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M3_margin_two_days`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_the_day_before_the_margin_is_the_first_day_left_out`

Old text:

```
NATIVE_WRITE_MARGIN = timedelta(days=1)
```

New text:

```
NATIVE_WRITE_MARGIN = timedelta(days=2)
```

### `r235-a.M4_unparseable_start_predates`

a session start nothing can parse is read as before the cutover, so its write does not count

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M4_unparseable_start_predates`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_a_write_that_cannot_be_shown_to_predate_the_cutover_counts[not a timestamp]`

Old text:

```
    except ValueError:
        return False
    return began < cutover_on - NATIVE_WRITE_MARGIN
```

New text:

```
    except ValueError:
        return True
    return began < cutover_on - NATIVE_WRITE_MARGIN
```

### `r235-a.M5_updates_not_counted`

only a creation counts as a native write, an update does not

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M5_updates_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_an_update_counts_as_a_native_write_as_a_creation_does`

Old text:

```
            change.tree == tree_id and (change.created > 0 or change.updated > 0)
```

New text:

```
            change.tree == tree_id and change.created > 0
```

### `r235-a.M6_any_tree_counts`

a write to any tree counts as a write to this one

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M6_any_tree_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 2 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_a_write_to_another_tree_does_not_close_this_trees_door`
  - `tests/test_cutover_precheck.py::test_a_session_that_wrote_nothing_to_this_tree_leaves_the_revert_open`

Old text:

```
            change.tree == tree_id and (change.created > 0 or change.updated > 0)
```

New text:

```
            (change.created > 0 or change.updated > 0)
```

### `r235-a.M7_zero_count_counts`

a record naming the tree with nothing added counts as a native write

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M7_zero_count_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 2 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_a_write_to_another_tree_does_not_close_this_trees_door`
  - `tests/test_cutover_precheck.py::test_a_session_that_wrote_nothing_to_this_tree_leaves_the_revert_open`

Old text:

```
            change.tree == tree_id and (change.created > 0 or change.updated > 0)
```

New text:

```
            change.tree == tree_id
```

### `r235-a.M8_open_run_reverts`

a revert no longer refuses over an open run

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M8_open_run_reverts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_an_open_run_refuses_the_revert_because_it_may_have_written`

Old text:

```
    if open_runs:
        raise refuse(
            "cutover-open-run",
            f"session {open_runs[0].session_id} has not reached a terminal "
```

New text:

```
    if False:
        raise refuse(
            "cutover-open-run",
            f"session {open_runs[0].session_id} has not reached a terminal "
```

### `r235-a.M9_library_guard_removed`

revert_cutover no longer asserts the tree is revertible, leaving only the verb's own check

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M9_library_guard_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 4 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_a_record_nobody_can_read_refuses_the_revert_rather_than_reading_as_no_write`
  - `tests/test_cutover_precheck.py::test_a_revert_after_a_native_write_is_refused_by_the_library_itself`
  - `tests/test_cutover_precheck.py::test_an_open_run_refuses_the_revert_because_it_may_have_written`
  - `tests/test_cutover_precheck.py::test_the_revert_holds_the_session_lock_while_it_asks_and_writes`

Old text:

```
        assert_revertible(cfg, tree_id)
        updated = read(cfg).without_record(tree_id)
```

New text:

```
        updated = read(cfg).without_record(tree_id)
```

### `r235-b.M14_empty_export_accepted`

an export of no bytes passes the fresh export check

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-b.json`, row `M14_empty_export_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_an_empty_export_is_no_export`

Old text:

```
    if export_path.is_file() and export_path.stat().st_size != 0:
```

New text:

```
    if export_path.is_file():
```

### `r501-a.T1_precheck_excusal`

tree_registry.assert_cutover_ready: drop the excusal, so a proven landing refuses the cutover for ever, which is R-501 itself

- File: `src/cratekit/core/tree_registry.py`
- Source: `r501-a.json`, row `T1_precheck_excusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 175 against a baseline of 175
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_landing_followed_step_by_step_passes_the_cutover_precheck`
  - `tests/test_intake_imported.py::test_a_run_landed_before_the_fix_is_settled_too`
  - `tests/test_intake_imported.py::test_intake_file_ends_pending_and_is_settled_the_same_way`
  - `tests/test_intake_imported.py::test_the_precheck_excuses_a_verified_run_holding_no_capture`

Old text:

```
        if not record.terminal and not session.owes_only_deferred_routing(record)
```

New text:

```
        if not record.terminal
```

### `r787.S1_set_drops_intake`

cutover_trees returns the routing tree alone, the list doctor held before R-787

- File: `src/cratekit/core/tree_registry.py`
- Source: `r787.json`, row `S1_set_drops_intake`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_intake_imported.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_landing_labels.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_tree_registry.py`, `tests/test_tree_writer.py`, `tests/test_xml_import_coexistence.py`, `tests/test_xml_splice_golden.py`
- Collected: 2697 against a baseline of 2697
- Kills: 7 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_a_tree_the_taxonomy_does_not_declare_is_refused`
  - `tests/test_cutover_cli.py::test_doctor_and_the_verb_read_one_set_of_cutover_trees`
  - `tests/test_cutover_cli.py::test_doctor_fails_on_a_native_record_the_cutover_would_refuse_to_create`
  - `tests/test_cutover_cli.py::test_doctor_reads_a_native_inbox_record_as_ok`
  - `tests/test_cutover_cli.py::test_doctor_reads_an_inbox_the_verb_cut_over_as_ok`
  - `tests/test_cutover_cli.py::test_the_catalogue_tree_is_refused_as_not_rebuildable`
  - `tests/test_cutover_cli.py::test_the_intake_tree_cuts_over_on_the_same_answer_as_the_routing_tree`

Old text:

```
    return frozenset({declared.tree.id, declared.intake.id})
```

New text:

```
    return frozenset({declared.tree.id})
```

### `r235-a.M12_second_record_replaces`

record_cutover replaces a tree already recorded native instead of refusing

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M12_second_record_replaces`
- Moved: the same guard in the same file and function, its comment cut to its rule and reason by U300's prose pass, so the text the row names changed and the condition it falsifies did not
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_a_tree_already_recorded_is_not_recorded_again`

Old text:

```
        if standing is not None and standing.mode == Mode.DATABASE:
            # Asked under the lock, so two cutovers of one tree cannot both pass.
```

New text:

```
        if False:
            # Asked under the lock, so two cutovers of one tree cannot both pass.
```

