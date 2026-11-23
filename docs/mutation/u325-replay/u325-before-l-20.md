# Mutation table: u325-before-l-20

Measured by `scripts/mutate.py` on 2026-11-23 03:15 UTC, branch `HEAD` at `539638eb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22663 collected. pytest invocations for this batch: 83.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:15 UTC for commit `539638ebe629`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 73, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard. 71 row(s) were reused from a prior sidecar and were measured by an earlier process, whose children this run did not watch.

Null control `NULL_CONTROL`: killed 0, collected 22663 against 22663. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u157.L1_selection_counts` | `src/cratekit/intake/land_cli.py` | user | 5 file(s) | 208 | 1 | killed |
| `u261.O2_account_drops_the_app` | `src/cratekit/modules/outbound/tidal_account.py` | user | 3 file(s) | 207 | 2 | killed |
| `u207.A2_catalogue_ignores_screen` | `src/cratekit/label/tidal_catalogue.py` | user | 2 file(s) | 206 | 1 | killed |
| `u129-author.A18_frozen_name_ignored` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 24 | 2 | killed |
| `u181.L1_half_is_a_warning` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 20 | 1 | killed |
| `u181.L2_coefficient` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 20 | 1 | killed |
| `r290-author.S01_master_call_removed` | `src/cratekit/master/cli.py` | user | 2 file(s) | 199 | 9 | killed |
| `u145.M3_landing_heart_undated` | `src/cratekit/intake/account_playlists.py` | user | 1 file(s) | 19 | 11 | killed |
| `u153.L3_notes_colour_skipped` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 19 | 1 | killed |
| `u142.S11_read_handle_requires_closed` | `src/cratekit/export/set_cli.py` | user | 3 file(s) | 22663 | 0 (promoted) | zero |
| `u260.E1_engine_encodes_per_file` | `src/cratekit/tagging/tag.py` | user | 3 file(s) | 196 | 8 | killed |
| `u100-c.C8_refused_counted_present_after_fix` | `src/cratekit/label/cli.py` | user | 1 file(s) | 16 | 1 | killed |
| `u100-c.R5_adopt_always_writes_after_fix` | `src/cratekit/label/registry.py` | user | 1 file(s) | 16 | 1 | killed |
| `u267.M5_handle_after_close` | `src/cratekit/core/rb_writer.py` | maintainer | 1 file(s) | 15 | 1 | killed |
| `u267.M7_release_any_handle` | `src/cratekit/core/rb_writer.py` | maintainer | 1 file(s) | 15 | 1 | killed |
| `u242.M22_unmark_releases_nothing` | `src/cratekit/sync/unmark_cli.py` | user | 4 file(s) | 190 | 7 | killed |
| `u164.T4_undated_name` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 10 | 2 | killed |
| `u164.T7_reuse_gone` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 10 | 1 | killed |
| `r598-b.B7_sample_live_holder_released` | `src/cratekit/core/session.py` | user | 2 file(s) | 183 | 4 | killed |
| `u84-b.T4_default_unchecked` | `src/cratekit/tagging/tag.py` | maintainer | 2 file(s) | 172 | 1 | killed |
| `r1255.S7_log_unlisted_predicate` | `src/cratekit/core/session.py` | user | 4 file(s) | 169 | 13 | killed |
| `u198.P2_release_side` | `src/cratekit/modules/outbound/pairs.py` | user | 3 file(s) | 166 | 3 | killed |
| `u156.L24_label_on_the_bridge` | `src/cratekit/intake/land_cli.py` | user | 3 file(s) | 165 | 2 | killed |
| `u37-author-light.G5_path_repair_queue` | `src/cratekit/intake/repair.py` | user | 2 file(s) | 164 | 3 | killed |
| `u202-composites.P1_reserve_held` | `src/cratekit/modules/outbound/pairs.py` | user | 3 file(s) | 158 | 1 | killed |
| `u270.A1_failed_attempt_reopens` | `src/cratekit/modules/outbound/tidal_account.py` | user | 3 file(s) | 157 | 2 | killed |
| `u142.S10_gate_folder_item_named_by_year` | `src/cratekit/export/set_cli.py` | user | 2 file(s) | 156 | 1 | killed |
| `u111-b.B1_move_names_every_table` | `src/cratekit/write/trees.py` | user | 2 file(s) | 153 | 1 | killed |
| `r1103.H1_item_not_failed` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 3 | killed |
| `r746-b.N9_placement_check_dropped_from_the_screen` | `src/cratekit/intake/landing.py` | user | 3 file(s) | 151 | 3 | killed |
| `r816-e.D2_survey_total` | `src/cratekit/write/metadata_cli.py` | user | 3 file(s) | 22663 | 0 (promoted) | zero |
| `u164.T1_filed_target` | `src/cratekit/intake/shelve.py` | user | 4 file(s) | 148 | 57 | killed |
| `u293.S3_sync_land_holds` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 144 | 1 | killed |
| `r1255.S8_clause_listing_wording` | `src/cratekit/core/session.py` | user | 3 file(s) | 142 | 9 | killed |
| `r669-b.B1_composer_not_sanitized` | `src/cratekit/core/naming.py` | user | 2 file(s) | 133 | 2 | killed |
| `u114.M18_narrow_called` | `src/cratekit/tagging/rows.py` | user | 2 file(s) | 131 | 21 | killed |
| `r1255.T1_tree_registry_clause` | `src/cratekit/core/tree_registry.py` | user | 3 file(s) | 125 | 2 | killed |
| `u56-catalogue-searcher-and-tag-workers.R26_retag_queues_no_items` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 122 | 20 | killed |
| `r1634.M16_worker_drops_how` | `src/cratekit/label/cli.py` | user | 2 file(s) | 119 | 1 | killed |
| `r705-b.S9_playlist_read_wraps_the_park` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 117 | 1 | killed |
| `u242.M21_mark_cli_already_marked_by_title` | `src/cratekit/sync/mark_cli.py` | user | 2 file(s) | 115 | 1 | killed |
| `u242.M9_take_overwrites_a_held_entry` | `src/cratekit/sync/mark_record.py` | user | 2 file(s) | 115 | 1 | killed |
| `a32.J3_bookkeeping_counted_as_moved` | `src/cratekit/write/row_defaults.py` | user | 2 file(s) | 112 | 6 | killed |
| `u144-c.C9_parent_of_named` | `src/cratekit/intake/set_playlist.py` | user | 2 file(s) | 112 | 12 | killed |
| `u319.M9_warning_drops_the_short_path` | `src/cratekit/intake/land_cli.py` | user | 3 file(s) | 106 | 1 | killed |
| `u181.C3_unscored_flag_ignored` | `src/cratekit/vocals/cli.py` | user | 2 file(s) | 105 | 4 | killed |
| `u179.P1_shared_preflight` | `src/cratekit/cli/sync_land.py` | user | 2 file(s) | 104 | 3 | killed |
| `r746-b.N8_unsupported_file_moved_anyway` | `src/cratekit/intake/landing.py` | user | 2 file(s) | 103 | 1 | killed |
| `u140.B6_mark_refusal_dropped` | `src/cratekit/export/set_cli.py` | user | 2 file(s) | 102 | 2 | killed |
| `u142.S12_undeclared_reads_as_empty` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 100 | 1 | killed |
| `u175.R1_account_ids_unrecorded` | `src/cratekit/intake/rotate.py` | user | 4 file(s) | 98 | 3 | killed |
| `u267.M4_handle_opens_every_time` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 92 | 6 | killed |
| `u319.M8_ok_on_any_field` | `src/cratekit/intake/land_cli.py` | user | 3 file(s) | 92 | 2 | killed |
| `u242.M8_twins_reads_the_title_alone` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 92 | 1 | killed |
| `u150.F2_record_provider` | `src/cratekit/intake/native.py` | user | 2 file(s) | 90 | 1 | killed |
| `u267.M12_inspiration_set_folder_write_guard` | `src/cratekit/export/set_cli.py` | maintainer | 2 file(s) | 88 | 1 | killed |
| `u156.L25_shared_rule_near_match` | `src/cratekit/intake/landing.py` | user | 2 file(s) | 85 | 1 | killed |
| `u135.A14_set_order_reverses` | `src/cratekit/intake/native.py` | user | 2 file(s) | 85 | 3 | killed |
| `u242.M7_inspiration_reads_the_title_alone` | `src/cratekit/organize/inspiration.py` | user | 2 file(s) | 85 | 1 | killed |
| `u288.M15_append_past_highest` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 84 | 2 | killed |
| `u221.R15_mark_drops_the_hold` | `src/cratekit/modules/outbound/pairs.py` | user | 3 file(s) | 84 | 14 | killed |
| `u113-c.C6_names_checked_after_moves` | `src/cratekit/intake/landing.py` | user | 2 file(s) | 79 | 1 | killed |
| `u221.R19_short_listing_records_its_misses` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 78 | 1 | killed |
| `u219.K3_accept_declined` | `src/cratekit/cli/rebuild.py` | user | 2 file(s) | 77 | 1 | killed |
| `u113-b.B5_export_clash_unasked` | `src/cratekit/intake/landing.py` | user | 2 file(s) | 76 | 1 | killed |
| `u185.G5_reading_at_open` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 75 | 20 | killed |
| `u130-c.C5_no_renumber` | `src/cratekit/write/playlist_pair.py` | user | 1 file(s) | 75 | 3 | killed |
| `u243.L7_kept_read_judged_blind` | `src/cratekit/label/kept_reads.py` | user | 2 file(s) | 74 | 4 | killed |
| `u166.R2_rotate_reserved` | `src/cratekit/intake/rotate.py` | user | 3 file(s) | 74 | 1 | killed |
| `u130-c.C6_pair_not_vouched` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 73 | 5 | killed |
| `u246.S16_inspiration_held_per_element` | `src/cratekit/organize/inspiration.py` | maintainer | 2 file(s) | 72 | 1 | killed |
| `u119.G16_read_back_blind_to_leftovers` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 22663 | 0 (promoted) | zero |
| `u164.W2_preflight_target` | `src/cratekit/intake/landing.py` | maintainer | 2 file(s) | 69 | 1 | killed |
| `u150.L1_forget_checks_id` | `src/cratekit/modules/outbound/ledger.py` | user | 2 file(s) | 67 | 1 | killed |
| `u145.M4_states_carried_only` | `src/cratekit/intake/account_playlists.py` | user | 2 file(s) | 64 | 8 | killed |
| `u212.N5_claim_plain` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 59 | 1 | killed |
| `u267.M11_rotation_opens_its_own` | `src/cratekit/intake/rotate_cli.py` | user | 2 file(s) | 56 | 4 | killed |
| `u113-a.A2_queue_order` | `src/cratekit/intake/account_playlists.py` | user | 2 file(s) | 22663 | 0 (promoted) | zero |

## Zero rows and what they owe

- `u142.S11_read_handle_requires_closed` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r816-e.D2_survey_total` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u119.G16_read_back_blind_to_leftovers` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u113-a.A2_queue_order` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `u157.L1_selection_counts`

awaiting_analysis: count no row as carrying dyn

- File: `src/cratekit/intake/land_cli.py`
- Source: `u157.json`, row `L1_selection_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`, `tests/test_drift.py`, `tests/test_analyze_check.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_dyn_native.py::test_the_warning_names_both_selections_and_counts_each`

Old text:

```
    dyned = sum(1 for row in collection.added if row.dyn)
    normal
```

New text:

```
    dyned = 0
    normal
```

### `u261.O2_account_drops_the_app`

open_account: build the account without the held app client, so its ISRC lookups go to the account

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u261.json`, row `O2_account_drops_the_app`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_catalogue_app.py`, `tests/test_outbound_tidal_account.py`
- Collected: 207 against a baseline of 207
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_open_account_and_open_catalogue_hand_the_app_client_on`
  - `tests/test_provider_session_hold.py::test_the_app_client_is_held_with_the_session_and_asks_one_token`

Old text:

```
    return TidalAccount(held.client, cfg=cfg, catalogue=held.app)
```

New text:

```
    return TidalAccount(held.client, cfg=cfg, catalogue=None)
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

### `u129-author.A18_frozen_name_ignored`

Ignore the frozen INSPIRATION name on the job and recompute it

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u129-author.json`, row `A18_frozen_name_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/test_u129_set_account_playlist.py::test_export_set_backfill_names_playlists_already_made_when_a_credential_fails`
  - `tests/test_u129_set_account_playlist.py::test_export_set_backfill_names_playlists_already_made_when_one_fails`

Old text:

```
    return str(payload.get(intake_cli.PLAYLIST_NAME) or "").strip()

```

New text:

```
    return ""

```

### `u181.L1_half_is_a_warning`

land_cli vox_plan_warnings: warn at exactly half the added rows unscored

- File: `src/cratekit/intake/land_cli.py`
- Source: `u181.json`, row `L1_half_is_a_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_vox_native.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_half_a_batch_unscored_is_said_on_the_line_and_is_no_warning`

Old text:

```
    if not adding or 2 * len(unscored) <= len(adding):
```

New text:

```
    if not adding or 2 * len(unscored) < len(adding):
```

### `u181.L2_coefficient`

land_cli vox_plan_warnings: halve the coefficient, so only an unscored batch above the whole warns

- File: `src/cratekit/intake/land_cli.py`
- Source: `u181.json`, row `L2_coefficient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_vox_native.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_batch_mostly_unscored_carries_a_warning_with_its_code_on_the_gate_screen`

Old text:

```
    if not adding or 2 * len(unscored) <= len(adding):
```

New text:

```
    if not adding or 1 * len(unscored) <= len(adding):
```

### `r290-author.S01_master_call_removed`

Remove the one jobs.raise_for_state call from master/cli.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/master/cli.py`
- Source: `r290-author.json`, row `S01_master_call_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_master_cli.py`
- Collected: 199 against a baseline of 199
- Kills: 9 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[master]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[master]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[master]`
  - `tests/test_job_outcome.py::test_a_park_on_a_gate_coded_cause_is_still_not_resumable_through_the_run`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[master]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[master]`
  - `tests/test_job_outcome.py::test_every_function_that_drives_a_job_maps_its_ending_afterwards`
  - `tests/test_job_outcome.py::test_the_dispatcher_reads_the_blocked_type_as_the_blocked_outcome`
  - `tests/test_master_cli.py::test_a_job_that_failed_on_a_missing_source_is_not_reopened_and_a_fresh_job_masters_it`

Old text:

```
jobs.raise_for_state(job)
```

New text:

```
jobs.get  # the mapping call, removed
```

### `u145.M3_landing_heart_undated`

Hearted.month: a landed heart whose job dated it goes to Undated

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u145.json`, row `M3_landing_heart_undated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_hearts_native.py`
- Collected: 19 against a baseline of 19
- Kills: 11 (killed)
- Killed:
  - `tests/test_intake_land_hearts_native.py::test_a_heart_a_playlist_also_asked_for_is_in_that_playlist_and_in_all_favorites`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_dated_the_twentieth_of_october_joins_its_month_and_no_quarter_is_made`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_whose_job_froze_no_date_key_joins_all_favorites_and_no_month`
  - `tests/test_intake_land_hearts_native.py::test_a_hearted_file_lands_in_its_batch_all_favorites_and_a_month_made_for_it`
  - `tests/test_intake_land_hearts_native.py::test_a_source_at_the_root_takes_its_months_beside_it`
  - `tests/test_intake_land_hearts_native.py::test_the_hearts_are_in_the_digest_so_another_set_is_another_plan`
  - `tests/test_intake_land_hearts_native.py::test_the_pass_jobs_hearts_are_read_from_the_job_and_a_playlist_job_claims_no_heart`
  - `tests/test_intake_land_hearts_native.py::test_the_pass_prefers_the_mention_that_knows_its_date`
  - `tests/test_intake_land_hearts_native.py::test_the_record_carries_the_hearts_placed_under_their_own_key`
  - `tests/test_intake_land_hearts_native.py::test_two_hearts_of_two_months_and_an_existing_month_is_added_to_not_made`
  - `tests/test_intake_land_hearts_native.py::test_with_no_pink_row_the_landing_places_the_heart_and_warns`

Old text:

```
        return placeholders.month_label(self.hearted) if self.known else None
```

New text:

```
        return placeholders.UNDATED if self.known else None
```

### `u153.L3_notes_colour_skipped`

land_cli favorites_notes: never emit the missing-Pink note, so a landing that coloured nothing says nothing

- File: `src/cratekit/intake/land_cli.py`
- Source: `u153.json`, row `L3_notes_colour_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_hearts_native.py`
- Collected: 19 against a baseline of 19
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_hearts_native.py::test_with_no_pink_row_the_landing_places_the_heart_and_warns`

Old text:

```
    if placed.colour_skipped:
        notes.append(
            {
                "code": colour_mod.PINK_COLOUR_MISSING,
```

New text:

```
    if False:
        notes.append(
            {
                "code": colour_mod.PINK_COLOUR_MISSING,
```

### `u142.S11_read_handle_requires_closed`

_inspiration_playlists: open for writing on organize's read too, so a running rekordbox refuses the INSPIRATION proof

- File: `src/cratekit/export/set_cli.py`
- Source: `u142.json`, row `S11_read_handle_requires_closed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        require_closed=not read_only,
```

New text:

```
        require_closed=True,
```

### `u260.E1_engine_encodes_per_file`

_art_embedded: call the plain encoder again, so every file encodes the same bytes

- File: `src/cratekit/tagging/tag.py`
- Source: `u260.json`, row `E1_engine_encodes_per_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 196 against a baseline of 196
- Kills: 8 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[a refusal]`
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[a transport failure]`
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[an empty answer]`
  - `tests/test_album_cover_once.py::test_every_file_carries_byte_for_byte_what_it_carried_before`
  - `tests/test_album_cover_once.py::test_ten_files_naming_one_address_make_one_request_one_wait_and_one_encode`
  - `tests/test_album_cover_once.py::test_two_addresses_serving_the_same_bytes_make_two_requests_and_one_encode`
  - `tests/test_album_cover_once.py::test_two_albums_in_one_folder_make_two_requests_and_two_encodes`
  - `tests/test_tag_workers.py::test_an_albums_cover_is_asked_for_and_encoded_once_across_the_queued_sweep`

Old text:

```
        cdj = art.to_cdj_jpeg_remembered(data)
```

New text:

```
        cdj = art.to_cdj_jpeg(data)
```

### `u100-c.C8_refused_counted_present_after_fix`

the summary lists a refused name as present, telling a script the registry holds it, re-measured after the fix round added its test

- File: `src/cratekit/label/cli.py`
- Source: `u100-c.json`, row `C8_refused_counted_present_after_fix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_adopt.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_a_name_with_no_identifier_fails_alone_and_the_rest_land`

Old text:

```
                    if not result.added and result.refused is None
```

New text:

```
                    if not result.added
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

### `u267.M5_handle_after_close`

SharedRead.handle: drop the refusal after close, so a closed shared read reopens silently

- File: `src/cratekit/core/rb_writer.py`
- Source: `u267.json`, row `M5_handle_after_close`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`
- Collected: 15 against a baseline of 15
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_a_shared_read_refuses_a_handle_not_its_own_and_a_read_after_close`

Old text:

```
        if self._closed:
            raise _defect("a read handle was asked of a shared read that was already closed")
```

New text:

```
        if False:
            raise _defect("a read handle was asked of a shared read that was already closed")
```

### `u267.M7_release_any_handle`

SharedRead.release: drop the refusal of a handle that is not its own

- File: `src/cratekit/core/rb_writer.py`
- Source: `u267.json`, row `M7_release_any_handle`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`
- Collected: 15 against a baseline of 15
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_a_shared_read_refuses_a_handle_not_its_own_and_a_read_after_close`

Old text:

```
        if db is not self._db:
            raise _defect("a handle that is not the shared read's own was released through it")
```

New text:

```
        if False:
            raise _defect("a handle that is not the shared read's own was released through it")
```

### `u242.M22_unmark_releases_nothing`

sync unmark: never plan a release, so a pass's taken playlists cannot be let go

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `u242.json`, row `M22_unmark_releases_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_sync_unmark.py`, `tests/test_label_playlists.py`, `tests/test_export_set.py`
- Collected: 190 against a baseline of 190
- Kills: 7 (killed)
- Killed:
  - `tests/test_export_set.py::test_sync_unmark_takes_the_archive_mark_off_again`
  - `tests/test_label_playlists.py::test_sync_unmark_takes_the_label_mark_off_again`
  - `tests/test_u242_taken.py::test_a_release_that_fails_part_way_names_what_was_let_go`
  - `tests/test_u242_taken.py::test_a_release_whose_title_was_retitled_since_stamps_the_pass_mark`
  - `tests/test_u242_taken.py::test_unmark_lets_go_a_pass_mark_with_no_write_to_the_account`
  - `tests/test_u242_taken.py::test_unmark_of_a_legacy_pass_after_the_strip_releases_and_stamps_it`
  - `tests/test_u242_taken.py::test_unmark_playlist_narrows_the_releases`

Old text:

```
    taken_held = held is not None and held.held
```

New text:

```
    taken_held = False
```

### `u164.T4_undated_name`

filed_parts: file a name with no date under the whole name as a date-free folder

- File: `src/cratekit/intake/shelve.py`
- Source: `u164.json`, row `T4_undated_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filed.py`
- Collected: 10 against a baseline of 10
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_name_landed_into_again_goes_back_to_its_folder_unless_the_folder_is_gone`
  - `tests/test_intake_land_filed.py::test_a_name_with_no_date_is_the_subject_under_the_landing_day`

Old text:

```
    when, words = parsed if parsed is not None else (on, " ".join(batch.split()))
```

New text:

```
    when, words = parsed if parsed is not None else (on, "")
```

### `u164.T7_reuse_gone`

landing_target: reuse a recorded folder even when it is gone from disk

- File: `src/cratekit/intake/shelve.py`
- Source: `u164.json`, row `T7_reuse_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filed.py`
- Collected: 10 against a baseline of 10
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_name_landed_into_again_goes_back_to_its_folder_unless_the_folder_is_gone`

Old text:

```
    if again is not None and os.path.isdir(again) and not os.path.islink(again):
```

New text:

```
    if again is not None:
```

### `r598-b.B7_sample_live_holder_released`

release_stale_lock: skip the live holder refusal (existing guard, sampled because the sweep now sits behind it)

- File: `src/cratekit/core/session.py`
- Source: `r598-b.json`, row `B7_sample_live_holder_released`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`, `tests/test_write_session.py`
- Collected: 183 against a baseline of 183
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_live_holders_claim_is_refused_and_the_lock_file_is_untouched`
  - `tests/test_session_cli.py::test_a_live_lock_holder_refuses_and_abandons_nothing`
  - `tests/test_write_session.py::test_a_live_holder_this_platform_will_not_describe_is_assumed_alive`
  - `tests/test_write_session.py::test_the_lock_left_by_another_machine_with_this_host_name_is_not_releasable`

Old text:

```
    if holder_alive(recorded):
        raise refuse(
```

New text:

```
    if False:
        raise refuse(
```

### `u84-b.T4_default_unchecked`

A result built without the repair claims the repair passed

- File: `src/cratekit/tagging/tag.py`
- Source: `u84-b.json`, row `T4_default_unchecked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_result_built_without_the_repair_does_not_claim_it_passed`

Old text:

```
    art_repair: str = art.REPAIR_UNCHECKED
```

New text:

```
    art_repair: str = art.REPAIR_OK
```

### `r1255.S7_log_unlisted_predicate`

log_unlisted: never name the unread half as the log, so every refusal counts it as one entry

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S7_log_unlisted_predicate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_unmirrored.py`, `tests/test_intake_shelve.py`, `tests/test_tree_registry.py`
- Collected: 169 against a baseline of 169
- Kills: 13 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`
  - `tests/test_session_log_unlisted.py::test_a_log_that_cannot_be_listed_is_returned_as_the_one_unread_entry`
  - `tests/test_session_log_unlisted.py::test_every_destructive_session_is_refused_at_its_gate`
  - `tests/test_session_log_unlisted.py::test_restore_list_refuses_a_log_it_cannot_list_rather_than_list_nothing`
  - `tests/test_session_log_unlisted.py::test_restore_run_refuses_naming_the_listing_not_an_unrecorded_session`
  - `tests/test_session_log_unlisted.py::test_the_batch_name_rule_refuses_rather_than_call_a_name_free`
  - `tests/test_session_log_unlisted.py::test_the_check_refuses_an_unknown_landing_naming_the_listing`
  - `tests/test_session_log_unlisted.py::test_the_clause_names_the_listing_and_not_an_entry`
  - `tests/test_session_log_unlisted.py::test_the_native_landing_lookups_refuse_a_log_they_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_reporting_reader_refuses_a_log_it_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_rotation_reads_the_listing_from_the_scan`
  - `tests/test_session_log_unlisted.py::test_the_tree_registry_refuses_rather_than_read_no_open_run`
  - `tests/test_session_log_unlisted.py::test_the_unresolved_session_gate_refuses_over_a_log_it_cannot_list`

Old text:

```
    return log_dir(cfg) in unreadable
```

New text:

```
    return False
```

### `u198.P2_release_side`

pairs.release: the survivor is recorded on the wrong side

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u198.json`, row `P2_release_side`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 166 against a baseline of 166
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_playlist_deleted_in_rekordbox_unpairs_and_leaves_the_account_playlist`
  - `tests/test_sync_pair_discover.py::test_a_playlist_deleted_on_the_account_unpairs_stays_and_is_not_made_again`
  - `tests/test_sync_pair_discover.py::test_a_write_of_the_pairs_alone_keeps_the_folders_misses_and_released`

Old text:

```
            if side == ACCOUNT_SIDE:
```

New text:

```
            if side != ACCOUNT_SIDE:
```

### `u156.L24_label_on_the_bridge`

_label_flag: accept --label on the bridge, where the landing files nothing from it

- File: `src/cratekit/intake/land_cli.py`
- Source: `u156.json`, row `L24_label_on_the_bridge`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land.py`
- Collected: 165 against a baseline of 165
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_label_from_tags_on_the_bridge_is_refused_before_the_gate_naming_the_flag`
  - `tests/test_intake_land_labels_native.py::test_label_on_the_bridge_is_refused_before_the_gate_naming_the_flag`

Old text:

```
    if not medium.native:
        raise refuse(
            "intake-list-unusable",
            f"{flag} files the batch
```

New text:

```
    if False:
        raise refuse(
            "intake-list-unusable",
            f"{flag} files the batch
```

### `u37-author-light.G5_path_repair_queue`

Offer path repair into the adoption queue instead

- File: `src/cratekit/intake/repair.py`
- Source: `u37-author-light.json`, row `G5_path_repair_queue`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_review_queue.py`, `tests/intake/test_repair.py`
- Collected: 164 against a baseline of 164
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_repair.py::test_offer_repairs_writes_path_repair_queue_items`
  - `tests/test_review_queue.py::test_every_new_adjudication_surface_is_owed_by_a_registered_unit`
  - `tests/test_review_queue.py::test_the_path_repair_pass_offers_its_proposals_into_the_path_repair_queue`

Old text:

```
            queue=Queue.PATH_REPAIR,
```

New text:

```
            queue=Queue.ADOPTION,
```

### `u202-composites.P1_reserve_held`

reserve_made_rekordbox: an account playlist a pair already holds is made a second rekordbox playlist

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u202-composites.json`, row `P1_reserve_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`
- Collected: 158 against a baseline of 158
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_reserving_an_account_playlist_a_pair_holds_answers_that_pair_and_makes_nothing`

Old text:

```
            held = document.pairs.get(account_id)
            if held is not None:
                return held.rekordbox_id, False
            rekordbox_id = str(create())
```

New text:

```
            rekordbox_id = str(create())
```

### `u270.A1_failed_attempt_reopens`

add_tracks: keep the object after a failed attempt, so the retry sends its stale tag and is refused 412 (round one's finding)

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u270.json`, row `A1_failed_attempt_reopens`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_export_batches.py`, `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`
- Collected: 157 against a baseline of 157
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_export_batches.py::test_one_refused_read_after_a_landed_add_is_retried_on_a_fresh_open_and_recorded`
  - `tests/test_outbound_export_batches.py::test_one_refused_read_after_a_landed_add_through_the_driver_finishes_the_job`

Old text:

```
                except Exception:
                    opened[0] = None
                    raise

            for start in range(0, len(lacking), ADD_CHUNK):
```

New text:

```
                except Exception:
                    raise

            for start in range(0, len(lacking), ADD_CHUNK):
```

### `u142.S10_gate_folder_item_named_by_year`

export archive payload: name the folder item by the plain year, so the plan shows a folder that is not the one written

- File: `src/cratekit/export/set_cli.py`
- Source: `u142.json`, row `S10_gate_folder_item_named_by_year`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`, `tests/test_organize.py`
- Collected: 156 against a baseline of 156
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_the_archive_takes_records_and_files_it_in_a_year_folder_made_once`

Old text:

```
                "name": planned.folder_name,
```

New text:

```
                "name": planned.year,
```

### `u111-b.B1_move_names_every_table`

The membership move's commit admits the whole removable set again, the playlist table included

- File: `src/cratekit/write/trees.py`
- Source: `u111-b.json`, row `B1_move_names_every_table`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_adopt_move.py`
- Collected: 153 against a baseline of 153
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_only_the_rotation_asks_its_commit_to_admit_a_removed_playlist`

Old text:

```
                rb_writer.commit_guarded(db, removals=(rb_writer.MEMBERSHIP_TABLE,))
```

New text:

```
                rb_writer.commit_guarded(db, removals=rb_writer.REMOVABLE_TABLES)
```

### `r1103.H1_item_not_failed`

handle: drop the refusal for an unwritten result, so the item ends done with a report and the job succeeds over a file that kept its catch-all

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r1103.json`, row `H1_item_not_failed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_genre_retag.py`
- Collected: 152 against a baseline of 152
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_is_named_in_the_human_answer`
  - `tests/test_tag_workers.py::test_a_retag_whose_only_file_will_not_take_its_genre_names_no_reload`

Old text:

```
    if result.reason == retag.UNWRITTEN_REASON:
```

New text:

```
    if False:
```

### `r746-b.N9_placement_check_dropped_from_the_screen`

_screen: a file whose tags resolve to no sub is moved on both media

- File: `src/cratekit/intake/landing.py`
- Source: `r746-b.json`, row `N9_placement_check_dropped_from_the_screen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_landing.py`, `tests/test_intake_land.py`
- Collected: 151 against a baseline of 151
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_file_whose_tags_resolve_to_no_sub_stays_in_staging_on_the_native_medium_too`
  - `tests/test_landing.py::test_a_batch_where_nothing_lands_leaves_no_batch_folder`
  - `tests/test_landing.py::test_a_file_with_no_declared_sub_is_left_in_staging_naming_tag_folder`

Old text:

```
            named.get(item) or _unplaceable(item, declared) or _occupied(item, target / item.name)
```

New text:

```
            named.get(item) or _occupied(item, target / item.name)
```

### `r816-e.D2_survey_total`

_is_a_file: let a refusal to answer raise out of the survey

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r816-e.json`, row `D2_survey_total`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`, `tests/test_metadata_cli.py`, `tests/test_paths_resolved.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    try:
        return path.is_file()
    except (OSError, ValueError):
        return False
```

New text:

```
    return path.is_file()
```

### `u164.T1_filed_target`

landing_target: land in the music folder's batch path rather than the filed folder

- File: `src/cratekit/intake/shelve.py`
- Source: `u164.json`, row `T1_filed_target`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_shelve.py`, `tests/test_intake_land_rehearse.py`
- Collected: 148 against a baseline of 148
- Kills: 57 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_filed_folder_on_another_device_is_refused_at_the_move`
  - `tests/test_intake_land_filed.py::test_a_folder_already_on_disk_is_passed_over_for_the_next_suffix`
  - `tests/test_intake_land_filed.py::test_a_folder_the_collection_stores_rows_under_is_passed_over_with_nothing_on_disk`
  - `tests/test_intake_land_filed.py::test_a_landing_on_the_27th_lands_in_its_year_folder_under_its_subject`
  - `tests/test_intake_land_filed.py::test_a_name_landed_into_again_goes_back_to_its_folder_unless_the_folder_is_gone`
  - `tests/test_intake_land_filed.py::test_a_name_that_is_a_date_alone_files_as_downloads`
  - `tests/test_intake_land_filed.py::test_a_name_with_no_date_is_the_subject_under_the_landing_day`
  - `tests/test_intake_land_filed.py::test_a_second_unnamed_landing_that_day_takes_two_for_its_playlist_and_its_folder`
  - `tests/test_intake_land_filed.py::test_an_unnamed_landing_files_under_the_day_and_its_source_words`
  - `tests/test_intake_land_filed.py::test_shelve_over_a_batch_landed_filed_reports_nothing_to_do`
  - `tests/test_intake_land_native.py::test_a_failure_on_the_second_file_leaves_the_database_as_it_was_and_names_the_moves`
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_file_whose_tags_resolve_to_no_sub_stays_in_staging_on_the_native_medium_too`
  - `tests/test_intake_land_native.py::test_a_landing_that_adds_no_row_needs_no_majority`
  - `tests/test_intake_land_native.py::test_a_row_whose_content_link_did_not_take_is_refused_after_the_commit`
  - ... and 42 more, see the JSON sidecar

Old text:

```
    when, said = filed_parts(batch, on=on)
    spell = _speller(db)
```

New text:

```
    return landing.target_dir(cfg, batch)
    when, said = filed_parts(batch, on=on)
    spell = _speller(db)
```

### `u293.S3_sync_land_holds`

sync_land: a pass by hand takes no staging lock

- File: `src/cratekit/cli/sync_land.py`
- Source: `u293.json`, row `S3_sync_land_holds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_night.py`, `tests/test_sync_land.py`, `tests/test_sync_land_beside.py`
- Collected: 144 against a baseline of 144
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_night.py::test_a_pass_by_hand_refuses_while_the_night_holds_the_lock`

Old text:

```
    with staging_lock.held("crate sync land", run_id=ctx.run.run_id):
```

New text:

```
    if True:
```

### `r1255.S8_clause_listing_wording`

unread_clause: word an unlisted log as the count of entries, so a gate sends a person to a damaged file

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S8_clause_listing_wording`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_intake_shelve.py`, `tests/test_tree_registry.py`
- Collected: 142 against a baseline of 142
- Kills: 9 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_every_destructive_session_is_refused_at_its_gate`
  - `tests/test_session_log_unlisted.py::test_restore_list_refuses_a_log_it_cannot_list_rather_than_list_nothing`
  - `tests/test_session_log_unlisted.py::test_restore_run_refuses_naming_the_listing_not_an_unrecorded_session`
  - `tests/test_session_log_unlisted.py::test_the_batch_name_rule_refuses_rather_than_call_a_name_free`
  - `tests/test_session_log_unlisted.py::test_the_clause_names_the_listing_and_not_an_entry`
  - `tests/test_session_log_unlisted.py::test_the_native_landing_lookups_refuse_a_log_they_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_reporting_reader_refuses_a_log_it_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_tree_registry_refuses_rather_than_read_no_open_run`
  - `tests/test_session_log_unlisted.py::test_the_unresolved_session_gate_refuses_over_a_log_it_cannot_list`

Old text:

```
        return "the session log exists and cannot be listed by this account"
```

New text:

```
        return "the session log holds 1 entry this build cannot read"
```

### `r669-b.B1_composer_not_sanitized`

G14's composite: drop the one sanitizer, the composer's, now that the copy in _artist is gone, so a slash in a credit reaches the filename

- File: `src/cratekit/core/naming.py`
- Source: `r669-b.json`, row `B1_composer_not_sanitized`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/test_acquire_fallback_fetch.py`
- Collected: 133 against a baseline of 133
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_the_stem_is_the_rows_and_carries_no_path_separator`
  - `tests/test_naming_apply_cli.py::test_a_slash_in_a_tag_takes_the_body_form_of_a_segment`

Old text:

```
        part for part in (sanitize_segment(artist or ""), sanitize_segment(title or "")) if part
```

New text:

```
        part for part in (artist or "", title or "") if part
```

### `u114.M18_narrow_called`

The row engine never calls the narrow step, so no file is written and every row is

- File: `src/cratekit/tagging/rows.py`
- Source: `u114.json`, row `M18_narrow_called`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`, `tests/test_tag_rows.py`
- Collected: 131 against a baseline of 131
- Kills: 21 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_commit_that_refuses_leaves_the_row_as_it_was_and_claims_no_commit`
  - `tests/test_tag_rows.py::test_a_file_on_a_volume_that_is_not_mounted_is_counted_and_the_run_does_not_fail`
  - `tests/test_tag_rows.py::test_a_held_row_survives_the_write_and_the_apply_must_name_it_again`
  - `tests/test_tag_rows.py::test_a_mistyped_identifier_is_shown_at_the_gate_and_warned_about`
  - `tests/test_tag_rows.py::test_a_person_reads_the_counts_and_the_pairs_at_the_gate_and_after_the_write`
  - `tests/test_tag_rows.py::test_a_restore_out_of_band_is_marked_before_this_write_replaces_the_evidence`
  - `tests/test_tag_rows.py::test_a_second_apply_plans_nothing_and_writes_nothing`
  - `tests/test_tag_rows.py::test_a_second_run_after_a_clean_one_asks_and_is_a_no_op`
  - `tests/test_tag_rows.py::test_a_word_the_library_has_no_row_for_names_the_act_on_a_run_that_wrote`
  - `tests/test_tag_rows.py::test_an_unregistered_policy_would_write_nothing_and_the_apply_registers_it`
  - `tests/test_tag_rows.py::test_planned_written_and_read_back_through_the_two_acts`
  - `tests/test_tag_rows.py::test_the_apply_is_a_recorded_session_a_restore_can_undo`
  - `tests/test_tag_rows.py::test_the_apply_writes_the_genre_and_no_other_column_of_any_row`
  - `tests/test_tag_rows.py::test_the_genre_report_stops_naming_the_old_word_after_the_run`
  - `tests/test_tag_rows.py::test_with_no_regression_the_write_marks_nothing_and_records_where_it_left_off`
  - ... and 6 more, see the JSON sidecar

Old text:

```
        if narrow is not None:
            plan = narrow(plan)
```

New text:

```
        if narrow is None:
            plan = narrow(plan)
```

### `r1255.T1_tree_registry_clause`

tree_registry._whole_log: word the refusal with the old count, not the clause

- File: `src/cratekit/core/tree_registry.py`
- Source: `r1255.json`, row `T1_tree_registry_clause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_tree_registry.py`, `tests/test_cutover_precheck.py`
- Collected: 125 against a baseline of 125
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_an_unreadable_record_keeps_its_own_refusal`
  - `tests/test_session_log_unlisted.py::test_the_tree_registry_refuses_rather_than_read_no_open_run`

Old text:

```
            f"{session.unread_clause(unreadable, cfg)}, so {so}; refusing rather than "
```

New text:

```
            f"the session log holds {len(unreadable)} entries this build cannot read, so {so}; refusing rather than "
```

### `u56-catalogue-searcher-and-tag-workers.R26_retag_queues_no_items`

The zero item rule broken on the second verb, over work somebody explicitly confirmed

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R26_retag_queues_no_items`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 122 against a baseline of 122
- Kills: 20 (killed)
- Killed:
  - `tests/test_queued_resume_contract.py::test_the_resume_the_job_driver_spawns_can_actually_proceed[tag.retag]`
  - `tests/test_tag_workers.py::test_a_corrected_retag_ends_by_naming_the_reload_the_stale_row_needs`
  - `tests/test_tag_workers.py::test_a_file_gone_at_drive_time_is_refused_rather_than_reported_done`
  - `tests/test_tag_workers.py::test_a_genre_made_blank_between_the_confirm_and_the_drive_is_left_to_its_owner`
  - `tests/test_tag_workers.py::test_a_genre_made_specific_between_the_confirm_and_the_drive_is_not_rewritten`
  - `tests/test_tag_workers.py::test_a_half_corrected_retag_carries_the_reload_on_its_refusal`
  - `tests/test_tag_workers.py::test_a_parked_retag_keeps_both_the_block_and_the_reload`
  - `tests/test_tag_workers.py::test_a_recorded_acceptance_is_used_and_the_searcher_is_never_asked`
  - `tests/test_tag_workers.py::test_a_resume_after_a_partial_run_meets_its_gate_rather_than_going_stale`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_is_named_in_the_human_answer`
  - `tests/test_tag_workers.py::test_a_retag_parses_the_active_taxonomy_once_however_many_files_it_corrects`
  - `tests/test_tag_workers.py::test_a_retag_that_corrected_nothing_does_not_send_a_person_to_rekordbox`
  - `tests/test_tag_workers.py::test_a_retag_whose_only_file_will_not_take_its_genre_names_no_reload`
  - `tests/test_tag_workers.py::test_a_retried_retag_drives_only_the_item_that_failed`
  - ... and 5 more, see the JSON sidecar

Old text:

```
            item_ids=tuple(str(row["path"]) for row in plan["items"]),
```

New text:

```
            item_ids=(),
```

### `r1634.M16_worker_drops_how`

label-sweep-incomplete: the worker's message no longer says how the release was asked

- File: `src/cratekit/label/cli.py`
- Source: `r1634.json`, row `M16_worker_drops_how`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_workers.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_though_every_held_line_names_the_label`

Old text:

```
            f"{one.how()}: {one.said()}."
```

New text:

```
            f": {one.said()}."
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

### `u242.M21_mark_cli_already_marked_by_title`

sync mark: decide already marked by the title alone, so a taken playlist is planned again

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u242.json`, row `M21_mark_cli_already_marked_by_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_u242_taken.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_partial_failure_names_what_was_marked`

Old text:

```
        elif playlists.is_taken(identity, entry.name, sweep.taken):
```

New text:

```
        elif playlists.is_swept_name(entry.name):
```

### `u242.M9_take_overwrites_a_held_entry`

take: replace an entry still held, so a second taker's stamp replaces the first and the migration is not idempotent

- File: `src/cratekit/sync/mark_record.py`
- Source: `u242.json`, row `M9_take_overwrites_a_held_entry`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_sync_mark.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_take_is_idempotent_and_a_released_entry_is_taken_afresh`

Old text:

```
                elif not taken[at].held:
```

New text:

```
                elif True:
```

### `a32.J3_bookkeeping_counted_as_moved`

The shared moved column rule counts the binding's bookkeeping columns as moved

- File: `src/cratekit/write/row_defaults.py`
- Source: `a32.json`, row `J3_bookkeeping_counted_as_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`, `tests/test_repair_rows.py`
- Collected: 112 against a baseline of 112
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

### `u144-c.C9_parent_of_named`

Sample of an existing U121 guard, now shared: take a live playlist of the name under any parent

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u144-c.json`, row `C9_parent_of_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`, `tests/test_organize_inspiration.py`
- Collected: 112 against a baseline of 112
- Kills: 12 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_file_two_collection_rows_claim_is_left_out_rather_than_one_row_picked`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_creates_the_declared_folder_at_the_root_when_the_library_lacks_it`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order`
  - `tests/test_set_inspiration_playlist.py::test_a_recorded_playlist_that_was_removed_is_not_added_to_and_a_live_one_is_made`
  - `tests/test_set_inspiration_playlist.py::test_a_row_neither_owned_nor_landed_is_counted_and_named_and_not_added`
  - `tests/test_set_inspiration_playlist.py::test_a_track_accepted_at_review_as_a_library_file_joins_the_playlist_at_a_landing`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_follows_the_live_inspiration_row_on_the_disposable_database`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_refuses_a_playlist_a_legacy_archive_prefixed`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_renames_a_set_the_landing_archived_and_it_stays_taken`
  - `tests/test_set_inspiration_playlist.py::test_members_keep_the_sets_order_when_it_is_not_alphabetical`
  - `tests/test_set_inspiration_playlist.py::test_posted_on_a_frozen_job_names_another_day_and_the_frozen_name_wins_with_a_warning`
  - `tests/test_set_inspiration_playlist.py::test_two_landings_of_one_set_on_two_days_make_one_playlist`

Old text:

```
        if str(getattr(row, "ParentID", "") or "") == parent_id:
```

New text:

```
        if True:
```

### `u319.M9_warning_drops_the_short_path`

land_cli: the awaiting analysis warning names one path again

- File: `src/cratekit/intake/land_cli.py`
- Source: `u319.json`, row `M9_warning_drops_the_short_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`, `tests/test_intake_land_native.py`, `tests/test_inbox_analyzed.py`
- Collected: 106 against a baseline of 106
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_dyn_native.py::test_the_warning_names_both_selections_and_counts_each`

Old text:

```
                f"for analysis, and {selections}; {AUTO_ANALYSIS_STEP}; then "
```

New text:

```
                f"for analysis, and {selections}; then "
```

### `u181.C3_unscored_flag_ignored`

analyze vocals: ignore --unscored, so the whole folder is queued

- File: `src/cratekit/vocals/cli.py`
- Source: `u181.json`, row `C3_unscored_flag_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`, `tests/test_sync_land.py`
- Collected: 105 against a baseline of 105
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_land.py::test_the_analyze_step_rescores_after_analyze_run_and_before_the_restamp`
  - `tests/test_vocals_cli.py::test_the_tails_rescore_scores_a_headed_file_with_no_score_and_leaves_a_scored_one`
  - `tests/test_vocals_cli.py::test_unscored_over_a_folder_whose_headed_files_all_carry_a_score_queues_nothing`
  - `tests/test_vocals_cli.py::test_unscored_queues_a_headed_file_with_no_score_and_leaves_the_rest_alone`

Old text:

```
    unscored = bool(getattr(ctx.args, "unscored", False))
```

New text:

```
    unscored = False
```

### `u179.P1_shared_preflight`

preflight: drop the rekordbox check, so sync bandcamp plans and fetches with rekordbox open

- File: `src/cratekit/cli/sync_land.py`
- Source: `u179.json`, row `P1_shared_preflight`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_land.py`
- Collected: 104 against a baseline of 104
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_rekordbox_running_refuses_before_the_plan`
  - `tests/test_sync_land.py::test_a_continued_pass_refused_while_rekordbox_runs_names_the_way_back`
  - `tests/test_sync_land.py::test_rekordbox_running_refuses_before_any_write`

Old text:

```
    rb_writer.assert_rekordbox_closed(verb)
```

New text:

```
    pass
```

### `r746-b.N8_unsupported_file_moved_anyway`

apply_native: a file the database has no type for is not refused per file and moves

- File: `src/cratekit/intake/landing.py`
- Source: `r746-b.json`, row `N8_unsupported_file_moved_anyway`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_landing.py`
- Collected: 103 against a baseline of 103
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_suffix_the_database_has_no_type_for_is_left_in_staging_and_the_batch_lands`

Old text:

```
        if row.action == native.UNSUPPORTED
    }
```

New text:

```
        if False
    }
```

### `u140.B6_mark_refusal_dropped`

plan_rename retitles a playlist the archive marked

- File: `src/cratekit/export/set_cli.py`
- Source: `u140.json`, row `B6_mark_refusal_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_playlist_the_archive_marked_is_refused_rather_than_retitled`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_refuses_a_playlist_a_legacy_archive_prefixed`

Old text:

```
        if mark is not None:
            raise _rename_unresolved(

```

New text:

```
        if False:
            raise _rename_unresolved(

```

### `u142.S12_undeclared_reads_as_empty`

inspiration_names: answer an empty set when no INSPIRATION folder is declared, so the wait says no playlist rather than no folder

- File: `src/cratekit/export/set_cli.py`
- Source: `u142.json`, row `S12_undeclared_reads_as_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 100 against a baseline of 100
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_taxonomy_with_no_inspiration_folder_waits_and_says_why`

Old text:

```
    if declared.inspiration is None:
        return None
    return frozenset(
```

New text:

```
    if declared.inspiration is None:
        return frozenset()
    return frozenset(
```

### `u175.R1_account_ids_unrecorded`

rotate._named_ids: read no account playlist off a native landing record, so a dated playlist is no batch and is neither rotated nor mirrored

- File: `src/cratekit/intake/rotate.py`
- Source: `u175.json`, row `R1_account_ids_unrecorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`
- Collected: 98 against a baseline of 98
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together`
  - `tests/test_intake_land_account_playlists_native.py::test_the_rotation_ages_an_account_playlist_by_its_landing_date`
  - `tests/test_organize_mirror_inbox.py::test_a_passs_dated_account_playlist_is_mirrored_beside_its_batch_under_its_dated_name`

Old text:

```
    accounts = record.detail.get(native.INBOX_PLAYLISTS_KEY)
    if isinstance(accounts, list):
```

New text:

```
    accounts = None
    if isinstance(accounts, list):
```

### `u267.M4_handle_opens_every_time`

SharedRead.handle: open again on every call, keeping the last, so the report pays an open per reader and leaks the rest

- File: `src/cratekit/core/rb_writer.py`
- Source: `u267.json`, row `M4_handle_opens_every_time`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_organize_inspiration.py`, `tests/test_organize_mirror_edits_u204.py`
- Collected: 92 against a baseline of 92
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_report_reads_inspiration_twice_through_one_handle_and_locks_nothing_meanwhile`
  - `tests/test_organize_one_read.py::test_a_failure_nobody_expected_still_closes_the_handle`
  - `tests/test_organize_one_read.py::test_a_shared_read_opens_at_its_first_read_and_once`
  - `tests/test_organize_one_read.py::test_a_step_that_refuses_after_the_open_leaves_no_handle_open`
  - `tests/test_organize_one_read.py::test_the_report_opens_the_database_once_and_closes_it_once`
  - `tests/test_organize_one_read.py::test_the_sets_step_reads_inspiration_through_the_one_handle`

Old text:

```
        if self._db is None:
            self._db = open_db(
```

New text:

```
        if True:
            self._db = open_db(
```

### `u319.M8_ok_on_any_field`

land_cli: the short path's OK offered whatever the dialog shows

- File: `src/cratekit/intake/land_cli.py`
- Source: `u319.json`, row `M8_ok_on_any_field`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_drift.py`, `tests/test_intake_land_dyn_native.py`, `tests/test_rekordbox_visit_skill.py`
- Collected: 92 against a baseline of 92
- Kills: 2 (killed)
- Killed:
  - `tests/test_drift.py::test_the_auto_analysis_step_cancels_on_any_other_field_and_leaves_dyn_to_dynamic`
  - `tests/test_drift.py::test_the_sync_stop_offers_the_auto_analysis_path_after_the_selections_it_stands_in_for`

Old text:

```
    "on its Auto Analysis dialog only when it shows every one of those Normal "
```

New text:

```
    "on its Auto Analysis dialog whatever it shows of those Normal "
```

### `u242.M8_twins_reads_the_title_alone`

twins backfill: read a downloaded custom playlist by its prefix alone, so a stripped one gets no twin

- File: `src/cratekit/sync/twins.py`
- Source: `u242.json`, row `M8_twins_reads_the_title_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_sync_twins.py`
- Collected: 92 against a baseline of 92
- Kills: 1 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_twins_reads_a_stripped_custom_playlist_as_downloaded`

Old text:

```
            if not is_taken(playlist_id, name, held):
```

New text:

```
            if not name.startswith("DOWNLOADED "):
```

### `u150.F2_record_provider`

native._record_commit: write no provider tracks on the landing's record

- File: `src/cratekit/intake/native.py`
- Source: `u150.json`, row `F2_record_provider`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`, `tests/test_organize_mirror_inbox.py`
- Collected: 90 against a baseline of 90
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_the_record_names_each_landed_rows_provider_track_for_the_account_mirror`

Old text:

```
        record.detail[label_filing.PROVIDER_KEY] = dict(labels_written.provider)
```

New text:

```
        pass
```

### `u267.M12_inspiration_set_folder_write_guard`

set_cli._inspiration_folder: drop the refusal of a shared read handed to an opener asked to write

- File: `src/cratekit/export/set_cli.py`
- Source: `u267.json`, row `M12_inspiration_set_folder_write_guard`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 88 against a baseline of 88
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_the_inspiration_opener_refuses_to_write_through_a_shared_read`

Old text:

```
    if one_read is not None and not read_only:
```

New text:

```
    if False:
```

### `u156.L25_shared_rule_near_match`

match_label_rows: file a row the batch holds only something close to, on both media

- File: `src/cratekit/intake/landing.py`
- Source: `u156.json`, row `L25_shared_rule_near_match`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_intake_land_labels_native.py`
- Collected: 85 against a baseline of 85
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_a_landed_file_at_another_version_is_a_question_and_is_not_filed`

Old text:

```
        if found.state is match.MatchState.NEEDS_REVIEW:
```

New text:

```
        if False:
```

### `u135.A14_set_order_reverses`

INBOX set-order walk appends members in reverse position order

- File: `src/cratekit/intake/native.py`
- Source: `u135.json`, row `A14_set_order_reverses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`
- Collected: 85 against a baseline of 85
- Kills: 3 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order`
  - `tests/test_u135_set_inbox_join.py::test_a_set_landed_once_keeps_one_inbox_playlist_named_for_the_set`
  - `tests/test_u135_set_inbox_join.py::test_one_landing_of_a_set_files_its_inbox_playlist_in_set_order_not_name_order`

Old text:

```
                for member in plan.set_playlist.members:

```

New text:

```
                for member in reversed(plan.set_playlist.members):

```

### `u242.M7_inspiration_reads_the_title_alone`

INSPIRATION step: read a set in a sets folder by its prefix alone, so a stripped set is shown unprefixed and never backfilled

- File: `src/cratekit/organize/inspiration.py`
- Source: `u242.json`, row `M7_inspiration_reads_the_title_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_organize_inspiration.py`
- Collected: 85 against a baseline of 85
- Kills: 1 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_the_inspiration_set_rule_reads_a_stripped_set_as_the_prefixed_one`

Old text:

```
            stripped = untaken_name(name) if is_taken(playlist_id, name, held) else ""
```

New text:

```
            stripped = untaken_name(name) if name.startswith("DOWNLOADED ") else ""
```

### `u288.M15_append_past_highest`

add_memberships: keep the binding's count plus one, so an append after a removal lands on a live row's position

- File: `src/cratekit/core/rb_writer.py`
- Source: `u288.json`, row `M15_append_past_highest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`, `tests/test_inbox_refill.py`
- Collected: 84 against a baseline of 84
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_track_added_after_a_removal_goes_past_the_highest_position`
  - `tests/test_sync_removed.py::test_two_appends_after_a_removal_each_take_the_next_position`

Old text:

```
        if added is not None and number <= highest:
```

New text:

```
        if False:
```

### `u221.R15_mark_drops_the_hold`

PairStore.mark: record no hold on a new pair, so a backfilled twin falls to the time rule

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u221.json`, row `R15_mark_drops_the_hold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 84 against a baseline of 84
- Kills: 14 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_backfilled_pair_merges_both_ways_and_queues_the_added_track_once`
  - `tests/test_sync_twins_hold.py::test_a_held_track_whose_linked_row_left_the_library_is_still_counted_and_released`
  - `tests/test_sync_twins_hold.py::test_a_landing_twin_records_an_empty_hold`
  - `tests/test_sync_twins_hold.py::test_a_name_that_is_no_twin_is_refused_and_nothing_is_planned`
  - `tests/test_sync_twins_hold.py::test_a_second_twin_stays_held_when_the_first_is_released`
  - `tests/test_sync_twins_hold.py::test_a_track_added_later_on_the_account_is_queued_and_the_held_stay_held`
  - `tests/test_sync_twins_hold.py::test_a_twin_paired_again_since_the_plan_is_left_held`
  - `tests/test_sync_twins_hold.py::test_a_twin_with_three_missing_tracks_queues_none_and_names_three_on_hold`
  - `tests/test_sync_twins_hold.py::test_an_abort_lets_nothing_go`
  - `tests/test_sync_twins_hold.py::test_release_hold_passes_over_a_pair_that_is_no_twin_and_one_holding_nothing`
  - `tests/test_sync_twins_hold.py::test_release_needs_names_or_all_and_not_both[args0]`
  - `tests/test_sync_twins_hold.py::test_release_needs_names_or_all_and_not_both[args1]`
  - `tests/test_sync_twins_hold.py::test_releasing_the_twin_queues_its_three_at_the_next_sync`
  - `tests/test_sync_twins_hold.py::test_the_hold_survives_a_recorded_snapshot_and_a_mark_of_the_same_pair`

Old text:

```
                on_hold=(
                    None
                    if on_hold is None
                    else MappingProxyType({str(k): str(v) for k, v in on_hold.items() if k})
                ),
```

New text:

```
                on_hold=None,
```

### `u113-c.C6_names_checked_after_moves`

The native landing no longer asks whether a chosen name was taken before its first move

- File: `src/cratekit/intake/landing.py`
- Source: `u113-c.json`, row `C6_names_checked_after_moves`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`
- Collected: 79 against a baseline of 79
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_name_inbox_came_to_hold_after_the_plan_is_refused_and_nothing_is_written`

Old text:

```
    native.assert_names_still_free(db, rows)
```

New text:

```
    pass
```

### `u221.R19_short_listing_records_its_misses`

pair_backfilled: record a short listing's misses as its hold, so a track the account withheld and serves later is queued with no choice

- File: `src/cratekit/sync/twins.py`
- Source: `u221.json`, row `R19_short_listing_records_its_misses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`
- Collected: 78 against a baseline of 78
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_a_short_listings_twin_records_no_hold_and_holds_a_track_served_later`

Old text:

```
                {miss.remote_id: miss.held_as() for miss in one.misses} if one.whole else None
```

New text:

```
                {miss.remote_id: miss.held_as() for miss in one.misses}
```

### `u219.K3_accept_declined`

rebuild accept: an abort records the disposition anyway

- File: `src/cratekit/cli/rebuild.py`
- Source: `u219.json`, row `K3_accept_declined`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`, `tests/test_resort_scope.py`
- Collected: 77 against a baseline of 77
- Kills: 1 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_an_aborted_acceptance_leaves_the_inbox_refusing`

Old text:

```
    if option != "accept":
```

New text:

```
    if option == "never":
```

### `u113-b.B5_export_clash_unasked`

A name the export came to hold since it was chosen is not refused before the moves

- File: `src/cratekit/intake/landing.py`
- Source: `u113-b.json`, row `B5_export_clash_unasked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_landing.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_name_the_export_came_to_hold_after_the_gate_is_refused_and_moves_nothing`

Old text:

```
    clash = sorted(set(names) & set(held))
```

New text:

```
    clash: list[str] = []
```

### `u185.G5_reading_at_open`

open_db: keep no reading of the subtree as the handle opens

- File: `src/cratekit/core/rb_writer.py`
- Source: `u185.json`, row `G5_reading_at_open`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`, `tests/test_rb_writer_db.py`
- Collected: 75 against a baseline of 75
- Kills: 20 (killed)
- Killed:
  - `tests/test_foreign_tree.py::test_a_handle_with_no_reading_at_open_refuses_rather_than_assuming_nothing_is_there`
  - `tests/test_foreign_tree.py::test_a_membership_added_to_a_pushed_playlist_is_refused`
  - `tests/test_foreign_tree.py::test_a_playlist_made_inside_the_folder_is_refused`
  - `tests/test_foreign_tree.py::test_a_playlist_of_ones_own_moved_into_the_folder_is_refused`
  - `tests/test_foreign_tree.py::test_a_position_named_at_the_top_moves_the_folder_and_is_refused`
  - `tests/test_foreign_tree.py::test_a_push_that_lands_while_a_handle_is_open_refuses_that_handles_commit`
  - `tests/test_foreign_tree.py::test_a_pushed_membership_rewritten_to_another_owner_is_refused`
  - `tests/test_foreign_tree.py::test_a_pushed_playlist_moved_out_of_the_folder_is_refused`
  - `tests/test_foreign_tree.py::test_a_second_folder_of_the_name_at_the_top_is_refused`
  - `tests/test_foreign_tree.py::test_a_write_beside_the_folder_commits_and_leaves_every_row_the_push_wrote`
  - `tests/test_foreign_tree.py::test_raw_sql_into_the_folder_is_seen_by_the_reading_again_from_sql`
  - `tests/test_foreign_tree.py::test_the_reading_at_open_names_the_push_and_not_a_namesake_below_the_top`
  - `tests/test_rb_writer_db.py::test_a_playlist_creation_commits_because_the_table_is_whitelisted`
  - `tests/test_rb_writer_db.py::test_a_registered_column_write_commits_and_persists`
  - `tests/test_rb_writer_db.py::test_a_registration_widens_the_gate_by_exactly_its_own_fields`
  - ... and 5 more, see the JSON sidecar

Old text:

```
    foreign_tree.remember(db)
    return db
```

New text:

```
    return db
```

### `u130-c.C5_no_renumber`

Leave rekordbox's order as the adds and removals left it

- File: `src/cratekit/write/playlist_pair.py`
- Source: `u130-c.json`, row `C5_no_renumber`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 75 against a baseline of 75
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_track_added_on_the_account_only_lands_in_rekordbox_in_place`
  - `tests/test_sync_pair.py::test_the_first_sync_marks_the_pair_and_adds_only`
  - `tests/test_sync_pair.py::test_when_both_sides_reorder_the_account_order_wins`

Old text:

```
            moved = renumber(db, change.playlist_id, change.order)
```

New text:

```
            moved = 0
```

### `u243.L7_kept_read_judged_blind`

KeptReads._is_fresh: a kept read without the tracks' words is reused and judged without them

- File: `src/cratekit/label/kept_reads.py`
- Source: `u243.json`, row `L7_kept_read_judged_blind`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tombstoned.py`, `tests/test_label_playlists_kept.py`
- Collected: 74 against a baseline of 74
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_tombstoned.py::test_a_kept_read_missing_any_track_word_is_read_again[no-artist]`
  - `tests/test_label_tombstoned.py::test_a_kept_read_missing_any_track_word_is_read_again[no-title]`
  - `tests/test_label_tombstoned.py::test_a_kept_read_missing_any_track_word_is_read_again[one-track-unnamed]`
  - `tests/test_label_tombstoned.py::test_a_kept_read_written_without_the_words_is_read_again`

Old text:

```
        return timedelta(0) <= age < KEPT_FOR and kept.named
```

New text:

```
        return timedelta(0) <= age < KEPT_FOR
```

### `u166.R2_rotate_reserved`

_classify: let the rotation take Analyze for a batch

- File: `src/cratekit/intake/rotate.py`
- Source: `u166.json`, row `R2_rotate_reserved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_the_rotation_never_takes_analyze_for_a_batch_whatever_a_record_says`

Old text:

```
    if not in_old and name == native.ANALYZE:
```

New text:

```
    if False:
```

### `u130-c.C6_pair_not_vouched`

The account seam refuses a removal from a paired playlist

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u130-c.json`, row `C6_pair_not_vouched`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_account.py`, `tests/test_prune.py`
- Collected: 73 against a baseline of 73
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair_account.py::test_a_move_that_landed_elsewhere_is_left_to_the_settle_reading_with_every_track_kept`
  - `tests/test_sync_pair_account.py::test_a_paired_playlist_takes_a_removal`
  - `tests/test_sync_pair_account.py::test_a_track_held_twice_is_not_moved`
  - `tests/test_sync_pair_account.py::test_an_order_already_standing_sends_nothing`
  - `tests/test_sync_pair_account.py::test_the_order_moves_each_track_to_the_front_and_reads_back`

Old text:

```
            ledger.product_made(self._cfg, identifier) or pairs.paired(self._cfg, identifier)
```

New text:

```
            ledger.product_made(self._cfg, identifier)
```

### `u246.S16_inspiration_held_per_element`

assert_read_back (inspiration): build the live set once per planned row again (the shape on main)

- File: `src/cratekit/organize/inspiration.py`
- Source: `u246.json`, row `S16_inspiration_held_per_element`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_comprehension_sets.py`, `tests/test_organize_inspiration.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_comprehension_sets.py::test_no_comprehension_in_the_package_rebuilds_an_invariant_set_per_element`

Old text:

```
        missing = [row for row in one.members if row not in held]
```

New text:

```
        missing = [row for row in one.members if row not in set(live)]
```

### `u119.G16_read_back_blind_to_leftovers`

_read_back: a track still in Favorites after the removals is not a disagreement

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G16_read_back_blind_to_leftovers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if removed_too and live - wanted:
```

New text:

```
        if False:
```

### `u164.W2_preflight_target`

apply_native: check the library against the music folder rather than the chosen folder

- File: `src/cratekit/intake/landing.py`
- Source: `u164.json`, row `W2_preflight_target`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_intake_land_filed.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_filed_folder_on_another_device_is_refused_at_the_move`

Old text:

```
    preflight_native(plan, cfg=cfg, target=target)
```

New text:

```
    preflight_native(plan, cfg=cfg)
```

### `u150.L1_forget_checks_id`

ledger.forget_mirror_playlist: drop the identifier check, so a playlist recorded under the title since is forgotten in its place

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u150.json`, row `L1_forget_checks_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_forgetting_a_mirrored_playlist_drops_only_the_record_of_that_identifier`

Old text:

```
        if not entry or str(entry.get("remote_id") or "") != str(remote_id):
            return
```

New text:

```
        if not entry:
            return
```

### `u145.M4_states_carried_only`

carried_hearts: states=None still reads only the carried states, so an owned row dates nothing

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u145.json`, row `M4_states_carried_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`, `tests/test_favorites_backfill.py`
- Collected: 64 against a baseline of 64
- Kills: 8 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_and_undated_holds_is_not_given_a_month`
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_at_the_root_beside_another_playlist_still_takes_its_month`
  - `tests/test_favorites_backfill.py::test_a_heart_its_job_dated_nowhere_stays_undated_though_the_account_dates_it_now`
  - `tests/test_favorites_backfill.py::test_a_heart_put_back_by_hand_after_a_removal_takes_its_month_and_is_not_taken_back`
  - `tests/test_favorites_backfill.py::test_an_owned_heart_in_a_batch_folder_is_placed_beside_a_downloaded_one`
  - `tests/test_favorites_backfill.py::test_an_owned_heart_the_source_system_filed_is_placed_and_one_with_no_row_is_not`
  - `tests/test_favorites_backfill.py::test_owned_hearts_not_in_all_favorites_are_planned_by_month_and_those_taken_back_are_named`
  - `tests/test_favorites_split.py::test_a_job_row_owned_when_its_job_ran_still_dates_the_member`

Old text:

```
        if states is not None and report.get("state") not in states:
```

New text:

```
        if report.get("state") not in (states or CARRIED_STATES):
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

### `u267.M11_rotation_opens_its_own`

rotate_cli.planned: ignore the shared read and open its own handle, a second open in the report

- File: `src/cratekit/intake/rotate_cli.py`
- Source: `u267.json`, row `M11_rotation_opens_its_own`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_inbox_rotate.py`
- Collected: 56 against a baseline of 56
- Kills: 4 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_a_failure_nobody_expected_still_closes_the_handle`
  - `tests/test_organize_one_read.py::test_a_step_that_refuses_after_the_open_leaves_no_handle_open`
  - `tests/test_organize_one_read.py::test_the_report_opens_the_database_once_and_closes_it_once`
  - `tests/test_organize_one_read.py::test_the_sets_step_reads_inspiration_through_the_one_handle`

Old text:

```
    db = (
        one_read.handle()
        if one_read is not None
        else rb_writer.open_db(
```

New text:

```
    one_read = None
    db = (
        one_read.handle()
        if one_read is not None
        else rb_writer.open_db(
```

### `u113-a.A2_queue_order`

The account playlists are taken newest job first, the order the store lists them

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u113-a.json`, row `A2_queue_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        queued = sorted(
            batch_name.pass_jobs(cfg, pass_name), key=lambda job: (job.created, job.job_id)
        )
```

New text:

```
        queued = batch_name.pass_jobs(cfg, pass_name)
```

