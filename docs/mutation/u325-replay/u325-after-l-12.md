# Mutation table: u325-after-l-12

Measured by `scripts/mutate.py` on 2026-11-22 22:23 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 100.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:22 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 8, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u69.M6_state_word` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `u73-b.B2_every_ref_kept` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `u73-b.B3_first_source_wins` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `u73.A10_every_job_skipped` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `u73.A1_blank_run` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `u73.A2_library_filter` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `u73.A3_run_filter` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 2 | killed |
| `u73.A4_intake_key_filter` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `u73.A5_oldest_first` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 2 | killed |
| `u73.A7_open_refuses` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `u73.A8_failed_refuses` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `u73.A9_skip_failed_ignored` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 3 | killed |
| `r515-operator.S11_intake_playlist_no_warning` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 72 | 6 | killed |
| `r679-a.A1_supersede_guard_both_layers` | `src/cratekit/core/review.py` | user | 3 file(s) | 879 | 5 | killed |
| `r679-a.A3_supersede_readers_predicate` | `src/cratekit/core/review.py` | user | 3 file(s) | 879 | 1 | killed |
| `r679-a.A4_resolve_admits_the_machines_verdict` | `src/cratekit/core/review.py` | user | 3 file(s) | 879 | 1 | killed |
| `r679-a.A5_import_routes_through_resolve` | `src/cratekit/core/review.py` | user | 3 file(s) | 879 | 2 | killed |
| `r679-a.A6_empty_rule_admitted` | `src/cratekit/core/review.py` | user | 3 file(s) | 879 | 2 | killed |
| `r679-a.A7_person_verdicts_are_all_verdicts` | `src/cratekit/core/review.py` | user | 3 file(s) | 879 | 2 | killed |
| `r679-a.A8_actor_is_not_the_rule` | `src/cratekit/core/review.py` | user | 3 file(s) | 879 | 11 | killed |
| `u235.T1_tail_back_to_sixteen_bits` | `src/cratekit/cli/output.py` | user | 1 file(s) | 997 | 2 | killed |
| `u235.T2_tail_thirty_two_bits` | `src/cratekit/cli/output.py` | user | 1 file(s) | 997 | 1 | killed |
| `u235.T3_tail_fifty_six_bits` | `src/cratekit/cli/output.py` | user | 1 file(s) | 997 | 1 | killed |
| `u235.T4_tail_from_the_instant` | `src/cratekit/cli/output.py` | user | 1 file(s) | 997 | 1 | killed |
| `u235.T5_instant_ignored` | `src/cratekit/cli/output.py` | maintainer | 1 file(s) | 997 | 2 | killed |
| `u235.T6_stamp_loses_its_colons` | `src/cratekit/cli/output.py` | user | 1 file(s) | 997 | 2 | killed |
| `u127-b.N6b_digest_blind_to_vox` | `src/cratekit/intake/native.py` | user | 9 file(s) | 328 | 1 | killed |
| `u127.N10_record_silent` | `src/cratekit/intake/native.py` | user | 9 file(s) | 328 | 1 | killed |
| `u127.N11_missing_unreported` | `src/cratekit/intake/native.py` | user | 9 file(s) | 328 | 1 | killed |
| `u127.N12_unscored_dropped` | `src/cratekit/intake/native.py` | user | 9 file(s) | 328 | 1 | killed |
| `u127.N14_read_back_skipped` | `src/cratekit/intake/native.py` | user | 9 file(s) | 328 | 5 | killed |
| `u127.N1_cut_strict` | `src/cratekit/intake/native.py` | user | 9 file(s) | 328 | 2 | killed |
| `u127.N2_every_add_tagged` | `src/cratekit/intake/native.py` | user | 9 file(s) | 328 | 7 | killed |
| `u127.N3_default_cut_when_uncalibrated` | `src/cratekit/intake/native.py` | user | 9 file(s) | 328 | 2 | killed |
| `u127.N4_unreadable_refuses` | `src/cratekit/intake/native.py` | user | 9 file(s) | 328 | 1 | killed |
| `u127.N5_no_category_check` | `src/cratekit/intake/native.py` | user | 9 file(s) | 328 | 1 | killed |
| `u127.N7_digest_blind_to_cut` | `src/cratekit/intake/native.py` | user | 9 file(s) | 328 | 1 | killed |
| `u127.N8_tag_never_written` | `src/cratekit/intake/native.py` | user | 9 file(s) | 328 | 7 | killed |
| `u127.N9_tag_every_added` | `src/cratekit/intake/native.py` | user | 9 file(s) | 328 | 65 | killed |
| `u193.M14_park_job_id_dropped` | `src/cratekit/core/jobs.py` | user | 5 file(s) | 508 | 1 | killed |
| `u193.M15_park_job_id_overwrites` | `src/cratekit/core/jobs.py` | maintainer | 5 file(s) | 508 | 1 | killed |
| `u193.M11_validation_floor` | `src/cratekit/core/config.py` | user | 5 file(s) | 508 | 1 | killed |
| `u193.M12_validation_bool` | `src/cratekit/core/config.py` | user | 5 file(s) | 508 | 1 | killed |
| `u193.M13_default_coefficient` | `src/cratekit/core/config.py` | user | 5 file(s) | 508 | 3 | killed |
| `u193.M10_config_not_read` | `src/cratekit/core/provider_gate.py` | user | 5 file(s) | 508 | 4 | killed |
| `u193.M1_ceiling_check_removed` | `src/cratekit/core/provider_gate.py` | user | 5 file(s) | 508 | 13 | killed |
| `u193.M2_ceiling_off_by_one` | `src/cratekit/core/provider_gate.py` | user | 5 file(s) | 508 | 13 | killed |
| `u193.M3_spent_from_process_start` | `src/cratekit/core/provider_gate.py` | user | 5 file(s) | 508 | 12 | killed |
| `u193.M8_raised_ignored` | `src/cratekit/core/provider_gate.py` | user | 5 file(s) | 508 | 7 | killed |
| `u262.C1_letters_rule_back` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 681 | 15 | killed |
| `u262.C2_any_word` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 681 | 1 | killed |
| `u262.C3_last_word` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 681 | 32 | killed |
| `u262.C4_unfolded_words` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 681 | 26 | killed |
| `u262.C5_no_with` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 681 | 7 | killed |
| `u262.C6_no_ft` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 681 | 9 | killed |
| `u262.C7_no_featuring` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 681 | 4 | killed |
| `u262.C8_no_feat` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 681 | 19 | killed |
| `a32.V4_policy_unrestricted` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 59 | 1 | killed |
| `a32.A2_stale_deleted` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 59 | 1 | killed |
| `a32.A3_stale_value` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 59 | 1 | killed |
| `a32.A5_policy_widened` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 59 | 1 | killed |
| `a32.D1_digest_drops_replaced` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 59 | 2 | killed |
| `a32.D2_digest_unordered` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 59 | 1 | killed |
| `a32.J1_wrong_unjudged` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 59 | 1 | killed |
| `a32.J2_planned_across_rows` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 59 | 1 | killed |
| `a32.J4_moved_not_refused` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 59 | 2 | killed |
| `a32.P1_tombstone_plans` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 59 | 1 | killed |
| `a32.P2_unknown_row` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 59 | 4 | killed |
| `a32.P3_unheld_value` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 59 | 2 | killed |
| `a32.P4_count_tombstones` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 59 | 5 | killed |
| `a32.P6_writes_always` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 59 | 6 | killed |
| `a32.P7_minority_boundary` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 59 | 1 | killed |
| `a32.P8_null_fellows` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 59 | 1 | killed |
| `a32.V1_any_column` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 59 | 4 | killed |
| `a32.V2_link_not_converted` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 59 | 4 | killed |
| `a32.C1_ack_after_gate` | `src/cratekit/write/row_link_cli.py` | user | 1 file(s) | 59 | 1 | killed |
| `a32.C2_abort_writes` | `src/cratekit/write/row_link_cli.py` | user | 1 file(s) | 59 | 1 | killed |
| `a32.C3_nothing_to_write_applies` | `src/cratekit/write/row_link_cli.py` | user | 1 file(s) | 59 | 1 | killed |
| `a32.C4_read_back_unasserted` | `src/cratekit/write/row_link_cli.py` | user | 1 file(s) | 59 | 1 | killed |
| `r705-b.S2_client_session_never_attaches` | `src/cratekit/acquire/provider_session.py` | user | 1 file(s) | 117 | 16 | killed |
| `r705-b.S9_playlist_read_wraps_the_park` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 117 | 1 | killed |
| `r705-b.S10_infinite_interval_accepted` | `src/cratekit/core/config.py` | user | 1 file(s) | 117 | 2 | killed |
| `r705-b.S7_acquire_one_softens_the_park_at_the_lookup` | `src/cratekit/acquire/adapter.py` | user | 1 file(s) | 117 | 1 | killed |
| `r705-b.S8_acquire_one_softens_the_park_at_the_fetch` | `src/cratekit/acquire/adapter.py` | user | 1 file(s) | 117 | 1 | killed |
| `r705-a.G10_long_wait_under_the_lock` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 117 | 1 | killed |
| `r705-a.G11_lock_limit_without_the_interval` | `src/cratekit/core/provider_gate.py` | maintainer | 1 file(s) | 117 | 1 | killed |
| `r705-a.G12_park_forgotten` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 117 | 2 | killed |
| `r705-a.G13_process_calls_not_counted` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 117 | 19 | killed |
| `r705-a.G1_interval_halved` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 117 | 9 | killed |
| `r705-a.G2_last_call_ignored` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 117 | 9 | killed |
| `r705-a.G3_retry_after_ignored` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 117 | 3 | killed |

## Row definitions

### `u69.M6_state_word`

Drop the refusal of a report whose state word this verb cannot read

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69.json`, row `M6_state_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_report_with_a_state_this_verb_cannot_read_refuses`

Old text:

```
        if report.get("state") not in _WORDS or not isinstance(report.get("track"), Mapping):
```

New text:

```
        if not isinstance(report.get("track"), Mapping):
```

### `u73-b.B2_every_ref_kept`

Stop accumulating every reference an id came from

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73-b.json`, row `B2_every_ref_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_two_playlists_sharing_a_track_list_it_once_with_both_provenances`

Old text:

```
            refs.append(said)
```

New text:

```
            pass
```

### `u73-b.B3_first_source_wins`

Let the last job an id came from win its provenance instead of the first

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73-b.json`, row `B3_first_source_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_two_playlists_sharing_a_track_list_it_once_with_both_provenances`

Old text:

```
        first.setdefault(ref, job)
```

New text:

```
        first[ref] = job
```

### `u73.A10_every_job_skipped`

Drop the refusal of a run whose every job failed, left to the layer after it

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A10_every_job_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_whose_every_job_failed_refuses_even_with_skip_failed`

Old text:

```
    if not kept:
```

New text:

```
    if False:
```

### `u73.A1_blank_run`

Drop the refusal of a blank --run, so a blank run is compared as it stands

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A1_blank_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_blank_run_is_refused_and_does_not_match_a_job_queued_with_no_run`

Old text:

```
    if not run_id.strip():
```

New text:

```
    if False:
```

### `u73.A2_library_filter`

Drop the library half of the run selection, so the run alone picks jobs

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A2_library_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_another_librarys_job_in_the_same_run_is_not_this_librarys_to_list`

Old text:

```
and job.library_id == library_id
```

New text:

```
and True
```

### `u73.A3_run_filter`

Drop the run half of the selection, so every intake job for the library is listed

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A3_run_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_job_queued_by_hand_is_not_part_of_any_run`
  - `tests/test_intake_missing.py::test_an_unknown_run_is_refused_by_name`

Old text:

```
(job.payload or {}).get(RUN_ID) == run_id
```

New text:

```
True
```

### `u73.A4_intake_key_filter`

Drop the intake handler key filter, so a labels or favourites job in the run is selected

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A4_intake_key_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_job_of_another_verb_in_the_same_run_is_not_listed`

Old text:

```
            if job.handler_key in intake_cli.INTAKE_KEYS
```

New text:

```
            if True
```

### `u73.A5_oldest_first`

Reverse the job order, newest first, so first source wins picks the later playlist

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A5_oldest_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_two_playlists_sharing_a_track_list_it_once_with_both_provenances`

Old text:

```
key=lambda job: (job.created, job.job_id),
```

New text:

```
key=lambda job: (job.created, job.job_id), reverse=True,
```

### `u73.A7_open_refuses`

Drop the refusal of a run holding an open job

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A7_open_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_an_open_job_refuses_the_whole_run_and_names_it`

Old text:

```
    if still_open:
```

New text:

```
    if False:
```

### `u73.A8_failed_refuses`

Drop the refusal of a run holding a failed or cancelled job

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A8_failed_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_failed_job_is_named_and_refuses_the_run_without_skip_failed`

Old text:

```
    if unfinished and not skip_failed:
```

New text:

```
    if False:
```

### `u73.A9_skip_failed_ignored`

Ignore --skip-failed, so a failed job refuses the run whatever the flag says

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A9_skip_failed_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_whose_every_job_failed_refuses_even_with_skip_failed`
  - `tests/test_intake_missing.py::test_skip_failed_lists_the_rest_and_names_what_it_left_out`
  - `tests/test_intake_missing.py::test_skip_failed_over_tracks_only_handed_on_writes_them_rather_than_refusing`

Old text:

```
    if unfinished and not skip_failed:
```

New text:

```
    if unfinished:
```

### `r515-operator.S11_intake_playlist_no_warning`

An intake playlist listed short carries no warning

- File: `src/cratekit/intake/cli.py`
- Source: `r515-operator.json`, row `S11_intake_playlist_no_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 6 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_playlist_declaring_ten_with_two_withheld_queues_eight_and_warns`
  - `tests/test_intake_missing.py::test_a_playlist_whose_every_track_is_withheld_is_not_a_quiet_no_op`
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`
  - `tests/test_intake_missing.py::test_the_default_human_output_names_the_playlist_shortfall`
  - `tests/test_intake_missing.py::test_the_default_human_output_names_the_shortfall`

Old text:

```
        warnings = (warned(short),) if short is not None else ()
```

New text:

```
        warnings = ()
```

### `r679-a.A1_supersede_guard_both_layers`

supersede: drop the empty column condition from the read and the write together, so a person's verdict is overwritten

- File: `src/cratekit/core/review.py`
- Source: `r679-a.json`, row `A1_supersede_guard_both_layers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_review_queue.py`, `tests/test_match_states.py`, `tests/intake/test_workers.py`
- Collected: 879 against a baseline of 879
- Kills: 5 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_persons_answer_is_never_overwritten_by_a_later_resolution`
  - `tests/test_review_queue.py::test_supersede_never_overwrites_a_persons_verdict[accepted]`
  - `tests/test_review_queue.py::test_supersede_never_overwrites_a_persons_verdict[rejected]`
  - `tests/test_review_queue.py::test_supersede_never_overwrites_a_verdict_this_build_cannot_read`
  - `tests/test_review_queue.py::test_supersede_takes_several_identifiers_and_retires_only_the_open_ones_among_them`

Old text:

```
            f"SELECT item_id FROM review_items WHERE item_id IN ({marks}) "
            f"AND verdict IS NULL ORDER BY ordinal",
            wanted,
        )
    )
    if not open_ids:
        return ()
    now = timestamp()
    marks = ", ".join("?" for _ in open_ids)
    with store.immediate() as conn:
        conn.execute(
            f"UPDATE review_items SET verdict = ?, option = NULL, actor = ?, decided = ?, "
            f"updated = ? WHERE item_id IN ({marks}) AND verdict IS NULL",
```

New text:

```
            f"SELECT item_id FROM review_items WHERE item_id IN ({marks}) "
            f"ORDER BY ordinal",
            wanted,
        )
    )
    if not open_ids:
        return ()
    now = timestamp()
    marks = ", ".join("?" for _ in open_ids)
    with store.immediate() as conn:
        conn.execute(
            f"UPDATE review_items SET verdict = ?, option = NULL, actor = ?, decided = ?, "
            f"updated = ? WHERE item_id IN ({marks})",
```

### `r679-a.A3_supersede_readers_predicate`

supersede: widen the write's condition to the reader's unresolved predicate, so a verdict a newer build wrote is overwritten

- File: `src/cratekit/core/review.py`
- Source: `r679-a.json`, row `A3_supersede_readers_predicate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_review_queue.py`, `tests/test_match_states.py`, `tests/intake/test_workers.py`
- Collected: 879 against a baseline of 879
- Kills: 1 (killed)
- Killed:
  - `tests/test_review_queue.py::test_supersede_never_overwrites_a_verdict_this_build_cannot_read`

Old text:

```
            f"SELECT item_id FROM review_items WHERE item_id IN ({marks}) "
            f"AND verdict IS NULL ORDER BY ordinal",
            wanted,
        )
    )
    if not open_ids:
        return ()
    now = timestamp()
    marks = ", ".join("?" for _ in open_ids)
    with store.immediate() as conn:
        conn.execute(
            f"UPDATE review_items SET verdict = ?, option = NULL, actor = ?, decided = ?, "
            f"updated = ? WHERE item_id IN ({marks}) AND verdict IS NULL",
```

New text:

```
            f"SELECT item_id FROM review_items WHERE item_id IN ({marks}) "
            f"AND (verdict IS NULL OR verdict NOT IN ('accepted', 'rejected', 'superseded')) ORDER BY ordinal",
            wanted,
        )
    )
    if not open_ids:
        return ()
    now = timestamp()
    marks = ", ".join("?" for _ in open_ids)
    with store.immediate() as conn:
        conn.execute(
            f"UPDATE review_items SET verdict = ?, option = NULL, actor = ?, decided = ?, "
            f"updated = ? WHERE item_id IN ({marks}) AND (verdict IS NULL OR verdict NOT IN ('accepted', 'rejected', 'superseded'))",
```

### `r679-a.A4_resolve_admits_the_machines_verdict`

resolve: drop the refusal of the machine's verdict, so a batch or an import can land it with a candidate

- File: `src/cratekit/core/review.py`
- Source: `r679-a.json`, row `A4_resolve_admits_the_machines_verdict`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_review_queue.py`, `tests/test_match_states.py`, `tests/intake/test_workers.py`
- Collected: 879 against a baseline of 879
- Kills: 1 (killed)
- Killed:
  - `tests/test_review_queue.py::test_resolve_and_the_batch_refuse_the_machines_verdict`

Old text:

```
    if verdict not in PERSON_VERDICTS:
        # The machine's verdict has its own writer with its own invariants: no
```

New text:

```
    if False:
        # The machine's verdict has its own writer with its own invariants: no
```

### `r679-a.A5_import_routes_through_resolve`

import: send an incoming superseded verdict through resolve rather than supersede

- File: `src/cratekit/core/review.py`
- Source: `r679-a.json`, row `A5_import_routes_through_resolve`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_review_queue.py`, `tests/test_match_states.py`, `tests/intake/test_workers.py`
- Collected: 879 against a baseline of 879
- Kills: 2 (killed)
- Killed:
  - `tests/test_review_queue.py::test_an_export_carrying_the_third_verdict_imports_without_conflict`
  - `tests/test_review_queue.py::test_an_import_carries_the_machines_verdict_under_the_machines_rules`

Old text:

```
        if verdict is Verdict.SUPERSEDED:
            # The machine's verdict travels under the machine's rules: the
```

New text:

```
        if False:
            # The machine's verdict travels under the machine's rules: the
```

### `r679-a.A6_empty_rule_admitted`

supersede: drop the refusal of an empty rule, so a superseded item can name nothing

- File: `src/cratekit/core/review.py`
- Source: `r679-a.json`, row `A6_empty_rule_admitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_review_queue.py`, `tests/test_match_states.py`, `tests/intake/test_workers.py`
- Collected: 879 against a baseline of 879
- Kills: 2 (killed)
- Killed:
  - `tests/test_review_queue.py::test_an_import_carries_the_machines_verdict_under_the_machines_rules`
  - `tests/test_review_queue.py::test_supersede_refuses_an_empty_rule`

Old text:

```
    if not rule:
        raise refuse(
            "review-selection-invalid",
            "a superseded item names the rule that owned its row; an empty one "
```

New text:

```
    if False:
        raise refuse(
            "review-selection-invalid",
            "a superseded item names the rule that owned its row; an empty one "
```

### `r679-a.A7_person_verdicts_are_all_verdicts`

PERSON_VERDICTS: include the machine's verdict, so the command line offers it

- File: `src/cratekit/core/review.py`
- Source: `r679-a.json`, row `A7_person_verdicts_are_all_verdicts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_review_queue.py`, `tests/test_match_states.py`, `tests/intake/test_workers.py`
- Collected: 879 against a baseline of 879
- Kills: 2 (killed)
- Killed:
  - `tests/test_review_queue.py::test_resolve_and_the_batch_refuse_the_machines_verdict`
  - `tests/test_review_queue.py::test_the_command_line_offers_a_person_only_the_persons_verdicts`

Old text:

```
    member for member in Verdict if member is not Verdict.SUPERSEDED
```

New text:

```
    member for member in Verdict
```

### `r679-a.A8_actor_is_not_the_rule`

supersede: write a fixed word as the actor instead of the rule that owned the row

- File: `src/cratekit/core/review.py`
- Source: `r679-a.json`, row `A8_actor_is_not_the_rule`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_review_queue.py`, `tests/test_match_states.py`, `tests/intake/test_workers.py`
- Collected: 879 against a baseline of 879
- Kills: 11 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_an_intake_job_that_owns_a_row_by_isrc_retires_the_question_an_earlier_job_asked`
  - `tests/test_match_states.py::test_a_retired_question_whose_row_goes_missing_keeps_the_verdict`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[credited-exact]`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[isrc-exact]`
  - `tests/test_match_states.py::test_the_verb_lists_a_retired_question_only_when_asked_for_everything`
  - `tests/test_review_queue.py::test_a_batch_resolution_does_not_touch_items_a_resolution_superseded`
  - `tests/test_review_queue.py::test_a_superseded_item_offered_again_is_neither_reopened_nor_duplicated`
  - `tests/test_review_queue.py::test_an_export_carrying_the_third_verdict_imports_without_conflict`
  - `tests/test_review_queue.py::test_an_import_carries_the_machines_verdict_under_the_machines_rules`
  - `tests/test_review_queue.py::test_supersede_retires_an_open_item_naming_the_rule_and_it_leaves_the_open_list`
  - `tests/test_review_queue.py::test_supersede_takes_several_identifiers_and_retires_only_the_open_ones_among_them`

Old text:

```
            (str(Verdict.SUPERSEDED), rule, now, now, *open_ids),
```

New text:

```
            (str(Verdict.SUPERSEDED), "resolution", now, now, *open_ids),
```

### `u235.T1_tail_back_to_sixteen_bits`

new_run_id: the tail goes back to token_hex(2), four hex characters, the width the card's failure came from

- File: `src/cratekit/cli/output.py`
- Source: `u235.json`, row `T1_tail_back_to_sixteen_bits`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 997 against a baseline of 997
- Kills: 2 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_run_identifier_carries_sixty_four_bits_of_random_tail`
  - `tests/test_cli_contract.py::test_two_thousand_identifiers_minted_inside_one_second_are_all_distinct`

Old text:

```
    return f"{moment.strftime('%Y-%m-%dT%H:%M:%SZ')}-{secrets.token_hex(8)}"
```

New text:

```
    return f"{moment.strftime('%Y-%m-%dT%H:%M:%SZ')}-{secrets.token_hex(2)}"
```

### `u235.T2_tail_thirty_two_bits`

new_run_id: the tail narrows to token_hex(4), eight hex characters, a width the distinct test alone cannot tell from sixty four

- File: `src/cratekit/cli/output.py`
- Source: `u235.json`, row `T2_tail_thirty_two_bits`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 997 against a baseline of 997
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_run_identifier_carries_sixty_four_bits_of_random_tail`

Old text:

```
    return f"{moment.strftime('%Y-%m-%dT%H:%M:%SZ')}-{secrets.token_hex(8)}"
```

New text:

```
    return f"{moment.strftime('%Y-%m-%dT%H:%M:%SZ')}-{secrets.token_hex(4)}"
```

### `u235.T3_tail_fifty_six_bits`

new_run_id: the tail narrows by one byte, token_hex(7), fourteen hex characters

- File: `src/cratekit/cli/output.py`
- Source: `u235.json`, row `T3_tail_fifty_six_bits`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 997 against a baseline of 997
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_run_identifier_carries_sixty_four_bits_of_random_tail`

Old text:

```
    return f"{moment.strftime('%Y-%m-%dT%H:%M:%SZ')}-{secrets.token_hex(8)}"
```

New text:

```
    return f"{moment.strftime('%Y-%m-%dT%H:%M:%SZ')}-{secrets.token_hex(7)}"
```

### `u235.T4_tail_from_the_instant`

new_run_id: the tail keeps its sixteen hex characters but is read off the instant's microseconds, so two ids at one instant are equal

- File: `src/cratekit/cli/output.py`
- Source: `u235.json`, row `T4_tail_from_the_instant`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 997 against a baseline of 997
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_two_thousand_identifiers_minted_inside_one_second_are_all_distinct`

Old text:

```
    return f"{moment.strftime('%Y-%m-%dT%H:%M:%SZ')}-{secrets.token_hex(8)}"
```

New text:

```
    return f"{moment.strftime('%Y-%m-%dT%H:%M:%SZ')}-{moment.microsecond:016x}"
```

### `u235.T5_instant_ignored`

new_run_id: the instant a caller hands it is ignored and the clock is read instead

- File: `src/cratekit/cli/output.py`
- Source: `u235.json`, row `T5_instant_ignored`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 997 against a baseline of 997
- Kills: 2 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_run_identifier_carries_sixty_four_bits_of_random_tail`
  - `tests/test_cli_contract.py::test_two_thousand_identifiers_minted_inside_one_second_are_all_distinct`

Old text:

```
    moment = now or datetime.now(timezone.utc)
    return f"{moment.strftime('%Y-%m-%dT%H:%M:%SZ')}-{secrets.token_hex(8)}"
```

New text:

```
    moment = datetime.now(timezone.utc)
    return f"{moment.strftime('%Y-%m-%dT%H:%M:%SZ')}-{secrets.token_hex(8)}"
```

### `u235.T6_stamp_loses_its_colons`

new_run_id: the stamp drops its colons, so an id minted after the widening no longer reads like one minted before it

- File: `src/cratekit/cli/output.py`
- Source: `u235.json`, row `T6_stamp_loses_its_colons`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 997 against a baseline of 997
- Kills: 2 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_run_identifier_carries_sixty_four_bits_of_random_tail`
  - `tests/test_cli_contract.py::test_two_thousand_identifiers_minted_inside_one_second_are_all_distinct`

Old text:

```
    return f"{moment.strftime('%Y-%m-%dT%H:%M:%SZ')}-{secrets.token_hex(8)}"
```

New text:

```
    return f"{moment.strftime('%Y-%m-%dT%H%M%SZ')}-{secrets.token_hex(8)}"
```

### `u127-b.N6b_digest_blind_to_vox`

Drop each added row's score and answer from the digest, after the engine test

- File: `src/cratekit/intake/native.py`
- Source: `u127-b.json`, row `N6b_digest_blind_to_vox`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 328 against a baseline of 328
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_the_engine_digest_covers_each_rows_score_and_answer`

Old text:

```
                "rows": [[str(row.target), row.voxlevel, row.vox] for row in plan.to_add()],
```

New text:

```
                "rows": [[str(row.target)] for row in plan.to_add()],
```

### `u127.N10_record_silent`

Record no commit under the vocals key, so a restore cannot count the tags

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N10_record_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 328 against a baseline of 328
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_the_tag_is_written_under_the_vocals_category_the_vocals_verb_uses`

Old text:

```
    if vox_written > 0:
```

New text:

```
    if vox_written > 10**6:
```

### `u127.N11_missing_unreported`

Never report a planned tag that adoption does not read back

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N11_missing_unreported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 328 against a baseline of 328
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_tag_written_under_a_removed_category_is_said_and_never_counted`

Old text:

```
            row.target for row, content_id in added_ids if row.vox and content_id not in voxed
```

New text:

```
            row.target for row, content_id in added_ids if False
```

### `u127.N12_unscored_dropped`

Name no unscored file on the landed record

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N12_unscored_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 328 against a baseline of 328
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_file_with_no_score_gets_no_tag_and_is_named`

Old text:

```
    unscored = {row.target for row in plan.vox_unscored()}
```

New text:

```
    unscored = set()
```

### `u127.N14_read_back_skipped`

Never read the tag back, so every landed row reports untagged

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N14_read_back_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 328 against a baseline of 328
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_file_with_no_score_gets_no_tag_and_is_named`
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[above]`
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[exactly-at-the-cut]`
  - `tests/test_intake_land_vox_native.py::test_the_tag_is_written_under_the_vocals_category_the_vocals_verb_uses`
  - `tests/test_intake_writers_native.py::test_intake_file_tags_its_row_vox_from_the_files_score`

Old text:

```
            _vox_read_back(db) if any(row.vox for row, _ in added_ids) else (frozenset(), "")
```

New text:

```
            (frozenset(), "") if any(row.vox for row, _ in added_ids) else (frozenset(), "")
```

### `u127.N1_cut_strict`

Compare the score strictly above the cut, so a file exactly at the cut is not tagged

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N1_cut_strict`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 328 against a baseline of 328
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[exactly-at-the-cut]`
  - `tests/test_intake_writers_native.py::test_intake_file_tags_its_row_vox_from_the_files_score`

Old text:

```
        values = metadata_cli.vocal_tag_values(level, None, cut)
        scored.append(replace(row, voxlevel=level, vox=metadata_cli.VALUE_VOX in values))
```

New text:

```
        values = metadata_cli.vocal_tag_values(level, None, cut + 0.5)
        scored.append(replace(row, voxlevel=level, vox=metadata_cli.VALUE_VOX in values))
```

### `u127.N2_every_add_tagged`

Tag every added row whatever its score, the guess the brief forbids

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N2_every_add_tagged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 328 against a baseline of 328
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_file_with_no_score_gets_no_tag_and_is_named`
  - `tests/test_intake_land_vox_native.py::test_a_hand_placed_tag_on_a_row_already_present_survives`
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[below]`
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[zero]`
  - `tests/test_intake_land_vox_native.py::test_the_digest_moves_when_a_tag_is_planned`
  - `tests/test_intake_land_vox_native.py::test_the_screen_counts_the_tagged_rows_against_the_cut`
  - `tests/test_intake_land_vox_native.py::test_the_tag_is_written_under_the_vocals_category_the_vocals_verb_uses`

Old text:

```
        scored.append(replace(row, voxlevel=level, vox=metadata_cli.VALUE_VOX in values))
```

New text:

```
        scored.append(replace(row, voxlevel=level, vox=True))
```

### `u127.N3_default_cut_when_uncalibrated`

Tag from the vocals verb's default cut on a library with no calibration instead of blocking

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N3_default_cut_when_uncalibrated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 328 against a baseline of 328
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_library_with_no_calibration_tags_nothing_and_says_why`
  - `tests/test_intake_writers_native.py::test_one_file_becomes_one_row_and_one_playlist_under_the_adopted_root`

Old text:

```
    if cut is None:
        return rows, None, VOX_UNCALIBRATED
```

New text:

```
    if cut is None:
        cut = metadata_cli.DEFAULT_VOCAL_THRESHOLD
```

### `u127.N4_unreadable_refuses`

Let an unreadable calibration refuse the landing rather than block the tag

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N4_unreadable_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 328 against a baseline of 328
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_an_unreadable_calibration_tags_nothing_and_lands_the_batch`

Old text:

```
    except CratekitError as exc:
        # AN UNREADABLE CALIBRATION BLOCKS THE TAG, NOT THE LANDING. The
```

New text:

```
    except ValueError as exc:
        # AN UNREADABLE CALIBRATION BLOCKS THE TAG, NOT THE LANDING. The
```

### `u127.N5_no_category_check`

Skip the writer's question at plan time, so a library with no category fails after the moves

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N5_no_category_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 328 against a baseline of 328
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_library_with_no_category_to_copy_tags_nothing_and_lands_the_batch`

Old text:

```
    if not rb_writer.my_tag_writable(db):
        return rows, cut, VOX_NO_CATEGORY
```

New text:

```
    if False:
        return rows, cut, VOX_NO_CATEGORY
```

### `u127.N7_digest_blind_to_cut`

Drop the cut from the digest

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N7_digest_blind_to_cut`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 328 against a baseline of 328
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_the_digest_moves_with_the_cut`

Old text:

```
                "cut": plan.vox_cut,
```

New text:

```
                "cut": None,
```

### `u127.N8_tag_never_written`

Write no tag at the apply, the defect R-841 measured

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N8_tag_never_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 328 against a baseline of 328
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_file_with_no_score_gets_no_tag_and_is_named`
  - `tests/test_intake_land_vox_native.py::test_a_hand_placed_tag_on_a_row_already_present_survives`
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[above]`
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[exactly-at-the-cut]`
  - `tests/test_intake_land_vox_native.py::test_a_library_with_another_category_only_gains_the_vocals_category`
  - `tests/test_intake_land_vox_native.py::test_the_tag_is_written_under_the_vocals_category_the_vocals_verb_uses`
  - `tests/test_intake_writers_native.py::test_intake_file_tags_its_row_vox_from_the_files_score`

Old text:

```
            vox_written = _tag_vox(db, added_ids)
```

New text:

```
            vox_written = 0
```

### `u127.N9_tag_every_added`

Write the tag on every added row, not only those the plan tagged

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N9_tag_every_added`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 328 against a baseline of 328
- Kills: 65 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists_native.py::test_a_job_queued_with_no_name_lands_in_the_batch_playlist_as_before`
  - `tests/test_intake_land_account_playlists_native.py::test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists_native.py::test_a_track_both_playlists_brought_in_is_a_member_of_both`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_in_two_account_playlists_is_in_both`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_an_undated_playlist_from_before_u175_is_left_as_it_is`
  - `tests/test_intake_land_account_playlists_native.py::test_the_gate_screen_counts_the_owned_rows_beside_the_new`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_the_rotation_ages_an_account_playlist_by_its_landing_date`
  - ... and 50 more, see the JSON sidecar

Old text:

```
    content_ids = [content_id for row, content_id in added if row.vox]
```

New text:

```
    content_ids = [content_id for row, content_id in added]
```

### `u193.M14_park_job_id_dropped`

jobs._parked_cause: do not name the job, so the continue command cannot resume it

- File: `src/cratekit/core/jobs.py`
- Source: `u193.json`, row `M14_park_job_id_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 508 against a baseline of 508
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_the_ceiling_parks_a_job_and_the_resumed_job_continues`

Old text:

```
    if "job_id" in (cause.detail or {}):
        return cause
```

New text:

```
    if True:
        return cause
```

### `u193.M15_park_job_id_overwrites`

jobs._parked_cause: overwrite a job id the cause already carries

- File: `src/cratekit/core/jobs.py`
- Source: `u193.json`, row `M15_park_job_id_overwrites`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 508 against a baseline of 508
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_park_that_names_its_job_keeps_its_own_job_id`

Old text:

```
    if "job_id" in (cause.detail or {}):
        return cause
```

New text:

```
    if False:
        return cause
```

### `u193.M11_validation_floor`

_validate_provider: accept zero as a ceiling

- File: `src/cratekit/core/config.py`
- Source: `u193.json`, row `M11_validation_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 508 against a baseline of 508
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_ceiling_that_is_not_a_positive_whole_number_refuses_at_load[0]`

Old text:

```
        not isinstance(ceiling, int) or isinstance(ceiling, bool) or ceiling < 1
```

New text:

```
        not isinstance(ceiling, int) or isinstance(ceiling, bool) or ceiling < 0
```

### `u193.M12_validation_bool`

_validate_provider: accept true as a ceiling of one

- File: `src/cratekit/core/config.py`
- Source: `u193.json`, row `M12_validation_bool`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 508 against a baseline of 508
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_ceiling_that_is_not_a_positive_whole_number_refuses_at_load[True]`

Old text:

```
        not isinstance(ceiling, int) or isinstance(ceiling, bool) or ceiling < 1
```

New text:

```
        not isinstance(ceiling, int) or ceiling < 1
```

### `u193.M13_default_coefficient`

config: halve the default ceiling

- File: `src/cratekit/core/config.py`
- Source: `u193.json`, row `M13_default_coefficient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 508 against a baseline of 508
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_playlists_releases.py::test_an_estimate_over_the_call_ceiling_asks_even_under_the_builds_own_line`
  - `tests/test_label_playlists_releases.py::test_the_estimate_is_two_calls_a_release_at_the_configured_pace`
  - `tests/test_provider_gate.py::test_the_ceiling_defaults_to_five_hundred_and_round_trips`

Old text:

```
DEFAULT_PROVIDER_CALLS_PER_COMMAND = 500
```

New text:

```
DEFAULT_PROVIDER_CALLS_PER_COMMAND = 250
```

### `u193.M10_config_not_read`

GateSettings.from_config: drop the configured ceiling, so the default always holds

- File: `src/cratekit/core/provider_gate.py`
- Source: `u193.json`, row `M10_config_not_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 508 against a baseline of 508
- Kills: 4 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_ceiling_stop_a_verb_swallowed_is_still_said`
  - `tests/test_provider_gate.py::test_a_verb_at_its_ceiling_is_blocked_and_names_the_exact_command_that_continues`
  - `tests/test_provider_gate.py::test_calls_on_the_command_line_lets_one_run_pass_and_the_next_is_back_at_the_ceiling`
  - `tests/test_provider_gate.py::test_the_ceiling_defaults_to_five_hundred_and_round_trips`

Old text:

```
            calls_per_command=int(provider.calls_per_command),
```

New text:

```
(empty)
```

### `u193.M1_ceiling_check_removed`

Gate.call: never ask the ceiling, so a command spends past it

- File: `src/cratekit/core/provider_gate.py`
- Source: `u193.json`, row `M1_ceiling_check_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 508 against a baseline of 508
- Kills: 13 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_ceiling_stop_a_verb_swallowed_is_still_said`
  - `tests/test_provider_gate.py::test_a_command_is_charged_only_for_its_own_calls`
  - `tests/test_provider_gate.py::test_a_command_stops_before_the_call_past_its_ceiling_with_the_count_at_the_ceiling`
  - `tests/test_provider_gate.py::test_a_nested_dispatch_keeps_the_outer_commands_count`
  - `tests/test_provider_gate.py::test_a_raised_ceiling_lasts_one_run_and_the_next_is_back_at_the_configured_one`
  - `tests/test_provider_gate.py::test_a_separate_session_such_as_the_media_segment_fetch_is_not_counted`
  - `tests/test_provider_gate.py::test_a_verb_at_its_ceiling_is_blocked_and_names_the_exact_command_that_continues`
  - `tests/test_provider_gate.py::test_calls_on_the_command_line_lets_one_run_pass_and_the_next_is_back_at_the_ceiling`
  - `tests/test_provider_gate.py::test_the_ceiling_never_says_kept_over_work_a_continue_does_again`
  - `tests/test_provider_gate.py::test_the_ceiling_parks_a_job_and_the_resumed_job_continues`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_calls_already_given`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_spaced_calls_already_given`
  - `tests/test_provider_gate.py::test_the_stop_is_remembered_so_a_swallowing_tool_still_parks`

Old text:

```
                    if scope.spent() >= line:
```

New text:

```
                    if False:
```

### `u193.M2_ceiling_off_by_one`

Gate.call: stop only past the ceiling, so one call more than the line is sent

- File: `src/cratekit/core/provider_gate.py`
- Source: `u193.json`, row `M2_ceiling_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 508 against a baseline of 508
- Kills: 13 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_ceiling_stop_a_verb_swallowed_is_still_said`
  - `tests/test_provider_gate.py::test_a_command_is_charged_only_for_its_own_calls`
  - `tests/test_provider_gate.py::test_a_command_stops_before_the_call_past_its_ceiling_with_the_count_at_the_ceiling`
  - `tests/test_provider_gate.py::test_a_nested_dispatch_keeps_the_outer_commands_count`
  - `tests/test_provider_gate.py::test_a_raised_ceiling_lasts_one_run_and_the_next_is_back_at_the_configured_one`
  - `tests/test_provider_gate.py::test_a_separate_session_such_as_the_media_segment_fetch_is_not_counted`
  - `tests/test_provider_gate.py::test_a_verb_at_its_ceiling_is_blocked_and_names_the_exact_command_that_continues`
  - `tests/test_provider_gate.py::test_calls_on_the_command_line_lets_one_run_pass_and_the_next_is_back_at_the_ceiling`
  - `tests/test_provider_gate.py::test_the_ceiling_never_says_kept_over_work_a_continue_does_again`
  - `tests/test_provider_gate.py::test_the_ceiling_parks_a_job_and_the_resumed_job_continues`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_calls_already_given`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_spaced_calls_already_given`
  - `tests/test_provider_gate.py::test_the_stop_is_remembered_so_a_swallowing_tool_still_parks`

Old text:

```
                    if scope.spent() >= line:
```

New text:

```
                    if scope.spent() > line:
```

### `u193.M3_spent_from_process_start`

Command.spent: count from process start, so a command is charged for calls before it

- File: `src/cratekit/core/provider_gate.py`
- Source: `u193.json`, row `M3_spent_from_process_start`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 508 against a baseline of 508
- Kills: 12 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_ceiling_stop_a_verb_swallowed_is_still_said`
  - `tests/test_provider_gate.py::test_a_command_is_charged_only_for_its_own_calls`
  - `tests/test_provider_gate.py::test_a_command_stops_before_the_call_past_its_ceiling_with_the_count_at_the_ceiling`
  - `tests/test_provider_gate.py::test_a_nested_dispatch_keeps_the_outer_commands_count`
  - `tests/test_provider_gate.py::test_a_raised_ceiling_lasts_one_run_and_the_next_is_back_at_the_configured_one`
  - `tests/test_provider_gate.py::test_a_separate_session_such_as_the_media_segment_fetch_is_not_counted`
  - `tests/test_provider_gate.py::test_a_verb_at_its_ceiling_is_blocked_and_names_the_exact_command_that_continues`
  - `tests/test_provider_gate.py::test_calls_on_the_command_line_lets_one_run_pass_and_the_next_is_back_at_the_ceiling`
  - `tests/test_provider_gate.py::test_the_ceiling_never_says_kept_over_work_a_continue_does_again`
  - `tests/test_provider_gate.py::test_the_ceiling_parks_a_job_and_the_resumed_job_continues`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_spaced_calls_already_given`
  - `tests/test_provider_gate.py::test_the_stop_is_remembered_so_a_swallowing_tool_still_parks`

Old text:

```
        return max(0, _PROCESS_CALLS - self.started)
```

New text:

```
        return max(0, _PROCESS_CALLS)
```

### `u193.M8_raised_ignored`

ceiling: ignore the raised ceiling, so --calls never lifts the line

- File: `src/cratekit/core/provider_gate.py`
- Source: `u193.json`, row `M8_raised_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 508 against a baseline of 508
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_playlists_releases.py::test_a_ceiling_raised_low_for_the_run_is_said_at_the_crawl_gate`
  - `tests/test_provider_gate.py::test_a_detached_child_reads_the_raised_ceiling_off_the_environment[700-700]`
  - `tests/test_provider_gate.py::test_a_raised_ceiling_lasts_one_run_and_the_next_is_back_at_the_configured_one`
  - `tests/test_provider_gate.py::test_calls_on_the_command_line_lets_one_run_pass_and_the_next_is_back_at_the_ceiling`
  - `tests/test_provider_gate.py::test_the_ceiling_parks_a_job_and_the_resumed_job_continues`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_calls_already_given`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_spaced_calls_already_given`

Old text:

```
    if scope is not None and scope.raised is not None:
        return scope.raised
```

New text:

```
    if False:
        return scope.raised
```

### `u262.C1_letters_rule_back`

_is_a_credit: answer by the folded group's first letters again, the defect, so (Without You Remix) is a credit

- File: `src/cratekit/acquire/match.py`
- Source: `u262.json`, row `C1_letters_rule_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_uncredited_tombstone.py`, `tests/test_tombstones.py`
- Collected: 681 against a baseline of 681
- Kills: 15 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_defect_title_keeps_the_tombstone_identity_its_spelling_always_had`
  - `tests/test_match_states.py::test_a_group_that_only_begins_with_a_credits_letters_is_a_version[Feature Edit]`
  - `tests/test_match_states.py::test_a_group_that_only_begins_with_a_credits_letters_is_a_version[Featureless Dub]`
  - `tests/test_match_states.py::test_a_group_that_only_begins_with_a_credits_letters_is_a_version[Withdrawn Mix]`
  - `tests/test_match_states.py::test_a_group_that_only_begins_with_a_credits_letters_is_a_version[Within Mix]`
  - `tests/test_match_states.py::test_a_group_that_only_begins_with_a_credits_letters_is_a_version[Without You Remix]`
  - `tests/test_match_states.py::test_a_library_file_whose_group_only_begins_with_a_credits_letters_is_that_version`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(Without You Remix)-expected11]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[Feature Edit]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[Featureless Dub]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[Featurette]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[Ftw Edit]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[Withdrawn Mix]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[Within Mix]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[Without You Remix]`

Old text:

```
    return bool(words) and words[0] in _CREDIT_MARKERS
```

New text:

```
    return any(" ".join(words).startswith(marker) for marker in _CREDIT_MARKERS)
```

### `u262.C2_any_word`

_is_a_credit: a marker anywhere in the group makes a credit, so (Live with Strings) loses its version

- File: `src/cratekit/acquire/match.py`
- Source: `u262.json`, row `C2_any_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_uncredited_tombstone.py`, `tests/test_tombstones.py`
- Collected: 681 against a baseline of 681
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[Live with Strings]`

Old text:

```
    return bool(words) and words[0] in _CREDIT_MARKERS
```

New text:

```
    return any(word in _CREDIT_MARKERS for word in words)
```

### `u262.C3_last_word`

_is_a_credit: ask the group's last word rather than its first

- File: `src/cratekit/acquire/match.py`
- Source: `u262.json`, row `C3_last_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_uncredited_tombstone.py`, `tests/test_tombstones.py`
- Collected: 681 against a baseline of 681
- Kills: 32 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[spotify-Sun Path (Live) (feat. Mira)-provider0-spelled_addresses0-provider_addresses0]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[spotify-Sun Path (feat. Mira) (Extended) (Remastered)-provider2-spelled_addresses2-provider_addresses2]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[spotify-Sun Path [Live] (feat. Mira)-provider1-spelled_addresses1-provider_addresses1]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[text-Sun Path (Live) (feat. Mira)-provider0-spelled_addresses0-provider_addresses0]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[text-Sun Path (feat. Mira) (Extended) (Remastered)-provider2-spelled_addresses2-provider_addresses2]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[text-Sun Path [Live] (feat. Mira)-provider1-spelled_addresses1-provider_addresses1]`
  - `tests/test_match_states.py::test_a_credited_listing_reaches_the_other_bracket_shape_of_its_own_version[round-listed]`
  - `tests/test_match_states.py::test_a_credited_rows_suppression_spellings_are_unchanged[Sun Path (Nightwave Remix) (ft Mira)-addresses1]`
  - `tests/test_match_states.py::test_a_credited_rows_suppression_spellings_are_unchanged[Sun Path (feat. Mira) (Nightwave Remix)-addresses0]`
  - `tests/test_match_states.py::test_a_credited_rows_suppression_spellings_are_unchanged[Sun Path (with Mira)-addresses2]`
  - `tests/test_match_states.py::test_a_featured_credit_is_a_performer_and_never_a_version`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[Featuring Anna]`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[feat. Anna]`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[ft Anna]`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[with Anna]`
  - ... and 17 more, see the JSON sidecar

Old text:

```
    return bool(words) and words[0] in _CREDIT_MARKERS
```

New text:

```
    return bool(words) and words[-1] in _CREDIT_MARKERS
```

### `u262.C4_unfolded_words`

_is_a_credit: split the raw group on spaces without folding, so feat. and Featuring are not markers

- File: `src/cratekit/acquire/match.py`
- Source: `u262.json`, row `C4_unfolded_words`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_uncredited_tombstone.py`, `tests/test_tombstones.py`
- Collected: 681 against a baseline of 681
- Kills: 26 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[spotify-Sun Path (Live) (feat. Mira)-provider0-spelled_addresses0-provider_addresses0]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[spotify-Sun Path (feat. Mira) (Extended) (Remastered)-provider2-spelled_addresses2-provider_addresses2]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[spotify-Sun Path [Live] (feat. Mira)-provider1-spelled_addresses1-provider_addresses1]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[text-Sun Path (Live) (feat. Mira)-provider0-spelled_addresses0-provider_addresses0]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[text-Sun Path (feat. Mira) (Extended) (Remastered)-provider2-spelled_addresses2-provider_addresses2]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[text-Sun Path [Live] (feat. Mira)-provider1-spelled_addresses1-provider_addresses1]`
  - `tests/test_match_states.py::test_a_credited_listing_reaches_the_other_bracket_shape_of_its_own_version[round-listed]`
  - `tests/test_match_states.py::test_a_credited_rows_suppression_spellings_are_unchanged[Sun Path (feat. Mira) (Nightwave Remix)-addresses0]`
  - `tests/test_match_states.py::test_a_featured_credit_is_a_performer_and_never_a_version`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[Featuring Anna]`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[feat. Anna]`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_the_abbreviation_ft_stays_a_credit`
  - `tests/test_match_states.py::test_a_held_file_crediting_somebody_else_never_calls_the_companion_stale`
  - `tests/test_match_states.py::test_a_listing_that_spelled_a_credit_never_asks_for_a_companion[Sun Path (Nightwave Remix) (feat. Zed)]`
  - `tests/test_match_states.py::test_a_listing_that_spelled_a_credit_never_asks_for_a_companion[Sun Path (feat. Zed) (Nightwave Remix)]`
  - ... and 11 more, see the JSON sidecar

Old text:

```
    words = fold(inside).split()
    return bool(words) and words[0] in _CREDIT_MARKERS
```

New text:

```
    words = str(inside).split()
    return bool(words) and words[0] in _CREDIT_MARKERS
```

### `u262.C5_no_with`

_CREDIT_MARKERS: drop with, so (with Anna) becomes a version

- File: `src/cratekit/acquire/match.py`
- Source: `u262.json`, row `C5_no_with`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_uncredited_tombstone.py`, `tests/test_tombstones.py`
- Collected: 681 against a baseline of 681
- Kills: 7 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_rows_suppression_spellings_are_unchanged[Sun Path (with Mira)-addresses2]`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[with Anna]`
  - `tests/test_match_states.py::test_a_listing_that_spelled_a_credit_never_asks_for_a_companion[Sun Path (with Zed) - Nightwave Remix]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[With You]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[With]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[with Anna]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_share_one_credit_vocabulary`

Old text:

```
_CREDIT_MARKERS: frozenset[str] = frozenset({"feat", "ft", "featuring", "with"})
```

New text:

```
_CREDIT_MARKERS: frozenset[str] = frozenset({"feat", "ft", "featuring"})
```

### `u262.C6_no_ft`

_CREDIT_MARKERS: drop ft, so (ft Anna) becomes a version

- File: `src/cratekit/acquire/match.py`
- Source: `u262.json`, row `C6_no_ft`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_uncredited_tombstone.py`, `tests/test_tombstones.py`
- Collected: 681 against a baseline of 681
- Kills: 9 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_rows_suppression_spellings_are_unchanged[Sun Path (Nightwave Remix) (ft Mira)-addresses1]`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[ft Anna]`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_the_abbreviation_ft_stays_a_credit`
  - `tests/test_match_states.py::test_a_listing_that_spelled_a_credit_never_asks_for_a_companion[Sun Path [ft. Zed] [Nightwave Remix]]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[FT. Anna]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[Ft Worth Edit]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[ft Anna]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[ft.anna]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_share_one_credit_vocabulary`

Old text:

```
_CREDIT_MARKERS: frozenset[str] = frozenset({"feat", "ft", "featuring", "with"})
```

New text:

```
_CREDIT_MARKERS: frozenset[str] = frozenset({"feat", "featuring", "with"})
```

### `u262.C7_no_featuring`

_CREDIT_MARKERS: drop featuring, so (Featuring Anna) becomes a version

- File: `src/cratekit/acquire/match.py`
- Source: `u262.json`, row `C7_no_featuring`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_uncredited_tombstone.py`, `tests/test_tombstones.py`
- Collected: 681 against a baseline of 681
- Kills: 4 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[Featuring Anna]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[Featuring Anna]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[featuring]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_share_one_credit_vocabulary`

Old text:

```
_CREDIT_MARKERS: frozenset[str] = frozenset({"feat", "ft", "featuring", "with"})
```

New text:

```
_CREDIT_MARKERS: frozenset[str] = frozenset({"feat", "ft", "with"})
```

### `u262.C8_no_feat`

_CREDIT_MARKERS: drop feat, so (feat. Anna) becomes a version

- File: `src/cratekit/acquire/match.py`
- Source: `u262.json`, row `C8_no_feat`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_uncredited_tombstone.py`, `tests/test_tombstones.py`
- Collected: 681 against a baseline of 681
- Kills: 19 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[spotify-Sun Path (Live) (feat. Mira)-provider0-spelled_addresses0-provider_addresses0]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[spotify-Sun Path (feat. Mira) (Extended) (Remastered)-provider2-spelled_addresses2-provider_addresses2]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[spotify-Sun Path [Live] (feat. Mira)-provider1-spelled_addresses1-provider_addresses1]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[text-Sun Path (Live) (feat. Mira)-provider0-spelled_addresses0-provider_addresses0]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[text-Sun Path (feat. Mira) (Extended) (Remastered)-provider2-spelled_addresses2-provider_addresses2]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[text-Sun Path [Live] (feat. Mira)-provider1-spelled_addresses1-provider_addresses1]`
  - `tests/test_match_states.py::test_a_credited_listing_reaches_the_other_bracket_shape_of_its_own_version[round-listed]`
  - `tests/test_match_states.py::test_a_credited_rows_suppression_spellings_are_unchanged[Sun Path (feat. Mira) (Nightwave Remix)-addresses0]`
  - `tests/test_match_states.py::test_a_featured_credit_is_a_performer_and_never_a_version`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[feat. Anna]`
  - `tests/test_match_states.py::test_a_held_file_crediting_somebody_else_never_calls_the_companion_stale`
  - `tests/test_match_states.py::test_a_listing_that_spelled_a_credit_never_asks_for_a_companion[Sun Path (Nightwave Remix) (feat. Zed)]`
  - `tests/test_match_states.py::test_a_listing_that_spelled_a_credit_never_asks_for_a_companion[Sun Path (feat. Zed) (Nightwave Remix)]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[Premade Sandwiches] (feat. Mira)-expected4]`
  - `tests/test_match_states.py::test_the_companion_reaches_exactly_what_ownership_reached`
  - ... and 4 more, see the JSON sidecar

Old text:

```
_CREDIT_MARKERS: frozenset[str] = frozenset({"feat", "ft", "featuring", "with"})
```

New text:

```
_CREDIT_MARKERS: frozenset[str] = frozenset({"ft", "featuring", "with"})
```

### `a32.V4_policy_unrestricted`

The probe policy builder admits a column outside the probe set

- File: `src/cratekit/core/rb_writer.py`
- Source: `a32.json`, row `V4_policy_unrestricted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_the_probe_policy_names_exactly_the_columns_asked_and_refuses_any_other`

Old text:

```
    outside = wanted - set(ROW_PROBE_COLUMNS)
    if outside:
```

New text:

```
    outside = wanted - set(ROW_PROBE_COLUMNS)
    if False:
```

### `a32.A2_stale_deleted`

A row deleted since the plan is still written

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `A2_stale_deleted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_row_deleted_since_the_plan_refuses_stale_and_writes_nothing`

Old text:

```
        if row is None or row[rb_writer.SOFT_DELETE_COLUMN] != 0:
```

New text:

```
        if row is None:
```

### `a32.A3_stale_value`

A row whose column moved since the plan is still written

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `A3_stale_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_column_changed_since_the_plan_refuses_stale_and_writes_nothing`

Old text:

```
        elif _text(row.get(probe.column)) != probe.was:
```

New text:

```
        elif False:
```

### `a32.A5_policy_widened`

The commit's policy admits both probe columns whatever the plan writes

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `A5_policy_widened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_plan_writing_one_column_admits_only_that_one_to_the_guard`

Old text:

```
    policy = rb_writer.row_probe_policy(p.column for p in plan.writing)
```

New text:

```
    policy = rb_writer.row_probe_policy(rb_writer.ROW_PROBE_COLUMNS)
```

### `a32.D1_digest_drops_replaced`

Drop the replaced value from the item, so the digest does not move when it changes

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `D1_digest_drops_replaced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_link.py::test_the_digest_moves_with_the_rows_the_columns_and_both_values`
  - `tests/test_repair_link.py::test_the_plan_is_each_triple_its_values_and_who_else_carries_each`

Old text:

```
            "from": self.was,
```

New text:

```
            "from": "",
```

### `a32.D2_digest_unordered`

Keep the triples in the order given, so the same plan digests two ways

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `D2_digest_unordered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_the_digest_is_equal_whatever_order_the_triples_are_given_in`

Old text:

```
    probes.sort(key=lambda p: (len(p.content_id), p.content_id, p.column))
```

New text:

```
(empty)
```

### `a32.J1_wrong_unjudged`

The judge never reports a value that did not take

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `J1_wrong_unjudged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_judge_names_a_value_that_did_not_take_and_a_column_that_moved`

Old text:

```
            if now.get(probe.column) is None or _text(now[probe.column]) != str(probe.value):
```

New text:

```
            if False:
```

### `a32.J2_planned_across_rows`

The judge excuses every column the plan writes on any row, not the row's own

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `J2_planned_across_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_judge_counts_a_column_written_on_another_row_as_moved_here`

Old text:

```
        changed = row_defaults.moved_columns(was, now, planned=plan.columns_on(content_id))
```

New text:

```
        changed = row_defaults.moved_columns(was, now, planned=[p.column for p in plan.writing])
```

### `a32.J4_moved_not_refused`

A moved column is reported as a wrong value rather than the guard's defect

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `J4_moved_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_column_moved_after_the_commit_refuses_through_the_verb`
  - `tests/test_repair_link.py::test_assert_read_back_refuses_a_moved_column_as_the_guards_defect`

Old text:

```
    if written.moved:
        raise refuse(
            "whitelist-violation",
```

New text:

```
    if False:
        raise refuse(
            "whitelist-violation",
```

### `a32.P1_tombstone_plans`

Drop the live row filter from the plan's row query, so a tombstone plans

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `P1_tombstone_plans`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_tombstone_refuses_as_unknown_though_the_row_is_in_the_table`

Old text:

```
                    f"WHERE ID = :id AND {rb_writer.SOFT_DELETE_COLUMN} = 0"
```

New text:

```
                    f"WHERE ID = :id"
```

### `a32.P2_unknown_row`

Drop the unknown row refusal, so an absent identifier falls through

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `P2_unknown_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 4 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_plan_refusal_reaches_no_gate`
  - `tests/test_repair_link.py::test_a_tombstone_refuses_as_unknown_though_the_row_is_in_the_table`
  - `tests/test_repair_link.py::test_an_unknown_identifier_refuses_by_name_before_any_gate`
  - `tests/test_repair_link.py::test_one_bad_triple_refuses_the_whole_plan`

Old text:

```
        if row is None:
            raise refuse(
                ROW_UNKNOWN,
```

New text:

```
        if row is None and False:
            raise refuse(
                ROW_UNKNOWN,
```

### `a32.P3_unheld_value`

Drop the unheld value refusal, so a value nobody carries is written

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `P3_unheld_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_value_no_other_live_row_carries_refuses`
  - `tests/test_repair_link.py::test_a_value_only_a_tombstone_carries_refuses_as_unheld`

Old text:

```
        if probe.writes and carriers == 0:
```

New text:

```
        if probe.writes and carriers < 0:
```

### `a32.P4_count_tombstones`

Count tombstones as carriers and fellows of a value

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `P4_count_tombstones`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 5 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_null_counts_its_fellows_as_null_so_writing_one_back_is_the_minority`
  - `tests/test_repair_link.py::test_a_value_only_a_tombstone_carries_refuses_as_unheld`
  - `tests/test_repair_link.py::test_the_bindings_value_onto_a_row_rekordbox_made_refuses_as_the_minority`
  - `tests/test_repair_link.py::test_the_plan_is_each_triple_its_values_and_who_else_carries_each`
  - `tests/test_repair_link.py::test_the_two_acts_write_each_triple_and_move_no_other_column`

Old text:

```
            f"AND {rb_writer.SOFT_DELETE_COLUMN} = 0 AND ID != :id"
```

New text:

```
            f"AND ID != :id"
```

### `a32.P6_writes_always`

Every triple writes, a row already at the value included

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `P6_writes_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 6 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_plan_where_every_row_is_already_at_its_value_still_asks_and_writes_nothing`
  - `tests/test_repair_link.py::test_a_row_already_at_a_value_nobody_else_carries_still_plans_nothing`
  - `tests/test_repair_link.py::test_a_row_already_at_the_value_plans_nothing_for_that_triple`
  - `tests/test_repair_link.py::test_a_triple_already_at_its_value_is_shown_and_not_written`
  - `tests/test_repair_link.py::test_apply_refuses_a_plan_that_writes_nothing_as_a_defect`
  - `tests/test_repair_link.py::test_judge_skips_a_triple_that_writes_nothing`

Old text:

```
        return self.was != str(self.value)
```

New text:

```
        return True
```

### `a32.P7_minority_boundary`

Move the majority rule's boundary, so a value carried by as many rows as the row's own is written

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `P7_minority_boundary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_value_carried_by_as_many_rows_as_the_rows_own_refuses_too`

Old text:

```
        if probe.writes and carriers <= fellows:
```

New text:

```
        if probe.writes and carriers < fellows:
```

### `a32.P8_null_fellows`

Count a NULL's fellows with an equality, which matches nothing, so a NULL has no fellows

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `P8_null_fellows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_the_plan_is_each_triple_its_values_and_who_else_carries_each`

Old text:

```
    test = f"{column} IS NULL" if value is None else f"{column} = :value"
```

New text:

```
    test = f"{column} = :value"
```

### `a32.V1_any_column`

A triple naming a column outside the probe set is parsed, AnalysisUpdated included

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `V1_any_column`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 4 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_malformed_triple_or_a_column_outside_the_probe_refuses_by_name[101:AnalysisUpdated=2]`
  - `tests/test_repair_link.py::test_a_malformed_triple_or_a_column_outside_the_probe_refuses_by_name[101:BPM=12800]`
  - `tests/test_repair_link.py::test_a_malformed_triple_or_a_column_outside_the_probe_refuses_by_name[101:Title=x]`
  - `tests/test_repair_link.py::test_a_malformed_triple_refuses_through_the_verb_before_any_gate`

Old text:

```
    if kind is None:
        raise _invalid(
```

New text:

```
    if False:
        raise _invalid(
```

### `a32.V2_link_not_converted`

A ContentLink value is kept as text rather than converted to a whole number

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `V2_link_not_converted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 4 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_malformed_triple_or_a_column_outside_the_probe_refuses_by_name[101:ContentLink=]`
  - `tests/test_repair_link.py::test_a_malformed_triple_or_a_column_outside_the_probe_refuses_by_name[101:ContentLink=lots]`
  - `tests/test_repair_link.py::test_a_triple_reads_row_column_and_a_value_of_the_columns_type`
  - `tests/test_repair_link.py::test_the_plan_is_each_triple_its_values_and_who_else_carries_each`

Old text:

```
    if kind is int:
```

New text:

```
    if False:
```

### `a32.C1_ack_after_gate`

The backup acknowledgment is not read before the gate

- File: `src/cratekit/write/row_link_cli.py`
- Source: `a32.json`, row `C1_ack_after_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    session.assert_backup_acknowledged(cfg)

    plan = _plan(cfg, ctx.args)
```

New text:

```
    plan = _plan(cfg, ctx.args)
```

### `a32.C2_abort_writes`

An abort at the gate proceeds to the write

- File: `src/cratekit/write/row_link_cli.py`
- Source: `a32.json`, row `C2_abort_writes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_an_abort_writes_nothing`

Old text:

```
    if ctx.gate.require(spec, plan=data, context=_facts(plan)) != "apply":
```

New text:

```
    if ctx.gate.require(spec, plan=data, context=_facts(plan)) not in ("apply", "abort"):
```

### `a32.C3_nothing_to_write_applies`

A plan that writes nothing reaches the apply

- File: `src/cratekit/write/row_link_cli.py`
- Source: `a32.json`, row `C3_nothing_to_write_applies`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_plan_where_every_row_is_already_at_its_value_still_asks_and_writes_nothing`

Old text:

```
    if not plan.writes:
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=[_nothing(plan)])
```

New text:

```
    if False:
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=[_nothing(plan)])
```

### `a32.C4_read_back_unasserted`

The verb answers OK without asserting the read back

- File: `src/cratekit/write/row_link_cli.py`
- Source: `a32.json`, row `C4_read_back_unasserted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_column_moved_after_the_commit_refuses_through_the_verb`

Old text:

```
    row_link.assert_read_back(written)
    data["totals"] = {
```

New text:

```
    data["totals"] = {
```

### `r705-b.S2_client_session_never_attaches`

the catalogue and account client's transport is not gated, so nothing it does is paced or counted

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r705-b.json`, row `S2_client_session_never_attaches`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 117 against a baseline of 117
- Kills: 16 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_ceiling_stop_a_verb_swallowed_is_still_said`
  - `tests/test_provider_gate.py::test_a_rate_limited_login_comes_out_of_client_session_as_the_park`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls`
  - `tests/test_provider_gate.py::test_a_verb_at_its_ceiling_is_blocked_and_names_the_exact_command_that_continues`
  - `tests/test_provider_gate.py::test_a_verb_at_the_hours_line_is_blocked_and_keeps_what_it_did`
  - `tests/test_provider_gate.py::test_calls_another_process_made_are_not_reported_as_this_runs`
  - `tests/test_provider_gate.py::test_calls_on_the_command_line_lets_one_run_pass_and_the_next_is_back_at_the_ceiling`
  - `tests/test_provider_gate.py::test_client_session_attaches_the_gate_before_the_login_goes_out`
  - `tests/test_provider_gate.py::test_client_session_with_no_gate_still_paces_at_the_defaults`
  - `tests/test_provider_gate.py::test_rate_limit_answers_are_named_in_the_spend_line`
  - `tests/test_provider_gate.py::test_the_account_opener_paces_with_the_frozen_configuration`
  - `tests/test_provider_gate.py::test_the_catalogue_opener_paces_with_the_frozen_configuration`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_calls_already_given`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_spaced_calls_already_given`
  - `tests/test_provider_gate.py::test_the_spend_line_reaches_a_person_on_the_human_output`
  - ... and 1 more, see the JSON sidecar

Old text:

```
        client = CLIENT_FACTORY()
        gate.attach(client)

```

New text:

```
        client = CLIENT_FACTORY()

```

### `r705-b.S9_playlist_read_wraps_the_park`

the playlist read wraps the park into an unresolvable playlist again

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r705-b.json`, row `S9_playlist_read_wraps_the_park`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 117 against a baseline of 117
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_the_playlist_read_lets_the_park_through`

Old text:

```
            playlist = self._session.playlist(identifier)
        except CratekitError:

```

New text:

```
            playlist = self._session.playlist(identifier)
        except ValueError:

```

### `r705-b.S10_infinite_interval_accepted`

an infinite interval passes validation and reaches time.sleep

- File: `src/cratekit/core/config.py`
- Source: `r705-b.json`, row `S10_infinite_interval_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 117 against a baseline of 117
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_non_positive_interval_is_refused_naming_the_key[inf]`
  - `tests/test_provider_gate.py::test_a_non_positive_interval_is_refused_naming_the_key[nan]`

Old text:

```
        or not math.isfinite(interval)
        or interval <= 0

```

New text:

```
        or interval <= 0

```

### `r705-b.S7_acquire_one_softens_the_park_at_the_lookup`

a park raised at the offer is one unavailable track and the driver claims the next

- File: `src/cratekit/acquire/adapter.py`
- Source: `r705-b.json`, row `S7_acquire_one_softens_the_park_at_the_lookup`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 117 against a baseline of 117
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_acquire_one_lets_the_park_through_rather_than_failing_the_track[offer]`

Old text:

```
        offer = source.offer(request)
    except (AdapterAuthFailed, AdapterBroken, Parked):

```

New text:

```
        offer = source.offer(request)
    except (AdapterAuthFailed, AdapterBroken):

```

### `r705-b.S8_acquire_one_softens_the_park_at_the_fetch`

a park raised at the fetch is one unavailable track and the driver claims the next

- File: `src/cratekit/acquire/adapter.py`
- Source: `r705-b.json`, row `S8_acquire_one_softens_the_park_at_the_fetch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 117 against a baseline of 117
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_acquire_one_lets_the_park_through_rather_than_failing_the_track[fetch]`

Old text:

```
        path = source.fetch(request, settings.download_staging)
    except (AdapterAuthFailed, AdapterBroken, Parked):

```

New text:

```
        path = source.fetch(request, settings.download_staging)
    except (AdapterAuthFailed, AdapterBroken):

```

### `r705-a.G10_long_wait_under_the_lock`

a Retry-After wait is slept holding the lock, so a second driver waits on the holder

- File: `src/cratekit/core/provider_gate.py`
- Source: `r705-a.json`, row `G10_long_wait_under_the_lock`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 117 against a baseline of 117
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_wait_the_provider_asked_for_is_taken_with_the_lock_released`

Old text:

```
                if due - now > self.settings.min_interval_s:

```

New text:

```
                if False:

```

### `r705-a.G11_lock_limit_without_the_interval`

the lock wait limit drops the one interval a holder may sleep under it

- File: `src/cratekit/core/provider_gate.py`
- Source: `r705-a.json`, row `G11_lock_limit_without_the_interval`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 117 against a baseline of 117
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_lock_held_past_the_wait_is_refused_with_the_holder_named`

Old text:

```
                limit = LOCK_WAIT_S + self.settings.min_interval_s

```

New text:

```
                limit = LOCK_WAIT_S

```

### `r705-a.G12_park_forgotten`

a park the tool swallowed is not remembered, so the vendored adapter reads it as no file

- File: `src/cratekit/core/provider_gate.py`
- Source: `r705-a.json`, row `G12_park_forgotten`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 117 against a baseline of 117
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_held_lock_the_tool_swallowed_during_a_download_comes_out_of_fetch`
  - `tests/test_provider_gate.py::test_the_stop_is_remembered_so_a_swallowing_tool_still_parks`

Old text:

```
        if self._last_park is not None:
            raise self._last_park

```

New text:

```
        if False:
            raise self._last_park

```

### `r705-a.G13_process_calls_not_counted`

this process's call counter never moves, so the spend line reports nothing

- File: `src/cratekit/core/provider_gate.py`
- Source: `r705-a.json`, row `G13_process_calls_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 117 against a baseline of 117
- Kills: 19 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_ceiling_stop_a_verb_swallowed_is_still_said`
  - `tests/test_provider_gate.py::test_a_command_is_charged_only_for_its_own_calls`
  - `tests/test_provider_gate.py::test_a_command_stops_before_the_call_past_its_ceiling_with_the_count_at_the_ceiling`
  - `tests/test_provider_gate.py::test_a_nested_dispatch_keeps_the_outer_commands_count`
  - `tests/test_provider_gate.py::test_a_raised_ceiling_lasts_one_run_and_the_next_is_back_at_the_configured_one`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls`
  - `tests/test_provider_gate.py::test_a_separate_session_such_as_the_media_segment_fetch_is_not_counted`
  - `tests/test_provider_gate.py::test_a_verb_at_its_ceiling_is_blocked_and_names_the_exact_command_that_continues`
  - `tests/test_provider_gate.py::test_calls_another_process_made_are_not_reported_as_this_runs`
  - `tests/test_provider_gate.py::test_calls_on_the_command_line_lets_one_run_pass_and_the_next_is_back_at_the_ceiling`
  - `tests/test_provider_gate.py::test_process_spend_is_this_process_alone`
  - `tests/test_provider_gate.py::test_rate_limit_answers_are_named_in_the_spend_line`
  - `tests/test_provider_gate.py::test_the_ceiling_never_says_kept_over_work_a_continue_does_again`
  - `tests/test_provider_gate.py::test_the_ceiling_parks_a_job_and_the_resumed_job_continues`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_calls_already_given`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        _PROCESS_CALLS += 1

```

New text:

```
        _PROCESS_CALLS += 0

```

### `r705-a.G1_interval_halved`

the shared interval is halved, so consecutive calls wait half of what the configuration says

- File: `src/cratekit/core/provider_gate.py`
- Source: `r705-a.json`, row `G1_interval_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 117 against a baseline of 117
- Kills: 9 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_retry_after_shorter_than_the_interval_does_not_shorten_it`
  - `tests/test_provider_gate.py::test_a_wait_the_provider_asked_for_is_taken_with_the_lock_released`
  - `tests/test_provider_gate.py::test_an_unreadable_retry_after_is_zero_rather_than_a_guess`
  - `tests/test_provider_gate.py::test_attach_routes_every_request_of_a_real_session_through_the_gate_once`
  - `tests/test_provider_gate.py::test_consecutive_calls_wait_out_the_interval`
  - `tests/test_provider_gate.py::test_the_interval_is_measured_from_the_last_call_by_any_gate`
  - `tests/test_provider_gate.py::test_the_interval_is_the_configured_one`
  - `tests/test_provider_gate.py::test_the_vendored_adapter_attaches_the_gate_to_an_injected_session`
  - `tests/test_provider_gate.py::test_two_processes_keep_the_interval_between_every_call`

Old text:

```
                due = max(state.last_call + self.settings.min_interval_s, state.not_before)

```

New text:

```
                due = max(state.last_call + self.settings.min_interval_s / 2, state.not_before)

```

### `r705-a.G2_last_call_ignored`

the interval is measured from now rather than from the last call any process made, so a second gate never waits on the first

- File: `src/cratekit/core/provider_gate.py`
- Source: `r705-a.json`, row `G2_last_call_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 117 against a baseline of 117
- Kills: 9 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_retry_after_shorter_than_the_interval_does_not_shorten_it`
  - `tests/test_provider_gate.py::test_a_wait_the_provider_asked_for_is_taken_with_the_lock_released`
  - `tests/test_provider_gate.py::test_an_unreadable_retry_after_is_zero_rather_than_a_guess`
  - `tests/test_provider_gate.py::test_attach_routes_every_request_of_a_real_session_through_the_gate_once`
  - `tests/test_provider_gate.py::test_consecutive_calls_wait_out_the_interval`
  - `tests/test_provider_gate.py::test_the_interval_is_measured_from_the_last_call_by_any_gate`
  - `tests/test_provider_gate.py::test_the_interval_is_the_configured_one`
  - `tests/test_provider_gate.py::test_the_vendored_adapter_attaches_the_gate_to_an_injected_session`
  - `tests/test_provider_gate.py::test_two_processes_keep_the_interval_between_every_call`

Old text:

```
                due = max(state.last_call + self.settings.min_interval_s, state.not_before)

```

New text:

```
                due = max(now, state.not_before)

```

### `r705-a.G3_retry_after_ignored`

a Retry-After the provider sends no longer holds the next call

- File: `src/cratekit/core/provider_gate.py`
- Source: `r705-a.json`, row `G3_retry_after_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 117 against a baseline of 117
- Kills: 3 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_retry_after_as_an_http_date_is_honoured`
  - `tests/test_provider_gate.py::test_a_retry_after_in_seconds_holds_the_next_call_at_least_that_long`
  - `tests/test_provider_gate.py::test_a_wait_the_provider_asked_for_is_taken_with_the_lock_released`

Old text:

```
                state.not_before = max(state.not_before, now + retry_after)

```

New text:

```
                state.not_before = state.not_before

```

