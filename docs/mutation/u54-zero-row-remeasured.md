# Mutation table: u54-zero-row-remeasured

Measured by `scripts/mutate.py` on 2026-09-09 11:56 UTC, branch `u54/finish` at `9bfd275`. Pass kind: light.

Baseline: green, 6991 collected. pytest invocations for this batch: 4.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6991 against 6991. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `G7_staging_cleared` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 64 | 1 | killed |

## Row definitions

### `G7_staging_cleared`

Keep whatever a killed attempt left in the item's staging directory, re-measured after the fake was taught to skip

- File: `src/cratekit/acquire/cli.py`
- Surface: user
- Subset: test files importing cratekit.acquire.cli
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_partial_file_left_in_staging_does_not_poison_the_next_attempt`

Old text:

```
    if directory.exists():
        shutil.rmtree(directory)

```

New text:

```
(empty)
```

