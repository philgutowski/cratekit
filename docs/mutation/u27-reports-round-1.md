# Mutation table: u27-reports-round-1

Measured by `scripts/mutate.py` on 2026-08-23 14:45 UTC, branch `unit/u27-reports-cli` at `3ee992f`. Pass kind: light.

Baseline: green, 6115 collected. pytest invocations for this batch: 32.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6115 against 6115. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `C1_tree_absent_refusal` | `src/cratekit/modules/reports/coverage.py` | user | 1 file(s) | 20 | 1 | killed |
| `C2_tree_anchored_at_zero` | `src/cratekit/modules/reports/coverage.py` | user | 1 file(s) | 20 | 1 | killed |
| `C3_uncovered_order` | `src/cratekit/modules/reports/coverage.py` | user | 1 file(s) | 6115 | 0 (promoted) | zero |
| `C4_placement_count` | `src/cratekit/modules/reports/coverage.py` | user | 1 file(s) | 20 | 1 | killed |
| `L1_distinct_tracks` | `src/cratekit/modules/reports/library.py` | user | 1 file(s) | 20 | 1 | killed |
| `L2_genre_parent` | `src/cratekit/modules/reports/library.py` | user | 1 file(s) | 6115 | 0 (promoted) | zero |
| `L3_empty_tempo_is_zero` | `src/cratekit/modules/reports/library.py` | user | 1 file(s) | 20 | 1 | killed |
| `L4_median_even` | `src/cratekit/modules/reports/library.py` | user | 1 file(s) | 20 | 1 | killed |
| `L5_unused_buckets` | `src/cratekit/modules/reports/library.py` | user | 1 file(s) | 20 | 1 | killed |
| `L6_entries_in_no_playlist` | `src/cratekit/modules/reports/library.py` | user | 1 file(s) | 20 | 1 | killed |
| `L7_shape_governed_filter` | `src/cratekit/modules/reports/library.py` | user | 1 file(s) | 20 | 2 | killed |
| `S1_limit_floor` | `src/cratekit/cli/reports.py` | user | full suite | 6115 | 1 | killed |
| `S2_truncation_row` | `src/cratekit/cli/reports.py` | user | full suite | 6115 | 2 | killed |
| `S3_summary_total` | `src/cratekit/cli/reports.py` | user | full suite | 6115 | 2 | killed |
| `S4_as_of_refusal` | `src/cratekit/cli/reports.py` | user | full suite | 6115 | 1 | killed |
| `S5_handler_key` | `src/cratekit/cli/reports.py` | user | full suite | 6115 | 0 | zero |
| `S6_lossy_marker` | `src/cratekit/cli/reports.py` | user | full suite | 6115 | 3 | killed |
| `D1_probe_creates` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 6115 | 0 (promoted) | zero |
| `D2_required_gate` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 945 | 1 | killed |
| `D3_trash_remedy` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 945 | 1 | killed |
| `D4_probe_refusal_classification` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 945 | 1 | killed |
| `R1_delete_review_precondition` | `src/cratekit/cli/registry.py` | user | 14 file(s) | 2707 | 1 | killed |
| `R2_governed_tree_code` | `src/cratekit/core/cause.py` | user | 26 file(s) | 3567 | 1 | killed |

## Zero rows and what they owe

- `C3_uncovered_order` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `L2_genre_parent` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `S5_handler_key` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `D1_probe_creates` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Considered and dropped

METHOD caps a light pass at 25 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `T1_floor_exclusion_assertions`: Drop the two assertions guarding U34's floor exclusion in tests/modules/test_reports.py Dropped because: ranked below the cap and it is a guard over a guard: nothing in the suite tests a test module's own assertion, so the row is a structural zero by construction rather than a measurement. Recorded here so the gap is visible.
- `T2_engine_docstring_claims`: Reword the two engines' refusal sentences to check the suite asserts on wording Dropped because: ranked below the cap. The message assertions in tests/modules/test_reports_engines.py assert on the reason slug and the detail mapping rather than on prose, which is deliberate, so a reword row would measure the absence of a coupling this unit chose not to create.

## Row definitions

### `C1_tree_absent_refusal`

Drop the refusal for a governed tree the export does not hold, so every entry reports uncovered

- File: `src/cratekit/modules/reports/coverage.py`
- Surface: user
- Subset: test files importing cratekit.modules.reports.coverage
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_tree_the_export_does_not_hold_refuses_rather_than_reporting_everything`

Old text:

```
    if not view.has_folder(tree.display):
        raise _refuse_absent(tree)

```

New text:

```
(empty)
```

### `C2_tree_anchored_at_zero`

Anchor the governed-path filter at position zero, the shape that reported nothing for a nested tree

- File: `src/cratekit/modules/reports/coverage.py`
- Surface: user
- Subset: test files importing cratekit.modules.reports.coverage
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_tree_nested_inside_another_folder_is_still_the_governed_tree`

Old text:

```
        playlist.path for playlist in view.playlists if wanted in playlist.path[:-1]
```

New text:

```
        playlist.path for playlist in view.playlists if playlist.path[:1] == (wanted,)
```

### `C3_uncovered_order`

Drop the deterministic order, so two runs of one library render differently

- File: `src/cratekit/modules/reports/coverage.py`
- Surface: user
- Subset: test files importing cratekit.modules.reports.coverage
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 6115 against a baseline of 6115
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        uncovered=tuple(sorted(uncovered, key=_by_name)),
```

New text:

```
        uncovered=tuple(uncovered),
```

### `C4_placement_count`

Keep only the first placement per track, so a track filed twice reports one

- File: `src/cratekit/modules/reports/coverage.py`
- Surface: user
- Subset: test files importing cratekit.modules.reports.coverage
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_covered_track_names_every_path_under_the_tree_that_holds_it`

Old text:

```
            held.setdefault(track_id, []).append(playlist.path)
```

New text:

```
            held.setdefault(track_id, [playlist.path])
```

### `L1_distinct_tracks`

Sum the sub-playlists instead of counting distinct tracks, the double count the docstring names

- File: `src/cratekit/modules/reports/library.py`
- Surface: user
- Subset: test files importing cratekit.modules.reports.library
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_genre_counts_distinct_tracks_rather_than_summing_its_playlists`

Old text:

```
                tracks=len(tracks),
```

New text:

```
                tracks=playlists and sum(len(p.track_ids) for p in view.playlists if p.path[: len(folder)] == folder and len(p.path) > len(folder)),
```

### `L2_genre_parent`

Loosen the genre filter from the tree being the folder's parent to appearing anywhere in its path

- File: `src/cratekit/modules/reports/library.py`
- Surface: user
- Subset: test files importing cratekit.modules.reports.library
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 6115 against a baseline of 6115
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if len(folder) < 2 or folder[-2] != tree_display:
```

New text:

```
        if len(folder) < 2 or tree_display not in folder:
```

### `L3_empty_tempo_is_zero`

Report an unreadable library as a tempo range of zero rather than as unknown

- File: `src/cratekit/modules/reports/library.py`
- Surface: user
- Subset: test files importing cratekit.modules.reports.library
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_library_with_no_readable_head_reports_none_rather_than_zero`

Old text:

```
    if not found:
        return TempoSpread(readable=0, unreadable=unreadable)

```

New text:

```
    if not found:
        return TempoSpread(
            readable=0, unreadable=unreadable, lowest=0.0, highest=0.0, median=0.0
        )

```

### `L4_median_even`

Take the upper middle instead of averaging the pair on an even population

- File: `src/cratekit/modules/reports/library.py`
- Surface: user
- Subset: test files importing cratekit.modules.reports.library
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_tempo_median_over_an_even_population_averages_the_middle_pair`

Old text:

```
    if len(ordered) % 2:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2

```

New text:

```
    return ordered[middle]

```

### `L5_unused_buckets`

Report no unused buckets at all

- File: `src/cratekit/modules/reports/library.py`
- Surface: user
- Subset: test files importing cratekit.modules.reports.library
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_declared_bucket_with_no_folder_is_a_gap`

Old text:

```
            unused_buckets=tuple(sorted(declared_ids - present_ids)),
```

New text:

```
            unused_buckets=(),
```

### `L6_entries_in_no_playlist`

Count every entry as in no playlist

- File: `src/cratekit/modules/reports/library.py`
- Surface: user
- Subset: test files importing cratekit.modules.reports.library
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_the_gaps_count_entries_with_no_head_and_entries_in_no_playlist`

Old text:

```
            entries_in_no_playlist=sum(1 for entry in view.entries if not entry.playlists),
```

New text:

```
            entries_in_no_playlist=len(view.entries),
```

### `L7_shape_governed_filter`

Measure the tree shape over every folder in the export rather than the governed tree

- File: `src/cratekit/modules/reports/library.py`
- Surface: user
- Subset: test files importing cratekit.modules.reports.library
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 20 against a baseline of 20
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_taxonomy_whose_tree_this_library_does_not_use_reports_no_genres`
  - `tests/modules/test_reports_engines.py::test_the_shape_measures_the_governed_tree_from_its_own_node`

Old text:

```
    governed_folders = [
        path for path in view.folders if tree_display == path[-1] or tree_display in path[:-1]
    ]

```

New text:

```
    governed_folders = list(view.folders)

```

### `S1_limit_floor`

Pass the limit through unfloored, so a negative one becomes a slice from the end

- File: `src/cratekit/cli/reports.py`
- Surface: user
- Subset: full suite (test files importing cratekit.cli.reports: none found)
- Collected: 6115 against a baseline of 6115
- Kills: 1 (killed)
- Killed:
  - `tests/test_reports_cli.py::test_a_negative_limit_is_read_as_zero_rather_than_as_a_slice_from_the_end`

Old text:

```
    limit = max(0, int(ctx.args.limit))
```

New text:

```
    limit = int(ctx.args.limit)
```

### `S2_truncation_row`

Drop the row that says the list was capped

- File: `src/cratekit/cli/reports.py`
- Surface: user
- Subset: full suite (test files importing cratekit.cli.reports: none found)
- Collected: 6115 against a baseline of 6115
- Kills: 2 (killed)
- Killed:
  - `tests/test_reports_cli.py::test_a_limit_of_zero_lists_nothing_and_still_counts_everything`
  - `tests/test_reports_cli.py::test_a_limit_that_drops_rows_says_so_and_still_reports_the_true_total`

Old text:

```
    if len(listed) < len(report.uncovered):
        findings.append(
            Finding(
                key="coverage.truncated",
                title="the list above is not the whole answer",
                status=Status.INFO,
                detail=(
                    f"{len(listed)} of {len(report.uncovered)} uncovered tracks "
                    f"are listed; raise the limit to see the rest"
                ),
            )
        )

```

New text:

```
(empty)
```

### `S3_summary_total`

Derive the summary total from the truncated list, the arithmetic that hides the cap

- File: `src/cratekit/cli/reports.py`
- Surface: user
- Subset: full suite (test files importing cratekit.cli.reports: none found)
- Collected: 6115 against a baseline of 6115
- Kills: 2 (killed)
- Killed:
  - `tests/test_reports_cli.py::test_a_limit_of_zero_lists_nothing_and_still_counts_everything`
  - `tests/test_reports_cli.py::test_a_limit_that_drops_rows_says_so_and_still_reports_the_true_total`

Old text:

```
            "uncovered": len(report.uncovered),
```

New text:

```
            "uncovered": len(listed),
```

### `S4_as_of_refusal`

Default a malformed as-of value to today rather than refusing

- File: `src/cratekit/cli/reports.py`
- Surface: user
- Subset: full suite (test files importing cratekit.cli.reports: none found)
- Collected: 6115 against a baseline of 6115
- Kills: 1 (killed)
- Killed:
  - `tests/test_reports_cli.py::test_an_as_of_that_is_not_a_date_refuses_rather_than_answering_for_today`

Old text:

```
    written = getattr(ctx.args, "as_of", None)
    if not written:
        return datetime.now(timezone.utc).date()
    try:
        return date.fromisoformat(written)
    except ValueError as exc:
        raise refuse(
            "report-as-of-invalid",
            f"{written!r} is not a date; an aging report run for a day nobody "
            f"can name would band every grouping against a value this shell "
            f"invented",
            remedy=Remedy.FIX_COMMAND_LINE,
            steps=("pass the as-of flag as an ISO date, for example 2026-08-23",),
        ) from exc

```

New text:

```
    written = getattr(ctx.args, "as_of", None)
    try:
        return date.fromisoformat(written or "")
    except ValueError:
        return datetime.now(timezone.utc).date()

```

### `S5_handler_key`

Offer duplicate items without the verb's handler key, so the queue cannot show them by name

- File: `src/cratekit/cli/reports.py`
- Surface: user
- Subset: full suite (test files importing cratekit.cli.reports: none found)
- Collected: 6115 against a baseline of 6115
- Kills: 0 (zero)
- Note: measured on the full suite

Old text:

```
            view, store, template=_template(cfg), handler_key=ctx.entry.handler_key
```

New text:

```
            view, store, template=_template(cfg)
```

### `S6_lossy_marker`

Build the naming template without the configured lossy marker

- File: `src/cratekit/cli/reports.py`
- Surface: user
- Subset: full suite (test files importing cratekit.cli.reports: none found)
- Collected: 6115 against a baseline of 6115
- Kills: 3 (killed)
- Killed:
  - `tests/test_reports_cli.py::test_a_rejected_pair_comes_back_suppressed_rather_than_as_a_question`
  - `tests/test_reports_cli.py::test_a_second_run_re_offers_the_same_item_rather_than_a_second_one`
  - `tests/test_reports_cli.py::test_duplicates_offers_the_pair_into_the_queue_under_its_own_handler_key`

Old text:

```
    marker = (cfg.naming.lossy_marker or "").strip()
    if not marker:
        return NameTemplate()
    return NameTemplate(markers=(MarkerRule(field="lossy", literal=marker),))

```

New text:

```
    return NameTemplate()

```

### `D1_probe_creates`

Let the doctor probe create the Trash it is asking about, so the check passes by having run

- File: `src/cratekit/cli/doctor.py`
- Surface: user
- Subset: test files importing cratekit.cli.doctor
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 6115 against a baseline of 6115
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return trash.probe(path, create=False)
```

New text:

```
    return trash.probe(path, create=True)
```

### `D2_required_gate`

Report a broken Trash as a failure even where no verb needs it

- File: `src/cratekit/cli/doctor.py`
- Surface: user
- Subset: test files importing cratekit.cli.doctor
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 945 against a baseline of 945
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_broken_trash_is_informational_when_no_verb_this_profile_needs_it`

Old text:

```
    if not inputs.required(key):
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"{status.problem}, and no verb this profile switches on moves a "
                f"file to the Trash, so nothing depends on it today"
            ),
        )

```

New text:

```
(empty)
```

### `D3_trash_remedy`

Answer a broken Trash with run-doctor, which is the token that sends a person here

- File: `src/cratekit/cli/doctor.py`
- Surface: user
- Subset: test files importing cratekit.cli.doctor
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 945 against a baseline of 945
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_volume_with_no_usable_trash_refuses_because_a_verb_depends_on_it`

Old text:

```
        remedy=Remedy.GRANT_PATH_ACCESS,
```

New text:

```
        remedy=Remedy.RUN_DOCTOR,
```

### `D4_probe_refusal_classification`

Drop the access classification when the operating system refuses the probe

- File: `src/cratekit/cli/doctor.py`
- Surface: user
- Subset: test files importing cratekit.cli.doctor
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 945 against a baseline of 945
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_trash_probe_the_operating_system_refuses_is_a_failure_with_the_right_act`

Old text:

```
            remedy=access_remedy(exc, otherwise=Remedy.REPORT_DEFECT),
            error=exc,
        )
    if status.usable:
```

New text:

```
            remedy=Remedy.REPORT_DEFECT,
        )
    if status.usable:
```

### `R1_delete_review_precondition`

Stop delete.review declaring the Trash check as a precondition

- File: `src/cratekit/cli/registry.py`
- Surface: user
- Subset: test files importing cratekit.cli.registry
- Ran: `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_layering.py`, `tests/test_match_states.py`, `tests/test_packaging.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_write_session.py`
- Collected: 2707 against a baseline of 2707
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_volume_with_no_usable_trash_refuses_because_a_verb_depends_on_it`

Old text:

```
            "library.identity",
            "library.trash",
            "rekordbox.closed",
```

New text:

```
            "library.identity",
            "rekordbox.closed",
```

### `R2_governed_tree_code`

Move the governed-tree refusal off the library-prerequisite code

- File: `src/cratekit/core/cause.py`
- Surface: user
- Subset: test files importing cratekit.core.cause
- Ran: `tests/intake/test_collection_xml.py`, `tests/intake/test_pipeline.py`, `tests/modules/test_labels.py`, `tests/modules/test_outbound.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/test_adoption.py`, `tests/test_cli_contract.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_incremental_sync.py`, `tests/test_jobs.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_review_queue.py`, `tests/test_snapshot.py`, `tests/test_tombstones.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 3567 against a baseline of 3567
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_tree_the_export_does_not_hold_refuses_rather_than_reporting_everything`

Old text:

```
        "governed-tree-absent": ExitCode.LIBRARY_PREREQUISITE,
```

New text:

```
        "governed-tree-absent": ExitCode.PRECONDITION,
```

