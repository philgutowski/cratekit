# Mutation table: u23-round-8-independent-hunt

Measured by `scripts/mutate.py` on 2026-08-14 14:29 UTC, branch `unit/u23-library-adoption` at `83ae047`. Pass kind: full.

Baseline: green, 3801 collected. pytest invocations for this batch: 4.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 3801 against 3801. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `HUNT_a_container_leaves_the_writers_table` | `src/cratekit/core/tags.py` | user | 2 file(s) | 615 | collection error | collect-error |

## Row definitions

### `HUNT_a_container_leaves_the_writers_table`

Drop .aifc from AIFF_SUFFIXES, so it leaves tags._DIALECT_BY_SUFFIX and LEDGER_CONTAINERS with it

- File: `src/cratekit/core/tags.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`, `tests/test_tags.py`
- Collected: 615 against a baseline of 653
- Kills: 1 (collect-error)
- Note: collection changed: 615 collected against a baseline of 653. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_tags.py::test_each_container_is_classified_once[.aifc-Dialect.ID3]`

Old text:

```
AIFF_SUFFIXES = (".aiff", ".aif", ".aifc")
```

New text:

```
AIFF_SUFFIXES = (".aiff", ".aif")
```

