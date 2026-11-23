# Mutation table: u325-after-l-10

Measured by `scripts/mutate.py` on 2026-11-22 22:23 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 130.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:20 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 7, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r650-a.B4_engine_leaks_the_flag_onto_a_skip` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R14_walk_unsorted` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 7 | killed |
| `u56-catalogue-searcher-and-tag-workers.R15_walk_not_recursive` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 4 | killed |
| `u85-a.A11_failed_write_is_error` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 1 | killed |
| `u85-a.A13_art_only_refusal_absorbed` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 2 | killed |
| `u85-a.A1_search_skipped_only_with_both` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 11 | killed |
| `u85-a.A2_any_picture_settles` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 8 | killed |
| `u85-a.A3_unreadable_is_unchecked` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 1 | killed |
| `u85-a.A5_no_url_guard` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 22933 | 1 (promoted) | killed |
| `u85-a.A6_no_fetch_guard` | `src/cratekit/tagging/tag.py` | maintainer | 4 file(s) | 242 | 1 | killed |
| `u85-a.A7_fetch_raise_is_a_decline` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 1 | killed |
| `u85-a.A9_not_a_picture_is_a_decline` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 1 | killed |
| `r345.A10_spelled_remote_wins` | `src/cratekit/core/config.py` | user | 3 file(s) | 757 | 9 | killed |
| `r345.A1_colon_required` | `src/cratekit/core/config.py` | user | 3 file(s) | 757 | 1 | killed |
| `r345.A2_single_letter` | `src/cratekit/core/config.py` | user | 3 file(s) | 757 | 6 | killed |
| `r345.A3_name_shape` | `src/cratekit/core/config.py` | user | 3 file(s) | 757 | 6 | killed |
| `r345.A4_leading_hyphen` | `src/cratekit/core/config.py` | user | 3 file(s) | 757 | 3 | killed |
| `r345.A5_trailing_space` | `src/cratekit/core/config.py` | user | 3 file(s) | 757 | 3 | killed |
| `r345.A6_one_remote` | `src/cratekit/core/config.py` | user | 3 file(s) | 757 | 2 | killed |
| `r345.A8_validate_wiring` | `src/cratekit/core/config.py` | user | 3 file(s) | 757 | 30 | killed |
| `r345.A9_derive_on_load` | `src/cratekit/core/config.py` | user | 3 file(s) | 757 | 9 | killed |
| `u163.W15_lookup_policy` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 294 | 5 | killed |
| `u163.W16_admittable_key` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 294 | 2 | killed |
| `u163.W10_search_convention` | `src/cratekit/intake/native.py` | user | 3 file(s) | 294 | 1 | killed |
| `u163.W11_search_tie` | `src/cratekit/intake/native.py` | user | 3 file(s) | 294 | 1 | killed |
| `u163.W12_readback_active` | `src/cratekit/intake/native.py` | user | 3 file(s) | 294 | 1 | killed |
| `u163.W13_identified_words` | `src/cratekit/intake/native.py` | user | 3 file(s) | 294 | 1 | killed |
| `u163.W14_album_artist_link` | `src/cratekit/intake/native.py` | user | 3 file(s) | 294 | 2 | killed |
| `u163.W1_words_planned` | `src/cratekit/intake/native.py` | user | 3 file(s) | 294 | 15 | killed |
| `u163.W2_first_value` | `src/cratekit/intake/native.py` | user | 3 file(s) | 294 | 1 | killed |
| `u163.W3_year_digits` | `src/cratekit/intake/native.py` | user | 3 file(s) | 294 | 2 | killed |
| `u163.W4_year_written` | `src/cratekit/intake/native.py` | user | 3 file(s) | 294 | 1 | killed |
| `u163.W5_album_artist_mint` | `src/cratekit/intake/native.py` | user | 3 file(s) | 294 | 1 | killed |
| `u163.W6_album_by_artist` | `src/cratekit/intake/native.py` | user | 3 file(s) | 294 | 1 | killed |
| `u163.W7_unmoved` | `src/cratekit/intake/native.py` | user | 3 file(s) | 294 | 1 | killed |
| `u163.W8_mint_once` | `src/cratekit/intake/native.py` | user | 3 file(s) | 294 | 1 | killed |
| `u163.W9_creations_named` | `src/cratekit/intake/native.py` | user | 3 file(s) | 294 | 32 | killed |
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
| `u121-b.S25r_bridge_backfill` | `src/cratekit/intake/inspiration_cli.py` | user | 1 file(s) | 73 | 1 | killed |
| `u121.S24_ack_before_gate` | `src/cratekit/intake/inspiration_cli.py` | user | 1 file(s) | 73 | 1 | killed |
| `u121-b.S20r_bridge_set` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 73 | 1 | killed |
| `u129-author.A19_plan_archive_always_none` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 73 | 4 | killed |
| `u121.S22_record_unnamed` | `src/cratekit/intake/native.py` | user | 1 file(s) | 73 | 5 | killed |
| `u121-b.S10r_folder_row_removed` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 1 | killed |
| `u121-b.S14r_stale_digest` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 1 | killed |
| `u121-b.S15r_member_order` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 1 | killed |
| `u121-c.S2c_separator` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 2 | killed |
| `u121-d.D1_record_ignored` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 1 | killed |
| `u121-d.D2_removed_namesake` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 2 | killed |
| `u121-d.D3_repeated_row_counted_twice` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 1 | killed |
| `u121-d.D4_record_on_nothing` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 1 | killed |
| `u121-d.D5_left_dropped_when_nothing_written` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 1 | killed |
| `u121-d.D6_recorded_but_removed` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 1 | killed |
| `u121.S11_landed_by_target` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 15 | killed |
| `u121.S17_unresolved_dropped` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 5 | killed |
| `u121.S1_uploader_prefix` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 2 | killed |
| `u121.S3_answer_not_read` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 1 | killed |
| `u121.S4_page_beats_flag` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 1 | killed |
| `u121.S5_missing_word` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 6 | killed |
| `u121.S7_job_handler` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 1 | killed |
| `u121.S8_job_state` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 1 | killed |
| `u121.S9_two_folders` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 1 | killed |
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

## Row definitions

### `r650-a.B4_engine_leaks_the_flag_onto_a_skip`

The flag is read off the hit for every file, so a has-genre skip claims a word this run did not write

- File: `src/cratekit/tagging/tag.py`
- Source: `r650-a.json`, row `B4_engine_leaks_the_flag_onto_a_skip`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_file_this_engine_did_not_tag_is_never_off_taxonomy`

Old text:

```
    written: str | None = None
    off_taxonomy = False
```

New text:

```
    written: str | None = None
    off_taxonomy = bool(hit and hit.off_taxonomy)
```

### `u56-catalogue-searcher-and-tag-workers.R14_walk_unsorted`

The walk stops sorting, so an enqueue and a later walk disagree about ordinal order and one file's report is filed under another's name

- File: `src/cratekit/tagging/tag.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R14_walk_unsorted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 7 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_folder_of_three_tags_the_two_with_no_genre_and_leaves_the_third`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_an_interrupted_sweep_names_its_job_command_and_that_command_finishes_it`
  - `tests/test_tag_workers.py::test_new_art_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_tag_folder_by_hand_queues_and_drives_its_sweep_to_succeeded_in_one_call`
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`

Old text:

```
        for path in sorted(root.rglob("*"))
```

New text:

```
        for path in root.rglob("*")
```

### `u56-catalogue-searcher-and-tag-workers.R15_walk_not_recursive`

The walk stops recursing, so a folder of subfolders queues nothing and reports the honest zero over a library

- File: `src/cratekit/tagging/tag.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R15_walk_not_recursive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_file_in_a_subfolder_keeps_its_relative_identifier_and_is_still_tagged`
  - `tests/test_tagging_engine.py::test_a_title_that_opens_with_dots_is_walked_and_so_is_the_album_holding_it`
  - `tests/test_tagging_engine.py::test_the_skip_does_not_stop_the_walk_recursing`
  - `tests/test_tagging_engine.py::test_the_walk_recurses_and_comes_back_sorted`

Old text:

```
        for path in sorted(root.rglob("*"))
```

New text:

```
        for path in sorted(root.glob("*"))
```

### `u85-a.A11_failed_write_is_error`

A write the file refused is reported embedded

- File: `src/cratekit/tagging/tag.py`
- Source: `u85-a.json`, row `A11_failed_write_is_error`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_picture_the_file_will_not_take_is_an_error_and_the_genre_stands`

Old text:

```
    if not written:
```

New text:

```
    if False:
```

### `u85-a.A13_art_only_refusal_absorbed`

A refusal on a tagged file searched only for art fails the item again

- File: `src/cratekit/tagging/tag.py`
- Source: `u85-a.json`, row `A13_art_only_refusal_absorbed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 2 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_tagged_file_searched_only_for_art_is_not_failed_by_a_refusal[catalogue-parse-broken]`
  - `tests/test_tagging_engine.py::test_a_tagged_file_searched_only_for_art_is_not_failed_by_a_refusal[catalogue-unreachable]`

Old text:

```
    except CratekitError as exc:
```

New text:

```
    except ZeroDivisionError as exc:
```

### `u85-a.A1_search_skipped_only_with_both`

A tagged file skips the search whatever its art, so a tagged file with no picture is never given one

- File: `src/cratekit/tagging/tag.py`
- Source: `u85-a.json`, row `A1_search_skipped_only_with_both`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 11 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_sweep_discogs_decides_asks_beatport_only_for_missing_covers_and_counts_discogs_first`
  - `tests/test_tag_workers.py::test_an_interrupted_sweep_names_its_job_command_and_that_command_finishes_it`
  - `tests/test_tag_workers.py::test_new_art_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_the_skip_reason_reaches_the_report_and_not_only_the_artifact`
  - `tests/test_tagging_engine.py::test_a_file_this_engine_did_not_tag_is_never_off_taxonomy`
  - `tests/test_tagging_engine.py::test_a_file_with_a_genre_and_no_art_gets_art_and_its_genre_is_untouched`
  - `tests/test_tagging_engine.py::test_a_tagged_file_nobody_carries_is_still_has_genre_and_art_unavailable`
  - `tests/test_tagging_engine.py::test_a_tagged_file_searched_only_for_art_is_not_failed_by_a_refusal[catalogue-parse-broken]`
  - `tests/test_tagging_engine.py::test_a_tagged_file_searched_only_for_art_is_not_failed_by_a_refusal[catalogue-unreachable]`
  - `tests/test_tagging_engine.py::test_a_tagged_file_whose_searcher_breaks_outright_still_raises`
  - `tests/test_tagging_engine.py::test_the_folder_pass_produces_exactly_what_the_per_file_calls_produce`

Old text:

```
if existing and settled is not None:
```

New text:

```
if existing:
```

### `u85-a.A2_any_picture_settles`

A file carrying a picture is treated as needing one, so art it already has is re-downloaded over

- File: `src/cratekit/tagging/tag.py`
- Source: `u85-a.json`, row `A2_any_picture_settles`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 8 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_folder_of_three_tags_the_two_with_no_genre_and_leaves_the_third`
  - `tests/test_tag_workers.py::test_a_sweep_discogs_decides_asks_beatport_only_for_missing_covers_and_counts_discogs_first`
  - `tests/test_tag_workers.py::test_new_art_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tagging_engine.py::test_a_file_that_already_carries_a_genre_is_skipped_and_never_overwritten`
  - `tests/test_tagging_engine.py::test_a_file_that_already_has_a_genre_is_still_repaired`
  - `tests/test_tagging_engine.py::test_a_tagged_file_with_zeroed_art_is_repaired_and_never_fetched`
  - `tests/test_tagging_engine.py::test_an_untagged_file_with_zeroed_art_gets_its_genre_and_keeps_its_picture`
  - `tests/test_tagging_engine.py::test_the_folder_pass_asks_once_per_untagged_file`

Old text:

```
    if pictures:
        return {"art_fetch": ART_PRESENT
```

New text:

```
    if False:
        return {"art_fetch": ART_PRESENT
```

### `u85-a.A3_unreadable_is_unchecked`

A file whose pictures cannot be read raises out of the item instead of reporting unchecked

- File: `src/cratekit/tagging/tag.py`
- Source: `u85-a.json`, row `A3_unreadable_is_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_file_whose_pictures_cannot_be_read_is_unchecked_and_not_fetched`

Old text:

```
except (tags.UnsupportedContainer, art.UnreadableFile) as exc:
```

New text:

```
except tags.UnsupportedContainer as exc:
```

### `u85-a.A5_no_url_guard`

A hit naming no picture is still fetched, with an empty URL

- File: `src/cratekit/tagging/tag.py`
- Source: `u85-a.json`, row `A5_no_url_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 22933 against a baseline of 22933
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_published_genre.py::test_a_picture_from_beatports_row_is_reported_as_beatports`

Old text:

```
    if not hit.art_url:
```

New text:

```
    if False:
```

### `u85-a.A6_no_fetch_guard`

No fetch supplied calls None and reports the TypeError as a fetch failure

- File: `src/cratekit/tagging/tag.py`
- Source: `u85-a.json`, row `A6_no_fetch_guard`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_no_fetch_supplied_is_unavailable_rather_than_a_silent_skip`

Old text:

```
    if fetch_image is None:
```

New text:

```
    if False:
```

### `u85-a.A7_fetch_raise_is_a_decline`

A fetch that raises fails the item instead of reporting art unavailable

- File: `src/cratekit/tagging/tag.py`
- Source: `u85-a.json`, row `A7_fetch_raise_is_a_decline`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_fetch_that_raises_is_unavailable_and_never_fails_the_item`

Old text:

```
    except Exception as exc:  # noqa: BLE001
        return result(ART_UNAVAILABLE, f"the picture at {url} could not be fetched: {exc}")
```

New text:

```
    except ZeroDivisionError as exc:  # noqa: BLE001
        return result(ART_UNAVAILABLE, f"the picture at {url} could not be fetched: {exc}")
```

### `u85-a.A9_not_a_picture_is_a_decline`

Bytes that are not an image fail the item instead of reporting art unavailable

- File: `src/cratekit/tagging/tag.py`
- Source: `u85-a.json`, row `A9_not_a_picture_is_a_decline`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_bytes_that_are_not_a_picture_are_unavailable_and_nothing_is_embedded`

Old text:

```
    except art.ArtError as exc:
        return result(ART_UNAVAILABLE, f"what
```

New text:

```
    except ZeroDivisionError as exc:
        return result(ART_UNAVAILABLE, f"what
```

### `r345.A10_spelled_remote_wins`

derived_backup_remote: derive even when the file spells a remote, so the file's own spelling is overwritten

- File: `src/cratekit/core/config.py`
- Source: `r345.json`, row `A10_spelled_remote_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_backup_cli.py`
- Collected: 757 against a baseline of 757
- Kills: 9 (killed)
- Killed:
  - `tests/test_config.py::test_a_spelled_backup_remote_that_matches_the_destinations_is_kept[gdrive:]`
  - `tests/test_config.py::test_a_spelled_backup_remote_that_matches_the_destinations_is_kept[gdrive:bucket]`
  - `tests/test_config.py::test_the_destination_keys_are_published_for_the_wizard_and_the_verb`
  - `tests/test_doctor.py::test_a_spelled_remote_is_kept_unless_rclone_was_read_and_lacks_it[rclone-absent]`
  - `tests/test_doctor.py::test_a_spelled_remote_is_kept_unless_rclone_was_read_and_lacks_it[rclone-knows-it]`
  - `tests/test_doctor.py::test_a_spelled_remote_is_kept_unless_rclone_was_read_and_lacks_it[rclone-knows-neither]`
  - `tests/test_doctor.py::test_a_spelled_remote_is_kept_unless_rclone_was_read_and_lacks_it[rclone-unreadable]`
  - `tests/test_doctor.py::test_the_disagreeing_remote_refusal_names_the_flag_and_the_flag_repairs_it`
  - `tests/test_doctor.py::test_the_wizard_keeps_recorded_backup_destinations_without_asking`

Old text:

```
    if isinstance(remote, str) and remote.strip():
        return None
    for key in BACKUP_DESTINATION_KEYS:
```

New text:

```
    if False:
        return None
    for key in BACKUP_DESTINATION_KEYS:
```

### `r345.A1_colon_required`

backup_remote_name: accept a value with no colon, so a bare folder name names a remote (the brief's row)

- File: `src/cratekit/core/config.py`
- Source: `r345.json`, row `A1_colon_required`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_backup_cli.py`
- Collected: 757 against a baseline of 757
- Kills: 1 (killed)
- Killed:
  - `tests/test_config.py::test_the_destination_keys_are_published_for_the_wizard_and_the_verb`

Old text:

```
    if not colon or len(name) < 2:
        return None
```

New text:

```
    if len(name) < 2:
        return None
```

### `r345.A2_single_letter`

backup_remote_name: accept a single character before the colon, so C:/x names a remote called C

- File: `src/cratekit/core/config.py`
- Source: `r345.json`, row `A2_single_letter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_backup_cli.py`
- Collected: 757 against a baseline of 757
- Kills: 6 (killed)
- Killed:
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[C:/Backups-archive_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[C:/Backups-db_dest_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[C:/Backups-dest]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[C:\\Backups-archive_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[C:\\Backups-db_dest_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[C:\\Backups-dest]`

Old text:

```
    if not colon or len(name) < 2:
        return None
```

New text:

```
    if not colon or len(name) < 1:
        return None
```

### `r345.A3_name_shape`

backup_remote_name: drop the rclone name rule, so -gdrive and a trailing space name a remote

- File: `src/cratekit/core/config.py`
- Source: `r345.json`, row `A3_name_shape`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_backup_cli.py`
- Collected: 757 against a baseline of 757
- Kills: 6 (killed)
- Killed:
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[-gdrive:bucket-archive_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[-gdrive:bucket-db_dest_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[-gdrive:bucket-dest]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[gdrive :bucket-archive_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[gdrive :bucket-db_dest_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[gdrive :bucket-dest]`

Old text:

```
    if not _RCLONE_REMOTE_NAME.match(name):
        return None
```

New text:

```
    if False:
        return None
```

### `r345.A4_leading_hyphen`

the name rule admits a leading hyphen

- File: `src/cratekit/core/config.py`
- Source: `r345.json`, row `A4_leading_hyphen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_backup_cli.py`
- Collected: 757 against a baseline of 757
- Kills: 3 (killed)
- Killed:
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[-gdrive:bucket-archive_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[-gdrive:bucket-db_dest_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[-gdrive:bucket-dest]`

Old text:

```
_RCLONE_REMOTE_NAME = re.compile(r"^[\w.+@][\w.+@ -]*(?<! )$")
```

New text:

```
_RCLONE_REMOTE_NAME = re.compile(r"^[\w.+@-][\w.+@ -]*(?<! )$")
```

### `r345.A5_trailing_space`

the name rule admits a trailing space

- File: `src/cratekit/core/config.py`
- Source: `r345.json`, row `A5_trailing_space`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_backup_cli.py`
- Collected: 757 against a baseline of 757
- Kills: 3 (killed)
- Killed:
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[gdrive :bucket-archive_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[gdrive :bucket-db_dest_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[gdrive :bucket-dest]`

Old text:

```
_RCLONE_REMOTE_NAME = re.compile(r"^[\w.+@][\w.+@ -]*(?<! )$")
```

New text:

```
_RCLONE_REMOTE_NAME = re.compile(r"^[\w.+@][\w.+@ -]*$")
```

### `r345.A6_one_remote`

_validate_backup_destinations: let the three destinations name several remotes

- File: `src/cratekit/core/config.py`
- Source: `r345.json`, row `A6_one_remote`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_backup_cli.py`
- Collected: 757 against a baseline of 757
- Kills: 2 (killed)
- Killed:
  - `tests/test_config.py::test_the_backup_destinations_must_name_one_remote`
  - `tests/test_doctor.py::test_no_disagreement_is_read_where_there_is_nothing_to_compare`

Old text:

```
    if len(set(named.values())) > 1:
```

New text:

```
    if len(set(named.values())) > 3:
```

### `r345.A8_validate_wiring`

validate: do not call the backup destination check at all

- File: `src/cratekit/core/config.py`
- Source: `r345.json`, row `A8_validate_wiring`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_backup_cli.py`
- Collected: 757 against a baseline of 757
- Kills: 30 (killed)
- Killed:
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[-gdrive:bucket-archive_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[-gdrive:bucket-db_dest_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[-gdrive:bucket-dest]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[:local:/tmp/backups-archive_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[:local:/tmp/backups-db_dest_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[:local:/tmp/backups-dest]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[C:/Backups-archive_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[C:/Backups-db_dest_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[C:/Backups-dest]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[C:\\Backups-archive_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[C:\\Backups-db_dest_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[C:\\Backups-dest]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[MusicBackup-archive_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[MusicBackup-db_dest_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[MusicBackup-dest]`
  - ... and 15 more, see the JSON sidecar

Old text:

```
    problems += _validate_backup_destinations(data)

```

New text:

```
(empty)
```

### `r345.A9_derive_on_load`

from_dict: do not derive backup.remote from the destinations

- File: `src/cratekit/core/config.py`
- Source: `r345.json`, row `A9_derive_on_load`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_backup_cli.py`
- Collected: 757 against a baseline of 757
- Kills: 9 (killed)
- Killed:
  - `tests/test_config.py::test_a_backup_destination_naming_an_rclone_remote_is_accepted`
  - `tests/test_config.py::test_an_unset_backup_destination_stays_allowed[full]`
  - `tests/test_config.py::test_an_unset_backup_destination_stays_allowed[slim]`
  - `tests/test_config.py::test_every_name_rclone_can_store_is_accepted_as_a_remote[Sicherung_\xfc]`
  - `tests/test_config.py::test_every_name_rclone_can_store_is_accepted_as_a_remote[b2]`
  - `tests/test_config.py::test_every_name_rclone_can_store_is_accepted_as_a_remote[gdrive-2.old]`
  - `tests/test_config.py::test_every_name_rclone_can_store_is_accepted_as_a_remote[me@gdrive]`
  - `tests/test_config.py::test_every_name_rclone_can_store_is_accepted_as_a_remote[my drive]`
  - `tests/test_config.py::test_every_name_rclone_can_store_is_accepted_as_a_remote[work+home]`

Old text:

```
            overrides={"remote": derived_backup_remote(data)},
```

New text:

```
            overrides=None,
```

### `u163.W15_lookup_policy`

guard_violations: wave an admitted lookup row through without the creation policy

- File: `src/cratekit/core/rb_writer.py`
- Source: `u163.json`, row `W15_lookup_policy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 294 against a baseline of 294
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
- Collected: 294 against a baseline of 294
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
- Collected: 294 against a baseline of 294
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
- Collected: 294 against a baseline of 294
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
- Collected: 294 against a baseline of 294
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
- Collected: 294 against a baseline of 294
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
- Collected: 294 against a baseline of 294
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
- Collected: 294 against a baseline of 294
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
- Collected: 294 against a baseline of 294
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
- Collected: 294 against a baseline of 294
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
- Collected: 294 against a baseline of 294
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
- Collected: 294 against a baseline of 294
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
- Collected: 294 against a baseline of 294
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
- Collected: 294 against a baseline of 294
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
- Collected: 294 against a baseline of 294
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
- Collected: 294 against a baseline of 294
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

### `u121-b.S25r_bridge_backfill`

_native_or_refuse: a bridge tree is not refused

- File: `src/cratekit/intake/inspiration_cli.py`
- Source: `u121-b.json`, row `S25r_bridge_backfill`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_the_backfill_on_the_bridge_is_refused_naming_the_cutover`

Old text:

```
    set_playlist.assert_native(medium, landing=False)
```

New text:

```
    pass
```

### `u121.S24_ack_before_gate`

intake_inspiration: the backup acknowledgment is not read before the gate

- File: `src/cratekit/intake/inspiration_cli.py`
- Source: `u121.json`, row `S24_ack_before_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    session.assert_backup_acknowledged(cfg)
```

New text:

```
    pass
```

### `u121-b.S20r_bridge_set`

intake_land: --set on a bridge tree is not refused, the batch lands with no playlist

- File: `src/cratekit/intake/land_cli.py`
- Source: `u121-b.json`, row `S20r_bridge_set`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_landing_on_the_bridge_given_set_is_refused_by_name_before_anything_moves`

Old text:

```
    if ctx.args.set_job:
        set_playlist.assert_native(medium, landing=True)
```

New text:

```
    if False:
        set_playlist.assert_native(medium, landing=True)
```

### `u129-author.A19_plan_archive_always_none`

A set landing never plans the account archive

- File: `src/cratekit/intake/land_cli.py`
- Source: `u129-author.json`, row `A19_plan_archive_always_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 73 against a baseline of 73
- Kills: 4 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archive_failure_is_a_warning_on_the_envelope`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archive_not_renamed_is_a_warning_on_the_envelope`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archives_the_account_playlist_as_taken_in_its_year_folder`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_renames_a_set_the_landing_archived_and_it_stays_taken`

Old text:

```
    try:
        return set_cli.plan_archive_named(cfg, name, pass_name=pass_name)
    except CratekitError:
        # Soft: the landing still lands; archive can run later via export archive.
        return None

```

New text:

```
    return None

```

### `u121.S22_record_unnamed`

_record_landing_commit: the set playlist is not named on the record

- File: `src/cratekit/intake/native.py`
- Source: `u121.json`, row `S22_record_unnamed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 73 against a baseline of 73
- Kills: 5 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_follows_the_live_inspiration_row_on_the_disposable_database`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_refuses_a_playlist_a_legacy_archive_prefixed`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_renames_a_set_the_landing_archived_and_it_stays_taken`
  - `tests/test_set_inspiration_playlist.py::test_two_landings_of_one_set_on_two_days_make_one_playlist`

Old text:

```
    if set_written is not None and plan.set_playlist is not None:
```

New text:

```
    if False:
```

### `u121-b.S10r_folder_row_removed`

_folder_row: a folder rekordbox removed since the plan is still written into

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121-b.json`, row `S10r_folder_row_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_the_engine_refuses_a_folder_removed_after_the_plan_even_with_no_gate_in_front`

Old text:

```
        if row is None or rb_writer.node_removed(row):
```

New text:

```
        if row is None:
```

### `u121-b.S14r_stale_digest`

apply_alone: a plan whose digest moved since the approval is written anyway

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121-b.json`, row `S14r_stale_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_the_engine_refuses_a_plan_whose_collection_moved_even_with_no_gate_in_front`

Old text:

```
    if again.digest != plan.digest:
```

New text:

```
    if False:
```

### `u121-b.S15r_member_order`

_members: members in title order rather than set order

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121-b.json`, row `S15r_member_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_members_keep_the_sets_order_when_it_is_not_alphabetical`

Old text:

```
    return tuple(members), tuple(left)
```

New text:

```
    return tuple(sorted(members, key=lambda one: one.title)), tuple(left)
```

### `u121-c.S2c_separator`

_without_leading: keep the separator after the uploader's name

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121-c.json`, row `S2c_separator`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 73 against a baseline of 73
- Kills: 2 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_the_words_come_from_the_page_with_the_uploader_taken_off_the_title`
  - `tests/test_set_inspiration_playlist.py::test_the_words_come_off_the_jobs_page_when_no_flag_is_given`

Old text:

```
    stripped = re.sub(r"^\s*(?:[-:|\u2013\u2014]+\s*)?", "", rest)
```

New text:

```
    stripped = rest.strip()
```

### `u121-d.D1_record_ignored`

plan_for_landing: the playlist an earlier landing recorded for the job is never read, so a second day makes a twin

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121-d.json`, row `D1_record_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_two_landings_of_one_set_on_two_days_make_one_playlist`

Old text:

```
    recorded = recorded_playlist(cfg, db, job.job_id, folder_id)
    staged = [source for source, _target in files]
```

New text:

```
    recorded = None
    staged = [source for source, _target in files]
```

### `u121-d.D2_removed_namesake`

_playlist_row: a removed playlist of the name under the folder is written into

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121-d.json`, row `D2_removed_namesake`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 73 against a baseline of 73
- Kills: 2 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_recorded_playlist_that_was_removed_is_not_added_to_and_a_live_one_is_made`
  - `tests/test_set_inspiration_playlist.py::test_a_removed_namesake_under_the_folder_is_not_written_into`

Old text:

```
        if rb_writer.is_folder(row) or rb_writer.node_removed(row):
            continue
        if str(getattr(row, "ParentID", "") or "") == parent_id:
```

New text:

```
        if rb_writer.is_folder(row):
            continue
        if str(getattr(row, "ParentID", "") or "") == parent_id:
```

### `u121-d.D3_repeated_row_counted_twice`

write_members: two reports resolving to one row count as two members

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121-d.json`, row `D3_repeated_row_counted_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_two_rows_of_the_set_resolving_to_one_track_are_one_member`

Old text:

```
    distinct = tuple(dict.fromkeys(ids))
```

New text:

```
    distinct = tuple(ids)
```

### `u121-d.D4_record_on_nothing`

_record_set_commit: a rerun that added nothing still records the folder committed

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121-d.json`, row `D4_record_on_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_rerun_that_adds_nothing_records_no_commit`

Old text:

```
    if not (written.added or written.playlist_created or written.folder_created):
        return

```

New text:

```
(empty)
```

### `u121-d.D5_left_dropped_when_nothing_written`

write_members: the members whose files did not land are dropped from the left list when nothing is written

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121-d.json`, row `D5_left_dropped_when_nothing_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_when_every_landed_members_file_is_refused_the_left_list_names_them`

Old text:

```
            members=0,
            added=0,
            left=(*left, *plan.left),
        )
```

New text:

```
            members=0,
            added=0,
            left=tuple(plan.left),
        )
```

### `u121-d.D6_recorded_but_removed`

recorded_playlist: a recorded playlist rekordbox removed is still the one added to

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121-d.json`, row `D6_recorded_but_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_recorded_playlist_that_was_removed_is_not_added_to_and_a_live_one_is_made`

Old text:

```
            or rb_writer.node_removed(row)
            or str(getattr(row, "ParentID", "") or "") != folder_id
```

New text:

```
            or str(getattr(row, "ParentID", "") or "") != folder_id
```

### `u121.S11_landed_by_target`

write_members: a landed member's row is not looked up by its target

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121.json`, row `S11_landed_by_target`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 73 against a baseline of 73
- Kills: 15 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_file_two_collection_rows_claim_is_left_out_rather_than_one_row_picked`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_creates_the_declared_folder_at_the_root_when_the_library_lacks_it`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_honours_posted_on_a_pre_freeze_job`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_with_a_page_date_names_the_playlist_for_the_posted_day`
  - `tests/test_set_inspiration_playlist.py::test_a_recorded_playlist_that_was_removed_is_not_added_to_and_a_live_one_is_made`
  - `tests/test_set_inspiration_playlist.py::test_a_row_neither_owned_nor_landed_is_counted_and_named_and_not_added`
  - `tests/test_set_inspiration_playlist.py::test_a_track_accepted_at_review_as_a_library_file_joins_the_playlist_at_a_landing`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_follows_the_live_inspiration_row_on_the_disposable_database`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_refuses_a_playlist_a_legacy_archive_prefixed`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_renames_a_set_the_landing_archived_and_it_stays_taken`
  - `tests/test_set_inspiration_playlist.py::test_members_keep_the_sets_order_when_it_is_not_alphabetical`
  - `tests/test_set_inspiration_playlist.py::test_posted_on_a_frozen_job_names_another_day_and_the_frozen_name_wins_with_a_warning`
  - `tests/test_set_inspiration_playlist.py::test_the_words_come_off_the_jobs_page_when_no_flag_is_given`
  - `tests/test_set_inspiration_playlist.py::test_two_landings_of_one_set_on_two_days_make_one_playlist`

Old text:

```
        held = one.content_id or rows.get(one.target, "")
```

New text:

```
        held = one.content_id
```

### `u121.S17_unresolved_dropped`

_members: a downloaded row tied to nothing is dropped silently rather than listed

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121.json`, row `S17_unresolved_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 73 against a baseline of 73
- Kills: 5 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_row_neither_owned_nor_landed_is_counted_and_named_and_not_added`
  - `tests/test_set_inspiration_playlist.py::test_a_row_that_resolves_only_to_a_different_version_is_not_guessed`
  - `tests/test_set_inspiration_playlist.py::test_a_set_with_nothing_owned_or_landed_writes_no_playlist_and_says_so`
  - `tests/test_set_inspiration_playlist.py::test_an_unanswered_question_is_left_out_and_the_plan_offers_nothing`
  - `tests/test_set_inspiration_playlist.py::test_the_backfill_over_a_set_with_nothing_owned_asks_and_then_writes_nothing`

Old text:

```
        if not paths:
            left.append(Left(position, artist, title, state, NOT_RESOLVED))
            continue
        if how == LANDED:
```

New text:

```
        if not paths:
            continue
        if how == LANDED:
```

### `u121.S1_uploader_prefix`

_without_leading: never take the uploader's name off the front of the page title

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121.json`, row `S1_uploader_prefix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 73 against a baseline of 73
- Kills: 2 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_the_words_come_from_the_page_with_the_uploader_taken_off_the_title`
  - `tests/test_set_inspiration_playlist.py::test_the_words_come_off_the_jobs_page_when_no_flag_is_given`

Old text:

```
    if head.casefold() != dj.casefold():
```

New text:

```
    if True:
```

### `u121.S3_answer_not_read`

_LibraryView.resolve: a person's review answer is never read back, a question stays one

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121.json`, row `S3_answer_not_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_track_accepted_at_review_as_a_library_file_joins_the_playlist_at_a_landing`

Old text:

```
        if found.state is not match.MatchState.NEEDS_REVIEW:
            return found
```

New text:

```
        if True:
            return found
```

### `u121.S4_page_beats_flag`

words_for: the page's uploader wins over --dj

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121.json`, row `S4_page_beats_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_flag_wins_over_the_page_and_a_day_is_read_as_its_month`

Old text:

```
    who = (dj if dj is not None else str(page.get(fetch.PAGE_UPLOADER) or "")).strip()
```

New text:

```
    who = str(page.get(fetch.PAGE_UPLOADER) or dj or "").strip()
```

### `u121.S5_missing_word`

words_for: a missing word is not refused, the name is made with a hole

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121.json`, row `S5_missing_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 73 against a baseline of 73
- Kills: 6 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_page_date_that_is_not_a_date_names_no_month_and_the_flag_is_asked_for`
  - `tests/test_set_inspiration_playlist.py::test_a_set_the_page_and_the_flags_cannot_name_is_refused_before_the_gate`
  - `tests/test_set_inspiration_playlist.py::test_a_word_neither_the_page_nor_a_flag_gives_is_refused_naming_the_flag[page0-flags0-missing0]`
  - `tests/test_set_inspiration_playlist.py::test_a_word_neither_the_page_nor_a_flag_gives_is_refused_naming_the_flag[page1-flags1-missing1]`
  - `tests/test_set_inspiration_playlist.py::test_a_word_neither_the_page_nor_a_flag_gives_is_refused_naming_the_flag[page2-flags2-missing2]`
  - `tests/test_set_inspiration_playlist.py::test_a_word_neither_the_page_nor_a_flag_gives_is_refused_naming_the_flag[page3-flags3-missing3]`

Old text:

```
    if missing:
```

New text:

```
    if False:
```

### `u121.S7_job_handler`

set_job_or_refuse: accept a playlist job as a set

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121.json`, row `S7_job_handler`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_playlist_job_named_with_set_is_refused_before_anything_moves`

Old text:

```
    if job.handler_key != SET_KEY:
```

New text:

```
    if False:
```

### `u121.S8_job_state`

set_job_or_refuse: accept a job that has not finished

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121.json`, row `S8_job_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_the_backfill_refuses_a_job_that_is_not_a_set_and_an_unfinished_one`

Old text:

```
    if job.state is not jobs.JobState.SUCCEEDED:
```

New text:

```
    if False:
```

### `u121.S9_two_folders`

folder_for: two root folders of the name pass, the first is taken

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121.json`, row `S9_two_folders`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_two_root_folders_of_the_name_are_refused_rather_than_one_chosen`

Old text:

```
    if len(live) > 1:
```

New text:

```
    if len(live) > 2:
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

