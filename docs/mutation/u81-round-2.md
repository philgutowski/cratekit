# Mutation table: u81-round-2

Measured by `scripts/mutate.py` on 2026-09-10 22:15 UTC, branch `relay/81` at `0bb1064`. Pass kind: light.

Baseline: green, 7233 collected. pytest invocations for this batch: 4.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 7233 against 7233. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `B5_owed_argument_ignored` | `scripts/board.py` | user | 1 file(s) | 75 | 1 | killed |

## Row definitions

### `B5_owed_argument_ignored`

Ignore a supplied register and always read the live one

- File: `scripts/board.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 75 against a baseline of 75
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_closed_unit_a_register_still_owes_is_the_contradiction_the_audit_exits_2_on`

Old text:

```
    owed = owed_by_unit() if owed is None else owed
    issues_by_unit = units_by_issue_number(graph)
```

New text:

```
    owed = owed_by_unit()
    issues_by_unit = units_by_issue_number(graph)
```

