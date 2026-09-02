# Mutation table: u50-zero-rows

Measured by `scripts/mutate.py` on 2026-09-02 11:11 UTC, branch `relay/68` at `7789522`. Pass kind: light.

Baseline: green, 6579 collected. pytest invocations for this batch: 6.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6579 against 6579. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `B2_items_hardcoded_pair` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `W4b_item_ignored_entirely` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 46 | 4 | killed |
| `W8_read_back_inside_the_item` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 46 | 1 | killed |

## Row definitions

### `B2_items_hardcoded_pair`

Name the two portions instead of deriving them, so a third portion is queued by nobody

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_item_list_is_derived_from_the_portions_rather_than_written_out`

Old text:

```
    return tuple(str(portion) for portion in backup_facts.Portion)
```

New text:

```
    return ("files", "database")
```

### `W4b_item_ignored_entirely`

Back up the mirror whatever the item says, so every item of the job does the same half

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 46 against a baseline of 46
- Kills: 4 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_queued_backup_runs_every_portion_through_the_real_resume`
  - `tests/test_backup_cli.py::test_an_item_naming_something_that_is_not_a_portion_refuses_by_name`
  - `tests/test_backup_cli.py::test_the_age_a_driven_run_publishes_is_the_engine_s_and_reaches_the_envelope`

Old text:

```
    named = str(item.item_id or "")
```

New text:

```
    named = str(backup_facts.Portion.FILES)
```

### `W8_read_back_inside_the_item`

Read the age back under the driver, so an unreadable fact file fails an item over a rehearsal that copied nothing

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_handler_does_not_fail_an_item_over_the_age_read_back`

Old text:

```
        read_back=False,
    )
    return None
```

New text:

```
    )
    return None
```

