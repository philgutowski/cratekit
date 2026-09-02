# Mutation table: u52-item-derivation

Measured by `scripts/mutate.py` on 2026-09-02 21:44 UTC, branch `relay/70` at `3cde6ff`. Pass kind: full.

Baseline: green, 6695 collected. pytest invocations for this batch: 35.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6695 against 6695. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `I1_items_keyed_on_name` | `src/cratekit/label/cli.py` | user | 2 file(s) | 72 | 14 | killed |
| `I2_one_item_for_the_whole_registry` | `src/cratekit/label/cli.py` | user | 2 file(s) | 72 | 5 | killed |
| `I3_empty_registry_queues` | `src/cratekit/label/cli.py` | user | 2 file(s) | 72 | 3 | killed |
| `I4_registry_empty_message` | `src/cratekit/label/cli.py` | user | 2 file(s) | 6695 | 0 (promoted) | zero |
| `I5_import_queues_no_item` | `src/cratekit/label/cli.py` | user | 2 file(s) | 72 | 3 | killed |
| `I6_import_item_keyed_on_name` | `src/cratekit/label/cli.py` | user | 2 file(s) | 72 | 2 | killed |
| `S1_errors_branch_gone` | `src/cratekit/label/cli.py` | user | 2 file(s) | 72 | 1 | killed |
| `S2_empty_shortfall_branch_gone` | `src/cratekit/label/cli.py` | user | 2 file(s) | 72 | 2 | killed |
| `S3_and_dropped_conjunct_gone` | `src/cratekit/label/cli.py` | user | 2 file(s) | 72 | 2 | killed |
| `S4_and_shortfall_conjunct_gone` | `src/cratekit/label/cli.py` | user | 2 file(s) | 6695 | 0 (promoted) | zero |
| `S5_dropped_never_accumulated` | `src/cratekit/label/sweep.py` | user | 3 file(s) | 89 | 2 | killed |
| `A1_acquires_early_return_gone` | `src/cratekit/sync/run.py` | user | 2 file(s) | 45 | 3 | killed |
| `A2_acquires_default_false` | `src/cratekit/sync/run.py` | user | 2 file(s) | 45 | 6 | killed |
| `A3_label_source_acquires` | `src/cratekit/label/sweep.py` | user | 3 file(s) | 89 | 1 | killed |
| `L1_can_list_refusal_gone` | `src/cratekit/label/sweep.py` | user | 3 file(s) | 89 | 1 | killed |
| `L2_crawl_except_gone` | `src/cratekit/label/sweep.py` | user | 3 file(s) | 89 | 3 | killed |
| `L4_artist_for_wrapper_gone` | `src/cratekit/label/sweep.py` | user | 3 file(s) | 89 | 2 | killed |
| `L5_artist_for_missing_returns_none` | `src/cratekit/label/sweep.py` | user | 3 file(s) | 6695 | 0 (promoted) | zero |
| `L6_verifier_missing_returns_stub` | `src/cratekit/label/sweep.py` | user | 3 file(s) | 6695 | 0 (promoted) | zero |
| `L7_verifier_wrapper_gone` | `src/cratekit/label/sweep.py` | user | 3 file(s) | 89 | 1 | killed |
| `L8_verifier_passthrough_gone` | `src/cratekit/label/sweep.py` | user | 3 file(s) | 6695 | 0 (promoted) | zero |
| `C1_can_list_always_true` | `src/cratekit/label/crawl.py` | user | 1 file(s) | 28 | 1 | killed |
| `C2_can_list_requires_all` | `src/cratekit/label/crawl.py` | user | 1 file(s) | 28 | 3 | killed |
| `R1_itemless_job_drives` | `src/cratekit/label/cli.py` | user | 2 file(s) | 72 | 1 | killed |
| `R2_closed_cause_reraise_gone` | `src/cratekit/label/cli.py` | user | 2 file(s) | 72 | 2 | killed |
| `R3_closed_cause_narrowed_to_failed` | `src/cratekit/label/cli.py` | user | 2 file(s) | 6695 | 0 (promoted) | zero |
| `R4_reraise_inside_is_open` | `src/cratekit/label/cli.py` | user | 2 file(s) | 72 | 1 | killed |
| `H1_catalogue_not_resolved_first` | `src/cratekit/label/cli.py` | user | 2 file(s) | 72 | 11 | killed |
| `H2_listing_passthrough_gone` | `src/cratekit/label/cli.py` | user | 2 file(s) | 72 | 1 | killed |
| `H3_listing_translation_gone` | `src/cratekit/label/cli.py` | user | 2 file(s) | 72 | 2 | killed |
| `H4_verification_boundary_gone` | `src/cratekit/label/cli.py` | user | 2 file(s) | 72 | 2 | killed |
| `H5_verifier_passthrough_gone` | `src/cratekit/label/cli.py` | user | 2 file(s) | 6695 | 0 (promoted) | zero |
| `H6_empty_playlist_reports_ok` | `src/cratekit/label/cli.py` | user | 2 file(s) | 72 | 1 | killed |
| `H7_unresolved_drops_nameless` | `src/cratekit/label/cli.py` | user | 2 file(s) | 72 | 1 | killed |
| `F1_worker_loads_live_config` | `src/cratekit/label/cli.py` | user | 2 file(s) | 72 | 1 | killed |
| `B1_label_import_unbound` | `src/cratekit/cli/handlers.py` | user | 5 file(s) | 163 | 5 | killed |
| `B2_sync_labels_unbound` | `src/cratekit/cli/handlers.py` | user | 5 file(s) | 163 | 17 | killed |
| `B3_sync_labels_wrong_worker` | `src/cratekit/cli/handlers.py` | user | 5 file(s) | 163 | 13 | killed |
| `P1_revoked_tombstones_suppress` | `src/cratekit/label/sweep.py` | user | 3 file(s) | 6695 | 0 (promoted) | zero |
| `P2_snapshot_read_eagerly` | `src/cratekit/label/sweep.py` | user | 3 file(s) | 6695 | 0 (promoted) | zero |

## Zero rows and what they owe

- `I4_registry_empty_message` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `S4_and_shortfall_conjunct_gone` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `L5_artist_for_missing_returns_none` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `L6_verifier_missing_returns_stub` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `L8_verifier_passthrough_gone` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `R3_closed_cause_narrowed_to_failed` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `H5_verifier_passthrough_gone` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `P1_revoked_tombstones_suppress` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `P2_snapshot_read_eagerly` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Considered and dropped

METHOD caps a full pass at 45 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `L3_crawl_except_narrowed`: Narrow _crawl_or_refuse's broad except to a type this layer happens to know, such as ValueError Dropped because: ranked below the cap; L2 measures whether the translation exists at all, and the breadth is the same guard family with a strictly weaker mutation
- `S6_incomplete_remedy`: Flip the errors branch remedy from RESUME_JOB to REPORT_DEFECT Dropped because: ranked below the cap; S1 measures the whole branch and the remedy is one field inside a refusal S1 already removes
- `S7_dropped_appended_not_rebuilt`: Append to LabelSource.dropped rather than rebuilding it, so a second list_recent answers about both passes Dropped because: ranked below the cap and maintainer facing; the class is constructed fresh per queued item and label.cli.handle is its only constructor in src, so a second pass on one instance is not a reachable state today
- `C3_listing_methods_restated`: Replace the LISTING_METHODS derivation with a hand written tuple that has gone stale against the wrapper's signature Dropped because: ranked below the cap; whether it kills anything depends entirely on which method names the test fakes happen to expose, so the number would be about the fixtures rather than about the guard
- `P3_identity_short_circuit`: Change the artist and title short circuit from and to or Dropped because: ranked below the cap and maintainer facing; it is a performance short circuit carried over unchanged from the per release form rather than a decision this unit made
- `F2_increment_live_config`: Hand run_increment a freshly loaded configuration instead of the frozen one Dropped because: ranked below the cap; the acquires early return fires before the watermark store, the artifact registry and the staging path are ever used, so on this path the mutation changes no observable answer and a zero would say nothing
- `H8_nameless_counter`: Stop incrementing the nameless counter inside the extractor Dropped because: ranked below the cap; it is the same population H7 measures, reached one line earlier
- `E1_engine_lines`: Guards inside acquire/listing.py, core/jobs.py, core/review.py and label/harvest.py that this unit newly reaches Dropped because: out of scope by the rule U51's row spec states: this unit is their first caller and not their author, so a table over them measures those modules' suites rather than this binding

## Row definitions

### `I1_items_keyed_on_name`

Key a sweep's items on the display name instead of the label id, which is the rename hazard Seam R19 and the registry's D5 both forbid

- File: `src/cratekit/label/cli.py`
- Surface: user
- Subset: test files importing cratekit.label.cli
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 72 against a baseline of 72
- Kills: 14 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_catalogue_that_cannot_be_listed_fails_the_item_and_the_job`
  - `tests/test_label_workers.py::test_a_label_the_registry_no_longer_holds_refuses_rather_than_sweeping_nothing`
  - `tests/test_label_workers.py::test_a_label_whose_crawl_listed_nothing_at_all_still_succeeds`
  - `tests/test_label_workers.py::test_a_label_whose_every_release_is_tombstoned_still_succeeds`
  - `tests/test_label_workers.py::test_a_sweep_carries_the_identifier_and_never_the_display_name`
  - `tests/test_label_workers.py::test_a_sweep_queues_one_item_per_registered_label`
  - `tests/test_label_workers.py::test_a_sweep_runs_every_one_of_its_labels_from_pending_to_done`
  - `tests/test_label_workers.py::test_a_sweep_that_confirmed_none_of_what_it_read_fails_rather_than_succeeding`
  - `tests/test_label_workers.py::test_a_verification_call_that_raises_fails_the_item_in_the_lookup_vocabulary`
  - `tests/test_label_workers.py::test_an_increment_that_could_not_offer_every_release_fails_the_item`
  - `tests/test_label_workers.py::test_each_item_sweeps_its_own_label_and_not_one_named_by_the_payload`
  - `tests/test_label_workers.py::test_the_resume_envelope_is_exactly_job_state_and_nothing_beside_it`
  - `tests/test_label_workers.py::test_the_unconfirmed_refusal_says_how_many_were_read_and_that_the_provider_answered`
  - `tests/test_label_workers.py::test_the_worker_offers_into_the_library_its_job_was_queued_for`

Old text:

```
    return tuple(entry.label_id for entry in held.labels.values())
```

New text:

```
    return tuple(entry.name for entry in held.labels.values())
```

### `I2_one_item_for_the_whole_registry`

Queue ONE item for the whole registry rather than one per registered label, so a five label sweep sweeps one label

- File: `src/cratekit/label/cli.py`
- Surface: user
- Subset: test files importing cratekit.label.cli
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 72 against a baseline of 72
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_label_the_registry_no_longer_holds_refuses_rather_than_sweeping_nothing`
  - `tests/test_label_workers.py::test_a_sweep_carries_the_identifier_and_never_the_display_name`
  - `tests/test_label_workers.py::test_a_sweep_queues_one_item_per_registered_label`
  - `tests/test_label_workers.py::test_a_sweep_runs_every_one_of_its_labels_from_pending_to_done`
  - `tests/test_label_workers.py::test_each_item_sweeps_its_own_label_and_not_one_named_by_the_payload`

Old text:

```
    return tuple(entry.label_id for entry in held.labels.values())
```

New text:

```
    return tuple(entry.label_id for entry in held.labels.values())[:1]
```

### `I3_empty_registry_queues`

THE ZERO ITEM RULE at the sweep end: let an empty registry queue a job that drives straight to SUCCEEDED

- File: `src/cratekit/label/cli.py`
- Surface: user
- Subset: test files importing cratekit.label.cli
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 72 against a baseline of 72
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_refused_sweep_carries_no_warning_because_nothing_was_queued`
  - `tests/test_label_workers.py::test_a_sweep_with_an_empty_registry_refuses_and_queues_nothing`
  - `tests/test_label_workers.py::test_the_empty_registry_refusal_names_the_command_that_fixes_it`

Old text:

```
    items = sweep_items(labels.RegistryStore().load())
    if items:
        return items
```

New text:

```
    items = sweep_items(labels.RegistryStore().load())
    if True:
        return items
```

### `I4_registry_empty_message`

Reword the label-registry-empty sentence, never append to it, because the suite asserts with in

- File: `src/cratekit/label/cli.py`
- Surface: user
- Subset: test files importing cratekit.label.cli
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 6695 against a baseline of 6695
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        "no favourite label is registered, so a sweep would queue a job with "
        "nothing to claim and would then report that it succeeded",
```

New text:

```
        "the favourite label list holds nothing, so this sweep has no work in "
        "it and would finish by claiming a result it never produced",
```

### `I5_import_queues_no_item`

THE ZERO ITEM RULE at the import end: queue the single label job with no items at all

- File: `src/cratekit/label/cli.py`
- Surface: user
- Subset: test files importing cratekit.label.cli
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 72 against a baseline of 72
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_workers.py::test_an_import_queues_exactly_one_item_and_it_is_the_label_id`
  - `tests/test_label_workers.py::test_an_import_runs_its_one_item_to_done_through_the_same_worker`
  - `tests/test_label_workers.py::test_both_queueing_paths_warn_that_no_catalogue_adapter_is_bound[label.import]`

Old text:

```
        item_ids=(entry.label_id,),
```

New text:

```
        item_ids=(),
```

### `I6_import_item_keyed_on_name`

The import's single item names the label by display name, which the worker then cannot resolve by id

- File: `src/cratekit/label/cli.py`
- Surface: user
- Subset: test files importing cratekit.label.cli
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_workers.py::test_an_import_queues_exactly_one_item_and_it_is_the_label_id`
  - `tests/test_label_workers.py::test_an_import_runs_its_one_item_to_done_through_the_same_worker`

Old text:

```
        item_ids=(entry.label_id,),
```

New text:

```
        item_ids=(entry.name,),
```

### `S1_errors_branch_gone`

A sweep that could not offer some of the releases it listed exits 0 and reports the job done

- File: `src/cratekit/label/cli.py`
- Surface: user
- Subset: test files importing cratekit.label.cli
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_an_increment_that_could_not_offer_every_release_fails_the_item`

Old text:

```
    if result.errors:
        raise refuse(
            "label-sweep-incomplete",
```

New text:

```
    if False:
        raise refuse(
            "label-sweep-incomplete",
```

### `S2_empty_shortfall_branch_gone`

A catalogue that confirms nothing is reported as a label with nothing new, which is the defect this branch closed

- File: `src/cratekit/label/cli.py`
- Surface: user
- Subset: test files importing cratekit.label.cli
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_sweep_that_confirmed_none_of_what_it_read_fails_rather_than_succeeding`
  - `tests/test_label_workers.py::test_the_unconfirmed_refusal_says_how_many_were_read_and_that_the_provider_answered`

Old text:

```
    if result.shortfall == "empty" and source.dropped:
```

New text:

```
    if False:
```

### `S3_and_dropped_conjunct_gone`

MUTATE THE AND, first arm: drop the dropped population conjunct, so a genuinely exhausted crawl and a fully tombstoned label both refuse

- File: `src/cratekit/label/cli.py`
- Surface: user
- Subset: test files importing cratekit.label.cli
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_label_whose_crawl_listed_nothing_at_all_still_succeeds`
  - `tests/test_label_workers.py::test_a_label_whose_every_release_is_tombstoned_still_succeeds`

Old text:

```
    if result.shortfall == "empty" and source.dropped:
```

New text:

```
    if result.shortfall == "empty":
```

### `S4_and_shortfall_conjunct_gone`

MUTATE THE AND, second arm: drop the shortfall conjunct, so a sweep that offered plenty and dropped one release refuses

- File: `src/cratekit/label/cli.py`
- Surface: user
- Subset: test files importing cratekit.label.cli
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 6695 against a baseline of 6695
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if result.shortfall == "empty" and source.dropped:
```

New text:

```
    if source.dropped:
```

### `S5_dropped_never_accumulated`

Stop accumulating the dropped population in LabelSource.list_recent, so the refusal above can never see one

- File: `src/cratekit/label/sweep.py`
- Surface: user
- Subset: test files importing cratekit.label.sweep
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_workers.py`
- Collected: 89 against a baseline of 89
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_sweep_that_confirmed_none_of_what_it_read_fails_rather_than_succeeding`
  - `tests/test_label_workers.py::test_the_unconfirmed_refusal_says_how_many_were_read_and_that_the_provider_answered`

Old text:

```
            discarded.extend(listing.dropped)
```

New text:

```
            pass
```

### `A1_acquires_early_return_gone`

R-140: an offering source writes the intake row, registers the artifact and moves the watermark over releases nobody accepted

- File: `src/cratekit/sync/run.py`
- Surface: user
- Subset: test files importing cratekit.sync.run
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`
- Collected: 45 against a baseline of 45
- Kills: 3 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_an_offering_run_leaves_the_source_watermark_unset`
  - `tests/test_incremental_sync.py::test_an_offering_source_writes_no_intake_file`
  - `tests/test_incremental_sync.py::test_one_run_records_only_the_acquiring_source_of_a_mixed_pair`

Old text:

```
        if not getattr(source, "acquires", True):
```

New text:

```
        if False:
```

### `A2_acquires_default_false`

MUTATE THE COEFFICIENT: flip the getattr default, so every source written before the attribute existed stops recording what it acquired

- File: `src/cratekit/sync/run.py`
- Surface: user
- Subset: test files importing cratekit.sync.run
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`
- Collected: 45 against a baseline of 45
- Kills: 6 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_rerun_after_a_clean_sync_processes_only_unowned_items`
  - `tests/test_incremental_sync.py::test_a_watermark_does_not_empty_the_scope_of_unowned_items`
  - `tests/test_incremental_sync.py::test_an_acquiring_source_still_writes_the_intake_file_and_advances`
  - `tests/test_incremental_sync.py::test_one_run_records_only_the_acquiring_source_of_a_mixed_pair`
  - `tests/test_incremental_sync.py::test_one_source_failing_does_not_block_the_other`
  - `tests/test_incremental_sync.py::test_two_sources_in_one_run_share_one_importable_file`

Old text:

```
        if not getattr(source, "acquires", True):
```

New text:

```
        if not getattr(source, "acquires", False):
```

### `A3_label_source_acquires`

Declare the labels source an acquiring one, which is the state R-140 was recorded against

- File: `src/cratekit/label/sweep.py`
- Surface: user
- Subset: test files importing cratekit.label.sweep
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_workers.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_the_label_source_declares_that_it_does_not_acquire`

Old text:

```
    acquires = False
```

New text:

```
    acquires = True
```

### `L1_can_list_refusal_gone`

R-135: an artist object exposing none of the listing methods yields an empty list read as an empty catalogue

- File: `src/cratekit/label/sweep.py`
- Surface: user
- Subset: test files importing cratekit.label.sweep
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_workers.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_an_artist_exposing_no_listing_method_raises_rather_than_crawling_nothing`

Old text:

```
    if not crawl.can_list(artist):
```

New text:

```
    if False:
```

### `L2_crawl_except_gone`

REMOVE THE LAYER ALONE: an exception out of the crawl escapes untranslated instead of becoming a LookupFailure

- File: `src/cratekit/label/sweep.py`
- Surface: user
- Subset: test files importing cratekit.label.sweep
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_workers.py`
- Collected: 89 against a baseline of 89
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_listing_that_cannot_be_paged_raises_instead_of_reporting_empty`
  - `tests/modules/test_labels.py::test_a_provider_error_out_of_the_crawl_is_not_an_empty_catalogue`
  - `tests/modules/test_labels.py::test_an_unreadable_listing_stops_the_increment_at_the_lookup`

Old text:

```
    try:
        return list(crawl.releases(artist))
    except Exception as exc:
        raise run.LookupFailure(
            f"the catalogue listing for {entry.name!r} could not be read "
            f"({type(exc).__name__}: {exc}); that is not an empty catalogue"
        ) from exc
```

New text:

```
    return list(crawl.releases(artist))
```

### `L4_artist_for_wrapper_gone`

The seam's artist lookup raises the adapter's own exception past the increment instead of sync-source-lookups-failed

- File: `src/cratekit/label/sweep.py`
- Surface: user
- Subset: test files importing cratekit.label.sweep
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_workers.py`
- Collected: 89 against a baseline of 89
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_label_the_catalogue_cannot_resolve_stops_the_increment`
  - `tests/test_label_workers.py::test_a_catalogue_that_cannot_be_listed_fails_the_item_and_the_job`

Old text:

```
        if self.catalogue is not None:
            try:
                return self.catalogue.artist_for(entry)
            except Exception as exc:
                raise run.LookupFailure(
                    f"the catalogue could not resolve an artist for the label "
                    f"{entry.name!r} ({type(exc).__name__}: {exc}); its releases "
                    f"were never listed"
                ) from exc
```

New text:

```
        if self.catalogue is not None:
            return self.catalogue.artist_for(entry)
```

### `L5_artist_for_missing_returns_none`

The bare skip R-135 named in miniature: a label with no catalogue object at all returns None rather than refusing

- File: `src/cratekit/label/sweep.py`
- Surface: user
- Subset: test files importing cratekit.label.sweep
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_workers.py`
- Collected: 6695 against a baseline of 6695
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        raise run.LookupFailure(
            f"no catalogue object was available for the registered label "
            f"{entry.name!r}, so its releases were never listed; that is not "
            f"a label with nothing new"
        )
```

New text:

```
        return None
```

### `L6_verifier_missing_returns_stub`

A source built with neither verifier nor catalogue confirms nothing instead of refusing, so every release is dropped as unconfirmed

- File: `src/cratekit/label/sweep.py`
- Surface: user
- Subset: test files importing cratekit.label.sweep
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_workers.py`
- Collected: 6695 against a baseline of 6695
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        raise run.LookupFailure(
            "this labels source was built with neither a verification callable "
            "nor a catalogue, so no release it listed could be confirmed"
        )
```

New text:

```
        def unconfirmed(claimed: str, release: Any) -> Mapping[str, Any]:
            return {}

        return unconfirmed
```

### `L7_verifier_wrapper_gone`

THE NEW WRAPPER: return the bare seam method, which is the exact pre-fix shape that failed a provider outage as internal-error

- File: `src/cratekit/label/sweep.py`
- Surface: user
- Subset: test files importing cratekit.label.sweep
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_workers.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_verification_call_that_raises_fails_the_item_in_the_lookup_vocabulary`

Old text:

```
        if self.catalogue is not None:
            catalogue = self.catalogue

            def verified(claimed: str, release: Any) -> Mapping[str, Any]:
                try:
                    return catalogue.search_release(claimed, release)
                except CratekitError:
                    raise
                except Exception as exc:
                    raise run.LookupFailure(
                        f"the catalogue could not confirm who is credited on a "
                        f"release ({type(exc).__name__}: {exc}); the releases "
                        f"this sweep listed were never verified, and an "
                        f"unverified release is not a release with no match"
                    ) from exc

            return verified
```

New text:

```
        if self.catalogue is not None:
            return self.catalogue.search_release
```

### `L8_verifier_passthrough_gone`

REMOVE THE LAYER ALONE: an adapter's credential-missing refusal is flattened into this source could not list

- File: `src/cratekit/label/sweep.py`
- Surface: user
- Subset: test files importing cratekit.label.sweep
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_workers.py`
- Collected: 6695 against a baseline of 6695
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                except CratekitError:
                    raise
                except Exception as exc:
```

New text:

```
                except Exception as exc:
```

### `C1_can_list_always_true`

Answer yes for every object, which is what makes the refusal above unreachable from the other side

- File: `src/cratekit/label/crawl.py`
- Surface: user
- Subset: test files importing cratekit.label.crawl
- Ran: `tests/modules/test_labels.py`
- Collected: 28 against a baseline of 28
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_an_artist_exposing_no_listing_method_raises_rather_than_crawling_nothing`

Old text:

```
    return any(getattr(artist, method, None) is not None for method in LISTING_METHODS)
```

New text:

```
    return True
```

### `C2_can_list_requires_all`

Require EVERY listing method rather than any, so a client exposing one of two is refused instead of half read

- File: `src/cratekit/label/crawl.py`
- Surface: user
- Subset: test files importing cratekit.label.crawl
- Ran: `tests/modules/test_labels.py`
- Collected: 28 against a baseline of 28
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_listing_that_cannot_be_paged_raises_instead_of_reporting_empty`
  - `tests/modules/test_labels.py::test_a_provider_error_out_of_the_crawl_is_not_an_empty_catalogue`
  - `tests/modules/test_labels.py::test_one_working_listing_with_no_releases_still_reports_empty`

Old text:

```
    return any(getattr(artist, method, None) is not None for method in LISTING_METHODS)
```

New text:

```
    return all(getattr(artist, method, None) is not None for method in LISTING_METHODS)
```

### `R1_itemless_job_drives`

Drive a label job with no items, which jobs.drive transitions straight to SUCCEEDED over a registry nothing was read from

- File: `src/cratekit/label/cli.py`
- Surface: user
- Subset: test files importing cratekit.label.cli
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_job_carrying_no_items_refuses_on_resume_and_is_left_open`

Old text:

```
            _refuse_an_itemless_job(store, job)
```

New text:

```
            pass
```

### `R2_closed_cause_reraise_gone`

R-225 restored: a job recorded failed or cancelled reports through a normal envelope and exits 0

- File: `src/cratekit/label/cli.py`
- Surface: user
- Subset: test files importing cratekit.label.cli
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_label_the_registry_no_longer_holds_refuses_rather_than_sweeping_nothing`
  - `tests/test_label_workers.py::test_a_second_resume_of_a_failed_sweep_still_does_not_exit_ok`

Old text:

```
        if not job.is_open() and job.cause is not None:
            raise CratekitError(job.cause)
```

New text:

```
        if False and job.cause is not None:
            raise CratekitError(job.cause)
```

### `R3_closed_cause_narrowed_to_failed`

Narrow the predicate back to FAILED alone, which exits 0 over a CANCELLED job with 0 of 3 items done

- File: `src/cratekit/label/cli.py`
- Surface: user
- Subset: test files importing cratekit.label.cli
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 6695 against a baseline of 6695
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if not job.is_open() and job.cause is not None:
```

New text:

```
        if job.state is jobs.JobState.FAILED and job.cause is not None:
```

### `R4_reraise_inside_is_open`

THE LOAD BEARING PLACEMENT: put the check back inside the is_open branch, so a job already closed on entry reports a normal envelope for ever after

- File: `src/cratekit/label/cli.py`
- Surface: user
- Subset: test files importing cratekit.label.cli
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_second_resume_of_a_failed_sweep_still_does_not_exit_ok`

Old text:

```
        job = jobs.reconcile(store, job_id)
        warnings: tuple[dict[str, str], ...] = ()
```

New text:

```
        job = jobs.reconcile(store, job_id)
        warnings: tuple[dict[str, str], ...] = ()
        if not job.is_open():
            return ctx.envelope(data=_reported(store, job), warnings=warnings)
```

### `H1_catalogue_not_resolved_first`

R13: an unbound build reaches the listing with no catalogue and earns label-playlist-unreadable about a provider it never had

- File: `src/cratekit/label/cli.py`
- Surface: user
- Subset: test files importing cratekit.label.cli
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 72 against a baseline of 72
- Kills: 11 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_harvest_on_a_build_with_no_adapter_refuses_that_nothing_is_bound`
  - `tests/modules/test_labels.py::test_harvest_with_no_provider_session_refuses_the_credential_instead`
  - `tests/test_label_workers.py::test_a_cratekit_refusal_from_below_is_not_flattened_into_an_unreadable_playlist`
  - `tests/test_label_workers.py::test_a_harvest_that_fails_mid_verification_names_what_it_already_offered`
  - `tests/test_label_workers.py::test_a_name_the_catalogue_will_not_confirm_is_counted_and_never_offered`
  - `tests/test_label_workers.py::test_a_playlist_that_resolves_and_cannot_be_listed_refuses_the_same_way`
  - `tests/test_label_workers.py::test_a_playlist_the_catalogue_cannot_resolve_refuses_that_it_was_unreadable`
  - `tests/test_label_workers.py::test_a_track_with_no_copyright_string_is_counted_rather_than_dropped_silently`
  - `tests/test_label_workers.py::test_an_empty_playlist_offers_nothing_and_reports_zero_rather_than_refusing`
  - `tests/test_label_workers.py::test_harvest_of_a_readable_playlist_offers_one_item_per_verified_label`
  - `tests/test_label_workers.py::test_harvest_payload_is_exactly_the_three_declared_review_set_keys`

Old text:

```
    found = catalogue.resolve(cfg)
```

New text:

```
    found = catalogue.resolve(cfg) if catalogue.bound() else None
```

### `H2_listing_passthrough_gone`

REMOVE THE LAYER ALONE: an adapter's own CratekitError refusal is rewritten as an unreadable playlist

- File: `src/cratekit/label/cli.py`
- Surface: user
- Subset: test files importing cratekit.label.cli
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_cratekit_refusal_from_below_is_not_flattened_into_an_unreadable_playlist`

Old text:

```
    except CratekitError:
        raise
    except Exception as exc:
        raise refuse(
            "label-playlist-unreadable",
            f"the playlist {reference!r} could not be listed by the provider "
```

New text:

```
    except Exception as exc:
        raise refuse(
            "label-playlist-unreadable",
            f"the playlist {reference!r} could not be listed by the provider "
```

### `H3_listing_translation_gone`

A provider failure while resolving or listing the playlist escapes as an unclassified crash rather than a refusal

- File: `src/cratekit/label/cli.py`
- Surface: user
- Subset: test files importing cratekit.label.cli
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_playlist_that_resolves_and_cannot_be_listed_refuses_the_same_way`
  - `tests/test_label_workers.py::test_a_playlist_the_catalogue_cannot_resolve_refuses_that_it_was_unreadable`

Old text:

```
    try:
        playlist = found.playlist_for(reference)
        return harvest.playlist_tracks(playlist)
    except CratekitError:
        raise
    except Exception as exc:
        raise refuse(
            "label-playlist-unreadable",
            f"the playlist {reference!r} could not be listed by the provider "
            f"({exc}); harvest needs a reachable provider playlist and will not "
            f"invent labels",
            steps=("pass a playlist this account can read, then retry",),
            origin=("label.cli",),
            detail={"playlist": reference, "kind": type(exc).__name__},
        ) from exc
```

New text:

```
    playlist = found.playlist_for(reference)
    return harvest.playlist_tracks(playlist)
```

### `H4_verification_boundary_gone`

THE THIRD PROVIDER CALL: hand from_tracks the bare seam method, so a provider that went away mid playlist becomes internal-error with report-defect

- File: `src/cratekit/label/cli.py`
- Surface: user
- Subset: test files importing cratekit.label.cli
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_harvest_that_fails_mid_verification_names_what_it_already_offered`
  - `tests/test_label_workers.py::test_a_provider_that_fails_mid_verification_refuses_rather_than_reporting_a_defect`

Old text:

```
            verify=_label_verifier(found, reference),
```

New text:

```
            verify=found.check_label,
```

### `H5_verifier_passthrough_gone`

REMOVE THE LAYER ALONE: the verification boundary swallows an adapter's own refusal into label-playlist-unreadable

- File: `src/cratekit/label/cli.py`
- Surface: user
- Subset: test files importing cratekit.label.cli
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 6695 against a baseline of 6695
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        except CratekitError:
            raise
        except Exception as exc:
```

New text:

```
        except Exception as exc:
```

### `H6_empty_playlist_reports_ok`

An empty playlist reports OK rather than NO_OP, so nothing found is indistinguishable from something found

- File: `src/cratekit/label/cli.py`
- Surface: user
- Subset: test files importing cratekit.label.cli
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_an_empty_playlist_offers_nothing_and_reports_zero_rather_than_refusing`

Old text:

```
        outcome=Outcome.OK if report.offered else Outcome.NO_OP,
```

New text:

```
        outcome=Outcome.OK,
```

### `H7_unresolved_drops_nameless`

Count only the names a catalogue refused, so a playlist whose tracks carry no copyright string at all reports a clean zero unresolved

- File: `src/cratekit/label/cli.py`
- Surface: user
- Subset: test files importing cratekit.label.cli
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_track_with_no_copyright_string_is_counted_rather_than_dropped_silently`

Old text:

```
    unresolved = len(report.dropped) + nameless
```

New text:

```
    unresolved = len(report.dropped)
```

### `F1_worker_loads_live_config`

R17: the worker builds its source against a freshly loaded configuration, so the offers are written under this run's library rather than the frozen one

- File: `src/cratekit/label/cli.py`
- Surface: user
- Subset: test files importing cratekit.label.cli
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_the_worker_offers_into_the_library_its_job_was_queued_for`

Old text:

```
    source = sweep.LabelSource(
        cfg,
```

New text:

```
    source = sweep.LabelSource(
        config.load(),
```

### `B1_label_import_unbound`

Unbind label.import, leaving a queued job with a worker in neither table

- File: `src/cratekit/cli/handlers.py`
- Surface: user
- Subset: test files importing cratekit.cli.handlers
- Ran: `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_label_workers.py`, `tests/test_master_cli.py`, `tests/test_outbound_workers.py`
- Collected: 163 against a baseline of 163
- Kills: 5 (killed)
- Killed:
  - `tests/test_handlers.py::test_every_queued_verb_is_either_bound_or_named_as_unbound`
  - `tests/test_label_workers.py::test_an_import_runs_its_one_item_to_done_through_the_same_worker`
  - `tests/test_label_workers.py::test_both_label_keys_report_a_bound_worker_rather_than_a_reason_they_have_none`
  - `tests/test_label_workers.py::test_neither_label_key_is_recorded_as_unbound_now_that_both_are_bound`
  - `tests/test_label_workers.py::test_one_worker_serves_both_label_keys`

Old text:

```
    "label.import": "cratekit.label.cli:handle",
```

New text:

```
(empty)
```

### `B2_sync_labels_unbound`

Unbind sync.labels, leaving a queued sweep with a worker in neither table

- File: `src/cratekit/cli/handlers.py`
- Surface: user
- Subset: test files importing cratekit.cli.handlers
- Ran: `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_label_workers.py`, `tests/test_master_cli.py`, `tests/test_outbound_workers.py`
- Collected: 163 against a baseline of 163
- Kills: 17 (killed)
- Killed:
  - `tests/test_handlers.py::test_every_queued_verb_is_either_bound_or_named_as_unbound`
  - `tests/test_label_workers.py::test_a_catalogue_that_cannot_be_listed_fails_the_item_and_the_job`
  - `tests/test_label_workers.py::test_a_label_the_registry_no_longer_holds_refuses_rather_than_sweeping_nothing`
  - `tests/test_label_workers.py::test_a_label_whose_crawl_listed_nothing_at_all_still_succeeds`
  - `tests/test_label_workers.py::test_a_label_whose_every_release_is_tombstoned_still_succeeds`
  - `tests/test_label_workers.py::test_a_second_resume_of_a_failed_sweep_still_does_not_exit_ok`
  - `tests/test_label_workers.py::test_a_sweep_runs_every_one_of_its_labels_from_pending_to_done`
  - `tests/test_label_workers.py::test_a_sweep_that_confirmed_none_of_what_it_read_fails_rather_than_succeeding`
  - `tests/test_label_workers.py::test_a_verification_call_that_raises_fails_the_item_in_the_lookup_vocabulary`
  - `tests/test_label_workers.py::test_an_increment_that_could_not_offer_every_release_fails_the_item`
  - `tests/test_label_workers.py::test_both_label_keys_report_a_bound_worker_rather_than_a_reason_they_have_none`
  - `tests/test_label_workers.py::test_each_item_sweeps_its_own_label_and_not_one_named_by_the_payload`
  - `tests/test_label_workers.py::test_neither_label_key_is_recorded_as_unbound_now_that_both_are_bound`
  - `tests/test_label_workers.py::test_one_worker_serves_both_label_keys`
  - `tests/test_label_workers.py::test_the_resume_envelope_is_exactly_job_state_and_nothing_beside_it`
  - ... and 2 more, see the JSON sidecar

Old text:

```
    "sync.labels": "cratekit.label.cli:handle",
```

New text:

```
(empty)
```

### `B3_sync_labels_wrong_worker`

Point sync.labels at the favorites worker, which asks whether anything checks the TARGET or only that the key is present

- File: `src/cratekit/cli/handlers.py`
- Surface: user
- Subset: test files importing cratekit.cli.handlers
- Ran: `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_label_workers.py`, `tests/test_master_cli.py`, `tests/test_outbound_workers.py`
- Collected: 163 against a baseline of 163
- Kills: 13 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_catalogue_that_cannot_be_listed_fails_the_item_and_the_job`
  - `tests/test_label_workers.py::test_a_label_the_registry_no_longer_holds_refuses_rather_than_sweeping_nothing`
  - `tests/test_label_workers.py::test_a_label_whose_crawl_listed_nothing_at_all_still_succeeds`
  - `tests/test_label_workers.py::test_a_label_whose_every_release_is_tombstoned_still_succeeds`
  - `tests/test_label_workers.py::test_a_sweep_runs_every_one_of_its_labels_from_pending_to_done`
  - `tests/test_label_workers.py::test_a_sweep_that_confirmed_none_of_what_it_read_fails_rather_than_succeeding`
  - `tests/test_label_workers.py::test_a_verification_call_that_raises_fails_the_item_in_the_lookup_vocabulary`
  - `tests/test_label_workers.py::test_an_increment_that_could_not_offer_every_release_fails_the_item`
  - `tests/test_label_workers.py::test_each_item_sweeps_its_own_label_and_not_one_named_by_the_payload`
  - `tests/test_label_workers.py::test_one_worker_serves_both_label_keys`
  - `tests/test_label_workers.py::test_the_resume_envelope_is_exactly_job_state_and_nothing_beside_it`
  - `tests/test_label_workers.py::test_the_unconfirmed_refusal_says_how_many_were_read_and_that_the_provider_answered`
  - `tests/test_label_workers.py::test_the_worker_offers_into_the_library_its_job_was_queued_for`

Old text:

```
    "sync.labels": "cratekit.label.cli:handle",
```

New text:

```
    "sync.labels": "cratekit.favorites.cli:handle",
```

### `P1_revoked_tombstones_suppress`

Snapshot revoked tombstones too, so a lifted suppression silently keeps a release out of the review queue

- File: `src/cratekit/label/sweep.py`
- Surface: user
- Subset: test files importing cratekit.label.sweep
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_workers.py`
- Collected: 6695 against a baseline of 6695
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            snapshot = {record.suppression_id for record in store.suppressions()}
```

New text:

```
            snapshot = {
                record.suppression_id
                for record in store.suppressions(include_revoked=True)
            }
```

### `P2_snapshot_read_eagerly`

THE LAZY READ: take the snapshot when the reader is built, which fires the unreadable store refusal on a label that has no confirmed release to ask about

- File: `src/cratekit/label/sweep.py`
- Surface: user
- Subset: test files importing cratekit.label.sweep
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_workers.py`
- Collected: 6695 against a baseline of 6695
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    snapshot: set[str] | None = None
```

New text:

```
    snapshot: set[str] | None = {
        record.suppression_id
        for record in DecisionStore(tombstone.STORE_KEY, cfg).suppressions()
    }
```

