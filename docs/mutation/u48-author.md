# Mutation table: u48-author

Measured by `scripts/mutate.py` on 2026-09-02 04:45 UTC, branch `relay/66` at `95f4d6d`. Pass kind: light.

Baseline: green, 6528 collected. pytest invocations for this batch: 21.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6528 against 6528. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `P1_listing_classification_dropped` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 423 | 4 | killed |
| `P2_purge_classification_dropped` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 423 | 1 | killed |
| `P3_two_codes_collapsed_to_one` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 6528 | 1 (promoted) | killed |
| `P4_warning_not_recorded_on_the_portion` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 423 | 5 | killed |
| `P5_payload_key_dropped` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 423 | 3 | killed |
| `P6_purge_count_not_named` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 423 | 1 | killed |
| `P7_listing_message_reworded` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 423 | 1 | killed |
| `P8_rehearsal_starts_purging` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 423 | 2 | killed |
| `P9_purge_defaults_off` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 6528 | 0 (promoted) | zero |
| `P10_warnings_dropped_from_a_failed_portion` | `src/cratekit/modules/tools/backup.py` | maintainer | 6 file(s) | 6528 | 0 (promoted) | zero |
| `E1_listing_return_code_inverted` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 423 | 10 | killed |
| `E2_retention_ignored` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 423 | 4 | killed |
| `S1_remedy_fixed_at_repair` | `src/cratekit/core/session.py` | user | 11 file(s) | 1115 | 2 | killed |
| `S2_remedy_fixed_at_grant` | `src/cratekit/core/session.py` | user | 11 file(s) | 1115 | 2 | killed |

## Zero rows and what they owe

- `P9_purge_defaults_off` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `P10_warnings_dropped_from_a_failed_portion` (maintainer facing): maintainer facing, composite not required

## Considered and dropped

METHOD caps a light pass at 25 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `P11_warnings_field_default_shared`: Give PortionOutcome.warnings a shared mutable default instead of a factory Dropped because: a frozen slots dataclass rejects a mutable default at class definition, so the row cannot run rather than measuring nothing
- `P12_payload_key_reordered`: Move the warnings key above detail in outcome_payload Dropped because: inert by inspection: dict ordering is not asserted anywhere, so the row is shape one of the three the corpus names and would report a zero that says nothing
- `C1_shell_comment_reverted`: Restore the shell comment that conceded the prune was unreported Dropped because: a comment is invisible to the interpreter and to an AST walk, so this is the null control wearing a description; the real control is the driver's own
- `E3_prune_after_a_failed_mirror`: Let the prune run when the mirror in its portion failed Dropped because: ranked below the cap: measured at U45 and untouched by this diff, and E1 and E2 already sample the same guard family

## Row definitions

### `P1_listing_classification_dropped`

A failed listing returns no warning, so the rotation stops silently again

- File: `src/cratekit/modules/tools/backup.py`
- Surface: user
- Subset: test files importing cratekit.modules.tools.backup
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 423 against a baseline of 423
- Kills: 4 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_listing_reports_the_rotation_and_leaves_the_backup_successful`
  - `tests/modules/test_tools.py::test_a_rehearsal_reports_a_failed_listing_and_still_purges_nothing`
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_stopped_reports_it_and_is_still_a_backup`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`

Old text:

```
    if result.returncode != 0:
        return out, {
            "code": ARCHIVE_LISTING_FAILED,
```

New text:

```
    if result.returncode != 0:
        return out, None
    if result.returncode != 0:
        return out, {
            "code": ARCHIVE_LISTING_FAILED,
```

### `P2_purge_classification_dropped`

Failed purges return no warning, so folders survive with nothing saying so

- File: `src/cratekit/modules/tools/backup.py`
- Surface: user
- Subset: test files importing cratekit.modules.tools.backup
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 423 against a baseline of 423
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_purge_reports_how_many_folders_survived_it`

Old text:

```
    if unremoved:
        return out, {
            "code": ARCHIVE_PURGE_FAILED,
```

New text:

```
    if False:
        return out, {
            "code": ARCHIVE_PURGE_FAILED,
```

### `P3_two_codes_collapsed_to_one`

One code over both conditions, which is the discriminator this unit split

- File: `src/cratekit/modules/tools/backup.py`
- Surface: user
- Subset: test files importing cratekit.modules.tools.backup
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 6528 against a baseline of 6528
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`

Old text:

```
ARCHIVE_PURGE_FAILED = "archive-purge-failed"
```

New text:

```
ARCHIVE_PURGE_FAILED = "archive-listing-failed"
```

### `P4_warning_not_recorded_on_the_portion`

run_backup reads the classification and drops it instead of carrying it

- File: `src/cratekit/modules/tools/backup.py`
- Surface: user
- Subset: test files importing cratekit.modules.tools.backup
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 423 against a baseline of 423
- Kills: 5 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_listing_reports_the_rotation_and_leaves_the_backup_successful`
  - `tests/modules/test_tools.py::test_a_failed_purge_reports_how_many_folders_survived_it`
  - `tests/modules/test_tools.py::test_a_rehearsal_reports_a_failed_listing_and_still_purges_nothing`
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_stopped_reports_it_and_is_still_a_backup`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`

Old text:

```
                results += pruned
                if warning is not None:
                    warnings.append(warning)
                continue
```

New text:

```
                results += pruned
                continue
```

### `P5_payload_key_dropped`

The engine records the condition and its own payload does not render it

- File: `src/cratekit/modules/tools/backup.py`
- Surface: user
- Subset: test files importing cratekit.modules.tools.backup
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 423 against a baseline of 423
- Kills: 3 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_completed_warns_about_nothing`
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_stopped_reports_it_and_is_still_a_backup`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`

Old text:

```
                "warnings": [dict(warning) for warning in entry.warnings],
```

New text:

```
(empty)
```

### `P6_purge_count_not_named`

The purge message drops how many folders survived it

- File: `src/cratekit/modules/tools/backup.py`
- Surface: user
- Subset: test files importing cratekit.modules.tools.backup
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 423 against a baseline of 423
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_purge_reports_how_many_folders_survived_it`

Old text:

```
                f"the archive rotation did not finish: {unremoved} dated folder(s) "
```

New text:

```
                f"the archive rotation did not finish: some dated folder(s) "
```

### `P7_listing_message_reworded`

Reword the listing message, not append: the suite asserts with `in`

- File: `src/cratekit/modules/tools/backup.py`
- Surface: user
- Subset: test files importing cratekit.modules.tools.backup
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 423 against a baseline of 423
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_listing_reports_the_rotation_and_leaves_the_backup_successful`

Old text:

```
                f"nothing was removed and dated archive folders will accumulate "
                f"until it succeeds. The backup itself completed"
```

New text:

```
                f"nothing was removed and the rotation will stay stopped "
                f"until it succeeds. The backup itself completed"
```

### `P8_rehearsal_starts_purging`

The dry run passes purge on, so a preview deletes archives

- File: `src/cratekit/modules/tools/backup.py`
- Surface: user
- Subset: test files importing cratekit.modules.tools.backup
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 423 against a baseline of 423
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_dry_run_never_purges`
  - `tests/modules/test_tools.py::test_a_rehearsal_whose_listing_succeeded_warns_about_nothing_and_purges_nothing`

Old text:

```
                    purge=not dry_run,
```

New text:

```
                    purge=True,
```

### `P9_purge_defaults_off`

The suppression flag defaults to off, so a real run stops rotating

- File: `src/cratekit/modules/tools/backup.py`
- Surface: user
- Subset: test files importing cratekit.modules.tools.backup
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 6528 against a baseline of 6528
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    purge: bool = True,
```

New text:

```
    purge: bool = False,
```

### `P10_warnings_dropped_from_a_failed_portion`

A portion that failed carries no warnings, which is unreachable while the prune is last

- File: `src/cratekit/modules/tools/backup.py`
- Surface: maintainer
- Subset: test files importing cratekit.modules.tools.backup
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 6528 against a baseline of 6528
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                    detail=f"{entry.portion.value} portion failed: {failed.stderr.strip()[-400:]}",
                    results=tuple(results),
                    warnings=tuple(warnings),
```

New text:

```
                    detail=f"{entry.portion.value} portion failed: {failed.stderr.strip()[-400:]}",
                    results=tuple(results),
```

### `E1_listing_return_code_inverted`

Existing guard: purge on a failed listing and report a good one as failed

- File: `src/cratekit/modules/tools/backup.py`
- Surface: user
- Subset: test files importing cratekit.modules.tools.backup
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 423 against a baseline of 423
- Kills: 10 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_listing_reports_the_rotation_and_leaves_the_backup_successful`
  - `tests/modules/test_tools.py::test_a_failed_purge_reports_how_many_folders_survived_it`
  - `tests/modules/test_tools.py::test_a_prune_that_completed_warns_about_nothing`
  - `tests/modules/test_tools.py::test_a_rehearsal_reports_a_failed_listing_and_still_purges_nothing`
  - `tests/modules/test_tools.py::test_a_rehearsal_whose_listing_succeeded_warns_about_nothing_and_purges_nothing`
  - `tests/modules/test_tools.py::test_the_prune_keeps_the_newest_and_removes_the_rest`
  - `tests/modules/test_tools.py::test_the_retention_the_plan_declared_is_the_retention_the_run_applies`
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_completed_warns_about_nothing`
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_stopped_reports_it_and_is_still_a_backup`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`

Old text:

```
    result = runner(listing)
    out.append(result)
    if result.returncode != 0:
```

New text:

```
    result = runner(listing)
    out.append(result)
    if result.returncode == 0:
```

### `E2_retention_ignored`

Existing guard: prune every dated folder rather than keeping `keep` of them

- File: `src/cratekit/modules/tools/backup.py`
- Surface: user
- Subset: test files importing cratekit.modules.tools.backup
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 423 against a baseline of 423
- Kills: 4 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_purge_reports_how_many_folders_survived_it`
  - `tests/modules/test_tools.py::test_a_prune_that_completed_warns_about_nothing`
  - `tests/modules/test_tools.py::test_the_prune_keeps_the_newest_and_removes_the_rest`
  - `tests/modules/test_tools.py::test_the_retention_the_plan_declared_is_the_retention_the_run_applies`

Old text:

```
    for stale in names[: max(0, len(names) - keep)]:
```

New text:

```
    for stale in names:
```

### `S1_remedy_fixed_at_repair`

The session names the repair token again, which is the defect this unit closed

- File: `src/cratekit/core/session.py`
- Surface: user
- Subset: test files importing cratekit.core.session
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_backup_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 1115 against a baseline of 1115
- Kills: 2 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_fact_file_from_a_newer_build_asks_for_an_upgrade`
  - `tests/test_write_session.py::test_a_fact_file_this_account_may_not_open_asks_for_access_not_for_repair`

Old text:

```
            remedy=Remedy(str(exc.remedy)),
```

New text:

```
            remedy=Remedy.REPAIR_BACKUP_FACTS,
```

### `S2_remedy_fixed_at_grant`

The same defect mirrored: hard code the permission token over every condition

- File: `src/cratekit/core/session.py`
- Surface: user
- Subset: test files importing cratekit.core.session
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_backup_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 1115 against a baseline of 1115
- Kills: 2 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_fact_file_from_a_newer_build_asks_for_an_upgrade`
  - `tests/test_write_session.py::test_an_unreadable_backup_fact_file_refuses_the_mint`

Old text:

```
            remedy=Remedy(str(exc.remedy)),
```

New text:

```
            remedy=Remedy.GRANT_PATH_ACCESS,
```


---

## What the author read into the two zeros

The driver reports counts. This section is the reading, written by the author of
the diff, and an author's own table is a draft rather than a result.

### `P9_purge_defaults_off` is inert by construction, not a test gap

The row flips `_prune_archive`'s `purge` keyword from defaulting to True to
defaulting to False, and kills nothing on the full suite. That is not a hole in
the coverage: `run_backup` is the only caller and it passes `purge=not dry_run`
explicitly at the one call site, so the default is never read by anything. The
row is therefore shape one of the three inert shapes the corpus names, removing
an argument equal to what its caller always supplies, and it was written anyway
because that fact is worth knowing rather than assuming.

**What it does mean.** The argument in the plan for defaulting to purge on, that
a caller which says nothing gets the real rotation rather than a silent no-op,
is a statement about a caller that does not exist yet. It costs nothing and it
is not load bearing today.

**The composite, which is a user-facing surface and did kill.**
`P8_rehearsal_starts_purging` mutates the thing the default would guard, the
value actually passed, and kills 2. So the behaviour is pinned at the call site
where it is decided; only the fallback nobody reaches is unpinned.

### `P10_warnings_dropped_from_a_failed_portion` is unreachable, and the plan said so first

The row drops `warnings=tuple(warnings)` from the outcome a FAILED portion
builds, and kills nothing. The prune is the last command in its portion and the
loop breaks on the first non zero return code, so a portion that failed never
reached the prune and has no warning to carry. The plan's own requirement text
records this before the measurement: the field is carried there for a future
plan that puts a command after the prune, and until such a plan exists nothing
can produce the state.

Marked `maintainer` for that reason, so it takes the one line the method allows
rather than a composite. The alternative, deleting the argument because nothing
reaches it, would mean the day a command is appended after the prune the warning
disappears from exactly the report that most needs it, with no test failing.
