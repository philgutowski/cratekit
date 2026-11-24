# Mutation table: u334-replay-before-10

Measured by `scripts/mutate.py` on 2026-11-24 04:16 UTC, branch `HEAD` at `89c9e120`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23216 collected. pytest invocations for this batch: 309.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 04:16 UTC for commit `89c9e120f5d4`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 53, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23216 against 23216. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r500-a.G1_no_refusal` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 13 | killed |
| `r500-a.G2_existence_half_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r500-a.G3_unmapped_half_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r500-a.G4_lexists` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r500-a.G5_recorded_key_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 2 | killed |
| `r500-b.G9_plural_always` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r500-c.G11_prefix_cap_halved` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r500-c.G12_remedy_run_doctor` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r500-c.G15_other_host_refuses` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r669.E1_key_from_the_head_only` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 1 | killed |
| `r669.E2_body_from_the_title_tag` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 27 | killed |
| `r669.E3_lossy_from_the_stem_only` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 3 | killed |
| `r669.G10_apply_trusts_the_plan_for_the_hold` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 1 | killed |
| `r669.G11_gate_shows_nothing` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 3 | killed |
| `r669.G12_shown_count_is_every_item` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 2 | killed |
| `r669.G13_referenced_held_without_a_reason` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 1 | killed |
| `r669.G17_held_file_never_referenced` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 1 | killed |
| `r669.G18_drifted_name_renamed_anyway` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 1 | killed |
| `r669.G19_no_step_for_unnamed` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 1 | killed |
| `r669.G1_identifier_is_no_letters` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 1 | killed |
| `r669.G20_screen_uncapped` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 1 | killed |
| `r669.G21_artist_alone_when_no_title_tag` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 1 | killed |
| `r669.G2_title_alone_when_no_artist` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 5 | killed |
| `r669.G3_artist_alone_when_title_is_a_head` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 1 | killed |
| `r669.G4_order_swapped` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 10 | killed |
| `r669.G5_first_artist_only` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 2 | killed |
| `r669.G6_title_head_kept_in_body` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 2 | killed |
| `r669.G7_unnamed_left_out_of_the_plan` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 9 | killed |
| `r669.G8_digest_ignores_unnamed` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 1 | killed |
| `r669.G9_unnamed_not_owed_on_apply` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 3 | killed |
| `r675.E2_key_not_casefolded` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 3 | killed |
| `r675.E4_tombstones_dropped_from_the_read` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 4 | killed |
| `r675.G11_prefixes_dropped` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 3 | killed |
| `r675.G12_could_name_uncapped` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 1 | killed |
| `r675.G13_as_recorded_key_dropped` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 2 | killed |
| `r675.G14_remapped_key_dropped` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 1 | killed |
| `r675.G15_first_location_dropped` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 4 | killed |
| `r675.G16_locations_uncapped` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 1 | killed |
| `r675.G17_prefixes_uncapped` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 1 | killed |
| `r675.G18_held_candidates_asked_about` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 1 | killed |
| `r675.G19_second_step_dropped` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 1 | killed |
| `r675.G1_every_dark_row_refuses` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 6 | killed |
| `r675.G2_row_leaf_not_keyed` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 14 | killed |
| `r675.G3_candidate_leaf_not_keyed` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 14 | killed |
| `r675.G4_could_name_empty` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 7 | killed |
| `r675.G5_leaf_compared_as_whole_path` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 15 | killed |
| `r675.G6_plan_asks_with_no_candidates` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 1 | killed |
| `r675.G7_apply_asks_with_no_candidates` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 1 | killed |
| `r675.G8_count_reworded` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 3 | killed |
| `u212.N1_second_copy_compare` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 6 | 1 | killed |
| `u212.N3_taken_plain` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 6 | 2 | killed |
| `u212.N4_plan_isrc` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 6 | 1 | killed |
| `u212.N5_claim_plain` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 59 | 1 | killed |
| `u212.N6_cause_step` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 6 | 1 | killed |
| `u327.A24_spec_reads_title_head_first` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 213 | 2 | killed |
| `u39-author-full.R3_bpm_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 30 | killed |
| `u39-author-full.R4_head_key_overrules_tag` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `u39-author-full.R5_junk_tag_admitted` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `u39-author-full.R6_lossy_flag_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 5 | killed |
| `u39-naming-independent.R5_bpm_wrong_type` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 72 | killed |
| `u41-author-full.R6_head_key_overrules_tag` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `u41-author-full.T1_title_tag_fed_the_filename_body` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 4 | killed |
| `u41-author-full.T2_title_field_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 4 | killed |
| `u41-naming-independent.B7_lossy_filename_operand_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `u41-naming-independent.B8_lossy_title_operand_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 3 | killed |
| `u41-naming-independent.C1_plan_no_op_filter_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 14 | killed |
| `u67-round-2.C1_action_filter_and_recheck` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 19 | killed |
| `u67.M2_nfc` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `u67.M3_prefix_resolution` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `u67.M6_remote_host_skip` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `u67.M7_absolute_spelling` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `u67.M8_resolved_spelling` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `u67.R1_refusal_to_empty` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 3 | killed |
| `u67.R2_generic_to_empty` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `u67.R3_remedy_passthrough` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 2 | killed |
| `u302.W1_intake_replace_bumps_count` | `src/cratekit/write/rbxml.py` | user | 2 file(s) | 86 | 1 | killed |
| `u302.W2_self_closed_node_deepens` | `src/cratekit/write/rbxml.py` | user | 3 file(s) | 164 | 15 | killed |
| `u302.W3_close_tag_not_counted` | `src/cratekit/write/rbxml.py` | user | 3 file(s) | 164 | 58 | killed |
| `u302.W4_open_tag_never_self_closing` | `src/cratekit/write/rbxml.py` | user | 3 file(s) | 164 | 17 | killed |
| `u76-a.D3_tree_level_lookup` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 1 | killed |
| `u76-a.D4_folder_level_lookup` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 2 | killed |
| `u76-a.D5_playlist_level_lookup` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 3 | killed |
| `u76-a.M1_merge_not_append` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 16 | killed |
| `u76-a.W1_copy_on_write` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 2 | killed |
| `u76-a.W2_commit_on_success` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 2 | killed |
| `u76-a.X1_dedupe_against_held` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 6 | killed |
| `u76-b.C1_count_bump` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 3 | killed |
| `u76-b.L1_folder_own_line` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 1 | killed |
| `u76-b.L2_anchor_own_line` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 1 | killed |
| `u76-b.L3_folder_close_own_line` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 1 | killed |
| `u76-b.L4_playlist_close_own_line` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 1 | killed |
| `u76-b.O1_anchor_order` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 4 | killed |
| `u76-b.O2_anchor_none` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 4 | killed |
| `u76-b.S1_self_closed_folder` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 1 | killed |
| `u76-b.X2_entries_count` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 2 | killed |
| `u76-b.X3_self_closed_playlist` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 3 | killed |
| `u76-b.X4_track_indent` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 1 | killed |
| `u76-zeros.X5_entries_absent` | `src/cratekit/write/rbxml.py` | maintainer | 4 file(s) | 224 | 3 | killed |
| `u76-a.D1_duplicate_sibling` | `src/cratekit/write/rbxml_insert.py` | user | 4 file(s) | 224 | 2 | killed |
| `u76-a.D2_type_collision` | `src/cratekit/write/rbxml_insert.py` | user | 4 file(s) | 224 | 1 | killed |
| `u76-a.F1_nfc_fold` | `src/cratekit/write/rbxml_insert.py` | user | 4 file(s) | 224 | 1 | killed |
| `u76-a.F2_case_fold` | `src/cratekit/write/rbxml_insert.py` | user | 4 file(s) | 224 | 1 | killed |
| `u76-a.P2_dedupe_ids` | `src/cratekit/write/rbxml_insert.py` | user | 4 file(s) | 224 | 2 | killed |
| `u76-zeros.P1_join_pairs` | `src/cratekit/write/rbxml_insert.py` | user | 4 file(s) | 224 | 1 | killed |
| `r312.E2_vocal_gap_filter_off` | `src/cratekit/write/rebuild.py` | user | 2 file(s) | 309 | 1 | killed |
| `r316.M10_derivation_restates_no_gap` | `src/cratekit/write/rebuild.py` | user | 2 file(s) | 309 | 9 | killed |
| `r316.M9_not_derived_ignores_threshold` | `src/cratekit/write/rebuild.py` | user | 2 file(s) | 309 | 14 | killed |
| `u119.R1_vox_unknown_by_id` | `src/cratekit/write/rebuild.py` | user | 2 file(s) | 158 | 40 | killed |
| `u219.A1_approved_equality` | `src/cratekit/write/rebuild.py` | user | 11 file(s) | 732 | 2 | killed |
| `u219.A2_approved_checked` | `src/cratekit/write/rebuild.py` | user | 11 file(s) | 732 | 2 | killed |
| `u219.A3_approved_passed_down` | `src/cratekit/write/rebuild.py` | user | 11 file(s) | 732 | 5 | killed |
| `u219.A4_additions_rows` | `src/cratekit/write/rebuild.py` | user | 11 file(s) | 732 | 21 | killed |
| `u219.D1_derivable_guard` | `src/cratekit/write/rebuild.py` | user | 11 file(s) | 732 | 3 | killed |
| `u219.D2_derivation_asks` | `src/cratekit/write/rebuild.py` | user | 11 file(s) | 732 | 2 | killed |
| `u219.D4_derivable_answer` | `src/cratekit/write/rebuild.py` | user | 11 file(s) | 732 | 19 | killed |
| `u219.F1_favourites_held` | `src/cratekit/write/rebuild.py` | user | 11 file(s) | 732 | 3 | killed |
| `u219.K1_accept_routing_refused` | `src/cratekit/write/rebuild.py` | user | 11 file(s) | 732 | 1 | killed |
| `u219.M1_accept_fingerprint` | `src/cratekit/write/rebuild.py` | user | 11 file(s) | 732 | 2 | killed |
| `u246.R1_rebuild_set_per_placement` | `src/cratekit/write/rebuild.py` | user | 5 file(s) | 216 | 2 | killed |
| `u246.R2_rebuild_tuple_scan` | `src/cratekit/write/rebuild.py` | user | 5 file(s) | 216 | 1 | killed |
| `u246.R3_rebuild_set_of_placements` | `src/cratekit/write/rebuild.py` | user | 5 file(s) | 380 | 5 | killed |
| `u246.R4_rebuild_membership_inverted` | `src/cratekit/write/rebuild.py` | user | 5 file(s) | 380 | 7 | killed |
| `u246.R5_rebuild_set_empty` | `src/cratekit/write/rebuild.py` | user | 5 file(s) | 380 | 2 | killed |
| `u250.M2_genre_dropped` | `src/cratekit/write/rebuild.py` | user | 3 file(s) | 215 | 39 | killed |
| `u250.M3_energy_unconverted` | `src/cratekit/write/rebuild.py` | user | 3 file(s) | 215 | 32 | killed |
| `u250.M4_vox_reads_energy` | `src/cratekit/write/rebuild.py` | user | 3 file(s) | 215 | 27 | killed |
| `u302.W12_resort_writes_favourites_its_gate_never_showed` | `src/cratekit/write/rebuild.py` | user | 4 file(s) | 183 | 3 | killed |
| `u302.W13_unconverged_tree_cleared` | `src/cratekit/write/rebuild.py` | user | 3 file(s) | 182 | 7 | killed |
| `u340.R05_derive_one_bucket` | `src/cratekit/write/rebuild.py` | user | 3 file(s) | 173 | 11 | killed |
| `u340.R06_truth_unread` | `src/cratekit/write/rebuild.py` | user | 3 file(s) | 173 | 4 | killed |
| `u219-composites.G6_answer_pinned` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 221 | 1 | killed |
| `u219.G1_resort_abort` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 297 | 1 | killed |
| `u219.G2_nothing_to_add` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 297 | 1 | killed |
| `u219.G3_adds_frozen` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 297 | 21 | killed |
| `u219.G5_resume_run` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 297 | 1 | killed |
| `u219.M3_due_again_said` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 297 | 1 | killed |
| `u219.R1_routed_trees` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 297 | 12 | killed |
| `u219.R2_inbox_routed_only` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 297 | 1 | killed |
| `u219.R3_left_alone_named` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 297 | 1 | killed |
| `r239-b.S2_unplaced_key_off` | `src/cratekit/write/routing_export.py` | user | 7 file(s) | 724 | 2 | killed |
| `u155.W2_destination` | `src/cratekit/write/routing_pass.py` | user | 13 file(s) | 817 | 63 | killed |
| `a32.J3_bookkeeping_counted_as_moved` | `src/cratekit/write/row_defaults.py` | user | 2 file(s) | 113 | 6 | killed |
| `r923.N11_digest_drops_items` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 2 | killed |
| `r923.N13_judge_compares_raw` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 3 | killed |
| `r923.N2_plan_lists_tombstones` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 13 | killed |
| `r923.N3_plan_sees_no_null` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 8 | killed |
| `r923.N4_stale_fill_accepted` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 1 | killed |
| `r923.N5_stale_tombstone_accepted` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 1 | killed |
| `r923.N6_judge_blind_to_wrong` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 1 | killed |
| `r923.N7_judge_blind_to_moved` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 2 | killed |
| `r923.N8_read_back_never_refuses` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 2 | killed |
| `u115.F11_stale_file_id_not_checked` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 1 | killed |
| `u115.F12_read_back_ignores_file_id` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 1 | killed |
| `u115.F13_planned_renumber_read_as_moved` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 2 | killed |
| `u115.F14_renumber_never_written` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 1 | killed |
| `u115.F17_bound_is_zero` | `src/cratekit/write/row_defaults.py` | maintainer | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u115.F21_other_volume_compared` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 1 | killed |
| `u115.F22_off_apfs_decides` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 1 | killed |
| `u115.F23_loose_digits` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 3 | killed |
| `u115.F5_bound_boundary` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 2 | killed |
| `u115.F6_every_id_above` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 12 | killed |
| `u115.F7_zero_is_not_zero` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 4 | killed |
| `u115.F8_matching_inode_renumbered` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u115.F9_unreadable_file_dropped_silently` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 5 | killed |
| `u302.W10_empty_watch_accepted` | `src/cratekit/write/row_defaults.py` | user | 2 file(s) | 113 | 1 | killed |
| `r923.N14_verb_writes_on_abort` | `src/cratekit/write/row_defaults_cli.py` | user | 1 file(s) | 53 | 7 | killed |
| `r923.N15_verb_writes_empty_plan` | `src/cratekit/write/row_defaults_cli.py` | user | 1 file(s) | 53 | 2 | killed |
| `r923.N16_ack_not_read` | `src/cratekit/write/row_defaults_cli.py` | user | 1 file(s) | 53 | 1 | killed |
| `r923.N17_write_handle_not_closed` | `src/cratekit/write/row_defaults_cli.py` | maintainer | 1 file(s) | 53 | 1 | killed |
| `u115.F18_undecidable_unsaid` | `src/cratekit/write/row_defaults_cli.py` | user | 1 file(s) | 53 | 1 | killed |
| `u115.F19_unrenumbered_unsaid` | `src/cratekit/write/row_defaults_cli.py` | user | 1 file(s) | 53 | 2 | killed |
| `a32.A2_stale_deleted` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 60 | 1 | killed |
| `a32.A3_stale_value` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 60 | 1 | killed |
| `a32.A5_policy_widened` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 60 | 1 | killed |
| `a32.D1_digest_drops_replaced` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 60 | 2 | killed |
| `a32.D2_digest_unordered` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 60 | 1 | killed |
| `a32.J1_wrong_unjudged` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 60 | 1 | killed |
| `a32.J2_planned_across_rows` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 60 | 1 | killed |
| `a32.J4_moved_not_refused` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 60 | 2 | killed |
| `a32.P1_tombstone_plans` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 60 | 1 | killed |
| `a32.P2_unknown_row` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 60 | 4 | killed |
| `a32.P3_unheld_value` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 60 | 3 | killed |
| `a32.P4_count_tombstones` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 60 | 5 | killed |
| `a32.P6_writes_always` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 60 | 6 | killed |
| `a32.P7_minority_boundary` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 60 | 1 | killed |
| `a32.P8_null_fellows` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 60 | 1 | killed |
| `a32.V1_any_column` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 60 | 4 | killed |
| `a32.V2_link_not_converted` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 60 | 4 | killed |
| `a32.C1_ack_after_gate` | `src/cratekit/write/row_link_cli.py` | user | 1 file(s) | 60 | 1 | killed |
| `a32.C2_abort_writes` | `src/cratekit/write/row_link_cli.py` | user | 1 file(s) | 60 | 1 | killed |
| `a32.C3_nothing_to_write_applies` | `src/cratekit/write/row_link_cli.py` | user | 1 file(s) | 60 | 1 | killed |
| `a32.C4_read_back_unasserted` | `src/cratekit/write/row_link_cli.py` | user | 1 file(s) | 60 | 1 | killed |
| `r375-b.M1_capture_never_attached` | `src/cratekit/write/trees.py` | user | 1 file(s) | 26 | 3 | killed |
| `u302.W9c_configuration_rules_dropped` | `src/cratekit/write/trees.py` | user | 4 file(s) | 438 | 2 | killed |
| `u40-author-full.F4_tombstone_indexed` | `src/cratekit/write/trees.py` | user | 7 file(s) | 757 | 3 | killed |
| `u77-b.B6_trial_id` | `src/cratekit/write/trees.py` | user | 6 file(s) | 254 | 2 | killed |
| `u77-b.B7_check_empty_catalog` | `src/cratekit/write/trees.py` | user | 6 file(s) | 254 | 3 | killed |
| `u77-b.B8_label_write_order` | `src/cratekit/write/trees.py` | user | 6 file(s) | 254 | 2 | killed |
| `u258.M1_key_on_length` | `tests/_parse_memo.py` | maintainer | 1 file(s) | 10 | 1 | killed |
| `u258.M2_scope_shares_nothing` | `tests/_parse_memo.py` | maintainer | 1 file(s) | 10 | 6 | killed |
| `u258.M3_scope_never_ends` | `tests/_parse_memo.py` | maintainer | 1 file(s) | 10 | 5 | killed |
| `u258.M4_inner_scope_ends_the_outer` | `tests/_parse_memo.py` | maintainer | 1 file(s) | 10 | 2 | killed |
| `u258.M5_decorator_opens_no_scope` | `tests/_parse_memo.py` | maintainer | 1 file(s) | 10 | 2 | killed |
| `u258.M6_decorator_returns_the_test` | `tests/_parse_memo.py` | maintainer | 1 file(s) | 10 | 1 | killed |
| `u125.P2_drop_slug` | `tests/_pinned_reserved_populations.py` | maintainer | 2 file(s) | 2 | 2 | killed |
| `u296.M19_pin_in_the_wrong_file` | `tests/_pinned_reserved_populations.py` | maintainer | 2 file(s) | 235 | 2 | killed |
| `u296.M20_unknown_pin_table` | `tests/_pinned_reserved_populations.py` | maintainer | 2 file(s) | 235 | 1 | killed |
| `u12-independent-round-6.S2_package_never_resolved` | `tests/_source_guards.py` | maintainer | 3 file(s) | 1443 | 10 | killed |
| `u12-independent-round-6.S3_only_the_module_itself_counts` | `tests/_source_guards.py` | maintainer | 3 file(s) | 1443 | 6 | killed |
| `u258.M7_a_question_writes_the_shared_tree` | `tests/_source_guards.py` | maintainer | 2 file(s) | 239 | 1 | killed |
| `u258.M8_tree_form_answers_nothing` | `tests/_source_guards.py` | maintainer | 2 file(s) | 239 | 2 | killed |
| `u326.W1_children_reads_lists` | `tests/_source_guards.py` | maintainer | 4 file(s) | 1616 | 153 | killed |
| `u326.W2_cache_by_identity` | `tests/_source_guards.py` | maintainer | 4 file(s) | 1616 | 146 | killed |
| `u329.G1_guard_reads_the_old_accessor_name` | `tests/_source_guards.py` | maintainer | 4 file(s) | 277 | 2 | killed |
| `u329.G2_guard_reads_the_old_home` | `tests/_source_guards.py` | maintainer | 4 file(s) | 277 | 2 | killed |
| `u329.G3_guard_skips_the_relative_import` | `tests/_source_guards.py` | maintainer | 4 file(s) | 277 | 1 | killed |
| `u232.A1_platform_stub` | `tests/conftest.py` | maintainer | 4 file(s) | 90 | 4 | killed |
| `u232.A8_opt_in` | `tests/conftest.py` | maintainer | 2 file(s) | 55 | 4 | killed |
| `u326.R8_general_catalogue_refused` | `tests/conftest.py` | maintainer | 1 file(s) | 141 | 1 | killed |
| `u296.M21_placed_modules_unread` | `tests/test_layering.py` | maintainer | 1 file(s) | 50 | 10 | killed |
| `u253.L10_relative_is_the_name` | `tests/test_locations.py` | maintainer | 1 file(s) | 146 | 15 | killed |
| `u253.L11_guard_narrowed_root` | `tests/test_locations.py` | maintainer | 1 file(s) | 146 | 1 | killed |
| `u253.L12_guard_drops_the_sweep` | `tests/test_locations.py` | maintainer | 1 file(s) | 146 | 1 | killed |
| `u253.L2_relative_before_exclusions` | `tests/test_locations.py` | maintainer | 1 file(s) | 146 | 1 | killed |
| `u253.L3_no_decoder_skip` | `tests/test_locations.py` | maintainer | 1 file(s) | 146 | 3 | killed |
| `u253.L4_no_vendor_skip` | `tests/test_locations.py` | maintainer | 1 file(s) | 146 | 3 | killed |
| `u253.L5_vendor_skip_by_part` | `tests/test_locations.py` | maintainer | 1 file(s) | 146 | 1 | killed |
| `u253.L6_permit_by_name_only` | `tests/test_locations.py` | maintainer | 1 file(s) | 146 | 3 | killed |
| `u253.L7_bare_calls_only` | `tests/test_locations.py` | maintainer | 1 file(s) | 146 | 5 | killed |
| `u253.L8_three_names` | `tests/test_locations.py` | maintainer | 1 file(s) | 146 | 3 | killed |
| `u253.L9_one_line_per_file` | `tests/test_locations.py` | maintainer | 1 file(s) | 146 | 1 | killed |
| `r658-b.S10_outbound_zone` | `tests/test_outbound_workers.py` | user | 1 file(s) | 123 | 1 | killed |
| `u28-skills-independent.P1_annassign_branch` | `tests/test_pending_units.py` | maintainer | 1 file(s) | 102 | 1 | killed |
| `u28-skills-independent.P2_empty_call_args` | `tests/test_pending_units.py` | maintainer | 1 file(s) | 102 | 1 | killed |
| `u25-author-light.G4_sizing_countdown` | `tests/test_pool_sizing.py` | maintainer | 1 file(s) | 269 | 7 | killed |
| `u232.A10_real_walk_restored` | `tests/test_process_scan.py` | maintainer | 1 file(s) | 46 | 8 | killed |
| `u256.T4_key_carries_the_variant` | `tests/test_rb_writer_db.py` | maintainer | 2 file(s) | 57 | 2 | killed |
| `u256.T8_private_copy_per_call` | `tests/test_rb_writer_db.py` | maintainer | 2 file(s) | 57 | 6 | killed |
| `r658-b.S8_reserved_short_walk` | `tests/test_reserved_causes.py` | user | 1 file(s) | 229 | 1 | killed |
| `r658-b.S9_reserved_moved_module` | `tests/test_reserved_causes.py` | user | 1 file(s) | 229 | 1 | killed |
| `u258.M11_kebab_reads_a_second_package` | `tests/test_reserved_causes.py` | maintainer | 2 file(s) | 239 | 1 | killed |
| `u258.M9_population_keeps_the_owners` | `tests/test_reserved_causes.py` | maintainer | 2 file(s) | 239 | 2 | killed |
| `u312.C1_citation_prefilter` | `tests/test_reserved_causes.py` | maintainer | 1 file(s) | 229 | 2 | killed |
| `u199.M1_table_not_applied` | `tests/test_restart_and_residual_files.py` | maintainer | 1 file(s) | 48 | 1 | killed |
| `u199.M2_entry_widened_to_paragraph` | `tests/test_restart_and_residual_files.py` | maintainer | 1 file(s) | 48 | 3 | killed |
| `u199.M3_only_the_opening_compared` | `tests/test_restart_and_residual_files.py` | maintainer | 1 file(s) | 48 | 3 | killed |
| `u199.M4_exactly_once_relaxed` | `tests/test_restart_and_residual_files.py` | maintainer | 1 file(s) | 48 | 1 | killed |
| `u199.M5_old_text_unchecked` | `tests/test_restart_and_residual_files.py` | maintainer | 1 file(s) | 48 | 2 | killed |
| `u199.M6_new_text_unchecked` | `tests/test_restart_and_residual_files.py` | maintainer | 1 file(s) | 48 | 2 | killed |
| `u199.M7_new_text_in_any_fragment` | `tests/test_restart_and_residual_files.py` | maintainer | 1 file(s) | 48 | 1 | killed |
| `r658-b.S6_restore_full_disk` | `tests/test_restore.py` | user | 1 file(s) | 159 | 1 | killed |
| `u28-skills-independent.L9_command_comment_split` | `tests/test_skills_lint.py` | maintainer | 1 file(s) | 23216 | 0 (promoted) | zero |

## Zero rows and what they owe

- `u115.F17_bound_is_zero` (maintainer facing): maintainer facing, composite not required
- `u115.F8_matching_inode_renumbered` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u28-skills-independent.L9_command_comment_split` (maintainer facing): maintainer facing, composite not required

## Row definitions

### `r500-a.G1_no_refusal`

Drop the refusal over dark rows in _referenced, so an unmapped row contributes only a key nothing matches and the file it names is renamed (R-500 as filed)

- File: `src/cratekit/write/naming_cli.py`
- Source: `r500-a.json`, row `G1_no_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 13 (killed)
- Killed:
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
  - `tests/test_naming_apply_cli.py::test_two_dark_rows_under_one_candidate_name_each_name_it`

Old text:

```
    if dark:
        raise _unmapped_refusal(dark)

```

New text:

```
(empty)
```

### `r500-a.G2_existence_half_dropped`

Drop the existence half of dark, so every unmapped row refuses, including a row whose recorded file is on this machine (the first cut the review rejected)

- File: `src/cratekit/write/naming_cli.py`
- Source: `r500-a.json`, row `G2_existence_half_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_whose_file_exists_elsewhere_does_not_hold_a_namesake_in_the_library`

Old text:

```
        elif resolved.resolution is locations.Resolution.UNMAPPED and not os.path.exists(decoded):
```

New text:

```
        elif resolved.resolution is locations.Resolution.UNMAPPED:
```

### `r500-a.G3_unmapped_half_dropped`

Drop the UNMAPPED half of dark, so any unresolved row whose text is not a file here refuses, a streaming pseudo-location included

- File: `src/cratekit/write/naming_cli.py`
- Source: `r500-a.json`, row `G3_unmapped_half_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_that_can_name_no_candidate_neither_blocks_nor_protects[a-device-relative-row]`

Old text:

```
        elif resolved.resolution is locations.Resolution.UNMAPPED and not os.path.exists(decoded):
```

New text:

```
        elif not os.path.exists(decoded):
```

### `r500-a.G4_lexists`

Ask whether the recorded NAME exists rather than whether it reaches a file, so a link to nothing reads as a row that answered

- File: `src/cratekit/write/naming_cli.py`
- Source: `r500-a.json`, row `G4_lexists`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_recording_a_link_to_nothing_is_dark`

Old text:

```
not os.path.exists(decoded):
```

New text:

```
not os.path.lexists(decoded):
```

### `r500-a.G5_recorded_key_dropped`

Drop the as recorded key. The existence rule rests on it: an unmapped row whose file exists is excused BECAUSE this key protects the file

- File: `src/cratekit/write/naming_cli.py`
- Source: `r500-a.json`, row `G5_recorded_key_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_file_is_protected_through_a_linked_root[link-recorded]`
  - `tests/test_naming_apply_cli.py::test_a_root_outside_the_library_is_still_checked`

Old text:

```
        keys.add(_key(decoded))

```

New text:

```
(empty)
```

### `r500-b.G9_plural_always`

Move the singular wording's bound, so one row reads as rows

- File: `src/cratekit/write/naming_cli.py`
- Source: `r500-b.json`, row `G9_plural_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_under_an_unmapped_volume_refuses_and_renames_nothing`

Old text:

```
"collection row records" if count == 1 else
```

New text:

```
"collection row records" if count == 0 else
```

### `r500-c.G11_prefix_cap_halved`

Halve the cap on the detail's prefix list, a coefficient

- File: `src/cratekit/write/naming_cli.py`
- Source: `r500-c.json`, row `G11_prefix_cap_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_refusal_counts_every_row_and_lists_no_more_than_twenty`

Old text:

```
            "unmapped_prefixes": prefixes[:20],
```

New text:

```
            "unmapped_prefixes": prefixes[:10],
```

### `r500-c.G12_remedy_run_doctor`

Carry the deletion pass's run-doctor token, which sends a caller to a report no check of which reads the prefix map

- File: `src/cratekit/write/naming_cli.py`
- Source: `r500-c.json`, row `G12_remedy_run_doctor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_under_an_unmapped_volume_refuses_and_renames_nothing`

Old text:

```
        remedy=Remedy.FIX_CONFIG_VALUES,
```

New text:

```
        remedy=Remedy.RUN_DOCTOR,
```

### `r500-c.G15_other_host_refuses`

Existing U67 guard, sampled: a row naming another host raises out of the verb rather than being passed over

- File: `src/cratekit/write/naming_cli.py`
- Source: `r500-c.json`, row `G15_other_host_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_that_can_name_no_candidate_neither_blocks_nor_protects[a-row-naming-another-host]`

Old text:

```
        except locations.LocationDecodeError:
            continue
```

New text:

```
        except locations.LocationDecodeError:
            raise
```

### `r669.E1_key_from_the_head_only`

Ignore the initialkey tag and take the key from the head alone (U39)

- File: `src/cratekit/write/naming_cli.py`
- Source: `r669.json`, row `E1_key_from_the_head_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_naming_apply_cli.py`
- Collected: 121 against a baseline of 121
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[the-tag-key-wins-over-a-stale-head]`

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
- Collected: 121 against a baseline of 121
- Kills: 27 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_composed_body_over_the_ceiling_is_fitted_not_left_as_a_number`
  - `tests/test_naming_apply_cli.py::test_a_file_analyze_run_measured_is_named_with_no_head_and_a_head_on_file_is_kept`
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_a_name_over_the_byte_ceiling_is_truncated_not_rebuilt`
  - `tests/test_naming_apply_cli.py::test_a_referenced_file_does_not_hold_a_name_it_will_never_take`
  - `tests/test_naming_apply_cli.py::test_a_rename_never_replaces_the_body_with_the_title_tag`
  - `tests/test_naming_apply_cli.py::test_a_stem_carrying_text_is_not_recomposed_from_its_tags`
  - `tests/test_naming_apply_cli.py::test_a_tag_edited_while_the_gate_waits_is_not_renamed_to_a_name_nobody_saw`
  - `tests/test_naming_apply_cli.py::test_a_target_a_collider_holds_is_held_back_too`
  - `tests/test_naming_apply_cli.py::test_a_target_another_mover_still_holds_is_promised_and_then_reported`
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[a-deduping-rename-converges-on-one-pass]`
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[the-title-tag-is-not-given-the-filename-body]`
  - `tests/test_naming_apply_cli.py::test_an_artist_tag_removed_while_the_gate_waits_holds_the_file`
  - `tests/test_naming_apply_cli.py::test_an_identifier_it_cannot_name_is_held_with_its_own_reason[title-only-a-head-R-664]`
  - `tests/test_naming_apply_cli.py::test_an_identifier_stem_composes_its_one_name[a-camelot-key-without-a-tempo-renders-no-head]`
  - ... and 12 more, see the JSON sidecar

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
- Collected: 121 against a baseline of 121
- Kills: 3 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_target_a_collider_holds_is_held_back_too`
  - `tests/test_naming_apply_cli.py::test_a_target_another_mover_still_holds_is_promised_and_then_reported`
  - `tests/test_naming_apply_cli.py::test_one_file_is_planned_its_one_rename[a-marker-in-the-title-alone-is-recovered]`

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
- Collected: 121 against a baseline of 121
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
- Collected: 121 against a baseline of 121
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
- Collected: 121 against a baseline of 121
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
- Collected: 121 against a baseline of 121
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
- Collected: 121 against a baseline of 121
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
- Collected: 121 against a baseline of 121
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
- Collected: 121 against a baseline of 121
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
- Collected: 121 against a baseline of 121
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
- Collected: 121 against a baseline of 121
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
- Collected: 121 against a baseline of 121
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_an_identifier_it_cannot_name_is_held_with_its_own_reason[an-artist-and-no-title]`

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
- Collected: 121 against a baseline of 121
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
- Collected: 121 against a baseline of 121
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_an_identifier_it_cannot_name_is_held_with_its_own_reason[title-only-a-head-R-664]`

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
- Collected: 121 against a baseline of 121
- Kills: 10 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_composed_body_over_the_ceiling_is_fitted_not_left_as_a_number`
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_a_tag_edited_while_the_gate_waits_is_not_renamed_to_a_name_nobody_saw`
  - `tests/test_naming_apply_cli.py::test_an_identifier_stem_composes_its_one_name[a-camelot-key-without-a-tempo-renders-no-head]`
  - `tests/test_naming_apply_cli.py::test_an_identifier_stem_composes_its_one_name[a-head-in-the-title-tag-stays-out-of-the-body]`
  - `tests/test_naming_apply_cli.py::test_an_identifier_stem_composes_its_one_name[a-slash-takes-the-body-form-of-a-segment]`
  - `tests/test_naming_apply_cli.py::test_an_identifier_stem_is_composed_from_the_artist_and_title_tags`
  - `tests/test_naming_apply_cli.py::test_every_credited_artist_reaches_the_composed_body[an-empty-value-leads-with-no-comma]`
  - `tests/test_naming_apply_cli.py::test_every_credited_artist_reaches_the_composed_body[every-credited-artist]`
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
- Collected: 121 against a baseline of 121
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_every_credited_artist_reaches_the_composed_body[an-empty-value-leads-with-no-comma]`
  - `tests/test_naming_apply_cli.py::test_every_credited_artist_reaches_the_composed_body[every-credited-artist]`

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
- Collected: 121 against a baseline of 121
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_an_identifier_it_cannot_name_is_held_with_its_own_reason[title-only-a-head-R-664]`
  - `tests/test_naming_apply_cli.py::test_an_identifier_stem_composes_its_one_name[a-head-in-the-title-tag-stays-out-of-the-body]`

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
- Collected: 121 against a baseline of 121
- Kills: 9 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_only_asked_about_the_files_being_renamed`
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_an_identifier_it_cannot_name_is_held_with_its_own_reason[an-artist-and-no-title]`
  - `tests/test_naming_apply_cli.py::test_an_identifier_it_cannot_name_is_held_with_its_own_reason[no-tags-at-all]`
  - `tests/test_naming_apply_cli.py::test_an_identifier_it_cannot_name_is_held_with_its_own_reason[title-only-a-head-R-664]`
  - `tests/test_naming_apply_cli.py::test_an_identifier_with_no_artist_tag_is_held_and_named_in_the_plan`
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
- Collected: 121 against a baseline of 121
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
- Collected: 121 against a baseline of 121
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

### `r675.E2_key_not_casefolded`

existing layer: the referenced key keeps case, so a row differing from the file only in case no longer protects it

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `E2_key_not_casefolded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 121 against a baseline of 121
- Kills: 3 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_matched_to_a_candidate_by_name_ignoring_case`
  - `tests/test_naming_apply_cli.py::test_a_row_naming_the_file_another_way_still_protects_it[a-case-variant]`
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
- Collected: 121 against a baseline of 121
- Kills: 4 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_dark_tombstone_under_a_candidate_name_still_refuses`
  - `tests/test_naming_apply_cli.py::test_a_row_naming_the_file_another_way_still_protects_it[a-tombstoned-row]`
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
- Collected: 121 against a baseline of 121
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
- Collected: 121 against a baseline of 121
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
- Collected: 121 against a baseline of 121
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_file_is_protected_through_a_linked_root[link-recorded]`
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
- Collected: 121 against a baseline of 121
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
- Collected: 121 against a baseline of 121
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
- Collected: 121 against a baseline of 121
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
- Collected: 121 against a baseline of 121
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
- Collected: 121 against a baseline of 121
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
- Collected: 121 against a baseline of 121
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
- Collected: 121 against a baseline of 121
- Kills: 6 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_dark_row_under_another_name_lets_the_repair_run`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_only_asked_about_the_files_being_renamed`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_under_a_held_candidate_name_refuses_nothing`
  - `tests/test_naming_apply_cli.py::test_a_gone_file_under_another_name_refuses_nothing`
  - `tests/test_naming_apply_cli.py::test_a_row_that_can_name_no_candidate_neither_blocks_nor_protects[a-dark-tombstone-under-another-name-R-524]`
  - `tests/test_naming_apply_cli.py::test_a_row_that_can_name_no_candidate_neither_blocks_nor_protects[a-streamed-catalogue-path]`

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
- Collected: 121 against a baseline of 121
- Kills: 14 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_dark_row_recorded_after_the_gate_refuses_the_repair_before_any_rename`
  - `tests/intake/test_repair_apply.py::test_a_dark_row_under_a_proposal_name_refuses_the_repair_and_its_plan`
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
- Collected: 121 against a baseline of 121
- Kills: 14 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_dark_row_recorded_after_the_gate_refuses_the_repair_before_any_rename`
  - `tests/intake/test_repair_apply.py::test_a_dark_row_under_a_proposal_name_refuses_the_repair_and_its_plan`
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
- Collected: 121 against a baseline of 121
- Kills: 7 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_dark_row_recorded_after_the_gate_refuses_the_repair_before_any_rename`
  - `tests/intake/test_repair_apply.py::test_a_dark_row_under_a_proposal_name_refuses_the_repair_and_its_plan`
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
- Collected: 121 against a baseline of 121
- Kills: 15 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_dark_row_recorded_after_the_gate_refuses_the_repair_before_any_rename`
  - `tests/intake/test_repair_apply.py::test_a_dark_row_under_a_proposal_name_refuses_the_repair_and_its_plan`
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
  - `tests/test_naming_apply_cli.py::test_two_dark_rows_under_one_candidate_name_each_name_it`

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
- Collected: 121 against a baseline of 121
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
- Collected: 121 against a baseline of 121
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
- Collected: 121 against a baseline of 121
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

### `u212.N1_second_copy_compare`

naming_cli.second_copy: two different ISRCs read as one recording

- File: `src/cratekit/write/naming_cli.py`
- Source: `u212.json`, row `N1_second_copy_compare`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_second_copy.py`
- Collected: 6 against a baseline of 6
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_second_copy.py::test_a_target_held_by_another_recording_keeps_the_plain_collision`

Old text:

```
    return mine if tags.isrc_token(tags.read_tag(target, "isrc")) == mine else ""
```

New text:

```
    return mine if tags.isrc_token(tags.read_tag(target, "isrc")) != "" else ""
```

### `u212.N3_taken_plain`

naming_cli._taken: always the plain collision, never a second copy

- File: `src/cratekit/write/naming_cli.py`
- Source: `u212.json`, row `N3_taken_plain`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_second_copy.py`
- Collected: 6 against a baseline of 6
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_second_copy.py::test_a_copy_that_takes_the_name_after_the_plan_is_said_a_second_copy`
  - `tests/test_naming_second_copy.py::test_a_target_held_by_the_same_recording_is_said_as_a_second_copy`

Old text:

```
    same = second_copy(path, target)
    if same:
```

New text:

```
    same = second_copy(path, target)
    if False:
```

### `u212.N4_plan_isrc`

naming_cli._plan_for: the plan item carries no ISRC

- File: `src/cratekit/write/naming_cli.py`
- Source: `u212.json`, row `N4_plan_isrc`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_second_copy.py`
- Collected: 6 against a baseline of 6
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_second_copy.py::test_a_target_held_by_the_same_recording_is_said_as_a_second_copy`

Old text:

```
            if str(path) in seconds:
                item["isrc"] = seconds[str(path)]
```

New text:

```
(empty)
```

### `u212.N5_claim_plain`

naming_cli.name_apply: a name taken after the plan is always the plain collision, round one's F8

- File: `src/cratekit/write/naming_cli.py`
- Source: `u212.json`, row `N5_claim_plain`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_second_copy.py`, `tests/test_repair_rows.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_second_copy.py::test_a_copy_that_takes_the_name_after_the_plan_is_said_a_second_copy`

Old text:

```
                why, same = _taken(
                    path, target, fallback=f"{rendered.filename} is already taken in the folder"
                )
```

New text:

```
                why, same = f"{rendered.filename} is already taken in the folder", ""
```

### `u212.N6_cause_step`

naming_cli._incomplete_cause: the second copy step is never added

- File: `src/cratekit/write/naming_cli.py`
- Source: `u212.json`, row `N6_cause_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_second_copy.py`
- Collected: 6 against a baseline of 6
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_second_copy.py::test_a_target_held_by_the_same_recording_is_said_as_a_second_copy`

Old text:

```
    if any(item.get("isrc") for item in incomplete):
```

New text:

```
    if False:
```

### `u327.A24_spec_reads_title_head_first`

_spec_for: read the file name's head first again, so name apply writes the old tempo back over a corrected title

- File: `src/cratekit/write/naming_cli.py`
- Source: `u327.json`, row `A24_spec_reads_title_head_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/test_analyze_adopt.py`
- Collected: 213 against a baseline of 213
- Kills: 2 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_full_library_name_apply_after_the_adopt_brings_nothing_back`
  - `tests/test_naming_apply_cli.py::test_one_file_is_planned_its_one_rename[the-title-head-wins-over-the-filename-head]`

Old text:

```
        naming.parse_head(title, template=template)
        or naming.parse_head(path.name, template=template)
        or {}
```

New text:

```
        naming.parse_head(path.name, template=template)
        or naming.parse_head(title, template=template)
        or {}
```

### `u39-author-full.R3_bpm_dropped`

The recovered tempo is discarded, reproducing the head destroying defect

- File: `src/cratekit/write/naming_cli.py`
- Source: `u39-author-full.json`, row `R3_bpm_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 30 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_dark_row_under_a_held_candidate_name_refuses_nothing`
  - `tests/test_naming_apply_cli.py::test_a_file_analyze_run_measured_is_named_with_no_head_and_a_head_on_file_is_kept`
  - `tests/test_naming_apply_cli.py::test_a_file_gone_after_the_plan_is_named_rather_than_skipped`
  - `tests/test_naming_apply_cli.py::test_a_file_the_pass_must_leave_proposes_no_rename[in-convention]`
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_a_gone_file_under_another_name_refuses_nothing`
  - `tests/test_naming_apply_cli.py::test_a_padded_text_stem_with_tags_plans_nothing`
  - `tests/test_naming_apply_cli.py::test_a_referenced_file_does_not_hold_a_name_it_will_never_take`
  - `tests/test_naming_apply_cli.py::test_a_referenced_file_is_untouched_and_its_sibling_is_renamed`
  - `tests/test_naming_apply_cli.py::test_a_rename_onto_a_name_another_file_holds_overwrites_nothing`
  - `tests/test_naming_apply_cli.py::test_a_row_whose_file_exists_elsewhere_does_not_hold_a_namesake_in_the_library`
  - `tests/test_naming_apply_cli.py::test_a_stem_carrying_text_is_not_recomposed_from_its_tags`
  - `tests/test_naming_apply_cli.py::test_a_sweep_that_carried_out_every_rename_still_answers_ok`
  - `tests/test_naming_apply_cli.py::test_a_target_a_collider_holds_is_held_back_too`
  - `tests/test_naming_apply_cli.py::test_a_target_another_mover_still_holds_is_promised_and_then_reported`
  - ... and 15 more, see the JSON sidecar

Old text:

```
        bpm=int(head["bpm"]) if "bpm" in head else None,

```

New text:

```
        bpm=None,

```

### `u39-author-full.R4_head_key_overrules_tag`

The stale head key wins over a corrected initialkey tag

- File: `src/cratekit/write/naming_cli.py`
- Source: `u39-author-full.json`, row `R4_head_key_overrules_tag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[the-tag-key-wins-over-a-stale-head]`

Old text:

```
    key = tag_key if tag_key and naming.is_camelot(tag_key) else head.get("key")

```

New text:

```
    key = head.get("key") or tag_key

```

### `u39-author-full.R5_junk_tag_admitted`

A non Camelot initialkey tag reaches the renderer instead of being ignored

- File: `src/cratekit/write/naming_cli.py`
- Source: `u39-author-full.json`, row `R5_junk_tag_admitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_one_file_is_planned_its_one_rename[a-key-tag-not-camelot-is-ignored]`

Old text:

```
    key = tag_key if tag_key and naming.is_camelot(tag_key) else head.get("key")

```

New text:

```
    key = tag_key if tag_key else head.get("key")

```

### `u39-author-full.R6_lossy_flag_dropped`

The shared spec loses the lossy flag, recreating the plan and apply disagreement

- File: `src/cratekit/write/naming_cli.py`
- Source: `u39-author-full.json`, row `R6_lossy_flag_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 5 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_file_the_pass_must_leave_proposes_no_rename[marked-plan-agrees-with-apply]`
  - `tests/test_naming_apply_cli.py::test_a_file_the_pass_must_leave_proposes_no_rename[marker-in-filename-alone-kept]`
  - `tests/test_naming_apply_cli.py::test_a_target_a_collider_holds_is_held_back_too`
  - `tests/test_naming_apply_cli.py::test_a_target_another_mover_still_holds_is_promised_and_then_reported`
  - `tests/test_naming_apply_cli.py::test_one_file_is_planned_its_one_rename[a-marker-in-the-title-alone-is-recovered]`

Old text:

```
        lossy=marker in path.stem or marker in title,

```

New text:

```
        lossy=False,

```

### `u39-naming-independent.R5_bpm_wrong_type`

The recovered tempo is coerced to float instead of int

- File: `src/cratekit/write/naming_cli.py`
- Source: `u39-naming-independent.json`, row `R5_bpm_wrong_type`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 72 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_collision_answers_with_the_files_that_stayed_put`
  - `tests/test_naming_apply_cli.py::test_a_composition_variant_of_the_name_still_protects_its_file[NFC]`
  - `tests/test_naming_apply_cli.py::test_a_composition_variant_of_the_name_still_protects_its_file[NFD]`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_matched_across_folders_by_leaf_alone`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_matched_to_a_candidate_by_name_ignoring_case`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_only_asked_about_the_files_being_renamed`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_under_a_held_candidate_name_refuses_nothing`
  - `tests/test_naming_apply_cli.py::test_a_dark_tombstone_under_a_candidate_name_still_refuses`
  - `tests/test_naming_apply_cli.py::test_a_database_with_no_matching_row_proceeds`
  - `tests/test_naming_apply_cli.py::test_a_file_analyze_run_measured_is_named_with_no_head_and_a_head_on_file_is_kept`
  - `tests/test_naming_apply_cli.py::test_a_file_gone_after_the_plan_is_named_rather_than_skipped`
  - `tests/test_naming_apply_cli.py::test_a_file_is_protected_through_a_linked_root[link-recorded]`
  - `tests/test_naming_apply_cli.py::test_a_file_is_protected_through_a_linked_root[real-path-recorded]`
  - `tests/test_naming_apply_cli.py::test_a_file_the_pass_must_leave_proposes_no_rename[in-convention]`
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - ... and 57 more, see the JSON sidecar

Old text:

```
        bpm=int(head["bpm"]) if "bpm" in head else None,

```

New text:

```
        bpm=float(head["bpm"]) if "bpm" in head else None,

```

### `u41-author-full.R6_head_key_overrules_tag`

Key precedence reversed, so a corrected key tag can no longer move a file

- File: `src/cratekit/write/naming_cli.py`
- Source: `u41-author-full.json`, row `R6_head_key_overrules_tag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[the-tag-key-wins-over-a-stale-head]`

Old text:

```
    key = tag_key if tag_key and naming.is_camelot(tag_key) else head.get("key")

```

New text:

```
    key = head.get("key") or (tag_key if tag_key and naming.is_camelot(tag_key) else None)

```

### `u41-author-full.T1_title_tag_fed_the_filename_body`

The title tag is rebuilt from the filename body, which stuffs the artist and the album into every tag the apply pass rewrites

- File: `src/cratekit/write/naming_cli.py`
- Source: `u41-author-full.json`, row `T1_title_tag_fed_the_filename_body`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 4 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_file_analyze_run_measured_is_named_with_no_head_and_a_head_on_file_is_kept`
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[a-deduping-rename-converges-on-one-pass]`
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[the-title-tag-is-not-given-the-filename-body]`

Old text:

```
        title=naming.strip_head(title, template=template),

```

New text:

```
        title=naming.strip_head(path.stem, template=template),

```

### `u41-author-full.T2_title_field_dropped`

The spec stops carrying a title at all, so render_all falls back to the stem for the tag surface

- File: `src/cratekit/write/naming_cli.py`
- Source: `u41-author-full.json`, row `T2_title_field_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 4 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_file_analyze_run_measured_is_named_with_no_head_and_a_head_on_file_is_kept`
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[a-deduping-rename-converges-on-one-pass]`
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[the-title-tag-is-not-given-the-filename-body]`

Old text:

```
        title=naming.strip_head(title, template=template),

```

New text:

```
        title=None,

```

### `u41-naming-independent.B7_lossy_filename_operand_dropped`

U39's K2: the lossy OR loses its filename operand, so a file marked only in its name is renamed to its unmarked form

- File: `src/cratekit/write/naming_cli.py`
- Source: `u41-naming-independent.json`, row `B7_lossy_filename_operand_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_file_the_pass_must_leave_proposes_no_rename[marker-in-filename-alone-kept]`

Old text:

```
        lossy=marker in path.stem or marker in title,

```

New text:

```
        lossy=marker in title,

```

### `u41-naming-independent.B8_lossy_title_operand_dropped`

U39's K1: the lossy OR loses its title operand, so a marker surviving only in the tag stops being restored

- File: `src/cratekit/write/naming_cli.py`
- Source: `u41-naming-independent.json`, row `B8_lossy_title_operand_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 3 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_target_a_collider_holds_is_held_back_too`
  - `tests/test_naming_apply_cli.py::test_a_target_another_mover_still_holds_is_promised_and_then_reported`
  - `tests/test_naming_apply_cli.py::test_one_file_is_planned_its_one_rename[a-marker-in-the-title-alone-is-recovered]`

Old text:

```
        lossy=marker in path.stem or marker in title,

```

New text:

```
        lossy=marker in path.stem,

```

### `u41-naming-independent.C1_plan_no_op_filter_dropped`

Every audio file enters the plan, including the ones already in convention

- File: `src/cratekit/write/naming_cli.py`
- Source: `u41-naming-independent.json`, row `C1_plan_no_op_filter_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 14 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_file_the_pass_must_leave_proposes_no_rename[13A-is-no-head]`
  - `tests/test_naming_apply_cli.py::test_a_file_the_pass_must_leave_proposes_no_rename[in-convention]`
  - `tests/test_naming_apply_cli.py::test_a_file_the_pass_must_leave_proposes_no_rename[marked-plan-agrees-with-apply]`
  - `tests/test_naming_apply_cli.py::test_a_file_the_pass_must_leave_proposes_no_rename[marker-in-filename-alone-kept]`
  - `tests/test_naming_apply_cli.py::test_a_letterless_stem_that_is_not_a_number_is_carried_as_it_is`
  - `tests/test_naming_apply_cli.py::test_a_padded_text_stem_with_tags_plans_nothing`
  - `tests/test_naming_apply_cli.py::test_a_rename_onto_a_name_another_file_holds_overwrites_nothing`
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[a-deduping-rename-converges-on-one-pass]`
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[an-unpadded-head-is-padded-with-the-tempo-intact]`
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[no-title-tag-takes-the-body-from-the-filename]`
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[the-filename-head-alone-is-enough]`
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[the-head-is-recovered-from-the-title-tag]`
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[the-tag-key-wins-over-a-stale-head]`
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[the-title-tag-is-not-given-the-filename-body]`

Old text:

```
            if rendered.filename != path.name:

```

New text:

```
            if True:

```

### `u67-round-2.C1_action_filter_and_recheck`

Composite: apply every plan item AND drop the re-check before the rename

- File: `src/cratekit/write/naming_cli.py`
- Source: `u67-round-2.json`, row `C1_action_filter_and_recheck`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 19 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_collision_answers_with_the_files_that_stayed_put`
  - `tests/test_naming_apply_cli.py::test_a_composition_variant_of_the_name_still_protects_its_file[NFC]`
  - `tests/test_naming_apply_cli.py::test_a_composition_variant_of_the_name_still_protects_its_file[NFD]`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_only_asked_about_the_files_being_renamed`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_under_a_held_candidate_name_refuses_nothing`
  - `tests/test_naming_apply_cli.py::test_a_file_is_protected_through_a_linked_root[link-recorded]`
  - `tests/test_naming_apply_cli.py::test_a_file_is_protected_through_a_linked_root[real-path-recorded]`
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_a_referenced_file_does_not_hold_a_name_it_will_never_take`
  - `tests/test_naming_apply_cli.py::test_a_referenced_file_is_untouched_and_its_sibling_is_renamed`
  - `tests/test_naming_apply_cli.py::test_a_referenced_identifier_file_is_held_as_referenced_and_never_owed`
  - `tests/test_naming_apply_cli.py::test_a_root_outside_the_library_is_still_checked`
  - `tests/test_naming_apply_cli.py::test_a_row_naming_the_file_another_way_still_protects_it[a-case-variant]`
  - `tests/test_naming_apply_cli.py::test_a_row_naming_the_file_another_way_still_protects_it[a-tombstoned-row]`
  - `tests/test_naming_apply_cli.py::test_a_row_naming_the_file_another_way_still_protects_it[recorded-as-a-location-url]`
  - ... and 4 more, see the JSON sidecar

Old text:

```
    renames = [item for item in plan["items"] if item["action"] == RENAME]
```

New text:

```
    renames = list(plan["items"])
    _is_referenced = lambda path, referenced: False  # noqa: E731
```

### `u67.M2_nfc`

Skip NFC normalisation of the compared path

- File: `src/cratekit/write/naming_cli.py`
- Source: `u67.json`, row `M2_nfc`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_composition_variant_of_the_name_still_protects_its_file[NFD]`

Old text:

```
    return locations.norm_for_compare(path).casefold()
```

New text:

```
    return path.casefold()
```

### `u67.M3_prefix_resolution`

Drop the prefix mapped spelling of a row

- File: `src/cratekit/write/naming_cli.py`
- Source: `u67.json`, row `M3_prefix_resolution`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_under_a_remapped_volume_still_protects_its_file[prefix_map0]`

Old text:

```
        if resolved.path is not None:
            keys.add(_key(resolved.path))
```

New text:

```
        if False:
            keys.add(_key(resolved.path))
```

### `u67.M6_remote_host_skip`

Let a row naming another host raise instead of being skipped

- File: `src/cratekit/write/naming_cli.py`
- Source: `u67.json`, row `M6_remote_host_skip`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_that_can_name_no_candidate_neither_blocks_nor_protects[a-row-naming-another-host]`

Old text:

```
        except locations.LocationDecodeError:
            continue
```

New text:

```
        except ZeroDivisionError:
            continue
```

### `u67.M7_absolute_spelling`

Ask only the resolved spelling of a candidate

- File: `src/cratekit/write/naming_cli.py`
- Source: `u67.json`, row `M7_absolute_spelling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_file_is_protected_through_a_linked_root[link-recorded]`

Old text:

```
    return _key(str(path.absolute())) in referenced or _key(str(path.resolve())) in referenced
```

New text:

```
    return _key(str(path.resolve())) in referenced
```

### `u67.M8_resolved_spelling`

Ask only the absolute spelling of a candidate

- File: `src/cratekit/write/naming_cli.py`
- Source: `u67.json`, row `M8_resolved_spelling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_file_is_protected_through_a_linked_root[real-path-recorded]`

Old text:

```
    return _key(str(path.absolute())) in referenced or _key(str(path.resolve())) in referenced
```

New text:

```
    return _key(str(path.absolute())) in referenced
```

### `u67.R1_refusal_to_empty`

A classified open failure reads as an empty collection instead of refusing

- File: `src/cratekit/write/naming_cli.py`
- Source: `u67.json`, row `R1_refusal_to_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 3 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_library_with_cloud_sync_on_refuses_and_names_the_real_cause`
  - `tests/test_naming_apply_cli.py::test_a_missing_database_refuses_and_renames_nothing`
  - `tests/test_naming_apply_cli.py::test_an_unopenable_database_refuses_and_renames_nothing`

Old text:

```
    except CratekitError as exc:
        inner = exc.cause
```

New text:

```
    except CratekitError as exc:
        return ()
        inner = exc.cause
```

### `u67.R2_generic_to_empty`

A read that fails after the open reads as an empty collection instead of refusing

- File: `src/cratekit/write/naming_cli.py`
- Source: `u67.json`, row `R2_generic_to_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_read_that_fails_after_the_open_refuses_and_renames_nothing`

Old text:

```
    except Exception as exc:  # noqa: BLE001 - every failed read is one refusal
        raise refuse(
```

New text:

```
    except Exception as exc:  # noqa: BLE001 - every failed read is one refusal
        return ()
        raise refuse(
```

### `u67.R3_remedy_passthrough`

Drop the inner remedy, so the refusal defaults to restore-from-snapshot

- File: `src/cratekit/write/naming_cli.py`
- Source: `u67.json`, row `R3_remedy_passthrough`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_library_with_cloud_sync_on_refuses_and_names_the_real_cause`
  - `tests/test_naming_apply_cli.py::test_a_missing_database_refuses_and_renames_nothing`

Old text:

```
            remedy=inner.remediation.remedy or (None if steps else Remedy.REPORT_DEFECT),
            steps=steps,
```

New text:

```
            remedy=None,
            steps=(),
```

### `u302.W1_intake_replace_bumps_count`

insert_intake_playlist: a replaced playlist bumps its folder's count as if it were new

- File: `src/cratekit/write/rbxml.py`
- Source: `u302.json`, row `W1_intake_replace_bumps_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_an_intake_playlist_replaced_leaves_its_folders_count_alone`

Old text:

```
    if existing is None:
        _bump_count(content, parent, +1)
```

New text:

```
    if True:
        _bump_count(content, parent, +1)
```

### `u302.W2_self_closed_node_deepens`

_node_tokens: a self closed node counts as an open one

- File: `src/cratekit/write/rbxml.py`
- Source: `u302.json`, row `W2_self_closed_node_deepens`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_registry.py`
- Collected: 164 against a baseline of 164
- Kills: 15 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_failure_after_an_earlier_merge_writes_nothing`
  - `tests/test_rbxml.py::test_a_merge_point_sharing_its_line_refuses_and_writes_nothing`
  - `tests/test_rbxml.py::test_insert_genre_folder_byte_exact`
  - `tests/test_rbxml.py::test_insert_genre_folder_is_idempotent`
  - `tests/test_rbxml.py::test_insert_root_playlist_and_idempotent_replace`
  - `tests/test_rbxml.py::test_insert_then_remove_round_trips`
  - `tests/test_rbxml.py::test_remove_folder_node_absent_is_warning_noop`
  - `tests/test_rbxml.py::test_remove_folder_node_self_closed_target_does_not_wipe_siblings`
  - `tests/test_rbxml.py::test_remove_folder_node_with_track_bearing_subs`
  - `tests/test_rbxml.py::test_self_closed_folder_and_playlist_are_merged_into`
  - `tests/test_rbxml.py::test_two_siblings_of_one_name_refuse_and_write_nothing`
  - `tests/test_tree_registry.py::test_a_raw_angle_bracket_in_a_display_name_does_not_unanchor_the_document`
  - `tests/test_xml_splice_golden.py::test_add_vocal_playlists_golden`
  - `tests/test_xml_splice_golden.py::test_add_vocal_playlists_is_idempotent`
  - `tests/test_xml_splice_golden.py::test_unplaced_new_sub_golden`

Old text:

```
            yield (0 if self_closing else 1), opening
```

New text:

```
            yield 1, opening
```

### `u302.W3_close_tag_not_counted`

_node_tokens: a close tag no longer ends a level

- File: `src/cratekit/write/rbxml.py`
- Source: `u302.json`, row `W3_close_tag_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_registry.py`
- Collected: 164 against a baseline of 164
- Kills: 58 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_caller_naming_one_playlist_twice_gets_one_on_the_creating_write`
  - `tests/test_rbxml.py::test_a_catalog_written_twice_is_byte_identical_to_written_once`
  - `tests/test_rbxml.py::test_a_failure_after_an_earlier_merge_writes_nothing`
  - `tests/test_rbxml.py::test_a_held_playlist_with_no_entry_count_refuses_rather_than_guessing_one`
  - `tests/test_rbxml.py::test_a_merge_point_sharing_its_line_refuses_and_writes_nothing`
  - `tests/test_rbxml.py::test_a_name_drawn_two_ways_in_unicode_is_one_folder`
  - `tests/test_rbxml.py::test_a_new_year_is_placed_among_held_years_the_caller_did_not_name`
  - `tests/test_rbxml.py::test_a_new_year_lands_first_or_last_by_the_callers_order`
  - `tests/test_rbxml.py::test_a_node_whose_kind_is_unreadable_is_never_described_as_a_playlist`
  - `tests/test_rbxml.py::test_a_playlist_that_gains_nothing_is_left_byte_identical`
  - `tests/test_rbxml.py::test_a_second_write_with_one_new_year_adds_that_playlist_and_nothing_else`
  - `tests/test_rbxml.py::test_a_similarly_named_sibling_folder_is_untouched`
  - `tests/test_rbxml.py::test_a_writer_refuses_to_replace_a_node_of_the_other_type`
  - `tests/test_rbxml.py::test_an_intake_playlist_replaced_leaves_its_folders_count_alone`
  - `tests/test_rbxml.py::test_insert_genre_folder_byte_exact`
  - ... and 43 more, see the JSON sidecar

Old text:

```
            yield -1, closing
```

New text:

```
            yield 0, closing
```

### `u302.W4_open_tag_never_self_closing`

_open_tag: every open tag is read as one that has children

- File: `src/cratekit/write/rbxml.py`
- Source: `u302.json`, row `W4_open_tag_never_self_closing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_registry.py`
- Collected: 164 against a baseline of 164
- Kills: 17 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_failure_after_an_earlier_merge_writes_nothing`
  - `tests/test_rbxml.py::test_a_merge_point_sharing_its_line_refuses_and_writes_nothing`
  - `tests/test_rbxml.py::test_rating_patch_is_exact_id_match`
  - `tests/test_rbxml.py::test_remove_folder_node_self_closed_target_does_not_wipe_siblings`
  - `tests/test_rbxml.py::test_self_closed_folder_and_playlist_are_merged_into`
  - `tests/test_rbxml.py::test_splice_digit_growth_into_self_closing_sub`
  - `tests/test_rbxml.py::test_splice_is_playlists_scoped`
  - `tests/test_rbxml.py::test_two_siblings_of_one_name_refuse_and_write_nothing`
  - `tests/test_tree_registry.py::test_a_track_id_never_matches_a_longer_one`
  - `tests/test_tree_registry.py::test_the_locates_read_attributes_in_either_order`
  - `tests/test_xml_splice_golden.py::test_add_vocal_playlists_is_idempotent`
  - `tests/test_xml_splice_golden.py::test_name_collision_current_behaviour`
  - `tests/test_xml_splice_golden.py::test_rating_write_golden[sort_inbox_rating]`
  - `tests/test_xml_splice_golden.py::test_rating_write_golden[sort_unplaced_rating]`
  - `tests/test_xml_splice_golden.py::test_route_into_energy_sub_golden`
  - ... and 2 more, see the JSON sidecar

Old text:

```
    return match, dict(_ATTR_PAIR.findall(raw_attrs)), raw_attrs.endswith(b"/")
```

New text:

```
    return match, dict(_ATTR_PAIR.findall(raw_attrs)), False
```

### `u76-a.D3_tree_level_lookup`

_write_catalog: locate the catalog tree under ROOT with direct_child, so two trees of one name are written into rather than refused

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-a.json`, row `D3_tree_level_lookup`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_two_siblings_of_one_name_refuse_and_write_nothing`

Old text:

```
        found = _sole_child(content, root, tree.display, FOLDER_TYPE)
```

New text:

```
        found = direct_child(content, root, tree.display, FOLDER_TYPE)
```

### `u76-a.D4_folder_level_lookup`

_write_catalog: locate the label folder with direct_child, so two folders of the label's name are written into rather than refused

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-a.json`, row `D4_folder_level_lookup`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 2 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_name_drawn_two_ways_in_unicode_is_one_folder`
  - `tests/test_rbxml.py::test_two_siblings_of_one_name_refuse_and_write_nothing`

Old text:

```
    existing = _sole_child(content, parent, folder_name, FOLDER_TYPE)
```

New text:

```
    existing = direct_child(content, parent, folder_name, FOLDER_TYPE)
```

### `u76-a.D5_playlist_level_lookup`

_merge_catalog: locate a held year playlist with direct_child, so two playlists of one year are written into rather than refused

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-a.json`, row `D5_playlist_level_lookup`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 3 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_name_drawn_two_ways_in_unicode_is_one_folder`
  - `tests/test_rbxml.py::test_two_siblings_of_one_name_refuse_and_write_nothing`
  - `tests/test_tree_writer.py::test_the_catalog_check_refuses_a_held_year_playlist_that_appears_twice`

Old text:

```
        playlist = _sole_child(content, here, name, PLAYLIST_TYPE)
```

New text:

```
        playlist = direct_child(content, here, name, PLAYLIST_TYPE)
```

### `u76-a.M1_merge_not_append`

_write_catalog: never take the merge path, so a held folder gets a second folder of its name beside it (the R-129 doubling)

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-a.json`, row `M1_merge_not_append`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 16 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_catalog_written_twice_is_byte_identical_to_written_once`
  - `tests/test_rbxml.py::test_a_failure_after_an_earlier_merge_writes_nothing`
  - `tests/test_rbxml.py::test_a_held_playlist_with_no_entry_count_refuses_rather_than_guessing_one`
  - `tests/test_rbxml.py::test_a_merge_point_sharing_its_line_refuses_and_writes_nothing`
  - `tests/test_rbxml.py::test_a_name_drawn_two_ways_in_unicode_is_one_folder`
  - `tests/test_rbxml.py::test_a_new_year_is_placed_among_held_years_the_caller_did_not_name`
  - `tests/test_rbxml.py::test_a_playlist_that_gains_nothing_is_left_byte_identical`
  - `tests/test_rbxml.py::test_a_second_write_with_one_new_year_adds_that_playlist_and_nothing_else`
  - `tests/test_rbxml.py::test_self_closed_folder_and_playlist_are_merged_into`
  - `tests/test_rbxml.py::test_track_ids_are_deduplicated_inside_a_playlist`
  - `tests/test_rbxml.py::test_two_siblings_of_one_name_refuse_and_write_nothing`
  - `tests/test_tree_writer.py::test_a_catalog_rerun_refreshes_the_folder_rather_than_duplicating_it`
  - `tests/test_tree_writer.py::test_one_source_the_writer_refuses_writes_none_of_them`
  - `tests/test_tree_writer.py::test_the_catalog_check_reaches_a_held_playlist_the_writer_cannot_extend`
  - `tests/test_tree_writer.py::test_the_catalog_check_refuses_a_held_year_playlist_that_appears_twice`
  - ... and 1 more, see the JSON sidecar

Old text:

```
    if existing is not None:
        return _merge_catalog(content, existing, pairs)
```

New text:

```
    if existing is not None and not existing:
        return _merge_catalog(content, existing, pairs)
```

### `u76-a.W1_copy_on_write`

insert_catalog_folder: edit the caller's document directly, so a refusal after an earlier merge leaves that merge behind

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-a.json`, row `W1_copy_on_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 2 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_failure_after_an_earlier_merge_writes_nothing`
  - `tests/test_rbxml.py::test_a_merge_point_sharing_its_line_refuses_and_writes_nothing`

Old text:

```
    work = bytearray(content)
    warning = _write_catalog(
```

New text:

```
    work = content
    warning = _write_catalog(
```

### `u76-a.W2_commit_on_success`

insert_catalog_folder: copy the working bytes back even on a refusal

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-a.json`, row `W2_commit_on_success`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 2 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_failure_after_an_earlier_merge_writes_nothing`
  - `tests/test_rbxml.py::test_a_merge_point_sharing_its_line_refuses_and_writes_nothing`

Old text:

```
    if warning is None:
        content[:] = work
    return warning
```

New text:

```
    if warning is None or warning:
        content[:] = work
    return warning
```

### `u76-a.X1_dedupe_against_held`

_extend_playlist: dedupe the new ids against nothing, so a member the playlist holds is added again

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-a.json`, row `X1_dedupe_against_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 6 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_catalog_written_twice_is_byte_identical_to_written_once`
  - `tests/test_rbxml.py::test_a_name_drawn_two_ways_in_unicode_is_one_folder`
  - `tests/test_rbxml.py::test_a_playlist_that_gains_nothing_is_left_byte_identical`
  - `tests/test_rbxml.py::test_a_second_write_with_one_new_year_adds_that_playlist_and_nothing_else`
  - `tests/test_rbxml.py::test_track_ids_are_deduplicated_inside_a_playlist`
  - `tests/test_xml_splice_golden.py::test_label_subtree_written_twice_matches_the_single_write_golden`

Old text:

```
    fresh = dedupe_track_ids(track_ids, track_keys(content, playlist))
```

New text:

```
    fresh = dedupe_track_ids(track_ids, ())
```

### `u76-b.C1_count_bump`

_merge_catalog: move the folder's Count by one less than the playlists created

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-b.json`, row `C1_count_bump`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 3 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_new_year_lands_first_or_last_by_the_callers_order`
  - `tests/test_rbxml.py::test_a_second_write_with_one_new_year_adds_that_playlist_and_nothing_else`
  - `tests/test_rbxml.py::test_self_closed_folder_and_playlist_are_merged_into`

Old text:

```
        _bump_count(content, here, created)
```

New text:

```
        _bump_count(content, here, created - 1)
```

### `u76-b.L1_folder_own_line`

_merge_catalog: drop the check that the held folder starts its own line

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-b.json`, row `L1_folder_own_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_merge_point_sharing_its_line_refuses_and_writes_nothing`

Old text:

```
    if not _starts_its_line(content, folder.line_start, folder.tag_start):
        return f"the folder {folder.name!r} does not start its own line"
```

New text:

```
    if False:
        return f"the folder {folder.name!r} does not start its own line"
```

### `u76-b.L2_anchor_own_line`

_merge_catalog: drop the check that the playlist a new year goes before starts its own line

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-b.json`, row `L2_anchor_own_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_merge_point_sharing_its_line_refuses_and_writes_nothing`

Old text:

```
            if not _starts_its_line(content, at, anchor.tag_start):
```

New text:

```
            if False:
```

### `u76-b.L3_folder_close_own_line`

_merge_catalog: drop the check that the folder's close tag starts its own line

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-b.json`, row `L3_folder_close_own_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_merge_point_sharing_its_line_refuses_and_writes_nothing`

Old text:

```
            if not _starts_its_line(content, at, here.close_start):
```

New text:

```
            if False:
```

### `u76-b.L4_playlist_close_own_line`

_extend_playlist: drop the check that a held playlist's close tag starts its own line

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-b.json`, row `L4_playlist_close_own_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_merge_point_sharing_its_line_refuses_and_writes_nothing`

Old text:

```
        if not _starts_its_line(content, at, playlist.close_start):
```

New text:

```
        if False:
```

### `u76-b.O1_anchor_order`

_merge_catalog: place a new year before the first held playlist sorting ABOVE it, reversing newest first

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-b.json`, row `O1_anchor_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 4 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_merge_point_sharing_its_line_refuses_and_writes_nothing`
  - `tests/test_rbxml.py::test_a_new_year_is_placed_among_held_years_the_caller_did_not_name`
  - `tests/test_rbxml.py::test_a_new_year_lands_first_or_last_by_the_callers_order`
  - `tests/test_rbxml.py::test_a_second_write_with_one_new_year_adds_that_playlist_and_nothing_else`

Old text:

```
                if child.node_type == PLAYLIST_TYPE and _folded(child.name) < wanted
```

New text:

```
                if child.node_type == PLAYLIST_TYPE and _folded(child.name) > wanted
```

### `u76-b.O2_anchor_none`

_merge_catalog: always append a new year last

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-b.json`, row `O2_anchor_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 4 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_merge_point_sharing_its_line_refuses_and_writes_nothing`
  - `tests/test_rbxml.py::test_a_new_year_is_placed_among_held_years_the_caller_did_not_name`
  - `tests/test_rbxml.py::test_a_new_year_lands_first_or_last_by_the_callers_order`
  - `tests/test_rbxml.py::test_a_second_write_with_one_new_year_adds_that_playlist_and_nothing_else`

Old text:

```
                if child.node_type == PLAYLIST_TYPE and _folded(child.name) < wanted
```

New text:

```
                if child.node_type == PLAYLIST_TYPE and _folded(child.name) < wanted and False
```

### `u76-b.S1_self_closed_folder`

_merge_catalog: do not open a self closed held folder before merging into it

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-b.json`, row `S1_self_closed_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_self_closed_folder_and_playlist_are_merged_into`

Old text:

```
    if folder.self_closing:
        # An empty folder exported self closed
```

New text:

```
    if folder.self_closing and not folder.self_closing:
        # An empty folder exported self closed
```

### `u76-b.X2_entries_count`

_extend_playlist: move Entries by the ids offered rather than the ids added

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-b.json`, row `X2_entries_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 2 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_name_drawn_two_ways_in_unicode_is_one_folder`
  - `tests/test_rbxml.py::test_track_ids_are_deduplicated_inside_a_playlist`

Old text:

```
    total = _read_int(content, entries) + len(fresh)
```

New text:

```
    total = _read_int(content, entries) + len(track_ids)
```

### `u76-b.X3_self_closed_playlist`

_extend_playlist: treat a self closed playlist as open, writing at the line of a close tag it does not have

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-b.json`, row `X3_self_closed_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 3 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_failure_after_an_earlier_merge_writes_nothing`
  - `tests/test_rbxml.py::test_a_merge_point_sharing_its_line_refuses_and_writes_nothing`
  - `tests/test_rbxml.py::test_self_closed_folder_and_playlist_are_merged_into`

Old text:

```
    if playlist.self_closing:
        content[playlist.tag_end - 1 : playlist.tag_end + 1] = bytearray(
            b">" + CRLF + lines + b" " * playlist.indent + _NODE_CLOSE
```

New text:

```
    if playlist.self_closing and not playlist.self_closing:
        content[playlist.tag_end - 1 : playlist.tag_end + 1] = bytearray(
            b">" + CRLF + lines + b" " * playlist.indent + _NODE_CLOSE
```

### `u76-b.X4_track_indent`

_extend_playlist: write the added track keys at the playlist's own indent rather than one step in

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-b.json`, row `X4_track_indent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_self_closed_folder_and_playlist_are_merged_into`

Old text:

```
    lines = track_key_lines(fresh, playlist.indent + INDENT_STEP).encode("utf-8")
```

New text:

```
    lines = track_key_lines(fresh, playlist.indent).encode("utf-8")
```

### `u76-zeros.X5_entries_absent`

_extend_playlist: write the ids into a held playlist with no Entries attribute rather than refusing

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-zeros.json`, row `X5_entries_absent`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 3 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_held_playlist_with_no_entry_count_refuses_rather_than_guessing_one`
  - `tests/test_tree_writer.py::test_one_source_the_writer_refuses_writes_none_of_them`
  - `tests/test_tree_writer.py::test_the_catalog_check_reaches_a_held_playlist_the_writer_cannot_extend`

Old text:

```
    if entries is None:
        return f"Entries attr not found for playlist {playlist.name!r}"
    total = _read_int(content, entries) + len(fresh)
```

New text:

```
    if entries is None:
        entries = (playlist.tag_end, playlist.tag_end)
    total = _read_int(content, entries) + len(fresh) if entries[0] != entries[1] else len(fresh)
```

### `u76-a.D1_duplicate_sibling`

_sole_child: answer the first of two same named siblings instead of refusing the duplicate (R-129's refusal removed)

- File: `src/cratekit/write/rbxml_insert.py`
- Source: `u76-a.json`, row `D1_duplicate_sibling`
- Moved: the same text, now in src/cratekit/write/rbxml_insert.py, was in src/cratekit/write/rbxml.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 2 (killed)
- Killed:
  - `tests/test_rbxml.py::test_two_siblings_of_one_name_refuse_and_write_nothing`
  - `tests/test_tree_writer.py::test_the_catalog_check_refuses_a_held_year_playlist_that_appears_twice`

Old text:

```
    if len(matches) > 1:
        return (
            f"{len(matches)} {_type_name(node_type)}s named
```

New text:

```
    if len(matches) > 99:
        return (
            f"{len(matches)} {_type_name(node_type)}s named
```

### `u76-a.D2_type_collision`

_sole_child: check the type of every match but the first, so a same named node of the other type standing first is merged into

- File: `src/cratekit/write/rbxml_insert.py`
- Source: `u76-a.json`, row `D2_type_collision`
- Moved: the same text, now in src/cratekit/write/rbxml_insert.py, was in src/cratekit/write/rbxml.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_failure_after_an_earlier_merge_writes_nothing`

Old text:

```
    for child in matches:
        if child.node_type != node_type:
```

New text:

```
    for child in matches[1:]:
        if child.node_type != node_type:
```

### `u76-a.F1_nfc_fold`

_folded: compare names as given, so a composed and a decomposed spelling of one label are two folders

- File: `src/cratekit/write/rbxml_insert.py`
- Source: `u76-a.json`, row `F1_nfc_fold`
- Moved: the same text, now in src/cratekit/write/rbxml_insert.py, was in src/cratekit/write/rbxml.py; the text also occurs in an intake module, so the tool could not pick the file
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_name_drawn_two_ways_in_unicode_is_one_folder`

Old text:

```
    return unicodedata.normalize("NFC", name)
```

New text:

```
    return name
```

### `u76-a.F2_case_fold`

_folded: fold case as well, so a label differing only by case is poured into another label's folder

- File: `src/cratekit/write/rbxml_insert.py`
- Source: `u76-a.json`, row `F2_case_fold`
- Moved: the same text, now in src/cratekit/write/rbxml_insert.py, was in src/cratekit/write/rbxml.py; the text also occurs in an intake module, so the tool could not pick the file
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_similarly_named_sibling_folder_is_untouched`

Old text:

```
    return unicodedata.normalize("NFC", name)
```

New text:

```
    return unicodedata.normalize("NFC", name).casefold()
```

### `u76-a.P2_dedupe_ids`

_merged_pairs: keep a batch's repeated ids, so a playlist lists one track twice

- File: `src/cratekit/write/rbxml_insert.py`
- Source: `u76-a.json`, row `P2_dedupe_ids`
- Moved: the same text, now in src/cratekit/write/rbxml_insert.py, was in src/cratekit/write/rbxml.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 2 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_caller_naming_one_playlist_twice_gets_one_on_the_creating_write`
  - `tests/test_rbxml.py::test_track_ids_are_deduplicated_inside_a_playlist`

Old text:

```
    return [(joined[key][0], dedupe_track_ids(joined[key][1])) for key in order]
```

New text:

```
    return [(joined[key][0], list(joined[key][1])) for key in order]
```

### `u76-zeros.P1_join_pairs`

_merged_pairs: keep every pair as given, so a caller naming one playlist twice emits two siblings of that name

- File: `src/cratekit/write/rbxml_insert.py`
- Source: `u76-zeros.json`, row `P1_join_pairs`
- Moved: the same text, now in src/cratekit/write/rbxml_insert.py, was in src/cratekit/write/rbxml.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_caller_naming_one_playlist_twice_gets_one_on_the_creating_write`

Old text:

```
    return [(joined[key][0], dedupe_track_ids(joined[key][1])) for key in order]
```

New text:

```
    return [(name, dedupe_track_ids(ids)) for name, ids in playlists]
```

### `r312.E2_vocal_gap_filter_off`

left_behind: return every unexpected membership, so a vocal playlist nothing compared is named as left behind

- File: `src/cratekit/write/rebuild.py`
- Source: `r312.json`, row `E2_vocal_gap_filter_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 309 against a baseline of 309
- Kills: 1 (killed)
- Killed:
  - `tests/test_rebuild.py::test_a_vocal_playlist_nothing_compared_is_not_named_as_left_behind`

Old text:

```
    return tuple(entry for entry in after.unexpected if entry.sub not in skipped)
```

New text:

```
    return tuple(entry for entry in after.unexpected if entry.sub is not None)
```

### `r316.M10_derivation_restates_no_gap`

derive_from_taxonomy stops calling not_derived and reports no gaps, so the resume and the derivation disagree

- File: `src/cratekit/write/rebuild.py`
- Source: `r316.json`, row `M10_derivation_restates_no_gap`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`, `tests/test_rebuild.py`
- Collected: 309 against a baseline of 309
- Kills: 9 (killed)
- Killed:
  - `tests/test_rebuild.py::test_a_library_with_no_vocal_calibration_reports_what_it_did_not_compare`
  - `tests/test_rebuild.py::test_a_vocal_playlist_nothing_compared_is_not_named_as_left_behind`
  - `tests/test_rebuild.py::test_the_derivation_routes_a_file_through_the_declared_rules`
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_over_the_shipped_taxonomy_says_the_vocal_dimension_was_not_compared`
  - `tests/test_routing_workers.py::test_an_uncalibrated_export_creates_no_vocal_sub_and_names_the_gap`
  - `tests/test_routing_workers.py::test_an_uncalibrated_inbox_warns_and_files_nothing_under_with_vox`
  - `tests/test_routing_workers.py::test_the_database_inbox_gate_shows_each_files_destination`
  - `tests/test_routing_workers.py::test_the_export_gate_names_the_vocal_dimension_it_did_not_read`
  - `tests/test_routing_workers.py::test_the_gap_rule_is_the_derivations_own`

Old text:

```
    gaps = not_derived(declared, vocal_threshold=vocal_threshold)
```

New text:

```
    gaps = ()
```

### `r316.M9_not_derived_ignores_threshold`

not_derived names the vocal gap even when a threshold was handed in and the dimension was derived

- File: `src/cratekit/write/rebuild.py`
- Source: `r316.json`, row `M9_not_derived_ignores_threshold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`, `tests/test_rebuild.py`
- Collected: 309 against a baseline of 309
- Kills: 14 (killed)
- Killed:
  - `tests/test_rebuild.py::test_a_vocal_playlist_nothing_compared_is_not_named_as_left_behind`
  - `tests/test_rebuild.py::test_a_vocal_track_lands_in_its_energy_sub_AND_the_additive_one`
  - `tests/test_routing_workers.py::test_a_calibrated_export_files_over_the_cut_and_not_under_it`
  - `tests/test_routing_workers.py::test_a_calibrated_inbox_files_a_track_over_the_cut_under_with_vox[above]`
  - `tests/test_routing_workers.py::test_a_calibrated_inbox_files_a_track_over_the_cut_under_with_vox[below]`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[above-rebuild]`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[above-resort]`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[below-rebuild]`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[below-resort]`
  - `tests/test_routing_workers.py::test_converge_compares_the_vocal_sub_once_calibrated`
  - `tests/test_routing_workers.py::test_the_database_apply_files_the_track_where_the_gate_said`
  - `tests/test_routing_workers.py::test_the_export_gate_prints_the_plan_in_the_default_mode`
  - `tests/test_routing_workers.py::test_the_export_gate_shows_every_item_the_digest_was_taken_over`
  - `tests/test_routing_workers.py::test_the_gap_rule_is_the_derivations_own`

Old text:

```
    return (VOCAL_DIMENSION,) if additive and vocal_threshold is None else ()
```

New text:

```
    return (VOCAL_DIMENSION,) if additive else ()
```

### `u119.R1_vox_unknown_by_id`

derive_from_taxonomy: a playlist class is asked of the vocal derivation and refused

- File: `src/cratekit/write/rebuild.py`
- Source: `u119.json`, row `R1_vox_unknown_by_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild.py`, `tests/test_genre_favorites.py`
- Collected: 158 against a baseline of 158
- Kills: 40 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_the_rebuild_files_a_favourite_into_the_folder_it_moves_it_to`
  - `tests/test_genre_favorites.py::test_the_rebuild_puts_a_first_favorites_under_a_renamed_folder_its_record_binds`
  - `tests/test_rebuild.py::test_a_destination_that_lost_every_track_is_still_compared`
  - `tests/test_rebuild.py::test_a_destination_with_no_recorded_node_falls_back_to_the_declared_name`
  - `tests/test_rebuild.py::test_a_genre_sub_is_created_once_beside_the_band_and_a_second_rebuild_plans_nothing`
  - `tests/test_rebuild.py::test_a_governed_write_records_the_fingerprint_at_its_close`
  - `tests/test_rebuild.py::test_a_library_with_no_vocal_calibration_reports_what_it_did_not_compare`
  - `tests/test_rebuild.py::test_a_membership_pointing_at_a_soft_deleted_row_is_not_a_difference_either`
  - `tests/test_rebuild.py::test_a_rebuild_after_a_rename_converges_rather_than_doubling_the_tree`
  - `tests/test_rebuild.py::test_a_rebuild_and_its_check_beside_deadca7s_folder_leave_it_and_report_no_drift[ordinary]`
  - `tests/test_rebuild.py::test_a_rebuild_and_its_check_beside_deadca7s_folder_leave_it_and_report_no_drift[zero-date-west-of-utc]`
  - `tests/test_rebuild.py::test_a_rebuild_is_not_refused_by_the_flag_it_exists_to_clear`
  - `tests/test_rebuild.py::test_a_rebuild_never_removes_a_membership_the_declaration_does_not_place`
  - `tests/test_rebuild.py::test_a_rebuild_refuses_on_a_volume_whose_identity_does_not_match`
  - `tests/test_rebuild.py::test_a_rebuild_refuses_while_the_lock_is_held_elsewhere`
  - ... and 25 more, see the JSON sidecar

Old text:

```
        if entry.additive and entry.signal == taxonomy.SIGNAL_VOX
    )
    unknown = sorted(
```

New text:

```
        if entry.additive
    )
    unknown = sorted(
```

### `u219.A1_approved_equality`

assert_as_approved: return whatever the before check would add, so a library that moved after the gate is written

- File: `src/cratekit/write/rebuild.py`
- Source: `u219.json`, row `A1_approved_equality`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_jazz_folder.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_rebuild.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 732 against a baseline of 732
- Kills: 2 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_library_that_moved_after_the_gate_refuses_before_writing[the library moved]`
  - `tests/test_resort_scope.py::test_a_library_that_moved_after_the_gate_refuses_before_writing[two files swapped]`

Old text:

```
    if planned == wanted:
        return
```

New text:

```
    if True:
        return
```

### `u219.A2_approved_checked`

rebuild_tree: skip the approved check, so the worker never compares its adds with the frozen plan

- File: `src/cratekit/write/rebuild.py`
- Source: `u219.json`, row `A2_approved_checked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_jazz_folder.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_rebuild.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 732 against a baseline of 732
- Kills: 2 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_library_that_moved_after_the_gate_refuses_before_writing[the library moved]`
  - `tests/test_resort_scope.py::test_a_library_that_moved_after_the_gate_refuses_before_writing[two files swapped]`

Old text:

```
    if approved is not None:
        assert_as_approved(before, approved)
```

New text:

```
(empty)
```

### `u219.A3_approved_passed_down`

rebuild_governed_tree: hand the engine no approved plan, so a resort runs as a rebuild

- File: `src/cratekit/write/rebuild.py`
- Source: `u219.json`, row `A3_approved_passed_down`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_jazz_folder.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_rebuild.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 732 against a baseline of 732
- Kills: 5 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_library_that_moved_after_the_gate_refuses_before_writing[the library moved]`
  - `tests/test_resort_scope.py::test_a_library_that_moved_after_the_gate_refuses_before_writing[two files swapped]`
  - `tests/test_resort_scope.py::test_a_resort_that_left_a_favourite_for_later_says_so`
  - `tests/test_resort_scope.py::test_a_resort_writes_no_favourite_its_gate_did_not_show`
  - `tests/test_resort_scope.py::test_the_favourite_a_resort_left_is_shown_and_filed_by_the_next`

Old text:

```
            workflow=workflow,
            approved=approved,
        )
```

New text:

```
            workflow=workflow,
            approved=None,
        )
```

### `u219.A4_additions_rows`

additions: report nothing missing, so the gate shows no add and the resort queues nothing

- File: `src/cratekit/write/rebuild.py`
- Source: `u219.json`, row `A4_additions_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_jazz_folder.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_rebuild.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 732 against a baseline of 732
- Kills: 21 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_library_that_moved_after_the_gate_refuses_before_writing[the library moved]`
  - `tests/test_resort_scope.py::test_a_library_that_moved_after_the_gate_refuses_before_writing[two files swapped]`
  - `tests/test_resort_scope.py::test_a_resort_after_a_genre_sub_writes_nothing_under_the_intake_root`
  - `tests/test_resort_scope.py::test_a_resort_that_left_a_favourite_for_later_says_so`
  - `tests/test_resort_scope.py::test_the_favourite_a_resort_left_is_shown_and_filed_by_the_next`
  - `tests/test_resort_scope.py::test_the_gate_shows_every_add_and_only_the_routing_trees`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[above-resort]`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[below-resort]`
  - `tests/test_routing_workers.py::test_a_corrupt_calibration_refuses_the_resume_before_any_item_runs[resort]`
  - `tests/test_routing_workers.py::test_a_driven_resume_over_no_favorites_class_names_the_skipped_step[resort]`
  - `tests/test_routing_workers.py::test_a_driven_resume_says_the_vocal_dimension_was_not_compared_beside_drift[resort]`
  - `tests/test_routing_workers.py::test_a_queued_job_runs_its_item_and_the_tree_holds_the_track[resort-encrypted]`
  - `tests/test_routing_workers.py::test_a_queued_job_runs_its_item_and_the_tree_holds_the_track[resort-native]`
  - `tests/test_routing_workers.py::test_a_resort_names_the_membership_it_left_where_it_was`
  - `tests/test_routing_workers.py::test_a_resort_resume_that_drove_nothing_names_no_leftover`
  - ... and 6 more, see the JSON sidecar

Old text:

```
        for entry in report.missing
    ]
```

New text:

```
        for entry in report.missing[:0]
    ]
```

### `u219.D1_derivable_guard`

assert_derivable: return for every tree, so the intake tree is derived from the taxonomy again (R-789, sitting 61)

- File: `src/cratekit/write/rebuild.py`
- Source: `u219.json`, row `D1_derivable_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_jazz_folder.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_rebuild.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 732 against a baseline of 732
- Kills: 3 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_rebuild_naming_the_intake_tree_refuses_and_queues_nothing`
  - `tests/test_resort_scope.py::test_converge_reads_the_intake_tree_as_not_compared`
  - `tests/test_resort_scope.py::test_the_derivation_refuses_the_intake_tree_before_reading_a_file`

Old text:

```
    others = other_declared_trees(declared)
    if tree_id not in others:
        return
    raise refuse(
        "rebuild-tree-not-derivable",
```

New text:

```
    others = other_declared_trees(declared)
    if True:
        return
    raise refuse(
        "rebuild-tree-not-derivable",
```

### `u219.D2_derivation_asks`

declared_membership: drop its call of assert_derivable, so the derivation takes the source alone as it did

- File: `src/cratekit/write/rebuild.py`
- Source: `u219.json`, row `D2_derivation_asks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_jazz_folder.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_rebuild.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 732 against a baseline of 732
- Kills: 2 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_converge_reads_the_intake_tree_as_not_compared`
  - `tests/test_resort_scope.py::test_the_derivation_refuses_the_intake_tree_before_reading_a_file`

Old text:

```
    assert_derivable(declared, tree_id)
    derive = None if source is None else DERIVATIONS.get(source)
```

New text:

```
    derive = None if source is None else DERIVATIONS.get(source)
```

### `u219.D4_derivable_answer`

derivable: answer True for every tree, so every sweep files the intake tree again

- File: `src/cratekit/write/rebuild.py`
- Source: `u219.json`, row `D4_derivable_answer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_jazz_folder.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_rebuild.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 732 against a baseline of 732
- Kills: 19 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_library_that_moved_after_the_gate_refuses_before_writing[the library moved]`
  - `tests/test_resort_scope.py::test_a_library_that_moved_after_the_gate_refuses_before_writing[two files swapped]`
  - `tests/test_resort_scope.py::test_a_rebuild_naming_the_intake_tree_refuses_and_queues_nothing`
  - `tests/test_resort_scope.py::test_a_rebuild_of_every_tree_leaves_the_intake_tree_alone`
  - `tests/test_resort_scope.py::test_a_resort_after_a_genre_sub_writes_nothing_under_the_intake_root`
  - `tests/test_resort_scope.py::test_a_resort_that_left_a_favourite_for_later_says_so`
  - `tests/test_resort_scope.py::test_a_resort_with_no_change_plans_nothing_and_queues_nothing`
  - `tests/test_resort_scope.py::test_a_resort_writes_no_favourite_its_gate_did_not_show`
  - `tests/test_resort_scope.py::test_a_restore_marked_inbox_is_accepted_by_a_named_person`
  - `tests/test_resort_scope.py::test_a_second_restore_clears_the_acceptance_of_the_first`
  - `tests/test_resort_scope.py::test_an_abort_queues_nothing_and_writes_nothing`
  - `tests/test_resort_scope.py::test_an_aborted_acceptance_leaves_the_inbox_refusing`
  - `tests/test_resort_scope.py::test_an_answer_over_one_database_file_does_not_approve_another`
  - `tests/test_resort_scope.py::test_every_declared_place_but_the_routing_tree_is_not_derivable`
  - `tests/test_resort_scope.py::test_route_inbox_files_into_the_routing_tree_only`
  - ... and 4 more, see the JSON sidecar

Old text:

```
    return tree_id not in other_declared_trees(declared)
```

New text:

```
    return True
```

### `u219.F1_favourites_held`

rebuild_tree: the second pass writes every favourite again, shown or not (round one's first hold)

- File: `src/cratekit/write/rebuild.py`
- Source: `u219.json`, row `F1_favourites_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_jazz_folder.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_rebuild.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 732 against a baseline of 732
- Kills: 3 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_resort_that_left_a_favourite_for_later_says_so`
  - `tests/test_resort_scope.py::test_a_resort_writes_no_favourite_its_gate_did_not_show`
  - `tests/test_resort_scope.py::test_the_favourite_a_resort_left_is_shown_and_filed_by_the_next`

Old text:

```
        favorites = tuple(
            entry for entry in favorites if (entry.location, entry.bucket, entry.sub) in shown
        )
```

New text:

```
(empty)
```

### `u219.K1_accept_routing_refused`

accept_as_it_stands: accept the routing tree too, so a disposition can stand in for its rebuild

- File: `src/cratekit/write/rebuild.py`
- Source: `u219.json`, row `K1_accept_routing_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_jazz_folder.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_rebuild.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 732 against a baseline of 732
- Kills: 1 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_the_engine_never_accepts_a_tree_a_rebuild_can_repair`

Old text:

```
    if derivable(declared, tree_id):
        # No surface asks this for a routing tree; one that did is a defect.
```

New text:

```
    if False:
        # No surface asks this for a routing tree; one that did is a defect.
```

### `u219.M1_accept_fingerprint`

accept_as_it_stands: record no fingerprint, so an accepted INBOX still meets the restore latch (round two's first hold)

- File: `src/cratekit/write/rebuild.py`
- Source: `u219.json`, row `M1_accept_fingerprint`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_jazz_folder.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_rebuild.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 732 against a baseline of 732
- Kills: 2 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_restore_marked_inbox_is_accepted_by_a_named_person`
  - `tests/test_resort_scope.py::test_a_second_restore_clears_the_acceptance_of_the_first`

Old text:

```
        convergence.record_fingerprint(cfg, handle)
    finally:
        rb_writer.close_db(handle)


def declared_membership(
```

New text:

```
    finally:
        rb_writer.close_db(handle)


def declared_membership(
```

### `u246.R1_rebuild_set_per_placement`

rebuild_tree: put the set back inside the comprehension, one set of the derived placements built per placement (the shape on main)

- File: `src/cratekit/write/rebuild.py`
- Source: `u246.json`, row `R1_rebuild_set_per_placement`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild_growth.py`, `tests/test_comprehension_sets.py`, `tests/test_rebuild.py`, `tests/test_genre_favorites.py`, `tests/test_resort_scope.py`
- Collected: 216 against a baseline of 216
- Kills: 2 (killed)
- Killed:
  - `tests/test_comprehension_sets.py::test_no_comprehension_in_the_package_rebuilds_an_invariant_set_per_element`
  - `tests/test_rebuild_growth.py::test_a_rebuilds_placement_comparisons_double_when_its_favourites_double`

Old text:

```
    favorites = tuple(entry for entry in placements if entry not in first_pass)
```

New text:

```
    favorites = tuple(entry for entry in placements if entry not in set(derived))
```

### `u246.R2_rebuild_tuple_scan`

rebuild_tree: test each placement against the derived tuple itself, a linear scan per placement, quadratic by equality and not by hashing

- File: `src/cratekit/write/rebuild.py`
- Source: `u246.json`, row `R2_rebuild_tuple_scan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild_growth.py`, `tests/test_comprehension_sets.py`, `tests/test_rebuild.py`, `tests/test_genre_favorites.py`, `tests/test_resort_scope.py`
- Collected: 216 against a baseline of 216
- Kills: 1 (killed)
- Killed:
  - `tests/test_rebuild_growth.py::test_a_rebuilds_placement_comparisons_double_when_its_favourites_double`

Old text:

```
    favorites = tuple(entry for entry in placements if entry not in first_pass)
```

New text:

```
    favorites = tuple(entry for entry in placements if entry not in derived)
```

### `u246.R3_rebuild_set_of_placements`

rebuild_tree: build the set from every placement rather than the derived ones, so the second pass files no favourite

- File: `src/cratekit/write/rebuild.py`
- Source: `u246.json`, row `R3_rebuild_set_of_placements`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild_growth.py`, `tests/test_rebuild.py`, `tests/test_genre_favorites.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 380 against a baseline of 380
- Kills: 5 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_the_rebuild_files_a_favourite_into_the_folder_it_moves_it_to`
  - `tests/test_genre_favorites.py::test_the_rebuild_puts_a_first_favorites_under_a_renamed_folder_its_record_binds`
  - `tests/test_rebuild_growth.py::test_a_rebuilds_placement_comparisons_double_when_its_favourites_double`
  - `tests/test_resort_scope.py::test_a_resort_that_left_a_favourite_for_later_says_so`
  - `tests/test_resort_scope.py::test_the_favourite_a_resort_left_is_shown_and_filed_by_the_next`

Old text:

```
    first_pass = set(derived)
```

New text:

```
    first_pass = set(placements)
```

### `u246.R4_rebuild_membership_inverted`

rebuild_tree: keep the placements present in the derived set, so the second pass refiles the first pass's placements and no favourite

- File: `src/cratekit/write/rebuild.py`
- Source: `u246.json`, row `R4_rebuild_membership_inverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild_growth.py`, `tests/test_rebuild.py`, `tests/test_genre_favorites.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 380 against a baseline of 380
- Kills: 7 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_the_rebuild_files_a_favourite_into_the_folder_it_moves_it_to`
  - `tests/test_genre_favorites.py::test_the_rebuild_puts_a_first_favorites_under_a_renamed_folder_its_record_binds`
  - `tests/test_rebuild.py::test_a_second_rebuild_writes_nothing`
  - `tests/test_rebuild.py::test_the_rebuild_declares_a_recovery_intent_so_the_restore_latch_lets_it_past`
  - `tests/test_rebuild_growth.py::test_a_rebuilds_placement_comparisons_double_when_its_favourites_double`
  - `tests/test_resort_scope.py::test_a_resort_that_left_a_favourite_for_later_says_so`
  - `tests/test_resort_scope.py::test_the_favourite_a_resort_left_is_shown_and_filed_by_the_next`

Old text:

```
    favorites = tuple(entry for entry in placements if entry not in first_pass)
```

New text:

```
    favorites = tuple(entry for entry in placements if entry in first_pass)
```

### `u246.R5_rebuild_set_empty`

rebuild_tree: an empty set, so every placement, the first pass's included, is filed again as a favourite

- File: `src/cratekit/write/rebuild.py`
- Source: `u246.json`, row `R5_rebuild_set_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild_growth.py`, `tests/test_rebuild.py`, `tests/test_genre_favorites.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 380 against a baseline of 380
- Kills: 2 (killed)
- Killed:
  - `tests/test_rebuild.py::test_a_second_rebuild_writes_nothing`
  - `tests/test_rebuild.py::test_the_rebuild_declares_a_recovery_intent_so_the_restore_latch_lets_it_past`

Old text:

```
    first_pass = set(derived)
```

New text:

```
    first_pass = set()
```

### `u250.M2_genre_dropped`

read_truth: read no genre, so every file routes to the fallback bucket

- File: `src/cratekit/write/rebuild.py`
- Source: `u250.json`, row `M2_genre_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild_one_open.py`, `tests/test_rebuild.py`, `tests/test_tags.py`
- Collected: 215 against a baseline of 215
- Kills: 39 (killed)
- Killed:
  - `tests/test_rebuild_one_open.py::test_a_derivation_over_n_files_makes_n_opens`
  - `tests/test_rebuild_one_open.py::test_a_numeric_reading_converts_the_way_the_single_readers_convert`
  - `tests/test_rebuild_one_open.py::test_an_undecodable_field_reads_none_and_its_neighbours_still_read`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[decimal-.aiff]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[decimal-.flac]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[decimal-.m4a]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[decimal-.mp3]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[decimal-.ogg]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[decimal-.wav]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[energy-word-.aiff]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[energy-word-.flac]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[energy-word-.m4a]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[energy-word-.mp3]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[energy-word-.ogg]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[energy-word-.wav]`
  - ... and 24 more, see the JSON sidecar

Old text:

```
        genre=values["genre"],
```

New text:

```
        genre=None,
```

### `u250.M3_energy_unconverted`

read_truth: hand the energy on as text, skipping the whole number conversion

- File: `src/cratekit/write/rebuild.py`
- Source: `u250.json`, row `M3_energy_unconverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild_one_open.py`, `tests/test_rebuild.py`, `tests/test_tags.py`
- Collected: 215 against a baseline of 215
- Kills: 32 (killed)
- Killed:
  - `tests/test_rebuild_one_open.py::test_a_derivation_over_n_files_makes_n_opens`
  - `tests/test_rebuild_one_open.py::test_a_numeric_reading_converts_the_way_the_single_readers_convert`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[decimal-.aiff]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[decimal-.flac]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[decimal-.m4a]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[decimal-.mp3]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[decimal-.ogg]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[decimal-.wav]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[energy-word-.aiff]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[energy-word-.flac]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[energy-word-.m4a]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[energy-word-.mp3]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[energy-word-.ogg]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[energy-word-.wav]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[numeric-.aiff]`
  - ... and 17 more, see the JSON sidecar

Old text:

```
        energy=tags.whole_number(values["energylevel"], field="energylevel", path=path),
```

New text:

```
        energy=values["energylevel"],
```

### `u250.M4_vox_reads_energy`

read_truth: read the vocal level from the energy field, a crossed key

- File: `src/cratekit/write/rebuild.py`
- Source: `u250.json`, row `M4_vox_reads_energy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild_one_open.py`, `tests/test_rebuild.py`, `tests/test_tags.py`
- Collected: 215 against a baseline of 215
- Kills: 27 (killed)
- Killed:
  - `tests/test_rebuild_one_open.py::test_a_derivation_over_n_files_makes_n_opens`
  - `tests/test_rebuild_one_open.py::test_a_numeric_reading_converts_the_way_the_single_readers_convert`
  - `tests/test_rebuild_one_open.py::test_an_undecodable_field_reads_none_and_its_neighbours_still_read`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[energy-word-.aiff]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[energy-word-.flac]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[energy-word-.m4a]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[energy-word-.mp3]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[energy-word-.ogg]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[energy-word-.wav]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[numeric-.aiff]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[numeric-.flac]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[numeric-.m4a]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[numeric-.mp3]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[numeric-.ogg]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[numeric-.wav]`
  - ... and 12 more, see the JSON sidecar

Old text:

```
        voxlevel=tags.whole_number(values["voxlevel"], field="voxlevel", path=path),
```

New text:

```
        voxlevel=tags.whole_number(values["energylevel"], field="voxlevel", path=path),
```

### `u302.W12_resort_writes_favourites_its_gate_never_showed`

_favorites_to_file: a resort files favourites derived only from the tree it just wrote

- File: `src/cratekit/write/rebuild.py`
- Source: `u302.json`, row `W12_resort_writes_favourites_its_gate_never_showed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_resort_scope.py`, `tests/test_rebuild_growth.py`, `tests/test_genre_favorites.py`, `tests/test_rebuild.py`
- Collected: 183 against a baseline of 183
- Kills: 3 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_resort_that_left_a_favourite_for_later_says_so`
  - `tests/test_resort_scope.py::test_a_resort_writes_no_favourite_its_gate_did_not_show`
  - `tests/test_resort_scope.py::test_the_favourite_a_resort_left_is_shown_and_filed_by_the_next`

Old text:

```
            entry for entry in favorites if (entry.location, entry.bucket, entry.sub) in shown
```

New text:

```
            entry for entry in favorites
```

### `u302.W13_unconverged_tree_cleared`

_clear_on_evidence: the flag is cleared though the after check still differs

- File: `src/cratekit/write/rebuild.py`
- Source: `u302.json`, row `W13_unconverged_tree_cleared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild.py`, `tests/test_resort_scope.py`, `tests/test_genre_favorites.py`
- Collected: 182 against a baseline of 182
- Kills: 7 (killed)
- Killed:
  - `tests/test_rebuild.py::test_a_destination_that_lost_every_track_is_still_compared`
  - `tests/test_rebuild.py::test_a_rebuild_never_removes_a_membership_the_declaration_does_not_place`
  - `tests/test_rebuild.py::test_a_track_held_twice_in_one_playlist_is_a_difference_the_flag_stays_shut_on`
  - `tests/test_rebuild.py::test_a_vocal_playlist_nothing_compared_is_not_named_as_left_behind`
  - `tests/test_resort_scope.py::test_a_resort_that_left_a_favourite_for_later_says_so`
  - `tests/test_resort_scope.py::test_a_resort_writes_no_favourite_its_gate_did_not_show`
  - `tests/test_resort_scope.py::test_the_favourite_a_resort_left_is_shown_and_filed_by_the_next`

Old text:

```
    if not after.converged:
        logger.warning(
```

New text:

```
    if False:
        logger.warning(
```

### `u340.R05_derive_one_bucket`

filed_genres: answer the genre's bucket alone, so rebuild, converge and resort never file the second folder

- File: `src/cratekit/write/rebuild.py`
- Source: `u340.json`, row `R05_derive_one_bucket`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_rebuild.py`, `tests/test_organize_mirror_edits_u340.py`
- Collected: 173 against a baseline of 173
- Kills: 11 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u340.py::test_a_band_move_in_one_folder_moves_the_energy_in_both_and_keeps_the_second_genre`
  - `tests/test_second_genre.py::test_a_cleared_second_genre_alone_in_its_folder_is_named_by_the_check`
  - `tests/test_second_genre.py::test_a_cleared_second_genre_leaves_its_genre_sub_named_as_well`
  - `tests/test_second_genre.py::test_a_cleared_second_genre_under_a_folder_renamed_in_rekordbox_is_named`
  - `tests/test_second_genre.py::test_a_recorded_folder_renamed_to_another_genres_name_is_read_by_that_name`
  - `tests/test_second_genre.py::test_a_soul_tracks_cleared_rnb_alone_in_the_rnb_band_is_named_too`
  - `tests/test_second_genre.py::test_a_vocal_track_takes_with_vox_in_both_folders`
  - `tests/test_second_genre.py::test_an_energy_change_moves_the_band_in_both_folders`
  - `tests/test_second_genre.py::test_rebuild_files_both_and_a_cleared_second_genre_reads_as_that_folder_alone`
  - `tests/test_second_genre.py::test_the_converge_verb_says_differing_over_a_cleared_second_genre`
  - `tests/test_second_genre.py::test_the_derivation_places_a_track_in_both_folders_in_the_same_band`

Old text:

```
    return ((first, entry.genre), (second, entry.second_genre))
```

New text:

```
    return ((first, entry.genre),)
```

### `u340.R06_truth_unread`

read_truth: drop the second genre reading, so a file's second genre never reaches the derivation

- File: `src/cratekit/write/rebuild.py`
- Source: `u340.json`, row `R06_truth_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_rebuild.py`, `tests/test_organize_mirror_edits_u340.py`
- Collected: 173 against a baseline of 173
- Kills: 4 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u340.py::test_a_band_move_in_one_folder_moves_the_energy_in_both_and_keeps_the_second_genre`
  - `tests/test_organize_mirror_edits_u340.py::test_a_move_that_would_wake_a_second_genre_naming_its_own_folder_is_not_taken`
  - `tests/test_organize_mirror_edits_u340.py::test_taking_it_off_one_folder_alone_is_listed_and_not_taken`
  - `tests/test_second_genre.py::test_the_truth_reads_the_second_genre_in_the_same_open`

Old text:

```
        second_genre=values["secondgenre"],
```

New text:

```
        second_genre=None,
```

### `u219-composites.G6_answer_pinned`

_resort_pin: pin the answer to no database file, so an answer over a copy satisfies the live run

- File: `src/cratekit/write/routing_cli.py`
- Source: `u219-composites.json`, row `G6_answer_pinned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 221 against a baseline of 221
- Kills: 1 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_an_answer_over_one_database_file_does_not_approve_another`

Old text:

```
    return {RESORT_DATABASE_KEY: str(opened)} if opened else None
```

New text:

```
    return None
```

### `u219.G1_resort_abort`

route resort: an abort at the gate queues the resort anyway

- File: `src/cratekit/write/routing_cli.py`
- Source: `u219.json`, row `G1_resort_abort`
- Moved: Same gate answer in route_resort; U298 replaced the local _no_op with cli.output.no_job
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_organize_mirror_edits.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 297 against a baseline of 297
- Kills: 1 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_an_abort_queues_nothing_and_writes_nothing`

Old text:

```
    if option != "apply":
        return ctx.envelope(data=no_job("declined"), outcome=Outcome.NO_OP, warnings=warnings)
```

New text:

```
    if option == "never":
        return ctx.envelope(data=no_job("declined"), outcome=Outcome.NO_OP, warnings=warnings)
```

### `u219.G2_nothing_to_add`

route resort: queue a job over a plan with nothing to add

- File: `src/cratekit/write/routing_cli.py`
- Source: `u219.json`, row `G2_nothing_to_add`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_organize_mirror_edits.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 297 against a baseline of 297
- Kills: 1 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_resort_with_no_change_plans_nothing_and_queues_nothing`

Old text:

```
    if not adds:
        return ctx.envelope(
```

New text:

```
    if False:
        return ctx.envelope(
```

### `u219.G3_adds_frozen`

route resort: freeze an empty plan in the job, so the worker holds its write to nothing the gate showed

- File: `src/cratekit/write/routing_cli.py`
- Source: `u219.json`, row `G3_adds_frozen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_organize_mirror_edits.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 297 against a baseline of 297
- Kills: 21 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_library_that_moved_after_the_gate_refuses_before_writing[the library moved]`
  - `tests/test_resort_scope.py::test_a_library_that_moved_after_the_gate_refuses_before_writing[two files swapped]`
  - `tests/test_resort_scope.py::test_a_resort_after_a_genre_sub_writes_nothing_under_the_intake_root`
  - `tests/test_resort_scope.py::test_a_resort_that_left_a_favourite_for_later_says_so`
  - `tests/test_resort_scope.py::test_a_resort_with_no_change_plans_nothing_and_queues_nothing`
  - `tests/test_resort_scope.py::test_a_resort_writes_no_favourite_its_gate_did_not_show`
  - `tests/test_resort_scope.py::test_the_favourite_a_resort_left_is_shown_and_filed_by_the_next`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[above-resort]`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[below-resort]`
  - `tests/test_routing_workers.py::test_a_driven_resume_over_no_favorites_class_names_the_skipped_step[resort]`
  - `tests/test_routing_workers.py::test_a_driven_resume_over_the_declared_class_says_nothing_of_it[resort]`
  - `tests/test_routing_workers.py::test_a_driven_resume_says_the_vocal_dimension_was_not_compared_beside_drift[resort]`
  - `tests/test_routing_workers.py::test_a_queued_job_runs_its_item_and_the_tree_holds_the_track[resort-encrypted]`
  - `tests/test_routing_workers.py::test_a_queued_job_runs_its_item_and_the_tree_holds_the_track[resort-native]`
  - `tests/test_routing_workers.py::test_a_rebuild_of_another_tree_says_nothing_of_the_routing_trees_favorites[resort]`
  - ... and 6 more, see the JSON sidecar

Old text:

```
                RESORT_ADDS_KEY: adds,
```

New text:

```
                RESORT_ADDS_KEY: [],
```

### `u219.G5_resume_run`

resort_argv: drop --run, so the spawned child meets the explicit gate with nothing recorded

- File: `src/cratekit/write/routing_cli.py`
- Source: `u219.json`, row `G5_resume_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_organize_mirror_edits.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 297 against a baseline of 297
- Kills: 1 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_the_resume_argv_names_the_gate_run`

Old text:

```
    resume = ["--run", str(gate_run)] if gate_run else []
    return [*resume, "route", "resort", "--job", job.job_id]
```

New text:

```
    resume = []
    return [*resume, "route", "resort", "--job", job.job_id]
```

### `u219.M3_due_again_said`

_due_again_warnings: count nothing due, so a resort that left a favourite for later reports a clean success (round two's third hold)

- File: `src/cratekit/write/routing_cli.py`
- Source: `u219.json`, row `M3_due_again_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_organize_mirror_edits.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 297 against a baseline of 297
- Kills: 1 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_resort_that_left_a_favourite_for_later_says_so`

Old text:

```
        count = int(report.get("due_again") or 0)
```

New text:

```
        count = 0
```

### `u219.R1_routed_trees`

_routed_trees: every native tree, so the resort queues the intake tree again

- File: `src/cratekit/write/routing_cli.py`
- Source: `u219.json`, row `R1_routed_trees`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_organize_mirror_edits.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 297 against a baseline of 297
- Kills: 12 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_library_that_moved_after_the_gate_refuses_before_writing[the library moved]`
  - `tests/test_resort_scope.py::test_a_library_that_moved_after_the_gate_refuses_before_writing[two files swapped]`
  - `tests/test_resort_scope.py::test_a_resort_after_a_genre_sub_writes_nothing_under_the_intake_root`
  - `tests/test_resort_scope.py::test_a_resort_that_left_a_favourite_for_later_says_so`
  - `tests/test_resort_scope.py::test_a_resort_with_no_change_plans_nothing_and_queues_nothing`
  - `tests/test_resort_scope.py::test_a_resort_writes_no_favourite_its_gate_did_not_show`
  - `tests/test_resort_scope.py::test_an_abort_queues_nothing_and_writes_nothing`
  - `tests/test_resort_scope.py::test_an_answer_over_one_database_file_does_not_approve_another`
  - `tests/test_resort_scope.py::test_route_inbox_files_into_the_routing_tree_only`
  - `tests/test_resort_scope.py::test_the_digest_is_the_same_over_one_unchanged_library`
  - `tests/test_resort_scope.py::test_the_favourite_a_resort_left_is_shown_and_filed_by_the_next`
  - `tests/test_resort_scope.py::test_the_gate_shows_every_add_and_only_the_routing_trees`

Old text:

```
    return tuple(t for t in _native_trees(entries) if rebuild.derivable(declared, t))
```

New text:

```
    return _native_trees(entries)
```

### `u219.R2_inbox_routed_only`

plan_inbox: file the intake folder into every native tree, INBOX included

- File: `src/cratekit/write/routing_cli.py`
- Source: `u219.json`, row `R2_inbox_routed_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_organize_mirror_edits.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 297 against a baseline of 297
- Kills: 1 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_route_inbox_files_into_the_routing_tree_only`

Old text:

```
    native = _routed_trees(entries, declared)
```

New text:

```
    native = _native_trees(entries)
```

### `u219.R3_left_alone_named`

_passed_over: name no tree the resort left alone

- File: `src/cratekit/write/routing_cli.py`
- Source: `u219.json`, row `R3_left_alone_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_organize_mirror_edits.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 297 against a baseline of 297
- Kills: 1 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_the_gate_shows_every_add_and_only_the_routing_trees`

Old text:

```
    skipped = [t for t in _native_trees(entries) if t in others]
    if not skipped:
        return []
    named = ", ".join(f"{others[t]} ({t})" for t in skipped)
    return [
        {
            "code": TREE_NOT_DERIVED,
```

New text:

```
    skipped = [t for t in _native_trees(entries) if t in others]
    if skipped:
        return []
    named = ", ".join(f"{others[t]} ({t})" for t in skipped)
    return [
        {
            "code": TREE_NOT_DERIVED,
```

### `r239-b.S2_unplaced_key_off`

route unplaced's open, unplaced_items, passes unlock=False again

- File: `src/cratekit/write/routing_export.py`
- Source: `r239-b.json`, row `S2_unplaced_key_off`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_adopt_apply_cli.py`
- Collected: 724 against a baseline of 724
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_no_caller_in_src_answers_the_key_question_for_itself`
  - `tests/test_routing_workers.py::test_unplaced_reports_the_rows_no_governed_tree_holds[encrypted]`

Old text:

```
        return [], {"compared": False, "reason": "no-native-tree", "collection": 0}
    handle = rb_writer.open_db(cfg=cfg)

```

New text:

```
        return [], {"compared": False, "reason": "no-native-tree", "collection": 0}
    handle = rb_writer.open_db(cfg=cfg, unlock=False)

```

### `u155.W2_destination`

destination: resolve no genre sub, so its playlist has no name

- File: `src/cratekit/write/routing_pass.py`
- Source: `u155.json`, row `W2_destination`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_jazz_folder.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_deferred_routing.py`, `tests/test_genre_sub.py`, `tests/test_intake_imported.py`, `tests/test_intake_land_filing.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 817 against a baseline of 817
- Kills: 63 (killed)
- Killed:
  - `tests/test_adopt_former_place.py::test_a_library_whose_own_taxonomy_still_has_the_sub_moves_no_track_of_that_sub`
  - `tests/test_adopt_former_place.py::test_a_renamed_old_playlist_is_found_through_the_node_recorded_under_the_old_sub`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_holds_the_former_place_in_both_buckets`
  - `tests/test_adopt_former_place.py::test_an_approved_move_files_each_track_in_its_band_and_a_second_plans_nothing`
  - `tests/test_adopt_former_place.py::test_the_gate_shows_every_track_leaving_the_old_playlist_and_every_one_left`
  - `tests/test_adopt_jazz_folder.py::test_a_track_in_the_old_jazz_playlist_holds_its_former_place_in_both_buckets`
  - `tests/test_adopt_jazz_folder.py::test_an_approved_move_files_jazz_in_its_bands_and_keeps_every_other_membership`
  - `tests/test_adopt_jazz_folder.py::test_the_gate_shows_every_jazz_track_moving_and_no_other_track`
  - `tests/test_adopt_move.py::test_a_cancelled_move_exits_with_its_own_cause_and_not_ok`
  - `tests/test_adopt_move.py::test_a_failure_after_the_add_leaves_the_track_in_both_and_a_resume_finishes`
  - `tests/test_adopt_move.py::test_a_failure_in_the_additions_writes_nothing_at_all`
  - `tests/test_adopt_move.py::test_a_job_another_verb_queued_is_never_driven_through_this_gate`
  - `tests/test_adopt_move.py::test_a_parked_move_leaves_blocked_and_non_zero`
  - `tests/test_adopt_move.py::test_a_reading_that_changed_after_the_approval_is_a_stale_decision`
  - `tests/test_adopt_move.py::test_a_refusal_at_the_second_commit_keeps_its_own_cause_and_the_job_says_in_both`
  - ... and 48 more, see the JSON sidecar

Old text:

```
    for genre in bucket.genre_subs:
        if genre.id == sub_id:
            return bucket.display, genre.display
```

New text:

```
(empty)
```

### `a32.J3_bookkeeping_counted_as_moved`

The shared moved column rule counts the binding's bookkeeping columns as moved

- File: `src/cratekit/write/row_defaults.py`
- Source: `a32.json`, row `J3_bookkeeping_counted_as_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`, `tests/test_repair_rows.py`
- Collected: 113 against a baseline of 113
- Kills: 6 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_triple_already_at_its_value_is_shown_and_not_written`
  - `tests/test_repair_link.py::test_judge_accepts_values_read_back_as_the_live_tables_types`
  - `tests/test_repair_link.py::test_the_two_acts_write_each_triple_and_move_no_other_column`
  - `tests/test_repair_rows.py::test_judge_names_a_planned_column_still_null_and_a_column_that_moved`
  - `tests/test_repair_rows.py::test_past_the_bindings_range_the_gate_says_why_no_id_is_renumbered`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
    skip = set(planned) | rb_writer.BOOKKEEPING_COLUMNS
```

New text:

```
    skip = set(planned)
```

### `r923.N11_digest_drops_items`

The digest no longer covers the rows and columns the plan fills

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N11_digest_drops_items`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_the_digest_moves_when_a_planned_column_is_filled_elsewhere`
  - `tests/test_repair_rows.py::test_the_digest_moves_when_a_random_id_is_replaced_elsewhere`

Old text:

```
                "items": [item.to_json() for item in self.items],
```

New text:

```
                "items": [],
```

### `r923.N13_judge_compares_raw`

The read back compares a default by raw value, so the live table's integer reads as wrong against the binding's string

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N13_judge_compares_raw`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 3 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_judge_names_a_planned_column_still_null_and_a_column_that_moved`
  - `tests/test_repair_rows.py::test_past_the_bindings_range_the_gate_says_why_no_id_is_renumbered`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
            or str(now[column]) != str(rb_writer.CONTENT_ROW_DEFAULTS[column])
```

New text:

```
            or now[column] != rb_writer.CONTENT_ROW_DEFAULTS[column]
```

### `r923.N2_plan_lists_tombstones`

The repair plans soft deleted rows beside live ones

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N2_plan_lists_tombstones`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 13 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_file_on_another_volume_than_the_bound_is_left_and_names_why`
  - `tests/test_repair_rows.py::test_a_library_with_no_row_missing_a_default_still_asks_and_then_writes_nothing`
  - `tests/test_repair_rows.py::test_a_path_that_does_not_resolve_leaves_the_row_and_names_why`
  - `tests/test_repair_rows.py::test_a_plan_that_renumbers_nothing_registers_no_file_id_policy`
  - `tests/test_repair_rows.py::test_a_policy_registered_before_the_apply_survives_it`
  - `tests/test_repair_rows.py::test_a_random_id_on_a_row_with_every_default_is_an_item_of_its_own`
  - `tests/test_repair_rows.py::test_a_row_whose_file_is_gone_is_named_on_a_run_that_writes_nothing`
  - `tests/test_repair_rows.py::test_a_tombstone_is_never_listed_though_every_default_is_null`
  - `tests/test_repair_rows.py::test_off_apfs_nothing_is_judged_random_and_the_plan_says_which_filesystem`
  - `tests/test_repair_rows.py::test_past_the_bindings_range_nothing_is_judged_random`
  - `tests/test_repair_rows.py::test_past_the_bindings_range_the_gate_says_why_no_id_is_renumbered`
  - `tests/test_repair_rows.py::test_the_plan_lists_each_live_row_missing_a_default_with_exactly_its_null_columns`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
            f"WHERE {rb_writer.SOFT_DELETE_COLUMN} = 0"
```

New text:

```
            ""
```

### `r923.N3_plan_sees_no_null`

The repair never finds a NULL default, so it plans nothing

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N3_plan_sees_no_null`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 8 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_file_on_another_volume_than_the_bound_is_left_and_names_why`
  - `tests/test_repair_rows.py::test_a_row_changed_since_the_plan_refuses_stale_and_writes_nothing[a-planned-column-set]`
  - `tests/test_repair_rows.py::test_off_apfs_nothing_is_judged_random_and_the_plan_says_which_filesystem`
  - `tests/test_repair_rows.py::test_past_the_bindings_range_nothing_is_judged_random`
  - `tests/test_repair_rows.py::test_past_the_bindings_range_the_gate_says_why_no_id_is_renumbered`
  - `tests/test_repair_rows.py::test_the_digest_moves_when_a_planned_column_is_filled_elsewhere`
  - `tests/test_repair_rows.py::test_the_plan_lists_each_live_row_missing_a_default_with_exactly_its_null_columns`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
        missing = tuple(column for column in COLUMNS if row[column] is None)
```

New text:

```
        missing = tuple(column for column in COLUMNS if False)
```

### `r923.N4_stale_fill_accepted`

A planned column set since the plan is written over anyway

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N4_stale_fill_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_row_changed_since_the_plan_refuses_stale_and_writes_nothing[a-planned-column-set]`

Old text:

```
        if filled:
```

New text:

```
        if False:
```

### `r923.N5_stale_tombstone_accepted`

A row soft deleted since the plan is still written

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N5_stale_tombstone_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_row_changed_since_the_plan_refuses_stale_and_writes_nothing[a-row-deleted]`

Old text:

```
        if row is None or row[rb_writer.SOFT_DELETE_COLUMN] != 0:
```

New text:

```
        if row is None:
```

### `r923.N6_judge_blind_to_wrong`

The read back no longer names a planned column that did not take its default

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N6_judge_blind_to_wrong`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_judge_names_a_planned_column_still_null_and_a_column_that_moved`

Old text:

```
        if off:
```

New text:

```
        if False:
```

### `r923.N7_judge_blind_to_moved`

The read back no longer names a column outside the plan that moved

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N7_judge_blind_to_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_judge_names_a_planned_column_still_null_and_a_column_that_moved`
  - `tests/test_repair_rows.py::test_judge_reads_a_planned_renumber_as_written_and_an_unplanned_one_as_moved`

Old text:

```
        if changed:
```

New text:

```
        if False:
```

### `r923.N8_read_back_never_refuses`

assert_read_back returns whatever the read back found

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N8_read_back_never_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_assert_read_back_refuses_and_names_the_undo[a-moved-column]`
  - `tests/test_repair_rows.py::test_assert_read_back_refuses_and_names_the_undo[a-wrong-value]`

Old text:

```
    if not written.wrong and not written.moved:
        return
```

New text:

```
    if True:
        return
```

### `u115.F11_stale_file_id_not_checked`

A file id changed since the plan is written over without a staleness refusal

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F11_stale_file_id_not_checked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_row_changed_since_the_plan_refuses_stale_and_writes_nothing[a-file-id-renumbered]`

Old text:

```
        if item.renumbers and str(row.get(FILE_ID) or "").strip() != item.file_id_was:
            moved.append(f"{item.content_id}: {FILE_ID} changed since the plan")
```

New text:

```
        if False:
            moved.append(f"{item.content_id}: {FILE_ID} changed since the plan")
```

### `u115.F12_read_back_ignores_file_id`

The read back never checks that the inode took, so a renumber that did not land reads as written

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F12_read_back_ignores_file_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_judge_names_a_renumber_that_did_not_take`

Old text:

```
        if item.renumbers and str(now.get(FILE_ID) or "").strip() != str(item.file_id):
            wrong.append(f"{item.content_id}: {FILE_ID} not the file's inode")
```

New text:

```
        if False:
            wrong.append(f"{item.content_id}: {FILE_ID} not the file's inode")
```

### `u115.F13_planned_renumber_read_as_moved`

The read back forgets the file id was planned, so every renumber is reported as a column the guard let move

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F13_planned_renumber_read_as_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_judge_reads_a_planned_renumber_as_written_and_an_unplanned_one_as_moved`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
        if item.renumbers:
            planned.add(FILE_ID)
```

New text:

```
        if False:
            planned.add(FILE_ID)
```

### `u115.F14_renumber_never_written`

The apply fills the defaults and never writes the planned file id

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F14_renumber_never_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
        if item.renumbers:
            writes.append((file_owner, FILE_ID, item.file_id))
```

New text:

```
        if False:
            writes.append((file_owner, FILE_ID, item.file_id))
```

### `u115.F17_bound_is_zero`

The volume's inode bound is reported as zero rather than measured from a fresh file

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F17_bound_is_zero`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        inode=measured.st_ino, device=measured.st_dev, filesystem=filesystem_of(directory)
```

New text:

```
        inode=0, device=measured.st_dev, filesystem=filesystem_of(directory)
```

### `u115.F21_other_volume_compared`

A file on another volume than the bound is stat'ed and its inode compared, so rekordbox's rows there can be renumbered

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F21_other_volume_compared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_file_on_another_volume_than_the_bound_is_left_and_names_why`

Old text:

```
    if found.st_dev != device:
        return None, ON_ANOTHER_VOLUME
```

New text:

```
    if False:
        return None, ON_ANOTHER_VOLUME
```

### `u115.F22_off_apfs_decides`

The bound is trusted on any filesystem, so an exFAT or HFS+ library has rekordbox's rows renumbered

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F22_off_apfs_decides`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_off_apfs_nothing_is_judged_random_and_the_plan_says_which_filesystem`

Old text:

```
        if self.filesystem != APFS:
            named = self.filesystem or "unknown"
```

New text:

```
        if False:
            named = self.filesystem or "unknown"
```

### `u115.F23_loose_digits`

A signed or underscored text, or a digit from another script, is parsed as a number and judged above the bound

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F23_loose_digits`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 3 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[+200000000-within]`
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[300_000_000-within]`
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[\u0663\u0663\u0663\u0663\u0663\u0663\u0663\u0663\u0663-within]`

Old text:

```
    if not (text.isascii() and text.isdigit()):
        return WITHIN
    return ABOVE if int(text) > bound else WITHIN
```

New text:

```
    try:
        number = int(text)
    except ValueError:
        return WITHIN
    return ABOVE if number > bound else WITHIN
```

### `u115.F5_bound_boundary`

An id equal to the bound is judged above it

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F5_bound_boundary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[2000000-within0]`
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[2000000-within1]`

Old text:

```
    return ABOVE if int(text) > bound else WITHIN
```

New text:

```
    return ABOVE if int(text) >= bound else WITHIN
```

### `u115.F6_every_id_above`

Every nonzero id is judged above the bound, so stale rows rekordbox tolerates are renumbered

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F6_every_id_above`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 12 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[1-within]`
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[2000000-within0]`
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[2000000-within1]`
  - `tests/test_repair_rows.py::test_a_file_on_another_volume_than_the_bound_is_left_and_names_why`
  - `tests/test_repair_rows.py::test_a_library_with_no_row_missing_a_default_still_asks_and_then_writes_nothing`
  - `tests/test_repair_rows.py::test_a_path_that_does_not_resolve_leaves_the_row_and_names_why`
  - `tests/test_repair_rows.py::test_a_policy_registered_before_the_apply_survives_it`
  - `tests/test_repair_rows.py::test_a_random_id_on_a_row_with_every_default_is_an_item_of_its_own`
  - `tests/test_repair_rows.py::test_a_row_whose_file_is_gone_is_named_on_a_run_that_writes_nothing`
  - `tests/test_repair_rows.py::test_a_tombstone_is_never_listed_though_every_default_is_null`
  - `tests/test_repair_rows.py::test_the_plan_lists_each_live_row_missing_a_default_with_exactly_its_null_columns`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
    return ABOVE if int(text) > bound else WITHIN
```

New text:

```
    return ABOVE
```

### `u115.F7_zero_is_not_zero`

A stored 0 is no longer read as the zero form rekordbox tolerates

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F7_zero_is_not_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 4 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[0-zero0]`
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[0-zero1]`
  - `tests/test_repair_rows.py::test_off_apfs_nothing_is_judged_random_and_the_plan_says_which_filesystem`
  - `tests/test_repair_rows.py::test_the_plan_lists_each_live_row_missing_a_default_with_exactly_its_null_columns`

Old text:

```
    if text in ("", "0"):
        return ZERO
```

New text:

```
    if text == "":
        return ZERO
```

### `u115.F8_matching_inode_renumbered`

A row above the bound whose file reads the same inode is renumbered to itself rather than left

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F8_matching_inode_renumbered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            elif str(inode) == str(row[FILE_ID]).strip():
                matched += 1
```

New text:

```
            elif False:
                matched += 1
```

### `u115.F9_unreadable_file_dropped_silently`

A row above the bound whose file cannot be read is neither listed nor written, and the gate says nothing

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F9_unreadable_file_dropped_silently`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 5 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_file_on_another_volume_than_the_bound_is_left_and_names_why`
  - `tests/test_repair_rows.py::test_a_path_that_does_not_resolve_leaves_the_row_and_names_why`
  - `tests/test_repair_rows.py::test_a_row_whose_file_is_gone_is_named_on_a_run_that_writes_nothing`
  - `tests/test_repair_rows.py::test_the_plan_lists_each_live_row_missing_a_default_with_exactly_its_null_columns`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
            if inode is None:
                unrenumbered.append(
```

New text:

```
            if False:
                unrenumbered.append(
```

### `u302.W10_empty_watch_accepted`

watched_roots: a watch over no roots is accepted, so the session reports itself clean

- File: `src/cratekit/write/row_defaults.py`
- Source: `u302.json`, row `W10_empty_watch_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`, `tests/test_repair_link.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_apply_refuses_an_empty_watch_before_touching_the_database`

Old text:

```
    watched = [Path(root) for root in analysis_roots]
    if not watched:
```

New text:

```
    watched = [Path(root) for root in analysis_roots]
    if False:
```

### `r923.N14_verb_writes_on_abort`

The verb proceeds to write whatever the gate answered

- File: `src/cratekit/write/row_defaults_cli.py`
- Source: `r923.json`, row `N14_verb_writes_on_abort`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 7 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_library_with_no_row_missing_a_default_still_asks_and_then_writes_nothing`
  - `tests/test_repair_rows.py::test_a_row_whose_file_is_gone_is_named_on_a_run_that_writes_nothing`
  - `tests/test_repair_rows.py::test_an_abort_writes_nothing`
  - `tests/test_repair_rows.py::test_past_the_bindings_range_the_gate_says_why_no_id_is_renumbered`
  - `tests/test_repair_rows.py::test_rekordbox_running_refuses_at_the_apply_and_writes_nothing`
  - `tests/test_repair_rows.py::test_the_gate_takes_no_inline_answer`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
    if ctx.gate.require(spec, plan=data, context=_facts(plan)) != "apply":
```

New text:

```
    if False:
```

### `r923.N15_verb_writes_empty_plan`

An empty plan opens the database to write instead of ending as a no op

- File: `src/cratekit/write/row_defaults_cli.py`
- Source: `r923.json`, row `N15_verb_writes_empty_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_library_with_no_row_missing_a_default_still_asks_and_then_writes_nothing`
  - `tests/test_repair_rows.py::test_a_row_whose_file_is_gone_is_named_on_a_run_that_writes_nothing`

Old text:

```
    if not plan.items:
```

New text:

```
    if False:
```

### `r923.N16_ack_not_read`

The verb no longer reads the backup acknowledgment before the plan and the gate

- File: `src/cratekit/write/row_defaults_cli.py`
- Source: `r923.json`, row `N16_ack_not_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    session.assert_backup_acknowledged(cfg)

```

New text:

```
(empty)
```

### `r923.N17_write_handle_not_closed`

The write handle no longer requires rekordbox closed at open

- File: `src/cratekit/write/row_defaults_cli.py`
- Source: `r923.json`, row `N17_write_handle_not_closed`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_rekordbox_running_refuses_at_the_apply_and_writes_nothing`

Old text:

```
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
```

New text:

```
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=False, cfg=cfg)
```

### `u115.F18_undecidable_unsaid`

The gate and the envelope say nothing when the volume's counter has passed the binding's range

- File: `src/cratekit/write/row_defaults_cli.py`
- Source: `u115.json`, row `F18_undecidable_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_past_the_bindings_range_the_gate_says_why_no_id_is_renumbered`

Old text:

```
    if plan.undecidable:
        notes.append(_undecidable(plan))
```

New text:

```
    if False:
        notes.append(_undecidable(plan))
```

### `u115.F19_unrenumbered_unsaid`

The envelope says nothing about the rows left with a random id because their file could not be read

- File: `src/cratekit/write/row_defaults_cli.py`
- Source: `u115.json`, row `F19_unrenumbered_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_row_whose_file_is_gone_is_named_on_a_run_that_writes_nothing`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
    if plan.unrenumbered:
        notes.append(_unrenumbered(plan))
```

New text:

```
    if False:
        notes.append(_unrenumbered(plan))
```

### `a32.A2_stale_deleted`

A row deleted since the plan is still written

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `A2_stale_deleted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_row_deleted_since_the_plan_refuses_stale_and_writes_nothing`

Old text:

```
        if row is None or row[rb_writer.SOFT_DELETE_COLUMN] != 0:
```

New text:

```
        if row is None:
```

### `a32.A3_stale_value`

A row whose column moved since the plan is still written

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `A3_stale_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_column_changed_since_the_plan_refuses_stale_and_writes_nothing`

Old text:

```
        elif _text(row.get(probe.column)) != probe.was:
```

New text:

```
        elif False:
```

### `a32.A5_policy_widened`

The commit's policy admits both probe columns whatever the plan writes

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `A5_policy_widened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_plan_writing_one_column_admits_only_that_one_to_the_guard`

Old text:

```
    policy = rb_writer.row_probe_policy(p.column for p in plan.writing)
```

New text:

```
    policy = rb_writer.row_probe_policy(rb_writer.ROW_PROBE_COLUMNS)
```

### `a32.D1_digest_drops_replaced`

Drop the replaced value from the item, so the digest does not move when it changes

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `D1_digest_drops_replaced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_link.py::test_the_digest_moves_with_the_rows_the_columns_and_both_values`
  - `tests/test_repair_link.py::test_the_plan_is_each_triple_its_values_and_who_else_carries_each`

Old text:

```
            "from": self.was,
```

New text:

```
            "from": "",
```

### `a32.D2_digest_unordered`

Keep the triples in the order given, so the same plan digests two ways

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `D2_digest_unordered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_the_digest_is_equal_whatever_order_the_triples_are_given_in`

Old text:

```
    probes.sort(key=lambda p: (len(p.content_id), p.content_id, p.column))
```

New text:

```
(empty)
```

### `a32.J1_wrong_unjudged`

The judge never reports a value that did not take

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `J1_wrong_unjudged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_judge_names_a_value_that_did_not_take_and_a_column_that_moved`

Old text:

```
            if now.get(probe.column) is None or _text(now[probe.column]) != str(probe.value):
```

New text:

```
            if False:
```

### `a32.J2_planned_across_rows`

The judge excuses every column the plan writes on any row, not the row's own

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `J2_planned_across_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_judge_counts_a_column_written_on_another_row_as_moved_here`

Old text:

```
        changed = row_defaults.moved_columns(was, now, planned=plan.columns_on(content_id))
```

New text:

```
        changed = row_defaults.moved_columns(was, now, planned=[p.column for p in plan.writing])
```

### `a32.J4_moved_not_refused`

A moved column is reported as a wrong value rather than the guard's defect

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `J4_moved_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_column_moved_after_the_commit_refuses_through_the_verb`
  - `tests/test_repair_link.py::test_assert_read_back_refuses_and_names_the_undo[a-moved-column]`

Old text:

```
    if written.moved:
        raise refuse(
            "whitelist-violation",
```

New text:

```
    if False:
        raise refuse(
            "whitelist-violation",
```

### `a32.P1_tombstone_plans`

Drop the live row filter from the plan's row query, so a tombstone plans

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `P1_tombstone_plans`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_triple_the_plan_cannot_take_refuses_by_name[a-tombstone]`

Old text:

```
                    f"WHERE ID = :id AND {rb_writer.SOFT_DELETE_COLUMN} = 0"
```

New text:

```
                    f"WHERE ID = :id"
```

### `a32.P2_unknown_row`

Drop the unknown row refusal, so an absent identifier falls through

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `P2_unknown_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 4 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_plan_refusal_reaches_no_gate`
  - `tests/test_repair_link.py::test_a_triple_the_plan_cannot_take_refuses_by_name[a-tombstone]`
  - `tests/test_repair_link.py::test_a_triple_the_plan_cannot_take_refuses_by_name[an-unknown-row]`
  - `tests/test_repair_link.py::test_a_triple_the_plan_cannot_take_refuses_by_name[one-bad-triple-refuses-the-whole-plan]`

Old text:

```
        if row is None:
            raise refuse(
                ROW_UNKNOWN,
```

New text:

```
        if row is None and False:
            raise refuse(
                ROW_UNKNOWN,
```

### `a32.P3_unheld_value`

Drop the unheld value refusal, so a value nobody carries is written

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `P3_unheld_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 3 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_triple_the_plan_cannot_take_refuses_by_name[a-link-nobody-carries]`
  - `tests/test_repair_link.py::test_a_triple_the_plan_cannot_take_refuses_by_name[a-value-only-a-tombstone-carries]`
  - `tests/test_repair_link.py::test_a_triple_the_plan_cannot_take_refuses_by_name[an-isrc-nobody-carries]`

Old text:

```
        if probe.writes and carriers == 0:
```

New text:

```
        if probe.writes and carriers < 0:
```

### `a32.P4_count_tombstones`

Count tombstones as carriers and fellows of a value

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `P4_count_tombstones`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 5 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_null_counts_its_fellows_as_null_so_writing_one_back_is_the_minority`
  - `tests/test_repair_link.py::test_a_triple_the_plan_cannot_take_refuses_by_name[a-value-only-a-tombstone-carries]`
  - `tests/test_repair_link.py::test_the_bindings_value_onto_a_row_rekordbox_made_refuses_as_the_minority`
  - `tests/test_repair_link.py::test_the_plan_is_each_triple_its_values_and_who_else_carries_each`
  - `tests/test_repair_link.py::test_the_two_acts_write_each_triple_and_move_no_other_column`

Old text:

```
            f"AND {rb_writer.SOFT_DELETE_COLUMN} = 0 AND ID != :id"
```

New text:

```
            f"AND ID != :id"
```

### `a32.P6_writes_always`

Every triple writes, a row already at the value included

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `P6_writes_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 6 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_plan_where_every_row_is_already_at_its_value_still_asks_and_writes_nothing`
  - `tests/test_repair_link.py::test_a_row_already_at_a_value_nobody_else_carries_still_plans_nothing`
  - `tests/test_repair_link.py::test_a_row_already_at_the_value_plans_nothing_for_that_triple`
  - `tests/test_repair_link.py::test_a_triple_already_at_its_value_is_shown_and_not_written`
  - `tests/test_repair_link.py::test_apply_refuses_a_plan_that_writes_nothing_as_a_defect`
  - `tests/test_repair_link.py::test_judge_skips_a_triple_that_writes_nothing`

Old text:

```
        return self.was != str(self.value)
```

New text:

```
        return True
```

### `a32.P7_minority_boundary`

Move the majority rule's boundary, so a value carried by as many rows as the row's own is written

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `P7_minority_boundary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_triple_the_plan_cannot_take_refuses_by_name[a-value-as-many-rows-carry-as-the-rows-own]`

Old text:

```
        if probe.writes and carriers <= fellows:
```

New text:

```
        if probe.writes and carriers < fellows:
```

### `a32.P8_null_fellows`

Count a NULL's fellows with an equality, which matches nothing, so a NULL has no fellows

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `P8_null_fellows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_the_plan_is_each_triple_its_values_and_who_else_carries_each`

Old text:

```
    test = f"{column} IS NULL" if value is None else f"{column} = :value"
```

New text:

```
    test = f"{column} = :value"
```

### `a32.V1_any_column`

A triple naming a column outside the probe set is parsed, AnalysisUpdated included

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `V1_any_column`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 4 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_malformed_triple_or_a_column_outside_the_probe_refuses_by_name[101:AnalysisUpdated=2]`
  - `tests/test_repair_link.py::test_a_malformed_triple_or_a_column_outside_the_probe_refuses_by_name[101:BPM=12800]`
  - `tests/test_repair_link.py::test_a_malformed_triple_or_a_column_outside_the_probe_refuses_by_name[101:Title=x]`
  - `tests/test_repair_link.py::test_a_malformed_triple_refuses_through_the_verb_before_any_gate`

Old text:

```
    if kind is None:
        raise _invalid(
```

New text:

```
    if False:
        raise _invalid(
```

### `a32.V2_link_not_converted`

A ContentLink value is kept as text rather than converted to a whole number

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `V2_link_not_converted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 4 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_malformed_triple_or_a_column_outside_the_probe_refuses_by_name[101:ContentLink=]`
  - `tests/test_repair_link.py::test_a_malformed_triple_or_a_column_outside_the_probe_refuses_by_name[101:ContentLink=lots]`
  - `tests/test_repair_link.py::test_a_triple_reads_row_column_and_a_value_of_the_columns_type`
  - `tests/test_repair_link.py::test_the_plan_is_each_triple_its_values_and_who_else_carries_each`

Old text:

```
    if kind is int:
```

New text:

```
    if False:
```

### `a32.C1_ack_after_gate`

The backup acknowledgment is not read before the gate

- File: `src/cratekit/write/row_link_cli.py`
- Source: `a32.json`, row `C1_ack_after_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    session.assert_backup_acknowledged(cfg)

    plan = _plan(cfg, ctx.args)
```

New text:

```
    plan = _plan(cfg, ctx.args)
```

### `a32.C2_abort_writes`

An abort at the gate proceeds to the write

- File: `src/cratekit/write/row_link_cli.py`
- Source: `a32.json`, row `C2_abort_writes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_an_abort_writes_nothing`

Old text:

```
    if ctx.gate.require(spec, plan=data, context=_facts(plan)) != "apply":
```

New text:

```
    if ctx.gate.require(spec, plan=data, context=_facts(plan)) not in ("apply", "abort"):
```

### `a32.C3_nothing_to_write_applies`

A plan that writes nothing reaches the apply

- File: `src/cratekit/write/row_link_cli.py`
- Source: `a32.json`, row `C3_nothing_to_write_applies`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_plan_where_every_row_is_already_at_its_value_still_asks_and_writes_nothing`

Old text:

```
    if not plan.writes:
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=[_nothing(plan)])
```

New text:

```
    if False:
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=[_nothing(plan)])
```

### `a32.C4_read_back_unasserted`

The verb answers OK without asserting the read back

- File: `src/cratekit/write/row_link_cli.py`
- Source: `a32.json`, row `C4_read_back_unasserted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_column_moved_after_the_commit_refuses_through_the_verb`

Old text:

```
    row_link.assert_read_back(written)
    data["totals"] = {
```

New text:

```
    data["totals"] = {
```

### `r375-b.M1_capture_never_attached`

mytags_vocals: take the capture and never attach it, which is R-375 itself with a record beside it

- File: `src/cratekit/write/trees.py`
- Source: `r375-b.json`, row `M1_capture_never_attached`
- Moved: U298 replaced mytags_vocals' own capture, attach and verify lines with trees.attached_capture, which it now calls; the attach is the same line there, so dropping it takes the capture and never attaches it
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 3 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_an_apply_is_listed_by_restore_list_as_a_restorable_session`
  - `tests/test_metadata_cli.py::test_an_apply_that_refuses_mid_write_is_abandoned_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_the_capture_is_protected_while_the_apply_is_in_flight`

Old text:

```
    capture = snapshot.capture(cfg, db=db)
    session.attach_capture(record, capture.root, cfg)
    snapshot.assert_verified(capture)
    return record, capture
```

New text:

```
    capture = snapshot.capture(cfg, db=db)
    snapshot.assert_verified(capture)
    return record, capture
```

### `u302.W9c_configuration_rules_dropped`

what W9 holds: prefix_rules with no caller map returns no rules, so a recorded path is never resolved through the configuration

- File: `src/cratekit/write/trees.py`
- Source: `u302.json`, row `W9c_configuration_rules_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tree_writer.py`, `tests/test_naming_apply_cli.py`, `tests/test_routing_workers.py`, `tests/test_deferred_routing.py`
- Collected: 438 against a baseline of 438
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_under_a_remapped_volume_still_protects_its_file[prefix_map0]`
  - `tests/test_routing_workers.py::test_an_export_location_under_a_retired_volume_name_resolves_through_the_prefix_map`

Old text:

```
        return list(locations.prefix_rules(cfg.resolved_prefix_map()))
```

New text:

```
        return []
```

### `u40-author-full.F4_tombstone_indexed`

First caller sample: stop dropping tombstones from the active row index, so a removed track claims its location

- File: `src/cratekit/write/trees.py`
- Source: `u40-author-full.json`, row `F4_tombstone_indexed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_genre_retag.py`, `tests/test_rebuild.py`, `tests/test_tree_registry.py`, `tests/test_tree_writer.py`, `tests/test_xml_splice_golden.py`
- Collected: 757 against a baseline of 757
- Kills: 3 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_soft_deleted_row_is_never_retagged`
  - `tests/test_rebuild.py::test_a_membership_pointing_at_a_soft_deleted_row_is_not_a_difference_either`
  - `tests/test_tree_writer.py::test_normalization_resolves_each_spelling_to_the_right_row[a-tombstone-beside-an-active-row]`

Old text:

```
    for row in rows:
        if row.deleted:
            continue
        resolved = _comparable(row.recorded, root=root, prefix_map=prefix_map)
```

New text:

```
    for row in rows:
        resolved = _comparable(row.recorded, root=root, prefix_map=prefix_map)
```

### `u77-b.B6_trial_id`

check_record_labels_tree: trial every year with no id, so the writer returns from a held playlist before its three layout refusals and the check passes what the write refuses

- File: `src/cratekit/write/trees.py`
- Source: `u77-b.json`, row `B6_trial_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 254 against a baseline of 254
- Kills: 2 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_a_held_year_playlist_the_writer_cannot_extend_refuses_before_any_move`
  - `tests/test_tree_writer.py::test_the_catalog_check_reaches_a_held_playlist_the_writer_cannot_extend`

Old text:

```
trial, label, [(f"{label} {year}", [_TRIAL_ID]) for year in years], target
```

New text:

```
trial, label, [(f"{label} {year}", []) for year in years], target
```

### `u77-b.B7_check_empty_catalog`

check_record_labels_tree: resolve the catalog tree even when nothing would be written, so an undeclared tree refuses a landing that has no label row

- File: `src/cratekit/write/trees.py`
- Source: `u77-b.json`, row `B7_check_empty_catalog`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 254 against a baseline of 254
- Kills: 3 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_an_undeclared_catalog_tree_costs_a_landing_with_no_label_row_nothing[favourites]`
  - `tests/test_landing_labels.py::test_an_undeclared_catalog_tree_costs_a_landing_with_no_label_row_nothing[no-manifest]`
  - `tests/test_tree_writer.py::test_the_catalog_check_asks_nothing_when_there_is_nothing_to_write`

Old text:

```
    if not catalog:
        return
    target = _catalog_tree(declared, registry, tree)
    trial
```

New text:

```
    if catalog is None:
        return
    target = _catalog_tree(declared, registry, tree)
    trial
```

### `u77-b.B8_label_write_order`

insert_record_labels_trees: write the sources first name first, so a new tree reads Z to A

- File: `src/cratekit/write/trees.py`
- Source: `u77-b.json`, row `B8_label_write_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 254 against a baseline of 254
- Kills: 2 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_two_labels_across_two_years_are_four_playlists_in_the_intake_file`
  - `tests/test_tree_writer.py::test_several_sources_are_one_write_and_a_new_tree_reads_a_to_z`

Old text:

```
    for label in sorted(catalog, reverse=True):
        _insert_catalog(content,
```

New text:

```
    for label in sorted(catalog):
        _insert_catalog(content,
```

### `u258.M1_key_on_length`

parsed: key the memo on the text's length, not the text, so an equal length edit is served the old tree

- File: `tests/_parse_memo.py`
- Source: `u258.json`, row `M1_key_on_length`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_parse_memo.py`
- Collected: 10 against a baseline of 10
- Kills: 1 (killed)
- Killed:
  - `tests/test_parse_memo.py::test_a_file_edited_inside_a_scope_is_read_as_it_now_is`

Old text:

```
    tree = _TREES.get(source)
    if tree is None:
        tree = ast.parse(source)
        _TREES[source] = tree
```

New text:

```
    tree = _TREES.get(len(source))
    if tree is None:
        tree = ast.parse(source)
        _TREES[len(source)] = tree
```

### `u258.M2_scope_shares_nothing`

parsed: parse on every call inside a scope too, so a test's sweeps parse each file again

- File: `tests/_parse_memo.py`
- Source: `u258.json`, row `M2_scope_shares_nothing`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_parse_memo.py`
- Collected: 10 against a baseline of 10
- Kills: 6 (killed)
- Killed:
  - `tests/test_parse_memo.py::test_a_decorated_test_shares_and_keeps_its_name_and_its_fixtures`
  - `tests/test_parse_memo.py::test_a_file_edited_inside_a_scope_is_read_as_it_now_is`
  - `tests/test_parse_memo.py::test_a_scope_inside_a_scope_shares_the_outer_one_and_ends_with_it`
  - `tests/test_parse_memo.py::test_every_shared_question_leaves_a_shared_tree_as_a_fresh_parse_would`
  - `tests/test_parse_memo.py::test_inside_a_scope_one_text_is_parsed_once_however_many_ask`
  - `tests/test_parse_memo.py::test_the_population_sweeps_parse_each_package_file_once_between_them`

Old text:

```
    tree = _TREES.get(source)
    if tree is None:
```

New text:

```
    tree = _TREES.get(source)
    if True:
```

### `u258.M3_scope_never_ends`

sharing_parses: leave the trees in place when the scope ends, so a test's trees outlive it

- File: `tests/_parse_memo.py`
- Source: `u258.json`, row `M3_scope_never_ends`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_parse_memo.py`
- Collected: 10 against a baseline of 10
- Kills: 5 (killed)
- Killed:
  - `tests/test_parse_memo.py::test_a_decorated_test_shares_and_keeps_its_name_and_its_fixtures`
  - `tests/test_parse_memo.py::test_a_file_edited_inside_a_scope_is_read_as_it_now_is`
  - `tests/test_parse_memo.py::test_a_scope_drops_its_trees_when_it_ends_however_it_ends`
  - `tests/test_parse_memo.py::test_a_scope_inside_a_scope_shares_the_outer_one_and_ends_with_it`
  - `tests/test_parse_memo.py::test_outside_a_scope_nothing_is_held_and_every_ask_parses`

Old text:

```
    try:
        yield
    finally:
        _TREES = None
```

New text:

```
    try:
        yield
    finally:
        pass
```

### `u258.M4_inner_scope_ends_the_outer`

sharing_parses: open a fresh memo for a scope inside a scope, so the inner one drops the outer one's trees

- File: `tests/_parse_memo.py`
- Source: `u258.json`, row `M4_inner_scope_ends_the_outer`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_parse_memo.py`
- Collected: 10 against a baseline of 10
- Kills: 2 (killed)
- Killed:
  - `tests/test_parse_memo.py::test_a_file_edited_inside_a_scope_is_read_as_it_now_is`
  - `tests/test_parse_memo.py::test_a_scope_inside_a_scope_shares_the_outer_one_and_ends_with_it`

Old text:

```
    if _TREES is not None:
        yield
        return
    _TREES = {}
```

New text:

```
    _TREES = {}
```

### `u258.M5_decorator_opens_no_scope`

shares_parses: call the test without opening a scope, so a decorated test shares nothing

- File: `tests/_parse_memo.py`
- Source: `u258.json`, row `M5_decorator_opens_no_scope`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_parse_memo.py`
- Collected: 10 against a baseline of 10
- Kills: 2 (killed)
- Killed:
  - `tests/test_parse_memo.py::test_a_decorated_test_shares_and_keeps_its_name_and_its_fixtures`
  - `tests/test_parse_memo.py::test_a_file_edited_inside_a_scope_is_read_as_it_now_is`

Old text:

```
        with sharing_parses():
            return test(*args, **kwargs)
```

New text:

```
        return test(*args, **kwargs)
```

### `u258.M6_decorator_returns_the_test`

shares_parses: hand the test back undecorated

- File: `tests/_parse_memo.py`
- Source: `u258.json`, row `M6_decorator_returns_the_test`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_parse_memo.py`
- Collected: 10 against a baseline of 10
- Kills: 1 (killed)
- Killed:
  - `tests/test_parse_memo.py::test_a_decorated_test_shares_and_keeps_its_name_and_its_fixtures`

Old text:

```
    return shared  # type: ignore[return-value]
```

New text:

```
    return test
```

### `u125.P2_drop_slug`

Remove cancelled from PINNED_NON_RESERVED_CAUSES while the tree still declares it

- File: `tests/_pinned_reserved_populations.py`
- Source: `u125.json`, row `P2_drop_slug`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`, `tests/test_reserved_causes.py::test_pinned_populations_derive_totals_and_key_by_module`
- Collected: 2 against a baseline of 2
- Kills: 2 (killed)
- Killed:
  - `tests/test_reserved_causes.py::test_pinned_populations_derive_totals_and_key_by_module`
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`

Old text:

```
    'canary-read-failed',
    'cancelled',
    'catalog-tree-undeclared',

```

New text:

```
    'canary-read-failed',
    'catalog-tree-undeclared',

```

### `u296.M19_pin_in_the_wrong_file`

read_package_pins: accept a module pinned in another package's file, so a pin can sit where nobody looks for it

- File: `tests/_pinned_reserved_populations.py`
- Source: `u296.json`, row `M19_pin_in_the_wrong_file`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_reserved_pins_reader.py`, `tests/test_reserved_causes.py`
- Collected: 235 against a baseline of 235
- Kills: 2 (killed)
- Killed:
  - `tests/test_reserved_pins_reader.py::test_a_file_the_reader_would_read_wrongly_is_refused[a-module-pinned-in-another-packages-file]`
  - `tests/test_reserved_pins_reader.py::test_a_frozenset_table_is_read_by_its_members`

Old text:

```
                if owner != package:
```

New text:

```
                if False:
```

### `u296.M20_unknown_pin_table`

read_package_pins: ignore a table it does not know, so a misspelt table silently stops pinning

- File: `tests/_pinned_reserved_populations.py`
- Source: `u296.json`, row `M20_unknown_pin_table`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_reserved_pins_reader.py`, `tests/test_reserved_causes.py`
- Collected: 235 against a baseline of 235
- Kills: 1 (killed)
- Killed:
  - `tests/test_reserved_pins_reader.py::test_a_file_the_reader_would_read_wrongly_is_refused[a-table-the-reader-does-not-know]`

Old text:

```
        if unknown:
            raise ValueError
```

New text:

```
        if False:
            raise ValueError
```

### `u12-independent-round-6.S2_package_never_resolved`

Always fall back to the dotted-tail heuristic even when the importing file's package is known, which is the false direction the round closed.

- File: `tests/_source_guards.py`
- Source: `u12-independent-round-6.json`, row `S2_package_never_resolved`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`, `tests/test_review_queue.py`, `tests/test_cli_contract.py`
- Collected: 1443 against a baseline of 1443
- Kills: 10 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_relative_import_in_an_unrelated_package_is_not_this_module[0]`
  - `tests/test_pool_sizing.py::test_a_relative_import_in_an_unrelated_package_is_not_this_module[1]`
  - `tests/test_pool_sizing.py::test_a_relative_import_in_an_unrelated_package_is_not_this_module[2]`
  - `tests/test_pool_sizing.py::test_a_relative_import_in_an_unrelated_package_is_not_this_module[3]`
  - `tests/test_pool_sizing.py::test_a_relative_import_in_an_unrelated_package_is_not_this_module[4]`
  - `tests/test_pool_sizing.py::test_the_analysis_countdown_stays_silent_on_correctly_sized_modules[a-sibling-of-its-own-named-pool]`
  - `tests/test_pool_sizing.py::test_the_walk_credits_a_relative_import_only_to_the_package_that_owns_it`
  - `tests/test_review_queue.py::test_a_relative_import_is_resolved_against_the_package_the_file_sits_in[source0]`
  - `tests/test_review_queue.py::test_a_relative_import_is_resolved_against_the_package_the_file_sits_in[source1]`
  - `tests/test_review_queue.py::test_the_countdown_reads_a_decision_store_through_a_relative_import`

Old text:

```
                if node.level:
                    if package is None:

```

New text:

```
                if node.level:
                    if True:

```

### `u12-independent-round-6.S3_only_the_module_itself_counts`

Recognize only the module's own dotted name and none of its ancestor packages, the hole that let a fabricated plan through.

- File: `tests/_source_guards.py`
- Source: `u12-independent-round-6.json`, row `S3_only_the_module_itself_counts`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`, `tests/test_review_queue.py`, `tests/test_cli_contract.py`
- Collected: 1443 against a baseline of 1443
- Kills: 6 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_the_analysis_countdown_bites_the_evasions_that_used_to_pass_it[hand-built-plan-through-an-ancestor]`
  - `tests/test_pool_sizing.py::test_the_analysis_countdown_stays_silent_on_correctly_sized_modules[ancestor-package]`
  - `tests/test_pool_sizing.py::test_the_plan_provenance_guard_bites_a_plan_somebody_typed[4]`
  - `tests/test_pool_sizing.py::test_the_plan_provenance_guard_bites_a_plan_somebody_typed[5]`
  - `tests/test_pool_sizing.py::test_the_plan_provenance_guard_bites_a_plan_somebody_typed[6]`
  - `tests/test_pool_sizing.py::test_the_same_relative_shapes_still_bite_from_the_package_that_owns_them[2]`

Old text:

```
            for size in range(1, len(parts) + 1)

```

New text:

```
            for size in range(len(parts), len(parts) + 1)

```

### `u258.M7_a_question_writes_the_shared_tree`

reserved_code_tables_in: leave a note on every node of the tree it is handed, which every question after it would read

- File: `tests/_source_guards.py`
- Source: `u258.json`, row `M7_a_question_writes_the_shared_tree`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_parse_memo.py`, `tests/test_reserved_causes.py`
- Collected: 239 against a baseline of 239
- Kills: 1 (killed)
- Killed:
  - `tests/test_parse_memo.py::test_every_shared_question_leaves_a_shared_tree_as_a_fresh_parse_would`

Old text:

```
    return _reservations(ReservedCodeTable(tree, causes, code_range, package))
```

New text:

```
    for node in ast.walk(tree):
        node.seen_by_guard = True
    return _reservations(ReservedCodeTable(tree, causes, code_range, package))
```

### `u258.M8_tree_form_answers_nothing`

reserved_code_tables_in: report no reservation, so the widened headroom check over the population passes on anything

- File: `tests/_source_guards.py`
- Source: `u258.json`, row `M8_tree_form_answers_nothing`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_parse_memo.py`, `tests/test_reserved_causes.py`
- Collected: 239 against a baseline of 239
- Kills: 2 (killed)
- Killed:
  - `tests/test_parse_memo.py::test_a_file_edited_inside_a_scope_is_read_as_it_now_is`
  - `tests/test_parse_memo.py::test_shared_trees_answer_alike_in_either_order_and_as_trees_of_their_own`

Old text:

```
    return _reservations(ReservedCodeTable(tree, causes, code_range, package))
```

New text:

```
    return []
```

### `u326.W1_children_reads_lists`

_children: skip a list field's nodes, so a walk never enters a body, an argument list or a target list

- File: `tests/_source_guards.py`
- Source: `u326.json`, row `W1_children_reads_lists`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_reserved_causes.py`, `tests/test_rb_writer_guard.py`, `tests/test_review_queue.py`, `tests/test_cli_contract.py`
- Collected: 1616 against a baseline of 1616
- Kills: 153 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_the_csv_writer_guard_bites_and_stays_quiet_on_correct_code`
  - `tests/test_rb_writer_guard.py::test_a_conditional_defaulting_the_marker_fires_and_a_summary_string_does_not`
  - `tests/test_rb_writer_guard.py::test_a_presence_flag_is_not_a_marker_holder`
  - `tests/test_rb_writer_guard.py::test_defining_the_marker_on_a_row_double_is_not_reading_it`
  - `tests/test_rb_writer_guard.py::test_every_way_of_shadowing_a_lookup_table_still_fires[except as-    try:\n        pass\n    except ValueError as TABLE:\n        return TABLE.get(COLUMN, 0)\n]`
  - `tests/test_rb_writer_guard.py::test_every_way_of_shadowing_a_lookup_table_still_fires[for target-    for TABLE, _ in rows:\n        return TABLE.get(COLUMN, 0)\n]`
  - `tests/test_rb_writer_guard.py::test_every_way_of_shadowing_a_lookup_table_still_fires[nested unpacking-    (a, [TABLE, b]) = rows[0]\n    return TABLE.get(COLUMN, 0)\n]`
  - `tests/test_rb_writer_guard.py::test_every_way_of_shadowing_a_lookup_table_still_fires[plain assignment-    TABLE = rows[0]\n    return TABLE.get(COLUMN, 0)\n]`
  - `tests/test_rb_writer_guard.py::test_every_way_of_shadowing_a_lookup_table_still_fires[tuple unpacking-    TABLE, meta = rows[0]\n    return TABLE.get(COLUMN, 0)\n]`
  - `tests/test_rb_writer_guard.py::test_every_way_of_shadowing_a_lookup_table_still_fires[with as-    with rows as TABLE:\n        return TABLE.get(COLUMN, 0)\n]`
  - `tests/test_rb_writer_guard.py::test_only_the_declared_modules_read_the_soft_delete_marker_at_all`
  - `tests/test_rb_writer_guard.py::test_the_launder_rules_reach_a_class_body_and_a_nonlocal_rebinding`
  - `tests/test_rb_writer_guard.py::test_the_lookup_table_exclusion_is_not_an_evasion_route`
  - `tests/test_rb_writer_guard.py::test_the_lookup_table_exclusion_is_scope_aware_not_just_name_keyed`
  - `tests/test_rb_writer_guard.py::test_the_soft_delete_guard_catches_a_read_laundered_one_line_later`
  - ... and 138 more, see the JSON sidecar

Old text:

```
            found.extend([item for item in value if isinstance(item, _AST)])
```

New text:

```
            pass
```

### `u326.W2_cache_by_identity`

_walk: hand back the held walk for any module once one is held, so a second module is answered from the first

- File: `tests/_source_guards.py`
- Source: `u326.json`, row `W2_cache_by_identity`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_reserved_causes.py`, `tests/test_rb_writer_guard.py`, `tests/test_review_queue.py`, `tests/test_cli_contract.py`
- Collected: 1616 against a baseline of 1616
- Kills: 146 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[acquire.fallback-fetch]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[acquire.fallback]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[audit.duplicates]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[delete.review]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[intake.identify]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[intake.missing]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[intake.playlist]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[intake.set]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[label.approved]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[label.harvest]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[label.held]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[label.import]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[label.judge]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[label.sync]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[match.run]`
  - ... and 131 more, see the JSON sidecar

Old text:

```
    if not (_LAST_MODULE_WALK and _LAST_MODULE_WALK[0] is node):
```

New text:

```
    if not _LAST_MODULE_WALK:
```

### `u329.G1_guard_reads_the_old_accessor_name`

the soft delete guard looks for the accessor under its old name rb_writer, so _writer imported from rb_call_time names nothing

- File: `tests/_source_guards.py`
- Source: `u329.json`, row `G1_guard_reads_the_old_accessor_name`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_parts_guard.py`, `tests/test_rb_writer_guard.py`, `tests/test_no_beatgrid_ever.py`, `tests/test_split_modules.py`
- Collected: 277 against a baseline of 277
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_writer_parts_guard.py::test_every_accessor_read_of_the_column_in_the_parts_is_seen_by_the_guard`
  - `tests/test_rb_writer_parts_guard.py::test_the_accessor_imported_from_its_one_home_names_the_column`

Old text:

```
                    if alias.name == RB_WRITER_ACCESSOR:
```

New text:

```
                    if alias.name == "rb_writer":
```

### `u329.G2_guard_reads_the_old_home`

the soft delete guard looks for the accessor in core.call_time, a module that no longer exists

- File: `tests/_source_guards.py`
- Source: `u329.json`, row `G2_guard_reads_the_old_home`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_parts_guard.py`, `tests/test_rb_writer_guard.py`, `tests/test_no_beatgrid_ever.py`, `tests/test_split_modules.py`
- Collected: 277 against a baseline of 277
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_writer_parts_guard.py::test_every_accessor_read_of_the_column_in_the_parts_is_seen_by_the_guard`
  - `tests/test_rb_writer_parts_guard.py::test_the_accessor_imported_from_its_one_home_names_the_column`

Old text:

```
RB_WRITER_ACCESSOR_MODULE = "cratekit.core.rb_call_time"
```

New text:

```
RB_WRITER_ACCESSOR_MODULE = "cratekit.core.call_time"
```

### `u329.G3_guard_skips_the_relative_import`

the soft delete guard reads only the absolute import of the accessor, not from .rb_call_time

- File: `tests/_source_guards.py`
- Source: `u329.json`, row `G3_guard_skips_the_relative_import`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_parts_guard.py`, `tests/test_rb_writer_guard.py`, `tests/test_no_beatgrid_ever.py`, `tests/test_split_modules.py`
- Collected: 277 against a baseline of 277
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_parts_guard.py::test_the_accessor_imported_from_its_one_home_names_the_column`

Old text:

```
                node.level == 1 and module ==
```

New text:

```
                node.level == 2 and module ==
```

### `u232.A1_platform_stub`

_no_host_process_table: leave core.processes._platform as psutil, so the careful scan reads the host

- File: `tests/conftest.py`
- Source: `u232.json`, row `A1_platform_stub`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_host_process_table.py`, `tests/test_process_scan.py`, `tests/test_sync_bandcamp.py`, `tests/test_process_scan_jobs.py`
- Collected: 90 against a baseline of 90
- Kills: 4 (killed)
- Killed:
  - `tests/test_host_process_table.py::test_a_test_reaching_psutils_enumeration_without_the_opt_in_fails`
  - `tests/test_host_process_table.py::test_the_careful_scan_reads_no_rekordbox_with_rekordbox_open_on_the_host`
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`

Old text:

```
        monkeypatch.setattr(processes, "_platform", lambda: empty)
```

New text:

```
        pass
```

### `u232.A8_opt_in`

_no_host_process_table: ignore the real_process_table marker, so no test can reach the real table

- File: `tests/conftest.py`
- Source: `u232.json`, row `A8_opt_in`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_host_process_table.py`, `tests/test_process_scan.py`
- Collected: 55 against a baseline of 55
- Kills: 4 (killed)
- Killed:
  - `tests/test_host_process_table.py::test_a_test_opted_in_reads_the_real_host`
  - `tests/test_host_process_table.py::test_a_test_reaching_psutils_enumeration_without_the_opt_in_fails`
  - `tests/test_host_process_table.py::test_the_fake_host_is_what_the_real_scan_reads`
  - `tests/test_process_scan.py::test_the_seam_is_psutil_when_nothing_replaces_it`

Old text:

```
    if request.node.get_closest_marker(REAL_PROCESS_TABLE) is not None:
        yield
        return
    import psutil
```

New text:

```
    import psutil
```

### `u326.R8_general_catalogue_refused`

_no_live_general_catalogue: leave the process wide genre lookup as shipped, so an ISRC asks the real catalogue

- File: `tests/conftest.py`
- Source: `u326.json`, row `R8_general_catalogue_refused`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_published_genre.py::test_the_suite_cannot_reach_the_live_catalogue_through_the_shared_lookup`

Old text:

```
        monkeypatch.setattr(published, "_shared", [guarded])
```

New text:

```
        pass
```

### `u296.M21_placed_modules_unread`

layer_of: skip the per module placement table, so every module takes its directory's layer

- File: `tests/test_layering.py`
- Source: `u296.json`, row `M21_placed_modules_unread`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_layering.py`
- Collected: 50 against a baseline of 50
- Kills: 10 (killed)
- Killed:
  - `tests/test_layering.py::test_a_part_split_from_a_placed_module_is_placed_by_one_line_of_its_own`
  - `tests/test_layering.py::test_every_planned_module_has_a_layer[cratekit.cli.output-foundation]`
  - `tests/test_layering.py::test_every_planned_module_has_a_layer[cratekit.core.config-foundation]`
  - `tests/test_layering.py::test_every_planned_module_has_a_layer[cratekit.core.convergence-write]`
  - `tests/test_layering.py::test_every_planned_module_has_a_layer[cratekit.core.naming-foundation]`
  - `tests/test_layering.py::test_every_planned_module_has_a_layer[cratekit.core.routing-domain]`
  - `tests/test_layering.py::test_every_planned_module_has_a_layer[cratekit.core.taxonomy-domain]`
  - `tests/test_layering.py::test_every_planned_module_has_a_layer[cratekit.core.tree_registry-write]`
  - `tests/test_layering.py::test_the_package_imports_downward_only`
  - `tests/test_layering.py::test_upward_import_from_a_lower_layer_fails`

Old text:

```
    placed = _PLACED.get(module)
```

New text:

```
    placed = None
```

### `u253.L10_relative_is_the_name`

_location_codec_offenders: key the offender and the permitted pair on the file name, not its path under the root

- File: `tests/test_locations.py`
- Source: `u253.json`, row `L10_relative_is_the_name`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_locations.py`
- Collected: 146 against a baseline of 146
- Kills: 15 (killed)
- Killed:
  - `tests/test_locations.py::test_no_module_outside_this_one_decodes_a_location_itself`
  - `tests/test_locations.py::test_the_guard_itself_fails_naming_a_decoder_planted_under_its_root`
  - `tests/test_locations.py::test_the_permitted_quote_plus_is_excused_and_nothing_else_is`
  - `tests/test_locations.py::test_the_sweep_computes_each_relative_path_once_per_file`
  - `tests/test_locations.py::test_the_sweep_reports_each_name_called_bare_or_as_an_attribute[quote-attribute]`
  - `tests/test_locations.py::test_the_sweep_reports_each_name_called_bare_or_as_an_attribute[quote-bare]`
  - `tests/test_locations.py::test_the_sweep_reports_each_name_called_bare_or_as_an_attribute[quote_plus-attribute]`
  - `tests/test_locations.py::test_the_sweep_reports_each_name_called_bare_or_as_an_attribute[quote_plus-bare]`
  - `tests/test_locations.py::test_the_sweep_reports_each_name_called_bare_or_as_an_attribute[unquote-attribute]`
  - `tests/test_locations.py::test_the_sweep_reports_each_name_called_bare_or_as_an_attribute[unquote-bare]`
  - `tests/test_locations.py::test_the_sweep_reports_each_name_called_bare_or_as_an_attribute[unquote_plus-attribute]`
  - `tests/test_locations.py::test_the_sweep_reports_each_name_called_bare_or_as_an_attribute[unquote_plus-bare]`
  - `tests/test_locations.py::test_the_sweep_reports_every_call_and_reads_the_name_alone`
  - `tests/test_locations.py::test_the_sweep_skips_the_decoder_and_the_vendored_tree`
  - `tests/test_locations.py::test_the_sweep_still_reports_a_planted_decoder_by_its_relative_path`

Old text:

```
        relative = path.relative_to(root).as_posix()
```

New text:

```
        relative = path.name
```

### `u253.L11_guard_narrowed_root`

test_no_module_outside_this_one_decodes_a_location_itself: sweep one package of the tree rather than the whole root it is given

- File: `tests/test_locations.py`
- Source: `u253.json`, row `L11_guard_narrowed_root`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_locations.py`
- Collected: 146 against a baseline of 146
- Kills: 1 (killed)
- Killed:
  - `tests/test_locations.py::test_the_guard_itself_fails_naming_a_decoder_planted_under_its_root`

Old text:

```
    offenders = _location_codec_offenders(SRC_ROOT)
```

New text:

```
    offenders = _location_codec_offenders(SRC_ROOT / "cratekit" / "core")
```

### `u253.L12_guard_drops_the_sweep`

test_no_module_outside_this_one_decodes_a_location_itself: assert on an empty list, so the sweep's findings never reach the assert (round one's surviving row)

- File: `tests/test_locations.py`
- Source: `u253.json`, row `L12_guard_drops_the_sweep`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_locations.py`
- Collected: 146 against a baseline of 146
- Kills: 1 (killed)
- Killed:
  - `tests/test_locations.py::test_the_guard_itself_fails_naming_a_decoder_planted_under_its_root`

Old text:

```
    offenders = _location_codec_offenders(SRC_ROOT)
```

New text:

```
    offenders = []
```

### `u253.L2_relative_before_exclusions`

_location_codec_offenders: compute the relative path before the two exclusions, so a skipped file still costs one

- File: `tests/test_locations.py`
- Source: `u253.json`, row `L2_relative_before_exclusions`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_locations.py`
- Collected: 146 against a baseline of 146
- Kills: 1 (killed)
- Killed:
  - `tests/test_locations.py::test_the_sweep_computes_each_relative_path_once_per_file`

Old text:

```
    for path in sorted(root.rglob("*.py")):
        if path.name == "locations.py":
```

New text:

```
    for path in sorted(root.rglob("*.py")):
        path.relative_to(root)
        if path.name == "locations.py":
```

### `u253.L3_no_decoder_skip`

_location_codec_offenders: drop the locations.py skip, so the one decoder reports itself

- File: `tests/test_locations.py`
- Source: `u253.json`, row `L3_no_decoder_skip`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_locations.py`
- Collected: 146 against a baseline of 146
- Kills: 3 (killed)
- Killed:
  - `tests/test_locations.py::test_no_module_outside_this_one_decodes_a_location_itself`
  - `tests/test_locations.py::test_the_sweep_computes_each_relative_path_once_per_file`
  - `tests/test_locations.py::test_the_sweep_skips_the_decoder_and_the_vendored_tree`

Old text:

```
        if path.name == "locations.py":
            continue

```

New text:

```
(empty)
```

### `u253.L4_no_vendor_skip`

_location_codec_offenders: drop the vendored tree exclusion

- File: `tests/test_locations.py`
- Source: `u253.json`, row `L4_no_vendor_skip`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_locations.py`
- Collected: 146 against a baseline of 146
- Kills: 3 (killed)
- Killed:
  - `tests/test_locations.py::test_no_module_outside_this_one_decodes_a_location_itself`
  - `tests/test_locations.py::test_the_sweep_computes_each_relative_path_once_per_file`
  - `tests/test_locations.py::test_the_sweep_skips_the_decoder_and_the_vendored_tree`

Old text:

```
        if vendor_root in path.parents:
```

New text:

```
        if False:
```

### `u253.L5_vendor_skip_by_part`

_location_codec_offenders: widen the vendored exclusion to any directory named _vendor anywhere in the tree

- File: `tests/test_locations.py`
- Source: `u253.json`, row `L5_vendor_skip_by_part`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_locations.py`
- Collected: 146 against a baseline of 146
- Kills: 1 (killed)
- Killed:
  - `tests/test_locations.py::test_the_sweep_skips_the_decoder_and_the_vendored_tree`

Old text:

```
        if vendor_root in path.parents:
```

New text:

```
        if "_vendor" in path.parts:
```

### `u253.L6_permit_by_name_only`

_location_codec_offenders: excuse quote_plus in every module, the permitted pair narrowed on one axis only

- File: `tests/test_locations.py`
- Source: `u253.json`, row `L6_permit_by_name_only`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_locations.py`
- Collected: 146 against a baseline of 146
- Kills: 3 (killed)
- Killed:
  - `tests/test_locations.py::test_the_permitted_quote_plus_is_excused_and_nothing_else_is`
  - `tests/test_locations.py::test_the_sweep_reports_each_name_called_bare_or_as_an_attribute[quote_plus-attribute]`
  - `tests/test_locations.py::test_the_sweep_reports_each_name_called_bare_or_as_an_attribute[quote_plus-bare]`

Old text:

```
            if called in _LOCATION_CODEC_CALLS and (relative, called) not in _PERMITTED_CODEC_CALLS:
```

New text:

```
            if called in _LOCATION_CODEC_CALLS and called != "quote_plus":
```

### `u253.L7_bare_calls_only`

_location_codec_offenders: stop reading an attribute call, so parse.quote and shlex.quote pass

- File: `tests/test_locations.py`
- Source: `u253.json`, row `L7_bare_calls_only`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_locations.py`
- Collected: 146 against a baseline of 146
- Kills: 5 (killed)
- Killed:
  - `tests/test_locations.py::test_the_sweep_reports_each_name_called_bare_or_as_an_attribute[quote-attribute]`
  - `tests/test_locations.py::test_the_sweep_reports_each_name_called_bare_or_as_an_attribute[quote_plus-attribute]`
  - `tests/test_locations.py::test_the_sweep_reports_each_name_called_bare_or_as_an_attribute[unquote-attribute]`
  - `tests/test_locations.py::test_the_sweep_reports_each_name_called_bare_or_as_an_attribute[unquote_plus-attribute]`
  - `tests/test_locations.py::test_the_sweep_reports_every_call_and_reads_the_name_alone`

Old text:

```
                elif isinstance(node.func, ast.Attribute):
```

New text:

```
                elif False:
```

### `u253.L8_three_names`

_LOCATION_CODEC_CALLS: drop unquote_plus from the four names

- File: `tests/test_locations.py`
- Source: `u253.json`, row `L8_three_names`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_locations.py`
- Collected: 146 against a baseline of 146
- Kills: 3 (killed)
- Killed:
  - `tests/test_locations.py::test_the_sweep_reports_each_name_called_bare_or_as_an_attribute[unquote_plus-attribute]`
  - `tests/test_locations.py::test_the_sweep_reports_each_name_called_bare_or_as_an_attribute[unquote_plus-bare]`
  - `tests/test_locations.py::test_the_sweep_still_reports_a_planted_decoder_by_its_relative_path`

Old text:

```
_LOCATION_CODEC_CALLS = frozenset({"unquote", "unquote_plus", "quote", "quote_plus"})
```

New text:

```
_LOCATION_CODEC_CALLS = frozenset({"unquote", "quote", "quote_plus"})
```

### `u253.L9_one_line_per_file`

_location_codec_offenders: stop at a file's first offending call, so a second call in it goes unreported

- File: `tests/test_locations.py`
- Source: `u253.json`, row `L9_one_line_per_file`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_locations.py`
- Collected: 146 against a baseline of 146
- Kills: 1 (killed)
- Killed:
  - `tests/test_locations.py::test_the_sweep_reports_every_call_and_reads_the_name_alone`

Old text:

```
                offenders.append(f"{relative} calls {called}()")
```

New text:

```
                offenders.append(f"{relative} calls {called}()")
                break
```

### `r658-b.S10_outbound_zone`

Scope the zone to UTC instead of New York, which is the defect this test pins

- File: `tests/test_outbound_workers.py`
- Source: `r658-b.json`, row `S10_outbound_zone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_the_date_is_the_persons_own_and_not_greenwichs`

Old text:

```
        zone.setenv("TZ", "America/New_York")

```

New text:

```
        zone.setenv("TZ", "UTC")

```

### `u28-skills-independent.P1_annassign_branch`

the duplicate guard stops reading an AnnAssign, which is the node the annotated empty register became

- File: `tests/test_pending_units.py`
- Source: `u28-skills-independent.json`, row `P1_annassign_branch`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_the_intended_pending_set_has_no_duplicate_element`

Old text:

```
        if isinstance(node, ast.AnnAssign):
            target = getattr(node.target, "id", None)
        elif isinstance(node, ast.Assign) and len(node.targets) == 1:
```

New text:

```
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
```

### `u28-skills-independent.P2_empty_call_args`

the duplicate guard stops tolerating frozenset() with no argument, which is the empty register's own spelling

- File: `tests/test_pending_units.py`
- Source: `u28-skills-independent.json`, row `P2_empty_call_args`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_the_intended_pending_set_has_no_duplicate_element`

Old text:

```
        elements = literal.args[0].elts if literal.args else []
```

New text:

```
        elements = literal.args[0].elts
```

### `u25-author-light.G4_sizing_countdown`

Report the analysis package as correctly sized no matter what it contains

- File: `tests/test_pool_sizing.py`
- Source: `u25-author-light.json`, row `G4_sizing_countdown`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 7 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_the_analysis_countdown_bites_the_evasions_that_used_to_pass_it[core-count-in-a-hand-built-plan]`
  - `tests/test_pool_sizing.py::test_the_analysis_countdown_bites_the_evasions_that_used_to_pass_it[empty]`
  - `tests/test_pool_sizing.py::test_the_analysis_countdown_bites_the_evasions_that_used_to_pass_it[hand-built-plan-through-an-ancestor]`
  - `tests/test_pool_sizing.py::test_the_analysis_countdown_bites_the_evasions_that_used_to_pass_it[hand-built-plan-through-the-stream]`
  - `tests/test_pool_sizing.py::test_the_analysis_countdown_bites_the_evasions_that_used_to_pass_it[hand-built-plan]`
  - `tests/test_pool_sizing.py::test_the_analysis_countdown_bites_the_evasions_that_used_to_pass_it[no-sizing]`
  - `tests/test_pool_sizing.py::test_the_analysis_countdown_bites_the_evasions_that_used_to_pass_it[private-pool]`

Old text:

```
    if not modules:
        return ["the analysis package landed with no modules in it"]

```

New text:

```
    return []

```

### `u232.A10_real_walk_restored`

real_probes: leave pyrekordbox's walk stubbed, so the U211 tests over a dying process_iter read nothing

- File: `tests/test_process_scan.py`
- Source: `u232.json`, row `A10_real_walk_restored`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`
- Collected: 46 against a baseline of 46
- Kills: 8 (killed)
- Killed:
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[agent]`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[both]`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[none]`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[rekordbox]`
  - `tests/test_process_scan.py::test_pyrekordbox_alone_lets_the_dying_process_escape`
  - `tests/test_process_scan.py::test_the_writer_refuses_a_live_unreadable_process_by_name_not_as_internal`
  - `tests/test_process_scan.py::test_the_writer_refuses_a_read_agent_as_running_not_as_unconfirmed`
  - `tests/test_process_scan.py::test_the_writer_still_sees_rekordbox_beside_the_dying_process`

Old text:

```
    monkeypatch.setattr(pyrekordbox.utils, "get_process_id", REAL_WALK)
```

New text:

```
    pass
```

### `u256.T4_key_carries_the_variant`

_build_disposable_database: key the cache on the pin alone, so an untagged call gets the tagged database or the other way about

- File: `tests/test_rb_writer_db.py`
- Source: `u256.json`, row `T4_key_carries_the_variant`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_fixture_database_template.py`, `tests/test_rb_writer_db.py`
- Collected: 57 against a baseline of 57
- Kills: 2 (killed)
- Killed:
  - `tests/test_fixture_database_template.py::test_each_variant_is_built_from_nothing_once_and_every_call_gets_its_own_file`
  - `tests/test_rb_writer_db.py::test_a_library_with_no_tag_category_refuses_rather_than_inventing_one`

Old text:

```
    key = (with_tag_category, db_version)
```

New text:

```
    key = (True, db_version)
```

### `u256.T8_private_copy_per_call`

_build_disposable_database: hand every caller the first caller's file by a hard link instead of a copy, the shared mutable state the unit must not introduce

- File: `tests/test_rb_writer_db.py`
- Source: `u256.json`, row `T8_private_copy_per_call`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_fixture_database_template.py`, `tests/test_rb_writer_db.py`
- Collected: 57 against a baseline of 57
- Kills: 6 (killed)
- Killed:
  - `tests/test_fixture_database_template.py::test_a_database_written_and_encrypted_leaves_its_sibling_and_the_next_untouched`
  - `tests/test_fixture_database_template.py::test_each_variant_is_built_from_nothing_once_and_every_call_gets_its_own_file`
  - `tests/test_rb_writer_db.py::test_a_snapshot_check_that_names_no_key_verifies_either_kind[encrypted]`
  - `tests/test_rb_writer_db.py::test_an_encrypted_database_does_not_open_with_the_key_withheld`
  - `tests/test_rb_writer_db.py::test_an_open_that_names_no_key_opens_either_kind_of_database[encrypted]`
  - `tests/test_rb_writer_db.py::test_the_batch_membership_primitive_reads_presence_once_and_inserts_what_is_absent`

Old text:

```
    descriptor = os.open(db_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, _SQLITE_FILE_MODE)
```

New text:

```
    first = _TEMPLATES.setdefault(("first", key), db_path)
    if first != db_path and os.path.exists(first):
        os.link(first, db_path)
        return
    descriptor = os.open(db_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, _SQLITE_FILE_MODE)
```

### `r658-b.S8_reserved_short_walk`

Drop the scoped short walk handed to structured_refusal_causes

- File: `tests/test_reserved_causes.py`
- Source: `r658-b.json`, row `S8_reserved_short_walk`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reserved_causes.py`
- Collected: 229 against a baseline of 229
- Kills: 1 (killed)
- Killed:
  - `tests/test_reserved_causes.py::test_the_derivation_refuses_to_answer_from_an_incomplete_walk`

Old text:

```
        short_walk.setitem(
            globals(),
            "imported_package_modules",
            lambda: ([], {"cratekit.modules.tools.backup": "No module named 'boto3'"}),
        )

```

New text:

```
(empty)
```

### `r658-b.S9_reserved_moved_module`

Drop the scoped EXIT_CODE_MODULE move

- File: `tests/test_reserved_causes.py`
- Source: `r658-b.json`, row `S9_reserved_moved_module`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reserved_causes.py`
- Collected: 229 against a baseline of 229
- Kills: 1 (killed)
- Killed:
  - `tests/test_reserved_causes.py::test_the_module_and_the_class_are_named_once_each`

Old text:

```
        moved_module.setattr(_guards, "EXIT_CODE_MODULE", "cratekit.core.statuses")

```

New text:

```
(empty)
```

### `u258.M11_kebab_reads_a_second_package`

kebab_literals_by_module: read the package again rather than the sources the test handed it, so the two can disagree

- File: `tests/test_reserved_causes.py`
- Source: `u258.json`, row `M11_kebab_reads_a_second_package`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_reserved_causes.py`, `tests/test_parse_memo.py`
- Collected: 239 against a baseline of 239
- Kills: 1 (killed)
- Killed:
  - `tests/test_parse_memo.py::test_the_population_sweeps_parse_each_package_file_once_between_them`

Old text:

```
    found: dict[str, list[str]] = {}
    for relative, source in sources:
        hits = sorted(
```

New text:

```
    found: dict[str, list[str]] = {}
    for relative, source in package_sources():
        hits = sorted(
```

### `u258.M9_population_keeps_the_owners`

population_under_measurement: keep the two table owners, so every count in the at risk section is over a wider basis than its pins

- File: `tests/test_reserved_causes.py`
- Source: `u258.json`, row `M9_population_keeps_the_owners`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_reserved_causes.py`, `tests/test_parse_memo.py`
- Collected: 239 against a baseline of 239
- Kills: 2 (killed)
- Killed:
  - `tests/test_reserved_causes.py::test_pinned_populations_derive_totals_and_key_by_module`
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`

Old text:

```
        for relative, source in sources
        if relative not in TABLE_OWNERS
    ]
```

New text:

```
        for relative, source in sources
    ]
```

### `u312.C1_citation_prefilter`

the citation sweep: look only at texts that say residuals, so a citation written with the singular word is never read

- File: `tests/test_reserved_causes.py`
- Source: `u312.json`, row `C1_citation_prefilter`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_reserved_causes.py`
- Collected: 229 against a baseline of 229
- Kills: 2 (killed)
- Killed:
  - `tests/test_reserved_causes.py::test_every_residual_this_unit_cites_is_cited_by_title`
  - `tests/test_reserved_causes.py::test_the_covered_file_set_is_derived_and_reaches_what_the_unit_touched`

Old text:

```
        if "residual" in text and CITATION.search(text):
```

New text:

```
        if "residuals" in text and CITATION.search(text):
```

### `u199.M1_table_not_applied`

_lost_paragraphs: apply no rewording at all, as if the table were empty, so U195's deliberate sentence reads as a lost paragraph

- File: `tests/test_restart_and_residual_files.py`
- Source: `u199.json`, row `M1_table_not_applied`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_every_moved_paragraph_is_in_a_fragment_byte_for_byte`

Old text:

```
    for entry in rewordings:
        expected = [p.replace(entry.old, entry.new) for p in expected]
```

New text:

```
    for entry in ():
        expected = [p.replace(entry.old, entry.new) for p in expected]
```

### `u199.M2_entry_widened_to_paragraph`

_lost_paragraphs: an entry excuses the whole paragraph holding its old text rather than replacing only its span

- File: `tests/test_restart_and_residual_files.py`
- Source: `u199.json`, row `M2_entry_widened_to_paragraph`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 3 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_changed_or_removed_paragraph_still_fails[change0]`
  - `tests/test_restart_and_residual_files.py::test_a_changed_or_removed_paragraph_still_fails[change1]`
  - `tests/test_restart_and_residual_files.py::test_a_changed_or_removed_paragraph_still_fails[change2]`

Old text:

```
        expected = [p.replace(entry.old, entry.new) for p in expected]
```

New text:

```
        expected = [entry.new if entry.old in p else p for p in expected]
```

### `u199.M3_only_the_opening_compared`

_lost_paragraphs: compare only each paragraph's first 80 characters, so the byte for byte check stops holding the rest

- File: `tests/test_restart_and_residual_files.py`
- Source: `u199.json`, row `M3_only_the_opening_compared`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 3 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_changed_or_removed_paragraph_still_fails[change0]`
  - `tests/test_restart_and_residual_files.py::test_a_changed_or_removed_paragraph_still_fails[change1]`
  - `tests/test_restart_and_residual_files.py::test_a_changed_or_removed_paragraph_still_fails[change2]`

Old text:

```
    return [p[:80] for p in expected if p not in joined]
```

New text:

```
    return [p[:80] for p in expected if p[:80] not in joined]
```

### `u199.M4_exactly_once_relaxed`

_stale_rewordings: accept an old text found many times, so an entry can rewrite several paragraphs at once

- File: `tests/test_restart_and_residual_files.py`
- Source: `u199.json`, row `M4_exactly_once_relaxed`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_stale_rewording_fails_rather_than_excusing_nothing[entry1-times, not once]`

Old text:

```
        if found != 1:
```

New text:

```
        if found == 0:
```

### `u199.M5_old_text_unchecked`

_stale_rewordings: drop the check on the old text, so an entry whose old text is not in the split base passes

- File: `tests/test_restart_and_residual_files.py`
- Source: `u199.json`, row `M5_old_text_unchecked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 2 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_stale_rewording_fails_rather_than_excusing_nothing[entry0-in the split base 0 times]`
  - `tests/test_restart_and_residual_files.py::test_a_stale_rewording_fails_rather_than_excusing_nothing[entry1-times, not once]`

Old text:

```
        if found != 1:
```

New text:

```
        if False:
```

### `u199.M6_new_text_unchecked`

_stale_rewordings: drop the check on the new text, so an entry whose new text is in no fragment passes

- File: `tests/test_restart_and_residual_files.py`
- Source: `u199.json`, row `M6_new_text_unchecked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 2 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_stale_rewording_fails_rather_than_excusing_nothing[entry2-its new text is not in r301.md]`
  - `tests/test_restart_and_residual_files.py::test_a_stale_rewording_fails_rather_than_excusing_nothing[entry3-its new text is not in r999.md]`

Old text:

```
        if entry.new not in fragments.get(entry.fragment, ""):
```

New text:

```
        if False:
```

### `u199.M7_new_text_in_any_fragment`

_stale_rewordings: look for the new text in every fragment rather than the one the entry names

- File: `tests/test_restart_and_residual_files.py`
- Source: `u199.json`, row `M7_new_text_in_any_fragment`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_stale_rewording_fails_rather_than_excusing_nothing[entry3-its new text is not in r999.md]`

Old text:

```
        if entry.new not in fragments.get(entry.fragment, ""):
```

New text:

```
        if entry.new not in "\n\n".join(fragments.values()):
```

### `r658-b.S6_restore_full_disk`

Drop the scoped full disk around the first restore run

- File: `tests/test_restore.py`
- Source: `r658-b.json`, row `S6_restore_full_disk`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`
- Collected: 159 against a baseline of 159
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_round6_a_retry_after_a_partial_failure_still_runs`

Old text:

```
        full_disk.setattr(restore, "_replace_file", _explode)

```

New text:

```
(empty)
```

### `u28-skills-independent.L9_command_comment_split`

the fenced text stops being split into command and comment, so a retired name in a history note is checked as a command

- File: `tests/test_skills_lint.py`
- Source: `u28-skills-independent.json`, row `L9_command_comment_split`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            elif " #" in line:
                command, _, tail = line.partition(" #")
                command_parts.append(command)
                comment_parts.append(tail)
```

New text:

```
            elif " #" in line:
                command_parts.append(line)
```

