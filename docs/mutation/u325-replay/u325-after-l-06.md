# Mutation table: u325-after-l-06

Measured by `scripts/mutate.py` on 2026-11-22 23:23 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 116.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:21 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 5, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r667.G12_same_recording_no_credit` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 729 | 1 | killed |
| `r667.G13_isrc_not_consulted` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 729 | 16 | killed |
| `r667.G15_isrc_hit_skips_key` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 729 | 3 | killed |
| `r667.G16_isrc_reason_is_exact` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 729 | 11 | killed |
| `r667.G17_reader_drops_isrc` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 729 | 17 | killed |
| `r667.G3_members_not_split` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 729 | 6 | killed |
| `r667.G4_members_not_folded` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 729 | 5 | killed |
| `r667.G5_empty_isrc_asks` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 729 | 1 | killed |
| `r667.G8_no_credited_rule` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 729 | 6 | killed |
| `r312.W2_worker_writes_nothing` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 8 | killed |
| `r312.W3_success_exit_silent` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 5 | killed |
| `r312.W4_failure_exit_silent` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 2 | killed |
| `r312.W5_cause_steps_replaced` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `r312.W7b_pre_drive_refusal_extended` | `src/cratekit/write/routing_cli.py` | maintainer | 2 file(s) | 244 | 1 | killed |
| `r312.W8_list_not_by_job` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 2 | killed |
| `r318-b.C7_trees_not_deduplicated` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `r318-b.N1_no_native_key_dropped` | `src/cratekit/write/routing_cli.py` | maintainer | 2 file(s) | 244 | 1 | killed |
| `r318-b.W2_cap_halved` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `r318.C1_skipped_files_always_empty` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 4 | killed |
| `r318.C2_tombstones_not_consulted` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `r318.C3_ambiguous_ids_dropped` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `r318.C4_withdrawn_ids_dropped` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `r318.C5_withdrawn_single_id_dropped` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `r318.C6_trees_emptied` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 2 | killed |
| `r318.C8_path_reduced_to_name` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `r318.C9_warnings_not_emitted` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 4 | killed |
| `r318.W1_cap_not_applied` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `r318.W3_count_is_named_not_whole` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `r318.W4_reasons_unsorted` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `r318.W5_next_act_dropped` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `u132.W6_resort_note` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `u155.W3_gate_column` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 3 | killed |
| `u155.W4_gate_count` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 3 | killed |
| `u155.W5_owed_once` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `u155.W6_inbox_item_genre` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `u155.W7_export_item_genre` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `r187-a.C1_blank_not_key` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 2 | killed |
| `r187-a.C2_uncapped` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `r187-a.C3_mutex` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 2 | killed |
| `r187-a.C4_key_beside_name` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `r187-a.C5_empty_name_scans` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `r187-a.C6_no_cache_path` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 3 | killed |
| `u43-author-light.A1_first_track_wins` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 4 | killed |
| `u43-author-light.A3_containment_not_checked` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 2 | killed |
| `u43-author-light.A4_empty_anchor_defaults` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 2 | killed |
| `u43-author-light.C1_no_lower_bound` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 4 | killed |
| `u43-author-light.C2_bound_off_by_one` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 2 | killed |
| `u43-author-light.P1_anchor_absent_from_digest` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 2 | killed |
| `u43-author-light.P3_pool_leads_the_items` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u43-author-light.P4_no_positions_at_all` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 4 | killed |
| `u43-author-light.P5_role_ignored` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 2 | killed |
| `u43-author-light.P7_vox_threshold_ignored` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u43-author-round-2.A2_no_resolved_second_pass` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u43-author-round-2.H2_empty_is_a_no_op` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u43-author-round-2.H3_missing_root_not_refused` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u43-author-round-2.P2_items_absent_from_digest` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u43-author-round-2.P6_count_ignored` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u43-author-round-2.V1_pool_total_is_the_union` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u43-author-round-2.V3_root_check_reports_instead_of_refusing` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u98-a.K1_key_off_wheel` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 7 | killed |
| `u98-a.T1_tempo_nonfinite` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 2 | killed |
| `u98-a.T2_tempo_zero` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u98-a.U1_empty_label` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u98-a.U2_key_missing` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 2 | killed |
| `u98-a.U3_reported_owned` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 5 | killed |
| `u98-a.U4_tempo_dropped` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 3 | killed |
| `u98-a.X1_mutex` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 3 | killed |
| `u98-b.E1_existing_containment` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 2 | killed |
| `u98-b.H1_held_not_excluded` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u98-b.H2_held_not_reported` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u98-b.H3_held_fuzzy` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u98-b.S1_supplied_beside_path` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 3 | killed |
| `u98-b.S2_tempo_half` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u240.M11_needle_is_the_name` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 334 | 2 | killed |
| `u240.M12_raw_line_matched` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 334 | 2 | killed |
| `u240.M13_two_way_match` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 334 | 7 | killed |
| `u240.M14_widest_any` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 334 | 1 | killed |
| `u240.M15_no_widest_rule` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 334 | 1 | killed |
| `u240.M16_genres_joined_by_name` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 334 | 1 | killed |
| `u240.M17_worker_hands_no_seam` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 334 | 8 | killed |
| `u240.M18_way_inverted` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 334 | 3 | killed |
| `u240.M19_one_name_ambiguous` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 334 | 2 | killed |
| `u240.M20_warning_dropped` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 334 | 1 | killed |
| `u240.M21_failed_sweep_unreported` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 334 | 3 | killed |
| `u240.M22_failed_items_left_out` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 334 | 3 | killed |
| `u240.M23_cap_lowered` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 334 | 1 | killed |
| `u240.M1_two_names_take_the_first` | `src/cratekit/tagging/tag.py` | user | 5 file(s) | 334 | 4 | killed |
| `u240.M2_no_genre_label_named` | `src/cratekit/tagging/tag.py` | user | 5 file(s) | 334 | 4 | killed |
| `u240.M3_tag_no_longer_outranks_the_line` | `src/cratekit/tagging/tag.py` | user | 5 file(s) | 334 | 17 | killed |
| `u240.M4_folder_label_no_longer_outranks_the_line` | `src/cratekit/tagging/tag.py` | user | 5 file(s) | 334 | 9 | killed |
| `u240.M5_wrong_field_read` | `src/cratekit/tagging/tag.py` | user | 5 file(s) | 334 | 11 | killed |
| `u240.M6_named_by_lost` | `src/cratekit/tagging/tag.py` | user | 5 file(s) | 334 | 5 | killed |
| `u240.M7_line_labels_dropped_from_result` | `src/cratekit/tagging/tag.py` | user | 5 file(s) | 334 | 3 | killed |
| `u240.M8_failed_files_line_dropped` | `src/cratekit/tagging/tag.py` | user | 5 file(s) | 334 | 1 | killed |
| `u240.M9_park_flattened` | `src/cratekit/tagging/tag.py` | user | 5 file(s) | 334 | 1 | killed |
| `u93-recursive-analysis.D21_restamp_flag` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 206 | 11 | killed |
| `u93-recursive-analysis.D22_restamp_resume_warning` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 206 | 2 | killed |
| `u93-recursive-analysis.D24_restamp_join` | `src/cratekit/analysis/cli.py` | maintainer | 2 file(s) | 206 | 1 | killed |
| `u94-a.S1_floor_dropped` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 206 | 3 | killed |
| `u94-a.S2_floor_off_by_one` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 206 | 2 | killed |
| `u94-a.S3_partial_refusal_dropped` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 206 | 6 | killed |
| `u94-a.S4_accept_flag_dead` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 206 | 11 | killed |
| `u94-a.S5_recursive_not_required` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 206 | 2 | killed |
| `u94-a.S6_music_folder_not_wide` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 206 | 1 | killed |
| `u94-a.S7_samefile_to_spelling` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 206 | 1 | killed |
| `u94-a.S8_after_walk_never_asked` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 206 | 1 | killed |
| `u94-b.W1_after_walk_refusal_dropped` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 206 | 1 | killed |
| `u94-b.W3_accepted_reads_ok` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 206 | 2 | killed |
| `u94-b.W4_partial_warning_dropped` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 206 | 2 | killed |
| `u94-b.W5_warning_without_a_write` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 206 | 1 | killed |

## Row definitions

### `r667.G12_same_recording_no_credit`

_same_recording: a credited hit at another version is title-approximate, not version-differs

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `G12_same_recording_no_credit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 729 against a baseline of 729
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_hit_at_another_version_is_a_version_question_not_an_approximate_one`

Old text:

```
    return fold(wanted.artist) in held.members or _carries(held, token)
```

New text:

```
    return _carries(held, token)
```

### `r667.G13_isrc_not_consulted`

resolve_one: never ask the index by ISRC, the engine before this unit

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `G13_isrc_not_consulted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 729 against a baseline of 729
- Kills: 16 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_file_held_under_the_rows_isrc_is_owned_whatever_its_artist_tag_says`
  - `tests/test_match_states.py::test_a_files_isrc_tag_is_folded_before_it_is_indexed`
  - `tests/test_match_states.py::test_a_persons_answer_is_never_overwritten_by_a_later_resolution`
  - `tests/test_match_states.py::test_a_retired_question_offered_again_is_neither_reopened_nor_duplicated`
  - `tests/test_match_states.py::test_a_retired_question_the_row_asks_again_is_reopened_not_read_as_a_rejection`
  - `tests/test_match_states.py::test_a_retired_question_whose_row_goes_missing_keeps_the_verdict`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[isrc-exact]`
  - `tests/test_match_states.py::test_a_rows_isrc_is_folded_before_it_is_asked`
  - `tests/test_match_states.py::test_an_isrc_hit_at_another_version_spelling_asks_about_the_key_alone`
  - `tests/test_match_states.py::test_an_isrc_hit_on_an_abbreviated_title_is_still_asked_about`
  - `tests/test_match_states.py::test_an_isrc_hit_whose_artist_tag_credits_nobody_the_row_names_still_asks_about_the_key_alone`
  - `tests/test_match_states.py::test_an_isrc_hit_whose_title_disagrees_is_a_question_not_a_match`
  - `tests/test_match_states.py::test_an_isrc_on_a_file_under_another_emoji_title_is_asked_not_settled`
  - `tests/test_match_states.py::test_an_isrc_settled_row_lists_the_files_carrying_the_isrc_and_no_other`
  - `tests/test_match_states.py::test_an_isrc_under_another_artist_and_another_emoji_title_is_asked`
  - ... and 1 more, see the JSON sidecar

Old text:

```
    carrying = index.held_by_isrc(isrc_token(wanted.isrc))
```

New text:

```
    carrying = ()
```

### `r667.G15_isrc_hit_skips_key`

resolve_one: an ISRC hit is matched before the key check runs

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `G15_isrc_hit_skips_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 729 against a baseline of 729
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_isrc_hit_at_another_version_spelling_asks_about_the_key_alone`
  - `tests/test_match_states.py::test_an_isrc_hit_still_asks_about_the_key`
  - `tests/test_match_states.py::test_an_isrc_hit_whose_artist_tag_credits_nobody_the_row_names_still_asks_about_the_key_alone`

Old text:

```
        disagreements = {key_disagreement(wanted.key, held.key) for held in exact}
        if disagreements == {None}:
```

New text:

```
        disagreements = {key_disagreement(wanted.key, held.key) for held in exact}
        if disagreements == {None} or settled:
```

### `r667.G16_isrc_reason_is_exact`

resolve_one: an ISRC hit reports the text reason, so the report claims an agreement that did not happen

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `G16_isrc_reason_is_exact`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 729 against a baseline of 729
- Kills: 11 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_file_held_under_the_rows_isrc_is_owned_whatever_its_artist_tag_says`
  - `tests/test_match_states.py::test_a_files_isrc_tag_is_folded_before_it_is_indexed`
  - `tests/test_match_states.py::test_a_persons_answer_is_never_overwritten_by_a_later_resolution`
  - `tests/test_match_states.py::test_a_retired_question_offered_again_is_neither_reopened_nor_duplicated`
  - `tests/test_match_states.py::test_a_retired_question_the_row_asks_again_is_reopened_not_read_as_a_rejection`
  - `tests/test_match_states.py::test_a_retired_question_whose_row_goes_missing_keeps_the_verdict`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[isrc-exact]`
  - `tests/test_match_states.py::test_a_rows_isrc_is_folded_before_it_is_asked`
  - `tests/test_match_states.py::test_an_isrc_on_a_file_under_another_emoji_title_is_asked_not_settled`
  - `tests/test_match_states.py::test_an_isrc_settled_row_lists_the_files_carrying_the_isrc_and_no_other`
  - `tests/test_match_states.py::test_the_verb_lists_a_retired_question_only_when_asked_for_everything`

Old text:

```
        exact, agreed = settled, Why.ISRC_EXACT
```

New text:

```
        exact, agreed = settled, Why.EXACT
```

### `r667.G17_reader_drops_isrc`

_read_from_disk: the ISRC tag is read and not carried, so the index has nothing to be asked by

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `G17_reader_drops_isrc`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 729 against a baseline of 729
- Kills: 17 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_file_held_under_the_rows_isrc_is_owned_whatever_its_artist_tag_says`
  - `tests/test_match_states.py::test_a_files_isrc_tag_is_folded_before_it_is_indexed`
  - `tests/test_match_states.py::test_a_persons_answer_is_never_overwritten_by_a_later_resolution`
  - `tests/test_match_states.py::test_a_retired_question_offered_again_is_neither_reopened_nor_duplicated`
  - `tests/test_match_states.py::test_a_retired_question_the_row_asks_again_is_reopened_not_read_as_a_rejection`
  - `tests/test_match_states.py::test_a_retired_question_whose_row_goes_missing_keeps_the_verdict`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[isrc-exact]`
  - `tests/test_match_states.py::test_a_rows_isrc_is_folded_before_it_is_asked`
  - `tests/test_match_states.py::test_a_single_artist_file_is_indexed_once_and_the_rule_moves_nothing`
  - `tests/test_match_states.py::test_an_isrc_hit_at_another_version_spelling_asks_about_the_key_alone`
  - `tests/test_match_states.py::test_an_isrc_hit_on_an_abbreviated_title_is_still_asked_about`
  - `tests/test_match_states.py::test_an_isrc_hit_whose_artist_tag_credits_nobody_the_row_names_still_asks_about_the_key_alone`
  - `tests/test_match_states.py::test_an_isrc_hit_whose_title_disagrees_is_a_question_not_a_match`
  - `tests/test_match_states.py::test_an_isrc_on_a_file_under_another_emoji_title_is_asked_not_settled`
  - `tests/test_match_states.py::test_an_isrc_settled_row_lists_the_files_carrying_the_isrc_and_no_other`
  - ... and 2 more, see the JSON sidecar

Old text:

```
        isrc=isrc_token(read["isrc"]),
```

New text:

```
        isrc="",
```

### `r667.G3_members_not_split`

credited_members: a comma separated tag is one name, so nobody is a member

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `G3_members_not_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 729 against a baseline of 729
- Kills: 6 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_track_held_with_no_isrc_under_a_credited_list_is_owned_and_nothing_is_listed`
  - `tests/test_match_states.py::test_a_credited_hit_at_another_version_is_a_version_question_not_an_approximate_one`
  - `tests/test_match_states.py::test_a_file_with_no_isrc_tag_is_owned_when_the_primary_artist_is_a_credited_member`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[credited-exact]`
  - `tests/test_match_states.py::test_the_credited_list_rule_tells_two_emoji_titles_apart`
  - `tests/test_match_states.py::test_the_primary_artist_need_not_be_first_in_the_credited_list`

Old text:

```
    return tuple(part for part in (piece.strip() for piece in str(artist).split(",")) if part)
```

New text:

```
    return (str(artist).strip(),) if str(artist).strip() else ()
```

### `r667.G4_members_not_folded`

Owned.members: the credited names unfolded, so case and marks decide membership

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `G4_members_not_folded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 729 against a baseline of 729
- Kills: 5 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_hit_at_another_version_is_a_version_question_not_an_approximate_one`
  - `tests/test_match_states.py::test_a_file_with_no_isrc_tag_is_owned_when_the_primary_artist_is_a_credited_member`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[credited-exact]`
  - `tests/test_match_states.py::test_a_single_artist_file_is_indexed_once_and_the_rule_moves_nothing`
  - `tests/test_match_states.py::test_the_credited_list_rule_tells_two_emoji_titles_apart`

Old text:

```
            self, "members", frozenset(fold(name) for name in credited_members(self.artist))
```

New text:

```
            self, "members", frozenset(credited_members(self.artist))
```

### `r667.G5_empty_isrc_asks`

held_by_isrc: an empty token asks the map instead of answering nothing

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `G5_empty_isrc_asks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 729 against a baseline of 729
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_empty_isrc_token_asks_the_index_nothing`

Old text:

```
        return self.by_isrc.get(isrc, ()) if isrc else ()
```

New text:

```
        return self.by_isrc.get(isrc, ())
```

### `r667.G8_no_credited_rule`

held: the recording token alone, the rule every caller had before this unit

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `G8_no_credited_rule`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 729 against a baseline of 729
- Kills: 6 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_track_held_with_no_isrc_under_a_credited_list_is_owned_and_nothing_is_listed`
  - `tests/test_match_states.py::test_a_credited_hit_at_another_version_is_a_version_question_not_an_approximate_one`
  - `tests/test_match_states.py::test_a_file_with_no_isrc_tag_is_owned_when_the_primary_artist_is_a_credited_member`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[credited-exact]`
  - `tests/test_match_states.py::test_the_credited_list_rule_tells_two_emoji_titles_apart`
  - `tests/test_match_states.py::test_the_primary_artist_need_not_be_first_in_the_credited_list`

Old text:

```
        return exact + credited
```

New text:

```
        return exact
```

### `r312.W2_worker_writes_nothing`

handle_resort: the item report always says nothing was left

- File: `src/cratekit/write/routing_cli.py`
- Source: `r312.json`, row `W2_worker_writes_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 8 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_refusal_raised_before_the_drive_carries_no_leftover_step`
  - `tests/test_routing_workers.py::test_a_resort_names_the_membership_it_left_where_it_was`
  - `tests/test_routing_workers.py::test_a_resort_resume_that_drove_nothing_names_no_leftover`
  - `tests/test_routing_workers.py::test_a_resort_that_failed_part_way_still_names_what_the_finished_tree_left`
  - `tests/test_routing_workers.py::test_a_second_process_names_what_the_first_ones_tree_left`
  - `tests/test_routing_workers.py::test_each_worker_names_its_own_verb_and_rebuilds_the_item_it_was_handed`
  - `tests/test_routing_workers.py::test_one_jobs_leftovers_are_not_counted_under_another`
  - `tests/test_routing_workers.py::test_the_whole_list_is_written_where_the_warning_says_it_is`

Old text:

```
            "left_behind": [rebuild.left_behind_record(entry) for entry in left],
```

New text:

```
            "left_behind": [],
```

### `r312.W3_success_exit_silent`

_resume: the success envelope carries no leftover warning

- File: `src/cratekit/write/routing_cli.py`
- Source: `r312.json`, row `W3_success_exit_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 5 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_resort_names_the_membership_it_left_where_it_was`
  - `tests/test_routing_workers.py::test_a_resort_resume_that_drove_nothing_names_no_leftover`
  - `tests/test_routing_workers.py::test_a_second_process_names_what_the_first_ones_tree_left`
  - `tests/test_routing_workers.py::test_one_jobs_leftovers_are_not_counted_under_another`
  - `tests/test_routing_workers.py::test_the_whole_list_is_written_where_the_warning_says_it_is`

Old text:

```
                *rebuild.left_behind_warnings(records, listed_in=listed_in),

```

New text:

```
(empty)
```

### `r312.W4_failure_exit_silent`

_resume: a refusal is re-raised as it came, the leftovers never added to it

- File: `src/cratekit/write/routing_cli.py`
- Source: `r312.json`, row `W4_failure_exit_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_refusal_raised_before_the_drive_carries_no_leftover_step`
  - `tests/test_routing_workers.py::test_a_resort_that_failed_part_way_still_names_what_the_finished_tree_left`

Old text:

```
        raise _with_left_behind(failed, frozen, job.job_id) from failed
```

New text:

```
        raise
```

### `r312.W5_cause_steps_replaced`

_with_left_behind: replace the recorded steps with the leftover step, not append to them

- File: `src/cratekit/write/routing_cli.py`
- Source: `r312.json`, row `W5_cause_steps_replaced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_resort_that_failed_part_way_still_names_what_the_finished_tree_left`

Old text:

```
                cause.remediation, steps=(*cause.remediation.steps, message)
```

New text:

```
                cause.remediation, steps=(message,)
```

### `r312.W7b_pre_drive_refusal_extended`

_resume: drop the guard that re-raises a refusal raised before the drive. Measured ZERO on the first pass over a full run of 9679, then re-measured after test_a_refusal_raised_before_the_drive_carries_no_leftover_step was written against it

- File: `src/cratekit/write/routing_cli.py`
- Source: `r312.json`, row `W7b_pre_drive_refusal_extended`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_refusal_raised_before_the_drive_carries_no_leftover_step`

Old text:

```
        if frozen is None:
            raise
        raise _with_left_behind
```

New text:

```
        raise _with_left_behind
```

### `r312.W8_list_not_by_job`

_left_behind: point at the shared reports directory, not this job's

- File: `src/cratekit/write/routing_cli.py`
- Source: `r312.json`, row `W8_list_not_by_job`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_one_jobs_leftovers_are_not_counted_under_another`
  - `tests/test_routing_workers.py::test_the_whole_list_is_written_where_the_warning_says_it_is`

Old text:

```
    return records, str(jobs.store_dir(cfg) / RESORT_ARTIFACTS.final / job_id)
```

New text:

```
    return records, str(jobs.store_dir(cfg) / RESORT_ARTIFACTS.final)
```

### `r318-b.C7_trees_not_deduplicated`

_skipped_files: a tree the writer skipped a file in twice is listed twice

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318-b.json`, row `C7_trees_not_deduplicated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_file_skipped_twice_in_one_tree_names_that_tree_once`

Old text:

```
                "trees": sorted(set(tree_ids)),
```

New text:

```
                "trees": sorted(tree_ids),
```

### `r318-b.N1_no_native_key_dropped`

apply_inbox: the no-native-tree answer carries no skipped_files key, so the payload shape differs by branch

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318-b.json`, row `N1_no_native_key_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_on_a_library_with_no_native_tree_says_so`

Old text:

```
            "skipped": 0,
            "skipped_files": [],
        }
```

New text:

```
            "skipped": 0,
        }
```

### `r318-b.W2_cap_halved`

Halve the cap on how many skipped files a warning names, 10 to 5

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318-b.json`, row `W2_cap_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_skip_warning_counts_every_file_and_caps_the_names`

Old text:

```
SKIPPED_NAMED = 10
```

New text:

```
SKIPPED_NAMED = 5
```

### `r318.C1_skipped_files_always_empty`

apply_inbox: skipped_files is always empty, the headline defect R-318 measured, a count and no file

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `C1_skipped_files_always_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 4 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_names_the_file_it_could_not_file_and_why`
  - `tests/test_routing_workers.py::test_a_file_two_rows_claim_is_reported_ambiguous_with_both_rows`
  - `tests/test_routing_workers.py::test_a_row_rekordbox_removed_is_reported_withdrawn_not_unimported`
  - `tests/test_routing_workers.py::test_the_human_output_names_the_skipped_file`

Old text:

```
        "skipped_files": _skipped_files(cfg, rows, missed),
```

New text:

```
        "skipped_files": [],
```

### `r318.C2_tombstones_not_consulted`

_skipped_files: match against the live index instead of the tombstoned one, so withdrawn can never be told from not imported

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `C2_tombstones_not_consulted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_row_rekordbox_removed_is_reported_withdrawn_not_unimported`

Old text:

```
        paths, index.by_tombstoned_location, root=cfg.library.root, prefix_map=rules
```

New text:

```
        paths, index.by_active_location, root=cfg.library.root, prefix_map=rules
```

### `r318.C3_ambiguous_ids_dropped`

_skipped_files: an ambiguous file names no rows, so a person cannot see which two rows to choose between

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `C3_ambiguous_ids_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_file_two_rows_claim_is_reported_ambiguous_with_both_rows`

Old text:

```
            ids = alive.content_ids
        elif
```

New text:

```
            ids = ()
        elif
```

### `r318.C4_withdrawn_ids_dropped`

_skipped_files: a withdrawn file names no tombstoned row

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `C4_withdrawn_ids_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_row_rekordbox_removed_is_reported_withdrawn_not_unimported`

Old text:

```
            ids = dead.content_ids or ((dead.content_id,) if dead.content_id else ())
```

New text:

```
            ids = ()
```

### `r318.C5_withdrawn_single_id_dropped`

_skipped_files: a withdrawn file with ONE tombstone names nothing, only the ambiguous-tombstone ids survive

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `C5_withdrawn_single_id_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_row_rekordbox_removed_is_reported_withdrawn_not_unimported`

Old text:

```
            ids = dead.content_ids or ((dead.content_id,) if dead.content_id else ())
```

New text:

```
            ids = dead.content_ids
```

### `r318.C6_trees_emptied`

_skipped_files: the record names no tree it was declared into

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `C6_trees_emptied`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_names_the_file_it_could_not_file_and_why`
  - `tests/test_routing_workers.py::test_a_file_skipped_twice_in_one_tree_names_that_tree_once`

Old text:

```
                "trees": sorted(set(tree_ids)),
```

New text:

```
                "trees": [],
```

### `r318.C8_path_reduced_to_name`

_skipped_files: the payload carries the file name instead of the full path

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `C8_path_reduced_to_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_names_the_file_it_could_not_file_and_why`

Old text:

```
                "path": path,
```

New text:

```
                "path": Path(path).name,
```

### `r318.C9_warnings_not_emitted`

route_inbox: the skip warnings never reach the envelope, so the human output, which prints warnings and no totals, names no file

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `C9_warnings_not_emitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 4 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_names_the_file_it_could_not_file_and_why`
  - `tests/test_routing_workers.py::test_a_file_two_rows_claim_is_reported_ambiguous_with_both_rows`
  - `tests/test_routing_workers.py::test_a_row_rekordbox_removed_is_reported_withdrawn_not_unimported`
  - `tests/test_routing_workers.py::test_the_human_output_names_the_skipped_file`

Old text:

```
                *skipped_warnings(result["skipped_files"]),
```

New text:

```
(empty)
```

### `r318.W1_cap_not_applied`

skipped_warnings: name every file, the cap never applied

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `W1_cap_not_applied`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_skip_warning_counts_every_file_and_caps_the_names`

Old text:

```
        named = names[:SKIPPED_NAMED]
```

New text:

```
        named = names
```

### `r318.W3_count_is_named_not_whole`

skipped_warnings: the count is the number named rather than the whole set, so a long list reads as a short one

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `W3_count_is_named_not_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_skip_warning_counts_every_file_and_caps_the_names`

Old text:

```
                    f"{len(names)} file(s) in the intake folder were not filed because "
```

New text:

```
                    f"{len(named)} file(s) in the intake folder were not filed because "
```

### `r318.W4_reasons_unsorted`

skipped_warnings: reasons in arrival order, so two runs over one state say things in two orders

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `W4_reasons_unsorted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_skip_warnings_are_one_per_reason_in_a_stable_order`

Old text:

```
    for reason in sorted(by_reason):
```

New text:

```
    for reason in by_reason:
```

### `r318.W5_next_act_dropped`

skipped_warnings: the reason sentence and its next act are replaced by a bare phrase

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `W5_next_act_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_row_rekordbox_removed_is_reported_withdrawn_not_unimported`

Old text:

```
        why = SKIP_NEXT_ACT[routing_pass.Placement(reason)]
```

New text:

```
        why = "of its state"
```

### `u132.W6_resort_note`

The resort resume carries no skipped step note

- File: `src/cratekit/write/routing_cli.py`
- Source: `u132.json`, row `W6_resort_note`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_driven_resume_over_no_favorites_class_names_the_skipped_step[resort]`

Old text:

```
                *rebuild.favorites_skipped_warnings(declared, driven),

```

New text:

```
(empty)
```

### `u155.W3_gate_column`

_column: show a genre sub placement in the energy sub column, the round 1 defect

- File: `src/cratekit/write/routing_cli.py`
- Source: `u155.json`, row `W3_gate_column`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 3 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_database_inbox_gate_shows_a_genre_sub_beside_the_band_and_files_both`
  - `tests/test_routing_workers.py::test_the_export_gate_shows_a_genre_sub_beside_the_band_and_files_both`
  - `tests/test_routing_workers.py::test_the_unplaced_export_names_a_genre_sub_beside_the_band_and_files_both`

Old text:

```
    if routing.genre_sub_named(declared, placement.bucket, placement.sub):
        return genre
```

New text:

```
(empty)
```

### `u155.W4_gate_count`

_placed_counts: count no track as filed into a genre sub

- File: `src/cratekit/write/routing_cli.py`
- Source: `u155.json`, row `W4_gate_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 3 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_database_inbox_gate_shows_a_genre_sub_beside_the_band_and_files_both`
  - `tests/test_routing_workers.py::test_the_export_gate_shows_a_genre_sub_beside_the_band_and_files_both`
  - `tests/test_routing_workers.py::test_the_gate_counts_tracks_filed_into_a_genre_sub`

Old text:

```
        "genre sub": sum(1 for item in tracks if item.get("genre")),
```

New text:

```
        "genre sub": 0,
```

### `u155.W5_owed_once`

_owed_ratings: count a row once per placement again, two for a vocal track

- File: `src/cratekit/write/routing_cli.py`
- Source: `u155.json`, row `W5_owed_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_vocal_track_unrated_is_owed_one_rating_not_one_per_place`

Old text:

```
        if placement.location in counted:
            continue
```

New text:

```
(empty)
```

### `u155.W6_inbox_item_genre`

plan_inbox: carry an empty genre column on every item, the database gate hiding the second place

- File: `src/cratekit/write/routing_cli.py`
- Source: `u155.json`, row `W6_inbox_item_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_database_inbox_gate_shows_a_genre_sub_beside_the_band_and_files_both`

Old text:

```
            "genre": genre.get(str(path), ""),
```

New text:

```
            "genre": "",
```

### `u155.W7_export_item_genre`

plan_export: carry an empty genre column on every item, the export gate hiding the second place

- File: `src/cratekit/write/routing_cli.py`
- Source: `u155.json`, row `W7_export_item_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_export_gate_shows_a_genre_sub_beside_the_band_and_files_both`

Old text:

```
            "vocal": vocal.get(key, ""),
            "genre": decision.genre.get(key, ""),
```

New text:

```
            "vocal": vocal.get(key, ""),
            "genre": "",
```

### `r187-a.C1_blank_not_key`

names_something: ask the text and not the comparison key, so a name of punctuation alone is searched for

- File: `src/cratekit/setbuilder/cli.py`
- Source: `r187-a.json`, row `C1_blank_not_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_name_with_nothing_in_it_is_an_unknown_anchor[ - ]`
  - `tests/test_setbuilder_cli.py::test_an_empty_name_refuses_before_any_scan`

Old text:

```
    return bool(setbuilder.match_key("", text))
```

New text:

```
    return bool(text.strip())
```

### `r187-a.C2_uncapped`

named_anchor: list every candidate, so a vague name prints a whole label

- File: `src/cratekit/setbuilder/cli.py`
- Source: `r187-a.json`, row `C2_uncapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_the_listing_is_capped_and_says_how_many_it_reached`

Old text:

```
    shown = matched.candidates[: setbuilder.CANDIDATE_LIMIT]
```

New text:

```
    shown = matched.candidates
```

### `r187-a.C3_mutex`

build: declare --named on the parser and not in the exclusive group, so it can sit beside a path or a label

- File: `src/cratekit/setbuilder/cli.py`
- Source: `r187-a.json`, row `C3_mutex`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_name_beside_another_anchor_form_is_the_parsers_verdict[path]`
  - `tests/test_setbuilder_cli.py::test_a_name_beside_another_anchor_form_is_the_parsers_verdict[unowned]`

Old text:

```
    anchor.add_argument(
        "--named",
```

New text:

```
    parser.add_argument(
        "--named",
```

### `r187-a.C4_key_beside_name`

set_build: a key beside --named is let through and silently ignored

- File: `src/cratekit/setbuilder/cli.py`
- Source: `r187-a.json`, row `C4_key_beside_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_supplied_key_beside_a_name_refuses_rather_than_being_ignored`

Old text:

```
    if ctx.args.key is not None or ctx.args.tempo is not None:
```

New text:

```
    if ctx.args.named is None and (ctx.args.key is not None or ctx.args.tempo is not None):
```

### `r187-a.C5_empty_name_scans`

set_build: an empty name pays for the library walk before it is refused

- File: `src/cratekit/setbuilder/cli.py`
- Source: `r187-a.json`, row `C5_empty_name_scans`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_empty_name_refuses_before_any_scan`

Old text:

```
        index = _index(cfg, root) if names_something(ctx.args.named) else ()
```

New text:

```
        index = _index(cfg, root)
```

### `r187-a.C6_no_cache_path`

_index: pass no cache path, which is R-188 itself, every set a full scan

- File: `src/cratekit/setbuilder/cli.py`
- Source: `r187-a.json`, row `C6_no_cache_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 3 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_second_run_reads_no_tag_it_already_holds`
  - `tests/test_setbuilder_cli.py::test_the_first_run_opens_each_file_once_and_the_second_none`
  - `tests/test_setbuilder_cli.py::test_the_verb_writes_its_declared_cache_and_nothing_of_the_librarys`

Old text:

```
        cache_path=config.state_path("setbuilder_index_cache", cfg),
```

New text:

```
        cache_path=None,
```

### `u43-author-light.A1_first_track_wins`

anchor_in_index returns the first indexed track instead of the one at the path, which is exactly what the fuzzy lookup this design replaces does when a version suffix is present

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `A1_first_track_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 4 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_anchor_that_is_not_in_the_library_refuses_with_a_vocabulary_code`
  - `tests/test_setbuilder_cli.py::test_an_anchor_the_index_does_not_hold_is_absent_rather_than_approximated`
  - `tests/test_setbuilder_cli.py::test_an_exact_name_is_never_lost_to_a_longer_title_whichever_came_first`
  - `tests/test_setbuilder_cli.py::test_what_plays_after_a_track_is_asked_by_name`

Old text:

```
    wanted = str(path)
    for track in index:
        if track.path == wanted:
            return track
```

New text:

```
    wanted = str(path)
    for track in index:
        if track.path or wanted:
            return track
```

### `u43-author-light.A3_containment_not_checked`

anchor_path stops checking that the anchor is inside the library, so a path walking out with .. is scanned for and refused as unindexed rather than refused as outside

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `A3_containment_not_checked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_anchor_outside_the_library_refuses_before_any_scan`
  - `tests/test_setbuilder_cli.py::test_an_anchor_that_walks_out_of_the_library_is_refused`

Old text:

```
    if not _within(candidate, root):
```

New text:

```
    if _within(candidate, root) and False:
```

### `u43-author-light.A4_empty_anchor_defaults`

anchor_path stops refusing an empty anchor, which turns it into the library root and asks the index for a directory

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `A4_empty_anchor_defaults`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_empty_anchor_is_refused_rather_than_defaulted`
  - `tests/test_setbuilder_cli.py::test_an_empty_anchor_refuses_through_the_dispatcher`

Old text:

```
    if not anchor:
        raise refuse(
```

New text:

```
    if anchor and not anchor:
        raise refuse(
```

### `u43-author-light.C1_no_lower_bound`

positive_count stops refusing zero and negatives, so build_plan's pool[: count or DEFAULT_POOL] silently turns 0 into 8 and -1 into a dropped last companion

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `C1_no_lower_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 4 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_count_below_one_is_refused_at_the_parser[-1]`
  - `tests/test_setbuilder_cli.py::test_a_count_below_one_is_refused_at_the_parser[-8]`
  - `tests/test_setbuilder_cli.py::test_a_count_below_one_is_refused_at_the_parser[0]`
  - `tests/test_setbuilder_cli.py::test_a_count_below_one_is_the_parsers_verdict_and_not_a_refusal`

Old text:

```
    value = int(text)
    if value < 1:
        raise ValueError(f"{text!r} is not a positive count")
    return value
```

New text:

```
    return int(text)
```

### `u43-author-light.C2_bound_off_by_one`

The bound is loosened by one rather than removed, so zero passes and negatives do not. A guard whose constant can be moved without a death is a guard that pins nothing.

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `C2_bound_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_count_below_one_is_refused_at_the_parser[0]`
  - `tests/test_setbuilder_cli.py::test_a_count_below_one_is_the_parsers_verdict_and_not_a_refusal`

Old text:

```
    if value < 1:
```

New text:

```
    if value < 0:
```

### `u43-author-light.P1_anchor_absent_from_digest`

The digest stops covering the anchor, so two plans over the same companions and different anchors are indistinguishable

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `P1_anchor_absent_from_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_owned_and_an_unowned_anchor_in_one_key_digest_apart`
  - `tests/test_setbuilder_cli.py::test_the_anchor_is_in_the_digest_even_when_the_companions_are_identical`

Old text:

```
        "digest": digest_of({"kind": "setbuild", "anchor": rendered["anchor"], "items": items}),
```

New text:

```
        "digest": digest_of({"kind": "setbuild", "items": items}),
```

### `u43-author-light.P3_pool_leads_the_items`

The pool leads and the sequence follows, so the recommendation is no longer at the top of the array a consumer reads

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `P3_pool_leads_the_items`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_the_sequence_leads_the_items_and_carries_its_own_order`

Old text:

```
    ordered = list(plan.sequence) + [s for s in plan.pool if id(s) not in placed]
```

New text:

```
    ordered = [s for s in plan.pool if id(s) not in placed] + list(plan.sequence)
```

### `u43-author-light.P4_no_positions_at_all`

Every item reports position null, so the suggested sequence is not recoverable from the payload

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `P4_no_positions_at_all`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 4 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_unowned_sequence_places_each_companion_once`
  - `tests/test_setbuilder_cli.py::test_one_either_companion_of_an_owned_anchor_is_placed_once`
  - `tests/test_setbuilder_cli.py::test_plan_for_composes_the_engine_exactly_as_build_set_does`
  - `tests/test_setbuilder_cli.py::test_the_sequence_leads_the_items_and_carries_its_own_order`

Old text:

```
        {**entry, "position": placed.get(id(scored))}
```

New text:

```
        {**entry, "position": None}
```

### `u43-author-light.P5_role_ignored`

The role flag is dropped on the way to the engine, so --role before answers with both sides

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `P5_role_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_role_narrows_the_answer_to_one_side`
  - `tests/test_setbuilder_cli.py::test_the_role_flag_reaches_the_engine`

Old text:

```
    plan = setbuilder.build_plan(ranked, resolved, count=count, role=role)
```

New text:

```
    plan = setbuilder.build_plan(ranked, resolved, count=count, role=None)
```

### `u43-author-light.P7_vox_threshold_ignored`

The vocal threshold is dropped on the way to the ranker, which makes the fifth ranking signal permanently neutral and its whole weight dead

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `P7_vox_threshold_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_the_vocal_signal_is_reachable_only_because_a_threshold_can_be_supplied`

Old text:

```
        vox_threshold=vox_threshold,
    )
    plan = setbuilder.build_plan
```

New text:

```
        vox_threshold=None,
    )
    plan = setbuilder.build_plan
```

### `u43-author-round-2.A2_no_resolved_second_pass`

ROUND ONE: zero. Drop the resolved second pass in anchor_in_index, so a path spelled through a symlink or a different absolute form never matches

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-round-2.json`, row `A2_no_resolved_second_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_anchor_spelled_through_a_symlink_still_resolves`

Old text:

```
    try:
        resolved = path.resolve()
    except OSError:
        return None
    for track in index:
        if not track.path:
            continue
        try:
            if Path(track.path).resolve() == resolved:
                return track
        except OSError:
            continue
    return None
```

New text:

```
    return None
```

### `u43-author-round-2.H2_empty_is_a_no_op`

ROUND ONE: zero. A plan with no companions reports NO_OP rather than OK, which tells a consumer nothing happened when the question was answered

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-round-2.json`, row `H2_empty_is_a_no_op`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_library_holding_only_the_anchor_is_an_empty_plan_and_not_a_failure`

Old text:

```
    return ctx.envelope(data=plan, outcome=Outcome.OK)
```

New text:

```
    return ctx.envelope(
        data=plan, outcome=Outcome.OK if plan["items"] else Outcome.NO_OP
    )
```

### `u43-author-round-2.H3_missing_root_not_refused`

ROUND ONE: zero. The configured library root is no longer checked before the scan, so an unmounted volume scans zero files and every anchor comes back unindexed

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-round-2.json`, row `H3_missing_root_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_unreachable_library_refuses_rather_than_reporting_an_unindexed_anchor`

Old text:

```
    if not root.is_dir():
```

New text:

```
    if root.is_dir() and False:
```

### `u43-author-round-2.P2_items_absent_from_digest`

ROUND ONE: zero. The digest stops covering the items, so two entirely different sets of recommendations for one anchor carry one identity

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-round-2.json`, row `P2_items_absent_from_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_two_plans_over_the_same_anchor_and_different_companions_digest_apart`

Old text:

```
        "digest": digest_of({"kind": "setbuild", "anchor": rendered["anchor"], "items": items}),
```

New text:

```
        "digest": digest_of({"kind": "setbuild", "anchor": rendered["anchor"]}),
```

### `u43-author-round-2.P6_count_ignored`

ROUND ONE: zero. The count flag is dropped on the way to the engine, so the pool is always the default eight

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-round-2.json`, row `P6_count_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_count_caps_the_companions`

Old text:

```
    plan = setbuilder.build_plan(ranked, resolved, count=count, role=role)
```

New text:

```
    plan = setbuilder.build_plan(ranked, resolved, count=None, role=role)
```

### `u43-author-round-2.V1_pool_total_is_the_union`

totals reports the union size where it says pool, which is the wrong number and the one a reader would otherwise have to derive. The round-one arithmetic surprise is exactly this confusion, so the new count guard owes a death here

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-round-2.json`, row `V1_pool_total_is_the_union`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_count_caps_the_companions`

Old text:

```
        "pool": len(plan.pool),
```

New text:

```
        "pool": len(items),
```

### `u43-author-round-2.V3_root_check_reports_instead_of_refusing`

The missing root produces an empty plan and an OK exit rather than a refusal, which is the clean-report-over-unreadable-state shape rather than the crash shape. A guard that only catches the crash is not the guard this row needs

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-round-2.json`, row `V3_root_check_reports_instead_of_refusing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_unreachable_library_refuses_rather_than_reporting_an_unindexed_anchor`

Old text:

```
    if not root.is_dir():
        raise refuse(
```

New text:

```
    if not root.is_dir():
        return ctx.envelope(
            data=plan_for(
                setbuilder.Track(
                    artist="", title="", key="", bpm=None, genre="",
                    energy=None, vox=None, voxgender=None, match="",
                ),
                (),
                declared=taxonomy.default_taxonomy(),
            ),
            outcome=Outcome.OK,
        )
    if False:
        raise refuse(
```

### `u98-a.K1_key_off_wheel`

camelot_key: drop the refusal, so a code off the wheel parses to the empty string

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-a.json`, row `K1_key_off_wheel`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 7 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_key_off_the_wheel_is_refused_at_the_parser[0A]`
  - `tests/test_setbuilder_cli.py::test_a_key_off_the_wheel_is_refused_at_the_parser[13A]`
  - `tests/test_setbuilder_cli.py::test_a_key_off_the_wheel_is_refused_at_the_parser[13C]`
  - `tests/test_setbuilder_cli.py::test_a_key_off_the_wheel_is_refused_at_the_parser[8C]`
  - `tests/test_setbuilder_cli.py::test_a_key_off_the_wheel_is_refused_at_the_parser[]`
  - `tests/test_setbuilder_cli.py::test_a_key_off_the_wheel_is_refused_at_the_parser[eight]`
  - `tests/test_setbuilder_cli.py::test_a_key_off_the_wheel_is_the_parsers_verdict`

Old text:

```
    if not canonical:
        raise ValueError(f"{text!r} is not a Camelot code between 1A and 12B")

```

New text:

```
(empty)
```

### `u98-a.T1_tempo_nonfinite`

positive_tempo: drop the finiteness half, so NaN and inf parse

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-a.json`, row `T1_tempo_nonfinite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_tempo_that_would_empty_the_pool_is_refused_at_the_parser[inf]`
  - `tests/test_setbuilder_cli.py::test_a_tempo_that_would_empty_the_pool_is_refused_at_the_parser[nan]`

Old text:

```
if not math.isfinite(value) or value <= 0:
```

New text:

```
if value <= 0:
```

### `u98-a.T2_tempo_zero`

positive_tempo: move the bound to strictly negative, so zero parses

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-a.json`, row `T2_tempo_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_tempo_that_would_empty_the_pool_is_refused_at_the_parser[0]`

Old text:

```
if not math.isfinite(value) or value <= 0:
```

New text:

```
if not math.isfinite(value) or value < 0:
```

### `u98-a.U1_empty_label`

unowned_anchor: drop the empty label refusal, so an empty label resolves by key alone

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-a.json`, row `U1_empty_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_empty_unowned_label_refuses_as_an_unknown_anchor`

Old text:

```
    if not label:
        raise refuse(
            "setbuild-anchor-unknown",
            "setbuild needs the track to build the set around",
            steps=("pass a label with --unowned, and its Camelot key with --key",),
            origin=("setbuilder", "cli"),
        )

```

New text:

```
(empty)
```

### `u98-a.U2_key_missing`

unowned_anchor: drop the key missing refusal, so an unresolved anchor reaches the engine

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-a.json`, row `U2_key_missing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_unowned_anchor_with_no_key_refuses`
  - `tests/test_setbuilder_cli.py::test_an_unowned_anchor_with_no_key_refuses_through_the_dispatcher`

Old text:

```
    if resolved.key is None:
```

New text:

```
    if False:
```

### `u98-a.U3_reported_owned`

unowned_anchor: return the anchor marked owned and confirmed, the envelope's honesty flags

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-a.json`, row `U3_reported_owned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 5 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_owned_and_an_unowned_anchor_in_one_key_digest_apart`
  - `tests/test_setbuilder_cli.py::test_an_unowned_anchor_in_8a_ranks_the_library_against_it`
  - `tests/test_setbuilder_cli.py::test_an_unowned_anchor_is_ranked_through_the_dispatcher`
  - `tests/test_setbuilder_cli.py::test_an_unowned_label_naming_an_owned_track_exactly_is_held_and_not_ranked`
  - `tests/test_setbuilder_cli.py::test_an_unowned_label_that_names_an_owned_title_is_never_matched_to_it`

Old text:

```
            detail={"label": label, "unresolved": resolved.unresolved},
        )
    return resolved
```

New text:

```
            detail={"label": label, "unresolved": resolved.unresolved},
        )
    return setbuilder.Anchor(
        key=resolved.key, bpm=resolved.bpm, owned=True, display=resolved.display
    )
```

### `u98-a.U4_tempo_dropped`

unowned_anchor: pass no tempo to the engine, so --bpm is silently ignored

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-a.json`, row `U4_tempo_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 3 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_supplied_tempo_narrows_an_unowned_anchor_to_its_band`
  - `tests/test_setbuilder_cli.py::test_an_owned_and_an_unowned_anchor_in_one_key_digest_apart`
  - `tests/test_setbuilder_cli.py::test_an_unowned_anchor_is_ranked_through_the_dispatcher`

Old text:

```
resolve_anchor(label, (), key=key, bpm=tempo)
```

New text:

```
resolve_anchor(label, (), key=key, bpm=None)
```

### `u98-a.X1_mutex`

build: declare the anchor and --unowned on the parser, not in an exclusive group

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-a.json`, row `X1_mutex`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 3 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_name_beside_another_anchor_form_is_the_parsers_verdict[path]`
  - `tests/test_setbuilder_cli.py::test_a_name_beside_another_anchor_form_is_the_parsers_verdict[unowned]`
  - `tests/test_setbuilder_cli.py::test_a_path_and_an_unowned_label_together_are_the_parsers_verdict`

Old text:

```
    anchor = parser.add_mutually_exclusive_group()
```

New text:

```
    anchor = parser
```

### `u98-b.E1_existing_containment`

existing sample: anchor_path drops the library containment refusal

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-b.json`, row `E1_existing_containment`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_anchor_outside_the_library_refuses_before_any_scan`
  - `tests/test_setbuilder_cli.py::test_an_anchor_that_walks_out_of_the_library_is_refused`

Old text:

```
    if not _within(candidate, root):
```

New text:

```
    if False:
```

### `u98-b.H1_held_not_excluded`

plan_for: report the exact match copies but leave them in the ranked index

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-b.json`, row `H1_held_not_excluded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_unowned_label_naming_an_owned_track_exactly_is_held_and_not_ranked`

Old text:

```
        index = [t for t in index if not (label and t.match == label)]
```

New text:

```
(empty)
```

### `u98-b.H2_held_not_reported`

plan_for: exclude the exact match copies but report none

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-b.json`, row `H2_held_not_reported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_unowned_label_naming_an_owned_track_exactly_is_held_and_not_ranked`

Old text:

```
        totals["held"] = held
```

New text:

```
        totals["held"] = []
```

### `u98-b.H3_held_fuzzy`

plan_for: widen the exact match to containment, the fuzzy shape the empty index exists to avoid

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-b.json`, row `H3_held_fuzzy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_unowned_label_that_names_an_owned_title_is_never_matched_to_it`

Old text:

```
        index = [t for t in index if not (label and t.match == label)]
```

New text:

```
        index = [t for t in index if not (label and label in t.match)]
```

### `u98-b.S1_supplied_beside_path`

set_build: drop the refusal of --key or --bpm beside a path anchor, so both are silently ignored

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-b.json`, row `S1_supplied_beside_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 3 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_supplied_key_beside_a_name_refuses_rather_than_being_ignored`
  - `tests/test_setbuilder_cli.py::test_a_supplied_value_beside_a_path_anchor_refuses_rather_than_being_ignored[key]`
  - `tests/test_setbuilder_cli.py::test_a_supplied_value_beside_a_path_anchor_refuses_rather_than_being_ignored[tempo]`

Old text:

```
    if ctx.args.key is not None or ctx.args.tempo is not None:
```

New text:

```
    if False:
```

### `u98-b.S2_tempo_half`

set_build: drop only the tempo half of that refusal

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-b.json`, row `S2_tempo_half`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_supplied_value_beside_a_path_anchor_refuses_rather_than_being_ignored[tempo]`

Old text:

```
    if ctx.args.key is not None or ctx.args.tempo is not None:
```

New text:

```
    if ctx.args.key is not None:
```

### `u240.M11_needle_is_the_name`

_label_payload: freeze the label's name as its needle, ignoring --match

- File: `src/cratekit/tagging/cli.py`
- Source: `u240.json`, row `M11_needle_is_the_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 334 against a baseline of 334
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_the_needles_are_frozen_with_the_genres_when_the_sweep_is_queued`
  - `tests/test_tag_folder_copyright.py::test_two_labels_sharing_a_display_name_never_lend_each_other_a_genre`

Old text:

```
            entry.label_id: {"name": entry.name, "needle": entry.match or entry.name}
```

New text:

```
            entry.label_id: {"name": entry.name, "needle": entry.name}
```

### `u240.M12_raw_line_matched`

copyright_matcher: match the needle against the raw line, mark and year included (round two's first blocker)

- File: `src/cratekit/tagging/cli.py`
- Source: `u240.json`, row `M12_raw_line_matched`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 334 against a baseline of 334
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_lines_year_never_completes_a_needle[1985 Music-(P) 1985 Music For Nations]`
  - `tests/test_tag_folder_copyright.py::test_a_lines_year_never_completes_a_needle[2020 Vision-\u2117 2020 Vision Quest]`

Old text:

```
        credit = credits[0]
```

New text:

```
        credit = line
```

### `u240.M13_two_way_match`

copyright_matcher: match either way, so a short line inside a long needle names it

- File: `src/cratekit/tagging/cli.py`
- Source: `u240.json`, row `M13_two_way_match`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 334 against a baseline of 334
- Kills: 7 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_letter_outside_ascii_never_folds_away_from_a_needle[\u6771\u4eac Records-\u2117 2023 Completely Unrelated Records]`
  - `tests/test_tag_folder_copyright.py::test_a_letter_outside_ascii_never_folds_away_from_a_needle[\xc2me-\u2117 2021 Give Me Records]`
  - `tests/test_tag_folder_copyright.py::test_a_line_carrying_only_part_of_a_needle_names_no_label[(P) 2024 Cronos]`
  - `tests/test_tag_folder_copyright.py::test_a_line_carrying_only_part_of_a_needle_names_no_label[\u2117 2023 Barac]`
  - `tests/test_tag_folder_copyright.py::test_a_line_carrying_only_part_of_a_needle_names_no_label[\u2117 2023 Records]`
  - `tests/test_tag_folder_copyright.py::test_a_line_carrying_only_part_of_a_needle_names_no_label[\u2117 2024 Music]`
  - `tests/test_tag_folder_copyright.py::test_a_sublabels_own_line_names_the_sublabel_and_the_parents_names_the_parent`

Old text:

```
        named = [row for row in rows if label_verify.credit_names(row[1], credit)]
```

New text:

```
        named = [row for row in rows if label_verify.labels_match(row[1], credit)]
```

### `u240.M14_widest_any`

copyright_matcher: the longer needle wins when it carries any other named, not every other

- File: `src/cratekit/tagging/cli.py`
- Source: `u240.json`, row `M14_widest_any`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 334 against a baseline of 334
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_sublabel_beside_a_third_label_settles_nothing`

Old text:

```
            if all(label_verify.credit_names(other[1], row[1]) for other in named)
```

New text:

```
            if any(label_verify.credit_names(other[1], row[1]) for other in named if other is not row)
```

### `u240.M15_no_widest_rule`

copyright_matcher: no specificity rule, so a sublabel's line settles neither label

- File: `src/cratekit/tagging/cli.py`
- Source: `u240.json`, row `M15_no_widest_rule`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 334 against a baseline of 334
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_sublabels_own_line_names_the_sublabel_and_the_parents_names_the_parent`

Old text:

```
        if len(widest) == 1:
```

New text:

```
        if False:
```

### `u240.M16_genres_joined_by_name`

_copyright_seam: join a label's genre by its display name, round one's second blocker

- File: `src/cratekit/tagging/cli.py`
- Source: `u240.json`, row `M16_genres_joined_by_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 334 against a baseline of 334
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_two_labels_sharing_a_display_name_never_lend_each_other_a_genre`

Old text:

```
        held = genres.get(label_id)
```

New text:

```
        held = next((row for row in genres.values() if isinstance(row, Mapping) and row.get("name") == name), None)
```

### `u240.M17_worker_hands_no_seam`

handle: the worker never builds the copyright seam

- File: `src/cratekit/tagging/cli.py`
- Source: `u240.json`, row `M17_worker_hands_no_seam`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 334 against a baseline of 334
- Kills: 8 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_label_batch_with_every_catalogue_blocked_lands_tagged_by_label`
  - `tests/test_tag_folder_copyright.py::test_a_sweep_one_file_of_which_fails_still_reports_every_file`
  - `tests/test_tag_folder_copyright.py::test_an_unregistered_file_in_the_batch_is_left_untagged_and_its_item_fails`
  - `tests/test_tag_folder_copyright.py::test_files_whose_line_named_two_labels_are_counted_and_warned`
  - `tests/test_tag_folder_copyright.py::test_the_needles_are_frozen_with_the_genres_when_the_sweep_is_queued`
  - `tests/test_tag_folder_copyright.py::test_the_report_names_each_file_by_label_by_catalogue_or_not_at_all`
  - `tests/test_tag_folder_copyright.py::test_the_tails_tag_step_lands_a_label_batch_with_every_catalogue_blocked`
  - `tests/test_tag_folder_copyright.py::test_two_labels_sharing_a_display_name_never_lend_each_other_a_genre`

Old text:

```
        copyright_labels=_copyright_seam(payload),
```

New text:

```
        copyright_labels=None,
```

### `u240.M18_way_inverted`

_way: a label's genre reported as a catalogue's

- File: `src/cratekit/tagging/cli.py`
- Source: `u240.json`, row `M18_way_inverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 334 against a baseline of 334
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_label_batch_with_every_catalogue_blocked_lands_tagged_by_label`
  - `tests/test_tag_folder_copyright.py::test_a_sweep_one_file_of_which_fails_still_reports_every_file`
  - `tests/test_tag_folder_copyright.py::test_the_report_names_each_file_by_label_by_catalogue_or_not_at_all`

Old text:

```
    if str(report.get("source") or "") == tag_engine.LABEL_GENRE:
```

New text:

```
    if str(report.get("source") or "") != tag_engine.LABEL_GENRE:
```

### `u240.M19_one_name_ambiguous`

_count_ambiguous: count a line naming one label as ambiguous

- File: `src/cratekit/tagging/cli.py`
- Source: `u240.json`, row `M19_one_name_ambiguous`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 334 against a baseline of 334
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_files_whose_line_named_two_labels_are_counted_and_warned`
  - `tests/test_tag_folder_copyright.py::test_two_labels_sharing_a_display_name_are_two_in_the_ambiguous_count`

Old text:

```
    if len(names) > 1:
```

New text:

```
    if len(names) > 0:
```

### `u240.M20_warning_dropped`

_resume: the two label warning never reaches the envelope

- File: `src/cratekit/tagging/cli.py`
- Source: `u240.json`, row `M20_warning_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 334 against a baseline of 334
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_files_whose_line_named_two_labels_are_counted_and_warned`

Old text:

```
            + _ambiguous_warnings(summary)

```

New text:

```
(empty)
```

### `u240.M21_failed_sweep_unreported`

_with_report: no ending carries the report, so a failed sweep says nothing of its files

- File: `src/cratekit/tagging/cli.py`
- Source: `u240.json`, row `M21_failed_sweep_unreported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 334 against a baseline of 334
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_cancelled_sweep_carries_its_report_too`
  - `tests/test_tag_folder_copyright.py::test_a_refusal_names_ten_failed_files_and_counts_the_rest`
  - `tests/test_tag_folder_copyright.py::test_a_sweep_one_file_of_which_fails_still_reports_every_file`

Old text:

```
    if job.state not in _REPORTED_ENDINGS:
```

New text:

```
    if True:
```

### `u240.M22_failed_items_left_out`

_summary: items with no report are not listed

- File: `src/cratekit/tagging/cli.py`
- Source: `u240.json`, row `M22_failed_items_left_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 334 against a baseline of 334
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_cancelled_sweep_carries_its_report_too`
  - `tests/test_tag_folder_copyright.py::test_a_refusal_names_ten_failed_files_and_counts_the_rest`
  - `tests/test_tag_folder_copyright.py::test_a_sweep_one_file_of_which_fails_still_reports_every_file`

Old text:

```
        if item_id in reported:
```

New text:

```
        if True:
```

### `u240.M23_cap_lowered`

_with_report: name three failed files rather than ten

- File: `src/cratekit/tagging/cli.py`
- Source: `u240.json`, row `M23_cap_lowered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 334 against a baseline of 334
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_refusal_names_ten_failed_files_and_counts_the_rest`

Old text:

```
_FAILED_NAMED = 10
```

New text:

```
_FAILED_NAMED = 3
```

### `u240.M1_two_names_take_the_first`

_by_label: a line naming two registered labels gives the file the first one's genre

- File: `src/cratekit/tagging/tag.py`
- Source: `u240.json`, row `M1_two_names_take_the_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 334 against a baseline of 334
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_line_naming_two_registered_labels_is_refused_for_that_file`
  - `tests/test_tag_folder_copyright.py::test_a_searchers_park_reaches_the_job_as_a_park_on_a_file_its_line_could_not_settle`
  - `tests/test_tag_folder_copyright.py::test_a_sweep_one_file_of_which_fails_still_reports_every_file`
  - `tests/test_tag_folder_copyright.py::test_files_whose_line_named_two_labels_are_counted_and_warned`

Old text:

```
    if len(named) != 1 or not named[0].genre:
```

New text:

```
    if not named or not named[0].genre:
```

### `u240.M2_no_genre_label_named`

_by_label: a line naming one label with no genre is not recorded on the file

- File: `src/cratekit/tagging/tag.py`
- Source: `u240.json`, row `M2_no_genre_label_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 334 against a baseline of 334
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_line_naming_one_label_with_no_genre_is_asked_of_the_catalogues`
  - `tests/test_tag_folder_copyright.py::test_a_line_naming_two_registered_labels_is_refused_for_that_file`
  - `tests/test_tag_folder_copyright.py::test_a_sweep_one_file_of_which_fails_still_reports_every_file`
  - `tests/test_tag_folder_copyright.py::test_files_whose_line_named_two_labels_are_counted_and_warned`

Old text:

```
        return _Labelled(None, own, copyright_labels=tuple(found.label for found in named))
```

New text:

```
        return _Labelled(None, own, copyright_labels=())
```

### `u240.M3_tag_no_longer_outranks_the_line`

_by_label: a file's own label tag no longer comes first, so the line or --label decides a tagged file

- File: `src/cratekit/tagging/tag.py`
- Source: `u240.json`, row `M3_tag_no_longer_outranks_the_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 334 against a baseline of 334
- Kills: 17 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_file_its_own_label_answered_for_is_never_named_as_outranked`
  - `tests/test_label_genre.py::test_a_file_of_a_label_with_no_genre_is_searched_as_today`
  - `tests/test_label_genre.py::test_a_folder_of_mixed_labels_tags_each_by_its_own`
  - `tests/test_label_genre.py::test_a_label_tag_reaches_its_genre_with_no_label_named`
  - `tests/test_label_genre.py::test_a_name_that_is_another_labels_identifier_is_the_label_named_so`
  - `tests/test_label_genre.py::test_a_puls_batch_is_tagged_by_the_label_and_the_report_counts_it_apart`
  - `tests/test_label_genre.py::test_a_puls_file_with_no_genre_gets_its_labels_genre_with_no_searcher_called`
  - `tests/test_label_genre.py::test_a_puls_file_with_no_picture_is_searched_for_its_art_only`
  - `tests/test_label_genre.py::test_a_refusal_on_the_art_search_does_not_fail_a_puls_file`
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`
  - `tests/test_label_genre.py::test_a_tag_carrying_a_labels_name_from_before_its_rename_still_reaches_it`
  - `tests/test_label_genre.py::test_a_tag_naming_a_label_whose_name_is_another_labels_identifier_takes_its_genre`
  - `tests/test_label_genre.py::test_an_art_search_for_a_labelled_file_never_offers_the_general_catalogue_its_isrc`
  - `tests/test_label_genre.py::test_files_whose_own_tag_outranked_the_label_are_counted_and_named`
  - `tests/test_label_genre.py::test_the_verbs_label_names_the_label_of_a_file_with_no_tag_and_the_tag_wins`
  - ... and 2 more, see the JSON sidecar

Old text:

```
    if own:

```

New text:

```
    if False:

```

### `u240.M4_folder_label_no_longer_outranks_the_line`

_by_label: --label no longer comes before the copyright line

- File: `src/cratekit/tagging/tag.py`
- Source: `u240.json`, row `M4_folder_label_no_longer_outranks_the_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 334 against a baseline of 334
- Kills: 9 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_file_that_will_not_take_its_labels_genre_fails_and_is_never_counted_tagged`
  - `tests/test_label_genre.py::test_a_puls_batch_is_tagged_by_the_label_and_the_report_counts_it_apart`
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`
  - `tests/test_label_genre.py::test_a_sweep_queued_before_the_identifier_was_frozen_still_tags_by_its_labels_name`
  - `tests/test_label_genre.py::test_files_whose_own_tag_outranked_the_label_are_counted_and_named`
  - `tests/test_label_genre.py::test_the_genres_are_frozen_when_the_sweep_is_queued`
  - `tests/test_label_genre.py::test_the_label_carrying_the_genre_still_gives_it_under_the_shared_name`
  - `tests/test_label_genre.py::test_the_verbs_label_names_the_label_of_a_file_with_no_tag_and_the_tag_wins`
  - `tests/test_tag_folder_copyright.py::test_the_verbs_label_outranks_the_copyright_line`

Old text:

```
    if typed:

```

New text:

```
    if False:

```

### `u240.M5_wrong_field_read`

_by_label: the label tag read where the copyright line should be

- File: `src/cratekit/tagging/tag.py`
- Source: `u240.json`, row `M5_wrong_field_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 334 against a baseline of 334
- Kills: 11 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_label_batch_with_every_catalogue_blocked_lands_tagged_by_label`
  - `tests/test_tag_folder_copyright.py::test_a_line_naming_one_label_with_no_genre_is_asked_of_the_catalogues`
  - `tests/test_tag_folder_copyright.py::test_a_line_naming_two_registered_labels_is_refused_for_that_file`
  - `tests/test_tag_folder_copyright.py::test_a_mixed_folder_with_every_catalogue_blocked_tags_each_file_by_its_line`
  - `tests/test_tag_folder_copyright.py::test_a_sweep_one_file_of_which_fails_still_reports_every_file`
  - `tests/test_tag_folder_copyright.py::test_an_unregistered_file_in_the_batch_is_left_untagged_and_its_item_fails`
  - `tests/test_tag_folder_copyright.py::test_files_whose_line_named_two_labels_are_counted_and_warned`
  - `tests/test_tag_folder_copyright.py::test_the_needles_are_frozen_with_the_genres_when_the_sweep_is_queued`
  - `tests/test_tag_folder_copyright.py::test_the_report_names_each_file_by_label_by_catalogue_or_not_at_all`
  - `tests/test_tag_folder_copyright.py::test_the_tails_tag_step_lands_a_label_batch_with_every_catalogue_blocked`
  - `tests/test_tag_folder_copyright.py::test_two_labels_sharing_a_display_name_never_lend_each_other_a_genre`

Old text:

```
        line = held["copyright"] or ""
```

New text:

```
        line = held["label"] or ""
```

### `u240.M6_named_by_lost`

tag_one: the record says nothing of how the label was named

- File: `src/cratekit/tagging/tag.py`
- Source: `u240.json`, row `M6_named_by_lost`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 334 against a baseline of 334
- Kills: 5 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_label_batch_with_every_catalogue_blocked_lands_tagged_by_label`
  - `tests/test_tag_folder_copyright.py::test_a_label_tag_naming_a_label_with_a_genre_is_named_by_the_tag`
  - `tests/test_tag_folder_copyright.py::test_a_mixed_folder_with_every_catalogue_blocked_tags_each_file_by_its_line`
  - `tests/test_tag_folder_copyright.py::test_the_report_names_each_file_by_label_by_catalogue_or_not_at_all`
  - `tests/test_tag_folder_copyright.py::test_the_verbs_label_outranks_the_copyright_line`

Old text:

```
            "label_from": tier.named_by,
```

New text:

```
            "label_from": "",
```

### `u240.M7_line_labels_dropped_from_result`

tag_one: the labels an unsettled line named never reach the result

- File: `src/cratekit/tagging/tag.py`
- Source: `u240.json`, row `M7_line_labels_dropped_from_result`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 334 against a baseline of 334
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_line_naming_one_label_with_no_genre_is_asked_of_the_catalogues`
  - `tests/test_tag_folder_copyright.py::test_a_line_naming_two_registered_labels_is_refused_for_that_file`
  - `tests/test_tag_folder_copyright.py::test_files_whose_line_named_two_labels_are_counted_and_warned`

Old text:

```
        copyright_labels=tier.copyright_labels,
```

New text:

```
        copyright_labels=(),
```

### `u240.M8_failed_files_line_dropped`

tag_one: a failed file's refusal no longer carries its line's labels

- File: `src/cratekit/tagging/tag.py`
- Source: `u240.json`, row `M8_failed_files_line_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 334 against a baseline of 334
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_sweep_one_file_of_which_fails_still_reports_every_file`

Old text:

```
        if needs_genre and tier.copyright_labels and type(exc) is CratekitError:
```

New text:

```
        if False:
```

### `u240.M9_park_flattened`

tag_one: a searcher's park on an unsettled line is rebuilt as a plain refusal

- File: `src/cratekit/tagging/tag.py`
- Source: `u240.json`, row `M9_park_flattened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 334 against a baseline of 334
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_searchers_park_reaches_the_job_as_a_park_on_a_file_its_line_could_not_settle`

Old text:

```
        if needs_genre and tier.copyright_labels and type(exc) is CratekitError:
```

New text:

```
        if needs_genre and tier.copyright_labels:
```

### `u93-recursive-analysis.D21_restamp_flag`

The restamp queue ignores the flag and always scans one level

- File: `src/cratekit/analysis/cli.py`
- Source: `u93-recursive-analysis.json`, row `D21_restamp_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 11 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_nested_appledouble_sidecar_and_a_dot_directory_are_not_items`
  - `tests/test_analysis_workers.py::test_a_nested_file_deleted_after_the_queue_refuses_that_item_only`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_freezes_the_flag_in_the_payload`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_queues_every_nested_file_once_in_sorted_order`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_resumes_after_a_kill_and_finishes_the_rest`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_runs_every_nested_item_to_done_and_writes_the_right_file`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_says_which_linked_folders_it_did_not_walk`
  - `tests/test_analysis_workers.py::test_a_restamp_driven_at_its_queue_names_a_linked_folder_once`
  - `tests/test_analysis_workers.py::test_a_tree_whose_only_folders_are_links_says_so_on_the_zero`
  - `tests/test_analysis_workers.py::test_the_resume_repeats_what_the_walk_left_out_rather_than_only_the_queue`
  - `tests/test_analysis_workers.py::test_two_nested_folders_holding_the_same_filename_are_two_items`

Old text:

```
    recursive = bool(getattr(ctx.args, "recursive", False))
    scan = discovery.scan_audio(folder, recursive=recursive)
```

New text:

```
    recursive = bool(getattr(ctx.args, "recursive", False))
    scan = discovery.scan_audio(folder, recursive=False)
```

### `u93-recursive-analysis.D22_restamp_resume_warning`

The restamp resume drops the walk's omissions, leaving them on the queue envelope only

- File: `src/cratekit/analysis/cli.py`
- Source: `u93-recursive-analysis.json`, row `D22_restamp_resume_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_restamp_driven_at_its_queue_names_a_linked_folder_once`
  - `tests/test_analysis_workers.py::test_the_resume_repeats_what_the_walk_left_out_rather_than_only_the_queue`

Old text:

```
        warnings = (*warnings, *discovery.warnings_of(job.payload))
        if job.handler_key == "analyze.restamp":
```

New text:

```
        if job.handler_key == "analyze.restamp":
```

### `u93-recursive-analysis.D24_restamp_join`

The restamp worker joins the item id with the operator instead of the checked rule

- File: `src/cratekit/analysis/cli.py`
- Source: `u93-recursive-analysis.json`, row `D24_restamp_join`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_restamp_item_that_would_leave_the_frozen_folder_is_refused`

Old text:

```
    return folder, discovery.item_path(folder, str(item.item_id))
```

New text:

```
    return folder, folder / item.item_id
```

### `u94-a.S1_floor_dropped`

analyze_calibrate: never refuse a sample below the fit floor, so --sample 3 measures three tracks and fails after the walk instead of before it

- File: `src/cratekit/analysis/cli.py`
- Source: `u94-a.json`, row `S1_floor_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_refusal_known_before_the_walk_does_not_make_the_walk`
  - `tests/test_analysis_workers.py::test_a_sample_below_the_fit_floor_is_refused_before_measuring[extra0]`
  - `tests/test_analysis_workers.py::test_a_sample_below_the_fit_floor_is_refused_before_measuring[extra1]`

Old text:

```
    if sample < MIN_CALIBRATION_TRACKS:
        return _calibrate_refusal(
```

New text:

```
    if sample < 0:
        return _calibrate_refusal(
```

### `u94-a.S2_floor_off_by_one`

analyze_calibrate: move the floor one below MIN_CALIBRATION_TRACKS, a nearby value, so a sample of nine is accepted

- File: `src/cratekit/analysis/cli.py`
- Source: `u94-a.json`, row `S2_floor_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_sample_below_the_fit_floor_is_refused_before_measuring[extra0]`
  - `tests/test_analysis_workers.py::test_a_sample_below_the_fit_floor_is_refused_before_measuring[extra1]`

Old text:

```
    if sample < MIN_CALIBRATION_TRACKS:
        return _calibrate_refusal(
```

New text:

```
    if sample < MIN_CALIBRATION_TRACKS - 1:
        return _calibrate_refusal(
```

### `u94-a.S3_partial_refusal_dropped`

analyze_calibrate: never refuse a walk known to be partial before it is made, which is R-409 itself: one genre folder fits and writes

- File: `src/cratekit/analysis/cli.py`
- Source: `u94-a.json`, row `S3_partial_refusal_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 6 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_recursive_walk_of_one_genre_is_still_one_genre`
  - `tests/test_analysis_workers.py::test_a_refusal_known_before_the_walk_does_not_make_the_walk`
  - `tests/test_analysis_workers.py::test_a_single_genre_folder_without_the_flag_writes_nothing_and_says_why`
  - `tests/test_analysis_workers.py::test_the_root_read_one_level_deep_is_partial_and_names_the_flag`
  - `tests/test_analysis_workers.py::test_the_root_with_no_loose_tracks_and_no_flag_is_told_about_the_flag`
  - `tests/test_analysis_workers.py::test_the_wrong_folder_is_said_before_the_missing_extra`

Old text:

```
    if partial is not None and not accepted:
        return _calibrate_refusal(ctx, _partial_refused(partial), summary)

```

New text:

```
    if False:
        return _calibrate_refusal(ctx, _partial_refused(partial), summary)

```

### `u94-a.S4_accept_flag_dead`

analyze_calibrate: read --accept-partial as always false, so the flag the refusal names does nothing

- File: `src/cratekit/analysis/cli.py`
- Source: `u94-a.json`, row `S4_accept_flag_dead`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 11 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_fit_after_a_hand_cut_replaces_it_and_says_so`
  - `tests/test_analysis_workers.py::test_a_fit_over_a_fitted_cut_names_the_fit_it_replaces`
  - `tests/test_analysis_workers.py::test_a_partial_fit_that_wrote_nothing_does_not_warn_about_a_calibration`
  - `tests/test_analysis_workers.py::test_a_single_cluster_is_not_cut_down_the_middle`
  - `tests/test_analysis_workers.py::test_a_walk_that_left_a_folder_out_is_not_the_library`
  - `tests/test_analysis_workers.py::test_accept_partial_writes_and_warns`
  - `tests/test_analysis_workers.py::test_calibrate_cuts_the_vocal_threshold_between_the_two_clusters`
  - `tests/test_analysis_workers.py::test_calibrate_fits_the_energy_reference_over_a_folder_and_writes_it`
  - `tests/test_analysis_workers.py::test_calibrate_over_an_empty_folder_is_a_failed_check_not_a_traceback`
  - `tests/test_analysis_workers.py::test_calibrate_over_too_few_tracks_writes_nothing_and_says_so`
  - `tests/test_analysis_workers.py::test_calibrate_without_the_extra_refuses_rather_than_fitting_over_nothing`

Old text:

```
    accepted = bool(ctx.args.accept_partial)
```

New text:

```
    accepted = False
```

### `u94-a.S5_recursive_not_required`

_partial_before_walk: treat the root read one level deep as the whole library, so only its loose files are fitted and the check says ok

- File: `src/cratekit/analysis/cli.py`
- Source: `u94-a.json`, row `S5_recursive_not_required`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_root_read_one_level_deep_is_partial_and_names_the_flag`
  - `tests/test_analysis_workers.py::test_the_root_with_no_loose_tracks_and_no_flag_is_told_about_the_flag`

Old text:

```
    if wide and recursive:
        return None
```

New text:

```
    if wide:
        return None
```

### `u94-a.S6_music_folder_not_wide`

_is_library_wide: accept the root alone, so the music folder every module places tracks under is refused as not the library

- File: `src/cratekit/analysis/cli.py`
- Source: `u94-a.json`, row `S6_music_folder_not_wide`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_music_folder_walked_recursively_is_the_library_too`

Old text:

```
    for candidate in (root, root / cfg.library.music_dir):
```

New text:

```
    for candidate in (root,):
```

### `u94-a.S7_samefile_to_spelling`

_is_library_wide: compare two spellings instead of asking the filesystem, so the root reached through a link is not the root

- File: `src/cratekit/analysis/cli.py`
- Source: `u94-a.json`, row `S7_samefile_to_spelling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_root_reached_through_a_link_is_still_the_root`

Old text:

```
            if os.path.samefile(folder, candidate):
```

New text:

```
            if str(folder) == str(candidate):
```

### `u94-a.S8_after_walk_never_asked`

analyze_calibrate: never ask what the walk left out, so a root missing a linked or unreadable genre reads ok

- File: `src/cratekit/analysis/cli.py`
- Source: `u94-a.json`, row `S8_after_walk_never_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_walk_that_left_a_folder_out_is_not_the_library`

Old text:

```
        partial = _partial_after_walk(scan)
```

New text:

```
        partial = None
```

### `u94-b.W1_after_walk_refusal_dropped`

analyze_calibrate: ask what the walk left out and fit anyway without the flag, so the omission is known and ignored

- File: `src/cratekit/analysis/cli.py`
- Source: `u94-b.json`, row `W1_after_walk_refusal_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_walk_that_left_a_folder_out_is_not_the_library`

Old text:

```
        if partial is not None and not accepted:
            return _calibrate_refusal(ctx, _partial_refused(partial), summary, omitted)
```

New text:

```
        if False:
            return _calibrate_refusal(ctx, _partial_refused(partial), summary, omitted)
```

### `u94-b.W3_accepted_reads_ok`

_partial_accepted: report an accepted partial as ok, so it reads as the library wide fit on the check row

- File: `src/cratekit/analysis/cli.py`
- Source: `u94-b.json`, row `W3_accepted_reads_ok`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_walk_that_left_a_folder_out_is_not_the_library`
  - `tests/test_analysis_workers.py::test_accept_partial_writes_and_warns`

Old text:

```
        "skipped",
        f"{what}; fitted anyway
```

New text:

```
        "ok",
        f"{what}; fitted anyway
```

### `u94-b.W4_partial_warning_dropped`

analyze_calibrate: never put calibration-partial-sample on the envelope

- File: `src/cratekit/analysis/cli.py`
- Source: `u94-b.json`, row `W4_partial_warning_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_walk_that_left_a_folder_out_is_not_the_library`
  - `tests/test_analysis_workers.py::test_accept_partial_writes_and_warns`

Old text:

```
if partial is not None and wrote else ())
```

New text:

```
if False else ())
```

### `u94-b.W5_warning_without_a_write`

analyze_calibrate: warn about what was written when neither half wrote anything

- File: `src/cratekit/analysis/cli.py`
- Source: `u94-b.json`, row `W5_warning_without_a_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_partial_fit_that_wrote_nothing_does_not_warn_about_a_calibration`

Old text:

```
if partial is not None and wrote else ())
```

New text:

```
if partial is not None else ())
```

