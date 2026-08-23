# Mutation table: u27-reports-round-2

Measured by `scripts/mutate.py` on 2026-08-23 15:48 UTC, branch `unit/u27-reports-cli` at `106335d`. Pass kind: light.

Baseline: green, 6120 collected. pytest invocations for this batch: 12.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6120 against 6120. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `C3_uncovered_order` | `src/cratekit/modules/reports/coverage.py` | user | 1 file(s) | 23 | 2 | killed |
| `C3b_tie_break` | `src/cratekit/modules/reports/coverage.py` | user | 1 file(s) | 23 | 1 | killed |
| `L2_genre_parent` | `src/cratekit/modules/reports/library.py` | user | 1 file(s) | 23 | 2 | killed |
| `S5_handler_key_wrong` | `src/cratekit/cli/reports.py` | user | 1 file(s) | 22 | 2 | killed |
| `S5b_engine_default_drift` | `src/cratekit/modules/reports/duplicates.py` | user | 2 file(s) | 371 | 3 | killed |
| `D1_probe_creates` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 945 | 1 | killed |

## Row definitions

### `C3_uncovered_order`

Round 1 zero, re-run against the replacement guard: drop the deterministic order

- File: `src/cratekit/modules/reports/coverage.py`
- Surface: user
- Subset: test files importing cratekit.modules.reports.coverage
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 23 against a baseline of 23
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_the_uncovered_list_is_ordered_BY_ARTIST_AND_NOT_BY_THE_WALK`
  - `tests/modules/test_reports_engines.py::test_two_entries_sharing_an_artist_and_a_name_still_hold_an_order`

Old text:

```
        uncovered=tuple(sorted(uncovered, key=_by_name)),
```

New text:

```
        uncovered=tuple(uncovered),
```

### `C3b_tie_break`

Sort on artist and name alone, leaving the tie to the walk

- File: `src/cratekit/modules/reports/coverage.py`
- Surface: user
- Subset: test files importing cratekit.modules.reports.coverage
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_two_entries_sharing_an_artist_and_a_name_still_hold_an_order`

Old text:

```
    return (placement.entry.artist, placement.entry.name, placement.entry.track_id)
```

New text:

```
    return (placement.entry.artist, placement.entry.name, "")
```

### `L2_genre_parent`

Round 1 zero, re-run against the replacement guards: loosen the genre filter

- File: `src/cratekit/modules/reports/library.py`
- Surface: user
- Subset: test files importing cratekit.modules.reports.library
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 23 against a baseline of 23
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_folder_below_a_genre_is_not_itself_a_genre`
  - `tests/modules/test_reports_engines.py::test_a_tree_nested_under_another_folder_yields_no_genre_from_that_folder`

Old text:

```
        if len(folder) < 2 or folder[-2] != tree_display:
```

New text:

```
        if len(folder) < 2 or tree_display not in folder:
```

### `S5_handler_key_wrong`

Round 1's S5 was inert because the engine default matched; pass a WRONG key instead

- File: `src/cratekit/cli/reports.py`
- Surface: user
- Subset: test files importing cratekit.cli.reports
- Ran: `tests/test_reports_cli.py`
- Collected: 22 against a baseline of 22
- Kills: 2 (killed)
- Killed:
  - `tests/test_reports_cli.py::test_duplicates_offers_the_pair_into_the_queue_under_its_own_handler_key`
  - `tests/test_reports_cli.py::test_the_shell_passes_the_REGISTRY_key_rather_than_letting_the_engine_default`

Old text:

```
            view, store, template=_template(cfg), handler_key=ctx.entry.handler_key
```

New text:

```
            view, store, template=_template(cfg), handler_key="duplicates"
```

### `S5b_engine_default_drift`

Drift the engine's own copy of the handler key away from the registry's

- File: `src/cratekit/modules/reports/duplicates.py`
- Surface: user
- Subset: test files importing cratekit.modules.reports.duplicates
- Ran: `tests/modules/test_reports.py`, `tests/test_reports_cli.py`
- Collected: 371 against a baseline of 371
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_reports.py::test_every_item_carries_the_handler_key_the_registry_declares`
  - `tests/modules/test_reports.py::test_the_declared_handler_key_is_the_one_the_registry_carries`
  - `tests/test_reports_cli.py::test_the_two_copies_of_the_duplicate_handler_key_cannot_drift`

Old text:

```
HANDLER_KEY = "audit.duplicates"
```

New text:

```
HANDLER_KEY = "duplicates.audit"
```

### `D1_probe_creates`

Round 1 zero, re-run against the replacement guard: take the creating default

- File: `src/cratekit/cli/doctor.py`
- Surface: user
- Subset: test files importing cratekit.cli.doctor
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 945 against a baseline of 945
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_trash_check_cannot_pass_by_having_run`

Old text:

```
    return trash.probe(path, create=False)
```

New text:

```
    return trash.probe(path, create=True)
```

