# Mutation table: u325-before-l-16

Measured by `scripts/mutate.py` on 2026-11-23 01:12 UTC, branch `HEAD` at `539638eb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22663 collected. pytest invocations for this batch: 122.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:15 UTC for commit `539638ebe629`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 23, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard. 18 row(s) were reused from a prior sidecar and were measured by an earlier process, whose children this run did not watch.

Null control `NULL_CONTROL`: killed 0, collected 22663 against 22663. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u212.S1_missing_ends` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 334 | 1 | killed |
| `u212.S2_download_refused_all` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 22663 | 0 (promoted) | zero |
| `u212.S3_no_list_download` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 22663 | 0 (promoted) | zero |
| `u212.S4_staged_said` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 334 | 1 | killed |
| `r836-a.A1_product_made_asked_first` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 22663 | 3 (promoted) | killed |
| `r836-a.A4_no_video_declared` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 501 | 1 | killed |
| `r836-a.A5_removal_never_retried` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 501 | 1 | killed |
| `r1056.N1_no_refusal_of_an_unreadable_record` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 33 | 7 | killed |
| `r1056.N2_first_landing_only` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `r1056.N3_years_from_the_argument` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `r1056.N4_no_landings_in_digest` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 33 | 2 | killed |
| `r1056.N5_no_reread_before_rename` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `r1056.N8_shown_pass_bare` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `r1056.N9_verb_not_threaded` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 33 | 6 | killed |
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
| `u126.M1_half_is_a_majority` | `src/cratekit/write/row_link.py` | user | 2 file(s) | 118 | 2 | killed |
| `u126.M2_plurality` | `src/cratekit/write/row_link.py` | user | 2 file(s) | 118 | 3 | killed |
| `u126.M3_dead_rows_count` | `src/cratekit/write/row_link.py` | user | 2 file(s) | 118 | 2 | killed |
| `u126.M4_least_common_first` | `src/cratekit/write/row_link.py` | user | 2 file(s) | 118 | 3 | killed |
| `u126.M5_null_is_a_value` | `src/cratekit/write/row_link.py` | user | 2 file(s) | 118 | 3 | killed |
| `u126.M6_any_text` | `src/cratekit/write/row_link.py` | user | 2 file(s) | 118 | 2 | killed |
| `r758-a.T2_first_commit_admits_a_removal` | `src/cratekit/write/trees.py` | user | 1 file(s) | 112 | 1 | killed |
| `r758-a.T3_target_not_proven` | `src/cratekit/write/trees.py` | user | 1 file(s) | 112 | 1 | killed |
| `r758-a.T4_target_can_be_removed_from` | `src/cratekit/write/trees.py` | user | 1 file(s) | 112 | 1 | killed |
| `r758-a.T5_dead_track_moved` | `src/cratekit/write/trees.py` | user | 1 file(s) | 112 | 1 | killed |
| `r758-a.T6_removed_playlist_is_a_destination` | `src/cratekit/write/trees.py` | user | 1 file(s) | 112 | 2 | killed |
| `r758-b.T7_refusal_read_as_an_interruption` | `src/cratekit/write/trees.py` | user | 1 file(s) | 112 | 1 | killed |
| `u282.C1_refused_token_not_counted` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 435 | 1 | killed |
| `u282.C2_refused_token_not_warned` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 435 | 1 | killed |
| `u282.C3_label_genre_counted_as_owed` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 435 | 1 | killed |
| `r501-a.S1_verify_state_guard` | `src/cratekit/core/session.py` | maintainer | 5 file(s) | 175 | 1 | killed |
| `r501-a.S2_excusal_capture` | `src/cratekit/core/session.py` | user | 5 file(s) | 175 | 1 | killed |
| `r501-a.S3_excusal_proof` | `src/cratekit/core/session.py` | user | 5 file(s) | 175 | 5 | killed |
| `r501-a.S4_excusal_state` | `src/cratekit/core/session.py` | user | 5 file(s) | 175 | 1 | killed |
| `r501-a.T1_precheck_excusal` | `src/cratekit/core/tree_registry.py` | user | 5 file(s) | 175 | 4 | killed |
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
| `u165.L1_bridge_skip` | `src/cratekit/intake/land_cli.py` | user | 4 file(s) | 152 | 2 | killed |
| `u165.L2_land_only` | `src/cratekit/intake/land_cli.py` | user | 4 file(s) | 152 | 3 | killed |
| `u165.L3_filing_tail` | `src/cratekit/intake/land_cli.py` | user | 4 file(s) | 152 | 4 | killed |
| `u165.L4_files_into` | `src/cratekit/intake/land_cli.py` | user | 4 file(s) | 152 | 2 | killed |
| `u165.N1_digest` | `src/cratekit/intake/native.py` | user | 4 file(s) | 152 | 1 | killed |
| `r1031.M10_filter_against_raw_links` | `src/cratekit/modules/outbound/ledger.py` | user | 2 file(s) | 73 | 1 | killed |
| `r1031.M11_filter_removed` | `src/cratekit/modules/outbound/ledger.py` | user | 2 file(s) | 73 | 1 | killed |
| `r1031.M12_link_keeps_its_miss` | `src/cratekit/modules/outbound/ledger.py` | maintainer | 2 file(s) | 73 | 1 | killed |
| `r1031.M13_miss_written_over_a_link` | `src/cratekit/modules/outbound/ledger.py` | maintainer | 2 file(s) | 73 | 1 | killed |
| `r1031.M8_misses_not_a_map_read` | `src/cratekit/modules/outbound/ledger.py` | user | 2 file(s) | 73 | 1 | killed |
| `r1031.M9_malformed_miss_kept` | `src/cratekit/modules/outbound/ledger.py` | maintainer | 2 file(s) | 73 | 1 | killed |
| `u174.N1_landed_passes_closed` | `src/cratekit/intake/native.py` | user | 3 file(s) | 228 | 1 | killed |
| `u174.N2_landed_passes_committed` | `src/cratekit/intake/native.py` | user | 3 file(s) | 228 | 1 | killed |
| `u174.N3_landed_passes_workflow` | `src/cratekit/intake/native.py` | maintainer | 3 file(s) | 228 | 1 | killed |
| `u174.N4_landed_passes_pass_key` | `src/cratekit/intake/native.py` | maintainer | 3 file(s) | 228 | 1 | killed |
| `u62.C1_bound_constant_true` | `src/cratekit/label/catalogue.py` | user | 4 file(s) | 544 | 1 | killed |
| `u62.C2_outage_as_credential` | `src/cratekit/label/catalogue.py` | user | 4 file(s) | 544 | 4 | killed |
| `sitting3.G8_queue_skips_readiness` | `src/cratekit/vocals/cli.py` | user | 1 file(s) | 34 | 2 | killed |
| `u181.C1_unscored_head_or_score` | `src/cratekit/vocals/cli.py` | user | 1 file(s) | 34 | 3 | killed |
| `u181.C2_unscored_ignores_score` | `src/cratekit/vocals/cli.py` | user | 1 file(s) | 34 | 3 | killed |
| `u25.G6_always_rewrite` | `src/cratekit/vocals/cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `u93-recursive-analysis.D23_vocals_resume_warning` | `src/cratekit/vocals/cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `u93-recursive-analysis.D25_vocals_join` | `src/cratekit/vocals/cli.py` | maintainer | 1 file(s) | 34 | 1 | killed |
| `u140.B10_queued_day_name_dropped` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 29 | 2 | killed |
| `u140.B7_twin_refusal_dropped` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 29 | 4 | killed |
| `u140.B8_flag_conflict_dropped` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 29 | 1 | killed |
| `u140.B9_abort_applies` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 29 | 1 | killed |
| `u140.B1_ledger_folds_into_a_twin` | `src/cratekit/modules/outbound/ledger.py` | user | 1 file(s) | 29 | 1 | killed |
| `u140.B2_ledger_moves_another_id` | `src/cratekit/modules/outbound/ledger.py` | user | 1 file(s) | 29 | 1 | killed |
| `r515-operator.S14_harvest_no_warning` | `src/cratekit/label/cli.py` | user | 1 file(s) | 82 | 1 | killed |
| `u109-b.B4_resume_dropped` | `src/cratekit/label/cli.py` | user | 1 file(s) | 82 | 47 | killed |
| `u109-b.B6_message_drops_verb` | `src/cratekit/label/cli.py` | user | 1 file(s) | 82 | 1 | killed |
| `u109-b.B7_step_drops_verb` | `src/cratekit/label/cli.py` | user | 1 file(s) | 82 | 1 | killed |
| `u109-b.B8_itemless_branch` | `src/cratekit/label/cli.py` | user | 1 file(s) | 82 | 1 | killed |
| `r1184.M19_tag_folder_wiring` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 292 | 1 | killed |
| `r1184.M20_tag_folder_fallback` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 292 | 1 | killed |
| `r1184.M21_guess_wiring` | `src/cratekit/tagging/guess_cli.py` | user | 3 file(s) | 292 | 1 | killed |
| `r835-b.T1_folder_create_never_retried` | `src/cratekit/modules/outbound/tidal_account.py` | user | 3 file(s) | 284 | 1 | killed |
| `r835-b.T2_refused_move_raised` | `src/cratekit/modules/outbound/tidal_account.py` | user | 3 file(s) | 284 | 1 | killed |
| `r835-c.T3_short_answer_read_again_again` | `src/cratekit/modules/outbound/tidal_account.py` | user | 3 file(s) | 284 | 1 | killed |
| `u44-author.C2_argv_drops_overwrite` | `src/cratekit/master/cli.py` | user | 1 file(s) | 73 | 2 | killed |
| `u44-author.C3_argv_drops_output_dir` | `src/cratekit/master/cli.py` | user | 1 file(s) | 73 | 2 | killed |
| `u44-author.C4_refusal_not_translated` | `src/cratekit/master/cli.py` | user | 1 file(s) | 73 | 23 | killed |
| `u44-author.C6_overwrite_always_true` | `src/cratekit/master/cli.py` | user | 1 file(s) | 73 | 4 | killed |
| `u44-author.C7_output_dir_ignored_at_the_work` | `src/cratekit/master/cli.py` | user | 1 file(s) | 73 | 3 | killed |

## Zero rows and what they owe

- `u212.S2_download_refused_all` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u212.S3_no_list_download` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

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
- Collected: 22663 against a baseline of 22663
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
- Collected: 22663 against a baseline of 22663
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
- Collected: 22663 against a baseline of 22663
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

### `r758-a.T2_first_commit_admits_a_removal`

the move's first commit admits a removal, so one slipped into the additions lands

- File: `src/cratekit/write/trees.py`
- Source: `r758-a.json`, row `T2_first_commit_admits_a_removal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 112 against a baseline of 112
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_the_moves_own_first_commit_refuses_a_removal`

Old text:

```
                    already_present += len(content_ids) - len(inserted)
                rb_writer.commit_guarded(db)
```

New text:

```
                    already_present += len(content_ids) - len(inserted)
                rb_writer.commit_guarded(db, removals=rb_writer.REMOVABLE_TABLES)
```

### `r758-a.T3_target_not_proven`

a removal is made whether or not the track sits in its target, so a track can end in neither

- File: `src/cratekit/write/trees.py`
- Source: `r758-a.json`, row `T3_target_not_proven`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 112 against a baseline of 112
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_track_not_in_its_target_has_nothing_removed`

Old text:

```
            if not places.holds(move.target, move.content_id):
                held_back.append(move.content_id)
                continue
```

New text:

```
(empty)
```

### `r758-a.T4_target_can_be_removed_from`

a move that names its own target among its removals takes the track out of the target

- File: `src/cratekit/write/trees.py`
- Source: `r758-a.json`, row `T4_target_can_be_removed_from`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 112 against a baseline of 112
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_the_target_is_never_removed_from_even_when_a_move_names_it`

Old text:

```
                if destination != move.target:
                    leaving.setdefault(destination, []).append(move.content_id)
```

New text:

```
                leaving.setdefault(destination, []).append(move.content_id)
```

### `r758-a.T5_dead_track_moved`

a track with no live collection row is moved like any other

- File: `src/cratekit/write/trees.py`
- Source: `r758-a.json`, row `T5_dead_track_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 112 against a baseline of 112
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_track_with_no_live_collection_row_is_skipped_whole`

Old text:

```
        live = [move for move in moves if _live_content(db, move.content_id)]
```

New text:

```
        live = list(moves)
```

### `r758-a.T6_removed_playlist_is_a_destination`

a playlist rekordbox removed answers for a destination, so an addition lands where nobody can see it

- File: `src/cratekit/write/trees.py`
- Source: `r758-a.json`, row `T6_removed_playlist_is_a_destination`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 112 against a baseline of 112
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_sub_held_only_through_a_removed_playlist_is_not_planned_for_removal`
  - `tests/test_adopt_move.py::test_an_addition_never_lands_in_a_playlist_rekordbox_removed`

Old text:

```
        and str(getattr(playlist, "ParentID", "")) in parents
        and not rb_writer.node_removed(playlist)
```

New text:

```
        and str(getattr(playlist, "ParentID", "")) in parents
```

### `r758-b.T7_refusal_read_as_an_interruption`

a refusal in the removals is raised as an interrupted move and loses its own cause and remedy

- File: `src/cratekit/write/trees.py`
- Source: `r758-b.json`, row `T7_refusal_read_as_an_interruption`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 112 against a baseline of 112
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_refusal_at_the_second_commit_keeps_its_own_cause_and_the_job_says_in_both`

Old text:

```
                if isinstance(exc, cause.CratekitError):
                    raise

```

New text:

```
(empty)
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

### `r501-a.S1_verify_state_guard`

session.mark_import_verified: drop the refusal of any state but awaiting-import, so any record can be marked proven

- File: `src/cratekit/core/session.py`
- Source: `r501-a.json`, row `S1_verify_state_guard`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 175 against a baseline of 175
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_only_a_run_waiting_on_an_import_has_one_to_verify`

Old text:

```
    if record.state is not SessionState.AWAITING_IMPORT:
        raise refuse(
            "internal-error",
            f"session {record.session_id} is {str(record.state)!r}, not "
            f"{str(SessionState.AWAITING_IMPORT)!r}; only a session waiting on an "
            f"import has one to verify",
```

New text:

```
    if False:
        raise refuse(
            "internal-error",
            f"session {record.session_id} is {str(record.state)!r}, not "
            f"{str(SessionState.AWAITING_IMPORT)!r}; only a session waiting on an "
            f"import has one to verify",
```

### `r501-a.S2_excusal_capture`

session.owes_only_deferred_routing: drop the no capture condition, so a run holding a capture is excused from the cutover precheck

- File: `src/cratekit/core/session.py`
- Source: `r501-a.json`, row `S2_excusal_capture`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 175 against a baseline of 175
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_the_precheck_refuses_a_verified_run_that_holds_a_capture`

Old text:

```
        record.state is SessionState.OPEN
        and record.snapshot_path is None
        and IMPORT_VERIFIED_KEY in record.detail
```

New text:

```
        record.state is SessionState.OPEN
        and IMPORT_VERIFIED_KEY in record.detail
```

### `r501-a.S3_excusal_proof`

session.owes_only_deferred_routing: drop the proof condition, so any open run with no capture is excused, a crashed landing included

- File: `src/cratekit/core/session.py`
- Source: `r501-a.json`, row `S3_excusal_proof`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 175 against a baseline of 175
- Kills: 5 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_an_open_run_blocks_the_flip`
  - `tests/test_cutover_precheck.py::test_an_open_run_refuses_the_revert_because_it_may_have_written`
  - `tests/test_intake_imported.py::test_a_run_landed_before_the_fix_is_settled_too`
  - `tests/test_intake_imported.py::test_doctor_reads_a_proven_run_as_proven_and_not_as_in_progress`
  - `tests/test_intake_imported.py::test_the_precheck_refuses_an_open_run_with_no_proof_recorded`

Old text:

```
        record.state is SessionState.OPEN
        and record.snapshot_path is None
        and IMPORT_VERIFIED_KEY in record.detail
```

New text:

```
        record.state is SessionState.OPEN
        and record.snapshot_path is None
```

### `r501-a.S4_excusal_state`

session.owes_only_deferred_routing: drop the open state condition, so a committed-unverified run carrying the key is excused

- File: `src/cratekit/core/session.py`
- Source: `r501-a.json`, row `S4_excusal_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 175 against a baseline of 175
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_the_precheck_refuses_a_verified_run_that_is_not_open`

Old text:

```
        record.state is SessionState.OPEN
        and record.snapshot_path is None
        and IMPORT_VERIFIED_KEY in record.detail
```

New text:

```
        record.snapshot_path is None
        and IMPORT_VERIFIED_KEY in record.detail
```

### `r501-a.T1_precheck_excusal`

tree_registry.assert_cutover_ready: drop the excusal, so a proven landing refuses the cutover for ever, which is R-501 itself

- File: `src/cratekit/core/tree_registry.py`
- Source: `r501-a.json`, row `T1_precheck_excusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 175 against a baseline of 175
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_landing_followed_step_by_step_passes_the_cutover_precheck`
  - `tests/test_intake_imported.py::test_a_run_landed_before_the_fix_is_settled_too`
  - `tests/test_intake_imported.py::test_intake_file_ends_pending_and_is_settled_the_same_way`
  - `tests/test_intake_imported.py::test_the_precheck_excuses_a_verified_run_holding_no_capture`

Old text:

```
        if not record.terminal and not session.owes_only_deferred_routing(record)
```

New text:

```
        if not record.terminal
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

### `u165.L1_bridge_skip`

_land_native: predict a filing on a routing tree still on the bridge

- File: `src/cratekit/intake/land_cli.py`
- Source: `u165.json`, row `L1_bridge_skip`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`, `tests/test_intake_land_native.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_a_routing_tree_on_the_bridge_files_nothing_and_the_screen_names_it`
  - `tests/test_intake_land_native.py::test_three_files_become_three_rows_and_one_playlist_under_the_adopted_root`

Old text:

```
            if medium.files_natively
```

New text:

```
            if True
```

### `u165.L2_land_only`

planner: predict and file under --land-only too

- File: `src/cratekit/intake/land_cli.py`
- Source: `u165.json`, row `L2_land_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`, `tests/test_intake_land_native.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_a_routing_tree_on_the_bridge_files_nothing_and_the_screen_names_it`
  - `tests/test_intake_land_filing.py::test_land_only_files_nothing_and_digests_apart_from_a_landing_that_files`
  - `tests/test_intake_land_native.py::test_three_files_become_three_rows_and_one_playlist_under_the_adopted_root`

Old text:

```
            if unfiled:
                return made
```

New text:

```
            if False:
                return made
```

### `u165.L3_filing_tail`

_land_native: never file after the landing

- File: `src/cratekit/intake/land_cli.py`
- Source: `u165.json`, row `L3_filing_tail`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`, `tests/test_intake_land_native.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_a_collection_read_before_the_commit_does_not_hide_the_landed_rows`
  - `tests/test_intake_land_filing.py::test_a_plan_after_the_commit_that_differs_files_nothing_and_says_so`
  - `tests/test_intake_land_filing.py::test_five_files_land_and_file_under_one_answer`
  - `tests/test_intake_land_filing.py::test_the_filed_rows_are_what_adopt_apply_then_finds_nothing_to_do_for`

Old text:

```
    if predicted is not None:
        # THE FILING
```

New text:

```
    if False:
        # THE FILING
```

### `u165.L4_files_into`

_native_payload: drop each item's files into

- File: `src/cratekit/intake/land_cli.py`
- Source: `u165.json`, row `L4_files_into`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`, `tests/test_intake_land_native.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_a_rehearsal_digests_as_the_live_landing_that_files`
  - `tests/test_intake_land_filing.py::test_five_files_land_and_file_under_one_answer`

Old text:

```
        if str(row.target) in sorted_into:
```

New text:

```
        if False:
```

### `u165.N1_digest`

identity: leave the predictions out of the digest

- File: `src/cratekit/intake/native.py`
- Source: `u165.json`, row `N1_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`, `tests/test_intake_land_native.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_land_only_files_nothing_and_digests_apart_from_a_landing_that_files`

Old text:

```
        {"filing": [one.identity() for one in plan.filing]} if plan.filing is not None else {}
```

New text:

```
        {}
```

### `r1031.M10_filter_against_raw_links`

ledger._load: drop a miss beside a raw link entry with no account track, the review's round one finding

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r1031.json`, row `M10_filter_against_raw_links`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_link_with_no_account_track_does_not_hide_a_miss`

Old text:

```
            and str(content_id) not in linked
```

New text:

```
            and str(content_id) not in links
```

### `r1031.M11_filter_removed`

ledger._load: keep a miss of a row the ledger links

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r1031.json`, row `M11_filter_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_ledger_holding_a_link_and_a_miss_of_one_row_reads_the_link`

Old text:

```
            and str(content_id) not in linked
```

New text:

```
            and True
```

### `r1031.M12_link_keeps_its_miss`

ledger.record_mirror_links: leave the row's miss in the document when it is linked

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r1031.json`, row `M12_link_keeps_its_miss`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_linking_a_row_takes_its_miss_out_of_the_document`

Old text:

```
                document["mirror_misses"].pop(str(content_id), None)
```

New text:

```
                pass
```

### `r1031.M13_miss_written_over_a_link`

ledger.record_mirror_misses: write a miss for a row the ledger already links

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r1031.json`, row `M13_miss_written_over_a_link`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_miss_over_a_linked_row_is_never_written_to_the_document`

Old text:

```
            if str(content_id) in document["mirror_links"]:
                continue
```

New text:

```
            if False:
                continue
```

### `r1031.M8_misses_not_a_map_read`

ledger._load: read a mirror_misses that is not a map instead of refusing

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r1031.json`, row `M8_misses_not_a_map_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_ledger_whose_misses_are_not_a_map_refuses`

Old text:

```
    if not isinstance(misses, Mapping):
        raise _unusable(path, "mirror_misses must be a map of content row to its miss")
```

New text:

```
    if False:
        raise _unusable(path, "mirror_misses must be a map of content row to its miss")
```

### `r1031.M9_malformed_miss_kept`

ledger._load: keep a miss whose key is not a list

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r1031.json`, row `M9_malformed_miss_kept`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_malformed_miss_is_dropped_and_asked_again_rather_than_refusing`

Old text:

```
            and isinstance(value.get("under"), list)
```

New text:

```
            and True
```

### `u174.N1_landed_passes_closed`

landed_passes: drop the closed state check, so an open landing's pass is planned

- File: `src/cratekit/intake/native.py`
- Source: `u174.json`, row `N1_landed_passes_closed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_intake_land_native.py`
- Collected: 228 against a baseline of 228
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_landed_passes_reads_only_closed_committed_landings`

Old text:

```
                and record.state is session.SessionState.CLOSED
                and str(session.SourceState.COMMITTED) in record.sources.values()
                and record.detail.get(PASS_KEY)
            }
```

New text:

```
                and str(session.SourceState.COMMITTED) in record.sources.values()
                and record.detail.get(PASS_KEY)
            }
```

### `u174.N2_landed_passes_committed`

landed_passes: drop the committed source check, so a refused landing's pass is planned

- File: `src/cratekit/intake/native.py`
- Source: `u174.json`, row `N2_landed_passes_committed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_intake_land_native.py`
- Collected: 228 against a baseline of 228
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_landed_passes_reads_only_closed_committed_landings`

Old text:

```
                and record.state is session.SessionState.CLOSED
                and str(session.SourceState.COMMITTED) in record.sources.values()
                and record.detail.get(PASS_KEY)
            }
```

New text:

```
                and record.state is session.SessionState.CLOSED
                and record.detail.get(PASS_KEY)
            }
```

### `u174.N3_landed_passes_workflow`

landed_passes: drop the workflow check, so any closed session naming a pass is read as a landing

- File: `src/cratekit/intake/native.py`
- Source: `u174.json`, row `N3_landed_passes_workflow`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_intake_land_native.py`
- Collected: 228 against a baseline of 228
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_landed_passes_reads_only_closed_committed_landings`

Old text:

```
                if record.workflow == WORKFLOW
                and record.state is session.SessionState.CLOSED
                and str(session.SourceState.COMMITTED) in record.sources.values()
                and record.detail.get(PASS_KEY)
            }
```

New text:

```
                if record.state is session.SessionState.CLOSED
                and str(session.SourceState.COMMITTED) in record.sources.values()
                and record.detail.get(PASS_KEY)
            }
```

### `u174.N4_landed_passes_pass_key`

landed_passes: drop the pass key check, so a landing of no pass is listed as a pass named None

- File: `src/cratekit/intake/native.py`
- Source: `u174.json`, row `N4_landed_passes_pass_key`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_intake_land_native.py`
- Collected: 228 against a baseline of 228
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_landed_passes_reads_only_closed_committed_landings`

Old text:

```
                and str(session.SourceState.COMMITTED) in record.sources.values()
                and record.detail.get(PASS_KEY)
            }
```

New text:

```
                and str(session.SourceState.COMMITTED) in record.sources.values()
            }
```

### `u62.C1_bound_constant_true`

Answer bound() True without asking whether the adapter imports

- File: `src/cratekit/label/catalogue.py`
- Source: `u62.json`, row `C1_bound_constant_true`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/intake/test_workers.py`
- Collected: 544 against a baseline of 544
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_the_catalogue_seam_answers_bound_without_reading_a_credential`

Old text:

```
    try:
        importlib.import_module(ADAPTER_MODULE)
    except ImportError:
        return False
    return True
```

New text:

```
    return True
```

### `u62.C2_outage_as_credential`

Refuse an unreachable provider as a credential problem

- File: `src/cratekit/label/catalogue.py`
- Source: `u62.json`, row `C2_outage_as_credential`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/intake/test_workers.py`
- Collected: 544 against a baseline of 544
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_provider_that_cannot_be_reached_is_a_wait_not_a_new_login[connection]`
  - `tests/test_label_tidal_catalogue.py::test_a_provider_that_cannot_be_reached_is_a_wait_not_a_new_login[server-error]`
  - `tests/test_label_tidal_catalogue.py::test_a_provider_that_cannot_be_reached_is_a_wait_not_a_new_login[timeout]`
  - `tests/test_label_tidal_catalogue.py::test_a_provider_that_cannot_be_reached_is_a_wait_not_a_new_login[unparseable-page]`

Old text:

```
    except ProviderUnavailable as exc:
        raise refuse(
            "unavailable-transient",
```

New text:

```
    except ProviderUnavailable as exc:
        raise refuse(
            "credential-missing",
```

### `sitting3.G8_queue_skips_readiness`

File the job whatever is missing, so a restamp scores nothing and reports ok

- File: `src/cratekit/vocals/cli.py`
- Source: `sitting3.json`, row `G8_queue_skips_readiness`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`
- Collected: 34 against a baseline of 34
- Kills: 2 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_a_missing_checkpoint_is_refused_at_the_queue_and_named`
  - `tests/test_vocals_cli.py::test_a_slim_worker_refuses_at_the_queue_rather_than_reporting_done`

Old text:

```
    if scoring.loader_bound():
        return
    missing = scoring.missing_requirement()
    if missing is None:
        return

```

New text:

```
    if scoring.loader_bound():
        return
    missing = scoring.missing_requirement()
    if True:
        return

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

### `r515-operator.S14_harvest_no_warning`

A harvest over a short playlist carries no warning

- File: `src/cratekit/label/cli.py`
- Source: `r515-operator.json`, row `S14_harvest_no_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_workers.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_harvest_over_a_short_playlist_offers_what_it_read_and_warns`

Old text:

```
        warnings=(harvest_withheld_warning(short, reference),) if short is not None else (),
```

New text:

```
        warnings=(),
```

### `u109-b.B4_resume_dropped`

sync labels refuses even with --job, so a sweep queued before U109 can never run

- File: `src/cratekit/label/cli.py`
- Source: `u109-b.json`, row `B4_resume_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_workers.py`
- Collected: 82 against a baseline of 82
- Kills: 47 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_catalogue_that_cannot_be_listed_fails_the_item_and_the_job`
  - `tests/test_label_workers.py::test_a_job_carrying_no_items_refuses_on_resume_and_is_left_open`
  - `tests/test_label_workers.py::test_a_label_the_registry_no_longer_holds_refuses_rather_than_sweeping_nothing`
  - `tests/test_label_workers.py::test_a_label_verb_will_not_drive_a_job_queued_for_another_verb`
  - `tests/test_label_workers.py::test_a_label_whose_catalogue_the_library_already_holds_offers_nothing`
  - `tests/test_label_workers.py::test_a_label_whose_crawl_listed_nothing_at_all_still_succeeds`
  - `tests/test_label_workers.py::test_a_label_whose_every_release_is_tombstoned_still_succeeds`
  - `tests/test_label_workers.py::test_a_listing_failure_that_is_not_a_rate_limit_stays_permanent`
  - `tests/test_label_workers.py::test_a_mixed_listing_of_tombstoned_and_unconfirmed_releases_is_a_label_with_nothing_new`
  - `tests/test_label_workers.py::test_a_rate_limit_at_every_other_sweep_boundary_is_retryable[artist-resolve]`
  - `tests/test_label_workers.py::test_a_rate_limit_at_every_other_sweep_boundary_is_retryable[listing-probe]`
  - `tests/test_label_workers.py::test_a_rate_limited_listing_fails_its_item_as_retryable_and_the_job_says_resume`
  - `tests/test_label_workers.py::test_a_rate_limited_verification_is_retryable_too`
  - `tests/test_label_workers.py::test_a_refusal_the_artist_lookup_raises_in_kind_keeps_its_own_reason`
  - `tests/test_label_workers.py::test_a_refusal_the_sweep_verifier_raises_in_kind_keeps_its_own_reason`
  - ... and 32 more, see the JSON sidecar

Old text:

```
    if ctx.args.job:
        return _resume(ctx, ctx.args.job)
    raise refuse(
        "verb-retired",
```

New text:

```
    raise refuse(
        "verb-retired",
```

### `u109-b.B6_message_drops_verb`

Reword the refusal message so it no longer names crate label sync

- File: `src/cratekit/label/cli.py`
- Source: `u109-b.json`, row `B6_message_drops_verb`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_workers.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_sync_labels_refuses_to_queue_and_names_the_guided_verb`

Old text:

```
        f"by label with {GUIDED_VERB}, which asks before it downloads anything",
```

New text:

```
        "by label, asking before anything downloads",
```

### `u109-b.B7_step_drops_verb`

Drop the step that names the guided verb from the retired refusal

- File: `src/cratekit/label/cli.py`
- Source: `u109-b.json`, row `B7_step_drops_verb`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_workers.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_sync_labels_refuses_to_queue_and_names_the_guided_verb`

Old text:

```
            f"take label releases with: {GUIDED_VERB}",
            "a sweep queued before this change still runs with: crate sync labels "
```

New text:

```
            "a sweep queued before this change still runs with: crate sync labels "
```

### `u109-b.B8_itemless_branch`

The itemless refusal tells a sweep job to queue the import again, never naming the guided verb

- File: `src/cratekit/label/cli.py`
- Source: `u109-b.json`, row `B8_itemless_branch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_workers.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_the_itemless_refusal_names_the_cancel_that_gets_a_person_out`

Old text:

```
                if job.handler_key == sweep.HANDLER_KEY
```

New text:

```
                if False
```

### `r1184.M19_tag_folder_wiring`

tag folder report: never hand the warning the taxonomy, so the own name answer is dropped

- File: `src/cratekit/tagging/cli.py`
- Source: `r1184.json`, row `M19_tag_folder_wiring`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`, `tests/test_tag_workers.py`, `tests/test_tag_guess.py`
- Collected: 292 against a baseline of 292
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_sweep_names_a_folders_own_name_with_its_one_answer_and_falls_back_when_the_copy_breaks`

Old text:

```
_off_taxonomy_warning(summary, _declared(cfg) if summary.get("off_taxonomy") else None)
```

New text:

```
_off_taxonomy_warning(summary, None)
```

### `r1184.M20_tag_folder_fallback`

tag folder report: drop the catch of an unreadable copy, so the report is refused over a sentence

- File: `src/cratekit/tagging/cli.py`
- Source: `r1184.json`, row `M20_tag_folder_fallback`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`, `tests/test_tag_workers.py`, `tests/test_tag_guess.py`
- Collected: 292 against a baseline of 292
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_sweep_names_a_folders_own_name_with_its_one_answer_and_falls_back_when_the_copy_breaks`

Old text:

```
    try:
        return active_taxonomy.load(cfg)
    except CratekitError:
        return None
```

New text:

```
    return active_taxonomy.load(cfg)
```

### `r1184.M21_guess_wiring`

tag guess: drop the own name sentence from the off taxonomy warning

- File: `src/cratekit/tagging/guess_cli.py`
- Source: `r1184.json`, row `M21_guess_wiring`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`, `tests/test_tag_workers.py`, `tests/test_tag_guess.py`
- Collected: 292 against a baseline of 292
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_folders_own_name_in_another_case_is_named_with_its_one_answer`

Old text:

```
                    + taxonomy_word.own_names(declared, found.off_taxonomy)

```

New text:

```
(empty)
```

### `r835-b.T1_folder_create_never_retried`

TidalAccount.create_folder: a create that timed out after reaching the provider is retried into a second folder

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r835-b.json`, row `T1_folder_create_never_retried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_folder_create_is_never_retried_into_a_second_folder`

Old text:

```
            doing, lambda: self._session.user.create_folder(name), retries=0
```

New text:

```
            doing, lambda: self._session.user.create_folder(name), retries=1
```

### `r835-b.T2_refused_move_raised`

TidalAccount.move_to_folder: a move the client answers False is returned as done

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r835-b.json`, row `T2_refused_move_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_move_the_client_answers_false_is_a_failure_not_a_quiet_return`

Old text:

```
        if moved is False or moved is _ABSENT:
```

New text:

```
        if moved is _ABSENT:
```

### `r835-c.T3_short_answer_read_again_again`

TidalAccount.add_tracks: an add answer that leaves a track out is trusted, so a track the playlist holds is reported refused

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r835-c.json`, row `T3_short_answer_read_again_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_an_add_answered_with_nothing_is_read_again_and_not_reported_refused`

Old text:

```
            if unconfirmed:
                del self._members[playlist_id]
```

New text:

```
            if False:
                del self._members[playlist_id]
```

### `u44-author.C2_argv_drops_overwrite`

Drop --overwrite from the resume argv, so a respawned child meets the refusal the first run was told to ignore

- File: `src/cratekit/master/cli.py`
- Source: `u44-author.json`, row `C2_argv_drops_overwrite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_master_cli.py`
- Collected: 73 against a baseline of 73
- Kills: 2 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_split_recording_and_its_target_survive_the_resume_argv`
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

### `u44-author.C3_argv_drops_output_dir`

Drop --output-dir from the resume argv, so the child writes the master somewhere the person did not ask for

- File: `src/cratekit/master/cli.py`
- Source: `u44-author.json`, row `C3_argv_drops_output_dir`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_master_cli.py`
- Collected: 73 against a baseline of 73
- Kills: 2 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_split_recording_and_its_target_survive_the_resume_argv`
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

### `u44-author.C4_refusal_not_translated`

Let MasteringRefused escape, so every engine refusal reaches the person as internal-error

- File: `src/cratekit/master/cli.py`
- Source: `u44-author.json`, row `C4_refusal_not_translated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_master_cli.py`
- Collected: 73 against a baseline of 73
- Kills: 23 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_24_bit_and_a_32_bit_part_are_told_apart_by_codec_alone`
  - `tests/test_master_cli.py::test_a_container_the_engine_does_not_read_refuses_under_its_own_slug`
  - `tests/test_master_cli.py::test_a_corrupt_archive_copy_refuses_and_leaves_no_false_safety_copy`
  - `tests/test_master_cli.py::test_a_failed_encode_under_overwrite_says_what_the_person_is_left_holding`
  - `tests/test_master_cli.py::test_a_failing_encode_does_not_report_success`
  - `tests/test_master_cli.py::test_a_job_that_failed_on_a_missing_source_is_not_reopened_and_a_fresh_job_masters_it`
  - `tests/test_master_cli.py::test_a_missing_encoder_reports_that_refusal_rather_than_an_internal_defect`
  - `tests/test_master_cli.py::test_a_missing_part_refuses_as_missing`
  - `tests/test_master_cli.py::test_a_missing_recording_reports_the_engines_own_cause_on_the_item`
  - `tests/test_master_cli.py::test_a_part_named_twice_refuses`
  - `tests/test_master_cli.py::test_a_recording_that_is_not_there_refuses_rather_than_raising`
  - `tests/test_master_cli.py::test_an_archive_holding_different_audio_refuses_and_keeps_both`
  - `tests/test_master_cli.py::test_an_encode_that_exits_zero_and_writes_nothing_does_not_report_success`
  - `tests/test_master_cli.py::test_an_encode_that_produces_nothing_reaches_the_item_as_the_engines_own_cause`
  - `tests/test_master_cli.py::test_an_encode_that_writes_an_empty_file_does_not_report_success`
  - ... and 8 more, see the JSON sidecar

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

### `u44-author.C6_overwrite_always_true`

Freeze overwrite as always true, so every run replaces an existing master without being asked to

- File: `src/cratekit/master/cli.py`
- Source: `u44-author.json`, row `C6_overwrite_always_true`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_master_cli.py`
- Collected: 73 against a baseline of 73
- Kills: 4 (killed)
- Killed:
  - `tests/test_master_cli.py::test_an_existing_joined_master_is_refused_on_the_real_destination`
  - `tests/test_master_cli.py::test_an_existing_master_is_refused_before_the_engine_runs`
  - `tests/test_master_cli.py::test_an_existing_master_refuses_without_overwrite_and_proceeds_with_it`
  - `tests/test_master_cli.py::test_one_input_freezes_queues_and_resumes_exactly_as_before`

Old text:

```
        OVERWRITE: bool(overwrite),
```

New text:

```
        OVERWRITE: True,
```

### `u44-author.C7_output_dir_ignored_at_the_work`

Ignore the frozen output directory, so the master lands beside the source whatever was asked for

- File: `src/cratekit/master/cli.py`
- Source: `u44-author.json`, row `C7_output_dir_ignored_at_the_work`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_master_cli.py`
- Collected: 73 against a baseline of 73
- Kills: 3 (killed)
- Killed:
  - `tests/test_master_cli.py::test_overwrite_reaches_the_handler_and_replaces_the_previous_master`
  - `tests/test_master_cli.py::test_the_encode_lands_in_staging_and_is_committed_rather_than_written_in_place`
  - `tests/test_master_cli.py::test_the_output_directory_is_honoured_and_never_the_source`

Old text:

```
            output_dir=Path(output_dir) if output_dir else None,
```

New text:

```
            output_dir=None,
```

