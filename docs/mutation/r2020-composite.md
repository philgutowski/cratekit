# Mutation table: r2020-composite

Measured by `scripts/mutate.py` on 2026-11-24 01:53 UTC, branch `cloud/1036-resort-gate-names-unread-playlists` at `42e403d4`. Pass kind: light.

Baseline: green, 23136 collected. pytest invocations for this batch: 5.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 01:53 UTC for commit `42e403d4cbfb`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 1, each measured by this driver.

Known failures: 249 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23136 against 23136. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `C5_message_count_after_its_test` | `src/cratekit/write/rebuild.py` | user | 4 file(s) | 261 | 1 | killed |
| `C9_messages_first_report_only_after_its_test` | `src/cratekit/write/rebuild.py` | user | 4 file(s) | 261 | 1 | killed |
| `C14_favorites_step_reads_no_tree_list` | `src/cratekit/write/rebuild.py` | user | 4 file(s) | 261 | 2 | killed |

## Row definitions

### `C5_message_count_after_its_test`

M5 measured again once a test named two trees' same named playlists: count the distinct names, so the count disagrees with the list

- File: `src/cratekit/write/rebuild.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_unread_playlist_warnings.py`, `tests/test_routing_workers.py`, `tests/test_unrecorded_genre_folder.py`, `tests/test_resort_scope.py`
- Collected: 261 against a baseline of 261
- Kills: 1 (killed)
- Killed:
  - `tests/test_unread_playlist_warnings.py::test_the_count_is_every_entry_named_a_name_two_trees_share_included`

Old text:

```
        f"{len(found)} playlist(s) under the tree
```

New text:

```
        f"{len(set(found))} playlist(s) under the tree
```

### `C9_messages_first_report_only_after_its_test`

M9 measured again once a test read a job of two item reports: read the unidentified playlists of the first report only

- File: `src/cratekit/write/rebuild.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_unread_playlist_warnings.py`, `tests/test_routing_workers.py`, `tests/test_unrecorded_genre_folder.py`, `tests/test_resort_scope.py`
- Collected: 261 against a baseline of 261
- Kills: 1 (killed)
- Killed:
  - `tests/test_unread_playlist_warnings.py::test_every_item_report_of_a_job_is_read_back`

Old text:

```
    unread = [str(entry) for report in reports for entry in report.get("unidentified") or ()]
```

New text:

```
    unread = [str(entry) for report in reports[:1] for entry in report.get("unidentified") or ()]
```

### `C14_favorites_step_reads_no_tree_list`

M14's composite, the thing it guards: the favorites step skipped warning reads no list of driven trees, so a drive over another tree names the routing tree's skipped step

- File: `src/cratekit/write/rebuild.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_unread_playlist_warnings.py`, `tests/test_routing_workers.py`, `tests/test_unrecorded_genre_folder.py`, `tests/test_resort_scope.py`
- Collected: 261 against a baseline of 261
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_rebuild_of_another_tree_says_nothing_of_the_routing_trees_favorites[rebuild]`
  - `tests/test_routing_workers.py::test_a_rebuild_of_another_tree_says_nothing_of_the_routing_trees_favorites[resort]`

Old text:

```
    if declared.tree.id not in {str(tree_id) for tree_id in tree_ids}:
        return ()
```

New text:

```
    if False:
        return ()
```

