# Mutation table: u222-zeros

Measured by `scripts/mutate.py` on 2026-11-05 23:52 UTC, branch `cloud/552-the-account-mirror-s-apply-after` at `7c2e23e4`. Pass kind: light.

Baseline: green, 16816 collected. pytest invocations for this batch: 9.

Known failures: 161 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 16816 against 16816. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `M4_freeze_recorded_after` | `src/cratekit/organize/account_mirror.py` | maintainer | 6 file(s) | 16816 | 0 (promoted) | zero |
| `M5_agreed_none_lost` | `src/cratekit/organize/mirror_frozen.py` | user | 6 file(s) | 247 | 1 | killed |
| `M18_label_no_folder` | `src/cratekit/organize/mirror_frozen.py` | user | 6 file(s) | 247 | 1 | killed |
| `M24_cli_any_code_reworded` | `src/cratekit/organize/cli.py` | maintainer | 6 file(s) | 16816 | 0 (promoted) | zero |

## Zero rows and what they owe

- `M4_freeze_recorded_after` (maintainer facing): maintainer facing, composite not required
- `M24_cli_any_code_reworded` (maintainer facing): maintainer facing, composite not required

## Row definitions

### `M4_freeze_recorded_after`

_record: freeze the ledger after the gate's own plan time record, not the snapshot the plan read

- File: `src/cratekit/organize/account_mirror.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 16816 against a baseline of 16816
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            recorded=reading.recorded,
```

New text:

```
            recorded=ledger.mirror_folders(cfg),
```

### `M5_agreed_none_lost`

_agreed_json: freeze a never agreed snapshot as an empty one

- File: `src/cratekit/organize/mirror_frozen.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 247 against a baseline of 247
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_never_agreed_snapshot_is_frozen_and_read_back_as_never_agreed`

Old text:

```
            title: [one.remote_id, None if one.agreed is None else sorted(one.agreed)]
```

New text:

```
            title: [one.remote_id, sorted(one.agreed or ())]
```

### `M18_label_no_folder`

_label: read no folder line, so a folder that moved is never named

- File: `src/cratekit/organize/mirror_frozen.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 247 against a baseline of 247
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_label_step_that_moved_is_named_by_its_folder_line`

Old text:

```
    for key in ("playlist", "folder"):
```

New text:

```
    for key in ("playlist",):
```

### `M24_cli_any_code_reworded`

_ask: reword any refusal of a decided area, whatever its code

- File: `src/cratekit/organize/cli.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 16816 against a baseline of 16816
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if exc.cause.code != ExitCode.DECISION_STALE or not area.stale:
```

New text:

```
        if not area.stale:
```

