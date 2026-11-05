# Mutation table: u201-composites

Measured by `scripts/mutate.py` on 2026-11-05 01:52 UTC, branch `cloud/489-an-edit-made-on-tidal-to-a-genre` at `ab2355d7`. Pass kind: full.

Baseline: green, 16084 collected. pytest invocations for this batch: 9.

Known failures: 161 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 16084 against 16084. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `C1_two_bands_composite` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 5 file(s) | 173 | 1 | killed |
| `C2_agrees_never` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 5 file(s) | 173 | 1 | killed |
| `C3_settled_none` | `src/cratekit/modules/outbound/mirror.py` | user | 5 file(s) | 16084 | 0 (promoted) | zero |
| `C4_settle_none` | `src/cratekit/modules/outbound/ledger.py` | user | 5 file(s) | 173 | 3 | killed |
| `C5_leave_nothing` | `src/cratekit/organize/mirror_edits.py` | user | 5 file(s) | 173 | 5 | killed |

## Zero rows and what they owe

- `C3_settled_none` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `C1_two_bands_composite`

E2 with the guard after it: neither the two bands guard nor the still in two bands guard, so a track added to two bands at once is moved to one

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 173 against a baseline of 173
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_a_track_added_to_two_bands_at_once_is_held_on_both_sides`

Old text:

```
    if len(added) > 1:
        return (
            HELD,
            None,
            f"added on the account to {len(added)} band playlists at once "
            f"({', '.join(_titles(added))}), so which one it belongs in is not "
            f"something the account says",
        )
    if removed and len(now) == 1:
        (place,) = now
        return MOVE, place, f"taken off {', '.join(_titles(removed))} on the account, left in {place.title}"
    if removed and len(now) > 1:
        return (
            HELD,
            None,
            f"taken off {', '.join(_titles(removed))} on the account and still in "
            f"{len(now)} band playlists there, so which one it belongs in is not "
            f"something the account says",
        )

```

New text:

```
    if False:
        return (
            HELD,
            None,
            f"added on the account to {len(added)} band playlists at once "
            f"({', '.join(_titles(added))}), so which one it belongs in is not "
            f"something the account says",
        )
    if removed and len(now) == 1:
        (place,) = now
        return MOVE, place, f"taken off {', '.join(_titles(removed))} on the account, left in {place.title}"
    if False:
        return (
            HELD,
            None,
            f"taken off {', '.join(_titles(removed))} on the account and still in "
            f"{len(now)} band playlists there, so which one it belongs in is not "
            f"something the account says",
        )

```

### `C2_agrees_never`

_agrees: a MOVE never agrees with rekordbox, the thing E5's exactness narrows

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 173 against a baseline of 173
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_both_sides_moving_a_track_to_one_place_agree`

Old text:

```
        return now == frozenset({to})
```

New text:

```
        return False
```

### `C3_settled_none`

settled: no playlist with nothing to write records its snapshot, the thing M3 narrows

- File: `src/cratekit/modules/outbound/mirror.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 16084 against a baseline of 16084
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if one.action == REUSE and not one.writes and one.remote_id
```

New text:

```
        if False
```

### `C4_settle_none`

settle_mirror_tracks: the library step settles nothing, the thing L2 narrows

- File: `src/cratekit/modules/outbound/ledger.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 173 against a baseline of 173
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_a_move_in_rekordbox_after_an_edit_was_taken_is_rekordboxs`
  - `tests/test_organize_mirror_edits.py::test_a_track_moved_on_the_account_is_retagged_refiled_and_the_next_run_plans_nothing`
  - `tests/test_organize_mirror_edits.py::test_the_ledger_keeps_a_snapshot_apart_from_none_and_only_on_its_own_playlist`

Old text:

```
    wanted = list(settled)
```

New text:

```
    wanted = []
```

### `C5_leave_nothing`

plan: a move leaves no tree playlist, the thing O4 narrows

- File: `src/cratekit/organize/mirror_edits.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 173 against a baseline of 173
- Kills: 5 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_a_library_moved_since_the_plan_writes_nothing`
  - `tests/test_organize_mirror_edits.py::test_a_move_to_unsorted_clears_the_energy`
  - `tests/test_organize_mirror_edits.py::test_a_move_within_a_genre_keeps_the_genre_and_moves_the_energy_to_the_nearest`
  - `tests/test_organize_mirror_edits.py::test_a_track_moved_on_the_account_is_retagged_refiled_and_the_next_run_plans_nothing`
  - `tests/test_organize_mirror_edits.py::test_two_moves_follow_the_later_account_move`

Old text:

```
            leave_ids = [pid for pid in held if pid not in wanted and routed(tree.names[pid])]
```

New text:

```
            leave_ids = []
```

