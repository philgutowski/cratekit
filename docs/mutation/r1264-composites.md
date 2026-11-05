# Mutation table: r1264-composites

Measured by `scripts/mutate.py` on 2026-11-05 17:12 UTC, branch `cloud/532-crate-sync-pair-refuses-every-pa` at `fca9c16f`. Pass kind: light.

Baseline: green, 16647 collected. pytest invocations for this batch: 4.

Known failures: 162 node ids whose failure is this machine's and not the tree's, read from `/tmp/claude-0/-home-user-cratekit/f7e2fcaf-586d-5218-9b51-1f70d625e657/scratchpad/known-r1264.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 16647 against 16647. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `M7_account_add_filter` | `src/cratekit/sync/pair_cli.py` | user | 1 file(s) | 16 | 1 | killed |

## Row definitions

### `M7_account_add_filter`

plan_pair: offer an unread track to the account as an addition, which already lists it; reached on a first sync, where no base strips the unread key

- File: `src/cratekit/sync/pair_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_first_sync_never_offers_the_account_an_unread_track_it_already_lists`

Old text:

```
        if remote_of(key) and key not in unseen and key not in unread_keys
```

New text:

```
        if remote_of(key) and key not in unseen
```

