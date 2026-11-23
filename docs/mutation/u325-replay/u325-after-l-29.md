# Mutation table: u325-after-l-29

Measured by `scripts/mutate.py` on 2026-11-23 01:36 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 70.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:20 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 55, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard. 70 row(s) were reused from a prior sidecar and were measured by an earlier process, whose children this run did not watch.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u267.M8_close_closes_nothing` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 115 | 5 | killed |
| `u131.K6_adopt_not_made` | `src/cratekit/modules/outbound/ledger.py` | user | 2 file(s) | 114 | 1 | killed |
| `u131.K7_kind_folders_kept` | `src/cratekit/modules/outbound/ledger.py` | user | 2 file(s) | 114 | 5 | killed |
| `r879-a.C11_sole_exact_ignores_full` | `src/cratekit/intake/candidates.py` | user | 2 file(s) | 112 | 4 | killed |
| `r879-a.C1_full_reads_total_not_last_page` | `src/cratekit/intake/candidates.py` | user | 2 file(s) | 112 | 5 | killed |
| `a32.J3_bookkeeping_counted_as_moved` | `src/cratekit/write/row_defaults.py` | user | 2 file(s) | 112 | 6 | killed |
| `a32.A6_policy_left_behind` | `src/cratekit/core/rb_writer.py` | maintainer | 2 file(s) | 112 | 4 | killed |
| `r1103.H2_refusal_slug` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 331 | 4 | killed |
| `r1255.S9_gate_unlisted_detail` | `src/cratekit/core/session.py` | maintainer | 3 file(s) | 328 | 2 | killed |
| `u164.T6_reuse_recorded` | `src/cratekit/intake/shelve.py` | user | 3 file(s) | 105 | 5 | killed |
| `u164.R1_record_filed` | `src/cratekit/intake/native.py` | user | 3 file(s) | 105 | 7 | killed |
| `r290-author.S08_route_resort_call_removed` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 323 | 11 | killed |
| `r1056.S1_no_landing_step_names_intake_missing` | `src/cratekit/sync/mark_cli.py` | user | 2 file(s) | 102 | 4 | killed |
| `r1056.S2_unreachable_step_names_sync` | `src/cratekit/sync/mark_cli.py` | user | 2 file(s) | 102 | 1 | killed |
| `u132.G1_undeclared_cause` | `src/cratekit/write/genre_favorites.py` | user | 5 file(s) | 319 | 2 | killed |
| `u259.M1_judge_no_row` | `src/cratekit/intake/analyzed.py` | user | 2 file(s) | 98 | 6 | killed |
| `u259.M5_member_reads_nothing` | `src/cratekit/intake/analyzed.py` | user | 2 file(s) | 98 | 19 | killed |
| `r1032.A2_tie_always_broken` | `src/cratekit/modules/outbound/tidal_account.py` | user | 4 file(s) | 316 | 15 | killed |
| `r835-c.S2_sync_hands_the_ledger_to_the_sweep_again` | `src/cratekit/sync/cli.py` | user | 4 file(s) | 315 | 1 | killed |
| `u129-author.A4_archive_raise_fails_landing` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 97 | 2 | killed |
| `u129-author.A5_archive_return_discarded` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 97 | 2 | killed |
| `r1115.S1_sync_land_stops_on_unsettled` | `src/cratekit/cli/sync_land.py` | user | 2 file(s) | 93 | 2 | killed |
| `r1115.S2_sync_land_names_the_refused` | `src/cratekit/cli/sync_land.py` | user | 2 file(s) | 93 | 2 | killed |
| `r390-a.A2_retry_refuses_any_closed_job_with_a_cause` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 306 | 9 | killed |
| `r1255.N1_landings_of_pass_refuses` | `src/cratekit/intake/native.py` | user | 2 file(s) | 90 | 2 | killed |
| `r1255.N2_landed_passes_refuses` | `src/cratekit/intake/native.py` | user | 2 file(s) | 90 | 1 | killed |
| `r1056.N6_no_nothing_filed_warning` | `src/cratekit/label/mark_cli.py` | user | 2 file(s) | 89 | 4 | killed |
| `r1056.N7_nothing_filed_against_any_year` | `src/cratekit/label/mark_cli.py` | user | 2 file(s) | 89 | 1 | killed |
| `r375-c.W1_listener_left_on_the_handle` | `src/cratekit/core/rb_writer.py` | maintainer | 2 file(s) | 87 | 1 | killed |
| `r375-c.W2_witness_listens_one_event_early` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 87 | 2 | killed |
| `u243.L10_empties_never_said` | `src/cratekit/modules/outbound/prune.py` | user | 2 file(s) | 84 | 1 | killed |
| `u243.L9_prune_ignores_tombstones` | `src/cratekit/modules/outbound/prune.py` | user | 2 file(s) | 84 | 6 | killed |
| `r746-a.G3_content_row_admitted_without_asking` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 293 | 5 | killed |
| `u184.A1_flag_ignored` | `src/cratekit/session/cli.py` | user | 3 file(s) | 81 | 10 | killed |
| `u184.A2_any_actor_accepted` | `src/cratekit/session/cli.py` | user | 3 file(s) | 81 | 3 | killed |
| `u113-b.B4_steps_name_one` | `src/cratekit/intake/ingest.py` | user | 2 file(s) | 80 | 1 | killed |
| `u113-b.B7_digest_blind_to_split` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 80 | 2 | killed |
| `u285.M1_seam_installs` | `src/cratekit/core/rb_writer.py` | user | 4 file(s) | 289 | 6 | killed |
| `u185.G1_commit_guard_called` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 287 | 13 | killed |
| `u278.M17_spending_widens` | `src/cratekit/core/provider_gate.py` | user | 3 file(s) | 287 | 1 | killed |
| `u242.M6_record_v1_reads_a_taken_key` | `src/cratekit/sync/mark_record.py` | user | 2 file(s) | 78 | 1 | killed |
| `u242.M26_release_stamps_no_mark` | `src/cratekit/sync/unmark_cli.py` | user | 2 file(s) | 78 | 3 | killed |
| `r1677.R5_file_set_drops_playlist` | `src/cratekit/core/rb_writer.py` | user | 5 file(s) | 278 | 2 | killed |
| `r289-b.C2_fallback_resume_call_site` | `src/cratekit/acquire/fallback_cli.py` | user | 2 file(s) | 72 | 1 | killed |
| `r289-b.C3_fallback_queue_call_site` | `src/cratekit/acquire/fallback_cli.py` | user | 2 file(s) | 72 | 1 | killed |
| `u157.A2_cut_unbound` | `src/cratekit/analysis/cli.py` | user | 3 file(s) | 277 | 3 | killed |
| `u167.M23_waiting_exit` | `src/cratekit/analysis/check_cli.py` | user | 1 file(s) | 70 | 7 | killed |
| `u167.M24_suspect_exit` | `src/cratekit/analysis/check_cli.py` | user | 1 file(s) | 70 | 5 | killed |
| `u40-author-full.C3_resume_without_run` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 70 | 3 | killed |
| `u40-author-full.C4_resume_always_runs` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 70 | 1 | killed |
| `u223.M3_no_clear` | `src/cratekit/analysis/artifacts.py` | user | 2 file(s) | 274 | 3 | killed |
| `u164.W1_apply_folder` | `src/cratekit/intake/landing.py` | user | 2 file(s) | 69 | 32 | killed |
| `u164.T3_free_stored` | `src/cratekit/intake/shelve.py` | user | 2 file(s) | 69 | 2 | killed |
| `u261.O1_catalogue_drops_the_app` | `src/cratekit/label/tidal_catalogue.py` | user | 3 file(s) | 270 | 3 | killed |
| `r744.C1_equal_bounds_accepted` | `src/cratekit/core/config.py` | user | 1 file(s) | 65 | 1 | killed |
| `r744.C2_bool_accepted` | `src/cratekit/core/config.py` | user | 1 file(s) | 65 | 1 | killed |
| `r1295.M16_set_aside_one_word` | `src/cratekit/intake/cli.py` | user | 3 file(s) | 262 | 4 | killed |
| `u211.W3_strict_at_commit` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 261 | 2 | killed |
| `u246.S1_adapter_asked_empty` | `src/cratekit/acquire/adapter.py` | user | 4 file(s) | 260 | 70 | killed |
| `u270.L2_row_only_for_a_recorded_track` | `src/cratekit/modules/outbound/ledger.py` | user | 4 file(s) | 259 | 1 | killed |
| `u114.M19_write_intent` | `src/cratekit/tagging/suggest_cli.py` | user | 1 file(s) | 59 | 1 | killed |
| `u114.M20_pick_declared` | `src/cratekit/tagging/suggest_cli.py` | user | 1 file(s) | 59 | 1 | killed |
| `u177.C3_flag_beside_label` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 58 | 1 | killed |
| `u177.C4_flag_ignored` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 58 | 5 | killed |
| `u205.S3_catalogue_lookup_ignores_app` | `src/cratekit/label/tidal_catalogue.py` | user | 3 file(s) | 256 | 15 | killed |
| `u293.S4_label_go_holds` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 253 | 2 | killed |
| `u55-collection-reader.R11_scan_item_ids` | `src/cratekit/adopt/scan_cli.py` | user | 1 file(s) | 54 | 7 | killed |
| `u55-collection-reader.R9_scan_zero_item_refusal` | `src/cratekit/adopt/scan_cli.py` | user | 1 file(s) | 54 | 2 | killed |
| `u164.T2_free_disk` | `src/cratekit/intake/shelve.py` | user | 2 file(s) | 53 | 3 | killed |
| `u164.T5_empty_subject` | `src/cratekit/intake/shelve.py` | user | 2 file(s) | 53 | 1 | killed |
| `u113-a.A2_queue_order` | `src/cratekit/intake/account_playlists.py` | user | 2 file(s) | 22933 | 0 (promoted) | zero |
| `u113-a.A7_payload_drops_name` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 52 | 40 | killed |
| `u278.M9_continue_names_no_hour` | `src/cratekit/core/provider_gate.py` | user | 4 file(s) | 247 | 3 | killed |
| `u27-restore-cli-round-2.S3_analysis_watch_watches_nothing` | `src/cratekit/session/restore_cli.py` | user | 2 file(s) | 246 | 1 | killed |
| `u169.N5_repair_scan_bypasses` | `src/cratekit/intake/repair_cli.py` | user | 2 file(s) | 48 | 2 | killed |
| `u169.N6_repair_apply_bypasses` | `src/cratekit/intake/repair_cli.py` | user | 2 file(s) | 48 | 1 | killed |
| `r1032.A10_reason_words_reworded` | `src/cratekit/modules/outbound/tidal_account.py` | user | 3 file(s) | 241 | 6 | killed |
| `u246.S14_unmark_narrowed_empty` | `src/cratekit/sync/unmark_cli.py` | user | 2 file(s) | 47 | 3 | killed |
| `u246.S15_unmark_narrowed_first_only` | `src/cratekit/sync/unmark_cli.py` | user | 2 file(s) | 47 | 1 | killed |
| `u113-c.C7_unproven_import_names` | `src/cratekit/intake/rotate.py` | user | 2 file(s) | 46 | 1 | killed |
| `u113-c.C9_earliest_name_wins` | `src/cratekit/intake/rotate.py` | user | 2 file(s) | 46 | 1 | killed |
| `u110-c.C5_missing_hint` | `src/cratekit/intake/missing_cli.py` | user | 5 file(s) | 238 | 1 | killed |
| `r1255.F1_refill_plan_unlisted` | `src/cratekit/intake/refill.py` | user | 2 file(s) | 43 | 1 | killed |

## Zero rows and what they owe

- `u113-a.A2_queue_order` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

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

### `a32.A6_policy_left_behind`

The commit's policies are left registered after the body, in the shared context manager

- File: `src/cratekit/core/rb_writer.py`
- Source: `a32.json`, row `A6_policy_left_behind`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`, `tests/test_repair_rows.py`
- Collected: 112 against a baseline of 112
- Kills: 4 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_policy_registered_before_the_apply_survives_it`
  - `tests/test_repair_link.py::test_the_two_acts_write_each_triple_and_move_no_other_column`
  - `tests/test_repair_rows.py::test_a_policy_registered_before_the_apply_survives_it`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
    finally:
        reset_field_policies()
        for policy in was.values():
            register_field_policy(policy)
```

New text:

```
    finally:
        for policy in was.values():
            register_field_policy(policy)
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

### `r1255.S9_gate_unlisted_detail`

assert_no_unresolved_session: drop the unlisted flag from the refusal's detail

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S9_gate_unlisted_detail`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_restore.py`, `tests/test_write_session.py`
- Collected: 328 against a baseline of 328
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

### `u259.M1_judge_no_row`

analyzed.judge: drop the answer for a row the collection lacks, so None reaches the removal marker read

- File: `src/cratekit/intake/analyzed.py`
- Source: `u259.json`, row `M1_judge_no_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`, `tests/test_inbox_analyzed.py`
- Collected: 98 against a baseline of 98
- Kills: 6 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_row_whose_id_is_not_text_stays_out_of_every_row_as_it_did`
  - `tests/test_analyze_check.py::test_a_scope_past_one_chunk_is_read_a_statement_a_500_and_answers_as_the_per_row_reads`
  - `tests/test_analyze_check.py::test_read_row_handed_no_row_reads_it_and_answers_as_handed_one`
  - `tests/test_analyze_check.py::test_the_mixed_library_reads_as_the_per_row_reads_read_it_for_a_named_landing`
  - `tests/test_analyze_check.py::test_the_mixed_library_reads_as_the_per_row_reads_read_it_in_inbox_analyze`
  - `tests/test_inbox_analyzed.py::test_a_membership_whose_collection_row_is_missing_stays_and_is_named`

Old text:

```
    if row is None:
        return Member(content_id=content_id, title="", action=WAIT, why=NO_ROW)
```

New text:

```
    if False:
        return Member(content_id=content_id, title="", action=WAIT, why=NO_ROW)
```

### `u259.M5_member_reads_nothing`

analyzed.member: judge no row instead of the row read by ID, so the clear reads every member as missing

- File: `src/cratekit/intake/analyzed.py`
- Source: `u259.json`, row `M5_member_reads_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`, `tests/test_inbox_analyzed.py`
- Collected: 98 against a baseline of 98
- Kills: 19 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_collection_whose_ids_are_stored_as_integers_reads_as_it_did[analyze]`
  - `tests/test_analyze_check.py::test_a_collection_whose_ids_are_stored_as_integers_reads_as_it_did[unanalysed]`
  - `tests/test_analyze_check.py::test_a_row_the_binding_cannot_load_after_one_that_refuses_still_refuses_as_it_did`
  - `tests/test_analyze_check.py::test_a_row_whose_id_is_not_text_stays_out_of_every_row_as_it_did`
  - `tests/test_analyze_check.py::test_a_row_whose_removal_marker_cannot_be_read_refuses_as_it_did[analyze]`
  - `tests/test_analyze_check.py::test_a_row_whose_removal_marker_cannot_be_read_refuses_as_it_did[unanalysed]`
  - `tests/test_analyze_check.py::test_a_scope_past_one_chunk_is_read_a_statement_a_500_and_answers_as_the_per_row_reads`
  - `tests/test_analyze_check.py::test_the_mixed_library_reads_as_the_per_row_reads_read_it_for_a_named_landing`
  - `tests/test_analyze_check.py::test_the_mixed_library_reads_as_the_per_row_reads_read_it_in_inbox_analyze`
  - `tests/test_analyze_check.py::test_the_mixed_library_reads_as_the_per_row_reads_read_it_over_every_row`
  - `tests/test_inbox_analyzed.py::test_a_membership_whose_collection_row_is_missing_stays_and_is_named`
  - `tests/test_inbox_analyzed.py::test_a_removal_that_did_not_take_is_refused_after_the_commit`
  - `tests/test_inbox_analyzed.py::test_a_row_marked_analysed_with_no_analysis_path_stays`
  - `tests/test_inbox_analyzed.py::test_a_row_removed_from_the_collection_stays_and_is_named`
  - `tests/test_inbox_analyzed.py::test_a_second_clear_plans_nothing`
  - ... and 4 more, see the JSON sidecar

Old text:

```
    return judge(content_id, db.get_content(ID=content_id))
```

New text:

```
    return judge(content_id, None)
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

### `u129-author.A4_archive_raise_fails_landing`

Let an account archive raise escape the landing write after rows are in the library

- File: `src/cratekit/intake/land_cli.py`
- Source: `u129-author.json`, row `A4_archive_raise_fails_landing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 97 against a baseline of 97
- Kills: 2 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archive_failure_is_a_warning_on_the_envelope`
  - `tests/test_u129_set_account_playlist.py::test_landing_archive_failure_after_write_is_a_warning`

Old text:

```
    try:
        _data, warnings, _wrote = set_cli.apply_archive(cfg, archived)
    except Exception as exc:
        message = (
            exc.cause.message if isinstance(exc, CratekitError) else f"{type(exc).__name__}: {exc}"
        )
        return [
            {
                "code": LAND_ARCHIVE_FAILED,
                "message": (
                    f"the account archive could not finish after the landing wrote "
                    f"({message}); the batch is in the library, run crate export "
                    f"archive over the set once the account can be reached"
                ),
            }
        ]
    return list(warnings)

```

New text:

```
    _data, warnings, _wrote = set_cli.apply_archive(cfg, archived)
    return list(warnings)

```

### `u129-author.A5_archive_return_discarded`

Discard apply_archive warnings so a not-renamed return is silent on the landed envelope

- File: `src/cratekit/intake/land_cli.py`
- Source: `u129-author.json`, row `A5_archive_return_discarded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 97 against a baseline of 97
- Kills: 2 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archive_not_renamed_is_a_warning_on_the_envelope`
  - `tests/test_u129_set_account_playlist.py::test_landing_archive_surfaces_changed_since_plan_as_a_warning`

Old text:

```
    try:
        _data, warnings, _wrote = set_cli.apply_archive(cfg, archived)
    except Exception as exc:

```

New text:

```
    try:
        _data, warnings, _wrote = set_cli.apply_archive(cfg, archived)
        warnings = []
    except Exception as exc:

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

### `r390-a.A2_retry_refuses_any_closed_job_with_a_cause`

the flag is not read: a cancelled job and a retryable failure are refused too

- File: `src/cratekit/core/jobs.py`
- Source: `r390-a.json`, row `A2_retry_refuses_any_closed_job_with_a_cause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_backup_cli.py`, `tests/test_outbound_workers.py`
- Collected: 306 against a baseline of 306
- Kills: 9 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`
  - `tests/test_jobs.py::test_a_cancelled_job_can_be_resumed_and_a_succeeded_one_cannot`
  - `tests/test_jobs.py::test_a_retry_re_arms_the_failure_and_leaves_the_declined_item_settled`
  - `tests/test_outbound_workers.py::test_a_failed_favourite_leaves_the_sweep_resumable`
  - `tests/test_outbound_workers.py::test_a_failed_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/test_outbound_workers.py::test_a_refused_request_fails_every_item_it_carried_and_the_resume_adds_each_once`
  - `tests/test_outbound_workers.py::test_a_resumed_export_counts_across_both_runs_and_each_item_once`

Old text:

```
    if current.cause is not None and not current.cause.retryable:
        raise refuse(
            "job-not-retryable",
```

New text:

```
    if current.cause is not None:
        raise refuse(
            "job-not-retryable",
```

### `r1255.N1_landings_of_pass_refuses`

native.landings_of_pass: drop the unread half again, so sync mark says a recorded landing never committed

- File: `src/cratekit/intake/native.py`
- Source: `r1255.json`, row `N1_landings_of_pass_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_sync_mark.py`
- Collected: 90 against a baseline of 90
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_the_native_landing_lookups_refuse_a_log_they_cannot_list`
  - `tests/test_sync_mark.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_landing`

Old text:

```
    land the pass again.
    """
    records = session.records(cfg)
```

New text:

```
    land the pass again.
    """
    records = session.scan_log(cfg)[0]
```

### `r1255.N2_landed_passes_refuses`

native.landed_passes: drop the unread half again, so organize plans no native pass over a log it could not list

- File: `src/cratekit/intake/native.py`
- Source: `r1255.json`, row `N2_landed_passes_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_sync_mark.py`
- Collected: 90 against a baseline of 90
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_the_native_landing_lookups_refuse_a_log_they_cannot_list`

Old text:

```
    cannot list refuses rather than reading as no landing (R-1255).
    """
    records = session.records(cfg)
```

New text:

```
    cannot list refuses rather than reading as no landing (R-1255).
    """
    records = session.scan_log(cfg)[0]
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

### `r375-c.W1_listener_left_on_the_handle`

commit_witness: never remove the listener, so a handle that outlives the write keeps marking a witness nobody reads

- File: `src/cratekit/core/rb_writer.py`
- Source: `r375-c.json`, row `W1_listener_left_on_the_handle`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_the_commit_witness_leaves_the_handle_as_it_found_it`

Old text:

```
        event.remove(target, "after_commit", witness._mark)
```

New text:

```
        pass
```

### `r375-c.W2_witness_listens_one_event_early`

commit_witness: listen for before_commit, so a transaction refused on its way in is witnessed as landed

- File: `src/cratekit/core/rb_writer.py`
- Source: `r375-c.json`, row `W2_witness_listens_one_event_early`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`
- Collected: 87 against a baseline of 87
- Kills: 2 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_the_commit_witness_does_not_read_a_commit_that_never_landed_as_landed`
  - `tests/test_tree_writer.py::test_the_commit_witness_leaves_the_handle_as_it_found_it`

Old text:

```
    event.listen(target, "after_commit", witness._mark)
    try:
        yield witness
    finally:
        event.remove(target, "after_commit", witness._mark)
```

New text:

```
    event.listen(target, "before_commit", witness._mark)
    try:
        yield witness
    finally:
        event.remove(target, "before_commit", witness._mark)
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

### `r746-a.G3_content_row_admitted_without_asking`

guard_violations: every commit admits a content row, whether or not it named the table

- File: `src/cratekit/core/rb_writer.py`
- Source: `r746-a.json`, row `G3_content_row_admitted_without_asking`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_write_guard_completeness.py`, `tests/test_intake_land_native.py`
- Collected: 293 against a baseline of 293
- Kills: 5 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_commit_that_asks_may_create_a_content_row_carrying_what_the_file_says`
  - `tests/test_rb_writer_guard.py::test_an_admitted_delete_admits_no_soft_delete_no_creation_and_no_modification`
  - `tests/test_rb_writer_guard.py::test_creating_a_track_row_is_forbidden`
  - `tests/test_rb_writer_guard.py::test_mixed_session_reports_every_violation`
  - `tests/test_write_guard_completeness.py::test_a_content_creation_flushed_away_is_still_refused`

Old text:

```
        if table == CONTENT_TABLE and table in creatable:
```

New text:

```
        if table == CONTENT_TABLE:
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

### `u113-b.B4_steps_name_one`

The import steps name only the first playlist when the file holds several

- File: `src/cratekit/intake/ingest.py`
- Source: `u113-b.json`, row `B4_steps_name_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land.py`
- Collected: 80 against a baseline of 80
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`

Old text:

```
    if len(playlists) > 1:
```

New text:

```
    if len(playlists) > 99:
```

### `u113-b.B7_digest_blind_to_split`

The xml gate's digest does not cover the split, so an answer given for one carries out another

- File: `src/cratekit/intake/land_cli.py`
- Source: `u113-b.json`, row `B7_digest_blind_to_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land.py`
- Collected: 80 against a baseline of 80
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_an_answer_given_for_one_split_is_stale_for_another`
  - `tests/test_intake_land_account_playlists.py::test_an_export_rewritten_after_the_gate_moves_nothing`

Old text:

```
        identity["playlists"] = [claimed.identity() for claimed in split]
```

New text:

```
        pass
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

### `u185.G1_commit_guard_called`

commit_guarded: drop the foreign folder guard from the commit

- File: `src/cratekit/core/rb_writer.py`
- Source: `u185.json`, row `G1_commit_guard_called`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`
- Collected: 287 against a baseline of 287
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

### `u278.M17_spending_widens`

spending: widen to the reserve whatever the verb declared

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M17_spending_widens`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_label_sync_go.py`
- Collected: 287 against a baseline of 287
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_spending_never_reaches_past_the_class_the_verb_declared`

Old text:

```
    scope.reserve = scope.declared

```

New text:

```
    scope.reserve = True

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

### `r1677.R5_file_set_drops_playlist`

_copy_file_set: copy the companions but not the playlist file, so the measured list and the copied list drift

- File: `src/cratekit/core/rb_writer.py`
- Source: `r1677.json`, row `R5_file_set_drops_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot_wal_r1665.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`
- Collected: 278 against a baseline of 278
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_snapshot.py::test_the_legacy_playlist_file_travels_with_the_database`
  - `tests/test_snapshot_check_room_r1677.py::test_the_file_set_measured_is_the_one_the_check_copies`

Old text:

```
    for companion in companions:
        if companion.exists():
```

New text:

```
    for companion in companions[:-1]:
        if companion.exists():
```

### `r289-b.C2_fallback_resume_call_site`

Drop the sweep on the fallback fetch resume path

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `r289-b.json`, row `C2_fallback_resume_call_site`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_this_verb_sweeps_the_staging_tree_it_shares_with_the_download_verb`

Old text:

```
            acquire_cli.sweep_staging(
                Path(jobs.frozen_config(job).paths.download_staging), store
            )

```

New text:

```
(empty)
```

### `r289-b.C3_fallback_queue_call_site`

Drop the sweep on the fallback fetch queue path

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `r289-b.json`, row `C3_fallback_queue_call_site`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_this_verb_sweeps_the_staging_tree_it_shares_with_the_download_verb`

Old text:

```
        acquire_cli.sweep_staging(Path(cfg.paths.download_staging), store)

```

New text:

```
(empty)
```

### `u157.A2_cut_unbound`

_bind_defaults: bind no drift cut, so the detector reads the shipped default

- File: `src/cratekit/analysis/cli.py`
- Source: `u157.json`, row `A2_cut_unbound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_drift.py`, `tests/test_analysis_workers.py`, `tests/test_head_agreement.py`
- Collected: 277 against a baseline of 277
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_worker_process_with_nothing_bound_binds_the_shipped_defaults`
  - `tests/test_analysis_workers.py::test_the_default_detector_is_rebound_with_a_fresh_calibration_per_item`
  - `tests/test_drift.py::test_a_whole_number_cut_loads_and_reaches_the_detector_binding`

Old text:

```
            drift_cut=cfg.analysis.drift_cut,

```

New text:

```
(empty)
```

### `u167.M23_waiting_exit`

analyze_check: waiting ends ok with exit 0 rather than pending

- File: `src/cratekit/analysis/check_cli.py`
- Source: `u167.json`, row `M23_waiting_exit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 70 against a baseline of 70
- Kills: 7 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_landing_s_session_names_its_rows`
  - `tests/test_analyze_check.py::test_a_scope_past_one_chunk_is_read_a_statement_a_500_and_answers_as_the_per_row_reads`
  - `tests/test_analyze_check.py::test_an_empty_analyze_playlist_falls_to_every_row_not_analysed`
  - `tests/test_analyze_check.py::test_an_intake_tree_not_cut_over_falls_to_every_row_not_analysed_and_says_why`
  - `tests/test_analyze_check.py::test_rows_landed_and_not_yet_analysed_are_waiting_on_a_pending_action`
  - `tests/test_analyze_check.py::test_the_check_reads_the_collection_in_statements_that_do_not_grow_with_it[analyze]`
  - `tests/test_analyze_check.py::test_the_check_reads_the_collection_in_statements_that_do_not_grow_with_it[unanalysed]`

Old text:

```
    if verdict == rc.WAITING:
```

New text:

```
    if False:
```

### `u167.M24_suspect_exit`

analyze_check: suspect ends ok with exit 0 rather than refusing

- File: `src/cratekit/analysis/check_cli.py`
- Source: `u167.json`, row `M24_suspect_exit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 70 against a baseline of 70
- Kills: 5 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_removed_dyn_mark_does_not_excuse_a_variable_grid`
  - `tests/test_analyze_check.py::test_a_variable_grid_on_a_row_not_marked_dyn_is_suspect_and_exits_27`
  - `tests/test_analyze_check.py::test_an_analysed_row_whose_file_is_missing_is_suspect`
  - `tests/test_analyze_check.py::test_no_file_under_the_library_is_opened_for_writing`
  - `tests/test_analyze_check.py::test_suspect_outranks_waiting_through_the_verb`

Old text:

```
    if verdict == rc.SUSPECT:
```

New text:

```
    if False:
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

### `u223.M3_no_clear`

staged_path: clear nothing, so a stale report and scratch leak into the next attempt

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M3_no_clear`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_tag_workers.py`
- Collected: 274 against a baseline of 274
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_directory_at_the_report_name_is_cleared_and_the_attempt_finishes`
  - `tests/test_analysis_workers.py::test_a_linked_intent_is_cleared_rather_than_kept_and_followed`
  - `tests/test_analysis_workers.py::test_a_new_attempt_clears_a_stale_report_and_keeps_only_the_intent`

Old text:

```
            if entry.is_dir() and not entry.is_symlink():
                shutil.rmtree(entry)
            else:
                entry.unlink()
```

New text:

```
            continue
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

### `r744.C1_equal_bounds_accepted`

a floor equal to the ceiling is accepted, an empty window the estimator answers None for on every track

- File: `src/cratekit/core/config.py`
- Source: `r744.json`, row `C1_equal_bounds_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_head_agreement.py`
- Collected: 65 against a baseline of 65
- Kills: 1 (killed)
- Killed:
  - `tests/test_head_agreement.py::test_an_empty_or_ill_typed_window_is_refused_at_load[analysis0-must be below]`

Old text:

```
    if isinstance(floor, int) and isinstance(ceiling, int) and floor >= ceiling:
```

New text:

```
    if isinstance(floor, int) and isinstance(ceiling, int) and floor > ceiling:
```

### `r744.C2_bool_accepted`

a boolean is accepted as a bound, since bool is an int to isinstance

- File: `src/cratekit/core/config.py`
- Source: `r744.json`, row `C2_bool_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_head_agreement.py`
- Collected: 65 against a baseline of 65
- Kills: 1 (killed)
- Killed:
  - `tests/test_head_agreement.py::test_an_empty_or_ill_typed_window_is_refused_at_load[analysis5-tempo_floor must be a whole number]`

Old text:

```
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
```

New text:

```
        if not isinstance(value, int) or value < 1:
```

### `r1295.M16_set_aside_one_word`

set_aside: always names the title as the absent half, so an artistless track is misnamed

- File: `src/cratekit/intake/cli.py`
- Source: `r1295.json`, row `M16_set_aside_one_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`, `tests/intake/test_workers.py`, `tests/test_sync_all.py`
- Collected: 262 against a baseline of 262
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_the_readable_listing_sets_aside_a_refused_row_by_id_in_its_place`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_artist_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_sync_all.py::test_a_playlist_whose_every_track_is_unread_is_unreadable_not_empty`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled1-artist]`

Old text:

```
why=f"the account lists it with no {_absent(title)}"
```

New text:

```
why="the account lists it with no title"
```

### `u211.W3_strict_at_commit`

_binding_probe: answer zero at commit too when the scan cannot confirm, so the binding commits over an unreadable live process

- File: `src/cratekit/core/rb_writer.py`
- Source: `u211.json`, row `W3_strict_at_commit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_rb_writer_guard.py`
- Collected: 261 against a baseline of 261
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

### `u246.S1_adapter_asked_empty`

InvocationResult: an empty set of requested keys, so every result reads as a track nobody asked for

- File: `src/cratekit/acquire/adapter.py`
- Source: `u246.json`, row `S1_adapter_asked_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`, `tests/intake/test_pipeline.py`
- Collected: 260 against a baseline of 260
- Kills: 70 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_deleted_frozen_list_named_relative_from_where_it_was_queued_still_drives`
  - `tests/test_acquire_workers.py::test_a_download_job_runs_pending_to_done_through_the_resume_path`
  - `tests/test_acquire_workers.py::test_a_lossless_landing_under_the_permissive_policy_is_not_marked`
  - `tests/test_acquire_workers.py::test_a_lossy_landing_under_strict_policy_is_refused_at_the_item_with_the_codec_named`
  - `tests/test_acquire_workers.py::test_a_lossy_landing_under_the_permissive_policy_is_committed_marked`
  - `tests/test_acquire_workers.py::test_a_lossy_offer_under_strict_policy_is_refused_before_anything_is_fetched`
  - `tests/test_acquire_workers.py::test_a_lying_offer_under_the_permissive_policy_is_still_committed_marked`
  - `tests/test_acquire_workers.py::test_a_mid_batch_defect_fails_that_item_and_the_resume_the_job_refuses_fetches_nothing`
  - `tests/test_acquire_workers.py::test_a_partial_file_left_in_staging_does_not_poison_the_next_attempt`
  - `tests/test_acquire_workers.py::test_a_provider_block_parks_the_job_and_makes_no_further_request`
  - `tests/test_acquire_workers.py::test_a_rate_limit_is_retried_under_backoff_and_then_lands`
  - `tests/test_acquire_workers.py::test_a_rate_limit_that_never_clears_fails_the_item_as_transient`
  - `tests/test_acquire_workers.py::test_a_refusal_beside_a_network_failure_fails_and_keeps_the_refusal_skipped`
  - `tests/test_acquire_workers.py::test_a_track_the_provider_does_not_have_is_permanent_and_carries_no_remedy`
  - `tests/test_acquire_workers.py::test_a_track_the_provider_no_longer_has_is_declined_as_well`
  - ... and 55 more, see the JSON sidecar

Old text:

```
            asked = set(self.requested)
```

New text:

```
            asked = set()
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

### `u55-collection-reader.R11_scan_item_ids`

The scan enqueues with no items at all, which is the R-203 shape

- File: `src/cratekit/adopt/scan_cli.py`
- Source: `u55-collection-reader.json`, row `R11_scan_item_ids`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`
- Collected: 54 against a baseline of 54
- Kills: 7 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_copy_edited_during_a_scan_judges_every_row_after_the_edit`
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item`
  - `tests/test_adopt_workers.py::test_a_row_tombstoned_between_queueing_and_driving_fails_its_own_item`
  - `tests/test_adopt_workers.py::test_a_scan_parses_the_active_taxonomy_once_however_many_rows_it_drives`
  - `tests/test_adopt_workers.py::test_a_scan_queues_one_item_per_live_row_and_drives_them_all`
  - `tests/test_adopt_workers.py::test_the_configuration_reaching_the_scan_worker_is_the_frozen_one`
  - `tests/test_adopt_workers.py::test_the_reported_counts_come_from_the_artifacts_and_not_from_the_queue`

Old text:

```
            item_ids=live,
```

New text:

```
            item_ids=(),
```

### `u55-collection-reader.R9_scan_zero_item_refusal`

The scan queues a job over an empty library, which drives to SUCCEEDED having read nothing

- File: `src/cratekit/adopt/scan_cli.py`
- Source: `u55-collection-reader.json`, row `R9_scan_zero_item_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`
- Collected: 54 against a baseline of 54
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_library_of_tombstones_is_a_different_zero_from_an_empty_one`
  - `tests/test_adopt_workers.py::test_an_empty_library_queues_nothing_and_says_so`

Old text:

```
    if not live:
```

New text:

```
    if False:
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

### `u113-a.A2_queue_order`

The account playlists are taken newest job first, the order the store lists them

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u113-a.json`, row `A2_queue_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`
- Collected: 22933 against a baseline of 22933
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

### `u113-a.A7_payload_drops_name`

queue_playlist is handed the name and records nothing

- File: `src/cratekit/intake/cli.py`
- Source: `u113-a.json`, row `A7_payload_drops_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`
- Collected: 52 against a baseline of 52
- Kills: 40 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_bridge_landing_is_what_a_rerun_of_its_pass_reads_as_mirrored`
  - `tests/test_intake_land_account_playlists.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists.py::test_a_name_an_unimported_intake_file_holds_is_not_given_again`
  - `tests/test_intake_land_account_playlists.py::test_a_name_at_the_playlist_root_is_not_given_since_an_import_lands_there`
  - `tests/test_intake_land_account_playlists.py::test_a_name_the_export_came_to_hold_after_the_gate_is_refused_and_moves_nothing`
  - `tests/test_intake_land_account_playlists.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists.py::test_a_row_that_only_resembles_a_file_does_not_claim_it`
  - `tests/test_intake_land_account_playlists.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists.py::test_a_track_both_playlists_brought_in_is_a_member_of_both`
  - `tests/test_intake_land_account_playlists.py::test_a_track_neither_owned_nor_brought_is_named_in_the_warnings`
  - `tests/test_intake_land_account_playlists.py::test_an_abandoned_landing_is_not_read_as_mirrored`
  - `tests/test_intake_land_account_playlists.py::test_an_account_playlist_whose_dated_name_is_the_batchs_takes_two`
  - `tests/test_intake_land_account_playlists.py::test_an_answer_given_for_one_split_is_stale_for_another`
  - `tests/test_intake_land_account_playlists.py::test_an_export_entry_on_another_machine_is_no_owned_row`
  - `tests/test_intake_land_account_playlists.py::test_an_export_rewritten_after_the_gate_moves_nothing`
  - ... and 25 more, see the JSON sidecar

Old text:

```
    if name:
        payload[PLAYLIST_NAME] = name
```

New text:

```
    if name and False:
        payload[PLAYLIST_NAME] = name
```

### `u278.M9_continue_names_no_hour`

hour_to_name: never name the hour, so a continue above the budget is refused as printed

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M9_continue_names_no_hour`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_sync_pair_resume.py`, `tests/test_label_playlists.py`
- Collected: 247 against a baseline of 247
- Kills: 3 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_parked_jobs_continue_carries_the_hour_its_ceiling_needs`
  - `tests/test_sync_pair_resume.py::test_a_ceiling_continue_above_the_hour_names_the_hour_and_finishes_the_run`
  - `tests/test_sync_pair_resume.py::test_a_gate_forecast_above_the_hour_names_the_hour_and_its_command_runs`

Old text:

```
    return wanted if wanted > settings.calls_per_hour else None
```

New text:

```
    return None
```

### `u27-restore-cli-round-2.S3_analysis_watch_watches_nothing`

Arm the analysis watch on no roots, so it reports a clean session either way

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-round-2.json`, row `S3_analysis_watch_watches_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 246 against a baseline of 246
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

