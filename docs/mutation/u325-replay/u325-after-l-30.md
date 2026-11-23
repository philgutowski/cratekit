# Mutation table: u325-after-l-30

Measured by `scripts/mutate.py` on 2026-11-22 23:47 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 142.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:22 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 63, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u293.S1_reentrant` | `src/cratekit/core/staging_lock.py` | user | 4 file(s) | 237 | 6 | killed |
| `r744.B1_window_not_bound` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 237 | 1 | killed |
| `r1255.F2_refill_warning_wording` | `src/cratekit/intake/refill_cli.py` | user | 2 file(s) | 43 | 2 | killed |
| `r235-b.M22_nested_namesake_is_a_root` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 40 | 2 | killed |
| `r235-b.M23_playlist_is_a_root` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 40 | 1 | killed |
| `r290-author.R1_retag_rebuild_drops_the_type` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 228 | 2 | killed |
| `r1313.T1_account_skips_the_classifier` | `src/cratekit/modules/outbound/tidal_account.py` | user | 3 file(s) | 227 | 5 | killed |
| `u216.M25_dated_no_time` | `src/cratekit/modules/outbound/tidal_account.py` | user | 3 file(s) | 227 | 1 | killed |
| `u153.L1_facts_colour_count` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 37 | 1 | killed |
| `u153.N1_restamp_id_text` | `src/cratekit/intake/native.py` | user | 2 file(s) | 37 | 9 | killed |
| `u102-a.D1_keep_is_not_accept` | `src/cratekit/intake/repair.py` | user | 2 file(s) | 35 | 1 | killed |
| `u102-a.D2_open_is_not_accepted` | `src/cratekit/intake/repair.py` | user | 2 file(s) | 35 | 1 | killed |
| `u192.T4_tag_queue_only_ignored` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 221 | 7 | killed |
| `u219-composites.G6_answer_pinned` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 221 | 1 | killed |
| `u173.M21_gate_name` | `src/cratekit/intake/analyzed_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `u173.M24_analyze_name` | `src/cratekit/intake/native.py` | user | 1 file(s) | 33 | 1 | killed |
| `r685-a.V1_route_inbox_export_reads_the_shipped_text` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 215 | 4 | killed |
| `u179.T4_commands_quoted` | `src/cratekit/cli/tail.py` | user | 4 file(s) | 215 | 3 | killed |
| `u181.T1_rescore_ignores_unable` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 215 | 4 | killed |
| `u181.T2_rescore_ignores_profile` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 215 | 30 | killed |
| `u261.H8_blob_is_the_stored_not_the_refresh` | `src/cratekit/acquire/provider_session.py` | maintainer | 1 file(s) | 30 | 1 | killed |
| `u261.R5_drop_not_by_identity` | `src/cratekit/acquire/provider_session.py` | maintainer | 1 file(s) | 30 | 2 | killed |
| `u261.H1_reuse_skips_the_gate` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 213 | 1 | killed |
| `u157.A1_no_level_tag` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 212 | 1 | killed |
| `u177.A6_first_of_two` | `src/cratekit/label/registry.py` | user | 6 file(s) | 190 | 2 | killed |
| `r685-b.P1_place_files_rereads_the_registry` | `src/cratekit/intake/ingest.py` | maintainer | 1 file(s) | 27 | 1 | killed |
| `r685-a.V2_composite_a_landing_under_an_alias` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 27 | 1 | killed |
| `r290-author.S06_label_call_removed` | `src/cratekit/label/cli.py` | user | 2 file(s) | 208 | 17 | killed |
| `u157.L1_selection_counts` | `src/cratekit/intake/land_cli.py` | user | 5 file(s) | 208 | 1 | killed |
| `u261.O2_account_drops_the_app` | `src/cratekit/modules/outbound/tidal_account.py` | user | 3 file(s) | 207 | 2 | killed |
| `u207.A2_catalogue_ignores_screen` | `src/cratekit/label/tidal_catalogue.py` | user | 2 file(s) | 206 | 1 | killed |
| `u47-author.CODEC_refused_track_sinks_the_run` | `src/cratekit/acquire/adapter.py` | user | 2 file(s) | 201 | 2 | killed |
| `u270.J5_declined_outcome` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 20 | 1 | killed |
| `u270.J9_outcome_type_check` | `src/cratekit/core/jobs.py` | maintainer | 1 file(s) | 20 | 1 | killed |
| `u181.L1_half_is_a_warning` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 20 | 1 | killed |
| `u181.L2_coefficient` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 20 | 1 | killed |
| `u233.C1_schema_default_moves` | `src/cratekit/core/config.py` | user | 1 file(s) | 19 | 1 | killed |
| `u233.C2_schema_gains_a_key` | `src/cratekit/core/config.py` | user | 1 file(s) | 19 | 1 | killed |
| `u142.S11_read_handle_requires_closed` | `src/cratekit/export/set_cli.py` | user | 3 file(s) | 22933 | 0 (promoted) | zero |
| `u260.E1_engine_encodes_per_file` | `src/cratekit/tagging/tag.py` | user | 3 file(s) | 196 | 8 | killed |
| `r290-author.S02_acquire_download_call_removed` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 195 | 11 | killed |
| `u100-c.C8_refused_counted_present_after_fix` | `src/cratekit/label/cli.py` | user | 1 file(s) | 16 | 1 | killed |
| `u100-c.R5_adopt_always_writes_after_fix` | `src/cratekit/label/registry.py` | user | 1 file(s) | 16 | 1 | killed |
| `u242.M22_unmark_releases_nothing` | `src/cratekit/sync/unmark_cli.py` | user | 4 file(s) | 190 | 7 | killed |
| `u246.S2_adapter_per_element` | `src/cratekit/acquire/adapter.py` | maintainer | 2 file(s) | 190 | 1 | killed |
| `r598-b.B7_sample_live_holder_released` | `src/cratekit/core/session.py` | user | 2 file(s) | 185 | 4 | killed |
| `u164.T4_undated_name` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 10 | 2 | killed |
| `u164.T7_reuse_gone` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 10 | 1 | killed |
| `u319.M10_sync_stop_drops_the_short_path` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 183 | 1 | killed |
| `r1264.M22_readable_dates` | `src/cratekit/intake/cli.py` | user | 4 file(s) | 182 | 6 | killed |
| `u27-adopt-apply-author.S2_analysis_watch_watches_nothing` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 175 | 2 | killed |
| `u261.R4_forbidden_not_a_refusal` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 174 | 4 | killed |
| `u84-b.T4_default_unchecked` | `src/cratekit/tagging/tag.py` | maintainer | 2 file(s) | 172 | 1 | killed |
| `r759.A1_deadline_asked_only_at_the_end` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 1 | 1 | killed |
| `r759.A2_deadline_a_second_late` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 1 | 1 | killed |
| `r759-b.P4_lock_removed_r01` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 1 | 1 | killed |
| `r759.P5_lock_shared` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 1 | 1 | killed |
| `r759.P1_interval_dropped` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 1 | 1 | killed |
| `r759.P6_wait_skipped_stamp_kept` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 1 | 1 | killed |
| `r1255.S7_log_unlisted_predicate` | `src/cratekit/core/session.py` | user | 4 file(s) | 169 | 13 | killed |
| `u249.M21_intake_reset_leaves_reader` | `src/cratekit/intake/cli.py` | maintainer | 3 file(s) | 169 | 1 | killed |
| `u270.J7_raise_is_every_outcome` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 167 | 3 | killed |
| `r788-d.A5_move_worker_reads_vocals` | `src/cratekit/adopt/move_cli.py` | maintainer | 2 file(s) | 166 | 1 | killed |
| `u198.P2_release_side` | `src/cratekit/modules/outbound/pairs.py` | user | 3 file(s) | 166 | 3 | killed |
| `u156.L24_label_on_the_bridge` | `src/cratekit/intake/land_cli.py` | user | 3 file(s) | 165 | 2 | killed |
| `r380.G5_permanent_failures_still_offer_resume` | `src/cratekit/core/jobs.py` | user | 2 file(s) | 164 | 5 | killed |
| `u37-author-light.G5_path_repair_queue` | `src/cratekit/intake/repair.py` | user | 2 file(s) | 164 | 3 | killed |
| `r501-b.L1_unretired_name` | `src/cratekit/intake/land_cli.py` | user | 3 file(s) | 164 | 3 | killed |
| `r682-a.M1_no_by_reason_in_summary` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 163 | 4 | killed |
| `u202-composites.P1_reserve_held` | `src/cratekit/modules/outbound/pairs.py` | user | 3 file(s) | 158 | 1 | killed |
| `u270.A1_failed_attempt_reopens` | `src/cratekit/modules/outbound/tidal_account.py` | user | 3 file(s) | 157 | 2 | killed |
| `u142.S10_gate_folder_item_named_by_year` | `src/cratekit/export/set_cli.py` | user | 2 file(s) | 156 | 1 | killed |
| `u111-b.B1_move_names_every_table` | `src/cratekit/write/trees.py` | user | 2 file(s) | 153 | 1 | killed |
| `r1103.H1_item_not_failed` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 3 | killed |
| `r746-b.N9_placement_check_dropped_from_the_screen` | `src/cratekit/intake/landing.py` | user | 3 file(s) | 151 | 3 | killed |
| `u164.T1_filed_target` | `src/cratekit/intake/shelve.py` | user | 4 file(s) | 148 | 57 | killed |
| `u261.H5_settings_not_in_the_key` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 147 | 1 | killed |

## Zero rows and what they owe

- `u142.S11_read_handle_requires_closed` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `u293.S1_reentrant`

held: a process holding the lock takes it again on a second descriptor and refuses itself

- File: `src/cratekit/core/staging_lock.py`
- Source: `u293.json`, row `S1_reentrant`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_staging_lock.py`, `tests/test_sync_night.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 237 against a baseline of 237
- Kills: 6 (killed)
- Killed:
  - `tests/test_staging_lock.py::test_one_process_holds_it_again_by_count_and_releases_at_the_outermost`
  - `tests/test_sync_night.py::test_a_night_pass_reaches_the_landing_gate_and_answers_nothing_but_the_name_confirm`
  - `tests/test_sync_night.py::test_a_night_pass_that_needs_the_acknowledgment_stops_there_and_mints_none`
  - `tests/test_sync_night.py::test_a_night_pass_the_vocal_model_cannot_score_waits_at_that_gate_and_queues_nothing`
  - `tests/test_sync_night.py::test_a_refused_firing_keeps_the_pass_waiting_at_its_gate`
  - `tests/test_sync_night.py::test_a_track_the_download_refused_is_named_in_the_record`

Old text:

```
    if _HANDLE is not None:
```

New text:

```
    if False:
```

### `r744.B1_window_not_bound`

the run binds the shipped window rather than the configured one, so analysis.tempo_floor and tempo_ceiling change nothing

- File: `src/cratekit/analysis/cli.py`
- Source: `r744.json`, row `B1_window_not_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_head_agreement.py`, `tests/test_analysis_workers.py`
- Collected: 237 against a baseline of 237
- Kills: 1 (killed)
- Killed:
  - `tests/test_head_agreement.py::test_a_raised_window_loads_and_reaches_the_detector_binding`

Old text:

```
            tempo_window=(cfg.analysis.tempo_floor, cfg.analysis.tempo_ceiling),
```

New text:

```
            tempo_window=(80, 160),
```

### `r1255.F2_refill_warning_wording`

warnings_of: word an unlisted log as a count of records

- File: `src/cratekit/intake/refill_cli.py`
- Source: `r1255.json`, row `F2_refill_warning_wording`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_refill.py`
- Collected: 43 against a baseline of 43
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_session_log_that_cannot_be_listed_is_named_as_one_by_the_plan`
  - `tests/test_session_log_unlisted.py::test_the_refill_warns_on_a_log_it_could_not_list`

Old text:

```
                        if plan.log_unlisted
```

New text:

```
                        if False
```

### `r235-b.M22_nested_namesake_is_a_root`

a folder of the tree's name anywhere in the library is a candidate root

- File: `src/cratekit/core/rb_writer.py`
- Source: `r235-b.json`, row `M22_nested_namesake_is_a_root`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_a_namesake_nested_under_another_folder_is_not_a_root`
  - `tests/test_cutover_cli.py::test_a_nested_namesake_alone_is_no_root_at_all`

Old text:

```
        if _is_folder(playlist)
        and str(getattr(playlist, "ParentID", "")) in ROOT_PARENT_SENTINELS
```

New text:

```
        if _is_folder(playlist)
```

### `r235-b.M23_playlist_is_a_root`

a playlist of the tree's name under the playlist root is a candidate root

- File: `src/cratekit/core/rb_writer.py`
- Source: `r235-b.json`, row `M23_playlist_is_a_root`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_a_playlist_of_the_trees_name_is_not_a_root`

Old text:

```
        if _is_folder(playlist)
        and str(getattr(playlist, "ParentID", "")) in ROOT_PARENT_SENTINELS
```

New text:

```
        if str(getattr(playlist, "ParentID", "")) in ROOT_PARENT_SENTINELS
```

### `r290-author.R1_retag_rebuild_drops_the_type`

Rebuild the retag refusal as a plain CratekitError again, so a retag parked after correcting a file says failed

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r290-author.json`, row `R1_retag_rebuild_drops_the_type`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_tag_workers.py`
- Collected: 228 against a baseline of 228
- Kills: 2 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_reworded_refusal_is_rebuilt_in_one_place_only`
  - `tests/test_tag_workers.py::test_a_parked_retag_keeps_both_the_block_and_the_reload`

Old text:

```
    return rebuilt(
        error,
        replace(
```

New text:

```
    return CratekitError(
        replace(
```

### `r1313.T1_account_skips_the_classifier`

tidal_account._not_found: read the class names alone and stop asking classify_unavailable, so a 404 the account reads by status is retried

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1313.json`, row `T1_account_skips_the_classifier`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_isrc_cache.py`, `tests/test_outbound_tidal_account.py`
- Collected: 227 against a baseline of 227
- Kills: 5 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_404_status_is_kept_as_a_not_found_at_either_seam[account]`
  - `tests/test_provider_not_found_bodies.py::test_a_404_is_a_not_found_whatever_its_body[404-html-account]`
  - `tests/test_provider_not_found_bodies.py::test_a_rewrapped_404_page_is_a_not_found[account]`
  - `tests/test_provider_not_found_bodies.py::test_an_isrc_answered_by_a_404_page_is_asked_once_and_kept[account]`
  - `tests/test_provider_not_found_bodies.py::test_off_the_declared_chain_a_links_cause_is_nearer_than_what_it_was_handling`

Old text:

```
    return classify_unavailable(exc) is TrackOutcome.UNAVAILABLE_PERMANENT

```

New text:

```
    return False

```

### `u216.M25_dated_no_time`

folder_playlists_dated: every playlist reads as made at no known time

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u216.json`, row `M25_dated_no_time`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_adopted.py`, `tests/test_outbound_tidal_account.py`, `tests/test_adapter_listing.py`
- Collected: 227 against a baseline of 227
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_the_dated_folder_read_gives_each_playlists_creation_time_from_the_same_pages`

Old text:

```
                made if isinstance(made, datetime) else None,
```

New text:

```
                None,
```

### `u153.L1_facts_colour_count`

land_cli favorites_facts: count only the items, so the owned hearts are left out of the Pink total shown

- File: `src/cratekit/intake/land_cli.py`
- Source: `u153.json`, row `L1_facts_colour_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_beside_a_landed_file_takes_pink_in_the_same_commit`

Old text:

```
        facts["rows to colour Pink"] = len(plan.items) + len(plan.colour)
```

New text:

```
        facts["rows to colour Pink"] = len(plan.items)
```

### `u153.N1_restamp_id_text`

native _restamp: do not coerce the minted ID to text, so a colour on an existing row cannot flush beside a new one

- File: `src/cratekit/intake/native.py`
- Source: `u153.json`, row `N1_restamp_id_text`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 37 against a baseline of 37
- Kills: 9 (killed)
- Killed:
  - `tests/test_intake_land_hearts_native.py::test_a_heart_a_playlist_also_asked_for_is_in_that_playlist_and_in_all_favorites`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_whose_job_froze_no_date_key_joins_all_favorites_and_no_month`
  - `tests/test_intake_land_hearts_native.py::test_a_hearted_file_lands_in_its_batch_all_favorites_and_a_month_made_for_it`
  - `tests/test_intake_land_hearts_native.py::test_a_source_at_the_root_takes_its_months_beside_it`
  - `tests/test_intake_land_hearts_native.py::test_an_undated_heart_lands_in_the_undated_playlist`
  - `tests/test_intake_land_hearts_native.py::test_the_record_carries_the_hearts_placed_under_their_own_key`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_beside_a_landed_file_takes_pink_in_the_same_commit`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_beside_a_landed_file_that_is_no_heart`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_in_the_same_commit_as_a_downloaded_one`

Old text:

```
    content.ID = str(content.ID)
```

New text:

```
    content.ID = content.ID
```

### `u102-a.D1_keep_is_not_accept`

decided(): read the accepted verdict alone, so an item answered keep is treated as a rename to apply

- File: `src/cratekit/intake/repair.py`
- Source: `u102-a.json`, row `D1_keep_is_not_accept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/intake/test_repair.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_an_open_or_rejected_or_kept_proposal_is_untouched`

Old text:

```
        elif item.option != ACCEPT:
            kept += 1
```

New text:

```
        elif item.option is None:
            kept += 1
```

### `u102-a.D2_open_is_not_accepted`

decided(): drop the branch that counts an item with no accepted verdict as open

- File: `src/cratekit/intake/repair.py`
- Source: `u102-a.json`, row `D2_open_is_not_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/intake/test_repair.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_an_open_or_rejected_or_kept_proposal_is_untouched`

Old text:

```
        elif item.verdict is not Verdict.ACCEPTED:
            still_open += 1
```

New text:

```
        elif False:
            still_open += 1
```

### `u192.T4_tag_queue_only_ignored`

tag_folder: ignore --queue-only and drive the sweep

- File: `src/cratekit/tagging/cli.py`
- Source: `u192.json`, row `T4_tag_queue_only_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_label_genre.py`, `tests/test_render_payloads.py`
- Collected: 221 against a baseline of 221
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_genre.py::test_an_unreadable_registry_warns_and_refuses_only_a_sweep_that_named_a_label`
  - `tests/test_label_genre.py::test_the_remedy_names_the_label_by_its_identifier`
  - `tests/test_render_payloads.py::test_a_builder_that_raises_leaves_the_queued_verb_a_success`
  - `tests/test_tag_workers.py::test_a_file_removed_between_the_queueing_and_the_drive_is_refused_by_name`
  - `tests/test_tag_workers.py::test_a_real_track_beside_the_staging_tree_is_still_queued`
  - `tests/test_tag_workers.py::test_queueing_a_folder_names_the_job_and_the_command_that_drives_it`
  - `tests/test_tag_workers.py::test_tag_folder_queue_only_returns_the_sweep_queued_with_nothing_asked`

Old text:

```
        if foreground.queue_only(ctx.args):
```

New text:

```
        if False:
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

### `u173.M21_gate_name`

analyzed_cli: the clear's gate renamed, so the skill's decide line names a gate that does not exist

- File: `src/cratekit/intake/analyzed_cli.py`
- Source: `u173.json`, row `M21_gate_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rekordbox_visit_skill.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_rekordbox_visit_skill.py::test_the_clear_s_gate_is_answered_by_its_own_name_and_option`

Old text:

```
APPROVE_GATE = "inbox.analyzed.approve"
```

New text:

```
APPROVE_GATE = "inbox.analyzed.confirm"
```

### `u173.M24_analyze_name`

native: the queue playlist renamed, so the skill sends a session to a playlist no landing fills

- File: `src/cratekit/intake/native.py`
- Source: `u173.json`, row `M24_analyze_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rekordbox_visit_skill.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_rekordbox_visit_skill.py::test_it_selects_the_playlist_every_landing_fills`

Old text:

```
ANALYZE = "Analyze"
```

New text:

```
ANALYZE = "Analysis"
```

### `r685-a.V1_route_inbox_export_reads_the_shipped_text`

The export routing verb parses the shipped text instead of loading the library's copy

- File: `src/cratekit/write/routing_cli.py`
- Source: `r685-a.json`, row `V1_route_inbox_export_reads_the_shipped_text`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_active_taxonomy.py`, `tests/test_routing_workers.py`
- Collected: 215 against a baseline of 215
- Kills: 4 (killed)
- Killed:
  - `tests/test_active_taxonomy.py::test_no_module_but_the_loader_reads_the_shipped_template`
  - `tests/test_routing_workers.py::test_a_calibrated_export_over_a_taxonomy_with_no_vocal_sub_creates_none`
  - `tests/test_routing_workers.py::test_a_template_declaring_no_long_track_playlist_builds_none`
  - `tests/test_routing_workers.py::test_an_edit_to_the_active_copy_is_the_playlist_the_routing_plan_names`

Old text:

```
    declared = active_taxonomy.load(cfg)
    _refuse_off_the_bridge(
        cfg, declared, export, instead="run route inbox without --export, which "

```

New text:

```
    declared = taxonomy.load_taxonomy(taxonomy.shipped_template_text("default"))
    _refuse_off_the_bridge(
        cfg, declared, export, instead="run route inbox without --export, which "

```

### `u179.T4_commands_quoted`

attended: join the step's command with plain spaces, so a batch folder with a space cannot be pasted

- File: `src/cratekit/cli/tail.py`
- Source: `u179.json`, row `T4_commands_quoted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 215 against a baseline of 215
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_failed_rehearsal_plans_no_live_landing`
  - `tests/test_sync_bandcamp.py::test_a_rehearsal_that_needs_the_acknowledgment_names_the_rehearsal_then_the_landing`
  - `tests/test_sync_bandcamp_native.py::test_one_new_puls_release_and_one_owned_land_one_batch_filed_under_its_label`

Old text:

```
    command = shlex.join(stop.argv)
```

New text:

```
    command = " ".join(stop.argv)
```

### `u181.T1_rescore_ignores_unable`

tail.rescore: queue the rescore although the model cannot score here

- File: `src/cratekit/cli/tail.py`
- Source: `u181.json`, row `T1_rescore_ignores_unable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 215 against a baseline of 215
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_over_two_answered_releases_runs_the_tail_in_order_and_stops_at_the_landing_gate`
  - `tests/test_sync_land.py::test_the_answered_gate_takes_the_pass_on_and_the_summary_says_vocals_were_skipped`
  - `tests/test_sync_land.py::test_the_tail_asks_the_vocal_model_before_analyze_run_binds_its_loader`
  - `tests/test_vocals_cli.py::test_the_tails_rescore_asks_nothing_of_a_model_that_cannot_score`

Old text:

```
    if unable is not None:
        chain.summary["vocal_rescore"] = "skipped"
```

New text:

```
    if False:
        chain.summary["vocal_rescore"] = "skipped"
```

### `u181.T2_rescore_ignores_profile`

tail.rescore: run the vocals verb on a profile with the vocals module off

- File: `src/cratekit/cli/tail.py`
- Source: `u181.json`, row `T2_rescore_ignores_profile`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_label_sync_go.py`, `tests/test_vocals_cli.py`
- Collected: 215 against a baseline of 215
- Kills: 30 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_cancelled_download_over_the_same_list_is_not_reused`
  - `tests/test_sync_land.py::test_a_continued_pass_drives_the_download_it_queued_and_queues_no_second`
  - `tests/test_sync_land.py::test_a_continued_pass_never_drives_a_cancelled_job_and_lists_the_rest`
  - `tests/test_sync_land.py::test_a_continued_pass_over_an_open_intake_job_drives_it_first`
  - `tests/test_sync_land.py::test_a_continued_pass_refused_while_rekordbox_runs_names_the_way_back`
  - `tests/test_sync_land.py::test_a_continued_pass_retries_a_download_that_failed_transiently`
  - `tests/test_sync_land.py::test_a_fresh_pass_never_reuses_another_lists_download_job`
  - `tests/test_sync_land.py::test_a_gate_any_earlier_step_stops_at_is_the_steps_own_not_the_passes`
  - `tests/test_sync_land.py::test_a_landing_that_needs_the_backup_acknowledgment_stops_without_minting_one`
  - `tests/test_sync_land.py::test_a_name_apply_refusal_ends_the_pass_before_the_landing`
  - `tests/test_sync_land.py::test_a_pass_continued_by_its_land_run_id_reaches_the_same_jobs_as_by_its_pass_id`
  - `tests/test_sync_land.py::test_a_pass_queued_by_hand_and_never_driven_is_the_one_this_verb_takes`
  - `tests/test_sync_land.py::test_a_profile_with_the_vocals_module_off_is_not_asked`
  - `tests/test_sync_land.py::test_a_refused_id_names_the_land_run_recorded_beside_each_pass`
  - `tests/test_sync_land.py::test_a_run_interrupted_after_sync_all_continues_by_its_own_id`
  - ... and 15 more, see the JSON sidecar

Old text:

```
    if not vocals_on(cfg):
        chain.summary["vocal_rescore"] = "off"
```

New text:

```
    if False:
        chain.summary["vocal_rescore"] = "off"
```

### `u261.H8_blob_is_the_stored_not_the_refresh`

_login: report the session read rather than the refresh written back, so a refreshed login reads as replaced on every reuse and logs in again

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `H8_blob_is_the_stored_not_the_refresh`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`
- Collected: 30 against a baseline of 30
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

### `u261.R5_drop_not_by_identity`

drop: drop whatever is held, so a stale client's refusal throws away the newer session logged in since

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `R5_drop_not_by_identity`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`
- Collected: 30 against a baseline of 30
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

### `u157.A1_no_level_tag`

_finalize: write no driftlevel tag

- File: `src/cratekit/analysis/cli.py`
- Source: `u157.json`, row `A1_no_level_tag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_drift.py`, `tests/test_analysis_workers.py`
- Collected: 212 against a baseline of 212
- Kills: 1 (killed)
- Killed:
  - `tests/test_drift.py::test_a_measured_drift_is_written_as_its_level_and_verdict`

Old text:

```
        "driftlevel": _drift_level(scored.get("drift")),
```

New text:

```
        "driftlevel": None,
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

### `r685-b.P1_place_files_rereads_the_registry`

place_files ignores the registry the landing handed it and reads its own after the moves

- File: `src/cratekit/intake/ingest.py`
- Source: `r685-b.json`, row `P1_place_files_rereads_the_registry`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_the_registry_is_read_before_the_first_move_and_never_after`

Old text:

```
    if registry is None:
        registry = tree_registry.read(cfg)

```

New text:

```
    registry = tree_registry.read(cfg)

```

### `r685-a.V2_composite_a_landing_under_an_alias`

What V2 holds without the guard's spelling: an aliased default loader at the preflight

- File: `src/cratekit/intake/landing.py`
- Source: `r685-a.json`, row `V2_composite_a_landing_under_an_alias`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_an_undeclared_catalog_tree_refuses_before_any_file_moves`

Old text:

```
    checked = Checked(registry=tree_registry.read(cfg), declared=active_taxonomy.load(cfg))

```

New text:

```
    from cratekit.core.taxonomy import default_taxonomy as shipped

    checked = Checked(registry=tree_registry.read(cfg), declared=shipped())

```

### `r290-author.S06_label_call_removed`

Remove the one jobs.raise_for_state call from label/cli.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/label/cli.py`
- Source: `r290-author.json`, row `S06_label_call_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_label_workers.py`
- Collected: 208 against a baseline of 208
- Kills: 17 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[label.import]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[sync.labels]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[label.import]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[sync.labels]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[label.import]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[sync.labels]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[label.import]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[sync.labels]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[label.import]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[sync.labels]`
  - `tests/test_job_outcome.py::test_every_function_that_drives_a_job_maps_its_ending_afterwards`
  - `tests/test_label_workers.py::test_a_label_the_registry_no_longer_holds_refuses_rather_than_sweeping_nothing`
  - `tests/test_label_workers.py::test_a_rate_limited_listing_fails_its_item_as_retryable_and_the_job_says_resume`
  - `tests/test_label_workers.py::test_a_resume_of_a_cancelled_sweep_does_not_exit_ok_over_the_items_it_never_ran`
  - `tests/test_label_workers.py::test_a_resumed_job_rearms_the_rate_limited_label_and_not_the_settled_one`
  - ... and 2 more, see the JSON sidecar

Old text:

```
jobs.raise_for_state(job)
```

New text:

```
jobs.get  # the mapping call, removed
```

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

### `u47-author.CODEC_refused_track_sinks_the_run`

Escalate a lossy landing to an adapter failure, the shape that raises an uncaught ValueError when a delisted track landed earlier in the same batch

- File: `src/cratekit/acquire/adapter.py`
- Source: `u47-author.json`, row `CODEC_refused_track_sinks_the_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 201 against a baseline of 201
- Kills: 2 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_lossy_landing_after_a_delisted_track_still_returns_a_contract_result`
  - `tests/test_adapter_contract.py::test_a_lossy_landing_refuses_the_track_and_lets_the_run_continue`

Old text:

```
        return TrackResult(
            key=request.key,
            outcome=TrackOutcome.REFUSED_BY_POLICY,
            detail=str(exc),
            remedy=exc.remedy,
        )
```

New text:

```
        raise AdapterBroken(str(exc)) from exc
```

### `u270.J5_declined_outcome`

drive: settle a declined outcome as failed, so a batch item the worker declined fails the job

- File: `src/cratekit/core/jobs.py`
- Source: `u270.json`, row `J5_declined_outcome`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs_batch.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs_batch.py::test_each_outcome_settles_its_own_item`

Old text:

```
                    if isinstance(outcome, Declined):
```

New text:

```
                    if False:
```

### `u270.J9_outcome_type_check`

_batch_outcomes: pass an outcome that is neither produced nor an exception through to the commit

- File: `src/cratekit/core/jobs.py`
- Source: `u270.json`, row `J9_outcome_type_check`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_jobs_batch.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs_batch.py::test_an_outcome_that_is_neither_produced_nor_an_exception_fails_its_item`

Old text:

```
        if outcome is not None and not isinstance(outcome, (Produced, Exception)):
```

New text:

```
        if False:
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

### `u233.C1_schema_default_moves`

config: labels.offer_per_sweep's default goes from 10 to 12, so the guide's settings table states an old default

- File: `src/cratekit/core/config.py`
- Source: `u233.json`, row `C1_schema_default_moves`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_docs_current.py`
- Collected: 19 against a baseline of 19
- Kills: 1 (killed)
- Killed:
  - `tests/test_docs_current.py::test_the_settings_table_is_the_schema`

Old text:

```
DEFAULT_LABEL_OFFER = 10
```

New text:

```
DEFAULT_LABEL_OFFER = 12
```

### `u233.C2_schema_gains_a_key`

config: LabelsConfig gains a key a person can set, which the guide's settings table has no row for

- File: `src/cratekit/core/config.py`
- Source: `u233.json`, row `C2_schema_gains_a_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_docs_current.py`
- Collected: 19 against a baseline of 19
- Kills: 1 (killed)
- Killed:
  - `tests/test_docs_current.py::test_the_settings_table_is_the_schema`

Old text:

```
    new_playlist_age_days: int = DEFAULT_NEW_PLAYLIST_AGE_DAYS

```

New text:

```
    new_playlist_age_days: int = DEFAULT_NEW_PLAYLIST_AGE_DAYS
    sweep_note_days: int = 3

```

### `u142.S11_read_handle_requires_closed`

_inspiration_playlists: open for writing on organize's read too, so a running rekordbox refuses the INSPIRATION proof

- File: `src/cratekit/export/set_cli.py`
- Source: `u142.json`, row `S11_read_handle_requires_closed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`
- Collected: 22933 against a baseline of 22933
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

### `r290-author.S02_acquire_download_call_removed`

Remove the one jobs.raise_for_state call from acquire/cli.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/acquire/cli.py`
- Source: `r290-author.json`, row `S02_acquire_download_call_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_acquire_workers.py`
- Collected: 195 against a baseline of 195
- Kills: 11 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_mid_batch_defect_fails_that_item_and_the_resume_the_job_refuses_fetches_nothing`
  - `tests/test_acquire_workers.py::test_a_provider_block_parks_the_job_and_makes_no_further_request`
  - `tests/test_acquire_workers.py::test_a_refusal_beside_a_network_failure_fails_and_keeps_the_refusal_skipped`
  - `tests/test_acquire_workers.py::test_an_authentication_failure_parks_the_run_and_names_the_replacement_path`
  - `tests/test_acquire_workers.py::test_three_landed_and_one_network_failure_still_fails`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.download]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[acquire.download]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[acquire.download]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.download]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[acquire.download]`
  - `tests/test_job_outcome.py::test_every_function_that_drives_a_job_maps_its_ending_afterwards`

Old text:

```
jobs.raise_for_state(job)
```

New text:

```
jobs.get  # the mapping call, removed
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

### `u246.S2_adapter_per_element`

InvocationResult: build the requested set once per result again (the shape on main)

- File: `src/cratekit/acquire/adapter.py`
- Source: `u246.json`, row `S2_adapter_per_element`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_comprehension_sets.py`, `tests/test_adapter_contract.py`
- Collected: 190 against a baseline of 190
- Kills: 1 (killed)
- Killed:
  - `tests/test_comprehension_sets.py::test_no_comprehension_in_the_package_rebuilds_an_invariant_set_per_element`

Old text:

```
            stray = [r.key for r in self.results if r.key not in asked]
```

New text:

```
            stray = [r.key for r in self.results if r.key not in set(self.requested)]
```

### `r598-b.B7_sample_live_holder_released`

release_stale_lock: skip the live holder refusal (existing guard, sampled because the sweep now sits behind it)

- File: `src/cratekit/core/session.py`
- Source: `r598-b.json`, row `B7_sample_live_holder_released`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`, `tests/test_write_session.py`
- Collected: 185 against a baseline of 185
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

### `u319.M10_sync_stop_drops_the_short_path`

tail: the step crate sync land prints names one path again

- File: `src/cratekit/cli/tail.py`
- Source: `u319.json`, row `M10_sync_stop_drops_the_short_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_drift.py`, `tests/test_rekordbox_visit_skill.py`, `tests/test_label_sync_go.py`
- Collected: 183 against a baseline of 183
- Kills: 1 (killed)
- Killed:
  - `tests/test_drift.py::test_the_sync_stop_offers_the_auto_analysis_path_after_the_selections_it_stands_in_for`

Old text:

```
    f"carrying the dyn My Tag, if any: {drift.DYNAMIC_SETTINGS}; "
    f"{AUTO_ANALYSIS_STEP}",
```

New text:

```
    f"carrying the dyn My Tag, if any: {drift.DYNAMIC_SETTINGS}",
```

### `r1264.M22_readable_dates`

list_playlist_readable: give no added dates, so a pair's later change calls read every time as unknown

- File: `src/cratekit/intake/cli.py`
- Source: `r1264.json`, row `M22_readable_dates`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_merge.py`
- Collected: 182 against a baseline of 182
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_a_rekordbox_removal_later_than_the_account_putting_it_back_takes_it_off_both`
  - `tests/test_sync_pair_back.py::test_a_removal_rekordbox_kept_no_moment_for_keeps_the_track_and_names_the_call`
  - `tests/test_sync_pair_back.py::test_a_removal_whose_row_time_predates_the_last_sync_is_no_moment`
  - `tests/test_sync_pair_back.py::test_a_row_held_as_two_releases_is_put_back_when_its_later_release_was`
  - `tests/test_sync_pair_back.py::test_a_track_put_back_on_the_account_after_rekordbox_took_it_out_stays_on_both`
  - `tests/test_sync_pair_back.py::test_the_snapshot_records_each_account_tracks_added_date`

Old text:

```
        dates=_added_dates(rows, tracks),
```

New text:

```
        dates={},
```

### `u27-adopt-apply-author.S2_analysis_watch_watches_nothing`

Arm the analysis watch on no roots, so it reports a clean session either way

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u27-adopt-apply-author.json`, row `S2_analysis_watch_watches_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_write_session.py`
- Collected: 175 against a baseline of 175
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_the_analysis_watch_is_armed_on_the_library_root`
  - `tests/test_adopt_apply_cli.py::test_the_analysis_watch_reaches_a_share_outside_the_library_root`

Old text:

```
        analysis_roots=watched,
```

New text:

```
        analysis_roots=(),
```

### `u261.R4_forbidden_not_a_refusal`

SESSION_REFUSED_STATUSES: read only 401 as judging the session, so a 403 neither drops the shared client nor forgets the account

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `R4_forbidden_not_a_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_rejection_bodies.py`
- Collected: 174 against a baseline of 174
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

### `r759.A1_deadline_asked_only_at_the_end`

the read deadline is asked only after the stream has ended, so a trickling file is read to its end before the timeout is raised

- File: `src/cratekit/adopt/revert.py`
- Source: `r759.json`, row `A1_deadline_asked_only_at_the_end`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py::test_the_deadline_ends_a_read_that_keeps_arriving_forever`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_the_deadline_ends_a_read_that_keeps_arriving_forever`

Old text:

```
                if not block:
                    break
                hasher.update(block)
                if time.monotonic() > give_up_at:
                    raise TimeoutError(
                        f"{path} did not finish arriving within "
                        f"{deadline_seconds} seconds"
                    )

```

New text:

```
                if not block:
                    if time.monotonic() > give_up_at:
                        raise TimeoutError(
                            f"{path} did not finish arriving within "
                            f"{deadline_seconds} seconds"
                        )
                    break
                hasher.update(block)

```

### `r759.A2_deadline_a_second_late`

the read deadline is honoured a second after it passes, so a trickling file is read fifty blocks further than the caller allowed

- File: `src/cratekit/adopt/revert.py`
- Source: `r759.json`, row `A2_deadline_a_second_late`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py::test_the_deadline_ends_a_read_that_keeps_arriving_forever`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_the_deadline_ends_a_read_that_keeps_arriving_forever`

Old text:

```
                if time.monotonic() > give_up_at:
                    raise TimeoutError(

```

New text:

```
                if time.monotonic() > give_up_at + 1.0:
                    raise TimeoutError(

```

### `r759-b.P4_lock_removed_r01`

the one call at a time lock is never taken, so two processes can have a request in flight together, repeat 1 of 10

- File: `src/cratekit/core/provider_gate.py`
- Source: `r759-b.json`, row `P4_lock_removed_r01`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py::test_two_processes_never_have_a_call_in_flight_together`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_two_processes_never_have_a_call_in_flight_together`

Old text:

```
                        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)

```

New text:

```
                        pass

```

### `r759.P5_lock_shared`

the lock is taken shared rather than exclusive, so every process holds it at once

- File: `src/cratekit/core/provider_gate.py`
- Source: `r759.json`, row `P5_lock_shared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py::test_two_processes_never_have_a_call_in_flight_together`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_two_processes_never_have_a_call_in_flight_together`

Old text:

```
                        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)

```

New text:

```
                        fcntl.flock(fd, fcntl.LOCK_SH | fcntl.LOCK_NB)

```

### `r759.P1_interval_dropped`

the interval is dropped from the due time, so a call waits on nothing but a Retry-After and two processes call back to back

- File: `src/cratekit/core/provider_gate.py`
- Source: `r759.json`, row `P1_interval_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py::test_two_processes_keep_the_interval_between_every_call`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_two_processes_keep_the_interval_between_every_call`

Old text:

```
                due = max(state.last_call + self.settings.min_interval_s, state.not_before)

```

New text:

```
                due = max(state.last_call, state.not_before)

```

### `r759.P6_wait_skipped_stamp_kept`

the wait before a call is skipped while its stamp still reads the due time, so the stamps stay spaced and the requests go out back to back

- File: `src/cratekit/core/provider_gate.py`
- Source: `r759.json`, row `P6_wait_skipped_stamp_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py::test_two_processes_keep_the_interval_between_every_call`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_two_processes_keep_the_interval_between_every_call`

Old text:

```
        if due > now:
            self._sleep(due - now)
            now = max(self._clock(), due)

```

New text:

```
        if due > now:
            now = max(self._clock(), due)

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

### `u249.M21_intake_reset_leaves_reader`

intake.cli.reset_cache: clear the drive's view and leave the reader's memory

- File: `src/cratekit/intake/cli.py`
- Source: `u249.json`, row `M21_intake_reset_leaves_reader`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_sync_unmark.py`, `tests/intake/test_workers.py`
- Collected: 169 against a baseline of 169
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_reset_forgets_every_file[intake]`

Old text:

```
    _RESOLVED.clear()
    match.reset_cache()
```

New text:

```
    _RESOLVED.clear()
```

### `u270.J7_raise_is_every_outcome`

_batch_outcomes: a raise out of the batch handler fails only the first item, and the rest have no outcome

- File: `src/cratekit/core/jobs.py`
- Source: `u270.json`, row `J7_raise_is_every_outcome`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs_batch.py`, `tests/test_outbound_workers.py`, `tests/test_outbound_export_batches.py`
- Collected: 167 against a baseline of 167
- Kills: 3 (killed)
- Killed:
  - `tests/test_jobs_batch.py::test_a_batch_that_fails_every_item_records_the_job_failed_then_raises`
  - `tests/test_jobs_batch.py::test_a_raise_out_of_the_batch_handler_is_every_items_outcome`
  - `tests/test_outbound_workers.py::test_a_job_driven_with_no_adapter_fails_rather_than_reporting_success`

Old text:

```
        return {item.item_id: exc for item in claimed}
```

New text:

```
        return {claimed[0].item_id: exc}
```

### `r788-d.A5_move_worker_reads_vocals`

move worker: the plan it checks against is built with the vocal reads, so a refusal about a tag row or a calibration stops a move

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r788-d.json`, row `A5_move_worker_reads_vocals`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`
- Collected: 166 against a baseline of 166
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_an_approved_move_reads_no_vocals_in_its_gate_or_in_its_worker`

Old text:

```
    todo, gone = remaining(
        approved, apply_cli.current_plan(cfg, declared, vocals=False), declared
    )
```

New text:

```
    todo, gone = remaining(
        approved, apply_cli.current_plan(cfg, declared, vocals=True), declared
    )
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

### `r380.G5_permanent_failures_still_offer_resume`

the permanent branch still carries the resume-job remedy

- File: `src/cratekit/core/jobs.py`
- Source: `r380.json`, row `G5_permanent_failures_still_offer_resume`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_label_workers.py`
- Collected: 164 against a baseline of 164
- Kills: 5 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_job_whose_every_item_failed_permanently_reports_itself_non_retryable`
  - `tests/test_jobs.py::test_a_partial_failure_whose_failures_are_permanent_is_not_resumable`
  - `tests/test_jobs.py::test_two_distinct_permanent_reasons_name_both_whichever_failed_last`
  - `tests/test_label_workers.py::test_a_second_resume_of_a_failed_sweep_still_does_not_exit_ok`
  - `tests/test_label_workers.py::test_a_sweep_whose_failures_are_permanent_does_not_tell_the_person_to_resume`

Old text:

```
        Remediation(
            steps=(
                "the failed items cannot succeed on resume; inspect each item's cause",
            )
        ),

```

New text:

```
        Remediation(remedy=Remedy.RESUME_JOB),

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

### `r501-b.L1_unretired_name`

land_cli.unretired_name: return the name unchanged, so sync mark cannot find its pass from a retired intake file

- File: `src/cratekit/intake/land_cli.py`
- Source: `r501-b.json`, row `L1_unretired_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_sync_mark.py`
- Collected: 164 against a baseline of 164
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_sync_mark_reads_the_same_pass_off_a_retired_intake_file[RUN_synced_inboxed.xml.imported-2]`
  - `tests/test_intake_imported.py::test_sync_mark_reads_the_same_pass_off_a_retired_intake_file[RUN_synced_inboxed.xml.imported]`
  - `tests/test_intake_imported.py::test_the_retired_name_is_out_of_the_pending_scan_and_reads_back`

Old text:

```
    return _RETIRED_TAIL.sub("", name)
```

New text:

```
    return name
```

### `r682-a.M1_no_by_reason_in_summary`

the intake summary no longer carries by_reason, so the json and the rendering both lose the breakdown

- File: `src/cratekit/intake/cli.py`
- Source: `r682-a.json`, row `M1_no_by_reason_in_summary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_render_payloads.py`
- Collected: 163 against a baseline of 163
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_report_without_a_reason_counts_in_its_state_and_under_no_reason`
  - `tests/intake/test_workers.py::test_a_set_job_runs_pending_to_done_and_reports_owned_offered_and_missing`
  - `tests/intake/test_workers.py::test_each_resolution_count_is_followed_by_its_reasons`
  - `tests/intake/test_workers.py::test_the_reasons_are_read_back_from_the_reports_on_every_resume`

Old text:

```
        "by_reason": by_reason,

```

New text:

```
(empty)
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

