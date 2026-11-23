# Mutation table: u325-after-l-24-rest

Measured by `scripts/mutate.py` on 2026-11-23 05:54 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 144.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-23 05:54 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 21, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u212.S1_missing_ends` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 334 | 1 | killed |
| `u212.S2_download_refused_all` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 22933 | 0 (promoted) | zero |
| `u212.S3_no_list_download` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 22933 | 0 (promoted) | zero |
| `u212.S4_staged_said` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 334 | 1 | killed |
| `r836-a.A1_product_made_asked_first` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 22933 | 3 (promoted) | killed |
| `r836-a.A4_no_video_declared` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 501 | 1 | killed |
| `r836-a.A5_removal_never_retried` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 501 | 1 | killed |
| `u181.C1_unscored_head_or_score` | `src/cratekit/vocals/cli.py` | user | 1 file(s) | 34 | 3 | killed |
| `u181.C2_unscored_ignores_score` | `src/cratekit/vocals/cli.py` | user | 1 file(s) | 34 | 3 | killed |
| `u25.G6_always_rewrite` | `src/cratekit/vocals/cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `u93-recursive-analysis.D23_vocals_resume_warning` | `src/cratekit/vocals/cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `u93-recursive-analysis.D25_vocals_join` | `src/cratekit/vocals/cli.py` | maintainer | 1 file(s) | 34 | 1 | killed |
| `u181.T3_rescore_keeps_stale` | `src/cratekit/cli/tail.py` | user | 1 file(s) | 34 | 1 | killed |
| `u181.T4_rescore_failure_ignored` | `src/cratekit/cli/tail.py` | user | 1 file(s) | 34 | 1 | killed |
| `u213.M21_first_group_version_check` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 778 | 6 | killed |
| `u213.M22_names_a_version_last_word` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 778 | 2 | killed |
| `r1056.N10_pass_not_required` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `r1056.N1_no_refusal_of_an_unreadable_record` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 33 | 7 | killed |
| `r1056.N2_first_landing_only` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `r1056.N3_years_from_the_argument` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `r1056.N4_no_landings_in_digest` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 33 | 2 | killed |
| `r1056.N5_no_reread_before_rename` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `r1056.N8_shown_pass_bare` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `r1056.N9_verb_not_threaded` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 33 | 6 | killed |
| `r758-a.W1_marker_not_judged` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 324 | 75 | killed |
| `r758-a.W2_asked_table_not_held_to_the_set` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 324 | 33 | killed |
| `r758-a.W3_ask_outside_the_set_not_refused` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 324 | 33 | killed |
| `r758-a.W7_removed_row_marked_again` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 324 | 1 | killed |
| `u140.B10_queued_day_name_dropped` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 29 | 2 | killed |
| `u140.B7_twin_refusal_dropped` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 29 | 4 | killed |
| `u140.B8_flag_conflict_dropped` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 29 | 1 | killed |
| `u140.B9_abort_applies` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 29 | 1 | killed |
| `u140.B3_refreeze_any_state` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 29 | 1 | killed |
| `u140.B4_refreeze_writes_nothing_new` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 29 | 7 | killed |
| `u140.B1_ledger_folds_into_a_twin` | `src/cratekit/modules/outbound/ledger.py` | user | 1 file(s) | 29 | 1 | killed |
| `u140.B2_ledger_moves_another_id` | `src/cratekit/modules/outbound/ledger.py` | user | 1 file(s) | 29 | 1 | killed |
| `r381-b.M14_follow_all_renames` | `src/cratekit/label/marks.py` | user | 2 file(s) | 208 | 1 | killed |
| `r381.M13_follow_overwrites` | `src/cratekit/label/marks.py` | user | 2 file(s) | 208 | 1 | killed |
| `r381.M15_read_does_not_persist` | `src/cratekit/label/marks.py` | user | 2 file(s) | 208 | 1 | killed |
| `r381.M16_advance_does_not_follow` | `src/cratekit/label/marks.py` | user | 2 file(s) | 208 | 1 | killed |
| `r381.M17_read_no_follow` | `src/cratekit/label/marks.py` | user | 2 file(s) | 208 | 1 | killed |
| `u157.L2_blocked_unnamed` | `src/cratekit/intake/land_cli.py` | user | 3 file(s) | 129 | 1 | killed |
| `u157.N1_writable_unasked` | `src/cratekit/intake/native.py` | user | 3 file(s) | 129 | 1 | killed |
| `u157.N2_digest_rows` | `src/cratekit/intake/native.py` | user | 3 file(s) | 129 | 1 | killed |
| `u157.N3_no_write` | `src/cratekit/intake/native.py` | user | 3 file(s) | 129 | 5 | killed |
| `u157.N4_trust_the_writer` | `src/cratekit/intake/native.py` | user | 3 file(s) | 129 | 1 | killed |
| `u157.N5_no_record` | `src/cratekit/intake/native.py` | user | 3 file(s) | 129 | 1 | killed |
| `r349-b.B3_clear_before_attempt` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `r349-b.B4_stage_error_completes` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `r349-c.C2_write_failure_step` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `r757-c1.S3_work_body_plans_fast` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `r746-a.G7_sql_value_check_disarmed` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `r746-d.G5_content_row_read_back_against_five_not_ten` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u263.D20_energy_load` | `src/cratekit/analysis/energy.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u126.M1_half_is_a_majority` | `src/cratekit/write/row_link.py` | user | 2 file(s) | 118 | 2 | killed |
| `u126.M2_plurality` | `src/cratekit/write/row_link.py` | user | 2 file(s) | 118 | 3 | killed |
| `u126.M3_dead_rows_count` | `src/cratekit/write/row_link.py` | user | 2 file(s) | 118 | 2 | killed |
| `u126.M4_least_common_first` | `src/cratekit/write/row_link.py` | user | 2 file(s) | 118 | 3 | killed |
| `u126.M5_null_is_a_value` | `src/cratekit/write/row_link.py` | user | 2 file(s) | 118 | 3 | killed |
| `u126.M6_any_text` | `src/cratekit/write/row_link.py` | user | 2 file(s) | 118 | 2 | killed |
| `u282.C1_refused_token_not_counted` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 435 | 1 | killed |
| `u282.C2_refused_token_not_warned` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 435 | 1 | killed |
| `u282.C3_label_genre_counted_as_owed` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 435 | 1 | killed |
| `u293.L1_dead_mark_charged` | `src/cratekit/core/night_budget.py` | user | 2 file(s) | 103 | 3 | killed |
| `u293.L2_night_reset` | `src/cratekit/core/night_budget.py` | user | 2 file(s) | 103 | 4 | killed |
| `u293.L3_spent_off_by_one` | `src/cratekit/core/night_budget.py` | user | 2 file(s) | 103 | 2 | killed |
| `u293.L4_noon_to_noon` | `src/cratekit/core/night_budget.py` | user | 2 file(s) | 103 | 3 | killed |
| `u293.L5_close_adds_to_night` | `src/cratekit/core/night_budget.py` | user | 2 file(s) | 103 | 1 | killed |
| `u293.L6_unreadable_gate_refuses` | `src/cratekit/core/night_budget.py` | user | 2 file(s) | 103 | 1 | killed |
| `u190.T1_run_folder_absolute` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 275 | 1 | killed |
| `u190.T3_stale_matches_folder` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 275 | 1 | killed |
| `u190.T4_name_answers_inline` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 275 | 2 | killed |
| `u190.T6_chain_namespace` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 275 | 3 | killed |
| `u227.R15_way_on_wording` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 96 | 1 | killed |
| `u227.R19_take_library` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 96 | 1 | killed |
| `u227.R20_take_source` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 96 | 2 | killed |
| `u227.R21_take_continued` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 96 | 1 | killed |
| `u227.R22_take_not_driven` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 96 | 1 | killed |
| `u227.R25_way_on_state` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 96 | 1 | killed |
| `u111-c.C3_inboxed_suffix` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 41 | 3 | killed |
| `u111-c.C4_removal_threshold` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 41 | 2 | killed |
| `u111-c.C5_move_threshold` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 41 | 3 | killed |
| `u111-c.C6_plan_taken_again` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 41 | 1 | killed |
| `u111-c.C7_old_creation_planned` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 41 | 2 | killed |
| `u111-d.C10_two_olds_refused` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 41 | 1 | killed |
| `u111-d.C9_committed_records_only` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 41 | 1 | killed |
| `r1372.K19_passed_by_strict` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 1 | killed |
| `r1372.K20_passed_by_any_pair` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 1 | killed |
| `r1372.K21_made_pair_unmapped` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 2 | killed |
| `r1376.F14_finished_filter_gone` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 1 | killed |
| `u225.M8_reached_strict_membership` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 3 | killed |
| `u225.M9_finish_ignored` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 3 | killed |
| `u284.R1_since_moves_every_refusal` | `src/cratekit/tagging/refused.py` | user | 1 file(s) | 35 | 3 | killed |
| `u284.R2_an_answer_never_clears` | `src/cratekit/tagging/refused.py` | user | 1 file(s) | 35 | 2 | killed |
| `u284.R3_write_without_the_lock` | `src/cratekit/tagging/refused.py` | maintainer | 1 file(s) | 35 | 1 | killed |
| `u284.R4_empty_since_read` | `src/cratekit/tagging/refused.py` | maintainer | 1 file(s) | 35 | 1 | killed |
| `u284.R5_count_never_grows` | `src/cratekit/tagging/refused.py` | maintainer | 1 file(s) | 35 | 2 | killed |
| `u284.R6_write_failure_raises` | `src/cratekit/tagging/refused.py` | user | 1 file(s) | 35 | 1 | killed |
| `u284.R7_deep_record_raises` | `src/cratekit/tagging/refused.py` | user | 1 file(s) | 35 | 1 | killed |
| `u78-a.A3_several_listed` | `src/cratekit/intake/missing_cli.py` | user | 2 file(s) | 88 | 3 | killed |
| `u78-a.A5_outage_read_as_none` | `src/cratekit/intake/missing_cli.py` | user | 2 file(s) | 88 | 1 | killed |
| `u78-a.A6_blank_id_dropped` | `src/cratekit/intake/missing_cli.py` | user | 2 file(s) | 88 | 1 | killed |
| `u78-b.B1_unwritable_refuses_whole` | `src/cratekit/intake/missing_cli.py` | user | 2 file(s) | 88 | 2 | killed |
| `u78-b.B3_ids_unsorted` | `src/cratekit/intake/missing_cli.py` | user | 2 file(s) | 88 | 1 | killed |
| `u78-d.A4_cratekit_error_passthrough_again` | `src/cratekit/intake/missing_cli.py` | user | 2 file(s) | 88 | 1 | killed |
| `u169.E1_declined_accepts_retryable` | `src/cratekit/core/jobs.py` | user | 2 file(s) | 151 | 2 | killed |
| `u169.E2_drive_fails_a_decline` | `src/cratekit/core/jobs.py` | user | 2 file(s) | 151 | 11 | killed |
| `u169.E3_decline_writes_failed` | `src/cratekit/core/jobs.py` | user | 2 file(s) | 151 | 10 | killed |
| `u169.E4_decline_drops_cause` | `src/cratekit/core/jobs.py` | user | 2 file(s) | 151 | 10 | killed |
| `u169.E6_failed_cause_hides_declines` | `src/cratekit/core/jobs.py` | user | 2 file(s) | 151 | 1 | killed |
| `u42-author-round-2.C2_unknown_defaults_lossless` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 1 | killed |
| `u42-author.C1_undecided_derived` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 3 | killed |

## Zero rows and what they owe

- `u212.S2_download_refused_all` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u212.S3_no_list_download` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r349-b.B3_clear_before_attempt` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r349-b.B4_stage_error_completes` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r349-c.C2_write_failure_step` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r757-c1.S3_work_body_plans_fast` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r746-a.G7_sql_value_check_disarmed` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r746-d.G5_content_row_read_back_against_five_not_ten` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u263.D20_energy_load` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `u212.S1_missing_ends`

sync_land._missing: nothing listed ends the pass whatever is staged

- File: `src/cratekit/cli/sync_land.py`
- Source: `u212.json`, row `S1_missing_ends`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_crate_sync_skill.py`, `tests/test_inbox_analyzed.py`, `tests/test_rekordbox_visit_skill.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`
- Collected: 334 against a baseline of 334
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_staged.py::test_a_pass_whose_every_missing_track_is_staged_downloads_nothing_and_refuses`

Old text:

```
    if (envelope.get("outcome") == str(Outcome.NO_OP) or not listed) and not staged:
```

New text:

```
    if envelope.get("outcome") == str(Outcome.NO_OP) or not listed:
```

### `u212.S2_download_refused_all`

sync_land._download: a download that landed nothing ends the pass whatever is staged, round one's F1

- File: `src/cratekit/cli/sync_land.py`
- Source: `u212.json`, row `S2_download_refused_all`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_crate_sync_skill.py`, `tests/test_inbox_analyzed.py`, `tests/test_rekordbox_visit_skill.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if not listed.staged:
            raise _Done(DOWNLOAD)
        return 0
    report.check(
```

New text:

```
        raise _Done(DOWNLOAD)
    report.check(
```

### `u212.S3_no_list_download`

sync_land._download: no early return for a pass with no list, so it asks the download verb for a list that is not there

- File: `src/cratekit/cli/sync_land.py`
- Source: `u212.json`, row `S3_no_list_download`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_crate_sync_skill.py`, `tests/test_inbox_analyzed.py`, `tests/test_rekordbox_visit_skill.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if listed.path is None:
        report.check(DOWNLOAD, "info", "nothing downloaded: every missing track is staged already")
        return 0
```

New text:

```
(empty)
```

### `u212.S4_staged_said`

sync_land._missing: the missing row drops the staged clause, so the pass does not say how many it skipped

- File: `src/cratekit/cli/sync_land.py`
- Source: `u212.json`, row `S4_staged_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_crate_sync_skill.py`, `tests/test_inbox_analyzed.py`, `tests/test_rekordbox_visit_skill.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`
- Collected: 334 against a baseline of 334
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_staged.py::test_a_second_pass_beside_the_unlanded_first_lists_only_what_it_did_not_stage_and_refuses`

Old text:

```
        + (f"; {staged} more {held}" if staged else ""),
```

New text:

```
        + "",
```

### `r836-a.A1_product_made_asked_first`

tidal_account.remove_tracks: the ledger is never asked, so a playlist the product did not create loses tracks

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r836-a.json`, row `A1_product_made_asked_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_export_collection.py`
- Collected: 22933 against a baseline of 22933
- Kills: 3 (killed)
- Promoted: subset killed 0, full suite killed 3
- Killed:
  - `tests/test_label_heard.py::test_the_adapter_refuses_a_playlist_the_ledger_does_not_vouch_for_unasked`
  - `tests/test_organize_root.py::test_the_generic_removal_still_refuses_an_unrecorded_playlist`
  - `tests/test_sync_pair_account.py::test_a_paired_playlist_is_never_removed_whole`

Old text:

```
        if self._cfg is None or not ledger.product_made(self._cfg, identifier):
```

New text:

```
        if False:
```

### `r836-a.A4_no_video_declared`

tidal_account._positions: a playlist holding a video is read by track position, which the item removal does not use

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r836-a.json`, row `A4_no_video_declared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_export_collection.py`
- Collected: 501 against a baseline of 501
- Kills: 1 (killed)
- Killed:
  - `tests/test_prune.py::test_a_playlist_holding_a_video_is_refused_with_nothing_sent`

Old text:

```
            or videos != 0
```

New text:

```
(empty)
```

### `r836-a.A5_removal_never_retried`

tidal_account.remove_tracks: a removal by position is retried once, so a request that landed and timed out takes off whatever moved up

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r836-a.json`, row `A5_removal_never_retried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_export_collection.py`
- Collected: 501 against a baseline of 501
- Kills: 1 (killed)
- Killed:
  - `tests/test_prune.py::test_a_removal_the_provider_refuses_once_is_never_sent_again`

Old text:

```
                doing, lambda at=at, playlist=playlist: playlist.remove_by_indices(at), retries=0
```

New text:

```
                doing, lambda at=at, playlist=playlist: playlist.remove_by_indices(at)
```

### `u181.C1_unscored_head_or_score`

analyze vocals --unscored: queue a file carrying the head OR no score, so an unheaded file is queued

- File: `src/cratekit/vocals/cli.py`
- Source: `u181.json`, row `C1_unscored_head_or_score`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`
- Collected: 34 against a baseline of 34
- Kills: 3 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_the_tails_rescore_scores_a_headed_file_with_no_score_and_leaves_a_scored_one`
  - `tests/test_vocals_cli.py::test_unscored_over_a_folder_whose_headed_files_all_carry_a_score_queues_nothing`
  - `tests/test_vocals_cli.py::test_unscored_queues_a_headed_file_with_no_score_and_leaves_the_rest_alone`

Old text:

```
        if analysis_cli.carries_head(path, cfg) and tags.read_vox_from_file(path) is None:
```

New text:

```
        if analysis_cli.carries_head(path, cfg) or tags.read_vox_from_file(path) is None:
```

### `u181.C2_unscored_ignores_score`

analyze vocals --unscored: queue every headed file, scored or not

- File: `src/cratekit/vocals/cli.py`
- Source: `u181.json`, row `C2_unscored_ignores_score`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`
- Collected: 34 against a baseline of 34
- Kills: 3 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_the_tails_rescore_scores_a_headed_file_with_no_score_and_leaves_a_scored_one`
  - `tests/test_vocals_cli.py::test_unscored_over_a_folder_whose_headed_files_all_carry_a_score_queues_nothing`
  - `tests/test_vocals_cli.py::test_unscored_queues_a_headed_file_with_no_score_and_leaves_the_rest_alone`

Old text:

```
        if analysis_cli.carries_head(path, cfg) and tags.read_vox_from_file(path) is None:
```

New text:

```
        if analysis_cli.carries_head(path, cfg):
```

### `u25.G6_always_rewrite`

Rewrite vocal tags even when the values did not move

- File: `src/cratekit/vocals/cli.py`
- Source: `u25.json`, row `G6_always_rewrite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_an_unchanged_score_is_not_rewritten`

Old text:

```
    if (previous_level, previous_gender, previous_conf) != (level, gender, conf):
        _write_or_refuse(

```

New text:

```
    if True or (previous_level, previous_gender, previous_conf) != (level, gender, conf):
        _write_or_refuse(

```

### `u93-recursive-analysis.D23_vocals_resume_warning`

The vocals resume drops the walk's omissions, the same hole on the other verb

- File: `src/cratekit/vocals/cli.py`
- Source: `u93-recursive-analysis.json`, row `D23_vocals_resume_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_the_vocals_resume_repeats_what_the_walk_left_out`

Old text:

```
        warnings = (*warnings, *discovery.warnings_of(job.payload))
        unscored = _unscored_warning(summary)
```

New text:

```
        unscored = _unscored_warning(summary)
```

### `u93-recursive-analysis.D25_vocals_join`

The vocals worker joins with the operator, the same reversion one file over

- File: `src/cratekit/vocals/cli.py`
- Source: `u93-recursive-analysis.json`, row `D25_vocals_join`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_a_vocals_item_that_would_leave_the_frozen_folder_is_refused`

Old text:

```
    return folder, discovery.item_path(folder, str(item.item_id))
```

New text:

```
    return folder, folder / item.item_id
```

### `u181.T3_rescore_keeps_stale`

tail.rescore: leave a stale vocals job over the folder open

- File: `src/cratekit/cli/tail.py`
- Source: `u181.json`, row `T3_rescore_keeps_stale`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_the_tails_rescore_replaces_a_stale_vocals_job_over_the_folder`

Old text:

```
        replace_stale(chain, ANALYZE, VOCALS_VERB, folder, cfg)
```

New text:

```
        pass
```

### `u181.T4_rescore_failure_ignored`

tail.rescore: a vocals job that did not succeed is reported scored and the chain goes on

- File: `src/cratekit/cli/tail.py`
- Source: `u181.json`, row `T4_rescore_failure_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_a_rescore_job_that_does_not_succeed_ends_the_chain_at_the_analyze_step`

Old text:

```
    if job.state is not jobs.JobState.SUCCEEDED:
        raise Stop(ANALYZE, job_error(chain, job))
    chain.summary["vocal_rescore"] = count
```

New text:

```
    chain.summary["vocal_rescore"] = count
```

### `u213.M21_first_group_version_check`

split_version: drop the version check from the first group rule, so a row titled only (Extended) reads as the title Extended and the emitter writes it

- File: `src/cratekit/acquire/match.py`
- Source: `u213.json`, row `M21_first_group_version_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_listdoc.py`, `tests/intake/test_workers.py`
- Collected: 778 against a baseline of 778
- Kills: 6 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_row_the_reader_would_refuse_is_refused_by_the_emitter[only-a-version]`
  - `tests/test_match_states.py::test_a_provider_row_titled_wholly_in_brackets_reads_rather_than_refuses`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(Extended)-expected14]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(Without You Remix)-expected11]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[Original Mix] (Remastered)-expected15]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[Premade Sandwiches Live]-expected16]`

Old text:

```
        if found.start() == 0 and not _names_a_version(inside):
```

New text:

```
        if found.start() == 0:
```

### `u213.M22_names_a_version_last_word`

_names_a_version: read the group's first word rather than its last

- File: `src/cratekit/acquire/match.py`
- Source: `u213.json`, row `M22_names_a_version_last_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_listdoc.py`, `tests/intake/test_workers.py`
- Collected: 778 against a baseline of 778
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(Without You Remix)-expected11]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[Premade Sandwiches Live]-expected16]`

Old text:

```
    return bool(words) and words[-1] in _DASH_VERSIONS
```

New text:

```
    return bool(words) and words[0] in _DASH_VERSIONS
```

### `r1056.N10_pass_not_required`

build_mark: neither --xml nor --pass required, so a bare mark reaches the handler

- File: `src/cratekit/label/mark_cli.py`
- Source: `r1056.json`, row `N10_pass_not_required`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_the_pass_is_named_by_exactly_one_of_the_file_and_the_name[neither]`

Old text:

```
    proof = parser.add_mutually_exclusive_group(required=True)
```

New text:

```
    proof = parser.add_mutually_exclusive_group(required=False)
```

### `r1056.N1_no_refusal_of_an_unreadable_record`

native_years: read a record this build cannot read as one that filed nothing

- File: `src/cratekit/label/mark_cli.py`
- Source: `r1056.json`, row `N1_no_refusal_of_an_unreadable_record`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_record_naming_its_filing_in_a_form_this_build_cannot_read_is_refused[a-bool-tracks]`
  - `tests/test_label_mark_native.py::test_a_record_naming_its_filing_in_a_form_this_build_cannot_read_is_refused[a-bool-year]`
  - `tests/test_label_mark_native.py::test_a_record_naming_its_filing_in_a_form_this_build_cannot_read_is_refused[a-list-of-strings]`
  - `tests/test_label_mark_native.py::test_a_record_naming_its_filing_in_a_form_this_build_cannot_read_is_refused[a-string]`
  - `tests/test_label_mark_native.py::test_a_record_naming_its_filing_in_a_form_this_build_cannot_read_is_refused[a-text-year]`
  - `tests/test_label_mark_native.py::test_a_record_naming_its_filing_in_a_form_this_build_cannot_read_is_refused[no-label]`
  - `tests/test_label_mark_native.py::test_a_record_naming_its_filing_in_a_form_this_build_cannot_read_is_refused[no-tracks]`

Old text:

```
        if filed is None:
            raise _blocked(
```

New text:

```
        if filed is None:
            filed = frozenset()
        if False:
            raise _blocked(
```

### `r1056.N2_first_landing_only`

native_years: read only the first landing the proof names, so a pass landed twice loses the second's years

- File: `src/cratekit/label/mark_cli.py`
- Source: `r1056.json`, row `N2_first_landing_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_every_committed_landing_of_the_pass_counts_and_no_other_does`

Old text:

```
    for session_id in proof.landings:
```

New text:

```
    for session_id in proof.landings[:1]:
```

### `r1056.N3_years_from_the_argument`

label_mark: read the native years under the name given on the command line, not the registry's name

- File: `src/cratekit/label/mark_cli.py`
- Source: `r1056.json`, row `N3_years_from_the_argument`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_label_named_by_its_registry_identifier_is_compared_under_its_name`

Old text:

```
native_years(cfg, native, label)
```

New text:

```
native_years(cfg, native, name)
```

### `r1056.N4_no_landings_in_digest`

_payload: leave the landings out of the native digest, so a landing after the answer is not stale

- File: `src/cratekit/label/mark_cli.py`
- Source: `r1056.json`, row `N4_no_landings_in_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_landing_of_the_pass_after_the_answer_makes_it_stale`
  - `tests/test_label_mark_native.py::test_the_gate_digest_names_the_landings`

Old text:

```
        identity["landings"] = list(native.landings)
```

New text:

```
        pass
```

### `r1056.N5_no_reread_before_rename`

label_mark: drop the reread of the native proof before the first rename

- File: `src/cratekit/label/mark_cli.py`
- Source: `r1056.json`, row `N5_no_reread_before_rename`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_landing_between_the_plan_and_the_first_rename_renames_nothing`

Old text:

```
    if native is not None and native_proof(cfg, pass_name, verb=_VERB, named=_NAMED) != native:
```

New text:

```
    if False:
```

### `r1056.N8_shown_pass_bare`

_shown: name the native pass with no word that it landed on the database native tree

- File: `src/cratekit/label/mark_cli.py`
- Source: `r1056.json`, row `N8_shown_pass_bare`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_native_pass_marks_exactly_the_years_its_landing_filed`

Old text:

```
            else f"{pass_name}, landed on the database native {native.tree_id!r} tree"
```

New text:

```
            else pass_name
```

### `r1056.N9_verb_not_threaded`

label_mark: prove the pass with sync mark's own wording, so a refusal names sync mark and intake missing

- File: `src/cratekit/label/mark_cli.py`
- Source: `r1056.json`, row `N9_verb_not_threaded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_landing_between_the_plan_and_the_first_rename_renames_nothing`
  - `tests/test_label_mark_native.py::test_a_pass_no_closed_committed_native_landing_names_is_refused_by_name[abandoned]`
  - `tests/test_label_mark_native.py::test_a_pass_no_closed_committed_native_landing_names_is_refused_by_name[another-pass]`
  - `tests/test_label_mark_native.py::test_a_pass_no_closed_committed_native_landing_names_is_refused_by_name[never-committed]`
  - `tests/test_label_mark_native.py::test_a_pass_no_closed_committed_native_landing_names_is_refused_by_name[no-landing]`
  - `tests/test_label_mark_native.py::test_an_unreachable_library_names_label_mark_as_the_verb_to_run_again`

Old text:

```
        native = native_proof(cfg, str(ctx.args.pass_name), verb=_VERB, named=_NAMED)
```

New text:

```
        native = native_proof(cfg, str(ctx.args.pass_name))
```

### `r758-a.W1_marker_not_judged`

the guard stops judging a changed soft delete marker, so any writer removes a row in any table with the guard saying nothing

- File: `src/cratekit/core/rb_writer.py`
- Source: `r758-a.json`, row `W1_marker_not_judged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_adopt_move.py`
- Collected: 324 against a baseline of 324
- Kills: 75 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_an_admitted_commit_refuses_a_removed_collection_row`
  - `tests/test_adopt_move.py::test_an_ordinary_guarded_commit_refuses_a_removal_and_rolls_it_back`
  - `tests/test_adopt_move.py::test_the_additive_membership_writer_refuses_a_removal_in_its_session`
  - `tests/test_adopt_move.py::test_the_moves_own_first_commit_refuses_a_removal`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[cloudAgentRegistry]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[contentActiveCensor]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[contentCue]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[contentFile]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[djmdActiveCensor]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[djmdAlbum]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[djmdArtist]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[djmdCategory]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[djmdColor]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[djmdContent]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[djmdCue]`
  - ... and 60 more, see the JSON sidecar

Old text:

```
        if SOFT_DELETE_COLUMN in columns and table not in admitted:
            violations.append(
```

New text:

```
        if SOFT_DELETE_COLUMN in columns and table not in admitted and table == "":
            violations.append(
```

### `r758-a.W2_asked_table_not_held_to_the_set`

a commit that asks for a removal in any table is admitted it, the refusal of the ask left standing

- File: `src/cratekit/core/rb_writer.py`
- Source: `r758-a.json`, row `W2_asked_table_not_held_to_the_set`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_adopt_move.py`
- Collected: 324 against a baseline of 324
- Kills: 33 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[cloudAgentRegistry]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[contentActiveCensor]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[contentCue]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[contentFile]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdActiveCensor]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdAlbum]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdArtist]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdCategory]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdColor]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdContent]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdCue]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdDevice]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdGenre]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdHistory]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdHotCueBanklist]`
  - ... and 18 more, see the JSON sidecar

Old text:

```
    admitted &= REMOVABLE_TABLES

```

New text:

```
(empty)
```

### `r758-a.W3_ask_outside_the_set_not_refused`

asking for a removal outside the removable set is no longer itself a violation, the intersection left standing

- File: `src/cratekit/core/rb_writer.py`
- Source: `r758-a.json`, row `W3_ask_outside_the_set_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_adopt_move.py`
- Collected: 324 against a baseline of 324
- Kills: 33 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[cloudAgentRegistry]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[contentActiveCensor]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[contentCue]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[contentFile]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdActiveCensor]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdAlbum]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdArtist]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdCategory]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdColor]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdContent]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdCue]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdDevice]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdGenre]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdHistory]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdHotCueBanklist]`
  - ... and 18 more, see the JSON sidecar

Old text:

```
    for table in sorted(admitted - REMOVABLE_TABLES):
```

New text:

```
    for table in sorted(admitted - admitted):
```

### `r758-a.W7_removed_row_marked_again`

remove_memberships marks a row that is already removed and reports it, so a second removal counts a row it did not remove

- File: `src/cratekit/core/rb_writer.py`
- Source: `r758-a.json`, row `W7_removed_row_marked_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_adopt_move.py`
- Collected: 324 against a baseline of 324
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_removed_membership_is_not_held_and_not_present`

Old text:

```
        if key not in wanted or membership_removed(song):
```

New text:

```
        if key not in wanted:
```

### `u140.B10_queued_day_name_dropped`

_names_for_job stops giving the queued day's form, which is the name the Signal set was exported under

- File: `src/cratekit/export/set_cli.py`
- Source: `u140.json`, row `B10_queued_day_name_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_backfill_after_the_rename_plans_no_twin_and_a_named_export_adds_to_it`
  - `tests/test_export_set_rename.py::test_a_job_with_no_frozen_name_is_found_by_the_queued_day_and_refrozen`

Old text:

```
    if landing is not None and landing != posted:
        found.append(set_name(set_playlist.playlist_name(words, on=landing)))

```

New text:

```
    if False:
        found.append(set_name(set_playlist.playlist_name(words, on=landing)))

```

### `u140.B7_twin_refusal_dropped`

plan_rename names the twin and goes on to adopt the record under the new name

- File: `src/cratekit/export/set_cli.py`
- Source: `u140.json`, row `B7_twin_refusal_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 4 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_twin_under_the_new_name_is_refused_rather_than_adopted`
  - `tests/test_export_set_rename.py::test_a_twin_under_the_new_name_still_refuses_when_the_landing_names_the_old`
  - `tests/test_export_set_rename.py::test_the_frozen_name_ranks_ahead_of_the_landing_record`
  - `tests/test_export_set_rename.py::test_two_playlists_under_two_older_names_are_a_twin_not_a_choice`

Old text:

```
    if planned.twin is not None:

```

New text:

```
    if False:

```

### `u140.B8_flag_conflict_dropped`

export set --rename accepts a tracklist or --name beside it

- File: `src/cratekit/export/set_cli.py`
- Source: `u140.json`, row `B8_flag_conflict_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_rename_with_a_tracklist_or_name_is_refused_before_anything`

Old text:

```
    if ctx.args.tracklist is not None or ctx.args.name is not None:

```

New text:

```
    if False:

```

### `u140.B9_abort_applies`

the rename writes when the gate was answered abort

- File: `src/cratekit/export/set_cli.py`
- Source: `u140.json`, row `B9_abort_applies`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_an_aborted_rename_writes_nothing`

Old text:

```
    option = ctx.gate.require(gate, plan=built.payload, context=built.shown)
    if option != "apply" or not built.writes:

```

New text:

```
    option = ctx.gate.require(gate, plan=built.payload, context=built.shown)
    if not built.writes:

```

### `u140.B3_refreeze_any_state`

jobs.refreeze drops the succeeded state check, so a job that may still run is rewritten

- File: `src/cratekit/core/jobs.py`
- Source: `u140.json`, row `B3_refreeze_any_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_refreeze_refuses_a_job_that_has_not_succeeded`

Old text:

```
        if current.state is not JobState.SUCCEEDED:
            raise refuse(
                "internal-error",
                f"job {job_id} is {current.state}, and only a succeeded job's frozen "

```

New text:

```
        if False:
            raise refuse(
                "internal-error",
                f"job {job_id} is {current.state}, and only a succeeded job's frozen "

```

### `u140.B4_refreeze_writes_nothing_new`

jobs.refreeze writes the payload back without the new value

- File: `src/cratekit/core/jobs.py`
- Source: `u140.json`, row `B4_refreeze_writes_nothing_new`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 7 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_job_whose_page_words_differ_renames_by_the_name_its_landing_recorded`
  - `tests/test_export_set_rename.py::test_a_job_with_no_frozen_name_is_found_by_the_queued_day_and_refrozen`
  - `tests/test_export_set_rename.py::test_a_ledger_left_under_the_old_key_is_moved_on_the_next_run`
  - `tests/test_export_set_rename.py::test_a_name_with_a_slash_freezes_as_the_library_spells_it`
  - `tests/test_export_set_rename.py::test_a_rename_that_failed_after_the_account_finishes_on_the_next_run`
  - `tests/test_export_set_rename.py::test_a_renamed_inspiration_playlist_renames_the_account_playlist_ledger_and_job`
  - `tests/test_export_set_rename.py::test_a_second_rename_is_a_no_op`

Old text:

```
        payload[key] = str(value)

```

New text:

```
        payload.setdefault(key, str(value))

```

### `u140.B1_ledger_folds_into_a_twin`

rename_set_playlist drops its refusal when the new name already holds another playlist

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u140.json`, row `B1_ledger_folds_into_a_twin`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_the_ledger_refuses_to_fold_a_rename_into_another_playlist`

Old text:

```
        if held:
            raise _unusable(

```

New text:

```
        if False:
            raise _unusable(

```

### `u140.B2_ledger_moves_another_id`

rename_set_playlist drops its refusal when the old name records a different playlist

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u140.json`, row `B2_ledger_moves_another_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_the_ledger_refuses_to_fold_a_rename_into_another_playlist`

Old text:

```
        if recorded != remote_id:

```

New text:

```
        if False:

```

### `r381-b.M14_follow_all_renames`

marks follows every recorded move, including one whose old identifier is held again

- File: `src/cratekit/label/marks.py`
- Source: `r381-b.json`, row `M14_follow_all_renames`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_slug.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_slug.py::test_a_stored_move_whose_old_identifier_is_held_is_not_followed`

Old text:

```
        renamed = registry.RegistryStore().load().live_renames()
```

New text:

```
        renamed = registry.RegistryStore().load().renamed
```

### `r381.M13_follow_overwrites`

marks follow overwrites a year already held under the new identifier

- File: `src/cratekit/label/marks.py`
- Source: `r381.json`, row `M13_follow_overwrites`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_slug.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_slug.py::test_a_year_already_held_under_the_new_identifier_is_not_overwritten`

Old text:

```
        if old in records and new not in records:
```

New text:

```
        if old in records:
```

### `r381.M15_read_does_not_persist`

read answers the followed year and never writes the move

- File: `src/cratekit/label/marks.py`
- Source: `r381.json`, row `M15_read_does_not_persist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_slug.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_slug.py::test_a_migrated_label_keeps_its_watermark`

Old text:

```
                if _follow(held):
                    _write(cfg, held)
```

New text:

```
                if _follow(held):
                    pass
```

### `r381.M16_advance_does_not_follow`

advance writes without following, so another label's advance leaves the old key

- File: `src/cratekit/label/marks.py`
- Source: `r381.json`, row `M16_advance_does_not_follow`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_slug.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_slug.py::test_an_advance_of_another_label_carries_the_migrated_year_along`

Old text:

```
        _follow(records)
        records[label_id] = recorded
```

New text:

```
        records[label_id] = recorded
```

### `r381.M17_read_no_follow`

read never follows, so a migrated label reads no year

- File: `src/cratekit/label/marks.py`
- Source: `r381.json`, row `M17_read_no_follow`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_slug.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_slug.py::test_a_migrated_label_keeps_its_watermark`

Old text:

```
    records = _load(cfg)
    if _follow(records):
```

New text:

```
    records = _load(cfg)
    if False:
```

### `u157.L2_blocked_unnamed`

dyn_warnings: a blocked landing names none of its variable rows

- File: `src/cratekit/intake/land_cli.py`
- Source: `u157.json`, row `L2_blocked_unnamed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`, `tests/test_drift.py`, `tests/test_analyze_check.py`
- Collected: 129 against a baseline of 129
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_dyn_native.py::test_a_library_with_no_category_to_copy_lands_and_names_the_variable_rows`

Old text:

```
    if collection.dyn_blocked:
        untagged.update(collection.dyn_variable)

```

New text:

```
(empty)
```

### `u157.N1_writable_unasked`

_dyn_plan: skip the writer's own question, so a library with no category to copy plans a tag the commit refuses

- File: `src/cratekit/intake/native.py`
- Source: `u157.json`, row `N1_writable_unasked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`, `tests/test_drift.py`, `tests/test_analyze_check.py`
- Collected: 129 against a baseline of 129
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_dyn_native.py::test_a_library_with_no_category_to_copy_lands_and_names_the_variable_rows`

Old text:

```
    if not rb_writer.my_tag_writable(db):
        return read, cut, DYN_NO_CATEGORY

```

New text:

```
(empty)
```

### `u157.N2_digest_rows`

identity: the dyn block names each row's answer only, not its drift or verdict

- File: `src/cratekit/intake/native.py`
- Source: `u157.json`, row `N2_digest_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`, `tests/test_drift.py`, `tests/test_analyze_check.py`
- Collected: 129 against a baseline of 129
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_dyn_native.py::test_the_engine_digest_covers_each_rows_drift_verdict_and_answer`

Old text:

```
[str(row.target), row.drift, row.drift_verdict, row.dyn]
```

New text:

```
[str(row.target), row.dyn]
```

### `u157.N3_no_write`

apply: the dyn tag is never written

- File: `src/cratekit/intake/native.py`
- Source: `u157.json`, row `N3_no_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`, `tests/test_drift.py`, `tests/test_analyze_check.py`
- Collected: 129 against a baseline of 129
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_land_dyn_native.py::test_a_landed_row_is_tagged_dyn_exactly_when_its_drift_reads_variable[exactly-at-the-cut]`
  - `tests/test_intake_land_dyn_native.py::test_a_landed_row_is_tagged_dyn_exactly_when_its_drift_reads_variable[moving]`
  - `tests/test_intake_land_dyn_native.py::test_a_removed_membership_is_no_mark_to_the_shared_reader`
  - `tests/test_intake_land_dyn_native.py::test_the_tag_is_written_under_one_value_and_counted_on_the_session`
  - `tests/test_intake_land_dyn_native.py::test_the_warning_names_both_selections_and_counts_each`

Old text:

```
            dyn_written = _tag_dyn(db, added_ids)
```

New text:

```
            dyn_written = 0
```

### `u157.N4_trust_the_writer`

apply: report each row's dyn from the plan, not the read back

- File: `src/cratekit/intake/native.py`
- Source: `u157.json`, row `N4_trust_the_writer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`, `tests/test_drift.py`, `tests/test_analyze_check.py`
- Collected: 129 against a baseline of 129
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_dyn_native.py::test_a_tag_written_under_a_removed_value_is_said_and_never_counted`

Old text:

```
                    dyn=content_id in dyned,
```

New text:

```
                    dyn=row.dyn,
```

### `u157.N5_no_record`

_record_landing_commit: record no dyn tags on the session

- File: `src/cratekit/intake/native.py`
- Source: `u157.json`, row `N5_no_record`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`, `tests/test_drift.py`, `tests/test_analyze_check.py`
- Collected: 129 against a baseline of 129
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_dyn_native.py::test_the_tag_is_written_under_one_value_and_counted_on_the_session`

Old text:

```
    if dyn_written > 0:
        session.record_commit(
```

New text:

```
    if False:
        session.record_commit(
```

### `r349-b.B3_clear_before_attempt`

The handler no longer clears the previous attempt's record

- File: `src/cratekit/backup/cli.py`
- Source: `r349-b.json`, row `B3_clear_before_attempt`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

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
- Ran: `tests/test_config_test_root.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

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
- Ran: `tests/test_config_test_root.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

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

### `r757-c1.S3_work_body_plans_fast`

perform_backup: plan in the fast mode whatever the payload froze

- File: `src/cratekit/backup/cli.py`
- Source: `r757-c1.json`, row `S3_work_body_plans_fast`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            full=bool(payload.get(FULL)),
```

New text:

```
            full=False,
```

### `r746-a.G7_sql_value_check_disarmed`

assert_created_rows_are_gridless: a value read from SQL is never a violation

- File: `src/cratekit/core/rb_writer.py`
- Source: `r746-a.json`, row `G7_sql_value_check_disarmed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            if value not in EMPTY_ON_CREATE:
                violations.append(f"{table}.{name} = {value!r}")
```

New text:

```
            if False:
                violations.append(f"{table}.{name} = {value!r}")
```

### `r746-d.G5_content_row_read_back_against_five_not_ten`

assert_created_rows_are_gridless: a content row is held to the playlist tables' five columns, so a key or a rate rides in. Measured again after the key taint test its zero bought

- File: `src/cratekit/core/rb_writer.py`
- Source: `r746-d.json`, row `G5_content_row_read_back_against_five_not_ten`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        policy = CONTENT_ROW_EMPTY_COLUMNS if table == CONTENT_TABLE else GRIDLESS_ON_CREATE_COLUMNS
```

New text:

```
        policy = GRIDLESS_ON_CREATE_COLUMNS
```

### `u263.D20_energy_load`

energy.features_from_path: decode through librosa.load again, so an M4A is unmeasured

- File: `src/cratekit/analysis/energy.py`
- Source: `u263.json`, row `D20_energy_load`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        samples, decoded_rate = decode.load(
            path, MEASURE_RATE, offset=offset, duration=SEGMENT_SECONDS
        )
```

New text:

```
        samples, decoded_rate = __import__("librosa").load(
            str(path), sr=MEASURE_RATE, mono=True, offset=offset, duration=SEGMENT_SECONDS
        )
```

### `u126.M1_half_is_a_majority`

Accept a value carried by exactly half the live rows

- File: `src/cratekit/write/row_link.py`
- Source: `u126.json`, row `M1_half_is_a_majority`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_repair_link.py`
- Collected: 118 against a baseline of 118
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_library_with_no_majority_content_link_refuses_before_the_gate`
  - `tests/test_intake_land_native.py::test_no_majority_link_refuses_by_name[rows0]`

Old text:

```
and carriers * 2 > rows:
```

New text:

```
and carriers * 2 >= rows:
```

### `u126.M2_plurality`

Accept the most common value whatever share of the live rows carries it

- File: `src/cratekit/write/row_link.py`
- Source: `u126.json`, row `M2_plurality`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_repair_link.py`
- Collected: 118 against a baseline of 118
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_library_with_no_majority_content_link_refuses_before_the_gate`
  - `tests/test_intake_land_native.py::test_no_majority_link_refuses_by_name[rows0]`
  - `tests/test_intake_land_native.py::test_no_majority_link_refuses_by_name[rows1]`

Old text:

```
and carriers * 2 > rows:
```

New text:

```
:
```

### `u126.M3_dead_rows_count`

Count removed rows in the majority, so a library's tombstones vote

- File: `src/cratekit/write/row_link.py`
- Source: `u126.json`, row `M3_dead_rows_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_repair_link.py`
- Collected: 118 against a baseline of 118
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_no_majority_link_refuses_by_name[rows6]`
  - `tests/test_intake_land_native.py::test_the_library_link_is_the_value_more_than_half_the_live_rows_carry[rows1-2]`

Old text:

```
            f"WHERE {rb_writer.SOFT_DELETE_COLUMN} = 0 GROUP BY {LINK} "
```

New text:

```
            f"GROUP BY {LINK} "
```

### `u126.M4_least_common_first`

Order the values least common first, so the first read is not the majority

- File: `src/cratekit/write/row_link.py`
- Source: `u126.json`, row `M4_least_common_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_repair_link.py`
- Collected: 118 against a baseline of 118
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_the_library_link_is_the_value_more_than_half_the_live_rows_carry[rows0-3]`
  - `tests/test_intake_land_native.py::test_the_library_link_is_the_value_more_than_half_the_live_rows_carry[rows2-2]`

Old text:

```
            f"ORDER BY COUNT(*) DESC"
```

New text:

```
            f"ORDER BY COUNT(*) ASC"
```

### `u126.M5_null_is_a_value`

Drop the NULL test, so a NULL majority is taken as the value

- File: `src/cratekit/write/row_link.py`
- Source: `u126.json`, row `M5_null_is_a_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_repair_link.py`
- Collected: 118 against a baseline of 118
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_no_majority_link_refuses_by_name[rows2]`
  - `tests/test_intake_land_native.py::test_no_majority_link_refuses_by_name[rows6]`
  - `tests/test_intake_land_native.py::test_no_majority_link_refuses_by_name[rows7]`

Old text:

```
    if whole is not None and _WHOLE.fullmatch(whole) and carriers * 2 > rows:
```

New text:

```
    if whole is None or _WHOLE.fullmatch(whole) and carriers * 2 > rows:
```

### `u126.M6_any_text`

Loosen the whole number test to the sign stripped isdigit the review found, so --5 and a superscript digit reach int()

- File: `src/cratekit/write/row_link.py`
- Source: `u126.json`, row `M6_any_text`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_repair_link.py`
- Collected: 118 against a baseline of 118
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_no_majority_link_refuses_by_name[rows4]`
  - `tests/test_intake_land_native.py::test_no_majority_link_refuses_by_name[rows5]`

Old text:

```
    if whole is not None and _WHOLE.fullmatch(whole) and carriers * 2 > rows:
```

New text:

```
    if whole is not None and whole.lstrip("-").isdigit() and carriers * 2 > rows:
```

### `u282.C1_refused_token_not_counted`

_summary: a refused token's not-asked is never counted, so the sweep says nothing about it (round two's BLOCKING)

- File: `src/cratekit/tagging/cli.py`
- Source: `u282.json`, row `C1_refused_token_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tag_suggest.py`
- Collected: 435 against a baseline of 435
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_token_discogs_refuses_is_warned_about_even_when_beatport_settles_every_file`

Old text:

```
                discogs_refused += 1
```

New text:

```
                discogs_refused += 0
```

### `u282.C2_refused_token_not_warned`

_discogs_warnings: the refused token's warning is never raised

- File: `src/cratekit/tagging/cli.py`
- Source: `u282.json`, row `C2_refused_token_not_warned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tag_suggest.py`
- Collected: 435 against a baseline of 435
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_token_discogs_refuses_is_warned_about_even_when_beatport_settles_every_file`

Old text:

```
    if refused:
        warnings.append(
```

New text:

```
    if False:
        warnings.append(
```

### `u282.C3_label_genre_counted_as_owed`

_summary: a file whose label gave its genre is counted as having no token, overstating the warning

- File: `src/cratekit/tagging/cli.py`
- Source: `u282.json`, row `C3_label_genre_counted_as_owed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tag_suggest.py`
- Collected: 435 against a baseline of 435
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_the_no_token_count_leaves_out_files_whose_genre_was_their_own_or_their_labels`

Old text:

```
                and str(report.get("source") or "") != tag_engine.LABEL_GENRE
            )
```

New text:

```
            )
```

### `u293.L1_dead_mark_charged`

open_night: a dead firing's mark is not charged, so a crash is a free night

- File: `src/cratekit/core/night_budget.py`
- Source: `u293.json`, row `L1_dead_mark_charged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_sync_night.py`
- Collected: 103 against a baseline of 103
- Kills: 3 (killed)
- Killed:
  - `tests/test_provider_gate_night.py::test_a_dead_firings_mark_from_an_earlier_night_is_charged_to_tonight`
  - `tests/test_provider_gate_night.py::test_a_dead_firings_mark_is_charged_in_full_and_folded_on_a_refusal`
  - `tests/test_sync_night.py::test_a_firing_that_died_is_charged_to_the_next_of_the_same_night`

Old text:

```
        spent += max(0, moved)
```

New text:

```
        spent += 0
```

### `u293.L2_night_reset`

open_night: every firing starts from nothing, whatever the night spent

- File: `src/cratekit/core/night_budget.py`
- Source: `u293.json`, row `L2_night_reset`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_sync_night.py`
- Collected: 103 against a baseline of 103
- Kills: 4 (killed)
- Killed:
  - `tests/test_provider_gate_night.py::test_a_second_firing_of_the_night_has_only_what_is_left`
  - `tests/test_provider_gate_night.py::test_a_spent_night_refuses_and_names_when_it_frees`
  - `tests/test_sync_night.py::test_a_firing_that_died_is_charged_to_the_next_of_the_same_night`
  - `tests/test_sync_night.py::test_a_night_already_spent_refuses_before_any_call`

Old text:

```
    spent = ledger.spent if ledger.night == night else 0
    if ledger.open_start is not None:
        # A DEAD
```

New text:

```
    spent = 0
    if ledger.open_start is not None:
        # A DEAD
```

### `u293.L3_spent_off_by_one`

open_night: a night with exactly its budget spent is not refused

- File: `src/cratekit/core/night_budget.py`
- Source: `u293.json`, row `L3_spent_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_sync_night.py`
- Collected: 103 against a baseline of 103
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_gate_night.py::test_a_spent_night_refuses_and_names_when_it_frees`
  - `tests/test_sync_night.py::test_a_night_already_spent_refuses_before_any_call`

Old text:

```
    if spent >= budget:
```

New text:

```
    if spent > budget:
```

### `u293.L4_noon_to_noon`

night_of: a night runs midnight to midnight, so a three in the morning firing starts a new night

- File: `src/cratekit/core/night_budget.py`
- Source: `u293.json`, row `L4_noon_to_noon`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_sync_night.py`
- Collected: 103 against a baseline of 103
- Kills: 3 (killed)
- Killed:
  - `tests/test_provider_gate_night.py::test_a_firing_is_charged_before_its_first_call_and_closed_after`
  - `tests/test_provider_gate_night.py::test_a_night_runs_noon_to_noon_local_time`
  - `tests/test_provider_gate_night.py::test_the_next_night_starts_from_nothing`

Old text:

```
    return (local - timedelta(hours=NOON)).date().isoformat()
```

New text:

```
    return (local - timedelta(hours=0)).date().isoformat()
```

### `u293.L5_close_adds_to_night`

close_night: a firing's spend replaces the night's rather than adding to it

- File: `src/cratekit/core/night_budget.py`
- Source: `u293.json`, row `L5_close_adds_to_night`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_sync_night.py`
- Collected: 103 against a baseline of 103
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_night.py::test_a_firing_that_died_is_charged_to_the_next_of_the_same_night`

Old text:

```
        Ledger(night=opened.night, spent=opened.spent_before + spent, open_start=None), target
```

New text:

```
        Ledger(night=opened.night, spent=spent, open_start=None), target
```

### `u293.L6_unreadable_gate_refuses`

_total: a gate file that cannot be read is a total of nothing

- File: `src/cratekit/core/night_budget.py`
- Source: `u293.json`, row `L6_unreadable_gate_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_sync_night.py`
- Collected: 103 against a baseline of 103
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate_night.py::test_a_gate_that_cannot_be_read_refuses_the_night`

Old text:

```
    if spend is None:
        raise _unreadable("the provider gate's state file could not be read", path)
```

New text:

```
    if spend is None:
        return 0
```

### `u190.T1_run_folder_absolute`

run: trust the folder handed in as absolute

- File: `src/cratekit/cli/tail.py`
- Source: `u190.json`, row `T1_run_folder_absolute`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_sync_land.py`, `tests/test_label_sync.py`
- Collected: 275 against a baseline of 275
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_the_chain_runs_on_the_absolute_folder_whatever_it_is_handed`

Old text:

```
    folder = folder.expanduser().absolute()
    chain.summary["staging"] = str(folder)
```

New text:

```
    chain.summary["staging"] = str(folder)
```

### `u190.T3_stale_matches_folder`

replace_stale: cancel open tail jobs over any folder, so another folder's work is lost

- File: `src/cratekit/cli/tail.py`
- Source: `u190.json`, row `T3_stale_matches_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_sync_land.py`, `tests/test_label_sync.py`
- Collected: 275 against a baseline of 275
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_stale_job_over_another_folder_or_library_is_left_alone`

Old text:

```
            and str((job.payload or {}).get("folder") or "") == str(folder)
```

New text:

```
            and True
```

### `u190.T4_name_answers_inline`

name_argv: leave name apply's confirm unanswered, so the chain stops at a gate a person running the tail answers on the command line

- File: `src/cratekit/cli/tail.py`
- Source: `u190.json`, row `T4_name_answers_inline`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_sync_land.py`, `tests/test_label_sync.py`
- Collected: 275 against a baseline of 275
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_name_apply_has_its_confirm_answered_inline_over_the_absolute_staging_folder`
  - `tests/test_sync_land.py::test_the_pass_runs_every_step_in_its_order_and_the_tail_on_the_absolute_staging_path`

Old text:

```
    return ["-d", f"{NAME_GATE}={NAME_OPTION}", "name", "apply", "--root", str(folder)]
```

New text:

```
    return ["name", "apply", "--root", str(folder)]
```

### `u190.T6_chain_namespace`

Chain.check: key every check sync.land whatever the chain, so the go's checks read as a sync pass's

- File: `src/cratekit/cli/tail.py`
- Source: `u190.json`, row `T6_chain_namespace`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_sync_land.py`, `tests/test_label_sync.py`
- Collected: 275 against a baseline of 275
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_failing_analyze_run_stops_the_go_and_plans_no_landing`
  - `tests/test_label_sync_go.py::test_a_go_over_two_answered_releases_runs_the_tail_in_order_and_stops_at_the_landing_gate`
  - `tests/test_label_sync_go.py::test_a_landing_that_planned_nothing_ends_the_go_with_its_own_outcome`

Old text:

```
                "key": f"{self.namespace}.{step}",
```

New text:

```
                "key": f"sync.land.{step}",
```

### `u227.R15_way_on_wording`

_way_on: name a mirror download as queued by hand, to be driven outside a pass (round one's S12)

- File: `src/cratekit/cli/sync_land.py`
- Source: `u227.json`, row `R15_way_on_wording`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_land_mirror_downloads.py`, `tests/test_sync_land_staged.py`
- Collected: 96 against a baseline of 96
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_mirror_downloads.py::test_a_pass_continuing_an_earlier_one_over_nothing_new_takes_none`

Old text:

```
    elif _mirror_download(job) and job.state is jobs.JobState.QUEUED:
```

New text:

```
    elif False:
```

### `u227.R19_take_library`

_take_mirror_downloads: take another library's mirror job

- File: `src/cratekit/cli/sync_land.py`
- Source: `u227.json`, row `R19_take_library`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_land_mirror_downloads.py`, `tests/test_sync_land_staged.py`
- Collected: 96 against a baseline of 96
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_mirror_downloads.py::test_a_mirror_download_another_library_queued_is_not_taken`

Old text:

```
                or job.library_id != cfg.library.volume_id

```

New text:

```
(empty)
```

### `u227.R20_take_source`

_mirror_download: any intake.playlist job is a mirror download, a hand queued one included

- File: `src/cratekit/cli/sync_land.py`
- Source: `u227.json`, row `R20_take_source`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_land_mirror_downloads.py`, `tests/test_sync_land_staged.py`
- Collected: 96 against a baseline of 96
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land.py::test_an_intake_job_queued_by_hand_with_no_pass_is_named_not_passed_over`
  - `tests/test_sync_land_mirror_downloads.py::test_a_hand_queued_playlist_job_and_a_cancelled_mirror_job_are_not_taken`

Old text:

```
        and (job.payload or {}).get("source_id") == mirror_downloads.SOURCE_ID

```

New text:

```
(empty)
```

### `u227.R21_take_continued`

sync_land: take mirror jobs into a continued earlier pass

- File: `src/cratekit/cli/sync_land.py`
- Source: `u227.json`, row `R21_take_continued`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_land_mirror_downloads.py`, `tests/test_sync_land_staged.py`
- Collected: 96 against a baseline of 96
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_mirror_downloads.py::test_a_pass_continuing_an_earlier_one_over_nothing_new_takes_none`

Old text:

```
            if fresh and run_id in (None, fresh) and _take_mirror_downloads(report, cfg, fresh):
```

New text:

```
            if fresh and _take_mirror_downloads(report, cfg, run_id or fresh):
```

### `u227.R22_take_not_driven`

sync_land: give the jobs the run but keep driving the pass sync all named nothing for

- File: `src/cratekit/cli/sync_land.py`
- Source: `u227.json`, row `R22_take_not_driven`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_land_mirror_downloads.py`, `tests/test_sync_land_staged.py`
- Collected: 96 against a baseline of 96
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_mirror_downloads.py::test_a_pass_whose_sync_all_queued_nothing_takes_the_mirror_download`

Old text:

```
                run_id = fresh
                report.summary["pass_run"] = fresh
```

New text:

```
                pass
```

### `u227.R25_way_on_state`

_way_on: name a blocked mirror download as the next pass's, which takes queued jobs only (round two's R3)

- File: `src/cratekit/cli/sync_land.py`
- Source: `u227.json`, row `R25_way_on_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_land_mirror_downloads.py`, `tests/test_sync_land_staged.py`
- Collected: 96 against a baseline of 96
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_mirror_downloads.py::test_a_mirror_download_a_pass_cannot_take_keeps_the_command_that_settles_it`

Old text:

```
    elif _mirror_download(job) and job.state is jobs.JobState.QUEUED:
```

New text:

```
    elif _mirror_download(job):
```

### `u111-c.C3_inboxed_suffix`

A name ending _inboxed is no longer recognised as a batch

- File: `src/cratekit/intake/rotate.py`
- Source: `u111-c.json`, row `C3_inboxed_suffix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 41 against a baseline of 41
- Kills: 3 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_a_batch_moved_past_expiry_is_removed_by_the_next_run_and_then_nothing`
  - `tests/test_inbox_rotate.py::test_each_batch_says_how_it_was_recognised_and_what_it_was_aged_from`
  - `tests/test_inbox_rotate.py::test_the_forty_and_the_hundred_move_the_old_one_hundred_twenty_goes_and_no_track_moves`

Old text:

```
    if name.endswith(INBOXED_SUFFIX):
```

New text:

```
    if False:
```

### `u111-c.C4_removal_threshold`

A batch in Old is removed after the stale threshold instead of the expired one

- File: `src/cratekit/intake/rotate.py`
- Source: `u111-c.json`, row `C4_removal_threshold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 41 against a baseline of 41
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_a_batch_moved_past_expiry_is_removed_by_the_next_run_and_then_nothing`
  - `tests/test_inbox_rotate.py::test_a_second_run_plans_nothing_and_still_asks`

Old text:

```
        action = REMOVE if age > expired_days else KEEP
```

New text:

```
        action = REMOVE if age > stale_days else KEEP
```

### `u111-c.C5_move_threshold`

A batch in INBOX moves only after the expired threshold instead of the stale one

- File: `src/cratekit/intake/rotate.py`
- Source: `u111-c.json`, row `C5_move_threshold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 41 against a baseline of 41
- Kills: 3 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_a_second_run_plans_nothing_and_still_asks`
  - `tests/test_inbox_rotate.py::test_old_is_created_once_and_the_second_run_reuses_it`
  - `tests/test_inbox_rotate.py::test_the_forty_and_the_hundred_move_the_old_one_hundred_twenty_goes_and_no_track_moves`

Old text:

```
        action = MOVE if age > stale_days else KEEP
```

New text:

```
        action = MOVE if age > expired_days else KEEP
```

### `u111-c.C6_plan_taken_again`

The write no longer takes the plan again on its own handle and compares digests

- File: `src/cratekit/intake/rotate.py`
- Source: `u111-c.json`, row `C6_plan_taken_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_the_engine_refuses_a_plan_inbox_no_longer_matches`

Old text:

```
    if again.digest != plan.digest:
```

New text:

```
    if False:
```

### `u111-c.C7_old_creation_planned`

The folder the write creates for Old is not named to the confinement judge

- File: `src/cratekit/intake/rotate.py`
- Source: `u111-c.json`, row `C7_old_creation_planned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 41 against a baseline of 41
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_a_second_run_plans_nothing_and_still_asks`
  - `tests/test_inbox_rotate.py::test_old_is_created_once_and_the_second_run_reuses_it`

Old text:

```
                created.append(str(old.ID))
```

New text:

```
                pass
```

### `u111-d.C10_two_olds_refused`

Two live Old folders under INBOX are no longer refused, the first is used

- File: `src/cratekit/intake/rotate.py`
- Source: `u111-d.json`, row `C10_two_olds_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_two_old_folders_are_refused_rather_than_one_chosen`

Old text:

```
    if len(olds) > 1:
```

New text:

```
    if len(olds) > 99:
```

### `u111-d.C9_committed_records_only`

A landing record dates its batch whether or not its commit landed

- File: `src/cratekit/intake/rotate.py`
- Source: `u111-d.json`, row `C9_committed_records_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_a_landing_record_that_committed_nothing_dates_nothing`

Old text:

```
        if str(session.SourceState.COMMITTED) not in {str(v) for v in record.sources.values()}:
```

New text:

```
        if False:
```

### `r1372.K19_passed_by_strict`

passed_by: a write that began at the snapshot's very moment is not passed

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1372.json`, row `K19_passed_by_strict`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_snapshot_passes_the_carried_records_of_its_pair_that_began_before_it`

Old text:

```
            if began is not None and not began > moment:
```

New text:

```
            if began is not None and began < moment:
```

### `r1372.K20_passed_by_any_pair`

passed_by: a snapshot lets go of every pair's carried records, not its own

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1372.json`, row `K20_passed_by_any_pair`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_snapshot_passes_the_carried_records_of_its_pair_that_began_before_it`

Old text:

```
            if _account_of(key, steps, new=new, made=made) != account_id:
                continue
            began = placeholders.parse_hearted(steps.get(account))
            if began is not None
```

New text:

```
            began = placeholders.parse_hearted(steps.get(account))
            if began is not None
```

### `r1372.K21_made_pair_unmapped`

_account_of: a made pair is read under its key, not the account playlist it was made as

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1372.json`, row `K21_made_pair_unmapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`
- Collected: 89 against a baseline of 89
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_made_pair_is_read_under_the_account_playlist_it_was_made_as`
  - `tests/test_sync_pair_stopped.py::test_a_snapshot_passes_the_carried_records_of_its_pair_that_began_before_it`

Old text:

```
    if key.startswith(new):
        return steps.get(made) if isinstance(steps.get(made), str) else ""
    return key
```

New text:

```
    return key
```

### `r1376.F14_finished_filter_gone`

stopped_writes (sample, U225): a stop a later run finished is still read, by a first sync among others

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1376.json`, row `F14_finished_filter_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_later_run_that_finished_the_pair_hides_the_stopped_write_in_either_order`

Old text:

```
        if account_id not in finished or not finished[account_id] > began
```

New text:

```
        if True
```

### `u225.M8_reached_strict_membership`

reached: a track added or taken off since is compared too

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `u225.json`, row `M8_reached_strict_membership`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`
- Collected: 89 against a baseline of 89
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_track_added_or_taken_off_since_is_left_out_of_the_comparison`
  - `tests/test_sync_pair_stopped.py::test_orders_on_the_path_that_differ_only_by_a_track_taken_off_all_count`
  - `tests/test_sync_pair_stopped.py::test_positions_counts_the_moves_that_leave_each_order_on_the_path`

Old text:

```
    common = set(current) & set(start)
```

New text:

```
    common = set(current) | set(start)
```

### `u225.M9_finish_ignored`

stopped_writes: a later run that finished the pair does not hide the stopped write

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `u225.json`, row `M9_finish_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`
- Collected: 89 against a baseline of 89
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_carried_copy_gives_way_to_its_own_runs_steps_kept_under_the_same_plan`
  - `tests/test_sync_pair_stopped.py::test_a_finished_or_unordered_write_is_no_stopped_one`
  - `tests/test_sync_pair_stopped.py::test_a_later_run_that_finished_the_pair_hides_the_stopped_write_in_either_order`

Old text:

```
            if done in steps:
                if account_id not in finished
```

New text:

```
            if False:
                if account_id not in finished
```

### `u284.R1_since_moves_every_refusal`

refused._change: a later refusal resets since to now, so the date says the latest refusal rather than when it began

- File: `src/cratekit/tagging/refused.py`
- Source: `u284.json`, row `R1_since_moves_every_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`
- Collected: 35 against a baseline of 35
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_first_refusal_sets_since_and_a_later_one_keeps_it`
  - `tests/test_sync_refused.py::test_a_sweep_with_no_token_fails_each_file_and_says_who_refused_and_the_token`
  - `tests/test_sync_refused.py::test_with_no_token_the_pass_stops_at_its_tag_step_saying_who_refused_and_the_token`

Old text:

```
                    since=before.since if before is not None else now,
```

New text:

```
                    since=now,
```

### `u284.R2_an_answer_never_clears`

refused._change: a match or a miss leaves the date, so a catalogue that answers again still reads as refusing

- File: `src/cratekit/tagging/refused.py`
- Source: `u284.json`, row `R2_an_answer_never_clears`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`
- Collected: 35 against a baseline of 35
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_miss_from_the_refusing_catalogue_clears_it_and_an_outage_does_not`
  - `tests/test_sync_refused.py::test_an_answer_clears_the_catalogue_and_leaves_the_others`

Old text:

```
            elif held.pop(source, None) is None:
                return
```

New text:

```
            else:
                return
```

### `u284.R3_write_without_the_lock`

refused._change: write though the lock was not had, so two sweeps can lose each other's dates

- File: `src/cratekit/tagging/refused.py`
- Source: `u284.json`, row `R3_write_without_the_lock`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_lock_another_process_holds_skips_the_write_rather_than_waiting`

Old text:

```
            if not had:
                LOG.info
```

New text:

```
            if False:
                LOG.info
```

### `u284.R4_empty_since_read`

refused._parse: an entry with an empty since is read as refusing

- File: `src/cratekit/tagging/refused.py`
- Source: `u284.json`, row `R4_empty_since_read`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_an_entry_of_the_wrong_shape_is_skipped_and_the_rest_read`

Old text:

```
        if isinstance(since, str) and since and isinstance(last, str)
```

New text:

```
        if isinstance(since, str) and isinstance(last, str)
```

### `u284.R5_count_never_grows`

refused._change: the refusal count stays where it was

- File: `src/cratekit/tagging/refused.py`
- Source: `u284.json`, row `R5_count_never_grows`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`
- Collected: 35 against a baseline of 35
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_first_refusal_sets_since_and_a_later_one_keeps_it`
  - `tests/test_sync_refused.py::test_a_sweeps_run_count_records_a_refusal_sent_and_not_one_unsent`

Old text:

```
                    count=(before.count if before is not None else 0) + 1,
```

New text:

```
                    count=(before.count if before is not None else 0) + 0,
```

### `u284.R6_write_failure_raises`

refused._change: catch only ValueError, so a record that cannot be written fails the file it was asked about

- File: `src/cratekit/tagging/refused.py`
- Source: `u284.json`, row `R6_write_failure_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_record_whose_target_cannot_be_replaced_never_raises`

Old text:

```
    except (OSError, ValueError, RecursionError) as exc:
```

New text:

```
    except ValueError as exc:
```

### `u284.R7_deep_record_raises`

refused._parse: a record nested past the parser's depth raises out of every read

- File: `src/cratekit/tagging/refused.py`
- Source: `u284.json`, row `R7_deep_record_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_record_nested_past_the_parsers_depth_reads_as_none_and_is_written_over`

Old text:

```
    except (ValueError, RecursionError):
        # A RECORD NESTED
```

New text:

```
    except ValueError:
        # A RECORD NESTED
```

### `u78-a.A3_several_listed`

An ISRC filed under several tracks lists the first, the guess R-356 forbids

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u78-a.json`, row `A3_several_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 88 against a baseline of 88
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_a_one_id_isrc_is_listed_and_two_ids_and_no_isrc_are_handed_on`
  - `tests/test_intake_missing_isrc.py::test_the_order_the_provider_answers_in_does_not_change_the_files`
  - `tests/test_intake_missing_isrc.py::test_the_unlisted_file_round_trips_through_read_list_with_its_reasons`

Old text:

```
        elif len(answer) == 1:
```

New text:

```
        elif len(answer) >= 1:
```

### `u78-a.A5_outage_read_as_none`

A provider that could not answer is read as filing no track, so the row is handed on and the verb writes

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u78-a.json`, row `A5_outage_read_as_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 88 against a baseline of 88
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_a_provider_outage_refuses_and_writes_nothing`

Old text:

```
            except Exception as exc:  # noqa: BLE001 - refused whole, never swallowed
                raise refuse(
```

New text:

```
            except Exception as exc:  # noqa: BLE001 - refused whole, never swallowed
                answers[code] = ()
                continue
                raise refuse(
```

### `u78-a.A6_blank_id_dropped`

A track with no identifier in the answer is dropped, so one named and one unnamed reads as one id

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u78-a.json`, row `A6_blank_id_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 88 against a baseline of 88
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_an_answer_holding_a_track_with_no_identifier_is_handed_on_not_read_as_one`

Old text:

```
    if any(not one for one in ids):
```

New text:

```
    ids = [one for one in ids if one]
    if False:
```

### `u78-b.B1_unwritable_refuses_whole`

The per row text line check before writing is removed, so one unwritable row refuses the verb again

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u78-b.json`, row `B1_unwritable_refuses_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 88 against a baseline of 88
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_a_track_that_cannot_be_a_text_line_is_named_and_the_rest_are_still_written`
  - `tests/test_intake_missing_isrc.py::test_missing_tracks_none_named_and_none_writable_refuse_rather_than_no_op`

Old text:

```
            try:
                listdoc.text_line(row)
            except listdoc.ListDocRefused:
```

New text:

```
            try:
                pass
            except listdoc.ListDocRefused:
```

### `u78-b.B3_ids_unsorted`

The identifiers in a several reason are written in provider order

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u78-b.json`, row `B3_ids_unsorted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 88 against a baseline of 88
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_the_order_the_provider_answers_in_does_not_change_the_files`

Old text:

```
f"({', '.join(sorted(answer))}), and which release to download is "
```

New text:

```
f"({', '.join(answer)}), and which release to download is "
```

### `u78-d.A4_cratekit_error_passthrough_again`

A product refusal raised by the catalogue is relabelled unavailable-transient

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u78-d.json`, row `A4_cratekit_error_passthrough_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 88 against a baseline of 88
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_a_product_refusal_from_the_catalogue_passes_through_unrelabelled`

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

### `u169.E1_declined_accepts_retryable`

Declined: drop the refusal of a retryable cause, so a transient failure can be skipped and never retried

- File: `src/cratekit/core/jobs.py`
- Source: `u169.json`, row `E1_declined_accepts_retryable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_acquire_workers.py`
- Collected: 151 against a baseline of 151
- Kills: 2 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_handler_that_declines_a_retryable_cause_fails_the_item_rather_than_skipping_it`
  - `tests/test_jobs.py::test_a_retryable_cause_cannot_decline_an_item`

Old text:

```
        if cause.retryable:
            raise ValueError(
```

New text:

```
        if False:
            raise ValueError(
```

### `u169.E2_drive_fails_a_decline`

drive: no Declined clause, so a declined item falls to the failure boundary and fails the job

- File: `src/cratekit/core/jobs.py`
- Source: `u169.json`, row `E2_drive_fails_a_decline`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_acquire_workers.py`
- Collected: 151 against a baseline of 151
- Kills: 11 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_lossy_landing_under_strict_policy_is_refused_at_the_item_with_the_codec_named`
  - `tests/test_acquire_workers.py::test_a_refusal_beside_a_network_failure_fails_and_keeps_the_refusal_skipped`
  - `tests/test_acquire_workers.py::test_a_track_the_provider_no_longer_has_is_declined_as_well`
  - `tests/test_acquire_workers.py::test_the_declined_warnings_name_skipped_tracks_and_never_a_failed_one`
  - `tests/test_acquire_workers.py::test_the_human_output_says_ok_and_names_the_refused_track`
  - `tests/test_acquire_workers.py::test_the_warning_is_the_same_when_the_finished_job_is_asked_about_again`
  - `tests/test_acquire_workers.py::test_three_landed_and_one_refused_by_policy_ends_ok_with_a_warning_naming_it`
  - `tests/test_jobs.py::test_a_declined_item_is_skipped_with_its_cause_and_the_job_succeeds`
  - `tests/test_jobs.py::test_a_job_every_item_of_which_was_declined_succeeds_rather_than_failing`
  - `tests/test_jobs.py::test_a_real_failure_beside_a_declined_item_still_fails_the_job_and_names_both`
  - `tests/test_jobs.py::test_a_retry_re_arms_the_failure_and_leaves_the_declined_item_settled`

Old text:

```
                except Declined as exc:
```

New text:

```
                except Parked as exc:
```

### `u169.E3_decline_writes_failed`

decline_item: record the item failed rather than skipped

- File: `src/cratekit/core/jobs.py`
- Source: `u169.json`, row `E3_decline_writes_failed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_acquire_workers.py`
- Collected: 151 against a baseline of 151
- Kills: 10 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_lossy_landing_under_strict_policy_is_refused_at_the_item_with_the_codec_named`
  - `tests/test_acquire_workers.py::test_a_refusal_beside_a_network_failure_fails_and_keeps_the_refusal_skipped`
  - `tests/test_acquire_workers.py::test_a_track_the_provider_no_longer_has_is_declined_as_well`
  - `tests/test_acquire_workers.py::test_the_declined_warnings_name_skipped_tracks_and_never_a_failed_one`
  - `tests/test_acquire_workers.py::test_the_human_output_says_ok_and_names_the_refused_track`
  - `tests/test_acquire_workers.py::test_the_warning_is_the_same_when_the_finished_job_is_asked_about_again`
  - `tests/test_acquire_workers.py::test_three_landed_and_one_refused_by_policy_ends_ok_with_a_warning_naming_it`
  - `tests/test_jobs.py::test_a_declined_item_is_skipped_with_its_cause_and_the_job_succeeds`
  - `tests/test_jobs.py::test_a_real_failure_beside_a_declined_item_still_fails_the_job_and_names_both`
  - `tests/test_jobs.py::test_a_retry_re_arms_the_failure_and_leaves_the_declined_item_settled`

Old text:

```
            (str(ItemState.SKIPPED), json.dumps(cause.to_json()), job_id, item_id),
```

New text:

```
            (str(ItemState.FAILED), json.dumps(cause.to_json()), job_id, item_id),
```

### `u169.E4_decline_drops_cause`

decline_item: keep no cause on the skipped item, so nothing can name why

- File: `src/cratekit/core/jobs.py`
- Source: `u169.json`, row `E4_decline_drops_cause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_acquire_workers.py`
- Collected: 151 against a baseline of 151
- Kills: 10 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_lossy_landing_under_strict_policy_is_refused_at_the_item_with_the_codec_named`
  - `tests/test_acquire_workers.py::test_a_lossy_offer_under_strict_policy_is_refused_before_anything_is_fetched`
  - `tests/test_acquire_workers.py::test_a_track_the_provider_does_not_have_is_permanent_and_carries_no_remedy`
  - `tests/test_acquire_workers.py::test_a_track_the_provider_no_longer_has_is_declined_as_well`
  - `tests/test_acquire_workers.py::test_the_declined_warnings_name_skipped_tracks_and_never_a_failed_one`
  - `tests/test_acquire_workers.py::test_the_frozen_policy_reaches_the_worker_not_the_live_one`
  - `tests/test_acquire_workers.py::test_the_human_output_says_ok_and_names_the_refused_track`
  - `tests/test_acquire_workers.py::test_the_warning_is_the_same_when_the_finished_job_is_asked_about_again`
  - `tests/test_acquire_workers.py::test_three_landed_and_one_refused_by_policy_ends_ok_with_a_warning_naming_it`
  - `tests/test_jobs.py::test_a_declined_item_is_skipped_with_its_cause_and_the_job_succeeds`

Old text:

```
            (str(ItemState.SKIPPED), json.dumps(cause.to_json()), job_id, item_id),
```

New text:

```
            (str(ItemState.SKIPPED), None, job_id, item_id),
```

### `u169.E6_failed_cause_hides_declines`

partial failure cause: say nothing of the declined items beside the failures

- File: `src/cratekit/core/jobs.py`
- Source: `u169.json`, row `E6_failed_cause_hides_declines`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_acquire_workers.py`
- Collected: 151 against a baseline of 151
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_real_failure_beside_a_declined_item_still_fails_the_job_and_names_both`

Old text:

```
    if result.declined:
```

New text:

```
    if False:
```

### `u42-author-round-2.C2_unknown_defaults_lossless`

Classify an unrecognised suffix as lossless instead of 'other'

- File: `src/cratekit/acquire/cli.py`
- Source: `u42-author-round-2.json`, row `C2_unknown_defaults_lossless`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_non_audio_files_are_not_reported`

Old text:

```
    return "other"
```

New text:

```
    return "lossless"
```

### `u42-author.C1_undecided_derived`

Empty the undecided remainder, so an MP4 container falls out as 'other'

- File: `src/cratekit/acquire/cli.py`
- Source: `u42-author.json`, row `C1_undecided_derived`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 3 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_an_mp4_container_is_reported_undecided_rather_than_assumed`
  - `tests/test_acquire_cli.py::test_every_audio_container_the_renamer_knows_has_a_classification`
  - `tests/test_acquire_cli.py::test_the_undecided_remainder_is_the_mp4_container_today`

Old text:

```
UNDECIDED_EXTS: frozenset[str] = frozenset(naming.AUDIO_EXTS) - LOSSLESS_EXTS - LOSSY_EXTS
```

New text:

```
UNDECIDED_EXTS: frozenset[str] = frozenset()
```

