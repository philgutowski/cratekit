# Mutation table: u44-author

Measured by `scripts/mutate.py` on 2026-08-27 15:20 UTC, branch `relay/62` at `d679ccd`. Pass kind: light.

Baseline: green, 6380 collected. pytest invocations for this batch: 27.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6380 against 6380. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `A1_archive_verify_dropped` | `src/cratekit/modules/tools/mastering.py` | user | 2 file(s) | 6380 | 0 (promoted) | zero |
| `A2_archive_collision_skips` | `src/cratekit/modules/tools/mastering.py` | user | 2 file(s) | 148 | 2 | killed |
| `A3_archive_after_the_first_pass` | `src/cratekit/modules/tools/mastering.py` | user | 2 file(s) | 148 | 1 | killed |
| `A4_digest_reads_first_chunk_only` | `src/cratekit/modules/tools/mastering.py` | user | 2 file(s) | 6380 | 0 (promoted) | zero |
| `B1_output_unread` | `src/cratekit/modules/tools/mastering.py` | user | 2 file(s) | 148 | 2 | killed |
| `B2_output_existence_only` | `src/cratekit/modules/tools/mastering.py` | user | 2 file(s) | 148 | 1 | killed |
| `B3_concat_output_unread` | `src/cratekit/modules/tools/mastering.py` | user | 2 file(s) | 6380 | 0 (promoted) | zero |
| `C1_empty_output_dir_not_normalized` | `src/cratekit/master/cli.py` | user | 1 file(s) | 23 | 1 | killed |
| `C2_argv_drops_overwrite` | `src/cratekit/master/cli.py` | user | 1 file(s) | 23 | 1 | killed |
| `C3_argv_drops_output_dir` | `src/cratekit/master/cli.py` | user | 1 file(s) | 23 | 1 | killed |
| `C4_refusal_not_translated` | `src/cratekit/master/cli.py` | user | 1 file(s) | 23 | 8 | killed |
| `C5_empty_recording_accepted` | `src/cratekit/master/cli.py` | user | 1 file(s) | 23 | 1 | killed |
| `C6_overwrite_always_true` | `src/cratekit/master/cli.py` | user | 1 file(s) | 23 | 1 | killed |
| `C7_output_dir_ignored_at_the_work` | `src/cratekit/master/cli.py` | user | 1 file(s) | 23 | 1 | killed |
| `D1_registry_drops_long_running` | `src/cratekit/cli/registry.py` | maintainer | 22 file(s) | 2933 | collection error | collect-error |
| `D2_reason_slug_removed` | `src/cratekit/core/cause.py` | user | 32 file(s) | 3767 | 2 | killed |
| `Z0_null_control` | `src/cratekit/master/cli.py` | maintainer | 1 file(s) | 6380 | 0 (promoted) | zero |

## Zero rows and what they owe

- `A1_archive_verify_dropped` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `A4_digest_reads_first_chunk_only` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `B3_concat_output_unread` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `Z0_null_control` (maintainer facing): maintainer facing, composite not required

## Considered and dropped

METHOD caps a light pass at 25 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `E1_settings_validation`: Halve the drift-window bound coefficient in Settings.__post_init__ Dropped because: ranked below the cap: the shell exposes no settings flag, so no input this unit adds can reach the validator. It is U35's guard over U35's surface.
- `E2_parse_loudness_last_block`: Take the FIRST JSON block rather than the last in parse_loudness Dropped because: ranked below the cap: same reason as E1. The shell passes stderr through untouched and adds no caller that can vary which block arrives.
- `E3_encoder_args_dither`: Drop the triangular dither from the sixteen-bit branch of encoder_args Dropped because: ranked below the cap: an audio-quality guard with no assertion this unit adds, and the shell cannot select the branch. Measured by U35 or not at all.
- `E4_sample_argument_entry`: Point the master entry in _sample_arguments at a path outside the configured library Dropped because: ranked below the cap: it would measure the R1 convention rather than this unit's code, and the same guard already covers twenty other verbs.

## Row definitions

### `A1_archive_verify_dropped`

Drop the post-copy digest verification, so a corrupt archive is reported safe

- File: `src/cratekit/modules/tools/mastering.py`
- Surface: user
- Subset: test files importing cratekit.modules.tools.mastering
- Ran: `tests/modules/test_tools.py`, `tests/test_master_cli.py`
- Collected: 6380 against a baseline of 6380
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    shutil.copy2(source, destination)
    if digest(destination) != source_digest:
```

New text:

```
    shutil.copy2(source, destination)
    if False:
```

### `A2_archive_collision_skips`

Restore the source system's behaviour: an existing archive entry is skipped rather than verified

- File: `src/cratekit/modules/tools/mastering.py`
- Surface: user
- Subset: test files importing cratekit.modules.tools.mastering
- Ran: `tests/modules/test_tools.py`, `tests/test_master_cli.py`
- Collected: 148 against a baseline of 148
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_an_archive_entry_with_the_same_name_and_different_content_refuses`
  - `tests/test_master_cli.py::test_an_archive_holding_different_audio_refuses_and_keeps_both`

Old text:

```
    if destination.exists():
        if digest(destination) == source_digest:
            return destination
```

New text:

```
    if destination.exists():
        return destination
```

### `A3_archive_after_the_first_pass`

Move the archive AFTER the probe, so a crash between them leaves no verified copy

- File: `src/cratekit/modules/tools/mastering.py`
- Surface: user
- Subset: test files importing cratekit.modules.tools.mastering
- Ran: `tests/modules/test_tools.py`, `tests/test_master_cli.py`
- Collected: 148 against a baseline of 148
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_archive_is_taken_before_any_encoding_stage`

Old text:

```
    archived_to = None
    if archive:
        archived_to = archive_source(
            source, archive_dir or (source.parent / ARCHIVE_DIRNAME)
        )

    probe = probe_source(source, runner=runner, ffprobe=ffprobe)
```

New text:

```
    probe = probe_source(source, runner=runner, ffprobe=ffprobe)

    archived_to = None
    if archive:
        archived_to = archive_source(
            source, archive_dir or (source.parent / ARCHIVE_DIRNAME)
        )
```

### `A4_digest_reads_first_chunk_only`

Digest only the first chunk, so two sets differing later in the file hash identically

- File: `src/cratekit/modules/tools/mastering.py`
- Surface: user
- Subset: test files importing cratekit.modules.tools.mastering
- Ran: `tests/modules/test_tools.py`, `tests/test_master_cli.py`
- Collected: 6380 against a baseline of 6380
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        while True:
            block = handle.read(chunk)
            if not block:
                break
            hasher.update(block)
```

New text:

```
        hasher.update(handle.read(chunk))
```

### `B1_output_unread`

Drop the post-encode output check, restoring the success report over a file that is not there

- File: `src/cratekit/modules/tools/mastering.py`
- Surface: user
- Subset: test files importing cratekit.modules.tools.mastering
- Ran: `tests/modules/test_tools.py`, `tests/test_master_cli.py`
- Collected: 148 against a baseline of 148
- Kills: 2 (killed)
- Killed:
  - `tests/test_master_cli.py::test_an_encode_that_exits_zero_and_writes_nothing_does_not_report_success`
  - `tests/test_master_cli.py::test_an_encode_that_writes_an_empty_file_does_not_report_success`

Old text:

```
    _wrote_or_refuse(target, "normalize-and-encode")
    return Report(
```

New text:

```
    return Report(
```

### `B2_output_existence_only`

Check existence but not size, so a zero-byte encode still reports a saving of 1.0

- File: `src/cratekit/modules/tools/mastering.py`
- Surface: user
- Subset: test files importing cratekit.modules.tools.mastering
- Ran: `tests/modules/test_tools.py`, `tests/test_master_cli.py`
- Collected: 148 against a baseline of 148
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_an_encode_that_writes_an_empty_file_does_not_report_success`

Old text:

```
    if not target.exists() or target.stat().st_size == 0:
```

New text:

```
    if not target.exists():
```

### `B3_concat_output_unread`

Drop the same check from the join, one function over

- File: `src/cratekit/modules/tools/mastering.py`
- Surface: user
- Subset: test files importing cratekit.modules.tools.mastering
- Ran: `tests/modules/test_tools.py`, `tests/test_master_cli.py`
- Collected: 6380 against a baseline of 6380
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    _wrote_or_refuse(destination, "join")
    return destination
```

New text:

```
    return destination
```

### `C1_empty_output_dir_not_normalized`

Stop normalizing an empty --output-dir, so the queueing path and the resume disagree on the destination

- File: `src/cratekit/master/cli.py`
- Surface: user
- Subset: test files importing cratekit.master.cli
- Ran: `tests/test_master_cli.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_an_empty_output_dir_and_an_omitted_one_freeze_identically`

Old text:

```
        OUTPUT_DIR: output_dir or None,
```

New text:

```
        OUTPUT_DIR: output_dir,
```

### `C2_argv_drops_overwrite`

Drop --overwrite from the resume argv, so a respawned child meets the refusal the first run was told to ignore

- File: `src/cratekit/master/cli.py`
- Surface: user
- Subset: test files importing cratekit.master.cli
- Ran: `tests/test_master_cli.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_the_resume_argv_rebuilds_every_frozen_flag`

Old text:

```
    if payload.get(OVERWRITE):
        argv.append("--overwrite")
```

New text:

```
(empty)
```

### `C3_argv_drops_output_dir`

Drop --output-dir from the resume argv, so the child writes the master somewhere the person did not ask for

- File: `src/cratekit/master/cli.py`
- Surface: user
- Subset: test files importing cratekit.master.cli
- Ran: `tests/test_master_cli.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_the_resume_argv_rebuilds_every_frozen_flag`

Old text:

```
    if output_dir:
        argv += ["--output-dir", str(output_dir)]
```

New text:

```
(empty)
```

### `C4_refusal_not_translated`

Let MasteringRefused escape, so every engine refusal reaches the person as internal-error

- File: `src/cratekit/master/cli.py`
- Surface: user
- Subset: test files importing cratekit.master.cli
- Ran: `tests/test_master_cli.py`
- Collected: 23 against a baseline of 23
- Kills: 8 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_container_the_engine_does_not_read_refuses_under_its_own_slug`
  - `tests/test_master_cli.py::test_a_failed_encode_under_overwrite_says_what_the_person_is_left_holding`
  - `tests/test_master_cli.py::test_a_failing_encode_does_not_report_success`
  - `tests/test_master_cli.py::test_a_recording_that_is_not_there_refuses_rather_than_raising`
  - `tests/test_master_cli.py::test_an_archive_holding_different_audio_refuses_and_keeps_both`
  - `tests/test_master_cli.py::test_an_encode_that_exits_zero_and_writes_nothing_does_not_report_success`
  - `tests/test_master_cli.py::test_an_encode_that_writes_an_empty_file_does_not_report_success`
  - `tests/test_master_cli.py::test_an_existing_master_refuses_without_overwrite_and_proceeds_with_it`

Old text:

```
    except mastering.MasteringRefused as exc:
        raise refuse(
            str(exc.refusal),
            exc.detail,
            origin=("master", "cli"),
            detail={"path": str(exc.path) if exc.path is not None else None},
        ) from exc
```

New text:

```
    except ZeroDivisionError as exc:
        raise refuse(
            str(exc),
            "unreachable",
            origin=("master", "cli"),
        ) from exc
```

### `C5_empty_recording_accepted`

Accept an empty positional, so the verb queues a job over no recording at all

- File: `src/cratekit/master/cli.py`
- Surface: user
- Subset: test files importing cratekit.master.cli
- Ran: `tests/test_master_cli.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_an_empty_recording_refuses_from_the_vocabulary`

Old text:

```
    if not recording:
```

New text:

```
    if False:
```

### `C6_overwrite_always_true`

Freeze overwrite as always true, so every run replaces an existing master without being asked to

- File: `src/cratekit/master/cli.py`
- Surface: user
- Subset: test files importing cratekit.master.cli
- Ran: `tests/test_master_cli.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_an_existing_master_refuses_without_overwrite_and_proceeds_with_it`

Old text:

```
        OVERWRITE: bool(overwrite),
```

New text:

```
        OVERWRITE: True,
```

### `C7_output_dir_ignored_at_the_work`

Ignore the frozen output directory, so the master lands beside the source whatever was asked for

- File: `src/cratekit/master/cli.py`
- Surface: user
- Subset: test files importing cratekit.master.cli
- Ran: `tests/test_master_cli.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_the_output_directory_is_honoured_and_never_the_source`

Old text:

```
            output_dir=Path(output_dir) if output_dir else None,
```

New text:

```
            output_dir=None,
```

### `D1_registry_drops_long_running`

Remove long_running from the master entry, which should shrink two derived populations

- File: `src/cratekit/cli/registry.py`
- Surface: maintainer
- Subset: test files importing cratekit.cli.registry
- Ran: `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_jobs.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_packaging.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_write_session.py`
- Collected: 2933 against a baseline of 2934
- Kills: 2 (collect-error)
- Note: collection changed: 2933 collected against a baseline of 2934. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_cli_contract.py::test_a_verb_carrying_a_resume_argv_builder_declares_that_it_queues`
  - `tests/test_master_cli.py::test_the_entry_is_landed_and_declares_no_gate`

Old text:

```
        argv_builder="master_argv",
        long_running=True,
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        writes=frozenset({"files"}),
        destructive=True,
        doctor_checks=("binary.ffmpeg",),
```

New text:

```
        argv_builder="master_argv",
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        writes=frozenset({"files"}),
        destructive=True,
        doctor_checks=("binary.ffmpeg",),
```

### `D2_reason_slug_removed`

Remove source-missing from the closed reason registry, so the shell's own refusal cannot be built

- File: `src/cratekit/core/cause.py`
- Surface: user
- Subset: test files importing cratekit.core.cause
- Ran: `tests/intake/test_collection_xml.py`, `tests/intake/test_pipeline.py`, `tests/modules/test_labels.py`, `tests/modules/test_outbound.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_cli_contract.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_incremental_sync.py`, `tests/test_jobs.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_review_queue.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_install.py`, `tests/test_snapshot.py`, `tests/test_tombstones.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 3767 against a baseline of 3767
- Kills: 2 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_recording_that_is_not_there_refuses_rather_than_raising`
  - `tests/test_master_cli.py::test_an_empty_recording_refuses_from_the_vocabulary`

Old text:

```
        "source-missing": ExitCode.PRECONDITION,
```

New text:

```
(empty)
```

### `Z0_null_control`

The null control: rename a local with no behavioural effect. Must kill zero, or the driver is contaminated

- File: `src/cratekit/master/cli.py`
- Surface: maintainer
- Subset: test files importing cratekit.master.cli
- Ran: `tests/test_master_cli.py`
- Collected: 6380 against a baseline of 6380
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    payload = job.payload or {}
    argv = ["master", str(payload.get(SOURCE) or "")]
```

New text:

```
    frozen = job.payload or {}
    payload = frozen
    argv = ["master", str(payload.get(SOURCE) or "")]
```

