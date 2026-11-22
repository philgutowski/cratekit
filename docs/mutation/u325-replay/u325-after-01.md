# Mutation table: u325-after-01

Measured by `scripts/mutate.py` on 2026-11-22 16:29 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 39.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 16:29 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 2, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r1705.M10_holds_always` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 4 | killed |
| `r1705.M11_holds_reads_artist` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 38 | killed |
| `r1705.M12_lookup_ignores_wanted_side` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 28 | killed |
| `r1705.M13_lookup_ignores_held_side` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 25 | killed |
| `r1705.M14_lookup_key_drops_artist` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 6 | killed |
| `r1705.M15_lookup_key_spells_artist` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 1 | killed |
| `r1705.M16_lookup_removed` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 38 | killed |
| `r1705.M17_lookup_repeats_the_five` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 4 | killed |
| `r1705.M18_lookup_skips_every_scored` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 4 | killed |
| `r1705.M19_lookup_after_the_scored` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 6 | killed |
| `r1705.M1_luv_unlisted` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 15 | killed |
| `r1705.M20_lookup_counts_in_the_five` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 38 | killed |
| `r1705.M2_four_numeral_unlisted` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 14 | killed |
| `r1705.M3_too_unlisted` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 3 | killed |
| `r1705.M4_2nite_unlisted` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 2 | killed |
| `r1705.M5_spelled_test_removed` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 5 | killed |
| `r1705.M6_spelled_test_a_ratio` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 12 | killed |
| `r1705.M7_spelled_replaces_written` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 2 | killed |
| `r1705.M8_spelled_keeps_spaces` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 7 | killed |
| `r1705.M9_spelled_spells_nothing` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 52 | killed |
| `r1705.S1_discovery_floor_raised` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 28 | killed |
| `r1705.S2_unreadable_title_dropped` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 15 | killed |
| `u286.M10_swap_either_half` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 4 | killed |
| `u286.M11_swap_removed` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 8 | killed |
| `u286.M12_swap_second_half_artist` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 8 | killed |
| `u286.M13_filter_removed` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 20 | killed |
| `u132.W5_rebuild_note` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 1 | killed |
| `u53-routing-and-rebuild-workers.I3_rebuild_items_dropped` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 21 | killed |
| `u53-routing-and-rebuild-workers.R2_rebuild_drives_a_foreign_job` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 1 | killed |
| `u53-routing-and-rebuild-workers.R4_rebuild_drives_an_itemless_job` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 1 | killed |
| `u53-zero-rows-remeasured.I6_tree_items_ignores_native` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 1 | killed |
| `u53-zero-rows-remeasured.I7_tree_items_ignores_the_named_tree` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 1 | killed |
| `u89.W4_rebuild_worker` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 4 | killed |
| `u89.W6_rebuild_resume_loads_first` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 3 | killed |
| `r316.M3_inbox_gaps_leak_into_totals` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `r686.E1_tracks_counts_every_item` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |

## Row definitions

### `r1705.M10_holds_always`

_holds_spelling answers yes for every title, so the lookup offers OK against O.K., U286's split class, where the score did not

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M10_holds_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
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

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M11_holds_reads_artist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
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

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M12_lookup_ignores_wanted_side`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
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

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M13_lookup_ignores_held_side`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
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

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M14_lookup_key_drops_artist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
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

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M15_lookup_key_spells_artist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
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

### `r1705.M16_lookup_removed`

_resembling never reads the lookup, so a pair the discovery score misses (Prince, 4 U against For You) reads missing and downloads

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M16_lookup_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
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
- Collected: 3906 against a baseline of 3906
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
- Collected: 3906 against a baseline of 3906
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
- Collected: 3906 against a baseline of 3906
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

### `r1705.M1_luv_unlisted`

_SPELLED_OUT loses luv, so Luv U against a held Love You reads missing and downloads

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M1_luv_unlisted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
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

### `r1705.M20_lookup_counts_in_the_five`

the lookup's hits are cut to the five with the scored ones, round one's shape, so a scored recording is pushed out with nothing withheld

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M20_lookup_counts_in_the_five`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
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

### `r1705.M2_four_numeral_unlisted`

_SPELLED_OUT loses 4, so 4 U against a held For You reads missing and downloads

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M2_four_numeral_unlisted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
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

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M3_too_unlisted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
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

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M4_2nite_unlisted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
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

### `r1705.M5_spelled_test_removed`

_agree loses the spelled out equality, so a scored slang pair (Monkey Safari, Luv U against Love You) is dropped by the title test

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M5_spelled_test_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
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
- Collected: 3906 against a baseline of 3906
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
- Collected: 3906 against a baseline of 3906
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

### `r1705.M8_spelled_keeps_spaces`

_spelled_out joins the words with a space, so 2 Nite against Tonight is no longer one string

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M8_spelled_keeps_spaces`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
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

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M9_spelled_spells_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
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

### `r1705.S1_discovery_floor_raised`

SAMPLED existing guard: APPROXIMATE_FLOOR raised from 82 to 90, so fewer near hits are discovered

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `S1_discovery_floor_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
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
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Alex Kaminski-Mana-Nebula]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Hot Since 82-Wow-Wild]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Monkey Safari-Joy-Goodbye]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Paul Deep (AR)-Rea-Tique]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Traumer-Get Out-Agenou]`
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
    if not asked or not found:
        return False

```

### `u286.M10_swap_either_half`

the swap allowance takes either crossed half rather than both, so an unrelated title by an artist sharing one word is offered

- File: `src/cratekit/acquire/match.py`
- Source: `u286.json`, row `M10_swap_either_half`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
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
- Collected: 3906 against a baseline of 3906
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
- Collected: 3906 against a baseline of 3906
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
- Collected: 3906 against a baseline of 3906
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

### `u132.W5_rebuild_note`

The rebuild resume carries no skipped step note

- File: `src/cratekit/cli/rebuild.py`
- Source: `u132.json`, row `W5_rebuild_note`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_driven_resume_over_no_favorites_class_names_the_skipped_step[rebuild]`

Old text:

```
            *engine.favorites_skipped_warnings(declared, driven),

```

New text:

```
(empty)
```

### `u53-routing-and-rebuild-workers.I3_rebuild_items_dropped`

The rebuild files a job with no items, the state every rebuild was in before this unit

- File: `src/cratekit/cli/rebuild.py`
- Source: `u53-routing-and-rebuild-workers.json`, row `I3_rebuild_items_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 21 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[above-rebuild]`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[below-rebuild]`
  - `tests/test_routing_workers.py::test_a_corrupt_calibration_refuses_the_resume_before_any_item_runs[rebuild]`
  - `tests/test_routing_workers.py::test_a_driven_rebuild_over_an_absent_music_directory_fails_the_item`
  - `tests/test_routing_workers.py::test_a_driven_rebuild_watches_the_grids_where_they_actually_live`
  - `tests/test_routing_workers.py::test_a_driven_rebuild_whose_root_the_database_lacks_fails_the_item`
  - `tests/test_routing_workers.py::test_a_driven_rebuild_without_an_acknowledgment_refuses_through_the_real_gates`
  - `tests/test_routing_workers.py::test_a_driven_resume_over_no_favorites_class_names_the_skipped_step[rebuild]`
  - `tests/test_routing_workers.py::test_a_driven_resume_over_the_declared_class_says_nothing_of_it[rebuild]`
  - `tests/test_routing_workers.py::test_a_driven_resume_says_the_vocal_dimension_was_not_compared_beside_drift[rebuild]`
  - `tests/test_routing_workers.py::test_a_queued_rebuild_and_resort_run_on_an_encrypted_library[rebuild]`
  - `tests/test_routing_workers.py::test_a_queued_rebuild_runs_its_item_and_the_tree_holds_the_track`
  - `tests/test_routing_workers.py::test_a_rebuild_of_another_tree_says_nothing_of_the_routing_trees_favorites[rebuild]`
  - `tests/test_routing_workers.py::test_a_rebuild_of_one_named_tree_queues_that_tree_alone`
  - `tests/test_routing_workers.py::test_a_resume_reads_no_registry_of_its_own`
  - ... and 6 more, see the JSON sidecar

Old text:

```
            payload={"tree": tree_id, "actor": actor},
            item_ids=items,
```

New text:

```
            payload={"tree": tree_id, "actor": actor},
```

### `u53-routing-and-rebuild-workers.R2_rebuild_drives_a_foreign_job`

The rebuild drives another verb's job, without that verb's own resume checks

- File: `src/cratekit/cli/rebuild.py`
- Source: `u53-routing-and-rebuild-workers.json`, row `R2_rebuild_drives_a_foreign_job`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_neither_resume_drives_another_verbs_job[rebuild]`

Old text:

```
    if job.handler_key != ctx.entry.handler_key:
        raise refuse(
            "job-unknown",
```

New text:

```
    if False:
        raise refuse(
            "job-unknown",
```

### `u53-routing-and-rebuild-workers.R4_rebuild_drives_an_itemless_job`

A rebuild queued by an older build drives to succeeded having rebuilt nothing

- File: `src/cratekit/cli/rebuild.py`
- Source: `u53-routing-and-rebuild-workers.json`, row `R4_rebuild_drives_an_itemless_job`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_neither_resume_drives_a_job_an_older_build_queued_with_no_items[rebuild]`

Old text:

```
        if not jobs.items(store, job.job_id):
            raise refuse(
                "internal-error",
```

New text:

```
        if False:
            raise refuse(
                "internal-error",
```

### `u53-zero-rows-remeasured.I6_tree_items_ignores_native`

The rebuild's items include trees the registry says are still on the bridge

- File: `src/cratekit/cli/rebuild.py`
- Source: `u53-zero-rows-remeasured.json`, row `I6_tree_items_ignores_native`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_neither_queued_verb_takes_an_item_for_a_tree_still_on_the_bridge[rebuild]`

Old text:

```
    native = tuple(sorted(t for t in entries.tree_ids() if entries.is_database_native(t)))
```

New text:

```
    native = tuple(sorted(entries.tree_ids()))
```

### `u53-zero-rows-remeasured.I7_tree_items_ignores_the_named_tree`

A rebuild of one named tree quietly rebuilds every tree in the library

- File: `src/cratekit/cli/rebuild.py`
- Source: `u53-zero-rows-remeasured.json`, row `I7_tree_items_ignores_the_named_tree`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_rebuild_of_one_named_tree_queues_that_tree_alone`

Old text:

```
    if tree_id is None:
        return native
    return tuple(t for t in native if t == tree_id)
```

New text:

```
    return native
```

### `u89.W4_rebuild_worker`

cli/rebuild handle: hand the engine None instead of the loaded cut

- File: `src/cratekit/cli/rebuild.py`
- Source: `u89.json`, row `W4_rebuild_worker`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 4 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[above-rebuild]`
  - `tests/test_routing_workers.py::test_a_worker_driven_without_the_resume_refuses_a_corrupt_calibration`
  - `tests/test_routing_workers.py::test_converge_compares_the_vocal_sub_once_calibrated`
  - `tests/test_routing_workers.py::test_each_worker_names_its_own_verb_and_rebuilds_the_item_it_was_handed`

Old text:

```
        vocal_threshold=metadata_cli.load_vocal_threshold(cfg),
```

New text:

```
        vocal_threshold=None,
```

### `u89.W6_rebuild_resume_loads_first`

cli/rebuild _resume: do not read the cut before driving, so a corrupt calibration fails items instead of refusing

- File: `src/cratekit/cli/rebuild.py`
- Source: `u89.json`, row `W6_rebuild_resume_loads_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 3 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_corrupt_calibration_refuses_the_resume_before_any_item_runs[rebuild]`
  - `tests/test_routing_workers.py::test_a_driven_resume_says_the_vocal_dimension_was_not_compared_beside_drift[rebuild]`
  - `tests/test_routing_workers.py::test_a_resume_that_drove_nothing_carries_no_vocal_warning[rebuild]`

Old text:

```
        threshold = metadata_cli.load_vocal_threshold(jobs.frozen_config(job))
```

New text:

```
        threshold = 0.0
```

### `r316.M3_inbox_gaps_leak_into_totals`

route_inbox reads the gaps without taking them out of the result, so they ride in the plan totals

- File: `src/cratekit/write/routing_cli.py`
- Source: `r316.json`, row `M3_inbox_gaps_leak_into_totals`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_over_the_shipped_taxonomy_says_the_vocal_dimension_was_not_compared`

Old text:

```
    not_compared = result.pop("not_compared", ())
```

New text:

```
    not_compared = result.get("not_compared", ())
```

### `r686.E1_tracks_counts_every_item`

tracks counts created playlists as tracks

- File: `src/cratekit/write/routing_cli.py`
- Source: `r686.json`, row `E1_tracks_counts_every_item`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_export_gate_shows_every_item_the_digest_was_taken_over`

Old text:

```
        "tracks": len(tracks),

```

New text:

```
        "tracks": len(items),

```

