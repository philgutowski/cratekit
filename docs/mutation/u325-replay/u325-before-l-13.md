# Mutation table: u325-before-l-13

Measured by `scripts/mutate.py` on 2026-11-23 00:15 UTC, branch `HEAD` at `539638eb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22663 collected. pytest invocations for this batch: 21.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:15 UTC for commit `539638ebe629`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 14, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard. 111 row(s) were reused from a prior sidecar and were measured by an earlier process, whose children this run did not watch.

Null control `NULL_CONTROL`: killed 0, collected 22663 against 22663. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u146-b.B14_plan_owned_keeps_held_hearts` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 18 | 1 | killed |
| `u146-b.A1_superseded_ignored` | `src/cratekit/intake/account_playlists.py` | user | 1 file(s) | 18 | 1 | killed |
| `u146-b.A2_owned_reads_carried` | `src/cratekit/intake/account_playlists.py` | user | 1 file(s) | 18 | 12 | killed |
| `u146-b.A3_report_paths_dropped` | `src/cratekit/intake/account_playlists.py` | user | 1 file(s) | 18 | 11 | killed |
| `u146-c.L2_empty_landing_no_op` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 18 | 7 | killed |
| `u146-c.L3_gate_asked_for_nothing` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 18 | 4 | killed |
| `u146-c.L4_missing_source_refuses` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 18 | 1 | killed |
| `u146-c.N1_owned_held_planned` | `src/cratekit/intake/native.py` | user | 1 file(s) | 18 | 2 | killed |
| `u146-c.N2_owned_not_written` | `src/cratekit/intake/native.py` | user | 1 file(s) | 18 | 2 | killed |
| `u146-c.N4_owned_needs_a_heart_file` | `src/cratekit/intake/native.py` | user | 1 file(s) | 18 | 1 | killed |
| `u146-e.N3_owned_out_of_digest` | `src/cratekit/intake/native.py` | user | 1 file(s) | 22663 | 0 (promoted) | zero |
| `u153.N3_landing_colour_owned` | `src/cratekit/intake/native.py` | user | 1 file(s) | 18 | 1 | killed |
| `u105-b.S10_settings_to_engine` | `src/cratekit/master/cli.py` | user | 3 file(s) | 145 | 2 | killed |
| `u105-b.S1_parts_only_when_several` | `src/cratekit/master/cli.py` | user | 3 file(s) | 145 | 3 | killed |
| `u105-b.S2_lufs_frozen` | `src/cratekit/master/cli.py` | user | 3 file(s) | 145 | 2 | killed |
| `u105-b.S3_lufs_in_argv` | `src/cratekit/master/cli.py` | user | 3 file(s) | 145 | 1 | killed |
| `u105-b.S4_parts_in_argv` | `src/cratekit/master/cli.py` | user | 3 file(s) | 145 | 1 | killed |
| `u105-b.S5_queue_time_refusal` | `src/cratekit/master/cli.py` | user | 3 file(s) | 145 | 3 | killed |
| `u105-b.S6_join_order_notice` | `src/cratekit/master/cli.py` | user | 3 file(s) | 145 | 1 | killed |
| `u105-b.S7_staged_parts` | `src/cratekit/master/cli.py` | user | 3 file(s) | 145 | 1 | killed |
| `u105-b.S8_staged_target` | `src/cratekit/master/cli.py` | user | 3 file(s) | 145 | 1 | killed |
| `u105-b.S9_precheck_name` | `src/cratekit/master/cli.py` | user | 3 file(s) | 145 | 2 | killed |
| `u177.A10_clear_word` | `src/cratekit/label/cli.py` | user | 4 file(s) | 144 | 1 | killed |
| `u177.A11_field_flag_guard` | `src/cratekit/label/cli.py` | user | 4 file(s) | 144 | 7 | killed |
| `u177.A9_add_drops_account` | `src/cratekit/label/cli.py` | user | 4 file(s) | 144 | 12 | killed |
| `u177.A1_account_suffix` | `src/cratekit/label/registry.py` | user | 4 file(s) | 144 | 23 | killed |
| `u177.A2_account_shape` | `src/cratekit/label/registry.py` | user | 4 file(s) | 144 | 4 | killed |
| `u177.A3_account_case` | `src/cratekit/label/registry.py` | user | 4 file(s) | 144 | 5 | killed |
| `u177.A4_claim_removed` | `src/cratekit/label/registry.py` | user | 4 file(s) | 144 | 2 | killed |
| `u177.A5_claim_self` | `src/cratekit/label/registry.py` | user | 4 file(s) | 144 | 1 | killed |
| `u177.A7_stored_raw` | `src/cratekit/label/registry.py` | user | 4 file(s) | 144 | 2 | killed |
| `u177.A8_edit_drops_account` | `src/cratekit/label/registry.py` | user | 4 file(s) | 144 | 2 | killed |
| `r777-confirm.N4_plain_name` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 141 | 1 | killed |
| `r777-confirm.N7_digest_marks` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 141 | 1 | killed |
| `r777.N10_screen_says_pass` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 141 | 1 | killed |
| `r777.N11_exclusive` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 141 | 1 | killed |
| `r777.N12_no_landing_required` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 141 | 4 | killed |
| `r777.N18_unreachable_called_bridge` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 141 | 1 | killed |
| `r777.N19_digest_landings` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 141 | 1 | killed |
| `r777.N5_bridge_accepted` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 141 | 2 | killed |
| `r777.N6_no_reread` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 141 | 2 | killed |
| `r777.N9_proof_is_file` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 141 | 4 | killed |
| `r598-b.B1_sweep_before_the_lock` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `r598-b.B3_orphans_not_shown` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 2 | killed |
| `r598-b.B4_abandon_only_reported_as_no_op` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `r598-b.B5_kept_reports_nothing` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 4 | killed |
| `u49-author.A2_the_abort_mints_anyway` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 2 | killed |
| `u49-author.A3_the_refusal_names_no_ages` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 4 | killed |
| `u49-author.A4_the_record_on_file_is_not_shown` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 2 | killed |
| `u49-author.A6_the_authorisation_is_not_spent` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `u49-author.A7_the_check_rows_are_keyed_wrong` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `u49-author.A8_a_damaged_record_locks_the_verb_out` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `u49-author.R1_hard_code_the_repair_token` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `u49-author.R2_hard_code_the_permission_token` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 2 | killed |
| `u49-author.R3_an_unreadable_file_reads_as_empty` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 2 | killed |
| `u236.M13_write_records_no_month` | `src/cratekit/organize/mirror_edits.py` | user | 8 file(s) | 233 | 6 | killed |
| `u236.M14_write_wrong_time` | `src/cratekit/organize/mirror_edits.py` | user | 8 file(s) | 233 | 6 | killed |
| `u236.M15_settle_month_title` | `src/cratekit/organize/mirror_edits.py` | user | 8 file(s) | 233 | 8 | killed |
| `u236.M16_settle_any_favourite` | `src/cratekit/organize/mirror_edits.py` | user | 8 file(s) | 233 | 1 | killed |
| `u236.M17_ledger_settle_keeps_placement` | `src/cratekit/modules/outbound/ledger.py` | user | 8 file(s) | 233 | 4 | killed |
| `u236.M18_ledger_placement_not_written` | `src/cratekit/modules/outbound/ledger.py` | user | 8 file(s) | 233 | 8 | killed |
| `u236.M19_ledger_normalizer_drops` | `src/cratekit/modules/outbound/ledger.py` | user | 8 file(s) | 233 | 8 | killed |
| `u236.M20_agreed_never_drops` | `src/cratekit/modules/outbound/ledger.py` | user | 8 file(s) | 233 | 3 | killed |
| `r796-c.V1_the_worker_hands_the_seam_over` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 381 | 10 | killed |
| `r796-c.V2_blocked_warning_is_the_shops_only` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 381 | 1 | killed |
| `r796-c.V3_some_unread_is_said` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 381 | 1 | killed |
| `r796-c.V4_no_isrc_is_warned_about` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 381 | 1 | killed |
| `r796-c.V5_parse_break_sentence_said_once` | `src/cratekit/tagging/cli.py` | maintainer | 4 file(s) | 381 | 1 | killed |
| `r796-b.O9_no_isrc_is_not_no_hit` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 381 | 3 | killed |
| `u217.A1_flush_on_the_way_out` | `src/cratekit/label/tidal_catalogue.py` | user | 2 file(s) | 212 | 12 | killed |
| `u217.A2_roster_lists_now` | `src/cratekit/label/tidal_catalogue.py` | user | 2 file(s) | 212 | 7 | killed |
| `u217.A3_listing_not_kept` | `src/cratekit/label/tidal_catalogue.py` | user | 2 file(s) | 212 | 12 | killed |
| `u217.A4_search_not_kept` | `src/cratekit/label/tidal_catalogue.py` | user | 2 file(s) | 212 | 10 | killed |
| `u217.A5_name_not_kept` | `src/cratekit/label/tidal_catalogue.py` | user | 2 file(s) | 212 | 1 | killed |
| `u217.A6_need_object` | `src/cratekit/label/tidal_catalogue.py` | user | 2 file(s) | 212 | 1 | killed |
| `u217.A7_missing_method_kept` | `src/cratekit/label/tidal_catalogue.py` | user | 2 file(s) | 212 | 1 | killed |
| `u217.A8_member_read_uncounted` | `src/cratekit/label/tidal_catalogue.py` | user | 2 file(s) | 212 | 1 | killed |
| `r1255.S1_scan_unlisted_as_empty` | `src/cratekit/core/session.py` | user | 7 file(s) | 891 | 16 | killed |
| `r1255.S2_absent_log_unread` | `src/cratekit/core/session.py` | user | 7 file(s) | 891 | 63 | killed |
| `r1255.S5_json_filter` | `src/cratekit/core/session.py` | user | 7 file(s) | 891 | 1 | killed |
| `r185-r246-author.E1_plan_gate_by_position` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 1 | killed |
| `r185-r246-author.E3_empty_plan_queues_anyway` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 2 | killed |
| `r185-r246-author.M1_folder_dropped` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 5 | killed |
| `r185-r246-author.W1_queue_warning_dropped` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 1 | killed |
| `r185-r246-author.W2_resume_warning_dropped` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 1 | killed |
| `r185-r246-author.W3_resume_warning_unconditional` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 1 | killed |
| `r185-r246-author.W4_refusal_step_dropped` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 3 | killed |
| `r185-r246-author.W5_refusal_step_unconditional` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 2 | killed |
| `r185-r246-author.W6_refusal_counts_the_plan` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 2 | killed |
| `u288.M10_changed_rows` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 264 | 4 | killed |
| `u288.M11_added_rows` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 264 | 2 | killed |
| `u288.M12_still_names` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 264 | 2 | killed |
| `u288.M13_counter_forward` | `src/cratekit/core/rb_writer.py` | maintainer | 2 file(s) | 264 | 1 | killed |
| `u288.M1_delete_admitted_by_any_name` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 264 | 2 | killed |
| `u288.M2_deletable_set_unbounded` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 264 | 1 | killed |
| `u288.M9_whose_row_disappeared` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 264 | 1 | killed |
| `r1017.M12_twin_message_names_to` | `src/cratekit/export/set_cli.py` | user | 4 file(s) | 195 | 1 | killed |
| `r1017.M1_no_recorded_names` | `src/cratekit/export/set_cli.py` | user | 4 file(s) | 195 | 5 | killed |
| `r1017.M2_recorded_before_frozen` | `src/cratekit/export/set_cli.py` | user | 4 file(s) | 195 | 1 | killed |
| `r1017.M3_landing_open_read` | `src/cratekit/intake/set_playlist.py` | user | 4 file(s) | 195 | 1 | killed |
| `r1017.M4_landing_uncommitted_read` | `src/cratekit/intake/set_playlist.py` | user | 4 file(s) | 195 | 1 | killed |
| `r1017.M5_landing_any_job` | `src/cratekit/intake/set_playlist.py` | user | 4 file(s) | 195 | 2 | killed |
| `r1017.M6_oldest_first` | `src/cratekit/intake/set_playlist.py` | user | 4 file(s) | 195 | 1 | killed |
| `r1017.M7_names_not_deduplicated` | `src/cratekit/intake/set_playlist.py` | maintainer | 4 file(s) | 195 | 1 | killed |
| `r740-a.N1_no_fill` | `src/cratekit/core/naming.py` | user | 4 file(s) | 253 | 17 | killed |
| `r740-a.N2_no_agreement` | `src/cratekit/core/naming.py` | user | 4 file(s) | 253 | 3 | killed |
| `r740-a.N3_key_compared_raw` | `src/cratekit/core/naming.py` | user | 4 file(s) | 253 | 3 | killed |
| `r740-a.N4_stem_before_title` | `src/cratekit/core/naming.py` | user | 4 file(s) | 253 | 1 | killed |
| `r740-a.N5_no_marker_fill` | `src/cratekit/core/naming.py` | user | 4 file(s) | 253 | 4 | killed |
| `r740-a.N6_current_ignores_filled` | `src/cratekit/core/naming.py` | user | 4 file(s) | 253 | 1 | killed |
| `r740-b.E1_library_name_from_stem` | `src/cratekit/core/naming.py` | user | 4 file(s) | 253 | 4 | killed |
| `u113-a.A3_no_pass_splits_nothing` | `src/cratekit/intake/account_playlists.py` | user | 1 file(s) | 22663 | 0 (promoted) | zero |
| `u72-b.M20_shown_files` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 48 | 2 | killed |
| `u72-b.M21_empty_to_engine` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 48 | 3 | killed |
| `u72-b.M22_listing_without_isdir` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 48 | 1 | killed |
| `u72.M10_default_folder` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 48 | 32 | killed |

## Zero rows and what they owe

- `u146-e.N3_owned_out_of_digest` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u113-a.A3_no_pass_splits_nothing` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

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

### `u146-b.A1_superseded_ignored`

owned_hearts: an older pass places its owned hearts though a later hearts job ran, putting back a heart dropped since

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u146-b.json`, row `A1_superseded_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_landing_an_older_pass_places_no_owned_heart_once_a_later_hearts_job_ran`

Old text:

```
    if superseded:
        return ()
```

New text:

```
    if superseded and False:
        return ()
```

### `u146-b.A2_owned_reads_carried`

owned_hearts: reads the carried states, so the landing finds no owned heart

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u146-b.json`, row `A2_owned_reads_carried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 18 against a baseline of 18
- Kills: 12 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_a_pass_whose_owned_hearts_are_all_placed_asks_nothing_and_ends_no_op`
  - `tests/test_intake_land_owned_hearts_native.py::test_a_present_coloured_owned_heart_beside_a_landed_file_is_held_and_named`
  - `tests/test_intake_land_owned_hearts_native.py::test_a_track_removed_from_all_favorites_by_hand_and_still_hearted_joins_again`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_beside_a_landed_file_takes_pink_in_the_same_commit`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_is_coloured_pink_and_one_a_person_coloured_is_held`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_beside_a_landed_file_that_is_no_heart`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_in_the_same_commit_as_a_downloaded_one`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_placed_by_hand_between_the_two_acts_makes_the_answer_stale`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_the_account_dates_nowhere_goes_to_undated`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_only_pass_refuses_before_the_gate_with_no_acknowledgment`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_track_hearted_today_joins_all_favorites_and_its_month_with_nothing_downloaded`
  - `tests/test_intake_land_owned_hearts_native.py::test_with_no_all_favorites_an_owned_only_pass_ends_no_op_and_says_why`

Old text:

```
    return hearts(cfg, pass_name, states=frozenset({OWNED}))
```

New text:

```
    return hearts(cfg, pass_name)
```

### `u146-b.A3_report_paths_dropped`

carried_hearts: the report's files are not carried on the row, so no owned heart has a row to place

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u146-b.json`, row `A3_report_paths_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 18 against a baseline of 18
- Kills: 11 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_a_pass_whose_owned_hearts_are_all_placed_asks_nothing_and_ends_no_op`
  - `tests/test_intake_land_owned_hearts_native.py::test_a_present_coloured_owned_heart_beside_a_landed_file_is_held_and_named`
  - `tests/test_intake_land_owned_hearts_native.py::test_a_track_removed_from_all_favorites_by_hand_and_still_hearted_joins_again`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_beside_a_landed_file_takes_pink_in_the_same_commit`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_is_coloured_pink_and_one_a_person_coloured_is_held`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_beside_a_landed_file_that_is_no_heart`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_in_the_same_commit_as_a_downloaded_one`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_placed_by_hand_between_the_two_acts_makes_the_answer_stale`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_the_account_dates_nowhere_goes_to_undated`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_only_pass_refuses_before_the_gate_with_no_acknowledgment`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_track_hearted_today_joins_all_favorites_and_its_month_with_nothing_downloaded`

Old text:

```
                known=intake_cli.HEARTED in said,
                paths=tuple(str(path) for path in (report.get("paths") or ())),
```

New text:

```
                known=intake_cli.HEARTED in said,
                paths=(),
```

### `u146-c.L2_empty_landing_no_op`

_land_native: an empty landing ends NO_OP as before, its owned hearts never placed

- File: `src/cratekit/intake/land_cli.py`
- Source: `u146-c.json`, row `L2_empty_landing_no_op`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 18 against a baseline of 18
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_a_pass_whose_owned_hearts_are_all_placed_asks_nothing_and_ends_no_op`
  - `tests/test_intake_land_owned_hearts_native.py::test_a_track_removed_from_all_favorites_by_hand_and_still_hearted_joins_again`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_is_coloured_pink_and_one_a_person_coloured_is_held`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_the_account_dates_nowhere_goes_to_undated`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_only_pass_refuses_before_the_gate_with_no_acknowledgment`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_track_hearted_today_joins_all_favorites_and_its_month_with_nothing_downloaded`
  - `tests/test_intake_land_owned_hearts_native.py::test_with_no_all_favorites_an_owned_only_pass_ends_no_op_and_says_why`

Old text:

```
        if owned:
            return _place_owned(
```

New text:

```
        if owned and False:
            return _place_owned(
```

### `u146-c.L3_gate_asked_for_nothing`

_place_owned: a pass whose owned hearts are all placed opens the database to write and asks the gate over nothing

- File: `src/cratekit/intake/land_cli.py`
- Source: `u146-c.json`, row `L3_gate_asked_for_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 18 against a baseline of 18
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_a_pass_whose_owned_hearts_are_all_placed_asks_nothing_and_ends_no_op`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_all_favorites_holds_without_a_month_is_no_write_for_an_empty_landing`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_whose_file_two_rows_claim_is_not_placed_by_a_guess`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_whose_job_froze_no_date_key_is_left_to_the_backfill`

Old text:

```
    if not first.writes:
        return ctx.envelope(data=empty, outcome=Outcome.NO_OP)
```

New text:

```
(empty)
```

### `u146-c.L4_missing_source_refuses`

_place_owned: a library with no All Favorites refuses the empty landing instead of ending NO_OP and saying why

- File: `src/cratekit/intake/land_cli.py`
- Source: `u146-c.json`, row `L4_missing_source_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_with_no_all_favorites_an_owned_only_pass_ends_no_op_and_says_why`

Old text:

```
        if exc.cause.reason != placement.SOURCE_MISSING:
            raise
        return ctx.envelope(
            data=empty,
```

New text:

```
        raise
        return ctx.envelope(
            data=empty,
```

### `u146-c.N1_owned_held_planned`

_favorites_plan: an owned heart All Favorites holds is planned again beside a landing, and its month made

- File: `src/cratekit/intake/native.py`
- Source: `u146-c.json`, row `N1_owned_held_planned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 18 against a baseline of 18
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_all_favorites_holds_is_no_write_beside_a_landing`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_placed_by_hand_between_the_two_acts_makes_the_answer_stale`

Old text:

```
        if one.content_id in in_source or one.content_id in seen:
```

New text:

```
        if one.content_id in seen:
```

### `u146-c.N2_owned_not_written`

apply_rows: the owned hearts are planned and shown and never written

- File: `src/cratekit/intake/native.py`
- Source: `u146-c.json`, row `N2_owned_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 18 against a baseline of 18
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_beside_a_landed_file_that_is_no_heart`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_in_the_same_commit_as_a_downloaded_one`

Old text:

```
                pairs.extend((one.content_id, one.month) for one in plan.favorites.owned)
```

New text:

```
(empty)
```

### `u146-c.N4_owned_needs_a_heart_file`

_favorites_plan: owned hearts are placed only when a landed file is a heart too

- File: `src/cratekit/intake/native.py`
- Source: `u146-c.json`, row `N4_owned_needs_a_heart_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_beside_a_landed_file_that_is_no_heart`

Old text:

```
    if not (kept or owned) or not source:
```

New text:

```
    if not kept or not source:
```

### `u146-e.N3_owned_out_of_digest`

FavoritesPlan.identity: the owned hearts are not digested, so an answer given for one set of them stands for another

- File: `src/cratekit/intake/native.py`
- Source: `u146-e.json`, row `N3_owned_out_of_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if self.owned:
            identity["owned"] = [
```

New text:

```
        if self.owned and False:
            identity["owned"] = [
```

### `u153.N3_landing_colour_owned`

native apply: drop the owned hearts from the colour set, so an owned heart is placed but not coloured

- File: `src/cratekit/intake/native.py`
- Source: `u153.json`, row `N3_landing_colour_owned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_beside_a_landed_file_takes_pink_in_the_same_commit`

Old text:

```
                to_colour.extend(plan.favorites.colour)
```

New text:

```
                to_colour.extend([])
```

### `u105-b.S10_settings_to_engine`

Call the engine without the settings built from the frozen target

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S10_settings_to_engine`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 145 against a baseline of 145
- Kills: 2 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_queued_split_recording_lands_as_one_master_through_the_resume`
  - `tests/test_master_cli.py::test_the_target_reaches_every_loudnorm_filter`

Old text:

```
            settings=settings,
            output_dir=Path(output_dir) if output_dir else None,
```

New text:

```
            output_dir=Path(output_dir) if output_dir else None,
```

### `u105-b.S1_parts_only_when_several`

Freeze the parts key for a single recording too

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S1_parts_only_when_several`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 145 against a baseline of 145
- Kills: 3 (killed)
- Killed:
  - `tests/test_job_seam.py::test_a_driver_killed_inside_the_real_handler_resumes_redoing_exactly_that_item`
  - `tests/test_job_seam.py::test_the_partial_encode_a_kill_leaves_behind_is_in_staging_not_at_the_destination`
  - `tests/test_master_cli.py::test_one_input_freezes_queues_and_resumes_exactly_as_before`

Old text:

```
    if len(frozen) > 1:
```

New text:

```
    if frozen:
```

### `u105-b.S2_lufs_frozen`

Do not freeze --lufs into the payload

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S2_lufs_frozen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 145 against a baseline of 145
- Kills: 2 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_queued_split_recording_lands_as_one_master_through_the_resume`
  - `tests/test_master_cli.py::test_the_target_reaches_every_loudnorm_filter`

Old text:

```
        payload[TARGET_LUFS] = float(lufs)
```

New text:

```
        pass
```

### `u105-b.S3_lufs_in_argv`

Drop --lufs from the resume command line

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S3_lufs_in_argv`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 145 against a baseline of 145
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_split_recording_and_its_target_survive_the_resume_argv`

Old text:

```
        argv.append(f"--lufs={lufs}")
```

New text:

```
        pass
```

### `u105-b.S4_parts_in_argv`

Rebuild the resume command line from the first part alone

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S4_parts_in_argv`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 145 against a baseline of 145
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_split_recording_and_its_target_survive_the_resume_argv`

Old text:

```
    argv = ["master", *frozen_parts(payload)]
```

New text:

```
    argv = ["master", str(payload.get(SOURCE) or "")]
```

### `u105-b.S5_queue_time_refusal`

Stop validating --lufs at queue time

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S5_queue_time_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 145 against a baseline of 145
- Kills: 3 (killed)
- Killed:
  - `tests/test_master_cli.py::test_an_out_of_range_target_refuses_and_queues_nothing[-4]`
  - `tests/test_master_cli.py::test_an_out_of_range_target_refuses_and_queues_nothing[-71]`
  - `tests/test_master_cli.py::test_an_out_of_range_target_refuses_and_queues_nothing[nan]`

Old text:

```
    settings_for(ctx.args.lufs)
```

New text:

```
    pass
```

### `u105-b.S6_join_order_notice`

Queue a split recording without saying its order back

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S6_join_order_notice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 145 against a baseline of 145
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_the_order_printed_is_the_order_given`

Old text:

```
        notices = (join_order_warning(frozen_parts(payload)),) if PARTS in payload else ()
```

New text:

```
        notices = ()
```

### `u105-b.S7_staged_parts`

Stage a split recording's run without its parts, mastering part one alone

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S7_staged_parts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 145 against a baseline of 145
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_queued_split_recording_lands_as_one_master_through_the_resume`

Old text:

```
        staged[PARTS] = [str(p) for p in parts]
```

New text:

```
        pass
```

### `u105-b.S8_staged_target`

Stage the run without the frozen target, mastering at the default

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S8_staged_target`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 145 against a baseline of 145
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_queued_split_recording_lands_as_one_master_through_the_resume`

Old text:

```
        staged[TARGET_LUFS] = payload[TARGET_LUFS]
```

New text:

```
        pass
```

### `u105-b.S9_precheck_name`

Pre-check the destination with part one's master name instead of the joined one

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S9_precheck_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 145 against a baseline of 145
- Kills: 2 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_queued_split_recording_lands_as_one_master_through_the_resume`
  - `tests/test_master_cli.py::test_an_existing_joined_master_is_refused_on_the_real_destination`

Old text:

```
    final = mastering.planned_output(
        parts, output_dir=Path(str(output_dir)) if output_dir else None
    )
```

New text:

```
    final = mastering.output_path(
        parts[0], output_dir=Path(str(output_dir)) if output_dir else None
    )
```

### `u177.A10_clear_word`

registry_cmd: drop the clear word, so --bandcamp default stores an account named default

- File: `src/cratekit/label/cli.py`
- Source: `u177.json`, row `A10_clear_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_bandcamp_account.py`, `tests/test_label_registry_verbs.py`, `tests/test_bandcamp_labels.py`, `tests/test_label_genre.py`
- Collected: 144 against a baseline of 144
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_bandcamp_account.py::test_default_clears_the_account_and_frees_it_for_another_label`

Old text:

```
    clear_bandcamp = bandcamp is not None and bandcamp.strip().lower() == labels.CLEAR_BANDCAMP

```

New text:

```
    clear_bandcamp = False

```

### `u177.A11_field_flag_guard`

registry_cmd: leave --bandcamp out of the fields given, so remove --bandcamp is silently ignored and set --bandcamp alone refused

- File: `src/cratekit/label/cli.py`
- Source: `u177.json`, row `A11_field_flag_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_bandcamp_account.py`, `tests/test_label_registry_verbs.py`, `tests/test_bandcamp_labels.py`, `tests/test_label_genre.py`
- Collected: 144 against a baseline of 144
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_bandcamp_account.py::test_a_label_setting_its_own_account_again_is_no_conflict`
  - `tests/test_label_bandcamp_account.py::test_a_second_label_naming_a_held_account_is_refused_by_the_holders_name`
  - `tests/test_label_bandcamp_account.py::test_bandcamp_on_an_action_that_does_not_set_it_refuses[action0]`
  - `tests/test_label_bandcamp_account.py::test_bandcamp_on_an_action_that_does_not_set_it_refuses[action1]`
  - `tests/test_label_bandcamp_account.py::test_bandcamp_on_an_action_that_does_not_set_it_refuses[action2]`
  - `tests/test_label_bandcamp_account.py::test_default_clears_the_account_and_frees_it_for_another_label`
  - `tests/test_label_bandcamp_account.py::test_set_with_only_bandcamp_is_a_field_to_change`

Old text:

```
    fields_given = (seeds, track_limit, ctx.args.match, offer, kind, genre, bandcamp)

```

New text:

```
    fields_given = (seeds, track_limit, ctx.args.match, offer, kind, genre)

```

### `u177.A9_add_drops_account`

registry_cmd add: pass no account to the store, so add --bandcamp is accepted and never written

- File: `src/cratekit/label/cli.py`
- Source: `u177.json`, row `A9_add_drops_account`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_bandcamp_account.py`, `tests/test_label_registry_verbs.py`, `tests/test_bandcamp_labels.py`, `tests/test_label_genre.py`
- Collected: 144 against a baseline of 144
- Kills: 12 (killed)
- Killed:
  - `tests/test_label_bandcamp_account.py::test_a_rename_of_the_label_keeps_its_seller`
  - `tests/test_label_bandcamp_account.py::test_a_second_label_naming_a_held_account_is_refused_by_the_holders_name`
  - `tests/test_label_bandcamp_account.py::test_a_seller_on_its_own_domain_keeps_the_whole_host`
  - `tests/test_label_bandcamp_account.py::test_add_with_an_account_round_trips_through_list`
  - `tests/test_label_bandcamp_account.py::test_an_account_named_default_is_set_by_its_address`
  - `tests/test_label_bandcamp_account.py::test_an_address_or_any_case_is_stored_as_the_account_a_purchase_is_read_as[  pulsromania  ]`
  - `tests/test_label_bandcamp_account.py::test_an_address_or_any_case_is_stored_as_the_account_a_purchase_is_read_as[PulsRomania]`
  - `tests/test_label_bandcamp_account.py::test_an_address_or_any_case_is_stored_as_the_account_a_purchase_is_read_as[https://PulsRomania.bandcamp.com/music]`
  - `tests/test_label_bandcamp_account.py::test_an_address_or_any_case_is_stored_as_the_account_a_purchase_is_read_as[https://pulsromania.bandcamp.com]`
  - `tests/test_label_bandcamp_account.py::test_an_address_or_any_case_is_stored_as_the_account_a_purchase_is_read_as[pulsromania.bandcamp.com/album/sun-path]`
  - `tests/test_label_bandcamp_account.py::test_an_address_or_any_case_is_stored_as_the_account_a_purchase_is_read_as[pulsromania.bandcamp.com]`
  - `tests/test_label_bandcamp_account.py::test_set_of_another_field_keeps_the_account`

Old text:

```
            genre=genre,
            clear_genre=clear_genre,
            bandcamp=bandcamp,
            clear_bandcamp=clear_bandcamp,
        )
        held = store.load()
        return ctx.envelope(
            data={
                "checks": _checks_for(held, _routed(label_id, route)),

```

New text:

```
            genre=genre,
            clear_genre=clear_genre,
            bandcamp=None,
            clear_bandcamp=clear_bandcamp,
        )
        held = store.load()
        return ctx.envelope(
            data={
                "checks": _checks_for(held, _routed(label_id, route)),

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

### `r777-confirm.N4_plain_name`

Confirm: _native_proof takes a pass name no landing could have been given, after the test that pins its message

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777-confirm.json`, row `N4_plain_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_pass_name_no_landing_could_have_been_given_is_refused`

Old text:

```
    if not landing.plain_name(name):
```

New text:

```
    if False:
```

### `r777-confirm.N7_digest_marks`

Confirm, the first table's old text was moved by the fix round: the native digest no longer covers the planned marks

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777-confirm.json`, row `N7_digest_marks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_native_answer_is_stale_once_another_playlist_becomes_whole`

Old text:

```
            "landings": list(proof.landings),
            "marks": planned,
```

New text:

```
            "landings": list(proof.landings),
```

### `r777.N10_screen_says_pass`

The gate screen on a native pass shows an intake file line instead of the pass

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777.json`, row `N10_screen_says_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_native_pass_whose_tracks_the_library_holds_is_marked_after_the_answer`

Old text:

```
        if isinstance(proof, marks.NativeLanding)
        else {"intake file": str(proof)}
```

New text:

```
        if False
        else {"intake file": str(proof)}
```

### `r777.N11_exclusive`

--xml and --pass are no longer one or the other

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777.json`, row `N11_exclusive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_the_file_and_the_pass_are_one_or_the_other`

Old text:

```
    proof = parser.add_mutually_exclusive_group(required=True)
```

New text:

```
    proof = parser
```

### `r777.N12_no_landing_required`

_native_proof makes a proof when no closed landing of the pass committed

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777.json`, row `N12_no_landing_required`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 141 against a baseline of 141
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_native_pass_no_closed_committed_landing_names_is_refused[abandoned]`
  - `tests/test_sync_mark.py::test_a_native_pass_no_closed_committed_landing_names_is_refused[another-pass]`
  - `tests/test_sync_mark.py::test_a_native_pass_no_closed_committed_landing_names_is_refused[never-committed]`
  - `tests/test_sync_mark.py::test_a_native_pass_no_closed_committed_landing_names_is_refused[no-landing]`

Old text:

```
    if not landings:
        raise _blocked(
```

New text:

```
    if False:
        raise _blocked(
```

### `r777.N18_unreachable_called_bridge`

An unreachable library falls through to the bridge refusal

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777.json`, row `N18_unreachable_called_bridge`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_an_unreachable_library_is_named_and_never_called_the_bridge`

Old text:

```
    if medium.declared is None:
        # AN UNREACHABLE ROOT
```

New text:

```
    if False:
        # AN UNREACHABLE ROOT
```

### `r777.N19_digest_landings`

The native digest no longer covers the landings that prove the pass

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777.json`, row `N19_digest_landings`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_second_landing_of_the_pass_since_the_plan_makes_the_answer_stale`

Old text:

```
            "landings": list(proof.landings),

```

New text:

```
(empty)
```

### `r777.N5_bridge_accepted`

_native_proof accepts --pass on an intake tree still on the xml bridge

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777.json`, row `N5_bridge_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 141 against a baseline of 141
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_pass_named_on_a_tree_still_on_the_bridge_is_refused_naming_the_file`
  - `tests/test_sync_mark.py::test_a_tree_put_back_on_the_bridge_after_the_plan_renames_nothing`

Old text:

```
    if not medium.native:
        raise _blocked(
```

New text:

```
    if False:
        raise _blocked(
```

### `r777.N6_no_reread`

apply_pass no longer reads the proof again before the first rename

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777.json`, row `N6_no_reread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 141 against a baseline of 141
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_landing_recorded_between_the_plan_and_the_apply_renames_nothing`
  - `tests/test_sync_mark.py::test_a_tree_put_back_on_the_bridge_after_the_plan_renames_nothing`

Old text:

```
        if _native_proof(cfg, planned.name) != planned.native:
```

New text:

```
        if False:
```

### `r777.N9_proof_is_file`

PassPlan.proof hands the engine the absent file on a native pass

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777.json`, row `N9_proof_is_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 141 against a baseline of 141
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_native_pass_takes_playlist_as_the_file_does`
  - `tests/test_sync_mark.py::test_a_native_pass_whose_tracks_the_library_holds_is_marked_after_the_answer`
  - `tests/test_sync_mark.py::test_a_native_pass_with_one_track_not_held_leaves_that_playlist_alone`
  - `tests/test_sync_mark.py::test_organize_marks_a_native_pass_through_its_gate`

Old text:

```
        return self.native if self.native is not None else self.xml
```

New text:

```
        return self.xml
```

### `r598-b.B1_sweep_before_the_lock`

release_lock: abandon the orphans before releasing the lock, so a live holder's refusal arrives after records were already ended

- File: `src/cratekit/session/cli.py`
- Source: `r598-b.json`, row `B1_sweep_before_the_lock`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_live_lock_holder_refuses_and_abandons_nothing`

Old text:

```
    cleared = session.release_stale_lock(cfg)
    abandoned = [
```

New text:

```
    abandoned_first = session.abandon_orphaned_sessions(cfg)
    cleared = session.release_stale_lock(cfg)
    abandoned = [record.session_id for record in abandoned_first] + [
```

### `r598-b.B3_orphans_not_shown`

release_lock: show an empty orphan list at the gate, so the person decides without seeing what will be ended

- File: `src/cratekit/session/cli.py`
- Source: `r598-b.json`, row `B3_orphans_not_shown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_hard_killed_gated_write_blocks_cutover_until_release_abandons_it`
  - `tests/test_session_cli.py::test_a_power_loss_blocks_cutover_until_release_abandons_it`

Old text:

```
                for record in orphans
            ],
```

New text:

```
                for record in orphans[:0]
            ],
```

### `r598-b.B4_abandon_only_reported_as_no_op`

release_lock: report a release that only abandoned records as a no-op, telling a person nothing changed

- File: `src/cratekit/session/cli.py`
- Source: `r598-b.json`, row `B4_abandon_only_reported_as_no_op`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_release_that_only_abandons_is_a_change_and_passes_the_contract`

Old text:

```
            outcome=Outcome.OK if abandoned else Outcome.NO_OP,
```

New text:

```
            outcome=Outcome.NO_OP,
```

### `r598-b.B5_kept_reports_nothing`

release_lock: report no kept records, hiding an open record the verb deliberately left

- File: `src/cratekit/session/cli.py`
- Source: `r598-b.json`, row `B5_kept_reports_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_record_from_another_boot_not_proven_this_machines_is_kept[another-machine-with-this-host-name]`
  - `tests/test_session_cli.py::test_a_record_from_another_boot_not_proven_this_machines_is_kept[recorded-before-the-machine-identity]`
  - `tests/test_session_cli.py::test_a_record_whose_holder_is_alive_is_kept_open`
  - `tests/test_session_cli.py::test_an_open_record_that_names_no_holder_is_never_abandoned`

Old text:

```
    kept = [record.session_id for record in session.records(cfg) if not record.terminal]
```

New text:

```
    kept = []
```

### `u49-author.A2_the_abort_mints_anyway`

Drop the abort branch in record_ack, so a person who declines gets an acknowledgment

- File: `src/cratekit/session/cli.py`
- Source: `u49-author.json`, row `A2_the_abort_mints_anyway`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_cli.py::test_an_inline_answer_cannot_overturn_a_recorded_abort`
  - `tests/test_session_cli.py::test_answering_abort_records_nothing_and_says_so`

Old text:

```
    if option == "abort":
        return ctx.envelope(
            data={"checks": [], "summary": {"recorded": False, "ages": shown}},
            outcome=Outcome.NO_OP,
        )

```

New text:

```
(empty)
```

### `u49-author.A3_the_refusal_names_no_ages`

Drop the context argument from the ack gate, so the refusal asks the question over nothing

- File: `src/cratekit/session/cli.py`
- Source: `u49-author.json`, row `A3_the_refusal_names_no_ages`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_damaged_acknowledgment_record_can_still_be_replaced`
  - `tests/test_session_cli.py::test_a_person_at_a_terminal_reads_the_ages_and_not_only_a_json_consumer`
  - `tests/test_session_cli.py::test_the_refusal_before_acknowledging_names_the_ages_it_consulted`
  - `tests/test_session_cli.py::test_the_refusal_names_the_acknowledgment_on_record_in_all_three_states`

Old text:

```
    option = ctx.gate.require(
        spec, context={"ages": shown, "acknowledgment": _on_record(cfg, now)}
    )
```

New text:

```
    option = ctx.gate.require(spec)
```

### `u49-author.A4_the_record_on_file_is_not_shown`

Show the ages but not the acknowledgment already on record, so a person cannot see whether they are covered

- File: `src/cratekit/session/cli.py`
- Source: `u49-author.json`, row `A4_the_record_on_file_is_not_shown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_damaged_acknowledgment_record_can_still_be_replaced`
  - `tests/test_session_cli.py::test_the_refusal_names_the_acknowledgment_on_record_in_all_three_states`

Old text:

```
        spec, context={"ages": shown, "acknowledgment": _on_record(cfg, now)}
```

New text:

```
        spec, context={"ages": shown}
```

### `u49-author.A6_the_authorisation_is_not_spent`

Leave the recorded decision in place after the mint, so one run id re-mints the acknowledgment forever (R-217's defect restored)

- File: `src/cratekit/session/cli.py`
- Source: `u49-author.json`, row `A6_the_authorisation_is_not_spent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_spent_acknowledgment_decision_cannot_be_replayed`

Old text:

```
    ctx.run.decisions.pop(spec.name, None)
```

New text:

```
(empty)
```

### `u49-author.A7_the_check_rows_are_keyed_wrong`

Key the ack check rows by name rather than key, so the human check table prints a question mark where the portion should be

- File: `src/cratekit/session/cli.py`
- Source: `u49-author.json`, row `A7_the_check_rows_are_keyed_wrong`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_cli.py::test_the_check_rows_a_person_reads_name_the_portion`

Old text:

```
                    "key": f"backup.age.{entry['portion']}",
```

New text:

```
                    "name": f"backup.age.{entry['portion']}",
```

### `u49-author.A8_a_damaged_record_locks_the_verb_out`

Let the display read of the acknowledgment raise, so a corrupt record makes the one verb that replaces it refuse

- File: `src/cratekit/session/cli.py`
- Source: `u49-author.json`, row `A8_a_damaged_record_locks_the_verb_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_damaged_acknowledgment_record_can_still_be_replaced`

Old text:

```
    try:
        recorded = session.read_acknowledgment(cfg)
    except CratekitError as exc:
        return {"unreadable": exc.cause.message}
```

New text:

```
    recorded = session.read_acknowledgment(cfg)
```

### `u49-author.R1_hard_code_the_repair_token`

Name repair-backup-facts over every unreadable condition, which is R-201's defect reproduced on the new consumer

- File: `src/cratekit/session/cli.py`
- Source: `u49-author.json`, row `R1_hard_code_the_repair_token`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_cli.py::test_an_unreadable_fact_file_refuses_and_the_remedy_the_raiser_chose_travels[newer-upgrade-cratekit]`

Old text:

```
            remedy=Remedy(str(exc.remedy)),
            origin=("session", "cli"),
            detail={"path": str(exc.path), "library": str(cfg.library.root)},
```

New text:

```
            remedy=Remedy.REPAIR_BACKUP_FACTS,
            origin=("session", "cli"),
            detail={"path": str(exc.path), "library": str(cfg.library.root)},
```

### `u49-author.R2_hard_code_the_permission_token`

The same defect mirrored: name grant-path-access over every condition. Both directions are driven because a carry measured one way leaves the other unasserted

- File: `src/cratekit/session/cli.py`
- Source: `u49-author.json`, row `R2_hard_code_the_permission_token`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_cli.py::test_an_unreadable_fact_file_refuses_and_the_remedy_the_raiser_chose_travels[corrupt-repair-backup-facts]`
  - `tests/test_session_cli.py::test_an_unreadable_fact_file_refuses_and_the_remedy_the_raiser_chose_travels[newer-upgrade-cratekit]`

Old text:

```
            remedy=Remedy(str(exc.remedy)),
            origin=("session", "cli"),
            detail={"path": str(exc.path), "library": str(cfg.library.root)},
```

New text:

```
            remedy=Remedy.GRANT_PATH_ACCESS,
            origin=("session", "cli"),
            detail={"path": str(exc.path), "library": str(cfg.library.root)},
```

### `u49-author.R3_an_unreadable_file_reads_as_empty`

Swallow BackupFactsUnreadable and show no ages, collapsing could-not-read into never-backed-up

- File: `src/cratekit/session/cli.py`
- Source: `u49-author.json`, row `R3_an_unreadable_file_reads_as_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_cli.py::test_an_unreadable_fact_file_refuses_and_the_remedy_the_raiser_chose_travels[corrupt-repair-backup-facts]`
  - `tests/test_session_cli.py::test_an_unreadable_fact_file_refuses_and_the_remedy_the_raiser_chose_travels[newer-upgrade-cratekit]`

Old text:

```
    except backup_facts.BackupFactsUnreadable as exc:
        raise refuse(
```

New text:

```
    except backup_facts.BackupFactsUnreadable:
        return []
    except NotImplementedError as exc:
        raise refuse(
```

### `u236.M13_write_records_no_month`

write: record no month placement, so settle records none

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u236.json`, row `M13_write_records_no_month`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 233 against a baseline of 233
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_put_in_another_month_on_the_account_leaves_the_placed_month`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_taken_off_again_before_another_organize_is_unfavourited`
  - `tests/test_organize_mirror_edits_u236.py::test_a_month_whose_listing_fails_at_the_unfavourite_still_reads_its_placement`
  - `tests/test_organize_mirror_edits_u236.py::test_a_placement_the_account_refused_to_take_still_lets_the_unfavourite_through`
  - `tests/test_organize_mirror_edits_u236.py::test_the_placements_are_read_as_the_gate_read_them_after_a_write_between_the_acts`
  - `tests/test_organize_mirror_edits_u236.py::test_the_same_when_the_write_made_the_month`

Old text:

```
        if at:
            done.months.append((one.content_id, one.month, at))
```

New text:

```
        if False:
            done.months.append((one.content_id, one.month, at))
```

### `u236.M14_write_wrong_time`

write: record a time no membership carries

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u236.json`, row `M14_write_wrong_time`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 233 against a baseline of 233
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_put_in_another_month_on_the_account_leaves_the_placed_month`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_taken_off_again_before_another_organize_is_unfavourited`
  - `tests/test_organize_mirror_edits_u236.py::test_a_month_whose_listing_fails_at_the_unfavourite_still_reads_its_placement`
  - `tests/test_organize_mirror_edits_u236.py::test_a_placement_the_account_refused_to_take_still_lets_the_unfavourite_through`
  - `tests/test_organize_mirror_edits_u236.py::test_the_placements_are_read_as_the_gate_read_them_after_a_write_between_the_acts`
  - `tests/test_organize_mirror_edits_u236.py::test_the_same_when_the_write_made_the_month`

Old text:

```
            done.months.append((one.content_id, one.month, at))
```

New text:

```
            done.months.append((one.content_id, one.month, at + "x"))
```

### `u236.M15_settle_month_title`

settle: record the placement under the month's bare name, not its account title

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u236.json`, row `M15_settle_month_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 233 against a baseline of 233
- Kills: 8 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_put_in_another_month_on_the_account_leaves_the_placed_month`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_taken_off_again_before_another_organize_is_unfavourited`
  - `tests/test_organize_mirror_edits_u236.py::test_a_hand_addition_after_the_placement_is_dropped_is_read_as_one`
  - `tests/test_organize_mirror_edits_u236.py::test_a_month_whose_listing_fails_at_the_unfavourite_still_reads_its_placement`
  - `tests/test_organize_mirror_edits_u236.py::test_a_placement_the_account_refused_to_take_still_lets_the_unfavourite_through`
  - `tests/test_organize_mirror_edits_u236.py::test_the_organize_after_the_favourite_puts_it_in_the_accounts_month`
  - `tests/test_organize_mirror_edits_u236.py::test_the_placements_are_read_as_the_gate_read_them_after_a_write_between_the_acts`
  - `tests/test_organize_mirror_edits_u236.py::test_the_same_when_the_write_made_the_month`

Old text:

```
                mirror.title(decision.to.folder, month_of[decision.content_id][0]),
```

New text:

```
                month_of[decision.content_id][0],
```

### `u236.M16_settle_any_favourite`

settle: record a placement for a favourite put in a month on the account too

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u236.json`, row `M16_settle_any_favourite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 233 against a baseline of 233
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_put_in_another_month_on_the_account_leaves_the_placed_month`

Old text:

```
            and decision.to.primary
            and month_of.get(decision.content_id)
```

New text:

```
            and month_of.get(decision.content_id)
```

### `u236.M17_ledger_settle_keeps_placement`

ledger settle: a settled track keeps its placement on that title

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u236.json`, row `M17_ledger_settle_keeps_placement`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 233 against a baseline of 233
- Kills: 4 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_the_ledger_keeps_a_placement_until_the_mirror_finished_its_playlist`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_put_in_another_month_on_the_account_leaves_the_placed_month`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_taken_off_again_before_another_organize_is_unfavourited`
  - `tests/test_organize_mirror_edits_u236.py::test_the_placements_are_read_as_the_gate_read_them_after_a_write_between_the_acts`

Old text:

```
                if str(track) in before:
                    _place(record, name, {one: at for one, at in before.items() if one != str(track)})
                    wrote = True
```

New text:

```
                if False:
                    _place(record, name, {one: at for one, at in before.items() if one != str(track)})
                    wrote = True
```

### `u236.M18_ledger_placement_not_written`

ledger settle: never write a placement

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u236.json`, row `M18_ledger_placement_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 233 against a baseline of 233
- Kills: 8 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_a_placement_survives_the_ledgers_own_read_and_write`
  - `tests/test_mirror_edits_u236.py::test_the_ledger_keeps_a_placement_until_the_mirror_finished_its_playlist`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_put_in_another_month_on_the_account_leaves_the_placed_month`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_taken_off_again_before_another_organize_is_unfavourited`
  - `tests/test_organize_mirror_edits_u236.py::test_a_month_whose_listing_fails_at_the_unfavourite_still_reads_its_placement`
  - `tests/test_organize_mirror_edits_u236.py::test_a_placement_the_account_refused_to_take_still_lets_the_unfavourite_through`
  - `tests/test_organize_mirror_edits_u236.py::test_the_placements_are_read_as_the_gate_read_them_after_a_write_between_the_acts`
  - `tests/test_organize_mirror_edits_u236.py::test_the_same_when_the_write_made_the_month`

Old text:

```
            _place(
                record,
                name,
                {**_placements(record.get("placed")).get(str(name), {}), str(track): str(at)},
            )
            wrote = True
```

New text:

```
            wrote = True
```

### `u236.M19_ledger_normalizer_drops`

ledger load: drop every folder's placements on read and write

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u236.json`, row `M19_ledger_normalizer_drops`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 233 against a baseline of 233
- Kills: 8 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_a_placement_survives_the_ledgers_own_read_and_write`
  - `tests/test_mirror_edits_u236.py::test_the_ledger_keeps_a_placement_until_the_mirror_finished_its_playlist`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_put_in_another_month_on_the_account_leaves_the_placed_month`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_taken_off_again_before_another_organize_is_unfavourited`
  - `tests/test_organize_mirror_edits_u236.py::test_a_month_whose_listing_fails_at_the_unfavourite_still_reads_its_placement`
  - `tests/test_organize_mirror_edits_u236.py::test_a_placement_the_account_refused_to_take_still_lets_the_unfavourite_through`
  - `tests/test_organize_mirror_edits_u236.py::test_the_placements_are_read_as_the_gate_read_them_after_a_write_between_the_acts`
  - `tests/test_organize_mirror_edits_u236.py::test_the_same_when_the_write_made_the_month`

Old text:

```
                    {"placed": placed}
                    if (placed := _placements(value.get("placed")))
                    else {}
```

New text:

```
                    {}
```

### `u236.M20_agreed_never_drops`

record_mirror_agreed: never drop a placement the account now holds

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u236.json`, row `M20_agreed_never_drops`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 233 against a baseline of 233
- Kills: 3 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_the_ledger_keeps_a_placement_until_the_mirror_finished_its_playlist`
  - `tests/test_organize_mirror_edits_u236.py::test_a_hand_addition_after_the_placement_is_dropped_is_read_as_one`
  - `tests/test_organize_mirror_edits_u236.py::test_the_organize_after_the_favourite_puts_it_in_the_accounts_month`

Old text:

```
                mirror_edits.placed_after(
                    _placements(document["mirrors"][folder].get("placed")).get(name, {}),
                    after,
                    held,
                ),
```

New text:

```
                _placements(document["mirrors"][folder].get("placed")).get(name, {}),
```

### `r796-c.V1_the_worker_hands_the_seam_over`

handle: stop passing the general catalogue's seam to tag_one, so the verb never asks it

- File: `src/cratekit/tagging/cli.py`
- Source: `r796-c.json`, row `V1_the_worker_hands_the_seam_over`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 381 against a baseline of 381
- Kills: 10 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`
  - `tests/test_tag_workers.py::test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_some_files_says_how_many_of_how_many`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`
  - `tests/test_tag_workers.py::test_a_published_genre_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_a_published_word_with_no_folder_is_listed_as_unresolved`
  - `tests/test_tag_workers.py::test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit`
  - `tests/test_tag_workers.py::test_files_with_no_isrc_are_counted_and_warned_about_whatever_their_skip_reason`
  - `tests/test_tag_workers.py::test_four_real_misses_are_no_hit_and_carry_no_unread_warning`

Old text:

```
        published=published.for_taxonomy(declared),
```

New text:

```
        published=None,
```

### `r796-c.V2_blocked_warning_is_the_shops_only`

_unread_warnings: name every source blocked throughout, the general catalogue included, so one refusal is said under two codes

- File: `src/cratekit/tagging/cli.py`
- Source: `r796-c.json`, row `V2_blocked_warning_is_the_shops_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 381 against a baseline of 381
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`

Old text:

```
    for source in searchers.SOURCES:
        counted = answers.get(source) or {}
```

New text:

```
    for source in answers:
        counted = answers.get(source) or {}
```

### `r796-c.V3_some_unread_is_said`

_published_warnings: warn only when the catalogue was unread on every file asked about, so a partial block is counts and no sentence

- File: `src/cratekit/tagging/cli.py`
- Source: `r796-c.json`, row `V3_some_unread_is_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 381 against a baseline of 381
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_some_files_says_how_many_of_how_many`

Old text:

```
    if failed:
        seen = "; ".join(f"{word} on {count}" for word, count in unread.items() if count)
```

New text:

```
    if failed and failed == asked:
        seen = "; ".join(f"{word} on {count}" for word, count in unread.items() if count)
```

### `r796-c.V4_no_isrc_is_warned_about`

_published_warnings: never warn about files with no ISRC

- File: `src/cratekit/tagging/cli.py`
- Source: `r796-c.json`, row `V4_no_isrc_is_warned_about`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 381 against a baseline of 381
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_files_with_no_isrc_are_counted_and_warned_about_whatever_their_skip_reason`

Old text:

```
    if bare:
```

New text:

```
    if False:
```

### `r796-c.V5_parse_break_sentence_said_once`

_unread_warnings: read the general catalogue's parse break into the shops' sentence too

- File: `src/cratekit/tagging/cli.py`
- Source: `r796-c.json`, row `V5_parse_break_sentence_said_once`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 381 against a baseline of 381
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`

Old text:

```
            for source in searchers.SOURCES
        )
```

New text:

```
            for source in answers
        )
```

### `r796-b.O9_no_isrc_is_not_no_hit`

tag_one: drop the no-isrc skip reason, so a file the general catalogue could not be asked about is no-hit (AE4)

- File: `src/cratekit/tagging/tag.py`
- Source: `r796-b.json`, row `O9_no_isrc_is_not_no_hit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 381 against a baseline of 381
- Kills: 3 (killed)
- Killed:
  - `tests/test_published_genre.py::test_a_malformed_isrc_tag_is_reported_with_what_it_held`
  - `tests/test_published_genre.py::test_ae4_a_file_with_no_isrc_is_reported_as_that_and_not_as_no_hit`
  - `tests/test_tag_workers.py::test_files_with_no_isrc_are_counted_and_warned_about_whatever_their_skip_reason`

Old text:

```
        elif any(said.answer == NO_ISRC for said in hit.answers):
```

New text:

```
        elif False:
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

### `r1255.S1_scan_unlisted_as_empty`

scan_log: answer a log it is refused as no record and none unread, the defect itself

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S1_scan_unlisted_as_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_unmirrored.py`, `tests/test_intake_shelve.py`, `tests/test_tree_registry.py`, `tests/test_doctor.py`, `tests/test_restore.py`, `tests/test_write_session.py`
- Collected: 891 against a baseline of 891
- Kills: 16 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_session_log_this_account_cannot_list_is_failed_by_its_own_check`
  - `tests/test_doctor.py::test_status_names_a_session_log_it_cannot_list_and_still_reports_the_rest`
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`
  - `tests/test_session_log_unlisted.py::test_a_log_path_that_is_a_file_is_there_and_unread`
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
  - ... and 1 more, see the JSON sidecar

Old text:

```
        logger.debug("session log %s could not be listed: %s", directory, exc)
        return (), (directory,)
```

New text:

```
        logger.debug("session log %s could not be listed: %s", directory, exc)
        return (), ()
```

### `r1255.S2_absent_log_unread`

_listed: read a log that is not there as refused, so a library with no session refuses every write

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S2_absent_log_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_unmirrored.py`, `tests/test_intake_shelve.py`, `tests/test_tree_registry.py`, `tests/test_doctor.py`, `tests/test_restore.py`, `tests/test_write_session.py`
- Collected: 891 against a baseline of 891
- Kills: 63 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_green_doctor_exits_zero`
  - `tests/test_doctor.py::test_a_headless_machine_that_opted_into_the_environment_fallback_is_not_red`
  - `tests/test_doctor.py::test_a_library_with_no_sessions_still_reports_a_clean_log`
  - `tests/test_doctor.py::test_a_re_run_repairs_a_spelled_remote_rclone_does_not_know`
  - `tests/test_doctor.py::test_a_second_setup_run_asks_nothing_and_changes_nothing_it_was_not_asked_to`
  - `tests/test_doctor.py::test_an_empty_credential_leaves_the_exit_code_to_doctor`
  - `tests/test_doctor.py::test_no_ok_detail_claims_a_volume_the_run_never_identified`
  - `tests/test_doctor.py::test_the_backup_flags_are_recorded_without_a_question`
  - `tests/test_doctor.py::test_the_disagreeing_remote_refusal_names_the_flag_and_the_flag_repairs_it`
  - `tests/test_doctor.py::test_the_strong_claim_survives_where_the_identity_really_was_compared`
  - `tests/test_doctor.py::test_the_wizard_on_a_clean_machine_produces_a_valid_config_and_a_green_doctor`
  - `tests/test_inbox_unmirrored.py::test_a_dated_playlist_with_no_batch_folder_still_says_so`
  - `tests/test_inbox_unmirrored.py::test_an_absent_session_log_is_no_record_at_all`
  - `tests/test_inbox_unmirrored.py::test_the_live_batches_name_every_other_node_under_inbox_with_its_kind`
  - `tests/test_intake_shelve.py::test_a_batch_named_twice_is_planned_once`
  - ... and 48 more, see the JSON sidecar

Old text:

```
        return os.listdir(directory)
    except FileNotFoundError:
        return None
```

New text:

```
        return os.listdir(directory)
    except FileNotFoundError:
        raise
```

### `r1255.S5_json_filter`

scan_log: read every name in the log as a record, so a stray file reads as an unreadable record

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S5_json_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_unmirrored.py`, `tests/test_intake_shelve.py`, `tests/test_tree_registry.py`, `tests/test_doctor.py`, `tests/test_restore.py`, `tests/test_write_session.py`
- Collected: 891 against a baseline of 891
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_a_listed_log_is_read_and_names_nothing_unlisted`

Old text:

```
    entries = sorted(directory / name for name in names if fnmatch.fnmatchcase(name, "*.json"))
```

New text:

```
    entries = sorted(directory / name for name in names)
```

### `r185-r246-author.E1_plan_gate_by_position`

Index gates[0] instead of searching by digest source, the guard the repaired case in test_genre_retag.py measures

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r185-r246-author.json`, row `E1_plan_gate_by_position`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_the_handler_finds_its_gate_by_digest_source_and_not_by_position`

Old text:

```
    for spec in ctx.entry.gates:
        if spec.digest_source == PLAN:
            return spec
```

New text:

```
    for spec in ctx.entry.gates[:1]:
        return spec
```

### `r185-r246-author.E3_empty_plan_queues_anyway`

Queue a job over an empty selection, which core.jobs drives straight to SUCCEEDED over a folder nothing touched

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r185-r246-author.json`, row `E3_empty_plan_queues_anyway`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_folder_that_is_not_there_is_a_different_zero_from_one_with_nothing_coarse`
  - `tests/test_tag_workers.py::test_an_empty_plan_is_still_asked_about_and_still_queues_nothing`

Old text:

```
    if not plan["items"]:
        payload, warnings = (
```

New text:

```
    if False:
        payload, warnings = (
```

### `r185-r246-author.M1_folder_dropped`

Drop the folder from the instruction, so a person reading one envelope beside others cannot tell which sweep it names

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r185-r246-author.json`, row `M1_folder_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 5 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_corrected_retag_ends_by_naming_the_reload_the_stale_row_needs`
  - `tests/test_tag_workers.py::test_a_half_corrected_retag_carries_the_reload_on_its_refusal`
  - `tests/test_tag_workers.py::test_a_parked_retag_keeps_both_the_block_and_the_reload`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`
  - `tests/test_tag_workers.py::test_the_queueing_envelope_names_the_reload_before_the_person_walks_away`

Old text:

```
            f"this correction writes the genre onto the files under {folder} and "
            f"does not update the library rows, which go on carrying the old "
```

New text:

```
            f"this correction writes the genre onto the files it selected and "
            f"does not update the library rows, which go on carrying the old "
```

### `r185-r246-author.W1_queue_warning_dropped`

The queueing envelope stops naming the reload, so the person walks away told nothing

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r185-r246-author.json`, row `W1_queue_warning_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_queueing_envelope_names_the_reload_before_the_person_walks_away`

Old text:

```
            warnings=(library_row_warning(folder),),

```

New text:

```
(empty)
```

### `r185-r246-author.W2_resume_warning_dropped`

A successful resume stops naming the reload

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r185-r246-author.json`, row `W2_resume_warning_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_corrected_retag_ends_by_naming_the_reload_the_stale_row_needs`

Old text:

```
        if summary["corrected"]:
            warnings = (*warnings, library_row_warning(folder))

```

New text:

```
(empty)
```

### `r185-r246-author.W3_resume_warning_unconditional`

Name the reload on every resume, including one that corrected nothing and made no row stale

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r185-r246-author.json`, row `W3_resume_warning_unconditional`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_retag_that_corrected_nothing_does_not_send_a_person_to_rekordbox`

Old text:

```
        if summary["corrected"]:
            warnings = (*warnings, library_row_warning(folder))
```

New text:

```
        warnings = (*warnings, library_row_warning(folder))
```

### `r185-r246-author.W4_refusal_step_dropped`

A half corrected sweep leaves through its cause with nothing said about the rows it made stale

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r185-r246-author.json`, row `W4_refusal_step_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_half_corrected_retag_carries_the_reload_on_its_refusal`
  - `tests/test_tag_workers.py::test_a_parked_retag_keeps_both_the_block_and_the_reload`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`

Old text:

```
        try:
            job, warnings = shell.advance(
                ctx,
                store,
                queued,
                origin=("tagging", "retag_cli"),
                nothing_to_run="report a correction over files it never looked at",
            )
        except CratekitError as failed:
            # THE REFUSAL CARRIES THE RELOAD WHEN ANYTHING WAS CORRECTED. The
            # artifacts are committed per item before the failure, so this
            # counts what actually landed rather than what was confirmed, and a
            # sweep that refused on its first item adds nothing to a refusal it
            # has no reload to name. See ``with_reload_step``.
            if not _summary(cfg, ctx.args.job)["corrected"]:
                raise
            raise with_reload_step(failed, folder) from failed
```

New text:

```
        job, warnings = shell.advance(
            ctx,
            store,
            queued,
            origin=("tagging", "retag_cli"),
            nothing_to_run="report a correction over files it never looked at",
        )
```

### `r185-r246-author.W5_refusal_step_unconditional`

Append the reload to every refusal, including one that corrected nothing

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r185-r246-author.json`, row `W5_refusal_step_unconditional`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_retag_that_failed_before_correcting_anything_names_no_reload`
  - `tests/test_tag_workers.py::test_a_retag_whose_only_file_will_not_take_its_genre_names_no_reload`

Old text:

```
            if not _summary(cfg, ctx.args.job)["corrected"]:
                raise
            raise with_reload_step(failed, folder) from failed
```

New text:

```
            raise with_reload_step(failed, folder) from failed
```

### `r185-r246-author.W6_refusal_counts_the_plan`

Count the confirmed items instead of the committed artifacts, so a sweep that wrote nothing still reports a correction

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r185-r246-author.json`, row `W6_refusal_counts_the_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_retag_that_failed_before_correcting_anything_names_no_reload`
  - `tests/test_tag_workers.py::test_a_retag_whose_only_file_will_not_take_its_genre_names_no_reload`

Old text:

```
            if not _summary(cfg, ctx.args.job)["corrected"]:
                raise
```

New text:

```
            if not payload.get(ITEMS_KEY):
                raise
```

### `u288.M10_changed_rows`

collection_removal_violations: read a changed row as unchanged

- File: `src/cratekit/core/rb_writer.py`
- Source: `u288.json`, row `M10_changed_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 264 against a baseline of 264
- Kills: 4 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_confined_removal_reads_clean_and_every_stray_difference_is_named`
  - `tests/test_rb_writer_guard.py::test_the_read_back_after_the_commit_admits_only_the_counter_moving_forward`
  - `tests/test_sync_removed.py::test_a_removal_that_changes_anything_it_did_not_plan_is_refused_before_its_commit`
  - `tests/test_sync_removed.py::test_commit_proves_the_removal_confined_before_it_commits`

Old text:

```
            if old[key] == new[key]:
                continue
```

New text:

```
            if True:
                continue
```

### `u288.M11_added_rows`

collection_removal_violations: read an added row as nothing

- File: `src/cratekit/core/rb_writer.py`
- Source: `u288.json`, row `M11_added_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 264 against a baseline of 264
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_confined_removal_reads_clean_and_every_stray_difference_is_named`
  - `tests/test_rb_writer_guard.py::test_the_read_back_after_the_commit_admits_only_the_counter_moving_forward`

Old text:

```
        for key in sorted(set(new) - set(old)):
            violations.append(f"an unplanned {table} row {key!r} was added")
```

New text:

```
        for key in sorted(set(new) - set(old)):
            pass
```

### `u288.M12_still_names`

collection_removal_violations: drop the check that every row naming a removed track is gone

- File: `src/cratekit/core/rb_writer.py`
- Source: `u288.json`, row `M12_still_names`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 264 against a baseline of 264
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_planned_removal_that_was_not_made_is_refused`
  - `tests/test_sync_removed.py::test_a_removal_that_changes_anything_it_did_not_plan_is_refused_before_its_commit`

Old text:

```
            if names in gone and key in new:
```

New text:

```
            if False:
```

### `u288.M13_counter_forward`

collection_removal_violations: accept a read back whose update count did not move

- File: `src/cratekit/core/rb_writer.py`
- Source: `u288.json`, row `M13_counter_forward`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 264 against a baseline of 264
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_the_read_back_after_the_commit_admits_only_the_counter_moving_forward`

Old text:

```
        before.counter is None or after.counter is None or after.counter <= before.counter
```

New text:

```
        before.counter is None or after.counter is None or after.counter < before.counter
```

### `u288.M1_delete_admitted_by_any_name`

guard_violations: admit a delete in any table once any table is named, not only the named one

- File: `src/cratekit/core/rb_writer.py`
- Source: `u288.json`, row `M1_delete_admitted_by_any_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 264 against a baseline of 264
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_delete_is_admitted_only_in_a_table_the_commit_names`
  - `tests/test_sync_removed.py::test_another_writer_deleting_a_content_row_through_the_binding_is_refused_at_its_commit`

Old text:

```
        if table in deletable:
            continue
```

New text:

```
        if deletable:
            continue
```

### `u288.M2_deletable_set_unbounded`

guard_violations: stop holding the named tables to DELETABLE_TABLES, so a commit can ask to delete anywhere

- File: `src/cratekit/core/rb_writer.py`
- Source: `u288.json`, row `M2_deletable_set_unbounded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 264 against a baseline of 264
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_delete_outside_the_removal_set_is_refused_even_when_asked_for`

Old text:

```
    deletable &= DELETABLE_TABLES
```

New text:

```
    deletable = deletable
```

### `u288.M9_whose_row_disappeared`

collection_removal_violations: let any row of any table disappear

- File: `src/cratekit/core/rb_writer.py`
- Source: `u288.json`, row `M9_whose_row_disappeared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 264 against a baseline of 264
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_confined_removal_reads_clean_and_every_stray_difference_is_named`

Old text:

```
            if table not in DELETABLE_TABLES or naming.get(key) not in gone:
```

New text:

```
            if False:
```

### `r1017.M12_twin_message_names_to`

Refusal: name the held playlist under the new name rather than the name it is recorded under

- File: `src/cratekit/export/set_cli.py`
- Source: `r1017.json`, row `M12_twin_message_names_to`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_sync_mark.py`
- Collected: 195 against a baseline of 195
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_the_frozen_name_ranks_ahead_of_the_landing_record`

Old text:

```
            f"{planned.playlist.remote_id} under {planned.playlist.name!r} and "
```

New text:

```
            f"{planned.playlist.remote_id} under {to!r} and "
```

### `r1017.M1_no_recorded_names`

Rename: drop the names the landings recorded from the names looked up, the defect R-1017 names

- File: `src/cratekit/export/set_cli.py`
- Source: `r1017.json`, row `M1_no_recorded_names`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_sync_mark.py`
- Collected: 195 against a baseline of 195
- Kills: 5 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_job_whose_page_words_differ_renames_by_the_name_its_landing_recorded`
  - `tests/test_export_set_rename.py::test_a_twin_under_the_new_name_still_refuses_when_the_landing_names_the_old`
  - `tests/test_export_set_rename.py::test_the_backfill_plans_no_twin_after_a_rename_by_the_landing_record`
  - `tests/test_export_set_rename.py::test_the_frozen_name_ranks_ahead_of_the_landing_record`
  - `tests/test_export_set_rename.py::test_two_playlists_under_two_older_names_are_a_twin_not_a_choice`

Old text:

```
    recorded = tuple(set_name(one) for one in set_playlist.recorded_names(cfg, job.job_id))
```

New text:

```
    recorded = ()
```

### `r1017.M2_recorded_before_frozen`

Rename: rank the landing names ahead of the frozen name an earlier rename chose

- File: `src/cratekit/export/set_cli.py`
- Source: `r1017.json`, row `M2_recorded_before_frozen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_sync_mark.py`
- Collected: 195 against a baseline of 195
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_the_frozen_name_ranks_ahead_of_the_landing_record`

Old text:

```
            for one in (set_name(frozen) if frozen else "", *recorded, *_names_for_job(job))
```

New text:

```
            for one in (*recorded, set_name(frozen) if frozen else "", *_names_for_job(job))
```

### `r1017.M3_landing_open_read`

Landing records: read a record that never closed as a landing

- File: `src/cratekit/intake/set_playlist.py`
- Source: `r1017.json`, row `M3_landing_open_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_sync_mark.py`
- Collected: 195 against a baseline of 195
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_job_with_no_landing_record_and_no_matching_name_still_refuses[open]`

Old text:

```
        if record.state is session.SessionState.CLOSED
        and str(session.SourceState.COMMITTED) in record.sources.values()
        and isinstance(record.detail.get(RECORD_KEY), Mapping)
        and record.detail[RECORD_KEY].get("job") == job_id
    ]
    return tuple(
```

New text:

```
        if record.state is not None
        and str(session.SourceState.COMMITTED) in record.sources.values()
        and isinstance(record.detail.get(RECORD_KEY), Mapping)
        and record.detail[RECORD_KEY].get("job") == job_id
    ]
    return tuple(
```

### `r1017.M4_landing_uncommitted_read`

Landing records: read a record whose source never committed as a landing

- File: `src/cratekit/intake/set_playlist.py`
- Source: `r1017.json`, row `M4_landing_uncommitted_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_sync_mark.py`
- Collected: 195 against a baseline of 195
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_job_with_no_landing_record_and_no_matching_name_still_refuses[uncommitted]`

Old text:

```
        and str(session.SourceState.COMMITTED) in record.sources.values()
        and isinstance(record.detail.get(RECORD_KEY), Mapping)
        and record.detail[RECORD_KEY].get("job") == job_id
    ]
    return tuple(
```

New text:

```
        and record.sources
        and isinstance(record.detail.get(RECORD_KEY), Mapping)
        and record.detail[RECORD_KEY].get("job") == job_id
    ]
    return tuple(
```

### `r1017.M5_landing_any_job`

Landing records: read another job's landing as this job's

- File: `src/cratekit/intake/set_playlist.py`
- Source: `r1017.json`, row `M5_landing_any_job`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_sync_mark.py`
- Collected: 195 against a baseline of 195
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_job_with_no_landing_record_and_no_matching_name_still_refuses[another job]`
  - `tests/test_export_set_rename.py::test_recorded_names_reads_every_landing_of_the_job_the_newest_first`

Old text:

```
        and record.detail[RECORD_KEY].get("job") == job_id
    ]
    return tuple(
```

New text:

```
        and record.detail[RECORD_KEY].get("job") is not None
    ]
    return tuple(
```

### `r1017.M6_oldest_first`

Landing records: read them oldest first, which recorded_playlist also depends on

- File: `src/cratekit/intake/set_playlist.py`
- Source: `r1017.json`, row `M6_oldest_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_sync_mark.py`
- Collected: 195 against a baseline of 195
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_recorded_names_reads_every_landing_of_the_job_the_newest_first`

Old text:

```
        for record in sorted(found, key=lambda one: one.session_id, reverse=True)
```

New text:

```
        for record in sorted(found, key=lambda one: one.session_id, reverse=False)
```

### `r1017.M7_names_not_deduplicated`

recorded_names: return a name twice when two landings recorded it

- File: `src/cratekit/intake/set_playlist.py`
- Source: `r1017.json`, row `M7_names_not_deduplicated`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_sync_mark.py`
- Collected: 195 against a baseline of 195
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_recorded_names_reads_every_landing_of_the_job_the_newest_first`

Old text:

```
        dict.fromkeys(name for kept in _landed(cfg, job_id) if (name := str(kept.get("name") or "")))
```

New text:

```
        list(name for kept in _landed(cfg, job_id) if (name := str(kept.get("name") or "")))
```

### `r740-a.N1_no_fill`

normalize_spec: never fill a spec field from the stripped head, the R-740 loss itself

- File: `src/cratekit/core/naming.py`
- Source: `r740-a.json`, row `N1_no_fill`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming.py`, `tests/test_landing_head.py`, `tests/test_landing.py`, `tests/intake/test_pipeline.py`
- Collected: 253 against a baseline of 253
- Kills: 17 (killed)
- Killed:
  - `tests/test_landing_head.py::test_a_file_headed_in_its_filename_only_carries_that_head`
  - `tests/test_landing_head.py::test_a_filename_head_wins_over_a_disagreeing_key_tag`
  - `tests/test_landing_head.py::test_a_lossy_file_keeps_its_marker_on_all_three_surfaces`
  - `tests/test_landing_head.py::test_a_second_landing_of_the_same_file_renders_the_same_name`
  - `tests/test_landing_head.py::test_a_title_head_with_no_key_tag_still_lands_whole`
  - `tests/test_landing_head.py::test_a_title_headed_file_with_no_tempo_elsewhere_lands_named_as_its_title`
  - `tests/test_landing_head.py::test_an_off_wheel_key_tag_under_a_headed_title_lands_the_head`
  - `tests/test_landing_head.py::test_intake_file_names_its_track_from_the_same_head`
  - `tests/test_landing_head.py::test_the_lossy_flag_reported_is_the_one_the_name_was_rendered_from`
  - `tests/test_landing_head.py::test_the_title_head_wins_over_a_disagreeing_key_tag`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_disagreeing_title_head_leaves_the_stem_head_to_agree`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_key_only_spec_over_a_headed_title_keeps_the_whole_head`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_marker_in_the_stripped_head_marks_the_spec`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_spec_with_no_fields_takes_both_from_the_head`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_an_unpadded_or_lowercase_key_agrees_with_its_padded_head`
  - ... and 2 more, see the JSON sidecar

Old text:

```
            filled.update(
                (name, value) for name, value in values.items() if current[name] is None
            )
```

New text:

```
            pass
```

### `r740-a.N2_no_agreement`

normalize_spec: fill from the head whatever the spec supplied, so a fresh key takes the old tempo

- File: `src/cratekit/core/naming.py`
- Source: `r740-a.json`, row `N2_no_agreement`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming.py`, `tests/test_landing_head.py`, `tests/test_landing.py`, `tests/intake/test_pipeline.py`
- Collected: 253 against a baseline of 253
- Kills: 3 (killed)
- Killed:
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_disagreeing_title_head_leaves_the_stem_head_to_agree`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_fresh_key_is_never_paired_with_the_tempo_it_replaces`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_an_off_wheel_key_is_not_completed_into_a_refused_shape`

Old text:

```
        if all(_agrees(name, current[name], values[name]) for name in values):
```

New text:

```
        if True:
```

### `r740-a.N3_key_compared_raw`

_agrees: compare the key as raw text instead of on the wheel, so 8a disagrees with 08A

- File: `src/cratekit/core/naming.py`
- Source: `r740-a.json`, row `N3_key_compared_raw`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming.py`, `tests/test_landing_head.py`, `tests/test_landing.py`, `tests/intake/test_pipeline.py`
- Collected: 253 against a baseline of 253
- Kills: 3 (killed)
- Killed:
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_disagreeing_title_head_leaves_the_stem_head_to_agree`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_key_only_spec_over_a_headed_title_keeps_the_whole_head`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_an_unpadded_or_lowercase_key_agrees_with_its_padded_head`

Old text:

```
        return parsed is not None and parsed == parse_camelot(str(written))
```

New text:

```
        return str(supplied) == str(written)
```

### `r740-a.N4_stem_before_title`

normalize_spec: read the stem head before the title head

- File: `src/cratekit/core/naming.py`
- Source: `r740-a.json`, row `N4_stem_before_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming.py`, `tests/test_landing_head.py`, `tests/test_landing.py`, `tests/intake/test_pipeline.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_title_head_is_read_before_the_stem_head`

Old text:

```
    for head, fields in ((title_head, title_fields), (stem_head, stem_fields)):
```

New text:

```
    for head, fields in ((stem_head, stem_fields), (title_head, title_fields)):
```

### `r740-a.N5_no_marker_fill`

normalize_spec: a marker in the stripped head no longer marks the spec, so R21's marker is dropped

- File: `src/cratekit/core/naming.py`
- Source: `r740-a.json`, row `N5_no_marker_fill`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming.py`, `tests/test_landing_head.py`, `tests/test_landing.py`, `tests/intake/test_pipeline.py`
- Collected: 253 against a baseline of 253
- Kills: 4 (killed)
- Killed:
  - `tests/test_landing_head.py::test_a_lossy_file_keeps_its_marker_on_all_three_surfaces`
  - `tests/test_landing_head.py::test_the_lossy_flag_reported_is_the_one_the_name_was_rendered_from`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_marker_in_the_stripped_head_marks_the_spec`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_marker_only_head_marks_the_spec_and_invents_no_field`

Old text:

```
            if rule.literal in head:
                filled[rule.field] = True
```

New text:

```
            if rule.literal in head:
                pass
```

### `r740-a.N6_current_ignores_filled`

normalize_spec: judge the stem head against the spec alone, so it overwrites what the title head filled

- File: `src/cratekit/core/naming.py`
- Source: `r740-a.json`, row `N6_current_ignores_filled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming.py`, `tests/test_landing_head.py`, `tests/test_landing.py`, `tests/intake/test_pipeline.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_title_head_is_read_before_the_stem_head`

Old text:

```
        current = {name: filled.get(name, getattr(spec, name)) for name in values}
```

New text:

```
        current = {name: getattr(spec, name) for name in values}
```

### `r740-b.E1_library_name_from_stem`

existing guard sample: render_all derives the library name from the filename stem instead of the title tag

- File: `src/cratekit/core/naming.py`
- Source: `r740-b.json`, row `E1_library_name_from_stem`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming.py`, `tests/test_landing_head.py`, `tests/test_landing.py`, `tests/intake/test_pipeline.py`
- Collected: 253 against a baseline of 253
- Kills: 4 (killed)
- Killed:
  - `tests/test_landing_head.py::test_a_file_headed_in_its_filename_only_carries_that_head`
  - `tests/test_landing_head.py::test_a_filename_head_wins_over_a_disagreeing_key_tag`
  - `tests/test_landing_head.py::test_an_acquired_body_marker_is_not_doubled_into_the_head`
  - `tests/test_naming.py::TestRender::test_lossless_carries_no_marker`

Old text:

```
        library_name=title_tag,
```

New text:

```
        library_name=head + spec.stem,
```

### `u113-a.A3_no_pass_splits_nothing`

A landing given no pass still splits, by every named job on the library

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u113-a.json`, row `A3_no_pass_splits_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if not pass_name or not files:
        return ()
    found = sources(cfg, pass_name)
```

New text:

```
    if not files:
        return ()
    found = sources(cfg, pass_name or "")
```

### `u72-b.M20_shown_files`

The gate context lists no file names

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72-b.json`, row `M20_shown_files`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 48 against a baseline of 48
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land.py::test_the_first_run_stops_at_the_gate_and_moves_nothing`
  - `tests/test_intake_land.py::test_the_gate_screen_a_person_reads_names_the_files_and_the_intake_file`

Old text:

```
        "files": [item.name for item in planned.items],
```

New text:

```
        "files": [],
```

### `u72-b.M21_empty_to_engine`

An empty folder goes to the engine, which refuses it

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72-b.json`, row `M21_empty_to_engine`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 48 against a baseline of 48
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_plan_of_nothing_asks_nothing_of_the_export`
  - `tests/test_intake_land.py::test_an_empty_staging_folder_is_a_plan_of_nothing_and_makes_nothing`
  - `tests/test_intake_land.py::test_staging_holding_only_lists_and_dotfiles_is_a_plan_of_nothing`

Old text:

```
    if folder.is_dir() and not landing.listing(folder):
```

New text:

```
    if False:
```

### `u72-b.M22_listing_without_isdir`

The empty check lists a folder that may not exist

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72-b.json`, row `M22_listing_without_isdir`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_folder_that_is_not_there_is_refused_before_the_gate`

Old text:

```
    if folder.is_dir() and not landing.listing(folder):
```

New text:

```
    if not landing.listing(folder):
```

### `u72.M10_default_folder`

The default folder is the library root, not download staging

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72.json`, row `M10_default_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 48 against a baseline of 48
- Kills: 32 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_landing_in_another_process_refuses_this_one_until_it_ends`
  - `tests/test_intake_land.py::test_a_landing_under_another_batch_name_lands_while_one_is_held`
  - `tests/test_intake_land.py::test_a_landing_without_a_manifest_reports_nothing_about_labels`
  - `tests/test_intake_land.py::test_a_manifest_is_on_the_gate_screen_and_its_labels_are_in_the_envelope`
  - `tests/test_intake_land.py::test_a_manifest_whose_only_row_matched_nothing_still_reports_it`
  - `tests/test_intake_land.py::test_a_plan_over_a_usable_export_reaches_the_gate_with_the_digest_it_had_before`
  - `tests/test_intake_land.py::test_a_plan_over_an_export_that_is_not_a_collection_refuses_before_the_gate`
  - `tests/test_intake_land.py::test_a_plan_over_an_export_that_is_not_there_refuses_before_the_gate`
  - `tests/test_intake_land.py::test_a_plan_over_an_export_without_the_intake_folder_refuses_before_the_gate`
  - `tests/test_intake_land.py::test_a_recorded_abort_is_honored_over_a_library_that_went_missing`
  - `tests/test_intake_land.py::test_a_recorded_apply_over_an_export_that_went_missing_is_the_engine_s_refusal`
  - `tests/test_intake_land.py::test_a_refused_file_is_a_warning_a_person_reads`
  - `tests/test_intake_land.py::test_a_second_landing_under_a_held_batch_name_refuses_and_moves_nothing`
  - `tests/test_intake_land.py::test_a_stale_answer_is_refused_and_moves_nothing`
  - `tests/test_intake_land.py::test_an_abort_is_no_op_and_moves_nothing`
  - ... and 17 more, see the JSON sidecar

Old text:

```
    folder = Path(ctx.args.folder) if ctx.args.folder else Path(cfg.paths.download_staging)
```

New text:

```
    folder = Path(ctx.args.folder) if ctx.args.folder else Path(cfg.library.root)
```

