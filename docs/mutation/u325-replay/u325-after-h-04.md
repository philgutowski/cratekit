# Mutation table: u325-after-h-04

Measured by `scripts/mutate.py` on 2026-11-23 01:32 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 53.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 16:29 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 12, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r431-a.A6_a_standing_companion_is_rewritten` | `src/cratekit/core/review.py` | maintainer | 20 file(s) | 3066 | 1 | killed |
| `r431-a.A7_beside_written_when_the_record_stood` | `src/cratekit/core/review.py` | user | 20 file(s) | 3066 | 2 | killed |
| `r431-a.A8_also_is_never_asked` | `src/cratekit/core/review.py` | user | 20 file(s) | 3066 | 6 | killed |
| `r431-a.A9_an_already_lifted_record_is_lifted_again` | `src/cratekit/core/review.py` | maintainer | 20 file(s) | 3066 | 1 | killed |
| `u127.W1_writable_always` | `src/cratekit/core/rb_writer.py` | user | 52 file(s) | 4352 | 1 | killed |
| `u127.W2_writable_reason_drift` | `src/cratekit/core/rb_writer.py` | user | 52 file(s) | 4352 | 1 | killed |
| `r83-round-2.I1_fold_case` | `src/cratekit/core/preflight.py` | user | 15 file(s) | 2840 | 19 | killed |
| `r83-round-2.I3_configured_compare_exact` | `src/cratekit/core/preflight.py` | user | 15 file(s) | 2840 | 2 | killed |
| `r83-round-2.I4_elsewhere_compare_exact` | `src/cratekit/core/preflight.py` | user | 15 file(s) | 2840 | 1 | killed |
| `u293.N1_no_answer` | `src/cratekit/cli/sync_night.py` | user | 3 file(s) | 1068 | 4 | killed |
| `u293.N2_rekordbox_refused` | `src/cratekit/cli/sync_night.py` | user | 3 file(s) | 1068 | 3 | killed |
| `u293.N3_live_job_refused` | `src/cratekit/cli/sync_night.py` | user | 3 file(s) | 1068 | 1 | killed |
| `u293.N4_occupied_refused` | `src/cratekit/cli/sync_night.py` | user | 3 file(s) | 1068 | 4 | killed |
| `u293.N5_owed_kept` | `src/cratekit/cli/sync_night.py` | user | 3 file(s) | 1068 | 3 | killed |
| `u293.N6_settled_by_landing` | `src/cratekit/cli/sync_night.py` | user | 3 file(s) | 1068 | 1 | killed |
| `u293.N7_unread_landing_is_not_settled` | `src/cratekit/cli/sync_night.py` | user | 3 file(s) | 1068 | 1 | killed |
| `u212.T1_reason_guard` | `src/cratekit/cli/tail.py` | maintainer | 11 file(s) | 1607 | 1 | killed |
| `u212.T2_done_only` | `src/cratekit/cli/tail.py` | user | 11 file(s) | 1607 | 1 | killed |
| `u212.T3_library` | `src/cratekit/cli/tail.py` | user | 11 file(s) | 1607 | 1 | killed |
| `u212.T4_earliest_first` | `src/cratekit/cli/tail.py` | user | 11 file(s) | 1607 | 1 | killed |
| `u212.T5_name_wraps` | `src/cratekit/cli/tail.py` | user | 11 file(s) | 1607 | 2 | killed |
| `u282.T1_question_asked_with_a_picture` | `src/cratekit/tagging/tag.py` | user | 9 file(s) | 1463 | 2 | killed |
| `u282.T2_question_never_asked` | `src/cratekit/tagging/tag.py` | user | 9 file(s) | 1463 | 5 | killed |
| `u282.T3_failed_question_raises` | `src/cratekit/tagging/tag.py` | user | 9 file(s) | 1463 | 1 | killed |
| `u282.T4_failed_question_result_dropped` | `src/cratekit/tagging/tag.py` | user | 9 file(s) | 1463 | 1 | killed |
| `u289.C1_record_drops_asked` | `src/cratekit/tagging/cli.py` | user | 8 file(s) | 1430 | 1 | killed |
| `u289.T1_title_tag_split` | `src/cratekit/tagging/tag.py` | user | 8 file(s) | 1430 | 1 | killed |
| `u289.T2_split_artist_dropped` | `src/cratekit/tagging/tag.py` | user | 8 file(s) | 1430 | 4 | killed |
| `u289.T3_record_read_from_title` | `src/cratekit/tagging/tag.py` | user | 8 file(s) | 1430 | 3 | killed |
| `r289-b.D1_no_chunking` | `src/cratekit/core/jobs.py` | user | 30 file(s) | 2552 | 1 | killed |
| `r289-b.D3_unknown_name_gets_a_state` | `src/cratekit/core/jobs.py` | user | 30 file(s) | 2552 | 2 | killed |
| `u221.R21_unknown_name_not_refused` | `src/cratekit/sync/release_cli.py` | user | 2 file(s) | 1029 | 1 | killed |
| `u221.R22_all_beside_names` | `src/cratekit/sync/release_cli.py` | user | 2 file(s) | 1029 | 1 | killed |
| `u221.R23_nothing_named` | `src/cratekit/sync/release_cli.py` | user | 2 file(s) | 1029 | 1 | killed |
| `u221.R25_released_twin_asks_again` | `src/cratekit/sync/release_cli.py` | user | 2 file(s) | 1029 | 1 | killed |
| `u234.O18_snapshot_keeps_the_reading` | `src/cratekit/modules/outbound/pairs.py` | maintainer | 23 file(s) | 1765 | 4 | killed |
| `u234.O19_reading_not_written` | `src/cratekit/modules/outbound/pairs.py` | user | 23 file(s) | 1765 | 14 | killed |
| `r704-a.E2_job_verdict_needs_every_item_retryable` | `src/cratekit/core/jobs.py` | user | 33 file(s) | 2850 | 1 | killed |
| `r1724.N11_tag_one_raw_stem` | `src/cratekit/tagging/tag.py` | user | 9 file(s) | 1672 | 5 | killed |
| `r1724.N12_tag_one_tag_read` | `src/cratekit/tagging/tag.py` | user | 9 file(s) | 1672 | 1 | killed |

## Row definitions

### `r431-a.A6_a_standing_companion_is_rewritten`

beside overwrites a companion that already stands, so a second guest's deletion restamps the shared one

- File: `src/cratekit/core/review.py`
- Source: `r431-a.json`, row `A6_a_standing_companion_is_rewritten`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair.py`, `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/modules/test_reports.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_adoption.py`, `tests/test_deletion.py`, `tests/test_genre_retag.py`, `tests/test_intake_missing_search.py`, `tests/test_label_approved.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_match_states.py`, `tests/test_reports_cli.py`, `tests/test_review_queue.py`, `tests/test_tag_workers.py`, `tests/test_tombstones.py`, `tests/test_uncredited_tombstone.py`
- Collected: 3066 against a baseline of 3066
- Kills: 1 (killed)
- Killed:
  - `tests/test_uncredited_tombstone.py::test_a_second_deletion_leaves_the_shared_companion_exactly_as_it_stood`

Old text:

```
                if standing is not None and standing.suppressing:
                    continue
```

New text:

```
                if standing is None and standing is not None:
                    continue
```

### `r431-a.A7_beside_written_when_the_record_stood`

A record that already stood still writes its beside records, so a companion lifted alone comes back

- File: `src/cratekit/core/review.py`
- Source: `r431-a.json`, row `A7_beside_written_when_the_record_stood`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair.py`, `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/modules/test_reports.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_adoption.py`, `tests/test_deletion.py`, `tests/test_genre_retag.py`, `tests/test_intake_missing_search.py`, `tests/test_label_approved.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_match_states.py`, `tests/test_reports_cli.py`, `tests/test_review_queue.py`, `tests/test_tag_workers.py`, `tests/test_tombstones.py`, `tests/test_uncredited_tombstone.py`
- Collected: 3066 against a baseline of 3066
- Kills: 2 (killed)
- Killed:
  - `tests/test_uncredited_tombstone.py::test_a_companion_lifted_alone_does_not_come_back_behind_a_persons_back`
  - `tests/test_uncredited_tombstone.py::test_a_tombstone_that_already_stood_gains_no_companion`

Old text:

```
            if existing is not None and existing.suppressing:
                return existing
            suppression = Suppression(
```

New text:

```
            if existing is not None and existing.suppressing and not beside:
                return existing
            suppression = Suppression(
```

### `r431-a.A8_also_is_never_asked`

revoke ignores also, so lifting a credited tombstone leaves its companion suppressing

- File: `src/cratekit/core/review.py`
- Source: `r431-a.json`, row `A8_also_is_never_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair.py`, `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/modules/test_reports.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_adoption.py`, `tests/test_deletion.py`, `tests/test_genre_retag.py`, `tests/test_intake_missing_search.py`, `tests/test_label_approved.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_match_states.py`, `tests/test_reports_cli.py`, `tests/test_review_queue.py`, `tests/test_tag_workers.py`, `tests/test_tombstones.py`, `tests/test_uncredited_tombstone.py`
- Collected: 3066 against a baseline of 3066
- Kills: 6 (killed)
- Killed:
  - `tests/test_uncredited_tombstone.py::test_a_companion_is_found_by_its_pointer_when_the_stripping_rule_has_moved`
  - `tests/test_uncredited_tombstone.py::test_a_companion_two_deletions_share_outlives_the_first_lift_and_not_the_second`
  - `tests/test_uncredited_tombstone.py::test_a_credited_deletion_is_one_write_and_so_is_lifting_it`
  - `tests/test_uncredited_tombstone.py::test_a_tombstone_with_no_pointer_still_accounts_for_the_companion_it_strips_to`
  - `tests/test_uncredited_tombstone.py::test_lifting_a_credited_tombstone_lifts_its_companion`
  - `tests/test_uncredited_tombstone.py::test_the_shared_companion_is_also_found_in_the_other_order`

Old text:

```
            with_it = tuple(also(existing, dict(recorded))) if also is not None else ()
```

New text:

```
            with_it = ()
```

### `r431-a.A9_an_already_lifted_record_is_lifted_again`

also restamps a record that was already lifted, and fails on an identifier that names nothing

- File: `src/cratekit/core/review.py`
- Source: `r431-a.json`, row `A9_an_already_lifted_record_is_lifted_again`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair.py`, `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/modules/test_reports.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_adoption.py`, `tests/test_deletion.py`, `tests/test_genre_retag.py`, `tests/test_intake_missing_search.py`, `tests/test_label_approved.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_match_states.py`, `tests/test_reports_cli.py`, `tests/test_review_queue.py`, `tests/test_tag_workers.py`, `tests/test_tombstones.py`, `tests/test_uncredited_tombstone.py`
- Collected: 3066 against a baseline of 3066
- Kills: 1 (killed)
- Killed:
  - `tests/test_uncredited_tombstone.py::test_a_companion_already_lifted_keeps_the_lift_it_was_given`

Old text:

```
                if other is not None and other.suppressing:
                    recorded[other_id] = lifted(other)
```

New text:

```
                if other is not None:
                    recorded[other_id] = lifted(other)
```

### `u127.W1_writable_always`

The writer's question always answers writable

- File: `src/cratekit/core/rb_writer.py`
- Source: `u127.json`, row `W1_writable_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_favorites_colour_read.py`, `tests/test_favorites_placement.py`, `tests/test_genre_favorites.py`, `tests/test_genre_favorites_adoption.py`, `tests/test_genre_retag.py`, `tests/test_head_agreement.py`, `tests/test_inbox_rotate.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_metadata_policy.py`, `tests/test_naming_apply_cli.py`, `tests/test_organize.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_process_guard.py`, `tests/test_queued_resume_contract.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_snapshot.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_whitelist_membership.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 4352 against a baseline of 4352
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_library_with_no_category_to_copy_tags_nothing_and_lands_the_batch`

Old text:

```
        if exc.cause.reason != "mytag-category-template-missing":
            raise
        return False
```

New text:

```
        if exc.cause.reason != "mytag-category-template-missing":
            raise
        return True
```

### `u127.W2_writable_reason_drift`

The writer's question reads another reason than the writer raises

- File: `src/cratekit/core/rb_writer.py`
- Source: `u127.json`, row `W2_writable_reason_drift`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_favorites_colour_read.py`, `tests/test_favorites_placement.py`, `tests/test_genre_favorites.py`, `tests/test_genre_favorites_adoption.py`, `tests/test_genre_retag.py`, `tests/test_head_agreement.py`, `tests/test_inbox_rotate.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_metadata_policy.py`, `tests/test_naming_apply_cli.py`, `tests/test_organize.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_process_guard.py`, `tests/test_queued_resume_contract.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_snapshot.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_whitelist_membership.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 4352 against a baseline of 4352
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_library_with_no_category_to_copy_tags_nothing_and_lands_the_batch`

Old text:

```
        if exc.cause.reason != "mytag-category-template-missing":
```

New text:

```
        if exc.cause.reason != "mytag-category-missing":
```

### `r83-round-2.I1_fold_case`

R-344, after fix round 1: normalize_identity strips but no longer folds the case

- File: `src/cratekit/core/preflight.py`
- Source: `r83-round-2.json`, row `I1_fold_case`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_metadata_cli.py`, `tests/test_preflight.py`, `tests/test_rebuild.py`, `tests/test_reserved_causes.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 2840 against a baseline of 2840
- Kills: 19 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_identity_typed_as_diskutil_prints_it_passes_the_mount_check`
  - `tests/test_preflight.py::test_an_identity_in_another_case_is_still_found_where_it_is_mounted`
  - `tests/test_preflight.py::test_an_identity_recorded_in_uppercase_matches_the_lowercase_the_kernel_reports`
  - `tests/test_restore_cli.py::test_a_backup_landing_after_the_approval_does_not_change_what_is_pulled`
  - `tests/test_restore_cli.py::test_a_backup_landing_between_the_two_acts_moves_the_digest`
  - `tests/test_restore_cli.py::test_a_rehearsal_is_still_refused_while_rekordbox_is_running`
  - `tests/test_restore_cli.py::test_a_target_directory_that_does_not_exist_is_still_the_absent_refusal`
  - `tests/test_restore_cli.py::test_a_target_restores_the_database_into_the_directory_it_names`
  - `tests/test_restore_cli.py::test_a_target_run_rolls_no_session_back_even_by_default`
  - `tests/test_restore_cli.py::test_an_unconfirmed_absence_at_the_database_half_says_what_the_mirror_left`
  - `tests/test_restore_cli.py::test_another_librarys_snapshot_is_refused_at_the_verb_and_names_both_volumes`
  - `tests/test_restore_cli.py::test_the_digest_moves_when_the_expected_volume_is_stated`
  - `tests/test_restore_cli.py::test_the_digest_moves_when_the_mirror_half_is_added`
  - `tests/test_restore_cli.py::test_the_digest_moves_when_the_restore_is_pointed_somewhere_else`
  - `tests/test_restore_cli.py::test_the_from_backup_flag_reaches_the_off_machine_half_through_the_dispatcher`
  - ... and 4 more, see the JSON sidecar

Old text:

```
    return identity.strip().lower()
```

New text:

```
    return identity.strip()
```

### `r83-round-2.I3_configured_compare_exact`

R-344, after fix round 1: the configured mount's compare goes back to exact equality

- File: `src/cratekit/core/preflight.py`
- Source: `r83-round-2.json`, row `I3_configured_compare_exact`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_metadata_cli.py`, `tests/test_preflight.py`, `tests/test_rebuild.py`, `tests/test_reserved_causes.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 2840 against a baseline of 2840
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_identity_typed_as_diskutil_prints_it_passes_the_mount_check`
  - `tests/test_preflight.py::test_an_identity_recorded_in_uppercase_matches_the_lowercase_the_kernel_reports`

Old text:

```
    if same_identity(recorded_identity, observed):
```

New text:

```
    if observed == recorded_identity:
```

### `r83-round-2.I4_elsewhere_compare_exact`

R-344, after fix round 1: the mounted elsewhere sweep's compare goes back to exact equality, the round 1 zero

- File: `src/cratekit/core/preflight.py`
- Source: `r83-round-2.json`, row `I4_elsewhere_compare_exact`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_metadata_cli.py`, `tests/test_preflight.py`, `tests/test_rebuild.py`, `tests/test_reserved_causes.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 2840 against a baseline of 2840
- Kills: 1 (killed)
- Killed:
  - `tests/test_preflight.py::test_an_identity_in_another_case_is_still_found_where_it_is_mounted`

Old text:

```
        if found is not None and same_identity(recorded_identity, found):
```

New text:

```
        if found == recorded_identity:
```

### `u293.N1_no_answer`

_no_answer: an answer or a raised line given to the night is taken

- File: `src/cratekit/cli/sync_night.py`
- Source: `u293.json`, row `N1_no_answer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_night.py`, `tests/test_crate_sync_skill.py`, `tests/test_cli_contract.py`
- Collected: 1068 against a baseline of 1068
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_night.py::test_an_answer_or_a_raised_line_given_to_the_night_refuses_before_anything[argv0]`
  - `tests/test_sync_night.py::test_an_answer_or_a_raised_line_given_to_the_night_refuses_before_anything[argv1]`
  - `tests/test_sync_night.py::test_an_answer_or_a_raised_line_given_to_the_night_refuses_before_anything[argv2]`
  - `tests/test_sync_night.py::test_an_answer_or_a_raised_line_given_to_the_night_refuses_before_anything[argv3]`

Old text:

```
    if given:
```

New text:

```
    if False:
```

### `u293.N2_rekordbox_refused`

sync_night: the night runs beside rekordbox or its agent

- File: `src/cratekit/cli/sync_night.py`
- Source: `u293.json`, row `N2_rekordbox_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_night.py`, `tests/test_crate_sync_skill.py`, `tests/test_cli_contract.py`
- Collected: 1068 against a baseline of 1068
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_night.py::test_a_refused_night_writes_its_record_even_when_its_line_cannot_be_kept`
  - `tests/test_sync_night.py::test_rekordbox_or_its_agent_up_refuses_before_any_call[running0]`
  - `tests/test_sync_night.py::test_rekordbox_or_its_agent_up_refuses_before_any_call[running1]`

Old text:

```
            rb_writer.assert_rekordbox_closed("crate sync night")
```

New text:

```
            pass
```

### `u293.N3_live_job_refused`

sync_night: the night runs beside a job with a live driver

- File: `src/cratekit/cli/sync_night.py`
- Source: `u293.json`, row `N3_live_job_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_night.py`, `tests/test_crate_sync_skill.py`, `tests/test_cli_contract.py`
- Collected: 1068 against a baseline of 1068
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_night.py::test_a_job_with_a_live_driver_refuses_before_any_call`

Old text:

```
            _no_live_job()
            pass_run
```

New text:

```
            pass_run
```

### `u293.N4_occupied_refused`

sync_night: a new pass runs beside what the staging folder holds

- File: `src/cratekit/cli/sync_night.py`
- Source: `u293.json`, row `N4_occupied_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_night.py`, `tests/test_crate_sync_skill.py`, `tests/test_cli_contract.py`
- Collected: 1068 against a baseline of 1068
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_night.py::test_a_landed_pass_reads_settled_everywhere_whatever_is_staged_since`
  - `tests/test_sync_night.py::test_a_refused_firing_keeps_the_pass_waiting_at_its_gate`
  - `tests/test_sync_night.py::test_a_staging_folder_holding_what_a_landing_takes_refuses_a_new_pass`
  - `tests/test_sync_night.py::test_an_answered_gate_over_tracks_still_staged_stays_owed`

Old text:

```
                _nothing_waits(cfg, last)
```

New text:

```
                pass
```

### `u293.N5_owed_kept`

_refused: a refusal writes a fresh record over a pass still owed

- File: `src/cratekit/cli/sync_night.py`
- Source: `u293.json`, row `N5_owed_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_night.py`, `tests/test_crate_sync_skill.py`, `tests/test_cli_contract.py`
- Collected: 1068 against a baseline of 1068
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_night.py::test_a_refused_firing_keeps_the_pass_the_next_night_continues`
  - `tests/test_sync_night.py::test_a_refused_firing_keeps_the_pass_waiting_at_its_gate`
  - `tests/test_sync_night.py::test_an_answered_gate_over_tracks_still_staged_stays_owed`

Old text:

```
    if _owed(last) and last is not None:
```

New text:

```
    if False:
```

### `u293.N6_settled_by_landing`

settle: the pass's own landing never ends a wait, so a landed pass reads as waiting

- File: `src/cratekit/cli/sync_night.py`
- Source: `u293.json`, row `N6_settled_by_landing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_night.py`, `tests/test_crate_sync_skill.py`, `tests/test_cli_contract.py`
- Collected: 1068 against a baseline of 1068
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_night.py::test_a_landed_pass_reads_settled_everywhere_whatever_is_staged_since`

Old text:

```
    if _landed(cfg, record.get("land_name")):
```

New text:

```
    if False:
```

### `u293.N7_unread_landing_is_not_settled`

_landed: a landing log that cannot be read is read as landed, so a waiting pass reads settled

- File: `src/cratekit/cli/sync_night.py`
- Source: `u293.json`, row `N7_unread_landing_is_not_settled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_night.py`, `tests/test_crate_sync_skill.py`, `tests/test_cli_contract.py`
- Collected: 1068 against a baseline of 1068
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_night.py::test_a_landing_that_cannot_be_read_settles_nothing`

Old text:

```
    except (CratekitError, OSError):
        return None
```

New text:

```
    except (CratekitError, OSError):
        return True
```

### `u212.T1_reason_guard`

tail.second_copies: read any refusal's outstanding files, not only rename-incomplete's

- File: `src/cratekit/cli/tail.py`
- Source: `u212.json`, row `T1_reason_guard`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_cli_contract.py`, `tests/test_crate_sync_skill.py`, `tests/test_drift.py`, `tests/test_label_sync_go.py`, `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_tag_guess.py`, `tests/test_vocals_cli.py`
- Collected: 1607 against a baseline of 1607
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_staged.py::test_a_stop_that_is_not_rename_incomplete_or_cannot_read_the_queue_is_unchanged`

Old text:

```
    if cause.reason != RENAME_INCOMPLETE:
        return stop
```

New text:

```
(empty)
```

### `u212.T2_done_only`

tail._downloaded_by: a job that froze the track and never acquired it is named as its source

- File: `src/cratekit/cli/tail.py`
- Source: `u212.json`, row `T2_done_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_cli_contract.py`, `tests/test_crate_sync_skill.py`, `tests/test_drift.py`, `tests/test_label_sync_go.py`, `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_tag_guess.py`, `tests/test_vocals_cli.py`
- Collected: 1607 against a baseline of 1607
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_staged.py::test_the_passes_named_are_this_librarys_finished_downloads_earliest_first`

Old text:

```
            if refs & done:
```

New text:

```
            if refs:
```

### `u212.T3_library`

tail._downloaded_by: another library's download job is named

- File: `src/cratekit/cli/tail.py`
- Source: `u212.json`, row `T3_library`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_cli_contract.py`, `tests/test_crate_sync_skill.py`, `tests/test_drift.py`, `tests/test_label_sync_go.py`, `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_tag_guess.py`, `tests/test_vocals_cli.py`
- Collected: 1607 against a baseline of 1607
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_staged.py::test_the_passes_named_are_this_librarys_finished_downloads_earliest_first`

Old text:

```
            if cfg is not None and job.library_id != cfg.library.volume_id:
                continue
```

New text:

```
(empty)
```

### `u212.T4_earliest_first`

tail._downloaded_by: the passes named newest first, though the step says earliest first

- File: `src/cratekit/cli/tail.py`
- Source: `u212.json`, row `T4_earliest_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_cli_contract.py`, `tests/test_crate_sync_skill.py`, `tests/test_drift.py`, `tests/test_label_sync_go.py`, `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_tag_guess.py`, `tests/test_vocals_cli.py`
- Collected: 1607 against a baseline of 1607
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_staged.py::test_the_passes_named_are_this_librarys_finished_downloads_earliest_first`

Old text:

```
        for job in reversed(jobs.list_jobs(store)):
```

New text:

```
        for job in jobs.list_jobs(store):
```

### `u212.T5_name_wraps`

tail.name: the name step's stop passed on without the passes that downloaded the copy

- File: `src/cratekit/cli/tail.py`
- Source: `u212.json`, row `T5_name_wraps`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_cli_contract.py`, `tests/test_crate_sync_skill.py`, `tests/test_drift.py`, `tests/test_label_sync_go.py`, `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_tag_guess.py`, `tests/test_vocals_cli.py`
- Collected: 1607 against a baseline of 1607
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land_staged.py::test_a_name_stop_over_a_second_copy_names_the_pass_that_downloaded_it`
  - `tests/test_sync_land_staged.py::test_a_second_copy_no_download_job_records_is_said_so`

Old text:

```
        raise second_copies(stop, cfg) from None
```

New text:

```
        raise stop from None
```

### `u282.T1_question_asked_with_a_picture`

tag_one: the picture's question is asked whatever the file holds, so a file with a picture spends a Beatport request

- File: `src/cratekit/tagging/tag.py`
- Source: `u282.json`, row `T1_question_asked_with_a_picture`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1463 against a baseline of 1463
- Kills: 2 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_file_discogs_tagged_that_has_a_picture_sends_beatport_nothing`
  - `tests/test_tag_workers.py::test_a_sweep_discogs_decides_asks_beatport_only_for_missing_covers_and_counts_discogs_first`

Old text:

```
    if settled is None and hit is not None and hit.ask_picture is not None:
```

New text:

```
    if hit is not None and hit.ask_picture is not None:
```

### `u282.T2_question_never_asked`

tag_one: the picture's question is never asked (merge blocker 5)

- File: `src/cratekit/tagging/tag.py`
- Source: `u282.json`, row `T2_question_never_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1463 against a baseline of 1463
- Kills: 5 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_file_discogs_tagged_with_no_picture_gets_beatport_s_cover`
  - `tests/test_discogs_first.py::test_a_picture_ask_that_raises_never_fails_the_file`
  - `tests/test_discogs_first.py::test_a_refused_picture_ask_keeps_the_genre_and_says_beatport_went_unread`
  - `tests/test_discogs_first.py::test_a_tagged_file_with_no_picture_keeps_its_genre_and_gets_the_cover`
  - `tests/test_tag_workers.py::test_a_sweep_discogs_decides_asks_beatport_only_for_missing_covers_and_counts_discogs_first`

Old text:

```
    if settled is None and hit is not None and hit.ask_picture is not None:
```

New text:

```
    if False:
```

### `u282.T3_failed_question_raises`

_picture_asked: a question that fails raises and fails a file whose genre was written

- File: `src/cratekit/tagging/tag.py`
- Source: `u282.json`, row `T3_failed_question_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1463 against a baseline of 1463
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_picture_ask_that_raises_never_fails_the_file`

Old text:

```
    except Exception as exc:  # noqa: BLE001
        said = f"{exc.cause.reason}
```

New text:

```
    except ZeroDivisionError as exc:  # noqa: BLE001
        said = f"{exc.cause.reason}
```

### `u282.T4_failed_question_result_dropped`

tag_one: a failed question's art result is dropped, so the picture is fetched off a hit that named none

- File: `src/cratekit/tagging/tag.py`
- Source: `u282.json`, row `T4_failed_question_result_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1463 against a baseline of 1463
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_picture_ask_that_raises_never_fails_the_file`

Old text:

```
    elif unasked is not None:
        pictured = unasked
```

New text:

```
    elif False:
        pictured = unasked
```

### `u289.C1_record_drops_asked`

the sweep's record leaves the question's read out

- File: `src/cratekit/tagging/cli.py`
- Source: `u289.json`, row `C1_record_drops_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_beatport_refusal.py`
- Collected: 1430 against a baseline of 1430
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_the_sweeps_record_names_the_question_each_file_was_asked`

Old text:

```
                "read": result.asked_read,
```

New text:

```
                "read": "",
```

### `u289.T1_title_tag_split`

tag_one: a file with a title tag and no artist tag is split by its name

- File: `src/cratekit/tagging/tag.py`
- Source: `u289.json`, row `T1_title_tag_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_beatport_refusal.py`
- Collected: 1430 against a baseline of 1430
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_a_title_tag_with_no_artist_tag_is_never_split_by_its_name`

Old text:

```
    named = titles.by_name(path.stem) if not artist and not title_tag else None
```

New text:

```
    named = titles.by_name(path.stem) if not artist else None
```

### `u289.T2_split_artist_dropped`

tag_one: the name's artist is read and never handed to the searcher

- File: `src/cratekit/tagging/tag.py`
- Source: `u289.json`, row `T2_split_artist_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_beatport_refusal.py`
- Collected: 1430 against a baseline of 1430
- Kills: 4 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_an_mp3_named_untagged_file_carries_no_marker_into_the_question`
  - `tests/test_discogs_question.py::test_an_untagged_file_is_asked_by_the_artist_and_title_its_name_reads_to`
  - `tests/test_discogs_question.py::test_an_untagged_file_named_artist_and_title_takes_the_release_that_names_both`
  - `tests/test_discogs_question.py::test_the_sweeps_record_names_the_question_each_file_was_asked`

Old text:

```
    if named is not None:
        artist = named.artist
```

New text:

```
    if False:
        artist = named.artist
```

### `u289.T3_record_read_from_title`

tag_one: the record says how the title was read for a file asked by its name

- File: `src/cratekit/tagging/tag.py`
- Source: `u289.json`, row `T3_record_read_from_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_beatport_refusal.py`
- Collected: 1430 against a baseline of 1430
- Kills: 3 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_a_name_that_reads_to_no_one_split_is_asked_with_no_artist_and_says_so`
  - `tests/test_discogs_question.py::test_an_untagged_file_is_asked_by_the_artist_and_title_its_name_reads_to`
  - `tests/test_discogs_question.py::test_the_sweeps_record_names_the_question_each_file_was_asked`

Old text:

```
        if named is not None and named.read in (titles.Read.BY_NAME, titles.Read.NAME_AMBIGUOUS):
```

New text:

```
        if False:
```

### `r289-b.D1_no_chunking`

Ask about every name in one statement, past the parameter limit

- File: `src/cratekit/core/jobs.py`
- Source: `r289-b.json`, row `D1_no_chunking`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 2552 against a baseline of 2552
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_states_of_answers_past_the_parameter_limit_of_one_statement`

Old text:

```
_ID_CHUNK = 500
```

New text:

```
_ID_CHUNK = 1_000_000
```

### `r289-b.D3_unknown_name_gets_a_state`

Answer for every name asked about, inventing queued for the unknown ones

- File: `src/cratekit/core/jobs.py`
- Source: `r289-b.json`, row `D3_unknown_name_gets_a_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 2552 against a baseline of 2552
- Kills: 2 (killed)
- Killed:
  - `tests/test_jobs.py::test_states_of_answers_for_the_names_it_knows_and_omits_the_rest`
  - `tests/test_jobs.py::test_states_of_answers_past_the_parameter_limit_of_one_statement`

Old text:

```
    found: dict[str, JobState] = {}
    wanted = list(job_ids)
```

New text:

```
    wanted = list(job_ids)
    found: dict[str, JobState] = dict.fromkeys(wanted, JobState.QUEUED)
```

### `u221.R21_unknown_name_not_refused`

release plan: drop the refusal of a name that is no twin's, so it reaches the lookup

- File: `src/cratekit/sync/release_cli.py`
- Source: `u221.json`, row `R21_unknown_name_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_cli_contract.py`
- Collected: 1029 against a baseline of 1029
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_a_name_that_is_no_twin_is_refused_and_nothing_is_planned`

Old text:

```
        if missing:
            raise _not_a_twin(missing)
```

New text:

```
        if False:
            raise _not_a_twin(missing)
```

### `u221.R22_all_beside_names`

sync_release: drop the refusal of names beside --all

- File: `src/cratekit/sync/release_cli.py`
- Source: `u221.json`, row `R22_all_beside_names`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_cli_contract.py`
- Collected: 1029 against a baseline of 1029
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_release_needs_names_or_all_and_not_both[args1]`

Old text:

```
    if every and named:
```

New text:

```
    if False:
```

### `u221.R23_nothing_named`

sync_release: drop the refusal of a run naming nothing, so it plans nothing silently

- File: `src/cratekit/sync/release_cli.py`
- Source: `u221.json`, row `R23_nothing_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_cli_contract.py`
- Collected: 1029 against a baseline of 1029
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_release_needs_names_or_all_and_not_both[args0]`

Old text:

```
    if not every and not named:
```

New text:

```
    if False:
```

### `u221.R25_released_twin_asks_again`

Planned.action: a twin holding nothing reads as one to release, so a second run asks again over nothing

- File: `src/cratekit/sync/release_cli.py`
- Source: `u221.json`, row `R25_released_twin_asks_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_cli_contract.py`
- Collected: 1029 against a baseline of 1029
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_a_released_twin_asks_nothing_the_second_time`

Old text:

```
        return NOTHING_HELD if self.held is not None and not self.held else RELEASE
```

New text:

```
        return RELEASE
```

### `u234.O18_snapshot_keeps_the_reading`

a snapshot that moved keeps the reading after the stop, so it outlives the stop it was read after

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u234.json`, row `O18_snapshot_keeps_the_reading`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_intake_land_twins.py`, `tests/test_outbound_order.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 1765 against a baseline of 1765
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_the_person_reordered_after_a_sync_read_it_is_merged_as_their_change`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_stopped.py::test_a_reading_after_a_stop_round_trips_and_goes_when_the_snapshot_moves`
  - `tests/test_sync_pair_stopped_order.py::test_an_account_the_stop_left_off_its_path_is_never_written_into_rekordbox`

Old text:

```
                stop_seen=None if moved else held.stop_seen,
```

New text:

```
                stop_seen=held.stop_seen,
```

### `u234.O19_reading_not_written`

the pair's document never writes the reading after the stop, so a later sync never finds it

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u234.json`, row `O19_reading_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_intake_land_twins.py`, `tests/test_outbound_order.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 1765 against a baseline of 1765
- Kills: 14 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_the_person_reordered_after_a_sync_read_it_is_merged_as_their_change`
  - `tests/test_sync_pair_settle.py::test_a_reorder_settled_readings_show_keeps_the_unread_track_where_the_person_put_it`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_a_readable_track_beside_an_unread_one_still_leads`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`
  - `tests/test_sync_pair_stopped.py::test_a_reading_after_a_stop_round_trips_and_goes_when_the_snapshot_moves`
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_that_moves_again_before_it_settles_is_held_again`
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_waits_the_agreement_window`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_the_person_made_on_the_account_after_a_sync_read_it_still_leads`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_that_moved_before_it_settled_starts_again`
  - `tests/test_sync_pair_stopped_order.py::test_a_reorder_seen_changing_between_two_syncs_after_the_stop_leads`
  - `tests/test_sync_pair_stopped_order.py::test_an_order_held_as_the_one_after_waits_afresh_once_the_settled_order_is_read_between`

Old text:

```
        if self.stop_seen is not None:
            record["stop_seen"] = self.stop_seen.to_json()
```

New text:

```
        if False:
            record["stop_seen"] = self.stop_seen.to_json()
```

### `r704-a.E2_job_verdict_needs_every_item_retryable`

existing guard sample: the job verdict is transient only when every failure is, so a mixed job reads permanent

- File: `src/cratekit/core/jobs.py`
- Source: `r704-a.json`, row `E2_job_verdict_needs_every_item_retryable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_outcome.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_provider_gate.py`, `tests/test_queued_resume_contract.py`, `tests/test_render_payloads.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 2850 against a baseline of 2850
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_job_whose_failures_include_a_retryable_cause_stays_retryable`

Old text:

```
    if not failed or any(cause.retryable for cause in failed):
```

New text:

```
    if not failed or all(cause.retryable for cause in failed):
```

### `r1724.N11_tag_one_raw_stem`

tag_one: hand the searcher the raw stem, so the match reads mix)_pn and the Obiman release is missed

- File: `src/cratekit/tagging/tag.py`
- Source: `r1724.json`, row `N11_tag_one_raw_stem`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_name_tail.py`, `tests/test_discogs_question.py`, `tests/test_title_matcher.py`, `tests/test_genre_retag.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`
- Collected: 1672 against a baseline of 1672
- Kills: 5 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_an_untagged_file_is_asked_by_the_artist_and_title_its_name_reads_to`
  - `tests/test_name_tail.py::test_a_file_with_an_artist_tag_and_no_title_tag_is_asked_its_name_past_the_tail`
  - `tests/test_name_tail.py::test_sunshine_hotel_is_asked_by_its_artist_and_title_and_no_source_sees_the_tail`
  - `tests/test_name_tail.py::test_the_obiman_name_is_asked_its_title_and_takes_the_release_a_person_would_type`
  - `tests/test_name_tail.py::test_the_obiman_name_matches_its_release_whatever_discogs_is_asked`

Old text:

```
    title = title_tag or titles.name_title(path.stem)
```

New text:

```
    title = title_tag or path.stem
```

### `r1724.N12_tag_one_tag_read`

tag_one: read the tail off a title tag too, so a tag ending _PN is not asked as written

- File: `src/cratekit/tagging/tag.py`
- Source: `r1724.json`, row `N12_tag_one_tag_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_name_tail.py`, `tests/test_discogs_question.py`, `tests/test_title_matcher.py`, `tests/test_genre_retag.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`
- Collected: 1672 against a baseline of 1672
- Kills: 1 (killed)
- Killed:
  - `tests/test_name_tail.py::test_a_title_tag_ending_in_the_tail_is_asked_and_matched_as_written`

Old text:

```
    title = title_tag or titles.name_title(path.stem)
```

New text:

```
    title = titles.name_title(title_tag or path.stem)
```

