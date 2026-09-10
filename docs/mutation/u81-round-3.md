# Mutation table: u81-round-3

Measured by `scripts/mutate.py` on 2026-09-10 22:40 UTC, branch `relay/81` at `0a49edb`. Pass kind: light.

Baseline: green, 7235 collected. pytest invocations for this batch: 6.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 7235 against 7235. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `B5_owed_default_dropped` | `scripts/board.py` | user | 1 file(s) | 77 | 2 | killed |
| `B5_audit_exit_code` | `scripts/board.py` | user | 1 file(s) | 77 | 1 | killed |
| `B5_audit_drops_the_detector` | `scripts/board.py` | user | 1 file(s) | 77 | 1 | killed |

## Row definitions

### `B5_owed_default_dropped`

Collapse the no-register default into a falsy test, so an empty register reads as none

- File: `scripts/board.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 77 against a baseline of 77
- Kills: 2 (killed)
- Killed:
  - `tests/test_pending_units.py::test_the_audit_reports_a_contradiction_as_exit_2_and_drift_as_exit_1`
  - `tests/test_pending_units.py::test_the_register_defaults_to_the_live_one_when_no_caller_supplies_it`

Old text:

```
    owed = owed_by_unit() if owed is None else owed
    issues_by_unit = units_by_issue_number(graph)
```

New text:

```
    owed = owed or {}
    issues_by_unit = units_by_issue_number(graph)
```

### `B5_audit_exit_code`

Report a contradiction as exit 1, the code that sends a session to sync

- File: `scripts/board.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 77 against a baseline of 77
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_the_audit_reports_a_contradiction_as_exit_2_and_drift_as_exit_1`

Old text:

```
    return 2 if clashes else 1
```

New text:

```
    return 1
```

### `B5_audit_drops_the_detector`

Have the audit find no contradictions at all, keeping its drift report

- File: `scripts/board.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 77 against a baseline of 77
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_the_audit_reports_a_contradiction_as_exit_2_and_drift_as_exit_1`

Old text:

```
    clashes = contradictions(graph)
```

New text:

```
    clashes = []
```

