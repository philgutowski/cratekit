# Mutation table: u325-after-03

Measured by `scripts/mutate.py` on 2026-11-22 18:17 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 48.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 16:29 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 4, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r1709.M21_current_option_never_carries` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 3 | killed |
| `r1709.M3_bare_keeps_spaces` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 1 | killed |
| `r1709.M4_bare_keeps_invisible` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 5 | killed |
| `r1709.M5_no_variation_selectors` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 3 | killed |
| `r1709.M6_no_format_characters` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 2 | killed |
| `r1709.M7_tag_characters_dropped` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 1 | killed |
| `r1709.M8_bare_for_every_title` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 1 | killed |
| `r1709.M9_title_identity_is_the_fold` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 30 | killed |
| `r1709.M23_intake_exact_by_token` | `src/cratekit/intake/candidates.py` | user | 29 file(s) | 3983 | 2 | killed |
| `r1709.M22_adjudicate_not_carried` | `src/cratekit/acquire/match_cli.py` | user | 29 file(s) | 3983 | 1 | killed |
| `r1709.M2_adjudicate_offered_not_carried` | `src/cratekit/acquire/match_cli.py` | user | 29 file(s) | 3983 | 1 | killed |
| `u138-rerun.S5_bound_exclusive` | `src/cratekit/core/session.py` | user | 43 file(s) | 4220 | 1 | killed |
| `u138.E1_terminal_check` | `src/cratekit/core/session.py` | user | 43 file(s) | 4220 | 4 | killed |
| `u138.S10_older_record_reads_as_session` | `src/cratekit/core/session.py` | maintainer | 43 file(s) | 4220 | 1 | killed |
| `u138.S11_rule_not_written` | `src/cratekit/core/session.py` | user | 43 file(s) | 4220 | 4 | killed |
| `u138.S12_message_names_the_portion` | `src/cratekit/core/session.py` | user | 43 file(s) | 4220 | 4 | killed |
| `u138.S13_remedy_points_back_at_ack` | `src/cratekit/core/session.py` | user | 43 file(s) | 4220 | 8 | killed |
| `u138.S1_session_rule_gone` | `src/cratekit/core/session.py` | user | 43 file(s) | 4220 | 20 | killed |
| `u138.S2_any_answer_gets_the_age_rule` | `src/cratekit/core/session.py` | user | 43 file(s) | 4220 | 13 | killed |
| `u138.S3_stale_not_refused` | `src/cratekit/core/session.py` | user | 43 file(s) | 4220 | 10 | killed |
| `u138.S6_bound_six_days` | `src/cratekit/core/session.py` | user | 43 file(s) | 4220 | 5 | killed |
| `u138.S8_rule_not_recorded` | `src/cratekit/core/session.py` | user | 43 file(s) | 4220 | 6 | killed |
| `u138.S9_answer_not_recorded` | `src/cratekit/core/session.py` | user | 43 file(s) | 4220 | 4 | killed |
| `r688.C2_no_energy_counted` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 5 | killed |
| `r688.C3_files_not_rows` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `r688.G1_zero_owed_still_warns` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 9 | killed |
| `r688.G2_count_off_by_one` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 7 | killed |
| `r688.N1_long_track_change_not_a_write` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `r688.U1_hand_rated_counted` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 4 | killed |
| `r688.U2_missing_attribute_counted` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 8 | killed |
| `r688.U3_empty_rating_not_unrated` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 3 | killed |
| `r688.V1_applied_envelope_drops_warning` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 6 | killed |
| `r688.V2_gate_drops_warning` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 3 | killed |
| `r688.V3_declined_envelope_drops_warning` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `r688.W1_rating_written_again` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 5 | killed |
| `r691.F1_routed_counts_vocal` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 9 | killed |
| `r691.F2_trees_left_off` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 2 | killed |
| `r691.F3_planner_warnings_dropped_from_facts` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 2 | killed |
| `r691.F4_gaps_dropped_from_facts` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `r691.K1_empty_folder_plan_names_no_tree` | `src/cratekit/write/routing_cli.py` | maintainer | 1 file(s) | 197 | 1 | killed |
| `r691.K2_gaps_not_carried_to_the_apply` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 2 | killed |
| `r691.N3_declined_envelope_drops_the_warning` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 2 | killed |
| `r924.A4_split_on_one_part` | `src/cratekit/intake/acrcloud.py` | user | 1 file(s) | 11 | 1 | killed |

## Row definitions

### `r1709.M21_current_option_never_carries`

current_option never carries, so every answer recorded before about an emoji file reads as a candidate gone

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M21_current_option_never_carries`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
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

### `r1709.M3_bare_keeps_spaces`

bare_title keeps spacing, so ? ? and ?? are two titles and a real duplicate is not owned

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M3_bare_keeps_spaces`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
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

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M4_bare_keeps_invisible`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_search_answered_by_the_same_emoji_title_is_exact`
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

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M5_no_variation_selectors`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_search_answered_by_the_same_emoji_title_is_exact`
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

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M6_no_format_characters`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
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

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M7_tag_characters_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
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

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M8_bare_for_every_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
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

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M9_title_identity_is_the_fold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
- Kills: 30 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_two_emoji_titles_by_one_artist_played_back_to_back_stay_two_rows`
  - `tests/intake/test_workers.py::test_two_recognised_emoji_titles_by_one_artist_are_two_items`
  - `tests/test_acquire_fallback.py::test_an_upload_question_about_one_emoji_title_is_not_another_ones`
  - `tests/test_intake_missing_search.py::test_a_search_answered_by_another_emoji_title_is_not_exact`
  - `tests/test_intake_missing_search.py::test_a_search_question_about_one_emoji_title_is_not_another_ones`
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

### `r1709.M23_intake_exact_by_token`

intake's exact flag compares the token, so a search for a drop answered by a fire is listed and downloaded

- File: `src/cratekit/intake/candidates.py`
- Source: `r1709.json`, row `M23_intake_exact_by_token`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_search_answered_by_the_same_emoji_title_is_exact`
  - `tests/test_intake_missing_search.py::test_two_emoji_rows_are_each_searched_and_listed`

Old text:

```
    return frozenset((one.distinct, one.version_key) for one in wanted.readings)

```

New text:

```
    return frozenset((one.recording, one.version_key) for one in wanted.readings)

```

### `r1709.M22_adjudicate_not_carried`

adjudicate passes the stored option unchanged, so an answer recorded before about an emoji file reads as a candidate gone

- File: `src/cratekit/acquire/match_cli.py`
- Source: `r1709.json`, row `M22_adjudicate_not_carried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
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
- Collected: 3983 against a baseline of 3983
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

### `u138-rerun.S5_bound_exclusive`

A portion exactly five days old is under the bound

- File: `src/cratekit/core/session.py`
- Source: `u138-rerun.json`, row `S5_bound_exclusive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4220 against a baseline of 4220
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_the_bound_is_strict_at_exactly_five_days[exactly-five-days]`

Old text:

```
        elif entry.age_seconds >= limit:

```

New text:

```
        elif entry.age_seconds > limit:

```

### `u138.E1_terminal_check`

Existing guard sample: the terminal check on a person's answer

- File: `src/cratekit/core/session.py`
- Source: `u138.json`, row `E1_terminal_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4220 against a baseline of 4220
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_a_person_without_a_terminal_is_still_refused_over_fresh_backups`
  - `tests/test_session_cli.py::test_the_answering_invocation_refuses_when_nobody_is_there`
  - `tests/test_write_session.py::test_an_agent_shaped_invocation_cannot_mint_the_acknowledgment`
  - `tests/test_write_session.py::test_the_terminal_probe_the_mint_uses_by_default_is_the_real_one`

Old text:

```
        if not probe():

```

New text:

```
        if False:

```

### `u138.S10_older_record_reads_as_session`

A record from before U138 reads as minted by the session's rule

- File: `src/cratekit/core/session.py`
- Source: `u138.json`, row `S10_older_record_reads_as_session`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4220 against a baseline of 4220
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_a_record_written_before_u138_reads_as_the_terminal_rule`

Old text:

```
            rule=str(data.get("rule") or RULE_TERMINAL),

```

New text:

```
            rule=str(data.get("rule") or RULE_SESSION_AGES),

```

### `u138.S11_rule_not_written`

The record's rule key is not written to the file

- File: `src/cratekit/core/session.py`
- Source: `u138.json`, row `S11_rule_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4220 against a baseline of 4220
- Kills: 4 (killed)
- Killed:
  - `tests/test_doctor.py::test_doctor_shows_the_acknowledgments_expiry_beside_the_two_backup_ages`
  - `tests/test_session_ack_by_session.py::test_an_unreadable_acknowledgment_is_replaced_by_one_command`
  - `tests/test_session_ack_by_session.py::test_one_command_mints_as_the_session_when_both_ages_are_four_days`
  - `tests/test_session_ack_by_session.py::test_the_session_mints_with_no_terminal_when_both_ages_are_under_five_days`

Old text:

```
            "rule": self.rule,

```

New text:

```
(empty)
```

### `u138.S12_message_names_the_portion`

Reword the refusal so it no longer names the portion's age

- File: `src/cratekit/core/session.py`
- Source: `u138.json`, row `S12_message_names_the_portion`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4220 against a baseline of 4220
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[files-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-exactly-five]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[files-six-days]`

Old text:

```
                f"the {entry.portion} portion is {entry.age_seconds / 86400:.1f} days old"

```

New text:

```
                f"a backup portion is too old ({entry.portion})"

```

### `u138.S13_remedy_points_back_at_ack`

The too old refusal tells a person to acknowledge again rather than to run a backup

- File: `src/cratekit/core/session.py`
- Source: `u138.json`, row `S13_remedy_points_back_at_ack`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4220 against a baseline of 4220
- Kills: 8 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[both-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[files-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-exactly-five]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-never-recorded]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-recorded-in-the-future]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[files-six-days]`

Old text:

```
                remedy=Remedy.RUN_BACKUP,

```

New text:

```
                remedy=Remedy.ACKNOWLEDGE_BACKUP,

```

### `u138.S1_session_rule_gone`

A session's answer falls to the terminal check, as before U138

- File: `src/cratekit/core/session.py`
- Source: `u138.json`, row `S1_session_rule_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4220 against a baseline of 4220
- Kills: 20 (killed)
- Killed:
  - `tests/test_doctor.py::test_doctor_names_when_an_acknowledgment_lapsed`
  - `tests/test_doctor.py::test_doctor_shows_the_acknowledgments_expiry_beside_the_two_backup_ages`
  - `tests/test_doctor.py::test_no_acknowledgment_is_claimed_absent_off_a_volume_nobody_read`
  - `tests/test_session_ack_by_session.py::test_a_session_with_a_terminal_is_still_held_to_the_ages`
  - `tests/test_session_ack_by_session.py::test_an_expired_acknowledgment_is_replaced_by_one_command`
  - `tests/test_session_ack_by_session.py::test_an_unreadable_acknowledgment_is_replaced_by_one_command`
  - `tests/test_session_ack_by_session.py::test_one_command_mints_as_the_session_when_both_ages_are_four_days`
  - `tests/test_session_ack_by_session.py::test_one_command_prints_the_expiry_a_person_reads`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[both-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[files-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_reports_a_valid_acknowledgment_and_does_not_mint_again`
  - `tests/test_session_ack_by_session.py::test_the_bound_is_strict_at_exactly_five_days[a-second-under-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_bound_is_strict_at_exactly_five_days[exactly-five-days]`
  - ... and 5 more, see the JSON sidecar

Old text:

```
    if decided_by == SESSION_ACTOR:

```

New text:

```
    if False:

```

### `u138.S2_any_answer_gets_the_age_rule`

Any recorded answer, a person's included, mints without a terminal on young backups

- File: `src/cratekit/core/session.py`
- Source: `u138.json`, row `S2_any_answer_gets_the_age_rule`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4220 against a baseline of 4220
- Kills: 13 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[session.ack]`
  - `tests/test_session_ack_by_session.py::test_a_person_at_a_terminal_mints_by_the_terminal_rule_and_the_record_says_so`
  - `tests/test_session_ack_by_session.py::test_a_person_without_a_terminal_is_still_refused_over_fresh_backups`
  - `tests/test_session_ack_by_session.py::test_a_valid_acknowledgment_a_person_minted_is_reported_over_old_backups`
  - `tests/test_session_cli.py::test_a_damaged_acknowledgment_record_can_still_be_replaced`
  - `tests/test_session_cli.py::test_a_hard_killed_gated_write_blocks_cutover_until_release_abandons_it`
  - `tests/test_session_cli.py::test_a_power_loss_blocks_cutover_until_release_abandons_it`
  - `tests/test_session_cli.py::test_a_second_mint_replaces_the_record_and_moves_the_window`
  - `tests/test_session_cli.py::test_a_spent_acknowledgment_decision_cannot_be_replayed`
  - `tests/test_session_cli.py::test_the_answering_invocation_refuses_when_nobody_is_there`
  - `tests/test_session_cli.py::test_the_check_rows_a_person_reads_name_the_portion`
  - `tests/test_session_cli.py::test_the_cli_mints_an_acknowledgment_a_real_destructive_verb_then_spends`
  - `tests/test_session_cli.py::test_the_refusal_names_the_acknowledgment_on_record_in_all_three_states`

Old text:

```
    if decided_by == SESSION_ACTOR:

```

New text:

```
    if decided_by is not None:

```

### `u138.S3_stale_not_refused`

The session mints over a portion five days old or of unknown age

- File: `src/cratekit/core/session.py`
- Source: `u138.json`, row `S3_stale_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4220 against a baseline of 4220
- Kills: 10 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_a_session_with_a_terminal_is_still_held_to_the_ages`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[both-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[files-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_bound_is_strict_at_exactly_five_days[exactly-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-exactly-five]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-never-recorded]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-recorded-in-the-future]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[files-six-days]`

Old text:

```
        if stale:

```

New text:

```
        if False:

```

### `u138.S6_bound_six_days`

The bound is six days rather than five

- File: `src/cratekit/core/session.py`
- Source: `u138.json`, row `S6_bound_six_days`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4220 against a baseline of 4220
- Kills: 5 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[files-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_bound_is_five_days_as_the_author_set_it`
  - `tests/test_session_ack_by_session.py::test_the_bound_is_strict_at_exactly_five_days[exactly-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-exactly-five]`

Old text:

```
SESSION_MAX_BACKUP_AGE = timedelta(days=5)

```

New text:

```
SESSION_MAX_BACKUP_AGE = timedelta(days=6)

```

### `u138.S8_rule_not_recorded`

The record always says the terminal rule minted it

- File: `src/cratekit/core/session.py`
- Source: `u138.json`, row `S8_rule_not_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4220 against a baseline of 4220
- Kills: 6 (killed)
- Killed:
  - `tests/test_doctor.py::test_doctor_shows_the_acknowledgments_expiry_beside_the_two_backup_ages`
  - `tests/test_session_ack_by_session.py::test_an_unreadable_acknowledgment_is_replaced_by_one_command`
  - `tests/test_session_ack_by_session.py::test_one_command_mints_as_the_session_when_both_ages_are_four_days`
  - `tests/test_session_ack_by_session.py::test_one_command_prints_the_expiry_a_person_reads`
  - `tests/test_session_ack_by_session.py::test_the_bound_is_strict_at_exactly_five_days[a-second-under-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_session_mints_with_no_terminal_when_both_ages_are_under_five_days`

Old text:

```
        shown=shown,
        rule=rule,

```

New text:

```
        shown=shown,
        rule=RULE_TERMINAL,

```

### `u138.S9_answer_not_recorded`

The record never says who answered the gate

- File: `src/cratekit/core/session.py`
- Source: `u138.json`, row `S9_answer_not_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4220 against a baseline of 4220
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_a_person_at_a_terminal_mints_by_the_terminal_rule_and_the_record_says_so`
  - `tests/test_session_ack_by_session.py::test_one_command_mints_as_the_session_when_both_ages_are_four_days`
  - `tests/test_session_ack_by_session.py::test_the_bound_is_strict_at_exactly_five_days[a-second-under-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_session_mints_with_no_terminal_when_both_ages_are_under_five_days`

Old text:

```
        rule=rule,
        decided_by=decided_by,

```

New text:

```
        rule=rule,
        decided_by=None,

```

### `r688.C2_no_energy_counted`

a track with no energy reading is counted as owed a rating it has no value for

- File: `src/cratekit/write/routing_cli.py`
- Source: `r688.json`, row `C2_no_energy_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 5 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_declined_run_still_says_which_ratings_are_owed`
  - `tests/test_routing_workers.py::test_a_track_with_no_energy_reading_is_filed_and_not_owed`
  - `tests/test_routing_workers.py::test_an_owed_star_rating_is_not_written_into_the_export`
  - `tests/test_routing_workers.py::test_the_offered_plan_names_no_rating_and_says_which_are_owed`
  - `tests/test_routing_workers.py::test_two_rows_naming_one_file_are_both_counted_as_owed`

Old text:

```
        if routing.energy_rating(declared, energy.get(placement.location)) is None:

```

New text:

```
        if routing.energy_rating(declared, energy.get(placement.location)) == -1:

```

### `r688.C3_files_not_rows`

two rows naming one file are counted as one owed rating, though rekordbox rates each row

- File: `src/cratekit/write/routing_cli.py`
- Source: `r688.json`, row `C3_files_not_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_two_rows_naming_one_file_are_both_counted_as_owed`

Old text:

```
        owed += sum(1 for key in files[placement.location] if _unrated(by_id[key]))

```

New text:

```
        owed += 1 if any(_unrated(by_id[key]) for key in files[placement.location]) else 0

```

### `r688.G1_zero_owed_still_warns`

a run that owes no rating still carries the owed rating warning, so every export run warns

- File: `src/cratekit/write/routing_cli.py`
- Source: `r688.json`, row `G1_zero_owed_still_warns`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 9 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_hand_rated_export_track_is_not_owed_a_rating`
  - `tests/test_routing_workers.py::test_a_row_with_no_rating_attribute_is_not_counted_as_owed`
  - `tests/test_routing_workers.py::test_a_second_run_over_its_own_output_adds_nothing`
  - `tests/test_routing_workers.py::test_a_track_in_a_bucket_that_does_not_rate_is_filed_and_not_owed`
  - `tests/test_routing_workers.py::test_a_track_with_no_energy_reading_is_filed_and_not_owed`
  - `tests/test_routing_workers.py::test_an_export_location_under_a_retired_volume_name_resolves_through_the_prefix_map`
  - `tests/test_routing_workers.py::test_an_intake_key_with_no_row_warns_once_and_only_as_row_absent`
  - `tests/test_routing_workers.py::test_the_export_gate_says_why_an_intake_track_goes_nowhere`
  - `tests/test_routing_workers.py::test_the_export_gate_screen_says_none_for_an_empty_warning_list`

Old text:

```
    if not owed:
        return []

```

New text:

```
    if owed < 0:
        return []

```

### `r688.G2_count_off_by_one`

the warning names one row more than the count the planner returned

- File: `src/cratekit/write/routing_cli.py`
- Source: `r688.json`, row `G2_count_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 7 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_declined_run_still_says_which_ratings_are_owed`
  - `tests/test_routing_workers.py::test_a_lone_unrated_track_with_energy_is_owed_one_rating`
  - `tests/test_routing_workers.py::test_a_vocal_track_unrated_is_owed_one_rating_not_one_per_place`
  - `tests/test_routing_workers.py::test_an_owed_star_rating_is_not_written_into_the_export`
  - `tests/test_routing_workers.py::test_the_export_gate_shows_every_item_the_digest_was_taken_over`
  - `tests/test_routing_workers.py::test_the_offered_plan_names_no_rating_and_says_which_are_owed`
  - `tests/test_routing_workers.py::test_two_rows_naming_one_file_are_both_counted_as_owed`

Old text:

```
        "message": f"{owed} intake row(s) are owed a star rating from energy and "

```

New text:

```
        "message": f"{owed + 1} intake row(s) are owed a star rating from energy and "

```

### `r688.N1_long_track_change_not_a_write`

a run whose only change is the long track playlist writes no file, existing guard sampled

- File: `src/cratekit/write/routing_cli.py`
- Source: `r688.json`, row `N1_long_track_change_not_a_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_long_track_alone_is_a_change_and_writes_a_file`

Old text:

```
    if not report.inserted and not lengthened and not vox_created:

```

New text:

```
    if not report.inserted and not vox_created:

```

### `r688.U1_hand_rated_counted`

a rating a person set is counted as owed, existing guard sampled

- File: `src/cratekit/write/routing_cli.py`
- Source: `r688.json`, row `U1_hand_rated_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 4 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_declined_run_still_says_which_ratings_are_owed`
  - `tests/test_routing_workers.py::test_a_hand_rated_export_track_is_not_owed_a_rating`
  - `tests/test_routing_workers.py::test_an_owed_star_rating_is_not_written_into_the_export`
  - `tests/test_routing_workers.py::test_the_offered_plan_names_no_rating_and_says_which_are_owed`

Old text:

```
    return value is not None and value.strip() in ("", "0")

```

New text:

```
    return value is not None

```

### `r688.U2_missing_attribute_counted`

a row with no Rating attribute is counted as owed, existing guard sampled

- File: `src/cratekit/write/routing_cli.py`
- Source: `r688.json`, row `U2_missing_attribute_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 8 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_row_with_no_rating_attribute_is_not_counted_as_owed`
  - `tests/test_routing_workers.py::test_a_second_run_over_its_own_output_adds_nothing`
  - `tests/test_routing_workers.py::test_a_vocal_track_unrated_is_owed_one_rating_not_one_per_place`
  - `tests/test_routing_workers.py::test_an_export_location_under_a_retired_volume_name_resolves_through_the_prefix_map`
  - `tests/test_routing_workers.py::test_an_intake_key_with_no_row_warns_once_and_only_as_row_absent`
  - `tests/test_routing_workers.py::test_the_export_gate_says_why_an_intake_track_goes_nowhere`
  - `tests/test_routing_workers.py::test_the_export_gate_screen_says_none_for_an_empty_warning_list`
  - `tests/test_routing_workers.py::test_the_export_gate_shows_every_item_the_digest_was_taken_over`

Old text:

```
    return value is not None and value.strip() in ("", "0")

```

New text:

```
    return value is None or value.strip() in ("", "0")

```

### `r688.U3_empty_rating_not_unrated`

an empty Rating stops reading as nobody rated this, existing guard sampled

- File: `src/cratekit/write/routing_cli.py`
- Source: `r688.json`, row `U3_empty_rating_not_unrated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 3 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_declined_run_still_says_which_ratings_are_owed`
  - `tests/test_routing_workers.py::test_an_owed_star_rating_is_not_written_into_the_export`
  - `tests/test_routing_workers.py::test_the_offered_plan_names_no_rating_and_says_which_are_owed`

Old text:

```
    return value is not None and value.strip() in ("", "0")

```

New text:

```
    return value is not None and value.strip() in ("0",)

```

### `r688.V1_applied_envelope_drops_warning`

the applied run's envelope loses the owed rating warning, so the ratings nobody wrote go unsaid

- File: `src/cratekit/write/routing_cli.py`
- Source: `r688.json`, row `V1_applied_envelope_drops_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 6 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_lone_unrated_track_with_energy_is_owed_one_rating`
  - `tests/test_routing_workers.py::test_a_run_whose_every_filing_was_skipped_is_blocked_and_not_rated`
  - `tests/test_routing_workers.py::test_a_second_run_still_owing_ratings_is_nothing_to_route`
  - `tests/test_routing_workers.py::test_a_vocal_track_unrated_is_owed_one_rating_not_one_per_place`
  - `tests/test_routing_workers.py::test_an_owed_star_rating_is_not_written_into_the_export`
  - `tests/test_routing_workers.py::test_two_rows_naming_one_file_are_both_counted_as_owed`

Old text:

```
    warnings += unrated

```

New text:

```
    warnings += []

```

### `r688.V2_gate_drops_warning`

the gate's screen loses the owed rating warning, so a person answers without reading it

- File: `src/cratekit/write/routing_cli.py`
- Source: `r688.json`, row `V2_gate_drops_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 3 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_export_gate_prints_the_plan_in_the_default_mode`
  - `tests/test_routing_workers.py::test_the_export_gate_shows_every_item_the_digest_was_taken_over`
  - `tests/test_routing_workers.py::test_the_offered_plan_names_no_rating_and_says_which_are_owed`

Old text:

```
    facts = _export_facts(items, export, gaps, vox_created, [*warnings, *unrated])

```

New text:

```
    facts = _export_facts(items, export, gaps, vox_created, warnings)

```

### `r688.V3_declined_envelope_drops_warning`

the declined run's envelope loses the owed rating warning

- File: `src/cratekit/write/routing_cli.py`
- Source: `r688.json`, row `V3_declined_envelope_drops_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_declined_run_still_says_which_ratings_are_owed`

Old text:

```
            warnings=[*warnings, *unrated],

```

New text:

```
            warnings=warnings,

```

### `r688.W1_rating_written_again`

the export writer patches a rating onto every routed row again, the defect R-688 recorded: a write the import never lands

- File: `src/cratekit/write/routing_cli.py`
- Source: `r688.json`, row `W1_rating_written_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 5 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_hand_rated_export_track_is_not_owed_a_rating`
  - `tests/test_routing_workers.py::test_a_second_run_still_owing_ratings_is_nothing_to_route`
  - `tests/test_routing_workers.py::test_an_analysed_track_keeps_its_rating_and_its_grid`
  - `tests/test_routing_workers.py::test_an_owed_star_rating_is_not_written_into_the_export`
  - `tests/test_routing_workers.py::test_two_rows_naming_one_file_are_both_counted_as_owed`

Old text:

```
    report = trees.apply_playlist_changes(plan, buffer, tree=tree)
    lengthened, long_warning = 0, None

```

New text:

```
    report = trees.apply_playlist_changes(plan, buffer, tree=tree)
    trees.apply_rating_changes({key: 255 for keys in plan.values() for key in keys}, buffer)
    lengthened, long_warning = 0, None

```

### `r691.F1_routed_counts_vocal`

routed is counted off the vocal column instead of the destination, on both gates

- File: `src/cratekit/write/routing_cli.py`
- Source: `r691.json`, row `F1_routed_counts_vocal`
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
        "vocal": sum(1 for item in tracks if item["vocal"]),

```

New text:

```
        "routed": sum(1 for item in tracks if item["vocal"]),
        "vocal": sum(1 for item in tracks if item["vocal"]),

```

### `r691.F2_trees_left_off`

the trees the write goes into are left off the screen

- File: `src/cratekit/write/routing_cli.py`
- Source: `r691.json`, row `F2_trees_left_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_database_gate_prints_the_destination_in_the_default_mode`
  - `tests/test_routing_workers.py::test_the_database_inbox_gate_shows_each_files_destination`

Old text:

```
        "trees": list(plan.native),

```

New text:

```
        "trees": [],

```

### `r691.F3_planner_warnings_dropped_from_facts`

the planner's warnings stay off the screen, so a library with nothing native shows empty destinations and no reason

- File: `src/cratekit/write/routing_cli.py`
- Source: `r691.json`, row `F3_planner_warnings_dropped_from_facts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_an_empty_inbox_with_no_native_tree_answers_inbox_empty_with_the_remedy`
  - `tests/test_routing_workers.py::test_the_database_gate_on_a_library_with_no_native_tree_says_so_before_the_answer`

Old text:

```
        "not derived": list(plan.gaps),
        "warnings": [warning["message"] for warning in plan.warnings],

```

New text:

```
        "not derived": list(plan.gaps),
        "warnings": [],

```

### `r691.F4_gaps_dropped_from_facts`

the dimensions not derived stay off the database gate's screen

- File: `src/cratekit/write/routing_cli.py`
- Source: `r691.json`, row `F4_gaps_dropped_from_facts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_database_inbox_gate_shows_each_files_destination`

Old text:

```
        "not derived": list(plan.gaps),
        "warnings": [warning["message"] for warning in plan.warnings],

```

New text:

```
        "not derived": [],
        "warnings": [warning["message"] for warning in plan.warnings],

```

### `r691.K1_empty_folder_plan_names_no_tree`

the plan's placements are keyed only when the folder has files, so the write's index has nothing to find for an empty folder

- File: `src/cratekit/write/routing_cli.py`
- Source: `r691.json`, row `K1_empty_folder_plan_names_no_tree`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_an_empty_inbox_plan_names_every_native_tree`

Old text:

```
    placements: dict[str, tuple[rebuild.DeclaredPlacement, ...]] = {
        tree_id: () for tree_id in native
    }

```

New text:

```
    placements: dict[str, tuple[rebuild.DeclaredPlacement, ...]] = {}

```

### `r691.K2_gaps_not_carried_to_the_apply`

the apply reports nothing as not compared, the R-316 shape, now that the derivation happened on the plan

- File: `src/cratekit/write/routing_cli.py`
- Source: `r691.json`, row `K2_gaps_not_carried_to_the_apply`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_over_the_shipped_taxonomy_says_the_vocal_dimension_was_not_compared`
  - `tests/test_routing_workers.py::test_an_uncalibrated_inbox_warns_and_files_nothing_under_with_vox`

Old text:

```
        "not_compared": planned.gaps,

```

New text:

```
        "not_compared": (),

```

### `r691.N3_declined_envelope_drops_the_warning`

the declined answer drops the planner's warning, so a reader of the JSON after an abort cannot learn why every destination is empty

- File: `src/cratekit/write/routing_cli.py`
- Source: `r691.json`, row `N3_declined_envelope_drops_the_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_taxonomy_with_no_long_track_playlist_gets_the_review_alone_as_its_remedy`
  - `tests/test_routing_workers.py::test_the_database_gate_on_a_library_with_no_native_tree_says_so_before_the_answer`

Old text:

```
        return ctx.envelope(
            data=_plan(items, kind="inbox", applied=False),
            outcome=Outcome.NO_OP,
            warnings=planned.warnings,
        )

```

New text:

```
        return ctx.envelope(
            data=_plan(items, kind="inbox", applied=False),
            outcome=Outcome.NO_OP,
        )

```

### `r924.A4_split_on_one_part`

A set identified in one part is said to be in parts

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r924.json`, row `A4_split_on_one_part`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`
- Collected: 11 against a baseline of 11
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_human_output_says_the_fetch_then_the_plan_then_the_count`

Old text:

```
    split = f" in {parts} parts" if parts > 1 else ""
```

New text:

```
    split = f" in {parts} parts" if parts >= 1 else ""
```

