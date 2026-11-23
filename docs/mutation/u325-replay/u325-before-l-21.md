# Mutation table: u325-before-l-21

Measured by `scripts/mutate.py` on 2026-11-23 02:05 UTC, branch `HEAD` at `539638eb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22663 collected. pytest invocations for this batch: 29.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:15 UTC for commit `539638ebe629`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 14, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22663 against 22663. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u120.B2_first_mention_wins` | `src/cratekit/intake/account_playlists.py` | user | 2 file(s) | 50 | 2 | killed |
| `u175.F3_analyze_asked` | `src/cratekit/intake/refill.py` | user | 2 file(s) | 50 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R25_digest_drops_the_folder` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 50 | 2 | killed |
| `u207.I1_missing_never_screens` | `src/cratekit/intake/missing_cli.py` | user | 2 file(s) | 48 | 1 | killed |
| `r685-a.V2_landing_preflight_reads_the_shipped_text` | `src/cratekit/intake/landing.py` | user | 2 file(s) | 45 | 2 | killed |
| `u221.R20_landing_records_no_hold` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 38 | 1 | killed |
| `u173.M24_analyze_name` | `src/cratekit/intake/native.py` | user | 1 file(s) | 33 | 1 | killed |
| `r685-a.V2_composite_a_landing_under_an_alias` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 27 | 1 | killed |
| `u149.T21_landing_paired_again` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 6 | 1 | killed |
| `u135.A1_removed_namesake_written_into` | `src/cratekit/intake/native.py` | user | 1 file(s) | 1 | 1 | killed |
| `u135.A4_live_inbox_named_always_false` | `src/cratekit/intake/native.py` | user | 1 file(s) | 1 | 1 | killed |
| `u135.A7_leftover_joins_numbered_twin` | `src/cratekit/intake/native.py` | user | 1 file(s) | 1 | 1 | killed |
| `u135.A8_job_key_not_stamped` | `src/cratekit/intake/native.py` | user | 1 file(s) | 1 | 1 | killed |
| `u135.A12_inspiration_join_broken` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 1 | 1 | killed |

## Row definitions

### `u120.B2_first_mention_wins`

prefer_dated: a later mention that knows its date does not replace a first that does not

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u120.json`, row `B2_first_mention_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 50 against a baseline of 50
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_two_jobs_carried_is_one_heart_with_the_dated_jobs_date`
  - `tests/test_intake_land_hearts_native.py::test_the_pass_prefers_the_mention_that_knows_its_date`

Old text:

```
    return held is None or (not held.known and row.known)
```

New text:

```
    return held is None
```

### `u175.F3_analyze_asked`

refill.locate: stop excluding the reserved Analyze from the names asked

- File: `src/cratekit/intake/refill.py`
- Source: `u175.json`, row `F3_analyze_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`, `tests/test_inbox_analyzed.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_inbox_refill_never_takes_analyze_for_an_account_playlist_of_that_name`

Old text:

```
        asked = {name, recorded_name} - {"", native.ANALYZE}
```

New text:

```
        asked = {name, recorded_name} - {""}
```

### `u56-catalogue-searcher-and-tag-workers.R25_digest_drops_the_folder`

Two different empty folders digest identically, so a decision recorded against one satisfies the gate for the other

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R25_digest_drops_the_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_the_shell_digests_the_selection_and_the_folder_rather_than_a_constant`
  - `tests/test_genre_retag.py::test_two_different_empty_folders_digest_differently_through_the_pure_function`

Old text:

```
            FOLDER_KEY: folder,
            ITEMS_KEY: [dict(row) for row in items],
```

New text:

```
            ITEMS_KEY: [dict(row) for row in items],
```

### `u207.I1_missing_never_screens`

intake missing: the askable codes are never screened

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u207.json`, row `I1_missing_never_screens`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`, `tests/test_intake_missing_isrc.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_intake_missing_screens_the_codes_it_will_ask_before_asking_any`

Old text:

```
        found.screen_isrcs(askable)

```

New text:

```
(empty)
```

### `r685-a.V2_landing_preflight_reads_the_shipped_text`

The landing's preflight parses the shipped text, so an undeclared catalog tree is not seen

- File: `src/cratekit/intake/landing.py`
- Source: `r685-a.json`, row `V2_landing_preflight_reads_the_shipped_text`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_active_taxonomy.py`, `tests/test_landing_labels.py`
- Collected: 45 against a baseline of 45
- Kills: 2 (killed)
- Killed:
  - `tests/test_active_taxonomy.py::test_no_module_but_the_loader_reads_the_shipped_template`
  - `tests/test_landing_labels.py::test_an_undeclared_catalog_tree_refuses_before_any_file_moves`

Old text:

```
    checked = Checked(registry=tree_registry.read(cfg), declared=active_taxonomy.load(cfg))

```

New text:

```
    checked = Checked(
        registry=tree_registry.read(cfg),
        declared=taxonomy.load_taxonomy(taxonomy.shipped_template_text("default")),
    )

```

### `u221.R20_landing_records_no_hold`

pair_landed: mark a landing's twin with no hold, so it is read by time and its misses are held

- File: `src/cratekit/sync/twins.py`
- Source: `u221.json`, row `R20_landing_records_no_hold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_intake_land_twins.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_a_landing_twin_records_an_empty_hold`

Old text:

```
                one.account_id, one.playlist_id, name=one.account_name, twin=True, on_hold={}
```

New text:

```
                one.account_id, one.playlist_id, name=one.account_name, twin=True, on_hold=None
```

### `u173.M24_analyze_name`

native: the queue playlist renamed, so the skill sends a session to a playlist no landing fills

- File: `src/cratekit/intake/native.py`
- Source: `u173.json`, row `M24_analyze_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rekordbox_visit_skill.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_rekordbox_visit_skill.py::test_it_selects_the_playlist_every_landing_fills`

Old text:

```
ANALYZE = "Analyze"
```

New text:

```
ANALYZE = "Analysis"
```

### `r685-a.V2_composite_a_landing_under_an_alias`

What V2 holds without the guard's spelling: an aliased default loader at the preflight

- File: `src/cratekit/intake/landing.py`
- Source: `r685-a.json`, row `V2_composite_a_landing_under_an_alias`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_an_undeclared_catalog_tree_refuses_before_any_file_moves`

Old text:

```
    checked = Checked(registry=tree_registry.read(cfg), declared=active_taxonomy.load(cfg))

```

New text:

```
    from cratekit.core.taxonomy import default_taxonomy as shipped

    checked = Checked(registry=tree_registry.read(cfg), declared=shipped())

```

### `u149.T21_landing_paired_again`

plan_landing: plan a twin for an account playlist already paired

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T21_landing_paired_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_twins.py`
- Collected: 6 against a baseline of 6
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

### `u135.A1_removed_namesake_written_into`

Drop the node_removed skip so a soft-deleted set-named INBOX playlist is written into

- File: `src/cratekit/intake/native.py`
- Source: `u135.json`, row `A1_removed_namesake_written_into`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u135_set_inbox_join.py::test_a_removed_set_named_inbox_playlist_is_not_written_into`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_u135_set_inbox_join.py::test_a_removed_set_named_inbox_playlist_is_not_written_into`

Old text:

```
    for row in list(db.get_playlist(Name=plan.playlist)):
        if rb_writer.is_folder(row) or rb_writer.node_removed(row):
            continue
        if str(getattr(row, "ParentID", "") or "") == parent_id:
            return row
    return db.create_playlist(plan.playlist, parent=anchor)

```

New text:

```
    return rb_writer.ensure_playlist(db, plan.playlist, anchor)

```

### `u135.A4_live_inbox_named_always_false`

Never detect a live set-named INBOX playlist, so a hand-made one reads as made

- File: `src/cratekit/intake/native.py`
- Source: `u135.json`, row `A4_live_inbox_named_always_false`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u135_set_inbox_join.py::test_a_hand_made_inbox_playlist_of_the_set_name_is_named_found_not_recorded`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_u135_set_inbox_join.py::test_a_hand_made_inbox_playlist_of_the_set_name_is_named_found_not_recorded`

Old text:

```
    for row in list(db.get_playlist(Name=name)):
        if rb_writer.is_folder(row) or rb_writer.node_removed(row):
            continue
        if str(getattr(row, "ParentID", "") or "") == str(root_id):
            return True
    return False

```

New text:

```
    return False

```

### `u135.A7_leftover_joins_numbered_twin`

A numbered twin of the set name under INBOX is no longer named as a leftover

- File: `src/cratekit/intake/native.py`
- Source: `u135.json`, row `A7_leftover_joins_numbered_twin`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u135_set_inbox_join.py::test_a_numbered_leftover_inbox_playlist_is_named_on_the_screen_and_not_joined`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_u135_set_inbox_join.py::test_a_numbered_leftover_inbox_playlist_is_named_on_the_screen_and_not_joined`

Old text:

```
        if held.startswith(prefix) and held[len(prefix) :].isdigit():
            named.append(held)

```

New text:

```
        if False:
            named.append(held)

```

### `u135.A8_job_key_not_stamped`

A set landing's batch playlist record carries no job key

- File: `src/cratekit/intake/native.py`
- Source: `u135.json`, row `A8_job_key_not_stamped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u135_set_inbox_join.py::test_a_set_landed_once_keeps_one_inbox_playlist_named_for_the_set`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_u135_set_inbox_join.py::test_a_set_landed_once_keeps_one_inbox_playlist_named_for_the_set`

Old text:

```
        if plan.set_job_id:
            kept[INBOX_JOB_KEY] = plan.set_job_id

```

New text:

```
        if False:
            kept[INBOX_JOB_KEY] = plan.set_job_id

```

### `u135.A12_inspiration_join_broken`

Second landing of a set remakes the INSPIRATION playlist instead of adding

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u135.json`, row `A12_inspiration_join_broken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u135_set_inbox_join.py::test_inspiration_join_stays_pinned_beside_the_inbox_join`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_u135_set_inbox_join.py::test_inspiration_join_stays_pinned_beside_the_inbox_join`

Old text:

```
        if row is None or rb_writer.is_folder(row) or rb_writer.node_removed(row):
            raise refuse(
                "decision-stale",
                f"the set's playlist {plan.name!r} (row {plan.playlist_id}) the plan "
                f"adds to is not live any more, so nothing was written",
                origin=_ORIGIN,
                detail={"playlist": plan.playlist_id, "name": plan.name},
            )
        return row, False

```

New text:

```
        return db.create_playlist(plan.name, parent=folder), True

```

