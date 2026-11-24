# Mutation table: u343-composite

Measured by `scripts/mutate.py` on 2026-11-24 00:18 UTC, branch `cloud/995-analyze-run-stops-measuring-key` at `d85c1494`. Pass kind: light.

Baseline: green, 23086 collected. pytest invocations for this batch: 4.

Full baseline: measured by this driver (the battery's verdict was not read: it is for commit `bea5e0d599a5`, and this tree is at `d85c14946d6a`).

Subset baselines: 1, each measured by this driver.

Known failures: 248 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23086 against 23086. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `C13_headless_counts_headed_rows_with_the_name_guard_off` | `src/cratekit/analysis/rekordbox_check.py` | user | 2 file(s) | 185 | 2 | killed |

## Row definitions

### `C13_headless_counts_headed_rows_with_the_name_guard_off`

M13's composite: drop both the title's headed guard and the head_key and head_tempo guard, so a row with a head in its title is counted as bare and adopt named for it

- File: `src/cratekit/analysis/rekordbox_check.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`, `tests/test_analyze_adopt.py`
- Collected: 185 against a baseline of 185
- Kills: 2 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_the_check_counts_only_a_title_whose_own_head_differs`
  - `tests/test_analyze_check.py::test_an_analysed_row_with_no_head_in_its_title_is_counted_for_adopt_and_never_suspect`

Old text:

```
            if not row.headed
            and row.head_key is None
            and row.head_tempo is None
            and row.key
```

New text:

```
            if row.key
```

