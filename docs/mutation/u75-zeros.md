# Mutation table: u75-zeros

Measured by `scripts/mutate.py` on 2026-09-19 06:50 UTC, branch `relay/120` at `1c51cb0`. Pass kind: light.

Baseline: green, 8108 collected. pytest invocations for this batch: 5.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 8108 against 8108. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `A8_identity_before_payload` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 150 | 1 | killed |
| `B6_missing_and_nothing_listable_refuses` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 150 | 1 | killed |

## Row definitions

### `A8_identity_before_payload`

Read the release identifier from the payload first, not from the item's identity

- File: `src/cratekit/label/approved_cli.py`
- Surface: user
- Subset: test files importing cratekit.label.approved_cli
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 150 against a baseline of 150
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_the_items_identity_names_the_release_and_a_payload_that_disagrees_does_not`

Old text:

```
    release_id = _text(identity.get("release_id")) or _text(item.payload.get("identity")) or ""
```

New text:

```
    release_id = _text(item.payload.get("identity")) or _text(identity.get("release_id")) or ""
```

### `B6_missing_and_nothing_listable_refuses`

Remove the refusal for missing tracks none of which carries a provider identifier

- File: `src/cratekit/label/approved_cli.py`
- Surface: user
- Subset: test files importing cratekit.label.approved_cli
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 150 against a baseline of 150
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_missing_tracks_none_of_which_can_be_asked_for_is_refused_and_not_a_no_op`

Old text:

```
    if missing and not listed:
```

New text:

```
    if False:
```

