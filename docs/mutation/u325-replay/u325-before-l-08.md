# Mutation table: u325-before-l-08

Measured by `scripts/mutate.py` on 2026-11-23 02:08 UTC, branch `HEAD` at `539638eb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22663 collected. pytest invocations for this batch: 21.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:24 UTC for commit `539638ebe629`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 8, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard. 99 row(s) were reused from a prior sidecar and were measured by an earlier process, whose children this run did not watch.

Null control `NULL_CONTROL`: killed 0, collected 22663 against 22663. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r381.M4_migrate_ignores_taken` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 2 | killed |
| `r381.M5_migrate_any_identifier` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 4 | killed |
| `r381.M6_update_skips_move_write` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 1 | killed |
| `r381.M7_load_never_migrates` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 4 | killed |
| `r381.M8_no_renamed_map` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 2 | killed |
| `r381.M9_live_renames_unfiltered` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 2 | killed |
| `r301.B1_shipped_month_unbounded` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 5 | killed |
| `r301.B2_bound_host_ignored` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 3 | killed |
| `r301.B3_refusal_detail_no_key` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 5 | killed |
| `r301.B4_refusal_message_no_key` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 3 | killed |
| `r301.S1_month_ignores_ledger` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 6 | killed |
| `u57-recognition-and-items.M11_unreached_stop_tenfold` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 2 | killed |
| `u57-recognition-and-items.M12_quota_reads_as_failure` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 4 | killed |
| `u57-recognition-and-items.M16_grid_off_by_one` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 69 | killed |
| `u57-recognition-and-items.M18_missing_credential_is_unready` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 1 | killed |
| `u57-recognition-and-items.M1_miss_family_loses_1001` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 48 | killed |
| `u57-recognition-and-items.M2_quota_family_empty` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 6 | killed |
| `u57-recognition-and-items.M3_auth_family_loses_3001` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 2 | killed |
| `u57-recognition-and-items.M4_transient_range_dropped` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 4 | killed |
| `u57-recognition-and-items.M5_empty_music_not_none` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 1 | killed |
| `u57-recognition-and-items.M6_score_constant` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 2 | killed |
| `u57-recognition-and-items.M7_fold_never_takes_best_score` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 1 | killed |
| `r679-a.A1_supersede_guard_both_layers` | `src/cratekit/core/review.py` | user | 3 file(s) | 879 | 5 | killed |
| `r679-a.A3_supersede_readers_predicate` | `src/cratekit/core/review.py` | user | 3 file(s) | 879 | 1 | killed |
| `r679-a.A4_resolve_admits_the_machines_verdict` | `src/cratekit/core/review.py` | user | 3 file(s) | 879 | 1 | killed |
| `r679-a.A5_import_routes_through_resolve` | `src/cratekit/core/review.py` | user | 3 file(s) | 879 | 2 | killed |
| `r679-a.A6_empty_rule_admitted` | `src/cratekit/core/review.py` | user | 3 file(s) | 879 | 2 | killed |
| `r679-a.A7_person_verdicts_are_all_verdicts` | `src/cratekit/core/review.py` | user | 3 file(s) | 879 | 2 | killed |
| `r679-a.A8_actor_is_not_the_rule` | `src/cratekit/core/review.py` | user | 3 file(s) | 879 | 11 | killed |
| `r816-a.A1_too_coarse_protection` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 6 | killed |
| `r816-a.A2_held_out` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 2 | killed |
| `r816-a.A3_multi_valued` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 2 | killed |
| `r816-a.A4_agreement` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 12 | killed |
| `r816-a.A5_unreadable_is_blank` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 2 | killed |
| `r816-a.A6_first_value` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 2 | killed |
| `r816-a.A7_digest_counts` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 1 | killed |
| `r816-a.A8_leave_unmatched` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 2 | killed |
| `r816-b.B1_stale_check` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 2 | killed |
| `r816-b.B2_stale_tombstone` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 5 | killed |
| `r816-b.B3_blank_spellings` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 3 | killed |
| `r816-b.B4_restore_detection` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 1 | killed |
| `r816-b.B5_commit_recorded` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 1 | killed |
| `r816-c.B6_bookkeeping_exempt` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 10 | killed |
| `r816-c.B7_read_back_word` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 2 | killed |
| `r816-c.B8_read_back_columns` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 1 | killed |
| `r816-c.B9_cache_reset` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 1 | killed |
| `r816-d.C1_acknowledgment` | `src/cratekit/tagging/rows_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `r816-d.C2_empty_plan` | `src/cratekit/tagging/rows_cli.py` | user | 1 file(s) | 72 | 2 | killed |
| `r816-d.C3_majority_unmapped` | `src/cratekit/tagging/rows_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `r816-d.C4_only_apply_writes` | `src/cratekit/tagging/rows_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `r816-d.C5_leave_reaches_the_plan` | `src/cratekit/tagging/rows_cli.py` | user | 1 file(s) | 72 | 2 | killed |
| `u69-b.M10_out_not_a_folder` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `u69-b.M12_unlisted_status` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `u69-b.M16_next_command` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 22663 | 0 (promoted) | zero |
| `u69-b.M17_lists_folder` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 8 | killed |
| `u69-b.M18_inner_cause` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `u69-b.M19_resume_step` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `u69.M1_handler_key` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `u69.M2_succeeded_only` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 2 | killed |
| `u69.M4_report_coverage` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 2 | killed |
| `u69.M5_by_count` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `u69.M6_state_word` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `u73-b.B2_every_ref_kept` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `u73-b.B3_first_source_wins` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `u73.A10_every_job_skipped` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `u73.A1_blank_run` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `u73.A2_library_filter` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `u73.A3_run_filter` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 2 | killed |
| `u73.A4_intake_key_filter` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `u73.A5_oldest_first` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 2 | killed |
| `u73.A7_open_refuses` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `u73.A8_failed_refuses` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `u73.A9_skip_failed_ignored` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 72 | 3 | killed |
| `r706-a.A1_ceiling_dropped` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 312 | 6 | killed |
| `r706-a.A2_ceiling_one_part_wider` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 312 | 4 | killed |
| `r706-a.A3_max_parts_four` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 312 | 5 | killed |
| `r706-a.A4_month_asked_of_one_run` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 312 | 1 | killed |
| `r706-a.A5_run_guard_dropped` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 312 | 2 | killed |
| `r706-a.A6_run_message_reworded` | `src/cratekit/intake/acrcloud.py` | maintainer | 5 file(s) | 312 | 2 | killed |
| `r706-a.A7_ceiling_message_reworded` | `src/cratekit/intake/acrcloud.py` | maintainer | 5 file(s) | 312 | 1 | killed |
| `r706-b.B1_partition_front_loads_the_remainder` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 312 | 1 | killed |
| `r706-b.B2_parts_needed_floors` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 312 | 8 | killed |
| `r706-b.B3_partition_drops_the_remainder` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 312 | 5 | killed |
| `r706-b.B4_parts_reported_as_one` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 312 | 7 | killed |
| `r706-b.B5_chunks_count_the_first_part` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 312 | 6 | killed |
| `r706-b.B6_grid_not_partitioned` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 312 | 7 | killed |
| `r44-a.S10_default_slug` | `src/cratekit/core/session.py` | maintainer | 2 file(s) | 473 | 1 | killed |
| `r44-a.S1_empty_slot` | `src/cratekit/core/session.py` | user | 2 file(s) | 473 | 2 | killed |
| `r44-a.S2_proved_widened` | `src/cratekit/core/session.py` | user | 2 file(s) | 473 | 4 | killed |
| `r44-a.S3_default_to_library` | `src/cratekit/core/session.py` | user | 2 file(s) | 473 | 2 | killed |
| `r44-a.S4_inside_root_unheld` | `src/cratekit/core/session.py` | user | 2 file(s) | 473 | 6 | killed |
| `r44-a.S5_not_destructive` | `src/cratekit/core/session.py` | user | 2 file(s) | 473 | 5 | killed |
| `r44-a.S6_oserror_escapes` | `src/cratekit/core/session.py` | user | 2 file(s) | 473 | 2 | killed |
| `r44-a.S7_probe_the_target` | `src/cratekit/core/session.py` | user | 2 file(s) | 473 | 3 | killed |
| `r44-a.S8_wording_held_to` | `src/cratekit/core/session.py` | user | 2 file(s) | 473 | 1 | killed |
| `r44-a.S9_offer_to_record_nested` | `src/cratekit/core/session.py` | user | 2 file(s) | 473 | 1 | killed |
| `u71-b.B10_occupied_at_move` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 2 | killed |
| `u71-b.B11_nothing_moved` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 1 | killed |
| `u71-b.B12_take_back_folder` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 1 | killed |
| `u71-b.B13_unlink_destination` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 22663 | 0 (promoted) | zero |
| `u71-b.B1_target_under_staging` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 1 | killed |
| `u71-b.B2_device` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 1 | killed |
| `u71-b.B3_destination_exists` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 1 | killed |
| `u71-b.B4_export_missing` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 1 | killed |
| `u71-b.B5_trial_splice` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 1 | killed |
| `u71-b.B6_trial_playlist` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 1 | killed |
| `u71-c.C1_nothing_movable_rerun` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 1 | killed |
| `u71.A10_root_absent` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 1 | killed |
| `u71.A11_owned_folder` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 1 | killed |
| `u71.A12_staging_inside_library` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 2 | killed |

## Zero rows and what they owe

- `u69-b.M16_next_command` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u71-b.B13_unlink_destination` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `r381.M4_migrate_ignores_taken`

migrate moves an entry onto a slug another entry already holds

- File: `src/cratekit/label/registry.py`
- Source: `r381.json`, row `M4_migrate_ignores_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_slug.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 429 against a baseline of 429
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_slug.py::test_a_collision_leaves_the_old_identifier`
  - `tests/test_label_slug.py::test_re_adding_a_collided_label_updates_it_and_not_its_neighbour`

Old text:

```
        if new is None or new in taken:
```

New text:

```
        if new is None:
```

### `r381.M5_migrate_any_identifier`

migrate moves any entry whose slug differs, not only one the old fold produced

- File: `src/cratekit/label/registry.py`
- Source: `r381.json`, row `M5_migrate_any_identifier`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_slug.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 429 against a baseline of 429
- Kills: 4 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_the_registry_survives_a_label_rename_without_orphaning_its_state`
  - `tests/test_label_slug.py::test_a_renamed_entry_under_the_old_fold_is_not_taken_by_its_old_name`
  - `tests/test_label_slug.py::test_an_identifier_the_old_fold_did_not_produce_is_left_alone[entries0]`
  - `tests/test_label_slug.py::test_an_identifier_the_old_fold_did_not_produce_is_left_alone[entries1]`

Old text:

```
    if new == entry.label_id or entry.label_id != _legacy_slug(entry.name):
```

New text:

```
    if new == entry.label_id:
```

### `r381.M6_update_skips_move_write`

update writes nothing for a move when the mutator opts out, so load never persists a migration

- File: `src/cratekit/label/registry.py`
- Source: `r381.json`, row `M6_update_skips_move_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_slug.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 429 against a baseline of 429
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_slug.py::test_a_stored_fold_only_identifier_migrates_on_load`

Old text:

```
            if changed is not False or moved:
```

New text:

```
            if changed is not False:
```

### `r381.M7_load_never_migrates`

load returns the stored document without planning a move

- File: `src/cratekit/label/registry.py`
- Source: `r381.json`, row `M7_load_never_migrates`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_slug.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 429 against a baseline of 429
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_slug.py::test_a_migrated_label_keeps_its_watermark`
  - `tests/test_label_slug.py::test_a_stored_fold_only_identifier_migrates_on_load`
  - `tests/test_label_slug.py::test_an_advance_of_another_label_carries_the_migrated_year_along`
  - `tests/test_label_slug.py::test_an_identifier_frozen_before_the_move_still_finds_its_label`

Old text:

```
        if not migrate(held)[1]:
            return held
```

New text:

```
        if True:
            return held
```

### `r381.M8_no_renamed_map`

The writer leaves the renamed map out, so no watermark can follow

- File: `src/cratekit/label/registry.py`
- Source: `r381.json`, row `M8_no_renamed_map`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_slug.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 429 against a baseline of 429
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_slug.py::test_a_migrated_label_keeps_its_watermark`
  - `tests/test_label_slug.py::test_a_stored_fold_only_identifier_migrates_on_load`

Old text:

```
        if renamed:
            # Only when something moved
```

New text:

```
        if False:
            # Only when something moved
```

### `r381.M9_live_renames_unfiltered`

live_renames keeps a move whose old identifier a new label holds again

- File: `src/cratekit/label/registry.py`
- Source: `r381.json`, row `M9_live_renames_unfiltered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_slug.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 429 against a baseline of 429
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_slug.py::test_a_stored_move_whose_old_identifier_is_held_is_not_followed`
  - `tests/test_label_slug.py::test_an_old_identifier_reused_by_a_new_label_stops_following`

Old text:

```
        return {old: new for old, new in self.renamed.items() if old not in self.labels}
```

New text:

```
        return dict(self.renamed)
```

### `r301.B1_shipped_month_unbounded`

The shipped budget carries no monthly bound, which is the tree before this unit

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r301.json`, row `B1_shipped_month_unbounded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 5 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_the_shipped_budget_bounds_the_month_the_section_names`
  - `tests/intake/test_workers.py::test_an_unconfigured_machine_meets_a_monthly_bound_before_the_first_call[identify]`
  - `tests/intake/test_workers.py::test_an_unconfigured_machine_meets_a_monthly_bound_before_the_first_call[set]`
  - `tests/intake/test_workers.py::test_the_configured_monthly_bound_is_the_one_the_verb_meets[identify]`
  - `tests/intake/test_workers.py::test_the_configured_monthly_bound_is_the_one_the_verb_meets[set]`

Old text:

```
        return cls(per_run=MAX_CALLS_PER_RUN, monthly=recognition.monthly_calls)
```

New text:

```
        return cls(per_run=MAX_CALLS_PER_RUN, monthly=None)
```

### `r301.B2_bound_host_ignored`

The bound identifier asks the default region whatever the section names

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r301.json`, row `B2_bound_host_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_the_seam_binds_this_identifier_when_none_is_injected`
  - `tests/intake/test_workers.py::test_the_configured_host_is_the_one_every_paid_call_is_sent_to[identify]`
  - `tests/intake/test_workers.py::test_the_configured_host_is_the_one_every_paid_call_is_sent_to[set]`

Old text:

```
            host=recognition.host,
```

New text:

```
            host=config.DEFAULT_RECOGNITION_HOST,
```

### `r301.B3_refusal_detail_no_key`

The monthly refusal's detail no longer names the key that raises the bound

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r301.json`, row `B3_refusal_detail_no_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 5 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_the_monthly_bound_counts_what_the_ledger_already_holds`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_reads_what_is_owed_and_the_parts_ceiling_reads_the_grid`
  - `tests/intake/test_recognition.py::test_the_monthly_refusal_names_the_key_that_raises_the_bound`
  - `tests/intake/test_workers.py::test_an_unconfigured_machine_meets_a_monthly_bound_before_the_first_call[identify]`
  - `tests/intake/test_workers.py::test_an_unconfigured_machine_meets_a_monthly_bound_before_the_first_call[set]`

Old text:

```
                "key": MONTHLY_KEY,

```

New text:

```
(empty)
```

### `r301.B4_refusal_message_no_key`

The monthly refusal's message is reworded so it no longer names the key

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r301.json`, row `B4_refusal_message_no_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_the_monthly_refusal_names_the_key_that_raises_the_bound`
  - `tests/intake/test_workers.py::test_an_unconfigured_machine_meets_a_monthly_bound_before_the_first_call[identify]`
  - `tests/intake/test_workers.py::test_an_unconfigured_machine_meets_a_monthly_bound_before_the_first_call[set]`

Old text:

```
            f"or raise {MONTHLY_KEY} in the configuration if the plan allows more",
```

New text:

```
            f"or adjust the configured bound if the plan allows more",
```

### `r301.S1_month_ignores_ledger`

Sample of an existing guard: the monthly check ignores what the month already spent

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r301.json`, row `S1_month_ignores_ledger`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 6 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_the_month_is_asked_once_over_the_whole_set_before_the_first_part`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_counts_what_the_ledger_already_holds`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_reads_what_is_owed_and_the_parts_ceiling_reads_the_grid`
  - `tests/intake/test_recognition.py::test_the_monthly_refusal_names_the_key_that_raises_the_bound`
  - `tests/intake/test_workers.py::test_an_unconfigured_machine_meets_a_monthly_bound_before_the_first_call[identify]`
  - `tests/intake/test_workers.py::test_an_unconfigured_machine_meets_a_monthly_bound_before_the_first_call[set]`

Old text:

```
    if budget.monthly is not None and used_this_month + planned > budget.monthly:
```

New text:

```
    if budget.monthly is not None and planned > budget.monthly:
```

### `u57-recognition-and-items.M11_unreached_stop_tenfold`

Fifty unanswered calls in a row before the run stops, not five

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M11_unreached_stop_tenfold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_rejecting_host_stops_the_run_the_same_way`
  - `tests/intake/test_recognition.py::test_five_unanswered_calls_in_a_row_stop_the_run_and_count_what_was_spent`

Old text:

```
UNREACHED_STOP = 5
```

New text:

```
UNREACHED_STOP = 50
```

### `u57-recognition-and-items.M12_quota_reads_as_failure`

The provider's quota answer is raised under the failure slug, not the spend slug

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M12_quota_reads_as_failure`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_cache_that_cannot_be_written_does_not_replace_the_refusal_on_its_way_out`
  - `tests/intake/test_recognition.py::test_a_provider_quota_answer_is_a_spend_refusal_and_never_a_miss`
  - `tests/intake/test_recognition.py::test_the_two_spend_refusals_and_a_miss_are_three_different_things`
  - `tests/intake/test_workers.py::test_a_spend_refusal_at_the_queue_is_reported_as_policy_and_queues_nothing`

Old text:

```
    return refuse(
        "intake-recognition-spend-bound",
        f"the recognition service refused to spend: code {code} ({message or 'no message'}) "
```

New text:

```
    return refuse(
        "intake-recognition-failed",
        f"the recognition service refused to spend: code {code} ({message or 'no message'}) "
```

### `u57-recognition-and-items.M16_grid_off_by_one`

The planned count loses its last chunk

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M16_grid_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 69 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_changed_chunk_plan_misses_the_cache`
  - `tests/intake/test_recognition.py::test_a_changed_file_misses_the_cache`
  - `tests/intake/test_recognition.py::test_a_chunk_that_got_no_answer_is_never_kept_so_only_the_gap_is_paid_again`
  - `tests/intake/test_recognition.py::test_a_document_that_cannot_be_trusted_is_a_miss_and_never_a_tracklist[another-plan]`
  - `tests/intake/test_recognition.py::test_a_document_that_cannot_be_trusted_is_a_miss_and_never_a_tracklist[corrupt]`
  - `tests/intake/test_recognition.py::test_a_document_that_cannot_be_trusted_is_a_miss_and_never_a_tracklist[not-an-object]`
  - `tests/intake/test_recognition.py::test_a_five_hour_mix_is_identified_in_two_even_parts_as_one_set`
  - `tests/intake/test_recognition.py::test_a_ledger_that_cannot_record_stops_the_run_before_the_call`
  - `tests/intake/test_recognition.py::test_a_partition_that_hands_back_an_oversize_part_is_refused_before_any_call[oversize-second-part]`
  - `tests/intake/test_recognition.py::test_a_pass_that_raised_keeps_what_it_had_already_paid_for`
  - `tests/intake/test_recognition.py::test_a_provider_quota_answer_is_a_spend_refusal_and_never_a_miss`
  - `tests/intake/test_recognition.py::test_a_recording_that_cannot_be_digested_is_identified_without_the_cache_and_says_so`
  - `tests/intake/test_recognition.py::test_a_recording_that_cannot_be_measured_or_carved_fails_without_a_call`
  - `tests/intake/test_recognition.py::test_a_run_where_no_call_got_an_answer_is_a_failure_and_not_an_empty_set`
  - `tests/intake/test_recognition.py::test_a_second_pass_over_an_unchanged_recording_spends_nothing`
  - ... and 54 more, see the JSON sidecar

Old text:

```
    return (whole - chunk_s) // interval_s + 1
```

New text:

```
    return (whole - chunk_s) // interval_s
```

### `u57-recognition-and-items.M18_missing_credential_is_unready`

A credential missing after the gate is reported as the gate class, not as credential-missing

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M18_missing_credential_is_unready`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_credential_missing_after_the_gate_is_credential_missing_with_its_own_remedy`

Old text:

```
            "credential-missing" if missing else "intake-recognition-unready",
```

New text:

```
            "intake-recognition-unready",
```

### `u57-recognition-and-items.M1_miss_family_loses_1001`

1001, the service's own no result code, falls out of the miss family

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M1_miss_family_loses_1001`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 48 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_changed_chunk_plan_misses_the_cache`
  - `tests/intake/test_recognition.py::test_a_changed_file_misses_the_cache`
  - `tests/intake/test_recognition.py::test_a_chunk_that_got_no_answer_is_never_kept_so_only_the_gap_is_paid_again`
  - `tests/intake/test_recognition.py::test_a_document_from_another_cache_version_is_a_miss`
  - `tests/intake/test_recognition.py::test_a_document_that_cannot_be_trusted_is_a_miss_and_never_a_tracklist[another-plan]`
  - `tests/intake/test_recognition.py::test_a_document_that_cannot_be_trusted_is_a_miss_and_never_a_tracklist[corrupt]`
  - `tests/intake/test_recognition.py::test_a_document_that_cannot_be_trusted_is_a_miss_and_never_a_tracklist[not-an-object]`
  - `tests/intake/test_recognition.py::test_a_five_hour_mix_is_identified_in_two_even_parts_as_one_set`
  - `tests/intake/test_recognition.py::test_a_pass_that_paid_for_nothing_writes_nothing_and_reports_nothing_unwritten`
  - `tests/intake/test_recognition.py::test_a_pass_that_raised_keeps_what_it_had_already_paid_for`
  - `tests/intake/test_recognition.py::test_a_recording_that_cannot_be_digested_is_identified_without_the_cache_and_says_so`
  - `tests/intake/test_recognition.py::test_a_recording_that_cannot_be_measured_or_carved_fails_without_a_call`
  - `tests/intake/test_recognition.py::test_a_second_pass_over_an_unchanged_recording_spends_nothing`
  - `tests/intake/test_recognition.py::test_a_set_nobody_recognised_is_zero_rows_with_the_misses_counted_not_a_refusal`
  - `tests/intake/test_recognition.py::test_a_set_that_fits_one_run_is_one_part`
  - ... and 33 more, see the JSON sidecar

Old text:

```
_MISS_CODES = frozenset({1001, 2004, 3015})
```

New text:

```
_MISS_CODES = frozenset({2004, 3015})
```

### `u57-recognition-and-items.M2_quota_family_empty`

3003 stops being a quota answer, so a spent account reads as unclassified

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M2_quota_family_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 6 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_cache_that_cannot_be_written_does_not_replace_the_refusal_on_its_way_out`
  - `tests/intake/test_recognition.py::test_a_pass_that_raised_keeps_what_it_had_already_paid_for`
  - `tests/intake/test_recognition.py::test_a_provider_quota_answer_is_a_spend_refusal_and_never_a_miss`
  - `tests/intake/test_recognition.py::test_every_status_code_lands_in_exactly_one_family[payload4-quota]`
  - `tests/intake/test_recognition.py::test_the_two_spend_refusals_and_a_miss_are_three_different_things`
  - `tests/intake/test_workers.py::test_a_spend_refusal_at_the_queue_is_reported_as_policy_and_queues_nothing`

Old text:

```
_QUOTA_CODES = frozenset({3003})
```

New text:

```
_QUOTA_CODES = frozenset()
```

### `u57-recognition-and-items.M3_auth_family_loses_3001`

3001, a missing or invalid access key, stops being a credential answer

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M3_auth_family_loses_3001`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_credential_answer_ends_the_run_as_auth_failed`
  - `tests/intake/test_recognition.py::test_every_status_code_lands_in_exactly_one_family[payload5-auth]`

Old text:

```
_AUTH_CODES = frozenset({3001, 3002, 3006, 3014})
```

New text:

```
_AUTH_CODES = frozenset({3002, 3006, 3014})
```

### `u57-recognition-and-items.M4_transient_range_dropped`

The 2000s stop being transient, so a recording error ends the run as unclassified

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M4_transient_range_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_transient_answer_or_a_transport_that_raised_skips_the_chunk_and_is_counted`
  - `tests/intake/test_recognition.py::test_every_status_code_lands_in_exactly_one_family[payload10-transient]`
  - `tests/intake/test_recognition.py::test_every_status_code_lands_in_exactly_one_family[payload11-transient]`
  - `tests/intake/test_recognition.py::test_every_status_code_lands_in_exactly_one_family[payload9-transient]`

Old text:

```
    if 2000 <= code < 3000 or code in _TRANSIENT_CODES:
```

New text:

```
    if code in _TRANSIENT_CODES:
```

### `u57-recognition-and-items.M5_empty_music_not_none`

A match answer carrying no music entry is indexed rather than read as none

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M5_empty_music_not_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_match_with_no_music_and_a_malformed_score_are_handled`

Old text:

```
    if not isinstance(music, list) or not music:
        return None
```

New text:

```
    if not isinstance(music, list):
        return None
```

### `u57-recognition-and-items.M6_score_constant`

Every hit scores zero, so the fold can never prefer a better answer

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M6_score_constant`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_match_becomes_a_wanted_row_with_the_version_split_and_the_isrc_kept`
  - `tests/intake/test_recognition.py::test_adjacent_answers_for_one_recording_fold_to_the_first_offset_and_best_score`

Old text:

```
    try:
        score = int(top.get("score", 0))
    except (TypeError, ValueError):
        score = 0
```

New text:

```
    score = 0
```

### `u57-recognition-and-items.M7_fold_never_takes_best_score`

Adjacent answers fold to the first, whatever the later one scored

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M7_fold_never_takes_best_score`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_adjacent_answers_for_one_recording_fold_to_the_first_offset_and_best_score`

Old text:

```
            if found.score > last.score:
```

New text:

```
            if False:
```

### `r679-a.A1_supersede_guard_both_layers`

supersede: drop the empty column condition from the read and the write together, so a person's verdict is overwritten

- File: `src/cratekit/core/review.py`
- Source: `r679-a.json`, row `A1_supersede_guard_both_layers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_review_queue.py`, `tests/test_match_states.py`, `tests/intake/test_workers.py`
- Collected: 879 against a baseline of 879
- Kills: 5 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_persons_answer_is_never_overwritten_by_a_later_resolution`
  - `tests/test_review_queue.py::test_supersede_never_overwrites_a_persons_verdict[accepted]`
  - `tests/test_review_queue.py::test_supersede_never_overwrites_a_persons_verdict[rejected]`
  - `tests/test_review_queue.py::test_supersede_never_overwrites_a_verdict_this_build_cannot_read`
  - `tests/test_review_queue.py::test_supersede_takes_several_identifiers_and_retires_only_the_open_ones_among_them`

Old text:

```
            f"SELECT item_id FROM review_items WHERE item_id IN ({marks}) "
            f"AND verdict IS NULL ORDER BY ordinal",
            wanted,
        )
    )
    if not open_ids:
        return ()
    now = timestamp()
    marks = ", ".join("?" for _ in open_ids)
    with store.immediate() as conn:
        conn.execute(
            f"UPDATE review_items SET verdict = ?, option = NULL, actor = ?, decided = ?, "
            f"updated = ? WHERE item_id IN ({marks}) AND verdict IS NULL",
```

New text:

```
            f"SELECT item_id FROM review_items WHERE item_id IN ({marks}) "
            f"ORDER BY ordinal",
            wanted,
        )
    )
    if not open_ids:
        return ()
    now = timestamp()
    marks = ", ".join("?" for _ in open_ids)
    with store.immediate() as conn:
        conn.execute(
            f"UPDATE review_items SET verdict = ?, option = NULL, actor = ?, decided = ?, "
            f"updated = ? WHERE item_id IN ({marks})",
```

### `r679-a.A3_supersede_readers_predicate`

supersede: widen the write's condition to the reader's unresolved predicate, so a verdict a newer build wrote is overwritten

- File: `src/cratekit/core/review.py`
- Source: `r679-a.json`, row `A3_supersede_readers_predicate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_review_queue.py`, `tests/test_match_states.py`, `tests/intake/test_workers.py`
- Collected: 879 against a baseline of 879
- Kills: 1 (killed)
- Killed:
  - `tests/test_review_queue.py::test_supersede_never_overwrites_a_verdict_this_build_cannot_read`

Old text:

```
            f"SELECT item_id FROM review_items WHERE item_id IN ({marks}) "
            f"AND verdict IS NULL ORDER BY ordinal",
            wanted,
        )
    )
    if not open_ids:
        return ()
    now = timestamp()
    marks = ", ".join("?" for _ in open_ids)
    with store.immediate() as conn:
        conn.execute(
            f"UPDATE review_items SET verdict = ?, option = NULL, actor = ?, decided = ?, "
            f"updated = ? WHERE item_id IN ({marks}) AND verdict IS NULL",
```

New text:

```
            f"SELECT item_id FROM review_items WHERE item_id IN ({marks}) "
            f"AND (verdict IS NULL OR verdict NOT IN ('accepted', 'rejected', 'superseded')) ORDER BY ordinal",
            wanted,
        )
    )
    if not open_ids:
        return ()
    now = timestamp()
    marks = ", ".join("?" for _ in open_ids)
    with store.immediate() as conn:
        conn.execute(
            f"UPDATE review_items SET verdict = ?, option = NULL, actor = ?, decided = ?, "
            f"updated = ? WHERE item_id IN ({marks}) AND (verdict IS NULL OR verdict NOT IN ('accepted', 'rejected', 'superseded'))",
```

### `r679-a.A4_resolve_admits_the_machines_verdict`

resolve: drop the refusal of the machine's verdict, so a batch or an import can land it with a candidate

- File: `src/cratekit/core/review.py`
- Source: `r679-a.json`, row `A4_resolve_admits_the_machines_verdict`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_review_queue.py`, `tests/test_match_states.py`, `tests/intake/test_workers.py`
- Collected: 879 against a baseline of 879
- Kills: 1 (killed)
- Killed:
  - `tests/test_review_queue.py::test_resolve_and_the_batch_refuse_the_machines_verdict`

Old text:

```
    if verdict not in PERSON_VERDICTS:
        # The machine's verdict has its own writer with its own invariants: no
```

New text:

```
    if False:
        # The machine's verdict has its own writer with its own invariants: no
```

### `r679-a.A5_import_routes_through_resolve`

import: send an incoming superseded verdict through resolve rather than supersede

- File: `src/cratekit/core/review.py`
- Source: `r679-a.json`, row `A5_import_routes_through_resolve`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_review_queue.py`, `tests/test_match_states.py`, `tests/intake/test_workers.py`
- Collected: 879 against a baseline of 879
- Kills: 2 (killed)
- Killed:
  - `tests/test_review_queue.py::test_an_export_carrying_the_third_verdict_imports_without_conflict`
  - `tests/test_review_queue.py::test_an_import_carries_the_machines_verdict_under_the_machines_rules`

Old text:

```
        if verdict is Verdict.SUPERSEDED:
            # The machine's verdict travels under the machine's rules: the
```

New text:

```
        if False:
            # The machine's verdict travels under the machine's rules: the
```

### `r679-a.A6_empty_rule_admitted`

supersede: drop the refusal of an empty rule, so a superseded item can name nothing

- File: `src/cratekit/core/review.py`
- Source: `r679-a.json`, row `A6_empty_rule_admitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_review_queue.py`, `tests/test_match_states.py`, `tests/intake/test_workers.py`
- Collected: 879 against a baseline of 879
- Kills: 2 (killed)
- Killed:
  - `tests/test_review_queue.py::test_an_import_carries_the_machines_verdict_under_the_machines_rules`
  - `tests/test_review_queue.py::test_supersede_refuses_an_empty_rule`

Old text:

```
    if not rule:
        raise refuse(
            "review-selection-invalid",
            "a superseded item names the rule that owned its row; an empty one "
```

New text:

```
    if False:
        raise refuse(
            "review-selection-invalid",
            "a superseded item names the rule that owned its row; an empty one "
```

### `r679-a.A7_person_verdicts_are_all_verdicts`

PERSON_VERDICTS: include the machine's verdict, so the command line offers it

- File: `src/cratekit/core/review.py`
- Source: `r679-a.json`, row `A7_person_verdicts_are_all_verdicts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_review_queue.py`, `tests/test_match_states.py`, `tests/intake/test_workers.py`
- Collected: 879 against a baseline of 879
- Kills: 2 (killed)
- Killed:
  - `tests/test_review_queue.py::test_resolve_and_the_batch_refuse_the_machines_verdict`
  - `tests/test_review_queue.py::test_the_command_line_offers_a_person_only_the_persons_verdicts`

Old text:

```
    member for member in Verdict if member is not Verdict.SUPERSEDED
```

New text:

```
    member for member in Verdict
```

### `r679-a.A8_actor_is_not_the_rule`

supersede: write a fixed word as the actor instead of the rule that owned the row

- File: `src/cratekit/core/review.py`
- Source: `r679-a.json`, row `A8_actor_is_not_the_rule`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_review_queue.py`, `tests/test_match_states.py`, `tests/intake/test_workers.py`
- Collected: 879 against a baseline of 879
- Kills: 11 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_an_intake_job_that_owns_a_row_by_isrc_retires_the_question_an_earlier_job_asked`
  - `tests/test_match_states.py::test_a_retired_question_whose_row_goes_missing_keeps_the_verdict`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[credited-exact]`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[isrc-exact]`
  - `tests/test_match_states.py::test_the_verb_lists_a_retired_question_only_when_asked_for_everything`
  - `tests/test_review_queue.py::test_a_batch_resolution_does_not_touch_items_a_resolution_superseded`
  - `tests/test_review_queue.py::test_a_superseded_item_offered_again_is_neither_reopened_nor_duplicated`
  - `tests/test_review_queue.py::test_an_export_carrying_the_third_verdict_imports_without_conflict`
  - `tests/test_review_queue.py::test_an_import_carries_the_machines_verdict_under_the_machines_rules`
  - `tests/test_review_queue.py::test_supersede_retires_an_open_item_naming_the_rule_and_it_leaves_the_open_list`
  - `tests/test_review_queue.py::test_supersede_takes_several_identifiers_and_retires_only_the_open_ones_among_them`

Old text:

```
            (str(Verdict.SUPERSEDED), rule, now, now, *open_ids),
```

New text:

```
            (str(Verdict.SUPERSEDED), "resolution", now, now, *open_ids),
```

### `r816-a.A1_too_coarse_protection`

plan_rows: drop the rule that a too coarse file word does not replace a specific row word

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-a.json`, row `A1_too_coarse_protection`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 6 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_second_run_after_a_clean_one_asks_and_is_a_no_op`
  - `tests/test_tag_rows.py::test_a_too_coarse_file_does_not_replace_a_specific_row`
  - `tests/test_tag_rows.py::test_every_live_row_is_counted_exactly_once_and_items_are_in_identifier_order`
  - `tests/test_tag_rows.py::test_planned_written_and_read_back_through_the_two_acts`
  - `tests/test_tag_rows.py::test_the_apply_writes_the_genre_and_no_other_column_of_any_row`
  - `tests/test_tag_rows.py::test_the_pairs_are_the_writes_counted_largest_first`

Old text:

```
        elif _protected(declared, row_word, file_word):
```

New text:

```
        elif False:
```

### `r816-a.A2_held_out`

plan_rows: ignore the rows a person held out, so a hand set genre is planned as a write

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-a.json`, row `A2_held_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_held_row_survives_the_write_and_the_apply_must_name_it_again`
  - `tests/test_tag_rows.py::test_a_row_a_person_holds_out_is_listed_and_left`

Old text:

```
        if content_id in held_out:
```

New text:

```
        if False:
```

### `r816-a.A3_multi_valued`

plan_rows: write a row from a file holding more than one genre

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-a.json`, row `A3_multi_valued`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_file_holding_two_genres_is_left_alone_and_both_are_shown`
  - `tests/test_tag_rows.py::test_two_genres_in_an_id3_frame_read_as_they_do_in_a_list_container`

Old text:

```
            if several:
```

New text:

```
            if False:
```

### `r816-a.A4_agreement`

plan_rows: stop reading equal words as agreement, so every row with a file genre is a write

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-a.json`, row `A4_agreement`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 12 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_file_holding_two_genres_is_left_alone_and_both_are_shown`
  - `tests/test_tag_rows.py::test_a_row_and_file_that_agree_are_not_in_the_plan`
  - `tests/test_tag_rows.py::test_a_second_apply_plans_nothing_and_writes_nothing`
  - `tests/test_tag_rows.py::test_a_second_run_after_a_clean_one_asks_and_is_a_no_op`
  - `tests/test_tag_rows.py::test_an_empty_plan_still_asks_and_opens_nothing_to_write`
  - `tests/test_tag_rows.py::test_an_empty_second_value_is_not_a_second_genre_and_not_an_unknown_word`
  - `tests/test_tag_rows.py::test_an_identifier_held_out_that_names_no_differing_row_is_carried_and_digested`
  - `tests/test_tag_rows.py::test_every_live_row_is_counted_exactly_once_and_items_are_in_identifier_order`
  - `tests/test_tag_rows.py::test_planned_written_and_read_back_through_the_two_acts`
  - `tests/test_tag_rows.py::test_the_apply_writes_the_genre_and_no_other_column_of_any_row`
  - `tests/test_tag_rows.py::test_the_digest_moves_when_only_a_count_moves`
  - `tests/test_tag_rows.py::test_two_genres_in_an_id3_frame_read_as_they_do_in_a_list_container`

Old text:

```
        if row_word == file_word:
```

New text:

```
        if False:
```

### `r816-a.A5_unreadable_is_blank`

_file_word: count a file whose tags would not open as a file with no genre

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-a.json`, row `A5_unreadable_is_blank`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_file_no_tag_library_opens_is_unreadable_and_not_blank`
  - `tests/test_tag_rows.py::test_every_live_row_is_counted_exactly_once_and_items_are_in_identifier_order`

Old text:

```
        return "", FILE_UNREADABLE
```

New text:

```
        return "", FILE_BLANK
```

### `r816-a.A6_first_value`

_file_word: compare the checked reader's text as it came, null bytes and all

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-a.json`, row `A6_first_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_an_empty_second_value_is_not_a_second_genre_and_not_an_unknown_word`
  - `tests/test_tag_rows.py::test_two_genres_in_an_id3_frame_read_as_they_do_in_a_list_container`

Old text:

```
    word = next((part.strip() for part in text.split("\x00") if part.strip()), "")
```

New text:

```
    word = text.strip()
```

### `r816-a.A7_digest_counts`

RowsPlan.digest: leave the outcome counts out of the digest

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-a.json`, row `A7_digest_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_the_digest_moves_when_only_a_count_moves`

Old text:

```
                "counts": dict(self.counts),

```

New text:

```
(empty)
```

### `r816-a.A8_leave_unmatched`

plan_rows: drop the identifiers held out that name no differing row

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-a.json`, row `A8_leave_unmatched`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_mistyped_identifier_is_shown_at_the_gate_and_warned_about`
  - `tests/test_tag_rows.py::test_an_identifier_held_out_that_names_no_differing_row_is_carried_and_digested`

Old text:

```
        leave_unmatched=tuple(sorted(held_out - listed)),
```

New text:

```
        leave_unmatched=(),
```

### `r816-b.B1_stale_check`

apply_rows: write without asking whether each row is still as the plan read it

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-b.json`, row `B1_stale_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_row_removed_since_the_plan_refuses_and_nothing_is_written`
  - `tests/test_tag_rows.py::test_a_row_whose_genre_moved_since_the_plan_refuses_and_nothing_is_written`

Old text:

```
    assert_rows_as_planned(plan, mapped)

```

New text:

```
(empty)
```

### `r816-b.B2_stale_tombstone`

assert_rows_as_planned: write a row removed since the plan

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-b.json`, row `B2_stale_tombstone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 5 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_blank_row_is_as_planned_however_the_database_spells_blank[0_0]`
  - `tests/test_tag_rows.py::test_a_blank_row_is_as_planned_however_the_database_spells_blank[0_1]`
  - `tests/test_tag_rows.py::test_a_blank_row_is_as_planned_however_the_database_spells_blank[None]`
  - `tests/test_tag_rows.py::test_a_blank_row_is_as_planned_however_the_database_spells_blank[]`
  - `tests/test_tag_rows.py::test_a_row_removed_since_the_plan_refuses_and_nothing_is_written`

Old text:

```
        if row is None or trees.soft_delete_marker(row):
```

New text:

```
        if row is None:
```

### `r816-b.B3_blank_spellings`

assert_rows_as_planned: read two spellings of a blank genre as a change

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-b.json`, row `B3_blank_spellings`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_blank_row_is_as_planned_however_the_database_spells_blank[0_0]`
  - `tests/test_tag_rows.py::test_a_blank_row_is_as_planned_however_the_database_spells_blank[0_1]`
  - `tests/test_tag_rows.py::test_a_blank_row_is_as_planned_however_the_database_spells_blank[]`

Old text:

```
        if (_empty(held) and _empty(planned)) or str(held) == str(planned):
```

New text:

```
        if str(held) == str(planned):
```

### `r816-b.B4_restore_detection`

apply_rows: record a fingerprint without first looking for an out of band restore

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-b.json`, row `B4_restore_detection`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_restore_out_of_band_is_marked_before_this_write_replaces_the_evidence`

Old text:

```
    convergence.detect_out_of_band_restore(cfg, db, tree_registry.read(cfg))

```

New text:

```
(empty)
```

### `r816-b.B5_commit_recorded`

apply_rows: leave the landed commit off the session record

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-b.json`, row `B5_commit_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_the_apply_is_a_recorded_session_a_restore_can_undo`

Old text:

```
        # RECORDED THE INSTANT THE COMMIT RETURNS.
        _record_commit(record, written, cfg)

```

New text:

```
        # RECORDED THE INSTANT THE COMMIT RETURNS.

```

### `r816-c.B6_bookkeeping_exempt`

judge: stop exempting the binding's bookkeeping columns, so every clean write reads as moved

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-c.json`, row `B6_bookkeeping_exempt`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 10 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_file_on_a_volume_that_is_not_mounted_is_counted_and_the_run_does_not_fail`
  - `tests/test_tag_rows.py::test_a_held_row_survives_the_write_and_the_apply_must_name_it_again`
  - `tests/test_tag_rows.py::test_a_mistyped_identifier_is_shown_at_the_gate_and_warned_about`
  - `tests/test_tag_rows.py::test_a_person_reads_the_counts_and_the_pairs_at_the_gate_and_after_the_write`
  - `tests/test_tag_rows.py::test_a_second_run_after_a_clean_one_asks_and_is_a_no_op`
  - `tests/test_tag_rows.py::test_a_word_the_library_has_no_row_for_names_the_act_on_a_run_that_wrote`
  - `tests/test_tag_rows.py::test_planned_written_and_read_back_through_the_two_acts`
  - `tests/test_tag_rows.py::test_the_apply_writes_the_genre_and_no_other_column_of_any_row`
  - `tests/test_tag_rows.py::test_the_genre_report_stops_naming_the_old_word_after_the_run`
  - `tests/test_tag_rows.py::test_the_read_back_passes_a_row_whose_genre_and_bookkeeping_alone_moved`

Old text:

```
            and column not in rb_writer.BOOKKEEPING_COLUMNS

```

New text:

```
(empty)
```

### `r816-c.B7_read_back_word`

judge: stop comparing the genre read back with the file's word

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-c.json`, row `B7_read_back_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_the_read_back_names_a_row_that_does_not_carry_its_files_word`
  - `tests/test_tag_rows.py::test_the_read_back_names_a_row_whose_genre_points_at_no_lookup_row`

Old text:

```
        if word != item.file:
```

New text:

```
        if False:
```

### `r816-c.B8_read_back_columns`

judge: stop reporting another column that moved

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-c.json`, row `B8_read_back_columns`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_the_read_back_names_every_other_column_that_moved`

Old text:

```
        if changed:
```

New text:

```
        if False:
```

### `r816-c.B9_cache_reset`

apply_rows: leave the collection cache holding the words as they were

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-c.json`, row `B9_cache_reset`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_the_genre_report_stops_naming_the_old_word_after_the_run`

Old text:

```
    collection.reset_cache()

```

New text:

```
(empty)
```

### `r816-d.C1_acknowledgment`

tag_rows: ask the gate without reading the backup acknowledgment first

- File: `src/cratekit/tagging/rows_cli.py`
- Source: `r816-d.json`, row `C1_acknowledgment`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    session.assert_backup_acknowledged(cfg)

```

New text:

```
(empty)
```

### `r816-d.C2_empty_plan`

tag_rows: open the database to write for a plan that writes nothing

- File: `src/cratekit/tagging/rows_cli.py`
- Source: `r816-d.json`, row `C2_empty_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_second_run_after_a_clean_one_asks_and_is_a_no_op`
  - `tests/test_tag_rows.py::test_an_empty_plan_still_asks_and_opens_nothing_to_write`

Old text:

```
    if not plan.writes:
```

New text:

```
    if False:
```

### `r816-d.C3_majority_unmapped`

_plan: plan over a library most of whose rows are under no prefix rule

- File: `src/cratekit/tagging/rows_cli.py`
- Source: `r816-d.json`, row `C3_majority_unmapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_library_most_of_whose_rows_are_unmapped_refuses_before_the_gate`

Old text:

```
        if totals.majority_unmapped:
```

New text:

```
        if False:
```

### `r816-d.C4_only_apply_writes`

tag_rows: write on any answer

- File: `src/cratekit/tagging/rows_cli.py`
- Source: `r816-d.json`, row `C4_only_apply_writes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_the_plan_refusal_writes_nothing_and_a_declined_gate_writes_nothing`

Old text:

```
    if ctx.gate.require(spec, plan=data, context=_facts(plan)) != "apply":
```

New text:

```
    if ctx.gate.require(spec, plan=data, context=_facts(plan)) == "never":
```

### `r816-d.C5_leave_reaches_the_plan`

_plan: drop the rows held out on the command line

- File: `src/cratekit/tagging/rows_cli.py`
- Source: `r816-d.json`, row `C5_leave_reaches_the_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_held_row_survives_the_write_and_the_apply_must_name_it_again`
  - `tests/test_tag_rows.py::test_a_mistyped_identifier_is_shown_at_the_gate_and_warned_about`

Old text:

```
        return rows.plan_rows(cfg, db, declared, leave=leave)
```

New text:

```
        return rows.plan_rows(cfg, db, declared, leave=())
```

### `u69-b.M10_out_not_a_folder`

Drop the refusal of an --out that exists and is not a folder

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69-b.json`, row `M10_out_not_a_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_file_where_the_folder_should_be_is_refused`

Old text:

```
    if out.exists() and not out.is_dir():
```

New text:

```
    if False:
```

### `u69-b.M12_unlisted_status`

Report unlisted missing tracks as a note instead of a failing check

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69-b.json`, row `M12_unlisted_status`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_missing_row_from_no_provider_is_reported_unlisted_as_a_failing_check`

Old text:

```
"fail" if unlisted else "ok",
```

New text:

```
"info" if unlisted else "ok",
```

### `u69-b.M16_next_command`

Drop the literal next command from the written check a person reads

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69-b.json`, row `M16_next_command`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
written to {written.list_path}; next: {command}"
```

New text:

```
written to {written.list_path}"
```

### `u69-b.M17_lists_folder`

Write into download staging itself rather than its lists folder

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69-b.json`, row `M17_lists_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 8 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_different_list_already_at_the_path_is_refused_and_left_alone`
  - `tests/test_intake_missing.py::test_a_mixed_job_writes_only_the_missing_rows`
  - `tests/test_intake_missing.py::test_a_run_list_is_one_file_a_second_listing_reproduces`
  - `tests/test_intake_missing.py::test_an_earlier_file_that_is_not_a_list_gives_no_reason_rather_than_a_wrong_one`
  - `tests/test_intake_missing.py::test_missing_tracks_none_of_which_can_be_listed_write_the_unlisted_list_not_a_no_op`
  - `tests/test_intake_missing.py::test_the_default_human_output_names_the_list_and_the_next_command`
  - `tests/test_intake_missing.py::test_the_default_human_output_names_the_list_the_download_and_the_landing`
  - `tests/test_intake_missing.py::test_two_playlists_sharing_a_track_list_it_once_with_both_provenances`

Old text:

```
out = intake_cli._load().paths.download_staging / LISTS_DIR
```

New text:

```
out = intake_cli._load().paths.download_staging
```

### `u69-b.M18_inner_cause`

Drop the failed job's own cause from the refusal

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69-b.json`, row `M18_inner_cause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_failed_job_is_refused_carrying_its_own_cause`

Old text:

```
            inner=job.cause,
```

New text:

```
            inner=None,
```

### `u69-b.M19_resume_step`

Drop the resume command from an open job's refusal

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69-b.json`, row `M19_resume_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_an_open_job_is_refused_and_nothing_is_written`

Old text:

```
            f"finish it with: crate {argv}" if job.is_open() else
```

New text:

```
            "finish it first" if job.is_open() else
```

### `u69.M1_handler_key`

Drop the refusal of a job queued under another verb's handler key

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69.json`, row `M1_handler_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_job_of_another_verb_is_refused`

Old text:

```
    if job.handler_key not in intake_cli.INTAKE_KEYS:
```

New text:

```
    if False:
```

### `u69.M2_succeeded_only`

Drop the refusal of a job that is not succeeded (open, failed, cancelled)

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69.json`, row `M2_succeeded_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_failed_job_is_refused_carrying_its_own_cause`
  - `tests/test_intake_missing.py::test_an_open_job_is_refused_and_nothing_is_written`

Old text:

```
    if job.state is not jobs.JobState.SUCCEEDED:
```

New text:

```
    if False:
```

### `u69.M4_report_coverage`

Drop the refusal when the reports do not cover the items one for one

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69.json`, row `M4_report_coverage`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_report_for_the_wrong_item_refuses_even_when_the_count_matches`
  - `tests/test_intake_missing.py::test_fewer_readable_reports_than_items_refuses_rather_than_listing_a_subset`

Old text:

```
    if sorted(reported) != sorted(wanted):
```

New text:

```
    if False:
```

### `u69.M5_by_count`

Compare reports to items by count instead of by identifier

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69.json`, row `M5_by_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_report_for_the_wrong_item_refuses_even_when_the_count_matches`

Old text:

```
    if sorted(reported) != sorted(wanted):
```

New text:

```
    if len(reported) != len(wanted):
```

### `u69.M6_state_word`

Drop the refusal of a report whose state word this verb cannot read

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69.json`, row `M6_state_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_report_with_a_state_this_verb_cannot_read_refuses`

Old text:

```
        if report.get("state") not in _WORDS or not isinstance(report.get("track"), Mapping):
```

New text:

```
        if not isinstance(report.get("track"), Mapping):
```

### `u73-b.B2_every_ref_kept`

Stop accumulating every reference an id came from

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73-b.json`, row `B2_every_ref_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_two_playlists_sharing_a_track_list_it_once_with_both_provenances`

Old text:

```
            refs.append(said)
```

New text:

```
            pass
```

### `u73-b.B3_first_source_wins`

Let the last job an id came from win its provenance instead of the first

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73-b.json`, row `B3_first_source_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_two_playlists_sharing_a_track_list_it_once_with_both_provenances`

Old text:

```
        first.setdefault(ref, job)
```

New text:

```
        first[ref] = job
```

### `u73.A10_every_job_skipped`

Drop the refusal of a run whose every job failed, left to the layer after it

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A10_every_job_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_whose_every_job_failed_refuses_even_with_skip_failed`

Old text:

```
    if not kept:
```

New text:

```
    if False:
```

### `u73.A1_blank_run`

Drop the refusal of a blank --run, so a blank run is compared as it stands

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A1_blank_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_blank_run_is_refused_and_does_not_match_a_job_queued_with_no_run`

Old text:

```
    if not run_id.strip():
```

New text:

```
    if False:
```

### `u73.A2_library_filter`

Drop the library half of the run selection, so the run alone picks jobs

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A2_library_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_another_librarys_job_in_the_same_run_is_not_this_librarys_to_list`

Old text:

```
and job.library_id == library_id
```

New text:

```
and True
```

### `u73.A3_run_filter`

Drop the run half of the selection, so every intake job for the library is listed

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A3_run_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_job_queued_by_hand_is_not_part_of_any_run`
  - `tests/test_intake_missing.py::test_an_unknown_run_is_refused_by_name`

Old text:

```
(job.payload or {}).get(RUN_ID) == run_id
```

New text:

```
True
```

### `u73.A4_intake_key_filter`

Drop the intake handler key filter, so a labels or favourites job in the run is selected

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A4_intake_key_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_job_of_another_verb_in_the_same_run_is_not_listed`

Old text:

```
            if job.handler_key in intake_cli.INTAKE_KEYS
```

New text:

```
            if True
```

### `u73.A5_oldest_first`

Reverse the job order, newest first, so first source wins picks the later playlist

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A5_oldest_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_two_playlists_sharing_a_track_list_it_once_with_both_provenances`

Old text:

```
key=lambda job: (job.created, job.job_id),
```

New text:

```
key=lambda job: (job.created, job.job_id), reverse=True,
```

### `u73.A7_open_refuses`

Drop the refusal of a run holding an open job

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A7_open_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_an_open_job_refuses_the_whole_run_and_names_it`

Old text:

```
    if still_open:
```

New text:

```
    if False:
```

### `u73.A8_failed_refuses`

Drop the refusal of a run holding a failed or cancelled job

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A8_failed_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_failed_job_is_named_and_refuses_the_run_without_skip_failed`

Old text:

```
    if unfinished and not skip_failed:
```

New text:

```
    if False:
```

### `u73.A9_skip_failed_ignored`

Ignore --skip-failed, so a failed job refuses the run whatever the flag says

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A9_skip_failed_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 72 against a baseline of 72
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_whose_every_job_failed_refuses_even_with_skip_failed`
  - `tests/test_intake_missing.py::test_skip_failed_lists_the_rest_and_names_what_it_left_out`
  - `tests/test_intake_missing.py::test_skip_failed_over_tracks_only_handed_on_writes_them_rather_than_refusing`

Old text:

```
    if unfinished and not skip_failed:
```

New text:

```
    if unfinished:
```

### `r706-a.A1_ceiling_dropped`

Drop the parts ceiling, so a file of any length is cut into as many parts as it takes

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-a.json`, row `A1_ceiling_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 6 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_nonsense_duration_is_refused_by_the_bound_before_any_grid_exists`
  - `tests/intake/test_recognition.py::test_a_recording_over_the_parts_ceiling_is_refused_before_any_carve_call_or_credential`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_reads_what_is_owed_and_the_parts_ceiling_reads_the_grid`
  - `tests/intake/test_recognition.py::test_the_per_run_bound_refuses_before_any_carve_call_or_credential`
  - `tests/intake/test_recognition.py::test_the_two_spend_refusals_and_a_miss_are_three_different_things`
  - `tests/intake/test_workers.py::test_a_recording_over_the_parts_ceiling_is_refused_at_the_queue_and_queues_nothing`

Old text:

```
    assert_one_set(spend, planned=planned)
    offsets = sample_offsets(duration_s)
```

New text:

```
    offsets = sample_offsets(duration_s)
```

### `r706-a.A2_ceiling_one_part_wider`

The ceiling admits one part more than MAX_PARTS, a coefficient row on the bound

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-a.json`, row `A2_ceiling_one_part_wider`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_recording_over_the_parts_ceiling_is_refused_before_any_carve_call_or_credential`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_reads_what_is_owed_and_the_parts_ceiling_reads_the_grid`
  - `tests/intake/test_recognition.py::test_the_two_spend_refusals_and_a_miss_are_three_different_things`
  - `tests/intake/test_workers.py::test_a_recording_over_the_parts_ceiling_is_refused_at_the_queue_and_queues_nothing`

Old text:

```
    ceiling = budget.per_run * MAX_PARTS
```

New text:

```
    ceiling = budget.per_run * (MAX_PARTS + 1)
```

### `r706-a.A3_max_parts_four`

MAX_PARTS moves from three to four, the decision's Part A, B and C plus one

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-a.json`, row `A3_max_parts_four`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 5 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_recording_over_the_parts_ceiling_is_refused_before_any_carve_call_or_credential`
  - `tests/intake/test_recognition.py::test_a_two_hour_set_is_one_run_a_five_hour_mix_is_two_parts_and_nine_hours_is_over_the_ceiling`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_reads_what_is_owed_and_the_parts_ceiling_reads_the_grid`
  - `tests/intake/test_recognition.py::test_the_two_spend_refusals_and_a_miss_are_three_different_things`
  - `tests/intake/test_workers.py::test_a_recording_over_the_parts_ceiling_is_refused_at_the_queue_and_queues_nothing`

Old text:

```
MAX_PARTS = 3
```

New text:

```
MAX_PARTS = 4
```

### `r706-a.A4_month_asked_of_one_run`

The month is asked about one run's worth rather than the whole set, so a set the month cannot afford spends its first part

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-a.json`, row `A4_month_asked_of_one_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_the_month_is_asked_once_over_the_whole_set_before_the_first_part`

Old text:

```
        assert_month_within(spend, planned=len(owed), used_this_month=counter.used(month))
```

New text:

```
        assert_month_within(
            spend, planned=min(len(owed), spend.per_run), used_this_month=counter.used(month)
        )
```

### `r706-a.A5_run_guard_dropped`

Drop the per part run guard, so an oversize part is paid for

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-a.json`, row `A5_run_guard_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_partition_that_hands_back_an_oversize_part_is_refused_before_any_call[one-oversize-part]`
  - `tests/intake/test_recognition.py::test_a_partition_that_hands_back_an_oversize_part_is_refused_before_any_call[oversize-second-part]`

Old text:

```
    for part in parts:
        assert_run_within(spend, planned=sum(1 for offset in part if offset in still_owed))
    keys = ("", "")
```

New text:

```
    keys = ("", "")
```

### `r706-a.A6_run_message_reworded`

Reword the per part run refusal, do not append to it

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-a.json`, row `A6_run_message_reworded`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_partition_that_hands_back_an_oversize_part_is_refused_before_any_call[one-oversize-part]`
  - `tests/intake/test_recognition.py::test_a_partition_that_hands_back_an_oversize_part_is_refused_before_any_call[oversize-second-part]`

Old text:

```
            f"this run would take {planned} recognition calls and the per run "
```

New text:

```
            f"this part needs {planned} recognition calls and the per run "
```

### `r706-a.A7_ceiling_message_reworded`

Reword the ceiling refusal so it no longer says the file is not one set

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-a.json`, row `A7_ceiling_message_reworded`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_recording_over_the_parts_ceiling_is_refused_before_any_carve_call_or_credential`

Old text:

```
            f"nothing was sent. A file this long is not one set, so split it "
```

New text:

```
            f"nothing was sent. A file this long is too long, so split it "
```

### `r706-b.B1_partition_front_loads_the_remainder`

The remainder goes to the first part whole instead of one chunk to each of the first parts, so a cut is uneven and can exceed the bound

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-b.json`, row `B1_partition_front_loads_the_remainder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_partition_cuts_the_grid_into_the_fewest_even_parts_under_the_bound[5-2-sizes6]`

Old text:

```
        size = base + (1 if index < extra else 0)
```

New text:

```
        size = base + (extra if index == 0 else 0)
```

### `r706-b.B2_parts_needed_floors`

parts_needed floors instead of ceiling, so 732 chunks is one part of 732

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-b.json`, row `B2_parts_needed_floors`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 8 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_five_hour_mix_is_identified_in_two_even_parts_as_one_set`
  - `tests/intake/test_recognition.py::test_a_two_hour_set_is_one_run_a_five_hour_mix_is_two_parts_and_nine_hours_is_over_the_ceiling`
  - `tests/intake/test_recognition.py::test_partition_cuts_the_grid_into_the_fewest_even_parts_under_the_bound[401-400-sizes3]`
  - `tests/intake/test_recognition.py::test_partition_cuts_the_grid_into_the_fewest_even_parts_under_the_bound[5-2-sizes6]`
  - `tests/intake/test_recognition.py::test_partition_cuts_the_grid_into_the_fewest_even_parts_under_the_bound[7-3-sizes7]`
  - `tests/intake/test_recognition.py::test_partition_cuts_the_grid_into_the_fewest_even_parts_under_the_bound[732-400-sizes4]`
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`
  - `tests/intake/test_workers.py::test_identify_only_says_the_same_parts_note`

Old text:

```
    return -(-planned // per_run)
```

New text:

```
    return max(1, planned // per_run)
```

### `r706-b.B3_partition_drops_the_remainder`

Every part is cut to the base size, so the remainder chunks fall out of the grid

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-b.json`, row `B3_partition_drops_the_remainder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 5 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_partition_cuts_the_grid_into_the_fewest_even_parts_under_the_bound[401-400-sizes3]`
  - `tests/intake/test_recognition.py::test_partition_cuts_the_grid_into_the_fewest_even_parts_under_the_bound[5-2-sizes6]`
  - `tests/intake/test_recognition.py::test_partition_cuts_the_grid_into_the_fewest_even_parts_under_the_bound[7-3-sizes7]`
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`
  - `tests/intake/test_workers.py::test_identify_only_says_the_same_parts_note`

Old text:

```
        parts.append(tuple(offsets[start : start + size]))
```

New text:

```
        parts.append(tuple(offsets[start : start + base]))
```

### `r706-b.B4_parts_reported_as_one`

The result says one part whatever the cut

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-b.json`, row `B4_parts_reported_as_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 7 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_five_hour_mix_is_identified_in_two_even_parts_as_one_set`
  - `tests/intake/test_recognition.py::test_a_split_set_is_served_from_the_cache_as_one_plan`
  - `tests/intake/test_recognition.py::test_a_split_set_that_owes_only_a_gap_meets_the_run_bound_on_what_is_owed`
  - `tests/intake/test_recognition.py::test_the_month_is_asked_once_over_the_whole_set_before_the_first_part`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_reads_what_is_owed_and_the_parts_ceiling_reads_the_grid`
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`
  - `tests/intake/test_workers.py::test_identify_only_says_the_same_parts_note`

Old text:

```
        parts=len(parts),
```

New text:

```
        parts=1,
```

### `r706-b.B5_chunks_count_the_first_part`

The walked grid is rebuilt from the first part only, so chunks and cached count one part

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-b.json`, row `B5_chunks_count_the_first_part`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 6 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_five_hour_mix_is_identified_in_two_even_parts_as_one_set`
  - `tests/intake/test_recognition.py::test_a_split_set_is_served_from_the_cache_as_one_plan`
  - `tests/intake/test_recognition.py::test_a_split_set_that_owes_only_a_gap_meets_the_run_bound_on_what_is_owed`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_reads_what_is_owed_and_the_parts_ceiling_reads_the_grid`
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`
  - `tests/intake/test_workers.py::test_identify_only_says_the_same_parts_note`

Old text:

```
    offsets = tuple(offset for part in parts for offset in part)
```

New text:

```
    offsets = tuple(parts[0]) if parts else ()
```

### `r706-b.B6_grid_not_partitioned`

identify hands the whole grid over as one part, so the run guard meets a 5 hour mix

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-b.json`, row `B6_grid_not_partitioned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 7 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_five_hour_mix_is_identified_in_two_even_parts_as_one_set`
  - `tests/intake/test_recognition.py::test_a_split_set_is_served_from_the_cache_as_one_plan`
  - `tests/intake/test_recognition.py::test_a_split_set_that_owes_only_a_gap_meets_the_run_bound_on_what_is_owed`
  - `tests/intake/test_recognition.py::test_the_month_is_asked_once_over_the_whole_set_before_the_first_part`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_reads_what_is_owed_and_the_parts_ceiling_reads_the_grid`
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`
  - `tests/intake/test_workers.py::test_identify_only_says_the_same_parts_note`

Old text:

```
    parts = partition(offsets, per_run=spend.per_run)
```

New text:

```
    parts = (offsets,)
```

### `r44-a.S10_default_slug`

Look the slug up with a default, so a verdict in neither table wears the mismatch slug

- File: `src/cratekit/core/session.py`
- Source: `r44-a.json`, row `S10_default_slug`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 473 against a baseline of 473
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_verdict_in_neither_table_fails_rather_than_wearing_the_mismatch_slug`

Old text:

```
            reason = _MAPPED_REASONS[status.state]
```

New text:

```
            reason = _MAPPED_REASONS.get(status.state, "mapped-volume-mismatch")
```

### `r44-a.S1_empty_slot`

Never refuse an empty mount slot, so an identity read through an ejected drive's leftover directory is compared and can match

- File: `src/cratekit/core/session.py`
- Source: `r44-a.json`, row `S1_empty_slot`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 473 against a baseline of 473
- Kills: 2 (killed)
- Killed:
  - `tests/test_write_session.py::test_an_ejected_drive_is_never_offered_the_boot_disks_identity_to_record`
  - `tests/test_write_session.py::test_an_empty_mount_slot_refuses_even_when_the_recorded_identity_matches_it`

Old text:

```
        source = preflight.identity_source(probe)
        if source is None:
```

New text:

```
        source = preflight.identity_source(probe)
        if False:
```

### `r44-a.S2_proved_widened`

Let NOT_MOUNTED count as a proved identity, which is the pass set widening by one verdict

- File: `src/cratekit/core/session.py`
- Source: `r44-a.json`, row `S2_proved_widened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 473 against a baseline of 473
- Kills: 4 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_drive_ejected_mid_queue_is_not_settled_as_a_queue_of_deletions`
  - `tests/test_write_session.py::test_a_recorded_volume_that_is_not_mounted_anywhere_has_its_own_slug`
  - `tests/test_write_session.py::test_every_mount_verdict_about_a_rule_target_was_decided_exactly_once[MountState.NOT_MOUNTED]`
  - `tests/test_write_session.py::test_the_verdicts_that_prove_a_rule_target_are_spelled_out`

Old text:

```
    {preflight.MountState.OK, preflight.MountState.LIBRARY_PATH_MISSING}
)
```

New text:

```
    {
        preflight.MountState.OK,
        preflight.MountState.LIBRARY_PATH_MISSING,
        preflight.MountState.NOT_MOUNTED,
    }
)
```

### `r44-a.S3_default_to_library`

Hold a rule outside the library root with nothing recorded to the LIBRARY'S identity instead of refusing it

- File: `src/cratekit/core/session.py`
- Source: `r44-a.json`, row `S3_default_to_library`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 473 against a baseline of 473
- Kills: 2 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_rule_is_held_to_its_own_identity_then_the_librarys_then_to_nothing`
  - `tests/test_write_session.py::test_a_target_outside_the_root_with_nothing_recorded_refuses_and_hands_over_the_identity`

Old text:

```
    if inside.resolution is locations.Resolution.UNDER_ROOT:
        return cfg.library.volume_id
    return None
```

New text:

```
    if inside.resolution is locations.Resolution.UNDER_ROOT:
        return cfg.library.volume_id
    return cfg.library.volume_id
```

### `r44-a.S4_inside_root_unheld`

Hold a rule inside the library root to nothing of the library's, so a nested foreign volume is judged as unrecorded rather than foreign

- File: `src/cratekit/core/session.py`
- Source: `r44-a.json`, row `S4_inside_root_unheld`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 473 against a baseline of 473
- Kills: 6 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_rule_onto_the_wrong_volume_refuses_rather_than_trashing_the_only_copy`
  - `tests/test_write_session.py::test_a_different_disk_at_a_rules_target_refuses_and_names_the_rule`
  - `tests/test_write_session.py::test_a_foreign_volume_under_a_rule_that_recorded_nothing_offers_nothing_to_record`
  - `tests/test_write_session.py::test_a_rule_is_held_to_its_own_identity_then_the_librarys_then_to_nothing`
  - `tests/test_write_session.py::test_a_volume_nested_under_the_library_root_is_not_the_library`
  - `tests/test_write_session.py::test_the_file_is_proved_where_the_file_is_and_not_where_the_rule_points`

Old text:

```
    if inside.resolution is locations.Resolution.UNDER_ROOT:
        return cfg.library.volume_id
    return None
```

New text:

```
    return None
```

### `r44-a.S5_not_destructive`

Assert a rule target at read strength, where an unreadable or unrecorded identity is tolerated

- File: `src/cratekit/core/session.py`
- Source: `r44-a.json`, row `S5_not_destructive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 473 against a baseline of 473
- Kills: 5 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_rule_onto_the_wrong_volume_refuses_rather_than_trashing_the_only_copy`
  - `tests/test_write_session.py::test_a_provider_that_cannot_read_the_identity_to_hand_over_is_a_refusal_too`
  - `tests/test_write_session.py::test_a_rule_target_whose_identity_cannot_be_read_refuses`
  - `tests/test_write_session.py::test_a_target_outside_the_root_with_nothing_recorded_refuses_and_hands_over_the_identity`
  - `tests/test_write_session.py::test_the_seams_handed_in_are_the_seams_used`

Old text:

```
                expected_rule_identity(cfg, rule),
                destructive=True,
```

New text:

```
                expected_rule_identity(cfg, rule),
                destructive=False,
```

### `r44-a.S6_oserror_escapes`

Let an OSError from the walk or the identity read escape the gate instead of becoming a refusal

- File: `src/cratekit/core/session.py`
- Source: `r44-a.json`, row `S6_oserror_escapes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 473 against a baseline of 473
- Kills: 2 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_provider_that_cannot_read_the_identity_to_hand_over_is_a_refusal_too`
  - `tests/test_write_session.py::test_a_way_to_the_target_this_account_cannot_walk_is_a_refusal_and_not_a_traceback`

Old text:

```
    except OSError as exc:
        # "I COULD NOT LOOK" IS ITS OWN ANSWER.
```

New text:

```
    except KeyboardInterrupt as exc:
        # "I COULD NOT LOOK" IS ITS OWN ANSWER.
```

### `r44-a.S7_probe_the_target`

Probe the rule's target for a file instead of the file's own directory, so a volume nested under the target is never seen

- File: `src/cratekit/core/session.py`
- Source: `r44-a.json`, row `S7_probe_the_target`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 473 against a baseline of 473
- Kills: 3 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_drive_ejected_mid_queue_is_not_settled_as_a_queue_of_deletions`
  - `tests/test_deletion.py::test_a_file_in_a_volume_nested_under_the_rules_target_is_not_moved`
  - `tests/test_write_session.py::test_the_file_is_proved_where_the_file_is_and_not_where_the_rule_points`

Old text:

```
        rules[index],
        Path(path).parent,
```

New text:

```
        rules[index],
        Path(rules[index].target or "/"),
```

### `r44-a.S8_wording_held_to`

Say the volume was recorded on the rule when the identity compared was the library's

- File: `src/cratekit/core/session.py`
- Source: `r44-a.json`, row `S8_wording_held_to`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 473 against a baseline of 473
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_foreign_volume_under_a_rule_that_recorded_nothing_offers_nothing_to_record`

Old text:

```
    return "the library's volume, which a target inside the library root is held to"
```

New text:

```
    return "the volume recorded on that rule"
```

### `r44-a.S9_offer_to_record_nested`

Offer to record the foreign volume's identity on a rule that recorded none

- File: `src/cratekit/core/session.py`
- Source: `r44-a.json`, row `S9_offer_to_record_nested`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 473 against a baseline of 473
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_foreign_volume_under_a_rule_that_recorded_nothing_offers_nothing_to_record`

Old text:

```
        if rule.volume_id and observed:
```

New text:

```
        if observed:
```

### `u71-b.B10_occupied_at_move`

Drop the occupied check at the move, so os.replace can take a file's place

- File: `src/cratekit/intake/landing.py`
- Source: `u71-b.json`, row `B10_occupied_at_move`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 2 (killed)
- Killed:
  - `tests/test_landing.py::test_a_file_arriving_between_the_passes_is_not_replaced`
  - `tests/test_landing.py::test_every_file_taken_at_the_move_writes_no_intake_file`

Old text:

```
        occupied = _occupied(item, final)
```

New text:

```
        occupied = None
```

### `u71-b.B11_nothing_moved`

Drop the refusal after the move loop when nothing moved

- File: `src/cratekit/intake/landing.py`
- Source: `u71-b.json`, row `B11_nothing_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_every_file_taken_at_the_move_writes_no_intake_file`

Old text:

```
    if not moved:
        if made:
```

New text:

```
    if False:
        if made:
```

### `u71-b.B12_take_back_folder`

Keep the batch folder this call made when the first move fails

- File: `src/cratekit/intake/landing.py`
- Source: `u71-b.json`, row `B12_take_back_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_a_first_move_that_fails_leaves_no_batch_folder`

Old text:

```
            if made and not moved:
                _remove_if_empty(target)

```

New text:

```
(empty)
```

### `u71-b.B13_unlink_destination`

Leave the intake file behind when place_files fails after writing it

- File: `src/cratekit/intake/landing.py`
- Source: `u71-b.json`, row `B13_unlink_destination`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        destination.unlink(missing_ok=True)

```

New text:

```
(empty)
```

### `u71-b.B1_target_under_staging`

Drop the refusal of a landing target under download staging

- File: `src/cratekit/intake/landing.py`
- Source: `u71-b.json`, row `B1_target_under_staging`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_a_landing_target_under_staging_is_refused`

Old text:

```
    if resolved == staging or staging in resolved.parents:
```

New text:

```
    if False:
```

### `u71-b.B2_device`

Drop the cross device refusal, so a move across devices is attempted

- File: `src/cratekit/intake/landing.py`
- Source: `u71-b.json`, row `B2_device`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_a_staging_folder_on_another_device_is_refused_by_name`

Old text:

```
    if here is None or there is None or here != there:
```

New text:

```
    if False:
```

### `u71-b.B3_destination_exists`

Drop the refusal of an intake file that already exists

- File: `src/cratekit/intake/landing.py`
- Source: `u71-b.json`, row `B3_destination_exists`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_an_existing_intake_file_is_never_overwritten`

Old text:

```
    if destination.exists():
```

New text:

```
    if False:
```

### `u71-b.B4_export_missing`

Drop the missing export refusal before any move

- File: `src/cratekit/intake/landing.py`
- Source: `u71-b.json`, row `B4_export_missing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_a_missing_export_is_refused_before_any_move`

Old text:

```
    if not export.is_file():
```

New text:

```
    if False:
```

### `u71-b.B5_trial_splice`

Drop the trial splice on a copy, so a stub is met only after the moves

- File: `src/cratekit/intake/landing.py`
- Source: `u71-b.json`, row `B5_trial_splice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_a_stub_export_is_refused_before_any_move`

Old text:

```
    collection_xml.splice_tracks(trial, [])

```

New text:

```
(empty)
```

### `u71-b.B6_trial_playlist`

Drop the refusal of an export whose intake playlist cannot be written

- File: `src/cratekit/intake/landing.py`
- Source: `u71-b.json`, row `B6_trial_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_an_export_with_no_intake_folder_is_refused_before_any_move`

Old text:

```
    if error:
```

New text:

```
    if False:
```

### `u71-c.C1_nothing_movable_rerun`

Drop the refusal before the batch folder is made when nothing can move

- File: `src/cratekit/intake/landing.py`
- Source: `u71-c.json`, row `C1_nothing_movable_rerun`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_a_batch_where_nothing_lands_leaves_no_batch_folder`

Old text:

```
    if not movable:
```

New text:

```
    if False:
```

### `u71.A10_root_absent`

Drop the refusal of an absent library root before the device probe

- File: `src/cratekit/intake/landing.py`
- Source: `u71.json`, row `A10_root_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_an_absent_library_root_is_refused_before_the_device_probe`

Old text:

```
    if not root.is_dir():
```

New text:

```
    if False:
```

### `u71.A11_owned_folder`

Drop the refusal of a source folder the library already owns

- File: `src/cratekit/intake/landing.py`
- Source: `u71.json`, row `A11_owned_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_a_folder_the_library_already_owns_is_refused`

Old text:

```
    if not in_staging and (source == owned or owned in source.parents):
```

New text:

```
    if False:
```

### `u71.A12_staging_inside_library`

Drop the exemption for staging configured inside the library root

- File: `src/cratekit/intake/landing.py`
- Source: `u71.json`, row `A12_staging_inside_library`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 2 (killed)
- Killed:
  - `tests/test_landing.py::test_a_landing_target_under_staging_is_refused`
  - `tests/test_landing.py::test_staging_configured_inside_the_library_still_lands`

Old text:

```
    in_staging = source == staging or staging in source.parents
```

New text:

```
    in_staging = False
```

