# Mutation table: u27-r80-write-probe-zero-rows-repinned

Measured by `scripts/mutate.py` on 2026-08-15 13:02 UTC, branch `unit/u27-setup-wizard-and-doctor` at `3f4a1d5`. Pass kind: light.

Baseline: green, 3452 collected. pytest invocations for this batch: 7.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 3452 against 3452. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `W3_read_only_branch` | `src/cratekit/core/cause.py` | user | 11 file(s) | 1271 | 2 | killed |
| `W5_read_delegation` | `src/cratekit/core/cause.py` | user | 11 file(s) | 1271 | 1 | killed |
| `W4b_order_access_before_statvfs` | `src/cratekit/core/cause.py` | user | 11 file(s) | 1271 | 3 | killed |
| `W11_route_path_attribute` | `src/cratekit/core/cause.py` | user | 11 file(s) | 1271 | 1 | killed |

## Row definitions

### `W3_read_only_branch`

Drop the ST_RDONLY branch, so a read only volume reports permission. Was zero before the pin

- File: `src/cratekit/core/cause.py`
- Surface: user
- Subset: test files importing cratekit.core.cause
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_review_queue.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 1271 against a baseline of 1271
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_driver_path_to_the_write_probe_is_driven_on_a_real_read_only_volume`
  - `tests/test_doctor.py::test_the_write_probe_names_the_medium_rather_than_the_account`

Old text:

```
        if os.statvfs(path).f_flag & os.ST_RDONLY:
            return AccessRefusal(kind=AccessKind.READ_ONLY, path=path)

```

New text:

```
(empty)
```

### `W5_read_delegation`

Drop the read probe delegation, so an unreachable path answers silence. Was zero before the pin

- File: `src/cratekit/core/cause.py`
- Surface: user
- Subset: test files importing cratekit.core.cause
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_review_queue.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 1271 against a baseline of 1271
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_write_probe_answers_for_a_path_it_cannot_reach_at_all`

Old text:

```
    refused = _probe_readable(path)
    if refused is not None:
        return refused

```

New text:

```
(empty)
```

### `W4b_order_access_before_statvfs`

Ask os.access first, which is the tidy up that reintroduces W3's defect with the branch still present

- File: `src/cratekit/core/cause.py`
- Surface: user
- Subset: test files importing cratekit.core.cause
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_review_queue.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 1271 against a baseline of 1271
- Kills: 3 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_driver_path_to_the_write_probe_is_driven_on_a_real_read_only_volume`
  - `tests/test_doctor.py::test_the_write_probe_classifies_every_way_a_write_is_refused`
  - `tests/test_doctor.py::test_the_write_probe_names_the_medium_rather_than_the_account`

Old text:

```
        if os.statvfs(path).f_flag & os.ST_RDONLY:
            return AccessRefusal(kind=AccessKind.READ_ONLY, path=path)
        if _immutable(path):
            return AccessRefusal(kind=AccessKind.LOCKED, path=path)
        if not os.access(path, os.W_OK, effective_ids=effective):
            return AccessRefusal(kind=AccessKind.PERMISSION, path=path)

```

New text:

```
        if not os.access(path, os.W_OK, effective_ids=effective):
            return AccessRefusal(kind=AccessKind.PERMISSION, path=path)
        if os.statvfs(path).f_flag & os.ST_RDONLY:
            return AccessRefusal(kind=AccessKind.READ_ONLY, path=path)
        if _immutable(path):
            return AccessRefusal(kind=AccessKind.LOCKED, path=path)

```

### `W11_route_path_attribute`

Drop the path attribute the connection site attaches, so the driver route classifies nothing

- File: `src/cratekit/core/cause.py`
- Surface: user
- Subset: test files importing cratekit.core.cause
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_review_queue.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 1271 against a baseline of 1271
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_driver_path_to_the_write_probe_is_driven_on_a_real_read_only_volume`

Old text:

```
    if name.startswith("SQLITE_CANTOPEN"):
        return _probe_readable(str(path))
    return _probe_writable(str(path))
```

New text:

```
    if name.startswith("SQLITE_CANTOPEN"):
        return _probe_readable(str(path))
    return None
```

