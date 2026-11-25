# Mutation table: u337-survey-b2a

Measured by `scripts/mutate.py` on 2026-11-25 04:24 UTC, branch `HEAD` at `ff8e5ecb2`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 21196 collected. pytest invocations for this batch: 21.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py baseline` at 2026-11-25 04:24 UTC for commit `ff8e5ecb2d9b`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 6, each measured by this driver.

Known failures: 161 node ids whose failure is this machine's and not the tree's, read from `<survey-worktree>/.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 21196 against 21196. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u100-a.R1_slug_only_presence` | `src/cratekit/label/registry.py` | user | 4 file(s) | 21196 | 0 (promoted) | zero |
| `u99-a.A13_by_name_unnormalized` | `src/cratekit/label/registry.py` | user | 3 file(s) | 21196 | 0 (promoted) | zero |
| `r259.O1_no_tracks_guard` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 21196 | 1 (promoted) | killed |
| `r259.O5_memo` | `src/cratekit/label/sweep.py` | maintainer | 5 file(s) | 21196 | 0 (promoted) | zero |
| `r1308.M10_count_unchecked` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 21196 | 0 (promoted) | zero |
| `u226.M18_waited_unformatted` | `src/cratekit/modules/outbound/tidal_account.py` | maintainer | 9 file(s) | 21196 | 0 (promoted) | zero |
| `u112-b.A6_exported_not_product_made` | `src/cratekit/organize/account.py` | user | 1 file(s) | 21196 | 1 (promoted) | killed |

## Zero rows and what they owe

- `u100-a.R1_slug_only_presence` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u99-a.A13_by_name_unnormalized` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r259.O5_memo` (maintainer facing): maintainer facing, composite not required
- `r1308.M10_count_unchecked` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u226.M18_waited_unformatted` (maintainer facing): maintainer facing, composite not required

## Row definitions

### `u100-a.R1_slug_only_presence`

RegistryStore.adopt checks presence by slug alone, the R-381 hazard: a label held under sueno is filed again as sue-o

- File: `src/cratekit/label/registry.py`
- Source: `u100-a.json`, row `R1_slug_only_presence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 21196 against a baseline of 21196
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                held = Registry(labels=current).resolve(name)
```

New text:

```
                held = Registry(labels=current).by_id(label_id)
```

### `u99-a.A13_by_name_unnormalized`

_folded: drop the NFC normalization, so a decomposed accented name resolves nothing

- File: `src/cratekit/label/registry.py`
- Source: `u99-a.json`, row `A13_by_name_unnormalized`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 21196 against a baseline of 21196
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return unicodedata.normalize("NFC", name.strip()).casefold()
```

New text:

```
    return name.strip().casefold()
```

### `r259.O1_no_tracks_guard`

A release the provider lists with no track reads as owned, since all over nothing is True

- File: `src/cratekit/label/sweep.py`
- Source: `r259.json`, row `O1_no_tracks_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`
- Collected: 21196 against a baseline of 21196
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_repair_rows.py::test_an_id_above_the_bound_that_is_the_files_inode_is_not_random`

Old text:

```
        if not rows:
            return False

```

New text:

```
(empty)
```

### `r259.O5_memo`

The answer is not kept, so the increment's scope reads every release a second time

- File: `src/cratekit/label/sweep.py`
- Source: `r259.json`, row `O5_memo`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`
- Collected: 21196 against a baseline of 21196
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if identity not in self._answers:
            self._answers[identity] = self._holds(identity)
        return self._answers[identity]
```

New text:

```
        return self._holds(identity)
```

### `r1308.M10_count_unchecked`

_removal_read_back: drop the whole number check on the count

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M10_count_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 21196 against a baseline of 21196
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
if not _count(declared) or not _count(videos) or videos != 0
```

New text:

```
if not _count(videos) or videos != 0
```

### `u226.M18_waited_unformatted`

_waited: seconds named as 7.0 rather than 7

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u226.json`, row `M18_waited_unformatted`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`
- Collected: 21196 against a baseline of 21196
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return f"{seconds:g}"
```

New text:

```
    return f"{seconds}"
```

### `u112-b.A6_exported_not_product_made`

An exported playlist the ledger records as product made is listed as the author's

- File: `src/cratekit/organize/account.py`
- Source: `u112-b.json`, row `A6_exported_not_product_made`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 21196 against a baseline of 21196
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_repair_rows.py::test_the_real_bound_is_a_fresh_files_inode_and_leaves_no_file_behind`

Old text:

```
            | ledger.product_made_among(cfg, (one.playlist_id for one in listed))
```

New text:

```
            | frozenset()
```

