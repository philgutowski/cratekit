# Mutation table: u202-composites

Measured by `scripts/mutate.py` on 2026-11-05 02:14 UTC, branch `cloud/490-a-playlist-made-on-tidal-in-a-sy` at `cccf9f41`. Pass kind: light.

Baseline: green, 16063 collected. pytest invocations for this batch: 10.

Known failures: 162 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (2 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 16063 against 16063. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `C8_scope` | `src/cratekit/sync/pair_cli.py` | user | 3 file(s) | 123 | 1 | killed |
| `C10_reads_account` | `src/cratekit/sync/pair_cli.py` | user | 3 file(s) | 123 | 1 | killed |
| `R2_confined` | `src/cratekit/sync/pair_reverse.py` | user | 1 file(s) | 37 | 1 | killed |
| `P1_reserve_held` | `src/cratekit/modules/outbound/pairs.py` | user | 3 file(s) | 123 | 1 | killed |
| `C3_composite` | `src/cratekit/sync/pair_cli.py` | user | 3 file(s) | 123 | 2 | killed |

## Row definitions

### `C8_scope`

_discovered_back: an account playlist a pair may not hold is brought over

- File: `src/cratekit/sync/pair_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_a_set_playlist_sharing_a_name_does_not_stop_the_authors_own`

Old text:

```
            try:
                _scope_account(
                    account_id, reader.listed, reader.label_owned, reader.set_built, reader.mirrored
                )
            except CratekitError as exc:
```

New text:

```
            try:
                pass
            except CratekitError as exc:
```

### `C10_reads_account`

plan: a sync of every pair with no marked pair never lists the account, so nothing comes back

- File: `src/cratekit/sync/pair_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_with_every_pair_released_a_new_playlist_in_a_recorded_folder_still_comes`

Old text:

```
    reads_account = bool(wanted) or (every and bool(document.folders))
```

New text:

```
    reads_account = bool(wanted)
```

### `R2_confined`

pair_reverse.create: the twins' confinement check is not run before the commit

- File: `src/cratekit/sync/pair_reverse.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_a_write_outside_the_playlist_made_is_refused_with_nothing_written`

Old text:

```
                twins.assert_confined(
                    db,
```

New text:

```
                (lambda *a, **k: None)(
                    db,
```

### `P1_reserve_held`

reserve_made_rekordbox: an account playlist a pair already holds is made a second rekordbox playlist

- File: `src/cratekit/modules/outbound/pairs.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_reserving_an_account_playlist_a_pair_holds_answers_that_pair_and_makes_nothing`

Old text:

```
            held = document.pairs.get(account_id)
            if held is not None:
                return held.rekordbox_id, False
            rekordbox_id = str(create())
```

New text:

```
            rekordbox_id = str(create())
```

### `C3_composite`

composite for C3_removed_only in u202.md: plan_pair never dates a rekordbox removal, so a removal later than the account's put back reads as no moment

- File: `src/cratekit/sync/pair_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 123 against a baseline of 123
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_a_rekordbox_removal_later_than_the_account_putting_it_back_takes_it_off_both`
  - `tests/test_sync_pair_back.py::test_a_track_put_back_on_the_account_after_rekordbox_took_it_out_stays_on_both`

Old text:

```
                rekordbox_removed[as_key(content_id)] = max(
```

New text:

```
                _undated = max(
```

