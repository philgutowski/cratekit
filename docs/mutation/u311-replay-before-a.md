# Mutation table: u311-replay-before-a

Measured by `scripts/mutate.py` on 2026-11-22 22:37 UTC, branch `HEAD` at `48a0103d`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 131.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py baseline` at 2026-11-22 22:37 UTC for commit `48a0103d4f0a`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 10, each measured by this driver.

Known failures: 149 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r221-a.S3_flag_reads_a_key_nothing_freezes` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 8 | killed |
| `r221-a.W1_rehearsal_never_said` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 3 | killed |
| `r221-a.W2_rehearsal_said_unconditionally` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 3 | killed |
| `r221-a.W3_queue_branch_warning_dropped` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r221-a.W4_twin_branch_warning_dropped` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r221-a.W6_twin_branch_says_it_unconditionally` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r221-b.M1_refusal_step_dropped` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 5 | killed |
| `r221-b.M2_refusal_step_unconditional` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 5 | killed |
| `r221-b.M4_steps_replaced_not_joined` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `r221-b.R1_refusal_is_its_own_cause` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r222-b.B10_archive_not_compared` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r222-b.B11_finished_jobs_are_twins` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 3 | killed |
| `r222-b.B12_warnings_from_the_live_configuration` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r222-b.B14_destination_claimed_unread` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r222-b.B1_always_enqueue` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 9 | killed |
| `r222-b.B2_any_verb_is_a_twin` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r222-b.B3_any_library_is_a_twin` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r222-b.B4_rehearsal_is_a_twin` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 3 | killed |
| `r222-b.B5_whole_payload_compared` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 10 | killed |
| `r222-b.B6_itemless_job_is_a_twin` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r222-b.B7_unreadable_is_elsewhere` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r222-b.B8_every_exception_is_unreadable` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r222-b.B9_mirror_not_compared` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r349-a.A1_failure_write` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 3 | killed |
| `r349-a.A2_success_produced` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 6 | killed |
| `r349-a.A4_envelope_field` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r349-b.B3_clear_before_attempt` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r349-b.B4_stage_error_completes` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r349-c.C2_write_failure_step` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r390-a.A6_backup_transfer_exit_is_permanent` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 5 | killed |
| `u45-round-1.A1_unreadable_reported_as_absent` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 5 | killed |
| `u45-round-1.A4_state_collapsed_to_known` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 2 | killed |
| `u45-round-1.C2_refusal_read_as_failure` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 6 | killed |
| `u45-round-1.C3_nothing_ran_accepted` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 6 | killed |
| `u45-round-1.C4_uniform_refusal_flattened` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 3 | killed |
| `u45-round-1.C5_first_refusal_taken` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `u45-round-1.C6_partial_run_refused` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 3 | killed |
| `u45-round-1.Q1_resume_drops_the_rehearsal` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 2 | killed |
| `u45-round-1.Q2_resume_always_rehearses` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `u45-round-1.Q3_resume_loses_the_job` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 2 | killed |
| `u45-round-1.Q4_payload_key_not_read` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 2 | killed |
| `u45-round-1.R1_reserved_remediation_discarded` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 4 | killed |
| `u45-round-1.R2_slug_flattened` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 2 | killed |
| `u45-round-1.W2_report_from_the_plan` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 11 | killed |
| `u45-round-1.W3_ages_not_read_back` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 5 | killed |
| `u45-round-1.W4_ages_derived_from_the_outcome` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 3 | killed |
| `u45-round-1.W5_publishing_switched_off` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 9 | killed |
| `u45-round-1.W6_rehearsal_becomes_a_real_run` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 6 | killed |
| `u45-round-1.W8_engine_refusal_escapes` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `u45-round-2.A3_age_seconds_always_none` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `u45-round-2.C7_failed_detail_dropped` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `u50-author.B1_no_items_enqueued` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 39 | killed |
| `u50-author.B3_items_one_portion_only` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 17 | killed |
| `u50-author.W1_no_narrowing` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u50-author.W5_unknown_portion_unchecked` | `src/cratekit/backup/cli.py` | maintainer | 1 file(s) | 99 | 1 | killed |
| `u50-author.W6_fresh_config_in_the_handler` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 29 | killed |
| `u50-review-fixes.R2_empty_job_guard_dropped` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `u50-zero-rows.B2_items_hardcoded_pair` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `u50-zero-rows.W4b_item_ignored_entirely` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 16 | killed |
| `r154-a.A1_stamp_pattern` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 209 | 1 | killed |
| `r154-a.A2_stamp_calendar` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 209 | 1 | killed |
| `r154-a.A4_legacy_spelling` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 209 | 1 | killed |
| `r154-a.A5_listing_filter` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 209 | 1 | killed |
| `r154-a.A7_read_normalization` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 209 | 1 | killed |
| `r154-a.A8_empty_expected` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 209 | 2 | killed |
| `r154-b.B2_two_markers` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 209 | 2 | killed |
| `r154-b.B3_handed_down_stamp` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 209 | 1 | killed |
| `r154-b.B4_stated_volume_over_unmarked` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 209 | 1 | killed |
| `r154-b.B5_veto_not_select` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 209 | 3 | killed |
| `r154-b.B6_walk_bound` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 209 | 1 | killed |
| `r154-b.B8_walk_match` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 209 | 3 | killed |
| `r222-a.A10_plan_text_at_keep_zero` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 209 | 1 | killed |
| `r367.E3_a_live_rekordbox_is_ignored` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 209 | 1 | killed |
| `r367.G8_files_only_is_dropped` | `src/cratekit/modules/tools/backup.py` | maintainer | 1 file(s) | 209 | 1 | killed |
| `u279.M12_holder_never_found` | `src/cratekit/modules/tools/setbuilder.py` | user | 4 file(s) | 366 | 2 | killed |
| `u279.M1_walk_ignores_exclude` | `src/cratekit/modules/tools/setbuilder.py` | user | 4 file(s) | 366 | 10 | killed |
| `u279.M2_excluded_folder_walked` | `src/cratekit/modules/tools/setbuilder.py` | user | 4 file(s) | 366 | 10 | killed |
| `u279.M3_ancestor_taken_whole` | `src/cratekit/modules/tools/setbuilder.py` | user | 4 file(s) | 366 | 1 | killed |
| `u279.M4_symlink_followed` | `src/cratekit/modules/tools/setbuilder.py` | user | 4 file(s) | 366 | 1 | killed |
| `u279.M5_unlistable_raises` | `src/cratekit/modules/tools/setbuilder.py` | user | 4 file(s) | 366 | 1 | killed |
| `u279.M6_chain_unresolved` | `src/cratekit/modules/tools/setbuilder.py` | user | 4 file(s) | 366 | 1 | killed |
| `u279.M7_outermost_folder_excluded` | `src/cratekit/modules/tools/setbuilder.py` | user | 4 file(s) | 366 | 1 | killed |
| `u279.M10_tilde_not_expanded` | `src/cratekit/setbuilder/cli.py` | user | 4 file(s) | 366 | 1 | killed |
| `u279.M11_excluded_anchor_not_refused` | `src/cratekit/setbuilder/cli.py` | user | 4 file(s) | 366 | 2 | killed |
| `u279.M13_wrong_folder_named` | `src/cratekit/setbuilder/cli.py` | user | 4 file(s) | 366 | 1 | killed |
| `u279.M8_index_call_unexcluded` | `src/cratekit/setbuilder/cli.py` | user | 4 file(s) | 366 | 6 | killed |
| `u279.M9_staging_not_excluded` | `src/cratekit/setbuilder/cli.py` | user | 4 file(s) | 366 | 4 | killed |
| `r154-a.A3_named_shape_check` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 307 | 9 | killed |
| `r154-b.B1_named_mismatch` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 307 | 9 | killed |
| `r154-b.B7_walk_order` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 307 | 6 | killed |
| `r367.E1_a_failed_transfer_is_unread` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 307 | 42 | killed |
| `r367.E2_an_unconfirmed_restore_is_allowed` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 307 | 1 | killed |
| `r367.G12_listing_results_are_discarded` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 307 | 12 | killed |
| `r367.G1_always_copy_the_restored_sidecar` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 307 | 10 | killed |
| `r367.G3_membership_is_inverted` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 307 | 18 | killed |
| `r367.G4_the_inventory_restored_flag_is_ignored` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 307 | 6 | killed |
| `r367.G5_absent_sidecars_are_not_recorded` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 307 | 3 | killed |
| `r367.G7_the_listing_is_of_the_snapshot_root` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 307 | 1 | killed |
| `u138.S7_verb_drops_the_answer` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 7 | killed |
| `u184.A10_summary_always_recorded` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `u184.A11_wording_swapped` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 2 | killed |
| `u184.A3_engine_rule_not_selected` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 9 | killed |
| `u184.A4_valid_record_minted_again` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 2 | killed |
| `u184.A5_expired_reported_valid` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `u184.A6_unreadable_record_refuses` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `u184.A7_already_valid_says_ok` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `u184.A8_expiry_row_dropped` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `u184.A9_expiry_row_names_the_mint` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `u266.M1_seven_opens_again` | `src/cratekit/modules/tools/setbuilder.py` | user | 3 file(s) | 351 | 52 | killed |
| `u266.M2_strict_reader` | `src/cratekit/modules/tools/setbuilder.py` | user | 3 file(s) | 351 | 6 | killed |
| `u266.M3_a_field_dropped` | `src/cratekit/modules/tools/setbuilder.py` | user | 3 file(s) | 351 | 55 | killed |
| `u266.M4_key_order_reversed` | `src/cratekit/modules/tools/setbuilder.py` | maintainer | 3 file(s) | 351 | 48 | killed |
| `u266.M6_size_not_compared` | `src/cratekit/modules/tools/setbuilder.py` | user | 3 file(s) | 351 | 1 | killed |
| `r349-c.C1_prune_recorded` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 308 | 41 | killed |
| `r349-c.C4_argv_rendered` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 308 | 4 | killed |
| `u181.E2_direct_reference_drops_extras` | `src/cratekit/modules/extras.py` | user | 1 file(s) | 13 | 1 | killed |
| `u27-reports-round-2.S5b_engine_default_drift` | `src/cratekit/modules/reports/duplicates.py` | user | 2 file(s) | 382 | 3 | killed |
| `u48-author.P3_two_codes_collapsed_to_one` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 229 | 2 | killed |

## Zero rows and what they owe

- `r221-b.M4_steps_replaced_not_joined` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u50-author.W1_no_narrowing` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `r221-a.S3_flag_reads_a_key_nothing_freezes`

Read the rehearsal flag under a name the build does not freeze, so every job reads as a real backup

- File: `src/cratekit/backup/cli.py`
- Source: `r221-a.json`, row `S3_flag_reads_a_key_nothing_freezes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 8 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_half_failed_rehearsal_says_it_too_on_the_other_refusal`
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_a_refusal_this_verb_re_raises_is_never_its_own_cause`
  - `tests/test_backup_cli.py::test_a_rehearsal_that_ended_badly_still_says_it_was_a_rehearsal`
  - `tests/test_backup_cli.py::test_an_unreadable_fact_file_under_a_rehearsal_says_which_kind_of_run_it_was`
  - `tests/test_backup_cli.py::test_the_ages_a_rehearsal_reports_are_the_previous_real_runs_and_it_says_so`
  - `tests/test_backup_cli.py::test_the_rehearsal_is_said_at_queue_time_and_when_the_open_job_is_reported`

Old text:

```
    return bool((job.payload or {}).get(DRY_RUN))
```

New text:

```
    return bool((job.payload or {}).get("rehearsal"))
```

### `r221-a.W1_rehearsal_never_said`

The warning is never carried, which is the exact state the ledger entry describes

- File: `src/cratekit/backup/cli.py`
- Source: `r221-a.json`, row `W1_rehearsal_never_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 3 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_the_ages_a_rehearsal_reports_are_the_previous_real_runs_and_it_says_so`
  - `tests/test_backup_cli.py::test_the_rehearsal_is_said_at_queue_time_and_when_the_open_job_is_reported`

Old text:

```
    return (rehearsal_warning(),) if _is_rehearsal(job) else ()
```

New text:

```
    return ()
```

### `r221-a.W2_rehearsal_said_unconditionally`

Every run is told it copied nothing, including the real one that copied and published, which is the same defect pointing the other way

- File: `src/cratekit/backup/cli.py`
- Source: `r221-a.json`, row `W2_rehearsal_said_unconditionally`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 3 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_queued_real_backup_carries_no_rehearsal_word`
  - `tests/test_backup_cli.py::test_a_second_ask_for_a_real_backup_is_not_told_the_open_job_copies_nothing`
  - `tests/test_backup_cli.py::test_the_flag_on_the_envelope_is_the_jobs_own_and_not_the_command_lines`

Old text:

```
    return (rehearsal_warning(),) if _is_rehearsal(job) else ()
```

New text:

```
    return (rehearsal_warning(),)
```

### `r221-a.W3_queue_branch_warning_dropped`

The identifier is handed back with no word about what it will do, and the detached child a resume spawns writes to a log nobody is watching

- File: `src/cratekit/backup/cli.py`
- Source: `r221-a.json`, row `W3_queue_branch_warning_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_rehearsal_is_said_at_queue_time_and_when_the_open_job_is_reported`

Old text:

```
                *map(dict, backup.snapshot_identity_warning(cfg)),
                *_rehearsal(job),
            ),
        )
```

New text:

```
                *map(dict, backup.snapshot_identity_warning(cfg)),
            ),
        )
```

### `r221-a.W4_twin_branch_warning_dropped`

A second ask reports the open rehearsal as the backup the person asked for, with nothing saying it is one

- File: `src/cratekit/backup/cli.py`
- Source: `r221-a.json`, row `W4_twin_branch_warning_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_rehearsal_is_said_at_queue_time_and_when_the_open_job_is_reported`

Old text:

```
                    *_rehearsal(twin),
                ),
            )
```

New text:

```
                ),
            )
```

### `r221-a.W6_twin_branch_says_it_unconditionally`

The reported twin always carries the word, so a person asking twice for a REAL backup is told the open job copies nothing. Removing the helper's own guard is W2; this is the branch's own reading of the job it hands back

- File: `src/cratekit/backup/cli.py`
- Source: `r221-a.json`, row `W6_twin_branch_says_it_unconditionally`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_second_ask_for_a_real_backup_is_not_told_the_open_job_copies_nothing`

Old text:

```
                    *_rehearsal(twin),
```

New text:

```
                    rehearsal_warning(),
```

### `r221-b.M1_refusal_step_dropped`

No refusal carries the sentence, so a rehearsal that failed reads as a real backup attempt that fell over

- File: `src/cratekit/backup/cli.py`
- Source: `r221-b.json`, row `M1_refusal_step_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 5 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_half_failed_rehearsal_says_it_too_on_the_other_refusal`
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
  - `tests/test_backup_cli.py::test_a_refusal_this_verb_re_raises_is_never_its_own_cause`
  - `tests/test_backup_cli.py::test_a_rehearsal_that_ended_badly_still_says_it_was_a_rehearsal`
  - `tests/test_backup_cli.py::test_an_unreadable_fact_file_under_a_rehearsal_says_which_kind_of_run_it_was`

Old text:

```
    if not _is_rehearsal(job):
        return error
    cause = error.cause
```

New text:

```
    return error
    cause = error.cause
```

### `r221-b.M2_refusal_step_unconditional`

Every refusal gains the sentence, so a person whose REAL backup failed is told nothing was copied and stops looking for the half that was

- File: `src/cratekit/backup/cli.py`
- Source: `r221-b.json`, row `M2_refusal_step_unconditional`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 5 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_half_failed_rehearsal_says_it_too_on_the_other_refusal`
  - `tests/test_backup_cli.py::test_a_real_backup_that_ended_badly_gains_no_rehearsal_step`
  - `tests/test_backup_cli.py::test_a_refusal_this_verb_re_raises_is_never_its_own_cause`
  - `tests/test_backup_cli.py::test_a_rehearsal_that_ended_badly_still_says_it_was_a_rehearsal`
  - `tests/test_backup_cli.py::test_an_unreadable_fact_file_under_a_real_run_gains_no_rehearsal_step`

Old text:

```
    if not _is_rehearsal(job):
        return error
    cause = error.cause
```

New text:

```
    cause = error.cause
```

### `r221-b.M4_steps_replaced_not_joined`

The sentence replaces the failure's own steps rather than joining them, so the thing a person has to do to fix it is gone

- File: `src/cratekit/backup/cli.py`
- Source: `r221-b.json`, row `M4_steps_replaced_not_joined`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                steps=(*cause.remediation.steps, rehearsal_warning()["message"]),
```

New text:

```
                steps=(rehearsal_warning()["message"],),
```

### `r221-b.R1_refusal_is_its_own_cause`

Raise the result from the original unconditionally, which is `raise exc from exc` on a real run and truncates the chain cause.classified walks. This is the defect the code review found

- File: `src/cratekit/backup/cli.py`
- Source: `r221-b.json`, row `R1_refusal_is_its_own_cause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_refusal_this_verb_re_raises_is_never_its_own_cause`

Old text:

```
    extended = _with_rehearsal_step(error, job)
    if extended is error:
        raise error
    raise extended from error
```

New text:

```
    raise _with_rehearsal_step(error, job) from error
```

### `r222-b.B10_archive_not_compared`

Compare only the mirror, so two jobs rotating one archive root from different mirrors are strangers

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B10_archive_not_compared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_either_shared_destination_is_the_same_backup[archive_root]`

Old text:

```
            frozen.backup.dest == cfg.backup.dest
            or frozen.backup.archive_root == cfg.backup.archive_root
```

New text:

```
            frozen.backup.dest == cfg.backup.dest
```

### `r222-b.B11_finished_jobs_are_twins`

Read every state from the queue, so a backup that is over stands in for a new one for ever

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B11_finished_jobs_are_twins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 3 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_backup_that_is_over_does_not_stand_in_for_a_new_one[cancelled]`
  - `tests/test_backup_cli.py::test_a_backup_that_is_over_does_not_stand_in_for_a_new_one[failed]`
  - `tests/test_backup_cli.py::test_a_backup_that_is_over_does_not_stand_in_for_a_new_one[succeeded]`

Old text:

```
    for job in jobs.list_jobs(store, states=open_states):
```

New text:

```
    for job in jobs.list_jobs(store):
```

### `r222-b.B12_warnings_from_the_live_configuration`

Describe the reported job from the configuration on disk rather than the one it was frozen against

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B12_warnings_from_the_live_configuration`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_warnings_beside_a_reported_job_describe_that_job`

Old text:

```
            described = cfg if frozen is None else frozen
```

New text:

```
            described = cfg
```

### `r222-b.B14_destination_claimed_unread`

Reword the unreadable case to the ordinary sentence's opening, so the warning no longer says the configuration was not rebuilt

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B14_destination_claimed_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_an_open_backup_whose_destinations_cannot_be_read_is_not_read_as_elsewhere`

Old text:

```
        "its frozen configuration could not be rebuilt, so where it writes is "
```

New text:

```
        "its frozen configuration was not consulted, so where it writes is "
```

### `r222-b.B1_always_enqueue`

Never report a twin, which is the finding itself: every ask files another job

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B1_always_enqueue`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 9 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_payload_key_this_build_does_not_read_does_not_make_a_stranger`
  - `tests/test_backup_cli.py::test_a_second_ask_for_a_real_backup_is_not_told_the_open_job_copies_nothing`
  - `tests/test_backup_cli.py::test_an_open_backup_whose_destinations_cannot_be_read_is_not_read_as_elsewhere`
  - `tests/test_backup_cli.py::test_asking_for_a_backup_twice_reports_the_open_job_rather_than_a_second`
  - `tests/test_backup_cli.py::test_either_shared_destination_is_the_same_backup[archive_root]`
  - `tests/test_backup_cli.py::test_either_shared_destination_is_the_same_backup[dest]`
  - `tests/test_backup_cli.py::test_the_emptied_flag_is_frozen_by_the_parser_and_rebuilt_by_the_resume`
  - `tests/test_backup_cli.py::test_the_rehearsal_is_said_at_queue_time_and_when_the_open_job_is_reported`
  - `tests/test_backup_cli.py::test_the_warnings_beside_a_reported_job_describe_that_job`

Old text:

```
        if found is not None:
            twin, frozen = found
```

New text:

```
        if False:
            twin, frozen = found
```

### `r222-b.B2_any_verb_is_a_twin`

Drop the handler key comparison, so another verb's open job is reported as the backup

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B2_any_verb_is_a_twin`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_another_verb_s_open_job_is_not_a_backup`

Old text:

```
        if job.handler_key != handler_key or job.library_id != cfg.library.volume_id:
```

New text:

```
        if job.library_id != cfg.library.volume_id:
```

### `r222-b.B3_any_library_is_a_twin`

Drop the library comparison, so a job copying another library is reported as this one's backup

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B3_any_library_is_a_twin`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_another_library_s_open_backup_is_not_this_library_s`

Old text:

```
        if job.handler_key != handler_key or job.library_id != cfg.library.volume_id:
```

New text:

```
        if job.handler_key != handler_key:
```

### `r222-b.B4_rehearsal_is_a_twin`

Drop the rehearsal flag comparison, so an open rehearsal answers a request for a real backup

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B4_rehearsal_is_a_twin`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 3 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_rehearsal_and_a_real_run_are_two_jobs`
  - `tests/test_backup_cli.py::test_the_emptied_flag_is_frozen_by_the_parser_and_rebuilt_by_the_resume`
  - `tests/test_backup_cli.py::test_the_frozen_payload_and_the_parser_agree_about_the_flag`

Old text:

```
        if bool((job.payload or {}).get(DRY_RUN)) != dry_run:
            continue
```

New text:

```
        if False:
            continue
```

### `r222-b.B5_whole_payload_compared`

Compare the whole payload, so a job frozen with one more key is a stranger and a second backup is filed beside it

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B5_whole_payload_compared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 10 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_defect_in_rebuilding_a_configuration_is_not_reported_as_a_queued_backup`
  - `tests/test_backup_cli.py::test_a_payload_key_this_build_does_not_read_does_not_make_a_stranger`
  - `tests/test_backup_cli.py::test_a_second_ask_for_a_real_backup_is_not_told_the_open_job_copies_nothing`
  - `tests/test_backup_cli.py::test_an_open_backup_whose_destinations_cannot_be_read_is_not_read_as_elsewhere`
  - `tests/test_backup_cli.py::test_asking_for_a_backup_twice_reports_the_open_job_rather_than_a_second`
  - `tests/test_backup_cli.py::test_either_shared_destination_is_the_same_backup[archive_root]`
  - `tests/test_backup_cli.py::test_either_shared_destination_is_the_same_backup[dest]`
  - `tests/test_backup_cli.py::test_the_emptied_flag_is_frozen_by_the_parser_and_rebuilt_by_the_resume`
  - `tests/test_backup_cli.py::test_the_rehearsal_is_said_at_queue_time_and_when_the_open_job_is_reported`
  - `tests/test_backup_cli.py::test_the_warnings_beside_a_reported_job_describe_that_job`

Old text:

```
        if bool((job.payload or {}).get(DRY_RUN)) != dry_run:
```

New text:

```
        if dict(job.payload or {}) != {DRY_RUN: dry_run}:
```

### `r222-b.B6_itemless_job_is_a_twin`

Report a job with no items, which refuses when driven, as the backup asked for

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B6_itemless_job_is_a_twin`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_job_that_can_never_run_does_not_stand_in_for_a_backup`

Old text:

```
        if not jobs.items(store, job.job_id):
            continue
        try:
```

New text:

```
        if False:
            continue
        try:
```

### `r222-b.B7_unreadable_is_elsewhere`

Read a frozen configuration that cannot be rebuilt as somewhere else, and file a second job beside it

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B7_unreadable_is_elsewhere`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_an_open_backup_whose_destinations_cannot_be_read_is_not_read_as_elsewhere`

Old text:

```
        except (config.ConfigError, ValueError):
            return job, None
```

New text:

```
        except (config.ConfigError, ValueError):
            continue
```

### `r222-b.B8_every_exception_is_unreadable`

Catch every exception from the rebuild, so a defect in it is reported as an open backup with exit zero

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B8_every_exception_is_unreadable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_defect_in_rebuilding_a_configuration_is_not_reported_as_a_queued_backup`

Old text:

```
        except (config.ConfigError, ValueError):
            return job, None
```

New text:

```
        except Exception:
            return job, None
```

### `r222-b.B9_mirror_not_compared`

Compare only the archive root, so two jobs syncing into one mirror with different archives are strangers

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B9_mirror_not_compared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_either_shared_destination_is_the_same_backup[dest]`

Old text:

```
            frozen.backup.dest == cfg.backup.dest
            or frozen.backup.archive_root == cfg.backup.archive_root
```

New text:

```
            frozen.backup.archive_root == cfg.backup.archive_root
```

### `r349-a.A1_failure_write`

Drop the failure path JSON write: raise the refusal without writing the outcome

- File: `src/cratekit/backup/cli.py`
- Source: `r349-a.json`, row `A1_failure_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 3 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_record_that_cannot_be_written_does_not_replace_the_transfer_failure`
  - `tests/test_backup_cli.py::test_the_outcome_record_is_private_under_a_permissive_umask`

Old text:

```
            raise _with_outcome_recorded(refusal, outcome, outcome_to)
```

New text:

```
            raise refusal
```

### `r349-a.A2_success_produced`

The handler returns nothing on success instead of the staged record

- File: `src/cratekit/backup/cli.py`
- Source: `r349-a.json`, row `A2_success_produced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 6 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_queued_backup_names_every_command_it_ran_in_job_show`
  - `tests/test_backup_cli.py::test_a_rehearsal_s_outcome_is_recorded_and_says_it_was_one`
  - `tests/test_backup_cli.py::test_the_handler_does_not_fail_an_item_over_the_age_read_back`
  - `tests/test_backup_cli.py::test_the_handler_uses_the_configuration_it_was_handed`
  - `tests/test_backup_cli.py::test_the_outcome_record_is_private_under_a_permissive_umask`

Old text:

```
    return jobs.Produced(staged=staged, final=final)
```

New text:

```
    return None
```

### `r349-a.A4_envelope_field`

The backup run --job envelope stops attaching the outcomes field

- File: `src/cratekit/backup/cli.py`
- Source: `r349-a.json`, row `A4_envelope_field`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_queued_backup_names_every_command_it_ran_in_job_show`

Old text:

```
        progress[OUTCOMES] = outcomes
```

New text:

```
        pass
```

### `r349-b.B3_clear_before_attempt`

The handler no longer clears the previous attempt's record

- File: `src/cratekit/backup/cli.py`
- Source: `r349-b.json`, row `B3_clear_before_attempt`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_retry_that_fails_another_way_does_not_show_the_last_attempt_s_commands`

Old text:

```
    backup_facts.clear_outcome(job.job_id, named)
    report = perform_backup(
```

New text:

```
    report = perform_backup(
```

### `r349-b.B4_stage_error_completes`

A staging write error escapes the handler instead of completing the item

- File: `src/cratekit/backup/cli.py`
- Source: `r349-b.json`, row `B4_stage_error_completes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_record_that_cannot_be_staged_does_not_fail_a_completed_backup`

Old text:

```
    except OSError:
        return None
    return jobs.Produced
```

New text:

```
    except KeyError:
        return None
    return jobs.Produced
```

### `r349-c.C2_write_failure_step`

A failed record write returns the refusal without the step saying the record is missing

- File: `src/cratekit/backup/cli.py`
- Source: `r349-c.json`, row `C2_write_failure_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_record_that_cannot_be_written_does_not_replace_the_transfer_failure`

Old text:

```
    except OSError as exc:
        cause = refusal.cause
```

New text:

```
    except OSError as exc:
        return refusal
        cause = refusal.cause
```

### `r390-a.A6_backup_transfer_exit_is_permanent`

the flag the review round added: a transfer exit recorded with no retryable flag

- File: `src/cratekit/backup/cli.py`
- Source: `r390-a.json`, row `A6_backup_transfer_exit_is_permanent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 5 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_portion_decides_the_run_even_when_the_other_completed`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_half_failed_rehearsal_says_it_too_on_the_other_refusal`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`

Old text:

```
            retryable=True,
            origin=("backup", "cli"),
            detail={"portions": [entry.portion.value for entry in failed]},
```

New text:

```
            origin=("backup", "cli"),
            detail={"portions": [entry.portion.value for entry in failed]},
```

### `u45-round-1.A1_unreadable_reported_as_absent`

Return an empty list for an unreadable fact file, so a library with a good backup reads as never backed up

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `A1_unreadable_reported_as_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 5 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_fact_file_that_cannot_be_read_refuses_rather_than_reporting_nothing`
  - `tests/test_backup_cli.py::test_an_unreadable_fact_file_under_a_real_run_gains_no_rehearsal_step`
  - `tests/test_backup_cli.py::test_an_unreadable_fact_file_under_a_rehearsal_says_which_kind_of_run_it_was`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`
  - `tests/test_backup_cli.py::test_the_remedy_for_an_unreadable_fact_file_travels_from_the_exception`

Old text:

```
    except backup_facts.BackupFactsUnreadable as exc:
        raise refuse(
            "backup-facts-unreadable",
```

New text:

```
    except backup_facts.BackupFactsUnreadable as exc:
        del exc
        return []
        raise refuse(
            "backup-facts-unreadable",
```

### `u45-round-1.A4_state_collapsed_to_known`

Report every portion as known, so never-recorded and recorded-in-the-future both read as a current backup

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `A4_state_collapsed_to_known`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 2 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`

Old text:

```
            "state": str(entry.state),
            "age_seconds"
```

New text:

```
            "state": "known",
            "age_seconds"
```

### `u45-round-1.C2_refusal_read_as_failure`

Widen the failed predicate to any portion that did not run, so a refused database portion reads as a failed transfer

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `C2_refusal_read_as_failure`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 6 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_machine_with_no_rclone_fails_every_portion_by_name`
  - `tests/test_backup_cli.py::test_a_machine_with_no_rclone_refuses_by_name`
  - `tests/test_backup_cli.py::test_a_partial_run_succeeds_and_publishes_only_the_half_that_ran`
  - `tests/test_backup_cli.py::test_a_portion_the_engine_refused_fails_rather_than_reporting_a_copy`
  - `tests/test_backup_cli.py::test_nothing_that_ran_is_never_reported_as_a_refusal`
  - `tests/test_backup_cli.py::test_two_portions_refused_for_different_reasons_name_both`

Old text:

```
        entry for entry in outcome.portions if not entry.ran and entry.refusal is None
```

New text:

```
        entry for entry in outcome.portions if not entry.ran
```

### `u45-round-1.C3_nothing_ran_accepted`

Return None when no portion ran, so a machine with no rclone exits OK over a backup that did not happen

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `C3_nothing_ran_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 6 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_job_in_which_nothing_ran_never_reports_success`
  - `tests/test_backup_cli.py::test_a_machine_with_no_rclone_fails_every_portion_by_name`
  - `tests/test_backup_cli.py::test_a_machine_with_no_rclone_refuses_by_name`
  - `tests/test_backup_cli.py::test_a_portion_the_engine_refused_fails_rather_than_reporting_a_copy`
  - `tests/test_backup_cli.py::test_an_outcome_with_no_portions_refuses_rather_than_raising`
  - `tests/test_backup_cli.py::test_two_portions_refused_for_different_reasons_name_both`

Old text:

```
    if any(entry.ran for entry in outcome.portions):
        return None
    refusals
```

New text:

```
    return None
    refusals
```

### `u45-round-1.C4_uniform_refusal_flattened`

Drop the uniform pass-through so every no-run refusal becomes the summary slug and rclone-missing loses install-binary

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `C4_uniform_refusal_flattened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 3 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_machine_with_no_rclone_fails_every_portion_by_name`
  - `tests/test_backup_cli.py::test_a_machine_with_no_rclone_refuses_by_name`
  - `tests/test_backup_cli.py::test_a_portion_the_engine_refused_fails_rather_than_reporting_a_copy`

Old text:

```
    if len(refusals) == 1:
        only = next(iter(refusals))
```

New text:

```
    if False:
        only = next(iter(refusals))
```

### `u45-round-1.C5_first_refusal_taken`

Take the first portion's refusal when the reasons differ, rather than naming all of them

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `C5_first_refusal_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_two_portions_refused_for_different_reasons_name_both`

Old text:

```
    if len(refusals) == 1:
```

New text:

```
    if refusals:
```

### `u45-round-1.C6_partial_run_refused`

Refuse whenever any portion did not run, so a mirror that completed while the database was skipped is reported as a failure

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `C6_partial_run_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 3 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_partial_run_succeeds_and_publishes_only_the_half_that_ran`
  - `tests/test_backup_cli.py::test_an_outcome_with_no_portions_refuses_rather_than_raising`
  - `tests/test_backup_cli.py::test_nothing_that_ran_is_never_reported_as_a_refusal`

Old text:

```
    if any(entry.ran for entry in outcome.portions):
        return None
```

New text:

```
    if all(entry.ran for entry in outcome.portions):
        return None
```

### `u45-round-1.Q1_resume_drops_the_rehearsal`

Drop --dry-run from the resume argv, so a queued rehearsal respawns as a real transfer that publishes an age

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `Q1_resume_drops_the_rehearsal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 2 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_emptied_flag_is_frozen_by_the_parser_and_rebuilt_by_the_resume`
  - `tests/test_backup_cli.py::test_the_resume_rebuilds_the_rehearsal_flag_and_never_carries_a_run`

Old text:

```
    if payload.get(DRY_RUN):
        argv.append("--dry-run")
```

New text:

```
    pass
```

### `u45-round-1.Q2_resume_always_rehearses`

Always emit --dry-run, the other direction, so a real backup respawns as a rehearsal that copies nothing

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `Q2_resume_always_rehearses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_resume_rebuilds_the_rehearsal_flag_and_never_carries_a_run`

Old text:

```
    if payload.get(DRY_RUN):
        argv.append("--dry-run")
```

New text:

```
    argv.append("--dry-run")
```

### `u45-round-1.Q3_resume_loses_the_job`

Drop --job from the resume argv, so the child queues a second backup instead of continuing the first

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `Q3_resume_loses_the_job`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 2 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_emptied_flag_is_frozen_by_the_parser_and_rebuilt_by_the_resume`
  - `tests/test_backup_cli.py::test_the_resume_rebuilds_the_rehearsal_flag_and_never_carries_a_run`

Old text:

```
    return [*argv, "--job", job.job_id]
```

New text:

```
    return list(argv)
```

### `u45-round-1.Q4_payload_key_not_read`

Read a key the handler does not freeze, which is the drift the named constant exists to prevent

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `Q4_payload_key_not_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 2 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_emptied_flag_is_frozen_by_the_parser_and_rebuilt_by_the_resume`
  - `tests/test_backup_cli.py::test_the_resume_rebuilds_the_rehearsal_flag_and_never_carries_a_run`

Old text:

```
    if payload.get(DRY_RUN):
```

New text:

```
    if payload.get("dryrun"):
```

### `u45-round-1.R1_reserved_remediation_discarded`

Replace the reservation table's per-slug remediation with the class default, which is what the first draft did

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `R1_reserved_remediation_discarded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 4 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_machine_with_no_rclone_fails_every_portion_by_name`
  - `tests/test_backup_cli.py::test_a_machine_with_no_rclone_refuses_by_name`
  - `tests/test_backup_cli.py::test_a_portion_the_engine_refused_fails_rather_than_reporting_a_copy`
  - `tests/test_backup_cli.py::test_an_unconfigured_remote_refuses_in_the_backup_vocabulary`

Old text:

```
            remediation=reservations.remediation_for(slug),
```

New text:

```
            remediation=Remediation(),
```

### `u45-round-1.R2_slug_flattened`

Fold every engine refusal into one slug, so nine diagnoses arrive as one and each loses its own fix

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `R2_slug_flattened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 2 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_portion_the_engine_refused_fails_rather_than_reporting_a_copy`
  - `tests/test_backup_cli.py::test_an_unconfigured_remote_refuses_in_the_backup_vocabulary`

Old text:

```
    slug = str(refusal)
    return CratekitError(
```

New text:

```
    slug = str(backup.Refusal.RCLONE_MISSING)
    return CratekitError(
```

### `u45-round-1.W2_report_from_the_plan`

Report the PLAN rather than the OUTCOME, which is the shell half of the first-caller defect

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `W2_report_from_the_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 11 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_completed_warns_about_nothing`
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_stopped_reports_it_and_is_still_a_backup`
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_partial_run_succeeds_and_publishes_only_the_half_that_ran`
  - `tests/test_backup_cli.py::test_a_queued_backup_names_every_command_it_ran_in_job_show`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`
  - `tests/test_backup_cli.py::test_a_rehearsal_s_outcome_is_recorded_and_says_it_was_one`
  - `tests/test_backup_cli.py::test_a_run_that_succeeded_publishes_an_age_the_session_reads_back`
  - `tests/test_backup_cli.py::test_every_command_the_engine_ran_is_paired_with_its_own_return_code`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`

Old text:

```
    report = backup.outcome_payload(outcome)
```

New text:

```
    report = backup.plan_payload(plan)
```

### `u45-round-1.W3_ages_not_read_back`

Drop the age read-back, so the verb never reports what a destructive session would see

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `W3_ages_not_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 5 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_completed_warns_about_nothing`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`
  - `tests/test_backup_cli.py::test_a_run_that_succeeded_publishes_an_age_the_session_reads_back`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`

Old text:

```
    report["ages"] = published_ages(cfg, now=now)
```

New text:

```
    report["ages"] = []
```

### `u45-round-1.W4_ages_derived_from_the_outcome`

Derive the published ages from the outcome instead of reading the fact file, the duplicate rule the module argues against

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `W4_ages_derived_from_the_outcome`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 3 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`

Old text:

```
    report["ages"] = published_ages(cfg, now=now)
```

New text:

```
    report["ages"] = [
        {"portion": p.portion.value, "state": "known" if p.ran else "never-recorded"}
        for p in outcome.portions
    ]
```

### `u45-round-1.W5_publishing_switched_off`

Pass publish=False, so a successful backup records no age and the write session still sees never-recorded

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `W5_publishing_switched_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 9 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_completed_warns_about_nothing`
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_stopped_reports_it_and_is_still_a_backup`
  - `tests/test_backup_cli.py::test_a_partial_run_succeeds_and_publishes_only_the_half_that_ran`
  - `tests/test_backup_cli.py::test_a_run_that_succeeded_publishes_an_age_the_session_reads_back`
  - `tests/test_backup_cli.py::test_a_supplied_configuration_is_used_rather_than_the_one_on_disk`
  - `tests/test_backup_cli.py::test_the_age_a_driven_run_publishes_is_the_engine_s_and_reaches_the_envelope`
  - `tests/test_backup_cli.py::test_the_ages_a_rehearsal_reports_are_the_previous_real_runs_and_it_says_so`
  - `tests/test_backup_cli.py::test_the_ages_reported_are_the_ones_this_job_published`
  - `tests/test_backup_cli.py::test_the_report_carries_the_age_number_and_not_only_the_state`

Old text:

```
    outcome = backup.run_backup(cfg, plan, runner=runner, now=now, dry_run=dry_run)
```

New text:

```
    outcome = backup.run_backup(
        cfg, plan, runner=runner, now=now, dry_run=dry_run, publish=False
    )
```

### `u45-round-1.W6_rehearsal_becomes_a_real_run`

Ignore the frozen dry-run key, so a rehearsal transfers for real and publishes an age

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `W6_rehearsal_becomes_a_real_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 6 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`
  - `tests/test_backup_cli.py::test_a_rehearsal_s_outcome_is_recorded_and_says_it_was_one`
  - `tests/test_backup_cli.py::test_the_ages_a_rehearsal_reports_are_the_previous_real_runs_and_it_says_so`
  - `tests/test_backup_cli.py::test_the_handler_does_not_fail_an_item_over_the_age_read_back`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`

Old text:

```
    dry_run = bool(payload.get(DRY_RUN))
```

New text:

```
    dry_run = False
```

### `u45-round-1.W8_engine_refusal_escapes`

Let BackupRefused escape, so an unconfigured remote reaches the dispatcher as internal-error with report-defect

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `W8_engine_refusal_escapes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_an_unconfigured_remote_refuses_in_the_backup_vocabulary`

Old text:

```
    except backup.BackupRefused as exc:
        raise _engine_refusal(
            exc.refusal, exc.detail, library=str(cfg.library.root)
        ) from exc
```

New text:

```
    except backup.BackupRefused:
        raise
```

### `u45-round-2.A3_age_seconds_always_none`

Report no age number even for a known portion, so the value R15's warning quotes never reaches the report

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-2.json`, row `A3_age_seconds_always_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_report_carries_the_age_number_and_not_only_the_state`

Old text:

```
            "age_seconds": entry.age.total_seconds() if entry.age is not None else None,
```

New text:

```
            "age_seconds": None,
```

### `u45-round-2.C7_failed_detail_dropped`

Reword the transfer-failed message so it no longer says a destructive session still sees the previous age

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-2.json`, row `C7_failed_detail_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_transfer_failure_says_no_age_was_published`

Old text:

```
            + ". No backup age was published for that portion, so a destructive "
            "session still sees whatever the last successful run left",
```

New text:

```
            + ". The run stopped there.",
```

### `u50-author.B1_no_items_enqueued`

Queue the backup with no items, so the driver has nothing to claim and reports an empty success

- File: `src/cratekit/backup/cli.py`
- Source: `u50-author.json`, row `B1_no_items_enqueued`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 39 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_backup_job_carries_one_item_per_declared_portion`
  - `tests/test_backup_cli.py::test_a_contained_analysis_share_draws_no_warning_from_the_verb`
  - `tests/test_backup_cli.py::test_a_defect_in_rebuilding_a_configuration_is_not_reported_as_a_queued_backup`
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_half_failed_rehearsal_says_it_too_on_the_other_refusal`
  - `tests/test_backup_cli.py::test_a_job_in_which_nothing_ran_never_reports_success`
  - `tests/test_backup_cli.py::test_a_library_whose_identity_cannot_be_a_marker_is_told_so`
  - `tests/test_backup_cli.py::test_a_library_with_an_identity_draws_no_such_warning`
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
  - `tests/test_backup_cli.py::test_a_queued_backup_names_every_command_it_ran_in_job_show`
  - `tests/test_backup_cli.py::test_a_queued_backup_runs_every_portion_through_the_real_resume`
  - `tests/test_backup_cli.py::test_a_queued_real_backup_carries_no_rehearsal_word`
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - ... and 24 more, see the JSON sidecar

Old text:

```
            item_ids=backup_items(),
```

New text:

```
(empty)
```

### `u50-author.B3_items_one_portion_only`

Queue only the mirror, so the database half of every backup is never claimed

- File: `src/cratekit/backup/cli.py`
- Source: `u50-author.json`, row `B3_items_one_portion_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 17 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_backup_job_carries_one_item_per_declared_portion`
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_half_failed_rehearsal_says_it_too_on_the_other_refusal`
  - `tests/test_backup_cli.py::test_a_queued_backup_names_every_command_it_ran_in_job_show`
  - `tests/test_backup_cli.py::test_a_queued_backup_runs_every_portion_through_the_real_resume`
  - `tests/test_backup_cli.py::test_a_rehearsal_s_outcome_is_recorded_and_says_it_was_one`
  - `tests/test_backup_cli.py::test_an_item_naming_something_that_is_not_a_portion_refuses_by_name`
  - `tests/test_backup_cli.py::test_an_outside_analysis_share_is_carried_through_the_verb`
  - `tests/test_backup_cli.py::test_asking_twice_about_a_half_failed_backup_answers_the_same_way_twice`
  - `tests/test_backup_cli.py::test_queueing_still_needs_nothing_from_the_machine`
  - `tests/test_backup_cli.py::test_the_age_a_driven_run_publishes_is_the_engine_s_and_reaches_the_envelope`
  - `tests/test_backup_cli.py::test_the_ages_a_rehearsal_reports_are_the_previous_real_runs_and_it_says_so`
  - `tests/test_backup_cli.py::test_the_ages_reported_are_the_ones_this_job_published`
  - ... and 2 more, see the JSON sidecar

Old text:

```
    return tuple(str(portion) for portion in backup_facts.Portion)
```

New text:

```
    return (str(backup_facts.Portion.FILES),)
```

### `u50-author.W1_no_narrowing`

Ignore the portion and run the whole plan for every item, so each item does the whole backup

- File: `src/cratekit/backup/cli.py`
- Source: `u50-author.json`, row `W1_no_narrowing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if portion is not None:
```

New text:

```
    if False:
```

### `u50-author.W5_unknown_portion_unchecked`

Let an undeclared item name raise out of the coercion rather than refusing by name

- File: `src/cratekit/backup/cli.py`
- Source: `u50-author.json`, row `W5_unknown_portion_unchecked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_an_item_naming_something_that_is_not_a_portion_refuses_by_name`

Old text:

```
        raise refuse(
            "internal-error",
            f"this job's item is {named!r}, which is not a backup portion this "
            f"build declares. The portions are {', '.join(declared)}",
```

New text:

```
        raise refuse(
            "internal-error",
            "the item could not be read",
```

### `u50-author.W6_fresh_config_in_the_handler`

Load the configuration in the handler rather than using the one frozen on the job (KTD9)

- File: `src/cratekit/backup/cli.py`
- Source: `u50-author.json`, row `W6_fresh_config_in_the_handler`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 29 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_contained_analysis_share_draws_no_warning_from_the_verb`
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_half_failed_rehearsal_says_it_too_on_the_other_refusal`
  - `tests/test_backup_cli.py::test_a_library_whose_identity_cannot_be_a_marker_is_told_so`
  - `tests/test_backup_cli.py::test_a_library_with_an_identity_draws_no_such_warning`
  - `tests/test_backup_cli.py::test_a_queued_backup_names_every_command_it_ran_in_job_show`
  - `tests/test_backup_cli.py::test_a_queued_backup_runs_every_portion_through_the_real_resume`
  - `tests/test_backup_cli.py::test_a_queued_real_backup_carries_no_rehearsal_word`
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_a_record_that_cannot_be_staged_does_not_fail_a_completed_backup`
  - `tests/test_backup_cli.py::test_a_rehearsal_s_outcome_is_recorded_and_says_it_was_one`
  - `tests/test_backup_cli.py::test_a_resume_reports_the_queued_job_rather_than_filing_a_second`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`
  - ... and 14 more, see the JSON sidecar

Old text:

```
        cfg=cfg,
        # RESOLVED AT CALL TIME, not left to the default, so a test can put a
        # stand-in in front of it. ``perform_backup``'s own default is bound when
        # this module is imported and cannot be reached any other way.
        runner=backup.subprocess_runner,
```

New text:

```
        cfg=_load(),
        runner=backup.subprocess_runner,
```

### `u50-review-fixes.R2_empty_job_guard_dropped`

Drive a job with no items, so a job queued by the previous build reports SUCCEEDED over a library nothing copied

- File: `src/cratekit/backup/cli.py`
- Source: `u50-review-fixes.json`, row `R2_empty_job_guard_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_job_queued_before_the_worker_existed_refuses_rather_than_succeeding`

Old text:

```
                _refuse_an_empty_job(store, job)
```

New text:

```
(empty)
```

### `u50-zero-rows.B2_items_hardcoded_pair`

Name the two portions instead of deriving them, so a third portion is queued by nobody

- File: `src/cratekit/backup/cli.py`
- Source: `u50-zero-rows.json`, row `B2_items_hardcoded_pair`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_item_list_is_derived_from_the_portions_rather_than_written_out`

Old text:

```
    return tuple(str(portion) for portion in backup_facts.Portion)
```

New text:

```
    return ("files", "database")
```

### `u50-zero-rows.W4b_item_ignored_entirely`

Back up the mirror whatever the item says, so every item of the job does the same half

- File: `src/cratekit/backup/cli.py`
- Source: `u50-zero-rows.json`, row `W4b_item_ignored_entirely`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 16 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_half_failed_rehearsal_says_it_too_on_the_other_refusal`
  - `tests/test_backup_cli.py::test_a_queued_backup_names_every_command_it_ran_in_job_show`
  - `tests/test_backup_cli.py::test_a_queued_backup_runs_every_portion_through_the_real_resume`
  - `tests/test_backup_cli.py::test_a_rehearsal_s_outcome_is_recorded_and_says_it_was_one`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`
  - `tests/test_backup_cli.py::test_a_retry_that_fails_another_way_does_not_show_the_last_attempt_s_commands`
  - `tests/test_backup_cli.py::test_an_item_naming_something_that_is_not_a_portion_refuses_by_name`
  - `tests/test_backup_cli.py::test_an_outside_analysis_share_is_carried_through_the_verb`
  - `tests/test_backup_cli.py::test_asking_twice_about_a_half_failed_backup_answers_the_same_way_twice`
  - `tests/test_backup_cli.py::test_the_age_a_driven_run_publishes_is_the_engine_s_and_reaches_the_envelope`
  - `tests/test_backup_cli.py::test_the_ages_a_rehearsal_reports_are_the_previous_real_runs_and_it_says_so`
  - `tests/test_backup_cli.py::test_the_ages_reported_are_the_ones_this_job_published`
  - ... and 1 more, see the JSON sidecar

Old text:

```
    named = str(item.item_id or "")
```

New text:

```
    named = str(backup_facts.Portion.FILES)
```

### `r154-a.A1_stamp_pattern`

Drop the pattern half of is_stamp, so the calendar parse alone decides and its lenient padding admits 2026-8-01T000000Z

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r154-a.json`, row `A1_stamp_pattern`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 209 against a baseline of 209
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_snapshot_value_that_is_not_a_stamp_is_refused_before_the_remote_is_asked[2026-8-01T000000Z]`

Old text:

```
    if not _STAMP_SHAPE.fullmatch(value):
        return False
    try:
        datetime.strptime(value, _STAMP_FORMAT)
```

New text:

```
    try:
        datetime.strptime(value, _STAMP_FORMAT)
```

### `r154-a.A2_stamp_calendar`

Drop the calendar half of is_stamp, so the pattern alone decides and a thirteenth month is a stamp

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r154-a.json`, row `A2_stamp_calendar`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 209 against a baseline of 209
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_snapshot_value_that_is_not_a_stamp_is_refused_before_the_remote_is_asked[2026-13-01T000000Z]`

Old text:

```
    try:
        datetime.strptime(value, _STAMP_FORMAT)
    except ValueError:
        return False
    return True
```

New text:

```
    return True
```

### `r154-a.A4_legacy_spelling`

Accept only this product's stamp as a snapshot name, so every snapshot the source system wrote is refused by name and hidden from the listing

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r154-a.json`, row `A4_legacy_spelling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 209 against a baseline of 209
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_snapshot_the_source_system_wrote_is_still_a_name_and_still_pulled`

Old text:

```
    if is_stamp(value):
        return True
    if not _LEGACY_SHAPE.fullmatch(value):
        return False
```

New text:

```
    if is_stamp(value):
        return True
    return False
    if not _LEGACY_SHAPE.fullmatch(value):
        return False
```

### `r154-a.A5_listing_filter`

List every folder under the snapshot root as a snapshot, so a stray folder sorting last is the newest

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r154-a.json`, row `A5_listing_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 209 against a baseline of 209
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_newest_snapshot_ignores_folders_that_are_not_stamps`

Old text:

```
            if is_snapshot_name(name)
```

New text:

```
            if name
```

### `r154-a.A7_read_normalization`

Compare a marker's identity as spelled on the remote, so a marker written in another letter case names a foreign volume

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r154-a.json`, row `A7_read_normalization`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 209 against a baseline of 209
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_identity_is_compared_case_blind_like_the_volume_gate`

Old text:

```
        preflight.normalize_identity(name[len(IDENTITY_MARKER_PREFIX):])
```

New text:

```
        name[len(IDENTITY_MARKER_PREFIX):]
```

### `r154-a.A8_empty_expected`

Let an expected identity of nothing stay the empty string, so it matches a marker with nothing after its prefix

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r154-a.json`, row `A8_empty_expected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 209 against a baseline of 209
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_an_empty_expected_identity_never_matches_an_empty_marker[   ]`
  - `tests/modules/test_tools.py::test_an_empty_expected_identity_never_matches_an_empty_marker[]`

Old text:

```
    expected = (preflight.normalize_identity(wanted) or None) if wanted is not None else None
```

New text:

```
    expected = preflight.normalize_identity(wanted) if wanted is not None else None
```

### `r154-b.B2_two_markers`

Accept a named snapshot when the expected identity is AMONG its markers, so a folder two libraries wrote passes on either one

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r154-b.json`, row `B2_two_markers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 209 against a baseline of 209
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_snapshot_carrying_two_identities_is_refused`
  - `tests/modules/test_tools.py::test_two_markers_are_refused_without_offering_an_identity_to_pass`

Old text:

```
        if recorded == (expected,):
            return ResolvedSnapshot(stamp=snapshot, recorded_volume=expected, named=True)
```

New text:

```
        if expected in recorded:
            return ResolvedSnapshot(stamp=snapshot, recorded_volume=expected, named=True)
```

### `r154-b.B3_handed_down_stamp`

Ignore accept_unrecorded, so a stamp the verb resolved and handed down arrives looking typed and an unmarked one is pulled

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r154-b.json`, row `B3_handed_down_stamp`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 209 against a baseline of 209
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_resolved_stamp_handed_down_is_not_mistaken_for_one_a_person_named`

Old text:

```
        accepted = True if accept_unrecorded is None else accept_unrecorded
```

New text:

```
        accepted = True
```

### `r154-b.B4_stated_volume_over_unmarked`

Pull an unmarked named snapshot even when a person stated the volume it should record, so the statement is checked against nothing

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r154-b.json`, row `B4_stated_volume_over_unmarked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 209 against a baseline of 209
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_replaced_drive_restores_the_old_volumes_snapshot_by_naming_it`

Old text:

```
        if not recorded and snapshot_volume is None and accepted:
```

New text:

```
        if not recorded and accepted:
```

### `r154-b.B5_veto_not_select`

Read only the newest folder, which is the first cut: a shared root refuses whenever the other library backed up last

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r154-b.json`, row `B5_veto_not_select`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 209 against a baseline of 209
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_default_takes_the_newest_snapshot_that_is_this_librarys`
  - `tests/modules/test_tools.py::test_the_default_walk_is_bounded_and_the_refusal_says_how_far_it_looked`
  - `tests/modules/test_tools.py::test_the_replaced_drive_identity_selects_the_newest_of_the_old_volumes`

Old text:

```
    newest = names[::-1][:NEWEST_WALK]
```

New text:

```
    newest = names[::-1][:1]
```

### `r154-b.B6_walk_bound`

Multiply the walk bound by ten, so a remote of foreign snapshots is read far past what the refusal says it looked at

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r154-b.json`, row `B6_walk_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 209 against a baseline of 209
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_default_walk_is_bounded_and_the_refusal_says_how_far_it_looked`

Old text:

```
NEWEST_WALK = 8
```

New text:

```
NEWEST_WALK = 80
```

### `r154-b.B8_walk_match`

Stop the walk at the first folder carrying ANY marker, so the default pulls another library's snapshot under a shared root

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r154-b.json`, row `B8_walk_match`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 209 against a baseline of 209
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_default_takes_the_newest_snapshot_that_is_this_librarys`
  - `tests/modules/test_tools.py::test_the_default_walk_is_bounded_and_the_refusal_says_how_far_it_looked`
  - `tests/modules/test_tools.py::test_the_replaced_drive_identity_selects_the_newest_of_the_old_volumes`

Old text:

```
        if seen[name] == (expected,):
            return ResolvedSnapshot(stamp=name, recorded_volume=expected, named=False)
```

New text:

```
        if seen[name]:
            return ResolvedSnapshot(stamp=name, recorded_volume=expected, named=False)
```

### `r222-a.A10_plan_text_at_keep_zero`

Describe the held run at a keep of zero, so the preview promises a retention the run does not apply

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r222-a.json`, row `A10_plan_text_at_keep_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 209 against a baseline of 209
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_plan_describes_the_rotation_the_run_applies[0-keeping no-last completed mirror]`

Old text:

```
    if archive_keep == 0:
        return "keeping no dated archive folder"
```

New text:

```
    if False:
        return "keeping no dated archive folder"
```

### `r367.E3_a_live_rekordbox_is_ignored`

existing guard sample: a restore proceeds while rekordbox holds the database

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r367.json`, row `E3_a_live_rekordbox_is_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 209 against a baseline of 209
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_restore_refuses_while_rekordbox_holds_the_database`

Old text:

```
    if running:
        raise BackupRefused(
            Refusal.REKORDBOX_RUNNING,
```

New text:

```
    if running and False:
        raise BackupRefused(
            Refusal.REKORDBOX_RUNNING,
```

### `r367.G8_files_only_is_dropped`

directories in the snapshot folder can be read as sidecar names

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r367.json`, row `G8_files_only_is_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 209 against a baseline of 209
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_snapshot_listing_is_of_the_database_folder`

Old text:

```
                f"{cfg.backup.db_dest_root}/{snapshot}/db/",
                "--files-only",
```

New text:

```
                f"{cfg.backup.db_dest_root}/{snapshot}/db/",
```

### `u279.M12_holder_never_found`

Exclusion.holder: answer None for every path, so no anchor is placed in an excluded folder

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u279.json`, row `M12_holder_never_found`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 366 against a baseline of 366
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_an_anchor_inside_an_excluded_folder_is_refused_naming_the_folder[staging]`
  - `tests/test_setbuilder_excluded.py::test_an_anchor_inside_an_excluded_folder_is_refused_naming_the_folder[state]`

Old text:

```
            if identity in self.folders:
                return self.folders[identity]
```

New text:

```
            if False:
                return self.folders[identity]
```

### `u279.M1_walk_ignores_exclude`

iter_audio: walk the whole root again, sorted(root.rglob), so the excluded folders are indexed (the defect itself)

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u279.json`, row `M1_walk_ignores_exclude`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 366 against a baseline of 366
- Kills: 10 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_a_companion_held_only_in_staging_is_left_out_of_the_set`
  - `tests/test_setbuilder_excluded.py::test_a_name_held_only_in_staging_is_not_indexed_and_says_what_is`
  - `tests/test_setbuilder_excluded.py::test_a_staging_copy_never_takes_the_library_files_place`
  - `tests/test_setbuilder_excluded.py::test_an_earlier_cache_entry_under_an_excluded_folder_is_not_served`
  - `tests/test_setbuilder_excluded.py::test_an_excluded_folder_is_matched_by_location_whatever_its_spelling`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[download-staging]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[renamed-state-folder]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[state-folder]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[tilde-staging]`
  - `tests/test_setbuilder_excluded.py::test_the_excluded_walk_is_todays_walk_less_the_excluded_folders`

Old text:

```
    for candidate in sorted(Exclusion.under(root, exclude).walk(root)):
```

New text:

```
    for candidate in sorted(root.rglob("*")):
```

### `u279.M2_excluded_folder_walked`

Exclusion.walk: drop the skip of an excluded folder, so the hand walk yields it and its contents

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u279.json`, row `M2_excluded_folder_walked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 366 against a baseline of 366
- Kills: 10 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_a_companion_held_only_in_staging_is_left_out_of_the_set`
  - `tests/test_setbuilder_excluded.py::test_a_name_held_only_in_staging_is_not_indexed_and_says_what_is`
  - `tests/test_setbuilder_excluded.py::test_a_staging_copy_never_takes_the_library_files_place`
  - `tests/test_setbuilder_excluded.py::test_an_earlier_cache_entry_under_an_excluded_folder_is_not_served`
  - `tests/test_setbuilder_excluded.py::test_an_excluded_folder_is_matched_by_location_whatever_its_spelling`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[download-staging]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[renamed-state-folder]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[state-folder]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[tilde-staging]`
  - `tests/test_setbuilder_excluded.py::test_the_excluded_walk_is_todays_walk_less_the_excluded_folders`

Old text:

```
            if identity in self.folders:
                continue
            yield child
```

New text:

```
            yield child
```

### `u279.M3_ancestor_taken_whole`

Exclusion.walk: hand an ancestor of an excluded folder to rglob whole, so a nested excluded folder is walked

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u279.json`, row `M3_ancestor_taken_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 366 against a baseline of 366
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_the_excluded_walk_is_todays_walk_less_the_excluded_folders`

Old text:

```
            if identity in self.ancestors:
```

New text:

```
            if False:
```

### `u279.M4_symlink_followed`

Exclusion.walk: read a symlinked folder on the hand walked path as a directory, so it is descended where rglob does not

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u279.json`, row `M4_symlink_followed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 366 against a baseline of 366
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_the_excluded_walk_is_todays_walk_less_the_excluded_folders`

Old text:

```
                if entry.is_dir(follow_symlinks=False):
```

New text:

```
                if entry.is_dir():
```

### `u279.M5_unlistable_raises`

Exclusion.walk: catch only a missing folder, so one the walk cannot list stops the index where rglob passes it over

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u279.json`, row `M5_unlistable_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 366 against a baseline of 366
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_a_folder_the_walk_cannot_list_is_passed_over_as_today`

Old text:

```
                entries = list(listing)
        except OSError:
            return
```

New text:

```
                entries = list(listing)
        except FileNotFoundError:
            return
```

### `u279.M6_chain_unresolved`

_chain_to: read the configured folder as spelled, so a staging folder configured through a link outside the root excludes nothing

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u279.json`, row `M6_chain_unresolved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 366 against a baseline of 366
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_an_excluded_folder_is_matched_by_location_whatever_its_spelling`

Old text:

```
        current = folder.resolve()
```

New text:

```
        current = folder.absolute()
```

### `u279.M7_outermost_folder_excluded`

Exclusion.under: exclude the outermost folder above a configured one rather than the folder itself, so its library siblings are dropped

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u279.json`, row `M7_outermost_folder_excluded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 366 against a baseline of 366
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_the_excluded_walk_is_todays_walk_less_the_excluded_folders`

Old text:

```
                folders.setdefault(chain[0], Path(folder))
```

New text:

```
                folders.setdefault(chain[-1], Path(folder))
```

### `u279.M10_tilde_not_expanded`

excluded_folders: read the staging path without expanding a tilde, round one's finding

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u279.json`, row `M10_tilde_not_expanded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 366 against a baseline of 366
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[tilde-staging]`

Old text:

```
Path(cfg.paths.download_staging).expanduser())
```

New text:

```
Path(cfg.paths.download_staging))
```

### `u279.M11_excluded_anchor_not_refused`

set_build: drop the excluded anchor refusal, so an anchor in staging gets the generic not indexed wording

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u279.json`, row `M11_excluded_anchor_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 366 against a baseline of 366
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_an_anchor_inside_an_excluded_folder_is_refused_naming_the_folder[staging]`
  - `tests/test_setbuilder_excluded.py::test_an_anchor_inside_an_excluded_folder_is_refused_naming_the_folder[state]`

Old text:

```
    _refuse_if_excluded(candidate, cfg, root)

```

New text:

```
(empty)
```

### `u279.M13_wrong_folder_named`

_refuse_if_excluded: say the state folder whichever folder holds the anchor

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u279.json`, row `M13_wrong_folder_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 366 against a baseline of 366
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_an_anchor_inside_an_excluded_folder_is_refused_naming_the_folder[staging]`

Old text:

```
    if holder == folders[0]:
```

New text:

```
    if True:
```

### `u279.M8_index_call_unexcluded`

setbuild _index: drop exclude, so the verb's index walks the state and staging folders again

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u279.json`, row `M8_index_call_unexcluded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 366 against a baseline of 366
- Kills: 6 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_a_companion_held_only_in_staging_is_left_out_of_the_set`
  - `tests/test_setbuilder_excluded.py::test_a_name_held_only_in_staging_is_not_indexed_and_says_what_is`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[download-staging]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[renamed-state-folder]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[state-folder]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[tilde-staging]`

Old text:

```
        exclude=excluded_folders(cfg),

```

New text:

```
(empty)
```

### `u279.M9_staging_not_excluded`

excluded_folders: leave download staging out of the exclusion, the state folder only

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u279.json`, row `M9_staging_not_excluded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 366 against a baseline of 366
- Kills: 4 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_a_name_held_only_in_staging_is_not_indexed_and_says_what_is`
  - `tests/test_setbuilder_excluded.py::test_an_anchor_inside_an_excluded_folder_is_refused_naming_the_folder[staging]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[download-staging]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[tilde-staging]`

Old text:

```
    return (config.library_state_dir(cfg), Path(cfg.paths.download_staging).expanduser())
```

New text:

```
    return (config.library_state_dir(cfg), config.library_state_dir(cfg))
```

### `r154-a.A3_named_shape_check`

Never refuse a named snapshot on shape, which is the finding itself: the traversal value reaches the remote path again

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r154-a.json`, row `A3_named_shape_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 307 against a baseline of 307
- Kills: 9 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_snapshot_value_that_is_not_a_stamp_is_refused_before_the_remote_is_asked[../another-library-snapshots/2020-01-01T000000Z]`
  - `tests/modules/test_tools.py::test_a_snapshot_value_that_is_not_a_stamp_is_refused_before_the_remote_is_asked[2026-08-01T000000Z ]`
  - `tests/modules/test_tools.py::test_a_snapshot_value_that_is_not_a_stamp_is_refused_before_the_remote_is_asked[2026-08-01T000000Z/../../elsewhere]`
  - `tests/modules/test_tools.py::test_a_snapshot_value_that_is_not_a_stamp_is_refused_before_the_remote_is_asked[2026-08-01]`
  - `tests/modules/test_tools.py::test_a_snapshot_value_that_is_not_a_stamp_is_refused_before_the_remote_is_asked[2026-13-01T000000Z]`
  - `tests/modules/test_tools.py::test_a_snapshot_value_that_is_not_a_stamp_is_refused_before_the_remote_is_asked[2026-8-01T000000Z]`
  - `tests/modules/test_tools.py::test_a_snapshot_value_that_is_not_a_stamp_is_refused_before_the_remote_is_asked[]`
  - `tests/modules/test_tools.py::test_a_snapshot_value_that_is_not_a_stamp_is_refused_before_the_remote_is_asked[newest]`
  - `tests/test_restore_cli.py::test_the_ledgers_traversal_value_is_refused_at_the_verb`

Old text:

```
        if not is_snapshot_name(snapshot):
```

New text:

```
        if False:
```

### `r154-b.B1_named_mismatch`

Accept a named snapshot carrying ANY marker, which is the finding's real half: a well formed stamp from another library is pulled

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r154-b.json`, row `B1_named_mismatch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 307 against a baseline of 307
- Kills: 9 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_marker_with_no_identity_after_its_prefix_is_not_read_as_unmarked`
  - `tests/modules/test_tools.py::test_a_replaced_drive_restores_the_old_volumes_snapshot_by_naming_it`
  - `tests/modules/test_tools.py::test_a_snapshot_carrying_two_identities_is_refused`
  - `tests/modules/test_tools.py::test_a_snapshot_marked_for_another_library_is_refused`
  - `tests/modules/test_tools.py::test_an_empty_expected_identity_never_matches_an_empty_marker[   ]`
  - `tests/modules/test_tools.py::test_an_empty_expected_identity_never_matches_an_empty_marker[]`
  - `tests/modules/test_tools.py::test_two_markers_are_refused_without_offering_an_identity_to_pass`
  - `tests/test_restore_cli.py::test_another_librarys_snapshot_is_refused_at_the_verb_and_names_both_volumes`
  - `tests/test_restore_cli.py::test_the_replaced_drive_flag_reaches_the_engine_and_the_digest`

Old text:

```
        if recorded == (expected,):
            return ResolvedSnapshot(stamp=snapshot, recorded_volume=expected, named=True)
```

New text:

```
        if recorded:
            return ResolvedSnapshot(stamp=snapshot, recorded_volume=expected, named=True)
```

### `r154-b.B7_walk_order`

Walk oldest first, so the default pulls the OLDEST snapshot that is this library's

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r154-b.json`, row `B7_walk_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 307 against a baseline of 307
- Kills: 6 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_default_takes_the_newest_snapshot_that_is_this_librarys`
  - `tests/modules/test_tools.py::test_the_default_walk_is_bounded_and_the_refusal_says_how_far_it_looked`
  - `tests/modules/test_tools.py::test_the_replaced_drive_identity_selects_the_newest_of_the_old_volumes`
  - `tests/test_restore_cli.py::test_a_backup_landing_between_the_two_acts_moves_the_digest`
  - `tests/test_restore_cli.py::test_the_report_names_the_snapshot_that_arrived`
  - `tests/test_restore_cli.py::test_what_is_offered_is_what_is_pulled`

Old text:

```
    newest = names[::-1][:NEWEST_WALK]
```

New text:

```
    newest = names[:NEWEST_WALK]
```

### `r367.E1_a_failed_transfer_is_unread`

existing guard sample: run_restore returns results without reading return codes

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r367.json`, row `E1_a_failed_transfer_is_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 307 against a baseline of 307
- Kills: 42 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_database_copy_still_refuses_when_the_sidecar_is_absent`
  - `tests/modules/test_tools.py::test_a_rehearsed_restore_does_not_clear_the_live_sidecars`
  - `tests/modules/test_tools.py::test_a_restore_from_a_snapshot_holding_only_the_database_skips_the_absent_sidecar`
  - `tests/modules/test_tools.py::test_a_restore_from_a_snapshot_holding_the_log_copies_it`
  - `tests/modules/test_tools.py::test_restore_removes_stale_sidecars_before_copying`
  - `tests/modules/test_tools.py::test_the_sidecars_are_cleared_before_the_mirror_too`
  - `tests/test_restore_cli.py::test_a_backup_landing_after_the_approval_does_not_change_what_is_pulled`
  - `tests/test_restore_cli.py::test_a_database_half_that_landed_part_of_the_fileset_is_refused_until_the_step`
  - `tests/test_restore_cli.py::test_a_database_that_was_never_on_the_lost_volume_is_not_recovered_onto_the_new_one`
  - `tests/test_restore_cli.py::test_a_failed_database_half_says_the_mirror_arrived_and_what_to_remove`
  - `tests/test_restore_cli.py::test_a_failed_mirror_stops_the_recovery_before_the_database`
  - `tests/test_restore_cli.py::test_a_failed_transfer_refuses_and_never_reports_a_restore_that_did_not_happen`
  - `tests/test_restore_cli.py::test_a_live_restore_in_the_outside_layout_withholds_the_share_and_closes_clean`
  - `tests/test_restore_cli.py::test_a_mirror_pull_with_no_session_named_is_reported_as_work_that_happened`
  - `tests/test_restore_cli.py::test_a_mirror_still_carrying_the_database_does_not_land_it`
  - ... and 27 more, see the JSON sidecar

Old text:

```
        if result.returncode != 0:
            raise BackupRefused(
                Refusal.RESTORE_TRANSFER_FAILED,
```

New text:

```
        if result.returncode == 0:
            raise BackupRefused(
                Refusal.RESTORE_TRANSFER_FAILED,
```

### `r367.E2_an_unconfirmed_restore_is_allowed`

existing guard sample: a restore proceeds without the named decision

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r367.json`, row `E2_an_unconfirmed_restore_is_allowed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 307 against a baseline of 307
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_restore_is_a_named_decision_and_never_a_prompt`

Old text:

```
    if not confirmed:
        raise BackupRefused(
            Refusal.RESTORE_NOT_CONFIRMED,
```

New text:

```
    if confirmed and False:
        raise BackupRefused(
            Refusal.RESTORE_NOT_CONFIRMED,
```

### `r367.G12_listing_results_are_discarded`

the listing runs and its names are thrown away, so every sidecar is treated as absent

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r367.json`, row `G12_listing_results_are_discarded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 307 against a baseline of 307
- Kills: 12 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_restore_from_a_snapshot_holding_the_log_copies_it`
  - `tests/modules/test_tools.py::test_restore_writes_back_the_log_and_never_the_shared_memory_index`
  - `tests/test_restore_cli.py::test_a_database_half_that_landed_part_of_the_fileset_is_refused_until_the_step`
  - `tests/test_restore_cli.py::test_a_failed_mirror_stops_the_recovery_before_the_database`
  - `tests/test_restore_cli.py::test_a_mirror_pull_with_no_session_named_is_reported_as_work_that_happened`
  - `tests/test_restore_cli.py::test_a_mirror_still_carrying_the_database_does_not_land_it`
  - `tests/test_restore_cli.py::test_a_recovery_lands_the_mirror_and_the_database_only_under_the_target`
  - `tests/test_restore_cli.py::test_a_recovery_whose_database_half_failed_reruns_with_nothing_removed`
  - `tests/test_restore_cli.py::test_a_recovery_whose_mirror_was_cut_off_reruns_with_nothing_removed`
  - `tests/test_restore_cli.py::test_a_rehearsal_passes_the_same_gates_and_writes_nothing`
  - `tests/test_restore_cli.py::test_both_halves_run_inside_one_holding_of_the_recovery_lock`
  - `tests/test_restore_cli.py::test_every_transfer_is_pointed_under_the_target_and_nowhere_else`

Old text:

```
    held = snapshot_filenames(cfg, chosen, runner=runner)
```

New text:

```
    snapshot_filenames(cfg, chosen, runner=runner)
    held = frozenset()
```

### `r367.G1_always_copy_the_restored_sidecar`

the original defect: copy every restored sidecar whether the snapshot holds it or not

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r367.json`, row `G1_always_copy_the_restored_sidecar`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 307 against a baseline of 307
- Kills: 10 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_folder_rclone_says_is_absent_is_not_a_listing_failure[list-snapshot-contents-2026-08-01T000000Z-holds no database folder]`
  - `tests/modules/test_tools.py::test_a_named_snapshot_whose_listing_fails_sends_the_person_to_the_remote[list-snapshot-contents]`
  - `tests/modules/test_tools.py::test_a_restore_from_a_snapshot_holding_only_the_database_skips_the_absent_sidecar`
  - `tests/modules/test_tools.py::test_a_snapshot_that_cannot_be_listed_refuses_before_clearing`
  - `tests/modules/test_tools.py::test_the_snapshot_listing_is_of_the_database_folder`
  - `tests/test_restore_cli.py::test_a_live_restore_in_the_outside_layout_withholds_the_share_and_closes_clean`
  - `tests/test_restore_cli.py::test_a_restore_from_a_database_only_snapshot_names_the_absent_sidecar`
  - `tests/test_restore_cli.py::test_a_restore_in_the_outside_layout_says_whether_the_share_came_back[-pulled1-absent]`
  - `tests/test_restore_cli.py::test_a_restore_in_the_outside_layout_says_whether_the_share_came_back[PIONEER/\n-pulled0-pulled]`
  - `tests/test_restore_cli.py::test_the_verb_recovers_both_halves_and_reports_them_apart`

Old text:

```
    held = snapshot_filenames(cfg, chosen, runner=runner)
    absent: list[str] = []
    for sidecar in config.state_file("rekordbox_db").sidecars:
        if not sidecar.restored:
            continue
        name = f"{database_target.name}{sidecar.suffix}"
        if name not in held:
            absent.append(sidecar.suffix)
            continue
        commands.append(

```

New text:

```
    absent: list[str] = []
    for sidecar in config.state_file("rekordbox_db").sidecars:
        if not sidecar.restored:
            continue
        name = f"{database_target.name}{sidecar.suffix}"
        commands.append(

```

### `r367.G3_membership_is_inverted`

copy the sidecar when it is absent and skip it when it is present

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r367.json`, row `G3_membership_is_inverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 307 against a baseline of 307
- Kills: 18 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_restore_from_a_snapshot_holding_only_the_database_skips_the_absent_sidecar`
  - `tests/modules/test_tools.py::test_a_restore_from_a_snapshot_holding_the_log_copies_it`
  - `tests/modules/test_tools.py::test_restore_writes_back_the_log_and_never_the_shared_memory_index`
  - `tests/test_restore_cli.py::test_a_database_half_that_landed_part_of_the_fileset_is_refused_until_the_step`
  - `tests/test_restore_cli.py::test_a_failed_mirror_stops_the_recovery_before_the_database`
  - `tests/test_restore_cli.py::test_a_live_restore_in_the_outside_layout_withholds_the_share_and_closes_clean`
  - `tests/test_restore_cli.py::test_a_mirror_pull_with_no_session_named_is_reported_as_work_that_happened`
  - `tests/test_restore_cli.py::test_a_mirror_still_carrying_the_database_does_not_land_it`
  - `tests/test_restore_cli.py::test_a_recovery_lands_the_mirror_and_the_database_only_under_the_target`
  - `tests/test_restore_cli.py::test_a_recovery_whose_database_half_failed_reruns_with_nothing_removed`
  - `tests/test_restore_cli.py::test_a_recovery_whose_mirror_was_cut_off_reruns_with_nothing_removed`
  - `tests/test_restore_cli.py::test_a_rehearsal_passes_the_same_gates_and_writes_nothing`
  - `tests/test_restore_cli.py::test_a_restore_from_a_database_only_snapshot_names_the_absent_sidecar`
  - `tests/test_restore_cli.py::test_a_restore_in_the_outside_layout_says_whether_the_share_came_back[-pulled1-absent]`
  - `tests/test_restore_cli.py::test_a_restore_in_the_outside_layout_says_whether_the_share_came_back[PIONEER/\n-pulled0-pulled]`
  - ... and 3 more, see the JSON sidecar

Old text:

```
        if name not in held:
```

New text:

```
        if name in held:
```

### `r367.G4_the_inventory_restored_flag_is_ignored`

a listed shared memory index is written back beside a fresh log

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r367.json`, row `G4_the_inventory_restored_flag_is_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 307 against a baseline of 307
- Kills: 6 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_restore_from_a_snapshot_holding_only_the_database_skips_the_absent_sidecar`
  - `tests/modules/test_tools.py::test_a_restore_from_a_snapshot_holding_the_log_copies_it`
  - `tests/modules/test_tools.py::test_restore_writes_back_the_log_and_never_the_shared_memory_index`
  - `tests/test_restore_cli.py::test_a_mirror_pull_with_no_session_named_is_reported_as_work_that_happened`
  - `tests/test_restore_cli.py::test_a_restore_from_a_database_only_snapshot_names_the_absent_sidecar`
  - `tests/test_restore_cli.py::test_the_verb_recovers_both_halves_and_reports_them_apart`

Old text:

```
        if not sidecar.restored:
            continue

```

New text:

```
(empty)
```

### `r367.G5_absent_sidecars_are_not_recorded`

the plan copies nothing extra and also does not name what it skipped

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r367.json`, row `G5_absent_sidecars_are_not_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 307 against a baseline of 307
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_restore_from_a_snapshot_holding_only_the_database_skips_the_absent_sidecar`
  - `tests/test_restore_cli.py::test_a_restore_from_a_database_only_snapshot_names_the_absent_sidecar`
  - `tests/test_restore_cli.py::test_the_verb_recovers_both_halves_and_reports_them_apart`

Old text:

```
            absent.append(sidecar.suffix)

```

New text:

```
(empty)
```

### `r367.G7_the_listing_is_of_the_snapshot_root`

list the dated folder, not the db folder inside it, so the log is never seen

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r367.json`, row `G7_the_listing_is_of_the_snapshot_root`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 307 against a baseline of 307
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_snapshot_listing_is_of_the_database_folder`

Old text:

```
                f"{cfg.backup.db_dest_root}/{snapshot}/db/",
```

New text:

```
                f"{cfg.backup.db_dest_root}/{snapshot}/",
```

### `u138.S7_verb_drops_the_answer`

The verb never hands down who answered the gate

- File: `src/cratekit/session/cli.py`
- Source: `u138.json`, row `S7_verb_drops_the_answer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 7 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_a_person_at_a_terminal_mints_by_the_terminal_rule_and_the_record_says_so`
  - `tests/test_session_ack_by_session.py::test_a_session_with_a_terminal_is_still_held_to_the_ages`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-exactly-five]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-never-recorded]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-recorded-in-the-future]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[files-six-days]`
  - `tests/test_session_ack_by_session.py::test_the_session_mints_with_no_terminal_when_both_ages_are_under_five_days`

Old text:

```
        cfg, now=now, decided_by=answered.actor if answered is not None else None

```

New text:

```
        cfg, now=now, decided_by=None

```

### `u184.A10_summary_always_recorded`

_summary: say recorded whether or not this call minted

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A10_summary_always_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_one_command_reports_a_valid_acknowledgment_and_does_not_mint_again`

Old text:

```
        "recorded": minted,
```

New text:

```
        "recorded": True,
```

### `u184.A11_wording_swapped`

_expiry_row: swap the two phrasings, so a mint reads as already on record

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A11_wording_swapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_one_command_prints_the_expiry_a_person_reads`
  - `tests/test_session_ack_by_session.py::test_one_command_reports_a_valid_acknowledgment_and_does_not_mint_again`

Old text:

```
    said = "recorded now" if minted else "already on record, not minted again"
```

New text:

```
    said = "already on record, not minted again" if minted else "recorded now"
```

### `u184.A3_engine_rule_not_selected`

_mint_as_session: hand no actor to the engine, so the terminal rule decides and the ages are not judged

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A3_engine_rule_not_selected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 9 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_an_expired_acknowledgment_is_replaced_by_one_command`
  - `tests/test_session_ack_by_session.py::test_an_unreadable_acknowledgment_is_replaced_by_one_command`
  - `tests/test_session_ack_by_session.py::test_one_command_mints_as_the_session_when_both_ages_are_four_days`
  - `tests/test_session_ack_by_session.py::test_one_command_prints_the_expiry_a_person_reads`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[both-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[files-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_reports_a_valid_acknowledgment_and_does_not_mint_again`

Old text:

```
        cfg, now=now, decided_by=session.SESSION_ACTOR
    )
```

New text:

```
        cfg, now=now, decided_by=None
    )
```

### `u184.A4_valid_record_minted_again`

_mint_as_session: never report a valid acknowledgment, so every call mints a fresh one

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A4_valid_record_minted_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_a_valid_acknowledgment_a_person_minted_is_reported_over_old_backups`
  - `tests/test_session_ack_by_session.py::test_one_command_reports_a_valid_acknowledgment_and_does_not_mint_again`

Old text:

```
    if recorded is not None and recorded.valid_at(now):
```

New text:

```
    if False:
```

### `u184.A5_expired_reported_valid`

_mint_as_session: drop the window check, so an expired acknowledgment is reported as on record

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A5_expired_reported_valid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_an_expired_acknowledgment_is_replaced_by_one_command`

Old text:

```
    if recorded is not None and recorded.valid_at(now):
```

New text:

```
    if recorded is not None:
```

### `u184.A6_unreadable_record_refuses`

_mint_as_session: let an unreadable record raise, so a damaged file can never be replaced by the session

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A6_unreadable_record_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_an_unreadable_acknowledgment_is_replaced_by_one_command`

Old text:

```
    except CratekitError:
        recorded = None
```

New text:

```
    except CratekitError:
        raise
```

### `u184.A7_already_valid_says_ok`

_mint_as_session: report an existing acknowledgment as an ok run rather than a no op

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A7_already_valid_says_ok`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_one_command_reports_a_valid_acknowledgment_and_does_not_mint_again`

Old text:

```
                "summary": _summary(recorded, minted=False),
            },
            outcome=Outcome.NO_OP,
```

New text:

```
                "summary": _summary(recorded, minted=False),
            },
            outcome=Outcome.OK,
```

### `u184.A8_expiry_row_dropped`

_mint_as_session: leave the expiry row out of a mint, so a person at a terminal is never shown it

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A8_expiry_row_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_one_command_prints_the_expiry_a_person_reads`

Old text:

```
                _expiry_row(acknowledgment, minted=True),
```

New text:

```
(empty)
```

### `u184.A9_expiry_row_names_the_mint`

_expiry_row: name the moment recorded where the expiry belongs

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A9_expiry_row_names_the_mint`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_one_command_prints_the_expiry_a_person_reads`

Old text:

```
            f"{acknowledgment.expires_at.isoformat()}"
```

New text:

```
            f"{acknowledgment.recorded_at.isoformat()}"
```

### `u266.M1_seven_opens_again`

read_index_tags: go back to one read_tag call per field, seven opens a file, the regression the card removes

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u266.json`, row `M1_seven_opens_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_one_open.py`, `tests/test_setbuilder_cli.py`, `tests/modules/test_tools.py`
- Collected: 351 against a baseline of 351
- Kills: 52 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_the_first_run_opens_each_file_once_and_the_second_none`
  - `tests/test_setbuilder_one_open.py::test_a_file_one_open_cannot_read_reads_all_absent_and_never_raises`
  - `tests/test_setbuilder_one_open.py::test_an_undecodable_field_reads_none_and_its_neighbours_still_read`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.aif]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.aiff]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.flac]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.m4a]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.mp3]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.ogg]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.opus]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.wav]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[every-field-.aif]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[every-field-.aiff]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[every-field-.flac]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[every-field-.m4a]`
  - ... and 37 more, see the JSON sidecar

Old text:

```
    return tags.read_tags(path, INDEX_FIELDS)
```

New text:

```
    return {name: tags.read_tag(path, name) for name in INDEX_FIELDS}
```

### `u266.M2_strict_reader`

read_index_tags: read through the checked reader, so a file one open cannot read raises and aborts the walk instead of reading all absent

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u266.json`, row `M2_strict_reader`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_one_open.py`, `tests/test_setbuilder_cli.py`, `tests/modules/test_tools.py`
- Collected: 351 against a baseline of 351
- Kills: 6 (killed)
- Killed:
  - `tests/test_setbuilder_one_open.py::test_a_file_one_open_cannot_read_reads_all_absent_and_never_raises`
  - `tests/test_setbuilder_one_open.py::test_a_listed_container_no_tag_reader_handles_opens_nothing[.aac]`
  - `tests/test_setbuilder_one_open.py::test_a_listed_container_no_tag_reader_handles_opens_nothing[.alac]`
  - `tests/test_setbuilder_one_open.py::test_a_listed_container_no_tag_reader_handles_opens_nothing[.webm]`
  - `tests/test_setbuilder_one_open.py::test_an_undecodable_field_reads_none_and_its_neighbours_still_read`
  - `tests/test_setbuilder_one_open.py::test_the_index_is_what_the_seven_open_reader_built_one_open_a_file`

Old text:

```
    return tags.read_tags(path, INDEX_FIELDS)
```

New text:

```
    return tags.read_tags_checked(path, INDEX_FIELDS)
```

### `u266.M3_a_field_dropped`

read_index_tags: read every field but the last, so the vocal gender never reaches the index

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u266.json`, row `M3_a_field_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_one_open.py`, `tests/test_setbuilder_cli.py`, `tests/modules/test_tools.py`
- Collected: 351 against a baseline of 351
- Kills: 55 (killed)
- Killed:
  - `tests/test_setbuilder_one_open.py::test_a_file_one_open_cannot_read_reads_all_absent_and_never_raises`
  - `tests/test_setbuilder_one_open.py::test_a_listed_container_no_tag_reader_handles_opens_nothing[.aac]`
  - `tests/test_setbuilder_one_open.py::test_a_listed_container_no_tag_reader_handles_opens_nothing[.alac]`
  - `tests/test_setbuilder_one_open.py::test_a_listed_container_no_tag_reader_handles_opens_nothing[.webm]`
  - `tests/test_setbuilder_one_open.py::test_an_undecodable_field_reads_none_and_its_neighbours_still_read`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.aif]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.aiff]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.flac]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.m4a]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.mp3]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.ogg]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.opus]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.wav]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[every-field-.aif]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[every-field-.aiff]`
  - ... and 40 more, see the JSON sidecar

Old text:

```
    return tags.read_tags(path, INDEX_FIELDS)
```

New text:

```
    return tags.read_tags(path, INDEX_FIELDS[:-1])
```

### `u266.M4_key_order_reversed`

read_index_tags: read the fields in reverse order, the same values under a different key order

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u266.json`, row `M4_key_order_reversed`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_one_open.py`, `tests/test_setbuilder_cli.py`, `tests/modules/test_tools.py`
- Collected: 351 against a baseline of 351
- Kills: 48 (killed)
- Killed:
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.aif]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.aiff]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.flac]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.m4a]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.mp3]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.ogg]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.opus]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.wav]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[every-field-.aif]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[every-field-.aiff]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[every-field-.flac]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[every-field-.m4a]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[every-field-.mp3]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[every-field-.ogg]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[every-field-.opus]`
  - ... and 33 more, see the JSON sidecar

Old text:

```
    return tags.read_tags(path, INDEX_FIELDS)
```

New text:

```
    return tags.read_tags(path, tuple(reversed(INDEX_FIELDS)))
```

### `u266.M6_size_not_compared`

_entry_is_current: trust a cached entry without comparing the size, the sample guard on when the warm index is trusted

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u266.json`, row `M6_size_not_compared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_one_open.py`, `tests/test_setbuilder_cli.py`, `tests/modules/test_tools.py`
- Collected: 351 against a baseline of 351
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_new_bytes_under_an_old_modification_time_are_re_read`

Old text:

```
        and entry.get("size") == identity["size"]

```

New text:

```
(empty)
```

### `r349-c.C1_prune_recorded`

The prune calls the bare runner, so its commands are not recorded beside its results

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r349-c.json`, row `C1_prune_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`, `tests/modules/test_tools.py`
- Collected: 308 against a baseline of 308
- Kills: 41 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_backup_payload_carries_a_version`
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_completed_warns_about_nothing`
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_stopped_reports_it_and_is_still_a_backup`
  - `tests/test_backup_cli.py::test_a_contained_analysis_share_draws_no_warning_from_the_verb`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_half_failed_rehearsal_says_it_too_on_the_other_refusal`
  - `tests/test_backup_cli.py::test_a_library_whose_identity_cannot_be_a_marker_is_told_so`
  - `tests/test_backup_cli.py::test_a_library_with_an_identity_draws_no_such_warning`
  - `tests/test_backup_cli.py::test_a_named_portion_runs_only_its_own_half`
  - `tests/test_backup_cli.py::test_a_partial_run_succeeds_and_publishes_only_the_half_that_ran`
  - `tests/test_backup_cli.py::test_a_queued_backup_names_every_command_it_ran_in_job_show`
  - `tests/test_backup_cli.py::test_a_queued_backup_runs_every_portion_through_the_real_resume`
  - `tests/test_backup_cli.py::test_a_queued_real_backup_carries_no_rehearsal_word`
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - ... and 26 more, see the JSON sidecar

Old text:

```
                    runner=recorded,
```

New text:

```
                    runner=runner,
```

### `r349-c.C4_argv_rendered`

outcome_payload renders the label where the argv belongs

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r349-c.json`, row `C4_argv_rendered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`, `tests/modules/test_tools.py`
- Collected: 308 against a baseline of 308
- Kills: 4 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_queued_backup_names_every_command_it_ran_in_job_show`
  - `tests/test_backup_cli.py::test_a_rehearsal_s_outcome_is_recorded_and_says_it_was_one`
  - `tests/test_backup_cli.py::test_every_command_the_engine_ran_is_paired_with_its_own_return_code`

Old text:

```
                        "argv": list(command.argv),
```

New text:

```
                        "argv": [command.label],
```

### `u181.E2_direct_reference_drops_extras`

extras.install_command: the direct reference names only the extra asked for, dropping the ones the copy carries

- File: `src/cratekit/modules/extras.py`
- Source: `u181.json`, row `E2_direct_reference_drops_extras`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_install_command.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_install_command.py::test_a_release_install_pipx_recorded_as_a_direct_reference_keeps_it_and_its_extras`

Old text:

```
            name, chosen, url = reference
            wanted = ",".join(sorted({*chosen, extras}))
```

New text:

```
            name, chosen, url = reference
            wanted = ",".join(sorted({extras}))
```

### `u27-reports-round-2.S5b_engine_default_drift`

Drift the engine's own copy of the handler key away from the registry's

- File: `src/cratekit/modules/reports/duplicates.py`
- Source: `u27-reports-round-2.json`, row `S5b_engine_default_drift`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports.py`, `tests/test_reports_cli.py`
- Collected: 382 against a baseline of 382
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_reports.py::test_every_item_carries_the_handler_key_the_registry_declares`
  - `tests/modules/test_reports.py::test_the_declared_handler_key_is_the_one_the_registry_carries`
  - `tests/test_reports_cli.py::test_the_two_copies_of_the_duplicate_handler_key_cannot_drift`

Old text:

```
HANDLER_KEY = "audit.duplicates"
```

New text:

```
HANDLER_KEY = "duplicates.audit"
```

### `u48-author.P3_two_codes_collapsed_to_one`

One code over both conditions, which is the discriminator this unit split

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u48-author.json`, row `P3_two_codes_collapsed_to_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reserved_causes.py`
- Collected: 229 against a baseline of 229
- Kills: 2 (killed)
- Killed:
  - `tests/test_reserved_causes.py::test_pinned_populations_derive_totals_and_key_by_module`
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`

Old text:

```
ARCHIVE_PURGE_FAILED = "archive-purge-failed"
```

New text:

```
ARCHIVE_PURGE_FAILED = "archive-listing-failed"
```

