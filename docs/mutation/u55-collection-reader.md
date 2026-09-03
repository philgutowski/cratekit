# Mutation table: u55-collection-reader

Measured by `scripts/mutate.py` on 2026-09-02 23:47 UTC, branch `relay/73` at `02ac89b`. Pass kind: full.

Baseline: green, 6669 collected. pytest invocations for this batch: 48.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6669 against 6669. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `R1_read_only_open` | `src/cratekit/adopt/collection.py` | user | 3 file(s) | 57 | 2 | killed |
| `R2_reader_unlock_probe` | `src/cratekit/adopt/collection.py` | user | 3 file(s) | 6669 | 0 (promoted) | zero |
| `R3_soft_delete_marker` | `src/cratekit/adopt/collection.py` | user | 3 file(s) | 57 | 1 | killed |
| `R4_genre_proxy` | `src/cratekit/adopt/collection.py` | user | 3 file(s) | 57 | 19 | killed |
| `R5_cache_key_resolved` | `src/cratekit/adopt/collection.py` | maintainer | 3 file(s) | 6669 | 0 (promoted) | zero |
| `R6_unlock_probe_answer` | `src/cratekit/core/rb_writer.py` | user | 21 file(s) | 6669 | 0 (promoted) | zero |
| `R7_census_taxonomy` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 43 | 1 | killed |
| `R8_census_prefix_map` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 6669 | 0 (promoted) | zero |
| `R9_scan_zero_item_refusal` | `src/cratekit/adopt/scan_cli.py` | user | 1 file(s) | 19 | 2 | killed |
| `R10_apply_zero_item_refusal` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 43 | 1 | killed |
| `R11_scan_item_ids` | `src/cratekit/adopt/scan_cli.py` | user | 1 file(s) | 19 | 4 | killed |
| `R12_apply_item_ids` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 43 | 11 | killed |
| `R13_scan_job_id_string` | `src/cratekit/adopt/scan_cli.py` | user | 1 file(s) | 19 | 2 | killed |
| `R14_apply_job_id_string` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 43 | 2 | killed |
| `R15_scan_no_items_refusal` | `src/cratekit/adopt/scan_cli.py` | user | 1 file(s) | 19 | 1 | killed |
| `R16_apply_no_items_refusal` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 6669 | 0 (promoted) | zero |
| `R17_scan_r225_predicate` | `src/cratekit/adopt/scan_cli.py` | user | 1 file(s) | 6669 | 0 (promoted) | zero |
| `R18_apply_r225_predicate` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 6669 | 0 (promoted) | zero |
| `R19_collector_groups_locations` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 43 | 1 | killed |
| `R20_membership_locations_key` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 43 | 4 | killed |
| `R21_membership_from_the_plan` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 43 | 9 | killed |
| `R22_membership_before_the_mark` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 43 | 2 | killed |
| `R23_worker_raises_on_failure` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 6669 | 0 (promoted) | zero |
| `R24_worker_digest_check` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 43 | 1 | killed |
| `R25_scan_item_absent_refusal` | `src/cratekit/adopt/scan_cli.py` | user | 1 file(s) | 19 | 1 | killed |
| `R26_apply_write_intent_open` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 6669 | 0 (promoted) | zero |
| `R27_apply_no_tag_value` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 43 | 3 | killed |
| `R28_scan_frozen_config` | `src/cratekit/adopt/scan_cli.py` | user | 1 file(s) | 6669 | 1 (promoted) | killed |
| `R29_apply_frozen_config` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 6669 | 1 (promoted) | killed |
| `R30_scan_handler_bound` | `src/cratekit/cli/handlers.py` | user | 5 file(s) | 138 | 6 | killed |

## Zero rows and what they owe

- `R2_reader_unlock_probe` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `R5_cache_key_resolved` (maintainer facing): maintainer facing, composite not required
- `R6_unlock_probe_answer` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `R8_census_prefix_map` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `R16_apply_no_items_refusal` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `R17_scan_r225_predicate` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `R18_apply_r225_predicate` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `R23_worker_raises_on_failure` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `R26_apply_write_intent_open` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Considered and dropped

METHOD caps a full pass at 45 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `R31_check_app_version`: Flip check_app_version on the reader's open Dropped because: inert by construction: open_db consults it only inside its require_closed branch, so on a read it can kill nothing. Recorded in KTD1 rather than measured.
- `R32_apply_handler_bound`: adopt.apply loses its worker, the sibling of R30 Dropped because: ranked below R30 as the same guard in the same table with the same derivation; test_handlers derives the population from the registry, so one of the pair measures the mechanism
- `R33_artifact_ordinal`: Build the artifact filename from the item identifier rather than the ordinal Dropped because: the same guard modules/outbound/artifacts already carries and U51 already measured; this unit's copy adds no new decision
- `R34_analysis_roots`: Empty the analysis_roots the apply's membership write names Dropped because: write_tree_membership raises ValueError on an empty one by construction, so the row measures that function's own guard rather than this unit's caller

## Row definitions

### `R1_read_only_open`

The reader asks for a WRITE intent open. The single most important row in this table.

- File: `src/cratekit/adopt/collection.py`
- Surface: user
- Subset: test files importing cratekit.adopt.collection
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_workers.py`
- Collected: 57 against a baseline of 57
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_collection.py::test_the_reader_never_opens_the_database_for_writing`
  - `tests/test_adopt_collection.py::test_this_module_holds_no_write_path_at_all`

Old text:

```
        require_closed=False,
```

New text:

```
        require_closed=True,
```

### `R2_reader_unlock_probe`

The reader assumes the file is never encrypted rather than asking the bytes

- File: `src/cratekit/adopt/collection.py`
- Surface: user
- Subset: test files importing cratekit.adopt.collection
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_workers.py`
- Collected: 6669 against a baseline of 6669
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

### `R3_soft_delete_marker`

R-186's exact defect: default the tombstone marker instead of reading it

- File: `src/cratekit/adopt/collection.py`
- Surface: user
- Subset: test files importing cratekit.adopt.collection
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_workers.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_collection.py::test_a_row_that_cannot_report_the_marker_refuses_rather_than_defaulting`

Old text:

```
            deleted=trees.soft_delete_marker(row),
```

New text:

```
            deleted=bool(getattr(row, "rb_local_deleted", False)),
```

### `R4_genre_proxy`

Read the raw GenreID rather than the binding's own display proxy

- File: `src/cratekit/adopt/collection.py`
- Surface: user
- Subset: test files importing cratekit.adopt.collection
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_workers.py`
- Collected: 57 against a baseline of 57
- Kills: 19 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_a_resume_reconciles_a_claim_a_dead_driver_left_behind`
  - `tests/test_adopt_apply_cli.py::test_an_approved_run_queues_one_job_carrying_the_tree_and_the_digest`
  - `tests/test_adopt_apply_cli.py::test_the_census_classifies_against_the_taxonomy_its_caller_resolved`
  - `tests/test_adopt_apply_cli.py::test_the_census_is_the_library_and_every_row_of_it_is_carried`
  - `tests/test_adopt_apply_cli.py::test_the_resume_the_job_driver_spawns_can_actually_proceed`
  - `tests/test_adopt_collection.py::test_a_dangling_genre_reference_reads_as_no_genre`
  - `tests/test_adopt_collection.py::test_every_field_comes_off_the_row_it_belongs_to`
  - `tests/test_adopt_collection.py::test_the_reader_yields_the_rows_the_database_holds`
  - `tests/test_adopt_workers.py::test_a_collection_that_moved_after_approval_refuses_rather_than_applying`
  - `tests/test_adopt_workers.py::test_a_registry_naming_a_root_the_library_does_not_have_is_its_own_refusal`
  - `tests/test_adopt_workers.py::test_a_scan_queues_one_item_per_live_row_and_drives_them_all`
  - `tests/test_adopt_workers.py::test_a_second_drive_adds_no_second_membership_row`
  - `tests/test_adopt_workers.py::test_an_apply_over_a_cut_over_library_writes_the_memberships`
  - `tests/test_adopt_workers.py::test_an_uncut_library_marks_nothing_and_the_job_stays_resumable`
  - `tests/test_adopt_workers.py::test_one_capture_per_apply_job_whatever_the_entry_count`
  - ... and 4 more, see the JSON sidecar

Old text:

```
    return str(getattr(row, "GenreName", "") or "")
```

New text:

```
    return str(getattr(row, "GenreID", "") or "")
```

### `R5_cache_key_resolved`

Key the reader's cache on the raw path rather than the resolved absolute one

- File: `src/cratekit/adopt/collection.py`
- Surface: maintainer
- Subset: test files importing cratekit.adopt.collection
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_workers.py`
- Collected: 6669 against a baseline of 6669
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
- Collected: 6669 against a baseline of 6669
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

### `R7_census_taxonomy`

The census resolves its own taxonomy, so one entry can be built from two

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: test files importing cratekit.adopt.apply_cli
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 43 against a baseline of 43
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_the_census_classifies_against_the_taxonomy_its_caller_resolved`

Old text:

```
            collection.read_collection(cfg),
            declared,
            root=cfg.library.root,
```

New text:

```
            collection.read_collection(cfg),
            taxonomy.default_taxonomy(),
            root=cfg.library.root,
```

### `R8_census_prefix_map`

The census drops the configured volume rewrites, so an older volume name resolves nowhere

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: test files importing cratekit.adopt.apply_cli
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 6669 against a baseline of 6669
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

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

### `R9_scan_zero_item_refusal`

The scan queues a job over an empty library, which drives to SUCCEEDED having read nothing

- File: `src/cratekit/adopt/scan_cli.py`
- Surface: user
- Subset: test files importing cratekit.adopt.scan_cli
- Ran: `tests/test_adopt_workers.py`
- Collected: 19 against a baseline of 19
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_library_of_tombstones_is_a_different_zero_from_an_empty_one`
  - `tests/test_adopt_workers.py::test_an_empty_library_queues_nothing_and_says_so`

Old text:

```
    if not live:
```

New text:

```
    if False:
```

### `R10_apply_zero_item_refusal`

The apply queues a job with one item over a plan that can place nothing

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: test files importing cratekit.adopt.apply_cli
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 43 against a baseline of 43
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_plan_with_nothing_applicable_queues_nothing`

Old text:

```
    if not applicable:
```

New text:

```
    if False:
```

### `R11_scan_item_ids`

The scan enqueues with no items at all, which is the R-203 shape

- File: `src/cratekit/adopt/scan_cli.py`
- Surface: user
- Subset: test files importing cratekit.adopt.scan_cli
- Ran: `tests/test_adopt_workers.py`
- Collected: 19 against a baseline of 19
- Kills: 4 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item`
  - `tests/test_adopt_workers.py::test_a_scan_queues_one_item_per_live_row_and_drives_them_all`
  - `tests/test_adopt_workers.py::test_the_configuration_reaching_the_scan_worker_is_the_frozen_one`
  - `tests/test_adopt_workers.py::test_the_reported_counts_come_from_the_artifacts_and_not_from_the_queue`

Old text:

```
            item_ids=live,
```

New text:

```
            item_ids=(),
```

### `R12_apply_item_ids`

The apply enqueues with no items at all

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: test files importing cratekit.adopt.apply_cli
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 43 against a baseline of 43
- Kills: 11 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_a_resume_reconciles_a_claim_a_dead_driver_left_behind`
  - `tests/test_adopt_apply_cli.py::test_the_resume_the_job_driver_spawns_can_actually_proceed`
  - `tests/test_adopt_workers.py::test_a_collection_that_moved_after_approval_refuses_rather_than_applying`
  - `tests/test_adopt_workers.py::test_a_registry_naming_a_root_the_library_does_not_have_is_its_own_refusal`
  - `tests/test_adopt_workers.py::test_a_second_drive_adds_no_second_membership_row`
  - `tests/test_adopt_workers.py::test_an_apply_over_a_cut_over_library_writes_the_memberships`
  - `tests/test_adopt_workers.py::test_an_uncut_library_marks_nothing_and_the_job_stays_resumable`
  - `tests/test_adopt_workers.py::test_one_capture_per_apply_job_whatever_the_entry_count`
  - `tests/test_adopt_workers.py::test_the_apply_writes_no_tag_and_leaves_every_file_byte_identical`
  - `tests/test_adopt_workers.py::test_the_approving_actor_travels_in_the_payload`
  - `tests/test_adopt_workers.py::test_the_membership_write_is_derived_from_the_plan_and_not_from_the_run`

Old text:

```
            item_ids=(plan.digest(),),
```

New text:

```
            item_ids=(),
```

### `R13_scan_job_id_string`

R-234's shape on the scan's no-op payload: a null job_id fails the declared schema

- File: `src/cratekit/adopt/scan_cli.py`
- Surface: user
- Subset: test files importing cratekit.adopt.scan_cli
- Ran: `tests/test_adopt_workers.py`
- Collected: 19 against a baseline of 19
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_library_of_tombstones_is_a_different_zero_from_an_empty_one`
  - `tests/test_adopt_workers.py::test_an_empty_library_queues_nothing_and_says_so`

Old text:

```
    payload = {"job_id": "", "state": "no-op", "cause": None, "progress": {}}
```

New text:

```
    payload = {"job_id": None, "state": "no-op", "cause": None, "progress": {}}
```

### `R14_apply_job_id_string`

R-234 itself, reverted: the declined payload emits a null job_id again

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: test files importing cratekit.adopt.apply_cli
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 43 against a baseline of 43
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_a_declined_run_queues_nothing_at_all`
  - `tests/test_adopt_workers.py::test_a_plan_with_nothing_applicable_queues_nothing`

Old text:

```
    return {"job_id": "", "state": state, "cause": None, "progress": {}}
```

New text:

```
    return {"job_id": None, "state": state, "cause": None, "progress": {}}
```

### `R15_scan_no_items_refusal`

A job queued by an older build drives to SUCCEEDED over a census it never took

- File: `src/cratekit/adopt/scan_cli.py`
- Surface: user
- Subset: test files importing cratekit.adopt.scan_cli
- Ran: `tests/test_adopt_workers.py`
- Collected: 19 against a baseline of 19
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_job_queued_with_no_items_refuses_rather_than_reporting_success`

Old text:

```
            if not jobs.items(store, job.job_id):
                raise refuse(
                    "internal-error",
                    f"job {job.job_id} has no items to run, so driving it would "
                    f"report a census over a library it never read. It was queued "
                    f"by a build that did not record what its items were",
                    remedy=Remedy.REPORT_DEFECT,
                    origin=("adopt", "scan_cli"),
                    detail={"job_id": job.job_id},
                )

```

New text:

```
(empty)
```

### `R16_apply_no_items_refusal`

The same, on the apply's resume branch

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: test files importing cratekit.adopt.apply_cli
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 6669 against a baseline of 6669
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

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
- Collected: 6669 against a baseline of 6669
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

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

The same predicate on the apply's resume branch

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: test files importing cratekit.adopt.apply_cli
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 6669 against a baseline of 6669
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

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

### `R19_collector_groups_locations`

The collector groups content identifiers again, which is the seam defect U55 found

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: test files importing cratekit.adopt.apply_cli
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 43 against a baseline of 43
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_the_memberships_are_collected_and_match_what_the_loop_reached`

Old text:

```
            into.setdefault((folder, sub), []).append(entry.path)
```

New text:

```
            into.setdefault((folder, sub), []).append(entry.content_id)
```

### `R20_membership_locations_key`

The written mapping groups content identifiers, so the write matches nothing

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: test files importing cratekit.adopt.apply_cli
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 43 against a baseline of 43
- Kills: 4 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_the_memberships_are_collected_and_match_what_the_loop_reached`
  - `tests/test_adopt_workers.py::test_an_apply_over_a_cut_over_library_writes_the_memberships`
  - `tests/test_adopt_workers.py::test_the_membership_write_is_derived_from_the_plan_and_not_from_the_run`
  - `tests/test_adopt_workers.py::test_the_membership_write_needs_locations_and_not_content_identifiers`

Old text:

```
        grouped.setdefault((folder, sub), []).append(entry.path)
```

New text:

```
        grouped.setdefault((folder, sub), []).append(entry.content_id)
```

### `R21_membership_from_the_plan`

The write is derived from THIS RUN rather than from the plan, so a crash is permanent

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: test files importing cratekit.adopt.apply_cli
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 43 against a baseline of 43
- Kills: 9 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_the_resume_the_job_driver_spawns_can_actually_proceed`
  - `tests/test_adopt_workers.py::test_a_registry_naming_a_root_the_library_does_not_have_is_its_own_refusal`
  - `tests/test_adopt_workers.py::test_a_second_drive_adds_no_second_membership_row`
  - `tests/test_adopt_workers.py::test_an_apply_over_a_cut_over_library_writes_the_memberships`
  - `tests/test_adopt_workers.py::test_an_uncut_library_marks_nothing_and_the_job_stays_resumable`
  - `tests/test_adopt_workers.py::test_one_capture_per_apply_job_whatever_the_entry_count`
  - `tests/test_adopt_workers.py::test_the_apply_writes_no_tag_and_leaves_every_file_byte_identical`
  - `tests/test_adopt_workers.py::test_the_approving_actor_travels_in_the_payload`
  - `tests/test_adopt_workers.py::test_the_membership_write_is_derived_from_the_plan_and_not_from_the_run`

Old text:

```
            plan=membership_locations(plan.applicable(), declared),
```

New text:

```
            plan=dict(gathered),
```

### `R22_membership_before_the_mark`

Apply first, write memberships second: the ordering the drive reversed

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: test files importing cratekit.adopt.apply_cli
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 43 against a baseline of 43
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_the_resume_the_job_driver_spawns_can_actually_proceed`
  - `tests/test_adopt_workers.py::test_an_uncut_library_marks_nothing_and_the_job_stays_resumable`

Old text:

```
    membership = _write_memberships(cfg, plan, declared)

    actor = str((job.payload or {}).get(ACTOR_KEY) or "")
    report, gathered = apply_outstanding(cfg, plan, declared, actor=actor)
```

New text:

```
    actor = str((job.payload or {}).get(ACTOR_KEY) or "")
    report, gathered = apply_outstanding(cfg, plan, declared, actor=actor)

    membership = _write_memberships(cfg, plan, declared)
```

### `R23_worker_raises_on_failure`

A failed apply returns rather than raising, so the job reaches SUCCEEDED over nothing

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: test files importing cratekit.adopt.apply_cli
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 6669 against a baseline of 6669
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

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

### `R24_worker_digest_check`

The worker applies a plan nobody approved, because the frozen digest is not compared

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: test files importing cratekit.adopt.apply_cli
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 43 against a baseline of 43
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_collection_that_moved_after_approval_refuses_rather_than_applying`

Old text:

```
    if plan.digest() != frozen_digest:
```

New text:

```
    if False:
```

### `R25_scan_item_absent_refusal`

A row removed between queueing and driving crashes the worker instead of failing its item

- File: `src/cratekit/adopt/scan_cli.py`
- Surface: user
- Subset: test files importing cratekit.adopt.scan_cli
- Ran: `tests/test_adopt_workers.py`
- Collected: 19 against a baseline of 19
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item`

Old text:

```
    row = rows.get(item.item_id)
    if row is None:
```

New text:

```
    row = rows.get(item.item_id)
    if False:
```

### `R26_apply_write_intent_open`

The apply's own handle drops its write intent, so rekordbox may be running under it

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: test files importing cratekit.adopt.apply_cli
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 6669 against a baseline of 6669
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

### `R27_apply_no_tag_value`

A tag_value supplier is installed, so the apply writes a genre onto the person's files

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: test files importing cratekit.adopt.apply_cli
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 43 against a baseline of 43
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_second_drive_adds_no_second_membership_row`
  - `tests/test_adopt_workers.py::test_an_apply_over_a_cut_over_library_writes_the_memberships`
  - `tests/test_adopt_workers.py::test_the_apply_writes_no_tag_and_leaves_every_file_byte_identical`

Old text:

```
    report, gathered = apply_outstanding(cfg, plan, declared, actor=actor)
```

New text:

```
    report, gathered = apply_outstanding(
        cfg, plan, declared, actor=actor, tag_value=lambda entry, _d: entry.bucket or None
    )
```

### `R28_scan_frozen_config`

KTD9: the scan worker loads a fresh configuration rather than using the frozen one

- File: `src/cratekit/adopt/scan_cli.py`
- Surface: user
- Subset: test files importing cratekit.adopt.scan_cli
- Ran: `tests/test_adopt_workers.py`
- Collected: 6669 against a baseline of 6669
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_handlers.py::test_no_declared_handler_loads_a_fresh_configuration`

Old text:

```
    rows = {row.content_id: row for row in collection.read_collection(cfg)}
```

New text:

```
    cfg = config.load()
    rows = {row.content_id: row for row in collection.read_collection(cfg)}
```

### `R29_apply_frozen_config`

The same, on the apply worker

- File: `src/cratekit/adopt/apply_cli.py`
- Surface: user
- Subset: test files importing cratekit.adopt.apply_cli
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 6669 against a baseline of 6669
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_handlers.py::test_no_declared_handler_loads_a_fresh_configuration`

Old text:

```
    del item
    declared = taxonomy.default_taxonomy()
    plan = current_plan(cfg, declared)
```

New text:

```
    del item
    cfg = config.load()
    declared = taxonomy.default_taxonomy()
    plan = current_plan(cfg, declared)
```

### `R30_scan_handler_bound`

adopt.scan loses its worker, which is the state R-203 records

- File: `src/cratekit/cli/handlers.py`
- Surface: user
- Subset: test files importing cratekit.cli.handlers
- Ran: `tests/test_adopt_workers.py`, `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_outbound_workers.py`
- Collected: 138 against a baseline of 138
- Kills: 6 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item`
  - `tests/test_adopt_workers.py::test_a_scan_queues_one_item_per_live_row_and_drives_them_all`
  - `tests/test_adopt_workers.py::test_both_adopt_keys_resolve_to_a_worker`
  - `tests/test_adopt_workers.py::test_the_configuration_reaching_the_scan_worker_is_the_frozen_one`
  - `tests/test_adopt_workers.py::test_the_reported_counts_come_from_the_artifacts_and_not_from_the_queue`
  - `tests/test_handlers.py::test_every_queued_verb_is_either_bound_or_named_as_unbound`

Old text:

```
    "adopt.scan": "cratekit.adopt.scan_cli:handle",
```

New text:

```
(empty)
```

