# Mutation table: u337-survey-a

Measured by `scripts/mutate.py` on 2026-11-25 03:43 UTC, branch `HEAD` at `ff8e5ecb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 21196 collected. pytest invocations for this batch: 17.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py baseline` at 2026-11-25 01:41 UTC for commit `ff8e5ecb2d9b`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 12, each measured by this driver.

Known failures: 161 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard. 15 row(s) were reused from a prior sidecar and were measured by an earlier process, whose children this run did not watch.

Null control `NULL_CONTROL`: killed 0, collected 21196 against 21196. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r668-a.M11_no_frozen_list_skip` | `src/cratekit/acquire/cli.py` | maintainer | 1 file(s) | 21196 | 0 (promoted) | zero |
| `u62.S7_naive_expiry_as_local` | `src/cratekit/acquire/provider_session.py` | maintainer | 2 file(s) | 21196 | 0 (promoted) | zero |
| `u50-author.W1_no_narrowing` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 98 | 6 | killed |
| `u212.S2_download_refused_all` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 21196 | 0 (promoted) | zero |
| `u212.S3_no_list_download` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 21196 | 0 (promoted) | zero |
| `r746-a.G7_sql_value_check_disarmed` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 21196 | 0 (promoted) | zero |
| `r746-d.G5_content_row_read_back_against_five_not_ten` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 21196 | 0 (promoted) | zero |
| `u28-skills-independent.S10_stamp_skill_name` | `src/cratekit/skills/cli.py` | maintainer | 1 file(s) | 21196 | 0 (promoted) | zero |
| `u28-skills-independent.S13_expanduser` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 21196 | 0 (promoted) | zero |
| `u28-skills-independent.S17_outcome_always_ok` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 21196 | 0 (promoted) | zero |
| `u28-skills-independent.S20_packaged_root_via_file` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 21196 | 0 (promoted) | zero |
| `u130-a.A1_removal_beats_addition` | `src/cratekit/sync/pair_merge.py` | user | 2 file(s) | 21196 | 1 (promoted) | killed |
| `r799-b.P6_one_file_is_one_group` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 21196 | 0 (promoted) | zero |
| `u119.G16_read_back_blind_to_leftovers` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 21196 | 0 (promoted) | zero |
| `r923.N12_digest_drops_values` | `src/cratekit/write/row_defaults.py` | maintainer | 1 file(s) | 21196 | 1 (promoted) | killed |
| `u125.D1_derive_test_tautology` | `tests/test_reserved_causes.py` | maintainer | 1 file(s) | 21196 | 0 (promoted) | zero |
| `u28-skills-independent.L9_command_comment_split` | `tests/test_skills_lint.py` | maintainer | 1 file(s) | 21196 | 1 (promoted) | killed |

## Zero rows and what they owe

- `r668-a.M11_no_frozen_list_skip` (maintainer facing): maintainer facing, composite not required
- `u62.S7_naive_expiry_as_local` (maintainer facing): maintainer facing, composite not required
- `u212.S2_download_refused_all` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u212.S3_no_list_download` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r746-a.G7_sql_value_check_disarmed` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r746-d.G5_content_row_read_back_against_five_not_ten` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u28-skills-independent.S10_stamp_skill_name` (maintainer facing): maintainer facing, composite not required
- `u28-skills-independent.S13_expanduser` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u28-skills-independent.S17_outcome_always_ok` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u28-skills-independent.S20_packaged_root_via_file` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r799-b.P6_one_file_is_one_group` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u119.G16_read_back_blind_to_leftovers` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u125.D1_derive_test_tautology` (maintainer facing): maintainer facing, composite not required

## Row definitions

### `r668-a.M11_no_frozen_list_skip`

a job whose payload names no list is compared against an empty path and refuses any list named beside it

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-a.json`, row `M11_no_frozen_list_skip`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 21196 against a baseline of 21196
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if not frozen:
        return
    try:
```

New text:

```
    try:
```

### `u62.S7_naive_expiry_as_local`

Read the client's naive expiry as local time

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u62.json`, row `S7_naive_expiry_as_local`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/test_adapter_contract.py`
- Collected: 21196 against a baseline of 21196
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if value.tzinfo is None:
```

New text:

```
        if value.tzinfo is None and False:
```

### `u50-author.W1_no_narrowing`

Ignore the portion and run the whole plan for every item, so each item does the whole backup

- File: `src/cratekit/backup/cli.py`
- Source: `u50-author.json`, row `W1_no_narrowing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 6 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_portion_the_engine_refused_fails_rather_than_reporting_a_copy`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`
  - `tests/test_backup_cli.py::test_an_outside_analysis_share_is_carried_through_the_verb`
  - `tests/test_backup_cli.py::test_asking_twice_about_a_half_failed_backup_answers_the_same_way_twice`

Old text:

```
    if portion is not None:
```

New text:

```
    if False:
```

### `u212.S2_download_refused_all`

sync_land._download: a download that landed nothing ends the pass whatever is staged, round one's F1

- File: `src/cratekit/cli/sync_land.py`
- Source: `u212.json`, row `S2_download_refused_all`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_crate_sync_skill.py`, `tests/test_inbox_analyzed.py`, `tests/test_rekordbox_visit_skill.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`
- Collected: 21196 against a baseline of 21196
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if not listed.staged:
            raise _Done(DOWNLOAD)
        return 0
    report.check(
```

New text:

```
        raise _Done(DOWNLOAD)
    report.check(
```

### `u212.S3_no_list_download`

sync_land._download: no early return for a pass with no list, so it asks the download verb for a list that is not there

- File: `src/cratekit/cli/sync_land.py`
- Source: `u212.json`, row `S3_no_list_download`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_crate_sync_skill.py`, `tests/test_inbox_analyzed.py`, `tests/test_rekordbox_visit_skill.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`
- Collected: 21196 against a baseline of 21196
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if listed.path is None:
        report.check(DOWNLOAD, "info", "nothing downloaded: every missing track is staged already")
        return 0
```

New text:

```
(empty)
```

### `r746-a.G7_sql_value_check_disarmed`

assert_created_rows_are_gridless: a value read from SQL is never a violation

- File: `src/cratekit/core/rb_writer.py`
- Source: `r746-a.json`, row `G7_sql_value_check_disarmed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_write_guard_completeness.py`, `tests/test_rb_writer_db.py`
- Collected: 21196 against a baseline of 21196
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            if value not in EMPTY_ON_CREATE:
                violations.append(f"{table}.{name} = {value!r}")
```

New text:

```
            if False:
                violations.append(f"{table}.{name} = {value!r}")
```

### `r746-d.G5_content_row_read_back_against_five_not_ten`

assert_created_rows_are_gridless: a content row is held to the playlist tables' five columns, so a key or a rate rides in. Measured again after the key taint test its zero bought

- File: `src/cratekit/core/rb_writer.py`
- Source: `r746-d.json`, row `G5_content_row_read_back_against_five_not_ten`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_write_guard_completeness.py`, `tests/test_rb_writer_guard.py`
- Collected: 21196 against a baseline of 21196
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        policy = CONTENT_ROW_EMPTY_COLUMNS if table == CONTENT_TABLE else GRIDLESS_ON_CREATE_COLUMNS
```

New text:

```
        policy = GRIDLESS_ON_CREATE_COLUMNS
```

### `u28-skills-independent.S10_stamp_skill_name`

the stamp stops recording which skill it belongs to, so a copied stamp cannot be told from its own

- File: `src/cratekit/skills/cli.py`
- Source: `u28-skills-independent.json`, row `S10_stamp_skill_name`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`
- Collected: 21196 against a baseline of 21196
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
\nskill = "{name}"
```

New text:

```
(empty)
```

### `u28-skills-independent.S13_expanduser`

--into stops expanding a tilde, so a target given as ~/skills is created as a literal directory named ~

- File: `src/cratekit/skills/cli.py`
- Source: `u28-skills-independent.json`, row `S13_expanduser`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`
- Collected: 21196 against a baseline of 21196
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    into = Path(ctx.args.into).expanduser() if ctx.args.into else default_target()
```

New text:

```
    into = Path(ctx.args.into) if ctx.args.into else default_target()
```

### `u28-skills-independent.S17_outcome_always_ok`

the envelope reports OK even when nothing was installed, so an empty package reads as a successful install

- File: `src/cratekit/skills/cli.py`
- Source: `u28-skills-independent.json`, row `S17_outcome_always_ok`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`
- Collected: 21196 against a baseline of 21196
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        outcome=Outcome.OK if checks else Outcome.NO_OP,
```

New text:

```
        outcome=Outcome.OK,
```

### `u28-skills-independent.S20_packaged_root_via_file`

packaged_root resolves by path arithmetic from __file__ rather than through importlib.resources

- File: `src/cratekit/skills/cli.py`
- Source: `u28-skills-independent.json`, row `S20_packaged_root_via_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`
- Collected: 21196 against a baseline of 21196
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return resources.files("cratekit.skills") / "assets"
```

New text:

```
    return Path(__file__).resolve().parent / "assets"
```

### `u130-a.A1_removal_beats_addition`

A removal wins over an addition, so a track removed on one side and re-added on the other is dropped

- File: `src/cratekit/sync/pair_merge.py`
- Source: `u130-a.json`, row `A1_removal_beats_addition`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_merge.py`, `tests/test_sync_pair.py`
- Collected: 21196 against a baseline of 21196
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_repair_rows.py::test_an_id_above_the_bound_that_is_the_files_inode_is_not_random`

Old text:

```
        if added or not removed:
```

New text:

```
        if not removed:
```

### `r799-b.P6_one_file_is_one_group`

plan: key a file under the library by its resolved name and not by the file itself

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-b.json`, row `P6_one_file_is_one_group`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 21196 against a baseline of 21196
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    try:
        stat = resolved.stat()
    except OSError:
        return ("name", str(resolved))
    return ("file", stat.st_dev, stat.st_ino)
```

New text:

```
    return ("name", str(resolved))
```

### `u119.G16_read_back_blind_to_leftovers`

_read_back: a track still in Favorites after the removals is not a disagreement

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G16_read_back_blind_to_leftovers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`
- Collected: 21196 against a baseline of 21196
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if removed_too and live - wanted:
```

New text:

```
        if False:
```

### `r923.N12_digest_drops_values`

The digest no longer covers the values written

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N12_digest_drops_values`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 21196 against a baseline of 21196
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_repair_rows.py::test_the_real_bound_is_a_fresh_files_inode_and_leaves_no_file_behind`

Old text:

```
                "defaults": {column: str(value) for column, value in rb_writer.CONTENT_ROW_DEFAULTS.items()},

```

New text:

```
(empty)
```

### `u125.D1_derive_test_tautology`

Restore the derive test's cause-total assert to x == x so a broken reserved count stays green there

- File: `tests/test_reserved_causes.py`
- Source: `u125.json`, row `D1_derive_test_tautology`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`
- Collected: 21196 against a baseline of 21196
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    assert (
        PINNED_RESERVED_CAUSE_COUNT + len(PINNED_NON_RESERVED_CAUSES),
        len(PINNED_NON_RESERVED_CAUSES),
        PINNED_RESERVED_CAUSE_COUNT,
    ) == (len(causes), len(non_reserved), len(CAUSES)), (
        "derived cause totals from the pins disagree with the tree"
    )

```

New text:

```
    assert (
        PINNED_RESERVED_CAUSE_COUNT + len(PINNED_NON_RESERVED_CAUSES),
        len(PINNED_NON_RESERVED_CAUSES),
        PINNED_RESERVED_CAUSE_COUNT,
    ) == (
        PINNED_RESERVED_CAUSE_COUNT + len(PINNED_NON_RESERVED_CAUSES),
        len(PINNED_NON_RESERVED_CAUSES),
        PINNED_RESERVED_CAUSE_COUNT,
    ), (
        "derived cause totals from the pins disagree with the tree"
    )

```

### `u28-skills-independent.L9_command_comment_split`

the fenced text stops being split into command and comment, so a retired name in a history note is checked as a command

- File: `tests/test_skills_lint.py`
- Source: `u28-skills-independent.json`, row `L9_command_comment_split`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`
- Collected: 21196 against a baseline of 21196
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_repair_rows.py::test_the_real_bound_is_a_fresh_files_inode_and_leaves_no_file_behind`

Old text:

```
            elif " #" in line:
                command, _, tail = line.partition(" #")
                command_parts.append(command)
                comment_parts.append(tail)
```

New text:

```
            elif " #" in line:
                command_parts.append(line)
```

