# Mutation table: u50-review-fixes

Measured by `scripts/mutate.py` on 2026-09-02 11:59 UTC, branch `relay/68` at `854e3ca`. Pass kind: light.

Baseline: green, 6583 collected. pytest invocations for this batch: 8.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6583 against 6583. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `R1_reraise_back_inside_is_open` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 50 | 2 | killed |
| `R2_empty_job_guard_dropped` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 50 | 1 | killed |
| `R3_fact_file_failure_untranslated` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 50 | 1 | killed |
| `R4_ages_from_the_live_config` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 6583 | 0 (promoted) | zero |

## Zero rows and what they owe

- `R4_ages_from_the_live_config` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `R1_reraise_back_inside_is_open`

Put the failed job re-raise back inside the is_open branch, which is the placement three reviewers found wrong

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 50 against a baseline of 50
- Kills: 2 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_asking_twice_about_a_half_failed_backup_answers_the_same_way_twice`

Old text:

```
            if not job.is_open() and job.cause is not None:
                raise CratekitError(job.cause)
```

New text:

```
(empty)
```

### `R2_empty_job_guard_dropped`

Drive a job with no items, so a job queued by the previous build reports SUCCEEDED over a library nothing copied

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_job_queued_before_the_worker_existed_refuses_rather_than_succeeding`

Old text:

```
                _refuse_an_empty_job(store, job)
```

New text:

```
(empty)
```

### `R3_fact_file_failure_untranslated`

Let BackupFactsUnreadable escape the work body, so the driver records report-defect over a repairable file

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_an_unwritable_fact_file_says_which_file_rather_than_report_defect`

Old text:

```
        raise refuse(
            "backup-facts-unreadable",
            f"the {portion or 'backup'} portion transferred and the age it "
            f"publishes cannot be written: {exc}. The copy exists; the fact a "
            f"destructive session reads does not",
            remedy=Remedy(str(exc.remedy)),
            origin=("backup", "cli"),
            detail={"path": str(exc.path), "library": str(cfg.library.root)},
        ) from exc
```

New text:

```
        raise
```

### `R4_ages_from_the_live_config`

Read the ages back from the live configuration rather than the one the job was frozen against

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 6583 against a baseline of 6583
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            reported["ages"] = published_ages(jobs.frozen_config(job))
```

New text:

```
            reported["ages"] = published_ages(cfg)
```


## The zero row, and what it was

`R4_ages_from_the_live_config` killed nothing on this pass, and the cause was the
test rather than the fix. It is recorded here in full because the mechanism cost
two wrong drafts to find.

`test_the_ages_reported_are_the_ones_this_job_published` moved the library in the
saved configuration file and asserted the envelope still reported this job's ages.
It could not fail. The `cfg` fixture sets `CRATEKIT_LIBRARY_ROOT`, and
`config.from_dict` relocates a configured root onto whatever that variable says, so
both readings stayed on the original library and the mutation changed nothing
observable.

The second draft moved the environment variable as well, which is worse, and the
reason is the part worth keeping: `jobs.frozen_config` rebuilds through that same
`config.from_dict`. So the override relocates a FROZEN configuration's library root
exactly as it relocates a live one, and the two agree again. What a frozen
configuration is frozen against is the configuration FILE changing, not an explicit
environment override, and nothing in this repository said so before now.

The third draft unsets the variable and changes the file, which is the only shape
where the two readings differ. Re-measured by hand against the same mutation on
2026-09-02: the row now kills
`test_the_ages_reported_are_the_ones_this_job_published`, failing with `the files
age read back as never-recorded`, and the tree was restored from `git show HEAD`
afterwards.
