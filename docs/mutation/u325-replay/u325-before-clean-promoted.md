# Mutation table: u325-before-clean-promoted

Measured by `scripts/mutate.py` on 2026-11-23 04:31 UTC, branch `HEAD` at `539638eb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22663 collected. pytest invocations for this batch: 20.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-23 04:31 UTC for commit `539638ebe629`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 5, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22663 against 22663. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r349-b.B3_clear_before_attempt` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 22663 | 0 (promoted) | zero |
| `r349-b.B4_stage_error_completes` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 22663 | 0 (promoted) | zero |
| `r349-c.C2_write_failure_step` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 22663 | 0 (promoted) | zero |
| `r757-c1.S3_work_body_plans_fast` | `src/cratekit/backup/cli.py` | user | 4 file(s) | 22663 | 0 (promoted) | zero |
| `r746-a.G7_sql_value_check_disarmed` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 22663 | 0 (promoted) | zero |
| `r746-d.G5_content_row_read_back_against_five_not_ten` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 22663 | 0 (promoted) | zero |
| `u263.D20_energy_load` | `src/cratekit/analysis/energy.py` | user | 3 file(s) | 22663 | 0 (promoted) | zero |

## Zero rows and what they owe

- `r349-b.B3_clear_before_attempt` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r349-b.B4_stage_error_completes` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r349-c.C2_write_failure_step` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r757-c1.S3_work_body_plans_fast` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r746-a.G7_sql_value_check_disarmed` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r746-d.G5_content_row_read_back_against_five_not_ten` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u263.D20_energy_load` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `r349-b.B3_clear_before_attempt`

The handler no longer clears the previous attempt's record

- File: `src/cratekit/backup/cli.py`
- Source: `r349-b.json`, row `B3_clear_before_attempt`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    backup_facts.clear_outcome(job.job_id, named)
    report = perform_backup(
```

New text:

```
    report = perform_backup(
```

### `r349-b.B4_stage_error_completes`

A staging write error escapes the handler instead of completing the item

- File: `src/cratekit/backup/cli.py`
- Source: `r349-b.json`, row `B4_stage_error_completes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    except OSError:
        return None
    return jobs.Produced
```

New text:

```
    except KeyError:
        return None
    return jobs.Produced
```

### `r349-c.C2_write_failure_step`

A failed record write returns the refusal without the step saying the record is missing

- File: `src/cratekit/backup/cli.py`
- Source: `r349-c.json`, row `C2_write_failure_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    except OSError as exc:
        cause = refusal.cause
```

New text:

```
    except OSError as exc:
        return refusal
        cause = refusal.cause
```

### `r757-c1.S3_work_body_plans_fast`

perform_backup: plan in the fast mode whatever the payload froze

- File: `src/cratekit/backup/cli.py`
- Source: `r757-c1.json`, row `S3_work_body_plans_fast`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            full=bool(payload.get(FULL)),
```

New text:

```
            full=False,
```

### `r746-a.G7_sql_value_check_disarmed`

assert_created_rows_are_gridless: a value read from SQL is never a violation

- File: `src/cratekit/core/rb_writer.py`
- Source: `r746-a.json`, row `G7_sql_value_check_disarmed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_write_guard_completeness.py`, `tests/test_rb_writer_db.py`
- Collected: 22663 against a baseline of 22663
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
- Collected: 22663 against a baseline of 22663
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

### `u263.D20_energy_load`

energy.features_from_path: decode through librosa.load again, so an M4A is unmeasured

- File: `src/cratekit/analysis/energy.py`
- Source: `u263.json`, row `D20_energy_load`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`, `tests/test_analysis_workers.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        samples, decoded_rate = decode.load(
            path, MEASURE_RATE, offset=offset, duration=SEGMENT_SECONDS
        )
```

New text:

```
        samples, decoded_rate = __import__("librosa").load(
            str(path), sr=MEASURE_RATE, mono=True, offset=offset, duration=SEGMENT_SECONDS
        )
```

