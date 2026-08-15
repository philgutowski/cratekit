# Mutation table: u27-r80-write-probe-replacement

Measured by `scripts/mutate.py` on 2026-08-15 12:44 UTC, branch `unit/u27-setup-wizard-and-doctor` at `4a34a84`. Pass kind: light.

Baseline: green, 3449 collected. pytest invocations for this batch: 14.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 3449 against 3449. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `W1_permission_branch` | `src/cratekit/core/cause.py` | user | 11 file(s) | 1268 | 1 | killed |
| `W2_immutable_branch` | `src/cratekit/core/cause.py` | user | 11 file(s) | 1268 | 1 | killed |
| `W3_read_only_branch` | `src/cratekit/core/cause.py` | user | 11 file(s) | 3449 | 0 (promoted) | zero |
| `W4_order_access_first` | `src/cratekit/core/cause.py` | maintainer | 11 file(s) | 1268 | 1 | killed |
| `W5_read_delegation` | `src/cratekit/core/cause.py` | user | 11 file(s) | 3449 | 0 (promoted) | zero |
| `W6_effective_ids` | `src/cratekit/core/cause.py` | maintainer | 11 file(s) | 3449 | 0 (promoted) | zero |
| `W7_swallow_guard` | `src/cratekit/core/cause.py` | maintainer | 11 file(s) | 1268 | 1 | killed |
| `W8_read_probe_flags` | `src/cratekit/core/cause.py` | user | 11 file(s) | 1268 | 1 | killed |

## Zero rows and what they owe

- `W3_read_only_branch` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `W5_read_delegation` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `W6_effective_ids` (maintainer facing): maintainer facing, composite not required

## Considered and dropped

METHOD caps a light pass at 25 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `W9_statvfs_on_parent`: Read ST_RDONLY off the parent directory rather than the path Dropped because: ranked below the cap: same branch as W3 and W4, which are both measured, and the two answer the same on every arrangement driven because a file and its parent are on one volume
- `W10_close_the_read_handle`: Leak the read probe's descriptor by dropping os.close Dropped because: ranked below the cap: not this round's diff, and a descriptor leak is a maintainer facing cost with no classification change

## Row definitions

### `W1_permission_branch`

Drop the os.access branch, so a mode or ACL refusal is not attributed

- File: `src/cratekit/core/cause.py`
- Surface: user
- Subset: test files importing cratekit.core.cause
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_review_queue.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 1268 against a baseline of 1268
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_write_probe_classifies_every_way_a_write_is_refused`

Old text:

```
        if not os.access(path, os.W_OK, effective_ids=effective):
            return AccessRefusal(kind=AccessKind.PERMISSION, path=path)

```

New text:

```
(empty)
```

### `W2_immutable_branch`

Drop the immutable branch, so a Finder Locked file reports permission

- File: `src/cratekit/core/cause.py`
- Surface: user
- Subset: test files importing cratekit.core.cause
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_review_queue.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 1268 against a baseline of 1268
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_write_probe_classifies_every_way_a_write_is_refused`

Old text:

```
        if _immutable(path):
            return AccessRefusal(kind=AccessKind.LOCKED, path=path)

```

New text:

```
(empty)
```

### `W3_read_only_branch`

Drop the ST_RDONLY branch, so a read only volume reports permission

- File: `src/cratekit/core/cause.py`
- Surface: user
- Subset: test files importing cratekit.core.cause
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_review_queue.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 3449 against a baseline of 3449
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if os.statvfs(path).f_flag & os.ST_RDONLY:
            return AccessRefusal(kind=AccessKind.READ_ONLY, path=path)

```

New text:

```
(empty)
```

### `W4_order_access_first`

Ask os.access before ST_RDONLY, so a read only volume reads as a permission

- File: `src/cratekit/core/cause.py`
- Surface: maintainer
- Subset: test files importing cratekit.core.cause
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_review_queue.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 1268 against a baseline of 1268
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_write_probe_classifies_every_way_a_write_is_refused`

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

### `W5_read_delegation`

Drop the read probe delegation, so a file this account cannot read is misattributed

- File: `src/cratekit/core/cause.py`
- Surface: user
- Subset: test files importing cratekit.core.cause
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_review_queue.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 3449 against a baseline of 3449
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

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

### `W6_effective_ids`

Ask os.access for the real identity rather than the effective one

- File: `src/cratekit/core/cause.py`
- Surface: maintainer
- Subset: test files importing cratekit.core.cause
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_review_queue.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 3449 against a baseline of 3449
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    effective = os.access in os.supports_effective_ids
```

New text:

```
    effective = False
```

### `W7_swallow_guard`

Narrow the guard to OSError, dropping the ValueError an unrepresentable path raises

- File: `src/cratekit/core/cause.py`
- Surface: maintainer
- Subset: test files importing cratekit.core.cause
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_review_queue.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 1268 against a baseline of 1268
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_path_no_filesystem_can_represent_is_answered_rather_than_raised`

Old text:

```
    except (OSError, ValueError):
        # The same two guards :func:`_probe_readable` gives, for the same reason:
```

New text:

```
    except OSError:
        # The same two guards :func:`_probe_readable` gives, for the same reason:
```

### `W8_read_probe_flags`

Make the read probe write capable, the shape the reports allowlist forbids

- File: `src/cratekit/core/cause.py`
- Surface: user
- Subset: test files importing cratekit.core.cause
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_review_queue.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 1268 against a baseline of 1268
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_write_probe_classifies_every_way_a_write_is_refused`

Old text:

```
        handle = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
```

New text:

```
        handle = os.open(path, os.O_RDWR | os.O_NONBLOCK)
```

