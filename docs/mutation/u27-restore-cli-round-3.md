# Mutation table: u27-restore-cli-round-3

Measured by `scripts/mutate.py` on 2026-08-23 23:38 UTC, branch `unit/u27-restore-cli` at `e2dd532`. Pass kind: full.

Baseline: green, 6190 collected. pytest invocations for this batch: 4.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6190 against 6190. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `S5_the_off_machine_half_runs_second` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 23 | 1 | killed |

## Row definitions

### `S5_the_off_machine_half_runs_second`

Pull the mirror AFTER the capture restore, so the remote overwrites the session just restored

- File: `src/cratekit/session/restore_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_the_mirror_is_pulled_before_the_capture_is_spent`

Old text:

```
        transferred: tuple[str, ...] = ()
        if from_backup:
```

New text:

```
        transferred: tuple[str, ...] = ()
        if session_id is not None and from_backup:
            decided = restore.plan(cfg, session_id, held=held, discarding=discarding)
            restore.run(decided, cfg, held=held, dry_run=dry_run)
        if from_backup:
```

