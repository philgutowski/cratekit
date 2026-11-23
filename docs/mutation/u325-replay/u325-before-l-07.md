# Mutation table: u325-before-l-07

Measured by `scripts/mutate.py` on 2026-11-23 01:39 UTC, branch `HEAD` at `539638eb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22663 collected. pytest invocations for this batch: 37.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:21 UTC for commit `539638ebe629`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 7, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard. 105 row(s) were reused from a prior sidecar and were measured by an earlier process, whose children this run did not watch.

Null control `NULL_CONTROL`: killed 0, collected 22663 against 22663. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u163.W15_lookup_policy` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 284 | 5 | killed |
| `u163.W16_admittable_key` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 284 | 2 | killed |
| `u163.W10_search_convention` | `src/cratekit/intake/native.py` | user | 3 file(s) | 284 | 1 | killed |
| `u163.W11_search_tie` | `src/cratekit/intake/native.py` | user | 3 file(s) | 284 | 1 | killed |
| `u163.W12_readback_active` | `src/cratekit/intake/native.py` | user | 3 file(s) | 284 | 1 | killed |
| `u163.W13_identified_words` | `src/cratekit/intake/native.py` | user | 3 file(s) | 284 | 1 | killed |
| `u163.W14_album_artist_link` | `src/cratekit/intake/native.py` | user | 3 file(s) | 284 | 2 | killed |
| `u163.W1_words_planned` | `src/cratekit/intake/native.py` | user | 3 file(s) | 284 | 15 | killed |
| `u163.W2_first_value` | `src/cratekit/intake/native.py` | user | 3 file(s) | 284 | 1 | killed |
| `u163.W3_year_digits` | `src/cratekit/intake/native.py` | user | 3 file(s) | 284 | 2 | killed |
| `u163.W4_year_written` | `src/cratekit/intake/native.py` | user | 3 file(s) | 284 | 1 | killed |
| `u163.W5_album_artist_mint` | `src/cratekit/intake/native.py` | user | 3 file(s) | 284 | 1 | killed |
| `u163.W6_album_by_artist` | `src/cratekit/intake/native.py` | user | 3 file(s) | 284 | 1 | killed |
| `u163.W7_unmoved` | `src/cratekit/intake/native.py` | user | 3 file(s) | 284 | 1 | killed |
| `u163.W8_mint_once` | `src/cratekit/intake/native.py` | user | 3 file(s) | 284 | 1 | killed |
| `u163.W9_creations_named` | `src/cratekit/intake/native.py` | user | 3 file(s) | 284 | 32 | killed |
| `u107-c.S19_approved_superseded` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `r515-operator.S8_short_of_keeps_zero` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `r515-operator.S9_question_no_short` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u107-a.S01_record_not_json` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 2 | killed |
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
| `r675.G10_repair_apply_asks_with_no_candidates` | `src/cratekit/intake/repair_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r675.G9_repair_plan_asks_with_no_candidates` | `src/cratekit/intake/repair_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r675.E2_key_not_casefolded` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 3 | killed |
| `r675.E4_tombstones_dropped_from_the_read` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 4 | killed |
| `r675.G11_prefixes_dropped` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 3 | killed |
| `r675.G12_could_name_uncapped` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r675.G13_as_recorded_key_dropped` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 2 | killed |
| `r675.G14_remapped_key_dropped` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r675.G15_first_location_dropped` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 4 | killed |
| `r675.G16_locations_uncapped` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r675.G17_prefixes_uncapped` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r675.G18_held_candidates_asked_about` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r675.G19_second_step_dropped` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r675.G1_every_dark_row_refuses` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 6 | killed |
| `r675.G2_row_leaf_not_keyed` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 15 | killed |
| `r675.G3_candidate_leaf_not_keyed` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 15 | killed |
| `r675.G4_could_name_empty` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 7 | killed |
| `r675.G5_leaf_compared_as_whole_path` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 16 | killed |
| `r675.G6_plan_asks_with_no_candidates` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r675.G7_apply_asks_with_no_candidates` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r675.G8_count_reworded` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 3 | killed |
| `r669.E1_key_from_the_head_only` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r669.E2_body_from_the_title_tag` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 26 | killed |
| `r669.E3_lossy_from_the_stem_only` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 3 | killed |
| `r669.G10_apply_trusts_the_plan_for_the_hold` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r669.G11_gate_shows_nothing` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 3 | killed |
| `r669.G12_shown_count_is_every_item` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 2 | killed |
| `r669.G13_referenced_held_without_a_reason` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r669.G17_held_file_never_referenced` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r669.G18_drifted_name_renamed_anyway` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r669.G19_no_step_for_unnamed` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r669.G1_identifier_is_no_letters` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r669.G20_screen_uncapped` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r669.G21_artist_alone_when_no_title_tag` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r669.G2_title_alone_when_no_artist` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 5 | killed |
| `r669.G3_artist_alone_when_title_is_a_head` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r669.G4_order_swapped` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 10 | killed |
| `r669.G5_first_artist_only` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 2 | killed |
| `r669.G6_title_head_kept_in_body` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 2 | killed |
| `r669.G7_unnamed_left_out_of_the_plan` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 9 | killed |
| `r669.G8_digest_ignores_unnamed` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 1 | killed |
| `r669.G9_unnamed_not_owed_on_apply` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 131 | 3 | killed |
| `r572.Z1_set_drop_album` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `r837-b.B1_ref_only_from_the_provider` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `r837-b.B2_isrc_route` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `r837-b.B3_accepted_in_review` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 56 | 2 | killed |
| `r837-b.B4_sole_exact_listed` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 56 | 20 | killed |
| `r837-b.B5_unmatched_warning` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 56 | 2 | killed |
| `r879-b.S10_unnamed_exact_said_to_resemble_nothing` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `r879-b.S4_several_codes_take_one` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `r879-b.S5_codes_from_every_version` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `r879-b.S6_absent_music_folder_unsaid` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `r879-b.S7_library_before_a_persons_answer` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `r879-b.S8_several_needs_three` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 56 | 2 | killed |
| `r879-b.S9_ambiguous_full_said_as_bound` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `u142.S8_gate_stale_said_without_a_write` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `r879-a.C10_offset_counts_pages_not_rows` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 4 | killed |
| `r879-a.C2_walk_ignores_short_page` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 6 | killed |
| `r879-a.C3_settled_early_without_ambiguity` | `src/cratekit/intake/candidates.py` | maintainer | 1 file(s) | 56 | 2 | killed |
| `r879-a.C4_settled_early_without_unreadable` | `src/cratekit/intake/candidates.py` | maintainer | 1 file(s) | 56 | 1 | killed |
| `r879-a.C6_settled_early_without_several` | `src/cratekit/intake/candidates.py` | maintainer | 1 file(s) | 56 | 1 | killed |
| `r879-a.C7_bound_off_by_one` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 2 | killed |
| `r879-a.C9_read_pages_forgets_last_page` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 5 | killed |
| `r879-b.C5r_settled_early_without_unnamed_exact` | `src/cratekit/intake/candidates.py` | maintainer | 1 file(s) | 56 | 1 | killed |
| `r879-b.C8r_ceiling_coefficient` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 1 | killed |
| `r923.N12_digest_drops_values` | `src/cratekit/write/row_defaults.py` | maintainer | 1 file(s) | 22663 | 0 (promoted) | zero |
| `r1308.M10_count_unchecked` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 22663 | 0 (promoted) | zero |
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
| `r381-b.M12_add_legacy_any_name` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 1 | killed |
| `r381.M10_by_id_no_follow` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 1 | killed |
| `r381.M11_add_ignores_legacy` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 1 | killed |
| `r381.M1_fold_only_slug` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 13 | killed |
| `r381.M2_no_umlaut_table` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 6 | killed |
| `r381.M3_keep_combining_marks` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 10 | killed |

## Zero rows and what they owe

- `r923.N12_digest_drops_values` (maintainer facing): maintainer facing, composite not required
- `r1308.M10_count_unchecked` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `u163.W15_lookup_policy`

guard_violations: wave an admitted lookup row through without the creation policy

- File: `src/cratekit/core/rb_writer.py`
- Source: `u163.json`, row `W15_lookup_policy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 284 against a baseline of 284
- Kills: 5 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_an_admitted_lookup_row_declaring_an_analysis_column_is_refused[Analysed]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_lookup_row_declaring_an_analysis_column_is_refused[AnalysisDataPath]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_lookup_row_declaring_an_analysis_column_is_refused[AnalysisUpdated]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_lookup_row_declaring_an_analysis_column_is_refused[BPM]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_lookup_row_declaring_an_analysis_column_is_refused[CueUpdated]`

Old text:

```
            declared = {column for column in columns if column in GRIDLESS_ON_CREATE_COLUMNS}
            if declared:
                violations.append(
                    f"creates a row in {table!r} declaring analysis column(s): "
                    f"{sorted(declared)}; a row this product creates is gridless and "
                    f"rekordbox derives the grid from the audio"
                )
            continue
        if table == CONTENT_TABLE:
```

New text:

```
            continue
        if table == CONTENT_TABLE:
```

### `u163.W16_admittable_key`

ADMITTABLE_ROW_TABLES: admit djmdKey beside the lookups

- File: `src/cratekit/core/rb_writer.py`
- Source: `u163.json`, row `W16_admittable_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 284 against a baseline of 284
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_creation_naming_the_key_table_is_refused`
  - `tests/test_rb_writer_guard.py::test_the_admittable_tables_are_exactly_the_content_table_and_the_three_lookups`

Old text:

```
ADMITTABLE_ROW_TABLES = frozenset({CONTENT_TABLE, *LOOKUP_TABLES})
```

New text:

```
ADMITTABLE_ROW_TABLES = frozenset({CONTENT_TABLE, *LOOKUP_TABLES, "djmdKey"})
```

### `u163.W10_search_convention`

_Resolver._shaped: store NULL in SearchStr whatever the library's convention

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W10_search_convention`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_a_mint_follows_the_librarys_searchstr_convention`

Old text:

```
        return replace(word, search=word.name if convention == SEARCH_NAME else convention)
```

New text:

```
        return replace(word, search=None)
```

### `u163.W11_search_tie`

search_convention: answer the first ranked convention on a tie

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W11_search_tie`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_a_tied_searchstr_convention_mints_null`

Old text:

```
    if not ranked or (len(ranked) > 1 and ranked[0][1] == ranked[1][1]):
```

New text:

```
    if not ranked:
```

### `u163.W12_readback_active`

_words_back: read the artist through any row, tombstones included

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W12_readback_active`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_the_read_back_takes_no_word_through_a_tombstoned_lookup_row`

Old text:

```
            f"LEFT JOIN {rb_writer.ARTIST_TABLE} a ON a.ID = c.{ARTIST_COLUMN} AND a.{active} "
```

New text:

```
            f"LEFT JOIN {rb_writer.ARTIST_TABLE} a ON a.ID = c.{ARTIST_COLUMN} "
```

### `u163.W13_identified_words`

assert_rows_identified: never compare the words read back

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W13_identified_words`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_a_landed_row_whose_word_reads_back_wrong_is_refused`

Old text:

```
        if row.words.get(column) != want
```

New text:

```
        if False
```

### `u163.W14_album_artist_link`

_Mints._mint: mint an album with no album artist

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W14_album_artist_link`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 284 against a baseline of 284
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_a_word_the_library_lacks_is_minted_and_linked_in_the_one_commit`
  - `tests/test_intake_land_words.py::test_an_album_whose_album_artist_is_minted_is_minted_beside_a_namesake_with_none`

Old text:

```
        if word.table == rb_writer.ALBUM_TABLE:
            columns[ALBUM_ARTIST]
```

New text:

```
        if False:
            columns[ALBUM_ARTIST]
```

### `u163.W1_words_planned`

plan_rows: never plan the words, so no row carries artist, album, genre or year

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W1_words_planned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 284 against a baseline of 284
- Kills: 15 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_gate_screen_names_every_row_its_columns_the_playlist_and_the_database`
  - `tests/test_intake_land_words.py::test_a_file_with_no_artist_leaves_the_column_empty`
  - `tests/test_intake_land_words.py::test_a_mint_follows_the_librarys_searchstr_convention`
  - `tests/test_intake_land_words.py::test_a_multi_value_id3_frame_lands_its_first_value_as_the_word`
  - `tests/test_intake_land_words.py::test_a_tied_searchstr_convention_mints_null`
  - `tests/test_intake_land_words.py::test_a_tombstoned_namesake_is_skipped_for_the_active_row_after_it`
  - `tests/test_intake_land_words.py::test_a_word_minted_by_another_hand_since_the_plan_refuses_and_writes_nothing`
  - `tests/test_intake_land_words.py::test_a_word_the_library_holds_links_its_active_row_and_mints_nothing`
  - `tests/test_intake_land_words.py::test_a_word_the_library_lacks_is_minted_and_linked_in_the_one_commit`
  - `tests/test_intake_land_words.py::test_a_word_whose_only_namesake_is_a_tombstone_is_minted`
  - `tests/test_intake_land_words.py::test_adoption_reads_the_landed_rows_genre_with_rekordbox_closed`
  - `tests/test_intake_land_words.py::test_an_album_links_the_one_its_album_artist_holds`
  - `tests/test_intake_land_words.py::test_an_album_whose_album_artist_is_minted_is_minted_beside_a_namesake_with_none`
  - `tests/test_intake_land_words.py::test_the_read_back_takes_no_word_through_a_tombstoned_lookup_row`
  - `tests/test_intake_land_words.py::test_two_files_with_one_new_artist_mint_it_once`

Old text:

```
    rows = _words_plan(db, rows)

```

New text:

```
    rows = rows

```

### `u163.W2_first_value`

_word: keep the NUL joined ID3 value whole (round one's fix)

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W2_first_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_a_multi_value_id3_frame_lands_its_first_value_as_the_word`

Old text:

```
    first = (value or "").split("\x00")[0]
```

New text:

```
    first = value or ""
```

### `u163.W3_year_digits`

year_of: accept any four characters as a year

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W3_year_digits`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 284 against a baseline of 284
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_the_year_is_the_four_digits_the_date_tag_opens_with[0000-None]`
  - `tests/test_intake_land_words.py::test_the_year_is_the_four_digits_the_date_tag_opens_with[circa 2021-None]`

Old text:

```
    if len(head) != 4 or not head.isdigit() or int(head) == 0:
```

New text:

```
    if len(head) != 4:
```

### `u163.W4_year_written`

_Mints.link: drop the ReleaseYear write

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W4_year_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_a_word_the_library_lacks_is_minted_and_linked_in_the_one_commit`

Old text:

```
        if row.year is not None:
            setattr(content, YEAR_COLUMN, row.year)
```

New text:

```
        if False:
            setattr(content, YEAR_COLUMN, row.year)
```

### `u163.W5_album_artist_mint`

_active_album_id: look up an album whose album artist is minted, instead of minting it

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W5_album_artist_mint`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_an_album_whose_album_artist_is_minted_is_minted_beside_a_namesake_with_none`

Old text:

```
    if album_artist is not None and not album_artist.row_id:
        return ""
```

New text:

```
    if False:
        return ""
```

### `u163.W6_album_by_artist`

_active_album_id: find the album by name alone, ignoring its album artist

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W6_album_by_artist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_an_album_links_the_one_its_album_artist_holds`

Old text:

```
        if str(getattr(row, ALBUM_ARTIST, None) or "") == want
```

New text:

```
        if True
```

### `u163.W7_unmoved`

_assert_words_unmoved: never refuse a word that moved since the plan

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W7_unmoved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_a_word_minted_by_another_hand_since_the_plan_refuses_and_writes_nothing`

Old text:

```
            if _rows_of(now) != _rows_of(word):
```

New text:

```
            if False:
```

### `u163.W8_mint_once`

_Mints.id_of: mint a new word again for every row

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W8_mint_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_two_files_with_one_new_artist_mint_it_once`

Old text:

```
        if key not in self._made:
            self._made[key] = self._mint(word)
```

New text:

```
        if True:
            self._made[key] = self._mint(word)
```

### `u163.W9_creations_named`

apply_rows: name only the content table in creations, so a mint is refused

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W9_creations_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 284 against a baseline of 284
- Kills: 32 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_file_whose_tags_resolve_to_no_sub_stays_in_staging_on_the_native_medium_too`
  - `tests/test_intake_land_native.py::test_a_landing_given_a_pass_names_it_on_the_record_sync_mark_reads`
  - `tests/test_intake_land_native.py::test_a_landing_given_no_pass_names_none`
  - `tests/test_intake_land_native.py::test_a_landing_that_adds_no_row_needs_no_majority`
  - `tests/test_intake_land_native.py::test_a_row_whose_content_link_did_not_take_is_refused_after_the_commit`
  - `tests/test_intake_land_native.py::test_a_row_whose_file_id_did_not_take_is_refused_after_the_commit_naming_the_session`
  - `tests/test_intake_land_native.py::test_a_second_approved_run_over_the_landed_files_adds_nothing`
  - `tests/test_intake_land_native.py::test_a_suffix_the_database_has_no_type_for_is_left_in_staging_and_the_batch_lands`
  - `tests/test_intake_land_native.py::test_after_the_write_no_analysis_value_exists_on_the_new_rows_column_by_column`
  - `tests/test_intake_land_native.py::test_an_analysis_product_row_for_the_new_row_is_refused_from_sql_before_the_commit`
  - `tests/test_intake_land_native.py::test_an_answer_continued_over_the_file_it_was_given_over_lands`
  - `tests/test_intake_land_native.py::test_folder_path_is_stored_under_the_base_drive_rekordbox_records`
  - `tests/test_intake_land_native.py::test_the_rows_carry_every_default_rekordbox_writes_on_a_row_it_makes`
  - `tests/test_intake_land_native.py::test_the_rows_carry_the_landed_files_inode_as_their_file_id`
  - ... and 17 more, see the JSON sidecar

Old text:

```
                db, creations=(rb_writer.CONTENT_TABLE, *mints.tables())
```

New text:

```
                db, creations=(rb_writer.CONTENT_TABLE,)
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

### `u107-a.S01_record_not_json`

sync_cli.load_record: read a record that is not JSON as an empty one, so every question is asked again and every answer is lost

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-a.json`, row `S01_record_not_json`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_record_that_cannot_be_read_refuses_rather_than_asking_everything_again`
  - `tests/test_label_sync.py::test_the_labels_sweep_refuses_an_unreadable_record_before_any_login`

Old text:

```
        raise _unusable(path, "it is not JSON") from exc
```

New text:

```
        return _empty()
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

### `r675.G10_repair_apply_asks_with_no_candidates`

repair_cli apply: the repair verb's read after the gate hands the guard no candidates

- File: `src/cratekit/intake/repair_cli.py`
- Source: `r675.json`, row `G10_repair_apply_asks_with_no_candidates`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_dark_row_recorded_after_the_gate_refuses_the_repair_before_any_rename`

Old text:

```
        naming_cli.referenced_keys(cfg, renaming=[Path(item["path"]) for item in renames])
```

New text:

```
        naming_cli.referenced_keys(cfg, renaming=[])
```

### `r675.G9_repair_plan_asks_with_no_candidates`

repair_cli plan: the repair verb's plan read hands the guard no candidates

- File: `src/cratekit/intake/repair_cli.py`
- Source: `r675.json`, row `G9_repair_plan_asks_with_no_candidates`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_dark_row_under_a_proposal_name_refuses_the_repair_plan_too`

Old text:

```
        naming_cli.referenced_keys(cfg, renaming=[path for _, path in candidates])
```

New text:

```
        naming_cli.referenced_keys(cfg, renaming=[])
```

### `r675.E2_key_not_casefolded`

existing layer: the referenced key keeps case, so a row differing from the file only in case no longer protects it

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `E2_key_not_casefolded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 3 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_case_variant_of_the_name_still_protects_its_file`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_matched_to_a_candidate_by_name_ignoring_case`
  - `tests/test_naming_apply_cli.py::test_two_targets_differing_only_in_case_are_one_name`

Old text:

```
    return locations.norm_for_compare(path).casefold()
```

New text:

```
    return locations.norm_for_compare(path)
```

### `r675.E4_tombstones_dropped_from_the_read`

existing layer: _recorded reads live rows only, so a tombstone neither protects its file nor counts as dark

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `E4_tombstones_dropped_from_the_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 4 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_dark_tombstone_under_a_candidate_name_still_refuses`
  - `tests/test_naming_apply_cli.py::test_a_tombstoned_row_still_protects_its_file`
  - `tests/test_naming_apply_cli.py::test_every_unmapped_row_is_counted_and_the_first_is_named`
  - `tests/test_naming_apply_cli.py::test_two_dark_rows_under_one_candidate_name_each_name_it`

Old text:

```
            return tuple(str(row.FolderPath or "") for row in handle.get_content())
```

New text:

```
            return tuple(
                str(row.FolderPath or "")
                for row in handle.get_content()
                if not row.rb_local_deleted
            )
```

### `r675.G11_prefixes_dropped`

_unmapped_refusal: the grouped prefixes left out of the detail

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G11_prefixes_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 3 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_under_an_unmapped_volume_refuses_and_renames_nothing`
  - `tests/test_naming_apply_cli.py::test_every_unmapped_row_is_counted_and_the_first_is_named`
  - `tests/test_naming_apply_cli.py::test_the_refusal_counts_every_row_and_lists_no_more_than_twenty`

Old text:

```
            "unmapped_prefixes": prefixes[:20],
```

New text:

```
            "unmapped_prefixes": [],
```

### `r675.G12_could_name_uncapped`

_unmapped_refusal: the pairs list uncapped, so a fresh setup's 9937 dark rows are 9937 pairs in one envelope

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G12_could_name_uncapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_refusal_counts_every_row_and_lists_no_more_than_twenty`

Old text:

```
            "could_name": [{"row": decoded, "files": named} for decoded, named in dark[:20]],
```

New text:

```
            "could_name": [{"row": decoded, "files": named} for decoded, named in dark],
```

### `r675.G13_as_recorded_key_dropped`

_referenced: a row's as recorded key is not added, so a row outside every rule whose file exists no longer protects it

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G13_as_recorded_key_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_file_recorded_through_a_link_is_protected_through_that_link`
  - `tests/test_naming_apply_cli.py::test_a_root_outside_the_library_is_still_checked`

Old text:

```
        keys.add(_key(decoded))
        if resolved.path is not None:
```

New text:

```
        if resolved.path is not None:
```

### `r675.G14_remapped_key_dropped`

_referenced: a row's remapped key is not added, so a row under a mapped old volume name no longer protects its file

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G14_remapped_key_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_under_a_remapped_volume_still_protects_its_file[prefix_map0]`

Old text:

```
        if resolved.path is not None:
            keys.add(_key(resolved.path))
        elif
```

New text:

```
        if resolved.path is not None:
            pass
        elif
```

### `r675.G15_first_location_dropped`

_unmapped_refusal: the first dark location no longer quoted in the message

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G15_first_location_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 4 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_under_an_unmapped_volume_refuses_and_renames_nothing`
  - `tests/test_naming_apply_cli.py::test_a_rule_differing_from_the_recorded_volume_only_in_case_refuses[prefix_map0]`
  - `tests/test_naming_apply_cli.py::test_every_unmapped_row_is_counted_and_the_first_is_named`
  - `tests/test_naming_apply_cli.py::test_the_refusal_names_the_decoded_location_a_rule_is_matched_against`

Old text:

```
        f"of a file this plan would rename, the first of them {dark[0][0]}, so "
```

New text:

```
        f"of a file this plan would rename, so "
```

### `r675.G16_locations_uncapped`

_unmapped_refusal: the locations list uncapped

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G16_locations_uncapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_refusal_counts_every_row_and_lists_no_more_than_twenty`

Old text:

```
            "unmapped_locations": locations_listed[:20],
```

New text:

```
            "unmapped_locations": locations_listed,
```

### `r675.G17_prefixes_uncapped`

_unmapped_refusal: the prefixes list uncapped

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G17_prefixes_uncapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_refusal_counts_every_row_and_lists_no_more_than_twenty`

Old text:

```
            "unmapped_prefixes": prefixes[:20],
```

New text:

```
            "unmapped_prefixes": prefixes,
```

### `r675.G18_held_candidates_asked_about`

_referenced: a candidate the resolved rows hold is still indexed, so a dark row under its name refuses although the file is never renamed

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G18_held_candidates_asked_about`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_dark_row_under_a_held_candidate_name_refuses_nothing`

Old text:

```
        if not _is_referenced(path, referenced):
            leaves.setdefault(_key(path.name), []).append(str(path))
```

New text:

```
        leaves.setdefault(_key(path.name), []).append(str(path))
```

### `r675.G19_second_step_dropped`

_unmapped_refusal: the step for a row no rule can place is left out, so a person with no volume to map is told to map one

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G19_second_step_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_under_an_unmapped_volume_refuses_and_renames_nothing`

Old text:

```
            "when no volume is missing, the row names a file that is gone and no "
            "rule can place it: rename the file it could be naming by hand, or "
            "remove that track in rekordbox, then run this again",
        ),
```

New text:

```
        ),
```

### `r675.G1_every_dark_row_refuses`

_referenced: the leaf test dropped, so every dark row refuses, which is the behaviour R-675 measured at 582 rows

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G1_every_dark_row_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 6 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_dark_row_under_another_name_lets_the_repair_run`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_only_asked_about_the_files_being_renamed`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_under_a_held_candidate_name_refuses_nothing`
  - `tests/test_naming_apply_cli.py::test_a_dark_tombstone_under_another_name_refuses_nothing`
  - `tests/test_naming_apply_cli.py::test_a_gone_file_under_another_name_refuses_nothing`
  - `tests/test_naming_apply_cli.py::test_a_streamed_track_recorded_as_a_catalogue_path_refuses_nothing`

Old text:

```
        if (named := leaves.get(_key(Path(decoded).name)))
```

New text:

```
        if (named := leaves.get(_key(Path(decoded).name)) or [decoded])
```

### `r675.G2_row_leaf_not_keyed`

_referenced: the dark row's leaf is looked up as spelled, so a case or composition variant of a candidate's name is another name

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G2_row_leaf_not_keyed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 15 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_dark_row_recorded_after_the_gate_refuses_the_repair_before_any_rename`
  - `tests/intake/test_repair_apply.py::test_a_dark_row_under_a_proposal_name_refuses_the_repair`
  - `tests/intake/test_repair_apply.py::test_a_dark_row_under_a_proposal_name_refuses_the_repair_plan_too`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_matched_across_folders_by_leaf_alone`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_matched_to_a_candidate_by_name_ignoring_case`
  - `tests/test_naming_apply_cli.py::test_a_dark_tombstone_under_a_candidate_name_still_refuses`
  - `tests/test_naming_apply_cli.py::test_a_gone_file_under_a_folder_on_this_machine_refuses_under_a_candidate_name`
  - `tests/test_naming_apply_cli.py::test_a_row_recording_a_link_to_nothing_is_dark`
  - `tests/test_naming_apply_cli.py::test_a_row_that_goes_unmapped_after_the_gate_refuses_before_any_rename`
  - `tests/test_naming_apply_cli.py::test_a_row_under_an_unmapped_volume_refuses_and_renames_nothing`
  - `tests/test_naming_apply_cli.py::test_a_rule_differing_from_the_recorded_volume_only_in_case_refuses[prefix_map0]`
  - `tests/test_naming_apply_cli.py::test_an_unmapped_row_refuses_the_plan_too`
  - `tests/test_naming_apply_cli.py::test_every_unmapped_row_is_counted_and_the_first_is_named`
  - `tests/test_naming_apply_cli.py::test_the_refusal_names_the_decoded_location_a_rule_is_matched_against`
  - `tests/test_naming_apply_cli.py::test_two_dark_rows_under_one_candidate_name_each_name_it`

Old text:

```
        if (named := leaves.get(_key(Path(decoded).name)))
```

New text:

```
        if (named := leaves.get(Path(decoded).name))
```

### `r675.G3_candidate_leaf_not_keyed`

_referenced: the candidates are indexed by their name as spelled, so a keyed lookup never finds one

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G3_candidate_leaf_not_keyed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 15 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_dark_row_recorded_after_the_gate_refuses_the_repair_before_any_rename`
  - `tests/intake/test_repair_apply.py::test_a_dark_row_under_a_proposal_name_refuses_the_repair`
  - `tests/intake/test_repair_apply.py::test_a_dark_row_under_a_proposal_name_refuses_the_repair_plan_too`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_matched_across_folders_by_leaf_alone`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_matched_to_a_candidate_by_name_ignoring_case`
  - `tests/test_naming_apply_cli.py::test_a_dark_tombstone_under_a_candidate_name_still_refuses`
  - `tests/test_naming_apply_cli.py::test_a_gone_file_under_a_folder_on_this_machine_refuses_under_a_candidate_name`
  - `tests/test_naming_apply_cli.py::test_a_row_recording_a_link_to_nothing_is_dark`
  - `tests/test_naming_apply_cli.py::test_a_row_that_goes_unmapped_after_the_gate_refuses_before_any_rename`
  - `tests/test_naming_apply_cli.py::test_a_row_under_an_unmapped_volume_refuses_and_renames_nothing`
  - `tests/test_naming_apply_cli.py::test_a_rule_differing_from_the_recorded_volume_only_in_case_refuses[prefix_map0]`
  - `tests/test_naming_apply_cli.py::test_an_unmapped_row_refuses_the_plan_too`
  - `tests/test_naming_apply_cli.py::test_every_unmapped_row_is_counted_and_the_first_is_named`
  - `tests/test_naming_apply_cli.py::test_the_refusal_names_the_decoded_location_a_rule_is_matched_against`
  - `tests/test_naming_apply_cli.py::test_two_dark_rows_under_one_candidate_name_each_name_it`

Old text:

```
        leaves.setdefault(_key(path.name), []).append(str(path))
```

New text:

```
        leaves.setdefault(path.name, []).append(str(path))
```

### `r675.G4_could_name_empty`

_referenced: the candidates in doubt are never collected, so the refusal names rows and no files

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G4_could_name_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 7 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_dark_row_recorded_after_the_gate_refuses_the_repair_before_any_rename`
  - `tests/intake/test_repair_apply.py::test_a_dark_row_under_a_proposal_name_refuses_the_repair`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_matched_across_folders_by_leaf_alone`
  - `tests/test_naming_apply_cli.py::test_a_dark_tombstone_under_a_candidate_name_still_refuses`
  - `tests/test_naming_apply_cli.py::test_a_gone_file_under_a_folder_on_this_machine_refuses_under_a_candidate_name`
  - `tests/test_naming_apply_cli.py::test_every_unmapped_row_is_counted_and_the_first_is_named`
  - `tests/test_naming_apply_cli.py::test_two_dark_rows_under_one_candidate_name_each_name_it`

Old text:

```
            "could_name": [{"row": decoded, "files": named} for decoded, named in dark[:20]],
```

New text:

```
            "could_name": [{"row": decoded, "files": []} for decoded, named in dark[:20]],
```

### `r675.G5_leaf_compared_as_whole_path`

_referenced: the dark row is looked up by its whole decoded path rather than its leaf, so no row under another volume ever matches

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G5_leaf_compared_as_whole_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 16 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_dark_row_recorded_after_the_gate_refuses_the_repair_before_any_rename`
  - `tests/intake/test_repair_apply.py::test_a_dark_row_under_a_proposal_name_refuses_the_repair`
  - `tests/intake/test_repair_apply.py::test_a_dark_row_under_a_proposal_name_refuses_the_repair_plan_too`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_matched_across_folders_by_leaf_alone`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_matched_to_a_candidate_by_name_ignoring_case`
  - `tests/test_naming_apply_cli.py::test_a_dark_tombstone_under_a_candidate_name_still_refuses`
  - `tests/test_naming_apply_cli.py::test_a_gone_file_under_a_folder_on_this_machine_refuses_under_a_candidate_name`
  - `tests/test_naming_apply_cli.py::test_a_row_recording_a_link_to_nothing_is_dark`
  - `tests/test_naming_apply_cli.py::test_a_row_that_goes_unmapped_after_the_gate_refuses_before_any_rename`
  - `tests/test_naming_apply_cli.py::test_a_row_under_an_unmapped_volume_refuses_and_renames_nothing`
  - `tests/test_naming_apply_cli.py::test_a_rule_differing_from_the_recorded_volume_only_in_case_refuses[prefix_map0]`
  - `tests/test_naming_apply_cli.py::test_an_unmapped_row_refuses_the_plan_too`
  - `tests/test_naming_apply_cli.py::test_every_unmapped_row_is_counted_and_the_first_is_named`
  - `tests/test_naming_apply_cli.py::test_the_refusal_counts_every_row_and_lists_no_more_than_twenty`
  - `tests/test_naming_apply_cli.py::test_the_refusal_names_the_decoded_location_a_rule_is_matched_against`
  - ... and 1 more, see the JSON sidecar

Old text:

```
        if (named := leaves.get(_key(Path(decoded).name)))
```

New text:

```
        if (named := leaves.get(_key(decoded)))
```

### `r675.G6_plan_asks_with_no_candidates`

_plan_for: the plan's read hands the guard no candidates, so the plan never refuses and only the apply's read can

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G6_plan_asks_with_no_candidates`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_an_unmapped_row_refuses_the_plan_too`

Old text:

```
        _referenced(_recorded(cfg), cfg=cfg, renaming=[path for path, _ in candidates])
```

New text:

```
        _referenced(_recorded(cfg), cfg=cfg, renaming=[])
```

### `r675.G7_apply_asks_with_no_candidates`

name_apply: the read after the gate hands the guard no candidates, so a row that went dark while the gate waited is not seen

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G7_apply_asks_with_no_candidates`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_that_goes_unmapped_after_the_gate_refuses_before_any_rename`

Old text:

```
            _recorded(cfg), cfg=cfg, renaming=[Path(item["path"]) for item in renames]
```

New text:

```
            _recorded(cfg), cfg=cfg, renaming=[]
```

### `r675.G8_count_reworded`

_unmapped_refusal: the count's noun reworded, so the message no longer says what was counted

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G8_count_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 131 against a baseline of 131
- Kills: 3 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_under_an_unmapped_volume_refuses_and_renames_nothing`
  - `tests/test_naming_apply_cli.py::test_every_unmapped_row_is_counted_and_the_first_is_named`
  - `tests/test_naming_apply_cli.py::test_the_refusal_counts_every_row_and_lists_no_more_than_twenty`

Old text:

```
    rows = "collection row records" if count == 1 else "collection rows record"
```

New text:

```
    rows = "row records" if count == 1 else "rows record"
```

### `r669.E1_key_from_the_head_only`

Ignore the initialkey tag and take the key from the head alone (U39)

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `E1_key_from_the_head_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_tag_key_wins_over_a_stale_head_and_the_pass_converges`

Old text:

```
    key = tag_key if tag_key and naming.is_camelot(tag_key) else head.get("key")
```

New text:

```
    key = head.get("key")
```

### `r669.E2_body_from_the_title_tag`

Take the filename body from the title tag, the R-168 truncation, for every file

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `E2_body_from_the_title_tag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 26 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_camelot_key_tag_without_a_tempo_still_renders_no_head`
  - `tests/test_naming_apply_cli.py::test_a_composed_body_over_the_ceiling_is_fitted_not_left_as_a_number`
  - `tests/test_naming_apply_cli.py::test_a_deduping_rename_converges_on_one_pass`
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_a_head_inside_the_title_tag_is_not_composed_into_the_body`
  - `tests/test_naming_apply_cli.py::test_a_name_over_the_byte_ceiling_is_truncated_not_rebuilt`
  - `tests/test_naming_apply_cli.py::test_a_referenced_file_does_not_hold_a_name_it_will_never_take`
  - `tests/test_naming_apply_cli.py::test_a_rename_never_replaces_the_body_with_the_title_tag`
  - `tests/test_naming_apply_cli.py::test_a_slash_in_a_tag_takes_the_body_form_of_a_segment`
  - `tests/test_naming_apply_cli.py::test_a_stem_carrying_text_is_not_recomposed_from_its_tags`
  - `tests/test_naming_apply_cli.py::test_a_tag_edited_while_the_gate_waits_is_not_renamed_to_a_name_nobody_saw`
  - `tests/test_naming_apply_cli.py::test_a_target_a_collider_holds_is_held_back_too`
  - `tests/test_naming_apply_cli.py::test_a_target_another_mover_still_holds_is_promised_and_then_reported`
  - `tests/test_naming_apply_cli.py::test_a_trailing_segment_repeating_the_lead_is_still_deduped`
  - `tests/test_naming_apply_cli.py::test_a_trailing_segment_that_only_starts_with_the_lead_survives`
  - ... and 11 more, see the JSON sidecar

Old text:

```
    stem = naming.strip_head(path.stem, template=template)
    unnamed = None
```

New text:

```
    stem = naming.strip_head(title, template=template)
    unnamed = None
```

### `r669.E3_lossy_from_the_stem_only`

Read the lossy marker off the filename alone and miss one carried by the title

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `E3_lossy_from_the_stem_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 3 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_marker_in_the_title_alone_is_still_recovered`
  - `tests/test_naming_apply_cli.py::test_a_target_a_collider_holds_is_held_back_too`
  - `tests/test_naming_apply_cli.py::test_a_target_another_mover_still_holds_is_promised_and_then_reported`

Old text:

```
        lossy=marker in path.stem or marker in title,
```

New text:

```
        lossy=marker in path.stem,
```

### `r669.G10_apply_trusts_the_plan_for_the_hold`

Skip the post gate re-read's hold, so a body composed from a tag that is gone is still acted on

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `G10_apply_trusts_the_plan_for_the_hold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_an_artist_tag_removed_while_the_gate_waits_holds_the_file`

Old text:

```
        built, why = _spec_for(path, template=template, cfg=cfg)
        if why is not None:
            _owed(item, why)
            continue
```

New text:

```
        built, why = _spec_for(path, template=template, cfg=cfg)
```

### `r669.G11_gate_shows_nothing`

Drop the gate context, which is the R-670 defect exactly

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `G11_gate_shows_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 3 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_gate_names_a_referenced_file_among_the_held`
  - `tests/test_naming_apply_cli.py::test_the_gate_screen_omits_the_not_listed_keys_under_the_bound`
  - `tests/test_naming_apply_cli.py::test_the_gate_shows_the_totals_and_every_item`

Old text:

```
    option = ctx.gate.require(spec, digest=plan["digest"], context=_shown(plan, root=root))
```

New text:

```
    option = ctx.gate.require(spec, digest=plan["digest"])
```

### `r669.G12_shown_count_is_every_item`

Show the item count as the rename count, so the screen overstates what will move

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `G12_shown_count_is_every_item`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_gate_screen_lists_no_more_than_the_bound_and_counts_the_rest`
  - `tests/test_naming_apply_cli.py::test_the_gate_shows_the_totals_and_every_item`

Old text:

```
        "renames": plan["totals"]["count"],
```

New text:

```
        "renames": len(items),
```

### `r669.G13_referenced_held_without_a_reason`

Carry an empty reason on a referenced item

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `G13_referenced_held_without_a_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_gate_names_a_referenced_file_among_the_held`

Old text:

```
REFERENCED_WHY = "the rekordbox collection references it"
```

New text:

```
REFERENCED_WHY = ""
```

### `r669.G17_held_file_never_referenced`

Mark every uncomposed file unnamed without asking the collection, the review's first finding

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `G17_held_file_never_referenced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_referenced_identifier_file_is_held_as_referenced_and_never_owed`

Old text:

```
    for path, why in uncomposed:
        if _is_referenced(path, referenced):
```

New text:

```
    for path, why in uncomposed:
        if False:
```

### `r669.G18_drifted_name_renamed_anyway`

Rename to whatever the tags render after the gate, the review's second finding

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `G18_drifted_name_renamed_anyway`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_tag_edited_while_the_gate_waits_is_not_renamed_to_a_name_nobody_saw`

Old text:

```
        if rendered.filename != item["to"]:
```

New text:

```
        if False:
```

### `r669.G19_no_step_for_unnamed`

Leave the unnamed step out of the report, so the remedy is to run it again

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `G19_no_step_for_unnamed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_report_over_a_held_identifier_says_to_tag_it`

Old text:

```
    if unnamed:
        steps.append(
```

New text:

```
    if False:
        steps.append(
```

### `r669.G1_identifier_is_no_letters`

Widen the identifier test from digits only to no letters, the first draft's rule the review sent back

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `G1_identifier_is_no_letters`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_letterless_stem_that_is_not_a_number_is_carried_as_it_is`

Old text:

```
    return stem.strip().isdigit()
```

New text:

```
    return not any(ch.isalpha() for ch in stem)
```

### `r669.G20_screen_uncapped`

List every planned rename on the gate screen with no bound

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `G20_screen_uncapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_gate_screen_lists_no_more_than_the_bound_and_counts_the_rest`

Old text:

```
        "planned": planned[:PLAN_SHOWN],
```

New text:

```
        "planned": planned,
```

### `r669.G21_artist_alone_when_no_title_tag`

An identifier with an artist and no title tag at all is renamed to its artist alone

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `G21_artist_alone_when_no_title_tag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_an_identifier_with_an_artist_and_no_title_tag_is_held_with_its_own_reason`

Old text:

```
    if not tagged_title:
        return None, (
            "its name is an identifier and it carries no title tag, so it is not "
            "renamed to its artist alone"
        )
```

New text:

```
    if not tagged_title:
        return artist, None
```

### `r669.G2_title_alone_when_no_artist`

An identifier with no artist tag is renamed to its title alone instead of held

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `G2_title_alone_when_no_artist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 5 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_an_artist_tag_removed_while_the_gate_waits_holds_the_file`
  - `tests/test_naming_apply_cli.py::test_an_identifier_with_no_artist_tag_is_held_and_named_in_the_plan`
  - `tests/test_naming_apply_cli.py::test_the_gate_shows_the_totals_and_every_item`
  - `tests/test_naming_apply_cli.py::test_the_report_over_a_held_identifier_says_to_tag_it`

Old text:

```
    if not artist:
        return None, (
            "its name is an identifier and it carries no artist tag, so it is not "
            "renamed to its title alone"
        )
```

New text:

```
    if not artist:
        return title, None
```

### `r669.G3_artist_alone_when_title_is_a_head`

An identifier whose title is only a head is renamed to its artist alone

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `G3_artist_alone_when_title_is_a_head`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_an_identifier_whose_title_tag_is_only_a_head_is_held`

Old text:

```
    if not title:
        return None, (
            "its name is an identifier and its title tag is only a head, empty once "
            "the head is removed, so no name can be composed for it"
        )
```

New text:

```
    if not title:
        return artist, None
```

### `r669.G4_order_swapped`

Compose Title - Artist, the other library grammar, instead of the declared Artist - Title

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `G4_order_swapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 10 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_camelot_key_tag_without_a_tempo_still_renders_no_head`
  - `tests/test_naming_apply_cli.py::test_a_composed_body_over_the_ceiling_is_fitted_not_left_as_a_number`
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_a_head_inside_the_title_tag_is_not_composed_into_the_body`
  - `tests/test_naming_apply_cli.py::test_a_slash_in_a_tag_takes_the_body_form_of_a_segment`
  - `tests/test_naming_apply_cli.py::test_a_tag_edited_while_the_gate_waits_is_not_renamed_to_a_name_nobody_saw`
  - `tests/test_naming_apply_cli.py::test_an_empty_artist_value_does_not_lead_the_body_with_a_comma`
  - `tests/test_naming_apply_cli.py::test_an_identifier_stem_is_composed_from_the_artist_and_title_tags`
  - `tests/test_naming_apply_cli.py::test_every_credited_artist_reaches_the_composed_body`
  - `tests/test_naming_apply_cli.py::test_the_gate_shows_the_totals_and_every_item`

Old text:

```
    return naming.compose_body(artist, title, sep=template.segment_sep), None
```

New text:

```
    return naming.compose_body(title, artist, sep=template.segment_sep), None
```

### `r669.G5_first_artist_only`

Read the artist through the single value reader, so a multi valued credit names the file for the first artist alone

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `G5_first_artist_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_an_empty_artist_value_does_not_lead_the_body_with_a_comma`
  - `tests/test_naming_apply_cli.py::test_every_credited_artist_reaches_the_composed_body`

Old text:

```
    values = tags.read_tag_values(path, "artist")
    if not values:
        return None
```

New text:

```
    values = [tags.read_tag(path, "artist") or ""]
    if not values:
        return None
```

### `r669.G6_title_head_kept_in_body`

Compose from the title tag verbatim, so a head the live system wrote into the tag lands inside the body

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `G6_title_head_kept_in_body`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_head_inside_the_title_tag_is_not_composed_into_the_body`
  - `tests/test_naming_apply_cli.py::test_an_identifier_whose_title_tag_is_only_a_head_is_held`

Old text:

```
    title = naming.strip_head(tagged_title, template=template).strip() if tagged_title else ""
```

New text:

```
    title = tagged_title.strip() if tagged_title else ""
```

### `r669.G7_unnamed_left_out_of_the_plan`

Drop the held identifier files from the plan's items, so the plan omits them silently

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `G7_unnamed_left_out_of_the_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 9 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_only_asked_about_the_files_being_renamed`
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_an_identifier_whose_title_tag_is_only_a_head_is_held`
  - `tests/test_naming_apply_cli.py::test_an_identifier_with_an_artist_and_no_title_tag_is_held_with_its_own_reason`
  - `tests/test_naming_apply_cli.py::test_an_identifier_with_no_artist_tag_is_held_and_named_in_the_plan`
  - `tests/test_naming_apply_cli.py::test_an_identifier_with_no_tags_at_all_is_held_with_its_own_reason`
  - `tests/test_naming_apply_cli.py::test_the_digest_covers_a_held_identifier_file`
  - `tests/test_naming_apply_cli.py::test_the_gate_shows_the_totals_and_every_item`
  - `tests/test_naming_apply_cli.py::test_the_report_over_a_held_identifier_says_to_tag_it`

Old text:

```
    items.extend(unnamed)
    return {
```

New text:

```
    return {
```

### `r669.G8_digest_ignores_unnamed`

Compute the digest over everything but the held identifier files, so a held file is not part of what was approved

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `G8_digest_ignores_unnamed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_digest_covers_a_held_identifier_file`

Old text:

```
        "digest": digest_of({"kind": "rename", "items": items}),
        "items": items,
        "totals": {
            "count": len(items) - held - len(collides) - len(unnamed),
```

New text:

```
        "digest": digest_of(
            {"kind": "rename", "items": [i for i in items if i["action"] != UNNAMED]}
        ),
        "items": items,
        "totals": {
            "count": len(items) - held - len(collides) - len(unnamed),
```

### `r669.G9_unnamed_not_owed_on_apply`

Owe only collisions on apply, so a sweep over a held identifier file answers ok

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `G9_unnamed_not_owed_on_apply`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 131 against a baseline of 131
- Kills: 3 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_only_asked_about_the_files_being_renamed`
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_the_report_over_a_held_identifier_says_to_tag_it`

Old text:

```
        if item["action"] in (COLLIDES, UNNAMED)
    ]
```

New text:

```
        if item["action"] == COLLIDES
    ]
```

### `r572.Z1_set_drop_album`

export set stops passing the album to match_track

- File: `src/cratekit/export/set_cli.py`
- Source: `r572.json`, row `Z1_set_drop_album`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_held_files_album_tag_is_handed_to_the_account_with_its_isrc`

Old text:

```
                    remote, said = _isrc_match(
                        account, identity, one, code, agree=True, album=album
                    )
```

New text:

```
                    remote, said = _isrc_match(
                        account, identity, one, code, agree=True
                    )
```

### `r837-b.B1_ref_only_from_the_provider`

set_cli.match_rows: a list document's row identifier is trusted whatever its origin, so a Spotify id is handed to the account

- File: `src/cratekit/export/set_cli.py`
- Source: `r837-b.json`, row `B1_ref_only_from_the_provider`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_another_sources_identifier_is_never_handed_to_the_account`

Old text:

```
            if one.ref and one.origin == match.TIDAL:
```

New text:

```
            if one.ref:
```

### `r837-b.B2_isrc_route`

set_cli.match_rows: a row's ISRC is never asked of the account, so it goes to the text search

- File: `src/cratekit/export/set_cli.py`
- Source: `r837-b.json`, row `B2_isrc_route`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_row_carrying_an_isrc_is_matched_through_the_accounts_own_match`

Old text:

```
            if one.isrc:
```

New text:

```
            if False:
```

### `r837-b.B3_accepted_in_review`

set_cli.match_rows: a candidate accepted in review is not used, so the row is left out

- File: `src/cratekit/export/set_cli.py`
- Source: `r837-b.json`, row `B3_accepted_in_review`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_candidate_accepted_in_review_is_used_and_not_searched_for_again`
  - `tests/test_export_set.py::test_a_persons_answer_in_review_wins_over_the_librarys_file`

Old text:

```
                if answered.state == candidates.ACCEPTED and answered.track is not None:
```

New text:

```
                if False:
```

### `r837-b.B4_sole_exact_listed`

set_cli.match_rows: the one exact search candidate is never listed, so every typed row is left out

- File: `src/cratekit/export/set_cli.py`
- Source: `r837-b.json`, row `B4_sole_exact_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 20 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_folder_named_as_the_year_by_hand_is_adopted_not_doubled`
  - `tests/test_export_set.py::test_a_full_first_page_with_one_exact_and_a_second_with_none_lists_it`
  - `tests/test_export_set.py::test_a_name_with_a_slash_finds_the_set_it_named_at_build`
  - `tests/test_export_set.py::test_a_playlist_already_in_its_folder_is_left`
  - `tests/test_export_set.py::test_a_playlist_retitled_by_a_person_is_filed_and_its_title_left`
  - `tests/test_export_set.py::test_a_playlist_the_folder_does_not_list_yet_is_not_renamed_or_blamed`
  - `tests/test_export_set.py::test_a_row_added_to_the_tracklist_later_is_added_to_the_same_playlist`
  - `tests/test_export_set.py::test_a_second_run_onto_the_same_set_plans_nothing`
  - `tests/test_export_set.py::test_a_set_put_in_its_folder_by_hand_writes_nothing_and_its_gate_says_so`
  - `tests/test_export_set.py::test_a_track_already_on_the_playlist_and_never_recorded_is_not_asked_for`
  - `tests/test_export_set.py::test_a_track_refused_before_is_said_as_refused_not_as_on_the_playlist`
  - `tests/test_export_set.py::test_a_track_taken_off_by_a_person_is_said_and_not_put_back`
  - `tests/test_export_set.py::test_a_year_folder_deleted_on_the_account_is_made_again`
  - `tests/test_export_set.py::test_an_exact_match_on_the_second_page_alone_is_listed`
  - `tests/test_export_set.py::test_approved_the_account_holds_a_private_playlist_of_four_in_order`
  - ... and 5 more, see the JSON sidecar

Old text:

```
            sole = candidates.sole_exact(answer)
```

New text:

```
            sole = None
```

### `r837-b.B5_unmatched_warning`

set_cli._unmatched_warnings: a set that left tracks out answers with no warning naming them (R-850)

- File: `src/cratekit/export/set_cli.py`
- Source: `r837-b.json`, row `B5_unmatched_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set.py::test_approved_the_account_holds_a_private_playlist_of_four_in_order`
  - `tests/test_export_set.py::test_five_rows_with_one_unmatched_plan_four_and_name_the_fifth`

Old text:

```
    if not planned.unmatched:
        return []
    return [
```

New text:

```
    if True:
        return []
    return [
```

### `r879-b.S10_unnamed_exact_said_to_resemble_nothing`

_not_chosen: count only identified exact matches before saying none resembles it

- File: `src/cratekit/export/set_cli.py`
- Source: `r879-b.json`, row `S10_unnamed_exact_said_to_resemble_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_an_exact_match_with_no_identifier_is_not_said_to_resemble_nothing`

Old text:

```
        if any(one.exact for one in answer.candidates):
```

New text:

```
        if exact:
```

### `r879-b.S4_several_codes_take_one`

file_isrc: take one of several distinct codes the held copies carry

- File: `src/cratekit/export/set_cli.py`
- Source: `r879-b.json`, row `S4_several_codes_take_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_held_copies_carrying_different_isrcs_ask_the_account_nothing`

Old text:

```
        if len(codes) == 1:
```

New text:

```
        if codes:
```

### `r879-b.S5_codes_from_every_version`

file_isrc: read the code of every held version, not only the matched files

- File: `src/cratekit/export/set_cli.py`
- Source: `r879-b.json`, row `S5_codes_from_every_version`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_another_versions_isrc_is_not_the_rows`

Old text:

```
            if str(held.path) in paths and held.isrc
```

New text:

```
            if held.isrc
```

### `r879-b.S6_absent_music_folder_unsaid`

file_isrc: drop the absent music folder check, so an unmounted volume reads as a library holding nothing

- File: `src/cratekit/export/set_cli.py`
- Source: `r879-b.json`, row `S6_absent_music_folder_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_an_absent_music_folder_is_said_and_never_read_as_holding_nothing`

Old text:

```
        if not self.music.is_dir():
```

New text:

```
        if False:
```

### `r879-b.S7_library_before_a_persons_answer`

match_rows: let the library's file pre-empt a person's answer in review

- File: `src/cratekit/export/set_cli.py`
- Source: `r879-b.json`, row `S7_library_before_a_persons_answer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_persons_answer_in_review_wins_over_the_librarys_file`

Old text:

```
            answered = candidates.settled(items, one)
```

New text:

```
            answered = None if not one.isrc and library.file_isrc(one)[0] else candidates.settled(items, one)
```

### `r879-b.S8_several_needs_three`

_not_chosen: say several only from three distinct exact matches

- File: `src/cratekit/export/set_cli.py`
- Source: `r879-b.json`, row `S8_several_needs_three`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_second_distinct_exact_match_on_the_next_page_leaves_it_out_as_several`
  - `tests/test_export_set.py::test_two_exact_candidates_are_not_chosen_between`

Old text:

```
    elif exact > 1:
```

New text:

```
    elif exact > 2:
```

### `r879-b.S9_ambiguous_full_said_as_bound`

_not_chosen: say two readings only with an exact match, so a full first page of an ambiguous row is said as the bound

- File: `src/cratekit/export/set_cli.py`
- Source: `r879-b.json`, row `S9_ambiguous_full_said_as_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_title_read_two_ways_on_a_full_page_says_so_and_not_the_bound`

Old text:

```
    if answer.ambiguous and (exact or answer.full):
```

New text:

```
    if answer.ambiguous and exact:
```

### `u142.S8_gate_stale_said_without_a_write`

export archive gate: say a stale record is replaced even when nothing is written

- File: `src/cratekit/export/set_cli.py`
- Source: `u142.json`, row `S8_gate_stale_said_without_a_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_set_put_in_its_folder_by_hand_writes_nothing_and_its_gate_says_so`

Old text:

```
    if planned.stale_folder and planned.writes:
```

New text:

```
    if planned.stale_folder:
```

### `r879-a.C10_offset_counts_pages_not_rows`

search_pages: ask offset 1, 2 for the next pages instead of 50, 100

- File: `src/cratekit/intake/candidates.py`
- Source: `r879-a.json`, row `C10_offset_counts_pages_not_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 4 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_full_first_page_with_one_exact_and_a_second_with_none_lists_it`
  - `tests/test_export_set.py::test_an_empty_page_after_full_ones_ends_the_listing_and_a_full_last_page_never_lists`
  - `tests/test_export_set.py::test_no_exact_match_on_any_page_leaves_it_out_as_none`
  - `tests/test_export_set.py::test_the_page_bound_reached_leaves_it_out_and_says_so`

Old text:

```
        pages.append(tuple(search(len(pages) * TRACK_SEARCH_PAGE)))
```

New text:

```
        pages.append(tuple(search(len(pages))))
```

### `r879-a.C2_walk_ignores_short_page`

search_pages: drop the stop on a short page, so the walk asks every page to the bound

- File: `src/cratekit/intake/candidates.py`
- Source: `r879-a.json`, row `C2_walk_ignores_short_page`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 6 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_full_first_page_with_one_exact_and_a_second_with_none_lists_it`
  - `tests/test_export_set.py::test_a_held_file_whose_isrc_the_account_cannot_name_is_searched_and_said`
  - `tests/test_export_set.py::test_a_held_file_with_no_isrc_is_searched_and_says_so`
  - `tests/test_export_set.py::test_a_short_first_page_is_read_once`
  - `tests/test_export_set.py::test_an_empty_page_after_full_ones_ends_the_listing_and_a_full_last_page_never_lists`
  - `tests/test_export_set.py::test_no_exact_match_on_any_page_leaves_it_out_as_none`

Old text:

```
        if not answer.full or _settled_early(answer) or len(pages) >= bound:
```

New text:

```
        if _settled_early(answer) or len(pages) >= bound:
```

### `r879-a.C3_settled_early_without_ambiguity`

_settled_early: drop the ambiguous title, so a title read two ways reads on past a full page

- File: `src/cratekit/intake/candidates.py`
- Source: `r879-a.json`, row `C3_settled_early_without_ambiguity`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_title_read_two_ways_on_a_full_page_says_so_and_not_the_bound`
  - `tests/test_export_set.py::test_a_title_that_reads_two_ways_reads_no_second_page`

Old text:

```
        answer.ambiguous
        or bool(answer.unreadable)
```

New text:

```
        bool(answer.unreadable)
```

### `r879-a.C4_settled_early_without_unreadable`

_settled_early: drop the unreadable row, so a page with one reads on

- File: `src/cratekit/intake/candidates.py`
- Source: `r879-a.json`, row `C4_settled_early_without_unreadable`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_an_unreadable_row_on_a_full_page_reads_no_second_page`

Old text:

```
        or bool(answer.unreadable)

```

New text:

```
        or False

```

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
- Collected: 22663 against a baseline of 22663
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
- Collected: 22663 against a baseline of 22663
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

