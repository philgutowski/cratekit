# Mutation table: r185-r246-author

Measured by `scripts/mutate.py` on 2026-09-20 04:53 UTC, branch `relay/157` at `7770051`. Pass kind: light.

Baseline: green, 9071 collected. pytest invocations for this batch: 18.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 9071 against 9071. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `D1_writes_reclaims_the_database` | `src/cratekit/cli/registry.py` | user | 44 file(s) | 4461 | 2 | killed |
| `D2_cloud_gate_restored` | `src/cratekit/cli/registry.py` | user | 44 file(s) | 4461 | 2 | killed |
| `W1_queue_warning_dropped` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 106 | 1 | killed |
| `W2_resume_warning_dropped` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 106 | 1 | killed |
| `W3_resume_warning_unconditional` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 106 | 1 | killed |
| `W4_refusal_step_dropped` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 106 | 1 | killed |
| `W5_refusal_step_unconditional` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 106 | 1 | killed |
| `W6_refusal_counts_the_plan` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 106 | 1 | killed |
| `M1_folder_dropped` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 106 | 3 | killed |
| `M2_act_dropped` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 106 | 2 | killed |
| `M3_cause_rebuilt_losing_the_trail` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 106 | 1 | killed |
| `E1_plan_gate_by_position` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 106 | 1 | killed |
| `E2_resume_digests_a_fresh_walk` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 106 | 6 | killed |
| `E3_empty_plan_queues_anyway` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 106 | 2 | killed |

## Considered and dropped

METHOD caps a light pass at 25 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `X1_pending_kind_for_the_reload`: Make the warning a PendingHumanAction instead Dropped because: not a mutation of a guard this round added, it is the design fork the round decided against and recorded as R-568. Reverting it would measure a verb this branch never built.
- `X2_doctor_checks_narrowed`: Drop rekordbox.pins from the entry now that no database is opened Dropped because: ranked below the cap and out of this unit's scope: R-246 names the writes set alone, name.apply is the landed precedent for keeping the check after the same narrowing, and doctor.requires_check is an any() across every entry so nothing observable moves. Recorded as R-569.
- `X3_summary_reasons_zero_filled`: Drop the zero fill from REASONS so the summary lists only the reasons it saw Dropped because: an existing guard of U40's rather than this round's, and it is already measured in that unit's table. Ranked below the three existing guards above it, which are the ones this round's new code sits directly on.

## Row definitions

### `D1_writes_reclaims_the_database`

Put db_metadata back among tag.retag's write surfaces, so the entry reclaims a write no caller performs

- File: `src/cratekit/cli/registry.py`
- Surface: user
- Subset: test files importing cratekit.cli.registry
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_jobs.py`, `tests/test_label_approved.py`, `tests/test_label_workers.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_pending_units.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`, `tests/test_write_session.py`
- Collected: 4461 against a baseline of 4461
- Kills: 2 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_every_verb_that_writes_the_database_declares_the_cloud_sync_decision`
  - `tests/test_tag_workers.py::test_the_retag_entry_declares_the_file_surface_alone_and_no_database_decision`

Old text:

```
        writes=frozenset({"files"}),
        adjudicates=True,
```

New text:

```
        writes=frozenset({"files", "db_metadata"}),
        adjudicates=True,
```

### `D2_cloud_gate_restored`

Declare the cloud sync decision on a verb that opens no database, the half the contract suite calls spurious

- File: `src/cratekit/cli/registry.py`
- Surface: user
- Subset: test files importing cratekit.cli.registry
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_jobs.py`, `tests/test_label_approved.py`, `tests/test_label_workers.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_pending_units.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`, `tests/test_write_session.py`
- Collected: 4461 against a baseline of 4461
- Kills: 2 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_every_verb_that_writes_the_database_declares_the_cloud_sync_decision`
  - `tests/test_tag_workers.py::test_the_retag_entry_declares_the_file_surface_alone_and_no_database_decision`

Old text:

```
                explicit=True,
                digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="name.apply",
```

New text:

```
                explicit=True,
                digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    Entry(
        name="name.apply",
```

### `W1_queue_warning_dropped`

The queueing envelope stops naming the reload, so the person walks away told nothing

- File: `src/cratekit/tagging/retag_cli.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag_cli
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 106 against a baseline of 106
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_queueing_envelope_names_the_reload_before_the_person_walks_away`

Old text:

```
            warnings=(library_row_warning(folder),),

```

New text:

```
(empty)
```

### `W2_resume_warning_dropped`

A successful resume stops naming the reload

- File: `src/cratekit/tagging/retag_cli.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag_cli
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 106 against a baseline of 106
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_corrected_retag_ends_by_naming_the_reload_the_stale_row_needs`

Old text:

```
        if summary["corrected"]:
            warnings = (*warnings, library_row_warning(folder))

```

New text:

```
(empty)
```

### `W3_resume_warning_unconditional`

Name the reload on every resume, including one that corrected nothing and made no row stale

- File: `src/cratekit/tagging/retag_cli.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag_cli
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 106 against a baseline of 106
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_retag_that_corrected_nothing_does_not_send_a_person_to_rekordbox`

Old text:

```
        if summary["corrected"]:
            warnings = (*warnings, library_row_warning(folder))
```

New text:

```
        warnings = (*warnings, library_row_warning(folder))
```

### `W4_refusal_step_dropped`

A half corrected sweep leaves through its cause with nothing said about the rows it made stale

- File: `src/cratekit/tagging/retag_cli.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag_cli
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 106 against a baseline of 106
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_half_corrected_retag_carries_the_reload_on_its_refusal`

Old text:

```
        try:
            job, warnings = shell.advance(
                ctx,
                store,
                queued,
                origin=("tagging", "retag_cli"),
                nothing_to_run="report a correction over files it never looked at",
            )
        except CratekitError as failed:
            # THE REFUSAL CARRIES THE RELOAD WHEN ANYTHING WAS CORRECTED. The
            # artifacts are committed per item before the failure, so this
            # counts what actually landed rather than what was confirmed, and a
            # sweep that refused on its first item adds nothing to a refusal it
            # has no reload to name. See ``with_reload_step``.
            if not _summary(cfg, ctx.args.job)["corrected"]:
                raise
            raise with_reload_step(failed, folder) from failed
```

New text:

```
        job, warnings = shell.advance(
            ctx,
            store,
            queued,
            origin=("tagging", "retag_cli"),
            nothing_to_run="report a correction over files it never looked at",
        )
```

### `W5_refusal_step_unconditional`

Append the reload to every refusal, including one that corrected nothing

- File: `src/cratekit/tagging/retag_cli.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag_cli
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 106 against a baseline of 106
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_retag_that_failed_before_correcting_anything_names_no_reload`

Old text:

```
            if not _summary(cfg, ctx.args.job)["corrected"]:
                raise
            raise with_reload_step(failed, folder) from failed
```

New text:

```
            raise with_reload_step(failed, folder) from failed
```

### `W6_refusal_counts_the_plan`

Count the confirmed items instead of the committed artifacts, so a sweep that wrote nothing still reports a correction

- File: `src/cratekit/tagging/retag_cli.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag_cli
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 106 against a baseline of 106
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_retag_that_failed_before_correcting_anything_names_no_reload`

Old text:

```
            if not _summary(cfg, ctx.args.job)["corrected"]:
                raise
```

New text:

```
            if not payload.get(ITEMS_KEY):
                raise
```

### `M1_folder_dropped`

Drop the folder from the instruction, so a person reading one envelope beside others cannot tell which sweep it names

- File: `src/cratekit/tagging/retag_cli.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag_cli
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 106 against a baseline of 106
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_corrected_retag_ends_by_naming_the_reload_the_stale_row_needs`
  - `tests/test_tag_workers.py::test_a_half_corrected_retag_carries_the_reload_on_its_refusal`
  - `tests/test_tag_workers.py::test_the_queueing_envelope_names_the_reload_before_the_person_walks_away`

Old text:

```
            f"this correction writes the genre onto the files under {folder} and "
            f"does not update the library rows, which go on carrying the old "
```

New text:

```
            f"this correction writes the genre onto the files it selected and "
            f"does not update the library rows, which go on carrying the old "
```

### `M2_act_dropped`

Reword the instruction to announce the disagreement and name no act, which is the printed instruction shape the product refuses

- File: `src/cratekit/tagging/retag_cli.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag_cli
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 106 against a baseline of 106
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_corrected_retag_ends_by_naming_the_reload_the_stale_row_needs`
  - `tests/test_tag_workers.py::test_a_half_corrected_retag_carries_the_reload_on_its_refusal`

Old text:

```
            f"value, because this build writes the file half only; select that "
            f"folder in rekordbox and reload its tags so the rows catch up"
```

New text:

```
            f"value, because this build writes the file half only, so the files "
            f"and the library disagree about the genre until something fixes it"
```

### `M3_cause_rebuilt_losing_the_trail`

Rebuild the cause in with_reload_step instead of replacing two fields, which shortens the origin trail

- File: `src/cratekit/tagging/retag_cli.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag_cli
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 106 against a baseline of 106
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_half_corrected_retag_carries_the_reload_on_its_refusal`

Old text:

```
    return CratekitError(
        replace(
            cause,
            remediation=replace(
                cause.remediation, steps=(*cause.remediation.steps, reload_step)
            ),
        )
    )
```

New text:

```
    return CratekitError(
        Cause(
            reason=cause.reason,
            message=cause.message,
            remediation=replace(
                cause.remediation, steps=(*cause.remediation.steps, reload_step)
            ),
            origin=("tagging", "retag_cli"),
        )
    )
```

### `E1_plan_gate_by_position`

Index gates[0] instead of searching by digest source, the guard the repaired case in test_genre_retag.py measures

- File: `src/cratekit/tagging/retag_cli.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag_cli
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 106 against a baseline of 106
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_the_handler_finds_its_gate_by_digest_source_and_not_by_position`

Old text:

```
    for spec in ctx.entry.gates:
        if spec.digest_source == PLAN:
            return spec
```

New text:

```
    for spec in ctx.entry.gates[:1]:
        return spec
```

### `E2_resume_digests_a_fresh_walk`

Digest the folder as it now stands rather than the frozen rows, which is KTD8's permanent stall

- File: `src/cratekit/tagging/retag_cli.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag_cli
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 106 against a baseline of 106
- Kills: 6 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_file_gone_at_drive_time_is_refused_rather_than_reported_done`
  - `tests/test_tag_workers.py::test_a_genre_made_blank_between_the_confirm_and_the_drive_is_left_to_its_owner`
  - `tests/test_tag_workers.py::test_a_genre_made_specific_between_the_confirm_and_the_drive_is_not_rewritten`
  - `tests/test_tag_workers.py::test_a_resume_after_a_partial_run_meets_its_gate_rather_than_going_stale`
  - `tests/test_tag_workers.py::test_a_retried_retag_drives_only_the_item_that_failed`
  - `tests/test_tag_workers.py::test_the_report_is_derived_from_what_ran_rather_than_from_what_was_planned`

Old text:

```
            digest=digest_for(
                str(payload.get(FOLDER_KEY) or ""),
                [dict(row) for row in payload.get(ITEMS_KEY) or ()],
            ),
```

New text:

```
            digest=plan_for(
                str(payload.get(FOLDER_KEY) or ""), taxonomy.default_taxonomy()
            )["digest"],
```

### `E3_empty_plan_queues_anyway`

Queue a job over an empty selection, which core.jobs drives straight to SUCCEEDED over a folder nothing touched

- File: `src/cratekit/tagging/retag_cli.py`
- Surface: user
- Subset: test files importing cratekit.tagging.retag_cli
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 106 against a baseline of 106
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_folder_that_is_not_there_is_a_different_zero_from_one_with_nothing_coarse`
  - `tests/test_tag_workers.py::test_an_empty_plan_is_still_asked_about_and_still_queues_nothing`

Old text:

```
    if not plan["items"]:
        payload, warnings = (
```

New text:

```
    if False:
        payload, warnings = (
```

