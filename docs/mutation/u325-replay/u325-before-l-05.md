# Mutation table: u325-before-l-05

Measured by `scripts/mutate.py` on 2026-11-22 22:24 UTC, branch `HEAD` at `539638eb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22663 collected. pytest invocations for this batch: 126.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:24 UTC for commit `539638ebe629`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 7, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22663 against 22663. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u144-a.A6_set_name_spelling` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 1 | killed |
| `u144-a.A7_only_matched` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 8 | killed |
| `u144-a.A8_empty_not_written` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 2 | killed |
| `u144-b.B1_unnamed_membership` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 1 | killed |
| `u144-b.B2_stale_digest` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 1 | killed |
| `u144-b.B4_convergence_latch` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 1 | killed |
| `u144-b.B5_read_back_exact` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 1 | killed |
| `u144-b.B6_read_back_missing` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 1 | killed |
| `u144-b.B7_writes_the_members` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 8 | killed |
| `u144-b.B8_commit_recorded` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 1 | killed |
| `u144-c.C1_again_now_held` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 1 | killed |
| `u144-c.C2_folder_unread` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 1 | killed |
| `u144-c.C4_missed_coefficient` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 1 | killed |
| `r1476.M10_no_name_slug_step` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 4 | killed |
| `r1476.M11_slug_step_beats_exact_name` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 1 | killed |
| `r1476.M12_no_identifier_fallback` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 3 | killed |
| `r1476.M13_needles_not_held` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 11 | killed |
| `r1476.M14_genre_join_by_name` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 2 | killed |
| `r1476.M15_answer_without_genre` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 5 | killed |
| `r1476.M16_unsluggable_raises` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 2 | killed |
| `r1476.M17_remedy_names_display_name` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 3 | killed |
| `r1476.M18_remedy_head_never_shared` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 1 | killed |
| `r1476.M19_outranked_wording` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 1 | killed |
| `r1476.M1_identifier_not_frozen` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 7 | killed |
| `r1476.M2_folder_seam_by_name` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 2 | killed |
| `r1476.M3_folder_seam_with_no_identifier` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 2 | killed |
| `r1476.M6_worker_hands_no_folder_seam` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 2 | killed |
| `r1476.M7_worker_hands_identifier_as_label` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 1 | killed |
| `r1476.M8_shared_name_takes_first` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 10 | killed |
| `r1476.M9_identifier_first` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 5 | killed |
| `r1476.M4_engine_ignores_folder_seam` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 286 | 2 | killed |
| `r1476.M5_tag_one_drops_folder_seam` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 286 | 2 | killed |
| `u77-c.C6_gate_manifest_bytes` | `src/cratekit/intake/land_cli.py` | user | 6 file(s) | 285 | 1 | killed |
| `u77-c.C7_digest_handed_to_engine` | `src/cratekit/intake/land_cli.py` | user | 6 file(s) | 285 | 1 | killed |
| `u77-c.C8_unfiled_rows_warned` | `src/cratekit/intake/land_cli.py` | user | 6 file(s) | 285 | 2 | killed |
| `u77-a.A1_label_source_filter` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 285 | 1 | killed |
| `u77-a.A2_engine_stale_digest` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 285 | 20 | killed |
| `u77-a.A4_export_reason_mapping` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 285 | 2 | killed |
| `u77-a.A5_needs_review_guard` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 285 | 1 | killed |
| `u77-a.A6_no_landed_file_guard` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 285 | 5 | killed |
| `u77-a.A7_year_absent_guard` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 285 | 1 | killed |
| `u77-a.A8_library_template` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 285 | 1 | killed |
| `u77-a.A9_this_runs_files_only` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 285 | 1 | killed |
| `u77-a2.A2_engine_stale_digest` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 285 | 1 | killed |
| `u77-b.B1_reported_ids_deduped` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 285 | 1 | killed |
| `u77-b.B2_disk_refusal_reported` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 285 | 1 | killed |
| `u77-b.B3_index_refusal_reported` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 285 | 1 | killed |
| `u77-b.B5_unmatched_sentence` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 285 | 1 | killed |
| `u77-b.B6_trial_id` | `src/cratekit/write/trees.py` | user | 6 file(s) | 285 | 2 | killed |
| `u77-b.B7_check_empty_catalog` | `src/cratekit/write/trees.py` | user | 6 file(s) | 285 | 2 | killed |
| `u77-b.B8_label_write_order` | `src/cratekit/write/trees.py` | user | 6 file(s) | 285 | 3 | killed |
| `u287-m11.M11_gone_offers_nothing` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 62 | 3 | killed |
| `u287.M10_gone_on_one_read` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 62 | 5 | killed |
| `u287.M13_folder_separator` | `src/cratekit/sync/removed.py` | maintainer | 1 file(s) | 62 | 1 | killed |
| `u287.M14_twin_is_own_filing` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 62 | 30 | killed |
| `u287.M16_gone_holds_what_was_recorded` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 62 | 3 | killed |
| `u287.M17_gone_with_no_record_is_not_whole` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 62 | 2 | killed |
| `u287.M18_set_aside_rows_count` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 62 | 1 | killed |
| `u287.M19_old_prefix_is_synced` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 62 | 1 | killed |
| `u287.M1_partial_read_stops_offers` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 62 | 8 | killed |
| `u287.M20_unreadable_record_is_not_whole` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 62 | 1 | killed |
| `u287.M2_held_by_isrc` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 62 | 3 | killed |
| `u287.M3_held_by_recording` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 62 | 2 | killed |
| `u287.M4_held_before_the_pass` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 62 | 2 | killed |
| `u287.M5_not_this_pass_file` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 62 | 2 | killed |
| `u287.M6_on_another_synced` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 62 | 8 | killed |
| `u287.M7_in_a_playlist_of_yours` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 62 | 3 | killed |
| `u287.M8_empty_read_untrusted` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 62 | 1 | killed |
| `u287.M9_short_read_untrusted` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 62 | 1 | killed |
| `u288.M16_stale_digest` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 62 | 1 | killed |
| `u288.M17_only_the_offered` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 62 | 7 | killed |
| `u288.M18_unmeasured_kept` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 62 | 1 | killed |
| `u288.M19_first_position` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 62 | 1 | killed |
| `u288.M20_read_back_refusal` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 62 | 1 | killed |
| `u288.M14_confinement_not_called` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 62 | 1 | killed |
| `u288.M3_unmeasured_tables_skipped` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 62 | 3 | killed |
| `u288.M4_target_id_not_asked` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 62 | 1 | killed |
| `u288.M5_prepare_liveness` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 62 | 1 | killed |
| `u288.M6_prepare_unmeasured_refusal` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 62 | 3 | killed |
| `u288.M7_prepare_identity` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 62 | 1 | killed |
| `u288.M8_memberships_kept` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 62 | 11 | killed |
| `u255.C4_held_before_read_and_playlist_keeps_the_hold` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 330 | 2 | killed |
| `u255.C8_no_open_before_and_retry_opens_raw` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 330 | 3 | killed |
| `u255.M10_failed_attempt_keeps_the_hold` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 330 | 5 | killed |
| `u255.M11_retry_opens_raw` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 330 | 2 | killed |
| `u255.M12_add_never_retried` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 330 | 7 | killed |
| `u255.M13_add_retried_twice` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 330 | 3 | killed |
| `u255.M1_playlist_keeps_the_hold` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 330 | 2 | killed |
| `u255.M2_membership_reads_the_held_object` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 330 | 3 | killed |
| `u255.M3_membership_holds_nothing` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 330 | 6 | killed |
| `u255.M5_membership_reuses_the_hold` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 330 | 1 | killed |
| `u255.M6_held_never_stores` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 330 | 3 | killed |
| `u255.M7_held_always_opens` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 330 | 9 | killed |
| `u255.M9_every_attempt_opens` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 330 | 11 | killed |
| `u255.S1_member_already_on` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 330 | 2 | killed |
| `u255.S2_read_back_trusts_the_cache` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 330 | 3 | killed |
| `u255.S3_answer_absent_passes` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 330 | 1 | killed |
| `u255.S4_added_not_remembered` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 330 | 5 | killed |
| `u99-b.B1_parser_limit_floor` | `src/cratekit/label/cli.py` | user | 3 file(s) | 293 | 1 | killed |
| `u99-b.B5_add_drops_seeds` | `src/cratekit/label/cli.py` | user | 3 file(s) | 293 | 11 | killed |
| `u99-b.B6_add_drops_limit` | `src/cratekit/label/cli.py` | user | 3 file(s) | 293 | 3 | killed |
| `u99-b.B7_set_drops_seeds` | `src/cratekit/label/cli.py` | user | 3 file(s) | 293 | 2 | killed |
| `u99-b.B8_list_json_empty` | `src/cratekit/label/cli.py` | user | 3 file(s) | 293 | 12 | killed |
| `u99-b.B9_detail_drops_seeds` | `src/cratekit/label/cli.py` | user | 3 file(s) | 293 | 1 | killed |
| `u99-a.A10_edit_drops_match` | `src/cratekit/label/registry.py` | user | 3 file(s) | 293 | 1 | killed |
| `u99-a.A11_edit_drops_seeds` | `src/cratekit/label/registry.py` | user | 3 file(s) | 293 | 1 | killed |
| `u99-a.A12_edit_drops_limit` | `src/cratekit/label/registry.py` | user | 3 file(s) | 293 | 1 | killed |
| `u99-a.A13_by_name_unnormalized` | `src/cratekit/label/registry.py` | user | 3 file(s) | 22663 | 0 (promoted) | zero |
| `u99-a.A1_blank_seed` | `src/cratekit/label/registry.py` | user | 3 file(s) | 293 | 1 | killed |
| `u99-a.A2_malformed_id_seed` | `src/cratekit/label/registry.py` | user | 3 file(s) | 293 | 7 | killed |
| `u99-a.A3_id_prefix_case` | `src/cratekit/label/registry.py` | user | 3 file(s) | 293 | 1 | killed |
| `u99-a.A4_id_digits_optional` | `src/cratekit/label/registry.py` | user | 3 file(s) | 293 | 1 | killed |
| `u99-a.A5_id_prefix_match` | `src/cratekit/label/registry.py` | user | 3 file(s) | 293 | 2 | killed |
| `u99-a.A7_add_unchecked_seeds` | `src/cratekit/label/registry.py` | user | 3 file(s) | 293 | 7 | killed |
| `u99-a.A8_edit_unchecked_seeds` | `src/cratekit/label/registry.py` | user | 3 file(s) | 293 | 1 | killed |
| `u99-b.A6r_store_limit_floor` | `src/cratekit/label/registry.py` | maintainer | 3 file(s) | 293 | 1 | killed |
| `r923.N11_digest_drops_items` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 2 | killed |

## Zero rows and what they owe

- `u99-a.A13_by_name_unnormalized` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `u144-a.A6_set_name_spelling`

Account sets: write the stripped account name as it is, slash and all

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-a.json`, row `A6_set_name_spelling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_slash_in_the_account_name_is_written_as_a_dash`

Old text:

```
            sets_found.append((folder_name, playlist_id, set_cli.set_name(stripped)))
```

New text:

```
            sets_found.append((folder_name, playlist_id, stripped))
```

### `u144-a.A7_only_matched`

Match: take a track with no row as a member, an empty id in the playlist

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-a.json`, row `A7_only_matched`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 8 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_miss_the_library_lacks_ahead_of_an_unread_track_keeps_set_order`
  - `tests/test_organize_inspiration.py::test_a_near_match_is_a_question_named_as_a_miss_and_never_written`
  - `tests/test_organize_inspiration.py::test_a_second_run_plans_nothing`
  - `tests/test_organize_inspiration.py::test_a_set_with_no_match_is_reported_and_no_empty_playlist_is_written`
  - `tests/test_organize_inspiration.py::test_a_step_whose_every_set_has_no_match_plans_nothing_and_writes_nothing`
  - `tests/test_organize_inspiration.py::test_an_unread_track_keeps_the_sets_positions_for_every_other_miss`
  - `tests/test_organize_inspiration.py::test_eighteen_tracks_fifteen_in_the_library_plan_fifteen_and_name_three`
  - `tests/test_organize_inspiration.py::test_the_writer_refuses_a_membership_the_plan_did_not_name`

Old text:

```
        held, why = row_of(one)
        if held:
```

New text:

```
        held, why = row_of(one)
        if True:
```

### `u144-a.A8_empty_not_written`

Decide: plan a set with no match as a create, an empty playlist

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-a.json`, row `A8_empty_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_set_with_no_match_is_reported_and_no_empty_playlist_is_written`
  - `tests/test_organize_inspiration.py::test_a_step_whose_every_set_has_no_match_plans_nothing_and_writes_nothing`

Old text:

```
        action=CREATE if members else EMPTY,
```

New text:

```
        action=CREATE,
```

### `u144-b.B1_unnamed_membership`

Write guard: drop the refusal of a membership the approved plan did not name

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-b.json`, row `B1_unnamed_membership`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_the_writer_refuses_a_membership_the_plan_did_not_name`

Old text:

```
        if unnamed:
```

New text:

```
        if False:
```

### `u144-b.B2_stale_digest`

Write guard: drop the digest comparison of the plan taken again on the write handle

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-b.json`, row `B2_stale_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_set_given_its_inspiration_playlist_since_the_plan_is_stale`

Old text:

```
    if now.digest() != approved.digest():
```

New text:

```
    if False:
```

### `u144-b.B4_convergence_latch`

Write: drop the INSPIRATION tree's convergence latch before the session

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-b.json`, row `B4_convergence_latch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_convergence_latch_refuses_the_write_before_anything_is_written`

Old text:

```
        convergence.assert_tree_writable(cfg, db, approved.tree_id, tree_registry.read(cfg))
```

New text:

```
        pass
```

### `u144-b.B5_read_back_exact`

Read back: accept a made playlist holding rows the plan did not name, or out of order

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-b.json`, row `B5_read_back_exact`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_read_back_holding_a_row_the_plan_did_not_name_is_refused`

Old text:

```
        if missing or (one.created and not exact):
```

New text:

```
        if missing:
```

### `u144-b.B6_read_back_missing`

Read back: accept a found playlist missing a planned row

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-b.json`, row `B6_read_back_missing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_read_back_holding_a_row_the_plan_did_not_name_is_refused`

Old text:

```
        if missing or (one.created and not exact):
```

New text:

```
        if one.created and not exact:
```

### `u144-b.B7_writes_the_members`

Write: add every member but the first

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-b.json`, row `B7_writes_the_members`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 8 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_readable_track_with_no_provider_id_is_matched_as_before`
  - `tests/test_organize_inspiration.py::test_a_second_run_plans_nothing`
  - `tests/test_organize_inspiration.py::test_a_set_with_no_match_is_reported_and_no_empty_playlist_is_written`
  - `tests/test_organize_inspiration.py::test_a_slash_in_the_account_name_is_written_as_a_dash`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_artist_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_title_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_eighteen_tracks_fifteen_in_the_library_plan_fifteen_and_name_three`
  - `tests/test_organize_inspiration.py::test_the_name_written_is_the_account_name_without_its_prefix`

Old text:

```
        added = rb_writer.add_memberships(db, playlist, row.members)
```

New text:

```
        added = rb_writer.add_memberships(db, playlist, row.members[1:])
```

### `u144-b.B8_commit_recorded`

Record: record no commit, so a restore cannot weigh the session

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-b.json`, row `B8_commit_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_eighteen_tracks_fifteen_in_the_library_plan_fifteen_and_name_three`

Old text:

```
    made = [one for one in wrote if one.added or one.created]
```

New text:

```
    made = []
```

### `u144-c.C1_again_now_held`

B3 measured again after the stale test was tightened: a set given its INSPIRATION playlist since the plan is decided as before, not skipped

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-c.json`, row `C1_again_now_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_set_given_its_inspiration_playlist_since_the_plan_is_stale`

Old text:

```
                replace(row, action=SKIP, members=(), misses=(), withheld=0, why="")
                if now
```

New text:

```
                replace(row, action=SKIP, members=(), misses=(), withheld=0, why="")
                if False
```

### `u144-c.C2_folder_unread`

Account sets: let a folder listing refusal refuse the whole step instead of one folder

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-c.json`, row `C2_folder_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_sets_folder_that_cannot_be_listed_is_named_and_the_rest_still_plan`

Old text:

```
            listed = remote.folder_playlists(folder_id)
        except CratekitError as exc:
```

New text:

```
            listed = remote.folder_playlists(folder_id)
        except ZeroDivisionError as exc:
```

### `u144-c.C4_missed_coefficient`

Counts: leave the withheld tracks out of the tracks missed

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-c.json`, row `C4_missed_coefficient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_short_listing_counts_what_the_provider_withheld`

Old text:

```
            "tracks missed": sum(len(row.misses) + row.withheld for row in self.creates),
```

New text:

```
            "tracks missed": sum(len(row.misses) for row in self.creates),
```

### `r1476.M10_no_name_slug_step`

_label_seam: drop the name slug step, so Some*Label no longer names Some Label

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M10_no_name_slug_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_name_one_label_holds_exactly_is_never_lost_to_a_slug_it_shares`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[(Alpha)]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[Alpha.]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[\xc1lpha]`

Old text:

```
            named = tuple(entry for entry in held.labels.values() if _name_slug(entry.name) == wanted)
```

New text:

```
            named = ()
```

### `r1476.M11_slug_step_beats_exact_name`

_label_seam: run the name slug step even when a label is called the tag exactly

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M11_slug_step_beats_exact_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_name_one_label_holds_exactly_is_never_lost_to_a_slug_it_shares`

Old text:

```
        if not named and wanted:
            named = tuple(entry for entry in held.labels.values() if _name_slug(entry.name) == wanted)
```

New text:

```
        if wanted:
            named = tuple(entry for entry in held.labels.values() if _name_slug(entry.name) == wanted)
```

### `r1476.M12_no_identifier_fallback`

_label_seam: drop the identifier step, so a renamed label's old name reaches nothing

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M12_no_identifier_fallback`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_tag_carrying_a_labels_name_from_before_its_rename_still_reaches_it`
  - `tests/test_label_genre.py::test_a_tag_is_read_as_a_name_before_an_identifier`
  - `tests/test_label_genre.py::test_a_tag_names_one_label_by_its_name_its_slug_or_the_name_it_was_registered_under`

Old text:

```
            named = tuple(entry for entry in (held.labels.get(wanted),) if entry is not None)
```

New text:

```
            named = ()
```

### `r1476.M13_needles_not_held`

_frozen_labels: hold only the labels with a genre, so a lookup falls through to another label

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M13_needles_not_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 11 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_files_own_tag_naming_a_shared_name_is_given_neither_labels_genre`
  - `tests/test_label_genre.py::test_a_name_one_label_holds_exactly_is_never_lost_to_a_slug_it_shares`
  - `tests/test_label_genre.py::test_a_name_that_is_another_labels_identifier_is_the_label_named_so`
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[ Alpha ]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[(Alpha)]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[ALPHA]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[Alpha.]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[Alpha]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[\xc1lpha]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[alpha]`

Old text:

```
    for rows in (needles if isinstance(needles, Mapping) else {}, frozen):
```

New text:

```
    for rows in (frozen,):
```

### `r1476.M14_genre_join_by_name`

_frozen_labels: give each frozen label the genre of the first label with a genre sharing its name

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M14_genre_join_by_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_label_sharing_its_name_with_one_carrying_a_genre_is_never_given_that_genre`
  - `tests/test_label_genre.py::test_the_folders_label_is_answered_by_its_frozen_identifier_whatever_it_is_called`

Old text:

```
                    genre=genres.get(str(label_id)),
```

New text:

```
                    genre=next((genres[other] for other, them in frozen.items() if other in genres and isinstance(them, Mapping) and them.get("name") == row.get("name")), None),
```

### `r1476.M15_answer_without_genre`

_answered: answer a label with no genre as one

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M15_answer_without_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_label_sharing_its_name_with_one_carrying_a_genre_is_never_given_that_genre`
  - `tests/test_label_genre.py::test_a_name_that_is_another_labels_identifier_is_the_label_named_so`
  - `tests/test_label_genre.py::test_a_tag_is_read_as_a_name_before_an_identifier`
  - `tests/test_label_genre.py::test_a_tag_names_one_label_by_its_name_its_slug_or_the_name_it_was_registered_under`
  - `tests/test_label_genre.py::test_the_folders_label_is_answered_by_its_frozen_identifier_whatever_it_is_called`

Old text:

```
    if entry is None or not entry.genre:
        return None
    return tag_engine.LabelAnswer
```

New text:

```
    if entry is None:
        return None
    return tag_engine.LabelAnswer
```

### `r1476.M16_unsluggable_raises`

_name_slug: let a name that could never be a label raise rather than read as none

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M16_unsluggable_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_label_tag_that_could_never_name_a_label_is_searched_and_never_fails`
  - `tests/test_label_genre.py::test_a_tag_names_one_label_by_its_name_its_slug_or_the_name_it_was_registered_under`

Old text:

```
    except CratekitError:
        return ""


def _label_seam
```

New text:

```
    except CratekitError:
        raise


def _label_seam
```

### `r1476.M17_remedy_names_display_name`

_label_payload: the no genre remedy names the label by its display name

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M17_remedy_names_display_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_label_sharing_its_name_with_one_carrying_a_genre_is_never_given_that_genre`
  - `tests/test_label_genre.py::test_a_name_that_is_another_labels_identifier_is_the_label_named_so`
  - `tests/test_label_genre.py::test_the_remedy_names_the_label_by_its_identifier`

Old text:

```
            handle = entry.label_id
```

New text:

```
            handle = entry.name
```

### `r1476.M18_remedy_head_never_shared`

_label_payload: never name the identifier beside a shared display name in the warning's head

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M18_remedy_head_never_shared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_label_sharing_its_name_with_one_carrying_a_genre_is_never_given_that_genre`

Old text:

```
            shared = len(held.named(entry.name)) > 1
```

New text:

```
            shared = False
```

### `r1476.M19_outranked_wording`

_label_warnings: the outranked warning no longer says a tag can name two labels

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M19_outranked_wording`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`

Old text:

```
names two labels or "
```

New text:

```
names a retired label "
```

### `r1476.M1_identifier_not_frozen`

_label_payload: freeze the label's display name where its identifier goes, so the sweep answers --label by a name another label may share

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M1_identifier_not_frozen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_file_that_will_not_take_its_labels_genre_fails_and_is_never_counted_tagged`
  - `tests/test_label_genre.py::test_a_label_sharing_its_name_with_one_carrying_a_genre_is_never_given_that_genre`
  - `tests/test_label_genre.py::test_a_puls_batch_is_tagged_by_the_label_and_the_report_counts_it_apart`
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`
  - `tests/test_label_genre.py::test_files_whose_own_tag_outranked_the_label_are_counted_and_named`
  - `tests/test_label_genre.py::test_the_genres_are_frozen_when_the_sweep_is_queued`
  - `tests/test_label_genre.py::test_the_label_carrying_the_genre_still_gives_it_under_the_shared_name`

Old text:

```
        frozen["label_id"] = entry.label_id
```

New text:

```
        frozen["label_id"] = entry.name
```

### `r1476.M2_folder_seam_by_name`

_folder_seam: look the folder's label up again by the name the engine hands it, the card's defect

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M2_folder_seam_by_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_label_sharing_its_name_with_one_carrying_a_genre_is_never_given_that_genre`
  - `tests/test_label_genre.py::test_the_folders_label_is_answered_by_its_frozen_identifier_whatever_it_is_called`

Old text:

```
        return _answered(held.labels.get(wanted))
```

New text:

```
        return _answered(held.by_name(_name) or held.labels.get(wanted))
```

### `r1476.M3_folder_seam_with_no_identifier`

_folder_seam: hand a seam for a job frozen with no identifier, so its --label answers nothing

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M3_folder_seam_with_no_identifier`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_sweep_frozen_with_no_identifier_reads_its_label_as_a_name`
  - `tests/test_label_genre.py::test_a_sweep_queued_before_the_identifier_was_frozen_still_tags_by_its_labels_name`

Old text:

```
    if held is None or not wanted:
```

New text:

```
    if held is None:
```

### `r1476.M6_worker_hands_no_folder_seam`

handle: hand the engine no folder seam

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M6_worker_hands_no_folder_seam`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`
  - `tests/test_label_genre.py::test_the_label_carrying_the_genre_still_gives_it_under_the_shared_name`

Old text:

```
        folder_genre=_folder_seam(payload),
```

New text:

```
        folder_genre=None,
```

### `r1476.M7_worker_hands_identifier_as_label`

handle: hand the engine the frozen identifier as the folder's label text, round one's shape

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M7_worker_hands_identifier_as_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_sweep_queued_before_the_identifier_was_frozen_still_tags_by_its_labels_name`

Old text:

```
        label=str(payload.get("label") or "") or None,
```

New text:

```
        label=str(payload.get("label_id") or "") or None,
```

### `r1476.M8_shared_name_takes_first`

_label_seam: a name two labels hold answers the first holder

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M8_shared_name_takes_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 10 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_files_own_tag_naming_a_shared_name_is_given_neither_labels_genre`
  - `tests/test_label_genre.py::test_a_name_one_label_holds_exactly_is_never_lost_to_a_slug_it_shares`
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[ Alpha ]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[(Alpha)]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[ALPHA]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[Alpha.]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[Alpha]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[\xc1lpha]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[alpha]`

Old text:

```
        return _answered(named[0]) if len(named) == 1 else None
```

New text:

```
        return _answered(named[0]) if named else None
```

### `r1476.M9_identifier_first`

_label_seam: read a tag as an identifier before a name, round one's blockers

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M9_identifier_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_files_own_tag_naming_a_shared_name_is_given_neither_labels_genre`
  - `tests/test_label_genre.py::test_a_name_that_is_another_labels_identifier_is_the_label_named_so`
  - `tests/test_label_genre.py::test_a_tag_is_read_as_a_name_before_an_identifier`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[alpha]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_label_whose_name_is_another_labels_identifier_takes_its_genre`

Old text:

```
        named = held.named(name)
        wanted = _name_slug(name)
```

New text:

```
        named = tuple(entry for entry in (held.labels.get(name),) if entry is not None) or held.named(name)
        wanted = _name_slug(name)
```

### `r1476.M4_engine_ignores_folder_seam`

_by_label: answer --label through the tag seam, never the folder seam

- File: `src/cratekit/tagging/tag.py`
- Source: `r1476.json`, row `M4_engine_ignores_folder_seam`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`
  - `tests/test_label_genre.py::test_the_label_carrying_the_genre_still_gives_it_under_the_shared_name`

Old text:

```
        return _Labelled((folder_genre or label_genre)(typed), own, NAMED_BY_FOLDER)
```

New text:

```
        return _Labelled(label_genre(typed), own, NAMED_BY_FOLDER)
```

### `r1476.M5_tag_one_drops_folder_seam`

tag_one: never hand the folder seam to _by_label

- File: `src/cratekit/tagging/tag.py`
- Source: `r1476.json`, row `M5_tag_one_drops_folder_seam`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`
  - `tests/test_label_genre.py::test_the_label_carrying_the_genre_still_gives_it_under_the_shared_name`

Old text:

```
        else _by_label(path, label_genre, label, copyright_labels, folder_genre)
```

New text:

```
        else _by_label(path, label_genre, label, copyright_labels)
```

### `u77-c.C6_gate_manifest_bytes`

_payload: leave the manifest's bytes out of the plan identity, so the gate accepts an answer given against other rows (the gate layer alone, the engine's own check left in place)

- File: `src/cratekit/intake/land_cli.py`
- Source: `u77-c.json`, row `C6_gate_manifest_bytes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 285 against a baseline of 285
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_an_answer_given_against_one_manifest_is_stale_once_it_is_rewritten`

Old text:

```
identity["manifest_bytes"] = manifest.digest
```

New text:

```
identity["manifest_bytes"] = ""
```

### `u77-c.C7_digest_handed_to_engine`

intake_land: hand the engine no fingerprint, so a manifest rewritten between the gate and the first move is filed

- File: `src/cratekit/intake/land_cli.py`
- Source: `u77-c.json`, row `C7_digest_handed_to_engine`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 285 against a baseline of 285
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_the_engine_is_handed_the_fingerprint_of_the_bytes_the_gate_compared`

Old text:

```
manifest_digest=manifest.digest if manifest is not None else None,
```

New text:

```
manifest_digest=None,
```

### `u77-c.C8_unfiled_rows_warned`

intake_land: warn about refused files only, so a label row filed under nothing is named nowhere a person reads

- File: `src/cratekit/intake/land_cli.py`
- Source: `u77-c.json`, row `C8_unfiled_rows_warned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 285 against a baseline of 285
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_manifest_is_on_the_gate_screen_and_its_labels_are_in_the_envelope`
  - `tests/test_intake_land.py::test_a_manifest_whose_only_row_matched_nothing_still_reports_it`

Old text:

```
for entry in (*landed.refused, *landed.unlabelled)
```

New text:

```
for entry in (*landed.refused,)
```

### `u77-a.A1_label_source_filter`

read_label_manifest: keep every manifest row whatever its source, so a favourites or playlist row is filed under a label

- File: `src/cratekit/intake/landing.py`
- Source: `u77-a.json`, row `A1_label_source_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 285 against a baseline of 285
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_an_undeclared_catalog_tree_costs_a_landing_with_no_label_row_nothing`

Old text:

```
rows=tuple(row for row in rows if row.provenance.source == LABEL_SOURCE),
```

New text:

```
rows=tuple(row for row in rows if row.provenance.source),
```

### `u77-a.A2_engine_stale_digest`

apply: never compare the manifest's bytes with the fingerprint the caller was shown, so a manifest rewritten after the gate is filed (the engine layer alone, the gate's own check left in place)

- File: `src/cratekit/intake/landing.py`
- Source: `u77-a.json`, row `A2_engine_stale_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 285 against a baseline of 285
- Kills: 20 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_a_batch_folder_that_cannot_be_indexed_reports_every_label_row`
  - `tests/test_landing_labels.py::test_a_catalog_tree_the_database_owns_refuses_before_any_file_moves`
  - `tests/test_landing_labels.py::test_a_file_already_in_the_batch_folder_is_not_filed_under_this_landing`
  - `tests/test_landing_labels.py::test_a_held_year_playlist_the_writer_cannot_extend_refuses_before_any_move`
  - `tests/test_landing_labels.py::test_a_label_row_no_landed_file_matches_is_reported_by_name`
  - `tests/test_landing_labels.py::test_a_label_row_with_no_year_is_reported_and_files_nothing`
  - `tests/test_landing_labels.py::test_a_landed_file_at_another_version_is_a_question_and_is_not_filed`
  - `tests/test_landing_labels.py::test_a_manifest_rewritten_after_it_was_fingerprinted_is_stale_and_moves_nothing`
  - `tests/test_landing_labels.py::test_a_marked_lossy_file_with_no_title_tag_is_still_filed`
  - `tests/test_landing_labels.py::test_a_second_landing_into_the_first_ones_file_merges_and_duplicates_nothing`
  - `tests/test_landing_labels.py::test_a_tree_the_disk_refuses_after_the_moves_is_named_and_the_file_stays`
  - `tests/test_landing_labels.py::test_an_export_holding_a_label_folder_twice_refuses_before_any_file_moves`
  - `tests/test_landing_labels.py::test_an_undeclared_catalog_tree_costs_a_landing_with_no_label_row_nothing`
  - `tests/test_landing_labels.py::test_an_undeclared_catalog_tree_refuses_before_any_file_moves`
  - `tests/test_landing_labels.py::test_one_recording_listed_under_two_ids_is_in_its_year_once`
  - ... and 5 more, see the JSON sidecar

Old text:

```
if manifest_digest is not None and read.digest != manifest_digest:
```

New text:

```
if manifest_digest is None and read.digest != manifest_digest:
```

### `u77-a.A4_export_reason_mapping`

_check_export: pass the writer's internal-error through unchanged, so a doubled label folder in the person's export reaches them as a defect

- File: `src/cratekit/intake/landing.py`
- Source: `u77-a.json`, row `A4_export_reason_mapping`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 285 against a baseline of 285
- Kills: 2 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_a_held_year_playlist_the_writer_cannot_extend_refuses_before_any_move`
  - `tests/test_landing_labels.py::test_an_export_holding_a_label_folder_twice_refuses_before_any_file_moves`

Old text:

```
if exc.cause.reason != "internal-error":
```

New text:

```
if exc.cause.reason:
```

### `u77-a.A5_needs_review_guard`

_file_labels: stop treating a needs review match as a question, so a row whose batch holds another version falls through to the unmatched answer

- File: `src/cratekit/intake/landing.py`
- Source: `u77-a.json`, row `A5_needs_review_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 285 against a baseline of 285
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_a_landed_file_at_another_version_is_a_question_and_is_not_filed`

Old text:

```
if found.state is match.MatchState.NEEDS_REVIEW:
```

New text:

```
if found.state is match.MatchState.SUPPRESSED:
```

### `u77-a.A6_no_landed_file_guard`

_file_labels: file a row that resolved to no file this run placed, so a year playlist is written for a track the intake file gave no id

- File: `src/cratekit/intake/landing.py`
- Source: `u77-a.json`, row `A6_no_landed_file_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 285 against a baseline of 285
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_manifest_is_on_the_gate_screen_and_its_labels_are_in_the_envelope`
  - `tests/test_intake_land.py::test_a_manifest_whose_only_row_matched_nothing_still_reports_it`
  - `tests/test_landing_labels.py::test_a_file_already_in_the_batch_folder_is_not_filed_under_this_landing`
  - `tests/test_landing_labels.py::test_a_label_row_no_landed_file_matches_is_reported_by_name`
  - `tests/test_landing_labels.py::test_a_second_landing_into_the_first_ones_file_merges_and_duplicates_nothing`

Old text:

```
        if not landed:
            # TRUE OF BOTH ROWS
```

New text:

```
        if landed is None:
            # TRUE OF BOTH ROWS
```

### `u77-a.A7_year_absent_guard`

_file_labels: file a label row that carries no year, so a playlist named for the label and None is written

- File: `src/cratekit/intake/landing.py`
- Source: `u77-a.json`, row `A7_year_absent_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 285 against a baseline of 285
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_a_label_row_with_no_year_is_reported_and_files_nothing`

Old text:

```
        if not label or year is None:
            absent =
```

New text:

```
        if not label:
            absent =
```

### `u77-a.A8_library_template`

_file_labels: index the batch folder with the bare default name template, so the library's lossy marker stays in a title read from the filename

- File: `src/cratekit/intake/landing.py`
- Source: `u77-a.json`, row `A8_library_template`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 285 against a baseline of 285
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_a_marked_lossy_file_with_no_title_tag_is_still_filed`

Old text:

```
index = match.index_library(batch_dir, template=template)
```

New text:

```
index = match.index_library(batch_dir)
```

### `u77-a.A9_this_runs_files_only`

_file_labels: take a matched path's id without asking whether this run placed it (the membership test removed, the lookup defaulted), so a file an earlier landing left in the batch folder is filed under id None

- File: `src/cratekit/intake/landing.py`
- Source: `u77-a.json`, row `A9_this_runs_files_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 285 against a baseline of 285
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_a_file_already_in_the_batch_folder_is_not_filed_under_this_landing`

Old text:

```
            ids[Path(path).resolve()]
            for path in (found.paths if found.state is match.MatchState.MATCHED else ())
            if Path(path).resolve() in ids

```

New text:

```
            ids.get(Path(path).resolve())
            for path in (found.paths if found.state is match.MatchState.MATCHED else ())

```

### `u77-a2.A2_engine_stale_digest`

apply: the same row as u77-a's, measured again with a mutation that only removes the guard. The first inverted the test for a fingerprint being given, so it refused every landing that gave none and its 19 deaths were mostly not the guard's. This one compares the fingerprint with itself, so the check can never fire and nothing else changes

- File: `src/cratekit/intake/landing.py`
- Source: `u77-a2.json`, row `A2_engine_stale_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 285 against a baseline of 285
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_a_manifest_rewritten_after_it_was_fingerprinted_is_stale_and_moves_nothing`

Old text:

```
if manifest_digest is not None and read.digest != manifest_digest:
```

New text:

```
if manifest_digest is not None and manifest_digest != manifest_digest:
```

### `u77-b.B1_reported_ids_deduped`

_label: report a year's ids as collected instead of deduplicated, so a recording listed under two provider ids is reported twice while the file holds it once

- File: `src/cratekit/intake/landing.py`
- Source: `u77-b.json`, row `B1_reported_ids_deduped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 285 against a baseline of 285
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_one_recording_listed_under_two_ids_is_in_its_year_once`

Old text:

```
track_ids=tuple(rbxml.dedupe_track_ids(years[label][year])),
```

New text:

```
track_ids=tuple(years[label][year]),
```

### `u77-b.B2_disk_refusal_reported`

_label: catch only a structured refusal from the tree write, so a disk that refuses after the moves raises out of a landing that already succeeded

- File: `src/cratekit/intake/landing.py`
- Source: `u77-b.json`, row `B2_disk_refusal_reported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 285 against a baseline of 285
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_a_tree_the_disk_refuses_after_the_moves_is_named_and_the_file_stays`

Old text:

```
    except (CratekitError, OSError) as exc:
        said = f"the label tree could not be written ({exc})"
```

New text:

```
    except CratekitError as exc:
        said = f"the label tree could not be written ({exc})"
```

### `u77-b.B3_index_refusal_reported`

_label: stop catching a batch folder that cannot be read, so the index raises after the moves

- File: `src/cratekit/intake/landing.py`
- Source: `u77-b.json`, row `B3_index_refusal_reported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 285 against a baseline of 285
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_a_batch_folder_that_cannot_be_indexed_reports_every_label_row`

Old text:

```
    except OSError as exc:
        said = f"the batch folder could not be read
```

New text:

```
    except KeyError as exc:
        said = f"the batch folder could not be read
```

### `u77-b.B5_unmatched_sentence`

_file_labels: reword the unmatched sentence so it no longer limits the claim to this run, which is false of a row an earlier landing filed

- File: `src/cratekit/intake/landing.py`
- Source: `u77-b.json`, row `B5_unmatched_sentence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 285 against a baseline of 285
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_a_label_row_no_landed_file_matches_is_reported_by_name`

Old text:

```
sentence=f"{spelled} was filed under no label playlist by this run, because {because}",
```

New text:

```
sentence=f"{spelled} was filed under no label playlist at all, because {because}",
```

### `u77-b.B6_trial_id`

check_record_labels_tree: trial every year with no id, so the writer returns from a held playlist before its three layout refusals and the check passes what the write refuses

- File: `src/cratekit/write/trees.py`
- Source: `u77-b.json`, row `B6_trial_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 285 against a baseline of 285
- Kills: 2 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_a_held_year_playlist_the_writer_cannot_extend_refuses_before_any_move`
  - `tests/test_tree_writer.py::test_the_catalog_check_reaches_a_held_playlist_the_writer_cannot_extend`

Old text:

```
trial, label, [(f"{label} {year}", [_TRIAL_ID]) for year in years], target
```

New text:

```
trial, label, [(f"{label} {year}", []) for year in years], target
```

### `u77-b.B7_check_empty_catalog`

check_record_labels_tree: resolve the catalog tree even when nothing would be written, so an undeclared tree refuses a landing that has no label row

- File: `src/cratekit/write/trees.py`
- Source: `u77-b.json`, row `B7_check_empty_catalog`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 285 against a baseline of 285
- Kills: 2 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_an_undeclared_catalog_tree_costs_a_landing_with_no_label_row_nothing`
  - `tests/test_tree_writer.py::test_the_catalog_check_asks_nothing_when_there_is_nothing_to_write`

Old text:

```
    if not catalog:
        return
    target = _catalog_tree(declared, registry, tree)
    trial
```

New text:

```
    if catalog is None:
        return
    target = _catalog_tree(declared, registry, tree)
    trial
```

### `u77-b.B8_label_write_order`

insert_record_labels_trees: write the sources first name first, so a new tree reads Z to A

- File: `src/cratekit/write/trees.py`
- Source: `u77-b.json`, row `B8_label_write_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 285 against a baseline of 285
- Kills: 3 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_the_labelled_intake_file_golden`
  - `tests/test_landing_labels.py::test_two_labels_across_two_years_are_four_playlists_in_the_intake_file`
  - `tests/test_tree_writer.py::test_several_sources_are_one_write_and_a_new_tree_reads_a_to_z`

Old text:

```
    for label in sorted(catalog, reverse=True):
        _insert_catalog(content,
```

New text:

```
    for label in sorted(catalog):
        _insert_catalog(content,
```

### `u287-m11.M11_gone_offers_nothing`

removals: read a playlist not read whole as removing every track, measured again after the zero of the first table was given a test

- File: `src/cratekit/sync/removed.py`
- Source: `u287-m11.json`, row `M11_gone_offers_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 62 against a baseline of 62
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_synced_playlist_not_read_whole_offers_nothing_from_any_playlist[empty]`
  - `tests/test_sync_removed.py::test_a_synced_playlist_not_read_whole_offers_nothing_from_any_playlist[short]`
  - `tests/test_sync_removed.py::test_a_synced_playlist_not_read_whole_offers_nothing_from_any_playlist[unreadable]`

Old text:

```
        if one.account in reads and reads[one.account].state == READ
```

New text:

```
        if one.account in reads
```

### `u287.M10_gone_on_one_read`

read_one: read a playlist the account's list omits as gone without opening it by its id

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M10_gone_on_one_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 62 against a baseline of 62
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_damaged_job_of_another_playlist_never_refuses_the_verb[False]`
  - `tests/test_sync_removed.py::test_a_gone_downloaded_playlist_holds_what_its_pass_recorded`
  - `tests/test_sync_removed.py::test_a_gone_playlist_a_pass_swept_and_never_landed_holds_what_it_recorded`
  - `tests/test_sync_removed.py::test_a_playlist_the_account_list_omits_and_its_id_opens_is_read_and_keeps_its_tracks`
  - `tests/test_sync_removed.py::test_a_synced_playlist_nothing_records_that_neither_read_finds_offers_nothing`

Old text:

```
    name = shown.name if shown is not None else ""
```

New text:

```
    name = shown.name if shown is not None else ""
    if shown is None:
        return Listing(account=account, name=name, state=GONE, why="")
```

### `u287.M13_folder_separator`

_under: compare the folder as a bare prefix, so a sibling folder sharing its name's start reads as the pass's

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M13_folder_separator`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 62 against a baseline of 62
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_path_is_under_a_folder_only_past_a_separator_and_in_one_unicode_form`

Old text:

```
        if root and (held.startswith(root + "/") or held.startswith(root + "\\")):
```

New text:

```
        if root and held.startswith(root):
```

### `u287.M14_twin_is_own_filing`

plan_removed: leave the recorded twins out of the pass's own filing, so the landing's own twin keeps a track

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M14_twin_is_own_filing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 62 against a baseline of 62
- Kills: 30 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_commit_that_lands_and_then_raises_still_records_every_row`
  - `tests/test_sync_removed.py::test_a_damaged_job_of_another_playlist_never_refuses_the_verb[False]`
  - `tests/test_sync_removed.py::test_a_damaged_job_of_another_playlist_never_refuses_the_verb[True]`
  - `tests/test_sync_removed.py::test_a_genre_playlist_of_a_native_routing_tree_keeps_nothing`
  - `tests/test_sync_removed.py::test_a_gone_downloaded_playlist_holds_what_its_pass_recorded`
  - `tests/test_sync_removed.py::test_a_gone_playlist_a_pass_swept_and_never_landed_holds_what_it_recorded`
  - `tests/test_sync_removed.py::test_a_new_track_taken_off_is_offered_and_an_owned_one_is_kept_as_held_before`
  - `tests/test_sync_removed.py::test_a_plan_that_moved_before_the_write_refuses_with_nothing_written`
  - `tests/test_sync_removed.py::test_a_playlist_the_account_list_omits_and_its_id_opens_is_read_and_keeps_its_tracks`
  - `tests/test_sync_removed.py::test_a_playlist_the_account_says_holds_none_is_read_empty_and_every_new_track_offered`
  - `tests/test_sync_removed.py::test_a_position_the_pass_holds_is_kept_and_the_collection_not_walked`
  - `tests/test_sync_removed.py::test_a_read_back_that_disagrees_refuses_as_unverified`
  - `tests/test_sync_removed.py::test_a_refused_removal_gives_the_deletion_pass_no_position`
  - `tests/test_sync_removed.py::test_a_removed_row_the_database_holds_again_is_not_offered_by_delete_review`
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`
  - ... and 15 more, see the JSON sidecar

Old text:

```
            own = own_nodes.union(
                *(made.get(account, frozenset()) for account in held.accounts),
            )
```

New text:

```
            own = own_nodes
```

### `u287.M16_gone_holds_what_was_recorded`

Listing.holds: a gone playlist holds nothing, so a track its pass recorded on it can be offered

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M16_gone_holds_what_was_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 62 against a baseline of 62
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_gone_downloaded_playlist_holds_what_its_pass_recorded`
  - `tests/test_sync_removed.py::test_a_gone_playlist_a_pass_swept_and_never_landed_holds_what_it_recorded`
  - `tests/test_sync_removed.py::test_a_listing_holds_a_track_by_any_of_three_tests_and_only_a_read_or_gone_one_holds`

Old text:

```
        if self.state not in (READ, GONE):
```

New text:

```
        if self.state != READ:
```

### `u287.M17_gone_with_no_record_is_not_whole`

read_one: read a playlist neither read finds and nothing records as gone, holding nothing, rather than not read whole

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M17_gone_with_no_record_is_not_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 62 against a baseline of 62
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_damaged_job_of_another_playlist_never_refuses_the_verb[False]`
  - `tests/test_sync_removed.py::test_a_synced_playlist_nothing_records_that_neither_read_finds_offers_nothing`

Old text:

```
            if not known:
                return Listing(
```

New text:

```
            if False:
                return Listing(
```

### `u287.M18_set_aside_rows_count`

read_one: leave the reader's set aside rows out of the identity sets

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M18_set_aside_rows_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 62 against a baseline of 62
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_row_the_reader_set_aside_keeps_a_track_by_its_isrc`

Old text:

```
        for one in readable.unread.values()
    )
```

New text:

```
        for one in ()
    )
```

### `u287.M19_old_prefix_is_synced`

synced: leave a playlist still titled with the retired swept prefix out of the synced set

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M19_old_prefix_is_synced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 62 against a baseline of 62
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_playlist_still_titled_with_the_old_prefix_is_synced`

Old text:

```
                    if playlists.is_swept_name(one.name)
```

New text:

```
                    if False
```

### `u287.M1_partial_read_stops_offers`

plan_removed: never read a synced listing as partial, so an unreadable, short or empty playlist or hearts no longer stops any offer

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M1_partial_read_stops_offers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 62 against a baseline of 62
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_damaged_job_of_another_playlist_never_refuses_the_verb[False]`
  - `tests/test_sync_removed.py::test_a_synced_playlist_not_read_whole_offers_nothing_from_any_playlist[empty]`
  - `tests/test_sync_removed.py::test_a_synced_playlist_not_read_whole_offers_nothing_from_any_playlist[short]`
  - `tests/test_sync_removed.py::test_a_synced_playlist_not_read_whole_offers_nothing_from_any_playlist[unreadable]`
  - `tests/test_sync_removed.py::test_a_synced_playlist_nothing_records_that_neither_read_finds_offers_nothing`
  - `tests/test_sync_removed.py::test_hearts_not_read_whole_offer_nothing[empty]`
  - `tests/test_sync_removed.py::test_hearts_not_read_whole_offer_nothing[short]`
  - `tests/test_sync_removed.py::test_hearts_not_read_whole_offer_nothing[unreadable]`

Old text:

```
    partial = any(one.state in NOT_WHOLE for one in listings)
```

New text:

```
    partial = False
```

### `u287.M20_unreadable_record_is_not_whole`

recorded_contents: read a gone playlist whose job reports cannot be read as holding nothing recorded, refusing the verb

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M20_unreadable_record_is_not_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 62 against a baseline of 62
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_damaged_job_of_another_playlist_never_refuses_the_verb[False]`

Old text:

```
        except CratekitError:
            return None
        return tuple(found) or None
```

New text:

```
        except ZeroDivisionError:
            return None
        return tuple(found) or None
```

### `u287.M2_held_by_isrc`

Listing.holds: drop the ISRC test, so a track relisted under another id with its ISRC reads as removed

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M2_held_by_isrc`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 62 against a baseline of 62
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_listing_holds_a_track_by_any_of_three_tests_and_only_a_read_or_gone_one_holds`
  - `tests/test_sync_removed.py::test_a_row_the_reader_set_aside_keeps_a_track_by_its_isrc`
  - `tests/test_sync_removed.py::test_a_track_still_on_another_synced_playlist_is_kept_by_id_isrc_and_recording`

Old text:

```
        if wanted.isrc and wanted.isrc.strip().upper() in self.isrcs:
```

New text:

```
        if False and wanted.isrc and wanted.isrc.strip().upper() in self.isrcs:
```

### `u287.M3_held_by_recording`

Listing.holds: drop the folded recording test, so a relinked track with its artist and title reads as removed

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M3_held_by_recording`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 62 against a baseline of 62
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_listing_holds_a_track_by_any_of_three_tests_and_only_a_read_or_gone_one_holds`
  - `tests/test_sync_removed.py::test_a_track_still_on_another_synced_playlist_is_kept_by_id_isrc_and_recording`

Old text:

```
        return recording(wanted) in self.recordings
```

New text:

```
        return False
```

### `u287.M4_held_before_the_pass`

_answer: drop the held before the pass keep, so a track the library owned when the job ran can be offered

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M4_held_before_the_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 62 against a baseline of 62
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_new_track_taken_off_is_offered_and_an_owned_one_is_kept_as_held_before`
  - `tests/test_sync_removed.py::test_a_playlist_the_account_says_holds_none_is_read_empty_and_every_new_track_offered`

Old text:

```
    if not held.carried:
        return replace(shown, why=HELD_BEFORE)
```

New text:

```
    if False:
        return replace(shown, why=HELD_BEFORE)
```

### `u287.M5_not_this_pass_file`

_answer: drop the filed folder keep, so a hand brought file the match found can be offered

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M5_not_this_pass_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 62 against a baseline of 62
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_file_another_pass_filed_is_not_this_pass_s_file`
  - `tests/test_sync_removed.py::test_a_match_on_a_file_the_pass_did_not_file_is_kept`

Old text:

```
    if not held.brought:
        return replace(shown, why=NOT_THIS_PASS)
```

New text:

```
    if False:
        return replace(shown, why=NOT_THIS_PASS)
```

### `u287.M6_on_another_synced`

_answer: drop the still on another synced playlist keep

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M6_on_another_synced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 62 against a baseline of 62
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_gone_downloaded_playlist_holds_what_its_pass_recorded`
  - `tests/test_sync_removed.py::test_a_gone_playlist_a_pass_swept_and_never_landed_holds_what_it_recorded`
  - `tests/test_sync_removed.py::test_a_playlist_a_later_pass_swept_and_never_landed_still_keeps_its_tracks`
  - `tests/test_sync_removed.py::test_a_playlist_still_titled_with_the_old_prefix_is_synced`
  - `tests/test_sync_removed.py::test_a_playlist_the_account_list_omits_and_its_id_opens_is_read_and_keeps_its_tracks`
  - `tests/test_sync_removed.py::test_a_row_the_reader_set_aside_keeps_a_track_by_its_isrc`
  - `tests/test_sync_removed.py::test_a_track_hearted_on_the_account_is_kept_by_the_hearts`
  - `tests/test_sync_removed.py::test_a_track_still_on_another_synced_playlist_is_kept_by_id_isrc_and_recording`

Old text:

```
    if still:
        return replace(shown, why=ON_ANOTHER, kept_by=still)
```

New text:

```
    if False:
        return replace(shown, why=ON_ANOTHER, kept_by=still)
```

### `u287.M7_in_a_playlist_of_yours`

_answer: drop the playlist of yours keep, so a track in a hand made playlist or All Favorites can be offered

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M7_in_a_playlist_of_yours`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 62 against a baseline of 62
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_genre_playlist_of_a_native_routing_tree_keeps_nothing`
  - `tests/test_sync_removed.py::test_a_plan_that_moved_before_the_write_refuses_with_nothing_written`
  - `tests/test_sync_removed.py::test_a_track_in_a_playlist_of_yours_is_kept_and_its_own_filing_keeps_nothing`

Old text:

```
    if yours:
        return replace(shown, why=IN_YOURS, kept_by=yours)
```

New text:

```
    if False:
        return replace(shown, why=IN_YOURS, kept_by=yours)
```

### `u287.M8_empty_read_untrusted`

read_one: trust an empty read with an unknown count, so a provider fault reads every track removed

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M8_empty_read_untrusted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 62 against a baseline of 62
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_synced_playlist_not_read_whole_offers_nothing_from_any_playlist[empty]`

Old text:

```
    if not readable.order and (shown is None or shown.tracks != 0):
```

New text:

```
    if False:
```

### `u287.M9_short_read_untrusted`

read_one: trust a listing short of its declared count

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M9_short_read_untrusted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 62 against a baseline of 62
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_synced_playlist_not_read_whole_offers_nothing_from_any_playlist[short]`

Old text:

```
    if readable.short is not None:
        block = readable.short.block()
```

New text:

```
    if False:
        block = readable.short.block()
```

### `u288.M16_stale_digest`

apply_removed: never refuse a plan that moved between the gate and the write

- File: `src/cratekit/sync/removed.py`
- Source: `u288.json`, row `M16_stale_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 62 against a baseline of 62
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_plan_that_moved_before_the_write_refuses_with_nothing_written`

Old text:

```
    if again.digest != plan.digest:
```

New text:

```
    if False:
```

### `u288.M17_only_the_offered`

apply_removed: take out every answered row that has one, kept rows included, not only the offered

- File: `src/cratekit/sync/removed.py`
- Source: `u288.json`, row `M17_only_the_offered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 62 against a baseline of 62
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_commit_that_lands_and_then_raises_still_records_every_row`
  - `tests/test_sync_removed.py::test_a_removed_row_the_database_holds_again_is_not_offered_by_delete_review`
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`
  - `tests/test_sync_removed.py::test_apply_takes_out_exactly_the_offered_rows_and_every_row_naming_them`
  - `tests/test_sync_removed.py::test_delete_review_after_the_apply_offers_the_removed_file_and_none_other`
  - `tests/test_sync_removed.py::test_the_removal_writes_no_beat_grid_and_no_tempo`
  - `tests/test_sync_removed.py::test_the_session_record_names_every_row_removed_and_restore_list_reads_it`

Old text:

```
    offered = plan.offered
    if not offered:
```

New text:

```
    offered = tuple(one for one in plan.answers if one.content_id)
    if not offered:
```

### `u288.M18_unmeasured_kept`

_answer: drop the keep of a row an unmeasured table names, so a vox tagged track is offered and then refuses the apply

- File: `src/cratekit/sync/removed.py`
- Source: `u288.json`, row `M18_unmeasured_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 62 against a baseline of 62
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`

Old text:

```
    if unmeasured:
        return replace(shown, why=UNMEASURED, kept_by=tuple(sorted(unmeasured)))
```

New text:

```
    if False:
        return replace(shown, why=UNMEASURED, kept_by=tuple(sorted(unmeasured)))
```

### `u288.M19_first_position`

apply_removed: give the deletion pass no first position, so a first delete review accepts the removal as history

- File: `src/cratekit/sync/removed.py`
- Source: `u288.json`, row `M19_first_position`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 62 against a baseline of 62
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_delete_review_after_the_apply_offers_the_removed_file_and_none_other`

Old text:

```
        first = _first_deletion_position(cfg, db)
```

New text:

```
        first = None
```

### `u288.M20_read_back_refusal`

apply_removed: report a read back that disagrees as success

- File: `src/cratekit/sync/removed.py`
- Source: `u288.json`, row `M20_read_back_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 62 against a baseline of 62
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_read_back_that_disagrees_refuses_as_unverified`

Old text:

```
        violations = removal.read_back()
        if violations:
```

New text:

```
        violations = removal.read_back()
        if False:
```

### `u288.M14_confinement_not_called`

CollectionRemoval.commit: skip the SQL confinement before the commit

- File: `src/cratekit/core/rb_writer.py`
- Source: `u288.json`, row `M14_confinement_not_called`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 62 against a baseline of 62
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_commit_proves_the_removal_confined_before_it_commits`

Old text:

```
        assert_collection_removal_confined(self.db, self.before, removed=self.content_ids)
        commit_guarded(
```

New text:

```
        commit_guarded(
```

### `u288.M3_unmeasured_tables_skipped`

content_references: ask no table, so a My Tag, sampler or unknown table naming the row is never refused nor kept

- File: `src/cratekit/core/rb_writer.py`
- Source: `u288.json`, row `M3_unmeasured_tables_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 62 against a baseline of 62
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`
  - `tests/test_sync_removed.py::test_the_writer_refuses_a_row_an_unmeasured_table_names_with_nothing_written[CREATE TABLE "someFutureTable" (ID TEXT PRIMARY KEY, ContentID TEXT)-INSERT INTO "someFutureTable" (ID, ContentID) VALUES ('x-1', ?)]`
  - `tests/test_sync_removed.py::test_the_writer_refuses_a_row_an_unmeasured_table_names_with_nothing_written[None-INSERT INTO "djmdSongSampler" (ID, ContentID) VALUES ('x-1', ?)]`

Old text:

```
        asked = [CONTENT_REFERENCE_COLUMN] if CONTENT_REFERENCE_COLUMN in names else []
```

New text:

```
        asked = []
```

### `u288.M4_target_id_not_asked`

content_references: drop the TargetID column, so an image row naming the track is left naming a row that is gone

- File: `src/cratekit/core/rb_writer.py`
- Source: `u288.json`, row `M4_target_id_not_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 62 against a baseline of 62
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_the_writer_refuses_a_row_an_unmeasured_table_names_with_nothing_written[None-INSERT INTO "imageFile" (ID, TargetID) VALUES ('x-1', ?)]`

Old text:

```
        if TARGET_REFERENCE_COLUMN in names:
```

New text:

```
        if False:
```

### `u288.M5_prepare_liveness`

CollectionRemoval.prepare: drop the soft delete check, so a row rekordbox already removed is taken out as live

- File: `src/cratekit/core/rb_writer.py`
- Source: `u288.json`, row `M5_prepare_liveness`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 62 against a baseline of 62
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_prepare_refuses_a_row_not_live_and_a_database_with_no_identity`

Old text:

```
            if row is None or soft_deleted(
                row,
                message=(
                    f"the collection row {key!r} cannot say whether rekordbox removed it, "
```

New text:

```
            if row is None or False and soft_deleted(
                row,
                message=(
                    f"the collection row {key!r} cannot say whether rekordbox removed it, "
```

### `u288.M6_prepare_unmeasured_refusal`

CollectionRemoval.prepare: drop the refusal of a row an unmeasured table names

- File: `src/cratekit/core/rb_writer.py`
- Source: `u288.json`, row `M6_prepare_unmeasured_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 62 against a baseline of 62
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_the_writer_refuses_a_row_an_unmeasured_table_names_with_nothing_written[CREATE TABLE "someFutureTable" (ID TEXT PRIMARY KEY, ContentID TEXT)-INSERT INTO "someFutureTable" (ID, ContentID) VALUES ('x-1', ?)]`
  - `tests/test_sync_removed.py::test_the_writer_refuses_a_row_an_unmeasured_table_names_with_nothing_written[None-INSERT INTO "djmdSongSampler" (ID, ContentID) VALUES ('x-1', ?)]`
  - `tests/test_sync_removed.py::test_the_writer_refuses_a_row_an_unmeasured_table_names_with_nothing_written[None-INSERT INTO "imageFile" (ID, TargetID) VALUES ('x-1', ?)]`

Old text:

```
        held = content_references(db, ids)
        if held:
```

New text:

```
        held = content_references(db, ids)
        if False:
```

### `u288.M7_prepare_identity`

CollectionRemoval.prepare: drop the refusal of a database with no identity, so the record is bound to nothing

- File: `src/cratekit/core/rb_writer.py`
- Source: `u288.json`, row `M7_prepare_identity`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 62 against a baseline of 62
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_prepare_refuses_a_row_not_live_and_a_database_with_no_identity`

Old text:

```
        identity = database_id(db)
        if not identity:
```

New text:

```
        identity = database_id(db)
        if False:
```

### `u288.M8_memberships_kept`

remove_from_collection: delete from the five tables after the membership table only, so the track's memberships stay naming a row that is gone

- File: `src/cratekit/core/rb_writer.py`
- Source: `u288.json`, row `M8_memberships_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 62 against a baseline of 62
- Kills: 11 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_commit_that_lands_and_then_raises_still_records_every_row`
  - `tests/test_sync_removed.py::test_a_position_the_pass_holds_is_kept_and_the_collection_not_walked`
  - `tests/test_sync_removed.py::test_a_read_back_that_disagrees_refuses_as_unverified`
  - `tests/test_sync_removed.py::test_a_removal_that_changes_anything_it_did_not_plan_is_refused_before_its_commit`
  - `tests/test_sync_removed.py::test_a_removed_row_the_database_holds_again_is_not_offered_by_delete_review`
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`
  - `tests/test_sync_removed.py::test_apply_takes_out_exactly_the_offered_rows_and_every_row_naming_them`
  - `tests/test_sync_removed.py::test_commit_proves_the_removal_confined_before_it_commits`
  - `tests/test_sync_removed.py::test_delete_review_after_the_apply_offers_the_removed_file_and_none_other`
  - `tests/test_sync_removed.py::test_the_removal_writes_no_beat_grid_and_no_tempo`
  - `tests/test_sync_removed.py::test_the_session_record_names_every_row_removed_and_restore_list_reads_it`

Old text:

```
    for table in COLLECTION_REMOVAL_TABLES[1:]:
```

New text:

```
    for table in COLLECTION_REMOVAL_TABLES[2:]:
```

### `u255.C4_held_before_read_and_playlist_keeps_the_hold`

M4 with _playlist's drop removed too: a failed tracks read leaves the opened object held, and the next membership read reuses nothing that drops it, drive H of round one

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `C4_held_before_read_and_playlist_keeps_the_hold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 330 against a baseline of 330
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_an_open_that_fails_is_refused_on_its_own_retry_before_any_add_is_sent`
  - `tests/test_outbound_add_requests.py::test_another_write_through_the_adapter_drops_the_hold`

Old text:

```
        self._opened.pop(playlist_id, None)
        found = self._call(
            f"open the playlist {playlist_id}",
            lambda: self._session.playlist(playlist_id),
        )
        if found is _ABSENT or found is None:
            raise account.provider_failure(
                LookupError(f"the provider has no playlist {playlist_id!r}"),
                f"open the playlist {playlist_id}",
            )
        return found

    def _listed(self, playlist_id: str, playlist: Any) -> list[Any]:
        """Every track object on the playlist, in order, read now across pages."""
        return self._read(
            f"read the playlist {playlist_id}",
            lambda: listing.playlist_tracks(playlist),
        )

    def _held(self, playlist_id: str) -> Any:
        """The playlist's held object, opened through :meth:`_playlist` only if none is held.

        ONE OPEN FOR A RUN OF ADDS, NOT ONE PER ADD (U255). Opening a playlist
        the account owns is two GETs, since the client fetches it as a
        ``Playlist`` and then again as the ``UserPlaylist`` its factory builds,
        and the client's own add reads the playlist once more after its POST
        for the 
... truncated ...
```

New text:

```
        found = self._call(
            f"open the playlist {playlist_id}",
            lambda: self._session.playlist(playlist_id),
        )
        if found is _ABSENT or found is None:
            raise account.provider_failure(
                LookupError(f"the provider has no playlist {playlist_id!r}"),
                f"open the playlist {playlist_id}",
            )
        return found

    def _listed(self, playlist_id: str, playlist: Any) -> list[Any]:
        """Every track object on the playlist, in order, read now across pages."""
        return self._read(
            f"read the playlist {playlist_id}",
            lambda: listing.playlist_tracks(playlist),
        )

    def _held(self, playlist_id: str) -> Any:
        """The playlist's held object, opened through :meth:`_playlist` only if none is held.

        ONE OPEN FOR A RUN OF ADDS, NOT ONE PER ADD (U255). Opening a playlist
        the account owns is two GETs, since the client fetches it as a
        ``Playlist`` and then again as the ``UserPlaylist`` its factory builds,
        and the client's own add reads the playlist once more after its POST
        for the next version tag. An add that opened afresh 
... truncated ...
```

### `u255.C8_no_open_before_and_retry_opens_raw`

M8 with the attempt's open made raw through the session: the first open then rides inside the add's attempts with no retry or refusal of its own

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `C8_no_open_before_and_retry_opens_raw`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 330 against a baseline of 330
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_an_add_refused_for_a_stale_tag_is_sent_once_more_on_a_fresh_open_and_lands`
  - `tests/test_outbound_add_requests.py::test_an_open_that_fails_is_refused_on_its_own_retry_before_any_add_is_sent`
  - `tests/test_outbound_add_requests.py::test_the_retrys_open_has_a_retry_of_its_own`

Old text:

```
        self._held(playlist_id)
        doing = f"add the track {identifier} to the playlist {playlist_id}"

        def attempt() -> Any:
            playlist = self._opened.get(playlist_id)
            if playlist is None:
                playlist = self._held(playlist_id)
            try:
```

New text:

```
        doing = f"add the track {identifier} to the playlist {playlist_id}"

        def attempt() -> Any:
            playlist = self._opened.get(playlist_id)
            if playlist is None:
                playlist = self._session.playlist(playlist_id)
            try:
```

### `u255.M10_failed_attempt_keeps_the_hold`

add_to_playlist attempt: keep the held object after a failed add, so the retry resends the refused tag

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `M10_failed_attempt_keeps_the_hold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 330 against a baseline of 330
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_a_refused_add_drops_the_hold_so_the_next_track_opens_afresh`
  - `tests/test_outbound_add_requests.py::test_a_track_added_elsewhere_meanwhile_lands_once_and_is_read_back`
  - `tests/test_outbound_add_requests.py::test_a_write_between_the_open_and_the_tracks_read_never_puts_the_add_before_it`
  - `tests/test_outbound_add_requests.py::test_an_add_refused_for_a_stale_tag_is_sent_once_more_on_a_fresh_open_and_lands`
  - `tests/test_outbound_add_requests.py::test_the_retrys_open_has_a_retry_of_its_own`

Old text:

```
            except Exception:
                self._opened.pop(playlist_id, None)
                raise
```

New text:

```
            except Exception:
                raise
```

### `u255.M11_retry_opens_raw`

add_to_playlist attempt: the retry opens through the session with no retry of its own and no hold, round one's finding three

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `M11_retry_opens_raw`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 330 against a baseline of 330
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_an_add_refused_for_a_stale_tag_is_sent_once_more_on_a_fresh_open_and_lands`
  - `tests/test_outbound_add_requests.py::test_the_retrys_open_has_a_retry_of_its_own`

Old text:

```
                playlist = self._held(playlist_id)
            try:
```

New text:

```
                playlist = self._session.playlist(playlist_id)
            try:
```

### `u255.M12_add_never_retried`

add_to_playlist: no retry at all, so a 412 on a stale held tag fails the item

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `M12_add_never_retried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 330 against a baseline of 330
- Kills: 7 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_a_playlist_read_one_write_behind_writes_nothing`
  - `tests/test_outbound_add_requests.py::test_a_track_added_elsewhere_meanwhile_lands_once_and_is_read_back`
  - `tests/test_outbound_add_requests.py::test_a_write_between_the_open_and_the_tracks_read_never_puts_the_add_before_it`
  - `tests/test_outbound_add_requests.py::test_an_add_refused_for_a_stale_tag_is_sent_once_more_on_a_fresh_open_and_lands`
  - `tests/test_outbound_add_requests.py::test_an_add_refused_twice_fails_the_item_with_nothing_more_sent[412]`
  - `tests/test_outbound_add_requests.py::test_an_add_refused_twice_fails_the_item_with_nothing_more_sent[503]`
  - `tests/test_outbound_add_requests.py::test_the_retrys_open_has_a_retry_of_its_own`

Old text:

```
        added = self._call(doing, attempt)
```

New text:

```
        added = self._call(doing, attempt, retries=0)
```

### `u255.M13_add_retried_twice`

add_to_playlist: two retries, more than the policy allows a write

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `M13_add_retried_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 330 against a baseline of 330
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_a_playlist_read_one_write_behind_writes_nothing`
  - `tests/test_outbound_add_requests.py::test_an_add_refused_twice_fails_the_item_with_nothing_more_sent[412]`
  - `tests/test_outbound_add_requests.py::test_an_add_refused_twice_fails_the_item_with_nothing_more_sent[503]`

Old text:

```
        added = self._call(doing, attempt)
```

New text:

```
        added = self._call(doing, attempt, retries=2)
```

### `u255.M1_playlist_keeps_the_hold`

_playlist: drop nothing, so a member that opens and writes through its own object leaves the held one stale

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `M1_playlist_keeps_the_hold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 330 against a baseline of 330
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_an_open_that_fails_is_refused_on_its_own_retry_before_any_add_is_sent`
  - `tests/test_outbound_add_requests.py::test_another_write_through_the_adapter_drops_the_hold`

Old text:

```
        self._opened.pop(playlist_id, None)
        found = self._call(
```

New text:

```
        found = self._call(
```

### `u255.M2_membership_reads_the_held_object`

_membership: read the tracks through the opened object itself, so the client's tracks read overwrites its tag and leaves its length, round one's BLOCKING

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `M2_membership_reads_the_held_object`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 330 against a baseline of 330
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_a_playlist_read_one_write_behind_writes_nothing`
  - `tests/test_outbound_add_requests.py::test_a_tracks_read_one_write_behind_never_reaches_the_add`
  - `tests/test_outbound_add_requests.py::test_a_write_between_the_open_and_the_tracks_read_never_puts_the_add_before_it`

Old text:

```
            tracks = self._listed(playlist_id, copy.copy(opened))
```

New text:

```
            tracks = self._listed(playlist_id, opened)
```

### `u255.M3_membership_holds_nothing`

_membership: never hold the opened object, so the first add opens again, K + 4 GETs

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `M3_membership_holds_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 330 against a baseline of 330
- Kills: 6 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_a_held_playlist_never_outlives_its_adapter`
  - `tests/test_outbound_add_requests.py::test_a_write_between_the_open_and_the_tracks_read_never_puts_the_add_before_it`
  - `tests/test_outbound_add_requests.py::test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts[100]`
  - `tests/test_outbound_add_requests.py::test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts[10]`
  - `tests/test_outbound_add_requests.py::test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts[1]`
  - `tests/test_outbound_add_requests.py::test_two_playlists_added_to_in_turn_each_keep_their_own_held_object`

Old text:

```
            ]
            self._opened[playlist_id] = opened

```

New text:

```
            ]

```

### `u255.M5_membership_reuses_the_hold`

_membership: read through a held object when one is held, so the read back of an answer without the track reads a held object, not a fresh open

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `M5_membership_reuses_the_hold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 330 against a baseline of 330
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_an_add_answered_without_the_track_reads_the_playlist_back_and_refuses`

Old text:

```
            opened = self._playlist(playlist_id)

```

New text:

```
            opened = self._opened.get(playlist_id) or self._playlist(playlist_id)

```

### `u255.M6_held_never_stores`

_held: open without holding, so the retry's fresh object is not kept and the next add opens again

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `M6_held_never_stores`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 330 against a baseline of 330
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_a_refused_add_drops_the_hold_so_the_next_track_opens_afresh`
  - `tests/test_outbound_add_requests.py::test_an_add_refused_for_a_stale_tag_is_sent_once_more_on_a_fresh_open_and_lands`
  - `tests/test_outbound_add_requests.py::test_another_write_through_the_adapter_drops_the_hold`

Old text:

```
            self._opened[playlist_id] = held

```

New text:

```
(empty)
```

### `u255.M7_held_always_opens`

_held: ignore what is held and open every time

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `M7_held_always_opens`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 330 against a baseline of 330
- Kills: 9 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_a_held_playlist_never_outlives_its_adapter`
  - `tests/test_outbound_add_requests.py::test_a_write_between_the_open_and_the_tracks_read_never_puts_the_add_before_it`
  - `tests/test_outbound_add_requests.py::test_an_add_answered_without_the_track_reads_the_playlist_back_and_refuses`
  - `tests/test_outbound_add_requests.py::test_an_add_refused_for_a_stale_tag_is_sent_once_more_on_a_fresh_open_and_lands`
  - `tests/test_outbound_add_requests.py::test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts[100]`
  - `tests/test_outbound_add_requests.py::test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts[10]`
  - `tests/test_outbound_add_requests.py::test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts[1]`
  - `tests/test_outbound_add_requests.py::test_the_retrys_open_has_a_retry_of_its_own`
  - `tests/test_outbound_add_requests.py::test_two_playlists_added_to_in_turn_each_keep_their_own_held_object`

Old text:

```
        held = self._opened.get(playlist_id)

```

New text:

```
        held = None

```

### `u255.M9_every_attempt_opens`

add_to_playlist attempt: open afresh for every add, today's four requests a track

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `M9_every_attempt_opens`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 330 against a baseline of 330
- Kills: 11 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_a_held_playlist_never_outlives_its_adapter`
  - `tests/test_outbound_add_requests.py::test_a_refused_add_drops_the_hold_so_the_next_track_opens_afresh`
  - `tests/test_outbound_add_requests.py::test_a_write_between_the_open_and_the_tracks_read_never_puts_the_add_before_it`
  - `tests/test_outbound_add_requests.py::test_an_add_answered_without_the_track_reads_the_playlist_back_and_refuses`
  - `tests/test_outbound_add_requests.py::test_an_add_refused_for_a_stale_tag_is_sent_once_more_on_a_fresh_open_and_lands`
  - `tests/test_outbound_add_requests.py::test_another_write_through_the_adapter_drops_the_hold`
  - `tests/test_outbound_add_requests.py::test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts[100]`
  - `tests/test_outbound_add_requests.py::test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts[10]`
  - `tests/test_outbound_add_requests.py::test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts[1]`
  - `tests/test_outbound_add_requests.py::test_the_retrys_open_has_a_retry_of_its_own`
  - `tests/test_outbound_add_requests.py::test_two_playlists_added_to_in_turn_each_keep_their_own_held_object`

Old text:

```
            playlist = self._opened.get(playlist_id)
            if playlist is None:
                playlist = self._held(playlist_id)
```

New text:

```
            playlist = self._playlist(playlist_id)
            if playlist is None:
                playlist = self._held(playlist_id)
```

### `u255.S1_member_already_on`

add_to_playlist: send the add for a track the membership already holds, an existing guard

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `S1_member_already_on`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 330 against a baseline of 330
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_a_track_already_on_the_playlist_makes_no_request_at_all`
  - `tests/test_outbound_tidal_account.py::test_a_member_already_on_the_playlist_makes_no_write`

Old text:

```
        if identifier in members:
            return
        self._held
```

New text:

```
        if False:
            return
        self._held
```

### `u255.S2_read_back_trusts_the_cache`

add_to_playlist: an answer without the track is checked against the cached membership, not read back, an existing guard

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `S2_read_back_trusts_the_cache`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 330 against a baseline of 330
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_a_track_added_elsewhere_meanwhile_lands_once_and_is_read_back`
  - `tests/test_outbound_add_requests.py::test_an_add_answered_without_the_track_reads_the_playlist_back_and_refuses`
  - `tests/test_outbound_tidal_account.py::test_an_empty_answer_for_a_track_the_playlist_now_holds_is_not_a_failure`

Old text:

```
            del self._members[playlist_id]
            if identifier not in self._membership(playlist_id):
```

New text:

```
            if identifier not in self._membership(playlist_id):
```

### `u255.S3_answer_absent_passes`

add_to_playlist: a playlist gone mid add is not refused, an existing guard

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `S3_answer_absent_passes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 330 against a baseline of 330
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_an_add_to_a_playlist_deleted_mid_run_is_the_items_cause`

Old text:

```
        if added is _ABSENT:
            raise account.provider_failure(
                LookupError(f"the provider no longer has the playlist {playlist_id!r}"),
```

New text:

```
        if False:
            raise account.provider_failure(
                LookupError(f"the provider no longer has the playlist {playlist_id!r}"),
```

### `u255.S4_added_not_remembered`

add_to_playlist: a landed add is not appended to the membership, an existing guard

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `S4_added_not_remembered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 330 against a baseline of 330
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_a_write_between_the_open_and_the_tracks_read_never_puts_the_add_before_it`
  - `tests/test_outbound_add_requests.py::test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts[100]`
  - `tests/test_outbound_add_requests.py::test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts[10]`
  - `tests/test_outbound_add_requests.py::test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts[1]`
  - `tests/test_outbound_tidal_account.py::test_a_member_already_on_the_playlist_makes_no_write`

Old text:

```
            return
        members.append(identifier)

```

New text:

```
            return

```

### `u99-b.B1_parser_limit_floor`

positive_limit: accept zero at the parser, so --track-limit 0 reaches the store

- File: `src/cratekit/label/cli.py`
- Source: `u99-b.json`, row `B1_parser_limit_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_a_track_limit_below_one_refuses_at_the_parser[0]`

Old text:

```
    if value < 1:
        raise ValueError(f"{text!r} is not a positive track limit")
```

New text:

```
    if value < 0:
        raise ValueError(f"{text!r} is not a positive track limit")
```

### `u99-b.B5_add_drops_seeds`

registry_cmd add: pass no seeds to the store, so --seed on add is accepted and never written

- File: `src/cratekit/label/cli.py`
- Source: `u99-b.json`, row `B5_add_drops_seeds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 11 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_a_malformed_id_seed_on_a_new_label_creates_no_entry`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[   ]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[ID:12]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id: 12]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id:-4]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id:12a]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id:]`
  - `tests/test_label_registry_verbs.py::test_a_name_seed_that_merely_contains_id_is_stored`
  - `tests/test_label_registry_verbs.py::test_an_add_with_a_limit_and_two_seeds_round_trips_through_list`
  - `tests/test_label_registry_verbs.py::test_list_shows_the_limit_and_the_seeds_to_a_person`
  - `tests/test_label_registry_verbs.py::test_set_changes_one_field_and_keeps_the_rest`

Old text:

```
            seed_artists=tuple(seeds or ()),
```

New text:

```
            seed_artists=(),
```

### `u99-b.B6_add_drops_limit`

registry_cmd add: pass no track limit to the store, so --track-limit on add is accepted and never written

- File: `src/cratekit/label/cli.py`
- Source: `u99-b.json`, row `B6_add_drops_limit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_an_add_with_a_limit_and_two_seeds_round_trips_through_list`
  - `tests/test_label_registry_verbs.py::test_list_shows_the_limit_and_the_seeds_to_a_person`
  - `tests/test_label_registry_verbs.py::test_set_seeds_replaces_the_list_and_keeps_the_limit`

Old text:

```
            seed_artists=tuple(seeds or ()),
            track_limit=track_limit,
```

New text:

```
            seed_artists=tuple(seeds or ()),
            track_limit=None,
```

### `u99-b.B7_set_drops_seeds`

registry_cmd set: pass no seeds to edit, so set --seed reports an edit and writes nothing

- File: `src/cratekit/label/cli.py`
- Source: `u99-b.json`, row `B7_set_drops_seeds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_a_malformed_id_seed_on_set_refuses_and_writes_nothing`
  - `tests/test_label_registry_verbs.py::test_set_seeds_replaces_the_list_and_keeps_the_limit`

Old text:

```
            seed_artists=seeds,
            track_limit=track_limit,
```

New text:

```
            seed_artists=None,
            track_limit=track_limit,
```

### `u99-b.B8_list_json_empty`

registry_cmd list: report an empty summary.labels, so a reader that is not a person sees no fields

- File: `src/cratekit/label/cli.py`
- Source: `u99-b.json`, row `B8_list_json_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 12 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[   ]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[ID:12]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id: 12]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id:-4]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id:12a]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id:]`
  - `tests/test_label_registry_verbs.py::test_a_name_seed_that_merely_contains_id_is_stored`
  - `tests/test_label_registry_verbs.py::test_an_add_with_a_limit_and_two_seeds_round_trips_through_list`
  - `tests/test_label_registry_verbs.py::test_set_changes_one_field_and_keeps_the_rest`
  - `tests/test_label_registry_verbs.py::test_set_finds_an_accented_name_typed_in_decomposed_form`
  - `tests/test_label_registry_verbs.py::test_set_on_an_unknown_label_refuses_by_name_and_creates_nothing`
  - `tests/test_label_registry_verbs.py::test_set_seeds_replaces_the_list_and_keeps_the_limit`

Old text:

```
"labels": _labels_json(held)},
```

New text:

```
"labels": []},
```

### `u99-b.B9_detail_drops_seeds`

_detail: leave the seeds out of the check detail a person reads

- File: `src/cratekit/label/cli.py`
- Source: `u99-b.json`, row `B9_detail_drops_seeds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_list_shows_the_limit_and_the_seeds_to_a_person`

Old text:

```
        parts.append("seeds " + " | ".join(entry.seed_artists))
```

New text:

```
        pass
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
- Collected: 22663 against a baseline of 22663
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

### `r923.N11_digest_drops_items`

The digest no longer covers the rows and columns the plan fills

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N11_digest_drops_items`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_the_digest_moves_when_a_planned_column_is_filled_elsewhere`
  - `tests/test_repair_rows.py::test_the_digest_moves_when_a_random_id_is_replaced_elsewhere`

Old text:

```
                "items": [item.to_json() for item in self.items],
```

New text:

```
                "items": [],
```

