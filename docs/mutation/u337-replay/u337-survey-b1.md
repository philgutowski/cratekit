# Mutation table: u337-survey-b1

Measured by `scripts/mutate.py` on 2026-11-25 02:16 UTC, branch `HEAD` at `ff8e5ecb2`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 21196 collected. pytest invocations for this batch: 33.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py baseline` at 2026-11-25 02:16 UTC for commit `ff8e5ecb2d9b`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 11, each measured by this driver.

Known failures: 161 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 21196 against 21196. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u51-item-derivation.H1_export_item_not_payload` | `src/cratekit/export/cli.py` | user | 1 file(s) | 21196 | 0 (promoted) | zero |
| `r424.B4_warning_copied` | `src/cratekit/favorites/cli.py` | maintainer | 1 file(s) | 21196 | 0 (promoted) | zero |
| `u113-a.A2_queue_order` | `src/cratekit/intake/account_playlists.py` | user | 2 file(s) | 21196 | 0 (promoted) | zero |
| `u165.F5_report_failed` | `src/cratekit/intake/filing.py` | user | 1 file(s) | 21196 | 1 (promoted) | killed |
| `u188.M5_repeat_kept` | `src/cratekit/intake/land_cli.py` | maintainer | 1 file(s) | 21196 | 0 (promoted) | zero |
| `u71-b.B13_unlink_destination` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 21196 | 0 (promoted) | zero |
| `u69-b.M16_next_command` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 21196 | 0 (promoted) | zero |
| `u146-e.N3_owned_out_of_digest` | `src/cratekit/intake/native.py` | user | 1 file(s) | 21196 | 0 (promoted) | zero |
| `r504-a.A11_boundary_refuses` | `src/cratekit/label/cli.py` | user | 4 file(s) | 551 | 5 | killed |
| `u190.G5_resume_one_job_only` | `src/cratekit/label/go.py` | user | 2 file(s) | 21196 | 0 (promoted) | zero |
| `u239.M07_beside_done` | `src/cratekit/label/go.py` | user | 3 file(s) | 21196 | 0 (promoted) | zero |

## Zero rows and what they owe

- `u51-item-derivation.H1_export_item_not_payload` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r424.B4_warning_copied` (maintainer facing): maintainer facing, composite not required
- `u113-a.A2_queue_order` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u188.M5_repeat_kept` (maintainer facing): maintainer facing, composite not required
- `u71-b.B13_unlink_destination` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u69-b.M16_next_command` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u146-e.N3_owned_out_of_digest` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u190.G5_resume_one_job_only` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u239.M07_beside_done` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `u51-item-derivation.H1_export_item_not_payload`

The export handler reads the playlist key as its track, not the claimed item

- File: `src/cratekit/export/cli.py`
- Source: `u51-item-derivation.json`, row `H1_export_item_not_payload`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 21196 against a baseline of 21196
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    report = run_export_item(payload, str(item.item_id), cfg, account.resolve(cfg))
```

New text:

```
    report = run_export_item(payload, str(payload[PLAYLIST]), cfg, account.resolve(cfg))
```

### `r424.B4_warning_copied`

Hand callers the module level dict instead of a copy per call

- File: `src/cratekit/favorites/cli.py`
- Source: `r424.json`, row `B4_warning_copied`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild.py`
- Collected: 21196 against a baseline of 21196
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return (dict(LOCAL_WRITE_WARNING),)
```

New text:

```
    return (LOCAL_WRITE_WARNING,)
```

### `u113-a.A2_queue_order`

The account playlists are taken newest job first, the order the store lists them

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u113-a.json`, row `A2_queue_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`
- Collected: 21196 against a baseline of 21196
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        queued = sorted(
            batch_name.pass_jobs(cfg, pass_name), key=lambda job: (job.created, job.job_id)
        )
```

New text:

```
        queued = batch_name.pass_jobs(cfg, pass_name)
```

### `u165.F5_report_failed`

file_landed: report a filing whose entries failed as filed

- File: `src/cratekit/intake/filing.py`
- Source: `u165.json`, row `F5_report_failed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 21196 against a baseline of 21196
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_repair_rows.py::test_an_id_above_the_bound_that_is_the_files_inode_is_not_random`

Old text:

```
    if report.failed:
        return Filed(
            state=NOT_FILED,
```

New text:

```
    if False:
        return Filed(
            state=NOT_FILED,
```

### `u188.M5_repeat_kept`

_mapped_back: keep a repeated pair instead of dropping it, so the refusal names the folder pair twice on a drive that never moved

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M5_repeat_kept`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 21196 against a baseline of 21196
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return tuple(
        dict.fromkeys(
            (
                (str(area.staging), str(planned.folder)),
                (str(scratch_target), str(target)),
                stored,
            )
        )
    )
```

New text:

```
    return (
        (str(area.staging), str(planned.folder)),
        (str(scratch_target), str(target)),
        stored,
    )
```

### `u71-b.B13_unlink_destination`

Leave the intake file behind when place_files fails after writing it

- File: `src/cratekit/intake/landing.py`
- Source: `u71-b.json`, row `B13_unlink_destination`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 21196 against a baseline of 21196
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        destination.unlink(missing_ok=True)

```

New text:

```
(empty)
```

### `u69-b.M16_next_command`

Drop the literal next command from the written check a person reads

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69-b.json`, row `M16_next_command`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 21196 against a baseline of 21196
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
written to {written.list_path}; next: {command}"
```

New text:

```
written to {written.list_path}"
```

### `u146-e.N3_owned_out_of_digest`

FavoritesPlan.identity: the owned hearts are not digested, so an answer given for one set of them stands for another

- File: `src/cratekit/intake/native.py`
- Source: `u146-e.json`, row `N3_owned_out_of_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 21196 against a baseline of 21196
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if self.owned:
            identity["owned"] = [
```

New text:

```
        if self.owned and False:
            identity["owned"] = [
```

### `r504-a.A11_boundary_refuses`

The verb boundary no longer catches the shortfall, so it is refused as an unreadable listing

- File: `src/cratekit/label/cli.py`
- Source: `r504-a.json`, row `A11_boundary_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_sync_all.py`
- Collected: 551 against a baseline of 551
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`
  - `tests/test_label_tidal_catalogue.py::test_the_verb_boundary_keeps_the_rows_and_hands_back_the_shortfall`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`

Old text:

```
    except catalogue.HeartsShortfall as short:
        return list(short.rows), short

```

New text:

```
(empty)
```

### `u190.G5_resume_one_job_only`

_resume: take the first earlier job's tail whatever the count, so two manifests share one landing

- File: `src/cratekit/label/go.py`
- Source: `u190.json`, row `G5_resume_one_job_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`
- Collected: 21196 against a baseline of 21196
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    land = lands[0] if len(lands) == 1 else None
```

New text:

```
    land = lands[0] if lands else None
```

### `u239.M07_beside_done`

_beside: count only an open later go job, so one that downloaded and settled is ignored

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M07_beside_done`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 21196 against a baseline of 21196
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if other.is_open() or any(
```

New text:

```
        if other.is_open() or False and any(
```

