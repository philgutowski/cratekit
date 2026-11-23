# Mutation table: u325-before-l-11

Measured by `scripts/mutate.py` on 2026-11-23 02:51 UTC, branch `HEAD` at `539638eb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22663 collected. pytest invocations for this batch: 130.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:21 UTC for commit `539638ebe629`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 11, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22663 against 22663. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u143-d.A7_folder_empty` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 451 | 1 | killed |
| `u143-d.A8_folder_read_back` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 451 | 1 | killed |
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
| `u181.S3_stop_goes_on` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u182.M18_left_open_taken` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 2 | killed |
| `u182.M19_left_open_identity` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u182.M20_cancelled_driven` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 2 | killed |
| `u182.M21_all_cancelled_done` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u182.M22_skip_failed` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u183.M11_land_runs_named` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 2 | killed |
| `u183.M12_preflight_way_back` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u183.M14_retryable_intake_continues` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u183.M15_continue_command_words` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 9 | killed |
| `u183.M1_pass_run_as_given` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 16 | killed |
| `u183.M2_land_record_resolves` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 3 | killed |
| `u183.M3_recorded_pass_needs_a_job` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u183.M6_unreadable_record` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u183.M7_remember_saves` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u183.M8_remember_called` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 5 | killed |
| `r799-c.V1_the_gate_is_asked_before_the_write` | `src/cratekit/tagging/remap_cli.py` | user | 1 file(s) | 93 | 15 | killed |
| `r799-c.V2_a_file_that_did_not_take_refuses` | `src/cratekit/tagging/remap_cli.py` | user | 1 file(s) | 93 | 7 | killed |
| `r799-b.P1_a_file_is_planned_only_while_it_carries_what_a_record_wrote` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 15 | killed |
| `r799-b.P2_two_explanations_are_ambiguous` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 4 | killed |
| `r799-b.P3_a_shops_genre_is_the_shops` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 1 | killed |
| `r799-b.P4_a_rewrite_retires_the_record_it_replaced` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 2 | killed |
| `r799-b.P5_only_a_file_under_the_library_is_opened` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 4 | killed |
| `r799-b.P6_one_file_is_one_group` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 22663 | 0 (promoted) | zero |
| `r799-b.W1_a_file_is_read_again_before_it_is_written` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 1 | killed |
| `r799-b.W2_the_writers_answer_is_kept` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 3 | killed |
| `r799-b.W3_a_write_is_read_back` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 1 | killed |
| `r799-c.P11_blank_is_not_agreement` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 1 | killed |
| `r799-c.V3_an_unrecorded_rewrite_is_not_clean` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 2 | killed |
| `r799-c.W4_a_rewrite_is_recorded` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 5 | killed |
| `r799-c.W5_a_rewrites_record_is_one_generation_on` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 4 | killed |
| `u119-b.G5r_favorites_counted_as_members` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 45 | 1 | killed |
| `u119-c.C2_torn_bucket_bound_anyway` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 45 | 1 | killed |
| `u119-c.C5_interruption_unreported` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 45 | 3 | killed |
| `u119.G10_placements_no_gap` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 45 | 2 | killed |
| `u119.G11_stale_digest` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 45 | 2 | killed |
| `u119.G13_removals_when_not_asked` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 45 | 2 | killed |
| `u119.G15_removal_commit_admits_nothing` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 45 | 5 | killed |
| `u119.G1_class_undeclared` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 45 | 2 | killed |
| `u119.G2_source_folder_counts` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 45 | 1 | killed |
| `u119.G3_two_sources_first_wins` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 45 | 1 | killed |
| `u119.G4_removed_membership_live` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 45 | 1 | killed |
| `u119.G6_wanted_is_members` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 45 | 13 | killed |
| `u119.G7_twin_folders_first_taken` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 45 | 1 | killed |
| `u119.G9_digest_over_adds` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 45 | 1 | killed |
| `u185.R4_genre_source` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 45 | 1 | killed |
| `u119.V1_ack_after_plan` | `src/cratekit/favorites/refresh_cli.py` | user | 1 file(s) | 45 | 1 | killed |
| `r261.W1_worker_refuses` | `src/cratekit/label/cli.py` | user | 4 file(s) | 522 | 2 | killed |
| `r261.W2_remedy` | `src/cratekit/label/cli.py` | user | 4 file(s) | 522 | 1 | killed |
| `r261.W3_retryable` | `src/cratekit/label/cli.py` | user | 4 file(s) | 522 | 1 | killed |
| `r261.D1_discovery_record` | `src/cratekit/label/tidal_catalogue.py` | user | 4 file(s) | 522 | 3 | killed |
| `r261.D2_transient_class` | `src/cratekit/label/tidal_catalogue.py` | user | 4 file(s) | 522 | 1 | killed |
| `r261.D3_held_guard` | `src/cratekit/label/tidal_catalogue.py` | user | 4 file(s) | 522 | 1 | killed |
| `r261.R2_roster_keeps_discovery` | `src/cratekit/label/tidal_catalogue.py` | user | 4 file(s) | 522 | 3 | killed |
| `u75-a.A1_kind_filter` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u75-a.A3_nothing_accepted_before_the_catalogue` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u75-a.A5_only_the_seams_exception_is_gone` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u75-a.A6_no_identifier_is_not_asked_of_the_provider` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u75-a.A7_each_row_read_alone` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u75-b.B11_write_failure_is_the_verbs_refusal` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u75-b.B1_outage_threshold` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u75-b.B3_only_a_provider_failure_counts` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u75-b.B7_same_recording_listed_once` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u75-b.B9_name_digests_the_provenance` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 2 | killed |
| `u75-zeros.B6_missing_and_nothing_listable_refuses` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `r790-b.L1_guard_counts_held` | `src/cratekit/label/cli.py` | user | 4 file(s) | 332 | 1 | killed |
| `r790-b.L2_round_records_beyond` | `src/cratekit/label/cli.py` | user | 4 file(s) | 332 | 8 | killed |
| `r790-b.L3_set_passes_offer` | `src/cratekit/label/cli.py` | user | 4 file(s) | 332 | 1 | killed |
| `r790-b.L4_bound_is_said` | `src/cratekit/label/cli.py` | user | 4 file(s) | 332 | 1 | killed |
| `r790-c.G1_offer_bounded_by_limit` | `src/cratekit/label/registry.py` | user | 4 file(s) | 332 | 1 | killed |
| `r790-c.G2_entry_overrides` | `src/cratekit/label/registry.py` | user | 4 file(s) | 332 | 4 | killed |
| `r790-c.G3_offer_floor` | `src/cratekit/label/registry.py` | user | 4 file(s) | 332 | 1 | killed |
| `r790-c.G4_offer_read_back` | `src/cratekit/label/registry.py` | user | 4 file(s) | 332 | 5 | killed |
| `r790-c.G5_rename_keeps_offer` | `src/cratekit/label/registry.py` | user | 4 file(s) | 332 | 1 | killed |
| `u166.A11_warning_names_batch` | `src/cratekit/intake/land_cli.py` | user | 7 file(s) | 258 | 3 | killed |
| `u166.A1_parent_check` | `src/cratekit/intake/native.py` | user | 7 file(s) | 258 | 1 | killed |
| `u166.A2_removed_check` | `src/cratekit/intake/native.py` | user | 7 file(s) | 258 | 2 | killed |
| `u166.A3_plain_check` | `src/cratekit/intake/native.py` | user | 7 file(s) | 258 | 1 | killed |
| `u166.A4_no_add` | `src/cratekit/intake/native.py` | user | 7 file(s) | 258 | 23 | killed |
| `u166.A5_present_rows_too` | `src/cratekit/intake/native.py` | user | 7 file(s) | 258 | 1 | killed |
| `u166.A6_always_create` | `src/cratekit/intake/native.py` | user | 7 file(s) | 258 | 2 | killed |
| `u166.A7_record_count` | `src/cratekit/intake/native.py` | user | 7 file(s) | 258 | 5 | killed |
| `u166.A8_digest_key` | `src/cratekit/intake/native.py` | user | 7 file(s) | 258 | 1 | killed |
| `u166.A9_reserved_batch` | `src/cratekit/intake/native.py` | user | 7 file(s) | 258 | 1 | killed |
| `u162.L10_interrupt_cancel` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 95 | 1 | killed |
| `u162.L12_rehearsal_equal` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 95 | 1 | killed |
| `u162.L1_bridge_refusal` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 95 | 1 | killed |
| `u162.L2_area_plan_compare` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 95 | 2 | killed |
| `u162.L4_occupied_hold` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 95 | 1 | killed |
| `u162.L6_gridless_read_back` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 95 | 1 | killed |
| `u162.L7_identified_read_back` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 95 | 1 | killed |
| `u162.L8_success_witness` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 95 | 2 | killed |
| `u162.L9_kept_area_named` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 95 | 4 | killed |
| `u188.M1_stored_pair_dropped` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 95 | 3 | killed |
| `u188.M2_scratch_stored_under_the_mount` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 95 | 3 | killed |
| `u188.M3_live_stored_under_the_mount` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 95 | 3 | killed |
| `u188.M4_staging_pair_dropped` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 95 | 20 | killed |
| `u188.M6_mapped_as_lines` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 95 | 2 | killed |
| `u219.G1_resort_abort` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 309 | 1 | killed |
| `u219.G2_nothing_to_add` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 309 | 1 | killed |
| `u219.G3_adds_frozen` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 309 | 21 | killed |
| `u219.G4_worker_own_tree` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 309 | 1 | killed |
| `u219.G5_resume_run` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 309 | 1 | killed |

## Zero rows and what they owe

- `r799-b.P6_one_file_is_one_group` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

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

### `u181.S3_stop_goes_on`

sync land _vocals: an answer of stop takes the pass on

- File: `src/cratekit/cli/sync_land.py`
- Source: `u181.json`, row `S3_stop_goes_on`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_answering_stop_refuses_with_the_command_that_mends_it`

Old text:

```
    if option != WITHOUT_VOCALS_GO:
```

New text:

```
    if option is None:
```

### `u182.M18_left_open_taken`

_left_behind: name the pass's own jobs on the left open row too

- File: `src/cratekit/cli/sync_land.py`
- Source: `u182.json`, row `M18_left_open_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land.py::test_an_earlier_pass_left_open_beside_a_new_one_is_named_with_its_way_on`
  - `tests/test_sync_land.py::test_the_hearts_the_provider_withholds_are_reported_once_and_not_retried`

Old text:

```
    left = [hold for hold in holds if not taken or _run_of(hold.job) != taken]
```

New text:

```
    left = list(holds)
```

### `u182.M19_left_open_identity`

_left_behind: group by the label alone, so a typed URL and a sweep's id are two playlists

- File: `src/cratekit/cli/sync_land.py`
- Source: `u182.json`, row `M19_left_open_identity`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_url_typed_by_hand_and_a_sweeps_id_are_one_playlist_on_the_left_open_row`

Old text:

```
        grouped.setdefault(hold.identity or hold.label(), []).append(hold)
```

New text:

```
        grouped.setdefault(hold.label(), []).append(hold)
```

### `u182.M20_cancelled_driven`

_intake: drive cancelled jobs with the rest, so a continued pass stops on a cancelled job

- File: `src/cratekit/cli/sync_land.py`
- Source: `u182.json`, row `M20_cancelled_driven`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_continued_pass_never_drives_a_cancelled_job_and_lists_the_rest`
  - `tests/test_sync_land.py::test_a_continued_pass_whose_every_job_was_cancelled_names_a_new_pass_not_a_resume`

Old text:

```
    live = [job for job in found if job.state is not jobs.JobState.CANCELLED]
```

New text:

```
    live = list(found)
```

### `u182.M21_all_cancelled_done`

_intake: go on when every job was cancelled, so the listing refuses a pass with nothing resolved

- File: `src/cratekit/cli/sync_land.py`
- Source: `u182.json`, row `M21_all_cancelled_done`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_continued_pass_whose_every_job_was_cancelled_names_a_new_pass_not_a_resume`

Old text:

```
        if not live:
            report.check(
```

New text:

```
        if False:
            report.check(
```

### `u182.M22_skip_failed`

_missing: list without --skip-failed, so a pass with a cancelled copy stops at the listing

- File: `src/cratekit/cli/sync_land.py`
- Source: `u182.json`, row `M22_skip_failed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_continued_pass_never_drives_a_cancelled_job_and_lists_the_rest`

Old text:

```
        argv.append("--skip-failed")
```

New text:

```
        pass
```

### `u183.M11_land_runs_named`

_unknown_pass: name no land run beside a recent pass

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M11_land_runs_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_refused_id_names_the_land_run_recorded_beside_each_pass`
  - `tests/test_sync_land.py::test_a_run_record_that_is_not_an_object_leaves_the_refusal_whole`

Old text:

```
    lands = _land_runs_of(passes)
```

New text:

```
    lands: dict[str, str] = {}
```

### `u183.M12_preflight_way_back`

_preflight: a rekordbox or backup refusal no longer ends with the command that comes back

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M12_preflight_way_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_continued_pass_refused_while_rekordbox_runs_names_the_way_back`

Old text:

```
        raise tail.with_steps(exc, f"then run it again: {again}") from None
```

New text:

```
        raise
```

### `u183.M14_retryable_intake_continues`

_intake: a retryable ended intake job stops as one that cannot continue, so its way on ends at the resume

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M14_retryable_intake_continues`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_an_intake_job_that_ended_retryable_ends_its_way_on_with_the_continuation`

Old text:

```
                raise _Stop(INTAKE, tail.with_steps(error, retry))
```

New text:

```
                raise _Stop(INTAKE, tail.with_steps(error, retry), continues=False)
```

### `u183.M15_continue_command_words`

_continue_command: drop the flag, so every printed continuation starts a new pass

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M15_continue_command_words`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 9 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_continued_pass_refused_while_rekordbox_runs_names_the_way_back`
  - `tests/test_sync_land.py::test_a_failed_tail_step_plans_no_landing_and_names_the_continuation`
  - `tests/test_sync_land.py::test_a_gate_any_earlier_step_stops_at_is_the_steps_own_not_the_passes`
  - `tests/test_sync_land.py::test_an_earlier_pass_left_open_beside_a_new_one_is_named_with_its_way_on`
  - `tests/test_sync_land.py::test_an_intake_job_that_ended_retryable_ends_its_way_on_with_the_continuation`
  - `tests/test_sync_land.py::test_an_unknown_id_refuses_before_any_step_and_names_the_recent_passes`
  - `tests/test_sync_land.py::test_the_continue_command_a_failed_step_prints_works_when_pasted`
  - `tests/test_sync_land.py::test_the_continue_command_a_pending_stop_prints_works_when_pasted`
  - `tests/test_sync_land.py::test_two_earlier_passes_holding_open_jobs_are_a_choice_named_not_made`

Old text:

```
    return f"crate sync land --pass-run {pass_run}"
```

New text:

```
    return f"crate sync land {pass_run}"
```

### `u183.M1_pass_run_as_given`

_resolve: never take the given id as a pass run, so a pass id is looked up as a land record and refused

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M1_pass_run_as_given`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 16 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_cancelled_download_over_the_same_list_is_not_reused`
  - `tests/test_sync_land.py::test_a_continued_pass_drives_the_download_it_queued_and_queues_no_second`
  - `tests/test_sync_land.py::test_a_continued_pass_is_told_the_answer_that_continues_it`
  - `tests/test_sync_land.py::test_a_continued_pass_never_drives_a_cancelled_job_and_lists_the_rest`
  - `tests/test_sync_land.py::test_a_continued_pass_over_an_open_intake_job_drives_it_first`
  - `tests/test_sync_land.py::test_a_continued_pass_retries_a_download_that_failed_transiently`
  - `tests/test_sync_land.py::test_a_continued_pass_whose_every_job_was_cancelled_names_a_new_pass_not_a_resume`
  - `tests/test_sync_land.py::test_a_job_another_driver_holds_ends_the_pass_with_that_drivers_refusal`
  - `tests/test_sync_land.py::test_a_pass_continued_by_its_land_run_id_reaches_the_same_jobs_as_by_its_pass_id`
  - `tests/test_sync_land.py::test_a_url_typed_by_hand_and_a_sweeps_id_are_one_playlist_on_the_left_open_row`
  - `tests/test_sync_land.py::test_an_intake_job_that_ended_failed_names_its_retry_not_a_continuation`
  - `tests/test_sync_land.py::test_an_intake_job_that_ended_retryable_ends_its_way_on_with_the_continuation`
  - `tests/test_sync_land.py::test_the_continue_command_a_failed_step_prints_works_when_pasted`
  - `tests/test_sync_land.py::test_the_continue_command_a_pending_stop_prints_works_when_pasted`
  - `tests/test_sync_land.py::test_the_left_open_row_names_each_playlist_its_age_size_and_copies`
  - ... and 1 more, see the JSON sidecar

Old text:

```
        if _pass_jobs(store, given, cfg):
            return given
```

New text:

```
        if False:
            return given
```

### `u183.M2_land_record_resolves`

_resolve: ignore the land run's recorded pass, so the land run's own id is refused as it was before U183

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M2_land_record_resolves`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_continued_pass_refused_while_rekordbox_runs_names_the_way_back`
  - `tests/test_sync_land.py::test_a_pass_continued_by_its_land_run_id_reaches_the_same_jobs_as_by_its_pass_id`
  - `tests/test_sync_land.py::test_a_run_interrupted_after_sync_all_continues_by_its_own_id`

Old text:

```
    recorded = land.related_runs.get(PASS_ROLE) if land is not None else None
    if recorded:
```

New text:

```
    recorded = land.related_runs.get(PASS_ROLE) if land is not None else None
    if False:
```

### `u183.M3_recorded_pass_needs_a_job`

_resolve: take a land run's recorded pass with no intake job of this library, so the pass fails at the fourth step again

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M3_recorded_pass_needs_a_job`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_land_run_whose_pass_no_intake_job_carries_is_refused_not_continued`

Old text:

```
            if _pass_jobs(store, recorded, cfg):
                report.check(
```

New text:

```
            if True:
                report.check(
```

### `u183.M6_unreadable_record`

_land_record: let a record that cannot be read raise out of the resolver

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M6_unreadable_record`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_run_record_that_is_not_an_object_leaves_the_refusal_whole`

Old text:

```
    except (CratekitError, AttributeError, KeyError, TypeError, ValueError, OSError):
        return None
    return state if
```

New text:

```
    except KeyError:
        return None
    return state if
```

### `u183.M7_remember_saves`

_remember: record the pass on the run without saving, so a run that stops before the dispatcher saves keeps nothing

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M7_remember_saves`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_run_interrupted_after_sync_all_continues_by_its_own_id`

Old text:

```
    ctx.run.related_runs[PASS_ROLE] = pass_run
    gates.save(ctx.run)
```

New text:

```
    ctx.run.related_runs[PASS_ROLE] = pass_run
```

### `u183.M8_remember_called`

sync_land: never record the pass on the land run

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M8_remember_called`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_continued_pass_refused_while_rekordbox_runs_names_the_way_back`
  - `tests/test_sync_land.py::test_a_pass_continued_by_its_land_run_id_reaches_the_same_jobs_as_by_its_pass_id`
  - `tests/test_sync_land.py::test_a_refused_id_names_the_land_run_recorded_beside_each_pass`
  - `tests/test_sync_land.py::test_a_run_interrupted_after_sync_all_continues_by_its_own_id`
  - `tests/test_sync_land.py::test_a_run_record_that_is_not_an_object_leaves_the_refusal_whole`

Old text:

```
        if run_id:
            _remember(ctx, report, run_id)
```

New text:

```
        if False:
            _remember(ctx, report, run_id)
```

### `r799-c.V1_the_gate_is_asked_before_the_write`

verb: apply the plan whatever the gate answers

- File: `src/cratekit/tagging/remap_cli.py`
- Source: `r799-c.json`, row `V1_the_gate_is_asked_before_the_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 15 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_file_changed_after_the_answer_makes_the_decision_stale`
  - `tests/test_tag_remap.py::test_a_file_outside_the_library_is_said_and_not_listed`
  - `tests/test_tag_remap.py::test_a_person_reads_the_counts_and_the_pairs_at_the_gate`
  - `tests/test_tag_remap.py::test_a_record_that_could_not_be_parsed_is_said`
  - `tests/test_tag_remap.py::test_a_refusal_that_rewrote_nothing_does_not_send_a_person_to_the_row_verb`
  - `tests/test_tag_remap.py::test_a_run_that_leaves_a_file_says_how_many_and_why_on_every_path`
  - `tests/test_tag_remap.py::test_a_run_that_wrote_still_says_what_it_left`
  - `tests/test_tag_remap.py::test_a_write_that_does_not_take_refuses_after_the_rest_were_written`
  - `tests/test_tag_remap.py::test_an_abort_writes_nothing`
  - `tests/test_tag_remap.py::test_an_active_taxonomy_with_no_table_says_so_and_plans_nothing`
  - `tests/test_tag_remap.py::test_an_approved_plan_is_written_and_the_run_names_the_verb_the_rows_follow_by`
  - `tests/test_tag_remap.py::test_an_empty_plan_still_asks_and_then_writes_nothing`
  - `tests/test_tag_remap.py::test_the_gate_takes_no_inline_answer`
  - `tests/test_tag_remap.py::test_the_shipped_template_declares_the_table_so_the_warning_is_not_given`
  - `tests/test_tag_remap.py::test_the_verb_asks_before_it_writes_and_the_gate_shows_the_plan`

Old text:

```
    if ctx.gate.require(spec, plan=data, context=_facts(plan)) != "apply":
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=_advisories(plan))
```

New text:

```
(empty)
```

### `r799-c.V2_a_file_that_did_not_take_refuses`

verb: answer a clean run over a file that did not take its genre

- File: `src/cratekit/tagging/remap_cli.py`
- Source: `r799-c.json`, row `V2_a_file_that_did_not_take_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 7 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_refusal_that_rewrote_nothing_does_not_send_a_person_to_the_row_verb`
  - `tests/test_tag_remap.py::test_a_write_that_does_not_take_refuses_after_the_rest_were_written`
  - `tests/test_tag_remap.py::test_each_way_a_file_did_not_take_its_genre_refuses_and_says_which[failed-could not be written and are untouched]`
  - `tests/test_tag_remap.py::test_each_way_a_file_did_not_take_its_genre_refuses_and_says_which[moved-carried something else]`
  - `tests/test_tag_remap.py::test_each_way_a_file_did_not_take_its_genre_refuses_and_says_which[unrecorded-no record of the rewrite could be committed]`
  - `tests/test_tag_remap.py::test_each_way_a_file_did_not_take_its_genre_refuses_and_says_which[wrong-do not read back]`
  - `tests/test_tag_remap.py::test_the_refusal_names_a_few_files_and_carries_them_all`

Old text:

```
    if written.clean:
        return
    parts = []
```

New text:

```
    if True:
        return
    parts = []
```

### `r799-b.P1_a_file_is_planned_only_while_it_carries_what_a_record_wrote`

plan: take every record in force as explaining the file, whatever the file carries

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-b.json`, row `P1_a_file_is_planned_only_while_it_carries_what_a_record_wrote`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 15 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_blank_file_whose_word_is_now_declined_is_not_read_as_agreeing`
  - `tests/test_tag_remap.py::test_a_file_holding_a_second_genre_is_left_alone_and_both_are_shown`
  - `tests/test_tag_remap.py::test_a_file_whose_genre_was_cleared_is_left_alone_and_not_read_as_agreeing`
  - `tests/test_tag_remap.py::test_a_genre_a_record_shop_wrote_later_on_a_path_the_catalogue_once_wrote_agrees`
  - `tests/test_tag_remap.py::test_a_genre_frame_holding_two_values_is_two_values_on_an_id3_container`
  - `tests/test_tag_remap.py::test_a_genre_nobody_recorded_writing_is_left_alone_and_listed[Deep House]`
  - `tests/test_tag_remap.py::test_a_genre_nobody_recorded_writing_is_left_alone_and_listed[Pop]`
  - `tests/test_tag_remap.py::test_a_genre_nobody_recorded_writing_is_left_alone_and_listed[dance / pop]`
  - `tests/test_tag_remap.py::test_a_genre_put_back_by_hand_after_a_rewrite_is_left_alone`
  - `tests/test_tag_remap.py::test_a_record_shops_genre_is_never_resolved_as_the_catalogues_word`
  - `tests/test_tag_remap.py::test_a_run_that_leaves_a_file_says_how_many_and_why_on_every_path`
  - `tests/test_tag_remap.py::test_a_run_that_wrote_still_says_what_it_left`
  - `tests/test_tag_remap.py::test_every_file_is_counted_once_and_the_items_are_in_path_order`
  - `tests/test_tag_remap.py::test_only_a_planned_write_is_written`
  - `tests/test_tag_remap.py::test_the_apply_writes_the_planned_genre_and_no_other_file`

Old text:

```
    explaining = [record for record in in_force if values == (record.written,)]
```

New text:

```
    explaining = list(in_force)
```

### `r799-b.P2_two_explanations_are_ambiguous`

plan: settle a genre two records explain differently by the first of them

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-b.json`, row `P2_two_explanations_are_ambiguous`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_file_reached_through_a_link_is_the_file`
  - `tests/test_tag_remap.py::test_a_genre_two_records_explain_with_different_sources_is_left`
  - `tests/test_tag_remap.py::test_a_genre_two_records_explain_with_different_words_is_left`
  - `tests/test_tag_remap.py::test_one_file_recorded_under_two_spellings_is_one_file`

Old text:

```
    if len({(record.source, record.word) for record in explaining}) > 1:
```

New text:

```
    if False:
```

### `r799-b.P3_a_shops_genre_is_the_shops`

plan: resolve a record shop's word as the general catalogue's

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-b.json`, row `P3_a_shops_genre_is_the_shops`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_record_shops_genre_is_never_resolved_as_the_catalogues_word`

Old text:

```
    if wrote.source != SOURCE:
```

New text:

```
    if False:
```

### `r799-b.P4_a_rewrite_retires_the_record_it_replaced`

plan: keep every record of the source in force, whatever its generation

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-b.json`, row `P4_a_rewrite_retires_the_record_it_replaced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_genre_put_back_by_hand_after_a_rewrite_is_left_alone`
  - `tests/test_tag_remap.py::test_a_word_given_its_first_genre_back_is_still_followed`

Old text:

```
        if record.source == SOURCE and record.generation == newest
    ]
```

New text:

```
        if record.source == SOURCE
    ]
```

### `r799-b.P5_only_a_file_under_the_library_is_opened`

plan: settle a recorded path wherever it is

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-b.json`, row `P5_only_a_file_under_the_library_is_opened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_file_outside_the_library_is_said_and_not_listed`
  - `tests/test_tag_remap.py::test_a_file_outside_this_librarys_root_is_counted_and_never_opened`
  - `tests/test_tag_remap.py::test_a_folder_named_in_another_case_on_a_volume_that_folds_case_is_inside`
  - `tests/test_tag_remap.py::test_a_path_that_climbs_out_of_the_library_is_outside_it`

Old text:

```
        if resolved is None or not _inside(resolved, library):
```

New text:

```
        if resolved is None:
```

### `r799-b.P6_one_file_is_one_group`

plan: key a file under the library by its resolved name and not by the file itself

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-b.json`, row `P6_one_file_is_one_group`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    try:
        stat = resolved.stat()
    except OSError:
        return ("name", str(resolved))
    return ("file", stat.st_dev, stat.st_ino)
```

New text:

```
    return ("name", str(resolved))
```

### `r799-b.W1_a_file_is_read_again_before_it_is_written`

apply: write over whatever the file carries by now

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-b.json`, row `W1_a_file_is_read_again_before_it_is_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_file_that_moved_since_the_plan_is_named_and_not_written`

Old text:

```
        if _file_genres(target) != (item.current,):
            moved.append(item.path)
            continue
```

New text:

```
(empty)
```

### `r799-b.W2_the_writers_answer_is_kept`

apply: count a file the writer could not write as written

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-b.json`, row `W2_the_writers_answer_is_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_file_the_writer_could_not_write_is_named_as_untouched_and_the_rest_are_written`
  - `tests/test_tag_remap.py::test_a_refusal_that_rewrote_nothing_does_not_send_a_person_to_the_row_verb`
  - `tests/test_tag_remap.py::test_a_write_that_does_not_take_refuses_after_the_rest_were_written`

Old text:

```
        if not tags.write_genre(target, item.wanted):
            failed.append(item.path)
            continue
```

New text:

```
        tags.write_genre(target, item.wanted)
```

### `r799-b.W3_a_write_is_read_back`

apply: take the writer's word that the genre is on the file

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-b.json`, row `W3_a_write_is_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_file_written_that_does_not_read_back_is_named_as_wrong`

Old text:

```
        if _file_genres(target) != (item.wanted,):
            wrong.append(item.path)
            continue
```

New text:

```
(empty)
```

### `r799-c.P11_blank_is_not_agreement`

plan: read a blank file whose word is given nothing as agreeing

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-c.json`, row `P11_blank_is_not_agreement`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_blank_file_whose_word_is_now_declined_is_not_read_as_agreeing`

Old text:

```
        if any(current and current == _wanted(declared, record.word) for record in mine):
```

New text:

```
        if any(current == _wanted(declared, record.word) for record in mine):
```

### `r799-c.V3_an_unrecorded_rewrite_is_not_clean`

verb: call a run clean whose rewrite could not be recorded

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-c.json`, row `V3_an_unrecorded_rewrite_is_not_clean`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_record_that_cannot_be_committed_is_named_and_the_file_stays_rewritten`
  - `tests/test_tag_remap.py::test_each_way_a_file_did_not_take_its_genre_refuses_and_says_which[unrecorded-no record of the rewrite could be committed]`

Old text:

```
        return not (self.wrong or self.moved or self.failed or self.unrecorded)
```

New text:

```
        return not (self.wrong or self.moved or self.failed)
```

### `r799-c.W4_a_rewrite_is_recorded`

apply: commit no record of a rewrite, so the verb's own write reads as a hand edit

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-c.json`, row `W4_a_rewrite_is_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 5 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_file_this_verb_rewrote_is_corrected_again_when_the_word_moves_again`
  - `tests/test_tag_remap.py::test_a_genre_put_back_by_hand_after_a_rewrite_is_left_alone`
  - `tests/test_tag_remap.py::test_a_record_that_cannot_be_committed_is_named_and_the_file_stays_rewritten`
  - `tests/test_tag_remap.py::test_a_rewrite_is_recorded_as_a_tagging_record_of_its_own`
  - `tests/test_tag_remap.py::test_a_word_given_its_first_genre_back_is_still_followed`

Old text:

```
        if not _record(cfg, name, ordinal, item):
            unrecorded.append(item.path)
```

New text:

```
(empty)
```

### `r799-c.W5_a_rewrites_record_is_one_generation_on`

apply: record a rewrite at the generation of the record it replaced

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-c.json`, row `W5_a_rewrites_record_is_one_generation_on`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_file_this_verb_rewrote_is_corrected_again_when_the_word_moves_again`
  - `tests/test_tag_remap.py::test_a_genre_put_back_by_hand_after_a_rewrite_is_left_alone`
  - `tests/test_tag_remap.py::test_a_rewrite_is_recorded_as_a_tagging_record_of_its_own`
  - `tests/test_tag_remap.py::test_a_word_given_its_first_genre_back_is_still_followed`

Old text:

```
                "generation": item.generation + 1,
```

New text:

```
                "generation": item.generation,
```

### `u119-b.G5r_favorites_counted_as_members`

plan_refresh: the folder's own Favorites counts among the folder's members

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119-b.json`, row `G5r_favorites_counted_as_members`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 45 against a baseline of 45
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_favourite_sitting_only_in_favorites_after_leaving_its_band_is_removed`

Old text:

```
            if favorites_node is not None and node.playlist_id == favorites_node.playlist_id:
                continue
            members.update(node.content_ids)
```

New text:

```
            members.update(node.content_ids)
```

### `u119-c.C2_torn_bucket_bound_anyway`

plan_refresh: a bucket whose record names two live folders is bound to the first

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119-c.json`, row `C2_torn_bucket_bound_anyway`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 45 against a baseline of 45
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_bucket_is_bound_by_its_band_entries_before_its_favorites_entry`

Old text:

```
        if bucket.id in recorded_folder and bucket.id not in torn
    }
```

New text:

```
        if bucket.id in recorded_folder
    }
```

### `u119-c.C5_interruption_unreported`

apply_refresh: a failure after the additions landed is raised bare, the additions unreported

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119-c.json`, row `C5_interruption_unreported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 45 against a baseline of 45
- Kills: 3 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_removal_that_fails_after_the_additions_landed_says_what_landed`
  - `tests/test_genre_favorites.py::test_the_additive_half_carries_the_additions_when_interrupted_past_them`
  - `tests/test_genre_favorites.py::test_the_verb_reports_an_interrupted_refresh_with_the_additions_that_committed`

Old text:

```
        except Exception as exc:
            raise RefreshInterrupted(landed) from exc
```

New text:

```
        except Exception:
            raise
```

### `u119.G10_placements_no_gap`

placements: a source that cannot be read names no dimension as not compared

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G10_placements_no_gap`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 45 against a baseline of 45
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_check_with_no_source_leaves_the_recorded_favorites_out_and_names_the_gap`
  - `tests/test_genre_favorites.py::test_the_favourites_become_declared_placements_and_a_missing_source_a_gap`

Old text:

```
        return (), (FAVORITES_DIMENSION,)
```

New text:

```
        return (), ()
```

### `u119.G11_stale_digest`

apply_refresh: a plan whose digest moved since the approval is written anyway

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G11_stale_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 45 against a baseline of 45
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_plan_that_moved_between_the_approval_and_the_write_is_refused`
  - `tests/test_genre_favorites.py::test_the_digest_moves_when_a_track_is_dragged_into_favorites_between_the_acts`

Old text:

```
    if again.digest != plan.digest:
        raise refuse(
            "decision-stale",
            "the genre Favorites are not as the approved plan read them
```

New text:

```
    if False:
        raise refuse(
            "decision-stale",
            "the genre Favorites are not as the approved plan read them
```

### `u119.G13_removals_when_not_asked`

apply_refresh: the removals are made whether or not the caller was approved for them

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G13_removals_when_not_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 45 against a baseline of 45
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_the_additive_half_adds_and_counts_what_it_leaves_owed`
  - `tests/test_genre_favorites.py::test_the_digest_covers_the_target_and_stands_still_across_a_partial_apply`

Old text:

```
        if remove and owed:
```

New text:

```
        if owed:
```

### `u119.G15_removal_commit_admits_nothing`

apply_refresh: the second commit does not admit the membership table

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G15_removal_commit_admits_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 45 against a baseline of 45
- Kills: 5 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_favourite_sitting_only_in_favorites_after_leaving_its_band_is_removed`
  - `tests/test_genre_favorites.py::test_a_hand_added_track_not_in_all_favorites_is_removed_at_the_refresh`
  - `tests/test_genre_favorites.py::test_a_track_that_leaves_all_favorites_leaves_its_genre_favorites_and_keeps_its_band`
  - `tests/test_genre_favorites.py::test_no_content_row_tempo_or_rating_is_written`
  - `tests/test_genre_favorites.py::test_the_verb_asks_its_explicit_gate_then_adds_and_removes_and_reads_back`

Old text:

```
                    rb_writer.commit_guarded(db, removals=(rb_writer.MEMBERSHIP_TABLE,))
```

New text:

```
                    rb_writer.commit_guarded(db)
```

### `u119.G1_class_undeclared`

require_class: a taxonomy with no playlist class is not refused

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G1_class_undeclared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 45 against a baseline of 45
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_taxonomy_declaring_no_playlist_class_refuses_by_name`
  - `tests/test_genre_favorites.py::test_the_verb_refuses_an_undeclared_class_by_name`

Old text:

```
    found = favorites_class(declared)
    if found is None:
        raise refuse(
            CLASS_UNDECLARED,
```

New text:

```
    found = favorites_class(declared)
    if False:
        raise refuse(
            CLASS_UNDECLARED,
```

### `u119.G2_source_folder_counts`

source_playlist: a source playlist holding no live track is mirrored, emptying every Favorites

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G2_source_folder_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 45 against a baseline of 45
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_smart_playlist_or_an_emptied_playlist_of_the_source_name_is_not_the_source`

Old text:

```
        if not _live_members(db, str(live[0].ID)):
```

New text:

```
        if False:
```

### `u119.G3_two_sources_first_wins`

source_playlist: two live sources, the first is taken

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G3_two_sources_first_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 45 against a baseline of 45
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_two_source_playlists_are_refused_rather_than_one_chosen`

Old text:

```
    if len(live) == 1:
        if not _live_members(db, str(live[0].ID)):
```

New text:

```
    if len(live) >= 1:
        if not _live_members(db, str(live[0].ID)):
```

### `u119.G4_removed_membership_live`

_live_members: a membership rekordbox removed still counts as held

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G4_removed_membership_live`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 45 against a baseline of 45
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_track_that_leaves_all_favorites_leaves_its_genre_favorites_and_keeps_its_band`

Old text:

```
        if not rb_writer.membership_removed(song)
    )
```

New text:

```
    )
```

### `u119.G6_wanted_is_members`

plan_refresh: every member of the folder is wanted, favourite or not

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G6_wanted_is_members`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 45 against a baseline of 45
- Kills: 13 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_hand_added_track_not_in_all_favorites_is_removed_at_the_refresh`
  - `tests/test_genre_favorites.py::test_a_plan_that_moved_between_the_approval_and_the_write_is_refused`
  - `tests/test_genre_favorites.py::test_a_removal_that_fails_after_the_additions_landed_says_what_landed`
  - `tests/test_genre_favorites.py::test_a_source_that_went_between_the_two_acts_is_refused_by_the_gate`
  - `tests/test_genre_favorites.py::test_a_track_that_leaves_all_favorites_leaves_its_genre_favorites_and_keeps_its_band`
  - `tests/test_genre_favorites.py::test_a_vocal_favourite_is_in_its_band_with_vox_and_favorites_under_one_genre`
  - `tests/test_genre_favorites.py::test_the_additive_half_adds_and_counts_what_it_leaves_owed`
  - `tests/test_genre_favorites.py::test_the_check_reports_a_favourite_missing_from_its_favorites_and_not_a_hand_added_one_as_foreign`
  - `tests/test_genre_favorites.py::test_the_digest_covers_the_target_and_stands_still_across_a_partial_apply`
  - `tests/test_genre_favorites.py::test_the_digest_moves_when_a_track_is_dragged_into_favorites_between_the_acts`
  - `tests/test_genre_favorites.py::test_the_favourites_become_declared_placements_and_a_missing_source_a_gap`
  - `tests/test_genre_favorites.py::test_the_verb_asks_its_explicit_gate_then_adds_and_removes_and_reads_back`
  - `tests/test_genre_favorites.py::test_the_verb_reports_an_interrupted_refresh_with_the_additions_that_committed`

Old text:

```
                wanted=tuple(sorted(members & favourites)),
```

New text:

```
                wanted=tuple(sorted(members)),
```

### `u119.G7_twin_folders_first_taken`

plan_refresh: two folders of one bucket's name, the first is taken

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G7_twin_folders_first_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 45 against a baseline of 45
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_folder_nobody_declares_and_a_name_two_folders_carry_are_left_alone`

Old text:

```
        if len(named) > 1:
            unclaimed.extend(
```

New text:

```
        if len(named) > 9:
            unclaimed.extend(
```

### `u119.G9_digest_over_adds`

identity: the digest covers the adds rather than the target

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G9_digest_over_adds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 45 against a baseline of 45
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_the_digest_covers_the_target_and_stands_still_across_a_partial_apply`

Old text:

```
            "wanted": list(self.wanted),
            "removes": list(self.removes),
```

New text:

```
            "wanted": list(self.adds),
            "removes": list(self.removes),
```

### `u185.R4_genre_source`

source_playlist: count a playlist of the source's name inside the folder

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u185.json`, row `R4_genre_source`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 45 against a baseline of 45
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_source_namesake_inside_deadca7s_folder_is_not_a_second_source`

Old text:

```
    live = foreign_tree.outside(live, list(db.get_playlist()))
```

New text:

```
    live = list(live)
```

### `u119.V1_ack_after_plan`

favorites_refresh: the backup acknowledgment is not read before the gate

- File: `src/cratekit/favorites/refresh_cli.py`
- Source: `u119.json`, row `V1_ack_after_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 45 against a baseline of 45
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    session.assert_backup_acknowledged(cfg)

    plan = planned(cfg, declared, registry)
```

New text:

```
    plan = planned(cfg, declared, registry)
```

### `r261.W1_worker_refuses`

The worker returns success over a sweep that left something unread

- File: `src/cratekit/label/cli.py`
- Source: `r261.json`, row `W1_worker_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/modules/test_labels.py`
- Collected: 522 against a baseline of 522
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_during_discovery_fails_the_sweep_and_names_the_artist`
  - `tests/test_label_tidal_catalogue.py::test_a_roster_member_missing_one_listing_fails_the_sweep_and_names_it`

Old text:

```
    if source.unread:
        _refuse_unread(
```

New text:

```
    if False:
        _refuse_unread(
```

### `r261.W2_remedy`

The refusal tells the person to resume even when only a missing method is unread

- File: `src/cratekit/label/cli.py`
- Source: `r261.json`, row `W2_remedy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/modules/test_labels.py`
- Collected: 522 against a baseline of 522
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_roster_member_missing_one_listing_fails_the_sweep_and_names_it`

Old text:

```
        remedy=Remedy.RESUME_JOB if transient else Remedy.REPORT_DEFECT,
```

New text:

```
        remedy=Remedy.RESUME_JOB,
```

### `r261.W3_retryable`

The refusal is retryable whatever was unread

- File: `src/cratekit/label/cli.py`
- Source: `r261.json`, row `W3_retryable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/modules/test_labels.py`
- Collected: 522 against a baseline of 522
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_roster_member_missing_one_listing_fails_the_sweep_and_names_it`

Old text:

```
        retryable=transient,
```

New text:

```
        retryable=True,
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

### `u75-a.A1_kind_filter`

Drop the kind filter, so an accepted harvested label name, which shares the queue, is read as a release

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-a.json`, row `A1_kind_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_an_accepted_harvested_label_shares_the_queue_and_is_not_a_release`

Old text:

```
        kinds=(sweep.KIND,),

```

New text:

```
(empty)
```

### `u75-a.A3_nothing_accepted_before_the_catalogue`

Remove the early return, so a queue with nothing accepted resolves the catalogue and spends a login

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-a.json`, row `A3_nothing_accepted_before_the_catalogue`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_nothing_accepted_is_a_no_op_that_never_opens_the_catalogue`

Old text:

```
    if not accepted:
        # ASKED BEFORE THE CATALOGUE IS RESOLVED
```

New text:

```
    if False:
        # ASKED BEFORE THE CATALOGUE IS RESOLVED
```

### `u75-a.A5_only_the_seams_exception_is_gone`

Catch LookupError again instead of the seam's own class, the review's first finding

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-a.json`, row `A5_only_the_seams_exception_is_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_lookup_error_that_is_not_the_seams_own_is_never_read_as_a_gone_release`

Old text:

```
    except catalogue.ReleaseUnresolvable as exc:
        return _Failed(release, GONE, str(exc))
```

New text:

```
    except LookupError as exc:
        return _Failed(release, GONE, str(exc))
```

### `u75-a.A6_no_identifier_is_not_asked_of_the_provider`

Remove the empty identifier guard, so the provider is asked for a release with no name

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-a.json`, row `A6_no_identifier_is_not_asked_of_the_provider`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_an_accepted_item_naming_no_release_is_a_named_failure`

Old text:

```
    if not release.release_id:
        return _Failed(release, NO_IDENTIFIER, "the review item names no release identifier")

```

New text:

```
(empty)
```

### `u75-a.A7_each_row_read_alone`

Let one unreadable row escape, which costs the run instead of one line

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-a.json`, row `A7_each_row_read_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_one_unreadable_row_is_reported_and_the_rest_of_the_release_still_lists`

Old text:

```
        except match.UnreadableList as exc:
            unreadable.append(str(exc))
```

New text:

```
        except ZeroDivisionError as exc:
            unreadable.append(str(exc))
```

### `u75-b.B11_write_failure_is_the_verbs_refusal`

Remove the OSError conversion, so a full disk reaches a person as an internal error

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-b.json`, row `B11_write_failure_is_the_verbs_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_write_the_disk_refuses_is_the_verbs_refusal_and_not_an_internal_error`

Old text:

```
        except OSError as exc:
            # A FOLDER THAT CANNOT BE WRITTEN IS THIS VERB'S REFUSAL.
```

New text:

```
        except ZeroDivisionError as exc:
            # A FOLDER THAT CANNOT BE WRITTEN IS THIS VERB'S REFUSAL.
```

### `u75-b.B1_outage_threshold`

Raise the outage threshold from three to thirty, a realistic slip, so a dead provider is asked about every release

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-b.json`, row `B1_outage_threshold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_provider_that_stopped_answering_is_not_asked_about_every_release`

Old text:

```
OUTAGE_AFTER = 3
```

New text:

```
OUTAGE_AFTER = 30
```

### `u75-b.B3_only_a_provider_failure_counts`

Count a gone release towards an outage

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-b.json`, row `B3_only_a_provider_failure_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_gone_release_does_not_count_towards_an_outage`

Old text:

```
            in_a_row = in_a_row + 1 if outcome.kind == PROVIDER else 0
```

New text:

```
            in_a_row = in_a_row + 1
```

### `u75-b.B7_same_recording_listed_once`

Remove the match id dedupe, so a single and its album list one recording twice

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-b.json`, row `B7_same_recording_listed_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_the_same_recording_on_two_releases_is_listed_once_under_the_first`

Old text:

```
            elif settled.match_id in seen:
                counts["duplicate"] += 1

```

New text:

```
(empty)
```

### `u75-b.B9_name_digests_the_provenance`

Digest the tracks alone, the review's fourth finding, so a corrected year meets the emitter's refusal

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-b.json`, row `B9_name_digests_the_provenance`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_approved.py::test_the_list_name_moves_with_anything_the_emitter_would_write`
  - `tests/test_label_approved.py::test_the_same_tracks_with_a_corrected_year_take_a_new_name_and_are_not_refused`

Old text:

```
        "provenance": [
            dataclasses.asdict(provenance[track["id"]]) for track in body["tracks"]
        ],
```

New text:

```
        "provenance": [],
```

### `u75-zeros.B6_missing_and_nothing_listable_refuses`

Remove the refusal for missing tracks none of which carries a provider identifier

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-zeros.json`, row `B6_missing_and_nothing_listable_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_missing_tracks_none_of_which_can_be_asked_for_is_refused_and_not_a_no_op`

Old text:

```
    if missing and not listed:
```

New text:

```
    if False:
```

### `r790-b.L1_guard_counts_held`

_refuse_unfinished: leave held releases out of the confirmed-none count, so a dead verifier reads as nothing new

- File: `src/cratekit/label/cli.py`
- Source: `r790-b.json`, row `L1_guard_counts_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_label_registry_verbs.py`
- Collected: 332 against a baseline of 332
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_dead_verifier_on_a_later_sweep_refuses_rather_than_reporting_nothing_new`

Old text:

```
    unconfirmed = len(source.dropped) + source.held_unconfirmed
```

New text:

```
    unconfirmed = len(source.dropped)
```

### `r790-b.L2_round_records_beyond`

handle: record every round as nothing beyond

- File: `src/cratekit/label/cli.py`
- Source: `r790-b.json`, row `L2_round_records_beyond`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_label_registry_verbs.py`
- Collected: 332 against a baseline of 332
- Kills: 8 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_first_sweep_files_the_default_ten_and_counts_the_other_forty`
  - `tests/test_label_offer_window.py::test_a_label_whose_offer_is_raised_to_thirty_files_thirty`
  - `tests/test_label_offer_window.py::test_a_label_whose_window_is_already_held_records_its_beyond_with_nothing_filed`
  - `tests/test_label_offer_window.py::test_a_round_records_the_most_the_label_could_still_offer`
  - `tests/test_label_offer_window.py::test_a_run_over_two_labels_counts_what_both_left_beyond`
  - `tests/test_label_offer_window.py::test_a_second_sweep_files_only_the_new_release_and_refiles_nothing`
  - `tests/test_label_offer_window.py::test_a_track_limit_below_the_offer_bounds_it_and_the_rest_is_still_counted`
  - `tests/test_label_offer_window.py::test_the_configured_offer_is_the_default_for_every_label`

Old text:

```
                beyond=listing.beyond,
```

New text:

```
                beyond=0,
```

### `r790-b.L3_set_passes_offer`

registry_cmd set: drop --offer on the way to the store, so set reports an edit it never wrote

- File: `src/cratekit/label/cli.py`
- Source: `r790-b.json`, row `L3_set_passes_offer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_label_registry_verbs.py`
- Collected: 332 against a baseline of 332
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_raising_a_label_offer_after_a_sweep_files_the_difference`

Old text:

```
            seed_artists=seeds,
            track_limit=track_limit,
            offer=offer,
```

New text:

```
            seed_artists=seeds,
            track_limit=track_limit,
```

### `r790-b.L4_bound_is_said`

_detail: stop saying the track limit bounds an offer

- File: `src/cratekit/label/cli.py`
- Source: `r790-b.json`, row `L4_bound_is_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_label_registry_verbs.py`
- Collected: 332 against a baseline of 332
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_the_registry_says_when_the_track_limit_bounds_an_offer`

Old text:

```
            + (f", bounded by the track limit to {bound}" if entry.offer > bound else "")
```

New text:

```
            + ""
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

### `u166.A11_warning_names_batch`

awaiting_analysis: name the batch playlist again instead of Analyze

- File: `src/cratekit/intake/land_cli.py`
- Source: `u166.json`, row `A11_warning_names_batch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 258 against a baseline of 258
- Kills: 3 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_landing_of_five_adds_five_memberships_to_analyze_under_the_root`
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_writers_native.py::test_one_file_becomes_one_row_and_one_playlist_under_the_adopted_root`

Old text:

```
                f"{collection.analyze_name} playlist, which holds every row waiting "
```

New text:

```
                f"{collection.playlist} playlist, which holds every row waiting "
```

### `u166.A1_parent_check`

analyze_playlist: take a live Analyze anywhere, not only directly under the root

- File: `src/cratekit/intake/native.py`
- Source: `u166.json`, row `A1_parent_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 258 against a baseline of 258
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_an_analyze_playlist_outside_the_root_is_never_written_into`

Old text:

```
        if str(getattr(row, "ParentID", "") or "") != str(root_id):
            continue
        if rb_writer.node_removed(row)
```

New text:

```
        if False:
            continue
        if rb_writer.node_removed(row)
```

### `u166.A2_removed_check`

analyze_playlist: take a removed Analyze as the queue

- File: `src/cratekit/intake/native.py`
- Source: `u166.json`, row `A2_removed_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 258 against a baseline of 258
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_removed_or_smart_node_named_analyze_is_never_written_into`
  - `tests/test_inbox_analyzed.py::test_analyze_removed_after_the_approval_is_refused_and_nothing_lands`

Old text:

```
        if rb_writer.node_removed(row) or int(getattr(row, "Attribute", -1)) != 0:
```

New text:

```
        if int(getattr(row, "Attribute", -1)) != 0:
```

### `u166.A3_plain_check`

analyze_playlist: take a folder or smart playlist named Analyze as the queue

- File: `src/cratekit/intake/native.py`
- Source: `u166.json`, row `A3_plain_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 258 against a baseline of 258
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_removed_or_smart_node_named_analyze_is_never_written_into`

Old text:

```
        if rb_writer.node_removed(row) or int(getattr(row, "Attribute", -1)) != 0:
```

New text:

```
        if rb_writer.node_removed(row):
```

### `u166.A4_no_add`

apply_rows: add nothing to Analyze

- File: `src/cratekit/intake/native.py`
- Source: `u166.json`, row `A4_no_add`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 258 against a baseline of 258
- Kills: 23 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_landing_of_five_adds_five_memberships_to_analyze_under_the_root`
  - `tests/test_inbox_analyzed.py::test_a_membership_whose_collection_row_is_missing_stays_and_is_named`
  - `tests/test_inbox_analyzed.py::test_a_removal_that_did_not_take_is_refused_after_the_commit`
  - `tests/test_inbox_analyzed.py::test_a_removed_or_smart_node_named_analyze_is_never_written_into`
  - `tests/test_inbox_analyzed.py::test_a_row_marked_analysed_with_no_analysis_path_stays`
  - `tests/test_inbox_analyzed.py::test_a_row_removed_from_the_collection_stays_and_is_named`
  - `tests/test_inbox_analyzed.py::test_a_row_the_collection_already_held_is_not_added_to_analyze`
  - `tests/test_inbox_analyzed.py::test_a_row_with_an_analysis_path_and_analysed_unset_stays`
  - `tests/test_inbox_analyzed.py::test_a_second_clear_plans_nothing`
  - `tests/test_inbox_analyzed.py::test_a_second_landing_adds_its_own_beside_them_and_the_playlist_is_never_made_twice`
  - `tests/test_inbox_analyzed.py::test_a_track_held_twice_is_one_row_cleared_and_counted_once`
  - `tests/test_inbox_analyzed.py::test_after_an_analysis_of_three_the_clear_removes_exactly_three_and_no_track`
  - `tests/test_inbox_analyzed.py::test_an_analysis_finished_after_the_approval_is_refused_by_the_engine`
  - `tests/test_inbox_analyzed.py::test_an_analyze_playlist_outside_the_root_is_never_written_into`
  - `tests/test_inbox_analyzed.py::test_analyze_removed_after_the_approval_is_refused_and_nothing_lands`
  - ... and 8 more, see the JSON sidecar

Old text:

```
            if added_ids:
                analyze = _analyze_row(db, plan, anchor)
```

New text:

```
            if False:
                analyze = _analyze_row(db, plan, anchor)
```

### `u166.A5_present_rows_too`

apply_rows: add every row the plan names, present ones too

- File: `src/cratekit/intake/native.py`
- Source: `u166.json`, row `A5_present_rows_too`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 258 against a baseline of 258
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_row_the_collection_already_held_is_not_added_to_analyze`

Old text:

```
                        db, analyze, [content_id for _row, content_id in added_ids]
```

New text:

```
                        db, analyze, list(by_target.values())
```

### `u166.A6_always_create`

_analyze_row: make a new Analyze every landing

- File: `src/cratekit/intake/native.py`
- Source: `u166.json`, row `A6_always_create`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 258 against a baseline of 258
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_row_the_collection_already_held_is_not_added_to_analyze`
  - `tests/test_inbox_analyzed.py::test_a_second_landing_adds_its_own_beside_them_and_the_playlist_is_never_made_twice`

Old text:

```
    return found if found is not None else db.create_playlist(ANALYZE, parent=anchor)
```

New text:

```
    return db.create_playlist(ANALYZE, parent=anchor)
```

### `u166.A7_record_count`

apply_rows: record the batch's memberships only on success

- File: `src/cratekit/intake/native.py`
- Source: `u166.json`, row `A7_record_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 258 against a baseline of 258
- Kills: 5 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_landing_of_five_adds_five_memberships_to_analyze_under_the_root`
  - `tests/test_intake_land_hearts_native.py::test_the_record_carries_the_hearts_placed_under_their_own_key`
  - `tests/test_intake_land_native.py::test_three_files_become_three_rows_and_one_playlist_under_the_adopted_root`
  - `tests/test_intake_writers_native.py::test_one_file_becomes_one_row_and_one_playlist_under_the_adopted_root`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order`

Old text:

```
        _record_landing_commit(
            record,
            plan,
            len(added_ids),
            memberships + analyze_added,
```

New text:

```
        _record_landing_commit(
            record,
            plan,
            len(added_ids),
            memberships,
```

### `u166.A8_digest_key`

identity: leave the found Analyze out of the digest

- File: `src/cratekit/intake/native.py`
- Source: `u166.json`, row `A8_digest_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 258 against a baseline of 258
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_analyze_removed_after_the_approval_is_refused_and_nothing_lands`

Old text:

```
    analyze = {"analyze": plan.analyze_playlist_id} if plan.to_add() else {}
```

New text:

```
    analyze = {}
```

### `u166.A9_reserved_batch`

plan_rows: let a batch take the name Analyze

- File: `src/cratekit/intake/native.py`
- Source: `u166.json`, row `A9_reserved_batch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 258 against a baseline of 258
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_batch_named_analyze_is_refused_before_the_gate_and_nothing_moves`

Old text:

```
    if batch == ANALYZE:
```

New text:

```
    if False:
```

### `u162.L10_interrupt_cancel`

_rehearse_native: an interrupt reported as internal-error rather than cancelled

- File: `src/cratekit/intake/land_cli.py`
- Source: `u162.json`, row `L10_interrupt_cancel`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_an_interrupted_rehearsal_is_a_cancel_that_names_its_area`

Old text:

```
            "cancelled",
```

New text:

```
            "internal-error",
```

### `u162.L12_rehearsal_equal`

rehearsal_facts: report every rehearsal as equal to the live plan

- File: `src/cratekit/intake/land_cli.py`
- Source: `u162.json`, row `L12_rehearsal_equal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_live_plan_that_differs_names_the_rehearsal_and_prints_the_differing_lines`

Old text:

```
    equal = found.get("digest") == digest
```

New text:

```
    equal = True
```

### `u162.L1_bridge_refusal`

intake_land: drop the refusal of --rehearse on an intake tree on the xml bridge

- File: `src/cratekit/intake/land_cli.py`
- Source: `u162.json`, row `L1_bridge_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_on_the_bridge_is_refused`

Old text:

```
    if rehearse and not medium.native:
```

New text:

```
    if False:
```

### `u162.L2_area_plan_compare`

_rehearse_in: drop the refusal of an area plan that is not the live plan, so a differing plan is applied

- File: `src/cratekit/intake/land_cli.py`
- Source: `u162.json`, row `L2_area_plan_compare`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 95 against a baseline of 95
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_scratch_plan_that_is_not_the_live_plan_applies_nothing`
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_file_name_that_differs_still_refuses_and_names_the_line`

Old text:

```
        if differ:
            raise refuse(
```

New text:

```
        if False:
            raise refuse(
```

### `u162.L4_occupied_hold`

_rehearse_in: drop the hold of the live batch folder's names at the area (round one's fix)

- File: `src/cratekit/intake/land_cli.py`
- Source: `u162.json`, row `L4_occupied_hold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_name_the_live_batch_folder_holds_is_refused_at_the_area_as_it_will_be_live`

Old text:

```
            if (target / item.name).exists() or (target / item.name).is_symlink():
```

New text:

```
            if False:
```

### `u162.L6_gridless_read_back`

_rehearse_in: drop the gridless read back of the landed rows

- File: `src/cratekit/intake/land_cli.py`
- Source: `u162.json`, row `L6_gridless_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_landed_row_read_back_with_a_grid_is_refused_and_never_reported_gridless`

Old text:

```
            native.assert_rows_gridless(landed.collection)
            native.assert_rows_identified(landed.collection)
            rows_after
```

New text:

```
            native.assert_rows_identified(landed.collection)
            rows_after
```

### `u162.L7_identified_read_back`

_rehearse_in: drop the file id read back of the landed rows

- File: `src/cratekit/intake/land_cli.py`
- Source: `u162.json`, row `L7_identified_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_landed_row_whose_file_id_did_not_take_is_refused_in_the_rehearsal`

Old text:

```
            native.assert_rows_gridless(landed.collection)
            native.assert_rows_identified(landed.collection)
            rows_after
```

New text:

```
            native.assert_rows_gridless(landed.collection)
            rows_after
```

### `u162.L8_success_witness`

_rehearse_native: drop the witness on the success path, so a rehearsal that touched the live library reports clean

- File: `src/cratekit/intake/land_cli.py`
- Source: `u162.json`, row `L8_success_witness`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 95 against a baseline of 95
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_a_batch_filed_in_another_year_is_refused`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_the_live_library_is_refused_as_a_defect`

Old text:

```
    rehearsal.assert_untouched(before, kept=area.paths)
    rehearsal.remove(area)
```

New text:

```
    rehearsal.remove(area)
```

### `u162.L9_kept_area_named`

_rehearse_native: a refusal inside the rehearsal no longer carries the kept area in its detail

- File: `src/cratekit/intake/land_cli.py`
- Source: `u162.json`, row `L9_kept_area_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 95 against a baseline of 95
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_refusal_inside_the_rehearsal_keeps_its_reason_and_names_the_area`
  - `tests/test_intake_land_rehearse.py::test_a_scratch_plan_that_is_not_the_live_plan_applies_nothing`
  - `tests/test_intake_land_rehearse.py::test_an_interrupted_rehearsal_keeps_its_area_and_names_it`
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_file_name_that_differs_still_refuses_and_names_the_line`

Old text:

```
            detail={**dict(inner.detail), "rehearsal_area": [str(path) for path in area.paths]},
```

New text:

```
            detail=dict(inner.detail),
```

### `u188.M1_stored_pair_dropped`

_mapped_back: leave the stored spelling pair out, so FolderPath on a renamed drive is never mapped back (the defect)

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M1_stored_pair_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 95 against a baseline of 95
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_batch_whose_name_is_not_ascii_rehearses_equal_and_the_gate_says_so`
  - `tests/test_intake_land_rehearse.py::test_a_library_whose_base_drive_is_not_its_mount_rehearses_equal_and_the_gate_says_so`
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_file_name_that_differs_still_refuses_and_names_the_line`

Old text:

```
                (str(scratch_target), str(target)),
                stored,
            )
```

New text:

```
                (str(scratch_target), str(target)),
            )
```

### `u188.M2_scratch_stored_under_the_mount`

_mapped_back: spell the area's folder with no base drive, so the scratch side of the stored pair is the mounted spelling

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M2_scratch_stored_under_the_mount`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 95 against a baseline of 95
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_batch_whose_name_is_not_ascii_rehearses_equal_and_the_gate_says_so`
  - `tests/test_intake_land_rehearse.py::test_a_library_whose_base_drive_is_not_its_mount_rehearses_equal_and_the_gate_says_so`
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_file_name_that_differs_still_refuses_and_names_the_line`

Old text:

```
            base_drive=scratch_rows.base_drive,
            current_drive=scratch_rows.current_drive,
```

New text:

```
            base_drive=None,
            current_drive=scratch_rows.current_drive,
```

### `u188.M3_live_stored_under_the_mount`

_mapped_back: spell the live folder with no base drive, so the area's FolderPath maps to the mounted spelling the live rows do not carry

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M3_live_stored_under_the_mount`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 95 against a baseline of 95
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_batch_whose_name_is_not_ascii_rehearses_equal_and_the_gate_says_so`
  - `tests/test_intake_land_rehearse.py::test_a_library_whose_base_drive_is_not_its_mount_rehearses_equal_and_the_gate_says_so`
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_file_name_that_differs_still_refuses_and_names_the_line`

Old text:

```
            target, base_drive=rows.base_drive, current_drive=rows.current_drive
```

New text:

```
            target, base_drive=None, current_drive=rows.current_drive
```

### `u188.M4_staging_pair_dropped`

_mapped_back: leave the staging pair out, so every from line keeps the area's staging

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M4_staging_pair_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 95 against a baseline of 95
- Kills: 20 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_batch_whose_name_is_not_ascii_rehearses_equal_and_the_gate_says_so`
  - `tests/test_intake_land_rehearse.py::test_a_copy_that_fails_its_integrity_check_is_refused_naming_the_area`
  - `tests/test_intake_land_rehearse.py::test_a_landed_row_read_back_with_a_grid_is_refused_and_never_reported_gridless`
  - `tests/test_intake_land_rehearse.py::test_a_landed_row_whose_file_id_did_not_take_is_refused_in_the_rehearsal`
  - `tests/test_intake_land_rehearse.py::test_a_library_whose_base_drive_is_not_its_mount_rehearses_equal_and_the_gate_says_so`
  - `tests/test_intake_land_rehearse.py::test_a_live_plan_that_differs_names_the_rehearsal_and_prints_the_differing_lines`
  - `tests/test_intake_land_rehearse.py::test_a_name_the_live_batch_folder_holds_is_refused_at_the_area_as_it_will_be_live`
  - `tests/test_intake_land_rehearse.py::test_a_refusal_inside_the_rehearsal_keeps_its_reason_and_names_the_area`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_beside_another_runs_area_lands_and_leaves_that_area_alone`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_check_whose_copy_fails_otherwise_is_still_a_failed_check`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_check_whose_copy_finds_no_room_is_refused_under_the_room_slug`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_leaves_staging_the_music_folder_and_the_database_as_they_were`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_of_another_batch_is_not_the_one_compared`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_a_batch_filed_in_another_year_is_refused`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_the_live_library_is_refused_as_a_defect`
  - ... and 5 more, see the JSON sidecar

Old text:

```
                (str(area.staging), str(planned.folder)),
                (str(scratch_target), str(target)),
```

New text:

```
                (str(scratch_target), str(target)),
```

### `u188.M6_mapped_as_lines`

_rehearse_in: map the area's plan after it is printed, so a JSON escaped accent or quote is never mapped (the review's round one)

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M6_mapped_as_lines`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 95 against a baseline of 95
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_batch_whose_name_is_not_ascii_rehearses_equal_and_the_gate_says_so`
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_file_name_that_differs_still_refuses_and_names_the_line`

Old text:

```
        back = rehearsal.lines(
            rehearsal.mapped(
                plan_identity(staged, scratch_rows, target=scratch_target, archived=archived),
                pairs,
            )
        )
```

New text:

```
        back = rehearsal.mapped(
            plan_lines(staged, scratch_rows, target=scratch_target, archived=archived), pairs
        )
```

### `u219.G1_resort_abort`

route resort: an abort at the gate queues the resort anyway

- File: `src/cratekit/write/routing_cli.py`
- Source: `u219.json`, row `G1_resort_abort`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_organize_mirror_edits.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 309 against a baseline of 309
- Kills: 1 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_an_abort_queues_nothing_and_writes_nothing`

Old text:

```
    if option != "apply":
        return ctx.envelope(data=_no_op("declined"), outcome=Outcome.NO_OP, warnings=warnings)
```

New text:

```
    if option == "never":
        return ctx.envelope(data=_no_op("declined"), outcome=Outcome.NO_OP, warnings=warnings)
```

### `u219.G2_nothing_to_add`

route resort: queue a job over a plan with nothing to add

- File: `src/cratekit/write/routing_cli.py`
- Source: `u219.json`, row `G2_nothing_to_add`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_organize_mirror_edits.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 309 against a baseline of 309
- Kills: 1 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_resort_with_no_change_plans_nothing_and_queues_nothing`

Old text:

```
    if not adds:
        return ctx.envelope(
```

New text:

```
    if False:
        return ctx.envelope(
```

### `u219.G3_adds_frozen`

route resort: freeze an empty plan in the job, so the worker holds its write to nothing the gate showed

- File: `src/cratekit/write/routing_cli.py`
- Source: `u219.json`, row `G3_adds_frozen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_organize_mirror_edits.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 309 against a baseline of 309
- Kills: 21 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_library_that_moved_after_the_gate_refuses_before_writing`
  - `tests/test_resort_scope.py::test_a_resort_after_a_genre_sub_writes_nothing_under_the_intake_root`
  - `tests/test_resort_scope.py::test_a_resort_that_left_a_favourite_for_later_says_so`
  - `tests/test_resort_scope.py::test_a_resort_with_no_change_plans_nothing_and_queues_nothing`
  - `tests/test_resort_scope.py::test_a_resort_writes_no_favourite_its_gate_did_not_show`
  - `tests/test_resort_scope.py::test_the_favourite_a_resort_left_is_shown_and_filed_by_the_next`
  - `tests/test_resort_scope.py::test_two_files_that_swap_places_after_the_gate_refuse_by_their_paths`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[above-resort]`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[below-resort]`
  - `tests/test_routing_workers.py::test_a_driven_resume_over_no_favorites_class_names_the_skipped_step[resort]`
  - `tests/test_routing_workers.py::test_a_driven_resume_over_the_declared_class_says_nothing_of_it[resort]`
  - `tests/test_routing_workers.py::test_a_driven_resume_says_the_vocal_dimension_was_not_compared_beside_drift[resort]`
  - `tests/test_routing_workers.py::test_a_queued_rebuild_and_resort_run_on_an_encrypted_library[resort]`
  - `tests/test_routing_workers.py::test_a_queued_resort_runs_its_item_and_the_tree_holds_the_track`
  - `tests/test_routing_workers.py::test_a_rebuild_of_another_tree_says_nothing_of_the_routing_trees_favorites[resort]`
  - ... and 6 more, see the JSON sidecar

Old text:

```
                RESORT_ADDS_KEY: adds,
```

New text:

```
                RESORT_ADDS_KEY: [],
```

### `u219.G4_worker_own_tree`

handle_resort: hand the engine every tree's approved adds, not its own tree's

- File: `src/cratekit/write/routing_cli.py`
- Source: `u219.json`, row `G4_worker_own_tree`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_organize_mirror_edits.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 309 against a baseline of 309
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_each_worker_names_its_own_verb_and_rebuilds_the_item_it_was_handed`

Old text:

```
            if row.get("tree") == tree_id
```

New text:

```
            if row.get("tree") is not None
```

### `u219.G5_resume_run`

resort_argv: drop --run, so the spawned child meets the explicit gate with nothing recorded

- File: `src/cratekit/write/routing_cli.py`
- Source: `u219.json`, row `G5_resume_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_organize_mirror_edits.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 309 against a baseline of 309
- Kills: 1 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_the_resume_argv_names_the_gate_run`

Old text:

```
    resume = ["--run", str(gate_run)] if gate_run else []
    return [*resume, "route", "resort", "--job", job.job_id]
```

New text:

```
    resume = []
    return [*resume, "route", "resort", "--job", job.job_id]
```

