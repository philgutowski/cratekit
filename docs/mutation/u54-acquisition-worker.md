# Mutation table: u54-acquisition-worker

Measured by `scripts/mutate.py` on 2026-09-09 11:35 UTC, branch `u54/finish` at `fe2624f`. Pass kind: light.

Baseline: green, 6991 collected. pytest invocations for this batch: 27.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6991 against 6991. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `G1_origin_refusal` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 64 | 1 | killed |
| `G2_missing_identifier` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 64 | 1 | killed |
| `G4_zero_item_noop` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 64 | 1 | killed |
| `G6_resume_drives_open_job` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 64 | 24 | killed |
| `G7_staging_cleared` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 6991 | 0 (promoted) | zero |
| `G8_park_on_block` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 64 | 1 | killed |
| `G9_failed_invocation` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 64 | 5 | killed |
| `G10_absent_result` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 64 | 1 | killed |
| `G11_not_acquired` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 64 | 2 | killed |
| `G12_landing_check` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 64 | 3 | killed |
| `G14_marker_applied` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 64 | 3 | killed |
| `G15_no_marker_text` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 64 | 1 | killed |
| `G17_paced_sleep_bound` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 64 | 2 | killed |
| `G19_frozen_config` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 64 | 3 | killed |
| `G20_output_exists` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 64 | 1 | killed |
| `G21_park_releases_item` | `src/cratekit/core/jobs.py` | user | 19 file(s) | 900 | 5 | killed |
| `G22_park_before_item_boundary` | `src/cratekit/core/jobs.py` | user | 19 file(s) | 900 | 8 | killed |
| `G27_remedy_absent_stays_absent` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 64 | 1 | killed |
| `G28_marker_decided_by_the_file` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 64 | 1 | killed |
| `G29_auth_failure_parks` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 64 | 3 | killed |
| `G30_zero_item_resume` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 64 | 1 | killed |
| `G31_reader_sees_the_path_as_typed` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 64 | 1 | killed |

## Zero rows and what they owe

- `G7_staging_cleared` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Considered and dropped

METHOD caps a light pass at 25 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `G16_invocation_retryable`: Flatten retryable on an invocation refusal to False for every outcome Dropped because: ranked below the cap: the retryable flag rides the same two refusal builders G9 and G11 already measure, and the item's slug rather than its flag is what the person is shown
- `G24_track_retryable`: Flatten transient on a per-track refusal so every outcome reads permanent Dropped because: ranked below the cap for G16's reason, the same builder measured from a different field
- `G25_remedy_fallback`: Drop the fallback in _remedy so a result carrying no remedy token raises instead Dropped because: ranked below the cap: maintainer facing, and every fixture in the suite carries a remedy token, so the fallback's reachability is unmeasured
- `G26_marked_stem_form`: Append the marker after the suffix rather than into the stem Dropped because: ranked below the cap: G14 already measures whether the marker reaches the name at all, and the naming engine's stem reading is U40's guard rather than this unit's
- `G3_repeat_folds_first_wins`: Last occurrence of a repeated identifier wins instead of the first Dropped because: dropped at the fix round to make room for the round's own guards: a repeat asks for the same file either way, so what moves is which row's artist and title are frozen, not what lands
- `G5_list_frozen_absolute`: Freeze the list path as given rather than absolute Dropped because: dropped at the fix round: the fix split that line, and G31 measures the half a defect was actually found in
- `G13_unreadable_is_transient`: Report a file nothing could read as a policy refusal rather than a transient failure Dropped because: dropped at the fix round: G12 removes the landing check whole, so the branch is measured; this row measured only which slug it carries
- `G18_per_item_staging`: Point the adapter at the shared staging root rather than this item's own directory Dropped because: dropped at the fix round: G7 measures the staging tree's clearing, which is the half a partial download travels through
- `G23_handler_bound`: Unbind the download handler key Dropped because: dropped at the fix round: a named test resolves the key to this worker directly, so the row's only news would be that test disappearing

## Row definitions

### `G1_origin_refusal`

Queue a list from any provider, dropping the refusal that only the provider's own list carries acquirable identifiers

- File: `src/cratekit/acquire/cli.py`
- Surface: user
- Subset: test files importing cratekit.acquire.cli
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_pasted_tracklist_is_refused_at_the_queue_rather_than_queued_unacquirable`

Old text:

```
    if origin != match.TIDAL:
        raise _unusable(
            f"this is a {origin} list, and acquiring needs the provider's own track "
            f"identifiers, which only a list fetched from the provider carries",
            "fetch the playlist from the provider into a list document first, "
            "then acquire that",
            "a pasted tracklist is matched against the library with match.run; "
            "its missing rows carry acquisition options, not identifiers",
            origin=origin,
        )

```

New text:

```
(empty)
```

### `G2_missing_identifier`

Queue a provider list whose rows carry no identifier, dropping the by-position refusal

- File: `src/cratekit/acquire/cli.py`
- Surface: user
- Subset: test files importing cratekit.acquire.cli
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_provider_row_without_an_identifier_is_refused_by_position`

Old text:

```
    if missing:
        raise _unusable(
            f"{len(missing)} track(s) in this list carry no provider identifier "
            f"(positions {', '.join(str(p) for p in missing[:5])}"
            f"{', ...' if len(missing) > 5 else ''}), so nothing can ask the "
            f"provider for them",
            "fetch the list from the provider again so every row carries its id",
            positions=missing,
        )

```

New text:

```
(empty)
```

### `G4_zero_item_noop`

Enqueue a job for a list that read to no tracks, the zero item rule's own shape

- File: `src/cratekit/acquire/cli.py`
- Surface: user
- Subset: test files importing cratekit.acquire.cli
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_list_with_no_tracks_queues_nothing_and_says_so`

Old text:

```
        if not tracks:
            return ctx.envelope(data=_no_op("no-tracks"), outcome=Outcome.NO_OP)

```

New text:

```
(empty)
```

### `G6_resume_drives_open_job`

Report the reconciled job without driving it, so a resume does no work

- File: `src/cratekit/acquire/cli.py`
- Surface: user
- Subset: test files importing cratekit.acquire.cli
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 24 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_broken_adapter_fails_the_item_and_does_not_park_the_run`
  - `tests/test_acquire_workers.py::test_a_configuration_naming_an_unknown_adapter_fails_the_item_by_name`
  - `tests/test_acquire_workers.py::test_a_dead_session_logs_in_once_and_not_once_per_track`
  - `tests/test_acquire_workers.py::test_a_download_job_runs_pending_to_done_through_the_resume_path`
  - `tests/test_acquire_workers.py::test_a_lossless_landing_under_the_permissive_policy_is_not_marked`
  - `tests/test_acquire_workers.py::test_a_lossy_landing_under_strict_policy_is_refused_at_the_item_with_the_codec_named`
  - `tests/test_acquire_workers.py::test_a_lossy_landing_under_the_permissive_policy_is_committed_marked`
  - `tests/test_acquire_workers.py::test_a_lossy_offer_under_strict_policy_is_refused_before_anything_is_fetched`
  - `tests/test_acquire_workers.py::test_a_lying_offer_under_the_permissive_policy_is_still_committed_marked`
  - `tests/test_acquire_workers.py::test_a_mid_batch_refusal_fails_that_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/test_acquire_workers.py::test_a_partial_file_left_in_staging_does_not_poison_the_next_attempt`
  - `tests/test_acquire_workers.py::test_a_provider_block_parks_the_job_and_makes_no_further_request`
  - `tests/test_acquire_workers.py::test_a_rate_limit_is_retried_under_backoff_and_then_lands`
  - `tests/test_acquire_workers.py::test_a_rate_limit_that_never_clears_fails_the_item_as_transient`
  - `tests/test_acquire_workers.py::test_a_track_the_provider_does_not_have_is_permanent_and_carries_no_remedy`
  - ... and 9 more, see the JSON sidecar

Old text:

```
                _, warnings = ctx.run_job(store, job)
                job = jobs.get(store, job.job_id)

```

New text:

```
(empty)
```

### `G7_staging_cleared`

Keep whatever a killed attempt left in the item's staging directory

- File: `src/cratekit/acquire/cli.py`
- Surface: user
- Subset: test files importing cratekit.acquire.cli
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 6991 against a baseline of 6991
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if directory.exists():
        shutil.rmtree(directory)

```

New text:

```
(empty)
```

### `G8_park_on_block`

Read a parked run as an ordinary result, so the driver claims the next item into a provider block

- File: `src/cratekit/acquire/cli.py`
- Surface: user
- Subset: test files importing cratekit.acquire.cli
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_provider_block_parks_the_job_and_makes_no_further_request`

Old text:

```
    if run.parked is not None:
        raise jobs.Parked(run.parked)

```

New text:

```
(empty)
```

### `G9_failed_invocation`

Ignore an invocation the adapter could not run at all

- File: `src/cratekit/acquire/cli.py`
- Surface: user
- Subset: test files importing cratekit.acquire.cli
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 5 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_broken_adapter_fails_the_item_and_does_not_park_the_run`
  - `tests/test_acquire_workers.py::test_a_dead_session_logs_in_once_and_not_once_per_track`
  - `tests/test_acquire_workers.py::test_a_mid_batch_refusal_fails_that_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/test_acquire_workers.py::test_an_authentication_failure_parks_the_run_and_names_the_replacement_path`
  - `tests/test_acquire_workers.py::test_the_shipped_adapter_is_constructed_through_build_and_refuses_with_a_named_remedy`

Old text:

```
    if invocation.outcome in FAILED_INVOCATIONS:
```

New text:

```
    if False:
```

### `G10_absent_result`

Drop the refusal for a run that reported OK with no result for this key

- File: `src/cratekit/acquire/cli.py`
- Surface: user
- Subset: test files importing cratekit.acquire.cli
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_run_reporting_nothing_for_the_key_is_refused_rather_than_read_as_success`

Old text:

```
    if result is None:
        raise refuse(
            "unavailable-transient",
            f"{invocation.adapter} finished without reporting on {request.key}, "
            f"so nothing is known about it and it stays queued",
            remedy=Remedy.RETRY_LATER,
            scope=Scope.ITEM,
            retryable=True,
            origin=("acquire.cli",),
            detail={"adapter": invocation.adapter, "key": request.key},
        )

```

New text:

```
(empty)
```

### `G11_not_acquired`

Commit a per-track result that is not an acquisition

- File: `src/cratekit/acquire/cli.py`
- Surface: user
- Subset: test files importing cratekit.acquire.cli
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_lossy_offer_under_strict_policy_is_refused_before_anything_is_fetched`
  - `tests/test_acquire_workers.py::test_a_track_the_provider_does_not_have_is_permanent_and_carries_no_remedy`

Old text:

```
    if result.outcome is not TrackOutcome.ACQUIRED:
        raise _refused_track(result, invocation.adapter)

```

New text:

```
(empty)
```

### `G12_landing_check`

Take the adapter's word for the landed file, skipping the policy check at the file

- File: `src/cratekit/acquire/cli.py`
- Surface: user
- Subset: test files importing cratekit.acquire.cli
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 3 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_lossy_landing_under_strict_policy_is_refused_at_the_item_with_the_codec_named`
  - `tests/test_acquire_workers.py::test_an_unreadable_landing_is_transient_and_not_a_policy_refusal`
  - `tests/test_acquire_workers.py::test_the_frozen_policy_reaches_the_worker_not_the_live_one`

Old text:

```
    landed = checked_landing(Path(str(result.path)), request.key, policy=per_item.lossless_policy)
```

New text:

```
    landed = Path(str(result.path))
```

### `G14_marker_applied`

Commit a lossy landing under its unmarked name whatever the policy required

- File: `src/cratekit/acquire/cli.py`
- Surface: user
- Subset: test files importing cratekit.acquire.cli
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 3 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_lossy_landing_under_the_permissive_policy_is_committed_marked`
  - `tests/test_acquire_workers.py::test_a_lossy_landing_with_no_marker_text_is_refused_rather_than_committed_unmarked`
  - `tests/test_acquire_workers.py::test_a_lying_offer_under_the_permissive_policy_is_still_committed_marked`

Old text:

```
    if not required:
        return landed.name

```

New text:

```
    return landed.name

```

### `G15_no_marker_text`

Commit a lossy landing unmarked when the configuration names no marker text

- File: `src/cratekit/acquire/cli.py`
- Surface: user
- Subset: test files importing cratekit.acquire.cli
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_lossy_landing_with_no_marker_text_is_refused_rather_than_committed_unmarked`

Old text:

```
    if not text:
        raise refuse(
            "lossy-refused",
            f"{landed.name} landed lossy under a policy that permits lossy only "
            f"when marked, and the configuration names no marker text, so it "
            f"cannot be marked and is not kept",
            remedy=Remedy.RELAX_LOSSLESS_POLICY,
            scope=Scope.ITEM,
            origin=("acquire.cli",),
            detail={"path": str(landed)},
        )

```

New text:

```
(empty)
```

### `G17_paced_sleep_bound`

Let the pool bind its own definition time sleep instead of the one the frozen configuration paces

- File: `src/cratekit/acquire/cli.py`
- Surface: user
- Subset: test files importing cratekit.acquire.cli
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_rate_limit_that_never_clears_fails_the_item_as_transient`
  - `tests/test_acquire_workers.py::test_the_pacing_delay_comes_from_the_frozen_configuration_not_a_fresh_load`

Old text:

```
    run = download.acquire_paced(adapter, (request,), sleep=_SLEEP)
```

New text:

```
    run = download.acquire_paced(adapter, (request,))
```

### `G19_frozen_config`

Build the adapter settings from a fresh load rather than the configuration the job was frozen against

- File: `src/cratekit/acquire/cli.py`
- Surface: user
- Subset: test files importing cratekit.acquire.cli
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 3 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_delay_frozen_at_zero_waits_nothing_whatever_the_live_configuration_says`
  - `tests/test_acquire_workers.py::test_the_frozen_policy_reaches_the_worker_not_the_live_one`
  - `tests/test_acquire_workers.py::test_the_pacing_delay_comes_from_the_frozen_configuration_not_a_fresh_load`

Old text:

```
    settings = AdapterSettings.from_config(cfg)
```

New text:

```
    settings = AdapterSettings.from_config(_load())
```

### `G20_output_exists`

Replace a file already at the destination instead of refusing

- File: `src/cratekit/acquire/cli.py`
- Surface: user
- Subset: test files importing cratekit.acquire.cli
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_an_existing_file_at_the_destination_refuses_rather_than_replacing_it`

Old text:

```
    if final.exists():
```

New text:

```
    if False:
```

### `G21_park_releases_item`

Park the job with the claimed item still claimed, so the resume cannot redo it

- File: `src/cratekit/core/jobs.py`
- Surface: user
- Subset: test files importing cratekit.core.jobs
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_incremental_sync.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_workers.py`, `tests/test_master_cli.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_tag_workers.py`
- Collected: 900 against a baseline of 900
- Kills: 5 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_provider_block_parks_the_job_and_makes_no_further_request`
  - `tests/test_acquire_workers.py::test_an_authentication_failure_parks_the_run_and_names_the_replacement_path`
  - `tests/test_acquire_workers.py::test_the_shipped_adapter_is_constructed_through_build_and_refuses_with_a_named_remedy`
  - `tests/test_jobs.py::test_parked_is_not_the_item_boundary`
  - `tests/test_jobs.py::test_the_parked_item_is_released_rather_than_failed`

Old text:

```
                    release_claims(store, job_id, driver=driver)
                    result.job = block(store, job_id, exc.cause.at("jobs.drive"))
```

New text:

```
                    result.job = block(store, job_id, exc.cause.at("jobs.drive"))
```

### `G22_park_before_item_boundary`

Drop the park seam entirely, so a block falls through to the item boundary and fails the track

- File: `src/cratekit/core/jobs.py`
- Surface: user
- Subset: test files importing cratekit.core.jobs
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_incremental_sync.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_workers.py`, `tests/test_master_cli.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_tag_workers.py`
- Collected: 900 against a baseline of 900
- Kills: 8 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_dead_session_logs_in_once_and_not_once_per_track`
  - `tests/test_acquire_workers.py::test_a_provider_block_parks_the_job_and_makes_no_further_request`
  - `tests/test_acquire_workers.py::test_an_authentication_failure_parks_the_run_and_names_the_replacement_path`
  - `tests/test_acquire_workers.py::test_the_shipped_adapter_is_constructed_through_build_and_refuses_with_a_named_remedy`
  - `tests/test_jobs.py::test_a_blocked_job_is_re_driven_from_the_parked_item_on_the_next_drive`
  - `tests/test_jobs.py::test_a_parked_item_blocks_the_job_and_claims_nothing_further`
  - `tests/test_jobs.py::test_parked_is_not_the_item_boundary`
  - `tests/test_jobs.py::test_the_parked_item_is_released_rather_than_failed`

Old text:

```
                except Parked as exc:
                    # BEFORE the item boundary below, which would fail the item
                    # and claim the next one. The next claim is the second
                    # request into a block, which is the one thing the pacing
                    # layer exists to never make. The item goes back to pending
                    # and the job records why it stopped.
                    release_claims(store, job_id, driver=driver)
                    result.job = block(store, job_id, exc.cause.at("jobs.drive"))
                    return result

```

New text:

```
(empty)
```

### `G27_remedy_absent_stays_absent`

Restore the non-transient remedy fallback, so a delisted track is told to relax the lossless policy

- File: `src/cratekit/acquire/cli.py`
- Surface: user
- Subset: test files importing cratekit.acquire.cli
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_track_the_provider_does_not_have_is_permanent_and_carries_no_remedy`

Old text:

```
        remedy=_remedy(result.remedy, Remedy.RETRY_LATER if transient else None),
```

New text:

```
        remedy=_remedy(result.remedy, Remedy.RETRY_LATER if transient else Remedy.RELAX_LOSSLESS_POLICY),
```

### `G28_marker_decided_by_the_file`

Take the marker requirement from the offer's claim alone, so a lying offer commits an unmarked lossy file

- File: `src/cratekit/acquire/cli.py`
- Surface: user
- Subset: test files importing cratekit.acquire.cli
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_lying_offer_under_the_permissive_policy_is_still_committed_marked`

Old text:

```
    required = result.requires_lossy_marker or lossy_landing(
        landed, policy=per_item.lossless_policy
    )
```

New text:

```
    required = result.requires_lossy_marker
```

### `G29_auth_failure_parks`

Fail the item on a dead credential instead of parking, so the driver re-authenticates once per remaining track

- File: `src/cratekit/acquire/cli.py`
- Surface: user
- Subset: test files importing cratekit.acquire.cli
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 3 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_dead_session_logs_in_once_and_not_once_per_track`
  - `tests/test_acquire_workers.py::test_an_authentication_failure_parks_the_run_and_names_the_replacement_path`
  - `tests/test_acquire_workers.py::test_the_shipped_adapter_is_constructed_through_build_and_refuses_with_a_named_remedy`

Old text:

```
        if invocation.outcome is InvocationOutcome.AUTH_FAILED:
```

New text:

```
        if False:
```

### `G30_zero_item_resume`

Drive an open job that has no items, reporting success over a list nothing read

- File: `src/cratekit/acquire/cli.py`
- Surface: user
- Subset: test files importing cratekit.acquire.cli
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_an_open_job_with_no_items_refuses_rather_than_reporting_success`

Old text:

```
                if not jobs.items(store, job.job_id):
```

New text:

```
                if False:
```

### `G31_reader_sees_the_path_as_typed`

Absolutise before the read again, so a pasted web address defeats the reader's URL refusal

- File: `src/cratekit/acquire/cli.py`
- Surface: user
- Subset: test files importing cratekit.acquire.cli
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_pasted_web_address_gets_the_readers_own_refusal`

Old text:

```
        wanted = match_cli.read_list(given)
```

New text:

```
        wanted = match_cli.read_list(given.expanduser().absolute())
```

