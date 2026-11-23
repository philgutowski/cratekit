# Mutation table: u325-before-l-19

Measured by `scripts/mutate.py` on 2026-11-23 00:58 UTC, branch `HEAD` at `539638eb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22663 collected. pytest invocations for this batch: 140.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:15 UTC for commit `539638ebe629`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 55, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22663 against 22663. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r1634.M17_check_drops_how` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 131 | 5 | killed |
| `u277.M10_next_says_no_canary` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 131 | 12 | killed |
| `u135.A13_live_inbox_ignores_parent` | `src/cratekit/intake/native.py` | user | 1 file(s) | 12 | 1 | killed |
| `u135.A2_set_order_falls_to_name_order` | `src/cratekit/intake/native.py` | user | 1 file(s) | 12 | 1 | killed |
| `u135.A5_recorded_inbox_skips_job_key` | `src/cratekit/intake/native.py` | user | 1 file(s) | 12 | 1 | killed |
| `u194.W24_write_copy_bytes_stale` | `src/cratekit/cli/verbs/taxonomy.py` | user | 2 file(s) | 128 | 1 | killed |
| `u194.W25_write_copy_read_back` | `src/cratekit/cli/verbs/taxonomy.py` | user | 2 file(s) | 128 | 2 | killed |
| `r290-author.S07_rebuild_call_removed` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 126 | 6 | killed |
| `r312.W6_type_not_carried` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 126 | 1 | killed |
| `r840-c.C4_no_name_is_the_empty_string` | `src/cratekit/label/catalogue.py` | user | 2 file(s) | 354 | 2 | killed |
| `u243.D14_screen_never_says_ignored` | `src/cratekit/deletion/cli.py` | user | 2 file(s) | 349 | 2 | killed |
| `r924.A3_cached_count_zero` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 119 | 1 | killed |
| `r924.A7_kept_chunks_counted` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 119 | 1 | killed |
| `u267.M10_done_reading_leaks_own` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 115 | 3 | killed |
| `u267.M8_close_closes_nothing` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 115 | 5 | killed |
| `u131.K6_adopt_not_made` | `src/cratekit/modules/outbound/ledger.py` | user | 2 file(s) | 114 | 1 | killed |
| `u131.K7_kind_folders_kept` | `src/cratekit/modules/outbound/ledger.py` | user | 2 file(s) | 114 | 5 | killed |
| `r879-a.C11_sole_exact_ignores_full` | `src/cratekit/intake/candidates.py` | user | 2 file(s) | 112 | 4 | killed |
| `r879-a.C1_full_reads_total_not_last_page` | `src/cratekit/intake/candidates.py` | user | 2 file(s) | 112 | 5 | killed |
| `r1103.H2_refusal_slug` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 331 | 4 | killed |
| `r1665.R1_log_not_restored` | `src/cratekit/core/restore.py` | user | 7 file(s) | 327 | 4 | killed |
| `u164.T6_reuse_recorded` | `src/cratekit/intake/shelve.py` | user | 3 file(s) | 105 | 5 | killed |
| `u164.R1_record_filed` | `src/cratekit/intake/native.py` | user | 3 file(s) | 105 | 7 | killed |
| `r1255.S9_gate_unlisted_detail` | `src/cratekit/core/session.py` | maintainer | 3 file(s) | 326 | 2 | killed |
| `r290-author.S08_route_resort_call_removed` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 323 | 11 | killed |
| `r1056.S1_no_landing_step_names_intake_missing` | `src/cratekit/sync/mark_cli.py` | user | 2 file(s) | 102 | 4 | killed |
| `r1056.S2_unreachable_step_names_sync` | `src/cratekit/sync/mark_cli.py` | user | 2 file(s) | 102 | 1 | killed |
| `u132.G1_undeclared_cause` | `src/cratekit/write/genre_favorites.py` | user | 5 file(s) | 319 | 2 | killed |
| `r1032.A2_tie_always_broken` | `src/cratekit/modules/outbound/tidal_account.py` | user | 4 file(s) | 316 | 15 | killed |
| `r835-c.S2_sync_hands_the_ledger_to_the_sweep_again` | `src/cratekit/sync/cli.py` | user | 4 file(s) | 315 | 1 | killed |
| `r1115.S1_sync_land_stops_on_unsettled` | `src/cratekit/cli/sync_land.py` | user | 2 file(s) | 93 | 2 | killed |
| `r1115.S2_sync_land_names_the_refused` | `src/cratekit/cli/sync_land.py` | user | 2 file(s) | 93 | 2 | killed |
| `r1056.N6_no_nothing_filed_warning` | `src/cratekit/label/mark_cli.py` | user | 2 file(s) | 89 | 4 | killed |
| `r1056.N7_nothing_filed_against_any_year` | `src/cratekit/label/mark_cli.py` | user | 2 file(s) | 89 | 1 | killed |
| `u243.L10_empties_never_said` | `src/cratekit/modules/outbound/prune.py` | user | 2 file(s) | 84 | 1 | killed |
| `u243.L9_prune_ignores_tombstones` | `src/cratekit/modules/outbound/prune.py` | user | 2 file(s) | 84 | 6 | killed |
| `u184.A1_flag_ignored` | `src/cratekit/session/cli.py` | user | 3 file(s) | 81 | 10 | killed |
| `u184.A2_any_actor_accepted` | `src/cratekit/session/cli.py` | user | 3 file(s) | 81 | 3 | killed |
| `u285.M1_seam_installs` | `src/cratekit/core/rb_writer.py` | user | 4 file(s) | 289 | 6 | killed |
| `u242.M6_record_v1_reads_a_taken_key` | `src/cratekit/sync/mark_record.py` | user | 2 file(s) | 78 | 1 | killed |
| `u242.M26_release_stamps_no_mark` | `src/cratekit/sync/unmark_cli.py` | user | 2 file(s) | 78 | 3 | killed |
| `u185.G1_commit_guard_called` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 277 | 13 | killed |
| `u40-author-full.C3_resume_without_run` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 70 | 3 | killed |
| `u40-author-full.C4_resume_always_runs` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 70 | 1 | killed |
| `u164.W1_apply_folder` | `src/cratekit/intake/landing.py` | user | 2 file(s) | 69 | 32 | killed |
| `u164.T3_free_stored` | `src/cratekit/intake/shelve.py` | user | 2 file(s) | 69 | 2 | killed |
| `u261.O1_catalogue_drops_the_app` | `src/cratekit/label/tidal_catalogue.py` | user | 3 file(s) | 270 | 3 | killed |
| `u270.L2_row_only_for_a_recorded_track` | `src/cratekit/modules/outbound/ledger.py` | user | 4 file(s) | 259 | 1 | killed |
| `u114.M19_write_intent` | `src/cratekit/tagging/suggest_cli.py` | user | 1 file(s) | 59 | 1 | killed |
| `u114.M20_pick_declared` | `src/cratekit/tagging/suggest_cli.py` | user | 1 file(s) | 59 | 1 | killed |
| `u177.C3_flag_beside_label` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 58 | 1 | killed |
| `u177.C4_flag_ignored` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 58 | 5 | killed |
| `u205.S3_catalogue_lookup_ignores_app` | `src/cratekit/label/tidal_catalogue.py` | user | 3 file(s) | 256 | 15 | killed |
| `u293.S4_label_go_holds` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 253 | 2 | killed |
| `u211.W3_strict_at_commit` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 251 | 2 | killed |
| `u164.T2_free_disk` | `src/cratekit/intake/shelve.py` | user | 2 file(s) | 53 | 3 | killed |
| `u164.T5_empty_subject` | `src/cratekit/intake/shelve.py` | user | 2 file(s) | 53 | 1 | killed |
| `u27-restore-cli-round-2.S3_analysis_watch_watches_nothing` | `src/cratekit/session/restore_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `u169.N5_repair_scan_bypasses` | `src/cratekit/intake/repair_cli.py` | user | 2 file(s) | 48 | 2 | killed |
| `u169.N6_repair_apply_bypasses` | `src/cratekit/intake/repair_cli.py` | user | 2 file(s) | 48 | 1 | killed |
| `r1032.A10_reason_words_reworded` | `src/cratekit/modules/outbound/tidal_account.py` | user | 3 file(s) | 241 | 6 | killed |
| `u246.S14_unmark_narrowed_empty` | `src/cratekit/sync/unmark_cli.py` | user | 2 file(s) | 47 | 3 | killed |
| `u246.S15_unmark_narrowed_first_only` | `src/cratekit/sync/unmark_cli.py` | user | 2 file(s) | 47 | 1 | killed |
| `u113-c.C7_unproven_import_names` | `src/cratekit/intake/rotate.py` | user | 2 file(s) | 46 | 1 | killed |
| `u113-c.C9_earliest_name_wins` | `src/cratekit/intake/rotate.py` | user | 2 file(s) | 46 | 1 | killed |
| `u110-c.C5_missing_hint` | `src/cratekit/intake/missing_cli.py` | user | 5 file(s) | 238 | 1 | killed |
| `r1255.F1_refill_plan_unlisted` | `src/cratekit/intake/refill.py` | user | 2 file(s) | 43 | 1 | killed |
| `r1255.F2_refill_warning_wording` | `src/cratekit/intake/refill_cli.py` | user | 2 file(s) | 43 | 2 | killed |
| `r1313.T1_account_skips_the_classifier` | `src/cratekit/modules/outbound/tidal_account.py` | user | 3 file(s) | 227 | 5 | killed |
| `u216.M25_dated_no_time` | `src/cratekit/modules/outbound/tidal_account.py` | user | 3 file(s) | 227 | 1 | killed |
| `u153.L1_facts_colour_count` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 37 | 1 | killed |
| `u153.N1_restamp_id_text` | `src/cratekit/intake/native.py` | user | 2 file(s) | 37 | 9 | killed |
| `u102-a.D1_keep_is_not_accept` | `src/cratekit/intake/repair.py` | user | 2 file(s) | 35 | 1 | killed |
| `u102-a.D2_open_is_not_accepted` | `src/cratekit/intake/repair.py` | user | 2 file(s) | 35 | 1 | killed |
| `u192.T4_tag_queue_only_ignored` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 221 | 7 | killed |
| `u219-composites.G6_answer_pinned` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 221 | 1 | killed |
| `r338-c.C6_only_the_first_root_is_watched` | `src/cratekit/core/analysis_store.py` | user | 1 file(s) | 32 | 1 | killed |
| `u25.G15_barren_watch` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `u113-a.A8_pending_any_state` | `src/cratekit/intake/account_playlists.py` | user | 1 file(s) | 32 | 1 | killed |
| `u113-b.B6_root_names_unheld` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 32 | 1 | killed |
| `r685-a.V1_route_inbox_export_reads_the_shipped_text` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 215 | 4 | killed |
| `u177.A6_first_of_two` | `src/cratekit/label/registry.py` | user | 6 file(s) | 190 | 2 | killed |
| `r290-author.S06_label_call_removed` | `src/cratekit/label/cli.py` | user | 2 file(s) | 208 | 17 | killed |
| `u129-author.A12_archive_backfill_swallows_all` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 24 | 1 | killed |

## Row definitions

### `r1634.M17_check_drops_how`

label sync --next: the reverified line no longer says how the release was asked

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1634.json`, row `M17_check_drops_how`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_sync.py`
- Collected: 131 against a baseline of 131
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_provider_crediting_another_label_still_answers_nothing_new`
  - `tests/test_label_canary.py::test_a_provider_that_answers_with_no_credit_for_the_new_ones_answers_nothing_new`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_passed_over_for_the_next_and_the_label_has_nothing_new`
  - `tests/test_label_canary.py::test_an_unanswered_release_with_no_held_release_to_read_refuses_as_before`

Old text:

```
                f"{listing.canary.how()}: {listing.canary.said()}",
```

New text:

```
                f": {listing.canary.said()}",
```

### `u277.M10_next_says_no_canary`

_listing_checks: never say the reverified line, so --next is silent about which release it re-verified

- File: `src/cratekit/label/sync_cli.py`
- Source: `u277.json`, row `M10_next_says_no_canary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_sync.py`
- Collected: 131 against a baseline of 131
- Kills: 12 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_the_newest_held_release_names_the_label`
  - `tests/test_label_canary.py::test_a_degraded_provider_still_refuses_though_a_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_provider_crediting_another_label_still_answers_nothing_new`
  - `tests/test_label_canary.py::test_a_provider_that_answers_turns_the_same_shape_into_nothing_new`
  - `tests/test_label_canary.py::test_a_provider_that_answers_with_no_credit_for_the_new_ones_answers_nothing_new`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_never_replaced_by_another_acts`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_passed_over_for_the_next_and_the_label_has_nothing_new`
  - `tests/test_label_canary.py::test_an_unanswered_release_with_no_held_release_to_read_refuses_as_before`
  - `tests/test_label_canary.py::test_held_releases_whose_lines_name_another_act_still_refuse`
  - `tests/test_label_canary.py::test_the_record_names_the_release_re_verified_and_what_it_answered`
  - `tests/test_label_canary.py::test_two_withdrawn_held_releases_refuse_and_no_third_is_read`

Old text:

```
    if listing.canary is not None:
```

New text:

```
    if False:
```

### `u135.A13_live_inbox_ignores_parent`

live_inbox_named matches the name anywhere, not only under the intake root

- File: `src/cratekit/intake/native.py`
- Source: `u135.json`, row `A13_live_inbox_ignores_parent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u135_set_inbox_join.py`
- Collected: 12 against a baseline of 12
- Kills: 1 (killed)
- Killed:
  - `tests/test_u135_set_inbox_join.py::test_a_dated_batch_from_before_the_unit_is_named_as_a_leftover_and_not_joined`

Old text:

```
        if str(getattr(row, "ParentID", "") or "") == str(root_id):
            return True

```

New text:

```
        if True:
            return True

```

### `u135.A2_set_order_falls_to_name_order`

INBOX members follow landing file name order even when a set playlist is planned

- File: `src/cratekit/intake/native.py`
- Source: `u135.json`, row `A2_set_order_falls_to_name_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u135_set_inbox_join.py`
- Collected: 12 against a baseline of 12
- Kills: 1 (killed)
- Killed:
  - `tests/test_u135_set_inbox_join.py::test_one_landing_of_a_set_files_its_inbox_playlist_in_set_order_not_name_order`

Old text:

```
            if plan.set_playlist is not None:
                ordered = []
                seen: set[str] = set()
                for member in plan.set_playlist.members:
                    target = str(member.target) if member.target else ""
                    if not target or target not in by_target or target in claimed:
                        continue
                    held = by_target[target]
                    if held in seen:
                        continue
                    ordered.append(held)
                    seen.add(held)
                for row in plan.rows:
                    target = str(row.target)
                    if target not in by_target or target in claimed:
                        continue
                    held = by_target[target]
                    if held in seen:
                        continue
                    ordered.append(held)
                    seen.add(held)
            else:
                ordered = [
                    by_target[str(row.target)]
                    for row in plan.rows
                    if str(row.target) in by_target and str(row.target) not in claimed
                ]

```

New text:

```
            ordered = [
                by_target[str(row.target)]
                for row in plan.rows
                if str(row.target) in by_target and str(row.target) not in claimed
            ]

```

### `u135.A5_recorded_inbox_skips_job_key`

recorded_inbox_playlist ignores the job key so any closed batch playlist is treated as this job's

- File: `src/cratekit/intake/native.py`
- Source: `u135.json`, row `A5_recorded_inbox_skips_job_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u135_set_inbox_join.py`
- Collected: 12 against a baseline of 12
- Kills: 1 (killed)
- Killed:
  - `tests/test_u135_set_inbox_join.py::test_a_dated_batch_from_before_the_unit_is_named_as_a_leftover_and_not_joined`

Old text:

```
        and record.detail[BATCH_PLAYLIST_KEY].get(INBOX_JOB_KEY) == job_id

```

New text:

```
        and True

```

### `u194.W24_write_copy_bytes_stale`

write_copy: drop the byte check after the second plan, so an edit made since is written over

- File: `src/cratekit/cli/verbs/taxonomy.py`
- Source: `u194.json`, row `W24_write_copy_bytes_stale`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`, `tests/test_taxonomy_upgrade.py`
- Collected: 128 against a baseline of 128
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_an_edit_after_the_second_plan_is_refused_as_stale`

Old text:

```
    if as_read(raw) != before:
```

New text:

```
    if False:
```

### `u194.W25_write_copy_read_back`

write_copy: drop the read back, so a copy that does not load is left as every verb's declaration

- File: `src/cratekit/cli/verbs/taxonomy.py`
- Source: `u194.json`, row `W25_write_copy_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`, `tests/test_taxonomy_upgrade.py`
- Collected: 128 against a baseline of 128
- Kills: 2 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_a_copy_that_does_not_read_back_is_replaced_by_the_one_it_replaced`
  - `tests/test_taxonomy_upgrade.py::test_a_restore_that_fails_says_so_and_names_the_backup`

Old text:

```
    problem = _read_back(cfg, path, written)
    if problem is not None:
```

New text:

```
    problem = _read_back(cfg, path, written)
    if False:
```

### `r290-author.S07_rebuild_call_removed`

Remove the one jobs.raise_for_state call from cli/rebuild.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/cli/rebuild.py`
- Source: `r290-author.json`, row `S07_rebuild_call_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`
- Collected: 126 against a baseline of 126
- Kills: 6 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[rebuild]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[rebuild]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[rebuild]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[rebuild]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[rebuild]`
  - `tests/test_job_outcome.py::test_every_function_that_drives_a_job_maps_its_ending_afterwards`

Old text:

```
jobs.raise_for_state(job)
```

New text:

```
jobs.get  # the mapping call, removed
```

### `r312.W6_type_not_carried`

_with_left_behind: rebuild as a plain CratekitError, dropping the blocked or cancelled type

- File: `src/cratekit/write/routing_cli.py`
- Source: `r312.json`, row `W6_type_not_carried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`
- Collected: 126 against a baseline of 126
- Kills: 1 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_reworded_refusal_is_rebuilt_in_one_place_only`

Old text:

```
    return rebuilt(
        error,
        replace(
            cause,
```

New text:

```
    return CratekitError(
        replace(
            cause,
```

### `r840-c.C4_no_name_is_the_empty_string`

artist_name: answer with the text of whatever the artist's name attribute holds, so an object with no name reads None

- File: `src/cratekit/label/catalogue.py`
- Source: `r840-c.json`, row `C4_no_name_is_the_empty_string`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/modules/test_labels.py`
- Collected: 354 against a baseline of 354
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_an_artist_that_is_already_text_or_has_no_name_is_read_as_what_it_is[held2-]`
  - `tests/test_label_tidal_catalogue.py::test_an_artist_that_is_already_text_or_has_no_name_is_read_as_what_it_is[held3-]`

Old text:

```
    return name if isinstance(name, str) else ""
```

New text:

```
    return str(name)
```

### `u243.D14_screen_never_says_ignored`

deletion.cli._shown: the count of rows excused as no local file is never put on the gate screen

- File: `src/cratekit/deletion/cli.py`
- Source: `u243.json`, row `D14_screen_never_says_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion_streaming.py`, `tests/test_deletion.py`
- Collected: 349 against a baseline of 349
- Kills: 2 (killed)
- Killed:
  - `tests/test_deletion.py::test_delete_review_says_on_the_refusal_that_a_first_run_accepted_history`
  - `tests/test_deletion_streaming.py::test_delete_review_trashes_a_removed_file_beside_streaming_rows`

Old text:

```
    if ignored:
        shown["ignored, not local files"] = ignored
```

New text:

```
    if False:
        shown["ignored, not local files"] = ignored
```

### `r924.A3_cached_count_zero`

The plan line is told nothing was cached

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r924.json`, row `A3_cached_count_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`, `tests/intake/test_workers.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_a_cached_recording_says_so_and_counts_no_calls`

Old text:

```
        progress(_plan_line(len(offsets), cached=len(offsets) - len(owed), parts=len(parts)))
```

New text:

```
        progress(_plan_line(len(offsets), cached=0, parts=len(parts)))
```

### `r924.A7_kept_chunks_counted`

A chunk the cache answered speaks the counter as if it were paid

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r924.json`, row `A7_kept_chunks_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`, `tests/intake/test_workers.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_a_cached_recording_says_so_and_counts_no_calls`

Old text:

```
            if progress is not None and calls > before and _worth_saying(calls, len(owed)):
```

New text:

```
            if progress is not None and _worth_saying(calls, len(owed)):
```

### `u267.M10_done_reading_leaks_own`

done_reading: never close a reader's own handle, so every reader of the run that answers a gate leaks one

- File: `src/cratekit/core/rb_writer.py`
- Source: `u267.json`, row `M10_done_reading_leaks_own`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_organize.py`
- Collected: 115 against a baseline of 115
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_a_reader_with_no_shared_read_closes_its_own_handle`
  - `tests/test_organize_one_read.py::test_the_applying_run_opens_exactly_as_it_did`
  - `tests/test_organize_one_read.py::test_the_report_says_exactly_what_it_said_with_an_open_per_step`

Old text:

```
    if shared is None:
        close_db(db)
```

New text:

```
    if shared is None:
        pass
```

### `u267.M8_close_closes_nothing`

SharedRead.close: forget the handle without close_db, so its engine and pooled connection stay open

- File: `src/cratekit/core/rb_writer.py`
- Source: `u267.json`, row `M8_close_closes_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_organize.py`
- Collected: 115 against a baseline of 115
- Kills: 5 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_a_failure_nobody_expected_still_closes_the_handle`
  - `tests/test_organize_one_read.py::test_a_shared_read_opens_at_its_first_read_and_once`
  - `tests/test_organize_one_read.py::test_a_step_that_refuses_after_the_open_leaves_no_handle_open`
  - `tests/test_organize_one_read.py::test_the_report_opens_the_database_once_and_closes_it_once`
  - `tests/test_organize_one_read.py::test_the_sets_step_reads_inspiration_through_the_one_handle`

Old text:

```
        if db is not None:
            close_db(db)
```

New text:

```
        if db is not None:
            pass
```

### `u131.K6_adopt_not_made`

ledger.reserve_kind_folder: record an adopted folder as made here

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u131.json`, row `K6_adopt_not_made`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_playlist_kinds.py`, `tests/test_organize.py`
- Collected: 114 against a baseline of 114
- Kills: 1 (killed)
- Killed:
  - `tests/test_playlist_kinds.py::test_a_hand_made_folder_named_mine_is_adopted_and_never_emptied`

Old text:

```
            document["kind_folders"][kind] = {"folder_id": adopt, "created": False}
```

New text:

```
            document["kind_folders"][kind] = {"folder_id": adopt, "created": True}
```

### `u131.K7_kind_folders_kept`

ledger._load: drop the kind folder records on read, so the next write forgets them

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u131.json`, row `K7_kind_folders_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_playlist_kinds.py`, `tests/test_organize.py`
- Collected: 114 against a baseline of 114
- Kills: 5 (killed)
- Killed:
  - `tests/test_playlist_kinds.py::test_a_playlist_marked_after_it_was_filed_in_mine_reaches_its_year`
  - `tests/test_playlist_kinds.py::test_a_renamed_playlist_and_a_renamed_folder_stay_where_they_are`
  - `tests/test_playlist_kinds.py::test_a_stale_kind_folder_record_is_replaced`
  - `tests/test_playlist_kinds.py::test_each_kind_lands_in_its_own_folder`
  - `tests/test_playlist_kinds.py::test_the_kind_folders_record_survives_another_write`

Old text:

```
            for kind, value in kind_folders.items()
            if value.get("folder_id")
```

New text:

```
            for kind, value in kind_folders.items()
            if False
```

### `r879-a.C11_sole_exact_ignores_full`

sole_exact (existing, sampled): drop the full page condition, so a bound reached answer lists its one exact candidate

- File: `src/cratekit/intake/candidates.py`
- Source: `r879-a.json`, row `C11_sole_exact_ignores_full`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`, `tests/test_intake_missing_search.py`
- Collected: 112 against a baseline of 112
- Kills: 4 (killed)
- Killed:
  - `tests/test_export_set.py::test_an_empty_page_after_full_ones_ends_the_listing_and_a_full_last_page_never_lists`
  - `tests/test_export_set.py::test_the_page_bound_reached_leaves_it_out_and_says_so`
  - `tests/test_export_set.py::test_the_walk_never_asks_past_the_providers_ceiling_of_300`
  - `tests/test_intake_missing_search.py::test_a_full_page_is_never_the_whole_answer_so_its_one_exact_hit_is_offered`

Old text:

```
    if answer.ambiguous or answer.full:
```

New text:

```
    if answer.ambiguous:
```

### `r879-a.C1_full_reads_total_not_last_page`

Answer.full: read the total hits rather than the last page, so a walk that read a full page then a short one still reads as cut short

- File: `src/cratekit/intake/candidates.py`
- Source: `r879-a.json`, row `C1_full_reads_total_not_last_page`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`, `tests/test_intake_missing_search.py`
- Collected: 112 against a baseline of 112
- Kills: 5 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_full_first_page_with_one_exact_and_a_second_with_none_lists_it`
  - `tests/test_export_set.py::test_an_empty_page_after_full_ones_ends_the_listing_and_a_full_last_page_never_lists`
  - `tests/test_export_set.py::test_an_exact_match_on_the_second_page_alone_is_listed`
  - `tests/test_export_set.py::test_no_exact_match_on_any_page_leaves_it_out_as_none`
  - `tests/test_export_set.py::test_the_same_exact_track_served_again_on_the_next_page_is_one`

Old text:

```
        last = self.hits if self.last_page is None else self.last_page
```

New text:

```
        last = self.hits
```

### `r1103.H2_refusal_slug`

handle: the item fails under the general analysis-write-failed slug instead of retag's own

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r1103.json`, row `H2_refusal_slug`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_reserved_causes.py`
- Collected: 331 against a baseline of 331
- Kills: 4 (killed)
- Killed:
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_is_named_in_the_human_answer`
  - `tests/test_tag_workers.py::test_a_retag_whose_only_file_will_not_take_its_genre_names_no_reload`

Old text:

```
        raise refuse(
            retag.UNWRITTEN_REASON,
```

New text:

```
        raise refuse(
            "analysis-write-failed",
```

### `r1665.R1_log_not_restored`

restore._file_steps: never write back a restored companion, so the log's rows are lost

- File: `src/cratekit/core/restore.py`
- Source: `r1665.json`, row `R1_log_not_restored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 327 against a baseline of 327
- Kills: 4 (killed)
- Killed:
  - `tests/test_restore.py::test_only_the_companion_the_inventory_declares_restored_is_written_back`
  - `tests/test_restore.py::test_round3_a_staged_log_is_counted_as_permanent_growth`
  - `tests/test_restore.py::test_round3_a_volume_between_the_two_rules_is_refused`
  - `tests/test_snapshot_wal_r1665.py::test_a_capture_taken_while_a_handle_holds_the_log_restores_what_it_recorded`

Old text:

```
        if entry.source in restored_companions:
            if entry.captured is not None:
```

New text:

```
        if entry.source in restored_companions:
            if False:
```

### `u164.T6_reuse_recorded`

landing_target: never go back to the folder recorded for a batch landed into again

- File: `src/cratekit/intake/shelve.py`
- Source: `u164.json`, row `T6_reuse_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_rehearse.py`
- Collected: 105 against a baseline of 105
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_name_landed_into_again_goes_back_to_its_folder_unless_the_folder_is_gone`
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_landing_that_adds_no_row_needs_no_majority`
  - `tests/test_intake_land_native.py::test_the_same_files_staged_again_are_refused_at_the_move_and_the_collection_is_unchanged`
  - `tests/test_intake_land_rehearse.py::test_a_name_the_live_batch_folder_holds_is_refused_at_the_area_as_it_will_be_live`

Old text:

```
    if again is not None and os.path.isdir(again) and not os.path.islink(again):
        return Path(again)
```

New text:

```
    if False:
        return Path(again)
```

### `u164.R1_record_filed`

_record_landing_commit: never record the filed batch and its folder

- File: `src/cratekit/intake/native.py`
- Source: `u164.json`, row `R1_record_filed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_rehearse.py`
- Collected: 105 against a baseline of 105
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_name_landed_into_again_goes_back_to_its_folder_unless_the_folder_is_gone`
  - `tests/test_intake_land_filed.py::test_shelve_over_a_batch_landed_filed_reports_nothing_to_do`
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_landing_that_adds_no_row_needs_no_majority`
  - `tests/test_intake_land_native.py::test_the_same_files_staged_again_are_refused_at_the_move_and_the_collection_is_unchanged`
  - `tests/test_intake_land_rehearse.py::test_a_name_the_live_batch_folder_holds_is_refused_at_the_area_as_it_will_be_live`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_a_batch_filed_in_another_year_is_refused`

Old text:

```
    if plan.folder is not None and plan.batch:
        record.detail[FILED_BATCH_KEY]
```

New text:

```
    if False:
        record.detail[FILED_BATCH_KEY]
```

### `r1255.S9_gate_unlisted_detail`

assert_no_unresolved_session: drop the unlisted flag from the refusal's detail

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S9_gate_unlisted_detail`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_restore.py`, `tests/test_write_session.py`
- Collected: 326 against a baseline of 326
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_an_unreadable_record_keeps_its_own_refusal`
  - `tests/test_session_log_unlisted.py::test_the_unresolved_session_gate_refuses_over_a_log_it_cannot_list`

Old text:

```
                "unreadable": [str(path) for path in unreadable],
                "unlisted": log_unlisted(unreadable, cfg),
            },
        )


def resolve_unverified_session(
```

New text:

```
                "unreadable": [str(path) for path in unreadable],
            },
        )


def resolve_unverified_session(
```

### `r290-author.S08_route_resort_call_removed`

Remove the one jobs.raise_for_state call from write/routing_cli.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/write/routing_cli.py`
- Source: `r290-author.json`, row `S08_route_resort_call_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_routing_workers.py`
- Collected: 323 against a baseline of 323
- Kills: 11 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[route.resort]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[route.resort]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[route.resort]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[route.resort]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[route.resort]`
  - `tests/test_job_outcome.py::test_every_function_that_drives_a_job_maps_its_ending_afterwards`
  - `tests/test_routing_workers.py::test_a_refusal_raised_before_the_drive_carries_no_leftover_step`
  - `tests/test_routing_workers.py::test_a_resort_that_failed_part_way_still_names_what_the_finished_tree_left`
  - `tests/test_routing_workers.py::test_a_resort_that_failed_with_nothing_left_behind_adds_no_step`
  - `tests/test_routing_workers.py::test_a_resume_whose_items_did_not_all_succeed_is_not_an_ok_exit[resort]`
  - `tests/test_routing_workers.py::test_a_second_process_names_what_the_first_ones_tree_left`

Old text:

```
jobs.raise_for_state(job)
```

New text:

```
jobs.get  # the mapping call, removed
```

### `r1056.S1_no_landing_step_names_intake_missing`

_native_proof: drop the named source from the no landing step, so a label batch is told intake missing

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r1056.json`, row `S1_no_landing_step_names_intake_missing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`, `tests/test_sync_mark.py`
- Collected: 102 against a baseline of 102
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_pass_no_closed_committed_native_landing_names_is_refused_by_name[abandoned]`
  - `tests/test_label_mark_native.py::test_a_pass_no_closed_committed_native_landing_names_is_refused_by_name[another-pass]`
  - `tests/test_label_mark_native.py::test_a_pass_no_closed_committed_native_landing_names_is_refused_by_name[never-committed]`
  - `tests/test_label_mark_native.py::test_a_pass_no_closed_committed_native_landing_names_is_refused_by_name[no-landing]`

Old text:

```
            f"land the pass with crate intake land --pass and {named}, then run {verb} "
```

New text:

```
            f"land the pass with crate intake land --pass and {SYNC_PASS_NAMED}, then run {verb} "
```

### `r1056.S2_unreachable_step_names_sync`

_native_proof: name sync mark in the unreachable library step whatever verb asked

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r1056.json`, row `S2_unreachable_step_names_sync`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`, `tests/test_sync_mark.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_an_unreachable_library_names_label_mark_as_the_verb_to_run_again`

Old text:

```
            f"mount the library volume, then run {verb} again",
```

New text:

```
            "mount the library volume, then run crate sync mark again",
```

### `u132.G1_undeclared_cause`

The additive half's skip over an undeclared class carries no cause

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u132.json`, row `G1_undeclared_cause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`, `tests/test_genre_favorites.py`, `tests/test_genre_favorites_adoption.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_routing_workers.py`
- Collected: 319 against a baseline of 319
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_drive_that_adds_nothing_still_names_an_undeclared_favorites_class`
  - `tests/test_genre_favorites_adoption.py::test_an_adoption_over_a_taxonomy_without_the_class_names_the_skipped_step`

Old text:

```
            cause=CLASS_UNDECLARED,

```

New text:

```
            cause="",

```

### `r1032.A2_tie_always_broken`

_among: break the tie whatever the caller asked, so a heart or a pair takes a release R-572 refuses

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1032.json`, row `A2_tie_always_broken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_sync_pair.py`, `tests/test_organize_mirror_tie.py`
- Collected: 316 against a baseline of 316
- Kills: 15 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_file_album_matching_both_releases_stays_unmatched`
  - `tests/test_outbound_tidal_account.py::test_a_file_album_naming_neither_release_stays_unmatched_and_says_so`
  - `tests/test_outbound_tidal_account.py::test_a_file_with_no_album_tag_stays_unmatched_and_says_the_tag_is_missing`
  - `tests/test_outbound_tidal_account.py::test_a_heart_on_a_release_the_row_does_not_name_decides_nothing`
  - `tests/test_outbound_tidal_account.py::test_a_reason_does_not_outlive_the_match_it_was_about`
  - `tests/test_outbound_tidal_account.py::test_a_sweep_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_tidal_account.py::test_a_tie_broken_by_any_agreeing_is_said_and_no_other_match_is`
  - `tests/test_outbound_tidal_account.py::test_a_title_that_reads_two_ways_agrees_under_either_and_still_needs_one`
  - `tests/test_outbound_tidal_account.py::test_an_export_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_tidal_account.py::test_releases_spelled_alike_stay_unmatched_and_the_reason_counts_them`
  - `tests/test_outbound_tidal_account.py::test_the_album_chooses_only_among_releases_that_agree_with_the_row`
  - `tests/test_outbound_tidal_account.py::test_the_album_never_overrides_a_heart_or_breaks_a_tie_between_two`
  - `tests/test_outbound_tidal_account.py::test_two_hearted_releases_spelled_alike_are_still_no_match`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_and_an_album_naming_one_of_them_is_a_broken_tie`
  - `tests/test_outbound_tidal_account.py::test_without_any_agreeing_the_same_tie_still_refuses_in_the_words_the_mirror_reads`

Old text:

```
        if any_agreeing and not unreadable:
```

New text:

```
        if not unreadable:
```

### `r835-c.S2_sync_hands_the_ledger_to_the_sweep_again`

sync.cli._plan_playlists: the sweep is handed no label built playlists, so every year playlist is swept as intake

- File: `src/cratekit/sync/cli.py`
- Source: `r835-c.json`, row `S2_sync_hands_the_ledger_to_the_sweep_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`, `tests/test_intake_writers_native.py`, `tests/test_label_playlists.py`, `tests/test_sync_all.py`
- Collected: 315 against a baseline of 315
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_the_sync_pass_hands_the_sweep_every_year_playlist_a_build_recorded`

Old text:

```
    label_built = ledger.label_playlist_ids(cfg)
```

New text:

```
    label_built = frozenset()
```

### `r1115.S1_sync_land_stops_on_unsettled`

sync land _download: carry on over a download that did not settle, so a transient failure lands the rest

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1115.json`, row `S1_sync_land_stops_on_unsettled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_crate_sync_skill.py`
- Collected: 93 against a baseline of 93
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_parked_download_ends_the_pass_blocked_before_the_tail`
  - `tests/test_sync_land.py::test_a_transient_download_failure_ends_the_pass_and_lands_nothing`

Old text:

```
    if not read.settled:
        raise _Stop(DOWNLOAD, tail.job_error(report, job))
```

New text:

```
    if False:
        raise _Stop(DOWNLOAD, tail.job_error(report, job))
```

### `r1115.S2_sync_land_names_the_refused`

sync land _download: report no refused track

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1115.json`, row `S2_sync_land_names_the_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_crate_sync_skill.py`
- Collected: 93 against a baseline of 93
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land.py::test_every_download_refused_lands_nothing_on_a_failing_row`
  - `tests/test_sync_land.py::test_one_lossy_refusal_among_eight_downloads_lands_seven_and_reports_one`

Old text:

```
    refused = [dict(row) for row in read.refused]
```

New text:

```
    refused = []
```

### `r1056.N6_no_nothing_filed_warning`

label_mark: never say a batch filed none of the built years

- File: `src/cratekit/label/mark_cli.py`
- Source: `r1056.json`, row `N6_no_nothing_filed_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`, `tests/test_label_playlists.py`
- Collected: 89 against a baseline of 89
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_bridge_batch_of_another_label_says_it_filed_nothing_too`
  - `tests/test_label_mark_native.py::test_a_pass_whose_landings_filed_none_of_the_built_years_marks_nothing_and_says_so[a-year-never-built]`
  - `tests/test_label_mark_native.py::test_a_pass_whose_landings_filed_none_of_the_built_years_marks_nothing_and_says_so[another-label]`
  - `tests/test_label_mark_native.py::test_a_pass_whose_landings_filed_none_of_the_built_years_marks_nothing_and_says_so[no-label-filed]`

Old text:

```
    if not filed & {year.year for year in built}:
```

New text:

```
    if False:
```

### `r1056.N7_nothing_filed_against_any_year`

label_mark: warn only when the batch filed no year at all, not none of the built ones

- File: `src/cratekit/label/mark_cli.py`
- Source: `r1056.json`, row `N7_nothing_filed_against_any_year`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`, `tests/test_label_playlists.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_pass_whose_landings_filed_none_of_the_built_years_marks_nothing_and_says_so[a-year-never-built]`

Old text:

```
    if not filed & {year.year for year in built}:
```

New text:

```
    if not filed:
```

### `u243.L10_empties_never_said`

prune._step: a playlist the plan empties is never marked, so the screen does not say so

- File: `src/cratekit/modules/outbound/prune.py`
- Source: `u243.json`, row `L10_empties_never_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tombstoned.py`, `tests/test_prune.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tombstoned.py::test_a_year_playlist_the_prune_empties_is_named_and_kept`

Old text:

```
        empties=bool(take) and set(order) <= {one.remote_id for one in take},
```

New text:

```
        empties=False,
```

### `u243.L9_prune_ignores_tombstones`

prune.plan_label: a tombstoned track leaves only when a held or mismatched release says so

- File: `src/cratekit/modules/outbound/prune.py`
- Source: `u243.json`, row `L9_prune_ignores_tombstones`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tombstoned.py`, `tests/test_prune.py`
- Collected: 84 against a baseline of 84
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_tombstoned.py::test_a_removed_single_is_taken_off_though_its_release_is_suppressed`
  - `tests/test_label_tombstoned.py::test_a_removed_track_stays_off_after_a_full_build`
  - `tests/test_label_tombstoned.py::test_a_tombstone_matches_the_version_and_every_billed_artist`
  - `tests/test_label_tombstoned.py::test_a_tombstoned_track_on_a_year_playlist_is_pruned`
  - `tests/test_label_tombstoned.py::test_a_year_playlist_the_prune_empties_is_named_and_kept`
  - `tests/test_label_tombstoned.py::test_hearing_a_dated_playlist_never_puts_a_removed_track_back`

Old text:

```
            if one in taken_away
            or (one not in staying(year) and (one in on_held or one in on_other))
```

New text:

```
            if (one not in staying(year) and (one in on_held or one in on_other))
```

### `u184.A1_flag_ignored`

record_ack: never take the session road, so --as session falls to the gate and leaves a run waiting

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A1_flag_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`, `tests/test_crate_sync_skill.py`, `tests/test_rekordbox_visit_skill.py`
- Collected: 81 against a baseline of 81
- Kills: 10 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_a_valid_acknowledgment_a_person_minted_is_reported_over_old_backups`
  - `tests/test_session_ack_by_session.py::test_an_expired_acknowledgment_is_replaced_by_one_command`
  - `tests/test_session_ack_by_session.py::test_an_unreadable_acknowledgment_is_replaced_by_one_command`
  - `tests/test_session_ack_by_session.py::test_one_command_mints_as_the_session_when_both_ages_are_four_days`
  - `tests/test_session_ack_by_session.py::test_one_command_prints_the_expiry_a_person_reads`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[both-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[files-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_reports_a_valid_acknowledgment_and_does_not_mint_again`

Old text:

```
    if getattr(ctx.args, "as_actor", None) == session.SESSION_ACTOR:
```

New text:

```
    if False:
```

### `u184.A2_any_actor_accepted`

build_ack: drop the one value restriction, so --as names any actor and is parsed

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A2_any_actor_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`, `tests/test_crate_sync_skill.py`, `tests/test_rekordbox_visit_skill.py`
- Collected: 81 against a baseline of 81
- Kills: 3 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_the_flag_names_no_actor_but_the_session[Session]`
  - `tests/test_session_ack_by_session.py::test_the_flag_names_no_actor_but_the_session[a-person]`
  - `tests/test_session_ack_by_session.py::test_the_flag_names_no_actor_but_the_session[cli]`

Old text:

```
        choices=(session.SESSION_ACTOR,),
```

New text:

```
        choices=None,
```

### `u285.M1_seam_installs`

open_db: drop the install, so a handle reads with the binding's own conversion and a zero dated push fails its row west of UTC

- File: `src/cratekit/core/rb_writer.py`
- Source: `u285.json`, row `M1_seam_installs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_dates.py`, `tests/test_organize.py`, `tests/test_rebuild.py`, `tests/test_foreign_tree.py`
- Collected: 289 against a baseline of 289
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize.py::test_a_push_stamped_with_the_zero_date_reads_as_no_push_at_all_west_of_utc`
  - `tests/test_rb_dates.py::test_a_commit_leaves_the_pushed_nodes_xml_timestamps_and_still_syncs_its_own[EST5EDT,M3.2.0,M11.1.0]`
  - `tests/test_rb_dates.py::test_a_commit_leaves_the_pushed_nodes_xml_timestamps_and_still_syncs_its_own[JST-9]`
  - `tests/test_rb_dates.py::test_a_commit_leaves_the_pushed_nodes_xml_timestamps_and_still_syncs_its_own[UTC0]`
  - `tests/test_rb_dates.py::test_a_handle_reads_the_whole_tree_over_a_zero_dated_push_and_writes_nothing`
  - `tests/test_rb_dates.py::test_the_open_seam_installs_the_wrapper`

Old text:

```
    rb_dates.install()

```

New text:

```
    pass

```

### `u242.M6_record_v1_reads_a_taken_key`

mark record: drop the version 1 branch, so a record written before U242 is refused for having no taken list

- File: `src/cratekit/sync/mark_record.py`
- Source: `u242.json`, row `M6_record_v1_reads_a_taken_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_sync_unmark.py`
- Collected: 78 against a baseline of 78
- Kills: 1 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_a_version_one_record_reads_as_one_with_nothing_taken`

Old text:

```
        if version == 1:
            # BEFORE U242 NOTHING WAS TAKEN HERE. A version 1 record that
            # somehow carries the key is still read as it was written.
            return []
```

New text:

```
        if False:
            return []
```

### `u242.M26_release_stamps_no_mark`

sync unmark: a release leaves the pass's legacy mark unstamped, so the next migration or strip takes it again

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `u242.json`, row `M26_release_stamps_no_mark`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_sync_unmark.py`
- Collected: 78 against a baseline of 78
- Kills: 3 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_a_release_that_fails_part_way_names_what_was_let_go`
  - `tests/test_u242_taken.py::test_a_release_whose_title_was_retitled_since_stamps_the_pass_mark`
  - `tests/test_u242_taken.py::test_unmark_of_a_legacy_pass_after_the_strip_releases_and_stamps_it`

Old text:

```
            if identity in by_id and not by_id[identity].unmarked:
                record.record_unmarked(name, identity)
```

New text:

```
            if False:
                record.record_unmarked(name, identity)
```

### `u185.G1_commit_guard_called`

commit_guarded: drop the foreign folder guard from the commit

- File: `src/cratekit/core/rb_writer.py`
- Source: `u185.json`, row `G1_commit_guard_called`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`
- Collected: 277 against a baseline of 277
- Kills: 13 (killed)
- Killed:
  - `tests/test_foreign_tree.py::test_a_handle_with_no_reading_at_open_refuses_rather_than_assuming_nothing_is_there`
  - `tests/test_foreign_tree.py::test_a_membership_added_to_a_pushed_playlist_is_refused`
  - `tests/test_foreign_tree.py::test_a_playlist_made_inside_the_folder_is_refused`
  - `tests/test_foreign_tree.py::test_a_playlist_of_ones_own_moved_into_the_folder_is_refused`
  - `tests/test_foreign_tree.py::test_a_position_named_at_the_top_moves_the_folder_and_is_refused`
  - `tests/test_foreign_tree.py::test_a_push_that_lands_while_a_handle_is_open_refuses_that_handles_commit`
  - `tests/test_foreign_tree.py::test_a_pushed_membership_rewritten_to_another_owner_is_refused`
  - `tests/test_foreign_tree.py::test_a_pushed_playlist_moved_out_of_the_folder_is_refused`
  - `tests/test_foreign_tree.py::test_a_reading_that_failed_at_open_is_kept_as_unread_and_refuses`
  - `tests/test_foreign_tree.py::test_a_second_folder_of_the_name_at_the_top_is_refused`
  - `tests/test_foreign_tree.py::test_a_soft_delete_of_a_pushed_playlist_is_refused_even_where_the_commit_admits_removals`
  - `tests/test_foreign_tree.py::test_raw_sql_into_the_folder_is_seen_by_the_reading_again_from_sql`
  - `tests/test_foreign_tree.py::test_renaming_the_folder_is_refused_and_rolled_back`

Old text:

```
            assert_created_rows_are_gridless(db)
            assert_foreign_untouched(db)
```

New text:

```
            assert_created_rows_are_gridless(db)
```

### `u40-author-full.C3_resume_without_run`

Drop --run from the resume argv, so the job driver's child meets the explicit gate with nothing recorded and stalls for ever

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `u40-author-full.json`, row `C3_resume_without_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`
- Collected: 70 against a baseline of 70
- Kills: 3 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_the_resume_argv_carries_the_folder_the_job_and_the_gate_run`
  - `tests/test_queued_resume_contract.py::test_a_queued_gated_verb_emits_the_run_its_decision_was_recorded_against[tag.retag]`
  - `tests/test_queued_resume_contract.py::test_the_resume_the_job_driver_spawns_can_actually_proceed[tag.retag]`

Old text:

```
    resume = ["--run", str(gate_run)] if gate_run else []
```

New text:

```
    resume = []
```

### `u40-author-full.C4_resume_always_runs`

Emit --run even when no gate run is frozen, so a job from an older build hands its child an empty run identifier

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `u40-author-full.json`, row `C4_resume_always_runs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`
- Collected: 70 against a baseline of 70
- Kills: 1 (killed)
- Killed:
  - `tests/test_queued_resume_contract.py::test_a_payload_from_an_older_build_still_builds_a_valid_command_line[tag.retag]`

Old text:

```
    resume = ["--run", str(gate_run)] if gate_run else []
    return [*resume, "tag", "retag", folder, "--job", job.job_id]
```

New text:

```
    return ["--run", str(gate_run), "tag", "retag", folder, "--job", job.job_id]
```

### `u164.W1_apply_folder`

apply_native: move into the music folder's batch path whatever the plan chose

- File: `src/cratekit/intake/landing.py`
- Source: `u164.json`, row `W1_apply_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filed.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
- Kills: 32 (killed)
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
  - `tests/test_intake_land_native.py::test_a_key_reaching_the_row_is_refused_from_sql_before_the_commit`
  - `tests/test_intake_land_native.py::test_a_landing_given_a_pass_names_it_on_the_record_sync_mark_reads`
  - ... and 17 more, see the JSON sidecar

Old text:

```
    target = rows.folder if rows.folder is not None else target_dir(cfg, plan.batch)
```

New text:

```
    target = target_dir(cfg, plan.batch)
```

### `u164.T3_free_stored`

landing_target: ask the disk alone, not the collection's stored folders

- File: `src/cratekit/intake/shelve.py`
- Source: `u164.json`, row `T3_free_stored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filed.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_folder_the_collection_stores_rows_under_is_passed_over_with_nothing_on_disk`
  - `tests/test_intake_land_filed.py::test_a_name_landed_into_again_goes_back_to_its_folder_unless_the_folder_is_gone`

Old text:

```
        stored_dirs=_stored_dirs(recorded),
```

New text:

```
        stored_dirs=frozenset(),
```

### `u261.O1_catalogue_drops_the_app`

open_catalogue: build the catalogue without the held app client, so its ISRC lookups go to the account

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u261.json`, row `O1_catalogue_drops_the_app`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_catalogue_app.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 270 against a baseline of 270
- Kills: 3 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_open_account_and_open_catalogue_hand_the_app_client_on`
  - `tests/test_provider_session_hold.py::test_an_app_recorded_after_the_open_is_picked_up_by_the_next_resolve`
  - `tests/test_provider_session_hold.py::test_the_app_client_is_held_with_the_session_and_asks_one_token`

Old text:

```
        catalogue=held.app,
```

New text:

```
        catalogue=None,
```

### `u270.L2_row_only_for_a_recorded_track`

record_playlist_tracks: note a row for a track not recorded as added, claiming a person's track by its row

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u270.json`, row `L2_row_only_for_a_recorded_track`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_export_batches.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_workers.py`, `tests/test_prune.py`
- Collected: 259 against a baseline of 259
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_export_batches.py::test_the_ledger_never_notes_a_row_for_a_track_it_does_not_hold_as_added`

Old text:

```
            if str(track) in added:
                known[str(row)] = str(track)
```

New text:

```
            if True:
                known[str(row)] = str(track)
```

### `u114.M19_write_intent`

The apply opens the database without write intent, so a running rekordbox is not refused by the opener

- File: `src/cratekit/tagging/suggest_cli.py`
- Source: `u114.json`, row `M19_write_intent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_with_rekordbox_open_the_plan_is_read_and_no_file_is_written`

Old text:

```
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
```

New text:

```
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=False, cfg=cfg)
```

### `u114.M20_pick_declared`

A --set genre the taxonomy does not declare is accepted

- File: `src/cratekit/tagging/suggest_cli.py`
- Source: `u114.json`, row `M20_pick_declared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_a_pick_outside_the_taxonomy_is_refused_before_any_row_is_read`

Old text:

```
        if not suggest.suggestable(declared, genre):
```

New text:

```
        if not genre.strip():
```

### `u177.C3_flag_beside_label`

_label_flag: drop the refusal of --label-from-tags beside --label, so one label for every file silently wins

- File: `src/cratekit/intake/land_cli.py`
- Source: `u177.json`, row `C3_flag_beside_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_label_from_tags_beside_another_label_source_is_refused_before_the_gate[--label]`

Old text:

```
    if from_tags and given is not None:
        raise refuse(

```

New text:

```
    if False:
        raise refuse(

```

### `u177.C4_flag_ignored`

label_plan: ignore --label-from-tags, so the batch lands filed under nothing

- File: `src/cratekit/intake/land_cli.py`
- Source: `u177.json`, row `C4_flag_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 58 against a baseline of 58
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_batch_of_two_labels_and_an_unregistered_seller_files_each_under_its_own`
  - `tests/test_intake_land_labels_native.py::test_a_label_tag_spelled_decomposed_files_under_the_composed_folder`
  - `tests/test_intake_land_labels_native.py::test_a_labelled_file_with_no_year_is_named_with_its_label_and_filed_nowhere`
  - `tests/test_intake_land_labels_native.py::test_a_puls_batch_of_three_years_lands_as_three_year_playlists_under_its_label`
  - `tests/test_intake_land_labels_native.py::test_the_digest_moves_between_one_label_and_each_files_own`

Old text:

```
            if label_from_tags:
                return label_filing.plan_for_tags(db, medium, files=files)

```

New text:

```
            if False:
                return label_filing.plan_for_tags(db, medium, files=files)

```

### `u205.S3_catalogue_lookup_ignores_app`

label catalogue: tracks_for_isrc goes to the account session whatever the opener built, and intake missing with it

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u205.json`, row `S3_catalogue_lookup_ignores_app`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_intake_missing_isrc.py`
- Collected: 256 against a baseline of 256
- Kills: 15 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_a_404_on_the_isrc_collection_is_an_outage_and_never_no_track`
  - `tests/test_catalogue_app.py::test_a_failed_lookup_climbs_the_ladder_and_refuses_rather_than_reading_as_no_match[400]`
  - `tests/test_catalogue_app.py::test_a_failed_lookup_climbs_the_ladder_and_refuses_rather_than_reading_as_no_match[500]`
  - `tests/test_catalogue_app.py::test_a_failed_lookup_climbs_the_ladder_and_refuses_rather_than_reading_as_no_match[503]`
  - `tests/test_catalogue_app.py::test_a_failed_lookup_climbs_the_ladder_and_refuses_rather_than_reading_as_no_match[data-not-a-list]`
  - `tests/test_catalogue_app.py::test_a_failed_lookup_climbs_the_ladder_and_refuses_rather_than_reading_as_no_match[not-an-object]`
  - `tests/test_catalogue_app.py::test_a_failed_lookup_climbs_the_ladder_and_refuses_rather_than_reading_as_no_match[not-json]`
  - `tests/test_catalogue_app.py::test_a_rate_limit_on_the_app_trips_the_shared_gate_and_refuses_the_account_too`
  - `tests/test_catalogue_app.py::test_a_rejected_app_token_climbs_the_ladder_then_refuses_naming_the_app[401]`
  - `tests/test_catalogue_app.py::test_a_rejected_app_token_climbs_the_ladder_then_refuses_naming_the_app[403]`
  - `tests/test_catalogue_app.py::test_a_token_service_refusing_the_app_is_a_rejected_app_credential[400]`
  - `tests/test_catalogue_app.py::test_a_token_service_refusing_the_app_is_a_rejected_app_credential[401]`
  - `tests/test_catalogue_app.py::test_a_token_service_refusing_the_app_is_a_rejected_app_credential[403]`
  - `tests/test_catalogue_app.py::test_an_isrc_catalogue_lookup_goes_to_the_app_and_intake_missing_with_it`
  - `tests/test_catalogue_app.py::test_open_account_and_open_catalogue_hand_the_app_client_on`

Old text:

```
        self._lookups = catalogue if catalogue is not None else session
```

New text:

```
        self._lookups = session
```

### `u293.S4_label_go_holds`

label_sync: a label go takes no staging lock

- File: `src/cratekit/cli/label_sync.py`
- Source: `u293.json`, row `S4_label_go_holds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_night.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`
- Collected: 253 against a baseline of 253
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_night.py::test_a_label_go_holds_the_lock_and_a_walk_does_not`
  - `tests/test_sync_night.py::test_a_label_go_refuses_while_another_pass_holds_the_lock`

Old text:

```
    with staging_lock.held("crate label sync --go", run_id=ctx.run.run_id):
```

New text:

```
    if True:
```

### `u211.W3_strict_at_commit`

_binding_probe: answer zero at commit too when the scan cannot confirm, so the binding commits over an unreadable live process

- File: `src/cratekit/core/rb_writer.py`
- Source: `u211.json`, row `W3_strict_at_commit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_rb_writer_guard.py`
- Collected: 251 against a baseline of 251
- Kills: 2 (killed)
- Killed:
  - `tests/test_process_scan.py::test_the_binding_probe_is_put_back_after_a_refusal`
  - `tests/test_process_scan.py::test_the_binding_probe_refuses_a_live_unreadable_process_at_commit`

Old text:

```
            if strict:
                raise
            return 0
```

New text:

```
            if False:
                raise
            return 0
```

### `u164.T2_free_disk`

_free_target: never pass over a folder already on disk

- File: `src/cratekit/intake/shelve.py`
- Source: `u164.json`, row `T2_free_disk`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filed.py`, `tests/test_intake_shelve.py`
- Collected: 53 against a baseline of 53
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_folder_already_on_disk_is_passed_over_for_the_next_suffix`
  - `tests/test_intake_shelve.py::test_a_target_made_after_the_plan_is_stale_and_the_folder_stays`
  - `tests/test_intake_shelve.py::test_two_batches_filing_to_one_name_get_two_and_a_taken_target_is_passed_over`

Old text:

```
    while os.path.lexists(candidate) or candidate in planned or spell(candidate) in stored_dirs:
```

New text:

```
    while candidate in planned or spell(candidate) in stored_dirs:
```

### `u164.T5_empty_subject`

filed_parts: leave an empty subject empty instead of Downloads

- File: `src/cratekit/intake/shelve.py`
- Source: `u164.json`, row `T5_empty_subject`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filed.py`, `tests/test_intake_shelve.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_name_that_is_a_date_alone_files_as_downloads`

Old text:

```
    return when, words or batch_name.DOWNLOADS
```

New text:

```
    return when, words
```

### `u27-restore-cli-round-2.S3_analysis_watch_watches_nothing`

Arm the analysis watch on no roots, so it reports a clean session either way

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-round-2.json`, row `S3_analysis_watch_watches_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_the_session_watches_the_whole_library_and_not_a_folder_inside_it`

Old text:

```
        analysis_roots=watched,
```

New text:

```
        analysis_roots=(),
```

### `u169.N5_repair_scan_bypasses`

repair paths: read --root as the base did, bypassing the helper

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u169.json`, row `N5_repair_scan_bypasses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_root_option.py`, `tests/intake/test_repair_apply.py`
- Collected: 48 against a baseline of 48
- Kills: 2 (killed)
- Killed:
  - `tests/test_root_option.py::test_repair_paths_refuses_a_root_with_no_folder`
  - `tests/test_root_option.py::test_repair_paths_scans_a_relative_root_inside_the_library`

Old text:

```
    root = naming_cli.root_folder(ctx.args.root, cfg, verb="repair paths")
```

New text:

```
    root = Path(ctx.args.root) if ctx.args.root else Path(cfg.library.root)
```

### `u169.N6_repair_apply_bypasses`

repair paths --apply: take a relative root as it is

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u169.json`, row `N6_repair_apply_bypasses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_root_option.py`, `tests/intake/test_repair_apply.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_root_option.py::test_repair_apply_reads_a_relative_root_against_the_library_root`

Old text:

```
        naming_cli.root_path(ctx.args.root, cfg, verb="repair paths --apply")
```

New text:

```
        Path(ctx.args.root)
```

### `r1032.A10_reason_words_reworded`

_among: reword the tie reason away from the constant the mirror reads

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1032.json`, row `A10_reason_words_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_organize_mirror_tie.py`, `tests/test_outbound_workers.py`
- Collected: 241 against a baseline of 241
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize_mirror_tie.py::test_a_tie_beside_a_release_that_cannot_be_read_is_left_out_and_asked_again`
  - `tests/test_outbound_tidal_account.py::test_a_file_with_no_album_tag_stays_unmatched_and_says_the_tag_is_missing`
  - `tests/test_outbound_tidal_account.py::test_a_sweep_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_tidal_account.py::test_an_unreadable_release_beside_the_tie_still_refuses_with_any_agreeing`
  - `tests/test_outbound_tidal_account.py::test_releases_spelled_alike_stay_unmatched_and_the_reason_counts_them`
  - `tests/test_outbound_tidal_account.py::test_without_any_agreeing_the_same_tie_still_refuses_in_the_words_the_mirror_reads`

Old text:

```
            f"{named}{aside}, {len(agreeing)} {AGREEING_RELEASES} and the "
```

New text:

```
            f"{named}{aside}, {len(agreeing)} of them match this row's artist, title and version and the "
```

### `u246.S14_unmark_narrowed_empty`

unmark: an empty narrowed set, so --playlist narrows every mark away and the verb puts nothing back

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `u246.json`, row `S14_unmark_narrowed_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`, `tests/test_gate_shown_plan.py`
- Collected: 47 against a baseline of 47
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_playlist_given_twice_narrows_to_both_marks_named`
  - `tests/test_sync_unmark.py::test_playlist_narrows_to_the_marks_named`
  - `tests/test_sync_unmark.py::test_the_mark_screen_says_a_playlist_was_put_back`

Old text:

```
    narrowed = set(named)
```

New text:

```
    narrowed = set()
```

### `u246.S15_unmark_narrowed_first_only`

unmark: narrow to the first playlist named alone, so a second --playlist is dropped

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `u246.json`, row `S15_unmark_narrowed_first_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`, `tests/test_gate_shown_plan.py`
- Collected: 47 against a baseline of 47
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_playlist_given_twice_narrows_to_both_marks_named`

Old text:

```
    narrowed = set(named)
```

New text:

```
    narrowed = set(named[:1])
```

### `u113-c.C7_unproven_import_names`

The rotation reads an intake file's recorded names whether or not its import was proven

- File: `src/cratekit/intake/rotate.py`
- Source: `u113-c.json`, row `C7_unproven_import_names`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate_account_playlists.py`, `tests/test_inbox_rotate.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate_account_playlists.py::test_an_intake_file_nobody_imported_names_nothing`

Old text:

```
        if session.IMPORT_VERIFIED_KEY in record.detail:
```

New text:

```
        if True:
```

### `u113-c.C9_earliest_name_wins`

The earliest landing of a recorded name ages it, not the latest

- File: `src/cratekit/intake/rotate.py`
- Source: `u113-c.json`, row `C9_earliest_name_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate_account_playlists.py`, `tests/test_inbox_rotate.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate_account_playlists.py::test_the_latest_landing_of_a_name_is_the_one_it_is_aged_by`

Old text:

```
                if name not in by_name or landed >= by_name[name][0]:
```

New text:

```
                if name not in by_name or landed <= by_name[name][0]:
```

### `u110-c.C5_missing_hint`

intake missing --run prints --name RUN again

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u110-c.json`, row `C5_missing_hint`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_names.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 238 against a baseline of 238
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_the_default_human_output_names_the_list_the_download_and_the_landing`

Old text:

```
f"--pass {name}, adding
```

New text:

```
f"--name {name}, adding
```

### `r1255.F1_refill_plan_unlisted`

plan_refill: leave the plan's log_unlisted at its default, so the warning counts a record

- File: `src/cratekit/intake/refill.py`
- Source: `r1255.json`, row `F1_refill_plan_unlisted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_refill.py`
- Collected: 43 against a baseline of 43
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_session_log_that_cannot_be_listed_is_named_as_one_by_the_plan`

Old text:

```
        log_unlisted=session.log_unlisted(unreadable, cfg),
```

New text:

```
        log_unlisted=False,
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

### `r338-c.C6_only_the_first_root_is_watched`

is_watched: ask the library root alone, so a share aimed at the live share's own parent is pulled under the watch that refuses it

- File: `src/cratekit/core/analysis_store.py`
- Source: `r338-c.json`, row `C6_only_the_first_root_is_watched`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_store.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_a_share_that_would_land_under_the_analysis_watch_is_withheld_and_not_asked_about`

Old text:

```
    return any(_is_within(Path(path), root) for root in watch_roots(cfg))
```

New text:

```
    return _is_within(Path(path), watch_roots(cfg)[0])
```

### `u25.G15_barren_watch`

Watch Music, which holds no ANLZ file, instead of watch_roots

- File: `src/cratekit/write/metadata_cli.py`
- Source: `u25.json`, row `G15_barren_watch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_store.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_no_call_site_hand_lists_the_roots_an_analysis_watch_covers`

Old text:

```
            analysis_roots=analysis_store.watch_roots(cfg),

```

New text:

```
            analysis_roots=(Path(cfg.library.root) / "Music",),

```

### `u113-a.A8_pending_any_state`

Names held by intake files are read from records whatever their state, not only those awaiting import

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u113-a.json`, row `A8_pending_any_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_name_an_unimported_intake_file_holds_is_not_given_again`

Old text:

```
        and record.state is session.SessionState.AWAITING_IMPORT
```

New text:

```
        and record.state is not session.SessionState.AWAITING_IMPORT
```

### `u113-b.B6_root_names_unheld`

Names at the export's playlist root, where an import lands first, are not held

- File: `src/cratekit/intake/landing.py`
- Source: `u113-b.json`, row `B6_root_names_unheld`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_name_at_the_playlist_root_is_not_given_since_an_import_lands_there`

Old text:

```
    return (*held, *at_root)
```

New text:

```
    return held
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

### `u129-author.A12_archive_backfill_swallows_all`

Catch Exception around plan_archive so a credential refusal becomes a warning

- File: `src/cratekit/export/set_cli.py`
- Source: `u129-author.json`, row `A12_archive_backfill_swallows_all`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_u129_set_account_playlist.py::test_export_archive_backfill_refuses_a_credential_error`

Old text:

```
        except CratekitError as exc:
            # Soft skip per set, as a landing's _plan_set_archive does. A
            # CredentialError (not a CratekitError) still refuses the verb.
            warnings.append(
                {
                    "code": "export-archive-backfill-refused",
                    "message": f"{name}: {exc.cause.message}",
                }
            )
            continue

```

New text:

```
        except Exception as exc:
            warnings.append(
                {
                    "code": "export-archive-backfill-refused",
                    "message": f"{name}: {exc}",
                }
            )
            continue

```

