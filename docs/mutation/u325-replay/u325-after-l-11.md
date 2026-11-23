# Mutation table: u325-after-l-11

Measured by `scripts/mutate.py` on 2026-11-23 02:23 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 18.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:20 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 8, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard. 105 row(s) were reused from a prior sidecar and were measured by an earlier process, whose children this run did not watch.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r879-a.C6_settled_early_without_several` | `src/cratekit/intake/candidates.py` | maintainer | 1 file(s) | 56 | 1 | killed |
| `r879-a.C7_bound_off_by_one` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 2 | killed |
| `r879-a.C9_read_pages_forgets_last_page` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 5 | killed |
| `r879-b.C5r_settled_early_without_unnamed_exact` | `src/cratekit/intake/candidates.py` | maintainer | 1 file(s) | 56 | 1 | killed |
| `r879-b.C8r_ceiling_coefficient` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 1 | killed |
| `r923.N12_digest_drops_values` | `src/cratekit/write/row_defaults.py` | maintainer | 1 file(s) | 22933 | 0 (promoted) | zero |
| `r1308.M10_count_unchecked` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u172-b.A14_write_false_trusted` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 1 | killed |
| `u172-b.A16_tombstone_votes` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 1 | killed |
| `u172.A10_tie_not_broken_by_artist` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 1 | killed |
| `u172.A11_split_not_written` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 3 | killed |
| `u172.A12_fraction_into_weigh` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 2 | killed |
| `u172.A13_report_writes` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 1 | killed |
| `u172.A15_read_back_skipped` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 1 | killed |
| `u172.A17_bound_read_as_float` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 3 | killed |
| `u172.A1_unreadable_read_as_blank` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 1 | killed |
| `u172.A2_tagged_file_is_a_candidate` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 7 | killed |
| `u172.A3_off_taxonomy_never_named` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 3 | killed |
| `u172.A5_same_artist_votes_twice` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 1 | killed |
| `u172.A6_vote_per_member` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 5 | killed |
| `u172.A7_playlist_weight_halved` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 6 | killed |
| `u172.A8_artist_weight_halved` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 6 | killed |
| `u172.A9_folder_artist_ignored` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 5 | killed |
| `u172.B1_library_read_for_nothing` | `src/cratekit/tagging/guess_cli.py` | user | 1 file(s) | 119 | 1 | killed |
| `u172.B2_unknown_pass_silent` | `src/cratekit/tagging/guess_cli.py` | user | 1 file(s) | 119 | 1 | killed |
| `u172.B3_pass_ignored` | `src/cratekit/tagging/guess_cli.py` | user | 1 file(s) | 119 | 3 | killed |
| `u172.B4_outcome_ok_always` | `src/cratekit/tagging/guess_cli.py` | user | 1 file(s) | 119 | 4 | killed |
| `u172.B5_missing_folder_walked` | `src/cratekit/tagging/guess_cli.py` | user | 1 file(s) | 119 | 1 | killed |
| `r372-a.A10_copy_left_behind` | `src/cratekit/core/rb_writer.py` | maintainer | 3 file(s) | 494 | 15 | killed |
| `r372-a.A11_copy_under_a_running_application` | `src/cratekit/core/rb_writer.py` | maintainer | 3 file(s) | 494 | 1 | killed |
| `r372-a.A12_separator_kept` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 494 | 7 | killed |
| `r372-a.A1_majority_boundary` | `src/cratekit/write/metadata_cli.py` | user | 3 file(s) | 494 | 1 | killed |
| `r372-a.A2_majority_coefficient` | `src/cratekit/write/metadata_cli.py` | user | 3 file(s) | 494 | 1 | killed |
| `r372-a.A3_pathless_rows_count_as_unmapped` | `src/cratekit/write/metadata_cli.py` | user | 3 file(s) | 494 | 17 | killed |
| `r372-a.A4_verb_never_refuses` | `src/cratekit/write/metadata_cli.py` | user | 3 file(s) | 494 | 2 | killed |
| `r372-a.A5_apply_proceeds` | `src/cratekit/write/metadata_cli.py` | user | 3 file(s) | 494 | 1 | killed |
| `r372-a.A6_decode_error_escapes` | `src/cratekit/write/metadata_cli.py` | user | 3 file(s) | 494 | 1 | killed |
| `r372-a.A7_remedy_run_doctor` | `src/cratekit/write/metadata_cli.py` | user | 3 file(s) | 494 | 3 | killed |
| `r372-a.A8_refused_plan_reports_ok` | `src/cratekit/write/metadata_cli.py` | user | 3 file(s) | 494 | 2 | killed |
| `r381-b.M12_add_legacy_any_name` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 1 | killed |
| `r381.M10_by_id_no_follow` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 1 | killed |
| `r381.M11_add_ignores_legacy` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 1 | killed |
| `r381.M1_fold_only_slug` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 13 | killed |
| `r381.M2_no_umlaut_table` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 6 | killed |
| `r381.M3_keep_combining_marks` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 10 | killed |
| `r381.M4_migrate_ignores_taken` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 2 | killed |
| `r381.M5_migrate_any_identifier` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 4 | killed |
| `r381.M6_update_skips_move_write` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 1 | killed |
| `r381.M7_load_never_migrates` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 4 | killed |
| `r381.M8_no_renamed_map` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 2 | killed |
| `r381.M9_live_renames_unfiltered` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 2 | killed |
| `u107-c.S19_approved_superseded` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `r515-operator.S8_short_of_keeps_zero` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `r515-operator.S9_question_no_short` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u107-a.S03_marker_moves` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 13 | killed |
| `u107-a.S04_marker_takes_window_place` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 8 | killed |
| `u107-a.S07_gate_before_asking` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u107-a.S08_catch_up_withhold` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 2 | killed |
| `u107-b.S10_pick_unknown` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 2 | killed |
| `u107-b.S11_pick_takes_only_chosen` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 7 | killed |
| `u107-b.S12_stop_removes` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 3 | killed |
| `u107-b.S13_take_accepts` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 10 | killed |
| `u107-b.S15_no_default_answer` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u107-b.S16_save_before_ask` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 9 | killed |
| `u107-b.S17_dead_verifier_skip` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u107-c.S20_pick_isdecimal` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u107-c.S21_filing_run` | `src/cratekit/label/sync_cli.py` | maintainer | 1 file(s) | 94 | 1 | killed |
| `u107-c.S23_stop_remedy` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u107-c.S24_size_coefficient` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 2 | killed |
| `u107-d.S02_record_version_again` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u107-d.S14_take_respects_decided_again` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u107-d.S25_measured_passes_refusal_again` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `r515-operator.S6_cache_drops_short` | `src/cratekit/label/catalogue.py` | user | 1 file(s) | 94 | 1 | killed |
| `r1499.L01_go_arrival_after_tail` | `src/cratekit/cli/label_sync.py` | user | 6 file(s) | 324 | 1 | killed |
| `r1499.S01_download_reading` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 324 | 12 | killed |
| `r1499.S02_tail_reading` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 324 | 1 | killed |
| `r1499.S03_arrival_after_tail` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 324 | 2 | killed |
| `r1499.S04_arrival_after_plan` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 324 | 1 | killed |
| `r1499.S05_keep_after_arrival` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 324 | 2 | killed |
| `r1499.S06_keep_called` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 324 | 7 | killed |
| `r1499.S07_kept_read` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 324 | 4 | killed |
| `r1499.S08_own_pass_proof` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 324 | 2 | killed |
| `r1499.S09_own_library` | `src/cratekit/cli/sync_land.py` | maintainer | 6 file(s) | 324 | 1 | killed |
| `r1499.S10_own_by_list` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 324 | 66 | killed |
| `r1499.S11_unreadable_refuses` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 324 | 1 | killed |
| `r1499.S12_warnings_in_refusal` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 324 | 1 | killed |
| `r1499.S13_own_unnamed_step` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 324 | 1 | killed |
| `r301.B1_shipped_month_unbounded` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 5 | killed |
| `r301.B2_bound_host_ignored` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 3 | killed |
| `r301.B3_refusal_detail_no_key` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 5 | killed |
| `r301.B4_refusal_message_no_key` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 3 | killed |
| `r301.S1_month_ignores_ledger` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 6 | killed |
| `u57-recognition-and-items.M11_unreached_stop_tenfold` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 2 | killed |
| `u57-recognition-and-items.M12_quota_reads_as_failure` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 4 | killed |
| `u57-recognition-and-items.M16_grid_off_by_one` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 69 | killed |
| `u57-recognition-and-items.M18_missing_credential_is_unready` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 1 | killed |
| `u57-recognition-and-items.M1_miss_family_loses_1001` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 48 | killed |
| `u57-recognition-and-items.M2_quota_family_empty` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 6 | killed |
| `u57-recognition-and-items.M3_auth_family_loses_3001` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 2 | killed |
| `u57-recognition-and-items.M4_transient_range_dropped` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 4 | killed |
| `u57-recognition-and-items.M5_empty_music_not_none` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 1 | killed |
| `u57-recognition-and-items.M6_score_constant` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 2 | killed |
| `u57-recognition-and-items.M7_fold_never_takes_best_score` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 1 | killed |
| `u69-b.M10_out_not_a_folder` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `u69-b.M12_unlisted_status` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `u69-b.M16_next_command` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u69-b.M17_lists_folder` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 8 | killed |
| `u69-b.M18_inner_cause` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `u69-b.M19_resume_step` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `u69.M1_handler_key` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `u69.M2_succeeded_only` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 2 | killed |
| `u69.M4_report_coverage` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 2 | killed |
| `u69.M5_by_count` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 1 | killed |

## Zero rows and what they owe

- `r923.N12_digest_drops_values` (maintainer facing): maintainer facing, composite not required
- `r1308.M10_count_unchecked` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u69-b.M16_next_command` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `r879-a.C6_settled_early_without_several`

_settled_early: drop two distinct exact candidates, so a settled several reads a second page

- File: `src/cratekit/intake/candidates.py`
- Source: `r879-a.json`, row `C6_settled_early_without_several`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_two_exact_matches_on_the_first_page_read_no_second`

Old text:

```
        or len(answer.exact_refs) > 1

```

New text:

```
        or len(answer.exact_refs) > 2

```

### `r879-a.C7_bound_off_by_one`

search_pages: let the bound allow one page more, so the walk asks offset 300, past the ceiling

- File: `src/cratekit/intake/candidates.py`
- Source: `r879-a.json`, row `C7_bound_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set.py::test_the_page_bound_reached_leaves_it_out_and_says_so`
  - `tests/test_export_set.py::test_the_walk_never_asks_past_the_providers_ceiling_of_300`

Old text:

```
        if not answer.full or _settled_early(answer) or len(pages) >= bound:
```

New text:

```
        if not answer.full or _settled_early(answer) or len(pages) > bound:
```

### `r879-a.C9_read_pages_forgets_last_page`

read_pages: carry no last page, so a two page answer is judged on its total

- File: `src/cratekit/intake/candidates.py`
- Source: `r879-a.json`, row `C9_read_pages_forgets_last_page`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 5 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_full_first_page_with_one_exact_and_a_second_with_none_lists_it`
  - `tests/test_export_set.py::test_an_empty_page_after_full_ones_ends_the_listing_and_a_full_last_page_never_lists`
  - `tests/test_export_set.py::test_an_exact_match_on_the_second_page_alone_is_listed`
  - `tests/test_export_set.py::test_no_exact_match_on_any_page_leaves_it_out_as_none`
  - `tests/test_export_set.py::test_the_same_exact_track_served_again_on_the_next_page_is_one`

Old text:

```
    return replace(answer, pages=len(pages), last_page=len(pages[-1]) if pages else 0)
```

New text:

```
    return replace(answer, pages=len(pages), last_page=None)
```

### `r879-b.C5r_settled_early_without_unnamed_exact`

rerun of C5 after its zero: _settled_early drops the exact candidate with no identifier

- File: `src/cratekit/intake/candidates.py`
- Source: `r879-b.json`, row `C5r_settled_early_without_unnamed_exact`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_an_exact_match_with_no_identifier_on_a_full_page_reads_no_second_page`

Old text:

```
        or any(not one.track.ref for one in exact)

```

New text:

```
        or False

```

### `r879-b.C8r_ceiling_coefficient`

rerun of C8 after its zero: SEARCH_CEILING 300 to 350, so the derived bound is seven pages

- File: `src/cratekit/intake/candidates.py`
- Source: `r879-b.json`, row `C8r_ceiling_coefficient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_the_walk_never_asks_past_the_providers_ceiling_of_300`

Old text:

```
SEARCH_CEILING = 300
```

New text:

```
SEARCH_CEILING = 350
```

### `r923.N12_digest_drops_values`

The digest no longer covers the values written

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N12_digest_drops_values`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                "defaults": {column: str(value) for column, value in rb_writer.CONTENT_ROW_DEFAULTS.items()},

```

New text:

```
(empty)
```

### `r1308.M10_count_unchecked`

_removal_read_back: drop the whole number check on the count

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M10_count_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
if not _count(declared) or not _count(videos) or videos != 0
```

New text:

```
if not _count(videos) or videos != 0
```

### `u172-b.A14_write_false_trusted`

write: trust the writer's answer, so a file that would not take the genre is reported guessed

- File: `src/cratekit/tagging/guess.py`
- Source: `u172-b.json`, row `A14_write_false_trusted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_file_that_will_not_take_its_genre_is_never_reported_guessed`

Old text:

```
        if not tags.write_genre(item.path, item.genre):
```

New text:

```
        if tags.write_genre(item.path, item.genre) and False:
```

### `u172-b.A16_tombstone_votes`

library_by_artist: a soft deleted row votes

- File: `src/cratekit/tagging/guess.py`
- Source: `u172-b.json`, row `A16_tombstone_votes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_soft_deleted_row_is_no_neighbour`

Old text:

```
        if trees.soft_delete_marker(row):
            continue
```

New text:

```
        if False:
            continue
```

### `u172.A10_tie_not_broken_by_artist`

_broken: a split goes to the first by name only, ignoring the artist's weight

- File: `src/cratekit/tagging/guess.py`
- Source: `u172.json`, row `A10_tie_not_broken_by_artist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_three_way_tie_goes_to_the_artist_then_to_the_name`

Old text:

```
    return sorted(tied, key=lambda word: (-artist.get(word, 0), word))[0]
```

New text:

```
    return sorted(tied)[0]
```

### `u172.A11_split_not_written`

plan: a split writes no genre, contrary to Phillip's write every guess

- File: `src/cratekit/tagging/guess.py`
- Source: `u172.json`, row `A11_split_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_three_way_tie_goes_to_the_artist_then_to_the_name`
  - `tests/test_tag_guess.py::test_a_tie_is_warned_with_the_genre_it_was_written_as`
  - `tests/test_tag_guess.py::test_a_tie_no_artist_breaks_goes_to_the_first_by_name`

Old text:

```
        if band == suggest.SPLIT:
            genre = _broken(tied, artist)
```

New text:

```
        if band == suggest.SPLIT:
            genre = ''
```

### `u172.A12_fraction_into_weigh`

plan: drop the exact band, so tag suggest's float band_of decides, the rounds 1 and 2 defect

- File: `src/cratekit/tagging/guess.py`
- Source: `u172.json`, row `A12_fraction_into_weigh`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_an_exact_bound_over_a_playlist_and_an_artist_is_banded_exactly`
  - `tests/test_tag_guess.py::test_an_exact_eighty_percent_share_is_high_as_tag_suggest_says`

Old text:

```
        if band in suggest.BANDS:
```

New text:

```
        if False:
```

### `u172.A13_report_writes`

write: drop the report's early return, so --report writes

- File: `src/cratekit/tagging/guess.py`
- Source: `u172.json`, row `A13_report_writes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_report_writes_nothing_and_says_what_a_run_would`

Old text:

```
    if found.report:
        return found
```

New text:

```
    if False:
        return found
```

### `u172.A15_read_back_skipped`

write: skip the read back, so a file reading back another genre is reported guessed

- File: `src/cratekit/tagging/guess.py`
- Source: `u172.json`, row `A15_read_back_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_file_that_reads_back_another_genre_is_unwritten`

Old text:

```
        if back != item.genre:
```

New text:

```
        if False:
```

### `u172.A17_bound_read_as_float`

band_of: compare the exact share with the float bound, so an exact eighty percent reads medium

- File: `src/cratekit/tagging/guess.py`
- Source: `u172.json`, row `A17_bound_read_as_float`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_an_exact_bound_over_a_playlist_and_an_artist_is_banded_exactly`
  - `tests/test_tag_guess.py::test_an_exact_eighty_percent_share_is_high_as_tag_suggest_says`
  - `tests/test_tag_guess.py::test_the_exact_band_agrees_with_tag_suggests_on_every_whole_vote[8-10]`

Old text:

```
        if share >= Fraction(str(least)) and total >= votes:
```

New text:

```
        if share >= least and total >= votes:
```

### `u172.A1_unreadable_read_as_blank`

plan: drop the unreadable branch, so a file whose genre could not be read is a candidate and written over

- File: `src/cratekit/tagging/guess.py`
- Source: `u172.json`, row `A1_unreadable_read_as_blank`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_file_whose_genre_could_not_be_read_is_not_a_blank`

Old text:

```
        if not one.readable:
```

New text:

```
        if False:
```

### `u172.A2_tagged_file_is_a_candidate`

plan: drop the fill if empty branch, so a file carrying a genre is guessed and overwritten

- File: `src/cratekit/tagging/guess.py`
- Source: `u172.json`, row `A2_tagged_file_is_a_candidate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 7 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_file_with_a_genre_is_never_a_candidate_and_its_off_taxonomy_word_is_named`
  - `tests/test_tag_guess.py::test_a_folder_that_needs_no_guess_opens_no_library`
  - `tests/test_tag_guess.py::test_a_folders_own_name_in_another_case_is_named_with_its_one_answer`
  - `tests/test_tag_guess.py::test_an_off_taxonomy_word_is_named_with_both_offers`
  - `tests/test_tag_guess.py::test_the_artists_tracks_in_the_folder_vote_too`
  - `tests/test_tag_guess.py::test_the_share_before_and_after_counts_the_files_carrying_a_genre`
  - `tests/test_tag_guess.py::test_the_verb_writes_each_guess_and_never_touches_a_tagged_file`

Old text:

```
        if one.genre:
            if off_taxonomy
```

New text:

```
        if False:
            if off_taxonomy
```

### `u172.A3_off_taxonomy_never_named`

plan: never name an off taxonomy word on a staged file, so the review offers nothing

- File: `src/cratekit/tagging/guess.py`
- Source: `u172.json`, row `A3_off_taxonomy_never_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_file_with_a_genre_is_never_a_candidate_and_its_off_taxonomy_word_is_named`
  - `tests/test_tag_guess.py::test_a_folders_own_name_in_another_case_is_named_with_its_one_answer`
  - `tests/test_tag_guess.py::test_an_off_taxonomy_word_is_named_with_both_offers`

Old text:

```
            if off_taxonomy(declared, one.genre):
```

New text:

```
            if False:
```

### `u172.A5_same_artist_votes_twice`

_share: keep the artist's own tracks in the playlist's share, so they vote twice

- File: `src/cratekit/tagging/guess.py`
- Source: `u172.json`, row `A5_same_artist_votes_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_track_by_the_same_artist_votes_once_as_the_artists`

Old text:

```
        if not member.genre or (own and artist_key(member.artist) == own):
```

New text:

```
        if not member.genre:
```

### `u172.A6_vote_per_member`

_share: a vote per member rather than one shared voice, so a long playlist drowns the artist

- File: `src/cratekit/tagging/guess.py`
- Source: `u172.json`, row `A6_vote_per_member`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 5 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_long_playlist_does_not_drown_three_tracks_by_the_artist`
  - `tests/test_tag_guess.py::test_a_playlist_share_on_an_exact_bound_is_banded_as_the_ints_would_be`
  - `tests/test_tag_guess.py::test_a_three_way_tie_goes_to_the_artist_then_to_the_name`
  - `tests/test_tag_guess.py::test_a_track_by_the_same_artist_votes_once_as_the_artists`
  - `tests/test_tag_guess.py::test_an_exact_bound_over_a_playlist_and_an_artist_is_banded_exactly`

Old text:

```
Fraction(PLAYLIST_WEIGHT * count, total)
```

New text:

```
Fraction(count)
```

### `u172.A7_playlist_weight_halved`

PLAYLIST_WEIGHT: halve the playlist's voice, from four to two

- File: `src/cratekit/tagging/guess.py`
- Source: `u172.json`, row `A7_playlist_weight_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 6 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_long_playlist_does_not_drown_three_tracks_by_the_artist`
  - `tests/test_tag_guess.py::test_a_playlist_mostly_of_one_genre_gives_it_to_a_track_no_artist_knows`
  - `tests/test_tag_guess.py::test_a_playlist_share_on_an_exact_bound_is_banded_as_the_ints_would_be`
  - `tests/test_tag_guess.py::test_a_three_way_tie_goes_to_the_artist_then_to_the_name`
  - `tests/test_tag_guess.py::test_a_track_by_the_same_artist_votes_once_as_the_artists`
  - `tests/test_tag_guess.py::test_an_exact_bound_over_a_playlist_and_an_artist_is_banded_exactly`

Old text:

```
PLAYLIST_WEIGHT = 4
```

New text:

```
PLAYLIST_WEIGHT = 2
```

### `u172.A8_artist_weight_halved`

_artist_votes: an artist neighbour weighs one rather than two

- File: `src/cratekit/tagging/guess.py`
- Source: `u172.json`, row `A8_artist_weight_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 6 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_long_playlist_does_not_drown_three_tracks_by_the_artist`
  - `tests/test_tag_guess.py::test_a_three_way_tie_goes_to_the_artist_then_to_the_name`
  - `tests/test_tag_guess.py::test_a_track_by_the_same_artist_votes_once_as_the_artists`
  - `tests/test_tag_guess.py::test_an_exact_bound_over_a_playlist_and_an_artist_is_banded_exactly`
  - `tests/test_tag_guess.py::test_an_exact_eighty_percent_share_is_high_as_tag_suggest_says`
  - `tests/test_tag_guess.py::test_the_artists_tracks_in_the_library_give_the_genre`

Old text:

```
        votes[word] += ARTIST_WEIGHT
```

New text:

```
        votes[word] += 1
```

### `u172.A9_folder_artist_ignored`

_artist_votes: the folder's own tracks by the artist give no vote

- File: `src/cratekit/tagging/guess.py`
- Source: `u172.json`, row `A9_folder_artist_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 5 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_track_by_the_same_artist_votes_once_as_the_artists`
  - `tests/test_tag_guess.py::test_an_unreadable_library_is_said_and_the_folder_still_votes`
  - `tests/test_tag_guess.py::test_the_artists_tracks_in_the_folder_vote_too`
  - `tests/test_tag_guess.py::test_the_share_before_and_after_counts_the_files_carrying_a_genre`
  - `tests/test_tag_guess.py::test_the_verb_writes_each_guess_and_never_touches_a_tagged_file`

Old text:

```
        if one.path != candidate.path and one.genre and artist_key(one.artist) == own
```

New text:

```
        if False
```

### `u172.B1_library_read_for_nothing`

signals: read the library and the pass even when no file needs a genre

- File: `src/cratekit/tagging/guess_cli.py`
- Source: `u172.json`, row `B1_library_read_for_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_folder_that_needs_no_guess_opens_no_library`

Old text:

```
    if not any(one.readable and not one.genre for one in staged):
```

New text:

```
    if False:
```

### `u172.B2_unknown_pass_silent`

_playlists: read a pass no job carries as no playlists, the round 1 defect

- File: `src/cratekit/tagging/guess_cli.py`
- Source: `u172.json`, row `B2_unknown_pass_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_pass_no_job_carries_is_said_and_never_read_as_no_playlists`

Old text:

```
        if not batch_name.pass_jobs(cfg, pass_name):
```

New text:

```
        if False:
```

### `u172.B3_pass_ignored`

signals: never read the pass's playlists

- File: `src/cratekit/tagging/guess_cli.py`
- Source: `u172.json`, row `B3_pass_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_pass_no_job_carries_is_said_and_never_read_as_no_playlists`
  - `tests/test_tag_guess.py::test_a_pass_that_cannot_be_read_is_said_and_the_artist_still_votes`
  - `tests/test_tag_guess.py::test_the_pass_names_the_playlists_that_vote`

Old text:

```
    if pass_name:
        playlists, playlists_unread
```

New text:

```
    if False:
        playlists, playlists_unread
```

### `u172.B4_outcome_ok_always`

tag_guess: answer OK when nothing was written

- File: `src/cratekit/tagging/guess_cli.py`
- Source: `u172.json`, row `B4_outcome_ok_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_file_that_will_not_take_its_genre_is_never_reported_guessed`
  - `tests/test_tag_guess.py::test_a_folder_that_needs_no_guess_opens_no_library`
  - `tests/test_tag_guess.py::test_a_report_writes_nothing_and_says_what_a_run_would`
  - `tests/test_tag_guess.py::test_no_pass_reads_no_playlist`

Old text:

```
        outcome=Outcome.OK if written else Outcome.NO_OP,
```

New text:

```
        outcome=Outcome.OK,
```

### `u172.B5_missing_folder_walked`

tag_guess: drop the refusal of a folder that is not there

- File: `src/cratekit/tagging/guess_cli.py`
- Source: `u172.json`, row `B5_missing_folder_walked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_folder_that_is_not_there_refuses`

Old text:

```
    if not root.is_dir():
```

New text:

```
    if False:
```

### `r372-a.A10_copy_left_behind`

disposable_copy: leave the temporary directory and the copy in it

- File: `src/cratekit/core/rb_writer.py`
- Source: `r372-a.json`, row `A10_copy_left_behind`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 15 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_doctor_fails_paths_resolved_over_a_majority_off_a_copy`
  - `tests/test_paths_resolved.py::test_doctor_reports_a_copy_it_could_not_open_as_unknown_rather_than_good`
  - `tests/test_paths_resolved.py::test_doctor_reports_a_minority_as_a_note_and_a_clean_collection_as_ok`
  - `tests/test_paths_resolved.py::test_setup_end_to_end_writes_the_rule_and_ends_on_a_doctor_that_reads_it`
  - `tests/test_paths_resolved.py::test_setup_leaves_a_damaged_library_to_the_notes_and_doctor`
  - `tests/test_paths_resolved.py::test_setup_notes_a_copy_it_could_not_open_and_leaves_the_verdict_to_doctor`
  - `tests/test_paths_resolved.py::test_setup_offers_nothing_when_the_root_sits_under_the_recorded_drive`
  - `tests/test_paths_resolved.py::test_setup_offers_nothing_when_the_two_drive_names_agree`
  - `tests/test_paths_resolved.py::test_setup_offers_the_root_when_rekordbox_still_records_the_old_name_twice`
  - `tests/test_paths_resolved.py::test_setup_offers_the_rule_from_the_databases_own_drive_names_off_a_copy`
  - `tests/test_paths_resolved.py::test_setup_records_a_current_drive_that_is_not_the_root_literally`
  - `tests/test_paths_resolved.py::test_setup_records_nothing_when_the_offer_goes_unanswered`
  - `tests/test_paths_resolved.py::test_the_copy_names_a_file_holding_none_of_the_canary_tables`
  - `tests/test_paths_resolved.py::test_the_copy_names_an_empty_file_by_its_size_and_its_configured_path`
  - `tests/test_paths_resolved.py::test_the_disposable_copy_is_private_and_gone_afterwards`

Old text:

```
        shutil.rmtree(directory, ignore_errors=True)
```

New text:

```
        pass
```

### `r372-a.A11_copy_under_a_running_application`

read_only_copy: drop its own closed assertion, the layer beneath doctor and setup

- File: `src/cratekit/core/rb_writer.py`
- Source: `r372-a.json`, row `A11_copy_under_a_running_application`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 1 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_the_read_only_copy_refuses_under_a_running_application_on_its_own`

Old text:

```
    assert_rekordbox_closed("copying the database for a read only look")
```

New text:

```
    pass
```

### `r372-a.A12_separator_kept`

recorded_db_drives: keep the trailing separator rekordbox stores, so the rule never matches

- File: `src/cratekit/core/rb_writer.py`
- Source: `r372-a.json`, row `A12_separator_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 7 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_recorded_drives_strip_the_separator_rekordbox_stores_and_blank_is_none`
  - `tests/test_paths_resolved.py::test_setup_end_to_end_writes_the_rule_and_ends_on_a_doctor_that_reads_it`
  - `tests/test_paths_resolved.py::test_setup_offers_nothing_when_the_root_sits_under_the_recorded_drive`
  - `tests/test_paths_resolved.py::test_setup_offers_nothing_when_the_two_drive_names_agree`
  - `tests/test_paths_resolved.py::test_setup_offers_the_root_when_rekordbox_still_records_the_old_name_twice`
  - `tests/test_paths_resolved.py::test_setup_offers_the_rule_from_the_databases_own_drive_names_off_a_copy`
  - `tests/test_paths_resolved.py::test_setup_records_a_current_drive_that_is_not_the_root_literally`

Old text:

```
        stripped = value.strip().rstrip("/\\")
```

New text:

```
        stripped = value.strip()
```

### `r372-a.A1_majority_boundary`

majority_unmapped: half is a majority, so 5 of 10 refuses

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r372-a.json`, row `A1_majority_boundary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 1 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_a_majority_is_strictly_more_than_half_and_never_an_empty_collection[10-5-False]`

Old text:

```
        return self.active > 0 and self.unmapped * 2 > self.active
```

New text:

```
        return self.active > 0 and self.unmapped * 2 >= self.active
```

### `r372-a.A2_majority_coefficient`

majority_unmapped: two thirds rather than half, so 6 of 10 is not a majority

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r372-a.json`, row `A2_majority_coefficient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 1 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_a_majority_is_strictly_more_than_half_and_never_an_empty_collection[10-5-False]`

Old text:

```
        return self.active > 0 and self.unmapped * 2 > self.active
```

New text:

```
        return self.active > 0 and self.unmapped * 3 > self.active
```

### `r372-a.A3_pathless_rows_count_as_unmapped`

_survey: count every row that did not resolve as unmapped, streaming rows included

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r372-a.json`, row `A3_pathless_rows_count_as_unmapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 17 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_a_library_with_no_tag_category_refuses_through_the_verb`
  - `tests/test_metadata_cli.py::test_a_plan_only_run_leaves_no_record`
  - `tests/test_metadata_cli.py::test_a_second_apply_is_idempotent`
  - `tests/test_metadata_cli.py::test_a_second_apply_writes_nothing_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_apply_is_listed_by_restore_list_as_a_restorable_session`
  - `tests/test_metadata_cli.py::test_an_apply_that_refuses_mid_write_is_abandoned_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_apply_whose_commit_lands_and_then_raises_is_recorded_as_committed`
  - `tests/test_metadata_cli.py::test_apply_writes_my_tags_and_does_not_write_a_content_column`
  - `tests/test_metadata_cli.py::test_the_capture_is_protected_while_the_apply_is_in_flight`
  - `tests/test_metadata_cli.py::test_the_plan_names_existing_rows_and_writes_nothing`
  - `tests/test_paths_resolved.py::test_a_minority_of_unmapped_rows_stays_ok_with_the_counts_visible`
  - `tests/test_paths_resolved.py::test_a_plan_over_a_majority_of_unmapped_rows_fails_with_the_totals_in_the_payload`
  - `tests/test_paths_resolved.py::test_a_row_whose_location_will_not_decode_counts_as_unresolved_not_a_defect`
  - `tests/test_paths_resolved.py::test_doctor_fails_paths_resolved_over_a_majority_off_a_copy`
  - `tests/test_paths_resolved.py::test_doctor_reports_a_minority_as_a_note_and_a_clean_collection_as_ok`
  - ... and 2 more, see the JSON sidecar

Old text:

```
        if outcome.resolution is locations.Resolution.UNMAPPED:
```

New text:

```
        if outcome.path is None:
```

### `r372-a.A4_verb_never_refuses`

mytags_vocals: drop the majority refusal, so the plan reports ok over a majority

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r372-a.json`, row `A4_verb_never_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 2 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_a_plan_over_a_majority_of_unmapped_rows_fails_with_the_totals_in_the_payload`
  - `tests/test_paths_resolved.py::test_an_apply_over_a_majority_refuses_the_same_way_and_writes_nothing`

Old text:

```
        if survey.totals.majority_unmapped:
            empty = _plan_from(cfg, _Survey(survey.totals, ()))
```

New text:

```
        if False:
            empty = _plan_from(cfg, _Survey(survey.totals, ()))
```

### `r372-a.A5_apply_proceeds`

mytags_vocals: refuse the plan alone and let the apply through

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r372-a.json`, row `A5_apply_proceeds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 1 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_an_apply_over_a_majority_refuses_the_same_way_and_writes_nothing`

Old text:

```
        if survey.totals.majority_unmapped:
            empty = _plan_from(cfg, _Survey(survey.totals, ()))
```

New text:

```
        if survey.totals.majority_unmapped and not writing:
            empty = _plan_from(cfg, _Survey(survey.totals, ()))
```

### `r372-a.A6_decode_error_escapes`

_survey: let a location that will not decode raise through the plan and the check

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r372-a.json`, row `A6_decode_error_escapes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 1 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_a_row_whose_location_will_not_decode_counts_as_unresolved_not_a_defect`

Old text:

```
        except locations.LocationDecodeError:
```

New text:

```
        except ZeroDivisionError:
```

### `r372-a.A7_remedy_run_doctor`

majority_unmapped_cause: send the person to doctor, which sends them back

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r372-a.json`, row `A7_remedy_run_doctor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 3 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_a_plan_over_a_majority_of_unmapped_rows_fails_with_the_totals_in_the_payload`
  - `tests/test_paths_resolved.py::test_doctor_fails_paths_resolved_over_a_majority_off_a_copy`
  - `tests/test_paths_resolved.py::test_the_two_synthetic_machines_answer_the_check_opposite_ways`

Old text:

```
        remedy=Remedy.RUN_SETUP,
        steps=(
```

New text:

```
        remedy=Remedy.RUN_DOCTOR,
        steps=(
```

### `r372-a.A8_refused_plan_reports_ok`

_refused_plan: outcome ok beside a cause, the envelope the validator rejects

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r372-a.json`, row `A8_refused_plan_reports_ok`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 2 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_a_plan_over_a_majority_of_unmapped_rows_fails_with_the_totals_in_the_payload`
  - `tests/test_paths_resolved.py::test_an_apply_over_a_majority_refuses_the_same_way_and_writes_nothing`

Old text:

```
        outcome=Outcome.FAILED,
        code=cause.code,
        data=plan,
```

New text:

```
        outcome=Outcome.OK,
        code=cause.code,
        data=plan,
```

### `r381-b.M12_add_legacy_any_name`

add takes the entry under the old fold whatever its display name

- File: `src/cratekit/label/registry.py`
- Source: `r381-b.json`, row `M12_add_legacy_any_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_slug.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 429 against a baseline of 429
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_slug.py::test_a_renamed_entry_under_the_old_fold_is_not_taken_by_its_old_name`

Old text:

```
                if legacy is not None and _name_key(legacy.name) == _name_key(name)
```

New text:

```
                if legacy is not None
```

### `r381.M10_by_id_no_follow`

by_id stops following the renamed map, so a frozen old identifier refuses label-unknown

- File: `src/cratekit/label/registry.py`
- Source: `r381.json`, row `M10_by_id_no_follow`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_slug.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 429 against a baseline of 429
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_slug.py::test_an_identifier_frozen_before_the_move_still_finds_its_label`

Old text:

```
        if found is None and label_id in self.renamed:
```

New text:

```
        if found is None and label_id in ():
```

### `r381.M11_add_ignores_legacy`

add keys on the new slug alone, so a collided label overwrites its neighbour

- File: `src/cratekit/label/registry.py`
- Source: `r381.json`, row `M11_add_ignores_legacy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_slug.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 429 against a baseline of 429
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_slug.py::test_re_adding_a_collided_label_updates_it_and_not_its_neighbour`

Old text:

```
                if legacy is not None and _name_key(legacy.name) == _name_key(name)
```

New text:

```
                if False
```

### `r381.M1_fold_only_slug`

Restore the fold only slug, the brief's named row: slug folds the raw name and transliterates nothing

- File: `src/cratekit/label/registry.py`
- Source: `r381.json`, row `M1_fold_only_slug`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_slug.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 429 against a baseline of 429
- Kills: 13 (killed)
- Killed:
  - `tests/test_label_slug.py::test_a_migrated_label_keeps_its_watermark`
  - `tests/test_label_slug.py::test_a_renamed_entry_under_the_old_fold_is_not_taken_by_its_old_name`
  - `tests/test_label_slug.py::test_a_slug_transliterates_before_it_folds[Caf\xe9 del Mar-cafe-del-mar]`
  - `tests/test_label_slug.py::test_a_slug_transliterates_before_it_folds[Stra\xdfe-strasse]`
  - `tests/test_label_slug.py::test_a_slug_transliterates_before_it_folds[Sue\xf1o-sueno]`
  - `tests/test_label_slug.py::test_a_slug_transliterates_before_it_folds[Suen\u0303o-sueno]`
  - `tests/test_label_slug.py::test_a_slug_transliterates_before_it_folds[Voll Sch\xf6n-voll-schoen]`
  - `tests/test_label_slug.py::test_a_slug_transliterates_before_it_folds[Voll Scho\u0308n-voll-schoen]`
  - `tests/test_label_slug.py::test_a_slug_transliterates_before_it_folds[\xc4\xd6\xdc Records-aeoeue-records]`
  - `tests/test_label_slug.py::test_a_stored_fold_only_identifier_migrates_on_load`
  - `tests/test_label_slug.py::test_an_advance_of_another_label_carries_the_migrated_year_along`
  - `tests/test_label_slug.py::test_an_identifier_frozen_before_the_move_still_finds_its_label`
  - `tests/test_label_slug.py::test_re_adding_a_migrated_label_does_not_file_it_twice`

Old text:

```
    folded = _fold(stripped)
```

New text:

```
    folded = _fold(name)
```

### `r381.M2_no_umlaut_table`

Drop the umlaut and sharp s table, so NFKD alone turns Schön into schon

- File: `src/cratekit/label/registry.py`
- Source: `r381.json`, row `M2_no_umlaut_table`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_slug.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 429 against a baseline of 429
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_slug.py::test_a_slug_transliterates_before_it_folds[Stra\xdfe-strasse]`
  - `tests/test_label_slug.py::test_a_slug_transliterates_before_it_folds[Voll Sch\xf6n-voll-schoen]`
  - `tests/test_label_slug.py::test_a_slug_transliterates_before_it_folds[Voll Scho\u0308n-voll-schoen]`
  - `tests/test_label_slug.py::test_a_slug_transliterates_before_it_folds[\xc4\xd6\xdc Records-aeoeue-records]`
  - `tests/test_label_slug.py::test_a_stored_fold_only_identifier_migrates_on_load`
  - `tests/test_label_slug.py::test_an_advance_of_another_label_carries_the_migrated_year_along`

Old text:

```
    composed = unicodedata.normalize("NFC", name).translate(_TRANSLITERATE)
```

New text:

```
    composed = unicodedata.normalize("NFC", name)
```

### `r381.M3_keep_combining_marks`

Keep the combining marks after NFKD, so they fold to hyphens as before

- File: `src/cratekit/label/registry.py`
- Source: `r381.json`, row `M3_keep_combining_marks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_slug.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 429 against a baseline of 429
- Kills: 10 (killed)
- Killed:
  - `tests/test_label_slug.py::test_a_collision_leaves_the_old_identifier`
  - `tests/test_label_slug.py::test_a_migrated_label_keeps_its_watermark`
  - `tests/test_label_slug.py::test_a_renamed_entry_under_the_old_fold_is_not_taken_by_its_old_name`
  - `tests/test_label_slug.py::test_a_slug_transliterates_before_it_folds[Sue\xf1o-sueno]`
  - `tests/test_label_slug.py::test_a_slug_transliterates_before_it_folds[Suen\u0303o-sueno]`
  - `tests/test_label_slug.py::test_a_stored_fold_only_identifier_migrates_on_load`
  - `tests/test_label_slug.py::test_a_year_already_held_under_the_new_identifier_is_not_overwritten`
  - `tests/test_label_slug.py::test_an_identifier_frozen_before_the_move_still_finds_its_label`
  - `tests/test_label_slug.py::test_re_adding_a_collided_label_updates_it_and_not_its_neighbour`
  - `tests/test_label_slug.py::test_re_adding_a_migrated_label_does_not_file_it_twice`

Old text:

```
        if not unicodedata.combining(char)
```

New text:

```
        if unicodedata.combining(char) or True
```

### `r381.M4_migrate_ignores_taken`

migrate moves an entry onto a slug another entry already holds

- File: `src/cratekit/label/registry.py`
- Source: `r381.json`, row `M4_migrate_ignores_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_slug.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 429 against a baseline of 429
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_slug.py::test_a_collision_leaves_the_old_identifier`
  - `tests/test_label_slug.py::test_re_adding_a_collided_label_updates_it_and_not_its_neighbour`

Old text:

```
        if new is None or new in taken:
```

New text:

```
        if new is None:
```

### `r381.M5_migrate_any_identifier`

migrate moves any entry whose slug differs, not only one the old fold produced

- File: `src/cratekit/label/registry.py`
- Source: `r381.json`, row `M5_migrate_any_identifier`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_slug.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 429 against a baseline of 429
- Kills: 4 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_the_registry_survives_a_label_rename_without_orphaning_its_state`
  - `tests/test_label_slug.py::test_a_renamed_entry_under_the_old_fold_is_not_taken_by_its_old_name`
  - `tests/test_label_slug.py::test_an_identifier_the_old_fold_did_not_produce_is_left_alone[entries0]`
  - `tests/test_label_slug.py::test_an_identifier_the_old_fold_did_not_produce_is_left_alone[entries1]`

Old text:

```
    if new == entry.label_id or entry.label_id != _legacy_slug(entry.name):
```

New text:

```
    if new == entry.label_id:
```

### `r381.M6_update_skips_move_write`

update writes nothing for a move when the mutator opts out, so load never persists a migration

- File: `src/cratekit/label/registry.py`
- Source: `r381.json`, row `M6_update_skips_move_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_slug.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 429 against a baseline of 429
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_slug.py::test_a_stored_fold_only_identifier_migrates_on_load`

Old text:

```
            if changed is not False or moved:
```

New text:

```
            if changed is not False:
```

### `r381.M7_load_never_migrates`

load returns the stored document without planning a move

- File: `src/cratekit/label/registry.py`
- Source: `r381.json`, row `M7_load_never_migrates`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_slug.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 429 against a baseline of 429
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_slug.py::test_a_migrated_label_keeps_its_watermark`
  - `tests/test_label_slug.py::test_a_stored_fold_only_identifier_migrates_on_load`
  - `tests/test_label_slug.py::test_an_advance_of_another_label_carries_the_migrated_year_along`
  - `tests/test_label_slug.py::test_an_identifier_frozen_before_the_move_still_finds_its_label`

Old text:

```
        if not migrate(held)[1]:
            return held
```

New text:

```
        if True:
            return held
```

### `r381.M8_no_renamed_map`

The writer leaves the renamed map out, so no watermark can follow

- File: `src/cratekit/label/registry.py`
- Source: `r381.json`, row `M8_no_renamed_map`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_slug.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 429 against a baseline of 429
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_slug.py::test_a_migrated_label_keeps_its_watermark`
  - `tests/test_label_slug.py::test_a_stored_fold_only_identifier_migrates_on_load`

Old text:

```
        if renamed:
            # Only when something moved
```

New text:

```
        if False:
            # Only when something moved
```

### `r381.M9_live_renames_unfiltered`

live_renames keeps a move whose old identifier a new label holds again

- File: `src/cratekit/label/registry.py`
- Source: `r381.json`, row `M9_live_renames_unfiltered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_slug.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 429 against a baseline of 429
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_slug.py::test_a_stored_move_whose_old_identifier_is_held_is_not_followed`
  - `tests/test_label_slug.py::test_an_old_identifier_reused_by_a_new_label_stops_following`

Old text:

```
        return {old: new for old, new in self.renamed.items() if old not in self.labels}
```

New text:

```
        return dict(self.renamed)
```

### `u107-c.S19_approved_superseded`

approved_cli._queued: count a superseded item as not yet answered

- File: `src/cratekit/label/approved_cli.py`
- Source: `u107-c.json`, row `S19_approved_superseded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_superseded_item_is_not_counted_as_waiting_by_label_approved`

Old text:

```
        elif item.verdict is not review.Verdict.SUPERSEDED:
```

New text:

```
        else:
```

### `r515-operator.S8_short_of_keeps_zero`

Read a saved shortfall block back even when it withheld nothing

- File: `src/cratekit/label/sync_cli.py`
- Source: `r515-operator.json`, row `S8_short_of_keeps_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_saved_shortfall_that_withheld_nothing_reads_back_as_no_shortfall`

Old text:

```
    if any(value is None for value in block.values()) or not block["withheld"]:
```

New text:

```
    if any(value is None for value in block.values()):
```

### `r515-operator.S9_question_no_short`

The label sync question drops the release shortfall

- File: `src/cratekit/label/sync_cli.py`
- Source: `r515-operator.json`, row `S9_question_no_short`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_short_release_is_counted_over_its_rows_and_the_question_says_the_shortfall`

Old text:

```
    if question.provider_withheld:
```

New text:

```
    if False:
```

### `u107-a.S03_marker_moves`

sync_cli.record_answer: keep the asked set as it was, so an answer does not move the marker and the same releases are asked again

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-a.json`, row `S03_marker_moves`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 13 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_label_with_three_new_releases_is_asked_once`
  - `tests/test_label_sync.py::test_a_release_answered_not_now_is_not_filed_by_the_labels_sweep`
  - `tests/test_label_sync.py::test_a_release_the_genre_gate_holds_never_appears_in_a_question`
  - `tests/test_label_sync.py::test_after_any_answer_a_second_run_asks_nothing_about_those_releases[all]`
  - `tests/test_label_sync.py::test_after_any_answer_a_second_run_asks_nothing_about_those_releases[not-now]`
  - `tests/test_label_sync.py::test_after_any_answer_a_second_run_asks_nothing_about_those_releases[pick]`
  - `tests/test_label_sync.py::test_after_any_answer_a_second_run_asks_nothing_about_those_releases[stop]`
  - `tests/test_label_sync.py::test_not_now_moves_the_marker_and_a_release_published_after_is_asked_next_run`
  - `tests/test_label_sync.py::test_nothing_new_after_an_answer_says_the_count_past_the_window`
  - `tests/test_label_sync.py::test_open_review_items_are_offered_once_and_settled_by_the_answer`
  - `tests/test_label_sync.py::test_pick_records_exactly_the_chosen_releases_and_no_others`
  - `tests/test_label_sync.py::test_stopping_after_two_of_five_labels_resumes_at_the_third`
  - `tests/test_label_sync.py::test_the_structured_path_asks_the_same_question_and_takes_the_same_answer`

Old text:

```
        asked = set(asked_releases(document, entry.label_id)) | set(question.identities())
```

New text:

```
        asked = set(asked_releases(document, entry.label_id))
```

### `u107-a.S04_marker_takes_window_place`

sync_cli._question_for: hand the label's source no asked set, so releases already answered are offered again

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-a.json`, row `S04_marker_takes_window_place`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 8 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_release_answered_not_now_is_not_filed_by_the_labels_sweep`
  - `tests/test_label_sync.py::test_after_any_answer_a_second_run_asks_nothing_about_those_releases[not-now]`
  - `tests/test_label_sync.py::test_after_any_answer_a_second_run_asks_nothing_about_those_releases[pick]`
  - `tests/test_label_sync.py::test_not_now_moves_the_marker_and_a_release_published_after_is_asked_next_run`
  - `tests/test_label_sync.py::test_nothing_new_after_an_answer_says_the_count_past_the_window`
  - `tests/test_label_sync.py::test_open_review_items_are_offered_once_and_settled_by_the_answer`
  - `tests/test_label_sync.py::test_stopping_after_two_of_five_labels_resumes_at_the_third`
  - `tests/test_label_sync.py::test_the_structured_path_asks_the_same_question_and_takes_the_same_answer`

Old text:

```
        offered=asked,
```

New text:

```
        offered=None,
```

### `u107-a.S07_gate_before_asking`

sync_cli._question_for: list the label with no genre gate, so a release the gate would hold reaches a question

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-a.json`, row `S07_gate_before_asking`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_release_the_genre_gate_holds_never_appears_in_a_question`

Old text:

```
        gate=genre_gate.SweepGate(
            declared,
            tracks=reader.release_tracks,
            standing=genre_gate.StandingHolds(store),
            asking=tools.asking,
        ),
```

New text:

```
        gate=None,
```

### `u107-a.S08_catch_up_withhold`

sync_cli._question_for: never take back an open item the gate would now hold, so it is offered in the catch up

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-a.json`, row `S08_catch_up_withhold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_walk_whose_gate_took_back_every_open_item_is_not_a_no_op`
  - `tests/test_label_sync.py::test_an_open_item_the_gate_would_now_hold_is_taken_back_before_the_question`

Old text:

```
            elif judged.held:
```

New text:

```
            elif False:
```

### `u107-b.S10_pick_unknown`

sync_cli.record_answer: accept a pick naming a release the question did not offer

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-b.json`, row `S10_pick_unknown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_pick_naming_a_release_the_question_did_not_offer_is_refused`
  - `tests/test_label_sync.py::test_a_pick_outside_the_question_names_next_label_for_its_identifiers`

Old text:

```
            if unknown or not wanted:
```

New text:

```
            if not wanted:
```

### `u107-b.S11_pick_takes_only_chosen`

sync_cli.record_answer: a pick takes every offered release, not only the chosen ones

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-b.json`, row `S11_pick_takes_only_chosen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_pick_of_a_digit_that_is_not_a_number_is_asked_again`
  - `tests/test_label_sync.py::test_a_pick_outside_the_numbers_is_asked_again`
  - `tests/test_label_sync.py::test_a_superseded_item_is_not_counted_as_waiting_by_label_approved`
  - `tests/test_label_sync.py::test_open_review_items_are_offered_once_and_settled_by_the_answer`
  - `tests/test_label_sync.py::test_pick_records_exactly_the_chosen_releases_and_no_others`
  - `tests/test_label_sync.py::test_stopping_after_two_of_five_labels_resumes_at_the_third`
  - `tests/test_label_sync.py::test_the_structured_path_asks_the_same_question_and_takes_the_same_answer`

Old text:

```
            if answer == ALL or (answer == PICK and one.identity in wanted)
```

New text:

```
            if answer in (ALL, PICK)
```

### `u107-b.S12_stop_removes`

sync_cli.record_answer: stop reports the label removed and leaves it in the registry

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-b.json`, row `S12_stop_removes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync.py::test_after_any_answer_a_second_run_asks_nothing_about_those_releases[stop]`
  - `tests/test_label_sync.py::test_stop_following_removes_the_label_and_records_no_download`
  - `tests/test_label_sync.py::test_stopping_after_two_of_five_labels_resumes_at_the_third`

Old text:

```
            removed = labels.RegistryStore().remove(entry.label_id)
```

New text:

```
            removed = True
```

### `u107-b.S13_take_accepts`

sync_cli._take: file a taken release and never record it accepted

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-b.json`, row `S13_take_accepts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 10 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_label_with_three_new_releases_is_asked_once`
  - `tests/test_label_sync.py::test_a_superseded_item_is_not_counted_as_waiting_by_label_approved`
  - `tests/test_label_sync.py::test_after_any_answer_a_second_run_asks_nothing_about_those_releases[all]`
  - `tests/test_label_sync.py::test_after_any_answer_a_second_run_asks_nothing_about_those_releases[pick]`
  - `tests/test_label_sync.py::test_an_item_decided_between_the_question_and_the_answer_is_left_as_decided`
  - `tests/test_label_sync.py::test_next_label_then_answer_then_next_label_says_nothing_new`
  - `tests/test_label_sync.py::test_open_review_items_are_offered_once_and_settled_by_the_answer`
  - `tests/test_label_sync.py::test_pick_records_exactly_the_chosen_releases_and_no_others`
  - `tests/test_label_sync.py::test_stopping_after_two_of_five_labels_resumes_at_the_third`
  - `tests/test_label_sync.py::test_the_structured_path_asks_the_same_question_and_takes_the_same_answer`

Old text:

```
    review.resolve(store, item.item_id, Verdict.ACCEPTED, actor=ACTOR)
```

New text:

```
    pass
```

### `u107-b.S15_no_default_answer`

sync_cli._ask: give the prompt a default of not-now, so an empty line moves the marker

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-b.json`, row `S15_no_default_answer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_an_empty_line_never_moves_a_marker_and_a_prompt_nobody_answers_refuses`

Old text:

```
        answer = prompter.ask(f"Answer ({', '.join(words)})").lower()
```

New text:

```
        answer = prompter.ask(f"Answer ({', '.join(words)})", default=NOT_NOW).lower()
```

### `u107-b.S16_save_before_ask`

sync_cli._walk: ask without saving the question first, so the answer has no question to apply to

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-b.json`, row `S16_save_before_ask`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 9 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_label_whose_catalogue_cannot_be_listed_fails_its_line_and_the_walk_goes_on`
  - `tests/test_label_sync.py::test_a_pick_of_a_digit_that_is_not_a_number_is_asked_again`
  - `tests/test_label_sync.py::test_a_pick_outside_the_numbers_is_asked_again`
  - `tests/test_label_sync.py::test_a_provider_refusal_mid_run_parks_it_with_the_remaining_labels_unasked`
  - `tests/test_label_sync.py::test_a_walk_left_unanswered_after_its_question_was_saved_is_not_a_no_op`
  - `tests/test_label_sync.py::test_a_word_outside_the_set_is_asked_again_and_the_answers_before_it_are_saved`
  - `tests/test_label_sync.py::test_an_empty_line_never_moves_a_marker_and_a_prompt_nobody_answers_refuses`
  - `tests/test_label_sync.py::test_stopping_after_two_of_five_labels_resumes_at_the_third`
  - `tests/test_label_sync.py::test_the_structured_path_asks_the_same_question_and_takes_the_same_answer`

Old text:

```
            _save_pending(cfg, listed.question)
```

New text:

```
            pass
```

### `u107-b.S17_dead_verifier_skip`

sync_cli._question_for: read a catalogue that confirmed nothing as a label with nothing new

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-b.json`, row `S17_dead_verifier_skip`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_catalogue_that_confirms_nothing_is_not_a_label_with_nothing_new`

Old text:

```
    if not candidates and source.dropped and unconfirmed == source.read:
```

New text:

```
    if False:
```

### `u107-c.S20_pick_isdecimal`

sync_cli._pick: decide a release number with isdigit again, so a superscript digit crashes the walk (fix round guard)

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-c.json`, row `S20_pick_isdecimal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_pick_of_a_digit_that_is_not_a_number_is_asked_again`

Old text:

```
            if word.isdecimal() and 1 <= int(word) <= count:
```

New text:

```
            if word.isdigit() and 1 <= int(word) <= count:
```

### `u107-c.S21_filing_run`

sync_cli.record_answer: file taken releases under the answering run, not the run that asked (fix round guard)

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-c.json`, row `S21_filing_run`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_later_answer_files_its_releases_under_the_run_that_asked`

Old text:

```
        filing_run = question.run or run_id
```

New text:

```
        filing_run = run_id
```

### `u107-c.S23_stop_remedy`

sync_cli.record_answer: stop with nothing waiting sends a person to --next, which asks nothing (fix round guard)

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-c.json`, row `S23_stop_remedy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_stop_with_no_question_waiting_names_the_registry_remove`

Old text:

```
                    if answer == STOP
```

New text:

```
                    if False
```

### `u107-c.S24_size_coefficient`

sync_cli: halve the bytes per second the size estimate uses

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-c.json`, row `S24_size_coefficient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync.py::test_the_default_human_output_names_the_question_and_each_release`
  - `tests/test_label_sync.py::test_the_structured_path_asks_the_same_question_and_takes_the_same_answer`

Old text:

```
BYTES_PER_SECOND = 110_000
```

New text:

```
BYTES_PER_SECOND = 55_000
```

### `u107-d.S02_record_version_again`

sync_cli.load_record: accept a record of any version as this build's

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-d.json`, row `S02_record_version_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_record_of_another_version_refuses_rather_than_being_read_as_this_builds`

Old text:

```
    if version != RECORD_VERSION:
```

New text:

```
    if False:
```

### `u107-d.S14_take_respects_decided_again`

sync_cli._take: overwrite an item a person decided between the question and the answer

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-d.json`, row `S14_take_respects_decided_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_an_item_decided_between_the_question_and_the_answer_is_left_as_decided`

Old text:

```
    if item.stored_verdict is not None:
        return False
```

New text:

```
    if False:
        return False
```

### `u107-d.S25_measured_passes_refusal_again`

sync_cli._measured: count a provider refusal while reading a release's tracks as tracks unread, so the walk goes on instead of parking

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-d.json`, row `S25_measured_passes_refusal_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_provider_refusal_while_counting_a_catch_up_release_parks_the_run`

Old text:

```
    except CratekitError:
        raise
    except Exception:  # noqa: BLE001 - counted as unread, never guessed at
```

New text:

```
    except Exception:  # noqa: BLE001 - counted as unread, never guessed at
```

### `r515-operator.S6_cache_drops_short`

The caching release reader stores the rows and year but drops the shortfall

- File: `src/cratekit/label/catalogue.py`
- Source: `r515-operator.json`, row `S6_cache_drops_short`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_short_release_is_counted_over_its_rows_and_the_question_says_the_shortfall`

Old text:

```
        answer = (tuple(rows), year, short)
```

New text:

```
        answer = (tuple(rows), year, None)
```

### `r1499.L01_go_arrival_after_tail`

label sync: no check after the go's name apply, so an arrival is planned into the go's landing

- File: `src/cratekit/cli/label_sync.py`
- Source: `r1499.json`, row `L01_go_arrival_after_tail`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_download_finished_while_a_gos_tail_runs_refuses_its_landing`

Old text:

```
        if changed is not None:
            raise tail.Stop(tail.LAND, changed, continues=False)
```

New text:

```
        if False:
            raise tail.Stop(tail.LAND, changed, continues=False)
```

### `r1499.S01_download_reading`

sync land: the reading before the download never refuses, so a pass downloads beside a go's download at its gate

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S01_download_reading`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 12 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_file_put_there_since_the_tail_stopped_is_not_the_passes_own`
  - `tests/test_sync_land_beside.py::test_a_file_the_passes_tail_left_and_then_changed_is_not_its_own`
  - `tests/test_sync_land_beside.py::test_a_label_gos_download_at_its_landings_gate_renamed_refuses_the_pass_before_it_downloads`
  - `tests/test_sync_land_beside.py::test_a_pass_whose_landing_is_proven_is_not_named`
  - `tests/test_sync_land_beside.py::test_a_plain_download_beside_the_pass_refuses_naming_it`
  - `tests/test_sync_land_beside.py::test_a_record_that_cannot_be_kept_is_a_warning_and_the_next_run_refuses`
  - `tests/test_sync_land_beside.py::test_an_earlier_pass_renamed_at_its_gate_is_named_by_its_pass`
  - `tests/test_sync_land_beside.py::test_an_earlier_passes_unlanded_download_refuses_a_new_pass_naming_how_it_lands`
  - `tests/test_sync_land_beside.py::test_once_the_passes_landing_is_proven_its_record_reads_nothing_as_its_own`
  - `tests/test_sync_land_staged.py::test_a_pass_whose_every_missing_track_is_staged_downloads_nothing_and_refuses`
  - `tests/test_sync_land_staged.py::test_a_second_pass_beside_an_unlanded_first_refuses_before_any_download_is_refused`
  - `tests/test_sync_land_staged.py::test_a_second_pass_beside_the_unlanded_first_lists_only_what_it_did_not_stage_and_refuses`

Old text:

```
    if not found:
        return settled

```

New text:

```
    if not found or step == DOWNLOAD:
        return settled

```

### `r1499.S02_tail_reading`

sync land: the reading before the tail never refuses, so a download finished during the pass's download is tailed and landed with it

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S02_tail_reading`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_gos_download_arriving_while_the_pass_downloads_refuses_its_tail`

Old text:

```
    if not found:
        return settled

```

New text:

```
    if not found or step == TAG:
        return settled

```

### `r1499.S03_arrival_after_tail`

sync land: no check after name apply, so a download finished during the tail is renamed and planned into the landing

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S03_arrival_after_tail`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_download_finished_while_the_passes_tail_runs_refuses_its_landing`
  - `tests/test_sync_land_beside.py::test_a_file_a_person_put_there_while_the_tail_ran_refuses_its_landing`

Old text:

```
            if changed is not None:
                # NOT CONTINUED
```

New text:

```
            if False:
                # NOT CONTINUED
```

### `r1499.S04_arrival_after_plan`

sync land: a landing planned over an arrival is handed on at its gate

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S04_arrival_after_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_download_finished_as_the_landing_is_planned_refuses_the_planned_landing`

Old text:

```
                changed = _arrived(cfg, staging, name, before)
                if changed is None:
                    raise

```

New text:

```
                changed = None
                if changed is None:
                    raise

```

### `r1499.S05_keep_after_arrival`

_keep: keep the record although something arrived, so the arrival reads as the pass's own on its next run

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S05_keep_after_arrival`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_download_finished_as_the_landing_is_planned_refuses_the_planned_landing`
  - `tests/test_sync_land_beside.py::test_a_download_finished_while_the_passes_tail_runs_refuses_its_landing`

Old text:

```
    if why is not None:
        report.warnings.append(
```

New text:

```
    if False:
        report.warnings.append(
```

### `r1499.S06_keep_called`

sync land: keep no record at the tail's stop, so the pass continued refuses beside its own renamed tracks

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S06_keep_called`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_download_finished_while_the_passes_tail_runs_refuses_its_landing`
  - `tests/test_sync_land_beside.py::test_a_file_put_there_since_the_tail_stopped_is_not_the_passes_own`
  - `tests/test_sync_land_beside.py::test_a_record_that_cannot_be_kept_is_a_warning_and_the_next_run_refuses`
  - `tests/test_sync_land_beside.py::test_an_unreadable_library_root_refuses_over_the_passes_renamed_tracks`
  - `tests/test_sync_land_beside.py::test_the_passes_own_renamed_tracks_after_its_tail_stopped_run_on[failed]`
  - `tests/test_sync_land_beside.py::test_the_passes_own_renamed_tracks_after_its_tail_stopped_run_on[gate]`
  - `tests/test_sync_land_beside.py::test_the_record_is_kept_under_the_pass_at_each_tail_stop`

Old text:

```
            _keep(report, cfg, staging, name, before)
```

New text:

```
            pass
```

### `r1499.S07_kept_read`

_alone: read no kept record, so the pass's own renamed tracks are beside it

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S07_kept_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_file_put_there_since_the_tail_stopped_is_not_the_passes_own`
  - `tests/test_sync_land_beside.py::test_an_unreadable_library_root_refuses_over_the_passes_renamed_tracks`
  - `tests/test_sync_land_beside.py::test_the_passes_own_renamed_tracks_after_its_tail_stopped_run_on[failed]`
  - `tests/test_sync_land_beside.py::test_the_passes_own_renamed_tracks_after_its_tail_stopped_run_on[gate]`

Old text:

```
                kept=staged.kept(staged.pass_record(cfg, name)),
```

New text:

```
                kept=frozenset(),
```

### `r1499.S08_own_pass_proof`

_alone: never read the pass's landing proof, so a landed pass's record still reads files as its own

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S08_own_pass_proof`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_an_unreadable_library_root_refuses_over_the_passes_renamed_tracks`
  - `tests/test_sync_land_beside.py::test_once_the_passes_landing_is_proven_its_record_reads_nothing_as_its_own`

Old text:

```
                own_pass=name,
                origin=_ORIGIN,
```

New text:

```
                own_pass=None,
                origin=_ORIGIN,
```

### `r1499.S09_own_library`

_own_downloads: a download of another library over the pass's list is its own

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S09_own_library`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_passes_own_downloads_are_this_librarys_over_its_own_list_by_name`

Old text:

```
        if staged.pass_of(job) == name and job.library_id == cfg.library.volume_id
```

New text:

```
        if staged.pass_of(job) == name
```

### `r1499.S10_own_by_list`

_own_downloads: no download is the pass's own, so its own fresh tracks refuse it

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S10_own_by_list`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 66 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_cancelled_download_over_the_same_list_is_not_reused`
  - `tests/test_sync_land.py::test_a_continued_pass_drives_the_download_it_queued_and_queues_no_second`
  - `tests/test_sync_land.py::test_a_continued_pass_never_drives_a_cancelled_job_and_lists_the_rest`
  - `tests/test_sync_land.py::test_a_continued_pass_over_an_open_intake_job_drives_it_first`
  - `tests/test_sync_land.py::test_a_continued_pass_refused_while_rekordbox_runs_names_the_way_back`
  - `tests/test_sync_land.py::test_a_continued_pass_retries_a_download_that_failed_transiently`
  - `tests/test_sync_land.py::test_a_failed_tail_step_plans_no_landing_and_names_the_continuation`
  - `tests/test_sync_land.py::test_a_fresh_pass_never_reuses_another_lists_download_job`
  - `tests/test_sync_land.py::test_a_gate_any_earlier_step_stops_at_is_the_steps_own_not_the_passes`
  - `tests/test_sync_land.py::test_a_job_command_that_stops_at_a_gate_is_that_commands_gate`
  - `tests/test_sync_land.py::test_a_landing_that_needs_the_backup_acknowledgment_stops_without_minting_one`
  - `tests/test_sync_land.py::test_a_name_apply_refusal_ends_the_pass_before_the_landing`
  - `tests/test_sync_land.py::test_a_pass_continued_by_its_land_run_id_reaches_the_same_jobs_as_by_its_pass_id`
  - `tests/test_sync_land.py::test_a_pass_queued_by_hand_and_never_driven_is_the_one_this_verb_takes`
  - `tests/test_sync_land.py::test_a_pass_whose_vocal_model_can_score_says_so_and_asks_nothing`
  - ... and 51 more, see the JSON sidecar

Old text:

```
        if staged.pass_of(job) == name and job.library_id == cfg.library.volume_id
```

New text:

```
        if staged.pass_of(job) == name + '-' and job.library_id == cfg.library.volume_id
```

### `r1499.S11_unreadable_refuses`

_alone: a refusal of the reading (an unlistable folder, an unreadable root) reads as nothing beside

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S11_unreadable_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_an_unreadable_library_root_refuses_over_the_passes_renamed_tracks`

Old text:

```
    except CratekitError as exc:
        raise _Stop(step, exc) from None
    except OSError
```

New text:

```
    except CratekitError:
        return staged.Settled(frozenset(), 0)
    except OSError
```

### `r1499.S12_warnings_in_refusal`

_with_warnings: a refusal drops the pass's warnings

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S12_warnings_in_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_download_finished_while_the_passes_tail_runs_refuses_its_landing`

Old text:

```
    if report.warnings:
        data["warnings"]
```

New text:

```
    if False:
        data["warnings"]
```

### `r1499.S13_own_unnamed_step`

_own_unnamed: never name the landing under the pass for files no download names

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S13_own_unnamed_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_record_that_cannot_be_kept_is_a_warning_and_the_next_run_refuses`

Old text:

```
    if not (found.unnamed and own):
        return ()
```

New text:

```
    if True:
        return ()
```

### `r301.B1_shipped_month_unbounded`

The shipped budget carries no monthly bound, which is the tree before this unit

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r301.json`, row `B1_shipped_month_unbounded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 5 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_the_shipped_budget_bounds_the_month_the_section_names`
  - `tests/intake/test_workers.py::test_an_unconfigured_machine_meets_a_monthly_bound_before_the_first_call[identify]`
  - `tests/intake/test_workers.py::test_an_unconfigured_machine_meets_a_monthly_bound_before_the_first_call[set]`
  - `tests/intake/test_workers.py::test_the_configured_monthly_bound_is_the_one_the_verb_meets[identify]`
  - `tests/intake/test_workers.py::test_the_configured_monthly_bound_is_the_one_the_verb_meets[set]`

Old text:

```
        return cls(per_run=MAX_CALLS_PER_RUN, monthly=recognition.monthly_calls)
```

New text:

```
        return cls(per_run=MAX_CALLS_PER_RUN, monthly=None)
```

### `r301.B2_bound_host_ignored`

The bound identifier asks the default region whatever the section names

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r301.json`, row `B2_bound_host_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_the_seam_binds_this_identifier_when_none_is_injected`
  - `tests/intake/test_workers.py::test_the_configured_host_is_the_one_every_paid_call_is_sent_to[identify]`
  - `tests/intake/test_workers.py::test_the_configured_host_is_the_one_every_paid_call_is_sent_to[set]`

Old text:

```
            host=recognition.host,
```

New text:

```
            host=config.DEFAULT_RECOGNITION_HOST,
```

### `r301.B3_refusal_detail_no_key`

The monthly refusal's detail no longer names the key that raises the bound

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r301.json`, row `B3_refusal_detail_no_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 5 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_the_monthly_bound_counts_what_the_ledger_already_holds`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_reads_what_is_owed_and_the_parts_ceiling_reads_the_grid`
  - `tests/intake/test_recognition.py::test_the_monthly_refusal_names_the_key_that_raises_the_bound`
  - `tests/intake/test_workers.py::test_an_unconfigured_machine_meets_a_monthly_bound_before_the_first_call[identify]`
  - `tests/intake/test_workers.py::test_an_unconfigured_machine_meets_a_monthly_bound_before_the_first_call[set]`

Old text:

```
                "key": MONTHLY_KEY,

```

New text:

```
(empty)
```

### `r301.B4_refusal_message_no_key`

The monthly refusal's message is reworded so it no longer names the key

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r301.json`, row `B4_refusal_message_no_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_the_monthly_refusal_names_the_key_that_raises_the_bound`
  - `tests/intake/test_workers.py::test_an_unconfigured_machine_meets_a_monthly_bound_before_the_first_call[identify]`
  - `tests/intake/test_workers.py::test_an_unconfigured_machine_meets_a_monthly_bound_before_the_first_call[set]`

Old text:

```
            f"or raise {MONTHLY_KEY} in the configuration if the plan allows more",
```

New text:

```
            f"or adjust the configured bound if the plan allows more",
```

### `r301.S1_month_ignores_ledger`

Sample of an existing guard: the monthly check ignores what the month already spent

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r301.json`, row `S1_month_ignores_ledger`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 6 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_the_month_is_asked_once_over_the_whole_set_before_the_first_part`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_counts_what_the_ledger_already_holds`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_reads_what_is_owed_and_the_parts_ceiling_reads_the_grid`
  - `tests/intake/test_recognition.py::test_the_monthly_refusal_names_the_key_that_raises_the_bound`
  - `tests/intake/test_workers.py::test_an_unconfigured_machine_meets_a_monthly_bound_before_the_first_call[identify]`
  - `tests/intake/test_workers.py::test_an_unconfigured_machine_meets_a_monthly_bound_before_the_first_call[set]`

Old text:

```
    if budget.monthly is not None and used_this_month + planned > budget.monthly:
```

New text:

```
    if budget.monthly is not None and planned > budget.monthly:
```

### `u57-recognition-and-items.M11_unreached_stop_tenfold`

Fifty unanswered calls in a row before the run stops, not five

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M11_unreached_stop_tenfold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
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

### `u57-recognition-and-items.M12_quota_reads_as_failure`

The provider's quota answer is raised under the failure slug, not the spend slug

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M12_quota_reads_as_failure`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_cache_that_cannot_be_written_does_not_replace_the_refusal_on_its_way_out`
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

### `u57-recognition-and-items.M16_grid_off_by_one`

The planned count loses its last chunk

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M16_grid_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 69 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_changed_chunk_plan_misses_the_cache`
  - `tests/intake/test_recognition.py::test_a_changed_file_misses_the_cache`
  - `tests/intake/test_recognition.py::test_a_chunk_that_got_no_answer_is_never_kept_so_only_the_gap_is_paid_again`
  - `tests/intake/test_recognition.py::test_a_document_that_cannot_be_trusted_is_a_miss_and_never_a_tracklist[another-plan]`
  - `tests/intake/test_recognition.py::test_a_document_that_cannot_be_trusted_is_a_miss_and_never_a_tracklist[corrupt]`
  - `tests/intake/test_recognition.py::test_a_document_that_cannot_be_trusted_is_a_miss_and_never_a_tracklist[not-an-object]`
  - `tests/intake/test_recognition.py::test_a_five_hour_mix_is_identified_in_two_even_parts_as_one_set`
  - `tests/intake/test_recognition.py::test_a_ledger_that_cannot_record_stops_the_run_before_the_call`
  - `tests/intake/test_recognition.py::test_a_partition_that_hands_back_an_oversize_part_is_refused_before_any_call[oversize-second-part]`
  - `tests/intake/test_recognition.py::test_a_pass_that_raised_keeps_what_it_had_already_paid_for`
  - `tests/intake/test_recognition.py::test_a_provider_quota_answer_is_a_spend_refusal_and_never_a_miss`
  - `tests/intake/test_recognition.py::test_a_recording_that_cannot_be_digested_is_identified_without_the_cache_and_says_so`
  - `tests/intake/test_recognition.py::test_a_recording_that_cannot_be_measured_or_carved_fails_without_a_call`
  - `tests/intake/test_recognition.py::test_a_run_where_no_call_got_an_answer_is_a_failure_and_not_an_empty_set`
  - `tests/intake/test_recognition.py::test_a_second_pass_over_an_unchanged_recording_spends_nothing`
  - ... and 54 more, see the JSON sidecar

Old text:

```
    return (whole - chunk_s) // interval_s + 1
```

New text:

```
    return (whole - chunk_s) // interval_s
```

### `u57-recognition-and-items.M18_missing_credential_is_unready`

A credential missing after the gate is reported as the gate class, not as credential-missing

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M18_missing_credential_is_unready`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
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

### `u57-recognition-and-items.M1_miss_family_loses_1001`

1001, the service's own no result code, falls out of the miss family

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M1_miss_family_loses_1001`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 48 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_changed_chunk_plan_misses_the_cache`
  - `tests/intake/test_recognition.py::test_a_changed_file_misses_the_cache`
  - `tests/intake/test_recognition.py::test_a_chunk_that_got_no_answer_is_never_kept_so_only_the_gap_is_paid_again`
  - `tests/intake/test_recognition.py::test_a_document_from_another_cache_version_is_a_miss`
  - `tests/intake/test_recognition.py::test_a_document_that_cannot_be_trusted_is_a_miss_and_never_a_tracklist[another-plan]`
  - `tests/intake/test_recognition.py::test_a_document_that_cannot_be_trusted_is_a_miss_and_never_a_tracklist[corrupt]`
  - `tests/intake/test_recognition.py::test_a_document_that_cannot_be_trusted_is_a_miss_and_never_a_tracklist[not-an-object]`
  - `tests/intake/test_recognition.py::test_a_five_hour_mix_is_identified_in_two_even_parts_as_one_set`
  - `tests/intake/test_recognition.py::test_a_pass_that_paid_for_nothing_writes_nothing_and_reports_nothing_unwritten`
  - `tests/intake/test_recognition.py::test_a_pass_that_raised_keeps_what_it_had_already_paid_for`
  - `tests/intake/test_recognition.py::test_a_recording_that_cannot_be_digested_is_identified_without_the_cache_and_says_so`
  - `tests/intake/test_recognition.py::test_a_recording_that_cannot_be_measured_or_carved_fails_without_a_call`
  - `tests/intake/test_recognition.py::test_a_second_pass_over_an_unchanged_recording_spends_nothing`
  - `tests/intake/test_recognition.py::test_a_set_nobody_recognised_is_zero_rows_with_the_misses_counted_not_a_refusal`
  - `tests/intake/test_recognition.py::test_a_set_that_fits_one_run_is_one_part`
  - ... and 33 more, see the JSON sidecar

Old text:

```
_MISS_CODES = frozenset({1001, 2004, 3015})
```

New text:

```
_MISS_CODES = frozenset({2004, 3015})
```

### `u57-recognition-and-items.M2_quota_family_empty`

3003 stops being a quota answer, so a spent account reads as unclassified

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M2_quota_family_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 6 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_cache_that_cannot_be_written_does_not_replace_the_refusal_on_its_way_out`
  - `tests/intake/test_recognition.py::test_a_pass_that_raised_keeps_what_it_had_already_paid_for`
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

### `u57-recognition-and-items.M3_auth_family_loses_3001`

3001, a missing or invalid access key, stops being a credential answer

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M3_auth_family_loses_3001`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
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

### `u57-recognition-and-items.M4_transient_range_dropped`

The 2000s stop being transient, so a recording error ends the run as unclassified

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M4_transient_range_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
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

### `u57-recognition-and-items.M5_empty_music_not_none`

A match answer carrying no music entry is indexed rather than read as none

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M5_empty_music_not_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
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

### `u57-recognition-and-items.M6_score_constant`

Every hit scores zero, so the fold can never prefer a better answer

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M6_score_constant`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
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

### `u57-recognition-and-items.M7_fold_never_takes_best_score`

Adjacent answers fold to the first, whatever the later one scored

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M7_fold_never_takes_best_score`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
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

### `u69-b.M10_out_not_a_folder`

Drop the refusal of an --out that exists and is not a folder

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69-b.json`, row `M10_out_not_a_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_file_where_the_folder_should_be_is_refused`

Old text:

```
    if out.exists() and not out.is_dir():
```

New text:

```
    if False:
```

### `u69-b.M12_unlisted_status`

Report unlisted missing tracks as a note instead of a failing check

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69-b.json`, row `M12_unlisted_status`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_missing_row_from_no_provider_is_reported_unlisted_as_a_failing_check`

Old text:

```
"fail" if unlisted else "ok",
```

New text:

```
"info" if unlisted else "ok",
```

### `u69-b.M16_next_command`

Drop the literal next command from the written check a person reads

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69-b.json`, row `M16_next_command`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
written to {written.list_path}; next: {command}"
```

New text:

```
written to {written.list_path}"
```

### `u69-b.M17_lists_folder`

Write into download staging itself rather than its lists folder

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69-b.json`, row `M17_lists_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 8 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_different_list_already_at_the_path_is_refused_and_left_alone`
  - `tests/test_intake_missing.py::test_a_mixed_job_writes_only_the_missing_rows`
  - `tests/test_intake_missing.py::test_a_run_list_is_one_file_a_second_listing_reproduces`
  - `tests/test_intake_missing.py::test_an_earlier_file_that_is_not_a_list_gives_no_reason_rather_than_a_wrong_one`
  - `tests/test_intake_missing.py::test_missing_tracks_none_of_which_can_be_listed_write_the_unlisted_list_not_a_no_op`
  - `tests/test_intake_missing.py::test_the_default_human_output_names_the_list_and_the_next_command`
  - `tests/test_intake_missing.py::test_the_default_human_output_names_the_list_the_download_and_the_landing`
  - `tests/test_intake_missing.py::test_two_playlists_sharing_a_track_list_it_once_with_both_provenances`

Old text:

```
out = intake_cli._load().paths.download_staging / LISTS_DIR
```

New text:

```
out = intake_cli._load().paths.download_staging
```

### `u69-b.M18_inner_cause`

Drop the failed job's own cause from the refusal

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69-b.json`, row `M18_inner_cause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_failed_job_is_refused_carrying_its_own_cause`

Old text:

```
            inner=job.cause,
```

New text:

```
            inner=None,
```

### `u69-b.M19_resume_step`

Drop the resume command from an open job's refusal

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69-b.json`, row `M19_resume_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_an_open_job_is_refused_and_nothing_is_written`

Old text:

```
            f"finish it with: crate {argv}" if job.is_open() else
```

New text:

```
            "finish it first" if job.is_open() else
```

### `u69.M1_handler_key`

Drop the refusal of a job queued under another verb's handler key

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69.json`, row `M1_handler_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_job_of_another_verb_is_refused`

Old text:

```
    if job.handler_key not in intake_cli.INTAKE_KEYS:
```

New text:

```
    if False:
```

### `u69.M2_succeeded_only`

Drop the refusal of a job that is not succeeded (open, failed, cancelled)

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69.json`, row `M2_succeeded_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_failed_job_is_refused_carrying_its_own_cause`
  - `tests/test_intake_missing.py::test_an_open_job_is_refused_and_nothing_is_written`

Old text:

```
    if job.state is not jobs.JobState.SUCCEEDED:
```

New text:

```
    if False:
```

### `u69.M4_report_coverage`

Drop the refusal when the reports do not cover the items one for one

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69.json`, row `M4_report_coverage`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_report_for_the_wrong_item_refuses_even_when_the_count_matches`
  - `tests/test_intake_missing.py::test_fewer_readable_reports_than_items_refuses_rather_than_listing_a_subset`

Old text:

```
    if sorted(reported) != sorted(wanted):
```

New text:

```
    if False:
```

### `u69.M5_by_count`

Compare reports to items by count instead of by identifier

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69.json`, row `M5_by_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_report_for_the_wrong_item_refuses_even_when_the_count_matches`

Old text:

```
    if sorted(reported) != sorted(wanted):
```

New text:

```
    if len(reported) != len(wanted):
```

