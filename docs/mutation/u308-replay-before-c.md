# Mutation table: u308-replay-before-c

Measured by `scripts/mutate.py` on 2026-11-22 13:17 UTC, branch `HEAD` at `c9192091`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 201.

Full baseline: measured by this driver (the battery's verdict was not read: no battery verdict at `.cloud-battery/verdict.json`).

Subset baselines: 31, each measured by this driver.

Known failures: 249 node ids whose failure is this machine's and not the tree's, read from `/tmp/claude-0/-home-user-cratekit/5bcab4be-2978-53ef-b3bd-2807d1f5544d/scratchpad/known-failures.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r1313.C1_catalogue_failure_alone` | `src/cratekit/label/tidal_catalogue.py` | user | 3 file(s) | 290 | 5 | killed |
| `r1313.C2_catalogue_name_on_any_link` | `src/cratekit/label/tidal_catalogue.py` | user | 3 file(s) | 290 | 1 | killed |
| `r1634.M11_reread_reads_the_line` | `src/cratekit/label/tidal_catalogue.py` | user | 3 file(s) | 293 | 15 | killed |
| `r1634.M12_gone_confirms` | `src/cratekit/label/tidal_catalogue.py` | user | 3 file(s) | 293 | 6 | killed |
| `r261.D1_discovery_record` | `src/cratekit/label/tidal_catalogue.py` | user | 4 file(s) | 522 | 3 | killed |
| `r261.D2_transient_class` | `src/cratekit/label/tidal_catalogue.py` | user | 4 file(s) | 522 | 1 | killed |
| `r261.D3_held_guard` | `src/cratekit/label/tidal_catalogue.py` | user | 4 file(s) | 522 | 1 | killed |
| `r261.R2_roster_keeps_discovery` | `src/cratekit/label/tidal_catalogue.py` | user | 4 file(s) | 522 | 3 | killed |
| `r351.A2_unresolved_seed_skipped` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 2 | killed |
| `r351.A3_empty_roster_returned` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 6 | killed |
| `r351.A5_ambiguity_takes_first` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 2 | killed |
| `r351.G10_identifier_message_says_named` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r351.G3_unresolved_id_skipped` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 5 | killed |
| `r351.G4_any_remainder_is_an_id` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r351.G5_except_everything` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 3 | killed |
| `r351.G7_drop_object_not_found` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r351.G8_id_prefix_case_insensitive` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r351.G9_all_lookuperror_is_absence` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r352.A2_empty_roster_returned` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 6 | killed |
| `r352.G10_no_collaborator_enqueue` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r352.G11_discovered_not_added` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 10 | killed |
| `r352.G13_duplicate_roster_member` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r352.G2_skip_when_roster_nonempty` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 7 | killed |
| `r352.G4_empty_message_omits_discovery` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r352.G5_compilation_range_shrunk` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 3 | killed |
| `r352.G6_name_query_only` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 3 | killed |
| `r352.G7_ignore_match_needle` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r504-a.A1_lt_to_le` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 2 | killed |
| `r504-a.A2_lt_to_gt` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 4 | killed |
| `r504-a.A3_no_none_guard` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 3 | killed |
| `r504-a.A4_no_raise` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 3 | killed |
| `r515-operator.S7_adapter_no_count` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r705-b.S9_playlist_read_wraps_the_park` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 117 | 1 | killed |
| `r840-c.C3_the_adapter_reads_a_name` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 5 | killed |
| `r879-b.T2_offset_not_sent` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r888.R1_roster_serves_one_listing` | `src/cratekit/label/tidal_catalogue.py` | user | 5 file(s) | 578 | 3 | killed |
| `u205.S3_catalogue_lookup_ignores_app` | `src/cratekit/label/tidal_catalogue.py` | user | 3 file(s) | 256 | 15 | killed |
| `u206.M18_catalogue_keeps_any_gone` | `src/cratekit/label/tidal_catalogue.py` | user | 9 file(s) | 1135 | 2 | killed |
| `u207.A2_catalogue_ignores_screen` | `src/cratekit/label/tidal_catalogue.py` | user | 2 file(s) | 206 | 1 | killed |
| `u217.A1_flush_on_the_way_out` | `src/cratekit/label/tidal_catalogue.py` | user | 2 file(s) | 212 | 12 | killed |
| `u217.A2_roster_lists_now` | `src/cratekit/label/tidal_catalogue.py` | user | 2 file(s) | 212 | 7 | killed |
| `u217.A3_listing_not_kept` | `src/cratekit/label/tidal_catalogue.py` | user | 2 file(s) | 212 | 12 | killed |
| `u217.A4_search_not_kept` | `src/cratekit/label/tidal_catalogue.py` | user | 2 file(s) | 212 | 10 | killed |
| `u217.A5_name_not_kept` | `src/cratekit/label/tidal_catalogue.py` | user | 2 file(s) | 212 | 1 | killed |
| `u217.A6_need_object` | `src/cratekit/label/tidal_catalogue.py` | user | 2 file(s) | 212 | 1 | killed |
| `u217.A7_missing_method_kept` | `src/cratekit/label/tidal_catalogue.py` | user | 2 file(s) | 212 | 1 | killed |
| `u217.A8_member_read_uncounted` | `src/cratekit/label/tidal_catalogue.py` | user | 2 file(s) | 212 | 1 | killed |
| `u261.O1_catalogue_drops_the_app` | `src/cratekit/label/tidal_catalogue.py` | user | 3 file(s) | 270 | 3 | killed |
| `u62.A1_missing_playlist_returns_none` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `u62.A4_first_hit_not_exact` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `u62.A6_no_reread_for_missing_copyright` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `u62.A7_any_search_hit_confirms` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 2 | killed |
| `u70.A1_no_favourites_refused` | `src/cratekit/label/tidal_catalogue.py` | maintainer | 1 file(s) | 174 | 1 | killed |
| `u75-c.C1_gone_is_never_retried` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 4 | killed |
| `u75-c.C5_none_album_raises` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 2 | killed |
| `u75-c.C7_tracks_through_the_paging_wrapper` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 3 | killed |
| `u78-c.D2_blank_isrc` | `src/cratekit/label/tidal_catalogue.py` | maintainer | 1 file(s) | 174 | 3 | killed |
| `u78-c.D3_no_lookup_method` | `src/cratekit/label/tidal_catalogue.py` | maintainer | 1 file(s) | 174 | 1 | killed |
| `u79-c.D1_search_shape_read_as_empty` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r1476.M20_named_first_only` | `src/cratekit/label/registry.py` | user | 6 file(s) | 497 | 7 | killed |
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
| `r790-c.G1_offer_bounded_by_limit` | `src/cratekit/label/registry.py` | user | 4 file(s) | 332 | 1 | killed |
| `r790-c.G2_entry_overrides` | `src/cratekit/label/registry.py` | user | 4 file(s) | 332 | 4 | killed |
| `r790-c.G3_offer_floor` | `src/cratekit/label/registry.py` | user | 4 file(s) | 332 | 1 | killed |
| `r790-c.G4_offer_read_back` | `src/cratekit/label/registry.py` | user | 4 file(s) | 332 | 5 | killed |
| `r790-c.G5_rename_keeps_offer` | `src/cratekit/label/registry.py` | user | 4 file(s) | 332 | 1 | killed |
| `u100-a.R1_slug_only_presence` | `src/cratekit/label/registry.py` | user | 4 file(s) | 22933 | 0 (promoted) | zero |
| `u100-a.R2_no_presence_check` | `src/cratekit/label/registry.py` | user | 4 file(s) | 401 | 6 | killed |
| `u100-a.R3_presence_before_the_batch` | `src/cratekit/label/registry.py` | user | 4 file(s) | 401 | 1 | killed |
| `u100-a.R4_slug_refusal_aborts` | `src/cratekit/label/registry.py` | user | 4 file(s) | 401 | 1 | killed |
| `u100-c.R5_adopt_always_writes_after_fix` | `src/cratekit/label/registry.py` | user | 1 file(s) | 16 | 1 | killed |
| `u177.A1_account_suffix` | `src/cratekit/label/registry.py` | user | 4 file(s) | 144 | 23 | killed |
| `u177.A2_account_shape` | `src/cratekit/label/registry.py` | user | 4 file(s) | 144 | 4 | killed |
| `u177.A3_account_case` | `src/cratekit/label/registry.py` | user | 4 file(s) | 144 | 5 | killed |
| `u177.A4_claim_removed` | `src/cratekit/label/registry.py` | user | 4 file(s) | 144 | 2 | killed |
| `u177.A5_claim_self` | `src/cratekit/label/registry.py` | user | 4 file(s) | 144 | 1 | killed |
| `u177.A6_first_of_two` | `src/cratekit/label/registry.py` | user | 6 file(s) | 190 | 2 | killed |
| `u177.A7_stored_raw` | `src/cratekit/label/registry.py` | user | 4 file(s) | 144 | 2 | killed |
| `u177.A8_edit_drops_account` | `src/cratekit/label/registry.py` | user | 4 file(s) | 144 | 2 | killed |
| `u178.G1_genre_length_bound` | `src/cratekit/label/registry.py` | user | 3 file(s) | 284 | 1 | killed |
| `u178.G2_genre_needs_a_letter` | `src/cratekit/label/registry.py` | user | 3 file(s) | 284 | 1 | killed |
| `u178.G3_genre_one_line` | `src/cratekit/label/registry.py` | user | 3 file(s) | 284 | 1 | killed |
| `u178.G4_edit_clear_genre` | `src/cratekit/label/registry.py` | user | 3 file(s) | 284 | 1 | killed |
| `u178.G5_edit_none_keeps_genre` | `src/cratekit/label/registry.py` | user | 3 file(s) | 284 | 1 | killed |
| `u99-a.A10_edit_drops_match` | `src/cratekit/label/registry.py` | user | 3 file(s) | 293 | 1 | killed |
| `u99-a.A11_edit_drops_seeds` | `src/cratekit/label/registry.py` | user | 3 file(s) | 293 | 1 | killed |
| `u99-a.A12_edit_drops_limit` | `src/cratekit/label/registry.py` | user | 3 file(s) | 293 | 1 | killed |
| `u99-a.A13_by_name_unnormalized` | `src/cratekit/label/registry.py` | user | 3 file(s) | 22933 | 0 (promoted) | zero |
| `u99-a.A1_blank_seed` | `src/cratekit/label/registry.py` | user | 3 file(s) | 293 | 1 | killed |
| `u99-a.A2_malformed_id_seed` | `src/cratekit/label/registry.py` | user | 3 file(s) | 293 | 7 | killed |
| `u99-a.A3_id_prefix_case` | `src/cratekit/label/registry.py` | user | 3 file(s) | 293 | 1 | killed |
| `u99-a.A4_id_digits_optional` | `src/cratekit/label/registry.py` | user | 3 file(s) | 293 | 1 | killed |
| `u99-a.A5_id_prefix_match` | `src/cratekit/label/registry.py` | user | 3 file(s) | 293 | 2 | killed |
| `u99-a.A7_add_unchecked_seeds` | `src/cratekit/label/registry.py` | user | 3 file(s) | 293 | 7 | killed |
| `u99-a.A8_edit_unchecked_seeds` | `src/cratekit/label/registry.py` | user | 3 file(s) | 293 | 1 | killed |
| `u99-b.A6r_store_limit_floor` | `src/cratekit/label/registry.py` | maintainer | 3 file(s) | 293 | 1 | killed |
| `u145-s2.S2b_removed_member_read_live` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.C1_unplanned_membership_admitted` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 3 | killed |
| `u145.C2_unplanned_playlist_admitted` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.C3_parent_unchecked` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.C4_changed_membership_admitted` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.C5_content_unchecked` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.C6_existing_playlist_change_admitted` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.S10_unemptied_retired` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.S11_unemptied_asks_taken_back` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.S12_retirement_admits_memberships_only` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 13 | killed |
| `u145.S13_retirement_confined_to_nothing` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 13 | killed |
| `u145.S1_any_name_is_a_quarter` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 8 | killed |
| `u145.S3_last_dated_mention_wins` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.S4_account_never_asked` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.S5_job_dates_ignored` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 11 | killed |
| `u145.S6_rehearted_is_taken_back` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.S7_taken_back_placed` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.S8_stale_digest_accepted` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.S9_digest_covers_the_months_state` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u120-b.B4r_stale_not_refused` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 31 | 2 | killed |
| `u146-a.B10_job_no_date_dated_by_account` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 31 | 1 | killed |
| `u146-a.B11_listing_always_asked` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 31 | 3 | killed |
| `u146-a.B12_landing_takes_keyless_rows` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 18 | 1 | killed |
| `u146-a.B1_carried_states` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 31 | 7 | killed |
| `u146-a.B3_already_ignores_filed` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 31 | 3 | killed |
| `u146-a.B4_already_ignores_source` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 31 | 1 | killed |
| `u146-a.B5_removed_counts_a_live_row` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 31 | 1 | killed |
| `u146-a.B9_whole_and_short_swapped` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 31 | 4 | killed |
| `u146-b.B13_first_of_two_rows` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 18 | 1 | killed |
| `u146-b.B14_plan_owned_keeps_held_hearts` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 18 | 1 | killed |
| `u153.B1_read_back_grey` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 31 | 21 | killed |
| `u153.B2_record_colour_only` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 31 | 1 | killed |
| `u153.B3_member_order_isdigit` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 31 | 1 | killed |
| `u120.T2_naive_is_utc` | `src/cratekit/favorites/placeholders.py` | user | 1 file(s) | 66 | 1 | killed |
| `u145.M1_month_off_by_one` | `src/cratekit/favorites/placeholders.py` | user | 3 file(s) | 118 | 35 | killed |
| `u146-b.B16_undated_is_no_filing` | `src/cratekit/favorites/placeholders.py` | user | 1 file(s) | 31 | 1 | killed |
| `u146-e.B17_month_label_wrong` | `src/cratekit/favorites/placeholders.py` | user | 1 file(s) | 31 | 5 | killed |
| `u180.M1_source_first` | `src/cratekit/favorites/placeholders.py` | user | 2 file(s) | 96 | 11 | killed |
| `u180.M2_newest_first_sign` | `src/cratekit/favorites/placeholders.py` | user | 2 file(s) | 96 | 18 | killed |
| `u180.M3_year_coefficient` | `src/cratekit/favorites/placeholders.py` | user | 2 file(s) | 96 | 3 | killed |
| `u180.M4_month_must_be_plain` | `src/cratekit/favorites/placeholders.py` | user | 2 file(s) | 96 | 2 | killed |
| `u180.M5_undated_rank` | `src/cratekit/favorites/placeholders.py` | user | 2 file(s) | 96 | 2 | killed |
| `u180.M6_undated_after_others` | `src/cratekit/favorites/placeholders.py` | user | 2 file(s) | 96 | 2 | killed |
| `u153.C1_is_uncoloured_narrowed` | `src/cratekit/favorites/colour.py` | user | 3 file(s) | 110 | 3 | killed |
| `u153.C2_sort_rows_dedup` | `src/cratekit/favorites/colour.py` | user | 3 file(s) | 110 | 1 | killed |
| `u153.C3_sort_rows_missing_row` | `src/cratekit/favorites/colour.py` | user | 3 file(s) | 110 | 1 | killed |
| `u153.C4_sort_rows_uncoloured_branch` | `src/cratekit/favorites/colour.py` | user | 3 file(s) | 110 | 10 | killed |
| `u153.C6_write_pink_fill_only` | `src/cratekit/favorites/colour.py` | user | 3 file(s) | 97 | 2 | killed |
| `u153.C7_write_pink_reports_write` | `src/cratekit/favorites/colour.py` | user | 3 file(s) | 110 | 5 | killed |
| `r798-c.H3_every_name_is_resolved_before_any_is_filed` | `src/cratekit/label/held_cli.py` | user | 2 file(s) | 1135 | 1 | killed |
| `r798-c.H4_a_release_with_no_isrc_was_not_asked_about` | `src/cratekit/label/held_cli.py` | user | 2 file(s) | 1135 | 1 | killed |
| `r798-c.H5_a_returned_hold_is_marked` | `src/cratekit/label/held_cli.py` | user | 2 file(s) | 1135 | 2 | killed |
| `r815-b.H1_a_withheld_release_returns_under_no_invented_run` | `src/cratekit/label/held_cli.py` | user | 2 file(s) | 214 | 1 | killed |
| `r815-b.H2_the_withheld_word_stays_with_the_hold` | `src/cratekit/label/held_cli.py` | maintainer | 2 file(s) | 214 | 2 | killed |
| `r815-b.H3_a_judge_runs_answer_is_not_the_sweeps` | `src/cratekit/label/held_cli.py` | user | 2 file(s) | 214 | 1 | killed |
| `u243.L1_companion_not_asked` | `src/cratekit/label/tombstoned.py` | user | 3 file(s) | 140 | 1 | killed |
| `u243.L2_revoked_tombstones_count` | `src/cratekit/label/tombstoned.py` | user | 3 file(s) | 140 | 1 | killed |
| `u243.L3_artists_joined_with_ampersand` | `src/cratekit/label/tombstoned.py` | user | 3 file(s) | 140 | 2 | killed |
| `u243.L4_title_without_version` | `src/cratekit/label/tombstoned.py` | user | 3 file(s) | 140 | 4 | killed |

## Zero rows and what they owe

- `u100-a.R1_slug_only_presence` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u99-a.A13_by_name_unnormalized` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `r1313.C1_catalogue_failure_alone`

_gone: read the 404 off the failure alone, as before R-1313, so a release answered with a 404 page climbs the ladder and fails as an outage

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r1313.json`, row `C1_catalogue_failure_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_isrc_cache.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 290 against a baseline of 290
- Kills: 5 (killed)
- Killed:
  - `tests/test_provider_not_found_bodies.py::test_a_404_is_a_not_found_whatever_its_body[404-html-catalogue]`
  - `tests/test_provider_not_found_bodies.py::test_a_release_answered_by_a_404_page_is_gone_at_once`
  - `tests/test_provider_not_found_bodies.py::test_a_rewrapped_404_page_is_a_not_found[catalogue]`
  - `tests/test_provider_not_found_bodies.py::test_an_isrc_answered_by_a_404_page_is_asked_once_and_kept[catalogue]`
  - `tests/test_provider_not_found_bodies.py::test_off_the_declared_chain_a_links_cause_is_nearer_than_what_it_was_handling`

Old text:

```
    if "notfound" in type(exc).__name__.lower():
        return True
    return answered_not_found(exc)
```

New text:

```
    if "notfound" in type(exc).__name__.lower():
        return True
    return getattr(getattr(exc, "response", None), "status_code", None) == 404
```

### `r1313.C2_catalogue_name_on_any_link`

_gone: read a not found class name on any link, so a parse failure met while handling a not found reads the release as gone

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r1313.json`, row `C2_catalogue_name_on_any_link`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_isrc_cache.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 290 against a baseline of 290
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_not_found_bodies.py::test_a_name_reached_only_as_context_is_not_a_not_found`

Old text:

```
    if "notfound" in type(exc).__name__.lower():
        return True
    return answered_not_found(exc)
```

New text:

```
    if any("notfound" in type(one).__name__.lower() for one, _ in provider_session.failure_links(exc)):
        return True
    return answered_not_found(exc)
```

### `r1634.M11_reread_reads_the_line`

TidalCatalogue.reread_release: judge the listed object's own line instead of reading the album

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r1634.json`, row `M11_reread_reads_the_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
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
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
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
                "verdict": RELEASE_GONE,
```

New text:

```
                "verdict": "confirmed",
```

### `r261.D1_discovery_record`

_discover skips a failed listing without recording it, which is R-393 as it was

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r261.json`, row `D1_discovery_record`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/modules/test_labels.py`
- Collected: 522 against a baseline of 522
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_listing_failure_on_one_discovered_artist_skips_that_artist`
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_during_discovery_climbs_the_ladder_before_it_is_recorded`
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_during_discovery_fails_the_sweep_and_names_the_artist`

Old text:

```
                unread.append(
                    Unread(
                        artist=str(getattr(artist, "name", "") or artist_id),
```

New text:

```
                (
                    Unread(
                        artist=str(getattr(artist, "name", "") or artist_id),
```

### `r261.D2_transient_class`

_discover marks every listing failure transient, a listing that cannot page included

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r261.json`, row `D2_transient_class`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/modules/test_labels.py`
- Collected: 522 against a baseline of 522
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_listing_failure_on_one_discovered_artist_skips_that_artist`

Old text:

```
                        transient=not isinstance(
```

New text:

```
                        transient=True or not isinstance(
```

### `r261.D3_held_guard`

_discover records a held artist the roster reads again (the review finding)

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r261.json`, row `D3_held_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/modules/test_labels.py`
- Collected: 522 against a baseline of 522
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_held_artist_rate_limited_during_discovery_is_not_recorded_as_unread`

Old text:

```
                if str(getattr(artist, "id", "") or artist_id) in held_ids:
                    continue
```

New text:

```
                if str(getattr(artist, "id", "") or artist_id) in ():
                    continue
```

### `r261.R2_roster_keeps_discovery`

LabelRoster.unread keeps only its own missing listings and loses what discovery handed in

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r261.json`, row `R2_roster_keeps_discovery`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/modules/test_labels.py`
- Collected: 522 against a baseline of 522
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_listing_failure_on_one_discovered_artist_skips_that_artist`
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_during_discovery_climbs_the_ladder_before_it_is_recorded`
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_during_discovery_fails_the_sweep_and_names_the_artist`

Old text:

```
        self.unread = (*unread, *missing)
```

New text:

```
        self.unread = (*missing,)
```

### `r351.A2_unresolved_seed_skipped`

crawl the seeds that resolved and skip the one that did not

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r351.json`, row `A2_unresolved_seed_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_seed_that_does_not_resolve_refuses_the_label_rather_than_narrowing_it`
  - `tests/test_label_tidal_catalogue.py::test_an_unresolved_id_seed_refuses_the_label`

Old text:

```
        if unresolved:
            bits = []

```

New text:

```
        if unresolved and not artists:
            bits = []

```

### `r351.A3_empty_roster_returned`

return an empty roster for a label nothing resolved

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r351.json`, row `A3_empty_roster_returned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_longer_act_name_holding_the_needle_neither_confirms_nor_discovers`
  - `tests/test_label_tidal_catalogue.py::test_a_near_name_is_not_the_label`
  - `tests/test_label_tidal_catalogue.py::test_an_unresolvable_label_raises_and_never_returns_none`
  - `tests/test_label_tidal_catalogue.py::test_discovery_that_finds_only_copyright_mismatches_still_refuses`
  - `tests/test_label_tidal_catalogue.py::test_numbered_compilation_queries_are_the_production_range`
  - `tests/test_label_tidal_catalogue.py::test_the_absence_contract_holds_through_the_sweep`

Old text:

```
        if not artists:
            raise LabelUnresolvable(
```

New text:

```
        if not artists:
            return LabelRoster([])
            raise LabelUnresolvable(
```

### `r351.A5_ambiguity_takes_first`

take the first of two artists named exactly the same

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r351.json`, row `A5_ambiguity_takes_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_colliding_name_seed_still_refuses`
  - `tests/test_label_tidal_catalogue.py::test_two_artists_named_exactly_the_label_refuse_rather_than_guess`

Old text:

```
        if len(distinct) > 1:
```

New text:

```
        if len(distinct) > 2:
```

### `r351.G10_identifier_message_says_named`

an unresolved identifier is reported as a name the provider does not carry

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r351.json`, row `G10_identifier_message_says_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_an_unresolved_id_seed_refuses_the_label`

Old text:

```
                if seed_identifier(seed) is not None:
                    bits.append(f"no artist with identifier {seed!r}")
                else:
                    bits.append(f"no artist named exactly {seed!r}")

```

New text:

```
                bits.append(f"no artist named exactly {seed!r}")

```

### `r351.G3_unresolved_id_skipped`

a seed that does not resolve is skipped rather than refusing the label

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r351.json`, row `G3_unresolved_id_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_seed_that_does_not_resolve_refuses_the_label_rather_than_narrowing_it`
  - `tests/test_label_tidal_catalogue.py::test_an_id_lookup_that_returns_none_is_an_unresolved_seed`
  - `tests/test_label_tidal_catalogue.py::test_an_unresolved_id_seed_refuses_the_label`
  - `tests/test_label_tidal_catalogue.py::test_an_unresolved_name_seed_refuses_even_when_discovery_would_find_albums`
  - `tests/test_label_tidal_catalogue.py::test_the_client_object_not_found_is_an_unresolved_id_seed`

Old text:

```
            if artist is None:
                unresolved.append(seed)

```

New text:

```
            if artist is None:
                continue

```

### `r351.G4_any_remainder_is_an_id`

treat anything after id: as an identifier, including a name

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r351.json`, row `G4_any_remainder_is_an_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_seed_that_is_not_digits_after_the_prefix_is_still_a_name`

Old text:

```
_ID_SEED = re.compile(r"^id:(\d+)$")

```

New text:

```
_ID_SEED = re.compile(r"^id:(.+)$")

```

### `r351.G5_except_everything`

a provider outage looking up an identifier is read as a missing seed

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r351.json`, row `G5_except_everything`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_key_error_looking_up_an_id_seed_is_not_an_unresolved_seed`
  - `tests/test_label_tidal_catalogue.py::test_a_provider_outage_looking_up_an_id_seed_is_not_an_unresolved_seed`
  - `tests/test_label_tidal_catalogue.py::test_a_session_dead_during_discovery_refuses_the_label`

Old text:

```
        except tidalapi.exceptions.ObjectNotFound:
            return None
        except LookupError as exc:
            # Bare LookupError is the fake's not found. KeyError and IndexError
            # are subclasses, and those are parse failures, not a missing id.
            if type(exc) is not LookupError:
                raise
            return None

```

New text:

```
        except Exception:
            return None

```

### `r351.G7_drop_object_not_found`

the live client's ObjectNotFound is no longer treated as a missing seed

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r351.json`, row `G7_drop_object_not_found`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_the_client_object_not_found_is_an_unresolved_id_seed`

Old text:

```
        except tidalapi.exceptions.ObjectNotFound:
            return None
        except LookupError as exc:

```

New text:

```
        except LookupError as exc:

```

### `r351.G8_id_prefix_case_insensitive`

ID:99 is treated as an identifier, against the locked id:<digits> shape

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r351.json`, row `G8_id_prefix_case_insensitive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_an_uppercase_id_prefix_is_still_a_name_seed`

Old text:

```
_ID_SEED = re.compile(r"^id:(\d+)$")

```

New text:

```
_ID_SEED = re.compile(r"^id:(\d+)$", re.IGNORECASE)

```

### `r351.G9_all_lookuperror_is_absence`

KeyError and IndexError from the identifier lookup are read as a missing seed

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r351.json`, row `G9_all_lookuperror_is_absence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_key_error_looking_up_an_id_seed_is_not_an_unresolved_seed`

Old text:

```
            if type(exc) is not LookupError:
                raise
            return None

```

New text:

```
            return None

```

### `r352.A2_empty_roster_returned`

return an empty roster for a label nothing resolved

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r352.json`, row `A2_empty_roster_returned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_longer_act_name_holding_the_needle_neither_confirms_nor_discovers`
  - `tests/test_label_tidal_catalogue.py::test_a_near_name_is_not_the_label`
  - `tests/test_label_tidal_catalogue.py::test_an_unresolvable_label_raises_and_never_returns_none`
  - `tests/test_label_tidal_catalogue.py::test_discovery_that_finds_only_copyright_mismatches_still_refuses`
  - `tests/test_label_tidal_catalogue.py::test_numbered_compilation_queries_are_the_production_range`
  - `tests/test_label_tidal_catalogue.py::test_the_absence_contract_holds_through_the_sweep`

Old text:

```
        if not artists:
            raise LabelUnresolvable(

```

New text:

```
        if False and not artists:
            raise LabelUnresolvable(

```

### `r352.G10_no_collaborator_enqueue`

BFS does not enqueue credited artists from listed matching releases

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r352.json`, row `G10_no_collaborator_enqueue`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_discovery_enqueues_collaborators_from_listed_matching_releases`

Old text:

```
            for release in releases:
                if _credits_label(release, needle):
                    for identity in _credited_ids(release):
                        enqueue(identity)

```

New text:

```
            for release in releases:
                if _credits_label(release, needle):
                    pass

```

### `r352.G11_discovered_not_added`

credited artists are walked but never appended to the roster

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r352.json`, row `G11_discovered_not_added`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 10 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_compilation_returned_only_for_a_numbered_query_is_consumed`
  - `tests/test_label_tidal_catalogue.py::test_a_crawl_that_read_everything_still_succeeds`
  - `tests/test_label_tidal_catalogue.py::test_a_credit_starting_with_p_or_c_is_resolved_whole`
  - `tests/test_label_tidal_catalogue.py::test_a_listing_failure_on_one_discovered_artist_skips_that_artist`
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_during_discovery_fails_the_sweep_and_names_the_artist`
  - `tests/test_label_tidal_catalogue.py::test_a_various_compilation_the_credited_artists_do_not_list_is_not_offered`
  - `tests/test_label_tidal_catalogue.py::test_discovery_enqueues_collaborators_from_listed_matching_releases`
  - `tests/test_label_tidal_catalogue.py::test_discovery_from_a_copyright_matching_compilation_offers_the_credited_artist`
  - `tests/test_label_tidal_catalogue.py::test_discovery_matches_copyright_against_the_entry_match_needle`
  - `tests/test_label_tidal_catalogue.py::test_discovery_runs_when_the_label_already_has_an_artist_page`

Old text:

```
            if identity not in held_ids:
                discovered.append(artist)
                held_ids.add(identity)

```

New text:

```
            if identity not in held_ids:
                held_ids.add(identity)

```

### `r352.G13_duplicate_roster_member`

a discovered artist already on the roster is appended again

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r352.json`, row `G13_duplicate_roster_member`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_discovered_artist_already_on_the_roster_is_not_added_twice`

Old text:

```
            if identity not in held_ids:
                discovered.append(artist)
                held_ids.add(identity)

```

New text:

```
            discovered.append(artist)
            held_ids.add(identity)

```

### `r352.G2_skip_when_roster_nonempty`

discovery does not run when the label already has an artist page

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r352.json`, row `G2_skip_when_roster_nonempty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_crawl_that_read_everything_still_succeeds`
  - `tests/test_label_tidal_catalogue.py::test_a_held_artist_rate_limited_during_discovery_is_not_recorded_as_unread`
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_during_discovery_climbs_the_ladder_before_it_is_recorded`
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_during_discovery_fails_the_sweep_and_names_the_artist`
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_on_one_album_query_does_not_discard_the_own_page`
  - `tests/test_label_tidal_catalogue.py::test_an_authentication_error_on_album_search_still_refuses_the_label`
  - `tests/test_label_tidal_catalogue.py::test_discovery_runs_when_the_label_already_has_an_artist_page`

Old text:

```
        needle = entry.match or entry.name
        seen: set[str] = set()

```

New text:

```
        if held:
            return []
        needle = entry.match or entry.name
        seen: set[str] = set()

```

### `r352.G4_empty_message_omits_discovery`

an empty roster still says only that the label names no seed artists

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r352.json`, row `G4_empty_message_omits_discovery`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_discovery_that_finds_only_copyright_mismatches_still_refuses`

Old text:

```
                f"the provider has no artist named exactly {entry.name!r}, the "
                f"label names no seed artists, and discovery found nothing"

```

New text:

```
                f"the provider has no artist named exactly {entry.name!r} and the "
                f"label names no seed artists to crawl instead"

```

### `r352.G5_compilation_range_shrunk`

numbered compilation searches stop at 001

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r352.json`, row `G5_compilation_range_shrunk`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_compilation_returned_only_for_a_numbered_query_is_consumed`
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_on_one_album_query_does_not_discard_the_own_page`
  - `tests/test_label_tidal_catalogue.py::test_numbered_compilation_queries_are_the_production_range`

Old text:

```
COMPILATION_RANGE = range(1, 80)

```

New text:

```
COMPILATION_RANGE = range(1, 2)

```

### `r352.G6_name_query_only`

discovery searches the bare label name and no numbered compilations

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r352.json`, row `G6_name_query_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_compilation_returned_only_for_a_numbered_query_is_consumed`
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_on_one_album_query_does_not_discard_the_own_page`
  - `tests/test_label_tidal_catalogue.py::test_numbered_compilation_queries_are_the_production_range`

Old text:

```
    return (name, *(f"{name} {number:03d}" for number in COMPILATION_RANGE))

```

New text:

```
    return (name,)

```

### `r352.G7_ignore_match_needle`

copyright match uses the display name and ignores entry.match

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r352.json`, row `G7_ignore_match_needle`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_discovery_matches_copyright_against_the_entry_match_needle`

Old text:

```
        needle = entry.match or entry.name

```

New text:

```
        needle = entry.name

```

### `r504-a.A1_lt_to_le`

Adapter compares with <= instead of <, so a listing that reached its count raises a shortfall of zero

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r504-a.json`, row `A1_lt_to_le`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_complete_hearts_listing_reports_no_shortfall`
  - `tests/test_label_tidal_catalogue.py::test_the_hearts_listing_pages_to_the_declared_total_through_the_listing`

Old text:

```
        if declared is not None and len(rows) < declared:
```

New text:

```
        if declared is not None and len(rows) <= declared:
```

### `r504-a.A2_lt_to_gt`

Adapter compares the wrong way round, so a short listing returns and a long one raises

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r504-a.json`, row `A2_lt_to_gt`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_listing_longer_than_its_count_is_not_a_shortfall`
  - `tests/test_label_tidal_catalogue.py::test_a_listing_short_of_the_declared_count_raises_the_shortfall_with_its_rows`
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`
  - `tests/test_label_tidal_catalogue.py::test_the_verb_boundary_keeps_the_rows_and_hands_back_the_shortfall`

Old text:

```
        if declared is not None and len(rows) < declared:
```

New text:

```
        if declared is not None and len(rows) > declared:
```

### `r504-a.A3_no_none_guard`

Adapter drops the guard for a count the provider did not publish

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r504-a.json`, row `A3_no_none_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_count_the_provider_did_not_publish_leaves_nothing_to_compare[-1]`
  - `tests/test_label_tidal_catalogue.py::test_a_count_the_provider_did_not_publish_leaves_nothing_to_compare[0]`
  - `tests/test_label_tidal_catalogue.py::test_a_count_the_provider_did_not_publish_leaves_nothing_to_compare[None]`

Old text:

```
        if declared is not None and len(rows) < declared:
```

New text:

```
        if len(rows) < declared:
```

### `r504-a.A4_no_raise`

Adapter never raises the shortfall, which is the pre R-504 behaviour

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r504-a.json`, row `A4_no_raise`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_listing_short_of_the_declared_count_raises_the_shortfall_with_its_rows`
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`
  - `tests/test_label_tidal_catalogue.py::test_the_verb_boundary_keeps_the_rows_and_hands_back_the_shortfall`

Old text:

```
            raise HeartsShortfall(rows, declared)
```

New text:

```
            pass
```

### `r515-operator.S7_adapter_no_count`

The release adapter ignores the album's num_tracks

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r515-operator.json`, row `S7_adapter_no_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_release_listed_short_of_its_count_carries_the_shortfall_and_its_rows`

Old text:

```
        short = ListingShortfall.of(tracks, getattr(album, "num_tracks", None))
```

New text:

```
        short = None
```

### `r705-b.S9_playlist_read_wraps_the_park`

the playlist read wraps the park into an unresolvable playlist again

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r705-b.json`, row `S9_playlist_read_wraps_the_park`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 117 against a baseline of 117
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_the_playlist_read_lets_the_park_through`

Old text:

```
            playlist = self._session.playlist(identifier)
        except CratekitError:

```

New text:

```
            playlist = self._session.playlist(identifier)
        except ValueError:

```

### `r840-c.C3_the_adapter_reads_a_name`

TidalCatalogue.release_artist: answer with the text of the album's artist object, which is its address, the defect R-379 named

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r840-c.json`, row `C3_the_adapter_reads_a_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limited_artist_read_waits_and_is_asked_again`
  - `tests/test_label_tidal_catalogue.py::test_a_releases_artist_is_its_name_and_never_the_objects_address`
  - `tests/test_label_tidal_catalogue.py::test_an_artist_that_is_already_text_or_has_no_name_is_read_as_what_it_is[held2-]`
  - `tests/test_label_tidal_catalogue.py::test_an_artist_that_is_already_text_or_has_no_name_is_read_as_what_it_is[held3-]`
  - `tests/test_label_tidal_catalogue.py::test_the_sweep_files_the_name_the_artist_read_returns`

Old text:

```
        return artist_name(self._album(release_id))
```

New text:

```
        return str(getattr(self._album(release_id), "artist", "") or "")
```

### `r879-b.T2_offset_not_sent`

TidalCatalogue.search_tracks: send offset 0 to the client whatever page was asked

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r879-b.json`, row `T2_offset_not_sent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_track_search_asks_for_the_page_its_offset_names`

Old text:

```
                query, models=[tidalapi.media.Track], limit=limit, offset=offset
```

New text:

```
                query, models=[tidalapi.media.Track], limit=limit, offset=0
```

### `r888.R1_roster_serves_one_listing`

LabelRoster.held: the roster answers its albums for every listing, so its singles are never read

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r888.json`, row `R1_roster_serves_one_listing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 578 against a baseline of 578
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_listing_a_roster_does_not_hold_is_skipped_and_recorded`
  - `tests/test_label_tidal_catalogue.py::test_the_roster_crawls_the_label_page_and_every_seed_through_the_listing`
  - `tests/test_label_tidal_catalogue.py::test_the_roster_lists_once_when_it_is_built_and_the_crawl_reads_memory`

Old text:

```
        return self._listed.get(method)
```

New text:

```
        return self._listed.get("get_albums")
```

### `u205.S3_catalogue_lookup_ignores_app`

label catalogue: tracks_for_isrc goes to the account session whatever the opener built, and intake missing with it

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u205.json`, row `S3_catalogue_lookup_ignores_app`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_intake_missing_isrc.py`
- Collected: 256 against a baseline of 256
- Kills: 15 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_a_404_on_the_isrc_collection_is_an_outage_and_never_no_track`
  - `tests/test_catalogue_app.py::test_a_failed_lookup_climbs_the_ladder_and_refuses_rather_than_reading_as_no_match[400]`
  - `tests/test_catalogue_app.py::test_a_failed_lookup_climbs_the_ladder_and_refuses_rather_than_reading_as_no_match[500]`
  - `tests/test_catalogue_app.py::test_a_failed_lookup_climbs_the_ladder_and_refuses_rather_than_reading_as_no_match[503]`
  - `tests/test_catalogue_app.py::test_a_failed_lookup_climbs_the_ladder_and_refuses_rather_than_reading_as_no_match[data-not-a-list]`
  - `tests/test_catalogue_app.py::test_a_failed_lookup_climbs_the_ladder_and_refuses_rather_than_reading_as_no_match[not-an-object]`
  - `tests/test_catalogue_app.py::test_a_failed_lookup_climbs_the_ladder_and_refuses_rather_than_reading_as_no_match[not-json]`
  - `tests/test_catalogue_app.py::test_a_rate_limit_on_the_app_trips_the_shared_gate_and_refuses_the_account_too`
  - `tests/test_catalogue_app.py::test_a_rejected_app_token_climbs_the_ladder_then_refuses_naming_the_app[401]`
  - `tests/test_catalogue_app.py::test_a_rejected_app_token_climbs_the_ladder_then_refuses_naming_the_app[403]`
  - `tests/test_catalogue_app.py::test_a_token_service_refusing_the_app_is_a_rejected_app_credential[400]`
  - `tests/test_catalogue_app.py::test_a_token_service_refusing_the_app_is_a_rejected_app_credential[401]`
  - `tests/test_catalogue_app.py::test_a_token_service_refusing_the_app_is_a_rejected_app_credential[403]`
  - `tests/test_catalogue_app.py::test_an_isrc_catalogue_lookup_goes_to_the_app_and_intake_missing_with_it`
  - `tests/test_catalogue_app.py::test_open_account_and_open_catalogue_hand_the_app_client_on`

Old text:

```
        self._lookups = catalogue if catalogue is not None else session
```

New text:

```
        self._lookups = session
```

### `u206.M18_catalogue_keeps_any_gone`

TidalCatalogue.tracks_for_isrc: keep every failure _gone reads as a not found, a FileNotFoundError among them

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u206.json`, row `M18_catalogue_keeps_any_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
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
- Ran: `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 206 against a baseline of 206
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
- Ran: `tests/test_label_kept_listing.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 212 against a baseline of 212
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
- Ran: `tests/test_label_kept_listing.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 212 against a baseline of 212
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_a_continue_stopped_inside_an_artist_listing_still_costs_less_than_fresh`
  - `tests/test_label_kept_listing.py::test_a_kept_seed_the_provider_no_longer_has_is_unread_not_empty`
  - `tests/test_label_kept_listing.py::test_a_listing_the_client_does_not_expose_stays_unread_on_every_run`
  - `tests/test_label_kept_listing.py::test_a_second_listing_of_the_same_label_asks_the_provider_nothing`
  - `tests/test_label_kept_listing.py::test_label_playlists_after_a_sync_listing_asks_no_listing`
  - `tests/test_label_kept_listing.py::test_the_first_listing_pages_each_discovered_artist_once`
  - `tests/test_label_tidal_catalogue.py::test_discovery_from_a_copyright_matching_compilation_offers_the_credited_artist`

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
- Ran: `tests/test_label_kept_listing.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 212 against a baseline of 212
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
- Ran: `tests/test_label_kept_listing.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 212 against a baseline of 212
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
- Ran: `tests/test_label_kept_listing.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 212 against a baseline of 212
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
- Ran: `tests/test_label_kept_listing.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 212 against a baseline of 212
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
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 212 against a baseline of 212
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_a_listing_the_client_does_not_expose_stays_unread_on_every_run`

Old text:

```
        if skipped:
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
- Ran: `tests/test_label_kept_listing.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 212 against a baseline of 212
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

### `u261.O1_catalogue_drops_the_app`

open_catalogue: build the catalogue without the held app client, so its ISRC lookups go to the account

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u261.json`, row `O1_catalogue_drops_the_app`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_catalogue_app.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 270 against a baseline of 270
- Kills: 3 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_open_account_and_open_catalogue_hand_the_app_client_on`
  - `tests/test_provider_session_hold.py::test_an_app_recorded_after_the_open_is_picked_up_by_the_next_resolve`
  - `tests/test_provider_session_hold.py::test_the_app_client_is_held_with_the_session_and_asks_one_token`

Old text:

```
        catalogue=held.app,
```

New text:

```
        catalogue=None,
```

### `u62.A1_missing_playlist_returns_none`

Return None for a playlist the client returned nothing for

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u62.json`, row `A1_missing_playlist_returns_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_playlist_the_client_returns_nothing_for_raises_too`

Old text:

```
        if playlist is None:
            raise PlaylistUnresolvable(
```

New text:

```
        if playlist is None:
            return None
            raise PlaylistUnresolvable(
```

### `u62.A4_first_hit_not_exact`

Take any hit the search returned rather than an exact name

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u62.json`, row `A4_first_hit_not_exact`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_near_name_is_not_the_label`

Old text:

```
            if label_verify.fold_label(str(getattr(artist, "name", "") or "")) == wanted
```

New text:

```
            if label_verify.fold_label(str(getattr(artist, "name", "") or ""))
```

### `u62.A6_no_reread_for_missing_copyright`

Judge a release with no copyright line unconfirmed instead of re-reading it

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u62.json`, row `A6_no_reread_for_missing_copyright`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_release_confirms_from_its_own_copyright_line_or_a_re_read`

Old text:

```
        if not resolved and identity:
```

New text:

```
        if not resolved and not identity:
```

### `u62.A7_any_search_hit_confirms`

Confirm a harvested label on any album with a copyright line

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u62.json`, row `A7_any_search_hit_confirms`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_harvested_name_is_confirmed_only_by_a_matching_copyright_line`
  - `tests/test_label_tidal_catalogue.py::test_a_longer_act_name_holding_the_needle_neither_confirms_nor_discovers`

Old text:

```
            if resolved and label_verify.labels_match(name, resolved):
```

New text:

```
            if resolved:
```

### `u70.A1_no_favourites_refused`

A client exposing no favourites is not refused by name, so the read fails as an attribute error

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u70.json`, row `A1_no_favourites_refused`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_client_that_exposes_no_favourites_refuses_rather_than_holding_no_hearts`

Old text:

```
        if getattr(user, "favorites", None) is None:
```

New text:

```
        if False:
```

### `u75-c.C1_gone_is_never_retried`

Stop classifying a not found answer first, so a withdrawn release climbs the whole retry ladder

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u75-c.json`, row `C1_gone_is_never_retried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_404_status_is_gone_whatever_the_class_is_called`
  - `tests/test_label_tidal_catalogue.py::test_a_gone_release_has_no_artist_to_read_and_is_asked_about_once`
  - `tests/test_label_tidal_catalogue.py::test_a_release_that_is_gone_raises_at_once_and_is_never_retried`
  - `tests/test_label_tidal_catalogue.py::test_the_adapter_and_the_verb_meet_over_a_gone_release`

Old text:

```
                if _gone(exc):
                    return _GONE
                raise
```

New text:

```
                raise
```

### `u75-c.C5_none_album_raises`

Let a client that returned nothing for a release through to the listing

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u75-c.json`, row `C5_none_album_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_release_the_client_returns_nothing_for_raises_too`
  - `tests/test_label_tidal_catalogue.py::test_an_artist_read_the_client_returns_nothing_for_raises_too`

Old text:

```
        if album is _GONE or album is None:
```

New text:

```
        if album is _GONE:
```

### `u75-c.C7_tracks_through_the_paging_wrapper`

List the tracks with one direct call instead of the paging wrapper, which serves one page

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u75-c.json`, row `C7_tracks_through_the_paging_wrapper`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_release_is_paged_to_its_declared_count_and_carries_its_year`
  - `tests/test_label_tidal_catalogue.py::test_a_short_window_in_the_middle_of_a_release_does_not_end_it`
  - `tests/test_label_tidal_catalogue.py::test_the_adapter_pages_nothing_by_hand`

Old text:

```
        tracks = listing.playlist_tracks(album, shape="release_tracks", sleep=_pause)
```

New text:

```
        tracks = album.tracks()
```

### `u78-c.D2_blank_isrc`

A blank ISRC is sent to the provider

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u78-c.json`, row `D2_blank_isrc`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_no_isrc_is_refused_before_the_provider_is_asked[   ]`
  - `tests/test_label_tidal_catalogue.py::test_no_isrc_is_refused_before_the_provider_is_asked[None]`
  - `tests/test_label_tidal_catalogue.py::test_no_isrc_is_refused_before_the_provider_is_asked[]`

Old text:

```
        if not wanted:
            raise ValueError("no ISRC was given to look up")
```

New text:

```
(empty)
```

### `u78-c.D3_no_lookup_method`

A client with no ISRC lookup climbs the whole ladder before failing

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u78-c.json`, row `D3_no_lookup_method`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_client_with_no_isrc_lookup_refuses_at_once_and_never_climbs_the_ladder`

Old text:

```
        if not callable(lookup):
            # A client without the method cannot be asked, and waiting on the
            # ladder cannot grow one.
            raise LookupError("the provider client exposes no ISRC lookup")
```

New text:

```
(empty)
```

### `u79-c.D1_search_shape_read_as_empty`

A search answer with no track listing is read as no candidate

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u79-c.json`, row `D1_search_shape_read_as_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_search_answer_with_no_track_listing_is_raised_at_once_and_is_not_empty`

Old text:

```
        if not present:
            raise LookupError("the provider's search answer carries no track listing")
```

New text:

```
        if False:
            raise LookupError("the provider's search answer carries no track listing")
```

### `r1476.M20_named_first_only`

Registry.named: answer only the first holder, as by_name does

- File: `src/cratekit/label/registry.py`
- Source: `r1476.json`, row `M20_named_first_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`
- Collected: 497 against a baseline of 497
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

### `r790-c.G1_offer_bounded_by_limit`

effective_offer: stop bounding the window by the track limit, so the increment slices what the listing reported

- File: `src/cratekit/label/registry.py`
- Source: `r790-c.json`, row `G1_offer_bounded_by_limit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_label_registry_verbs.py`
- Collected: 332 against a baseline of 332
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_track_limit_below_the_offer_bounds_it_and_the_rest_is_still_counted`

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
- Ran: `tests/test_label_offer_window.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_label_registry_verbs.py`
- Collected: 332 against a baseline of 332
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_label_whose_offer_is_raised_to_thirty_files_thirty`
  - `tests/test_label_offer_window.py::test_a_round_records_the_most_the_label_could_still_offer`
  - `tests/test_label_offer_window.py::test_raising_a_label_offer_after_a_sweep_files_the_difference`
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
- Ran: `tests/test_label_offer_window.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_label_registry_verbs.py`
- Collected: 332 against a baseline of 332
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
- Ran: `tests/test_label_offer_window.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_label_registry_verbs.py`
- Collected: 332 against a baseline of 332
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_label_offer_survives_a_rename_and_an_unrelated_edit`
  - `tests/test_label_offer_window.py::test_a_label_whose_offer_is_raised_to_thirty_files_thirty`
  - `tests/test_label_offer_window.py::test_a_round_records_the_most_the_label_could_still_offer`
  - `tests/test_label_offer_window.py::test_raising_a_label_offer_after_a_sweep_files_the_difference`
  - `tests/test_label_offer_window.py::test_the_registry_says_when_the_track_limit_bounds_an_offer`

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
- Ran: `tests/test_label_offer_window.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_label_registry_verbs.py`
- Collected: 332 against a baseline of 332
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

### `u100-a.R1_slug_only_presence`

RegistryStore.adopt checks presence by slug alone, the R-381 hazard: a label held under sueno is filed again as sue-o

- File: `src/cratekit/label/registry.py`
- Source: `u100-a.json`, row `R1_slug_only_presence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                held = Registry(labels=current).resolve(name)
```

New text:

```
                held = Registry(labels=current).by_id(label_id)
```

### `u100-a.R2_no_presence_check`

RegistryStore.adopt never finds a label present, so every accepted name is written over the held entry

- File: `src/cratekit/label/registry.py`
- Source: `u100-a.json`, row `R2_no_presence_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 401 against a baseline of 401
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_a_carried_over_accented_label_is_not_filed_twice`
  - `tests/test_label_registry_adopt.py::test_a_label_held_under_a_folded_name_is_reported_not_duplicated[case]`
  - `tests/test_label_registry_adopt.py::test_a_label_held_under_a_folded_name_is_reported_not_duplicated[padding]`
  - `tests/test_label_registry_adopt.py::test_an_accepted_label_is_added_once_and_a_second_run_adds_none`
  - `tests/test_label_registry_adopt.py::test_an_adopt_that_adds_nothing_does_not_rewrite_the_registry`
  - `tests/test_label_registry_adopt.py::test_two_spellings_accepted_in_one_run_add_the_label_once`

Old text:

```
                if held is not None:
                    results.append(
```

New text:

```
                if False:
                    results.append(
```

### `u100-a.R3_presence_before_the_batch`

RegistryStore.adopt resolves against the file as loaded, not the entries this run already added, so two spellings in one run both add

- File: `src/cratekit/label/registry.py`
- Source: `u100-a.json`, row `R3_presence_before_the_batch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 401 against a baseline of 401
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_two_spellings_accepted_in_one_run_add_the_label_once`

Old text:

```
                held = Registry(labels=current).resolve(name)
```

New text:

```
                held = self.load().resolve(name)
```

### `u100-a.R4_slug_refusal_aborts`

a name that yields no identifier is no longer caught per name, so it aborts the whole adopt

- File: `src/cratekit/label/registry.py`
- Source: `u100-a.json`, row `R4_slug_refusal_aborts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 401 against a baseline of 401
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_a_name_with_no_identifier_fails_alone_and_the_rest_land`

Old text:

```
                except CratekitError as exc:
                    results.append(
```

New text:

```
                except KeyError as exc:
                    results.append(
```

### `u100-c.R5_adopt_always_writes_after_fix`

RegistryStore.adopt asks for a write even when it added nothing, re-measured after the fix round added its test

- File: `src/cratekit/label/registry.py`
- Source: `u100-c.json`, row `R5_adopt_always_writes_after_fix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_adopt.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_an_adopt_that_adds_nothing_does_not_rewrite_the_registry`

Old text:

```
            return any(result.added for result in results)
```

New text:

```
            return True
```

### `u177.A1_account_suffix`

bandcamp_account: keep .bandcamp.com on the host, so an address is stored as a host no purchase's seller equals

- File: `src/cratekit/label/registry.py`
- Source: `u177.json`, row `A1_account_suffix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_bandcamp_account.py`, `tests/test_label_registry_verbs.py`, `tests/test_bandcamp_labels.py`, `tests/test_label_genre.py`
- Collected: 144 against a baseline of 144
- Kills: 23 (killed)
- Killed:
  - `tests/test_bandcamp_labels.py::test_a_fetch_of_no_labels_release_names_no_label_landing`
  - `tests/test_bandcamp_labels.py::test_a_file_that_would_not_take_the_label_is_staged_named_and_fails_its_item`
  - `tests/test_bandcamp_labels.py::test_a_label_whose_purchases_are_all_filtered_is_not_said_to_stage`
  - `tests/test_bandcamp_labels.py::test_a_registered_sellers_files_stage_with_the_label_on_every_one`
  - `tests/test_bandcamp_labels.py::test_a_rename_after_the_queue_tags_by_the_label_frozen_with_the_job`
  - `tests/test_bandcamp_labels.py::test_a_resumed_fetch_names_the_label_landing_too`
  - `tests/test_bandcamp_labels.py::test_a_seller_with_nothing_to_fetch_is_not_asked_to_register`
  - `tests/test_bandcamp_labels.py::test_an_unregistered_seller_is_named_with_the_command_that_registers_it`
  - `tests/test_bandcamp_labels.py::test_an_unregistered_sellers_files_stage_with_no_label_tag`
  - `tests/test_bandcamp_labels.py::test_seller_by_label_name_fetches_only_that_labels_releases`
  - `tests/test_bandcamp_labels.py::test_seller_takes_a_registered_labels_name_and_plans_what_its_account_does`
  - `tests/test_bandcamp_labels.py::test_the_fetch_names_the_landing_that_files_the_batch_by_label`
  - `tests/test_bandcamp_labels.py::test_the_job_freezes_each_releases_label`
  - `tests/test_bandcamp_labels.py::test_the_landing_the_fetch_names_is_one_the_landing_verb_parses`
  - `tests/test_bandcamp_labels.py::test_the_plan_names_each_rows_label_and_none_for_a_seller_no_label_names`
  - ... and 8 more, see the JSON sidecar

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
- Ran: `tests/test_label_bandcamp_account.py`, `tests/test_label_registry_verbs.py`, `tests/test_bandcamp_labels.py`, `tests/test_label_genre.py`
- Collected: 144 against a baseline of 144
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
- Ran: `tests/test_label_bandcamp_account.py`, `tests/test_label_registry_verbs.py`, `tests/test_bandcamp_labels.py`, `tests/test_label_genre.py`
- Collected: 144 against a baseline of 144
- Kills: 5 (killed)
- Killed:
  - `tests/test_bandcamp_labels.py::test_the_label_written_is_the_display_name_and_the_record_names_it`
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
- Ran: `tests/test_label_bandcamp_account.py`, `tests/test_label_registry_verbs.py`, `tests/test_bandcamp_labels.py`, `tests/test_label_genre.py`
- Collected: 144 against a baseline of 144
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
- Ran: `tests/test_label_bandcamp_account.py`, `tests/test_label_registry_verbs.py`, `tests/test_bandcamp_labels.py`, `tests/test_label_genre.py`
- Collected: 144 against a baseline of 144
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
- Ran: `tests/test_label_bandcamp_account.py`, `tests/test_label_registry_verbs.py`, `tests/test_bandcamp_labels.py`, `tests/test_label_genre.py`, `tests/test_bandcamp_labels.py`, `tests/test_bandcamp_cli.py`
- Collected: 190 against a baseline of 190
- Kills: 2 (killed)
- Killed:
  - `tests/test_bandcamp_labels.py::test_two_labels_naming_one_account_by_hand_stage_it_under_neither`
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
- Ran: `tests/test_label_bandcamp_account.py`, `tests/test_label_registry_verbs.py`, `tests/test_bandcamp_labels.py`, `tests/test_label_genre.py`
- Collected: 144 against a baseline of 144
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
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_bandcamp_account.py`, `tests/test_label_registry_verbs.py`, `tests/test_bandcamp_labels.py`, `tests/test_label_genre.py`
- Collected: 144 against a baseline of 144
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_bandcamp_account.py::test_default_clears_the_account_and_frees_it_for_another_label`
  - `tests/test_label_bandcamp_account.py::test_set_with_only_bandcamp_is_a_field_to_change`

Old text:

```
                else (bandcamp if bandcamp is not None else existing.bandcamp),

```

New text:

```
                else existing.bandcamp,

```

### `u178.G1_genre_length_bound`

check_genre: the bound read one past GENRE_MAX, so a 65 character genre is stored

- File: `src/cratekit/label/registry.py`
- Source: `u178.json`, row `G1_genre_length_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_label_genre_gate.py`, `tests/test_label_workers.py`
- Collected: 284 against a baseline of 284
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
- Ran: `tests/test_label_genre.py`, `tests/test_label_genre_gate.py`, `tests/test_label_workers.py`
- Collected: 284 against a baseline of 284
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
- Ran: `tests/test_label_genre.py`, `tests/test_label_genre_gate.py`, `tests/test_label_workers.py`
- Collected: 284 against a baseline of 284
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
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_label_genre_gate.py`, `tests/test_label_workers.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_the_word_default_clears_a_genre_and_none_keeps_it`

Old text:

```
                genre=None if clear_genre else (genre if genre is not None else existing.genre),
```

New text:

```
                genre=genre if genre is not None else existing.genre,
```

### `u178.G5_edit_none_keeps_genre`

edit: a genre of None drops the held genre, so an unrelated edit clears it

- File: `src/cratekit/label/registry.py`
- Source: `u178.json`, row `G5_edit_none_keeps_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_label_genre_gate.py`, `tests/test_label_workers.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_the_word_default_clears_a_genre_and_none_keeps_it`

Old text:

```
                genre=None if clear_genre else (genre if genre is not None else existing.genre),
```

New text:

```
                genre=None if clear_genre else genre,
```

### `u99-a.A10_edit_drops_match`

edit: write the passed match even when none was passed, so set --track-limit clears the needle

- File: `src/cratekit/label/registry.py`
- Source: `u99-a.json`, row `A10_edit_drops_match`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_set_changes_one_field_and_keeps_the_rest`

Old text:

```
                match=match if match is not None else existing.match,
```

New text:

```
                match=match,
```

### `u99-a.A11_edit_drops_seeds`

edit: write the passed seeds even when none were passed, so set --track-limit clears the seeds

- File: `src/cratekit/label/registry.py`
- Source: `u99-a.json`, row `A11_edit_drops_seeds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_set_changes_one_field_and_keeps_the_rest`

Old text:

```
                seed_artists=seeds if seeds is not None else existing.seed_artists,
```

New text:

```
                seed_artists=seeds or (),
```

### `u99-a.A12_edit_drops_limit`

edit: write the passed limit even when none was passed, so set --seed clears the limit

- File: `src/cratekit/label/registry.py`
- Source: `u99-a.json`, row `A12_edit_drops_limit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_set_seeds_replaces_the_list_and_keeps_the_limit`

Old text:

```
                track_limit=track_limit if track_limit is not None else existing.track_limit,
```

New text:

```
                track_limit=track_limit,
```

### `u99-a.A13_by_name_unnormalized`

_folded: drop the NFC normalization, so a decomposed accented name resolves nothing

- File: `src/cratekit/label/registry.py`
- Source: `u99-a.json`, row `A13_by_name_unnormalized`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return unicodedata.normalize("NFC", name.strip()).casefold()
```

New text:

```
    return name.strip().casefold()
```

### `u99-a.A1_blank_seed`

check_seed: drop the blank seed refusal, so a whitespace seed is stored as an empty name

- File: `src/cratekit/label/registry.py`
- Source: `u99-a.json`, row `A1_blank_seed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[   ]`

Old text:

```
    if not text:
        raise _field_invalid(
```

New text:

```
    if False:
        raise _field_invalid(
```

### `u99-a.A2_malformed_id_seed`

check_seed: drop the malformed id: refusal, so id:12a is stored and later searched for as a name

- File: `src/cratekit/label/registry.py`
- Source: `u99-a.json`, row `A2_malformed_id_seed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_a_malformed_id_seed_on_a_new_label_creates_no_entry`
  - `tests/test_label_registry_verbs.py::test_a_malformed_id_seed_on_set_refuses_and_writes_nothing`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[ID:12]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id: 12]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id:-4]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id:12a]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id:]`

Old text:

```
    if text[:3].casefold() == "id:" and not _ID_SEED.fullmatch(text):
```

New text:

```
    if False:
```

### `u99-a.A3_id_prefix_case`

check_seed: compare the id: prefix case sensitively, so ID:12 is stored as a name

- File: `src/cratekit/label/registry.py`
- Source: `u99-a.json`, row `A3_id_prefix_case`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[ID:12]`

Old text:

```
    if text[:3].casefold() == "id:" and not _ID_SEED.fullmatch(text):
```

New text:

```
    if text[:3] == "id:" and not _ID_SEED.fullmatch(text):
```

### `u99-a.A4_id_digits_optional`

_ID_SEED: allow zero digits, so a bare id: is stored

- File: `src/cratekit/label/registry.py`
- Source: `u99-a.json`, row `A4_id_digits_optional`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id:]`

Old text:

```
_ID_SEED = re.compile(r"id:[0-9]+")
```

New text:

```
_ID_SEED = re.compile(r"id:[0-9]*")
```

### `u99-a.A5_id_prefix_match`

check_seed: match the identifier as a prefix rather than whole, so id:12a is stored

- File: `src/cratekit/label/registry.py`
- Source: `u99-a.json`, row `A5_id_prefix_match`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_a_malformed_id_seed_on_set_refuses_and_writes_nothing`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id:12a]`

Old text:

```
not _ID_SEED.fullmatch(text):
```

New text:

```
not _ID_SEED.match(text):
```

### `u99-a.A7_add_unchecked_seeds`

add: store the seeds unchecked, so a malformed seed on add is written

- File: `src/cratekit/label/registry.py`
- Source: `u99-a.json`, row `A7_add_unchecked_seeds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_a_malformed_id_seed_on_a_new_label_creates_no_entry`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[   ]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[ID:12]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id: 12]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id:-4]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id:12a]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id:]`

Old text:

```
        seeds = _checked_seeds(seed_artists)

```

New text:

```
        seeds = tuple(seed_artists)

```

### `u99-a.A8_edit_unchecked_seeds`

edit: store the seeds unchecked, so a malformed seed on set is written

- File: `src/cratekit/label/registry.py`
- Source: `u99-a.json`, row `A8_edit_unchecked_seeds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_a_malformed_id_seed_on_set_refuses_and_writes_nothing`

Old text:

```
        seeds = _checked_seeds(seed_artists) if seed_artists is not None else None
```

New text:

```
        seeds = tuple(seed_artists) if seed_artists is not None else None
```

### `u99-b.A6r_store_limit_floor`

check_track_limit: accept zero, measured again after the store level test the A6 zero bought

- File: `src/cratekit/label/registry.py`
- Source: `u99-b.json`, row `A6r_store_limit_floor`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_the_store_refuses_a_limit_below_one_from_a_python_caller[0]`

Old text:

```
or limit < 1:
```

New text:

```
or limit < 0:
```

### `u145-s2.S2b_removed_member_read_live`

quarters: a membership rekordbox marked removed counts as a member

- File: `src/cratekit/favorites/split.py`
- Source: `u145-s2.json`, row `S2b_removed_member_read_live`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_track_taken_out_of_a_quarter_by_hand_goes_to_no_month`

Old text:

```
            if not rb_writer.membership_removed(song)
        ]
        found.append(Quarter(
```

New text:

```
            if True
        ]
        found.append(Quarter(
```

### `u145.C1_unplanned_membership_admitted`

addition_violations: a membership added into a month for a row the plan did not name is admitted

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `C1_unplanned_membership_admitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 3 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_an_addition_the_plan_did_not_name_is_a_violation[unplanned row-puts row '2']`
  - `tests/test_favorites_split.py::test_an_addition_the_plan_did_not_name_is_a_violation[wrong playlist-puts row '1' in playlist 'q']`
  - `tests/test_favorites_split.py::test_the_writer_refuses_a_membership_the_plan_did_not_name`

Old text:

```
        if row[m_marker] or content_id not in wanted.get(owner, set()):
```

New text:

```
        if row[m_marker]:
```

### `u145.C2_unplanned_playlist_admitted`

addition_violations: a playlist row the plan did not make is admitted

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `C2_unplanned_playlist_admitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_an_addition_the_plan_did_not_name_is_a_violation[unplanned playlist-unplanned djmdPlaylist row 'x']`

Old text:

```
    for key in sorted(added - set(created)):
```

New text:

```
    for key in sorted(set()):
```

### `u145.C3_parent_unchecked`

addition_violations: a made month under another parent is admitted

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `C3_parent_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_an_addition_the_plan_did_not_name_is_a_violation[wrong parent-not a live plain playlist named '2026-10' under 'f']`

Old text:

```
            or str(row[parent_at]) != str(parent)
```

New text:

```
            or False
```

### `u145.C4_changed_membership_admitted`

addition_violations: an existing membership that changed is admitted

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `C4_changed_membership_admitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_an_addition_the_plan_did_not_name_is_a_violation[changed membership-row 's1' changed]`

Old text:

```
        if before.memberships[key] != after.memberships[key]:
```

New text:

```
        if False:
```

### `u145.C5_content_unchecked`

addition_violations: a changed content row is admitted

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `C5_content_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_an_addition_the_plan_did_not_name_is_a_violation[content-djmdContent row changed]`

Old text:

```
    if before.content != after.content:
```

New text:

```
    if False:
```

### `u145.C6_existing_playlist_change_admitted`

addition_violations: an existing playlist row that changed beyond its bookkeeping is admitted

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `C6_existing_playlist_change_admitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_an_addition_the_plan_did_not_name_is_a_violation[quarter renamed-row 'q' changed ['Name']]`

Old text:

```
        if changed - allowed:
```

New text:

```
        if False:
```

### `u145.S10_unemptied_retired`

apply: a quarter whose member its month lacks is retired all the same

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `S10_unemptied_retired`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_quarter_whose_member_its_month_lacks_is_not_retired`

Old text:

```
        unemptied = _unemptied(db, planned, rows)
        if unemptied:
```

New text:

```
        unemptied = _unemptied(db, planned, rows)
        if False:
```

### `u145.S11_unemptied_asks_taken_back`

_unemptied: a taken back member is asked of a month it has none in

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `S11_unemptied_asks_taken_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_member_taken_out_of_all_favorites_goes_to_no_month_and_its_quarter_still_retires`

Old text:

```
            if content_id in month_of
            and content_id not in held.get(month_of[content_id], frozenset())
```

New text:

```
            if content_id not in held.get(month_of[content_id], frozenset())
```

### `u145.S12_retirement_admits_memberships_only`

apply: the retirement's commit admits a removed membership and no removed playlist

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `S12_retirement_admits_memberships_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 13 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_heart_every_sync_froze_again_is_resolved_once_with_its_first_dated_mention`
  - `tests/test_favorites_split.py::test_a_heart_taken_back_and_hearted_again_is_not_taken_back`
  - `tests/test_favorites_split.py::test_a_job_row_owned_when_its_job_ran_still_dates_the_member`
  - `tests/test_favorites_split.py::test_a_member_no_job_dates_takes_the_accounts_date_and_one_dated_nowhere_goes_to_undated`
  - `tests/test_favorites_split.py::test_a_member_taken_out_of_all_favorites_goes_to_no_month_and_its_quarter_still_retires`
  - `tests/test_favorites_split.py::test_a_member_two_quarters_hold_is_one_member_and_both_quarters_retire`
  - `tests/test_favorites_split.py::test_a_month_already_there_is_added_to_and_a_member_it_holds_is_not_added_twice`
  - `tests/test_favorites_split.py::test_a_quarter_of_seventeen_splits_into_fifteen_and_two_and_is_retired`
  - `tests/test_favorites_split.py::test_a_run_stopped_after_its_additions_replans_to_the_same_digest_and_finishes`
  - `tests/test_favorites_split.py::test_a_second_run_plans_nothing_and_opens_no_gate`
  - `tests/test_favorites_split.py::test_a_track_taken_out_of_a_quarter_by_hand_goes_to_no_month`
  - `tests/test_favorites_split.py::test_no_content_row_tempo_or_grid_is_written`
  - `tests/test_favorites_split.py::test_the_record_carries_both_commits_under_the_favourites_key`

Old text:

```
                rb_writer.commit_guarded(db, removals=REMOVALS)
```

New text:

```
                rb_writer.commit_guarded(db, removals=(rb_writer.MEMBERSHIP_TABLE,))
```

### `u145.S13_retirement_confined_to_nothing`

apply: the node confinement is told no quarter is removed

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `S13_retirement_confined_to_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 13 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_heart_every_sync_froze_again_is_resolved_once_with_its_first_dated_mention`
  - `tests/test_favorites_split.py::test_a_heart_taken_back_and_hearted_again_is_not_taken_back`
  - `tests/test_favorites_split.py::test_a_job_row_owned_when_its_job_ran_still_dates_the_member`
  - `tests/test_favorites_split.py::test_a_member_no_job_dates_takes_the_accounts_date_and_one_dated_nowhere_goes_to_undated`
  - `tests/test_favorites_split.py::test_a_member_taken_out_of_all_favorites_goes_to_no_month_and_its_quarter_still_retires`
  - `tests/test_favorites_split.py::test_a_member_two_quarters_hold_is_one_member_and_both_quarters_retire`
  - `tests/test_favorites_split.py::test_a_month_already_there_is_added_to_and_a_member_it_holds_is_not_added_twice`
  - `tests/test_favorites_split.py::test_a_quarter_of_seventeen_splits_into_fifteen_and_two_and_is_retired`
  - `tests/test_favorites_split.py::test_a_run_stopped_after_its_additions_replans_to_the_same_digest_and_finishes`
  - `tests/test_favorites_split.py::test_a_second_run_plans_nothing_and_opens_no_gate`
  - `tests/test_favorites_split.py::test_a_track_taken_out_of_a_quarter_by_hand_goes_to_no_month`
  - `tests/test_favorites_split.py::test_no_content_row_tempo_or_grid_is_written`
  - `tests/test_favorites_split.py::test_the_record_carries_both_commits_under_the_favourites_key`

Old text:

```
                    removed=[one.playlist_id for one in planned.quarters],
```

New text:

```
                    removed=[],
```

### `u145.S1_any_name_is_a_quarter`

quarters: every playlist beside the source but Undated is a quarter, All Favorites and the months included

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `S1_any_name_is_a_quarter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 8 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_library_with_no_quarter_never_walks_the_library_or_asks_the_account`
  - `tests/test_favorites_split.py::test_a_member_two_quarters_hold_is_one_member_and_both_quarters_retire`
  - `tests/test_favorites_split.py::test_a_month_already_there_is_added_to_and_a_member_it_holds_is_not_added_twice`
  - `tests/test_favorites_split.py::test_a_quarter_of_seventeen_splits_into_fifteen_and_two_and_is_retired`
  - `tests/test_favorites_split.py::test_a_run_stopped_after_its_additions_replans_to_the_same_digest_and_finishes`
  - `tests/test_favorites_split.py::test_a_second_run_plans_nothing_and_opens_no_gate`
  - `tests/test_favorites_split.py::test_a_track_taken_out_of_a_quarter_by_hand_goes_to_no_month`
  - `tests/test_favorites_split.py::test_the_record_carries_both_commits_under_the_favourites_key`

Old text:

```
        if not placeholders.QUARTER_LABEL.fullmatch(name):
```

New text:

```
        if name == placeholders.UNDATED:
```

### `u145.S3_last_dated_mention_wins`

_job_rows: a heart's last dated mention wins over its first

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `S3_last_dated_mention_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_heart_every_sync_froze_again_is_resolved_once_with_its_first_dated_mention`

Old text:

```
                if row.hearted is not None and row.ref not in found:
```

New text:

```
                if row.hearted is not None:
```

### `u145.S4_account_never_asked`

date_members: a member no job dates is never looked for on the account

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `S4_account_never_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_member_no_job_dates_takes_the_accounts_date_and_one_dated_nowhere_goes_to_undated`

Old text:

```
    rest = wanted - set(by_row)
    if rest:
```

New text:

```
    rest = wanted - set(by_row)
    if False:
```

### `u145.S5_job_dates_ignored`

_job_rows: no hearts job row is read, so every date comes from the account

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `S5_job_dates_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 11 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_heart_every_sync_froze_again_is_resolved_once_with_its_first_dated_mention`
  - `tests/test_favorites_split.py::test_a_heart_taken_back_and_hearted_again_is_not_taken_back`
  - `tests/test_favorites_split.py::test_a_job_row_owned_when_its_job_ran_still_dates_the_member`
  - `tests/test_favorites_split.py::test_a_member_no_job_dates_takes_the_accounts_date_and_one_dated_nowhere_goes_to_undated`
  - `tests/test_favorites_split.py::test_a_member_taken_out_of_all_favorites_goes_to_no_month_and_its_quarter_still_retires`
  - `tests/test_favorites_split.py::test_a_member_two_quarters_hold_is_one_member_and_both_quarters_retire`
  - `tests/test_favorites_split.py::test_a_month_already_there_is_added_to_and_a_member_it_holds_is_not_added_twice`
  - `tests/test_favorites_split.py::test_a_quarter_of_seventeen_splits_into_fifteen_and_two_and_is_retired`
  - `tests/test_favorites_split.py::test_a_run_stopped_after_its_additions_replans_to_the_same_digest_and_finishes`
  - `tests/test_favorites_split.py::test_a_second_run_plans_nothing_and_opens_no_gate`
  - `tests/test_favorites_split.py::test_a_track_taken_out_of_a_quarter_by_hand_goes_to_no_month`

Old text:

```
                if row.hearted is not None and row.ref not in found:
```

New text:

```
                if row.hearted is None and row.ref not in found:
```

### `u145.S6_rehearted_is_taken_back`

taken_back: a heart removed and added back live is still taken back

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `S6_rehearted_is_taken_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_heart_taken_back_and_hearted_again_is_not_taken_back`

Old text:

```
    return frozenset(removed - placement.members(db, home.source_id))
```

New text:

```
    return frozenset(removed)
```

### `u145.S7_taken_back_placed`

_planned: a member the author took back is put in its month all the same

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `S7_taken_back_placed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_member_taken_out_of_all_favorites_goes_to_no_month_and_its_quarter_still_retires`

Old text:

```
    members = tuple(one for one in every if one.content_id not in gone)
```

New text:

```
    members = tuple(one for one in every)
```

### `u145.S8_stale_digest_accepted`

apply: a digest that moved between the approval and the write is written anyway

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `S8_stale_digest_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_quarter_that_changed_after_the_approval_is_refused_and_nothing_is_written`

Old text:

```
    if again.digest != approved.digest:
```

New text:

```
    if False:
```

### `u145.S9_digest_covers_the_months_state`

identity: the digest covers what the months hold, so a run stopped after its additions plans another digest

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `S9_digest_covers_the_months_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_run_stopped_after_its_additions_replans_to_the_same_digest_and_finishes`

Old text:

```
            "taken_back": [one.content_id for one in self.taken_back],
        }
```

New text:

```
            "taken_back": [one.content_id for one in self.taken_back],
            "held": {name: sorted(ids) for name, ids in self.held.items()},
        }
```

### `u120-b.B4r_stale_not_refused`

apply: a plan whose digest moved is written anyway

- File: `src/cratekit/favorites/backfill.py`
- Source: `u120-b.json`, row `B4r_stale_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_month_playlist_deleted_between_the_plan_and_the_write_is_another_plan`
  - `tests/test_favorites_backfill.py::test_the_write_itself_refuses_a_plan_whose_home_moved_with_no_gate_in_front`

Old text:

```
    if again.digest != approved.digest:
        raise refuse(
            "decision-stale",
            "the favourites are not as the approved plan read them, so no heart was "
```

New text:

```
    if False:
        raise refuse(
            "decision-stale",
            "the favourites are not as the approved plan read them, so no heart was "
```

### `u146-a.B10_job_no_date_dated_by_account`

gather: a row whose job dated it nowhere is dated from the account, so the backfill and the landing file one heart in two places

- File: `src/cratekit/favorites/backfill.py`
- Source: `u146-a.json`, row `B10_job_no_date_dated_by_account`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_its_job_dated_nowhere_stays_undated_though_the_account_dates_it_now`

Old text:

```
        if not heart.known:
```

New text:

```
        if heart.hearted is None:
```

### `u146-a.B11_listing_always_asked`

gather: the account is listed even when no heart needs placing

- File: `src/cratekit/favorites/backfill.py`
- Source: `u146-a.json`, row `B11_listing_always_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 3 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_and_undated_holds_is_not_given_a_month`
  - `tests/test_favorites_backfill.py::test_an_unreadable_account_refuses_only_when_a_heart_needs_placing`
  - `tests/test_favorites_backfill.py::test_the_backfill_colours_the_members_placed_before_it_and_holds_a_coloured_one`

Old text:

```
    if not candidates:
        return Gathered(
```

New text:

```
    if not candidates and False:
        return Gathered(
```

### `u146-a.B12_landing_takes_keyless_rows`

owned_in_library: a row whose job froze no date key is placed by the landing, into Undated for good

- File: `src/cratekit/favorites/backfill.py`
- Source: `u146-a.json`, row `B12_landing_takes_keyless_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_whose_job_froze_no_date_key_is_left_to_the_backfill`

Old text:

```
    known = [row for row in rows if row.known and row.paths]
```

New text:

```
    known = [row for row in rows if row.paths]
```

### `u146-a.B1_carried_states`

carried: the backfill reads only the carried states again, so an owned heart is never placed

- File: `src/cratekit/favorites/backfill.py`
- Source: `u146-a.json`, row `B1_carried_states`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 7 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_and_undated_holds_is_not_given_a_month`
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_at_the_root_beside_another_playlist_still_takes_its_month`
  - `tests/test_favorites_backfill.py::test_a_heart_its_job_dated_nowhere_stays_undated_though_the_account_dates_it_now`
  - `tests/test_favorites_backfill.py::test_a_heart_put_back_by_hand_after_a_removal_takes_its_month_and_is_not_taken_back`
  - `tests/test_favorites_backfill.py::test_an_owned_heart_in_a_batch_folder_is_placed_beside_a_downloaded_one`
  - `tests/test_favorites_backfill.py::test_an_owned_heart_the_source_system_filed_is_placed_and_one_with_no_row_is_not`
  - `tests/test_favorites_backfill.py::test_owned_hearts_not_in_all_favorites_are_planned_by_month_and_those_taken_back_are_named`

Old text:

```
                found = account_playlists.carried_hearts(store, job, states=None)
```

New text:

```
                found = account_playlists.carried_hearts(store, job)
```

### `u146-a.B3_already_ignores_filed`

gather: a heart All Favorites holds is already placed whatever its month, so a heart with no month never takes one

- File: `src/cratekit/favorites/backfill.py`
- Source: `u146-a.json`, row `B3_already_ignores_filed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 3 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_at_the_root_beside_another_playlist_still_takes_its_month`
  - `tests/test_favorites_backfill.py::test_a_heart_put_back_by_hand_after_a_removal_takes_its_month_and_is_not_taken_back`
  - `tests/test_favorites_backfill.py::test_a_heart_the_landing_placed_without_a_month_takes_it_from_the_backfill`

Old text:

```
        if content_id in in_source and content_id in filed:
```

New text:

```
        if content_id in in_source:
```

### `u146-a.B4_already_ignores_source`

gather: a heart a month holds is already placed whatever All Favorites holds, so a heart out of All Favorites is never put back nor named

- File: `src/cratekit/favorites/backfill.py`
- Source: `u146-a.json`, row `B4_already_ignores_source`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_the_author_took_out_of_all_favorites_is_never_put_back`

Old text:

```
        if content_id in in_source and content_id in filed:
```

New text:

```
        if content_id in filed:
```

### `u146-a.B5_removed_counts_a_live_row`

gather: a removed membership beside a live one reads as taken back, so a heart put back by hand never takes its month

- File: `src/cratekit/favorites/backfill.py`
- Source: `u146-a.json`, row `B5_removed_counts_a_live_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_put_back_by_hand_after_a_removal_takes_its_month_and_is_not_taken_back`

Old text:

```
    removed = placement.members_marked_removed(db, home.source_id) - in_source
```

New text:

```
    removed = placement.members_marked_removed(db, home.source_id)
```

### `u146-a.B9_whole_and_short_swapped`

gather: a heart a whole listing lacks is held back and one a short listing lacks is taken back

- File: `src/cratekit/favorites/backfill.py`
- Source: `u146-a.json`, row `B9_whole_and_short_swapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 4 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_a_short_listing_did_not_date_is_held_back_not_filed_undated`
  - `tests/test_favorites_backfill.py::test_a_heart_the_account_dates_nowhere_goes_to_undated_and_one_it_no_longer_carries_is_taken_back`
  - `tests/test_favorites_backfill.py::test_a_listing_with_no_published_count_holds_back_a_heart_it_lacks`
  - `tests/test_favorites_backfill.py::test_owned_hearts_not_in_all_favorites_are_planned_by_month_and_those_taken_back_are_named`

Old text:

```
            if listing.whole:
```

New text:

```
            if not listing.whole:
```

### `u146-b.B13_first_of_two_rows`

owned_in_library: a file two active rows claim answers with the first, so a duplicate import joins All Favorites by a guess

- File: `src/cratekit/favorites/backfill.py`
- Source: `u146-b.json`, row `B13_first_of_two_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_whose_file_two_rows_claim_is_not_placed_by_a_guess`

Old text:

```
    by_path = native.single_rows_for(db, cfg, paths)
```

New text:

```
    by_path = native.content_ids_for(db, cfg, paths)
```

### `u146-b.B14_plan_owned_keeps_held_hearts`

plan_owned: an owned heart All Favorites holds is planned too, so an empty landing gives it a month

- File: `src/cratekit/favorites/backfill.py`
- Source: `u146-b.json`, row `B14_plan_owned_keeps_held_hearts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_all_favorites_holds_without_a_month_is_no_write_for_an_empty_landing`

Old text:

```
        one for one in owned_in_library(cfg, db, rows) if one.content_id not in in_source
```

New text:

```
        one for one in owned_in_library(cfg, db, rows)
```

### `u153.B1_read_back_grey`

backfill _read_back: invert the Pink check, so a row that reads Pink is called a disagreement and the verb refuses

- File: `src/cratekit/favorites/backfill.py`
- Source: `u153.json`, row `B1_read_back_grey`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 21 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_carried_heart_whose_row_sits_deep_is_placed_now_the_path_rule_is_gone`
  - `tests/test_favorites_backfill.py::test_a_date_the_job_froze_wins_over_the_accounts`
  - `tests/test_favorites_backfill.py::test_a_heart_a_short_listing_did_not_date_is_held_back_not_filed_undated`
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_and_undated_holds_is_not_given_a_month`
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_at_the_root_beside_another_playlist_still_takes_its_month`
  - `tests/test_favorites_backfill.py::test_a_heart_its_job_dated_nowhere_stays_undated_though_the_account_dates_it_now`
  - `tests/test_favorites_backfill.py::test_a_heart_put_back_by_hand_after_a_removal_takes_its_month_and_is_not_taken_back`
  - `tests/test_favorites_backfill.py::test_a_heart_the_account_dates_nowhere_goes_to_undated_and_one_it_no_longer_carries_is_taken_back`
  - `tests/test_favorites_backfill.py::test_a_heart_the_author_took_out_of_all_favorites_is_never_put_back`
  - `tests/test_favorites_backfill.py::test_a_heart_two_jobs_carried_is_one_heart_with_the_dated_jobs_date`
  - `tests/test_favorites_backfill.py::test_a_hearts_job_whose_reports_cannot_be_read_is_skipped_and_named`
  - `tests/test_favorites_backfill.py::test_a_listing_with_no_published_count_holds_back_a_heart_it_lacks`
  - `tests/test_favorites_backfill.py::test_a_second_run_finds_the_same_hearts_and_writes_nothing`
  - `tests/test_favorites_backfill.py::test_an_owned_heart_in_a_batch_folder_is_placed_beside_a_downloaded_one`
  - `tests/test_favorites_backfill.py::test_an_owned_heart_the_source_system_filed_is_placed_and_one_with_no_row_is_not`
  - ... and 6 more, see the JSON sidecar

Old text:

```
        if str(getattr(colour.find_row(db, row), colour.COLUMN, "") or "") != pink
```

New text:

```
        if str(getattr(colour.find_row(db, row), colour.COLUMN, "") or "") == pink
```

### `u153.B2_record_colour_only`

backfill record: do not record a colour-only commit, so a run that only coloured leaves no session record

- File: `src/cratekit/favorites/backfill.py`
- Source: `u153.json`, row `B2_record_colour_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_the_backfill_colours_the_members_placed_before_it_and_holds_a_coloured_one`

Old text:

```
    if placed.added <= 0 and not placed.coloured:
```

New text:

```
    if placed.added <= 0:
```

### `u153.B3_member_order_isdigit`

backfill _member_order: sort every id as an int, so a non-numeric id raises and takes the plan down

- File: `src/cratekit/favorites/backfill.py`
- Source: `u153.json`, row `B3_member_order_isdigit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_member_order_is_numeric_and_tolerates_a_non_numeric_id`

Old text:

```
        content_ids, key=lambda c: (0, int(c), "") if str(c).isdigit() else (1, 0, str(c))
```

New text:

```
        content_ids, key=lambda c: (0, int(c), "")
```

### `u120.T2_naive_is_utc`

as_utc: a naive moment is returned as it is rather than taken as UTC

- File: `src/cratekit/favorites/placeholders.py`
- Source: `u120.json`, row `T2_naive_is_utc`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_a_frozen_date_reads_back_and_junk_reads_as_no_date`

Old text:

```
    if moment.tzinfo is None:
        return moment.replace(tzinfo=timezone.utc)
```

New text:

```
    if moment.tzinfo is None:
        return moment
```

### `u145.M1_month_off_by_one`

month_of: the month is off by one, October named 2026-09

- File: `src/cratekit/favorites/placeholders.py`
- Source: `u145.json`, row `M1_month_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_split.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 118 against a baseline of 118
- Kills: 35 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_a_plan_over_a_library_already_placed_writes_nothing`
  - `tests/test_favorites_placement.py::test_a_row_named_twice_folds_to_its_first_mention`
  - `tests/test_favorites_placement.py::test_no_quarter_is_named_by_the_placement_any_more`
  - `tests/test_favorites_placement.py::test_the_month_is_the_utc_month[moment0-2026-01]`
  - `tests/test_favorites_placement.py::test_the_month_is_the_utc_month[moment1-2026-03]`
  - `tests/test_favorites_placement.py::test_the_month_is_the_utc_month[moment2-2026-04]`
  - `tests/test_favorites_placement.py::test_the_month_is_the_utc_month[moment3-2026-10]`
  - `tests/test_favorites_placement.py::test_the_month_is_the_utc_month[moment4-2026-12]`
  - `tests/test_favorites_placement.py::test_the_month_is_the_utc_month[moment5-2026-07]`
  - `tests/test_favorites_placement.py::test_the_month_is_the_utc_month[moment6-2026-11]`
  - `tests/test_favorites_placement.py::test_the_month_is_the_utc_month[moment7-2027-01]`
  - `tests/test_favorites_placement.py::test_the_plan_names_each_uncoloured_heart_for_pink_and_holds_a_coloured_one`
  - `tests/test_favorites_placement.py::test_the_plan_reads_what_each_heart_already_has_and_what_it_would_make`
  - `tests/test_favorites_placement.py::test_the_plans_digest_covers_each_months_row_found_or_to_be_made`
  - `tests/test_favorites_split.py::test_a_heart_every_sync_froze_again_is_resolved_once_with_its_first_dated_mention`
  - ... and 20 more, see the JSON sidecar

Old text:

```
    return f"{utc.year:04d}-{utc.month:02d}"
```

New text:

```
    return f"{utc.year:04d}-{utc.month - 1:02d}"
```

### `u146-b.B16_undated_is_no_filing`

is_filing: Undated is not a filing playlist, so a heart the split filed there is given a second month

- File: `src/cratekit/favorites/placeholders.py`
- Source: `u146-b.json`, row `B16_undated_is_no_filing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_and_undated_holds_is_not_given_a_month`

Old text:

```
        text == UNDATED
        or MONTH_LABEL
```

New text:

```
        False
        or MONTH_LABEL
```

### `u146-e.B17_month_label_wrong`

MONTH_LABEL: a month playlist does not read as a month, so every placed heart is planned again with nothing to add

- File: `src/cratekit/favorites/placeholders.py`
- Source: `u146-e.json`, row `B17_month_label_wrong`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 5 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_the_author_took_out_of_all_favorites_is_never_put_back`
  - `tests/test_favorites_backfill.py::test_a_second_run_finds_the_same_hearts_and_writes_nothing`
  - `tests/test_favorites_backfill.py::test_an_unreadable_account_refuses_only_when_a_heart_needs_placing`
  - `tests/test_favorites_backfill.py::test_owned_hearts_not_in_all_favorites_are_planned_by_month_and_those_taken_back_are_named`
  - `tests/test_favorites_backfill.py::test_the_backfill_colours_the_members_placed_before_it_and_holds_a_coloured_one`

Old text:

```
MONTH_LABEL = re.compile(r"\d{4}-(?:0[1-9]|1[0-2])")
```

New text:

```
MONTH_LABEL = re.compile(r"\d{4}-(?:0[1-9]|1[0-2])-")
```

### `u180.M1_source_first`

folder_rank: All Favorites ranks as any other playlist, so it is no longer first

- File: `src/cratekit/favorites/placeholders.py`
- Source: `u180.json`, row `M1_source_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_order.py`
- Collected: 96 against a baseline of 96
- Kills: 11 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_a_folder_already_in_order_plans_no_writes_and_opens_no_gate`
  - `tests/test_favorites_order.py::test_a_folder_named_as_a_month_is_not_a_month`
  - `tests/test_favorites_order.py::test_a_folder_oldest_first_reads_newest_first_with_all_favorites_first_and_undated_last`
  - `tests/test_favorites_order.py::test_a_landing_that_makes_a_new_month_puts_it_directly_under_all_favorites`
  - `tests/test_favorites_order.py::test_a_non_month_playlist_keeps_its_relative_place_after_the_months`
  - `tests/test_favorites_order.py::test_a_soft_deleted_month_is_neither_moved_nor_counted`
  - `tests/test_favorites_order.py::test_only_a_row_whose_position_changes_is_written`
  - `tests/test_favorites_order.py::test_the_order_takes_the_positions_the_live_children_hold_and_no_other`
  - `tests/test_favorites_order.py::test_the_read_back_names_a_folder_that_does_not_read_in_the_planned_order`
  - `tests/test_favorites_placement.py::test_the_folder_rank_reads_all_favorites_then_months_newest_first_then_undated[2026-11-True-True-rank1]`
  - `tests/test_favorites_placement.py::test_the_folder_rank_reads_all_favorites_then_months_newest_first_then_undated[All Favorites-True-True-rank0]`

Old text:

```
    if source:
        return (RANK_SOURCE, 0)
```

New text:

```
    if False:
        return (RANK_SOURCE, 0)
```

### `u180.M2_newest_first_sign`

folder_rank: the months rank oldest first, the order the brief replaces

- File: `src/cratekit/favorites/placeholders.py`
- Source: `u180.json`, row `M2_newest_first_sign`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_order.py`
- Collected: 96 against a baseline of 96
- Kills: 18 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_a_folder_already_in_order_plans_no_writes_and_opens_no_gate`
  - `tests/test_favorites_order.py::test_a_folder_oldest_first_reads_newest_first_with_all_favorites_first_and_undated_last`
  - `tests/test_favorites_order.py::test_a_landing_that_makes_a_new_month_puts_it_directly_under_all_favorites`
  - `tests/test_favorites_order.py::test_a_non_month_playlist_keeps_its_relative_place_after_the_months`
  - `tests/test_favorites_order.py::test_a_second_run_after_the_order_asks_nothing`
  - `tests/test_favorites_order.py::test_a_soft_deleted_month_is_neither_moved_nor_counted`
  - `tests/test_favorites_order.py::test_only_a_row_whose_position_changes_is_written`
  - `tests/test_favorites_order.py::test_the_order_takes_the_positions_the_live_children_hold_and_no_other`
  - `tests/test_favorites_order.py::test_the_read_back_names_a_folder_that_does_not_read_in_the_planned_order`
  - `tests/test_favorites_order.py::test_the_splits_months_land_in_order`
  - `tests/test_favorites_order.py::test_the_verb_refuses_an_answer_the_read_back_does_not_hold`
  - `tests/test_favorites_order.py::test_the_writer_refuses_an_order_that_reached_a_name`
  - `tests/test_favorites_placement.py::test_a_month_made_in_a_folder_out_of_order_lands_above_every_older_month`
  - `tests/test_favorites_placement.py::test_a_newer_month_ranks_above_an_older_one_across_a_year`
  - `tests/test_favorites_placement.py::test_a_removed_sibling_keeps_its_position_when_a_month_is_seated`
  - ... and 3 more, see the JSON sidecar

Old text:

```
        return (RANK_MONTH, -(int(year) * 12 + int(month)))
```

New text:

```
        return (RANK_MONTH, (int(year) * 12 + int(month)))
```

### `u180.M3_year_coefficient`

folder_rank: a year weighs ten months rather than twelve, so December reads above the January after it

- File: `src/cratekit/favorites/placeholders.py`
- Source: `u180.json`, row `M3_year_coefficient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_order.py`
- Collected: 96 against a baseline of 96
- Kills: 3 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_a_newer_month_ranks_above_an_older_one_across_a_year`
  - `tests/test_favorites_placement.py::test_the_folder_rank_reads_all_favorites_then_months_newest_first_then_undated[2025-12-False-True-rank3]`
  - `tests/test_favorites_placement.py::test_the_folder_rank_reads_all_favorites_then_months_newest_first_then_undated[2026-11-False-True-rank2]`

Old text:

```
        return (RANK_MONTH, -(int(year) * 12 + int(month)))
```

New text:

```
        return (RANK_MONTH, -(int(year) * 10 + int(month)))
```

### `u180.M4_month_must_be_plain`

folder_rank: a folder or smart list named as a month ranks as a month and is moved between the months

- File: `src/cratekit/favorites/placeholders.py`
- Source: `u180.json`, row `M4_month_must_be_plain`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_order.py`
- Collected: 96 against a baseline of 96
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_a_folder_named_as_a_month_is_not_a_month`
  - `tests/test_favorites_placement.py::test_the_folder_rank_reads_all_favorites_then_months_newest_first_then_undated[2026-11-False-False-rank5]`

Old text:

```
    if plain and MONTH_LABEL.fullmatch(text) is not None:
```

New text:

```
    if MONTH_LABEL.fullmatch(text) is not None:
```

### `u180.M5_undated_rank`

folder_rank: Undated ranks with the other playlists rather than directly after the months

- File: `src/cratekit/favorites/placeholders.py`
- Source: `u180.json`, row `M5_undated_rank`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_order.py`
- Collected: 96 against a baseline of 96
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_a_non_month_playlist_keeps_its_relative_place_after_the_months`
  - `tests/test_favorites_placement.py::test_the_folder_rank_reads_all_favorites_then_months_newest_first_then_undated[Undated-False-True-rank4]`

Old text:

```
    if plain and text == UNDATED:
        return (RANK_UNDATED, 0)
```

New text:

```
    if plain and text == UNDATED:
        return (RANK_OTHER, 0)
```

### `u180.M6_undated_after_others`

RANK_UNDATED: Undated reads after every other playlist rather than before them

- File: `src/cratekit/favorites/placeholders.py`
- Source: `u180.json`, row `M6_undated_after_others`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_order.py`
- Collected: 96 against a baseline of 96
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_a_landing_that_makes_a_new_month_puts_it_directly_under_all_favorites`
  - `tests/test_favorites_order.py::test_a_non_month_playlist_keeps_its_relative_place_after_the_months`

Old text:

```
RANK_UNDATED = 2
```

New text:

```
RANK_UNDATED = 4
```

### `u153.C1_is_uncoloured_narrowed`

is_uncoloured: only None counts as unset, so a '0' colour reads coloured and is held not written

- File: `src/cratekit/favorites/colour.py`
- Source: `u153.json`, row `C1_is_uncoloured_narrowed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_pink.py`, `tests/test_favorites_backfill.py`
- Collected: 110 against a baseline of 110
- Kills: 3 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_member_coloured_by_hand_between_the_two_acts_is_refused_by_the_write`
  - `tests/test_favorites_backfill.py::test_the_backfill_colours_the_members_placed_before_it_and_holds_a_coloured_one`
  - `tests/test_favorites_placement.py::test_the_colour_module_sorts_rows_by_what_they_carry`

Old text:

```
    return value in rb_writer.FIELD_EMPTIES[COLUMN]
```

New text:

```
    return value is None
```

### `u153.C2_sort_rows_dedup`

sort_rows: drop the seen check, so a row named twice is sorted and coloured twice

- File: `src/cratekit/favorites/colour.py`
- Source: `u153.json`, row `C2_sort_rows_dedup`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_pink.py`, `tests/test_favorites_backfill.py`
- Collected: 110 against a baseline of 110
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_the_colour_module_sorts_rows_by_what_they_carry`

Old text:

```
        if key in seen:
            continue
```

New text:

```
        if False:
            continue
```

### `u153.C3_sort_rows_missing_row`

sort_rows: do not skip a row the handle cannot find, so an absent id reaches getattr

- File: `src/cratekit/favorites/colour.py`
- Source: `u153.json`, row `C3_sort_rows_missing_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_pink.py`, `tests/test_favorites_backfill.py`
- Collected: 110 against a baseline of 110
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_the_colour_module_sorts_rows_by_what_they_carry`

Old text:

```
        row = find_row(db, key)
        if row is None:
            continue
```

New text:

```
        row = find_row(db, key)
        if row is None:
            to_colour.append(key)
            continue
```

### `u153.C4_sort_rows_uncoloured_branch`

sort_rows: treat every row as uncoloured, so a coloured row is coloured not held

- File: `src/cratekit/favorites/colour.py`
- Source: `u153.json`, row `C4_sort_rows_uncoloured_branch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_pink.py`, `tests/test_favorites_backfill.py`
- Collected: 110 against a baseline of 110
- Kills: 10 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_the_author_took_out_of_all_favorites_is_never_put_back`
  - `tests/test_favorites_backfill.py::test_a_member_coloured_by_hand_between_the_two_acts_is_refused_by_the_write`
  - `tests/test_favorites_backfill.py::test_a_second_run_finds_the_same_hearts_and_writes_nothing`
  - `tests/test_favorites_backfill.py::test_an_unreadable_account_refuses_only_when_a_heart_needs_placing`
  - `tests/test_favorites_backfill.py::test_owned_hearts_not_in_all_favorites_are_planned_by_month_and_those_taken_back_are_named`
  - `tests/test_favorites_backfill.py::test_the_backfill_colours_the_members_placed_before_it_and_holds_a_coloured_one`
  - `tests/test_favorites_placement.py::test_a_recolour_row_takes_pink_and_no_membership`
  - `tests/test_favorites_placement.py::test_a_row_coloured_by_hand_between_two_plans_moves_the_digest`
  - `tests/test_favorites_placement.py::test_the_colour_module_sorts_rows_by_what_they_carry`
  - `tests/test_favorites_placement.py::test_the_plan_names_each_uncoloured_heart_for_pink_and_holds_a_coloured_one`

Old text:

```
        if is_uncoloured(current):
            to_colour.append(key)
```

New text:

```
        if True:
            to_colour.append(key)
```

### `u153.C6_write_pink_fill_only`

write_pink: drop the is_uncoloured re-check, so a colour a person chose is overwritten

- File: `src/cratekit/favorites/colour.py`
- Source: `u153.json`, row `C6_write_pink_fill_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_pink.py`, `tests/test_intake_land_owned_hearts_native.py`
- Collected: 97 against a baseline of 97
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_the_colour_module_sorts_rows_by_what_they_carry`
  - `tests/test_favorites_placement.py::test_the_write_leaves_a_row_coloured_by_hand_after_the_plan`

Old text:

```
        if row is None or not is_uncoloured(getattr(row, COLUMN, None)):
            continue
```

New text:

```
        if row is None:
            continue
```

### `u153.C7_write_pink_reports_write`

write_pink: report every row as coloured, including one the policy skipped

- File: `src/cratekit/favorites/colour.py`
- Source: `u153.json`, row `C7_write_pink_reports_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_pink.py`, `tests/test_favorites_backfill.py`
- Collected: 110 against a baseline of 110
- Kills: 5 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_and_undated_holds_is_not_given_a_month`
  - `tests/test_favorites_backfill.py::test_the_backfill_colours_the_members_placed_before_it_and_holds_a_coloured_one`
  - `tests/test_favorites_placement.py::test_a_recolour_row_takes_pink_and_no_membership`
  - `tests/test_favorites_placement.py::test_the_colour_module_sorts_rows_by_what_they_carry`
  - `tests/test_favorites_placement.py::test_the_write_colours_the_planned_rows_and_only_those`

Old text:

```
        if decision is rb_writer.Decision.WRITE:
            written.append(str(content_id))
```

New text:

```
        if decision is not rb_writer.Decision.WRITE:
            written.append(str(content_id))
```

### `r798-c.H3_every_name_is_resolved_before_any_is_filed`

label held return: skip a name nothing holds and file the rest, so a mistyped identifier leaves a half done run reported as a refusal of nothing

- File: `src/cratekit/label/held_cli.py`
- Source: `r798-c.json`, row `H3_every_name_is_resolved_before_any_is_filed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`, `tests/test_cli_contract.py`
- Collected: 1135 against a baseline of 1135
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_returning_a_release_nothing_holds_refuses_and_files_none_of_the_others`

Old text:

```
        if unknown:
            raise refuse(
                "review-item-unknown",
```

New text:

```
        if False:
            raise refuse(
                "review-item-unknown",
```

### `r798-c.H4_a_release_with_no_isrc_was_not_asked_about`

label held: count a release with no ISRC as one the catalogue was asked about, so it hides a sweep whose every question went unread

- File: `src/cratekit/label/held_cli.py`
- Source: `r798-c.json`, row `H4_a_release_with_no_isrc_was_not_asked_about`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`, `tests/test_cli_contract.py`
- Collected: 1135 against a baseline of 1135
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
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`, `tests/test_cli_contract.py`
- Collected: 1135 against a baseline of 1135
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
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`, `tests/test_label_genre_gate.py`
- Collected: 214 against a baseline of 214
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
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`, `tests/test_label_genre_gate.py`
- Collected: 214 against a baseline of 214
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
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`, `tests/test_label_genre_gate.py`
- Collected: 214 against a baseline of 214
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

### `u243.L1_companion_not_asked`

Tombstoned: the uncredited companion kind is not asked

- File: `src/cratekit/label/tombstoned.py`
- Source: `u243.json`, row `L1_companion_not_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tombstoned.py`, `tests/test_prune.py`, `tests/test_label_playlists.py`
- Collected: 140 against a baseline of 140
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tombstoned.py::test_the_companion_of_a_credited_deletion_answers_for_the_provider_spelling`

Old text:

```
        for kind in (tombstone.KIND_VERSION, tombstone.KIND_VERSION_UNCREDITED):
```

New text:

```
        for kind in (tombstone.KIND_VERSION,):
```

### `u243.L2_revoked_tombstones_count`

Tombstoned: the snapshot includes revoked records, so a lifted deletion still takes the track off

- File: `src/cratekit/label/tombstoned.py`
- Source: `u243.json`, row `L2_revoked_tombstones_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tombstoned.py`, `tests/test_prune.py`, `tests/test_label_playlists.py`
- Collected: 140 against a baseline of 140
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tombstoned.py::test_a_revoked_tombstone_takes_nothing_off`

Old text:

```
                record.suppression_id for record in store.suppressions()
```

New text:

```
                record.suppression_id for record in store.suppressions(include_revoked=True)
```

### `u243.L3_artists_joined_with_ampersand`

track_artist: the billed artists are joined by an ampersand, not as the downloader tags them

- File: `src/cratekit/label/tombstoned.py`
- Source: `u243.json`, row `L3_artists_joined_with_ampersand`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tombstoned.py`, `tests/test_prune.py`, `tests/test_label_playlists.py`
- Collected: 140 against a baseline of 140
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tombstoned.py::test_a_tombstone_matches_the_version_and_every_billed_artist`
  - `tests/test_label_tombstoned.py::test_the_track_words_are_read_as_the_downloader_tags_them`

Old text:

```
        return ", ".join(names)
```

New text:

```
        return " & ".join(names)
```

### `u243.L4_title_without_version`

track_title: the bare name is read before the full name, so the version is dropped

- File: `src/cratekit/label/tombstoned.py`
- Source: `u243.json`, row `L4_title_without_version`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tombstoned.py`, `tests/test_prune.py`, `tests/test_label_playlists.py`
- Collected: 140 against a baseline of 140
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_tombstoned.py::test_a_kept_read_judges_a_track_by_the_words_it_kept`
  - `tests/test_label_tombstoned.py::test_a_tombstone_matches_the_version_and_every_billed_artist`
  - `tests/test_label_tombstoned.py::test_a_tombstone_of_another_version_takes_nothing_off[Label Act-Track t5]`
  - `tests/test_label_tombstoned.py::test_the_track_words_are_read_as_the_downloader_tags_them`

Old text:

```
    for attribute in ("full_name", "name", "title"):
```

New text:

```
    for attribute in ("name", "full_name", "title"):
```

