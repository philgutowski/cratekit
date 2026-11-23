# Mutation table: u303-replay-merged4

Measured by `scripts/mutate.py` on 2026-11-23 05:44 UTC, branch `cloud/860-cli-fifth-smaller` at `a7f08ce3`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22529 collected. pytest invocations for this batch: 94.

Full baseline: measured by this driver (the battery's verdict was not read: it was read against another known failures file).

Subset baselines: 10, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `docs/mutation/u303-replay-known-failures.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22529 against 22529. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r-1.E1_dispatch_impl` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 1 | killed |
| `r-1.E2_config_inside_checkout` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 1 | killed |
| `r-1.T10_no_yaml_falls_back` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 1 | killed |
| `r-1.T12_caller_ignores_unknown` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 2 | killed |
| `r-1.T13_missing_other_hook` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 2 | killed |
| `r-1.T15_other_dispatch` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 1 | killed |
| `r-1.T16_same_configuration` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 1 | killed |
| `r-1.T17_install_config_flag` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 1 | killed |
| `r-1.T18_remedy_floor` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 1 | killed |
| `r-1.T19_remedy_reads_config` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 1 | killed |
| `r-1.T1_manual_skip` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 1 | killed |
| `r-1.T20_stage_parameter` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 3 | killed |
| `r-1.T21_ok_names_others` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 1 | killed |
| `r-1.T22_pre_commit_floor` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 13 | killed |
| `r-1.T23_alias_value` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 1 | killed |
| `r-1.T2_alias_map` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 2 | killed |
| `r-1.T3_default_install_types` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 1 | killed |
| `r-1.T4_default_stages` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 1 | killed |
| `r-1.T5_hook_stages` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 12 | killed |
| `r-1.T6_unknown_stage` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 2 | killed |
| `r-1.T7_dedupe` | `src/cratekit/cli/doctor_state.py` | maintainer | 4 file(s) | 1685 | 2 | killed |
| `r-1.T8_not_a_mapping` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 1 | killed |
| `r-1.T9_yaml_error_falls_back` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 1 | killed |
| `r787.D1_doctor_own_list` | `src/cratekit/cli/doctor_state.py` | user | 12 file(s) | 2220 | 4 | killed |
| `r787.D2_set_guard_removed` | `src/cratekit/cli/doctor_state.py` | user | 12 file(s) | 2220 | 1 | killed |
| `r787.D3_source_guard_removed` | `src/cratekit/cli/doctor_state.py` | user | 12 file(s) | 2220 | 1 | killed |
| `u132.D1_doctor_behind` | `src/cratekit/cli/doctor_library.py` | user | 12 file(s) | 2220 | 2 | killed |
| `u132.D2_doctor_defect` | `src/cratekit/cli/doctor_library.py` | user | 12 file(s) | 2220 | 1 | killed |
| `u170.D1_kept_folded` | `src/cratekit/cli/doctor.py` | user | 5 file(s) | 1716 | 1 | killed |
| `u170.D2_status_week` | `src/cratekit/cli/doctor.py` | user | 5 file(s) | 1716 | 1 | killed |
| `u170.D3_open_runs_short` | `src/cratekit/cli/doctor.py` | user | 5 file(s) | 1716 | 1 | killed |
| `u170.D4_line_dropped` | `src/cratekit/cli/doctor.py` | user | 5 file(s) | 1716 | 3 | killed |
| `u206.M24_doctor_set_aside_unnamed` | `src/cratekit/cli/doctor_state.py` | user | 9 file(s) | 1129 | 1 | killed |
| `u27-reports-round-1.D2_required_gate` | `src/cratekit/cli/doctor_library.py` | user | 4 file(s) | 1685 | 1 | killed |
| `u27-reports-round-2.D1_probe_creates` | `src/cratekit/cli/doctor_model.py` | user | 4 file(s) | 1685 | 1 | killed |
| `u27-reports-round-3-fixes.F3_trash_absent_is_a_failure` | `src/cratekit/cli/doctor_library.py` | user | 4 file(s) | 1685 | 1 | killed |
| `u27-round-8-independent.E1_mount_detail_swapped` | `src/cratekit/cli/doctor_library.py` | user | 4 file(s) | 1685 | 1 | killed |
| `u27-round-8-independent.E2_identity_verdict_green` | `src/cratekit/cli/doctor_library.py` | user | 4 file(s) | 1685 | 3 | killed |
| `u27-round-8-independent.E3_found_at_dropped` | `src/cratekit/cli/doctor_library.py` | user | 4 file(s) | 1685 | 1 | killed |
| `u298.H1_config_cause_reason` | `src/cratekit/cli/output.py` | user | 2 file(s) | 352 | 3 | killed |
| `u298.H2_config_cause_origin` | `src/cratekit/cli/output.py` | user | 2 file(s) | 352 | 3 | killed |
| `u27-reports-round-1.D3_trash_remedy` | `src/cratekit/cli/doctor_library.py` | user | 4 file(s) | 1685 | 1 | killed |
| `u170.G1_threshold_boundary` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1716 | 1 | killed |
| `u170.G2_idle_from_start_only` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1716 | 3 | killed |
| `u170.G3_idle_from_write_only` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1716 | 1 | killed |
| `u170.G4_unstattable_is_old` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1716 | 1 | killed |
| `u170.G5_no_abort_retired` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1716 | 2 | killed |
| `u170.G6_missing_verb_branch` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1716 | 1 | killed |
| `u170.G8_malformed_stamp` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1716 | 1 | killed |
| `u132.V5_nothing` | `src/cratekit/cli/verbs/taxonomy.py` | user | 1 file(s) | 51 | 2 | killed |
| `u132.V6_backup_name` | `src/cratekit/cli/verbs/taxonomy.py` | user | 1 file(s) | 51 | 1 | killed |
| `u133-a.P12_verb_warning` | `src/cratekit/cli/verbs/taxonomy.py` | user | 1 file(s) | 51 | 1 | killed |
| `u194.W24_write_copy_bytes_stale` | `src/cratekit/cli/verbs/taxonomy.py` | user | 2 file(s) | 119 | 1 | killed |
| `u194.W25_write_copy_read_back` | `src/cratekit/cli/verbs/taxonomy.py` | user | 2 file(s) | 119 | 2 | killed |
| `r1184.M17_verb_takes_step` | `src/cratekit/cli/verbs/taxonomy_word.py` | user | 1 file(s) | 68 | 3 | killed |
| `r1184.M18_verb_nothing_to_do` | `src/cratekit/cli/verbs/taxonomy_word.py` | user | 1 file(s) | 68 | 1 | killed |
| `u194.W18_carrying_several_genres` | `src/cratekit/cli/verbs/taxonomy_word.py` | user | 1 file(s) | 68 | 1 | killed |
| `u194.W19_carrying_unread` | `src/cratekit/cli/verbs/taxonomy_word.py` | user | 1 file(s) | 68 | 2 | killed |
| `u194.W22_unwritten_refusal` | `src/cratekit/cli/verbs/taxonomy_word.py` | user | 1 file(s) | 68 | 1 | killed |
| `u194.W23_root_missing` | `src/cratekit/cli/verbs/taxonomy_word.py` | user | 1 file(s) | 68 | 1 | killed |
| `r290-author.D1_dispatcher_ignores_the_type` | `src/cratekit/cli/__init__.py` | user | 57 file(s) | 7247 | 47 | killed |
| `r290-author.D2_parked_marked_resumable` | `src/cratekit/cli/__init__.py` | user | 57 file(s) | 7247 | 2 | killed |
| `r290-author.D4_cancelled_reads_failed` | `src/cratekit/cli/__init__.py` | user | 57 file(s) | 7247 | 22 | killed |
| `u193.M16_continue_job_branch` | `src/cratekit/cli/__init__.py` | user | 5 file(s) | 522 | 1 | killed |
| `u193.M19_parked_outcome` | `src/cratekit/cli/__init__.py` | user | 5 file(s) | 522 | 1 | killed |
| `u193.M20_continue_step_not_written` | `src/cratekit/cli/__init__.py` | user | 5 file(s) | 522 | 3 | killed |
| `u193.M21_swallowed_warning_dropped` | `src/cratekit/cli/__init__.py` | user | 5 file(s) | 522 | 1 | killed |
| `u193.M22_warning_said_twice` | `src/cratekit/cli/__init__.py` | user | 5 file(s) | 522 | 1 | killed |
| `u193.M23_calls_floor` | `src/cratekit/cli/__init__.py` | user | 5 file(s) | 522 | 1 | killed |
| `u206.M23_lookup_line_dropped` | `src/cratekit/cli/__init__.py` | user | 9 file(s) | 1129 | 3 | killed |
| `u170.R10_moved_guard` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1716 | 1 | killed |
| `u170.R11_digest_ids_only` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1716 | 1 | killed |
| `u170.R12_default_week` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1716 | 1 | killed |
| `u170.R1_zero_days` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1716 | 1 | killed |
| `u170.R2_ceiling` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1716 | 1 | killed |
| `u170.R3_own_run` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1716 | 1 | killed |
| `u170.R4_unreadable_dropped` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1716 | 1 | killed |
| `u170.R5_answers_apply` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1716 | 2 | killed |
| `u170.R6_actor_cli` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1716 | 2 | killed |
| `u170.R7_declined_applies` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1716 | 1 | killed |
| `u170.R8_empty_asks` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1716 | 2 | killed |
| `u170.R9_kept_planned` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1716 | 1 | killed |

## Row definitions

### `r-1.E1_dispatch_impl`

Existing guard, sample: drop the requirement that the hook invokes hook-impl

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `E1_dispatch_impl`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_hook_that_does_not_dispatch_to_this_repository_is_refused[#!/bin/sh\n# pre-commit\nexit 0\n-True-hook-impl]`

Old text:

```
    if _HOOK_DISPATCH not in body:
        return f"it never invokes pre-commit's {_HOOK_DISPATCH}"

```

New text:

```
(empty)
```

### `r-1.E2_config_inside_checkout`

Existing guard, sample: drop the requirement that the named configuration is inside the checkout

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `E2_config_inside_checkout`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_hook_that_does_not_dispatch_to_this_repository_is_refused[ARGS=(hook-impl --config=/elsewhere/.pre-commit-config.yaml --hook-type=pre-commit)\n-True-outside]`

Old text:

```
    if root.resolve() not in resolved.parents and resolved != root.resolve():
```

New text:

```
    if False:
```

### `r-1.T10_no_yaml_falls_back`

PyYAML missing falls back to the pre-commit floor instead of a sentence

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T10_no_yaml_falls_back`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_no_yaml_reader_is_unknown_rather_than_one_hook_type`

Old text:

```
    except ImportError:
        return (
            (),
            (
                f"PyYAML is not importable from this interpreter, so the hook types "
                f"{config_file.name} configures could not be read. Install the dev "
                f"extra, `pip install -e '.[dev]'`"
            ),
            None,
        )

```

New text:

```
    except ImportError:
        return ("pre-commit",), None, None

```

### `r-1.T12_caller_ignores_unknown`

The check ignores an unknown configuration and reports on no extra types

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T12_caller_ignores_unknown`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_configuration_that_does_not_parse_is_not_read_as_one_hook_type`
  - `tests/test_doctor.py::test_no_yaml_reader_is_unknown_rather_than_one_hook_type`

Old text:

```
    if unknown is not None:
```

New text:

```
    if False:
```

### `r-1.T13_missing_other_hook`

A configured hook type with no hook file is not reported

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T13_missing_other_hook`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_configured_commit_msg_stage_with_no_hook_is_refused`
  - `tests/test_doctor.py::test_the_install_line_names_a_configuration_that_is_not_the_default`

Old text:

```
            absent.append(f"no {hook_type} hook at {other}")
            continue

```

New text:

```
            continue

```

### `r-1.T15_other_dispatch`

A configured hook that does not dispatch for its own stage is not reported

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T15_other_dispatch`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_commit_msg_hook_installed_for_another_stage_is_refused`

Old text:

```
        if other_problem is not None:
            absent.append(

```

New text:

```
        if other_problem is not None:
            continue
            absent.append(

```

### `r-1.T16_same_configuration`

Drop the requirement that every other hook dispatches to the pre-commit hook's configuration

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T16_same_configuration`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_commit_msg_hook_on_another_configuration_is_refused`

Old text:

```
        if _config_path(other_name, root).resolve() != config_file.resolve():
```

New text:

```
        if False:
```

### `r-1.T17_install_config_flag`

The install line never names a non-default configuration

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T17_install_config_flag`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_install_line_names_a_configuration_that_is_not_the_default`

Old text:

```
    if config_name != _HOOK_CONFIG_DEFAULT:
```

New text:

```
    if False:
```

### `r-1.T18_remedy_floor`

With no readable configuration the install line names no type at all

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T18_remedy_floor`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_clone_with_no_configuration_is_told_the_floor`

Old text:

```
    return _install_command(types if problem is None else ("pre-commit",))
```

New text:

```
    return _install_command(types)
```

### `r-1.T19_remedy_reads_config`

The fresh clone install line stops reading the configuration and names only pre-commit

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T19_remedy_reads_config`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_fresh_clone_is_told_the_whole_install_line`

Old text:

```
    types, problem, _remedy = _configured_hook_types(root / _HOOK_CONFIG_DEFAULT)
```

New text:

```
    types, problem, _remedy = ("pre-commit",), None, None
```

### `r-1.T1_manual_skip`

Stop skipping the manual stage, so a manual-only hook reads as an unknown stage

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T1_manual_skip`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[text5-expected5]`

Old text:

```
        if hook_type == "manual":  # run by hand, never by git
            continue

```

New text:

```
(empty)
```

### `r-1.T20_stage_parameter`

The dispatch check ignores the hook type it was asked about and always wants pre-commit

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T20_stage_parameter`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 3 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_commit_msg_hook_installed_for_another_stage_is_refused`
  - `tests/test_doctor.py::test_a_commit_msg_hook_on_another_configuration_is_refused`
  - `tests/test_doctor.py::test_every_configured_hook_type_installed_passes_the_check`

Old text:

```
    stage = f"--hook-type={hook_type}"
```

New text:

```
    stage = "--hook-type=pre-commit"
```

### `r-1.T21_ok_names_others`

The OK detail stops naming the other stages it verified

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T21_ok_names_others`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_every_configured_hook_type_installed_passes_the_check`

Old text:

```
        if len(types) > 1

```

New text:

```
        if False

```

### `r-1.T22_pre_commit_floor`

Pre-commit is no longer the floor of the needed types

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T22_pre_commit_floor`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 13 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_commit_msg_hook_installed_for_another_stage_is_refused`
  - `tests/test_doctor.py::test_a_commit_msg_hook_on_another_configuration_is_refused`
  - `tests/test_doctor.py::test_a_configured_commit_msg_stage_with_no_hook_is_refused`
  - `tests/test_doctor.py::test_a_fresh_clone_is_told_the_whole_install_line`
  - `tests/test_doctor.py::test_every_configured_hook_type_installed_passes_the_check`
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[default_install_hook_types: [pre-push]\nrepos: []\n-expected2]`
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[default_stages: [push]\nrepos: []\n-expected3]`
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[repos: []\n-expected0]`
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[text1-expected1]`
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[text5-expected5]`
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[text6-expected6]`
  - `tests/test_doctor.py::test_the_install_line_names_a_configuration_that_is_not_the_default`
  - `tests/test_doctor.py::test_this_repositorys_own_configuration_needs_both_hook_types`

Old text:

```
    types = ["pre-commit"]
    for stage in named:

```

New text:

```
    types = []
    for stage in named:

```

### `r-1.T23_alias_value`

Map merge-commit to a realistic nearby wrong hook, pre-commit

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T23_alias_value`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[text4-expected4]`

Old text:

```
"merge-commit": "pre-merge-commit"
```

New text:

```
"merge-commit": "pre-commit"
```

### `r-1.T2_alias_map`

Stop mapping the legacy stage spellings (commit, push, merge-commit) to their hook types

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T2_alias_map`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[default_stages: [push]\nrepos: []\n-expected3]`
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[text4-expected4]`

Old text:

```
hook_type = _STAGE_ALIASES.get(stage, stage) if isinstance(stage, str) else None
```

New text:

```
hook_type = stage if isinstance(stage, str) else None
```

### `r-1.T3_default_install_types`

Ignore default_install_hook_types when deriving the needed hook types

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T3_default_install_types`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[default_install_hook_types: [pre-push]\nrepos: []\n-expected2]`

Old text:

```
    named.extend(document.get("default_install_hook_types") or [])

```

New text:

```
(empty)
```

### `r-1.T4_default_stages`

Ignore default_stages when deriving the needed hook types

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T4_default_stages`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[default_stages: [push]\nrepos: []\n-expected3]`

Old text:

```
    named.extend(document.get("default_stages") or [])

```

New text:

```
(empty)
```

### `r-1.T5_hook_stages`

Ignore every hook's own stages, the reading that finds this repository's commit-msg stage

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T5_hook_stages`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 12 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_commit_msg_hook_installed_for_another_stage_is_refused`
  - `tests/test_doctor.py::test_a_commit_msg_hook_on_another_configuration_is_refused`
  - `tests/test_doctor.py::test_a_configuration_this_cannot_understand_is_a_sentence[text0-'on-commit']`
  - `tests/test_doctor.py::test_a_configuration_this_cannot_understand_is_a_sentence[text1-installs no hook for]`
  - `tests/test_doctor.py::test_a_configured_commit_msg_stage_with_no_hook_is_refused`
  - `tests/test_doctor.py::test_a_fresh_clone_is_told_the_whole_install_line`
  - `tests/test_doctor.py::test_every_configured_hook_type_installed_passes_the_check`
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[text1-expected1]`
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[text4-expected4]`
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[text6-expected6]`
  - `tests/test_doctor.py::test_the_install_line_names_a_configuration_that_is_not_the_default`
  - `tests/test_doctor.py::test_this_repositorys_own_configuration_needs_both_hook_types`

Old text:

```
                named.extend(hook.get("stages") or [])
```

New text:

```
                pass
```

### `r-1.T6_unknown_stage`

Skip an unknown stage instead of refusing the configuration

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T6_unknown_stage`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_configuration_this_cannot_understand_is_a_sentence[text0-'on-commit']`
  - `tests/test_doctor.py::test_a_configuration_this_cannot_understand_is_a_sentence[text1-installs no hook for]`

Old text:

```
        if hook_type not in _HOOK_TYPES:
            return (
                (),
                f"{config_file} names a stage pre-commit installs no hook for, {stage!r}",
                None,
            )

```

New text:

```
        if hook_type not in _HOOK_TYPES:
            continue

```

### `r-1.T7_dedupe`

Append a type every time it is named rather than once

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T7_dedupe`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[text4-expected4]`
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[text6-expected6]`

Old text:

```
        if hook_type not in types:
            types.append(hook_type)

```

New text:

```
        types.append(hook_type)

```

### `r-1.T8_not_a_mapping`

Drop the guard refusing a configuration whose top level is not a mapping

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T8_not_a_mapping`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_configuration_this_cannot_understand_is_a_sentence[- just\n- a list\n-is not a pre-commit configuration]`

Old text:

```
    if not isinstance(document, dict):
        return (), f"{config_file} is not a pre-commit configuration", None

```

New text:

```
(empty)
```

### `r-1.T9_yaml_error_falls_back`

A configuration that does not parse falls back to the pre-commit floor instead of a sentence

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T9_yaml_error_falls_back`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_configuration_that_does_not_parse_is_not_read_as_one_hook_type`

Old text:

```
    except yaml.YAMLError as exc:
        return (), f"{config_file} is not valid YAML ({exc})", None

```

New text:

```
    except yaml.YAMLError:
        return ("pre-commit",), None, None

```

### `r787.D1_doctor_own_list`

doctor's _declared_trees keeps a list of its own, the routing tree alone, instead of asking cutover_trees

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r787.json`, row `D1_doctor_own_list`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_cutover_cli.py`, `tests/test_doctor.py`, `tests/test_incremental_sync.py`, `tests/test_intake_imported.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_paths_resolved.py`, `tests/test_routing_workers.py`
- Collected: 2220 against a baseline of 2220
- Kills: 4 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_doctor_and_the_verb_read_one_set_of_cutover_trees`
  - `tests/test_cutover_cli.py::test_doctor_fails_on_a_native_record_the_cutover_would_refuse_to_create`
  - `tests/test_cutover_cli.py::test_doctor_reads_a_native_inbox_record_as_ok`
  - `tests/test_cutover_cli.py::test_doctor_reads_an_inbox_the_verb_cut_over_as_ok`

Old text:

```
    return tuple(named), tree_registry.cutover_trees(declared), None
```

New text:

```
    return tuple(named), frozenset({declared.tree.id}), None
```

### `r787.D2_set_guard_removed`

doctor stops judging a native record by the set, so a native catalogue tree reads ok

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r787.json`, row `D2_set_guard_removed`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_cutover_cli.py`, `tests/test_doctor.py`, `tests/test_incremental_sync.py`, `tests/test_intake_imported.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_paths_resolved.py`, `tests/test_routing_workers.py`
- Collected: 2220 against a baseline of 2220
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_doctor_lists_and_fails_a_recorded_tree_the_taxonomy_does_not_declare`

Old text:

```
            tree_id not in may_cut_over or record.source not in tree_registry.REBUILDABLE
```

New text:

```
            record.source not in tree_registry.REBUILDABLE
```

### `r787.D3_source_guard_removed`

doctor stops judging a native record by its source, so a native inbox from a catalogue crawl reads ok

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r787.json`, row `D3_source_guard_removed`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_cutover_cli.py`, `tests/test_doctor.py`, `tests/test_incremental_sync.py`, `tests/test_intake_imported.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_paths_resolved.py`, `tests/test_routing_workers.py`
- Collected: 2220 against a baseline of 2220
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_doctor_fails_a_native_inbox_whose_source_no_rebuild_reproduces`

Old text:

```
            tree_id not in may_cut_over or record.source not in tree_registry.REBUILDABLE
```

New text:

```
            tree_id not in may_cut_over
```

### `u132.D1_doctor_behind`

Doctor reads a copy behind the shipped schema as OK

- File: `src/cratekit/cli/doctor_library.py`
- Source: `u132.json`, row `D1_doctor_behind`
- Moved: the same text, now in src/cratekit/cli/doctor_library.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_cutover_cli.py`, `tests/test_doctor.py`, `tests/test_incremental_sync.py`, `tests/test_intake_imported.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_paths_resolved.py`, `tests/test_routing_workers.py`
- Collected: 2220 against a baseline of 2220
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_current_copy_with_every_entry_is_ok`
  - `tests/test_doctor.py::test_a_version_2_copy_without_favorites_is_named_with_both_versions`

Old text:

```
    if not found.behind:

```

New text:

```
    if found.behind:

```

### `u132.D2_doctor_defect`

Doctor reports a shipped template defect as the copy not compared

- File: `src/cratekit/cli/doctor_library.py`
- Source: `u132.json`, row `D2_doctor_defect`
- Moved: the same text, now in src/cratekit/cli/doctor_library.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_cutover_cli.py`, `tests/test_doctor.py`, `tests/test_incremental_sync.py`, `tests/test_intake_imported.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_paths_resolved.py`, `tests/test_routing_workers.py`
- Collected: 2220 against a baseline of 2220
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_shipped_template_that_does_not_load_is_a_defect_and_not_the_copy`

Old text:

```
        if exc.cause.reason == "internal-error":

```

New text:

```
        if False:

```

### `u170.D1_kept_folded`

status: fold every old gate, the kept ones too

- File: `src/cratekit/cli/doctor.py`
- Source: `u170.json`, row `D1_kept_folded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1716 against a baseline of 1716
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_an_old_gate_the_command_would_keep_is_listed_and_never_collapsed`

Old text:

```
            if aged is not None and aged.retirable:
```

New text:

```
            if aged is not None:
```

### `u170.D2_status_week`

status: threshold fixed at seven days, not the file's

- File: `src/cratekit/cli/doctor.py`
- Source: `u170.json`, row `D2_status_week`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1716 against a baseline of 1716
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_status_reads_the_threshold_from_the_file`

Old text:

```
    runs, folded = _run_report(timedelta(days=cfg.reports.open_gate_stale_days))
```

New text:

```
    runs, folded = _run_report(timedelta(days=7))
```

### `u170.D3_open_runs_short`

status: open_runs leaves the folded gates out

- File: `src/cratekit/cli/doctor.py`
- Source: `u170.json`, row `D3_open_runs_short`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1716 against a baseline of 1716
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_status_collapses_old_gates_into_one_line_and_lists_new_ones_as_before`

Old text:

```
            "open_runs": sum(1 for f in findings if f.key.startswith("run.")) + folded,
```

New text:

```
            "open_runs": sum(1 for f in findings if f.key.startswith("run.")),
```

### `u170.D4_line_dropped`

status: fold the gates and print no line for them

- File: `src/cratekit/cli/doctor.py`
- Source: `u170.json`, row `D4_line_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1716 against a baseline of 1716
- Kills: 3 (killed)
- Killed:
  - `tests/test_run_retire.py::test_status_collapses_old_gates_into_one_line_and_lists_new_ones_as_before`
  - `tests/test_run_retire.py::test_status_reads_the_threshold_from_the_file`
  - `tests/test_run_retire.py::test_the_collapsed_line_names_the_dates_it_spans_and_reaches_a_person`

Old text:

```
    if old and older_than is not None:
```

New text:

```
    if False:
```

### `u206.M24_doctor_set_aside_unnamed`

_check_isrc_cache: leave the set aside files out of the note

- File: `src/cratekit/cli/doctor_state.py`
- Source: `u206.json`, row `M24_doctor_set_aside_unnamed`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1129 against a baseline of 1129
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_doctor_names_a_set_aside_file_and_never_fails`

Old text:

```
    aside = cache.set_aside()
    if aside:
```

New text:

```
    aside = cache.set_aside()
    if False:
```

### `u27-reports-round-1.D2_required_gate`

Report a broken Trash as a failure even where no verb needs it

- File: `src/cratekit/cli/doctor_library.py`
- Source: `u27-reports-round-1.json`, row `D2_required_gate`
- Moved: the same text, now in src/cratekit/cli/doctor_library.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_broken_trash_is_informational_when_no_verb_this_profile_needs_it`

Old text:

```
    if not inputs.required(key):
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"{status.problem}, and no verb this profile switches on moves a "
                f"file to the Trash, so nothing depends on it today"
            ),
        )

```

New text:

```
(empty)
```

### `u27-reports-round-2.D1_probe_creates`

Round 1 zero, re-run against the replacement guard: take the creating default

- File: `src/cratekit/cli/doctor_model.py`
- Source: `u27-reports-round-2.json`, row `D1_probe_creates`
- Moved: the same text, now in src/cratekit/cli/doctor_model.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_trash_check_cannot_pass_by_having_run`

Old text:

```
    return trash.probe(path, create=False)
```

New text:

```
    return trash.probe(path, create=True)
```

### `u27-reports-round-3-fixes.F3_trash_absent_is_a_failure`

Report a volume whose Trash has not been created yet as a failure again

- File: `src/cratekit/cli/doctor_library.py`
- Source: `u27-reports-round-3-fixes.json`, row `F3_trash_absent_is_a_failure`
- Moved: the same text, now in src/cratekit/cli/doctor_library.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_volume_with_no_trash_directory_yet_is_not_a_failure`

Old text:

```
    if status.absent:
```

New text:

```
    if False:
```

### `u27-round-8-independent.E1_mount_detail_swapped`

Swap the NOT_MOUNTED and MOUNTED_ELSEWHERE sentences, conflating unmounted with moved

- File: `src/cratekit/cli/doctor_library.py`
- Source: `u27-round-8-independent.json`, row `E1_mount_detail_swapped`
- Moved: the same text, now in src/cratekit/cli/doctor_library.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_unmounted_volume_and_a_moved_volume_produce_different_messages`

Old text:

```
        preflight.MountState.NOT_MOUNTED: (
            "the recorded volume is not mounted anywhere and the configured root "
            "does not exist. Attach it"
        ),
        preflight.MountState.MOUNTED_ELSEWHERE: (
            "the recorded volume IS attached, at a different mount point than the "
            "configured root. Nothing needs plugging in; the configured root is "
            "pointing at the wrong place"
        ),
```

New text:

```
        preflight.MountState.NOT_MOUNTED: (
            "the recorded volume IS attached, at a different mount point than the "
            "configured root. Nothing needs plugging in; the configured root is "
            "pointing at the wrong place"
        ),
        preflight.MountState.MOUNTED_ELSEWHERE: (
            "the recorded volume is not mounted anywhere and the configured root "
            "does not exist. Attach it"
        ),
```

### `u27-round-8-independent.E2_identity_verdict_green`

Report the identity check GREEN for an absent and for a relocated volume

- File: `src/cratekit/cli/doctor_library.py`
- Source: `u27-round-8-independent.json`, row `E2_identity_verdict_green`
- Moved: the same text, now in src/cratekit/cli/doctor_library.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 3 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_volume_mounted_elsewhere_is_one_problem_reported_once`
  - `tests/test_doctor.py::test_an_unmounted_volume_never_reports_a_matching_identity`
  - `tests/test_doctor.py::test_the_identity_check_never_reports_green_over_an_identity_that_did_not_match`

Old text:

```
            preflight.MountState.NOT_MOUNTED: (Status.INFO, None),
            preflight.MountState.MOUNTED_ELSEWHERE: (Status.INFO, None),
```

New text:

```
            preflight.MountState.NOT_MOUNTED: (Status.OK, None),
            preflight.MountState.MOUNTED_ELSEWHERE: (Status.OK, None),
```

### `u27-round-8-independent.E3_found_at_dropped`

Stop telling the user where a relocated volume actually is

- File: `src/cratekit/cli/doctor_library.py`
- Source: `u27-round-8-independent.json`, row `E3_found_at_dropped`
- Moved: the same text, now in src/cratekit/cli/doctor_library.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_unmounted_volume_and_a_moved_volume_produce_different_messages`

Old text:

```
    if status.state is preflight.MountState.MOUNTED_ELSEWHERE:
        where = f" (configured root {status.configured_root}, found at {status.found_at})"
```

New text:

```
(empty)
```

### `u298.H1_config_cause_reason`

load_config: an unusable config ends a cause other than config-unusable

- File: `src/cratekit/cli/output.py`
- Source: `u298.json`, row `H1_config_cause_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`, `tests/test_config.py`
- Collected: 352 against a baseline of 352
- Kills: 3 (killed)
- Killed:
  - `tests/test_shared_homes.py::test_an_unusable_config_is_one_typed_cause_whatever_verb_met_it[failure0-run-setup]`
  - `tests/test_shared_homes.py::test_an_unusable_config_is_one_typed_cause_whatever_verb_met_it[failure1-fix-config-values]`
  - `tests/test_shared_homes.py::test_an_unusable_config_is_one_typed_cause_whatever_verb_met_it[failure2-run-doctor]`

Old text:

```
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=origin,
```

New text:

```
                reason="internal-error",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=origin,
```

### `u298.H2_config_cause_origin`

load_config: the refusal no longer names the verb that met it

- File: `src/cratekit/cli/output.py`
- Source: `u298.json`, row `H2_config_cause_origin`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`, `tests/test_config.py`
- Collected: 352 against a baseline of 352
- Kills: 3 (killed)
- Killed:
  - `tests/test_shared_homes.py::test_an_unusable_config_is_one_typed_cause_whatever_verb_met_it[failure0-run-setup]`
  - `tests/test_shared_homes.py::test_an_unusable_config_is_one_typed_cause_whatever_verb_met_it[failure1-fix-config-values]`
  - `tests/test_shared_homes.py::test_an_unusable_config_is_one_typed_cause_whatever_verb_met_it[failure2-run-doctor]`

Old text:

```
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=origin,
                detail={"kind": type(exc).__name__},
```

New text:

```
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=(),
                detail={"kind": type(exc).__name__},
```

### `u27-reports-round-1.D3_trash_remedy`

Answer a broken Trash with run-doctor, which is the token that sends a person here

- File: `src/cratekit/cli/doctor_library.py`
- Source: `u27-reports-round-1.json`, row `D3_trash_remedy`
- Moved: U303 split cli/doctor.py and moved the trash probe's finding, verbatim but for its comment, to cli/doctor_library.py; the remedy is the same value, swapped the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_volume_with_no_usable_trash_refuses_because_a_verb_depends_on_it`

Old text:

```
        # are a path to grant; another filesystem is named in the sentence.
        remedy=Remedy.GRANT_PATH_ACCESS,
```

New text:

```
        # are a path to grant; another filesystem is named in the sentence.
        remedy=Remedy.RUN_DOCTOR,
```

### `u170.G1_threshold_boundary`

old_gate: a gate idle exactly the threshold counts as old

- File: `src/cratekit/cli/gates.py`
- Source: `u170.json`, row `G1_threshold_boundary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1716 against a baseline of 1716
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_a_gate_exactly_at_the_threshold_is_not_yet_old`

Old text:

```
    if now - since <= older_than:
```

New text:

```
    if now - since < older_than:
```

### `u170.G2_idle_from_start_only`

idle_since: age from created alone, so a resumed run is old

- File: `src/cratekit/cli/gates.py`
- Source: `u170.json`, row `G2_idle_from_start_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1716 against a baseline of 1716
- Kills: 3 (killed)
- Killed:
  - `tests/test_run_retire.py::test_a_gate_exactly_at_the_threshold_is_not_yet_old`
  - `tests/test_run_retire.py::test_a_run_resumed_recently_is_not_old_however_long_ago_it_started`
  - `tests/test_run_retire.py::test_an_answer_is_stale_once_a_planned_run_is_resumed_even_if_it_stays_old`

Old text:

```
    return written if started is None else max(started, written)
```

New text:

```
    return written if started is None else started
```

### `u170.G3_idle_from_write_only`

idle_since: age from the record's write alone, so a copied record with an old date is old

- File: `src/cratekit/cli/gates.py`
- Source: `u170.json`, row `G3_idle_from_write_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1716 against a baseline of 1716
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_a_run_started_recently_is_not_old_whatever_its_file_says`

Old text:

```
    return written if started is None else max(started, written)
```

New text:

```
    return written
```

### `u170.G4_unstattable_is_old`

idle_since: a record whose time cannot be read is as old as the epoch

- File: `src/cratekit/cli/gates.py`
- Source: `u170.json`, row `G4_unstattable_is_old`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1716 against a baseline of 1716
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_a_record_whose_time_cannot_be_read_is_never_old`

Old text:

```
        return datetime.now(timezone.utc)
```

New text:

```
        return datetime.fromtimestamp(0, tz=timezone.utc)
```

### `u170.G5_no_abort_retired`

old_gate: drop the no abort refusal, so sync.pair gates are planned

- File: `src/cratekit/cli/gates.py`
- Source: `u170.json`, row `G5_no_abort_retired`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1716 against a baseline of 1716
- Kills: 2 (killed)
- Killed:
  - `tests/test_run_retire.py::test_an_old_gate_the_command_would_keep_is_listed_and_never_collapsed`
  - `tests/test_run_retire.py::test_retire_lists_what_it_retired_and_what_it_kept`

Old text:

```
    elif RETIRE_OPTION not in spec.options:
```

New text:

```
    elif False:
```

### `u170.G6_missing_verb_branch`

old_gate: drop the missing verb reason, so the fallback reason speaks for it

- File: `src/cratekit/cli/gates.py`
- Source: `u170.json`, row `G6_missing_verb_branch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1716 against a baseline of 1716
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_a_gate_whose_verb_is_gone_is_old_and_kept`

Old text:

```
    if owner is None:
        kept: str | None = f"{state.verb} is not a verb in this build"
    elif spec is None:
```

New text:

```
    if owner is None and False:
        kept: str | None = f"{state.verb} is not a verb in this build"
    elif spec is None:
```

### `u170.G8_malformed_stamp`

_instant: a malformed created stamp raises instead of reading as unknown

- File: `src/cratekit/cli/gates.py`
- Source: `u170.json`, row `G8_malformed_stamp`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1716 against a baseline of 1716
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_a_hand_edited_start_stamp_is_aged_by_the_records_last_write`

Old text:

```
    except (TypeError, ValueError):
        return None
    return moment if
```

New text:

```
    except TypeError:
        return None
    return moment if
```

### `u132.V5_nothing`

A plan that writes nothing still asks the gate

- File: `src/cratekit/cli/verbs/taxonomy.py`
- Source: `u132.json`, row `V5_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_upgrade.py`
- Collected: 51 against a baseline of 51
- Kills: 2 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_a_second_run_plans_nothing_and_asks_nothing`
  - `tests/test_taxonomy_upgrade.py::test_what_is_held_is_said_and_written_around`

Old text:

```
    if not found.writes:

```

New text:

```
    if False:

```

### `u132.V6_backup_name`

A backup takes the name an earlier backup holds

- File: `src/cratekit/cli/verbs/taxonomy.py`
- Source: `u132.json`, row `V6_backup_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_upgrade.py`
- Collected: 51 against a baseline of 51
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_a_backup_never_takes_an_earlier_backups_name`

Old text:

```
    while candidate.exists():

```

New text:

```
    while False:

```

### `u133-a.P12_verb_warning`

The verb drops the keyword rule warning

- File: `src/cratekit/cli/verbs/taxonomy.py`
- Source: `u133-a.json`, row `P12_verb_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_upgrade.py`
- Collected: 51 against a baseline of 51
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_the_upgrade_that_adds_jazz_says_the_copys_keyword_rule_is_left`

Old text:

```
    ] + [{"code": KEYWORD_RULE, "message": sentence} for sentence in found.keywords]

```

New text:

```
    ]

```

### `u194.W24_write_copy_bytes_stale`

write_copy: drop the byte check after the second plan, so an edit made since is written over

- File: `src/cratekit/cli/verbs/taxonomy.py`
- Source: `u194.json`, row `W24_write_copy_bytes_stale`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`, `tests/test_taxonomy_upgrade.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_an_edit_after_the_second_plan_is_refused_as_stale`

Old text:

```
    if as_read(raw) != before:
```

New text:

```
    if False:
```

### `u194.W25_write_copy_read_back`

write_copy: drop the read back, so a copy that does not load is left as every verb's declaration

- File: `src/cratekit/cli/verbs/taxonomy.py`
- Source: `u194.json`, row `W25_write_copy_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`, `tests/test_taxonomy_upgrade.py`
- Collected: 119 against a baseline of 119
- Kills: 2 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_a_copy_that_does_not_read_back_is_replaced_by_the_one_it_replaced`
  - `tests/test_taxonomy_upgrade.py::test_a_restore_that_fails_says_so_and_names_the_backup`

Old text:

```
    problem = _read_back(cfg, path, written)
    if problem is not None:
```

New text:

```
    problem = _read_back(cfg, path, written)
    if False:
```

### `r1184.M17_verb_takes_step`

taxonomy alias verb: ignore the refusal's own step, so the bare folder and own name refusals say leave the word

- File: `src/cratekit/cli/verbs/taxonomy_word.py`
- Source: `r1184.json`, row `M17_verb_takes_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 68 against a baseline of 68
- Kills: 3 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_file_carrying_a_folders_own_name_is_never_retagged`
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_its_folder_cannot_take_is_refused_with_its_step`
  - `tests/test_taxonomy_word.py::test_the_bare_folder_refusal_names_the_folder_verb_as_its_step`

Old text:

```
    if exc.step:

```

New text:

```
    if False:

```

### `r1184.M18_verb_nothing_to_do`

taxonomy alias verb: the no change sentence for an own name claims a tagging alias

- File: `src/cratekit/cli/verbs/taxonomy_word.py`
- Source: `r1184.json`, row `M18_verb_nothing_to_do`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 68 against a baseline of 68
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_in_another_case_is_retagged_to_the_exact_name`

Old text:

```
                        if edit.own_name

```

New text:

```
                        if False

```

### `u194.W18_carrying_several_genres`

carrying: plan a write for a file carrying the word beside another genre

- File: `src/cratekit/cli/verbs/taxonomy_word.py`
- Source: `u194.json`, row `W18_carrying_several_genres`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 68 against a baseline of 68
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_file_with_two_genres_is_left_and_named`

Old text:

```
        current = _JOINED.join(values)
        if len(values) == 1:
```

New text:

```
        current = _JOINED.join(values)
        if True:
```

### `u194.W19_carrying_unread`

carrying: read a file whose genre could not be read as one carrying no genre

- File: `src/cratekit/cli/verbs/taxonomy_word.py`
- Source: `u194.json`, row `W19_carrying_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 68 against a baseline of 68
- Kills: 2 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_file_whose_genre_cannot_be_read_is_named_and_never_called_clean`
  - `tests/test_taxonomy_word.py::test_nothing_to_do_does_not_claim_a_file_it_could_not_read`

Old text:

```
        if values is None:
            items.append(FileItem(path=path, relative=relative, change=UNREAD))
            continue
```

New text:

```
        if values is None:
            continue
```

### `u194.W22_unwritten_refusal`

alias verb: leave a file the writer could not write out of the refusal, so the run reports success

- File: `src/cratekit/cli/verbs/taxonomy_word.py`
- Source: `u194.json`, row `W22_unwritten_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 68 against a baseline of 68
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_file_that_will_not_take_the_genre_is_named_and_the_rerun_finishes`

Old text:

```
    if done.moved or done.failed or done.wrong:
```

New text:

```
    if done.moved or done.wrong:
```

### `u194.W23_root_missing`

_root: drop the refusal of a folder that is not there, so the walk plans nothing and reads clean

- File: `src/cratekit/cli/verbs/taxonomy_word.py`
- Source: `u194.json`, row `W23_root_missing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 68 against a baseline of 68
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_folder_that_is_not_there_is_refused_with_nothing_written`

Old text:

```
    if not root.is_dir():
        raise refuse(
            "source-missing",
            f"{root} is not a folder, so there are no files to retag; nothing was written",
```

New text:

```
    if False:
        raise refuse(
            "source-missing",
            f"{root} is not a folder, so there are no files to retag; nothing was written",
```

### `r290-author.D1_dispatcher_ignores_the_type`

Make the dispatcher blind to JobBlocked, so a parked job exits non zero and says failed

- File: `src/cratekit/cli/__init__.py`
- Source: `r290-author.json`, row `D1_dispatcher_ignores_the_type`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_cutover_parity.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_job_outcome.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_approved.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_workers.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_pending_units.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_review_queue.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_install.py`, `tests/test_skills_lint.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`, `tests/test_write_session.py`
- Collected: 7247 against a baseline of 7247
- Kills: 47 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_provider_block_parks_the_job_and_makes_no_further_request`
  - `tests/test_acquire_workers.py::test_an_authentication_failure_parks_the_run_and_names_the_replacement_path`
  - `tests/test_adopt_workers.py::test_a_parked_adoption_leaves_blocked_and_non_zero`
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
  - `tests/test_job_outcome.py::test_a_park_on_a_gate_coded_cause_is_still_not_resumable_through_the_run`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.bandcamp-fetch]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.download]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.fallback-fetch]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[adopt.scan]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[analyze.restamp]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[analyze.run]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[analyze.vocals]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[backup.run]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[export.playlist]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[intake.playlist]`
  - ... and 32 more, see the JSON sidecar

Old text:

```
        parked = isinstance(exc, JobBlocked)
```

New text:

```
        parked = False
```

### `r290-author.D2_parked_marked_resumable`

Mark a parked job's envelope resumable, which sends a wrapper to crate run for work only the verb can continue

- File: `src/cratekit/cli/__init__.py`
- Source: `r290-author.json`, row `D2_parked_marked_resumable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_cutover_parity.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_job_outcome.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_approved.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_workers.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_pending_units.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_review_queue.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_install.py`, `tests/test_skills_lint.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`, `tests/test_write_session.py`
- Collected: 7247 against a baseline of 7247
- Kills: 2 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_park_on_a_gate_coded_cause_is_still_not_resumable_through_the_run`
  - `tests/test_job_outcome.py::test_the_dispatcher_reads_the_blocked_type_as_the_blocked_outcome`

Old text:

```
            resumable=resumable,
            outcome=outcome,
```

New text:

```
            resumable=resumable or parked,
            outcome=outcome,
```

### `r290-author.D4_cancelled_reads_failed`

Read the cancelled type as the failed outcome, which is what the dispatcher said before Outcome.CANCELLED had a producer

- File: `src/cratekit/cli/__init__.py`
- Source: `r290-author.json`, row `D4_cancelled_reads_failed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_cutover_parity.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_job_outcome.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_approved.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_workers.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_pending_units.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_review_queue.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_install.py`, `tests/test_skills_lint.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`, `tests/test_write_session.py`
- Collected: 7247 against a baseline of 7247
- Kills: 22 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_an_interrupted_restamp_names_its_job_command_and_that_command_finishes_it`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.bandcamp-fetch]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.download]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.fallback-fetch]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[adopt.scan]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[analyze.restamp]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[analyze.run]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[analyze.vocals]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[backup.run]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[export.playlist]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[intake.playlist]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[intake.set]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[label.import]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[label.judge]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[master]`
  - ... and 7 more, see the JSON sidecar

Old text:

```
            outcome = Outcome.CANCELLED
```

New text:

```
            outcome = Outcome.FAILED
```

### `u193.M16_continue_job_branch`

continue_command: never resume the job, so a rerun queues a second job

- File: `src/cratekit/cli/__init__.py`
- Source: `u193.json`, row `M16_continue_job_branch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 522 against a baseline of 522
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_the_continue_command_names_the_job_or_run_to_continue[a-job-resumes-that-job]`

Old text:

```
    if job_id:
        return shlex.join
```

New text:

```
    if False:
        return shlex.join
```

### `u193.M19_parked_outcome`

_dispatched_in_scope: a ceiling stop out of a plain verb reads failed, not blocked

- File: `src/cratekit/cli/__init__.py`
- Source: `u193.json`, row `M19_parked_outcome`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 522 against a baseline of 522
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_verb_at_its_line_is_blocked_and_the_call_past_it_is_not_sent[its-ceiling-names-the-exact-command-that-continues]`

Old text:

```
        parked = isinstance(exc, JobBlocked) or ceiling_stop
```

New text:

```
        parked = isinstance(exc, JobBlocked)
```

### `u193.M20_continue_step_not_written`

_dispatched_in_scope: leave the gate's generic step, so the exact command is never printed

- File: `src/cratekit/cli/__init__.py`
- Source: `u193.json`, row `M20_continue_step_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 522 against a baseline of 522
- Kills: 3 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_verb_at_its_line_is_blocked_and_the_call_past_it_is_not_sent[its-ceiling-names-the-exact-command-that-continues]`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_calls_already_given[joined]`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_calls_already_given[spaced]`

Old text:

```
        if ceiling_stop:
            cause = _with_continue(cause, argv, entry)
```

New text:

```
        if False:
            cause = _with_continue(cause, argv, entry)
```

### `u193.M21_swallowed_warning_dropped`

_dispatched: say nothing when a verb swallowed the stop

- File: `src/cratekit/cli/__init__.py`
- Source: `u193.json`, row `M21_swallowed_warning_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 522 against a baseline of 522
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_ceiling_stop_a_verb_swallowed_is_still_said`

Old text:

```
    if stopped is not None and not reported:
```

New text:

```
    if False:
```

### `u193.M22_warning_said_twice`

_dispatched: warn even over a blocked ceiling refusal, so the stop is said twice

- File: `src/cratekit/cli/__init__.py`
- Source: `u193.json`, row `M22_warning_said_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 522 against a baseline of 522
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_verb_at_its_line_is_blocked_and_the_call_past_it_is_not_sent[its-ceiling-names-the-exact-command-that-continues]`

Old text:

```
    if stopped is not None and not reported:
```

New text:

```
    if stopped is not None:
```

### `u193.M23_calls_floor`

_positive_calls: accept zero on the command line

- File: `src/cratekit/cli/__init__.py`
- Source: `u193.json`, row `M23_calls_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 522 against a baseline of 522
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_calls_that_is_not_a_positive_whole_number_is_a_usage_error[0]`

Old text:

```
    if value < 1:
        raise argparse.ArgumentTypeError
```

New text:

```
    if value < 0:
        raise argparse.ArgumentTypeError
```

### `u206.M23_lookup_line_dropped`

_with_isrc_lookups: never add the isrc-lookups line

- File: `src/cratekit/cli/__init__.py`
- Source: `u206.json`, row `M23_lookup_line_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1129 against a baseline of 1129
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_a_one_id_isrc_is_listed_and_two_ids_and_no_isrc_are_handed_on`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[cache-off]`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[kept]`

Old text:

```
    if remembered == 0 and asked == 0:
        return envelope
```

New text:

```
    if True:
        return envelope
```

### `u170.R10_moved_guard`

_retire_one: record on a gate that moved since the plan

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u170.json`, row `R10_moved_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1716 against a baseline of 1716
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_a_gate_answered_after_the_plan_was_read_is_said_and_not_answered_again`

Old text:

```
    if state.open_gate != one.gate:
```

New text:

```
    if False:
```

### `u170.R11_digest_ids_only`

retire: digest the planned run ids alone, not when each went idle

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u170.json`, row `R11_digest_ids_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1716 against a baseline of 1716
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_an_answer_is_stale_once_a_planned_run_is_resumed_even_if_it_stays_old`

Old text:

```
    plan = {"digest": digest_of(items), "count": len(items), "items": items}
```

New text:

```
    plan = {"digest": digest_of([one["run_id"] for one in items]), "count": len(items), "items": items}
```

### `u170.R12_default_week`

retire: default threshold fixed at seven days, not the file's

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u170.json`, row `R12_default_week`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1716 against a baseline of 1716
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_retire_reads_its_default_threshold_from_the_file`

Old text:

```
        age = timedelta(days=config.load().reports.open_gate_stale_days)
```

New text:

```
        age = timedelta(days=7)
```

### `u170.R1_zero_days`

older_than: accept 0d

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u170.json`, row `R1_zero_days`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1716 against a baseline of 1716
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_an_age_that_is_not_a_whole_number_of_days_is_a_usage_error[0d]`

Old text:

```
_AGE = re.compile(r"^([1-9][0-9]*)d$")
```

New text:

```
_AGE = re.compile(r"^([0-9]+)d$")
```

### `u170.R2_ceiling`

older_than: the ceiling one day higher

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u170.json`, row `R2_ceiling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1716 against a baseline of 1716
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_an_age_that_is_not_a_whole_number_of_days_is_a_usage_error[3651d]`

Old text:

```
    if not match or days > config.MAX_OPEN_GATE_STALE_DAYS:
```

New text:

```
    if not match or days > config.MAX_OPEN_GATE_STALE_DAYS + 1:
```

### `u170.R3_own_run`

old_gates: plan the asking run too

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u170.json`, row `R3_own_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1716 against a baseline of 1716
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_retire_never_retires_its_own_run`

Old text:

```
        if path.stem == skip:
```

New text:

```
        if False:
```

### `u170.R4_unreadable_dropped`

old_gates: drop an unreadable record without saying so

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u170.json`, row `R4_unreadable_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1716 against a baseline of 1716
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_a_record_retire_cannot_read_is_said_and_not_dropped`

Old text:

```
            unreadable.append(path.stem)
```

New text:

```
            pass
```

### `u170.R5_answers_apply`

_retire_one: record the gate's first option, apply, instead of abort

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u170.json`, row `R5_answers_apply`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1716 against a baseline of 1716
- Kills: 2 (killed)
- Killed:
  - `tests/test_run_retire.py::test_an_explicit_gate_is_retired_with_abort_and_never_apply`
  - `tests/test_run_retire.py::test_retire_asks_once_over_every_old_gate_and_answers_only_those`

Old text:

```
    gates.record(state, spec, gates.RETIRE_OPTION, actor=SESSION_ACTOR)
```

New text:

```
    gates.record(state, spec, spec.options[0], actor=SESSION_ACTOR)
```

### `u170.R6_actor_cli`

_retire_one: record the abort as cli instead of session

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u170.json`, row `R6_actor_cli`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1716 against a baseline of 1716
- Kills: 2 (killed)
- Killed:
  - `tests/test_run_retire.py::test_an_explicit_gate_is_retired_with_abort_and_never_apply`
  - `tests/test_run_retire.py::test_retire_asks_once_over_every_old_gate_and_answers_only_those`

Old text:

```
    gates.record(state, spec, gates.RETIRE_OPTION, actor=SESSION_ACTOR)
```

New text:

```
    gates.record(state, spec, gates.RETIRE_OPTION, actor=TERMINAL_ACTOR)
```

### `u170.R7_declined_applies`

retire: an abort on the confirm still retires

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u170.json`, row `R7_declined_applies`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1716 against a baseline of 1716
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_a_declined_retirement_answers_nothing`

Old text:

```
    if option != "apply":
```

New text:

```
    if False:
```

### `u170.R8_empty_asks`

retire: an empty plan is asked over instead of ending with no change

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u170.json`, row `R8_empty_asks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1716 against a baseline of 1716
- Kills: 2 (killed)
- Killed:
  - `tests/test_run_retire.py::test_retire_says_nothing_about_an_old_run_already_answered`
  - `tests/test_run_retire.py::test_retire_with_nothing_old_asks_nothing_and_changes_nothing`

Old text:

```
    if not planned:
```

New text:

```
    if False:
```

### `u170.R9_kept_planned`

retire: plan every old gate, the kept ones too

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u170.json`, row `R9_kept_planned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1716 against a baseline of 1716
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_retire_lists_what_it_retired_and_what_it_kept`

Old text:

```
    planned = [one for one in found if one.retirable]
```

New text:

```
    planned = list(found)
```

