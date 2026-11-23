# Mutation table: u302-replay-after-c

Measured by `scripts/mutate.py` on 2026-11-22 22:32 UTC, branch `HEAD` at `9e27b874`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22930 collected. pytest invocations for this batch: 155.

Full baseline: measured by this driver (the battery's verdict was not read: no battery verdict at `.cloud-battery/verdict.json`).

Subset baselines: 24, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `../known-after.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22930 against 22930. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r745-a.E10_text_not_cleaned` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 7 | killed |
| `r745-a.E11_any_path_encoded` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 2 | killed |
| `r745-a.E12_three_stars_moved` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 2 | killed |
| `r745-a.E13_siblings_by_identifier` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 2 | killed |
| `r745-a.E1_tombstone_row_written` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 16 | killed |
| `r745-a.E3_tombstone_playlist_written` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 4 | killed |
| `r745-a.E4_dangling_member_written` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 6 | killed |
| `r745-a.E5_empty_folder_self_closed` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 34 | killed |
| `r745-a.E6_tempo_constant_moved` | `src/cratekit/write/collection_export.py` | user | 2 file(s) | 129 | 2 | killed |
| `r745-a.E7_identifier_not_held_to_digits` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 2 | killed |
| `r745-a.E8_duplicate_identifier_written` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 1 | killed |
| `r745-a.E9_smart_playlist_written` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 3 | killed |
| `r745-b.E14_members_as_they_arrive` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 1 | killed |
| `r745-b.E15_unreadable_kind_is_a_playlist` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 3 | killed |
| `r745-b.E16_lookups_not_primed` | `src/cratekit/write/collection_export.py` | maintainer | 1 file(s) | 94 | 1 | killed |
| `r745-b.E17_provenance_read_anywhere` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 1 | killed |
| `r745-c.E2_tombstone_membership_written` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 2 | killed |
| `r773-a.M10_unmapped_rows_not_collected` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 4 | killed |
| `r773-a.M11_prefixes_least_rows_first` | `src/cratekit/write/collection_export.py` | maintainer | 1 file(s) | 94 | 1 | killed |
| `r773-a.M1_read_back_not_asked` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 4 | killed |
| `r773-a.M2_unmapped_not_told_apart` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 4 | killed |
| `r773-a.M3_placed_row_written_as_recorded` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 5 | killed |
| `r773-a.M4_emitter_handed_the_rows_as_read` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 5 | killed |
| `r773-a.M5_another_host_not_caught` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 1 | killed |
| `r773-a.M6_left_row_counted_as_under_no_rule` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 4 | killed |
| `r773-a.M7_prefixes_not_carried` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 2 | killed |
| `r773-a.M8_placed_rows_not_counted` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 4 | killed |
| `r773-a.M9_left_rows_not_collected` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 4 | killed |
| `r773-a.S1_streamed_row_encoded_as_a_file` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 5 | killed |
| `r773-a.S2_tombstoned_row_written` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 16 | killed |
| `r773-a.S3_not_a_file_count_inverted` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 4 | killed |
| `r414.M10_skip_reason_reworded` | `src/cratekit/write/metadata.py` | user | 3 file(s) | 116 | 1 | killed |
| `r414.M11_byte_table_off_by_one` | `src/cratekit/write/metadata.py` | user | 3 file(s) | 116 | 3 | killed |
| `r414.M12_detail_key_renamed` | `src/cratekit/write/metadata.py` | maintainer | 3 file(s) | 116 | 5 | killed |
| `r414.M13_remedy_swapped` | `src/cratekit/write/metadata.py` | user | 3 file(s) | 116 | 5 | killed |
| `r414.M1_planner_writes_the_byte` | `src/cratekit/write/metadata.py` | user | 3 file(s) | 116 | 3 | killed |
| `r414.M2_fold_returns_the_byte` | `src/cratekit/write/metadata.py` | user | 3 file(s) | 116 | 4 | killed |
| `r414.M3_unknown_value_not_refused` | `src/cratekit/write/metadata.py` | user | 3 file(s) | 116 | 5 | killed |
| `r414.M4_star_passthrough_dropped` | `src/cratekit/write/metadata.py` | user | 3 file(s) | 116 | 2 | killed |
| `r414.M5_zero_passthrough_dropped` | `src/cratekit/write/metadata.py` | user | 3 file(s) | 116 | 1 | killed |
| `r414.M6_mixed_scale_not_refused` | `src/cratekit/write/metadata.py` | user | 3 file(s) | 116 | 1 | killed |
| `r414.M7_mixed_scale_needs_two_stars` | `src/cratekit/write/metadata.py` | user | 3 file(s) | 116 | 1 | killed |
| `r414.M8_curve_checked_lazily` | `src/cratekit/write/metadata.py` | user | 3 file(s) | 116 | 5 | killed |
| `r414.M9_zero_band_planned` | `src/cratekit/write/metadata.py` | user | 3 file(s) | 116 | 1 | killed |
| `r816-e.D1_resolve_once` | `src/cratekit/write/metadata.py` | maintainer | 3 file(s) | 169 | 1 | killed |
| `u163.W17_first_active` | `src/cratekit/write/metadata.py` | user | 3 file(s) | 294 | 2 | killed |
| `u40-author-full.F2_genre_unknown_silent` | `src/cratekit/write/metadata.py` | user | 2 file(s) | 97 | 4 | killed |
| `u40-author-full.F3_policy_owns_more` | `src/cratekit/write/metadata.py` | user | 2 file(s) | 97 | 2 | killed |
| `u59.M1_permissive_default` | `src/cratekit/write/metadata.py` | user | 2 file(s) | 97 | 3 | killed |
| `u59.M2_refusal_removed` | `src/cratekit/write/metadata.py` | user | 2 file(s) | 97 | 4 | killed |
| `u59.M3_none_admitted` | `src/cratekit/write/metadata.py` | user | 2 file(s) | 97 | 1 | killed |
| `u59.M4_tombstone_resolves` | `src/cratekit/write/metadata.py` | user | 2 file(s) | 97 | 10 | killed |
| `u59.M5_first_row_wins` | `src/cratekit/write/metadata.py` | user | 2 file(s) | 97 | 6 | killed |
| `u59.M6_reason_reworded` | `src/cratekit/write/metadata.py` | user | 2 file(s) | 97 | 4 | killed |
| `r239-b.S7_metadata_key_off` | `src/cratekit/write/metadata_cli.py` | user | 7 file(s) | 733 | 1 | killed |
| `r342.E1_cut_inclusive` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `r342.V13_detail_key` | `src/cratekit/write/metadata_cli.py` | maintainer | 1 file(s) | 26 | 10 | killed |
| `r342.V1_default_on_corrupt` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 12 | killed |
| `r342.V2_no_finite_check` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 2 | killed |
| `r342.V3_isnan_for_isfinite` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `r342.V4_no_bool_check` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `r342.V5_tuple_drops_overflow` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `r342.V6_tuple_drops_keyerror` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `r342.V7_tuple_drops_typeerror` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 3 | killed |
| `r342.V8_tuple_drops_valueerror` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 6 | killed |
| `r342.V9_tuple_drops_oserror` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `r372-a.A1_majority_boundary` | `src/cratekit/write/metadata_cli.py` | user | 3 file(s) | 494 | 1 | killed |
| `r372-a.A2_majority_coefficient` | `src/cratekit/write/metadata_cli.py` | user | 3 file(s) | 494 | 1 | killed |
| `r372-a.A3_pathless_rows_count_as_unmapped` | `src/cratekit/write/metadata_cli.py` | user | 3 file(s) | 494 | 17 | killed |
| `r372-a.A4_verb_never_refuses` | `src/cratekit/write/metadata_cli.py` | user | 3 file(s) | 494 | 2 | killed |
| `r372-a.A5_apply_proceeds` | `src/cratekit/write/metadata_cli.py` | user | 3 file(s) | 494 | 1 | killed |
| `r372-a.A6_decode_error_escapes` | `src/cratekit/write/metadata_cli.py` | user | 3 file(s) | 494 | 1 | killed |
| `r372-a.A7_remedy_run_doctor` | `src/cratekit/write/metadata_cli.py` | user | 3 file(s) | 494 | 3 | killed |
| `r372-a.A8_refused_plan_reports_ok` | `src/cratekit/write/metadata_cli.py` | user | 3 file(s) | 494 | 2 | killed |
| `r375-b.M2_a_noop_claims_a_commit` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `r375-b.M3_witnessed_commit_not_recorded` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `r375-b.M4_summary_keyed_on_the_display_name` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 2 | killed |
| `u25.G10_ignore_cut` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `u25.G11_gender_without_vox` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `u25.G12_apply_by_default` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 2 | killed |
| `u25.G13_skip_apply_gate` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 8 | killed |
| `u25.G15_barren_watch` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `u25.G24_content_column` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 6 | killed |
| `u89.L1_absent_is_default` | `src/cratekit/write/metadata_cli.py` | user | 2 file(s) | 223 | 126 | killed |
| `u89.L2_tagging_default` | `src/cratekit/write/metadata_cli.py` | user | 2 file(s) | 223 | 12 | killed |
| `u90-c.C6_wrapper_reads_nothing` | `src/cratekit/write/metadata_cli.py` | user | 2 file(s) | 198 | 8 | killed |
| `u90-c5.C5_record_threshold_unconverted` | `src/cratekit/write/metadata_cli.py` | user | 2 file(s) | 198 | 1 | killed |
| `r312.E10_empty_still_warns` | `src/cratekit/write/rebuild.py` | user | 2 file(s) | 307 | 3 | killed |
| `r312.E11_code_reworded` | `src/cratekit/write/rebuild.py` | user | 2 file(s) | 307 | 1 | killed |
| `r312.E12_check_names_no_file` | `src/cratekit/write/convergence_check.py` | user | 2 file(s) | 307 | 6 | killed |
| `r312.E13_record_drops_location` | `src/cratekit/write/rebuild.py` | user | 2 file(s) | 307 | 6 | killed |
| `r312.E14_listed_in_dropped` | `src/cratekit/write/rebuild.py` | user | 2 file(s) | 307 | 3 | killed |
| `r312.E2_vocal_gap_filter_off` | `src/cratekit/write/rebuild.py` | user | 2 file(s) | 307 | 1 | killed |
| `r312.E4_cap_halved` | `src/cratekit/write/rebuild.py` | user | 2 file(s) | 307 | 1 | killed |
| `r312.E5_cap_not_applied` | `src/cratekit/write/rebuild.py` | user | 2 file(s) | 307 | 1 | killed |
| `r312.E6_count_is_the_cap` | `src/cratekit/write/rebuild.py` | user | 2 file(s) | 307 | 1 | killed |
| `r312.E7_rest_not_counted` | `src/cratekit/write/rebuild.py` | user | 2 file(s) | 307 | 1 | killed |
| `r312.E8_unsorted` | `src/cratekit/write/rebuild.py` | user | 2 file(s) | 307 | 1 | killed |
| `r312.E9_row_fallback_blank` | `src/cratekit/write/rebuild.py` | user | 2 file(s) | 307 | 1 | killed |
| `r316.M10_derivation_restates_no_gap` | `src/cratekit/write/rebuild.py` | user | 2 file(s) | 307 | 9 | killed |
| `r316.M11_warning_ignores_dimension` | `src/cratekit/write/rebuild.py` | user | 1 file(s) | 197 | 8 | killed |
| `r316.M12_code_respelled` | `src/cratekit/write/rebuild.py` | user | 1 file(s) | 197 | 1 | killed |
| `r316.M8_not_derived_ignores_declaration` | `src/cratekit/write/rebuild.py` | user | 2 file(s) | 307 | 1 | killed |
| `r316.M9_not_derived_ignores_threshold` | `src/cratekit/write/rebuild.py` | user | 2 file(s) | 307 | 14 | killed |
| `u119-c.C3_uncompared_still_compared` | `src/cratekit/write/convergence_check.py` | user | 2 file(s) | 156 | 1 | killed |
| `u119-c.C4_favorites_beside_renamed_folder` | `src/cratekit/write/rebuild.py` | user | 1 file(s) | 46 | 1 | killed |
| `u119.R1_vox_unknown_by_id` | `src/cratekit/write/rebuild.py` | user | 2 file(s) | 156 | 39 | killed |
| `u119.R2_with_favorites_every_tree` | `src/cratekit/write/rebuild.py` | user | 1 file(s) | 46 | 1 | killed |
| `u132.W4_routing_tree_only` | `src/cratekit/write/rebuild.py` | user | 8 file(s) | 661 | 2 | killed |
| `u155.W1_derivation` | `src/cratekit/write/rebuild.py` | user | 10 file(s) | 736 | 7 | killed |
| `u219.A1_approved_equality` | `src/cratekit/write/rebuild.py` | user | 11 file(s) | 760 | 2 | killed |
| `u219.A2_approved_checked` | `src/cratekit/write/rebuild.py` | user | 11 file(s) | 760 | 2 | killed |
| `u219.A3_approved_passed_down` | `src/cratekit/write/rebuild.py` | user | 11 file(s) | 760 | 5 | killed |
| `u219.A4_additions_rows` | `src/cratekit/write/rebuild.py` | user | 11 file(s) | 760 | 21 | killed |
| `u219.D1_derivable_guard` | `src/cratekit/write/rebuild.py` | user | 11 file(s) | 760 | 3 | killed |
| `u219.D2_derivation_asks` | `src/cratekit/write/rebuild.py` | user | 11 file(s) | 760 | 2 | killed |
| `u219.D4_derivable_answer` | `src/cratekit/write/rebuild.py` | user | 11 file(s) | 760 | 19 | killed |
| `u219.F1_favourites_held` | `src/cratekit/write/rebuild.py` | user | 11 file(s) | 760 | 3 | killed |
| `u219.K1_accept_routing_refused` | `src/cratekit/write/rebuild.py` | user | 11 file(s) | 760 | 1 | killed |
| `u219.M1_accept_fingerprint` | `src/cratekit/write/rebuild.py` | user | 11 file(s) | 760 | 2 | killed |
| `u246.R1_rebuild_set_per_placement` | `src/cratekit/write/rebuild.py` | user | 5 file(s) | 214 | 2 | killed |
| `u246.R2_rebuild_tuple_scan` | `src/cratekit/write/rebuild.py` | user | 5 file(s) | 214 | 1 | killed |
| `u246.R3_rebuild_set_of_placements` | `src/cratekit/write/rebuild.py` | user | 5 file(s) | 378 | 5 | killed |
| `u246.R4_rebuild_membership_inverted` | `src/cratekit/write/rebuild.py` | user | 5 file(s) | 378 | 7 | killed |
| `u246.R5_rebuild_set_empty` | `src/cratekit/write/rebuild.py` | user | 5 file(s) | 378 | 2 | killed |
| `u250.M1_three_opens_again` | `src/cratekit/write/rebuild.py` | user | 3 file(s) | 209 | 49 | killed |
| `u250.M2_genre_dropped` | `src/cratekit/write/rebuild.py` | user | 3 file(s) | 209 | 39 | killed |
| `u250.M3_energy_unconverted` | `src/cratekit/write/rebuild.py` | user | 3 file(s) | 209 | 32 | killed |
| `u250.M4_vox_reads_energy` | `src/cratekit/write/rebuild.py` | user | 3 file(s) | 209 | 27 | killed |

## Row definitions

### `r745-a.E10_text_not_cleaned`

clean_text: write a control character as it is held

- File: `src/cratekit/write/collection_export.py`
- Source: `r745-a.json`, row `E10_text_not_cleaned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 7 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_character_no_document_may_carry_is_written_as_a_space_and_counted[\n]`
  - `tests/test_export_collection.py::test_a_character_no_document_may_carry_is_written_as_a_space_and_counted[\r]`
  - `tests/test_export_collection.py::test_a_character_no_document_may_carry_is_written_as_a_space_and_counted[\t]`
  - `tests/test_export_collection.py::test_a_character_no_document_may_carry_is_written_as_a_space_and_counted[\ufffe]`
  - `tests/test_export_collection.py::test_a_character_no_document_may_carry_is_written_as_a_space_and_counted[\x00]`
  - `tests/test_export_collection.py::test_a_character_no_document_may_carry_is_written_as_a_space_and_counted[\x01]`
  - `tests/test_export_collection.py::test_a_character_no_document_may_carry_is_written_as_a_space_and_counted[\x1f]`

Old text:

```
    return _NOT_ATTRIBUTE_TEXT.sub(" ", value)
```

New text:

```
    return value
```

### `r745-a.E11_any_path_encoded`

is_file_path: encode anything that is not already a location, a streamed reference included

- File: `src/cratekit/write/collection_export.py`
- Source: `r745-a.json`, row `E11_any_path_encoded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_streamed_track_is_not_dressed_as_a_file_on_this_machine`
  - `tests/test_export_collection.py::test_each_recorded_spelling_is_placed_or_left_by_the_one_resolver`

Old text:

```
    return recorded.startswith("/") and not locations.looks_like_location(recorded)
```

New text:

```
    return bool(recorded) and not locations.looks_like_location(recorded)
```

### `r745-a.E12_three_stars_moved`

STAR_BYTES: spell three stars 150, a nearby value that is not the export byte

- File: `src/cratekit/write/collection_export.py`
- Source: `r745-a.json`, row `E12_three_stars_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_row_says_what_the_database_row_says`
  - `tests/test_export_collection.py::test_each_star_count_is_spelled_as_the_export_byte`

Old text:

```
    {0: 0, 1: 51, 2: 102, 3: 153, 4: 204, 5: 255}
```

New text:

```
    {0: 0, 1: 51, 2: 102, 3: 150, 4: 204, 5: 255}
```

### `r745-a.E13_siblings_by_identifier`

_children: order siblings by identifier, ignoring the stored sequence

- File: `src/cratekit/write/collection_export.py`
- Source: `r745-a.json`, row `E13_siblings_by_identifier`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_collection.py::test_siblings_come_out_in_their_sequence_and_not_in_identifier_order`
  - `tests/test_export_collection.py::test_the_export_nests_as_the_database_nests_and_omits_what_was_deleted`

Old text:

```
        siblings.sort(key=lambda node: (node.seq, _ordinal(node.node_id), node.node_id))
```

New text:

```
        siblings.sort(key=lambda node: (_ordinal(node.node_id), node.node_id))
```

### `r745-a.E1_tombstone_row_written`

read_tracks: write a tombstoned collection row as a live one

- File: `src/cratekit/write/collection_export.py`
- Source: `r745-a.json`, row `E1_tombstone_row_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 16 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_landing_splices_into_the_file_and_the_import_is_proved_against_a_second[recorded-under-a-base-drive]`
  - `tests/test_export_collection.py::test_a_landing_splices_into_the_file_and_the_import_is_proved_against_a_second[recorded-under-the-root]`
  - `tests/test_export_collection.py::test_a_single_file_intake_splices_into_the_file[recorded-under-a-base-drive]`
  - `tests/test_export_collection.py::test_a_single_file_intake_splices_into_the_file[recorded-under-the-root]`
  - `tests/test_export_collection.py::test_each_star_count_is_spelled_as_the_export_byte`
  - `tests/test_export_collection.py::test_every_declared_count_equals_what_was_written`
  - `tests/test_export_collection.py::test_every_location_is_written_under_the_mounted_root_when_a_rule_places_it`
  - `tests/test_export_collection.py::test_no_tempo_the_database_holds_reaches_the_file[recorded-under-a-base-drive]`
  - `tests/test_export_collection.py::test_no_tempo_the_database_holds_reaches_the_file[recorded-under-the-root]`
  - `tests/test_export_collection.py::test_the_envelope_counts_a_row_left_to_its_rule`
  - `tests/test_export_collection.py::test_the_envelope_counts_what_the_file_holds_and_names_what_it_left_out`
  - `tests/test_export_collection.py::test_the_export_and_doctor_count_the_same_rows_as_under_no_rule`
  - `tests/test_export_collection.py::test_the_export_nests_as_the_database_nests_and_omits_what_was_deleted`
  - `tests/test_export_collection.py::test_the_import_proof_is_withheld_on_a_moved_library_with_no_rule`
  - `tests/test_export_collection.py::test_the_strict_reader_takes_the_file_and_sees_the_same_library`
  - ... and 1 more, see the JSON sidecar

Old text:

```
        if trees.soft_delete_marker(row):
            continue
        track_id = str(row.ID)
```

New text:

```
        track_id = str(row.ID)
```

### `r745-a.E3_tombstone_playlist_written`

read_nodes: write a tombstoned playlist as a live one

- File: `src/cratekit/write/collection_export.py`
- Source: `r745-a.json`, row `E3_tombstone_playlist_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 4 (killed)
- Killed:
  - `tests/test_export_collection.py::test_every_declared_count_equals_what_was_written`
  - `tests/test_export_collection.py::test_the_envelope_counts_what_the_file_holds_and_names_what_it_left_out`
  - `tests/test_export_collection.py::test_the_export_nests_as_the_database_nests_and_omits_what_was_deleted`
  - `tests/test_export_collection.py::test_the_strict_reader_takes_the_file_and_sees_the_same_library`

Old text:

```
        if trees.soft_delete_marker(row):
            continue
        node_id = str(row.ID)
```

New text:

```
        node_id = str(row.ID)
```

### `r745-a.E4_dangling_member_written`

_render_node: write every stored member, whether or not the collection holds it

- File: `src/cratekit/write/collection_export.py`
- Source: `r745-a.json`, row `E4_dangling_member_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 6 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_landing_splices_into_the_file_and_the_import_is_proved_against_a_second[recorded-under-a-base-drive]`
  - `tests/test_export_collection.py::test_a_landing_splices_into_the_file_and_the_import_is_proved_against_a_second[recorded-under-the-root]`
  - `tests/test_export_collection.py::test_every_declared_count_equals_what_was_written`
  - `tests/test_export_collection.py::test_the_envelope_counts_what_the_file_holds_and_names_what_it_left_out`
  - `tests/test_export_collection.py::test_the_export_nests_as_the_database_nests_and_omits_what_was_deleted`
  - `tests/test_export_collection.py::test_the_strict_reader_takes_the_file_and_sees_the_same_library`

Old text:

```
        keys = [member for member in node.members if member in live]
```

New text:

```
        keys = list(node.members)
```

### `r745-a.E5_empty_folder_self_closed`

_render_node: self close a folder with no children, as rekordbox does

- File: `src/cratekit/write/collection_export.py`
- Source: `r745-a.json`, row `E5_empty_folder_self_closed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 34 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_folder_with_nothing_in_it_has_a_body_a_landing_could_insert_into`
  - `tests/test_export_collection.py::test_a_landing_splices_into_the_file_and_the_import_is_proved_against_a_second[recorded-under-a-base-drive]`
  - `tests/test_export_collection.py::test_a_landing_splices_into_the_file_and_the_import_is_proved_against_a_second[recorded-under-the-root]`
  - `tests/test_export_collection.py::test_a_library_recorded_where_it_is_mounted_has_nothing_to_place`
  - `tests/test_export_collection.py::test_a_playlist_prune_reads_the_file_and_takes_off_only_what_left_it[recorded-under-a-base-drive]`
  - `tests/test_export_collection.py::test_a_playlist_prune_reads_the_file_and_takes_off_only_what_left_it[recorded-under-the-root]`
  - `tests/test_export_collection.py::test_a_queueing_verb_reads_the_file_and_queues_its_tracks[recorded-under-a-base-drive-favourites-sweep]`
  - `tests/test_export_collection.py::test_a_queueing_verb_reads_the_file_and_queues_its_tracks[recorded-under-a-base-drive-playlist-export]`
  - `tests/test_export_collection.py::test_a_queueing_verb_reads_the_file_and_queues_its_tracks[recorded-under-the-root-favourites-sweep]`
  - `tests/test_export_collection.py::test_a_queueing_verb_reads_the_file_and_queues_its_tracks[recorded-under-the-root-playlist-export]`
  - `tests/test_export_collection.py::test_a_rating_on_neither_scale_is_written_unrated_and_said_so`
  - `tests/test_export_collection.py::test_a_row_says_what_the_database_row_says`
  - `tests/test_export_collection.py::test_a_single_file_intake_splices_into_the_file[recorded-under-a-base-drive]`
  - `tests/test_export_collection.py::test_a_single_file_intake_splices_into_the_file[recorded-under-the-root]`
  - `tests/test_export_collection.py::test_an_ampersand_a_quote_and_an_accent_survive_the_readers`
  - ... and 19 more, see the JSON sidecar

Old text:

```
    return rbxml.folder_open(name, len(body), indent) + "".join(body) + rbxml.node_close(indent)
```

New text:

```
    if not body:
        return rbxml.folder_open(name, 0, indent).replace(">\\r\\n", "/>\\r\\n")
    return rbxml.folder_open(name, len(body), indent) + "".join(body) + rbxml.node_close(indent)
```

### `r745-a.E6_tempo_constant_moved`

track_element: write a real tempo in place of the gridless constant

- File: `src/cratekit/write/collection_export.py`
- Source: `r745-a.json`, row `E6_tempo_constant_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`, `tests/test_no_beatgrid_ever.py`
- Collected: 129 against a baseline of 129
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_collection.py::test_no_tempo_the_database_holds_reaches_the_file[recorded-under-a-base-drive]`
  - `tests/test_export_collection.py::test_no_tempo_the_database_holds_reaches_the_file[recorded-under-the-root]`

Old text:

```
AverageBpm="0.00"
```

New text:

```
AverageBpm="98.76"
```

### `r745-a.E7_identifier_not_held_to_digits`

refuse_unusable_id: accept any identifier

- File: `src/cratekit/write/collection_export.py`
- Source: `r745-a.json`, row `E7_identifier_not_held_to_digits`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_collection.py::test_an_identifier_that_is_not_digits_is_refused_and_nothing_is_written`
  - `tests/test_export_collection.py::test_an_identifier_the_readers_would_lose_is_refused_by_the_emitter[handed-straight-to-the-emitter-not-digits]`

Old text:

```
    if identifier.isascii() and identifier.isdigit():
        return
```

New text:

```
    if True:
        return
```

### `r745-a.E8_duplicate_identifier_written`

render: write one identifier twice

- File: `src/cratekit/write/collection_export.py`
- Source: `r745-a.json`, row `E8_duplicate_identifier_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_an_identifier_the_readers_would_lose_is_refused_by_the_emitter[held-twice]`

Old text:

```
        if track.track_id in seen:
```

New text:

```
        if False:
```

### `r745-a.E9_smart_playlist_written`

_writable: write a smart playlist, as a node of a kind no reader classifies as a playlist

- File: `src/cratekit/write/collection_export.py`
- Source: `r745-a.json`, row `E9_smart_playlist_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 3 (killed)
- Killed:
  - `tests/test_export_collection.py::test_every_declared_count_equals_what_was_written`
  - `tests/test_export_collection.py::test_the_envelope_counts_what_the_file_holds_and_names_what_it_left_out`
  - `tests/test_export_collection.py::test_the_export_nests_as_the_database_nests_and_omits_what_was_deleted`

Old text:

```
    return [node for node in nodes if node.attribute in (PLAYLIST_ATTRIBUTE, FOLDER_ATTRIBUTE)]
```

New text:

```
    return [
        node
        for node in nodes
        if node.attribute in (PLAYLIST_ATTRIBUTE, FOLDER_ATTRIBUTE, SMART_ATTRIBUTE)
    ]
```

### `r745-b.E14_members_as_they_arrive`

read_nodes: keep members in the order the rows arrive, not the stored order

- File: `src/cratekit/write/collection_export.py`
- Source: `r745-b.json`, row `E14_members_as_they_arrive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_members_come_out_in_their_stored_order_whatever_order_the_rows_arrive_in`

Old text:

```
sorted(members.get(node_id, ()))
```

New text:

```
members.get(node_id, ())
```

### `r745-b.E15_unreadable_kind_is_a_playlist`

_attribute: answer the playlist code for a kind that cannot be parsed

- File: `src/cratekit/write/collection_export.py`
- Source: `r745-b.json`, row `E15_unreadable_kind_is_a_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 3 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_kind_that_cannot_be_read_is_never_written_as_a_playlist[2.5j]`
  - `tests/test_export_collection.py::test_a_kind_that_cannot_be_read_is_never_written_as_a_playlist[]`
  - `tests/test_export_collection.py::test_a_kind_that_cannot_be_read_is_never_written_as_a_playlist[folder]`

Old text:

```
    try:
        return int(value)
    except (TypeError, ValueError):
        return UNREADABLE_ATTRIBUTE
```

New text:

```
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0
```

### `r745-b.E16_lookups_not_primed`

read_tracks: read no lookup table ahead of the rows

- File: `src/cratekit/write/collection_export.py`
- Source: `r745-b.json`, row `E16_lookups_not_primed`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_the_lookup_tables_are_read_once_each_and_not_once_per_row`

Old text:

```
    held = _prime_lookups(db)
```

New text:

```
    held = []
```

### `r745-b.E17_provenance_read_anywhere`

provenance_of: read the line anywhere in the file, not only ahead of the document element

- File: `src/cratekit/write/collection_export.py`
- Source: `r745-b.json`, row `E17_provenance_read_anywhere`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_comment_inside_the_document_does_not_answer_for_the_file`

Old text:

```
    head = content[: max(0, content.find(b"<DJ_PLAYLISTS"))]
```

New text:

```
    head = content
```

### `r745-c.E2_tombstone_membership_written`

read_nodes: keep a tombstoned membership row. Measured again after the test its zero bought

- File: `src/cratekit/write/collection_export.py`
- Source: `r745-c.json`, row `E2_tombstone_membership_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_membership_somebody_removed_is_not_written_back_into_the_playlist`
  - `tests/test_export_collection.py::test_a_membership_that_cannot_say_whether_it_was_removed_refuses`

Old text:

```
        if trees.soft_delete_marker(song):
            continue
```

New text:

```
        if False:
            continue
```

### `r773-a.M10_unmapped_rows_not_collected`

render: collect no row under no rule, the prefix still counted

- File: `src/cratekit/write/collection_export.py`
- Source: `r773-a.json`, row `M10_unmapped_rows_not_collected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 4 (killed)
- Killed:
  - `tests/test_export_collection.py::test_each_recorded_spelling_is_placed_or_left_by_the_one_resolver`
  - `tests/test_export_collection.py::test_the_export_and_doctor_count_the_same_rows_as_under_no_rule`
  - `tests/test_export_collection.py::test_the_import_proof_is_withheld_on_a_moved_library_with_no_rule`
  - `tests/test_export_collection.py::test_with_no_rule_each_location_is_written_as_the_database_holds_it_and_counted`

Old text:

```
            unmapped.append(track.track_id)
```

New text:

```
            pass
```

### `r773-a.M11_prefixes_least_rows_first`

render: order the prefixes with the fewest rows first

- File: `src/cratekit/write/collection_export.py`
- Source: `r773-a.json`, row `M11_prefixes_least_rows_first`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_each_recorded_spelling_is_placed_or_left_by_the_one_resolver`

Old text:

```
            unmapped_prefixes=tuple(prefixes.most_common()),
```

New text:

```
            unmapped_prefixes=tuple(reversed(prefixes.most_common())),
```

### `r773-a.M1_read_back_not_asked`

mounted_location: rewrite a row wherever a rule sends it, without asking whether the place reads back as itself

- File: `src/cratekit/write/collection_export.py`
- Source: `r773-a.json`, row `M1_read_back_not_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 4 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_rule_onto_a_second_volume_is_left_to_the_reader_that_follows_it`
  - `tests/test_export_collection.py::test_a_rule_places_a_row_only_where_it_reads_back_as_itself[moved-again]`
  - `tests/test_export_collection.py::test_a_rule_places_a_row_only_where_it_reads_back_as_itself[target-not-a-path]`
  - `tests/test_export_collection.py::test_the_envelope_counts_a_row_left_to_its_rule`

Old text:

```
        if read_back.path == resolved.path:
```

New text:

```
        if True:
```

### `r773-a.M2_unmapped_not_told_apart`

mounted_location: answer a row under no rule as recorded, so nothing counts it

- File: `src/cratekit/write/collection_export.py`
- Source: `r773-a.json`, row `M2_unmapped_not_told_apart`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 4 (killed)
- Killed:
  - `tests/test_export_collection.py::test_each_recorded_spelling_is_placed_or_left_by_the_one_resolver`
  - `tests/test_export_collection.py::test_the_export_and_doctor_count_the_same_rows_as_under_no_rule`
  - `tests/test_export_collection.py::test_the_import_proof_is_withheld_on_a_moved_library_with_no_rule`
  - `tests/test_export_collection.py::test_with_no_rule_each_location_is_written_as_the_database_holds_it_and_counted`

Old text:

```
        return Mounted(recorded, Mounting.UNDER_NO_RULE, prefix=resolved.prefix)
```

New text:

```
        return Mounted(recorded, Mounting.AS_RECORDED)
```

### `r773-a.M3_placed_row_written_as_recorded`

mounted_location: count a placed row and hand back the recorded spelling, which is the finding itself

- File: `src/cratekit/write/collection_export.py`
- Source: `r773-a.json`, row `M3_placed_row_written_as_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 5 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_landing_splices_into_the_file_and_the_import_is_proved_against_a_second[recorded-under-a-base-drive]`
  - `tests/test_export_collection.py::test_a_rule_places_a_row_only_where_it_reads_back_as_itself[onto-itself]`
  - `tests/test_export_collection.py::test_each_recorded_spelling_is_placed_or_left_by_the_one_resolver`
  - `tests/test_export_collection.py::test_every_location_is_written_under_the_mounted_root_when_a_rule_places_it`
  - `tests/test_export_collection.py::test_the_rules_are_walked_in_the_order_they_were_recorded`

Old text:

```
            return Mounted(resolved.path, Mounting.PLACED)
```

New text:

```
            return Mounted(recorded, Mounting.PLACED)
```

### `r773-a.M4_emitter_handed_the_rows_as_read`

render: emit the rows as read and not the rows as placed

- File: `src/cratekit/write/collection_export.py`
- Source: `r773-a.json`, row `M4_emitter_handed_the_rows_as_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 5 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_landing_splices_into_the_file_and_the_import_is_proved_against_a_second[recorded-under-a-base-drive]`
  - `tests/test_export_collection.py::test_a_rule_places_a_row_only_where_it_reads_back_as_itself[onto-itself]`
  - `tests/test_export_collection.py::test_each_recorded_spelling_is_placed_or_left_by_the_one_resolver`
  - `tests/test_export_collection.py::test_every_location_is_written_under_the_mounted_root_when_a_rule_places_it`
  - `tests/test_export_collection.py::test_the_rules_are_walked_in_the_order_they_were_recorded`

Old text:

```
        + "".join(track_element(track) for track in placed)
```

New text:

```
        + "".join(track_element(track) for track in tracks)
```

### `r773-a.M5_another_host_not_caught`

mounted_location: catch a different error, so a location naming another host ends the export

- File: `src/cratekit/write/collection_export.py`
- Source: `r773-a.json`, row `M5_another_host_not_caught`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_each_recorded_spelling_is_placed_or_left_by_the_one_resolver`

Old text:

```
    except locations.LocationDecodeError:
        return Mounted(recorded, Mounting.AS_RECORDED)
```

New text:

```
    except KeyError:
        return Mounted(recorded, Mounting.AS_RECORDED)
```

### `r773-a.M6_left_row_counted_as_under_no_rule`

mounted_location: answer a row left to its rule as under no rule, which is where doctor and the export disagreed

- File: `src/cratekit/write/collection_export.py`
- Source: `r773-a.json`, row `M6_left_row_counted_as_under_no_rule`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 4 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_rule_onto_a_second_volume_is_left_to_the_reader_that_follows_it`
  - `tests/test_export_collection.py::test_a_rule_places_a_row_only_where_it_reads_back_as_itself[moved-again]`
  - `tests/test_export_collection.py::test_a_rule_places_a_row_only_where_it_reads_back_as_itself[target-not-a-path]`
  - `tests/test_export_collection.py::test_the_envelope_counts_a_row_left_to_its_rule`

Old text:

```
        return Mounted(recorded, Mounting.LEFT_TO_ITS_RULE)
```

New text:

```
        return Mounted(recorded, Mounting.UNDER_NO_RULE)
```

### `r773-a.M7_prefixes_not_carried`

render: carry no leading prefix for the rows under no rule

- File: `src/cratekit/write/collection_export.py`
- Source: `r773-a.json`, row `M7_prefixes_not_carried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_collection.py::test_each_recorded_spelling_is_placed_or_left_by_the_one_resolver`
  - `tests/test_export_collection.py::test_with_no_rule_each_location_is_written_as_the_database_holds_it_and_counted`

Old text:

```
            unmapped_prefixes=tuple(prefixes.most_common()),
```

New text:

```
            unmapped_prefixes=(),
```

### `r773-a.M8_placed_rows_not_counted`

render: count no placed row

- File: `src/cratekit/write/collection_export.py`
- Source: `r773-a.json`, row `M8_placed_rows_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 4 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_rule_places_a_row_only_where_it_reads_back_as_itself[onto-itself]`
  - `tests/test_export_collection.py::test_each_recorded_spelling_is_placed_or_left_by_the_one_resolver`
  - `tests/test_export_collection.py::test_every_location_is_written_under_the_mounted_root_when_a_rule_places_it`
  - `tests/test_export_collection.py::test_the_rules_are_walked_in_the_order_they_were_recorded`

Old text:

```
            remapped += 1
```

New text:

```
            remapped += 0
```

### `r773-a.M9_left_rows_not_collected`

render: collect no row left to its rule

- File: `src/cratekit/write/collection_export.py`
- Source: `r773-a.json`, row `M9_left_rows_not_collected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 4 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_rule_onto_a_second_volume_is_left_to_the_reader_that_follows_it`
  - `tests/test_export_collection.py::test_a_rule_places_a_row_only_where_it_reads_back_as_itself[moved-again]`
  - `tests/test_export_collection.py::test_a_rule_places_a_row_only_where_it_reads_back_as_itself[target-not-a-path]`
  - `tests/test_export_collection.py::test_the_envelope_counts_a_row_left_to_its_rule`

Old text:

```
            left.append(track.track_id)
```

New text:

```
            pass
```

### `r773-a.S1_streamed_row_encoded_as_a_file`

is_file_path, existing: take any value that is not a location as a path, a streamed track and an empty one included

- File: `src/cratekit/write/collection_export.py`
- Source: `r773-a.json`, row `S1_streamed_row_encoded_as_a_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 5 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_streamed_track_is_not_dressed_as_a_file_on_this_machine`
  - `tests/test_export_collection.py::test_each_recorded_spelling_is_placed_or_left_by_the_one_resolver`
  - `tests/test_export_collection.py::test_every_location_is_written_under_the_mounted_root_when_a_rule_places_it`
  - `tests/test_export_collection.py::test_the_envelope_counts_what_the_file_holds_and_names_what_it_left_out`
  - `tests/test_export_collection.py::test_with_no_rule_each_location_is_written_as_the_database_holds_it_and_counted`

Old text:

```
    return recorded.startswith("/") and not locations.looks_like_location(recorded)
```

New text:

```
    return not locations.looks_like_location(recorded)
```

### `r773-a.S2_tombstoned_row_written`

read_tracks, existing: write a tombstoned collection row

- File: `src/cratekit/write/collection_export.py`
- Source: `r773-a.json`, row `S2_tombstoned_row_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 16 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_landing_splices_into_the_file_and_the_import_is_proved_against_a_second[recorded-under-a-base-drive]`
  - `tests/test_export_collection.py::test_a_landing_splices_into_the_file_and_the_import_is_proved_against_a_second[recorded-under-the-root]`
  - `tests/test_export_collection.py::test_a_single_file_intake_splices_into_the_file[recorded-under-a-base-drive]`
  - `tests/test_export_collection.py::test_a_single_file_intake_splices_into_the_file[recorded-under-the-root]`
  - `tests/test_export_collection.py::test_each_star_count_is_spelled_as_the_export_byte`
  - `tests/test_export_collection.py::test_every_declared_count_equals_what_was_written`
  - `tests/test_export_collection.py::test_every_location_is_written_under_the_mounted_root_when_a_rule_places_it`
  - `tests/test_export_collection.py::test_no_tempo_the_database_holds_reaches_the_file[recorded-under-a-base-drive]`
  - `tests/test_export_collection.py::test_no_tempo_the_database_holds_reaches_the_file[recorded-under-the-root]`
  - `tests/test_export_collection.py::test_the_envelope_counts_a_row_left_to_its_rule`
  - `tests/test_export_collection.py::test_the_envelope_counts_what_the_file_holds_and_names_what_it_left_out`
  - `tests/test_export_collection.py::test_the_export_and_doctor_count_the_same_rows_as_under_no_rule`
  - `tests/test_export_collection.py::test_the_export_nests_as_the_database_nests_and_omits_what_was_deleted`
  - `tests/test_export_collection.py::test_the_import_proof_is_withheld_on_a_moved_library_with_no_rule`
  - `tests/test_export_collection.py::test_the_strict_reader_takes_the_file_and_sees_the_same_library`
  - ... and 1 more, see the JSON sidecar

Old text:

```
        if trees.soft_delete_marker(row):
            continue
        track_id = str(row.ID)
```

New text:

```
        if False:
            continue
        track_id = str(row.ID)
```

### `r773-a.S3_not_a_file_count_inverted`

render, existing: count the rows that do name a file as the ones that do not

- File: `src/cratekit/write/collection_export.py`
- Source: `r773-a.json`, row `S3_not_a_file_count_inverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 4 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_streamed_track_is_not_dressed_as_a_file_on_this_machine`
  - `tests/test_export_collection.py::test_each_recorded_spelling_is_placed_or_left_by_the_one_resolver`
  - `tests/test_export_collection.py::test_the_envelope_counts_what_the_file_holds_and_names_what_it_left_out`
  - `tests/test_export_collection.py::test_with_no_rule_each_location_is_written_as_the_database_holds_it_and_counted`

Old text:

```
    unlocated = tuple(track.track_id for track in tracks if not is_located(track.location))
```

New text:

```
    unlocated = tuple(track.track_id for track in tracks if is_located(track.location))
```

### `r414.M10_skip_reason_reworded`

Reword the zero band's skip reason to the uncut reason

- File: `src/cratekit/write/metadata.py`
- Source: `r414.json`, row `M10_skip_reason_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`, `tests/test_whitelist_membership.py`
- Collected: 116 against a baseline of 116
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_policy.py::test_a_cut_that_declares_zero_skips_its_band_and_keeps_the_rest`

Old text:

```
"level-unrated"
```

New text:

```
"level-uncut"
```

### `r414.M11_byte_table_off_by_one`

Realistic nearby value in the byte table, 204 folds to three stars

- File: `src/cratekit/write/metadata.py`
- Source: `r414.json`, row `M11_byte_table_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`, `tests/test_whitelist_membership.py`
- Collected: 116 against a baseline of 116
- Kills: 3 (killed)
- Killed:
  - `tests/test_metadata_policy.py::test_a_curve_already_on_the_star_scale_passes_through`
  - `tests/test_metadata_policy.py::test_a_cut_that_declares_zero_skips_its_band_and_keeps_the_rest`
  - `tests/test_metadata_policy.py::test_the_shipped_curve_plans_one_to_five_stars_for_the_database`

Old text:

```
204: 4,
```

New text:

```
204: 3,
```

### `r414.M12_detail_key_renamed`

The refusal detail names the offending value under a different key

- File: `src/cratekit/write/metadata.py`
- Source: `r414.json`, row `M12_detail_key_renamed`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`, `tests/test_whitelist_membership.py`
- Collected: 116 against a baseline of 116
- Kills: 5 (killed)
- Killed:
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[-1]`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[20]`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[256]`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[50]`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[6]`

Old text:

```
            {"rating": value},
```

New text:

```
            {"value": value},
```

### `r414.M13_remedy_swapped`

The refusal carries the doctor token instead of the configuration token

- File: `src/cratekit/write/metadata.py`
- Source: `r414.json`, row `M13_remedy_swapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`, `tests/test_whitelist_membership.py`
- Collected: 116 against a baseline of 116
- Kills: 5 (killed)
- Killed:
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[-1]`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[20]`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[256]`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[50]`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[6]`

Old text:

```
        remedy=Remedy.FIX_CONFIG_VALUES,
        scope=Scope.RUN,
        origin=("write", "metadata"),
        detail=dict(detail),
```

New text:

```
        remedy=Remedy.RUN_DOCTOR,
        scope=Scope.RUN,
        origin=("write", "metadata"),
        detail=dict(detail),
```

### `r414.M1_planner_writes_the_byte`

The planner writes the cut's export value instead of the folded star, which is R-414 itself

- File: `src/cratekit/write/metadata.py`
- Source: `r414.json`, row `M1_planner_writes_the_byte`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`, `tests/test_whitelist_membership.py`
- Collected: 116 against a baseline of 116
- Kills: 3 (killed)
- Killed:
  - `tests/test_metadata_policy.py::test_a_cut_that_declares_zero_skips_its_band_and_keeps_the_rest`
  - `tests/test_metadata_policy.py::test_a_rating_backfill_fills_an_empty_rating_with_a_star_not_a_byte`
  - `tests/test_metadata_policy.py::test_the_shipped_curve_plans_one_to_five_stars_for_the_database`

Old text:

```
        stars = curve[rating]
```

New text:

```
        stars = rating
```

### `r414.M2_fold_returns_the_byte`

database_stars returns the value it was given instead of the star it folds to

- File: `src/cratekit/write/metadata.py`
- Source: `r414.json`, row `M2_fold_returns_the_byte`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`, `tests/test_whitelist_membership.py`
- Collected: 116 against a baseline of 116
- Kills: 4 (killed)
- Killed:
  - `tests/test_metadata_policy.py::test_a_cut_that_declares_zero_skips_its_band_and_keeps_the_rest`
  - `tests/test_metadata_policy.py::test_a_rating_backfill_fills_an_empty_rating_with_a_star_not_a_byte`
  - `tests/test_metadata_policy.py::test_the_export_scale_is_what_rating_for_still_answers`
  - `tests/test_metadata_policy.py::test_the_shipped_curve_plans_one_to_five_stars_for_the_database`

Old text:

```
    return stars


def _database_curve(
```

New text:

```
    return value


def _database_curve(
```

### `r414.M3_unknown_value_not_refused`

Drop the refusal for a value on neither scale, so database_stars returns None

- File: `src/cratekit/write/metadata.py`
- Source: `r414.json`, row `M3_unknown_value_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`, `tests/test_whitelist_membership.py`
- Collected: 116 against a baseline of 116
- Kills: 5 (killed)
- Killed:
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[-1]`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[20]`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[256]`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[50]`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[6]`

Old text:

```
    if stars is None:
        raise _scale_unknown(
```

New text:

```
    if False:
        raise _scale_unknown(
```

### `r414.M4_star_passthrough_dropped`

A value already on the star scale is no longer passed through, so a star curve refuses

- File: `src/cratekit/write/metadata.py`
- Source: `r414.json`, row `M4_star_passthrough_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`, `tests/test_whitelist_membership.py`
- Collected: 116 against a baseline of 116
- Kills: 2 (killed)
- Killed:
  - `tests/test_metadata_policy.py::test_a_curve_already_on_the_star_scale_passes_through`
  - `tests/test_metadata_policy.py::test_a_curve_mixing_the_two_scales_is_refused_at_plan_time`

Old text:

```
    if value == 0 or value in _DATABASE_STARS:
```

New text:

```
    if value == 0:
```

### `r414.M5_zero_passthrough_dropped`

Zero is no longer answered as zero, so a curve with an unrated band refuses the whole plan

- File: `src/cratekit/write/metadata.py`
- Source: `r414.json`, row `M5_zero_passthrough_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`, `tests/test_whitelist_membership.py`
- Collected: 116 against a baseline of 116
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_policy.py::test_a_cut_that_declares_zero_skips_its_band_and_keeps_the_rest`

Old text:

```
    if value == 0 or value in _DATABASE_STARS:
```

New text:

```
    if value in _DATABASE_STARS:
```

### `r414.M6_mixed_scale_not_refused`

Drop the mixed scale refusal in _database_curve

- File: `src/cratekit/write/metadata.py`
- Source: `r414.json`, row `M6_mixed_scale_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`, `tests/test_whitelist_membership.py`
- Collected: 116 against a baseline of 116
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_policy.py::test_a_curve_mixing_the_two_scales_is_refused_at_plan_time`

Old text:

```
    if bytes_ and stars:
```

New text:

```
    if False:
```

### `r414.M7_mixed_scale_needs_two_stars`

Nearby value, a mix is refused only when two or more star values sit beside the bytes

- File: `src/cratekit/write/metadata.py`
- Source: `r414.json`, row `M7_mixed_scale_needs_two_stars`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`, `tests/test_whitelist_membership.py`
- Collected: 116 against a baseline of 116
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_policy.py::test_a_curve_mixing_the_two_scales_is_refused_at_plan_time`

Old text:

```
    if bytes_ and stars:
```

New text:

```
    if bytes_ and len(stars) > 1:
```

### `r414.M8_curve_checked_lazily`

The curve is folded only over values it recognises, so a bad cut refuses only the rows landing in it, not the plan

- File: `src/cratekit/write/metadata.py`
- Source: `r414.json`, row `M8_curve_checked_lazily`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`, `tests/test_whitelist_membership.py`
- Collected: 116 against a baseline of 116
- Kills: 5 (killed)
- Killed:
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[-1]`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[20]`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[256]`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[50]`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[6]`

Old text:

```
    curve = _database_curve(cuts)
```

New text:

```
    curve = _database_curve(
        [c for c in cuts if c.rating == 0 or c.rating in _DATABASE_STARS or c.rating in _EXPORT_BYTE_STARS]
    )
```

### `r414.M9_zero_band_planned`

Drop the level-unrated skip, so a zero cut plans a zero rating as a change

- File: `src/cratekit/write/metadata.py`
- Source: `r414.json`, row `M9_zero_band_planned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`, `tests/test_whitelist_membership.py`
- Collected: 116 against a baseline of 116
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_policy.py::test_a_cut_that_declares_zero_skips_its_band_and_keeps_the_rest`

Old text:

```
        if stars == 0:
```

New text:

```
        if False:
```

### `r816-e.D1_resolve_once`

plan_genre_retag: ask the database for the lookup row once per row

- File: `src/cratekit/write/metadata.py`
- Source: `r816-e.json`, row `D1_resolve_once`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`, `tests/test_metadata_policy.py`, `tests/test_genre_retag.py`
- Collected: 169 against a baseline of 169
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_each_distinct_file_word_is_resolved_once`

Old text:

```
        if wanted not in resolved:
```

New text:

```
        if True:
```

### `u163.W17_first_active`

first_active_id: take the first row, tombstone or not

- File: `src/cratekit/write/metadata.py`
- Source: `u163.json`, row `W17_first_active`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 294 against a baseline of 294
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_a_tombstoned_namesake_is_skipped_for_the_active_row_after_it`
  - `tests/test_intake_land_words.py::test_a_word_whose_only_namesake_is_a_tombstone_is_minted`

Old text:

```
        if not marker:
            return row.ID
```

New text:

```
        return row.ID
```

### `u40-author-full.F2_genre_unknown_silent`

First caller sample: drop the genre-unknown skip, so an unresolvable answer disappears from the plan

- File: `src/cratekit/write/metadata.py`
- Source: `u40-author-full.json`, row `F2_genre_unknown_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`
- Collected: 97 against a baseline of 97
- Kills: 4 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_genre_the_library_has_never_seen_is_skipped_and_surfaced`
  - `tests/test_genre_retag.py::test_a_soft_deleted_genre_is_invisible_through_the_shipped_reader`
  - `tests/test_metadata_policy.py::test_a_genre_with_no_lookup_row_is_skipped_and_surfaced`
  - `tests/test_metadata_policy.py::test_an_unreadable_marker_is_not_collapsed_into_the_genre_unknown_skip`

Old text:

```
        if genre_id is None:
            skipped.append(Skipped(content_id, "genre-unknown", wanted))
            continue
```

New text:

```
        if genre_id is None:
            continue
```

### `u40-author-full.F3_policy_owns_more`

First caller sample: widen the RETAG_GENRE policy to a second column

- File: `src/cratekit/write/metadata.py`
- Source: `u40-author-full.json`, row `F3_policy_owns_more`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`
- Collected: 97 against a baseline of 97
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_the_apply_refuses_a_field_the_retag_policy_does_not_own`
  - `tests/test_genre_retag.py::test_the_retag_operation_owns_the_genre_column_and_nothing_else`

Old text:

```
            fields=MappingProxyType({"GenreID": rb_writer.Ownership.OWNED}),
```

New text:

```
            fields=MappingProxyType(
                {"GenreID": rb_writer.Ownership.OWNED, "Rating": rb_writer.Ownership.OWNED}
            ),
```

### `u59.M1_permissive_default`

Restore the permissive default: an unreadable marker reads as active

- File: `src/cratekit/write/metadata.py`
- Source: `u59.json`, row `M1_permissive_default`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`
- Collected: 97 against a baseline of 97
- Kills: 3 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_an_unreadable_marker_stops_the_run_rather_than_skipping_one_row`
  - `tests/test_metadata_policy.py::test_a_genre_row_that_cannot_report_the_marker_refuses_rather_than_resolving`
  - `tests/test_metadata_policy.py::test_an_unreadable_marker_is_not_collapsed_into_the_genre_unknown_skip`

Old text:

```
        marker = getattr(row, rb_writer.SOFT_DELETE_COLUMN, _MARKER_ABSENT)
```

New text:

```
        marker = getattr(row, rb_writer.SOFT_DELETE_COLUMN, 0)
```

### `u59.M2_refusal_removed`

Delete the refusal entirely, so an absent marker falls through as falsey

- File: `src/cratekit/write/metadata.py`
- Source: `u59.json`, row `M2_refusal_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`
- Collected: 97 against a baseline of 97
- Kills: 4 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_an_unreadable_marker_stops_the_run_rather_than_skipping_one_row`
  - `tests/test_metadata_policy.py::test_a_genre_row_that_cannot_report_the_marker_refuses_rather_than_resolving`
  - `tests/test_metadata_policy.py::test_an_explicit_none_marker_refuses_alongside_a_missing_attribute`
  - `tests/test_metadata_policy.py::test_an_unreadable_marker_is_not_collapsed_into_the_genre_unknown_skip`

Old text:

```
        if marker is _MARKER_ABSENT or marker is None:
```

New text:

```
        if False:
```

### `u59.M3_none_admitted`

Stop refusing an explicit None; bool(None) is the same permissive answer

- File: `src/cratekit/write/metadata.py`
- Source: `u59.json`, row `M3_none_admitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_policy.py::test_an_explicit_none_marker_refuses_alongside_a_missing_attribute`

Old text:

```
        if marker is _MARKER_ABSENT or marker is None:
```

New text:

```
        if marker is _MARKER_ABSENT:
```

### `u59.M4_tombstone_resolves`

Invert the active test, so a soft-deleted genre is the one that resolves

- File: `src/cratekit/write/metadata.py`
- Source: `u59.json`, row `M4_tombstone_resolves`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`
- Collected: 97 against a baseline of 97
- Kills: 10 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_live_namesake_behind_a_tombstone_is_still_found_through_the_reader`
  - `tests/test_genre_retag.py::test_a_soft_deleted_genre_is_invisible_through_the_shipped_reader`
  - `tests/test_genre_retag.py::test_a_soft_deleted_namesake_does_not_mask_the_live_genre_row`
  - `tests/test_genre_retag.py::test_a_written_file_is_relinked_to_the_existing_genre_row`
  - `tests/test_genre_retag.py::test_an_unregistered_operation_writes_nothing_and_the_apply_is_what_prevents_it`
  - `tests/test_genre_retag.py::test_re_applying_a_plan_over_an_already_linked_row_is_a_no_op`
  - `tests/test_metadata_policy.py::test_a_deleted_marker_is_not_an_error_here_the_way_it_is_for_a_track`
  - `tests/test_metadata_policy.py::test_a_genre_that_exists_is_linked_by_identifier`
  - `tests/test_metadata_policy.py::test_a_genre_whose_only_row_is_soft_deleted_resolves_to_nothing`
  - `tests/test_metadata_policy.py::test_a_soft_deleted_namesake_does_not_mask_the_live_genre_row`

Old text:

```
        if not marker:
            return row.ID
```

New text:

```
        if marker:
            return row.ID
```

### `u59.M5_first_row_wins`

Return the first row rather than the first ACTIVE one, ending the loop

- File: `src/cratekit/write/metadata.py`
- Source: `u59.json`, row `M5_first_row_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`
- Collected: 97 against a baseline of 97
- Kills: 6 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_live_namesake_behind_a_tombstone_is_still_found_through_the_reader`
  - `tests/test_genre_retag.py::test_a_soft_deleted_genre_is_invisible_through_the_shipped_reader`
  - `tests/test_genre_retag.py::test_a_soft_deleted_namesake_does_not_mask_the_live_genre_row`
  - `tests/test_metadata_policy.py::test_a_deleted_marker_is_not_an_error_here_the_way_it_is_for_a_track`
  - `tests/test_metadata_policy.py::test_a_genre_whose_only_row_is_soft_deleted_resolves_to_nothing`
  - `tests/test_metadata_policy.py::test_a_soft_deleted_namesake_does_not_mask_the_live_genre_row`

Old text:

```
        if not marker:
            return row.ID
    return None
```

New text:

```
        return row.ID
    return None
```

### `u59.M6_reason_reworded`

Reword the refusal reason, which the plan and the report both key on

- File: `src/cratekit/write/metadata.py`
- Source: `u59.json`, row `M6_reason_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`
- Collected: 97 against a baseline of 97
- Kills: 4 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_an_unreadable_marker_stops_the_run_rather_than_skipping_one_row`
  - `tests/test_metadata_policy.py::test_a_genre_row_that_cannot_report_the_marker_refuses_rather_than_resolving`
  - `tests/test_metadata_policy.py::test_an_explicit_none_marker_refuses_alongside_a_missing_attribute`
  - `tests/test_metadata_policy.py::test_an_unreadable_marker_is_not_collapsed_into_the_genre_unknown_skip`

Old text:

```
                "soft-delete-marker-unreadable",
```

New text:

```
                "soft-delete-marker-unknown",
```

### `r239-b.S7_metadata_key_off`

mytags' open passes unlock=False

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r239-b.json`, row `S7_metadata_key_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_adopt_apply_cli.py`
- Collected: 733 against a baseline of 733
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_no_caller_in_src_answers_the_key_question_for_itself`

Old text:

```
        require_closed=writing,
        cfg=cfg,

```

New text:

```
        require_closed=writing,
        unlock=False,
        cfg=cfg,

```

### `r342.E1_cut_inclusive`

Existing guard sample: the with-vox cut becomes exclusive

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r342.json`, row `E1_cut_inclusive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_vocal_tag_values_are_empty_below_the_cut`

Old text:

```
if voxlevel is None or voxlevel < cut:
```

New text:

```
if voxlevel is None or voxlevel <= cut:
```

### `r342.V13_detail_key`

Rename the calibration detail key the refusal carries

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r342.json`, row `V13_detail_key`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 10 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[boolean]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[empty]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[infinity]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[list]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[nan]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[no-key]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[null]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[overflow]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[text]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[truncated]`

Old text:

```
detail={"calibration": str(path), "kind": type(exc).__name__},
```

New text:

```
detail={"path": str(path), "kind": type(exc).__name__},
```

### `r342.V1_default_on_corrupt`

Restore the defect: an unreadable calibration returns the default cut instead of refusing

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r342.json`, row `V1_default_on_corrupt`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 12 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_a_corrupt_vocal_calibration_refuses_through_the_verb_and_writes_nothing`
  - `tests/test_metadata_cli.py::test_a_vocal_calibration_this_account_cannot_read_refuses`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[boolean]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[empty]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[infinity]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[list]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[nan]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[no-key]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[null]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[overflow]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[text]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[truncated]`

Old text:

```
    except (OSError, ValueError, KeyError, TypeError, OverflowError) as exc:
        raise refuse(

```

New text:

```
    except (OSError, ValueError, KeyError, TypeError, OverflowError) as exc:
        return DEFAULT_VOCAL_THRESHOLD
        raise refuse(

```

### `r342.V2_no_finite_check`

Drop the finiteness check, so NaN and Infinity read as a cut

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r342.json`, row `V2_no_finite_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 2 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[infinity]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[nan]`

Old text:

```
        if not math.isfinite(threshold):
            raise ValueError(f"threshold {threshold} is not a finite number")

```

New text:

```
(empty)
```

### `r342.V3_isnan_for_isfinite`

Nearby value: check only for NaN, so Infinity reads as a cut

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r342.json`, row `V3_isnan_for_isfinite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[infinity]`

Old text:

```
if not math.isfinite(threshold):
```

New text:

```
if math.isnan(threshold):
```

### `r342.V4_no_bool_check`

Drop the boolean check, so true reads as a cut of 1.0

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r342.json`, row `V4_no_bool_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[boolean]`

Old text:

```
        if isinstance(raw, bool):
            raise TypeError(f"threshold {raw} is a boolean, not a number")

```

New text:

```
(empty)
```

### `r342.V5_tuple_drops_overflow`

Drop OverflowError from the except tuple, the review's finding

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r342.json`, row `V5_tuple_drops_overflow`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[overflow]`

Old text:

```
except (OSError, ValueError, KeyError, TypeError, OverflowError) as exc:
```

New text:

```
except (OSError, ValueError, KeyError, TypeError) as exc:
```

### `r342.V6_tuple_drops_keyerror`

Drop KeyError from the except tuple, so a file with no threshold key crashes

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r342.json`, row `V6_tuple_drops_keyerror`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[no-key]`

Old text:

```
except (OSError, ValueError, KeyError, TypeError, OverflowError) as exc:
```

New text:

```
except (OSError, ValueError, TypeError, OverflowError) as exc:
```

### `r342.V7_tuple_drops_typeerror`

Drop TypeError from the except tuple, so a list, null or boolean payload crashes

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r342.json`, row `V7_tuple_drops_typeerror`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 3 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[boolean]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[list]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[null]`

Old text:

```
except (OSError, ValueError, KeyError, TypeError, OverflowError) as exc:
```

New text:

```
except (OSError, ValueError, KeyError, OverflowError) as exc:
```

### `r342.V8_tuple_drops_valueerror`

Drop ValueError from the except tuple, so truncated JSON crashes

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r342.json`, row `V8_tuple_drops_valueerror`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 6 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_a_corrupt_vocal_calibration_refuses_through_the_verb_and_writes_nothing`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[empty]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[infinity]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[nan]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[text]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[truncated]`

Old text:

```
except (OSError, ValueError, KeyError, TypeError, OverflowError) as exc:
```

New text:

```
except (OSError, KeyError, TypeError, OverflowError) as exc:
```

### `r342.V9_tuple_drops_oserror`

Drop OSError from the except tuple, so an unreadable file escapes unnamed

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r342.json`, row `V9_tuple_drops_oserror`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_a_vocal_calibration_this_account_cannot_read_refuses`

Old text:

```
except (OSError, ValueError, KeyError, TypeError, OverflowError) as exc:
```

New text:

```
except (ValueError, KeyError, TypeError, OverflowError) as exc:
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

### `r375-b.M2_a_noop_claims_a_commit`

_record_mytags_commit: record a commit for an apply that wrote nothing

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r375-b.json`, row `M2_a_noop_claims_a_commit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_a_second_apply_writes_nothing_and_claims_no_commit`

Old text:

```
    if written <= 0:
        return

```

New text:

```
(empty)
```

### `r375-b.M3_witnessed_commit_not_recorded`

mytags_vocals: ignore the witness, so a commit that landed and then raised closes as though nothing landed

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r375-b.json`, row `M3_witnessed_commit_not_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_an_apply_whose_commit_lands_and_then_raises_is_recorded_as_committed`

Old text:

```
                if witness.landed:
```

New text:

```
                if False:
```

### `r375-b.M4_summary_keyed_on_the_display_name`

_record_mytags_commit: key the change summary on the category's display name, which a person can rename (R19)

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r375-b.json`, row `M4_summary_keyed_on_the_display_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 2 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_an_apply_is_listed_by_restore_list_as_a_restorable_session`
  - `tests/test_metadata_cli.py::test_an_apply_whose_commit_lands_and_then_raises_is_recorded_as_committed`

Old text:

```
session.TreeChange(tree=CHANGE_KEY, created=written)
```

New text:

```
session.TreeChange(tree=CATEGORY, created=written)
```

### `u25.G10_ignore_cut`

Every scored track is tagged, including those below the cut

- File: `src/cratekit/write/metadata_cli.py`
- Source: `u25.json`, row `G10_ignore_cut`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_vocal_tag_values_are_empty_below_the_cut`

Old text:

```
    if voxlevel is None or voxlevel < cut:
        return []

```

New text:

```
    if voxlevel is None:
        return []

```

### `u25.G11_gender_without_vox`

Gender tags are applied even when the track is below the cut

- File: `src/cratekit/write/metadata_cli.py`
- Source: `u25.json`, row `G11_gender_without_vox`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_vocal_tag_values_are_empty_below_the_cut`

Old text:

```
    if voxlevel is None or voxlevel < cut:
        return []
    values = [VALUE_VOX]
    if voxgender == "M":
        values.append(VALUE_MALE)
    elif voxgender == "F":
        values.append(VALUE_FEMALE)
    return values

```

New text:

```
    values = []
    if voxlevel is not None and voxlevel >= cut:
        values.append(VALUE_VOX)
    if voxgender == "M":
        values.append(VALUE_MALE)
    elif voxgender == "F":
        values.append(VALUE_FEMALE)
    return values

```

### `u25.G12_apply_by_default`

The plan path writes, so a dry run mutates the database

- File: `src/cratekit/write/metadata_cli.py`
- Source: `u25.json`, row `G12_apply_by_default`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 2 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_a_plan_only_run_leaves_no_record`
  - `tests/test_metadata_cli.py::test_the_plan_names_existing_rows_and_writes_nothing`

Old text:

```
        action="store_true",
        default=False,

```

New text:

```
        action="store_true",
        default=True,

```

### `u25.G13_skip_apply_gate`

Return the plan even when apply was requested, so nothing is written

- File: `src/cratekit/write/metadata_cli.py`
- Source: `u25.json`, row `G13_skip_apply_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 8 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_a_library_with_no_tag_category_refuses_through_the_verb`
  - `tests/test_metadata_cli.py::test_a_second_apply_is_idempotent`
  - `tests/test_metadata_cli.py::test_a_second_apply_writes_nothing_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_apply_is_listed_by_restore_list_as_a_restorable_session`
  - `tests/test_metadata_cli.py::test_an_apply_that_refuses_mid_write_is_abandoned_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_apply_whose_commit_lands_and_then_raises_is_recorded_as_committed`
  - `tests/test_metadata_cli.py::test_apply_writes_my_tags_and_does_not_write_a_content_column`
  - `tests/test_metadata_cli.py::test_the_capture_is_protected_while_the_apply_is_in_flight`

Old text:

```
        if not writing:
            return ctx.envelope(data=plan, outcome=Outcome.OK)

```

New text:

```
        if True:
            return ctx.envelope(data=plan, outcome=Outcome.OK)

```

### `u25.G15_barren_watch`

Watch Music, which holds no ANLZ file, instead of watch_roots

- File: `src/cratekit/write/metadata_cli.py`
- Source: `u25.json`, row `G15_barren_watch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_store.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_no_call_site_hand_lists_the_roots_an_analysis_watch_covers`

Old text:

```
            analysis_roots=analysis_store.watch_roots(cfg),

```

New text:

```
            analysis_roots=(Path(cfg.library.root) / "Music",),

```

### `u25.G24_content_column`

The My Tags apply also writes Rating, a content column

- File: `src/cratekit/write/metadata_cli.py`
- Source: `u25.json`, row `G24_content_column`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 6 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_a_second_apply_is_idempotent`
  - `tests/test_metadata_cli.py::test_a_second_apply_writes_nothing_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_apply_is_listed_by_restore_list_as_a_restorable_session`
  - `tests/test_metadata_cli.py::test_an_apply_whose_commit_lands_and_then_raises_is_recorded_as_committed`
  - `tests/test_metadata_cli.py::test_apply_writes_my_tags_and_does_not_write_a_content_column`
  - `tests/test_metadata_cli.py::test_the_capture_is_protected_while_the_apply_is_in_flight`

Old text:

```
            if rb_writer.add_my_tag(db, value_row, content_id):
                written += 1
            else:
                already += 1

```

New text:

```
            if rb_writer.add_my_tag(db, value_row, content_id):
                written += 1
            else:
                already += 1
            row = db.get_content(ID=content_id)
            if row is not None:
                row.Rating = 5

```

### `u89.L1_absent_is_default`

load_vocal_threshold: an absent calibration returns the default cut instead of None, so routing files from a cut nobody fitted

- File: `src/cratekit/write/metadata_cli.py`
- Source: `u89.json`, row `L1_absent_is_default`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`, `tests/test_metadata_cli.py`
- Collected: 223 against a baseline of 223
- Kills: 126 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_a_library_with_no_tag_category_refuses_through_the_verb`
  - `tests/test_metadata_cli.py::test_a_plan_only_run_leaves_no_record`
  - `tests/test_metadata_cli.py::test_a_second_apply_is_idempotent`
  - `tests/test_metadata_cli.py::test_a_second_apply_writes_nothing_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_absent_vocal_calibration_is_the_default_cut`
  - `tests/test_metadata_cli.py::test_an_apply_is_listed_by_restore_list_as_a_restorable_session`
  - `tests/test_metadata_cli.py::test_an_apply_that_refuses_mid_write_is_abandoned_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_apply_whose_commit_lands_and_then_raises_is_recorded_as_committed`
  - `tests/test_metadata_cli.py::test_apply_writes_my_tags_and_does_not_write_a_content_column`
  - `tests/test_metadata_cli.py::test_the_capture_is_protected_while_the_apply_is_in_flight`
  - `tests/test_metadata_cli.py::test_the_plan_names_existing_rows_and_writes_nothing`
  - `tests/test_routing_workers.py::test_a_25_minute_track_is_a_member_and_a_19_minute_one_is_not`
  - `tests/test_routing_workers.py::test_a_bare_lf_before_a_folder_close_is_a_skipped_create_and_the_file_parses`
  - `tests/test_routing_workers.py::test_a_clean_apply_names_no_skipped_file`
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_names_the_file_it_could_not_file_and_why`
  - ... and 111 more, see the JSON sidecar

Old text:

```
    if not path.is_file():
        return None
```

New text:

```
    if not path.is_file():
        return DEFAULT_VOCAL_THRESHOLD
```

### `u89.L2_tagging_default`

vocal_cut: drop the default fallback, so an uncalibrated My Tags pass has no cut

- File: `src/cratekit/write/metadata_cli.py`
- Source: `u89.json`, row `L2_tagging_default`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`, `tests/test_metadata_cli.py`
- Collected: 223 against a baseline of 223
- Kills: 12 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_a_library_with_no_tag_category_refuses_through_the_verb`
  - `tests/test_metadata_cli.py::test_a_plan_only_run_leaves_no_record`
  - `tests/test_metadata_cli.py::test_a_second_apply_is_idempotent`
  - `tests/test_metadata_cli.py::test_a_second_apply_writes_nothing_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_absent_vocal_calibration_is_the_default_cut`
  - `tests/test_metadata_cli.py::test_an_apply_is_listed_by_restore_list_as_a_restorable_session`
  - `tests/test_metadata_cli.py::test_an_apply_that_refuses_mid_write_is_abandoned_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_apply_whose_commit_lands_and_then_raises_is_recorded_as_committed`
  - `tests/test_metadata_cli.py::test_apply_writes_my_tags_and_does_not_write_a_content_column`
  - `tests/test_metadata_cli.py::test_the_capture_is_protected_while_the_apply_is_in_flight`
  - `tests/test_metadata_cli.py::test_the_plan_names_existing_rows_and_writes_nothing`
  - `tests/test_routing_workers.py::test_the_loader_says_absent_as_none_and_the_tagging_cut_still_defaults`

Old text:

```
    return DEFAULT_VOCAL_THRESHOLD if threshold is None else threshold
```

New text:

```
    return threshold
```

### `u90-c.C6_wrapper_reads_nothing`

load_vocal_threshold stops delegating, so every caller sees an uncalibrated library

- File: `src/cratekit/write/metadata_cli.py`
- Source: `u90-c.json`, row `C6_wrapper_reads_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_metadata_cli.py`
- Collected: 198 against a baseline of 198
- Kills: 8 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_fit_over_a_fitted_cut_names_the_fit_it_replaces`
  - `tests/test_analysis_workers.py::test_a_hand_cut_is_written_and_the_one_loader_reads_it_back`
  - `tests/test_analysis_workers.py::test_a_hand_cut_replaces_an_unreadable_calibration_and_says_it_could_not_be_read`
  - `tests/test_analysis_workers.py::test_a_second_hand_cut_reports_the_cut_it_replaces`
  - `tests/test_analysis_workers.py::test_a_threshold_written_as_text_comes_back_from_the_one_reader_as_a_float`
  - `tests/test_analysis_workers.py::test_the_ends_of_the_score_range_are_cuts[0]`
  - `tests/test_analysis_workers.py::test_the_ends_of_the_score_range_are_cuts[100]`
  - `tests/test_metadata_cli.py::test_a_present_vocal_calibration_is_its_own_threshold`

Old text:

```
    return None if record is None else record["threshold"]
```

New text:

```
    return None
```

### `u90-c5.C5_record_threshold_unconverted`

The one reader returns the stored threshold as written rather than the checked float

- File: `src/cratekit/write/metadata_cli.py`
- Source: `u90-c5.json`, row `C5_record_threshold_unconverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_metadata_cli.py`
- Collected: 198 against a baseline of 198
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_threshold_written_as_text_comes_back_from_the_one_reader_as_a_float`

Old text:

```
    return {**record, "threshold": threshold}
```

New text:

```
    return dict(record)
```

### `r312.E10_empty_still_warns`

left_behind_message: a run that left nothing still produces a sentence

- File: `src/cratekit/write/rebuild.py`
- Source: `r312.json`, row `E10_empty_still_warns`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 307 against a baseline of 307
- Kills: 3 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_resort_that_failed_part_way_names_only_what_the_finished_tree_left[converged]`
  - `tests/test_routing_workers.py::test_a_resort_that_left_nothing_behind_says_nothing_about_it`
  - `tests/test_routing_workers.py::test_the_leftover_code_is_the_locked_spelling`

Old text:

```
    if not found:
        return None
    named
```

New text:

```
    named
```

### `r312.E11_code_reworded`

Reword the warning code a filter would key on

- File: `src/cratekit/write/rebuild.py`
- Source: `r312.json`, row `E11_code_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 307 against a baseline of 307
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_leftover_code_is_the_locked_spelling`

Old text:

```
LEFT_BEHIND = "membership-left-behind"
```

New text:

```
LEFT_BEHIND = "membership-left"
```

### `r312.E12_check_names_no_file`

check: an unexpected difference carries no file location, the state before this unit

- File: `src/cratekit/write/convergence_check.py`
- Source: `r312.json`, row `E12_check_names_no_file`
- Moved: the same text, now in src/cratekit/write/convergence_check.py, was in src/cratekit/write/rebuild.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 307 against a baseline of 307
- Kills: 6 (killed)
- Killed:
  - `tests/test_rebuild.py::test_the_check_reports_a_difference_in_both_directions`
  - `tests/test_routing_workers.py::test_a_refusal_raised_before_the_drive_carries_no_leftover_step`
  - `tests/test_routing_workers.py::test_a_resort_names_the_membership_it_left_where_it_was`
  - `tests/test_routing_workers.py::test_a_resort_that_failed_part_way_names_only_what_the_finished_tree_left[left-behind]`
  - `tests/test_routing_workers.py::test_a_second_process_names_what_the_first_ones_tree_left`
  - `tests/test_routing_workers.py::test_the_whole_list_is_written_where_the_warning_says_it_is`

Old text:

```
            replace(entry, location=located_at.get(entry.content_id or ""))
```

New text:

```
            replace(entry, location=None)
```

### `r312.E13_record_drops_location`

left_behind_record: the written record carries no location, so the message falls back to a row number

- File: `src/cratekit/write/rebuild.py`
- Source: `r312.json`, row `E13_record_drops_location`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 307 against a baseline of 307
- Kills: 6 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_refusal_raised_before_the_drive_carries_no_leftover_step`
  - `tests/test_routing_workers.py::test_a_resort_names_the_membership_it_left_where_it_was`
  - `tests/test_routing_workers.py::test_a_resort_that_failed_part_way_names_only_what_the_finished_tree_left[left-behind]`
  - `tests/test_routing_workers.py::test_a_second_process_names_what_the_first_ones_tree_left`
  - `tests/test_routing_workers.py::test_the_record_a_worker_writes_is_the_one_the_message_reads`
  - `tests/test_routing_workers.py::test_the_whole_list_is_written_where_the_warning_says_it_is`

Old text:

```
        "location": entry.location,
    }
```

New text:

```
        "location": None,
    }
```

### `r312.E14_listed_in_dropped`

left_behind_message: reword the closing sentence so it no longer says where the whole list is

- File: `src/cratekit/write/rebuild.py`
- Source: `r312.json`, row `E14_listed_in_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 307 against a baseline of 307
- Kills: 3 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_one_jobs_leftovers_are_not_counted_under_another`
  - `tests/test_routing_workers.py::test_the_leftover_warning_is_capped_and_still_counts_every_one`
  - `tests/test_routing_workers.py::test_the_whole_list_is_written_where_the_warning_says_it_is`

Old text:

```
        f"Every one is listed in {listed_in}"
```

New text:

```
        "Every one was recorded"
```

### `r312.E2_vocal_gap_filter_off`

left_behind: return every unexpected membership, so a vocal playlist nothing compared is named as left behind

- File: `src/cratekit/write/rebuild.py`
- Source: `r312.json`, row `E2_vocal_gap_filter_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 307 against a baseline of 307
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

### `r312.E4_cap_halved`

Halve the cap on how many leftovers a warning names, 20 to 10

- File: `src/cratekit/write/rebuild.py`
- Source: `r312.json`, row `E4_cap_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 307 against a baseline of 307
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_leftover_code_is_the_locked_spelling`

Old text:

```
LEFT_BEHIND_NAMED = 20
```

New text:

```
LEFT_BEHIND_NAMED = 10
```

### `r312.E5_cap_not_applied`

left_behind_message: name every leftover, the cap never applied

- File: `src/cratekit/write/rebuild.py`
- Source: `r312.json`, row `E5_cap_not_applied`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 307 against a baseline of 307
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_leftover_warning_is_capped_and_still_counts_every_one`

Old text:

```
    named = found[:LEFT_BEHIND_NAMED]
```

New text:

```
    named = found[:]
```

### `r312.E6_count_is_the_cap`

left_behind_message: state the count of the NAMED leftovers, so a long list reads as a short one

- File: `src/cratekit/write/rebuild.py`
- Source: `r312.json`, row `E6_count_is_the_cap`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 307 against a baseline of 307
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_leftover_warning_is_capped_and_still_counts_every_one`

Old text:

```
so {len(found)} membership(s) the "
```

New text:

```
so {len(named)} membership(s) the "
```

### `r312.E7_rest_not_counted`

left_behind_message: drop the and N more clause

- File: `src/cratekit/write/rebuild.py`
- Source: `r312.json`, row `E7_rest_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 307 against a baseline of 307
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_leftover_warning_is_capped_and_still_counts_every_one`

Old text:

```
        + (f"; and {rest} more" if rest else "")
```

New text:

```
        + ""
```

### `r312.E8_unsorted`

left_behind_message: keep arrival order, so the capped names depend on the order the reports were read

- File: `src/cratekit/write/rebuild.py`
- Source: `r312.json`, row `E8_unsorted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 307 against a baseline of 307
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_leftover_warning_is_capped_and_still_counts_every_one`

Old text:

```
    found = sorted(
        f"{entry['folder']}/{entry['playlist']}: "
```

New text:

```
    found = list(
        f"{entry['folder']}/{entry['playlist']}: "
```

### `r312.E9_row_fallback_blank`

left_behind_message: a leftover with no file is named by nothing, the row identifier dropped

- File: `src/cratekit/write/rebuild.py`
- Source: `r312.json`, row `E9_row_fallback_blank`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 307 against a baseline of 307
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_leftover_with_no_readable_file_is_named_by_its_row`

Old text:

```
        f"{entry.get('location') or 'row ' + str(entry.get('content_id'))}"
```

New text:

```
        f"{entry.get('location') or ''}"
```

### `r316.M10_derivation_restates_no_gap`

derive_from_taxonomy stops calling not_derived and reports no gaps, so the resume and the derivation disagree

- File: `src/cratekit/write/rebuild.py`
- Source: `r316.json`, row `M10_derivation_restates_no_gap`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`, `tests/test_rebuild.py`
- Collected: 307 against a baseline of 307
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

### `r316.M11_warning_ignores_dimension`

not_compared_warnings warns whatever the gaps say, so a taxonomy with no vocal dimension is warned about

- File: `src/cratekit/write/rebuild.py`
- Source: `r316.json`, row `M11_warning_ignores_dimension`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 8 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_calibrated_inbox_files_a_track_over_the_cut_under_with_vox[above]`
  - `tests/test_routing_workers.py::test_a_calibrated_inbox_files_a_track_over_the_cut_under_with_vox[below]`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[above-rebuild]`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[above-resort]`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[below-rebuild]`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[below-resort]`
  - `tests/test_routing_workers.py::test_a_taxonomy_with_no_vocal_dimension_warns_on_neither_surface`
  - `tests/test_routing_workers.py::test_the_warning_code_is_the_locked_spelling`

Old text:

```
    if VOCAL_DIMENSION not in tuple(not_compared):
        return ()

```

New text:

```
(empty)
```

### `r316.M12_code_respelled`

The locked warning code is respelled to a realistic nearby value

- File: `src/cratekit/write/rebuild.py`
- Source: `r316.json`, row `M12_code_respelled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_warning_code_is_the_locked_spelling`

Old text:

```
VOCAL_NOT_COMPARED = "vocal-dimension-not-compared"
```

New text:

```
VOCAL_NOT_COMPARED = "vocal-dimension-not-derived"
```

### `r316.M8_not_derived_ignores_declaration`

not_derived names the vocal gap whether or not the taxonomy declares an additive sub-playlist

- File: `src/cratekit/write/rebuild.py`
- Source: `r316.json`, row `M8_not_derived_ignores_declaration`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`, `tests/test_rebuild.py`
- Collected: 307 against a baseline of 307
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_taxonomy_with_no_vocal_dimension_warns_on_neither_surface`

Old text:

```
    return (VOCAL_DIMENSION,) if additive and vocal_threshold is None else ()
```

New text:

```
    return (VOCAL_DIMENSION,) if vocal_threshold is None else ()
```

### `r316.M9_not_derived_ignores_threshold`

not_derived names the vocal gap even when a threshold was handed in and the dimension was derived

- File: `src/cratekit/write/rebuild.py`
- Source: `r316.json`, row `M9_not_derived_ignores_threshold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`, `tests/test_rebuild.py`
- Collected: 307 against a baseline of 307
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

### `u119-c.C3_uncompared_still_compared`

check: a playlist dimension not compared still counts its differences, so the tree reads unconverged

- File: `src/cratekit/write/convergence_check.py`
- Source: `u119-c.json`, row `C3_uncompared_still_compared`
- Moved: the same text, now in src/cratekit/write/convergence_check.py, was in src/cratekit/write/rebuild.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`, `tests/test_rebuild.py`
- Collected: 156 against a baseline of 156
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_check_with_no_source_leaves_the_recorded_favorites_out_and_names_the_gap`

Old text:

```
    uncompared = _uncompared_playlist_subs(declared, not_compared)
    if uncompared:
```

New text:

```
    uncompared = _uncompared_playlist_subs(declared, not_compared)
    if False:
```

### `u119-c.C4_favorites_beside_renamed_folder`

rebuild_tree: a first Favorites is made under the declared name beside a renamed folder

- File: `src/cratekit/write/rebuild.py`
- Source: `u119-c.json`, row `C4_favorites_beside_renamed_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_the_rebuild_puts_a_first_favorites_under_a_renamed_folder_its_record_binds`

Old text:

```
        more, second_plan = _under_recorded_folders(more, second_plan, record_now, standing_now)

```

New text:

```
(empty)
```

### `u119.R1_vox_unknown_by_id`

derive_from_taxonomy: a playlist class is asked of the vocal derivation and refused

- File: `src/cratekit/write/rebuild.py`
- Source: `u119.json`, row `R1_vox_unknown_by_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild.py`, `tests/test_genre_favorites.py`
- Collected: 156 against a baseline of 156
- Kills: 39 (killed)
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
  - ... and 24 more, see the JSON sidecar

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

### `u119.R2_with_favorites_every_tree`

with_favorites: the favourites are added to every governed tree, not only the routing tree

- File: `src/cratekit/write/rebuild.py`
- Source: `u119.json`, row `R2_with_favorites_every_tree`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_with_favorites_leaves_another_tree_and_an_undeclared_class_alone`

Old text:

```
    if tree_id != declared.tree.id or genre_favorites.favorites_class(declared) is None:
```

New text:

```
    if genre_favorites.favorites_class(declared) is None:
```

### `u132.W4_routing_tree_only`

A rebuild of another tree names the routing tree's skipped step

- File: `src/cratekit/write/rebuild.py`
- Source: `u132.json`, row `W4_routing_tree_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_genre_favorites.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 661 against a baseline of 661
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_rebuild_of_another_tree_says_nothing_of_the_routing_trees_favorites[rebuild]`
  - `tests/test_routing_workers.py::test_a_rebuild_of_another_tree_says_nothing_of_the_routing_trees_favorites[resort]`

Old text:

```
    if declared.tree.id not in {str(tree_id) for tree_id in tree_ids}:

```

New text:

```
    if False:

```

### `u155.W1_derivation`

derive_from_taxonomy: place no genre sub, so the rebuild and resort never write it

- File: `src/cratekit/write/rebuild.py`
- Source: `u155.json`, row `W1_derivation`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_jazz_folder.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 736 against a baseline of 736
- Kills: 7 (killed)
- Killed:
  - `tests/test_genre_sub.py::test_a_rominimal_track_at_energy_3_lands_in_its_band_and_in_rominimal`
  - `tests/test_genre_sub.py::test_a_rominimal_track_with_no_reading_lands_in_unsorted_and_in_rominimal`
  - `tests/test_genre_sub.py::test_route_resort_moves_the_96_puls_tracks_additively`
  - `tests/test_rebuild.py::test_a_genre_sub_is_created_once_beside_the_band_and_a_second_rebuild_plans_nothing`
  - `tests/test_routing_workers.py::test_the_database_inbox_gate_shows_a_genre_sub_beside_the_band_and_files_both`
  - `tests/test_routing_workers.py::test_the_export_gate_shows_a_genre_sub_beside_the_band_and_files_both`
  - `tests/test_routing_workers.py::test_the_unplaced_export_names_a_genre_sub_beside_the_band_and_files_both`

Old text:

```
        if genre is not None:
            out.append(DeclaredPlacement(entry.location, resolution.bucket_id, genre.id))
```

New text:

```
        if False:
            out.append(DeclaredPlacement(entry.location, resolution.bucket_id, genre.id))
```

### `u219.A1_approved_equality`

assert_as_approved: return whatever the before check would add, so a library that moved after the gate is written

- File: `src/cratekit/write/rebuild.py`
- Source: `u219.json`, row `A1_approved_equality`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_jazz_folder.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_rebuild.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 760 against a baseline of 760
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
- Collected: 760 against a baseline of 760
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
- Collected: 760 against a baseline of 760
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
- Collected: 760 against a baseline of 760
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
- Collected: 760 against a baseline of 760
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
- Collected: 760 against a baseline of 760
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
- Collected: 760 against a baseline of 760
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
- Collected: 760 against a baseline of 760
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
- Collected: 760 against a baseline of 760
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
- Collected: 760 against a baseline of 760
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
- Collected: 214 against a baseline of 214
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
- Collected: 214 against a baseline of 214
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
- Collected: 378 against a baseline of 378
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
- Collected: 378 against a baseline of 378
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
- Collected: 378 against a baseline of 378
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

### `u250.M1_three_opens_again`

read_truth: go back to the three single field readers, three opens a file, the regression the card removes

- File: `src/cratekit/write/rebuild.py`
- Source: `u250.json`, row `M1_three_opens_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild_one_open.py`, `tests/test_rebuild.py`, `tests/test_tags.py`
- Collected: 209 against a baseline of 209
- Kills: 49 (killed)
- Killed:
  - `tests/test_rebuild_one_open.py::test_a_derivation_over_n_files_makes_n_opens`
  - `tests/test_rebuild_one_open.py::test_a_file_no_open_can_read_reads_three_absent_values[empty.flac-]`
  - `tests/test_rebuild_one_open.py::test_a_file_no_open_can_read_reads_three_absent_values[garbage.aiff-FORM\x00\x00\x00\x04AIFX]`
  - `tests/test_rebuild_one_open.py::test_a_file_no_open_can_read_reads_three_absent_values[garbage.m4a-\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk]`
  - `tests/test_rebuild_one_open.py::test_a_file_no_open_can_read_reads_three_absent_values[garbage.mp3-content1]`
  - `tests/test_rebuild_one_open.py::test_a_file_no_open_can_read_reads_three_absent_values[truncated.wav-RIFF$\x00\x00\x00WAVEfmt ]`
  - `tests/test_rebuild_one_open.py::test_an_undecodable_field_reads_none_and_its_neighbours_still_read`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[decimal-.aiff]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[decimal-.flac]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[decimal-.m4a]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[decimal-.mp3]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[decimal-.ogg]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[decimal-.wav]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[energy-word-.aiff]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[energy-word-.flac]`
  - ... and 34 more, see the JSON sidecar

Old text:

```
    values = tags.read_tags(path, _TRUTH_FIELDS)
    return Truth(
        location=str(path),
        genre=values["genre"],
        energy=tags.whole_number(values["energylevel"], field="energylevel", path=path),
        voxlevel=tags.whole_number(values["voxlevel"], field="voxlevel", path=path),
    )
```

New text:

```
    return Truth(
        location=str(path),
        genre=tags.read_genre_from_file(path),
        energy=tags.read_energy_from_file(path),
        voxlevel=tags.read_vox_from_file(path),
    )
```

### `u250.M2_genre_dropped`

read_truth: read no genre, so every file routes to the fallback bucket

- File: `src/cratekit/write/rebuild.py`
- Source: `u250.json`, row `M2_genre_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild_one_open.py`, `tests/test_rebuild.py`, `tests/test_tags.py`
- Collected: 209 against a baseline of 209
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
- Collected: 209 against a baseline of 209
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
- Collected: 209 against a baseline of 209
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

