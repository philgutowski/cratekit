# Mutation table: u42-author-round-2

Measured by `scripts/mutate.py` on 2026-08-29 02:01 UTC, branch `unit/u42-the-two-acquire-command-line-shells-rows` at `bf2b8a9`. Pass kind: light.

Baseline: green, 6414 collected. pytest invocations for this batch: 6.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6414 against 6414. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `C2_unknown_defaults_lossless` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 1 | killed |
| `R2_handler_lookup_imports` | `src/cratekit/cli/registry.py` | user | 1 file(s) | 540 | 1 | killed |

## Row definitions

### `C2_unknown_defaults_lossless`

Classify an unrecognised suffix as lossless instead of 'other'

- File: `src/cratekit/acquire/cli.py`
- Surface: user
- Subset: test files importing cratekit.acquire.cli
- Ran: `tests/test_acquire_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_non_audio_files_are_not_reported`

Old text:

```
    return "other"
```

New text:

```
    return "lossless"
```

### `R2_handler_lookup_imports`

Make by_handler_key import the module, which is what the rewritten guard forbids

- File: `src/cratekit/cli/registry.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 540 against a baseline of 540
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_handler_key_resolves_without_importing_the_module`

Old text:

```
def by_handler_key(key: str) -> Entry:
```

New text:

```
def by_handler_key(key: str) -> Entry:
    import importlib

    importlib.import_module("cratekit.acquire.cli")
```

