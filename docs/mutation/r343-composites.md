# Mutation table: r343-composites

Measured by `scripts/mutate.py` on 2026-09-22 22:21 UTC, branch `unit/issue190-a-mutation-driver-run-wrote-343-files-in` at `4d2e028`. Pass kind: light.

Baseline: green, 9986 collected. pytest invocations for this batch: 7.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/Library/Application Support/cratekit (930 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 9986 against 9986. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `C1_no_timestamps` | `scripts/mutate.py` | user | 1 file(s) | 9986 | 0 (promoted) | zero |
| `C2_no_timestamps_no_hash` | `scripts/mutate.py` | user | 1 file(s) | 61 | 1 | killed |
| `C3_path_only` | `scripts/mutate.py` | user | 1 file(s) | 61 | 1 | killed |

## Zero rows and what they owe

- `C1_no_timestamps` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `C1_no_timestamps`

composite for G2 in r343.md: drop mtime and ctime together; the content hash is what is left to carry a same size rewrite

- File: `scripts/mutate.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 9986 against a baseline of 9986
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                f"\t{info.st_mtime_ns}\t{info.st_ctime_ns}"
```

New text:

```
                ""
```

### `C2_no_timestamps_no_hash`

composite for G8 in r343.md: drop mtime, ctime and the content hash together, leaving path, size and inode; a same size rewrite must now pass unseen, so the test that rewrites in place is the death

- File: `scripts/mutate.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_same_size_rewrite_of_a_small_file_is_a_leak`

Old text:

```
                f"\t{info.st_mtime_ns}\t{info.st_ctime_ns}"
            )
            if info.st_size <= SMALL_FILE_BYTES and not os.path.islink(path):
```

New text:

```
                ""
            )
            if False:
```

### `C3_path_only`

composite for G3 in r343.md: drop size, inode, timestamps and the hash, leaving the path alone; only a new or removed entry is seen

- File: `scripts/mutate.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_same_size_rewrite_of_a_small_file_is_a_leak`

Old text:

```
                f"{relative}\t{info.st_size}\t{info.st_ino}"
                f"\t{info.st_mtime_ns}\t{info.st_ctime_ns}"
            )
            if info.st_size <= SMALL_FILE_BYTES and not os.path.islink(path):
```

New text:

```
                f"{relative}"
            )
            if False:
```

