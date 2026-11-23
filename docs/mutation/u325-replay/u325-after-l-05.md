# Mutation table: u325-after-l-05

Measured by `scripts/mutate.py` on 2026-11-22 22:22 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 90.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:21 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 4, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r598-a.A2_no_holder_read_as_gone` | `src/cratekit/core/session.py` | user | 3 file(s) | 602 | 3 | killed |
| `r598-a.A3_liveness_not_consulted` | `src/cratekit/core/session.py` | user | 3 file(s) | 602 | 8 | killed |
| `r598-a.A4_unreadable_holder_read_as_gone` | `src/cratekit/core/session.py` | user | 3 file(s) | 602 | 1 | killed |
| `r598-a.A5_holder_never_recorded` | `src/cratekit/core/session.py` | user | 3 file(s) | 602 | 8 | killed |
| `r647-a.B10_live_identifier_not_asked` | `src/cratekit/core/session.py` | user | 3 file(s) | 602 | 3 | killed |
| `r647-a.B11_start_time_compared_again` | `src/cratekit/core/session.py` | user | 3 file(s) | 602 | 1 | killed |
| `r647-a.B12_cross_boot_never_judged` | `src/cratekit/core/session.py` | user | 3 file(s) | 602 | 4 | killed |
| `r647-a.B13_current_holder_names_no_machine` | `src/cratekit/core/session.py` | user | 3 file(s) | 602 | 3 | killed |
| `r647-a.B14_machine_not_read_back` | `src/cratekit/core/session.py` | user | 3 file(s) | 602 | 5 | killed |
| `r647-a.B15_machine_not_written` | `src/cratekit/core/session.py` | user | 3 file(s) | 602 | 5 | killed |
| `r647-a.B1_unknown_machine_not_refused` | `src/cratekit/core/session.py` | user | 3 file(s) | 602 | 1 | killed |
| `r647-a.B2_machine_equality_dropped` | `src/cratekit/core/session.py` | user | 3 file(s) | 602 | 3 | killed |
| `r647-a.B3_unparsable_boot_read_as_gone` | `src/cratekit/core/session.py` | user | 3 file(s) | 602 | 1 | killed |
| `r647-a.B4_infinite_boot_accepted` | `src/cratekit/core/session.py` | user | 3 file(s) | 602 | 1 | killed |
| `r647-a.B5_drift_margin_halved` | `src/cratekit/core/session.py` | user | 3 file(s) | 602 | 2 | killed |
| `r647-a.B6_drift_margin_doubled` | `src/cratekit/core/session.py` | user | 3 file(s) | 602 | 1 | killed |
| `r647-a.B7_margin_boundary_exclusive` | `src/cratekit/core/session.py` | user | 3 file(s) | 602 | 1 | killed |
| `r647-a.B8_direction_ignored` | `src/cratekit/core/session.py` | user | 3 file(s) | 602 | 1 | killed |
| `r647-a.B9_platform_silence_read_as_gone` | `src/cratekit/core/session.py` | user | 3 file(s) | 602 | 1 | killed |
| `u249.M01_path_alone` | `src/cratekit/acquire/match.py` | user | 4 file(s) | 817 | 7 | killed |
| `u249.M02_size_out_of_stamp` | `src/cratekit/acquire/match.py` | user | 4 file(s) | 817 | 2 | killed |
| `u249.M03_mtime_out_of_stamp` | `src/cratekit/acquire/match.py` | user | 4 file(s) | 817 | 1 | killed |
| `u249.M04_ctime_out_of_stamp` | `src/cratekit/acquire/match.py` | user | 4 file(s) | 817 | 1 | killed |
| `u249.M05_inode_out_of_stamp` | `src/cratekit/acquire/match.py` | user | 4 file(s) | 817 | 1 | killed |
| `u249.M06_device_out_of_stamp` | `src/cratekit/acquire/match.py` | user | 4 file(s) | 817 | 1 | killed |
| `u249.M07_size_not_stat` | `src/cratekit/acquire/match.py` | user | 4 file(s) | 817 | 2 | killed |
| `u249.M08_template_out_of_key` | `src/cratekit/acquire/match.py` | user | 4 file(s) | 817 | 1 | killed |
| `u249.M09_no_window` | `src/cratekit/acquire/match.py` | user | 4 file(s) | 817 | 4 | killed |
| `u249.M10_window_halved` | `src/cratekit/acquire/match.py` | user | 4 file(s) | 817 | 3 | killed |
| `u249.M11_window_boundary` | `src/cratekit/acquire/match.py` | maintainer | 4 file(s) | 817 | 1 | killed |
| `u249.M12_moment_after_read` | `src/cratekit/acquire/match.py` | user | 4 file(s) | 817 | 1 | killed |
| `u249.M13_failed_read_remembered` | `src/cratekit/acquire/match.py` | user | 4 file(s) | 817 | 3 | killed |
| `u249.M14_unstated_remembered_never` | `src/cratekit/acquire/match.py` | user | 4 file(s) | 817 | 11 | killed |
| `u249.M20_reset_forgets_nothing` | `src/cratekit/acquire/match.py` | maintainer | 4 file(s) | 817 | 6 | killed |
| `u249.M20a_failed_read_keeps_old_entry` | `src/cratekit/acquire/match.py` | user | 4 file(s) | 817 | 1 | killed |
| `r227.C6_composed_limit_spelled` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `r359.M5_unwired` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `r359.M6_no_append` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `r359.M7_note_before_describe` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `r504-b.B10_check_no_numbers` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 3 | killed |
| `r504-b.B7_sync_drops_short` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 3 | killed |
| `r504-b.B8_check_passes` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 3 | killed |
| `r504-b.B9_all_withheld_says_no_hearts` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `r515-operator.S13_sweep_no_warning` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u109-a.A1_plan_guided` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 9 | killed |
| `u109-a.A2_guided_empty` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 6 | killed |
| `u109-a.A3_no_check_row` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 2 | killed |
| `u109-a.A4_summary_guided` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 3 | killed |
| `u109-a.A5_gate_guided` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u109-a.A6_refusal_step_dropped` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 2 | killed |
| `u109-a.A7_refusal_step_first` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u109-a.A8_row_reworded` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u73-c.C3_next_only_with_intake_jobs` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 5 | killed |
| `u73-c.C4_next_counts_intake_jobs_only` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u73-c.C5_next_check_row` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u74-b.B10_refused_check_status` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 3 | killed |
| `u74-b.B11_gate_screen` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u74-b.B12_next_step_outbound_only` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u74-b.B1_source_id_dropped` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 9 | killed |
| `u74-b.B2_compose_skips_inbound` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 16 | killed |
| `u74-b.B3_queue_refusal_raised` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 3 | killed |
| `u74-b.B4_filed_outbound_only` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 10 | killed |
| `u74-b.B5_inbound_refusal_not_counted` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u74-b.B6_inbound_warning` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u74-b.B7_block_dropped` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 13 | killed |
| `u74-b.B8_check_dropped` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 10 | killed |
| `u74-b.B9_check_wording` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u74.A10_export_refusal_raised` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 15 | killed |
| `u74.A11_queue_not_bound` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 17 | killed |
| `u74.A12_run_id_dropped` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 2 | killed |
| `u74.A3_handler_filter` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u74.A4_source_filter` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u74.A5_library_filter` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u74.A6_open_filter` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 3 | killed |
| `u74.A7_in_flight_guard` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 2 | killed |
| `u74.A8_empty_guard` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 4 | killed |
| `u74.A9_listing_refusal_raised` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 19 | killed |
| `r667-b.B1_same_recording_no_isrc` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 729 | 1 | killed |
| `r667-b.B2_reader_isrc_unfolded` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 729 | 2 | killed |
| `r667.E1_title_head_kept` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 729 | 33 | killed |
| `r667.E2_first_copy_only` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 729 | 2 | killed |
| `r667.F1_credited_reason_is_exact` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 729 | 3 | killed |
| `r667.F2_isrc_version_not_settled` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 729 | 1 | killed |
| `r667.F3_doubtful_not_offered` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 729 | 3 | killed |
| `r667.F4_text_copy_joins_isrc_paths` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 729 | 1 | killed |

## Row definitions

### `r598-a.A2_no_holder_read_as_gone`

orphaned: read a record with no recorded holder as orphaned, so every intake landing left open for a deferred placement is abandoned

- File: `src/cratekit/core/session.py`
- Source: `r598-a.json`, row `A2_no_holder_read_as_gone`
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

- File: `src/cratekit/core/session.py`
- Source: `r598-a.json`, row `A3_liveness_not_consulted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 8 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_open_session_whose_process_is_gone_names_the_verb_that_ends_it`
  - `tests/test_session_cli.py::test_a_record_from_another_boot_not_proven_this_machines_is_kept[another-machine-with-this-host-name]`
  - `tests/test_session_cli.py::test_a_record_from_another_boot_not_proven_this_machines_is_kept[recorded-before-the-machine-identity]`
  - `tests/test_session_cli.py::test_a_record_whose_holder_is_alive_is_kept_open`
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

- File: `src/cratekit/core/session.py`
- Source: `r598-a.json`, row `A4_unreadable_holder_read_as_gone`
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

### `r598-a.A5_holder_never_recorded`

open_session: drop the holder instead of recording it, so no record is ever provably orphaned and a hard kill is a dead end again

- File: `src/cratekit/core/session.py`
- Source: `r598-a.json`, row `A5_holder_never_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 8 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_open_session_whose_process_is_gone_names_the_verb_that_ends_it`
  - `tests/test_session_cli.py::test_a_hard_killed_gated_write_blocks_cutover_until_release_abandons_it`
  - `tests/test_session_cli.py::test_a_power_loss_blocks_cutover_until_release_abandons_it`
  - `tests/test_session_cli.py::test_a_release_that_only_abandons_is_a_change_and_passes_the_contract`
  - `tests/test_write_session.py::test_a_supplied_holder_reaches_the_record_as_well_as_the_lock`
  - `tests/test_write_session.py::test_abandon_orphaned_sessions_ends_only_the_orphans`
  - `tests/test_write_session.py::test_the_record_names_the_holder_the_lock_names`
  - `tests/test_write_session.py::test_the_sweep_ends_only_the_orphans_it_was_shown`

Old text:

```
        detail={HOLDER_KEY: holder.to_json()} if holder is not None else {},
```

New text:

```
        detail={},
```

### `r647-a.B10_live_identifier_not_asked`

_gone_since_an_earlier_boot: skip the live process check, so a live holder read through a moved clock has its claim cleared mid write

- File: `src/cratekit/core/session.py`
- Source: `r647-a.json`, row `B10_live_identifier_not_asked`
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
    return process_exists(holder.pid) is False
```

New text:

```
    return True
```

### `r647-a.B11_start_time_compared_again`

_gone_since_an_earlier_boot: the review's defect restored, a live identifier keeps the claim only when its start time matches, so the Linux shape of a stepped clock clears a live claim

- File: `src/cratekit/core/session.py`
- Source: `r647-a.json`, row `B11_start_time_compared_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_live_process_whose_start_time_moved_with_the_clock_is_kept`

Old text:

```
    return process_exists(holder.pid) is False
```

New text:

```
    exists = process_exists(holder.pid)
    if exists is None:
        return False
    return not (exists and process_started(holder.pid) == holder.started)
```

### `r647-a.B12_cross_boot_never_judged`

holder_alive: every other boot judged alive again, the state before this unit, so a power loss stays a dead end

- File: `src/cratekit/core/session.py`
- Source: `r647-a.json`, row `B12_cross_boot_never_judged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_power_loss_blocks_cutover_until_release_abandons_it`
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

- File: `src/cratekit/core/session.py`
- Source: `r647-a.json`, row `B13_current_holder_names_no_machine`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 3 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_power_loss_blocks_cutover_until_release_abandons_it`
  - `tests/test_write_session.py::test_the_lock_left_by_this_machines_earlier_boot_is_releasable`
  - `tests/test_write_session.py::test_this_platform_names_its_machine_as_a_digest_not_the_serial`

Old text:

```
        machine=machine_identity(),
```

New text:

```
        machine=UNKNOWN_IDENTITY,
```

### `r647-a.B14_machine_not_read_back`

Holder.from_json: ignore the recorded machine, so a record or lock read from disk never names one

- File: `src/cratekit/core/session.py`
- Source: `r647-a.json`, row `B14_machine_not_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 5 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_live_holders_claim_is_refused_and_the_lock_file_is_untouched`
  - `tests/test_session_cli.py::test_a_power_loss_blocks_cutover_until_release_abandons_it`
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

- File: `src/cratekit/core/session.py`
- Source: `r647-a.json`, row `B15_machine_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 5 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_live_holders_claim_is_refused_and_the_lock_file_is_untouched`
  - `tests/test_session_cli.py::test_a_power_loss_blocks_cutover_until_release_abandons_it`
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

- File: `src/cratekit/core/session.py`
- Source: `r647-a.json`, row `B1_unknown_machine_not_refused`
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

- File: `src/cratekit/core/session.py`
- Source: `r647-a.json`, row `B2_machine_equality_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 3 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_record_from_another_boot_not_proven_this_machines_is_kept[another-machine-with-this-host-name]`
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

- File: `src/cratekit/core/session.py`
- Source: `r647-a.json`, row `B3_unparsable_boot_read_as_gone`
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

- File: `src/cratekit/core/session.py`
- Source: `r647-a.json`, row `B4_infinite_boot_accepted`
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

- File: `src/cratekit/core/session.py`
- Source: `r647-a.json`, row `B5_drift_margin_halved`
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

### `r647-a.B6_drift_margin_doubled`

BOOT_DRIFT_SECONDS: 60 to 120, so a restart a minute and a half apart is kept for no reason

- File: `src/cratekit/core/session.py`
- Source: `r647-a.json`, row `B6_drift_margin_doubled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_boot_just_past_the_drift_margin_is_gone`

Old text:

```
BOOT_DRIFT_SECONDS = 60.0
```

New text:

```
BOOT_DRIFT_SECONDS = 120.0
```

### `r647-a.B7_margin_boundary_exclusive`

_gone_since_an_earlier_boot: less than instead of less than or equal, so a boot exactly at the margin is judged earlier

- File: `src/cratekit/core/session.py`
- Source: `r647-a.json`, row `B7_margin_boundary_exclusive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_holder_from_another_boot_is_kept_without_proof_it_was_this_machine[a boot exactly at the drift margin-changes3]`

Old text:

```
earlier_by <= BOOT_DRIFT_SECONDS:
```

New text:

```
earlier_by < BOOT_DRIFT_SECONDS:
```

### `r647-a.B8_direction_ignored`

_gone_since_an_earlier_boot: take the distance between the boots rather than which came first, so a LATER boot reading reads as an earlier boot

- File: `src/cratekit/core/session.py`
- Source: `r647-a.json`, row `B8_direction_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_holder_from_another_boot_is_kept_without_proof_it_was_this_machine[a later boot-changes4]`

Old text:

```
        earlier_by = float(reference.boot) - float(holder.boot)
```

New text:

```
        earlier_by = abs(float(reference.boot) - float(holder.boot))
```

### `r647-a.B9_platform_silence_read_as_gone`

_gone_since_an_earlier_boot: read a platform declining to say whether the process exists as gone

- File: `src/cratekit/core/session.py`
- Source: `r647-a.json`, row `B9_platform_silence_read_as_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_platform_that_cannot_say_whether_the_process_exists_keeps_it`

Old text:

```
    return process_exists(holder.pid) is False
```

New text:

```
    return process_exists(holder.pid) is not True
```

### `u249.M01_path_alone`

_read_from_disk: answer any remembered path whatever its stamp, the path alone as identity

- File: `src/cratekit/acquire/match.py`
- Source: `u249.json`, row `M01_path_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 817 against a baseline of 817
- Kills: 7 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_on_another_device_under_the_same_name_and_stamp_is_read_again`
  - `tests/test_library_reads_remembered.py::test_a_file_rewritten_between_two_jobs_is_read_again_and_the_second_job_matches_its_new_tags`
  - `tests/test_library_reads_remembered.py::test_a_file_swapped_in_under_the_same_name_size_and_times_is_read_again_on_its_inode`
  - `tests/test_library_reads_remembered.py::test_a_file_with_a_new_modification_time_is_read_again`
  - `tests/test_library_reads_remembered.py::test_a_file_with_a_new_size_is_read_again`
  - `tests/test_library_reads_remembered.py::test_a_read_that_is_not_whole_forgets_what_an_earlier_whole_read_left`
  - `tests/test_library_reads_remembered.py::test_a_restore_that_puts_the_old_size_and_time_back_is_read_again_on_its_change_time`

Old text:

```
            and entry.stamp == stamp

```

New text:

```
            and True

```

### `u249.M02_size_out_of_stamp`

_read_from_disk: compare the stamp without its size

- File: `src/cratekit/acquire/match.py`
- Source: `u249.json`, row `M02_size_out_of_stamp`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 817 against a baseline of 817
- Kills: 2 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_with_a_new_size_is_read_again`
  - `tests/test_library_reads_remembered.py::test_a_read_that_is_not_whole_forgets_what_an_earlier_whole_read_left`

Old text:

```
            and entry.stamp == stamp

```

New text:

```
            and entry.stamp[1:] == stamp[1:]

```

### `u249.M03_mtime_out_of_stamp`

_read_from_disk: compare the stamp without its modification time

- File: `src/cratekit/acquire/match.py`
- Source: `u249.json`, row `M03_mtime_out_of_stamp`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 817 against a baseline of 817
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_with_a_new_modification_time_is_read_again`

Old text:

```
            and entry.stamp == stamp

```

New text:

```
            and entry.stamp[:1] + entry.stamp[2:] == stamp[:1] + stamp[2:]

```

### `u249.M04_ctime_out_of_stamp`

_read_from_disk: compare the stamp without its change time, so a restore tool's old time over new bytes is answered from memory

- File: `src/cratekit/acquire/match.py`
- Source: `u249.json`, row `M04_ctime_out_of_stamp`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 817 against a baseline of 817
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_restore_that_puts_the_old_size_and_time_back_is_read_again_on_its_change_time`

Old text:

```
            and entry.stamp == stamp

```

New text:

```
            and entry.stamp[:2] + entry.stamp[3:] == stamp[:2] + stamp[3:]

```

### `u249.M05_inode_out_of_stamp`

_read_from_disk: compare the stamp without its inode

- File: `src/cratekit/acquire/match.py`
- Source: `u249.json`, row `M05_inode_out_of_stamp`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 817 against a baseline of 817
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_swapped_in_under_the_same_name_size_and_times_is_read_again_on_its_inode`

Old text:

```
            and entry.stamp == stamp

```

New text:

```
            and entry.stamp[:3] + entry.stamp[4:] == stamp[:3] + stamp[4:]

```

### `u249.M06_device_out_of_stamp`

_read_from_disk: compare the stamp without its device

- File: `src/cratekit/acquire/match.py`
- Source: `u249.json`, row `M06_device_out_of_stamp`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 817 against a baseline of 817
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_on_another_device_under_the_same_name_and_stamp_is_read_again`

Old text:

```
            and entry.stamp == stamp

```

New text:

```
            and entry.stamp[:4] == stamp[:4]

```

### `u249.M07_size_not_stat`

_stamp_of: stamp a constant in place of the file's size

- File: `src/cratekit/acquire/match.py`
- Source: `u249.json`, row `M07_size_not_stat`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 817 against a baseline of 817
- Kills: 2 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_with_a_new_size_is_read_again`
  - `tests/test_library_reads_remembered.py::test_the_stamp_is_the_files_stat_and_none_for_a_file_that_is_gone`

Old text:

```
    return (seen.st_size, seen.st_mtime_ns, seen.st_ctime_ns, seen.st_ino, seen.st_dev)
```

New text:

```
    return (0, seen.st_mtime_ns, seen.st_ctime_ns, seen.st_ino, seen.st_dev)
```

### `u249.M08_template_out_of_key`

_read_from_disk: key the memory on the path alone, so an entry parsed under one name template answers another

- File: `src/cratekit/acquire/match.py`
- Source: `u249.json`, row `M08_template_out_of_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 817 against a baseline of 817
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_the_name_template_is_part_of_the_key`

Old text:

```
    key = (path, template)
```

New text:

```
    key = (path, None)
```

### `u249.M09_no_window`

_read_from_disk: answer an equal stamp from memory however recent the file's modification time

- File: `src/cratekit/acquire/match.py`
- Source: `u249.json`, row `M09_no_window`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 817 against a baseline of 817
- Kills: 4 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_rewritten_to_the_same_size_inside_the_window_is_read_again`
  - `tests/test_library_reads_remembered.py::test_the_entrys_moment_is_taken_before_the_read`
  - `tests/test_library_reads_remembered.py::test_the_window_is_two_seconds_to_the_nanosecond[1.5s]`
  - `tests/test_library_reads_remembered.py::test_the_window_is_two_seconds_to_the_nanosecond[just-under-2s]`

Old text:

```
            and stamp[1] <= entry.made_ns - REMEMBER_WINDOW_NS

```

New text:

```
            and True

```

### `u249.M10_window_halved`

REMEMBER_WINDOW_NS: one second in place of two, under a FAT volume's step

- File: `src/cratekit/acquire/match.py`
- Source: `u249.json`, row `M10_window_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 817 against a baseline of 817
- Kills: 3 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_the_entrys_moment_is_taken_before_the_read`
  - `tests/test_library_reads_remembered.py::test_the_window_is_two_seconds_to_the_nanosecond[1.5s]`
  - `tests/test_library_reads_remembered.py::test_the_window_is_two_seconds_to_the_nanosecond[just-under-2s]`

Old text:

```
REMEMBER_WINDOW_NS = 2_000_000_000
```

New text:

```
REMEMBER_WINDOW_NS = 1_000_000_000
```

### `u249.M11_window_boundary`

_read_from_disk: a file exactly two seconds older than its entry is read again rather than answered

- File: `src/cratekit/acquire/match.py`
- Source: `u249.json`, row `M11_window_boundary`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 817 against a baseline of 817
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_the_window_is_two_seconds_to_the_nanosecond[2s]`

Old text:

```
            and stamp[1] <= entry.made_ns - REMEMBER_WINDOW_NS

```

New text:

```
            and stamp[1] < entry.made_ns - REMEMBER_WINDOW_NS

```

### `u249.M12_moment_after_read`

_read_from_disk: take the entry's moment after the read, so a write during the read can be answered from memory

- File: `src/cratekit/acquire/match.py`
- Source: `u249.json`, row `M12_moment_after_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 817 against a baseline of 817
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_the_entrys_moment_is_taken_before_the_read`

Old text:

```
    owned, whole = _read_fresh(path, template)
    if stamp is not None and whole:
```

New text:

```
    owned, whole = _read_fresh(path, template)
    made_ns = _now_ns()
    if stamp is not None and whole:
```

### `u249.M13_failed_read_remembered`

_read_from_disk: remember a read that failed, so a moment's I/O error on a USB volume answers every later job

- File: `src/cratekit/acquire/match.py`
- Source: `u249.json`, row `M13_failed_read_remembered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 817 against a baseline of 817
- Kills: 3 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_read_that_failed_is_not_remembered`
  - `tests/test_library_reads_remembered.py::test_a_read_that_is_not_whole_forgets_what_an_earlier_whole_read_left`
  - `tests/test_library_reads_remembered.py::test_a_read_that_is_not_whole_is_indexed_as_read_and_not_remembered`

Old text:

```
    if stamp is not None and whole:
```

New text:

```
    if stamp is not None:
```

### `u249.M14_unstated_remembered_never`

_stamp_of: answer None for every file, so nothing is ever remembered and every walk opens every file

- File: `src/cratekit/acquire/match.py`
- Source: `u249.json`, row `M14_unstated_remembered_never`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 817 against a baseline of 817
- Kills: 11 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_on_another_device_under_the_same_name_and_stamp_is_read_again`
  - `tests/test_library_reads_remembered.py::test_a_file_rewritten_between_two_jobs_is_read_again_and_the_second_job_matches_its_new_tags`
  - `tests/test_library_reads_remembered.py::test_a_pass_of_three_playlists_opens_each_library_file_once`
  - `tests/test_library_reads_remembered.py::test_a_read_that_is_not_whole_forgets_what_an_earlier_whole_read_left`
  - `tests/test_library_reads_remembered.py::test_a_removed_file_is_absent_a_new_one_is_read_and_a_renamed_one_is_read_under_its_name`
  - `tests/test_library_reads_remembered.py::test_a_reset_forgets_every_file[intake]`
  - `tests/test_library_reads_remembered.py::test_a_reset_forgets_every_file[match]`
  - `tests/test_library_reads_remembered.py::test_an_unchanged_old_file_is_answered_from_memory_on_the_second_index`
  - `tests/test_library_reads_remembered.py::test_the_stamp_is_the_files_stat_and_none_for_a_file_that_is_gone`
  - `tests/test_library_reads_remembered.py::test_the_window_is_two_seconds_to_the_nanosecond[2.5s]`
  - `tests/test_library_reads_remembered.py::test_the_window_is_two_seconds_to_the_nanosecond[2s]`

Old text:

```
    return (seen.st_size, seen.st_mtime_ns, seen.st_ctime_ns, seen.st_ino, seen.st_dev)
```

New text:

```
    return None
```

### `u249.M20_reset_forgets_nothing`

match.reset_cache: forget nothing

- File: `src/cratekit/acquire/match.py`
- Source: `u249.json`, row `M20_reset_forgets_nothing`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 817 against a baseline of 817
- Kills: 6 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_that_cannot_be_stated_is_read_as_before_and_never_remembered`
  - `tests/test_library_reads_remembered.py::test_a_read_that_is_not_whole_forgets_what_an_earlier_whole_read_left`
  - `tests/test_library_reads_remembered.py::test_a_read_that_is_not_whole_is_indexed_as_read_and_not_remembered`
  - `tests/test_library_reads_remembered.py::test_a_reset_forgets_every_file[intake]`
  - `tests/test_library_reads_remembered.py::test_a_reset_forgets_every_file[match]`
  - `tests/test_library_reads_remembered.py::test_a_test_starts_with_nothing_remembered`

Old text:

```
    test can clear is a memory that leaks one test's library into the next."""
    _REMEMBERED.clear()
```

New text:

```
    test can clear is a memory that leaks one test's library into the next."""
```

### `u249.M20a_failed_read_keeps_old_entry`

_read_from_disk: keep an earlier whole read's entry when a later read is not whole, so a stamp that comes back brings the old tags back

- File: `src/cratekit/acquire/match.py`
- Source: `u249.json`, row `M20a_failed_read_keeps_old_entry`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 817 against a baseline of 817
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_read_that_is_not_whole_forgets_what_an_earlier_whole_read_left`

Old text:

```
    else:
        # A read that was not whole, or a file with no stamp, forgets what an
        # earlier whole read left: the file has been seen changing, and a stamp
        # that came back later must not bring the older answer back with it.
        _REMEMBERED.pop(key, None)
    return owned
```

New text:

```
    return owned
```

### `r227.C6_composed_limit_spelled`

sync all judges against a seven spelled in the shell

- File: `src/cratekit/sync/cli.py`
- Source: `r227.json`, row `C6_composed_limit_spelled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_the_composed_gate_judges_against_the_configured_limit`

Old text:

```
    age = source.export_age(exported, limit_days=cfg.outbound.export_stale_days)
```

New text:

```
    age = source.export_age(exported, limit_days=7)
```

### `r359.M5_unwired`

The playlists planner no longer hands its note to the plan

- File: `src/cratekit/sync/cli.py`
- Source: `r359.json`, row `M5_unwired`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_recorded_playlist_says_in_the_default_output_it_was_resolved_not_acquired`

Old text:

```
    plan = _Plan(spec=spec, describe=describe, detail=describe([]), note=playlists.said)
```

New text:

```
    plan = _Plan(spec=spec, describe=describe, detail=describe([]))
```

### `r359.M6_no_append`

The check computes the note and never appends it to the detail a person reads

- File: `src/cratekit/sync/cli.py`
- Source: `r359.json`, row `M6_no_append`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_recorded_playlist_says_in_the_default_output_it_was_resolved_not_acquired`

Old text:

```
        check["detail"] += f"; {noted}"
```

New text:

```
        pass
```

### `r359.M7_note_before_describe`

The note reads an empty block instead of the source's own, so it says nothing

- File: `src/cratekit/sync/cli.py`
- Source: `r359.json`, row `M7_note_before_describe`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_recorded_playlist_says_in_the_default_output_it_was_resolved_not_acquired`

Old text:

```
    noted = plan.note(plan.detail or {}) if plan.note is not None else None
```

New text:

```
    noted = plan.note({}) if plan.note is not None else None
```

### `r504-b.B10_check_no_numbers`

The inbound check fails without naming the three numbers

- File: `src/cratekit/sync/cli.py`
- Source: `r504-b.json`, row `B10_check_no_numbers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`

Old text:

```
            f"; the listing came back short, {short.summary()}, which does not say which"
```

New text:

```
            "; the listing came back short, which does not say which"
```

### `r504-b.B7_sync_drops_short`

sync all lists the hearts and keeps no shortfall

- File: `src/cratekit/sync/cli.py`
- Source: `r504-b.json`, row `B7_sync_drops_short`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`

Old text:

```
    inbound.shortfall = short
```

New text:

```
    inbound.shortfall = None
```

### `r504-b.B8_check_passes`

A short listing leaves the inbound check at its prior status instead of failing it

- File: `src/cratekit/sync/cli.py`
- Source: `r504-b.json`, row `B8_check_passes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`

Old text:

```
        check["status"] = "fail"
        if inbound.not_queued == playlists.Excluded.EMPTY:
```

New text:

```
        if inbound.not_queued == playlists.Excluded.EMPTY:
```

### `r504-b.B9_all_withheld_says_no_hearts`

Every heart withheld still reads as an account that lists no hearts

- File: `src/cratekit/sync/cli.py`
- Source: `r504-b.json`, row `B9_all_withheld_says_no_hearts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`

Old text:

```
            check["detail"] = "not queued: the provider served none of the account's hearts"
```

New text:

```
            pass
```

### `r515-operator.S13_sweep_no_warning`

The sync all sweep says nothing of a short playlist

- File: `src/cratekit/sync/cli.py`
- Source: `r515-operator.json`, row `S13_sweep_no_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_the_sweep_summary_carries_the_shortfall_per_playlist`

Old text:

```
    if sweep.short:
```

New text:

```
    if False:
```

### `u109-a.A1_plan_guided`

Plan every enabled source again, guided ones included, so labels is planned as a source with no worker

- File: `src/cratekit/sync/cli.py`
- Source: `u109-a.json`, row `A1_plan_guided`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 9 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_full_pass_queues_each_source_under_its_own_key_with_one_run`
  - `tests/test_sync_all.py::test_a_missing_export_still_queues_the_hearts_and_the_pass_is_not_a_refusal`
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_a_source_that_refuses_does_not_stop_the_other`
  - `tests/test_sync_all.py::test_aborting_the_confirmation_queues_no_favourites_job_and_says_so`
  - `tests/test_sync_all.py::test_nothing_queued_because_every_source_refused_is_a_refusal`
  - `tests/test_sync_all.py::test_the_gate_names_the_guided_verb_and_nothing_for_labels_to_queue`
  - `tests/test_sync_all.py::test_the_human_output_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_pass_names_the_guided_verb_in_one_check_row`

Old text:

```
    plans = [_plan(spec, ctx) for spec in enabled if spec.guided_by is None]
```

New text:

```
    plans = [_plan(spec, ctx) for spec in enabled]
```

### `u109-a.A2_guided_empty`

Collect no guided source, so nothing names crate label sync anywhere

- File: `src/cratekit/sync/cli.py`
- Source: `u109-a.json`, row `A2_guided_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_nothing_queued_because_every_source_refused_is_a_refusal`
  - `tests/test_sync_all.py::test_the_gate_names_the_guided_verb_and_nothing_for_labels_to_queue`
  - `tests/test_sync_all.py::test_the_human_output_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_human_refusal_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_pass_names_the_guided_verb_in_one_check_row`

Old text:

```
    guided = tuple(spec for spec in enabled if spec.guided_by is not None)
```

New text:

```
    guided = ()
```

### `u109-a.A3_no_check_row`

Drop the guided check row, the one line the human output prints

- File: `src/cratekit/sync/cli.py`
- Source: `u109-a.json`, row `A3_no_check_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_the_human_output_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_pass_names_the_guided_verb_in_one_check_row`

Old text:

```
    checks.extend(_guided_check(spec) for spec in guided)
```

New text:

```
(empty)
```

### `u109-a.A4_summary_guided`

Drop summary.guided from the pass report

- File: `src/cratekit/sync/cli.py`
- Source: `u109-a.json`, row `A4_summary_guided`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_a_profile_without_the_labels_module_names_no_guided_verb`
  - `tests/test_sync_all.py::test_nothing_queued_because_every_source_refused_is_a_refusal`

Old text:

```
        "guided": _guided(guided),
    }
    for plan in plans:
```

New text:

```
    }
    for plan in plans:
```

### `u109-a.A5_gate_guided`

Drop the guided block from what the favourites gate shows

- File: `src/cratekit/sync/cli.py`
- Source: `u109-a.json`, row `A5_gate_guided`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_the_gate_names_the_guided_verb_and_nothing_for_labels_to_queue`

Old text:

```
            if p.inbound is not None
        },
        "guided": _guided(guided),
    }
```

New text:

```
            if p.inbound is not None
        },
    }
```

### `u109-a.A6_refusal_step_dropped`

A pass that queued nothing refuses without the step naming the guided verb

- File: `src/cratekit/sync/cli.py`
- Source: `u109-a.json`, row `A6_refusal_step_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_nothing_queued_because_every_source_refused_is_a_refusal`
  - `tests/test_sync_all.py::test_the_human_refusal_names_the_guided_verb`

Old text:

```
            steps=(*first.remediation.steps, *(_guided_step(spec) for spec in guided)),
```

New text:

```
            steps=first.remediation.steps,
```

### `u109-a.A7_refusal_step_first`

Prepend the guided step instead of appending it, so it displaces the refusing source's own first step

- File: `src/cratekit/sync/cli.py`
- Source: `u109-a.json`, row `A7_refusal_step_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_nothing_queued_because_every_source_refused_is_a_refusal`

Old text:

```
            steps=(*first.remediation.steps, *(_guided_step(spec) for spec in guided)),
```

New text:

```
            steps=(*(_guided_step(spec) for spec in guided), *first.remediation.steps),
```

### `u109-a.A8_row_reworded`

Reword the guided row so it no longer says the source is not swept here

- File: `src/cratekit/sync/cli.py`
- Source: `u109-a.json`, row `A8_row_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_the_pass_names_the_guided_verb_in_one_check_row`

Old text:

```
            f"not swept by sync all; {spec.command()} takes this source on its "
```

New text:

```
            f"left to another verb; {spec.command()} takes this source on its "
```

### `u73-c.C3_next_only_with_intake_jobs`

Name intake missing --run on every pass, including one that queued no intake job

- File: `src/cratekit/sync/cli.py`
- Source: `u73-c.json`, row `C3_next_only_with_intake_jobs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_full_pass_queues_each_source_under_its_own_key_with_one_run`
  - `tests/test_sync_all.py::test_a_pass_that_finds_only_debris_says_so_on_the_check`
  - `tests/test_sync_all.py::test_a_pass_that_queued_no_intake_job_names_no_run_verb`
  - `tests/test_sync_all.py::test_a_pass_whose_only_playlist_left_every_track_unread_says_so_on_the_check`
  - `tests/test_sync_all.py::test_a_playlist_with_no_tracks_queues_nothing_and_is_reported`

Old text:

```
    if not filed:
```

New text:

```
    if False:
```

### `u73-c.C4_next_counts_intake_jobs_only`

Count every filed job as an intake job when deciding to name the run verb

- File: `src/cratekit/sync/cli.py`
- Source: `u73-c.json`, row `C4_next_counts_intake_jobs_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_full_pass_queues_each_source_under_its_own_key_with_one_run`

Old text:

```
if job.handler_key in intake_cli.INTAKE_KEYS]
```

New text:

```
if True]
```

### `u73-c.C5_next_check_row`

Keep the command in the summary and drop the check row the human output prints

- File: `src/cratekit/sync/cli.py`
- Source: `u73-c.json`, row `C5_next_check_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_the_default_output_of_a_pass_that_queued_intake_jobs_names_the_run_verb`

Old text:

```
        checks.append(step["check"])
```

New text:

```
        pass
```

### `u74-b.B10_refused_check_status`

Report a hearts refusal as info rather than fail

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B10_refused_check_status`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_catalogue_refusal_is_the_hearts_own_and_the_others_still_run`
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`
  - `tests/test_sync_all.py::test_an_unreadable_hearts_listing_is_reported_and_the_playlists_still_queue`

Old text:

```
    elif inbound.refused is not None:
        check["status"] = "fail"
```

New text:

```
    elif inbound.refused is not None:
        check["status"] = "info"
```

### `u74-b.B11_gate_screen`

The gate screen says the hearts are queued whatever the answer when the listing refused

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B11_gate_screen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_the_gate_says_when_the_hearts_could_not_be_listed`

Old text:

```
                "queued_whatever_the_answer": p.inbound.queue is not None,
```

New text:

```
                "queued_whatever_the_answer": True,
```

### `u74-b.B12_next_step_outbound_only`

Name no intake missing --run step when only the hearts filed an intake job

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B12_next_step_outbound_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`

Old text:

```
    filed = [job for p in plans for job in _filed(p) if job.handler_key in intake_cli.INTAKE_KEYS]
```

New text:

```
    filed = [job for p in plans for job in p.filed if job.handler_key in intake_cli.INTAKE_KEYS]
```

### `u74-b.B1_source_id_dropped`

Queue the hearts job with no source_id, so the next pass cannot see it is open

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B1_source_id_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 9 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_finished_hearts_job_does_not_hold_the_next_pass`
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`
  - `tests/test_sync_all.py::test_a_missing_export_still_queues_the_hearts_and_the_pass_is_not_a_refusal`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`
  - `tests/test_sync_all.py::test_an_open_outbound_favourites_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_an_open_playlists_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_another_librarys_open_hearts_job_does_not_hold_this_one`

Old text:

```
                run_id=run_id,
                source_id=intake_cli.FAVORITES_SOURCE_ID,
            )
```

New text:

```
                run_id=run_id,
                source_id=None,
            )
```

### `u74-b.B2_compose_skips_inbound`

The composer never queues the read half

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B2_compose_skips_inbound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 16 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_complete_hearts_listing_carries_no_shortfall`
  - `tests/test_sync_all.py::test_a_confirmed_pass_queues_both_halves`
  - `tests/test_sync_all.py::test_a_declined_favourites_source_says_nothing_about_a_write_it_never_reached`
  - `tests/test_sync_all.py::test_a_finished_hearts_job_does_not_hold_the_next_pass`
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`
  - `tests/test_sync_all.py::test_a_missing_export_still_queues_the_hearts_and_the_pass_is_not_a_refusal`
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_aborting_the_confirmation_queues_no_favourites_job_and_says_so`
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`
  - `tests/test_sync_all.py::test_an_open_outbound_favourites_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_an_open_playlists_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_another_librarys_open_hearts_job_does_not_hold_this_one`
  - `tests/test_sync_all.py::test_the_human_output_names_the_guided_verb`
  - ... and 1 more, see the JSON sidecar

Old text:

```
        if p.inbound is not None and p.inbound.queue is not None:
            ready.append
```

New text:

```
        if False:
            ready.append
```

### `u74-b.B3_queue_refusal_raised`

Raise a queue time refusal instead of recording it against its half

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B3_queue_refusal_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`
  - `tests/test_sync_all.py::test_a_refusal_part_way_through_the_playlists_keeps_the_filed_ones_named`
  - `tests/test_sync_all.py::test_a_source_refused_at_queue_time_leaves_the_queued_ones_named`

Old text:

```
                    half.refused, half.not_queued = exc.cause, exc.cause.reason
```

New text:

```
                    raise
```

### `u74-b.B4_filed_outbound_only`

Count only the write half's jobs as filed, so a pass that queued only the hearts refuses or reads as a no-op

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B4_filed_outbound_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_complete_hearts_listing_carries_no_shortfall`
  - `tests/test_sync_all.py::test_a_finished_hearts_job_does_not_hold_the_next_pass`
  - `tests/test_sync_all.py::test_a_missing_export_still_queues_the_hearts_and_the_pass_is_not_a_refusal`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`
  - `tests/test_sync_all.py::test_an_open_playlists_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_another_librarys_open_hearts_job_does_not_hold_this_one`
  - `tests/test_sync_all.py::test_the_human_output_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`

Old text:

```
    return [*plan.filed, *(plan.inbound.filed if plan.inbound is not None else ())]
```

New text:

```
    return [*plan.filed]
```

### `u74-b.B5_inbound_refusal_not_counted`

Leave the hearts refusal out of the refusal list, so a declined pass it alone stopped reads as a no-op

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B5_inbound_refusal_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_declined_pass_whose_hearts_refused_is_a_refusal_not_a_no_op`

Old text:

```
        for cause in (p.refused, p.inbound.refused if p.inbound else None)
```

New text:

```
        for cause in (p.refused, None)
```

### `u74-b.B6_inbound_warning`

Emit no warning for a hearts refusal

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B6_inbound_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_catalogue_refusal_is_the_hearts_own_and_the_others_still_run`

Old text:

```
        if plan.inbound is not None and plan.inbound.refused is not None:
            warnings.append(
```

New text:

```
        if False:
            warnings.append(
```

### `u74-b.B7_block_dropped`

Leave the favourites.inbound block out of the summary

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B7_block_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 13 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_catalogue_refusal_is_the_hearts_own_and_the_others_still_run`
  - `tests/test_sync_all.py::test_a_complete_hearts_listing_carries_no_shortfall`
  - `tests/test_sync_all.py::test_a_finished_hearts_job_does_not_hold_the_next_pass`
  - `tests/test_sync_all.py::test_a_hearts_job_queued_by_hand_is_not_queued_beside`
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`
  - `tests/test_sync_all.py::test_an_account_with_no_hearts_queues_nothing_for_them`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`
  - `tests/test_sync_all.py::test_an_unreadable_hearts_listing_is_reported_and_the_playlists_still_queue`
  - `tests/test_sync_all.py::test_another_librarys_open_hearts_job_does_not_hold_this_one`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_nothing_queued_because_every_half_refused_is_still_a_refusal`

Old text:

```
            plan.detail = {**(plan.detail or {}), "inbound": plan.inbound.block()}
```

New text:

```
            pass
```

### `u74-b.B8_check_dropped`

Leave the sync.favorites.inbound check out, which is all the default output prints

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B8_check_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_catalogue_refusal_is_the_hearts_own_and_the_others_still_run`
  - `tests/test_sync_all.py::test_a_complete_hearts_listing_carries_no_shortfall`
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`
  - `tests/test_sync_all.py::test_an_account_with_no_hearts_queues_nothing_for_them`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`
  - `tests/test_sync_all.py::test_an_unreadable_hearts_listing_is_reported_and_the_playlists_still_queue`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`

Old text:

```
            checks.append(_inbound_check(plan, plan.inbound))
```

New text:

```
            pass
```

### `u74-b.B9_check_wording`

Say the hearts were not listed for a half that was listed and refused at the queue

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B9_check_wording`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`

Old text:

```
            if inbound.hearts is None
```

New text:

```
            if True
```

### `u74.A10_export_refusal_raised`

Raise the write half's export refusal to _plan again, which drops the read half with it

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A10_export_refusal_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 15 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_complete_hearts_listing_carries_no_shortfall`
  - `tests/test_sync_all.py::test_a_finished_hearts_job_does_not_hold_the_next_pass`
  - `tests/test_sync_all.py::test_a_hearts_job_queued_by_hand_is_not_queued_beside`
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`
  - `tests/test_sync_all.py::test_a_missing_export_still_queues_the_hearts_and_the_pass_is_not_a_refusal`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_an_account_with_no_hearts_queues_nothing_for_them`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`
  - `tests/test_sync_all.py::test_an_open_playlists_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_an_unreadable_hearts_listing_is_reported_and_the_playlists_still_queue`
  - `tests/test_sync_all.py::test_another_librarys_open_hearts_job_does_not_hold_this_one`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_nothing_queued_because_every_half_refused_is_still_a_refusal`
  - `tests/test_sync_all.py::test_the_human_output_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`

Old text:

```
        plan.refused, plan.not_queued = exc.cause, exc.cause.reason
        return plan
```

New text:

```
        raise
```

### `u74.A11_queue_not_bound`

Never bind the read half's queue callable, so a listed half queues nothing

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A11_queue_not_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 17 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_complete_hearts_listing_carries_no_shortfall`
  - `tests/test_sync_all.py::test_a_confirmed_pass_queues_both_halves`
  - `tests/test_sync_all.py::test_a_declined_favourites_source_says_nothing_about_a_write_it_never_reached`
  - `tests/test_sync_all.py::test_a_finished_hearts_job_does_not_hold_the_next_pass`
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`
  - `tests/test_sync_all.py::test_a_missing_export_still_queues_the_hearts_and_the_pass_is_not_a_refusal`
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_aborting_the_confirmation_queues_no_favourites_job_and_says_so`
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`
  - `tests/test_sync_all.py::test_an_open_outbound_favourites_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_an_open_playlists_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_another_librarys_open_hearts_job_does_not_hold_this_one`
  - `tests/test_sync_all.py::test_the_gate_refusal_queues_no_hearts_listing_either`
  - ... and 2 more, see the JSON sidecar

Old text:

```
    inbound.queue = queue
    return inbound
```

New text:

```
    return inbound
```

### `u74.A12_run_id_dropped`

Queue the hearts job without the shared run id, so intake missing --run cannot find it

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A12_run_id_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_confirmed_pass_queues_both_halves`
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`

Old text:

```
                tracks=tracks,
                run_id=run_id,
                source_id=intake_cli.FAVORITES_SOURCE_ID,
```

New text:

```
                tracks=tracks,
                run_id=None,
                source_id=intake_cli.FAVORITES_SOURCE_ID,
```

### `u74.A3_handler_filter`

Drop the handler key filter, so an open outbound favourites job holds the hearts listing

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A3_handler_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_an_open_outbound_favourites_job_does_not_hold_the_hearts`

Old text:

```
        if job.handler_key == handler_key
        and (job.payload or {}).get("source_id") == intake_cli.FAVORITES_SOURCE_ID
```

New text:

```
        if True
        and (job.payload or {}).get("source_id") == intake_cli.FAVORITES_SOURCE_ID
```

### `u74.A4_source_filter`

Drop the source_id filter, so an open playlists job holds the hearts listing

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A4_source_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_an_open_playlists_job_does_not_hold_the_hearts`

Old text:

```
        and (job.payload or {}).get("source_id") == intake_cli.FAVORITES_SOURCE_ID
        and job.library_id == cfg.library.volume_id
```

New text:

```
        and True
        and job.library_id == cfg.library.volume_id
```

### `u74.A5_library_filter`

Drop the library filter, so another library's open hearts job holds this one

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A5_library_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_another_librarys_open_hearts_job_does_not_hold_this_one`

Old text:

```
        and job.library_id == cfg.library.volume_id
    )
```

New text:

```
        and True
    )
```

### `u74.A6_open_filter`

Count a finished hearts job as open, so a failed job holds every later pass

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A6_open_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_finished_hearts_job_does_not_hold_the_next_pass`
  - `tests/test_sync_all.py::test_an_open_outbound_favourites_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_an_open_playlists_job_does_not_hold_the_hearts`

Old text:

```
                if job.is_open()
            )
```

New text:

```
                if True
            )
```

### `u74.A7_in_flight_guard`

Ignore an open hearts job, so every pass queues a second listing beside it

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A7_in_flight_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_hearts_job_queued_by_hand_is_not_queued_beside`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`

Old text:

```
        if in_flight:
            inbound.not_queued
```

New text:

```
        if False:
            inbound.not_queued
```

### `u74.A8_empty_guard`

Queue an empty hearts listing as a job, rather than reporting no hearts

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A8_empty_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_source_refused_at_queue_time_leaves_the_queued_ones_named`
  - `tests/test_sync_all.py::test_a_source_that_refuses_does_not_stop_the_other`
  - `tests/test_sync_all.py::test_an_account_with_no_hearts_queues_nothing_for_them`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`

Old text:

```
    if not tracks:
        inbound.not_queued = playlists.Excluded.EMPTY
```

New text:

```
    if False:
        inbound.not_queued = playlists.Excluded.EMPTY
```

### `u74.A9_listing_refusal_raised`

Raise a hearts listing refusal instead of recording it, so it ends the favourites source

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A9_listing_refusal_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 19 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_catalogue_refusal_is_the_hearts_own_and_the_others_still_run`
  - `tests/test_sync_all.py::test_a_declined_pass_whose_hearts_refused_is_a_refusal_not_a_no_op`
  - `tests/test_sync_all.py::test_a_full_pass_queues_each_source_under_its_own_key_with_one_run`
  - `tests/test_sync_all.py::test_a_pass_over_a_recent_export_carries_no_age_warning`
  - `tests/test_sync_all.py::test_a_pass_that_queued_over_an_old_export_warns_and_still_queues`
  - `tests/test_sync_all.py::test_an_unreadable_hearts_listing_is_reported_and_the_playlists_still_queue`
  - `tests/test_sync_all.py::test_nothing_queued_because_every_half_refused_is_still_a_refusal`
  - `tests/test_sync_all.py::test_nothing_queued_because_every_source_refused_is_a_refusal`
  - `tests/test_sync_all.py::test_the_composed_gate_judges_against_the_configured_limit`
  - `tests/test_sync_all.py::test_the_composed_gate_names_the_exports_date_beside_what_would_queue`
  - `tests/test_sync_all.py::test_the_composed_gate_shows_the_tracks_the_sweeps_digest_covers`
  - `tests/test_sync_all.py::test_the_composed_pass_carries_the_favourites_verb_standing_warning`
  - `tests/test_sync_all.py::test_the_favourites_job_carries_a_gate_run_its_own_verb_owns`
  - `tests/test_sync_all.py::test_the_gate_asks_over_the_digest_sync_favorites_itself_offers`
  - `tests/test_sync_all.py::test_the_gate_names_the_guided_verb_and_nothing_for_labels_to_queue`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        inbound.refused, inbound.not_queued = exc.cause, exc.cause.reason
        return inbound
```

New text:

```
        raise
```

### `r667-b.B1_same_recording_no_isrc`

_same_recording: the ISRC clause removed, r667's G11 after its direct test

- File: `src/cratekit/acquire/match.py`
- Source: `r667-b.json`, row `B1_same_recording_no_isrc`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 729 against a baseline of 729
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_isrc_hit_whose_artist_tag_credits_nobody_the_row_names_still_asks_about_the_key_alone`

Old text:

```
    return fold(wanted.artist) in held.members or _carries(held, token)
```

New text:

```
    return fold(wanted.artist) in held.members
```

### `r667-b.B2_reader_isrc_unfolded`

_read_from_disk: the ISRC tag carried verbatim, r667's G18 after its direct tests

- File: `src/cratekit/acquire/match.py`
- Source: `r667-b.json`, row `B2_reader_isrc_unfolded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 729 against a baseline of 729
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_files_isrc_tag_is_folded_before_it_is_indexed`
  - `tests/test_match_states.py::test_a_malformed_isrc_tag_is_not_an_identity`

Old text:

```
        isrc=isrc_token(read["isrc"]),
```

New text:

```
        isrc=str(read["isrc"] or ""),
```

### `r667.E1_title_head_kept`

Existing: _read_from_disk takes the title tag verbatim, the R-664 defect

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `E1_title_head_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 729 against a baseline of 729
- Kills: 33 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_track_held_under_a_headed_title_tag_is_owned_and_nothing_is_listed`
  - `tests/test_intake_missing.py::test_a_track_held_under_the_rows_isrc_is_owned_and_nothing_is_listed`
  - `tests/test_intake_missing.py::test_a_track_held_with_no_isrc_under_a_credited_list_is_owned_and_nothing_is_listed`
  - `tests/test_match_states.py::test_a_credited_hit_at_another_version_is_a_version_question_not_an_approximate_one`
  - `tests/test_match_states.py::test_a_file_held_under_the_rows_isrc_is_owned_whatever_its_artist_tag_says`
  - `tests/test_match_states.py::test_a_file_with_no_isrc_tag_is_owned_when_the_primary_artist_is_a_credited_member`
  - `tests/test_match_states.py::test_a_files_isrc_tag_is_folded_before_it_is_indexed`
  - `tests/test_match_states.py::test_a_head_found_only_in_the_tag_carries_the_key_when_the_stem_has_none`
  - `tests/test_match_states.py::test_a_head_inside_the_title_tag_is_stripped_so_a_plain_provider_row_matches`
  - `tests/test_match_states.py::test_a_head_written_as_a_suffix_inside_the_tag_comes_off_as_it_does_from_the_stem`
  - `tests/test_match_states.py::test_a_headed_tag_titled_wholly_in_brackets_matches_the_provider_row`
  - `tests/test_match_states.py::test_a_headed_tag_with_a_lossy_marker_strips_under_the_librarys_template`
  - `tests/test_match_states.py::test_a_persons_answer_is_never_overwritten_by_a_later_resolution`
  - `tests/test_match_states.py::test_a_retired_question_offered_again_is_neither_reopened_nor_duplicated`
  - `tests/test_match_states.py::test_a_retired_question_the_row_asks_again_is_reopened_not_read_as_a_rejection`
  - ... and 18 more, see the JSON sidecar

Old text:

```
    tagged_title = naming.strip_heads(spelled_tag, template=template)
```

New text:

```
    tagged_title = spelled_tag
```

### `r667.E2_first_copy_only`

Existing: resolve_one reads the key off the first held copy only

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `E2_first_copy_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 729 against a baseline of 729
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_the_key_check_reads_every_held_copy_rather_than_whichever_sorted_first[sorts-first]`
  - `tests/test_match_states.py::test_the_relative_key_wins_the_reporting_when_both_disagreements_are_present`

Old text:

```
        disagreements = {key_disagreement(wanted.key, held.key) for held in exact}
```

New text:

```
        disagreements = {key_disagreement(wanted.key, exact[0].key)}
```

### `r667.F1_credited_reason_is_exact`

resolve_one: a credited list hit reports exact, so the report claims a token agreement that did not happen

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `F1_credited_reason_is_exact`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 729 against a baseline of 729
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_file_with_no_isrc_tag_is_owned_when_the_primary_artist_is_a_credited_member`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[credited-exact]`
  - `tests/test_match_states.py::test_the_credited_list_rule_tells_two_emoji_titles_apart`

Old text:

```
            else Why.CREDITED_EXACT
```

New text:

```
            else Why.EXACT
```

### `r667.F2_isrc_version_not_settled`

_candidates_for: an ISRC hit at another version spelling is a version question on the candidate beside a key question on the match

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `F2_isrc_version_not_settled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 729 against a baseline of 729
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_isrc_hit_at_another_version_spelling_asks_about_the_key_alone`

Old text:

```
        elif version_key != wanted.version_key and not _carries(first, token):
```

New text:

```
        elif version_key != wanted.version_key:
```

### `r667.F3_doubtful_not_offered`

resolve_one: an ISRC hit whose title disagrees is not offered, so it falls through to missing or a scored hit

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `F3_doubtful_not_offered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 729 against a baseline of 729
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_isrc_hit_on_an_abbreviated_title_is_still_asked_about`
  - `tests/test_match_states.py::test_an_isrc_hit_whose_title_disagrees_is_a_question_not_a_match`
  - `tests/test_match_states.py::test_an_isrc_under_another_artist_and_another_emoji_title_is_asked`

Old text:

```
    if doubtful:
        # The ISRC agrees and the title does not, see above. Asked, not assumed.
```

New text:

```
    if False:
        # The ISRC agrees and the title does not, see above. Asked, not assumed.
```

### `r667.F4_text_copy_joins_isrc_paths`

resolve_one: a text matched copy at the wanted version joins an ISRC settled row's paths and key check

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `F4_text_copy_joins_isrc_paths`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 729 against a baseline of 729
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_isrc_settled_row_lists_the_files_carrying_the_isrc_and_no_other`

Old text:

```
    if settled:
        exact, agreed = settled, Why.ISRC_EXACT
```

New text:

```
    if settled:
        exact = settled + [held for held in owned if held.version_key == wanted.version_key and held.path not in {one.path for one in settled}]
        agreed = Why.ISRC_EXACT
```

