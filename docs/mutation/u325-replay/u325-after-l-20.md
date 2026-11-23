# Mutation table: u325-after-l-20

Measured by `scripts/mutate.py` on 2026-11-22 22:24 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 138.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:23 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 14, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u49-author.A3_the_refusal_names_no_ages` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 4 | killed |
| `u49-author.A4_the_record_on_file_is_not_shown` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 2 | killed |
| `u49-author.A6_the_authorisation_is_not_spent` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `u49-author.A7_the_check_rows_are_keyed_wrong` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `u49-author.A8_a_damaged_record_locks_the_verb_out` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `u49-author.R1_hard_code_the_repair_token` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `u49-author.R2_hard_code_the_permission_token` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 2 | killed |
| `u49-author.R3_an_unreadable_file_reads_as_empty` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 2 | killed |
| `u120-b.B4r_stale_not_refused` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 31 | 2 | killed |
| `u146-a.B10_job_no_date_dated_by_account` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 31 | 1 | killed |
| `u146-a.B11_listing_always_asked` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 31 | 3 | killed |
| `u146-a.B1_carried_states` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 31 | 7 | killed |
| `u146-a.B3_already_ignores_filed` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 31 | 3 | killed |
| `u146-a.B4_already_ignores_source` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 31 | 1 | killed |
| `u146-a.B5_removed_counts_a_live_row` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 31 | 1 | killed |
| `u146-a.B9_whole_and_short_swapped` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 31 | 4 | killed |
| `u153.B1_read_back_grey` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 31 | 21 | killed |
| `u153.B2_record_colour_only` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 31 | 1 | killed |
| `u153.B3_member_order_isdigit` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 31 | 1 | killed |
| `u146-b.B15_any_playlist_files` | `src/cratekit/favorites/placement.py` | user | 1 file(s) | 31 | 1 | killed |
| `u120.V1_no_ack` | `src/cratekit/favorites/backfill_cli.py` | user | 1 file(s) | 31 | 1 | killed |
| `u236.M13_write_records_no_month` | `src/cratekit/organize/mirror_edits.py` | user | 8 file(s) | 233 | 6 | killed |
| `u236.M14_write_wrong_time` | `src/cratekit/organize/mirror_edits.py` | user | 8 file(s) | 233 | 6 | killed |
| `u236.M15_settle_month_title` | `src/cratekit/organize/mirror_edits.py` | user | 8 file(s) | 233 | 8 | killed |
| `u236.M16_settle_any_favourite` | `src/cratekit/organize/mirror_edits.py` | user | 8 file(s) | 233 | 1 | killed |
| `u236.M17_ledger_settle_keeps_placement` | `src/cratekit/modules/outbound/ledger.py` | user | 8 file(s) | 233 | 4 | killed |
| `u236.M18_ledger_placement_not_written` | `src/cratekit/modules/outbound/ledger.py` | user | 8 file(s) | 233 | 8 | killed |
| `u236.M19_ledger_normalizer_drops` | `src/cratekit/modules/outbound/ledger.py` | user | 8 file(s) | 233 | 8 | killed |
| `u236.M20_agreed_never_drops` | `src/cratekit/modules/outbound/ledger.py` | user | 8 file(s) | 233 | 3 | killed |
| `r501-a.S1_verify_state_guard` | `src/cratekit/core/session.py` | maintainer | 5 file(s) | 175 | 1 | killed |
| `r501-a.S2_excusal_capture` | `src/cratekit/core/session.py` | user | 5 file(s) | 175 | 1 | killed |
| `r501-a.S3_excusal_proof` | `src/cratekit/core/session.py` | user | 5 file(s) | 175 | 5 | killed |
| `r501-a.S4_excusal_state` | `src/cratekit/core/session.py` | user | 5 file(s) | 175 | 1 | killed |
| `r501-a.T1_precheck_excusal` | `src/cratekit/core/tree_registry.py` | user | 5 file(s) | 175 | 4 | killed |
| `r501-b.I1_rollback_abandon` | `src/cratekit/intake/ingest.py` | user | 5 file(s) | 175 | 3 | killed |
| `r501-b.I2_rollback_unlink` | `src/cratekit/intake/ingest.py` | user | 5 file(s) | 175 | 1 | killed |
| `r501-b.I3_rollback_fresh_only` | `src/cratekit/intake/ingest.py` | user | 5 file(s) | 175 | 1 | killed |
| `r501-b.I4_mark_awaiting` | `src/cratekit/intake/ingest.py` | user | 5 file(s) | 175 | 42 | killed |
| `u79-a.A1_ambiguous_listed` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 2 | killed |
| `u79-a.A2_full_page_listed` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 1 | killed |
| `u79-a.A3_unreadable_ignored` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 1 | killed |
| `u79-a.A4_no_identifier_listed` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 2 | killed |
| `u79-a.A5_two_exact_picked` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 4 | killed |
| `u79-b.B1_floor_halved` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 1 | killed |
| `u79-b.B2_score_before_exact` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 1 | killed |
| `u79-b.B3_no_identifier_offered` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 2 | killed |
| `u79-b.B4_rejected_read_as_accepted` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 1 | killed |
| `u79-b.B5_unspecific_yes_takes_first` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 1 | killed |
| `u79-b.B6_option_track_mismatch` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 1 | killed |
| `u79-b.B8_open_item_searched_again` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 1 | killed |
| `r380.G3_retryable_requires_every_item` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 82 | 1 | killed |
| `r390-a.A3_a_failed_job_with_no_cause_is_refused` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 82 | 1 | killed |
| `r390-a.A4_refusal_drops_the_permanent_reasons` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 82 | 1 | killed |
| `r390-b.B1_last_reason_restored` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 82 | 1 | killed |
| `r390-b.B2_reasons_in_reverse_order` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 82 | 1 | killed |
| `r390-b.B3_message_does_not_name_the_reasons` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 82 | 1 | killed |
| `r390-b.B4_detail_drops_permanent_reasons` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 82 | 1 | killed |
| `r390-b.B5_one_shared_reason_is_also_mixed` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 82 | 2 | killed |
| `r390-b.B6_envelope_drops_the_reasons` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 82 | 1 | killed |
| `r390-b.B7_drive_passes_no_reasons_to_the_envelope` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 82 | 1 | killed |
| `u235.S1_enqueue_ignores_a_given_job_id` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 82 | 24 | killed |
| `r796-c.V1_the_worker_hands_the_seam_over` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 381 | 10 | killed |
| `r796-c.V2_blocked_warning_is_the_shops_only` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 381 | 1 | killed |
| `r796-c.V3_some_unread_is_said` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 381 | 1 | killed |
| `r796-c.V4_no_isrc_is_warned_about` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 381 | 1 | killed |
| `r796-c.V5_parse_break_sentence_said_once` | `src/cratekit/tagging/cli.py` | maintainer | 4 file(s) | 381 | 1 | killed |
| `r796-b.O9_no_isrc_is_not_no_hit` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 381 | 3 | killed |
| `u176.V10_same_bytes_staged` | `src/cratekit/acquire/bandcamp_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u176.V11_marked_by_file` | `src/cratekit/acquire/bandcamp_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u176.V12_strict_refuses_lossy` | `src/cratekit/acquire/bandcamp_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u176.V13_number_after_prefix` | `src/cratekit/acquire/bandcamp_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u176.V2_hidden` | `src/cratekit/acquire/bandcamp_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u176.V3_seller_filter` | `src/cratekit/acquire/bandcamp_cli.py` | user | 1 file(s) | 46 | 13 | killed |
| `u176.V4_record_planned_fetched` | `src/cratekit/acquire/bandcamp_cli.py` | user | 1 file(s) | 46 | 2 | killed |
| `u176.V5_suppressed_is_held` | `src/cratekit/acquire/bandcamp_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u176.V6_music_folder_present` | `src/cratekit/acquire/bandcamp_cli.py` | user | 1 file(s) | 46 | 2 | killed |
| `u176.V7_record_version` | `src/cratekit/acquire/bandcamp_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u176.V8_recorded_item_done` | `src/cratekit/acquire/bandcamp_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u176.V9_collision_refused` | `src/cratekit/acquire/bandcamp_cli.py` | user | 1 file(s) | 46 | 2 | killed |
| `u288.M10_changed_rows` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 286 | 7 | killed |
| `u288.M11_added_rows` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 286 | 2 | killed |
| `u288.M12_still_names` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 286 | 1 | killed |
| `u288.M13_counter_forward` | `src/cratekit/core/rb_writer.py` | maintainer | 2 file(s) | 286 | 1 | killed |
| `u288.M1_delete_admitted_by_any_name` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 286 | 2 | killed |
| `u288.M2_deletable_set_unbounded` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 286 | 1 | killed |
| `u288.M9_whose_row_disappeared` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 286 | 1 | killed |
| `r815-b.J1_one_refusal_ends_the_asking` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 1 | killed |
| `r815-b.J2_an_unread_catalogue_ends_the_run` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 1 | killed |
| `r815-b.J3_a_failing_provider_ends_the_run` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 1 | killed |
| `r815-b.J4_a_record_never_holds_on_its_own` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 3 | killed |
| `r815-c.J11_the_scope_reads_the_registry` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 1 | killed |
| `r815-c.J12_a_release_held_and_gone_is_counted_held` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 3 | killed |
| `r815-c.J13_the_refusal_carries_the_counts` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 7 | killed |
| `r815-c.J5_a_recorded_no_word_answer_is_not_asked_again` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 4 | killed |
| `r815-c.J6_a_decided_item_is_not_judged` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 2 | killed |
| `r815-c.J7_a_returned_release_is_not_judged` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 1 | killed |
| `r815-c.J9_a_park_drops_the_jobs_tools` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 3 | killed |
| `u217.A1_flush_on_the_way_out` | `src/cratekit/label/tidal_catalogue.py` | user | 2 file(s) | 212 | 12 | killed |
| `u217.A2_roster_lists_now` | `src/cratekit/label/tidal_catalogue.py` | user | 2 file(s) | 212 | 7 | killed |
| `u217.A3_listing_not_kept` | `src/cratekit/label/tidal_catalogue.py` | user | 2 file(s) | 212 | 12 | killed |
| `u217.A4_search_not_kept` | `src/cratekit/label/tidal_catalogue.py` | user | 2 file(s) | 212 | 10 | killed |
| `u217.A5_name_not_kept` | `src/cratekit/label/tidal_catalogue.py` | user | 2 file(s) | 212 | 1 | killed |
| `u217.A6_need_object` | `src/cratekit/label/tidal_catalogue.py` | user | 2 file(s) | 212 | 1 | killed |
| `u217.A7_missing_method_kept` | `src/cratekit/label/tidal_catalogue.py` | user | 2 file(s) | 212 | 1 | killed |
| `u217.A8_member_read_uncounted` | `src/cratekit/label/tidal_catalogue.py` | user | 2 file(s) | 212 | 1 | killed |
| `r1255.S1_scan_unlisted_as_empty` | `src/cratekit/core/session.py` | user | 7 file(s) | 893 | 16 | killed |
| `r1255.S2_absent_log_unread` | `src/cratekit/core/session.py` | user | 7 file(s) | 893 | 63 | killed |
| `r1255.S5_json_filter` | `src/cratekit/core/session.py` | user | 7 file(s) | 893 | 1 | killed |
| `r185-r246-author.E1_plan_gate_by_position` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 1 | killed |
| `r185-r246-author.E3_empty_plan_queues_anyway` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 2 | killed |
| `r185-r246-author.M1_folder_dropped` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 5 | killed |
| `r185-r246-author.W1_queue_warning_dropped` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 1 | killed |
| `r185-r246-author.W2_resume_warning_dropped` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 1 | killed |
| `r185-r246-author.W3_resume_warning_unconditional` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 1 | killed |
| `r185-r246-author.W4_refusal_step_dropped` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 3 | killed |
| `r185-r246-author.W5_refusal_step_unconditional` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 2 | killed |
| `r185-r246-author.W6_refusal_counts_the_plan` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 2 | killed |
| `r1017.M12_twin_message_names_to` | `src/cratekit/export/set_cli.py` | user | 4 file(s) | 195 | 1 | killed |
| `r1017.M1_no_recorded_names` | `src/cratekit/export/set_cli.py` | user | 4 file(s) | 195 | 5 | killed |
| `r1017.M2_recorded_before_frozen` | `src/cratekit/export/set_cli.py` | user | 4 file(s) | 195 | 1 | killed |
| `r1017.M3_landing_open_read` | `src/cratekit/intake/set_playlist.py` | user | 4 file(s) | 195 | 1 | killed |
| `r1017.M4_landing_uncommitted_read` | `src/cratekit/intake/set_playlist.py` | user | 4 file(s) | 195 | 1 | killed |
| `r1017.M5_landing_any_job` | `src/cratekit/intake/set_playlist.py` | user | 4 file(s) | 195 | 2 | killed |

## Row definitions

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

### `u120-b.B4r_stale_not_refused`

apply: a plan whose digest moved is written anyway

- File: `src/cratekit/favorites/backfill.py`
- Source: `u120-b.json`, row `B4r_stale_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_month_playlist_deleted_between_the_plan_and_the_write_is_another_plan`
  - `tests/test_favorites_backfill.py::test_the_write_itself_refuses_a_plan_whose_home_moved_with_no_gate_in_front`

Old text:

```
    if again.digest != approved.digest:
        raise refuse(
            "decision-stale",
            "the favourites are not as the approved plan read them, so no heart was "
```

New text:

```
    if False:
        raise refuse(
            "decision-stale",
            "the favourites are not as the approved plan read them, so no heart was "
```

### `u146-a.B10_job_no_date_dated_by_account`

gather: a row whose job dated it nowhere is dated from the account, so the backfill and the landing file one heart in two places

- File: `src/cratekit/favorites/backfill.py`
- Source: `u146-a.json`, row `B10_job_no_date_dated_by_account`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_its_job_dated_nowhere_stays_undated_though_the_account_dates_it_now`

Old text:

```
        if not heart.known:
```

New text:

```
        if heart.hearted is None:
```

### `u146-a.B11_listing_always_asked`

gather: the account is listed even when no heart needs placing

- File: `src/cratekit/favorites/backfill.py`
- Source: `u146-a.json`, row `B11_listing_always_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 3 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_and_undated_holds_is_not_given_a_month`
  - `tests/test_favorites_backfill.py::test_an_unreadable_account_refuses_only_when_a_heart_needs_placing`
  - `tests/test_favorites_backfill.py::test_the_backfill_colours_the_members_placed_before_it_and_holds_a_coloured_one`

Old text:

```
    if not candidates:
        return Gathered(
```

New text:

```
    if not candidates and False:
        return Gathered(
```

### `u146-a.B1_carried_states`

carried: the backfill reads only the carried states again, so an owned heart is never placed

- File: `src/cratekit/favorites/backfill.py`
- Source: `u146-a.json`, row `B1_carried_states`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 7 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_and_undated_holds_is_not_given_a_month`
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_at_the_root_beside_another_playlist_still_takes_its_month`
  - `tests/test_favorites_backfill.py::test_a_heart_its_job_dated_nowhere_stays_undated_though_the_account_dates_it_now`
  - `tests/test_favorites_backfill.py::test_a_heart_put_back_by_hand_after_a_removal_takes_its_month_and_is_not_taken_back`
  - `tests/test_favorites_backfill.py::test_an_owned_heart_in_a_batch_folder_is_placed_beside_a_downloaded_one`
  - `tests/test_favorites_backfill.py::test_an_owned_heart_the_source_system_filed_is_placed_and_one_with_no_row_is_not`
  - `tests/test_favorites_backfill.py::test_owned_hearts_not_in_all_favorites_are_planned_by_month_and_those_taken_back_are_named`

Old text:

```
                found = account_playlists.carried_hearts(store, job, states=None)
```

New text:

```
                found = account_playlists.carried_hearts(store, job)
```

### `u146-a.B3_already_ignores_filed`

gather: a heart All Favorites holds is already placed whatever its month, so a heart with no month never takes one

- File: `src/cratekit/favorites/backfill.py`
- Source: `u146-a.json`, row `B3_already_ignores_filed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 3 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_at_the_root_beside_another_playlist_still_takes_its_month`
  - `tests/test_favorites_backfill.py::test_a_heart_put_back_by_hand_after_a_removal_takes_its_month_and_is_not_taken_back`
  - `tests/test_favorites_backfill.py::test_a_heart_the_landing_placed_without_a_month_takes_it_from_the_backfill`

Old text:

```
        if content_id in in_source and content_id in filed:
```

New text:

```
        if content_id in in_source:
```

### `u146-a.B4_already_ignores_source`

gather: a heart a month holds is already placed whatever All Favorites holds, so a heart out of All Favorites is never put back nor named

- File: `src/cratekit/favorites/backfill.py`
- Source: `u146-a.json`, row `B4_already_ignores_source`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_the_author_took_out_of_all_favorites_is_never_put_back`

Old text:

```
        if content_id in in_source and content_id in filed:
```

New text:

```
        if content_id in filed:
```

### `u146-a.B5_removed_counts_a_live_row`

gather: a removed membership beside a live one reads as taken back, so a heart put back by hand never takes its month

- File: `src/cratekit/favorites/backfill.py`
- Source: `u146-a.json`, row `B5_removed_counts_a_live_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_put_back_by_hand_after_a_removal_takes_its_month_and_is_not_taken_back`

Old text:

```
    removed = placement.members_marked_removed(db, home.source_id) - in_source
```

New text:

```
    removed = placement.members_marked_removed(db, home.source_id)
```

### `u146-a.B9_whole_and_short_swapped`

gather: a heart a whole listing lacks is held back and one a short listing lacks is taken back

- File: `src/cratekit/favorites/backfill.py`
- Source: `u146-a.json`, row `B9_whole_and_short_swapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 4 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_a_short_listing_did_not_date_is_held_back_not_filed_undated`
  - `tests/test_favorites_backfill.py::test_a_heart_the_account_dates_nowhere_goes_to_undated_and_one_it_no_longer_carries_is_taken_back`
  - `tests/test_favorites_backfill.py::test_a_listing_with_no_published_count_holds_back_a_heart_it_lacks`
  - `tests/test_favorites_backfill.py::test_owned_hearts_not_in_all_favorites_are_planned_by_month_and_those_taken_back_are_named`

Old text:

```
            if listing.whole:
```

New text:

```
            if not listing.whole:
```

### `u153.B1_read_back_grey`

backfill _read_back: invert the Pink check, so a row that reads Pink is called a disagreement and the verb refuses

- File: `src/cratekit/favorites/backfill.py`
- Source: `u153.json`, row `B1_read_back_grey`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 21 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_carried_heart_whose_row_sits_deep_is_placed_now_the_path_rule_is_gone`
  - `tests/test_favorites_backfill.py::test_a_date_the_job_froze_wins_over_the_accounts`
  - `tests/test_favorites_backfill.py::test_a_heart_a_short_listing_did_not_date_is_held_back_not_filed_undated`
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_and_undated_holds_is_not_given_a_month`
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_at_the_root_beside_another_playlist_still_takes_its_month`
  - `tests/test_favorites_backfill.py::test_a_heart_its_job_dated_nowhere_stays_undated_though_the_account_dates_it_now`
  - `tests/test_favorites_backfill.py::test_a_heart_put_back_by_hand_after_a_removal_takes_its_month_and_is_not_taken_back`
  - `tests/test_favorites_backfill.py::test_a_heart_the_account_dates_nowhere_goes_to_undated_and_one_it_no_longer_carries_is_taken_back`
  - `tests/test_favorites_backfill.py::test_a_heart_the_author_took_out_of_all_favorites_is_never_put_back`
  - `tests/test_favorites_backfill.py::test_a_heart_two_jobs_carried_is_one_heart_with_the_dated_jobs_date`
  - `tests/test_favorites_backfill.py::test_a_hearts_job_whose_reports_cannot_be_read_is_skipped_and_named`
  - `tests/test_favorites_backfill.py::test_a_listing_with_no_published_count_holds_back_a_heart_it_lacks`
  - `tests/test_favorites_backfill.py::test_a_second_run_finds_the_same_hearts_and_writes_nothing`
  - `tests/test_favorites_backfill.py::test_an_owned_heart_in_a_batch_folder_is_placed_beside_a_downloaded_one`
  - `tests/test_favorites_backfill.py::test_an_owned_heart_the_source_system_filed_is_placed_and_one_with_no_row_is_not`
  - ... and 6 more, see the JSON sidecar

Old text:

```
        if str(getattr(colour.find_row(db, row), colour.COLUMN, "") or "") != pink
```

New text:

```
        if str(getattr(colour.find_row(db, row), colour.COLUMN, "") or "") == pink
```

### `u153.B2_record_colour_only`

backfill record: do not record a colour-only commit, so a run that only coloured leaves no session record

- File: `src/cratekit/favorites/backfill.py`
- Source: `u153.json`, row `B2_record_colour_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_the_backfill_colours_the_members_placed_before_it_and_holds_a_coloured_one`

Old text:

```
    if placed.added <= 0 and not placed.coloured:
```

New text:

```
    if placed.added <= 0:
```

### `u153.B3_member_order_isdigit`

backfill _member_order: sort every id as an int, so a non-numeric id raises and takes the plan down

- File: `src/cratekit/favorites/backfill.py`
- Source: `u153.json`, row `B3_member_order_isdigit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_member_order_is_numeric_and_tolerates_a_non_numeric_id`

Old text:

```
        content_ids, key=lambda c: (0, int(c), "") if str(c).isdigit() else (1, 0, str(c))
```

New text:

```
        content_ids, key=lambda c: (0, int(c), "")
```

### `u146-b.B15_any_playlist_files`

filed: any playlist beside the source files a heart, so one at the root beside another playlist never takes its month

- File: `src/cratekit/favorites/placement.py`
- Source: `u146-b.json`, row `B15_any_playlist_files`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_at_the_root_beside_another_playlist_still_takes_its_month`

Old text:

```
        if row != home.source_id and placeholders.is_filing(name):
```

New text:

```
        if row != home.source_id:
```

### `u120.V1_no_ack`

favorites_backfill: the acknowledgment is not read before the gate

- File: `src/cratekit/favorites/backfill_cli.py`
- Source: `u120.json`, row `V1_no_ack`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    session.assert_backup_acknowledged(cfg)

    plan = planned(cfg, source=source)
```

New text:

```
    plan = planned(cfg, source=source)
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

### `r501-a.S1_verify_state_guard`

session.mark_import_verified: drop the refusal of any state but awaiting-import, so any record can be marked proven

- File: `src/cratekit/core/session.py`
- Source: `r501-a.json`, row `S1_verify_state_guard`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 175 against a baseline of 175
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_only_a_run_waiting_on_an_import_has_one_to_verify`

Old text:

```
    if record.state is not SessionState.AWAITING_IMPORT:
        raise refuse(
            "internal-error",
            f"session {record.session_id} is {str(record.state)!r}, not "
            f"{str(SessionState.AWAITING_IMPORT)!r}; only a session waiting on an "
            f"import has one to verify",
```

New text:

```
    if False:
        raise refuse(
            "internal-error",
            f"session {record.session_id} is {str(record.state)!r}, not "
            f"{str(SessionState.AWAITING_IMPORT)!r}; only a session waiting on an "
            f"import has one to verify",
```

### `r501-a.S2_excusal_capture`

session.owes_only_deferred_routing: drop the no capture condition, so a run holding a capture is excused from the cutover precheck

- File: `src/cratekit/core/session.py`
- Source: `r501-a.json`, row `S2_excusal_capture`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 175 against a baseline of 175
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_the_precheck_refuses_a_verified_run_that_holds_a_capture`

Old text:

```
        record.state is SessionState.OPEN
        and record.snapshot_path is None
        and IMPORT_VERIFIED_KEY in record.detail
```

New text:

```
        record.state is SessionState.OPEN
        and IMPORT_VERIFIED_KEY in record.detail
```

### `r501-a.S3_excusal_proof`

session.owes_only_deferred_routing: drop the proof condition, so any open run with no capture is excused, a crashed landing included

- File: `src/cratekit/core/session.py`
- Source: `r501-a.json`, row `S3_excusal_proof`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 175 against a baseline of 175
- Kills: 5 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_an_open_run_blocks_the_flip`
  - `tests/test_cutover_precheck.py::test_an_open_run_refuses_the_revert_because_it_may_have_written`
  - `tests/test_intake_imported.py::test_a_run_landed_before_the_fix_is_settled_too`
  - `tests/test_intake_imported.py::test_doctor_reads_a_proven_run_as_proven_and_not_as_in_progress`
  - `tests/test_intake_imported.py::test_the_precheck_refuses_an_open_run_with_no_proof_recorded`

Old text:

```
        record.state is SessionState.OPEN
        and record.snapshot_path is None
        and IMPORT_VERIFIED_KEY in record.detail
```

New text:

```
        record.state is SessionState.OPEN
        and record.snapshot_path is None
```

### `r501-a.S4_excusal_state`

session.owes_only_deferred_routing: drop the open state condition, so a committed-unverified run carrying the key is excused

- File: `src/cratekit/core/session.py`
- Source: `r501-a.json`, row `S4_excusal_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 175 against a baseline of 175
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_the_precheck_refuses_a_verified_run_that_is_not_open`

Old text:

```
        record.state is SessionState.OPEN
        and record.snapshot_path is None
        and IMPORT_VERIFIED_KEY in record.detail
```

New text:

```
        record.snapshot_path is None
        and IMPORT_VERIFIED_KEY in record.detail
```

### `r501-a.T1_precheck_excusal`

tree_registry.assert_cutover_ready: drop the excusal, so a proven landing refuses the cutover for ever, which is R-501 itself

- File: `src/cratekit/core/tree_registry.py`
- Source: `r501-a.json`, row `T1_precheck_excusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 175 against a baseline of 175
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_landing_followed_step_by_step_passes_the_cutover_precheck`
  - `tests/test_intake_imported.py::test_a_run_landed_before_the_fix_is_settled_too`
  - `tests/test_intake_imported.py::test_intake_file_ends_pending_and_is_settled_the_same_way`
  - `tests/test_intake_imported.py::test_the_precheck_excuses_a_verified_run_holding_no_capture`

Old text:

```
        if not record.terminal and not session.owes_only_deferred_routing(record)
```

New text:

```
        if not record.terminal
```

### `r501-b.I1_rollback_abandon`

ingest.place_files: drop the abandon in the rollback, so a refused call leaves its session non terminal

- File: `src/cratekit/intake/ingest.py`
- Source: `r501-b.json`, row `I1_rollback_abandon`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 175 against a baseline of 175
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_failed_call_leaves_an_earlier_runs_intake_file_alone`
  - `tests/test_intake_imported.py::test_a_failed_call_records_no_track_the_ledger_cannot_withdraw`
  - `tests/test_intake_imported.py::test_a_refusal_after_the_session_opens_abandons_it_and_removes_the_file`

Old text:

```
        with contextlib.suppress(Exception):
            routing_pass.close_run(record, cfg, state=session.SessionState.ABANDONED)
        raise
```

New text:

```
        raise
```

### `r501-b.I2_rollback_unlink`

ingest.place_files: drop the unlink in the rollback, so a refused call leaves an intake file with no run behind it

- File: `src/cratekit/intake/ingest.py`
- Source: `r501-b.json`, row `I2_rollback_unlink`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 175 against a baseline of 175
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_refusal_after_the_session_opens_abandons_it_and_removes_the_file`

Old text:

```
        if wrote and fresh:
            with contextlib.suppress(OSError):
                destination.unlink(missing_ok=True)
```

New text:

```
        if False:
            with contextlib.suppress(OSError):
                destination.unlink(missing_ok=True)
```

### `r501-b.I3_rollback_fresh_only`

ingest.place_files: unlink whatever is at the destination, so a failed call removes an earlier run's intake file

- File: `src/cratekit/intake/ingest.py`
- Source: `r501-b.json`, row `I3_rollback_fresh_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 175 against a baseline of 175
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_failed_call_leaves_an_earlier_runs_intake_file_alone`

Old text:

```
        if wrote and fresh:
```

New text:

```
        if wrote:
```

### `r501-b.I4_mark_awaiting`

ingest.place_files: never mark the session awaiting-import, so every landing leaves an open record again

- File: `src/cratekit/intake/ingest.py`
- Source: `r501-b.json`, row `I4_mark_awaiting`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 175 against a baseline of 175
- Kills: 42 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_failed_call_leaves_an_earlier_runs_intake_file_alone`
  - `tests/test_intake_imported.py::test_a_failed_call_records_no_track_the_ledger_cannot_withdraw`
  - `tests/test_intake_imported.py::test_a_landing_followed_step_by_step_passes_the_cutover_precheck`
  - `tests/test_intake_imported.py::test_a_named_run_that_is_not_waiting_is_refused`
  - `tests/test_intake_imported.py::test_a_partly_imported_batch_is_not_imported`
  - `tests/test_intake_imported.py::test_a_placed_call_ends_awaiting_import_with_the_action_persisted`
  - `tests/test_intake_imported.py::test_a_refused_close_is_reported_and_tried_again_next_time`
  - `tests/test_intake_imported.py::test_a_retire_that_cannot_rename_is_a_refusal_and_changes_nothing`
  - `tests/test_intake_imported.py::test_a_run_landed_before_the_fix_is_settled_too`
  - `tests/test_intake_imported.py::test_a_run_the_export_does_not_prove_is_named_beside_the_one_it_does`
  - `tests/test_intake_imported.py::test_a_run_the_ledger_names_no_file_for_is_left_alone`
  - `tests/test_intake_imported.py::test_a_stub_listing_is_refused_as_the_export`
  - `tests/test_intake_imported.py::test_a_verified_run_stays_open_with_its_placements_still_owed`
  - `tests/test_intake_imported.py::test_a_waiting_run_with_no_export_named_is_refused_and_says_what_to_pass`
  - `tests/test_intake_imported.py::test_a_waiting_run_with_tracks_still_outstanding_is_not_called_imported`
  - ... and 27 more, see the JSON sidecar

Old text:

```
        wrote = True
        session.mark_awaiting_import(
```

New text:

```
        wrote = True
        session.pending_import if False else (lambda *a, **k: None)(
```

### `u79-a.A1_ambiguous_listed`

A title that reads two ways is listed on one candidate without a person

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-a.json`, row `A1_ambiguous_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 56 against a baseline of 56
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_title_with_two_readings_is_never_listed_on_one_candidate[the-title-reading]`
  - `tests/test_intake_missing_search.py::test_a_title_with_two_readings_is_never_listed_on_one_candidate[the-version-reading]`

Old text:

```
    if answer.ambiguous or answer.full:
        return None
```

New text:

```
    if answer.full:
        return None
```

### `u79-a.A2_full_page_listed`

A full page is read as the whole answer, so its one exact hit is listed

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-a.json`, row `A2_full_page_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_full_page_is_never_the_whole_answer_so_its_one_exact_hit_is_offered`

Old text:

```
    if answer.ambiguous or answer.full:
        return None
```

New text:

```
    if answer.ambiguous:
        return None
```

### `u79-a.A3_unreadable_ignored`

A row of the answer that could not be read no longer stops a listing

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-a.json`, row `A3_unreadable_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_an_exact_candidate_beside_a_row_that_cannot_be_read_is_offered`

Old text:

```
    if answer.unreadable or not exact:
```

New text:

```
    if not exact:
```

### `u79-a.A4_no_identifier_listed`

Exact candidates carrying no identifier are one distinct value and are listed

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-a.json`, row `A4_no_identifier_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 56 against a baseline of 56
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_exact_hits_with_no_identifier_are_reported_as_that_and_not_as_no_resemblance`
  - `tests/test_intake_missing_search.py::test_the_only_exact_candidate_carrying_no_identifier_is_not_listed`

Old text:

```
    if any(not one.track.ref for one in exact):
        return None
```

New text:

```
    if False:
        return None
```

### `u79-a.A5_two_exact_picked`

Two exact candidates list the first, the pick the brief forbids

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-a.json`, row `A5_two_exact_picked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 56 against a baseline of 56
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_an_acceptance_naming_none_of_several_candidates_lists_nothing`
  - `tests/test_intake_missing_search.py::test_an_exact_candidate_under_the_floor_of_nothing_is_still_first`
  - `tests/test_intake_missing_search.py::test_more_candidates_than_the_screen_holds_are_truncated_and_counted`
  - `tests/test_intake_missing_search.py::test_two_exact_candidates_are_offered_and_neither_is_picked`

Old text:

```
    if len({one.track.ref for one in exact}) != 1:
```

New text:

```
    if len({one.track.ref for one in exact}) < 1:
```

### `u79-b.B1_floor_halved`

The floor's value is halved, so a weaker hit is shown

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-b.json`, row `B1_floor_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_no_candidate_for_any_row_refuses_rather_than_reading_as_nothing_to_do`

Old text:

```
CANDIDATE_FLOOR = 60.0
```

New text:

```
CANDIDATE_FLOOR = 30.0
```

### `u79-b.B2_score_before_exact`

A near miss scoring 100 leads an exact candidate

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-b.json`, row `B2_score_before_exact`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_an_exact_candidate_under_the_floor_of_nothing_is_still_first`

Old text:

```
            (not one.exact, -one.score, position, one)
```

New text:

```
            (False, -one.score, position, one)
```

### `u79-b.B3_no_identifier_offered`

A candidate with no identifier is offered as an option

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-b.json`, row `B3_no_identifier_offered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 56 against a baseline of 56
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_an_exact_candidate_beside_an_exact_one_with_no_identifier_is_offered`
  - `tests/test_intake_missing_search.py::test_exact_hits_with_no_identifier_are_reported_as_that_and_not_as_no_resemblance`

Old text:

```
            if one.track.ref and (one.exact or one.score >= CANDIDATE_FLOOR)
        ),
        key=
```

New text:

```
            if (one.exact or one.score >= CANDIDATE_FLOOR)
        ),
        key=
```

### `u79-b.B4_rejected_read_as_accepted`

A rejected row falls through to the accepted path and its one candidate is listed

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-b.json`, row `B4_rejected_read_as_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_rejected_row_is_reported_and_never_searched_again`

Old text:

```
    if held.verdict is review.Verdict.REJECTED:
```

New text:

```
    if False:
```

### `u79-b.B5_unspecific_yes_takes_first`

An acceptance naming none of several candidates lists the first

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-b.json`, row `B5_unspecific_yes_takes_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_an_acceptance_naming_none_of_several_candidates_lists_nothing`

Old text:

```
    if chosen is None and len(held.options) == 1:
```

New text:

```
    if chosen is None and len(held.options) >= 1:
```

### `u79-b.B6_option_track_mismatch`

An accepted option whose detail names another track is listed as that track

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-b.json`, row `B6_option_track_mismatch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_an_accepted_option_that_does_not_carry_its_own_track_lists_nothing`

Old text:

```
    if track is None or not track.ref or track.ref != option.option_id:
```

New text:

```
    if track is None or not track.ref:
```

### `u79-b.B8_open_item_searched_again`

A row already in front of a person is searched for again

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-b.json`, row `B8_open_item_searched_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_second_run_offers_nothing_new_and_spends_no_search`

Old text:

```
    if held.verdict is None:
        return Proposal(
```

New text:

```
    if held.verdict is None:
        return None
    if held.verdict is None:
        return Proposal(
```

### `r380.G3_retryable_requires_every_item`

a mixed job is non retryable unless every failure is retryable

- File: `src/cratekit/core/jobs.py`
- Source: `r380.json`, row `G3_retryable_requires_every_item`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 82 against a baseline of 82
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

### `r390-a.A3_a_failed_job_with_no_cause_is_refused`

a missing verdict is read as a permanent one

- File: `src/cratekit/core/jobs.py`
- Source: `r390-a.json`, row `A3_a_failed_job_with_no_cause_is_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_failed_job_with_no_recorded_cause_still_re_arms`

Old text:

```
    if current.cause is not None and not current.cause.retryable:
        raise refuse(
            "job-not-retryable",
```

New text:

```
    if current.cause is None or not current.cause.retryable:
        raise refuse(
            "job-not-retryable",
```

### `r390-a.A4_refusal_drops_the_permanent_reasons`

the resume refusal no longer names the mixed reasons at its own top level

- File: `src/cratekit/core/jobs.py`
- Source: `r390-a.json`, row `A4_refusal_drops_the_permanent_reasons`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_two_distinct_permanent_reasons_name_both_whichever_failed_last`

Old text:

```
                "state": str(current.state),
                # Named on the refusal as the job cause names them (R-391), so
                # a person is not sent into the nested cause to learn which.
                **_permanent_reasons_of(current.cause),
            },
            inner=current.cause,
```

New text:

```
                "state": str(current.state),
            },
            inner=current.cause,
```

### `r390-b.B1_last_reason_restored`

the original defect: several permanent reasons take the last item's reason

- File: `src/cratekit/core/jobs.py`
- Source: `r390-b.json`, row `B1_last_reason_restored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_two_distinct_permanent_reasons_name_both_whichever_failed_last`

Old text:

```
    reason = reasons[0] if len(reasons) == 1 else "mixed-permanent-failures"
```

New text:

```
    reason = failed[-1].reason
```

### `r390-b.B2_reasons_in_reverse_order`

the sorted set is pinned in one order: reverse it

- File: `src/cratekit/core/jobs.py`
- Source: `r390-b.json`, row `B2_reasons_in_reverse_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_two_distinct_permanent_reasons_name_both_whichever_failed_last`

Old text:

```
    reasons = tuple(sorted({cause.reason for cause in failed}))
```

New text:

```
    reasons = tuple(sorted({cause.reason for cause in failed}, reverse=True))
```

### `r390-b.B3_message_does_not_name_the_reasons`

the job cause message keeps the counts and drops the list of reasons

- File: `src/cratekit/core/jobs.py`
- Source: `r390-b.json`, row `B3_message_does_not_name_the_reasons`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_two_distinct_permanent_reasons_name_both_whichever_failed_last`

Old text:

```
            message += (
                f"; the {permanent} permanent failures carry {len(reasons)} "
                f"distinct reasons: {', '.join(reasons)}"
            )
            detail[PERMANENT_REASONS] = reasons
```

New text:

```
            detail[PERMANENT_REASONS] = reasons
```

### `r390-b.B4_detail_drops_permanent_reasons`

the job cause names the reasons in prose and drops them from detail

- File: `src/cratekit/core/jobs.py`
- Source: `r390-b.json`, row `B4_detail_drops_permanent_reasons`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_two_distinct_permanent_reasons_name_both_whichever_failed_last`

Old text:

```
            message += (
                f"; the {permanent} permanent failures carry {len(reasons)} "
                f"distinct reasons: {', '.join(reasons)}"
            )
            detail[PERMANENT_REASONS] = reasons
```

New text:

```
            message += (
                f"; the {permanent} permanent failures carry {len(reasons)} "
                f"distinct reasons: {', '.join(reasons)}"
            )
```

### `r390-b.B5_one_shared_reason_is_also_mixed`

the threshold moves so a single shared reason is reported as mixed too

- File: `src/cratekit/core/jobs.py`
- Source: `r390-b.json`, row `B5_one_shared_reason_is_also_mixed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 82 against a baseline of 82
- Kills: 2 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_partial_failure_whose_failures_are_permanent_is_not_resumable`
  - `tests/test_jobs.py::test_one_shared_permanent_reason_is_still_the_jobs_reason`

Old text:

```
        if len(reasons) > 1:
            # R-391.
```

New text:

```
        if len(reasons) > 0:
            # R-391.
```

### `r390-b.B6_envelope_drops_the_reasons`

the all failed envelope keeps the item nested and drops the reasons beside it

- File: `src/cratekit/core/jobs.py`
- Source: `r390-b.json`, row `B6_envelope_drops_the_reasons`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_two_distinct_permanent_reasons_name_both_whichever_failed_last`

Old text:

```
        message += (
            f"; the failures carry {len(permanent_reasons)} distinct permanent "
            f"reasons: {', '.join(permanent_reasons)}"
        )
        detail[PERMANENT_REASONS] = tuple(permanent_reasons)
```

New text:

```
        pass
```

### `r390-b.B7_drive_passes_no_reasons_to_the_envelope`

the envelope can carry the reasons and the driver hands it none

- File: `src/cratekit/core/jobs.py`
- Source: `r390-b.json`, row `B7_drive_passes_no_reasons_to_the_envelope`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_two_distinct_permanent_reasons_name_both_whichever_failed_last`

Old text:

```
                permanent_reasons=_permanent_reasons_of(result.job.cause).get(
                    PERMANENT_REASONS, ()
                )
                if result.job.cause is not None
                else (),
```

New text:

```
                permanent_reasons=(),
```

### `u235.S1_enqueue_ignores_a_given_job_id`

jobs.enqueue: a job id the caller names is ignored and a fresh identifier minted, a sample of the guard that hands new_run_id to every job

- File: `src/cratekit/core/jobs.py`
- Source: `u235.json`, row `S1_enqueue_ignores_a_given_job_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 82 against a baseline of 82
- Kills: 24 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_blocked_job_or_another_librarys_is_left_by_the_stale_cancel`
  - `tests/test_jobs.py::test_a_cancel_whose_playlist_another_open_job_holds_says_it_frees_nothing_yet`
  - `tests/test_jobs.py::test_a_cancelled_stale_job_reports_cancelled_and_resumes_by_its_own_command`
  - `tests/test_jobs.py::test_a_dry_run_lists_a_queued_job_a_live_driver_holds_as_left`
  - `tests/test_jobs.py::test_a_dry_run_lists_three_stale_jobs_and_names_the_keeper_of_the_identical_two`
  - `tests/test_jobs.py::test_a_dry_run_of_one_job_cancels_nothing`
  - `tests/test_jobs.py::test_a_hearts_job_names_no_playlist_and_frees_the_hearts`
  - `tests/test_jobs.py::test_a_job_id_beside_stale_days_is_a_usage_error`
  - `tests/test_jobs.py::test_a_job_whose_queued_time_cannot_be_read_is_never_stale`
  - `tests/test_jobs.py::test_a_reference_the_url_parser_cannot_read_is_kept_as_typed_not_a_crash`
  - `tests/test_jobs.py::test_a_running_job_is_never_listed_for_cancel_however_old`
  - `tests/test_jobs.py::test_a_stale_set_job_says_it_frees_no_playlist_and_names_no_file_as_one`
  - `tests/test_jobs.py::test_a_url_typed_by_hand_holds_the_same_playlist_a_sweeps_id_does`
  - `tests/test_jobs.py::test_a_zero_or_negative_day_count_is_the_parsers_usage_error_and_cancels_nothing`
  - `tests/test_jobs.py::test_cancelling_through_the_verb_succeeds_and_reports_cancelled`
  - ... and 9 more, see the JSON sidecar

Old text:

```
    identifier = job_id or new_run_id()
```

New text:

```
    identifier = new_run_id()
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

### `u176.V10_same_bytes_staged`

handle_fetch: the same bytes already in the batch are refused rather than counted staged

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u176.json`, row `V10_same_bytes_staged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_cli.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_bandcamp_cli.py::test_the_same_bytes_already_in_the_batch_count_as_staged`

Old text:

```
            if final.is_file() and filecmp.cmp(path, final, shallow=False):
```

New text:

```
            if False:
```

### `u176.V11_marked_by_file`

handle_fetch: a file is marked by the offer alone, so lossy bytes under a lossless offer stage unmarked

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u176.json`, row `V11_marked_by_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_cli.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_bandcamp_cli.py::test_a_lossy_file_under_a_lossless_offer_is_marked_by_what_it_is`

Old text:

```
        marked = lossy or acquire_cli.lossy_landing(path, policy=policy)
```

New text:

```
        marked = lossy
```

### `u176.V12_strict_refuses_lossy`

_encoding: the strict policy takes a lossy format when no lossless one is offered

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u176.json`, row `V12_strict_refuses_lossy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_cli.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_bandcamp_cli.py::test_strict_refuses_a_release_offered_only_lossy`

Old text:

```
    if not decision.permitted:
```

New text:

```
    if False:
```

### `u176.V13_number_after_prefix`

number_in: the prefix is not required, so a number in the album title holds the wrong track

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u176.json`, row `V13_number_after_prefix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_cli.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_bandcamp_cli.py::test_number_in_reads_after_the_release_prefix_only`

Old text:

```
    if not artist or not title or not name.startswith(prefix):
        return None
```

New text:

```
    if not artist or not title:
        return None
```

### `u176.V2_hidden`

plan: a hidden purchase is not planned hidden, so a purchase the account hid is fetched

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u176.json`, row `V2_hidden`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_cli.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_bandcamp_cli.py::test_a_hidden_purchase_is_planned_hidden`

Old text:

```
        if purchase.hidden:
```

New text:

```
        if False:
```

### `u176.V3_seller_filter`

plan: --seller filters nothing

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u176.json`, row `V3_seller_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_cli.py`
- Collected: 46 against a baseline of 46
- Kills: 13 (killed)
- Killed:
  - `tests/test_bandcamp_cli.py::test_a_library_unmounted_since_the_queue_parks_the_resumed_job`
  - `tests/test_bandcamp_cli.py::test_a_listing_bandcamp_cannot_answer_parks_the_resumed_job`
  - `tests/test_bandcamp_cli.py::test_a_listing_the_session_is_refused_at_parks_the_resumed_job`
  - `tests/test_bandcamp_cli.py::test_a_lossy_file_under_a_lossless_offer_is_marked_by_what_it_is`
  - `tests/test_bandcamp_cli.py::test_a_permissive_policy_takes_the_lossy_release_marked`
  - `tests/test_bandcamp_cli.py::test_a_purchase_already_recorded_is_done_when_its_item_runs_again`
  - `tests/test_bandcamp_cli.py::test_a_purchase_filtered_out_is_offered_on_the_next_run_without_the_filter`
  - `tests/test_bandcamp_cli.py::test_a_purchase_no_longer_downloadable_fails_permanently`
  - `tests/test_bandcamp_cli.py::test_a_seller_filter_plans_only_that_seller`
  - `tests/test_bandcamp_cli.py::test_a_seller_matching_nothing_is_warned_about`
  - `tests/test_bandcamp_cli.py::test_a_session_refused_in_the_worker_parks_the_job_and_a_resume_continues`
  - `tests/test_bandcamp_cli.py::test_a_session_removed_since_the_queue_parks_the_resumed_job`
  - `tests/test_bandcamp_cli.py::test_strict_refuses_a_release_offered_only_lossy`

Old text:

```
        if sellers and purchase.seller.casefold() not in sellers:
```

New text:

```
        if False:
```

### `u176.V4_record_planned_fetched`

plan: a purchase the record holds is planned again, so a second run fetches it again

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u176.json`, row `V4_record_planned_fetched`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_cli.py`
- Collected: 46 against a baseline of 46
- Kills: 2 (killed)
- Killed:
  - `tests/test_bandcamp_cli.py::test_a_purchase_the_record_holds_is_done_on_a_resume_and_fetched_nothing_twice`
  - `tests/test_bandcamp_cli.py::test_a_second_run_plans_nothing`

Old text:

```
        if purchase.item_id in record:
```

New text:

```
        if False:
```

### `u176.V5_suppressed_is_held`

holding: a track a tombstone suppresses is not held, so a deletion made on purpose is fetched back

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u176.json`, row `V5_suppressed_is_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_cli.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_bandcamp_cli.py::test_a_track_the_library_deleted_on_purpose_is_held`

Old text:

```
        return str(found.why), ()
```

New text:

```
        return None
```

### `u176.V6_music_folder_present`

Library: an absent music folder is read as an empty library, so every purchase plans new

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u176.json`, row `V6_music_folder_present`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_cli.py`
- Collected: 46 against a baseline of 46
- Kills: 2 (killed)
- Killed:
  - `tests/test_bandcamp_cli.py::test_a_library_unmounted_since_the_queue_parks_the_resumed_job`
  - `tests/test_bandcamp_cli.py::test_an_absent_music_folder_refuses_rather_than_planning_everything_new`

Old text:

```
        if not music.is_dir():
```

New text:

```
        if False:
```

### `u176.V7_record_version`

fetched: a record of another version is read, so its purchases are trusted under a shape this build does not know

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u176.json`, row `V7_record_version`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_cli.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_bandcamp_cli.py::test_an_unreadable_record_refuses_rather_than_offering_everything_again[newer-version]`

Old text:

```
    if raw.get("version") != RECORD_VERSION:
```

New text:

```
    if False:
```

### `u176.V8_recorded_item_done`

handle_fetch: a purchase the record holds is fetched again when its item runs again

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u176.json`, row `V8_recorded_item_done`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_cli.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_bandcamp_cli.py::test_a_purchase_already_recorded_is_done_when_its_item_runs_again`

Old text:

```
    if item.item_id in fetched(cfg):
```

New text:

```
    if False:
```

### `u176.V9_collision_refused`

handle_fetch: a name already in the batch is overwritten rather than refused

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u176.json`, row `V9_collision_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_cli.py`
- Collected: 46 against a baseline of 46
- Kills: 2 (killed)
- Killed:
  - `tests/test_bandcamp_cli.py::test_a_name_already_in_the_batch_refuses_that_file_alone`
  - `tests/test_bandcamp_cli.py::test_a_refused_copy_is_kept_and_named_never_deleted`

Old text:

```
        if final.exists():
            if final.is_file()
```

New text:

```
        if False:
            if final.is_file()
```

### `u288.M10_changed_rows`

collection_removal_violations: read a changed row as unchanged

- File: `src/cratekit/core/rb_writer.py`
- Source: `u288.json`, row `M10_changed_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 286 against a baseline of 286
- Kills: 7 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_confined_removal_reads_clean_and_every_stray_difference_is_named`
  - `tests/test_rb_writer_guard.py::test_a_reading_with_no_positions_admits_no_membership_change`
  - `tests/test_rb_writer_guard.py::test_the_confinement_admits_the_planned_renumbering_and_nothing_beside_it`
  - `tests/test_rb_writer_guard.py::test_the_confinement_refuses_a_marked_row_renumbered`
  - `tests/test_rb_writer_guard.py::test_the_read_back_after_the_commit_admits_only_the_counter_moving_forward`
  - `tests/test_sync_removed.py::test_a_renumbering_that_moves_any_other_membership_is_refused_with_nothing_written`
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
- Collected: 286 against a baseline of 286
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
- Collected: 286 against a baseline of 286
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_planned_removal_that_was_not_made_is_refused`

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
- Collected: 286 against a baseline of 286
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
- Collected: 286 against a baseline of 286
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
- Collected: 286 against a baseline of 286
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
- Collected: 286 against a baseline of 286
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

### `r815-b.J1_one_refusal_ends_the_asking`

_asked: remember no refusal

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-b.json`, row `J1_one_refusal_ends_the_asking`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_catalogue_that_refuses_stops_the_run_at_once_and_says_how_many_were_left`

Old text:

```
    if judged.answer == searchers.Answer.BLOCKED.value:
        tools.refused = judged.reason
```

New text:

```
    if False:
        tools.refused = judged.reason
```

### `r815-b.J2_an_unread_catalogue_ends_the_run`

_asked: never stop on the gate's bound of unread releases

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-b.json`, row `J2_an_unread_catalogue_ends_the_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_catalogue_unread_three_times_in_a_row_stops_the_run_and_says_how_many_were_left`

Old text:

```
    if tools.asking.given_up:
        raise refuse(
```

New text:

```
    if False:
        raise refuse(
```

### `r815-b.J3_a_failing_provider_ends_the_run`

_asked: never stop on the reader's bound of failed reads

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-b.json`, row `J3_a_failing_provider_ends_the_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_judge.py::test_three_provider_reads_failing_in_a_row_stop_the_run`

Old text:

```
    if tools.reader.given_up:
        raise refuse(
```

New text:

```
    if False:
        raise refuse(
```

### `r815-b.J4_a_record_never_holds_on_its_own`

_judged: take a hold from recorded words without asking

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-b.json`, row `J4_a_record_never_holds_on_its_own`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_fresh_answer_with_no_word_takes_the_old_words_off_the_item`
  - `tests/test_label_judge.py::test_a_record_of_one_tracks_album_does_not_hold_a_release_its_next_track_passes`
  - `tests/test_label_judge.py::test_recorded_words_that_would_hold_are_asked_about_before_the_release_is_held`

Old text:

```
    if recorded is not None and not recorded.held:
        return recorded, False
```

New text:

```
    if recorded is not None:
        return recorded, False
```

### `r815-c.J11_the_scope_reads_the_registry`

_Scope.holds: compare the identifier as text

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-c.json`, row `J11_the_scope_reads_the_registry`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_release_filed_under_a_labels_old_identifier_is_in_a_run_scoped_to_the_label`

Old text:

```
        return entry is not None and entry.label_id in self.label_ids
```

New text:

```
        return label_id in self.label_ids
```

### `r815-c.J12_a_release_held_and_gone_is_counted_held`

_left_review: report gone whatever holds the release

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-c.json`, row `J12_a_release_held_and_gone_is_counted_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_release_another_job_held_while_this_one_was_asking_is_counted_held`
  - `tests/test_label_judge.py::test_a_release_held_under_an_earlier_holds_run_is_counted_held_when_it_is_redone`
  - `tests/test_label_judge.py::test_a_run_stopped_part_way_and_resumed_judges_none_twice_and_skips_none[stopped-on-a-held-release]`

Old text:

```
    if standing is not None and standing.state == review.HOLD_HELD:
        return _report(item_id, HELD, _held_already(standing), reason=standing.reason)
```

New text:

```
    if False:
        return _report(item_id, HELD, _held_already(standing), reason=standing.reason)
```

### `r815-c.J13_the_refusal_carries_the_counts`

_resume: let the refusal leave without the summary

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-c.json`, row `J13_the_refusal_carries_the_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_catalogue_that_refuses_stops_the_run_at_once_and_says_how_many_were_left`
  - `tests/test_label_judge.py::test_a_catalogue_unread_three_times_in_a_row_stops_the_run_and_says_how_many_were_left`
  - `tests/test_label_judge.py::test_a_refusal_from_the_provider_parks_the_run_on_that_refusal`
  - `tests/test_label_judge.py::test_a_run_stopped_part_way_and_resumed_judges_none_twice_and_skips_none[stopped-on-a-held-release]`
  - `tests/test_label_judge.py::test_a_run_stopped_part_way_and_resumed_judges_none_twice_and_skips_none[stopped-on-a-passed-release]`
  - `tests/test_label_judge.py::test_a_taxonomy_that_stops_being_readable_parks_the_run_and_fails_no_release`
  - `tests/test_label_judge.py::test_three_provider_reads_failing_in_a_row_stop_the_run`

Old text:

```
            raise _with_summary(failed, cfg, store, queued.job_id) from failed
```

New text:

```
            raise
```

### `r815-c.J5_a_recorded_no_word_answer_is_not_asked_again`

_judged: ask about a release the catalogue already had no word for

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-c.json`, row `J5_a_recorded_no_word_answer_is_not_asked_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_fresh_answer_with_no_word_takes_the_old_words_off_the_item`
  - `tests/test_label_judge.py::test_a_release_the_catalogue_already_had_no_word_for_is_not_asked_about_again[matched]`
  - `tests/test_label_judge.py::test_a_release_the_catalogue_already_had_no_word_for_is_not_asked_about_again[miss]`
  - `tests/test_label_judge.py::test_a_release_the_catalogue_already_had_no_word_for_is_not_asked_about_again[no-isrc]`

Old text:

```
    if recorded is None and isinstance(said, str) and said in genre_gate.NO_WORD_ANSWERS:
```

New text:

```
    if False:
```

### `r815-c.J6_a_decided_item_is_not_judged`

_judge_one: judge an item a person has decided

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-c.json`, row `J6_a_decided_item_is_not_judged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_judge.py::test_an_item_decided_after_the_job_was_queued_is_untouched[accepted]`
  - `tests/test_label_judge.py::test_an_item_decided_after_the_job_was_queued_is_untouched[rejected]`

Old text:

```
        if found.stored_verdict is not None:
            return _report(
```

New text:

```
        if False:
            return _report(
```

### `r815-c.J7_a_returned_release_is_not_judged`

_judge_one: judge a release a person returned

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-c.json`, row `J7_a_returned_release_is_not_judged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_returned_release_is_not_judged_again_and_nobody_is_asked`

Old text:

```
        if genre_gate.returned_by(standing, found.payload):
            return _report(
```

New text:

```
        if False:
            return _report(
```

### `r815-c.J9_a_park_drops_the_jobs_tools`

_parked: keep the job's tools across a park

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-c.json`, row `J9_a_park_drops_the_jobs_tools`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_catalogue_that_refuses_stops_the_run_at_once_and_says_how_many_were_left`
  - `tests/test_label_judge.py::test_a_catalogue_unread_three_times_in_a_row_stops_the_run_and_says_how_many_were_left`
  - `tests/test_label_judge.py::test_three_provider_reads_failing_in_a_row_stop_the_run`

Old text:

```
    _JOB_TOOLS.pop(str(job.job_id), None)
    if isinstance(error, jobs.Parked):
```

New text:

```
    if isinstance(error, jobs.Parked):
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
- Collected: 893 against a baseline of 893
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
- Collected: 893 against a baseline of 893
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
- Collected: 893 against a baseline of 893
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

