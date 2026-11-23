# Mutation table: u325-after-l-27

Measured by `scripts/mutate.py` on 2026-11-22 22:23 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 118.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:22 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 38, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u192.T1_typed_label_on_queue` | `src/cratekit/tagging/cli.py` | user | 2 file(s) | 166 | 1 | killed |
| `u192.T2_queue_warnings_lost` | `src/cratekit/tagging/cli.py` | user | 2 file(s) | 166 | 1 | killed |
| `u192.T3_resume_label_unsaid` | `src/cratekit/tagging/cli.py` | user | 2 file(s) | 166 | 2 | killed |
| `u246.S5_inspiration_held_empty` | `src/cratekit/organize/inspiration.py` | user | 4 file(s) | 333 | 9 | killed |
| `u246.S6_inspiration_planned_live` | `src/cratekit/organize/inspiration.py` | user | 4 file(s) | 333 | 1 | killed |
| `r501-d.R2_settled_is_not_imported` | `src/cratekit/write/routing_cli.py` | user | 3 file(s) | 329 | 1 | killed |
| `r501-d.R3_pass_is_proof` | `src/cratekit/write/routing_cli.py` | user | 3 file(s) | 329 | 1 | killed |
| `u246.S3_set_playlist_order_set_empty` | `src/cratekit/intake/set_playlist.py` | user | 5 file(s) | 323 | 29 | killed |
| `u246.S4_set_playlist_order_set_read_back` | `src/cratekit/intake/set_playlist.py` | user | 5 file(s) | 323 | 1 | killed |
| `u221.R12_hold_not_written` | `src/cratekit/modules/outbound/pairs.py` | user | 3 file(s) | 153 | 18 | killed |
| `u221.R13_hold_not_read` | `src/cratekit/modules/outbound/pairs.py` | user | 3 file(s) | 153 | 18 | killed |
| `u221.R14_hold_unvalidated` | `src/cratekit/modules/outbound/pairs.py` | maintainer | 3 file(s) | 153 | 4 | killed |
| `u27-adopt-apply-author.A1_approval_actor_is_the_process` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 642 | 1 | killed |
| `r1255.S6_records_refuses_unlisted` | `src/cratekit/core/session.py` | user | 4 file(s) | 634 | 5 | killed |
| `r770-a.A4_refusal_asks_for_a_defect_report` | `src/cratekit/intake/ingest.py` | user | 1 file(s) | 47 | 4 | killed |
| `r770-a.A5_tree_built_without_the_refusal` | `src/cratekit/intake/ingest.py` | user | 1 file(s) | 47 | 3 | killed |
| `r770-a.A6_splice_asks_only_after_the_export` | `src/cratekit/intake/ingest.py` | user | 1 file(s) | 47 | 1 | killed |
| `r1634.M11_reread_reads_the_line` | `src/cratekit/label/tidal_catalogue.py` | user | 3 file(s) | 293 | 15 | killed |
| `r1634.M12_gone_confirms` | `src/cratekit/label/tidal_catalogue.py` | user | 3 file(s) | 293 | 6 | killed |
| `r1313.C1_catalogue_failure_alone` | `src/cratekit/label/tidal_catalogue.py` | user | 3 file(s) | 290 | 5 | killed |
| `r1313.C2_catalogue_name_on_any_link` | `src/cratekit/label/tidal_catalogue.py` | user | 3 file(s) | 290 | 1 | killed |
| `u294.M01_rows_narrowed_keeps_all` | `src/cratekit/tagging/rows.py` | user | 2 file(s) | 128 | 11 | killed |
| `u294.M02_rows_narrowed_changes_unfiltered` | `src/cratekit/tagging/rows.py` | user | 2 file(s) | 128 | 21 | killed |
| `u294.M23_rows_read_back` | `src/cratekit/tagging/rows_cli.py` | user | 2 file(s) | 128 | 1 | killed |
| `u227.R16_join_state` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 128 | 5 | killed |
| `u227.R17_join_held` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 128 | 1 | killed |
| `u227.R18_join_blank` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 128 | 1 | killed |
| `u157.F1_cut_zero` | `src/cratekit/core/config.py` | user | 2 file(s) | 281 | 2 | killed |
| `u157.F2_cut_nan` | `src/cratekit/core/config.py` | user | 2 file(s) | 281 | 1 | killed |
| `r290-author.S07_rebuild_call_removed` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 126 | 6 | killed |
| `r312.W6_type_not_carried` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 126 | 1 | killed |
| `r290-author.S05_intake_call_removed` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 126 | 11 | killed |
| `r790-c.C1_config_floor` | `src/cratekit/core/config.py` | user | 2 file(s) | 280 | 1 | killed |
| `r790-c.C2_config_built` | `src/cratekit/core/config.py` | user | 2 file(s) | 280 | 1 | killed |
| `u211.W1_writer_falls_back` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 273 | 15 | killed |
| `u211.W7_writer_unconfirmed_with_nothing_read` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 273 | 2 | killed |
| `r888.R1_roster_serves_one_listing` | `src/cratekit/label/tidal_catalogue.py` | user | 5 file(s) | 578 | 3 | killed |
| `r361-a.A7_mark_verb_forgets_debris` | `src/cratekit/sync/mark_cli.py` | user | 2 file(s) | 116 | 1 | killed |
| `r361-a.A8_mark_verb_respells_the_word` | `src/cratekit/sync/mark_cli.py` | user | 2 file(s) | 116 | 1 | killed |
| `r361-a.A9_reword_the_why` | `src/cratekit/sync/mark_cli.py` | user | 2 file(s) | 116 | 1 | killed |
| `r44-a.C4_identity_not_read` | `src/cratekit/core/config.py` | user | 2 file(s) | 568 | 2 | killed |
| `u123.L1_dated_vouched` | `src/cratekit/modules/outbound/ledger.py` | user | 3 file(s) | 114 | 20 | killed |
| `u123.L2_forget_drops_the_entry` | `src/cratekit/modules/outbound/ledger.py` | user | 3 file(s) | 114 | 2 | killed |
| `u123.L3_malformed_entry_dropped` | `src/cratekit/modules/outbound/ledger.py` | maintainer | 3 file(s) | 114 | 1 | killed |
| `u128-b.B4_bridge_owned_dropped` | `src/cratekit/intake/ingest.py` | user | 8 file(s) | 256 | 2 | killed |
| `u128-b.B5_bridge_record_no_account` | `src/cratekit/intake/ingest.py` | user | 8 file(s) | 256 | 3 | killed |
| `r924.A1_no_plan_line` | `src/cratekit/intake/acrcloud.py` | user | 3 file(s) | 255 | 4 | killed |
| `r924.A2_plan_before_the_bounds` | `src/cratekit/intake/acrcloud.py` | user | 3 file(s) | 255 | 1 | killed |
| `u62.C2_outage_as_credential` | `src/cratekit/label/catalogue.py` | user | 4 file(s) | 544 | 4 | killed |
| `r777.N1_empty_proof` | `src/cratekit/sync/marks.py` | maintainer | 2 file(s) | 100 | 1 | killed |
| `r777.N2_neither_proof` | `src/cratekit/sync/marks.py` | maintainer | 2 file(s) | 100 | 1 | killed |
| `r777.N3_engine_unchecked` | `src/cratekit/sync/marks.py` | user | 2 file(s) | 100 | 3 | killed |
| `u180.M7_children_live_only` | `src/cratekit/favorites/placement.py` | user | 2 file(s) | 96 | 3 | killed |
| `u180.M8_slots_lift_shared` | `src/cratekit/favorites/placement.py` | user | 2 file(s) | 96 | 4 | killed |
| `u180.M9_seat_skips_unmoved` | `src/cratekit/favorites/placement.py` | user | 2 file(s) | 96 | 7 | killed |
| `r791-b.T1_sources_unread_disposition` | `src/cratekit/tagging/tag.py` | user | 3 file(s) | 240 | 12 | killed |
| `r791-b.T2_art_names_unread` | `src/cratekit/tagging/tag.py` | user | 3 file(s) | 240 | 1 | killed |
| `u126.P3_gate_fact` | `src/cratekit/intake/land_cli.py` | user | 10 file(s) | 529 | 4 | killed |
| `sitting4.G10_absent_root_reads_as_untagged` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 236 | 1 | killed |
| `sitting4.G3_builders_ignore_the_prefix_map` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 236 | 1 | killed |
| `u212.N3_taken_plain` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 6 | 2 | killed |
| `u212.N4_plan_isrc` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 6 | 1 | killed |
| `u212.N6_cause_step` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 6 | 1 | killed |
| `u42-author.W2_unreadable_reported` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 229 | 2 | killed |
| `u90-c.C1_swallow_every_refusal` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 229 | 1 | killed |
| `u108-c.G25_drive_maps_ending` | `src/cratekit/acquire/cli.py` | user | 7 file(s) | 508 | 31 | killed |
| `r290-author.R2_backup_rebuild_drops_the_type` | `src/cratekit/backup/cli.py` | user | 2 file(s) | 225 | 2 | killed |
| `r290-author.S04_backup_call_removed` | `src/cratekit/backup/cli.py` | user | 2 file(s) | 225 | 11 | killed |
| `r390-a.A5_refusal_drops_the_inner_cause` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 224 | 4 | killed |
| `u89.L1_absent_is_default` | `src/cratekit/write/metadata_cli.py` | user | 2 file(s) | 223 | 126 | killed |
| `u89.L2_tagging_default` | `src/cratekit/write/metadata_cli.py` | user | 2 file(s) | 223 | 12 | killed |
| `r731-b.M13_gate_without_the_review_list` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 81 | 4 | killed |
| `r731-b.M14_gate_without_the_count` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 81 | 3 | killed |
| `r731-b.M15_gate_without_the_read_state` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 81 | 2 | killed |
| `r1476.M20_named_first_only` | `src/cratekit/label/registry.py` | user | 6 file(s) | 497 | 7 | killed |
| `u113-c.C6_names_checked_after_moves` | `src/cratekit/intake/landing.py` | user | 2 file(s) | 79 | 1 | killed |
| `u113-c.C1_native_batch_always` | `src/cratekit/intake/native.py` | user | 2 file(s) | 79 | 8 | killed |
| `u113-c.C2_native_batch_keeps_claimed` | `src/cratekit/intake/native.py` | user | 2 file(s) | 79 | 9 | killed |
| `u179.T2_rehearsal_ack_attends` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 214 | 1 | killed |

## Row definitions

### `u192.T1_typed_label_on_queue`

tag_folder: hand the queue's own --label to the resume, so a sweep driven at its queue says its label was not applied

- File: `src/cratekit/tagging/cli.py`
- Source: `u192.json`, row `T1_typed_label_on_queue`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`
- Collected: 166 against a baseline of 166
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_sweep_driven_at_its_queue_keeps_the_label_warning_and_never_calls_its_label_unapplied`

Old text:

```
        lambda: _resume(ctx, cfg, job.job_id, typed_label=None, queued=label_warnings),
```

New text:

```
        lambda: _resume(ctx, cfg, job.job_id, typed_label=ctx.args.label, queued=label_warnings),
```

### `u192.T2_queue_warnings_lost`

tag_folder: drop the queue's label warnings from the settled answer

- File: `src/cratekit/tagging/cli.py`
- Source: `u192.json`, row `T2_queue_warnings_lost`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`
- Collected: 166 against a baseline of 166
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_sweep_driven_at_its_queue_keeps_the_label_warning_and_never_calls_its_label_unapplied`

Old text:

```
        lambda: _resume(ctx, cfg, job.job_id, typed_label=None, queued=label_warnings),
```

New text:

```
        lambda: _resume(ctx, cfg, job.job_id, typed_label=None),
```

### `u192.T3_resume_label_unsaid`

tag_folder --job: stop passing the typed --label, so a label typed on a resume is applied silently in the report's eyes

- File: `src/cratekit/tagging/cli.py`
- Source: `u192.json`, row `T3_resume_label_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`
- Collected: 166 against a baseline of 166
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_label_typed_on_a_resume_is_not_applied_and_says_so`
  - `tests/test_label_genre.py::test_a_label_typed_on_a_resume_is_still_said_to_be_unapplied`

Old text:

```
        return _resume(ctx, cfg, ctx.args.job, typed_label=ctx.args.label)
```

New text:

```
        return _resume(ctx, cfg, ctx.args.job, typed_label=None)
```

### `u246.S5_inspiration_held_empty`

assert_read_back (inspiration): an empty set of live rows, so every planned row reads as missing and the write refuses

- File: `src/cratekit/organize/inspiration.py`
- Source: `u246.json`, row `S5_inspiration_held_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`, `tests/test_u242_taken.py`, `tests/test_write_session.py`, `tests/test_organize.py`
- Collected: 333 against a baseline of 333
- Kills: 9 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_read_back_holding_a_row_the_plan_did_not_name_is_refused`
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
        held = set(live)
```

New text:

```
        held = set()
```

### `u246.S6_inspiration_planned_live`

assert_read_back (inspiration): the planned set built from the live rows, so the refusal names no unplanned row

- File: `src/cratekit/organize/inspiration.py`
- Source: `u246.json`, row `S6_inspiration_planned_live`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`, `tests/test_u242_taken.py`, `tests/test_write_session.py`, `tests/test_organize.py`
- Collected: 333 against a baseline of 333
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_read_back_holding_a_row_the_plan_did_not_name_is_refused`

Old text:

```
            planned = set(one.members)
```

New text:

```
            planned = set(live)
```

### `r501-d.R2_settled_is_not_imported`

routing_cli._all_settled: count acknowledged tracks as proof, so a run nobody imported is recorded as proven

- File: `src/cratekit/write/routing_cli.py`
- Source: `r501-d.json`, row `R2_settled_is_not_imported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_deferred_routing.py`, `tests/test_routing_workers.py`
- Collected: 329 against a baseline of 329
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_tracks_acknowledged_as_gone_are_not_proof_of_an_import`

Old text:

```
    return bool(routed) and not ledger.outstanding(session_id)
```

New text:

```
    return not ledger.outstanding(session_id)
```

### `r501-d.R3_pass_is_proof`

routing_cli._close_if_settled: never record the pass as proof, so after a cutover no landed run can close

- File: `src/cratekit/write/routing_cli.py`
- Source: `r501-d.json`, row `R3_pass_is_proof`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_deferred_routing.py`, `tests/test_routing_workers.py`
- Collected: 329 against a baseline of 329
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_after_a_cutover_the_pass_placing_every_track_is_proof_and_closes_the_run`

Old text:

```
        if record.state is session.SessionState.AWAITING_IMPORT and _all_settled(
```

New text:

```
        if False and _all_settled(
```

### `u246.S3_set_playlist_order_set_empty`

assert_read_back (set playlist): an empty set of wanted ids, so a filled playlist always reads as out of order and refuses

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u246.json`, row `S3_set_playlist_order_set_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`, `tests/test_export_set.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_write_session.py`, `tests/test_inbox_refill.py`
- Collected: 323 against a baseline of 323
- Kills: 29 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_backfill_a_week_later_adds_to_a_playlist_pre_made_under_the_posted_name`
  - `tests/test_set_inspiration_playlist.py::test_a_file_two_collection_rows_claim_is_left_out_rather_than_one_row_picked`
  - `tests/test_set_inspiration_playlist.py::test_a_filled_playlist_holding_a_row_it_found_still_reads_back_in_set_order`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archive_failure_is_a_warning_on_the_envelope`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archive_not_renamed_is_a_warning_on_the_envelope`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archives_the_account_playlist_as_taken_in_its_year_folder`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_creates_the_declared_folder_at_the_root_when_the_library_lacks_it`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_honours_posted_on_a_pre_freeze_job`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_with_a_page_date_names_the_playlist_for_the_posted_day`
  - `tests/test_set_inspiration_playlist.py::test_a_recorded_playlist_that_was_removed_is_not_added_to_and_a_live_one_is_made`
  - `tests/test_set_inspiration_playlist.py::test_a_removed_namesake_under_the_folder_is_not_written_into`
  - `tests/test_set_inspiration_playlist.py::test_a_rerun_that_adds_nothing_records_no_commit`
  - `tests/test_set_inspiration_playlist.py::test_a_row_neither_owned_nor_landed_is_counted_and_named_and_not_added`
  - `tests/test_set_inspiration_playlist.py::test_a_second_write_that_fills_a_gap_mid_set_is_not_a_failed_write`
  - ... and 14 more, see the JSON sidecar

Old text:

```
    named = set(wanted)
```

New text:

```
    named = set()
```

### `u246.S4_set_playlist_order_set_read_back`

assert_read_back (set playlist): the set built from the read back, so a stranger row in a filled playlist no longer breaks the order

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u246.json`, row `S4_set_playlist_order_set_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`, `tests/test_export_set.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_write_session.py`, `tests/test_inbox_refill.py`
- Collected: 323 against a baseline of 323
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_filled_playlist_holding_a_row_it_found_still_reads_back_in_set_order`

Old text:

```
    named = set(wanted)
```

New text:

```
    named = set(written.read_back)
```

### `u221.R12_hold_not_written`

Pair.to_json: write no hold, so the next read finds none and a twin made since U221 falls to the time rule

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u221.json`, row `R12_hold_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair.py`
- Collected: 153 against a baseline of 153
- Kills: 18 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_backfilled_pair_merges_both_ways_and_queues_the_added_track_once`
  - `tests/test_sync_twins_hold.py::test_a_held_track_whose_linked_row_left_the_library_is_still_counted_and_released`
  - `tests/test_sync_twins_hold.py::test_a_landing_twin_records_an_empty_hold`
  - `tests/test_sync_twins_hold.py::test_a_name_that_is_no_twin_is_refused_and_nothing_is_planned`
  - `tests/test_sync_twins_hold.py::test_a_released_twin_asks_nothing_the_second_time`
  - `tests/test_sync_twins_hold.py::test_a_second_twin_stays_held_when_the_first_is_released`
  - `tests/test_sync_twins_hold.py::test_a_track_added_later_on_the_account_is_queued_and_the_held_stay_held`
  - `tests/test_sync_twins_hold.py::test_a_track_an_earlier_sync_queued_is_awaiting_not_on_hold`
  - `tests/test_sync_twins_hold.py::test_a_twin_paired_again_since_the_plan_is_left_held`
  - `tests/test_sync_twins_hold.py::test_a_twin_paired_before_u221_is_released_by_name_and_counted_by_time`
  - `tests/test_sync_twins_hold.py::test_a_twin_with_three_missing_tracks_queues_none_and_names_three_on_hold`
  - `tests/test_sync_twins_hold.py::test_an_abort_lets_nothing_go`
  - `tests/test_sync_twins_hold.py::test_release_all_lets_every_twin_go`
  - `tests/test_sync_twins_hold.py::test_release_hold_passes_over_a_pair_that_is_no_twin_and_one_holding_nothing`
  - `tests/test_sync_twins_hold.py::test_release_needs_names_or_all_and_not_both[args0]`
  - ... and 3 more, see the JSON sidecar

Old text:

```
        if self.on_hold is not None:
            record["on_hold"] = dict(sorted(self.on_hold.items()))
```

New text:

```
        if False:
            record["on_hold"] = dict(sorted(self.on_hold.items()))
```

### `u221.R13_hold_not_read`

PairStore._pair: read no hold, so every twin falls to the time rule and a released one is held again

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u221.json`, row `R13_hold_not_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair.py`
- Collected: 153 against a baseline of 153
- Kills: 18 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_backfilled_pair_merges_both_ways_and_queues_the_added_track_once`
  - `tests/test_sync_twins_hold.py::test_a_held_track_whose_linked_row_left_the_library_is_still_counted_and_released`
  - `tests/test_sync_twins_hold.py::test_a_landing_twin_records_an_empty_hold`
  - `tests/test_sync_twins_hold.py::test_a_name_that_is_no_twin_is_refused_and_nothing_is_planned`
  - `tests/test_sync_twins_hold.py::test_a_released_twin_asks_nothing_the_second_time`
  - `tests/test_sync_twins_hold.py::test_a_second_twin_stays_held_when_the_first_is_released`
  - `tests/test_sync_twins_hold.py::test_a_track_added_later_on_the_account_is_queued_and_the_held_stay_held`
  - `tests/test_sync_twins_hold.py::test_a_track_an_earlier_sync_queued_is_awaiting_not_on_hold`
  - `tests/test_sync_twins_hold.py::test_a_twin_paired_again_since_the_plan_is_left_held`
  - `tests/test_sync_twins_hold.py::test_a_twin_paired_before_u221_is_released_by_name_and_counted_by_time`
  - `tests/test_sync_twins_hold.py::test_a_twin_with_three_missing_tracks_queues_none_and_names_three_on_hold`
  - `tests/test_sync_twins_hold.py::test_an_abort_lets_nothing_go`
  - `tests/test_sync_twins_hold.py::test_release_all_lets_every_twin_go`
  - `tests/test_sync_twins_hold.py::test_release_hold_passes_over_a_pair_that_is_no_twin_and_one_holding_nothing`
  - `tests/test_sync_twins_hold.py::test_release_needs_names_or_all_and_not_both[args0]`
  - ... and 3 more, see the JSON sidecar

Old text:

```
            on_hold=None if on_hold is None else MappingProxyType(dict(on_hold)),
```

New text:

```
            on_hold=None,
```

### `u221.R14_hold_unvalidated`

PairStore._pair: accept a hold that is not ids to words, so a damaged document is read rather than refused

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u221.json`, row `R14_hold_unvalidated`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair.py`
- Collected: 153 against a baseline of 153
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_a_hold_that_is_not_ids_to_words_refuses_the_document[bad0]`
  - `tests/test_sync_twins_hold.py::test_a_hold_that_is_not_ids_to_words_refuses_the_document[bad1]`
  - `tests/test_sync_twins_hold.py::test_a_hold_that_is_not_ids_to_words_refuses_the_document[bad2]`
  - `tests/test_sync_twins_hold.py::test_a_hold_that_is_not_ids_to_words_refuses_the_document[t1]`

Old text:

```
        if on_hold is not None and not (
```

New text:

```
        if False and not (
```

### `u27-adopt-apply-author.A1_approval_actor_is_the_process`

Mint the approval under a fixed actor, so the record cannot say who asserted it

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u27-adopt-apply-author.json`, row `A1_approval_actor_is_the_process`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`
- Collected: 642 against a baseline of 642
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_the_approval_names_whoever_answered_the_gate`

Old text:

```
            approval=grant(plan, actor=actor),
```

New text:

```
            approval=grant(plan, actor="cli"),
```

### `r1255.S6_records_refuses_unlisted`

records: answer an unlisted log as no session again, so restore list, restore run and session release read it as empty

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S6_records_refuses_unlisted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_session_cli.py`, `tests/test_restore.py`, `tests/test_doctor.py`
- Collected: 634 against a baseline of 634
- Kills: 5 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_session_log_that_cannot_be_listed_refuses_the_release_before_its_question`
  - `tests/test_session_log_unlisted.py::test_restore_list_refuses_a_log_it_cannot_list_rather_than_list_nothing`
  - `tests/test_session_log_unlisted.py::test_restore_run_refuses_naming_the_listing_not_an_unrecorded_session`
  - `tests/test_session_log_unlisted.py::test_the_native_landing_lookups_refuse_a_log_they_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_reporting_reader_refuses_a_log_it_cannot_list`

Old text:

```
    if log_unlisted(unreadable, cfg):
        raise refuse(
```

New text:

```
    if False:
        raise refuse(
```

### `r770-a.A4_refusal_asks_for_a_defect_report`

assert_intake_on_the_bridge: give the refusal the remedy the finding was about

- File: `src/cratekit/intake/ingest.py`
- Source: `r770-a.json`, row `A4_refusal_asks_for_a_defect_report`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`
- Collected: 47 against a baseline of 47
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_writers_native.py::test_a_bridge_apply_on_a_native_tree_moves_nothing_and_keeps_the_splices_cause`
  - `tests/test_intake_writers_native.py::test_the_bridge_landing_engine_refuses_a_native_tree_the_same_way`
  - `tests/test_intake_writers_native.py::test_the_splice_refuses_a_native_intake_tree_naming_the_landing`
  - `tests/test_intake_writers_native.py::test_the_splice_refuses_a_native_tree_before_it_looks_for_the_export`

Old text:

```
        remedy=Remedy.FIX_COMMAND_LINE,
```

New text:

```
        remedy=Remedy.REPORT_DEFECT,
```

### `r770-a.A5_tree_built_without_the_refusal`

bridge_intake_tree: build the tree without asking first, the layer the landing's pre-move check rests on alone

- File: `src/cratekit/intake/ingest.py`
- Source: `r770-a.json`, row `A5_tree_built_without_the_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`
- Collected: 47 against a baseline of 47
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_writers_native.py::test_a_bridge_apply_on_a_native_tree_moves_nothing_and_keeps_the_splices_cause`
  - `tests/test_intake_writers_native.py::test_the_bridge_landing_engine_refuses_a_native_tree_the_same_way`
  - `tests/test_intake_writers_native.py::test_the_intake_tree_is_built_in_one_place_and_that_place_refuses_first`

Old text:

```
    assert_intake_on_the_bridge(declared, registry)
    return rbxml.intake_tree(declared, registry)
```

New text:

```
    return rbxml.intake_tree(declared, registry)
```

### `r770-a.A6_splice_asks_only_after_the_export`

place_files: drop the refusal made before the export is looked for, leaving the one made where the tree is built

- File: `src/cratekit/intake/ingest.py`
- Source: `r770-a.json`, row `A6_splice_asks_only_after_the_export`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`
- Collected: 47 against a baseline of 47
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_writers_native.py::test_the_splice_refuses_a_native_tree_before_it_looks_for_the_export`

Old text:

```
    if declared is not None and registry is not None:
        assert_intake_on_the_bridge(declared, registry)
```

New text:

```
    if declared is not None and registry is not None:
        pass
```

### `r1634.M11_reread_reads_the_line`

TidalCatalogue.reread_release: judge the listed object's own line instead of reading the album

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r1634.json`, row `M11_reread_reads_the_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 15 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_the_newest_held_release_names_the_label`
  - `tests/test_label_canary.py::test_a_degraded_provider_still_refuses_though_a_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_lone_withdrawn_held_release_refuses`
  - `tests/test_label_canary.py::test_a_provider_that_answers_with_no_credit_for_the_new_ones_answers_nothing_new`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_never_replaced_by_another_acts`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_passed_over_for_the_next_and_the_label_has_nothing_new`
  - `tests/test_label_canary.py::test_an_unanswered_release_with_no_held_release_to_read_refuses_as_before`
  - `tests/test_label_canary.py::test_the_shipped_reread_of_a_release_the_provider_no_longer_has_is_no_credit`
  - `tests/test_label_canary.py::test_the_shipped_reread_reads_the_provider_though_the_release_carries_a_line`
  - `tests/test_label_canary.py::test_the_worker_answers_nothing_new_when_the_provider_reads_the_held_release`
  - `tests/test_label_canary.py::test_the_worker_passes_over_a_withdrawn_held_release_too`
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_two_withdrawn_held_releases_refuse_and_no_third_is_read`
  - `tests/test_label_canary.py::test_with_a_drop_given_no_credit_the_held_label_line_comes_before_another_acts`

Old text:

```
            album = self._album(identity)
        except ReleaseUnresolvable as exc:
```

New text:

```
            album = release
        except ReleaseUnresolvable as exc:
```

### `r1634.M12_gone_confirms`

TidalCatalogue.reread_release: answer a withdrawn release confirmed

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r1634.json`, row `M12_gone_confirms`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_lone_withdrawn_held_release_refuses`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_never_replaced_by_another_acts`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_passed_over_for_the_next_and_the_label_has_nothing_new`
  - `tests/test_label_canary.py::test_the_shipped_reread_of_a_release_the_provider_no_longer_has_is_no_credit`
  - `tests/test_label_canary.py::test_the_worker_passes_over_a_withdrawn_held_release_too`
  - `tests/test_label_canary.py::test_two_withdrawn_held_releases_refuse_and_no_third_is_read`

Old text:

```
                "verdict": RELEASE_GONE,
```

New text:

```
                "verdict": "confirmed",
```

### `r1313.C1_catalogue_failure_alone`

_gone: read the 404 off the failure alone, as before R-1313, so a release answered with a 404 page climbs the ladder and fails as an outage

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r1313.json`, row `C1_catalogue_failure_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_isrc_cache.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 290 against a baseline of 290
- Kills: 5 (killed)
- Killed:
  - `tests/test_provider_not_found_bodies.py::test_a_404_is_a_not_found_whatever_its_body[404-html-catalogue]`
  - `tests/test_provider_not_found_bodies.py::test_a_release_answered_by_a_404_page_is_gone_at_once`
  - `tests/test_provider_not_found_bodies.py::test_a_rewrapped_404_page_is_a_not_found[catalogue]`
  - `tests/test_provider_not_found_bodies.py::test_an_isrc_answered_by_a_404_page_is_asked_once_and_kept[catalogue]`
  - `tests/test_provider_not_found_bodies.py::test_off_the_declared_chain_a_links_cause_is_nearer_than_what_it_was_handling`

Old text:

```
    if "notfound" in type(exc).__name__.lower():
        return True
    return answered_not_found(exc)
```

New text:

```
    if "notfound" in type(exc).__name__.lower():
        return True
    return getattr(getattr(exc, "response", None), "status_code", None) == 404
```

### `r1313.C2_catalogue_name_on_any_link`

_gone: read a not found class name on any link, so a parse failure met while handling a not found reads the release as gone

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r1313.json`, row `C2_catalogue_name_on_any_link`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_isrc_cache.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 290 against a baseline of 290
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_not_found_bodies.py::test_a_name_reached_only_as_context_is_not_a_not_found`

Old text:

```
    if "notfound" in type(exc).__name__.lower():
        return True
    return answered_not_found(exc)
```

New text:

```
    if any("notfound" in type(one).__name__.lower() for one, _ in provider_session.failure_links(exc)):
        return True
    return answered_not_found(exc)
```

### `u294.M01_rows_narrowed_keeps_all`

rows.narrowed: hold out no write, so the campaign's tag rows step writes every row the verb would, joining and other routed rows included

- File: `src/cratekit/tagging/rows.py`
- Source: `u294.json`, row `M01_rows_narrowed_keeps_all`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`, `tests/test_tag_rows.py`
- Collected: 128 against a baseline of 128
- Kills: 11 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_a_file_that_comes_to_carry_the_word_after_the_gate_stops_the_words_as_stale`
  - `tests/test_tag_campaign.py::test_a_folder_answer_makes_the_folder_and_the_rows_follow_their_files`
  - `tests/test_tag_campaign.py::test_a_follower_whose_file_carries_another_spelling_is_held_out`
  - `tests/test_tag_campaign.py::test_a_rows_plan_narrowed_to_nothing_writes_nothing`
  - `tests/test_tag_campaign.py::test_a_rows_plan_narrowed_writes_only_the_rows_kept_and_holds_the_rest_out`
  - `tests/test_tag_campaign.py::test_a_step_that_refuses_stops_the_campaign_with_the_earlier_writes_named`
  - `tests/test_tag_campaign.py::test_a_word_left_or_unanswered_is_named_and_nothing_retags_it`
  - `tests/test_tag_campaign.py::test_an_unexpected_failure_in_a_step_is_this_builds_defect_with_what_landed`
  - `tests/test_tag_campaign.py::test_only_the_genre_column_moves_on_a_written_row`
  - `tests/test_tag_campaign.py::test_rows_joining_needs_genre_and_any_other_routed_row_are_never_written`
  - `tests/test_tag_campaign.py::test_the_whole_campaign_lands_and_needs_genre_falls_as_measured`

Old text:

```
    held = {item.content_id for item in plan.writes if item.content_id not in kept}
```

New text:

```
    held = set()
```

### `u294.M02_rows_narrowed_changes_unfiltered`

rows.narrowed: leave every change in the write, so a held row is written though its item says held

- File: `src/cratekit/tagging/rows.py`
- Source: `u294.json`, row `M02_rows_narrowed_changes_unfiltered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`, `tests/test_tag_rows.py`
- Collected: 128 against a baseline of 128
- Kills: 21 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_a_file_that_comes_to_carry_the_word_after_the_gate_stops_the_words_as_stale`
  - `tests/test_tag_campaign.py::test_a_folder_answer_makes_the_folder_and_the_rows_follow_their_files`
  - `tests/test_tag_campaign.py::test_a_folder_that_would_copy_another_bucket_after_the_gate_stops_the_words_as_stale`
  - `tests/test_tag_campaign.py::test_a_follower_whose_file_carries_another_spelling_is_held_out`
  - `tests/test_tag_campaign.py::test_a_person_reads_the_campaign_and_the_resort_it_leaves`
  - `tests/test_tag_campaign.py::test_a_rows_plan_narrowed_to_nothing_writes_nothing`
  - `tests/test_tag_campaign.py::test_a_rows_plan_narrowed_writes_only_the_rows_kept_and_holds_the_rest_out`
  - `tests/test_tag_campaign.py::test_a_step_that_refuses_after_part_of_it_landed_reports_what_the_census_reads`
  - `tests/test_tag_campaign.py::test_a_step_that_refuses_stops_the_campaign_with_the_earlier_writes_named`
  - `tests/test_tag_campaign.py::test_a_word_left_or_unanswered_is_named_and_nothing_retags_it`
  - `tests/test_tag_campaign.py::test_an_alias_to_the_folder_another_answer_makes_is_planned_on_that_folder`
  - `tests/test_tag_campaign.py::test_an_unexpected_failure_in_a_step_is_this_builds_defect_with_what_landed`
  - `tests/test_tag_campaign.py::test_every_file_an_alias_retags_is_on_the_gate_and_in_the_digest`
  - `tests/test_tag_campaign.py::test_only_the_genre_column_moves_on_a_written_row`
  - `tests/test_tag_campaign.py::test_rows_joining_needs_genre_and_any_other_routed_row_are_never_written`
  - ... and 6 more, see the JSON sidecar

Old text:

```
        changes=tuple(change for change in plan.changes.changes if change.content_id not in held),
```

New text:

```
        changes=tuple(plan.changes.changes),
```

### `u294.M23_rows_read_back`

tag rows' apply path no longer refuses over a row that does not read back

- File: `src/cratekit/tagging/rows_cli.py`
- Source: `u294.json`, row `M23_rows_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`, `tests/test_tag_rows.py`
- Collected: 128 against a baseline of 128
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_a_row_that_does_not_read_back_refuses_the_rows_step`

Old text:

```
    rows.assert_read_back(written)
    return written
```

New text:

```
    return written
```

### `u227.R16_join_state`

join_run: write a job in any state, so a running or finished job is moved into a pass

- File: `src/cratekit/core/jobs.py`
- Source: `u227.json`, row `R16_join_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_mirror_downloads.py`, `tests/test_jobs.py`, `tests/test_export_set_rename.py`
- Collected: 128 against a baseline of 128
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_land_mirror_downloads.py::test_join_run_refuses_every_other_job[blocked]`
  - `tests/test_sync_land_mirror_downloads.py::test_join_run_refuses_every_other_job[cancelled]`
  - `tests/test_sync_land_mirror_downloads.py::test_join_run_refuses_every_other_job[failed]`
  - `tests/test_sync_land_mirror_downloads.py::test_join_run_refuses_every_other_job[running]`
  - `tests/test_sync_land_mirror_downloads.py::test_join_run_refuses_every_other_job[succeeded]`

Old text:

```
        if current.state is not JobState.QUEUED or held:
```

New text:

```
        if held:
```

### `u227.R17_join_held`

join_run: write a job that already carries a run, moving it between passes

- File: `src/cratekit/core/jobs.py`
- Source: `u227.json`, row `R17_join_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_mirror_downloads.py`, `tests/test_jobs.py`, `tests/test_export_set_rename.py`
- Collected: 128 against a baseline of 128
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_mirror_downloads.py::test_join_run_refuses_every_other_job[has-a-run]`

Old text:

```
        if current.state is not JobState.QUEUED or held:
```

New text:

```
        if current.state is not JobState.QUEUED:
```

### `u227.R18_join_blank`

join_run: accept a blank run

- File: `src/cratekit/core/jobs.py`
- Source: `u227.json`, row `R18_join_blank`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_mirror_downloads.py`, `tests/test_jobs.py`, `tests/test_export_set_rename.py`
- Collected: 128 against a baseline of 128
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_mirror_downloads.py::test_join_run_refuses_every_other_job[blank]`

Old text:

```
    if not wanted:
        raise refuse(
```

New text:

```
    if False:
        raise refuse(
```

### `u157.F1_cut_zero`

_validate_drift_cut: accept a cut of zero, which marks every measured track

- File: `src/cratekit/core/config.py`
- Source: `u157.json`, row `F1_cut_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_drift.py`, `tests/test_config.py`
- Collected: 281 against a baseline of 281
- Kills: 2 (killed)
- Killed:
  - `tests/test_drift.py::test_a_cut_that_is_not_a_percent_above_zero_is_refused_at_load[0.0]`
  - `tests/test_drift.py::test_a_cut_that_is_not_a_percent_above_zero_is_refused_at_load[0]`

Old text:

```
        or value <= 0
        or value > 100
```

New text:

```
        or value < 0
        or value > 100
```

### `u157.F2_cut_nan`

_validate_drift_cut: accept a cut that is not finite

- File: `src/cratekit/core/config.py`
- Source: `u157.json`, row `F2_cut_nan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_drift.py`, `tests/test_config.py`
- Collected: 281 against a baseline of 281
- Kills: 1 (killed)
- Killed:
  - `tests/test_drift.py::test_a_cut_that_is_not_a_percent_above_zero_is_refused_at_load[nan]`

Old text:

```
        or not math.isfinite(value)
        or value <= 0
```

New text:

```
        or value <= 0
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

### `r290-author.S05_intake_call_removed`

Remove the one jobs.raise_for_state call from intake/cli.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/intake/cli.py`
- Source: `r290-author.json`, row `S05_intake_call_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`
- Collected: 126 against a baseline of 126
- Kills: 11 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[intake.playlist]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[intake.set]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[intake.playlist]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[intake.set]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[intake.playlist]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[intake.set]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[intake.playlist]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[intake.set]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[intake.playlist]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[intake.set]`
  - `tests/test_job_outcome.py::test_every_function_that_drives_a_job_maps_its_ending_afterwards`

Old text:

```
jobs.raise_for_state(job)
```

New text:

```
jobs.get  # the mapping call, removed
```

### `r790-c.C1_config_floor`

_validate_labels: accept zero

- File: `src/cratekit/core/config.py`
- Source: `r790-c.json`, row `C1_config_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`, `tests/test_config.py`
- Collected: 280 against a baseline of 280
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_the_configured_offer_must_be_a_positive_whole_number[0]`

Old text:

```
        not isinstance(offer, int) or isinstance(offer, bool) or offer < 1
```

New text:

```
        not isinstance(offer, int) or isinstance(offer, bool) or offer < 0
```

### `r790-c.C2_config_built`

from_dict: ignore the labels section and always take the default

- File: `src/cratekit/core/config.py`
- Source: `r790-c.json`, row `C2_config_built`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`, `tests/test_config.py`
- Collected: 280 against a baseline of 280
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_the_configured_offer_is_the_default_for_every_label`

Old text:

```
        labels=_build(LabelsConfig, data.get("labels") or {}),
```

New text:

```
        labels=LabelsConfig(),
```

### `u211.W1_writer_falls_back`

_asked_or_scanned: re-raise pyrekordbox's error instead of asking the careful scan, the defect itself

- File: `src/cratekit/core/rb_writer.py`
- Source: `u211.json`, row `W1_writer_falls_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`, `tests/test_rb_writer_guard.py`
- Collected: 273 against a baseline of 273
- Kills: 15 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[agent]`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[both]`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[none]`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[rekordbox]`
  - `tests/test_process_scan.py::test_the_binding_probe_at_open_only_loses_a_warning`
  - `tests/test_process_scan.py::test_the_binding_probe_is_put_back_after_a_refusal`
  - `tests/test_process_scan.py::test_the_binding_probe_names_rekordbox_at_commit`
  - `tests/test_process_scan.py::test_the_binding_probe_refuses_a_live_unreadable_process_at_commit`
  - `tests/test_process_scan.py::test_the_binding_probe_skips_a_zombie_at_commit`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`
  - `tests/test_process_scan.py::test_the_writer_refuses_a_live_unreadable_process_by_name_not_as_internal`
  - `tests/test_process_scan.py::test_the_writer_refuses_a_read_agent_as_running_not_as_unconfirmed`
  - `tests/test_process_scan.py::test_the_writer_skips_a_zombie_pyrekordbox_could_not_read`
  - `tests/test_process_scan.py::test_the_writer_still_sees_rekordbox_beside_the_dying_process`

Old text:

```
        return processes.rekordbox_pid(name)
```

New text:

```
        raise
```

### `u211.W7_writer_unconfirmed_with_nothing_read`

rekordbox_processes_running in the writer: a probe that could not confirm, with no rekordbox process read at all, answers clear instead of refusing

- File: `src/cratekit/core/rb_writer.py`
- Source: `u211.json`, row `W7_writer_unconfirmed_with_nothing_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`, `tests/test_rb_writer_guard.py`
- Collected: 273 against a baseline of 273
- Kills: 2 (killed)
- Killed:
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[none]`
  - `tests/test_process_scan.py::test_the_writer_refuses_a_live_unreadable_process_by_name_not_as_internal`

Old text:

```
        if not running:
            raise unconfirmed
```

New text:

```
        if False:
            raise unconfirmed
```

### `r888.R1_roster_serves_one_listing`

LabelRoster.held: the roster answers its albums for every listing, so its singles are never read

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r888.json`, row `R1_roster_serves_one_listing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 578 against a baseline of 578
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_listing_a_roster_does_not_hold_is_skipped_and_recorded`
  - `tests/test_label_tidal_catalogue.py::test_the_roster_crawls_the_label_page_and_every_seed_through_the_listing`
  - `tests/test_label_tidal_catalogue.py::test_the_roster_lists_once_when_it_is_built_and_the_crawl_reads_memory`

Old text:

```
        return self._listed.get(method)
```

New text:

```
        return self._listed.get("get_albums")
```

### `r361-a.A7_mark_verb_forgets_debris`

The mark verb's plan no longer decides label-debris, so the playlist falls through to the reports

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r361-a.json`, row `A7_mark_verb_forgets_debris`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 116 against a baseline of 116
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_the_label_batch_debris_is_said_and_never_renamed`

Old text:

```
        elif playlists.is_library_debris(entry.name):
            entry.reason = LABEL_DEBRIS
        elif job.state is not jobs.JobState.SUCCEEDED:
```

New text:

```
        elif job.state is not jobs.JobState.SUCCEEDED:
```

### `r361-a.A8_mark_verb_respells_the_word`

The mark verb spells its own word for the reason instead of reading the enum

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r361-a.json`, row `A8_mark_verb_respells_the_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 116 against a baseline of 116
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_the_label_batch_debris_is_said_and_never_renamed`

Old text:

```
LABEL_DEBRIS = str(playlists.Excluded.LABEL_DEBRIS)
```

New text:

```
LABEL_DEBRIS = "label-library"
```

### `r361-a.A9_reword_the_why`

The why sentence is reworded, never appended to, since the suite asserts with in

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r361-a.json`, row `A9_reword_the_why`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 116 against a baseline of 116
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_the_label_batch_debris_is_said_and_never_renamed`

Old text:

```
        "its name is the source system's label run debris, which a sync never "
        "offers and never renames"
```

New text:

```
        "its name is a throwaway the other system left, which a sync never "
        "offers and never renames"
```

### `r44-a.C4_identity_not_read`

Never read a rule's identity in, so every configured rule arrives unrecorded

- File: `src/cratekit/core/config.py`
- Source: `r44-a.json`, row `C4_identity_not_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_deletion.py`
- Collected: 568 against a baseline of 568
- Kills: 2 (killed)
- Killed:
  - `tests/test_config.py::test_a_prefix_rule_carries_the_identity_of_the_volume_it_points_at`
  - `tests/test_deletion.py::test_the_rules_the_pass_builds_from_configuration_carry_each_recorded_identity`

Old text:

```
                    volume_id=entry.get(PREFIX_VOLUME_IDENTITY_KEY),
```

New text:

```
                    volume_id=None,
```

### `u123.L1_dated_vouched`

Stop the ledger vouching for a dated playlist it records

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u123.json`, row `L1_dated_vouched`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_dated.py`, `tests/test_prune.py`
- Collected: 114 against a baseline of 114
- Kills: 20 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_dated_entry_that_is_not_a_name_to_an_identifier_is_not_vouched_for`
  - `tests/test_label_heard.py::test_a_dated_playlist_made_by_the_dated_plan_is_vouched_for_and_one_reused_is_not`
  - `tests/test_label_heard.py::test_a_delete_the_client_answers_false_is_a_failure`
  - `tests/test_label_heard.py::test_a_folder_with_no_year_playlist_refuses_when_there_is_something_to_add`
  - `tests/test_label_heard.py::test_a_named_release_already_heard_is_said_and_writes_nothing`
  - `tests/test_label_heard.py::test_a_playlist_already_gone_is_removed_with_no_delete`
  - `tests/test_label_heard.py::test_a_playlist_still_served_after_its_delete_is_refused_not_reported_removed`
  - `tests/test_label_heard.py::test_a_playlist_the_client_does_not_serve_as_owned_is_refused_in_words`
  - `tests/test_label_heard.py::test_a_removal_refused_part_way_names_the_adds_marks_nothing_and_a_resume_finishes`
  - `tests/test_label_heard.py::test_a_track_an_unheard_release_also_carries_stays_on_the_dated_playlist`
  - `tests/test_label_heard.py::test_a_track_the_year_will_not_take_keeps_the_dated_playlist`
  - `tests/test_label_heard.py::test_a_year_known_only_by_the_marks_prefixed_name_is_the_year`
  - `tests/test_label_heard.py::test_an_adopted_year_still_wins_over_a_dated_entry_for_the_same_identifier`
  - `tests/test_label_heard.py::test_declined_nothing_is_written`
  - `tests/test_label_heard.py::test_every_run_says_the_record_labels_tree_is_not_changed`
  - ... and 5 more, see the JSON sidecar

Old text:

```
        if wanted in (record.get("dated") or {}).values():
            made = True
```

New text:

```
        if False:
            made = True
```

### `u123.L2_forget_drops_the_entry`

Keep a removed dated playlist's ledger entry

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u123.json`, row `L2_forget_drops_the_entry`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_dated.py`, `tests/test_prune.py`
- Collected: 114 against a baseline of 114
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_dated_playlist_made_by_the_dated_plan_is_vouched_for_and_one_reused_is_not`
  - `tests/test_label_heard.py::test_heard_writes_the_ids_merges_and_removes_and_a_second_run_is_a_no_op`

Old text:

```
        kept = {name: pid for name, pid in held.items() if pid != str(remote_id)}
```

New text:

```
        kept = dict(held)
```

### `u123.L3_malformed_entry_dropped`

Keep a dated entry with an empty name or identifier

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u123.json`, row `L3_malformed_entry_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_dated.py`, `tests/test_prune.py`
- Collected: 114 against a baseline of 114
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_dated_entry_that_is_not_a_name_to_an_identifier_is_not_vouched_for`

Old text:

```
            {"dated": {str(name): str(pid) for name, pid in dated.items() if name and pid}}
```

New text:

```
            {"dated": {str(name): str(pid) for name, pid in dated.items()}}
```

### `u128-b.B4_bridge_owned_dropped`

The intake file's playlist names no owned TrackID, the new files alone

- File: `src/cratekit/intake/ingest.py`
- Source: `u128-b.json`, row `B4_bridge_owned_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_landing.py`, `tests/test_landing_head.py`
- Collected: 256 against a baseline of 256
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists.py::test_an_owned_track_in_two_account_playlists_is_in_both`

Old text:

```
            else:
                held.append(member)
        return list(dict.fromkeys(held))
```

New text:

```
        return list(dict.fromkeys(held))
```

### `u128-b.B5_bridge_record_no_account`

The intake file's record names no account, so a rerun cannot find what it mirrored

- File: `src/cratekit/intake/ingest.py`
- Source: `u128-b.json`, row `B5_bridge_record_no_account`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_landing.py`, `tests/test_landing_head.py`
- Collected: 256 against a baseline of 256
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_bridge_landing_is_what_a_rerun_of_its_pass_reads_as_mirrored`
  - `tests/test_intake_land_account_playlists.py::test_an_abandoned_landing_is_not_read_as_mirrored`
  - `tests/test_intake_land_account_playlists.py::test_the_intake_record_names_each_playlist_and_its_batch_folder`

Old text:

```
                INBOX_ACCOUNT_KEY: one.account,
```

New text:

```
                INBOX_ACCOUNT_KEY: "",
```

### `r924.A1_no_plan_line`

Identification never states its plan before the first call

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r924.json`, row `A1_no_plan_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`, `tests/intake/test_workers.py`, `tests/intake/test_recognition.py`
- Collected: 255 against a baseline of 255
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_a_cached_recording_says_so_and_counts_no_calls`
  - `tests/intake/test_set_progress.py::test_a_parted_set_says_its_parts_in_the_plan`
  - `tests/intake/test_set_progress.py::test_human_output_says_the_fetch_then_the_plan_then_the_count`
  - `tests/intake/test_set_progress.py::test_the_planned_count_is_the_chunks_the_carver_is_asked_for`

Old text:

```
    if progress is not None:
        progress(_plan_line(len(offsets), cached=len(offsets) - len(owed), parts=len(parts)))
```

New text:

```
    if False:
        progress(_plan_line(len(offsets), cached=len(offsets) - len(owed), parts=len(parts)))
```

### `r924.A2_plan_before_the_bounds`

The plan line is said before the month bound and the credential read, so a refused run is told it will pay

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r924.json`, row `A2_plan_before_the_bounds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`, `tests/intake/test_workers.py`, `tests/intake/test_recognition.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_a_run_the_month_refuses_is_not_told_it_will_pay`

Old text:

```
    keys = ("", "")
    if owed:
        assert_month_within(spend, planned=len(owed), used_this_month=counter.used(month))
        keys = credentials()
    # AFTER EVERY REFUSAL THAT SPENDS NOTHING, so a run told it is about to pay
    # is a run that will, and one refused by a bound or a missing key is told
    # only the refusal.
    offsets = tuple(offset for part in parts for offset in part)
    if progress is not None:
        progress(_plan_line(len(offsets), cached=len(offsets) - len(owed), parts=len(parts)))
```

New text:

```
    keys = ("", "")
    offsets = tuple(offset for part in parts for offset in part)
    if progress is not None:
        progress(_plan_line(len(offsets), cached=len(offsets) - len(owed), parts=len(parts)))
    if owed:
        assert_month_within(spend, planned=len(owed), used_this_month=counter.used(month))
        keys = credentials()
```

### `u62.C2_outage_as_credential`

Refuse an unreachable provider as a credential problem

- File: `src/cratekit/label/catalogue.py`
- Source: `u62.json`, row `C2_outage_as_credential`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/intake/test_workers.py`
- Collected: 544 against a baseline of 544
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_provider_that_cannot_be_reached_is_a_wait_not_a_new_login[connection]`
  - `tests/test_label_tidal_catalogue.py::test_a_provider_that_cannot_be_reached_is_a_wait_not_a_new_login[server-error]`
  - `tests/test_label_tidal_catalogue.py::test_a_provider_that_cannot_be_reached_is_a_wait_not_a_new_login[timeout]`
  - `tests/test_label_tidal_catalogue.py::test_a_provider_that_cannot_be_reached_is_a_wait_not_a_new_login[unparseable-page]`

Old text:

```
    except ProviderUnavailable as exc:
        raise refuse(
            "unavailable-transient",
```

New text:

```
    except ProviderUnavailable as exc:
        raise refuse(
            "credential-missing",
```

### `r777.N1_empty_proof`

marks.require_proof accepts a NativeLanding naming no tree, no pass or no landing

- File: `src/cratekit/sync/marks.py`
- Source: `r777.json`, row `N1_empty_proof`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_mark.py`
- Collected: 100 against a baseline of 100
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_the_engine_refuses_a_mark_with_neither_proof`

Old text:

```
        if not local_output.tree_id or not local_output.pass_name or not local_output.landings:
```

New text:

```
        if False:
```

### `r777.N2_neither_proof`

marks.require_proof hands anything that is not a NativeLanding to require_output, so None is no longer refused by name

- File: `src/cratekit/sync/marks.py`
- Source: `r777.json`, row `N2_neither_proof`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_mark.py`
- Collected: 100 against a baseline of 100
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_the_engine_refuses_a_mark_with_neither_proof`

Old text:

```
    if not isinstance(local_output, Path):
```

New text:

```
    if False:
```

### `r777.N3_engine_unchecked`

apply_deferred no longer checks its proof before renaming

- File: `src/cratekit/sync/marks.py`
- Source: `r777.json`, row `N3_engine_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_mark.py`
- Collected: 100 against a baseline of 100
- Kills: 3 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_external_marks_wait_for_local_output_and_recheck`
  - `tests/test_sync_mark.py::test_the_engine_refuses_a_mark_with_neither_proof`
  - `tests/test_sync_mark.py::test_the_file_check_makes_one_stat_and_refuses_whatever_it_raises`

Old text:

```
    require_proof(local_output)
    applied: list[str] = []
```

New text:

```
    applied: list[str] = []
```

### `u180.M7_children_live_only`

children: a soft deleted child is read, ranked and moved like a live one

- File: `src/cratekit/favorites/placement.py`
- Source: `u180.json`, row `M7_children_live_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_order.py`
- Collected: 96 against a baseline of 96
- Kills: 3 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_a_soft_deleted_month_is_neither_moved_nor_counted`
  - `tests/test_favorites_order.py::test_the_order_takes_the_positions_the_live_children_hold_and_no_other`
  - `tests/test_favorites_placement.py::test_a_removed_sibling_keeps_its_position_when_a_month_is_seated`

Old text:

```
        for row in db.get_playlist(ParentID=str(folder_id))
        if not rb_writer.node_removed(row)
```

New text:

```
        for row in db.get_playlist(ParentID=str(folder_id))
        if True
```

### `u180.M8_slots_lift_shared`

slots: a position two rows share is not lifted apart, so the order is written with a tie rekordbox can read either way

- File: `src/cratekit/favorites/placement.py`
- Source: `u180.json`, row `M8_slots_lift_shared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_order.py`
- Collected: 96 against a baseline of 96
- Kills: 4 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_the_order_takes_the_positions_the_live_children_hold_and_no_other`
  - `tests/test_favorites_placement.py::test_the_slots_are_the_rows_own_positions_with_a_shared_one_lifted[held3-given3]`
  - `tests/test_favorites_placement.py::test_the_slots_are_the_rows_own_positions_with_a_shared_one_lifted[held4-given4]`
  - `tests/test_favorites_placement.py::test_the_slots_are_the_rows_own_positions_with_a_shared_one_lifted[held5-given5]`

Old text:

```
        given.append(value if not given or value > given[-1] else given[-1] + 1)
```

New text:

```
        given.append(value)
```

### `u180.M9_seat_skips_unmoved`

seat: every row is written, its position unchanged or not

- File: `src/cratekit/favorites/placement.py`
- Source: `u180.json`, row `M9_seat_skips_unmoved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_order.py`
- Collected: 96 against a baseline of 96
- Kills: 7 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_a_folder_oldest_first_reads_newest_first_with_all_favorites_first_and_undated_last`
  - `tests/test_favorites_order.py::test_a_non_month_playlist_keeps_its_relative_place_after_the_months`
  - `tests/test_favorites_order.py::test_a_second_run_after_the_order_asks_nothing`
  - `tests/test_favorites_order.py::test_a_soft_deleted_month_is_neither_moved_nor_counted`
  - `tests/test_favorites_order.py::test_only_a_row_whose_position_changes_is_written`
  - `tests/test_favorites_order.py::test_the_order_takes_the_positions_the_live_children_hold_and_no_other`
  - `tests/test_favorites_order.py::test_the_verb_refuses_an_answer_the_read_back_does_not_hold`

Old text:

```
        if seq_of(row) == slot:
            continue
        row.Seq = slot
```

New text:

```
        row.Seq = slot
```

### `r791-b.T1_sources_unread_disposition`

tag_one: a decline naming unread sources is reported no-hit

- File: `src/cratekit/tagging/tag.py`
- Source: `r791-b.json`, row `T1_sources_unread_disposition`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_catalogue_searcher.py`
- Collected: 240 against a baseline of 240
- Kills: 12 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_a_sweep_with_no_discogs_token_says_so_and_reads_no_file_as_no_hit`
  - `tests/test_tag_workers.py::test_an_outage_keeps_its_own_word_in_the_sweeps_warning`
  - `tests/test_tag_workers.py::test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit`
  - `tests/test_tag_workers.py::test_files_with_no_isrc_are_counted_and_warned_about_whatever_their_skip_reason`
  - `tests/test_tag_workers.py::test_one_unread_file_beside_a_parse_break_is_counted_and_the_defect_is_said`
  - `tests/test_tag_workers.py::test_the_sweeps_unread_warning_names_discogs_first`
  - `tests/test_tagging_engine.py::test_a_decline_beside_an_unread_catalogue_is_sources_unread_and_not_no_hit`

Old text:

```
        elif hit.unread:
```

New text:

```
        elif False:
```

### `r791-b.T2_art_names_unread`

_art_embedded: the picture decline never names the unread sources

- File: `src/cratekit/tagging/tag.py`
- Source: `r791-b.json`, row `T2_art_names_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_catalogue_searcher.py`
- Collected: 240 against a baseline of 240
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_decline_beside_an_unread_catalogue_is_sources_unread_and_not_no_hit`

Old text:

```
        unread = hit.unread if hit is not None else ()
```

New text:

```
        unread = ()
```

### `u126.P3_gate_fact`

Rename the content link fact on the gate screen, so the value and its count are not where the person reads them

- File: `src/cratekit/intake/land_cli.py`
- Source: `u126.json`, row `P3_gate_fact`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 529 against a baseline of 529
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_landing_that_adds_no_row_needs_no_majority`
  - `tests/test_intake_land_native.py::test_the_content_link_counts_move_the_digest`
  - `tests/test_intake_land_native.py::test_the_gate_screen_names_every_row_its_columns_the_playlist_and_the_database`
  - `tests/test_intake_writers_native.py::test_the_gate_screen_names_the_row_its_columns_the_playlist_and_the_database`

Old text:

```
        "content link": (
```

New text:

```
        "link": (
```

### `sitting4.G10_absent_root_reads_as_untagged`

The mount guard is removed, so an unplugged volume reads as a library of untagged files and the sweep succeeds unmatched

- File: `src/cratekit/modules/outbound/source.py`
- Source: `sitting4.json`, row `G10_absent_root_reads_as_untagged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_outbound_tidal_account.py`
- Collected: 236 against a baseline of 236
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_an_absent_library_root_refuses_rather_than_reading_every_row_untagged`

Old text:

```
    root = Path(cfg.library.root)
    if root.is_dir():
        return
    raise refuse(
        "library-volume-unmounted",
        f"the library root {root} is not a directory on this machine, so no "
```

New text:

```
    root = Path(cfg.library.root)
    if True:
        return
    raise refuse(
        "library-volume-unmounted",
        f"the library root {root} is not a directory on this machine, so no "
```

### `sitting4.G3_builders_ignore_the_prefix_map`

The builders hand the resolver an empty map, so a renamed drive resolves no row (R-372)

- File: `src/cratekit/modules/outbound/source.py`
- Source: `sitting4.json`, row `G3_builders_ignore_the_prefix_map`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_outbound_tidal_account.py`
- Collected: 236 against a baseline of 236
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_the_row_builders_use_the_configured_prefix_map`

Old text:

```
    return [
        locations.PrefixRule(source_prefix, target)
        for source_prefix, target in cfg.resolved_prefix_map()
    ]
```

New text:

```
    return []
```

### `u212.N3_taken_plain`

naming_cli._taken: always the plain collision, never a second copy

- File: `src/cratekit/write/naming_cli.py`
- Source: `u212.json`, row `N3_taken_plain`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_second_copy.py`
- Collected: 6 against a baseline of 6
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_second_copy.py::test_a_copy_that_takes_the_name_after_the_plan_is_said_a_second_copy`
  - `tests/test_naming_second_copy.py::test_a_target_held_by_the_same_recording_is_said_as_a_second_copy`

Old text:

```
    same = second_copy(path, target)
    if same:
```

New text:

```
    same = second_copy(path, target)
    if False:
```

### `u212.N4_plan_isrc`

naming_cli._plan_for: the plan item carries no ISRC

- File: `src/cratekit/write/naming_cli.py`
- Source: `u212.json`, row `N4_plan_isrc`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_second_copy.py`
- Collected: 6 against a baseline of 6
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_second_copy.py::test_a_target_held_by_the_same_recording_is_said_as_a_second_copy`

Old text:

```
            if str(path) in seconds:
                item["isrc"] = seconds[str(path)]
```

New text:

```
(empty)
```

### `u212.N6_cause_step`

naming_cli._incomplete_cause: the second copy step is never added

- File: `src/cratekit/write/naming_cli.py`
- Source: `u212.json`, row `N6_cause_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_second_copy.py`
- Collected: 6 against a baseline of 6
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_second_copy.py::test_a_target_held_by_the_same_recording_is_said_as_a_second_copy`

Old text:

```
    if any(item.get("isrc") for item in incomplete):
```

New text:

```
    if False:
```

### `u42-author.W2_unreadable_reported`

Collect the unreadable directories and then never report them

- File: `src/cratekit/acquire/cli.py`
- Source: `u42-author.json`, row `W2_unreadable_reported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reserved_causes.py`
- Collected: 229 against a baseline of 229
- Kills: 2 (killed)
- Killed:
  - `tests/test_reserved_causes.py::test_pinned_populations_derive_totals_and_key_by_module`
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`

Old text:

```
    found += [_item(path, root, "path-unreadable") for path in unreadable]
```

New text:

```
(empty)
```

### `u90-c.C1_swallow_every_refusal`

The previous cut reader swallows every refusal, the permission one included

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-c.json`, row `C1_swallow_every_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reserved_causes.py`
- Collected: 229 against a baseline of 229
- Kills: 1 (killed)
- Killed:
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`

Old text:

```
        if exc.cause.reason != "vocal-calibration-unreadable":
            raise

```

New text:

```
(empty)
```

### `u108-c.G25_drive_maps_ending`

acquire_cli.drive_queued: a parked or half failed job is returned as if it ended clean

- File: `src/cratekit/acquire/cli.py`
- Source: `u108-c.json`, row `G25_drive_maps_ending`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_intake_missing.py`, `tests/test_label_sync_go.py`, `tests/test_listdoc.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 508 against a baseline of 508
- Kills: 31 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_mid_batch_defect_fails_that_item_and_the_resume_the_job_refuses_fetches_nothing`
  - `tests/test_acquire_workers.py::test_a_provider_block_parks_the_job_and_makes_no_further_request`
  - `tests/test_acquire_workers.py::test_a_refusal_beside_a_network_failure_fails_and_keeps_the_refusal_skipped`
  - `tests/test_acquire_workers.py::test_an_authentication_failure_parks_the_run_and_names_the_replacement_path`
  - `tests/test_acquire_workers.py::test_three_landed_and_one_network_failure_still_fails`
  - `tests/test_label_sync_go.py::test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run`
  - `tests/test_label_sync_go.py::test_a_download_that_ended_half_failed_is_retried_by_the_next_go_and_only_its_failures`
  - `tests/test_label_sync_go.py::test_a_download_that_finished_while_a_go_resumed_another_refuses_the_resumes_tail`
  - `tests/test_label_sync_go.py::test_a_fresh_go_that_landed_another_runs_download_records_it_on_that_run`
  - `tests/test_label_sync_go.py::test_a_go_parked_by_a_rate_limit_names_its_own_go_for_after_the_park`
  - `tests/test_label_sync_go.py::test_a_go_resumed_under_another_run_names_the_run_that_queued_it_to_continue`
  - `tests/test_label_sync_go.py::test_a_go_stopped_at_the_ceiling_finishes_and_lands_on_the_next_go_under_its_run`
  - `tests/test_label_sync_go.py::test_a_go_stopped_at_the_ceiling_names_its_own_go_to_continue_not_the_job`
  - `tests/test_label_sync_go.py::test_a_go_whose_job_was_cancelled_still_refuses_and_lands_nothing`
  - `tests/test_label_sync_go.py::test_a_go_whose_job_was_finished_by_hand_lands_on_the_next_go_with_no_new_decision`
  - ... and 16 more, see the JSON sidecar

Old text:

```
    jobs.raise_for_state(job)
    return job, warnings
```

New text:

```
    return job, warnings
```

### `r290-author.R2_backup_rebuild_drops_the_type`

Rebuild the backup rehearsal refusal as a plain CratekitError again, so a rehearsal the worker parked says failed

- File: `src/cratekit/backup/cli.py`
- Source: `r290-author.json`, row `R2_backup_rebuild_drops_the_type`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_backup_cli.py`
- Collected: 225 against a baseline of 225
- Kills: 2 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
  - `tests/test_job_outcome.py::test_a_reworded_refusal_is_rebuilt_in_one_place_only`

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

### `r290-author.S04_backup_call_removed`

Remove the one jobs.raise_for_state call from backup/cli.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/backup/cli.py`
- Source: `r290-author.json`, row `S04_backup_call_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_backup_cli.py`
- Collected: 225 against a baseline of 225
- Kills: 11 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`
  - `tests/test_backup_cli.py::test_asking_twice_about_a_half_failed_backup_answers_the_same_way_twice`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[backup.run]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[backup.run]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[backup.run]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[backup.run]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[backup.run]`
  - `tests/test_job_outcome.py::test_every_function_that_drives_a_job_maps_its_ending_afterwards`

Old text:

```
jobs.raise_for_state(job)
```

New text:

```
jobs.get  # the mapping call, removed
```

### `r390-a.A5_refusal_drops_the_inner_cause`

the refusal no longer nests the job's own cause, so the item's reason is unreachable

- File: `src/cratekit/core/jobs.py`
- Source: `r390-a.json`, row `A5_refusal_drops_the_inner_cause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_master_cli.py`, `tests/test_acquire_workers.py`
- Collected: 224 against a baseline of 224
- Kills: 4 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_mid_batch_defect_fails_that_item_and_the_resume_the_job_refuses_fetches_nothing`
  - `tests/test_jobs.py::test_a_partial_failure_whose_failures_are_permanent_is_not_resumable`
  - `tests/test_jobs.py::test_resuming_a_job_of_permanent_failures_through_the_verb_refuses`
  - `tests/test_master_cli.py::test_a_job_that_failed_on_a_missing_source_is_not_reopened_and_a_fresh_job_masters_it`

Old text:

```
                **_permanent_reasons_of(current.cause),
            },
            inner=current.cause,
        )
```

New text:

```
                **_permanent_reasons_of(current.cause),
            },
        )
```

### `u89.L1_absent_is_default`

load_vocal_threshold: an absent calibration returns the default cut instead of None, so routing files from a cut nobody fitted

- File: `src/cratekit/write/metadata_cli.py`
- Source: `u89.json`, row `L1_absent_is_default`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`, `tests/test_metadata_cli.py`
- Collected: 223 against a baseline of 223
- Kills: 126 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_a_library_with_no_tag_category_refuses_through_the_verb`
  - `tests/test_metadata_cli.py::test_a_plan_only_run_leaves_no_record`
  - `tests/test_metadata_cli.py::test_a_second_apply_is_idempotent`
  - `tests/test_metadata_cli.py::test_a_second_apply_writes_nothing_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_absent_vocal_calibration_is_the_default_cut`
  - `tests/test_metadata_cli.py::test_an_apply_is_listed_by_restore_list_as_a_restorable_session`
  - `tests/test_metadata_cli.py::test_an_apply_that_refuses_mid_write_is_abandoned_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_apply_whose_commit_lands_and_then_raises_is_recorded_as_committed`
  - `tests/test_metadata_cli.py::test_apply_writes_my_tags_and_does_not_write_a_content_column`
  - `tests/test_metadata_cli.py::test_the_capture_is_protected_while_the_apply_is_in_flight`
  - `tests/test_metadata_cli.py::test_the_plan_names_existing_rows_and_writes_nothing`
  - `tests/test_routing_workers.py::test_a_25_minute_track_is_a_member_and_a_19_minute_one_is_not`
  - `tests/test_routing_workers.py::test_a_bare_lf_before_a_folder_close_is_a_skipped_create_and_the_file_parses`
  - `tests/test_routing_workers.py::test_a_clean_apply_names_no_skipped_file`
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_applies_on_an_encrypted_library`
  - ... and 111 more, see the JSON sidecar

Old text:

```
    if not path.is_file():
        return None
```

New text:

```
    if not path.is_file():
        return DEFAULT_VOCAL_THRESHOLD
```

### `u89.L2_tagging_default`

vocal_cut: drop the default fallback, so an uncalibrated My Tags pass has no cut

- File: `src/cratekit/write/metadata_cli.py`
- Source: `u89.json`, row `L2_tagging_default`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`, `tests/test_metadata_cli.py`
- Collected: 223 against a baseline of 223
- Kills: 12 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_a_library_with_no_tag_category_refuses_through_the_verb`
  - `tests/test_metadata_cli.py::test_a_plan_only_run_leaves_no_record`
  - `tests/test_metadata_cli.py::test_a_second_apply_is_idempotent`
  - `tests/test_metadata_cli.py::test_a_second_apply_writes_nothing_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_absent_vocal_calibration_is_the_default_cut`
  - `tests/test_metadata_cli.py::test_an_apply_is_listed_by_restore_list_as_a_restorable_session`
  - `tests/test_metadata_cli.py::test_an_apply_that_refuses_mid_write_is_abandoned_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_apply_whose_commit_lands_and_then_raises_is_recorded_as_committed`
  - `tests/test_metadata_cli.py::test_apply_writes_my_tags_and_does_not_write_a_content_column`
  - `tests/test_metadata_cli.py::test_the_capture_is_protected_while_the_apply_is_in_flight`
  - `tests/test_metadata_cli.py::test_the_plan_names_existing_rows_and_writes_nothing`
  - `tests/test_routing_workers.py::test_the_loader_says_absent_as_none_and_the_tagging_cut_still_defaults`

Old text:

```
    return DEFAULT_VOCAL_THRESHOLD if threshold is None else threshold
```

New text:

```
    return threshold
```

### `r731-b.M13_gate_without_the_review_list`

the gate's facts no longer carry the list of withheld entries

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `r731-b.json`, row `M13_gate_without_the_review_list`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`, `tests/test_adopt_apply_cli.py`
- Collected: 81 against a baseline of 81
- Kills: 4 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_person_reading_the_gate_is_shown_the_whole_list`
  - `tests/test_adopt_workers.py::test_a_second_approved_apply_adds_nothing_and_withholds_the_same`
  - `tests/test_adopt_workers.py::test_a_track_in_the_planned_sub_under_another_name_is_withheld_not_doubled`
  - `tests/test_adopt_workers.py::test_the_gate_counts_the_withheld_by_kind_and_lists_every_one`

Old text:

```
            "held_elsewhere": document["held_elsewhere"],

```

New text:

```
(empty)
```

### `r731-b.M14_gate_without_the_count`

the gate's facts no longer carry the withheld count split by kind

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `r731-b.json`, row `M14_gate_without_the_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`, `tests/test_adopt_apply_cli.py`
- Collected: 81 against a baseline of 81
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_person_reading_the_gate_is_shown_the_whole_list`
  - `tests/test_adopt_workers.py::test_a_second_approved_apply_adds_nothing_and_withholds_the_same`
  - `tests/test_adopt_workers.py::test_the_gate_counts_the_withheld_by_kind_and_lists_every_one`

Old text:

```
            "withheld_by_placement": document["withheld_by_placement"],

```

New text:

```
(empty)
```

### `r731-b.M15_gate_without_the_read_state`

the gate's facts no longer say whether the tree was read

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `r731-b.json`, row `M15_gate_without_the_read_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`, `tests/test_adopt_apply_cli.py`
- Collected: 81 against a baseline of 81
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_an_uncut_library_says_its_tree_was_not_read`
  - `tests/test_adopt_workers.py::test_the_gate_counts_the_withheld_by_kind_and_lists_every_one`

Old text:

```
            "placements": document["placements"],

```

New text:

```
(empty)
```

### `r1476.M20_named_first_only`

Registry.named: answer only the first holder, as by_name does

- File: `src/cratekit/label/registry.py`
- Source: `r1476.json`, row `M20_named_first_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`
- Collected: 497 against a baseline of 497
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_files_own_tag_naming_a_shared_name_is_given_neither_labels_genre`
  - `tests/test_label_genre.py::test_a_label_sharing_its_name_with_one_carrying_a_genre_is_never_given_that_genre`
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[ Alpha ]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[ALPHA]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[Alpha]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[alpha]`

Old text:

```
        return tuple(entry for entry in self.labels.values() if _name_key(entry.name) == wanted)
```

New text:

```
        return tuple(entry for entry in self.labels.values() if _name_key(entry.name) == wanted)[:1]
```

### `u113-c.C6_names_checked_after_moves`

The native landing no longer asks whether a chosen name was taken before its first move

- File: `src/cratekit/intake/landing.py`
- Source: `u113-c.json`, row `C6_names_checked_after_moves`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`
- Collected: 79 against a baseline of 79
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_name_inbox_came_to_hold_after_the_plan_is_refused_and_nothing_is_written`

Old text:

```
    native.assert_names_still_free(db, rows)
```

New text:

```
    pass
```

### `u113-c.C1_native_batch_always`

The native write always makes the batch playlist, empty when every row was claimed

- File: `src/cratekit/intake/native.py`
- Source: `u113-c.json`, row `C1_native_batch_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`
- Collected: 79 against a baseline of 79
- Kills: 8 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`
  - `tests/test_intake_land_account_playlists_native.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists_native.py::test_a_track_both_playlists_brought_in_is_a_member_of_both`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_an_undated_playlist_from_before_u175_is_left_as_it_is`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_the_rotation_ages_an_account_playlist_by_its_landing_date`
  - `tests/test_intake_land_account_playlists_native.py::test_two_swept_playlists_land_as_two_playlist_rows_under_their_exact_names`

Old text:

```
            if ordered or not accounts:
```

New text:

```
            if True:
```

### `u113-c.C2_native_batch_keeps_claimed`

The native batch playlist holds the claimed rows too

- File: `src/cratekit/intake/native.py`
- Source: `u113-c.json`, row `C2_native_batch_keeps_claimed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`
- Collected: 79 against a baseline of 79
- Kills: 9 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`
  - `tests/test_intake_land_account_playlists_native.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists_native.py::test_a_track_both_playlists_brought_in_is_a_member_of_both`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_an_undated_playlist_from_before_u175_is_left_as_it_is`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_the_rotation_ages_an_account_playlist_by_its_landing_date`
  - `tests/test_intake_land_account_playlists_native.py::test_two_swept_playlists_land_as_two_playlist_rows_under_their_exact_names`

Old text:

```
                if str(row.target) in by_target and str(row.target) not in claimed
```

New text:

```
                if str(row.target) in by_target
```

### `u179.T2_rehearsal_ack_attends`

rehearse: a missing acknowledgment at the rehearsal ends the verb as a failure, not for a person

- File: `src/cratekit/cli/tail.py`
- Source: `u179.json`, row `T2_rehearsal_ack_attends`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 214 against a baseline of 214
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_rehearsal_that_needs_the_acknowledgment_names_the_rehearsal_then_the_landing`

Old text:

```
        if cause.reason == ACK_STOP or cause.code in gates.GATE_CODES:
            raise Attend(REHEARSE, argv, cause)
```

New text:

```
        if cause.code in gates.GATE_CODES:
            raise Attend(REHEARSE, argv, cause)
```

