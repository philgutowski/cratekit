# Mutation table: u44-author-round-2

Measured by `scripts/mutate.py` on 2026-08-27 15:56 UTC, branch `relay/62` at `f6ef7a1`. Pass kind: light.

Baseline: green, 6383 collected. pytest invocations for this batch: 6.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6383 against 6383. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `A1_archive_verify_dropped` | `src/cratekit/modules/tools/mastering.py` | user | 2 file(s) | 151 | 1 | killed |
| `A4_digest_reads_first_chunk_only` | `src/cratekit/modules/tools/mastering.py` | user | 2 file(s) | 151 | 1 | killed |
| `B3_concat_output_unread` | `src/cratekit/modules/tools/mastering.py` | user | 2 file(s) | 151 | 1 | killed |

## Row definitions

### `A1_archive_verify_dropped`

Drop the post-copy digest verification, so a corrupt archive is reported safe

- File: `src/cratekit/modules/tools/mastering.py`
- Surface: user
- Subset: test files importing cratekit.modules.tools.mastering
- Ran: `tests/modules/test_tools.py`, `tests/test_master_cli.py`
- Collected: 151 against a baseline of 151
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_corrupt_archive_copy_refuses_and_leaves_no_false_safety_copy`

Old text:

```
    shutil.copy2(source, destination)
    if digest(destination) != source_digest:
```

New text:

```
    shutil.copy2(source, destination)
    if False:
```

### `A4_digest_reads_first_chunk_only`

Digest only the first chunk, so two sets differing later in the file hash identically

- File: `src/cratekit/modules/tools/mastering.py`
- Surface: user
- Subset: test files importing cratekit.modules.tools.mastering
- Ran: `tests/modules/test_tools.py`, `tests/test_master_cli.py`
- Collected: 151 against a baseline of 151
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_an_impostor_matching_the_first_chunk_is_still_a_different_recording`

Old text:

```
        while True:
            block = handle.read(chunk)
            if not block:
                break
            hasher.update(block)
```

New text:

```
        hasher.update(handle.read(chunk))
```

### `B3_concat_output_unread`

Drop the same check from the join, one function over

- File: `src/cratekit/modules/tools/mastering.py`
- Surface: user
- Subset: test files importing cratekit.modules.tools.mastering
- Ran: `tests/modules/test_tools.py`, `tests/test_master_cli.py`
- Collected: 151 against a baseline of 151
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_join_that_exits_zero_and_writes_nothing_refuses_rather_than_returning`

Old text:

```
    _wrote_or_refuse(destination, "join")
    return destination
```

New text:

```
    return destination
```

