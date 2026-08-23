# Mutation table: u27-reports-round-3-fixes

Measured by `scripts/mutate.py` on 2026-08-23 16:31 UTC, branch `unit/u27-reports-cli` at `2354b67`. Pass kind: light.

Baseline: green, 6126 collected. pytest invocations for this batch: 17.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6126 against 6126. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `F1_as_of_falsiness` | `src/cratekit/cli/reports.py` | user | 1 file(s) | 24 | 1 | killed |
| `F2_depth_origin` | `src/cratekit/modules/reports/library.py` | user | 1 file(s) | 25 | 1 | killed |
| `F3_trash_absent_is_a_failure` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 947 | 1 | killed |
| `F4_absent_flag_never_set` | `src/cratekit/deletion/trash.py` | user | 2 file(s) | 576 | 1 | killed |
| `F5_gap_row_flood` | `src/cratekit/cli/reports.py` | user | 1 file(s) | 24 | 1 | killed |
| `F6_folder_count_overwrite` | `src/cratekit/modules/reports/coverage.py` | user | 1 file(s) | 25 | 2 | killed |
| `F7_ownership_exclusion_disjoint` | `tests/modules/test_reports.py` | maintainer | 1 file(s) | 6126 | 0 (promoted) | zero |
| `F8_oserror_gate` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 6126 | 0 (promoted) | zero |

## Zero rows and what they owe

- `F7_ownership_exclusion_disjoint` (maintainer facing): maintainer facing, composite not required
- `F8_oserror_gate` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `F1_as_of_falsiness`

Restore the falsiness test, so an explicitly empty as-of is read as an absent flag

- File: `src/cratekit/cli/reports.py`
- Surface: user
- Subset: test files importing cratekit.cli.reports
- Ran: `tests/test_reports_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_reports_cli.py::test_an_explicitly_empty_as_of_refuses_rather_than_answering_for_today`

Old text:

```
    if written is None:
```

New text:

```
    if not written:
```

### `F2_depth_origin`

Measure the tree depth from the export root again rather than from the tree's own node

- File: `src/cratekit/modules/reports/library.py`
- Surface: user
- Subset: test files importing cratekit.modules.reports.library
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_tree_nested_under_another_folder_yields_no_genre_from_that_folder`

Old text:

```
    try:
        return len(path) - path.index(tree_display)
    except ValueError:  # pragma: no cover - callers filter to governed paths
        return 0
```

New text:

```
    return len(path)
```

### `F3_trash_absent_is_a_failure`

Report a volume whose Trash has not been created yet as a failure again

- File: `src/cratekit/cli/doctor.py`
- Surface: user
- Subset: test files importing cratekit.cli.doctor
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 947 against a baseline of 947
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_volume_with_no_trash_directory_yet_is_not_a_failure`

Old text:

```
    if status.absent:
```

New text:

```
    if False:
```

### `F4_absent_flag_never_set`

Never mark an absent Trash as absent, so doctor cannot tell it from an unwritable one

- File: `src/cratekit/deletion/trash.py`
- Surface: user
- Subset: test files importing cratekit.deletion.trash
- Ran: `tests/test_deletion.py`, `tests/test_doctor.py`
- Collected: 576 against a baseline of 576
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_two_probe_answers_that_made_the_false_red_are_really_different`

Old text:

```
            absent=not target.exists(),
```

New text:

```
            absent=False,
```

### `F5_gap_row_flood`

Render one gap row per declared bucket again when the governed tree is absent

- File: `src/cratekit/cli/reports.py`
- Surface: user
- Subset: test files importing cratekit.cli.reports
- Ran: `tests/test_reports_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_reports_cli.py::test_a_missing_tree_is_named_once_rather_than_as_a_row_per_bucket`

Old text:

```
    if stats.shape.folders == 0:
```

New text:

```
    if False:
```

### `F6_folder_count_overwrite`

Count a playlist's raw length again, so folder rows stop reconciling with placements

- File: `src/cratekit/modules/reports/coverage.py`
- Surface: user
- Subset: test files importing cratekit.modules.reports.coverage
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 25 against a baseline of 25
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_folder_count_never_exceeds_what_the_collection_can_account_for`
  - `tests/modules/test_reports_engines.py::test_two_playlists_sharing_a_display_path_add_up_rather_than_overwrite`

Old text:

```
        counts.setdefault(playlist.path, 0)
        for track_id in playlist.track_ids:
            if track_id not in known:
                continue
            counts[playlist.path] += 1
            held.setdefault(track_id, []).append(playlist.path)
```

New text:

```
        counts[playlist.path] = len(playlist.track_ids)
        for track_id in playlist.track_ids:
            held.setdefault(track_id, []).append(playlist.path)
```

### `F7_ownership_exclusion_disjoint`

Drop the assertion that the exclusion set cannot name a file the floor claims

- File: `tests/modules/test_reports.py`
- Surface: maintainer
- Subset: the mutated test file itself
- Ran: `tests/modules/test_reports.py`
- Collected: 6126 against a baseline of 6126
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    claimed = sorted(set(_PACKAGE_MODULES_ANOTHER_UNIT_OWNS) & set(CITED_FLOOR))
    assert claimed == [], (
```

New text:

```
    claimed: list[str] = []
    assert claimed == [], (
```

### `F8_oserror_gate`

Paint the unanswerable Trash probe red even where no verb needs the check

- File: `src/cratekit/cli/doctor.py`
- Surface: user
- Subset: test files importing cratekit.cli.doctor
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 6126 against a baseline of 6126
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        needed = inputs.required(key)
```

New text:

```
        needed = True
```

