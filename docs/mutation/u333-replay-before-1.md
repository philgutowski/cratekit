# Mutation table: u333-replay-before-1

Measured by `scripts/mutate.py` on 2026-11-24 05:15 UTC, branch `HEAD` at `35e9a825`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23216 collected. pytest invocations for this batch: 421.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 05:15 UTC for commit `35e9a825cd73`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 42, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23216 against 23216. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u233.D7_readme_invents_a_flag` | `README.md` | user | 1 file(s) | 19 | 1 | killed |
| `u233.D2_guide_invents_a_verb` | `docs/GUIDE.md` | user | 1 file(s) | 19 | 1 | killed |
| `u233.D3_guide_invents_a_flag` | `docs/GUIDE.md` | user | 1 file(s) | 19 | 1 | killed |
| `u233.D4_guide_default_moves` | `docs/GUIDE.md` | user | 1 file(s) | 19 | 1 | killed |
| `u233.D5_guide_drops_a_key_row` | `docs/GUIDE.md` | user | 1 file(s) | 19 | 1 | killed |
| `u233.D6_guide_misspells_a_key` | `docs/GUIDE.md` | user | 1 file(s) | 19 | 1 | killed |
| `u251.W1_drop_worksteal` | `pyproject.toml` | maintainer | 1 file(s) | 58 | 1 | killed |
| `u200.M11_complete_clone_fetched` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 58 | 1 | killed |
| `u200.M1_unreadable_read_as_complete` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 58 | 1 | killed |
| `u200.M2_no_fetch` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 58 | 1 | killed |
| `u200.M3_no_reread` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 58 | 1 | killed |
| `u268.W11_error_count_singular_only` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 58 | 1 | killed |
| `u268.W1_id_cut_at_space` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 58 | 7 | killed |
| `u268.W2_errors_not_read` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 58 | 18 | killed |
| `u268.W3_no_report_read_as_clean` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 58 | 1 | killed |
| `u268.W4_counts_not_checked` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 58 | 1 | killed |
| `u268.W5_listed_not_checked` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 58 | 1 | killed |
| `u268.W6_id_with_line_break_stored` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 58 | 4 | killed |
| `u271-measured.B1_run_cleanliness_at_the_end_only` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 58 | 1 | killed |
| `u271-measured.B2_commit_read_after_the_run` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 58 | 1 | killed |
| `u271-measured.B3_status_unread` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 58 | 3 | killed |
| `u271-measured.B4_release_line_never_dirty` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 58 | 4 | killed |
| `u271-measured.B5_collection_errors_unlisted` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 58 | 1 | killed |
| `u271-measured.B6_count_unread_under_workers` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 58 | 2 | killed |
| `u271-measured.B8_ran_uncounted` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 58 | 4 | killed |
| `u273.P10_placeless_baseline_read` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 58 | 3 | killed |
| `u273.P11_other_place_compared` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 58 | 2 | killed |
| `u273.P13_rerun_disk_unchecked_upfront` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 58 | 1 | killed |
| `u273.P1_memory_any_filesystem` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 58 | 1 | killed |
| `u273.P2_no_floor` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 58 | 2 | killed |
| `u273.P3_disk_on_memory_accepted` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 58 | 2 | killed |
| `u273.P4_mount_first_match` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 58 | 1 | killed |
| `u273.P5_tmpdir_not_set` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 58 | 7 | killed |
| `u273.P6_no_rerun_on_disk` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 58 | 5 | killed |
| `u273.P8_disk_run_unchecked` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 58 | 1 | killed |
| `u313.C1_history_refusal_ignored` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 58 | 1 | killed |
| `u313.C3_tree_read_once` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 58 | 1 | killed |
| `u297.K1_a_zero_row_counted_as_a_kill` | `scripts/killset.py` | maintainer | 1 file(s) | 77 | 6 | killed |
| `u297.K2_a_lost_kill_passes_check` | `scripts/killset.py` | user | 1 file(s) | 77 | 6 | killed |
| `u297.K3_mapped_to_a_row_that_is_not_killed` | `scripts/killset.py` | user | 1 file(s) | 77 | 2 | killed |
| `u297.K4_a_collection_error_counts_as_a_kill` | `scripts/killset.py` | maintainer | 1 file(s) | 77 | 3 | killed |
| `u297.K5_any_reason_vouches_for_a_move` | `scripts/killset.py` | user | 1 file(s) | 77 | 3 | killed |
| `u297.K6_a_twin_read_as_a_move` | `scripts/killset.py` | user | 1 file(s) | 77 | 3 | killed |
| `u297.K7_a_batch_in_progress_read_as_finished` | `scripts/killset.py` | maintainer | 1 file(s) | 77 | 1 | killed |
| `u297.D4_a_measured_row_loses_its_source` | `scripts/mutate.py` | maintainer | 1 file(s) | 77 | 1 | killed |
| `u296.M10_type_checking_reads_as_running` | `scripts/refactor_measure.py` | maintainer | 1 file(s) | 57 | 4 | killed |
| `u296.M11_builder_imports_unread` | `scripts/refactor_measure.py` | maintainer | 1 file(s) | 57 | 2 | killed |
| `u296.M12_followed_through_a_blocked_module` | `scripts/refactor_measure.py` | maintainer | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u296.M13_own_verbs_dangle` | `scripts/refactor_measure.py` | maintainer | 1 file(s) | 57 | 2 | killed |
| `u296.M14_core_names_everywhere` | `scripts/refactor_measure.py` | maintainer | 1 file(s) | 57 | 3 | killed |
| `u296.M15_shadowed_alias_counts` | `scripts/refactor_measure.py` | maintainer | 1 file(s) | 57 | 1 | killed |
| `u296.M16_prune_adds_lines` | `scripts/refactor_measure.py` | maintainer | 1 file(s) | 31 | 1 | killed |
| `u296.M18_vendored_tree_read` | `scripts/refactor_measure.py` | maintainer | 1 file(s) | 31 | 1 | killed |
| `u296.M1_block_size` | `scripts/refactor_measure.py` | maintainer | 1 file(s) | 31 | 11 | killed |
| `u296.M22_initializer_relative_import` | `scripts/refactor_measure.py` | maintainer | 1 file(s) | 57 | 1 | killed |
| `u296.M23_except_branch_names_unread` | `scripts/refactor_measure.py` | maintainer | 1 file(s) | 57 | 1 | killed |
| `u296.M24_builder_names_a_home_directly` | `scripts/refactor_measure.py` | maintainer | 1 file(s) | 57 | 1 | killed |
| `u296.M25_dotted_import_alias` | `scripts/refactor_measure.py` | maintainer | 1 file(s) | 57 | 1 | killed |
| `u296.M26_core_package_name` | `scripts/refactor_measure.py` | maintainer | 1 file(s) | 57 | 1 | killed |
| `u296.M2_imports_count_as_lines` | `scripts/refactor_measure.py` | maintainer | 1 file(s) | 31 | 3 | killed |
| `u296.M3_allowance_forgets_places` | `scripts/refactor_measure.py` | maintainer | 1 file(s) | 31 | 1 | killed |
| `u296.M4_allowance_shared_between_packages` | `scripts/refactor_measure.py` | maintainer | 1 file(s) | 31 | 1 | killed |
| `u296.M5_private_inside_its_package` | `scripts/refactor_measure.py` | maintainer | 1 file(s) | 57 | 3 | killed |
| `u296.M6_private_through_a_module` | `scripts/refactor_measure.py` | maintainer | 1 file(s) | 57 | 3 | killed |
| `u296.M7_interface_binds_the_lower_layers` | `scripts/refactor_measure.py` | maintainer | 1 file(s) | 57 | 7 | killed |
| `u296.M8_interface_list_ignored` | `scripts/refactor_measure.py` | maintainer | 1 file(s) | 57 | 9 | killed |
| `u296.M9_lazy_reads_as_top_level` | `scripts/refactor_measure.py` | maintainer | 1 file(s) | 57 | 5 | killed |
| `u328.R1_starred_name_not_followed` | `scripts/refactor_measure.py` | maintainer | 1 file(s) | 57 | 2 | killed |
| `u328.R2_missing_part_read_as_empty` | `scripts/refactor_measure.py` | maintainer | 1 file(s) | 57 | 1 | killed |
| `u328.R3_starred_attribute_crashes` | `scripts/refactor_measure.py` | maintainer | 1 file(s) | 57 | 1 | killed |
| `u328.R4_loader_reads_the_registry_alone` | `scripts/refactor_measure.py` | maintainer | 1 file(s) | 57 | 1 | killed |
| `u331.M01_use_as_written_dropped` | `scripts/refactor_measure.py` | maintainer | 1 file(s) | 57 | 34 | killed |
| `u331.M03_lazy_from_import_hands_a_name` | `scripts/refactor_measure.py` | maintainer | 1 file(s) | 57 | 1 | killed |
| `u331.M04_one_hop_only` | `scripts/refactor_measure.py` | maintainer | 1 file(s) | 57 | 1 | killed |
| `u331.M05_chains_off_an_imported_name_unread` | `scripts/refactor_measure.py` | maintainer | 1 file(s) | 57 | 1 | killed |
| `u331.M06_attribute_use_not_followed` | `scripts/refactor_measure.py` | maintainer | 1 file(s) | 57 | 2 | killed |
| `u331.M07_followed_module_use_filtered_out` | `scripts/refactor_measure.py` | maintainer | 1 file(s) | 57 | 1 | killed |
| `u246.S2_adapter_per_element` | `src/cratekit/acquire/adapter.py` | maintainer | 1 file(s) | 33 | 1 | killed |
| `u207.C1_no_isrc_track_skipped` | `src/cratekit/acquire/catalogue_api.py` | user | 1 file(s) | 32 | 2 | killed |
| `u207.C2_code_not_asked_accepted` | `src/cratekit/acquire/catalogue_api.py` | user | 1 file(s) | 32 | 1 | killed |
| `u207.C3_paged_answer_accepted` | `src/cratekit/acquire/catalogue_api.py` | user | 1 file(s) | 32 | 1 | killed |
| `u207.C4_non_resource_skipped` | `src/cratekit/acquire/catalogue_api.py` | user | 1 file(s) | 32 | 1 | killed |
| `u207.C5_batch_ceiling_raised` | `src/cratekit/acquire/catalogue_api.py` | user | 1 file(s) | 32 | 4 | killed |
| `u207.C6_batch_shape_unchecked` | `src/cratekit/acquire/catalogue_api.py` | user | 1 file(s) | 32 | 1 | killed |
| `r290-author.S02_acquire_download_call_removed` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 126 | 6 | killed |
| `r1313.I2_cache_keeps_any_status` | `src/cratekit/acquire/isrc_cache.py` | user | 1 file(s) | 60 | 1 | killed |
| `u206-b.M10b_day_coefficient_halved` | `src/cratekit/acquire/isrc_cache.py` | user | 1 file(s) | 60 | 3 | killed |
| `u206-b.M2b_disabled_recall_composite` | `src/cratekit/acquire/isrc_cache.py` | user | 1 file(s) | 60 | 2 | killed |
| `u206.M11_unreadable_answer_kept` | `src/cratekit/acquire/isrc_cache.py` | user | 1 file(s) | 60 | 3 | killed |
| `u206.M12_corrupt_file_not_set_aside` | `src/cratekit/acquire/isrc_cache.py` | user | 1 file(s) | 60 | 3 | killed |
| `u206.M13_write_without_merge` | `src/cratekit/acquire/isrc_cache.py` | user | 2 file(s) | 68 | 4 | killed |
| `u206.M16_said_not_found_widened` | `src/cratekit/acquire/isrc_cache.py` | user | 1 file(s) | 60 | 3 | killed |
| `u206.M1_recall_never_hits` | `src/cratekit/acquire/isrc_cache.py` | user | 2 file(s) | 68 | 18 | killed |
| `u206.M21_override_ignored` | `src/cratekit/acquire/isrc_cache.py` | user | 1 file(s) | 60 | 1 | killed |
| `u206.M3_disabled_still_remembers` | `src/cratekit/acquire/isrc_cache.py` | user | 1 file(s) | 60 | 1 | killed |
| `u206.M4_unfolded_spelling_kept` | `src/cratekit/acquire/isrc_cache.py` | user | 1 file(s) | 60 | 1 | killed |
| `u206.M5_country_ignored` | `src/cratekit/acquire/isrc_cache.py` | user | 1 file(s) | 60 | 5 | killed |
| `u206.M6_not_found_lives_as_found` | `src/cratekit/acquire/isrc_cache.py` | user | 1 file(s) | 60 | 1 | killed |
| `u206.M7_not_found_ignores_shorter_setting` | `src/cratekit/acquire/isrc_cache.py` | user | 1 file(s) | 60 | 1 | killed |
| `u206.M8_expiry_off_by_one` | `src/cratekit/acquire/isrc_cache.py` | user | 1 file(s) | 60 | 5 | killed |
| `u206.M9_future_stamp_trusted` | `src/cratekit/acquire/isrc_cache.py` | user | 1 file(s) | 60 | 1 | killed |
| `u207.S1_any_client_screened` | `src/cratekit/acquire/isrc_screen.py` | user | 1 file(s) | 32 | 1 | killed |
| `u207.S2_lone_code_screened` | `src/cratekit/acquire/isrc_screen.py` | user | 1 file(s) | 32 | 1 | killed |
| `u207.S3_unfolded_spelling_screened` | `src/cratekit/acquire/isrc_screen.py` | user | 1 file(s) | 32 | 1 | killed |
| `u207.S4_rate_limit_keeps_screening` | `src/cratekit/acquire/isrc_screen.py` | user | 1 file(s) | 32 | 2 | killed |
| `u207.S5_refused_form_keeps_screening` | `src/cratekit/acquire/isrc_screen.py` | user | 1 file(s) | 32 | 3 | killed |
| `u207.S6_failed_batch_read_as_empty` | `src/cratekit/acquire/isrc_screen.py` | user | 1 file(s) | 32 | 8 | killed |
| `u207.S7_failed_batch_sent_again` | `src/cratekit/acquire/isrc_screen.py` | user | 1 file(s) | 32 | 2 | killed |
| `u77-c.C3_not_a_manifest` | `src/cratekit/acquire/listdoc.py` | user | 1 file(s) | 27 | 1 | killed |
| `u78-c.C1_readback_identity` | `src/cratekit/acquire/listdoc.py` | user | 1 file(s) | 8 | 2 | killed |
| `u78-c.C5_unlisted_checked_first` | `src/cratekit/acquire/listdoc.py` | user | 1 file(s) | 8 | 1 | killed |
| `r1016.M3_folder_parse_through_the_factory` | `src/cratekit/acquire/listing.py` | user | 1 file(s) | 56 | 1 | killed |
| `r878-a.A8_no_cursor_ends` | `src/cratekit/acquire/listing.py` | user | 1 file(s) | 56 | 2 | killed |
| `r878-a.A9_cursor_advances` | `src/cratekit/acquire/listing.py` | user | 1 file(s) | 56 | 2 | killed |
| `r878-b.B11_folder_rule_in_table` | `src/cratekit/acquire/listing.py` | user | 1 file(s) | 56 | 1 | killed |
| `r1709.M18_match_id_token` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 50 | 1 | killed |
| `r431-b.B4_the_engine_never_asks` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 40 | 1 | killed |
| `u265.M8_other_scorer` | `src/cratekit/acquire/match.py` | user | 2 file(s) | 90 | 10 | killed |
| `r1709.M11_recording_identity_is_the_token` | `src/cratekit/acquire/match_identity.py` | user | 1 file(s) | 50 | 2 | killed |
| `r1709.M4_bare_keeps_invisible` | `src/cratekit/acquire/match_identity.py` | user | 1 file(s) | 50 | 1 | killed |
| `r1709.M5_no_variation_selectors` | `src/cratekit/acquire/match_identity.py` | user | 1 file(s) | 50 | 1 | killed |
| `r1709.M9_title_identity_is_the_fold` | `src/cratekit/acquire/match_identity.py` | user | 2 file(s) | 82 | 4 | killed |
| `r431-b.B7_the_engine_asks_under_the_tombstones_kind` | `src/cratekit/acquire/match_identity.py` | user | 1 file(s) | 40 | 1 | killed |
| `r667.G3_members_not_split` | `src/cratekit/acquire/match_identity.py` | user | 1 file(s) | 40 | 1 | killed |
| `u305.M3_recorded_version_key_unfolded` | `src/cratekit/acquire/match_identity.py` | user | 1 file(s) | 50 | 2 | killed |
| `r664.E4_title_not_split` | `src/cratekit/acquire/match_library.py` | user | 2 file(s) | 90 | 13 | killed |
| `r667.E1_title_head_kept` | `src/cratekit/acquire/match_library.py` | user | 1 file(s) | 40 | 3 | killed |
| `r667.G8_no_credited_rule` | `src/cratekit/acquire/match_library.py` | user | 1 file(s) | 40 | 1 | killed |
| `r431-b.B2_a_row_billing_a_guest_asks` | `src/cratekit/acquire/match_list.py` | user | 1 file(s) | 40 | 1 | killed |
| `r431-b.B8_the_reader_never_counts_the_artists` | `src/cratekit/acquire/match_list.py` | user | 1 file(s) | 40 | 1 | killed |
| `u197.M5_adapter_name` | `src/cratekit/acquire/vendored.py` | user | 1 file(s) | 417 | 9 | killed |
| `u254.M07_always_append` | `src/cratekit/adopt/apply.py` | user | 1 file(s) | 10 | 2 | killed |
| `u254.M19_already_inverted` | `src/cratekit/adopt/apply.py` | user | 1 file(s) | 10 | 1 | killed |
| `r235-b.M25_adoption_refusal_names_no_verb` | `src/cratekit/adopt/apply_cli.py` | user | 1 file(s) | 40 | 2 | killed |
| `u132.W2_coded_note` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 49 | 2 | killed |
| `u132.W3_version_from_report` | `src/cratekit/adopt/apply_cli.py` | user | 1 file(s) | 3 | 1 | killed |
| `u165.A1_scope` | `src/cratekit/adopt/apply_cli.py` | user | 1 file(s) | 10 | 1 | killed |
| `u165.P1_undeclared` | `src/cratekit/adopt/plan.py` | user | 1 file(s) | 10 | 1 | killed |
| `u165.P2_vocal_sub` | `src/cratekit/adopt/plan.py` | user | 1 file(s) | 10 | 2 | killed |
| `u165.P3_of_vocal` | `src/cratekit/adopt/plan.py` | user | 1 file(s) | 10 | 1 | killed |
| `r744.A1_near_miss_widened` | `src/cratekit/analysis/agreement.py` | maintainer | 1 file(s) | 65 | 5 | killed |
| `r744.A2_half_not_recognised` | `src/cratekit/analysis/agreement.py` | maintainer | 1 file(s) | 65 | 4 | killed |
| `r744.A3_classic_names_unmapped` | `src/cratekit/analysis/agreement.py` | user | 1 file(s) | 65 | 18 | killed |
| `r744.A4_whole_number_counts_as_rekordbox` | `src/cratekit/analysis/agreement.py` | maintainer | 1 file(s) | 65 | 2 | killed |
| `r744.A5_removed_rows_counted` | `src/cratekit/analysis/agreement.py` | user | 1 file(s) | 65 | 2 | killed |
| `r744.A6_sample_never_full` | `src/cratekit/analysis/agreement.py` | maintainer | 1 file(s) | 65 | 1 | killed |
| `u343.M20_detection_head_keeps_a_key` | `src/cratekit/analysis/agreement.py` | maintainer | 1 file(s) | 65 | 1 | killed |
| `r744.B1_window_not_bound` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 65 | 1 | killed |
| `u157.A1_no_level_tag` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 41 | 1 | killed |
| `u157.A2_cut_unbound` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 41 | 1 | killed |
| `r744.E8_record_applies_to_every_window` | `src/cratekit/analysis/detect.py` | user | 1 file(s) | 65 | 1 | killed |
| `r744.E9_record_does_not_sum` | `src/cratekit/analysis/detect.py` | maintainer | 1 file(s) | 65 | 1 | killed |
| `u343.M22_record_keeps_key_buckets` | `src/cratekit/analysis/detect.py` | user | 1 file(s) | 65 | 1 | killed |
| `r290-author.R2_backup_rebuild_drops_the_type` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 126 | 1 | killed |
| `r290-author.S04_backup_call_removed` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 126 | 6 | killed |
| `r1334.S18_emit_open_gate_only` | `src/cratekit/cli/__init__.py` | user | 1 file(s) | 13 | 1 | killed |
| `r290-author.D1_dispatcher_ignores_the_type` | `src/cratekit/cli/__init__.py` | user | 1 file(s) | 126 | 42 | killed |
| `r290-author.D2_parked_marked_resumable` | `src/cratekit/cli/__init__.py` | user | 1 file(s) | 126 | 2 | killed |
| `r290-author.D4_cancelled_reads_failed` | `src/cratekit/cli/__init__.py` | user | 1 file(s) | 126 | 20 | killed |
| `u168.C10_argv_never` | `src/cratekit/cli/__init__.py` | user | 1 file(s) | 1020 | 2 | killed |
| `u168.C11_argv_whole_line` | `src/cratekit/cli/__init__.py` | user | 1 file(s) | 1020 | 2 | killed |
| `u168.C9_argv_on_every_run` | `src/cratekit/cli/__init__.py` | user | 1 file(s) | 1020 | 1 | killed |
| `u186.D1_dispatch_unhooked` | `src/cratekit/cli/__init__.py` | user | 1 file(s) | 34 | 9 | killed |
| `u186.D2_dispatch_any_refusal` | `src/cratekit/cli/__init__.py` | user | 1 file(s) | 34 | 1 | killed |
| `u186.D3_dispatch_scope` | `src/cratekit/cli/__init__.py` | user | 1 file(s) | 34 | 1 | killed |
| `u186.D4_dispatch_break_silent` | `src/cratekit/cli/__init__.py` | user | 1 file(s) | 34 | 1 | killed |
| `u206.M23_lookup_line_dropped` | `src/cratekit/cli/__init__.py` | user | 1 file(s) | 8 | 1 | killed |
| `u248.L10_built_before_the_builder` | `src/cratekit/cli/__init__.py` | maintainer | 1 file(s) | 161 | 1 | killed |
| `u248.L1_lazy_off` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 1181 | 12 | killed |
| `u248.L2_chosen_never_built` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 1181 | 314 | killed |
| `u248.L3_listing_asks_everyone` | `src/cratekit/cli/__init__.py` | maintainer | 1 file(s) | 161 | 4 | killed |
| `u248.L4_listing_drops_the_stub_line` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 1181 | 2 | killed |
| `u248.L5_listing_asked_twice` | `src/cratekit/cli/__init__.py` | maintainer | 1 file(s) | 161 | 2 | killed |
| `u248.L6_built_twice` | `src/cratekit/cli/__init__.py` | user | 1 file(s) | 161 | 1 | killed |
| `u248.L7_defect_as_stub` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 1181 | 2 | killed |
| `u248.L8_listing_raises_a_defect` | `src/cratekit/cli/__init__.py` | user | 1 file(s) | 161 | 1 | killed |
| `u248.L9_argument_error_unwrapped` | `src/cratekit/cli/__init__.py` | user | 1 file(s) | 161 | 2 | killed |
| `r235-a.M10_verb_guard_removed` | `src/cratekit/cli/cutover.py` | user | 1 file(s) | 40 | 1 | killed |
| `r235-b.M15_first_of_several_roots` | `src/cratekit/cli/cutover.py` | user | 1 file(s) | 40 | 1 | killed |
| `r235-b.M16_native_tree_offered_again` | `src/cratekit/cli/cutover.py` | user | 1 file(s) | 40 | 2 | killed |
| `r235-b.M19_unready_library_asked` | `src/cratekit/cli/cutover.py` | user | 1 file(s) | 40 | 6 | killed |
| `r235-b.M20_refusal_without_the_table` | `src/cratekit/cli/cutover.py` | user | 1 file(s) | 40 | 5 | killed |
| `r235-b.M21_digest_blind_to_the_plan` | `src/cratekit/cli/cutover.py` | user | 1 file(s) | 40 | 1 | killed |
| `r787.V1_verb_own_list` | `src/cratekit/cli/cutover.py` | user | 1 file(s) | 40 | 1 | killed |
| `r787.V2_undeclared_step_routing_only` | `src/cratekit/cli/cutover.py` | user | 1 file(s) | 40 | 1 | killed |
| `r787.V3_catalogue_refusal_loses_set` | `src/cratekit/cli/cutover.py` | user | 1 file(s) | 40 | 1 | killed |
| `r1255.D2_status_names_the_log` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 1 | killed |
| `r1255.D3_status_guard_precise` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 1 | killed |
| `u184.D8_check_unlisted` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 6 | killed |
| `u303.D3_offered_ignores_required` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 6 | killed |
| `u303.D4_run_ignores_probes` | `src/cratekit/cli/doctor.py` | user | 2 file(s) | 1437 | 78 | killed |
| `u328.S3_a_part_imported_past_the_registry` | `src/cratekit/cli/doctor.py` | maintainer | 1 file(s) | 57 | 1 | killed |
| `u184.D1_volume_not_established` | `src/cratekit/cli/doctor_backup.py` | user | 1 file(s) | 417 | 1 | killed |
| `u184.D2_unreadable_is_a_note` | `src/cratekit/cli/doctor_backup.py` | user | 1 file(s) | 417 | 1 | killed |
| `u184.D3_remedy_chosen_here` | `src/cratekit/cli/doctor_backup.py` | user | 1 file(s) | 417 | 1 | killed |
| `u184.D4_expired_read_as_valid` | `src/cratekit/cli/doctor_backup.py` | user | 1 file(s) | 417 | 1 | killed |
| `u184.D5_wall_clock` | `src/cratekit/cli/doctor_backup.py` | user | 1 file(s) | 417 | 1 | killed |
| `u184.D6_hours_coefficient` | `src/cratekit/cli/doctor_backup.py` | user | 1 file(s) | 417 | 1 | killed |
| `u184.D7_rule_not_named` | `src/cratekit/cli/doctor_backup.py` | user | 1 file(s) | 417 | 1 | killed |
| `u185.D1_push_newer_warns` | `src/cratekit/cli/doctor_backup.py` | user | 1 file(s) | 417 | 2 | killed |
| `u185.D2_hidden_entries` | `src/cratekit/cli/doctor_backup.py` | user | 1 file(s) | 417 | 4 | killed |
| `u185.D3_unread_folder` | `src/cratekit/cli/doctor_backup.py` | user | 1 file(s) | 417 | 2 | killed |
| `u224.M10_refused_backups_read_no_push` | `src/cratekit/cli/doctor_backup.py` | user | 1 file(s) | 417 | 1 | killed |
| `u224.M1_found_ignored` | `src/cratekit/cli/doctor_backup.py` | user | 1 file(s) | 417 | 7 | killed |
| `u224.M2_unread_place_dropped` | `src/cratekit/cli/doctor_backup.py` | user | 1 file(s) | 417 | 1 | killed |
| `u224.M3_broken_installed_probe_silent` | `src/cratekit/cli/doctor_backup.py` | user | 1 file(s) | 417 | 1 | killed |
| `u224.M4_unread_support_read_absent` | `src/cratekit/cli/doctor_backup.py` | user | 1 file(s) | 417 | 1 | killed |
| `u224.M5_refused_stat_read_absent` | `src/cratekit/cli/doctor_backup.py` | user | 1 file(s) | 417 | 4 | killed |
| `u224.M6_unread_folded_into_not_installed` | `src/cratekit/cli/doctor_backup.py` | user | 1 file(s) | 417 | 4 | killed |
| `u224.M7_install_signals_always_asked` | `src/cratekit/cli/doctor_backup.py` | maintainer | 1 file(s) | 417 | 1 | killed |
| `u224.M9_path_through_a_file_unread` | `src/cratekit/cli/doctor_backup.py` | user | 1 file(s) | 417 | 1 | killed |
| `u263.D21_doctor_names_verbs` | `src/cratekit/cli/doctor_keys.py` | user | 1 file(s) | 417 | 1 | killed |
| `u97-b.B1_doctor_routes_the_wrong_credential_token` | `src/cratekit/cli/doctor_keys.py` | user | 1 file(s) | 417 | 1 | killed |
| `u132.D1_doctor_behind` | `src/cratekit/cli/doctor_library.py` | user | 1 file(s) | 417 | 2 | killed |
| `u132.D2_doctor_defect` | `src/cratekit/cli/doctor_library.py` | user | 1 file(s) | 417 | 1 | killed |
| `u27-reports-round-1.D2_required_gate` | `src/cratekit/cli/doctor_library.py` | user | 1 file(s) | 417 | 1 | killed |
| `u27-reports-round-1.D3_trash_remedy` | `src/cratekit/cli/doctor_library.py` | user | 1 file(s) | 417 | 1 | killed |
| `u27-reports-round-3-fixes.F3_trash_absent_is_a_failure` | `src/cratekit/cli/doctor_library.py` | user | 1 file(s) | 417 | 1 | killed |
| `u27-round-8-independent.E1_mount_detail_swapped` | `src/cratekit/cli/doctor_library.py` | user | 1 file(s) | 417 | 1 | killed |
| `u27-round-8-independent.E2_identity_verdict_green` | `src/cratekit/cli/doctor_library.py` | user | 1 file(s) | 417 | 3 | killed |
| `u27-round-8-independent.E3_found_at_dropped` | `src/cratekit/cli/doctor_library.py` | user | 1 file(s) | 417 | 1 | killed |
| `u159.M10_unread_reads_none_published` | `src/cratekit/cli/doctor_model.py` | user | 1 file(s) | 417 | 1 | killed |
| `u181.D7_scored_probe_false` | `src/cratekit/cli/doctor_model.py` | user | 1 file(s) | 417 | 1 | killed |
| `u224.M8_default_probe_empty` | `src/cratekit/cli/doctor_model.py` | user | 1 file(s) | 417 | 1 | killed |
| `u27-reports-round-2.D1_probe_creates` | `src/cratekit/cli/doctor_model.py` | user | 1 file(s) | 417 | 1 | killed |
| `r-1.E1_dispatch_impl` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 417 | 1 | killed |
| `r-1.E2_config_inside_checkout` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 417 | 1 | killed |
| `r-1.T10_no_yaml_falls_back` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 417 | 1 | killed |
| `r-1.T12_caller_ignores_unknown` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 417 | 2 | killed |
| `r-1.T13_missing_other_hook` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 417 | 2 | killed |
| `r-1.T15_other_dispatch` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 417 | 1 | killed |
| `r-1.T16_same_configuration` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 417 | 1 | killed |
| `r-1.T17_install_config_flag` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 417 | 1 | killed |
| `r-1.T18_remedy_floor` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 417 | 1 | killed |
| `r-1.T19_remedy_reads_config` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 417 | 1 | killed |
| `r-1.T1_manual_skip` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 417 | 1 | killed |
| `r-1.T20_stage_parameter` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 417 | 3 | killed |
| `r-1.T21_ok_names_others` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 417 | 1 | killed |
| `r-1.T22_pre_commit_floor` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 417 | 13 | killed |
| `r-1.T23_alias_value` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 417 | 1 | killed |
| `r-1.T2_alias_map` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 417 | 2 | killed |
| `r-1.T3_default_install_types` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 417 | 1 | killed |
| `r-1.T4_default_stages` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 417 | 1 | killed |
| `r-1.T5_hook_stages` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 417 | 12 | killed |
| `r-1.T6_unknown_stage` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 417 | 2 | killed |
| `r-1.T7_dedupe` | `src/cratekit/cli/doctor_state.py` | maintainer | 1 file(s) | 417 | 2 | killed |
| `r-1.T8_not_a_mapping` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 417 | 1 | killed |
| `r-1.T9_yaml_error_falls_back` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 417 | 1 | killed |
| `r1255.D1_doctor_branches_on_the_scan` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 417 | 1 | killed |
| `r598-b.B6_doctor_clause_dropped` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 417 | 1 | killed |
| `r787.D1_doctor_own_list` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 40 | 4 | killed |
| `r787.D2_set_guard_removed` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 40 | 1 | killed |
| `r787.D3_source_guard_removed` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 40 | 1 | killed |
| `u159.M8_behind_reads_current` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 417 | 4 | killed |
| `u181.D1_extras_row_never_ok` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 417 | 2 | killed |
| `u181.D2_files_offered_reinstall` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 417 | 1 | killed |
| `u181.D3_release_form_dropped` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 417 | 3 | killed |
| `u181.D4_release_form_no_vocals` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 417 | 2 | killed |
| `u181.D5_upgrade_never_adds_vocals` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 417 | 1 | killed |
| `u181.D6_upgrade_always_adds_vocals` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 417 | 2 | killed |
| `u186.N1_note_age` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 34 | 1 | killed |
| `u186.N2_note_fails` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 34 | 2 | killed |
| `u186.N3_note_unreadable_dropped` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 34 | 2 | killed |
| `u206.M24_doctor_set_aside_unnamed` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 60 | 1 | killed |
| `u303.D2_vocals_kind_inverted` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 417 | 4 | killed |
| `u331.S13_doctor_state_loads_the_taxonomy_loader_at_top` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 161 | 1 | killed |
| `r745-b.C1_pending_name_accepted` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 94 | 3 | killed |
| `r745-b.C3_create_not_exclusive` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 94 | 2 | killed |
| `r745-b.C4_torn_file_left` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 94 | 1 | killed |
| `r745-b.C5_made_folders_left` | `src/cratekit/cli/export_collection.py` | maintainer | 1 file(s) | 94 | 1 | killed |
| `r745-b.C6_folder_not_asked_before_the_copy` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 94 | 1 | killed |
| `r745-b.C8_live_database_opened` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 94 | 3 | killed |
| `r745-c.C2_existing_file_not_checked_first` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 94 | 1 | killed |
| `r745-c.C7_a_file_taken_for_a_folder` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 94 | 1 | killed |
| `r773-b.C10_summary_remapped_zero` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 94 | 1 | killed |
| `r773-b.C1_no_rule_handed_to_the_emitter` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 94 | 3 | killed |
| `r773-b.C2_root_not_the_library_root` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 94 | 5 | killed |
| `r773-b.C3_warning_not_given` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 94 | 5 | killed |
| `r773-b.C4_warning_counts_prefixes_as_rows` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 94 | 5 | killed |
| `r773-b.C5_prefix_cap_two` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 94 | 3 | killed |
| `r773-b.C6_rest_of_the_prefixes_not_counted` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 94 | 2 | killed |
| `r773-b.C7_check_always_ok` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 94 | 1 | killed |
| `r773-b.C8_summary_unmapped_zero` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 94 | 3 | killed |
| `r773-b.C9_summary_left_zero` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 94 | 1 | killed |
| `r1334.E1_offer_after_compare` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 13 | 3 | killed |
| `r1334.E2_stale_compare_dropped` | `src/cratekit/cli/gates.py` | user | 3 file(s) | 1040 | 10 | killed |
| `r1334.E3_record_binds_no_offer` | `src/cratekit/cli/gates.py` | user | 3 file(s) | 1040 | 12 | killed |
| `r1334.S10_unknown_option_no_context` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 13 | 1 | killed |
| `r1334.S11_unknown_option_shown_dropped` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 13 | 1 | killed |
| `r1334.S1_stale_not_offered` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 13 | 7 | killed |
| `r1334.S2_stale_screen_without_plan` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 13 | 5 | killed |
| `r1334.S3_offered_ignored` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 13 | 7 | killed |
| `r1334.S4_screen_always` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 13 | 3 | killed |
| `r1334.S5_screen_no_shown` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 13 | 5 | killed |
| `r1334.S6_screen_shown_empty_for_none` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 13 | 1 | killed |
| `r1334.S7_screen_no_options` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 13 | 4 | killed |
| `r1334.S8_screen_no_prompt` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 13 | 1 | killed |
| `r1334.S9_screen_explicit_false` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 13 | 1 | killed |
| `r1349.C1_argv_ignored` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 13 | 3 | killed |
| `r1349.C2_run_dropped` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 13 | 3 | killed |
| `r1349.E2_open_left` | `src/cratekit/cli/gates.py` | user | 2 file(s) | 47 | 4 | killed |
| `r1349.E3_offer_unrecorded` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1087 | 19 | killed |
| `r1349.N1_guard_gone` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 13 | 5 | killed |
| `r1349.N2_any_gate` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 13 | 1 | killed |
| `r1349.N3_offer_ignored` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 13 | 1 | killed |
| `r1349.N4_open_ignored` | `src/cratekit/cli/gates.py` | user | 3 file(s) | 1067 | 6 | killed |
| `r1349.N5_answered_ignored` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 13 | 1 | killed |
| `r1349.N6_offer_inverted` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 13 | 6 | killed |
| `r1349.N7_written_before_refusal` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 13 | 3 | killed |
| `r1349.N8_after_unknown_swapped` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 13 | 1 | killed |
| `r1349.R1_reason_open_gate` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 13 | 3 | killed |
| `r1349.R2_answer_remedy` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 13 | 1 | killed |
| `r1349.R3_waiting_ignored` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 13 | 2 | killed |
| `r1349.R4_continue_wrong` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 13 | 4 | killed |
| `r1349.R5_open_gate_detail` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 13 | 1 | killed |
| `r1349.R6_message_no_gate` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 13 | 2 | killed |
| `r1349.R7_answer_step_dropped` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 13 | 1 | killed |
| `u161.G1_pin_never_compared` | `src/cratekit/cli/gates.py` | user | 2 file(s) | 51 | 4 | killed |
| `u161.G2_pin_overwritten_before_compare` | `src/cratekit/cli/gates.py` | user | 2 file(s) | 51 | 3 | killed |
| `u161.G3_absence_read_as_agreement` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 7 | 2 | killed |
| `u161.G4_pins_not_written` | `src/cratekit/cli/gates.py` | user | 2 file(s) | 51 | 24 | killed |
| `u161.G5_pins_not_read` | `src/cratekit/cli/gates.py` | user | 2 file(s) | 51 | 24 | killed |
| `u168.C12_argv_not_saved` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 1020 | 2 | killed |
| `u186.S10_scope_every_verb` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 34 | 2 | killed |
| `u186.S1_window_wider` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 34 | 2 | killed |
| `u186.S2_window_narrower` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 34 | 1 | killed |
| `u186.S3_exclude_self` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 34 | 19 | killed |
| `u186.S4_other_verb` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 34 | 1 | killed |
| `u186.S5_unreadable_dropped` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 34 | 2 | killed |
| `u186.S6_unrecorded_time_old` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 34 | 1 | killed |
| `u186.S7_open_drops_answers` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 34 | 1 | killed |
| `u186.S8_open_read_as_answered` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 34 | 4 | killed |
| `u186.S9_unreadable_unsaid` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 34 | 2 | killed |
| `u49-author.G2_the_second_raise_site_drops_the_context` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 1020 | 1 | killed |
| `u270.H1_batch_size_floor` | `src/cratekit/cli/handlers.py` | maintainer | 1 file(s) | 32 | 1 | killed |
| `u270.H2_run_job_drives_the_batch` | `src/cratekit/cli/handlers.py` | user | 1 file(s) | 32 | 1 | killed |
| `u46-author.H1_binding_removed` | `src/cratekit/cli/handlers.py` | user | 2 file(s) | 34 | 3 | killed |
| `u46-author.H2_is_known_always_true` | `src/cratekit/cli/handlers.py` | user | 1 file(s) | 32 | 2 | killed |
| `u46-author.H3_import_before_refusing` | `src/cratekit/cli/handlers.py` | maintainer | 1 file(s) | 32 | 1 | killed |
| `u46-author.H4_unbound_reason_silent` | `src/cratekit/cli/handlers.py` | user | 1 file(s) | 23216 | 1 (promoted) | killed |
| `u46-author.H5_fresh_config` | `src/cratekit/cli/handlers.py` | user | 1 file(s) | 32 | 2 | killed |
| `u46-author.H7_no_drift` | `src/cratekit/cli/handlers.py` | user | 1 file(s) | 32 | 1 | killed |
| `u46-author.H8_drift_wording_dropped` | `src/cratekit/cli/handlers.py` | user | 1 file(s) | 32 | 1 | killed |
| `u52-item-derivation.B1_label_import_unbound` | `src/cratekit/cli/handlers.py` | user | 1 file(s) | 32 | 1 | killed |
| `u52-item-derivation.B2_sync_labels_unbound` | `src/cratekit/cli/handlers.py` | user | 1 file(s) | 32 | 1 | killed |
| `u55-collection-reader.R30_scan_handler_bound` | `src/cratekit/cli/handlers.py` | user | 1 file(s) | 32 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R39_tag_folder_unbound` | `src/cratekit/cli/handlers.py` | user | 1 file(s) | 32 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R40_tag_retag_unbound` | `src/cratekit/cli/handlers.py` | user | 1 file(s) | 32 | 1 | killed |
| `u58-workers-and-wav.H1_run_unbound` | `src/cratekit/cli/handlers.py` | user | 1 file(s) | 32 | 1 | killed |
| `u182.M10_dry_run_writes` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 84 | 1 | killed |
| `u182.M12_empty_set_copies` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 84 | 1 | killed |
| `u182.M13_identity_parse` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 84 | 2 | killed |
| `u182.M13b_sweep_verbatim` | `src/cratekit/cli/jobs.py` | maintainer | 1 file(s) | 84 | 1 | killed |
| `u182.M14c_frees_set_composite` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 84 | 1 | killed |
| `u182.M15_name_fallback` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 84 | 2 | killed |
| `u182.M16_naive_instant` | `src/cratekit/cli/jobs.py` | maintainer | 1 file(s) | 84 | 1 | killed |
| `u182.M17_summary_playlist` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 84 | 3 | killed |
| `u182.M1_days_floor` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 84 | 1 | killed |
| `u182.M2c_running_composite` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 84 | 4 | killed |
| `u182.M3_blocked_offered` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 84 | 1 | killed |
| `u182.M4_unknown_age_stale` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 84 | 1 | killed |
| `u182.M5_cutoff` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 84 | 3 | killed |
| `u182.M6_listing_lock_check` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 84 | 1 | killed |
| `u182.M7_frees_identity` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 84 | 1 | killed |
| `u182.M8_keeper_kept` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 84 | 2 | killed |
| `u182.M9_keeper_newest` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 84 | 2 | killed |
| `u190.L1_no_tail_returns_untouched` | `src/cratekit/cli/label_sync.py` | user | 1 file(s) | 1020 | 1 | killed |
| `u235.T1_tail_back_to_sixteen_bits` | `src/cratekit/cli/output.py` | user | 1 file(s) | 1020 | 2 | killed |
| `u235.T2_tail_thirty_two_bits` | `src/cratekit/cli/output.py` | user | 1 file(s) | 1020 | 1 | killed |
| `u235.T3_tail_fifty_six_bits` | `src/cratekit/cli/output.py` | user | 1 file(s) | 1020 | 1 | killed |
| `u235.T4_tail_from_the_instant` | `src/cratekit/cli/output.py` | user | 1 file(s) | 1020 | 1 | killed |
| `u235.T5_instant_ignored` | `src/cratekit/cli/output.py` | maintainer | 1 file(s) | 1020 | 2 | killed |
| `u235.T6_stamp_loses_its_colons` | `src/cratekit/cli/output.py` | user | 1 file(s) | 1020 | 2 | killed |
| `r83.P1_flush` | `src/cratekit/cli/prompt.py` | user | 1 file(s) | 417 | 1 | killed |
| `r83.P2_nothing_entered_raise` | `src/cratekit/cli/prompt.py` | user | 1 file(s) | 417 | 2 | killed |
| `u328.S1_a_part_left_out_of_the_table` | `src/cratekit/cli/registry.py` | user | 8 file(s) | 1585 | collection error | collect-error |

## Zero rows and what they owe

- `u296.M12_followed_through_a_blocked_module` (maintainer facing): maintainer facing, composite not required

## Row definitions

### `u233.D7_readme_invents_a_flag`

README: crate login NAME --from-file becomes --from-path, a flag login does not take

- File: `README.md`
- Source: `u233.json`, row `D7_readme_invents_a_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_docs_current.py`
- Collected: 19 against a baseline of 19
- Kills: 1 (killed)
- Killed:
  - `tests/test_docs_current.py::test_every_verb_a_doc_names_exists_with_its_flags[README.md]`

Old text:

```
`crate login NAME --from-file PATH` records a credential in the keychain.
```

New text:

```
`crate login NAME --from-path PATH` records a credential in the keychain.
```

### `u233.D2_guide_invents_a_verb`

guide: crate route pending in a fenced block becomes route pendings, a verb help does not list

- File: `docs/GUIDE.md`
- Source: `u233.json`, row `D2_guide_invents_a_verb`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_docs_current.py`
- Collected: 19 against a baseline of 19
- Kills: 1 (killed)
- Killed:
  - `tests/test_docs_current.py::test_every_verb_a_doc_names_exists_with_its_flags[GUIDE.md]`

Old text:

```
crate route pending

```

New text:

```
crate route pendings

```

### `u233.D3_guide_invents_a_flag`

guide: intake missing --run becomes --runs, a flag the verb does not take

- File: `docs/GUIDE.md`
- Source: `u233.json`, row `D3_guide_invents_a_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_docs_current.py`
- Collected: 19 against a baseline of 19
- Kills: 1 (killed)
- Killed:
  - `tests/test_docs_current.py::test_every_verb_a_doc_names_exists_with_its_flags[GUIDE.md]`

Old text:

```
crate intake missing --run RUN_ID     # a whole sync all pass, one list
```

New text:

```
crate intake missing --runs RUN_ID    # a whole sync all pass, one list
```

### `u233.D4_guide_default_moves`

guide: the settings table states analysis.drift_cut as 1.4 against the schema's 1.5

- File: `docs/GUIDE.md`
- Source: `u233.json`, row `D4_guide_default_moves`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_docs_current.py`
- Collected: 19 against a baseline of 19
- Kills: 1 (killed)
- Killed:
  - `tests/test_docs_current.py::test_the_settings_table_is_the_schema`

Old text:

```
| `analysis.drift_cut` | 1.5 |
```

New text:

```
| `analysis.drift_cut` | 1.4 |
```

### `u233.D5_guide_drops_a_key_row`

guide: the settings table loses its provider.cooldown_s row

- File: `docs/GUIDE.md`
- Source: `u233.json`, row `D5_guide_drops_a_key_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_docs_current.py`
- Collected: 19 against a baseline of 19
- Kills: 1 (killed)
- Killed:
  - `tests/test_docs_current.py::test_the_settings_table_is_the_schema`

Old text:

```
| `provider.cooldown_s` | 900 |

```

New text:

```
(empty)
```

### `u233.D6_guide_misspells_a_key`

guide: prose spells labels.offers_per_sweep, a key the schema does not have

- File: `docs/GUIDE.md`
- Source: `u233.json`, row `D6_guide_misspells_a_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_docs_current.py`
- Collected: 19 against a baseline of 19
- Kills: 1 (killed)
- Killed:
  - `tests/test_docs_current.py::test_every_config_key_a_doc_spells_exists[GUIDE.md]`

Old text:

```
(releases kept in review per sweep, `labels.offer_per_sweep` by default),
```

New text:

```
(releases kept in review per sweep, `labels.offers_per_sweep` by default),
```

### `u251.W1_drop_worksteal`

pyproject addopts: drop --dist worksteal, so the suite runs under xdist's default distribution again

- File: `pyproject.toml`
- Source: `u251.json`, row `W1_drop_worksteal`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_failure_that_moved_between_workers_is_read_by_its_id`

Old text:

```
addopts = "-q -n auto --dist worksteal"
```

New text:

```
addopts = "-q -n auto"
```

### `u200.M11_complete_clone_fetched`

ensure_full_history: fetch a complete clone too, the review's survivor its fix round pins

- File: `scripts/cloud_battery.py`
- Source: `u200.json`, row `M11_complete_clone_fetched`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_complete_clone_runs_no_fetch`

Old text:

```
    if state == "false":
        return None
    if state != "true":
        return state
```

New text:

```
    if state not in ("true", "false"):
        return state
```

### `u200.M1_unreadable_read_as_complete`

ensure_full_history: read any answer but true as a complete clone, so a directory git cannot read passes

- File: `scripts/cloud_battery.py`
- Source: `u200.json`, row `M1_unreadable_read_as_complete`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_directory_git_cannot_read_is_never_read_as_complete_or_clean`

Old text:

```
    if state != "true":
        return state
```

New text:

```
    if state != "true":
        return None
```

### `u200.M2_no_fetch`

ensure_full_history: never fetch, so a shallow clone stays shallow

- File: `scripts/cloud_battery.py`
- Source: `u200.json`, row `M2_no_fetch`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_shallow_clone_is_unshallowed_and_the_baseline_header_says_so`

Old text:

```
["git", "fetch", "--unshallow", "origin", "main"]
```

New text:

```
["git", "--version"]
```

### `u200.M3_no_reread`

ensure_full_history: trust the fetch and skip reading the clone again, so a failed fetch passes

- File: `scripts/cloud_battery.py`
- Source: `u200.json`, row `M3_no_reread`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_remote_that_cannot_serve_the_history_refuses_baseline_and_compare`

Old text:

```
    after = _shallow(root)
```

New text:

```
    after = "false"
```

### `u268.W11_error_count_singular_only`

read_report: read only the singular error count, so a run with two errors is refused

- File: `scripts/cloud_battery.py`
- Source: `u268.json`, row `W11_error_count_singular_only`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_report_that_agrees_with_the_summary_line_is_read[plural]`

Old text:

```
        "error": _summary_count(summary, "errors?"),
```

New text:

```
        "error": _summary_count(summary, "error"),
```

### `u268.W1_id_cut_at_space`

read_report: keep each id up to its first space, as the summary line reader did, so a sibling's failure reads as the machine's

- File: `scripts/cloud_battery.py`
- Source: `u268.json`, row `W1_id_cut_at_space`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 58 against a baseline of 58
- Kills: 7 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_report_that_agrees_with_the_summary_line_is_read[plural]`
  - `tests/test_cloud_battery.py::test_a_report_that_agrees_with_the_summary_line_is_read[singular]`
  - `tests/test_cloud_battery.py::test_compare_reads_each_failure_by_its_whole_id[after-a-space]`
  - `tests/test_cloud_battery.py::test_compare_reads_each_failure_by_its_whole_id[an-error]`
  - `tests/test_cloud_battery.py::test_compare_reads_each_failure_by_its_whole_id[the-same-failures]`
  - `tests/test_cloud_battery.py::test_compare_reads_each_failure_by_its_whole_id[the-summary-separator]`
  - `tests/test_cloud_battery.py::test_each_run_records_every_key_the_driver_reads`

Old text:

```
            ids.add(nodeid)
```

New text:

```
            ids.add(nodeid.split(" ")[0])
```

### `u268.W2_errors_not_read`

PLUGIN_SOURCE: read only the failed category, so an erroring test is never listed

- File: `scripts/cloud_battery.py`
- Source: `u268.json`, row `W2_errors_not_read`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 58 against a baseline of 58
- Kills: 18 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_baseline_header_names_its_place_and_lists_its_tests_on_disk`
  - `tests/test_cloud_battery.py::test_a_change_to_the_tree_marks_the_run_unclean[before]`
  - `tests/test_cloud_battery.py::test_a_change_to_the_tree_marks_the_run_unclean[during]`
  - `tests/test_cloud_battery.py::test_a_change_to_the_tree_marks_the_run_unclean[hidden]`
  - `tests/test_cloud_battery.py::test_a_commit_made_during_the_run_is_never_recorded_as_measured`
  - `tests/test_cloud_battery.py::test_a_failure_that_moved_between_workers_is_read_by_its_id`
  - `tests/test_cloud_battery.py::test_a_file_that_cannot_be_collected_is_read_by_its_path`
  - `tests/test_cloud_battery.py::test_a_skip_an_unrun_xfail_and_a_setup_error_each_count_as_run[serial]`
  - `tests/test_cloud_battery.py::test_a_skip_an_unrun_xfail_and_a_setup_error_each_count_as_run[workers]`
  - `tests/test_cloud_battery.py::test_compare_reads_each_failure_by_its_whole_id[after-a-space]`
  - `tests/test_cloud_battery.py::test_compare_reads_each_failure_by_its_whole_id[an-error]`
  - `tests/test_cloud_battery.py::test_compare_reads_each_failure_by_its_whole_id[the-same-failures]`
  - `tests/test_cloud_battery.py::test_compare_reads_each_failure_by_its_whole_id[the-summary-separator]`
  - `tests/test_cloud_battery.py::test_each_run_records_every_key_the_driver_reads`
  - `tests/test_cloud_battery.py::test_in_memory_the_whole_suite_runs_there_and_the_listed_tests_again_on_disk`
  - ... and 3 more, see the JSON sidecar

Old text:

```
    for category in ("failed", "error"):
        reports = terminalreporter.stats.get(category, [])
```

New text:

```
    for category in ("failed",):
        reports = terminalreporter.stats.get(category, [])
```

### `u268.W3_no_report_read_as_clean`

failing_ids: drop the refusal of a run that wrote no report

- File: `scripts/cloud_battery.py`
- Source: `u268.json`, row `W3_no_report_read_as_clean`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_run_that_wrote_no_report_is_refused`

Old text:

```
        if not report_path.is_file():
            print(result.stdout[-3000:])
```

New text:

```
        if False:
            print(result.stdout[-3000:])
```

### `u268.W4_counts_not_checked`

read_report: drop the check of the report's counts against the summary line

- File: `scripts/cloud_battery.py`
- Source: `u268.json`, row `W4_counts_not_checked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_report_that_cannot_be_read_whole_is_refused[an-error-the-summary-never-counted]`

Old text:

```
        if not isinstance(entry, dict) or entry.get("counted") != count:
```

New text:

```
        if not isinstance(entry, dict):
```

### `u268.W5_listed_not_checked`

read_report: drop the check that the report lists as many ids as it counts

- File: `scripts/cloud_battery.py`
- Source: `u268.json`, row `W5_listed_not_checked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_report_that_cannot_be_read_whole_is_refused[counted-but-not-listed]`

Old text:

```
        if not isinstance(listed, list) or len(listed) < count:
```

New text:

```
        if not isinstance(listed, list):
```

### `u268.W6_id_with_line_break_stored`

read_report: store an id holding a line break, which the file would split in two

- File: `scripts/cloud_battery.py`
- Source: `u268.json`, row `W6_id_with_line_break_stored`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 58 against a baseline of 58
- Kills: 4 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_report_that_cannot_be_read_whole_is_refused[a-carriage-return]`
  - `tests/test_cloud_battery.py::test_a_report_that_cannot_be_read_whole_is_refused[a-line-break]`
  - `tests/test_cloud_battery.py::test_a_report_that_cannot_be_read_whole_is_refused[a-line-separator]`
  - `tests/test_cloud_battery.py::test_a_report_that_cannot_be_read_whole_is_refused[a-vertical-tab]`

Old text:

```
                or nodeid.splitlines() != [nodeid]

```

New text:

```
(empty)
```

### `u271-measured.B1_run_cleanliness_at_the_end_only`

measured_tree: read cleanliness after the run only, so a change made before it and a moved HEAD are missed

- File: `scripts/cloud_battery.py`
- Source: `u271-measured.json`, row `B1_run_cleanliness_at_the_end_only`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_commit_made_during_the_run_is_never_recorded_as_measured`

Old text:

```
    clean = before.clean and after.clean and before.commit == after.commit
```

New text:

```
    clean = after.clean
```

### `u271-measured.B2_commit_read_after_the_run`

measured_tree: name the commit read after the run, as last-compare.txt did before U271

- File: `scripts/cloud_battery.py`
- Source: `u271-measured.json`, row `B2_commit_read_after_the_run`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_commit_made_during_the_run_is_never_recorded_as_measured`

Old text:

```
    return TreeState(commit=before.commit, clean=clean)
```

New text:

```
    return TreeState(commit=after.commit, clean=clean)
```

### `u271-measured.B3_status_unread`

tree_state in the battery: read only git's exit, so a tree with changes reads clean

- File: `scripts/cloud_battery.py`
- Source: `u271-measured.json`, row `B3_status_unread`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 58 against a baseline of 58
- Kills: 3 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_change_to_the_tree_marks_the_run_unclean[before]`
  - `tests/test_cloud_battery.py::test_a_change_to_the_tree_marks_the_run_unclean[during]`
  - `tests/test_cloud_battery.py::test_a_change_to_the_tree_marks_the_run_unclean[hidden]`

Old text:

```
    clean = bool(commit) and status.returncode == 0 and not status.stdout.strip()
    return TreeState(commit=commit, clean=clean)
```

New text:

```
    clean = bool(commit) and status.returncode == 0
    return TreeState(commit=commit, clean=clean)
```

### `u271-measured.B4_release_line_never_dirty`

record_verdict: never write dirty, so the release reads a moved tree as clean

- File: `scripts/cloud_battery.py`
- Source: `u271-measured.json`, row `B4_release_line_never_dirty`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 58 against a baseline of 58
- Kills: 4 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_change_to_the_tree_marks_the_run_unclean[before]`
  - `tests/test_cloud_battery.py::test_a_change_to_the_tree_marks_the_run_unclean[during]`
  - `tests/test_cloud_battery.py::test_a_change_to_the_tree_marks_the_run_unclean[hidden]`
  - `tests/test_cloud_battery.py::test_a_commit_made_during_the_run_is_never_recorded_as_measured`

Old text:

```
    if not tree.clean:
        verdict = "dirty"
```

New text:

```
    if False:
        verdict = "dirty"
```

### `u271-measured.B5_collection_errors_unlisted`

the reporting plugin: list no collection errors

- File: `scripts/cloud_battery.py`
- Source: `u271-measured.json`, row `B5_collection_errors_unlisted`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_file_that_cannot_be_collected_is_read_by_its_path`

Old text:

```
            if getattr(report, "when", None) == "collect"
```

New text:

```
            if getattr(report, "when", None) == "never"
```

### `u271-measured.B6_count_unread_under_workers`

the reporting plugin: drop the xdist hook, so a run with workers records no collected count

- File: `scripts/cloud_battery.py`
- Source: `u271-measured.json`, row `B6_count_unread_under_workers`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 58 against a baseline of 58
- Kills: 2 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_failure_that_moved_between_workers_is_read_by_its_id`
  - `tests/test_cloud_battery.py::test_a_skip_an_unrun_xfail_and_a_setup_error_each_count_as_run[workers]`

Old text:

```
def pytest_xdist_node_collection_finished(node, ids):
    _COLLECTED["count"] = len(ids)
```

New text:

```
def pytest_xdist_node_collection_finished(node, ids):
    pass
```

### `u271-measured.B8_ran_uncounted`

the reporting plugin: count no test as having reported

- File: `scripts/cloud_battery.py`
- Source: `u271-measured.json`, row `B8_ran_uncounted`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 58 against a baseline of 58
- Kills: 4 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_baseline_header_names_its_place_and_lists_its_tests_on_disk`
  - `tests/test_cloud_battery.py::test_a_skip_an_unrun_xfail_and_a_setup_error_each_count_as_run[serial]`
  - `tests/test_cloud_battery.py::test_a_skip_an_unrun_xfail_and_a_setup_error_each_count_as_run[workers]`
  - `tests/test_cloud_battery.py::test_each_run_records_every_key_the_driver_reads`

Old text:

```
    _RAN.add(report.nodeid)
```

New text:

```
    pass
```

### `u273.P10_placeless_baseline_read`

read_baseline: read a baseline that names no place, as every one before U273

- File: `scripts/cloud_battery.py`
- Source: `u273.json`, row `P10_placeless_baseline_read`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 58 against a baseline of 58
- Kills: 3 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_baseline_without_a_field_compare_needs_is_refused_saying_why[a-filesystem]`
  - `tests/test_cloud_battery.py::test_a_baseline_without_a_field_compare_needs_is_refused_saying_why[before-u273]`
  - `tests/test_cloud_battery.py::test_a_baseline_without_a_field_compare_needs_is_refused_saying_why[unknown]`

Old text:

```
    if match.group(3) not in PLACES:
```

New text:

```
    if False:
```

### `u273.P11_other_place_compared`

cmd_compare: run a compare in the place it asks for even when the baseline was measured in the other

- File: `scripts/cloud_battery.py`
- Source: `u273.json`, row `P11_other_place_compared`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 58 against a baseline of 58
- Kills: 2 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_compare_in_the_other_place_from_its_baseline_is_refused[disk-memory]`
  - `tests/test_cloud_battery.py::test_a_compare_in_the_other_place_from_its_baseline_is_refused[memory-disk]`

Old text:

```
    if requested is not None and requested != base.place:
```

New text:

```
    if False:
```

### `u273.P13_rerun_disk_unchecked_upfront`

refusal_for: check only the run's own place, so a disk the rerun cannot have refuses after a whole run in memory

- File: `scripts/cloud_battery.py`
- Source: `u273.json`, row `P13_rerun_disk_unchecked_upfront`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_memory_run_whose_disk_rerun_cannot_be_given_is_refused_before_it_runs`

Old text:

```
    return (MEMORY, DISK) if place == MEMORY and ON_DISK else (place,)
```

New text:

```
    return (place,)
```

### `u273.P1_memory_any_filesystem`

place_root: accept any filesystem as memory, so a run named memory may be on disk

- File: `scripts/cloud_battery.py`
- Source: `u273.json`, row `P1_memory_any_filesystem`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_each_place_is_given_only_where_it_is_what_it_names`

Old text:

```
        if kind not in MEMORY_FILESYSTEMS:
            return None, f"{root} is not a memory filesystem here ({kind or 'no mount table'})"
```

New text:

```
        if False:
            return None, f"{root} is not a memory filesystem here ({kind or 'no mount table'})"
```

### `u273.P2_no_floor`

place_root: drop the free space floor, so a small /dev/shm fills partway through a run

- File: `scripts/cloud_battery.py`
- Source: `u273.json`, row `P2_no_floor`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 58 against a baseline of 58
- Kills: 2 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_place_the_machine_cannot_give_refuses_baseline_and_compare`
  - `tests/test_cloud_battery.py::test_each_place_is_given_only_where_it_is_what_it_names`

Old text:

```
        if free < MEMORY_FLOOR:
```

New text:

```
        if False:
```

### `u273.P3_disk_on_memory_accepted`

place_root: accept a disk TMPDIR that is itself on a memory filesystem

- File: `scripts/cloud_battery.py`
- Source: `u273.json`, row `P3_disk_on_memory_accepted`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 58 against a baseline of 58
- Kills: 2 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_memory_run_whose_disk_rerun_cannot_be_given_is_refused_before_it_runs`
  - `tests/test_cloud_battery.py::test_each_place_is_given_only_where_it_is_what_it_names`

Old text:

```
        if kind in MEMORY_FILESYSTEMS:
            return None, (
```

New text:

```
        if False:
            return None, (
```

### `u273.P4_mount_first_match`

filesystem_of: take every mount point holding the path rather than the longest

- File: `scripts/cloud_battery.py`
- Source: `u273.json`, row `P4_mount_first_match`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_mount_table_is_read_by_its_longest_mount_point`

Old text:

```
        if inside and len(point) >= len(best):
```

New text:

```
        if inside:
```

### `u273.P5_tmpdir_not_set`

_run_suite: do not point the run's TMPDIR at its place, so it inherits the caller's

- File: `scripts/cloud_battery.py`
- Source: `u273.json`, row `P5_tmpdir_not_set`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 58 against a baseline of 58
- Kills: 7 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_baseline_header_names_its_place_and_lists_its_tests_on_disk`
  - `tests/test_cloud_battery.py::test_a_file_that_cannot_be_collected_is_read_by_its_path`
  - `tests/test_cloud_battery.py::test_a_skip_an_unrun_xfail_and_a_setup_error_each_count_as_run[serial]`
  - `tests/test_cloud_battery.py::test_a_skip_an_unrun_xfail_and_a_setup_error_each_count_as_run[workers]`
  - `tests/test_cloud_battery.py::test_in_memory_the_whole_suite_runs_there_and_the_listed_tests_again_on_disk`
  - `tests/test_cloud_battery.py::test_the_disk_run_stands_only_for_the_tests_listed[an-unlisted-test-failing-in-memory]`
  - `tests/test_cloud_battery.py::test_the_suite_command_leaves_the_distribution_to_addopts`

Old text:

```
        env["TMPDIR"] = str(temp)

```

New text:

```
(empty)
```

### `u273.P6_no_rerun_on_disk`

failing_ids: never run the listed tests again on disk after a run in memory

- File: `scripts/cloud_battery.py`
- Source: `u273.json`, row `P6_no_rerun_on_disk`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 58 against a baseline of 58
- Kills: 5 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_baseline_header_names_its_place_and_lists_its_tests_on_disk`
  - `tests/test_cloud_battery.py::test_an_on_disk_run_that_did_not_run_a_listed_test_is_refused[not-collected]`
  - `tests/test_cloud_battery.py::test_an_on_disk_run_that_did_not_run_a_listed_test_is_refused[skipped-on-disk]`
  - `tests/test_cloud_battery.py::test_in_memory_the_whole_suite_runs_there_and_the_listed_tests_again_on_disk`
  - `tests/test_cloud_battery.py::test_the_disk_run_stands_only_for_the_tests_listed[a-listed-test-failing-on-disk]`

Old text:

```
    listed = tuple(ON_DISK) if place == MEMORY else ()
```

New text:

```
    listed = ()
```

### `u273.P8_disk_run_unchecked`

failing_ids: accept an on disk run that skipped or never collected a listed test

- File: `scripts/cloud_battery.py`
- Source: `u273.json`, row `P8_disk_run_unchecked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_an_on_disk_run_that_did_not_run_a_listed_test_is_refused[skipped-on-disk]`

Old text:

```
    if unread or stray:
```

New text:

```
    if False:
```

### `u313.C1_history_refusal_ignored`

_checked_run: print the history refusal and go on, so a shallow clone is measured and its known failures subtracted

- File: `scripts/cloud_battery.py`
- Source: `u313.json`, row `C1_history_refusal_ignored`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_remote_that_cannot_serve_the_history_refuses_baseline_and_compare`

Old text:

```
        print(f"history: REFUSED, {reason}")
        return None
```

New text:

```
        print(f"history: REFUSED, {reason}")
```

### `u313.C3_tree_read_once`

_checked_run: read the tree after the run only, so a change made during the suite reads as clean

- File: `scripts/cloud_battery.py`
- Source: `u313.json`, row `C3_tree_read_once`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_commit_made_during_the_run_is_never_recorded_as_measured`

Old text:

```
    return at, measured, measured_tree(before, tree_state())
```

New text:

```
    return at, measured, measured_tree(tree_state(), tree_state())
```

### `u297.K1_a_zero_row_counted_as_a_kill`

killed: count a row with zero deaths as killed, so the kill set holds rows no test ever killed

- File: `scripts/killset.py`
- Source: `u297.json`, row `K1_a_zero_row_counted_as_a_kill`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_killset.py`
- Collected: 77 against a baseline of 77
- Kills: 6 (killed)
- Killed:
  - `tests/test_killset.py::test_a_row_is_live_stale_ambiguous_or_gone_by_what_the_tree_holds`
  - `tests/test_killset.py::test_a_row_that_broke_collection_before_is_held_to_no_less_after`
  - `tests/test_killset.py::test_a_table_of_the_older_form_is_read_by_its_deaths`
  - `tests/test_killset.py::test_check_passes_when_every_kill_is_kept`
  - `tests/test_killset.py::test_list_prints_the_counts_and_one_line_a_file`
  - `tests/test_killset.py::test_rows_after_leaves_text_it_cannot_place_for_the_author`

Old text:

```
    return isinstance(deaths, int) and not isinstance(deaths, bool) and deaths > 0
```

New text:

```
    return isinstance(deaths, int) and not isinstance(deaths, bool) and deaths >= 0
```

### `u297.K2_a_lost_kill_passes_check`

compare_tables: stop reading a row that is weaker after than before as lost, so check passes a refactor that lost a kill

- File: `scripts/killset.py`
- Source: `u297.json`, row `K2_a_lost_kill_passes_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_killset.py`
- Collected: 77 against a baseline of 77
- Kills: 6 (killed)
- Killed:
  - `tests/test_killset.py::test_a_kill_that_became_a_collection_error_is_lost_though_it_records_a_death`
  - `tests/test_killset.py::test_a_row_that_broke_collection_before_is_held_to_no_less_after`
  - `tests/test_killset.py::test_a_table_of_the_older_form_is_read_by_its_deaths`
  - `tests/test_killset.py::test_check_fails_on_one_lost_kill_and_names_it`
  - `tests/test_killset.py::test_check_matches_tables_that_are_not_replays_by_row_id`
  - `tests/test_killset.py::test_recorded_kills_replay_through_the_driver_and_check_clean`

Old text:

```
            if strength(now) < held:
```

New text:

```
            if False:
```

### `u297.K3_mapped_to_a_row_that_is_not_killed`

compare_tables: accept a mapping whose target row is weaker after than the kill it covers

- File: `scripts/killset.py`
- Source: `u297.json`, row `K3_mapped_to_a_row_that_is_not_killed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_killset.py`
- Collected: 77 against a baseline of 77
- Kills: 2 (killed)
- Killed:
  - `tests/test_killset.py::test_a_mapping_onto_a_row_that_only_broke_collection_does_not_cover_a_kill`
  - `tests/test_killset.py::test_check_fails_a_row_mapped_to_a_row_that_is_not_killed`

Old text:

```
        elif strength(target) < held:
```

New text:

```
        elif False:
```

### `u297.K4_a_collection_error_counts_as_a_kill`

strength: rank a row that broke collection with a death as high as a clean kill, so a kill that became one is kept

- File: `scripts/killset.py`
- Source: `u297.json`, row `K4_a_collection_error_counts_as_a_kill`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_killset.py`
- Collected: 77 against a baseline of 77
- Kills: 3 (killed)
- Killed:
  - `tests/test_killset.py::test_a_kill_that_became_a_collection_error_is_lost_though_it_records_a_death`
  - `tests/test_killset.py::test_a_mapping_onto_a_row_that_only_broke_collection_does_not_cover_a_kill`
  - `tests/test_killset.py::test_a_row_that_broke_collection_before_is_held_to_no_less_after`

Old text:

```
    return 2 if row.get("status") in (None, "killed") else 1
```

New text:

```
    return 2
```

### `u297.K5_any_reason_vouches_for_a_move`

unvouched_move: accept the reason rows --after wrote with no test in common, so a row killed at another guard's line passes check

- File: `scripts/killset.py`
- Source: `u297.json`, row `K5_any_reason_vouches_for_a_move`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_killset.py`
- Collected: 77 against a baseline of 77
- Kills: 3 (killed)
- Killed:
  - `tests/test_killset.py::test_a_line_written_new_elsewhere_reads_as_a_move_and_check_is_what_catches_it`
  - `tests/test_killset.py::test_a_replay_at_another_guards_line_does_not_bring_a_dead_row_back`
  - `tests/test_killset.py::test_a_row_the_tool_moved_must_still_die_by_a_test_that_killed_it_before`

Old text:

```
    if killers_before & now or not reason.startswith(AUTOMATIC_MOVE):
```

New text:

```
    if reason:
```

### `u297.K6_a_twin_read_as_a_move`

moved_to: place a row at the one file that holds its text now though the text stood in two places at the measured commit

- File: `scripts/killset.py`
- Source: `u297.json`, row `K6_a_twin_read_as_a_move`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_killset.py`
- Collected: 77 against a baseline of 77
- Kills: 3 (killed)
- Killed:
  - `tests/test_killset.py::test_a_deleted_guard_is_not_anchored_on_its_twin_wherever_the_twin_is_now[_twin_is_renamed]`
  - `tests/test_killset.py::test_a_deleted_guard_is_not_anchored_on_its_twin_wherever_the_twin_is_now[_twin_is_split]`
  - `tests/test_killset.py::test_a_deleted_guard_is_not_anchored_on_its_twin_wherever_the_twin_is_now[_twin_stays]`

Old text:

```
    if stood != 1:
```

New text:

```
    if False:
```

### `u297.K7_a_batch_in_progress_read_as_finished`

read_measured: read a table still in progress as a finished batch, so its unmeasured rows are compared as if measured

- File: `scripts/killset.py`
- Source: `u297.json`, row `K7_a_batch_in_progress_read_as_finished`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_killset.py`
- Collected: 77 against a baseline of 77
- Kills: 1 (killed)
- Killed:
  - `tests/test_killset.py::test_check_refuses_a_table_that_is_not_a_finished_valid_batch[extra1-in progress]`

Old text:

```
    if table.get("valid") is not True or table.get("invalid_reason"):
```

New text:

```
    if table.get("valid") is not True:
```

### `u297.D4_a_measured_row_loses_its_source`

measure_row: stop carrying a replay row's source and moved reason into its result, so check has nothing to match the row by

- File: `scripts/mutate.py`
- Source: `u297.json`, row `D4_a_measured_row_loses_its_source`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_killset.py`
- Collected: 77 against a baseline of 77
- Kills: 1 (killed)
- Killed:
  - `tests/test_killset.py::test_recorded_kills_replay_through_the_driver_and_check_clean`

Old text:

```
        head_verified=head_verify,
        **replay_fields(row),
    )
```

New text:

```
        head_verified=head_verify,
    )
```

### `u296.M10_type_checking_reads_as_running`

Tree._read_file: read an import under TYPE_CHECKING as one that runs, so a typing only import fails rule three

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M10_type_checking_reads_as_running`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`
- Collected: 57 against a baseline of 57
- Kills: 4 (killed)
- Killed:
  - `tests/test_import_rules.py::test_an_import_under_type_checking_is_never_loaded_for_a_verb`
  - `tests/test_import_rules.py::test_an_import_under_type_checking_never_runs_and_passes`
  - `tests/test_import_rules.py::test_no_package_crosses_a_seam_beyond_its_allowance`
  - `tests/test_import_rules.py::test_type_checking_spelled_through_its_module_is_read_the_same`

Old text:

```
            typing_only = inside(node.lineno, typing_blocks)
```

New text:

```
            typing_only = False
```

### `u296.M11_builder_imports_unread`

dangling: do not read the imports written in a verb's builder, so intake.set's shape builds on paper and dangles in fact

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M11_builder_imports_unread`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`
- Collected: 57 against a baseline of 57
- Kills: 2 (killed)
- Killed:
  - `tests/test_import_rules.py::test_a_home_imported_directly_in_the_builder_dangles_the_verb`
  - `tests/test_import_rules.py::test_an_import_written_in_the_builder_runs_when_the_verb_builds_and_dangles`

Old text:

```
            built = tree.function_loads(verb.module, verb.builder)
```

New text:

```
            built = frozenset()
```

### `u296.M12_followed_through_a_blocked_module`

Tree.loaded_from: follow imports through a module that cannot be imported, so an import nothing reaches is named as a cause

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M12_followed_through_a_blocked_module`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                if module in seen or within(module, blocked):
```

New text:

```
                if module in seen:
```

### `u296.M13_own_verbs_dangle`

dangling: count the switched off toggle's own verbs, so every gated verb reads as dangling

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M13_own_verbs_dangle`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`
- Collected: 57 against a baseline of 57
- Kills: 2 (killed)
- Killed:
  - `tests/test_import_rules.py::test_no_package_crosses_a_seam_beyond_its_allowance`
  - `tests/test_import_rules.py::test_the_toggles_own_verbs_are_off_and_so_never_dangle`

Old text:

```
            if verb.toggle == toggle:
                continue
```

New text:

```
            if verb.toggle == "":
                continue
```

### `u296.M14_core_names_everywhere`

core_names: count the names core, write and the shell use too, so the ceiling measures something else

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M14_core_names_everywhere`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`
- Collected: 57 against a baseline of 57
- Kills: 3 (killed)
- Killed:
  - `tests/test_import_rules.py::test_a_name_a_listed_module_re_exports_is_reached_through_the_list`
  - `tests/test_import_rules.py::test_core_names_are_counted_across_feature_packages_and_only_there`
  - `tests/test_import_rules.py::test_no_package_crosses_a_seam_beyond_its_allowance`

Old text:

```
    out: dict[str, set[str]] = collections.defaultdict(set)
    for path, uses in tree.uses.items():
        importer = package_of_path(path)
        if importer in LOWER_PACKAGES:
            continue
        for use in uses:
            if use.name is not None and (use.target == core or use.target.startswith(core + ".")):
```

New text:

```
    out: dict[str, set[str]] = collections.defaultdict(set)
    for path, uses in tree.uses.items():
        importer = package_of_path(path)
        for use in uses:
            if use.name is not None and (use.target == core or use.target.startswith(core + ".")):
```

### `u296.M15_shadowed_alias_counts`

Tree.uses: count a name reached through a module whether or not the module defines it, so a local variable named as an imported module is reads as a use

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M15_shadowed_alias_counts`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_import_rules.py::test_a_local_variable_named_as_an_imported_module_is_not_a_use_of_it`

Old text:

```
                or use.name in defined[use.target]
```

New text:

```
                or use.name is not None
```

### `u296.M16_prune_adds_lines`

pruned: keep what is found or allowed, so prune writes newly found lines into an allowance

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M16_prune_adds_lines`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_duplication.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_duplication.py::test_pruning_keeps_what_is_still_found_and_can_never_add_a_line`

Old text:

```
    return found & allowed
```

New text:

```
    return found | allowed
```

### `u296.M18_vendored_tree_read`

python_files: read the vendored tree, which is never refactored and never measured

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M18_vendored_tree_read`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_duplication.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_duplication.py::test_no_package_holds_a_copied_block_beyond_its_allowance`

Old text:

```
        and f"/{VENDOR}/" not in f"/{path}"
```

New text:

```
        and f"/{VENDOR}x/" not in f"/{path}"
```

### `u296.M1_block_size`

BLOCK_LINES: a block needs seven logical lines, so a new copy of exactly six passes the duplication check

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M1_block_size`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_duplication.py`
- Collected: 31 against a baseline of 31
- Kills: 11 (killed)
- Killed:
  - `tests/test_duplication.py::test_a_block_on_the_allowance_passes_and_a_new_one_beside_it_fails`
  - `tests/test_duplication.py::test_a_copy_inside_one_file_is_found`
  - `tests/test_duplication.py::test_a_copy_of_six_lines_is_found_in_both_packages`
  - `tests/test_duplication.py::test_a_copy_that_was_only_reindented_recommented_and_rewrapped_is_still_found`
  - `tests/test_duplication.py::test_a_deletion_that_brings_two_stretches_together_is_a_new_copy`
  - `tests/test_duplication.py::test_a_longer_copy_is_its_run_of_windows`
  - `tests/test_duplication.py::test_a_third_copy_of_an_allowed_block_in_the_same_package_fails`
  - `tests/test_duplication.py::test_a_window_is_described_by_where_it_stands`
  - `tests/test_duplication.py::test_an_allowance_is_its_own_packages_and_excuses_no_other`
  - `tests/test_duplication.py::test_overlapping_windows_in_one_file_are_two_places`
  - `tests/test_duplication.py::test_the_block_size_is_six_logical_lines`

Old text:

```
BLOCK_LINES = 6
```

New text:

```
BLOCK_LINES = 7
```

### `u296.M22_initializer_relative_import`

Tree._base_of: resolve a relative import in a package initializer as in any other module, one package too high, so a crossing written there is read against the wrong module (the review's row 7)

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M22_initializer_relative_import`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_import_rules.py::test_a_relative_import_in_a_package_initializer_starts_from_that_package`

Old text:

```
        if not path.endswith("/__init__.py"):
            parts = parts[:-1]
```

New text:

```
        parts = parts[:-1]
```

### `u296.M23_except_branch_names_unread`

_defined_names: do not read the names bound in except branches, so a name defined there is taken for a local variable's attribute and dropped (the review's row 7)

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M23_except_branch_names_unread`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_import_rules.py::test_a_name_bound_in_an_except_branch_is_a_name_the_module_defines`

Old text:

```
            pending.extend(
                inner for handler in getattr(node, "handlers", ()) for inner in handler.body
            )
```

New text:

```
            pass
```

### `u296.M24_builder_names_a_home_directly`

dangling: forget the homes a builder imports directly, so only what its other imports reach can dangle the verb (the review's row 7)

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M24_builder_names_a_home_directly`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_import_rules.py::test_a_home_imported_directly_in_the_builder_dangles_the_verb`

Old text:

```
            crossing = {(verb.module, target) for target in built if within(target, owned)}
```

New text:

```
            crossing = set()
```

### `u296.M25_dotted_import_alias`

Tree._read_file: bind an import under another name to the root package, so a private name reached through it passes (the review's row 7)

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M25_dotted_import_alias`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_import_rules.py::test_a_dotted_import_under_another_name_is_followed_to_its_module`

Old text:

```
                    aliases[alias.asname or top] = alias.name if alias.asname else top
```

New text:

```
                    aliases[alias.asname or top] = top
```

### `u296.M26_core_package_name`

core_names: count names of core's modules only, so a name imported from the core package itself is not a core name (the review's row 7)

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M26_core_package_name`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_import_rules.py::test_a_name_imported_from_the_core_package_itself_is_a_core_name`

Old text:

```
            if use.name is not None and (use.target == core or use.target.startswith(core + ".")):
                out[importer].add(use.dotted)
```

New text:

```
            if use.name is not None and use.target.startswith(core + "."):
                out[importer].add(use.dotted)
```

### `u296.M2_imports_count_as_lines`

logical_lines: stop dropping import statements, so two module headers read as a copied block

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M2_imports_count_as_lines`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_duplication.py`
- Collected: 31 against a baseline of 31
- Kills: 3 (killed)
- Killed:
  - `tests/test_duplication.py::test_comments_blank_lines_docstrings_and_imports_are_not_logical_lines`
  - `tests/test_duplication.py::test_imports_do_not_count_toward_the_six_lines`
  - `tests/test_duplication.py::test_no_package_holds_a_copied_block_beyond_its_allowance`

Old text:

```
                an_import = first.type == tokenize.NAME and first.string in ("import", "from")
```

New text:

```
                an_import = False
```

### `u296.M3_allowance_forgets_places`

over_allowance: compare which lines are held and not how many places hold each, so a third copy of an allowed block passes

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M3_allowance_forgets_places`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_duplication.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_duplication.py::test_a_third_copy_of_an_allowed_block_in_the_same_package_fails`

Old text:

```
        excess = counts - allowed.get(package, collections.Counter())
```

New text:

```
        excess = collections.Counter(set(counts) - set(allowed.get(package, ())))
```

### `u296.M4_allowance_shared_between_packages`

over_allowance: read every package against one merged allowance, so a block allowed in one package is allowed in all

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M4_allowance_shared_between_packages`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_duplication.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_duplication.py::test_an_allowance_is_its_own_packages_and_excuses_no_other`

Old text:

```
    for package, counts in found.items():
        excess = counts - allowed.get(package, collections.Counter())
```

New text:

```
    for package, counts in found.items():
        excess = counts - sum(allowed.values(), collections.Counter())
```

### `u296.M5_private_inside_its_package`

private_crossings: drop the comparison of packages, so a private name used inside its own package is a crossing

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M5_private_inside_its_package`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`
- Collected: 57 against a baseline of 57
- Kills: 3 (killed)
- Killed:
  - `tests/test_import_rules.py::test_a_relative_import_in_a_package_initializer_starts_from_that_package`
  - `tests/test_import_rules.py::test_no_package_crosses_a_seam_beyond_its_allowance`
  - `tests/test_import_rules.py::test_the_same_private_import_inside_its_own_package_passes`

Old text:

```
            if private and tree.package(use.target) != importer:
```

New text:

```
            if private:
```

### `u296.M6_private_through_a_module`

private_crossings: read the private rule off import statements only, so a private name reached through an imported module passes

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M6_private_through_a_module`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`
- Collected: 57 against a baseline of 57
- Kills: 3 (killed)
- Killed:
  - `tests/test_import_rules.py::test_a_dotted_import_under_another_name_is_followed_to_its_module`
  - `tests/test_import_rules.py::test_a_private_name_of_a_module_handed_over_is_still_a_crossing`
  - `tests/test_import_rules.py::test_a_private_name_reached_through_an_imported_module_fails`

Old text:

```
        for use in uses:
            parts = use.target.split(".")[1:]
            if VENDOR in parts:
```

New text:

```
        for use in uses:
            parts = use.target.split(".")[1:]
            if VENDOR in parts or use.kind != "import":
```

### `u296.M7_interface_binds_the_lower_layers`

core_modules_reached: stop exempting core, write and the shell, so the interface list binds packages it was never for

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M7_interface_binds_the_lower_layers`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`
- Collected: 57 against a baseline of 57
- Kills: 7 (killed)
- Killed:
  - `tests/test_import_rules.py::test_a_function_that_imports_its_module_when_called_is_not_that_module`
  - `tests/test_import_rules.py::test_a_module_handed_over_by_a_listed_one_is_a_reach_of_that_module`
  - `tests/test_import_rules.py::test_a_module_handed_over_twice_is_followed_to_the_module_it_is`
  - `tests/test_import_rules.py::test_a_module_passed_on_by_name_through_a_third_module_is_followed_to_it`
  - `tests/test_import_rules.py::test_a_name_a_listed_module_re_exports_is_reached_through_the_list`
  - `tests/test_import_rules.py::test_no_package_crosses_a_seam_beyond_its_allowance`
  - `tests/test_import_rules.py::test_the_same_import_passes_from_core_write_and_the_shell`

Old text:

```
    core = f"{tree.root_package}.core"
    for path, uses in tree.uses.items():
        importer = package_of_path(path)
        if importer in LOWER_PACKAGES:
            continue
        for use in uses:
            if use.target.startswith(core + "."):
```

New text:

```
    core = f"{tree.root_package}.core"
    for path, uses in tree.uses.items():
        importer = package_of_path(path)
        for use in uses:
            if use.target.startswith(core + "."):
```

### `u296.M8_interface_list_ignored`

off_interface: treat every core module as off the list, so the named interface allows nothing

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M8_interface_list_ignored`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`
- Collected: 57 against a baseline of 57
- Kills: 9 (killed)
- Killed:
  - `tests/test_import_rules.py::test_a_core_module_off_the_list_fails_from_a_feature_package`
  - `tests/test_import_rules.py::test_a_function_that_imports_its_module_when_called_is_not_that_module`
  - `tests/test_import_rules.py::test_a_module_handed_over_by_a_listed_one_is_a_reach_of_that_module`
  - `tests/test_import_rules.py::test_a_module_handed_over_twice_is_followed_to_the_module_it_is`
  - `tests/test_import_rules.py::test_a_module_on_the_list_passes_from_a_feature_package`
  - `tests/test_import_rules.py::test_a_module_passed_on_by_name_through_a_third_module_is_followed_to_it`
  - `tests/test_import_rules.py::test_a_name_a_listed_module_re_exports_is_reached_through_the_list`
  - `tests/test_import_rules.py::test_no_package_crosses_a_seam_beyond_its_allowance`
  - `tests/test_import_rules.py::test_the_module_an_import_names_is_still_reached_when_the_name_is_a_module`

Old text:

```
        if module in named:
            continue
```

New text:

```
        if module in ():
            continue
```

### `u296.M9_lazy_reads_as_top_level`

Tree._read_file: read every import as top level, so an import under a function fails rule three and dangles a verb

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M9_lazy_reads_as_top_level`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`
- Collected: 57 against a baseline of 57
- Kills: 5 (killed)
- Killed:
  - `tests/test_import_rules.py::test_a_function_that_imports_its_module_when_called_is_not_that_module`
  - `tests/test_import_rules.py::test_an_import_under_a_function_does_not_dangle_a_verb`
  - `tests/test_import_rules.py::test_an_import_written_in_the_builder_runs_when_the_verb_builds_and_dangles`
  - `tests/test_import_rules.py::test_no_package_crosses_a_seam_beyond_its_allowance`
  - `tests/test_import_rules.py::test_the_same_import_under_a_function_passes`

Old text:

```
            lazy = inside(node.lineno, functions)
```

New text:

```
            lazy = False
```

### `u328.R1_starred_name_not_followed`

verbs_from: never follow a starred name into its part, so the split table's parts are not read

- File: `scripts/refactor_measure.py`
- Source: `u328.json`, row `R1_starred_name_not_followed`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`
- Collected: 57 against a baseline of 57
- Kills: 2 (killed)
- Killed:
  - `tests/test_import_rules.py::test_a_starred_name_is_followed_into_the_part_that_holds_its_tuple`
  - `tests/test_import_rules.py::test_the_script_reads_the_registry_as_the_package_declares_it`

Old text:

```
            starred = isinstance(member, ast.Starred) and isinstance(member.value, ast.Name)
```

New text:

```
            starred = False
```

### `u328.R2_missing_part_read_as_empty`

verbs_from: a starred name no source holds yields nothing instead of raising, so a part the loader missed reads as no verbs

- File: `scripts/refactor_measure.py`
- Source: `u328.json`, row `R2_missing_part_read_as_empty`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_import_rules.py::test_a_starred_name_is_followed_into_the_part_that_holds_its_tuple`

Old text:

```
            raise ValueError(f"the registry holds no {name} tuple")
```

New text:

```
            return
```

### `u328.R3_starred_attribute_crashes`

verbs_from: follow any starred member, so a starred attribute crashes on its missing id instead of being refused as unreadable

- File: `scripts/refactor_measure.py`
- Source: `u328.json`, row `R3_starred_attribute_crashes`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_import_rules.py::test_a_starred_name_is_followed_into_the_part_that_holds_its_tuple`

Old text:

```
            starred = isinstance(member, ast.Starred) and isinstance(member.value, ast.Name)
```

New text:

```
            starred = isinstance(member, ast.Starred)
```

### `u328.R4_loader_reads_the_registry_alone`

_load: hand verbs_from the registry's own file and none of its parts

- File: `scripts/refactor_measure.py`
- Source: `u328.json`, row `R4_loader_reads_the_registry_alone`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_import_rules.py::test_the_script_reads_the_registry_as_the_package_declares_it`

Old text:

```
    verbs = verbs_from(*(text for path, text in sources.items() if path.startswith(table)))
```

New text:

```
    verbs = verbs_from(*(text for path, text in sources.items() if path == REGISTRY))
```

### `u331.M01_use_as_written_dropped`

Tree._followed: drop the use as written, so a name that is a module reads only as the module it leads to, and an off interface import, a top level import of a toggleable package and a private name each read clean

- File: `scripts/refactor_measure.py`
- Source: `u331.json`, row `M01_use_as_written_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`
- Collected: 57 against a baseline of 57
- Kills: 34 (killed)
- Killed:
  - `tests/test_import_rules.py::test_a_core_module_off_the_list_fails_from_a_feature_package`
  - `tests/test_import_rules.py::test_a_core_verb_whose_module_imports_a_toggled_off_package_dangles`
  - `tests/test_import_rules.py::test_a_dotted_import_under_another_name_is_followed_to_its_module`
  - `tests/test_import_rules.py::test_a_function_that_imports_its_module_when_called_is_not_that_module`
  - `tests/test_import_rules.py::test_a_home_imported_directly_in_the_builder_dangles_the_verb`
  - `tests/test_import_rules.py::test_a_lazy_private_import_across_packages_still_fails`
  - `tests/test_import_rules.py::test_a_lazy_reach_off_the_list_still_fails`
  - `tests/test_import_rules.py::test_a_local_variable_named_as_an_imported_module_is_not_a_use_of_it`
  - `tests/test_import_rules.py::test_a_module_handed_over_by_a_listed_one_is_a_reach_of_that_module`
  - `tests/test_import_rules.py::test_a_module_handed_over_twice_is_followed_to_the_module_it_is`
  - `tests/test_import_rules.py::test_a_module_that_answers_for_any_name_has_every_attribute_counted`
  - `tests/test_import_rules.py::test_a_name_a_listed_module_re_exports_is_reached_through_the_list`
  - `tests/test_import_rules.py::test_a_name_bound_in_an_except_branch_is_a_name_the_module_defines`
  - `tests/test_import_rules.py::test_a_name_imported_from_the_core_package_itself_is_a_core_name`
  - `tests/test_import_rules.py::test_a_package_initializer_is_loaded_with_any_module_inside_it`
  - ... and 19 more, see the JSON sidecar

Old text:

```
            # The use as written stands: the module it names was reached too.
            out.append(use)

```

New text:

```
            # The use as written stands: the module it names was reached too.

```

### `u331.M03_lazy_from_import_hands_a_name`

Tree._parse: a from import inside a function counts as a top level binding, so a name imported at call time is followed as if the module handed it over

- File: `scripts/refactor_measure.py`
- Source: `u331.json`, row `M03_lazy_from_import_hands_a_name`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_import_rules.py::test_a_function_that_imports_its_module_when_called_is_not_that_module`

Old text:

```
                at_top = not lazy and not typing_only
```

New text:

```
                at_top = not typing_only
```

### `u331.M04_one_hop_only`

Tree._handed: follow a handed name through one module only, so a module passed on through a third module is not followed

- File: `scripts/refactor_measure.py`
- Source: `u331.json`, row `M04_one_hop_only`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_import_rules.py::test_a_module_passed_on_by_name_through_a_third_module_is_followed_to_it`

Old text:

```
        while name is not None and (module, name) not in seen:
```

New text:

```
        if name is not None and (module, name) not in seen:
```

### `u331.M05_chains_off_an_imported_name_unread`

Tree._parse: read no attribute chain off a name imported from a module, so tags.art.read after from cratekit.core import tags is never followed to art

- File: `scripts/refactor_measure.py`
- Source: `u331.json`, row `M05_chains_off_an_imported_name_unread`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_import_rules.py::test_a_module_handed_over_by_a_listed_one_is_a_reach_of_that_module`

Old text:

```
            if current.id in named and current.id not in aliases:
```

New text:

```
            if False:
```

### `u331.M06_attribute_use_not_followed`

Tree._followed: an attribute use that names a module is kept as written and not followed into it

- File: `scripts/refactor_measure.py`
- Source: `u331.json`, row `M06_attribute_use_not_followed`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`
- Collected: 57 against a baseline of 57
- Kills: 2 (killed)
- Killed:
  - `tests/test_import_rules.py::test_a_module_handed_over_by_a_listed_one_is_a_reach_of_that_module`
  - `tests/test_import_rules.py::test_a_private_name_of_a_module_handed_over_is_still_a_crossing`

Old text:

```
                target, name = self._reached(module, use.rest)
                out.append(replace(use, target=target, name=name, rest=()))
```

New text:

```
                pass
```

### `u331.M07_followed_module_use_filtered_out`

Tree.uses: drop the uses that name a whole module, so a module reached as an attribute of a listed module is filtered away as an unknown name

- File: `scripts/refactor_measure.py`
- Source: `u331.json`, row `M07_followed_module_use_filtered_out`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_import_rules.py::test_a_module_handed_over_by_a_listed_one_is_a_reach_of_that_module`

Old text:

```
                if use.kind == "import"
                or use.name is None

```

New text:

```
                if use.kind == "import"

```

### `u246.S2_adapter_per_element`

InvocationResult: build the requested set once per result again (the shape on main)

- File: `src/cratekit/acquire/adapter.py`
- Source: `u246.json`, row `S2_adapter_per_element`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_comprehension_sets.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_comprehension_sets.py::test_no_comprehension_in_the_package_rebuilds_an_invariant_set_per_element`

Old text:

```
            stray = [r.key for r in self.results if r.key not in asked]
```

New text:

```
            stray = [r.key for r in self.results if r.key not in set(self.requested)]
```

### `u207.C1_no_isrc_track_skipped`

isrcs_held: a track with no readable ISRC is skipped rather than refusing the answer, so the code it answered is read as absent

- File: `src/cratekit/acquire/catalogue_api.py`
- Source: `u207.json`, row `C1_no_isrc_track_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`
- Collected: 32 against a baseline of 32
- Kills: 2 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_an_answer_that_cannot_be_attributed_whole_marks_nothing_absent[no-isrc]`
  - `tests/test_isrc_screen.py::test_an_answer_that_cannot_be_attributed_whole_marks_nothing_absent[unreadable-isrc]`

Old text:

```
            if not code:
                raise CatalogueUnavailable(
                    f"the catalogue API's answer to this {what} holds a track with no "
```

New text:

```
            if not code:
                continue
                raise CatalogueUnavailable(
                    f"the catalogue API's answer to this {what} holds a track with no "
```

### `u207.C2_code_not_asked_accepted`

isrcs_held: an answer naming a code nobody asked is accepted, so the code asked is read as absent

- File: `src/cratekit/acquire/catalogue_api.py`
- Source: `u207.json`, row `C2_code_not_asked_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_an_answer_that_cannot_be_attributed_whole_marks_nothing_absent[a-code-not-asked]`

Old text:

```
        if not named <= set(asked):
```

New text:

```
        if False:
```

### `u207.C3_paged_answer_accepted`

isrcs_held: an answer with a next link is read whole, so a code on the page not read is absent

- File: `src/cratekit/acquire/catalogue_api.py`
- Source: `u207.json`, row `C3_paged_answer_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_an_answer_that_cannot_be_attributed_whole_marks_nothing_absent[paged]`

Old text:

```
        if isinstance(links, Mapping) and _text(links.get("next")):
```

New text:

```
        if False:
```

### `u207.C4_non_resource_skipped`

isrcs_held: an entry that is not a resource is skipped rather than refusing the answer

- File: `src/cratekit/acquire/catalogue_api.py`
- Source: `u207.json`, row `C4_non_resource_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_an_answer_that_cannot_be_attributed_whole_marks_nothing_absent[not-a-resource]`

Old text:

```
            if not isinstance(resource, Mapping):
                raise CatalogueUnavailable(
```

New text:

```
            if not isinstance(resource, Mapping):
                continue
                raise CatalogueUnavailable(
```

### `u207.C5_batch_ceiling_raised`

catalogue: the batch ceiling is fifty, past the API's documented twenty

- File: `src/cratekit/acquire/catalogue_api.py`
- Source: `u207.json`, row `C5_batch_ceiling_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`
- Collected: 32 against a baseline of 32
- Kills: 4 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_a_failed_batch_does_not_stop_the_next_one`
  - `tests/test_isrc_screen.py::test_a_lone_code_is_never_screened_since_its_own_lookup_costs_the_same`
  - `tests/test_isrc_screen.py::test_fifty_codes_the_catalogue_files_nothing_under_cost_three_requests_not_fifty`
  - `tests/test_isrc_screen.py::test_the_app_client_refuses_a_batch_it_was_not_built_to_ask`

Old text:

```
ISRC_BATCH = 20
```

New text:

```
ISRC_BATCH = 50
```

### `u207.C6_batch_shape_unchecked`

isrcs_held: a batch of duplicate, unfolded or malformed codes is sent as given

- File: `src/cratekit/acquire/catalogue_api.py`
- Source: `u207.json`, row `C6_batch_shape_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_the_app_client_refuses_a_batch_it_was_not_built_to_ask`

Old text:

```
        if len(set(asked)) != len(asked) or any(code != match.isrc_token(code) for code in asked):
```

New text:

```
        if False:
```

### `r290-author.S02_acquire_download_call_removed`

Remove the one jobs.raise_for_state call from acquire/cli.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/acquire/cli.py`
- Source: `r290-author.json`, row `S02_acquire_download_call_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`
- Collected: 126 against a baseline of 126
- Kills: 6 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.download]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[acquire.download]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[acquire.download]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.download]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[acquire.download]`
  - `tests/test_job_outcome.py::test_every_function_that_drives_a_job_maps_its_ending_afterwards`

Old text:

```
jobs.raise_for_state(job)
```

New text:

```
jobs.get  # the mapping call, removed
```

### `r1313.I2_cache_keeps_any_status`

said_not_found: keep any failure carrying a status, so an outage is remembered for a week as filed under nothing

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `r1313.json`, row `I2_cache_keeps_any_status`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_said_not_found_is_the_clients_own_class_or_a_404_and_nothing_else[500]`

Old text:

```
    return answered_not_found(exc)
```

New text:

```
    return answered_not_found(exc) or getattr(getattr(exc, "response", None), "status_code", None) is not None
```

### `u206-b.M10b_day_coefficient_halved`

DAY_S halved, measured again once the tests write a day out as 86 400 seconds

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206-b.json`, row `M10b_day_coefficient_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`
- Collected: 60 against a baseline of 60
- Kills: 3 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_found_answer_is_asked_again_after_the_configured_days`
  - `tests/test_isrc_cache.py::test_a_found_answer_lives_thirty_days_unless_set`
  - `tests/test_isrc_cache.py::test_a_not_found_is_kept_and_asked_again_after_seven_days`

Old text:

```
DAY_S = 86_400
```

New text:

```
DAY_S = 43_200
```

### `u206-b.M2b_disabled_recall_composite`

Composite: drop recall's days 0 guard AND give every entry at least a day's life, so answers kept before the cache was turned off still answer

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206-b.json`, row `M2b_disabled_recall_composite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`
- Collected: 60 against a baseline of 60
- Kills: 2 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_answers_kept_before_the_cache_was_turned_off_answer_nothing`
  - `tests/test_isrc_cache.py::test_zero_days_asks_every_time_and_writes_nothing`

Old text:

```
        global _PROCESS_HITS
        if not self.enabled:
            return None
```

New text:

```
        global _PROCESS_HITS
        self.days = max(self.days, 1)
```

### `u206.M11_unreadable_answer_kept`

Cache.remember: keep an answer holding a track that cannot be read

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M11_unreadable_answer_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`
- Collected: 60 against a baseline of 60
- Kills: 3 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_an_answer_holding_a_track_that_cannot_be_read_is_asked_again[no-artist]`
  - `tests/test_isrc_cache.py::test_an_answer_holding_a_track_that_cannot_be_read_is_asked_again[no-identifier]`
  - `tests/test_isrc_cache.py::test_an_answer_holding_a_track_that_cannot_be_read_is_asked_again[no-title]`

Old text:

```
        if not all(_readable(track) for track in tracks):
            return False
```

New text:

```
        if False:
            return False
```

### `u206.M12_corrupt_file_not_set_aside`

Cache._entries: a file that does not parse is read as empty and overwritten, never set aside

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M12_corrupt_file_not_set_aside`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`
- Collected: 60 against a baseline of 60
- Kills: 3 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_corrupt_file_is_set_aside_and_the_lookup_succeeds`
  - `tests/test_isrc_cache.py::test_a_file_of_another_shape_is_set_aside_too`
  - `tests/test_isrc_cache.py::test_doctor_names_a_set_aside_file_and_never_fails`

Old text:

```
        if entries is None:
            if locked:
                self._set_aside_held()
            else:
                self._set_aside()
            return {}
```

New text:

```
        if entries is None:
            return {}
```

### `u206.M13_write_without_merge`

Cache.remember: write only this entry, dropping what another process wrote since

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M13_write_without_merge`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_isrc.py`, `tests/test_isrc_cache.py`
- Collected: 68 against a baseline of 68
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_a_one_id_isrc_is_listed_and_two_ids_and_no_isrc_are_handed_on`
  - `tests/test_isrc_cache.py::test_a_different_country_is_a_different_key`
  - `tests/test_isrc_cache.py::test_another_processs_answer_written_since_this_one_read_survives`
  - `tests/test_isrc_cache.py::test_two_writer_processes_leave_one_readable_file_holding_both`

Old text:

```
            merged = {
                name: entry for name, entry in entries.items() if self._fresh(entry, now) is not None
            }
```

New text:

```
            merged = {}
```

### `u206.M16_said_not_found_widened`

said_not_found: read InvalidISRC as a said not found too

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M16_said_not_found_widened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`
- Collected: 60 against a baseline of 60
- Kills: 3 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_an_invalid_isrc_the_account_reads_as_no_match_is_never_kept`
  - `tests/test_isrc_cache.py::test_an_outage_then_an_invalid_isrc_on_the_retry_keeps_nothing`
  - `tests/test_isrc_cache.py::test_said_not_found_is_the_clients_own_class_or_a_404_and_nothing_else[invalid-isrc]`

Old text:

```
    if type(exc).__name__ == "ObjectNotFound":
```

New text:

```
    if type(exc).__name__ in ("ObjectNotFound", "InvalidISRC"):
```

### `u206.M1_recall_never_hits`

Cache.recall: never answer from the file, so every lookup asks the provider again

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M1_recall_never_hits`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_isrc.py`, `tests/test_isrc_cache.py`
- Collected: 68 against a baseline of 68
- Kills: 18 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_a_one_id_isrc_is_listed_and_two_ids_and_no_isrc_are_handed_on`
  - `tests/test_isrc_cache.py::test_a_404_status_is_kept_as_a_not_found_at_either_seam[account]`
  - `tests/test_isrc_cache.py::test_a_404_status_is_kept_as_a_not_found_at_either_seam[catalogue]`
  - `tests/test_isrc_cache.py::test_a_choice_among_several_releases_is_made_from_a_remembered_answer_with_no_call`
  - `tests/test_isrc_cache.py::test_a_copy_run_redirecting_installation_state_shares_answers_through_the_override`
  - `tests/test_isrc_cache.py::test_a_found_answer_is_asked_again_after_the_configured_days`
  - `tests/test_isrc_cache.py::test_a_found_answer_lives_thirty_days_unless_set`
  - `tests/test_isrc_cache.py::test_a_not_found_is_kept_and_asked_again_after_seven_days`
  - `tests/test_isrc_cache.py::test_a_remembered_client_track_reads_as_the_client_track_does[streamable]`
  - `tests/test_isrc_cache.py::test_a_remembered_client_track_reads_as_the_client_track_does[withdrawn]`
  - `tests/test_isrc_cache.py::test_a_second_account_over_a_fresh_client_asks_nothing_for_an_answered_isrc`
  - `tests/test_isrc_cache.py::test_a_tie_remembered_is_still_refused_with_its_reason`
  - `tests/test_isrc_cache.py::test_an_expired_answer_is_replaced_by_the_new_one`
  - `tests/test_isrc_cache.py::test_an_outage_then_a_not_found_on_the_retry_keeps_the_not_found`
  - `tests/test_isrc_cache.py::test_the_catalogue_and_the_account_share_one_answer`
  - ... and 3 more, see the JSON sidecar

Old text:

```
        held = self._fresh(entries.get(key), self.clock())
```

New text:

```
        held = None
```

### `u206.M21_override_ignored`

_resolved: ignore CRATEKIT_ISRC_CACHE_DIR, so a hand copy run cannot share the live answers

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M21_override_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_rehearsal_keeps_the_live_isrc_cache_and_restores_the_environment`

Old text:

```
    if override:
        return Path(override) / config.state_file(key).relative
```

New text:

```
    if False:
        return Path(override) / config.state_file(key).relative
```

### `u206.M3_disabled_still_remembers`

Cache.remember: drop the days 0 guard, so a cache turned off still writes the file

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M3_disabled_still_remembers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_zero_days_asks_every_time_and_writes_nothing`

Old text:

```
        if not self.enabled:
            return False
        key = _key(isrc, country)
        if key is None:
            return False
        tracks = list(tracks)
```

New text:

```
        key = _key(isrc, country)
        if key is None:
            return False
        tracks = list(tracks)
```

### `u206.M4_unfolded_spelling_kept`

_key: keep a spelling that is not its own fold under the folded key

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M4_unfolded_spelling_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_spelling_that_is_not_its_own_fold_is_asked_and_never_kept`

Old text:

```
    if not folded or folded != isrc:
```

New text:

```
    if not folded:
```

### `u206.M5_country_ignored`

_key: leave the country out, so an answer in one country answers another

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M5_country_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`
- Collected: 60 against a baseline of 60
- Kills: 5 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_404_status_is_kept_as_a_not_found_at_either_seam[account]`
  - `tests/test_isrc_cache.py::test_a_404_status_is_kept_as_a_not_found_at_either_seam[catalogue]`
  - `tests/test_isrc_cache.py::test_a_corrupt_file_is_set_aside_and_the_lookup_succeeds`
  - `tests/test_isrc_cache.py::test_a_different_country_is_a_different_key`
  - `tests/test_isrc_cache.py::test_another_processs_answer_written_since_this_one_read_survives`

Old text:

```
    return f"{folded}|{country}"
```

New text:

```
    return f"{folded}|"
```

### `u206.M6_not_found_lives_as_found`

_fresh: a not found lives as long as a found answer

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M6_not_found_lives_as_found`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_not_found_is_kept_and_asked_again_after_seven_days`

Old text:

```
        days = self.days if tracks else min(NOT_FOUND_DAYS, self.days)
```

New text:

```
        days = self.days
```

### `u206.M7_not_found_ignores_shorter_setting`

_fresh: a not found lives a week even when the setting is shorter

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M7_not_found_ignores_shorter_setting`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_not_found_lives_no_longer_than_a_shorter_setting`

Old text:

```
        days = self.days if tracks else min(NOT_FOUND_DAYS, self.days)
```

New text:

```
        days = self.days if tracks else NOT_FOUND_DAYS
```

### `u206.M8_expiry_off_by_one`

_fresh: an entry exactly its lifetime old is still used

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M8_expiry_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`
- Collected: 60 against a baseline of 60
- Kills: 5 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_found_answer_is_asked_again_after_the_configured_days`
  - `tests/test_isrc_cache.py::test_a_found_answer_lives_thirty_days_unless_set`
  - `tests/test_isrc_cache.py::test_a_not_found_is_kept_and_asked_again_after_seven_days`
  - `tests/test_isrc_cache.py::test_a_not_found_lives_no_longer_than_a_shorter_setting`
  - `tests/test_isrc_cache.py::test_an_expired_answer_is_replaced_by_the_new_one`

Old text:

```
        if age < 0 or age >= days * DAY_S:
```

New text:

```
        if age < 0 or age > days * DAY_S:
```

### `u206.M9_future_stamp_trusted`

_fresh: an entry stamped later than now is used

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M9_future_stamp_trusted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_an_answer_stamped_later_than_now_is_asked_again`

Old text:

```
        if age < 0 or age >= days * DAY_S:
```

New text:

```
        if age >= days * DAY_S:
```

### `u207.S1_any_client_screened`

screen: ask any client with an isrcs_held member, not only the app catalogue, so a stand in that answers an empty set marks every code absent

- File: `src/cratekit/acquire/isrc_screen.py`
- Source: `u207.json`, row `S1_any_client_screened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_a_stand_in_for_the_client_is_never_screened_whatever_it_answers`

Old text:

```
        if self._stopped or not isinstance(client, catalogue_api.AppCatalogue):
            return 0
```

New text:

```
        if self._stopped or not callable(getattr(client, "isrcs_held", None)):
            return 0
```

### `u207.S2_lone_code_screened`

screen: a batch of one code is screened, paying a request its own lookup would have answered

- File: `src/cratekit/acquire/isrc_screen.py`
- Source: `u207.json`, row `S2_lone_code_screened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_a_lone_code_is_never_screened_since_its_own_lookup_costs_the_same`

Old text:

```
MIN_BATCH = 2
```

New text:

```
MIN_BATCH = 1
```

### `u207.S3_unfolded_spelling_screened`

screen: a spelling that is not its own fold enters a batch, so a lowercase code is screened under its fold

- File: `src/cratekit/acquire/isrc_screen.py`
- Source: `u207.json`, row `S3_unfolded_spelling_screened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_a_malformed_code_or_a_spelling_not_its_own_fold_never_enters_a_batch`

Old text:

```
            if code and code == match.isrc_token(code) and code not in self._asked
```

New text:

```
            if code and match.isrc_token(code) and code not in self._asked
```

### `u207.S4_rate_limit_keeps_screening`

screen: a rate limit or a rejected app credential on a batch leaves the screening running, so every later batch is sent into it

- File: `src/cratekit/acquire/isrc_screen.py`
- Source: `u207.json`, row `S4_rate_limit_keeps_screening`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`
- Collected: 32 against a baseline of 32
- Kills: 2 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_a_rate_limit_on_a_batch_is_counted_marks_nothing_and_stops_the_screening`
  - `tests/test_isrc_screen.py::test_a_rejected_app_credential_on_a_batch_marks_nothing_and_stops_the_screening`

Old text:

```
            except (catalogue_api.CatalogueRateLimited, catalogue_api.AppCredentialsRejected):
                self._stopped = True
                break
```

New text:

```
            except (catalogue_api.CatalogueRateLimited, catalogue_api.AppCredentialsRejected):
                continue
```

### `u207.S5_refused_form_keeps_screening`

screen: a 4xx refusal of the request form does not stop the screening

- File: `src/cratekit/acquire/isrc_screen.py`
- Source: `u207.json`, row `S5_refused_form_keeps_screening`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`
- Collected: 32 against a baseline of 32
- Kills: 3 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_a_refused_request_form_stops_the_screening_and_marks_nothing[400]`
  - `tests/test_isrc_screen.py::test_a_refused_request_form_stops_the_screening_and_marks_nothing[404]`
  - `tests/test_isrc_screen.py::test_a_refused_request_form_stops_the_screening_and_marks_nothing[422]`

Old text:

```
                if exc.status is not None and 400 <= exc.status < 500:
```

New text:

```
                if exc.status is not None and 400 <= exc.status < 400:
```

### `u207.S6_failed_batch_read_as_empty`

screen: a batch the API could not answer is read as an empty answer, so every code in it is answered not found

- File: `src/cratekit/acquire/isrc_screen.py`
- Source: `u207.json`, row `S6_failed_batch_read_as_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`
- Collected: 32 against a baseline of 32
- Kills: 8 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_a_failed_batch_does_not_stop_the_next_one`
  - `tests/test_isrc_screen.py::test_a_server_error_on_a_batch_falls_back_to_singles_and_finds_the_one_bad_answer`
  - `tests/test_isrc_screen.py::test_an_answer_that_cannot_be_attributed_whole_marks_nothing_absent[a-code-not-asked]`
  - `tests/test_isrc_screen.py::test_an_answer_that_cannot_be_attributed_whole_marks_nothing_absent[no-isrc]`
  - `tests/test_isrc_screen.py::test_an_answer_that_cannot_be_attributed_whole_marks_nothing_absent[no-list]`
  - `tests/test_isrc_screen.py::test_an_answer_that_cannot_be_attributed_whole_marks_nothing_absent[not-a-resource]`
  - `tests/test_isrc_screen.py::test_an_answer_that_cannot_be_attributed_whole_marks_nothing_absent[paged]`
  - `tests/test_isrc_screen.py::test_an_answer_that_cannot_be_attributed_whole_marks_nothing_absent[unreadable-isrc]`

Old text:

```
                continue
            self._absent.update(code for code in batch if code not in held)
```

New text:

```
                held = frozenset()
            self._absent.update(code for code in batch if code not in held)
```

### `u207.S7_failed_batch_sent_again`

screen: a batch's codes are marked asked only once it answered, so a failed batch is sent again by the next plan

- File: `src/cratekit/acquire/isrc_screen.py`
- Source: `u207.json`, row `S7_failed_batch_sent_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`
- Collected: 32 against a baseline of 32
- Kills: 2 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_a_batch_that_failed_is_not_sent_again_by_the_next_plan`
  - `tests/test_isrc_screen.py::test_a_code_already_screened_is_not_sent_again`

Old text:

```
            self._asked.update(batch)
            made += 1
```

New text:

```
            made += 1
```

### `u77-c.C3_not_a_manifest`

manifest_rows: stop asking whether the document names a manifest version at all, so a list document passed by mistake is not refused by name

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u77-c.json`, row `C3_not_a_manifest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_manifest_that_is_not_one_is_refused[the list]`

Old text:

```
if not isinstance(body, Mapping) or "manifest" not in body:
```

New text:

```
if not isinstance(body, Mapping):
```

### `u78-c.C1_readback_identity`

The text line read back compares only that one track came back, not which

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u78-c.json`, row `C1_readback_identity`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_isrc.py`
- Collected: 8 against a baseline of 8
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_a_track_that_cannot_be_a_text_line_is_named_and_the_rest_are_still_written`
  - `tests/test_intake_missing_isrc.py::test_missing_tracks_none_named_and_none_writable_refuse_rather_than_no_op`

Old text:

```
    if len(again) != 1 or (again[0].recording, again[0].version_key) != (
        wanted.recording,
        wanted.version_key,
    ):
```

New text:

```
    if len(again) != 1:
```

### `u78-c.C5_unlisted_checked_first`

The unlisted file is written over whatever is there, after the list, rather than checked with the other two

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u78-c.json`, row `C5_unlisted_checked_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_isrc.py`
- Collected: 8 against a baseline of 8
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_a_one_id_isrc_is_listed_and_two_ids_and_no_isrc_are_handed_on`

Old text:

```
        files.append((unlisted_path, _encoded(text_document(handed))))
    pending = [(path, payload) for path, payload in files if not _unchanged(path, payload)]
    for path, payload in pending:
        config.atomic_write_bytes(payload, path)
```

New text:

```
    pending = [(path, payload) for path, payload in files if not _unchanged(path, payload)]
    for path, payload in pending:
        config.atomic_write_bytes(payload, path)
    if handed:
        config.atomic_write_bytes(_encoded(text_document(handed)), unlisted_path)
```

### `r1016.M3_folder_parse_through_the_factory`

The folder walk parses with parse_factory again, so every owned playlist in a folder is fetched again

- File: `src/cratekit/acquire/listing.py`
- Source: `r1016.json`, row `M3_folder_parse_through_the_factory`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_folders_playlists_are_read_past_one_page_without_the_clients_lookup`

Old text:

```
    parse_playlist = _client_part(folder, "playlist", "parse", walk=FOLDER_WALK)
```

New text:

```
    parse_playlist = _client_part(folder, "playlist", "parse_factory", walk=FOLDER_WALK)
```

### `r878-a.A8_no_cursor_ends`

paginate_cursor: a response with no cursor no longer ends the walk

- File: `src/cratekit/acquire/listing.py`
- Source: `r878-a.json`, row `A8_no_cursor_ends`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_folders_playlists_are_read_past_one_page_without_the_clients_lookup`
  - `tests/test_label_playlists.py::test_the_root_folders_are_read_past_one_page`

Old text:

```
        if not page or not following:
```

New text:

```
        if not page:
```

### `r878-a.A9_cursor_advances`

paginate_cursor: never send the cursor the last response carried, so every request reads the first page

- File: `src/cratekit/acquire/listing.py`
- Source: `r878-a.json`, row `A9_cursor_advances`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_folders_playlists_are_read_past_one_page_without_the_clients_lookup`
  - `tests/test_label_playlists.py::test_the_root_folders_are_read_past_one_page`

Old text:

```
        cursor = str(following)
```

New text:

```
        pass
```

### `r878-b.B11_folder_rule_in_table`

STOP_RULES: put account_folders back on the empty page rule, the offset walk R-878 found

- File: `src/cratekit/acquire/listing.py`
- Source: `r878-b.json`, row `B11_folder_rule_in_table`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_the_root_folders_are_read_past_one_page`

Old text:

```
    "account_folders": StopRule.CURSOR,
```

New text:

```
    "account_folders": StopRule.EMPTY_PAGE,
```

### `r1709.M18_match_id_token`

match_id hashes the token, so intake missing drops a second emoji row as a line listed twice

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M18_match_id_token`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_two_emoji_rows_are_each_searched_and_listed`

Old text:

```
            f"mt_{_digest(self.wanted.distinct, self.wanted.version_key, self.wanted.key_key)}"

```

New text:

```
            f"mt_{_digest(self.wanted.recording, self.wanted.version_key, self.wanted.key_key)}"

```

### `r431-b.B4_the_engine_never_asks`

standing_tombstone asks under the companion kind for nothing, which is the defect the unit closes

- File: `src/cratekit/acquire/match.py`
- Source: `r431-b.json`, row `B4_the_engine_never_asks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_deleted_track_whose_row_kept_a_credit_is_suppressed_and_not_listed`

Old text:

```
    for identity in wanted.uncredited_spellings:
        if suppresses(UNCREDITED_KIND, identity):
```

New text:

```
    for identity in ():
        if suppresses(UNCREDITED_KIND, identity):
```

### `u265.M8_other_scorer`

_approximate: score the sorted forms with WRatio instead of ratio, so scores and the floor's cut move

- File: `src/cratekit/acquire/match.py`
- Source: `u265.json`, row `M8_other_scorer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`
- Collected: 90 against a baseline of 90
- Kills: 10 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_mixed_job_writes_only_the_missing_rows`
  - `tests/test_intake_missing.py::test_a_row_held_in_another_version_since_is_offered_not_listed`
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_a_track_deleted_on_purpose_is_suppressed_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`
  - `tests/test_intake_missing.py::test_rows_acquired_since_the_job_are_not_listed_and_name_no_download`
  - `tests/test_intake_missing.py::test_the_library_is_asked_where_it_is_now_not_where_the_job_froze_it`
  - `tests/test_intake_missing_search.py::test_an_accepted_candidate_the_library_now_holds_is_not_listed_again`

Old text:

```
        scorer=fuzz.ratio,
```

New text:

```
        scorer=fuzz.WRatio,
```

### `r1709.M11_recording_identity_is_the_token`

recording_identity reads the title by fold, the base's token, so every identity collapses again

- File: `src/cratekit/acquire/match_identity.py`
- Source: `r1709.json`, row `M11_recording_identity_is_the_token`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_search_answered_by_another_emoji_title_is_not_exact[another-emoji]`
  - `tests/test_intake_missing_search.py::test_two_emoji_rows_are_each_searched_and_listed`

Old text:

```
    return f"{fold(artist)}\x1f{title_identity(title)}"

```

New text:

```
    return f"{fold(artist)}\x1f{fold(title)}"

```

### `r1709.M4_bare_keeps_invisible`

bare_title keeps every invisible character, so a variation selector or a joiner makes one title two

- File: `src/cratekit/acquire/match_identity.py`
- Source: `r1709.json`, row `M4_bare_keeps_invisible`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_search_answered_by_another_emoji_title_is_not_exact[the-same-emoji]`

Old text:

```
    return "".join(ch for ch in composed if not ch.isspace() and not _invisible(ch))

```

New text:

```
    return "".join(ch for ch in composed if not ch.isspace())

```

### `r1709.M5_no_variation_selectors`

_invisible no longer drops the variation selectors, so the heart with and without its emoji presentation are two titles

- File: `src/cratekit/acquire/match_identity.py`
- Source: `r1709.json`, row `M5_no_variation_selectors`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_search_answered_by_another_emoji_title_is_not_exact[the-same-emoji]`

Old text:

```
    if any(point in selectors for selectors in _VARIATION_SELECTORS):
        return True

```

New text:

```
    if False:
        return True

```

### `r1709.M9_title_identity_is_the_fold`

title_identity returns the fold alone, the base's reading, so an emoji title is every other one by the artist

- File: `src/cratekit/acquire/match_identity.py`
- Source: `r1709.json`, row `M9_title_identity_is_the_fold`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`, `tests/test_isrc_screen.py`
- Collected: 82 against a baseline of 82
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_search_answered_by_another_emoji_title_is_not_exact[another-emoji]`
  - `tests/test_intake_missing_search.py::test_the_identity_is_the_folded_row_and_not_its_spelling`
  - `tests/test_intake_missing_search.py::test_two_emoji_rows_are_each_searched_and_listed`
  - `tests/test_isrc_screen.py::test_a_provider_track_under_another_emoji_title_does_not_agree`

Old text:

```
    bare = bare_title(title)
    return f"\x1f{bare}" if bare else ""

```

New text:

```
    return ""

```

### `r431-b.B7_the_engine_asks_under_the_tombstones_kind`

The engine's copy of the companion kind drifts onto the tombstone's own

- File: `src/cratekit/acquire/match_identity.py`
- Source: `r431-b.json`, row `B7_the_engine_asks_under_the_tombstones_kind`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_deleted_track_whose_row_kept_a_credit_is_suppressed_and_not_listed`

Old text:

```
UNCREDITED_KIND = "version-uncredited"
```

New text:

```
UNCREDITED_KIND = "version"
```

### `r667.G3_members_not_split`

credited_members: a comma separated tag is one name, so nobody is a member

- File: `src/cratekit/acquire/match_identity.py`
- Source: `r667.json`, row `G3_members_not_split`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_held_track_is_owned_and_nothing_is_listed[07A - 128 - Traumer, antraum, Anton - Hyaku.flac-tags2-row2]`

Old text:

```
    return tuple(part for part in (piece.strip() for piece in str(artist).split(",")) if part)
```

New text:

```
    return (str(artist).strip(),) if str(artist).strip() else ()
```

### `u305.M3_recorded_version_key_unfolded`

Recorded.version_key: fold the version without dropping the no-op qualifiers, so Original Mix and nothing are two versions

- File: `src/cratekit/acquire/match_identity.py`
- Source: `u305.json`, row `M3_recorded_version_key_unfolded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_an_original_mix_row_and_a_bare_candidate_are_one_version`
  - `tests/test_intake_missing_search.py::test_the_identity_is_the_folded_row_and_not_its_spelling`

Old text:

```
        return version_token(self.version)
```

New text:

```
        return fold(self.version)
```

### `r664.E4_title_not_split`

Skip split_title on the chosen title, so a version stays inside the recording token

- File: `src/cratekit/acquire/match_library.py`
- Source: `r664.json`, row `E4_title_not_split`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`
- Collected: 90 against a baseline of 90
- Kills: 13 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_held_track_is_owned_and_nothing_is_listed[04A - 126 - Malive, Tito Azevedo, MRQZ - Burning (Extended Mix).flac-tags1-row1]`
  - `tests/test_intake_missing.py::test_a_mixed_job_writes_only_the_missing_rows`
  - `tests/test_intake_missing.py::test_a_row_a_person_answered_as_another_track_stays_listed`
  - `tests/test_intake_missing.py::test_a_row_held_in_another_version_since_is_offered_not_listed`
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_a_track_deleted_on_purpose_is_suppressed_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_nobody_answered_is_unchanged_and_asks_nothing`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`
  - `tests/test_intake_missing.py::test_rows_acquired_since_the_job_are_not_listed_and_name_no_download`
  - `tests/test_intake_missing.py::test_the_library_is_asked_where_it_is_now_not_where_the_job_froze_it`
  - `tests/test_intake_missing_search.py::test_a_failed_search_says_which_offers_it_did_not_make`

Old text:

```
    title, version = split_title(spelled)

```

New text:

```
    title, version = spelled, ""

```

### `r667.E1_title_head_kept`

Existing: _read_from_disk takes the title tag verbatim, the R-664 defect

- File: `src/cratekit/acquire/match_library.py`
- Source: `r667.json`, row `E1_title_head_kept`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_held_track_is_owned_and_nothing_is_listed[04A - 126 - Malive, Tito Azevedo, MRQZ - Burning (Extended Mix).flac-tags1-row1]`
  - `tests/test_intake_missing.py::test_a_held_track_is_owned_and_nothing_is_listed[07A - 128 - Traumer, antraum, Anton - Hyaku.flac-tags2-row2]`
  - `tests/test_intake_missing.py::test_a_held_track_is_owned_and_nothing_is_listed[08A - 124 - Aurora Bloom - Sun Path.flac-tags0-row0]`

Old text:

```
    tagged_title = naming.strip_heads(spelled_tag, template=template)
```

New text:

```
    tagged_title = spelled_tag
```

### `r667.G8_no_credited_rule`

held: the recording token alone, the rule every caller had before this unit

- File: `src/cratekit/acquire/match_library.py`
- Source: `r667.json`, row `G8_no_credited_rule`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_held_track_is_owned_and_nothing_is_listed[07A - 128 - Traumer, antraum, Anton - Hyaku.flac-tags2-row2]`

Old text:

```
        return exact + credited
```

New text:

```
        return exact
```

### `r431-b.B2_a_row_billing_a_guest_asks`

uncredited_spellings ignores several_artists, so a row crediting a guest in its artists list asks

- File: `src/cratekit/acquire/match_list.py`
- Source: `r431-b.json`, row `B2_a_row_billing_a_guest_asks`
- Moved: the same text, now in src/cratekit/acquire/match_list.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_billed_guest_survives_the_freeze_the_worker_resolves_from`

Old text:

```
        if not self.spelled or self.several_artists or _credits_in(self.spelled):
```

New text:

```
        if not self.spelled or _credits_in(self.spelled):
```

### `r431-b.B8_the_reader_never_counts_the_artists`

_from_row stops setting several_artists, so every provider row reads as billing one

- File: `src/cratekit/acquire/match_list.py`
- Source: `r431-b.json`, row `B8_the_reader_never_counts_the_artists`
- Moved: the same text, now in src/cratekit/acquire/match_list.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_billed_guest_survives_the_freeze_the_worker_resolves_from`

Old text:

```
        several_artists=_bills_several(row),
```

New text:

```
        several_artists=False,
```

### `u197.M5_adapter_name`

VendoredAdapter.name: keep the retired key, so the class disagrees with the registry and the configuration

- File: `src/cratekit/acquire/vendored.py`
- Source: `u197.json`, row `M5_adapter_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 9 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_configuration_naming_the_retired_vendored_key_passes_the_adapter_check`
  - `tests/test_doctor.py::test_a_green_doctor_exits_zero`
  - `tests/test_doctor.py::test_a_headless_machine_that_opted_into_the_environment_fallback_is_not_red`
  - `tests/test_doctor.py::test_a_re_run_repairs_a_spelled_remote_rclone_does_not_know`
  - `tests/test_doctor.py::test_a_second_setup_run_asks_nothing_and_changes_nothing_it_was_not_asked_to`
  - `tests/test_doctor.py::test_an_empty_credential_leaves_the_exit_code_to_doctor`
  - `tests/test_doctor.py::test_the_backup_flags_are_recorded_without_a_question`
  - `tests/test_doctor.py::test_the_disagreeing_remote_refusal_names_the_flag_and_the_flag_repairs_it`
  - `tests/test_doctor.py::test_the_wizard_on_a_clean_machine_produces_a_valid_config_and_a_green_doctor`

Old text:

```
    name = "vendored"
```

New text:

```
    name = "tidal_dl_ng"
```

### `u254.M07_always_append`

mark_applied: append even to a torn, absent or schema 1 ledger

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M07_always_append`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`
- Collected: 10 against a baseline of 10
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_a_collection_read_before_the_commit_does_not_hide_the_landed_rows`
  - `tests/test_intake_land_filing.py::test_five_files_land_and_file_under_one_answer`

Old text:

```
            if appendable:
                config.append_durable_bytes(line, path)
```

New text:

```
            if True:
                config.append_durable_bytes(line, path)
```

### `u254.M19_already_inverted`

apply_plan: report as already applied the entries the ledger does not hold

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M19_already_inverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`
- Collected: 10 against a baseline of 10
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_five_files_land_and_file_under_one_answer`

Old text:

```
        entry.entry_id for entry in plan.applicable() if entry.entry_id in done
```

New text:

```
        entry.entry_id for entry in plan.applicable() if entry.entry_id not in done
```

### `r235-b.M25_adoption_refusal_names_no_verb`

the adoption refusal on an uncut library is re-raised as it came, with no step

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `r235-b.json`, row `M25_adoption_refusal_names_no_verb`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_an_uncut_library_refuses_adoption_and_names_the_cutover_verb`
  - `tests/test_cutover_cli.py::test_the_steps_the_refused_adoption_names_are_the_steps_that_work`

Old text:

```
        named = _naming_the_cutover(exc)
        if named is None:
```

New text:

```
        named = None
        if named is None:
```

### `u132.W2_coded_note`

A skip over an undeclared class carries favorites-skipped, not its cause code

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u132.json`, row `W2_coded_note`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`, `tests/test_genre_favorites_adoption.py`
- Collected: 49 against a baseline of 49
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_the_undeclared_note_states_the_version_the_skip_saw`
  - `tests/test_genre_favorites_adoption.py::test_an_adoption_over_a_taxonomy_without_the_class_names_the_skipped_step`

Old text:

```
    if skipped and cause == genre_favorites.CLASS_UNDECLARED:

```

New text:

```
    if False:

```

### `u132.W3_version_from_report`

The job's report does not carry the version the skip saw

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u132.json`, row `W3_version_from_report`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites_adoption.py`
- Collected: 3 against a baseline of 3
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites_adoption.py::test_an_adoption_over_a_taxonomy_without_the_class_names_the_skipped_step`

Old text:

```
            "schema_version": declared.schema_version,

```

New text:

```
            "schema_version": None,

```

### `u165.A1_scope`

census: ignore the scope and walk the whole collection

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u165.json`, row `A1_scope`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`
- Collected: 10 against a baseline of 10
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_the_census_a_landing_files_walks_only_the_rows_it_made`

Old text:

```
        rows = tuple(row for row in rows if row.content_id in scope)
```

New text:

```
        rows = tuple(rows)
```

### `u165.P1_undeclared`

predicted_place: route a band the taxonomy declares no sub for

- File: `src/cratekit/adopt/plan.py`
- Source: `u165.json`, row `P1_undeclared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`
- Collected: 10 against a baseline of 10
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_a_band_the_taxonomy_declares_no_sub_for_predicts_undeclared`

Old text:

```
        return Predicted(disposition=Disposition.UNDECLARED)
```

New text:

```
        return Predicted(disposition=disposition, bucket=bucket)
```

### `u165.P2_vocal_sub`

predicted_place: give every route the vocal sub, vox or not

- File: `src/cratekit/adopt/plan.py`
- Source: `u165.json`, row `P2_vocal_sub`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`
- Collected: 10 against a baseline of 10
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_a_collection_read_before_the_commit_does_not_hide_the_landed_rows`
  - `tests/test_intake_land_filing.py::test_five_files_land_and_file_under_one_answer`

Old text:

```
    vocal = (vocal_sub(declared, bucket) or "") if vox else ""
```

New text:

```
    vocal = vocal_sub(declared, bucket) or ""
```

### `u165.P3_of_vocal`

Predicted.of: read the vocal sub of an entry whatever its vocal state

- File: `src/cratekit/adopt/plan.py`
- Source: `u165.json`, row `P3_of_vocal`
- Moved: Predicted.of now names the vocal sub before building itself; the condition on it is dropped as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`
- Collected: 10 against a baseline of 10
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_an_entry_whose_vocal_is_not_added_reads_no_vocal_sub`

Old text:

```
        vocal_sub = entry.vocal_sub if entry.vocal == VOCAL_ADD else ""
```

New text:

```
        vocal_sub = entry.vocal_sub
```

### `r744.A1_near_miss_widened`

off by four counts as a near miss, hiding sitting 19's 144 against 140.00 in the bucket the bin width explains

- File: `src/cratekit/analysis/agreement.py`
- Source: `r744.json`, row `A1_near_miss_widened`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_head_agreement.py`
- Collected: 65 against a baseline of 65
- Kills: 5 (killed)
- Killed:
  - `tests/test_head_agreement.py::test_a_head_off_by_four_is_not_off_by_one_to_three`
  - `tests/test_head_agreement.py::test_the_comparison_buckets_every_row_and_counts_what_it_could_not_compare`
  - `tests/test_head_agreement.py::test_the_four_tempo_buckets[124-120.0-other_level]`
  - `tests/test_head_agreement.py::test_the_measurement_reads_a_disposable_copy_and_buckets_the_fixture`
  - `tests/test_head_agreement.py::test_the_script_prints_the_four_buckets_over_a_fixture_copy`

Old text:

```
    if distance <= 3:
        return OFF_ONE_TO_THREE
```

New text:

```
    if distance <= 4:
        return OFF_ONE_TO_THREE
```

### `r744.A2_half_not_recognised`

a head at half the reference is read as another level rather than as the octave case

- File: `src/cratekit/analysis/agreement.py`
- Source: `r744.json`, row `A2_half_not_recognised`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_head_agreement.py`
- Collected: 65 against a baseline of 65
- Kills: 4 (killed)
- Killed:
  - `tests/test_head_agreement.py::test_the_comparison_buckets_every_row_and_counts_what_it_could_not_compare`
  - `tests/test_head_agreement.py::test_the_four_tempo_buckets[83-166.0-half_or_double]`
  - `tests/test_head_agreement.py::test_the_measurement_reads_a_disposable_copy_and_buckets_the_fixture`
  - `tests/test_head_agreement.py::test_the_script_prints_the_four_buckets_over_a_fixture_copy`

Old text:

```
    if abs(ratio - 2.0) <= _DOUBLE_TOLERANCE or abs(ratio - 0.5) <= _HALF_TOLERANCE:
```

New text:

```
    if abs(ratio - 2.0) <= _DOUBLE_TOLERANCE:
```

### `r744.A3_classic_names_unmapped`

a classic key name is not mapped, so a library whose display is not Camelot reads every key as unkeyed

- File: `src/cratekit/analysis/agreement.py`
- Source: `r744.json`, row `A3_classic_names_unmapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_head_agreement.py`
- Collected: 65 against a baseline of 65
- Kills: 18 (killed)
- Killed:
  - `tests/test_head_agreement.py::test_either_key_notation_maps_to_one_padded_camelot[A#-06B]`
  - `tests/test_head_agreement.py::test_either_key_notation_maps_to_one_padded_camelot[Abm-01A]`
  - `tests/test_head_agreement.py::test_either_key_notation_maps_to_one_padded_camelot[Am-08A]`
  - `tests/test_head_agreement.py::test_either_key_notation_maps_to_one_padded_camelot[Bb-06B]`
  - `tests/test_head_agreement.py::test_either_key_notation_maps_to_one_padded_camelot[C#-03B]`
  - `tests/test_head_agreement.py::test_either_key_notation_maps_to_one_padded_camelot[C#m-12A]`
  - `tests/test_head_agreement.py::test_either_key_notation_maps_to_one_padded_camelot[C-08B]`
  - `tests/test_head_agreement.py::test_either_key_notation_maps_to_one_padded_camelot[Db-03B]`
  - `tests/test_head_agreement.py::test_either_key_notation_maps_to_one_padded_camelot[Dbm-12A]`
  - `tests/test_head_agreement.py::test_either_key_notation_maps_to_one_padded_camelot[F#-02B]`
  - `tests/test_head_agreement.py::test_either_key_notation_maps_to_one_padded_camelot[F#m-11A]`
  - `tests/test_head_agreement.py::test_either_key_notation_maps_to_one_padded_camelot[G#m-01A]`
  - `tests/test_head_agreement.py::test_either_key_notation_maps_to_one_padded_camelot[Gb-02B]`
  - `tests/test_head_agreement.py::test_either_key_notation_maps_to_one_padded_camelot[Gbm-11A]`
  - `tests/test_head_agreement.py::test_every_classic_name_reaches_one_of_the_twenty_four_codes`
  - ... and 3 more, see the JSON sidecar

Old text:

```
    classic = _CLASSIC_TO_CAMELOT.get(text)
```

New text:

```
    classic = None
```

### `r744.A4_whole_number_counts_as_rekordbox`

a whole number stored tempo counts as rekordbox's own analysis, so the imported back catalogue measures itself

- File: `src/cratekit/analysis/agreement.py`
- Source: `r744.json`, row `A4_whole_number_counts_as_rekordbox`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_head_agreement.py`
- Collected: 65 against a baseline of 65
- Kills: 2 (killed)
- Killed:
  - `tests/test_head_agreement.py::test_a_fractional_stored_tempo_is_rekordbox_own_analysis_and_a_whole_one_is_not`
  - `tests/test_head_agreement.py::test_reanalysis_samples_rekordbox_own_rows_with_a_file_and_buckets_the_detector`

Old text:

```
        return bool(self.stored_hundredths) and self.stored_hundredths % 100 != 0
```

New text:

```
        return bool(self.stored_hundredths)
```

### `r744.A5_removed_rows_counted`

a row rekordbox removed is compared, measuring a head nobody can see

- File: `src/cratekit/analysis/agreement.py`
- Source: `r744.json`, row `A5_removed_rows_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_head_agreement.py`
- Collected: 65 against a baseline of 65
- Kills: 2 (killed)
- Killed:
  - `tests/test_head_agreement.py::test_the_measurement_reads_a_disposable_copy_and_buckets_the_fixture`
  - `tests/test_head_agreement.py::test_the_script_prints_the_four_buckets_over_a_fixture_copy`

Old text:

```
            detail={"content_id": str(getattr(content, "ID", ""))},
        ):
            continue
```

New text:

```
            detail={"content_id": str(getattr(content, "ID", ""))},
        ):
            pass
```

### `r744.A6_sample_never_full`

the sample keeps resolving rows after the limit, walking the whole collection for ten files

- File: `src/cratekit/analysis/agreement.py`
- Source: `r744.json`, row `A6_sample_never_full`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_head_agreement.py`
- Collected: 65 against a baseline of 65
- Kills: 1 (killed)
- Killed:
  - `tests/test_head_agreement.py::test_the_sample_stops_resolving_rows_once_it_is_full`

Old text:

```
        if len(chosen) >= limit:
            break
```

New text:

```
        if len(chosen) >= limit:
            pass
```

### `u343.M20_detection_head_keeps_a_key`

head_from_detection: read a detector's camelot again, so a fake's key is compared

- File: `src/cratekit/analysis/agreement.py`
- Source: `u343.json`, row `M20_detection_head_keeps_a_key`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_head_agreement.py`
- Collected: 65 against a baseline of 65
- Kills: 1 (killed)
- Killed:
  - `tests/test_head_agreement.py::test_the_detector_head_is_its_tempo_with_no_key_and_a_terminal_is_none`

Old text:

```
    return (None, int(found["rate"]))
```

New text:

```
    camelot = found.get("camelot")
    return (pad_camelot(str(camelot)) if camelot else None, int(found["rate"]))
```

### `r744.B1_window_not_bound`

the run binds the shipped window rather than the configured one, so analysis.tempo_floor and tempo_ceiling change nothing

- File: `src/cratekit/analysis/cli.py`
- Source: `r744.json`, row `B1_window_not_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_head_agreement.py`
- Collected: 65 against a baseline of 65
- Kills: 1 (killed)
- Killed:
  - `tests/test_head_agreement.py::test_a_raised_window_loads_and_reaches_the_detector_binding`

Old text:

```
            tempo_window=(cfg.analysis.tempo_floor, cfg.analysis.tempo_ceiling),
```

New text:

```
            tempo_window=(80, 160),
```

### `u157.A1_no_level_tag`

_finalize: write no driftlevel tag

- File: `src/cratekit/analysis/cli.py`
- Source: `u157.json`, row `A1_no_level_tag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_drift.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/test_drift.py::test_a_measured_drift_is_written_as_its_level_and_verdict`

Old text:

```
        "driftlevel": _drift_level(scored.get("drift")),
```

New text:

```
        "driftlevel": None,
```

### `u157.A2_cut_unbound`

_bind_defaults: bind no drift cut, so the detector reads the shipped default

- File: `src/cratekit/analysis/cli.py`
- Source: `u157.json`, row `A2_cut_unbound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_drift.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/test_drift.py::test_a_whole_number_cut_loads_and_reaches_the_detector_binding`

Old text:

```
            drift_cut=cfg.analysis.drift_cut,

```

New text:

```
(empty)
```

### `r744.E8_record_applies_to_every_window`

the recorded agreement says it applies whatever window the run bound, so a DJ who raised theirs is shown a rate nobody measured for it

- File: `src/cratekit/analysis/detect.py`
- Source: `r744.json`, row `E8_record_applies_to_every_window`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_head_agreement.py`
- Collected: 65 against a baseline of 65
- Kills: 1 (killed)
- Killed:
  - `tests/test_head_agreement.py::test_the_record_says_whether_it_applies_to_the_bound_window`

Old text:

```
    record["applies_to_window"] = window is None or tuple(window) == measured
```

New text:

```
    record["applies_to_window"] = True
```

### `r744.E9_record_does_not_sum`

one recorded bucket is changed, so the four no longer sum to the files measured

- File: `src/cratekit/analysis/detect.py`
- Source: `r744.json`, row `E9_record_does_not_sum`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_head_agreement.py`
- Collected: 65 against a baseline of 65
- Kills: 1 (killed)
- Killed:
  - `tests/test_head_agreement.py::test_the_recorded_buckets_sum_to_the_files_measured`

Old text:

```
        "equal": 194,
```

New text:

```
        "equal": 190,
```

### `u343.M22_record_keeps_key_buckets`

_HEAD_AGREEMENT: carry the detector's key buckets in the run's answer again

- File: `src/cratekit/analysis/detect.py`
- Source: `u343.json`, row `M22_record_keeps_key_buckets`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_head_agreement.py`
- Collected: 65 against a baseline of 65
- Kills: 1 (killed)
- Killed:
  - `tests/test_head_agreement.py::test_the_recorded_shape_is_the_shape_the_measurement_prints`

Old text:

```
    "within_one": 226,
}
```

New text:

```
    "within_one": 226,
    "key": {"equal": 158, "differs": 141},
}
```

### `r290-author.R2_backup_rebuild_drops_the_type`

Rebuild the backup rehearsal refusal as a plain CratekitError again, so a rehearsal the worker parked says failed

- File: `src/cratekit/backup/cli.py`
- Source: `r290-author.json`, row `R2_backup_rebuild_drops_the_type`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`
- Collected: 126 against a baseline of 126
- Kills: 1 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_reworded_refusal_is_rebuilt_in_one_place_only`

Old text:

```
    return rebuilt(
        error,
        replace(
```

New text:

```
    return CratekitError(
        replace(
```

### `r290-author.S04_backup_call_removed`

Remove the one jobs.raise_for_state call from backup/cli.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/backup/cli.py`
- Source: `r290-author.json`, row `S04_backup_call_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`
- Collected: 126 against a baseline of 126
- Kills: 6 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[backup.run]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[backup.run]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[backup.run]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[backup.run]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[backup.run]`
  - `tests/test_job_outcome.py::test_every_function_that_drives_a_job_maps_its_ending_afterwards`

Old text:

```
jobs.raise_for_state(job)
```

New text:

```
jobs.get  # the mapping call, removed
```

### `r1334.S18_emit_open_gate_only`

_emit: print the gate screen for an open gate only, as before

- File: `src/cratekit/cli/__init__.py`
- Source: `r1334.json`, row `S18_emit_open_gate_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_stale_screen.py::test_through_the_dispatcher_the_stale_refusal_shows_the_moved_plan_and_a_decide_applies_it`

Old text:

```
    if envelope.cause is not None and render.is_gate_screen(envelope.cause):
```

New text:

```
    if envelope.cause is not None and envelope.cause.reason == "decision-required":
```

### `r290-author.D1_dispatcher_ignores_the_type`

Make the dispatcher blind to JobBlocked, so a parked job exits non zero and says failed

- File: `src/cratekit/cli/__init__.py`
- Source: `r290-author.json`, row `D1_dispatcher_ignores_the_type`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`
- Collected: 126 against a baseline of 126
- Kills: 42 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_park_on_a_gate_coded_cause_is_still_not_resumable_through_the_run`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.bandcamp-fetch]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.download]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.fallback-fetch]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[adopt.scan]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[analyze.restamp]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[analyze.run]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[analyze.vocals]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[backup.run]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[export.playlist]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[intake.playlist]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[intake.set]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[label.import]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[label.judge]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[master]`
  - ... and 27 more, see the JSON sidecar

Old text:

```
        parked = isinstance(exc, JobBlocked)
```

New text:

```
        parked = False
```

### `r290-author.D2_parked_marked_resumable`

Mark a parked job's envelope resumable, which sends a wrapper to crate run for work only the verb can continue

- File: `src/cratekit/cli/__init__.py`
- Source: `r290-author.json`, row `D2_parked_marked_resumable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`
- Collected: 126 against a baseline of 126
- Kills: 2 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_park_on_a_gate_coded_cause_is_still_not_resumable_through_the_run`
  - `tests/test_job_outcome.py::test_the_dispatcher_reads_the_blocked_type_as_the_blocked_outcome`

Old text:

```
            resumable=resumable,
            outcome=outcome,
```

New text:

```
            resumable=resumable or parked,
            outcome=outcome,
```

### `r290-author.D4_cancelled_reads_failed`

Read the cancelled type as the failed outcome, which is what the dispatcher said before Outcome.CANCELLED had a producer

- File: `src/cratekit/cli/__init__.py`
- Source: `r290-author.json`, row `D4_cancelled_reads_failed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`
- Collected: 126 against a baseline of 126
- Kills: 20 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.bandcamp-fetch]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.download]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.fallback-fetch]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[adopt.scan]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[analyze.restamp]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[analyze.run]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[analyze.vocals]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[backup.run]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[export.playlist]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[intake.playlist]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[intake.set]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[label.import]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[label.judge]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[master]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[rebuild]`
  - ... and 5 more, see the JSON sidecar

Old text:

```
            outcome = Outcome.CANCELLED
```

New text:

```
            outcome = Outcome.FAILED
```

### `u168.C10_argv_never`

_dispatched: never record the command line

- File: `src/cratekit/cli/__init__.py`
- Source: `u168.json`, row `C10_argv_never`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 1020 against a baseline of 1020
- Kills: 2 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_run_continued_by_hand_keeps_the_command_line_its_first_invocation_recorded`
  - `tests/test_cli_contract.py::test_run_decide_continue_resumes_the_owning_verb_with_its_own_arguments`

Old text:

```
        if not args.run:
            state.argv = _verb_argv(argv, entry)
```

New text:

```
        if False:
            state.argv = _verb_argv(argv, entry)
```

### `u168.C11_argv_whole_line`

_verb_argv: keep the global options before the verb

- File: `src/cratekit/cli/__init__.py`
- Source: `u168.json`, row `C11_argv_whole_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 1020 against a baseline of 1020
- Kills: 2 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_run_continued_by_hand_keeps_the_command_line_its_first_invocation_recorded`
  - `tests/test_cli_contract.py::test_run_decide_continue_resumes_the_owning_verb_with_its_own_arguments`

Old text:

```
            return tuple(tokens[index:])
```

New text:

```
            return tuple(tokens)
```

### `u168.C9_argv_on_every_run`

_dispatched: record the command line on a continued run too, overwriting the first

- File: `src/cratekit/cli/__init__.py`
- Source: `u168.json`, row `C9_argv_on_every_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 1020 against a baseline of 1020
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_run_continued_by_hand_keeps_the_command_line_its_first_invocation_recorded`

Old text:

```
        if not args.run:
            state.argv = _verb_argv(argv, entry)
```

New text:

```
        if True:
            state.argv = _verb_argv(argv, entry)
```

### `u186.D1_dispatch_unhooked`

dispatcher: never call the sibling hook, so a second plan at its gate is told nothing

- File: `src/cratekit/cli/__init__.py`
- Source: `u186.json`, row `D1_dispatch_unhooked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 9 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_a_reading_that_breaks_says_so_and_leaves_the_gate_as_it_was`
  - `tests/test_gate_siblings.py::test_a_record_missing_a_field_is_named_unreadable_at_the_gate_and_in_doctor`
  - `tests/test_gate_siblings.py::test_a_record_that_cannot_be_read_is_said_rather_than_read_as_no_run`
  - `tests/test_gate_siblings.py::test_a_sibling_whose_gate_is_open_is_named_as_open`
  - `tests/test_gate_siblings.py::test_an_answer_just_inside_twelve_hours_is_still_named`
  - `tests/test_gate_siblings.py::test_an_answer_ten_minutes_ago_is_named_with_its_actor_option_and_time`
  - `tests/test_gate_siblings.py::test_an_answer_with_no_recorded_time_is_named_as_unrecorded`
  - `tests/test_gate_siblings.py::test_one_warning_per_other_run`
  - `tests/test_gate_siblings.py::test_the_warning_prints_on_the_screen_a_person_reads`

Old text:

```
        if state is not None and resumable:
            envelope = _with_sibling_runs(envelope, state)
```

New text:

```
(empty)
```

### `u186.D2_dispatch_any_refusal`

dispatcher: call the hook on every refusal, not only a run persisted at its gate

- File: `src/cratekit/cli/__init__.py`
- Source: `u186.json`, row `D2_dispatch_any_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_a_refusal_before_the_gate_names_no_sibling`

Old text:

```
        if state is not None and resumable:
            envelope = _with_sibling_runs(envelope, state)
```

New text:

```
        if state is not None:
            envelope = _with_sibling_runs(envelope, state)
```

### `u186.D3_dispatch_scope`

_with_sibling_runs: drop the database writing scope guard

- File: `src/cratekit/cli/__init__.py`
- Source: `u186.json`, row `D3_dispatch_scope`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_a_verb_writing_no_database_says_nothing_of_its_own_siblings`

Old text:

```
    if not gates.writes_the_database(state.verb):
        return envelope
    try:
        found, unreadable = gates.siblings(state.verb, exclude=state.run_id)
```

New text:

```
    try:
        found, unreadable = gates.siblings(state.verb, exclude=state.run_id)
```

### `u186.D4_dispatch_break_silent`

_with_sibling_runs: a reading that breaks says nothing rather than naming the break

- File: `src/cratekit/cli/__init__.py`
- Source: `u186.json`, row `D4_dispatch_break_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_a_reading_that_breaks_says_so_and_leaves_the_gate_as_it_was`

Old text:

```
    except Exception as exc:  # noqa: BLE001 - see the docstring, the gate stays the gate
        said = [
```

New text:

```
    except Exception as exc:  # noqa: BLE001 - see the docstring, the gate stays the gate
        said = [] and [
```

### `u206.M23_lookup_line_dropped`

_with_isrc_lookups: never add the isrc-lookups line

- File: `src/cratekit/cli/__init__.py`
- Source: `u206.json`, row `M23_lookup_line_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_isrc.py`
- Collected: 8 against a baseline of 8
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_a_one_id_isrc_is_listed_and_two_ids_and_no_isrc_are_handed_on`

Old text:

```
    if remembered == 0 and asked == 0:
        return envelope
```

New text:

```
    if True:
        return envelope
```

### `u248.L10_built_before_the_builder`

build: count the verb built before its builder returns, so a builder that failed part way hands on a half built verb

- File: `src/cratekit/cli/__init__.py`
- Source: `u248.json`, row `L10_built_before_the_builder`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cli_lazy.py`
- Collected: 161 against a baseline of 161
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_lazy.py::test_a_verb_is_built_once_however_often_it_is_asked`

Old text:

```
            ) from exc
        self.built = True
```

New text:

```
            ) from exc
        self.built = self.built
```

### `u248.L1_lazy_off`

build_parser: build every verb eagerly whatever eager says, so every command imports every verb module again

- File: `src/cratekit/cli/__init__.py`
- Source: `u248.json`, row `L1_lazy_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_cli_lazy.py`
- Collected: 1181 against a baseline of 1181
- Kills: 12 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_defect_in_our_own_module_does_not_masquerade_as_a_missing_extra`
  - `tests/test_cli_lazy.py::test_a_broken_module_fails_its_own_verb_and_leaves_every_other_one_working`
  - `tests/test_cli_lazy.py::test_a_defective_builder_is_a_defect_and_never_a_usage_error`
  - `tests/test_cli_lazy.py::test_a_group_help_loads_no_verb_module_when_none_of_its_verbs_declares_an_extra`
  - `tests/test_cli_lazy.py::test_a_listing_asks_only_the_verbs_whose_line_could_differ`
  - `tests/test_cli_lazy.py::test_a_module_that_raises_anything_at_import_is_listed_plainly_and_raises_for_its_verb`
  - `tests/test_cli_lazy.py::test_a_verb_is_built_once_however_often_it_is_asked`
  - `tests/test_cli_lazy.py::test_an_argument_error_raised_by_the_import_is_a_defect_too`
  - `tests/test_cli_lazy.py::test_doctor_help_loads_the_doctor_and_only_what_the_doctor_itself_imports`
  - `tests/test_cli_lazy.py::test_the_version_and_the_top_level_help_load_no_verb_module[bare]`
  - `tests/test_cli_lazy.py::test_the_version_and_the_top_level_help_load_no_verb_module[help]`
  - `tests/test_cli_lazy.py::test_the_version_and_the_top_level_help_load_no_verb_module[version]`

Old text:

```
        if not eager:
            sub = target.add_parser(path[-1], help=entry.summary)
```

New text:

```
        if False:
            sub = target.add_parser(path[-1], help=entry.summary)
```

### `u248.L2_chosen_never_built`

_LazyChoices.__call__: never build the chosen verb, so it parses as an empty subparser with no handler

- File: `src/cratekit/cli/__init__.py`
- Source: `u248.json`, row `L2_chosen_never_built`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_cli_lazy.py`
- Collected: 1181 against a baseline of 1181
- Kills: 314 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_decision_answered_against_a_plan_that_has_since_moved_is_stale`
  - `tests/test_cli_contract.py::test_a_decision_naming_a_gate_the_verb_does_not_declare_is_refused`
  - `tests/test_cli_contract.py::test_a_defect_in_our_own_module_does_not_masquerade_as_a_missing_extra`
  - `tests/test_cli_contract.py::test_a_gate_is_answerable_from_a_different_process_in_a_later_session`
  - `tests/test_cli_contract.py::test_a_malformed_decision_is_refused_rather_than_ignored`
  - `tests/test_cli_contract.py::test_a_profile_that_switches_a_module_off_removes_its_verbs`
  - `tests/test_cli_contract.py::test_a_run_carrying_a_pending_action_reports_it_as_pending`
  - `tests/test_cli_contract.py::test_a_run_continued_by_hand_keeps_the_command_line_its_first_invocation_recorded`
  - `tests/test_cli_contract.py::test_a_run_record_belongs_to_the_verb_that_created_it`
  - `tests/test_cli_contract.py::test_a_run_that_reached_a_gate_reports_it`
  - `tests/test_cli_contract.py::test_a_scripted_run_with_no_terminal_reaches_a_gate_and_exits_with_its_code`
  - `tests/test_cli_contract.py::test_a_verb_blocked_by_an_unverified_pending_action_refuses_before_doing_anything`
  - `tests/test_cli_contract.py::test_a_verb_that_exits_the_process_directly_is_converted_rather_than_obeyed`
  - `tests/test_cli_contract.py::test_a_verb_that_raises_something_unexpected_becomes_an_internal_cause`
  - `tests/test_cli_contract.py::test_an_unanswered_gate_exits_with_the_documented_code_and_leaves_the_run_resumable`
  - ... and 299 more, see the JSON sidecar

Old text:

```
        if waiting is not None:
            waiting.build()
```

New text:

```
        if waiting is not None:
            pass
```

### `u248.L3_listing_asks_everyone`

ask_for_listing: ask every verb, not only those declaring extras, so a group help imports all its verbs

- File: `src/cratekit/cli/__init__.py`
- Source: `u248.json`, row `L3_listing_asks_everyone`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cli_lazy.py`
- Collected: 161 against a baseline of 161
- Kills: 4 (killed)
- Killed:
  - `tests/test_cli_lazy.py::test_a_group_help_loads_no_verb_module_when_none_of_its_verbs_declares_an_extra`
  - `tests/test_cli_lazy.py::test_a_listing_asks_only_the_verbs_whose_line_could_differ`
  - `tests/test_cli_lazy.py::test_the_version_and_the_top_level_help_load_no_verb_module[bare]`
  - `tests/test_cli_lazy.py::test_the_version_and_the_top_level_help_load_no_verb_module[help]`

Old text:

```
        if self.built or self.asked or not self.entry.extras_modules:
```

New text:

```
        if self.built or self.asked:
```

### `u248.L4_listing_drops_the_stub_line`

ask_for_listing: a missing extra no longer makes the stub, so the listing omits (requires the extra)

- File: `src/cratekit/cli/__init__.py`
- Source: `u248.json`, row `L4_listing_drops_the_stub_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_cli_lazy.py`
- Collected: 1181 against a baseline of 1181
- Kills: 2 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_module_with_missing_extras_becomes_a_stub_that_names_the_install_command`
  - `tests/test_cli_lazy.py::test_a_blocked_extra_still_lists_the_stub_line_and_refuses_with_the_install_command`

Old text:

```
            if _is_missing_extra(exc, self.entry):
                self._stub(exc)
```

New text:

```
            if _is_missing_extra(exc, self.entry):
                pass
```

### `u248.L5_listing_asked_twice`

ask_for_listing: forget it was asked, so one help screen imports the module twice

- File: `src/cratekit/cli/__init__.py`
- Source: `u248.json`, row `L5_listing_asked_twice`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cli_lazy.py`
- Collected: 161 against a baseline of 161
- Kills: 2 (killed)
- Killed:
  - `tests/test_cli_lazy.py::test_a_listing_asks_only_the_verbs_whose_line_could_differ`
  - `tests/test_cli_lazy.py::test_a_verb_is_built_once_however_often_it_is_asked`

Old text:

```
        self.asked = True
```

New text:

```
        self.asked = False
```

### `u248.L6_built_twice`

build: drop the built check, so a parser asked twice runs the builder twice and argparse refuses a duplicate option

- File: `src/cratekit/cli/__init__.py`
- Source: `u248.json`, row `L6_built_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_lazy.py`
- Collected: 161 against a baseline of 161
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_lazy.py::test_a_verb_is_built_once_however_often_it_is_asked`

Old text:

```
        if self.built:
            return
        try:
            try:
                module = self.importer(self.entry.module)
```

New text:

```
        try:
            try:
                module = self.importer(self.entry.module)
```

### `u248.L7_defect_as_stub`

build: treat every import error as a missing extra, so a defect of our own reads as install the extra

- File: `src/cratekit/cli/__init__.py`
- Source: `u248.json`, row `L7_defect_as_stub`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_cli_lazy.py`
- Collected: 1181 against a baseline of 1181
- Kills: 2 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_defect_in_our_own_module_does_not_masquerade_as_a_missing_extra`
  - `tests/test_cli_lazy.py::test_a_broken_module_fails_its_own_verb_and_leaves_every_other_one_working`

Old text:

```
                if not _is_missing_extra(exc, self.entry):
                    raise
                self._stub(exc)
                return
```

New text:

```
                self._stub(exc)
                return
```

### `u248.L8_listing_raises_a_defect`

ask_for_listing: let a non extra failure escape, so a broken module takes its whole group's help down

- File: `src/cratekit/cli/__init__.py`
- Source: `u248.json`, row `L8_listing_raises_a_defect`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_lazy.py`
- Collected: 161 against a baseline of 161
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_lazy.py::test_a_module_that_raises_anything_at_import_is_listed_plainly_and_raises_for_its_verb`

Old text:

```
        except Exception:  # noqa: BLE001 - see the docstring, the verb itself raises
            pass
```

New text:

```
        except Exception:  # noqa: BLE001 - see the docstring, the verb itself raises
            raise
```

### `u248.L9_argument_error_unwrapped`

build: let an ArgumentError from the import or the builder reach argparse, so a defect of ours exits 2 as the user's usage error

- File: `src/cratekit/cli/__init__.py`
- Source: `u248.json`, row `L9_argument_error_unwrapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_lazy.py`
- Collected: 161 against a baseline of 161
- Kills: 2 (killed)
- Killed:
  - `tests/test_cli_lazy.py::test_a_defective_builder_is_a_defect_and_never_a_usage_error`
  - `tests/test_cli_lazy.py::test_an_argument_error_raised_by_the_import_is_a_defect_too`

Old text:

```
        except argparse.ArgumentError as exc:
            raise RuntimeError(
```

New text:

```
        except ZeroDivisionError as exc:
            raise RuntimeError(
```

### `r235-a.M10_verb_guard_removed`

the revert verb no longer asks before the gate, leaving only the library's check after the approval

- File: `src/cratekit/cli/cutover.py`
- Source: `r235-a.json`, row `M10_verb_guard_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_a_revert_after_a_native_write_refuses_and_the_tree_stays_native`

Old text:

```
    tree_registry.assert_revertible(cfg, tree_id)
    item = {**_recorded(standing), "registry": str(tree_registry.path_for(cfg))}
```

New text:

```
    item = {**_recorded(standing), "registry": str(tree_registry.path_for(cfg))}
```

### `r235-b.M15_first_of_several_roots`

more than one root no longer refuses, the first is adopted

- File: `src/cratekit/cli/cutover.py`
- Source: `r235-b.json`, row `M15_first_of_several_roots`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_two_roots_of_one_name_are_refused`

Old text:

```
    if len(roots) == 1:
        return roots[0]
```

New text:

```
    if len(roots) >= 1:
        return roots[0]
```

### `r235-b.M16_native_tree_offered_again`

the verb no longer answers a tree already native before it asks

- File: `src/cratekit/cli/cutover.py`
- Source: `r235-b.json`, row `M16_native_tree_offered_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_a_tree_already_native_records_nothing_and_asks_nothing`
  - `tests/test_cutover_cli.py::test_two_cutovers_offered_before_either_was_approved_record_one`

Old text:

```
    if standing is not None and standing.mode == tree_registry.Mode.DATABASE:
        return ctx.envelope(
            data=_digested("tree.cutover", _recorded(standing), {"recorded": False}),
```

New text:

```
    if False:
        return ctx.envelope(
            data=_digested("tree.cutover", _recorded(standing), {"recorded": False}),
```

### `r235-b.M19_unready_library_asked`

a library that fails its precheck is offered the plan instead of being refused

- File: `src/cratekit/cli/cutover.py`
- Source: `r235-b.json`, row `M19_unready_library_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 6 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_an_empty_export_is_no_export`
  - `tests/test_cutover_cli.py::test_each_precheck_failure_refuses_before_anything_is_recorded[_leave_intake_xml-cutover-xml-pending-no-pending-intake-xml]`
  - `tests/test_cutover_cli.py::test_each_precheck_failure_refuses_before_anything_is_recorded[_open_a_run-cutover-open-run-no-open-run]`
  - `tests/test_cutover_cli.py::test_each_precheck_failure_refuses_before_anything_is_recorded[_remove_the_export-cutover-export-missing-fresh-export]`
  - `tests/test_cutover_cli.py::test_each_precheck_failure_refuses_before_anything_is_recorded[_remove_the_snapshot-cutover-snapshot-missing-verified-snapshot]`
  - `tests/test_cutover_cli.py::test_two_failing_prechecks_are_both_named_on_one_run`

Old text:

```
    results = tree_registry.cutover_precheck(cfg, export=export)
    _refuse_unready(results)
```

New text:

```
    results = tree_registry.cutover_precheck(cfg, export=export)
```

### `r235-b.M20_refusal_without_the_table`

the precheck refusal no longer carries every check's result

- File: `src/cratekit/cli/cutover.py`
- Source: `r235-b.json`, row `M20_refusal_without_the_table`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 5 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_each_precheck_failure_refuses_before_anything_is_recorded[_leave_intake_xml-cutover-xml-pending-no-pending-intake-xml]`
  - `tests/test_cutover_cli.py::test_each_precheck_failure_refuses_before_anything_is_recorded[_open_a_run-cutover-open-run-no-open-run]`
  - `tests/test_cutover_cli.py::test_each_precheck_failure_refuses_before_anything_is_recorded[_remove_the_export-cutover-export-missing-fresh-export]`
  - `tests/test_cutover_cli.py::test_each_precheck_failure_refuses_before_anything_is_recorded[_remove_the_snapshot-cutover-snapshot-missing-verified-snapshot]`
  - `tests/test_cutover_cli.py::test_two_failing_prechecks_are_both_named_on_one_run`

Old text:

```
                detail={**cause.detail, "precheck": _precheck_rows(results)},
```

New text:

```
                detail=dict(cause.detail),
```

### `r235-b.M21_digest_blind_to_the_plan`

the digest covers the kind of plan and not its item, so a root that changed leaves the approval standing

- File: `src/cratekit/cli/cutover.py`
- Source: `r235-b.json`, row `M21_digest_blind_to_the_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_a_root_that_changed_after_the_offer_makes_the_approval_stale`

Old text:

```
        "digest": digest_of({"kind": kind, "items": [item]}),
```

New text:

```
        "digest": digest_of({"kind": kind}),
```

### `r787.V1_verb_own_list`

derivation_source keeps a list of its own, the routing tree and intake tree spelled inline, instead of asking cutover_trees

- File: `src/cratekit/cli/cutover.py`
- Source: `r787.json`, row `V1_verb_own_list`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_doctor_and_the_verb_read_one_set_of_cutover_trees`

Old text:

```
    if tree_id in accepted:
        return tree_registry.DerivationSource.TAXONOMY
```

New text:

```
    if tree_id in (declared.tree.id, declared.intake.id):
        return tree_registry.DerivationSource.TAXONOMY
```

### `r787.V2_undeclared_step_routing_only`

the undeclared refusal's step names the routing tree alone rather than the set

- File: `src/cratekit/cli/cutover.py`
- Source: `r787.json`, row `V2_undeclared_step_routing_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_a_tree_the_taxonomy_does_not_declare_is_refused`

Old text:

```
            f"name a tree a cutover records, which this library declares as "
            f"{', '.join(repr(t) for t in named)}",
```

New text:

```
            f"name a tree a cutover records, which this library declares as "
            f"{declared.tree.id!r}",
```

### `r787.V3_catalogue_refusal_loses_set`

the catalogue refusal carries the registry's detail alone, without the set a cutover accepts

- File: `src/cratekit/cli/cutover.py`
- Source: `r787.json`, row `V3_catalogue_refusal_loses_set`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_the_catalogue_tree_is_refused_as_not_rebuildable`

Old text:

```
                detail={
                    **cause.detail,
                    "cutover_trees": sorted(tree_registry.cutover_trees(declared)),
                },
```

New text:

```
                detail={**cause.detail},
```

### `r1255.D2_status_names_the_log`

status _source_findings: never name an unlisted log, so a refused source reads as none in flight

- File: `src/cratekit/cli/doctor.py`
- Source: `r1255.json`, row `D2_status_names_the_log`
- Moved: U303 shortened the comment under the condition; status's unlisted log check in the doctor hub is unchanged in the same place
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_status_names_a_session_log_it_cannot_list_and_still_reports_the_rest`

Old text:

```
    if session.log_unlisted(unreadable, cfg):
        # A log nobody could list is reported, never read as no source in
```

New text:

```
    if False:
        # A log nobody could list is reported, never read as no source in
```

### `r1255.D3_status_guard_precise`

status _source_findings: name any unread entry as an unlisted log, so one damaged record hides every source

- File: `src/cratekit/cli/doctor.py`
- Source: `r1255.json`, row `D3_status_guard_precise`
- Moved: U303 shortened the comment under the condition; status's unlisted log check in the doctor hub is unchanged in the same place
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_status_reads_one_damaged_record_as_a_record_not_as_an_unlisted_log`

Old text:

```
    if session.log_unlisted(unreadable, cfg):
        # A log nobody could list is reported, never read as no source in
```

New text:

```
    if unreadable:
        # A log nobody could list is reported, never read as no source in
```

### `u184.D8_check_unlisted`

CHECKS: drop the new check, so doctor never shows the acknowledgment

- File: `src/cratekit/cli/doctor.py`
- Source: `u184.json`, row `D8_check_unlisted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 6 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_acknowledgment_that_cannot_be_understood_is_a_failure`
  - `tests/test_doctor.py::test_doctor_names_when_an_acknowledgment_lapsed`
  - `tests/test_doctor.py::test_doctor_says_when_no_acknowledgment_is_on_record`
  - `tests/test_doctor.py::test_doctor_shows_the_acknowledgments_expiry_beside_the_two_backup_ages`
  - `tests/test_doctor.py::test_every_check_key_and_its_place_in_the_run_order_is_written_out`
  - `tests/test_doctor.py::test_no_acknowledgment_is_claimed_absent_off_a_volume_nobody_read`

Old text:

```
    Check("backup.acknowledgment", _check_backup_acknowledgment),
```

New text:

```
(empty)
```

### `u303.D3_offered_ignores_required`

doctor.offered: a credential a switched on verb declares is not offered by setup

- File: `src/cratekit/cli/doctor.py`
- Source: `u303.json`, row `D3_offered_ignores_required`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 6 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_credential_offer_accepted_and_left_empty_is_the_same_note_as_a_no`
  - `tests/test_doctor.py::test_a_credential_offer_that_could_not_be_read_still_fails`
  - `tests/test_doctor.py::test_a_credential_that_cannot_be_read_and_one_that_cannot_be_stored_differ`
  - `tests/test_doctor.py::test_the_wizard_notes_an_index_that_refuses_the_write_rather_than_dying`
  - `tests/test_doctor.py::test_the_wizard_notes_an_unreadable_credential_index_rather_than_dying`
  - `tests/test_doctor.py::test_the_wizard_offers_every_credential_the_profile_needs_and_records_it`

Old text:

```
    if requires_check(key, membership):
```

New text:

```
    if False:
```

### `u303.D4_run_ignores_probes`

doctor.run: a caller's probes are dropped for the real machine's

- File: `src/cratekit/cli/doctor.py`
- Source: `u303.json`, row `D4_run_ignores_probes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_doctor.py`
- Collected: 1437 against a baseline of 1437
- Kills: 78 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_conformance_8_every_declared_precondition_can_pass_and_can_refuse`
  - `tests/test_doctor.py::test_a_backup_folder_that_cannot_be_read_is_said_as_unread_and_does_not_fail`
  - `tests/test_doctor.py::test_a_backup_folder_whose_stat_is_refused_is_unread_never_no_push`
  - `tests/test_doctor.py::test_a_backup_recorded_in_the_future_is_refused_rather_than_treated_as_fresh`
  - `tests/test_doctor.py::test_a_binary_that_is_simply_absent_still_says_install_it`
  - `tests/test_doctor.py::test_a_broken_trash_is_informational_when_no_verb_this_profile_needs_it`
  - `tests/test_doctor.py::test_a_clone_with_no_configuration_is_told_the_floor`
  - `tests/test_doctor.py::test_a_commit_hook_that_is_present_and_is_not_text_is_reported`
  - `tests/test_doctor.py::test_a_commit_msg_hook_installed_for_another_stage_is_refused`
  - `tests/test_doctor.py::test_a_commit_msg_hook_on_another_configuration_is_refused`
  - `tests/test_doctor.py::test_a_commondir_that_is_present_and_is_not_text_is_reported_too`
  - `tests/test_doctor.py::test_a_configuration_that_does_not_parse_is_not_read_as_one_hook_type`
  - `tests/test_doctor.py::test_a_configured_commit_msg_stage_with_no_hook_is_refused`
  - `tests/test_doctor.py::test_a_drifted_application_pin_is_a_different_answer_from_an_unset_one`
  - `tests/test_doctor.py::test_a_foreign_volume_at_the_configured_root_is_its_own_answer`
  - ... and 63 more, see the JSON sidecar

Old text:

```
    inputs = _Inputs(cfg, error, probes or Probes())
```

New text:

```
    inputs = _Inputs(cfg, error, Probes())
```

### `u328.S3_a_part_imported_past_the_registry`

cli/doctor.py imports a part's tuple directly, so its rows are read past cli.registry, where the suite patches the table

- File: `src/cratekit/cli/doctor.py`
- Source: `u328.json`, row `S3_a_part_imported_past_the_registry`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_import_rules.py::test_no_package_crosses_a_seam_beyond_its_allowance`

Old text:

```
from cratekit.cli import gates, output, registry, render

```

New text:

```
from cratekit.cli import gates, output, registry, render
from cratekit.cli.registry_later import LATER_VERBS  # noqa: F401

```

### `u184.D1_volume_not_established`

_check_backup_acknowledgment: read the record off a volume nobody established, so a missing disk reads as none on record

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u184.json`, row `D1_volume_not_established`
- Moved: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_no_acknowledgment_is_claimed_absent_off_a_volume_nobody_read`

Old text:

```
    unreadable = _library_state_unreadable(inputs, "the backup acknowledgment")
```

New text:

```
    unreadable = None
```

### `u184.D2_unreadable_is_a_note`

_check_backup_acknowledgment: report a record that cannot be understood as a note rather than a failure

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u184.json`, row `D2_unreadable_is_a_note`
- Moved: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_acknowledgment_that_cannot_be_understood_is_a_failure`

Old text:

```
            status=Status.FAIL,
            detail=(
                f"{exc.cause.message}. Every destructive verb refuses while the "
```

New text:

```
            status=Status.INFO,
            detail=(
                f"{exc.cause.message}. Every destructive verb refuses while the "
```

### `u184.D3_remedy_chosen_here`

_check_backup_acknowledgment: name a remedy chosen here instead of the reader's own

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u184.json`, row `D3_remedy_chosen_here`
- Moved: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_acknowledgment_that_cannot_be_understood_is_a_failure`

Old text:

```
            remedy=exc.cause.remediation.remedy,
        )
    if recorded is None:
```

New text:

```
            remedy=Remedy.ACKNOWLEDGE_BACKUP,
        )
    if recorded is None:
```

### `u184.D4_expired_read_as_valid`

_check_backup_acknowledgment: drop the expired branch, so a lapsed record reads as valid with time left

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u184.json`, row `D4_expired_read_as_valid`
- Moved: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_doctor_names_when_an_acknowledgment_lapsed`

Old text:

```
    if not recorded.valid_at(now):
```

New text:

```
    if False:
```

### `u184.D5_wall_clock`

_check_backup_acknowledgment: read the wall clock rather than the run's own instant

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u184.json`, row `D5_wall_clock`
- Moved: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_doctor_shows_the_acknowledgments_expiry_beside_the_two_backup_ages`

Old text:

```
    now = inputs.probes.now
    expires = recorded.expires_at.replace(microsecond=0).isoformat()
```

New text:

```
    now = datetime.now(timezone.utc)
    expires = recorded.expires_at.replace(microsecond=0).isoformat()
```

### `u184.D6_hours_coefficient`

_check_backup_acknowledgment: halve the minutes per hour, so the time left is misstated

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u184.json`, row `D6_hours_coefficient`
- Moved: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_doctor_shows_the_acknowledgments_expiry_beside_the_two_backup_ages`

Old text:

```
    hours, minutes = divmod(int(left.total_seconds()) // 60, 60)
```

New text:

```
    hours, minutes = divmod(int(left.total_seconds()) // 60, 30)
```

### `u184.D7_rule_not_named`

_check_backup_acknowledgment: name the terminal rule whatever minted the record

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u184.json`, row `D7_rule_not_named`
- Moved: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_doctor_shows_the_acknowledgments_expiry_beside_the_two_backup_ages`

Old text:

```
            f"the {recorded.rule} rule"
```

New text:

```
            f"the terminal rule"
```

### `u185.D1_push_newer_warns`

deadca7.push: invert the comparison, so a push after the last backup reads as held by it

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u185.json`, row `D1_push_newer_warns`
- Moved: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_push_newer_than_the_last_database_backup_warns_and_names_the_backup`
  - `tests/test_doctor.py::test_a_push_older_than_the_last_database_backup_is_held_by_it`

Old text:

```
    if completed is not None and pushed > completed:
```

New text:

```
    if completed is not None and pushed < completed:
```

### `u185.D2_hidden_entries`

deadca7.push: count hidden entries, so a .DS_Store reads as a push

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u185.json`, row `D2_hidden_entries`
- Moved: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 4 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_push_older_than_the_last_database_backup_is_held_by_it`
  - `tests/test_doctor.py::test_installed_with_an_empty_backup_folder_says_the_location_is_unconfirmed`
  - `tests/test_doctor.py::test_installed_with_no_push_says_so`
  - `tests/test_doctor.py::test_with_its_support_folder_here_the_install_signals_are_not_asked`

Old text:

```
        entry.stat().st_mtime for entry in folder.iterdir() if not entry.name.startswith(".")
```

New text:

```
        entry.stat().st_mtime for entry in folder.iterdir()
```

### `u185.D3_unread_folder`

deadca7.push: let an unreadable backup folder escape, so the check fails the report

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u185.json`, row `D3_unread_folder`
- Moved: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_backup_folder_that_cannot_be_read_is_said_as_unread_and_does_not_fail`
  - `tests/test_doctor.py::test_a_backup_folder_whose_stat_is_refused_is_unread_never_no_push`

Old text:

```
    except OSError as exc:
        # Unread is not none
```

New text:

```
    except ZeroDivisionError as exc:
        # Unread is not none
```

### `u224.M10_refused_backups_read_no_push`

_check_deadca7_push: a backup folder whose stat is refused reads as absent, so no push

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u224.json`, row `M10_refused_backups_read_no_push`
- Moved: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_backup_folder_whose_stat_is_refused_is_unread_never_no_push`

Old text:

```
        if isinstance(presence, OSError):
            raise presence
```

New text:

```
        if isinstance(presence, OSError):
            presence = False
```

### `u224.M1_found_ignored`

_deadca7_presence: never count a present install place as found, so a bundle reads not installed again

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u224.json`, row `M1_found_ignored`
- Moved: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 7 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_probe_that_raises_beside_a_present_bundle_still_reads_installed`
  - `tests/test_doctor.py::test_a_real_probes_value_asks_the_installed_probe`
  - `tests/test_doctor.py::test_installed_with_its_support_folder_unread_says_its_push_cannot_be_said`
  - `tests/test_doctor.py::test_installed_with_no_home_to_resolve_says_where_its_backups_land_is_unconfirmed`
  - `tests/test_doctor.py::test_one_installed_place_alone_reads_installed_with_no_push[the-accounts-own-applications-folder]`
  - `tests/test_doctor.py::test_one_installed_place_alone_reads_installed_with_no_push[the-state-folder-alone]`
  - `tests/test_doctor.py::test_sitting_68s_mac_the_bundle_and_no_support_folder_reads_installed_with_no_push`

Old text:

```
            elif state:
                found.append(place)
```

New text:

```
            elif False:
                found.append(place)
```

### `u224.M2_unread_place_dropped`

_deadca7_presence: drop an install place the account cannot stat, so it reads absent

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u224.json`, row `M2_unread_place_dropped`
- Moved: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_install_signal_that_cannot_be_read_is_unread_never_not_installed`

Old text:

```
                unread.append(f"{place} could not be read ({_said(state)})")
```

New text:

```
                pass
```

### `u224.M3_broken_installed_probe_silent`

_deadca7_presence: an install probe that raises adds nothing, so it reads not installed

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u224.json`, row `M3_broken_installed_probe_silent`
- Moved: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_probe_that_raises_reads_unread_rather_than_not_installed[deadca7_installed]`

Old text:

```
            unread.append(f"where its app is installed could not be located ({_said(exc)})")
```

New text:

```
            pass
```

### `u224.M4_unread_support_read_absent`

_deadca7_presence: a support folder whose stat is refused answers absent, so an installed app reads no push

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u224.json`, row `M4_unread_support_read_absent`
- Moved: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_installed_with_its_support_folder_unread_says_its_push_cannot_be_said`

Old text:

```
            support = None
            unread.append(f"{home} could not be read
```

New text:

```
            support = False
            unread.append(f"{home} could not be read
```

### `u224.M5_refused_stat_read_absent`

_folder_presence: any refused stat answers absent, the Path.is_dir shape on later Pythons

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u224.json`, row `M5_refused_stat_read_absent`
- Moved: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 4 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_backup_folder_whose_stat_is_refused_is_unread_never_no_push`
  - `tests/test_doctor.py::test_a_support_folder_that_cannot_be_read_is_unread_never_not_installed`
  - `tests/test_doctor.py::test_an_install_signal_that_cannot_be_read_is_unread_never_not_installed`
  - `tests/test_doctor.py::test_installed_with_its_support_folder_unread_says_its_push_cannot_be_said`

Old text:

```
    except OSError as exc:
        return exc
    return stat.S_ISDIR(mode)
```

New text:

```
    except OSError as exc:
        return False
    return stat.S_ISDIR(mode)
```

### `u224.M6_unread_folded_into_not_installed`

_check_deadca7_push: nothing found and something unread reads not installed

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u224.json`, row `M6_unread_folded_into_not_installed`
- Moved: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 4 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_probe_that_raises_reads_unread_rather_than_not_installed[deadca7_home]`
  - `tests/test_doctor.py::test_a_probe_that_raises_reads_unread_rather_than_not_installed[deadca7_installed]`
  - `tests/test_doctor.py::test_a_support_folder_that_cannot_be_read_is_unread_never_not_installed`
  - `tests/test_doctor.py::test_an_install_signal_that_cannot_be_read_is_unread_never_not_installed`

Old text:

```
        if unread:
            return said("whether DEADCA7 is installed here cannot be said: "
```

New text:

```
        if False:
            return said("whether DEADCA7 is installed here cannot be said: "
```

### `u224.M7_install_signals_always_asked`

_deadca7_presence: ask the install signals even with the support folder here

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u224.json`, row `M7_install_signals_always_asked`
- Moved: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_with_its_support_folder_here_the_install_signals_are_not_asked`

Old text:

```
    if not support:
        try:
            places = tuple(probes.deadca7_installed())
```

New text:

```
    if True:
        try:
            places = tuple(probes.deadca7_installed())
```

### `u224.M9_path_through_a_file_unread`

_folder_presence: a stat through a file reads unread rather than absent

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u224.json`, row `M9_path_through_a_file_unread`
- Moved: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_install_place_reached_through_a_file_is_absent_not_unread`

Old text:

```
    except (FileNotFoundError, NotADirectoryError):
        return False
    except OSError as exc:
        return exc
```

New text:

```
    except FileNotFoundError:
        return False
    except OSError as exc:
        return exc
```

### `u263.D21_doctor_names_verbs`

doctor: drop the verbs from a failing binary row

- File: `src/cratekit/cli/doctor_keys.py`
- Source: `u263.json`, row `D21_doctor_names_verbs`
- Moved: the same text, now in src/cratekit/cli/doctor_keys.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_missing_ffmpeg_names_the_analysis_whose_decoder_it_is`

Old text:

```
            f"{', '.join(inputs.requiring(key))} ({source}; override with {override})"
```

New text:

```
            f"({source}; override with {override})"
```

### `u97-b.B1_doctor_routes_the_wrong_credential_token`

doctor _CREDENTIAL_REMEDY: answer the provider check with SET_CREDENTIAL, the recognition token, so the report tells a person to paste a key they cannot have

- File: `src/cratekit/cli/doctor_keys.py`
- Source: `u97-b.json`, row `B1_doctor_routes_the_wrong_credential_token`
- Moved: the same text, now in src/cratekit/cli/doctor_keys.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_missing_provider_session_is_offered_the_procedure_and_not_the_bare_verb`

Old text:

```
        "credential.provider": Remedy.AUTHENTICATE_PROVIDER,
```

New text:

```
        "credential.provider": Remedy.SET_CREDENTIAL,
```

### `u132.D1_doctor_behind`

Doctor reads a copy behind the shipped schema as OK

- File: `src/cratekit/cli/doctor_library.py`
- Source: `u132.json`, row `D1_doctor_behind`
- Moved: the same text, now in src/cratekit/cli/doctor_library.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_current_copy_with_every_entry_is_ok`
  - `tests/test_doctor.py::test_a_version_2_copy_without_favorites_is_named_with_both_versions`

Old text:

```
    if not found.behind:

```

New text:

```
    if found.behind:

```

### `u132.D2_doctor_defect`

Doctor reports a shipped template defect as the copy not compared

- File: `src/cratekit/cli/doctor_library.py`
- Source: `u132.json`, row `D2_doctor_defect`
- Moved: the same text, now in src/cratekit/cli/doctor_library.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_shipped_template_that_does_not_load_is_a_defect_and_not_the_copy`

Old text:

```
        if exc.cause.reason == "internal-error":

```

New text:

```
        if False:

```

### `u27-reports-round-1.D2_required_gate`

Report a broken Trash as a failure even where no verb needs it

- File: `src/cratekit/cli/doctor_library.py`
- Source: `u27-reports-round-1.json`, row `D2_required_gate`
- Moved: the same text, now in src/cratekit/cli/doctor_library.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_broken_trash_is_informational_when_no_verb_this_profile_needs_it`

Old text:

```
    if not inputs.required(key):
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"{status.problem}, and no verb this profile switches on moves a "
                f"file to the Trash, so nothing depends on it today"
            ),
        )

```

New text:

```
(empty)
```

### `u27-reports-round-1.D3_trash_remedy`

Answer a broken Trash with run-doctor, which is the token that sends a person here

- File: `src/cratekit/cli/doctor_library.py`
- Source: `u27-reports-round-1.json`, row `D3_trash_remedy`
- Moved: U303 split cli/doctor.py and moved the trash probe's finding, verbatim but for its comment, to cli/doctor_library.py; the remedy is the same value, swapped the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_volume_with_no_usable_trash_refuses_because_a_verb_depends_on_it`

Old text:

```
        # are a path to grant; another filesystem is named in the sentence.
        remedy=Remedy.GRANT_PATH_ACCESS,
```

New text:

```
        # are a path to grant; another filesystem is named in the sentence.
        remedy=Remedy.RUN_DOCTOR,
```

### `u27-reports-round-3-fixes.F3_trash_absent_is_a_failure`

Report a volume whose Trash has not been created yet as a failure again

- File: `src/cratekit/cli/doctor_library.py`
- Source: `u27-reports-round-3-fixes.json`, row `F3_trash_absent_is_a_failure`
- Moved: the same text, now in src/cratekit/cli/doctor_library.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_volume_with_no_trash_directory_yet_is_not_a_failure`

Old text:

```
    if status.absent:
```

New text:

```
    if False:
```

### `u27-round-8-independent.E1_mount_detail_swapped`

Swap the NOT_MOUNTED and MOUNTED_ELSEWHERE sentences, conflating unmounted with moved

- File: `src/cratekit/cli/doctor_library.py`
- Source: `u27-round-8-independent.json`, row `E1_mount_detail_swapped`
- Moved: the same text, now in src/cratekit/cli/doctor_library.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_unmounted_volume_and_a_moved_volume_produce_different_messages`

Old text:

```
        preflight.MountState.NOT_MOUNTED: (
            "the recorded volume is not mounted anywhere and the configured root "
            "does not exist. Attach it"
        ),
        preflight.MountState.MOUNTED_ELSEWHERE: (
            "the recorded volume IS attached, at a different mount point than the "
            "configured root. Nothing needs plugging in; the configured root is "
            "pointing at the wrong place"
        ),
```

New text:

```
        preflight.MountState.NOT_MOUNTED: (
            "the recorded volume IS attached, at a different mount point than the "
            "configured root. Nothing needs plugging in; the configured root is "
            "pointing at the wrong place"
        ),
        preflight.MountState.MOUNTED_ELSEWHERE: (
            "the recorded volume is not mounted anywhere and the configured root "
            "does not exist. Attach it"
        ),
```

### `u27-round-8-independent.E2_identity_verdict_green`

Report the identity check GREEN for an absent and for a relocated volume

- File: `src/cratekit/cli/doctor_library.py`
- Source: `u27-round-8-independent.json`, row `E2_identity_verdict_green`
- Moved: the same text, now in src/cratekit/cli/doctor_library.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 3 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_volume_mounted_elsewhere_is_one_problem_reported_once`
  - `tests/test_doctor.py::test_an_unmounted_volume_never_reports_a_matching_identity`
  - `tests/test_doctor.py::test_the_identity_check_never_reports_green_over_an_identity_that_did_not_match`

Old text:

```
            preflight.MountState.NOT_MOUNTED: (Status.INFO, None),
            preflight.MountState.MOUNTED_ELSEWHERE: (Status.INFO, None),
```

New text:

```
            preflight.MountState.NOT_MOUNTED: (Status.OK, None),
            preflight.MountState.MOUNTED_ELSEWHERE: (Status.OK, None),
```

### `u27-round-8-independent.E3_found_at_dropped`

Stop telling the user where a relocated volume actually is

- File: `src/cratekit/cli/doctor_library.py`
- Source: `u27-round-8-independent.json`, row `E3_found_at_dropped`
- Moved: the same text, now in src/cratekit/cli/doctor_library.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_unmounted_volume_and_a_moved_volume_produce_different_messages`

Old text:

```
    if status.state is preflight.MountState.MOUNTED_ELSEWHERE:
        where = f" (configured root {status.configured_root}, found at {status.found_at})"
```

New text:

```
(empty)
```

### `u159.M10_unread_reads_none_published`

_release_tags: a refused read answers no tags, so doctor says none is published

- File: `src/cratekit/cli/doctor_model.py`
- Source: `u159.json`, row `M10_unread_reads_none_published`
- Moved: the same text, now in src/cratekit/cli/doctor_model.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_release_read_parses_ls_remote_and_refuses_on_failure`

Old text:

```
    if done.returncode != 0:
        return None
    tags = []
```

New text:

```
    if done.returncode != 0:
        return ()
    tags = []
```

### `u181.D7_scored_probe_false`

doctor _vocals_scored: never see the recorded calibration

- File: `src/cratekit/cli/doctor_model.py`
- Source: `u181.json`, row `D7_scored_probe_false`
- Moved: the same text, now in src/cratekit/cli/doctor_model.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_library_has_scored_when_a_vocal_calibration_is_recorded`

Old text:

```
    return config.state_path(metadata_cli.STATE_KEY_VOCAL_CALIBRATION, cfg).is_file()
```

New text:

```
    return False
```

### `u224.M8_default_probe_empty`

Probes: the install probe's default answers nothing, the regression that re-creates the bug

- File: `src/cratekit/cli/doctor_model.py`
- Source: `u224.json`, row `M8_default_probe_empty`
- Moved: the same text, now in src/cratekit/cli/doctor_model.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_real_probes_value_asks_the_installed_probe`

Old text:

```
    deadca7_installed: Callable[[], tuple[Path, ...]] = _deadca7_installed
```

New text:

```
    deadca7_installed: Callable[[], tuple[Path, ...]] = lambda: ()
```

### `u27-reports-round-2.D1_probe_creates`

Round 1 zero, re-run against the replacement guard: take the creating default

- File: `src/cratekit/cli/doctor_model.py`
- Source: `u27-reports-round-2.json`, row `D1_probe_creates`
- Moved: the same text, now in src/cratekit/cli/doctor_model.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_trash_check_cannot_pass_by_having_run`

Old text:

```
    return trash.probe(path, create=False)
```

New text:

```
    return trash.probe(path, create=True)
```

### `r-1.E1_dispatch_impl`

Existing guard, sample: drop the requirement that the hook invokes hook-impl

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `E1_dispatch_impl`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_hook_that_does_not_dispatch_to_this_repository_is_refused[#!/bin/sh\n# pre-commit\nexit 0\n-True-hook-impl]`

Old text:

```
    if _HOOK_DISPATCH not in body:
        return f"it never invokes pre-commit's {_HOOK_DISPATCH}"

```

New text:

```
(empty)
```

### `r-1.E2_config_inside_checkout`

Existing guard, sample: drop the requirement that the named configuration is inside the checkout

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `E2_config_inside_checkout`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_hook_that_does_not_dispatch_to_this_repository_is_refused[ARGS=(hook-impl --config=/elsewhere/.pre-commit-config.yaml --hook-type=pre-commit)\n-True-outside]`

Old text:

```
    if root.resolve() not in resolved.parents and resolved != root.resolve():
```

New text:

```
    if False:
```

### `r-1.T10_no_yaml_falls_back`

PyYAML missing falls back to the pre-commit floor instead of a sentence

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T10_no_yaml_falls_back`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_no_yaml_reader_is_unknown_rather_than_one_hook_type`

Old text:

```
    except ImportError:
        return (
            (),
            (
                f"PyYAML is not importable from this interpreter, so the hook types "
                f"{config_file.name} configures could not be read. Install the dev "
                f"extra, `pip install -e '.[dev]'`"
            ),
            None,
        )

```

New text:

```
    except ImportError:
        return ("pre-commit",), None, None

```

### `r-1.T12_caller_ignores_unknown`

The check ignores an unknown configuration and reports on no extra types

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T12_caller_ignores_unknown`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_configuration_that_does_not_parse_is_not_read_as_one_hook_type`
  - `tests/test_doctor.py::test_no_yaml_reader_is_unknown_rather_than_one_hook_type`

Old text:

```
    if unknown is not None:
```

New text:

```
    if False:
```

### `r-1.T13_missing_other_hook`

A configured hook type with no hook file is not reported

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T13_missing_other_hook`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_configured_commit_msg_stage_with_no_hook_is_refused`
  - `tests/test_doctor.py::test_the_install_line_names_a_configuration_that_is_not_the_default`

Old text:

```
            absent.append(f"no {hook_type} hook at {other}")
            continue

```

New text:

```
            continue

```

### `r-1.T15_other_dispatch`

A configured hook that does not dispatch for its own stage is not reported

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T15_other_dispatch`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_commit_msg_hook_installed_for_another_stage_is_refused`

Old text:

```
        if other_problem is not None:
            absent.append(

```

New text:

```
        if other_problem is not None:
            continue
            absent.append(

```

### `r-1.T16_same_configuration`

Drop the requirement that every other hook dispatches to the pre-commit hook's configuration

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T16_same_configuration`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_commit_msg_hook_on_another_configuration_is_refused`

Old text:

```
        if _config_path(other_name, root).resolve() != config_file.resolve():
```

New text:

```
        if False:
```

### `r-1.T17_install_config_flag`

The install line never names a non-default configuration

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T17_install_config_flag`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_install_line_names_a_configuration_that_is_not_the_default`

Old text:

```
    if config_name != _HOOK_CONFIG_DEFAULT:
```

New text:

```
    if False:
```

### `r-1.T18_remedy_floor`

With no readable configuration the install line names no type at all

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T18_remedy_floor`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_clone_with_no_configuration_is_told_the_floor`

Old text:

```
    return _install_command(types if problem is None else ("pre-commit",))
```

New text:

```
    return _install_command(types)
```

### `r-1.T19_remedy_reads_config`

The fresh clone install line stops reading the configuration and names only pre-commit

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T19_remedy_reads_config`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_fresh_clone_is_told_the_whole_install_line`

Old text:

```
    types, problem, _remedy = _configured_hook_types(root / _HOOK_CONFIG_DEFAULT)
```

New text:

```
    types, problem, _remedy = ("pre-commit",), None, None
```

### `r-1.T1_manual_skip`

Stop skipping the manual stage, so a manual-only hook reads as an unknown stage

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T1_manual_skip`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[text5-expected5]`

Old text:

```
        if hook_type == "manual":  # run by hand, never by git
            continue

```

New text:

```
(empty)
```

### `r-1.T20_stage_parameter`

The dispatch check ignores the hook type it was asked about and always wants pre-commit

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T20_stage_parameter`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 3 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_commit_msg_hook_installed_for_another_stage_is_refused`
  - `tests/test_doctor.py::test_a_commit_msg_hook_on_another_configuration_is_refused`
  - `tests/test_doctor.py::test_every_configured_hook_type_installed_passes_the_check`

Old text:

```
    stage = f"--hook-type={hook_type}"
```

New text:

```
    stage = "--hook-type=pre-commit"
```

### `r-1.T21_ok_names_others`

The OK detail stops naming the other stages it verified

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T21_ok_names_others`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_every_configured_hook_type_installed_passes_the_check`

Old text:

```
        if len(types) > 1

```

New text:

```
        if False

```

### `r-1.T22_pre_commit_floor`

Pre-commit is no longer the floor of the needed types

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T22_pre_commit_floor`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 13 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_commit_msg_hook_installed_for_another_stage_is_refused`
  - `tests/test_doctor.py::test_a_commit_msg_hook_on_another_configuration_is_refused`
  - `tests/test_doctor.py::test_a_configured_commit_msg_stage_with_no_hook_is_refused`
  - `tests/test_doctor.py::test_a_fresh_clone_is_told_the_whole_install_line`
  - `tests/test_doctor.py::test_every_configured_hook_type_installed_passes_the_check`
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[default_install_hook_types: [pre-push]\nrepos: []\n-expected2]`
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[default_stages: [push]\nrepos: []\n-expected3]`
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[repos: []\n-expected0]`
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[text1-expected1]`
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[text5-expected5]`
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[text6-expected6]`
  - `tests/test_doctor.py::test_the_install_line_names_a_configuration_that_is_not_the_default`
  - `tests/test_doctor.py::test_this_repositorys_own_configuration_needs_both_hook_types`

Old text:

```
    types = ["pre-commit"]
    for stage in named:

```

New text:

```
    types = []
    for stage in named:

```

### `r-1.T23_alias_value`

Map merge-commit to a realistic nearby wrong hook, pre-commit

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T23_alias_value`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[text4-expected4]`

Old text:

```
"merge-commit": "pre-merge-commit"
```

New text:

```
"merge-commit": "pre-commit"
```

### `r-1.T2_alias_map`

Stop mapping the legacy stage spellings (commit, push, merge-commit) to their hook types

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T2_alias_map`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[default_stages: [push]\nrepos: []\n-expected3]`
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[text4-expected4]`

Old text:

```
hook_type = _STAGE_ALIASES.get(stage, stage) if isinstance(stage, str) else None
```

New text:

```
hook_type = stage if isinstance(stage, str) else None
```

### `r-1.T3_default_install_types`

Ignore default_install_hook_types when deriving the needed hook types

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T3_default_install_types`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[default_install_hook_types: [pre-push]\nrepos: []\n-expected2]`

Old text:

```
    named.extend(document.get("default_install_hook_types") or [])

```

New text:

```
(empty)
```

### `r-1.T4_default_stages`

Ignore default_stages when deriving the needed hook types

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T4_default_stages`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[default_stages: [push]\nrepos: []\n-expected3]`

Old text:

```
    named.extend(document.get("default_stages") or [])

```

New text:

```
(empty)
```

### `r-1.T5_hook_stages`

Ignore every hook's own stages, the reading that finds this repository's commit-msg stage

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T5_hook_stages`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 12 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_commit_msg_hook_installed_for_another_stage_is_refused`
  - `tests/test_doctor.py::test_a_commit_msg_hook_on_another_configuration_is_refused`
  - `tests/test_doctor.py::test_a_configuration_this_cannot_understand_is_a_sentence[text0-'on-commit']`
  - `tests/test_doctor.py::test_a_configuration_this_cannot_understand_is_a_sentence[text1-installs no hook for]`
  - `tests/test_doctor.py::test_a_configured_commit_msg_stage_with_no_hook_is_refused`
  - `tests/test_doctor.py::test_a_fresh_clone_is_told_the_whole_install_line`
  - `tests/test_doctor.py::test_every_configured_hook_type_installed_passes_the_check`
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[text1-expected1]`
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[text4-expected4]`
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[text6-expected6]`
  - `tests/test_doctor.py::test_the_install_line_names_a_configuration_that_is_not_the_default`
  - `tests/test_doctor.py::test_this_repositorys_own_configuration_needs_both_hook_types`

Old text:

```
                named.extend(hook.get("stages") or [])
```

New text:

```
                pass
```

### `r-1.T6_unknown_stage`

Skip an unknown stage instead of refusing the configuration

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T6_unknown_stage`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_configuration_this_cannot_understand_is_a_sentence[text0-'on-commit']`
  - `tests/test_doctor.py::test_a_configuration_this_cannot_understand_is_a_sentence[text1-installs no hook for]`

Old text:

```
        if hook_type not in _HOOK_TYPES:
            return (
                (),
                f"{config_file} names a stage pre-commit installs no hook for, {stage!r}",
                None,
            )

```

New text:

```
        if hook_type not in _HOOK_TYPES:
            continue

```

### `r-1.T7_dedupe`

Append a type every time it is named rather than once

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T7_dedupe`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[text4-expected4]`
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[text6-expected6]`

Old text:

```
        if hook_type not in types:
            types.append(hook_type)

```

New text:

```
        types.append(hook_type)

```

### `r-1.T8_not_a_mapping`

Drop the guard refusing a configuration whose top level is not a mapping

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T8_not_a_mapping`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_configuration_this_cannot_understand_is_a_sentence[- just\n- a list\n-is not a pre-commit configuration]`

Old text:

```
    if not isinstance(document, dict):
        return (), f"{config_file} is not a pre-commit configuration", None

```

New text:

```
(empty)
```

### `r-1.T9_yaml_error_falls_back`

A configuration that does not parse falls back to the pre-commit floor instead of a sentence

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T9_yaml_error_falls_back`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_configuration_that_does_not_parse_is_not_read_as_one_hook_type`

Old text:

```
    except yaml.YAMLError as exc:
        return (), f"{config_file} is not valid YAML ({exc})", None

```

New text:

```
    except yaml.YAMLError:
        return ("pre-commit",), None, None

```

### `r1255.D1_doctor_branches_on_the_scan`

doctor _check_unresolved_session: never branch on the listing, so the log directory is named as an unreadable record

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r1255.json`, row `D1_doctor_branches_on_the_scan`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_session_log_this_account_cannot_list_is_failed_by_its_own_check`

Old text:

```
    if session.log_unlisted(unreadable, inputs.cfg):
        unreadable_directory = session.log_dir(inputs.cfg)
```

New text:

```
    if False:
        unreadable_directory = session.log_dir(inputs.cfg)
```

### `r598-b.B6_doctor_clause_dropped`

_open_state: list an orphaned record bare, so it reads as a run in progress with no verb named

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r598-b.json`, row `B6_doctor_clause_dropped`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_open_session_whose_process_is_gone_names_the_verb_that_ends_it`

Old text:

```
    if session.orphaned(record):
        return f"{record.state}, its process is gone, crate session release abandons it"
```

New text:

```
    if False:
        return f"{record.state}, its process is gone, crate session release abandons it"
```

### `r787.D1_doctor_own_list`

doctor's _declared_trees keeps a list of its own, the routing tree alone, instead of asking cutover_trees

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r787.json`, row `D1_doctor_own_list`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 4 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_doctor_and_the_verb_read_one_set_of_cutover_trees`
  - `tests/test_cutover_cli.py::test_doctor_fails_on_a_native_record_the_cutover_would_refuse_to_create`
  - `tests/test_cutover_cli.py::test_doctor_reads_a_native_inbox_record_as_ok`
  - `tests/test_cutover_cli.py::test_doctor_reads_an_inbox_the_verb_cut_over_as_ok`

Old text:

```
    return tuple(named), tree_registry.cutover_trees(declared), None
```

New text:

```
    return tuple(named), frozenset({declared.tree.id}), None
```

### `r787.D2_set_guard_removed`

doctor stops judging a native record by the set, so a native catalogue tree reads ok

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r787.json`, row `D2_set_guard_removed`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_doctor_lists_and_fails_a_recorded_tree_the_taxonomy_does_not_declare`

Old text:

```
            tree_id not in may_cut_over or record.source not in tree_registry.REBUILDABLE
```

New text:

```
            record.source not in tree_registry.REBUILDABLE
```

### `r787.D3_source_guard_removed`

doctor stops judging a native record by its source, so a native inbox from a catalogue crawl reads ok

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r787.json`, row `D3_source_guard_removed`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_doctor_fails_a_native_inbox_whose_source_no_rebuild_reproduces`

Old text:

```
            tree_id not in may_cut_over or record.source not in tree_registry.REBUILDABLE
```

New text:

```
            tree_id not in may_cut_over
```

### `u159.M8_behind_reads_current`

_check_release: any parseable installed version passes, so a copy behind reads as current

- File: `src/cratekit/cli/doctor_state.py`
- Source: `u159.json`, row `M8_behind_reads_current`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 4 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_newer_release_warns_with_the_one_pipx_command_keeping_the_extras`
  - `tests/test_doctor.py::test_a_newer_release_without_extras_names_plain_cratekit`
  - `tests/test_doctor.py::test_an_upgrade_keeps_the_extras_and_adds_vocals_only_for_a_scored_library[never-scored-adds-nothing]`
  - `tests/test_doctor.py::test_an_upgrade_keeps_the_extras_and_adds_vocals_only_for_a_scored_library[scored-adds-vocals]`

Old text:

```
    if installed >= newest:
```

New text:

```
    if True:
```

### `u181.D1_extras_row_never_ok`

doctor install.extras: never report ok, so a copy whose model scores is told the extra is absent

- File: `src/cratekit/cli/doctor_state.py`
- Source: `u181.json`, row `D1_extras_row_never_ok`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_copy_whose_vocal_model_can_score_is_ok`
  - `tests/test_doctor.py::test_the_row_reads_the_vocals_modules_own_probe_with_the_loader_bound_or_not`

Old text:

```
    missing = inputs.probes.vocal_requirement()
    if missing is None:
```

New text:

```
    missing = inputs.probes.vocal_requirement() or ("extra", "forced")
    if missing is None:
```

### `u181.D2_files_offered_reinstall`

doctor install.extras: treat missing model files as the extra, so a reinstall that places nothing is printed

- File: `src/cratekit/cli/doctor_state.py`
- Source: `u181.json`, row `D2_files_offered_reinstall`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_missing_model_files_are_named_and_no_reinstall_is_offered_for_them`

Old text:

```
    if kind != vocal_scoring.MISSING_EXTRA:
```

New text:

```
    if False:
```

### `u181.D3_release_form_dropped`

doctor vocals_install_command: ignore a release install, so the command is the folder or pip form

- File: `src/cratekit/cli/doctor_state.py`
- Source: `u181.json`, row `D3_release_form_dropped`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 3 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_copy_without_the_vocals_extra_says_so_and_prints_the_reinstall_command`
  - `tests/test_doctor.py::test_a_git_install_of_a_branch_head_names_no_tag_that_does_not_exist`
  - `tests/test_doctor.py::test_the_row_reads_the_vocals_modules_own_probe_with_the_loader_bound_or_not`

Old text:

```
    if origin.kind == "vcs" and origin.url and origin.version and _is_release(origin.version):
        extras = sorted({*origin.extras, VOCALS_EXTRA})
```

New text:

```
    if False:
        extras = sorted({*origin.extras, VOCALS_EXTRA})
```

### `u181.D4_release_form_no_vocals`

doctor vocals_install_command: the release form keeps the extras and does not add vocals

- File: `src/cratekit/cli/doctor_state.py`
- Source: `u181.json`, row `D4_release_form_no_vocals`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_copy_without_the_vocals_extra_says_so_and_prints_the_reinstall_command`
  - `tests/test_doctor.py::test_the_row_reads_the_vocals_modules_own_probe_with_the_loader_bound_or_not`

Old text:

```
        extras = sorted({*origin.extras, VOCALS_EXTRA})
```

New text:

```
        extras = sorted({*origin.extras})
```

### `u181.D5_upgrade_never_adds_vocals`

doctor _kept: the upgrade command never adds vocals, so a scored library upgrades without it

- File: `src/cratekit/cli/doctor_state.py`
- Source: `u181.json`, row `D5_upgrade_never_adds_vocals`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_upgrade_keeps_the_extras_and_adds_vocals_only_for_a_scored_library[scored-adds-vocals]`

Old text:

```
    if VOCALS_EXTRA in origin.extras or not inputs.probes.vocals_scored(inputs.cfg):
```

New text:

```
    if True:
```

### `u181.D6_upgrade_always_adds_vocals`

doctor _kept: the upgrade command adds vocals for a library never scored

- File: `src/cratekit/cli/doctor_state.py`
- Source: `u181.json`, row `D6_upgrade_always_adds_vocals`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_newer_release_without_extras_names_plain_cratekit`
  - `tests/test_doctor.py::test_an_upgrade_keeps_the_extras_and_adds_vocals_only_for_a_scored_library[never-scored-adds-nothing]`

Old text:

```
    if VOCALS_EXTRA in origin.extras or not inputs.probes.vocals_scored(inputs.cfg):
```

New text:

```
    if VOCALS_EXTRA in origin.extras:
```

### `u186.N1_note_age`

doctor: the note's age halved to twelve hours, so a gate open twenty hours is listed

- File: `src/cratekit/cli/doctor_state.py`
- Source: `u186.json`, row `N1_note_age`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_doctor_leaves_a_gate_open_twenty_hours_off_the_list`

Old text:

```
OPEN_GATE_NOTE_AGE = timedelta(days=1)
```

New text:

```
OPEN_GATE_NOTE_AGE = timedelta(hours=12)
```

### `u186.N2_note_fails`

doctor: the note is a failure when it lists a run, though the brief says never

- File: `src/cratekit/cli/doctor_state.py`
- Source: `u186.json`, row `N2_note_fails`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 2 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_doctor_lists_a_gate_open_two_days_and_not_one_open_an_hour`
  - `tests/test_gate_siblings.py::test_doctor_names_a_session_ack_left_blocked_as_sitting_51_left_one`

Old text:

```
    return Finding(key=OPEN_GATES_CHECK, title="runs at a gate", status=Status.INFO, detail=detail)
```

New text:

```
    return Finding(key=OPEN_GATES_CHECK, title="runs at a gate", status=Status.FAIL if blocked else Status.INFO, detail=detail)
```

### `u186.N3_note_unreadable_dropped`

doctor: a record that cannot be read is skipped, so the note reads as clean over it

- File: `src/cratekit/cli/doctor_state.py`
- Source: `u186.json`, row `N3_note_unreadable_dropped`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 2 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_a_record_missing_a_field_is_named_unreadable_at_the_gate_and_in_doctor`
  - `tests/test_gate_siblings.py::test_doctor_says_a_record_it_could_not_read_and_still_never_fails`

Old text:

```
        except Exception:  # noqa: BLE001 - a note never fails; an unread record is named
            unreadable.append(path.stem)
            continue
```

New text:

```
        except Exception:  # noqa: BLE001 - a note never fails; an unread record is named
            continue
```

### `u206.M24_doctor_set_aside_unnamed`

_check_isrc_cache: leave the set aside files out of the note

- File: `src/cratekit/cli/doctor_state.py`
- Source: `u206.json`, row `M24_doctor_set_aside_unnamed`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_doctor_names_a_set_aside_file_and_never_fails`

Old text:

```
    aside = cache.set_aside()
    if aside:
```

New text:

```
    aside = cache.set_aside()
    if False:
```

### `u303.D2_vocals_kind_inverted`

doctor: install.extras reads a missing extra as a model that cannot load

- File: `src/cratekit/cli/doctor_state.py`
- Source: `u303.json`, row `D2_vocals_kind_inverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 4 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_copy_not_installed_from_a_release_gets_the_vocals_modules_own_command`
  - `tests/test_doctor.py::test_a_copy_without_the_vocals_extra_says_so_and_prints_the_reinstall_command`
  - `tests/test_doctor.py::test_missing_model_files_are_named_and_no_reinstall_is_offered_for_them`
  - `tests/test_doctor.py::test_the_row_reads_the_vocals_modules_own_probe_with_the_loader_bound_or_not`

Old text:

```
    if kind != vocal_scoring.MISSING_EXTRA:
```

New text:

```
    if kind == vocal_scoring.MISSING_EXTRA:
```

### `u331.S13_doctor_state_loads_the_taxonomy_loader_at_top`

cli/doctor_state: import the active taxonomy loader at the top again, so crate doctor --help loads the foreign tree with it

- File: `src/cratekit/cli/doctor_state.py`
- Source: `u331.json`, row `S13_doctor_state_loads_the_taxonomy_loader_at_top`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_lazy.py`
- Collected: 161 against a baseline of 161
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_lazy.py::test_doctor_help_loads_the_doctor_and_only_what_the_doctor_itself_imports`

Old text:

```
from cratekit.core import (
    config,
    provider_gate,
```

New text:

```
from cratekit.core import (
    active_taxonomy,  # noqa: F401
    config,
    provider_gate,
```

### `r745-b.C1_pending_name_accepted`

_refuse_destination: accept a name the pending scan reads as an intake file

- File: `src/cratekit/cli/export_collection.py`
- Source: `r745-b.json`, row `C1_pending_name_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 3 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_name_the_pending_scan_reads_as_an_intake_file_is_refused[_favorites.xml]`
  - `tests/test_export_collection.py::test_a_name_the_pending_scan_reads_as_an_intake_file_is_refused[_inboxed.xml]`
  - `tests/test_export_collection.py::test_a_name_the_pending_scan_reads_as_an_intake_file_is_refused[_synced.xml]`

Old text:

```
        if name.endswith(suffix):
```

New text:

```
        if False:
```

### `r745-b.C3_create_not_exclusive`

_write_new: open for writing, replacing what is there. The composite for C2

- File: `src/cratekit/cli/export_collection.py`
- Source: `r745-b.json`, row `C3_create_not_exclusive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_file_that_appears_after_the_check_is_refused_by_the_write`
  - `tests/test_export_collection.py::test_a_file_that_came_and_went_is_still_refused_as_taken`

Old text:

```
open(destination, "xb")
```

New text:

```
open(destination, "wb")
```

### `r745-b.C4_torn_file_left`

_write_new: leave the file a failed write created

- File: `src/cratekit/cli/export_collection.py`
- Source: `r745-b.json`, row `C4_torn_file_left`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_write_that_fails_part_way_leaves_no_file_and_no_folder_it_made`

Old text:

```
                destination.unlink()
```

New text:

```
                pass
```

### `r745-b.C5_made_folders_left`

_write_new: leave the folders a failed write made

- File: `src/cratekit/cli/export_collection.py`
- Source: `r745-b.json`, row `C5_made_folders_left`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_write_that_fails_part_way_leaves_no_file_and_no_folder_it_made`

Old text:

```
                path.rmdir()
```

New text:

```
                pass
```

### `r745-b.C6_folder_not_asked_before_the_copy`

_refuse_destination: do not ask the folder before the database is copied

- File: `src/cratekit/cli/export_collection.py`
- Source: `r745-b.json`, row `C6_folder_not_asked_before_the_copy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_folder_that_is_a_file_is_refused_before_the_database_is_copied`

Old text:

```
    _refuse_unwritable_folder(destination)
```

New text:

```
    pass
```

### `r745-b.C8_live_database_opened`

_read: open the configured database itself, with no copy and no check that rekordbox is closed

- File: `src/cratekit/cli/export_collection.py`
- Source: `r745-b.json`, row `C8_live_database_opened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 3 (killed)
- Killed:
  - `tests/test_export_collection.py::test_rekordbox_or_its_agent_running_is_refused_and_nothing_is_written[rekordbox_agent_running]`
  - `tests/test_export_collection.py::test_rekordbox_or_its_agent_running_is_refused_and_nothing_is_written[rekordbox_running]`
  - `tests/test_export_collection.py::test_the_configured_database_is_never_opened_and_is_left_byte_for_byte`

Old text:

```
    with rb_writer.read_only_copy(database, cfg=cfg) as db:
```

New text:

```
    with __import__("contextlib").closing(
        rb_writer.open_db(database, require_closed=False, check_app_version=False, cfg=cfg)
    ) as db:
```

### `r745-c.C2_existing_file_not_checked_first`

_refuse_destination: drop the check ahead of the copy. Measured again after the test its zero bought

- File: `src/cratekit/cli/export_collection.py`
- Source: `r745-c.json`, row `C2_existing_file_not_checked_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_an_existing_file_is_refused_before_the_database_is_copied`

Old text:

```
    if os.path.lexists(destination):
        raise _taken(destination)
```

New text:

```
    if False:
        raise _taken(destination)
```

### `r745-c.C7_a_file_taken_for_a_folder`

_refuse_unwritable_folder: do not ask whether the nearest ancestor is a folder. Measured again after the assertion its zero bought

- File: `src/cratekit/cli/export_collection.py`
- Source: `r745-c.json`, row `C7_a_file_taken_for_a_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_folder_that_is_a_file_is_refused_before_the_database_is_copied`

Old text:

```
    if not nearest.is_dir():
```

New text:

```
    if False:
```

### `r773-b.C10_summary_remapped_zero`

summary: report no location placed by a rule

- File: `src/cratekit/cli/export_collection.py`
- Source: `r773-b.json`, row `C10_summary_remapped_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_every_location_is_written_under_the_mounted_root_when_a_rule_places_it`

Old text:

```
                "locations_remapped": document.remapped,
```

New text:

```
                "locations_remapped": 0,
```

### `r773-b.C1_no_rule_handed_to_the_emitter`

_read: hand the emitter an empty prefix map, which is the export sitting 19 measured

- File: `src/cratekit/cli/export_collection.py`
- Source: `r773-b.json`, row `C1_no_rule_handed_to_the_emitter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 3 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_landing_splices_into_the_file_and_the_import_is_proved_against_a_second[recorded-under-a-base-drive]`
  - `tests/test_export_collection.py::test_every_location_is_written_under_the_mounted_root_when_a_rule_places_it`
  - `tests/test_export_collection.py::test_the_envelope_counts_a_row_left_to_its_rule`

Old text:

```
        prefix_map=[
            locations.PrefixRule(source, target) for source, target in cfg.resolved_prefix_map()
        ],
```

New text:

```
        prefix_map=[],
```

### `r773-b.C2_root_not_the_library_root`

_read: hand the emitter the filesystem root as the library root

- File: `src/cratekit/cli/export_collection.py`
- Source: `r773-b.json`, row `C2_root_not_the_library_root`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 5 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_landing_splices_into_the_file_and_the_import_is_proved_against_a_second[recorded-under-a-base-drive]`
  - `tests/test_export_collection.py::test_a_library_recorded_where_it_is_mounted_has_nothing_to_place`
  - `tests/test_export_collection.py::test_every_location_is_written_under_the_mounted_root_when_a_rule_places_it`
  - `tests/test_export_collection.py::test_the_envelope_counts_what_the_file_holds_and_names_what_it_left_out`
  - `tests/test_export_collection.py::test_the_export_and_doctor_count_the_same_rows_as_under_no_rule`

Old text:

```
        root=cfg.library.root,
```

New text:

```
        root="/",
```

### `r773-b.C3_warning_not_given`

_warnings: give no warning over rows under no rule

- File: `src/cratekit/cli/export_collection.py`
- Source: `r773-b.json`, row `C3_warning_not_given`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 5 (killed)
- Killed:
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes0-rule (3 under /a/b), and]`
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes1-rule (3 under /a/b, 2 under /c/d, 1 under /e/f), and]`
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes2-rule (3 under /a/b, 2 under /c/d, 1 under /e/f, and 1 other prefix), and]`
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes3-rule (3 under /a/b, 2 under /c/d, 1 under /e/f, and 2 other prefixes), and]`
  - `tests/test_export_collection.py::test_with_no_rule_each_location_is_written_as_the_database_holds_it_and_counted`

Old text:

```
    if omitted.unmapped_paths:
        shown = omitted.unmapped_prefixes[:_NAMED_PREFIXES]
```

New text:

```
    if False:
        shown = omitted.unmapped_prefixes[:_NAMED_PREFIXES]
```

### `r773-b.C4_warning_counts_prefixes_as_rows`

_warnings: open the warning with the number of prefixes where the number of rows goes

- File: `src/cratekit/cli/export_collection.py`
- Source: `r773-b.json`, row `C4_warning_counts_prefixes_as_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 5 (killed)
- Killed:
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes0-rule (3 under /a/b), and]`
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes1-rule (3 under /a/b, 2 under /c/d, 1 under /e/f), and]`
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes2-rule (3 under /a/b, 2 under /c/d, 1 under /e/f, and 1 other prefix), and]`
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes3-rule (3 under /a/b, 2 under /c/d, 1 under /e/f, and 2 other prefixes), and]`
  - `tests/test_export_collection.py::test_with_no_rule_each_location_is_written_as_the_database_holds_it_and_counted`

Old text:

```
                    f"{len(omitted.unmapped_paths)} track(s) record a path under "
```

New text:

```
                    f"{len(omitted.unmapped_prefixes)} track(s) record a path under "
```

### `r773-b.C5_prefix_cap_two`

_NAMED_PREFIXES: name two prefixes where three are named

- File: `src/cratekit/cli/export_collection.py`
- Source: `r773-b.json`, row `C5_prefix_cap_two`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 3 (killed)
- Killed:
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes1-rule (3 under /a/b, 2 under /c/d, 1 under /e/f), and]`
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes2-rule (3 under /a/b, 2 under /c/d, 1 under /e/f, and 1 other prefix), and]`
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes3-rule (3 under /a/b, 2 under /c/d, 1 under /e/f, and 2 other prefixes), and]`

Old text:

```
_NAMED_PREFIXES = 3
```

New text:

```
_NAMED_PREFIXES = 2
```

### `r773-b.C6_rest_of_the_prefixes_not_counted`

_warnings: never say how many prefixes were not named

- File: `src/cratekit/cli/export_collection.py`
- Source: `r773-b.json`, row `C6_rest_of_the_prefixes_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes2-rule (3 under /a/b, 2 under /c/d, 1 under /e/f, and 1 other prefix), and]`
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes3-rule (3 under /a/b, 2 under /c/d, 1 under /e/f, and 2 other prefixes), and]`

Old text:

```
        if more > 0:
            listed +=
```

New text:

```
        if False:
            listed +=
```

### `r773-b.C7_check_always_ok`

export.locations: report ok whatever is under no rule

- File: `src/cratekit/cli/export_collection.py`
- Source: `r773-b.json`, row `C7_check_always_ok`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_with_no_rule_each_location_is_written_as_the_database_holds_it_and_counted`

Old text:

```
            status="ok" if not omitted.unmapped_paths else "info",
        ),
        _check(
            "export.tempo",
```

New text:

```
            status="ok",
        ),
        _check(
            "export.tempo",
```

### `r773-b.C8_summary_unmapped_zero`

summary: report no track under no rule

- File: `src/cratekit/cli/export_collection.py`
- Source: `r773-b.json`, row `C8_summary_unmapped_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 3 (killed)
- Killed:
  - `tests/test_export_collection.py::test_the_export_and_doctor_count_the_same_rows_as_under_no_rule`
  - `tests/test_export_collection.py::test_the_import_proof_is_withheld_on_a_moved_library_with_no_rule`
  - `tests/test_export_collection.py::test_with_no_rule_each_location_is_written_as_the_database_holds_it_and_counted`

Old text:

```
                "tracks_under_no_rule": len(omitted.unmapped_paths),
```

New text:

```
                "tracks_under_no_rule": 0,
```

### `r773-b.C9_summary_left_zero`

summary: report no location left to a rule

- File: `src/cratekit/cli/export_collection.py`
- Source: `r773-b.json`, row `C9_summary_left_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_the_envelope_counts_a_row_left_to_its_rule`

Old text:

```
                "locations_left_to_a_rule": len(omitted.left_to_rule),
```

New text:

```
                "locations_left_to_a_rule": 0,
```

### `r1334.E1_offer_after_compare`

require (existing, sampled): record the offer only on the open gate, so the decide after a stale binds the shown digest again and every resume is stale

- File: `src/cratekit/cli/gates.py`
- Source: `r1334.json`, row `E1_offer_after_compare`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`
- Collected: 13 against a baseline of 13
- Kills: 3 (killed)
- Killed:
  - `tests/test_gate_stale_screen.py::test_a_plan_that_moves_again_after_the_second_answer_is_stale_and_shows_the_newer_plan`
  - `tests/test_gate_stale_screen.py::test_the_answer_recorded_after_a_stale_refusal_binds_the_plan_it_showed`
  - `tests/test_gate_stale_screen.py::test_through_the_dispatcher_the_stale_refusal_shows_the_moved_plan_and_a_decide_applies_it`

Old text:

```
        if spec.digest_source is not None and digest is not None:
            self.state.offers[spec.name] = digest
        pins =
```

New text:

```
        if spec.digest_source is not None and digest is not None and recorded is None:
            self.state.offers[spec.name] = digest
        pins =
```

### `r1334.E2_stale_compare_dropped`

require (existing, sampled): never compare a recorded digest, so a moved plan applies

- File: `src/cratekit/cli/gates.py`
- Source: `r1334.json`, row `E2_stale_compare_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_gate_pins.py`, `tests/test_gate_stale_screen.py`
- Collected: 1040 against a baseline of 1040
- Kills: 10 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_decision_answered_against_a_plan_that_has_since_moved_is_stale`
  - `tests/test_gate_pins.py::test_a_moved_digest_is_still_refused_before_the_pin_is_read`
  - `tests/test_gate_stale_screen.py::test_a_digest_gate_with_nothing_to_show_says_so_as_its_open_gate_does`
  - `tests/test_gate_stale_screen.py::test_a_plan_that_moves_again_after_the_second_answer_is_stale_and_shows_the_newer_plan`
  - `tests/test_gate_stale_screen.py::test_a_stale_refusal_and_its_message_are_otherwise_the_gates_own`
  - `tests/test_gate_stale_screen.py::test_a_stale_refusal_carries_the_moved_plan_as_an_open_gate_shows_it`
  - `tests/test_gate_stale_screen.py::test_only_the_gates_own_stale_prints_a_gate_screen`
  - `tests/test_gate_stale_screen.py::test_the_answer_recorded_after_a_stale_refusal_binds_the_plan_it_showed`
  - `tests/test_gate_stale_screen.py::test_the_stale_screen_shows_the_moved_plan_and_the_answer_it_takes`
  - `tests/test_gate_stale_screen.py::test_through_the_dispatcher_the_stale_refusal_shows_the_moved_plan_and_a_decide_applies_it`

Old text:

```
            if against is not None and against != digest:
```

New text:

```
            if False:
```

### `r1334.E3_record_binds_no_offer`

record (existing, sampled): bind no digest, so the decide after a stale applies any plan

- File: `src/cratekit/cli/gates.py`
- Source: `r1334.json`, row `E3_record_binds_no_offer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_gate_pins.py`, `tests/test_gate_stale_screen.py`
- Collected: 1040 against a baseline of 1040
- Kills: 12 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_decision_answered_against_a_plan_that_has_since_moved_is_stale`
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[sync.all]`
  - `tests/test_gate_pins.py::test_a_moved_digest_is_still_refused_before_the_pin_is_read`
  - `tests/test_gate_pins.py::test_the_open_gate_records_the_pin_and_the_record_carries_it_through_json`
  - `tests/test_gate_stale_screen.py::test_a_digest_gate_with_nothing_to_show_says_so_as_its_open_gate_does`
  - `tests/test_gate_stale_screen.py::test_a_plan_that_moves_again_after_the_second_answer_is_stale_and_shows_the_newer_plan`
  - `tests/test_gate_stale_screen.py::test_a_stale_refusal_and_its_message_are_otherwise_the_gates_own`
  - `tests/test_gate_stale_screen.py::test_a_stale_refusal_carries_the_moved_plan_as_an_open_gate_shows_it`
  - `tests/test_gate_stale_screen.py::test_only_the_gates_own_stale_prints_a_gate_screen`
  - `tests/test_gate_stale_screen.py::test_the_answer_recorded_after_a_stale_refusal_binds_the_plan_it_showed`
  - `tests/test_gate_stale_screen.py::test_the_stale_screen_shows_the_moved_plan_and_the_answer_it_takes`
  - `tests/test_gate_stale_screen.py::test_through_the_dispatcher_the_stale_refusal_shows_the_moved_plan_and_a_decide_applies_it`

Old text:

```
        digest=state.offers.get(spec.name),
    )
    if state.open_gate == spec.name:
```

New text:

```
        digest=None,
    )
    if state.open_gate == spec.name:
```

### `r1334.S10_unknown_option_no_context`

require: raise the unknown option with no screen, as before, though its offer is recorded

- File: `src/cratekit/cli/gates.py`
- Source: `r1334.json`, row `S10_unknown_option_no_context`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_stale_screen.py::test_an_unknown_inline_option_shows_the_plan_its_offer_recorded`

Old text:

```
            raise UnknownOption(spec, chosen, context)
```

New text:

```
            raise UnknownOption(spec, chosen)
```

### `r1334.S11_unknown_option_shown_dropped`

UnknownOption: ignore the context it is handed

- File: `src/cratekit/cli/gates.py`
- Source: `r1334.json`, row `S11_unknown_option_shown_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_stale_screen.py::test_an_unknown_inline_option_shows_the_plan_its_offer_recorded`

Old text:

```
        detail: dict[str, Any] = {"gate": spec.name, "options": list(spec.options)}
        if context is not None:
            detail["shown"] = dict(context)
```

New text:

```
        detail: dict[str, Any] = {"gate": spec.name, "options": list(spec.options)}
```

### `r1334.S1_stale_not_offered`

require: raise the digest stale as a verb's own, offered false, so the refusal carries no screen and the decide after it binds an unshown plan (R-1334 itself)

- File: `src/cratekit/cli/gates.py`
- Source: `r1334.json`, row `S1_stale_not_offered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`
- Collected: 13 against a baseline of 13
- Kills: 7 (killed)
- Killed:
  - `tests/test_gate_stale_screen.py::test_a_digest_gate_with_nothing_to_show_says_so_as_its_open_gate_does`
  - `tests/test_gate_stale_screen.py::test_a_plan_that_moves_again_after_the_second_answer_is_stale_and_shows_the_newer_plan`
  - `tests/test_gate_stale_screen.py::test_a_stale_refusal_carries_the_moved_plan_as_an_open_gate_shows_it`
  - `tests/test_gate_stale_screen.py::test_only_the_gates_own_stale_prints_a_gate_screen`
  - `tests/test_gate_stale_screen.py::test_the_answer_recorded_after_a_stale_refusal_binds_the_plan_it_showed`
  - `tests/test_gate_stale_screen.py::test_the_stale_screen_shows_the_moved_plan_and_the_answer_it_takes`
  - `tests/test_gate_stale_screen.py::test_through_the_dispatcher_the_stale_refusal_shows_the_moved_plan_and_a_decide_applies_it`

Old text:

```
                    spec, self.state.run_id, against, digest, offered=True, context=context
```

New text:

```
                    spec, self.state.run_id, against, digest, offered=False, context=context
```

### `r1334.S2_stale_screen_without_plan`

require: the stale carries the options but not the plan, context dropped

- File: `src/cratekit/cli/gates.py`
- Source: `r1334.json`, row `S2_stale_screen_without_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`
- Collected: 13 against a baseline of 13
- Kills: 5 (killed)
- Killed:
  - `tests/test_gate_stale_screen.py::test_a_plan_that_moves_again_after_the_second_answer_is_stale_and_shows_the_newer_plan`
  - `tests/test_gate_stale_screen.py::test_a_stale_refusal_carries_the_moved_plan_as_an_open_gate_shows_it`
  - `tests/test_gate_stale_screen.py::test_the_answer_recorded_after_a_stale_refusal_binds_the_plan_it_showed`
  - `tests/test_gate_stale_screen.py::test_the_stale_screen_shows_the_moved_plan_and_the_answer_it_takes`
  - `tests/test_gate_stale_screen.py::test_through_the_dispatcher_the_stale_refusal_shows_the_moved_plan_and_a_decide_applies_it`

Old text:

```
                    spec, self.state.run_id, against, digest, offered=True, context=context
```

New text:

```
                    spec, self.state.run_id, against, digest, offered=True, context=None
```

### `r1334.S3_offered_ignored`

DecisionStale: never add the screen, whatever offered says

- File: `src/cratekit/cli/gates.py`
- Source: `r1334.json`, row `S3_offered_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`
- Collected: 13 against a baseline of 13
- Kills: 7 (killed)
- Killed:
  - `tests/test_gate_stale_screen.py::test_a_digest_gate_with_nothing_to_show_says_so_as_its_open_gate_does`
  - `tests/test_gate_stale_screen.py::test_a_plan_that_moves_again_after_the_second_answer_is_stale_and_shows_the_newer_plan`
  - `tests/test_gate_stale_screen.py::test_a_stale_refusal_carries_the_moved_plan_as_an_open_gate_shows_it`
  - `tests/test_gate_stale_screen.py::test_only_the_gates_own_stale_prints_a_gate_screen`
  - `tests/test_gate_stale_screen.py::test_the_answer_recorded_after_a_stale_refusal_binds_the_plan_it_showed`
  - `tests/test_gate_stale_screen.py::test_the_stale_screen_shows_the_moved_plan_and_the_answer_it_takes`
  - `tests/test_gate_stale_screen.py::test_through_the_dispatcher_the_stale_refusal_shows_the_moved_plan_and_a_decide_applies_it`

Old text:

```
        if offered:
            detail.update(_screen(spec, context))
```

New text:

```
        if False:
            detail.update(_screen(spec, context))
```

### `r1334.S4_screen_always`

DecisionStale: add the screen to every stale, a verb's own write handle stale and the pinned one included

- File: `src/cratekit/cli/gates.py`
- Source: `r1334.json`, row `S4_screen_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`
- Collected: 13 against a baseline of 13
- Kills: 3 (killed)
- Killed:
  - `tests/test_gate_stale_screen.py::test_a_pinned_stale_keeps_the_detail_it_had`
  - `tests/test_gate_stale_screen.py::test_a_stale_a_verb_raises_itself_keeps_the_detail_it_had`
  - `tests/test_gate_stale_screen.py::test_only_the_gates_own_stale_prints_a_gate_screen`

Old text:

```
        if offered:
            detail.update(_screen(spec, context))
```

New text:

```
        if True:
            detail.update(_screen(spec, context))
```

### `r1334.S5_screen_no_shown`

_screen: drop the shown plan, keep the options

- File: `src/cratekit/cli/gates.py`
- Source: `r1334.json`, row `S5_screen_no_shown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`
- Collected: 13 against a baseline of 13
- Kills: 5 (killed)
- Killed:
  - `tests/test_gate_stale_screen.py::test_a_plan_that_moves_again_after_the_second_answer_is_stale_and_shows_the_newer_plan`
  - `tests/test_gate_stale_screen.py::test_a_stale_refusal_carries_the_moved_plan_as_an_open_gate_shows_it`
  - `tests/test_gate_stale_screen.py::test_the_answer_recorded_after_a_stale_refusal_binds_the_plan_it_showed`
  - `tests/test_gate_stale_screen.py::test_the_stale_screen_shows_the_moved_plan_and_the_answer_it_takes`
  - `tests/test_gate_stale_screen.py::test_through_the_dispatcher_the_stale_refusal_shows_the_moved_plan_and_a_decide_applies_it`

Old text:

```
    if context is not None:
        screen["shown"] = dict(context)
    return screen
```

New text:

```
    return screen
```

### `r1334.S6_screen_shown_empty_for_none`

_screen: an empty shown where the gate shows nothing, absent read as empty

- File: `src/cratekit/cli/gates.py`
- Source: `r1334.json`, row `S6_screen_shown_empty_for_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_stale_screen.py::test_a_digest_gate_with_nothing_to_show_says_so_as_its_open_gate_does`

Old text:

```
    if context is not None:
        screen["shown"] = dict(context)
    return screen
```

New text:

```
    screen["shown"] = dict(context or {})
    return screen
```

### `r1334.S7_screen_no_options`

_screen: no options, so the human screen is never printed for a stale

- File: `src/cratekit/cli/gates.py`
- Source: `r1334.json`, row `S7_screen_no_options`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`
- Collected: 13 against a baseline of 13
- Kills: 4 (killed)
- Killed:
  - `tests/test_gate_stale_screen.py::test_a_digest_gate_with_nothing_to_show_says_so_as_its_open_gate_does`
  - `tests/test_gate_stale_screen.py::test_a_stale_refusal_carries_the_moved_plan_as_an_open_gate_shows_it`
  - `tests/test_gate_stale_screen.py::test_only_the_gates_own_stale_prints_a_gate_screen`
  - `tests/test_gate_stale_screen.py::test_through_the_dispatcher_the_stale_refusal_shows_the_moved_plan_and_a_decide_applies_it`

Old text:

```
        "options": list(spec.options),
        "prompt": spec.prompt,
```

New text:

```
        "prompt": spec.prompt,
```

### `r1334.S8_screen_no_prompt`

_screen: no prompt, so the stale screen asks 'A decision is required.'

- File: `src/cratekit/cli/gates.py`
- Source: `r1334.json`, row `S8_screen_no_prompt`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_stale_screen.py::test_a_stale_refusal_carries_the_moved_plan_as_an_open_gate_shows_it`

Old text:

```
        "prompt": spec.prompt,
        "explicit": spec.explicit,
```

New text:

```
        "explicit": spec.explicit,
```

### `r1334.S9_screen_explicit_false`

_screen: every stale read as a gate that takes an inline answer

- File: `src/cratekit/cli/gates.py`
- Source: `r1334.json`, row `S9_screen_explicit_false`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_stale_screen.py::test_a_stale_refusal_carries_the_moved_plan_as_an_open_gate_shows_it`

Old text:

```
        "explicit": spec.explicit,
    }
```

New text:

```
        "explicit": False,
    }
```

### `r1349.C1_argv_ignored`

continue_command: the recorded command line ignored, so every continue says the verb's words and an ellipsis

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `C1_argv_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`
- Collected: 13 against a baseline of 13
- Kills: 3 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_a_decide_on_a_digest_gate_the_run_has_not_reached_is_refused_and_writes_nothing`
  - `tests/test_gate_not_reached.py::test_the_refusal_names_the_open_gate_first_and_then_the_run_that_reaches_this_one`
  - `tests/test_gate_not_reached.py::test_through_the_dispatcher_the_refusal_saves_nothing_and_prints_no_gate_screen`

Old text:

```
    if state.argv is not None:
        return shlex.join(["crate", "--run", state.run_id, *state.argv])
```

New text:

```
    if False:
        return shlex.join(["crate", "--run", state.run_id, *state.argv])
```

### `r1349.C2_run_dropped`

continue_command: the --run dropped, so the command starts a fresh run that loses the answers

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `C2_run_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`
- Collected: 13 against a baseline of 13
- Kills: 3 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_a_decide_on_a_digest_gate_the_run_has_not_reached_is_refused_and_writes_nothing`
  - `tests/test_gate_not_reached.py::test_the_refusal_names_the_open_gate_first_and_then_the_run_that_reaches_this_one`
  - `tests/test_gate_not_reached.py::test_through_the_dispatcher_the_refusal_saves_nothing_and_prints_no_gate_screen`

Old text:

```
        return shlex.join(["crate", "--run", state.run_id, *state.argv])
```

New text:

```
        return shlex.join(["crate", *state.argv])
```

### `r1349.E2_open_left`

record (existing): the open gate left open after it is answered

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `E2_open_left`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`, `tests/test_gate_siblings.py`
- Collected: 47 against a baseline of 47
- Kills: 4 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_a_gate_reached_and_left_open_takes_the_answer_and_binds_what_it_showed`
  - `tests/test_gate_not_reached.py::test_a_gate_reached_with_no_digest_and_left_open_still_takes_a_decide`
  - `tests/test_gate_siblings.py::test_an_answer_thirteen_hours_ago_is_history_and_says_nothing`
  - `tests/test_gate_siblings.py::test_an_answered_run_two_days_old_is_not_blocked`

Old text:

```
    if state.open_gate == spec.name:
        state.open_gate = None


def blocked_by
```

New text:

```
    if False:
        state.open_gate = None


def blocked_by
```

### `r1349.E3_offer_unrecorded`

require (existing): the offer never recorded when the gate is reached

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `E3_offer_unrecorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_gate_not_reached.py`, `tests/test_gate_pins.py`, `tests/test_gate_siblings.py`, `tests/test_gate_stale_screen.py`
- Collected: 1087 against a baseline of 1087
- Kills: 19 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_decision_answered_against_a_plan_that_has_since_moved_is_stale`
  - `tests/test_cli_contract.py::test_an_unanswered_gate_exits_with_the_documented_code_and_leaves_the_run_resumable`
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[sync.all]`
  - `tests/test_gate_not_reached.py::test_a_gate_offered_and_answered_takes_a_new_answer_over_its_offer`
  - `tests/test_gate_not_reached.py::test_a_gate_reached_and_left_open_takes_the_answer_and_binds_what_it_showed`
  - `tests/test_gate_pins.py::test_a_moved_digest_is_still_refused_before_the_pin_is_read`
  - `tests/test_gate_pins.py::test_the_open_gate_records_the_pin_and_the_record_carries_it_through_json`
  - `tests/test_gate_siblings.py::test_decide_continue_carries_the_warning_on_the_verbs_own_envelope`
  - `tests/test_gate_siblings.py::test_decide_repeats_over_a_sibling_that_answered_then_stopped_at_another_gate`
  - `tests/test_gate_siblings.py::test_decide_repeats_the_warning_over_a_sibling_answered_apply_on_the_same_plan`
  - `tests/test_gate_stale_screen.py::test_a_digest_gate_with_nothing_to_show_says_so_as_its_open_gate_does`
  - `tests/test_gate_stale_screen.py::test_a_plan_that_moves_again_after_the_second_answer_is_stale_and_shows_the_newer_plan`
  - `tests/test_gate_stale_screen.py::test_a_stale_refusal_and_its_message_are_otherwise_the_gates_own`
  - `tests/test_gate_stale_screen.py::test_a_stale_refusal_carries_the_moved_plan_as_an_open_gate_shows_it`
  - `tests/test_gate_stale_screen.py::test_an_unknown_inline_option_shows_the_plan_its_offer_recorded`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        if spec.digest_source is not None and digest is not None:
            self.state.offers[spec.name] = digest
```

New text:

```
        if False:
            self.state.offers[spec.name] = digest
```

### `r1349.N1_guard_gone`

record: the not reached refusal removed, so an answer ahead of a digest gate is recorded with no digest (R-1349 itself)

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `N1_guard_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`
- Collected: 13 against a baseline of 13
- Kills: 5 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_a_decide_on_a_digest_gate_the_run_has_not_reached_is_refused_and_writes_nothing`
  - `tests/test_gate_not_reached.py::test_a_run_waiting_at_no_gate_is_told_to_continue_to_this_one`
  - `tests/test_gate_not_reached.py::test_the_refusal_is_not_an_open_gate_to_any_reader`
  - `tests/test_gate_not_reached.py::test_the_refusal_names_the_open_gate_first_and_then_the_run_that_reaches_this_one`
  - `tests/test_gate_not_reached.py::test_through_the_dispatcher_the_refusal_saves_nothing_and_prints_no_gate_screen`

Old text:

```
        spec.digest_source is not None
        and spec.name not in state.offers
        and state.open_gate != spec.name
        and spec.name not in state.decisions
    ):
        raise GateNotReached(state, spec)
```

New text:

```
        False
        and spec.digest_source is not None
        and spec.name not in state.offers
        and state.open_gate != spec.name
        and spec.name not in state.decisions
    ):
        raise GateNotReached(state, spec)
```

### `r1349.N2_any_gate`

record: the digest source clause dropped, so a gate that binds no plan is refused ahead too

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `N2_any_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_a_gate_that_binds_no_plan_takes_an_answer_before_it_is_reached`

Old text:

```
        spec.digest_source is not None
        and spec.name not in state.offers
        and state.open_gate != spec.name
        and spec.name not in state.decisions
    ):
        raise GateNotReached(state, spec)
```

New text:

```
        spec.name not in state.offers
        and state.open_gate != spec.name
        and spec.name not in state.decisions
    ):
        raise GateNotReached(state, spec)
```

### `r1349.N3_offer_ignored`

record: the offer clause dropped, so a run handed an offer (hand_off) or a gate offered and not open is refused

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `N3_offer_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_a_handed_off_run_holds_the_offer_its_decide_binds`

Old text:

```
        spec.digest_source is not None
        and spec.name not in state.offers
        and state.open_gate != spec.name
        and spec.name not in state.decisions
    ):
        raise GateNotReached(state, spec)
```

New text:

```
        spec.digest_source is not None
        and state.open_gate != spec.name
        and spec.name not in state.decisions
    ):
        raise GateNotReached(state, spec)
```

### `r1349.N4_open_ignored`

record: the open gate clause dropped, so a gate reached with no digest and left open is refused

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `N4_open_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_gate_not_reached.py`, `tests/test_gate_siblings.py`
- Collected: 1067 against a baseline of 1067
- Kills: 6 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_conformance_3_admits_a_verb_carrying_two_gates[explicit-then-explicit]`
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[run.retire]`
  - `tests/test_gate_not_reached.py::test_a_gate_already_answered_takes_a_new_answer_once_the_run_waits_elsewhere`
  - `tests/test_gate_not_reached.py::test_a_gate_reached_with_no_digest_and_left_open_still_takes_a_decide`
  - `tests/test_gate_siblings.py::test_an_answered_run_two_days_old_is_not_blocked`
  - `tests/test_gate_siblings.py::test_decide_says_nothing_when_this_run_was_offered_no_digest`

Old text:

```
        spec.digest_source is not None
        and spec.name not in state.offers
        and state.open_gate != spec.name
        and spec.name not in state.decisions
    ):
        raise GateNotReached(state, spec)
```

New text:

```
        spec.digest_source is not None
        and spec.name not in state.offers
        and spec.name not in state.decisions
    ):
        raise GateNotReached(state, spec)
```

### `r1349.N5_answered_ignored`

record: the answered clause dropped, so a gate reached with no digest and answered cannot be answered again

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `N5_answered_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_a_gate_already_answered_takes_a_new_answer_once_the_run_waits_elsewhere`

Old text:

```
        spec.digest_source is not None
        and spec.name not in state.offers
        and state.open_gate != spec.name
        and spec.name not in state.decisions
    ):
        raise GateNotReached(state, spec)
```

New text:

```
        spec.digest_source is not None
        and spec.name not in state.offers
        and state.open_gate != spec.name
    ):
        raise GateNotReached(state, spec)
```

### `r1349.N6_offer_inverted`

record: the offer clause inverted, refusing only a gate that holds an offer

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `N6_offer_inverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`
- Collected: 13 against a baseline of 13
- Kills: 6 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_a_decide_on_a_digest_gate_the_run_has_not_reached_is_refused_and_writes_nothing`
  - `tests/test_gate_not_reached.py::test_a_handed_off_run_holds_the_offer_its_decide_binds`
  - `tests/test_gate_not_reached.py::test_a_run_waiting_at_no_gate_is_told_to_continue_to_this_one`
  - `tests/test_gate_not_reached.py::test_the_refusal_is_not_an_open_gate_to_any_reader`
  - `tests/test_gate_not_reached.py::test_the_refusal_names_the_open_gate_first_and_then_the_run_that_reaches_this_one`
  - `tests/test_gate_not_reached.py::test_through_the_dispatcher_the_refusal_saves_nothing_and_prints_no_gate_screen`

Old text:

```
        spec.digest_source is not None
        and spec.name not in state.offers
        and state.open_gate != spec.name
        and spec.name not in state.decisions
    ):
        raise GateNotReached(state, spec)
```

New text:

```
        spec.digest_source is not None
        and spec.name in state.offers
        and state.open_gate != spec.name
        and spec.name not in state.decisions
    ):
        raise GateNotReached(state, spec)
```

### `r1349.N7_written_before_refusal`

record: the answer written before the refusal is raised, so the refusal leaves a digestless decision in the run

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `N7_written_before_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`
- Collected: 13 against a baseline of 13
- Kills: 3 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_a_decide_on_a_digest_gate_the_run_has_not_reached_is_refused_and_writes_nothing`
  - `tests/test_gate_not_reached.py::test_a_run_waiting_at_no_gate_is_told_to_continue_to_this_one`
  - `tests/test_gate_not_reached.py::test_the_refusal_names_the_open_gate_first_and_then_the_run_that_reaches_this_one`

Old text:

```
        raise GateNotReached(state, spec)

```

New text:

```
        state.decisions[spec.name] = Decision(option=option, actor=actor, recorded="", digest=None)
        raise GateNotReached(state, spec)

```

### `r1349.N8_after_unknown_swapped`

record: the unknown option check skipped, so an option the gate does not offer is recorded

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `N8_after_unknown_swapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_an_unknown_option_is_refused_as_it_was_on_a_gate_not_reached`

Old text:

```
    if option not in spec.options:
        raise UnknownOption(spec, option)
    if (

```

New text:

```
    if False:
        raise UnknownOption(spec, option)
    if (

```

### `r1349.R1_reason_open_gate`

GateNotReached: reason decision-required, read and printed as an open gate inviting the refused answer

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `R1_reason_open_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`
- Collected: 13 against a baseline of 13
- Kills: 3 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_a_decide_on_a_digest_gate_the_run_has_not_reached_is_refused_and_writes_nothing`
  - `tests/test_gate_not_reached.py::test_the_refusal_is_not_an_open_gate_to_any_reader`
  - `tests/test_gate_not_reached.py::test_through_the_dispatcher_the_refusal_saves_nothing_and_prints_no_gate_screen`

Old text:

```
                reason="gate-not-reached",
```

New text:

```
                reason="decision-required",
```

### `r1349.R2_answer_remedy`

GateNotReached: carries the answer-decision remedy verbs read as an open gate

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `R2_answer_remedy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_the_refusal_is_not_an_open_gate_to_any_reader`

Old text:

```
                remediation=Remediation(steps=steps),
```

New text:

```
                remediation=Remediation(remedy=Remedy.ANSWER_DECISION, steps=steps),
```

### `r1349.R3_waiting_ignored`

GateNotReached: the gate the run waits at is never named in the steps

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `R3_waiting_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`
- Collected: 13 against a baseline of 13
- Kills: 2 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_a_decide_on_a_digest_gate_the_run_has_not_reached_is_refused_and_writes_nothing`
  - `tests/test_gate_not_reached.py::test_the_refusal_names_the_open_gate_first_and_then_the_run_that_reaches_this_one`

Old text:

```
        if waiting is not None:
            steps: tuple
```

New text:

```
        if False:
            steps: tuple
```

### `r1349.R4_continue_wrong`

GateNotReached: the continue step names a fresh run of the verb instead of the run under --run

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `R4_continue_wrong`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`
- Collected: 13 against a baseline of 13
- Kills: 4 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_a_decide_on_a_digest_gate_the_run_has_not_reached_is_refused_and_writes_nothing`
  - `tests/test_gate_not_reached.py::test_a_run_waiting_at_no_gate_is_told_to_continue_to_this_one`
  - `tests/test_gate_not_reached.py::test_the_refusal_names_the_open_gate_first_and_then_the_run_that_reaches_this_one`
  - `tests/test_gate_not_reached.py::test_through_the_dispatcher_the_refusal_saves_nothing_and_prints_no_gate_screen`

Old text:

```
        command = continue_command(state)
        waiting = state.open_gate
```

New text:

```
        command = f"crate {state.verb.replace('.', ' ')}"
        waiting = state.open_gate
```

### `r1349.R5_open_gate_detail`

GateNotReached: the detail's open_gate always None

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `R5_open_gate_detail`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_a_decide_on_a_digest_gate_the_run_has_not_reached_is_refused_and_writes_nothing`

Old text:

```
                    "open_gate": waiting,
```

New text:

```
                    "open_gate": None,
```

### `r1349.R6_message_no_gate`

GateNotReached: the message names no gate

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `R6_message_no_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`
- Collected: 13 against a baseline of 13
- Kills: 2 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_a_decide_on_a_digest_gate_the_run_has_not_reached_is_refused_and_writes_nothing`
  - `tests/test_gate_not_reached.py::test_through_the_dispatcher_the_refusal_saves_nothing_and_prints_no_gate_screen`

Old text:

```
                    f"run {state.run_id} has not reached the gate {spec.name!r}, so "
```

New text:

```
                    f"run {state.run_id} has not reached a gate yet, so "
```

### `r1349.R7_answer_step_dropped`

GateNotReached: the closing step that answers the named gate dropped when the run waits at another

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `R7_answer_step_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_the_refusal_names_the_open_gate_first_and_then_the_run_that_reaches_this_one`

Old text:

```
                f"then {reach}",
                answer,

```

New text:

```
                f"then {reach}",

```

### `u161.G1_pin_never_compared`

Gates.require: skip the pin comparison, so an answer given over one file is used by a run that opened another

- File: `src/cratekit/cli/gates.py`
- Source: `u161.json`, row `G1_pin_never_compared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_pins.py`, `tests/test_intake_land_native.py`
- Collected: 51 against a baseline of 51
- Kills: 4 (killed)
- Killed:
  - `tests/test_gate_pins.py::test_a_pinned_run_asked_with_no_pin_is_stale_too`
  - `tests/test_gate_pins.py::test_an_answer_whose_run_pinned_nothing_is_stale_to_a_gate_that_now_pins`
  - `tests/test_gate_pins.py::test_another_pin_with_the_same_digest_is_stale_and_names_both_values`
  - `tests/test_intake_land_native.py::test_the_same_files_against_a_copy_at_another_path_digest_equal_and_each_screen_names_its_path`

Old text:

```
        if recorded is not None and inline is None:
            held = self.state.pins.get(spec.name, {})
```

New text:

```
        if False:
            held = self.state.pins.get(spec.name, {})
```

### `u161.G2_pin_overwritten_before_compare`

Gates.require: record the pin on every call, so the continuation replaces the answered pin before comparing it

- File: `src/cratekit/cli/gates.py`
- Source: `u161.json`, row `G2_pin_overwritten_before_compare`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_pins.py`, `tests/test_intake_land_native.py`
- Collected: 51 against a baseline of 51
- Kills: 3 (killed)
- Killed:
  - `tests/test_gate_pins.py::test_an_answer_whose_run_pinned_nothing_is_stale_to_a_gate_that_now_pins`
  - `tests/test_gate_pins.py::test_another_pin_with_the_same_digest_is_stale_and_names_both_values`
  - `tests/test_intake_land_native.py::test_the_same_files_against_a_copy_at_another_path_digest_equal_and_each_screen_names_its_path`

Old text:

```
        if recorded is None and pins:
```

New text:

```
        if pins:
```

### `u161.G3_absence_read_as_agreement`

Gates.require: compare only keys both sides pinned, so a run that pinned nothing passes a gate that now pins

- File: `src/cratekit/cli/gates.py`
- Source: `u161.json`, row `G3_absence_read_as_agreement`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_pins.py`
- Collected: 7 against a baseline of 7
- Kills: 2 (killed)
- Killed:
  - `tests/test_gate_pins.py::test_a_pinned_run_asked_with_no_pin_is_stale_too`
  - `tests/test_gate_pins.py::test_an_answer_whose_run_pinned_nothing_is_stale_to_a_gate_that_now_pins`

Old text:

```
                if held.get(key) != pins.get(key):
```

New text:

```
                if key in held and key in pins and held[key] != pins[key]:
```

### `u161.G4_pins_not_written`

RunState.to_json: never write the pins, so the answer's file is lost when the first act exits

- File: `src/cratekit/cli/gates.py`
- Source: `u161.json`, row `G4_pins_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_pins.py`, `tests/test_intake_land_native.py`
- Collected: 51 against a baseline of 51
- Kills: 24 (killed)
- Killed:
  - `tests/test_gate_pins.py::test_a_pinned_run_asked_with_no_pin_is_stale_too`
  - `tests/test_gate_pins.py::test_another_pin_with_the_same_digest_is_stale_and_names_both_values`
  - `tests/test_gate_pins.py::test_the_open_gate_records_the_pin_and_the_record_carries_it_through_json`
  - `tests/test_gate_pins.py::test_the_same_pin_on_the_continuation_takes_the_recorded_answer`
  - `tests/test_intake_land_native.py::test_a_failure_after_the_commit_landed_is_recorded_and_still_refuses`
  - `tests/test_intake_land_native.py::test_a_failure_on_the_second_file_leaves_the_database_as_it_was_and_names_the_moves`
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_file_whose_tags_resolve_to_no_sub_stays_in_staging_on_the_native_medium_too`
  - `tests/test_intake_land_native.py::test_a_landing_names_the_pass_it_was_given_on_the_record_sync_mark_reads[None]`
  - `tests/test_intake_land_native.py::test_a_landing_names_the_pass_it_was_given_on_the_record_sync_mark_reads[RUN_synced]`
  - `tests/test_intake_land_native.py::test_a_landing_that_adds_no_row_needs_no_majority`
  - `tests/test_intake_land_native.py::test_a_row_whose_file_id_or_link_did_not_take_is_refused_after_the_commit[_file_id_lies_once]`
  - `tests/test_intake_land_native.py::test_a_row_whose_file_id_or_link_did_not_take_is_refused_after_the_commit[_link_keeps_the_bindings]`
  - `tests/test_intake_land_native.py::test_a_suffix_the_database_has_no_type_for_is_left_in_staging_and_the_batch_lands`
  - `tests/test_intake_land_native.py::test_an_analysis_value_reaching_the_row_is_refused_from_sql_before_the_commit[UPDATE djmdContent SET BPM = 12400 WHERE ID = :id-BPM]`
  - ... and 9 more, see the JSON sidecar

Old text:

```
        if self.pins:
            record["pins"]
```

New text:

```
        if False:
            record["pins"]
```

### `u161.G5_pins_not_read`

RunState.from_json: read no pins back, so a continuation sees none

- File: `src/cratekit/cli/gates.py`
- Source: `u161.json`, row `G5_pins_not_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_pins.py`, `tests/test_intake_land_native.py`
- Collected: 51 against a baseline of 51
- Kills: 24 (killed)
- Killed:
  - `tests/test_gate_pins.py::test_a_pinned_run_asked_with_no_pin_is_stale_too`
  - `tests/test_gate_pins.py::test_another_pin_with_the_same_digest_is_stale_and_names_both_values`
  - `tests/test_gate_pins.py::test_the_open_gate_records_the_pin_and_the_record_carries_it_through_json`
  - `tests/test_gate_pins.py::test_the_same_pin_on_the_continuation_takes_the_recorded_answer`
  - `tests/test_intake_land_native.py::test_a_failure_after_the_commit_landed_is_recorded_and_still_refuses`
  - `tests/test_intake_land_native.py::test_a_failure_on_the_second_file_leaves_the_database_as_it_was_and_names_the_moves`
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_file_whose_tags_resolve_to_no_sub_stays_in_staging_on_the_native_medium_too`
  - `tests/test_intake_land_native.py::test_a_landing_names_the_pass_it_was_given_on_the_record_sync_mark_reads[None]`
  - `tests/test_intake_land_native.py::test_a_landing_names_the_pass_it_was_given_on_the_record_sync_mark_reads[RUN_synced]`
  - `tests/test_intake_land_native.py::test_a_landing_that_adds_no_row_needs_no_majority`
  - `tests/test_intake_land_native.py::test_a_row_whose_file_id_or_link_did_not_take_is_refused_after_the_commit[_file_id_lies_once]`
  - `tests/test_intake_land_native.py::test_a_row_whose_file_id_or_link_did_not_take_is_refused_after_the_commit[_link_keeps_the_bindings]`
  - `tests/test_intake_land_native.py::test_a_suffix_the_database_has_no_type_for_is_left_in_staging_and_the_batch_lands`
  - `tests/test_intake_land_native.py::test_an_analysis_value_reaching_the_row_is_refused_from_sql_before_the_commit[UPDATE djmdContent SET BPM = 12400 WHERE ID = :id-BPM]`
  - ... and 9 more, see the JSON sidecar

Old text:

```
                for name, one in (data.get("pins") or {}).items()
```

New text:

```
                for name, one in {}.items()
```

### `u168.C12_argv_not_saved`

RunState.to_json: drop the command line from the saved record

- File: `src/cratekit/cli/gates.py`
- Source: `u168.json`, row `C12_argv_not_saved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 1020 against a baseline of 1020
- Kills: 2 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_run_continued_by_hand_keeps_the_command_line_its_first_invocation_recorded`
  - `tests/test_cli_contract.py::test_run_decide_continue_resumes_the_owning_verb_with_its_own_arguments`

Old text:

```
        if self.argv is not None:
            record["argv"] = list(self.argv)
```

New text:

```
        if False:
            record["argv"] = list(self.argv)
```

### `u186.S10_scope_every_verb`

writes_the_database: answer True for every declared verb, so a gated verb writing no database warns

- File: `src/cratekit/cli/gates.py`
- Source: `u186.json`, row `S10_scope_every_verb`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 2 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_a_verb_that_writes_no_database_is_outside_the_warning`
  - `tests/test_gate_siblings.py::test_a_verb_writing_no_database_says_nothing_of_its_own_siblings`

Old text:

```
    return bool(owner.writes & DB_WRITE_SURFACES)
```

New text:

```
    return True
```

### `u186.S1_window_wider`

SIBLING_WINDOW: twelve hours widened to a day, so an answer thirteen hours old is named

- File: `src/cratekit/cli/gates.py`
- Source: `u186.json`, row `S1_window_wider`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 2 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_an_answer_thirteen_hours_ago_is_history_and_says_nothing`
  - `tests/test_gate_siblings.py::test_decide_says_nothing_over_a_sibling_answered_thirteen_hours_ago`

Old text:

```
SIBLING_WINDOW = timedelta(hours=12)
```

New text:

```
SIBLING_WINDOW = timedelta(hours=24)
```

### `u186.S2_window_narrower`

SIBLING_WINDOW: twelve hours halved, so an answer eleven hours fifty old is silent

- File: `src/cratekit/cli/gates.py`
- Source: `u186.json`, row `S2_window_narrower`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_an_answer_just_inside_twelve_hours_is_still_named`

Old text:

```
SIBLING_WINDOW = timedelta(hours=12)
```

New text:

```
SIBLING_WINDOW = timedelta(hours=6)
```

### `u186.S3_exclude_self`

siblings: drop the asking run's exclusion, so a run continued to its gate names itself

- File: `src/cratekit/cli/gates.py`
- Source: `u186.json`, row `S3_exclude_self`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 19 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_a_record_missing_a_field_is_named_unreadable_at_the_gate_and_in_doctor`
  - `tests/test_gate_siblings.py::test_a_record_that_cannot_be_read_is_said_rather_than_read_as_no_run`
  - `tests/test_gate_siblings.py::test_a_run_never_warns_about_itself`
  - `tests/test_gate_siblings.py::test_a_run_of_another_verb_is_never_named`
  - `tests/test_gate_siblings.py::test_a_sibling_whose_gate_is_open_is_named_as_open`
  - `tests/test_gate_siblings.py::test_an_answer_just_inside_twelve_hours_is_still_named`
  - `tests/test_gate_siblings.py::test_an_answer_ten_minutes_ago_is_named_with_its_actor_option_and_time`
  - `tests/test_gate_siblings.py::test_an_answer_thirteen_hours_ago_is_history_and_says_nothing`
  - `tests/test_gate_siblings.py::test_an_answer_with_no_recorded_time_is_named_as_unrecorded`
  - `tests/test_gate_siblings.py::test_decide_continue_carries_the_warning_on_the_verbs_own_envelope`
  - `tests/test_gate_siblings.py::test_decide_continue_says_a_sibling_once_when_the_verb_stops_at_its_gate_again`
  - `tests/test_gate_siblings.py::test_decide_repeats_over_a_sibling_that_answered_then_stopped_at_another_gate`
  - `tests/test_gate_siblings.py::test_decide_repeats_the_warning_over_a_sibling_answered_apply_on_the_same_plan`
  - `tests/test_gate_siblings.py::test_decide_says_nothing_over_a_sibling_answered_thirteen_hours_ago`
  - `tests/test_gate_siblings.py::test_decide_says_nothing_when_the_sibling_aborted`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        if path.stem == exclude:
            continue
        try:
            state = load(path.stem)
```

New text:

```
        try:
            state = load(path.stem)
```

### `u186.S4_other_verb`

siblings: drop the verb filter, so a run of another verb is named

- File: `src/cratekit/cli/gates.py`
- Source: `u186.json`, row `S4_other_verb`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_a_run_of_another_verb_is_never_named`

Old text:

```
        if state.verb != verb:
            continue
```

New text:

```
(empty)
```

### `u186.S5_unreadable_dropped`

siblings: skip a record that cannot be read rather than counting it, so the gap reads as no sibling

- File: `src/cratekit/cli/gates.py`
- Source: `u186.json`, row `S5_unreadable_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 2 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_a_record_missing_a_field_is_named_unreadable_at_the_gate_and_in_doctor`
  - `tests/test_gate_siblings.py::test_a_record_that_cannot_be_read_is_said_rather_than_read_as_no_run`

Old text:

```
        except Exception:  # noqa: BLE001 - an unread record is said, never skipped
            unreadable.append(path.stem)
            continue
```

New text:

```
        except Exception:  # noqa: BLE001 - an unread record is said, never skipped
            continue
```

### `u186.S6_unrecorded_time_old`

siblings: an answer whose time cannot be read counts as old rather than recent

- File: `src/cratekit/cli/gates.py`
- Source: `u186.json`, row `S6_unrecorded_time_old`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_an_answer_with_no_recorded_time_is_named_as_unrecorded`

Old text:

```
            if when is None or moment - when <= within:
```

New text:

```
            if when is not None and moment - when <= within:
```

### `u186.S7_open_drops_answers`

siblings: a run with an open gate keeps no answers, the shape the first review round drove

- File: `src/cratekit/cli/gates.py`
- Source: `u186.json`, row `S7_open_drops_answers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_decide_repeats_over_a_sibling_that_answered_then_stopped_at_another_gate`

Old text:

```
                    run_id=state.run_id, verb=verb, gate=state.open_gate, at=since, answers=answers
```

New text:

```
                    run_id=state.run_id, verb=verb, gate=state.open_gate, at=since, answers=()
```

### `u186.S8_open_read_as_answered`

siblings: an open gate is reported as an answered run, so the message never says open

- File: `src/cratekit/cli/gates.py`
- Source: `u186.json`, row `S8_open_read_as_answered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 4 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_a_sibling_whose_gate_is_open_is_named_as_open`
  - `tests/test_gate_siblings.py::test_decide_repeats_over_a_sibling_that_answered_then_stopped_at_another_gate`
  - `tests/test_gate_siblings.py::test_one_warning_per_other_run`
  - `tests/test_gate_siblings.py::test_the_warning_prints_on_the_screen_a_person_reads`

Old text:

```
        if state.open_gate is not None:
            since = idle_since(state, path)
```

New text:

```
        if False:
            since = idle_since(state, path)
```

### `u186.S9_unreadable_unsaid`

sibling_warnings: say nothing of the records that could not be read

- File: `src/cratekit/cli/gates.py`
- Source: `u186.json`, row `S9_unreadable_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 2 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_a_record_missing_a_field_is_named_unreadable_at_the_gate_and_in_doctor`
  - `tests/test_gate_siblings.py::test_a_record_that_cannot_be_read_is_said_rather_than_read_as_no_run`

Old text:

```
    if unreadable:
        records_word = "record" if len(unreadable) == 1 else "records"
        said.append(
```

New text:

```
    if False:
        records_word = "record" if len(unreadable) == 1 else "records"
        said.append(
```

### `u49-author.G2_the_second_raise_site_drops_the_context`

Carry the context at the no-answer refusal only, so what a person sees depends on whether they typed a flag

- File: `src/cratekit/cli/gates.py`
- Source: `u49-author.json`, row `G2_the_second_raise_site_drops_the_context`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 1020 against a baseline of 1020
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_the_explicit_inline_refusal_carries_the_context_too`

Old text:

```
            self.state.open_gate = spec.name
            raise DecisionRequired(spec, self.state.run_id, context)

        chosen = inline if inline is not None else (recorded.option if recorded else None)
```

New text:

```
            self.state.open_gate = spec.name
            raise DecisionRequired(spec, self.state.run_id)

        chosen = inline if inline is not None else (recorded.option if recorded else None)
```

### `u270.H1_batch_size_floor`

batching_of: accept a batch form of size zero

- File: `src/cratekit/cli/handlers.py`
- Source: `u270.json`, row `H1_batch_size_floor`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_handlers.py::test_a_batch_form_that_is_not_a_callable_and_a_size_refuses[size-zero]`

Old text:

```
isinstance(size, bool) or size < 1:
```

New text:

```
isinstance(size, bool) or size < 0:
```

### `u270.H2_run_job_drives_the_batch`

run_job: never hand the driver the batch form, so the export goes back to a request a track

- File: `src/cratekit/cli/handlers.py`
- Source: `u270.json`, row `H2_run_job_drives_the_batch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_handlers.py::test_a_worker_naming_a_batch_form_is_driven_in_batches_against_the_frozen_config`

Old text:

```
current_config=current, batch=batching
```

New text:

```
current_config=current, batch=None
```

### `u46-author.H1_binding_removed`

Unbind master, so no verb in the build has a handler at all

- File: `src/cratekit/cli/handlers.py`
- Source: `u46-author.json`, row `H1_binding_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`, `tests/test_job_seam.py`
- Collected: 34 against a baseline of 34
- Kills: 3 (killed)
- Killed:
  - `tests/test_handlers.py::test_every_queued_verb_is_either_bound_or_named_as_unbound`
  - `tests/test_job_seam.py::test_a_driver_killed_inside_the_real_handler_resumes_redoing_exactly_that_item`
  - `tests/test_job_seam.py::test_the_partial_encode_a_kill_leaves_behind_is_in_staging_not_at_the_destination`

Old text:

```
    "master": "cratekit.master.cli:handle",
```

New text:

```
(empty)
```

### `u46-author.H2_is_known_always_true`

Claim every handler key is bound, including the eighteen that are not

- File: `src/cratekit/cli/handlers.py`
- Source: `u46-author.json`, row `H2_is_known_always_true`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`
- Collected: 32 against a baseline of 32
- Kills: 2 (killed)
- Killed:
  - `tests/test_handlers.py::test_every_unbound_verb_says_why_and_every_bound_one_says_nothing`
  - `tests/test_handlers.py::test_is_known_answers_for_a_declared_key_and_an_invented_one`

Old text:

```
    return key in HANDLERS
```

New text:

```
    return True
```

### `u46-author.H3_import_before_refusing`

Import the declared module before checking the key is real, defeating KTD26

- File: `src/cratekit/cli/handlers.py`
- Source: `u46-author.json`, row `H3_import_before_refusing`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_handlers.py::test_resolving_a_handler_key_imports_nothing_a_supervisor_does_not_need`

Old text:

```
def is_known(key: str) -> bool:
```

New text:

```
def is_known(key: str) -> bool:
    importlib.import_module("cratekit.master.cli")
```

### `u46-author.H4_unbound_reason_silent`

Stop saying why a queued verb has no worker

- File: `src/cratekit/cli/handlers.py`
- Source: `u46-author.json`, row `H4_unbound_reason_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`
- Collected: 23216 against a baseline of 23216
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_master_cli.py::test_a_job_show_says_when_a_queued_verb_has_no_worker`

Old text:

```
    return HANDLERS_NOT_YET_BOUND.get(key)
```

New text:

```
    return None
```

### `u46-author.H5_fresh_config`

Hand the handler a freshly loaded configuration instead of the frozen one

- File: `src/cratekit/cli/handlers.py`
- Source: `u46-author.json`, row `H5_fresh_config`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`
- Collected: 32 against a baseline of 32
- Kills: 2 (killed)
- Killed:
  - `tests/test_handlers.py::test_a_worker_naming_a_batch_form_is_driven_in_batches_against_the_frozen_config`
  - `tests/test_handlers.py::test_the_handler_receives_the_frozen_configuration_and_not_the_current_one`

Old text:

```
    frozen = jobs.frozen_config(job)
```

New text:

```
    frozen = config.load()
```

### `u46-author.H7_no_drift`

Never compute drift, so a moved configuration is silently chosen between

- File: `src/cratekit/cli/handlers.py`
- Source: `u46-author.json`, row `H7_no_drift`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_handlers.py::test_a_configuration_that_moved_is_reported_as_drift_rather_than_chosen_between`

Old text:

```
        current: config.Config | None = config.load()
```

New text:

```
        current: config.Config | None = None
```

### `u46-author.H8_drift_wording_dropped`

Report drift without naming what moved

- File: `src/cratekit/cli/handlers.py`
- Source: `u46-author.json`, row `H8_drift_wording_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_handlers.py::test_a_configuration_that_moved_is_reported_as_drift_rather_than_chosen_between`

Old text:

```
                f"configuration changed since this job was queued; it runs against "
                f"the frozen copy. Changed: {', '.join(keys)}"
```

New text:

```
                f"the frozen configuration was used for this run"
```

### `u52-item-derivation.B1_label_import_unbound`

Unbind label.import, leaving a queued job with a worker in neither table

- File: `src/cratekit/cli/handlers.py`
- Source: `u52-item-derivation.json`, row `B1_label_import_unbound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_handlers.py::test_every_queued_verb_is_either_bound_or_named_as_unbound`

Old text:

```
    "label.import": "cratekit.label.cli:handle",
```

New text:

```
(empty)
```

### `u52-item-derivation.B2_sync_labels_unbound`

Unbind sync.labels, leaving a queued sweep with a worker in neither table

- File: `src/cratekit/cli/handlers.py`
- Source: `u52-item-derivation.json`, row `B2_sync_labels_unbound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_handlers.py::test_every_queued_verb_is_either_bound_or_named_as_unbound`

Old text:

```
    "sync.labels": "cratekit.label.cli:handle",
```

New text:

```
(empty)
```

### `u55-collection-reader.R30_scan_handler_bound`

adopt.scan loses its worker, which is the state R-203 records

- File: `src/cratekit/cli/handlers.py`
- Source: `u55-collection-reader.json`, row `R30_scan_handler_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_handlers.py::test_every_queued_verb_is_either_bound_or_named_as_unbound`

Old text:

```
    "adopt.scan": "cratekit.adopt.scan_cli:handle",
```

New text:

```
(empty)
```

### `u56-catalogue-searcher-and-tag-workers.R39_tag_folder_unbound`

The handler key goes back to declaring no worker, which is the state this whole unit exists to leave

- File: `src/cratekit/cli/handlers.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R39_tag_folder_unbound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_handlers.py::test_every_queued_verb_is_either_bound_or_named_as_unbound`

Old text:

```
    "tag.folder": "cratekit.tagging.cli:handle",
```

New text:

```
(empty)
```

### `u56-catalogue-searcher-and-tag-workers.R40_tag_retag_unbound`

The same for the correction verb

- File: `src/cratekit/cli/handlers.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R40_tag_retag_unbound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_handlers.py::test_every_queued_verb_is_either_bound_or_named_as_unbound`

Old text:

```
    "tag.retag": "cratekit.tagging.retag_cli:handle",
```

New text:

```
(empty)
```

### `u58-workers-and-wav.H1_run_unbound`

Drop the analyze.run binding from the handler table

- File: `src/cratekit/cli/handlers.py`
- Source: `u58-workers-and-wav.json`, row `H1_run_unbound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_handlers.py::test_every_queued_verb_is_either_bound_or_named_as_unbound`

Old text:

```
    "analyze.run": "cratekit.analysis.cli:handle_run",

```

New text:

```
(empty)
```

### `u182.M10_dry_run_writes`

_cancel_stale: cancel in a dry run too

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M10_dry_run_writes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_dry_run_lists_three_stale_jobs_and_names_the_keeper_of_the_identical_two`

Old text:

```
            if not dry_run:
                outcome = _cancel_queued(store, hold.job.job_id)
```

New text:

```
            if True:
                outcome = _cancel_queued(store, hold.job.job_id)
```

### `u182.M12_empty_set_copies`

intake_holds: count two jobs with no item as copies of each other

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M12_empty_set_copies`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_two_jobs_with_no_item_are_nobodys_copies`

Old text:

```
                    if mine and other.job_id != job.job_id and sets[other.job_id] == mine
```

New text:

```
                    if other.job_id != job.job_id and sets[other.job_id] == mine
```

### `u182.M13_identity_parse`

playlist_identity: key on the raw source instead of the pass's reading

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M13_identity_parse`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 2 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_stale_cancel_says_what_it_frees[url-typed-by-hand-holds-the-swept-id]`
  - `tests/test_jobs.py::test_the_job_verbs_read_a_playlist_as_the_sweep_records_it`

Old text:

```
        return catalogue.playlist_id(source)
```

New text:

```
        return source
```

### `u182.M13b_sweep_verbatim`

playlist_identity: parse a sweep's own id as if typed, so it no longer agrees with the cursor

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M13b_sweep_verbatim`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_the_job_verbs_read_a_playlist_as_the_sweep_records_it`

Old text:

```
    if (job.payload or {}).get(INTAKE_SWEEP_KEY) == INTAKE_SWEEP_ID:
```

New text:

```
    if False:
```

### `u182.M14c_frees_set_composite`

composite for M14: drop _frees's own set check, the layer that holds when the identity's set branch is gone

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M14c_frees_set_composite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_stale_set_or_hearts_job_names_no_playlist_and_says_what_it_frees[set-job]`

Old text:

```
    if hold.job.handler_key != "intake.playlist":
        return "frees no account playlist: a set job holds none out of a pass"
```

New text:

```
    if False:
        return "frees no account playlist: a set job holds none out of a pass"
```

### `u182.M15_name_fallback`

intake_playlist: name a job queued by hand by nothing rather than by its source

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M15_name_fallback`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 2 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_stale_cancel_says_what_it_frees[unparseable-url]`
  - `tests/test_jobs.py::test_job_show_and_list_name_the_playlist_an_intake_job_was_made_for`

Old text:

```
    return source, source


def playlist_identity
```

New text:

```
    return "", source


def playlist_identity
```

### `u182.M16_naive_instant`

_instant: accept a stamp with no offset, read as if it were UTC

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M16_naive_instant`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_job_whose_queued_time_cannot_be_read_is_never_stale`

Old text:

```
    return moment if moment.tzinfo is not None else None
```

New text:

```
    return moment if moment.tzinfo is not None else moment.replace(tzinfo=timezone.utc)
```

### `u182.M17_summary_playlist`

_summary: carry no playlist field, so job show and job list say nothing of it

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M17_summary_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 3 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_stale_set_or_hearts_job_names_no_playlist_and_says_what_it_frees[hearts-job]`
  - `tests/test_jobs.py::test_a_stale_set_or_hearts_job_names_no_playlist_and_says_what_it_frees[set-job]`
  - `tests/test_jobs.py::test_job_show_and_list_name_the_playlist_an_intake_job_was_made_for`

Old text:

```
    named = intake_playlist(job)
    if named is not None:
```

New text:

```
    named = None
    if named is not None:
```

### `u182.M1_days_floor`

_days: accept zero, so --stale-days 0 offers a job queued a second ago as stale

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M1_days_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_bad_stale_cancel_is_the_parsers_usage_error_and_cancels_nothing[zero-days]`

Old text:

```
    if value < 1:
        raise ValueError(f"{text!r} is not a number of days")
```

New text:

```
    if value < 0:
        raise ValueError(f"{text!r} is not a number of days")
```

### `u182.M2c_running_composite`

composite for M2: drop the running check, the queued check and the listing's lock check together, so a job a live driver runs is offered

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M2c_running_composite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 4 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_blocked_job_or_another_librarys_is_left_by_the_stale_cancel`
  - `tests/test_jobs.py::test_a_dry_run_lists_a_queued_job_a_live_driver_holds_as_left`
  - `tests/test_jobs.py::test_a_job_whose_queued_time_cannot_be_read_is_never_stale`
  - `tests/test_jobs.py::test_the_stale_cancel_cancels_the_stale_keeps_the_newest_copy_and_leaves_the_younger`

Old text:

```
    state = hold.job.state
    if state is jobs.JobState.RUNNING:
        return "running; a stale cancel never touches a running job"
    if state is not jobs.JobState.QUEUED:
        return (
            f"{state}, not queued; if it is stale, cancel it by its id: "
            f"crate job cancel {hold.job.job_id}"
        )
    created = _instant(hold.job.created)
    if created is None:
        return f"its queued time {hold.job.created!r} cannot be read, so its age is unknown"
    if created >= cutoff:
        return f"queued {hold.age_days} day(s) ago, within the {days} day(s) asked"
    try:
        jobs.assert_free(hold.job.job_id)
    except jobs.DriverHeld:
        return "a live driver holds it; a stale cancel never touches a running job"
```

New text:

```
    created = _instant(hold.job.created)
    if created is None:
        return "unknown"
    if created >= cutoff:
        return "young"
```

### `u182.M3_blocked_offered`

_left_reason: offer a blocked job as stale, so a parked job is cancelled

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M3_blocked_offered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_blocked_job_or_another_librarys_is_left_by_the_stale_cancel`

Old text:

```
    if state is not jobs.JobState.QUEUED:
        return (
```

New text:

```
    if state not in (jobs.JobState.QUEUED, jobs.JobState.BLOCKED):
        return (
```

### `u182.M4_unknown_age_stale`

_left_reason: read an unreadable queued time as stale rather than of unknown age

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M4_unknown_age_stale`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_job_whose_queued_time_cannot_be_read_is_never_stale`

Old text:

```
    if created is None:
        return f"its queued time {hold.job.created!r} cannot be read, so its age is unknown"
```

New text:

```
    if created is None:
        return None
```

### `u182.M5_cutoff`

_left_reason: never leave a younger job, so every queued job is stale whatever its age

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M5_cutoff`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 3 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_stale_cancel_says_what_it_frees[another-open-job-holds-it]`
  - `tests/test_jobs.py::test_a_stale_cancel_says_what_it_frees[url-typed-by-hand-holds-the-swept-id]`
  - `tests/test_jobs.py::test_the_stale_cancel_cancels_the_stale_keeps_the_newest_copy_and_leaves_the_younger`

Old text:

```
    if created >= cutoff:
```

New text:

```
    if False:
```

### `u182.M6_listing_lock_check`

_left_reason: drop the live driver check, so a dry run lists a held job for cancel

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M6_listing_lock_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_dry_run_lists_a_queued_job_a_live_driver_holds_as_left`

Old text:

```
        jobs.assert_free(hold.job.job_id)
    except jobs.DriverHeld:
```

New text:

```
        pass
    except jobs.DriverHeld:
```

### `u182.M7_frees_identity`

_frees: match the holder by the raw source again, so a typed URL and a sweep's id read as two playlists

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M7_frees_identity`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_stale_cancel_says_what_it_frees[url-typed-by-hand-holds-the-swept-id]`

Old text:

```
            and hold.identity
            and other.identity == hold.identity
```

New text:

```
            and hold.source
            and other.source == hold.source
```

### `u182.M8_keeper_kept`

_cancel_stale: never keep the newest copy, so every stale copy of a track set is cancelled

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M8_keeper_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 2 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_dry_run_lists_three_stale_jobs_and_names_the_keeper_of_the_identical_two`
  - `tests/test_jobs.py::test_the_stale_cancel_cancels_the_stale_keeps_the_newest_copy_and_leaves_the_younger`

Old text:

```
            if hold.same_tracks and keeper.job_id == hold.job.job_id:
```

New text:

```
            if False:
```

### `u182.M9_keeper_newest`

_cancel_stale: keep the oldest copy of a track set rather than the newest

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M9_keeper_newest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 2 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_dry_run_lists_three_stale_jobs_and_names_the_keeper_of_the_identical_two`
  - `tests/test_jobs.py::test_the_stale_cancel_cancels_the_stale_keeps_the_newest_copy_and_leaves_the_younger`

Old text:

```
                (by_id[other].job for other in (hold.job.job_id, *hold.same_tracks)),
                key=_newest,
```

New text:

```
                (by_id[other].job for other in (hold.job.job_id, *hold.same_tracks)),
                key=lambda held: tuple(-ord(c) for c in held.created),
```

### `u190.L1_no_tail_returns_untouched`

label_sync: run the chain over a go that names no tail

- File: `src/cratekit/cli/label_sync.py`
- Source: `u190.json`, row `L1_no_tail_returns_untouched`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 1020 against a baseline of 1020
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[label.sync]`

Old text:

```
    if land is None:
        return envelope
    cfg
```

New text:

```
    if land is None:
        land = {"folder": "/nowhere", "pass": "none"}
    cfg
```

### `u235.T1_tail_back_to_sixteen_bits`

new_run_id: the tail goes back to token_hex(2), four hex characters, the width the card's failure came from

- File: `src/cratekit/cli/output.py`
- Source: `u235.json`, row `T1_tail_back_to_sixteen_bits`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 1020 against a baseline of 1020
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
- Collected: 1020 against a baseline of 1020
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
- Collected: 1020 against a baseline of 1020
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
- Collected: 1020 against a baseline of 1020
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
- Collected: 1020 against a baseline of 1020
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
- Collected: 1020 against a baseline of 1020
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

### `r83.P1_flush`

R-346: drop the flush from the prompter's writer, the defect as found

- File: `src/cratekit/cli/prompt.py`
- Source: `r83.json`, row `P1_flush`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_question_reaches_a_real_pipe_before_its_answer_is_read`

Old text:

```
    print(text, file=sys.stderr, end="", flush=True)
```

New text:

```
    print(text, file=sys.stderr, end="")
```

### `r83.P2_nothing_entered_raise`

R-347: an empty secret raises the plain PromptUnavailable again

- File: `src/cratekit/cli/prompt.py`
- Source: `r83.json`, row `P2_nothing_entered_raise`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_credential_offer_accepted_and_left_empty_is_the_same_note_as_a_no`
  - `tests/test_doctor.py::test_an_empty_credential_leaves_the_exit_code_to_doctor`

Old text:

```
            raise NothingEntered(f"nothing entered for {question!r}")
```

New text:

```
            raise PromptUnavailable(f"nothing entered for {question!r}")
```

### `u328.S1_a_part_left_out_of_the_table`

ENTRIES: leave the modules part out of the assembly, so adoption, deletion, export and the utilities are not registered

- File: `src/cratekit/cli/registry.py`
- Source: `u328.json`, row `S1_a_part_left_out_of_the_table`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_docs_current.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_handlers.py`
- Collected: 1585 against a baseline of 1682
- Kills: 94 (collect-error)
- Note: collection changed: 1585 collected against a baseline of 1682. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_cli_contract.py::test_a_verb_carrying_a_resume_argv_builder_declares_that_it_queues`
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[sync.land]`
  - `tests/test_cli_contract.py::test_every_declared_module_toggle_is_used_by_at_least_one_verb`
  - `tests/test_cli_contract.py::test_every_feature_row_maps_to_a_verb_at_its_stated_disposition`
  - `tests/test_cli_contract.py::test_every_live_toggle_is_driven_by_the_toggle_test_below`
  - `tests/test_cli_contract.py::test_every_source_entry_point_is_either_mapped_or_written_down_as_cut`
  - `tests/test_cli_contract.py::test_every_unreachable_gate_is_real_and_carries_a_reason`
  - `tests/test_cli_contract.py::test_every_verb_acknowledged_for_conformance_is_refused_without_one_elsewhere`
  - `tests/test_cli_contract.py::test_library_adoption_is_available_in_every_profile`
  - `tests/test_cli_contract.py::test_the_table_is_every_part_in_order_and_each_file_is_under_the_bar`
  - `tests/test_cutover_parity.py::test_a_row_cited_by_nothing_is_a_decision_and_not_an_oversight`
  - `tests/test_cutover_parity.py::test_the_backlog_is_every_owed_row_without_a_landed_verb`
  - `tests/test_cutover_parity.py::test_the_cutover_is_mechanically_possible_and_says_what_is_left`
  - `tests/test_cutover_parity.py::test_the_parity_table_renders_for_a_person`
  - `tests/test_docs_current.py::test_every_verb_a_doc_names_exists_with_its_flags[GUIDE.md]`
  - ... and 79 more, see the JSON sidecar

Old text:

```
    *MODULE_VERBS,

```

New text:

```
(empty)
```

