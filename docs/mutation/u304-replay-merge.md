# Mutation table: u304-replay-merge

Measured by `scripts/mutate.py` on 2026-11-23 06:06 UTC, branch `cloud/861-sync-a-fifth-smaller` at `761e7227`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22530 collected. pytest invocations for this batch: 21.

Full baseline: measured by this driver (the battery's verdict was not read: it is for commit `d6b0281be362`, and this tree is at `761e72276c07`).

Subset baselines: 8, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `/tmp/claude-0/-home-user-cratekit/5752b730-82d2-5bb0-b120-3c1da5ca9238/scratchpad/merge-known.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22530 against 22530. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r835-c.S2_sync_hands_the_ledger_to_the_sweep_again` | `src/cratekit/sync/cli.py` | user | 4 file(s) | 298 | 1 | killed |
| `r837-a.A17_sweep_hand_off` | `src/cratekit/sync/cli.py` | user | 5 file(s) | 361 | 1 | killed |
| `u147-c.M19_sweep_handoff` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `r1056.S1_no_landing_step_names_intake_missing` | `src/cratekit/sync/mark_cli.py` | user | 2 file(s) | 102 | 4 | killed |
| `r1056.S2_unreachable_step_names_sync` | `src/cratekit/sync/mark_cli.py` | user | 2 file(s) | 102 | 1 | killed |
| `u147-c.M20_pair_scope` | `src/cratekit/sync/pair_model.py` | user | 1 file(s) | 34 | 1 | killed |
| `r835-b.S1_built_year_excluded_from_sweep` | `src/cratekit/sync/playlists.py` | user | 4 file(s) | 271 | 1 | killed |
| `r837-a.A16_sweep_excludes_set` | `src/cratekit/sync/playlists.py` | user | 5 file(s) | 334 | 1 | killed |
| `u113-a.A6_sweep_passes_no_name` | `src/cratekit/sync/playlists.py` | user | 2 file(s) | 141 | 1 | killed |
| `u147-c.M18_sweep_exclusion` | `src/cratekit/sync/playlists.py` | user | 1 file(s) | 34 | 1 | killed |
| `u149.T21_landing_paired_again` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 5 | 1 | killed |

## Row definitions

### `r835-c.S2_sync_hands_the_ledger_to_the_sweep_again`

sync.cli._plan_playlists: the sweep is handed no label built playlists, so every year playlist is swept as intake

- File: `src/cratekit/sync/cli.py`
- Source: `r835-c.json`, row `S2_sync_hands_the_ledger_to_the_sweep_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`, `tests/test_intake_writers_native.py`, `tests/test_label_playlists.py`, `tests/test_sync_all.py`
- Collected: 298 against a baseline of 298
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_the_sync_pass_hands_the_sweep_every_year_playlist_a_build_recorded`

Old text:

```
    label_built = ledger.label_playlist_ids(cfg)
```

New text:

```
    label_built = frozenset()
```

### `r837-a.A17_sweep_hand_off`

sync.cli: the sweep is handed no set playlist, so the exclusion has nothing to exclude

- File: `src/cratekit/sync/cli.py`
- Source: `r837-a.json`, row `A17_sweep_hand_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`, `tests/test_export_set.py`, `tests/test_intake_writers_native.py`, `tests/test_label_playlists.py`, `tests/test_sync_all.py`
- Collected: 361 against a baseline of 361
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_the_sweep_never_reads_a_set_playlist_as_intake`

Old text:

```
            set_built=set_built,
```

New text:

```
            set_built=frozenset(),
```

### `u147-c.M19_sweep_handoff`

sync.cli: the sync source hands the sweep no mirrored playlist

- File: `src/cratekit/sync/cli.py`
- Source: `u147-c.json`, row `M19_sweep_handoff`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_the_sync_pass_hands_the_sweep_every_mirrored_playlist`

Old text:

```
            mirrored=mirrored,
```

New text:

```
(empty)
```

### `r1056.S1_no_landing_step_names_intake_missing`

_native_proof: drop the named source from the no landing step, so a label batch is told intake missing

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r1056.json`, row `S1_no_landing_step_names_intake_missing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`, `tests/test_sync_mark.py`
- Collected: 102 against a baseline of 102
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_pass_no_closed_committed_native_landing_names_is_refused_by_name[abandoned]`
  - `tests/test_label_mark_native.py::test_a_pass_no_closed_committed_native_landing_names_is_refused_by_name[another-pass]`
  - `tests/test_label_mark_native.py::test_a_pass_no_closed_committed_native_landing_names_is_refused_by_name[never-committed]`
  - `tests/test_label_mark_native.py::test_a_pass_no_closed_committed_native_landing_names_is_refused_by_name[no-landing]`

Old text:

```
            f"land the pass with crate intake land --pass and {named}, then run {verb} "
```

New text:

```
            f"land the pass with crate intake land --pass and {SYNC_PASS_NAMED}, then run {verb} "
```

### `r1056.S2_unreachable_step_names_sync`

_native_proof: name sync mark in the unreachable library step whatever verb asked

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r1056.json`, row `S2_unreachable_step_names_sync`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`, `tests/test_sync_mark.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_an_unreachable_library_names_label_mark_as_the_verb_to_run_again`

Old text:

```
            f"mount the library volume, then run {verb} again",
```

New text:

```
            "mount the library volume, then run crate sync mark again",
```

### `u147-c.M20_pair_scope`

sync.pair_cli._scope_account: a mirrored playlist may be paired

- File: `src/cratekit/sync/pair_model.py`
- Source: `u147-c.json`, row `M20_pair_scope`
- Moved: the same text, now in src/cratekit/sync/pair_model.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_sync_pair_refuses_to_pair_a_mirrored_playlist`

Old text:

```
    if account_id in mirrored:
```

New text:

```
    if False:
```

### `r835-b.S1_built_year_excluded_from_sweep`

sync.playlists.exclusion: a year playlist a label build recorded is swept as intake

- File: `src/cratekit/sync/playlists.py`
- Source: `r835-b.json`, row `S1_built_year_excluded_from_sweep`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_label_playlists.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 271 against a baseline of 271
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_the_sweep_never_reads_a_built_year_playlist_as_intake`

Old text:

```
    if playlist.playlist_id in label_built:
        return Excluded.LABEL_FOLDER
```

New text:

```
    if False:
        return Excluded.LABEL_FOLDER
```

### `r837-a.A16_sweep_excludes_set`

sync.playlists.exclusion: a set playlist export set recorded is swept as intake

- File: `src/cratekit/sync/playlists.py`
- Source: `r837-a.json`, row `A16_sweep_excludes_set`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`, `tests/test_incremental_sync.py`, `tests/test_label_playlists.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 334 against a baseline of 334
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_the_sweep_never_reads_a_set_playlist_as_intake`

Old text:

```
    if playlist.playlist_id in set_built:
        return Excluded.SET_PLAYLIST
```

New text:

```
    if False:
        return Excluded.SET_PLAYLIST
```

### `u113-a.A6_sweep_passes_no_name`

The sweep queues each playlist job without the account's name

- File: `src/cratekit/sync/playlists.py`
- Source: `u113-a.json`, row `A6_sweep_passes_no_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_sync_all.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_sync_all_records_the_name_the_account_listed_on_each_playlist_job`

Old text:

```
                name=names.get(playlist_id),
```

New text:

```
                name=None,
```

### `u147-c.M18_sweep_exclusion`

sync.playlists.exclusion: a mirrored playlist is swept as intake

- File: `src/cratekit/sync/playlists.py`
- Source: `u147-c.json`, row `M18_sweep_exclusion`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_the_intake_sweep_leaves_a_mirrored_playlist_alone`

Old text:

```
    if playlist.playlist_id in mirrored:
        return Excluded.MIRROR

```

New text:

```
(empty)
```

### `u149.T21_landing_paired_again`

plan_landing: plan a twin for an account playlist already paired

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T21_landing_paired_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_twins.py`
- Collected: 5 against a baseline of 5
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_twins.py::test_an_account_playlist_already_paired_gets_no_second_twin`

Old text:

```
    wanted = [(account_id, name) for account_id, name in accounts if account_id not in held]
```

New text:

```
    wanted = list(accounts)
```

