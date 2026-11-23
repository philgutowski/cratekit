# Mutation table: u325-after-l-31

Measured by `scripts/mutate.py` on 2026-11-22 23:51 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 146.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:22 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 72, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u270.J6_missing_outcome_fails` | `src/cratekit/core/jobs.py` | user | 2 file(s) | 145 | 1 | killed |
| `u293.S3_sync_land_holds` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 144 | 1 | killed |
| `r1255.S8_clause_listing_wording` | `src/cratekit/core/session.py` | user | 3 file(s) | 142 | 9 | killed |
| `u270.J1_claim_batch_size_floor` | `src/cratekit/core/jobs.py` | maintainer | 3 file(s) | 134 | 1 | killed |
| `r669-b.B1_composer_not_sanitized` | `src/cratekit/core/naming.py` | user | 2 file(s) | 133 | 2 | killed |
| `u114.M18_narrow_called` | `src/cratekit/tagging/rows.py` | user | 2 file(s) | 131 | 21 | killed |
| `r1255.T1_tree_registry_clause` | `src/cratekit/core/tree_registry.py` | user | 3 file(s) | 125 | 2 | killed |
| `u56-catalogue-searcher-and-tag-workers.R26_retag_queues_no_items` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 122 | 20 | killed |
| `r1634.M16_worker_drops_how` | `src/cratekit/label/cli.py` | user | 2 file(s) | 119 | 1 | killed |
| `u242.M21_mark_cli_already_marked_by_title` | `src/cratekit/sync/mark_cli.py` | user | 2 file(s) | 115 | 1 | killed |
| `u242.M9_take_overwrites_a_held_entry` | `src/cratekit/sync/mark_record.py` | user | 2 file(s) | 115 | 1 | killed |
| `u144-c.C9_parent_of_named` | `src/cratekit/intake/set_playlist.py` | user | 2 file(s) | 112 | 12 | killed |
| `u319.M9_warning_drops_the_short_path` | `src/cratekit/intake/land_cli.py` | user | 3 file(s) | 106 | 1 | killed |
| `u181.C3_unscored_flag_ignored` | `src/cratekit/vocals/cli.py` | user | 2 file(s) | 105 | 4 | killed |
| `u113-b.B2_batch_keeps_claimed` | `src/cratekit/intake/ingest.py` | user | 3 file(s) | 105 | 10 | killed |
| `u179.P1_shared_preflight` | `src/cratekit/cli/sync_land.py` | user | 2 file(s) | 104 | 3 | killed |
| `r746-b.N8_unsupported_file_moved_anyway` | `src/cratekit/intake/landing.py` | user | 2 file(s) | 103 | 1 | killed |
| `u140.B6_mark_refusal_dropped` | `src/cratekit/export/set_cli.py` | user | 2 file(s) | 102 | 2 | killed |
| `u142.S12_undeclared_reads_as_empty` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 100 | 1 | killed |
| `r722.A1_gate_drops_tally` | `src/cratekit/adopt/apply_cli.py` | user | 3 file(s) | 99 | 1 | killed |
| `u175.R1_account_ids_unrecorded` | `src/cratekit/intake/rotate.py` | user | 4 file(s) | 98 | 3 | killed |
| `u261.H6_app_not_asked_again` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 96 | 3 | killed |
| `u288.M15_append_past_highest` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 96 | 2 | killed |
| `r770-a.A2_unreachable_root_is_read_anyway` | `src/cratekit/intake/ingest.py` | user | 2 file(s) | 95 | 3 | killed |
| `r235-b.M25_adoption_refusal_names_no_verb` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 94 | 2 | killed |
| `u267.M4_handle_opens_every_time` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 92 | 6 | killed |
| `u319.M8_ok_on_any_field` | `src/cratekit/intake/land_cli.py` | user | 3 file(s) | 92 | 2 | killed |
| `u242.M8_twins_reads_the_title_alone` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 92 | 1 | killed |
| `u150.F2_record_provider` | `src/cratekit/intake/native.py` | user | 2 file(s) | 90 | 1 | killed |
| `u267.M12_inspiration_set_folder_write_guard` | `src/cratekit/export/set_cli.py` | maintainer | 2 file(s) | 88 | 1 | killed |
| `u156.L25_shared_rule_near_match` | `src/cratekit/intake/landing.py` | user | 2 file(s) | 85 | 1 | killed |
| `u135.A14_set_order_reverses` | `src/cratekit/intake/native.py` | user | 2 file(s) | 85 | 3 | killed |
| `u242.M7_inspiration_reads_the_title_alone` | `src/cratekit/organize/inspiration.py` | user | 2 file(s) | 85 | 1 | killed |
| `u221.R15_mark_drops_the_hold` | `src/cratekit/modules/outbound/pairs.py` | user | 3 file(s) | 84 | 14 | killed |
| `r746-a.G4_read_back_walks_session_new_only` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 81 | 2 | killed |
| `r746-a.G6_analysis_tables_not_checked` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 81 | 1 | killed |
| `u221.R19_short_listing_records_its_misses` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 78 | 1 | killed |
| `u219.K3_accept_declined` | `src/cratekit/cli/rebuild.py` | user | 2 file(s) | 77 | 1 | killed |
| `u113-b.B5_export_clash_unasked` | `src/cratekit/intake/landing.py` | user | 2 file(s) | 76 | 1 | killed |
| `u185.G5_reading_at_open` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 75 | 20 | killed |
| `u130-c.C5_no_renumber` | `src/cratekit/write/playlist_pair.py` | user | 1 file(s) | 75 | 3 | killed |
| `u243.L7_kept_read_judged_blind` | `src/cratekit/label/kept_reads.py` | user | 2 file(s) | 74 | 4 | killed |
| `u166.R2_rotate_reserved` | `src/cratekit/intake/rotate.py` | user | 3 file(s) | 74 | 1 | killed |
| `u130-c.C6_pair_not_vouched` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 73 | 5 | killed |
| `u81-fetch-b.Q5_owned_row_fetched` | `src/cratekit/acquire/fallback_cli.py` | user | 2 file(s) | 72 | 3 | killed |
| `u247.M8_scan_freezes_its_declaration` | `src/cratekit/adopt/scan_cli.py` | user | 2 file(s) | 72 | 1 | killed |
| `u246.S16_inspiration_held_per_element` | `src/cratekit/organize/inspiration.py` | maintainer | 2 file(s) | 72 | 1 | killed |
| `u119.G16_read_back_blind_to_leftovers` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u164.W2_preflight_target` | `src/cratekit/intake/landing.py` | maintainer | 2 file(s) | 69 | 1 | killed |
| `u150.L1_forget_checks_id` | `src/cratekit/modules/outbound/ledger.py` | user | 2 file(s) | 67 | 1 | killed |
| `u145.M4_states_carried_only` | `src/cratekit/intake/account_playlists.py` | user | 2 file(s) | 64 | 8 | killed |
| `u212.N5_claim_plain` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 59 | 1 | killed |
| `u267.M11_rotation_opens_its_own` | `src/cratekit/intake/rotate_cli.py` | user | 2 file(s) | 56 | 4 | killed |
| `u270.J8_stop_is_the_signal` | `src/cratekit/core/jobs.py` | user | 2 file(s) | 52 | 1 | killed |
| `u120.B2_first_mention_wins` | `src/cratekit/intake/account_playlists.py` | user | 2 file(s) | 50 | 2 | killed |
| `u175.F3_analyze_asked` | `src/cratekit/intake/refill.py` | user | 2 file(s) | 50 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R25_digest_drops_the_folder` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 50 | 2 | killed |
| `u207.I1_missing_never_screens` | `src/cratekit/intake/missing_cli.py` | user | 2 file(s) | 48 | 1 | killed |
| `r685-a.V2_landing_preflight_reads_the_shipped_text` | `src/cratekit/intake/landing.py` | user | 2 file(s) | 45 | 2 | killed |
| `u221.R20_landing_records_no_hold` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 38 | 1 | killed |
| `u197.M6_config_default` | `src/cratekit/core/config.py` | user | 2 file(s) | 36 | 1 | killed |
| `u25.G15_barren_watch` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `u276.K11_run_binding_names_whole` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 24 | 2 | killed |
| `u117-operator.D13_config_validation` | `src/cratekit/core/config.py` | maintainer | 1 file(s) | 22 | 1 | killed |
| `u37-author-light.G4_staging` | `src/cratekit/intake/ingest.py` | user | 1 file(s) | 10 | 1 | killed |
| `u149.T21_landing_paired_again` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 6 | 1 | killed |
| `u135.A3_found_vs_made_collapsed` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 2 | 2 | killed |
| `u135.A1_removed_namesake_written_into` | `src/cratekit/intake/native.py` | user | 1 file(s) | 1 | 1 | killed |
| `u135.A4_live_inbox_named_always_false` | `src/cratekit/intake/native.py` | user | 1 file(s) | 1 | 1 | killed |
| `u135.A7_leftover_joins_numbered_twin` | `src/cratekit/intake/native.py` | user | 1 file(s) | 1 | 1 | killed |
| `u135.A8_job_key_not_stamped` | `src/cratekit/intake/native.py` | user | 1 file(s) | 1 | 1 | killed |
| `u135.A12_inspiration_join_broken` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 1 | 1 | killed |

## Zero rows and what they owe

- `u119.G16_read_back_blind_to_leftovers` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `u270.J6_missing_outcome_fails`

_batch_outcomes: read an item the handler gave no outcome for as done

- File: `src/cratekit/core/jobs.py`
- Source: `u270.json`, row `J6_missing_outcome_fails`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs_batch.py`, `tests/test_outbound_workers.py`
- Collected: 145 against a baseline of 145
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs_batch.py::test_an_item_the_handler_answered_nothing_for_is_failed_not_done`

Old text:

```
            outcomes[item.item_id] = _no_outcome(item)
```

New text:

```
            outcomes[item.item_id] = None
```

### `u293.S3_sync_land_holds`

sync_land: a pass by hand takes no staging lock

- File: `src/cratekit/cli/sync_land.py`
- Source: `u293.json`, row `S3_sync_land_holds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_night.py`, `tests/test_sync_land.py`, `tests/test_sync_land_beside.py`
- Collected: 144 against a baseline of 144
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_night.py::test_a_pass_by_hand_refuses_while_the_night_holds_the_lock`

Old text:

```
    with staging_lock.held("crate sync land", run_id=ctx.run.run_id):
```

New text:

```
    if True:
```

### `r1255.S8_clause_listing_wording`

unread_clause: word an unlisted log as the count of entries, so a gate sends a person to a damaged file

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S8_clause_listing_wording`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_intake_shelve.py`, `tests/test_tree_registry.py`
- Collected: 142 against a baseline of 142
- Kills: 9 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_every_destructive_session_is_refused_at_its_gate`
  - `tests/test_session_log_unlisted.py::test_restore_list_refuses_a_log_it_cannot_list_rather_than_list_nothing`
  - `tests/test_session_log_unlisted.py::test_restore_run_refuses_naming_the_listing_not_an_unrecorded_session`
  - `tests/test_session_log_unlisted.py::test_the_batch_name_rule_refuses_rather_than_call_a_name_free`
  - `tests/test_session_log_unlisted.py::test_the_clause_names_the_listing_and_not_an_entry`
  - `tests/test_session_log_unlisted.py::test_the_native_landing_lookups_refuse_a_log_they_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_reporting_reader_refuses_a_log_it_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_tree_registry_refuses_rather_than_read_no_open_run`
  - `tests/test_session_log_unlisted.py::test_the_unresolved_session_gate_refuses_over_a_log_it_cannot_list`

Old text:

```
        return "the session log exists and cannot be listed by this account"
```

New text:

```
        return "the session log holds 1 entry this build cannot read"
```

### `u270.J1_claim_batch_size_floor`

claim_batch: accept a batch of zero items, so a size the binding never checks claims nothing and the job reads as finished

- File: `src/cratekit/core/jobs.py`
- Source: `u270.json`, row `J1_claim_batch_size_floor`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_jobs_batch.py`, `tests/test_jobs.py`, `tests/test_handlers.py`
- Collected: 134 against a baseline of 134
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs_batch.py::test_claim_batch_refuses_a_batch_of_no_items[0]`

Old text:

```
    if limit < 1:
        raise refuse(
            "internal-error",
            f"a batch of {limit} items was asked for; a batch takes at least one",
```

New text:

```
    if limit < 0:
        raise refuse(
            "internal-error",
            f"a batch of {limit} items was asked for; a batch takes at least one",
```

### `r669-b.B1_composer_not_sanitized`

G14's composite: drop the one sanitizer, the composer's, now that the copy in _artist is gone, so a slash in a credit reaches the filename

- File: `src/cratekit/core/naming.py`
- Source: `r669-b.json`, row `B1_composer_not_sanitized`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/test_acquire_fallback_fetch.py`
- Collected: 133 against a baseline of 133
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_the_stem_is_the_rows_and_carries_no_path_separator`
  - `tests/test_naming_apply_cli.py::test_a_slash_in_a_tag_takes_the_body_form_of_a_segment`

Old text:

```
        part for part in (sanitize_segment(artist or ""), sanitize_segment(title or "")) if part
```

New text:

```
        part for part in (artist or "", title or "") if part
```

### `u114.M18_narrow_called`

The row engine never calls the narrow step, so no file is written and every row is

- File: `src/cratekit/tagging/rows.py`
- Source: `u114.json`, row `M18_narrow_called`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`, `tests/test_tag_rows.py`
- Collected: 131 against a baseline of 131
- Kills: 21 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_commit_that_refuses_leaves_the_row_as_it_was_and_claims_no_commit`
  - `tests/test_tag_rows.py::test_a_file_on_a_volume_that_is_not_mounted_is_counted_and_the_run_does_not_fail`
  - `tests/test_tag_rows.py::test_a_held_row_survives_the_write_and_the_apply_must_name_it_again`
  - `tests/test_tag_rows.py::test_a_mistyped_identifier_is_shown_at_the_gate_and_warned_about`
  - `tests/test_tag_rows.py::test_a_person_reads_the_counts_and_the_pairs_at_the_gate_and_after_the_write`
  - `tests/test_tag_rows.py::test_a_restore_out_of_band_is_marked_before_this_write_replaces_the_evidence`
  - `tests/test_tag_rows.py::test_a_second_apply_plans_nothing_and_writes_nothing`
  - `tests/test_tag_rows.py::test_a_second_run_after_a_clean_one_asks_and_is_a_no_op`
  - `tests/test_tag_rows.py::test_a_word_the_library_has_no_row_for_names_the_act_on_a_run_that_wrote`
  - `tests/test_tag_rows.py::test_an_unregistered_policy_would_write_nothing_and_the_apply_registers_it`
  - `tests/test_tag_rows.py::test_planned_written_and_read_back_through_the_two_acts`
  - `tests/test_tag_rows.py::test_the_apply_is_a_recorded_session_a_restore_can_undo`
  - `tests/test_tag_rows.py::test_the_apply_writes_the_genre_and_no_other_column_of_any_row`
  - `tests/test_tag_rows.py::test_the_genre_report_stops_naming_the_old_word_after_the_run`
  - `tests/test_tag_rows.py::test_with_no_regression_the_write_marks_nothing_and_records_where_it_left_off`
  - ... and 6 more, see the JSON sidecar

Old text:

```
        if narrow is not None:
            plan = narrow(plan)
```

New text:

```
        if narrow is None:
            plan = narrow(plan)
```

### `r1255.T1_tree_registry_clause`

tree_registry._whole_log: word the refusal with the old count, not the clause

- File: `src/cratekit/core/tree_registry.py`
- Source: `r1255.json`, row `T1_tree_registry_clause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_tree_registry.py`, `tests/test_cutover_precheck.py`
- Collected: 125 against a baseline of 125
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_an_unreadable_record_keeps_its_own_refusal`
  - `tests/test_session_log_unlisted.py::test_the_tree_registry_refuses_rather_than_read_no_open_run`

Old text:

```
            f"{session.unread_clause(unreadable, cfg)}, so {so}; refusing rather than "
```

New text:

```
            f"the session log holds {len(unreadable)} entries this build cannot read, so {so}; refusing rather than "
```

### `u56-catalogue-searcher-and-tag-workers.R26_retag_queues_no_items`

The zero item rule broken on the second verb, over work somebody explicitly confirmed

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R26_retag_queues_no_items`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 122 against a baseline of 122
- Kills: 20 (killed)
- Killed:
  - `tests/test_queued_resume_contract.py::test_the_resume_the_job_driver_spawns_can_actually_proceed[tag.retag]`
  - `tests/test_tag_workers.py::test_a_corrected_retag_ends_by_naming_the_reload_the_stale_row_needs`
  - `tests/test_tag_workers.py::test_a_file_gone_at_drive_time_is_refused_rather_than_reported_done`
  - `tests/test_tag_workers.py::test_a_genre_made_blank_between_the_confirm_and_the_drive_is_left_to_its_owner`
  - `tests/test_tag_workers.py::test_a_genre_made_specific_between_the_confirm_and_the_drive_is_not_rewritten`
  - `tests/test_tag_workers.py::test_a_half_corrected_retag_carries_the_reload_on_its_refusal`
  - `tests/test_tag_workers.py::test_a_parked_retag_keeps_both_the_block_and_the_reload`
  - `tests/test_tag_workers.py::test_a_recorded_acceptance_is_used_and_the_searcher_is_never_asked`
  - `tests/test_tag_workers.py::test_a_resume_after_a_partial_run_meets_its_gate_rather_than_going_stale`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_is_named_in_the_human_answer`
  - `tests/test_tag_workers.py::test_a_retag_parses_the_active_taxonomy_once_however_many_files_it_corrects`
  - `tests/test_tag_workers.py::test_a_retag_that_corrected_nothing_does_not_send_a_person_to_rekordbox`
  - `tests/test_tag_workers.py::test_a_retag_whose_only_file_will_not_take_its_genre_names_no_reload`
  - `tests/test_tag_workers.py::test_a_retried_retag_drives_only_the_item_that_failed`
  - ... and 5 more, see the JSON sidecar

Old text:

```
            item_ids=tuple(str(row["path"]) for row in plan["items"]),
```

New text:

```
            item_ids=(),
```

### `r1634.M16_worker_drops_how`

label-sweep-incomplete: the worker's message no longer says how the release was asked

- File: `src/cratekit/label/cli.py`
- Source: `r1634.json`, row `M16_worker_drops_how`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_workers.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_though_every_held_line_names_the_label`

Old text:

```
            f"{one.how()}: {one.said()}."
```

New text:

```
            f": {one.said()}."
```

### `u242.M21_mark_cli_already_marked_by_title`

sync mark: decide already marked by the title alone, so a taken playlist is planned again

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u242.json`, row `M21_mark_cli_already_marked_by_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_u242_taken.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_partial_failure_names_what_was_marked`

Old text:

```
        elif playlists.is_taken(identity, entry.name, sweep.taken):
```

New text:

```
        elif playlists.is_swept_name(entry.name):
```

### `u242.M9_take_overwrites_a_held_entry`

take: replace an entry still held, so a second taker's stamp replaces the first and the migration is not idempotent

- File: `src/cratekit/sync/mark_record.py`
- Source: `u242.json`, row `M9_take_overwrites_a_held_entry`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_sync_mark.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_take_is_idempotent_and_a_released_entry_is_taken_afresh`

Old text:

```
                elif not taken[at].held:
```

New text:

```
                elif True:
```

### `u144-c.C9_parent_of_named`

Sample of an existing U121 guard, now shared: take a live playlist of the name under any parent

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u144-c.json`, row `C9_parent_of_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`, `tests/test_organize_inspiration.py`
- Collected: 112 against a baseline of 112
- Kills: 12 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_file_two_collection_rows_claim_is_left_out_rather_than_one_row_picked`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_creates_the_declared_folder_at_the_root_when_the_library_lacks_it`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order`
  - `tests/test_set_inspiration_playlist.py::test_a_recorded_playlist_that_was_removed_is_not_added_to_and_a_live_one_is_made`
  - `tests/test_set_inspiration_playlist.py::test_a_row_neither_owned_nor_landed_is_counted_and_named_and_not_added`
  - `tests/test_set_inspiration_playlist.py::test_a_track_accepted_at_review_as_a_library_file_joins_the_playlist_at_a_landing`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_follows_the_live_inspiration_row_on_the_disposable_database`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_refuses_a_playlist_a_legacy_archive_prefixed`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_renames_a_set_the_landing_archived_and_it_stays_taken`
  - `tests/test_set_inspiration_playlist.py::test_members_keep_the_sets_order_when_it_is_not_alphabetical`
  - `tests/test_set_inspiration_playlist.py::test_posted_on_a_frozen_job_names_another_day_and_the_frozen_name_wins_with_a_warning`
  - `tests/test_set_inspiration_playlist.py::test_two_landings_of_one_set_on_two_days_make_one_playlist`

Old text:

```
        if str(getattr(row, "ParentID", "") or "") == parent_id:
```

New text:

```
        if True:
```

### `u319.M9_warning_drops_the_short_path`

land_cli: the awaiting analysis warning names one path again

- File: `src/cratekit/intake/land_cli.py`
- Source: `u319.json`, row `M9_warning_drops_the_short_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`, `tests/test_intake_land_native.py`, `tests/test_inbox_analyzed.py`
- Collected: 106 against a baseline of 106
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_dyn_native.py::test_the_warning_names_both_selections_and_counts_each`

Old text:

```
                f"for analysis, and {selections}; {AUTO_ANALYSIS_STEP}; then "
```

New text:

```
                f"for analysis, and {selections}; then "
```

### `u181.C3_unscored_flag_ignored`

analyze vocals: ignore --unscored, so the whole folder is queued

- File: `src/cratekit/vocals/cli.py`
- Source: `u181.json`, row `C3_unscored_flag_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`, `tests/test_sync_land.py`
- Collected: 105 against a baseline of 105
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_land.py::test_the_analyze_step_rescores_after_analyze_run_and_before_the_restamp`
  - `tests/test_vocals_cli.py::test_the_tails_rescore_scores_a_headed_file_with_no_score_and_leaves_a_scored_one`
  - `tests/test_vocals_cli.py::test_unscored_over_a_folder_whose_headed_files_all_carry_a_score_queues_nothing`
  - `tests/test_vocals_cli.py::test_unscored_queues_a_headed_file_with_no_score_and_leaves_the_rest_alone`

Old text:

```
    unscored = bool(getattr(ctx.args, "unscored", False))
```

New text:

```
    unscored = False
```

### `u113-b.B2_batch_keeps_claimed`

The batch playlist in the intake file holds the claimed files too

- File: `src/cratekit/intake/ingest.py`
- Source: `u113-b.json`, row `B2_batch_keeps_claimed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_names.py`
- Collected: 105 against a baseline of 105
- Kills: 10 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists.py::test_a_name_an_unimported_intake_file_holds_is_not_given_again`
  - `tests/test_intake_land_account_playlists.py::test_a_name_at_the_playlist_root_is_not_given_since_an_import_lands_there`
  - `tests/test_intake_land_account_playlists.py::test_a_row_that_only_resembles_a_file_does_not_claim_it`
  - `tests/test_intake_land_account_playlists.py::test_a_track_both_playlists_brought_in_is_a_member_of_both`
  - `tests/test_intake_land_account_playlists.py::test_a_track_neither_owned_nor_brought_is_named_in_the_warnings`
  - `tests/test_intake_land_account_playlists.py::test_an_account_playlist_whose_dated_name_is_the_batchs_takes_two`
  - `tests/test_intake_land_account_playlists.py::test_an_export_entry_on_another_machine_is_no_owned_row`
  - `tests/test_intake_land_account_playlists.py::test_an_owned_track_whose_row_the_export_does_not_hold_is_warned`
  - `tests/test_intake_land_account_playlists.py::test_two_swept_playlists_land_as_two_inbox_playlists_under_their_exact_names`

Old text:

```
    rest = [item.track_id for item in placed if item.path not in claimed]
```

New text:

```
    rest = [item.track_id for item in placed]
```

### `u179.P1_shared_preflight`

preflight: drop the rekordbox check, so sync bandcamp plans and fetches with rekordbox open

- File: `src/cratekit/cli/sync_land.py`
- Source: `u179.json`, row `P1_shared_preflight`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_land.py`
- Collected: 104 against a baseline of 104
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_rekordbox_running_refuses_before_the_plan`
  - `tests/test_sync_land.py::test_a_continued_pass_refused_while_rekordbox_runs_names_the_way_back`
  - `tests/test_sync_land.py::test_rekordbox_running_refuses_before_any_write`

Old text:

```
    rb_writer.assert_rekordbox_closed(verb)
```

New text:

```
    pass
```

### `r746-b.N8_unsupported_file_moved_anyway`

apply_native: a file the database has no type for is not refused per file and moves

- File: `src/cratekit/intake/landing.py`
- Source: `r746-b.json`, row `N8_unsupported_file_moved_anyway`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_landing.py`
- Collected: 103 against a baseline of 103
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_suffix_the_database_has_no_type_for_is_left_in_staging_and_the_batch_lands`

Old text:

```
        if row.action == native.UNSUPPORTED
    }
```

New text:

```
        if False
    }
```

### `u140.B6_mark_refusal_dropped`

plan_rename retitles a playlist the archive marked

- File: `src/cratekit/export/set_cli.py`
- Source: `u140.json`, row `B6_mark_refusal_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_playlist_the_archive_marked_is_refused_rather_than_retitled`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_refuses_a_playlist_a_legacy_archive_prefixed`

Old text:

```
        if mark is not None:
            raise _rename_unresolved(

```

New text:

```
        if False:
            raise _rename_unresolved(

```

### `u142.S12_undeclared_reads_as_empty`

inspiration_names: answer an empty set when no INSPIRATION folder is declared, so the wait says no playlist rather than no folder

- File: `src/cratekit/export/set_cli.py`
- Source: `u142.json`, row `S12_undeclared_reads_as_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 100 against a baseline of 100
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_taxonomy_with_no_inspiration_folder_waits_and_says_why`

Old text:

```
    if declared.inspiration is None:
        return None
    return frozenset(
```

New text:

```
    if declared.inspiration is None:
        return frozenset()
    return frozenset(
```

### `r722.A1_gate_drops_tally`

The approval gate's facts omit the reading tally

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `r722.json`, row `A1_gate_drops_tally`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adopt_workers.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_the_approval_gate_shows_the_reading_tally`

Old text:

```
            "energy": document["energy"],

```

New text:

```
(empty)
```

### `u175.R1_account_ids_unrecorded`

rotate._named_ids: read no account playlist off a native landing record, so a dated playlist is no batch and is neither rotated nor mirrored

- File: `src/cratekit/intake/rotate.py`
- Source: `u175.json`, row `R1_account_ids_unrecorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`
- Collected: 98 against a baseline of 98
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together`
  - `tests/test_intake_land_account_playlists_native.py::test_the_rotation_ages_an_account_playlist_by_its_landing_date`
  - `tests/test_organize_mirror_inbox.py::test_a_passs_dated_account_playlist_is_mirrored_beside_its_batch_under_its_dated_name`

Old text:

```
    accounts = record.detail.get(native.INBOX_PLAYLISTS_KEY)
    if isinstance(accounts, list):
```

New text:

```
    accounts = None
    if isinstance(accounts, list):
```

### `u261.H6_app_not_asked_again`

session_for: hand a reuse the held absence of an app client, so app values recorded or lost since the open are not seen and no lost value is noted

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `H6_app_not_asked_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_catalogue_app.py`
- Collected: 96 against a baseline of 96
- Kills: 3 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_open_account_and_open_catalogue_hand_the_app_client_on`
  - `tests/test_provider_session_hold.py::test_a_lost_app_value_is_noted_on_every_resolve_that_falls_back`
  - `tests/test_provider_session_hold.py::test_an_app_recorded_after_the_open_is_picked_up_by_the_next_resolve`

Old text:

```
            if current.app is None:
```

New text:

```
            if False:
```

### `u288.M15_append_past_highest`

add_memberships: keep the binding's count plus one, so an append after a removal lands on a live row's position

- File: `src/cratekit/core/rb_writer.py`
- Source: `u288.json`, row `M15_append_past_highest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`, `tests/test_inbox_refill.py`
- Collected: 96 against a baseline of 96
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_track_added_after_a_removal_goes_past_the_highest_position`
  - `tests/test_sync_removed.py::test_two_appends_after_a_removal_each_take_the_next_position`

Old text:

```
        if added is not None and number <= highest:
```

New text:

```
        if False:
```

### `r770-a.A2_unreachable_root_is_read_anyway`

intake_medium: read the taxonomy and the registry of a library root that is not there

- File: `src/cratekit/intake/ingest.py`
- Source: `r770-a.json`, row `A2_unreachable_root_is_read_anyway`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`, `tests/test_intake_land.py`
- Collected: 95 against a baseline of 95
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_recorded_abort_is_honored_over_a_library_that_went_missing`
  - `tests/test_intake_land.py::test_an_unmounted_library_is_named_as_the_library_and_not_as_the_export`
  - `tests/test_intake_writers_native.py::test_an_unreachable_library_root_decides_nothing`

Old text:

```
    if not Path(cfg.library.root).is_dir():
```

New text:

```
    if False:
```

### `r235-b.M25_adoption_refusal_names_no_verb`

the adoption refusal on an uncut library is re-raised as it came, with no step

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `r235-b.json`, row `M25_adoption_refusal_names_no_verb`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`, `tests/test_adopt_workers.py`
- Collected: 94 against a baseline of 94
- Kills: 2 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_an_uncut_library_refuses_adoption_and_names_the_cutover_verb`
  - `tests/test_cutover_cli.py::test_the_steps_the_refused_adoption_names_are_the_steps_that_work`

Old text:

```
        named = _naming_the_cutover(exc)
        if named is None:
```

New text:

```
        named = None
        if named is None:
```

### `u267.M4_handle_opens_every_time`

SharedRead.handle: open again on every call, keeping the last, so the report pays an open per reader and leaks the rest

- File: `src/cratekit/core/rb_writer.py`
- Source: `u267.json`, row `M4_handle_opens_every_time`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_organize_inspiration.py`, `tests/test_organize_mirror_edits_u204.py`
- Collected: 92 against a baseline of 92
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_report_reads_inspiration_twice_through_one_handle_and_locks_nothing_meanwhile`
  - `tests/test_organize_one_read.py::test_a_failure_nobody_expected_still_closes_the_handle`
  - `tests/test_organize_one_read.py::test_a_shared_read_opens_at_its_first_read_and_once`
  - `tests/test_organize_one_read.py::test_a_step_that_refuses_after_the_open_leaves_no_handle_open`
  - `tests/test_organize_one_read.py::test_the_report_opens_the_database_once_and_closes_it_once`
  - `tests/test_organize_one_read.py::test_the_sets_step_reads_inspiration_through_the_one_handle`

Old text:

```
        if self._db is None:
            self._db = open_db(
```

New text:

```
        if True:
            self._db = open_db(
```

### `u319.M8_ok_on_any_field`

land_cli: the short path's OK offered whatever the dialog shows

- File: `src/cratekit/intake/land_cli.py`
- Source: `u319.json`, row `M8_ok_on_any_field`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_drift.py`, `tests/test_intake_land_dyn_native.py`, `tests/test_rekordbox_visit_skill.py`
- Collected: 92 against a baseline of 92
- Kills: 2 (killed)
- Killed:
  - `tests/test_drift.py::test_the_auto_analysis_step_cancels_on_any_other_field_and_leaves_dyn_to_dynamic`
  - `tests/test_drift.py::test_the_sync_stop_offers_the_auto_analysis_path_after_the_selections_it_stands_in_for`

Old text:

```
    "on its Auto Analysis dialog only when it shows every one of those Normal "
```

New text:

```
    "on its Auto Analysis dialog whatever it shows of those Normal "
```

### `u242.M8_twins_reads_the_title_alone`

twins backfill: read a downloaded custom playlist by its prefix alone, so a stripped one gets no twin

- File: `src/cratekit/sync/twins.py`
- Source: `u242.json`, row `M8_twins_reads_the_title_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_sync_twins.py`
- Collected: 92 against a baseline of 92
- Kills: 1 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_twins_reads_a_stripped_custom_playlist_as_downloaded`

Old text:

```
            if not is_taken(playlist_id, name, held):
```

New text:

```
            if not name.startswith("DOWNLOADED "):
```

### `u150.F2_record_provider`

native._record_commit: write no provider tracks on the landing's record

- File: `src/cratekit/intake/native.py`
- Source: `u150.json`, row `F2_record_provider`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`, `tests/test_organize_mirror_inbox.py`
- Collected: 90 against a baseline of 90
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_the_record_names_each_landed_rows_provider_track_for_the_account_mirror`

Old text:

```
        record.detail[label_filing.PROVIDER_KEY] = dict(labels_written.provider)
```

New text:

```
        pass
```

### `u267.M12_inspiration_set_folder_write_guard`

set_cli._inspiration_folder: drop the refusal of a shared read handed to an opener asked to write

- File: `src/cratekit/export/set_cli.py`
- Source: `u267.json`, row `M12_inspiration_set_folder_write_guard`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 88 against a baseline of 88
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_the_inspiration_opener_refuses_to_write_through_a_shared_read`

Old text:

```
    if one_read is not None and not read_only:
```

New text:

```
    if False:
```

### `u156.L25_shared_rule_near_match`

match_label_rows: file a row the batch holds only something close to, on both media

- File: `src/cratekit/intake/landing.py`
- Source: `u156.json`, row `L25_shared_rule_near_match`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_intake_land_labels_native.py`
- Collected: 85 against a baseline of 85
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_a_landed_file_at_another_version_is_a_question_and_is_not_filed`

Old text:

```
        if found.state is match.MatchState.NEEDS_REVIEW:
```

New text:

```
        if False:
```

### `u135.A14_set_order_reverses`

INBOX set-order walk appends members in reverse position order

- File: `src/cratekit/intake/native.py`
- Source: `u135.json`, row `A14_set_order_reverses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`
- Collected: 85 against a baseline of 85
- Kills: 3 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order`
  - `tests/test_u135_set_inbox_join.py::test_a_set_landed_once_keeps_one_inbox_playlist_named_for_the_set`
  - `tests/test_u135_set_inbox_join.py::test_one_landing_of_a_set_files_its_inbox_playlist_in_set_order_not_name_order`

Old text:

```
                for member in plan.set_playlist.members:

```

New text:

```
                for member in reversed(plan.set_playlist.members):

```

### `u242.M7_inspiration_reads_the_title_alone`

INSPIRATION step: read a set in a sets folder by its prefix alone, so a stripped set is shown unprefixed and never backfilled

- File: `src/cratekit/organize/inspiration.py`
- Source: `u242.json`, row `M7_inspiration_reads_the_title_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_organize_inspiration.py`
- Collected: 85 against a baseline of 85
- Kills: 1 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_the_inspiration_set_rule_reads_a_stripped_set_as_the_prefixed_one`

Old text:

```
            stripped = untaken_name(name) if is_taken(playlist_id, name, held) else ""
```

New text:

```
            stripped = untaken_name(name) if name.startswith("DOWNLOADED ") else ""
```

### `u221.R15_mark_drops_the_hold`

PairStore.mark: record no hold on a new pair, so a backfilled twin falls to the time rule

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u221.json`, row `R15_mark_drops_the_hold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 84 against a baseline of 84
- Kills: 14 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_backfilled_pair_merges_both_ways_and_queues_the_added_track_once`
  - `tests/test_sync_twins_hold.py::test_a_held_track_whose_linked_row_left_the_library_is_still_counted_and_released`
  - `tests/test_sync_twins_hold.py::test_a_landing_twin_records_an_empty_hold`
  - `tests/test_sync_twins_hold.py::test_a_name_that_is_no_twin_is_refused_and_nothing_is_planned`
  - `tests/test_sync_twins_hold.py::test_a_second_twin_stays_held_when_the_first_is_released`
  - `tests/test_sync_twins_hold.py::test_a_track_added_later_on_the_account_is_queued_and_the_held_stay_held`
  - `tests/test_sync_twins_hold.py::test_a_twin_paired_again_since_the_plan_is_left_held`
  - `tests/test_sync_twins_hold.py::test_a_twin_with_three_missing_tracks_queues_none_and_names_three_on_hold`
  - `tests/test_sync_twins_hold.py::test_an_abort_lets_nothing_go`
  - `tests/test_sync_twins_hold.py::test_release_hold_passes_over_a_pair_that_is_no_twin_and_one_holding_nothing`
  - `tests/test_sync_twins_hold.py::test_release_needs_names_or_all_and_not_both[args0]`
  - `tests/test_sync_twins_hold.py::test_release_needs_names_or_all_and_not_both[args1]`
  - `tests/test_sync_twins_hold.py::test_releasing_the_twin_queues_its_three_at_the_next_sync`
  - `tests/test_sync_twins_hold.py::test_the_hold_survives_a_recorded_snapshot_and_a_mark_of_the_same_pair`

Old text:

```
                on_hold=(
                    None
                    if on_hold is None
                    else MappingProxyType({str(k): str(v) for k, v in on_hold.items() if k})
                ),
```

New text:

```
                on_hold=None,
```

### `r746-a.G4_read_back_walks_session_new_only`

assert_created_rows_are_gridless: the R-760 blind spot put back, a flushed creation is never read from SQL

- File: `src/cratekit/core/rb_writer.py`
- Source: `r746-a.json`, row `G4_read_back_walks_session_new_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_guard_completeness.py`, `tests/test_intake_land_native.py`
- Collected: 81 against a baseline of 81
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_an_analysis_product_row_for_the_new_row_is_refused_from_sql_before_the_commit`
  - `tests/test_write_guard_completeness.py::test_a_flushed_creation_is_read_back_from_both_sources`

Old text:

```
    instances = {**_registry_created_instances(db), **pending}
```

New text:

```
    instances = {**pending}
```

### `r746-a.G6_analysis_tables_not_checked`

assert_created_rows_are_gridless: no cue, mixer or file row is looked for on the new content row

- File: `src/cratekit/core/rb_writer.py`
- Source: `r746-a.json`, row `G6_analysis_tables_not_checked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_write_guard_completeness.py`
- Collected: 81 against a baseline of 81
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_an_analysis_product_row_for_the_new_row_is_refused_from_sql_before_the_commit`

Old text:

```
        if table == CONTENT_TABLE and len(keys) == 1:
```

New text:

```
        if False:
```

### `u221.R19_short_listing_records_its_misses`

pair_backfilled: record a short listing's misses as its hold, so a track the account withheld and serves later is queued with no choice

- File: `src/cratekit/sync/twins.py`
- Source: `u221.json`, row `R19_short_listing_records_its_misses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`
- Collected: 78 against a baseline of 78
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_a_short_listings_twin_records_no_hold_and_holds_a_track_served_later`

Old text:

```
                {miss.remote_id: miss.held_as() for miss in one.misses} if one.whole else None
```

New text:

```
                {miss.remote_id: miss.held_as() for miss in one.misses}
```

### `u219.K3_accept_declined`

rebuild accept: an abort records the disposition anyway

- File: `src/cratekit/cli/rebuild.py`
- Source: `u219.json`, row `K3_accept_declined`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`, `tests/test_resort_scope.py`
- Collected: 77 against a baseline of 77
- Kills: 1 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_an_aborted_acceptance_leaves_the_inbox_refusing`

Old text:

```
    if option != "accept":
```

New text:

```
    if option == "never":
```

### `u113-b.B5_export_clash_unasked`

A name the export came to hold since it was chosen is not refused before the moves

- File: `src/cratekit/intake/landing.py`
- Source: `u113-b.json`, row `B5_export_clash_unasked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_landing.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_name_the_export_came_to_hold_after_the_gate_is_refused_and_moves_nothing`

Old text:

```
    clash = sorted(set(names) & set(held))
```

New text:

```
    clash: list[str] = []
```

### `u185.G5_reading_at_open`

open_db: keep no reading of the subtree as the handle opens

- File: `src/cratekit/core/rb_writer.py`
- Source: `u185.json`, row `G5_reading_at_open`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`, `tests/test_rb_writer_db.py`
- Collected: 75 against a baseline of 75
- Kills: 20 (killed)
- Killed:
  - `tests/test_foreign_tree.py::test_a_handle_with_no_reading_at_open_refuses_rather_than_assuming_nothing_is_there`
  - `tests/test_foreign_tree.py::test_a_membership_added_to_a_pushed_playlist_is_refused`
  - `tests/test_foreign_tree.py::test_a_playlist_made_inside_the_folder_is_refused`
  - `tests/test_foreign_tree.py::test_a_playlist_of_ones_own_moved_into_the_folder_is_refused`
  - `tests/test_foreign_tree.py::test_a_position_named_at_the_top_moves_the_folder_and_is_refused`
  - `tests/test_foreign_tree.py::test_a_push_that_lands_while_a_handle_is_open_refuses_that_handles_commit`
  - `tests/test_foreign_tree.py::test_a_pushed_membership_rewritten_to_another_owner_is_refused`
  - `tests/test_foreign_tree.py::test_a_pushed_playlist_moved_out_of_the_folder_is_refused`
  - `tests/test_foreign_tree.py::test_a_second_folder_of_the_name_at_the_top_is_refused`
  - `tests/test_foreign_tree.py::test_a_write_beside_the_folder_commits_and_leaves_every_row_the_push_wrote`
  - `tests/test_foreign_tree.py::test_raw_sql_into_the_folder_is_seen_by_the_reading_again_from_sql`
  - `tests/test_foreign_tree.py::test_the_reading_at_open_names_the_push_and_not_a_namesake_below_the_top`
  - `tests/test_rb_writer_db.py::test_a_playlist_creation_commits_because_the_table_is_whitelisted`
  - `tests/test_rb_writer_db.py::test_a_registered_column_write_commits_and_persists`
  - `tests/test_rb_writer_db.py::test_a_registration_widens_the_gate_by_exactly_its_own_fields`
  - ... and 5 more, see the JSON sidecar

Old text:

```
    foreign_tree.remember(db)
    return db
```

New text:

```
    return db
```

### `u130-c.C5_no_renumber`

Leave rekordbox's order as the adds and removals left it

- File: `src/cratekit/write/playlist_pair.py`
- Source: `u130-c.json`, row `C5_no_renumber`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 75 against a baseline of 75
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_track_added_on_the_account_only_lands_in_rekordbox_in_place`
  - `tests/test_sync_pair.py::test_the_first_sync_marks_the_pair_and_adds_only`
  - `tests/test_sync_pair.py::test_when_both_sides_reorder_the_account_order_wins`

Old text:

```
            moved = renumber(db, change.playlist_id, change.order)
```

New text:

```
            moved = 0
```

### `u243.L7_kept_read_judged_blind`

KeptReads._is_fresh: a kept read without the tracks' words is reused and judged without them

- File: `src/cratekit/label/kept_reads.py`
- Source: `u243.json`, row `L7_kept_read_judged_blind`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tombstoned.py`, `tests/test_label_playlists_kept.py`
- Collected: 74 against a baseline of 74
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_tombstoned.py::test_a_kept_read_missing_any_track_word_is_read_again[no-artist]`
  - `tests/test_label_tombstoned.py::test_a_kept_read_missing_any_track_word_is_read_again[no-title]`
  - `tests/test_label_tombstoned.py::test_a_kept_read_missing_any_track_word_is_read_again[one-track-unnamed]`
  - `tests/test_label_tombstoned.py::test_a_kept_read_written_without_the_words_is_read_again`

Old text:

```
        return timedelta(0) <= age < KEPT_FOR and kept.named
```

New text:

```
        return timedelta(0) <= age < KEPT_FOR
```

### `u166.R2_rotate_reserved`

_classify: let the rotation take Analyze for a batch

- File: `src/cratekit/intake/rotate.py`
- Source: `u166.json`, row `R2_rotate_reserved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_the_rotation_never_takes_analyze_for_a_batch_whatever_a_record_says`

Old text:

```
    if not in_old and name == native.ANALYZE:
```

New text:

```
    if False:
```

### `u130-c.C6_pair_not_vouched`

The account seam refuses a removal from a paired playlist

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u130-c.json`, row `C6_pair_not_vouched`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_account.py`, `tests/test_prune.py`
- Collected: 73 against a baseline of 73
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair_account.py::test_a_move_that_landed_elsewhere_is_left_to_the_settle_reading_with_every_track_kept`
  - `tests/test_sync_pair_account.py::test_a_paired_playlist_takes_a_removal`
  - `tests/test_sync_pair_account.py::test_a_track_held_twice_is_not_moved`
  - `tests/test_sync_pair_account.py::test_an_order_already_standing_sends_nothing`
  - `tests/test_sync_pair_account.py::test_the_order_moves_each_track_to_the_front_and_reads_back`

Old text:

```
            ledger.product_made(self._cfg, identifier) or pairs.paired(self._cfg, identifier)
```

New text:

```
            ledger.product_made(self._cfg, identifier)
```

### `u81-fetch-b.Q5_owned_row_fetched`

Existing guard, moved into missing_rows: a row the library holds is not counted owned and is fetched

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `u81-fetch-b.json`, row `Q5_owned_row_fetched`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_fallback.py`
- Collected: 72 against a baseline of 72
- Kills: 3 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_an_owned_row_is_never_searched`
  - `tests/test_acquire_fallback.py::test_no_binary_is_needed_when_nothing_is_searched`
  - `tests/test_acquire_fallback_fetch.py::test_a_row_the_library_already_holds_is_not_fetched`

Old text:

```
        if one.state is match.MatchState.MATCHED:
            counts["owned"] += 1
```

New text:

```
        if False:
            counts["owned"] += 1
```

### `u247.M8_scan_freezes_its_declaration`

adopt scan handle: judge every row of a job by the declaration its first row read, R-690's open question decided by accident

- File: `src/cratekit/adopt/scan_cli.py`
- Source: `u247.json`, row `M8_scan_freezes_its_declaration`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`, `tests/test_active_taxonomy.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_copy_edited_during_a_scan_judges_every_row_after_the_edit`

Old text:

```
    declared = active_taxonomy.load(cfg)
    (classified,) = scan_engine.scan_rows(
```

New text:

```
    declared = scan_engine.__dict__.setdefault(("u247", job.job_id), active_taxonomy.load(cfg))
    (classified,) = scan_engine.scan_rows(
```

### `u246.S16_inspiration_held_per_element`

assert_read_back (inspiration): build the live set once per planned row again (the shape on main)

- File: `src/cratekit/organize/inspiration.py`
- Source: `u246.json`, row `S16_inspiration_held_per_element`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_comprehension_sets.py`, `tests/test_organize_inspiration.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_comprehension_sets.py::test_no_comprehension_in_the_package_rebuilds_an_invariant_set_per_element`

Old text:

```
        missing = [row for row in one.members if row not in held]
```

New text:

```
        missing = [row for row in one.members if row not in set(live)]
```

### `u119.G16_read_back_blind_to_leftovers`

_read_back: a track still in Favorites after the removals is not a disagreement

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G16_read_back_blind_to_leftovers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if removed_too and live - wanted:
```

New text:

```
        if False:
```

### `u164.W2_preflight_target`

apply_native: check the library against the music folder rather than the chosen folder

- File: `src/cratekit/intake/landing.py`
- Source: `u164.json`, row `W2_preflight_target`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_intake_land_filed.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_filed_folder_on_another_device_is_refused_at_the_move`

Old text:

```
    preflight_native(plan, cfg=cfg, target=target)
```

New text:

```
    preflight_native(plan, cfg=cfg)
```

### `u150.L1_forget_checks_id`

ledger.forget_mirror_playlist: drop the identifier check, so a playlist recorded under the title since is forgotten in its place

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u150.json`, row `L1_forget_checks_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_forgetting_a_mirrored_playlist_drops_only_the_record_of_that_identifier`

Old text:

```
        if not entry or str(entry.get("remote_id") or "") != str(remote_id):
            return
```

New text:

```
        if not entry:
            return
```

### `u145.M4_states_carried_only`

carried_hearts: states=None still reads only the carried states, so an owned row dates nothing

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u145.json`, row `M4_states_carried_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`, `tests/test_favorites_backfill.py`
- Collected: 64 against a baseline of 64
- Kills: 8 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_and_undated_holds_is_not_given_a_month`
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_at_the_root_beside_another_playlist_still_takes_its_month`
  - `tests/test_favorites_backfill.py::test_a_heart_its_job_dated_nowhere_stays_undated_though_the_account_dates_it_now`
  - `tests/test_favorites_backfill.py::test_a_heart_put_back_by_hand_after_a_removal_takes_its_month_and_is_not_taken_back`
  - `tests/test_favorites_backfill.py::test_an_owned_heart_in_a_batch_folder_is_placed_beside_a_downloaded_one`
  - `tests/test_favorites_backfill.py::test_an_owned_heart_the_source_system_filed_is_placed_and_one_with_no_row_is_not`
  - `tests/test_favorites_backfill.py::test_owned_hearts_not_in_all_favorites_are_planned_by_month_and_those_taken_back_are_named`
  - `tests/test_favorites_split.py::test_a_job_row_owned_when_its_job_ran_still_dates_the_member`

Old text:

```
        if states is not None and report.get("state") not in states:
```

New text:

```
        if report.get("state") not in (states or CARRIED_STATES):
```

### `u212.N5_claim_plain`

naming_cli.name_apply: a name taken after the plan is always the plain collision, round one's F8

- File: `src/cratekit/write/naming_cli.py`
- Source: `u212.json`, row `N5_claim_plain`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_second_copy.py`, `tests/test_repair_rows.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_second_copy.py::test_a_copy_that_takes_the_name_after_the_plan_is_said_a_second_copy`

Old text:

```
                why, same = _taken(
                    path, target, fallback=f"{rendered.filename} is already taken in the folder"
                )
```

New text:

```
                why, same = f"{rendered.filename} is already taken in the folder", ""
```

### `u267.M11_rotation_opens_its_own`

rotate_cli.planned: ignore the shared read and open its own handle, a second open in the report

- File: `src/cratekit/intake/rotate_cli.py`
- Source: `u267.json`, row `M11_rotation_opens_its_own`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_inbox_rotate.py`
- Collected: 56 against a baseline of 56
- Kills: 4 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_a_failure_nobody_expected_still_closes_the_handle`
  - `tests/test_organize_one_read.py::test_a_step_that_refuses_after_the_open_leaves_no_handle_open`
  - `tests/test_organize_one_read.py::test_the_report_opens_the_database_once_and_closes_it_once`
  - `tests/test_organize_one_read.py::test_the_sets_step_reads_inspiration_through_the_one_handle`

Old text:

```
    db = (
        one_read.handle()
        if one_read is not None
        else rb_writer.open_db(
```

New text:

```
    one_read = None
    db = (
        one_read.handle()
        if one_read is not None
        else rb_writer.open_db(
```

### `u270.J8_stop_is_the_signal`

drive: hand the batch handler a stop that never answers true, so a signal waits for a whole batch's matching

- File: `src/cratekit/core/jobs.py`
- Source: `u270.json`, row `J8_stop_is_the_signal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs_batch.py`, `tests/test_handlers.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs_batch.py::test_a_batch_answered_under_a_signal_is_released_whole_and_the_job_cancelled`

Old text:

```
                    batch, job, claimed, lambda: interrupt.signalled
```

New text:

```
                    batch, job, claimed, lambda: False
```

### `u120.B2_first_mention_wins`

prefer_dated: a later mention that knows its date does not replace a first that does not

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u120.json`, row `B2_first_mention_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 50 against a baseline of 50
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_two_jobs_carried_is_one_heart_with_the_dated_jobs_date`
  - `tests/test_intake_land_hearts_native.py::test_the_pass_prefers_the_mention_that_knows_its_date`

Old text:

```
    return held is None or (not held.known and row.known)
```

New text:

```
    return held is None
```

### `u175.F3_analyze_asked`

refill.locate: stop excluding the reserved Analyze from the names asked

- File: `src/cratekit/intake/refill.py`
- Source: `u175.json`, row `F3_analyze_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`, `tests/test_inbox_analyzed.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_inbox_refill_never_takes_analyze_for_an_account_playlist_of_that_name`

Old text:

```
        asked = {name, recorded_name} - {"", native.ANALYZE}
```

New text:

```
        asked = {name, recorded_name} - {""}
```

### `u56-catalogue-searcher-and-tag-workers.R25_digest_drops_the_folder`

Two different empty folders digest identically, so a decision recorded against one satisfies the gate for the other

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R25_digest_drops_the_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_the_shell_digests_the_selection_and_the_folder_rather_than_a_constant`
  - `tests/test_genre_retag.py::test_two_different_empty_folders_digest_differently_through_the_pure_function`

Old text:

```
            FOLDER_KEY: folder,
            ITEMS_KEY: [dict(row) for row in items],
```

New text:

```
            ITEMS_KEY: [dict(row) for row in items],
```

### `u207.I1_missing_never_screens`

intake missing: the askable codes are never screened

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u207.json`, row `I1_missing_never_screens`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`, `tests/test_intake_missing_isrc.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_intake_missing_screens_the_codes_it_will_ask_before_asking_any`

Old text:

```
        found.screen_isrcs(askable)

```

New text:

```
(empty)
```

### `r685-a.V2_landing_preflight_reads_the_shipped_text`

The landing's preflight parses the shipped text, so an undeclared catalog tree is not seen

- File: `src/cratekit/intake/landing.py`
- Source: `r685-a.json`, row `V2_landing_preflight_reads_the_shipped_text`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_active_taxonomy.py`, `tests/test_landing_labels.py`
- Collected: 45 against a baseline of 45
- Kills: 2 (killed)
- Killed:
  - `tests/test_active_taxonomy.py::test_no_module_but_the_loader_reads_the_shipped_template`
  - `tests/test_landing_labels.py::test_an_undeclared_catalog_tree_refuses_before_any_file_moves`

Old text:

```
    checked = Checked(registry=tree_registry.read(cfg), declared=active_taxonomy.load(cfg))

```

New text:

```
    checked = Checked(
        registry=tree_registry.read(cfg),
        declared=taxonomy.load_taxonomy(taxonomy.shipped_template_text("default")),
    )

```

### `u221.R20_landing_records_no_hold`

pair_landed: mark a landing's twin with no hold, so it is read by time and its misses are held

- File: `src/cratekit/sync/twins.py`
- Source: `u221.json`, row `R20_landing_records_no_hold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_intake_land_twins.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_a_landing_twin_records_an_empty_hold`

Old text:

```
                one.account_id, one.playlist_id, name=one.account_name, twin=True, on_hold={}
```

New text:

```
                one.account_id, one.playlist_id, name=one.account_name, twin=True, on_hold=None
```

### `u197.M6_config_default`

AcquisitionConfig: default to the retired key, so a fresh configuration names it

- File: `src/cratekit/core/config.py`
- Source: `u197.json`, row `M6_config_default`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_docs_current.py`
- Collected: 36 against a baseline of 36
- Kills: 1 (killed)
- Killed:
  - `tests/test_docs_current.py::test_the_settings_table_is_the_schema`

Old text:

```
    adapter: str = "vendored"
```

New text:

```
    adapter: str = "tidal_dl_ng"
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

### `u276.K11_run_binding_names_whole`

analysis/cli.py: the driver's detector binding names the whole method, so analyze run separates whatever the default says

- File: `src/cratekit/analysis/cli.py`
- Source: `u276.json`, row `K11_run_binding_names_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_key_default.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_key_default.py::test_no_shipped_caller_of_the_detector_names_a_key_method`
  - `tests/test_analysis_key_default.py::test_the_runs_shipped_bindings_name_no_method_so_they_take_the_default[cli.py]`

Old text:

```
            drift_cut=cfg.analysis.drift_cut,
        )
        light.bind_detect(_BOUND_DETECT)
```

New text:

```
            drift_cut=cfg.analysis.drift_cut,
            key=detect.KEY_WHOLE,
        )
        light.bind_detect(_BOUND_DETECT)
```

### `u117-operator.D13_config_validation`

config: accept a zero age

- File: `src/cratekit/core/config.py`
- Source: `u117-operator.json`, row `D13_config_validation`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_dated.py::test_the_age_key_defaults_to_thirty_and_refuses_zero`

Old text:

```
    if age is not None and (not isinstance(age, int) or isinstance(age, bool) or age < 1):
```

New text:

```
    if age is not None and (not isinstance(age, int) or isinstance(age, bool) or age < 0):
```

### `u37-author-light.G4_staging`

Allow inbox of files still under download staging

- File: `src/cratekit/intake/ingest.py`
- Source: `u37-author-light.json`, row `G4_staging`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`
- Collected: 10 against a baseline of 10
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_pipeline.py::test_staging_files_are_refused`

Old text:

```
    if resolved == staging or staging in resolved.parents:
```

New text:

```
    if False and (resolved == staging or staging in resolved.parents):
```

### `u149.T21_landing_paired_again`

plan_landing: plan a twin for an account playlist already paired

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T21_landing_paired_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_twins.py`
- Collected: 6 against a baseline of 6
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_twins.py::test_an_account_playlist_already_paired_gets_no_second_twin`

Old text:

```
    wanted = [(account_id, name) for account_id, name in accounts if account_id not in held]
```

New text:

```
    wanted = list(accounts)
```

### `u135.A3_found_vs_made_collapsed`

The gate screen always says found-or-made when no recorded INBOX playlist is named

- File: `src/cratekit/intake/land_cli.py`
- Source: `u135.json`, row `A3_found_vs_made_collapsed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u135_set_inbox_join.py::test_a_set_landed_once_keeps_one_inbox_playlist_named_for_the_set`, `tests/test_u135_set_inbox_join.py::test_a_hand_made_inbox_playlist_of_the_set_name_is_named_found_not_recorded`
- Collected: 2 against a baseline of 2
- Kills: 2 (killed)
- Killed:
  - `tests/test_u135_set_inbox_join.py::test_a_hand_made_inbox_playlist_of_the_set_name_is_named_found_not_recorded`
  - `tests/test_u135_set_inbox_join.py::test_a_set_landed_once_keeps_one_inbox_playlist_named_for_the_set`

Old text:

```
        if rows.batch_playlist_id:
            facts["inbox"] = (
                f"adds to the playlist an earlier landing of this set made "
                f"(row {rows.batch_playlist_id})"
            )
        elif rows.inbox_found_by_name:
            facts["inbox"] = "found live by name, not recorded"
        else:
            facts["inbox"] = "made"

```

New text:

```
        facts["inbox"] = (
            f"adds to the playlist an earlier landing of this set made "
            f"(row {rows.batch_playlist_id})"
            if rows.batch_playlist_id
            else "found live by its name under INBOX, or made"
        )

```

### `u135.A1_removed_namesake_written_into`

Drop the node_removed skip so a soft-deleted set-named INBOX playlist is written into

- File: `src/cratekit/intake/native.py`
- Source: `u135.json`, row `A1_removed_namesake_written_into`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u135_set_inbox_join.py::test_a_removed_set_named_inbox_playlist_is_not_written_into`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_u135_set_inbox_join.py::test_a_removed_set_named_inbox_playlist_is_not_written_into`

Old text:

```
    for row in list(db.get_playlist(Name=plan.playlist)):
        if rb_writer.is_folder(row) or rb_writer.node_removed(row):
            continue
        if str(getattr(row, "ParentID", "") or "") == parent_id:
            return row
    return db.create_playlist(plan.playlist, parent=anchor)

```

New text:

```
    return rb_writer.ensure_playlist(db, plan.playlist, anchor)

```

### `u135.A4_live_inbox_named_always_false`

Never detect a live set-named INBOX playlist, so a hand-made one reads as made

- File: `src/cratekit/intake/native.py`
- Source: `u135.json`, row `A4_live_inbox_named_always_false`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u135_set_inbox_join.py::test_a_hand_made_inbox_playlist_of_the_set_name_is_named_found_not_recorded`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_u135_set_inbox_join.py::test_a_hand_made_inbox_playlist_of_the_set_name_is_named_found_not_recorded`

Old text:

```
    for row in list(db.get_playlist(Name=name)):
        if rb_writer.is_folder(row) or rb_writer.node_removed(row):
            continue
        if str(getattr(row, "ParentID", "") or "") == str(root_id):
            return True
    return False

```

New text:

```
    return False

```

### `u135.A7_leftover_joins_numbered_twin`

A numbered twin of the set name under INBOX is no longer named as a leftover

- File: `src/cratekit/intake/native.py`
- Source: `u135.json`, row `A7_leftover_joins_numbered_twin`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u135_set_inbox_join.py::test_a_numbered_leftover_inbox_playlist_is_named_on_the_screen_and_not_joined`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_u135_set_inbox_join.py::test_a_numbered_leftover_inbox_playlist_is_named_on_the_screen_and_not_joined`

Old text:

```
        if held.startswith(prefix) and held[len(prefix) :].isdigit():
            named.append(held)

```

New text:

```
        if False:
            named.append(held)

```

### `u135.A8_job_key_not_stamped`

A set landing's batch playlist record carries no job key

- File: `src/cratekit/intake/native.py`
- Source: `u135.json`, row `A8_job_key_not_stamped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u135_set_inbox_join.py::test_a_set_landed_once_keeps_one_inbox_playlist_named_for_the_set`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_u135_set_inbox_join.py::test_a_set_landed_once_keeps_one_inbox_playlist_named_for_the_set`

Old text:

```
        if plan.set_job_id:
            kept[INBOX_JOB_KEY] = plan.set_job_id

```

New text:

```
        if False:
            kept[INBOX_JOB_KEY] = plan.set_job_id

```

### `u135.A12_inspiration_join_broken`

Second landing of a set remakes the INSPIRATION playlist instead of adding

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u135.json`, row `A12_inspiration_join_broken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u135_set_inbox_join.py::test_inspiration_join_stays_pinned_beside_the_inbox_join`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_u135_set_inbox_join.py::test_inspiration_join_stays_pinned_beside_the_inbox_join`

Old text:

```
        if row is None or rb_writer.is_folder(row) or rb_writer.node_removed(row):
            raise refuse(
                "decision-stale",
                f"the set's playlist {plan.name!r} (row {plan.playlist_id}) the plan "
                f"adds to is not live any more, so nothing was written",
                origin=_ORIGIN,
                detail={"playlist": plan.playlist_id, "name": plan.name},
            )
        return row, False

```

New text:

```
        return db.create_playlist(plan.name, parent=folder), True

```

