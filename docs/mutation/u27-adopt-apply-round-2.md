# Mutation table: u27-adopt-apply-round-2

Measured by `scripts/mutate.py` on 2026-08-23 18:36 UTC, branch `unit/u27-adopt-apply-cli` at `60441e9`. Pass kind: full.

Baseline: green, 6150 collected. pytest invocations for this batch: 6.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6150 against 6150. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `S3_watched_root_is_narrower_than_the_library` | `src/cratekit/adopt/apply_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `G3_gate_offers_no_digest` | `src/cratekit/adopt/apply_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `G5_resume_does_not_reconcile` | `src/cratekit/adopt/apply_cli.py` | user | 1 file(s) | 22 | 1 | killed |

## Row definitions

### `S3_watched_root_is_narrower_than_the_library`

Watch only the Music folder, so a tag write outside it is unwatched

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_the_analysis_watch_is_armed_on_the_library_root`

Old text:

```
    watched: tuple[Path, ...] = (cfg.library.root,)
```

New text:

```
    watched: tuple[Path, ...] = (cfg.library.root / "Music",)
```

### `G3_gate_offers_no_digest`

Ask the approval gate with no digest, so an approval survives the plan moving

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_an_approval_recorded_against_a_plan_that_has_since_moved_is_refused`

Old text:

```
    option = ctx.gate.require(spec, digest=plan.digest())
```

New text:

```
    option = ctx.gate.require(spec)
```

### `G5_resume_does_not_reconcile`

Report the stored job without reconciling a claim a dead driver left behind

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_a_resume_reconciles_a_claim_a_dead_driver_left_behind`

Old text:

```
            return ctx.envelope(data=_reported(store, jobs.reconcile(store, ctx.args.job)))
```

New text:

```
            return ctx.envelope(data=_reported(store, jobs.get(store, ctx.args.job)))
```

