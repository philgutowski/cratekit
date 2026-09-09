# Mutation table: u57-recognition-and-items

Measured by `scripts/mutate.py` on 2026-09-09 19:48 UTC, branch `relay/75` at `ee162d4`. Pass kind: light.

Baseline: green, 7110 collected. pytest invocations for this batch: 29.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 7110 against 7110. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `M1_miss_family_loses_1001` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 119 | 14 | killed |
| `M2_quota_family_empty` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 119 | 4 | killed |
| `M3_auth_family_loses_3001` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 119 | 2 | killed |
| `M4_transient_range_dropped` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 119 | 4 | killed |
| `M5_empty_music_not_none` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 119 | 1 | killed |
| `M6_score_constant` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 119 | 2 | killed |
| `M7_fold_never_takes_best_score` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 119 | 1 | killed |
| `M9_fold_ignores_version` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 119 | 1 | killed |
| `M10_miss_does_not_reset_streak` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 119 | 1 | killed |
| `M11_unreached_stop_tenfold` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 119 | 2 | killed |
| `M12_quota_reads_as_failure` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 119 | 3 | killed |
| `M13_credentials_before_budget` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 119 | 1 | killed |
| `M14_monthly_ignores_used` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 119 | 1 | killed |
| `M15_ledger_after_answer` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 119 | 1 | killed |
| `M16_grid_off_by_one` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 119 | 26 | killed |
| `M18_missing_credential_is_unready` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 119 | 1 | killed |
| `C1_item_key_drops_isrc` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 35 | 2 | killed |
| `C2_item_key_ignores_provider_ref` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 35 | 3 | killed |
| `C3_missing_ref_not_refused` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 35 | 1 | killed |
| `C5_other_reading_dropped_at_thaw` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 35 | 1 | killed |
| `C6_unanswered_zero_reads_as_zero` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 35 | 1 | killed |
| `C7_foreign_job_driven` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 35 | 1 | killed |
| `C8_failed_job_exits_ok` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 35 | 1 | killed |
| `C9_never_offered` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 35 | 3 | killed |
| `C12_stray_file_sorted` | `src/cratekit/core/artifacts.py` | user | 1 file(s) | 35 | 1 | killed |

## Considered and dropped

METHOD caps a light pass at 25 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `M8_isrc_fold_always`: Two different ISRCs fold as one recording Dropped because: same guard family as M9, whose fallback branch is the one a recognised set without ISRCs walks
- `M17_short_file_zero_chunks`: A recording shorter than one chunk plans zero calls Dropped because: same function as M16, and the parametrised grid table pins both branches by value
- `M19_all_unreached_returns_empty`: A run where no call got an answer returns an empty result Dropped because: M11 exercises the same stop one line earlier, and the all-unreached branch is only reachable for a grid shorter than the stop
- `C4_fold_keeps_last`: A repeated identifier keeps the last occurrence instead of the first Dropped because: the count does not move and no current test pins which occurrence survives; a zero row known in advance is a finding to record, not a row to spend
- `C10_state_word_constant`: Every report says owned Dropped because: the same tests kill C9, which removes the offer rather than the word
- `C11_summary_calls_zero`: The resume summary reports zero calls Dropped because: maintainer facing count with one direct assertion; ranked below the user facing guards

## Row definitions

### `M1_miss_family_loses_1001`

1001, the service's own no result code, falls out of the miss family

- File: `src/cratekit/intake/acrcloud.py`
- Surface: user
- Subset: test files importing cratekit.intake.acrcloud
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 119 against a baseline of 119
- Kills: 14 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_recording_that_cannot_be_measured_or_carved_fails_without_a_call`
  - `tests/intake/test_recognition.py::test_a_set_nobody_recognised_is_zero_rows_with_the_misses_counted_not_a_refusal`
  - `tests/intake/test_recognition.py::test_an_answer_resets_the_streak_so_a_blip_does_not_end_the_run`
  - `tests/intake/test_recognition.py::test_every_status_code_lands_in_exactly_one_family[payload1-miss]`
  - `tests/intake/test_recognition.py::test_identification_returns_the_folded_rows_and_counts_every_call`
  - `tests/intake/test_recognition.py::test_the_bound_identifier_resolves_its_seams_at_call_time`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_counts_what_the_ledger_already_holds`
  - `tests/intake/test_recognition.py::test_the_two_spend_refusals_and_a_miss_are_three_different_things`
  - `tests/intake/test_workers.py::test_a_resume_that_redoes_an_offered_item_asks_nothing_twice`
  - `tests/intake/test_workers.py::test_a_set_identified_over_incomplete_coverage_queues_with_a_warning_and_freezes_the_gap`
  - `tests/intake/test_workers.py::test_a_set_nobody_recognised_is_an_honest_zero_that_says_what_it_cost`
  - `tests/intake/test_workers.py::test_a_set_where_chunks_got_no_answer_and_the_rest_named_nothing_is_a_failure_not_a_zero`
  - `tests/intake/test_workers.py::test_an_offered_track_is_a_review_item_and_no_intake_file_is_written`
  - `tests/intake/test_workers.py::test_identify_only_reports_the_same_coverage_rule`

Old text:

```
_MISS_CODES = frozenset({1001, 2004, 3015})
```

New text:

```
_MISS_CODES = frozenset({2004, 3015})
```

### `M2_quota_family_empty`

3003 stops being a quota answer, so a spent account reads as unclassified

- File: `src/cratekit/intake/acrcloud.py`
- Surface: user
- Subset: test files importing cratekit.intake.acrcloud
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 119 against a baseline of 119
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_provider_quota_answer_is_a_spend_refusal_and_never_a_miss`
  - `tests/intake/test_recognition.py::test_every_status_code_lands_in_exactly_one_family[payload4-quota]`
  - `tests/intake/test_recognition.py::test_the_two_spend_refusals_and_a_miss_are_three_different_things`
  - `tests/intake/test_workers.py::test_a_spend_refusal_at_the_queue_is_reported_as_policy_and_queues_nothing`

Old text:

```
_QUOTA_CODES = frozenset({3003})
```

New text:

```
_QUOTA_CODES = frozenset()
```

### `M3_auth_family_loses_3001`

3001, a missing or invalid access key, stops being a credential answer

- File: `src/cratekit/intake/acrcloud.py`
- Surface: user
- Subset: test files importing cratekit.intake.acrcloud
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 119 against a baseline of 119
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_credential_answer_ends_the_run_as_auth_failed`
  - `tests/intake/test_recognition.py::test_every_status_code_lands_in_exactly_one_family[payload5-auth]`

Old text:

```
_AUTH_CODES = frozenset({3001, 3002, 3006, 3014})
```

New text:

```
_AUTH_CODES = frozenset({3002, 3006, 3014})
```

### `M4_transient_range_dropped`

The 2000s stop being transient, so a recording error ends the run as unclassified

- File: `src/cratekit/intake/acrcloud.py`
- Surface: user
- Subset: test files importing cratekit.intake.acrcloud
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 119 against a baseline of 119
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_transient_answer_or_a_transport_that_raised_skips_the_chunk_and_is_counted`
  - `tests/intake/test_recognition.py::test_every_status_code_lands_in_exactly_one_family[payload10-transient]`
  - `tests/intake/test_recognition.py::test_every_status_code_lands_in_exactly_one_family[payload11-transient]`
  - `tests/intake/test_recognition.py::test_every_status_code_lands_in_exactly_one_family[payload9-transient]`

Old text:

```
    if 2000 <= code < 3000 or code in _TRANSIENT_CODES:
```

New text:

```
    if code in _TRANSIENT_CODES:
```

### `M5_empty_music_not_none`

A match answer carrying no music entry is indexed rather than read as none

- File: `src/cratekit/intake/acrcloud.py`
- Surface: user
- Subset: test files importing cratekit.intake.acrcloud
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_match_with_no_music_and_a_malformed_score_are_handled`

Old text:

```
    if not isinstance(music, list) or not music:
        return None
```

New text:

```
    if not isinstance(music, list):
        return None
```

### `M6_score_constant`

Every hit scores zero, so the fold can never prefer a better answer

- File: `src/cratekit/intake/acrcloud.py`
- Surface: user
- Subset: test files importing cratekit.intake.acrcloud
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 119 against a baseline of 119
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_match_becomes_a_wanted_row_with_the_version_split_and_the_isrc_kept`
  - `tests/intake/test_recognition.py::test_adjacent_answers_for_one_recording_fold_to_the_first_offset_and_best_score`

Old text:

```
    try:
        score = int(top.get("score", 0))
    except (TypeError, ValueError):
        score = 0
```

New text:

```
    score = 0
```

### `M7_fold_never_takes_best_score`

Adjacent answers fold to the first, whatever the later one scored

- File: `src/cratekit/intake/acrcloud.py`
- Surface: user
- Subset: test files importing cratekit.intake.acrcloud
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_adjacent_answers_for_one_recording_fold_to_the_first_offset_and_best_score`

Old text:

```
            if found.score > last.score:
```

New text:

```
            if False:
```

### `M9_fold_ignores_version`

Without an ISRC, a remix folds into the original it follows

- File: `src/cratekit/intake/acrcloud.py`
- Surface: user
- Subset: test files importing cratekit.intake.acrcloud
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_without_an_isrc_the_recording_token_decides_and_a_version_is_a_different_record`

Old text:

```
    return (
        one.wanted.recording == other.wanted.recording
        and one.wanted.version_key == other.wanted.version_key
    )
```

New text:

```
    return one.wanted.recording == other.wanted.recording
```

### `M10_miss_does_not_reset_streak`

A miss no longer resets the unanswered streak, so a blip either side of one ends the run

- File: `src/cratekit/intake/acrcloud.py`
- Surface: user
- Subset: test files importing cratekit.intake.acrcloud
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_an_answer_resets_the_streak_so_a_blip_does_not_end_the_run`

Old text:

```
        elif outcome is Outcome.MISS:
            streak = 0
            misses += 1
```

New text:

```
        elif outcome is Outcome.MISS:
            misses += 1
```

### `M11_unreached_stop_tenfold`

Fifty unanswered calls in a row before the run stops, not five

- File: `src/cratekit/intake/acrcloud.py`
- Surface: user
- Subset: test files importing cratekit.intake.acrcloud
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 119 against a baseline of 119
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_rejecting_host_stops_the_run_the_same_way`
  - `tests/intake/test_recognition.py::test_five_unanswered_calls_in_a_row_stop_the_run_and_count_what_was_spent`

Old text:

```
UNREACHED_STOP = 5
```

New text:

```
UNREACHED_STOP = 50
```

### `M12_quota_reads_as_failure`

The provider's quota answer is raised under the failure slug, not the spend slug

- File: `src/cratekit/intake/acrcloud.py`
- Surface: user
- Subset: test files importing cratekit.intake.acrcloud
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 119 against a baseline of 119
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_provider_quota_answer_is_a_spend_refusal_and_never_a_miss`
  - `tests/intake/test_recognition.py::test_the_two_spend_refusals_and_a_miss_are_three_different_things`
  - `tests/intake/test_workers.py::test_a_spend_refusal_at_the_queue_is_reported_as_policy_and_queues_nothing`

Old text:

```
    return refuse(
        "intake-recognition-spend-bound",
        f"the recognition service refused to spend: code {code} ({message or 'no message'}) "
```

New text:

```
    return refuse(
        "intake-recognition-failed",
        f"the recognition service refused to spend: code {code} ({message or 'no message'}) "
```

### `M13_credentials_before_budget`

The keychain is asked before the budget is checked

- File: `src/cratekit/intake/acrcloud.py`
- Surface: user
- Subset: test files importing cratekit.intake.acrcloud
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_the_per_run_bound_refuses_before_any_carve_call_or_credential`

Old text:

```
    assert_within(spend, planned=planned, used_this_month=counter.used(month))
    offsets = sample_offsets(duration_s)
    access_key, signing_key = credentials()
```

New text:

```
    access_key, signing_key = credentials()
    assert_within(spend, planned=planned, used_this_month=counter.used(month))
    offsets = sample_offsets(duration_s)
```

### `M14_monthly_ignores_used`

The monthly bound compares the plan alone, forgetting what the month already spent

- File: `src/cratekit/intake/acrcloud.py`
- Surface: user
- Subset: test files importing cratekit.intake.acrcloud
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_the_monthly_bound_counts_what_the_ledger_already_holds`

Old text:

```
    if budget.monthly is not None and used_this_month + planned > budget.monthly:
```

New text:

```
    if budget.monthly is not None and planned > budget.monthly:
```

### `M15_ledger_after_answer`

The call is counted after its answer arrives rather than before it is sent

- File: `src/cratekit/intake/acrcloud.py`
- Surface: user
- Subset: test files importing cratekit.intake.acrcloud
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_ledger_that_cannot_record_stops_the_run_before_the_call`

Old text:

```
        calls += 1
        try:
            counter.record(1, month)
        except (config.ConfigLockUnavailable, OSError) as exc:
            raise _failed(
                f"the recognition ledger could not record a call ({exc}), so the "
                f"call was not made; {calls - 1} call(s) were made before it",
                calls=calls - 1,
            ) from exc
        outcome, code, message, payload = _answer(transport, request)
```

New text:

```
        calls += 1
        outcome, code, message, payload = _answer(transport, request)
        try:
            counter.record(1, month)
        except (config.ConfigLockUnavailable, OSError) as exc:
            raise _failed(
                f"the recognition ledger could not record a call ({exc}), so the "
                f"call was not made; {calls - 1} call(s) were made before it",
                calls=calls - 1,
            ) from exc
```

### `M16_grid_off_by_one`

The planned count loses its last chunk

- File: `src/cratekit/intake/acrcloud.py`
- Surface: user
- Subset: test files importing cratekit.intake.acrcloud
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 119 against a baseline of 119
- Kills: 26 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_ledger_that_cannot_record_stops_the_run_before_the_call`
  - `tests/intake/test_recognition.py::test_a_provider_quota_answer_is_a_spend_refusal_and_never_a_miss`
  - `tests/intake/test_recognition.py::test_a_recording_that_cannot_be_measured_or_carved_fails_without_a_call`
  - `tests/intake/test_recognition.py::test_a_run_where_no_call_got_an_answer_is_a_failure_and_not_an_empty_set`
  - `tests/intake/test_recognition.py::test_a_set_nobody_recognised_is_zero_rows_with_the_misses_counted_not_a_refusal`
  - `tests/intake/test_recognition.py::test_a_transient_answer_or_a_transport_that_raised_skips_the_chunk_and_is_counted`
  - `tests/intake/test_recognition.py::test_an_answer_resets_the_streak_so_a_blip_does_not_end_the_run`
  - `tests/intake/test_recognition.py::test_an_answer_this_build_cannot_classify_stops_the_run_naming_the_code`
  - `tests/intake/test_recognition.py::test_identification_returns_the_folded_rows_and_counts_every_call`
  - `tests/intake/test_recognition.py::test_the_grid_is_a_function_of_the_duration_alone[12.0-offsets4]`
  - `tests/intake/test_recognition.py::test_the_grid_is_a_function_of_the_duration_alone[300.0-offsets8]`
  - `tests/intake/test_recognition.py::test_the_grid_is_a_function_of_the_duration_alone[36.0-offsets5]`
  - `tests/intake/test_recognition.py::test_the_grid_is_a_function_of_the_duration_alone[37.0-offsets6]`
  - `tests/intake/test_recognition.py::test_the_grid_is_a_function_of_the_duration_alone[60.0-offsets7]`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_counts_what_the_ledger_already_holds`
  - ... and 11 more, see the JSON sidecar

Old text:

```
    return (whole - chunk_s) // interval_s + 1
```

New text:

```
    return (whole - chunk_s) // interval_s
```

### `M18_missing_credential_is_unready`

A credential missing after the gate is reported as the gate class, not as credential-missing

- File: `src/cratekit/intake/acrcloud.py`
- Surface: user
- Subset: test files importing cratekit.intake.acrcloud
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_credential_missing_after_the_gate_is_credential_missing_with_its_own_remedy`

Old text:

```
            "credential-missing" if missing else "intake-recognition-unready",
```

New text:

```
            "intake-recognition-unready",
```

### `C1_item_key_drops_isrc`

A recognised track's identifier forgets the ISRC

- File: `src/cratekit/intake/cli.py`
- Surface: user
- Subset: test files importing cratekit.intake.cli
- Ran: `tests/intake/test_workers.py`
- Collected: 35 against a baseline of 35
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_recognised_track_is_keyed_by_recording_version_and_isrc_and_a_provider_row_by_its_id`
  - `tests/intake/test_workers.py::test_queueing_a_set_identifies_it_and_gives_the_driver_one_item_per_track`

Old text:

```
    return "rc_" + match.digest(row.recording, row.version_key, row.isrc or "")
```

New text:

```
    return "rc_" + match.digest(row.recording, row.version_key)
```

### `C2_item_key_ignores_provider_ref`

A provider row is keyed by digest rather than by the provider's identifier

- File: `src/cratekit/intake/cli.py`
- Surface: user
- Subset: test files importing cratekit.intake.cli
- Ran: `tests/intake/test_workers.py`
- Collected: 35 against a baseline of 35
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_playlist_job_runs_pending_to_done_through_the_resume_path`
  - `tests/intake/test_workers.py::test_a_recognised_track_is_keyed_by_recording_version_and_isrc_and_a_provider_row_by_its_id`
  - `tests/intake/test_workers.py::test_queueing_a_playlist_lists_it_through_the_catalogue_and_keys_items_by_provider_id`

Old text:

```
    if row.ref:
        return row.ref
    return "rc_" + match.digest(row.recording, row.version_key, row.isrc or "")
```

New text:

```
    return "rc_" + match.digest(row.recording, row.version_key, row.isrc or "")
```

### `C3_missing_ref_not_refused`

A provider row without an identifier is queued rather than refused by position

- File: `src/cratekit/intake/cli.py`
- Surface: user
- Subset: test files importing cratekit.intake.cli
- Ran: `tests/intake/test_workers.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_provider_row_without_an_identifier_is_refused_by_position`

Old text:

```
        if row.origin != match.TEXT and not row.ref
```

New text:

```
        if False
```

### `C5_other_reading_dropped_at_thaw`

The other reading of an ambiguous title is dropped when the worker thaws the row

- File: `src/cratekit/intake/cli.py`
- Surface: user
- Subset: test files importing cratekit.intake.cli
- Ran: `tests/intake/test_workers.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_titles_other_reading_survives_the_freeze`

Old text:

```
        other_reading=reading,
    )
```

New text:

```
        other_reading=None,
    )
```

### `C6_unanswered_zero_reads_as_zero`

A set where chunks got no answer and the rest named nothing is reported as nothing identified

- File: `src/cratekit/intake/cli.py`
- Surface: user
- Subset: test files importing cratekit.intake.cli
- Ran: `tests/intake/test_workers.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_set_where_chunks_got_no_answer_and_the_rest_named_nothing_is_a_failure_not_a_zero`

Old text:

```
    if not result.unreached:
        return ()
    if not result.rows:
        raise refuse(
```

New text:

```
    if not result.unreached or not result.rows:
        return ()
    if False:
        raise refuse(
```

### `C7_foreign_job_driven`

A job of another verb is driven under this verb's envelope

- File: `src/cratekit/intake/cli.py`
- Surface: user
- Subset: test files importing cratekit.intake.cli
- Ran: `tests/intake/test_workers.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_job_of_another_verb_is_refused_rather_than_driven_under_this_envelope`

Old text:

```
    if job.handler_key not in INTAKE_KEYS:
```

New text:

```
    if False:
```

### `C8_failed_job_exits_ok`

A closed job carrying a cause is reported with an OK exit

- File: `src/cratekit/intake/cli.py`
- Surface: user
- Subset: test files importing cratekit.intake.cli
- Ran: `tests/intake/test_workers.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_failure_mid_set_fails_that_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`

Old text:

```
    if not job.is_open() and job.cause is not None:
        raise CratekitError(job.cause)
    cfg = jobs.frozen_config(job)
```

New text:

```
    cfg = jobs.frozen_config(job)
```

### `C9_never_offered`

A needs review track is reported without being offered to the review queue

- File: `src/cratekit/intake/cli.py`
- Surface: user
- Subset: test files importing cratekit.intake.cli
- Ran: `tests/intake/test_workers.py`
- Collected: 35 against a baseline of 35
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_resume_that_redoes_an_offered_item_asks_nothing_twice`
  - `tests/intake/test_workers.py::test_a_set_job_runs_pending_to_done_and_reports_owned_offered_and_missing`
  - `tests/intake/test_workers.py::test_an_offered_track_is_a_review_item_and_no_intake_file_is_written`

Old text:

```
    if found.state is not match.MatchState.NEEDS_REVIEW:
        return found
```

New text:

```
    return found
```

### `C12_stray_file_sorted`

The report reader sorts every json file by its stem as a number again

- File: `src/cratekit/core/artifacts.py`
- Surface: user
- Subset: test files importing cratekit.core.artifacts
- Ran: `tests/intake/test_workers.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_stray_file_beside_the_reports_does_not_take_the_summary_down`

Old text:

```
    reports = [path for path in directory.glob("*.json") if path.stem.isdigit()]
```

New text:

```
    reports = list(directory.glob("*.json"))
```

