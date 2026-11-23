# Mutation table: u311-replay-after-d2

Measured by `scripts/mutate.py` on 2026-11-23 06:13 UTC, branch `cloud/868-tools-backup-refactor` at `f95ae3da`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22416 collected. pytest invocations for this batch: 21.

Full baseline: measured by this driver (the battery's verdict was not read: it is for commit `5224c6668bba`, and this tree is at `f95ae3dae63f`).

Subset baselines: 3, each measured by this driver.

Known failures: 149 node ids whose failure is this machine's and not the tree's, read from a scratch file measured by `cloud_battery.py baseline` on the base with a stand in `rclone` on the path and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22416 against 22416. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r1761.P19_census_not_written` | `src/cratekit/modules/tools/backup.py` | user | 5 file(s) | 406 | 2 | killed |
| `r1761.P1_identity_not_asked` | `src/cratekit/modules/tools/backup.py` | user | 5 file(s) | 406 | 2 | killed |
| `r1761.P25_max_delete_sentence_on_any_failure` | `src/cratekit/modules/tools/backup.py` | user | 5 file(s) | 406 | 1 | killed |
| `r1761.P2_identity_at_read_strength_tolerates_mismatch` | `src/cratekit/modules/tools/backup.py` | user | 5 file(s) | 406 | 2 | killed |
| `r1761.P4_content_proof_skipped` | `src/cratekit/modules/tools/backup.py` | user | 5 file(s) | 406 | 3 | killed |
| `r1761.P5_empty_root_passes` | `src/cratekit/modules/tools/backup_proof.py` | user | 5 file(s) | 406 | 1 | killed |
| `r1761.P8_floor_comparison_inclusive` | `src/cratekit/modules/tools/backup_proof.py` | user | 5 file(s) | 406 | 1 | killed |
| `r1761.P9_emptied_passes_on_the_fact_file` | `src/cratekit/modules/tools/backup_proof.py` | user | 2 file(s) | 233 | 1 | killed |
| `r1761.P23_probe_counts_state` | `src/cratekit/modules/tools/backup_record.py` | user | 5 file(s) | 406 | 1 | killed |
| `r1761.P7_floor_coefficient_halved` | `src/cratekit/modules/tools/backup_record.py` | user | 5 file(s) | 406 | 2 | killed |
| `r757-c1.S1_resume_drops_the_full_flag` | `src/cratekit/backup/cli.py` | user | 4 file(s) | 727 | 1 | killed |
| `r757-c1.S3_work_body_plans_fast` | `src/cratekit/backup/cli.py` | user | 4 file(s) | 727 | 1 | killed |
| `r757-c2.S5_unread_number_printed_as_zero` | `src/cratekit/backup/cli.py` | user | 4 file(s) | 727 | 1 | killed |
| `r757-c2.S6_twin_in_the_other_mode_says_nothing` | `src/cratekit/backup/cli.py` | user | 4 file(s) | 727 | 1 | killed |
| `r757-a.E1_full_mode_still_lists_recursively` | `src/cratekit/modules/tools/backup.py` | user | 4 file(s) | 727 | 3 | killed |
| `r757-a.E2_fast_mode_lists_folder_by_folder` | `src/cratekit/modules/tools/backup.py` | user | 4 file(s) | 727 | 4 | killed |

## Row definitions

### `r1761.P19_census_not_written`

run_backup: no census is kept after a completed files portion

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r1761.json`, row `P19_census_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_unproven_root.py`, `tests/test_backup_quick.py`, `tests/test_backup_cli.py`, `tests/test_backup_comparison.py`, `tests/modules/test_tools.py`
- Collected: 406 against a baseline of 406
- Kills: 2 (killed)
- Killed:
  - `tests/test_backup_unproven_root.py::test_a_walk_that_refused_is_counted_so_the_floor_still_holds`
  - `tests/test_backup_unproven_root.py::test_the_first_backup_of_a_new_empty_library_runs`

Old text:

```
                backup_record.write_census(cfg, entry.held, at=moment)
```

New text:

```
                pass
```

### `r1761.P1_identity_not_asked`

_plan_files: skip the identity proof, so a root on another volume is walked and mirrored

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r1761.json`, row `P1_identity_not_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_unproven_root.py`, `tests/test_backup_quick.py`, `tests/test_backup_cli.py`, `tests/test_backup_comparison.py`, `tests/modules/test_tools.py`
- Collected: 406 against a baseline of 406
- Kills: 2 (killed)
- Killed:
  - `tests/test_backup_unproven_root.py::test_a_root_on_another_volume_refuses_before_the_walk`
  - `tests/test_backup_unproven_root.py::test_the_identity_holds_whatever_the_flag_says`

Old text:

```
    if foreign:
        return PortionPlan(
            portion=backup_facts.Portion.FILES,
            refusal=Refusal.LIBRARY_ROOT_FOREIGN,
```

New text:

```
    if False:
        return PortionPlan(
            portion=backup_facts.Portion.FILES,
            refusal=Refusal.LIBRARY_ROOT_FOREIGN,
```

### `r1761.P25_max_delete_sentence_on_any_failure`

run_backup: the remote holds files sentence is said for any failure of a move nothing mirror, round one's B2

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r1761.json`, row `P25_max_delete_sentence_on_any_failure`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_unproven_root.py`, `tests/test_backup_quick.py`, `tests/test_backup_cli.py`, `tests/test_backup_comparison.py`, `tests/modules/test_tools.py`
- Collected: 406 against a baseline of 406
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_unproven_root.py::test_a_move_nothing_mirror_failing_for_another_reason_says_only_that`

Old text:

```
                and MOVE_NOTHING[0].lstrip("-") in failed.stderr
```

New text:

```
                and True
```

### `r1761.P2_identity_at_read_strength_tolerates_mismatch`

_not_the_recorded_volume: read every refusal of the gate as an unread identity, so a foreign volume is left to the census

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r1761.json`, row `P2_identity_at_read_strength_tolerates_mismatch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_unproven_root.py`, `tests/test_backup_quick.py`, `tests/test_backup_cli.py`, `tests/test_backup_comparison.py`, `tests/modules/test_tools.py`
- Collected: 406 against a baseline of 406
- Kills: 2 (killed)
- Killed:
  - `tests/test_backup_unproven_root.py::test_a_root_on_another_volume_refuses_before_the_walk`
  - `tests/test_backup_unproven_root.py::test_the_identity_holds_whatever_the_flag_says`

Old text:

```
        if recorded is None or observed is None:
            return ""
```

New text:

```
        if True:
            return ""
```

### `r1761.P4_content_proof_skipped`

_plan_files: ignore the content proof's refusal, so an empty root is mirrored (the defect)

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r1761.json`, row `P4_content_proof_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_unproven_root.py`, `tests/test_backup_quick.py`, `tests/test_backup_cli.py`, `tests/test_backup_comparison.py`, `tests/modules/test_tools.py`
- Collected: 406 against a baseline of 406
- Kills: 3 (killed)
- Killed:
  - `tests/test_backup_unproven_root.py::test_a_root_holding_nothing_at_all_refuses_with_no_history_anywhere`
  - `tests/test_backup_unproven_root.py::test_a_walk_that_refused_is_counted_so_the_floor_still_holds`
  - `tests/test_backup_unproven_root.py::test_one_file_under_the_floor_refuses_and_one_at_it_runs`

Old text:

```
    if unproven:
        return PortionPlan(
            portion=backup_facts.Portion.FILES,
            refusal=Refusal.LIBRARY_ROOT_UNPROVEN,
```

New text:

```
    if False:
        return PortionPlan(
            portion=backup_facts.Portion.FILES,
            refusal=Refusal.LIBRARY_ROOT_UNPROVEN,
```

### `r1761.P5_empty_root_passes`

_unproven: a root holding nothing at all is not refused, so with no history it runs as a new library

- File: `src/cratekit/modules/tools/backup_proof.py`
- Source: `r1761.json`, row `P5_empty_root_passes`
- Moved: the same text, now in src/cratekit/modules/tools/backup_proof.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_unproven_root.py`, `tests/test_backup_quick.py`, `tests/test_backup_cli.py`, `tests/test_backup_comparison.py`, `tests/modules/test_tools.py`
- Collected: 406 against a baseline of 406
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_unproven_root.py::test_a_root_holding_nothing_at_all_refuses_with_no_history_anywhere`

Old text:

```
    if not anything:
        held_before = ""
```

New text:

```
    if False:
        held_before = ""
```

### `r1761.P8_floor_comparison_inclusive`

_unproven: the floor refuses at a tenth as well as under it, so two of twenty refuses

- File: `src/cratekit/modules/tools/backup_proof.py`
- Source: `r1761.json`, row `P8_floor_comparison_inclusive`
- Moved: the same text, now in src/cratekit/modules/tools/backup_proof.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_unproven_root.py`, `tests/test_backup_quick.py`, `tests/test_backup_cli.py`, `tests/test_backup_comparison.py`, `tests/modules/test_tools.py`
- Collected: 406 against a baseline of 406
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_unproven_root.py::test_one_file_under_the_floor_refuses_and_one_at_it_runs`

Old text:

```
    if had and held * backup_record.LIBRARY_FLOOR < had:
```

New text:

```
    if had and held * backup_record.LIBRARY_FLOOR <= had:
```

### `r1761.P9_emptied_passes_on_the_fact_file`

_unproven: the emptied flag passes on the fact file alone, which a database item writes at a mount point (round two's N2)

- File: `src/cratekit/modules/tools/backup_proof.py`
- Source: `r1761.json`, row `P9_emptied_passes_on_the_fact_file`
- Moved: U311 moved the census proof out of backup.py into backup_proof.py with this line unchanged. On the base the row was killed only by the seam allowance test, which the mutant tripped by an incidental reach into the facts module from backup.py, and the guard's own tests need rclone and are this container's failures; from backup_proof.py the same reach crosses no seam, so U311 added test_the_emptied_flag_passes_on_the_files_record_and_not_on_the_fact_file_alone in tests/modules/test_tools.py, which writes a database record alone and asserts the emptied flag is still refused, the guard round two's N2 named
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_import_rules.py`
- Collected: 233 against a baseline of 233
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_emptied_flag_passes_on_the_files_record_and_not_on_the_fact_file_alone`

Old text:

```
        if carried is not None:
            return "", False
```

New text:

```
        if backup_facts.path_for(cfg).is_file():
            return "", False
```

### `r1761.P23_probe_counts_state`

probe: a file in the state folder is counted as the library's, so a stray state folder proves the root

- File: `src/cratekit/modules/tools/backup_record.py`
- Source: `r1761.json`, row `P23_probe_counts_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_unproven_root.py`, `tests/test_backup_quick.py`, `tests/test_backup_cli.py`, `tests/test_backup_comparison.py`, `tests/modules/test_tools.py`
- Collected: 406 against a baseline of 406
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_unproven_root.py::test_the_probe_reads_past_an_exclude_the_walk_cannot_translate`

Old text:

```
            anything = True
            if held(rel, state_dirname):
```

New text:

```
            anything = True
            if True:
```

### `r1761.P7_floor_coefficient_halved`

LIBRARY_FLOOR: a twentieth rather than a tenth, so one file where twelve were passes

- File: `src/cratekit/modules/tools/backup_record.py`
- Source: `r1761.json`, row `P7_floor_coefficient_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_unproven_root.py`, `tests/test_backup_quick.py`, `tests/test_backup_cli.py`, `tests/test_backup_comparison.py`, `tests/modules/test_tools.py`
- Collected: 406 against a baseline of 406
- Kills: 2 (killed)
- Killed:
  - `tests/test_backup_unproven_root.py::test_a_walk_that_refused_is_counted_so_the_floor_still_holds`
  - `tests/test_backup_unproven_root.py::test_one_file_under_the_floor_refuses_and_one_at_it_runs`

Old text:

```
LIBRARY_FLOOR = 10
```

New text:

```
LIBRARY_FLOOR = 20
```

### `r757-c1.S1_resume_drops_the_full_flag`

backup_argv: never emit --full, so a resumed full job's command line is a fast one

- File: `src/cratekit/backup/cli.py`
- Source: `r757-c1.json`, row `S1_resume_drops_the_full_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 727 against a baseline of 727
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_comparison.py::test_the_full_flag_is_frozen_by_the_parser_and_rebuilt_by_the_resume`

Old text:

```
    if payload.get(FULL):
        argv.append("--full")
```

New text:

```
    if False:
        argv.append("--full")
```

### `r757-c1.S3_work_body_plans_fast`

perform_backup: plan in the fast mode whatever the payload froze

- File: `src/cratekit/backup/cli.py`
- Source: `r757-c1.json`, row `S3_work_body_plans_fast`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 727 against a baseline of 727
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_comparison.py::test_the_frozen_mode_is_the_one_the_plan_is_built_in`

Old text:

```
            full=bool(payload.get(FULL)),
```

New text:

```
            full=False,
```

### `r757-c2.S5_unread_number_printed_as_zero`

comparison_warning: print a total that was not read as 0

- File: `src/cratekit/backup/cli.py`
- Source: `r757-c2.json`, row `S5_unread_number_printed_as_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 727 against a baseline of 727
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_comparison.py::test_the_sentence_never_prints_an_unread_number_as_zero`

Old text:

```
            return f"an unread number of {unit}"
```

New text:

```
            return f"0 {unit}"
```

### `r757-c2.S6_twin_in_the_other_mode_says_nothing`

_already_queued: drop the sentence saying the open job runs the other comparison, the review's fix

- File: `src/cratekit/backup/cli.py`
- Source: `r757-c2.json`, row `S6_twin_in_the_other_mode_says_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 727 against a baseline of 727
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_comparison.py::test_a_second_ask_in_the_other_mode_is_told_the_open_job_differs`

Old text:

```
    if asked_full is not None and asked_full != _is_full(job):
```

New text:

```
    if False:
```

### `r757-a.E1_full_mode_still_lists_recursively`

_plan_files: the full mode carries the recursive listing option too, so --full is the fast run under another name

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r757-a.json`, row `E1_full_mode_still_lists_recursively`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 727 against a baseline of 727
- Kills: 3 (killed)
- Killed:
  - `tests/test_backup_comparison.py::test_only_a_full_mirror_moves_the_date_of_the_last_full_comparison`
  - `tests/test_backup_comparison.py::test_the_frozen_mode_is_the_one_the_plan_is_built_in`
  - `tests/test_backup_comparison.py::test_the_two_modes_differ_by_the_listing_option_and_by_nothing_else`

Old text:

```
                *(() if full else (FAST_LIST,)),
```

New text:

```
                *((FAST_LIST,)),
```

### `r757-a.E2_fast_mode_lists_folder_by_folder`

_plan_files: the ordinary run drops the recursive listing option, which is the whole of the speed fix

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r757-a.json`, row `E2_fast_mode_lists_folder_by_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 727 against a baseline of 727
- Kills: 4 (killed)
- Killed:
  - `tests/test_backup_comparison.py::test_only_a_full_mirror_moves_the_date_of_the_last_full_comparison`
  - `tests/test_backup_comparison.py::test_the_frozen_mode_is_the_one_the_plan_is_built_in`
  - `tests/test_backup_comparison.py::test_the_two_modes_differ_by_the_listing_option_and_by_nothing_else`
  - `tests/test_backup_comparison.py::test_totals_that_could_not_be_read_are_none_and_never_zero`

Old text:

```
                *(() if full else (FAST_LIST,)),
```

New text:

```
                *(() if True else (FAST_LIST,)),
```

