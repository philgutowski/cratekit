# Mutation table: u133-a-rerun

Measured by `scripts/mutate.py` on 2026-10-13 01:08 UTC, branch `fable/308-jazz-genre-folder-under` at `a5bd3098`. Pass kind: light.

Baseline: green, 13744 collected. pytest invocations for this batch: 5.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/Library/Application Support/cratekit (408200 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 13744 against 13744. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `P5_vocabulary_owner` | `src/cratekit/core/taxonomy_upgrade.py` | user | 1 file(s) | 46 | 1 | killed |
| `P8_held_by_whole_copy` | `src/cratekit/core/taxonomy_upgrade.py` | user | 1 file(s) | 46 | 2 | killed |

## Row definitions

### `P5_vocabulary_owner`

A vocabulary row is named by its tag alone, whichever bucket files that tag

- File: `src/cratekit/core/taxonomy_upgrade.py`
- Surface: user
- Subset: test files importing cratekit.core.taxonomy_upgrade
- Ran: `tests/test_taxonomy_upgrade.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_a_vocabulary_row_whose_tag_files_where_the_template_shares_the_word_is_not_named`

Old text:

```
            if (row.bucket, row.tag.casefold().strip()) in clashing:

```

New text:

```
            if row.tag.casefold().strip() in {word for _owner, word in clashing}:

```

### `P8_held_by_whole_copy`

Only the copy's first bucket filing a word is asked about, as the setdefault before U133 did across buckets

- File: `src/cratekit/core/taxonomy_upgrade.py`
- Surface: user
- Subset: test files importing cratekit.core.taxonomy_upgrade
- Ran: `tests/test_taxonomy_upgrade.py`
- Collected: 46 against a baseline of 46
- Kills: 2 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_a_vocabulary_row_whose_tag_files_where_the_template_shares_the_word_is_not_named`
  - `tests/test_taxonomy_upgrade.py::test_every_bucket_of_the_copy_filing_a_word_is_named_not_the_first`

Old text:

```
            filed.setdefault(word, []).extend((bucket.id, s, w) for s, w in places)

```

New text:

```
            filed.setdefault(word, list((bucket.id, s, w) for s, w in places))

```

