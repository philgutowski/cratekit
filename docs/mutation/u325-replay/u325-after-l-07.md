# Mutation table: u325-after-l-07

Measured by `scripts/mutate.py` on 2026-11-22 23:30 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 120.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:21 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 7, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u94-b.W6_outcome_energy_only` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 206 | 1 | killed |
| `u94-b.W7_omissions_dropped_from_the_fit` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 206 | 1 | killed |
| `u94-b.W8_note_forgets_the_omission` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 206 | 1 | killed |
| `u94-c.N1_stride_is_the_first_n` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 206 | 2 | killed |
| `u94-c.N2_stride_is_a_fixed_step` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 206 | 1 | killed |
| `u94-c.N3_sample_ignored` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 206 | 3 | killed |
| `u94-c.N4_vocal_half_sampled` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 206 | 1 | killed |
| `u94-c.N5_note_m_is_the_sample` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 206 | 1 | killed |
| `u94-c.N6_default_sample_halved` | `src/cratekit/analysis/cli.py` | maintainer | 2 file(s) | 206 | 1 | killed |
| `u94-c.N7_root_not_required_first` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 206 | 1 | killed |
| `u94-c.N8_absent_folder_not_told_apart` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 206 | 2 | killed |
| `r650-a.B5_artifact_drops_the_key` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 3 | killed |
| `r650-a.C1_summary_counts_nothing` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 2 | killed |
| `r650-a.C3_summary_drops_the_key` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 4 | killed |
| `r650-a.C4_warning_fires_on_a_clean_sweep` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 2 | killed |
| `r650-a.C6_warning_names_no_strings` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 2 | killed |
| `r650-a.C7_warning_order_is_the_walk_order` | `src/cratekit/tagging/cli.py` | maintainer | 1 file(s) | 102 | 1 | killed |
| `r650-a.C8_warning_code_reworded` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `r650-a.C9_warning_counts_the_wrong_total` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `r650-a.D3_unresolved_is_fed_by_declines` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u281.C2_challenge_never_named` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u281.C3_unsent_never_counted` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 2 | killed |
| `u281.C4_source_blocked_counts_unsent_as_sent` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 2 | killed |
| `u281.C5_partial_challenge_called_whole` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R19_folder_queues_no_items` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 41 | killed |
| `u56-catalogue-searcher-and-tag-workers.R20_unnamed_folder_sweeps_cwd` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R21_two_zeroes_read_as_one` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R22_vanished_file_reports_done` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R23_summary_from_the_queue` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 27 | killed |
| `u84-b.C1_artifact_carries_status` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u84-b.C2_summary_zero_filled` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 2 | killed |
| `u84-b.C3_old_reports_uncounted` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u85-a.A15_worker_hands_in_the_fetch` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 3 | killed |
| `u85-a.A16_summary_counts_art` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `r1103.H3_message_names_no_file` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 102 | 2 | killed |
| `r1103.H4_detail_path` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 102 | 2 | killed |
| `r1103.H5_detail_genre` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `r1103.H6_detail_current` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `r816-e.E1_retag_names_the_verb` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R28_worker_trusts_the_frozen_row` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R29_blank_genre_is_corrected` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R30_specific_genre_is_overwritten` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 102 | 2 | killed |
| `u56-catalogue-searcher-and-tag-workers.R31_artifact_drops_the_previous_value` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `r502-a.G5_no_adjudicate` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 213 | 7 | killed |
| `r502-a.G6_no_mount_guard` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 213 | 1 | killed |
| `r502-a2.G7_frozen_config` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 213 | 1 | killed |
| `r502-b.E2_nothing_written_refusal` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 213 | 1 | killed |
| `r502-b.G10_since_keys_swapped` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 213 | 6 | killed |
| `r502-b.G12_since_check_detail` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 213 | 1 | killed |
| `r502-b.G9_missing_count_stale` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 213 | 3 | killed |
| `r502-b2.G13_written_line_for_gained` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 213 | 1 | killed |
| `r503-a.G10_owned_key` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 213 | 109 | killed |
| `r503-a.G1_no_lookup` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 213 | 7 | killed |
| `r503-a.G2_found_is_answered` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 213 | 1 | killed |
| `r503-a.G4_offered_not_decremented` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 213 | 5 | killed |
| `r503-a.G5_state_not_counted` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 213 | 3 | killed |
| `r503-a.G6_answered_not_counted` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 213 | 5 | killed |
| `r503-a.G7_answered_read_as_since` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 213 | 5 | killed |
| `r503-a.G8_rejected_not_kept` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 213 | 4 | killed |
| `r503-a.G9_answered_last` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 213 | 2 | killed |
| `r503-b.E2_offered_listed` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 213 | 1 | killed |
| `r503-b.G11_summary` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 213 | 5 | killed |
| `r503-b.G12_answered_check` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 213 | 2 | killed |
| `r503-b.G13_offered_check` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 213 | 1 | killed |
| `r503-b.G14_no_gone` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 213 | 2 | killed |
| `r503-b.G15_no_new` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 213 | 1 | killed |
| `r503-b.G16_json_uncaught` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 213 | 2 | killed |
| `r503-b.G17_no_hint` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 213 | 3 | killed |
| `r356-a.A10_provider_title_read_one_way_only` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 111 | 1 | killed |
| `r356-a.A11_row_title_read_one_way_only` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 111 | 1 | killed |
| `r356-a.A12_reason_outlives_its_match` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 111 | 1 | killed |
| `r356-a.A13_reason_never_stored` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 0 | collection error | collect-error |
| `r356-a.A14_no_joiner_words` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 111 | 1 | killed |
| `r356-a.A1_first_agreeing_rather_than_the_only_one` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 111 | 27 | killed |
| `r356-a.A2_unreadable_track_no_longer_stops_rule_one` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 111 | 2 | killed |
| `r356-a.A3_any_hearted_rather_than_the_only_hearted` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 111 | 4 | killed |
| `r356-a.A4_hearts_asked_of_every_track` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 111 | 1 | killed |
| `r356-a.A5_withdrawn_track_is_a_candidate` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 111 | 2 | killed |
| `r356-a.A7_artist_not_compared` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 111 | 2 | killed |
| `r356-a.A8_first_billed_artist_not_required` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 111 | 1 | killed |
| `r356-a.A9_row_may_name_an_artist_nobody_bills` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 111 | 1 | killed |
| `r358-round-2.A3_editor_check` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 111 | 1 | killed |
| `r358-round-2.A5_absent_answer` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 111 | 1 | killed |
| `r358-round-2.A7_empty_title_message` | `src/cratekit/modules/outbound/tidal_account.py` | maintainer | 1 file(s) | 111 | 3 | killed |
| `r358.A1_empty_title_refusal` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 111 | 3 | killed |
| `r358.A2_title_stripped_for_the_write` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 111 | 1 | killed |
| `r358.A4_false_answer` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 111 | 1 | killed |
| `r358.A6_retry_coefficient` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 111 | 1 | killed |
| `r572.A1_album_rule_gone` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 0 | collection error | collect-error |
| `r572.A2_first_named` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 111 | 1 | killed |
| `r572.A3_album_over_two_hearts` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 0 | collection error | collect-error |
| `r572.A4_no_fold` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 111 | 3 | killed |
| `r572.A5_album_among_all` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 111 | 1 | killed |
| `r572.A6_album_despite_unreadable` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 0 | collection error | collect-error |
| `r834.M1_a_create_makes_the_playlist_private` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 111 | 5 | killed |
| `r834.M3_a_refused_private_step_does_not_lose_the_playlist` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 111 | 2 | killed |
| `r834.M5_a_create_is_never_retried` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 111 | 1 | killed |
| `u97-c.C1_outbound_refusal_removed` | `src/cratekit/modules/outbound/account.py` | user | 1 file(s) | 111 | 1 | killed |
| `r679-b.C1_credited_rule_not_owning` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 879 | 2 | killed |
| `r679-b.C2_reading_shape_missing` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 879 | 1 | killed |
| `r679-b.D2_fallback_gate_on_question_alone` | `src/cratekit/acquire/fallback_cli.py` | user | 3 file(s) | 879 | 1 | killed |
| `r679-b.B1_no_retirement` | `src/cratekit/acquire/match_cli.py` | user | 3 file(s) | 879 | 7 | killed |
| `r679-b.B2_any_matched_row_is_owned_by_a_rule` | `src/cratekit/acquire/match_cli.py` | user | 3 file(s) | 879 | 1 | killed |
| `r679-b.B3_no_reopen` | `src/cratekit/acquire/match_cli.py` | user | 3 file(s) | 879 | 1 | killed |
| `r679-b.B5_rule_not_recorded` | `src/cratekit/acquire/match_cli.py` | user | 3 file(s) | 879 | 5 | killed |
| `r679-b.B6_one_shape_only` | `src/cratekit/acquire/match_cli.py` | user | 3 file(s) | 879 | 7 | killed |
| `r679-b.D5_missing_per_row_gate_on_question_alone` | `src/cratekit/intake/missing_cli.py` | user | 3 file(s) | 879 | 1 | killed |
| `r679-b.D1_intake_gate_on_question_alone` | `src/cratekit/intake/cli.py` | user | 3 file(s) | 879 | 2 | killed |
| `r431-b.B10_an_older_payload_reads_as_solo` | `src/cratekit/intake/cli.py` | user | 9 file(s) | 682 | 1 | killed |
| `r431-b.B9_the_freeze_drops_the_field` | `src/cratekit/intake/cli.py` | user | 9 file(s) | 682 | 3 | killed |
| `r504-b.B1_verb_drops_short` | `src/cratekit/intake/cli.py` | user | 9 file(s) | 682 | 4 | killed |
| `u144-c.C8_question_named` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 39 | 1 | killed |

## Row definitions

### `u94-b.W6_outcome_energy_only`

analyze_calibrate: derive the outcome from the energy half alone, so a run that replaced only the vocal cut answers no_op

- File: `src/cratekit/analysis/cli.py`
- Source: `u94-b.json`, row `W6_outcome_energy_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_run_where_only_the_vocal_half_wrote_does_not_answer_no_op`

Old text:

```
        outcome=Outcome.OK if wrote else Outcome.NO_OP,
```

New text:

```
        outcome=Outcome.OK if calibrated else Outcome.NO_OP,
```

### `u94-b.W7_omissions_dropped_from_the_fit`

analyze_calibrate: leave the walk's omissions off the envelope of a fit that went ahead

- File: `src/cratekit/analysis/cli.py`
- Source: `u94-b.json`, row `W7_omissions_dropped_from_the_fit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_walk_that_left_a_folder_out_is_not_the_library`

Old text:

```
        + tuple(omitted),
```

New text:

```
        + tuple(()),
```

### `u94-b.W8_note_forgets_the_omission`

fitted_note: never record how many folders were not walked, so the file a later restamp trusts reads as a whole fit

- File: `src/cratekit/analysis/cli.py`
- Source: `u94-b.json`, row `W8_note_forgets_the_omission`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_walk_that_left_a_folder_out_is_not_the_library`

Old text:

```
    if left_out:
        note +=
```

New text:

```
    if False:
        note +=
```

### `u94-c.N1_stride_is_the_first_n`

stride_sample: take the first N of the sorted walk, which is the first few folders of the alphabet

- File: `src/cratekit/analysis/cli.py`
- Source: `u94-c.json`, row `N1_stride_is_the_first_n`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_same_tree_gives_the_same_sample_twice`
  - `tests/test_analysis_workers.py::test_the_stride_sample_is_even_ordered_and_reaches_the_tail`

Old text:

```
    return [items[index * total // count] for index in range(count)]
```

New text:

```
    return list(items[:count])
```

### `u94-c.N2_stride_is_a_fixed_step`

stride_sample: a fixed step of len // count, which stops short of the tail whenever the division has a remainder

- File: `src/cratekit/analysis/cli.py`
- Source: `u94-c.json`, row `N2_stride_is_a_fixed_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_stride_sample_is_even_ordered_and_reaches_the_tail`

Old text:

```
    return [items[index * total // count] for index in range(count)]
```

New text:

```
    return [items[index * (total // count)] for index in range(count)]
```

### `u94-c.N3_sample_ignored`

analyze_calibrate: measure every walked track whatever --sample says, the unbounded run the brief rules out

- File: `src/cratekit/analysis/cli.py`
- Source: `u94-c.json`, row `N3_sample_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_sample_at_the_fit_floor_is_accepted`
  - `tests/test_analysis_workers.py::test_the_same_tree_gives_the_same_sample_twice`
  - `tests/test_analysis_workers.py::test_the_vocal_cut_reads_every_tagged_file_while_energy_reads_the_sample`

Old text:

```
    sampled = stride_sample(paths, sample)
```

New text:

```
    sampled = list(paths)
```

### `u94-c.N4_vocal_half_sampled`

analyze_calibrate: hand the vocal half the sample instead of every file under the walk

- File: `src/cratekit/analysis/cli.py`
- Source: `u94-c.json`, row `N4_vocal_half_sampled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_vocal_cut_reads_every_tagged_file_while_energy_reads_the_sample`

Old text:

```
        _calibrate_vocals(cfg, folder, paths, left_out),
```

New text:

```
        _calibrate_vocals(cfg, folder, sampled, left_out),
```

### `u94-c.N5_note_m_is_the_sample`

analyze_calibrate: record the sample size as M, so the note reads N of N and hides how much of the library was fitted

- File: `src/cratekit/analysis/cli.py`
- Source: `u94-c.json`, row `N5_note_m_is_the_sample`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_same_tree_gives_the_same_sample_twice`

Old text:

```
        _calibrate_energy(cfg, folder, sampled, len(paths), left_out),
```

New text:

```
        _calibrate_energy(cfg, folder, sampled, len(sampled), left_out),
```

### `u94-c.N6_default_sample_halved`

DEFAULT_CALIBRATION_SAMPLE: halve the coefficient, 500 to 250

- File: `src/cratekit/analysis/cli.py`
- Source: `u94-c.json`, row `N6_default_sample_halved`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_default_sample_is_what_the_parser_hands_the_verb`

Old text:

```
DEFAULT_CALIBRATION_SAMPLE = 500
```

New text:

```
DEFAULT_CALIBRATION_SAMPLE = 250
```

### `u94-c.N7_root_not_required_first`

analyze_calibrate: ask the folder's standing with the library away, so an unmounted volume is blamed on the folder

- File: `src/cratekit/analysis/cli.py`
- Source: `u94-c.json`, row `N7_root_not_required_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_calibrate_refuses_with_the_library_away_rather_than_writing_beside_the_mount`

Old text:

```
    _require_library_root(cfg)
    partial = _partial_before_walk
```

New text:

```
    partial = _partial_before_walk
```

### `u94-c.N8_absent_folder_not_told_apart`

analyze_calibrate: drop the not a folder answer, so a mistyped path is told it is not the library root

- File: `src/cratekit/analysis/cli.py`
- Source: `u94-c.json`, row `N8_absent_folder_not_told_apart`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_folder_that_is_not_there_is_a_different_zero_from_an_empty_one`
  - `tests/test_analysis_workers.py::test_calibrate_over_a_folder_that_is_not_there_says_that_and_not_empty`

Old text:

```
    if not folder.is_dir():
        return _calibrate_refusal(
```

New text:

```
    if False:
        return _calibrate_refusal(
```

### `r650-a.B5_artifact_drops_the_key`

The committed item report stops carrying the flag, so the summary reads it back as absent

- File: `src/cratekit/tagging/cli.py`
- Source: `r650-a.json`, row `B5_artifact_drops_the_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_published_genre_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`
  - `tests/test_tag_workers.py::test_the_sweep_names_a_folders_own_name_with_its_one_answer_and_falls_back_when_the_copy_breaks`

Old text:

```
            "off_taxonomy": result.off_taxonomy,
```

New text:

```
(empty)
```

### `r650-a.C1_summary_counts_nothing`

The report stops counting the strings, leaving the map empty on a folder that has them

- File: `src/cratekit/tagging/cli.py`
- Source: `r650-a.json`, row `C1_summary_counts_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`
  - `tests/test_tag_workers.py::test_the_sweep_names_a_folders_own_name_with_its_one_answer_and_falls_back_when_the_copy_breaks`

Old text:

```
            if report.get("off_taxonomy") and source_genre:
                off_taxonomy[source_genre] = off_taxonomy.get(source_genre, 0) + 1
```

New text:

```
(empty)
```

### `r650-a.C3_summary_drops_the_key`

The payload stops carrying the map at all

- File: `src/cratekit/tagging/cli.py`
- Source: `r650-a.json`, row `C3_summary_drops_the_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_published_word_with_no_folder_is_listed_as_unresolved`
  - `tests/test_tag_workers.py::test_a_sweep_with_nothing_off_taxonomy_carries_no_such_warning`
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`
  - `tests/test_tag_workers.py::test_the_sweep_names_a_folders_own_name_with_its_one_answer_and_falls_back_when_the_copy_breaks`

Old text:

```
        "off_taxonomy": off_taxonomy,
```

New text:

```
(empty)
```

### `r650-a.C4_warning_fires_on_a_clean_sweep`

The empty check goes, so an ordinary folder is warned about a gap it does not have

- File: `src/cratekit/tagging/cli.py`
- Source: `r650-a.json`, row `C4_warning_fires_on_a_clean_sweep`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_published_genre_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_a_sweep_with_nothing_off_taxonomy_carries_no_such_warning`

Old text:

```
    if not counted:
        return ()
```

New text:

```
(empty)
```

### `r650-a.C6_warning_names_no_strings`

The warning says a gap exists and not which word, which is the R24 mistake one verb over

- File: `src/cratekit/tagging/cli.py`
- Source: `r650-a.json`, row `C6_warning_names_no_strings`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`
  - `tests/test_tag_workers.py::test_the_sweep_names_a_folders_own_name_with_its_one_answer_and_falls_back_when_the_copy_breaks`

Old text:

```
                f"these catalogue answers: {words}. Each word was written onto "
```

New text:

```
                f"these catalogue answers. Each word was written onto "
```

### `r650-a.C7_warning_order_is_the_walk_order`

The strings are listed in commit order, so two runs over one folder disagree

- File: `src/cratekit/tagging/cli.py`
- Source: `r650-a.json`, row `C7_warning_order_is_the_walk_order`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`

Old text:

```
    words = ", ".join(sorted(counted))
```

New text:

```
    words = ", ".join(counted)
```

### `r650-a.C8_warning_code_reworded`

The code a log filter reads is reworded, never appended to

- File: `src/cratekit/tagging/cli.py`
- Source: `r650-a.json`, row `C8_warning_code_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`

Old text:

```
OFF_TAXONOMY = "tag-folder-off-taxonomy"
```

New text:

```
OFF_TAXONOMY = "tag-folder-unknown-word"
```

### `r650-a.C9_warning_counts_the_wrong_total`

The warning names the file count as the sweep's whole tagged total

- File: `src/cratekit/tagging/cli.py`
- Source: `r650-a.json`, row `C9_warning_counts_the_wrong_total`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`

Old text:

```
    files = sum(counted.values())
```

New text:

```
    files = summary.get("tagged", 0)
```

### `r650-a.D3_unresolved_is_fed_by_declines`

Existing: the unresolved map is filled from unmapped-genre and from nothing else

- File: `src/cratekit/tagging/cli.py`
- Source: `r650-a.json`, row `D3_unresolved_is_fed_by_declines`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`

Old text:

```
        if reason == tag_engine.UNMAPPED_GENRE and source_genre:
```

New text:

```
        if source_genre:
```

### `u281.C2_challenge_never_named`

_summary: never count a Cloudflare challenge, so the warning cannot name one

- File: `src/cratekit/tagging/cli.py`
- Source: `u281.json`, row `C2_challenge_never_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`

Old text:

```
                if searchers.CLOUDFLARE_CHALLENGE in note:
                    challenged[source] += 1
```

New text:

```
                if False:
                    challenged[source] += 1
```

### `u281.C3_unsent_never_counted`

_summary: never count a file a catalogue was not sent

- File: `src/cratekit/tagging/cli.py`
- Source: `u281.json`, row `C3_unsent_never_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`

Old text:

```
                if note.startswith(searchers.NOT_SENT):
                    not_sent[source] += 1
```

New text:

```
                if False:
                    not_sent[source] += 1
```

### `u281.C4_source_blocked_counts_unsent_as_sent`

_unread_warnings: count the unsent files among the searches sent, so the warning claims searches never made

- File: `src/cratekit/tagging/cli.py`
- Source: `u281.json`, row `C4_source_blocked_counts_unsent_as_sent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`

Old text:

```
        sent = asked - held
```

New text:

```
        sent = asked
```

### `u281.C5_partial_challenge_called_whole`

_unread_phrase: call every refusal a challenge when any one was

- File: `src/cratekit/tagging/cli.py`
- Source: `u281.json`, row `C5_partial_challenge_called_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_sweep_some_of_whose_refusals_were_a_challenge_says_how_many`

Old text:

```
    if challenged >= count:
```

New text:

```
    if challenged:
```

### `u56-catalogue-searcher-and-tag-workers.R19_folder_queues_no_items`

The zero item rule broken at its source: a job with nothing to claim drives straight to SUCCEEDED over a folder nothing walked

- File: `src/cratekit/tagging/cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R19_folder_queues_no_items`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 41 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning`
  - `tests/test_tag_workers.py::test_a_file_in_a_subfolder_keeps_its_relative_identifier_and_is_still_tagged`
  - `tests/test_tag_workers.py::test_a_file_removed_between_the_queueing_and_the_drive_is_refused_by_name`
  - `tests/test_tag_workers.py::test_a_folder_of_three_tags_the_two_with_no_genre_and_leaves_the_third`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_some_files_says_how_many_of_how_many`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`
  - `tests/test_tag_workers.py::test_a_published_genre_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_a_published_word_with_no_folder_is_listed_as_unresolved`
  - `tests/test_tag_workers.py::test_a_real_track_beside_the_staging_tree_is_still_queued`
  - `tests/test_tag_workers.py::test_a_resumed_run_asks_a_refusing_beatport_again_from_its_first_file`
  - `tests/test_tag_workers.py::test_a_retried_job_drives_only_the_item_that_failed`
  - `tests/test_tag_workers.py::test_a_searcher_that_raises_part_way_fails_only_its_own_item`
  - ... and 26 more, see the JSON sidecar

Old text:

```
            item_ids=tuple(str(path.relative_to(folder)) for path in files),
```

New text:

```
            item_ids=(),
```

### `u56-catalogue-searcher-and-tag-workers.R20_unnamed_folder_sweeps_cwd`

Path("") is the current directory, so an unnamed folder writes genres into whatever the person is standing in

- File: `src/cratekit/tagging/cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R20_unnamed_folder_sweeps_cwd`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_an_empty_folder_argument_never_sweeps_the_working_directory`

Old text:

```
    named = str(ctx.args.folder or "")
    if not named.strip():
```

New text:

```
    named = str(ctx.args.folder or "")
    if False:
```

### `u56-catalogue-searcher-and-tag-workers.R21_two_zeroes_read_as_one`

A mistyped path reports as a folder with nothing to tag, which is the answer most likely to stop somebody looking

- File: `src/cratekit/tagging/cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R21_two_zeroes_read_as_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_folder_that_is_not_there_is_a_different_zero_from_an_empty_one`

Old text:

```
            if folder.is_dir()
            else _empty(
                "tag-folder-absent",
```

New text:

```
            if True
            else _empty(
                "tag-folder-absent",
```

### `u56-catalogue-searcher-and-tag-workers.R22_vanished_file_reports_done`

An item whose file is gone reports done having tagged nothing, which is the clean report over unreadable state the merge bar names

- File: `src/cratekit/tagging/cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R22_vanished_file_reports_done`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_file_removed_between_the_queueing_and_the_drive_is_refused_by_name`

Old text:

```
    path = folder / item.item_id
    if not path.is_file():
```

New text:

```
    path = folder / item.item_id
    if False:
```

### `u56-catalogue-searcher-and-tag-workers.R23_summary_from_the_queue`

The report counts what was queued rather than what ran, so a half finished sweep reports every file as handled

- File: `src/cratekit/tagging/cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R23_summary_from_the_queue`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 27 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_some_files_says_how_many_of_how_many`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`
  - `tests/test_tag_workers.py::test_a_published_genre_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_a_published_word_with_no_folder_is_listed_as_unresolved`
  - `tests/test_tag_workers.py::test_a_report_from_before_the_repair_is_counted_under_no_status`
  - `tests/test_tag_workers.py::test_a_sweep_beatport_matched_whole_names_no_fallback_as_blocked`
  - `tests/test_tag_workers.py::test_a_sweep_discogs_decides_asks_beatport_only_for_missing_covers_and_counts_discogs_first`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_a_sweep_with_no_discogs_token_says_so_and_reads_no_file_as_no_hit`
  - `tests/test_tag_workers.py::test_a_token_discogs_refuses_is_warned_about_even_when_beatport_settles_every_file`
  - `tests/test_tag_workers.py::test_an_outage_keeps_its_own_word_in_the_sweeps_warning`
  - ... and 12 more, see the JSON sidecar

Old text:

```
    for report in artifacts.committed(cfg, job_id):
        reason = str(report.get("skipped") or "")
        source_genre = str(report.get("source_genre") or "")
```

New text:

```
    for report in []:
        reason = str(report.get("skipped") or "")
        source_genre = str(report.get("source_genre") or "")
```

### `u84-b.C1_artifact_carries_status`

The item artifact drops the repair status, so nothing on disk records what the repair did

- File: `src/cratekit/tagging/cli.py`
- Source: `u84-b.json`, row `C1_artifact_carries_status`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_art_repair_reaches_the_artifact_and_the_summary_counts_every_status`

Old text:

```
            "art_repair": result.art_repair,

```

New text:

```
(empty)
```

### `u84-b.C2_summary_zero_filled`

The summary lists only the statuses it saw, so none repaired and not counted read the same

- File: `src/cratekit/tagging/cli.py`
- Source: `u84-b.json`, row `C2_summary_zero_filled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_report_from_before_the_repair_is_counted_under_no_status`
  - `tests/test_tag_workers.py::test_the_art_repair_reaches_the_artifact_and_the_summary_counts_every_status`

Old text:

```
        "art_repair": art_repair,
```

New text:

```
        "art_repair": {key: value for key, value in art_repair.items() if value},
```

### `u84-b.C3_old_reports_uncounted`

A report committed before the repair existed is counted as ok, a status nobody measured

- File: `src/cratekit/tagging/cli.py`
- Source: `u84-b.json`, row `C3_old_reports_uncounted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_report_from_before_the_repair_is_counted_under_no_status`

Old text:

```
        status = str(report.get("art_repair") or "")
```

New text:

```
        status = str(report.get("art_repair") or art.REPAIR_OK)
```

### `u85-a.A15_worker_hands_in_the_fetch`

The worker passes no image fetch, so the verb never embeds art

- File: `src/cratekit/tagging/cli.py`
- Source: `u85-a.json`, row `A15_worker_hands_in_the_fetch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_sweep_discogs_decides_asks_beatport_only_for_missing_covers_and_counts_discogs_first`
  - `tests/test_tag_workers.py::test_an_albums_cover_is_asked_for_and_encoded_once_across_the_queued_sweep`
  - `tests/test_tag_workers.py::test_new_art_reaches_the_file_the_artifact_and_the_summary`

Old text:

```
        fetch_image=searchers.for_images(),

```

New text:

```
(empty)
```

### `u85-a.A16_summary_counts_art`

The job summary never counts an art status

- File: `src/cratekit/tagging/cli.py`
- Source: `u85-a.json`, row `A16_summary_counts_art`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_new_art_reaches_the_file_the_artifact_and_the_summary`

Old text:

```
            art_fetch[fetched] += 1
```

New text:

```
            pass
```

### `r1103.H3_message_names_no_file`

handle: reword the refusal so it names no file

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r1103.json`, row `H3_message_names_no_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_is_named_in_the_human_answer`

Old text:

```
            f"{path} would not take the genre {result.proposed!r}, so it still "
```

New text:

```
            f"the file would not take the genre {result.proposed!r}, so it still "
```

### `r1103.H4_detail_path`

handle: the refusal's detail loses the file's path

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r1103.json`, row `H4_detail_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`
  - `tests/test_tag_workers.py::test_a_retag_whose_only_file_will_not_take_its_genre_names_no_reload`

Old text:

```
                "path": str(path),
```

New text:

```
                "path": "",
```

### `r1103.H5_detail_genre`

handle: the refusal's detail names the genre the file still carries as the one it would not take

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r1103.json`, row `H5_detail_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`

Old text:

```
                "genre": result.proposed,
```

New text:

```
                "genre": result.current,
```

### `r1103.H6_detail_current`

handle: the refusal's detail loses the genre the file still carries

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r1103.json`, row `H6_detail_current`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`

Old text:

```
                "current": result.current,
```

New text:

```
                "current": "",
```

### `r816-e.E1_retag_names_the_verb`

library_row_warning: name no verb, reworded

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r816-e.json`, row `E1_retag_names_the_verb`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_corrected_retag_ends_by_naming_the_reload_the_stale_row_needs`

Old text:

```
because this verb writes the file half only; run `crate tag "
            f"rows` so the rows catch up
```

New text:

```
because this verb writes the file half only; run the row "
            f"verb so the rows catch up
```

### `u56-catalogue-searcher-and-tag-workers.R28_worker_trusts_the_frozen_row`

The genre is not re-read at drive time, so a file somebody corrected by hand between the confirmation and the drive is corrected again

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R28_worker_trusts_the_frozen_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_genre_made_blank_between_the_confirm_and_the_drive_is_left_to_its_owner`

Old text:

```
    current = tags.read_genre_from_file(path) or ""
    if not current:
```

New text:

```
    current = tags.read_genre_from_file(path) or ""
    if False:
```

### `u56-catalogue-searcher-and-tag-workers.R29_blank_genre_is_corrected`

The retag writes into a field tag.folder owns under fill if empty, which is one field under two policies

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R29_blank_genre_is_corrected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_genre_made_blank_between_the_confirm_and_the_drive_is_left_to_its_owner`

Old text:

```
    if not current:
        result = retag.RetagResult(path=path, current=current, reason=retag.NO_GENRE)
```

New text:

```
    if current == "\\u0000":
        result = retag.RetagResult(path=path, current=current, reason=retag.NO_GENRE)
```

### `u56-catalogue-searcher-and-tag-workers.R30_specific_genre_is_overwritten`

A queued job overwrites somebody's own curation, which is the write this verb exists to avoid making

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R30_specific_genre_is_overwritten`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_genre_made_specific_between_the_confirm_and_the_drive_is_not_rewritten`
  - `tests/test_tag_workers.py::test_the_report_is_derived_from_what_ran_rather_than_from_what_was_planned`

Old text:

```
    elif not declared.is_too_coarse_as_source(current):
```

New text:

```
    elif False:
```

### `u56-catalogue-searcher-and-tag-workers.R31_artifact_drops_the_previous_value`

R-185's only record: without the previous genre the artifacts stop naming which library rows went stale, so the deferred database half has no population to read

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R31_artifact_drops_the_previous_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_an_interrupted_retag_leaves_a_library_row_stale_and_the_artifact_recovers_it`

Old text:

```
            "current": result.current,
            "written": result.written,
```

New text:

```
            "written": result.written,
```

### `r502-a.G5_no_adjudicate`

Skip reading a person's answer back, so a row answered as another track reads as a fresh question and drops out

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r502-a.json`, row `G5_no_adjudicate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 213 against a baseline of 213
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_rejected_row_under_a_tombstone_is_suppressed_not_listed`
  - `tests/test_intake_missing.py::test_a_rejection_after_a_listing_refuses_over_the_earlier_list_and_says_why`
  - `tests/test_intake_missing.py::test_a_row_a_person_answered_as_another_track_stays_listed`
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`
  - `tests/test_intake_missing.py::test_the_refusal_names_what_the_earlier_list_holds_not_what_the_job_found`

Old text:

```
    if asked:
        with review.open_store(cfg) as items:
            for handler_key, at in asked.items():
```

New text:

```
    if False:
        with review.open_store(cfg) as items:
            for handler_key, at in asked.items():
```

### `r502-a.G6_no_mount_guard`

Drop the absent music folder refusal before the library walk

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r502-a.json`, row `G6_no_mount_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 213 against a baseline of 213
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_an_unmounted_library_refuses_rather_than_reading_every_row_missing`

Old text:

```
    if not music.is_dir():
        raise refuse(
            "library-volume-unmounted",
            f"this library's music folder {str(music)!r} is not there, so no track "
```

New text:

```
    if False:
        raise refuse(
            "library-volume-unmounted",
            f"this library's music folder {str(music)!r} is not there, so no track "
```

### `r502-a2.G7_frozen_config`

Ask the library at the root the first job froze rather than the current configuration (the review's finding)

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r502-a2.json`, row `G7_frozen_config`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 213 against a baseline of 213
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_the_library_is_asked_where_it_is_now_not_where_the_job_froze_it`

Old text:

```
    cfg = intake_cli._load()
    music = Path(cfg.library.root) / cfg.library.music_dir
```

New text:

```
    cfg = jobs.frozen_config(origins[0])
    music = Path(cfg.library.root) / cfg.library.music_dir
```

### `r502-b.E2_nothing_written_refusal`

Existing guard sample: drop the refusal for missing tracks none of which could be written

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r502-b.json`, row `E2_nothing_written_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 213 against a baseline of 213
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_missing_tracks_none_named_and_none_writable_refuse_rather_than_no_op`

Old text:

```
    if missing and not listed and not in_file:
```

New text:

```
    if False:
```

### `r502-b.G10_since_keys_swapped`

Count a row held since under suppressed_since and a row deleted since under owned_since

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r502-b.json`, row `G10_since_keys_swapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 213 against a baseline of 213
- Kills: 6 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_row_tombstoned_since_the_job_is_not_listed_and_counted_suppressed`
  - `tests/test_intake_missing.py::test_a_run_asks_each_missing_row_again_as_a_job_does`
  - `tests/test_intake_missing.py::test_a_run_whose_rows_were_all_acquired_since_names_no_download`
  - `tests/test_intake_missing.py::test_one_row_acquired_since_leaves_the_other_listed`
  - `tests/test_intake_missing.py::test_rows_acquired_since_the_job_are_not_listed_and_name_no_download`
  - `tests/test_intake_missing.py::test_the_library_is_asked_where_it_is_now_not_where_the_job_froze_it`

Old text:

```
    match.MatchState.MATCHED: "owned_since",
    match.MatchState.SUPPRESSED: "suppressed_since",
```

New text:

```
    match.MatchState.MATCHED: "suppressed_since",
    match.MatchState.SUPPRESSED: "owned_since",
```

### `r502-b.G12_since_check_detail`

Reword the since check so it no longer names the rows in the library since

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r502-b.json`, row `G12_since_check_detail`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 213 against a baseline of 213
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_rows_acquired_since_the_job_are_not_listed_and_name_no_download`

Old text:

```
            f"{since['owned_since']} in the library since, {since['suppressed_since']} "
```

New text:

```
            f"{since['owned_since']} held now, {since['suppressed_since']} "
```

### `r502-b.G9_missing_count_stale`

Report the job's missing count rather than the count still missing now

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r502-b.json`, row `G9_missing_count_stale`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 213 against a baseline of 213
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_asks_each_missing_row_again_as_a_job_does`
  - `tests/test_intake_missing.py::test_one_row_acquired_since_leaves_the_other_listed`
  - `tests/test_intake_missing.py::test_rows_acquired_since_the_job_are_not_listed_and_name_no_download`

Old text:

```
        counts["missing"] = len(missing)

```

New text:

```
(empty)
```

### `r502-b2.G13_written_line_for_gained`

Drop the written line's gained branch, so a job whose rows were all gained reads as a job with nothing missing

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r502-b2.json`, row `G13_written_line_for_gained`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 213 against a baseline of 213
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_rows_acquired_since_the_job_are_not_listed_and_name_no_download`

Old text:

```
    elif gained:
        said = (
```

New text:

```
    elif False:
        said = (
```

### `r503-a.G10_owned_key`

File an answered row now owned under answered_missing

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-a.json`, row `G10_owned_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 213 against a baseline of 213
- Kills: 109 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_deleted_credited_row_never_withholds_another_remix_of_the_recording`
  - `tests/test_intake_missing.py::test_a_deleted_track_whose_row_kept_a_credit_is_suppressed_and_not_listed`
  - `tests/test_intake_missing.py::test_a_job_of_another_verb_in_the_same_run_is_not_listed`
  - `tests/test_intake_missing.py::test_a_job_queued_by_hand_is_not_part_of_any_run`
  - `tests/test_intake_missing.py::test_a_job_with_nothing_missing_does_not_need_the_library`
  - `tests/test_intake_missing.py::test_a_job_with_nothing_missing_is_no_op_and_writes_nothing`
  - `tests/test_intake_missing.py::test_a_missing_row_from_no_provider_is_reported_unlisted_as_a_failing_check`
  - `tests/test_intake_missing.py::test_a_mixed_job_writes_only_the_missing_rows`
  - `tests/test_intake_missing.py::test_a_rejected_row_under_a_tombstone_is_suppressed_not_listed`
  - `tests/test_intake_missing.py::test_a_rejection_after_a_listing_refuses_over_the_earlier_list_and_says_why`
  - `tests/test_intake_missing.py::test_a_row_a_person_answered_as_another_track_stays_listed`
  - `tests/test_intake_missing.py::test_a_row_held_in_another_version_since_is_offered_not_listed`
  - `tests/test_intake_missing.py::test_a_row_tombstoned_since_the_job_is_not_listed_and_counted_suppressed`
  - `tests/test_intake_missing.py::test_a_run_asks_each_missing_row_again_as_a_job_does`
  - `tests/test_intake_missing.py::test_a_run_list_is_one_file_a_second_listing_reproduces`
  - ... and 94 more, see the JSON sidecar

Old text:

```
    match.MatchState.MATCHED: "answered_owned",
```

New text:

```
    match.MatchState.MATCHED: "answered_missing",
```

### `r503-a.G1_no_lookup`

Read no answer at all, so every offered row stays offered whatever a person said (R-503 as filed)

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-a.json`, row `G1_no_lookup`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 213 against a baseline of 213
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_rejected_row_under_a_tombstone_is_suppressed_not_listed`
  - `tests/test_intake_missing.py::test_a_rejection_after_a_listing_refuses_over_the_earlier_list_and_says_why`
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_a_yes_about_a_copy_that_is_gone_stays_a_question`
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`
  - `tests/test_intake_missing.py::test_the_refusal_names_what_the_earlier_list_holds_not_what_the_job_found`

Old text:

```
    answered = iter(_answered(offered))
```

New text:

```
    answered = iter([False] * len(offered))
```

### `r503-a.G2_found_is_answered`

Treat an item that exists as answered, so an unanswered row is asked again and offered again from the listing

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-a.json`, row `G2_found_is_answered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 213 against a baseline of 213
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_an_offered_row_nobody_answered_is_unchanged_and_asks_nothing`

Old text:

```
            said.append(held is not None and held.resolved)
```

New text:

```
            said.append(held is not None)
```

### `r503-a.G4_offered_not_decremented`

Leave an answered row in the offered count, so a rejected row still reads offered 1

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-a.json`, row `G4_offered_not_decremented`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 213 against a baseline of 213
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_rejected_row_under_a_tombstone_is_suppressed_not_listed`
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_a_yes_about_a_copy_that_is_gone_stays_a_question`
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
                counts["offered"] -= 1

```

New text:

```
(empty)
```

### `r503-a.G5_state_not_counted`

Do not count an answered row under the word it resolved to, so an accepted row is not owned

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-a.json`, row `G5_state_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 213 against a baseline of 213
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_rejected_row_under_a_tombstone_is_suppressed_not_listed`
  - `tests/test_intake_missing.py::test_a_yes_about_a_copy_that_is_gone_stays_a_question`
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`

Old text:

```
                counts[_WORD[one.state]] += 1

```

New text:

```
(empty)
```

### `r503-a.G6_answered_not_counted`

Do not count answered rows under answered_*

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-a.json`, row `G6_answered_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 213 against a baseline of 213
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_rejected_row_under_a_tombstone_is_suppressed_not_listed`
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_a_yes_about_a_copy_that_is_gone_stays_a_question`
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
                now_answered[_ANSWERED[one.state]] += 1

```

New text:

```
(empty)
```

### `r503-a.G7_answered_read_as_since`

Count an answered row as a missing row would be counted, under since, rather than as answered

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-a.json`, row `G7_answered_read_as_since`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 213 against a baseline of 213
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_rejected_row_under_a_tombstone_is_suppressed_not_listed`
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_a_yes_about_a_copy_that_is_gone_stays_a_question`
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
            if report["state"] == "offered":
                # COUNTED
```

New text:

```
            if report["state"] == "never":
                # COUNTED
```

### `r503-a.G8_rejected_not_kept`

Keep only rows the job found missing, so a rejected row is counted and never listed

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-a.json`, row `G8_rejected_not_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 213 against a baseline of 213
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_rejection_after_a_listing_refuses_over_the_earlier_list_and_says_why`
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`
  - `tests/test_intake_missing.py::test_the_refusal_names_what_the_earlier_list_holds_not_what_the_job_found`

Old text:

```
            if one.state is match.MatchState.MISSING:
                kept.append(n)
```

New text:

```
            if one.state is match.MatchState.MISSING and report["state"] == "missing":
                kept.append(n)
```

### `r503-a.G9_answered_last`

Ask answered rows after missing ones, so a rejected row is listed out of its playlist order

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-a.json`, row `G9_answered_last`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 213 against a baseline of 213
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
    asking = [
        (job, report)
        for job, report in rows_in
        if report["state"] == "missing" or next(answered)
    ]
```

New text:

```
    asking = sorted(
        [
            (job, report)
            for job, report in rows_in
            if report["state"] == "missing" or next(answered)
        ],
        key=lambda pair: pair[1]["state"] == "offered",
    )
```

### `r503-b.E2_offered_listed`

Existing: list every offered report as missing without asking, the shape the brief forbids

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-b.json`, row `E2_offered_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 213 against a baseline of 213
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_an_offered_row_nobody_answered_is_unchanged_and_asks_nothing`

Old text:

```
        if report["state"] == "missing" or next(answered)
```

New text:

```
        if report["state"] == "missing" or next(answered) or True
```

### `r503-b.G11_summary`

Drop the answered_* counts from the summary

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-b.json`, row `G11_summary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 213 against a baseline of 213
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_rejected_row_under_a_tombstone_is_suppressed_not_listed`
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_a_yes_about_a_copy_that_is_gone_stays_a_question`
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
        **now_answered,

```

New text:

```
(empty)
```

### `r503-b.G12_answered_check`

Reword the answered check's breakdown

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-b.json`, row `G12_answered_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 213 against a baseline of 213
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
            f"missing, {now_answered['answered_owned']} in the library, "
```

New text:

```
            f"listed, {now_answered['answered_owned']} owned, "
```

### `r503-b.G13_offered_check`

Reword the offered check's route back to this listing

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-b.json`, row `G13_offered_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 213 against a baseline of 213
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_an_offered_row_nobody_answered_is_unchanged_and_asks_nothing`

Old text:

```
            f"see: crate review list, then list this again",
```

New text:

```
            f"see: crate review list",
```

### `r503-b.G14_no_gone`

Never name the tracks the earlier list holds and this one does not

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-b.json`, row `G14_no_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 213 against a baseline of 213
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_shorter_rerun_over_the_jobs_earlier_list_refuses_and_says_why`
  - `tests/test_intake_missing.py::test_the_refusal_names_what_the_earlier_list_holds_not_what_the_job_found`

Old text:

```
    if gone:
        why.append(
```

New text:

```
    if False:
        why.append(
```

### `r503-b.G15_no_new`

Never name the tracks this list holds and the earlier one does not

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-b.json`, row `G15_no_new`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 213 against a baseline of 213
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_rejection_after_a_listing_refuses_over_the_earlier_list_and_says_why`

Old text:

```
    if new:
        why.append(
```

New text:

```
    if False:
        why.append(
```

### `r503-b.G16_json_uncaught`

Let an earlier file that is not JSON escape the hint as an internal error

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-b.json`, row `G16_json_uncaught`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 213 against a baseline of 213
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_different_list_already_at_the_path_is_refused_and_left_alone`
  - `tests/test_intake_missing.py::test_an_earlier_file_that_is_not_a_list_gives_no_reason_rather_than_a_wrong_one`

Old text:

```
    except (OSError, ValueError, KeyError, TypeError):
        return []
```

New text:

```
    except (OSError, KeyError, TypeError):
        return []
```

### `r503-b.G17_no_hint`

Drop the hint read from the earlier file altogether

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-b.json`, row `G17_no_hint`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 213 against a baseline of 213
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_rejection_after_a_listing_refuses_over_the_earlier_list_and_says_why`
  - `tests/test_intake_missing.py::test_a_shorter_rerun_over_the_jobs_earlier_list_refuses_and_says_why`
  - `tests/test_intake_missing.py::test_the_refusal_names_what_the_earlier_list_holds_not_what_the_job_found`

Old text:

```
        why = _changed_since(out, name, rows)
```

New text:

```
        why = []
```

### `r356-a.A10_provider_title_read_one_way_only`

Only the first reading of the provider's title is compared, so a version the provider spelled after a dash never agrees

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r356-a.json`, row `A10_provider_title_read_one_way_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 111 against a baseline of 111
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_provider_title_that_reads_two_ways_agrees_under_either_too`

Old text:

```
for one in listed.readings}
```

New text:

```
for one in (listed,)}
```

### `r356-a.A11_row_title_read_one_way_only`

Only the first reading of the row's title is compared

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r356-a.json`, row `A11_row_title_read_one_way_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 111 against a baseline of 111
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_title_that_reads_two_ways_agrees_under_either_and_still_needs_one`

Old text:

```
for one in row.readings}
```

New text:

```
for one in (row,)}
```

### `r356-a.A12_reason_outlives_its_match`

A reason is not cleared when the row is matched again, so a row that resolved still says it could not be

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r356-a.json`, row `A12_reason_outlives_its_match`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 111 against a baseline of 111
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_reason_does_not_outlive_the_match_it_was_about`

Old text:

```
        self._reasons.pop(key, None)

```

New text:

```
(empty)
```

### `r356-a.A13_reason_never_stored`

The adapter chooses nothing and says nothing about why

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r356-a.json`, row `A13_reason_never_stored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 0 against a baseline of 111
- Kills: 0 (collect-error)
- Note: collection changed: 0 collected against a baseline of 111. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Collection errors: `tests/test_outbound_tidal_account.py`

Old text:

```
                    if chosen is None:
                        self._reasons[key] = reason

```

New text:

```
(empty)
```

### `r356-a.A14_no_joiner_words`

A row spelling two artists with feat no longer agrees with the track billing both

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r356-a.json`, row `A14_no_joiner_words`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 111 against a baseline of 111
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_row_billing_two_artists_agrees_with_a_track_billing_the_same_two`

Old text:

```
_JOINERS = frozenset({"feat", "ft", "featuring", "with", "and", "vs", "x"})
```

New text:

```
_JOINERS = frozenset()
```

### `r356-a.A1_first_agreeing_rather_than_the_only_one`

Rule one takes the first agreeing track instead of requiring exactly one, which is the first result the unit's brief forbids

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r356-a.json`, row `A1_first_agreeing_rather_than_the_only_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 111 against a baseline of 111
- Kills: 27 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_file_album_matching_both_releases_stays_unmatched`
  - `tests/test_outbound_tidal_account.py::test_a_file_album_naming_neither_release_stays_unmatched_and_says_so`
  - `tests/test_outbound_tidal_account.py::test_a_file_album_naming_two_of_three_takes_the_lower_of_those_two`
  - `tests/test_outbound_tidal_account.py::test_a_file_with_no_album_tag_stays_unmatched_and_says_the_tag_is_missing`
  - `tests/test_outbound_tidal_account.py::test_a_heart_on_a_release_the_row_does_not_name_decides_nothing`
  - `tests/test_outbound_tidal_account.py::test_a_lone_heart_and_a_lone_album_choose_as_they_always_did`
  - `tests/test_outbound_tidal_account.py::test_a_lone_release_a_lone_heart_or_a_lone_album_is_never_a_broken_tie`
  - `tests/test_outbound_tidal_account.py::test_a_reason_does_not_outlive_the_match_it_was_about`
  - `tests/test_outbound_tidal_account.py::test_a_release_that_does_not_agree_is_never_taken`
  - `tests/test_outbound_tidal_account.py::test_a_release_the_account_already_hearts_is_the_one_an_export_adds`
  - `tests/test_outbound_tidal_account.py::test_a_sweep_hearts_the_release_the_files_album_tag_names`
  - `tests/test_outbound_tidal_account.py::test_a_sweep_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_tidal_account.py::test_a_tie_broken_by_any_agreeing_is_said_and_no_other_match_is`
  - `tests/test_outbound_tidal_account.py::test_a_tie_with_any_agreeing_takes_the_lowest_identifier_whatever_the_listing_order`
  - `tests/test_outbound_tidal_account.py::test_a_title_that_reads_two_ways_agrees_under_either_and_still_needs_one`
  - ... and 12 more, see the JSON sidecar

Old text:

```
        if len(agreeing) == 1 and not unreadable:
```

New text:

```
        if agreeing and not unreadable:
```

### `r356-a.A2_unreadable_track_no_longer_stops_rule_one`

A lone agreeing track is chosen beside one nobody could read

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r356-a.json`, row `A2_unreadable_track_no_longer_stops_rule_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 111 against a baseline of 111
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_release_that_cannot_be_read_stops_a_lone_agreeing_one_from_being_chosen`
  - `tests/test_outbound_tidal_account.py::test_an_unreadable_track_stops_the_album_from_choosing_the_lone_agreeing_one`

Old text:

```
        if len(agreeing) == 1 and not unreadable:
```

New text:

```
        if len(agreeing) == 1:
```

### `r356-a.A3_any_hearted_rather_than_the_only_hearted`

Rule two takes the first hearted release when the account hearts two

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r356-a.json`, row `A3_any_hearted_rather_than_the_only_hearted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 111 against a baseline of 111
- Kills: 4 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_the_album_never_overrides_a_heart_or_breaks_a_tie_between_two`
  - `tests/test_outbound_tidal_account.py::test_two_hearted_releases_spelled_alike_are_still_no_match`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_and_an_album_naming_one_of_them_is_a_broken_tie`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_or_an_album_naming_two_is_a_broken_tie`

Old text:

```
        if len(hearted) == 1:
```

New text:

```
        if hearted:
```

### `r356-a.A4_hearts_asked_of_every_track`

Rule two reads the hearts of every track the ISRC named instead of the agreeing ones, so a heart on the radio edit chooses for the plain record

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r356-a.json`, row `A4_hearts_asked_of_every_track`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 111 against a baseline of 111
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_heart_on_a_release_the_row_does_not_name_decides_nothing`

Old text:

```
        hearted = [remote for remote in agreeing if remote in hearts]
```

New text:

```
        hearted = [remote for remote in verdicts if remote in hearts]
```

### `r356-a.A5_withdrawn_track_is_a_candidate`

A track the provider will not play is compared like any other, with the version the client never read

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r356-a.json`, row `A5_withdrawn_track_is_a_candidate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 111 against a baseline of 111
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_track_the_provider_will_not_play_is_never_the_choice`
  - `tests/test_outbound_tidal_account.py::test_a_withdrawn_release_does_not_stop_the_one_that_plays_from_being_chosen`

Old text:

```
    return getattr(track, "available", True) is not False
```

New text:

```
    return True
```

### `r356-a.A7_artist_not_compared`

Agreement ignores the artist, so another act's record under the same title agrees

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r356-a.json`, row `A7_artist_not_compared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 111 against a baseline of 111
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_row_billing_two_artists_agrees_with_a_track_billing_the_same_two`
  - `tests/test_outbound_tidal_account.py::test_another_artist_under_the_same_title_does_not_agree`

Old text:

```
    if not _artist_agrees(row.artist, listed.artist, track):
        return False

```

New text:

```
(empty)
```

### `r356-a.A8_first_billed_artist_not_required`

A row naming only the guest agrees

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r356-a.json`, row `A8_first_billed_artist_not_required`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 111 against a baseline of 111
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_row_billing_two_artists_agrees_with_a_track_billing_the_same_two`

Old text:

```
    return bool(first) and first <= ours and ours - billed <= _JOINERS
```

New text:

```
    return bool(first) and ours - billed <= _JOINERS
```

### `r356-a.A9_row_may_name_an_artist_nobody_bills`

A row billing a third act the track does not agrees

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r356-a.json`, row `A9_row_may_name_an_artist_nobody_bills`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 111 against a baseline of 111
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_row_billing_two_artists_agrees_with_a_track_billing_the_same_two`

Old text:

```
    return bool(first) and first <= ours and ours - billed <= _JOINERS
```

New text:

```
    return bool(first) and first <= ours
```

### `r358-round-2.A3_editor_check`

Drop the editor check, so a playlist the account cannot edit is renamed

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r358-round-2.json`, row `A3_editor_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 111 against a baseline of 111
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_playlist_the_account_cannot_edit_refuses_rather_than_reporting_a_rename`

Old text:

```
        if not callable(retitle):
            raise account.provider_failure(
                LookupError(
                    f"the provider's playlist {playlist_id!r} cannot be retitled by "
                    f"this account"
                ),
                doing,
            )

```

New text:

```
(empty)
```

### `r358-round-2.A5_absent_answer`

Accept an explicit not found as a rename that landed

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r358-round-2.json`, row `A5_absent_answer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 111 against a baseline of 111
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_playlist_deleted_between_the_open_and_the_edit_is_the_items_cause`

Old text:

```
        accepted = self._call(doing, lambda: retitle(title=wanted))
        if accepted is False or accepted is _ABSENT:
```

New text:

```
        accepted = self._call(doing, lambda: retitle(title=wanted))
        if accepted is False:
```

### `r358-round-2.A7_empty_title_message`

Reword the empty-title refusal, never append to it

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r358-round-2.json`, row `A7_empty_title_message`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 111 against a baseline of 111
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_rename_with_no_title_is_refused_before_the_client_sees_it[   ]`
  - `tests/test_outbound_tidal_account.py::test_a_rename_with_no_title_is_refused_before_the_client_sees_it[\n]`
  - `tests/test_outbound_tidal_account.py::test_a_rename_with_no_title_is_refused_before_the_client_sees_it[]`

Old text:

```
                f"a rename of the playlist {playlist_id} was asked for with no "
                f"title; the client reads a falsy title as keep the current one "
                f"and answers that it succeeded, so nothing was sent",
```

New text:

```
                f"the playlist {playlist_id} was given a blank title, which the "
                f"client would read as an instruction to keep the current one",
```

### `r358.A1_empty_title_refusal`

Drop the empty-title refusal, so a blank title reaches the client

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r358.json`, row `A1_empty_title_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 111 against a baseline of 111
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_rename_with_no_title_is_refused_before_the_client_sees_it[   ]`
  - `tests/test_outbound_tidal_account.py::test_a_rename_with_no_title_is_refused_before_the_client_sees_it[\n]`
  - `tests/test_outbound_tidal_account.py::test_a_rename_with_no_title_is_refused_before_the_client_sees_it[]`

Old text:

```
        if not wanted.strip():
            # NOT ``provider_failure``. The provider did not fail, and its
            # remedy is "resume the job to retry this item", which is advice
            # that cannot work: the same empty title fails the same way.
            raise refuse(
                "internal-error",
                f"a rename of the playlist {playlist_id} was asked for with no "
                f"title; the client reads a falsy title as keep the current one "
                f"and answers that it succeeded, so nothing was sent",
                scope=Scope.SOURCE,
                origin=("outbound", "account"),
                detail={"playlist_id": str(playlist_id)},
            )

```

New text:

```
(empty)
```

### `r358.A2_title_stripped_for_the_write`

Strip the title for the write as well as for the emptiness test

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r358.json`, row `A2_title_stripped_for_the_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 111 against a baseline of 111
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_title_the_caller_padded_is_written_as_the_caller_asked`

Old text:

```
        wanted = str(name)
        doing = f"rename the playlist {playlist_id} to {wanted!r}"
```

New text:

```
        wanted = str(name).strip()
        doing = f"rename the playlist {playlist_id} to {wanted!r}"
```

### `r358.A4_false_answer`

Accept a False answer as a rename that landed

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r358.json`, row `A4_false_answer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 111 against a baseline of 111
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_rename_the_client_answers_false_is_the_items_cause_not_a_quiet_return`

Old text:

```
        if accepted is False or accepted is _ABSENT:
            raise account.provider_failure(
                RuntimeError("the provider did not accept the new playlist title"),
                doing,
            )
```

New text:

```
        if accepted is _ABSENT:
            raise account.provider_failure(
                RuntimeError("the provider did not accept the new playlist title"),
                doing,
            )
```

### `r358.A6_retry_coefficient`

Take the rename's retry to zero, the way a create takes it

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r358.json`, row `A6_retry_coefficient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 111 against a baseline of 111
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_rename_the_provider_refuses_once_is_retried_once_into_the_same_title`

Old text:

```
        accepted = self._call(doing, lambda: retitle(title=wanted))
```

New text:

```
        accepted = self._call(doing, lambda: retitle(title=wanted), retries=0)
```

### `r572.A1_album_rule_gone`

Drop the album rule: every none hearted tie stays unmatched

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r572.json`, row `A1_album_rule_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 0 against a baseline of 111
- Kills: 0 (collect-error)
- Note: collection changed: 0 collected against a baseline of 111. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Collection errors: `tests/test_outbound_tidal_account.py`

Old text:

```
        if len(named_album) == 1:
            return named_album[0], ""
```

New text:

```
(empty)
```

### `r572.A2_first_named`

Take the first release the album names even when several do

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r572.json`, row `A2_first_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 111 against a baseline of 111
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_file_album_matching_both_releases_stays_unmatched`

Old text:

```
        if len(named_album) == 1:
```

New text:

```
        if len(named_album) >= 1:
```

### `r572.A3_album_over_two_hearts`

Let the album decide when two releases are hearted

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r572.json`, row `A3_album_over_two_hearts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 0 against a baseline of 111
- Kills: 0 (collect-error)
- Note: collection changed: 0 collected against a baseline of 111. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Collection errors: `tests/test_outbound_tidal_account.py`

Old text:

```
        if hearted:
            return None, f"{said}, so none was chosen"
```

New text:

```
(empty)
```

### `r572.A4_no_fold`

Compare the album raw rather than folded

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r572.json`, row `A4_no_fold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 111 against a baseline of 111
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_file_album_matching_both_releases_stays_unmatched`
  - `tests/test_outbound_tidal_account.py::test_a_sweep_hearts_the_release_the_files_album_tag_names`
  - `tests/test_outbound_tidal_account.py::test_releases_spelled_alike_resolve_to_the_one_the_files_album_names`

Old text:

```
        wanted = match.fold(album)
```

New text:

```
        wanted = album
```

### `r572.A5_album_among_all`

Choose by album among every candidate, not only the agreeing ones

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r572.json`, row `A5_album_among_all`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 111 against a baseline of 111
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_the_album_chooses_only_among_releases_that_agree_with_the_row`

Old text:

```
            remote for remote in agreeing if match.fold(_album_name(tracks[remote])) == wanted
```

New text:

```
            remote for remote in tracks if match.fold(_album_name(tracks[remote])) == wanted
```

### `r572.A6_album_despite_unreadable`

Let the album choose even when another track could not be read

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r572.json`, row `A6_album_despite_unreadable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 0 against a baseline of 111
- Kills: 0 (collect-error)
- Note: collection changed: 0 collected against a baseline of 111. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Collection errors: `tests/test_outbound_tidal_account.py`

Old text:

```
        if unreadable:
            return None, f"{said}, so none was chosen"
```

New text:

```
(empty)
```

### `r834.M1_a_create_makes_the_playlist_private`

TidalAccount.create_playlist: drop the private step, so a created playlist keeps whatever visibility the provider defaults to, the defect R-834 named

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r834.json`, row `M1_a_create_makes_the_playlist_private`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 111 against a baseline of 111
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_created_playlist_is_made_private_once`
  - `tests/test_outbound_tidal_account.py::test_a_playlist_export_runs_to_done_and_the_ledger_records_every_add`
  - `tests/test_outbound_tidal_account.py::test_a_private_step_refused_once_is_retried_once_and_lands`
  - `tests/test_outbound_tidal_account.py::test_a_private_step_refused_twice_still_hands_back_the_one_playlist`
  - `tests/test_outbound_tidal_account.py::test_a_second_export_finds_its_playlist_and_neither_creates_nor_sets_visibility`

Old text:

```
        self._make_private(created, identifier)

```

New text:

```
(empty)
```

### `r834.M3_a_refused_private_step_does_not_lose_the_playlist`

_make_private: raise the refusal instead of passing over it, so the create fails after the playlist exists and the ledger never records it

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r834.json`, row `M3_a_refused_private_step_does_not_lose_the_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 111 against a baseline of 111
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_created_playlist_the_client_offers_no_private_call_for_is_still_returned`
  - `tests/test_outbound_tidal_account.py::test_a_private_step_refused_twice_still_hands_back_the_one_playlist`

Old text:

```
        except CratekitError:
            return
```

New text:

```
        except CratekitError:
            raise
```

### `r834.M5_a_create_is_never_retried`

create_playlist: retry the create like a write, so a create that reached the provider and timed out is retried into a second playlist (an existing guard, sampled)

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r834.json`, row `M5_a_create_is_never_retried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 111 against a baseline of 111
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_playlist_create_is_never_retried_into_a_second_playlist`

Old text:

```
            lambda: self._session.user.create_playlist(name, ""),
            retries=0,
```

New text:

```
            lambda: self._session.user.create_playlist(name, ""),
```

### `u97-c.C1_outbound_refusal_removed`

composite for B4: remove the outbound account's missing session refusal entirely, so the seam opens a client with no credential. Shows what the guard holds when its remedy holds nothing

- File: `src/cratekit/modules/outbound/account.py`
- Source: `u97-c.json`, row `C1_outbound_refusal_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 111 against a baseline of 111
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_session_removed_after_an_open_is_refused_rather_than_reused`

Old text:

```
    if not secrets.exists(str(secrets.Credential.PROVIDER_SESSION)):
        raise refuse(
            "credential-missing",
            "no streaming provider session is stored, so there is no account "
            "to write this playlist or these hearts to",
```

New text:

```
    if False:
        raise refuse(
            "credential-missing",
            "no streaming provider session is stored, so there is no account "
            "to write this playlist or these hearts to",
```

### `r679-b.C1_credited_rule_not_owning`

OWNING_RULES: leave the credited rule out, so its 4 items stay open

- File: `src/cratekit/acquire/match.py`
- Source: `r679-b.json`, row `C1_credited_rule_not_owning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_review_queue.py`
- Collected: 879 against a baseline of 879
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_persons_acceptance_being_applied_retires_nothing`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[credited-exact]`

Old text:

```
OWNING_RULES: frozenset[Why] = frozenset({Why.EXACT, Why.ISRC_EXACT, Why.CREDITED_EXACT})
```

New text:

```
OWNING_RULES: frozenset[Why] = frozenset({Why.EXACT, Why.ISRC_EXACT})
```

### `r679-b.C2_reading_shape_missing`

QUESTION_SHAPES: leave the reading shape out, so a reading question is never retired

- File: `src/cratekit/acquire/match.py`
- Source: `r679-b.json`, row `C2_reading_shape_missing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_review_queue.py`
- Collected: 879 against a baseline of 879
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_every_question_identity_is_one_per_shape_and_agrees_with_the_asked_one`

Old text:

```
    ASKS_ABOUT_RECORDING,
    ASKS_ABOUT_READING,
)
```

New text:

```
    ASKS_ABOUT_RECORDING,
)
```

### `r679-b.D2_fallback_gate_on_question_alone`

fallback pass: gate the store on the needs-review state alone

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `r679-b.json`, row `D2_fallback_gate_on_question_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_review_queue.py`
- Collected: 879 against a baseline of 879
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_every_caller_of_adjudicate_gates_on_the_rows_that_touch_the_queue`

Old text:

```
    if any(match_cli.touches_the_queue(one) for one in resolved.matches):
```

New text:

```
    if any(one.state is match.MatchState.NEEDS_REVIEW for one in resolved.matches):
```

### `r679-b.B1_no_retirement`

adjudicate: never retire, so an owned row leaves its question open

- File: `src/cratekit/acquire/match_cli.py`
- Source: `r679-b.json`, row `B1_no_retirement`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_review_queue.py`
- Collected: 879 against a baseline of 879
- Kills: 7 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_an_intake_job_that_owns_a_row_by_isrc_retires_the_question_an_earlier_job_asked`
  - `tests/test_match_states.py::test_a_retired_question_offered_again_is_neither_reopened_nor_duplicated`
  - `tests/test_match_states.py::test_a_retired_question_the_row_asks_again_is_reopened_not_read_as_a_rejection`
  - `tests/test_match_states.py::test_a_retired_question_whose_row_goes_missing_keeps_the_verdict`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[credited-exact]`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[isrc-exact]`
  - `tests/test_match_states.py::test_the_verb_lists_a_retired_question_only_when_asked_for_everything`

Old text:

```
        if owned_by_a_rule(found):
```

New text:

```
        if False:
```

### `r679-b.B2_any_matched_row_is_owned_by_a_rule`

owned_by_a_rule: any matched row counts, a person's applied acceptance included

- File: `src/cratekit/acquire/match_cli.py`
- Source: `r679-b.json`, row `B2_any_matched_row_is_owned_by_a_rule`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_review_queue.py`
- Collected: 879 against a baseline of 879
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_the_gate_predicate_admits_a_question_and_a_rule_owned_row_and_nothing_else`

Old text:

```
    return found.state is match.MatchState.MATCHED and found.why in match.OWNING_RULES
```

New text:

```
    return found.state is match.MatchState.MATCHED
```

### `r679-b.B3_no_reopen`

adjudicate: leave a superseded item standing when its row asks again

- File: `src/cratekit/acquire/match_cli.py`
- Source: `r679-b.json`, row `B3_no_reopen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_review_queue.py`
- Collected: 879 against a baseline of 879
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_retired_question_the_row_asks_again_is_reopened_not_read_as_a_rejection`

Old text:

```
        if held is not None and held.verdict is review.Verdict.SUPERSEDED:
```

New text:

```
        if False:
```

### `r679-b.B5_rule_not_recorded`

retire_questions: record a fixed rule instead of the why that owned the row

- File: `src/cratekit/acquire/match_cli.py`
- Source: `r679-b.json`, row `B5_rule_not_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_review_queue.py`
- Collected: 879 against a baseline of 879
- Kills: 5 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_an_intake_job_that_owns_a_row_by_isrc_retires_the_question_an_earlier_job_asked`
  - `tests/test_match_states.py::test_a_retired_question_whose_row_goes_missing_keeps_the_verdict`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[credited-exact]`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[isrc-exact]`
  - `tests/test_match_states.py::test_the_verb_lists_a_retired_question_only_when_asked_for_everything`

Old text:

```
        rule=str(found.why),
```

New text:

```
        rule="exact",
```

### `r679-b.B6_one_shape_only`

retire_questions: ask about the first shape only, so a version question is never retired

- File: `src/cratekit/acquire/match_cli.py`
- Source: `r679-b.json`, row `B6_one_shape_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_review_queue.py`
- Collected: 879 against a baseline of 879
- Kills: 7 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_an_intake_job_that_owns_a_row_by_isrc_retires_the_question_an_earlier_job_asked`
  - `tests/test_match_states.py::test_a_retired_question_offered_again_is_neither_reopened_nor_duplicated`
  - `tests/test_match_states.py::test_a_retired_question_the_row_asks_again_is_reopened_not_read_as_a_rejection`
  - `tests/test_match_states.py::test_a_retired_question_whose_row_goes_missing_keeps_the_verdict`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[credited-exact]`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[isrc-exact]`
  - `tests/test_match_states.py::test_the_verb_lists_a_retired_question_only_when_asked_for_everything`

Old text:

```
            for identity in found.wanted.questions()
```

New text:

```
            for identity in found.wanted.questions()[:1]
```

### `r679-b.D5_missing_per_row_gate_on_question_alone`

missing pass, per row grouping: gate on the needs-review state alone while the other call site still names the predicate

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r679-b.json`, row `D5_missing_per_row_gate_on_question_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_review_queue.py`
- Collected: 879 against a baseline of 879
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_every_caller_of_adjudicate_gates_on_the_rows_that_touch_the_queue`

Old text:

```
        if match_cli.touches_the_queue(one):
```

New text:

```
        if one.state is match.MatchState.NEEDS_REVIEW:
```

### `r679-b.D1_intake_gate_on_question_alone`

intake worker: gate the store on the needs-review state alone, the code before the fix round

- File: `src/cratekit/intake/cli.py`
- Source: `r679-b.json`, row `D1_intake_gate_on_question_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_review_queue.py`
- Collected: 879 against a baseline of 879
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_an_intake_job_that_owns_a_row_by_isrc_retires_the_question_an_earlier_job_asked`
  - `tests/test_match_states.py::test_every_caller_of_adjudicate_gates_on_the_rows_that_touch_the_queue`

Old text:

```
    if not match_cli.touches_the_queue(found):
```

New text:

```
    if found.state is not match.MatchState.NEEDS_REVIEW:
```

### `r431-b.B10_an_older_payload_reads_as_solo`

A payload frozen before the field existed thaws as billing one artist and asks for a companion

- File: `src/cratekit/intake/cli.py`
- Source: `r431-b.json`, row `B10_an_older_payload_reads_as_solo`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 682 against a baseline of 682
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_billed_guest_survives_the_freeze_the_worker_resolves_from`

Old text:

```
        several_artists=bool(said.get("several_artists", True)),
```

New text:

```
        several_artists=bool(said.get("several_artists", False)),
```

### `r431-b.B9_the_freeze_drops_the_field`

The intake freeze stops carrying several_artists, so the worker resolves from a track that never looked

- File: `src/cratekit/intake/cli.py`
- Source: `r431-b.json`, row `B9_the_freeze_drops_the_field`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 682 against a baseline of 682
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_queueing_a_playlist_lists_it_through_the_catalogue_and_keys_items_by_provider_id`
  - `tests/test_intake_missing.py::test_a_billed_guest_survives_the_freeze_the_worker_resolves_from`
  - `tests/test_intake_missing.py::test_a_deleted_track_whose_row_kept_a_credit_is_suppressed_and_not_listed`

Old text:

```
        "several_artists": row.several_artists,
```

New text:

```
(empty)
```

### `r504-b.B1_verb_drops_short`

intake playlist favorites lists the hearts and throws the shortfall away

- File: `src/cratekit/intake/cli.py`
- Source: `r504-b.json`, row `B1_verb_drops_short`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 682 against a baseline of 682
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`
  - `tests/test_intake_missing.py::test_the_default_human_output_names_the_shortfall`
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`

Old text:

```
            tracks, short = list_favorites(found)
```

New text:

```
            tracks, short = list_favorites(found)[0], None
```

### `u144-c.C8_question_named`

Library rows: name an unanswered question as a track the library lacks

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u144-c.json`, row `C8_question_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_near_match_is_a_question_named_as_a_miss_and_never_written`

Old text:

```
            return "", UNANSWERED
```

New text:

```
            return "", NOT_HELD
```

