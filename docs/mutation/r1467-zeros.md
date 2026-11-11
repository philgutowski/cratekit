# Mutation table: r1467-zeros

Measured by `scripts/mutate.py` on 2026-11-11 05:17 UTC, branch `cloud/655-a-label-go-s-tail-lands-whatever` at `a6bad9fc`. Pass kind: light.

Baseline: green, 17816 collected. pytest invocations for this batch: 5.

Known failures: 161 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 17816 against 17816. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `M08_folder_only` | `src/cratekit/label/go.py` | user | 3 file(s) | 275 | 1 | killed |
| `M13_candidate_not_present` | `src/cratekit/label/go.py` | user | 3 file(s) | 275 | 1 | killed |

## Row definitions

### `M08_folder_only`

beside: read every artifact a job recorded, not only those directly in the staging folder, measured again with the test written for it

- File: `src/cratekit/label/go.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 275 against a baseline of 275
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_whose_tracks_were_recorded_in_another_folder_is_not_named_for_this_one`

Old text:

```
            if path.parent == folder

```

New text:

```
            if True

```

### `M13_candidate_not_present`

beside: name a go with tracks already named again as a candidate for files no download names, measured again with the test written for it

- File: `src/cratekit/label/go.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 275 against a baseline of 275
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_with_tracks_in_the_folder_is_named_once_beside_files_no_download_names`

Old text:

```
            if job_id in own or run is None or any(path in others for path in paths):
```

New text:

```
            if job_id in own or run is None:
```

