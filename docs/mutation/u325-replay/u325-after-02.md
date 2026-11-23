# Mutation table: u325-after-02

Measured by `scripts/mutate.py` on 2026-11-22 17:24 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 36.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 16:29 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 3, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u286.M14_filter_after_cap` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 4 | killed |
| `u286.M15_cap_removed` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 6 | killed |
| `u286.M16_cap_off_by_one` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 6 | killed |
| `u286.M17_cap_counts_files` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 3 | killed |
| `u286.M18_resolver_back_to_base` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 51 | killed |
| `u286.M19_limit_ignored` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 9 | killed |
| `u286.M1_title_floor_up_one` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 3 | killed |
| `u286.M2_title_floor_down_one` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 1 | killed |
| `u286.M3_title_floor_to_sixty` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 3 | killed |
| `u286.M4_plain_ratio` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 6 | killed |
| `u286.M6_unreadable_title_not_asked` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 15 | killed |
| `u286.S1_discovery_floor_up_one` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 10 | killed |
| `u286.S2_offer_not_truncated` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 4 | killed |
| `r1709.M10_title_identity_no_separator` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 1 | killed |
| `r1709.M11_recording_identity_is_the_token` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 24 | killed |
| `r1709.M12_held_exact_unfiltered` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 14 | killed |
| `r1709.M13_held_credited_by_fold` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 9 | killed |
| `r1709.M14_isrc_settled_by_fold` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 2 | killed |
| `r1709.M15_same_recording_title_guard` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 3 | killed |
| `r1709.M16_candidates_grouped_by_token` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 5 | killed |
| `r1709.M17_question_identity_token` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 3 | killed |
| `r1709.M18_match_id_token` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 3 | killed |
| `r1709.M19_search_option_token` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 1 | killed |
| `r1709.M1_bare_no_nfkc` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 2 | killed |
| `r1709.M20_current_option_no_title` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 2 | killed |
| `r686.E2_routed_counts_vocal` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 9 | killed |
| `r686.E4_long_tracks_intake_only` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 2 | killed |
| `r686.E5_warnings_dropped` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 4 | killed |
| `r686.E6_gaps_dropped` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `r686.E7_subs_not_named` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `r688.B1_owed_rating_blocks_the_answer` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `r688.C1_rates_flag_ignored` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 5 | killed |

## Row definitions

### `u286.M14_filter_after_cap`

_resembling asks discovery for the best five only and filters those, so unrelated titles outscoring a real near match push it out and the row downloads

- File: `src/cratekit/acquire/match.py`
- Source: `u286.json`, row `M14_filter_after_cap`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
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
- Collected: 3906 against a baseline of 3906
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
- Collected: 3906 against a baseline of 3906
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
- Collected: 3906 against a baseline of 3906
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
- Collected: 3906 against a baseline of 3906
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
- Collected: 3906 against a baseline of 3906
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
- Collected: 3906 against a baseline of 3906
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
- Collected: 3906 against a baseline of 3906
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
- Collected: 3906 against a baseline of 3906
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
- Collected: 3906 against a baseline of 3906
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
- Collected: 3906 against a baseline of 3906
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
- Collected: 3906 against a baseline of 3906
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
- Collected: 3906 against a baseline of 3906
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

### `r1709.M10_title_identity_no_separator`

title_identity returns the bare text with no separator, so it can equal another title's fold

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M10_title_identity_no_separator`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
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

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M11_recording_identity_is_the_token`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
- Kills: 24 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_two_emoji_titles_by_one_artist_played_back_to_back_stay_two_rows`
  - `tests/intake/test_workers.py::test_two_recognised_emoji_titles_by_one_artist_are_two_items`
  - `tests/test_intake_missing_search.py::test_a_search_answered_by_another_emoji_title_is_not_exact`
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

### `r1709.M12_held_exact_unfiltered`

LibraryIndex.held keeps every file under the token, so a held fire emoji owns a wanted drop

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M12_held_exact_unfiltered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
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

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M13_held_credited_by_fold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
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

### `r1709.M14_isrc_settled_by_fold`

the ISRC branch settles a file under another emoji title by the fold

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M14_isrc_settled_by_fold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
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
- Collected: 3983 against a baseline of 3983
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_approximate_hit_is_a_question_and_never_a_match`
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
- Collected: 3983 against a baseline of 3983
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

### `r1709.M17_question_identity_token`

the review item hashes the token, so a held emoji row retires another's question and one answer settles both

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M17_question_identity_token`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
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

### `r1709.M18_match_id_token`

match_id hashes the token, so intake missing drops a second emoji row as a line listed twice

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M18_match_id_token`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
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
- Collected: 3983 against a baseline of 3983
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

### `r1709.M1_bare_no_nfkc`

bare_title composes with NFC rather than NFKC, so a title of fullwidth marks or an ellipsis is a different title and a real duplicate is offered rather than owned

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M1_bare_no_nfkc`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
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

### `r1709.M20_current_option_no_title`

current_option carries a former identifier without its title, so an answer about a fire emoji answers for a snow emoji held in its place

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M20_current_option_no_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
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

### `r686.E2_routed_counts_vocal`

routed is counted off the vocal column instead of the destination

- File: `src/cratekit/write/routing_cli.py`
- Source: `r686.json`, row `E2_routed_counts_vocal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 9 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_database_gate_prints_the_destination_in_the_default_mode`
  - `tests/test_routing_workers.py::test_the_database_inbox_gate_shows_a_genre_sub_beside_the_band_and_files_both`
  - `tests/test_routing_workers.py::test_the_database_inbox_gate_shows_each_files_destination`
  - `tests/test_routing_workers.py::test_the_export_gate_names_the_vocal_dimension_it_did_not_read`
  - `tests/test_routing_workers.py::test_the_export_gate_prints_the_plan_in_the_default_mode`
  - `tests/test_routing_workers.py::test_the_export_gate_says_why_an_intake_track_goes_nowhere`
  - `tests/test_routing_workers.py::test_the_export_gate_shows_a_genre_sub_beside_the_band_and_files_both`
  - `tests/test_routing_workers.py::test_the_export_gate_shows_every_item_the_digest_was_taken_over`
  - `tests/test_routing_workers.py::test_the_gate_counts_tracks_filed_into_a_genre_sub`

Old text:

```
        "routed": sum(1 for item in tracks if item["destination"]),

```

New text:

```
        "routed": sum(1 for item in tracks if item["vocal"]),

```

### `r686.E4_long_tracks_intake_only`

long tracks counts only the first track's membership

- File: `src/cratekit/write/routing_cli.py`
- Source: `r686.json`, row `E4_long_tracks_intake_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_export_gate_prints_the_plan_in_the_default_mode`
  - `tests/test_routing_workers.py::test_the_export_gate_shows_every_item_the_digest_was_taken_over`

Old text:

```
        "long tracks": sum(1 for item in tracks if item["long_track"]),

```

New text:

```
        "long tracks": sum(1 for item in tracks[:1] if item["long_track"]),

```

### `r686.E5_warnings_dropped`

The planner's warnings stay off the screen

- File: `src/cratekit/write/routing_cli.py`
- Source: `r686.json`, row `E5_warnings_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 4 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_export_gate_prints_the_plan_in_the_default_mode`
  - `tests/test_routing_workers.py::test_the_export_gate_says_why_an_intake_track_goes_nowhere`
  - `tests/test_routing_workers.py::test_the_export_gate_shows_every_item_the_digest_was_taken_over`
  - `tests/test_routing_workers.py::test_the_offered_plan_names_no_rating_and_says_which_are_owed`

Old text:

```
        "warnings": [warning["message"] for warning in warnings],

```

New text:

```
        "warnings": [],

```

### `r686.E6_gaps_dropped`

The dimensions not derived stay off the screen

- File: `src/cratekit/write/routing_cli.py`
- Source: `r686.json`, row `E6_gaps_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_export_gate_names_the_vocal_dimension_it_did_not_read`

Old text:

```
        "not derived": list(gaps),

```

New text:

```
        "not derived": [],

```

### `r686.E7_subs_not_named`

The created vocal subs are left off the screen

- File: `src/cratekit/write/routing_cli.py`
- Source: `r686.json`, row `E7_subs_not_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_export_gate_shows_every_item_the_digest_was_taken_over`

Old text:

```
        "vocal subs created": list(vox_created),

```

New text:

```
        "vocal subs created": [],

```

### `r688.B1_owed_rating_blocks_the_answer`

an owed rating turns a run with nothing to route into route-blocked, which no run of this medium can ever clear

- File: `src/cratekit/write/routing_cli.py`
- Source: `r688.json`, row `B1_owed_rating_blocks_the_answer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_second_run_still_owing_ratings_is_nothing_to_route`

Old text:

```
        reason = "nothing-to-route"
    warnings += unrated

```

New text:

```
        reason = "nothing-to-route"
    warnings += unrated
    if unrated and reason == "nothing-to-route":
        reason = "route-blocked"

```

### `r688.C1_rates_flag_ignored`

a bucket declared rates = false is counted as owed a rating

- File: `src/cratekit/write/routing_cli.py`
- Source: `r688.json`, row `C1_rates_flag_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 5 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_declined_run_still_says_which_ratings_are_owed`
  - `tests/test_routing_workers.py::test_a_track_in_a_bucket_that_does_not_rate_is_filed_and_not_owed`
  - `tests/test_routing_workers.py::test_an_owed_star_rating_is_not_written_into_the_export`
  - `tests/test_routing_workers.py::test_the_offered_plan_names_no_rating_and_says_which_are_owed`
  - `tests/test_routing_workers.py::test_two_rows_naming_one_file_are_both_counted_as_owed`

Old text:

```
        if not routing.rates(declared, placement.bucket):
            continue

```

New text:

```
        pass

```

