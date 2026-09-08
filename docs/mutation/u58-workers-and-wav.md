# Mutation table: u58-workers-and-wav

Measured by `scripts/mutate.py` on 2026-09-08 03:09 UTC, branch `relay/76` at `356eb0f`. Pass kind: light.

Baseline: green, 6929 collected. pytest invocations for this batch: 30.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6929 against 6929. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `W1_voxlevel_zero` | `src/cratekit/analysis/vocals.py` | user | 1 file(s) | 64 | 3 | killed |
| `W2_decoder_seam_ignored` | `src/cratekit/analysis/vocals.py` | user | 1 file(s) | 64 | 4 | killed |
| `W3_undecodable_scored` | `src/cratekit/analysis/vocals.py` | user | 1 file(s) | 64 | 1 | killed |
| `W4_model_guard` | `src/cratekit/analysis/vocals.py` | user | 1 file(s) | 64 | 1 | killed |
| `W5_terminal_decoded` | `src/cratekit/analysis/vocals.py` | maintainer | 1 file(s) | 64 | 1 | killed |
| `W6_gender_constant` | `src/cratekit/analysis/vocals.py` | user | 1 file(s) | 6929 | 0 (promoted) | zero |
| `W7_undecodable_reason_reworded` | `src/cratekit/analysis/vocals.py` | user | 1 file(s) | 64 | 1 | killed |
| `R1_prefixed_reanalysed` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 64 | 1 | killed |
| `R2_extra_not_required` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 64 | 1 | killed |
| `R3_defaults_not_bound` | `src/cratekit/analysis/cli.py` | maintainer | 1 file(s) | 64 | 1 | killed |
| `R4_keyless_finalized` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 64 | 2 | killed |
| `R5_tag_write_unchecked` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 64 | 2 | killed |
| `R6_target_not_claimed` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 64 | 1 | killed |
| `R7_absent_energy_stamped` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 64 | 1 | killed |
| `R8_title_without_head` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 64 | 2 | killed |
| `R9_missing_file_analysed` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 64 | 1 | killed |
| `S1_previous_not_recorded` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 64 | 3 | killed |
| `S2_unchanged_rewritten` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 64 | 1 | killed |
| `S3_queue_without_calibration` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 64 | 2 | killed |
| `S4_undo_overwritten` | `src/cratekit/analysis/energy.py` | user | 1 file(s) | 64 | 1 | killed |
| `Q1_empty_folder_queued` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 64 | 2 | killed |
| `Q2_absolute_item_ids` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 64 | 11 | killed |
| `H1_run_unbound` | `src/cratekit/cli/handlers.py` | user | 8 file(s) | 322 | 18 | killed |
| `E1_beatless_cap` | `src/cratekit/analysis/energy.py` | user | 1 file(s) | 64 | 1 | killed |
| `E2_uncalibrated_measured` | `src/cratekit/analysis/detect.py` | user | 1 file(s) | 64 | 1 | killed |

## Zero rows and what they owe

- `W6_gender_constant` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

The line above is the driver's own text at measurement time. The row was a
test gap, not an inert mutation: the suite asserted the gender was one of
three letters rather than the letter the fake model calls. Two assertions now
pin the call, and the row was re-measured in its own one row pass,
`u58-zero-row-remeasured.md`, where it is killed by two tests. The second fix
round, 2026-09-08, changed the wav plumbing after this table was measured,
adding a boundary around the model's inference; that change is covered by a
test that fails on the tree before it and was not re-measured as a row, per
the brief's instruction not to run the table again.

## Considered and dropped

METHOD caps a light pass at 25 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `E3_level_clamp`: Drop the clamp of the level into 1 to 10 Dropped because: ranked below the cap: nine ascending cut points already bound the level, so the clamp is belt over braces and maintainer facing
- `R10_rename_before_tags`: Swap the finalize order so the rename lands before the tag write Dropped because: ranked below the cap: the crash window between the two writes is not driven by any test in this unit, so the row would measure only the twin collision case R6 already covers
- `C1_min_tracks_lowered`: Halve the minimum track count a calibration needs Dropped because: ranked below the cap: the two track fixture would still refuse at five, so the row cannot distinguish the coefficient from its neighbour without a new fixture

## Row definitions

### `W1_voxlevel_zero`

The original defect: score every track voxlevel 0 with a model loaded

- File: `src/cratekit/analysis/vocals.py`
- Surface: user
- Subset: test files importing cratekit.analysis.vocals
- Ran: `tests/test_analysis_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_partial_carrying_only_a_path_scores_nonzero_through_the_fixed_path`
  - `tests/test_analysis_workers.py::test_an_analyze_job_runs_pending_to_done_and_the_files_carry_the_result`
  - `tests/test_analysis_workers.py::test_run_batch_threads_the_decoder_through_to_the_vocal_pass`

Old text:

```
    result["voxlevel"] = int(round(score.presence))
```

New text:

```
    result["voxlevel"] = 0
```

### `W2_decoder_seam_ignored`

Ignore the bound decoder and always use the shipped one

- File: `src/cratekit/analysis/vocals.py`
- Surface: user
- Subset: test files importing cratekit.analysis.vocals
- Ran: `tests/test_analysis_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_partial_carrying_only_a_path_scores_nonzero_through_the_fixed_path`
  - `tests/test_analysis_workers.py::test_an_analyze_job_runs_pending_to_done_and_the_files_carry_the_result`
  - `tests/test_analysis_workers.py::test_run_batch_threads_the_decoder_through_to_the_vocal_pass`
  - `tests/test_analysis_workers.py::test_the_decoder_receives_the_partials_path`

Old text:

```
    decoder = _DECODER
    if decoder is None:
        from cratekit.analysis.vocal import decode

        decoder = decode
    return decoder(path)
```

New text:

```
    from cratekit.analysis.vocal import decode

    return decode(path)
```

### `W3_undecodable_scored`

Drop the guard that reports a failed decode instead of scoring it

- File: `src/cratekit/analysis/vocals.py`
- Surface: user
- Subset: test files importing cratekit.analysis.vocals
- Ran: `tests/test_analysis_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_decode_that_fails_is_reported_as_inactive_and_never_as_zero`

Old text:

```
    if samples is None:
        return _inactive(result, REASON_AUDIO_UNDECODABLE)

```

New text:

```
(empty)
```

### `W4_model_guard`

Drop the guard for a model that did not load

- File: `src/cratekit/analysis/vocals.py`
- Surface: user
- Subset: test files importing cratekit.analysis.vocals
- Ran: `tests/test_analysis_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_model_that_did_not_load_is_a_named_absence`

Old text:

```
    if model is None:
        return _inactive(result, REASON_MODEL_UNAVAILABLE)

```

New text:

```
(empty)
```

### `W5_terminal_decoded`

Decode a track whose head was terminal anyway

- File: `src/cratekit/analysis/vocals.py`
- Surface: maintainer
- Subset: test files importing cratekit.analysis.vocals
- Ran: `tests/test_analysis_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_terminal_head_is_not_decoded_at_all`

Old text:

```
    if result.get("terminal") is not None:
        return _inactive(result, REASON_HEAD_TERMINAL)

```

New text:

```
(empty)
```

### `W6_gender_constant`

Report every scored track's gender as U

- File: `src/cratekit/analysis/vocals.py`
- Surface: user
- Subset: test files importing cratekit.analysis.vocals
- Ran: `tests/test_analysis_workers.py`
- Collected: 6929 against a baseline of 6929
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    result["voxgender"] = score.gender
```

New text:

```
    result["voxgender"] = "U"
```

### `W7_undecodable_reason_reworded`

Reword the undecodable reason, do not append

- File: `src/cratekit/analysis/vocals.py`
- Surface: user
- Subset: test files importing cratekit.analysis.vocals
- Ran: `tests/test_analysis_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_decode_that_fails_is_reported_as_inactive_and_never_as_zero`

Old text:

```
REASON_AUDIO_UNDECODABLE = "vocal-audio-undecodable"
```

New text:

```
REASON_AUDIO_UNDECODABLE = "vocal-audio-unreadable"
```

### `R1_prefixed_reanalysed`

Drop the resume marker: analyse a file already carrying the head

- File: `src/cratekit/analysis/cli.py`
- Surface: user
- Subset: test files importing cratekit.analysis.cli
- Ran: `tests/test_analysis_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_prefixed_file_is_the_resume_marker_and_is_skipped_without_a_read`

Old text:

```
    if naming.has_head(path.name, template=template):
        return artifacts.produced(
            cfg, job, item, {"item": item.item_id, "path": str(path), "status": "skipped-prefixed"}
        )

```

New text:

```
(empty)
```

### `R2_extra_not_required`

Drop the missing extra refusal in the run worker

- File: `src/cratekit/analysis/cli.py`
- Surface: user
- Subset: test files importing cratekit.analysis.cli
- Ran: `tests/test_analysis_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_missing_extra_refuses_the_item_rather_than_skipping_it_as_keyless`

Old text:

```
    _require_heavy(_fake_detect_bound(), "analysing a track")

```

New text:

```
(empty)
```

### `R3_defaults_not_bound`

Never bind the shipped seams in a worker process

- File: `src/cratekit/analysis/cli.py`
- Surface: maintainer
- Subset: test files importing cratekit.analysis.cli
- Ran: `tests/test_analysis_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_corrupt_calibration_reaches_the_person_as_a_remedy_not_a_defect`

Old text:

```
    _require_heavy(_fake_detect_bound(), "analysing a track")
    _bind_defaults(cfg)
```

New text:

```
    _require_heavy(_fake_detect_bound(), "analysing a track")
```

### `R4_keyless_finalized`

Finalize a track whose head found no key

- File: `src/cratekit/analysis/cli.py`
- Surface: user
- Subset: test files importing cratekit.analysis.cli
- Ran: `tests/test_analysis_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_keyless_track_is_a_terminal_skip_with_nothing_written`
  - `tests/test_analysis_workers.py::test_an_undecodable_file_is_its_own_terminal_and_not_a_keyless_track`

Old text:

```
    if partial.get("terminal") is not None:
        return artifacts.produced(
            cfg, job, item, {"item": item.item_id, "path": str(path), "status": partial["terminal"]}
        )

```

New text:

```
(empty)
```

### `R5_tag_write_unchecked`

Ignore a failed tag write and rename anyway

- File: `src/cratekit/analysis/cli.py`
- Surface: user
- Subset: test files importing cratekit.analysis.cli
- Ran: `tests/test_analysis_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_container_the_tag_writer_does_not_know_fails_under_the_analysis_slug`
  - `tests/test_analysis_workers.py::test_a_failed_tag_write_fails_the_item_and_leaves_the_name_alone`

Old text:

```
    _write_or_refuse(path, fields, untouched="The file is untouched and was not renamed")
```

New text:

```
    tags.write_tags(path, fields)
```

### `R6_target_not_claimed`

Rename without claiming the target first

- File: `src/cratekit/analysis/cli.py`
- Surface: user
- Subset: test files importing cratekit.analysis.cli
- Ran: `tests/test_analysis_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_taken_target_name_fails_the_item_and_keeps_the_written_head_in_the_title`

Old text:

```
    if not naming.claim_target(target):
        raise refuse(
            "analysis-write-failed",
            f"{path.name} could not be renamed to {rendered.filename}: that name "
            f"is already taken in the folder. The tags were written and the "
            f"title carries the head, so the next pass converges",
            origin=_ORIGIN,
            detail={"path": str(path), "target": str(target), "stage": "rename"},
        )

```

New text:

```
(empty)
```

### `R7_absent_energy_stamped`

Write a level for an absent energy

- File: `src/cratekit/analysis/cli.py`
- Surface: user
- Subset: test files importing cratekit.analysis.cli
- Ran: `tests/test_analysis_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_an_uncalibrated_library_writes_no_energy_tag_and_routes_to_the_sink`

Old text:

```
        "energylevel": scored.get("energy"),
```

New text:

```
        "energylevel": scored.get("energy") or 5,
```

### `R8_title_without_head`

Write the bare stem as the title tag

- File: `src/cratekit/analysis/cli.py`
- Surface: user
- Subset: test files importing cratekit.analysis.cli
- Ran: `tests/test_analysis_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_taken_target_name_fails_the_item_and_keeps_the_written_head_in_the_title`
  - `tests/test_analysis_workers.py::test_an_analyze_job_runs_pending_to_done_and_the_files_carry_the_result`

Old text:

```
        "title": rendered.title_tag,
```

New text:

```
        "title": path.stem,
```

### `R9_missing_file_analysed`

Drop the source-missing refusal for a file that vanished

- File: `src/cratekit/analysis/cli.py`
- Surface: user
- Subset: test files importing cratekit.analysis.cli
- Ran: `tests/test_analysis_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_file_removed_between_queueing_and_drive_is_refused_by_name`

Old text:

```
        if twin is None:
            raise _refuse_missing(item, folder, path, "analyse")

```

New text:

```
(empty)
```

### `S1_previous_not_recorded`

Restamp without recording the previous value

- File: `src/cratekit/analysis/cli.py`
- Surface: user
- Subset: test files importing cratekit.analysis.cli
- Ran: `tests/test_analysis_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_file_whose_level_did_not_move_is_reported_unchanged_and_not_rewritten`
  - `tests/test_analysis_workers.py::test_a_restamp_job_runs_pending_to_done_and_records_the_previous_value`
  - `tests/test_analysis_workers.py::test_the_undo_log_keeps_the_first_previous_value_across_a_second_restamp`

Old text:

```
    energy.record_previous(cfg, path, tags.read_tag(path, "energylevel"))

```

New text:

```
(empty)
```

### `S2_unchanged_rewritten`

Rewrite a file whose level did not move

- File: `src/cratekit/analysis/cli.py`
- Surface: user
- Subset: test files importing cratekit.analysis.cli
- Ran: `tests/test_analysis_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_file_whose_level_did_not_move_is_reported_unchanged_and_not_rewritten`

Old text:

```
    if previous != level:
```

New text:

```
    if True:
```

### `S3_queue_without_calibration`

Queue a restamp over a library that has no calibration

- File: `src/cratekit/analysis/cli.py`
- Surface: user
- Subset: test files importing cratekit.analysis.cli
- Ran: `tests/test_analysis_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_corrupt_calibration_reaches_the_person_as_a_remedy_not_a_defect`
  - `tests/test_analysis_workers.py::test_a_restamp_with_no_calibration_refuses_at_the_queue`

Old text:

```
    # REFUSED AT THE QUEUE, not only in the worker: a job whose every item
    # would fail on the same absence is a report over work nothing could do.
    _calibration_or_refuse(cfg)

```

New text:

```
(empty)
```

### `S4_undo_overwritten`

Let a second restamp overwrite the first previous value

- File: `src/cratekit/analysis/energy.py`
- Surface: user
- Subset: test files importing cratekit.analysis.energy
- Ran: `tests/test_analysis_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_undo_log_keeps_the_first_previous_value_across_a_second_restamp`

Old text:

```
        if key in log:
            return False

```

New text:

```
(empty)
```

### `Q1_empty_folder_queued`

Queue an analysis over a folder holding no audio

- File: `src/cratekit/analysis/cli.py`
- Surface: user
- Subset: test files importing cratekit.analysis.cli
- Ran: `tests/test_analysis_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_folder_that_is_not_there_is_a_different_zero_from_an_empty_one`
  - `tests/test_analysis_workers.py::test_a_folder_with_no_audio_queues_nothing_and_says_so`

Old text:

```
    if not items:
        return _nothing_to_queue(ctx, folder)
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={"folder": str(folder)},
            cfg=cfg,
            item_ids=items,
        )
        return ctx.envelope(data=_reported(store, job))
```

New text:

```
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={"folder": str(folder)},
            cfg=cfg,
            item_ids=items,
        )
        return ctx.envelope(data=_reported(store, job))
```

### `Q2_absolute_item_ids`

Queue absolute paths as item identifiers again

- File: `src/cratekit/analysis/cli.py`
- Surface: user
- Subset: test files importing cratekit.analysis.cli
- Ran: `tests/test_analysis_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 11 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_container_the_tag_writer_does_not_know_fails_under_the_analysis_slug`
  - `tests/test_analysis_workers.py::test_a_corrupt_calibration_reaches_the_person_as_a_remedy_not_a_defect`
  - `tests/test_analysis_workers.py::test_a_failed_tag_write_fails_the_item_and_leaves_the_name_alone`
  - `tests/test_analysis_workers.py::test_a_file_removed_between_queueing_and_drive_is_refused_by_name`
  - `tests/test_analysis_workers.py::test_a_prefixed_file_is_the_resume_marker_and_is_skipped_without_a_read`
  - `tests/test_analysis_workers.py::test_a_restamp_job_runs_pending_to_done_and_records_the_previous_value`
  - `tests/test_analysis_workers.py::test_a_restamp_worker_without_the_extra_refuses_rather_than_skipping`
  - `tests/test_analysis_workers.py::test_a_taken_target_name_fails_the_item_and_keeps_the_written_head_in_the_title`
  - `tests/test_analysis_workers.py::test_an_analyze_job_runs_pending_to_done_and_the_files_carry_the_result`
  - `tests/test_analysis_workers.py::test_an_item_renamed_before_its_row_moved_resumes_as_finished`
  - `tests/test_analysis_workers.py::test_the_missing_extra_refuses_the_item_rather_than_skipping_it_as_keyless`

Old text:

```
    return sorted(
        path.name
        for path in folder.iterdir()
```

New text:

```
    return sorted(
        str(path)
        for path in folder.iterdir()
```

### `H1_run_unbound`

Drop the analyze.run binding from the handler table

- File: `src/cratekit/cli/handlers.py`
- Surface: user
- Subset: test files importing cratekit.cli.handlers
- Ran: `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_label_workers.py`, `tests/test_master_cli.py`, `tests/test_outbound_workers.py`, `tests/test_tag_workers.py`
- Collected: 322 against a baseline of 322
- Kills: 18 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_calibrated_level_is_written_and_routes_to_a_band`
  - `tests/test_analysis_workers.py::test_a_container_the_tag_writer_does_not_know_fails_under_the_analysis_slug`
  - `tests/test_analysis_workers.py::test_a_corrupt_calibration_reaches_the_person_as_a_remedy_not_a_defect`
  - `tests/test_analysis_workers.py::test_a_detector_shaped_like_the_batch_fakes_is_accepted`
  - `tests/test_analysis_workers.py::test_a_failed_tag_write_fails_the_item_and_leaves_the_name_alone`
  - `tests/test_analysis_workers.py::test_a_file_removed_between_queueing_and_drive_is_refused_by_name`
  - `tests/test_analysis_workers.py::test_a_keyless_track_is_a_terminal_skip_with_nothing_written`
  - `tests/test_analysis_workers.py::test_a_prefixed_file_is_the_resume_marker_and_is_skipped_without_a_read`
  - `tests/test_analysis_workers.py::test_a_taken_target_name_fails_the_item_and_keeps_the_written_head_in_the_title`
  - `tests/test_analysis_workers.py::test_an_analyze_job_runs_pending_to_done_and_the_files_carry_the_result`
  - `tests/test_analysis_workers.py::test_an_item_renamed_before_its_row_moved_resumes_as_finished`
  - `tests/test_analysis_workers.py::test_an_uncalibrated_library_writes_no_energy_tag_and_routes_to_the_sink`
  - `tests/test_analysis_workers.py::test_an_undecodable_file_is_its_own_terminal_and_not_a_keyless_track`
  - `tests/test_analysis_workers.py::test_the_analysis_keys_resolve_to_workers[analyze.run]`
  - `tests/test_analysis_workers.py::test_the_frozen_folder_is_absolute_so_a_resume_from_elsewhere_finds_it`
  - ... and 3 more, see the JSON sidecar

Old text:

```
    "analyze.run": "cratekit.analysis.cli:handle_run",

```

New text:

```
(empty)
```

### `E1_beatless_cap`

Drop the beatless cap in the energy scorer

- File: `src/cratekit/analysis/energy.py`
- Surface: user
- Subset: test files importing cratekit.analysis.energy
- Ran: `tests/test_analysis_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_beatless_guard_caps_a_loud_track_with_no_onsets`

Old text:

```
    if calibration.onset_floor is not None:
        density = float(features.get("onset_density", math.inf))
        if not math.isnan(density) and density < calibration.onset_floor:
            level = min(level, BEATLESS_CAP)

```

New text:

```
(empty)
```

### `E2_uncalibrated_measured`

Measure energy with no calibration instead of reporting uncalibrated

- File: `src/cratekit/analysis/detect.py`
- Surface: user
- Subset: test files importing cratekit.analysis.detect
- Ran: `tests/test_analysis_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_detector_names_why_energy_is_what_it_is`

Old text:

```
    if calibration is None:
        return None, energy.STATUS_UNCALIBRATED

```

New text:

```
(empty)
```

