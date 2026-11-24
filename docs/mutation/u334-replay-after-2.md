# Mutation table: u334-replay-after-2

Measured by `scripts/mutate.py` on 2026-11-24 04:59 UTC, branch `HEAD` at `90c0cc08`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23214 collected. pytest invocations for this batch: 310.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 04:59 UTC for commit `90c0cc0829da`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 48, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23214 against 23214. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u77-c.C4_year_bool` | `src/cratekit/acquire/listdoc.py` | maintainer | 6 file(s) | 254 | 1 | killed |
| `u77-c.C5_source_refs_kept` | `src/cratekit/acquire/listdoc.py` | maintainer | 6 file(s) | 254 | 1 | killed |
| `u78-c.C1_readback_identity` | `src/cratekit/acquire/listdoc.py` | user | 3 file(s) | 109 | 4 | killed |
| `u78-c.C2_readback_count` | `src/cratekit/acquire/listdoc.py` | user | 3 file(s) | 109 | 1 | killed |
| `u78-c.C3_dedupe_lines` | `src/cratekit/acquire/listdoc.py` | maintainer | 3 file(s) | 109 | 1 | killed |
| `u78-c.C4_reason_one_row` | `src/cratekit/acquire/listdoc.py` | user | 3 file(s) | 109 | 1 | killed |
| `u78-c.C5_unlisted_checked_first` | `src/cratekit/acquire/listdoc.py` | user | 3 file(s) | 109 | 5 | killed |
| `u78-c.E2_emitter_checks_rows` | `src/cratekit/acquire/listdoc.py` | user | 1 file(s) | 61 | 3 | killed |
| `r1016.M1_account_walk_back_on_the_clients_method` | `src/cratekit/acquire/listing.py` | user | 7 file(s) | 794 | 14 | killed |
| `r1016.M2_account_parse_through_the_factory` | `src/cratekit/acquire/listing.py` | user | 7 file(s) | 794 | 12 | killed |
| `r1016.M9_offset_not_sent` | `src/cratekit/acquire/listing.py` | user | 7 file(s) | 794 | 10 | killed |
| `r1360.J1_prefix_agrees` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 828 | 5 | killed |
| `r1360.J2_prefix_equal_only` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 828 | 1 | killed |
| `r1360.J3_prefix_always_lags` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 828 | 4 | killed |
| `r1360.J4_prefix_uncounted_lags` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 828 | 2 | killed |
| `r1360.W11_offset_dropped` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 828 | 19 | killed |
| `r1360.W12_tag_unread` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 828 | 13 | killed |
| `r1360.W13_declared_unread` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 828 | 25 | killed |
| `r1360.W14_cap_of_one_walked` | `src/cratekit/acquire/listing.py` | maintainer | 15 file(s) | 828 | 1 | killed |
| `r1360.W15_short_page_walked_past` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 828 | 1 | killed |
| `r1360.W1_no_walk` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 828 | 25 | killed |
| `r1360.W2_walk_no_overlap` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 828 | 19 | killed |
| `r1360.W3_no_start_check` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 828 | 1 | killed |
| `r1360.W4_no_tag_check` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 828 | 4 | killed |
| `r1360.W5_no_length_check` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 828 | 1 | killed |
| `r1360.W6_no_empty_check` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 828 | 1 | killed |
| `r1360.W7_full_page_ends` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 828 | 10 | killed |
| `r1360.W8_overlap_kept` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 828 | 25 | killed |
| `r261.L1_skip_record` | `src/cratekit/acquire/listing.py` | user | 4 file(s) | 522 | 4 | killed |
| `r504-a.A5_listing_no_count` | `src/cratekit/acquire/listing.py` | user | 5 file(s) | 620 | 4 | killed |
| `r504-a.A6_listing_unrecorded` | `src/cratekit/acquire/listing.py` | user | 5 file(s) | 620 | 4 | killed |
| `r504-a.A7_listing_nonpositive` | `src/cratekit/acquire/listing.py` | maintainer | 5 file(s) | 620 | 2 | killed |
| `r888.H1_held_is_paged` | `src/cratekit/acquire/listing.py` | user | 5 file(s) | 578 | 11 | killed |
| `r888.H2_held_not_deduplicated` | `src/cratekit/acquire/listing.py` | user | 5 file(s) | 578 | 1 | killed |
| `r888.H3_unheld_listing_not_recorded` | `src/cratekit/acquire/listing.py` | user | 5 file(s) | 578 | 1 | killed |
| `r888.H4_provider_budget_halved` | `src/cratekit/acquire/listing.py` | user | 5 file(s) | 578 | 1 | killed |
| `r888.H5_abstract_held` | `src/cratekit/acquire/listing.py` | maintainer | 5 file(s) | 578 | 1 | killed |
| `u226.M1_equal_not_agreed` | `src/cratekit/acquire/listing.py` | user | 13 file(s) | 785 | 78 | killed |
| `u226.M4_prefix_as_subset` | `src/cratekit/acquire/listing.py` | user | 13 file(s) | 785 | 3 | killed |
| `u65.B1_favourites_back_to_the_short_page` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 199 | 9 | killed |
| `u65.B3_playlist_tracks_back_to_the_short_page` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 199 | 6 | killed |
| `u65.C4_the_short_page_rule_stops_every_walk` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 199 | 13 | killed |
| `u65.C6_offset_advances_by_what_was_served` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 199 | 10 | killed |
| `u70.E3_hearts_declared_total` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 260 | 4 | killed |
| `r1705.M16_lookup_removed` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3775 | 38 | killed |
| `r1705.M17_lookup_repeats_the_five` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3775 | 4 | killed |
| `r1705.M18_lookup_skips_every_scored` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3775 | 4 | killed |
| `r1705.M19_lookup_after_the_scored` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3775 | 6 | killed |
| `r1705.M20_lookup_counts_in_the_five` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3775 | 38 | killed |
| `r1705.M5_spelled_test_removed` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3775 | 5 | killed |
| `r1705.M6_spelled_test_a_ratio` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3775 | 12 | killed |
| `r1705.M7_spelled_replaces_written` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3775 | 2 | killed |
| `r1705.S1_discovery_floor_raised` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3775 | 28 | killed |
| `r1705.S2_unreadable_title_dropped` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3775 | 15 | killed |
| `r1709.M14_isrc_settled_by_fold` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3858 | 2 | killed |
| `r1709.M15_same_recording_title_guard` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3858 | 3 | killed |
| `r1709.M16_candidates_grouped_by_token` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3858 | 5 | killed |
| `r1709.M18_match_id_token` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3858 | 3 | killed |
| `r1709.M19_search_option_token` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3858 | 1 | killed |
| `r1709.M20_current_option_no_title` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3858 | 2 | killed |
| `r1709.M21_current_option_never_carries` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3858 | 3 | killed |
| `r431-b.B4_the_engine_never_asks` | `src/cratekit/acquire/match.py` | user | 10 file(s) | 1193 | 7 | killed |
| `r431-b.B5_the_engine_ignores_companions_false` | `src/cratekit/acquire/match.py` | user | 10 file(s) | 1193 | 1 | killed |
| `r667-b.B1_same_recording_no_isrc` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 705 | 1 | killed |
| `r667.E2_first_copy_only` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 705 | 2 | killed |
| `r667.F1_credited_reason_is_exact` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 705 | 3 | killed |
| `r667.F2_isrc_version_not_settled` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 705 | 1 | killed |
| `r667.F3_doubtful_not_offered` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 705 | 3 | killed |
| `r667.F4_text_copy_joins_isrc_paths` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 705 | 1 | killed |
| `r667.G12_same_recording_no_credit` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 705 | 1 | killed |
| `r667.G13_isrc_not_consulted` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 705 | 16 | killed |
| `r667.G15_isrc_hit_skips_key` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 705 | 3 | killed |
| `r667.G16_isrc_reason_is_exact` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 705 | 11 | killed |
| `u16-round-8-independent-composites.V24_approximate_limit_raised` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 613 | 10 | killed |
| `u16-round-8-independent.V11_candidate_order_sorted` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 613 | 3 | killed |
| `u16-round-8-independent.V12_approximate_floor_halved` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 613 | 13 | killed |
| `u16-round-8-independent.V13_withheld_not_reported` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 613 | 4 | killed |
| `u16-round-8-independent.V18_rejection_skips_tombstones` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 613 | 2 | killed |
| `u16-round-8-independent.V19_unbound_yes_takes_todays_candidate` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 613 | 2 | killed |
| `u16-round-8-independent.V1_key_check_first_copy_only` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 613 | 2 | killed |
| `u16-round-8-independent.V21_suppression_asked_one_spelling` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 613 | 9 | killed |
| `u16-round-8-independent.V3_version_differs_silently_joins` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 613 | 41 | killed |
| `u16-round-8-independent.V4_fuzzy_becomes_identity` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 613 | 98 | killed |
| `u16-round-8-independent.V5_ambiguous_reading_promoted` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 613 | 28 | killed |
| `u16-round-8-independent.V6_reading_question_never_asked` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 613 | 28 | killed |
| `u16-round-8-independent.V7_tombstoned_counted_missing` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 613 | 28 | killed |
| `u16-round-8-independent.V8_missing_without_options` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 613 | 9 | killed |
| `u16-round-8-independent.V9_relative_key_by_letter` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 613 | 11 | killed |
| `u265.M10_empty_index_scored` | `src/cratekit/acquire/match.py` | maintainer | 24 file(s) | 2712 | 1 | killed |
| `u265.M4_query_not_sorted` | `src/cratekit/acquire/match.py` | user | 24 file(s) | 2712 | 42 | killed |
| `u265.M5_hit_named_by_its_sorted_form` | `src/cratekit/acquire/match.py` | user | 24 file(s) | 2712 | 61 | killed |
| `u265.M8_other_scorer` | `src/cratekit/acquire/match.py` | user | 24 file(s) | 2712 | 25 | killed |
| `u286.M10_swap_either_half` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3775 | 4 | killed |
| `u286.M11_swap_removed` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3775 | 8 | killed |
| `u286.M12_swap_second_half_artist` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3775 | 8 | killed |
| `u286.M13_filter_removed` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3775 | 20 | killed |
| `u286.M14_filter_after_cap` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3775 | 4 | killed |
| `u286.M15_cap_removed` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3775 | 6 | killed |
| `u286.M16_cap_off_by_one` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3775 | 6 | killed |
| `u286.M17_cap_counts_files` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3775 | 3 | killed |
| `u286.M18_resolver_back_to_base` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3775 | 51 | killed |
| `u286.M19_limit_ignored` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3775 | 9 | killed |
| `u286.M1_title_floor_up_one` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3775 | 3 | killed |
| `u286.M2_title_floor_down_one` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3775 | 1 | killed |
| `u286.M3_title_floor_to_sixty` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3775 | 3 | killed |
| `u286.M4_plain_ratio` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3775 | 6 | killed |
| `u286.M6_unreadable_title_not_asked` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3775 | 15 | killed |
| `u286.S1_discovery_floor_up_one` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3775 | 10 | killed |
| `u286.S2_offer_not_truncated` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3775 | 4 | killed |
| `u305.M4_index_library_not_reexported` | `src/cratekit/acquire/match.py` | maintainer | 3 file(s) | 709 | 301 | killed |
| `u305.M5_wanted_not_reexported` | `src/cratekit/acquire/match.py` | maintainer | 3 file(s) | 674 | collection error | collect-error |
| `r1709.M22_adjudicate_not_carried` | `src/cratekit/acquire/match_cli.py` | user | 29 file(s) | 3858 | 1 | killed |
| `r1709.M2_adjudicate_offered_not_carried` | `src/cratekit/acquire/match_cli.py` | user | 29 file(s) | 3858 | 1 | killed |
| `r431-b.B6_the_verb_calls_a_companion_stale` | `src/cratekit/acquire/match_cli.py` | user | 7 file(s) | 928 | 1 | killed |
| `r679-b.B1_no_retirement` | `src/cratekit/acquire/match_cli.py` | user | 3 file(s) | 834 | 7 | killed |
| `r679-b.B2_any_matched_row_is_owned_by_a_rule` | `src/cratekit/acquire/match_cli.py` | user | 3 file(s) | 834 | 1 | killed |
| `r679-b.B3_no_reopen` | `src/cratekit/acquire/match_cli.py` | user | 3 file(s) | 834 | 1 | killed |
| `r679-b.B5_rule_not_recorded` | `src/cratekit/acquire/match_cli.py` | user | 3 file(s) | 834 | 5 | killed |
| `r679-b.B6_one_shape_only` | `src/cratekit/acquire/match_cli.py` | user | 3 file(s) | 834 | 7 | killed |
| `u16-round-8-independent.V22_suppressed_warning_omitted` | `src/cratekit/acquire/match_cli.py` | user | 1 file(s) | 613 | 26 | killed |
| `r1709.M10_title_identity_no_separator` | `src/cratekit/acquire/match_identity.py` | user | 29 file(s) | 3858 | 1 | killed |
| `r1709.M11_recording_identity_is_the_token` | `src/cratekit/acquire/match_identity.py` | user | 29 file(s) | 3858 | 24 | killed |
| `r1709.M17_question_identity_token` | `src/cratekit/acquire/match_identity.py` | user | 29 file(s) | 3858 | 3 | killed |
| `r1709.M1_bare_no_nfkc` | `src/cratekit/acquire/match_identity.py` | user | 29 file(s) | 3858 | 2 | killed |
| `r1709.M3_bare_keeps_spaces` | `src/cratekit/acquire/match_identity.py` | user | 29 file(s) | 3858 | 1 | killed |
| `r1709.M4_bare_keeps_invisible` | `src/cratekit/acquire/match_identity.py` | user | 29 file(s) | 3858 | 5 | killed |
| `r1709.M5_no_variation_selectors` | `src/cratekit/acquire/match_identity.py` | user | 29 file(s) | 3858 | 3 | killed |
| `r1709.M6_no_format_characters` | `src/cratekit/acquire/match_identity.py` | user | 29 file(s) | 3858 | 2 | killed |
| `r1709.M7_tag_characters_dropped` | `src/cratekit/acquire/match_identity.py` | user | 29 file(s) | 3858 | 1 | killed |
| `r1709.M8_bare_for_every_title` | `src/cratekit/acquire/match_identity.py` | user | 29 file(s) | 3858 | 1 | killed |
| `r1709.M9_title_identity_is_the_fold` | `src/cratekit/acquire/match_identity.py` | user | 29 file(s) | 3858 | 30 | killed |
| `r431-b.B7_the_engine_asks_under_the_tombstones_kind` | `src/cratekit/acquire/match_identity.py` | user | 10 file(s) | 1193 | 8 | killed |
| `r667.G3_members_not_split` | `src/cratekit/acquire/match_identity.py` | user | 3 file(s) | 705 | 6 | killed |
| `r679-b.C1_credited_rule_not_owning` | `src/cratekit/acquire/match_identity.py` | user | 3 file(s) | 834 | 2 | killed |
| `r679-b.C2_reading_shape_missing` | `src/cratekit/acquire/match_identity.py` | user | 3 file(s) | 834 | 1 | killed |
| `u16-round-8-independent.V14_tombstone_fold_nfd` | `src/cratekit/acquire/match_identity.py` | user | 1 file(s) | 613 | 4 | killed |
| `u16-round-8-independent.V15_empty_identity_accepted` | `src/cratekit/acquire/match_identity.py` | user | 1 file(s) | 613 | 1 | killed |
| `u16-round-8-independent.V16_key_leaves_item_identity` | `src/cratekit/acquire/match_identity.py` | user | 1 file(s) | 613 | 3 | killed |
| `u16-round-8-independent.V20_digest_width_halved` | `src/cratekit/acquire/match_identity.py` | maintainer | 1 file(s) | 613 | 3 | killed |
| `u213.M1_first_group_is_the_title` | `src/cratekit/acquire/match_identity.py` | user | 3 file(s) | 726 | 13 | killed |
| `u213.M21_first_group_version_check` | `src/cratekit/acquire/match_identity.py` | user | 3 file(s) | 741 | 6 | killed |
| `u213.M22_names_a_version_last_word` | `src/cratekit/acquire/match_identity.py` | user | 3 file(s) | 741 | 2 | killed |
| `u213.M3_first_group_position` | `src/cratekit/acquire/match_identity.py` | user | 3 file(s) | 726 | 16 | killed |
| `u213.M4_first_group_keeps_brackets` | `src/cratekit/acquire/match_identity.py` | user | 3 file(s) | 726 | 15 | killed |
| `u262.C1_letters_rule_back` | `src/cratekit/acquire/match_identity.py` | user | 3 file(s) | 685 | 15 | killed |
| `u262.C2_any_word` | `src/cratekit/acquire/match_identity.py` | user | 3 file(s) | 685 | 1 | killed |
| `u262.C3_last_word` | `src/cratekit/acquire/match_identity.py` | user | 3 file(s) | 685 | 32 | killed |
| `u262.C4_unfolded_words` | `src/cratekit/acquire/match_identity.py` | user | 3 file(s) | 685 | 26 | killed |
| `u262.C5_no_with` | `src/cratekit/acquire/match_identity.py` | user | 3 file(s) | 685 | 7 | killed |
| `u262.C6_no_ft` | `src/cratekit/acquire/match_identity.py` | user | 3 file(s) | 685 | 9 | killed |
| `u262.C7_no_featuring` | `src/cratekit/acquire/match_identity.py` | user | 3 file(s) | 685 | 4 | killed |
| `u262.C8_no_feat` | `src/cratekit/acquire/match_identity.py` | user | 3 file(s) | 685 | 19 | killed |
| `u265.M1_narrow_split_everywhere` | `src/cratekit/acquire/match_identity.py` | user | 24 file(s) | 2712 | 2 | killed |
| `u265.M2_python_split_everywhere` | `src/cratekit/acquire/match_identity.py` | user | 24 file(s) | 2712 | 2 | killed |
| `u265.M2b_width_off_by_one` | `src/cratekit/acquire/match_identity.py` | user | 24 file(s) | 2712 | 1 | killed |
| `u265.M3_words_not_sorted` | `src/cratekit/acquire/match_identity.py` | user | 24 file(s) | 2712 | 18 | killed |
| `u269.M7_match_engine_binds_lxml` | `src/cratekit/acquire/match_identity.py` | maintainer | 1 file(s) | 613 | 2 | killed |
| `u305.M1_recorded_recording_swapped` | `src/cratekit/acquire/match_identity.py` | user | 2 file(s) | 642 | 71 | killed |
| `u305.M2_recorded_distinct_is_the_token` | `src/cratekit/acquire/match_identity.py` | user | 2 file(s) | 642 | 15 | killed |
| `u305.M3_recorded_version_key_unfolded` | `src/cratekit/acquire/match_identity.py` | user | 2 file(s) | 163 | 3 | killed |
| `r1705.M10_holds_always` | `src/cratekit/acquire/match_library.py` | user | 27 file(s) | 3775 | 4 | killed |
| `r1705.M11_holds_reads_artist` | `src/cratekit/acquire/match_library.py` | user | 27 file(s) | 3775 | 38 | killed |
| `r1705.M12_lookup_ignores_wanted_side` | `src/cratekit/acquire/match_library.py` | user | 27 file(s) | 3775 | 28 | killed |
| `r1705.M13_lookup_ignores_held_side` | `src/cratekit/acquire/match_library.py` | user | 27 file(s) | 3775 | 25 | killed |
| `r1705.M14_lookup_key_drops_artist` | `src/cratekit/acquire/match_library.py` | user | 27 file(s) | 3775 | 6 | killed |
| `r1705.M15_lookup_key_spells_artist` | `src/cratekit/acquire/match_library.py` | user | 27 file(s) | 3775 | 1 | killed |
| `r1705.M1_luv_unlisted` | `src/cratekit/acquire/match_library.py` | user | 27 file(s) | 3775 | 15 | killed |
| `r1705.M2_four_numeral_unlisted` | `src/cratekit/acquire/match_library.py` | user | 27 file(s) | 3775 | 14 | killed |
| `r1705.M3_too_unlisted` | `src/cratekit/acquire/match_library.py` | user | 27 file(s) | 3775 | 3 | killed |
| `r1705.M4_2nite_unlisted` | `src/cratekit/acquire/match_library.py` | user | 27 file(s) | 3775 | 2 | killed |
| `r1705.M8_spelled_keeps_spaces` | `src/cratekit/acquire/match_library.py` | user | 27 file(s) | 3775 | 7 | killed |
| `r1705.M9_spelled_spells_nothing` | `src/cratekit/acquire/match_library.py` | user | 27 file(s) | 3775 | 52 | killed |
| `r1709.M12_held_exact_unfiltered` | `src/cratekit/acquire/match_library.py` | user | 29 file(s) | 3858 | 14 | killed |
| `r1709.M13_held_credited_by_fold` | `src/cratekit/acquire/match_library.py` | user | 29 file(s) | 3858 | 9 | killed |
| `r664.E1_stem_head_kept` | `src/cratekit/acquire/match_library.py` | user | 10 file(s) | 1193 | 149 | killed |
| `r664.E2_pair_rule_field_by_field` | `src/cratekit/acquire/match_library.py` | user | 10 file(s) | 1193 | 1 | killed |
| `r664.E4_title_not_split` | `src/cratekit/acquire/match_library.py` | user | 10 file(s) | 1193 | 106 | killed |
| `r667-b.B2_reader_isrc_unfolded` | `src/cratekit/acquire/match_library.py` | user | 3 file(s) | 705 | 2 | killed |
| `r667.E1_title_head_kept` | `src/cratekit/acquire/match_library.py` | user | 3 file(s) | 705 | 33 | killed |
| `r667.G17_reader_drops_isrc` | `src/cratekit/acquire/match_library.py` | user | 3 file(s) | 705 | 17 | killed |
| `r667.G4_members_not_folded` | `src/cratekit/acquire/match_library.py` | user | 3 file(s) | 705 | 5 | killed |
| `r667.G5_empty_isrc_asks` | `src/cratekit/acquire/match_library.py` | user | 3 file(s) | 705 | 1 | killed |
| `r667.G8_no_credited_rule` | `src/cratekit/acquire/match_library.py` | user | 3 file(s) | 705 | 6 | killed |
| `u249.M01_path_alone` | `src/cratekit/acquire/match_library.py` | user | 4 file(s) | 780 | 7 | killed |
| `u249.M02_size_out_of_stamp` | `src/cratekit/acquire/match_library.py` | user | 4 file(s) | 780 | 2 | killed |
| `u249.M03_mtime_out_of_stamp` | `src/cratekit/acquire/match_library.py` | user | 4 file(s) | 780 | 1 | killed |
| `u249.M04_ctime_out_of_stamp` | `src/cratekit/acquire/match_library.py` | user | 4 file(s) | 780 | 1 | killed |
| `u249.M05_inode_out_of_stamp` | `src/cratekit/acquire/match_library.py` | user | 4 file(s) | 780 | 1 | killed |
| `u249.M06_device_out_of_stamp` | `src/cratekit/acquire/match_library.py` | user | 4 file(s) | 780 | 1 | killed |
| `u249.M07_size_not_stat` | `src/cratekit/acquire/match_library.py` | user | 4 file(s) | 780 | 2 | killed |
| `u249.M08_template_out_of_key` | `src/cratekit/acquire/match_library.py` | user | 4 file(s) | 780 | 1 | killed |
| `u249.M09_no_window` | `src/cratekit/acquire/match_library.py` | user | 4 file(s) | 780 | 4 | killed |
| `u249.M10_window_halved` | `src/cratekit/acquire/match_library.py` | user | 4 file(s) | 780 | 3 | killed |
| `u249.M11_window_boundary` | `src/cratekit/acquire/match_library.py` | maintainer | 4 file(s) | 780 | 1 | killed |
| `u249.M12_moment_after_read` | `src/cratekit/acquire/match_library.py` | user | 4 file(s) | 780 | 1 | killed |
| `u249.M13_failed_read_remembered` | `src/cratekit/acquire/match_library.py` | user | 4 file(s) | 780 | 3 | killed |
| `u249.M14_unstated_remembered_never` | `src/cratekit/acquire/match_library.py` | user | 4 file(s) | 780 | 11 | killed |
| `u249.M20_reset_forgets_nothing` | `src/cratekit/acquire/match_library.py` | maintainer | 4 file(s) | 780 | 6 | killed |
| `u249.M20a_failed_read_keeps_old_entry` | `src/cratekit/acquire/match_library.py` | user | 4 file(s) | 780 | 1 | killed |
| `u265.M6_cache_misaligned` | `src/cratekit/acquire/match_library.py` | user | 24 file(s) | 2712 | 15 | killed |
| `u265.M7_cache_never_kept` | `src/cratekit/acquire/match_library.py` | maintainer | 24 file(s) | 2712 | 1 | killed |
| `u327.A25_index_reads_title_key_first` | `src/cratekit/acquire/match_library.py` | user | 1 file(s) | 613 | 1 | killed |
| `r431-b.B1_a_wanted_built_by_hand_asks` | `src/cratekit/acquire/match_list.py` | user | 10 file(s) | 1193 | 2 | killed |
| `r431-b.B2_a_row_billing_a_guest_asks` | `src/cratekit/acquire/match_list.py` | user | 10 file(s) | 1193 | 2 | killed |
| `r431-b.B3_a_listing_that_spelled_a_credit_asks` | `src/cratekit/acquire/match_list.py` | user | 10 file(s) | 1193 | 7 | killed |
| `r431-b.B8_the_reader_never_counts_the_artists` | `src/cratekit/acquire/match_list.py` | user | 10 file(s) | 1193 | 2 | killed |
| `u213.M5_listed_names_artist` | `src/cratekit/acquire/match_list.py` | user | 3 file(s) | 726 | 3 | killed |
| `r1305.L1_login_name_on_any_link` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 207 | 1 | killed |
| `r1305.L2_login_status_declared_only` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 207 | 5 | killed |
| `r1305.L3_login_name_dropped` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 207 | 1 | killed |
| `r1694.L1_login_no_tolerance` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 164 | 7 | killed |
| `r1694.L2_token_file_uncaught` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 164 | 1 | killed |
| `r1694.L3_token_file_catches_defect` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 164 | 1 | killed |
| `r1694.L4_rewrite_unchanged` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 164 | 2 | killed |
| `r1694.L5_hold_the_refresh` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 164 | 2 | killed |
| `r1694.L6_no_note` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 164 | 8 | killed |
| `r1694.L7_note_the_words` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 164 | 7 | killed |
| `r1694.S1_tolerance_reraises` | `src/cratekit/acquire/provider_session.py` | user | 4 file(s) | 208 | 7 | killed |
| `r1694.S2_tolerance_always` | `src/cratekit/acquire/provider_session.py` | user | 4 file(s) | 208 | 3 | killed |
| `r1694.S3_catch_everything` | `src/cratekit/acquire/provider_session.py` | user | 4 file(s) | 208 | 1 | killed |
| `r1694.S4_failures_no_credential` | `src/cratekit/acquire/provider_session.py` | user | 4 file(s) | 208 | 8 | killed |
| `r1694.S5_failures_no_cratekit` | `src/cratekit/acquire/provider_session.py` | user | 4 file(s) | 208 | 2 | killed |
| `r705-b.S2_client_session_never_attaches` | `src/cratekit/acquire/provider_session.py` | user | 1 file(s) | 118 | 16 | killed |
| `u261.H1_reuse_skips_the_gate` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 213 | 1 | killed |
| `u261.H2_reuse_ignores_a_replaced_session` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 208 | 4 | killed |
| `u261.H3_reuse_swallows_a_missing_session` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 142 | 2 | killed |
| `u261.H4_failed_read_keeps_the_hold` | `src/cratekit/acquire/provider_session.py` | maintainer | 2 file(s) | 142 | 1 | killed |
| `u261.H5_settings_not_in_the_key` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 147 | 1 | killed |
| `u261.H6_app_not_asked_again` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 95 | 3 | killed |
| `u261.H7_nothing_held` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 208 | 11 | killed |
| `u261.H8_blob_is_the_stored_not_the_refresh` | `src/cratekit/acquire/provider_session.py` | maintainer | 1 file(s) | 29 | 1 | killed |
| `u261.H9_no_forget_before_a_new_login` | `src/cratekit/acquire/provider_session.py` | maintainer | 2 file(s) | 142 | 1 | killed |
| `u261.R1_watch_not_installed` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 208 | 3 | killed |
| `u261.R2_answered_refusal_ignored` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 208 | 2 | killed |
| `u261.R3_raised_refusal_ignored` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 142 | 1 | killed |
| `u261.R4_forbidden_not_a_refusal` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 175 | 4 | killed |
| `u261.R5_drop_not_by_identity` | `src/cratekit/acquire/provider_session.py` | maintainer | 1 file(s) | 29 | 2 | killed |
| `u261.W1_unchanged_skip_removed` | `src/cratekit/acquire/provider_session.py` | user | 5 file(s) | 483 | 4 | killed |
| `u261.W2_changed_session_skipped` | `src/cratekit/acquire/provider_session.py` | user | 5 file(s) | 483 | 5 | killed |
| `u261.W3_compare_by_value_not_bytes` | `src/cratekit/acquire/provider_session.py` | maintainer | 2 file(s) | 186 | 1 | killed |
| `u274.P4_sweep_live` | `src/cratekit/acquire/provider_session.py` | user | 6 file(s) | 449 | 5 | killed |
| `u62.S1_device_flow_login` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 331 | 1 | killed |
| `u62.S2_401_not_rejected` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 331 | 2 | killed |
| `u62.S4_every_failure_rejected` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 331 | 4 | killed |
| `u62.S5_blob_without_token_logged_in` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 331 | 1 | killed |
| `u62.S6_refresh_not_written_back` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 331 | 1 | killed |
| `u62.S7_naive_expiry_as_local` | `src/cratekit/acquire/provider_session.py` | maintainer | 2 file(s) | 23214 | 0 (promoted) | zero |
| `r703-a.V6_sample_no_park_check` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 275 | 2 | killed |
| `r705-b.S3_vendored_never_asks_before_login` | `src/cratekit/acquire/vendored.py` | user | 1 file(s) | 118 | 1 | killed |
| `r705-b.S4_vendored_never_attaches_to_the_tool` | `src/cratekit/acquire/vendored.py` | user | 1 file(s) | 118 | 1 | killed |
| `r705-b.S5_vendored_never_asks_after_login` | `src/cratekit/acquire/vendored.py` | user | 1 file(s) | 118 | 1 | killed |
| `u254.M07_always_append` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 743 | 86 | killed |
| `r239-b.S10_adopt_apply_key_off` | `src/cratekit/adopt/apply_cli.py` | user | 7 file(s) | 724 | 1 | killed |
| `r797-c.G1_the_threshold_is_fifty` | `src/cratekit/adopt/genres.py` | user | 1 file(s) | 33 | 7 | killed |
| `r797-c.G2_at_the_threshold_is_named` | `src/cratekit/adopt/genres.py` | user | 1 file(s) | 33 | 4 | killed |
| `r797-c.G3_a_removed_row_is_not_counted` | `src/cratekit/adopt/genres.py` | user | 1 file(s) | 33 | 1 | killed |
| `r797-c.G4_no_genre_is_not_a_genre` | `src/cratekit/adopt/genres.py` | user | 1 file(s) | 33 | 3 | killed |
| `r797-c.G5_another_spelling_is_the_same_genre` | `src/cratekit/adopt/genres.py` | user | 1 file(s) | 33 | 3 | killed |
| `u343.M01_finalize_no_mark` | `src/cratekit/analysis/cli.py` | user | 5 file(s) | 536 | 9 | killed |
| `u343.M02_finalize_writes_a_key` | `src/cratekit/analysis/cli.py` | user | 3 file(s) | 482 | 6 | killed |

## Zero rows and what they owe

- `u62.S7_naive_expiry_as_local` (maintainer facing): maintainer facing, composite not required

## Row definitions

### `u77-c.C4_year_bool`

_manifest_row: drop the boolean test on the year, so a year of true is read as the year 1

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u77-c.json`, row `C4_year_bool`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 254 against a baseline of 254
- Kills: 1 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_manifest_this_build_did_not_write_is_refused_whole[{"manifest": 1, "rows": {"1": {"source": "label", "year": true}}}-year]`

Old text:

```
if year is not None and (isinstance(year, bool) or not isinstance(year, int)):
```

New text:

```
if year is not None and not isinstance(year, int):
```

### `u77-c.C5_source_refs_kept`

_manifest_row: read every entry's source_refs as empty, so the other sources that asked for an id are lost on the way back

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u77-c.json`, row `C5_source_refs_kept`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 254 against a baseline of 254
- Kills: 1 (killed)
- Killed:
  - `tests/test_listdoc.py::test_every_source_that_asked_for_an_id_reads_back`

Old text:

```
            source_refs=tuple(asked),

```

New text:

```
            source_refs=(),

```

### `u78-c.C1_readback_identity`

The text line read back compares only that one track came back, not which

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u78-c.json`, row `C1_readback_identity`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 109 against a baseline of 109
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_a_track_that_cannot_be_a_text_line_is_named_and_the_rest_are_still_written`
  - `tests/test_intake_missing_isrc.py::test_missing_tracks_none_named_and_none_writable_refuse_rather_than_no_op`
  - `tests/test_listdoc.py::test_a_row_that_would_read_back_as_another_track_is_refused_by_position[leading-ordinal]`
  - `tests/test_listdoc.py::test_a_row_that_would_read_back_as_another_track_is_refused_by_position[separator-in-artist]`

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

### `u78-c.C2_readback_count`

The text line read back no longer requires exactly one track, so a line read as a comment passes

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u78-c.json`, row `C2_readback_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 109 against a baseline of 109
- Kills: 1 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_row_that_would_read_back_as_another_track_is_refused_by_position[read-as-a-comment]`

Old text:

```
    if len(again) != 1 or (again[0].recording, again[0].version_key) != (
```

New text:

```
    if again and (again[0].recording, again[0].version_key) != (
```

### `u78-c.C3_dedupe_lines`

The same line twice is written twice

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u78-c.json`, row `C3_dedupe_lines`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 109 against a baseline of 109
- Kills: 1 (killed)
- Killed:
  - `tests/test_listdoc.py::test_the_same_line_twice_is_written_once_under_its_first_reason`

Old text:

```
        if line in seen:
            continue
        seen.add(line)
```

New text:

```
        seen.add(line)
```

### `u78-c.C4_reason_one_row`

A reason carrying a line break is written as it stands, so the text reader refuses the whole file

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u78-c.json`, row `C4_reason_one_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 109 against a baseline of 109
- Kills: 1 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_reason_carrying_a_line_break_stays_one_row`

Old text:

```
        tracks.extend((f"# {' '.join(str(entry.reason).split())}", line))
```

New text:

```
        tracks.extend((f"# {entry.reason}", line))
```

### `u78-c.C5_unlisted_checked_first`

The unlisted file is written over whatever is there, after the list, rather than checked with the other two

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u78-c.json`, row `C5_unlisted_checked_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 109 against a baseline of 109
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_a_one_id_isrc_is_listed_and_two_ids_and_no_isrc_are_handed_on`
  - `tests/test_listdoc.py::test_a_row_that_would_read_back_as_another_track_is_refused_by_position[leading-ordinal]`
  - `tests/test_listdoc.py::test_a_row_that_would_read_back_as_another_track_is_refused_by_position[read-as-a-comment]`
  - `tests/test_listdoc.py::test_a_row_that_would_read_back_as_another_track_is_refused_by_position[separator-in-artist]`
  - `tests/test_listdoc.py::test_an_existing_different_unlisted_file_refuses_before_either_half_is_written`

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

### `u78-c.E2_emitter_checks_rows`

Existing guard sample: the emitter no longer reads each listed row back through the reader

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u78-c.json`, row `E2_emitter_checks_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 3 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_row_the_reader_would_refuse_is_refused_by_the_emitter[no-artist]`
  - `tests/test_listdoc.py::test_a_row_the_reader_would_refuse_is_refused_by_the_emitter[no-title]`
  - `tests/test_listdoc.py::test_a_row_the_reader_would_refuse_is_refused_by_the_emitter[only-a-version]`

Old text:

```
        _checked(track, position)
```

New text:

```
(empty)
```

### `r1016.M1_account_walk_back_on_the_clients_method`

The account walk calls the client's playlist_and_favorite_playlists again, which parses through parse_factory and fetches every owned playlist, the defect itself

- File: `src/cratekit/acquire/listing.py`
- Source: `r1016.json`, row `M1_account_walk_back_on_the_clients_method`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/modules/test_labels.py`, `tests/test_provider_gate.py`, `tests/intake/test_workers.py`
- Collected: 794 against a baseline of 794
- Kills: 14 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_listed_playlist_carries_the_fields_the_callers_read`
  - `tests/test_adapter_listing.py::test_a_listing_of_624_playlists_is_paced_in_seconds_not_minutes`
  - `tests/test_adapter_listing.py::test_a_user_without_the_parts_the_account_walk_reaches_is_refused_by_name`
  - `tests/test_adapter_listing.py::test_account_playlists_are_returned_unfiltered`
  - `tests/test_adapter_listing.py::test_account_playlists_page_and_deduplicate`
  - `tests/test_adapter_listing.py::test_an_account_answer_that_is_not_a_page_is_refused_not_read_as_the_end[a-list]`
  - `tests/test_adapter_listing.py::test_an_account_answer_that_is_not_a_page_is_refused_not_read_as_the_end[an-error-body]`
  - `tests/test_adapter_listing.py::test_an_account_answer_that_is_not_a_page_is_refused_not_read_as_the_end[items-null]`
  - `tests/test_adapter_listing.py::test_an_account_listing_of_owned_playlists_costs_its_pages_and_no_single_fetch`
  - `tests/test_adapter_listing.py::test_an_account_request_that_rejects_the_arguments_refuses_by_name_unslept`
  - `tests/test_adapter_listing.py::test_the_account_playlists_listing_reads_to_the_end_at_its_own_page_size`
  - `tests/test_adapter_listing.py::test_the_catalogue_and_the_folder_reads_hand_the_plans_what_the_pages_said`
  - `tests/test_label_tidal_catalogue.py::test_the_account_listing_keeps_the_playlists_the_account_created`
  - `tests/test_label_tidal_catalogue.py::test_the_account_listing_pages_past_the_first_page`

Old text:

```
    return paginate(
        _account_playlists_endpoint(session.user),
        **_shape("account_playlists", **kwargs),
    )
```

New text:

```
    return paginate(
        _paged_caller(session.user, "playlist_and_favorite_playlists"),
        **_shape("account_playlists", **kwargs),
    )
```

### `r1016.M2_account_parse_through_the_factory`

The account walk keeps its own request but parses with parse_factory, so every owned playlist is fetched again

- File: `src/cratekit/acquire/listing.py`
- Source: `r1016.json`, row `M2_account_parse_through_the_factory`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/modules/test_labels.py`, `tests/test_provider_gate.py`, `tests/intake/test_workers.py`
- Collected: 794 against a baseline of 794
- Kills: 12 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_listed_playlist_carries_the_fields_the_callers_read`
  - `tests/test_adapter_listing.py::test_a_listing_of_624_playlists_is_paced_in_seconds_not_minutes`
  - `tests/test_adapter_listing.py::test_account_playlists_are_returned_unfiltered`
  - `tests/test_adapter_listing.py::test_account_playlists_page_and_deduplicate`
  - `tests/test_adapter_listing.py::test_an_account_answer_that_is_not_a_page_is_refused_not_read_as_the_end[a-list]`
  - `tests/test_adapter_listing.py::test_an_account_answer_that_is_not_a_page_is_refused_not_read_as_the_end[an-error-body]`
  - `tests/test_adapter_listing.py::test_an_account_answer_that_is_not_a_page_is_refused_not_read_as_the_end[items-null]`
  - `tests/test_adapter_listing.py::test_an_account_listing_of_owned_playlists_costs_its_pages_and_no_single_fetch`
  - `tests/test_adapter_listing.py::test_the_account_playlists_listing_reads_to_the_end_at_its_own_page_size`
  - `tests/test_adapter_listing.py::test_the_catalogue_and_the_folder_reads_hand_the_plans_what_the_pages_said`
  - `tests/test_label_tidal_catalogue.py::test_the_account_listing_keeps_the_playlists_the_account_created`
  - `tests/test_label_tidal_catalogue.py::test_the_account_listing_pages_past_the_first_page`

Old text:

```
    parse = _client_part(user, "playlist", "parse", walk=walk)
```

New text:

```
    parse = _client_part(user, "playlist", "parse_factory", walk=walk)
```

### `r1016.M9_offset_not_sent`

The account request always asks for offset 0, so the walk reads its first page until the budget raises

- File: `src/cratekit/acquire/listing.py`
- Source: `r1016.json`, row `M9_offset_not_sent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/modules/test_labels.py`, `tests/test_provider_gate.py`, `tests/intake/test_workers.py`
- Collected: 794 against a baseline of 794
- Kills: 10 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_listed_playlist_carries_the_fields_the_callers_read`
  - `tests/test_adapter_listing.py::test_a_listed_playlist_still_reads_its_tracks_through_the_playlist`
  - `tests/test_adapter_listing.py::test_a_listing_of_624_playlists_is_paced_in_seconds_not_minutes`
  - `tests/test_adapter_listing.py::test_account_playlists_are_returned_unfiltered`
  - `tests/test_adapter_listing.py::test_account_playlists_page_and_deduplicate`
  - `tests/test_adapter_listing.py::test_an_account_listing_of_owned_playlists_costs_its_pages_and_no_single_fetch`
  - `tests/test_adapter_listing.py::test_the_account_playlists_listing_reads_to_the_end_at_its_own_page_size`
  - `tests/test_adapter_listing.py::test_the_catalogue_and_the_folder_reads_hand_the_plans_what_the_pages_said`
  - `tests/test_label_tidal_catalogue.py::test_the_account_listing_keeps_the_playlists_the_account_created`
  - `tests/test_label_tidal_catalogue.py::test_the_account_listing_pages_past_the_first_page`

Old text:

```
params={"limit": limit, "offset": offset})
```

New text:

```
params={"limit": limit, "offset": 0})
```

### `r1360.J1_prefix_agrees`

judge_window: a first part beside a whole window agrees, as U226 left it

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `J1_prefix_agrees`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 828 against a baseline of 828
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_later_pages_lag_too_is_held_with_nothing_taken_off`
  - `tests/test_outbound_window_lag.py::test_an_order_whose_later_pages_lag_too_is_held_with_nothing_moved`
  - `tests/test_outbound_window_lag.py::test_the_judge_reads_the_two_reads_against_the_declared_count[paged6-unpaged6-4-lags]`
  - `tests/test_outbound_window_lag.py::test_the_judge_reads_the_two_reads_against_the_declared_count[paged7-unpaged7-4-lags]`
  - `tests/test_outbound_window_lag.py::test_the_judge_reads_the_two_reads_against_the_declared_count[paged8-unpaged8-4-lags]`

Old text:

```
        return WINDOW_LAGS if counted and len(paged) >= declared else WINDOW_AGREES
```

New text:

```
        return WINDOW_AGREES
```

### `r1360.J2_prefix_equal_only`

judge_window: a first part lags only beside a window of exactly the count

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `J2_prefix_equal_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 828 against a baseline of 828
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_the_judge_reads_the_two_reads_against_the_declared_count[paged8-unpaged8-4-lags]`

Old text:

```
counted and len(paged) >= declared else
```

New text:

```
counted and len(paged) == declared else
```

### `r1360.J3_prefix_always_lags`

judge_window: a first part beside a window short of the count lags too

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `J3_prefix_always_lags`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 828 against a baseline of 828
- Kills: 4 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_the_judge_reads_the_two_reads_against_the_declared_count[paged4-unpaged4-4-agrees]`
  - `tests/test_outbound_window_lag.py::test_the_judge_reads_the_two_reads_against_the_declared_count[paged5-unpaged5-4-agrees]`
  - `tests/test_outbound_window_lag.py::test_the_judge_reads_the_two_reads_against_the_declared_count[paged9-unpaged9-None-agrees]`
  - `tests/test_sync_pair_window_lag.py::test_a_window_that_starts_lagging_after_the_plan_stops_the_write_as_moved`

Old text:

```
        return WINDOW_LAGS if counted and len(paged) >= declared else WINDOW_AGREES
```

New text:

```
        return WINDOW_LAGS
```

### `r1360.J4_prefix_uncounted_lags`

judge_window: a first part beside a playlist declaring no count lags

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `J4_prefix_uncounted_lags`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 828 against a baseline of 828
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_the_judge_reads_the_two_reads_against_the_declared_count[paged9-unpaged9-None-agrees]`
  - `tests/test_sync_pair_window_lag.py::test_a_window_that_starts_lagging_after_the_plan_stops_the_write_as_moved`

Old text:

```
WINDOW_LAGS if counted and len(paged) >= declared else
```

New text:

```
WINDOW_LAGS if not counted or len(paged) >= declared else
```

### `r1360.W11_offset_dropped`

playlist_tracks_unpaged: a later request is asked with no offset

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `W11_offset_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 828 against a baseline of 828
- Kills: 19 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_first_reading_whose_window_lags_is_read_again_before_any_move`
  - `tests/test_outbound_window_lag.py::test_a_long_playlist_nothing_changed_is_read_whole_and_written_once`
  - `tests/test_outbound_window_lag.py::test_a_removal_past_the_first_hundred_takes_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_once_is_read_again_and_lands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_window_lags_beside_a_first_page_refuses_after_the_bound`
  - `tests/test_outbound_window_lag.py::test_a_window_that_catches_up_beside_a_first_page_settles_as_done`
  - `tests/test_outbound_window_lag.py::test_a_window_that_lags_beside_a_first_page_is_not_read_back_between_moves`
  - `tests/test_outbound_window_lag.py::test_an_order_past_the_first_hundred_moves_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_each_later_page_goes_through_the_retry_ladder`
  - `tests/test_outbound_window_lag.py::test_every_judged_reading_records_its_readings_and_wait`
  - `tests/test_outbound_window_lag.py::test_the_unpaged_read_walks_past_a_capped_first_page_one_track_back`
  - `tests/test_outbound_window_lag.py::test_the_walk_ends_at_the_page_that_cannot_follow_the_last[a-short-later-page]`
  - `tests/test_outbound_window_lag.py::test_the_walk_stops_once_it_holds_the_declared_count`
  - `tests/test_sync_pair_calls.py::test_a_300_track_order_with_adds_and_removals_stays_inside_its_forecast`
  - `tests/test_sync_pair_calls.py::test_an_existing_playlists_removals_and_additions_cost_what_is_expected[120-51-0]`
  - ... and 4 more, see the JSON sidecar

Old text:

```
                return playlist.tracks(offset=offset) if offset else playlist.tracks()
```

New text:

```
                return playlist.tracks()
```

### `r1360.W12_tag_unread`

playlist_tracks_unpaged: the first page's tag is not read, so no walk holds together where a client keeps one

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `W12_tag_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 828 against a baseline of 828
- Kills: 13 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_first_reading_whose_window_lags_is_read_again_before_any_move`
  - `tests/test_outbound_window_lag.py::test_a_long_playlist_nothing_changed_is_read_whole_and_written_once`
  - `tests/test_outbound_window_lag.py::test_a_removal_past_the_first_hundred_takes_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_once_is_read_again_and_lands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_window_lags_beside_a_first_page_refuses_after_the_bound`
  - `tests/test_outbound_window_lag.py::test_a_window_that_catches_up_beside_a_first_page_settles_as_done`
  - `tests/test_outbound_window_lag.py::test_a_window_that_lags_beside_a_first_page_is_not_read_back_between_moves`
  - `tests/test_outbound_window_lag.py::test_an_order_past_the_first_hundred_moves_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_each_later_page_goes_through_the_retry_ladder`
  - `tests/test_outbound_window_lag.py::test_every_judged_reading_records_its_readings_and_wait`
  - `tests/test_outbound_window_lag.py::test_the_unpaged_read_walks_past_a_capped_first_page_one_track_back`
  - `tests/test_outbound_window_lag.py::test_the_walk_ends_at_the_page_that_cannot_follow_the_last[a-short-later-page]`
  - `tests/test_outbound_window_lag.py::test_the_walk_stops_once_it_holds_the_declared_count`

Old text:

```
    tag = getattr(playlist, "_etag", None)
    for _ask
```

New text:

```
    tag = None
    for _ask
```

### `r1360.W13_declared_unread`

playlist_tracks_unpaged: the walk reads no declared count

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `W13_declared_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 828 against a baseline of 828
- Kills: 25 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_first_reading_whose_window_lags_is_read_again_before_any_move`
  - `tests/test_outbound_window_lag.py::test_a_long_playlist_nothing_changed_is_read_whole_and_written_once`
  - `tests/test_outbound_window_lag.py::test_a_removal_past_the_first_hundred_takes_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_once_is_read_again_and_lands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_window_lags_beside_a_first_page_refuses_after_the_bound`
  - `tests/test_outbound_window_lag.py::test_a_window_that_catches_up_beside_a_first_page_settles_as_done`
  - `tests/test_outbound_window_lag.py::test_a_window_that_lags_beside_a_first_page_is_not_read_back_between_moves`
  - `tests/test_outbound_window_lag.py::test_an_order_past_the_first_hundred_moves_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_each_later_page_goes_through_the_retry_ladder`
  - `tests/test_outbound_window_lag.py::test_every_judged_reading_records_its_readings_and_wait`
  - `tests/test_outbound_window_lag.py::test_the_unpaged_read_walks_past_a_capped_first_page_one_track_back`
  - `tests/test_outbound_window_lag.py::test_the_walk_ends_at_the_page_that_cannot_follow_the_last[a-page-carrying-another-version-tag]`
  - `tests/test_outbound_window_lag.py::test_the_walk_ends_at_the_page_that_cannot_follow_the_last[a-page-longer-than-the-first]`
  - `tests/test_outbound_window_lag.py::test_the_walk_ends_at_the_page_that_cannot_follow_the_last[a-page-not-starting-where-the-last-ended]`
  - `tests/test_outbound_window_lag.py::test_the_walk_ends_at_the_page_that_cannot_follow_the_last[a-short-later-page]`
  - ... and 10 more, see the JSON sidecar

Old text:

```
    declared = getattr(playlist, "num_tracks", None)
    if not _is_count
```

New text:

```
    declared = None
    if not _is_count
```

### `r1360.W14_cap_of_one_walked`

playlist_tracks_unpaged: a first page of one track is walked, which reads no new track a request

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `W14_cap_of_one_walked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 828 against a baseline of 828
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_cap_of_one_track_is_read_once_rather_than_walked_forever`

Old text:

```
or len(rows) >= declared or len(rows) < 2:
```

New text:

```
or len(rows) >= declared or len(rows) < 1:
```

### `r1360.W15_short_page_walked_past`

playlist_tracks_unpaged: a page shorter than the first does not end the walk

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `W15_short_page_walked_past`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 828 against a baseline of 828
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_the_walk_ends_at_the_page_that_cannot_follow_the_last[a-short-later-page]`

Old text:

```
        rows.extend(page[1:])
        if len(page) < step:
            break

```

New text:

```
        rows.extend(page[1:])

```

### `r1360.W1_no_walk`

playlist_tracks_unpaged: a first page short of the declared count is not walked past, as U226 left it

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `W1_no_walk`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 828 against a baseline of 828
- Kills: 25 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_first_reading_whose_window_lags_is_read_again_before_any_move`
  - `tests/test_outbound_window_lag.py::test_a_long_playlist_nothing_changed_is_read_whole_and_written_once`
  - `tests/test_outbound_window_lag.py::test_a_removal_past_the_first_hundred_takes_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_once_is_read_again_and_lands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_window_lags_beside_a_first_page_refuses_after_the_bound`
  - `tests/test_outbound_window_lag.py::test_a_window_that_catches_up_beside_a_first_page_settles_as_done`
  - `tests/test_outbound_window_lag.py::test_a_window_that_lags_beside_a_first_page_is_not_read_back_between_moves`
  - `tests/test_outbound_window_lag.py::test_an_order_past_the_first_hundred_moves_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_each_later_page_goes_through_the_retry_ladder`
  - `tests/test_outbound_window_lag.py::test_every_judged_reading_records_its_readings_and_wait`
  - `tests/test_outbound_window_lag.py::test_the_unpaged_read_walks_past_a_capped_first_page_one_track_back`
  - `tests/test_outbound_window_lag.py::test_the_walk_ends_at_the_page_that_cannot_follow_the_last[a-page-carrying-another-version-tag]`
  - `tests/test_outbound_window_lag.py::test_the_walk_ends_at_the_page_that_cannot_follow_the_last[a-page-longer-than-the-first]`
  - `tests/test_outbound_window_lag.py::test_the_walk_ends_at_the_page_that_cannot_follow_the_last[a-page-not-starting-where-the-last-ended]`
  - `tests/test_outbound_window_lag.py::test_the_walk_ends_at_the_page_that_cannot_follow_the_last[a-short-later-page]`
  - ... and 10 more, see the JSON sidecar

Old text:

```
    if not _is_count(declared) or len(rows) >= declared or len(rows) < 2:
        return rows
```

New text:

```
    if True:
        return rows
```

### `r1360.W2_walk_no_overlap`

playlist_tracks_unpaged: each later request starts where the last ended, not one track back

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `W2_walk_no_overlap`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 828 against a baseline of 828
- Kills: 19 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_first_reading_whose_window_lags_is_read_again_before_any_move`
  - `tests/test_outbound_window_lag.py::test_a_long_playlist_nothing_changed_is_read_whole_and_written_once`
  - `tests/test_outbound_window_lag.py::test_a_removal_past_the_first_hundred_takes_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_once_is_read_again_and_lands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_window_lags_beside_a_first_page_refuses_after_the_bound`
  - `tests/test_outbound_window_lag.py::test_a_window_that_catches_up_beside_a_first_page_settles_as_done`
  - `tests/test_outbound_window_lag.py::test_a_window_that_lags_beside_a_first_page_is_not_read_back_between_moves`
  - `tests/test_outbound_window_lag.py::test_an_order_past_the_first_hundred_moves_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_each_later_page_goes_through_the_retry_ladder`
  - `tests/test_outbound_window_lag.py::test_every_judged_reading_records_its_readings_and_wait`
  - `tests/test_outbound_window_lag.py::test_the_unpaged_read_walks_past_a_capped_first_page_one_track_back`
  - `tests/test_outbound_window_lag.py::test_the_walk_ends_at_the_page_that_cannot_follow_the_last[a-short-later-page]`
  - `tests/test_outbound_window_lag.py::test_the_walk_stops_once_it_holds_the_declared_count`
  - `tests/test_sync_pair_calls.py::test_a_300_track_order_with_adds_and_removals_stays_inside_its_forecast`
  - `tests/test_sync_pair_calls.py::test_an_existing_playlists_removals_and_additions_cost_what_is_expected[120-51-0]`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        offset = len(rows) - 1

```

New text:

```
        offset = len(rows)

```

### `r1360.W3_no_start_check`

playlist_tracks_unpaged: a page is taken without starting on the last track read

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `W3_no_start_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 828 against a baseline of 828
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_the_walk_ends_at_the_page_that_cannot_follow_the_last[a-page-not-starting-where-the-last-ended]`

Old text:

```
            or row_id(page[0]) != row_id(rows[-1])

```

New text:

```
(empty)
```

### `r1360.W4_no_tag_check`

playlist_tracks_unpaged: a page carrying another version tag is taken

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `W4_no_tag_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 828 against a baseline of 828
- Kills: 4 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_later_pages_lag_too_is_held_with_nothing_taken_off`
  - `tests/test_outbound_window_lag.py::test_an_order_whose_later_pages_lag_too_is_held_with_nothing_moved`
  - `tests/test_outbound_window_lag.py::test_every_judged_reading_records_its_readings_and_wait`
  - `tests/test_outbound_window_lag.py::test_the_walk_ends_at_the_page_that_cannot_follow_the_last[a-page-carrying-another-version-tag]`

Old text:

```
            or getattr(playlist, "_etag", None) != tag

```

New text:

```
(empty)
```

### `r1360.W5_no_length_check`

playlist_tracks_unpaged: a page longer than the first is taken

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `W5_no_length_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 828 against a baseline of 828
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_the_walk_ends_at_the_page_that_cannot_follow_the_last[a-page-longer-than-the-first]`

Old text:

```
            or len(page) > step

```

New text:

```
(empty)
```

### `r1360.W6_no_empty_check`

playlist_tracks_unpaged: an empty later page is not read as the end of the walk

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `W6_no_empty_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 828 against a baseline of 828
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_the_walk_ends_at_the_page_that_cannot_follow_the_last[an-empty-later-page]`

Old text:

```
            not page
            or len(page) > step
```

New text:

```
            len(page) > step
```

### `r1360.W7_full_page_ends`

playlist_tracks_unpaged: a full later page ends the walk as a short one does

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `W7_full_page_ends`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 828 against a baseline of 828
- Kills: 10 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_first_reading_whose_window_lags_is_read_again_before_any_move`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_window_lags_beside_a_first_page_refuses_after_the_bound`
  - `tests/test_outbound_window_lag.py::test_a_window_that_catches_up_beside_a_first_page_settles_as_done`
  - `tests/test_outbound_window_lag.py::test_a_window_that_lags_beside_a_first_page_is_not_read_back_between_moves`
  - `tests/test_outbound_window_lag.py::test_every_judged_reading_records_its_readings_and_wait`
  - `tests/test_outbound_window_lag.py::test_the_unpaged_read_walks_past_a_capped_first_page_one_track_back`
  - `tests/test_sync_pair_calls.py::test_a_300_track_order_with_adds_and_removals_stays_inside_its_forecast`
  - `tests/test_sync_pair_calls.py::test_an_existing_playlists_removals_and_additions_cost_what_is_expected[250-60-120]`
  - `tests/test_sync_pair_calls.py::test_an_unpaged_reads_requests_are_what_its_walk_asks[200-3]`
  - `tests/test_sync_pair_calls.py::test_an_unpaged_reads_requests_are_what_its_walk_asks[250-3]`

Old text:

```
        if len(page) < step:
            break
```

New text:

```
        if len(page) <= step:
            break
```

### `r1360.W8_overlap_kept`

playlist_tracks_unpaged: the overlapping track is read twice

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `W8_overlap_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 828 against a baseline of 828
- Kills: 25 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_the_settle_reading_waits_then_reads_once_and_names_a_lag`
  - `tests/test_outbound_remove_lag.py::test_a_pairs_removal_add_and_order_all_land_over_a_read_that_lags_each_write[count]`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[count]`
  - `tests/test_outbound_remove_lag.py::test_a_removal_whose_read_lags_one_write_is_taken_as_done[count]`
  - `tests/test_outbound_window_lag.py::test_a_first_reading_whose_window_lags_is_read_again_before_any_move`
  - `tests/test_outbound_window_lag.py::test_a_long_playlist_nothing_changed_is_read_whole_and_written_once`
  - `tests/test_outbound_window_lag.py::test_a_removal_past_the_first_hundred_takes_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_once_is_read_again_and_lands`
  - `tests/test_outbound_window_lag.py::test_a_window_short_of_the_declared_total_still_refuses_with_nothing_sent`
  - `tests/test_outbound_window_lag.py::test_a_window_that_catches_up_beside_a_first_page_settles_as_done`
  - `tests/test_outbound_window_lag.py::test_a_window_that_lags_beside_a_first_page_is_not_read_back_between_moves`
  - `tests/test_outbound_window_lag.py::test_an_order_past_the_first_hundred_moves_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_each_later_page_goes_through_the_retry_ladder`
  - `tests/test_outbound_window_lag.py::test_every_judged_reading_records_its_readings_and_wait`
  - `tests/test_outbound_window_lag.py::test_the_unpaged_read_walks_past_a_capped_first_page_one_track_back`
  - ... and 10 more, see the JSON sidecar

Old text:

```
        rows.extend(page[1:])
```

New text:

```
        rows.extend(page)
```

### `r261.L1_skip_record`

listing.artist_releases stops appending a skipped method to the caller's collector

- File: `src/cratekit/acquire/listing.py`
- Source: `r261.json`, row `L1_skip_record`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/modules/test_labels.py`
- Collected: 522 against a baseline of 522
- Kills: 4 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_skipped_release_listing_is_named_to_a_caller_that_asks`
  - `tests/test_label_tidal_catalogue.py::test_a_listing_a_roster_does_not_hold_is_skipped_and_recorded`
  - `tests/test_label_tidal_catalogue.py::test_a_plain_artist_object_missing_one_listing_is_recorded_by_the_source`
  - `tests/test_label_tidal_catalogue.py::test_a_roster_member_missing_one_listing_fails_the_sweep_and_names_it`

Old text:

```
                skipped.append(method)
```

New text:

```
                pass
```

### `r504-a.A5_listing_no_count`

The listing hands back no count at all

- File: `src/cratekit/acquire/listing.py`
- Source: `r504-a.json`, row `A5_listing_no_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_outbound_tidal_account.py`
- Collected: 620 against a baseline of 620
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_listing_short_of_the_declared_count_raises_the_shortfall_with_its_rows`
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`
  - `tests/test_label_tidal_catalogue.py::test_the_listing_hands_back_the_count_the_walk_ended_on`
  - `tests/test_label_tidal_catalogue.py::test_the_verb_boundary_keeps_the_rows_and_hands_back_the_shortfall`

Old text:

```
    return rows, total if isinstance(total, int) and total > 0 else None
```

New text:

```
    return rows, None
```

### `r504-a.A6_listing_unrecorded`

The listing walks on the unrecorded count, so the one it ended on is never kept

- File: `src/cratekit/acquire/listing.py`
- Source: `r504-a.json`, row `A6_listing_unrecorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_outbound_tidal_account.py`
- Collected: 620 against a baseline of 620
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_listing_short_of_the_declared_count_raises_the_shortfall_with_its_rows`
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`
  - `tests/test_label_tidal_catalogue.py::test_the_listing_hands_back_the_count_the_walk_ended_on`
  - `tests/test_label_tidal_catalogue.py::test_the_verb_boundary_keeps_the_rows_and_hands_back_the_shortfall`

Old text:

```
    rows = favorite_tracks(session, declared_total=declared, **kwargs)
```

New text:

```
    rows = favorite_tracks(session, declared_total=count, **kwargs)
```

### `r504-a.A7_listing_nonpositive`

The listing trusts a zero or sentinel count and hands it back as a count

- File: `src/cratekit/acquire/listing.py`
- Source: `r504-a.json`, row `A7_listing_nonpositive`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_outbound_tidal_account.py`
- Collected: 620 against a baseline of 620
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_count_the_provider_did_not_publish_leaves_nothing_to_compare[-1]`
  - `tests/test_label_tidal_catalogue.py::test_a_count_the_provider_did_not_publish_leaves_nothing_to_compare[0]`

Old text:

```
    return rows, total if isinstance(total, int) and total > 0 else None
```

New text:

```
    return rows, total if isinstance(total, int) else None
```

### `r888.H1_held_is_paged`

listing.artist_releases: a HeldReleases roster is treated as a provider artist, probed for paging methods it lacks, and read as empty

- File: `src/cratekit/acquire/listing.py`
- Source: `r888.json`, row `H1_held_is_paged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 578 against a baseline of 578
- Kills: 11 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_crawl_that_read_everything_still_succeeds`
  - `tests/test_label_tidal_catalogue.py::test_a_held_artist_rate_limited_during_discovery_is_not_recorded_as_unread`
  - `tests/test_label_tidal_catalogue.py::test_a_listing_a_roster_does_not_hold_is_skipped_and_recorded`
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_during_discovery_fails_the_sweep_and_names_the_artist`
  - `tests/test_label_tidal_catalogue.py::test_a_roster_larger_than_one_artists_budget_is_read_in_full_once_each`
  - `tests/test_label_tidal_catalogue.py::test_a_roster_member_missing_one_listing_fails_the_sweep_and_names_it`
  - `tests/test_label_tidal_catalogue.py::test_a_roster_release_credited_under_two_artists_is_returned_once`
  - `tests/test_label_tidal_catalogue.py::test_discovery_offers_the_credited_artist_and_never_the_compilation[compilation-not-offered]`
  - `tests/test_label_tidal_catalogue.py::test_discovery_offers_the_credited_artist_and_never_the_compilation[offers-the-credited-artist]`
  - `tests/test_label_tidal_catalogue.py::test_the_roster_crawls_the_label_page_and_every_seed_through_the_listing`
  - `tests/test_label_tidal_catalogue.py::test_the_roster_lists_once_when_it_is_built_and_the_crawl_reads_memory`

Old text:

```
    held = isinstance(artist, HeldReleases)
```

New text:

```
    held = False
```

### `r888.H2_held_not_deduplicated`

listing.artist_releases: a release a held roster lists under two artists is returned twice

- File: `src/cratekit/acquire/listing.py`
- Source: `r888.json`, row `H2_held_not_deduplicated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 578 against a baseline of 578
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_roster_release_credited_under_two_artists_is_returned_once`

Old text:

```
            if identity in seen:
```

New text:

```
            if identity in seen and not held:
```

### `r888.H3_unheld_listing_not_recorded`

listing.artist_releases: a listing a held roster does not hold reads as an empty listing and is not recorded as skipped

- File: `src/cratekit/acquire/listing.py`
- Source: `r888.json`, row `H3_unheld_listing_not_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 578 against a baseline of 578
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_listing_a_roster_does_not_hold_is_skipped_and_recorded`

Old text:

```
        listed = artist.held(method) if held else getattr(artist, method, None)
```

New text:

```
        listed = (artist.held(method) or []) if held else getattr(artist, method, None)
```

### `r888.H4_provider_budget_halved`

listing.PAGE_CAPS: a real provider artist's release walk gets a budget of 50 requests rather than 100

- File: `src/cratekit/acquire/listing.py`
- Source: `r888.json`, row `H4_provider_budget_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 578 against a baseline of 578
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_provider_listing_that_never_ends_still_spends_its_budget_and_blames_the_offset`

Old text:

```
    # A label roster held in memory spends none of it (R-888, ``HeldReleases``).
    "artist_releases": 100,
```

New text:

```
    # A label roster held in memory spends none of it (R-888, ``HeldReleases``).
    "artist_releases": 50,
```

### `r888.H5_abstract_held`

listing.HeldReleases: held is not abstract, so a subclass without it is built and fails mid crawl

- File: `src/cratekit/acquire/listing.py`
- Source: `r888.json`, row `H5_abstract_held`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 578 against a baseline of 578
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_held_object_that_forgets_its_lists_fails_when_built`

Old text:

```
    @abstractmethod
    def held(
```

New text:

```
    def held(
```

### `u226.M1_equal_not_agreed`

judge_window: two equal reads are not read as agreeing first

- File: `src/cratekit/acquire/listing.py`
- Source: `u226.json`, row `M1_equal_not_agreed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`
- Collected: 785 against a baseline of 785
- Kills: 78 (killed)
- Killed:
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[count]`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[tracks]`
  - `tests/test_outbound_remove_lag.py::test_a_wrong_track_behind_a_lagging_count_refuses_at_once`
  - `tests/test_outbound_window_lag.py::test_a_window_short_of_the_declared_total_still_refuses_with_nothing_sent`
  - `tests/test_outbound_window_lag.py::test_the_judge_reads_the_two_reads_against_the_declared_count[paged0-unpaged0-2-agrees]`
  - `tests/test_outbound_window_lag.py::test_the_judge_reads_the_two_reads_against_the_declared_count[paged1-unpaged1-3-agrees]`
  - `tests/test_prune.py::test_a_playlist_with_a_track_the_account_cannot_see_is_refused_with_nothing_sent`
  - `tests/test_prune.py::test_a_settled_track_the_listing_hides_is_not_recorded_as_off`
  - `tests/test_sync_pair.py::test_a_first_sync_with_a_side_skipped_records_no_snapshot_and_stays_first`
  - `tests/test_sync_pair.py::test_a_job_naming_no_playlist_is_named_by_its_account_playlist`
  - `tests/test_sync_pair.py::test_a_landed_track_is_found_in_the_inbox_playlist_landed_for_the_account`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[cache-off]`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[kept]`
  - `tests/test_sync_pair.py::test_a_pair_whose_playlist_is_gone_does_not_hold_every_other_pair`
  - `tests/test_sync_pair.py::test_a_plan_with_every_landing_record_readable_warns_nothing_of_them`
  - ... and 63 more, see the JSON sidecar

Old text:

```
    if unpaged == paged:
        return WINDOW_AGREES
```

New text:

```
    if False:
        return WINDOW_AGREES
```

### `u226.M4_prefix_as_subset`

judge_window: any unpaged read whose tracks the window holds agrees, wherever they stand

- File: `src/cratekit/acquire/listing.py`
- Source: `u226.json`, row `M4_prefix_as_subset`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`
- Collected: 785 against a baseline of 785
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_window_lag.py::test_a_named_pair_whose_window_lags_refuses_as_itself`
  - `tests/test_sync_pair_window_lag.py::test_a_window_that_lags_beside_a_partial_unpaged_read_holds_the_pair_and_says_why`
  - `tests/test_sync_pair_window_lag.py::test_a_window_that_starts_lagging_after_the_plan_stops_the_write_as_moved`

Old text:

```
paged[: len(unpaged)] == unpaged
```

New text:

```
set(unpaged) <= set(paged)
```

### `u65.B1_favourites_back_to_the_short_page`

R-383 reintroduced exactly: the favourites walk ends on a short page again

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `B1_favourites_back_to_the_short_page`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 199 against a baseline of 199
- Kills: 9 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_permanent_count_failure_still_surfaces_at_the_ceiling`
  - `tests/test_adapter_listing.py::test_a_whole_window_of_unservable_items_does_not_end_the_favourites_walk`
  - `tests/test_adapter_listing.py::test_each_wrapper_docstring_names_the_rule_its_table_declares`
  - `tests/test_adapter_listing.py::test_every_shape_declares_the_rule_its_provider_can_actually_support`
  - `tests/test_adapter_listing.py::test_the_declared_count_is_retried_on_the_same_ladder_every_page_is`
  - `tests/test_adapter_listing.py::test_the_favourites_listing_reads_the_whole_account_and_not_its_newest_fraction`
  - `tests/test_outbound_tidal_account.py::test_a_heart_already_held_makes_no_write_and_a_new_one_makes_exactly_one`
  - `tests/test_outbound_tidal_account.py::test_a_hearts_sweep_runs_to_done_and_the_ledger_records_every_heart`
  - `tests/test_outbound_tidal_account.py::test_has_heart_answers_a_whole_sweep_from_one_paged_read`

Old text:

```
    "favorite_tracks": StopRule.DECLARED_TOTAL,
```

New text:

```
    "favorite_tracks": StopRule.SHORT_PAGE,
```

### `u65.B3_playlist_tracks_back_to_the_short_page`

the placeholder acquire read ends on a short page, dropping the rest of a playlist

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `B3_playlist_tracks_back_to_the_short_page`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 199 against a baseline of 199
- Kills: 6 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_listing_with_no_declared_total_walks_to_an_empty_page`
  - `tests/test_adapter_listing.py::test_a_playlist_that_publishes_no_count_degrades_rather_than_refusing`
  - `tests/test_adapter_listing.py::test_a_playlist_whose_provider_omits_a_track_reads_to_the_end`
  - `tests/test_adapter_listing.py::test_each_wrapper_docstring_names_the_rule_its_table_declares`
  - `tests/test_adapter_listing.py::test_every_shape_declares_the_rule_its_provider_can_actually_support`
  - `tests/test_outbound_tidal_account.py::test_a_member_already_on_the_playlist_makes_no_write`

Old text:

```
    "playlist_tracks": StopRule.DECLARED_TOTAL,
```

New text:

```
    "playlist_tracks": StopRule.SHORT_PAGE,
```

### `u65.C4_the_short_page_rule_stops_every_walk`

the rule argument is dropped from the short page test, so every shape stops short

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `C4_the_short_page_rule_stops_every_walk`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 199 against a baseline of 199
- Kills: 13 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_listing_of_624_playlists_is_paced_in_seconds_not_minutes`
  - `tests/test_adapter_listing.py::test_a_listing_with_no_declared_total_walks_to_an_empty_page`
  - `tests/test_adapter_listing.py::test_a_playlist_that_publishes_no_count_degrades_rather_than_refusing`
  - `tests/test_adapter_listing.py::test_a_playlist_whose_provider_omits_a_track_reads_to_the_end`
  - `tests/test_adapter_listing.py::test_a_whole_window_of_unservable_items_does_not_end_the_favourites_walk`
  - `tests/test_adapter_listing.py::test_an_account_listing_of_owned_playlists_costs_its_pages_and_no_single_fetch`
  - `tests/test_adapter_listing.py::test_an_artist_release_listing_reads_to_the_end_across_both_methods`
  - `tests/test_adapter_listing.py::test_the_account_playlists_listing_reads_to_the_end_at_its_own_page_size`
  - `tests/test_adapter_listing.py::test_the_favourites_listing_reads_the_whole_account_and_not_its_newest_fraction`
  - `tests/test_outbound_tidal_account.py::test_a_heart_already_held_makes_no_write_and_a_new_one_makes_exactly_one`
  - `tests/test_outbound_tidal_account.py::test_a_hearts_sweep_runs_to_done_and_the_ledger_records_every_heart`
  - `tests/test_outbound_tidal_account.py::test_a_member_already_on_the_playlist_makes_no_write`
  - `tests/test_outbound_tidal_account.py::test_has_heart_answers_a_whole_sweep_from_one_paged_read`

Old text:

```
        if stop is StopRule.SHORT_PAGE and len(page) < page_size:
```

New text:

```
        if len(page) < page_size:
```

### `u65.C6_offset_advances_by_what_was_served`

the plausible wrong fix: advance by the page's length, not the window width, re-serving items

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `C6_offset_advances_by_what_was_served`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 199 against a baseline of 199
- Kills: 10 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_listing_with_no_declared_total_walks_to_an_empty_page`
  - `tests/test_adapter_listing.py::test_a_playlist_that_publishes_no_count_degrades_rather_than_refusing`
  - `tests/test_adapter_listing.py::test_a_playlist_whose_provider_omits_a_track_reads_to_the_end`
  - `tests/test_adapter_listing.py::test_a_whole_window_of_unservable_items_does_not_end_the_favourites_walk`
  - `tests/test_adapter_listing.py::test_the_account_playlists_listing_reads_to_the_end_at_its_own_page_size`
  - `tests/test_adapter_listing.py::test_the_favourites_listing_reads_the_whole_account_and_not_its_newest_fraction`
  - `tests/test_outbound_tidal_account.py::test_a_heart_already_held_makes_no_write_and_a_new_one_makes_exactly_one`
  - `tests/test_outbound_tidal_account.py::test_a_hearts_sweep_runs_to_done_and_the_ledger_records_every_heart`
  - `tests/test_outbound_tidal_account.py::test_a_member_already_on_the_playlist_makes_no_write`
  - `tests/test_outbound_tidal_account.py::test_has_heart_answers_a_whole_sweep_from_one_paged_read`

Old text:

```
        offset += page_size

        if total is not None:
```

New text:

```
        offset += len(page)

        if total is not None:
```

### `u70.E3_hearts_declared_total`

Existing: the favourites walk ends on a page shape instead of the declared count

- File: `src/cratekit/acquire/listing.py`
- Source: `u70.json`, row `E3_hearts_declared_total`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/test_adapter_listing.py`
- Collected: 260 against a baseline of 260
- Kills: 4 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_permanent_count_failure_still_surfaces_at_the_ceiling`
  - `tests/test_adapter_listing.py::test_a_whole_window_of_unservable_items_does_not_end_the_favourites_walk`
  - `tests/test_adapter_listing.py::test_the_declared_count_is_retried_on_the_same_ladder_every_page_is`
  - `tests/test_adapter_listing.py::test_the_favourites_listing_reads_the_whole_account_and_not_its_newest_fraction`

Old text:

```
    kwargs.setdefault("declared_total", _declared_count(favorites, "get_tracks_count"))
```

New text:

```
    kwargs.setdefault("declared_total", None)
```

### `r1705.M16_lookup_removed`

_resembling never reads the lookup, so a pair the discovery score misses (Prince, 4 U against For You) reads missing and downloads

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M16_lookup_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 38 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_a_slang_title_through_the_real_verb_is_asked_and_not_downloaded`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4 U-For You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4 U-For You-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4Ever-Forever-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4Ever-Forever-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-I Would Die 4 U-I Would Die For You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-I Would Die 4 U-I Would Die For You-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-Luv U 2-Love You Too-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-Luv U 2-Love You Too-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Monkey Safari-2 Nite-Tonight-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Monkey Safari-2 Nite-Tonight-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Prince-4 U-For You-slang-held]`
  - ... and 23 more, see the JSON sidecar

Old text:

```
        for recording in index.spelled_alike(wanted.recording)

```

New text:

```
        for recording in ()

```

### `r1705.M17_lookup_repeats_the_five`

the lookup's hits are not checked against the five scored recordings, so a recording both hold is offered twice

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M17_lookup_repeats_the_five`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 4 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`

Old text:

```
        if recording not in offered

```

New text:

```
(empty)
```

### `r1705.M18_lookup_skips_every_scored`

the lookup skips every recording discovery scored, round two's shape, so a lookup hit ranked sixth is cut by the cap, never offered and never counted withheld

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M18_lookup_skips_every_scored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 4 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`

Old text:

```
    offered = {held.recording for held in scored}

```

New text:

```
    offered = {held.recording for held in _approximate(wanted, index, limit=None)}

```

### `r1705.M19_lookup_after_the_scored`

the lookup's hits follow the scored five rather than leading, so the same title under the reading sits behind fuzzy hits and is truncated

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M19_lookup_after_the_scored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 6 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`

Old text:

```
    return tuple(looked_up + scored)

```

New text:

```
    return tuple(scored + looked_up)

```

### `r1705.M20_lookup_counts_in_the_five`

the lookup's hits are cut to the five with the scored ones, round one's shape, so a scored recording is pushed out with nothing withheld

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M20_lookup_counts_in_the_five`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 38 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_a_slang_title_through_the_real_verb_is_asked_and_not_downloaded`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4 U-For You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4 U-For You-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4Ever-Forever-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4Ever-Forever-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-I Would Die 4 U-I Would Die For You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-I Would Die 4 U-I Would Die For You-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-Luv U 2-Love You Too-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-Luv U 2-Love You Too-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Monkey Safari-2 Nite-Tonight-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Monkey Safari-2 Nite-Tonight-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Prince-4 U-For You-slang-held]`
  - ... and 23 more, see the JSON sidecar

Old text:

```
    return tuple(looked_up + scored)

```

New text:

```
    return tuple((looked_up + scored)[: len(scored)])

```

### `r1705.M5_spelled_test_removed`

_agree loses the spelled out equality, so a scored slang pair (Monkey Safari, Luv U against Love You) is dropped by the title test

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M5_spelled_test_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 5 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`
  - `tests/test_match_states.py::test_the_title_test_only_adds_agreement_and_only_for_a_spelled_out_equal_pair`

Old text:

```
        one.replace(" ", "") == other.replace(" ", "")
        or _spelled_out(one) == _spelled_out(other)

```

New text:

```
        one.replace(" ", "") == other.replace(" ", "")

```

### `r1705.M6_spelled_test_a_ratio`

_agree compares the spelled out forms by fuzz.ratio at the title floor rather than equality, so 2 against Tom (80) and N against Ant are offered

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M6_spelled_test_a_ratio`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 12 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[2-Tom]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[4-Fort]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[B-Bee]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Luv-Lover]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[N-Ant]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[U-Yo]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Traumer-Get Out-Agenou]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`
  - `tests/test_match_states.py::test_the_title_test_only_adds_agreement_and_only_for_a_spelled_out_equal_pair`
  - `tests/test_match_states.py::test_titles_split_differently_are_kept_by_equality_and_not_by_a_ratio`

Old text:

```
        or _spelled_out(one) == _spelled_out(other)

```

New text:

```
        or fuzz.ratio(_spelled_out(one), _spelled_out(other)) >= APPROXIMATE_TITLE_FLOOR

```

### `r1705.M7_spelled_replaces_written`

_agree reads only the spelled out form, dropping U286's equality as written, so U Turn against UTurn no longer agrees

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M7_spelled_replaces_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[DNA-D.N.A.]`
  - `tests/test_match_states.py::test_the_title_test_only_adds_agreement_and_only_for_a_spelled_out_equal_pair`

Old text:

```
        one.replace(" ", "") == other.replace(" ", "")
        or _spelled_out(one) == _spelled_out(other)

```

New text:

```
        _spelled_out(one) == _spelled_out(other)

```

### `r1705.S1_discovery_floor_raised`

SAMPLED existing guard: APPROXIMATE_FLOOR raised from 82 to 90, so fewer near hits are discovered

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `S1_discovery_floor_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 28 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_former_identifier_is_carried_only_with_one_fit_and_its_title`
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_one_letter_title_is_judged_by_the_same_rule`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Cos-Because]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[DNA-D.N.A.]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Every Day-Everyday]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Good Bye-Goodbye]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Hi Fi-HiFi]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Midnight Harbour Lights-Midnight Lights]`
  - `tests/test_match_states.py::test_a_row_settles_by_what_the_disk_holds[two-approximate-recordings-with-no-qualifier-stay-two-candidates]`
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Alex Kaminski-Mana-Nebula]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Hot Since 82-Wow-Wild]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Monkey Safari-Joy-Goodbye]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Paul Deep (AR)-Rea-Tique]`
  - ... and 13 more, see the JSON sidecar

Old text:

```
APPROXIMATE_FLOOR = 82

```

New text:

```
APPROXIMATE_FLOOR = 90

```

### `r1705.S2_unreadable_title_dropped`

SAMPLED existing guard: _title_resembles answers no for a title that folds to nothing, so a hit discovery found reads missing

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `S2_unreadable_title_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 15 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_former_identifier_is_carried_only_with_one_fit_and_its_title`
  - `tests/test_match_states.py::test_a_held_emoji_row_does_not_retire_another_emoji_rows_question`
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_is_offered_as_before[!!!-Sun]`
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_is_offered_as_before[Sun-!!!]`
  - `tests/test_match_states.py::test_a_yes_recorded_before_naming_no_option_still_applies`
  - `tests/test_match_states.py::test_an_answer_about_one_emoji_title_does_not_settle_another`
  - `tests/test_match_states.py::test_an_answer_recorded_before_is_not_carried_to_another_emoji_file`
  - `tests/test_match_states.py::test_an_answer_recorded_before_naming_an_emoji_file_still_applies`
  - `tests/test_match_states.py::test_an_emoji_candidate_offered_for_another_is_named_a_resemblance`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`
  - `tests/test_match_states.py::test_two_different_emoji_titles_by_one_artist_are_not_one_recording`
  - `tests/test_match_states.py::test_two_different_emoji_titles_through_the_real_verb_are_not_owned`
  - `tests/test_match_states.py::test_two_held_emoji_titles_are_offered_as_two_candidates`

Old text:

```
    if not asked or not found:
        return True

```

New text:

```
    if not asked or not found:
        return False

```

### `r1709.M14_isrc_settled_by_fold`

the ISRC branch settles a file under another emoji title by the fold

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M14_isrc_settled_by_fold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3858 against a baseline of 3858
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_isrc_on_a_file_under_another_emoji_title_is_asked_not_settled`
  - `tests/test_match_states.py::test_an_isrc_under_another_artist_and_another_emoji_title_is_asked`

Old text:

```
    settled = [held for held in carrying if same_title(held.title, wanted.title)]
    doubtful = [held for held in carrying if not same_title(held.title, wanted.title)]

```

New text:

```
    settled = [held for held in carrying if fold(held.title) == fold(wanted.title)]
    doubtful = [held for held in carrying if fold(held.title) != fold(wanted.title)]

```

### `r1709.M15_same_recording_title_guard`

_same_recording no longer reads the title, so an emoji candidate offered for another reads exact

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M15_same_recording_title_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3858 against a baseline of 3858
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_row_settles_by_what_the_disk_holds[an-approximate-hit-is-a-question-and-never-a-match]`
  - `tests/test_match_states.py::test_an_emoji_candidate_offered_for_another_is_named_a_resemblance`
  - `tests/test_match_states.py::test_an_isrc_hit_whose_title_disagrees_is_a_question_not_a_match`

Old text:

```
    if not same_title(held.title, wanted.title):
        return False
    if held.distinct
```

New text:

```
    if False:
        return False
    if held.recording
```

### `r1709.M16_candidates_grouped_by_token`

_candidates_for groups by the token, so two held emoji files are one candidate carrying both paths

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M16_candidates_grouped_by_token`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3858 against a baseline of 3858
- Kills: 5 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_former_identifier_is_carried_only_with_one_fit_and_its_title`
  - `tests/test_match_states.py::test_a_yes_recorded_before_naming_no_option_still_applies`
  - `tests/test_match_states.py::test_an_answer_recorded_before_is_not_carried_to_another_emoji_file`
  - `tests/test_match_states.py::test_an_answer_recorded_before_naming_an_emoji_file_still_applies`
  - `tests/test_match_states.py::test_two_held_emoji_titles_are_offered_as_two_candidates`

Old text:

```
        grouped.setdefault((held.distinct, held.version_key, held.key_key), []).append(held)

```

New text:

```
        grouped.setdefault((held.recording, held.version_key, held.key_key), []).append(held)

```

### `r1709.M18_match_id_token`

match_id hashes the token, so intake missing drops a second emoji row as a line listed twice

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M18_match_id_token`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3858 against a baseline of 3858
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_two_emoji_rows_are_each_searched_and_listed`
  - `tests/test_match_states.py::test_an_emoji_titles_identities_are_its_own`
  - `tests/test_match_states.py::test_two_emoji_rows_in_one_list_carry_two_match_identifiers`

Old text:

```
            f"mt_{_digest(self.wanted.distinct, self.wanted.version_key, self.wanted.key_key)}"

```

New text:

```
            f"mt_{_digest(self.wanted.recording, self.wanted.version_key, self.wanted.key_key)}"

```

### `r1709.M19_search_option_token`

the search acquisition option hashes the token

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M19_search_option_token`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3858 against a baseline of 3858
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_emoji_titles_identities_are_its_own`

Old text:

```
option_id=f"aq_{_digest(BY_SEARCH, wanted.distinct, wanted.version_key)}",
```

New text:

```
option_id=f"aq_{_digest(BY_SEARCH, wanted.recording, wanted.version_key)}",
```

### `r1709.M20_current_option_no_title`

current_option carries a former identifier without its title, so an answer about a fire emoji answers for a snow emoji held in its place

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M20_current_option_no_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3858 against a baseline of 3858
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_former_identifier_is_carried_only_with_one_fit_and_its_title`
  - `tests/test_match_states.py::test_an_answer_recorded_before_is_not_carried_to_another_emoji_file`

Old text:

```
        if _former_candidate_id(one) == option and same_title(one.title, title)

```

New text:

```
        if _former_candidate_id(one) == option

```

### `r1709.M21_current_option_never_carries`

current_option never carries, so every answer recorded before about an emoji file reads as a candidate gone

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M21_current_option_never_carries`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3858 against a baseline of 3858
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_former_identifier_is_carried_only_with_one_fit_and_its_title`
  - `tests/test_match_states.py::test_a_yes_recorded_before_naming_no_option_still_applies`
  - `tests/test_match_states.py::test_an_answer_recorded_before_naming_an_emoji_file_still_applies`

Old text:

```
    return carried[0].candidate_id if carried else option

```

New text:

```
    return option

```

### `r431-b.B4_the_engine_never_asks`

standing_tombstone asks under the companion kind for nothing, which is the defect the unit closes

- File: `src/cratekit/acquire/match.py`
- Source: `r431-b.json`, row `B4_the_engine_never_asks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1193 against a baseline of 1193
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_deleted_track_whose_row_kept_a_credit_is_suppressed_and_not_listed`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (Nightwave Remix) (feat. Mira)-]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (feat. Mira) (Nightwave Remix)-]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (feat. Mira)-Nightwave Remix]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path [ft. Mira] [Nightwave Remix]-]`
  - `tests/test_match_states.py::test_a_provider_row_crediting_somebody_else_is_not_withheld`
  - `tests/test_match_states.py::test_the_companion_reaches_exactly_what_ownership_reached`

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

### `r431-b.B5_the_engine_ignores_companions_false`

standing_tombstone asks for a companion even when the caller said not to

- File: `src/cratekit/acquire/match.py`
- Source: `r431-b.json`, row `B5_the_engine_ignores_companions_false`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1193 against a baseline of 1193
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_held_file_crediting_somebody_else_never_calls_the_companion_stale`

Old text:

```
    if not companions:
        return None
    for identity in wanted.uncredited_spellings:
```

New text:

```
    for identity in wanted.uncredited_spellings:
```

### `r667-b.B1_same_recording_no_isrc`

_same_recording: the ISRC clause removed, r667's G11 after its direct test

- File: `src/cratekit/acquire/match.py`
- Source: `r667-b.json`, row `B1_same_recording_no_isrc`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 705 against a baseline of 705
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_isrc_hit_asks_about_the_key_alone[artist_tag_credits_nobody]`

Old text:

```
    return fold(wanted.artist) in held.members or _carries(held, token)
```

New text:

```
    return fold(wanted.artist) in held.members
```

### `r667.E2_first_copy_only`

Existing: resolve_one reads the key off the first held copy only

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `E2_first_copy_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 705 against a baseline of 705
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_the_key_check_reads_every_held_copy_rather_than_whichever_sorted_first[sorts-first]`
  - `tests/test_match_states.py::test_the_relative_key_wins_the_reporting_when_both_disagreements_are_present`

Old text:

```
        disagreements = {key_disagreement(wanted.key, held.key) for held in exact}
```

New text:

```
        disagreements = {key_disagreement(wanted.key, exact[0].key)}
```

### `r667.F1_credited_reason_is_exact`

resolve_one: a credited list hit reports exact, so the report claims a token agreement that did not happen

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `F1_credited_reason_is_exact`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 705 against a baseline of 705
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_file_with_no_isrc_tag_is_owned_when_the_primary_artist_is_a_credited_member`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[credited-exact]`
  - `tests/test_match_states.py::test_the_credited_list_rule_tells_two_emoji_titles_apart`

Old text:

```
            else Why.CREDITED_EXACT
```

New text:

```
            else Why.EXACT
```

### `r667.F2_isrc_version_not_settled`

_candidates_for: an ISRC hit at another version spelling is a version question on the candidate beside a key question on the match

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `F2_isrc_version_not_settled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 705 against a baseline of 705
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_isrc_hit_asks_about_the_key_alone[another_version_spelling]`

Old text:

```
        elif version_key != wanted.version_key and not _carries(first, token):
```

New text:

```
        elif version_key != wanted.version_key:
```

### `r667.F3_doubtful_not_offered`

resolve_one: an ISRC hit whose title disagrees is not offered, so it falls through to missing or a scored hit

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `F3_doubtful_not_offered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 705 against a baseline of 705
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_isrc_hit_on_an_abbreviated_title_is_still_asked_about`
  - `tests/test_match_states.py::test_an_isrc_hit_whose_title_disagrees_is_a_question_not_a_match`
  - `tests/test_match_states.py::test_an_isrc_under_another_artist_and_another_emoji_title_is_asked`

Old text:

```
    if doubtful:
        # The ISRC agrees and the title does not, see above. Asked, not assumed.
```

New text:

```
    if False:
        # The ISRC agrees and the title does not, see above. Asked, not assumed.
```

### `r667.F4_text_copy_joins_isrc_paths`

resolve_one: a text matched copy at the wanted version joins an ISRC settled row's paths and key check

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `F4_text_copy_joins_isrc_paths`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 705 against a baseline of 705
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_isrc_settled_row_lists_the_files_carrying_the_isrc_and_no_other`

Old text:

```
    if settled:
        exact, agreed = settled, Why.ISRC_EXACT
```

New text:

```
    if settled:
        exact = settled + [held for held in owned if held.version_key == wanted.version_key and held.path not in {one.path for one in settled}]
        agreed = Why.ISRC_EXACT
```

### `r667.G12_same_recording_no_credit`

_same_recording: a credited hit at another version is title-approximate, not version-differs

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `G12_same_recording_no_credit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 705 against a baseline of 705
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
- Collected: 705 against a baseline of 705
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
  - `tests/test_match_states.py::test_an_isrc_hit_asks_about_the_key_alone[another_version_spelling]`
  - `tests/test_match_states.py::test_an_isrc_hit_asks_about_the_key_alone[artist_tag_credits_nobody]`
  - `tests/test_match_states.py::test_an_isrc_hit_on_an_abbreviated_title_is_still_asked_about`
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
- Collected: 705 against a baseline of 705
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_isrc_hit_asks_about_the_key_alone[another_version_spelling]`
  - `tests/test_match_states.py::test_an_isrc_hit_asks_about_the_key_alone[artist_tag_credits_nobody]`
  - `tests/test_match_states.py::test_an_isrc_hit_still_asks_about_the_key`

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
- Collected: 705 against a baseline of 705
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

### `u16-round-8-independent-composites.V24_approximate_limit_raised`

APPROXIMATE_LIMIT coefficient raised from 5 to 10; every test referencing it compares against match.APPROXIMATE_LIMIT itself, so the hunt predicts the value can drift green

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent-composites.json`, row `V24_approximate_limit_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 613 against a baseline of 613
- Kills: 10 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_at_most_the_declared_number_of_approximate_candidates_is_offered`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`
  - `tests/test_match_states.py::test_the_offer_limit_keeps_the_best_scoring_answers_and_says_what_it_kept_back`
  - `tests/test_match_states.py::test_the_scorer_is_capped_at_the_same_number_the_offer_is`
  - `tests/test_match_states.py::test_the_withheld_warning_survives_onto_the_run_that_actually_acquires`
  - `tests/test_match_states.py::test_unrelated_titles_scoring_higher_do_not_push_a_real_near_match_out`

Old text:

```
APPROXIMATE_LIMIT = 5

```

New text:

```
APPROXIMATE_LIMIT = 10

```

### `u16-round-8-independent.V11_candidate_order_sorted`

Candidate groups iterate sorted instead of insertion order, so the approximate offer truncates the best hit instead of the worst

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V11_candidate_order_sorted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 613 against a baseline of 613
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_the_offer_limit_keeps_the_best_scoring_answers_and_says_what_it_kept_back`

Old text:

```
    for recording, version_key, key in grouped:

```

New text:

```
    for recording, version_key, key in sorted(grouped):

```

### `u16-round-8-independent.V12_approximate_floor_halved`

APPROXIMATE_FLOOR coefficient halved from 82 to 41, admitting resemblances the unit exists to keep out of the offer

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V12_approximate_floor_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 613 against a baseline of 613
- Kills: 13 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_resemblance_below_the_floor_is_missing_rather_than_a_question`
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_a_spelled_number_is_not_read_as_a_numeral[Four Tune-Fortune]`
  - `tests/test_match_states.py::test_an_isrc_hit_on_an_abbreviated_title_is_still_asked_about`
  - `tests/test_match_states.py::test_an_unrelated_title_by_another_artist_is_still_not_offered`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[265-5]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[265-None]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[26500-5]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[26500-None]`
  - `tests/test_match_states.py::test_the_floor_is_pinned_from_both_sides_by_the_nearest_score_either_way`
  - `tests/test_match_states.py::test_the_lookup_is_what_reaches_a_pair_discovery_cannot_score`
  - `tests/test_match_states.py::test_the_lookup_reads_the_artist_as_it_folds_and_never_spelled_out`

Old text:

```
APPROXIMATE_FLOOR = 82

```

New text:

```
APPROXIMATE_FLOOR = 41

```

### `u16-round-8-independent.V13_withheld_not_reported`

The truncated approximate offer stops saying how many candidates were withheld, so a rejection rejects answers never shown

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V13_withheld_not_reported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 613 against a baseline of 613
- Kills: 4 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_the_offer_limit_keeps_the_best_scoring_answers_and_says_what_it_kept_back`
  - `tests/test_match_states.py::test_the_withheld_warning_survives_onto_the_run_that_actually_acquires`

Old text:

```
            withheld=max(len(offered) - APPROXIMATE_LIMIT, 0),

```

New text:

```
            withheld=0,

```

### `u16-round-8-independent.V18_rejection_skips_tombstones`

A rejection stops consulting the tombstones, so a rejected question hands acquisition a version standing under a tombstone (R36)

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V18_rejection_skips_tombstones`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 613 against a baseline of 613
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_rejecting_a_question_about_a_tombstoned_version_does_not_hand_it_to_acquisition`
  - `tests/test_match_states.py::test_rejecting_an_ambiguous_reading_can_skip_rather_than_acquire`

Old text:

```
        standing = standing_tombstone(
            found.wanted, suppresses=suppresses, suppression_id=suppression_id
        )

```

New text:

```
        standing = None

```

### `u16-round-8-independent.V19_unbound_yes_takes_todays_candidate`

An unspecific yes stops being bound to the candidate it was given about and accepts whatever the library holds today

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V19_unbound_yes_takes_todays_candidate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 613 against a baseline of 613
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_unspecific_yes_about_one_copy_does_not_settle_a_question_about_another[differs-then-relative]`
  - `tests/test_match_states.py::test_an_unspecific_yes_about_one_copy_does_not_settle_a_question_about_another[relative-then-differs]`

Old text:

```
            chosen = [c for c in found.candidates if c.candidate_id == about]

```

New text:

```
            chosen = list(found.candidates)

```

### `u16-round-8-independent.V1_key_check_first_copy_only`

Exact branch reads only the first held copy's key, so an unkeyed copy that sorts first answers the key question for a keyed one

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V1_key_check_first_copy_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 613 against a baseline of 613
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_the_key_check_reads_every_held_copy_rather_than_whichever_sorted_first[sorts-first]`
  - `tests/test_match_states.py::test_the_relative_key_wins_the_reporting_when_both_disagreements_are_present`

Old text:

```
        disagreements = {key_disagreement(wanted.key, held.key) for held in exact}

```

New text:

```
        disagreements = {key_disagreement(wanted.key, exact[0].key)}

```

### `u16-round-8-independent.V21_suppression_asked_one_spelling`

The tombstone store is asked under one spelling instead of every spelling a version could be recorded under, re-acquiring deletions recorded from another spelling

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V21_suppression_asked_one_spelling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 613 against a baseline of 613
- Kills: 9 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_listing_reaches_the_other_bracket_shape_of_its_own_version[round-listed]`
  - `tests/test_match_states.py::test_a_credited_listing_reaches_the_other_bracket_shape_of_its_own_version[square-listed]`
  - `tests/test_match_states.py::test_a_stale_tombstone_is_reported_under_every_spelling_the_match_consults`
  - `tests/test_match_states.py::test_a_tombstone_is_addressed_by_every_reading_except_the_undecidable_one[square]`
  - `tests/test_match_states.py::test_a_tombstone_under_a_spelling_the_composition_never_produces_is_found[sun path - nightwave remix]`
  - `tests/test_match_states.py::test_a_tombstone_under_a_spelling_the_composition_never_produces_is_found[sun path [nightwave remix]]`
  - `tests/test_match_states.py::test_the_two_spellings_of_no_qualifier_at_all_reach_each_other[Sun Path (Original Mix)-Sun Path [Original Version]]`
  - `tests/test_match_states.py::test_the_two_spellings_of_no_qualifier_at_all_reach_each_other[Sun Path (Original Mix)-Sun Path]`
  - `tests/test_match_states.py::test_the_two_spellings_of_no_qualifier_at_all_reach_each_other[Sun Path-Sun Path (Original Mix)]`

Old text:

```
    for identity in wanted.suppression_spellings:

```

New text:

```
    for identity in (wanted.identity,):

```

### `u16-round-8-independent.V3_version_differs_silently_joins`

A recording owned only at another version resolves MATCHED instead of needs review, the silent join R11 forbids

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V3_version_differs_silently_joins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 613 against a baseline of 613
- Kills: 41 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_hit_at_another_version_is_a_version_question_not_an_approximate_one`
  - `tests/test_match_states.py::test_a_group_that_only_begins_with_a_credits_letters_is_a_version[Feature Edit]`
  - `tests/test_match_states.py::test_a_group_that_only_begins_with_a_credits_letters_is_a_version[Featureless Dub]`
  - `tests/test_match_states.py::test_a_group_that_only_begins_with_a_credits_letters_is_a_version[Withdrawn Mix]`
  - `tests/test_match_states.py::test_a_group_that_only_begins_with_a_credits_letters_is_a_version[Within Mix]`
  - `tests/test_match_states.py::test_a_group_that_only_begins_with_a_credits_letters_is_a_version[Without You Remix]`
  - `tests/test_match_states.py::test_a_held_file_crediting_somebody_else_never_calls_the_companion_stale`
  - `tests/test_match_states.py::test_a_key_question_answered_elsewhere_does_not_settle_a_version_question`
  - `tests/test_match_states.py::test_a_library_file_whose_group_only_begins_with_a_credits_letters_is_that_version`
  - `tests/test_match_states.py::test_a_list_line_that_names_a_key_is_a_different_question_from_one_that_does_not`
  - `tests/test_match_states.py::test_a_persons_acceptance_being_applied_retires_nothing`
  - `tests/test_match_states.py::test_a_persons_answer_is_never_overwritten_by_a_later_resolution`
  - `tests/test_match_states.py::test_a_question_answered_from_one_source_is_never_asked_again_from_another`
  - `tests/test_match_states.py::test_a_rejected_question_makes_the_track_missing_rather_than_matched`
  - `tests/test_match_states.py::test_a_rejected_verdict_leaves_a_missing_row_that_says_what_to_go_and_get`
  - ... and 26 more, see the JSON sidecar

Old text:

```
            state=MatchState.NEEDS_REVIEW,
            why=Why.VERSION_DIFFERS,

```

New text:

```
            state=MatchState.MATCHED,
            why=Why.VERSION_DIFFERS,

```

### `u16-round-8-independent.V4_fuzzy_becomes_identity`

An approximate title hit resolves MATCHED, making a discovery heuristic an identity

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V4_fuzzy_becomes_identity`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 613 against a baseline of 613
- Kills: 98 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_file_whose_artist_and_title_are_the_rows_swapped_is_still_offered`
  - `tests/test_match_states.py::test_a_held_emoji_row_does_not_retire_another_emoji_rows_question`
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[DNA-D.N.A.]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Every Day-Everyday]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Good Bye-Goodbye]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Hi Fi-HiFi]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Joy-Jay]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Joy-Joys]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Lights Midnight-Midnight Lights]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Midnight Harbour Lights-Midnight Harbor Lights]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Midnight Harbour Lights-Midnight Harbour Light]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Midnight Harbour Lights-Midnight Harbour Lighte]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Midnight Harbour Lights-Midnight Lights]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[OK-O.K.]`
  - ... and 83 more, see the JSON sidecar

Old text:

```
            state=MatchState.NEEDS_REVIEW,
            why=Why.TITLE_APPROXIMATE,

```

New text:

```
            state=MatchState.MATCHED,
            why=Why.TITLE_APPROXIMATE,

```

### `u16-round-8-independent.V5_ambiguous_reading_promoted`

The other-reading question resolves MATCHED, reporting ownership of a record nobody checked

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V5_ambiguous_reading_promoted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 613 against a baseline of 613
- Kills: 28 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Acoustic]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Demo]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Dub]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Extended]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Instrumental]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Live]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Remix]`
  - `tests/test_match_states.py::test_a_tombstone_over_the_file_being_offered_as_the_answer_is_reported`
  - `tests/test_match_states.py::test_a_verdict_survives_the_rename_that_flips_the_reading`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[acapella]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[alternate]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[club]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[cut]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[flip]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[interlude]`
  - ... and 13 more, see the JSON sidecar

Old text:

```
            state=MatchState.NEEDS_REVIEW,
            why=Why.READING_AMBIGUOUS,

```

New text:

```
            state=MatchState.MATCHED,
            why=Why.READING_AMBIGUOUS,

```

### `u16-round-8-independent.V6_reading_question_never_asked`

The other-reading guard layer removed alone: the question is never asked and the row falls through to approximate or missing

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V6_reading_question_never_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 613 against a baseline of 613
- Kills: 28 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Acoustic]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Demo]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Dub]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Extended]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Instrumental]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Live]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Remix]`
  - `tests/test_match_states.py::test_a_tombstone_over_the_file_being_offered_as_the_answer_is_reported`
  - `tests/test_match_states.py::test_a_verdict_survives_the_rename_that_flips_the_reading`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[acapella]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[alternate]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[club]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[cut]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[flip]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[interlude]`
  - ... and 13 more, see the JSON sidecar

Old text:

```
    confirming = _other_reading_the_library_holds(wanted, index)

```

New text:

```
    confirming = None

```

### `u16-round-8-independent.V7_tombstoned_counted_missing`

Resolution never consults the tombstones, so a suppressed version reports MISSING with acquisition options and the deletion is undone (R36)

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V7_tombstoned_counted_missing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 613 against a baseline of 613
- Kills: 28 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (Nightwave Remix) (feat. Mira)-]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (feat. Mira) (Nightwave Remix)-]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (feat. Mira)-Nightwave Remix]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path [ft. Mira] [Nightwave Remix]-]`
  - `tests/test_match_states.py::test_a_credited_listing_reaches_the_other_bracket_shape_of_its_own_version[round-listed]`
  - `tests/test_match_states.py::test_a_credited_listing_reaches_the_other_bracket_shape_of_its_own_version[square-listed]`
  - `tests/test_match_states.py::test_a_deletion_of_the_plain_record_never_withholds_the_credited_one`
  - `tests/test_match_states.py::test_a_row_settles_by_what_the_disk_holds[a-tombstone-still-suppresses-when-the-library-can-say-nothing]`
  - `tests/test_match_states.py::test_a_suppressed_track_is_in_none_of_the_three_arrays`
  - `tests/test_match_states.py::test_a_suppressed_version_is_reported_as_a_warning_carrying_its_identifier`
  - `tests/test_match_states.py::test_a_tombstone_is_addressed_by_every_reading_except_the_undecidable_one[round]`
  - `tests/test_match_states.py::test_a_tombstone_is_addressed_by_every_reading_except_the_undecidable_one[square]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path (Extended) (Remastered)]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path (Nightwave Remix)]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path (Original Mix)]`
  - ... and 13 more, see the JSON sidecar

Old text:

```
    standing = standing_tombstone(
        wanted, suppresses=suppresses, suppression_id=suppression_id
    )

```

New text:

```
    standing = None

```

### `u16-round-8-independent.V8_missing_without_options`

A missing row carries no acquisition options, so the review queue item has nothing to offer (R12)

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V8_missing_without_options`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 613 against a baseline of 613
- Kills: 9 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_missing_track_carries_its_options_as_data_rather_than_as_a_question`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Alex Kaminski-Mana-Nebula]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Hot Since 82-Wow-Wild]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Monkey Safari-Joy-Goodbye]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Paul Deep (AR)-Rea-Tique]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Traumer-Get Out-Agenou]`
  - `tests/test_match_states.py::test_a_tombstone_is_addressed_by_every_reading_except_the_undecidable_one[ambiguous-dash]`
  - `tests/test_match_states.py::test_every_identifier_this_module_generates_is_the_declared_width`
  - `tests/test_match_states.py::test_the_dash_spelling_re_acquires_a_deleted_version_and_says_nothing_about_it`

Old text:

```
        acquisitions=acquisition_options(wanted),

```

New text:

```
        acquisitions=(),

```

### `u16-round-8-independent.V9_relative_key_by_letter`

Relative major or minor detected by matching letter instead of matching wheel number, so 8A vs 8B reads as outright disagreement and 8A vs 9A as relative

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V9_relative_key_by_letter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 613 against a baseline of 613
- Kills: 11 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_key_question_answered_elsewhere_does_not_settle_a_version_question`
  - `tests/test_match_states.py::test_a_row_settles_by_what_the_disk_holds[a-relative-key-disagreement-surfaces-rather-than-picking-one]`
  - `tests/test_match_states.py::test_a_version_answer_never_settles_a_key_question_about_the_same_line`
  - `tests/test_match_states.py::test_an_isrc_hit_asks_about_the_key_alone[another_version_spelling]`
  - `tests/test_match_states.py::test_an_isrc_hit_asks_about_the_key_alone[artist_tag_credits_nobody]`
  - `tests/test_match_states.py::test_an_isrc_hit_still_asks_about_the_key`
  - `tests/test_match_states.py::test_an_unspecific_yes_about_one_copy_does_not_settle_a_question_about_another[differs-then-relative]`
  - `tests/test_match_states.py::test_an_unspecific_yes_about_one_copy_does_not_settle_a_question_about_another[relative-then-differs]`
  - `tests/test_match_states.py::test_one_answered_key_question_never_settles_another_one`
  - `tests/test_match_states.py::test_the_key_check_reads_every_held_copy_rather_than_whichever_sorted_first[sorts-first]`
  - `tests/test_match_states.py::test_the_key_check_reads_every_held_copy_rather_than_whichever_sorted_first[sorts-last]`

Old text:

```
    return Why.KEY_RELATIVE if left[0] == right[0] else Why.KEY_DIFFERS

```

New text:

```
    return Why.KEY_RELATIVE if left[1] == right[1] else Why.KEY_DIFFERS

```

### `u265.M10_empty_index_scored`

_approximate: drop the early return on an empty index (an existing guard, sampled), so an empty library sorts the wanted token and asks the scorer

- File: `src/cratekit/acquire/match.py`
- Source: `u265.json`, row `M10_empty_index_scored`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`
- Collected: 2712 against a baseline of 2712
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_each_name_is_sorted_once_for_the_index_and_each_row_once_a_call`

Old text:

```
    if not index.by_recording:
        return ()
    from rapidfuzz import fuzz, process

    recordings, sorted_choices
```

New text:

```
    from rapidfuzz import fuzz, process

    recordings, sorted_choices
```

### `u265.M4_query_not_sorted`

_approximate: score the wanted token unsorted against the sorted library names

- File: `src/cratekit/acquire/match.py`
- Source: `u265.json`, row `M4_query_not_sorted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`
- Collected: 2712 against a baseline of 2712
- Kills: 42 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_rewritten_between_two_jobs_is_read_again_and_the_second_job_matches_its_new_tags`
  - `tests/test_match_states.py::test_a_file_whose_artist_and_title_are_the_rows_swapped_is_still_offered`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[2-Tom]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[4-Fort]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[B-Bee]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Cos-Because]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Luv-Lover]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[N-Ant]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[U-Yo]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Wot-What]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Midnight Harbour Lights-Midnight Harbor Lights]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Midnight Harbour Lights-Midnight Harbour Light]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Midnight Harbour Lights-Midnight Harbour Lighte]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Midnight Harbour Lights-Midnight Lights]`
  - ... and 27 more, see the JSON sidecar

Old text:

```
        _sorted_words(wanted.recording),
        sorted_choices,
```

New text:

```
        wanted.recording,
        sorted_choices,
```

### `u265.M5_hit_named_by_its_sorted_form`

_approximate: look a hit up by its sorted string rather than its position, so any recording whose words were not already in order loses its files

- File: `src/cratekit/acquire/match.py`
- Source: `u265.json`, row `M5_hit_named_by_its_sorted_form`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`
- Collected: 2712 against a baseline of 2712
- Kills: 61 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_rewritten_between_two_jobs_is_read_again_and_the_second_job_matches_its_new_tags`
  - `tests/test_match_states.py::test_a_file_whose_artist_and_title_are_the_rows_swapped_is_still_offered`
  - `tests/test_match_states.py::test_a_former_identifier_is_carried_only_with_one_fit_and_its_title`
  - `tests/test_match_states.py::test_a_held_emoji_row_does_not_retire_another_emoji_rows_question`
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[2-Tom]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[4-Fort]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[B-Bee]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Cos-Because]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Luv-Lover]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[N-Ant]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[U-Yo]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Wot-What]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[DNA-D.N.A.]`
  - ... and 46 more, see the JSON sidecar

Old text:

```
        held for _sorted, _score, position in found for held in index.versions(recordings[position])
```

New text:

```
        held for _sorted, _score, position in found for held in index.versions(_sorted)
```

### `u265.M8_other_scorer`

_approximate: score the sorted forms with WRatio instead of ratio, so scores and the floor's cut move

- File: `src/cratekit/acquire/match.py`
- Source: `u265.json`, row `M8_other_scorer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`
- Collected: 2712 against a baseline of 2712
- Kills: 25 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_favorites_lists_the_hearts_resolves_each_and_rereads_the_reasons_on_every_resume`
  - `tests/intake/test_workers.py::test_queueing_and_resolving_favorites_name_the_job_each_count_its_reasons_and_the_next_command`
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
  - `tests/test_match_states.py::test_a_resemblance_below_the_floor_is_missing_rather_than_a_question`
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_a_spelled_number_is_not_read_as_a_numeral[Four Tune-Fortune]`
  - ... and 10 more, see the JSON sidecar

Old text:

```
        scorer=fuzz.ratio,
```

New text:

```
        scorer=fuzz.WRatio,
```

### `u286.M10_swap_either_half`

the swap allowance takes either crossed half rather than both, so an unrelated title by an artist sharing one word is offered

- File: `src/cratekit/acquire/match.py`
- Source: `u286.json`, row `M10_swap_either_half`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 4 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_swap_is_offered_only_when_both_halves_cross`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`

Old text:

```
    return _agree(asked, fold(held.artist)) and _agree(fold(wanted.artist), found)

```

New text:

```
    return _agree(asked, fold(held.artist)) or _agree(fold(wanted.artist), found)

```

### `u286.M11_swap_removed`

the swap allowance removed, so a listing pasted title first reads missing and downloads the record the library holds

- File: `src/cratekit/acquire/match.py`
- Source: `u286.json`, row `M11_swap_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 8 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_file_whose_artist_and_title_are_the_rows_swapped_is_still_offered`
  - `tests/test_match_states.py::test_a_swapped_listing_split_differently_is_still_offered[Aurora Bloom - Every Day-Everyday - Aurora Bloom]`
  - `tests/test_match_states.py::test_a_swapped_listing_split_differently_is_still_offered[Aurora Bloom - Goodbye-Good Bye - Aurora Bloom]`
  - `tests/test_match_states.py::test_a_swapped_listing_split_differently_is_still_offered[Aurora Bloom - OK-O.K. - Aurora Bloom]`
  - `tests/test_match_states.py::test_a_swapped_listing_split_differently_is_still_offered[M.I.A. - Paper Planes-Paper Planes - MIA]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`

Old text:

```
    return _agree(asked, fold(held.artist)) and _agree(fold(wanted.artist), found)

```

New text:

```
    return False

```

### `u286.M12_swap_second_half_artist`

the swap's second half compares artist with artist, which the shared artist always passes, so one crossed half is enough

- File: `src/cratekit/acquire/match.py`
- Source: `u286.json`, row `M12_swap_second_half_artist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 8 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_file_whose_artist_and_title_are_the_rows_swapped_is_still_offered`
  - `tests/test_match_states.py::test_a_swapped_listing_split_differently_is_still_offered[Aurora Bloom - Every Day-Everyday - Aurora Bloom]`
  - `tests/test_match_states.py::test_a_swapped_listing_split_differently_is_still_offered[Aurora Bloom - Goodbye-Good Bye - Aurora Bloom]`
  - `tests/test_match_states.py::test_a_swapped_listing_split_differently_is_still_offered[Aurora Bloom - OK-O.K. - Aurora Bloom]`
  - `tests/test_match_states.py::test_a_swapped_listing_split_differently_is_still_offered[M.I.A. - Paper Planes-Paper Planes - MIA]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`

Old text:

```
    return _agree(asked, fold(held.artist)) and _agree(fold(wanted.artist), found)

```

New text:

```
    return _agree(asked, fold(held.artist)) and _agree(fold(wanted.artist), fold(held.artist))

```

### `u286.M13_filter_removed`

_resembling keeps every recording discovery finds, the base's behaviour, so Joy is offered Goodbye again

- File: `src/cratekit/acquire/match.py`
- Source: `u286.json`, row `M13_filter_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 20 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_one_letter_title_is_judged_by_the_same_rule`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[2-Tom]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[4-Fort]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[B-Bee]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Cos-Because]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Luv-Lover]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[N-Ant]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[U-Yo]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Wot-What]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Alex Kaminski-Mana-Nebula]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Hot Since 82-Wow-Wild]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Monkey Safari-Joy-Goodbye]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Paul Deep (AR)-Rea-Tique]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Traumer-Get Out-Agenou]`
  - `tests/test_match_states.py::test_joy_against_goodbye_is_downloaded_through_the_real_verb`
  - ... and 5 more, see the JSON sidecar

Old text:

```
        if not _title_resembles(wanted, held[0]):
            continue

```

New text:

```
        if False:
            continue

```

### `u286.M14_filter_after_cap`

_resembling asks discovery for the best five only and filters those, so unrelated titles outscoring a real near match push it out and the row downloads

- File: `src/cratekit/acquire/match.py`
- Source: `u286.json`, row `M14_filter_after_cap`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 4 (killed)
- Killed:
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`
  - `tests/test_match_states.py::test_unrelated_titles_scoring_higher_do_not_push_a_real_near_match_out`

Old text:

```
        _approximate(wanted, index, limit=None), key=attrgetter("recording")

```

New text:

```
        _approximate(wanted, index, limit=APPROXIMATE_LIMIT), key=attrgetter("recording")

```

### `u286.M15_cap_removed`

_resembling keeps every recording that passes, so more than five reach the candidate builder and the withheld count reports recordings the cap should not have built

- File: `src/cratekit/acquire/match.py`
- Source: `u286.json`, row `M15_cap_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 6 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`
  - `tests/test_match_states.py::test_the_scorer_is_capped_at_the_same_number_the_offer_is`

Old text:

```
        if recordings == APPROXIMATE_LIMIT:
            break

```

New text:

```
        if False:
            break

```

### `u286.M16_cap_off_by_one`

_resembling keeps six recordings rather than five

- File: `src/cratekit/acquire/match.py`
- Source: `u286.json`, row `M16_cap_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 6 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`
  - `tests/test_match_states.py::test_the_scorer_is_capped_at_the_same_number_the_offer_is`

Old text:

```
        if recordings == APPROXIMATE_LIMIT:

```

New text:

```
        if recordings == APPROXIMATE_LIMIT + 1:

```

### `u286.M17_cap_counts_files`

_resembling counts files rather than recordings toward the cap, so a recording held as several versions takes several places

- File: `src/cratekit/acquire/match.py`
- Source: `u286.json`, row `M17_cap_counts_files`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`

Old text:

```
        recordings += 1

```

New text:

```
        recordings += len(held)

```

### `u286.M18_resolver_back_to_base`

resolve_one calls the shipped discovery at the offer limit, the base, so the whole title test is bypassed

- File: `src/cratekit/acquire/match.py`
- Source: `u286.json`, row `M18_resolver_back_to_base`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 51 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_one_letter_title_is_judged_by_the_same_rule`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[2-Tom]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[4-Fort]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[B-Bee]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Cos-Because]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Luv-Lover]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[N-Ant]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[U-Yo]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Wot-What]`
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Alex Kaminski-Mana-Nebula]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Hot Since 82-Wow-Wild]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Monkey Safari-Joy-Goodbye]`
  - ... and 36 more, see the JSON sidecar

Old text:

```
    near = _resembling(wanted, index)

```

New text:

```
    near = _approximate(wanted, index, limit=APPROXIMATE_LIMIT)

```

### `u286.M19_limit_ignored`

_approximate ignores its limit and always caps at five, so the resolver's ask for every hit is cut before the title test

- File: `src/cratekit/acquire/match.py`
- Source: `u286.json`, row `M19_limit_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 9 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[265-None]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[2650-None]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[26500-None]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`
  - `tests/test_match_states.py::test_unrelated_titles_scoring_higher_do_not_push_a_real_near_match_out`

Old text:

```
        score_cutoff=APPROXIMATE_FLOOR,
        limit=limit,

```

New text:

```
        score_cutoff=APPROXIMATE_FLOOR,
        limit=APPROXIMATE_LIMIT,

```

### `u286.M1_title_floor_up_one`

APPROXIMATE_TITLE_FLOOR raised from 66 to 67, so one letter changed in a three letter title (Joy against Jay) reads missing and downloads

- File: `src/cratekit/acquire/match.py`
- Source: `u286.json`, row `M1_title_floor_up_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Joy-Jay]`
  - `tests/test_match_states.py::test_the_title_floor_is_pinned_from_both_sides_by_the_nearest_score_either_way`
  - `tests/test_match_states.py::test_titles_split_differently_are_kept_by_equality_and_not_by_a_ratio`

Old text:

```
APPROXIMATE_TITLE_FLOOR = 66

```

New text:

```
APPROXIMATE_TITLE_FLOOR = 67

```

### `u286.M2_title_floor_down_one`

APPROXIMATE_TITLE_FLOOR lowered from 66 to 65, so the nearest pair under it (Burning Sunlight against Morning Starlight Rising, 65.0) is offered

- File: `src/cratekit/acquire/match.py`
- Source: `u286.json`, row `M2_title_floor_down_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_the_title_floor_is_pinned_from_both_sides_by_the_nearest_score_either_way`

Old text:

```
APPROXIMATE_TITLE_FLOOR = 66

```

New text:

```
APPROXIMATE_TITLE_FLOOR = 65

```

### `u286.M3_title_floor_to_sixty`

APPROXIMATE_TITLE_FLOOR lowered to 60, so the card's Traumer pair, Get Out against Agenou at 61.5, is offered again

- File: `src/cratekit/acquire/match.py`
- Source: `u286.json`, row `M3_title_floor_to_sixty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Traumer-Get Out-Agenou]`
  - `tests/test_match_states.py::test_the_title_floor_is_pinned_from_both_sides_by_the_nearest_score_either_way`
  - `tests/test_match_states.py::test_titles_split_differently_are_kept_by_equality_and_not_by_a_ratio`

Old text:

```
APPROXIMATE_TITLE_FLOOR = 66

```

New text:

```
APPROXIMATE_TITLE_FLOOR = 60

```

### `u286.M4_plain_ratio`

_agree scores fuzz.ratio rather than token_set_ratio, so a dropped or reordered word scores on its letters and can read missing

- File: `src/cratekit/acquire/match.py`
- Source: `u286.json`, row `M4_plain_ratio`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 6 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Lights Midnight-Midnight Lights]`
  - `tests/test_match_states.py::test_the_floor_is_pinned_from_both_sides_by_the_nearest_score_either_way`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`
  - `tests/test_match_states.py::test_the_title_test_only_adds_agreement_and_only_for_a_spelled_out_equal_pair`

Old text:

```
    return fuzz.token_set_ratio(one, other) >= APPROXIMATE_TITLE_FLOOR

```

New text:

```
    return fuzz.ratio(one, other) >= APPROXIMATE_TITLE_FLOOR

```

### `u286.M6_unreadable_title_not_asked`

_title_resembles no longer asks whether a title folds to nothing, so the empty title is scored and agrees with nothing

- File: `src/cratekit/acquire/match.py`
- Source: `u286.json`, row `M6_unreadable_title_not_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 15 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_former_identifier_is_carried_only_with_one_fit_and_its_title`
  - `tests/test_match_states.py::test_a_held_emoji_row_does_not_retire_another_emoji_rows_question`
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_is_offered_as_before[!!!-Sun]`
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_is_offered_as_before[Sun-!!!]`
  - `tests/test_match_states.py::test_a_yes_recorded_before_naming_no_option_still_applies`
  - `tests/test_match_states.py::test_an_answer_about_one_emoji_title_does_not_settle_another`
  - `tests/test_match_states.py::test_an_answer_recorded_before_is_not_carried_to_another_emoji_file`
  - `tests/test_match_states.py::test_an_answer_recorded_before_naming_an_emoji_file_still_applies`
  - `tests/test_match_states.py::test_an_emoji_candidate_offered_for_another_is_named_a_resemblance`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`
  - `tests/test_match_states.py::test_two_different_emoji_titles_by_one_artist_are_not_one_recording`
  - `tests/test_match_states.py::test_two_different_emoji_titles_through_the_real_verb_are_not_owned`
  - `tests/test_match_states.py::test_two_held_emoji_titles_are_offered_as_two_candidates`

Old text:

```
    if not asked or not found:
        return True

```

New text:

```
    if False:
        return True

```

### `u286.S1_discovery_floor_up_one`

sampled existing guard: APPROXIMATE_FLOOR raised from 82 to 83

- File: `src/cratekit/acquire/match.py`
- Source: `u286.json`, row `S1_discovery_floor_up_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 10 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_former_identifier_is_carried_only_with_one_fit_and_its_title`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Good Bye-Goodbye]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Paul Deep (AR)-Rea-Tique]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Traumer-Get Out-Agenou]`
  - `tests/test_match_states.py::test_a_swapped_listing_split_differently_is_still_offered[Aurora Bloom - Goodbye-Good Bye - Aurora Bloom]`
  - `tests/test_match_states.py::test_a_swapped_listing_split_differently_is_still_offered[M.I.A. - Paper Planes-Paper Planes - MIA]`
  - `tests/test_match_states.py::test_a_yes_recorded_before_naming_no_option_still_applies`
  - `tests/test_match_states.py::test_an_answer_recorded_before_is_not_carried_to_another_emoji_file`
  - `tests/test_match_states.py::test_an_answer_recorded_before_naming_an_emoji_file_still_applies`
  - `tests/test_match_states.py::test_the_floor_is_pinned_from_both_sides_by_the_nearest_score_either_way`

Old text:

```
APPROXIMATE_FLOOR = 82

```

New text:

```
APPROXIMATE_FLOOR = 83

```

### `u286.S2_offer_not_truncated`

sampled existing guard: the approximate offer is not truncated to the limit

- File: `src/cratekit/acquire/match.py`
- Source: `u286.json`, row `S2_offer_not_truncated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 4 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_at_most_the_declared_number_of_approximate_candidates_is_offered`
  - `tests/test_match_states.py::test_the_offer_limit_keeps_the_best_scoring_answers_and_says_what_it_kept_back`

Old text:

```
            candidates=offered[:APPROXIMATE_LIMIT],

```

New text:

```
            candidates=offered,

```

### `u305.M4_index_library_not_reexported`

match: stop re-exporting index_library, so every caller of match.index_library and the intake suite's patch of it lose their target

- File: `src/cratekit/acquire/match.py`
- Source: `u305.json`, row `M4_index_library_not_reexported`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_library_reads_remembered.py`, `tests/intake/test_workers.py`
- Collected: 709 against a baseline of 709
- Kills: 301 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_failure_mid_set_fails_that_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/intake/test_workers.py::test_a_hearts_job_freezes_when_each_heart_was_made_and_a_playlist_job_does_not`
  - `tests/intake/test_workers.py::test_a_playlist_job_runs_pending_to_done_through_the_resume_path`
  - `tests/intake/test_workers.py::test_a_resolution_with_nothing_missing_names_no_next_command`
  - `tests/intake/test_workers.py::test_a_second_identify_over_the_same_recording_makes_zero_transport_calls`
  - `tests/intake/test_workers.py::test_a_set_identified_over_incomplete_coverage_queues_with_a_warning_and_freezes_the_gap`
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`
  - `tests/intake/test_workers.py::test_a_tracklist_that_cannot_be_written_refuses_and_says_the_answers_were_kept`
  - `tests/intake/test_workers.py::test_an_intake_job_that_owns_a_row_by_isrc_retires_the_question_an_earlier_job_asked`
  - `tests/intake/test_workers.py::test_an_offered_track_is_a_review_item_asked_once_however_often_it_is_redone`
  - `tests/intake/test_workers.py::test_answers_that_could_not_be_kept_are_said_on_both_verbs`
  - `tests/intake/test_workers.py::test_favorites_lists_the_hearts_resolves_each_and_rereads_the_reasons_on_every_resume`
  - `tests/intake/test_workers.py::test_identify_and_a_set_job_report_owned_offered_and_missing`
  - `tests/intake/test_workers.py::test_identify_reports_the_coverage_rule_and_a_gap_is_paid_for_again_and_nothing_else_is`
  - `tests/intake/test_workers.py::test_identify_then_set_pays_for_recognition_once_and_the_job_says_it_cost_nothing`
  - ... and 286 more, see the JSON sidecar

Old text:

```
    index_library,

```

New text:

```
(empty)
```

### `u305.M5_wanted_not_reexported`

match: stop re-exporting Wanted, so the readers and every package building one through match lose it

- File: `src/cratekit/acquire/match.py`
- Source: `u305.json`, row `M5_wanted_not_reexported`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_listdoc.py`, `tests/test_isrc_screen.py`
- Collected: 674 against a baseline of 706
- Kills: 674 (collect-error)
- Note: collection changed: 674 collected against a baseline of 706. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_listdoc.py::test_a_declared_version_beside_an_embedded_one_round_trips_whole[Sun Path (Extended)]`
  - `tests/test_listdoc.py::test_a_declared_version_beside_an_embedded_one_round_trips_whole[Sun Path (feat. Mira) (Extended)]`
  - `tests/test_listdoc.py::test_a_duplicate_id_is_written_once_and_the_first_occurrence_wins`
  - `tests/test_listdoc.py::test_a_frozen_mapping_carries_no_version_so_none_is_written`
  - `tests/test_listdoc.py::test_a_hand_built_track_with_no_spelling_writes_its_title_and_version`
  - `tests/test_listdoc.py::test_a_listed_id_with_no_provenance_refuses_and_writes_nothing`
  - `tests/test_listdoc.py::test_a_manifest_row_reads_as_the_wanted_track_its_list_row_reads_as`
  - `tests/test_listdoc.py::test_a_manifest_that_is_not_there_is_refused_by_name`
  - `tests/test_listdoc.py::test_a_manifest_this_build_did_not_write_is_refused_whole[[]-not a manifest]`
  - `tests/test_listdoc.py::test_a_manifest_this_build_did_not_write_is_refused_whole[\xff\xfe-not JSON]`
  - `tests/test_listdoc.py::test_a_manifest_this_build_did_not_write_is_refused_whole[{"list": 1, "origin": "tidal", "tracks": []}-not a manifest]`
  - `tests/test_listdoc.py::test_a_manifest_this_build_did_not_write_is_refused_whole[{"manifest": 1, "rows": []}-no rows object]`
  - `tests/test_listdoc.py::test_a_manifest_this_build_did_not_write_is_refused_whole[{"manifest": 1, "rows": {"1": []}}-not an object]`
  - `tests/test_listdoc.py::test_a_manifest_this_build_did_not_write_is_refused_whole[{"manifest": 1, "rows": {"1": {"source": " "}}}-names no source]`
  - `tests/test_listdoc.py::test_a_manifest_this_build_did_not_write_is_refused_whole[{"manifest": 1, "rows": {"1": {"source": "label", "label_name": 7}}}-label_name]`
  - ... and 659 more, see the JSON sidecar
- Collection errors: `tests/test_isrc_screen.py`

Old text:

```
    Wanted,

```

New text:

```
(empty)
```

### `r1709.M22_adjudicate_not_carried`

adjudicate passes the stored option unchanged, so an answer recorded before about an emoji file reads as a candidate gone

- File: `src/cratekit/acquire/match_cli.py`
- Source: `r1709.json`, row `M22_adjudicate_not_carried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3858 against a baseline of 3858
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_answer_recorded_before_naming_an_emoji_file_still_applies`

Old text:

```
                    else match.current_option(found, held.option, titles.get(held.option))

```

New text:

```
                    else held.option

```

### `r1709.M2_adjudicate_offered_not_carried`

adjudicate binds an unspecific yes to the stored option unchanged, so a yes recorded before about an emoji file reads as a candidate gone

- File: `src/cratekit/acquire/match_cli.py`
- Source: `r1709.json`, row `M2_adjudicate_offered_not_carried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3858 against a baseline of 3858
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_yes_recorded_before_naming_no_option_still_applies`

Old text:

```
                    match.current_option(found, one.option_id, titles.get(one.option_id))

```

New text:

```
                    one.option_id

```

### `r431-b.B6_the_verb_calls_a_companion_stale`

The verb's report over a matched row asks for companions, so a held file crediting somebody else calls one stale

- File: `src/cratekit/acquire/match_cli.py`
- Source: `r431-b.json`, row `B6_the_verb_calls_a_companion_stale`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_label_approved.py`, `tests/test_label_workers.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 928 against a baseline of 928
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_held_file_crediting_somebody_else_never_calls_the_companion_stale`

Old text:

```
                companions=not held,
```

New text:

```
                companions=True,
```

### `r679-b.B1_no_retirement`

adjudicate: never retire, so an owned row leaves its question open

- File: `src/cratekit/acquire/match_cli.py`
- Source: `r679-b.json`, row `B1_no_retirement`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_review_queue.py`
- Collected: 834 against a baseline of 834
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
- Collected: 834 against a baseline of 834
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
- Collected: 834 against a baseline of 834
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
- Collected: 834 against a baseline of 834
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
- Collected: 834 against a baseline of 834
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

### `u16-round-8-independent.V22_suppressed_warning_omitted`

The suppressed rows stop being reported on the warning channel, so a suppression is omitted silently (R36)

- File: `src/cratekit/acquire/match_cli.py`
- Source: `u16-round-8-independent.json`, row `V22_suppressed_warning_omitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 613 against a baseline of 613
- Kills: 26 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (Nightwave Remix) (feat. Mira)-]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (feat. Mira) (Nightwave Remix)-]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (feat. Mira)-Nightwave Remix]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path [ft. Mira] [Nightwave Remix]-]`
  - `tests/test_match_states.py::test_a_credited_listing_reaches_the_other_bracket_shape_of_its_own_version[round-listed]`
  - `tests/test_match_states.py::test_a_credited_listing_reaches_the_other_bracket_shape_of_its_own_version[square-listed]`
  - `tests/test_match_states.py::test_a_deletion_of_the_plain_record_never_withholds_the_credited_one`
  - `tests/test_match_states.py::test_a_listing_both_records_answer_is_reported_under_the_tombstone`
  - `tests/test_match_states.py::test_a_suppressed_version_is_reported_as_a_warning_carrying_its_identifier`
  - `tests/test_match_states.py::test_a_tombstone_is_addressed_by_every_reading_except_the_undecidable_one[round]`
  - `tests/test_match_states.py::test_a_tombstone_is_addressed_by_every_reading_except_the_undecidable_one[square]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path (Extended) (Remastered)]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path (Nightwave Remix)]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path (Original Mix)]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path (feat. Mira) (Nightwave Remix)]`
  - ... and 11 more, see the JSON sidecar

Old text:

```
    for track in result.suppressed:

```

New text:

```
    for track in ():

```

### `r1709.M10_title_identity_no_separator`

title_identity returns the bare text with no separator, so it can equal another title's fold

- File: `src/cratekit/acquire/match_identity.py`
- Source: `r1709.json`, row `M10_title_identity_no_separator`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3858 against a baseline of 3858
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_emoji_titles_identities_are_its_own`

Old text:

```
    return f"\x1f{bare}" if bare else ""

```

New text:

```
    return bare

```

### `r1709.M11_recording_identity_is_the_token`

recording_identity reads the title by fold, the base's token, so every identity collapses again

- File: `src/cratekit/acquire/match_identity.py`
- Source: `r1709.json`, row `M11_recording_identity_is_the_token`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3858 against a baseline of 3858
- Kills: 24 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_adjacent_answers_for_one_recording_fold_and_nothing_else_does[two-emoji-titles-stay-two-rows]`
  - `tests/intake/test_workers.py::test_a_recognised_track_is_keyed_by_recording_version_and_isrc_and_a_provider_row_by_its_id`
  - `tests/test_intake_missing_search.py::test_a_search_answered_by_another_emoji_title_is_not_exact[another-emoji]`
  - `tests/test_intake_missing_search.py::test_two_emoji_rows_are_each_searched_and_listed`
  - `tests/test_match_states.py::test_a_former_identifier_is_carried_only_with_one_fit_and_its_title`
  - `tests/test_match_states.py::test_a_held_emoji_row_does_not_retire_another_emoji_rows_question`
  - `tests/test_match_states.py::test_a_yes_recorded_before_naming_no_option_still_applies`
  - `tests/test_match_states.py::test_an_answer_about_one_emoji_title_does_not_settle_another`
  - `tests/test_match_states.py::test_an_answer_recorded_before_is_not_carried_to_another_emoji_file`
  - `tests/test_match_states.py::test_an_answer_recorded_before_naming_an_emoji_file_still_applies`
  - `tests/test_match_states.py::test_an_emoji_candidate_offered_for_another_is_named_a_resemblance`
  - `tests/test_match_states.py::test_an_emoji_titles_identities_are_its_own`
  - `tests/test_match_states.py::test_an_isrc_on_a_file_under_another_emoji_title_is_asked_not_settled`
  - `tests/test_match_states.py::test_the_wanted_emoji_title_is_owned_beside_another_one_the_library_holds`
  - `tests/test_match_states.py::test_two_different_emoji_titles_by_one_artist_are_not_one_recording`
  - ... and 9 more, see the JSON sidecar

Old text:

```
    return f"{fold(artist)}\x1f{title_identity(title)}"

```

New text:

```
    return f"{fold(artist)}\x1f{fold(title)}"

```

### `r1709.M17_question_identity_token`

the review item hashes the token, so a held emoji row retires another's question and one answer settles both

- File: `src/cratekit/acquire/match_identity.py`
- Source: `r1709.json`, row `M17_question_identity_token`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3858 against a baseline of 3858
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_held_emoji_row_does_not_retire_another_emoji_rows_question`
  - `tests/test_match_states.py::test_an_answer_about_one_emoji_title_does_not_settle_another`
  - `tests/test_match_states.py::test_an_emoji_titles_identities_are_its_own`

Old text:

```
        "recording": recording_identity(artist, title),

```

New text:

```
        "recording": recording_token(artist, title),

```

### `r1709.M1_bare_no_nfkc`

bare_title composes with NFC rather than NFKC, so a title of fullwidth marks or an ellipsis is a different title and a real duplicate is offered rather than owned

- File: `src/cratekit/acquire/match_identity.py`
- Source: `r1709.json`, row `M1_bare_no_nfkc`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3858 against a baseline of 3858
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_spelled_another_way_is_still_owned[ellipsis]`
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_spelled_another_way_is_still_owned[width]`

Old text:

```
    composed = unicodedata.normalize("NFKC", str(title))

```

New text:

```
    composed = unicodedata.normalize("NFC", str(title))

```

### `r1709.M3_bare_keeps_spaces`

bare_title keeps spacing, so ? ? and ?? are two titles and a real duplicate is not owned

- File: `src/cratekit/acquire/match_identity.py`
- Source: `r1709.json`, row `M3_bare_keeps_spaces`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3858 against a baseline of 3858
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_spelled_another_way_is_still_owned[spacing]`

Old text:

```
    return "".join(ch for ch in composed if not ch.isspace() and not _invisible(ch))

```

New text:

```
    return "".join(ch for ch in composed if not _invisible(ch))

```

### `r1709.M4_bare_keeps_invisible`

bare_title keeps every invisible character, so a variation selector or a joiner makes one title two

- File: `src/cratekit/acquire/match_identity.py`
- Source: `r1709.json`, row `M4_bare_keeps_invisible`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3858 against a baseline of 3858
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_search_answered_by_another_emoji_title_is_not_exact[the-same-emoji]`
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_spelled_another_way_is_still_owned[joiner]`
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_spelled_another_way_is_still_owned[selector]`
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_spelled_another_way_is_still_owned[text-and-emoji]`
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_spelled_another_way_is_still_owned[zero-width-space]`

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
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3858 against a baseline of 3858
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_search_answered_by_another_emoji_title_is_not_exact[the-same-emoji]`
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_spelled_another_way_is_still_owned[selector]`
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_spelled_another_way_is_still_owned[text-and-emoji]`

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

### `r1709.M6_no_format_characters`

_invisible no longer drops format characters, so a zero width joiner or space makes one title two

- File: `src/cratekit/acquire/match_identity.py`
- Source: `r1709.json`, row `M6_no_format_characters`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3858 against a baseline of 3858
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_spelled_another_way_is_still_owned[joiner]`
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_spelled_another_way_is_still_owned[zero-width-space]`

Old text:

```
    return unicodedata.category(ch) == "Cf" and point not in _TAG_CHARACTERS

```

New text:

```
    return False

```

### `r1709.M7_tag_characters_dropped`

_invisible drops the tag characters too, so England and Scotland flags are one title

- File: `src/cratekit/acquire/match_identity.py`
- Source: `r1709.json`, row `M7_tag_characters_dropped`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3858 against a baseline of 3858
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_two_flags_are_two_titles`

Old text:

```
    return unicodedata.category(ch) == "Cf" and point not in _TAG_CHARACTERS

```

New text:

```
    return unicodedata.category(ch) == "Cf"

```

### `r1709.M8_bare_for_every_title`

bare_title returns text for a title that folds to something too

- File: `src/cratekit/acquire/match_identity.py`
- Source: `r1709.json`, row `M8_bare_for_every_title`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3858 against a baseline of 3858
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_title_that_folds_to_something_compares_exactly_as_it_did`

Old text:

```
    if fold(title):
        return ""
    composed
```

New text:

```
    if False:
        return ""
    composed
```

### `r1709.M9_title_identity_is_the_fold`

title_identity returns the fold alone, the base's reading, so an emoji title is every other one by the artist

- File: `src/cratekit/acquire/match_identity.py`
- Source: `r1709.json`, row `M9_title_identity_is_the_fold`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3858 against a baseline of 3858
- Kills: 30 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_adjacent_answers_for_one_recording_fold_and_nothing_else_does[two-emoji-titles-stay-two-rows]`
  - `tests/intake/test_workers.py::test_a_recognised_track_is_keyed_by_recording_version_and_isrc_and_a_provider_row_by_its_id`
  - `tests/test_acquire_fallback.py::test_an_upload_question_about_one_emoji_title_is_not_another_ones`
  - `tests/test_intake_missing_search.py::test_a_search_answered_by_another_emoji_title_is_not_exact[another-emoji]`
  - `tests/test_intake_missing_search.py::test_the_identity_is_the_folded_row_and_not_its_spelling`
  - `tests/test_intake_missing_search.py::test_two_emoji_rows_are_each_searched_and_listed`
  - `tests/test_isrc_screen.py::test_a_provider_track_under_another_emoji_title_does_not_agree`
  - `tests/test_match_states.py::test_a_former_identifier_is_carried_only_with_one_fit_and_its_title`
  - `tests/test_match_states.py::test_a_held_emoji_row_does_not_retire_another_emoji_rows_question`
  - `tests/test_match_states.py::test_a_yes_recorded_before_naming_no_option_still_applies`
  - `tests/test_match_states.py::test_an_answer_about_one_emoji_title_does_not_settle_another`
  - `tests/test_match_states.py::test_an_answer_recorded_before_is_not_carried_to_another_emoji_file`
  - `tests/test_match_states.py::test_an_answer_recorded_before_naming_an_emoji_file_still_applies`
  - `tests/test_match_states.py::test_an_emoji_candidate_offered_for_another_is_named_a_resemblance`
  - `tests/test_match_states.py::test_an_emoji_titles_identities_are_its_own`
  - ... and 15 more, see the JSON sidecar

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
- Moved: Anchored where u305-replay-after.json replayed it: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1193 against a baseline of 1193
- Kills: 8 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_deleted_track_whose_row_kept_a_credit_is_suppressed_and_not_listed`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (Nightwave Remix) (feat. Mira)-]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (feat. Mira) (Nightwave Remix)-]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (feat. Mira)-Nightwave Remix]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path [ft. Mira] [Nightwave Remix]-]`
  - `tests/test_match_states.py::test_a_provider_row_crediting_somebody_else_is_not_withheld`
  - `tests/test_match_states.py::test_the_companion_reaches_exactly_what_ownership_reached`
  - `tests/test_match_states.py::test_the_two_copies_of_the_tombstone_identity_agree_once_both_exist`

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
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 705 against a baseline of 705
- Kills: 6 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_held_track_is_owned_and_nothing_is_listed[07A - 128 - Traumer, antraum, Anton - Hyaku.flac-tags2-row2]`
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

### `r679-b.C1_credited_rule_not_owning`

OWNING_RULES: leave the credited rule out, so its 4 items stay open

- File: `src/cratekit/acquire/match_identity.py`
- Source: `r679-b.json`, row `C1_credited_rule_not_owning`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_review_queue.py`
- Collected: 834 against a baseline of 834
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

- File: `src/cratekit/acquire/match_identity.py`
- Source: `r679-b.json`, row `C2_reading_shape_missing`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_review_queue.py`
- Collected: 834 against a baseline of 834
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

### `u16-round-8-independent.V14_tombstone_fold_nfd`

tombstone_fold normalizes NFD instead of NFC, drifting from U24's byte-for-byte algorithm so a recorded suppression can never be found

- File: `src/cratekit/acquire/match_identity.py`
- Source: `u16-round-8-independent.json`, row `V14_tombstone_fold_nfd`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 613 against a baseline of 613
- Kills: 4 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_composed_address_still_matches_a_row_spelled_that_way[Caf\xe9 del Mar-Track-Live]`
  - `tests/test_match_states.py::test_the_tombstone_fold_is_pinned_where_two_normalizations_disagree['Caf\xe9 del Mar'-'caf\xe9 del mar']`
  - `tests/test_match_states.py::test_the_tombstone_fold_is_pinned_where_two_normalizations_disagree['Cafe\u0301 del Mar'-'caf\xe9 del mar']`
  - `tests/test_match_states.py::test_the_two_copies_of_the_tombstone_identity_agree_once_both_exist`

Old text:

```
        " ", unicodedata.normalize("NFC", str(value)).casefold()

```

New text:

```
        " ", unicodedata.normalize("NFD", str(value)).casefold()

```

### `u16-round-8-independent.V15_empty_identity_accepted`

The empty tombstone identity refusal removed alone, so every unnamed candidate collides onto one suppression

- File: `src/cratekit/acquire/match_identity.py`
- Source: `u16-round-8-independent.json`, row `V15_empty_identity_accepted`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py; core/tombstone.py holds a second copy, which is not this row's target
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 613 against a baseline of 613
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_identity_with_neither_an_artist_nor_a_title_is_refused`

Old text:

```
    if not folded_artist and not folded_title:

```

New text:

```
    if False:

```

### `u16-round-8-independent.V16_key_leaves_item_identity`

The list's key leaves the review item identity, so one answer settles the key question and the version question both

- File: `src/cratekit/acquire/match_identity.py`
- Source: `u16-round-8-independent.json`, row `V16_key_leaves_item_identity`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 613 against a baseline of 613
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_list_line_that_names_a_key_is_a_different_question_from_one_that_does_not`
  - `tests/test_match_states.py::test_one_answered_key_question_never_settles_another_one`
  - `tests/test_match_states.py::test_the_review_item_identity_is_not_the_tombstone_identity`

Old text:

```
        "key": key_token(key),

```

New text:

```
        "key": "",

```

### `u16-round-8-independent.V20_digest_width_halved`

DIGEST_WIDTH coefficient halved from 16 to 8 hex characters, dropping identifier collision resistance from 64 to 32 bits

- File: `src/cratekit/acquire/match_identity.py`
- Source: `u16-round-8-independent.json`, row `V20_digest_width_halved`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 613 against a baseline of 613
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_every_identifier_this_module_generates_is_the_declared_width`
  - `tests/test_match_states.py::test_the_declared_width_survives_a_population_a_narrower_one_does_not`
  - `tests/test_match_states.py::test_the_digest_width_is_the_narrowest_one_that_meets_the_requirement`

Old text:

```
DIGEST_WIDTH = 16

```

New text:

```
DIGEST_WIDTH = 8

```

### `u213.M1_first_group_is_the_title`

split_version: drop the first group rule, so a title written wholly in brackets walks off whole and the row names no title

- File: `src/cratekit/acquire/match_identity.py`
- Source: `u213.json`, row `M1_first_group_is_the_title`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 726 against a baseline of 726
- Kills: 13 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_row_titled_wholly_in_brackets_is_queued_under_its_words`
  - `tests/test_match_states.py::test_a_head_in_the_title_tag_reads_as_the_stems_head_does[a-headed-tag-titled-wholly-in-brackets-matches-the-provider-row]`
  - `tests/test_match_states.py::test_a_provider_row_titled_wholly_in_brackets_reads_rather_than_refuses`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[  [Premade Sandwiches]  -expected2]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(Premade Sandwiches)-expected1]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(With Love) (Remix)-expected12]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(With Or Without You)-expected9]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(Without You)-expected10]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(feat. Mira)-expected13]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[Premade Sandwiches] (Live)-expected3]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[Premade Sandwiches] (feat. Mira)-expected4]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[Premade Sandwiches]-expected0]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[With You]-expected8]`

Old text:

```
        if found.start() == 0 and not _names_a_version(inside):
            remaining = inside
            break
```

New text:

```
        if False:
            remaining = inside
            break
```

### `u213.M21_first_group_version_check`

split_version: drop the version check from the first group rule, so a row titled only (Extended) reads as the title Extended and the emitter writes it

- File: `src/cratekit/acquire/match_identity.py`
- Source: `u213.json`, row `M21_first_group_version_check`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_listdoc.py`, `tests/intake/test_workers.py`
- Collected: 741 against a baseline of 741
- Kills: 6 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_row_the_reader_would_refuse_is_refused_by_the_emitter[only-a-version]`
  - `tests/test_match_states.py::test_a_provider_row_titled_wholly_in_brackets_reads_rather_than_refuses`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(Extended)-expected14]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(Without You Remix)-expected11]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[Original Mix] (Remastered)-expected15]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[Premade Sandwiches Live]-expected16]`

Old text:

```
        if found.start() == 0 and not _names_a_version(inside):
```

New text:

```
        if found.start() == 0:
```

### `u213.M22_names_a_version_last_word`

_names_a_version: read the group's first word rather than its last

- File: `src/cratekit/acquire/match_identity.py`
- Source: `u213.json`, row `M22_names_a_version_last_word`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_listdoc.py`, `tests/intake/test_workers.py`
- Collected: 741 against a baseline of 741
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(Without You Remix)-expected11]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[Premade Sandwiches Live]-expected16]`

Old text:

```
    return bool(words) and words[-1] in _DASH_VERSIONS
```

New text:

```
    return bool(words) and words[0] in _DASH_VERSIONS
```

### `u213.M3_first_group_position`

split_version: take any group as the title, not only the one standing first, so Song (Remix) reads as Remix

- File: `src/cratekit/acquire/match_identity.py`
- Source: `u213.json`, row `M3_first_group_position`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 726 against a baseline of 726
- Kills: 16 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[spotify-Sun Path (Live) (feat. Mira)-provider0-spelled_addresses0-provider_addresses0]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[spotify-Sun Path [Live] (feat. Mira)-provider1-spelled_addresses1-provider_addresses1]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[text-Sun Path (Live) (feat. Mira)-provider0-spelled_addresses0-provider_addresses0]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[text-Sun Path [Live] (feat. Mira)-provider1-spelled_addresses1-provider_addresses1]`
  - `tests/test_match_states.py::test_a_credited_rows_suppression_spellings_are_unchanged[Sun Path (Nightwave Remix) (ft Mira)-addresses1]`
  - `tests/test_match_states.py::test_a_featured_credit_is_a_performer_and_never_a_version`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[Featuring Anna]`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[feat. Anna]`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[ft Anna]`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[with Anna]`
  - `tests/test_match_states.py::test_a_held_file_crediting_somebody_else_never_calls_the_companion_stale`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[Premade Sandwiches] (feat. Mira)-expected4]`
  - `tests/test_match_states.py::test_of_two_near_hits_only_the_one_whose_title_resembles_is_offered`
  - `tests/test_match_states.py::test_the_companion_reaches_exactly_what_ownership_reached`
  - `tests/test_match_states.py::test_the_offer_limit_keeps_the_best_scoring_answers_and_says_what_it_kept_back`
  - ... and 1 more, see the JSON sidecar

Old text:

```
        if found.start() == 0 and not _names_a_version(inside):
```

New text:

```
        if found.start() >= 0 and not _names_a_version(inside):
```

### `u213.M4_first_group_keeps_brackets`

split_version: keep the brackets on a title written wholly in them

- File: `src/cratekit/acquire/match_identity.py`
- Source: `u213.json`, row `M4_first_group_keeps_brackets`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 726 against a baseline of 726
- Kills: 15 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_row_titled_wholly_in_brackets_is_queued_under_its_words`
  - `tests/intake/test_workers.py::test_a_set_aside_track_names_the_half_the_reader_names`
  - `tests/test_match_states.py::test_a_head_in_the_title_tag_reads_as_the_stems_head_does[a-headed-tag-titled-wholly-in-brackets-matches-the-provider-row]`
  - `tests/test_match_states.py::test_a_provider_row_titled_wholly_in_brackets_reads_rather_than_refuses`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[  [Premade Sandwiches]  -expected2]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(Premade Sandwiches)-expected1]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(With Love) (Remix)-expected12]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(With Or Without You)-expected9]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(Without You)-expected10]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(feat. Mira)-expected13]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[Premade Sandwiches] (Live)-expected3]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[Premade Sandwiches] (feat. Mira)-expected4]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[Premade Sandwiches]-expected0]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[With You]-expected8]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[]-expected7]`

Old text:

```
            remaining = inside
            break
```

New text:

```
            remaining = found.group(0).strip()
            break
```

### `u262.C1_letters_rule_back`

_is_a_credit: answer by the folded group's first letters again, the defect, so (Without You Remix) is a credit

- File: `src/cratekit/acquire/match_identity.py`
- Source: `u262.json`, row `C1_letters_rule_back`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py; core/tombstone.py holds a second copy, which is not this row's target
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_uncredited_tombstone.py`, `tests/test_tombstones.py`
- Collected: 685 against a baseline of 685
- Kills: 15 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_defect_title_keeps_the_tombstone_identity_its_spelling_always_had`
  - `tests/test_match_states.py::test_a_group_that_only_begins_with_a_credits_letters_is_a_version[Feature Edit]`
  - `tests/test_match_states.py::test_a_group_that_only_begins_with_a_credits_letters_is_a_version[Featureless Dub]`
  - `tests/test_match_states.py::test_a_group_that_only_begins_with_a_credits_letters_is_a_version[Withdrawn Mix]`
  - `tests/test_match_states.py::test_a_group_that_only_begins_with_a_credits_letters_is_a_version[Within Mix]`
  - `tests/test_match_states.py::test_a_group_that_only_begins_with_a_credits_letters_is_a_version[Without You Remix]`
  - `tests/test_match_states.py::test_a_library_file_whose_group_only_begins_with_a_credits_letters_is_that_version`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(Without You Remix)-expected11]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[Feature Edit]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[Featureless Dub]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[Featurette]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[Ftw Edit]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[Withdrawn Mix]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[Within Mix]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[Without You Remix]`

Old text:

```
    return bool(words) and words[0] in _CREDIT_MARKERS
```

New text:

```
    return any(" ".join(words).startswith(marker) for marker in _CREDIT_MARKERS)
```

### `u262.C2_any_word`

_is_a_credit: a marker anywhere in the group makes a credit, so (Live with Strings) loses its version

- File: `src/cratekit/acquire/match_identity.py`
- Source: `u262.json`, row `C2_any_word`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py; core/tombstone.py holds a second copy, which is not this row's target
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_uncredited_tombstone.py`, `tests/test_tombstones.py`
- Collected: 685 against a baseline of 685
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[Live with Strings]`

Old text:

```
    return bool(words) and words[0] in _CREDIT_MARKERS
```

New text:

```
    return any(word in _CREDIT_MARKERS for word in words)
```

### `u262.C3_last_word`

_is_a_credit: ask the group's last word rather than its first

- File: `src/cratekit/acquire/match_identity.py`
- Source: `u262.json`, row `C3_last_word`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py; core/tombstone.py holds a second copy, which is not this row's target
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_uncredited_tombstone.py`, `tests/test_tombstones.py`
- Collected: 685 against a baseline of 685
- Kills: 32 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[spotify-Sun Path (Live) (feat. Mira)-provider0-spelled_addresses0-provider_addresses0]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[spotify-Sun Path (feat. Mira) (Extended) (Remastered)-provider2-spelled_addresses2-provider_addresses2]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[spotify-Sun Path [Live] (feat. Mira)-provider1-spelled_addresses1-provider_addresses1]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[text-Sun Path (Live) (feat. Mira)-provider0-spelled_addresses0-provider_addresses0]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[text-Sun Path (feat. Mira) (Extended) (Remastered)-provider2-spelled_addresses2-provider_addresses2]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[text-Sun Path [Live] (feat. Mira)-provider1-spelled_addresses1-provider_addresses1]`
  - `tests/test_match_states.py::test_a_credited_listing_reaches_the_other_bracket_shape_of_its_own_version[round-listed]`
  - `tests/test_match_states.py::test_a_credited_rows_suppression_spellings_are_unchanged[Sun Path (Nightwave Remix) (ft Mira)-addresses1]`
  - `tests/test_match_states.py::test_a_credited_rows_suppression_spellings_are_unchanged[Sun Path (feat. Mira) (Nightwave Remix)-addresses0]`
  - `tests/test_match_states.py::test_a_credited_rows_suppression_spellings_are_unchanged[Sun Path (with Mira)-addresses2]`
  - `tests/test_match_states.py::test_a_featured_credit_is_a_performer_and_never_a_version`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[Featuring Anna]`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[feat. Anna]`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[ft Anna]`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[with Anna]`
  - ... and 17 more, see the JSON sidecar

Old text:

```
    return bool(words) and words[0] in _CREDIT_MARKERS
```

New text:

```
    return bool(words) and words[-1] in _CREDIT_MARKERS
```

### `u262.C4_unfolded_words`

_is_a_credit: split the raw group on spaces without folding, so feat. and Featuring are not markers

- File: `src/cratekit/acquire/match_identity.py`
- Source: `u262.json`, row `C4_unfolded_words`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_uncredited_tombstone.py`, `tests/test_tombstones.py`
- Collected: 685 against a baseline of 685
- Kills: 26 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[spotify-Sun Path (Live) (feat. Mira)-provider0-spelled_addresses0-provider_addresses0]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[spotify-Sun Path (feat. Mira) (Extended) (Remastered)-provider2-spelled_addresses2-provider_addresses2]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[spotify-Sun Path [Live] (feat. Mira)-provider1-spelled_addresses1-provider_addresses1]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[text-Sun Path (Live) (feat. Mira)-provider0-spelled_addresses0-provider_addresses0]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[text-Sun Path (feat. Mira) (Extended) (Remastered)-provider2-spelled_addresses2-provider_addresses2]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[text-Sun Path [Live] (feat. Mira)-provider1-spelled_addresses1-provider_addresses1]`
  - `tests/test_match_states.py::test_a_credited_listing_reaches_the_other_bracket_shape_of_its_own_version[round-listed]`
  - `tests/test_match_states.py::test_a_credited_rows_suppression_spellings_are_unchanged[Sun Path (feat. Mira) (Nightwave Remix)-addresses0]`
  - `tests/test_match_states.py::test_a_featured_credit_is_a_performer_and_never_a_version`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[Featuring Anna]`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[feat. Anna]`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_the_abbreviation_ft_stays_a_credit`
  - `tests/test_match_states.py::test_a_held_file_crediting_somebody_else_never_calls_the_companion_stale`
  - `tests/test_match_states.py::test_a_listing_that_spelled_a_credit_never_asks_for_a_companion[Sun Path (Nightwave Remix) (feat. Zed)]`
  - `tests/test_match_states.py::test_a_listing_that_spelled_a_credit_never_asks_for_a_companion[Sun Path (feat. Zed) (Nightwave Remix)]`
  - ... and 11 more, see the JSON sidecar

Old text:

```
    words = fold(inside).split()
    return bool(words) and words[0] in _CREDIT_MARKERS
```

New text:

```
    words = str(inside).split()
    return bool(words) and words[0] in _CREDIT_MARKERS
```

### `u262.C5_no_with`

_CREDIT_MARKERS: drop with, so (with Anna) becomes a version

- File: `src/cratekit/acquire/match_identity.py`
- Source: `u262.json`, row `C5_no_with`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_uncredited_tombstone.py`, `tests/test_tombstones.py`
- Collected: 685 against a baseline of 685
- Kills: 7 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_rows_suppression_spellings_are_unchanged[Sun Path (with Mira)-addresses2]`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[with Anna]`
  - `tests/test_match_states.py::test_a_listing_that_spelled_a_credit_never_asks_for_a_companion[Sun Path (with Zed) - Nightwave Remix]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[With You]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[With]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[with Anna]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_share_one_credit_vocabulary`

Old text:

```
_CREDIT_MARKERS: frozenset[str] = frozenset({"feat", "ft", "featuring", "with"})
```

New text:

```
_CREDIT_MARKERS: frozenset[str] = frozenset({"feat", "ft", "featuring"})
```

### `u262.C6_no_ft`

_CREDIT_MARKERS: drop ft, so (ft Anna) becomes a version

- File: `src/cratekit/acquire/match_identity.py`
- Source: `u262.json`, row `C6_no_ft`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_uncredited_tombstone.py`, `tests/test_tombstones.py`
- Collected: 685 against a baseline of 685
- Kills: 9 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_rows_suppression_spellings_are_unchanged[Sun Path (Nightwave Remix) (ft Mira)-addresses1]`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[ft Anna]`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_the_abbreviation_ft_stays_a_credit`
  - `tests/test_match_states.py::test_a_listing_that_spelled_a_credit_never_asks_for_a_companion[Sun Path [ft. Zed] [Nightwave Remix]]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[FT. Anna]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[Ft Worth Edit]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[ft Anna]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[ft.anna]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_share_one_credit_vocabulary`

Old text:

```
_CREDIT_MARKERS: frozenset[str] = frozenset({"feat", "ft", "featuring", "with"})
```

New text:

```
_CREDIT_MARKERS: frozenset[str] = frozenset({"feat", "featuring", "with"})
```

### `u262.C7_no_featuring`

_CREDIT_MARKERS: drop featuring, so (Featuring Anna) becomes a version

- File: `src/cratekit/acquire/match_identity.py`
- Source: `u262.json`, row `C7_no_featuring`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_uncredited_tombstone.py`, `tests/test_tombstones.py`
- Collected: 685 against a baseline of 685
- Kills: 4 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[Featuring Anna]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[Featuring Anna]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[featuring]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_share_one_credit_vocabulary`

Old text:

```
_CREDIT_MARKERS: frozenset[str] = frozenset({"feat", "ft", "featuring", "with"})
```

New text:

```
_CREDIT_MARKERS: frozenset[str] = frozenset({"feat", "ft", "with"})
```

### `u262.C8_no_feat`

_CREDIT_MARKERS: drop feat, so (feat. Anna) becomes a version

- File: `src/cratekit/acquire/match_identity.py`
- Source: `u262.json`, row `C8_no_feat`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_uncredited_tombstone.py`, `tests/test_tombstones.py`
- Collected: 685 against a baseline of 685
- Kills: 19 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[spotify-Sun Path (Live) (feat. Mira)-provider0-spelled_addresses0-provider_addresses0]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[spotify-Sun Path (feat. Mira) (Extended) (Remastered)-provider2-spelled_addresses2-provider_addresses2]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[spotify-Sun Path [Live] (feat. Mira)-provider1-spelled_addresses1-provider_addresses1]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[text-Sun Path (Live) (feat. Mira)-provider0-spelled_addresses0-provider_addresses0]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[text-Sun Path (feat. Mira) (Extended) (Remastered)-provider2-spelled_addresses2-provider_addresses2]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[text-Sun Path [Live] (feat. Mira)-provider1-spelled_addresses1-provider_addresses1]`
  - `tests/test_match_states.py::test_a_credited_listing_reaches_the_other_bracket_shape_of_its_own_version[round-listed]`
  - `tests/test_match_states.py::test_a_credited_rows_suppression_spellings_are_unchanged[Sun Path (feat. Mira) (Nightwave Remix)-addresses0]`
  - `tests/test_match_states.py::test_a_featured_credit_is_a_performer_and_never_a_version`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[feat. Anna]`
  - `tests/test_match_states.py::test_a_held_file_crediting_somebody_else_never_calls_the_companion_stale`
  - `tests/test_match_states.py::test_a_listing_that_spelled_a_credit_never_asks_for_a_companion[Sun Path (Nightwave Remix) (feat. Zed)]`
  - `tests/test_match_states.py::test_a_listing_that_spelled_a_credit_never_asks_for_a_companion[Sun Path (feat. Zed) (Nightwave Remix)]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[Premade Sandwiches] (feat. Mira)-expected4]`
  - `tests/test_match_states.py::test_the_companion_reaches_exactly_what_ownership_reached`
  - ... and 4 more, see the JSON sidecar

Old text:

```
_CREDIT_MARKERS: frozenset[str] = frozenset({"feat", "ft", "featuring", "with"})
```

New text:

```
_CREDIT_MARKERS: frozenset[str] = frozenset({"ft", "featuring", "with"})
```

### `u265.M1_narrow_split_everywhere`

_sorted_words: split every string on the narrow set, so a wide string keeps U+0085 and U+00A0 inside a word where the scorer splits

- File: `src/cratekit/acquire/match_identity.py`
- Source: `u265.json`, row `M1_narrow_split_everywhere`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`
- Collected: 2712 against a baseline of 2712
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_every_pair_scores_the_same_through_the_sorted_form`
  - `tests/test_match_states.py::test_the_word_sort_splits_on_exactly_the_whitespace_the_scorer_splits_on`

Old text:

```
    if token and max(token) > "\xff":
        words = token.split()
```

New text:

```
    if False:
        words = token.split()
```

### `u265.M2_python_split_everywhere`

_sorted_words: split every string on Python whitespace, so a narrow string splits on U+0085 and U+00A0 where the scorer does not

- File: `src/cratekit/acquire/match_identity.py`
- Source: `u265.json`, row `M2_python_split_everywhere`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`
- Collected: 2712 against a baseline of 2712
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_every_pair_scores_the_same_through_the_sorted_form`
  - `tests/test_match_states.py::test_the_word_sort_splits_on_exactly_the_whitespace_the_scorer_splits_on`

Old text:

```
    if token and max(token) > "\xff":
        words = token.split()
```

New text:

```
    if True:
        words = token.split()
```

### `u265.M2b_width_off_by_one`

_sorted_words: read a string as wide from U+00FF rather than U+0100, so a narrow name ending in y with a diaeresis splits on U+00A0 where the scorer does not (review round one's finding)

- File: `src/cratekit/acquire/match_identity.py`
- Source: `u265.json`, row `M2b_width_off_by_one`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`
- Collected: 2712 against a baseline of 2712
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_the_word_sort_splits_on_exactly_the_whitespace_the_scorer_splits_on`

Old text:

```
    if token and max(token) > "\xff":
```

New text:

```
    if token and max(token) >= "\xff":
```

### `u265.M3_words_not_sorted`

_sorted_words: join the words in their own order, so the pass scores plain ratio and an artist and title swap no longer matches

- File: `src/cratekit/acquire/match_identity.py`
- Source: `u265.json`, row `M3_words_not_sorted`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`
- Collected: 2712 against a baseline of 2712
- Kills: 18 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_file_whose_artist_and_title_are_the_rows_swapped_is_still_offered`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Lights Midnight-Midnight Lights]`
  - `tests/test_match_states.py::test_a_spelled_number_is_not_read_as_a_numeral[Four Tune-Fortune]`
  - `tests/test_match_states.py::test_a_swapped_listing_split_differently_is_still_offered[Aurora Bloom - Every Day-Everyday - Aurora Bloom]`
  - `tests/test_match_states.py::test_a_swapped_listing_split_differently_is_still_offered[Aurora Bloom - Goodbye-Good Bye - Aurora Bloom]`
  - `tests/test_match_states.py::test_a_swapped_listing_split_differently_is_still_offered[Aurora Bloom - OK-O.K. - Aurora Bloom]`
  - `tests/test_match_states.py::test_a_swapped_listing_split_differently_is_still_offered[M.I.A. - Paper Planes-Paper Planes - MIA]`
  - `tests/test_match_states.py::test_every_pair_scores_the_same_through_the_sorted_form`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[265-5]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[265-None]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[2650-5]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[2650-None]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[26500-5]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[26500-None]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - ... and 3 more, see the JSON sidecar

Old text:

```
    return " ".join(sorted(words))
```

New text:

```
    return " ".join(words)
```

### `u269.M7_match_engine_binds_lxml`

acquire/match.py: bind lxml.etree under a branch that never runs, the export reader guard's lxml case, which stays as it is

- File: `src/cratekit/acquire/match_identity.py`
- Source: `u269.json`, row `M7_match_engine_binds_lxml`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py; match.py no longer imports hashlib, and the export guard reads all four match modules
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 613 against a baseline of 613
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_the_export_guard_stays_quiet_on_correct_code[from . import match\n]`
  - `tests/test_match_states.py::test_the_match_engine_never_reaches_a_rekordbox_export`

Old text:

```
import hashlib

```

New text:

```
import hashlib

if False:
    import lxml.etree  # noqa: F401

```

### `u305.M1_recorded_recording_swapped`

Recorded.recording: fold the title as the artist and the artist as the title, so a list row and a held file disagree on their recording

- File: `src/cratekit/acquire/match_identity.py`
- Source: `u305.json`, row `M1_recorded_recording_swapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_library_reads_remembered.py`
- Collected: 642 against a baseline of 642
- Kills: 71 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_read_that_failed_is_not_remembered`
  - `tests/test_library_reads_remembered.py::test_an_unchanged_old_file_is_answered_from_memory_on_the_second_index`
  - `tests/test_match_states.py::test_a_half_tagged_file_does_not_get_an_identity_matching_neither_source`
  - `tests/test_match_states.py::test_a_head_in_the_title_tag_reads_as_the_stems_head_does[a-head-found-only-in-the-tag-carries-the-key-when-the-stem-has-none]`
  - `tests/test_match_states.py::test_a_head_in_the_title_tag_reads_as_the_stems_head_does[a-head-inside-the-title-tag-is-stripped-so-a-plain-provider-row-matches]`
  - `tests/test_match_states.py::test_a_head_in_the_title_tag_reads_as_the_stems_head_does[a-head-only-in-the-filename-with-a-plain-tag-indexes-as-it-did]`
  - `tests/test_match_states.py::test_a_head_in_the_title_tag_reads_as_the_stems_head_does[a-head-written-as-a-suffix-inside-the-tag-comes-off-as-it-does-from-the-stem]`
  - `tests/test_match_states.py::test_a_head_in_the_title_tag_reads_as_the_stems_head_does[a-headed-tag-titled-wholly-in-brackets-matches-the-provider-row]`
  - `tests/test_match_states.py::test_a_head_in_the_title_tag_reads_as_the_stems_head_does[a-plain-title-tag-is-untouched-by-the-head-strip]`
  - `tests/test_match_states.py::test_a_head_in_the_title_tag_reads_as_the_stems_head_does[a-tag-that-is-only-a-head-falls-to-the-filename-the-way-an-empty-tag-does]`
  - `tests/test_match_states.py::test_a_head_in_the_title_tag_reads_as_the_stems_head_does[a-title-that-genuinely-ends-with-a-camelot-code-and-a-number-loses-that-tail]`
  - `tests/test_match_states.py::test_a_head_in_the_title_tag_reads_as_the_stems_head_does[a-title-that-genuinely-opens-with-a-camelot-code-and-a-number-is-read-as-a-head]`
  - `tests/test_match_states.py::test_a_head_in_the_title_tag_reads_as_the_stems_head_does[the-tempo-goes-with-the-head-and-a-number-opening-the-title-stays]`
  - `tests/test_match_states.py::test_a_headed_tag_with_a_lossy_marker_strips_under_the_librarys_template`
  - `tests/test_match_states.py::test_a_headless_file_takes_its_key_from_initialkey_and_has_none_without_it`
  - ... and 56 more, see the JSON sidecar

Old text:

```
        return recording_token(self.artist, self.title)
```

New text:

```
        return recording_token(self.title, self.artist)
```

### `u305.M2_recorded_distinct_is_the_token`

Recorded.distinct: answer the folded token, so two titles of marks alone share one identity

- File: `src/cratekit/acquire/match_identity.py`
- Source: `u305.json`, row `M2_recorded_distinct_is_the_token`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_library_reads_remembered.py`
- Collected: 642 against a baseline of 642
- Kills: 15 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_former_identifier_is_carried_only_with_one_fit_and_its_title`
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_spelled_another_way_is_still_owned[ellipsis]`
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_spelled_another_way_is_still_owned[joiner]`
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_spelled_another_way_is_still_owned[marks]`
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_spelled_another_way_is_still_owned[selector]`
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_spelled_another_way_is_still_owned[spacing]`
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_spelled_another_way_is_still_owned[text-and-emoji]`
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_spelled_another_way_is_still_owned[width]`
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_spelled_another_way_is_still_owned[zero-width-space]`
  - `tests/test_match_states.py::test_a_yes_recorded_before_naming_no_option_still_applies`
  - `tests/test_match_states.py::test_an_answer_recorded_before_is_not_carried_to_another_emoji_file`
  - `tests/test_match_states.py::test_an_answer_recorded_before_naming_an_emoji_file_still_applies`
  - `tests/test_match_states.py::test_an_emoji_titles_identities_are_its_own`
  - `tests/test_match_states.py::test_two_emoji_rows_in_one_list_carry_two_match_identifiers`
  - `tests/test_match_states.py::test_two_held_emoji_titles_are_offered_as_two_candidates`

Old text:

```
        return recording_identity(self.artist, self.title)
```

New text:

```
        return recording_token(self.artist, self.title)
```

### `u305.M3_recorded_version_key_unfolded`

Recorded.version_key: fold the version without dropping the no-op qualifiers, so Original Mix and nothing are two versions

- File: `src/cratekit/acquire/match_identity.py`
- Source: `u305.json`, row `M3_recorded_version_key_unfolded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`, `tests/test_outbound_tidal_account.py`
- Collected: 163 against a baseline of 163
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_an_original_mix_row_and_a_bare_candidate_are_one_version`
  - `tests/test_intake_missing_search.py::test_the_identity_is_the_folded_row_and_not_its_spelling`
  - `tests/test_outbound_tidal_account.py::test_the_release_agreeing_with_the_rows_names_is_the_match[no-version-agrees-with-an-original-mix-not-an-edit]`

Old text:

```
        return version_token(self.version)
```

New text:

```
        return fold(self.version)
```

### `r1705.M10_holds_always`

_holds_spelling answers yes for every title, so the lookup offers OK against O.K., U286's split class, where the score did not

- File: `src/cratekit/acquire/match_library.py`
- Source: `r1705.json`, row `M10_holds_always`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 4 (killed)
- Killed:
  - `tests/test_match_states.py::test_the_lookup_does_not_widen_a_title_split_differently`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`

Old text:

```
    return any(word in _SPELLED_OUT for word in title.split())

```

New text:

```
    return True

```

### `r1705.M11_holds_reads_artist`

_holds_spelling reads the artist half of the token rather than the title

- File: `src/cratekit/acquire/match_library.py`
- Source: `r1705.json`, row `M11_holds_reads_artist`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 38 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_a_slang_title_through_the_real_verb_is_asked_and_not_downloaded`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4 U-For You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4 U-For You-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4Ever-Forever-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4Ever-Forever-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-I Would Die 4 U-I Would Die For You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-I Would Die 4 U-I Would Die For You-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-Luv U 2-Love You Too-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-Luv U 2-Love You Too-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Monkey Safari-2 Nite-Tonight-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Monkey Safari-2 Nite-Tonight-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Prince-4 U-For You-slang-held]`
  - ... and 23 more, see the JSON sidecar

Old text:

```
    _artist, _separator, title = recording.partition("\x1f")

```

New text:

```
    title, _separator, _artist = recording.partition("\x1f")

```

### `r1705.M12_lookup_ignores_wanted_side`

spelled_alike ignores a listed word in the WANTED title, so 4 U against a held For You for a short artist reads missing

- File: `src/cratekit/acquire/match_library.py`
- Source: `r1705.json`, row `M12_lookup_ignores_wanted_side`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 28 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_a_slang_title_through_the_real_verb_is_asked_and_not_downloaded`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4 U-For You-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4Ever-Forever-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-I Would Die 4 U-I Would Die For You-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Monkey Safari-2 Nite-Tonight-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Prince-4 U-For You-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Prince-I Would Die 4 U-I Would Die For You-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Prince-Luv U-Love You-slang-wanted]`
  - `tests/test_match_states.py::test_every_listed_spelling_offers_its_spelled_out_title[2-to]`
  - `tests/test_match_states.py::test_every_listed_spelling_offers_its_spelled_out_title[2day-today]`
  - `tests/test_match_states.py::test_every_listed_spelling_offers_its_spelled_out_title[2morrow-tomorrow]`
  - `tests/test_match_states.py::test_every_listed_spelling_offers_its_spelled_out_title[2nite-tonight]`
  - `tests/test_match_states.py::test_every_listed_spelling_offers_its_spelled_out_title[4-for]`
  - ... and 13 more, see the JSON sidecar

Old text:

```
        asks = _holds_spelling(recording)

```

New text:

```
        asks = False

```

### `r1705.M13_lookup_ignores_held_side`

spelled_alike ignores a listed word in the HELD title, so For You against a held 4 U for a short artist reads missing

- File: `src/cratekit/acquire/match_library.py`
- Source: `r1705.json`, row `M13_lookup_ignores_held_side`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 25 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4 U-For You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4Ever-Forever-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-I Would Die 4 U-I Would Die For You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Monkey Safari-2 Nite-Tonight-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Prince-4 U-For You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Prince-I Would Die 4 U-I Would Die For You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Prince-Luv U-Love You-slang-held]`
  - `tests/test_match_states.py::test_every_listed_spelling_offers_its_spelled_out_title[2-to]`
  - `tests/test_match_states.py::test_every_listed_spelling_offers_its_spelled_out_title[2day-today]`
  - `tests/test_match_states.py::test_every_listed_spelling_offers_its_spelled_out_title[2morrow-tomorrow]`
  - `tests/test_match_states.py::test_every_listed_spelling_offers_its_spelled_out_title[2nite-tonight]`
  - `tests/test_match_states.py::test_every_listed_spelling_offers_its_spelled_out_title[4-for]`
  - `tests/test_match_states.py::test_every_listed_spelling_offers_its_spelled_out_title[4ever-forever]`
  - `tests/test_match_states.py::test_every_listed_spelling_offers_its_spelled_out_title[b4-before]`
  - ... and 10 more, see the JSON sidecar

Old text:

```
            if asks or _holds_spelling(token)

```

New text:

```
            if asks

```

### `r1705.M14_lookup_key_drops_artist`

_spelled_key drops the artist, so a spelled out copy by another artist is offered

- File: `src/cratekit/acquire/match_library.py`
- Source: `r1705.json`, row `M14_lookup_key_drops_artist`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 6 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_a_spelled_out_copy_by_another_artist_is_not_offered`
  - `tests/test_match_states.py::test_the_lookup_reads_the_artist_as_it_folds_and_never_spelled_out`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`

Old text:

```
    return f"{artist}{separator}{_spelled_out(title)}"

```

New text:

```
    return f"{separator}{_spelled_out(title)}"

```

### `r1705.M15_lookup_key_spells_artist`

_spelled_key spells the artist out too, so Lil Kid and Little Kid read as one artist

- File: `src/cratekit/acquire/match_library.py`
- Source: `r1705.json`, row `M15_lookup_key_spells_artist`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_the_lookup_reads_the_artist_as_it_folds_and_never_spelled_out`

Old text:

```
    return f"{artist}{separator}{_spelled_out(title)}"

```

New text:

```
    return f"{_spelled_out(artist)}{separator}{_spelled_out(title)}"

```

### `r1705.M1_luv_unlisted`

_SPELLED_OUT loses luv, so Luv U against a held Love You reads missing and downloads

- File: `src/cratekit/acquire/match_library.py`
- Source: `r1705.json`, row `M1_luv_unlisted`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 15 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-Luv U 2-Love You Too-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-Luv U 2-Love You Too-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Monkey Safari-Luv U-Love You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Monkey Safari-Luv U-Love You-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Prince-Luv U-Love You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Prince-Luv U-Love You-slang-wanted]`
  - `tests/test_match_states.py::test_every_listed_spelling_offers_its_spelled_out_title[luv-love]`
  - `tests/test_match_states.py::test_the_lookup_is_what_reaches_a_pair_discovery_cannot_score`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`
  - `tests/test_match_states.py::test_the_word_list_is_the_curated_one`

Old text:

```
        "luv": "love",

```

New text:

```
(empty)
```

### `r1705.M2_four_numeral_unlisted`

_SPELLED_OUT loses 4, so 4 U against a held For You reads missing and downloads

- File: `src/cratekit/acquire/match_library.py`
- Source: `r1705.json`, row `M2_four_numeral_unlisted`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 14 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_slang_title_through_the_real_verb_is_asked_and_not_downloaded`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4 U-For You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4 U-For You-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-I Would Die 4 U-I Would Die For You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-I Would Die 4 U-I Would Die For You-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Monkey Safari-4 U-For You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Monkey Safari-4 U-For You-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Prince-4 U-For You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Prince-4 U-For You-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Prince-I Would Die 4 U-I Would Die For You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Prince-I Would Die 4 U-I Would Die For You-slang-wanted]`
  - `tests/test_match_states.py::test_every_listed_spelling_offers_its_spelled_out_title[4-for]`
  - `tests/test_match_states.py::test_the_lookup_is_what_reaches_a_pair_discovery_cannot_score`
  - `tests/test_match_states.py::test_the_word_list_is_the_curated_one`

Old text:

```
        "4": "for",

```

New text:

```
(empty)
```

### `r1705.M3_too_unlisted`

_SPELLED_OUT loses too, so Luv U 2 against a held Love You Too reads missing

- File: `src/cratekit/acquire/match_library.py`
- Source: `r1705.json`, row `M3_too_unlisted`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-Luv U 2-Love You Too-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-Luv U 2-Love You Too-slang-wanted]`
  - `tests/test_match_states.py::test_the_word_list_is_the_curated_one`

Old text:

```
        "too": "to",

```

New text:

```
(empty)
```

### `r1705.M4_2nite_unlisted`

_SPELLED_OUT loses 2nite, so 2Nite against Tonight reads missing

- File: `src/cratekit/acquire/match_library.py`
- Source: `r1705.json`, row `M4_2nite_unlisted`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_every_listed_spelling_offers_its_spelled_out_title[2nite-tonight]`
  - `tests/test_match_states.py::test_the_word_list_is_the_curated_one`

Old text:

```
        "2nite": "tonight",

```

New text:

```
(empty)
```

### `r1705.M8_spelled_keeps_spaces`

_spelled_out joins the words with a space, so 2 Nite against Tonight is no longer one string

- File: `src/cratekit/acquire/match_library.py`
- Source: `r1705.json`, row `M8_spelled_keeps_spaces`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 7 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-2 Nite-Tonight-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-2 Nite-Tonight-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Monkey Safari-2 Nite-Tonight-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Monkey Safari-2 Nite-Tonight-slang-wanted]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`

Old text:

```
    return "".join(_SPELLED_OUT.get(word, word) for word in folded.split())

```

New text:

```
    return " ".join(_SPELLED_OUT.get(word, word) for word in folded.split())

```

### `r1705.M9_spelled_spells_nothing`

_spelled_out spells no word out, so the reading and the lookup join nothing the written form does not

- File: `src/cratekit/acquire/match_library.py`
- Source: `r1705.json`, row `M9_spelled_spells_nothing`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3775 against a baseline of 3775
- Kills: 52 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_a_slang_title_through_the_real_verb_is_asked_and_not_downloaded`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-2 Nite-Tonight-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-2 Nite-Tonight-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4 U-For You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4 U-For You-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4Ever-Forever-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4Ever-Forever-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-B4 U Go-Before You Go-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-B4 U Go-Before You Go-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-I Would Die 4 U-I Would Die For You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-I Would Die 4 U-I Would Die For You-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-Luv U 2-Love You Too-slang-held]`
  - ... and 37 more, see the JSON sidecar

Old text:

```
    return "".join(_SPELLED_OUT.get(word, word) for word in folded.split())

```

New text:

```
    return "".join(word for word in folded.split())

```

### `r1709.M12_held_exact_unfiltered`

LibraryIndex.held keeps every file under the token, so a held fire emoji owns a wanted drop

- File: `src/cratekit/acquire/match_library.py`
- Source: `r1709.json`, row `M12_held_exact_unfiltered`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3858 against a baseline of 3858
- Kills: 14 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_held_emoji_row_does_not_retire_another_emoji_rows_question`
  - `tests/test_match_states.py::test_an_answer_about_one_emoji_title_does_not_settle_another`
  - `tests/test_match_states.py::test_an_emoji_candidate_offered_for_another_is_named_a_resemblance`
  - `tests/test_match_states.py::test_an_isrc_on_a_file_under_another_emoji_title_is_asked_not_settled`
  - `tests/test_match_states.py::test_the_wanted_emoji_title_is_owned_beside_another_one_the_library_holds`
  - `tests/test_match_states.py::test_two_different_emoji_titles_by_one_artist_are_not_one_recording`
  - `tests/test_match_states.py::test_two_different_emoji_titles_through_the_real_verb_are_not_owned`
  - `tests/test_match_states.py::test_two_held_emoji_titles_are_offered_as_two_candidates`
  - `tests/test_match_states.py::test_two_titles_that_fold_to_nothing_and_differ_are_not_one_title[!!!-!!]`
  - `tests/test_match_states.py::test_two_titles_that_fold_to_nothing_and_differ_are_not_one_title[!!!-???]`
  - `tests/test_match_states.py::test_two_titles_that_fold_to_nothing_and_differ_are_not_one_title[\U0001f44d-\U0001f44d\U0001f3fd]`
  - `tests/test_match_states.py::test_two_titles_that_fold_to_nothing_and_differ_are_not_one_title[\U0001f4a7-\U0001f525]`
  - `tests/test_match_states.py::test_two_titles_that_fold_to_nothing_and_differ_are_not_one_title[\U0001f525-]`
  - `tests/test_match_states.py::test_two_titles_that_fold_to_nothing_and_differ_are_not_one_title[\u2764-\u2665]`

Old text:

```
            if one.distinct == distinct

```

New text:

```
            if True

```

### `r1709.M13_held_credited_by_fold`

the credited list rule compares the fold alone again

- File: `src/cratekit/acquire/match_library.py`
- Source: `r1709.json`, row `M13_held_credited_by_fold`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3858 against a baseline of 3858
- Kills: 9 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_held_emoji_row_does_not_retire_another_emoji_rows_question`
  - `tests/test_match_states.py::test_an_answer_about_one_emoji_title_does_not_settle_another`
  - `tests/test_match_states.py::test_an_emoji_candidate_offered_for_another_is_named_a_resemblance`
  - `tests/test_match_states.py::test_an_isrc_on_a_file_under_another_emoji_title_is_asked_not_settled`
  - `tests/test_match_states.py::test_the_credited_list_rule_tells_two_emoji_titles_apart`
  - `tests/test_match_states.py::test_the_wanted_emoji_title_is_owned_beside_another_one_the_library_holds`
  - `tests/test_match_states.py::test_two_different_emoji_titles_by_one_artist_are_not_one_recording`
  - `tests/test_match_states.py::test_two_different_emoji_titles_through_the_real_verb_are_not_owned`
  - `tests/test_match_states.py::test_two_held_emoji_titles_are_offered_as_two_candidates`

Old text:

```
            if same_title(one.title, title) and member in one.members

```

New text:

```
            if member in one.members

```

### `r664.E1_stem_head_kept`

Stop stripping the head from the stem, the filename half of the same rule

- File: `src/cratekit/acquire/match_library.py`
- Source: `r664.json`, row `E1_stem_head_kept`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1193 against a baseline of 1193
- Kills: 149 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_an_intake_job_that_owns_a_row_by_isrc_retires_the_question_an_earlier_job_asked`
  - `tests/test_match_states.py::test_a_candidate_whose_title_folds_to_something_keeps_its_identifier`
  - `tests/test_match_states.py::test_a_file_whose_artist_and_title_are_the_rows_swapped_is_still_offered`
  - `tests/test_match_states.py::test_a_half_tagged_file_does_not_get_an_identity_matching_neither_source`
  - `tests/test_match_states.py::test_a_head_in_the_title_tag_reads_as_the_stems_head_does[a-tag-that-is-only-a-head-falls-to-the-filename-the-way-an-empty-tag-does]`
  - `tests/test_match_states.py::test_a_held_emoji_row_does_not_retire_another_emoji_rows_question`
  - `tests/test_match_states.py::test_a_held_file_crediting_somebody_else_never_calls_the_companion_stale`
  - `tests/test_match_states.py::test_a_key_question_answered_elsewhere_does_not_settle_a_version_question`
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_lossy_marker_the_template_declares_is_stripped_from_the_recording`
  - `tests/test_match_states.py::test_a_one_letter_title_is_judged_by_the_same_rule`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Acoustic]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Demo]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Dub]`
  - ... and 134 more, see the JSON sidecar

Old text:

```
    body = naming.strip_heads(stem, template=template)

```

New text:

```
    body = stem

```

### `r664.E2_pair_rule_field_by_field`

Collapse the pair rule to field by field fallback, the shape that assembled an identity matching neither source

- File: `src/cratekit/acquire/match_library.py`
- Source: `r664.json`, row `E2_pair_rule_field_by_field`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1193 against a baseline of 1193
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_half_tagged_file_does_not_get_an_identity_matching_neither_source`

Old text:

```
    if tagged_artist and tagged_title:
        artist, spelled = tagged_artist, tagged_title
    elif named_artist and named_title:
        artist, spelled = named_artist, named_title
    else:
        artist, spelled = tagged_artist or named_artist, tagged_title or named_title

```

New text:

```
    artist, spelled = tagged_artist or named_artist, tagged_title or named_title

```

### `r664.E4_title_not_split`

Skip split_title on the chosen title, so a version stays inside the recording token

- File: `src/cratekit/acquire/match_library.py`
- Source: `r664.json`, row `E4_title_not_split`
- Moved: Anchored where u305-replay-after.json replayed it: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1193 against a baseline of 1193
- Kills: 106 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_an_intake_job_that_owns_a_row_by_isrc_retires_the_question_an_earlier_job_asked`
  - `tests/intake/test_workers.py::test_an_offered_track_is_a_review_item_asked_once_however_often_it_is_redone`
  - `tests/intake/test_workers.py::test_favorites_lists_the_hearts_resolves_each_and_rereads_the_reasons_on_every_resume`
  - `tests/intake/test_workers.py::test_identify_and_a_set_job_report_owned_offered_and_missing`
  - `tests/intake/test_workers.py::test_queueing_and_resolving_favorites_name_the_job_each_count_its_reasons_and_the_next_command`
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
  - ... and 91 more, see the JSON sidecar

Old text:

```
    title, version = split_title(spelled)

```

New text:

```
    title, version = spelled, ""

```

### `r667-b.B2_reader_isrc_unfolded`

_read_from_disk: the ISRC tag carried verbatim, r667's G18 after its direct tests

- File: `src/cratekit/acquire/match_library.py`
- Source: `r667-b.json`, row `B2_reader_isrc_unfolded`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 705 against a baseline of 705
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_files_isrc_tag_is_folded_before_it_is_indexed`
  - `tests/test_match_states.py::test_a_malformed_isrc_tag_is_not_an_identity`

Old text:

```
        isrc=isrc_token(read["isrc"]),
```

New text:

```
        isrc=str(read["isrc"] or ""),
```

### `r667.E1_title_head_kept`

Existing: _read_from_disk takes the title tag verbatim, the R-664 defect

- File: `src/cratekit/acquire/match_library.py`
- Source: `r667.json`, row `E1_title_head_kept`
- Moved: Anchored where u305-replay-after.json replayed it: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 705 against a baseline of 705
- Kills: 33 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_held_track_is_owned_and_nothing_is_listed[04A - 126 - Malive, Tito Azevedo, MRQZ - Burning (Extended Mix).flac-tags1-row1]`
  - `tests/test_intake_missing.py::test_a_held_track_is_owned_and_nothing_is_listed[07A - 128 - Traumer, antraum, Anton - Hyaku.flac-tags2-row2]`
  - `tests/test_intake_missing.py::test_a_held_track_is_owned_and_nothing_is_listed[08A - 124 - Aurora Bloom - Sun Path.flac-tags0-row0]`
  - `tests/test_match_states.py::test_a_credited_hit_at_another_version_is_a_version_question_not_an_approximate_one`
  - `tests/test_match_states.py::test_a_file_held_under_the_rows_isrc_is_owned_whatever_its_artist_tag_says`
  - `tests/test_match_states.py::test_a_file_with_no_isrc_tag_is_owned_when_the_primary_artist_is_a_credited_member`
  - `tests/test_match_states.py::test_a_files_isrc_tag_is_folded_before_it_is_indexed`
  - `tests/test_match_states.py::test_a_head_in_the_title_tag_reads_as_the_stems_head_does[a-head-found-only-in-the-tag-carries-the-key-when-the-stem-has-none]`
  - `tests/test_match_states.py::test_a_head_in_the_title_tag_reads_as_the_stems_head_does[a-head-inside-the-title-tag-is-stripped-so-a-plain-provider-row-matches]`
  - `tests/test_match_states.py::test_a_head_in_the_title_tag_reads_as_the_stems_head_does[a-head-written-as-a-suffix-inside-the-tag-comes-off-as-it-does-from-the-stem]`
  - `tests/test_match_states.py::test_a_head_in_the_title_tag_reads_as_the_stems_head_does[a-headed-tag-titled-wholly-in-brackets-matches-the-provider-row]`
  - `tests/test_match_states.py::test_a_head_in_the_title_tag_reads_as_the_stems_head_does[a-tag-that-is-only-a-head-falls-to-the-filename-the-way-an-empty-tag-does]`
  - `tests/test_match_states.py::test_a_head_in_the_title_tag_reads_as_the_stems_head_does[a-title-that-genuinely-ends-with-a-camelot-code-and-a-number-loses-that-tail]`
  - `tests/test_match_states.py::test_a_head_in_the_title_tag_reads_as_the_stems_head_does[a-title-that-genuinely-opens-with-a-camelot-code-and-a-number-is-read-as-a-head]`
  - `tests/test_match_states.py::test_a_head_in_the_title_tag_reads_as_the_stems_head_does[the-tempo-goes-with-the-head-and-a-number-opening-the-title-stays]`
  - ... and 18 more, see the JSON sidecar

Old text:

```
    tagged_title = naming.strip_heads(spelled_tag, template=template)
```

New text:

```
    tagged_title = spelled_tag
```

### `r667.G17_reader_drops_isrc`

_read_from_disk: the ISRC tag is read and not carried, so the index has nothing to be asked by

- File: `src/cratekit/acquire/match_library.py`
- Source: `r667.json`, row `G17_reader_drops_isrc`
- Moved: Anchored where u305-replay-after.json replayed it: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 705 against a baseline of 705
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
  - `tests/test_match_states.py::test_an_isrc_hit_asks_about_the_key_alone[another_version_spelling]`
  - `tests/test_match_states.py::test_an_isrc_hit_asks_about_the_key_alone[artist_tag_credits_nobody]`
  - `tests/test_match_states.py::test_an_isrc_hit_on_an_abbreviated_title_is_still_asked_about`
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

### `r667.G4_members_not_folded`

Owned.members: the credited names unfolded, so case and marks decide membership

- File: `src/cratekit/acquire/match_library.py`
- Source: `r667.json`, row `G4_members_not_folded`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 705 against a baseline of 705
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

- File: `src/cratekit/acquire/match_library.py`
- Source: `r667.json`, row `G5_empty_isrc_asks`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 705 against a baseline of 705
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

- File: `src/cratekit/acquire/match_library.py`
- Source: `r667.json`, row `G8_no_credited_rule`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 705 against a baseline of 705
- Kills: 6 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_held_track_is_owned_and_nothing_is_listed[07A - 128 - Traumer, antraum, Anton - Hyaku.flac-tags2-row2]`
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

### `u249.M01_path_alone`

_read_from_disk: answer any remembered path whatever its stamp, the path alone as identity

- File: `src/cratekit/acquire/match_library.py`
- Source: `u249.json`, row `M01_path_alone`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 780 against a baseline of 780
- Kills: 7 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_on_another_device_under_the_same_name_and_stamp_is_read_again`
  - `tests/test_library_reads_remembered.py::test_a_file_rewritten_between_two_jobs_is_read_again_and_the_second_job_matches_its_new_tags`
  - `tests/test_library_reads_remembered.py::test_a_file_swapped_in_under_the_same_name_size_and_times_is_read_again_on_its_inode`
  - `tests/test_library_reads_remembered.py::test_a_file_with_a_new_modification_time_is_read_again`
  - `tests/test_library_reads_remembered.py::test_a_file_with_a_new_size_is_read_again`
  - `tests/test_library_reads_remembered.py::test_a_read_that_is_not_whole_forgets_what_an_earlier_whole_read_left`
  - `tests/test_library_reads_remembered.py::test_a_restore_that_puts_the_old_size_and_time_back_is_read_again_on_its_change_time`

Old text:

```
            and entry.stamp == stamp

```

New text:

```
            and True

```

### `u249.M02_size_out_of_stamp`

_read_from_disk: compare the stamp without its size

- File: `src/cratekit/acquire/match_library.py`
- Source: `u249.json`, row `M02_size_out_of_stamp`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 780 against a baseline of 780
- Kills: 2 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_with_a_new_size_is_read_again`
  - `tests/test_library_reads_remembered.py::test_a_read_that_is_not_whole_forgets_what_an_earlier_whole_read_left`

Old text:

```
            and entry.stamp == stamp

```

New text:

```
            and entry.stamp[1:] == stamp[1:]

```

### `u249.M03_mtime_out_of_stamp`

_read_from_disk: compare the stamp without its modification time

- File: `src/cratekit/acquire/match_library.py`
- Source: `u249.json`, row `M03_mtime_out_of_stamp`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 780 against a baseline of 780
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_with_a_new_modification_time_is_read_again`

Old text:

```
            and entry.stamp == stamp

```

New text:

```
            and entry.stamp[:1] + entry.stamp[2:] == stamp[:1] + stamp[2:]

```

### `u249.M04_ctime_out_of_stamp`

_read_from_disk: compare the stamp without its change time, so a restore tool's old time over new bytes is answered from memory

- File: `src/cratekit/acquire/match_library.py`
- Source: `u249.json`, row `M04_ctime_out_of_stamp`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 780 against a baseline of 780
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_restore_that_puts_the_old_size_and_time_back_is_read_again_on_its_change_time`

Old text:

```
            and entry.stamp == stamp

```

New text:

```
            and entry.stamp[:2] + entry.stamp[3:] == stamp[:2] + stamp[3:]

```

### `u249.M05_inode_out_of_stamp`

_read_from_disk: compare the stamp without its inode

- File: `src/cratekit/acquire/match_library.py`
- Source: `u249.json`, row `M05_inode_out_of_stamp`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 780 against a baseline of 780
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_swapped_in_under_the_same_name_size_and_times_is_read_again_on_its_inode`

Old text:

```
            and entry.stamp == stamp

```

New text:

```
            and entry.stamp[:3] + entry.stamp[4:] == stamp[:3] + stamp[4:]

```

### `u249.M06_device_out_of_stamp`

_read_from_disk: compare the stamp without its device

- File: `src/cratekit/acquire/match_library.py`
- Source: `u249.json`, row `M06_device_out_of_stamp`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 780 against a baseline of 780
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_on_another_device_under_the_same_name_and_stamp_is_read_again`

Old text:

```
            and entry.stamp == stamp

```

New text:

```
            and entry.stamp[:4] == stamp[:4]

```

### `u249.M07_size_not_stat`

_stamp_of: stamp a constant in place of the file's size

- File: `src/cratekit/acquire/match_library.py`
- Source: `u249.json`, row `M07_size_not_stat`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 780 against a baseline of 780
- Kills: 2 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_with_a_new_size_is_read_again`
  - `tests/test_library_reads_remembered.py::test_the_stamp_is_the_files_stat_and_none_for_a_file_that_is_gone`

Old text:

```
    return (seen.st_size, seen.st_mtime_ns, seen.st_ctime_ns, seen.st_ino, seen.st_dev)
```

New text:

```
    return (0, seen.st_mtime_ns, seen.st_ctime_ns, seen.st_ino, seen.st_dev)
```

### `u249.M08_template_out_of_key`

_read_from_disk: key the memory on the path alone, so an entry parsed under one name template answers another

- File: `src/cratekit/acquire/match_library.py`
- Source: `u249.json`, row `M08_template_out_of_key`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 780 against a baseline of 780
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_the_name_template_is_part_of_the_key`

Old text:

```
    key = (path, template)
```

New text:

```
    key = (path, None)
```

### `u249.M09_no_window`

_read_from_disk: answer an equal stamp from memory however recent the file's modification time

- File: `src/cratekit/acquire/match_library.py`
- Source: `u249.json`, row `M09_no_window`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 780 against a baseline of 780
- Kills: 4 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_rewritten_to_the_same_size_inside_the_window_is_read_again`
  - `tests/test_library_reads_remembered.py::test_the_entrys_moment_is_taken_before_the_read`
  - `tests/test_library_reads_remembered.py::test_the_window_is_two_seconds_to_the_nanosecond[1.5s]`
  - `tests/test_library_reads_remembered.py::test_the_window_is_two_seconds_to_the_nanosecond[just-under-2s]`

Old text:

```
            and stamp[1] <= entry.made_ns - REMEMBER_WINDOW_NS

```

New text:

```
            and True

```

### `u249.M10_window_halved`

REMEMBER_WINDOW_NS: one second in place of two, under a FAT volume's step

- File: `src/cratekit/acquire/match_library.py`
- Source: `u249.json`, row `M10_window_halved`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 780 against a baseline of 780
- Kills: 3 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_the_entrys_moment_is_taken_before_the_read`
  - `tests/test_library_reads_remembered.py::test_the_window_is_two_seconds_to_the_nanosecond[1.5s]`
  - `tests/test_library_reads_remembered.py::test_the_window_is_two_seconds_to_the_nanosecond[just-under-2s]`

Old text:

```
REMEMBER_WINDOW_NS = 2_000_000_000
```

New text:

```
REMEMBER_WINDOW_NS = 1_000_000_000
```

### `u249.M11_window_boundary`

_read_from_disk: a file exactly two seconds older than its entry is read again rather than answered

- File: `src/cratekit/acquire/match_library.py`
- Source: `u249.json`, row `M11_window_boundary`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 780 against a baseline of 780
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_the_window_is_two_seconds_to_the_nanosecond[2s]`

Old text:

```
            and stamp[1] <= entry.made_ns - REMEMBER_WINDOW_NS

```

New text:

```
            and stamp[1] < entry.made_ns - REMEMBER_WINDOW_NS

```

### `u249.M12_moment_after_read`

_read_from_disk: take the entry's moment after the read, so a write during the read can be answered from memory

- File: `src/cratekit/acquire/match_library.py`
- Source: `u249.json`, row `M12_moment_after_read`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 780 against a baseline of 780
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_the_entrys_moment_is_taken_before_the_read`

Old text:

```
    owned, whole = _read_fresh(path, template)
    if stamp is not None and whole:
```

New text:

```
    owned, whole = _read_fresh(path, template)
    made_ns = _now_ns()
    if stamp is not None and whole:
```

### `u249.M13_failed_read_remembered`

_read_from_disk: remember a read that failed, so a moment's I/O error on a USB volume answers every later job

- File: `src/cratekit/acquire/match_library.py`
- Source: `u249.json`, row `M13_failed_read_remembered`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 780 against a baseline of 780
- Kills: 3 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_read_that_failed_is_not_remembered`
  - `tests/test_library_reads_remembered.py::test_a_read_that_is_not_whole_forgets_what_an_earlier_whole_read_left`
  - `tests/test_library_reads_remembered.py::test_a_read_that_is_not_whole_is_indexed_as_read_and_not_remembered`

Old text:

```
    if stamp is not None and whole:
```

New text:

```
    if stamp is not None:
```

### `u249.M14_unstated_remembered_never`

_stamp_of: answer None for every file, so nothing is ever remembered and every walk opens every file

- File: `src/cratekit/acquire/match_library.py`
- Source: `u249.json`, row `M14_unstated_remembered_never`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 780 against a baseline of 780
- Kills: 11 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_on_another_device_under_the_same_name_and_stamp_is_read_again`
  - `tests/test_library_reads_remembered.py::test_a_file_rewritten_between_two_jobs_is_read_again_and_the_second_job_matches_its_new_tags`
  - `tests/test_library_reads_remembered.py::test_a_pass_of_three_playlists_opens_each_library_file_once`
  - `tests/test_library_reads_remembered.py::test_a_read_that_is_not_whole_forgets_what_an_earlier_whole_read_left`
  - `tests/test_library_reads_remembered.py::test_a_removed_file_is_absent_a_new_one_is_read_and_a_renamed_one_is_read_under_its_name`
  - `tests/test_library_reads_remembered.py::test_a_reset_forgets_every_file[intake]`
  - `tests/test_library_reads_remembered.py::test_a_reset_forgets_every_file[match]`
  - `tests/test_library_reads_remembered.py::test_an_unchanged_old_file_is_answered_from_memory_on_the_second_index`
  - `tests/test_library_reads_remembered.py::test_the_stamp_is_the_files_stat_and_none_for_a_file_that_is_gone`
  - `tests/test_library_reads_remembered.py::test_the_window_is_two_seconds_to_the_nanosecond[2.5s]`
  - `tests/test_library_reads_remembered.py::test_the_window_is_two_seconds_to_the_nanosecond[2s]`

Old text:

```
    return (seen.st_size, seen.st_mtime_ns, seen.st_ctime_ns, seen.st_ino, seen.st_dev)
```

New text:

```
    return None
```

### `u249.M20_reset_forgets_nothing`

match.reset_cache: forget nothing

- File: `src/cratekit/acquire/match_library.py`
- Source: `u249.json`, row `M20_reset_forgets_nothing`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 780 against a baseline of 780
- Kills: 6 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_that_cannot_be_stated_is_read_as_before_and_never_remembered`
  - `tests/test_library_reads_remembered.py::test_a_read_that_is_not_whole_forgets_what_an_earlier_whole_read_left`
  - `tests/test_library_reads_remembered.py::test_a_read_that_is_not_whole_is_indexed_as_read_and_not_remembered`
  - `tests/test_library_reads_remembered.py::test_a_reset_forgets_every_file[intake]`
  - `tests/test_library_reads_remembered.py::test_a_reset_forgets_every_file[match]`
  - `tests/test_library_reads_remembered.py::test_a_test_starts_with_nothing_remembered`

Old text:

```
    test can clear is a memory that leaks one test's library into the next."""
    _REMEMBERED.clear()
```

New text:

```
    test can clear is a memory that leaks one test's library into the next."""
```

### `u249.M20a_failed_read_keeps_old_entry`

_read_from_disk: keep an earlier whole read's entry when a later read is not whole, so a stamp that comes back brings the old tags back

- File: `src/cratekit/acquire/match_library.py`
- Source: `u249.json`, row `M20a_failed_read_keeps_old_entry`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 780 against a baseline of 780
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_read_that_is_not_whole_forgets_what_an_earlier_whole_read_left`

Old text:

```
    else:
        # A read that was not whole, or a file with no stamp, forgets what an
        # earlier whole read left: the file has been seen changing, and a stamp
        # that came back later must not bring the older answer back with it.
        _REMEMBERED.pop(key, None)
    return owned
```

New text:

```
    return owned
```

### `u265.M6_cache_misaligned`

sorted_recordings: build the sorted names in reverse, so a position the scorer returns names a different recording

- File: `src/cratekit/acquire/match_library.py`
- Source: `u265.json`, row `M6_cache_misaligned`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`
- Collected: 2712 against a baseline of 2712
- Kills: 15 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_rewritten_between_two_jobs_is_read_again_and_the_second_job_matches_its_new_tags`
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[265-5]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[265-None]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[2650-5]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[2650-None]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[26500-5]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[26500-None]`
  - `tests/test_match_states.py::test_the_floor_is_pinned_from_both_sides_by_the_nearest_score_either_way`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`
  - `tests/test_match_states.py::test_the_offer_limit_keeps_the_best_scoring_answers_and_says_what_it_kept_back`

Old text:

```
            cached = (recordings, tuple(_sorted_words(token) for token in recordings))
```

New text:

```
            cached = (recordings, tuple(_sorted_words(token) for token in reversed(recordings)))
```

### `u265.M7_cache_never_kept`

sorted_recordings: never store the sorted names, so every wanted row sorts the whole library again (answers unchanged, cost back to per pair)

- File: `src/cratekit/acquire/match_library.py`
- Source: `u265.json`, row `M7_cache_never_kept`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`
- Collected: 2712 against a baseline of 2712
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_each_name_is_sorted_once_for_the_index_and_each_row_once_a_call`

Old text:

```
            object.__setattr__(self, "_sorted", cached)
```

New text:

```
            pass
```

### `u327.A25_index_reads_title_key_first`

_read_fresh: read the file name's key first again, so the library index offers the old key for a corrected track

- File: `src/cratekit/acquire/match_library.py`
- Source: `u327.json`, row `A25_index_reads_title_key_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 613 against a baseline of 613
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_the_tag_head_outranks_the_stem_head_and_both_outrank_the_initialkey_tag`

Old text:

```
    written_key = tag_head.get("key") or head.get("key")
```

New text:

```
    written_key = head.get("key") or tag_head.get("key")
```

### `r431-b.B1_a_wanted_built_by_hand_asks`

uncredited_spellings no longer requires a spelled title, so a Wanted built from a held file asks for a companion

- File: `src/cratekit/acquire/match_list.py`
- Source: `r431-b.json`, row `B1_a_wanted_built_by_hand_asks`
- Moved: the same text, now in src/cratekit/acquire/match_list.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1193 against a baseline of 1193
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_held_file_crediting_somebody_else_never_calls_the_companion_stale`
  - `tests/test_match_states.py::test_a_wanted_nobody_read_from_a_listing_never_asks_for_a_companion`

Old text:

```
        if not self.spelled or self.several_artists or _credits_in(self.spelled):
```

New text:

```
        if self.several_artists or _credits_in(self.listed):
```

### `r431-b.B2_a_row_billing_a_guest_asks`

uncredited_spellings ignores several_artists, so a row crediting a guest in its artists list asks

- File: `src/cratekit/acquire/match_list.py`
- Source: `r431-b.json`, row `B2_a_row_billing_a_guest_asks`
- Moved: the same text, now in src/cratekit/acquire/match_list.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1193 against a baseline of 1193
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_billed_guest_survives_the_freeze_the_worker_resolves_from`
  - `tests/test_match_states.py::test_a_provider_row_billing_a_guest_in_its_artists_never_asks_for_a_companion`

Old text:

```
        if not self.spelled or self.several_artists or _credits_in(self.spelled):
```

New text:

```
        if not self.spelled or _credits_in(self.spelled):
```

### `r431-b.B3_a_listing_that_spelled_a_credit_asks`

uncredited_spellings ignores a bracketed credit, so a listing crediting Zed reaches Mira's companion

- File: `src/cratekit/acquire/match_list.py`
- Source: `r431-b.json`, row `B3_a_listing_that_spelled_a_credit_asks`
- Moved: the same text, now in src/cratekit/acquire/match_list.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1193 against a baseline of 1193
- Kills: 7 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_rows_suppression_spellings_are_unchanged[Sun Path (Nightwave Remix) (ft Mira)-addresses1]`
  - `tests/test_match_states.py::test_a_credited_rows_suppression_spellings_are_unchanged[Sun Path (feat. Mira) (Nightwave Remix)-addresses0]`
  - `tests/test_match_states.py::test_a_credited_rows_suppression_spellings_are_unchanged[Sun Path (with Mira)-addresses2]`
  - `tests/test_match_states.py::test_a_listing_that_spelled_a_credit_never_asks_for_a_companion[Sun Path (Nightwave Remix) (feat. Zed)]`
  - `tests/test_match_states.py::test_a_listing_that_spelled_a_credit_never_asks_for_a_companion[Sun Path (feat. Zed) (Nightwave Remix)]`
  - `tests/test_match_states.py::test_a_listing_that_spelled_a_credit_never_asks_for_a_companion[Sun Path (with Zed) - Nightwave Remix]`
  - `tests/test_match_states.py::test_a_listing_that_spelled_a_credit_never_asks_for_a_companion[Sun Path [ft. Zed] [Nightwave Remix]]`

Old text:

```
        if not self.spelled or self.several_artists or _credits_in(self.spelled):
```

New text:

```
        if not self.spelled or self.several_artists:
```

### `r431-b.B8_the_reader_never_counts_the_artists`

_from_row stops setting several_artists, so every provider row reads as billing one

- File: `src/cratekit/acquire/match_list.py`
- Source: `r431-b.json`, row `B8_the_reader_never_counts_the_artists`
- Moved: the same text, now in src/cratekit/acquire/match_list.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1193 against a baseline of 1193
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_billed_guest_survives_the_freeze_the_worker_resolves_from`
  - `tests/test_match_states.py::test_a_provider_row_billing_a_guest_in_its_artists_never_asks_for_a_companion`

Old text:

```
        several_artists=_bills_several(row),
```

New text:

```
        several_artists=False,
```

### `u213.M5_listed_names_artist`

listed_names: read no artist off a refused row

- File: `src/cratekit/acquire/match_list.py`
- Source: `u213.json`, row `M5_listed_names_artist`
- Moved: the same text, now in src/cratekit/acquire/match_list.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 726 against a baseline of 726
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_the_readable_listing_sets_aside_a_refused_row_by_id_in_its_place`
  - `tests/test_match_states.py::test_listed_names_reads_a_row_the_reader_refuses`
  - `tests/test_sync_twins.py::test_a_track_listed_with_no_title_is_named_in_its_twin_and_the_rest_are_planned`

Old text:

```
    return str(_field(row, "id", "")).strip(), _artist_of(row), _raw_title(row)
```

New text:

```
    return str(_field(row, "id", "")).strip(), "", _raw_title(row)
```

### `r1305.L1_login_name_on_any_link`

_rejected: read the client's authentication error by name on any link, so a reset met while handling one asks for a login

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1305.json`, row `L1_login_name_on_any_link`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_rejection_bodies.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 207 against a baseline of 207
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_rejection_bodies.py::test_a_login_failure_that_is_no_rejection_is_a_wait[context]`

Old text:

```
        if declared and type(link).__name__ == "AuthenticationError":
            return True
    return False

```

New text:

```
        if type(link).__name__ == "AuthenticationError":
            return True
    return False

```

### `r1305.L2_login_status_declared_only`

_rejected: read a status on the declared chain only, so a login answered 401 or 403 with a page is told to wait

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1305.json`, row `L2_login_status_declared_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_rejection_bodies.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 207 against a baseline of 207
- Kills: 5 (killed)
- Killed:
  - `tests/test_provider_rejection_bodies.py::test_a_login_rejected_whatever_the_body_asks_for_a_login[400-html]`
  - `tests/test_provider_rejection_bodies.py::test_a_login_rejected_whatever_the_body_asks_for_a_login[401-html]`
  - `tests/test_provider_rejection_bodies.py::test_a_login_rejected_whatever_the_body_asks_for_a_login[403-html]`
  - `tests/test_provider_rejection_bodies.py::test_a_login_rejected_with_a_page_tells_the_person_to_log_in_again`
  - `tests/test_provider_rejection_bodies.py::test_a_rejection_whose_body_is_not_json_rewrapped_by_the_client_still_asks_for_a_login`

Old text:

```
        if answered_status(link) in REJECTED_STATUSES:
```

New text:

```
        if declared and answered_status(link) in REJECTED_STATUSES:
```

### `r1305.L3_login_name_dropped`

_rejected: drop the client's authentication error by name, a sample of the guard as it stood before R-1305

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1305.json`, row `L3_login_name_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_rejection_bodies.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 207 against a baseline of 207
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_session_the_provider_rejects_asks_for_a_new_login_not_a_first_one[client-auth-error]`

Old text:

```
        if declared and type(link).__name__ == "AuthenticationError":
            return True
    return False

```

New text:

```
        if False:
            return True
    return False

```

### `r1694.L1_login_no_tolerance`

_login: open the scope with no tolerance, so the login fails as it did before R-1694

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `L1_login_no_tolerance`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`
- Collected: 164 against a baseline of 164
- Kills: 7 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_a_refreshed_login_the_keychain_cannot_take_returns_the_client`
  - `tests/test_provider_session_unstored.py::test_a_verb_whose_login_refreshed_on_the_opt_in_answers_as_before_and_warns`
  - `tests/test_provider_session_unstored.py::test_an_index_that_cannot_be_locked_is_noted_and_the_keychain_is_untouched`
  - `tests/test_provider_session_unstored.py::test_an_index_that_refuses_after_the_keychain_took_the_refresh_is_noted`
  - `tests/test_provider_session_unstored.py::test_the_held_session_is_the_stored_one_so_a_reuse_neither_logs_in_nor_warns_again`
  - `tests/test_provider_session_unstored.py::test_the_warning_is_this_verbs_alone`
  - `tests/test_provider_session_unstored.py::test_two_failed_stores_in_one_verb_make_one_warning_naming_the_class_once`

Old text:

```
    with materialised_session(name, unstored=failed.append) as scope:
```

New text:

```
    with materialised_session(name) as scope:
```

### `r1694.L2_token_file_uncaught`

_login: let a token file the refresh cannot be written to raise, so a full temporary disk fails the login

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `L2_token_file_uncaught`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`
- Collected: 164 against a baseline of 164
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_a_token_file_that_cannot_take_the_refresh_is_noted`

Old text:

```
            except OSError as exc:
                failed.append(exc)
    if failed:
```

New text:

```
            except ArithmeticError as exc:
                failed.append(exc)
    if failed:
```

### `r1694.L3_token_file_catches_defect`

_login: catch every exception at the token file write, so a field the file cannot encode is a warning rather than a defect

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `L3_token_file_catches_defect`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`
- Collected: 164 against a baseline of 164
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_a_login_that_is_no_store_failure_still_raises_on_the_opt_in[a-defect-in-the-capture-still-raises]`

Old text:

```
            except OSError as exc:
                failed.append(exc)
    if failed:
```

New text:

```
            except Exception as exc:
                failed.append(exc)
    if failed:
```

### `r1694.L4_rewrite_unchanged`

_login: rewrite the token file for an unchanged session too, so a file that cannot be written is reported over a session with nothing to store

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `L4_rewrite_unchanged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`
- Collected: 164 against a baseline of 164
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_a_login_that_is_no_store_failure_still_raises_on_the_opt_in[a-defect-in-the-capture-still-raises]`
  - `tests/test_provider_session_unstored.py::test_an_unchanged_session_never_rewrites_the_token_file`

Old text:

```
        if _canonical(refreshed) != _canonical(stored):
```

New text:

```
        if _canonical(refreshed) is not None:
```

### `r1694.L5_hold_the_refresh`

_login: return the refresh as what the keychain holds after a store failure, so every later resolve logs in again and fails to store again

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `L5_hold_the_refresh`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`
- Collected: 164 against a baseline of 164
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_the_held_session_is_the_stored_one_so_a_reuse_neither_logs_in_nor_warns_again`
  - `tests/test_provider_session_unstored.py::test_the_warning_is_this_verbs_alone`

Old text:

```
        return client, stored
    return client, refreshed
```

New text:

```
        return client, refreshed
    return client, refreshed
```

### `r1694.L6_no_note`

_login: note nothing on a store failure, so the verb never says the session was not stored

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `L6_no_note`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`
- Collected: 164 against a baseline of 164
- Kills: 8 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_a_refreshed_login_the_keychain_cannot_take_returns_the_client`
  - `tests/test_provider_session_unstored.py::test_a_token_file_that_cannot_take_the_refresh_is_noted`
  - `tests/test_provider_session_unstored.py::test_a_verb_whose_login_refreshed_on_the_opt_in_answers_as_before_and_warns`
  - `tests/test_provider_session_unstored.py::test_an_index_that_cannot_be_locked_is_noted_and_the_keychain_is_untouched`
  - `tests/test_provider_session_unstored.py::test_an_index_that_refuses_after_the_keychain_took_the_refresh_is_noted`
  - `tests/test_provider_session_unstored.py::test_the_held_session_is_the_stored_one_so_a_reuse_neither_logs_in_nor_warns_again`
  - `tests/test_provider_session_unstored.py::test_the_warning_is_this_verbs_alone`
  - `tests/test_provider_session_unstored.py::test_two_failed_stores_in_one_verb_make_one_warning_naming_the_class_once`

Old text:

```
        _UNSTORED.extend(type(exc).__name__ for exc in failed)
```

New text:

```
        pass
```

### `r1694.L7_note_the_words`

_login: note the failure's words rather than its class, so a credential refusal's setup advice reaches the warning

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `L7_note_the_words`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`
- Collected: 164 against a baseline of 164
- Kills: 7 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_a_refreshed_login_the_keychain_cannot_take_returns_the_client`
  - `tests/test_provider_session_unstored.py::test_a_token_file_that_cannot_take_the_refresh_is_noted`
  - `tests/test_provider_session_unstored.py::test_a_verb_whose_login_refreshed_on_the_opt_in_answers_as_before_and_warns`
  - `tests/test_provider_session_unstored.py::test_an_index_that_cannot_be_locked_is_noted_and_the_keychain_is_untouched`
  - `tests/test_provider_session_unstored.py::test_an_index_that_refuses_after_the_keychain_took_the_refresh_is_noted`
  - `tests/test_provider_session_unstored.py::test_the_held_session_is_the_stored_one_so_a_reuse_neither_logs_in_nor_warns_again`
  - `tests/test_provider_session_unstored.py::test_two_failed_stores_in_one_verb_make_one_warning_naming_the_class_once`

Old text:

```
        _UNSTORED.extend(type(exc).__name__ for exc in failed)
```

New text:

```
        _UNSTORED.extend(str(exc) for exc in failed)
```

### `r1694.S1_tolerance_reraises`

materialised_session: re-raise a store failure handed to the tolerance, so a refreshed login on the opt in fails the verb again

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `S1_tolerance_reraises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_vendored_drive.py`, `tests/test_provider_gate.py`
- Collected: 208 against a baseline of 208
- Kills: 7 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_a_refreshed_login_the_keychain_cannot_take_returns_the_client`
  - `tests/test_provider_session_unstored.py::test_a_verb_whose_login_refreshed_on_the_opt_in_answers_as_before_and_warns`
  - `tests/test_provider_session_unstored.py::test_an_index_that_cannot_be_locked_is_noted_and_the_keychain_is_untouched`
  - `tests/test_provider_session_unstored.py::test_an_index_that_refuses_after_the_keychain_took_the_refresh_is_noted`
  - `tests/test_provider_session_unstored.py::test_the_held_session_is_the_stored_one_so_a_reuse_neither_logs_in_nor_warns_again`
  - `tests/test_provider_session_unstored.py::test_the_warning_is_this_verbs_alone`
  - `tests/test_provider_session_unstored.py::test_two_failed_stores_in_one_verb_make_one_warning_naming_the_class_once`

Old text:

```
            except STORE_FAILURES as exc:
                unstored(exc)

```

New text:

```
            except STORE_FAILURES as exc:
                raise

```

### `r1694.S2_tolerance_always`

materialised_session: tolerate a store failure even when no callback was given, so the drive's own catch and streamrip's scope lose their failure

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `S2_tolerance_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_vendored_drive.py`, `tests/test_provider_gate.py`
- Collected: 208 against a baseline of 208
- Kills: 3 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_a_scope_that_asked_for_no_tolerance_still_raises_its_write_back_failure`
  - `tests/test_vendored_drive.py::test_a_refresh_the_keychain_cannot_take_is_a_warning_on_a_finished_download`
  - `tests/test_vendored_drive.py::test_an_index_that_refuses_after_the_keychain_took_the_session_is_a_warning`

Old text:

```
        if unstored is None:
            write_back(name, path, codec=codec, stored=payload)
        else:

```

New text:

```
        if False:
            write_back(name, path, codec=codec, stored=payload)
        else:
            unstored = unstored or (lambda exc: None)

```

### `r1694.S3_catch_everything`

materialised_session: catch every exception at the write back, so a defect in the write is a warning rather than a raise

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `S3_catch_everything`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_vendored_drive.py`, `tests/test_provider_gate.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_a_defect_in_the_write_back_still_raises`

Old text:

```
            except STORE_FAILURES as exc:
                unstored(exc)

```

New text:

```
            except Exception as exc:
                unstored(exc)

```

### `r1694.S4_failures_no_credential`

STORE_FAILURES: drop the credential errors, so the keychain's own refusal on the opt in fails the login and the drive

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `S4_failures_no_credential`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_vendored_drive.py`, `tests/test_provider_gate.py`
- Collected: 208 against a baseline of 208
- Kills: 8 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_a_refreshed_login_the_keychain_cannot_take_returns_the_client`
  - `tests/test_provider_session_unstored.py::test_a_verb_whose_login_refreshed_on_the_opt_in_answers_as_before_and_warns`
  - `tests/test_provider_session_unstored.py::test_an_index_that_cannot_be_locked_is_noted_and_the_keychain_is_untouched`
  - `tests/test_provider_session_unstored.py::test_the_held_session_is_the_stored_one_so_a_reuse_neither_logs_in_nor_warns_again`
  - `tests/test_provider_session_unstored.py::test_the_warning_is_this_verbs_alone`
  - `tests/test_provider_session_unstored.py::test_two_failed_stores_in_one_verb_make_one_warning_naming_the_class_once`
  - `tests/test_vendored_drive.py::test_a_refresh_the_keychain_cannot_take_is_a_warning_on_a_finished_download`
  - `tests/test_vendored_drive.py::test_a_refresh_the_keychain_cannot_take_leaves_a_park_its_own_cause`

Old text:

```
    secrets.CredentialError,
    CratekitError,
    OSError,
)
```

New text:

```
    CratekitError,
    OSError,
)
```

### `r1694.S5_failures_no_cratekit`

STORE_FAILURES: drop CratekitError, so an index the write could not read fails the login

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `S5_failures_no_cratekit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_vendored_drive.py`, `tests/test_provider_gate.py`
- Collected: 208 against a baseline of 208
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_an_index_that_refuses_after_the_keychain_took_the_refresh_is_noted`
  - `tests/test_vendored_drive.py::test_an_index_that_refuses_after_the_keychain_took_the_session_is_a_warning`

Old text:

```
    secrets.CredentialError,
    CratekitError,
    OSError,
)
```

New text:

```
    secrets.CredentialError,
    OSError,
)
```

### `r705-b.S2_client_session_never_attaches`

the catalogue and account client's transport is not gated, so nothing it does is paced or counted

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r705-b.json`, row `S2_client_session_never_attaches`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 118 against a baseline of 118
- Kills: 16 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_ceiling_stop_a_verb_swallowed_is_still_said`
  - `tests/test_provider_gate.py::test_a_rate_limited_login_comes_out_of_client_session_as_the_park`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[excludes-another-processs-calls]`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[names-rate-limit-answers]`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[reports-its-calls]`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[survives-a-refusal]`
  - `tests/test_provider_gate.py::test_a_verb_at_its_line_is_blocked_and_the_call_past_it_is_not_sent[its-ceiling-names-the-exact-command-that-continues]`
  - `tests/test_provider_gate.py::test_a_verb_at_its_line_is_blocked_and_the_call_past_it_is_not_sent[the-hours-line-U278]`
  - `tests/test_provider_gate.py::test_calls_on_the_command_line_lets_one_run_pass_and_the_next_is_back_at_the_ceiling`
  - `tests/test_provider_gate.py::test_client_session_attaches_the_gate_before_the_login_goes_out`
  - `tests/test_provider_gate.py::test_client_session_with_no_gate_still_paces_at_the_defaults`
  - `tests/test_provider_gate.py::test_each_opener_paces_with_the_frozen_configuration[account]`
  - `tests/test_provider_gate.py::test_each_opener_paces_with_the_frozen_configuration[catalogue]`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_calls_already_given[joined]`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_calls_already_given[spaced]`
  - ... and 1 more, see the JSON sidecar

Old text:

```
        client = CLIENT_FACTORY()
        gate.attach(client)

```

New text:

```
        client = CLIENT_FACTORY()

```

### `u261.H1_reuse_skips_the_gate`

session_for: reuse the held session without asking the gate, so a verb started inside a cooldown gets a client

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `H1_reuse_skips_the_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_catalogue_app.py`
- Collected: 213 against a baseline of 213
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_reuse_inside_a_cooldown_refuses_without_a_call`

Old text:

```
        current.gate.assert_open()
        try:
            stored = secrets.get_json(name)
```

New text:

```
        try:
            stored = secrets.get_json(name)
```

### `u261.H2_reuse_ignores_a_replaced_session`

session_for: reuse the held client whatever the keychain now holds, so a session replaced or refreshed elsewhere is never picked up

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `H2_reuse_ignores_a_replaced_session`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`, `tests/test_catalogue_app.py`
- Collected: 208 against a baseline of 208
- Kills: 4 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_to_a_client_no_longer_held_keeps_the_newer_one`
  - `tests/test_provider_session_hold.py::test_a_replaced_session_the_provider_rejects_leaves_no_seam_the_old_client`
  - `tests/test_provider_session_hold.py::test_a_session_replaced_after_an_open_is_logged_in_afresh_from_the_new_value`
  - `tests/test_provider_session_hold.py::test_an_old_clients_refusal_on_the_account_keeps_the_session_logged_in_since`

Old text:

```
        if _canonical(stored) == current.blob:
```

New text:

```
        if True:
```

### `u261.H3_reuse_swallows_a_missing_session`

session_for: answer a keychain that no longer holds the session with the held client, so a withdrawn session is reused

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `H3_reuse_swallows_a_missing_session`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`
- Collected: 142 against a baseline of 142
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_keychain_that_cannot_be_read_on_a_reuse_says_repair_it`
  - `tests/test_provider_session_hold.py::test_a_session_gone_from_the_keychain_after_an_open_is_refused_not_reused`

Old text:

```
            drop(current)
            raise _to_auth_failure(exc) from exc
```

New text:

```
            return current
```

### `u261.H4_failed_read_keeps_the_hold`

session_for: refuse a keychain that cannot be read on a reuse but keep the hold, so the account's held adapter goes on over it

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `H4_failed_read_keeps_the_hold`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`
- Collected: 142 against a baseline of 142
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_session_gone_from_the_keychain_after_an_open_is_refused_not_reused`

Old text:

```
            drop(current)
            raise _to_auth_failure(exc) from exc
```

New text:

```
            raise _to_auth_failure(exc) from exc
```

### `u261.H5_settings_not_in_the_key`

session_for: reuse a session opened under other gate settings, so a job's frozen interval and cooldown are not the ones its calls run under

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `H5_settings_not_in_the_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`
- Collected: 147 against a baseline of 147
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_other_gate_settings_open_a_session_of_their_own`

Old text:

```
    if current is not None and current.name == str(name) and current.settings == settings:
```

New text:

```
    if current is not None and current.name == str(name):
```

### `u261.H6_app_not_asked_again`

session_for: hand a reuse the held absence of an app client, so app values recorded or lost since the open are not seen and no lost value is noted

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `H6_app_not_asked_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_catalogue_app.py`
- Collected: 95 against a baseline of 95
- Kills: 3 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_open_account_and_open_catalogue_hand_the_app_client_on`
  - `tests/test_provider_session_hold.py::test_a_lost_app_value_is_noted_on_every_resolve_that_falls_back`
  - `tests/test_provider_session_hold.py::test_an_app_recorded_after_the_open_is_picked_up_by_the_next_resolve`

Old text:

```
            if current.app is None:
```

New text:

```
            if False:
```

### `u261.H7_nothing_held`

session_for: hold nothing after a login, so every opener logs in again as before the unit

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `H7_nothing_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`, `tests/test_catalogue_app.py`
- Collected: 208 against a baseline of 208
- Kills: 11 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_401_on_the_account_drops_the_shared_client_and_the_catalogue_logs_in_again`
  - `tests/test_provider_session_hold.py::test_a_process_resolving_both_seams_validates_the_session_once`
  - `tests/test_provider_session_hold.py::test_a_refreshed_login_is_reused_while_the_keychain_holds_the_refresh`
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_through_the_shared_client_drops_it_for_both_seams[401]`
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_through_the_shared_client_drops_it_for_both_seams[403]`
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_to_a_client_no_longer_held_keeps_the_newer_one`
  - `tests/test_provider_session_hold.py::test_a_replaced_session_the_provider_rejects_leaves_no_seam_the_old_client`
  - `tests/test_provider_session_hold.py::test_a_session_the_index_no_longer_records_is_refused_by_both_seams`
  - `tests/test_provider_session_hold.py::test_an_answer_that_judges_no_session_keeps_the_client`
  - `tests/test_provider_session_hold.py::test_an_old_clients_refusal_on_the_account_keeps_the_session_logged_in_since`
  - `tests/test_provider_session_hold.py::test_the_app_client_is_held_with_the_session_and_asks_one_token`

Old text:

```
    _watch(opened)
    _HELD = opened
    return opened
```

New text:

```
    _watch(opened)
    return opened
```

### `u261.H8_blob_is_the_stored_not_the_refresh`

_login: report the session read rather than the refresh written back, so a refreshed login reads as replaced on every reuse and logs in again

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `H8_blob_is_the_stored_not_the_refresh`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`
- Collected: 29 against a baseline of 29
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_refreshed_login_is_reused_while_the_keychain_holds_the_refresh`

Old text:

```
    return client, refreshed
```

New text:

```
    return client, stored
```

### `u261.H9_no_forget_before_a_new_login`

session_for: keep the old hold while a replaced session is logged in afresh, so a login that fails leaves the account's adapter over the replaced session

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `H9_no_forget_before_a_new_login`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`
- Collected: 142 against a baseline of 142
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_replaced_session_the_provider_rejects_leaves_no_seam_the_old_client`

Old text:

```
    forget()
    gate = provider_gate.Gate(settings)
```

New text:

```
    gate = provider_gate.Gate(settings)
```

### `u261.R1_watch_not_installed`

session_for: install no watch on the shared client, so a 401 or 403 the catalogue meets leaves the refused client held

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `R1_watch_not_installed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`, `tests/test_catalogue_app.py`
- Collected: 208 against a baseline of 208
- Kills: 3 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_through_the_shared_client_drops_it_for_both_seams[401]`
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_through_the_shared_client_drops_it_for_both_seams[403]`
  - `tests/test_provider_session_hold.py::test_a_refusal_the_transport_raises_drops_the_client_too`

Old text:

```
    _watch(opened)
    _HELD = opened
```

New text:

```
    _HELD = opened
```

### `u261.R2_answered_refusal_ignored`

_watch: ignore a 401 or 403 the transport answers, so a refused client stays held

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `R2_answered_refusal_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`, `tests/test_catalogue_app.py`
- Collected: 208 against a baseline of 208
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_through_the_shared_client_drops_it_for_both_seams[401]`
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_through_the_shared_client_drops_it_for_both_seams[403]`

Old text:

```
        if getattr(response, "status_code", None) in SESSION_REFUSED_STATUSES:
            drop(session)
```

New text:

```
        if False:
            drop(session)
```

### `u261.R3_raised_refusal_ignored`

_watch: ignore a 401 or 403 the transport raises, so a refusal that arrives as an exception leaves the client held

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `R3_raised_refusal_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`
- Collected: 142 against a baseline of 142
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_refusal_the_transport_raises_drops_the_client_too`

Old text:

```
            if answered_status(exc) in SESSION_REFUSED_STATUSES:
```

New text:

```
            if False:
```

### `u261.R4_forbidden_not_a_refusal`

SESSION_REFUSED_STATUSES: read only 401 as judging the session, so a 403 neither drops the shared client nor forgets the account

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `R4_forbidden_not_a_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_rejection_bodies.py`
- Collected: 175 against a baseline of 175
- Kills: 4 (killed)
- Killed:
  - `tests/test_provider_rejection_bodies.py::test_a_session_rejected_mid_sweep_asks_for_a_login_whatever_the_body[403-empty]`
  - `tests/test_provider_rejection_bodies.py::test_a_session_rejected_mid_sweep_asks_for_a_login_whatever_the_body[403-html]`
  - `tests/test_provider_rejection_bodies.py::test_a_session_rejected_mid_sweep_asks_for_a_login_whatever_the_body[403-json]`
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_through_the_shared_client_drops_it_for_both_seams[403]`

Old text:

```
SESSION_REFUSED_STATUSES = frozenset({401, 403})
```

New text:

```
SESSION_REFUSED_STATUSES = frozenset({401})
```

### `u261.R5_drop_not_by_identity`

drop: drop whatever is held, so a stale client's refusal throws away the newer session logged in since

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `R5_drop_not_by_identity`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`
- Collected: 29 against a baseline of 29
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_to_a_client_no_longer_held_keeps_the_newer_one`
  - `tests/test_provider_session_hold.py::test_an_old_clients_refusal_on_the_account_keeps_the_session_logged_in_since`

Old text:

```
    if _HELD is session:
        _HELD = None
```

New text:

```
    if True:
        _HELD = None
```

### `u261.W1_unchanged_skip_removed`

write_back: drop the unchanged comparison, so every login writes the value already stored back to the keychain

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `W1_unchanged_skip_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_adapter_contract.py`, `tests/test_outbound_tidal_account.py`, `tests/test_catalogue_app.py`, `tests/test_provider_gate.py`
- Collected: 483 against a baseline of 483
- Kills: 4 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_process_resolving_both_seams_validates_the_session_once`
  - `tests/test_provider_session_hold.py::test_an_unchanged_session_makes_no_keychain_write`
  - `tests/test_provider_session_hold.py::test_an_unchanged_toml_session_is_not_written_back`
  - `tests/test_provider_session_hold.py::test_write_back_compares_the_value_and_not_the_spelling`

Old text:

```
        if unchanged is not None and unchanged == _canonical(stored):
            return False
```

New text:

```
        if False:
            return False
```

### `u261.W2_changed_session_skipped`

write_back: read any encodable session as unchanged, so a refreshed token is never stored (the merge blocker the card names)

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `W2_changed_session_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_adapter_contract.py`, `tests/test_outbound_tidal_account.py`, `tests/test_catalogue_app.py`, `tests/test_provider_gate.py`
- Collected: 483 against a baseline of 483
- Kills: 5 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_refreshed_session_goes_back_to_the_keychain`
  - `tests/test_provider_session_hold.py::test_a_refreshed_login_is_reused_while_the_keychain_holds_the_refresh`
  - `tests/test_provider_session_hold.py::test_a_refreshed_session_is_written_once_through_the_index`
  - `tests/test_provider_session_hold.py::test_a_session_the_tool_changed_is_written_back_from_the_scope`
  - `tests/test_provider_session_hold.py::test_write_back_compares_the_value_and_not_the_spelling`

Old text:

```
        if unchanged is not None and unchanged == _canonical(stored):
```

New text:

```
        if unchanged is not None:
```

### `u261.W3_compare_by_value_not_bytes`

write_back: compare the dicts by Python equality rather than the bytes set_json stores, so a value that changed type (an int expiry for a float) is not written

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `W3_compare_by_value_not_bytes`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_adapter_contract.py`
- Collected: 186 against a baseline of 186
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_write_back_compares_the_value_and_not_the_spelling`

Old text:

```
        unchanged = _canonical(refreshed)
        if unchanged is not None and unchanged == _canonical(stored):
```

New text:

```
        unchanged = refreshed
        if unchanged == stored:
```

### `u274.P4_sweep_live`

sweep_orphans: drop the process check, so every directory of the form is removed, a live drive's token included

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u274.json`, row `P4_sweep_live`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 449 against a baseline of 449
- Kills: 5 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_other_gate_settings_open_a_session_of_their_own`
  - `tests/test_vendored_drive.py::test_a_drive_killed_outright_leaves_a_directory_the_next_one_sweeps`
  - `tests/test_vendored_drive.py::test_a_process_id_no_process_can_have_is_left_and_does_not_raise`
  - `tests/test_vendored_drive.py::test_the_sweep_leaves_a_directory_whose_process_it_cannot_see`
  - `tests/test_vendored_drive.py::test_the_sweep_leaves_alone_what_it_cannot_prove_is_an_orphan[own-process]`

Old text:

```
        if owned is None or not _gone(int(owned.group(1))):

```

New text:

```
        if owned is None:

```

### `u62.S1_device_flow_login`

Log in as a device flow session rather than PKCE

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u62.json`, row `S1_device_flow_login`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/test_adapter_contract.py`
- Collected: 331 against a baseline of 331
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_recorded_session_resolves_the_adapter_over_a_pkce_login`

Old text:

```
                is_pkce=True,
```

New text:

```
                is_pkce=False,
```

### `u62.S2_401_not_rejected`

Drop 401 from the statuses read as a rejected session

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u62.json`, row `S2_401_not_rejected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/test_adapter_contract.py`
- Collected: 331 against a baseline of 331
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_session_the_provider_rejects_asks_for_a_new_login_not_a_first_one[401]`
  - `tests/test_label_tidal_catalogue.py::test_a_session_the_provider_rejects_asks_for_a_new_login_not_a_first_one[chained-401]`

Old text:

```
REJECTED_STATUSES = frozenset({400, 401, 403})
```

New text:

```
REJECTED_STATUSES = frozenset({400, 403})
```

### `u62.S4_every_failure_rejected`

Read every login failure as a rejected session, the pre review behaviour

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u62.json`, row `S4_every_failure_rejected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/test_adapter_contract.py`
- Collected: 331 against a baseline of 331
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_provider_that_cannot_be_reached_is_a_wait_not_a_new_login[connection]`
  - `tests/test_label_tidal_catalogue.py::test_a_provider_that_cannot_be_reached_is_a_wait_not_a_new_login[server-error]`
  - `tests/test_label_tidal_catalogue.py::test_a_provider_that_cannot_be_reached_is_a_wait_not_a_new_login[timeout]`
  - `tests/test_label_tidal_catalogue.py::test_a_provider_that_cannot_be_reached_is_a_wait_not_a_new_login[unparseable-page]`

Old text:

```
            if _rejected(exc):
```

New text:

```
            if True:
```

### `u62.S5_blob_without_token_logged_in`

Hand a blob with no access token to the provider

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u62.json`, row `S5_blob_without_token_logged_in`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/test_adapter_contract.py`
- Collected: 331 against a baseline of 331
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_stored_blob_with_no_access_token_never_reaches_the_provider`

Old text:

```
        if not isinstance(stored, dict) or not stored.get("access_token"):
```

New text:

```
        if not isinstance(stored, dict):
```

### `u62.S6_refresh_not_written_back`

Write the stored blob back unchanged instead of the refreshed tokens

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u62.json`, row `S6_refresh_not_written_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/test_adapter_contract.py`
- Collected: 331 against a baseline of 331
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_refresh_during_login_is_written_back_to_the_keychain`

Old text:

```
            if value is not None:
                refreshed[field] = _epoch(value)
```

New text:

```
            if value is not None and False:
                refreshed[field] = _epoch(value)
```

### `u62.S7_naive_expiry_as_local`

Read the client's naive expiry as local time

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u62.json`, row `S7_naive_expiry_as_local`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/test_adapter_contract.py`
- Collected: 23214 against a baseline of 23214
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if value.tzinfo is None:
```

New text:

```
        if value.tzinfo is None and False:
```

### `r703-a.V6_sample_no_park_check`

Sample of an existing guard: fetch no longer asks the gate for a park it raised inside the tool (R-705)

- File: `src/cratekit/acquire/vendored.py`
- Source: `r703-a.json`, row `V6_sample_no_park_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_provider_gate.py`
- Collected: 275 against a baseline of 275
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_held_lock_the_tool_swallowed_during_a_download_comes_out_of_fetch`
  - `tests/test_provider_gate.py::test_a_trip_the_tool_swallowed_during_a_download_comes_out_of_fetch_as_the_park`

Old text:

```
        self._gate.raise_if_parked()
        # THE SWALLOWED ERROR
```

New text:

```
        # THE SWALLOWED ERROR
```

### `r705-b.S3_vendored_never_asks_before_login`

a download started inside the cooldown builds the tool and logs in

- File: `src/cratekit/acquire/vendored.py`
- Source: `r705-b.json`, row `S3_vendored_never_asks_before_login`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 118 against a baseline of 118
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_the_vendored_adapter_refuses_inside_the_cooldown_before_touching_the_tool`

Old text:

```
        self._gate.assert_open()
        if self._session is not None:

```

New text:

```
        if self._session is not None:

```

### `r705-b.S4_vendored_never_attaches_to_the_tool`

the tool's own session is not gated, so its login and every download lookup go out unpaced

- File: `src/cratekit/acquire/vendored.py`
- Source: `r705-b.json`, row `S4_vendored_never_attaches_to_the_tool`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 118 against a baseline of 118
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_rate_limited_login_comes_out_of_the_vendored_adapter_as_the_park`

Old text:

```
        self._gate.attach(tidal.session)

```

New text:

```
        pass

```

### `r705-b.S5_vendored_never_asks_after_login`

a park the tool swallowed inside its login reads as a rejected session

- File: `src/cratekit/acquire/vendored.py`
- Source: `r705-b.json`, row `S5_vendored_never_asks_after_login`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 118 against a baseline of 118
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_rate_limited_login_comes_out_of_the_vendored_adapter_as_the_park`

Old text:

```
        self._gate.raise_if_parked()
        if not authorised:

```

New text:

```
        if not authorised:

```

### `u254.M07_always_append`

mark_applied: append even to a torn, absent or schema 1 ledger

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M07_always_append`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 743 against a baseline of 743
- Kills: 86 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_file_put_in_place_with_the_same_size_and_time_is_read_again`
  - `tests/test_adopt_apply_journal_u254.py::test_a_file_rewritten_in_place_at_the_same_size_is_read_again`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[1]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[2]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[3]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[4]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_ledger_damaged_since_this_process_left_it_refuses_the_next_mark`
  - `tests/test_adopt_apply_journal_u254.py::test_a_mark_does_not_parse_the_ledger_it_appends_to`
  - `tests/test_adopt_apply_journal_u254.py::test_a_mark_on_a_ledger_written_before_u254_keeps_every_record`
  - `tests/test_adopt_apply_journal_u254.py::test_a_re_mark_replaces_the_earlier_record_as_the_document_did`
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_another_process_appended_is_kept`
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_the_reader_would_refuse_is_never_written[actor]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_the_reader_would_refuse_is_never_written[content_id]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_the_reader_would_refuse_is_never_written[entry_id]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_the_reader_would_refuse_is_never_written[tree]`
  - ... and 71 more, see the JSON sidecar

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

### `r239-b.S10_adopt_apply_key_off`

adopt apply's write open passes unlock=False

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `r239-b.json`, row `S10_adopt_apply_key_off`
- Moved: the write open's arguments were joined onto one line by the formatter; the mutation adds unlock=False to it as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_adopt_apply_cli.py`
- Collected: 724 against a baseline of 724
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_no_caller_in_src_answers_the_key_question_for_itself`

Old text:

```
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
```

New text:

```
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, unlock=False, cfg=cfg)
```

### `r797-c.G1_the_threshold_is_fifty`

FOLDER_WORTH: 51, a realistic nearby value, so a genre at 50 is not named

- File: `src/cratekit/adopt/genres.py`
- Source: `r797-c.json`, row `G1_the_threshold_is_fifty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_report_genres.py`
- Collected: 33 against a baseline of 33
- Kills: 7 (killed)
- Killed:
  - `tests/test_report_genres.py::test_a_genre_at_49_is_counted_and_not_named_and_one_at_50_is_named`
  - `tests/test_report_genres.py::test_a_genre_filed_whole_in_its_sub_names_no_other_spelling`
  - `tests/test_report_genres.py::test_a_style_sub_nothing_routes_a_lowercase_spelling_to_is_still_its_genre`
  - `tests/test_report_genres.py::test_ae8_the_verb_names_the_genre_with_its_count_and_the_library_is_unchanged`
  - `tests/test_report_genres.py::test_another_spelling_of_a_source_string_is_counted_with_its_sub`
  - `tests/test_report_genres.py::test_the_summary_a_person_reads_in_help_states_the_threshold_the_code_uses`
  - `tests/test_report_genres.py::test_with_nothing_at_the_threshold_the_report_says_so_in_a_row`

Old text:

```
FOLDER_WORTH = 50
```

New text:

```
FOLDER_WORTH = 51
```

### `r797-c.G2_at_the_threshold_is_named`

named: over the threshold and not at it

- File: `src/cratekit/adopt/genres.py`
- Source: `r797-c.json`, row `G2_at_the_threshold_is_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_report_genres.py`
- Collected: 33 against a baseline of 33
- Kills: 4 (killed)
- Killed:
  - `tests/test_report_genres.py::test_a_genre_at_49_is_counted_and_not_named_and_one_at_50_is_named`
  - `tests/test_report_genres.py::test_a_genre_filed_whole_in_its_sub_names_no_other_spelling`
  - `tests/test_report_genres.py::test_a_style_sub_nothing_routes_a_lowercase_spelling_to_is_still_its_genre`
  - `tests/test_report_genres.py::test_another_spelling_of_a_source_string_is_counted_with_its_sub`

Old text:

```
genre.tracks >= self.threshold
```

New text:

```
genre.tracks > self.threshold
```

### `r797-c.G3_a_removed_row_is_not_counted`

count: count a row rekordbox marked removed, so a folder is suggested for what a person deleted

- File: `src/cratekit/adopt/genres.py`
- Source: `r797-c.json`, row `G3_a_removed_row_is_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_report_genres.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_report_genres.py::test_a_removed_row_is_not_counted`

Old text:

```
        if row.deleted:
            continue

```

New text:

```
(empty)
```

### `r797-c.G4_no_genre_is_not_a_genre`

count: resolve an empty genre like any other, so the tagging backlog is counted as a genre or as having a folder

- File: `src/cratekit/adopt/genres.py`
- Source: `r797-c.json`, row `G4_no_genre_is_not_a_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_report_genres.py`
- Collected: 33 against a baseline of 33
- Kills: 3 (killed)
- Killed:
  - `tests/test_report_genres.py::test_ae8_the_verb_names_the_genre_with_its_count_and_the_library_is_unchanged`
  - `tests/test_report_genres.py::test_every_live_track_is_counted_exactly_once`
  - `tests/test_report_genres.py::test_tracks_with_no_genre_are_counted_apart_and_never_named`

Old text:

```
        if not value:
```

New text:

```
        if False:
```

### `r797-c.G5_another_spelling_is_the_same_genre`

count: stop folding another spelling of a style sub's name onto the sub, the review's 45 and 10

- File: `src/cratekit/adopt/genres.py`
- Source: `r797-c.json`, row `G5_another_spelling_is_the_same_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_report_genres.py`
- Collected: 33 against a baseline of 33
- Kills: 3 (killed)
- Killed:
  - `tests/test_report_genres.py::test_a_style_sub_nothing_routes_a_lowercase_spelling_to_is_still_its_genre`
  - `tests/test_report_genres.py::test_another_spelling_of_a_source_string_is_counted_with_its_sub`
  - `tests/test_report_genres.py::test_another_spelling_of_a_style_subs_own_name_is_counted_with_it`

Old text:

```
        elif value.casefold() in style_subs:
```

New text:

```
        elif False:
```

### `u343.M01_finalize_no_mark`

_finalize: drop the mark from the write, so a measured file reads as unmeasured and every resume measures it again

- File: `src/cratekit/analysis/cli.py`
- Source: `u343.json`, row `M01_finalize_no_mark`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_analysis.py`, `tests/test_vocals_cli.py`, `tests/test_restamp_scored_by.py`, `tests/test_analysis_ahead.py`
- Collected: 536 against a baseline of 536
- Kills: 9 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_pooled_run_leaves_exactly_what_the_serial_run_leaves`
  - `tests/test_analysis_workers.py::test_a_file_beside_its_headed_twin_is_measured_where_it_is_and_named_nothing`
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - `tests/test_analysis_workers.py::test_an_analyze_job_runs_pending_to_done_and_the_files_carry_the_result`
  - `tests/test_analysis_workers.py::test_an_interrupt_after_an_items_report_is_staged_resumes_by_the_printed_command`
  - `tests/test_analysis_workers.py::test_an_item_written_before_its_row_moved_resumes_by_its_mark_and_is_measured_once`
  - `tests/test_analysis_workers.py::test_an_uncalibrated_library_writes_no_energy_tag_and_routes_to_the_sink`
  - `tests/test_restamp_scored_by.py::test_a_resumed_tail_restamps_every_file_since_its_run_scored_none`
  - `tests/test_restamp_scored_by.py::test_the_tail_over_the_real_verbs_leaves_every_title_headless_for_the_landing`

Old text:

```
        run.MARK_FIELD: run.MARK_VALUE,
    }
```

New text:

```
    }
```

### `u343.M02_finalize_writes_a_key`

_finalize: write a detector's camelot as initialkey, the key the run no longer measures

- File: `src/cratekit/analysis/cli.py`
- Source: `u343.json`, row `M02_finalize_writes_a_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_restamp_scored_by.py`, `tests/test_analysis_ahead.py`
- Collected: 482 against a baseline of 482
- Kills: 6 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_detector_shaped_like_the_batch_fakes_is_accepted`
  - `tests/test_analysis_workers.py::test_an_analyze_job_runs_pending_to_done_and_the_files_carry_the_result`
  - `tests/test_analysis_workers.py::test_the_run_titles_only_a_file_with_no_title_and_never_with_a_head[a-title-kept]`
  - `tests/test_analysis_workers.py::test_the_run_titles_only_a_file_with_no_title_and_never_with_a_head[untitled-lossy-marked-first]`
  - `tests/test_analysis_workers.py::test_the_run_titles_only_a_file_with_no_title_and_never_with_a_head[untitled-the-stem]`
  - `tests/test_restamp_scored_by.py::test_the_tail_over_the_real_verbs_leaves_every_title_headless_for_the_landing`

Old text:

```
        "drift": scored.get("drift_verdict"),
        run.MARK_FIELD: run.MARK_VALUE,
```

New text:

```
        "drift": scored.get("drift_verdict"),
        "initialkey": scored.get("camelot"),
        run.MARK_FIELD: run.MARK_VALUE,
```

