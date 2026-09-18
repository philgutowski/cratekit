# Mutation table: u67-round-2

Measured by `scripts/mutate.py` on 2026-09-18 22:41 UTC, branch `relay/112` at `5780f5c`. Pass kind: light.

Baseline: green, 7699 collected. pytest invocations for this batch: 5.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 7699 against 7699. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `E1_claim_target` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `C1_action_filter_and_recheck` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 40 | 11 | killed |

## Row definitions

### `E1_claim_target`

Existing: rename over a target another file already holds

- File: `src/cratekit/write/naming_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_rename_onto_a_name_another_file_holds_overwrites_nothing`

Old text:

```
            if not naming.claim_target(target):
                continue
```

New text:

```
            if False:
                continue
```

### `C1_action_filter_and_recheck`

Composite: apply every plan item AND drop the re-check before the rename

- File: `src/cratekit/write/naming_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 11 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_case_variant_of_the_name_still_protects_its_file`
  - `tests/test_naming_apply_cli.py::test_a_composition_variant_of_the_name_still_protects_its_file[NFC]`
  - `tests/test_naming_apply_cli.py::test_a_composition_variant_of_the_name_still_protects_its_file[NFD]`
  - `tests/test_naming_apply_cli.py::test_a_file_recorded_by_its_real_path_is_protected_through_a_linked_root`
  - `tests/test_naming_apply_cli.py::test_a_file_recorded_through_a_link_is_protected_through_that_link`
  - `tests/test_naming_apply_cli.py::test_a_referenced_file_is_untouched_and_its_sibling_is_renamed`
  - `tests/test_naming_apply_cli.py::test_a_root_outside_the_library_is_still_checked`
  - `tests/test_naming_apply_cli.py::test_a_row_recorded_as_a_location_url_protects_its_file`
  - `tests/test_naming_apply_cli.py::test_a_row_that_appears_after_the_gate_still_protects_its_file`
  - `tests/test_naming_apply_cli.py::test_a_row_under_a_remapped_volume_still_protects_its_file[prefix_map0]`
  - `tests/test_naming_apply_cli.py::test_a_tombstoned_row_still_protects_its_file`

Old text:

```
    renames = [item for item in plan["items"] if item["action"] == RENAME]
```

New text:

```
    renames = list(plan["items"])
    _is_referenced = lambda path, referenced: False  # noqa: E731
```

