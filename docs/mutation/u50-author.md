# Mutation table: u50-author

Measured by `scripts/mutate.py` on 2026-09-02 10:45 UTC, branch `relay/68` at `995c985`. Pass kind: light.

Baseline: green, 6577 collected. pytest invocations for this batch: 21.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6577 against 6577. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `B1_no_items_enqueued` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 44 | 7 | killed |
| `B2_items_hardcoded_pair` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 6577 | 0 (promoted) | zero |
| `B3_items_one_portion_only` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 44 | 5 | killed |
| `B4_resume_does_not_drive` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 44 | 5 | killed |
| `B5_failed_job_exits_ok` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 44 | 1 | killed |
| `B6_ages_dropped_from_envelope` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 44 | 1 | killed |
| `W1_no_narrowing` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 44 | 3 | killed |
| `W2_narrow_to_the_wrong_half` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 44 | 6 | killed |
| `W3_refusal_suppressed` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 44 | 5 | killed |
| `W4_portion_from_the_payload` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 6577 | 0 (promoted) | zero |
| `W5_unknown_portion_unchecked` | `src/cratekit/backup/cli.py` | maintainer | 1 file(s) | 44 | 1 | killed |
| `W6_fresh_config_in_the_handler` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 44 | 2 | killed |
| `W7_runner_bound_at_definition` | `src/cratekit/backup/cli.py` | maintainer | 1 file(s) | 44 | 1 | killed |
| `W8_read_back_inside_the_item` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 6577 | 0 (promoted) | zero |
| `W9_handler_returns_an_artifact` | `src/cratekit/backup/cli.py` | maintainer | 1 file(s) | 44 | 6 | killed |

## Zero rows and what they owe

- `B2_items_hardcoded_pair` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `W4_portion_from_the_payload` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `W8_read_back_inside_the_item` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

### What was done about them, and it was not pairing

**All three are settled in `docs/mutation/u50-zero-rows.md`, measured after this
table and on the same branch.** Two were a real gap and one was a weak row, and
telling those apart is the reason a zero gets read rather than excused.

- `B2_items_hardcoded_pair` was a GAP. Replacing the derivation with the literal
  pair killed nothing across all 6577 tests, because every assertion about the
  item set compared it against `backup_facts.Portion`, and the literal and the
  derivation agree on any build with exactly these two portions. Closed by
  `test_the_item_list_is_derived_from_the_portions_rather_than_written_out`,
  which stands in a three member enum, the one condition a literal cannot follow.
  Re-measured: 1 kill.
- `W8_read_back_inside_the_item` was a GAP. Nothing drove the handler against an
  unreadable fact file, so the read back guard was asserted on the work body and
  unmeasured at the seam that asks for it. Closed by
  `test_the_handler_does_not_fail_an_item_over_the_age_read_back`. Re-measured:
  1 kill.
- `W4_portion_from_the_payload` was an INERT ROW rather than a gap, and it is
  reclassified rather than paired. It read `payload["portion"]` with a fallback to
  the item, and no payload this build writes carries that key, so the mutated code
  and the original take the same branch on every input. A row that cannot change
  behaviour cannot be killed and proves nothing about coverage. Replaced by
  `W4b_item_ignored_entirely`, which ignores the item outright and is the defect
  the original was reaching for. Measured: 4 kills.

## Considered and dropped

METHOD caps a light pass at 25 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `B7_reconcile_dropped`: Skip jobs.reconcile before the drive, so a claim left by a dead driver is never released Dropped because: ranked below the cap: jobs.drive releases orphaned claims itself under the driver lock, so removing the shell's reconcile is covered by the engine and would measure U46's guard rather than this unit's
- `B8_is_open_guard_dropped`: Drive without checking job.is_open, so a terminal job is re-driven Dropped because: ranked below the cap: jobs.drive refuses a terminal state by name, so the shell's guard only chooses which error the person sees and the engine's refusal is already measured elsewhere
- `W10_dry_run_flag_dropped`: Stop putting dry_run on the report Dropped because: ranked below the cap: the queued path discards the report entirely, which is R-221, so this row would measure the unqueued caller's guard that U45 already landed

## Row definitions

### `B1_no_items_enqueued`

Queue the backup with no items, so the driver has nothing to claim and reports an empty success

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 44 against a baseline of 44
- Kills: 7 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_backup_job_carries_one_item_per_declared_portion`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_job_in_which_nothing_ran_never_reports_success`
  - `tests/test_backup_cli.py::test_a_queued_backup_runs_every_portion_through_the_real_resume`
  - `tests/test_backup_cli.py::test_queueing_still_needs_nothing_from_the_machine`
  - `tests/test_backup_cli.py::test_the_age_a_driven_run_publishes_is_the_engine_s_and_reaches_the_envelope`
  - `tests/test_backup_cli.py::test_the_configuration_the_worker_runs_against_is_the_frozen_one`

Old text:

```
            item_ids=backup_items(),
```

New text:

```
(empty)
```

### `B2_items_hardcoded_pair`

Name the two portions instead of deriving them, so a third portion is queued by nobody

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 6577 against a baseline of 6577
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return tuple(str(portion) for portion in backup_facts.Portion)
```

New text:

```
    return ("files", "database")
```

### `B3_items_one_portion_only`

Queue only the mirror, so the database half of every backup is never claimed

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 44 against a baseline of 44
- Kills: 5 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_backup_job_carries_one_item_per_declared_portion`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_queued_backup_runs_every_portion_through_the_real_resume`
  - `tests/test_backup_cli.py::test_queueing_still_needs_nothing_from_the_machine`
  - `tests/test_backup_cli.py::test_the_age_a_driven_run_publishes_is_the_engine_s_and_reaches_the_envelope`

Old text:

```
    return tuple(str(portion) for portion in backup_facts.Portion)
```

New text:

```
    return (str(backup_facts.Portion.FILES),)
```

### `B4_resume_does_not_drive`

Report the queued job on resume without running any of it, which is the state R-198 describes

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 44 against a baseline of 44
- Kills: 5 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_job_in_which_nothing_ran_never_reports_success`
  - `tests/test_backup_cli.py::test_a_queued_backup_runs_every_portion_through_the_real_resume`
  - `tests/test_backup_cli.py::test_the_age_a_driven_run_publishes_is_the_engine_s_and_reaches_the_envelope`
  - `tests/test_backup_cli.py::test_the_configuration_the_worker_runs_against_is_the_frozen_one`

Old text:

```
                _, warnings = ctx.run_job(store, job)
                job = jobs.get(store, job.job_id)
```

New text:

```
(empty)
```

### `B5_failed_job_exits_ok`

Drop the re-raise, so a resume whose mirror completed and whose database failed exits 0

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`

Old text:

```
                if not job.is_open() and job.cause is not None:
                    raise CratekitError(job.cause)
```

New text:

```
(empty)
```

### `B6_ages_dropped_from_envelope`

Stop reporting the ages, so a person who just drove a backup cannot see what a destructive session would

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_age_a_driven_run_publishes_is_the_engine_s_and_reaches_the_envelope`

Old text:

```
            reported["ages"] = published_ages(cfg)
```

New text:

```
(empty)
```

### `W1_no_narrowing`

Ignore the portion and run the whole plan for every item, so each item does the whole backup

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 44 against a baseline of 44
- Kills: 3 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_named_portion_runs_only_its_own_half`
  - `tests/test_backup_cli.py::test_a_portion_the_engine_refused_fails_rather_than_reporting_a_copy`

Old text:

```
    if portion is not None:
```

New text:

```
    if False:
```

### `W2_narrow_to_the_wrong_half`

Always narrow to the mirror, so the database item copies the files again and the database never

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 44 against a baseline of 44
- Kills: 6 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_named_portion_runs_only_its_own_half`
  - `tests/test_backup_cli.py::test_a_narrowed_portion_whose_transfer_failed_refuses_by_that_portion`
  - `tests/test_backup_cli.py::test_a_portion_the_engine_refused_fails_rather_than_reporting_a_copy`
  - `tests/test_backup_cli.py::test_a_queued_backup_runs_every_portion_through_the_real_resume`
  - `tests/test_backup_cli.py::test_the_age_a_driven_run_publishes_is_the_engine_s_and_reaches_the_envelope`

Old text:

```
            portions=(plan.portion(portion),),
```

New text:

```
            portions=(plan.portion(backup_facts.Portion.FILES),),
```

### `W3_refusal_suppressed`

The first draft's rule: complete the item when another portion will run, which records a portion nothing copied as done for ever

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 44 against a baseline of 44
- Kills: 5 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_job_in_which_nothing_ran_never_reports_success`
  - `tests/test_backup_cli.py::test_a_machine_with_no_rclone_fails_every_portion_by_name`
  - `tests/test_backup_cli.py::test_a_machine_with_no_rclone_refuses_by_name`
  - `tests/test_backup_cli.py::test_a_portion_the_engine_refused_fails_rather_than_reporting_a_copy`
  - `tests/test_backup_cli.py::test_two_portions_refused_for_different_reasons_name_both`

Old text:

```
    refusal = refusal_for(outcome)
    if refusal is not None:
        raise refusal
```

New text:

```
    refusal = refusal_for(outcome)
    if refusal is not None and not any(
        entry.refusal is not None for entry in outcome.portions
    ):
        raise refusal
```

### `W4_portion_from_the_payload`

Read the portion from the payload rather than from the item the driver claimed

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 6577 against a baseline of 6577
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    named = str(item.item_id or "")
```

New text:

```
    named = str((job.payload or {}).get("portion") or item.item_id or "")
```

### `W5_unknown_portion_unchecked`

Let an undeclared item name raise out of the coercion rather than refusing by name

- File: `src/cratekit/backup/cli.py`
- Surface: maintainer
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_an_item_naming_something_that_is_not_a_portion_refuses_by_name`

Old text:

```
        raise refuse(
            "internal-error",
            f"this job's item is {named!r}, which is not a backup portion this "
            f"build declares. The portions are {', '.join(declared)}",
```

New text:

```
        raise refuse(
            "internal-error",
            "the item could not be read",
```

### `W6_fresh_config_in_the_handler`

Load the configuration in the handler rather than using the one frozen on the job (KTD9)

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 44 against a baseline of 44
- Kills: 2 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_configuration_the_worker_runs_against_is_the_frozen_one`
  - `tests/test_backup_cli.py::test_the_handler_uses_the_configuration_it_was_handed`

Old text:

```
        cfg=cfg,
        # RESOLVED AT CALL TIME, not left to the default, so a test can put a
        # stand-in in front of it. ``perform_backup``'s own default is bound when
        # this module is imported and cannot be reached any other way.
        runner=backup.subprocess_runner,
```

New text:

```
        cfg=_load(),
        runner=backup.subprocess_runner,
```

### `W7_runner_bound_at_definition`

Let the runner default apply, binding the transfer program at import so a stand-in cannot reach it

- File: `src/cratekit/backup/cli.py`
- Surface: maintainer
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`

Old text:

```
        runner=backup.subprocess_runner,
        read_back=False,
    )
```

New text:

```
        read_back=False,
    )
```

### `W8_read_back_inside_the_item`

Read the age back under the driver, so an unreadable fact file fails an item over a rehearsal that copied nothing

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 6577 against a baseline of 6577
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        read_back=False,
    )
    return None
```

New text:

```
    )
    return None
```

### `W9_handler_returns_an_artifact`

Return a Produced naming the library root, so the engine tries to commit a path no backup staged

- File: `src/cratekit/backup/cli.py`
- Surface: maintainer
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 44 against a baseline of 44
- Kills: 6 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_queued_backup_runs_every_portion_through_the_real_resume`
  - `tests/test_backup_cli.py::test_a_resume_reports_the_queued_job_rather_than_filing_a_second`
  - `tests/test_backup_cli.py::test_the_age_a_driven_run_publishes_is_the_engine_s_and_reaches_the_envelope`
  - `tests/test_backup_cli.py::test_the_configuration_the_worker_runs_against_is_the_frozen_one`
  - `tests/test_backup_cli.py::test_the_handler_uses_the_configuration_it_was_handed`

Old text:

```
        read_back=False,
    )
    return None
```

New text:

```
        read_back=False,
    )
    return jobs.Produced(staged=cfg.library.root, final=cfg.library.root)
```

