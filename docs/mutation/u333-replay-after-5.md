# Mutation table: u333-replay-after-5

Measured by `scripts/mutate.py` on 2026-11-24 06:10 UTC, branch `HEAD` at `5d49f5eb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23236 collected. pytest invocations for this batch: 423.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 06:10 UTC for commit `5d49f5ebb1bf`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 44, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23236 against 23236. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u154.G4_stale_target_check_dropped` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 23 | 1 | killed |
| `u154.G5_unmatched_file_shelved_anyway` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 23 | 1 | killed |
| `u154.G6_subfolder_check_dropped` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 23 | 1 | killed |
| `u154.G7_run_id_shape_unread` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 23 | 4 | killed |
| `u154.G8_free_target_no_suffix` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 23 | 3 | killed |
| `u154.R1_rows_under_target_not_consulted` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 23 | 1 | killed |
| `u154.R3_repeated_name_planned_twice` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 23 | 1 | killed |
| `u154.R6_device_probe_dropped` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 23 | 1 | killed |
| `u154.R7_exact_prefix_filter_dropped` | `src/cratekit/intake/shelve.py` | maintainer | 1 file(s) | 23 | 1 | killed |
| `u164.T1_filed_target` | `src/cratekit/intake/shelve.py` | user | 4 file(s) | 98 | 33 | killed |
| `u164.T2_free_disk` | `src/cratekit/intake/shelve.py` | user | 2 file(s) | 29 | 3 | killed |
| `u164.T3_free_stored` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 6 | 2 | killed |
| `u164.T4_undated_name` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 6 | 1 | killed |
| `u164.T5_empty_subject` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 6 | 1 | killed |
| `u164.T6_reuse_recorded` | `src/cratekit/intake/shelve.py` | user | 3 file(s) | 75 | 5 | killed |
| `u164.T7_reuse_gone` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 6 | 1 | killed |
| `u235.H1_shelve_four_hex_only` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 23 | 2 | killed |
| `u235.H2_shelve_sixteen_hex_only` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 23 | 2 | killed |
| `u154.G12_empty_plan_asks_a_gate` | `src/cratekit/intake/shelve_cli.py` | user | 1 file(s) | 23 | 1 | killed |
| `u154.G13_as_with_all_admitted` | `src/cratekit/intake/shelve_cli.py` | user | 1 file(s) | 23 | 1 | killed |
| `u154.R2_subject_path_part_admitted` | `src/cratekit/intake/shelve_cli.py` | user | 1 file(s) | 23 | 1 | killed |
| `u164.S1_already_filed` | `src/cratekit/intake/shelve_cli.py` | user | 1 file(s) | 6 | 1 | killed |
| `u164.S2_music_folder_wins` | `src/cratekit/intake/shelve_cli.py` | user | 1 file(s) | 23 | 6 | killed |
| `r798-c.H6_a_returned_release_passes_at_approval` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 141 | 3 | killed |
| `r798-d.H7_again_an_owned_release_is_not_asked_about` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 141 | 1 | killed |
| `u101.G10_ungated_not_reported_in_judged_label` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 3 | killed |
| `u101.G11_keep_read_as_drop` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 12 | killed |
| `u101.G12_reported_share_not_the_taxonomys` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G13_family_count_off_by_one` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 2 | killed |
| `u101.G14_classified_counts_unjudged` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G17_refusal_silent_on_held` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G18_no_op_claims_held` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G1_held_is_listed` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 7 | killed |
| `u101.G20_summary_held_empty` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 5 | killed |
| `u101.G2_judged_per_release` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 10 | killed |
| `u101.G3_all_labels_one_group` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 4 | killed |
| `u101.G4_unlabelled_grouped_together` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G5_unread_label_judged` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G6_unread_from_every_label` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 2 | killed |
| `u101.G7_mixed_is_a_genre` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G8_case_is_a_difference` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G9_mapping_row_unread` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u75-a.A1_kind_filter` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u75-a.A3_nothing_accepted_before_the_catalogue` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u75-a.A5_only_the_seams_exception_is_gone` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u75-a.A6_no_identifier_is_not_asked_of_the_provider` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u75-a.A7_each_row_read_alone` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u75-b.B11_write_failure_is_the_verbs_refusal` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u75-b.B1_outage_threshold` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u75-b.B3_only_a_provider_failure_counts` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u75-b.B7_same_recording_listed_once` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u75-b.B9_name_digests_the_provenance` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 2 | killed |
| `u75-zeros.B6_missing_and_nothing_listable_refuses` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `r840-a.A1_address_is_the_whole_field` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 2 | killed |
| `r840-a.A2_a_name_is_not_asked_about` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 6 | killed |
| `r840-a.A3_unreadable_verdict_is_decided` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 1 | killed |
| `r840-a.A4_only_label_releases` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 1 | killed |
| `r840-a.A5_no_identifier_is_not_read` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 1 | killed |
| `r840-a.A6_another_items_release_is_not_read` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 2 | killed |
| `r840-a.A7_catalogue_opened_on_demand` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 2 | killed |
| `r840-a.A8_outage_bound` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 1 | killed |
| `r840-a.A9_an_answer_resets_the_count` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 2 | killed |
| `r840-b.B10_unaddressed_is_keyed_by_item` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 1 | killed |
| `r840-b.B11_left_counts_what_was_not_reached` | `src/cratekit/label/artists_cli.py` | maintainer | 1 file(s) | 61 | 6 | killed |
| `r840-b.B1_only_the_seams_exception_is_not_served` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 1 | killed |
| `r840-b.B2_a_refusal_stops_the_run` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 1 | killed |
| `r840-b.B3_no_name_never_blanks` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 2 | killed |
| `r840-b.B4_an_unread_release_refuses` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 2 | killed |
| `r840-b.B5_decided_meanwhile_is_not_fine` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 2 | killed |
| `r840-b.B6_put_right_meanwhile_is_kept` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 2 | killed |
| `r840-b.B7_addresses_are_what_still_read_one` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 5 | killed |
| `r840-b.B8_only_the_artist_is_rewritten` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 3 | killed |
| `r840-b.B9_a_refusal_carries_why_each_read_failed` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 2 | killed |
| `r504-a.A10_block_listed` | `src/cratekit/label/catalogue.py` | user | 1 file(s) | 40 | 4 | killed |
| `r504-a.A8_withheld_sign` | `src/cratekit/label/catalogue.py` | user | 1 file(s) | 40 | 4 | killed |
| `r504-a.A9_summary_reworded` | `src/cratekit/label/catalogue.py` | user | 1 file(s) | 40 | 3 | killed |
| `r815-a.G2_forgetting_keeps_the_failure_count` | `src/cratekit/label/catalogue.py` | user | 1 file(s) | 76 | 2 | killed |
| `u308.L4_translated_swallows_refusal` | `src/cratekit/label/catalogue.py` | user | 1 file(s) | 31 | 1 | killed |
| `r1634.M16_worker_drops_how` | `src/cratekit/label/cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `r290-author.S06_label_call_removed` | `src/cratekit/label/cli.py` | user | 1 file(s) | 126 | 11 | killed |
| `r790-b.L1_guard_counts_held` | `src/cratekit/label/cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `r790-b.L2_round_records_beyond` | `src/cratekit/label/cli.py` | user | 1 file(s) | 40 | 8 | killed |
| `r790-b.L3_set_passes_offer` | `src/cratekit/label/cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `r790-b.L4_bound_is_said` | `src/cratekit/label/cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u177.A10_clear_word` | `src/cratekit/label/cli.py` | user | 1 file(s) | 28 | 1 | killed |
| `u177.A11_field_flag_guard` | `src/cratekit/label/cli.py` | user | 1 file(s) | 28 | 4 | killed |
| `u177.A9_add_drops_account` | `src/cratekit/label/cli.py` | user | 1 file(s) | 28 | 12 | killed |
| `u178.G6_fallback_refusal` | `src/cratekit/label/cli.py` | user | 1 file(s) | 64 | 1 | killed |
| `u178.G7_fallback_confirm_ignored` | `src/cratekit/label/cli.py` | user | 1 file(s) | 64 | 1 | killed |
| `u178.G8_clear_word_case` | `src/cratekit/label/cli.py` | user | 1 file(s) | 64 | 1 | killed |
| `u178.G9_accept_without_genre` | `src/cratekit/label/cli.py` | user | 1 file(s) | 64 | 1 | killed |
| `u277.M11_worker_detail_without_canary` | `src/cratekit/label/cli.py` | user | 1 file(s) | 37 | 3 | killed |
| `u277.M12_worker_message_without_canary` | `src/cratekit/label/cli.py` | user | 1 file(s) | 37 | 2 | killed |
| `u117-operator.D10_no_folder_refusal` | `src/cratekit/label/dated.py` | user | 1 file(s) | 24 | 1 | killed |
| `u117-operator.D11_part_way_named` | `src/cratekit/label/dated.py` | user | 1 file(s) | 24 | 2 | killed |
| `u117-operator.D12_move_into_folder` | `src/cratekit/label/dated.py` | user | 1 file(s) | 24 | 8 | killed |
| `u117-operator.D15_playable_only` | `src/cratekit/label/dated.py` | user | 1 file(s) | 24 | 1 | killed |
| `u117-operator.D16_recorded_before_move` | `src/cratekit/label/dated.py` | user | 1 file(s) | 24 | 1 | killed |
| `u117-operator.D1_heard_left_out` | `src/cratekit/label/dated.py` | user | 1 file(s) | 24 | 1 | killed |
| `u117-operator.D2_unsettled_taken` | `src/cratekit/label/dated.py` | user | 1 file(s) | 24 | 1 | killed |
| `u117-operator.D4_local_day` | `src/cratekit/label/dated.py` | user | 1 file(s) | 24 | 2 | killed |
| `u117-operator.D5_reuse_by_name` | `src/cratekit/label/dated.py` | user | 1 file(s) | 24 | 5 | killed |
| `u117-operator.D6_reuse_adds_only_missing` | `src/cratekit/label/dated.py` | user | 1 file(s) | 24 | 4 | killed |
| `u117-operator.D7_ambiguous` | `src/cratekit/label/dated.py` | user | 1 file(s) | 24 | 1 | killed |
| `u117-operator.D8_age_bound` | `src/cratekit/label/dated.py` | user | 1 file(s) | 24 | 2 | killed |
| `u117-operator.D9_age_configured` | `src/cratekit/label/dated.py` | user | 1 file(s) | 24 | 1 | killed |
| `u123.D1_dated_create_vouched` | `src/cratekit/label/dated.py` | user | 1 file(s) | 38 | 13 | killed |
| `u191.M21_unsettled_answers_read` | `src/cratekit/label/dated.py` | user | 1 file(s) | 24 | 1 | killed |
| `u308.L2_part_way_again_dropped` | `src/cratekit/label/dated.py` | user | 1 file(s) | 24 | 1 | killed |
| `u308.L3_part_way_reason_lost` | `src/cratekit/label/dated.py` | user | 1 file(s) | 24 | 1 | killed |
| `r798-b.G1_an_unread_answer_holds_nothing` | `src/cratekit/label/gate.py` | user | 1 file(s) | 141 | 4 | killed |
| `r798-b.G2_a_would_be_hold_is_asked_about_again` | `src/cratekit/label/gate.py` | user | 1 file(s) | 141 | 3 | killed |
| `r815-a.G1_the_asking_gives_up_at_the_bound` | `src/cratekit/label/gate.py` | user | 2 file(s) | 217 | 3 | killed |
| `u110-c.C4_go_tail` | `src/cratekit/label/go.py` | user | 1 file(s) | 20 | 1 | killed |
| `r1890.P10_heard_path_imports_a_writer_part` | `src/cratekit/label/heard.py` | user | 1 file(s) | 38 | 1 | killed |
| `u123.H10_year_filter` | `src/cratekit/label/heard.py` | user | 1 file(s) | 38 | 3 | killed |
| `u123.H11_day_filter` | `src/cratekit/label/heard.py` | user | 1 file(s) | 38 | 2 | killed |
| `u123.H12_newly_excludes_heard` | `src/cratekit/label/heard.py` | user | 1 file(s) | 38 | 2 | killed |
| `u123.H13_year_shape` | `src/cratekit/label/heard.py` | user | 1 file(s) | 38 | 1 | killed |
| `u123.H14_ambiguous_bound` | `src/cratekit/label/heard.py` | user | 1 file(s) | 38 | 1 | killed |
| `u123.H15_no_year_refusal` | `src/cratekit/label/heard.py` | user | 1 file(s) | 38 | 1 | killed |
| `u123.H1_outside_refusal` | `src/cratekit/label/heard.py` | user | 1 file(s) | 38 | 2 | killed |
| `u123.H2_no_releases_refusal` | `src/cratekit/label/heard.py` | user | 1 file(s) | 38 | 1 | killed |
| `u123.H3_vouched_before_a_write` | `src/cratekit/label/heard.py` | user | 1 file(s) | 38 | 1 | killed |
| `u123.H4_unheard_tracks_stay` | `src/cratekit/label/heard.py` | user | 1 file(s) | 38 | 1 | killed |
| `u123.H5_missing_holds_the_removal` | `src/cratekit/label/heard.py` | user | 1 file(s) | 38 | 1 | killed |
| `u123.H6_heard_recorded` | `src/cratekit/label/heard.py` | user | 1 file(s) | 38 | 7 | killed |
| `u123.H7_year_adds_recorded` | `src/cratekit/label/heard.py` | user | 1 file(s) | 38 | 1 | killed |
| `u123.H8_prefixed_year` | `src/cratekit/label/heard.py` | user | 1 file(s) | 38 | 1 | killed |
| `u123.H9_stray_said` | `src/cratekit/label/heard.py` | user | 1 file(s) | 38 | 1 | killed |
| `u123.C1_declined_writes_nothing` | `src/cratekit/label/heard_cli.py` | user | 1 file(s) | 38 | 1 | killed |
| `r798-c.H3_every_name_is_resolved_before_any_is_filed` | `src/cratekit/label/held_cli.py` | user | 1 file(s) | 141 | 1 | killed |
| `r798-c.H4_a_release_with_no_isrc_was_not_asked_about` | `src/cratekit/label/held_cli.py` | user | 1 file(s) | 141 | 1 | killed |
| `r798-c.H5_a_returned_hold_is_marked` | `src/cratekit/label/held_cli.py` | user | 1 file(s) | 141 | 2 | killed |
| `r815-b.H1_a_withheld_release_returns_under_no_invented_run` | `src/cratekit/label/held_cli.py` | user | 1 file(s) | 76 | 1 | killed |
| `r815-b.H2_the_withheld_word_stays_with_the_hold` | `src/cratekit/label/held_cli.py` | maintainer | 1 file(s) | 76 | 2 | killed |
| `r815-b.H3_a_judge_runs_answer_is_not_the_sweeps` | `src/cratekit/label/held_cli.py` | user | 1 file(s) | 76 | 1 | killed |
| `r815-b.J1_one_refusal_ends_the_asking` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 1 | killed |
| `r815-b.J2_an_unread_catalogue_ends_the_run` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 1 | killed |
| `r815-b.J3_a_failing_provider_ends_the_run` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 1 | killed |
| `r815-b.J4_a_record_never_holds_on_its_own` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 3 | killed |
| `r815-c.J11_the_scope_reads_the_registry` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 1 | killed |
| `r815-c.J12_a_release_held_and_gone_is_counted_held` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 3 | killed |
| `r815-c.J13_the_refusal_carries_the_counts` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 7 | killed |
| `r815-c.J5_a_recorded_no_word_answer_is_not_asked_again` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 4 | killed |
| `r815-c.J6_a_decided_item_is_not_judged` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 2 | killed |
| `r815-c.J7_a_returned_release_is_not_judged` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 1 | killed |
| `r815-c.J8_a_refusal_parks_and_fails_no_item` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 5 | killed |
| `r815-c.J9_a_park_drops_the_jobs_tools` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 3 | killed |
| `r840-c.C5_the_judging_stamp_is_made_on_the_payload_as_it_stands` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 1 | killed |
| `u217.K11_asked_now_counted_as_reused` | `src/cratekit/label/kept_listing.py` | user | 1 file(s) | 38 | 4 | killed |
| `u217.K12_flush_batch` | `src/cratekit/label/kept_listing.py` | maintainer | 1 file(s) | 38 | 1 | killed |
| `u217.K1_life_boundary` | `src/cratekit/label/kept_listing.py` | user | 1 file(s) | 38 | 1 | killed |
| `u217.K2_future_is_fresh` | `src/cratekit/label/kept_listing.py` | maintainer | 1 file(s) | 38 | 1 | killed |
| `u217.K3_life_coefficient` | `src/cratekit/label/kept_listing.py` | user | 1 file(s) | 38 | 1 | killed |
| `u217.K4_changed_entry` | `src/cratekit/label/kept_listing.py` | user | 1 file(s) | 38 | 2 | killed |
| `u217.K5_seeds_not_asked_for` | `src/cratekit/label/kept_listing.py` | user | 1 file(s) | 38 | 1 | killed |
| `u217.K6_match_not_asked_for` | `src/cratekit/label/kept_listing.py` | user | 1 file(s) | 38 | 1 | killed |
| `u217.K9_release_shape` | `src/cratekit/label/kept_listing.py` | user | 1 file(s) | 38 | 1 | killed |
| `u217.K10_naive_instant` | `src/cratekit/label/kept_reads.py` | maintainer | 1 file(s) | 38 | 1 | killed |
| `u217.K13_unkept_said` | `src/cratekit/label/kept_reads.py` | user | 1 file(s) | 38 | 1 | killed |
| `u308.L9_store_flushes_nothing` | `src/cratekit/label/kept_reads.py` | user | 1 file(s) | 38 | 20 | killed |
| `r1056.N10_pass_not_required` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `r1056.N1_no_refusal_of_an_unreadable_record` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 34 | 7 | killed |
| `r1056.N2_first_landing_only` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `r1056.N3_years_from_the_argument` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `r1056.N4_no_landings_in_digest` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 34 | 2 | killed |
| `r1056.N5_no_reread_before_rename` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `r1056.N6_no_nothing_filed_warning` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 34 | 4 | killed |
| `r1056.N7_nothing_filed_against_any_year` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `r1056.N8_shown_pass_bare` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `r1056.N9_verb_not_threaded` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 34 | 6 | killed |
| `r835-b.M1_only_the_batch_years_marked` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `r835-b.M5_deleted_folder_said` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `r835-c.M4_recheck_before_rename_again` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `r1091.P6_kept_gone_read_as_release` | `src/cratekit/label/playlists_cli.py` | user | 1 file(s) | 56 | 29 | killed |
| `r835-b.P2_nothing_confirmed_refused` | `src/cratekit/label/playlists_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `r835-c.P3_unplayable_track_never_asked_again` | `src/cratekit/label/playlists_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `u191.M13_gone_refused` | `src/cratekit/label/playlists_cli.py` | user | 1 file(s) | 56 | 35 | killed |
| `u191.M19_unread_listing_accepted` | `src/cratekit/label/playlists_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `u217.S3_playlists_line` | `src/cratekit/label/playlists_cli.py` | user | 1 file(s) | 38 | 1 | killed |
| `r1476.M20_named_first_only` | `src/cratekit/label/registry.py` | user | 1 file(s) | 64 | 7 | killed |
| `r790-c.G1_offer_bounded_by_limit` | `src/cratekit/label/registry.py` | user | 1 file(s) | 40 | 1 | killed |
| `r790-c.G2_entry_overrides` | `src/cratekit/label/registry.py` | user | 1 file(s) | 40 | 4 | killed |
| `r790-c.G3_offer_floor` | `src/cratekit/label/registry.py` | user | 1 file(s) | 40 | 1 | killed |
| `r790-c.G4_offer_read_back` | `src/cratekit/label/registry.py` | user | 1 file(s) | 40 | 5 | killed |
| `r790-c.G5_rename_keeps_offer` | `src/cratekit/label/registry.py` | user | 1 file(s) | 40 | 1 | killed |
| `u177.A1_account_suffix` | `src/cratekit/label/registry.py` | user | 1 file(s) | 28 | 8 | killed |
| `u177.A2_account_shape` | `src/cratekit/label/registry.py` | user | 1 file(s) | 28 | 4 | killed |
| `u177.A3_account_case` | `src/cratekit/label/registry.py` | user | 1 file(s) | 28 | 4 | killed |
| `u177.A4_claim_removed` | `src/cratekit/label/registry.py` | user | 1 file(s) | 28 | 2 | killed |
| `u177.A5_claim_self` | `src/cratekit/label/registry.py` | user | 1 file(s) | 28 | 1 | killed |
| `u177.A6_first_of_two` | `src/cratekit/label/registry.py` | user | 1 file(s) | 28 | 1 | killed |
| `u177.A7_stored_raw` | `src/cratekit/label/registry.py` | user | 1 file(s) | 28 | 2 | killed |
| `u177.A8_edit_drops_account` | `src/cratekit/label/registry.py` | user | 1 file(s) | 28 | 2 | killed |
| `u178.G1_genre_length_bound` | `src/cratekit/label/registry.py` | user | 1 file(s) | 64 | 1 | killed |
| `u178.G2_genre_needs_a_letter` | `src/cratekit/label/registry.py` | user | 1 file(s) | 64 | 1 | killed |
| `u178.G3_genre_one_line` | `src/cratekit/label/registry.py` | user | 1 file(s) | 64 | 1 | killed |
| `u178.G4_edit_clear_genre` | `src/cratekit/label/registry.py` | user | 1 file(s) | 64 | 1 | killed |
| `u178.G5_edit_none_keeps_genre` | `src/cratekit/label/registry.py` | user | 1 file(s) | 64 | 1 | killed |
| `u308.L7_clear_ignored` | `src/cratekit/label/registry.py` | user | 1 file(s) | 64 | 1 | killed |
| `u308.L8_offer_unchecked` | `src/cratekit/label/registry.py` | user | 1 file(s) | 40 | 1 | killed |
| `u308.L5_extended_step_dropped` | `src/cratekit/label/review_common.py` | user | 2 file(s) | 137 | 6 | killed |
| `u308.L6_ended_outcome_ignored` | `src/cratekit/label/review_common.py` | user | 3 file(s) | 259 | 17 | killed |
| `r1634.M10_basis_always_line` | `src/cratekit/label/sweep.py` | user | 1 file(s) | 37 | 1 | killed |
| `r1634.M13_rereader_unguarded` | `src/cratekit/label/sweep.py` | user | 1 file(s) | 37 | 1 | killed |
| `r1634.M14_rereader_beside_a_bare_verifier` | `src/cratekit/label/sweep.py` | maintainer | 1 file(s) | 37 | 1 | killed |
| `r1634.M15_how_reworded` | `src/cratekit/label/sweep.py` | user | 1 file(s) | 37 | 5 | killed |
| `r1634.M18_basis_not_in_detail` | `src/cratekit/label/sweep.py` | user | 1 file(s) | 37 | 1 | killed |
| `r1634.M19_another_act_replaces_a_gone_one` | `src/cratekit/label/sweep.py` | user | 1 file(s) | 37 | 1 | killed |
| `r1634.M1_mismatch_mode_always` | `src/cratekit/label/sweep.py` | user | 1 file(s) | 37 | 14 | killed |
| `r1634.M20_in_place_note_dropped` | `src/cratekit/label/sweep.py` | user | 1 file(s) | 37 | 1 | killed |
| `r1634.M2_mismatch_mode_never` | `src/cratekit/label/sweep.py` | user | 1 file(s) | 37 | 12 | killed |
| `r1634.M3_forced_read_dropped` | `src/cratekit/label/sweep.py` | user | 3 file(s) | 218 | 16 | killed |
| `r1634.M4_no_read_confirms` | `src/cratekit/label/sweep.py` | user | 1 file(s) | 37 | 2 | killed |
| `r1634.M5_no_read_asks_the_line` | `src/cratekit/label/sweep.py` | user | 1 file(s) | 37 | 2 | killed |
| `r1634.M6_gone_not_passed_over` | `src/cratekit/label/sweep.py` | user | 1 file(s) | 37 | 3 | killed |
| `r1634.M7_any_answer_passed_over` | `src/cratekit/label/sweep.py` | user | 1 file(s) | 37 | 6 | killed |
| `r1634.M8_order_label_line_first` | `src/cratekit/label/sweep.py` | user | 1 file(s) | 37 | 4 | killed |
| `r1634.M9_order_other_act_before_label` | `src/cratekit/label/sweep.py` | user | 1 file(s) | 37 | 5 | killed |
| `r790-a.S2_held_is_not_refiled` | `src/cratekit/label/sweep.py` | user | 1 file(s) | 40 | 3 | killed |
| `r790-a.S4_default_is_the_offer` | `src/cratekit/label/sweep.py` | user | 1 file(s) | 40 | 10 | killed |
| `r790-b.S7_first_run_kept` | `src/cratekit/label/sweep.py` | user | 1 file(s) | 40 | 1 | killed |
| `r798-b.G3_a_held_release_takes_a_place` | `src/cratekit/label/sweep.py` | user | 1 file(s) | 141 | 2 | killed |
| `r798-b.G4_a_returned_hold_is_never_judged` | `src/cratekit/label/sweep.py` | user | 1 file(s) | 141 | 1 | killed |
| `r798-b.G5_deleted_on_purpose_outranks_held` | `src/cratekit/label/sweep.py` | user | 1 file(s) | 141 | 1 | killed |
| `r798-b.G6_a_released_hold_the_library_owns_is_dropped` | `src/cratekit/label/sweep.py` | user | 1 file(s) | 141 | 1 | killed |
| `r798-b.G8_a_standing_hold_counts_for_the_canary` | `src/cratekit/label/sweep.py` | user | 1 file(s) | 141 | 1 | killed |
| `r815-b.S1_a_sweep_keeps_a_withheld_hold` | `src/cratekit/label/sweep.py` | user | 1 file(s) | 76 | 1 | killed |
| `u217.S1_summary_dropped` | `src/cratekit/label/sweep.py` | user | 1 file(s) | 38 | 3 | killed |
| `u238.M4_beyond_leaves_out_unchecked` | `src/cratekit/label/sweep.py` | user | 1 file(s) | 40 | 15 | killed |
| `u238.M5_window_edge_off_by_one` | `src/cratekit/label/sweep.py` | user | 1 file(s) | 40 | 12 | killed |
| `u238.M6_needle_ignored` | `src/cratekit/label/sweep.py` | user | 1 file(s) | 40 | 1 | killed |
| `u277.M2_no_line_before_the_labels_line` | `src/cratekit/label/sweep.py` | user | 1 file(s) | 37 | 2 | killed |
| `u277.M3_another_label_before_no_line` | `src/cratekit/label/sweep.py` | user | 2 file(s) | 77 | 10 | killed |
| `u277.M4_canary_answer_ignored` | `src/cratekit/label/sweep.py` | user | 3 file(s) | 218 | 17 | killed |
| `u277.M5_only_a_mismatch_is_unconfirmed` | `src/cratekit/label/sweep.py` | user | 3 file(s) | 218 | 14 | killed |
| `u277.M6_canary_asked_beside_candidates` | `src/cratekit/label/sweep.py` | maintainer | 1 file(s) | 37 | 1 | killed |
| `u277.M7_standing_hold_not_a_canary` | `src/cratekit/label/sweep.py` | user | 1 file(s) | 141 | 1 | killed |
| `u277.M8_past_window_counts_other_labels` | `src/cratekit/label/sweep.py` | user | 1 file(s) | 40 | 3 | killed |
| `u277.M9_canary_notes_dropped` | `src/cratekit/label/sweep.py` | user | 1 file(s) | 37 | 5 | killed |
| `u52-item-derivation.A3_label_source_acquires` | `src/cratekit/label/sweep.py` | user | 1 file(s) | 31 | 2 | killed |
| `r1634.M17_check_drops_how` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 37 | 5 | killed |
| `u277.M10_next_says_no_canary` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 37 | 12 | killed |
| `r1634.M11_reread_reads_the_line` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 37 | 15 | killed |
| `r1634.M12_gone_confirms` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 37 | 6 | killed |
| `u206.M18_catalogue_keeps_any_gone` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 60 | 2 | killed |
| `u207.A2_catalogue_ignores_screen` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 32 | 1 | killed |
| `u217.A1_flush_on_the_way_out` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 38 | 12 | killed |
| `u217.A2_roster_lists_now` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 38 | 6 | killed |
| `u217.A3_listing_not_kept` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 38 | 12 | killed |
| `u217.A4_search_not_kept` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 38 | 10 | killed |
| `u217.A5_name_not_kept` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 38 | 1 | killed |
| `u217.A6_need_object` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 38 | 1 | killed |
| `u217.A7_missing_method_kept` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 38 | 1 | killed |
| `u217.A8_member_read_uncounted` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 38 | 1 | killed |
| `u105-b.S1_parts_only_when_several` | `src/cratekit/master/cli.py` | user | 1 file(s) | 2 | 2 | killed |
| `u46-round-2.M6_staging_not_cleared` | `src/cratekit/master/cli.py` | user | 1 file(s) | 2 | 1 | killed |
| `r395.M1_no_pipx_detection` | `src/cratekit/modules/extras.py` | user | 1 file(s) | 13 | 12 | killed |
| `r395.M2_bare_pip` | `src/cratekit/modules/extras.py` | user | 1 file(s) | 13 | 1 | killed |
| `r395.M4_no_force` | `src/cratekit/modules/extras.py` | user | 1 file(s) | 13 | 8 | killed |
| `r395.M5_trust_missing_source` | `src/cratekit/modules/extras.py` | user | 1 file(s) | 13 | 3 | killed |
| `r395.M6_always_dot` | `src/cratekit/modules/extras.py` | user | 1 file(s) | 13 | 2 | killed |
| `r395.M7_fallback_drops_extras` | `src/cratekit/modules/extras.py` | user | 1 file(s) | 13 | 1 | killed |
| `u181.E1_direct_reference_unread` | `src/cratekit/modules/extras.py` | user | 1 file(s) | 13 | 3 | killed |
| `u181.E2_direct_reference_drops_extras` | `src/cratekit/modules/extras.py` | user | 1 file(s) | 13 | 1 | killed |
| `u311.D2_empty_extra_kept` | `src/cratekit/modules/extras.py` | user | 1 file(s) | 13 | 4 | killed |
| `u192.F6_queue_only_never` | `src/cratekit/modules/foreground.py` | user | 1 file(s) | 64 | 2 | killed |
| `u192.F7_queue_only_always` | `src/cratekit/modules/foreground.py` | user | 1 file(s) | 64 | 1 | killed |
| `r835-a.F12_refused_tracks_recorded` | `src/cratekit/modules/outbound/folders.py` | user | 1 file(s) | 56 | 1 | killed |
| `r835-a.F2_two_root_folders_refuse` | `src/cratekit/modules/outbound/folders.py` | user | 1 file(s) | 56 | 1 | killed |
| `r835-a.F3_root_folder_adopted_by_name` | `src/cratekit/modules/outbound/folders.py` | user | 1 file(s) | 56 | 3 | killed |
| `r835-a.F4_recorded_and_refused_not_asked_again` | `src/cratekit/modules/outbound/folders.py` | user | 1 file(s) | 56 | 5 | killed |
| `r835-a.F5_unplaced_recorded_year_is_moved` | `src/cratekit/modules/outbound/folders.py` | user | 1 file(s) | 56 | 2 | killed |
| `r835-c.F1_recorded_folder_must_be_listed_again` | `src/cratekit/modules/outbound/folders.py` | user | 1 file(s) | 56 | 1 | killed |
| `r835-c.F7_only_a_provider_failure_is_unreadable_again` | `src/cratekit/modules/outbound/folders.py` | user | 1 file(s) | 56 | 1 | killed |
| `r835-c.F8_marked_title_matches_by_name_again` | `src/cratekit/modules/outbound/folders.py` | user | 1 file(s) | 56 | 1 | killed |
| `r835-a.L1_load_carries_the_label_map` | `src/cratekit/modules/outbound/ledger.py` | user | 1 file(s) | 56 | 28 | killed |
| `r837-a.A8_load_carries_sets` | `src/cratekit/modules/outbound/ledger.py` | user | 1 file(s) | 63 | 20 | killed |
| `u123.L1_dated_vouched` | `src/cratekit/modules/outbound/ledger.py` | user | 1 file(s) | 38 | 20 | killed |
| `u123.L3_malformed_entry_dropped` | `src/cratekit/modules/outbound/ledger.py` | maintainer | 1 file(s) | 38 | 1 | killed |
| `r835-a.L3_recorded_year_never_created_again` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 1 file(s) | 56 | 4 | killed |
| `r837-a.A7_reserve_reuses_recorded` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 2 file(s) | 119 | 5 | killed |
| `u140.B1_ledger_folds_into_a_twin` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 1 file(s) | 29 | 1 | killed |
| `u140.B2_ledger_moves_another_id` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 1 file(s) | 29 | 1 | killed |
| `u309.U4_reserve_recorded_wins` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 2 file(s) | 119 | 5 | killed |
| `u309.U5_reserve_written` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 157 | 71 | killed |
| `u123.L2_forget_drops_the_entry` | `src/cratekit/modules/outbound/ledger_settle.py` | user | 1 file(s) | 38 | 2 | killed |
| `u207.M1_mirror_screens_settled_rows` | `src/cratekit/modules/outbound/mirror.py` | user | 1 file(s) | 32 | 1 | killed |
| `u207.M2_mirror_counts_a_screen_as_one` | `src/cratekit/modules/outbound/mirror.py` | user | 1 file(s) | 32 | 1 | killed |
| `u214.M8_plan_left_lines` | `src/cratekit/modules/outbound/mirror.py` | user | 1 file(s) | 27 | 4 | killed |
| `r1017.M10_older_beats_to` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 29 | 2 | killed |
| `r1017.M8_first_older_name_only` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 29 | 2 | killed |
| `r1017.M9_twin_only_beside_to` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 29 | 2 | killed |
| `r837-a.A11_year_folder_adopted` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 63 | 2 | killed |
| `r837-a.A12_in_folder_not_moved` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 63 | 3 | killed |
| `r837-a.A14_not_listed_not_blamed` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 63 | 1 | killed |
| `r837-a.A1_no_record_creates` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 63 | 4 | killed |
| `r837-a.A2_asked_not_asked_again` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 63 | 2 | killed |
| `r837-a.A4_nothing_matched_writes_nothing` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 63 | 3 | killed |
| `r837-a.A5_chunk_recorded` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 63 | 3 | killed |
| `r837-a.A6_refused_split` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 63 | 1 | killed |
| `r837-b.A3r_held_not_added` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 63 | 1 | killed |
| `r837-b.A9r_recorded_folder_listed` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 63 | 2 | killed |
| `u140.A2_new_name_record_ignored` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 29 | 6 | killed |
| `u140.A3_refreeze_against_account_spelling` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 29 | 1 | killed |
| `u140.A4_rename_always` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 29 | 4 | killed |
| `u140.A5_ledger_never_rekeyed` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 29 | 9 | killed |
| `u140.A6_refreeze_account_spelling` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 29 | 1 | killed |
| `u142.S1_folder_prefix` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 63 | 5 | killed |
| `u142.S2_plan_reads_the_year_key` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 63 | 1 | killed |
| `u142.S4_ambiguity_bound` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 63 | 1 | killed |
| `u142.S5_create_under_the_year` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 63 | 1 | killed |
| `u142.S6_reserve_under_the_year` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 63 | 1 | killed |
| `u142.S7_adoption_is_a_write` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 63 | 1 | killed |
| `r228-operator.D10_pink_warning_gone` | `src/cratekit/modules/outbound/shell.py` | user | 1 file(s) | 13 | 1 | killed |
| `r290-author.S13_outbound_shell_call_removed` | `src/cratekit/modules/outbound/shell.py` | user | 1 file(s) | 126 | 11 | killed |
| `r1308.M10_count_unchecked` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 23236 | 0 (promoted) | zero |
| `r835-b.T1_folder_create_never_retried` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 56 | 1 | killed |
| `r835-b.T2_refused_move_raised` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 56 | 1 | killed |
| `r835-c.T3_short_answer_read_again_again` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 56 | 1 | killed |
| `r836-a.A1_product_made_asked_first` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 38 | 1 | killed |
| `u123.T1_adapter_vouching` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 38 | 1 | killed |
| `u123.T2_read_back` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 38 | 2 | killed |
| `u123.T3_already_gone` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 38 | 2 | killed |
| `u143-d.A5_playlist_read_back` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 38 | 2 | killed |
| `u309.U11_delete_read_back` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 38 | 2 | killed |
| `u309.U9_delete_answered_false` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 38 | 3 | killed |
| `r1313.T1_account_skips_the_classifier` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 1 file(s) | 60 | 1 | killed |
| `u206.M14_account_keeps_invalid_isrc` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 1 file(s) | 60 | 2 | killed |
| `u206.M17_account_hit_ignored` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 1 file(s) | 60 | 13 | killed |
| `r1761.P9_emptied_passes_on_the_fact_file` | `src/cratekit/modules/tools/backup_proof.py` | user | 1 file(s) | 57 | 1 | killed |
| `u311.C5_binaries_out_of_order` | `src/cratekit/modules/tools/mastering.py` | user | 1 file(s) | 2 | 2 | killed |
| `u117-operator.D14_organize_call` | `src/cratekit/organize/account.py` | user | 1 file(s) | 24 | 3 | killed |
| `u214.M10_detail_names` | `src/cratekit/organize/account_mirror.py` | user | 1 file(s) | 27 | 4 | killed |
| `u214.M9_inbox_unmirrored` | `src/cratekit/organize/account_mirror.py` | user | 1 file(s) | 27 | 2 | killed |
| `u246.S16_inspiration_held_per_element` | `src/cratekit/organize/inspiration.py` | maintainer | 1 file(s) | 33 | 1 | killed |
| `u214.M11_frozen_carries` | `src/cratekit/organize/mirror_frozen.py` | user | 1 file(s) | 27 | 6 | killed |
| `r1255.R5_organize_rotation_warns` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 27 | 1 | killed |
| `u214.M14_old_not_yours` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 27 | 2 | killed |
| `u309.U24_planned_step_apply_bound` | `src/cratekit/organize/steps.py` | user | 1 file(s) | 24 | 1 | killed |
| `u27-restore-cli-independent.I_C4_the_session_identifier_becomes_required` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 1021 | 3 | killed |
| `r835-c.S2_sync_hands_the_ledger_to_the_sweep_again` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `r837-a.A17_sweep_hand_off` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 63 | 1 | killed |
| `r1056.S1_no_landing_step_names_intake_missing` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 34 | 4 | killed |
| `r1056.S2_unreachable_step_names_sync` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `r777.N3_engine_unchecked` | `src/cratekit/sync/marks.py` | user | 1 file(s) | 31 | 1 | killed |
| `u246.S13_pair_cli_per_element` | `src/cratekit/sync/pair_check.py` | maintainer | 1 file(s) | 33 | 1 | killed |
| `u304.S3_agreement_clock_through_its_module` | `src/cratekit/sync/pair_plan.py` | maintainer | 1 file(s) | 23236 | 0 (promoted) | zero |
| `r361-a.A10_enum_value_respelled` | `src/cratekit/sync/playlists.py` | user | 1 file(s) | 31 | 1 | killed |
| `r361-a.A2_case_insensitive` | `src/cratekit/sync/playlists.py` | user | 1 file(s) | 31 | 1 | killed |
| `r361-a.A3_no_leading_space` | `src/cratekit/sync/playlists.py` | user | 1 file(s) | 31 | 1 | killed |
| `r361-a.A4_substring_not_suffix` | `src/cratekit/sync/playlists.py` | user | 1 file(s) | 31 | 1 | killed |
| `r361-a.D2_drop_the_placeholder` | `src/cratekit/sync/playlists.py` | user | 1 file(s) | 31 | 1 | killed |
| `r361-a.D3_drop_in_flight` | `src/cratekit/sync/playlists.py` | user | 1 file(s) | 31 | 1 | killed |
| `r835-b.S1_built_year_excluded_from_sweep` | `src/cratekit/sync/playlists.py` | user | 1 file(s) | 56 | 1 | killed |
| `r837-a.A16_sweep_excludes_set` | `src/cratekit/sync/playlists.py` | user | 1 file(s) | 63 | 1 | killed |
| `u113-a.A6_sweep_passes_no_name` | `src/cratekit/sync/playlists.py` | user | 1 file(s) | 26 | 1 | killed |
| `r704-a.R1_increment_ignores_the_flag` | `src/cratekit/sync/run.py` | user | 1 file(s) | 31 | 1 | killed |
| `r704-a.R2_rate_limit_not_retryable` | `src/cratekit/sync/run.py` | user | 1 file(s) | 31 | 1 | killed |
| `r704-a.R3_remedy_retry_later` | `src/cratekit/sync/run.py` | user | 1 file(s) | 31 | 1 | killed |
| `r704-a.R4_detail_unmarked` | `src/cratekit/sync/run.py` | user | 1 file(s) | 31 | 1 | killed |
| `r704-a.R5_flag_not_stored` | `src/cratekit/sync/run.py` | user | 1 file(s) | 31 | 1 | killed |
| `r704-a.R6_sentence_reworded` | `src/cratekit/sync/run.py` | user | 1 file(s) | 31 | 1 | killed |
| `u52-item-derivation.A1_acquires_early_return_gone` | `src/cratekit/sync/run.py` | user | 1 file(s) | 31 | 3 | killed |
| `u52-item-derivation.A2_acquires_default_false` | `src/cratekit/sync/run.py` | user | 1 file(s) | 31 | 6 | killed |
| `r259.S1_scope_owned_sample` | `src/cratekit/sync/scope.py` | maintainer | 1 file(s) | 31 | 1 | killed |
| `r263.S2_favorites_reason` | `src/cratekit/sync/sources.py` | user | 1 file(s) | 31 | 1 | killed |
| `u109-b.B3_no_cursor_reworded` | `src/cratekit/sync/sources.py` | user | 1 file(s) | 31 | 3 | killed |
| `u149.T21_landing_paired_again` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 5 | 1 | killed |
| `u149.T3_folder_names_unread` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 5 | 1 | killed |
| `u149.T5_held_name_counted_free` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 5 | 1 | killed |
| `u242.M22_unmark_releases_nothing` | `src/cratekit/sync/unmark_cli.py` | user | 2 file(s) | 119 | 2 | killed |
| `r263.W1_no_unrecorded_state` | `src/cratekit/sync/watermarks.py` | user | 1 file(s) | 31 | 4 | killed |
| `r263.W2_state_word` | `src/cratekit/sync/watermarks.py` | user | 1 file(s) | 31 | 3 | killed |
| `r263.W3_stale_record_as_completion` | `src/cratekit/sync/watermarks.py` | user | 1 file(s) | 31 | 1 | killed |

## Zero rows and what they owe

- `r1308.M10_count_unchecked` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u304.S3_agreement_clock_through_its_module` (maintainer facing): maintainer facing, composite not required

## Row definitions

### `u154.G4_stale_target_check_dropped`

a target made after the plan is renamed over at apply

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G4_stale_target_check_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_every_refusal_and_failure_leaves_the_batch_and_its_rows_as_they_were`

Old text:

```
    if os.path.lexists(one.target):
        raise refuse(
            "decision-stale",
            f"{one.target} exists now and did not when the plan was made, so nothing "

```

New text:

```
    if False:
        raise refuse(
            "decision-stale",
            f"{one.target} exists now and did not when the plan was made, so nothing "

```

### `u154.G5_unmatched_file_shelved_anyway`

a batch with a file the collection does not hold is moved anyway

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G5_unmatched_file_shelved_anyway`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_every_refusal_and_failure_leaves_the_batch_and_its_rows_as_they_were`

Old text:

```
        if unmatched is not None:
            leave(batch, _why_unmatched(*unmatched))
            continue

```

New text:

```
        if False:
            leave(batch, _why_unmatched(*unmatched))
            continue

```

### `u154.G6_subfolder_check_dropped`

a batch folder holding a subfolder is planned

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G6_subfolder_check_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_every_refusal_and_failure_leaves_the_batch_and_its_rows_as_they_were`

Old text:

```
        if any(entry.is_dir() for entry in folder.iterdir()):

```

New text:

```
        if False:

```

### `u154.G7_run_id_shape_unread`

a batch named for its run identifier fits neither shape

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G7_run_id_shape_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_run_identifier_named_batch_files_as_downloads_or_as_the_subject_given[four-hex-before-u235]`
  - `tests/test_intake_shelve.py::test_a_run_identifier_named_batch_files_as_downloads_or_as_the_subject_given[sixteen-hex-since-u235]`
  - `tests/test_intake_shelve.py::test_parse_name_reads_the_two_shapes_and_refuses_the_rest[2026-09-23T222241Z-4773-expected5]`
  - `tests/test_intake_shelve.py::test_parse_name_reads_the_two_shapes_and_refuses_the_rest[2026-11-07T164826Z-ce458ab7cceccb0b-expected6]`

Old text:

```
    run = _RUN_ID.match(batch)
    if run is not None:

```

New text:

```
    run = None
    if run is not None:

```

### `u154.G8_free_target_no_suffix`

a taken target is reused rather than given the next suffix

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G8_free_target_no_suffix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_row_under_the_target_refuses_the_commit_and_the_free_target_rule_passes_it_over`
  - `tests/test_intake_shelve.py::test_every_refusal_and_failure_leaves_the_batch_and_its_rows_as_they_were`
  - `tests/test_intake_shelve.py::test_two_batches_filing_to_one_name_get_two_and_a_taken_target_is_passed_over`

Old text:

```
    while os.path.lexists(candidate) or candidate in planned or spell(candidate) in stored_dirs:

```

New text:

```
    while False:

```

### `u154.R1_rows_under_target_not_consulted`

a target free on disk but holding collection rows is chosen

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `R1_rows_under_target_not_consulted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_row_under_the_target_refuses_the_commit_and_the_free_target_rule_passes_it_over`

Old text:

```
    while os.path.lexists(candidate) or candidate in planned or spell(candidate) in stored_dirs:

```

New text:

```
    while os.path.lexists(candidate) or candidate in planned:

```

### `u154.R3_repeated_name_planned_twice`

a batch named twice is planned twice

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `R3_repeated_name_planned_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_apply_moves_the_folder_rewrites_the_paths_keeps_the_rest_and_the_name_stays_taken`

Old text:

```
    wanted = _candidates(cfg) if everything else list(dict.fromkeys(names))

```

New text:

```
    wanted = _candidates(cfg) if everything else list(names)

```

### `u154.R6_device_probe_dropped`

a processed tree on another device is planned and renamed into

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `R6_device_probe_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_every_refusal_and_failure_leaves_the_batch_and_its_rows_as_they_were`

Old text:

```
    _assert_one_device(cfg, root)

```

New text:

```
    pass

```

### `u154.R7_exact_prefix_filter_dropped`

the confinement check judges the case blind LIKE result as is

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `R7_exact_prefix_filter_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_apply_moves_the_folder_rewrites_the_paths_keeps_the_rest_and_the_name_stays_taken`

Old text:

```
            if str(row[1] or "").startswith(one.stored_target + os.sep)

```

New text:

```
            if True

```

### `u164.T1_filed_target`

landing_target: land in the music folder's batch path rather than the filed folder

- File: `src/cratekit/intake/shelve.py`
- Source: `u164.json`, row `T1_filed_target`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_rehearse.py`, `tests/test_intake_shelve.py`
- Collected: 98 against a baseline of 98
- Kills: 33 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_filed_folder_on_another_device_is_refused_at_the_move`
  - `tests/test_intake_land_filed.py::test_a_folder_on_disk_or_one_the_collection_stores_rows_under_is_passed_over`
  - `tests/test_intake_land_filed.py::test_a_landing_on_the_27th_lands_in_its_year_folder_under_its_subject`
  - `tests/test_intake_land_filed.py::test_a_name_landed_into_again_goes_back_to_its_folder_unless_the_folder_is_gone`
  - `tests/test_intake_land_filed.py::test_a_name_that_is_a_date_alone_files_as_downloads`
  - `tests/test_intake_land_filed.py::test_a_second_unnamed_landing_that_day_takes_two_for_its_playlist_and_its_folder`
  - `tests/test_intake_land_native.py::test_a_failure_on_the_second_file_leaves_the_database_as_it_was_and_names_the_moves`
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_file_whose_tags_resolve_to_no_sub_stays_in_staging_on_the_native_medium_too`
  - `tests/test_intake_land_native.py::test_a_landing_names_the_pass_it_was_given_on_the_record_sync_mark_reads[None]`
  - `tests/test_intake_land_native.py::test_a_landing_names_the_pass_it_was_given_on_the_record_sync_mark_reads[RUN_synced]`
  - `tests/test_intake_land_native.py::test_a_landing_that_adds_no_row_needs_no_majority`
  - `tests/test_intake_land_native.py::test_a_row_whose_file_id_or_link_did_not_take_is_refused_after_the_commit[_file_id_lies_once]`
  - `tests/test_intake_land_native.py::test_a_row_whose_file_id_or_link_did_not_take_is_refused_after_the_commit[_link_keeps_the_bindings]`
  - `tests/test_intake_land_native.py::test_a_suffix_the_database_has_no_type_for_is_left_in_staging_and_the_batch_lands`
  - ... and 18 more, see the JSON sidecar

Old text:

```
    when, said = filed_parts(batch, on=on)
    spell = _speller(db)
```

New text:

```
    return landing.target_dir(cfg, batch)
    when, said = filed_parts(batch, on=on)
    spell = _speller(db)
```

### `u164.T2_free_disk`

_free_target: never pass over a folder already on disk

- File: `src/cratekit/intake/shelve.py`
- Source: `u164.json`, row `T2_free_disk`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filed.py`, `tests/test_intake_shelve.py`
- Collected: 29 against a baseline of 29
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_folder_on_disk_or_one_the_collection_stores_rows_under_is_passed_over`
  - `tests/test_intake_shelve.py::test_every_refusal_and_failure_leaves_the_batch_and_its_rows_as_they_were`
  - `tests/test_intake_shelve.py::test_two_batches_filing_to_one_name_get_two_and_a_taken_target_is_passed_over`

Old text:

```
    while os.path.lexists(candidate) or candidate in planned or spell(candidate) in stored_dirs:
```

New text:

```
    while candidate in planned or spell(candidate) in stored_dirs:
```

### `u164.T3_free_stored`

landing_target: ask the disk alone, not the collection's stored folders

- File: `src/cratekit/intake/shelve.py`
- Source: `u164.json`, row `T3_free_stored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filed.py`
- Collected: 6 against a baseline of 6
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_folder_on_disk_or_one_the_collection_stores_rows_under_is_passed_over`
  - `tests/test_intake_land_filed.py::test_a_name_landed_into_again_goes_back_to_its_folder_unless_the_folder_is_gone`

Old text:

```
        stored_dirs=_stored_dirs(recorded),
```

New text:

```
        stored_dirs=frozenset(),
```

### `u164.T4_undated_name`

filed_parts: file a name with no date under the whole name as a date-free folder

- File: `src/cratekit/intake/shelve.py`
- Source: `u164.json`, row `T4_undated_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filed.py`
- Collected: 6 against a baseline of 6
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_name_landed_into_again_goes_back_to_its_folder_unless_the_folder_is_gone`

Old text:

```
    when, words = parsed if parsed is not None else (on, " ".join(batch.split()))
```

New text:

```
    when, words = parsed if parsed is not None else (on, "")
```

### `u164.T5_empty_subject`

filed_parts: leave an empty subject empty instead of Downloads

- File: `src/cratekit/intake/shelve.py`
- Source: `u164.json`, row `T5_empty_subject`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filed.py`
- Collected: 6 against a baseline of 6
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_name_that_is_a_date_alone_files_as_downloads`

Old text:

```
    return when, words or batch_name.DOWNLOADS
```

New text:

```
    return when, words
```

### `u164.T6_reuse_recorded`

landing_target: never go back to the folder recorded for a batch landed into again

- File: `src/cratekit/intake/shelve.py`
- Source: `u164.json`, row `T6_reuse_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_rehearse.py`
- Collected: 75 against a baseline of 75
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_name_landed_into_again_goes_back_to_its_folder_unless_the_folder_is_gone`
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_landing_that_adds_no_row_needs_no_majority`
  - `tests/test_intake_land_native.py::test_the_same_files_staged_again_are_refused_at_the_move_and_the_collection_is_unchanged`
  - `tests/test_intake_land_rehearse.py::test_a_name_the_live_folder_holds_is_refused_at_the_area`

Old text:

```
    if again is not None and os.path.isdir(again) and not os.path.islink(again):
        return Path(again)
```

New text:

```
    if False:
        return Path(again)
```

### `u164.T7_reuse_gone`

landing_target: reuse a recorded folder even when it is gone from disk

- File: `src/cratekit/intake/shelve.py`
- Source: `u164.json`, row `T7_reuse_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filed.py`
- Collected: 6 against a baseline of 6
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_name_landed_into_again_goes_back_to_its_folder_unless_the_folder_is_gone`

Old text:

```
    if again is not None and os.path.isdir(again) and not os.path.islink(again):
```

New text:

```
    if again is not None:
```

### `u235.H1_shelve_four_hex_only`

intake.shelve: the run named batch pattern takes a four hex tail only, the round one finding, so a batch named for a run minted since U235 is refused as carrying no date

- File: `src/cratekit/intake/shelve.py`
- Source: `u235.json`, row `H1_shelve_four_hex_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_run_identifier_named_batch_files_as_downloads_or_as_the_subject_given[sixteen-hex-since-u235]`
  - `tests/test_intake_shelve.py::test_parse_name_reads_the_two_shapes_and_refuses_the_rest[2026-11-07T164826Z-ce458ab7cceccb0b-expected6]`

Old text:

```
T\d{6}Z-(?:[0-9a-f]{4}|[0-9a-f]{16})$")
```

New text:

```
T\d{6}Z-[0-9a-f]{4}$")
```

### `u235.H2_shelve_sixteen_hex_only`

intake.shelve: the run named batch pattern takes a sixteen hex tail only, so a batch named for a run from before U235 is refused as carrying no date

- File: `src/cratekit/intake/shelve.py`
- Source: `u235.json`, row `H2_shelve_sixteen_hex_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_run_identifier_named_batch_files_as_downloads_or_as_the_subject_given[four-hex-before-u235]`
  - `tests/test_intake_shelve.py::test_parse_name_reads_the_two_shapes_and_refuses_the_rest[2026-09-23T222241Z-4773-expected5]`

Old text:

```
T\d{6}Z-(?:[0-9a-f]{4}|[0-9a-f]{16})$")
```

New text:

```
T\d{6}Z-[0-9a-f]{16}$")
```

### `u154.G12_empty_plan_asks_a_gate`

a plan that moves nothing is put to the gate

- File: `src/cratekit/intake/shelve_cli.py`
- Source: `u154.json`, row `G12_empty_plan_asks_a_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_plan_of_nothing_and_every_command_line_refusal_refuse_before_a_gate`

Old text:

```
    if planned.batches:
        return
    raise refuse(

```

New text:

```
    if True:
        return
    raise refuse(

```

### `u154.G13_as_with_all_admitted`

one subject is applied to every batch under --all

- File: `src/cratekit/intake/shelve_cli.py`
- Source: `u154.json`, row `G13_as_with_all_admitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_plan_of_nothing_and_every_command_line_refusal_refuse_before_a_gate`

Old text:

```
    if subject is not None and (everything or len(names) != 1):

```

New text:

```
    if False:

```

### `u154.R2_subject_path_part_admitted`

a subject carrying a slash composes a nested target

- File: `src/cratekit/intake/shelve_cli.py`
- Source: `u154.json`, row `R2_subject_path_part_admitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_every_refusal_and_failure_leaves_the_batch_and_its_rows_as_they_were`

Old text:

```
    if subject is not None and not landing.plain_name(subject.strip()):

```

New text:

```
    if False:

```

### `u164.S1_already_filed`

intake shelve: plan a filed batch as before, refusing it as no folder

- File: `src/cratekit/intake/shelve_cli.py`
- Source: `u164.json`, row `S1_already_filed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filed.py`
- Collected: 6 against a baseline of 6
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_landing_on_the_27th_lands_in_its_year_folder_under_its_subject`

Old text:

```
    filed = _already_filed(cfg, names)
```

New text:

```
    filed = {}
```

### `u164.S2_music_folder_wins`

_already_filed: call a batch filed even when a folder of its name is under the music folder

- File: `src/cratekit/intake/shelve_cli.py`
- Source: `u164.json`, row `S2_music_folder_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 6 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_library_whose_drive_was_renamed_stores_and_confines_under_the_base_drive`
  - `tests/test_intake_shelve.py::test_a_row_under_the_target_refuses_the_commit_and_the_free_target_rule_passes_it_over`
  - `tests/test_intake_shelve.py::test_a_run_identifier_named_batch_files_as_downloads_or_as_the_subject_given[four-hex-before-u235]`
  - `tests/test_intake_shelve.py::test_a_run_identifier_named_batch_files_as_downloads_or_as_the_subject_given[sixteen-hex-since-u235]`
  - `tests/test_intake_shelve.py::test_apply_moves_the_folder_rewrites_the_paths_keeps_the_rest_and_the_name_stays_taken`
  - `tests/test_intake_shelve.py::test_every_refusal_and_failure_leaves_the_batch_and_its_rows_as_they_were`

Old text:

```
        if name in folders and not os.path.lexists(landing.target_dir(cfg, name))
```

New text:

```
        if name in folders
```

### `r798-c.H6_a_returned_release_passes_at_approval`

label approved: judge a release a person returned, so it is held a second time when it is accepted

- File: `src/cratekit/label/approved_cli.py`
- Source: `r798-c.json`, row `H6_a_returned_release_passes_at_approval`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`
- Collected: 141 against a baseline of 141
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_release_held_at_approval_is_returned_by_name_and_listed_the_next_time`
  - `tests/test_label_genre_gate.py::test_a_returned_mark_on_the_payload_alone_is_believed`
  - `tests/test_label_genre_gate.py::test_a_returned_release_is_listed_at_approval_and_not_judged_again`

Old text:

```
        if release.returned:
            continue
```

New text:

```
        if False:
            continue
```

### `r798-d.H7_again_an_owned_release_is_not_asked_about`

label approved: ask the general catalogue about a release the library holds in full. H7 measured again, against the line as the second review left it, where ownership is read off the one resolution of each release

- File: `src/cratekit/label/approved_cli.py`
- Source: `r798-d.json`, row `H7_again_an_owned_release_is_not_asked_about`
- Moved: the recorded verdict is now the first value of judged, so the owned branch is the same test written as judged is None and owned
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_the_catalogue_is_not_asked_about_a_release_the_library_already_holds`

Old text:

```
        if judged is None and owned(release):
```

New text:

```
        if judged is None and False:
```

### `u101.G10_ungated_not_reported_in_judged_label`

Drop the ungated branch in a judged label, so a release with no genre is listed silently

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G10_ungated_not_reported_in_judged_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_release_with_no_genre_is_not_counted_in_its_labels_share`
  - `tests/test_label_approved.py::test_a_release_with_no_genre_known_is_listed_with_a_failing_line`
  - `tests/test_label_approved.py::test_tracks_that_disagree_on_the_genre_are_not_judged_and_are_listed`

Old text:

```
            if outcome.ungated is not None:
```

New text:

```
            if False:
```

### `u101.G11_keep_read_as_drop`

Hold on the KEEP verdict instead of DROP

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G11_keep_read_as_drop`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 12 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_family_exactly_at_the_share_belongs_and_is_listed`
  - `tests/test_label_approved.py::test_a_genre_on_a_mapping_row_is_read_like_one_on_an_object`
  - `tests/test_label_approved.py::test_a_genre_the_label_makes_enough_of_is_listed`
  - `tests/test_label_approved.py::test_a_held_release_is_never_offered_for_review`
  - `tests/test_label_approved.py::test_a_release_of_an_out_of_place_genre_is_held_by_name_and_not_listed`
  - `tests/test_label_approved.py::test_a_release_unread_on_another_label_does_not_stop_this_label_being_judged`
  - `tests/test_label_approved.py::test_a_release_with_no_genre_is_not_counted_in_its_labels_share`
  - `tests/test_label_approved.py::test_each_label_is_judged_against_its_own_output`
  - `tests/test_label_approved.py::test_every_release_held_or_owned_is_a_no_op_that_does_not_claim_the_held_one`
  - `tests/test_label_approved.py::test_nothing_missing_with_one_held_and_one_unread_is_refused_and_says_both`
  - `tests/test_label_approved.py::test_releases_naming_no_label_are_each_judged_alone`
  - `tests/test_label_approved.py::test_the_default_human_output_names_a_held_release`

Old text:

```
            elif verdict is routing.GateVerdict.DROP and family and outcome.genre:
```

New text:

```
            elif verdict is routing.GateVerdict.KEEP and family and outcome.genre:
```

### `u101.G12_reported_share_not_the_taxonomys`

Report a share the taxonomy did not declare

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G12_reported_share_not_the_taxonomys`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_release_of_an_out_of_place_genre_is_held_by_name_and_not_listed`

Old text:

```
    share = declared.label_gate.out_of_place_share
```

New text:

```
    share = 0.2
```

### `u101.G13_family_count_off_by_one`

Report one more release of the family than there were

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G13_family_count_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_release_of_an_out_of_place_genre_is_held_by_name_and_not_listed`
  - `tests/test_label_approved.py::test_a_release_with_no_genre_is_not_counted_in_its_labels_share`

Old text:

```
families.count(family), classified, share
```

New text:

```
families.count(family) + 1, classified, share
```

### `u101.G14_classified_counts_unjudged`

Count every release in the label as classified, including those with no genre

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G14_classified_counts_unjudged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_release_with_no_genre_is_not_counted_in_its_labels_share`

Old text:

```
        classified = sum(1 for genre in genres if genre)
```

New text:

```
        classified = len(genres)
```

### `u101.G17_refusal_silent_on_held`

Drop the held clause from the nothing missing refusal

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G17_refusal_silent_on_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_nothing_missing_with_one_held_and_one_unread_is_refused_and_says_both`

Old text:

```
            + (f" and passed the genre gate ({len(held)} more held by it)" if held else "")
```

New text:

```
            + ""
```

### `u101.G18_no_op_claims_held`

The no op wording ignores held releases and says the library holds everything read

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G18_no_op_claims_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_every_release_held_or_owned_is_a_no_op_that_does_not_claim_the_held_one`

Old text:

```
            f"held by it"
            if held
            else
```

New text:

```
            f"held by it"
            if False
            else
```

### `u101.G1_held_is_listed`

Drop the skip, so a release the gate held is resolved, offered and listed anyway

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G1_held_is_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_genre_on_a_mapping_row_is_read_like_one_on_an_object`
  - `tests/test_label_approved.py::test_a_held_release_is_never_offered_for_review`
  - `tests/test_label_approved.py::test_a_release_of_an_out_of_place_genre_is_held_by_name_and_not_listed`
  - `tests/test_label_approved.py::test_a_release_unread_on_another_label_does_not_stop_this_label_being_judged`
  - `tests/test_label_approved.py::test_each_label_is_judged_against_its_own_output`
  - `tests/test_label_approved.py::test_every_release_held_or_owned_is_a_no_op_that_does_not_claim_the_held_one`
  - `tests/test_label_approved.py::test_nothing_missing_with_one_held_and_one_unread_is_refused_and_says_both`

Old text:

```
        if release.item_id in held:
            continue

```

New text:

```
(empty)
```

### `u101.G20_summary_held_empty`

The summary carries no held releases

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G20_summary_held_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_genre_on_a_mapping_row_is_read_like_one_on_an_object`
  - `tests/test_label_approved.py::test_a_release_of_an_out_of_place_genre_is_held_by_name_and_not_listed`
  - `tests/test_label_approved.py::test_a_release_unread_on_another_label_does_not_stop_this_label_being_judged`
  - `tests/test_label_approved.py::test_a_release_with_no_genre_is_not_counted_in_its_labels_share`
  - `tests/test_label_approved.py::test_each_label_is_judged_against_its_own_output`

Old text:

```
        held=[one.to_json() for one in held.values()],
```

New text:

```
        held=[],
```

### `u101.G2_judged_per_release`

Group every release under itself, so each is judged alone and nothing is ever held

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G2_judged_per_release`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 10 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_genre_on_a_mapping_row_is_read_like_one_on_an_object`
  - `tests/test_label_approved.py::test_a_held_release_is_never_offered_for_review`
  - `tests/test_label_approved.py::test_a_label_with_a_release_unread_this_run_is_not_judged_and_says_why`
  - `tests/test_label_approved.py::test_a_release_of_an_out_of_place_genre_is_held_by_name_and_not_listed`
  - `tests/test_label_approved.py::test_a_release_unread_on_another_label_does_not_stop_this_label_being_judged`
  - `tests/test_label_approved.py::test_a_release_with_no_genre_is_not_counted_in_its_labels_share`
  - `tests/test_label_approved.py::test_each_label_is_judged_against_its_own_output`
  - `tests/test_label_approved.py::test_every_release_held_or_owned_is_a_no_op_that_does_not_claim_the_held_one`
  - `tests/test_label_approved.py::test_nothing_missing_with_one_held_and_one_unread_is_refused_and_says_both`
  - `tests/test_label_approved.py::test_the_default_human_output_names_a_held_release`

Old text:

```
    return release.label_id or release.label_name or f"release:{release.release_id}"
```

New text:

```
    return f"release:{release.release_id}"
```

### `u101.G3_all_labels_one_group`

Group every release under one key, so labels are judged against each other

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G3_all_labels_one_group`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_release_unread_on_another_label_does_not_stop_this_label_being_judged`
  - `tests/test_label_approved.py::test_each_label_is_judged_against_its_own_output`
  - `tests/test_label_approved.py::test_nothing_missing_with_one_held_and_one_unread_is_refused_and_says_both`
  - `tests/test_label_approved.py::test_releases_naming_no_label_are_each_judged_alone`

Old text:

```
    return release.label_id or release.label_name or f"release:{release.release_id}"
```

New text:

```
    return "all"
```

### `u101.G4_unlabelled_grouped_together`

Group every release naming no label under one key instead of judging each alone

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G4_unlabelled_grouped_together`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_releases_naming_no_label_are_each_judged_alone`

Old text:

```
    return release.label_id or release.label_name or f"release:{release.release_id}"
```

New text:

```
    return release.label_id or release.label_name or "release:"
```

### `u101.G5_unread_label_judged`

Judge a label even when one of its releases was unread this run

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G5_unread_label_judged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_label_with_a_release_unread_this_run_is_not_judged_and_says_why`

Old text:

```
        if label in unread:
```

New text:

```
        if label in unread and False:
```

### `u101.G6_unread_from_every_label`

Treat every label as having an unread release whenever any release failed

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G6_unread_from_every_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_release_unread_on_another_label_does_not_stop_this_label_being_judged`
  - `tests/test_label_approved.py::test_nothing_missing_with_one_held_and_one_unread_is_refused_and_says_both`

Old text:

```
        if label in unread:
```

New text:

```
        if unread:
```

### `u101.G7_mixed_is_a_genre`

Rows that disagree yield their first genre instead of none

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G7_mixed_is_a_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_tracks_that_disagree_on_the_genre_are_not_judged_and_are_listed`

Old text:

```
    if len(said) > 1:
```

New text:

```
    if len(said) > 99:
```

### `u101.G8_case_is_a_difference`

Compare genres by exact text, so one genre in two cases reads as mixed

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G8_case_is_a_difference`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_one_genre_in_two_cases_is_one_genre_and_is_judged`

Old text:

```
            said.setdefault(text.casefold(), text)
```

New text:

```
            said.setdefault(text, text)
```

### `u101.G9_mapping_row_unread`

Read the genre by attribute only, so a mapping shaped row reports none

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G9_mapping_row_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_genre_on_a_mapping_row_is_read_like_one_on_an_object`

Old text:

```
        value = row.get("genre") if isinstance(row, Mapping) else getattr(row, "genre", None)
```

New text:

```
        value = getattr(row, "genre", None)
```

### `u75-a.A1_kind_filter`

Drop the kind filter, so an accepted harvested label name, which shares the queue, is read as a release

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-a.json`, row `A1_kind_filter`
- Moved: the list_items keywords of _queued were joined onto one line, so the kind filter is the same keyword dropped from it
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_an_accepted_harvested_label_shares_the_queue_and_is_not_a_release`

Old text:

```
        items, queue=str(Queue.LABEL_RELEASE), kinds=(sweep.KIND,), include_resolved=True,
```

New text:

```
        items, queue=str(Queue.LABEL_RELEASE), include_resolved=True,
```

### `u75-a.A3_nothing_accepted_before_the_catalogue`

Remove the early return, so a queue with nothing accepted resolves the catalogue and spends a login

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-a.json`, row `A3_nothing_accepted_before_the_catalogue`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_nothing_accepted_is_a_no_op_that_never_opens_the_catalogue`

Old text:

```
    if not accepted:
        # ASKED BEFORE THE CATALOGUE IS RESOLVED
```

New text:

```
    if False:
        # ASKED BEFORE THE CATALOGUE IS RESOLVED
```

### `u75-a.A5_only_the_seams_exception_is_gone`

Catch LookupError again instead of the seam's own class, the review's first finding

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-a.json`, row `A5_only_the_seams_exception_is_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_lookup_error_that_is_not_the_seams_own_is_never_read_as_a_gone_release`

Old text:

```
    except catalogue.ReleaseUnresolvable as exc:
        return _Failed(release, GONE, str(exc))
```

New text:

```
    except LookupError as exc:
        return _Failed(release, GONE, str(exc))
```

### `u75-a.A6_no_identifier_is_not_asked_of_the_provider`

Remove the empty identifier guard, so the provider is asked for a release with no name

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-a.json`, row `A6_no_identifier_is_not_asked_of_the_provider`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_an_accepted_item_naming_no_release_is_a_named_failure`

Old text:

```
    if not release.release_id:
        return _Failed(release, NO_IDENTIFIER, "the review item names no release identifier")

```

New text:

```
(empty)
```

### `u75-a.A7_each_row_read_alone`

Let one unreadable row escape, which costs the run instead of one line

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-a.json`, row `A7_each_row_read_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_one_unreadable_row_is_reported_and_the_rest_of_the_release_still_lists`

Old text:

```
        except match.UnreadableList as exc:
            unreadable.append(str(exc))
```

New text:

```
        except ZeroDivisionError as exc:
            unreadable.append(str(exc))
```

### `u75-b.B11_write_failure_is_the_verbs_refusal`

Remove the OSError conversion, so a full disk reaches a person as an internal error

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-b.json`, row `B11_write_failure_is_the_verbs_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_write_the_disk_refuses_is_the_verbs_refusal_and_not_an_internal_error`

Old text:

```
        except OSError as exc:
            # A FOLDER THAT CANNOT BE WRITTEN IS THIS VERB'S REFUSAL.
```

New text:

```
        except ZeroDivisionError as exc:
            # A FOLDER THAT CANNOT BE WRITTEN IS THIS VERB'S REFUSAL.
```

### `u75-b.B1_outage_threshold`

Raise the outage threshold from three to thirty, a realistic slip, so a dead provider is asked about every release

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-b.json`, row `B1_outage_threshold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_provider_that_stopped_answering_is_not_asked_about_every_release`

Old text:

```
OUTAGE_AFTER = 3
```

New text:

```
OUTAGE_AFTER = 30
```

### `u75-b.B3_only_a_provider_failure_counts`

Count a gone release towards an outage

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-b.json`, row `B3_only_a_provider_failure_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_gone_release_does_not_count_towards_an_outage`

Old text:

```
            in_a_row = in_a_row + 1 if outcome.kind == PROVIDER else 0
```

New text:

```
            in_a_row = in_a_row + 1
```

### `u75-b.B7_same_recording_listed_once`

Remove the match id dedupe, so a single and its album list one recording twice

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-b.json`, row `B7_same_recording_listed_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_the_same_recording_on_two_releases_is_listed_once_under_the_first`

Old text:

```
            elif settled.match_id in seen:
                counts["duplicate"] += 1

```

New text:

```
(empty)
```

### `u75-b.B9_name_digests_the_provenance`

Digest the tracks alone, the review's fourth finding, so a corrected year meets the emitter's refusal

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-b.json`, row `B9_name_digests_the_provenance`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_approved.py::test_the_list_name_moves_with_anything_the_emitter_would_write`
  - `tests/test_label_approved.py::test_the_same_tracks_with_a_corrected_year_take_a_new_name_and_are_not_refused`

Old text:

```
        "provenance": [
            dataclasses.asdict(provenance[track["id"]]) for track in body["tracks"]
        ],
```

New text:

```
        "provenance": [],
```

### `u75-zeros.B6_missing_and_nothing_listable_refuses`

Remove the refusal for missing tracks none of which carries a provider identifier

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-zeros.json`, row `B6_missing_and_nothing_listable_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_missing_tracks_none_of_which_can_be_asked_for_is_refused_and_not_a_no_op`

Old text:

```
    if missing and not listed:
```

New text:

```
    if False:
```

### `r840-a.A1_address_is_the_whole_field`

is_address: search for the address shape anywhere in the field, so a name that merely contains one is asked about and overwritten

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-a.json`, row `A1_address_is_the_whole_field`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_name_is_never_read_as_an_address[<provider.artist.Artist object at 0x10b77ec00> (remix)]`
  - `tests/test_label_artists.py::test_a_name_is_never_read_as_an_address[Label Act <provider.artist.Artist object at 0x10b77ec00>]`

Old text:

```
ADDRESS.fullmatch(value.strip()) is not None
```

New text:

```
ADDRESS.search(value.strip()) is not None
```

### `r840-a.A2_a_name_is_not_asked_about`

_listed: drop the address check, so every open label release is read from the provider and rewritten

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-a.json`, row `A2_a_name_is_not_asked_about`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_queue_with_no_address_opens_no_catalogue`
  - `tests/test_label_artists.py::test_a_second_run_asks_about_nothing_the_first_repaired`
  - `tests/test_label_artists.py::test_an_item_whose_artist_is_a_name_is_not_asked_about`
  - `tests/test_label_artists.py::test_an_item_with_no_artist_at_all_is_not_an_address_and_is_not_said_to_have_one`
  - `tests/test_label_artists.py::test_the_counts_always_sum_to_the_addresses_and_the_items_left_alone`
  - `tests/test_label_artists.py::test_the_provider_is_asked_once_for_each_repaired_item_and_never_for_the_others`

Old text:

```
        if not is_address(item.payload.get("artist")):
            done.counts[ALREADY_FINE] += 1
            continue
        if item.stored_verdict
```

New text:

```
        if item.stored_verdict
```

### `r840-a.A3_unreadable_verdict_is_decided`

_listed: drop the stored verdict check, so an item carrying a verdict this build cannot read is asked about

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-a.json`, row `A3_unreadable_verdict_is_decided`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_artists.py::test_an_item_carrying_a_verdict_this_build_cannot_read_is_left_and_not_asked_about`

Old text:

```
        if item.stored_verdict is not None:
            done.counts[DECIDED] += 1
            continue

```

New text:

```
(empty)
```

### `r840-a.A4_only_label_releases`

_listed: drop the kind from the selection, so another producer's item in the same queue is read as a release

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-a.json`, row `A4_only_label_releases`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_artists.py::test_another_queues_item_reading_an_address_is_not_this_verbs`

Old text:

```
review.Predicate(queue=str(Queue.LABEL_RELEASE), kind=genre_gate.RELEASE_KIND)
```

New text:

```
review.Predicate(queue=str(Queue.LABEL_RELEASE))
```

### `r840-a.A5_no_identifier_is_not_read`

_walk: drop the empty identifier half of the unaddressed check, so an item filed under an empty identifier is asked for and reported as no longer served

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-a.json`, row `A5_no_identifier_is_not_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_artists.py::test_an_item_filed_under_an_empty_identifier_is_not_asked_about`

Old text:

```
        if (
            not subject.release_id
            or genre_gate.release_item_id(subject.release_id) != subject.item_id
        ):
```

New text:

```
        if (
            genre_gate.release_item_id(subject.release_id) != subject.item_id
        ):
```

### `r840-a.A6_another_items_release_is_not_read`

_walk: drop the addressing half of the unaddressed check, so an item naming another item's release is given that release's artist

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-a.json`, row `A6_another_items_release_is_not_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_artists.py::test_an_item_naming_another_items_release_is_not_given_that_releases_artist`
  - `tests/test_label_artists.py::test_two_items_naming_one_release_are_two_lines_under_two_keys`

Old text:

```
        if (
            not subject.release_id
            or genre_gate.release_item_id(subject.release_id) != subject.item_id
        ):
```

New text:

```
        if (
            not subject.release_id
        ):
```

### `r840-a.A7_catalogue_opened_on_demand`

_walk: open the catalogue before the walk, so a queue with no address in it logs in and can refuse on the credential

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-a.json`, row `A7_catalogue_opened_on_demand`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_queue_with_no_address_opens_no_catalogue`
  - `tests/test_label_artists.py::test_an_empty_queue_is_a_no_op_that_opens_no_catalogue`

Old text:

```
    found: catalogue.Catalogue | None = None
    failed_in_a_row = 0
```

New text:

```
    found: catalogue.Catalogue | None = catalogue.resolve(cfg)
    failed_in_a_row = 0
```

### `r840-a.A8_outage_bound`

_walk: stop after four reads failing in a row and not three

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-a.json`, row `A8_outage_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_artists.py::test_three_reads_failing_in_a_row_stop_the_run_and_say_what_was_left`

Old text:

```
        if failed_in_a_row >= catalogue.READS_FAILED_IN_A_ROW:
            # THE RUN STOPS
```

New text:

```
        if failed_in_a_row > catalogue.READS_FAILED_IN_A_ROW:
            # THE RUN STOPS
```

### `r840-a.A9_an_answer_resets_the_count`

_walk: never reset the count of failed reads, so three scattered failures stop the run as an outage

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-a.json`, row `A9_an_answer_resets_the_count`
- Moved: the once used failed local was inlined, so the reset is the same conditional over the call itself
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_release_that_is_gone_does_not_count_towards_an_outage`
  - `tests/test_label_artists.py::test_an_answer_between_failures_keeps_the_run_going`

Old text:

```
failed_in_a_row = failed_in_a_row + 1 if _repair_one(store, found, subject, done) else 0
```

New text:

```
failed_in_a_row = failed_in_a_row + (1 if _repair_one(store, found, subject, done) else 0)
```

### `r840-b.B10_unaddressed_is_keyed_by_item`

_Run.record: key a line by its item only when it names no release, so an item naming another item's release shares that release's key

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-b.json`, row `B10_unaddressed_is_keyed_by_item`
- Moved: the key conditional was folded onto one line; the item key still turns on outcome being unaddressed
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_artists.py::test_two_items_naming_one_release_are_two_lines_under_two_keys`

Old text:

```
        key = f"item.{subject.item_id}" if outcome == UNADDRESSED else (
```

New text:

```
        key = f"item.{subject.item_id}" if not subject.release_id else (
```

### `r840-b.B11_left_counts_what_was_not_reached`

_with_counts: count left against every address and not against the items the run set out to read

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-b.json`, row `B11_left_counts_what_was_not_reached`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_catalogue_that_cannot_be_opened_refuses_and_repairs_nothing`
  - `tests/test_label_artists.py::test_a_release_the_provider_could_not_answer_for_is_left_and_the_run_refuses`
  - `tests/test_label_artists.py::test_an_answer_between_failures_keeps_the_run_going`
  - `tests/test_label_artists.py::test_an_outage_over_the_last_releases_of_a_run_is_the_same_refusal`
  - `tests/test_label_artists.py::test_the_seams_own_refusal_stops_the_run_and_carries_what_was_repaired`
  - `tests/test_label_artists.py::test_three_reads_failing_in_a_row_stop_the_run_and_say_what_was_left`

Old text:

```
    left = listed - len(done.releases)
```

New text:

```
    left = done.addresses - done.counts[REPAIRED]
```

### `r840-b.B1_only_the_seams_exception_is_not_served`

_repair_one: catch LookupError where the seam's own exception is caught, so a client that could not parse a payload is reported as a release that is gone

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-b.json`, row `B1_only_the_seams_exception_is_not_served`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_lookup_error_that_is_not_the_seams_own_is_unread_and_never_not_served`

Old text:

```
    except catalogue.ReleaseUnresolvable as exc:
```

New text:

```
    except LookupError as exc:
```

### `r840-b.B2_a_refusal_stops_the_run`

_repair_one: drop the CratekitError passthrough, so an expired session is recorded as one unread release and the walk goes on asking

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-b.json`, row `B2_a_refusal_stops_the_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_artists.py::test_the_seams_own_refusal_stops_the_run_and_carries_what_was_repaired`

Old text:

```
        name = found.release_artist(subject.release_id)
    except CratekitError:
        raise
    except catalogue
```

New text:

```
        name = found.release_artist(subject.release_id)
    except catalogue
```

### `r840-b.B3_no_name_never_blanks`

_repair_one: write whatever the provider answered unless it is None, so a release it names no artist for has its address replaced by nothing

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-b.json`, row `B3_no_name_never_blanks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_release_the_provider_names_no_artist_for_is_left_reading_what_it_read[   ]`
  - `tests/test_label_artists.py::test_a_release_the_provider_names_no_artist_for_is_left_reading_what_it_read[]`

Old text:

```
    name = _text(name)
    if not name:
```

New text:

```
    name = _text(name)
    if name is None:
```

### `r840-b.B4_an_unread_release_refuses`

_walk: refuse only when the outage bound was reached, so a run that left one or two releases unread exits clean

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-b.json`, row `B4_an_unread_release_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_lookup_error_that_is_not_the_seams_own_is_unread_and_never_not_served`
  - `tests/test_label_artists.py::test_a_release_the_provider_could_not_answer_for_is_left_and_the_run_refuses`

Old text:

```
    if done.counts[UNREAD]:
        # AFTER THE WALK
```

New text:

```
    if done.counts[UNREAD] >= catalogue.READS_FAILED_IN_A_ROW:
        # AFTER THE WALK
```

### `r840-b.B5_decided_meanwhile_is_not_fine`

_write: answer already fine whenever nothing was written, so an item decided during the read is said to have stopped reading an address

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-b.json`, row `B5_decided_meanwhile_is_not_fine`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_release_decided_while_it_was_being_read_is_not_rewritten`
  - `tests/test_label_artists.py::test_a_release_that_left_review_while_it_was_being_read_is_not_filed_again`

Old text:

```
    return ALREADY_FINE if seen else DECIDED
```

New text:

```
    return ALREADY_FINE
```

### `r840-b.B6_put_right_meanwhile_is_kept`

_write: drop the address check on the payload as it stands, so an artist somebody typed during the read is overwritten by the provider's

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-b.json`, row `B6_put_right_meanwhile_is_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_artists.py::test_an_artist_put_right_meanwhile_is_not_overwritten`
  - `tests/test_label_artists.py::test_the_counts_always_sum_to_the_addresses_and_the_items_left_alone`

Old text:

```
        if not is_address(current.get("artist")):
            return None
        return {**current, "artist": name}
```

New text:

```
        return {**current, "artist": name}
```

### `r840-b.B7_addresses_are_what_still_read_one`

_Run.addresses: count every outcome, so an item that stopped reading an address, and every item that never did, is counted as one

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-b.json`, row `B7_addresses_are_what_still_read_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_queue_with_no_address_opens_no_catalogue`
  - `tests/test_label_artists.py::test_an_artist_put_right_meanwhile_is_not_overwritten`
  - `tests/test_label_artists.py::test_an_item_whose_artist_is_a_name_is_not_asked_about`
  - `tests/test_label_artists.py::test_the_counts_always_sum_to_the_addresses_and_the_items_left_alone`
  - `tests/test_label_artists.py::test_the_provider_is_asked_once_for_each_repaired_item_and_never_for_the_others`

Old text:

```
        return sum(n for outcome, n in self.counts.items() if outcome != ALREADY_FINE)
```

New text:

```
        return sum(self.counts.values())
```

### `r840-b.B8_only_the_artist_is_rewritten`

_write: write a payload holding the artist alone, so every other field of the item is lost

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-b.json`, row `B8_only_the_artist_is_rewritten`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_artists.py::test_an_answer_between_failures_keeps_the_run_going`
  - `tests/test_label_artists.py::test_an_open_item_reading_an_address_is_given_the_name_and_nothing_else_moves`
  - `tests/test_label_artists.py::test_what_a_judging_job_stamped_meanwhile_is_kept`

Old text:

```
        return {**current, "artist": name}
```

New text:

```
        return {"artist": name}
```

### `r840-b.B9_a_refusal_carries_why_each_read_failed`

_Run.record: leave the sentence off the release's row, so a refusal, which carries no check line, says a read failed and not why

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-b.json`, row `B9_a_refusal_carries_why_each_read_failed`
- Moved: the release row literal was written on one line; dropping the said key leaves the sentence off the row as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_release_the_provider_could_not_answer_for_is_left_and_the_run_refuses`
  - `tests/test_label_artists.py::test_an_open_item_reading_an_address_is_given_the_name_and_nothing_else_moves`

Old text:

```
            {**asdict(subject), "outcome": outcome, "artist": artist, "said": said}
```

New text:

```
            {**asdict(subject), "outcome": outcome, "artist": artist}
```

### `r504-a.A10_block_listed`

The report block carries the declared count where the listed count belongs

- File: `src/cratekit/label/catalogue.py`
- Source: `r504-a.json`, row `A10_block_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_playlist_declaring_ten_with_two_withheld_queues_eight_and_warns`
  - `tests/test_intake_missing.py::test_a_playlist_whose_every_track_is_withheld_is_not_a_quiet_no_op`
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`

Old text:

```
        return {"declared": self.declared, "listed": self.listed, "withheld": self.withheld}
```

New text:

```
        return {"declared": self.declared, "listed": self.declared, "withheld": self.withheld}
```

### `r504-a.A8_withheld_sign`

The seam subtracts the wrong way round, so the withheld count is negative

- File: `src/cratekit/label/catalogue.py`
- Source: `r504-a.json`, row `A8_withheld_sign`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_playlist_declaring_ten_with_two_withheld_queues_eight_and_warns`
  - `tests/test_intake_missing.py::test_a_playlist_whose_every_track_is_withheld_is_not_a_quiet_no_op`
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`

Old text:

```
        return self.declared - self.listed
```

New text:

```
        return self.listed - self.declared
```

### `r504-a.A9_summary_reworded`

The seam's one spelling of the three numbers is reworded

- File: `src/cratekit/label/catalogue.py`
- Source: `r504-a.json`, row `A9_summary_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_playlist_declaring_ten_with_two_withheld_queues_eight_and_warns`
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`

Old text:

```
            f"{self.withheld} withheld by the provider"
```

New text:

```
            f"{self.withheld} held back by the provider"
```

### `r815-a.G2_forgetting_keeps_the_failure_count`

ReleaseTracks.forget: forget the failures in a row as well

- File: `src/cratekit/label/catalogue.py`
- Source: `r815-a.json`, row `G2_forgetting_keeps_the_failure_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_judge.py::test_the_reader_forgets_each_release_and_keeps_its_count_of_failures`
  - `tests/test_label_judge.py::test_three_provider_reads_failing_in_a_row_stop_the_run`

Old text:

```
        self._read.clear()

    def release_tracks
```

New text:

```
        self._read.clear()
        self._failed_in_a_row = 0

    def release_tracks
```

### `u308.L4_translated_swallows_refusal`

catalogue.translated: an adapter's own refusal is translated into the boundary's failure

- File: `src/cratekit/label/catalogue.py`
- Source: `u308.json`, row `L4_translated_swallows_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_a_short_listing_did_not_date_is_held_back_not_filed_undated`

Old text:

```
    except passing:
        raise
    except Exception as exc:
```

New text:

```
    except Exception as exc:
```

### `r1634.M16_worker_drops_how`

label-sweep-incomplete: the worker's message no longer says how the release was asked

- File: `src/cratekit/label/cli.py`
- Source: `r1634.json`, row `M16_worker_drops_how`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_though_every_held_line_names_the_label`

Old text:

```
            f"{one.how()}: {one.said()}."
```

New text:

```
            f": {one.said()}."
```

### `r290-author.S06_label_call_removed`

Remove the one jobs.raise_for_state call from label/cli.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/label/cli.py`
- Source: `r290-author.json`, row `S06_label_call_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`
- Collected: 126 against a baseline of 126
- Kills: 11 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[label.import]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[sync.labels]`
  - `tests/test_job_outcome.py::test_a_parked_or_half_failed_job_answers_the_same_way_the_second_time_it_is_asked[half-failed-label.import]`
  - `tests/test_job_outcome.py::test_a_parked_or_half_failed_job_answers_the_same_way_the_second_time_it_is_asked[half-failed-sync.labels]`
  - `tests/test_job_outcome.py::test_a_parked_or_half_failed_job_answers_the_same_way_the_second_time_it_is_asked[parked-label.import]`
  - `tests/test_job_outcome.py::test_a_parked_or_half_failed_job_answers_the_same_way_the_second_time_it_is_asked[parked-sync.labels]`
  - `tests/test_job_outcome.py::test_a_parked_or_half_failed_job_leaves_every_queued_verb_non_zero[half-failed-label.import]`
  - `tests/test_job_outcome.py::test_a_parked_or_half_failed_job_leaves_every_queued_verb_non_zero[half-failed-sync.labels]`
  - `tests/test_job_outcome.py::test_a_parked_or_half_failed_job_leaves_every_queued_verb_non_zero[parked-label.import]`
  - `tests/test_job_outcome.py::test_a_parked_or_half_failed_job_leaves_every_queued_verb_non_zero[parked-sync.labels]`
  - `tests/test_job_outcome.py::test_every_function_that_drives_a_job_maps_its_ending_afterwards`

Old text:

```
jobs.raise_for_state(job)
```

New text:

```
jobs.get  # the mapping call, removed
```

### `r790-b.L1_guard_counts_held`

_refuse_unfinished: leave held releases out of the confirmed-none count, so a dead verifier reads as nothing new

- File: `src/cratekit/label/cli.py`
- Source: `r790-b.json`, row `L1_guard_counts_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_dead_verifier_on_a_later_sweep_refuses_rather_than_reporting_nothing_new`

Old text:

```
    unconfirmed = len(source.dropped) + source.held_unconfirmed
```

New text:

```
    unconfirmed = len(source.dropped)
```

### `r790-b.L2_round_records_beyond`

handle: record every round as nothing beyond

- File: `src/cratekit/label/cli.py`
- Source: `r790-b.json`, row `L2_round_records_beyond`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`
- Collected: 40 against a baseline of 40
- Kills: 8 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_first_sweep_files_the_default_ten_and_counts_the_other_forty`
  - `tests/test_label_offer_window.py::test_a_label_whose_window_is_already_held_records_its_beyond_with_nothing_filed`
  - `tests/test_label_offer_window.py::test_a_round_records_the_most_the_label_could_still_offer`
  - `tests/test_label_offer_window.py::test_a_run_over_two_labels_counts_what_both_left_beyond`
  - `tests/test_label_offer_window.py::test_a_second_sweep_files_only_the_new_release_and_refiles_nothing`
  - `tests/test_label_offer_window.py::test_the_window_bounds_what_a_sweep_files_and_the_rest_is_counted[a-track-limit-below-the-offer]`
  - `tests/test_label_offer_window.py::test_the_window_bounds_what_a_sweep_files_and_the_rest_is_counted[an-offer-raised-to-thirty-files-thirty]`
  - `tests/test_label_offer_window.py::test_the_window_bounds_what_a_sweep_files_and_the_rest_is_counted[the-configured-offer-is-every-labels-default]`

Old text:

```
                beyond=listing.beyond,
```

New text:

```
                beyond=0,
```

### `r790-b.L3_set_passes_offer`

registry_cmd set: drop --offer on the way to the store, so set reports an edit it never wrote

- File: `src/cratekit/label/cli.py`
- Source: `r790-b.json`, row `L3_set_passes_offer`
- Moved: The offer reaches edit through the shared field mapping; the mutation overrides it with None for the set call alone, so set reports an offer it never wrote.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_raising_a_label_offer_after_a_sweep_files_the_difference`

Old text:

```
        edited = store.edit(name, seed_artists=seeds, **fields)

```

New text:

```
        edited = store.edit(name, seed_artists=seeds, **{**fields, "offer": None})

```

### `r790-b.L4_bound_is_said`

_detail: stop saying the track limit bounds an offer

- File: `src/cratekit/label/cli.py`
- Source: `r790-b.json`, row `L4_bound_is_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_the_registry_says_when_the_track_limit_bounds_an_offer`

Old text:

```
            + (f", bounded by the track limit to {bound}" if entry.offer > bound else "")
```

New text:

```
            + ""
```

### `u177.A10_clear_word`

registry_cmd: drop the clear word, so --bandcamp default stores an account named default

- File: `src/cratekit/label/cli.py`
- Source: `u177.json`, row `A10_clear_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_bandcamp_account.py`
- Collected: 28 against a baseline of 28
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_bandcamp_account.py::test_default_clears_the_account_and_frees_it_for_another_label`

Old text:

```
    clear_bandcamp = bandcamp is not None and bandcamp.strip().lower() == labels.CLEAR_BANDCAMP

```

New text:

```
    clear_bandcamp = False

```

### `u177.A11_field_flag_guard`

registry_cmd: leave --bandcamp out of the fields given, so remove --bandcamp is silently ignored and set --bandcamp alone refused

- File: `src/cratekit/label/cli.py`
- Source: `u177.json`, row `A11_field_flag_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_bandcamp_account.py`
- Collected: 28 against a baseline of 28
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_bandcamp_account.py::test_a_label_setting_its_own_account_again_is_no_conflict`
  - `tests/test_label_bandcamp_account.py::test_a_second_label_naming_a_held_account_is_refused_by_the_holders_name`
  - `tests/test_label_bandcamp_account.py::test_default_clears_the_account_and_frees_it_for_another_label`
  - `tests/test_label_bandcamp_account.py::test_set_with_only_bandcamp_is_a_field_to_change`

Old text:

```
    fields_given = (seeds, track_limit, ctx.args.match, offer, kind, genre, bandcamp)

```

New text:

```
    fields_given = (seeds, track_limit, ctx.args.match, offer, kind, genre)

```

### `u177.A9_add_drops_account`

registry_cmd add: pass no account to the store, so add --bandcamp is accepted and never written

- File: `src/cratekit/label/cli.py`
- Source: `u177.json`, row `A9_add_drops_account`
- Moved: The fields add and set share are one mapping handed to the store, and the add answer follows the call; the mutation hands add no account, which is the same guard as passing bandcamp=None in the inline call.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_bandcamp_account.py`
- Collected: 28 against a baseline of 28
- Kills: 12 (killed)
- Killed:
  - `tests/test_label_bandcamp_account.py::test_a_rename_of_the_label_keeps_its_seller`
  - `tests/test_label_bandcamp_account.py::test_a_second_label_naming_a_held_account_is_refused_by_the_holders_name`
  - `tests/test_label_bandcamp_account.py::test_add_with_an_account_round_trips_through_list`
  - `tests/test_label_bandcamp_account.py::test_an_address_or_any_case_is_stored_as_the_account_a_purchase_is_read_as[  pulsromania  ]`
  - `tests/test_label_bandcamp_account.py::test_an_address_or_any_case_is_stored_as_the_account_a_purchase_is_read_as[PulsRomania]`
  - `tests/test_label_bandcamp_account.py::test_an_address_or_any_case_is_stored_as_the_account_a_purchase_is_read_as[an-account-named-default]`
  - `tests/test_label_bandcamp_account.py::test_an_address_or_any_case_is_stored_as_the_account_a_purchase_is_read_as[https://PulsRomania.bandcamp.com/music]`
  - `tests/test_label_bandcamp_account.py::test_an_address_or_any_case_is_stored_as_the_account_a_purchase_is_read_as[https://pulsromania.bandcamp.com]`
  - `tests/test_label_bandcamp_account.py::test_an_address_or_any_case_is_stored_as_the_account_a_purchase_is_read_as[own-domain]`
  - `tests/test_label_bandcamp_account.py::test_an_address_or_any_case_is_stored_as_the_account_a_purchase_is_read_as[pulsromania.bandcamp.com/album/sun-path]`
  - `tests/test_label_bandcamp_account.py::test_an_address_or_any_case_is_stored_as_the_account_a_purchase_is_read_as[pulsromania.bandcamp.com]`
  - `tests/test_label_bandcamp_account.py::test_set_of_another_field_keeps_the_account`

Old text:

```
        label_id = store.add(name, seed_artists=tuple(seeds or ()), **fields)
        return _answer(ctx, store, {"added": label_id}, label_id, route)

```

New text:

```
        label_id = store.add(name, seed_artists=tuple(seeds or ()), **{**fields, "bandcamp": None})
        return _answer(ctx, store, {"added": label_id}, label_id, route)

```

### `u178.G6_fallback_refusal`

_declared_genre: never refuse a fallback genre, so Polka is stored unconfirmed

- File: `src/cratekit/label/cli.py`
- Source: `u178.json`, row `G6_fallback_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_genre_routing_only_to_the_fallback_is_refused_and_nothing_is_written`

Old text:

```
    if resolution.match is routing.Match.FALLBACK and not accept_fallback:
```

New text:

```
    if False:
```

### `u178.G7_fallback_confirm_ignored`

_declared_genre: refuse a fallback genre even with --accept-fallback

- File: `src/cratekit/label/cli.py`
- Source: `u178.json`, row `G7_fallback_confirm_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_fallback_genre_is_kept_when_confirmed_and_the_screen_says_it`

Old text:

```
    if resolution.match is routing.Match.FALLBACK and not accept_fallback:
```

New text:

```
    if resolution.match is routing.Match.FALLBACK:
```

### `u178.G8_clear_word_case`

_declared_genre: match the clearing word in its exact case, so --genre Default is stored as a genre

- File: `src/cratekit/label/cli.py`
- Source: `u178.json`, row `G8_clear_word_case`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_the_word_default_clears_a_genre_and_none_keeps_it`

Old text:

```
    if wanted.casefold() == CLEAR_GENRE:
```

New text:

```
    if wanted == CLEAR_GENRE:
```

### `u178.G9_accept_without_genre`

registry_cmd: accept --accept-fallback with no --genre, so it confirms nothing silently

- File: `src/cratekit/label/cli.py`
- Source: `u178.json`, row `G9_accept_without_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_accept_fallback_with_no_genre_is_refused`

Old text:

```
    if accept_fallback and genre is None:
```

New text:

```
    if False:
```

### `u277.M11_worker_detail_without_canary`

the worker's label-sweep-incomplete: leave the canary out of the refusal's detail

- File: `src/cratekit/label/cli.py`
- Source: `u277.json`, row `M11_worker_detail_without_canary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`
- Collected: 37 against a baseline of 37
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_over_held_lines_that_name_the_label`
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_the_worker_refuses_held_lines_naming_another_act_and_names_the_canary`

Old text:

```
                **({"reverified": canaries[0].to_json()} if canaries else {}),
```

New text:

```
                **({}),
```

### `u277.M12_worker_message_without_canary`

the worker's label-sweep-incomplete: leave the canary out of the refusal's message

- File: `src/cratekit/label/cli.py`
- Source: `u277.json`, row `M12_worker_message_without_canary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`
- Collected: 37 against a baseline of 37
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_the_worker_refuses_held_lines_naming_another_act_and_names_the_canary`

Old text:

```
            f"{asked_again}",
```

New text:

```
            f"",
```

### `u117-operator.D10_no_folder_refusal`

apply: drop the missing folder refusal, so a dated playlist is made at the account root

- File: `src/cratekit/label/dated.py`
- Source: `u117-operator.json`, row `D10_no_folder_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_dated.py::test_a_label_with_no_folder_yet_refuses_the_apply_before_any_write`

Old text:

```
    if not folder_id:
        raise _no_folder(planned)
```

New text:

```
(empty)
```

### `u117-operator.D11_part_way_named`

apply: a failure part way is raised bare, without what was written

- File: `src/cratekit/label/dated.py`
- Source: `u117-operator.json`, row `D11_part_way_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_dated.py::test_a_move_refused_after_the_create_names_the_playlist_left_at_the_root`
  - `tests/test_label_dated.py::test_the_account_refusing_mid_pass_names_what_was_written_and_a_rerun_finishes`

Old text:

```
        raise _failed_part_way(exc, done, planned) from exc
```

New text:

```
        raise
```

### `u117-operator.D12_move_into_folder`

apply: a created dated playlist is not moved into the label's folder

- File: `src/cratekit/label/dated.py`
- Source: `u117-operator.json`, row `D12_move_into_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 24 against a baseline of 24
- Kills: 8 (killed)
- Killed:
  - `tests/test_label_dated.py::test_a_go_into_an_existing_year_makes_a_dated_playlist_and_leaves_the_year`
  - `tests/test_label_dated.py::test_a_move_refused_after_the_create_names_the_playlist_left_at_the_root`
  - `tests/test_label_dated.py::test_a_second_go_the_same_day_appends_to_the_same_dated_playlist`
  - `tests/test_label_dated.py::test_a_track_the_provider_will_not_play_is_never_planned_on_the_dated_path`
  - `tests/test_label_dated.py::test_organize_plans_the_dated_playlist_after_the_label_folder_and_applies_in_order`
  - `tests/test_label_dated.py::test_organize_reports_a_dated_playlist_past_the_age_and_moves_nothing`
  - `tests/test_label_dated.py::test_the_account_refusing_mid_pass_names_what_was_written_and_a_rerun_finishes`
  - `tests/test_label_dated.py::test_the_age_is_the_configured_one`

Old text:

```
                account.move_to_folder(remote_id, folder_id)
```

New text:

```
                pass
```

### `u117-operator.D15_playable_only`

plan: take every track of a release, playable or not, so an unplayable track is planned on every run

- File: `src/cratekit/label/dated.py`
- Source: `u117-operator.json`, row `D15_playable_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_dated.py::test_a_track_the_provider_will_not_play_is_never_planned_on_the_dated_path`

Old text:

```
        held.extend(one for one in tracks if one in playable and one not in held)
```

New text:

```
        held.extend(one for one in tracks if one not in held)
```

### `u117-operator.D16_recorded_before_move`

apply: record the created playlist only after the move, so a move refused after the create reports nothing written

- File: `src/cratekit/label/dated.py`
- Source: `u117-operator.json`, row `D16_recorded_before_move`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_dated.py::test_a_move_refused_after_the_create_names_the_playlist_left_at_the_root`

Old text:

```
                done.unplaced.append(step.name)
                account.move_to_folder(remote_id, folder_id)
```

New text:

```
                account.move_to_folder(remote_id, folder_id)
                done.unplaced.append(step.name)
```

### `u117-operator.D1_heard_left_out`

plan: drop the heard check, so a release the record lists as heard is filed into the dated playlist again

- File: `src/cratekit/label/dated.py`
- Source: `u117-operator.json`, row `D1_heard_left_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_dated.py::test_a_heard_release_is_left_out_and_the_record_is_not_written`

Old text:

```
        if identity in gone:
```

New text:

```
        if False:
```

### `u117-operator.D2_unsettled_taken`

taken_by_goes: drop the settled check, so an answer no go has taken files its releases as downloaded

- File: `src/cratekit/label/dated.py`
- Source: `u117-operator.json`, row `D2_unsettled_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_dated.py::test_an_unsettled_or_not_now_answer_took_nothing`

Old text:

```
        if not isinstance(settled, Mapping):
            continue
```

New text:

```
        if not isinstance(settled, Mapping):
            settled = {"at": "2026-10-09T12:00:00+00:00"}
```

### `u117-operator.D4_local_day`

_local_day: keep the recorded UTC day instead of the local one, so a go at 22:00 local west of UTC is filed under tomorrow; killed by the evening instant test

- File: `src/cratekit/label/dated.py`
- Source: `u117-operator.json`, row `D4_local_day`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_dated.py::test_a_move_refused_after_the_create_names_the_playlist_left_at_the_root`
  - `tests/test_label_dated.py::test_an_evening_go_west_of_utc_keeps_its_local_day`

Old text:

```
    if moment.tzinfo is not None:
        moment = moment.astimezone()
```

New text:

```
    if moment.tzinfo is not None:
        moment = moment
```

### `u117-operator.D5_reuse_by_name`

plan: never reuse a dated playlist by its name, so a second go the same day makes a second playlist

- File: `src/cratekit/label/dated.py`
- Source: `u117-operator.json`, row `D5_reuse_by_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 24 against a baseline of 24
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_dated.py::test_a_second_go_the_same_day_appends_to_the_same_dated_playlist`
  - `tests/test_label_dated.py::test_a_track_the_provider_will_not_play_is_never_planned_on_the_dated_path`
  - `tests/test_label_dated.py::test_organize_reports_a_dated_playlist_past_the_age_and_moves_nothing`
  - `tests/test_label_dated.py::test_the_account_refusing_mid_pass_names_what_was_written_and_a_rerun_finishes`
  - `tests/test_label_dated.py::test_two_playlists_with_the_dated_name_are_left_alone`

Old text:

```
        matching = sorted(pid for pid, title in inside.items() if title == name)
```

New text:

```
        matching = []
```

### `u117-operator.D6_reuse_adds_only_missing`

plan: a reused dated playlist adds every track again rather than only the missing ones

- File: `src/cratekit/label/dated.py`
- Source: `u117-operator.json`, row `D6_reuse_adds_only_missing`
- Moved: The same filter that adds to a reused dated playlist only the tracks it does not hold; the step choice became an if/elif/else, so the filtered tuple is named before the REUSE step is built rather than written as its keyword argument.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 24 against a baseline of 24
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_dated.py::test_a_second_go_the_same_day_appends_to_the_same_dated_playlist`
  - `tests/test_label_dated.py::test_a_track_the_provider_will_not_play_is_never_planned_on_the_dated_path`
  - `tests/test_label_dated.py::test_organize_reports_a_dated_playlist_past_the_age_and_moves_nothing`
  - `tests/test_label_dated.py::test_the_account_refusing_mid_pass_names_what_was_written_and_a_rerun_finishes`

Old text:

```
            add = tuple(one for one in tracks if one not in have)
```

New text:

```
            add = tuple(tracks)
```

### `u117-operator.D7_ambiguous`

plan: two playlists with the dated name reuse the first instead of being left alone

- File: `src/cratekit/label/dated.py`
- Source: `u117-operator.json`, row `D7_ambiguous`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_dated.py::test_two_playlists_with_the_dated_name_are_left_alone`

Old text:

```
        if len(matching) > 1:
```

New text:

```
        if len(matching) > 99:
```

### `u117-operator.D8_age_bound`

_aged: report at the age rather than past it, an off by one on the bound

- File: `src/cratekit/label/dated.py`
- Source: `u117-operator.json`, row `D8_age_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_dated.py::test_organize_reports_a_dated_playlist_past_the_age_and_moves_nothing`
  - `tests/test_label_dated.py::test_the_age_is_the_configured_one`

Old text:

```
        if days > limit:
```

New text:

```
        if days > limit * 2:
```

### `u117-operator.D9_age_configured`

plan: ignore the configured age and use the default

- File: `src/cratekit/label/dated.py`
- Source: `u117-operator.json`, row `D9_age_configured`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_dated.py::test_the_age_is_the_configured_one`

Old text:

```
        aged=_aged(catalogue.name, inside, today, cfg.labels.new_playlist_age_days),
```

New text:

```
        aged=_aged(catalogue.name, inside, today, 30),
```

### `u123.D1_dated_create_vouched`

Create a dated playlist without recording it in the ledger

- File: `src/cratekit/label/dated.py`
- Source: `u123.json`, row `D1_dated_create_vouched`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 13 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_dated_playlist_made_by_the_dated_plan_is_vouched_for_and_one_reused_is_not`
  - `tests/test_label_heard.py::test_a_folder_with_no_year_playlist_refuses_when_there_is_something_to_add`
  - `tests/test_label_heard.py::test_a_named_release_already_heard_is_said_and_writes_nothing`
  - `tests/test_label_heard.py::test_a_removal_refused_part_way_names_the_adds_marks_nothing_and_a_resume_finishes`
  - `tests/test_label_heard.py::test_a_track_an_unheard_release_also_carries_stays_on_the_dated_playlist`
  - `tests/test_label_heard.py::test_a_track_the_year_will_not_take_keeps_the_dated_playlist`
  - `tests/test_label_heard.py::test_a_year_known_only_by_the_marks_prefixed_name_is_the_year`
  - `tests/test_label_heard.py::test_declined_nothing_is_written`
  - `tests/test_label_heard.py::test_every_run_says_the_record_labels_tree_is_not_changed`
  - `tests/test_label_heard.py::test_heard_writes_the_ids_merges_and_removes_and_a_second_run_is_a_no_op`
  - `tests/test_label_heard.py::test_some_releases_heard_take_their_tracks_off_and_the_last_removes_it`
  - `tests/test_label_heard.py::test_the_merge_adds_only_what_the_year_lacks_and_never_a_duplicate`
  - `tests/test_label_heard.py::test_what_the_merge_adds_to_a_recorded_year_is_recorded_on_it`

Old text:

```
                remote_id = ledger.reserve_label_dated(
                    cfg,
                    planned.label_id,
                    step.name,
                    lambda name=step.name: account.create_playlist(name),
                )
```

New text:

```
                remote_id = account.create_playlist(step.name)
```

### `u191.M21_unsettled_answers_read`

taken_by_goes: read an answer no go has settled (existing guard, newly on this unit's path)

- File: `src/cratekit/label/dated.py`
- Source: `u191.json`, row `M21_unsettled_answers_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_dated.py::test_an_unsettled_or_not_now_answer_took_nothing`

Old text:

```
        if not isinstance(settled, Mapping):
            continue
```

New text:

```
        if not isinstance(settled, Mapping):
            settled = {"at": "2026-10-31T12:00:00+00:00"}
```

### `u308.L2_part_way_again_dropped`

dated.refused_part_way: a refusal that failed part way loses the step to run again

- File: `src/cratekit/label/dated.py`
- Source: `u308.json`, row `L2_part_way_again_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_dated.py::test_a_write_that_failed_part_way_keeps_a_refusals_reason_and_adds_its_step_again`

Old text:

```
            steps=(*cause.remediation.steps, again),
```

New text:

```
            steps=tuple(cause.remediation.steps),
```

### `u308.L3_part_way_reason_lost`

dated.refused_part_way: a refusal that failed part way reads as this build's defect

- File: `src/cratekit/label/dated.py`
- Source: `u308.json`, row `L3_part_way_reason_lost`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_dated.py::test_a_write_that_failed_part_way_keeps_a_refusals_reason_and_adds_its_step_again`

Old text:

```
    if isinstance(exc, CratekitError):
        cause = exc.cause
        return refuse(
```

New text:

```
    if False:
        cause = exc.cause
        return refuse(
```

### `r798-b.G1_an_unread_answer_holds_nothing`

published_words: read on past an answer that could not be read, so words read before a refusal still hold the release

- File: `src/cratekit/label/gate.py`
- Source: `r798-b.json`, row `G1_an_unread_answer_holds_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`
- Collected: 141 against a baseline of 141
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_release_is_judged_on_as_many_tracks_as_settle_it[a-catalogue-that-refuses-after-a-would-be-hold-holds-nothing]`
  - `tests/test_label_genre_gate.py::test_an_answer_that_could_not_be_read_stops_the_asking[blocked]`
  - `tests/test_label_genre_gate.py::test_an_answer_that_could_not_be_read_stops_the_asking[parse-break]`
  - `tests/test_label_genre_gate.py::test_an_answer_that_could_not_be_read_stops_the_asking[unreachable]`

Old text:

```
        if said.answer in published.UNREAD:
            return Words((), said.answer, said.note)
```

New text:

```
        if False:
            return Words((), said.answer, said.note)
```

### `r798-b.G2_a_would_be_hold_is_asked_about_again`

published_words: stop at the first track that publishes a genre whatever the caller needs, so a hold rests on one track's album

- File: `src/cratekit/label/gate.py`
- Source: `r798-b.json`, row `G2_a_would_be_hold_is_asked_about_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`
- Collected: 141 against a baseline of 141
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_release_is_judged_on_as_many_tracks_as_settle_it[a-catalogue-that-refuses-after-a-would-be-hold-holds-nothing]`
  - `tests/test_label_genre_gate.py::test_a_release_is_judged_on_as_many_tracks_as_settle_it[a-release-is-held-only-when-every-track-asked-agrees]`
  - `tests/test_label_genre_gate.py::test_a_release_is_judged_on_as_many_tracks_as_settle_it[a-release-that-would-be-held-is-asked-about-again-before-it-is]`

Old text:

```
    settled = enough if enough is not None else bool
```

New text:

```
    settled = bool
```

### `r815-a.G1_the_asking_gives_up_at_the_bound`

Asking.given_up: one release later than the bound

- File: `src/cratekit/label/gate.py`
- Source: `r815-a.json`, row `G1_the_asking_gives_up_at_the_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`, `tests/test_label_judge.py`
- Collected: 217 against a baseline of 217
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_an_unreachable_catalogue_is_given_up_on_once_for_the_whole_sweep`
  - `tests/test_label_genre_gate.py::test_three_releases_unread_in_a_row_end_the_asking_and_an_answer_resets_it`
  - `tests/test_label_judge.py::test_a_catalogue_unread_three_times_in_a_row_stops_the_run_and_says_how_many_were_left`

Old text:

```
        return self._unread_in_a_row >= UNREAD_IN_A_ROW
```

New text:

```
        return self._unread_in_a_row > UNREAD_IN_A_ROW
```

### `u110-c.C4_go_tail`

The label go tail prints --name RUN again

- File: `src/cratekit/label/go.py`
- Source: `u110-c.json`, row `C4_go_tail`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_names.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_the_label_go_tail_hands_the_run_as_the_pass_and_names_no_batch`

Old text:

```
"--pass", default_name(run_id)]
```

New text:

```
"--name", default_name(run_id)]
```

### `r1890.P10_heard_path_imports_a_writer_part`

The heard path imports rb_nodes, the writer part that writes playlists

- File: `src/cratekit/label/heard.py`
- Source: `r1890.json`, row `P10_heard_path_imports_a_writer_part`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_heard.py::test_nothing_on_the_heard_path_reaches_rekordbox_a_grid_a_tempo_or_a_rating`

Old text:

```
from cratekit.core import config

```

New text:

```
from cratekit.core import config, rb_nodes  # noqa: F401

```

### `u123.H10_year_filter`

Read a release of any year as the dated playlist's

- File: `src/cratekit/label/heard.py`
- Source: `u123.json`, row `H10_year_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_date_no_go_took_anything_on_is_refused`
  - `tests/test_label_heard.py::test_a_release_not_in_the_dated_playlist_is_refused_by_name`
  - `tests/test_label_heard.py::test_the_releases_of_a_dated_playlist_are_the_dated_plans_own`

Old text:

```
            if taken_on == day and (catalogue.by_release.get(identity) or ("",))[0] == year
```

New text:

```
            if taken_on == day and identity in catalogue.by_release
```

### `u123.H11_day_filter`

Read a release taken on any day as the dated playlist's

- File: `src/cratekit/label/heard.py`
- Source: `u123.json`, row `H11_day_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_date_no_go_took_anything_on_is_refused`
  - `tests/test_label_heard.py::test_the_releases_of_a_dated_playlist_are_the_dated_plans_own`

Old text:

```
            if taken_on == day and (catalogue.by_release.get(identity) or ("",))[0] == year
```

New text:

```
            if (catalogue.by_release.get(identity) or ("",))[0] == year
```

### `u123.H12_newly_excludes_heard`

Count a release already heard as newly heard, so a second run writes

- File: `src/cratekit/label/heard.py`
- Source: `u123.json`, row `H12_newly_excludes_heard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_named_release_already_heard_is_said_and_writes_nothing`
  - `tests/test_label_heard.py::test_heard_writes_the_ids_merges_and_removes_and_a_second_run_is_a_no_op`

Old text:

```
    newly = tuple(one for one in target if one not in heard)
```

New text:

```
    newly = tuple(target)
```

### `u123.H13_year_shape`

Accept a two digit year

- File: `src/cratekit/label/heard.py`
- Source: `u123.json`, row `H13_year_shape`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_year_or_date_that_is_not_one_is_refused[argv0]`

Old text:

```
_YEAR = re.compile(r"^\d{4}$")
```

New text:

```
_YEAR = re.compile(r"^\d{2,4}$")
```

### `u123.H14_ambiguous_bound`

Let two playlists with one name through as one, mutate the bound

- File: `src/cratekit/label/heard.py`
- Source: `u123.json`, row `H14_ambiguous_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_heard.py::test_two_playlists_with_the_dated_name_refuse`

Old text:

```
    if len(matching) > 1:
```

New text:

```
    if len(matching) > 2:
```

### `u123.H15_no_year_refusal`

Drop the refusal when there are tracks to add and no year playlist

- File: `src/cratekit/label/heard.py`
- Source: `u123.json`, row `H15_no_year_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_folder_with_no_year_playlist_refuses_when_there_is_something_to_add`

Old text:

```
    if not year_id:
        raise _refused(
```

New text:

```
    if False:
        raise _refused(
```

### `u123.H1_outside_refusal`

Drop the refusal of a --release that is not one of the dated playlist's

- File: `src/cratekit/label/heard.py`
- Source: `u123.json`, row `H1_outside_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_release_not_in_the_dated_playlist_is_refused_by_name`
  - `tests/test_label_heard.py::test_the_plan_refuses_through_the_engine_as_through_the_verb`

Old text:

```
    if outside:
        raise _refused(
```

New text:

```
    if False:
        raise _refused(
```

### `u123.H2_no_releases_refusal`

Drop the refusal when no go took a release that year on that day

- File: `src/cratekit/label/heard.py`
- Source: `u123.json`, row `H2_no_releases_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_date_no_go_took_anything_on_is_refused`

Old text:

```
    releases = releases_of(document, catalogue, year, day)
    if not releases:
```

New text:

```
    releases = releases_of(document, catalogue, year, day)
    if False:
```

### `u123.H3_vouched_before_a_write`

Drop the ledger's vouching before a removal or a take off

- File: `src/cratekit/label/heard.py`
- Source: `u123.json`, row `H3_vouched_before_a_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_dated_playlist_the_ledger_does_not_vouch_for_is_refused`

Old text:

```
    if action in (REMOVE, TAKE_OFF) and not ledger.product_made(cfg, dated_id):
```

New text:

```
    if False:
```

### `u123.H4_unheard_tracks_stay`

Take off every track of the named releases, a shared one with an unheard release too

- File: `src/cratekit/label/heard.py`
- Source: `u123.json`, row `H4_unheard_tracks_stay`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_track_an_unheard_release_also_carries_stays_on_the_dated_playlist`

Old text:

```
        leaving = tracks_of(target) - tracks_of(unheard)
```

New text:

```
        leaving = tracks_of(target)
```

### `u123.H5_missing_holds_the_removal`

Remove the dated playlist even when a track did not reach the year

- File: `src/cratekit/label/heard.py`
- Source: `u123.json`, row `H5_missing_holds_the_removal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_track_the_year_will_not_take_keeps_the_dated_playlist`

Old text:

```
            if done.missing:
                done.kept = True
```

New text:

```
            if False:
                done.kept = True
```

### `u123.H6_heard_recorded`

Never write the heard list

- File: `src/cratekit/label/heard.py`
- Source: `u123.json`, row `H6_heard_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_named_release_already_heard_is_said_and_writes_nothing`
  - `tests/test_label_heard.py::test_a_removal_refused_part_way_names_the_adds_marks_nothing_and_a_resume_finishes`
  - `tests/test_label_heard.py::test_a_track_the_year_will_not_take_keeps_the_dated_playlist`
  - `tests/test_label_heard.py::test_heard_writes_the_ids_merges_and_removes_and_a_second_run_is_a_no_op`
  - `tests/test_label_heard.py::test_marking_heard_with_nothing_to_write_on_a_playlist_made_by_hand_is_not_refused`
  - `tests/test_label_heard.py::test_no_dated_playlist_on_the_account_marks_heard_and_touches_nothing`
  - `tests/test_label_heard.py::test_some_releases_heard_take_their_tracks_off_and_the_last_removes_it`

Old text:

```
        done.recorded = record_heard(cfg, planned.label_id, planned.newly)
```

New text:

```
        done.recorded = 0
```

### `u123.H7_year_adds_recorded`

Do not record the merge's adds on the recorded year

- File: `src/cratekit/label/heard.py`
- Source: `u123.json`, row `H7_year_adds_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_heard.py::test_what_the_merge_adds_to_a_recorded_year_is_recorded_on_it`

Old text:

```
            if planned.year_recorded:
                ledger.record_label_tracks(
```

New text:

```
            if False:
                ledger.record_label_tracks(
```

### `u123.H8_prefixed_year`

Drop the mark's prefixed name from the year fallback

- File: `src/cratekit/label/heard.py`
- Source: `u123.json`, row `H8_prefixed_year`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_year_known_only_by_the_marks_prefixed_name_is_the_year`

Old text:

```
    year_id = year_id or _one_named(inside, year_name, folders.MARK_PREFIX + year_name)
```

New text:

```
    year_id = year_id or _one_named(inside, year_name)
```

### `u123.H9_stray_said`

Never name a dated playlist the ledger records outside the folder

- File: `src/cratekit/label/heard.py`
- Source: `u123.json`, row `H9_stray_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_dated_playlist_the_ledger_records_outside_the_folder_is_said`

Old text:

```
        return replace(base, stray_id=shape.dated.get(name, ""))
```

New text:

```
        return replace(base, stray_id="")
```

### `u123.C1_declined_writes_nothing`

Write on any answer, not only apply

- File: `src/cratekit/label/heard_cli.py`
- Source: `u123.json`, row `C1_declined_writes_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_heard.py::test_declined_nothing_is_written`

Old text:

```
    if option != "apply" or not planned.writes:
```

New text:

```
    if not planned.writes:
```

### `r798-c.H3_every_name_is_resolved_before_any_is_filed`

label held return: skip a name nothing holds and file the rest, so a mistyped identifier leaves a half done run reported as a refusal of nothing

- File: `src/cratekit/label/held_cli.py`
- Source: `r798-c.json`, row `H3_every_name_is_resolved_before_any_is_filed`
- Moved: The refusal over unknown names moved with the name resolution into _found, one level out of the with block, and is raised through _refuse, refuse with the module origin bound; the same if unknown guard raises before anything is filed, and the mutation disables it the same way.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_returning_a_release_nothing_holds_refuses_and_files_none_of_the_others`

Old text:

```
    if unknown:
        raise _refuse(
            "review-item-unknown",
```

New text:

```
    if False:
        raise _refuse(
            "review-item-unknown",
```

### `r798-c.H4_a_release_with_no_isrc_was_not_asked_about`

label held: count a release with no ISRC as one the catalogue was asked about, so it hides a sweep whose every question went unread

- File: `src/cratekit/label/held_cli.py`
- Source: `r798-c.json`, row `H4_a_release_with_no_isrc_was_not_asked_about`
- Moved: _sweep_rows walks the queue through review.iter_items, so the paging loop went and the same test stands one level shallower
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_release_with_no_isrc_does_not_hide_a_sweep_the_catalogue_refused_throughout`

Old text:

```
        if answer is not None and answer not in (searchers.NOT_ASKED, NO_ISRC):
```

New text:

```
        if answer is not None and answer != searchers.NOT_ASKED:
```

### `r798-c.H5_a_returned_hold_is_marked`

label held return: file the release and leave its hold in force, so it is listed as held while it waits in review

- File: `src/cratekit/label/held_cli.py`
- Source: `r798-c.json`, row `H5_a_returned_hold_is_marked`
- Moved: The hold's return mark moved with the per release body into _return_one, two levels out; it is the same call after the offer, and the mutation drops it the same way.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`
- Collected: 141 against a baseline of 141
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_held_release_returned_to_review_is_filed_and_not_held_again`
  - `tests/test_label_genre_gate.py::test_returning_twice_changes_nothing_the_second_time`

Old text:

```
    review.return_hold(store, queue=queue, item_id=one.item_id)
```

New text:

```
    pass
```

### `r815-b.H1_a_withheld_release_returns_under_no_invented_run`

label held return: fall back to the hold's own run for a withheld release

- File: `src/cratekit/label/held_cli.py`
- Source: `r815-b.json`, row `H1_a_withheld_release_returns_under_no_invented_run`
- Moved: The offer call moved into _return_one, two levels out; the same fallback run expression, and the mutation falls back to the hold's own run the same way.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_withheld_release_filed_before_runs_were_recorded_is_returned_under_no_run`

Old text:

```
        or (None if taken_back else one.run_id or None),
```

New text:

```
        or (one.run_id or None),
```

### `r815-b.H2_the_withheld_word_stays_with_the_hold`

label held return: file the hold's payload whole

- File: `src/cratekit/label/held_cli.py`
- Source: `r815-b.json`, row `H2_the_withheld_word_stays_with_the_hold`
- Moved: The returned payload moved into _return_one, two levels out; the same comprehension drops the withheld word, and the mutation files the hold's payload whole the same way.
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_queued_release_of_another_kind_is_held_listed_and_returned`
  - `tests/test_label_judge.py::test_a_withheld_release_filed_before_runs_were_recorded_is_returned_under_no_run`

Old text:

```
        **{k: v for k, v in one.payload.items() if k != review.WITHHELD_FIELD},
```

New text:

```
        **one.payload,
```

### `r815-b.H3_a_judge_runs_answer_is_not_the_sweeps`

_sweep_rows: count a judging job's answer as the sweep's

- File: `src/cratekit/label/held_cli.py`
- Source: `r815-b.json`, row `H3_a_judge_runs_answer_is_not_the_sweeps`
- Moved: _sweep_rows walks the queue through review.iter_items, so the same skip stands one level shallower
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_judge.py::test_label_held_does_not_say_a_sweep_was_refused_over_what_a_judge_run_met`

Old text:

```
        if item.payload.get(genre_gate.GATE_RUN_FIELD):
            continue
```

New text:

```
        if False:
            continue
```

### `r815-b.J1_one_refusal_ends_the_asking`

_asked: remember no refusal

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-b.json`, row `J1_one_refusal_ends_the_asking`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_catalogue_that_refuses_stops_the_run_at_once_and_says_how_many_were_left`

Old text:

```
    if judged.answer == searchers.Answer.BLOCKED.value:
        tools.refused = judged.reason
```

New text:

```
    if False:
        tools.refused = judged.reason
```

### `r815-b.J2_an_unread_catalogue_ends_the_run`

_asked: never stop on the gate's bound of unread releases

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-b.json`, row `J2_an_unread_catalogue_ends_the_run`
- Moved: _asked raises the refused and the given up stops through one refusal; the given up clause is this guard
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_catalogue_unread_three_times_in_a_row_stops_the_run_and_says_how_many_were_left`

Old text:

```
    if tools.refused is not None or tools.asking.given_up:
```

New text:

```
    if tools.refused is not None or False:
```

### `r815-b.J3_a_failing_provider_ends_the_run`

_asked: never stop on the reader's bound of failed reads

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-b.json`, row `J3_a_failing_provider_ends_the_run`
- Moved: the refusal is raised through _refuse, refuse with this module's origin bound, behind the same guard
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_judge.py::test_three_provider_reads_failing_in_a_row_stop_the_run`

Old text:

```
    if tools.reader.given_up:
        raise _refuse(
```

New text:

```
    if False:
        raise _refuse(
```

### `r815-b.J4_a_record_never_holds_on_its_own`

_judged: take a hold from recorded words without asking

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-b.json`, row `J4_a_record_never_holds_on_its_own`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_fresh_answer_with_no_word_takes_the_old_words_off_the_item`
  - `tests/test_label_judge.py::test_a_record_of_one_tracks_album_does_not_hold_a_release_its_next_track_passes`
  - `tests/test_label_judge.py::test_recorded_words_that_would_hold_are_asked_about_before_the_release_is_held`

Old text:

```
    if recorded is not None and not recorded.held:
        return recorded, False
```

New text:

```
    if recorded is not None:
        return recorded, False
```

### `r815-c.J11_the_scope_reads_the_registry`

_Scope.holds: compare the identifier as text

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-c.json`, row `J11_the_scope_reads_the_registry`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_release_filed_under_a_labels_old_identifier_is_in_a_run_scoped_to_the_label`

Old text:

```
        return entry is not None and entry.label_id in self.label_ids
```

New text:

```
        return label_id in self.label_ids
```

### `r815-c.J12_a_release_held_and_gone_is_counted_held`

_left_review: report gone whatever holds the release

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-c.json`, row `J12_a_release_held_and_gone_is_counted_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_release_another_job_held_while_this_one_was_asking_is_counted_held`
  - `tests/test_label_judge.py::test_a_release_held_under_an_earlier_holds_run_is_counted_held_when_it_is_redone`
  - `tests/test_label_judge.py::test_a_run_stopped_part_way_and_resumed_judges_none_twice_and_skips_none[stopped-on-a-held-release]`

Old text:

```
    if standing is not None and standing.state == review.HOLD_HELD:
        return _report(item_id, HELD, _held_already(standing), reason=standing.reason)
```

New text:

```
    if False:
        return _report(item_id, HELD, _held_already(standing), reason=standing.reason)
```

### `r815-c.J13_the_refusal_carries_the_counts`

_resume: let the refusal leave without the summary

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-c.json`, row `J13_the_refusal_carries_the_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_catalogue_that_refuses_stops_the_run_at_once_and_says_how_many_were_left`
  - `tests/test_label_judge.py::test_a_catalogue_unread_three_times_in_a_row_stops_the_run_and_says_how_many_were_left`
  - `tests/test_label_judge.py::test_a_refusal_from_the_provider_parks_the_run_on_that_refusal`
  - `tests/test_label_judge.py::test_a_run_stopped_part_way_and_resumed_judges_none_twice_and_skips_none[stopped-on-a-held-release]`
  - `tests/test_label_judge.py::test_a_run_stopped_part_way_and_resumed_judges_none_twice_and_skips_none[stopped-on-a-passed-release]`
  - `tests/test_label_judge.py::test_a_taxonomy_that_stops_being_readable_parks_the_run_and_fails_no_release`
  - `tests/test_label_judge.py::test_three_provider_reads_failing_in_a_row_stop_the_run`

Old text:

```
            raise _with_summary(failed, cfg, store, queued.job_id) from failed
```

New text:

```
            raise
```

### `r815-c.J5_a_recorded_no_word_answer_is_not_asked_again`

_judged: ask about a release the catalogue already had no word for

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-c.json`, row `J5_a_recorded_no_word_answer_is_not_asked_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_fresh_answer_with_no_word_takes_the_old_words_off_the_item`
  - `tests/test_label_judge.py::test_a_release_the_catalogue_already_had_no_word_for_is_not_asked_about_again[matched]`
  - `tests/test_label_judge.py::test_a_release_the_catalogue_already_had_no_word_for_is_not_asked_about_again[miss]`
  - `tests/test_label_judge.py::test_a_release_the_catalogue_already_had_no_word_for_is_not_asked_about_again[no-isrc]`

Old text:

```
    if recorded is None and isinstance(said, str) and said in genre_gate.NO_WORD_ANSWERS:
```

New text:

```
    if False:
```

### `r815-c.J6_a_decided_item_is_not_judged`

_judge_one: judge an item a person has decided

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-c.json`, row `J6_a_decided_item_is_not_judged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_judge.py::test_an_item_decided_after_the_job_was_queued_is_untouched[accepted]`
  - `tests/test_label_judge.py::test_an_item_decided_after_the_job_was_queued_is_untouched[rejected]`

Old text:

```
        if found.stored_verdict is not None:
            return _report(
```

New text:

```
        if False:
            return _report(
```

### `r815-c.J7_a_returned_release_is_not_judged`

_judge_one: judge a release a person returned

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-c.json`, row `J7_a_returned_release_is_not_judged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_returned_release_is_not_judged_again_and_nobody_is_asked`

Old text:

```
        if genre_gate.returned_by(standing, found.payload):
            return _report(
```

New text:

```
        if False:
            return _report(
```

### `r815-c.J8_a_refusal_parks_and_fails_no_item`

handle: let a refusal fail the item

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-c.json`, row `J8_a_refusal_parks_and_fails_no_item`
- Moved: Same except clause in handle; U298 replaced artifacts.produced(ARTIFACTS, ...) with the bound ARTIFACTS.produced on core.jobs.Artifacts, only the line after the guard
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_catalogue_that_refuses_stops_the_run_at_once_and_says_how_many_were_left`
  - `tests/test_label_judge.py::test_a_catalogue_unread_three_times_in_a_row_stops_the_run_and_says_how_many_were_left`
  - `tests/test_label_judge.py::test_a_refusal_from_the_provider_parks_the_run_on_that_refusal`
  - `tests/test_label_judge.py::test_a_taxonomy_that_stops_being_readable_parks_the_run_and_fails_no_release`
  - `tests/test_label_judge.py::test_three_provider_reads_failing_in_a_row_stop_the_run`

Old text:

```
    except CratekitError as exc:
        raise _parked(job, exc) from exc
    return ARTIFACTS.produced(cfg, job, item, report)
```

New text:

```
    except CratekitError:
        raise
    return ARTIFACTS.produced(cfg, job, item, report)
```

### `r815-c.J9_a_park_drops_the_jobs_tools`

_parked: keep the job's tools across a park

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-c.json`, row `J9_a_park_drops_the_jobs_tools`
- Moved: _parked returns through one conditional after the same pop of the job tools
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_catalogue_that_refuses_stops_the_run_at_once_and_says_how_many_were_left`
  - `tests/test_label_judge.py::test_a_catalogue_unread_three_times_in_a_row_stops_the_run_and_says_how_many_were_left`
  - `tests/test_label_judge.py::test_three_provider_reads_failing_in_a_row_stop_the_run`

Old text:

```
    _JOB_TOOLS.pop(str(job.job_id), None)
    return error if
```

New text:

```
    return error if
```

### `r840-c.C5_the_judging_stamp_is_made_on_the_payload_as_it_stands`

judge_cli._stamp: keep the fields of the item as it was read before the catalogue was asked, so an artist repaired in that time reads its address again

- File: `src/cratekit/label/judge_cli.py`
- Source: `r840-c.json`, row `C5_the_judging_stamp_is_made_on_the_payload_as_it_stands`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_judge.py::test_an_artist_put_right_while_a_release_was_being_judged_is_kept_by_the_stamp`

Old text:

```
        kept = {field: value for field, value in current.items() if field not in _STAMP_FIELDS}
```

New text:

```
        kept = {field: value for field, value in item.payload.items() if field not in _STAMP_FIELDS}
```

### `u217.K11_asked_now_counted_as_reused`

_fresh: drop the short circuit for an answer this run asked, so it counts as reused

- File: `src/cratekit/label/kept_listing.py`
- Source: `u217.json`, row `K11_asked_now_counted_as_reused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`
- Collected: 38 against a baseline of 38
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_a_label_entry_that_changed_reads_the_kept_listing_as_empty[changed0]`
  - `tests/test_label_kept_listing.py::test_a_label_entry_that_changed_reads_the_kept_listing_as_empty[changed1]`
  - `tests/test_label_kept_listing.py::test_a_listing_older_than_the_kept_life_is_asked_again`
  - `tests/test_label_kept_listing.py::test_the_first_listing_says_none_was_kept`

Old text:

```
        if (section, key) in self._asked_now:
            return held

```

New text:

```
(empty)
```

### `u217.K12_flush_batch`

_keep: flush at twice the batch, a coefficient

- File: `src/cratekit/label/kept_listing.py`
- Source: `u217.json`, row `K12_flush_batch`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_the_store_writes_every_flush_batch_as_it_goes`

Old text:

```
        if self._since >= FLUSH_EVERY:
```

New text:

```
        if self._since >= FLUSH_EVERY * 2:
```

### `u217.K1_life_boundary`

_young: keep an answer exactly the kept life old, so a seven day old listing still answers

- File: `src/cratekit/label/kept_listing.py`
- Source: `u217.json`, row `K1_life_boundary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_a_listing_older_than_the_kept_life_is_asked_again`

Old text:

```
    return timedelta(0) <= _now() - held.read_at < kept_for()
```

New text:

```
    return timedelta(0) <= _now() - held.read_at <= kept_for()
```

### `u217.K2_future_is_fresh`

_young: drop the lower bound, so an answer from the future is fresh

- File: `src/cratekit/label/kept_listing.py`
- Source: `u217.json`, row `K2_future_is_fresh`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_a_listing_kept_in_the_future_is_not_fresh`

Old text:

```
    return timedelta(0) <= _now() - held.read_at < kept_for()
```

New text:

```
    return _now() - held.read_at < kept_for()
```

### `u217.K3_life_coefficient`

kept_for: double the kept life, the one number shared with R-1091

- File: `src/cratekit/label/kept_listing.py`
- Source: `u217.json`, row `K3_life_coefficient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_a_listing_older_than_the_kept_life_is_asked_again`

Old text:

```
    return kept_reads.KEPT_FOR
```

New text:

```
    return kept_reads.KEPT_FOR * 2
```

### `u217.K4_changed_entry`

load: read a document kept for another name, match or seeds as this label's listing

- File: `src/cratekit/label/kept_listing.py`
- Source: `u217.json`, row `K4_changed_entry`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`
- Collected: 38 against a baseline of 38
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_a_label_entry_that_changed_reads_the_kept_listing_as_empty[changed0]`
  - `tests/test_label_kept_listing.py::test_a_label_entry_that_changed_reads_the_kept_listing_as_empty[changed1]`

Old text:

```
        if dict(raw["asked_for"]) != asked:
```

New text:

```
        if False:
```

### `u217.K5_seeds_not_asked_for`

asked_for: leave the seeds out, so a changed seed list reuses the old roster

- File: `src/cratekit/label/kept_listing.py`
- Source: `u217.json`, row `K5_seeds_not_asked_for`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_a_label_entry_that_changed_reads_the_kept_listing_as_empty[changed1]`

Old text:

```
        "seeds": [str(seed) for seed in entry.seed_artists],
```

New text:

```
        "seeds": [],
```

### `u217.K6_match_not_asked_for`

asked_for: leave the match out, so discovery's answers for another needle are reused

- File: `src/cratekit/label/kept_listing.py`
- Source: `u217.json`, row `K6_match_not_asked_for`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_a_label_entry_that_changed_reads_the_kept_listing_as_empty[changed0]`

Old text:

```
        "match": str(entry.match or ""),
```

New text:

```
        "match": "",
```

### `u217.K9_release_shape`

_valid: accept any list as a kept listing, whatever its releases hold

- File: `src/cratekit/label/kept_listing.py`
- Source: `u217.json`, row `K9_release_shape`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_a_kept_listing_that_cannot_be_read_refuses_before_any_call[written7]`

Old text:

```
    return isinstance(value, list) and all(_valid_release(one) for one in value)
```

New text:

```
    return isinstance(value, list)
```

### `u217.K10_naive_instant`

_instant: accept an instant with no zone

- File: `src/cratekit/label/kept_reads.py`
- Source: `u217.json`, row `K10_naive_instant`
- Moved: U298 deleted kept_listing's copy of _instant and has KeptListing read through kept_reads._instant, the identical function; the zone check is the same line there
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_a_kept_listing_that_cannot_be_read_refuses_before_any_call[written5]`

Old text:

```
    return moment if moment.tzinfo is not None else None
```

New text:

```
    return moment
```

### `u217.K13_unkept_said`

flush: swallow a refused write without saying it

- File: `src/cratekit/label/kept_reads.py`
- Source: `u217.json`, row `K13_unkept_said`
- Moved: the kept listing's flush and the kept reads' flush were the same code and are now one, kept_reads._Store.flush, which KeptListing inherits; the same line that records a refused write
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_a_write_the_filesystem_refuses_is_said_and_the_listing_still_made`

Old text:

```
            self.unkept = f"{type(exc).__name__}: {exc}"
```

New text:

```
            self.unkept = ""
```

### `u308.L9_store_flushes_nothing`

kept_reads._Store.flush: answers held are never written

- File: `src/cratekit/label/kept_reads.py`
- Source: `u308.json`, row `L9_store_flushes_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`
- Collected: 38 against a baseline of 38
- Kills: 20 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_a_ceiling_stop_inside_discovery_keeps_every_search_it_finished`
  - `tests/test_label_kept_listing.py::test_a_continue_stopped_inside_an_artist_listing_still_costs_less_than_fresh`
  - `tests/test_label_kept_listing.py::test_a_failed_artist_read_in_discovery_still_refuses_rather_than_skipping`
  - `tests/test_label_kept_listing.py::test_a_failed_listing_is_not_kept`
  - `tests/test_label_kept_listing.py::test_a_kept_listing_valid_but_for_its_version_or_label_refuses[label_id-another-label-another-label]`
  - `tests/test_label_kept_listing.py::test_a_kept_listing_valid_but_for_its_version_or_label_refuses[version-2-version 2]`
  - `tests/test_label_kept_listing.py::test_a_kept_seed_the_provider_no_longer_has_is_unread_not_empty`
  - `tests/test_label_kept_listing.py::test_a_label_entry_that_changed_reads_the_kept_listing_as_empty[changed0]`
  - `tests/test_label_kept_listing.py::test_a_label_entry_that_changed_reads_the_kept_listing_as_empty[changed1]`
  - `tests/test_label_kept_listing.py::test_a_listing_just_inside_the_kept_life_is_still_answered`
  - `tests/test_label_kept_listing.py::test_a_listing_older_than_the_kept_life_is_asked_again`
  - `tests/test_label_kept_listing.py::test_a_listing_stopped_at_the_ceiling_continues_with_only_the_unread_part`
  - `tests/test_label_kept_listing.py::test_a_search_that_fails_on_a_continue_is_counted_so_the_line_stays_true`
  - `tests/test_label_kept_listing.py::test_a_second_label_sync_next_of_the_label_makes_no_provider_call`
  - `tests/test_label_kept_listing.py::test_a_second_listing_of_the_same_label_asks_the_provider_nothing`
  - ... and 5 more, see the JSON sidecar

Old text:

```
        if self._unwritten:
            self._write(
```

New text:

```
        if False:
            self._write(
```

### `r1056.N10_pass_not_required`

build_mark: neither --xml nor --pass required, so a bare mark reaches the handler

- File: `src/cratekit/label/mark_cli.py`
- Source: `r1056.json`, row `N10_pass_not_required`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 34 against a baseline of 34
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
- Collected: 34 against a baseline of 34
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
- Collected: 34 against a baseline of 34
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
- Collected: 34 against a baseline of 34
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
- Collected: 34 against a baseline of 34
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
- Collected: 34 against a baseline of 34
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

### `r1056.N6_no_nothing_filed_warning`

label_mark: never say a batch filed none of the built years

- File: `src/cratekit/label/mark_cli.py`
- Source: `r1056.json`, row `N6_no_nothing_filed_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 34 against a baseline of 34
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_bridge_batch_of_another_label_says_it_filed_nothing_too`
  - `tests/test_label_mark_native.py::test_a_pass_whose_landings_filed_none_of_the_built_years_marks_nothing_and_says_so[a-year-never-built]`
  - `tests/test_label_mark_native.py::test_a_pass_whose_landings_filed_none_of_the_built_years_marks_nothing_and_says_so[another-label]`
  - `tests/test_label_mark_native.py::test_a_pass_whose_landings_filed_none_of_the_built_years_marks_nothing_and_says_so[no-label-filed]`

Old text:

```
    if not filed & {year.year for year in built}:
```

New text:

```
    if False:
```

### `r1056.N7_nothing_filed_against_any_year`

label_mark: warn only when the batch filed no year at all, not none of the built ones

- File: `src/cratekit/label/mark_cli.py`
- Source: `r1056.json`, row `N7_nothing_filed_against_any_year`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_pass_whose_landings_filed_none_of_the_built_years_marks_nothing_and_says_so[a-year-never-built]`

Old text:

```
    if not filed & {year.year for year in built}:
```

New text:

```
    if not filed:
```

### `r1056.N8_shown_pass_bare`

_shown: name the native pass with no word that it landed on the database native tree

- File: `src/cratekit/label/mark_cli.py`
- Source: `r1056.json`, row `N8_shown_pass_bare`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 34 against a baseline of 34
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
- Collected: 34 against a baseline of 34
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

### `r835-b.M1_only_the_batch_years_marked`

mark_cli._item: a year the landed batch did not file is marked anyway

- File: `src/cratekit/label/mark_cli.py`
- Source: `r835-b.json`, row `M1_only_the_batch_years_marked`
- Moved: The same guard on the batch's years; its skip item is now built by the local skip helper, so the line after the if returns skip(...) rather than a dict literal.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_year_the_batch_did_not_file_is_left_alone`

Old text:

```
    if year.year not in filed:
        return skip(NOT_IN_BATCH,
```

New text:

```
    if False:
        return skip(NOT_IN_BATCH,
```

### `r835-b.M5_deleted_folder_said`

mark_cli.label_mark: a label folder deleted on the account is listed as if it were there, and the read fails every run

- File: `src/cratekit/label/mark_cli.py`
- Source: `r835-b.json`, row `M5_deleted_folder_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_label_folder_deleted_on_the_account_is_said_not_failed`

Old text:

```
            if shape.folder_id in remote.folders()
```

New text:

```
            if True
```

### `r835-c.M4_recheck_before_rename_again`

mark_cli.label_mark: a title changed between the plan and the write is renamed anyway

- File: `src/cratekit/label/mark_cli.py`
- Source: `r835-c.json`, row `M4_recheck_before_rename_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_title_changed_between_the_plan_and_the_write_is_not_renamed`

Old text:

```
            if now.get(identity) != item["built_as"]:
```

New text:

```
            if False:
```

### `r1091.P6_kept_gone_read_as_release`

_read_one: answer a kept gone release as a release with no tracks, so it is counted undated rather than gone

- File: `src/cratekit/label/playlists_cli.py`
- Source: `r1091.json`, row `P6_kept_gone_read_as_release`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 29 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_batch_of_another_label_marks_nothing_and_reads_no_account`
  - `tests/test_label_playlists.py::test_a_folder_made_by_hand_at_the_root_is_adopted`
  - `tests/test_label_playlists.py::test_a_label_folder_deleted_on_the_account_is_made_again_and_recorded`
  - `tests/test_label_playlists.py::test_a_label_folder_deleted_on_the_account_is_said_not_failed`
  - `tests/test_label_playlists.py::test_a_ledger_written_by_another_verb_keeps_the_label_shape`
  - `tests/test_label_playlists.py::test_a_mark_the_record_cannot_take_names_what_it_took_before`
  - `tests/test_label_playlists.py::test_a_mark_with_no_landed_file_refuses_before_anything`
  - `tests/test_label_playlists.py::test_a_new_year_made_by_hand_under_the_folder_is_reused_not_duplicated`
  - `tests/test_label_playlists.py::test_a_playlist_made_and_not_yet_moved_is_moved_on_the_resume_and_not_made_again`
  - `tests/test_label_playlists.py::test_a_recorded_year_deleted_on_the_account_is_left_alone_not_refused`
  - `tests/test_label_playlists.py::test_a_refusal_part_way_leaves_what_was_written_recorded_and_a_resume_finishes`
  - `tests/test_label_playlists.py::test_a_rejected_session_reading_a_recorded_year_is_raised_not_passed_over`
  - `tests/test_label_playlists.py::test_a_second_mark_plans_nothing_and_a_build_after_it_reuses_the_marked_years`
  - `tests/test_label_playlists.py::test_a_second_mark_says_each_year_is_already_marked`
  - `tests/test_label_playlists.py::test_a_second_run_over_an_unchanged_catalogue_plans_nothing`
  - ... and 14 more, see the JSON sidecar

Old text:

```
        return None if held.gone else (held.tracks, held.year)
```

New text:

```
        return (held.tracks, held.year)
```

### `r835-b.P2_nothing_confirmed_refused`

playlists_cli.read_catalogue: a catalogue that confirmed none of its releases is shown as an empty label

- File: `src/cratekit/label/playlists_cli.py`
- Source: `r835-b.json`, row `P2_nothing_confirmed_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_catalogue_that_confirms_nothing_is_refused_not_shown_empty`

Old text:

```
    if confirmed.dropped and not confirmed.releases:
```

New text:

```
    if False:
```

### `r835-c.P3_unplayable_track_never_asked_again`

playlists_cli.read_catalogue: a track the provider will not play is asked for and refused on every run

- File: `src/cratekit/label/playlists_cli.py`
- Source: `r835-c.json`, row `P3_unplayable_track_never_asked_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_track_the_provider_will_not_play_is_never_planned`

Old text:

```
            if identifier and getattr(row, "available", True) is not False:
```

New text:

```
            if identifier:
```

### `u191.M13_gone_refused`

_grouped: refuse the plan over a release the provider no longer has, instead of counting it

- File: `src/cratekit/label/playlists_cli.py`
- Source: `u191.json`, row `M13_gone_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 35 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_batch_of_another_label_marks_nothing_and_reads_no_account`
  - `tests/test_label_playlists.py::test_a_folder_made_by_hand_at_the_root_is_adopted`
  - `tests/test_label_playlists.py::test_a_label_folder_deleted_on_the_account_is_made_again_and_recorded`
  - `tests/test_label_playlists.py::test_a_label_folder_deleted_on_the_account_is_said_not_failed`
  - `tests/test_label_playlists.py::test_a_ledger_written_by_another_verb_keeps_the_label_shape`
  - `tests/test_label_playlists.py::test_a_mark_the_record_cannot_take_names_what_it_took_before`
  - `tests/test_label_playlists.py::test_a_mark_with_no_landed_file_refuses_before_anything`
  - `tests/test_label_playlists.py::test_a_new_year_made_by_hand_under_the_folder_is_reused_not_duplicated`
  - `tests/test_label_playlists.py::test_a_playlist_made_and_not_yet_moved_is_moved_on_the_resume_and_not_made_again`
  - `tests/test_label_playlists.py::test_a_recorded_year_deleted_on_the_account_is_left_alone_not_refused`
  - `tests/test_label_playlists.py::test_a_refusal_part_way_leaves_what_was_written_recorded_and_a_resume_finishes`
  - `tests/test_label_playlists.py::test_a_rejected_session_reading_a_recorded_year_is_raised_not_passed_over`
  - `tests/test_label_playlists.py::test_a_renamed_label_is_a_different_plan_and_its_approval_is_stale`
  - `tests/test_label_playlists.py::test_a_second_mark_plans_nothing_and_a_build_after_it_reuses_the_marked_years`
  - `tests/test_label_playlists.py::test_a_second_mark_says_each_year_is_already_marked`
  - ... and 20 more, see the JSON sidecar

Old text:

```
            gone += 1
            continue
```

New text:

```
            raise incomplete(entry, "gone")
```

### `u191.M19_unread_listing_accepted`

list_catalogue: plan from a listing read in part (existing guard, moved by this unit)

- File: `src/cratekit/label/playlists_cli.py`
- Source: `u191.json`, row `M19_unread_listing_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_catalogue_read_in_part_is_refused_before_the_gate`

Old text:

```
    if listed.unread:
```

New text:

```
    if False:
```

### `u217.S3_playlists_line`

estimate: carry no listing sentence to the crawl gate

- File: `src/cratekit/label/playlists_cli.py`
- Source: `u217.json`, row `S3_playlists_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_the_playlists_crawl_gate_says_the_listing_was_kept`

Old text:

```
        listing=listed.kept.said() if listed.kept is not None else "",
```

New text:

```
        listing="",
```

### `r1476.M20_named_first_only`

Registry.named: answer only the first holder, as by_name does

- File: `src/cratekit/label/registry.py`
- Source: `r1476.json`, row `M20_named_first_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_files_own_tag_naming_a_shared_name_is_given_neither_labels_genre`
  - `tests/test_label_genre.py::test_a_label_sharing_its_name_with_one_carrying_a_genre_is_never_given_that_genre`
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[ Alpha ]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[ALPHA]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[Alpha]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[alpha]`

Old text:

```
        return tuple(entry for entry in self.labels.values() if _name_key(entry.name) == wanted)
```

New text:

```
        return tuple(entry for entry in self.labels.values() if _name_key(entry.name) == wanted)[:1]
```

### `r790-c.G1_offer_bounded_by_limit`

effective_offer: stop bounding the window by the track limit, so the increment slices what the listing reported

- File: `src/cratekit/label/registry.py`
- Source: `r790-c.json`, row `G1_offer_bounded_by_limit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_the_window_bounds_what_a_sweep_files_and_the_rest_is_counted[a-track-limit-below-the-offer]`

Old text:

```
    return min(offer, effective_limit(entry))
```

New text:

```
    return offer
```

### `r790-c.G2_entry_overrides`

effective_offer: ignore a label's own offer

- File: `src/cratekit/label/registry.py`
- Source: `r790-c.json`, row `G2_entry_overrides`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`
- Collected: 40 against a baseline of 40
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_round_records_the_most_the_label_could_still_offer`
  - `tests/test_label_offer_window.py::test_raising_a_label_offer_after_a_sweep_files_the_difference`
  - `tests/test_label_offer_window.py::test_the_window_bounds_what_a_sweep_files_and_the_rest_is_counted[an-offer-raised-to-thirty-files-thirty]`
  - `tests/test_label_offer_window.py::test_the_window_defaults_to_the_configuration_and_the_entry_overrides_it`

Old text:

```
    offer = entry.offer if entry.offer is not None and entry.offer > 0 else default
```

New text:

```
    offer = default
```

### `r790-c.G3_offer_floor`

check_offer: accept zero at the store

- File: `src/cratekit/label/registry.py`
- Source: `r790-c.json`, row `G3_offer_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_an_offer_below_one_refuses_at_the_store`

Old text:

```
    if isinstance(offer, bool) or not isinstance(offer, int) or offer < 1:
```

New text:

```
    if isinstance(offer, bool) or not isinstance(offer, int) or offer < 0:
```

### `r790-c.G4_offer_read_back`

_entry_from: read every stored offer as unset

- File: `src/cratekit/label/registry.py`
- Source: `r790-c.json`, row `G4_offer_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`
- Collected: 40 against a baseline of 40
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_label_offer_survives_a_rename_and_an_unrelated_edit`
  - `tests/test_label_offer_window.py::test_a_round_records_the_most_the_label_could_still_offer`
  - `tests/test_label_offer_window.py::test_raising_a_label_offer_after_a_sweep_files_the_difference`
  - `tests/test_label_offer_window.py::test_the_registry_says_when_the_track_limit_bounds_an_offer`
  - `tests/test_label_offer_window.py::test_the_window_bounds_what_a_sweep_files_and_the_rest_is_counted[an-offer-raised-to-thirty-files-thirty]`

Old text:

```
        offer=_coerce_int(raw.get("offer")),
```

New text:

```
        offer=None,
```

### `r790-c.G5_rename_keeps_offer`

rename: rebuild the entry field by field without the offer, the shape every copy had before

- File: `src/cratekit/label/registry.py`
- Source: `r790-c.json`, row `G5_rename_keeps_offer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_label_offer_survives_a_rename_and_an_unrelated_edit`

Old text:

```
            current[label_id] = replace(existing, name=new_name)
```

New text:

```
            current[label_id] = LabelEntry(
                label_id=existing.label_id,
                name=new_name,
                match=existing.match,
                seed_artists=existing.seed_artists,
                track_limit=existing.track_limit,
            )
```

### `u177.A1_account_suffix`

bandcamp_account: keep .bandcamp.com on the host, so an address is stored as a host no purchase's seller equals

- File: `src/cratekit/label/registry.py`
- Source: `u177.json`, row `A1_account_suffix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_bandcamp_account.py`
- Collected: 28 against a baseline of 28
- Kills: 8 (killed)
- Killed:
  - `tests/test_label_bandcamp_account.py::test_a_second_label_naming_a_held_account_is_refused_by_the_holders_name`
  - `tests/test_label_bandcamp_account.py::test_an_account_is_looked_up_in_any_form_a_purchase_could_name_it`
  - `tests/test_label_bandcamp_account.py::test_an_address_or_any_case_is_stored_as_the_account_a_purchase_is_read_as[an-account-named-default]`
  - `tests/test_label_bandcamp_account.py::test_an_address_or_any_case_is_stored_as_the_account_a_purchase_is_read_as[https://PulsRomania.bandcamp.com/music]`
  - `tests/test_label_bandcamp_account.py::test_an_address_or_any_case_is_stored_as_the_account_a_purchase_is_read_as[https://pulsromania.bandcamp.com]`
  - `tests/test_label_bandcamp_account.py::test_an_address_or_any_case_is_stored_as_the_account_a_purchase_is_read_as[pulsromania.bandcamp.com/album/sun-path]`
  - `tests/test_label_bandcamp_account.py::test_an_address_or_any_case_is_stored_as_the_account_a_purchase_is_read_as[pulsromania.bandcamp.com]`
  - `tests/test_label_bandcamp_account.py::test_two_labels_naming_one_account_by_hand_answer_no_label`

Old text:

```
    if host.endswith(_ACCOUNT_HOST):
        host = host[: -len(_ACCOUNT_HOST)]
    if not host or not _ACCOUNT.fullmatch(host):

```

New text:

```
    if not host or not _ACCOUNT.fullmatch(host):

```

### `u177.A2_account_shape`

bandcamp_account: drop the shape check, so an account with a space is stored and matches no purchase

- File: `src/cratekit/label/registry.py`
- Source: `u177.json`, row `A2_account_shape`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_bandcamp_account.py`
- Collected: 28 against a baseline of 28
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_bandcamp_account.py::test_a_malformed_stored_account_is_no_account_and_the_label_keeps_the_rest`
  - `tests/test_label_bandcamp_account.py::test_an_account_that_could_match_no_purchase_is_refused_and_writes_nothing[-puls]`
  - `tests/test_label_bandcamp_account.py::test_an_account_that_could_match_no_purchase_is_refused_and_writes_nothing[puls romania]`
  - `tests/test_label_bandcamp_account.py::test_an_account_that_could_match_no_purchase_is_refused_and_writes_nothing[puls_romania]`

Old text:

```
    if not host or not _ACCOUNT.fullmatch(host):

```

New text:

```
    if not host:

```

### `u177.A3_account_case`

bandcamp_account: keep the case typed, so PulsRomania never equals the purchase's pulsromania

- File: `src/cratekit/label/registry.py`
- Source: `u177.json`, row `A3_account_case`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_bandcamp_account.py`
- Collected: 28 against a baseline of 28
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_bandcamp_account.py::test_a_second_label_naming_a_held_account_is_refused_by_the_holders_name`
  - `tests/test_label_bandcamp_account.py::test_an_account_is_looked_up_in_any_form_a_purchase_could_name_it`
  - `tests/test_label_bandcamp_account.py::test_an_address_or_any_case_is_stored_as_the_account_a_purchase_is_read_as[PulsRomania]`
  - `tests/test_label_bandcamp_account.py::test_two_labels_naming_one_account_by_hand_answer_no_label`

Old text:

```
    text = account.strip().lower() if isinstance(account, str) else ""

```

New text:

```
    text = account.strip() if isinstance(account, str) else ""

```

### `u177.A4_claim_removed`

_claim: return at once, so a second label naming a held account is written beside the first

- File: `src/cratekit/label/registry.py`
- Source: `u177.json`, row `A4_claim_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_bandcamp_account.py`
- Collected: 28 against a baseline of 28
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_bandcamp_account.py::test_a_second_label_naming_a_held_account_is_refused_by_the_holders_name`
  - `tests/test_label_bandcamp_account.py::test_the_store_refuses_a_second_claimant_from_a_python_caller`

Old text:

```
    if account is None:
        return
    for other in current.values():

```

New text:

```
    if True:
        return
    for other in current.values():

```

### `u177.A5_claim_self`

_claim: count the label itself as a claimant, so setting its own account again is refused

- File: `src/cratekit/label/registry.py`
- Source: `u177.json`, row `A5_claim_self`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_bandcamp_account.py`
- Collected: 28 against a baseline of 28
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_bandcamp_account.py::test_a_label_setting_its_own_account_again_is_no_conflict`

Old text:

```
        if other.label_id != label_id and other.bandcamp == account:

```

New text:

```
        if other.bandcamp == account:

```

### `u177.A6_first_of_two`

by_bandcamp: answer the first of two claimants, so a hand edited tie stages under a guessed label

- File: `src/cratekit/label/registry.py`
- Source: `u177.json`, row `A6_first_of_two`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_bandcamp_account.py`
- Collected: 28 against a baseline of 28
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_bandcamp_account.py::test_two_labels_naming_one_account_by_hand_answer_no_label`

Old text:

```
        return found[0] if len(found) == 1 else None

```

New text:

```
        return found[0] if found else None

```

### `u177.A7_stored_raw`

_stored_account: keep a stored account as written, so a hand written address matches no purchase

- File: `src/cratekit/label/registry.py`
- Source: `u177.json`, row `A7_stored_raw`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_bandcamp_account.py`
- Collected: 28 against a baseline of 28
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_bandcamp_account.py::test_a_malformed_stored_account_is_no_account_and_the_label_keeps_the_rest`
  - `tests/test_label_bandcamp_account.py::test_two_labels_naming_one_account_by_hand_answer_no_label`

Old text:

```
    try:
        return bandcamp_account(value)
    except CratekitError:
        return None

```

New text:

```
    return value

```

### `u177.A8_edit_drops_account`

edit: keep the held account, so registry set --bandcamp reports a change it never writes

- File: `src/cratekit/label/registry.py`
- Source: `u177.json`, row `A8_edit_drops_account`
- Moved: The checked account reaches edit in the changes; the mutation keeps the held account unless cleared, so set --bandcamp reports a change it never writes.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_bandcamp_account.py`
- Collected: 28 against a baseline of 28
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_bandcamp_account.py::test_default_clears_the_account_and_frees_it_for_another_label`
  - `tests/test_label_bandcamp_account.py::test_set_with_only_bandcamp_is_a_field_to_change`

Old text:

```
            entry = replace(existing, **changes)

```

New text:

```
            entry = replace(existing, **{**changes, "bandcamp": None if clear_bandcamp else existing.bandcamp})

```

### `u178.G1_genre_length_bound`

check_genre: the bound read one past GENRE_MAX, so a 65 character genre is stored

- File: `src/cratekit/label/registry.py`
- Source: `u178.json`, row `G1_genre_length_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_genre_that_could_never_be_one_refuses_at_the_store[xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx]`

Old text:

```
        or len(text) > GENRE_MAX

```

New text:

```
        or len(text) > GENRE_MAX + 1

```

### `u178.G2_genre_needs_a_letter`

check_genre: drop the letter or digit rule, so a punctuation only genre is stored

- File: `src/cratekit/label/registry.py`
- Source: `u178.json`, row `G2_genre_needs_a_letter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_genre_that_could_never_be_one_refuses_at_the_store[---]`

Old text:

```
        or not any(char.isalnum() for char in text)

```

New text:

```
(empty)
```

### `u178.G3_genre_one_line`

check_genre: drop the control character rule, so a genre with a newline is stored

- File: `src/cratekit/label/registry.py`
- Source: `u178.json`, row `G3_genre_one_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_genre_that_could_never_be_one_refuses_at_the_store[Romi\nnimal]`

Old text:

```
        or any(unicodedata.category(char).startswith("C") for char in text)

```

New text:

```
(empty)
```

### `u178.G4_edit_clear_genre`

edit: ignore clear_genre, so --genre default on set keeps the genre

- File: `src/cratekit/label/registry.py`
- Source: `u178.json`, row `G4_edit_clear_genre`
- Moved: The clear flags are folded into the checked changes; the mutation sets the genre as if clear_genre were never given.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_the_word_default_clears_a_genre_and_none_keeps_it`

Old text:

```
            entry = replace(existing, **changes)

```

New text:

```
            entry = replace(existing, **{**changes, "genre": genre if genre is not None else existing.genre})

```

### `u178.G5_edit_none_keeps_genre`

edit: a genre of None drops the held genre, so an unrelated edit clears it

- File: `src/cratekit/label/registry.py`
- Source: `u178.json`, row `G5_edit_none_keeps_genre`
- Moved: The checked changes leave out a genre given as None; the mutation writes the passed genre, so a None genre drops the held one.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_the_word_default_clears_a_genre_and_none_keeps_it`

Old text:

```
            entry = replace(existing, **changes)

```

New text:

```
            entry = replace(existing, **{**changes, "genre": None if clear_genre else genre})

```

### `u308.L7_clear_ignored`

registry._checked: a field set to default keeps what the registry held

- File: `src/cratekit/label/registry.py`
- Source: `u308.json`, row `L7_clear_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_the_word_default_clears_a_genre_and_none_keeps_it`

Old text:

```
    changes.update((key, None) for key, clear in cleared.items() if clear)
```

New text:

```
    pass
```

### `u308.L8_offer_unchecked`

registry._checked: an offer window out of range is stored

- File: `src/cratekit/label/registry.py`
- Source: `u308.json`, row `L8_offer_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_an_offer_below_one_refuses_at_the_store`

Old text:

```
    if offer is not None:
        check_offer(offer)
```

New text:

```
    if False:
        check_offer(offer)
```

### `u308.L5_extended_step_dropped`

review_common.extended: the step the review verbs add to a refusal is dropped

- File: `src/cratekit/label/review_common.py`
- Source: `u308.json`, row `L5_extended_step_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`, `tests/test_label_judge.py`
- Collected: 137 against a baseline of 137
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_artists.py::test_an_answer_between_failures_keeps_the_run_going`
  - `tests/test_label_artists.py::test_the_seams_own_refusal_stops_the_run_and_carries_what_was_repaired`
  - `tests/test_label_artists.py::test_three_reads_failing_in_a_row_stop_the_run_and_say_what_was_left`
  - `tests/test_label_judge.py::test_a_catalogue_unread_three_times_in_a_row_stops_the_run_and_says_how_many_were_left`
  - `tests/test_label_judge.py::test_a_run_stopped_part_way_and_resumed_judges_none_twice_and_skips_none[stopped-on-a-held-release]`
  - `tests/test_label_judge.py::test_a_run_stopped_part_way_and_resumed_judges_none_twice_and_skips_none[stopped-on-a-passed-release]`

Old text:

```
    steps = (*cause.remediation.steps, step)
```

New text:

```
    steps = tuple(cause.remediation.steps)
```

### `u308.L6_ended_outcome_ignored`

review_common.ended: every review verb ends OK whatever outcome it reached

- File: `src/cratekit/label/review_common.py`
- Source: `u308.json`, row `L6_ended_outcome_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_artists.py`, `tests/test_label_genre_gate.py`
- Collected: 259 against a baseline of 259
- Kills: 17 (killed)
- Killed:
  - `tests/test_label_approved.py::test_every_release_held_or_owned_is_a_no_op_that_does_not_claim_the_held_one`
  - `tests/test_label_approved.py::test_every_track_owned_is_a_no_op_and_writes_nothing`
  - `tests/test_label_approved.py::test_nothing_accepted_is_a_no_op_that_never_opens_the_catalogue`
  - `tests/test_label_artists.py::test_a_decided_item_reading_an_address_is_left_as_it_is[accepted]`
  - `tests/test_label_artists.py::test_a_decided_item_reading_an_address_is_left_as_it_is[rejected]`
  - `tests/test_label_artists.py::test_a_queue_with_no_address_opens_no_catalogue`
  - `tests/test_label_artists.py::test_a_release_decided_while_it_was_being_read_is_not_rewritten`
  - `tests/test_label_artists.py::test_a_release_the_provider_does_not_serve_is_counted_and_never_blanked`
  - `tests/test_label_artists.py::test_a_release_the_provider_names_no_artist_for_is_left_reading_what_it_read[   ]`
  - `tests/test_label_artists.py::test_a_release_the_provider_names_no_artist_for_is_left_reading_what_it_read[]`
  - `tests/test_label_artists.py::test_an_artist_put_right_meanwhile_is_not_overwritten`
  - `tests/test_label_artists.py::test_an_empty_queue_is_a_no_op_that_opens_no_catalogue`
  - `tests/test_label_artists.py::test_an_item_whose_artist_is_a_name_is_not_asked_about`
  - `tests/test_label_genre_gate.py::test_a_held_release_returned_to_review_is_filed_and_not_held_again`
  - `tests/test_label_genre_gate.py::test_a_release_filed_before_the_sweep_had_a_gate_is_asked_about_at_approval`
  - ... and 2 more, see the JSON sidecar

Old text:

```
        data={"checks": checks, "summary": summary}, outcome=outcome, warnings=warnings
```

New text:

```
        data={"checks": checks, "summary": summary}, outcome=Outcome.OK, warnings=warnings
```

### `r1634.M10_basis_always_line`

list_for_label, every drop a mismatch: say the answer came from the release's own line even for a lineless one the provider read

- File: `src/cratekit/label/sweep.py`
- Source: `r1634.json`, row `M10_basis_always_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_canary.py::test_every_drop_a_mismatch_over_a_held_release_with_no_line_says_the_provider_was_read`

Old text:

```
            basis = READ_LINE if lined else READ_PROVIDER
```

New text:

```
            basis = READ_LINE
```

### `r1634.M13_rereader_unguarded`

LabelSource._rereader: hand the forced read over bare, so a provider failure on it ends internal-error

- File: `src/cratekit/label/sweep.py`
- Source: `r1634.json`, row `M13_rereader_unguarded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_forced_read_that_raises_fails_the_item_in_the_lookup_vocabulary`

Old text:

```
        return _guarded(lambda claimed, release: catalogue.reread_release(claimed, release))
```

New text:

```
        return lambda claimed, release: catalogue.reread_release(claimed, release)
```

### `r1634.M14_rereader_beside_a_bare_verifier`

LabelSource._rereader: take the catalogue's forced read though a bare verifier was handed in

- File: `src/cratekit/label/sweep.py`
- Source: `r1634.json`, row `M14_rereader_beside_a_bare_verifier`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_source_handed_a_bare_verifier_beside_a_catalogue_forces_no_read`

Old text:

```
        if self.verify is not None or self.catalogue is None:
            return None
```

New text:

```
        if self.catalogue is None:
            return None
```

### `r1634.M15_how_reworded`

Canary.how: the provider basis no longer says the provider was read

- File: `src/cratekit/label/sweep.py`
- Source: `r1634.json`, row `M15_how_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`
- Collected: 37 against a baseline of 37
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_provider_that_answers_with_no_credit_for_the_new_ones_answers_nothing_new`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_passed_over_for_the_next_and_the_label_has_nothing_new`
  - `tests/test_label_canary.py::test_an_unanswered_release_with_no_held_release_to_read_refuses_as_before`
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_though_every_held_line_names_the_label`

Old text:

```
    READ_PROVIDER: "read again from the provider",
```

New text:

```
    READ_PROVIDER: "verified once more",
```

### `r1634.M18_basis_not_in_detail`

Canary.to_json: the worker's detail no longer carries the basis

- File: `src/cratekit/label/sweep.py`
- Source: `r1634.json`, row `M18_basis_not_in_detail`
- Moved: Canary.to_json is the dataclass fields in order, which is the same mapping; the mutation blanks the basis in it.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_though_every_held_line_names_the_label`

Old text:

```
        return asdict(self)

```

New text:

```
        return {**asdict(self), "basis": ""}

```

### `r1634.M19_another_act_replaces_a_gone_one`

list_for_label: a gone answer's second read may go to a held release whose line names another act, which answers mismatch and names that act as the needle

- File: `src/cratekit/label/sweep.py`
- Source: `r1634.json`, row `M19_another_act_replaces_a_gone_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_never_replaced_by_another_acts`

Old text:

```
                one for one in order[1:] if line_reading(one, claimed) != LINE_NAMES_OTHER
```

New text:

```
                one for one in order[1:] if True
```

### `r1634.M1_mismatch_mode_always`

list_for_label: read every listing as all mismatches, so a drop with no credit asks the ordinary verifier, which judges a held label line from its line (the defect)

- File: `src/cratekit/label/sweep.py`
- Source: `r1634.json`, row `M1_mismatch_mode_always`
- Moved: The ordinary verifier branch now also takes a lineless release with no forced read, the former last elif, which asked the same verifier with the same basis; the mutation reads every listing as all mismatches.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`
- Collected: 37 against a baseline of 37
- Kills: 14 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_forced_read_that_raises_fails_the_item_in_the_lookup_vocabulary`
  - `tests/test_label_canary.py::test_a_lone_withdrawn_held_release_refuses`
  - `tests/test_label_canary.py::test_a_provider_that_answers_with_no_credit_for_the_new_ones_answers_nothing_new`
  - `tests/test_label_canary.py::test_a_source_handed_a_bare_verifier_beside_a_catalogue_forces_no_read`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_never_replaced_by_another_acts`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_passed_over_for_the_next_and_the_label_has_nothing_new`
  - `tests/test_label_canary.py::test_an_unanswered_release_with_no_held_release_to_read_refuses_as_before`
  - `tests/test_label_canary.py::test_the_worker_answers_nothing_new_when_the_provider_reads_the_held_release`
  - `tests/test_label_canary.py::test_the_worker_passes_over_a_withdrawn_held_release_too`
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_two_withdrawn_held_releases_refuse_and_no_third_is_read`
  - `tests/test_label_canary.py::test_with_a_drop_given_no_credit_the_held_label_line_comes_before_another_acts`
  - `tests/test_label_canary.py::test_with_no_provider_read_to_hand_a_held_line_counts_as_unverified`

Old text:

```
        if _answered_by_name(dropped) or (reread is None and not lined):
            answered = label_verify.verify_release(claimed, chosen, search=verify)

```

New text:

```
        if True:
            answered = label_verify.verify_release(claimed, chosen, search=verify)

```

### `r1634.M20_in_place_note_dropped`

list_for_label: a release read in a gone one's place no longer says so, so a refusal tells two reads as one

- File: `src/cratekit/label/sweep.py`
- Source: `r1634.json`, row `M20_in_place_note_dropped`
- Moved: The in place note joins the answer notes with a semicolon as the filtered join did; the mutation keeps the answer notes alone, so the note is dropped.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_canary.py::test_two_withdrawn_held_releases_refuse_and_no_third_is_read`

Old text:

```
                said = f"read in place of release {first}, which the provider no longer has"
                notes = str(answered.get("notes") or "")
                answered["notes"] = f"{notes}; {said}" if notes else said

```

New text:

```
                said = f"read in place of release {first}, which the provider no longer has"
                notes = str(answered.get("notes") or "")
                answered["notes"] = notes

```

### `r1634.M2_mismatch_mode_never`

list_for_label: never take the ordinary verifier, so every drop a mismatch forces a provider read it did not need

- File: `src/cratekit/label/sweep.py`
- Source: `r1634.json`, row `M2_mismatch_mode_never`
- Moved: The mismatch test is the first half of the merged condition; the mutation drops it, keeping the lineless no forced read case the old last elif took, so every drop a mismatch goes to the forced read.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`
- Collected: 37 against a baseline of 37
- Kills: 12 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_provider_crediting_another_label_still_answers_nothing_new`
  - `tests/test_label_canary.py::test_a_provider_that_answers_turns_the_same_shape_into_nothing_new`
  - `tests/test_label_canary.py::test_four_held_releases_whose_line_is_the_label_answer_nothing_new`
  - `tests/test_label_canary.py::test_held_releases_whose_lines_name_another_act_still_refuse`
  - `tests/test_label_canary.py::test_the_canary_is_a_held_release_whose_line_the_needle_confirms`
  - `tests/test_label_canary.py::test_the_forced_read_is_asked_only_when_a_drop_is_not_a_mismatch`
  - `tests/test_label_canary.py::test_the_live_shape_answers_nothing_new_rather_than_refusing`
  - `tests/test_label_canary.py::test_the_record_names_the_release_re_verified_and_what_it_answered`
  - `tests/test_label_canary.py::test_the_worker_answers_the_live_shape_as_nothing_new`
  - `tests/test_label_canary.py::test_the_worker_refuses_held_lines_naming_another_act_and_names_the_canary`
  - `tests/test_label_canary.py::test_with_every_drop_a_mismatch_a_held_labels_line_is_asked_before_one_with_none`
  - `tests/test_label_canary.py::test_with_every_held_line_naming_another_act_the_newest_is_asked_and_all_count`

Old text:

```
        if _answered_by_name(dropped) or (reread is None and not lined):
            answered = label_verify.verify_release(claimed, chosen, search=verify)

```

New text:

```
        if reread is None and not lined:
            answered = label_verify.verify_release(claimed, chosen, search=verify)

```

### `r1634.M3_forced_read_dropped`

list_for_label: never take the forced read, so a lined held release counts as unverified and a real nothing new refuses

- File: `src/cratekit/label/sweep.py`
- Source: `r1634.json`, row `M3_forced_read_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_genre_gate.py`, `tests/test_label_offer_window.py`
- Collected: 218 against a baseline of 218
- Kills: 16 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_the_newest_held_release_names_the_label`
  - `tests/test_label_canary.py::test_a_degraded_provider_still_refuses_though_a_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_forced_read_that_raises_fails_the_item_in_the_lookup_vocabulary`
  - `tests/test_label_canary.py::test_a_lone_withdrawn_held_release_refuses`
  - `tests/test_label_canary.py::test_a_provider_that_answers_with_no_credit_for_the_new_ones_answers_nothing_new`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_never_replaced_by_another_acts`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_passed_over_for_the_next_and_the_label_has_nothing_new`
  - `tests/test_label_canary.py::test_an_unanswered_release_with_no_held_release_to_read_refuses_as_before`
  - `tests/test_label_canary.py::test_the_worker_answers_nothing_new_when_the_provider_reads_the_held_release`
  - `tests/test_label_canary.py::test_the_worker_passes_over_a_withdrawn_held_release_too`
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_two_withdrawn_held_releases_refuse_and_no_third_is_read`
  - `tests/test_label_canary.py::test_with_a_drop_given_no_credit_the_held_label_line_comes_before_another_acts`
  - `tests/test_label_genre_gate.py::test_the_catalogue_is_asked_only_about_a_release_that_would_be_filed`
  - ... and 1 more, see the JSON sidecar

Old text:

```
        elif reread is not None:
```

New text:

```
        elif False:
```

### `r1634.M4_no_read_confirms`

list_for_label, no forced read to hand: count a lined held release confirmed rather than unverified

- File: `src/cratekit/label/sweep.py`
- Source: `r1634.json`, row `M4_no_read_confirms`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`
- Collected: 37 against a baseline of 37
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_source_handed_a_bare_verifier_beside_a_catalogue_forces_no_read`
  - `tests/test_label_canary.py::test_with_no_provider_read_to_hand_a_held_line_counts_as_unverified`

Old text:

```
            answered = {"verdict": "unconfirmed", "notes": "no provider read"}
```

New text:

```
            answered = {"verdict": "confirmed", "notes": "no provider read"}
```

### `r1634.M5_no_read_asks_the_line`

list_for_label, no forced read to hand: ask the ordinary verifier for a lined held release, which judges it from its line

- File: `src/cratekit/label/sweep.py`
- Source: `r1634.json`, row `M5_no_read_asks_the_line`
- Moved: The lineless no forced read case moved from its own elif into this condition; the mutation drops its lineless test, so a lined held release with no forced read asks the ordinary verifier.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`
- Collected: 37 against a baseline of 37
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_source_handed_a_bare_verifier_beside_a_catalogue_forces_no_read`
  - `tests/test_label_canary.py::test_with_no_provider_read_to_hand_a_held_line_counts_as_unverified`

Old text:

```
        if _answered_by_name(dropped) or (reread is None and not lined):
            answered = label_verify.verify_release(claimed, chosen, search=verify)

```

New text:

```
        if _answered_by_name(dropped) or reread is None:
            answered = label_verify.verify_release(claimed, chosen, search=verify)

```

### `r1634.M6_gone_not_passed_over`

list_for_label: a gone answer stands, so a withdrawn held release a kept listing still lists refuses a healthy label

- File: `src/cratekit/label/sweep.py`
- Source: `r1634.json`, row `M6_gone_not_passed_over`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`
- Collected: 37 against a baseline of 37
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_passed_over_for_the_next_and_the_label_has_nothing_new`
  - `tests/test_label_canary.py::test_the_worker_passes_over_a_withdrawn_held_release_too`
  - `tests/test_label_canary.py::test_two_withdrawn_held_releases_refuse_and_no_third_is_read`

Old text:

```
            if answered.get("verdict") == RELEASE_GONE and following:
```

New text:

```
            if False and following:
```

### `r1634.M7_any_answer_passed_over`

list_for_label: pass over any answer that is not confirmed, so a degraded provider gets a second read and the cap is spent on every refusal

- File: `src/cratekit/label/sweep.py`
- Source: `r1634.json`, row `M7_any_answer_passed_over`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`
- Collected: 37 against a baseline of 37
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_the_newest_held_release_names_the_label`
  - `tests/test_label_canary.py::test_a_degraded_provider_still_refuses_though_a_held_line_names_the_label`
  - `tests/test_label_canary.py::test_an_unanswered_release_with_no_held_release_to_read_refuses_as_before`
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_over_held_lines_that_name_the_label`
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_though_every_held_line_names_the_label`

Old text:

```
            if answered.get("verdict") == RELEASE_GONE and following:
```

New text:

```
            if answered.get("verdict") != "confirmed" and following:
```

### `r1634.M8_order_label_line_first`

_canary_order, a drop with no credit: rank a held label line ahead of a lineless one (U277's lineless preference lost)

- File: `src/cratekit/label/sweep.py`
- Source: `r1634.json`, row `M8_order_label_line_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`
- Collected: 37 against a baseline of 37
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_the_newest_held_release_names_the_label`
  - `tests/test_label_canary.py::test_a_degraded_provider_still_refuses_though_a_held_line_names_the_label`
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_over_held_lines_that_name_the_label`
  - `tests/test_label_canary.py::test_with_a_drop_the_verifier_gave_no_answer_for_a_held_release_with_no_line_is_asked`

Old text:

```
        return reading != LINE_ABSENT, reading
```

New text:

```
        return False, reading
```

### `r1634.M9_order_other_act_before_label`

_canary_order, a drop with no credit: rank another act's held line ahead of the label's, so a healthy read of a RAWAXXX hold refuses (R-1635)

- File: `src/cratekit/label/sweep.py`
- Source: `r1634.json`, row `M9_order_other_act_before_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`
- Collected: 37 against a baseline of 37
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_provider_that_answers_with_no_credit_for_the_new_ones_answers_nothing_new`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_never_replaced_by_another_acts`
  - `tests/test_label_canary.py::test_an_unanswered_release_with_no_held_release_to_read_refuses_as_before`
  - `tests/test_label_canary.py::test_the_worker_answers_nothing_new_when_the_provider_reads_the_held_release`
  - `tests/test_label_canary.py::test_with_a_drop_given_no_credit_the_held_label_line_comes_before_another_acts`

Old text:

```
        return reading != LINE_ABSENT, reading
```

New text:

```
        return reading != LINE_ABSENT, -reading
```

### `r790-a.S2_held_is_not_refiled`

list_for_label: drop the held check, so a release already in the queue is verified and filed again

- File: `src/cratekit/label/sweep.py`
- Source: `r790-a.json`, row `S2_held_is_not_refiled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`
- Collected: 40 against a baseline of 40
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_held_release_since_downloaded_keeps_its_place`
  - `tests/test_label_offer_window.py::test_a_later_sweep_asks_the_provider_nothing_about_releases_it_already_holds`
  - `tests/test_label_offer_window.py::test_a_release_already_in_the_queue_holds_a_place_and_is_not_verified_again`

Old text:

```
        if identity in offered_ids:
            held += 1
```

New text:

```
        if False:
            held += 1
```

### `r790-a.S4_default_is_the_offer`

list_for_label: default the window to the track limit again, the four hundred R-790 is about

- File: `src/cratekit/label/sweep.py`
- Source: `r790-a.json`, row `S4_default_is_the_offer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`
- Collected: 40 against a baseline of 40
- Kills: 10 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_first_sweep_files_the_default_ten_and_counts_the_other_forty`
  - `tests/test_label_offer_window.py::test_a_label_whose_window_is_already_held_records_its_beyond_with_nothing_filed`
  - `tests/test_label_offer_window.py::test_a_round_records_the_most_the_label_could_still_offer`
  - `tests/test_label_offer_window.py::test_a_run_over_two_labels_counts_what_both_left_beyond`
  - `tests/test_label_offer_window.py::test_a_second_sweep_files_only_the_new_release_and_refiles_nothing`
  - `tests/test_label_offer_window.py::test_a_watermark_past_every_release_still_offers_the_unowned_unoffered_ones`
  - `tests/test_label_offer_window.py::test_raising_a_label_offer_after_a_sweep_files_the_difference`
  - `tests/test_label_offer_window.py::test_the_window_bounds_what_a_sweep_files_and_the_rest_is_counted[an-offer-raised-to-thirty-files-thirty]`
  - `tests/test_label_offer_window.py::test_the_window_bounds_what_a_sweep_files_and_the_rest_is_counted[the-configured-offer-is-every-labels-default]`
  - `tests/test_label_offer_window.py::test_the_window_defaults_to_the_configuration_and_the_entry_overrides_it`

Old text:

```
        else registry.effective_offer(entry, cfg.labels.offer_per_sweep)
```

New text:

```
        else registry.effective_limit(entry)
```

### `r790-b.S7_first_run_kept`

offer_release: stamp the latest run over the one that filed the item

- File: `src/cratekit/label/sweep.py`
- Source: `r790-b.json`, row `S7_first_run_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_the_first_run_stays_the_filing_run_when_an_open_item_is_offered_again`

Old text:

```
        payload[SWEEP_RUN] = held_run or run_id
```

New text:

```
        payload[SWEEP_RUN] = run_id
```

### `r798-b.G3_a_held_release_takes_a_place`

list_for_label: stop counting a held release toward the offer window, so a label of another label's music is read to the end of its catalogue

- File: `src/cratekit/label/sweep.py`
- Source: `r798-b.json`, row `G3_a_held_release_takes_a_place`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`
- Collected: 141 against a baseline of 141
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_held_release_and_a_queued_one_both_take_a_place`
  - `tests/test_label_genre_gate.py::test_a_sweep_that_holds_some_releases_files_no_more_than_the_window`

Old text:

```
        if held + len(gated) + len(candidates) >= cap:
```

New text:

```
        if held + len(candidates) >= cap:
```

### `r798-b.G4_a_returned_hold_is_never_judged`

list_for_label: judge a hold a person returned like any standing hold, so a release they asked for is held again

- File: `src/cratekit/label/sweep.py`
- Source: `r798-b.json`, row `G4_a_returned_hold_is_never_judged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_returned_hold_the_queue_does_not_hold_is_filed_and_never_judged`

Old text:

```
        if standing is not None and standing.state == review.HOLD_RETURNED:
```

New text:

```
        if False:
```

### `r798-b.G5_deleted_on_purpose_outranks_held`

list_for_label: keep the hold on a release tombstoned since, so it stays counted as held

- File: `src/cratekit/label/sweep.py`
- Source: `r798-b.json`, row `G5_deleted_on_purpose_outranks_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_held_release_deleted_on_purpose_since_is_held_no_longer`

Old text:

```
            if was is not None and was.state == review.HOLD_HELD:
```

New text:

```
            if False:
```

### `r798-b.G6_a_released_hold_the_library_owns_is_dropped`

list_for_label: file a released hold without asking whether the library came to own it

- File: `src/cratekit/label/sweep.py`
- Source: `r798-b.json`, row `G6_a_released_hold_the_library_owns_is_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_released_hold_the_library_came_to_own_is_dropped_and_not_filed`

Old text:

```
            elif identity in owned_ids:
```

New text:

```
            elif False:
```

### `r798-b.G8_a_standing_hold_counts_for_the_canary`

list_for_label: leave standing holds out of the releases a dead verifier could not confirm again, so a window of holds hides one

- File: `src/cratekit/label/sweep.py`
- Source: `r798-b.json`, row `G8_a_standing_hold_counts_for_the_canary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_dead_verifier_over_a_window_of_standing_holds_refuses`

Old text:

```
            held_unconfirmed = held + sum(1 for one in gated if one.standing)
```

New text:

```
            held_unconfirmed = held
```

### `r815-b.S1_a_sweep_keeps_a_withheld_hold`

list_for_label: drop a withheld hold the window does not reach, as any other

- File: `src/cratekit/label/sweep.py`
- Source: `r815-b.json`, row `S1_a_sweep_keeps_a_withheld_hold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_withheld_release_the_window_does_not_reach_is_not_dropped_when_its_kind_changes`

Old text:

```
            if standing.payload.get(review.WITHHELD_FIELD):
                continue
```

New text:

```
            if False:
                continue
```

### `u217.S1_summary_dropped`

kept_of: never carry the roster's summary onto the sweep's listing

- File: `src/cratekit/label/sweep.py`
- Source: `u217.json`, row `S1_summary_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`
- Collected: 38 against a baseline of 38
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_a_second_label_sync_next_of_the_label_makes_no_provider_call`
  - `tests/test_label_kept_listing.py::test_label_playlists_after_a_sync_listing_asks_no_listing`
  - `tests/test_label_kept_listing.py::test_the_playlists_crawl_gate_says_the_listing_was_kept`

Old text:

```
    return held if isinstance(held, kept_listing.Summary) else None
```

New text:

```
    return None
```

### `u238.M4_beyond_leaves_out_unchecked`

list_for_label: beyond is the label's own only, so the recorded round drops every unchecked release

- File: `src/cratekit/label/sweep.py`
- Source: `u238.json`, row `M4_beyond_leaves_out_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`
- Collected: 40 against a baseline of 40
- Kills: 15 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_first_sweep_files_the_default_ten_and_counts_the_other_forty`
  - `tests/test_label_offer_window.py::test_a_label_whose_window_is_already_held_records_its_beyond_with_nothing_filed`
  - `tests/test_label_offer_window.py::test_a_release_already_in_the_queue_holds_a_place_and_is_not_verified_again`
  - `tests/test_label_offer_window.py::test_a_release_with_no_copyright_line_is_unchecked_never_dropped`
  - `tests/test_label_offer_window.py::test_a_round_records_the_most_the_label_could_still_offer`
  - `tests/test_label_offer_window.py::test_a_run_over_two_labels_counts_what_both_left_beyond`
  - `tests/test_label_offer_window.py::test_a_second_sweep_files_only_the_new_release_and_refiles_nothing`
  - `tests/test_label_offer_window.py::test_a_tombstoned_release_takes_no_place_in_the_window`
  - `tests/test_label_offer_window.py::test_a_watermark_past_every_release_still_offers_the_unowned_unoffered_ones`
  - `tests/test_label_offer_window.py::test_an_owned_release_takes_no_place_in_the_window`
  - `tests/test_label_offer_window.py::test_past_the_window_counts_only_the_labels_own_releases_and_the_unchecked`
  - `tests/test_label_offer_window.py::test_the_count_past_the_window_uses_the_labels_match_needle`
  - `tests/test_label_offer_window.py::test_the_window_bounds_what_a_sweep_files_and_the_rest_is_counted[a-track-limit-below-the-offer]`
  - `tests/test_label_offer_window.py::test_the_window_bounds_what_a_sweep_files_and_the_rest_is_counted[an-offer-raised-to-thirty-files-thirty]`
  - `tests/test_label_offer_window.py::test_the_window_bounds_what_a_sweep_files_and_the_rest_is_counted[the-configured-offer-is-every-labels-default]`

Old text:

```
        beyond=own_past + unchecked_past,
```

New text:

```
        beyond=own_past,
```

### `u238.M5_window_edge_off_by_one`

list_for_label: start the count one release past the window's edge

- File: `src/cratekit/label/sweep.py`
- Source: `u238.json`, row `M5_window_edge_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`
- Collected: 40 against a baseline of 40
- Kills: 12 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_first_sweep_files_the_default_ten_and_counts_the_other_forty`
  - `tests/test_label_offer_window.py::test_a_label_whose_window_is_already_held_records_its_beyond_with_nothing_filed`
  - `tests/test_label_offer_window.py::test_a_release_already_in_the_queue_holds_a_place_and_is_not_verified_again`
  - `tests/test_label_offer_window.py::test_a_release_with_no_copyright_line_is_unchecked_never_dropped`
  - `tests/test_label_offer_window.py::test_a_run_over_two_labels_counts_what_both_left_beyond`
  - `tests/test_label_offer_window.py::test_a_second_sweep_files_only_the_new_release_and_refiles_nothing`
  - `tests/test_label_offer_window.py::test_a_tombstoned_release_takes_no_place_in_the_window`
  - `tests/test_label_offer_window.py::test_a_watermark_past_every_release_still_offers_the_unowned_unoffered_ones`
  - `tests/test_label_offer_window.py::test_an_owned_release_takes_no_place_in_the_window`
  - `tests/test_label_offer_window.py::test_the_window_bounds_what_a_sweep_files_and_the_rest_is_counted[a-track-limit-below-the-offer]`
  - `tests/test_label_offer_window.py::test_the_window_bounds_what_a_sweep_files_and_the_rest_is_counted[an-offer-raised-to-thirty-files-thirty]`
  - `tests/test_label_offer_window.py::test_the_window_bounds_what_a_sweep_files_and_the_rest_is_counted[the-configured-offer-is-every-labels-default]`

Old text:

```
    own_past, unchecked_past = _past_window(listed[examined:], claimed)
```

New text:

```
    own_past, unchecked_past = _past_window(listed[examined + 1:], claimed)
```

### `u238.M6_needle_ignored`

list_for_label: judge the lines past the window by the label's name, not its --match needle

- File: `src/cratekit/label/sweep.py`
- Source: `u238.json`, row `M6_needle_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_the_count_past_the_window_uses_the_labels_match_needle`

Old text:

```
    own_past, unchecked_past = _past_window(listed[examined:], claimed)
```

New text:

```
    own_past, unchecked_past = _past_window(listed[examined:], entry.name)
```

### `u277.M2_no_line_before_the_labels_line`

line_reading order: rank a held release with no line ahead of one whose line names the label

- File: `src/cratekit/label/sweep.py`
- Source: `u277.json`, row `M2_no_line_before_the_labels_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`
- Collected: 37 against a baseline of 37
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_provider_that_answers_turns_the_same_shape_into_nothing_new`
  - `tests/test_label_canary.py::test_with_every_drop_a_mismatch_a_held_labels_line_is_asked_before_one_with_none`

Old text:

```
LINE_NAMES_LABEL = 0
LINE_ABSENT = 1
```

New text:

```
LINE_NAMES_LABEL = 1
LINE_ABSENT = 0
```

### `u277.M3_another_label_before_no_line`

line_reading order: rank a held release whose line names another label ahead of one with no line

- File: `src/cratekit/label/sweep.py`
- Source: `u277.json`, row `M3_another_label_before_no_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_offer_window.py`
- Collected: 77 against a baseline of 77
- Kills: 10 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_provider_that_answers_with_no_credit_for_the_new_ones_answers_nothing_new`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_never_replaced_by_another_acts`
  - `tests/test_label_canary.py::test_an_unanswered_release_with_no_held_release_to_read_refuses_as_before`
  - `tests/test_label_canary.py::test_every_drop_a_mismatch_over_a_held_release_with_no_line_says_the_provider_was_read`
  - `tests/test_label_canary.py::test_the_worker_answers_nothing_new_when_the_provider_reads_the_held_release`
  - `tests/test_label_canary.py::test_with_a_drop_given_no_credit_the_held_label_line_comes_before_another_acts`
  - `tests/test_label_canary.py::test_with_no_held_line_naming_the_label_a_held_release_with_no_line_comes_next`
  - `tests/test_label_offer_window.py::test_a_round_records_the_most_the_label_could_still_offer`
  - `tests/test_label_offer_window.py::test_past_the_window_counts_only_the_labels_own_releases_and_the_unchecked`
  - `tests/test_label_offer_window.py::test_the_count_past_the_window_uses_the_labels_match_needle`

Old text:

```
LINE_NAMES_OTHER = 2
```

New text:

```
LINE_NAMES_OTHER = 1
```

### `u277.M4_canary_answer_ignored`

list_for_label: never count the held releases unconfirmed, whatever the canary answered, so a dead verifier reads as nothing new

- File: `src/cratekit/label/sweep.py`
- Source: `u277.json`, row `M4_canary_answer_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_genre_gate.py`, `tests/test_label_offer_window.py`
- Collected: 218 against a baseline of 218
- Kills: 17 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_the_newest_held_release_names_the_label`
  - `tests/test_label_canary.py::test_a_degraded_provider_still_refuses_though_a_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_lone_withdrawn_held_release_refuses`
  - `tests/test_label_canary.py::test_a_source_handed_a_bare_verifier_beside_a_catalogue_forces_no_read`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_never_replaced_by_another_acts`
  - `tests/test_label_canary.py::test_an_unanswered_release_with_no_held_release_to_read_refuses_as_before`
  - `tests/test_label_canary.py::test_held_releases_whose_lines_name_another_act_still_refuse`
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_over_held_lines_that_name_the_label`
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_the_worker_refuses_held_lines_naming_another_act_and_names_the_canary`
  - `tests/test_label_canary.py::test_two_withdrawn_held_releases_refuse_and_no_third_is_read`
  - `tests/test_label_canary.py::test_with_a_drop_the_verifier_gave_no_answer_for_a_held_release_with_no_line_is_asked`
  - `tests/test_label_canary.py::test_with_every_held_line_naming_another_act_the_newest_is_asked_and_all_count`
  - `tests/test_label_canary.py::test_with_no_provider_read_to_hand_a_held_line_counts_as_unverified`
  - ... and 2 more, see the JSON sidecar

Old text:

```
        if not canary.confirmed:
            held_unconfirmed
```

New text:

```
        if False:
            held_unconfirmed
```

### `u277.M5_only_a_mismatch_is_unconfirmed`

Canary.confirmed: read anything but a mismatch as confirmed, so an unconfirmed answer from a dead verifier passes

- File: `src/cratekit/label/sweep.py`
- Source: `u277.json`, row `M5_only_a_mismatch_is_unconfirmed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_genre_gate.py`, `tests/test_label_offer_window.py`
- Collected: 218 against a baseline of 218
- Kills: 14 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_the_newest_held_release_names_the_label`
  - `tests/test_label_canary.py::test_a_degraded_provider_still_refuses_though_a_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_lone_withdrawn_held_release_refuses`
  - `tests/test_label_canary.py::test_a_source_handed_a_bare_verifier_beside_a_catalogue_forces_no_read`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_never_replaced_by_another_acts`
  - `tests/test_label_canary.py::test_an_unanswered_release_with_no_held_release_to_read_refuses_as_before`
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_over_held_lines_that_name_the_label`
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_two_withdrawn_held_releases_refuse_and_no_third_is_read`
  - `tests/test_label_canary.py::test_with_a_drop_the_verifier_gave_no_answer_for_a_held_release_with_no_line_is_asked`
  - `tests/test_label_canary.py::test_with_no_provider_read_to_hand_a_held_line_counts_as_unverified`
  - `tests/test_label_genre_gate.py::test_a_dead_verifier_over_a_window_of_standing_holds_refuses`
  - `tests/test_label_offer_window.py::test_a_dead_verifier_on_a_later_sweep_refuses_rather_than_reporting_nothing_new`

Old text:

```
        return self.verdict == "confirmed"
```

New text:

```
        return self.verdict != "mismatch"
```

### `u277.M6_canary_asked_beside_candidates`

list_for_label: ask the canary even when the sweep confirmed a candidate, one provider call a sweep more

- File: `src/cratekit/label/sweep.py`
- Source: `u277.json`, row `M6_canary_asked_beside_candidates`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_canary.py::test_no_canary_is_asked_when_the_sweep_confirmed_something`

Old text:

```
    if held_releases and dropped and not candidates:
```

New text:

```
    if held_releases and dropped:
```

### `u277.M7_standing_hold_not_a_canary`

list_for_label: leave a standing genre gate hold out of the releases the canary is chosen from

- File: `src/cratekit/label/sweep.py`
- Source: `u277.json`, row `M7_standing_hold_not_a_canary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_dead_verifier_over_a_window_of_standing_holds_refuses`

Old text:

```
                gated.append(Gated(_candidate(entry, release), again, standing=True))
                held_releases.append(release)
```

New text:

```
                gated.append(Gated(_candidate(entry, release), again, standing=True))
```

### `u277.M8_past_window_counts_other_labels`

_past_window: count a release whose line names another label as the label's own past the window (the shared reading, U238)

- File: `src/cratekit/label/sweep.py`
- Source: `u277.json`, row `M8_past_window_counts_other_labels`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`
- Collected: 40 against a baseline of 40
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_round_records_the_most_the_label_could_still_offer`
  - `tests/test_label_offer_window.py::test_past_the_window_counts_only_the_labels_own_releases_and_the_unchecked`
  - `tests/test_label_offer_window.py::test_the_count_past_the_window_uses_the_labels_match_needle`

Old text:

```
        elif reading == LINE_NAMES_LABEL:
            own += 1
```

New text:

```
        else:
            own += 1
```

### `u277.M9_canary_notes_dropped`

list_for_label: keep the canary's verdict and lose its notes, so a mismatch no longer says whom the release is credited to

- File: `src/cratekit/label/sweep.py`
- Source: `u277.json`, row `M9_canary_notes_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`
- Collected: 37 against a baseline of 37
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_degraded_provider_still_refuses_though_a_held_line_names_the_label`
  - `tests/test_label_canary.py::test_held_releases_whose_lines_name_another_act_still_refuse`
  - `tests/test_label_canary.py::test_the_worker_refuses_held_lines_naming_another_act_and_names_the_canary`
  - `tests/test_label_canary.py::test_two_withdrawn_held_releases_refuse_and_no_third_is_read`

Old text:

```
            notes=str(answered.get("notes") or ""),
```

New text:

```
            notes="",
```

### `u52-item-derivation.A3_label_source_acquires`

Declare the labels source an acquiring one, which is the state R-140 was recorded against

- File: `src/cratekit/label/sweep.py`
- Source: `u52-item-derivation.json`, row `A3_label_source_acquires`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`
- Collected: 31 against a baseline of 31
- Kills: 2 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_the_label_source_declares_that_it_does_not_acquire`
  - `tests/test_incremental_sync.py::test_the_labels_spec_agrees_with_the_source_that_offers`

Old text:

```
    acquires = False
```

New text:

```
    acquires = True
```

### `r1634.M17_check_drops_how`

label sync --next: the reverified line no longer says how the release was asked

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1634.json`, row `M17_check_drops_how`
- Moved: the reverified check call was compressed one level, so the same line stands four spaces shallower
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`
- Collected: 37 against a baseline of 37
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_provider_crediting_another_label_still_answers_nothing_new`
  - `tests/test_label_canary.py::test_a_provider_that_answers_with_no_credit_for_the_new_ones_answers_nothing_new`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_passed_over_for_the_next_and_the_label_has_nothing_new`
  - `tests/test_label_canary.py::test_an_unanswered_release_with_no_held_release_to_read_refuses_as_before`

Old text:

```
            f"{listing.canary.how()}: {listing.canary.said()}",
```

New text:

```
            f": {listing.canary.said()}",
```

### `u277.M10_next_says_no_canary`

_listing_checks: never say the reverified line, so --next is silent about which release it re-verified

- File: `src/cratekit/label/sync_cli.py`
- Source: `u277.json`, row `M10_next_says_no_canary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`
- Collected: 37 against a baseline of 37
- Kills: 12 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_the_newest_held_release_names_the_label`
  - `tests/test_label_canary.py::test_a_degraded_provider_still_refuses_though_a_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_provider_crediting_another_label_still_answers_nothing_new`
  - `tests/test_label_canary.py::test_a_provider_that_answers_turns_the_same_shape_into_nothing_new`
  - `tests/test_label_canary.py::test_a_provider_that_answers_with_no_credit_for_the_new_ones_answers_nothing_new`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_never_replaced_by_another_acts`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_passed_over_for_the_next_and_the_label_has_nothing_new`
  - `tests/test_label_canary.py::test_an_unanswered_release_with_no_held_release_to_read_refuses_as_before`
  - `tests/test_label_canary.py::test_held_releases_whose_lines_name_another_act_still_refuse`
  - `tests/test_label_canary.py::test_the_record_names_the_release_re_verified_and_what_it_answered`
  - `tests/test_label_canary.py::test_two_withdrawn_held_releases_refuse_and_no_third_is_read`

Old text:

```
    if listing.canary is not None:
```

New text:

```
    if False:
```

### `r1634.M11_reread_reads_the_line`

TidalCatalogue.reread_release: judge the listed object's own line instead of reading the album

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r1634.json`, row `M11_reread_reads_the_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`
- Collected: 37 against a baseline of 37
- Kills: 15 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_the_newest_held_release_names_the_label`
  - `tests/test_label_canary.py::test_a_degraded_provider_still_refuses_though_a_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_lone_withdrawn_held_release_refuses`
  - `tests/test_label_canary.py::test_a_provider_that_answers_with_no_credit_for_the_new_ones_answers_nothing_new`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_never_replaced_by_another_acts`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_passed_over_for_the_next_and_the_label_has_nothing_new`
  - `tests/test_label_canary.py::test_an_unanswered_release_with_no_held_release_to_read_refuses_as_before`
  - `tests/test_label_canary.py::test_the_shipped_reread_of_a_release_the_provider_no_longer_has_is_no_credit`
  - `tests/test_label_canary.py::test_the_shipped_reread_reads_the_provider_though_the_release_carries_a_line`
  - `tests/test_label_canary.py::test_the_worker_answers_nothing_new_when_the_provider_reads_the_held_release`
  - `tests/test_label_canary.py::test_the_worker_passes_over_a_withdrawn_held_release_too`
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_two_withdrawn_held_releases_refuse_and_no_third_is_read`
  - `tests/test_label_canary.py::test_with_a_drop_given_no_credit_the_held_label_line_comes_before_another_acts`

Old text:

```
            album = self._album(identity)
        except ReleaseUnresolvable as exc:
```

New text:

```
            album = release
        except ReleaseUnresolvable as exc:
```

### `r1634.M12_gone_confirms`

TidalCatalogue.reread_release: answer a withdrawn release confirmed

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r1634.json`, row `M12_gone_confirms`
- Moved: The gone answer of reread_release is the same dict built by the _unanswered helper; the verdict argument is the guarded value, and the mutation answers a withdrawn release confirmed as before.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`
- Collected: 37 against a baseline of 37
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_lone_withdrawn_held_release_refuses`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_never_replaced_by_another_acts`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_passed_over_for_the_next_and_the_label_has_nothing_new`
  - `tests/test_label_canary.py::test_the_shipped_reread_of_a_release_the_provider_no_longer_has_is_no_credit`
  - `tests/test_label_canary.py::test_the_worker_passes_over_a_withdrawn_held_release_too`
  - `tests/test_label_canary.py::test_two_withdrawn_held_releases_refuse_and_no_third_is_read`

Old text:

```
            return _unanswered(RELEASE_GONE, str(exc))

```

New text:

```
            return _unanswered("confirmed", str(exc))

```

### `u206.M18_catalogue_keeps_any_gone`

TidalCatalogue.tracks_for_isrc: keep every failure _gone reads as a not found, a FileNotFoundError among them

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u206.json`, row `M18_catalogue_keeps_any_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`
- Collected: 60 against a baseline of 60
- Kills: 2 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_the_catalogue_answers_a_class_named_not_found_as_before_and_keeps_nothing[file]`
  - `tests/test_isrc_cache.py::test_the_catalogue_answers_a_class_named_not_found_as_before_and_keeps_nothing[module]`

Old text:

```
                    if isrc_cache.said_not_found(exc):
                        answered.append(())
```

New text:

```
                    if True:
                        answered.append(())
```

### `u207.A2_catalogue_ignores_screen`

TidalCatalogue.tracks_for_isrc: a code the screen answered absent is asked again

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u207.json`, row `A2_catalogue_ignores_screen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_the_catalogue_answers_a_screened_absent_code_as_no_track_with_no_request`

Old text:

```
        if self._screen.absent(wanted):
```

New text:

```
        if False:
```

### `u217.A1_flush_on_the_way_out`

artist_for: drop the flush in the finally, so a ceiling stop before a batch keeps nothing

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u217.json`, row `A1_flush_on_the_way_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`
- Collected: 38 against a baseline of 38
- Kills: 12 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_a_ceiling_stop_inside_discovery_keeps_every_search_it_finished`
  - `tests/test_label_kept_listing.py::test_a_continue_stopped_inside_an_artist_listing_still_costs_less_than_fresh`
  - `tests/test_label_kept_listing.py::test_a_failed_artist_read_in_discovery_still_refuses_rather_than_skipping`
  - `tests/test_label_kept_listing.py::test_a_failed_listing_is_not_kept`
  - `tests/test_label_kept_listing.py::test_a_kept_seed_the_provider_no_longer_has_is_unread_not_empty`
  - `tests/test_label_kept_listing.py::test_a_listing_just_inside_the_kept_life_is_still_answered`
  - `tests/test_label_kept_listing.py::test_a_listing_stopped_at_the_ceiling_continues_with_only_the_unread_part`
  - `tests/test_label_kept_listing.py::test_a_search_that_fails_on_a_continue_is_counted_so_the_line_stays_true`
  - `tests/test_label_kept_listing.py::test_a_second_label_sync_next_of_the_label_makes_no_provider_call`
  - `tests/test_label_kept_listing.py::test_a_second_listing_of_the_same_label_asks_the_provider_nothing`
  - `tests/test_label_kept_listing.py::test_label_playlists_after_a_sync_listing_asks_no_listing`
  - `tests/test_label_kept_listing.py::test_the_playlists_crawl_gate_says_the_listing_was_kept`

Old text:

```
        finally:
            kept.flush()
```

New text:

```
        finally:
            pass
```

### `u217.A2_roster_lists_now`

_roster: hand the roster no lister, so every member is paged again after discovery

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u217.json`, row `A2_roster_lists_now`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`
- Collected: 38 against a baseline of 38
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_a_continue_stopped_inside_an_artist_listing_still_costs_less_than_fresh`
  - `tests/test_label_kept_listing.py::test_a_kept_seed_the_provider_no_longer_has_is_unread_not_empty`
  - `tests/test_label_kept_listing.py::test_a_listing_the_client_does_not_expose_stays_unread_on_every_run`
  - `tests/test_label_kept_listing.py::test_a_second_listing_of_the_same_label_asks_the_provider_nothing`
  - `tests/test_label_kept_listing.py::test_label_playlists_after_a_sync_listing_asks_no_listing`
  - `tests/test_label_kept_listing.py::test_the_first_listing_pages_each_discovered_artist_once`

Old text:

```
            lister=lambda artist, method, missing: self._listed(kept, artist, method, missing),
```

New text:

```
            lister=None,
```

### `u217.A3_listing_not_kept`

_listed: never keep a listing it asked

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u217.json`, row `A3_listing_not_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`
- Collected: 38 against a baseline of 38
- Kills: 12 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_a_continue_stopped_inside_an_artist_listing_still_costs_less_than_fresh`
  - `tests/test_label_kept_listing.py::test_a_failed_artist_read_in_discovery_still_refuses_rather_than_skipping`
  - `tests/test_label_kept_listing.py::test_a_failed_listing_is_not_kept`
  - `tests/test_label_kept_listing.py::test_a_kept_seed_the_provider_no_longer_has_is_unread_not_empty`
  - `tests/test_label_kept_listing.py::test_a_listing_just_inside_the_kept_life_is_still_answered`
  - `tests/test_label_kept_listing.py::test_a_search_that_fails_on_a_continue_is_counted_so_the_line_stays_true`
  - `tests/test_label_kept_listing.py::test_a_second_label_sync_next_of_the_label_makes_no_provider_call`
  - `tests/test_label_kept_listing.py::test_a_second_listing_of_the_same_label_asks_the_provider_nothing`
  - `tests/test_label_kept_listing.py::test_label_playlists_after_a_sync_listing_asks_no_listing`
  - `tests/test_label_kept_listing.py::test_the_first_listing_pages_each_discovered_artist_once`
  - `tests/test_label_kept_listing.py::test_the_playlists_crawl_gate_says_the_listing_was_kept`
  - `tests/test_label_kept_listing.py::test_the_store_writes_every_flush_batch_as_it_goes`

Old text:

```
            kept.keep_listed(identity, method, rows)
```

New text:

```
            kept.asked_unkept()
```

### `u217.A4_search_not_kept`

_credited_by: never keep a discovery album search

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u217.json`, row `A4_search_not_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`
- Collected: 38 against a baseline of 38
- Kills: 10 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_a_ceiling_stop_inside_discovery_keeps_every_search_it_finished`
  - `tests/test_label_kept_listing.py::test_a_continue_stopped_inside_an_artist_listing_still_costs_less_than_fresh`
  - `tests/test_label_kept_listing.py::test_a_listing_just_inside_the_kept_life_is_still_answered`
  - `tests/test_label_kept_listing.py::test_a_listing_stopped_at_the_ceiling_continues_with_only_the_unread_part`
  - `tests/test_label_kept_listing.py::test_a_search_that_fails_on_a_continue_is_counted_so_the_line_stays_true`
  - `tests/test_label_kept_listing.py::test_a_second_label_sync_next_of_the_label_makes_no_provider_call`
  - `tests/test_label_kept_listing.py::test_a_second_listing_of_the_same_label_asks_the_provider_nothing`
  - `tests/test_label_kept_listing.py::test_label_playlists_after_a_sync_listing_asks_no_listing`
  - `tests/test_label_kept_listing.py::test_the_playlists_crawl_gate_says_the_listing_was_kept`
  - `tests/test_label_kept_listing.py::test_the_store_writes_every_flush_batch_as_it_goes`

Old text:

```
        kept.keep_searched(query, credited)
```

New text:

```
        kept.asked_unkept()
```

### `u217.A5_name_not_kept`

_member_named: never keep an exact name found

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u217.json`, row `A5_name_not_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_a_second_label_sync_next_of_the_label_makes_no_provider_call`

Old text:

```
            kept.keep_named(name, ((identity, str(getattr(artist, "name", "") or "")),))
```

New text:

```
            kept.asked_unkept()
```

### `u217.A6_need_object`

_discover: never read a kept artist's object before its listing's skip

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u217.json`, row `A6_need_object`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_a_failed_artist_read_in_discovery_still_refuses_rather_than_skipping`

Old text:

```
                need_object=not all(
```

New text:

```
                need_object=False and not all(
```

### `u217.A7_missing_method_kept`

_listed: keep a listing the client does not expose, as empty

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u217.json`, row `A7_missing_method_kept`
- Moved: _listed reads through _listed_now, which records each missing method in missing; a longer missing list is the skip, and the mutation drops the early return so the empty listing is kept.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_a_listing_the_client_does_not_expose_stays_unread_on_every_run`

Old text:

```
        if len(missing) > before:
            return rows

```

New text:

```
(empty)
```

### `u217.A8_member_read_uncounted`

_listed: do not count the read of a kept artist's object, so the line can say no call over one

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u217.json`, row `A8_member_read_uncounted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_a_listing_the_client_does_not_expose_stays_unread_on_every_run`

Old text:

```
            if not artist.read_yet:
```

New text:

```
            if False:
```

### `u105-b.S1_parts_only_when_several`

Freeze the parts key for a single recording too

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S1_parts_only_when_several`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`
- Collected: 2 against a baseline of 2
- Kills: 2 (killed)
- Killed:
  - `tests/test_job_seam.py::test_a_driver_killed_inside_the_real_handler_resumes_redoing_exactly_that_item`
  - `tests/test_job_seam.py::test_the_partial_encode_a_kill_leaves_behind_is_in_staging_not_at_the_destination`

Old text:

```
    if len(frozen) > 1:
```

New text:

```
    if frozen:
```

### `u46-round-2.M6_staging_not_cleared`

Leave a previous attempt's partial encode in the staging directory

- File: `src/cratekit/master/cli.py`
- Source: `u46-round-2.json`, row `M6_staging_not_cleared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`
- Collected: 2 against a baseline of 2
- Kills: 1 (killed)
- Killed:
  - `tests/test_job_seam.py::test_a_driver_killed_inside_the_real_handler_resumes_redoing_exactly_that_item`

Old text:

```
    if directory.exists():
        shutil.rmtree(directory)
```

New text:

```
(empty)
```

### `r395.M1_no_pipx_detection`

Drop the pipx branch, every environment gets the pip form

- File: `src/cratekit/modules/extras.py`
- Source: `r395.json`, row `M1_no_pipx_detection`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_install_command.py`
- Collected: 13 against a baseline of 13
- Kills: 12 (killed)
- Killed:
  - `tests/test_install_command.py::test_a_direct_reference_to_another_package_is_not_read_as_this_install`
  - `tests/test_install_command.py::test_a_direct_reference_with_no_extras_gains_the_one_asked_for[cratekit @ git+https://github.com/philgutowski/cratekit@v0.3.0]`
  - `tests/test_install_command.py::test_a_direct_reference_with_no_extras_gains_the_one_asked_for[cratekit[]@ git+https://github.com/philgutowski/cratekit@v0.3.0]`
  - `tests/test_install_command.py::test_a_moved_clone_still_keeps_the_extras_pipx_recorded`
  - `tests/test_install_command.py::test_a_pipx_environment_gets_pipx_against_the_recorded_clone`
  - `tests/test_install_command.py::test_a_pipx_environment_whose_source_cannot_be_read_gets_the_readme_form[{"main_package": {"package_or_url": "/no/such/clone[vocals]"}}]`
  - `tests/test_install_command.py::test_a_pipx_environment_whose_source_cannot_be_read_gets_the_readme_form[{"main_package": {"package_or_url": "git+https://example.invalid/c.git"}}]`
  - `tests/test_install_command.py::test_a_pipx_environment_whose_source_cannot_be_read_gets_the_readme_form[{"main_package": {}}]`
  - `tests/test_install_command.py::test_a_pipx_environment_whose_source_cannot_be_read_gets_the_readme_form[{not json]`
  - `tests/test_install_command.py::test_a_pipx_force_install_keeps_the_extras_already_chosen`
  - `tests/test_install_command.py::test_a_release_install_pipx_recorded_as_a_direct_reference_keeps_it_and_its_extras`
  - `tests/test_install_command.py::test_the_parser_stub_and_the_workers_read_one_source`

Old text:

```
    if (prefix / PIPX_METADATA).is_file():
```

New text:

```
    if False:
```

### `r395.M2_bare_pip`

Print a bare pip instead of the running interpreter's pip

- File: `src/cratekit/modules/extras.py`
- Source: `r395.json`, row `M2_bare_pip`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_install_command.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_install_command.py::test_a_plain_virtual_environment_gets_pip_run_by_its_own_interpreter`

Old text:

```
[sys.executable, "-m", "pip", "install", f"{DISTRIBUTION}[{extras}]"]
```

New text:

```
["pip", "install", f"{DISTRIBUTION}[{extras}]"]
```

### `r395.M4_no_force`

Drop --force from the pipx form

- File: `src/cratekit/modules/extras.py`
- Source: `r395.json`, row `M4_no_force`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_install_command.py`
- Collected: 13 against a baseline of 13
- Kills: 8 (killed)
- Killed:
  - `tests/test_install_command.py::test_a_direct_reference_to_another_package_is_not_read_as_this_install`
  - `tests/test_install_command.py::test_a_moved_clone_still_keeps_the_extras_pipx_recorded`
  - `tests/test_install_command.py::test_a_pipx_environment_gets_pipx_against_the_recorded_clone`
  - `tests/test_install_command.py::test_a_pipx_environment_whose_source_cannot_be_read_gets_the_readme_form[{"main_package": {"package_or_url": "/no/such/clone[vocals]"}}]`
  - `tests/test_install_command.py::test_a_pipx_environment_whose_source_cannot_be_read_gets_the_readme_form[{"main_package": {"package_or_url": "git+https://example.invalid/c.git"}}]`
  - `tests/test_install_command.py::test_a_pipx_environment_whose_source_cannot_be_read_gets_the_readme_form[{"main_package": {}}]`
  - `tests/test_install_command.py::test_a_pipx_environment_whose_source_cannot_be_read_gets_the_readme_form[{not json]`
  - `tests/test_install_command.py::test_a_pipx_force_install_keeps_the_extras_already_chosen`

Old text:

```
["pipx", "install", "--force", f"{source}[{wanted}]"]
```

New text:

```
["pipx", "install", f"{source}[{wanted}]"]
```

### `r395.M5_trust_missing_source`

Use the recorded source even when the directory is gone

- File: `src/cratekit/modules/extras.py`
- Source: `r395.json`, row `M5_trust_missing_source`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_install_command.py`
- Collected: 13 against a baseline of 13
- Kills: 3 (killed)
- Killed:
  - `tests/test_install_command.py::test_a_moved_clone_still_keeps_the_extras_pipx_recorded`
  - `tests/test_install_command.py::test_a_pipx_environment_whose_source_cannot_be_read_gets_the_readme_form[{"main_package": {"package_or_url": "/no/such/clone[vocals]"}}]`
  - `tests/test_install_command.py::test_a_pipx_environment_whose_source_cannot_be_read_gets_the_readme_form[{"main_package": {"package_or_url": "git+https://example.invalid/c.git"}}]`

Old text:

```
    source = match["source"] if Path(match["source"]).is_dir() else "."
```

New text:

```
    source = match["source"]
```

### `r395.M6_always_dot`

Always print the '.' form, ignoring the recorded clone

- File: `src/cratekit/modules/extras.py`
- Source: `r395.json`, row `M6_always_dot`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_install_command.py`
- Collected: 13 against a baseline of 13
- Kills: 2 (killed)
- Killed:
  - `tests/test_install_command.py::test_a_pipx_environment_gets_pipx_against_the_recorded_clone`
  - `tests/test_install_command.py::test_a_pipx_force_install_keeps_the_extras_already_chosen`

Old text:

```
    source = match["source"] if Path(match["source"]).is_dir() else "."
```

New text:

```
    source = "."
```

### `r395.M7_fallback_drops_extras`

The review's defect: an unusable source drops the recorded extras

- File: `src/cratekit/modules/extras.py`
- Source: `r395.json`, row `M7_fallback_drops_extras`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_install_command.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_install_command.py::test_a_moved_clone_still_keeps_the_extras_pipx_recorded`

Old text:

```
    source = match["source"] if Path(match["source"]).is_dir() else "."
    return source, chosen
```

New text:

```
    if not Path(match["source"]).is_dir():
        return ".", ()
    return match["source"], chosen
```

### `u181.E1_direct_reference_unread`

extras.install_command: never read the direct reference, so the release install falls back to the folder form and drops analysis

- File: `src/cratekit/modules/extras.py`
- Source: `u181.json`, row `E1_direct_reference_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_install_command.py`
- Collected: 13 against a baseline of 13
- Kills: 3 (killed)
- Killed:
  - `tests/test_install_command.py::test_a_direct_reference_with_no_extras_gains_the_one_asked_for[cratekit @ git+https://github.com/philgutowski/cratekit@v0.3.0]`
  - `tests/test_install_command.py::test_a_direct_reference_with_no_extras_gains_the_one_asked_for[cratekit[]@ git+https://github.com/philgutowski/cratekit@v0.3.0]`
  - `tests/test_install_command.py::test_a_release_install_pipx_recorded_as_a_direct_reference_keeps_it_and_its_extras`

Old text:

```
        reference = _pipx_reference(prefix / PIPX_METADATA)
        if reference is not None:
```

New text:

```
        reference = _pipx_reference(prefix / PIPX_METADATA)
        if False:
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

### `u311.D2_empty_extra_kept`

An empty name between commas is kept as an extra in the install command

- File: `src/cratekit/modules/extras.py`
- Source: `u311.json`, row `D2_empty_extra_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_install_command.py`
- Collected: 13 against a baseline of 13
- Kills: 4 (killed)
- Killed:
  - `tests/test_install_command.py::test_a_direct_reference_with_no_extras_gains_the_one_asked_for[cratekit @ git+https://github.com/philgutowski/cratekit@v0.3.0]`
  - `tests/test_install_command.py::test_a_direct_reference_with_no_extras_gains_the_one_asked_for[cratekit[]@ git+https://github.com/philgutowski/cratekit@v0.3.0]`
  - `tests/test_install_command.py::test_a_pipx_environment_gets_pipx_against_the_recorded_clone`
  - `tests/test_install_command.py::test_a_pipx_environment_whose_source_cannot_be_read_gets_the_readme_form[{"main_package": {"package_or_url": "git+https://example.invalid/c.git"}}]`

Old text:

```
    return tuple(e.strip() for e in (match["extras"] or "").split(",") if e.strip())
```

New text:

```
    return tuple(e.strip() for e in (match["extras"] or "").split(","))
```

### `u192.F6_queue_only_never`

queue_only: always False, so --queue-only drives the job anyway

- File: `src/cratekit/modules/foreground.py`
- Source: `u192.json`, row `F6_queue_only_never`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_genre.py::test_an_unreadable_registry_warns_and_refuses_only_a_sweep_that_named_a_label`
  - `tests/test_label_genre.py::test_the_remedy_names_the_label_by_its_identifier`

Old text:

```
    return bool(getattr(args, "queue_only", False))
```

New text:

```
    return False
```

### `u192.F7_queue_only_always`

queue_only: always True, so a verb run by hand queues and returns as before U192

- File: `src/cratekit/modules/foreground.py`
- Source: `u192.json`, row `F7_queue_only_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_sweep_driven_at_its_queue_keeps_the_label_warning_and_never_calls_its_label_unapplied`

Old text:

```
    return bool(getattr(args, "queue_only", False))
```

New text:

```
    return True
```

### `r835-a.F12_refused_tracks_recorded`

folders.apply: a track the provider would not add is not recorded as refused, so every later plan asks for it again

- File: `src/cratekit/modules/outbound/folders.py`
- Source: `r835-a.json`, row `F12_refused_tracks_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_track_the_provider_will_not_add_is_recorded_and_not_asked_again`

Old text:

```
            refused = [one for one in chunk if one not in held]
```

New text:

```
            refused = []
```

### `r835-a.F2_two_root_folders_refuse`

folders.plan: two root folders under the label's name are not refused, and the first by identifier is adopted

- File: `src/cratekit/modules/outbound/folders.py`
- Source: `r835-a.json`, row `F2_two_root_folders_refuse`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_two_root_folders_named_as_the_label_refuse_and_write_nothing`

Old text:

```
        if len(named) > 1:
            raise _ambiguous_folder(catalogue.name, named)
```

New text:

```
        if False:
            raise _ambiguous_folder(catalogue.name, named)
```

### `r835-a.F3_root_folder_adopted_by_name`

folders.plan: a root folder already named as the label is never adopted, so a second folder of that name is created

- File: `src/cratekit/modules/outbound/folders.py`
- Source: `r835-a.json`, row `F3_root_folder_adopted_by_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_folder_made_by_hand_at_the_root_is_adopted`
  - `tests/test_label_playlists.py::test_an_unrecorded_marked_year_in_the_folder_is_matched_by_its_marked_name`
  - `tests/test_label_playlists.py::test_two_playlists_named_for_one_year_leave_that_year_alone`

Old text:

```
        if named:
            folder_action, folder_id = ADOPT, named[0]
```

New text:

```
        if False:
            folder_action, folder_id = ADOPT, named[0]
```

### `r835-a.F4_recorded_and_refused_not_asked_again`

folders.plan: a track recorded as added or refused is asked for again, so one a person took off is put back and one refused is asked every run

- File: `src/cratekit/modules/outbound/folders.py`
- Source: `r835-a.json`, row `F4_recorded_and_refused_not_asked_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_refusal_part_way_leaves_what_was_written_recorded_and_a_resume_finishes`
  - `tests/test_label_playlists.py::test_a_second_mark_plans_nothing_and_a_build_after_it_reuses_the_marked_years`
  - `tests/test_label_playlists.py::test_a_second_run_over_an_unchanged_catalogue_plans_nothing`
  - `tests/test_label_playlists.py::test_a_track_taken_off_by_a_person_is_not_put_back`
  - `tests/test_label_playlists.py::test_a_track_the_provider_will_not_add_is_recorded_and_not_asked_again`

Old text:

```
            skip = held | asked
```

New text:

```
            skip = held
```

### `r835-a.F5_unplaced_recorded_year_is_moved`

folders.plan: a recorded year playlist that is not in the folder is never moved into it, so a build stopped after its create leaves it at the root

- File: `src/cratekit/modules/outbound/folders.py`
- Source: `r835-a.json`, row `F5_unplaced_recorded_year_is_moved`
- Moved: the reused year step in folders.plan is now built through a partial of YearStep, so the same keyword sits four spaces shallower; same keyword reverted
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_label_folder_deleted_on_the_account_is_made_again_and_recorded`
  - `tests/test_label_playlists.py::test_a_playlist_made_and_not_yet_moved_is_moved_on_the_resume_and_not_made_again`

Old text:

```
                move=not placed,

```

New text:

```
                move=False,

```

### `r835-c.F1_recorded_folder_must_be_listed_again`

folders.plan: a recorded folder the account no longer lists is reused, so year playlists are moved into a folder that is gone

- File: `src/cratekit/modules/outbound/folders.py`
- Source: `r835-c.json`, row `F1_recorded_folder_must_be_listed_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_label_folder_deleted_on_the_account_is_made_again_and_recorded`

Old text:

```
    if shape.folder_id and shape.folder_id in root:
```

New text:

```
    if shape.folder_id:
```

### `r835-c.F7_only_a_provider_failure_is_unreadable_again`

folders.plan: any refusal reading a recorded year outside the folder is passed over as unreadable, a rejected session included

- File: `src/cratekit/modules/outbound/folders.py`
- Source: `r835-c.json`, row `F7_only_a_provider_failure_is_unreadable_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_rejected_session_reading_a_recorded_year_is_raised_not_passed_over`

Old text:

```
                    if placed or exc.cause.reason != "unavailable-transient":
                        raise
```

New text:

```
                    if placed:
                        raise
```

### `r835-c.F8_marked_title_matches_by_name_again`

folders.plan: a year playlist in the folder carrying the mark prefix is not matched by name, so an unrecorded marked year is created a second time

- File: `src/cratekit/modules/outbound/folders.py`
- Source: `r835-c.json`, row `F8_marked_title_matches_by_name_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_an_unrecorded_marked_year_in_the_folder_is_matched_by_its_marked_name`

Old text:

```
            pid for pid, title in inside.items() if title in (name, MARK_PREFIX + name)
```

New text:

```
            pid for pid, title in inside.items() if title == name
```

### `r835-a.L1_load_carries_the_label_map`

ledger._load: the label map is dropped on load, so any other write to the ledger forgets every label's folder and year playlists

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r835-a.json`, row `L1_load_carries_the_label_map`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 28 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_batch_of_another_label_marks_nothing_and_reads_no_account`
  - `tests/test_label_playlists.py::test_a_folder_made_by_hand_at_the_root_is_adopted`
  - `tests/test_label_playlists.py::test_a_label_folder_deleted_on_the_account_is_made_again_and_recorded`
  - `tests/test_label_playlists.py::test_a_label_folder_deleted_on_the_account_is_said_not_failed`
  - `tests/test_label_playlists.py::test_a_ledger_written_by_another_verb_keeps_the_label_shape`
  - `tests/test_label_playlists.py::test_a_mark_the_record_cannot_take_names_what_it_took_before`
  - `tests/test_label_playlists.py::test_a_mark_with_no_landed_file_refuses_before_anything`
  - `tests/test_label_playlists.py::test_a_new_year_made_by_hand_under_the_folder_is_reused_not_duplicated`
  - `tests/test_label_playlists.py::test_a_playlist_made_and_not_yet_moved_is_moved_on_the_resume_and_not_made_again`
  - `tests/test_label_playlists.py::test_a_recorded_year_deleted_on_the_account_is_left_alone_not_refused`
  - `tests/test_label_playlists.py::test_a_refusal_part_way_leaves_what_was_written_recorded_and_a_resume_finishes`
  - `tests/test_label_playlists.py::test_a_rejected_session_reading_a_recorded_year_is_raised_not_passed_over`
  - `tests/test_label_playlists.py::test_a_second_mark_plans_nothing_and_a_build_after_it_reuses_the_marked_years`
  - `tests/test_label_playlists.py::test_a_second_mark_says_each_year_is_already_marked`
  - `tests/test_label_playlists.py::test_a_second_run_over_an_unchanged_catalogue_plans_nothing`
  - ... and 13 more, see the JSON sidecar

Old text:

```
        "labels": {str(key): _label_document(path, value) for key, value in labels.items()},
```

New text:

```
        "labels": {},
```

### `r837-a.A8_load_carries_sets`

ledger._load: the sets map is dropped on read, so every later write forgets each set playlist

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r837-a.json`, row `A8_load_carries_sets`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 20 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_folder_named_as_the_year_by_hand_is_adopted_not_doubled`
  - `tests/test_export_set.py::test_a_name_with_a_slash_finds_the_set_it_named_at_build`
  - `tests/test_export_set.py::test_a_playlist_already_in_its_folder_is_left`
  - `tests/test_export_set.py::test_a_playlist_retitled_by_a_person_is_filed_and_its_title_left`
  - `tests/test_export_set.py::test_a_playlist_the_folder_does_not_list_yet_is_not_renamed_or_blamed`
  - `tests/test_export_set.py::test_a_row_added_to_the_tracklist_later_is_added_to_the_same_playlist`
  - `tests/test_export_set.py::test_a_row_carrying_an_isrc_is_matched_through_the_accounts_own_match`
  - `tests/test_export_set.py::test_a_second_run_onto_the_same_set_plans_nothing`
  - `tests/test_export_set.py::test_a_set_put_in_its_folder_by_hand_writes_nothing_and_its_gate_says_so`
  - `tests/test_export_set.py::test_a_tidal_list_documents_own_identifiers_are_used_without_a_search`
  - `tests/test_export_set.py::test_a_track_already_on_the_playlist_and_never_recorded_is_not_asked_for`
  - `tests/test_export_set.py::test_a_track_refused_before_is_said_as_refused_not_as_on_the_playlist`
  - `tests/test_export_set.py::test_a_track_taken_off_by_a_person_is_said_and_not_put_back`
  - `tests/test_export_set.py::test_a_year_folder_deleted_on_the_account_is_made_again`
  - `tests/test_export_set.py::test_an_archive_with_no_landed_file_refuses_before_anything`
  - ... and 5 more, see the JSON sidecar

Old text:

```
            for key, value in sets.items()
```

New text:

```
            for key, value in ()
```

### `u123.L1_dated_vouched`

Stop the ledger vouching for a dated playlist it records

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u123.json`, row `L1_dated_vouched`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 20 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_dated_entry_that_is_not_a_name_to_an_identifier_is_not_vouched_for`
  - `tests/test_label_heard.py::test_a_dated_playlist_made_by_the_dated_plan_is_vouched_for_and_one_reused_is_not`
  - `tests/test_label_heard.py::test_a_delete_the_client_answers_false_is_a_failure`
  - `tests/test_label_heard.py::test_a_folder_with_no_year_playlist_refuses_when_there_is_something_to_add`
  - `tests/test_label_heard.py::test_a_named_release_already_heard_is_said_and_writes_nothing`
  - `tests/test_label_heard.py::test_a_playlist_already_gone_is_removed_with_no_delete`
  - `tests/test_label_heard.py::test_a_playlist_still_served_after_its_delete_is_refused_not_reported_removed`
  - `tests/test_label_heard.py::test_a_playlist_the_client_does_not_serve_as_owned_is_refused_in_words`
  - `tests/test_label_heard.py::test_a_removal_refused_part_way_names_the_adds_marks_nothing_and_a_resume_finishes`
  - `tests/test_label_heard.py::test_a_track_an_unheard_release_also_carries_stays_on_the_dated_playlist`
  - `tests/test_label_heard.py::test_a_track_the_year_will_not_take_keeps_the_dated_playlist`
  - `tests/test_label_heard.py::test_a_year_known_only_by_the_marks_prefixed_name_is_the_year`
  - `tests/test_label_heard.py::test_an_adopted_year_still_wins_over_a_dated_entry_for_the_same_identifier`
  - `tests/test_label_heard.py::test_declined_nothing_is_written`
  - `tests/test_label_heard.py::test_every_run_says_the_record_labels_tree_is_not_changed`
  - ... and 5 more, see the JSON sidecar

Old text:

```
        if wanted in (record.get("dated") or {}).values():
            made = True
```

New text:

```
        if False:
            made = True
```

### `u123.L3_malformed_entry_dropped`

Keep a dated entry with an empty name or identifier

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u123.json`, row `L3_malformed_entry_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_dated_entry_that_is_not_a_name_to_an_identifier_is_not_vouched_for`

Old text:

```
            {"dated": {str(name): str(pid) for name, pid in dated.items() if name and pid}}
```

New text:

```
            {"dated": {str(name): str(pid) for name, pid in dated.items()}}
```

### `r835-a.L3_recorded_year_never_created_again`

ledger.reserve_label_year: a year already recorded is created again, so a resumed build makes a second playlist for it

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r835-a.json`, row `L3_recorded_year_never_created_again`
- Moved: the already recorded check was in ledger.reserve_label_year and is now in ledger_reserve._reserve, which reserve_label_year calls with the year table, so the record is read as held rather than years; same check reverted
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_label_folder_deleted_on_the_account_is_made_again_and_recorded`
  - `tests/test_label_playlists.py::test_a_new_year_made_by_hand_under_the_folder_is_reused_not_duplicated`
  - `tests/test_label_playlists.py::test_a_playlist_made_and_not_yet_moved_is_moved_on_the_resume_and_not_made_again`
  - `tests/test_label_playlists.py::test_a_refusal_part_way_leaves_what_was_written_recorded_and_a_resume_finishes`

Old text:

```
        recorded = str((held.get(key) or {}).get("remote_id") or "")
        if recorded:
            return recorded, False
```

New text:

```
        recorded = str((held.get(key) or {}).get("remote_id") or "")
        if False:
            return recorded, False
```

### `r837-a.A7_reserve_reuses_recorded`

ledger.reserve_set_playlist: a recorded set playlist is not reused, so the create runs again

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r837-a.json`, row `A7_reserve_reuses_recorded`
- Moved: the reuse check left ledger.reserve_set_playlist for ledger_reserve._reserve, the one reserve shared by the set, label year and mirrored playlists, so the record is read through the table it is handed; same condition reverted
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`, `tests/test_label_playlists.py`
- Collected: 119 against a baseline of 119
- Kills: 5 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_row_added_to_the_tracklist_later_is_added_to_the_same_playlist`
  - `tests/test_label_playlists.py::test_a_label_folder_deleted_on_the_account_is_made_again_and_recorded`
  - `tests/test_label_playlists.py::test_a_new_year_made_by_hand_under_the_folder_is_reused_not_duplicated`
  - `tests/test_label_playlists.py::test_a_playlist_made_and_not_yet_moved_is_moved_on_the_resume_and_not_made_again`
  - `tests/test_label_playlists.py::test_a_refusal_part_way_leaves_what_was_written_recorded_and_a_resume_finishes`

Old text:

```
        recorded = str((held.get(key) or {}).get("remote_id") or "")
        if recorded:
```

New text:

```
        recorded = str((held.get(key) or {}).get("remote_id") or "")
        if False:
```

### `u140.B1_ledger_folds_into_a_twin`

rename_set_playlist drops its refusal when the new name already holds another playlist

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `u140.json`, row `B1_ledger_folds_into_a_twin`
- Moved: rename_set_playlist moved from ledger.py to ledger_reserve.py and raises through the shared _refused instead of _unusable with a path; same refusal condition reverted
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
            raise _refused(

```

New text:

```
        if False:
            raise _refused(

```

### `u140.B2_ledger_moves_another_id`

rename_set_playlist drops its refusal when the old name records a different playlist

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `u140.json`, row `B2_ledger_moves_another_id`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
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

### `u309.U4_reserve_recorded_wins`

A reservation creates again over the playlist the ledger already records

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `u309.json`, row `U4_reserve_recorded_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`, `tests/test_label_playlists.py`
- Collected: 119 against a baseline of 119
- Kills: 5 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_row_added_to_the_tracklist_later_is_added_to_the_same_playlist`
  - `tests/test_label_playlists.py::test_a_label_folder_deleted_on_the_account_is_made_again_and_recorded`
  - `tests/test_label_playlists.py::test_a_new_year_made_by_hand_under_the_folder_is_reused_not_duplicated`
  - `tests/test_label_playlists.py::test_a_playlist_made_and_not_yet_moved_is_moved_on_the_resume_and_not_made_again`
  - `tests/test_label_playlists.py::test_a_refusal_part_way_leaves_what_was_written_recorded_and_a_resume_finishes`

Old text:

```
        if recorded:
            return recorded, False
        remote_id = create()
```

New text:

```
        if False:
            return recorded, False
        remote_id = create()
```

### `u309.U5_reserve_written`

A reservation's new identifier is never written to the ledger

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `u309.json`, row `U5_reserve_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`
- Collected: 157 against a baseline of 157
- Kills: 71 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_folder_named_as_the_year_by_hand_is_adopted_not_doubled`
  - `tests/test_export_set.py::test_a_name_with_a_slash_finds_the_set_it_named_at_build`
  - `tests/test_export_set.py::test_a_playlist_already_in_its_folder_is_left`
  - `tests/test_export_set.py::test_a_playlist_retitled_by_a_person_is_filed_and_its_title_left`
  - `tests/test_export_set.py::test_a_playlist_the_folder_does_not_list_yet_is_not_renamed_or_blamed`
  - `tests/test_export_set.py::test_a_row_added_to_the_tracklist_later_is_added_to_the_same_playlist`
  - `tests/test_export_set.py::test_a_row_carrying_an_isrc_is_matched_through_the_accounts_own_match`
  - `tests/test_export_set.py::test_a_second_run_onto_the_same_set_plans_nothing`
  - `tests/test_export_set.py::test_a_set_put_in_its_folder_by_hand_writes_nothing_and_its_gate_says_so`
  - `tests/test_export_set.py::test_a_tidal_list_documents_own_identifiers_are_used_without_a_search`
  - `tests/test_export_set.py::test_a_track_already_on_the_playlist_and_never_recorded_is_not_asked_for`
  - `tests/test_export_set.py::test_a_track_refused_before_is_said_as_refused_not_as_on_the_playlist`
  - `tests/test_export_set.py::test_a_track_taken_off_by_a_person_is_said_and_not_put_back`
  - `tests/test_export_set.py::test_a_year_folder_deleted_on_the_account_is_made_again`
  - `tests/test_export_set.py::test_an_archive_with_no_landed_file_refuses_before_anything`
  - ... and 56 more, see the JSON sidecar

Old text:

```
        held[key] = record(remote_id)
        ledger._write(cfg, document)
        return remote_id, True
```

New text:

```
        held[key] = record(remote_id)
        return remote_id, True
```

### `u123.L2_forget_drops_the_entry`

Keep a removed dated playlist's ledger entry

- File: `src/cratekit/modules/outbound/ledger_settle.py`
- Source: `u123.json`, row `L2_forget_drops_the_entry`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_settle.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_dated_playlist_made_by_the_dated_plan_is_vouched_for_and_one_reused_is_not`
  - `tests/test_label_heard.py::test_heard_writes_the_ids_merges_and_removes_and_a_second_run_is_a_no_op`

Old text:

```
        kept = {name: pid for name, pid in held.items() if pid != str(remote_id)}
```

New text:

```
        kept = dict(held)
```

### `u207.M1_mirror_screens_settled_rows`

mirror: the matcher screens every row with a code, a link, a recorded track and a remembered miss included

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u207.json`, row `M1_mirror_screens_settled_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_the_mirror_screens_only_the_rows_it_would_ask_the_provider_about`

Old text:

```
            if self._settled(row) is None and (said := self._identity(row)).isrc
```

New text:

```
            if (said := self._identity(row)).isrc
```

### `u207.M2_mirror_counts_a_screen_as_one`

mirror: Counted counts a screen as one request whatever it spent

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u207.json`, row `M2_mirror_counts_a_screen_as_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_the_mirrors_request_count_holds_what_the_screen_spent_and_no_more`

Old text:

```
            if name in SCREENS:
```

New text:

```
            if False:
```

### `u214.M8_plan_left_lines`

mirror.plan: start left empty, so no unmirrored node reaches the step's plan or left count

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u214.json`, row `M8_plan_left_lines`
- Moved: the unmirrored lines still open mirror.plan's left list in mirror.py, written without the list[str] annotation; same list emptied
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`
- Collected: 27 against a baseline of 27
- Kills: 4 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_rebuild_from_the_frozen_plan_still_names_them`
  - `tests/test_inbox_unmirrored.py::test_an_inbox_with_no_batch_at_all_still_names_them`
  - `tests/test_inbox_unmirrored.py::test_an_inbox_with_nothing_to_write_still_names_them`
  - `tests/test_inbox_unmirrored.py::test_the_inbox_step_names_each_unmirrored_node_on_its_plan_and_its_line`

Old text:

```
    left = [f"{label}: not mirrored, {reason}" for label, reason in folder.unmirrored]
```

New text:

```
    left = []
```

### `r1017.M10_older_beats_to`

Plan: hold an older name's record ahead of the one under the new name

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `r1017.json`, row `M10_older_beats_to`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_twin_under_the_new_name_is_refused_rather_than_adopted`
  - `tests/test_export_set_rename.py::test_a_twin_under_the_new_name_still_refuses_when_the_landing_names_the_old`

Old text:

```
    held = recorded_to or (older[0] if older else None)
```

New text:

```
    held = (older[0] if older else None) or recorded_to
```

### `r1017.M8_first_older_name_only`

Plan: stop at the first older name holding a record, the pre review behaviour

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `r1017.json`, row `M8_first_older_name_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_the_frozen_name_ranks_ahead_of_the_landing_record`
  - `tests/test_export_set_rename.py::test_two_playlists_under_two_older_names_are_a_twin_not_a_choice`

Old text:

```
        if found is not None and all(found.remote_id != one.remote_id for one in older):
```

New text:

```
        if found is not None and not older:
```

### `r1017.M9_twin_only_beside_to`

Plan: call a twin only when a record under the new name exists, the pre review rule

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `r1017.json`, row `M9_twin_only_beside_to`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_the_frozen_name_ranks_ahead_of_the_landing_record`
  - `tests/test_export_set_rename.py::test_two_playlists_under_two_older_names_are_a_twin_not_a_choice`

Old text:

```
    twin = next((one for one in older if one.remote_id != held.remote_id), None)
```

New text:

```
    twin = next((one for one in older if recorded_to is not None and one.remote_id != held.remote_id), None)
```

### `r837-a.A11_year_folder_adopted`

sets.plan_archive: a root folder already named as the year is never adopted, so a second is made

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `r837-a.json`, row `A11_year_folder_adopted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_folder_named_as_the_year_by_hand_is_adopted_not_doubled`
  - `tests/test_export_set.py::test_a_set_put_in_its_folder_by_hand_writes_nothing_and_its_gate_says_so`

Old text:

```
        action, folder_id = (ADOPT, named[0]) if named else (CREATE, "")
```

New text:

```
        action, folder_id = (CREATE, "")
```

### `r837-a.A12_in_folder_not_moved`

ArchivePlan.move: a playlist already in its folder is moved again

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `r837-a.json`, row `A12_in_folder_not_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 3 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_playlist_already_in_its_folder_is_left`
  - `tests/test_export_set.py::test_a_playlist_the_folder_does_not_list_yet_is_not_renamed_or_blamed`
  - `tests/test_export_set.py::test_a_set_put_in_its_folder_by_hand_writes_nothing_and_its_gate_says_so`

Old text:

```
    def move(self) -> bool:
        return self.title is None
```

New text:

```
    def move(self) -> bool:
        return True
```

### `r837-a.A14_not_listed_not_blamed`

sets.apply_archive: a playlist the folder does not list yet is read as retitled by somebody

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `r837-a.json`, row `A14_not_listed_not_blamed`
- Moved: the same NOT_LISTED guard in sets.apply_archive's recheck; its comment was shortened to one line, so the anchor carries the new comment and the condition is reverted the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_playlist_the_folder_does_not_list_yet_is_not_renamed_or_blamed`

Old text:

```
    if now is None:
        # NOT A RETITLE: a listing without it says nothing about its title.
```

New text:

```
    if False:
        # NOT A RETITLE: a listing without it says nothing about its title.
```

### `r837-a.A1_no_record_creates`

sets.plan_set: a set already recorded is planned as a create, so a second run makes a second playlist

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `r837-a.json`, row `A1_no_record_creates`
- Moved: the no record guard is still in sets.plan_set, its SetPlan now built with positional arguments instead of keywords; same condition forced true
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 4 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_second_run_onto_the_same_set_plans_nothing`
  - `tests/test_export_set.py::test_a_track_already_on_the_playlist_and_never_recorded_is_not_asked_for`
  - `tests/test_export_set.py::test_a_track_refused_before_is_said_as_refused_not_as_on_the_playlist`
  - `tests/test_export_set.py::test_a_track_taken_off_by_a_person_is_said_and_not_put_back`

Old text:

```
    if recorded is None:
        return SetPlan(name, year, CREATE, tuple(rows), add=wanted)

```

New text:

```
    if True:
        return SetPlan(name, year, CREATE, tuple(rows), add=wanted)

```

### `r837-a.A2_asked_not_asked_again`

sets.plan_set: a track written or refused before is asked for again

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `r837-a.json`, row `A2_asked_not_asked_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_track_refused_before_is_said_as_refused_not_as_on_the_playlist`
  - `tests/test_export_set.py::test_a_track_taken_off_by_a_person_is_said_and_not_put_back`

Old text:

```
        add=tuple(one for one in wanted if one not in asked and one not in held),
```

New text:

```
        add=tuple(one for one in wanted if one not in held),
```

### `r837-a.A4_nothing_matched_writes_nothing`

SetPlan.writes: a plan with nothing to add still writes, so a set with nothing matched makes an empty playlist

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `r837-a.json`, row `A4_nothing_matched_writes_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 3 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_second_run_onto_the_same_set_plans_nothing`
  - `tests/test_export_set.py::test_a_set_with_nothing_matched_makes_no_empty_playlist`
  - `tests/test_export_set.py::test_a_track_already_on_the_playlist_and_never_recorded_is_not_asked_for`

Old text:

```
        return bool(self.add)
```

New text:

```
        return True
```

### `r837-a.A5_chunk_recorded`

sets.apply_set: a chunk written is not recorded, so a resume asks for it again

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `r837-a.json`, row `A5_chunk_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 3 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_track_refused_before_is_said_as_refused_not_as_on_the_playlist`
  - `tests/test_export_set.py::test_a_track_taken_off_by_a_person_is_said_and_not_put_back`
  - `tests/test_export_set.py::test_approved_the_account_holds_a_private_playlist_of_four_in_order`

Old text:

```
        ledger.record_set_tracks(cfg, planned.name, added=added, refused=refused)
```

New text:

```
        pass
```

### `r837-a.A6_refused_split`

sets.apply_set: a track the provider would not add is not counted as refused

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `r837-a.json`, row `A6_refused_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_track_refused_before_is_said_as_refused_not_as_on_the_playlist`

Old text:

```
        refused = [one for one in chunk if one not in held]
```

New text:

```
        refused = []
```

### `r837-b.A3r_held_not_added`

batch a's A3 again: sets.plan_set adds a track already on the playlist and never recorded

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `r837-b.json`, row `A3r_held_not_added`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_track_already_on_the_playlist_and_never_recorded_is_not_asked_for`

Old text:

```
        add=tuple(one for one in wanted if one not in asked and one not in held),
```

New text:

```
        add=tuple(one for one in wanted if one not in asked),
```

### `r837-b.A9r_recorded_folder_listed`

batch a's A9 again: sets.plan_archive reuses a recorded year folder the account no longer lists

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `r837-b.json`, row `A9r_recorded_folder_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_set_put_in_its_folder_by_hand_writes_nothing_and_its_gate_says_so`
  - `tests/test_export_set.py::test_a_year_folder_deleted_on_the_account_is_made_again`

Old text:

```
    if recorded and recorded in root:
```

New text:

```
    if recorded:
```

### `u140.A2_new_name_record_ignored`

plan_rename does not look under the new name, so a rerun after the rekey finds nothing recorded

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u140.json`, row `A2_new_name_record_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 6 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_job_whose_page_words_differ_renames_by_the_name_its_landing_recorded`
  - `tests/test_export_set_rename.py::test_a_name_with_a_slash_freezes_as_the_library_spells_it`
  - `tests/test_export_set_rename.py::test_a_rename_that_failed_after_the_account_finishes_on_the_next_run`
  - `tests/test_export_set_rename.py::test_a_second_rename_is_a_no_op`
  - `tests/test_export_set_rename.py::test_a_twin_under_the_new_name_is_refused_rather_than_adopted`
  - `tests/test_export_set_rename.py::test_a_twin_under_the_new_name_still_refuses_when_the_landing_names_the_old`

Old text:

```
    recorded_to = ledger.set_playlist(cfg, to) if to else None

```

New text:

```
    recorded_to = None

```

### `u140.A3_refreeze_against_account_spelling`

RenamePlan.refreeze compares the frozen name with the account spelling, not the library's

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u140.json`, row `A3_refreeze_against_account_spelling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_name_with_a_slash_freezes_as_the_library_spells_it`

Old text:

```
        return self.frozen != (self.live or self.to)

```

New text:

```
        return self.frozen != self.to

```

### `u140.A4_rename_always`

RenamePlan.rename is always true, so a second run renames on the account again

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u140.json`, row `A4_rename_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 4 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_job_whose_page_words_differ_renames_by_the_name_its_landing_recorded`
  - `tests/test_export_set_rename.py::test_a_name_with_a_slash_freezes_as_the_library_spells_it`
  - `tests/test_export_set_rename.py::test_a_rename_that_failed_after_the_account_finishes_on_the_next_run`
  - `tests/test_export_set_rename.py::test_a_second_rename_is_a_no_op`

Old text:

```
        return self.playlist.name != self.to

```

New text:

```
        return True

```

### `u140.A5_ledger_never_rekeyed`

apply_rename retitles on the account and leaves the ledger key where it was

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u140.json`, row `A5_ledger_never_rekeyed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 9 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_backfill_after_the_rename_plans_no_twin_and_a_named_export_adds_to_it`
  - `tests/test_export_set_rename.py::test_a_job_whose_page_words_differ_renames_by_the_name_its_landing_recorded`
  - `tests/test_export_set_rename.py::test_a_job_with_no_frozen_name_is_found_by_the_queued_day_and_refrozen`
  - `tests/test_export_set_rename.py::test_a_ledger_left_under_the_old_key_is_moved_on_the_next_run`
  - `tests/test_export_set_rename.py::test_a_name_with_a_slash_freezes_as_the_library_spells_it`
  - `tests/test_export_set_rename.py::test_a_rename_that_failed_after_the_account_finishes_on_the_next_run`
  - `tests/test_export_set_rename.py::test_a_renamed_inspiration_playlist_renames_the_account_playlist_ledger_and_job`
  - `tests/test_export_set_rename.py::test_a_second_rename_is_a_no_op`
  - `tests/test_export_set_rename.py::test_the_backfill_plans_no_twin_after_a_rename_by_the_landing_record`

Old text:

```
        done.rekeyed = ledger.rename_set_playlist(
            cfg, playlist.name, planned.to, playlist.remote_id
        )

```

New text:

```
        done.rekeyed = False

```

### `u140.A6_refreeze_account_spelling`

apply_rename refreezes the account spelling rather than the INSPIRATION playlist's own name

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u140.json`, row `A6_refreeze_account_spelling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_name_with_a_slash_freezes_as_the_library_spells_it`

Old text:

```
        refreeze(planned.live or planned.to)

```

New text:

```
        refreeze(planned.to)

```

### `u142.S1_folder_prefix`

sets: drop the Downloaded Sets prefix, so a set is filed into the plain year folder the filing owns

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u142.json`, row `S1_folder_prefix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 5 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_folder_named_as_the_year_by_hand_is_adopted_not_doubled`
  - `tests/test_export_set.py::test_a_set_put_in_its_folder_by_hand_writes_nothing_and_its_gate_says_so`
  - `tests/test_export_set.py::test_a_year_folder_deleted_on_the_account_is_made_again`
  - `tests/test_export_set.py::test_the_archive_takes_records_and_files_it_in_a_year_folder_made_once`
  - `tests/test_export_set.py::test_two_folders_named_as_the_year_refuse_and_write_nothing`

Old text:

```
FOLDER_PREFIX = "Downloaded Sets "
```

New text:

```
FOLDER_PREFIX = ""
```

### `u142.S2_plan_reads_the_year_key`

plan_archive: read the ledger's folder record under the year, so the filing's plain year folder is reused for a set

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u142.json`, row `S2_plan_reads_the_year_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_year_folder_deleted_on_the_account_is_made_again`

Old text:

```
    recorded = ledger.set_folder(cfg, name)
```

New text:

```
    recorded = ledger.set_folder(cfg, year)
```

### `u142.S4_ambiguity_bound`

plan_archive: refuse only three folders of the name, so one of two Downloaded Sets folders is picked silently

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u142.json`, row `S4_ambiguity_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_two_folders_named_as_the_year_refuse_and_write_nothing`

Old text:

```
        if len(named) > 1:
            raise _ambiguous_folder(name, named)
```

New text:

```
        if len(named) > 2:
            raise _ambiguous_folder(name, named)
```

### `u142.S5_create_under_the_year`

apply_archive: create the folder under the plain year, so a set's folder is made with the filing's name

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u142.json`, row `S5_create_under_the_year`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_the_archive_takes_records_and_files_it_in_a_year_folder_made_once`

Old text:

```
        lambda: account.create_folder(planned.folder_name),
```

New text:

```
        lambda: account.create_folder(planned.year),
```

### `u142.S6_reserve_under_the_year`

apply_archive: record the folder under the plain year key, so the filing reuses the sets' folder

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u142.json`, row `S6_reserve_under_the_year`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_year_folder_deleted_on_the_account_is_made_again`

Old text:

```
        planned.folder_name,
        lambda: account.create_folder(planned.folder_name),
```

New text:

```
        planned.year,
        lambda: account.create_folder(planned.folder_name),
```

### `u142.S7_adoption_is_a_write`

ArchivePlan.writes: count an adoption alone as a write again, so a set already filed by hand reads as planned

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u142.json`, row `S7_adoption_is_a_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_set_put_in_its_folder_by_hand_writes_nothing_and_its_gate_says_so`

Old text:

```
        return self.move or self.mark
```

New text:

```
        return self.folder_action in (CREATE, ADOPT) or self.move or self.mark
```

### `r228-operator.D10_pink_warning_gone`

queue_warnings: drop the pink missing warning

- File: `src/cratekit/modules/outbound/shell.py`
- Source: `r228-operator.json`, row `D10_pink_warning_gone`
- Moved: queue_warnings now builds its warnings from one table of (due, code, message) entries rather than an if and append per warning, so the pink missing warning is dropped by deleting its entry from that table
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_pink.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_pink.py::test_pink_missing_is_warned_beside_dangling`

Old text:

```
        (
            resolved.pink_missing, "favorites-pink-export-missing",
            f"{len(resolved.pink_missing)} pink row(s) the library carries are not in the "
            f"export's collection and are not queued: {', '.join(resolved.pink_missing)}",
        ),

```

New text:

```
(empty)
```

### `r290-author.S13_outbound_shell_call_removed`

Remove the one jobs.raise_for_state call from modules/outbound/shell.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/modules/outbound/shell.py`
- Source: `r290-author.json`, row `S13_outbound_shell_call_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`
- Collected: 126 against a baseline of 126
- Kills: 11 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[export.playlist]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[sync.favorites]`
  - `tests/test_job_outcome.py::test_a_parked_or_half_failed_job_answers_the_same_way_the_second_time_it_is_asked[half-failed-export.playlist]`
  - `tests/test_job_outcome.py::test_a_parked_or_half_failed_job_answers_the_same_way_the_second_time_it_is_asked[half-failed-sync.favorites]`
  - `tests/test_job_outcome.py::test_a_parked_or_half_failed_job_answers_the_same_way_the_second_time_it_is_asked[parked-export.playlist]`
  - `tests/test_job_outcome.py::test_a_parked_or_half_failed_job_answers_the_same_way_the_second_time_it_is_asked[parked-sync.favorites]`
  - `tests/test_job_outcome.py::test_a_parked_or_half_failed_job_leaves_every_queued_verb_non_zero[half-failed-export.playlist]`
  - `tests/test_job_outcome.py::test_a_parked_or_half_failed_job_leaves_every_queued_verb_non_zero[half-failed-sync.favorites]`
  - `tests/test_job_outcome.py::test_a_parked_or_half_failed_job_leaves_every_queued_verb_non_zero[parked-export.playlist]`
  - `tests/test_job_outcome.py::test_a_parked_or_half_failed_job_leaves_every_queued_verb_non_zero[parked-sync.favorites]`
  - `tests/test_job_outcome.py::test_every_function_that_drives_a_job_maps_its_ending_afterwards`

Old text:

```
jobs.raise_for_state(job)
```

New text:

```
jobs.get  # the mapping call, removed
```

### `r1308.M10_count_unchecked`

_removal_read_back: drop the whole number check on the count

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M10_count_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 23236 against a baseline of 23236
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

### `r835-b.T1_folder_create_never_retried`

TidalAccount.create_folder: a create that timed out after reaching the provider is retried into a second folder

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r835-b.json`, row `T1_folder_create_never_retried`
- Moved: the never retried folder create stayed in TidalAccount.create_folder in tidal_account.py, but its call to _call now sits on one line assigned to created; the same retries=0 is raised to 1
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_folder_create_is_never_retried_into_a_second_folder`

Old text:

```
        created = self._call(doing, lambda: self._session.user.create_folder(name), retries=0)

```

New text:

```
        created = self._call(doing, lambda: self._session.user.create_folder(name), retries=1)

```

### `r835-b.T2_refused_move_raised`

TidalAccount.move_to_folder: a move the client answers False is returned as done

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r835-b.json`, row `T2_refused_move_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
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
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
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

### `r836-a.A1_product_made_asked_first`

tidal_account.remove_tracks: the ledger is never asked, so a playlist the product did not create loses tracks

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r836-a.json`, row `A1_product_made_asked_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_heard.py::test_the_adapter_refuses_a_playlist_the_ledger_does_not_vouch_for_unasked`

Old text:

```
        if self._cfg is None or not ledger.product_made(self._cfg, identifier):
```

New text:

```
        if False:
```

### `u123.T1_adapter_vouching`

Drop the adapter's ledger check before a playlist removal

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u123.json`, row `T1_adapter_vouching`
- Moved: the same ledger check at the head of remove_playlist in tidal_account.py; the refusal is now raised through the shared _refused helper instead of refuse, so the text differs and the condition is reverted the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_heard.py::test_the_adapter_refuses_a_playlist_the_ledger_does_not_vouch_for_unasked`

Old text:

```
        if self._cfg is None or not ledger.product_made(self._cfg, identifier):
            raise _refused(
                f"the outbound ledger does not record the playlist {identifier} as "
                f"one this product created, so it was not removed and the provider "
```

New text:

```
        if False:
            raise _refused(
                f"the outbound ledger does not record the playlist {identifier} as "
                f"one this product created, so it was not removed and the provider "
```

### `u123.T2_read_back`

Trust the delete and never read the playlist back

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u123.json`, row `T2_read_back`
- Moved: the read back after a playlist's delete moved out of remove_playlist into _sent_and_read_back, shared with the kind playlist removal, and reads the playlist through _served, which answers None for an absent one; the same still served check is made never true
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_playlist_still_served_after_its_delete_is_refused_not_reported_removed`
  - `tests/test_label_heard.py::test_the_adapter_removes_a_vouched_playlist_and_reads_it_back_gone`

Old text:

```
        if self._served(doing, identifier) is not None:

```

New text:

```
        if False:

```

### `u123.T3_already_gone`

Ask the delete of a playlist the provider no longer has

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u123.json`, row `T3_already_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_playlist_already_gone_is_removed_with_no_delete`
  - `tests/test_label_heard.py::test_the_adapter_removes_a_vouched_playlist_and_reads_it_back_gone`

Old text:

```
        if found is _ABSENT or found is None:
            self._members.pop(identifier, None)
            return
```

New text:

```
        if found is None:
            self._members.pop(identifier, None)
            return
```

### `u143-d.A5_playlist_read_back`

Adapter: report a root playlist removed though the provider still serves it

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u143-d.json`, row `A5_playlist_read_back`
- Moved: the root removal's read back moved into tidal_account._sent_and_read_back, shared with remove_playlist, which reads the playlist through _served and answers None for absent; same still served check reverted
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_playlist_still_served_after_its_delete_is_refused_not_reported_removed`
  - `tests/test_label_heard.py::test_the_adapter_removes_a_vouched_playlist_and_reads_it_back_gone`

Old text:

```
        if self._served(doing, identifier) is not None:
```

New text:

```
        if False:
```

### `u309.U11_delete_read_back`

A delete the provider still serves afterwards is reported as a removal

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u309.json`, row `U11_delete_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_playlist_still_served_after_its_delete_is_refused_not_reported_removed`
  - `tests/test_label_heard.py::test_the_adapter_removes_a_vouched_playlist_and_reads_it_back_gone`

Old text:

```
        if self._served(doing, identifier) is not None:
            raise _refused(
```

New text:

```
        if False:
            raise _refused(
```

### `u309.U9_delete_answered_false`

A delete the provider answered False is read as sent

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u309.json`, row `U9_delete_answered_false`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_delete_the_client_answers_false_is_a_failure`
  - `tests/test_label_heard.py::test_a_playlist_still_served_after_its_delete_is_refused_not_reported_removed`
  - `tests/test_label_heard.py::test_the_adapter_removes_a_vouched_playlist_and_reads_it_back_gone`

Old text:

```
        if self._call(doing, send, retries=0) is False:
```

New text:

```
        if False:
```

### `r1313.T1_account_skips_the_classifier`

tidal_account._not_found: read the class names alone and stop asking classify_unavailable, so a 404 the account reads by status is retried

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r1313.json`, row `T1_account_skips_the_classifier`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_404_status_is_kept_as_a_not_found_at_either_seam[account]`

Old text:

```
    return classify_unavailable(exc) is TrackOutcome.UNAVAILABLE_PERMANENT

```

New text:

```
    return False

```

### `u206.M14_account_keeps_invalid_isrc`

TidalAccount._isrc_tracks: keep any no match as a not found, InvalidISRC included

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `u206.json`, row `M14_account_keeps_invalid_isrc`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`
- Collected: 60 against a baseline of 60
- Kills: 2 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_an_invalid_isrc_the_account_reads_as_no_match_is_never_kept`
  - `tests/test_isrc_cache.py::test_an_outage_then_an_invalid_isrc_on_the_retry_keeps_nothing`

Old text:

```
            if last["said_not_found"]:
                self._cache.remember(wanted, country, ())
```

New text:

```
            if True:
                self._cache.remember(wanted, country, ())
```

### `u206.M17_account_hit_ignored`

TidalAccount._isrc_tracks: never use a remembered answer

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `u206.json`, row `M17_account_hit_ignored`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`
- Collected: 60 against a baseline of 60
- Kills: 13 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_404_status_is_kept_as_a_not_found_at_either_seam[account]`
  - `tests/test_isrc_cache.py::test_a_choice_among_several_releases_is_made_from_a_remembered_answer_with_no_call`
  - `tests/test_isrc_cache.py::test_a_copy_run_redirecting_installation_state_shares_answers_through_the_override`
  - `tests/test_isrc_cache.py::test_a_second_account_over_a_fresh_client_asks_nothing_for_an_answered_isrc`
  - `tests/test_isrc_cache.py::test_a_tie_remembered_is_still_refused_with_its_reason`
  - `tests/test_isrc_cache.py::test_an_answer_is_kept_for_its_lifetime_and_asked_again_after_it[found-the-configured-days]`
  - `tests/test_isrc_cache.py::test_an_answer_is_kept_for_its_lifetime_and_asked_again_after_it[found-thirty-days-unless-set]`
  - `tests/test_isrc_cache.py::test_an_answer_is_kept_for_its_lifetime_and_asked_again_after_it[not-found-no-longer-than-a-shorter-setting]`
  - `tests/test_isrc_cache.py::test_an_answer_is_kept_for_its_lifetime_and_asked_again_after_it[not-found-seven-days]`
  - `tests/test_isrc_cache.py::test_an_expired_answer_is_replaced_by_the_new_one`
  - `tests/test_isrc_cache.py::test_an_outage_then_a_not_found_on_the_retry_keeps_the_not_found`
  - `tests/test_isrc_cache.py::test_the_catalogue_and_the_account_share_one_answer`
  - `tests/test_isrc_cache.py::test_the_process_counts_say_what_the_cache_settled_and_what_was_asked`

Old text:

```
        if held is not None:
            return held if held else _ABSENT
        # What the LAST attempt said
```

New text:

```
        if False:
            return held if held else _ABSENT
        # What the LAST attempt said
```

### `r1761.P9_emptied_passes_on_the_fact_file`

_unproven: the emptied flag passes on the fact file alone, which a database item writes at a mount point (round two's N2)

- File: `src/cratekit/modules/tools/backup_proof.py`
- Source: `r1761.json`, row `P9_emptied_passes_on_the_fact_file`
- Moved: U311 moved the census proof out of backup.py into backup_proof.py with this line unchanged. On the base the row was killed only by the seam allowance test, which the mutant tripped by an incidental reach into the facts module from backup.py, and the guard's own tests need rclone and are this container's failures; from backup_proof.py the same reach crosses no seam, so U311 added test_the_emptied_flag_passes_on_the_files_record_and_not_on_the_fact_file_alone in tests/modules/test_tools.py, which writes a database record alone and asserts the emptied flag is still refused, the guard round two's N2 named
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_import_rules.py::test_no_package_crosses_a_seam_beyond_its_allowance`

Old text:

```
        if carried is not None:
            return "", False
```

New text:

```
        if backup_facts.path_for(cfg).is_file():
            return "", False
```

### `u311.C5_binaries_out_of_order`

The shared binary lookup answers its names in reverse, swapping ffmpeg and ffprobe

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u311.json`, row `C5_binaries_out_of_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`
- Collected: 2 against a baseline of 2
- Kills: 2 (killed)
- Killed:
  - `tests/test_job_seam.py::test_a_driver_killed_inside_the_real_handler_resumes_redoing_exactly_that_item`
  - `tests/test_job_seam.py::test_the_partial_encode_a_kill_leaves_behind_is_in_staging_not_at_the_destination`

Old text:

```
        return [binaries.resolve(name) for name in names]
```

New text:

```
        return [binaries.resolve(name) for name in reversed(names)]
```

### `u117-operator.D14_organize_call`

organize: drop the one call line, so organize never plans a dated playlist

- File: `src/cratekit/organize/account.py`
- Source: `u117-operator.json`, row `D14_organize_call`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 24 against a baseline of 24
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_dated.py::test_an_unreadable_record_refuses_the_dated_step_alone`
  - `tests/test_label_dated.py::test_organize_plans_the_dated_playlist_after_the_label_folder_and_applies_in_order`
  - `tests/test_label_dated.py::test_organize_with_nothing_taken_plans_nothing`

Old text:

```
        dated.add_step(cfg, area, entry, planned, remote_of)

```

New text:

```
        pass

```

### `u214.M10_detail_names`

_detail: never name the unmirrored nodes on the step's line, so the report shows only a count

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u214.json`, row `M10_detail_names`
- Moved: the guard stays in account_mirror._detail, whose folder argument is now required, so the not None half of the condition is gone; same guard reverted
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`
- Collected: 27 against a baseline of 27
- Kills: 4 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_rebuild_from_the_frozen_plan_still_names_them`
  - `tests/test_inbox_unmirrored.py::test_an_inbox_with_no_batch_at_all_still_names_them`
  - `tests/test_inbox_unmirrored.py::test_an_inbox_with_nothing_to_write_still_names_them`
  - `tests/test_inbox_unmirrored.py::test_the_inbox_step_names_each_unmirrored_node_on_its_plan_and_its_line`

Old text:

```
    if folder.unmirrored:

```

New text:

```
    if False:

```

### `u214.M9_inbox_unmirrored`

_inbox: hand the folder no unmirrored node

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u214.json`, row `M9_inbox_unmirrored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`
- Collected: 27 against a baseline of 27
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_playlist_whose_record_cannot_be_read_is_never_said_to_have_none`
  - `tests/test_inbox_unmirrored.py::test_the_inbox_folder_mirrors_the_batch_and_names_the_other_nodes`

Old text:

```
        unmirrored=tuple((node.label(), node.reason) for node in live.left),
```

New text:

```
        unmirrored=(),
```

### `u246.S16_inspiration_held_per_element`

assert_read_back (inspiration): build the live set once per planned row again (the shape on main)

- File: `src/cratekit/organize/inspiration.py`
- Source: `u246.json`, row `S16_inspiration_held_per_element`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_comprehension_sets.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_comprehension_sets.py::test_no_comprehension_in_the_package_rebuilds_an_invariant_set_per_element`

Old text:

```
        missing = [row for row in one.members if row not in held]
```

New text:

```
        missing = [row for row in one.members if row not in set(live)]
```

### `u214.M11_frozen_carries`

mirror_frozen: rebuild every folder with no unmirrored node, so the run that applies loses the lines

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u214.json`, row `M11_frozen_carries`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`
- Collected: 27 against a baseline of 27
- Kills: 6 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_rebuild_from_the_frozen_plan_still_names_them`
  - `tests/test_inbox_unmirrored.py::test_frozen_unmirrored_nodes_that_are_not_pairs_of_text_are_not_read[not text]`
  - `tests/test_inbox_unmirrored.py::test_frozen_unmirrored_nodes_that_are_not_pairs_of_text_are_not_read[one part]`
  - `tests/test_inbox_unmirrored.py::test_frozen_unmirrored_nodes_that_are_not_pairs_of_text_are_not_read[text]`
  - `tests/test_inbox_unmirrored.py::test_frozen_unmirrored_nodes_that_are_not_pairs_of_text_are_not_read[three parts]`
  - `tests/test_inbox_unmirrored.py::test_the_frozen_plan_carries_the_unmirrored_nodes`

Old text:

```
                unmirrored=_unmirrored(folder["unmirrored"]),
```

New text:

```
                unmirrored=(),
```

### `r1255.R5_organize_rotation_warns`

organize _rotation: drop the shared warning, so crate organize ages a batch unsaid

- File: `src/cratekit/organize/rekordbox.py`
- Source: `r1255.json`, row `R5_organize_rotation_warns`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`

Old text:

```
    step.warnings.extend(rotate_cli.records_warnings(plan))
```

New text:

```
    pass
```

### `u214.M14_old_not_yours`

organize rotation step: list Old as the author's own again

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u214.json`, row `M14_old_not_yours`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`
- Collected: 27 against a baseline of 27
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_folder_named_old_inside_old_is_a_folder_and_listed_as_yours`
  - `tests/test_inbox_unmirrored.py::test_the_organize_rotation_step_does_not_list_old_as_yours`

Old text:

```
        if node.kind == rotate.LEFT_OLD:
```

New text:

```
        if False:
```

### `u309.U24_planned_step_apply_bound`

A planned step that writes is given no apply

- File: `src/cratekit/organize/steps.py`
- Source: `u309.json`, row `U24_planned_step_apply_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_dated.py::test_organize_plans_the_dated_playlist_after_the_label_folder_and_applies_in_order`

Old text:

```
    if writes and apply is not None:
        step.apply = partial(apply, step)
```

New text:

```
    if False:
        step.apply = partial(apply, step)
```

### `u27-restore-cli-independent.I_C4_the_session_identifier_becomes_required`

Make the positional mandatory, so a bare crate restore run is a usage error rather than the newest spendable capture

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-independent.json`, row `I_C4_the_session_identifier_becomes_required`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 1021 against a baseline of 1021
- Kills: 3 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_conformance_1_structured_output_is_actually_emitted[restore.run]`
  - `tests/test_cli_contract.py::test_conformance_2_exit_codes_are_from_the_vocabulary_and_never_status_two[restore.run]`
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[restore.run]`

Old text:

```
        "session_id",
        nargs="?",
        default=None,
```

New text:

```
        "session_id",
```

### `r835-c.S2_sync_hands_the_ledger_to_the_sweep_again`

sync.cli._plan_playlists: the sweep is handed no label built playlists, so every year playlist is swept as intake

- File: `src/cratekit/sync/cli.py`
- Source: `r835-c.json`, row `S2_sync_hands_the_ledger_to_the_sweep_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_the_sync_pass_hands_the_sweep_every_year_playlist_a_build_recorded`

Old text:

```
    label_built = ledger.label_playlist_ids(cfg)
```

New text:

```
    label_built = frozenset()
```

### `r837-a.A17_sweep_hand_off`

sync.cli: the sweep is handed no set playlist, so the exclusion has nothing to exclude

- File: `src/cratekit/sync/cli.py`
- Source: `r837-a.json`, row `A17_sweep_hand_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_the_sweep_never_reads_a_set_playlist_as_intake`

Old text:

```
            set_built=set_built,
```

New text:

```
            set_built=frozenset(),
```

### `r1056.S1_no_landing_step_names_intake_missing`

_native_proof: drop the named source from the no landing step, so a label batch is told intake missing

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r1056.json`, row `S1_no_landing_step_names_intake_missing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 34 against a baseline of 34
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_pass_no_closed_committed_native_landing_names_is_refused_by_name[abandoned]`
  - `tests/test_label_mark_native.py::test_a_pass_no_closed_committed_native_landing_names_is_refused_by_name[another-pass]`
  - `tests/test_label_mark_native.py::test_a_pass_no_closed_committed_native_landing_names_is_refused_by_name[never-committed]`
  - `tests/test_label_mark_native.py::test_a_pass_no_closed_committed_native_landing_names_is_refused_by_name[no-landing]`

Old text:

```
            f"land the pass with crate intake land --pass and {named}, then run {verb} "
```

New text:

```
            f"land the pass with crate intake land --pass and {SYNC_PASS_NAMED}, then run {verb} "
```

### `r1056.S2_unreachable_step_names_sync`

_native_proof: name sync mark in the unreachable library step whatever verb asked

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r1056.json`, row `S2_unreachable_step_names_sync`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_an_unreachable_library_names_label_mark_as_the_verb_to_run_again`

Old text:

```
            f"mount the library volume, then run {verb} again",
```

New text:

```
            "mount the library volume, then run crate sync mark again",
```

### `r777.N3_engine_unchecked`

apply_deferred no longer checks its proof before renaming

- File: `src/cratekit/sync/marks.py`
- Source: `r777.json`, row `N3_engine_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_external_marks_wait_for_local_output_and_recheck`

Old text:

```
    require_proof(local_output)
    applied: list[str] = []
```

New text:

```
    applied: list[str] = []
```

### `u246.S13_pair_cli_per_element`

pair: build the made here set once per pair again (the shape on main)

- File: `src/cratekit/sync/pair_check.py`
- Source: `u246.json`, row `S13_pair_cli_per_element`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_comprehension_sets.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_comprehension_sets.py::test_no_comprehension_in_the_package_rebuilds_an_invariant_set_per_element`

Old text:

```
                        if pair.account_id not in made_here
```

New text:

```
                        if pair.account_id not in set(ours.values())
```

### `u304.S3_agreement_clock_through_its_module`

pair_plan._moved_since_stop: the agreement window read off the wall clock, not pair_model._now; maintainer facing, since the two clocks agree outside a test, and round one's review measured that no test moves the clock on this path

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u304.json`, row `S3_agreement_clock_through_its_module`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 23236 against a baseline of 23236
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        elif first is not None and pair_model._now() - first >= AGREE_AFTER:
```

New text:

```
        elif first is not None and __import__("datetime").datetime.now(__import__("datetime").UTC) - first >= AGREE_AFTER:
```

### `r361-a.A10_enum_value_respelled`

The enum member's kebab value changes, so the report and the check say another word

- File: `src/cratekit/sync/playlists.py`
- Source: `r361-a.json`, row `A10_enum_value_respelled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_the_label_batch_debris_is_excluded_by_the_source_systems_own_rule`

Old text:

```
    LABEL_DEBRIS = "label-debris"
```

New text:

```
    LABEL_DEBRIS = "label-library"
```

### `r361-a.A2_case_insensitive`

The rule widens to any case, so a person's Colorize Library is excluded too

- File: `src/cratekit/sync/playlists.py`
- Source: `r361-a.json`, row `A2_case_insensitive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_the_label_batch_debris_is_excluded_by_the_source_systems_own_rule`

Old text:

```
    return str(name or "").endswith(LIBRARY_PLAYLIST_SUFFIX)
```

New text:

```
    return str(name or "").upper().endswith(LIBRARY_PLAYLIST_SUFFIX)
```

### `r361-a.A3_no_leading_space`

The suffix loses its leading space, so ColorizeLIBRARY is debris

- File: `src/cratekit/sync/playlists.py`
- Source: `r361-a.json`, row `A3_no_leading_space`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_the_label_batch_debris_is_excluded_by_the_source_systems_own_rule`

Old text:

```
LIBRARY_PLAYLIST_SUFFIX = " LIBRARY"
```

New text:

```
LIBRARY_PLAYLIST_SUFFIX = "LIBRARY"
```

### `r361-a.A4_substring_not_suffix`

endswith becomes in, so LIBRARY Colorize and Colorize LIBRARY 2 are debris

- File: `src/cratekit/sync/playlists.py`
- Source: `r361-a.json`, row `A4_substring_not_suffix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_the_label_batch_debris_is_excluded_by_the_source_systems_own_rule`

Old text:

```
    return str(name or "").endswith(LIBRARY_PLAYLIST_SUFFIX)
```

New text:

```
    return LIBRARY_PLAYLIST_SUFFIX in str(name or "")
```

### `r361-a.D2_drop_the_placeholder`

Existing: the favourites placeholder is queued by the playlists source

- File: `src/cratekit/sync/playlists.py`
- Source: `r361-a.json`, row `D2_drop_the_placeholder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_the_playlist_exclusions_in_the_order_a_person_is_told`

Old text:

```
    if placeholders.is_placeholder(playlist.name):
        return Excluded.PLACEHOLDER

```

New text:

```
(empty)
```

### `r361-a.D3_drop_in_flight`

Existing: an open job no longer holds its playlist back, so it is queued twice

- File: `src/cratekit/sync/playlists.py`
- Source: `r361-a.json`, row `D3_drop_in_flight`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_the_playlist_exclusions_in_the_order_a_person_is_told`

Old text:

```
    if playlist.playlist_id in in_flight:
        return Excluded.IN_FLIGHT

```

New text:

```
(empty)
```

### `r835-b.S1_built_year_excluded_from_sweep`

sync.playlists.exclusion: a year playlist a label build recorded is swept as intake

- File: `src/cratekit/sync/playlists.py`
- Source: `r835-b.json`, row `S1_built_year_excluded_from_sweep`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_the_sweep_never_reads_a_built_year_playlist_as_intake`

Old text:

```
    if playlist.playlist_id in label_built:
        return Excluded.LABEL_FOLDER
```

New text:

```
    if False:
        return Excluded.LABEL_FOLDER
```

### `r837-a.A16_sweep_excludes_set`

sync.playlists.exclusion: a set playlist export set recorded is swept as intake

- File: `src/cratekit/sync/playlists.py`
- Source: `r837-a.json`, row `A16_sweep_excludes_set`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_the_sweep_never_reads_a_set_playlist_as_intake`

Old text:

```
    if playlist.playlist_id in set_built:
        return Excluded.SET_PLAYLIST
```

New text:

```
    if False:
        return Excluded.SET_PLAYLIST
```

### `u113-a.A6_sweep_passes_no_name`

The sweep queues each playlist job without the account's name

- File: `src/cratekit/sync/playlists.py`
- Source: `u113-a.json`, row `A6_sweep_passes_no_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_sync_all_records_the_name_the_account_listed_on_each_playlist_job`

Old text:

```
                name=names.get(playlist_id),
```

New text:

```
                name=None,
```

### `r704-a.R1_increment_ignores_the_flag`

the increment never takes the rate limited branch, every lookup failure is permanent as before R-704

- File: `src/cratekit/sync/run.py`
- Source: `r704-a.json`, row `R1_increment_ignores_the_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_lookup_failure_is_permanent_unless_the_source_says_rate_limited`

Old text:

```
            if exc.rate_limited:
```

New text:

```
            if False:
```

### `r704-a.R2_rate_limit_not_retryable`

the rate limited refusal says resume and records the item permanent, so the job verdict and jobs.retry still refuse

- File: `src/cratekit/sync/run.py`
- Source: `r704-a.json`, row `R2_rate_limit_not_retryable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_lookup_failure_is_permanent_unless_the_source_says_rate_limited`

Old text:

```
                    retryable=True,
                    origin=("sync.run",),
```

New text:

```
                    retryable=False,
                    origin=("sync.run",),
```

### `r704-a.R3_remedy_retry_later`

the rate limited refusal names retry later rather than resuming the job

- File: `src/cratekit/sync/run.py`
- Source: `r704-a.json`, row `R3_remedy_retry_later`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_lookup_failure_is_permanent_unless_the_source_says_rate_limited`

Old text:

```
                    remedy=Remedy.RESUME_JOB,
```

New text:

```
                    remedy=Remedy.RETRY_LATER,
```

### `r704-a.R4_detail_unmarked`

the refusal's detail no longer says rate limited, so a machine reader cannot tell it from an outage

- File: `src/cratekit/sync/run.py`
- Source: `r704-a.json`, row `R4_detail_unmarked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_lookup_failure_is_permanent_unless_the_source_says_rate_limited`

Old text:

```
                    detail={"source_id": source.id, "rate_limited": True},
```

New text:

```
                    detail={"source_id": source.id},
```

### `r704-a.R5_flag_not_stored`

LookupFailure drops the flag it was handed

- File: `src/cratekit/sync/run.py`
- Source: `r704-a.json`, row `R5_flag_not_stored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_lookup_failure_is_permanent_unless_the_source_says_rate_limited`

Old text:

```
        self.rate_limited = rate_limited
```

New text:

```
        self.rate_limited = False
```

### `r704-a.R6_sentence_reworded`

the refusal no longer says the provider rate limited the lookup

- File: `src/cratekit/sync/run.py`
- Source: `r704-a.json`, row `R6_sentence_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_lookup_failure_is_permanent_unless_the_source_says_rate_limited`

Old text:

```
                    f"the provider rate limited a lookup {source.id} needed "
```

New text:

```
                    f"the provider throttled a lookup {source.id} needed "
```

### `u52-item-derivation.A1_acquires_early_return_gone`

R-140: an offering source writes the intake row, registers the artifact and moves the watermark over releases nobody accepted

- File: `src/cratekit/sync/run.py`
- Source: `u52-item-derivation.json`, row `A1_acquires_early_return_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`
- Collected: 31 against a baseline of 31
- Kills: 3 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_an_offering_run_leaves_the_source_watermark_unset`
  - `tests/test_incremental_sync.py::test_an_offering_source_writes_no_intake_file`
  - `tests/test_incremental_sync.py::test_one_run_records_only_the_acquiring_source_of_a_mixed_pair`

Old text:

```
        if not getattr(source, "acquires", True):
```

New text:

```
        if False:
```

### `u52-item-derivation.A2_acquires_default_false`

MUTATE THE COEFFICIENT: flip the getattr default, so every source written before the attribute existed stops recording what it acquired

- File: `src/cratekit/sync/run.py`
- Source: `u52-item-derivation.json`, row `A2_acquires_default_false`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`
- Collected: 31 against a baseline of 31
- Kills: 6 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_rerun_after_a_clean_sync_processes_only_unowned_items`
  - `tests/test_incremental_sync.py::test_a_watermark_does_not_empty_the_scope_of_unowned_items`
  - `tests/test_incremental_sync.py::test_an_acquiring_source_still_writes_the_intake_file_and_advances`
  - `tests/test_incremental_sync.py::test_one_run_records_only_the_acquiring_source_of_a_mixed_pair`
  - `tests/test_incremental_sync.py::test_one_source_failing_does_not_block_the_other`
  - `tests/test_incremental_sync.py::test_two_sources_in_one_run_share_one_importable_file`

Old text:

```
        if not getattr(source, "acquires", True):
```

New text:

```
        if not getattr(source, "acquires", False):
```

### `r259.S1_scope_owned_sample`

Existing guard sample: scope.scoped no longer drops owned identities

- File: `src/cratekit/sync/scope.py`
- Source: `r259.json`, row `S1_scope_owned_sample`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_rerun_after_a_clean_sync_processes_only_unowned_items`

Old text:

```
        if item.identity in owned:
```

New text:

```
        if False:
```

### `r263.S2_favorites_reason`

Favorites declares no reason, so its absent record reads as never again

- File: `src/cratekit/sync/sources.py`
- Source: `r263.json`, row `S2_favorites_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_favorites_is_not_reported_as_never_having_run`

Old text:

```
        no_cursor="no favorites worker records a cursor, so a completed sync "
```

New text:

```
        no_cursor="" and "no favorites worker records a cursor, so a completed sync "
```

### `u109-b.B3_no_cursor_reworded`

Reword the labels no_cursor sentence so it no longer names the guided verb

- File: `src/cratekit/sync/sources.py`
- Source: `u109-b.json`, row `B3_no_cursor_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`
- Collected: 31 against a baseline of 31
- Kills: 3 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_clean_labels_sweep_is_not_reported_as_never_having_run`
  - `tests/test_incremental_sync.py::test_a_stale_cursor_on_a_source_that_records_none_is_not_a_live_completion`
  - `tests/test_incremental_sync.py::test_doctor_prints_the_labels_row_it_is_given`

Old text:

```
        no_cursor="label releases are taken by crate label sync, which keeps "
```

New text:

```
        no_cursor="label releases are taken by the guided verb, which keeps "
```

### `u149.T21_landing_paired_again`

plan_landing: plan a twin for an account playlist already paired

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T21_landing_paired_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_twins.py`
- Collected: 5 against a baseline of 5
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_twins.py::test_an_account_playlist_already_paired_gets_no_second_twin`

Old text:

```
    wanted = [(account_id, name) for account_id, name in accounts if account_id not in held]
```

New text:

```
    wanted = list(accounts)
```

### `u149.T3_folder_names_unread`

find_folder: read no names inside a live folder, so a held name is not seen

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T3_folder_names_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_twins.py`
- Collected: 5 against a baseline of 5
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_twins.py::test_a_twin_name_the_folder_holds_is_left_and_named_and_the_landing_still_lands`

Old text:

```
held=_live_children(db, found[0]))
```

New text:

```
held=frozenset())
```

### `u149.T5_held_name_counted_free`

place: drop the refusal of a name the folder holds, so a second twin of one name is made

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T5_held_name_counted_free`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_twins.py`
- Collected: 5 against a baseline of 5
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_twins.py::test_a_twin_name_the_folder_holds_is_left_and_named_and_the_landing_still_lands`

Old text:

```
    if name in folder.held:
```

New text:

```
    if False:
```

### `u242.M22_unmark_releases_nothing`

sync unmark: never plan a release, so a pass's taken playlists cannot be let go

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `u242.json`, row `M22_unmark_releases_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`, `tests/test_label_playlists.py`
- Collected: 119 against a baseline of 119
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set.py::test_sync_unmark_takes_the_archive_mark_off_again`
  - `tests/test_label_playlists.py::test_sync_unmark_takes_the_label_mark_off_again`

Old text:

```
    taken_held = held is not None and held.held
```

New text:

```
    taken_held = False
```

### `r263.W1_no_unrecorded_state`

status_rows ignores the declared no_cursor reason, so every absent record reads as never

- File: `src/cratekit/sync/watermarks.py`
- Source: `r263.json`, row `W1_no_unrecorded_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`
- Collected: 31 against a baseline of 31
- Kills: 4 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_clean_labels_sweep_is_not_reported_as_never_having_run`
  - `tests/test_incremental_sync.py::test_a_stale_cursor_on_a_source_that_records_none_is_not_a_live_completion`
  - `tests/test_incremental_sync.py::test_doctor_prints_the_labels_row_it_is_given`
  - `tests/test_incremental_sync.py::test_favorites_is_not_reported_as_never_having_run`

Old text:

```
        reason = no_cursor.get(source_id)
```

New text:

```
        reason = None
```

### `r263.W2_state_word`

A cursorless source is reported with state never, detail unchanged

- File: `src/cratekit/sync/watermarks.py`
- Source: `r263.json`, row `W2_state_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`
- Collected: 31 against a baseline of 31
- Kills: 3 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_clean_labels_sweep_is_not_reported_as_never_having_run`
  - `tests/test_incremental_sync.py::test_a_stale_cursor_on_a_source_that_records_none_is_not_a_live_completion`
  - `tests/test_incremental_sync.py::test_favorites_is_not_reported_as_never_having_run`

Old text:

```
"state": "unrecorded"
```

New text:

```
"state": "never"
```

### `r263.W3_stale_record_as_completion`

A stale record on a cursorless source is reported as its last completion again

- File: `src/cratekit/sync/watermarks.py`
- Source: `r263.json`, row `W3_stale_record_as_completion`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_stale_cursor_on_a_source_that_records_none_is_not_a_live_completion`

Old text:

```
        if reason is not None:
```

New text:

```
        if reason is not None and mark is None:
```

