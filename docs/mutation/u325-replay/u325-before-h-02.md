# Mutation table: u325-before-h-02

Measured by `scripts/mutate.py` on 2026-11-22 20:41 UTC, branch `HEAD` at `539638eb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22663 collected. pytest invocations for this batch: 57.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 16:21 UTC for commit `539638ebe629`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 15, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22663 against 22663. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r431-a.A6_a_standing_companion_is_rewritten` | `src/cratekit/core/review.py` | maintainer | 20 file(s) | 3066 | 1 | killed |
| `r431-a.A7_beside_written_when_the_record_stood` | `src/cratekit/core/review.py` | user | 20 file(s) | 3066 | 2 | killed |
| `r431-a.A8_also_is_never_asked` | `src/cratekit/core/review.py` | user | 20 file(s) | 3066 | 6 | killed |
| `r431-a.A9_an_already_lifted_record_is_lifted_again` | `src/cratekit/core/review.py` | maintainer | 20 file(s) | 3066 | 1 | killed |
| `r83-round-2.I1_fold_case` | `src/cratekit/core/preflight.py` | user | 15 file(s) | 2838 | 19 | killed |
| `r83-round-2.I3_configured_compare_exact` | `src/cratekit/core/preflight.py` | user | 15 file(s) | 2838 | 2 | killed |
| `r83-round-2.I4_elsewhere_compare_exact` | `src/cratekit/core/preflight.py` | user | 15 file(s) | 2838 | 1 | killed |
| `r1709.M23_intake_exact_by_token` | `src/cratekit/intake/candidates.py` | user | 29 file(s) | 3968 | 2 | killed |
| `r1709.M24_intake_identity_fold` | `src/cratekit/intake/candidates.py` | user | 29 file(s) | 3968 | 1 | killed |
| `u282.T1_question_asked_with_a_picture` | `src/cratekit/tagging/tag.py` | user | 9 file(s) | 1448 | 2 | killed |
| `u282.T2_question_never_asked` | `src/cratekit/tagging/tag.py` | user | 9 file(s) | 1448 | 5 | killed |
| `u282.T3_failed_question_raises` | `src/cratekit/tagging/tag.py` | user | 9 file(s) | 1448 | 1 | killed |
| `u282.T4_failed_question_result_dropped` | `src/cratekit/tagging/tag.py` | user | 9 file(s) | 1448 | 1 | killed |
| `u289.C1_record_drops_asked` | `src/cratekit/tagging/cli.py` | user | 8 file(s) | 1415 | 1 | killed |
| `u289.T1_title_tag_split` | `src/cratekit/tagging/tag.py` | user | 8 file(s) | 1415 | 1 | killed |
| `u289.T2_split_artist_dropped` | `src/cratekit/tagging/tag.py` | user | 8 file(s) | 1415 | 4 | killed |
| `u289.T3_record_read_from_title` | `src/cratekit/tagging/tag.py` | user | 8 file(s) | 1415 | 3 | killed |
| `u127.W2_writable_reason_drift` | `src/cratekit/core/rb_writer.py` | user | 52 file(s) | 4340 | 1 | killed |
| `u221.R21_unknown_name_not_refused` | `src/cratekit/sync/release_cli.py` | user | 2 file(s) | 1029 | 1 | killed |
| `u221.R22_all_beside_names` | `src/cratekit/sync/release_cli.py` | user | 2 file(s) | 1029 | 1 | killed |
| `u221.R23_nothing_named` | `src/cratekit/sync/release_cli.py` | user | 2 file(s) | 1029 | 1 | killed |
| `u221.R24_abort_releases` | `src/cratekit/sync/release_cli.py` | user | 2 file(s) | 1029 | 1 | killed |
| `u221.R25_released_twin_asks_again` | `src/cratekit/sync/release_cli.py` | user | 2 file(s) | 1029 | 1 | killed |
| `u27-round-8-independent.W2_composite_wrong_file` | `src/cratekit/core/rb_writer.py` | user | 11 file(s) | 22663 | 0 (promoted) | zero |
| `u27-round-8-independent.W3_canary_no_name_the_database` | `src/cratekit/core/rb_writer.py` | user | 11 file(s) | 22663 | 0 (promoted) | zero |
| `u27-round-8-independent.W5_canary_message_no_path` | `src/cratekit/core/rb_writer.py` | user | 11 file(s) | 22663 | 0 (promoted) | zero |
| `u234.O18_snapshot_keeps_the_reading` | `src/cratekit/modules/outbound/pairs.py` | maintainer | 23 file(s) | 1765 | 4 | killed |
| `u234.O19_reading_not_written` | `src/cratekit/modules/outbound/pairs.py` | user | 23 file(s) | 1765 | 14 | killed |
| `u206.M18_catalogue_keeps_any_gone` | `src/cratekit/label/tidal_catalogue.py` | user | 9 file(s) | 1135 | 2 | killed |
| `u206.M14_account_keeps_invalid_isrc` | `src/cratekit/modules/outbound/tidal_account.py` | user | 9 file(s) | 1135 | 2 | killed |
| `u206.M17_account_hit_ignored` | `src/cratekit/modules/outbound/tidal_account.py` | user | 9 file(s) | 1135 | 13 | killed |
| `r1724.N11_tag_one_raw_stem` | `src/cratekit/tagging/tag.py` | user | 9 file(s) | 1657 | 5 | killed |
| `r1724.N12_tag_one_tag_read` | `src/cratekit/tagging/tag.py` | user | 9 file(s) | 1657 | 1 | killed |
| `u59.M9_column_repointed` | `src/cratekit/core/rb_writer.py` | user | 22 file(s) | 2747 | 173 | killed |
| `r787.S1_set_drops_intake` | `src/cratekit/core/tree_registry.py` | user | 20 file(s) | 2697 | 7 | killed |
| `u48-author.S1_remedy_fixed_at_repair` | `src/cratekit/core/session.py` | user | 11 file(s) | 1553 | 1 | killed |
| `u48-author.S2_remedy_fixed_at_grant` | `src/cratekit/core/session.py` | user | 11 file(s) | 1553 | 2 | killed |
| `u49-author.L4_a_malformed_holder_raises_again` | `src/cratekit/core/session.py` | user | 13 file(s) | 2587 | 1 | killed |

## Zero rows and what they owe

- `u27-round-8-independent.W2_composite_wrong_file` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u27-round-8-independent.W3_canary_no_name_the_database` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u27-round-8-independent.W5_canary_message_no_path` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

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

### `r83-round-2.I1_fold_case`

R-344, after fix round 1: normalize_identity strips but no longer folds the case

- File: `src/cratekit/core/preflight.py`
- Source: `r83-round-2.json`, row `I1_fold_case`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_metadata_cli.py`, `tests/test_preflight.py`, `tests/test_rebuild.py`, `tests/test_reserved_causes.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 2838 against a baseline of 2838
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
- Collected: 2838 against a baseline of 2838
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
- Collected: 2838 against a baseline of 2838
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

### `r1709.M23_intake_exact_by_token`

intake's exact flag compares the token, so a search for a drop answered by a fire is listed and downloaded

- File: `src/cratekit/intake/candidates.py`
- Source: `r1709.json`, row `M23_intake_exact_by_token`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3968 against a baseline of 3968
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

### `r1709.M24_intake_identity_fold`

intake's search question keys the folded title, so an answer about a drop is listed for a later wave

- File: `src/cratekit/intake/candidates.py`
- Source: `r1709.json`, row `M24_intake_identity_fold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3968 against a baseline of 3968
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_search_question_about_one_emoji_title_is_not_another_ones`

Old text:

```
        "title": match.title_identity(wanted.title),

```

New text:

```
        "title": match.fold(wanted.title),

```

### `u282.T1_question_asked_with_a_picture`

tag_one: the picture's question is asked whatever the file holds, so a file with a picture spends a Beatport request

- File: `src/cratekit/tagging/tag.py`
- Source: `u282.json`, row `T1_question_asked_with_a_picture`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1448 against a baseline of 1448
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
- Collected: 1448 against a baseline of 1448
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
- Collected: 1448 against a baseline of 1448
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
- Collected: 1448 against a baseline of 1448
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
- Collected: 1415 against a baseline of 1415
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
- Collected: 1415 against a baseline of 1415
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
- Collected: 1415 against a baseline of 1415
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
- Collected: 1415 against a baseline of 1415
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

### `u127.W2_writable_reason_drift`

The writer's question reads another reason than the writer raises

- File: `src/cratekit/core/rb_writer.py`
- Source: `u127.json`, row `W2_writable_reason_drift`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_favorites_colour_read.py`, `tests/test_favorites_placement.py`, `tests/test_genre_favorites.py`, `tests/test_genre_favorites_adoption.py`, `tests/test_genre_retag.py`, `tests/test_head_agreement.py`, `tests/test_inbox_rotate.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_metadata_policy.py`, `tests/test_naming_apply_cli.py`, `tests/test_organize.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_process_guard.py`, `tests/test_queued_resume_contract.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_snapshot.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_whitelist_membership.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 4340 against a baseline of 4340
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

### `u221.R24_abort_releases`

sync_release: read an abort as an approval, so the hold is emptied without the choice

- File: `src/cratekit/sync/release_cli.py`
- Source: `u221.json`, row `R24_abort_releases`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_cli_contract.py`
- Collected: 1029 against a baseline of 1029
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_an_abort_lets_nothing_go`

Old text:

```
    if ctx.gate.require(_gate(ctx.entry), plan=data, context=facts(planned)) != "approve":
```

New text:

```
    if ctx.gate.require(_gate(ctx.entry), plan=data, context=facts(planned)) == "never":
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

### `u27-round-8-independent.W2_composite_wrong_file`

COMPOSITE for W2: the canary names a file that is not the one it opened

- File: `src/cratekit/core/rb_writer.py`
- Source: `u27-round-8-independent.json`, row `W2_composite_wrong_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_metadata_policy.py`, `tests/test_process_guard.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        named = path if path is not None else handle_path(db)
```

New text:

```
        named = (str(path) + "-not-this-file") if path is not None else handle_path(db)
```

### `u27-round-8-independent.W3_canary_no_name_the_database`

Drop the name_the_database hand-off in the canary, so a chmod 000 database is unclassifiable

- File: `src/cratekit/core/rb_writer.py`
- Source: `u27-round-8-independent.json`, row `W3_canary_no_name_the_database`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_metadata_policy.py`, `tests/test_process_guard.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if named is not None:
            name_the_database(exc, named)
```

New text:

```
(empty)
```

### `u27-round-8-independent.W5_canary_message_no_path`

Reword the canary refusal so its sentence no longer names the database file

- File: `src/cratekit/core/rb_writer.py`
- Source: `u27-round-8-independent.json`, row `W5_canary_message_no_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_metadata_policy.py`, `tests/test_process_guard.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            f"the rekordbox database{where} opened but could not be read as "
            f"expected: {exc}",
```

New text:

```
            f"the rekordbox database could not be read as expected after it "
            f"opened: {exc}",
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

### `u206.M18_catalogue_keeps_any_gone`

TidalCatalogue.tracks_for_isrc: keep every failure _gone reads as a not found, a FileNotFoundError among them

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u206.json`, row `M18_catalogue_keeps_any_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 2 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_the_catalogue_answers_a_class_named_not_found_as_before_and_keeps_nothing[file]`
  - `tests/test_isrc_cache.py::test_the_catalogue_answers_a_class_named_not_found_as_before_and_keeps_nothing[module]`

Old text:

```
                    if isrc_cache.said_not_found(exc):
                        answered.append(())
```

New text:

```
                    if True:
                        answered.append(())
```

### `u206.M14_account_keeps_invalid_isrc`

TidalAccount._isrc_tracks: keep any no match as a not found, InvalidISRC included

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u206.json`, row `M14_account_keeps_invalid_isrc`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 2 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_an_invalid_isrc_the_account_reads_as_no_match_is_never_kept`
  - `tests/test_isrc_cache.py::test_an_outage_then_an_invalid_isrc_on_the_retry_keeps_nothing`

Old text:

```
            if last["said_not_found"]:
                self._cache.remember(wanted, country, ())
```

New text:

```
            if True:
                self._cache.remember(wanted, country, ())
```

### `u206.M17_account_hit_ignored`

TidalAccount._isrc_tracks: never use a remembered answer

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u206.json`, row `M17_account_hit_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 13 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_404_status_is_kept_as_a_not_found_at_either_seam[account]`
  - `tests/test_isrc_cache.py::test_a_choice_among_several_releases_is_made_from_a_remembered_answer_with_no_call`
  - `tests/test_isrc_cache.py::test_a_copy_run_redirecting_installation_state_shares_answers_through_the_override`
  - `tests/test_isrc_cache.py::test_a_found_answer_is_asked_again_after_the_configured_days`
  - `tests/test_isrc_cache.py::test_a_found_answer_lives_thirty_days_unless_set`
  - `tests/test_isrc_cache.py::test_a_not_found_is_kept_and_asked_again_after_seven_days`
  - `tests/test_isrc_cache.py::test_a_second_account_over_a_fresh_client_asks_nothing_for_an_answered_isrc`
  - `tests/test_isrc_cache.py::test_a_tie_remembered_is_still_refused_with_its_reason`
  - `tests/test_isrc_cache.py::test_an_expired_answer_is_replaced_by_the_new_one`
  - `tests/test_isrc_cache.py::test_an_outage_then_a_not_found_on_the_retry_keeps_the_not_found`
  - `tests/test_isrc_cache.py::test_the_catalogue_and_the_account_share_one_answer`
  - `tests/test_isrc_cache.py::test_the_process_counts_say_what_the_cache_settled_and_what_was_asked`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[kept]`

Old text:

```
        if held is not None:
            return held if held else _ABSENT
        # What the LAST attempt said
```

New text:

```
        if False:
            return held if held else _ABSENT
        # What the LAST attempt said
```

### `r1724.N11_tag_one_raw_stem`

tag_one: hand the searcher the raw stem, so the match reads mix)_pn and the Obiman release is missed

- File: `src/cratekit/tagging/tag.py`
- Source: `r1724.json`, row `N11_tag_one_raw_stem`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_name_tail.py`, `tests/test_discogs_question.py`, `tests/test_title_matcher.py`, `tests/test_genre_retag.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`
- Collected: 1657 against a baseline of 1657
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
- Collected: 1657 against a baseline of 1657
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

### `u59.M9_column_repointed`

Point SOFT_DELETE_COLUMN at a neighbouring bookkeeping column

- File: `src/cratekit/core/rb_writer.py`
- Source: `u59.json`, row `M9_column_repointed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`, `tests/test_process_guard.py`, `tests/test_queued_resume_contract.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 2747 against a baseline of 2747
- Kills: 173 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_a_library_of_tombstones_and_an_empty_one_both_census_to_nothing`
  - `tests/test_adopt_apply_cli.py::test_the_census_is_the_library_and_every_row_of_it_is_carried`
  - `tests/test_adopt_collection.py::test_a_null_location_and_a_null_genre_are_empty_strings_not_none`
  - `tests/test_adopt_collection.py::test_a_tombstone_is_carried_rather_than_dropped`
  - `tests/test_adopt_collection.py::test_every_field_comes_off_the_row_it_belongs_to`
  - `tests/test_adopt_collection.py::test_the_identifier_is_stringified_because_the_column_need_not_be_text`
  - `tests/test_adopt_collection.py::test_the_reader_yields_the_rows_the_database_holds`
  - `tests/test_adopt_workers.py::test_a_configured_volume_rewrite_reaches_the_census`
  - `tests/test_adopt_workers.py::test_a_library_of_tombstones_is_a_different_zero_from_an_empty_one`
  - `tests/test_adopt_workers.py::test_a_plan_with_nothing_applicable_queues_nothing`
  - `tests/test_adopt_workers.py::test_a_row_tombstoned_between_queueing_and_driving_fails_its_own_item`
  - `tests/test_deferred_routing.py::test_content_rows_reads_the_soft_delete_marker_off_the_row`
  - `tests/test_deletion.py::test_a_binding_that_cannot_say_how_many_memberships_it_holds_refuses`
  - `tests/test_deletion.py::test_a_collection_row_with_no_id_reaches_the_pass_as_unidentifiable`
  - `tests/test_deletion.py::test_a_confirmed_ambiguous_row_is_refused_at_move_time_too`
  - ... and 158 more, see the JSON sidecar

Old text:

```
SOFT_DELETE_COLUMN = "rb_local_deleted"
```

New text:

```
SOFT_DELETE_COLUMN = "rb_local_synced"
```

### `r787.S1_set_drops_intake`

cutover_trees returns the routing tree alone, the list doctor held before R-787

- File: `src/cratekit/core/tree_registry.py`
- Source: `r787.json`, row `S1_set_drops_intake`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_intake_imported.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_landing_labels.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_tree_registry.py`, `tests/test_tree_writer.py`, `tests/test_xml_import_coexistence.py`, `tests/test_xml_splice_golden.py`
- Collected: 2697 against a baseline of 2697
- Kills: 7 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_a_tree_the_taxonomy_does_not_declare_is_refused`
  - `tests/test_cutover_cli.py::test_doctor_and_the_verb_read_one_set_of_cutover_trees`
  - `tests/test_cutover_cli.py::test_doctor_fails_on_a_native_record_the_cutover_would_refuse_to_create`
  - `tests/test_cutover_cli.py::test_doctor_reads_a_native_inbox_record_as_ok`
  - `tests/test_cutover_cli.py::test_doctor_reads_an_inbox_the_verb_cut_over_as_ok`
  - `tests/test_cutover_cli.py::test_the_catalogue_tree_is_refused_as_not_rebuildable`
  - `tests/test_cutover_cli.py::test_the_intake_tree_cuts_over_on_the_same_answer_as_the_routing_tree`

Old text:

```
    return frozenset({declared.tree.id, declared.intake.id})
```

New text:

```
    return frozenset({declared.tree.id})
```

### `u48-author.S1_remedy_fixed_at_repair`

The session names the repair token again, which is the defect this unit closed

- File: `src/cratekit/core/session.py`
- Source: `u48-author.json`, row `S1_remedy_fixed_at_repair`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_backup_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 1553 against a baseline of 1553
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_fact_file_from_a_newer_build_asks_for_an_upgrade`

Old text:

```
            remedy=Remedy(str(exc.remedy)),
```

New text:

```
            remedy=Remedy.REPAIR_BACKUP_FACTS,
```

### `u48-author.S2_remedy_fixed_at_grant`

The same defect mirrored: hard code the permission token over every condition

- File: `src/cratekit/core/session.py`
- Source: `u48-author.json`, row `S2_remedy_fixed_at_grant`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_backup_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 1553 against a baseline of 1553
- Kills: 2 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_fact_file_from_a_newer_build_asks_for_an_upgrade`
  - `tests/test_write_session.py::test_an_unreadable_backup_fact_file_refuses_the_mint`

Old text:

```
            remedy=Remedy(str(exc.remedy)),
```

New text:

```
            remedy=Remedy.GRANT_PATH_ACCESS,
```

### `u49-author.L4_a_malformed_holder_raises_again`

Remove the coercion guard from read_lock_holder, so a lock record with a non numeric pid escapes as a traceback rather than a typed refusal

- File: `src/cratekit/core/session.py`
- Source: `u49-author.json`, row `L4_a_malformed_holder_raises_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_session_cli.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 2587 against a baseline of 2587
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_lock_record_that_cannot_be_understood_refuses_by_name`

Old text:

```
    try:
        return Holder.from_json(data["holder"])
    except (TypeError, ValueError, AttributeError):
```

New text:

```
    if True:
        return Holder.from_json(data["holder"])
    if False:
```

