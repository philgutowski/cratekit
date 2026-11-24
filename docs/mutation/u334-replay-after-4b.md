# Mutation table: u334-replay-after-4b

Measured by `scripts/mutate.py` on 2026-11-24 07:38 UTC, branch `cloud/983-test-slice-3-of-4` at `30a19d79`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23214 collected. pytest invocations for this batch: 4.

Full baseline: measured by this driver (the battery's verdict was not read: it is for commit `e58f16b2e549`, and this tree is at `30a19d7998e0`).

Subset baselines: 1, each measured by this driver.

Known failures: 248 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23214 against 23214. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u241.M01_worker_takes_the_interrupt` | `src/cratekit/core/pool.py` | user | 1 file(s) | 26 | 1 | killed |

## Row definitions

### `u241.M01_worker_takes_the_interrupt`

stream worker: no longer ignore the terminal's interrupt, so Ctrl-C kills a worker mid item

- File: `src/cratekit/core/pool.py`
- Source: `u241.json`, row `M01_worker_takes_the_interrupt`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_stream.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_stream.py::test_the_terminals_interrupt_does_not_kill_a_stream_worker`

Old text:

```
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    _leave_when_the_parent_does()

```

New text:

```
    _leave_when_the_parent_does()

```

