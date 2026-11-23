# Mutation table: u325-before-l-04

Measured by `scripts/mutate.py` on 2026-11-22 22:24 UTC, branch `HEAD` at `539638eb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22663 collected. pytest invocations for this batch: 138.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:24 UTC for commit `539638ebe629`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 6, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22663 against 22663. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u155.W5_owed_once` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `u155.W6_inbox_item_genre` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `u155.W7_export_item_genre` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
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
| `u45-round-1.A1_unreadable_reported_as_absent` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 5 | killed |
| `u45-round-1.A4_state_collapsed_to_known` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 2 | killed |
| `u45-round-1.C2_refusal_read_as_failure` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 6 | killed |
| `u45-round-1.C3_nothing_ran_accepted` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 8 | killed |
| `u45-round-1.C4_uniform_refusal_flattened` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 3 | killed |
| `u45-round-1.C5_first_refusal_taken` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `u45-round-1.C6_partial_run_refused` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 3 | killed |
| `u45-round-1.H2_queueing_plans_first` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
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
| `u50-author.B1_no_items_enqueued` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 38 | killed |
| `u50-author.B3_items_one_portion_only` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 16 | killed |
| `u50-author.W1_no_narrowing` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 22663 | 0 (promoted) | zero |
| `u50-author.W5_unknown_portion_unchecked` | `src/cratekit/backup/cli.py` | maintainer | 1 file(s) | 99 | 1 | killed |
| `u50-author.W6_fresh_config_in_the_handler` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 2 | killed |
| `u50-review-fixes.R2_empty_job_guard_dropped` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `u50-zero-rows.B2_items_hardcoded_pair` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `u50-zero-rows.W4b_item_ignored_entirely` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 14 | killed |
| `r1295.M10_unread_off_misses` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 4 | killed |
| `r1295.M11_again_drops_unread` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 2 | killed |
| `r1295.M12_setrow_keeps_no_unread` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 2 | killed |
| `r1295.M13_unread_miss_no_id` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 4 | killed |
| `r1295.M14_unread_miss_blank_title` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 3 | killed |
| `r1295.M15_plan_passes_no_unread` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 4 | killed |
| `r1295.M17_skip_guard` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 2 | killed |
| `r1295.M1_refused_row_fatal` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 6 | killed |
| `r1295.M2_no_id_named` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 1 | killed |
| `r1295.M3_read_positions_renumbered` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 1 | killed |
| `r1295.M4_unread_positions_renumbered` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 3 | killed |
| `r1295.M5_all_unread_branch` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 2 | killed |
| `r1295.M6_none_read_uncapped` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 1 | killed |
| `r1295.M7_none_read_rest_uncounted` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 1 | killed |
| `r1295.M8_none_read_withheld_dropped` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 1 | killed |
| `r1295.M9_misses_unsorted` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 1 | killed |
| `u144-a.A1_skip_rule` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 2 | killed |
| `u144-a.A2_two_of_one_name` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 1 | killed |
| `u144-a.A4_sets_folder_name` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 2 | killed |
| `u144-a.A5_recorded_folder` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 1 | killed |

## Zero rows and what they owe

- `u50-author.W1_no_narrowing` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

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
- Kills: 8 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_job_in_which_nothing_ran_never_reports_success`
  - `tests/test_backup_cli.py::test_a_machine_with_no_rclone_fails_every_portion_by_name`
  - `tests/test_backup_cli.py::test_a_machine_with_no_rclone_refuses_by_name`
  - `tests/test_backup_cli.py::test_a_portion_the_engine_refused_fails_rather_than_reporting_a_copy`
  - `tests/test_backup_cli.py::test_a_real_backup_that_ended_badly_gains_no_rehearsal_step`
  - `tests/test_backup_cli.py::test_a_rehearsal_that_ended_badly_still_says_it_was_a_rehearsal`
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

### `u45-round-1.H2_queueing_plans_first`

Plan inside the handler, so queueing refuses on a machine with no rclone where the work would have run fine

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `H2_queueing_plans_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_queueing_needs_no_rclone_no_remote_and_no_volume`

Old text:

```
    cfg = _load()
    with jobs.open_store() as store:
        if ctx.args.job:
```

New text:

```
    cfg = _load()
    backup.plan_backup(cfg)
    with jobs.open_store() as store:
        if ctx.args.job:
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
- Kills: 38 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_backup_job_carries_one_item_per_declared_portion`
  - `tests/test_backup_cli.py::test_a_contained_analysis_share_draws_no_warning_from_the_verb`
  - `tests/test_backup_cli.py::test_a_defect_in_rebuilding_a_configuration_is_not_reported_as_a_queued_backup`
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_job_in_which_nothing_ran_never_reports_success`
  - `tests/test_backup_cli.py::test_a_library_whose_identity_cannot_be_a_marker_is_told_so`
  - `tests/test_backup_cli.py::test_a_library_with_an_identity_draws_no_such_warning`
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
  - `tests/test_backup_cli.py::test_a_queued_backup_names_every_command_it_ran_in_job_show`
  - `tests/test_backup_cli.py::test_a_queued_backup_runs_every_portion_through_the_real_resume`
  - `tests/test_backup_cli.py::test_a_queued_real_backup_carries_no_rehearsal_word`
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_a_rehearsal_s_outcome_is_recorded_and_says_it_was_one`
  - ... and 23 more, see the JSON sidecar

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
- Kills: 16 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_backup_job_carries_one_item_per_declared_portion`
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
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
  - `tests/test_backup_cli.py::test_the_item_list_is_derived_from_the_portions_rather_than_written_out`
  - ... and 1 more, see the JSON sidecar

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
- Collected: 22663 against a baseline of 22663
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
- Kills: 2 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_configuration_the_worker_runs_against_is_the_frozen_one`
  - `tests/test_backup_cli.py::test_the_handler_uses_the_configuration_it_was_handed`

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
- Kills: 14 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_queued_backup_names_every_command_it_ran_in_job_show`
  - `tests/test_backup_cli.py::test_a_queued_backup_runs_every_portion_through_the_real_resume`
  - `tests/test_backup_cli.py::test_a_rehearsal_s_outcome_is_recorded_and_says_it_was_one`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`
  - `tests/test_backup_cli.py::test_an_item_naming_something_that_is_not_a_portion_refuses_by_name`
  - `tests/test_backup_cli.py::test_an_outside_analysis_share_is_carried_through_the_verb`
  - `tests/test_backup_cli.py::test_asking_twice_about_a_half_failed_backup_answers_the_same_way_twice`
  - `tests/test_backup_cli.py::test_the_age_a_driven_run_publishes_is_the_engine_s_and_reaches_the_envelope`
  - `tests/test_backup_cli.py::test_the_ages_a_rehearsal_reports_are_the_previous_real_runs_and_it_says_so`
  - `tests/test_backup_cli.py::test_the_ages_reported_are_the_ones_this_job_published`
  - `tests/test_backup_cli.py::test_the_outcome_record_is_private_under_a_permissive_umask`

Old text:

```
    named = str(item.item_id or "")
```

New text:

```
    named = str(backup_facts.Portion.FILES)
```

### `r1295.M10_unread_off_misses`

_matched: an unread track is not among the set's misses

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M10_unread_off_misses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 4 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_miss_the_library_lacks_ahead_of_an_unread_track_keeps_set_order`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_artist_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_title_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_an_unread_track_keeps_the_sets_positions_for_every_other_miss`

Old text:

```
    misses: list[Miss] = list(unread)
```

New text:

```
    misses: list[Miss] = []
```

### `r1295.M11_again_drops_unread`

again: the write re-decides without the unread tracks, so the approved plan reads stale

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M11_again_drops_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_track_with_no_artist_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_title_is_named_and_the_sets_other_tracks_are_written`

Old text:

```
                    row.withheld,
                    row_of,
                    row.unread,
```

New text:

```
                    row.withheld,
                    row_of,
                    (),
```

### `r1295.M12_setrow_keeps_no_unread`

_decided: the set row keeps no unread tracks for the write to decide from

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M12_setrow_keeps_no_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_track_with_no_artist_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_title_is_named_and_the_sets_other_tracks_are_written`

Old text:

```
        unread=unread,
    )
```

New text:

```
        unread=(),
    )
```

### `r1295.M13_unread_miss_no_id`

_unread_miss: the miss line names no track id

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M13_unread_miss_no_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 4 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_miss_the_library_lacks_ahead_of_an_unread_track_keeps_set_order`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_artist_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_title_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_an_unread_track_keeps_the_sets_positions_for_every_other_miss`

Old text:

```
f"{one.why} (track {one.ref}), so it was not asked of the library"
```

New text:

```
f"{one.why}, so it was not asked of the library"
```

### `r1295.M14_unread_miss_blank_title`

_unread_miss: an absent title shown blank rather than as no title

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M14_unread_miss_blank_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_miss_the_library_lacks_ahead_of_an_unread_track_keeps_set_order`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_title_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_an_unread_track_keeps_the_sets_positions_for_every_other_miss`

Old text:

```
        one.title or "no title",
```

New text:

```
        one.title,
```

### `r1295.M15_plan_passes_no_unread`

plan: the readable sets are decided with no unread misses

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M15_plan_passes_no_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 4 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_miss_the_library_lacks_ahead_of_an_unread_track_keeps_set_order`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_artist_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_title_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_an_unread_track_keeps_the_sets_positions_for_every_other_miss`

Old text:

```
                    tuple(_unread_miss(place, one) for place, one in listing.unread),
```

New text:

```
                    (),
```

### `r1295.M17_skip_guard`

plan (existing guard, sample): a set INSPIRATION already holds is read and planned again

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M17_skip_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_second_run_plans_nothing`
  - `tests/test_organize_inspiration.py::test_a_set_already_under_inspiration_is_skipped_and_its_tracks_never_read`

Old text:

```
        if name in held:
```

New text:

```
        if False:
```

### `r1295.M1_refused_row_fatal`

_read: every refused row raises again, so one untitled track leaves the whole set unread as on main

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M1_refused_row_fatal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_miss_the_library_lacks_ahead_of_an_unread_track_keeps_set_order`
  - `tests/test_organize_inspiration.py::test_a_set_no_track_of_which_reads_is_filed_unread_naming_each`
  - `tests/test_organize_inspiration.py::test_a_set_no_track_of_which_reads_names_five_counts_the_rest_and_the_withheld`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_artist_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_title_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_an_unread_track_keeps_the_sets_positions_for_every_other_miss`

Old text:

```
            one = intake_cli.set_aside(row)
            if not one.ref:
```

New text:

```
            one = intake_cli.set_aside(row)
            if True:
```

### `r1295.M2_no_id_named`

_read: a refused row with no provider id is named as a miss rather than leaving its set unread

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M2_no_id_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_set_whose_unread_track_carries_no_provider_id_is_still_filed_unread`

Old text:

```
            if not one.ref:
```

New text:

```
            if False:
```

### `r1295.M3_read_positions_renumbered`

_read: a read track's place counts only the rows read, so a miss after an unread row is misplaced

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M3_read_positions_renumbered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_an_unread_track_keeps_the_sets_positions_for_every_other_miss`

Old text:

```
            wanted.append((position, match.read_row(
```

New text:

```
            wanted.append((len(wanted) + 1, match.read_row(
```

### `r1295.M4_unread_positions_renumbered`

_read: an unread track's place counts only the unread rows

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M4_unread_positions_renumbered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_miss_the_library_lacks_ahead_of_an_unread_track_keeps_set_order`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_artist_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_title_is_named_and_the_sets_other_tracks_are_written`

Old text:

```
            unread.append((position, one))
```

New text:

```
            unread.append((len(unread) + 1, one))
```

### `r1295.M5_all_unread_branch`

plan: drop the every track unread branch, so such a set reads as one with no match

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M5_all_unread_branch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_set_no_track_of_which_reads_is_filed_unread_naming_each`
  - `tests/test_organize_inspiration.py::test_a_set_no_track_of_which_reads_names_five_counts_the_rest_and_the_withheld`

Old text:

```
        if listing.unread and not listing.wanted:
```

New text:

```
        if False:
```

### `r1295.M6_none_read_uncapped`

_none_read: name every unread track rather than the first five

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M6_none_read_uncapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_set_no_track_of_which_reads_names_five_counts_the_rest_and_the_withheld`

Old text:

```
listing.unread[:NAMED_UNREAD])
```

New text:

```
listing.unread)
```

### `r1295.M7_none_read_rest_uncounted`

_none_read: say nothing of the unread tracks past the fifth

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M7_none_read_rest_uncounted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_set_no_track_of_which_reads_names_five_counts_the_rest_and_the_withheld`

Old text:

```
    if rest > 0:
```

New text:

```
    if False:
```

### `r1295.M8_none_read_withheld_dropped`

_none_read: say nothing of the tracks the provider withheld

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M8_none_read_withheld_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_set_no_track_of_which_reads_names_five_counts_the_rest_and_the_withheld`

Old text:

```
    if listing.withheld:
        said +=
```

New text:

```
    if False:
        said +=
```

### `r1295.M9_misses_unsorted`

_matched: misses kept unread first rather than in set order

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M9_misses_unsorted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_miss_the_library_lacks_ahead_of_an_unread_track_keeps_set_order`

Old text:

```
tuple(sorted(misses, key=lambda miss: miss.position))
```

New text:

```
tuple(misses)
```

### `u144-a.A1_skip_rule`

Plan: drop the skip of a set INSPIRATION already holds, so it is read and planned again

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-a.json`, row `A1_skip_rule`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_second_run_plans_nothing`
  - `tests/test_organize_inspiration.py::test_a_set_already_under_inspiration_is_skipped_and_its_tracks_never_read`

Old text:

```
        if name in held:
            rows.append(SetRow(name, playlist_id, folder, SKIP))
```

New text:

```
        if False:
            rows.append(SetRow(name, playlist_id, folder, SKIP))
```

### `u144-a.A2_two_of_one_name`

Plan: drop the two account sets of one name check, so both are read and planned

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-a.json`, row `A2_two_of_one_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_two_account_sets_of_one_name_are_both_left`

Old text:

```
        if named[name] > 1:
```

New text:

```
        if False:
```

### `u144-a.A4_sets_folder_name`

Account sets: read every root folder, not only a Downloaded Sets year or a recorded one

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-a.json`, row `A4_sets_folder_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_sets_folder_the_archive_recorded_is_read_whatever_it_is_called_now`
  - `tests/test_organize_inspiration.py::test_only_prefixed_playlists_in_a_downloaded_sets_folder_are_sets`

Old text:

```
        if not sets_folder(folder_name) and folder_id not in marked:
```

New text:

```
        if False:
```

### `u144-a.A5_recorded_folder`

Account sets: ignore the ledger's record, so a renamed sets folder is passed over

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-a.json`, row `A5_recorded_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_sets_folder_the_archive_recorded_is_read_whatever_it_is_called_now`

Old text:

```
        if not sets_folder(folder_name) and folder_id not in marked:
```

New text:

```
        if not sets_folder(folder_name):
```

