# Mutation table: u311-replay-before-d4

Measured by `scripts/mutate.py` on 2026-11-23 03:56 UTC, branch `HEAD` at `d8135e39`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 36.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py baseline` at 2026-11-23 03:56 UTC for commit `d8135e39d6eb`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 8, each measured by this driver.

Known failures: 150 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r222-a.A3_no_floor_holds_nothing` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 308 | 2 | killed |
| `r222-a.A4_keep_zero_holds` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 308 | 1 | killed |
| `r222-a.A5_held_run_takes_no_slot` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 308 | 5 | killed |
| `r222-a.A6_any_destination_is_a_floor` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 308 | 1 | killed |
| `r222-a.A7_no_record_is_a_late_floor` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 308 | 2 | killed |
| `r222-a.A8_floor_read_by_a_rehearsal` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 308 | 3 | killed |
| `r222-a.A9_rehearsal_purges` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 308 | 5 | killed |
| `r395.M1_no_pipx_detection` | `src/cratekit/modules/extras.py` | user | 5 file(s) | 1233 | 12 | killed |
| `r395.M2_bare_pip` | `src/cratekit/modules/extras.py` | user | 5 file(s) | 1233 | 1 | killed |
| `r395.M4_no_force` | `src/cratekit/modules/extras.py` | user | 5 file(s) | 1233 | 8 | killed |
| `r395.M5_trust_missing_source` | `src/cratekit/modules/extras.py` | user | 5 file(s) | 1233 | 3 | killed |
| `r395.M6_always_dot` | `src/cratekit/modules/extras.py` | user | 5 file(s) | 1233 | 2 | killed |
| `r395.M7_fallback_drops_extras` | `src/cratekit/modules/extras.py` | user | 5 file(s) | 1233 | 1 | killed |
| `u192.F1_no_rearm_catch` | `src/cratekit/modules/foreground.py` | user | 2 file(s) | 274 | 5 | killed |
| `u192.F2_no_retry` | `src/cratekit/modules/foreground.py` | user | 2 file(s) | 274 | 5 | killed |
| `u192.F3_keep_remedy_token` | `src/cratekit/modules/foreground.py` | user | 2 file(s) | 274 | 1 | killed |
| `u192.F4_command_dropped` | `src/cratekit/modules/foreground.py` | user | 2 file(s) | 274 | 5 | killed |
| `u192.F5_settled_count` | `src/cratekit/modules/foreground.py` | user | 2 file(s) | 274 | 1 | killed |
| `u192.F8_not_exclusive` | `src/cratekit/modules/foreground.py` | user | 2 file(s) | 274 | 3 | killed |
| `u46-author.M1_no_items_enqueued` | `src/cratekit/master/cli.py` | user | 2 file(s) | 75 | 17 | killed |
| `u46-round-2.M6_staging_not_cleared` | `src/cratekit/master/cli.py` | user | 2 file(s) | 75 | 2 | killed |
| `u46-round-2.M7B_engine_refusal_swallowed` | `src/cratekit/master/cli.py` | user | 2 file(s) | 75 | 23 | killed |
| `u184.A1_flag_ignored` | `src/cratekit/session/cli.py` | user | 3 file(s) | 81 | 10 | killed |
| `u184.A2_any_actor_accepted` | `src/cratekit/session/cli.py` | user | 3 file(s) | 81 | 3 | killed |
| `u192.F7_queue_only_always` | `src/cratekit/modules/foreground.py` | user | 3 file(s) | 338 | 10 | killed |
| `u27-restore-cli-independent.X1_the_off_machine_engine_stops_refusing_an_unconfirmed_restore` | `src/cratekit/modules/tools/backup.py` | user | 3 file(s) | 455 | 3 | killed |
| `u27-restore-cli-round-2.S3_analysis_watch_watches_nothing` | `src/cratekit/session/restore_cli.py` | user | 2 file(s) | 246 | 1 | killed |

## Row definitions

### `r222-a.A3_no_floor_holds_nothing`

Read no floor as nothing to hold, so a remote with no completed mirror on record is rotated as though every folder were settled

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r222-a.json`, row `A3_no_floor_holds_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 308 against a baseline of 308
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_completed_mirror_to_another_destination_settles_nothing_here`
  - `tests/modules/test_tools.py::test_a_remote_with_no_completed_mirror_on_record_is_never_purged`

Old text:

```
(floor is None or name > floor)]
```

New text:

```
(floor is not None and name > floor)]
```

### `r222-a.A4_keep_zero_holds`

Hold the run's folders at a keep of zero, overruling a request to keep no archive

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r222-a.json`, row `A4_keep_zero_holds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 308 against a baseline of 308
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_keep_of_zero_is_still_a_keep_of_zero`

Old text:

```
    held = [name for name in names if keep > 0 and (floor is None or name > floor)]
```

New text:

```
    held = [name for name in names if (floor is None or name > floor)]
```

### `r222-a.A5_held_run_takes_no_slot`

Spend the whole keep on settled folders, so the held run is kept on top of the keep rather than as one slot of it

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r222-a.json`, row `A5_held_run_takes_no_slot`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 308 against a baseline of 308
- Kills: 5 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_remote_with_no_completed_mirror_on_record_is_never_purged`
  - `tests/modules/test_tools.py::test_a_retried_mirror_does_not_purge_the_archive_its_failed_attempt_wrote`
  - `tests/modules/test_tools.py::test_a_wider_keep_counts_the_held_run_as_one_of_its_slots`
  - `tests/modules/test_tools.py::test_the_run_after_a_retried_one_rotates_every_attempt_out_together`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`

Old text:

```
    slots = keep - 1 if held else keep
```

New text:

```
    slots = keep
```

### `r222-a.A6_any_destination_is_a_floor`

Take the floor from a completed mirror to ANOTHER destination, which says nothing about which folders here are finished

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r222-a.json`, row `A6_any_destination_is_a_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 308 against a baseline of 308
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_completed_mirror_to_another_destination_settles_nothing_here`

Old text:

```
    if fact is None or fact.destination != _destination_for(cfg, backup_facts.Portion.FILES):
        return None
```

New text:

```
    if fact is None:
        return None
```

### `r222-a.A7_no_record_is_a_late_floor`

Answer a missing record with a floor after every date, so nothing is held and the old rotation runs on a remote with no completed mirror

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r222-a.json`, row `A7_no_record_is_a_late_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 308 against a baseline of 308
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_completed_mirror_to_another_destination_settles_nothing_here`
  - `tests/modules/test_tools.py::test_a_remote_with_no_completed_mirror_on_record_is_never_purged`

Old text:

```
    if fact is None or fact.destination != _destination_for(cfg, backup_facts.Portion.FILES):
        return None
```

New text:

```
    if fact is None or fact.destination != _destination_for(cfg, backup_facts.Portion.FILES):
        return "9999"
```

### `r222-a.A8_floor_read_by_a_rehearsal`

Read the record above the rehearsal's return, so a preview fails over a file it never touches

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r222-a.json`, row `A8_floor_read_by_a_rehearsal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 308 against a baseline of 308
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_rehearsal_does_not_read_the_record_to_list_a_rotation`
  - `tests/test_backup_cli.py::test_the_handler_does_not_fail_an_item_over_the_age_read_back`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`

Old text:

```
    if keep < 0 or not purge:
        return out, None
    floor = _rotation_floor(cfg)
```

New text:

```
    floor = _rotation_floor(cfg)
    if keep < 0 or not purge:
        return out, None
```

### `r222-a.A9_rehearsal_purges`

EXISTING GUARD, sampled because this round re-armed its tests: a rehearsal runs the real purge

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r222-a.json`, row `A9_rehearsal_purges`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 308 against a baseline of 308
- Kills: 5 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_dry_run_never_purges`
  - `tests/modules/test_tools.py::test_a_rehearsal_does_not_read_the_record_to_list_a_rotation`
  - `tests/modules/test_tools.py::test_a_rehearsal_whose_listing_succeeded_warns_about_nothing_and_purges_nothing`
  - `tests/test_backup_cli.py::test_the_handler_does_not_fail_an_item_over_the_age_read_back`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`

Old text:

```
                    purge=not dry_run,
```

New text:

```
                    purge=True,
```

### `r395.M1_no_pipx_detection`

Drop the pipx branch, every environment gets the pip form

- File: `src/cratekit/modules/extras.py`
- Source: `r395.json`, row `M1_no_pipx_detection`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_cli_contract.py`, `tests/test_install_command.py`, `tests/test_vocals_cli.py`
- Collected: 1233 against a baseline of 1233
- Kills: 12 (killed)
- Killed:
  - `tests/test_install_command.py::test_a_direct_reference_to_another_package_is_not_read_as_this_install`
  - `tests/test_install_command.py::test_a_direct_reference_with_no_extras_gains_the_one_asked_for[cratekit @ git+https://github.com/philgutowski/cratekit@v0.3.0]`
  - `tests/test_install_command.py::test_a_direct_reference_with_no_extras_gains_the_one_asked_for[cratekit[]@ git+https://github.com/philgutowski/cratekit@v0.3.0]`
  - `tests/test_install_command.py::test_a_moved_clone_still_keeps_the_extras_pipx_recorded`
  - `tests/test_install_command.py::test_a_pipx_environment_gets_pipx_against_the_recorded_clone`
  - `tests/test_install_command.py::test_a_pipx_environment_whose_source_cannot_be_read_gets_the_readme_form[{"main_package": {"package_or_url": "/no/such/clone[vocals]"}}]`
  - `tests/test_install_command.py::test_a_pipx_environment_whose_source_cannot_be_read_gets_the_readme_form[{"main_package": {"package_or_url": "git+https://example.invalid/c.git"}}]`
  - `tests/test_install_command.py::test_a_pipx_environment_whose_source_cannot_be_read_gets_the_readme_form[{"main_package": {}}]`
  - `tests/test_install_command.py::test_a_pipx_environment_whose_source_cannot_be_read_gets_the_readme_form[{not json]`
  - `tests/test_install_command.py::test_a_pipx_force_install_keeps_the_extras_already_chosen`
  - `tests/test_install_command.py::test_a_release_install_pipx_recorded_as_a_direct_reference_keeps_it_and_its_extras`
  - `tests/test_install_command.py::test_the_parser_stub_and_the_workers_read_one_source`

Old text:

```
    if (prefix / PIPX_METADATA).is_file():
```

New text:

```
    if False:
```

### `r395.M2_bare_pip`

Print a bare pip instead of the running interpreter's pip

- File: `src/cratekit/modules/extras.py`
- Source: `r395.json`, row `M2_bare_pip`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_cli_contract.py`, `tests/test_install_command.py`, `tests/test_vocals_cli.py`
- Collected: 1233 against a baseline of 1233
- Kills: 1 (killed)
- Killed:
  - `tests/test_install_command.py::test_a_plain_virtual_environment_gets_pip_run_by_its_own_interpreter`

Old text:

```
[sys.executable, "-m", "pip", "install", f"{DISTRIBUTION}[{extras}]"]
```

New text:

```
["pip", "install", f"{DISTRIBUTION}[{extras}]"]
```

### `r395.M4_no_force`

Drop --force from the pipx form

- File: `src/cratekit/modules/extras.py`
- Source: `r395.json`, row `M4_no_force`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_cli_contract.py`, `tests/test_install_command.py`, `tests/test_vocals_cli.py`
- Collected: 1233 against a baseline of 1233
- Kills: 8 (killed)
- Killed:
  - `tests/test_install_command.py::test_a_direct_reference_to_another_package_is_not_read_as_this_install`
  - `tests/test_install_command.py::test_a_moved_clone_still_keeps_the_extras_pipx_recorded`
  - `tests/test_install_command.py::test_a_pipx_environment_gets_pipx_against_the_recorded_clone`
  - `tests/test_install_command.py::test_a_pipx_environment_whose_source_cannot_be_read_gets_the_readme_form[{"main_package": {"package_or_url": "/no/such/clone[vocals]"}}]`
  - `tests/test_install_command.py::test_a_pipx_environment_whose_source_cannot_be_read_gets_the_readme_form[{"main_package": {"package_or_url": "git+https://example.invalid/c.git"}}]`
  - `tests/test_install_command.py::test_a_pipx_environment_whose_source_cannot_be_read_gets_the_readme_form[{"main_package": {}}]`
  - `tests/test_install_command.py::test_a_pipx_environment_whose_source_cannot_be_read_gets_the_readme_form[{not json]`
  - `tests/test_install_command.py::test_a_pipx_force_install_keeps_the_extras_already_chosen`

Old text:

```
["pipx", "install", "--force", f"{source}[{wanted}]"]
```

New text:

```
["pipx", "install", f"{source}[{wanted}]"]
```

### `r395.M5_trust_missing_source`

Use the recorded source even when the directory is gone

- File: `src/cratekit/modules/extras.py`
- Source: `r395.json`, row `M5_trust_missing_source`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_cli_contract.py`, `tests/test_install_command.py`, `tests/test_vocals_cli.py`
- Collected: 1233 against a baseline of 1233
- Kills: 3 (killed)
- Killed:
  - `tests/test_install_command.py::test_a_moved_clone_still_keeps_the_extras_pipx_recorded`
  - `tests/test_install_command.py::test_a_pipx_environment_whose_source_cannot_be_read_gets_the_readme_form[{"main_package": {"package_or_url": "/no/such/clone[vocals]"}}]`
  - `tests/test_install_command.py::test_a_pipx_environment_whose_source_cannot_be_read_gets_the_readme_form[{"main_package": {"package_or_url": "git+https://example.invalid/c.git"}}]`

Old text:

```
    source = match["source"] if Path(match["source"]).is_dir() else "."
```

New text:

```
    source = match["source"]
```

### `r395.M6_always_dot`

Always print the '.' form, ignoring the recorded clone

- File: `src/cratekit/modules/extras.py`
- Source: `r395.json`, row `M6_always_dot`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_cli_contract.py`, `tests/test_install_command.py`, `tests/test_vocals_cli.py`
- Collected: 1233 against a baseline of 1233
- Kills: 2 (killed)
- Killed:
  - `tests/test_install_command.py::test_a_pipx_environment_gets_pipx_against_the_recorded_clone`
  - `tests/test_install_command.py::test_a_pipx_force_install_keeps_the_extras_already_chosen`

Old text:

```
    source = match["source"] if Path(match["source"]).is_dir() else "."
```

New text:

```
    source = "."
```

### `r395.M7_fallback_drops_extras`

The review's defect: an unusable source drops the recorded extras

- File: `src/cratekit/modules/extras.py`
- Source: `r395.json`, row `M7_fallback_drops_extras`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_cli_contract.py`, `tests/test_install_command.py`, `tests/test_vocals_cli.py`
- Collected: 1233 against a baseline of 1233
- Kills: 1 (killed)
- Killed:
  - `tests/test_install_command.py::test_a_moved_clone_still_keeps_the_extras_pipx_recorded`

Old text:

```
    source = match["source"] if Path(match["source"]).is_dir() else "."
    return source, chosen
```

New text:

```
    if not Path(match["source"]).is_dir():
        return ".", ()
    return match["source"], chosen
```

### `u192.F1_no_rearm_catch`

settle: let the cancelled refusal through untouched, so an interrupted drive leaves the job closed and names job resume

- File: `src/cratekit/modules/foreground.py`
- Source: `u192.json`, row `F1_no_rearm_catch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_analysis_workers.py`
- Collected: 274 against a baseline of 274
- Kills: 5 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_job_the_shipped_code_left_with_no_intent_resumes_from_its_staged_report`
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - `tests/test_analysis_workers.py::test_an_interrupt_after_a_renamed_items_report_is_staged_resumes_by_the_printed_command`
  - `tests/test_analysis_workers.py::test_an_interrupted_restamp_names_its_job_command_and_that_command_finishes_it`
  - `tests/test_tag_workers.py::test_an_interrupted_sweep_names_its_job_command_and_that_command_finishes_it`

Old text:

```
    except JobCancelled as exc:
        raise _resumable(exc, job_id, argv, origin) from exc
```

New text:

```
    except ZeroDivisionError as exc:
        raise _resumable(exc, job_id, argv, origin) from exc
```

### `u192.F2_no_retry`

_resumable: read the job instead of re-arming it, so the named --job command meets a closed job

- File: `src/cratekit/modules/foreground.py`
- Source: `u192.json`, row `F2_no_retry`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_analysis_workers.py`
- Collected: 274 against a baseline of 274
- Kills: 5 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_job_the_shipped_code_left_with_no_intent_resumes_from_its_staged_report`
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - `tests/test_analysis_workers.py::test_an_interrupt_after_a_renamed_items_report_is_staged_resumes_by_the_printed_command`
  - `tests/test_analysis_workers.py::test_an_interrupted_restamp_names_its_job_command_and_that_command_finishes_it`
  - `tests/test_tag_workers.py::test_an_interrupted_sweep_names_its_job_command_and_that_command_finishes_it`

Old text:

```
        job = jobs.retry(store, job_id)
```

New text:

```
        job = jobs.get(store, job_id)
```

### `u192.F3_keep_remedy_token`

_resumable: keep the job resume token, so the fix line names the detached worker ahead of the --job command

- File: `src/cratekit/modules/foreground.py`
- Source: `u192.json`, row `F3_keep_remedy_token`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_analysis_workers.py`
- Collected: 274 against a baseline of 274
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_an_interrupted_restamp_names_its_job_command_and_that_command_finishes_it`

Old text:

```
    remediation = dataclasses.replace(cause.remediation, remedy=None, steps=steps)
```

New text:

```
    remediation = dataclasses.replace(cause.remediation, steps=steps)
```

### `u192.F4_command_dropped`

_resumable: the first step says to resume the job without naming the command

- File: `src/cratekit/modules/foreground.py`
- Source: `u192.json`, row `F4_command_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_analysis_workers.py`
- Collected: 274 against a baseline of 274
- Kills: 5 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_job_the_shipped_code_left_with_no_intent_resumes_from_its_staged_report`
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - `tests/test_analysis_workers.py::test_an_interrupt_after_a_renamed_items_report_is_staged_resumes_by_the_printed_command`
  - `tests/test_analysis_workers.py::test_an_interrupted_restamp_names_its_job_command_and_that_command_finishes_it`
  - `tests/test_tag_workers.py::test_an_interrupted_sweep_names_its_job_command_and_that_command_finishes_it`

Old text:

```
        f"resume it with: {command}",
```

New text:

```
        "resume it with its --job command",
```

### `u192.F5_settled_count`

_resumable: report the total in place of the settled count

- File: `src/cratekit/modules/foreground.py`
- Source: `u192.json`, row `F5_settled_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_analysis_workers.py`
- Collected: 274 against a baseline of 274
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_an_interrupted_sweep_names_its_job_command_and_that_command_finishes_it`

Old text:

```
        f"the job is queued again with {progress['settled']} of {progress['total']} "
```

New text:

```
        f"the job is queued again with {progress['total']} of {progress['total']} "
```

### `u192.F8_not_exclusive`

add_job_options: declare the two flags on the parser rather than in one exclusive group

- File: `src/cratekit/modules/foreground.py`
- Source: `u192.json`, row `F8_not_exclusive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_analysis_workers.py`
- Collected: 274 against a baseline of 274
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_queue_only_beside_job_is_refused_before_anything_is_queued[restamp]`
  - `tests/test_analysis_workers.py::test_queue_only_beside_job_is_refused_before_anything_is_queued[run]`
  - `tests/test_tag_workers.py::test_tag_folder_queue_only_beside_job_is_refused_before_anything_is_queued`

Old text:

```
    chosen = parser.add_mutually_exclusive_group()
```

New text:

```
    chosen = parser
```

### `u46-author.M1_no_items_enqueued`

Queue the recording with no item, so the driver has nothing to claim

- File: `src/cratekit/master/cli.py`
- Source: `u46-author.json`, row `M1_no_items_enqueued`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 75 against a baseline of 75
- Kills: 17 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_configuration_that_moved_reaches_the_person_as_a_warning_on_the_resume`
  - `tests/test_master_cli.py::test_a_handler_that_raises_an_undeclared_error_fails_the_item_not_the_driver`
  - `tests/test_master_cli.py::test_a_job_that_failed_on_a_missing_source_is_not_reopened_and_a_fresh_job_masters_it`
  - `tests/test_master_cli.py::test_a_missing_encoder_reports_that_refusal_rather_than_an_internal_defect`
  - `tests/test_master_cli.py::test_a_missing_recording_reports_the_engines_own_cause_on_the_item`
  - `tests/test_master_cli.py::test_a_partial_file_left_in_staging_does_not_refuse_the_next_attempt`
  - `tests/test_master_cli.py::test_a_queued_recording_runs_from_pending_to_done_through_the_resume_branch`
  - `tests/test_master_cli.py::test_a_queued_split_recording_lands_as_one_master_through_the_resume`
  - `tests/test_master_cli.py::test_a_relative_recording_masters_the_same_file_when_the_resume_runs_elsewhere`
  - `tests/test_master_cli.py::test_an_encode_that_produces_nothing_reaches_the_item_as_the_engines_own_cause`
  - `tests/test_master_cli.py::test_an_existing_joined_master_is_refused_on_the_real_destination`
  - `tests/test_master_cli.py::test_an_existing_master_is_refused_before_the_engine_runs`
  - `tests/test_master_cli.py::test_nothing_is_created_beside_a_destination_for_a_recording_that_is_not_there`
  - `tests/test_master_cli.py::test_overwrite_reaches_the_handler_and_replaces_the_previous_master`
  - `tests/test_master_cli.py::test_queueing_a_recording_gives_the_driver_one_item_to_claim`
  - ... and 2 more, see the JSON sidecar

Old text:

```
            item_ids=(str(payload[SOURCE]),),
```

New text:

```
(empty)
```

### `u46-round-2.M6_staging_not_cleared`

Leave a previous attempt's partial encode in the staging directory

- File: `src/cratekit/master/cli.py`
- Source: `u46-round-2.json`, row `M6_staging_not_cleared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 75 against a baseline of 75
- Kills: 2 (killed)
- Killed:
  - `tests/test_job_seam.py::test_a_driver_killed_inside_the_real_handler_resumes_redoing_exactly_that_item`
  - `tests/test_master_cli.py::test_a_partial_file_left_in_staging_does_not_refuse_the_next_attempt`

Old text:

```
    if directory.exists():
        shutil.rmtree(directory)
```

New text:

```
(empty)
```

### `u46-round-2.M7B_engine_refusal_swallowed`

Translate the engine's encoder-failed into a generic internal defect

- File: `src/cratekit/master/cli.py`
- Source: `u46-round-2.json`, row `M7B_engine_refusal_swallowed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 75 against a baseline of 75
- Kills: 23 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_24_bit_and_a_32_bit_part_are_told_apart_by_codec_alone`
  - `tests/test_master_cli.py::test_a_container_the_engine_does_not_read_refuses_under_its_own_slug`
  - `tests/test_master_cli.py::test_a_corrupt_archive_copy_refuses_and_leaves_no_false_safety_copy`
  - `tests/test_master_cli.py::test_a_failed_encode_under_overwrite_says_what_the_person_is_left_holding`
  - `tests/test_master_cli.py::test_a_failing_encode_does_not_report_success`
  - `tests/test_master_cli.py::test_a_job_that_failed_on_a_missing_source_is_not_reopened_and_a_fresh_job_masters_it`
  - `tests/test_master_cli.py::test_a_missing_encoder_reports_that_refusal_rather_than_an_internal_defect`
  - `tests/test_master_cli.py::test_a_missing_part_refuses_as_missing`
  - `tests/test_master_cli.py::test_a_missing_recording_reports_the_engines_own_cause_on_the_item`
  - `tests/test_master_cli.py::test_a_part_named_twice_refuses`
  - `tests/test_master_cli.py::test_a_recording_that_is_not_there_refuses_rather_than_raising`
  - `tests/test_master_cli.py::test_an_archive_holding_different_audio_refuses_and_keeps_both`
  - `tests/test_master_cli.py::test_an_encode_that_exits_zero_and_writes_nothing_does_not_report_success`
  - `tests/test_master_cli.py::test_an_encode_that_produces_nothing_reaches_the_item_as_the_engines_own_cause`
  - `tests/test_master_cli.py::test_an_encode_that_writes_an_empty_file_does_not_report_success`
  - ... and 8 more, see the JSON sidecar

Old text:

```
            str(exc.refusal),
            exc.detail,
```

New text:

```
            "internal-error",
            "the mastering engine refused",
```

### `u184.A1_flag_ignored`

record_ack: never take the session road, so --as session falls to the gate and leaves a run waiting

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A1_flag_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`, `tests/test_crate_sync_skill.py`, `tests/test_rekordbox_visit_skill.py`
- Collected: 81 against a baseline of 81
- Kills: 10 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_a_valid_acknowledgment_a_person_minted_is_reported_over_old_backups`
  - `tests/test_session_ack_by_session.py::test_an_expired_acknowledgment_is_replaced_by_one_command`
  - `tests/test_session_ack_by_session.py::test_an_unreadable_acknowledgment_is_replaced_by_one_command`
  - `tests/test_session_ack_by_session.py::test_one_command_mints_as_the_session_when_both_ages_are_four_days`
  - `tests/test_session_ack_by_session.py::test_one_command_prints_the_expiry_a_person_reads`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[both-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[files-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_reports_a_valid_acknowledgment_and_does_not_mint_again`

Old text:

```
    if getattr(ctx.args, "as_actor", None) == session.SESSION_ACTOR:
```

New text:

```
    if False:
```

### `u184.A2_any_actor_accepted`

build_ack: drop the one value restriction, so --as names any actor and is parsed

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A2_any_actor_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`, `tests/test_crate_sync_skill.py`, `tests/test_rekordbox_visit_skill.py`
- Collected: 81 against a baseline of 81
- Kills: 3 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_the_flag_names_no_actor_but_the_session[Session]`
  - `tests/test_session_ack_by_session.py::test_the_flag_names_no_actor_but_the_session[a-person]`
  - `tests/test_session_ack_by_session.py::test_the_flag_names_no_actor_but_the_session[cli]`

Old text:

```
        choices=(session.SESSION_ACTOR,),
```

New text:

```
        choices=None,
```

### `u192.F7_queue_only_always`

queue_only: always True, so a verb run by hand queues and returns as before U192

- File: `src/cratekit/modules/foreground.py`
- Source: `u192.json`, row `F7_queue_only_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_analysis_workers.py`, `tests/test_label_genre.py`
- Collected: 338 against a baseline of 338
- Kills: 10 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_job_the_shipped_code_left_with_no_intent_resumes_from_its_staged_report`
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - `tests/test_analysis_workers.py::test_an_interrupt_after_a_renamed_items_report_is_staged_resumes_by_the_printed_command`
  - `tests/test_analysis_workers.py::test_an_interrupted_restamp_names_its_job_command_and_that_command_finishes_it`
  - `tests/test_analysis_workers.py::test_analyze_restamp_by_hand_drives_its_job_and_says_the_database_note_once`
  - `tests/test_analysis_workers.py::test_analyze_run_by_hand_queues_and_drives_its_job_to_succeeded_in_one_call`
  - `tests/test_label_genre.py::test_a_sweep_driven_at_its_queue_keeps_the_label_warning_and_never_calls_its_label_unapplied`
  - `tests/test_tag_workers.py::test_an_interrupted_sweep_names_its_job_command_and_that_command_finishes_it`
  - `tests/test_tag_workers.py::test_tag_folder_by_hand_prints_the_settled_job_and_no_drive_command`
  - `tests/test_tag_workers.py::test_tag_folder_by_hand_queues_and_drives_its_sweep_to_succeeded_in_one_call`

Old text:

```
    return bool(getattr(args, "queue_only", False))
```

New text:

```
    return True
```

### `u27-restore-cli-independent.X1_the_off_machine_engine_stops_refusing_an_unconfirmed_restore`

What the from-backup zeros DO leave held: remove the refusal that stops a restore with no recorded decision, in the backup module the verb calls. Paired with I_A1 and with the whole from-backup family of zeros, which are one hole rather than eleven

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u27-restore-cli-independent.json`, row `X1_the_off_machine_engine_stops_refusing_an_unconfirmed_restore`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 455 against a baseline of 455
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_restore_is_a_named_decision_and_never_a_prompt`
  - `tests/test_write_session.py::test_the_restore_is_the_recovery_and_reaches_its_own_refusals`
  - `tests/test_write_session.py::test_the_restores_own_refusals_survive_the_gates_being_added`

Old text:

```
    if not confirmed:
        raise BackupRefused(
            Refusal.RESTORE_NOT_CONFIRMED,
            "a restore replaces the live database and is not performed without an "
            "explicit decision naming this library and this snapshot.",
        )
```

New text:

```
(empty)
```

### `u27-restore-cli-round-2.S3_analysis_watch_watches_nothing`

Arm the analysis watch on no roots, so it reports a clean session either way

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-round-2.json`, row `S3_analysis_watch_watches_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 246 against a baseline of 246
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_the_session_watches_the_whole_library_and_not_a_folder_inside_it`

Old text:

```
        analysis_roots=watched,
```

New text:

```
        analysis_roots=(),
```

