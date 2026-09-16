# Mutation table: r83-round-2

Measured by `scripts/mutate.py` on 2026-09-16 21:44 UTC, branch `relay/83` at `b68685a`. Pass kind: light.

Baseline: green, 7544 collected. pytest invocations for this batch: 6.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 7544 against 7544. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `I1_fold_case` | `src/cratekit/core/preflight.py` | user | 15 file(s) | 1897 | 3 | killed |
| `I3_configured_compare_exact` | `src/cratekit/core/preflight.py` | user | 15 file(s) | 1897 | 2 | killed |
| `I4_elsewhere_compare_exact` | `src/cratekit/core/preflight.py` | user | 15 file(s) | 1897 | 1 | killed |

## Row definitions

### `I1_fold_case`

R-344, after fix round 1: normalize_identity strips but no longer folds the case

- File: `src/cratekit/core/preflight.py`
- Surface: user
- Subset: test files importing cratekit.core.preflight
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_metadata_cli.py`, `tests/test_preflight.py`, `tests/test_rebuild.py`, `tests/test_reserved_causes.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 1897 against a baseline of 1897
- Kills: 3 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_identity_typed_as_diskutil_prints_it_passes_the_mount_check`
  - `tests/test_preflight.py::test_an_identity_in_another_case_is_still_found_where_it_is_mounted`
  - `tests/test_preflight.py::test_an_identity_recorded_in_uppercase_matches_the_lowercase_the_kernel_reports`

Old text:

```
    return identity.strip().lower()
```

New text:

```
    return identity.strip()
```

### `I3_configured_compare_exact`

R-344, after fix round 1: the configured mount's compare goes back to exact equality

- File: `src/cratekit/core/preflight.py`
- Surface: user
- Subset: test files importing cratekit.core.preflight
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_metadata_cli.py`, `tests/test_preflight.py`, `tests/test_rebuild.py`, `tests/test_reserved_causes.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 1897 against a baseline of 1897
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_identity_typed_as_diskutil_prints_it_passes_the_mount_check`
  - `tests/test_preflight.py::test_an_identity_recorded_in_uppercase_matches_the_lowercase_the_kernel_reports`

Old text:

```
    if same_identity(recorded_identity, observed):
```

New text:

```
    if observed == recorded_identity:
```

### `I4_elsewhere_compare_exact`

R-344, after fix round 1: the mounted elsewhere sweep's compare goes back to exact equality, the round 1 zero

- File: `src/cratekit/core/preflight.py`
- Surface: user
- Subset: test files importing cratekit.core.preflight
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_metadata_cli.py`, `tests/test_preflight.py`, `tests/test_rebuild.py`, `tests/test_reserved_causes.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 1897 against a baseline of 1897
- Kills: 1 (killed)
- Killed:
  - `tests/test_preflight.py::test_an_identity_in_another_case_is_still_found_where_it_is_mounted`

Old text:

```
        if found is not None and same_identity(recorded_identity, found):
```

New text:

```
        if found == recorded_identity:
```

