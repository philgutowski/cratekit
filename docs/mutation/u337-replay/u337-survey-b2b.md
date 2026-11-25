# Mutation table: u337-survey-b2b

Measured by `scripts/mutate.py` on 2026-11-25 04:39 UTC, branch `HEAD` at `ff8e5ecb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 21196 collected. pytest invocations for this batch: 17.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py baseline` at 2026-11-25 01:41 UTC for commit `ff8e5ecb2d9b`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 4, each measured by this driver.

Known failures: 161 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 21196 against 21196. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u116.M13_utc_year` | `src/cratekit/organize/filing.py` | user | 1 file(s) | 21196 | 0 (promoted) | zero |
| `u227.R12_tree_filter` | `src/cratekit/organize/mirror_downloads.py` | user | 1 file(s) | 21196 | 0 (promoted) | zero |
| `u214.M12_frozen_pairs` | `src/cratekit/organize/mirror_frozen.py` | user | 1 file(s) | 21196 | 0 (promoted) | zero |
| `r368-round-2.G14_the_destination_check_is_equality_only` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 21196 | 0 (promoted) | zero |
| `r368-round-2.G6_ancestors_not_walked` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 21196 | 0 (promoted) | zero |
| `r368.G5_paths_compared_as_strings` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 21196 | 0 (promoted) | zero |

## Zero rows and what they owe

- `u116.M13_utc_year` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u227.R12_tree_filter` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u214.M12_frozen_pairs` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r368-round-2.G14_the_destination_check_is_equality_only` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r368-round-2.G6_ancestors_not_walked` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r368.G5_paths_compared_as_strings` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `u116.M13_utc_year`

year_of_mark: the year is taken from the UTC stamp digits rather than local time

- File: `src/cratekit/organize/filing.py`
- Source: `u116.json`, row `M13_utc_year`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 21196 against a baseline of 21196
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if when.tzinfo is not None:
        when = when.astimezone()
    return f"{when.year:04d}"
```

New text:

```
    return str(marked or "")[:4]
```

### `u227.R12_tree_filter`

filed: read ledger entries of every tree, not the routing tree's alone

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `u227.json`, row `R12_tree_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 21196 against a baseline of 21196
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if entry.tree == tree and entry.digest not in by_person:
```

New text:

```
        if entry.digest not in by_person:
```

### `u214.M12_frozen_pairs`

_unmirrored: accept a frozen node of any length

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u214.json`, row `M12_frozen_pairs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 21196 against a baseline of 21196
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        isinstance(one, list) and len(one) == 2 and all(isinstance(part, str) for part in one)
```

New text:

```
        isinstance(one, list) and all(isinstance(part, str) for part in one)
```

### `r368-round-2.G14_the_destination_check_is_equality_only`

re-measured: drop the name-plus-parent half, so a landing path that is not on disk yet passes

- File: `src/cratekit/session/restore_cli.py`
- Source: `r368-round-2.json`, row `G14_the_destination_check_is_equality_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 21196 against a baseline of 21196
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if _same_place(landing, live) or (
        landing.name == live.name and _same_place(landing.parent, live.parent)
    ):

```

New text:

```
    if _same_place(landing, live):

```

### `r368-round-2.G6_ancestors_not_walked`

re-measured: ask samefile of the candidate alone, so a differently cased ancestor is missed

- File: `src/cratekit/session/restore_cli.py`
- Source: `r368-round-2.json`, row `G6_ancestors_not_walked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 21196 against a baseline of 21196
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return any(_same_place(ancestor, root) for ancestor in (place, *place.parents))

```

New text:

```
    return _same_place(place, root)

```

### `r368.G5_paths_compared_as_strings`

the review's finding, restored: compare spellings rather than places

- File: `src/cratekit/session/restore_cli.py`
- Source: `r368.json`, row `G5_paths_compared_as_strings`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 21196 against a baseline of 21196
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    try:
        return one.samefile(other)
    except OSError:
        return one == other

```

New text:

```
    return one == other

```

