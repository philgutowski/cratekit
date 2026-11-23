# Mutation table: u325-after-l-16

Measured by `scripts/mutate.py` on 2026-11-22 22:23 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 132.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:22 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 10, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r592-a.A7_companion_suffix_wrong` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 2 | killed |
| `r592-a.A8_sample_stub_check_beside` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 2 | killed |
| `u27-restore-cli-independent.X6_the_rekordbox_guard_itself_is_neutered` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 1 | killed |
| `u80-b.F9_coverage_weight` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 1 | killed |
| `u80.F10_no_url_dedupe` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 1 | killed |
| `u80.F11_tie_ignores_platform` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 1 | killed |
| `u80.F12_open_searched_again` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 3 | killed |
| `u80.F13_rejected_searched_again` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 1 | killed |
| `u80.F14_single_option_stalls` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 1 | killed |
| `u80.F15_empty_offered` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 4 | killed |
| `u80.F1_one_platform` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 7 | killed |
| `u80.F2_order_reversed` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 2 | killed |
| `u80.F4_timeout_is_empty` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 1 | killed |
| `u80.F5_api_url_kept` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 1 | killed |
| `u80.F6_ignore_errors_back` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 1 | killed |
| `u80.F7_mix_boundary` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 1 | killed |
| `u80.F8_mix_not_demoted` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 1 | killed |
| `u80-b.C4_searcher_eager` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 37 | 3 | killed |
| `u80.C3_dedupe_on_match_id` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `u80.C7_offered_not_named` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 37 | 3 | killed |
| `u80.C8_outage_narrowed` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `u101.G10_ungated_not_reported_in_judged_label` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 3 | killed |
| `u101.G11_keep_read_as_drop` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 12 | killed |
| `u101.G12_reported_share_not_the_taxonomys` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G13_family_count_off_by_one` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 2 | killed |
| `u101.G14_classified_counts_unjudged` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G17_refusal_silent_on_held` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G18_no_op_claims_held` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G1_held_is_listed` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 7 | killed |
| `u101.G20_summary_held_empty` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 5 | killed |
| `u101.G2_judged_per_release` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 10 | killed |
| `u101.G3_all_labels_one_group` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 4 | killed |
| `u101.G4_unlabelled_grouped_together` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G5_unread_label_judged` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G6_unread_from_every_label` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 2 | killed |
| `u101.G7_mixed_is_a_genre` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G8_case_is_a_difference` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G9_mapping_row_unread` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u143-c.A1_kind_named` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 451 | 1 | killed |
| `u143-c.A2_ledger_claimed` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 451 | 1 | killed |
| `u143-c.A3_debris_served` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 451 | 2 | killed |
| `u143-c.A4_empty_videos` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 451 | 2 | killed |
| `u143-d.A5_playlist_read_back` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 451 | 1 | killed |
| `u143-d.A6_legacy_name` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 451 | 2 | killed |
| `u143-d.A7_folder_empty` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 451 | 1 | killed |
| `u143-d.A8_folder_read_back` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 451 | 1 | killed |
| `u127.L1_screen_line_blind` | `src/cratekit/intake/land_cli.py` | user | 11 file(s) | 549 | 1 | killed |
| `u127.L2_items_carry_no_vox` | `src/cratekit/intake/land_cli.py` | user | 11 file(s) | 549 | 6 | killed |
| `u127.L3_totals_from_writer` | `src/cratekit/intake/land_cli.py` | user | 11 file(s) | 549 | 1 | killed |
| `u127.L4_missing_unsaid` | `src/cratekit/intake/land_cli.py` | user | 11 file(s) | 549 | 1 | killed |
| `u127.L5_unscored_unsaid` | `src/cratekit/intake/land_cli.py` | user | 11 file(s) | 549 | 1 | killed |
| `u127.L6_bridge_ignores_calibration` | `src/cratekit/intake/land_cli.py` | user | 11 file(s) | 549 | 1 | killed |
| `u127.L7_land_warnings_unsaid` | `src/cratekit/intake/land_cli.py` | user | 11 file(s) | 549 | 7 | killed |
| `u111-a.A1_folder_refused` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 253 | 1 | killed |
| `u111-a.A3_parent_not_folder` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 253 | 1 | killed |
| `u111-a.A4_memberships_unmarked` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 253 | 2 | killed |
| `u111-a.A5_node_unmarked` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 253 | 2 | killed |
| `u111-a.A6_playlist_not_removable` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 254 | collection error | collect-error |
| `u111-a.A7_content_compared` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 253 | 1 | killed |
| `u111-b.A10_renumber_scoped` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 253 | 1 | killed |
| `u111-b.A12_removed_keeps_no_live` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 253 | 2 | killed |
| `u111-b.A13_confinement_raises` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 253 | 2 | killed |
| `u111-b.A8_membership_owner` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 253 | 2 | killed |
| `u111-b.A9_planned_move_made` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 253 | 4 | killed |
| `u81-fetch-b.L1_two_files_first_wins` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 35 | 1 | killed |
| `u81-fetch-b.L2_any_suffix` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 35 | 1 | killed |
| `u81-fetch-b.Y1_no_option_terminator` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 35 | 1 | killed |
| `u81-fetch-b.Y2_metadata_kept_on_convert` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 35 | 1 | killed |
| `u81-fetch-b.Y3_failed_exit_is_a_file` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 35 | 1 | killed |
| `u81-fetch-a.W10_untaggable_committed` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 1 | killed |
| `u81-fetch-a.W12_download_failure_not_retryable` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 1 | killed |
| `u81-fetch-a.W1_strict_not_refused` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 1 | killed |
| `u81-fetch-a.W3_host_half` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 1 | killed |
| `u81-fetch-a.W5_pre_download_exists` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 1 | killed |
| `u81-fetch-a.W6_post_landing_exists` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 1 | killed |
| `u81-fetch-a.W7_final_unmarked` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 4 | killed |
| `u81-fetch-a.W8_upload_tags_kept` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 1 | killed |
| `u81-fetch-a.W9_row_tags_not_written` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 2 | killed |
| `u81-fetch-b.Q1_provider_route_fetched_lossy` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 1 | killed |
| `u81-fetch-b.Q3_empty_queue` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 4 | killed |
| `u81-fetch-b.W2_scheme_half_rerun` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 2 | killed |
| `u81-fetch-b.W4_empty_stem_rerun` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 1 | killed |
| `r227.A1_floored_days` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 371 | 2 | killed |
| `r227.A2_never_stale` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 371 | 13 | killed |
| `r227.A3_future_clamped` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 371 | 1 | killed |
| `r227.A4_no_tolerance` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 371 | 1 | killed |
| `r227.A5_half_a_pair` | `src/cratekit/modules/outbound/source.py` | maintainer | 4 file(s) | 371 | 1 | killed |
| `r227.A6_conversion_unguarded` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 371 | 1 | killed |
| `r227.A7_unreadable_reads_as_now` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 371 | 2 | killed |
| `r356-b.B1_naming_head_left_on_the_release_title` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 371 | 8 | killed |
| `r356-b.B4_heart_candidate_carries_no_artist` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 371 | 4 | killed |
| `u179-z.S4_to_fetch_counts_held` | `src/cratekit/cli/sync_bandcamp.py` | user | 2 file(s) | 34 | 1 | killed |
| `u179-z.S9_refusals_need_permanence` | `src/cratekit/cli/sync_bandcamp.py` | user | 2 file(s) | 34 | 1 | killed |
| `u179.D1_fetched_once` | `src/cratekit/cli/sync_bandcamp.py` | user | 2 file(s) | 34 | 1 | killed |
| `u179.D2_refused_once` | `src/cratekit/cli/sync_bandcamp.py` | user | 2 file(s) | 34 | 1 | killed |
| `u179.S10_open_fetch_stops` | `src/cratekit/cli/sync_bandcamp.py` | user | 2 file(s) | 34 | 2 | killed |
| `u179.S13_nothing_staged_ends` | `src/cratekit/cli/sync_bandcamp.py` | user | 2 file(s) | 34 | 4 | killed |
| `u179.S14_relist_after_name` | `src/cratekit/cli/sync_bandcamp.py` | user | 2 file(s) | 34 | 1 | killed |
| `u179.S15_unread_apart` | `src/cratekit/cli/sync_bandcamp.py` | user | 2 file(s) | 34 | 1 | killed |
| `u179.S16_no_genre_named` | `src/cratekit/cli/sync_bandcamp.py` | user | 2 file(s) | 34 | 1 | killed |
| `u179.S17_label_flag_needs_a_label` | `src/cratekit/cli/sync_bandcamp.py` | user | 2 file(s) | 34 | 1 | killed |
| `u179.S1_fetch_only_when_planned` | `src/cratekit/cli/sync_bandcamp.py` | user | 2 file(s) | 34 | 3 | killed |
| `u179.S2_owned_recorded` | `src/cratekit/cli/sync_bandcamp.py` | user | 2 file(s) | 34 | 4 | killed |
| `u179.S3_held_recorded` | `src/cratekit/cli/sync_bandcamp.py` | user | 2 file(s) | 34 | 3 | killed |
| `u179.S5_open_fetch_elsewhere` | `src/cratekit/cli/sync_bandcamp.py` | user | 2 file(s) | 34 | 1 | killed |
| `u179.S6_open_fetches_all` | `src/cratekit/cli/sync_bandcamp.py` | user | 2 file(s) | 34 | 1 | killed |
| `u179.S7_open_fetch_order` | `src/cratekit/cli/sync_bandcamp.py` | user | 2 file(s) | 34 | 1 | killed |
| `u179.S8_refusals_settle` | `src/cratekit/cli/sync_bandcamp.py` | user | 2 file(s) | 34 | 2 | killed |
| `u179.T1_rehearsal_runs` | `src/cratekit/cli/sync_bandcamp.py` | user | 2 file(s) | 34 | 5 | killed |
| `u214.M15_unread_is_not_none` | `src/cratekit/intake/rotate.py` | user | 6 file(s) | 201 | 2 | killed |
| `u214.M16_old_only_under_inbox` | `src/cratekit/intake/rotate.py` | user | 6 file(s) | 201 | 1 | killed |
| `u214.M18_folder_unknown` | `src/cratekit/intake/rotate.py` | user | 6 file(s) | 201 | 1 | killed |
| `u214.M19_folder_unread_reason` | `src/cratekit/intake/rotate.py` | user | 6 file(s) | 201 | 1 | killed |
| `u214.M1_old_named_as_old` | `src/cratekit/intake/rotate.py` | user | 6 file(s) | 201 | 5 | killed |
| `u214.M20_unread_unlisted` | `src/cratekit/intake/rotate.py` | user | 6 file(s) | 201 | 1 | killed |
| `u214.M2_left_row_count` | `src/cratekit/intake/rotate.py` | user | 6 file(s) | 201 | 4 | killed |
| `u214.M3_live_left_collected` | `src/cratekit/intake/rotate.py` | user | 6 file(s) | 201 | 8 | killed |
| `u214.M4_digest_without_count` | `src/cratekit/intake/rotate.py` | user | 6 file(s) | 201 | 1 | killed |
| `u214.M5_rotation_old_display` | `src/cratekit/intake/rotate.py` | user | 6 file(s) | 201 | 3 | killed |
| `u214.M6_live_old_display` | `src/cratekit/intake/rotate.py` | user | 6 file(s) | 201 | 3 | killed |
| `u214.M7_label_rows` | `src/cratekit/intake/rotate.py` | user | 6 file(s) | 201 | 2 | killed |

## Row definitions

### `r592-a.A7_companion_suffix_wrong`

recovered_database_fileset: name each companion with a dot before its suffix, master.db.-wal, so no real companion is ever found

- File: `src/cratekit/core/restore.py`
- Source: `r592-a.json`, row `A7_companion_suffix_wrong`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 257 against a baseline of 257
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_that_already_holds_a_library`
  - `tests/test_restore.py::test_the_occupancy_fileset_is_the_one_the_restore_plan_writes`

Old text:

```
        landing.with_name(landing.name + sidecar.suffix)
        for sidecar in config.state_file("rekordbox_db").sidecars
    )
    return (landing, *companions)
```

New text:

```
        landing.with_name(landing.name + "." + sidecar.suffix)
        for sidecar in config.state_file("rekordbox_db").sidecars
    )
    return (landing, *companions)
```

### `r592-a.A8_sample_stub_check_beside`

SAMPLE, existing guard: assert_recovery_target refuses only a stub at or under the configured root, not the suffixed name beside it

- File: `src/cratekit/core/restore.py`
- Source: `r592-a.json`, row `A8_sample_stub_check_beside`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 257 against a baseline of 257
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_the_stubs_beside_and_beneath_the_mount_point[library 1-why1]`
  - `tests/test_restore.py::test_round2_the_real_mount_probe_is_armed_by_default`

Old text:

```
    if (inside_configured or beside_configured) and not probe(where):
```

New text:

```
    if inside_configured and not probe(where):
```

### `u27-restore-cli-independent.X6_the_rekordbox_guard_itself_is_neutered`

What the process-lister zeros DO leave held: make the restore engine's rekordbox-closed assertion return without asking. Paired with I_A6 and I_A7, which stopped threading that guard's injected seam and killed nothing

- File: `src/cratekit/core/restore.py`
- Source: `u27-restore-cli-independent.json`, row `X6_the_rekordbox_guard_itself_is_neutered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 257 against a baseline of 257
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_a_restore_refuses_while_rekordbox_holds_the_database`

Old text:

```
    running = processes.rekordbox_processes_running(lister=process_lister)
    if not running:
        return
```

New text:

```
    running = processes.rekordbox_processes_running(lister=process_lister)
    if running or not running:
        return
```

### `u80-b.F9_coverage_weight`

The score weights similarity 60 and word coverage 40, not half and half

- File: `src/cratekit/acquire/fallback.py`
- Source: `u80-b.json`, row `F9_coverage_weight`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_the_score_is_half_similarity_half_word_coverage`

Old text:

```
    said = 50.0 * ratio + 50.0 * coverage
```

New text:

```
    said = 60.0 * ratio + 40.0 * coverage
```

### `u80.F10_no_url_dedupe`

The same upload returned twice is offered as two options

- File: `src/cratekit/acquire/fallback.py`
- Source: `u80.json`, row `F10_no_url_dedupe`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_ranking_breaks_a_tie_by_platform_then_order_and_dedupes_urls`

Old text:

```
        if hit.url in seen:
            continue
```

New text:

```
        if False:
            continue
```

### `u80.F11_tie_ignores_platform`

Two equal scores are ordered by position alone, not SoundCloud first

- File: `src/cratekit/acquire/fallback.py`
- Source: `u80.json`, row `F11_tie_ignores_platform`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_ranking_breaks_a_tie_by_platform_then_order_and_dedupes_urls`

Old text:

```
        key=lambda entry: entry[:3],
    )
    seen: set[str] = set()
    kept: list[Candidate] = []
```

New text:

```
        key=lambda entry: (entry[0], entry[2]),
    )
    seen: set[str] = set()
    kept: list[Candidate] = []
```

### `u80.F12_open_searched_again`

An open question is not read from the queue, so it is searched again

- File: `src/cratekit/acquire/fallback.py`
- Source: `u80.json`, row `F12_open_searched_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`
- Collected: 37 against a baseline of 37
- Kills: 3 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_a_list_whose_rows_are_all_settled_needs_no_binary`
  - `tests/test_acquire_fallback.py::test_a_second_run_searches_nothing_and_offers_nothing_twice`
  - `tests/test_acquire_fallback.py::test_an_outage_names_every_row_already_offered`

Old text:

```
    if held.verdict is None:
        return Proposal(
            wanted,
            WAITING,
```

New text:

```
    if held.verdict is None:
        return None
        return Proposal(
            wanted,
            WAITING,
```

### `u80.F13_rejected_searched_again`

A rejected row is searched and offered again

- File: `src/cratekit/acquire/fallback.py`
- Source: `u80.json`, row `F13_rejected_searched_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_a_rejected_row_is_not_searched_again_and_says_so`

Old text:

```
    if held.verdict is review.Verdict.REJECTED:
        return Proposal(
```

New text:

```
    if held.verdict is review.Verdict.REJECTED:
        return None
        return Proposal(
```

### `u80.F14_single_option_stalls`

An acceptance over one option without naming it stalls instead of choosing it

- File: `src/cratekit/acquire/fallback.py`
- Source: `u80.json`, row `F14_single_option_stalls`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_an_acceptance_over_one_option_is_that_option`

Old text:

```
    if chosen is None and count == 1:
```

New text:

```
    if chosen is None and count == 0:
```

### `u80.F15_empty_offered`

A row with no candidate is offered as an empty item rather than reported

- File: `src/cratekit/acquire/fallback.py`
- Source: `u80.json`, row `F15_empty_offered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`
- Collected: 37 against a baseline of 37
- Kills: 4 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_a_provider_route_beside_an_unfound_row_is_reported_not_refused`
  - `tests/test_acquire_fallback.py::test_a_row_with_none_beside_a_row_offered_is_a_failing_check`
  - `tests/test_acquire_fallback.py::test_no_candidate_anywhere_refuses_and_names_the_row`
  - `tests/test_acquire_fallback.py::test_unreadable_lines_are_counted_on_a_row_with_none`

Old text:

```
    on_screen = ranked(wanted, answer)
    if not on_screen:
```

New text:

```
    on_screen = ranked(wanted, answer)
    if False:
```

### `u80.F1_one_platform`

Only the first platform is searched, so YouTube is never asked

- File: `src/cratekit/acquire/fallback.py`
- Source: `u80.json`, row `F1_one_platform`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`
- Collected: 37 against a baseline of 37
- Kills: 7 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_an_accepted_upload_is_reported_with_its_url_and_not_searched`
  - `tests/test_acquire_fallback.py::test_an_outage_names_every_row_already_offered`
  - `tests/test_acquire_fallback.py::test_an_outage_on_the_first_row_says_nothing_was_offered`
  - `tests/test_acquire_fallback.py::test_no_candidate_anywhere_refuses_and_names_the_row`
  - `tests/test_acquire_fallback.py::test_one_track_with_and_without_a_key_is_searched_once`
  - `tests/test_acquire_fallback.py::test_ranked_candidates_are_offered_on_one_item`
  - `tests/test_acquire_fallback.py::test_the_same_line_twice_is_one_question`

Old text:

```
    for platform in PLATFORMS:
        answer = searcher.search(platform, query(wanted), SEARCH_LIMIT)
```

New text:

```
    for platform in PLATFORMS[:1]:
        answer = searcher.search(platform, query(wanted), SEARCH_LIMIT)
```

### `u80.F2_order_reversed`

YouTube is searched before SoundCloud, against the source system's order

- File: `src/cratekit/acquire/fallback.py`
- Source: `u80.json`, row `F2_order_reversed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`
- Collected: 37 against a baseline of 37
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_ranked_candidates_are_offered_on_one_item`
  - `tests/test_acquire_fallback.py::test_ranking_breaks_a_tie_by_platform_then_order_and_dedupes_urls`

Old text:

```
PLATFORMS: tuple[str, ...] = (SOUNDCLOUD, YOUTUBE)
```

New text:

```
PLATFORMS: tuple[str, ...] = (YOUTUBE, SOUNDCLOUD)
```

### `u80.F4_timeout_is_empty`

A search that timed out reads as an empty answer rather than an outage

- File: `src/cratekit/acquire/fallback.py`
- Source: `u80.json`, row `F4_timeout_is_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_a_timeout_or_a_program_that_cannot_start_is_unavailable[raised0]`

Old text:

```
        except subprocess.TimeoutExpired as exc:
            raise FallbackUnavailable(
                f"the {platform} search did not answer within {self._timeout:g} seconds"
            ) from exc
```

New text:

```
        except subprocess.TimeoutExpired:
            return Answer(hits=())
```

### `u80.F5_api_url_kept`

An unresolvable api.soundcloud.com URL is offered instead of the page URL

- File: `src/cratekit/acquire/fallback.py`
- Source: `u80.json`, row `F5_api_url_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_printed_lines_are_read_as_hits_and_bad_lines_are_counted`

Old text:

```
    if "api.soundcloud.com" in str(url):
        url = said.get("webpage_url") or ""
```

New text:

```
    if "api.soundcloud.com" in str(url) and False:
        url = said.get("webpage_url") or ""
```

### `u80.F6_ignore_errors_back`

The subprocess is run with the source system's ignore errors flag again

- File: `src/cratekit/acquire/fallback.py`
- Source: `u80.json`, row `F6_ignore_errors_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_the_argv_searches_flat_with_the_platform_prefix_and_no_ignore_errors`

Old text:

```
            "--no-warnings",
            "--print",
```

New text:

```
            "--no-warnings",
            "--ignore-errors",
            "--print",
```

### `u80.F7_mix_boundary`

An upload exactly at the mix length is demoted as a mix

- File: `src/cratekit/acquire/fallback.py`
- Source: `u80.json`, row `F7_mix_boundary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_a_long_mix_is_demoted_below_the_track_it_names`

Old text:

```
    if hit.duration is not None and hit.duration > LIKELY_MIX_SECONDS:
```

New text:

```
    if hit.duration is not None and hit.duration >= LIKELY_MIX_SECONDS:
```

### `u80.F8_mix_not_demoted`

A long mix is no longer demoted below the track it names

- File: `src/cratekit/acquire/fallback.py`
- Source: `u80.json`, row `F8_mix_not_demoted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_a_long_mix_is_demoted_below_the_track_it_names`

Old text:

```
        said *= MIX_FACTOR
```

New text:

```
        said *= 1.0
```

### `u80-b.C4_searcher_eager`

The searcher is built before any row needs a search, so a settled list needs yt-dlp

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `u80-b.json`, row `C4_searcher_eager`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`
- Collected: 37 against a baseline of 37
- Kills: 3 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_a_broken_override_is_its_own_refusal`
  - `tests/test_acquire_fallback.py::test_a_list_whose_rows_are_all_settled_needs_no_binary`
  - `tests/test_acquire_fallback.py::test_a_missing_binary_refuses_with_the_install_hint`

Old text:

```
            found: fallback.FallbackSearcher | None = None
```

New text:

```
            try:
                found: fallback.FallbackSearcher | None = searcher()
            except binaries.BinaryNotFound as exc:
                raise _binary_refusal(exc, subject) from exc
```

### `u80.C3_dedupe_on_match_id`

Rows are deduplicated on the match id, which carries the key

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `u80.json`, row `C3_dedupe_on_match_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_one_track_with_and_without_a_key_is_searched_once`

Old text:

```
            asked = fallback.item_id(one.wanted)
```

New text:

```
            asked = one.match_id
```

### `u80.C7_offered_not_named`

An outage no longer names the rows this run already offered

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `u80.json`, row `C7_offered_not_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`
- Collected: 37 against a baseline of 37
- Kills: 3 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_an_outage_names_every_row_already_offered`
  - `tests/test_acquire_fallback.py::test_one_track_with_and_without_a_key_is_searched_once`
  - `tests/test_acquire_fallback.py::test_ranked_candidates_are_offered_on_one_item`

Old text:

```
                if made.state == fallback.OFFERED:
                    offered_now.append(made)
```

New text:

```
                if made.state == fallback.OFFERED:
                    pass
```

### `u80.C8_outage_narrowed`

Only FallbackUnavailable is an outage, so any other searcher failure crashes

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `u80.json`, row `C8_outage_narrowed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_any_searcher_failure_is_an_outage_not_a_crash`

Old text:

```
                except Exception as exc:  # noqa: BLE001 - refused whole, never swallowed
```

New text:

```
                except fallback.FallbackUnavailable as exc:
```

### `u101.G10_ungated_not_reported_in_judged_label`

Drop the ungated branch in a judged label, so a release with no genre is listed silently

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G10_ungated_not_reported_in_judged_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_release_with_no_genre_is_not_counted_in_its_labels_share`
  - `tests/test_label_approved.py::test_a_release_with_no_genre_known_is_listed_with_a_failing_line`
  - `tests/test_label_approved.py::test_tracks_that_disagree_on_the_genre_are_not_judged_and_are_listed`

Old text:

```
            if outcome.ungated is not None:
```

New text:

```
            if False:
```

### `u101.G11_keep_read_as_drop`

Hold on the KEEP verdict instead of DROP

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G11_keep_read_as_drop`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 12 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_family_exactly_at_the_share_belongs_and_is_listed`
  - `tests/test_label_approved.py::test_a_genre_on_a_mapping_row_is_read_like_one_on_an_object`
  - `tests/test_label_approved.py::test_a_genre_the_label_makes_enough_of_is_listed`
  - `tests/test_label_approved.py::test_a_held_release_is_never_offered_for_review`
  - `tests/test_label_approved.py::test_a_release_of_an_out_of_place_genre_is_held_by_name_and_not_listed`
  - `tests/test_label_approved.py::test_a_release_unread_on_another_label_does_not_stop_this_label_being_judged`
  - `tests/test_label_approved.py::test_a_release_with_no_genre_is_not_counted_in_its_labels_share`
  - `tests/test_label_approved.py::test_each_label_is_judged_against_its_own_output`
  - `tests/test_label_approved.py::test_every_release_held_or_owned_is_a_no_op_that_does_not_claim_the_held_one`
  - `tests/test_label_approved.py::test_nothing_missing_with_one_held_and_one_unread_is_refused_and_says_both`
  - `tests/test_label_approved.py::test_releases_naming_no_label_are_each_judged_alone`
  - `tests/test_label_approved.py::test_the_default_human_output_names_a_held_release`

Old text:

```
            elif verdict is routing.GateVerdict.DROP and family and outcome.genre:
```

New text:

```
            elif verdict is routing.GateVerdict.KEEP and family and outcome.genre:
```

### `u101.G12_reported_share_not_the_taxonomys`

Report a share the taxonomy did not declare

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G12_reported_share_not_the_taxonomys`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_release_of_an_out_of_place_genre_is_held_by_name_and_not_listed`

Old text:

```
    share = declared.label_gate.out_of_place_share
```

New text:

```
    share = 0.2
```

### `u101.G13_family_count_off_by_one`

Report one more release of the family than there were

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G13_family_count_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_release_of_an_out_of_place_genre_is_held_by_name_and_not_listed`
  - `tests/test_label_approved.py::test_a_release_with_no_genre_is_not_counted_in_its_labels_share`

Old text:

```
families.count(family), classified, share
```

New text:

```
families.count(family) + 1, classified, share
```

### `u101.G14_classified_counts_unjudged`

Count every release in the label as classified, including those with no genre

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G14_classified_counts_unjudged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_release_with_no_genre_is_not_counted_in_its_labels_share`

Old text:

```
        classified = sum(1 for genre in genres if genre)
```

New text:

```
        classified = len(genres)
```

### `u101.G17_refusal_silent_on_held`

Drop the held clause from the nothing missing refusal

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G17_refusal_silent_on_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_nothing_missing_with_one_held_and_one_unread_is_refused_and_says_both`

Old text:

```
            + (f" and passed the genre gate ({len(held)} more held by it)" if held else "")
```

New text:

```
            + ""
```

### `u101.G18_no_op_claims_held`

The no op wording ignores held releases and says the library holds everything read

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G18_no_op_claims_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_every_release_held_or_owned_is_a_no_op_that_does_not_claim_the_held_one`

Old text:

```
            f"held by it"
            if held
            else
```

New text:

```
            f"held by it"
            if False
            else
```

### `u101.G1_held_is_listed`

Drop the skip, so a release the gate held is resolved, offered and listed anyway

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G1_held_is_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_genre_on_a_mapping_row_is_read_like_one_on_an_object`
  - `tests/test_label_approved.py::test_a_held_release_is_never_offered_for_review`
  - `tests/test_label_approved.py::test_a_release_of_an_out_of_place_genre_is_held_by_name_and_not_listed`
  - `tests/test_label_approved.py::test_a_release_unread_on_another_label_does_not_stop_this_label_being_judged`
  - `tests/test_label_approved.py::test_each_label_is_judged_against_its_own_output`
  - `tests/test_label_approved.py::test_every_release_held_or_owned_is_a_no_op_that_does_not_claim_the_held_one`
  - `tests/test_label_approved.py::test_nothing_missing_with_one_held_and_one_unread_is_refused_and_says_both`

Old text:

```
        if release.item_id in held:
            continue

```

New text:

```
(empty)
```

### `u101.G20_summary_held_empty`

The summary carries no held releases

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G20_summary_held_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_genre_on_a_mapping_row_is_read_like_one_on_an_object`
  - `tests/test_label_approved.py::test_a_release_of_an_out_of_place_genre_is_held_by_name_and_not_listed`
  - `tests/test_label_approved.py::test_a_release_unread_on_another_label_does_not_stop_this_label_being_judged`
  - `tests/test_label_approved.py::test_a_release_with_no_genre_is_not_counted_in_its_labels_share`
  - `tests/test_label_approved.py::test_each_label_is_judged_against_its_own_output`

Old text:

```
        held=[one.to_json() for one in held.values()],
```

New text:

```
        held=[],
```

### `u101.G2_judged_per_release`

Group every release under itself, so each is judged alone and nothing is ever held

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G2_judged_per_release`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 10 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_genre_on_a_mapping_row_is_read_like_one_on_an_object`
  - `tests/test_label_approved.py::test_a_held_release_is_never_offered_for_review`
  - `tests/test_label_approved.py::test_a_label_with_a_release_unread_this_run_is_not_judged_and_says_why`
  - `tests/test_label_approved.py::test_a_release_of_an_out_of_place_genre_is_held_by_name_and_not_listed`
  - `tests/test_label_approved.py::test_a_release_unread_on_another_label_does_not_stop_this_label_being_judged`
  - `tests/test_label_approved.py::test_a_release_with_no_genre_is_not_counted_in_its_labels_share`
  - `tests/test_label_approved.py::test_each_label_is_judged_against_its_own_output`
  - `tests/test_label_approved.py::test_every_release_held_or_owned_is_a_no_op_that_does_not_claim_the_held_one`
  - `tests/test_label_approved.py::test_nothing_missing_with_one_held_and_one_unread_is_refused_and_says_both`
  - `tests/test_label_approved.py::test_the_default_human_output_names_a_held_release`

Old text:

```
    return release.label_id or release.label_name or f"release:{release.release_id}"
```

New text:

```
    return f"release:{release.release_id}"
```

### `u101.G3_all_labels_one_group`

Group every release under one key, so labels are judged against each other

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G3_all_labels_one_group`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_release_unread_on_another_label_does_not_stop_this_label_being_judged`
  - `tests/test_label_approved.py::test_each_label_is_judged_against_its_own_output`
  - `tests/test_label_approved.py::test_nothing_missing_with_one_held_and_one_unread_is_refused_and_says_both`
  - `tests/test_label_approved.py::test_releases_naming_no_label_are_each_judged_alone`

Old text:

```
    return release.label_id or release.label_name or f"release:{release.release_id}"
```

New text:

```
    return "all"
```

### `u101.G4_unlabelled_grouped_together`

Group every release naming no label under one key instead of judging each alone

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G4_unlabelled_grouped_together`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_releases_naming_no_label_are_each_judged_alone`

Old text:

```
    return release.label_id or release.label_name or f"release:{release.release_id}"
```

New text:

```
    return release.label_id or release.label_name or "release:"
```

### `u101.G5_unread_label_judged`

Judge a label even when one of its releases was unread this run

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G5_unread_label_judged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_label_with_a_release_unread_this_run_is_not_judged_and_says_why`

Old text:

```
        if label in unread:
```

New text:

```
        if label in unread and False:
```

### `u101.G6_unread_from_every_label`

Treat every label as having an unread release whenever any release failed

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G6_unread_from_every_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_release_unread_on_another_label_does_not_stop_this_label_being_judged`
  - `tests/test_label_approved.py::test_nothing_missing_with_one_held_and_one_unread_is_refused_and_says_both`

Old text:

```
        if label in unread:
```

New text:

```
        if unread:
```

### `u101.G7_mixed_is_a_genre`

Rows that disagree yield their first genre instead of none

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G7_mixed_is_a_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_tracks_that_disagree_on_the_genre_are_not_judged_and_are_listed`

Old text:

```
    if len(said) > 1:
```

New text:

```
    if len(said) > 99:
```

### `u101.G8_case_is_a_difference`

Compare genres by exact text, so one genre in two cases reads as mixed

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G8_case_is_a_difference`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_one_genre_in_two_cases_is_one_genre_and_is_judged`

Old text:

```
            said.setdefault(text.casefold(), text)
```

New text:

```
            said.setdefault(text, text)
```

### `u101.G9_mapping_row_unread`

Read the genre by attribute only, so a mapping shaped row reports none

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G9_mapping_row_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_genre_on_a_mapping_row_is_read_like_one_on_an_object`

Old text:

```
        value = row.get("genre") if isinstance(row, Mapping) else getattr(row, "genre", None)
```

New text:

```
        value = getattr(row, "genre", None)
```

### `u143-c.A1_kind_named`

Adapter: drop the refusal of a kind other than debris or empty

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u143-c.json`, row `A1_kind_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_root.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`
- Collected: 451 against a baseline of 451
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_ledger_claimed_playlist_or_another_kind_is_refused_with_no_provider_call`

Old text:

```
        if kind not in kinds.ROOT_REMOVALS:
```

New text:

```
        if False:
```

### `u143-c.A2_ledger_claimed`

Adapter: remove a root playlist a ledger record names

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u143-c.json`, row `A2_ledger_claimed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_root.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`
- Collected: 451 against a baseline of 451
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_ledger_claimed_playlist_or_another_kind_is_refused_with_no_provider_call`

Old text:

```
        if self._cfg is None or self._claimed(identifier):
```

New text:

```
        if self._cfg is None:
```

### `u143-c.A3_debris_served`

Adapter: accept any served name as debris

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u143-c.json`, row `A3_debris_served`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_root.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`
- Collected: 451 against a baseline of 451
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_playlist_the_provider_serves_as_not_of_the_kind_is_refused_before_any_delete[served0-debris]`
  - `tests/test_organize_root.py::test_a_playlist_the_provider_serves_as_not_of_the_kind_is_refused_before_any_delete[served1-debris]`

Old text:

```
            served = is_library_debris(name)
```

New text:

```
            served = True
```

### `u143-c.A4_empty_videos`

Adapter: an empty playlist need not declare zero videos

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u143-c.json`, row `A4_empty_videos`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_root.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`
- Collected: 451 against a baseline of 451
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_playlist_the_provider_serves_as_not_of_the_kind_is_refused_before_any_delete[served3-empty]`
  - `tests/test_organize_root.py::test_a_playlist_the_provider_serves_as_not_of_the_kind_is_refused_before_any_delete[served4-empty]`

Old text:

```
            served = _count(tracks) and _count(videos) and tracks == 0 and videos == 0
```

New text:

```
            served = _count(tracks) and tracks == 0
```

### `u143-d.A5_playlist_read_back`

Adapter: report a root playlist removed though the provider still serves it

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u143-d.json`, row `A5_playlist_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_root.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`
- Collected: 451 against a baseline of 451
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_root_playlist_still_served_after_its_delete_is_refused_not_reported_removed`

Old text:

```
        if served_after is not _ABSENT and served_after is not None:
```

New text:

```
        if False:
```

### `u143-d.A6_legacy_name`

Adapter: remove a root folder whatever its name

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u143-d.json`, row `A6_legacy_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_root.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`
- Collected: 451 against a baseline of 451
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_folder_not_legacy_or_not_empty_is_refused_before_any_removal[2026-0-not-a-legacy-folder]`
  - `tests/test_organize_root.py::test_a_folder_not_legacy_or_not_empty_is_refused_before_any_removal[Phil's Spotify-0-not-a-legacy-folder]`

Old text:

```
        if not kinds.legacy_year(name):
```

New text:

```
        if False:
```

### `u143-d.A7_folder_empty`

Adapter: remove a legacy folder that still holds playlists

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u143-d.json`, row `A7_folder_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_root.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`
- Collected: 451 against a baseline of 451
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_folder_not_legacy_or_not_empty_is_refused_before_any_removal[2026 Custom Playlists-2-not-empty]`

Old text:

```
        held = len(self.folder_playlists(identifier)) + len(self.folder_folders(identifier))
```

New text:

```
        held = 0
```

### `u143-d.A8_folder_read_back`

Adapter: report a folder removed though the root still lists it

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u143-d.json`, row `A8_folder_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_root.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`
- Collected: 451 against a baseline of 451
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_legacy_folder_still_listed_after_its_removal_is_refused`

Old text:

```
        if identifier in self.folders():
```

New text:

```
        if False:
```

### `u127.L1_screen_line_blind`

The native screen counts no tagged row

- File: `src/cratekit/intake/land_cli.py`
- Source: `u127.json`, row `L1_screen_line_blind`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 549 against a baseline of 549
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_the_screen_counts_the_tagged_rows_against_the_cut`

Old text:

```
        f"{len(rows.vox_tagged())} of {len(adding)} added row(s), each whose voxlevel "
```

New text:

```
        f"{len(adding)} of {len(adding)} added row(s), each whose voxlevel "
```

### `u127.L2_items_carry_no_vox`

The gate items carry no score and no answer

- File: `src/cratekit/intake/land_cli.py`
- Source: `u127.json`, row `L2_items_carry_no_vox`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 549 against a baseline of 549
- Kills: 6 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[above]`
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[below]`
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[exactly-at-the-cut]`
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[zero]`
  - `tests/test_intake_land_vox_native.py::test_a_tag_written_under_a_removed_category_is_said_and_never_counted`
  - `tests/test_intake_land_vox_native.py::test_the_digest_moves_when_a_tag_is_planned`

Old text:

```
        if row.action == native.ADD and rows.vox_cut is not None and not rows.vox_blocked:
```

New text:

```
        if False:
```

### `u127.L3_totals_from_writer`

Count the written associations as tagged instead of what adoption reads back

- File: `src/cratekit/intake/land_cli.py`
- Source: `u127.json`, row `L3_totals_from_writer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 549 against a baseline of 549
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_tag_written_under_a_removed_category_is_said_and_never_counted`

Old text:

```
    voxed = sum(1 for row in landed.collection.added if row.vox)
```

New text:

```
    voxed = landed.collection.vox_written
```

### `u127.L4_missing_unsaid`

Say nothing when a planned tag does not read back

- File: `src/cratekit/intake/land_cli.py`
- Source: `u127.json`, row `L4_missing_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 549 against a baseline of 549
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_tag_written_under_a_removed_category_is_said_and_never_counted`

Old text:

```
    if collection.vox_missing:
```

New text:

```
    if False:
```

### `u127.L5_unscored_unsaid`

Say nothing about a file with no score

- File: `src/cratekit/intake/land_cli.py`
- Source: `u127.json`, row `L5_unscored_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 549 against a baseline of 549
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_file_with_no_score_gets_no_tag_and_is_named`

Old text:

```
    if not collection.vox_unscored:
```

New text:

```
    if True:
```

### `u127.L6_bridge_ignores_calibration`

The bridge names the vocals verb as owed on an uncalibrated library

- File: `src/cratekit/intake/land_cli.py`
- Source: `u127.json`, row `L6_bridge_ignores_calibration`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 549 against a baseline of 549
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_the_first_run_stops_at_the_gate_and_moves_nothing`

Old text:

```
    if cut is None:
        return f"{BRIDGE_VOX_NONE}, and {native.VOX_UNCALIBRATED}"
```

New text:

```
    if False:
        return f"{BRIDGE_VOX_NONE}, and {native.VOX_UNCALIBRATED}"
```

### `u127.L7_land_warnings_unsaid`

intake land gives no vox warning

- File: `src/cratekit/intake/land_cli.py`
- Source: `u127.json`, row `L7_land_warnings_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 549 against a baseline of 549
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_three_files_become_three_rows_and_one_playlist_under_the_adopted_root`
  - `tests/test_intake_land_vox_native.py::test_a_file_with_no_score_gets_no_tag_and_is_named`
  - `tests/test_intake_land_vox_native.py::test_a_library_with_no_calibration_tags_nothing_and_says_why`
  - `tests/test_intake_land_vox_native.py::test_a_library_with_no_category_to_copy_tags_nothing_and_lands_the_batch`
  - `tests/test_intake_land_vox_native.py::test_a_tag_written_under_a_removed_category_is_said_and_never_counted`
  - `tests/test_intake_land_vox_native.py::test_an_unreadable_calibration_tags_nothing_and_lands_the_batch`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order`

Old text:

```
    warnings.extend(vox_warnings(landed.collection))
```

New text:

```
    warnings.extend([])
```

### `u111-a.A1_folder_refused`

The writer no longer refuses a folder or smart playlist as the node it moves or removes

- File: `src/cratekit/core/rb_writer.py`
- Source: `u111-a.json`, row `A1_folder_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_rb_writer_guard.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_the_writer_refuses_to_move_or_remove_a_folder`

Old text:

```
    if int(getattr(playlist, "Attribute", -1)) != 0:
        raise _node_refusal(
```

New text:

```
    if False:
        raise _node_refusal(
```

### `u111-a.A3_parent_not_folder`

move_playlist_node no longer refuses a parent that is not a live folder

- File: `src/cratekit/core/rb_writer.py`
- Source: `u111-a.json`, row `A3_parent_not_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_rb_writer_guard.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_the_writer_refuses_a_parent_that_is_not_a_folder`

Old text:

```
    if not _is_folder(parent) or node_removed(parent):
```

New text:

```
    if False:
```

### `u111-a.A4_memberships_unmarked`

remove_playlist_node marks the node and leaves its own memberships live

- File: `src/cratekit/core/rb_writer.py`
- Source: `u111-a.json`, row `A4_memberships_unmarked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_rb_writer_guard.py`
- Collected: 253 against a baseline of 253
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_a_batch_moved_past_expiry_is_removed_by_the_next_run_and_then_nothing`
  - `tests/test_inbox_rotate.py::test_the_forty_and_the_hundred_move_the_old_one_hundred_twenty_goes_and_no_track_moves`

Old text:

```
    marked = remove_memberships(db, playlist, held)
    setattr(playlist, SOFT_DELETE_COLUMN, 1)
```

New text:

```
    marked = list(held)
    setattr(playlist, SOFT_DELETE_COLUMN, 1)
```

### `u111-a.A5_node_unmarked`

remove_playlist_node marks the memberships and never the node itself

- File: `src/cratekit/core/rb_writer.py`
- Source: `u111-a.json`, row `A5_node_unmarked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_rb_writer_guard.py`
- Collected: 253 against a baseline of 253
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_a_batch_moved_past_expiry_is_removed_by_the_next_run_and_then_nothing`
  - `tests/test_inbox_rotate.py::test_the_forty_and_the_hundred_move_the_old_one_hundred_twenty_goes_and_no_track_moves`

Old text:

```
    setattr(playlist, SOFT_DELETE_COLUMN, 1)
    playlist.updated_at = datetime.now()
    return marked
```

New text:

```
    playlist.updated_at = datetime.now()
    return marked
```

### `u111-a.A6_playlist_not_removable`

REMOVABLE_TABLES loses the playlist table, so the rotation's commit cannot carry a removed node

- File: `src/cratekit/core/rb_writer.py`
- Source: `u111-a.json`, row `A6_playlist_not_removable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_rb_writer_guard.py`
- Collected: 254 against a baseline of 253
- Kills: 6 (collect-error)
- Note: collection changed: 254 collected against a baseline of 253. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_inbox_rotate.py::test_a_batch_moved_past_expiry_is_removed_by_the_next_run_and_then_nothing`
  - `tests/test_inbox_rotate.py::test_a_commit_naming_the_rotation_tables_admits_a_node_marker_and_no_content_marker`
  - `tests/test_inbox_rotate.py::test_a_second_run_plans_nothing_and_still_asks`
  - `tests/test_inbox_rotate.py::test_old_is_created_once_and_the_second_run_reuses_it`
  - `tests/test_inbox_rotate.py::test_the_forty_and_the_hundred_move_the_old_one_hundred_twenty_goes_and_no_track_moves`
  - `tests/test_rb_writer_guard.py::test_the_removable_tables_are_exactly_the_membership_and_playlist_tables`

Old text:

```
REMOVABLE_TABLES = frozenset({MEMBERSHIP_TABLE, PLAYLIST_TABLE})
```

New text:

```
REMOVABLE_TABLES = frozenset({MEMBERSHIP_TABLE})
```

### `u111-a.A7_content_compared`

The node judge no longer compares the content table

- File: `src/cratekit/core/rb_writer.py`
- Source: `u111-a.json`, row `A7_content_compared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_rb_writer_guard.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after0-djmdContent]`

Old text:

```
    if before.content != after.content:
        changed = sorted(
```

New text:

```
    if False:
        changed = sorted(
```

### `u111-b.A10_renumber_scoped`

The node judge admits a position change in any parent, not only one a node left or joined

- File: `src/cratekit/core/rb_writer.py`
- Source: `u111-b.json`, row `A10_renumber_scoped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_rb_writer_guard.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_a_renumbering_outside_the_parents_a_node_left_or_joined`

Old text:

```
        elif str(old[parent_at]) in renumbered:
            allowed = _SIBLING_COLUMNS
        else:
            allowed = frozenset()
```

New text:

```
        else:
            allowed = _SIBLING_COLUMNS
```

### `u111-b.A12_removed_keeps_no_live`

The node judge no longer asks that a removed node keeps no live membership

- File: `src/cratekit/core/rb_writer.py`
- Source: `u111-b.json`, row `A12_removed_keeps_no_live`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_rb_writer_guard.py`
- Collected: 253 against a baseline of 253
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_a_planned_change_that_was_never_made`
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after3-is still live]`

Old text:

```
        if str(row[owner_at]) in gone and not row[m_marker]:
```

New text:

```
        if False:
```

### `u111-b.A13_confinement_raises`

assert_node_changes_confined computes the violations and never raises

- File: `src/cratekit/core/rb_writer.py`
- Source: `u111-b.json`, row `A13_confinement_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_rb_writer_guard.py`
- Collected: 253 against a baseline of 253
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_a_move_that_lands_somewhere_else_is_refused_and_rolled_back`
  - `tests/test_inbox_rotate.py::test_a_removal_that_reaches_another_playlists_membership_is_refused_and_rolled_back`

Old text:

```
    violations = node_change_violations(
        before, after, moved=moved, removed=removed, created=created
    )
    if violations:
        db.rollback()
```

New text:

```
    violations = node_change_violations(
        before, after, moved=moved, removed=removed, created=created
    )
    if False:
        db.rollback()
```

### `u111-b.A8_membership_owner`

The node judge admits a changed membership in any playlist, not only a removed one

- File: `src/cratekit/core/rb_writer.py`
- Source: `u111-b.json`, row `A8_membership_owner`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_rb_writer_guard.py`
- Collected: 253 against a baseline of 253
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_a_removal_that_reaches_another_playlists_membership_is_refused_and_rolled_back`
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after1-only a removed playlist]`

Old text:

```
        owner = str(old[owner_at])
        if owner not in gone:
```

New text:

```
        owner = str(old[owner_at])
        if False:
```

### `u111-b.A9_planned_move_made`

The node judge no longer asks whether each planned move sits live under its folder

- File: `src/cratekit/core/rb_writer.py`
- Source: `u111-b.json`, row `A9_planned_move_made`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_rb_writer_guard.py`
- Collected: 253 against a baseline of 253
- Kills: 4 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_a_move_that_lands_somewhere_else_is_refused_and_rolled_back`
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_a_planned_change_that_was_never_made`
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after5-not live under the planned]`
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after6-not live under the planned]`

Old text:

```
        if new is None or str(new[parent_at]) != planned_moves[key] or new[marker_at]:
```

New text:

```
        if new is None:
```

### `u81-fetch-b.L1_two_files_first_wins`

A download that left two MP3 files hands the first one on as the track

- File: `src/cratekit/acquire/fallback.py`
- Source: `u81-fetch-b.json`, row `L1_two_files_first_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_the_shipped_fetcher_never_reads_a_failure_as_a_file[two]`

Old text:

```
    if len(found) != 1:
```

New text:

```
    if len(found) == 0:
```

### `u81-fetch-b.L2_any_suffix`

The landing is not required to be MP3, so an unconverted upload is handed on

- File: `src/cratekit/acquire/fallback.py`
- Source: `u81-fetch-b.json`, row `L2_any_suffix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_the_shipped_fetcher_never_reads_a_failure_as_a_file[not-mp3]`

Old text:

```
            if one.is_file() and one.suffix.lower() == FETCH_SUFFIX
```

New text:

```
            if one.is_file()
```

### `u81-fetch-b.Y1_no_option_terminator`

The address is passed without the option terminator in front of it

- File: `src/cratekit/acquire/fallback.py`
- Source: `u81-fetch-b.json`, row `Y1_no_option_terminator`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_the_shipped_fetcher_extracts_mp3_drops_upload_metadata_and_ends_on_the_address`

Old text:

```
            "--",
            url,
```

New text:

```
            url,
```

### `u81-fetch-b.Y2_metadata_kept_on_convert`

The metadata drop is not passed to the conversion step

- File: `src/cratekit/acquire/fallback.py`
- Source: `u81-fetch-b.json`, row `Y2_metadata_kept_on_convert`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_the_shipped_fetcher_extracts_mp3_drops_upload_metadata_and_ends_on_the_address`

Old text:

```
            "--postprocessor-args",
            "ExtractAudio:-map_metadata -1",

```

New text:

```
(empty)
```

### `u81-fetch-b.Y3_failed_exit_is_a_file`

A download exiting nonzero is read as a landing whenever it left a file

- File: `src/cratekit/acquire/fallback.py`
- Source: `u81-fetch-b.json`, row `Y3_failed_exit_is_a_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_the_shipped_fetcher_never_reads_a_failure_as_a_file[nonzero]`

Old text:

```
        if done.returncode != 0:
            said = (done.stderr or "").strip().splitlines()
            raise FallbackUnavailable(
                f"the download failed
```

New text:

```
        if False:
            said = (done.stderr or "").strip().splitlines()
            raise FallbackUnavailable(
                f"the download failed
```

### `u81-fetch-a.W10_untaggable_committed`

A landing that could not be tagged from its row is committed anyway

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `u81-fetch-a.json`, row `W10_untaggable_committed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_a_file_that_cannot_be_tagged_from_its_row_is_not_committed`

Old text:

```
    if not written:
        raise refuse(
            "unavailable-transient",
            untagged,
```

New text:

```
    if False:
        raise refuse(
            "unavailable-transient",
            untagged,
```

### `u81-fetch-a.W12_download_failure_not_retryable`

A failed download is refused as final rather than retryable

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `u81-fetch-a.json`, row `W12_download_failure_not_retryable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_a_failed_download_is_transient_and_stays_retryable`

Old text:

```
            f"queued",
            remedy=Remedy.RETRY_LATER,
            scope=Scope.ITEM,
            retryable=True,
```

New text:

```
            f"queued",
            remedy=Remedy.RETRY_LATER,
            scope=Scope.ITEM,
            retryable=False,
```

### `u81-fetch-a.W1_strict_not_refused`

The strict policy refusal before the download is removed, so a lossy upload is fetched under strict

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `u81-fetch-a.json`, row `W1_strict_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_a_strict_policy_refuses_that_item_before_anything_downloads`

Old text:

```
    if not decision.permitted:
        raise refuse(
            "lossy-refused",
```

New text:

```
    if False:
        raise refuse(
            "lossy-refused",
```

### `u81-fetch-a.W3_host_half`

The web address check keeps only its scheme half, so an address with no host is handed to the tool

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `u81-fetch-a.json`, row `W3_host_half`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_an_accepted_option_that_is_not_a_web_address_is_never_handed_to_the_tool[https://]`

Old text:

```
    if where.scheme not in ("http", "https") or not where.netloc:
```

New text:

```
    if where.scheme not in ("http", "https"):
```

### `u81-fetch-a.W5_pre_download_exists`

The name already taken is no longer checked before the download, so one is spent on it

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `u81-fetch-a.json`, row `W5_pre_download_exists`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_an_existing_output_is_refused_without_a_download`

Old text:

```
    if expected.exists():
        raise _exists(expected, detail)
```

New text:

```
    if False:
        raise _exists(expected, detail)
```

### `u81-fetch-a.W6_post_landing_exists`

A file that appeared during the download is no longer checked, so the engine commits over it

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `u81-fetch-a.json`, row `W6_post_landing_exists`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_an_output_that_appears_during_the_download_is_refused_not_replaced`

Old text:

```
    if final.exists():
        raise _exists(final, detail)
```

New text:

```
    if False:
        raise _exists(final, detail)
```

### `u81-fetch-a.W7_final_unmarked`

The committed name ignores the policy decision and is never marked

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `u81-fetch-a.json`, row `W7_final_unmarked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 4 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_a_lossy_file_lands_marked`
  - `tests/test_acquire_fallback_fetch.py::test_a_tempo_the_upload_carried_is_never_committed`
  - `tests/test_acquire_fallback_fetch.py::test_an_output_that_appears_during_the_download_is_refused_not_replaced`
  - `tests/test_acquire_fallback_fetch.py::test_artist_and_title_tags_come_from_the_row_not_the_upload_page`

Old text:

```
        Path(stem + landed.suffix), marker, required=decision.marker_required
```

New text:

```
        Path(stem + landed.suffix), marker, required=False
```

### `u81-fetch-a.W8_upload_tags_kept`

The upload's own tag block is not stripped before the row's artist and title are written

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `u81-fetch-a.json`, row `W8_upload_tags_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_a_tempo_the_upload_carried_is_never_committed`

Old text:

```
        written = tags.strip_tags(landed) and tags.write_tags(
```

New text:

```
        written = tags.write_tags(
```

### `u81-fetch-a.W9_row_tags_not_written`

The row's artist and title are never written, so the file carries no name at all

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `u81-fetch-a.json`, row `W9_row_tags_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_a_tempo_the_upload_carried_is_never_committed`
  - `tests/test_acquire_fallback_fetch.py::test_artist_and_title_tags_come_from_the_row_not_the_upload_page`

Old text:

```
            landed, {"artist": artist or None, "title": title or None}
```

New text:

```
            landed, {"artist": None, "title": None}
```

### `u81-fetch-b.Q1_provider_route_fetched_lossy`

A row with a provider route is queued for a lossy second source download anyway

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `u81-fetch-b.json`, row `Q1_provider_route_fetched_lossy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_a_row_with_a_provider_route_is_not_fetched_lossy`

Old text:

```
        if provider_routed(items, one):
            continue
        said = fallback.settled(items, one)
```

New text:

```
        said = fallback.settled(items, one)
```

### `u81-fetch-b.Q3_empty_queue`

A list with nothing accepted queues a job anyway instead of reporting a no-op

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `u81-fetch-b.json`, row `Q3_empty_queue`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 4 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_a_row_the_library_already_holds_is_not_fetched`
  - `tests/test_acquire_fallback_fetch.py::test_a_row_with_a_provider_route_is_not_fetched_lossy`
  - `tests/test_acquire_fallback_fetch.py::test_an_acceptance_naming_no_upload_of_several_is_not_queued`
  - `tests/test_acquire_fallback_fetch.py::test_nothing_accepted_queues_nothing_and_says_so`

Old text:

```
    if not rows:
        return ctx.envelope(
```

New text:

```
    if False:
        return ctx.envelope(
```

### `u81-fetch-b.W2_scheme_half_rerun`

Re-run of W2: the web address check keeps only its host half

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `u81-fetch-b.json`, row `W2_scheme_half_rerun`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_an_accepted_option_that_is_not_a_web_address_is_never_handed_to_the_tool[file://localhost/etc/hosts]`
  - `tests/test_acquire_fallback_fetch.py::test_an_accepted_option_that_is_not_a_web_address_is_never_handed_to_the_tool[ftp://uploads.example/track.mp3]`

Old text:

```
    if where.scheme not in ("http", "https") or not where.netloc:
```

New text:

```
    if not where.netloc:
```

### `u81-fetch-b.W4_empty_stem_rerun`

Re-run of W4: a row naming no artist and no title is fetched and committed

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `u81-fetch-b.json`, row `W4_empty_stem_rerun`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_a_row_naming_no_artist_and_no_title_is_refused_before_a_download`

Old text:

```
    if not stem:
        raise refuse(
```

New text:

```
    if False:
        raise refuse(
```

### `r227.A1_floored_days`

Staleness is judged on floored whole days, so seven days and one second is not past seven

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r227.json`, row `A1_floored_days`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_sync_all.py`
- Collected: 371 against a baseline of 371
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_old_means_past_the_limit_and_not_at_it`
  - `tests/test_outbound_workers.py::test_the_sentence_does_not_say_seven_is_past_seven`

Old text:

```
        return age is not None and age.total_seconds() > self.limit_days * _SECONDS_PER_DAY
```

New text:

```
        return age is not None and age.days > self.limit_days
```

### `r227.A2_never_stale`

No export is ever stale, which is the tree before this unit

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r227.json`, row `A2_never_stale`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_sync_all.py`
- Collected: 371 against a baseline of 371
- Kills: 13 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_month_old_export_is_called_old_in_the_plan_the_gate_shows[export.playlist]`
  - `tests/test_outbound_workers.py::test_a_month_old_export_is_called_old_in_the_plan_the_gate_shows[sync.favorites]`
  - `tests/test_outbound_workers.py::test_old_means_past_the_limit_and_not_at_it`
  - `tests/test_outbound_workers.py::test_the_date_is_the_persons_own_and_not_greenwichs`
  - `tests/test_outbound_workers.py::test_the_date_reaches_a_person_who_is_not_reading_json[export.playlist]`
  - `tests/test_outbound_workers.py::test_the_date_reaches_a_person_who_is_not_reading_json[sync.favorites]`
  - `tests/test_outbound_workers.py::test_the_limit_is_the_configured_one_in_both_directions[export.playlist]`
  - `tests/test_outbound_workers.py::test_the_limit_is_the_configured_one_in_both_directions[sync.favorites]`
  - `tests/test_outbound_workers.py::test_the_queueing_envelope_warns_that_the_export_is_old[export.playlist]`
  - `tests/test_outbound_workers.py::test_the_queueing_envelope_warns_that_the_export_is_old[sync.favorites]`
  - `tests/test_outbound_workers.py::test_the_sentence_does_not_say_seven_is_past_seven`
  - `tests/test_sync_all.py::test_a_pass_that_queued_over_an_old_export_warns_and_still_queues`
  - `tests/test_sync_all.py::test_the_composed_gate_names_the_exports_date_beside_what_would_queue`

Old text:

```
        return age is not None and age.total_seconds() > self.limit_days * _SECONDS_PER_DAY
```

New text:

```
        return False
```

### `r227.A3_future_clamped`

A date far in the future is never future dated, so it clamps to an age of nothing and reads as recent

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r227.json`, row `A3_future_clamped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_sync_all.py`
- Collected: 371 against a baseline of 371
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_date_well_in_the_future_is_not_the_freshest_export_there_could_be`

Old text:

```
        return self.written - self.judged_at > FUTURE_TOLERANCE
```

New text:

```
        return False
```

### `r227.A4_no_tolerance`

No tolerance at all, so a volume whose clock runs a few hours ahead is future dated

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r227.json`, row `A4_no_tolerance`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_sync_all.py`
- Collected: 371 against a baseline of 371
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_few_hours_ahead_is_a_clock_and_reads_as_written_just_now`

Old text:

```
FUTURE_TOLERANCE = timedelta(days=1)
```

New text:

```
FUTURE_TOLERANCE = timedelta(0)
```

### `r227.A5_half_a_pair`

The constructor accepts a date with no instant to judge it at

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r227.json`, row `A5_half_a_pair`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_sync_all.py`
- Collected: 371 against a baseline of 371
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_an_age_is_built_whole_or_not_at_all`

Old text:

```
        if (self.written is None) != (self.judged_at is None):
```

New text:

```
        if False:
```

### `r227.A6_conversion_unguarded`

Only the stat is guarded, so a modification time no date can hold escapes as a traceback

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r227.json`, row `A6_conversion_unguarded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_sync_all.py`
- Collected: 371 against a baseline of 371
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_modification_time_no_date_can_hold_is_unknown_rather_than_a_crash`

Old text:

```
    except (OSError, OverflowError, ValueError):
```

New text:

```
    except FileNotFoundError:
```

### `r227.A7_unreadable_reads_as_now`

A file that cannot be asked its date is reported as written this instant

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r227.json`, row `A7_unreadable_reads_as_now`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_sync_all.py`
- Collected: 371 against a baseline of 371
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_modification_time_no_date_can_hold_is_unknown_rather_than_a_crash`
  - `tests/test_outbound_workers.py::test_an_age_that_cannot_be_read_is_unknown_rather_than_fresh`

Old text:

```
        return ExportAge(path=located, limit_days=limit_days)

```

New text:

```
        return ExportAge(path=located, limit_days=limit_days, written=datetime.now(timezone.utc), judged_at=datetime.now(timezone.utc))

```

### `r356-b.B1_naming_head_left_on_the_release_title`

The release title is the display title, key and tempo head and all, which agrees with no provider title

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r356-b.json`, row `B1_naming_head_left_on_the_release_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_sync_all.py`
- Collected: 371 against a baseline of 371
- Kills: 8 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_configuration_with_no_marker_text_still_strips_the_head`
  - `tests/test_outbound_tidal_account.py::test_a_release_the_account_already_hearts_is_the_one_an_export_adds`
  - `tests/test_outbound_tidal_account.py::test_a_sweep_hearts_the_release_the_files_album_tag_names`
  - `tests/test_outbound_tidal_account.py::test_a_sweep_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_tidal_account.py::test_an_export_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_tidal_account.py::test_the_release_title_is_the_display_title_with_the_naming_head_off`
  - `tests/test_outbound_workers.py::test_a_favourite_whose_isrc_names_several_tracks_is_listed_with_that_reason`
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`

Old text:

```
    return naming.strip_heads(entry.name, template=template)
```

New text:

```
    return entry.name
```

### `r356-b.B4_heart_candidate_carries_no_artist`

A favourite reaches the account with a title and no artist, which chooses nothing

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r356-b.json`, row `B4_heart_candidate_carries_no_artist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_sync_all.py`
- Collected: 371 against a baseline of 371
- Kills: 4 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_sweep_hearts_the_release_the_files_album_tag_names`
  - `tests/test_outbound_tidal_account.py::test_a_sweep_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_workers.py::test_a_favourite_whose_isrc_names_several_tracks_is_listed_with_that_reason`
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`

Old text:

```
            release_title=release_title(entry, template=template),
            artist=entry.artist,

```

New text:

```
            release_title=release_title(entry, template=template),

```

### `u179-z.S4_to_fetch_counts_held`

_plan: count only new purchases, so a plan holding only part owned releases reads as nothing new

- File: `src/cratekit/cli/sync_bandcamp.py`
- Source: `u179-z.json`, row `S4_to_fetch_counts_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_plan_holding_only_part_owned_releases_still_fetches_the_rest`

Old text:

```
    to_fetch = int(summary.get("new") or 0) + int(summary.get("held") or 0)
```

New text:

```
    to_fetch = int(summary.get("new") or 0)
```

### `u179-z.S9_refusals_need_permanence`

_fetched: read a fetch failed by a retryable item as settled too, so a transient failure lands the rest

- File: `src/cratekit/cli/sync_bandcamp.py`
- Source: `u179-z.json`, row `S9_refusals_need_permanence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_fetch_failed_by_a_transient_answer_ends_the_verb_and_lands_nothing`

Old text:

```
    settled_with_refusals = job.state is jobs.JobState.FAILED and len(permanent) == len(failed)
```

New text:

```
    settled_with_refusals = job.state is jobs.JobState.FAILED
```

### `u179.D1_fetched_once`

_fetched: count every done item as staged, so a release two fetches held is named twice

- File: `src/cratekit/cli/sync_bandcamp.py`
- Source: `u179.json`, row `D1_fetched_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_two_fetches_left_open_in_the_batch_are_both_driven_on_oldest_first`

Old text:

```
    staged = [item for item in done if item.item_id not in seen]
```

New text:

```
    staged = list(done)
```

### `u179.D2_refused_once`

_fetched: name a release each time a fetch refuses it, the second round's same shape one list over

- File: `src/cratekit/cli/sync_bandcamp.py`
- Source: `u179.json`, row `D2_refused_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_release_refused_by_two_fetches_is_named_once`

Old text:

```
        if item.item_id not in taken and item.item_id not in already
```

New text:

```
        if item.item_id not in taken
```

### `u179.S10_open_fetch_stops`

_fetched: drop the stop on a fetch that did not settle, so a parked fetch goes on to the tail

- File: `src/cratekit/cli/sync_bandcamp.py`
- Source: `u179.json`, row `S10_open_fetch_stops`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`
- Collected: 34 against a baseline of 34
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_fetch_failed_by_a_transient_answer_ends_the_verb_and_lands_nothing`
  - `tests/test_sync_bandcamp.py::test_a_fetch_parked_by_the_session_ends_blocked_and_the_next_run_drives_it_on`

Old text:

```
    if job.state is not jobs.JobState.SUCCEEDED and not settled_with_refusals:
        raise tail.Stop(FETCH, tail.job_error(report, job))
```

New text:

```
    if False:
        raise tail.Stop(FETCH, tail.job_error(report, job))
```

### `u179.S13_nothing_staged_ends`

sync_bandcamp: drop the empty folder end, so the tail is run over a folder holding nothing

- File: `src/cratekit/cli/sync_bandcamp.py`
- Source: `u179.json`, row `S13_nothing_staged_ends`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`
- Collected: 34 against a baseline of 34
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_release_refused_by_two_fetches_is_named_once`
  - `tests/test_sync_bandcamp.py::test_a_release_refused_for_good_is_recorded_and_nothing_is_landed_over_none`
  - `tests/test_sync_bandcamp.py::test_a_second_run_after_a_landing_finds_nothing_new_and_lands_nothing`
  - `tests/test_sync_bandcamp.py::test_nothing_new_ends_with_no_fetch_no_tail_and_no_landing`

Old text:

```
        if not files:
            report.check(
```

New text:

```
        if False:
            report.check(
```

### `u179.S14_relist_after_name`

sync_bandcamp: read the tags of the files as staged before name apply renamed them

- File: `src/cratekit/cli/sync_bandcamp.py`
- Source: `u179.json`, row `S14_relist_after_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_the_tags_are_read_from_the_files_the_name_step_renamed`

Old text:

```
        folder = tail.through_name(report, folder, cfg)
        files = _staged(folder)
```

New text:

```
        folder = tail.through_name(report, folder, cfg)
```

### `u179.S15_unread_apart`

_read_tags: count a file whose tags could not be read as a file with no genre

- File: `src/cratekit/cli/sync_bandcamp.py`
- Source: `u179.json`, row `S15_unread_apart`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_file_whose_tags_cannot_be_read_is_unread_not_ungenred_and_names_no_label`

Old text:

```
            report.summary["tags_unread"].append(path.name)
```

New text:

```
            report.summary["no_genre"].append(path.name)
```

### `u179.S16_no_genre_named`

_read_tags: never name a file with no genre

- File: `src/cratekit/cli/sync_bandcamp.py`
- Source: `u179.json`, row `S16_no_genre_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_files_left_without_a_genre_are_named_in_the_report`

Old text:

```
        if not (read.get("genre") or "").strip():
```

New text:

```
        if False:
```

### `u179.S17_label_flag_needs_a_label`

_landing: pass --label-from-tags whether or not any file carries a label tag

- File: `src/cratekit/cli/sync_bandcamp.py`
- Source: `u179.json`, row `S17_label_flag_needs_a_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_seller_no_label_names_lands_unlabelled_and_is_named`

Old text:

```
    if any(read.labels):
```

New text:

```
    if True:
```

### `u179.S1_fetch_only_when_planned`

sync_bandcamp: fetch whatever the plan said, so a plan with nothing new still queues a fetch

- File: `src/cratekit/cli/sync_bandcamp.py`
- Source: `u179.json`, row `S1_fetch_only_when_planned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`
- Collected: 34 against a baseline of 34
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_second_run_after_a_landing_finds_nothing_new_and_lands_nothing`
  - `tests/test_sync_bandcamp.py::test_nothing_new_ends_with_no_fetch_no_tail_and_no_landing`
  - `tests/test_sync_bandcamp.py::test_the_same_batch_again_takes_the_staged_files_on_and_fetches_nothing_twice`

Old text:

```
        if planned:
            _fetch(report, cfg, batch, sellers)
```

New text:

```
        if True:
            _fetch(report, cfg, batch, sellers)
```

### `u179.S2_owned_recorded`

_plan: never record an owned purchase, so the report names nothing held as owned

- File: `src/cratekit/cli/sync_bandcamp.py`
- Source: `u179.json`, row `S2_owned_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`
- Collected: 34 against a baseline of 34
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_labels_new_release_and_its_owned_one_reach_the_gate_named_for_the_label`
  - `tests/test_sync_bandcamp.py::test_nothing_new_ends_with_no_fetch_no_tail_and_no_landing`
  - `tests/test_sync_bandcamp.py::test_the_labels_release_reaches_the_same_gate_with_rekordbox_open_on_the_host`
  - `tests/test_sync_bandcamp_native.py::test_one_new_puls_release_and_one_owned_land_one_batch_filed_under_its_label`

Old text:

```
        if row.get("disposition") == OWNED:
```

New text:

```
        if row.get("disposition") == "none":
```

### `u179.S3_held_recorded`

_plan: never record a purchase with tracks held back, so those owned tracks go unnamed

- File: `src/cratekit/cli/sync_bandcamp.py`
- Source: `u179.json`, row `S3_held_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`
- Collected: 34 against a baseline of 34
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_labels_new_release_and_its_owned_one_reach_the_gate_named_for_the_label`
  - `tests/test_sync_bandcamp.py::test_a_plan_holding_only_part_owned_releases_still_fetches_the_rest`
  - `tests/test_sync_bandcamp.py::test_the_labels_release_reaches_the_same_gate_with_rekordbox_open_on_the_host`

Old text:

```
        elif row.get("disposition") == HELD:
```

New text:

```
        elif row.get("disposition") == "none":
```

### `u179.S5_open_fetch_elsewhere`

_open_fetch: drop the other batch test, so an open fetch into another batch is driven into this one

- File: `src/cratekit/cli/sync_bandcamp.py`
- Source: `u179.json`, row `S5_open_fetch_elsewhere`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_an_open_fetch_into_another_batch_is_named_and_nothing_is_fetched`

Old text:

```
        if _batch_of(job) != batch:
            raise _Elsewhere(job, _batch_of(job))
```

New text:

```
        if False:
            raise _Elsewhere(job, _batch_of(job))
```

### `u179.S6_open_fetches_all`

_open_fetch: drive only the newest open fetch, the round one residual

- File: `src/cratekit/cli/sync_bandcamp.py`
- Source: `u179.json`, row `S6_open_fetches_all`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_two_fetches_left_open_in_the_batch_are_both_driven_on_oldest_first`

Old text:

```
    return list(reversed(held))
```

New text:

```
    return held[:1]
```

### `u179.S7_open_fetch_order`

_open_fetch: drive the open fetches newest first rather than oldest first

- File: `src/cratekit/cli/sync_bandcamp.py`
- Source: `u179.json`, row `S7_open_fetch_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_two_fetches_left_open_in_the_batch_are_both_driven_on_oldest_first`

Old text:

```
    return list(reversed(held))
```

New text:

```
    return list(held)
```

### `u179.S8_refusals_settle`

_fetched: never read a fetch failed only by refusals as settled, so one lossy release ends the verb

- File: `src/cratekit/cli/sync_bandcamp.py`
- Source: `u179.json`, row `S8_refusals_settle`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`
- Collected: 34 against a baseline of 34
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_release_refused_by_two_fetches_is_named_once`
  - `tests/test_sync_bandcamp.py::test_a_release_refused_for_good_is_recorded_and_nothing_is_landed_over_none`

Old text:

```
    settled_with_refusals = job.state is jobs.JobState.FAILED and len(permanent) == len(failed)
```

New text:

```
    settled_with_refusals = False
```

### `u179.T1_rehearsal_runs`

sync_bandcamp: skip the rehearsal, so the landing is planned with none behind it

- File: `src/cratekit/cli/sync_bandcamp.py`
- Source: `u179.json`, row `T1_rehearsal_runs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`
- Collected: 34 against a baseline of 34
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_failed_rehearsal_plans_no_live_landing`
  - `tests/test_sync_bandcamp.py::test_a_labels_new_release_and_its_owned_one_reach_the_gate_named_for_the_label`
  - `tests/test_sync_bandcamp.py::test_a_rehearsal_that_needs_the_acknowledgment_names_the_rehearsal_then_the_landing`
  - `tests/test_sync_bandcamp.py::test_the_labels_release_reaches_the_same_gate_with_rekordbox_open_on_the_host`
  - `tests/test_sync_bandcamp_native.py::test_one_new_puls_release_and_one_owned_land_one_batch_filed_under_its_label`

Old text:

```
        tail.rehearse(report, folder, landing)
```

New text:

```
        pass
```

### `u214.M15_unread_is_not_none`

_classify: say no landing record names an unrecognised playlist even while a session record could not be read

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M15_unread_is_not_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 201 against a baseline of 201
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_playlist_whose_record_cannot_be_read_is_never_said_to_have_none`
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`

Old text:

```
            if unread
            else
```

New text:

```
            if False
            else
```

### `u214.M16_old_only_under_inbox`

_classify: read a folder named Old inside Old as the Old folder too

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M16_old_only_under_inbox`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 201 against a baseline of 201
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_folder_named_old_inside_old_is_a_folder_and_listed_as_yours`

Old text:

```
        if not in_old and old_display is not None and name == old_display:
```

New text:

```
        if old_display is not None and name == old_display:
```

### `u214.M18_folder_unknown`

_batch_folder: read a refused batch folder as absent, so a batch is said to have none

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M18_folder_unknown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 201 against a baseline of 201
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_music_folder_that_cannot_be_read_is_never_read_as_no_batch_folder`

Old text:

```
    except OSError:
        return None
```

New text:

```
    except OSError:
        return False
```

### `u214.M19_folder_unread_reason`

_classify: say no batch folder carries the name even while the music folder could not be read

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M19_folder_unread_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 201 against a baseline of 201
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_music_folder_that_cannot_be_read_is_never_read_as_no_batch_folder`

Old text:

```
            if folder_unread

```

New text:

```
            if False

```

### `u214.M1_old_named_as_old`

_classify: never name the declared Old as Old, so it reads as any folder

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M1_old_named_as_old`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 201 against a baseline of 201
- Kills: 5 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_folder_named_old_inside_old_is_a_folder_and_listed_as_yours`
  - `tests/test_inbox_unmirrored.py::test_the_inbox_folder_mirrors_the_batch_and_names_the_other_nodes`
  - `tests/test_inbox_unmirrored.py::test_the_live_batches_name_every_other_node_under_inbox_with_its_kind`
  - `tests/test_inbox_unmirrored.py::test_the_organize_rotation_step_does_not_list_old_as_yours`
  - `tests/test_inbox_unmirrored.py::test_the_rotation_plan_names_the_same_nodes_the_same_way`

Old text:

```
        if not in_old and old_display is not None and name == old_display:
```

New text:

```
        if False:
```

### `u214.M20_unread_unlisted`

Landings.unread: say nothing of a log that could not be listed

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M20_unread_unlisted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 201 against a baseline of 201
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`

Old text:

```
        if self.unlisted:
```

New text:

```
        if False:
```

### `u214.M2_left_row_count`

_classify: count no rows for a left playlist, so the unrecognised label playlist is named without its 36 rows

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M2_left_row_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 201 against a baseline of 201
- Kills: 4 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_row_added_to_a_left_playlist_does_not_move_the_rotations_digest`
  - `tests/test_inbox_unmirrored.py::test_the_inbox_folder_mirrors_the_batch_and_names_the_other_nodes`
  - `tests/test_inbox_unmirrored.py::test_the_live_batches_name_every_other_node_under_inbox_with_its_kind`
  - `tests/test_inbox_unmirrored.py::test_the_rotation_payload_shows_each_left_node_with_its_row_count`

Old text:

```
        tracks = _track_count(db, row) if counted else None
```

New text:

```
        tracks = None
```

### `u214.M3_live_left_collected`

live_batches: collect no left node, so the mirror drops them unsaid again

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M3_live_left_collected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 201 against a baseline of 201
- Kills: 8 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_dated_playlist_with_no_batch_folder_still_says_so`
  - `tests/test_inbox_unmirrored.py::test_a_music_folder_that_cannot_be_read_is_never_read_as_no_batch_folder`
  - `tests/test_inbox_unmirrored.py::test_a_playlist_whose_record_cannot_be_read_is_never_said_to_have_none`
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`
  - `tests/test_inbox_unmirrored.py::test_an_undeclared_old_is_named_as_a_folder`
  - `tests/test_inbox_unmirrored.py::test_the_inbox_folder_mirrors_the_batch_and_names_the_other_nodes`
  - `tests/test_inbox_unmirrored.py::test_the_live_batches_name_every_other_node_under_inbox_with_its_kind`
  - `tests/test_inbox_unmirrored.py::test_the_rotation_plan_names_the_same_nodes_the_same_way`

Old text:

```
        else:
            left.append(classified)
    return Live(
```

New text:

```
        else:
            pass
    return Live(
```

### `u214.M4_digest_without_count`

identity: digest each left node with its row count, so adding a track to a person's playlist stales the rotation gate

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M4_digest_without_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 201 against a baseline of 201
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_row_added_to_a_left_playlist_does_not_move_the_rotations_digest`

Old text:

```
        "left": [node.identity() for node in plan.left],
```

New text:

```
        "left": [node.to_json() for node in plan.left],
```

### `u214.M5_rotation_old_display`

plan_rotation: pass no Old display, so the rotation plan names Old as a folder and the mirror as Old

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M5_rotation_old_display`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 201 against a baseline of 201
- Kills: 3 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_folder_named_old_inside_old_is_a_folder_and_listed_as_yours`
  - `tests/test_inbox_unmirrored.py::test_the_organize_rotation_step_does_not_list_old_as_yours`
  - `tests/test_inbox_unmirrored.py::test_the_rotation_plan_names_the_same_nodes_the_same_way`

Old text:

```
            old_display=old.display,
```

New text:

```
            old_display=None,
```

### `u214.M6_live_old_display`

live_batches: read no Old display, so the mirror names Old as a plain folder

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M6_live_old_display`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 201 against a baseline of 201
- Kills: 3 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_the_inbox_folder_mirrors_the_batch_and_names_the_other_nodes`
  - `tests/test_inbox_unmirrored.py::test_the_live_batches_name_every_other_node_under_inbox_with_its_kind`
  - `tests/test_inbox_unmirrored.py::test_the_rotation_plan_names_the_same_nodes_the_same_way`

Old text:

```
    old_display = declared.intake_old.display if declared.intake_old is not None else None
```

New text:

```
    old_display = None
```

### `u214.M7_label_rows`

Left.label: leave the row count out of the line a person reads

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M7_label_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 201 against a baseline of 201
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_the_inbox_folder_mirrors_the_batch_and_names_the_other_nodes`
  - `tests/test_inbox_unmirrored.py::test_the_live_batches_name_every_other_node_under_inbox_with_its_kind`

Old text:

```
        rows = f" ({self.tracks} row(s))" if self.tracks is not None else ""
```

New text:

```
        rows = ""
```

