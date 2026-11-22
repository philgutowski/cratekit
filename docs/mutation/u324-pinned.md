# Mutation table: u324-pinned

Measured by `scripts/mutate.py` on 2026-11-22 00:10 UTC, branch `cloud/919-folded-makers` at `a0d6d1b2`. Pass kind: light.

Baseline: green, 22794 collected. pytest invocations for this batch: 3.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 00:10 UTC for commit `a0d6d1b20f8e`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 1, each measured by this driver.

Known failures: 249 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22794 against 22794. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `F20_initial_prefix_dropped_pinned` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1721 | 2 | killed |

## Row definitions

### `F20_initial_prefix_dropped_pinned`

_runs_in: an initial stands for any word, not only one it opens

- File: `src/cratekit/tagging/titles.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1721 against a baseline of 1721
- Kills: 2 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_a_folded_name_is_no_wider_than_its_letters[Bernard Badie-08A - 124 - C. Badie - Sun Path-Sun Path]`
  - `tests/test_title_matcher.py::test_a_folded_name_is_no_wider_than_its_letters[\xde\xf3r\xf0ur Badie-08A - 124 - \xc6. Badie - Sun Path-Sun Path]`

Old text:

```
        return mine == theirs or (initial(index) and theirs.startswith(mine))
```

New text:

```
        return mine == theirs or initial(index)
```

