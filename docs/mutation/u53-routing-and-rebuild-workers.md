# Mutation table: u53-routing-and-rebuild-workers

Measured by `scripts/mutate.py` on 2026-09-10 13:07 UTC, branch `relay/71` at `d565375`. Pass kind: light.

Baseline: green, 7136 collected. pytest invocations for this batch: 34.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 7136 against 7136. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `A1_apply_call_removed` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 26 | 4 | killed |
| `A2_abort_instead_of_not_apply` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 7136 | 0 (promoted) | zero |
| `A3_empty_folder_shortcircuit_removed` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `A4_native_check_removed` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `A5_applied_always_true` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `A6_inbox_watch_narrowed` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `U1_unplaced_constant_empty` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 26 | 2 | killed |
| `U2_compared_true_without_a_tree` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `U3_held_never_populated` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `U4_tombstones_reported` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `I1_native_filter_dropped` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 7136 | 0 (promoted) | zero |
| `I2_resort_items_dropped` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 26 | 2 | killed |
| `I3_rebuild_items_dropped` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 26 | 8 | killed |
| `I4_resort_empty_job_filed` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `I5_rebuild_empty_job_filed` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 26 | 1 | killed |
| `I6_tree_items_ignores_native` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 7136 | 0 (promoted) | zero |
| `I7_tree_items_ignores_the_named_tree` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 7136 | 0 (promoted) | zero |
| `R1_resort_drives_a_foreign_job` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `R2_rebuild_drives_a_foreign_job` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 26 | 1 | killed |
| `R3_resort_drives_an_itemless_job` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `R4_rebuild_drives_an_itemless_job` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 26 | 1 | killed |
| `R5_resort_swallows_the_jobs_cause` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `R6_rebuild_swallows_the_jobs_cause` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 26 | 1 | killed |
| `E1_addressability_check_dropped` | `src/cratekit/write/rebuild.py` | user | 2 file(s) | 7136 | 0 (promoted) | zero |
| `E2_rebuild_watch_narrowed` | `src/cratekit/write/rebuild.py` | user | 2 file(s) | 129 | 1 | killed |

## Zero rows and what they owe

- `A2_abort_instead_of_not_apply` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `I1_native_filter_dropped` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `I6_tree_items_ignores_native` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `I7_tree_items_ignores_the_named_tree` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `E1_addressability_check_dropped` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Considered and dropped

METHOD caps a light pass at 25 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `R7_resort_reports_without_driving`: The resume reports the job again instead of calling run_job, which is the state before U46 Dropped because: the item state assertions in the two end to end tests read exactly this line, so R3 and R5 already measure whether anything drives; a third row over one call adds no independent evidence
- `R8_rebuild_reports_without_driving`: The same omission in the rebuild's resume Dropped because: same as R7, and the rebuild arm of every parametrized resume test drives the same call
- `U5_unplaced_filter_inverted`: Unplaced reports the rows the tree DOES hold Dropped because: U1 and U3 bracket this from both sides, an empty answer and an everything answer, and an inverted filter cannot survive either
- `E3_rows_left_as_a_cursor`: rebuild_governed_tree hands the engine the content row generator rather than a list Dropped because: the engine materializes rows itself at its first line, so this mutation is inert in this build; a row known in advance to be inert is a finding to state, not a row to spend
- `E4_root_exists_always_true`: The worker answers that every root identifier exists Dropped because: driven directly as a behaviour instead, in the test for a registry naming a root the database lacks, which is stronger than a count
- `A7_readings_scoped_to_the_library`: The apply reads tag truth from the whole music directory rather than from the intake folder Dropped because: not expressible as one textual substitution without rewriting the derivation call, and the digest assertion already pins that the apply acts on the plan it offered

## Row definitions

### `A1_apply_call_removed`

The confirmed branch returns the plan without applying it, which is the defect this unit closed

- File: `src/cratekit/write/routing_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.routing_cli
- Ran: `tests/test_routing_workers.py`
- Collected: 26 against a baseline of 26
- Kills: 4 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_on_a_library_with_no_native_tree_says_so`
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_watches_the_grids_where_they_actually_live`
  - `tests/test_routing_workers.py::test_the_confirmed_inbox_applies_and_the_declined_one_does_not`
  - `tests/test_routing_workers.py::test_unplaced_over_a_fully_placed_library_reports_none`

Old text:

```
    result = apply_inbox(cfg, items)
```

New text:

```
    result = {"applied": True, "reason": None, "added": 0, "skipped": 0, "trees": 0}
```

### `A2_abort_instead_of_not_apply`

The branch tests for abort rather than for apply, so an option nobody classified acquires the write

- File: `src/cratekit/write/routing_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.routing_cli
- Ran: `tests/test_routing_workers.py`
- Collected: 7136 against a baseline of 7136
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if option != "apply":
        return ctx.envelope(data=_plan(items, kind="inbox", applied=False), outcome=Outcome.NO_OP)
```

New text:

```
    if option == "abort":
        return ctx.envelope(data=_plan(items, kind="inbox", applied=False), outcome=Outcome.NO_OP)
```

### `A3_empty_folder_shortcircuit_removed`

A confirmed apply over an empty intake folder derives and opens a database rather than stopping

- File: `src/cratekit/write/routing_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.routing_cli
- Ran: `tests/test_routing_workers.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_over_an_empty_folder_opens_nothing`

Old text:

```
    if not items:
        # AN EMPTY FOLDER IS NOT A WRITE.
```

New text:

```
    if False:
        # AN EMPTY FOLDER IS NOT A WRITE.
```

### `A4_native_check_removed`

The apply proceeds on a library whose trees are all still on the XML bridge

- File: `src/cratekit/write/routing_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.routing_cli
- Ran: `tests/test_routing_workers.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_on_a_library_with_no_native_tree_says_so`

Old text:

```
    if not native:
        return {"applied": False, "reason": "no-native-tree", "added": 0, "skipped": 0}
```

New text:

```
    if False:
        return {"applied": False, "reason": "no-native-tree", "added": 0, "skipped": 0}
```

### `A5_applied_always_true`

Every apply reports itself as having applied, whatever it did

- File: `src/cratekit/write/routing_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.routing_cli
- Ran: `tests/test_routing_workers.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_on_a_library_with_no_native_tree_says_so`

Old text:

```
        outcome=Outcome.OK if result["applied"] else Outcome.NO_OP,
```

New text:

```
        outcome=Outcome.OK,
```

### `A6_inbox_watch_narrowed`

The apply arms its analysis watch over the music directory, where no analysis file lives

- File: `src/cratekit/write/routing_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.routing_cli
- Ran: `tests/test_routing_workers.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_watches_the_grids_where_they_actually_live`

Old text:

```
                analysis_roots=[Path(cfg.library.root)],
                workflow=INBOX_WORKFLOW,
```

New text:

```
                analysis_roots=[Path(cfg.library.root) / cfg.library.music_dir],
                workflow=INBOX_WORKFLOW,
```

### `U1_unplaced_constant_empty`

Unplaced reports nothing whatever the library holds, which is the defect verbatim

- File: `src/cratekit/write/routing_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.routing_cli
- Ran: `tests/test_routing_workers.py`
- Collected: 26 against a baseline of 26
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_unplaced_does_not_report_a_row_rekordbox_removed`
  - `tests/test_routing_workers.py::test_unplaced_reports_the_rows_no_governed_tree_holds`

Old text:

```
    items = [
        {"content_id": row.content_id, "path": row.recorded}
        for row in active
        if row.content_id not in held
    ]
```

New text:

```
    items = []
```

### `U2_compared_true_without_a_tree`

A library with nothing native reports an empty answer as a comparison it made

- File: `src/cratekit/write/routing_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.routing_cli
- Ran: `tests/test_routing_workers.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_unplaced_says_when_it_could_not_compare`

Old text:

```
        return [], {"compared": False, "reason": "no-native-tree", "collection": 0}
```

New text:

```
        return [], {"compared": True, "reason": None, "collection": 0}
```

### `U3_held_never_populated`

Nothing is read out of the tree, so every row in the library reports as unplaced

- File: `src/cratekit/write/routing_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.routing_cli
- Ran: `tests/test_routing_workers.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_unplaced_over_a_fully_placed_library_reports_none`

Old text:

```
            for node in rebuild.read_tree(handle, root_id):
                held |= set(node.content_ids)
```

New text:

```
            rebuild.read_tree(handle, root_id)
```

### `U4_tombstones_reported`

A row rekordbox removed is reported as a track still waiting to be filed

- File: `src/cratekit/write/routing_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.routing_cli
- Ran: `tests/test_routing_workers.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_unplaced_does_not_report_a_row_rekordbox_removed`

Old text:

```
    active = [row for row in rows if not row.deleted]
```

New text:

```
    active = list(rows)
```

### `I1_native_filter_dropped`

A resort queues an item for a tree still on the bridge, which no rebuild can write

- File: `src/cratekit/write/routing_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.routing_cli
- Ran: `tests/test_routing_workers.py`
- Collected: 7136 against a baseline of 7136
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return tuple(sorted(t for t in entries.tree_ids() if entries.is_database_native(t)))
```

New text:

```
    return tuple(sorted(entries.tree_ids()))
```

### `I2_resort_items_dropped`

The resort files a job with no items, which the driver walks once and calls succeeded

- File: `src/cratekit/write/routing_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.routing_cli
- Ran: `tests/test_routing_workers.py`
- Collected: 26 against a baseline of 26
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_queued_resort_runs_its_item_and_the_tree_holds_the_track`
  - `tests/test_routing_workers.py::test_neither_queued_verb_files_a_job_with_no_items[resort]`

Old text:

```
            payload={},
            item_ids=items,
            cfg=cfg,
```

New text:

```
            payload={},
            cfg=cfg,
```

### `I3_rebuild_items_dropped`

The rebuild files a job with no items, the state every rebuild was in before this unit

- File: `src/cratekit/cli/rebuild.py`
- Surface: user
- Subset: test files importing cratekit.cli.rebuild
- Ran: `tests/test_routing_workers.py`
- Collected: 26 against a baseline of 26
- Kills: 8 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_driven_rebuild_over_an_absent_music_directory_fails_the_item`
  - `tests/test_routing_workers.py::test_a_driven_rebuild_watches_the_grids_where_they_actually_live`
  - `tests/test_routing_workers.py::test_a_driven_rebuild_whose_root_the_database_lacks_fails_the_item`
  - `tests/test_routing_workers.py::test_a_driven_rebuild_without_an_acknowledgment_refuses_through_the_real_gates`
  - `tests/test_routing_workers.py::test_a_queued_rebuild_runs_its_item_and_the_tree_holds_the_track`
  - `tests/test_routing_workers.py::test_a_resume_reads_no_registry_of_its_own`
  - `tests/test_routing_workers.py::test_neither_queued_verb_files_a_job_with_no_items[rebuild]`
  - `tests/test_routing_workers.py::test_unplaced_over_a_fully_placed_library_reports_none`

Old text:

```
            payload={"tree": tree_id, "actor": actor},
            item_ids=items,
```

New text:

```
            payload={"tree": tree_id, "actor": actor},
```

### `I4_resort_empty_job_filed`

A library with nothing native files an empty resort job instead of saying there was nothing to queue

- File: `src/cratekit/write/routing_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.routing_cli
- Ran: `tests/test_routing_workers.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_neither_queued_verb_files_a_job_at_all_with_no_native_tree[resort]`

Old text:

```
        items = _native_trees(tree_registry.read(cfg))
        if not items:
```

New text:

```
        items = _native_trees(tree_registry.read(cfg))
        if False:
```

### `I5_rebuild_empty_job_filed`

A library with nothing native files an empty rebuild job

- File: `src/cratekit/cli/rebuild.py`
- Surface: user
- Subset: test files importing cratekit.cli.rebuild
- Ran: `tests/test_routing_workers.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_neither_queued_verb_files_a_job_at_all_with_no_native_tree[rebuild]`

Old text:

```
        items = tree_items(entries, tree_id)
        if not items:
```

New text:

```
        items = tree_items(entries, tree_id)
        if False:
```

### `I6_tree_items_ignores_native`

The rebuild's items include trees the registry says are still on the bridge

- File: `src/cratekit/cli/rebuild.py`
- Surface: user
- Subset: test files importing cratekit.cli.rebuild
- Ran: `tests/test_routing_workers.py`
- Collected: 7136 against a baseline of 7136
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    native = tuple(sorted(t for t in entries.tree_ids() if entries.is_database_native(t)))
```

New text:

```
    native = tuple(sorted(entries.tree_ids()))
```

### `I7_tree_items_ignores_the_named_tree`

A rebuild of one named tree quietly rebuilds every tree in the library

- File: `src/cratekit/cli/rebuild.py`
- Surface: user
- Subset: test files importing cratekit.cli.rebuild
- Ran: `tests/test_routing_workers.py`
- Collected: 7136 against a baseline of 7136
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if tree_id is None:
        return native
    return tuple(t for t in native if t == tree_id)
```

New text:

```
    return native
```

### `R1_resort_drives_a_foreign_job`

The resort drives any queued job of any verb under its own envelope

- File: `src/cratekit/write/routing_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.routing_cli
- Ran: `tests/test_routing_workers.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_neither_resume_drives_another_verbs_job[resort]`

Old text:

```
    if job.handler_key != ctx.entry.handler_key:
        raise refuse(
            "job-unknown",
```

New text:

```
    if False:
        raise refuse(
            "job-unknown",
```

### `R2_rebuild_drives_a_foreign_job`

The rebuild drives another verb's job, without that verb's own resume checks

- File: `src/cratekit/cli/rebuild.py`
- Surface: user
- Subset: test files importing cratekit.cli.rebuild
- Ran: `tests/test_routing_workers.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_neither_resume_drives_another_verbs_job[rebuild]`

Old text:

```
    if job.handler_key != ctx.entry.handler_key:
        raise refuse(
            "job-unknown",
```

New text:

```
    if False:
        raise refuse(
            "job-unknown",
```

### `R3_resort_drives_an_itemless_job`

A resort queued by an older build drives to succeeded over a library nothing read

- File: `src/cratekit/write/routing_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.routing_cli
- Ran: `tests/test_routing_workers.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_neither_resume_drives_a_job_an_older_build_queued_with_no_items[resort]`

Old text:

```
        if not jobs.items(store, job.job_id):
            raise refuse(
                "internal-error",
```

New text:

```
        if False:
            raise refuse(
                "internal-error",
```

### `R4_rebuild_drives_an_itemless_job`

A rebuild queued by an older build drives to succeeded having rebuilt nothing

- File: `src/cratekit/cli/rebuild.py`
- Surface: user
- Subset: test files importing cratekit.cli.rebuild
- Ran: `tests/test_routing_workers.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_neither_resume_drives_a_job_an_older_build_queued_with_no_items[rebuild]`

Old text:

```
        if not jobs.items(store, job.job_id):
            raise refuse(
                "internal-error",
```

New text:

```
        if False:
            raise refuse(
                "internal-error",
```

### `R5_resort_swallows_the_jobs_cause`

A resort that failed half its trees exits zero, which is R-225 inherited

- File: `src/cratekit/write/routing_cli.py`
- Surface: user
- Subset: test files importing cratekit.write.routing_cli
- Ran: `tests/test_routing_workers.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_resume_whose_items_did_not_all_succeed_is_not_an_ok_exit[resort]`

Old text:

```
    if not job.is_open() and job.cause is not None:
        raise CratekitError(job.cause)
    return ctx.envelope(data=_reported(store, job), warnings=warnings)
```

New text:

```
    return ctx.envelope(data=_reported(store, job), warnings=warnings)
```

### `R6_rebuild_swallows_the_jobs_cause`

A rebuild that failed some of its trees exits zero over the rest of the library

- File: `src/cratekit/cli/rebuild.py`
- Surface: user
- Subset: test files importing cratekit.cli.rebuild
- Ran: `tests/test_routing_workers.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_resume_whose_items_did_not_all_succeed_is_not_an_ok_exit[rebuild]`

Old text:

```
    if not job.is_open() and job.cause is not None:
        raise CratekitError(job.cause)
    return ctx.envelope(
        data=_reported(store, job),
```

New text:

```
    return ctx.envelope(
        data=_reported(store, job),
```

### `E1_addressability_check_dropped`

Two destinations sharing one display pair are merged rather than refused, which writes one bucket's tracks into another's playlist

- File: `src/cratekit/write/rebuild.py`
- Surface: user
- Subset: test files importing cratekit.write.rebuild
- Ran: `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 7136 against a baseline of 7136
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    destinations = resolve_destinations(declared, placements, standing, record)
    assert_addressable(tree_id, destinations, standing)
```

New text:

```
    destinations = resolve_destinations(declared, placements, standing, record)
```

### `E2_rebuild_watch_narrowed`

The rebuild worker arms its analysis watch over the music directory, where no analysis file lives

- File: `src/cratekit/write/rebuild.py`
- Surface: user
- Subset: test files importing cratekit.write.rebuild
- Ran: `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 129 against a baseline of 129
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_driven_rebuild_watches_the_grids_where_they_actually_live`

Old text:

```
            analysis_roots=[Path(cfg.library.root)],
            vocal_threshold=vocal_threshold,
```

New text:

```
            analysis_roots=[Path(cfg.library.root) / cfg.library.music_dir],
            vocal_threshold=vocal_threshold,
```

