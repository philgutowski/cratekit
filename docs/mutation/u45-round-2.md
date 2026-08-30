# Mutation table: u45-round-2

Measured by `scripts/mutate.py` on 2026-08-30 03:07 UTC, branch `unit/u45-the-backup-run-shell-and-the-age-the-wri` at `2548aca`. Pass kind: full.

Baseline: green, 6441 collected. pytest invocations for this batch: 8.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6441 against 6441. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `C7_failed_detail_dropped` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 25 | 1 | killed |
| `A3_age_seconds_always_none` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 25 | 1 | killed |
| `H3_resume_branch_dropped` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 25 | 1 | killed |
| `E5_outcome_ok_widened` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 412 | 1 | killed |

## Row definitions

### `C7_failed_detail_dropped`

Reword the transfer-failed message so it no longer says a destructive session still sees the previous age

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_transfer_failure_says_no_age_was_published`

Old text:

```
            + ". No backup age was published for that portion, so a destructive "
            "session still sees whatever the last successful run left",
```

New text:

```
            + ". The run stopped there.",
```

### `A3_age_seconds_always_none`

Report no age number even for a known portion, so the value R15's warning quotes never reaches the report

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_report_carries_the_age_number_and_not_only_the_state`

Old text:

```
            "age_seconds": entry.age.total_seconds() if entry.age is not None else None,
```

New text:

```
            "age_seconds": None,
```

### `H3_resume_branch_dropped`

Always enqueue, so --job files a second backup rather than reporting the one already queued

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_resume_reports_the_queued_job_rather_than_filing_a_second`

Old text:

```
        if ctx.args.job:
            return ctx.envelope(data=_reported(store, jobs.reconcile(store, ctx.args.job)))
```

New text:

```
        if False:
            return ctx.envelope(data=_reported(store, jobs.reconcile(store, ctx.args.job)))
```

### `E5_outcome_ok_widened`

Answer ok when ANY portion is fine rather than all of them

- File: `src/cratekit/modules/tools/backup.py`
- Surface: user
- Subset: test files importing cratekit.modules.tools.backup
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 412 against a baseline of 412
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_outcome_answers_not_ok_when_a_portion_failed`

Old text:

```
        return all(p.refusal is not None or p.ran for p in self.portions)
```

New text:

```
        return any(p.refusal is not None or p.ran for p in self.portions)
```

