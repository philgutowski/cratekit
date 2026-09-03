# Mutation table: u55-round-2

Measured by `scripts/mutate.py` on 2026-09-03 01:22 UTC, branch `relay/73` at `b8fd94e`. Pass kind: full.

Baseline: green, 6675 collected. pytest invocations for this batch: 19.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6675 against 6675. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `R2_reader_unlock_probe` | `src/cratekit/adopt/collection.py` | user | 3 file(s) | 6675 | 0 (promoted) | zero |
| `R5_cache_key_resolved` | `src/cratekit/adopt/collection.py` | maintainer | 3 file(s) | 6675 | 0 (promoted) | zero |
| `R6_unlock_probe_answer` | `src/cratekit/core/rb_writer.py` | user | 21 file(s) | 6675 | 0 (promoted) | zero |
| `R8_census_prefix_map` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 49 | 1 | killed |
| `R16_apply_no_items_refusal` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 49 | 1 | killed |
| `R17_scan_r225_predicate` | `src/cratekit/adopt/scan_cli.py` | user | 1 file(s) | 25 | 1 | killed |
| `R18_apply_r225_predicate` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 49 | 1 | killed |
| `R23_worker_raises_on_failure` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 49 | 1 | killed |
| `R26_apply_write_intent_open` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 6675 | 0 (promoted) | zero |

## Zero rows and what they owe

- `R2_reader_unlock_probe` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `R5_cache_key_resolved` (maintainer facing): maintainer facing, composite not required
- `R6_unlock_probe_answer` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `R26_apply_write_intent_open` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `R2_reader_unlock_probe`

The reader assumes the file is never encrypted rather than asking the bytes

- File: `src/cratekit/adopt/collection.py`
- Surface: user
- Subset: test files importing cratekit.adopt.collection
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_workers.py`
- Collected: 6675 against a baseline of 6675
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        unlock=rb_writer.unlock_needed(target),
```

New text:

```
        unlock=False,
```

### `R5_cache_key_resolved`

Key the reader cache on the raw path rather than the resolved absolute one

- File: `src/cratekit/adopt/collection.py`
- Surface: maintainer
- Subset: test files importing cratekit.adopt.collection
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_workers.py`
- Collected: 6675 against a baseline of 6675
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    key = str(Path(target).resolve())
```

New text:

```
    key = str(target)
```

### `R6_unlock_probe_answer`

The encryption probe answers a constant, so a real library opens with the key off

- File: `src/cratekit/core/rb_writer.py`
- Surface: user
- Subset: test files importing cratekit.core.rb_writer
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`, `tests/test_process_guard.py`, `tests/test_queued_resume_contract.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_session_cli.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 6675 against a baseline of 6675
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        with Path(path).open("rb") as handle:
            return not handle.read(len(SQLITE_HEADER)).startswith(SQLITE_HEADER)
```

New text:

```
        with Path(path).open("rb") as handle:
            handle.read(len(SQLITE_HEADER))
            return False
```

### `R8_census_prefix_map`

The census drops the configured volume rewrites, so an older volume name resolves nowhere

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: test files importing cratekit.adopt.apply_cli
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 49 against a baseline of 49
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_configured_volume_rewrite_reaches_the_census`

Old text:

```
            prefix_map=collection.prefix_rules(cfg),
        )
    )
```

New text:

```
            prefix_map=(),
        )
    )
```

### `R16_apply_no_items_refusal`

The same guard on the apply resume branch

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: test files importing cratekit.adopt.apply_cli
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 49 against a baseline of 49
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_an_apply_job_queued_with_no_items_refuses_rather_than_driving`

Old text:

```
            if not jobs.items(store, job.job_id):
                raise refuse(
                    "internal-error",
                    f"job {job.job_id} has no items to run, so driving it would "
                    f"report an adoption over a library it never touched. It was "
                    f"queued by a build that did not record what its items were",
                    remedy=Remedy.REPORT_DEFECT,
                    origin=("adopt", "apply_cli"),
                    detail={"job_id": job.job_id},
                )

```

New text:

```
(empty)
```

### `R17_scan_r225_predicate`

R-225 narrowed: a run stopped by a signal is CANCELLED and would report OK

- File: `src/cratekit/adopt/scan_cli.py`
- Surface: user
- Subset: test files importing cratekit.adopt.scan_cli
- Ran: `tests/test_adopt_workers.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_an_interrupted_job_exits_with_its_own_cause_and_not_ok[adopt.scan]`

Old text:

```
        if not job.is_open() and job.cause is not None:
            raise CratekitError(job.cause)
        reported = _reported(store, job)
```

New text:

```
        if job.state is jobs.JobState.FAILED:
            raise CratekitError(job.cause)
        reported = _reported(store, job)
```

### `R18_apply_r225_predicate`

The same predicate on the applys resume branch

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: test files importing cratekit.adopt.apply_cli
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 49 against a baseline of 49
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_an_interrupted_job_exits_with_its_own_cause_and_not_ok[adopt.apply]`

Old text:

```
        if not job.is_open() and job.cause is not None:
            raise CratekitError(job.cause)
        reported = _reported(store, job)
```

New text:

```
        if job.state is jobs.JobState.FAILED:
            raise CratekitError(job.cause)
        reported = _reported(store, job)
```

### `R23_worker_raises_on_failure`

A failed apply returns rather than raising, so the job reaches SUCCEEDED over nothing

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: test files importing cratekit.adopt.apply_cli
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 49 against a baseline of 49
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_an_apply_whose_entries_failed_raises_rather_than_reporting_success`

Old text:

```
    if report.failed:
        _commit(produced)
        raise refuse(
```

New text:

```
    if False:
        _commit(produced)
        raise refuse(
```

### `R26_apply_write_intent_open`

The applys own handle drops its write intent, so rekordbox may be running under it

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: test files importing cratekit.adopt.apply_cli
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 6675 against a baseline of 6675
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        require_closed=True,
```

New text:

```
        require_closed=False,
```

