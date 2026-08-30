# Mutation table: u45-round-1

Measured by `scripts/mutate.py` on 2026-08-30 02:18 UTC, branch `unit/u45-the-backup-run-shell-and-the-age-the-wri` at `2548aca`. Pass kind: full.

Baseline: green, 6437 collected. pytest invocations for this batch: 55.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6437 against 6437. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `C1_failed_portion_ignored` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 21 | 4 | killed |
| `C2_refusal_read_as_failure` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 21 | 4 | killed |
| `C3_nothing_ran_accepted` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 21 | 3 | killed |
| `C4_uniform_refusal_flattened` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 21 | 1 | killed |
| `C5_first_refusal_taken` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 21 | 1 | killed |
| `C6_partial_run_refused` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 21 | 3 | killed |
| `C7_failed_detail_dropped` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 6437 | 0 (promoted) | zero |
| `W1_refusal_not_raised` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 21 | 5 | killed |
| `W2_report_from_the_plan` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 21 | 3 | killed |
| `W3_ages_not_read_back` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 21 | 2 | killed |
| `W4_ages_derived_from_the_outcome` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 21 | 1 | killed |
| `W5_publishing_switched_off` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 21 | 3 | killed |
| `W6_rehearsal_becomes_a_real_run` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 21 | 1 | killed |
| `W7_dry_run_flag_off_the_report` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 21 | 1 | killed |
| `W8_engine_refusal_escapes` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 21 | 1 | killed |
| `W9_process_lister_dropped` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 21 | 1 | killed |
| `R1_reserved_remediation_discarded` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 21 | 2 | killed |
| `R2_slug_flattened` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 21 | 1 | killed |
| `A1_unreadable_reported_as_absent` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 21 | 2 | killed |
| `A2_remedy_fixed_at_repair` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 21 | 1 | killed |
| `A3_age_seconds_always_none` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 6437 | 0 (promoted) | zero |
| `A4_state_collapsed_to_known` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 21 | 1 | killed |
| `Q1_resume_drops_the_rehearsal` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 21 | 2 | killed |
| `Q2_resume_always_rehearses` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 21 | 1 | killed |
| `Q3_resume_loses_the_job` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 21 | 1 | killed |
| `Q4_payload_key_not_read` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 21 | 1 | killed |
| `H1_flag_never_frozen` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 21 | 1 | killed |
| `H2_queueing_plans_first` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 21 | 1 | killed |
| `H3_resume_branch_dropped` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 6437 | 0 (promoted) | zero |
| `H4_payload_not_coerced` | `src/cratekit/backup/cli.py` | maintainer | 1 file(s) | 6437 | 0 (promoted) | zero |
| `V1_transfer_failure_is_a_defect` | `src/cratekit/core/cause.py` | user | 33 file(s) | 3795 | 1 | killed |
| `V2_summary_slug_undeclared` | `src/cratekit/core/cause.py` | user | 33 file(s) | 3795 | 3 | killed |
| `V3_marker_restored` | `src/cratekit/cli/registry.py` | user | 24 file(s) | 2985 | collection error | collect-error |
| `V4_argv_builder_dropped` | `src/cratekit/cli/registry.py` | user | 24 file(s) | 105 | collection error | collect-error |
| `V5_module_toggle_dropped` | `src/cratekit/cli/registry.py` | user | 24 file(s) | 2987 | 5 | killed |
| `E1_rehearsal_publishes` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 408 | 2 | killed |
| `E2_publish_unconditional` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 408 | 2 | killed |
| `E3_failed_portion_marked_ran` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 408 | 4 | killed |
| `E4_return_codes_unread` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 408 | 5 | killed |
| `E5_outcome_ok_widened` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 6437 | 0 (promoted) | zero |
| `E6_future_tolerance_reversed` | `src/cratekit/core/backup_facts.py` | user | 5 file(s) | 714 | 3 | killed |
| `E7_record_overwrites_the_file` | `src/cratekit/core/backup_facts.py` | user | 5 file(s) | 714 | 5 | killed |
| `E8_naive_timestamp_stored` | `src/cratekit/core/backup_facts.py` | user | 5 file(s) | 714 | 1 | killed |

## Zero rows and what they owe

- `C7_failed_detail_dropped` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `A3_age_seconds_always_none` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `H3_resume_branch_dropped` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `H4_payload_not_coerced` (maintainer facing): maintainer facing, composite not required
- `E5_outcome_ok_widened` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Considered and dropped

METHOD caps a full pass at 45 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `D1_prune_keep_coefficient`: Halve DEFAULT_ARCHIVE_KEEP in the engine Dropped because: ranked below the cap: the shell never passes archive_keep, so the coefficient is not on this unit's diff and its guards belong to U35
- `D2_settings_directories`: Return an empty settings directory tuple from the engine Dropped because: ranked below the cap: platform probing the shell does not touch, and the shell passes no settings_dirs at all
- `D3_dry_run_argv_translator`: Return the real argv from dry_run_argv Dropped because: ranked below the cap: covered indirectly by W6 and E1, both of which reach the same user facing cost of a rehearsal that transfers
- `D4_oldest_usable_age`: Return the minimum age rather than the maximum Dropped because: ranked below the cap: oldest_usable_age has no caller this unit adds, so a finding there is not this round's to own
- `D5_load_config_translation`: Let ConfigError escape from _load Dropped because: ranked below the cap: identical in every shell in the package, measured on U42 and U44, and this copy adds nothing new to measure

## Row definitions

### `C1_failed_portion_ignored`

Drop the failed-portion branch entirely, so a run whose transfers came back non zero reports success

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 21 against a baseline of 21
- Kills: 4 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_portion_decides_the_run_even_when_the_other_completed`
  - `tests/test_backup_cli.py::test_a_failing_rehearsal_is_not_reported_as_a_passing_one`
  - `tests/test_backup_cli.py::test_a_run_whose_every_transfer_failed_publishes_no_age_at_all`
  - `tests/test_backup_cli.py::test_the_report_is_built_from_the_outcome_and_never_from_the_plan`

Old text:

```
    if failed:
        return refuse(
            "backup-transfer-failed",

```

New text:

```
    if False:
        return refuse(
            "backup-transfer-failed",

```

### `C2_refusal_read_as_failure`

Widen the failed predicate to any portion that did not run, so a refused database portion reads as a failed transfer

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 21 against a baseline of 21
- Kills: 4 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_machine_with_no_rclone_refuses_by_name`
  - `tests/test_backup_cli.py::test_a_partial_run_succeeds_and_publishes_only_the_half_that_ran`
  - `tests/test_backup_cli.py::test_nothing_that_ran_is_never_reported_as_a_refusal`
  - `tests/test_backup_cli.py::test_two_portions_refused_for_different_reasons_name_both`

Old text:

```
        entry for entry in outcome.portions if not entry.ran and entry.refusal is None
```

New text:

```
        entry for entry in outcome.portions if not entry.ran
```

### `C3_nothing_ran_accepted`

Return None when no portion ran, so a machine with no rclone exits OK over a backup that did not happen

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 21 against a baseline of 21
- Kills: 3 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_machine_with_no_rclone_refuses_by_name`
  - `tests/test_backup_cli.py::test_an_outcome_with_no_portions_refuses_rather_than_raising`
  - `tests/test_backup_cli.py::test_two_portions_refused_for_different_reasons_name_both`

Old text:

```
    if any(entry.ran for entry in outcome.portions):
        return None
    refusals
```

New text:

```
    return None
    refusals
```

### `C4_uniform_refusal_flattened`

Drop the uniform pass-through so every no-run refusal becomes the summary slug and rclone-missing loses install-binary

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 21 against a baseline of 21
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_machine_with_no_rclone_refuses_by_name`

Old text:

```
    if len(refusals) == 1:
        only = next(iter(refusals))
```

New text:

```
    if False:
        only = next(iter(refusals))
```

### `C5_first_refusal_taken`

Take the first portion's refusal when the reasons differ, rather than naming all of them

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 21 against a baseline of 21
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_two_portions_refused_for_different_reasons_name_both`

Old text:

```
    if len(refusals) == 1:
```

New text:

```
    if refusals:
```

### `C6_partial_run_refused`

Refuse whenever any portion did not run, so a mirror that completed while the database was skipped is reported as a failure

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 21 against a baseline of 21
- Kills: 3 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_partial_run_succeeds_and_publishes_only_the_half_that_ran`
  - `tests/test_backup_cli.py::test_an_outcome_with_no_portions_refuses_rather_than_raising`
  - `tests/test_backup_cli.py::test_nothing_that_ran_is_never_reported_as_a_refusal`

Old text:

```
    if any(entry.ran for entry in outcome.portions):
        return None
```

New text:

```
    if all(entry.ran for entry in outcome.portions):
        return None
```

### `C7_failed_detail_dropped`

Reword the transfer-failed message so it no longer says a destructive session still sees the previous age

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 6437 against a baseline of 6437
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            + ". No backup age was published for that portion, so a destructive "
            "session still sees whatever the last successful run left",
```

New text:

```
            + ". The run stopped there.",
```

### `W1_refusal_not_raised`

Build the report anyway when the run earned a refusal, so a failed backup returns a payload instead of refusing

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 21 against a baseline of 21
- Kills: 5 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failing_rehearsal_is_not_reported_as_a_passing_one`
  - `tests/test_backup_cli.py::test_a_machine_with_no_rclone_refuses_by_name`
  - `tests/test_backup_cli.py::test_a_run_whose_every_transfer_failed_publishes_no_age_at_all`
  - `tests/test_backup_cli.py::test_the_report_is_built_from_the_outcome_and_never_from_the_plan`
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
    del refusal
```

### `W2_report_from_the_plan`

Report the PLAN rather than the OUTCOME, which is the shell half of the first-caller defect

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 21 against a baseline of 21
- Kills: 3 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_partial_run_succeeds_and_publishes_only_the_half_that_ran`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`
  - `tests/test_backup_cli.py::test_a_run_that_succeeded_publishes_an_age_the_session_reads_back`

Old text:

```
    report = backup.outcome_payload(outcome)
```

New text:

```
    report = backup.plan_payload(plan)
```

### `W3_ages_not_read_back`

Drop the age read-back, so the verb never reports what a destructive session would see

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 21 against a baseline of 21
- Kills: 2 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`
  - `tests/test_backup_cli.py::test_a_run_that_succeeded_publishes_an_age_the_session_reads_back`

Old text:

```
    report["ages"] = published_ages(cfg, now=now)
```

New text:

```
    report["ages"] = []
```

### `W4_ages_derived_from_the_outcome`

Derive the published ages from the outcome instead of reading the fact file, the duplicate rule the module argues against

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 21 against a baseline of 21
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`

Old text:

```
    report["ages"] = published_ages(cfg, now=now)
```

New text:

```
    report["ages"] = [
        {"portion": p.portion.value, "state": "known" if p.ran else "never-recorded"}
        for p in outcome.portions
    ]
```

### `W5_publishing_switched_off`

Pass publish=False, so a successful backup records no age and the write session still sees never-recorded

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 21 against a baseline of 21
- Kills: 3 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_partial_run_succeeds_and_publishes_only_the_half_that_ran`
  - `tests/test_backup_cli.py::test_a_run_that_succeeded_publishes_an_age_the_session_reads_back`
  - `tests/test_backup_cli.py::test_a_supplied_configuration_is_used_rather_than_the_one_on_disk`

Old text:

```
    outcome = backup.run_backup(cfg, plan, runner=runner, now=now, dry_run=dry_run)
```

New text:

```
    outcome = backup.run_backup(
        cfg, plan, runner=runner, now=now, dry_run=dry_run, publish=False
    )
```

### `W6_rehearsal_becomes_a_real_run`

Ignore the frozen dry-run key, so a rehearsal transfers for real and publishes an age

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 21 against a baseline of 21
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`

Old text:

```
    dry_run = bool(payload.get(DRY_RUN))
```

New text:

```
    dry_run = False
```

### `W7_dry_run_flag_off_the_report`

Report every run as a real one, so a rehearsal and a real run are indistinguishable in the payload

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 21 against a baseline of 21
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`

Old text:

```
    report["dry_run"] = dry_run
```

New text:

```
    report["dry_run"] = False
```

### `W8_engine_refusal_escapes`

Let BackupRefused escape, so an unconfigured remote reaches the dispatcher as internal-error with report-defect

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 21 against a baseline of 21
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_an_unconfigured_remote_refuses_in_the_backup_vocabulary`

Old text:

```
    except backup.BackupRefused as exc:
        raise _engine_refusal(
            exc.refusal, exc.detail, library=str(cfg.library.root)
        ) from exc
```

New text:

```
    except backup.BackupRefused:
        raise
```

### `W9_process_lister_dropped`

Stop passing the process lister through, so the database gate probes this machine rather than the caller's answer

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 21 against a baseline of 21
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_partial_run_succeeds_and_publishes_only_the_half_that_ran`

Old text:

```
        plan = backup.plan_backup(cfg, now=now, process_lister=process_lister)
```

New text:

```
        plan = backup.plan_backup(cfg, now=now)
```

### `R1_reserved_remediation_discarded`

Replace the reservation table's per-slug remediation with the class default, which is what the first draft did

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 21 against a baseline of 21
- Kills: 2 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_machine_with_no_rclone_refuses_by_name`
  - `tests/test_backup_cli.py::test_an_unconfigured_remote_refuses_in_the_backup_vocabulary`

Old text:

```
            remediation=reservations.remediation_for(slug),
```

New text:

```
            remediation=Remediation(),
```

### `R2_slug_flattened`

Fold every engine refusal into one slug, so nine diagnoses arrive as one and each loses its own fix

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 21 against a baseline of 21
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_an_unconfigured_remote_refuses_in_the_backup_vocabulary`

Old text:

```
    slug = str(refusal)
    return CratekitError(
```

New text:

```
    slug = str(backup.Refusal.RCLONE_MISSING)
    return CratekitError(
```

### `A1_unreadable_reported_as_absent`

Return an empty list for an unreadable fact file, so a library with a good backup reads as never backed up

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 21 against a baseline of 21
- Kills: 2 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_fact_file_that_cannot_be_read_refuses_rather_than_reporting_nothing`
  - `tests/test_backup_cli.py::test_the_remedy_for_an_unreadable_fact_file_travels_from_the_exception`

Old text:

```
    except backup_facts.BackupFactsUnreadable as exc:
        raise refuse(
            "backup-facts-unreadable",
```

New text:

```
    except backup_facts.BackupFactsUnreadable as exc:
        del exc
        return []
        raise refuse(
            "backup-facts-unreadable",
```

### `A2_remedy_fixed_at_repair`

Fix the remedy at repair-backup-facts, so a permission on a directory tells a person to reset library state

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 21 against a baseline of 21
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_remedy_for_an_unreadable_fact_file_travels_from_the_exception`

Old text:

```
            remedy=Remedy(str(exc.remedy)),
            origin=("backup", "cli"),
```

New text:

```
            remedy=Remedy.REPAIR_BACKUP_FACTS,
            origin=("backup", "cli"),
```

### `A3_age_seconds_always_none`

Report no age number even for a known portion, so the value R15's warning quotes never reaches the report

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 6437 against a baseline of 6437
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            "age_seconds": entry.age.total_seconds() if entry.age is not None else None,
```

New text:

```
            "age_seconds": None,
```

### `A4_state_collapsed_to_known`

Report every portion as known, so never-recorded and recorded-in-the-future both read as a current backup

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 21 against a baseline of 21
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`

Old text:

```
            "state": str(entry.state),
            "age_seconds"
```

New text:

```
            "state": "known",
            "age_seconds"
```

### `Q1_resume_drops_the_rehearsal`

Drop --dry-run from the resume argv, so a queued rehearsal respawns as a real transfer that publishes an age

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 21 against a baseline of 21
- Kills: 2 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_frozen_payload_and_the_parser_agree_about_the_flag`
  - `tests/test_backup_cli.py::test_the_resume_rebuilds_the_rehearsal_flag_and_never_carries_a_run`

Old text:

```
    if payload.get(DRY_RUN):
        argv.append("--dry-run")
```

New text:

```
    pass
```

### `Q2_resume_always_rehearses`

Always emit --dry-run, the other direction, so a real backup respawns as a rehearsal that copies nothing

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 21 against a baseline of 21
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_resume_rebuilds_the_rehearsal_flag_and_never_carries_a_run`

Old text:

```
    if payload.get(DRY_RUN):
        argv.append("--dry-run")
```

New text:

```
    argv.append("--dry-run")
```

### `Q3_resume_loses_the_job`

Drop --job from the resume argv, so the child queues a second backup instead of continuing the first

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 21 against a baseline of 21
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_resume_rebuilds_the_rehearsal_flag_and_never_carries_a_run`

Old text:

```
    return [*argv, "--job", job.job_id]
```

New text:

```
    return list(argv)
```

### `Q4_payload_key_not_read`

Read a key the handler does not freeze, which is the drift the named constant exists to prevent

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 21 against a baseline of 21
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_resume_rebuilds_the_rehearsal_flag_and_never_carries_a_run`

Old text:

```
    if payload.get(DRY_RUN):
```

New text:

```
    if payload.get("dryrun"):
```

### `H1_flag_never_frozen`

Freeze False whatever was typed, so --dry-run parses and the queued job does a real backup

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 21 against a baseline of 21
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_frozen_payload_and_the_parser_agree_about_the_flag`

Old text:

```
            payload=frozen_payload(ctx.args.dry_run),
```

New text:

```
            payload=frozen_payload(False),
```

### `H2_queueing_plans_first`

Plan inside the handler, so queueing refuses on a machine with no rclone where the work would have run fine

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 21 against a baseline of 21
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_queueing_needs_no_rclone_no_remote_and_no_volume`

Old text:

```
    cfg = _load()
    with jobs.open_store() as store:
        if ctx.args.job:
```

New text:

```
    cfg = _load()
    backup.plan_backup(cfg)
    with jobs.open_store() as store:
        if ctx.args.job:
```

### `H3_resume_branch_dropped`

Always enqueue, so --job files a second backup rather than reporting the one already queued

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 6437 against a baseline of 6437
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if ctx.args.job:
            return ctx.envelope(data=_reported(store, jobs.reconcile(store, ctx.args.job)))
```

New text:

```
        if False:
            return ctx.envelope(data=_reported(store, jobs.reconcile(store, ctx.args.job)))
```

### `H4_payload_not_coerced`

Freeze the argparse value rather than a boolean, so a payload holding a truthy string reads as true to every reader

- File: `src/cratekit/backup/cli.py`
- Surface: maintainer
- Subset: test files importing cratekit.backup.cli
- Ran: `tests/test_backup_cli.py`
- Collected: 6437 against a baseline of 6437
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return {DRY_RUN: bool(dry_run)}
```

New text:

```
    return {DRY_RUN: dry_run}
```

### `V1_transfer_failure_is_a_defect`

Classify a failed transfer as INTERNAL, so an unreachable remote tells a person to report a bug

- File: `src/cratekit/core/cause.py`
- Surface: user
- Subset: test files importing cratekit.core.cause
- Ran: `tests/intake/test_collection_xml.py`, `tests/intake/test_pipeline.py`, `tests/modules/test_labels.py`, `tests/modules/test_outbound.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_incremental_sync.py`, `tests/test_jobs.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_review_queue.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_install.py`, `tests/test_snapshot.py`, `tests/test_tombstones.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 3795 against a baseline of 3795
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_run_whose_every_transfer_failed_publishes_no_age_at_all`

Old text:

```
        "backup-transfer-failed": ExitCode.PRECONDITION,
```

New text:

```
        "backup-transfer-failed": ExitCode.INTERNAL,
```

### `V2_summary_slug_undeclared`

Remove backup-nothing-ran from the registry, so its raise site raises UnknownReason at the boundary

- File: `src/cratekit/core/cause.py`
- Surface: user
- Subset: test files importing cratekit.core.cause
- Ran: `tests/intake/test_collection_xml.py`, `tests/intake/test_pipeline.py`, `tests/modules/test_labels.py`, `tests/modules/test_outbound.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_incremental_sync.py`, `tests/test_jobs.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_review_queue.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_install.py`, `tests/test_snapshot.py`, `tests/test_tombstones.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 3795 against a baseline of 3795
- Kills: 3 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_an_outcome_with_no_portions_refuses_rather_than_raising`
  - `tests/test_backup_cli.py::test_two_portions_refused_for_different_reasons_name_both`
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`

Old text:

```
        "backup-nothing-ran": ExitCode.PRECONDITION,
```

New text:

```
(empty)
```

### `V3_marker_restored`

Put planned_in back, so the verb reads as unlanded and every conformance property stops arming against it

- File: `src/cratekit/cli/registry.py`
- Surface: user
- Subset: test files importing cratekit.cli.registry
- Ran: `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_jobs.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_packaging.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_write_session.py`
- Collected: 2985 against a baseline of 2987
- Kills: 6 (collect-error)
- Note: collection changed: 2985 collected against a baseline of 2987. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_backup_cli.py::test_queueing_needs_no_rclone_no_remote_and_no_volume`
  - `tests/test_backup_cli.py::test_the_frozen_payload_and_the_parser_agree_about_the_flag`
  - `tests/test_backup_cli.py::test_the_verb_is_declared_landed_and_names_this_module`
  - `tests/test_cli_contract.py::test_a_planned_verb_whose_module_has_landed_must_lose_its_marker[backup.run]`
  - `tests/test_cutover_parity.py::test_the_cutover_is_mechanically_possible_and_says_what_is_left`
  - `tests/test_cutover_parity.py::test_the_parity_table_renders_for_a_person`

Old text:

```
        doctor_checks=("library.mounted", "binary.rclone"),
        # U45 LANDED IT.
```

New text:

```
        doctor_checks=("library.mounted", "binary.rclone"),
        planned_in="U35",
        # U45 LANDED IT.
```

### `V4_argv_builder_dropped`

Drop the argv builder, so a queued backup has no command line to respawn with

- File: `src/cratekit/cli/registry.py`
- Surface: user
- Subset: test files importing cratekit.cli.registry
- Ran: `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_jobs.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_packaging.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_write_session.py`
- Collected: 105 against a baseline of 2987
- Kills: 0 (collect-error)
- Note: collection changed: 105 collected against a baseline of 2987. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Collection errors: `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_write_session.py`

Old text:

```
        argv_builder="backup_argv",
        long_running=True,
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        doctor_checks=("library.mounted", "binary.rclone"),
```

New text:

```
        long_running=True,
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        doctor_checks=("library.mounted", "binary.rclone"),
```

### `V5_module_toggle_dropped`

Drop the module toggle, so the verb is offered on a slim install that has no backup module

- File: `src/cratekit/cli/registry.py`
- Surface: user
- Subset: test files importing cratekit.cli.registry
- Ran: `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_jobs.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_packaging.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_write_session.py`
- Collected: 2987 against a baseline of 2987
- Kills: 5 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_verb_is_declared_landed_and_names_this_module`
  - `tests/test_backup_cli.py::test_the_verb_is_offered_on_the_full_profile_and_withheld_on_the_slim_one`
  - `tests/test_cli_contract.py::test_every_declared_module_toggle_is_used_by_at_least_one_verb`
  - `tests/test_cli_contract.py::test_every_feature_row_maps_to_a_verb_at_its_stated_disposition`
  - `tests/test_doctor.py::test_a_binary_no_enabled_verb_needs_is_a_note_rather_than_a_failure`

Old text:

```
        source_scripts=("backup.sh",),
        module_id="backup",
```

New text:

```
        source_scripts=("backup.sh",),
```

### `E1_rehearsal_publishes`

Let a dry run publish, so a preview records a backup age for a run that copied not one byte

- File: `src/cratekit/modules/tools/backup.py`
- Surface: user
- Subset: test files importing cratekit.modules.tools.backup
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 408 against a baseline of 408
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_dry_run_publishes_no_backup_age`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`

Old text:

```
    if dry_run:
        publish = False
```

New text:

```
    pass
```

### `E2_publish_unconditional`

Publish regardless of the flag, the same hole reached from the other side

- File: `src/cratekit/modules/tools/backup.py`
- Surface: user
- Subset: test files importing cratekit.modules.tools.backup
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 408 against a baseline of 408
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_dry_run_publishes_no_backup_age`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`

Old text:

```
        if publish:
            backup_facts.record(
```

New text:

```
        if True:
            backup_facts.record(
```

### `E3_failed_portion_marked_ran`

Mark a failed portion as having run, so BackupOutcome.ok is true over a transfer that came back non zero

- File: `src/cratekit/modules/tools/backup.py`
- Surface: user
- Subset: test files importing cratekit.modules.tools.backup
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 408 against a baseline of 408
- Kills: 4 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_prune_runs_only_after_the_mirror_succeeded`
  - `tests/test_backup_cli.py::test_a_failing_rehearsal_is_not_reported_as_a_passing_one`
  - `tests/test_backup_cli.py::test_a_run_whose_every_transfer_failed_publishes_no_age_at_all`
  - `tests/test_backup_cli.py::test_the_report_is_built_from_the_outcome_and_never_from_the_plan`

Old text:

```
                PortionOutcome(
                    portion=entry.portion,
                    ran=False,
                    detail=f"{entry.portion.value} portion failed: {failed.stderr.strip()[-400:]}",
```

New text:

```
                PortionOutcome(
                    portion=entry.portion,
                    ran=True,
                    detail=f"{entry.portion.value} portion failed: {failed.stderr.strip()[-400:]}",
```

### `E4_return_codes_unread`

Stop reading return codes in run_backup, which is exactly the defect its sibling run_restore shipped

- File: `src/cratekit/modules/tools/backup.py`
- Surface: user
- Subset: test files importing cratekit.modules.tools.backup
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 408 against a baseline of 408
- Kills: 5 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_portion_publishes_no_age`
  - `tests/modules/test_tools.py::test_the_prune_runs_only_after_the_mirror_succeeded`
  - `tests/test_backup_cli.py::test_a_failing_rehearsal_is_not_reported_as_a_passing_one`
  - `tests/test_backup_cli.py::test_a_run_whose_every_transfer_failed_publishes_no_age_at_all`
  - `tests/test_backup_cli.py::test_the_report_is_built_from_the_outcome_and_never_from_the_plan`

Old text:

```
            if result.returncode != 0:
                failed = result
                break
```

New text:

```
            pass
```

### `E5_outcome_ok_widened`

Answer ok when ANY portion is fine rather than all of them

- File: `src/cratekit/modules/tools/backup.py`
- Surface: user
- Subset: test files importing cratekit.modules.tools.backup
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 6437 against a baseline of 6437
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        return all(p.refusal is not None or p.ran for p in self.portions)
```

New text:

```
        return any(p.refusal is not None or p.ran for p in self.portions)
```

### `E6_future_tolerance_reversed`

Treat a future timestamp as fresh, so a skewed clock silently satisfies every freshness check

- File: `src/cratekit/core/backup_facts.py`
- Surface: user
- Subset: test files importing cratekit.core.backup_facts
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_reserved_causes.py`, `tests/test_write_session.py`
- Collected: 714 against a baseline of 714
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_small_clock_difference_between_machines_is_tolerated`
  - `tests/test_backup_cli.py::test_a_partial_run_succeeds_and_publishes_only_the_half_that_ran`
  - `tests/test_backup_cli.py::test_a_run_that_succeeded_publishes_an_age_the_session_reads_back`

Old text:

```
            if delta < -FUTURE_TOLERANCE
```

New text:

```
            if delta < FUTURE_TOLERANCE
```

### `E7_record_overwrites_the_file`

Replace the fact file rather than merging, so a file mirror finishing alone erases the database portion's record

- File: `src/cratekit/core/backup_facts.py`
- Surface: user
- Subset: test files importing cratekit.core.backup_facts
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_reserved_causes.py`, `tests/test_write_session.py`
- Collected: 714 against a baseline of 714
- Kills: 5 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_refused_portion_leaves_its_previous_age_untouched`
  - `tests/modules/test_tools.py::test_backup_age_is_readable_from_library_scoped_state`
  - `tests/modules/test_tools.py::test_the_quoted_age_is_none_unless_every_portion_has_a_usable_one`
  - `tests/test_backup_cli.py::test_a_run_that_succeeded_publishes_an_age_the_session_reads_back`
  - `tests/test_backup_cli.py::test_a_supplied_configuration_is_used_rather_than_the_one_on_disk`

Old text:

```
    facts = dict(read_facts(cfg))
    facts[portion] = BackupFact(
```

New text:

```
    facts = {}
    facts[portion] = BackupFact(
```

### `E8_naive_timestamp_stored`

Accept a naive completion timestamp at the boundary, so the instant recorded depends on who reads it

- File: `src/cratekit/core/backup_facts.py`
- Surface: user
- Subset: test files importing cratekit.core.backup_facts
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_reserved_causes.py`, `tests/test_write_session.py`
- Collected: 714 against a baseline of 714
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_naive_timestamp_is_refused_where_it_is_produced`

Old text:

```
    if completed_at.tzinfo is None:
        raise ValueError(
```

New text:

```
    if False:
        raise ValueError(
```

