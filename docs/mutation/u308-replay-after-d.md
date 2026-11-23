# Mutation table: u308-replay-after-d

Measured by `scripts/mutate.py` on 2026-11-22 22:48 UTC, branch `HEAD` at `7732dbfb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22942 collected. pytest invocations for this batch: 37.

Full baseline: measured by this driver (the battery's verdict was not read: no battery verdict at `.cloud-battery/verdict.json`).

Subset baselines: 34, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `/tmp/claude-0/-home-user-cratekit/5bcab4be-2978-53ef-b3bd-2807d1f5544d/scratchpad/known-failures-plus.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard. 163 row(s) were reused from a prior sidecar and were measured by an earlier process, whose children this run did not watch.

Null control `NULL_CONTROL`: killed 0, collected 22942 against 22942. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r1634.M16_worker_drops_how` | `src/cratekit/label/cli.py` | user | 2 file(s) | 119 | 1 | killed |
| `r261.W2_remedy` | `src/cratekit/label/cli.py` | user | 4 file(s) | 522 | 1 | killed |
| `r261.W3_retryable` | `src/cratekit/label/cli.py` | user | 4 file(s) | 522 | 1 | killed |
| `r290-author.S06_label_call_removed` | `src/cratekit/label/cli.py` | user | 2 file(s) | 208 | 17 | killed |
| `r504-a.A11_boundary_refuses` | `src/cratekit/label/cli.py` | user | 4 file(s) | 551 | 5 | killed |
| `r504-a.A12_boundary_drops_short` | `src/cratekit/label/cli.py` | user | 4 file(s) | 551 | 5 | killed |
| `r515-operator.S14_harvest_no_warning` | `src/cratekit/label/cli.py` | user | 1 file(s) | 82 | 1 | killed |
| `r790-b.L1_guard_counts_held` | `src/cratekit/label/cli.py` | user | 4 file(s) | 332 | 1 | killed |
| `r790-b.L2_round_records_beyond` | `src/cratekit/label/cli.py` | user | 4 file(s) | 332 | 8 | killed |
| `r790-b.L4_bound_is_said` | `src/cratekit/label/cli.py` | user | 4 file(s) | 332 | 1 | killed |
| `u100-b.C10_added_message` | `src/cratekit/label/cli.py` | user | 2 file(s) | 47 | 1 | killed |
| `u100-b.C1_name_accepted` | `src/cratekit/label/cli.py` | user | 2 file(s) | 47 | 1 | killed |
| `u100-b.C2_to_accepted` | `src/cratekit/label/cli.py` | user | 2 file(s) | 47 | 1 | killed |
| `u100-b.C3_outcome_always_ok` | `src/cratekit/label/cli.py` | user | 2 file(s) | 47 | 2 | killed |
| `u100-b.C4_empty_says_nothing` | `src/cratekit/label/cli.py` | user | 2 file(s) | 47 | 1 | killed |
| `u100-b.C5_nameless_unreported` | `src/cratekit/label/cli.py` | user | 2 file(s) | 47 | 1 | killed |
| `u100-b.C6_held_name_hidden` | `src/cratekit/label/cli.py` | user | 2 file(s) | 47 | 1 | killed |
| `u100-b.C7_refused_reads_as_note` | `src/cratekit/label/cli.py` | user | 2 file(s) | 47 | 1 | killed |
| `u100-b.C9_dispatch` | `src/cratekit/label/cli.py` | user | 2 file(s) | 47 | 12 | killed |
| `u100-c.C8_refused_counted_present_after_fix` | `src/cratekit/label/cli.py` | user | 1 file(s) | 16 | 1 | killed |
| `u109-b.B6_message_drops_verb` | `src/cratekit/label/cli.py` | user | 1 file(s) | 82 | 1 | killed |
| `u177.A10_clear_word` | `src/cratekit/label/cli.py` | user | 4 file(s) | 144 | 1 | killed |
| `u177.A11_field_flag_guard` | `src/cratekit/label/cli.py` | user | 4 file(s) | 144 | 7 | killed |
| `u178.G6_fallback_refusal` | `src/cratekit/label/cli.py` | user | 3 file(s) | 284 | 1 | killed |
| `u178.G7_fallback_confirm_ignored` | `src/cratekit/label/cli.py` | user | 3 file(s) | 284 | 1 | killed |
| `u178.G8_clear_word_case` | `src/cratekit/label/cli.py` | user | 3 file(s) | 284 | 1 | killed |
| `u178.G9_accept_without_genre` | `src/cratekit/label/cli.py` | user | 3 file(s) | 284 | 1 | killed |
| `u277.M11_worker_detail_without_canary` | `src/cratekit/label/cli.py` | user | 3 file(s) | 158 | 3 | killed |
| `u277.M12_worker_message_without_canary` | `src/cratekit/label/cli.py` | user | 3 file(s) | 158 | 2 | killed |
| `u52-item-derivation.H4_verification_boundary_gone` | `src/cratekit/label/cli.py` | user | 2 file(s) | 262 | 2 | killed |
| `u52-item-derivation.H6_empty_playlist_reports_ok` | `src/cratekit/label/cli.py` | user | 2 file(s) | 262 | 2 | killed |
| `u52-item-derivation.I5_import_queues_no_item` | `src/cratekit/label/cli.py` | user | 2 file(s) | 262 | 4 | killed |
| `u52-item-derivation.I6_import_item_keyed_on_name` | `src/cratekit/label/cli.py` | user | 2 file(s) | 262 | 2 | killed |
| `u52-item-derivation.R1_itemless_job_drives` | `src/cratekit/label/cli.py` | user | 2 file(s) | 262 | 3 | killed |
| `u99-b.B1_parser_limit_floor` | `src/cratekit/label/cli.py` | user | 3 file(s) | 293 | 1 | killed |
| `u99-b.B9_detail_drops_seeds` | `src/cratekit/label/cli.py` | user | 3 file(s) | 293 | 1 | killed |
| `r1115.G4_name_the_refused_on_the_check` | `src/cratekit/label/go.py` | user | 2 file(s) | 205 | 2 | killed |
| `r1115.G9_resume_no_commands_over_nothing` | `src/cratekit/label/go.py` | user | 2 file(s) | 205 | 1 | killed |
| `r1467.M01_fresh_go_checks_before_gate` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 15 | killed |
| `r1467.M02_resumed_jobs_are_own` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 14 | killed |
| `r1467.M04_resume_tail_checks` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 1 | killed |
| `r1467.M15_beside_keeps_later_jobs` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 2 | killed |
| `r1467.M18_refused_tracks_carried` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 2 | killed |
| `r1467.M25_own_pass_handed_to_beside` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 1 | killed |
| `u108-a.G02_pick_takes_releases` | `src/cratekit/label/go.py` | user | 1 file(s) | 110 | 2 | killed |
| `u108-a.G03_not_now_counted` | `src/cratekit/label/go.py` | user | 1 file(s) | 110 | 1 | killed |
| `u108-a.G06_abort_downloads_nothing` | `src/cratekit/label/go.py` | user | 1 file(s) | 110 | 2 | killed |
| `u108-a.G07_only_accepted_downloaded` | `src/cratekit/label/go.py` | user | 1 file(s) | 110 | 1 | killed |
| `u108-a.G08_already_passed_to_listing` | `src/cratekit/label/go.py` | user | 1 file(s) | 110 | 2 | killed |
| `u108-a.G09_gone_excused` | `src/cratekit/label/go.py` | user | 1 file(s) | 110 | 1 | killed |
| `u108-b.G10_unread_answer_kept` | `src/cratekit/label/go.py` | user | 1 file(s) | 110 | 1 | killed |
| `u108-b.G15_time_pacing_coefficient` | `src/cratekit/label/go.py` | user | 1 file(s) | 110 | 1 | killed |
| `u108-c.G23_job_carries_origin` | `src/cratekit/label/go.py` | user | 1 file(s) | 110 | 64 | killed |
| `u108-d.G11_waited_go_refuses_again` | `src/cratekit/label/go.py` | user | 1 file(s) | 110 | 1 | killed |
| `u108-d.G14_retryable_cause_only_again` | `src/cratekit/label/go.py` | user | 1 file(s) | 110 | 1 | killed |
| `u110-c.C4_go_tail` | `src/cratekit/label/go.py` | user | 2 file(s) | 135 | 2 | killed |
| `u239-composites.M11b_land_only_landed_after_its_test` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 3 | killed |
| `u239.M01_own_needs_apply` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 1 | killed |
| `u239.M04_go_takes_own_on` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 19 | killed |
| `u239.M06_beside_open` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 1 | killed |
| `u239.M09_named_landing` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 4 | killed |
| `u239.M14_ceiling_fresh` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 1 | killed |
| `u239.M15_ceiling_job_id` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 2 | killed |
| `u239.M16_other_stop_step` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 2 | killed |
| `u120.P1_live_plain_attribute` | `src/cratekit/favorites/placement.py` | user | 1 file(s) | 67 | 4 | killed |
| `u120.P2_two_sources_accepted` | `src/cratekit/favorites/placement.py` | user | 1 file(s) | 67 | 2 | killed |
| `u120.P4_into_source_always` | `src/cratekit/favorites/placement.py` | user | 1 file(s) | 67 | 3 | killed |
| `u120.P7_bypass_only_when_absent` | `src/cratekit/favorites/placement.py` | user | 1 file(s) | 67 | 3 | killed |
| `u120.P8_source_name_default` | `src/cratekit/favorites/placement.py` | user | 1 file(s) | 67 | 1 | killed |
| `u145.M2_placement_undated` | `src/cratekit/favorites/placement.py` | user | 2 file(s) | 98 | 21 | killed |
| `u146-b.B15_any_playlist_files` | `src/cratekit/favorites/placement.py` | user | 1 file(s) | 31 | 1 | killed |
| `u153.P3_writes_colours` | `src/cratekit/favorites/placement.py` | user | 2 file(s) | 98 | 4 | killed |
| `u153.P4_identity_pink` | `src/cratekit/favorites/placement.py` | user | 2 file(s) | 98 | 1 | killed |
| `u153.P5_recolour_dedup` | `src/cratekit/favorites/placement.py` | user | 2 file(s) | 98 | 3 | killed |
| `u153.P6_place_pink_guard` | `src/cratekit/favorites/placement.py` | user | 3 file(s) | 117 | 2 | killed |
| `u180.M11_new_month_seated` | `src/cratekit/favorites/placement.py` | user | 5 file(s) | 185 | 6 | killed |
| `u180.M12_new_month_knows_the_source` | `src/cratekit/favorites/placement.py` | user | 5 file(s) | 185 | 5 | killed |
| `u180.M13_never_above_all_favorites` | `src/cratekit/favorites/placement.py` | user | 5 file(s) | 185 | 1 | killed |
| `u180.M7_children_live_only` | `src/cratekit/favorites/placement.py` | user | 2 file(s) | 102 | 3 | killed |
| `u180.M8_slots_lift_shared` | `src/cratekit/favorites/placement.py` | user | 2 file(s) | 102 | 4 | killed |
| `u180.M9_seat_skips_unmoved` | `src/cratekit/favorites/placement.py` | user | 2 file(s) | 102 | 7 | killed |
| `u185.R3_favorites_home` | `src/cratekit/favorites/placement.py` | user | 1 file(s) | 67 | 1 | killed |
| `r1091.K10_available_dropped` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 1 | killed |
| `r1091.K12_periodic_write_off` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 2 | killed |
| `r1091.K13_write_error_raised` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 6 | killed |
| `r1091.K14_unkept_never_cleared` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 1 | killed |
| `r1091.K15_reuse_uncounted` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 3 | killed |
| `r1091.K1_age_never_expires` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 2 | killed |
| `r1091.K2_future_is_fresh` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 1 | killed |
| `r1091.K3_age_boundary` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 1 | killed |
| `r1091.K4_age_coefficient` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 4 | killed |
| `r1091.K6_label_unchecked` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 1 | killed |
| `r1091.K7_gone_shape_unchecked` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 1 | killed |
| `r1091.K8_year_shape_unchecked` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 2 | killed |
| `r1091.K9_track_shape_unchecked` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 1 | killed |
| `u243.L7_kept_read_judged_blind` | `src/cratekit/label/kept_reads.py` | user | 2 file(s) | 74 | 4 | killed |
| `r815-b.J1_one_refusal_ends_the_asking` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 1 | killed |
| `r815-b.J4_a_record_never_holds_on_its_own` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 3 | killed |
| `r815-c.J11_the_scope_reads_the_registry` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 1 | killed |
| `r815-c.J12_a_release_held_and_gone_is_counted_held` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 3 | killed |
| `r815-c.J13_the_refusal_carries_the_counts` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 7 | killed |
| `r815-c.J5_a_recorded_no_word_answer_is_not_asked_again` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 4 | killed |
| `r815-c.J6_a_decided_item_is_not_judged` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 2 | killed |
| `r815-c.J7_a_returned_release_is_not_judged` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 1 | killed |
| `r840-c.C5_the_judging_stamp_is_made_on_the_payload_as_it_stands` | `src/cratekit/label/judge_cli.py` | user | 2 file(s) | 214 | 1 | killed |
| `u217.K11_asked_now_counted_as_reused` | `src/cratekit/label/kept_listing.py` | user | 1 file(s) | 38 | 4 | killed |
| `u217.K12_flush_batch` | `src/cratekit/label/kept_listing.py` | maintainer | 1 file(s) | 38 | 1 | killed |
| `u217.K1_life_boundary` | `src/cratekit/label/kept_listing.py` | user | 1 file(s) | 38 | 1 | killed |
| `u217.K2_future_is_fresh` | `src/cratekit/label/kept_listing.py` | maintainer | 1 file(s) | 38 | 1 | killed |
| `u217.K3_life_coefficient` | `src/cratekit/label/kept_listing.py` | user | 1 file(s) | 38 | 1 | killed |
| `u217.K4_changed_entry` | `src/cratekit/label/kept_listing.py` | user | 1 file(s) | 38 | 2 | killed |
| `u217.K5_seeds_not_asked_for` | `src/cratekit/label/kept_listing.py` | user | 1 file(s) | 38 | 1 | killed |
| `u217.K6_match_not_asked_for` | `src/cratekit/label/kept_listing.py` | user | 1 file(s) | 38 | 1 | killed |
| `u217.K9_release_shape` | `src/cratekit/label/kept_listing.py` | user | 1 file(s) | 38 | 1 | killed |
| `r888.C1_probe_ignores_held` | `src/cratekit/label/crawl.py` | user | 5 file(s) | 578 | 7 | killed |
| `r888.C2_probe_trusts_held` | `src/cratekit/label/crawl.py` | user | 5 file(s) | 578 | 1 | killed |
| `u52-item-derivation.C1_can_list_always_true` | `src/cratekit/label/crawl.py` | user | 1 file(s) | 180 | 1 | killed |
| `u52-item-derivation.C2_can_list_requires_all` | `src/cratekit/label/crawl.py` | user | 1 file(s) | 180 | 3 | killed |
| `r259.L1_job_cache_read` | `src/cratekit/label/cli.py` | maintainer | 4 file(s) | 551 | 1 | killed |
| `r261.W1_worker_refuses` | `src/cratekit/label/cli.py` | user | 4 file(s) | 522 | 2 | killed |
| `r790-b.L3_set_passes_offer` | `src/cratekit/label/cli.py` | user | 4 file(s) | 332 | 1 | killed |
| `u109-b.B4_resume_dropped` | `src/cratekit/label/cli.py` | user | 1 file(s) | 82 | 47 | killed |
| `u109-b.B5_refusal_reason` | `src/cratekit/label/cli.py` | user | 2 file(s) | 1079 | 2 | killed |
| `u109-b.B7_step_drops_verb` | `src/cratekit/label/cli.py` | user | 1 file(s) | 82 | 1 | killed |
| `u109-b.B8_itemless_branch` | `src/cratekit/label/cli.py` | user | 1 file(s) | 82 | 1 | killed |
| `u109-b.B9_queue_again` | `src/cratekit/label/cli.py` | user | 2 file(s) | 1079 | 2 | killed |
| `u177.A9_add_drops_account` | `src/cratekit/label/cli.py` | user | 4 file(s) | 144 | 12 | killed |
| `u52-item-derivation.H2_listing_passthrough_gone` | `src/cratekit/label/cli.py` | user | 2 file(s) | 262 | 1 | killed |
| `u52-item-derivation.H7_unresolved_drops_nameless` | `src/cratekit/label/cli.py` | user | 2 file(s) | 262 | 1 | killed |
| `u52-item-derivation.S1_errors_branch_gone` | `src/cratekit/label/cli.py` | user | 2 file(s) | 262 | 1 | killed |
| `u52-zero-rows.H5_verifier_passthrough_gone` | `src/cratekit/label/cli.py` | user | 2 file(s) | 262 | 1 | killed |
| `u99-b.B5_add_drops_seeds` | `src/cratekit/label/cli.py` | user | 3 file(s) | 293 | 11 | killed |
| `u99-b.B6_add_drops_limit` | `src/cratekit/label/cli.py` | user | 3 file(s) | 293 | 3 | killed |
| `u99-b.B7_set_drops_seeds` | `src/cratekit/label/cli.py` | user | 3 file(s) | 293 | 2 | killed |
| `u99-b.B8_list_json_empty` | `src/cratekit/label/cli.py` | user | 3 file(s) | 293 | 12 | killed |
| `r1115.G10_resume_every_refused_fails` | `src/cratekit/label/go.py` | user | 2 file(s) | 205 | 4 | killed |
| `r1115.G3_warn_each_failed_track` | `src/cratekit/label/go.py` | user | 2 file(s) | 205 | 2 | killed |
| `r1115.G5_every_refused_fails_the_check` | `src/cratekit/label/go.py` | user | 2 file(s) | 205 | 4 | killed |
| `r1115.G6_no_commands_over_nothing` | `src/cratekit/label/go.py` | user | 2 file(s) | 205 | 2 | killed |
| `r1467.M03_fresh_tail_checks_after_drive` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 14 | killed |
| `r1467.M05_carry_on_checks` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 14 | killed |
| `r1467.M14_carry_on_reads_the_record` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 2 | killed |
| `r1467.M17_walk_answers_kept` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 1 | killed |
| `u108-a.G04_digest_covers_releases` | `src/cratekit/label/go.py` | user | 1 file(s) | 110 | 1 | killed |
| `u108-a.G05_digest_covers_resume` | `src/cratekit/label/go.py` | user | 1 file(s) | 22942 | 0 (promoted) | zero |
| `u108-b.G13_closed_job_retried` | `src/cratekit/label/go.py` | user | 1 file(s) | 110 | 1 | killed |
| `u108-b.G17_done_tracks_held` | `src/cratekit/label/go.py` | user | 1 file(s) | 110 | 2 | killed |
| `u108-d.G16_origin_marker_filter_again` | `src/cratekit/label/go.py` | user | 1 file(s) | 110 | 7 | killed |
| `u239.M02_own_skips_cancelled` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 1 | killed |
| `u239.M03_own_job_by_run` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 13 | killed |
| `u239.M05_beside_later_only` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 8 | killed |
| `u239.M08_retry_half_failed` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 1 | killed |
| `u239.M17_wrote` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 1 | killed |
| `u153.P1_into_colour_flag` | `src/cratekit/favorites/placement.py` | user | 3 file(s) | 117 | 11 | killed |
| `r1091.K11_year_dropped` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 1 | killed |
| `r1091.K5_version_unchecked` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 1 | killed |
| `r815-b.J2_an_unread_catalogue_ends_the_run` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 1 | killed |
| `r815-b.J3_a_failing_provider_ends_the_run` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 1 | killed |
| `r815-c.J9_a_park_drops_the_jobs_tools` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 3 | killed |
| `u217.K13_unkept_said` | `src/cratekit/label/kept_reads.py` | user | 1 file(s) | 38 | 1 | killed |
| `u180-m25.M25_read_back_asserted` | `src/cratekit/favorites/spine.py` | user | 1 file(s) | 35 | 1 | killed |
| `u180.M23_in_order_asks_nothing` | `src/cratekit/favorites/spine.py` | user | 2 file(s) | 1032 | 5 | killed |
| `u180.M24_backup_acknowledged_first` | `src/cratekit/favorites/spine.py` | user | 2 file(s) | 1032 | 1 | killed |
| `u119.V1_ack_after_plan` | `src/cratekit/favorites/spine.py` | user | 1 file(s) | 45 | 1 | killed |

## Zero rows and what they owe

- `u108-a.G05_digest_covers_resume` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

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

### `r261.W2_remedy`

The refusal tells the person to resume even when only a missing method is unread

- File: `src/cratekit/label/cli.py`
- Source: `r261.json`, row `W2_remedy`
- Moved: The unread refusal is inline in _refuse_unfinished, one indent deeper; the mutation always names a resume.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/modules/test_labels.py`
- Collected: 522 against a baseline of 522
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_roster_member_missing_one_listing_fails_the_sweep_and_names_it`

Old text:

```
            remedy=Remedy.RESUME_JOB if transient else Remedy.REPORT_DEFECT,

```

New text:

```
            remedy=Remedy.RESUME_JOB,

```

### `r261.W3_retryable`

The refusal is retryable whatever was unread

- File: `src/cratekit/label/cli.py`
- Source: `r261.json`, row `W3_retryable`
- Moved: The unread refusal is inline in _refuse_unfinished, one indent deeper; the mutation makes it always retryable.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/modules/test_labels.py`
- Collected: 522 against a baseline of 522
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_roster_member_missing_one_listing_fails_the_sweep_and_names_it`

Old text:

```
            retryable=transient,

```

New text:

```
            retryable=True,

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

### `r504-a.A11_boundary_refuses`

The verb boundary no longer catches the shortfall, so it is refused as an unreadable listing

- File: `src/cratekit/label/cli.py`
- Source: `r504-a.json`, row `A11_boundary_refuses`
- Moved: the broad translation became catalogue.translated, which lets the shortfall through by its passing tuple to the handler outside it; deleting the handler alone no longer parses, so the shortfall is dropped from passing and the handler left unreachable, which sends it into the broad translation and refuses the listing whole, as deleting the handler did on the base
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_sync_all.py`
- Collected: 551 against a baseline of 551
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`
  - `tests/test_label_tidal_catalogue.py::test_the_verb_boundary_keeps_the_rows_and_hands_back_the_shortfall`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`

Old text:

```
        ), passing=(CratekitError, catalogue.HeartsShortfall)):
            return list(found.favourite_tracks()), None
    except catalogue.HeartsShortfall as short:
        return list(short.rows), short

```

New text:

```
        ), passing=(CratekitError,)):
            return list(found.favourite_tracks()), None
    except ZeroDivisionError as short:
        return list(short.rows), short

```

### `r504-a.A12_boundary_drops_short`

The verb boundary keeps the rows and drops the shortfall, passing the short listing off as the account

- File: `src/cratekit/label/cli.py`
- Source: `r504-a.json`, row `A12_boundary_drops_short`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_sync_all.py`
- Collected: 551 against a baseline of 551
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`
  - `tests/test_label_tidal_catalogue.py::test_the_verb_boundary_keeps_the_rows_and_hands_back_the_shortfall`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`

Old text:

```
        return list(short.rows), short
```

New text:

```
        return list(short.rows), None
```

### `r515-operator.S14_harvest_no_warning`

A harvest over a short playlist carries no warning

- File: `src/cratekit/label/cli.py`
- Source: `r515-operator.json`, row `S14_harvest_no_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_workers.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_harvest_over_a_short_playlist_offers_what_it_read_and_warns`

Old text:

```
        warnings=(harvest_withheld_warning(short, reference),) if short is not None else (),
```

New text:

```
        warnings=(),
```

### `r790-b.L1_guard_counts_held`

_refuse_unfinished: leave held releases out of the confirmed-none count, so a dead verifier reads as nothing new

- File: `src/cratekit/label/cli.py`
- Source: `r790-b.json`, row `L1_guard_counts_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_label_registry_verbs.py`
- Collected: 332 against a baseline of 332
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_dead_verifier_on_a_later_sweep_refuses_rather_than_reporting_nothing_new`

Old text:

```
    unconfirmed = len(source.dropped) + source.held_unconfirmed
```

New text:

```
    unconfirmed = len(source.dropped)
```

### `r790-b.L2_round_records_beyond`

handle: record every round as nothing beyond

- File: `src/cratekit/label/cli.py`
- Source: `r790-b.json`, row `L2_round_records_beyond`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_label_registry_verbs.py`
- Collected: 332 against a baseline of 332
- Kills: 8 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_first_sweep_files_the_default_ten_and_counts_the_other_forty`
  - `tests/test_label_offer_window.py::test_a_label_whose_offer_is_raised_to_thirty_files_thirty`
  - `tests/test_label_offer_window.py::test_a_label_whose_window_is_already_held_records_its_beyond_with_nothing_filed`
  - `tests/test_label_offer_window.py::test_a_round_records_the_most_the_label_could_still_offer`
  - `tests/test_label_offer_window.py::test_a_run_over_two_labels_counts_what_both_left_beyond`
  - `tests/test_label_offer_window.py::test_a_second_sweep_files_only_the_new_release_and_refiles_nothing`
  - `tests/test_label_offer_window.py::test_a_track_limit_below_the_offer_bounds_it_and_the_rest_is_still_counted`
  - `tests/test_label_offer_window.py::test_the_configured_offer_is_the_default_for_every_label`

Old text:

```
                beyond=listing.beyond,
```

New text:

```
                beyond=0,
```

### `r790-b.L4_bound_is_said`

_detail: stop saying the track limit bounds an offer

- File: `src/cratekit/label/cli.py`
- Source: `r790-b.json`, row `L4_bound_is_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_label_registry_verbs.py`
- Collected: 332 against a baseline of 332
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_the_registry_says_when_the_track_limit_bounds_an_offer`

Old text:

```
            + (f", bounded by the track limit to {bound}" if entry.offer > bound else "")
```

New text:

```
            + ""
```

### `u100-b.C10_added_message`

reword the added detail a person reads

- File: `src/cratekit/label/cli.py`
- Source: `u100-b.json`, row `C10_added_message`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`
- Collected: 47 against a baseline of 47
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_a_person_reading_the_default_output_sees_what_was_added`

Old text:

```
        status, detail = "ok", f"{result.name}: added as {result.label_id}"
```

New text:

```
        status, detail = "ok", f"{result.name}: now followed as {result.label_id}"
```

### `u100-b.C1_name_accepted`

adopt no longer refuses a name argument and silently ignores it

- File: `src/cratekit/label/cli.py`
- Source: `u100-b.json`, row `C1_name_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`
- Collected: 47 against a baseline of 47
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_adopt_with_a_name_or_a_field_refuses_and_writes_nothing[name]`

Old text:

```
    if ctx.args.name or ctx.args.new_name is not None:
```

New text:

```
    if ctx.args.new_name is not None:
```

### `u100-b.C2_to_accepted`

adopt no longer refuses --to and silently ignores it

- File: `src/cratekit/label/cli.py`
- Source: `u100-b.json`, row `C2_to_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`
- Collected: 47 against a baseline of 47
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_adopt_with_a_name_or_a_field_refuses_and_writes_nothing[to]`

Old text:

```
    if ctx.args.name or ctx.args.new_name is not None:
```

New text:

```
    if ctx.args.name:
```

### `u100-b.C3_outcome_always_ok`

adopt reports ok when it added nothing

- File: `src/cratekit/label/cli.py`
- Source: `u100-b.json`, row `C3_outcome_always_ok`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`
- Collected: 47 against a baseline of 47
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_an_accepted_label_is_added_once_and_a_second_run_adds_none`
  - `tests/test_label_registry_adopt.py::test_nothing_accepted_writes_nothing_and_says_what_is_waiting`

Old text:

```
        outcome=Outcome.OK if added else Outcome.NO_OP,
```

New text:

```
        outcome=Outcome.OK,
```

### `u100-b.C4_empty_says_nothing`

adopt over a queue with nothing accepted emits no check, so a person reads a blank answer

- File: `src/cratekit/label/cli.py`
- Source: `u100-b.json`, row `C4_empty_says_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`
- Collected: 47 against a baseline of 47
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_nothing_accepted_writes_nothing_and_says_what_is_waiting`

Old text:

```
    if not checks:
        checks.append(
```

New text:

```
    if False:
        checks.append(
```

### `u100-b.C5_nameless_unreported`

adopt drops the failing check for an accepted item that names no label

- File: `src/cratekit/label/cli.py`
- Source: `u100-b.json`, row `C5_nameless_unreported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`
- Collected: 47 against a baseline of 47
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_an_accepted_item_naming_no_label_is_reported_not_skipped`

Old text:

```
        for item_id in found.nameless
```

New text:

```
        for item_id in ()
```

### `u100-b.C6_held_name_hidden`

the already held check no longer names the spelling the label is held under

- File: `src/cratekit/label/cli.py`
- Source: `u100-b.json`, row `C6_held_name_hidden`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`
- Collected: 47 against a baseline of 47
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_a_carried_over_accented_label_is_not_filed_twice`

Old text:

```
        if result.held_name != result.name:
```

New text:

```
        if False:
```

### `u100-b.C7_refused_reads_as_note`

a name that yields no identifier is shown as a note rather than a failure

- File: `src/cratekit/label/cli.py`
- Source: `u100-b.json`, row `C7_refused_reads_as_note`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`
- Collected: 47 against a baseline of 47
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_a_name_with_no_identifier_fails_alone_and_the_rest_land`

Old text:

```
        status = "fail"
        detail = (
```

New text:

```
        status = "info"
        detail = (
```

### `u100-b.C9_dispatch`

the adopt action is never dispatched and falls through to the named actions

- File: `src/cratekit/label/cli.py`
- Source: `u100-b.json`, row `C9_dispatch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`
- Collected: 47 against a baseline of 47
- Kills: 12 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_a_carried_over_accented_label_is_not_filed_twice`
  - `tests/test_label_registry_adopt.py::test_a_label_held_under_a_folded_name_is_reported_not_duplicated[case]`
  - `tests/test_label_registry_adopt.py::test_a_label_held_under_a_folded_name_is_reported_not_duplicated[padding]`
  - `tests/test_label_registry_adopt.py::test_a_label_release_on_the_same_queue_is_not_adopted`
  - `tests/test_label_registry_adopt.py::test_a_name_with_no_identifier_fails_alone_and_the_rest_land`
  - `tests/test_label_registry_adopt.py::test_a_person_reading_the_default_output_sees_what_was_added`
  - `tests/test_label_registry_adopt.py::test_a_rejected_or_open_label_is_not_added`
  - `tests/test_label_registry_adopt.py::test_an_accepted_item_naming_no_label_is_reported_not_skipped`
  - `tests/test_label_registry_adopt.py::test_an_accepted_label_is_added_once_and_a_second_run_adds_none`
  - `tests/test_label_registry_adopt.py::test_an_adopt_that_adds_nothing_does_not_rewrite_the_registry`
  - `tests/test_label_registry_adopt.py::test_nothing_accepted_writes_nothing_and_says_what_is_waiting`
  - `tests/test_label_registry_adopt.py::test_two_spellings_accepted_in_one_run_add_the_label_once`

Old text:

```
    if action == "adopt":
```

New text:

```
    if action == "adopted":
```

### `u100-c.C8_refused_counted_present_after_fix`

the summary lists a refused name as present, telling a script the registry holds it, re-measured after the fix round added its test

- File: `src/cratekit/label/cli.py`
- Source: `u100-c.json`, row `C8_refused_counted_present_after_fix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_adopt.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_a_name_with_no_identifier_fails_alone_and_the_rest_land`

Old text:

```
                    if not result.added and result.refused is None
```

New text:

```
                    if not result.added
```

### `u109-b.B6_message_drops_verb`

Reword the refusal message so it no longer names crate label sync

- File: `src/cratekit/label/cli.py`
- Source: `u109-b.json`, row `B6_message_drops_verb`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_workers.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_sync_labels_refuses_to_queue_and_names_the_guided_verb`

Old text:

```
        f"by label with {GUIDED_VERB}, which asks before it downloads anything",
```

New text:

```
        "by label, asking before anything downloads",
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

### `u178.G6_fallback_refusal`

_declared_genre: never refuse a fallback genre, so Polka is stored unconfirmed

- File: `src/cratekit/label/cli.py`
- Source: `u178.json`, row `G6_fallback_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_label_genre_gate.py`, `tests/test_label_workers.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_genre_routing_only_to_the_fallback_is_refused_and_nothing_is_written`

Old text:

```
    if resolution.match is routing.Match.FALLBACK and not accept_fallback:
```

New text:

```
    if False:
```

### `u178.G7_fallback_confirm_ignored`

_declared_genre: refuse a fallback genre even with --accept-fallback

- File: `src/cratekit/label/cli.py`
- Source: `u178.json`, row `G7_fallback_confirm_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_label_genre_gate.py`, `tests/test_label_workers.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_fallback_genre_is_kept_when_confirmed_and_the_screen_says_it`

Old text:

```
    if resolution.match is routing.Match.FALLBACK and not accept_fallback:
```

New text:

```
    if resolution.match is routing.Match.FALLBACK:
```

### `u178.G8_clear_word_case`

_declared_genre: match the clearing word in its exact case, so --genre Default is stored as a genre

- File: `src/cratekit/label/cli.py`
- Source: `u178.json`, row `G8_clear_word_case`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_label_genre_gate.py`, `tests/test_label_workers.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_the_word_default_clears_a_genre_and_none_keeps_it`

Old text:

```
    if wanted.casefold() == CLEAR_GENRE:
```

New text:

```
    if wanted == CLEAR_GENRE:
```

### `u178.G9_accept_without_genre`

registry_cmd: accept --accept-fallback with no --genre, so it confirms nothing silently

- File: `src/cratekit/label/cli.py`
- Source: `u178.json`, row `G9_accept_without_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_label_genre_gate.py`, `tests/test_label_workers.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_accept_fallback_with_no_genre_is_refused`

Old text:

```
    if accept_fallback and genre is None:
```

New text:

```
    if False:
```

### `u277.M11_worker_detail_without_canary`

the worker's label-sweep-incomplete: leave the canary out of the refusal's detail

- File: `src/cratekit/label/cli.py`
- Source: `u277.json`, row `M11_worker_detail_without_canary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_workers.py`, `tests/test_label_offer_window.py`
- Collected: 158 against a baseline of 158
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_over_held_lines_that_name_the_label`
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_the_worker_refuses_held_lines_naming_another_act_and_names_the_canary`

Old text:

```
                **({"reverified": canaries[0].to_json()} if canaries else {}),
```

New text:

```
                **({}),
```

### `u277.M12_worker_message_without_canary`

the worker's label-sweep-incomplete: leave the canary out of the refusal's message

- File: `src/cratekit/label/cli.py`
- Source: `u277.json`, row `M12_worker_message_without_canary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_workers.py`, `tests/test_label_offer_window.py`
- Collected: 158 against a baseline of 158
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_the_worker_refuses_held_lines_naming_another_act_and_names_the_canary`

Old text:

```
            f"{asked_again}",
```

New text:

```
            f"",
```

### `u52-item-derivation.H4_verification_boundary_gone`

THE THIRD PROVIDER CALL: hand from_tracks the bare seam method, so a provider that went away mid playlist becomes internal-error with report-defect

- File: `src/cratekit/label/cli.py`
- Source: `u52-item-derivation.json`, row `H4_verification_boundary_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 262 against a baseline of 262
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_harvest_that_fails_mid_verification_names_what_it_already_offered`
  - `tests/test_label_workers.py::test_a_provider_that_fails_mid_verification_refuses_rather_than_reporting_a_defect`

Old text:

```
            verify=_label_verifier(found, reference),
```

New text:

```
            verify=found.check_label,
```

### `u52-item-derivation.H6_empty_playlist_reports_ok`

An empty playlist reports OK rather than NO_OP, so nothing found is indistinguishable from something found

- File: `src/cratekit/label/cli.py`
- Source: `u52-item-derivation.json`, row `H6_empty_playlist_reports_ok`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 262 against a baseline of 262
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_workers.py::test_an_empty_harvest_still_names_that_nothing_was_offered`
  - `tests/test_label_workers.py::test_an_empty_playlist_offers_nothing_and_reports_zero_rather_than_refusing`

Old text:

```
        outcome=Outcome.OK if report.offered else Outcome.NO_OP,
```

New text:

```
        outcome=Outcome.OK,
```

### `u52-item-derivation.I5_import_queues_no_item`

THE ZERO ITEM RULE at the import end: queue the single label job with no items at all

- File: `src/cratekit/label/cli.py`
- Source: `u52-item-derivation.json`, row `I5_import_queues_no_item`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 262 against a baseline of 262
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_workers.py::test_an_import_queues_exactly_one_item_and_it_is_the_label_id`
  - `tests/test_label_workers.py::test_an_import_runs_its_one_item_to_done_through_the_same_worker`
  - `tests/test_label_workers.py::test_the_import_queues_without_a_warning_now_an_adapter_is_bound`
  - `tests/test_label_workers.py::test_the_unbound_warning_says_the_job_will_fail_at_the_provider_seam`

Old text:

```
        item_ids=(entry.label_id,),
```

New text:

```
        item_ids=(),
```

### `u52-item-derivation.I6_import_item_keyed_on_name`

The import's single item names the label by display name, which the worker then cannot resolve by id

- File: `src/cratekit/label/cli.py`
- Source: `u52-item-derivation.json`, row `I6_import_item_keyed_on_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 262 against a baseline of 262
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_workers.py::test_an_import_queues_exactly_one_item_and_it_is_the_label_id`
  - `tests/test_label_workers.py::test_an_import_runs_its_one_item_to_done_through_the_same_worker`

Old text:

```
        item_ids=(entry.label_id,),
```

New text:

```
        item_ids=(entry.name,),
```

### `u52-item-derivation.R1_itemless_job_drives`

Drive a label job with no items, which jobs.drive transitions straight to SUCCEEDED over a registry nothing was read from

- File: `src/cratekit/label/cli.py`
- Source: `u52-item-derivation.json`, row `R1_itemless_job_drives`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 262 against a baseline of 262
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_job_carrying_no_items_refuses_on_resume_and_is_left_open`
  - `tests/test_label_workers.py::test_the_itemless_refusal_names_the_cancel_that_gets_a_person_out`
  - `tests/test_label_workers.py::test_the_itemless_refusal_of_an_import_still_says_queue_it_again`

Old text:

```
            _refuse_an_itemless_job(store, job)
```

New text:

```
            pass
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

### `r1115.G4_name_the_refused_on_the_check`

go _downloaded: leave the refused tracks out of the check's words

- File: `src/cratekit/label/go.py`
- Source: `r1115.json`, row `G4_name_the_refused_on_the_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`
- Collected: 205 against a baseline of 205
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_failed_only_by_a_track_refused_for_good_runs_the_tail_on_the_rest`
  - `tests/test_label_sync_go.py::test_a_release_whose_second_track_lands_lossy_runs_the_tail_on_the_first_and_names_it`

Old text:

```
    if read.refused:
        said +=
```

New text:

```
    if False:
        said +=
```

### `r1115.G9_resume_no_commands_over_nothing`

go _resume: name the tail's commands over a resumed download that landed nothing

- File: `src/cratekit/label/go.py`
- Source: `r1115.json`, row `G9_resume_no_commands_over_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`
- Collected: 205 against a baseline of 205
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_resumed_download_whose_every_track_was_refused_runs_no_tail_and_says_so`

Old text:

```
            if isinstance(manifest, str) and manifest and not nothing:
```

New text:

```
            if isinstance(manifest, str) and manifest:
```

### `r1467.M01_fresh_go_checks_before_gate`

go: never refuse before the gate, so a fresh go queues beside a download no landing took and its tail lands both

- File: `src/cratekit/label/go.py`
- Source: `r1467.json`, row `M01_fresh_go_checks_before_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 15 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_of_another_verb_with_its_track_in_the_folder_refuses_the_go`
  - `tests/test_label_sync_go.py::test_a_fresh_go_with_nothing_new_names_an_unlanded_download_rather_than_end_quietly`
  - `tests/test_label_sync_go.py::test_a_go_whose_tracks_were_recorded_in_another_folder_is_not_named_for_this_one`
  - `tests/test_label_sync_go.py::test_a_go_with_tracks_in_the_folder_is_named_once_beside_files_no_download_names`
  - `tests/test_label_sync_go.py::test_a_landing_proof_of_another_pass_proves_nothing`
  - `tests/test_label_sync_go.py::test_a_plain_download_a_tail_renamed_refuses_a_fresh_go_before_its_gate`
  - `tests/test_label_sync_go.py::test_a_plain_download_in_the_folder_refuses_a_fresh_go_before_the_gate`
  - `tests/test_label_sync_go.py::test_a_proven_pass_whose_tracks_are_still_at_their_download_names_is_still_waiting`
  - `tests/test_label_sync_go.py::test_a_retired_intake_file_proves_the_pass`
  - `tests/test_label_sync_go.py::test_a_track_no_download_names_refuses_the_fresh_go_and_only_an_unproven_go_is_named[bridge]`
  - `tests/test_label_sync_go.py::test_a_track_no_download_names_refuses_the_fresh_go_and_only_an_unproven_go_is_named[native]`
  - `tests/test_label_sync_go.py::test_an_earlier_download_the_fresh_go_resumes_is_its_own_and_a_plain_one_is_not`
  - `tests/test_label_sync_go.py::test_an_earlier_go_whose_tail_renamed_its_tracks_at_the_landings_gate_still_refuses`
  - `tests/test_label_sync_go.py::test_an_earlier_gos_download_finished_by_hand_refuses_a_fresh_go_before_it_queues`
  - `tests/test_label_sync_go.py::test_the_walk_refused_beside_a_download_keeps_what_it_answered`

Old text:

```
    if found:
        raise _waiting_refusal(found, staging, walk)
```

New text:

```
    if False:
        raise _waiting_refusal(found, staging, walk)
```

### `r1467.M02_resumed_jobs_are_own`

go: read the jobs a fresh go resumes as beside it, so a go that resumes an earlier download refuses over that download's own tracks

- File: `src/cratekit/label/go.py`
- Source: `r1467.json`, row `M02_resumed_jobs_are_own`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 14 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_that_ended_half_failed_is_retried_by_the_next_go_and_only_its_failures`
  - `tests/test_label_sync_go.py::test_a_download_that_finished_while_a_go_resumed_another_refuses_the_resumes_tail`
  - `tests/test_label_sync_go.py::test_a_fresh_go_that_landed_another_runs_download_records_it_on_that_run`
  - `tests/test_label_sync_go.py::test_a_go_resumed_under_another_run_names_the_run_that_queued_it_to_continue`
  - `tests/test_label_sync_go.py::test_a_go_resuming_an_earlier_download_lands_it_under_that_gos_manifest_and_pass`
  - `tests/test_label_sync_go.py::test_a_go_whose_job_was_cancelled_still_refuses_and_lands_nothing`
  - `tests/test_label_sync_go.py::test_a_go_with_an_earlier_download_to_resume_resumes_it_and_queues_nothing_new`
  - `tests/test_label_sync_go.py::test_a_job_stopped_halfway_resumes_and_downloads_only_the_rest`
  - `tests/test_label_sync_go.py::test_a_landing_another_runs_record_cannot_keep_is_a_warning_and_the_go_still_ends_at_it`
  - `tests/test_label_sync_go.py::test_a_landing_recorded_for_one_download_never_answers_for_the_runs_next_one`
  - `tests/test_label_sync_go.py::test_a_resumed_download_failed_only_by_a_refusal_lands_under_the_first_gos_manifest`
  - `tests/test_label_sync_go.py::test_an_abort_recorded_after_the_stop_is_not_taken_on`
  - `tests/test_label_sync_go.py::test_an_earlier_download_the_fresh_go_resumes_alone_is_asked_about`
  - `tests/test_label_sync_go.py::test_an_earlier_download_the_fresh_go_resumes_is_its_own_and_a_plain_one_is_not`

Old text:

```
found = beside(cfg, store, staging, {job_id for job_id, _left in summary.open_jobs})
```

New text:

```
found = beside(cfg, store, staging, set())
```

### `r1467.M04_resume_tail_checks`

_resume: run a single resume's tail without reading the folder, so a download beside it lands under the resumed go's pass

- File: `src/cratekit/label/go.py`
- Source: `r1467.json`, row `M04_resume_tail_checks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_that_finished_while_a_go_resumed_another_refuses_the_resumes_tail`

Old text:

```
    if land is not None:
        # NOT BESIDE ANOTHER DOWNLOAD
```

New text:

```
    if False:
        # NOT BESIDE ANOTHER DOWNLOAD
```

### `r1467.M15_beside_keeps_later_jobs`

_refuse_beside: leave the later go jobs out of the detail's beside list

- File: `src/cratekit/label/go.py`
- Source: `r1467.json`, row `M15_beside_keeps_later_jobs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_later_go_parked_before_it_downloaded_anything_still_refuses_the_tail`
  - `tests/test_label_sync_go.py::test_a_later_gos_download_in_the_same_folder_refuses_the_tail_and_names_its_commands`

Old text:

```
            "beside": [*known, *(one.job_id for one in extra.waiting)],
```

New text:

```
            "beside": [one.job_id for one in extra.waiting],
```

### `r1467.M18_refused_tracks_carried`

_refuse_beside: drop the tracks refused for good from the tail's refusal

- File: `src/cratekit/label/go.py`
- Source: `r1467.json`, row `M18_refused_tracks_carried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_runs_own_tail_refused_beside_a_download_names_its_tracks_refused_for_good`
  - `tests/test_label_sync_go.py::test_a_tail_refused_beside_a_download_still_names_the_tracks_refused_for_good`

Old text:

```
            "refused": list(refused),
```

New text:

```
            "refused": [],
```

### `r1467.M25_own_pass_handed_to_beside`

_refuse_beside: never hand the go's own pass to beside, so a landed pass's record is still read

- File: `src/cratekit/label/go.py`
- Source: `r1467.json`, row `M25_own_pass_handed_to_beside`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_whose_pass_landed_reads_nothing_by_its_tails_record`

Old text:

```
own_pass=default_name(run_of) if kept else None
```

New text:

```
own_pass=None
```

### `u108-a.G02_pick_takes_releases`

go.summarise: only an all answer takes releases, so a pick's releases are left out of the summary and the download

- File: `src/cratekit/label/go.py`
- Source: `u108-a.json`, row `G02_pick_takes_releases`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`
- Collected: 110 against a baseline of 110
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_release_accepted_by_hand_and_answered_for_by_nobody_is_not_downloaded`
  - `tests/test_label_sync_go.py::test_two_labels_answered_all_and_one_picked_produce_one_summary_and_one_gate`

Old text:

```
        if word in TAKING:
```

New text:

```
        if word == sync_cli.ALL:
```

### `u108-a.G03_not_now_counted`

go.summarise: a not-now answer is not counted in the summary

- File: `src/cratekit/label/go.py`
- Source: `u108-a.json`, row `G03_not_now_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`
- Collected: 110 against a baseline of 110
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_two_labels_answered_all_and_one_picked_produce_one_summary_and_one_gate`

Old text:

```
        elif word == sync_cli.NOT_NOW:
            not_now.setdefault(name)
```

New text:

```
        elif word == sync_cli.NOT_NOW:
            pass
```

### `u108-a.G06_abort_downloads_nothing`

go.go: an abort at the gate goes on to download

- File: `src/cratekit/label/go.py`
- Source: `u108-a.json`, row `G06_abort_downloads_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`
- Collected: 110 against a baseline of 110
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_declined_go_runs_no_tail`
  - `tests/test_label_sync_go.py::test_aborting_at_the_gate_downloads_nothing_and_keeps_the_answers`

Old text:

```
    if option == "abort":
```

New text:

```
    if False:
```

### `u108-a.G07_only_accepted_downloaded`

go.go: a release an answer took is downloaded even after a person cleared it in review

- File: `src/cratekit/label/go.py`
- Source: `u108-a.json`, row `G07_only_accepted_downloaded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`
- Collected: 110 against a baseline of 110
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_release_cleared_after_answering_is_named_and_not_downloaded`

Old text:

```
                    if item is not None and item.verdict is Verdict.ACCEPTED:
```

New text:

```
                    if item is not None:
```

### `u108-a.G08_already_passed_to_listing`

go.go: the tracks an earlier go holds are not passed to the listing, so a second start asks for them again

- File: `src/cratekit/label/go.py`
- Source: `u108-a.json`, row `G08_already_passed_to_listing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`
- Collected: 110 against a baseline of 110
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_killed_between_its_queue_and_its_record_never_asks_for_a_track_twice`
  - `tests/test_label_sync_go.py::test_an_answer_holding_a_release_the_provider_did_not_answer_for_is_kept_for_the_next_go`

Old text:

```
                already=held.tracks,
```

New text:

```
                already=frozenset(),
```

### `u108-a.G09_gone_excused`

go.go: a release gone from the provider refuses the go again when nothing else is listed

- File: `src/cratekit/label/go.py`
- Source: `u108-a.json`, row `G09_gone_excused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`
- Collected: 110 against a baseline of 110
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_release_gone_from_the_provider_does_not_refuse_every_go_after_it`

Old text:

```
                excuse=frozenset({approved_cli.GONE, approved_cli.NO_IDENTIFIER}),
```

New text:

```
                excuse=frozenset(),
```

### `u108-b.G10_unread_answer_kept`

go.go: an answer holding a release the provider did not answer for is settled anyway, so it is never asked for again

- File: `src/cratekit/label/go.py`
- Source: `u108-b.json`, row `G10_unread_answer_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`
- Collected: 110 against a baseline of 110
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_an_answer_holding_a_release_the_provider_did_not_answer_for_is_kept_for_the_next_go`

Old text:

```
            keep=retry,
        )
```

New text:

```
            keep=frozenset(),
        )
```

### `u108-b.G15_time_pacing_coefficient`

Summary.seconds: the pacing delay counted at half its value per track

- File: `src/cratekit/label/go.py`
- Source: `u108-b.json`, row `G15_time_pacing_coefficient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`
- Collected: 110 against a baseline of 110
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_the_estimated_time_is_the_pacing_and_the_transfer_of_the_size`

Old text:

```
        return round(self.tracks * self.pace_s + self.size / TRANSFER_BYTES_PER_SECOND)
```

New text:

```
        return round(self.tracks * self.pace_s / 2 + self.size / TRANSFER_BYTES_PER_SECOND)
```

### `u108-c.G23_job_carries_origin`

go.go: the download job is queued without the go's marker, so no later go knows it holds those tracks

- File: `src/cratekit/label/go.py`
- Source: `u108-c.json`, row `G23_job_carries_origin`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`
- Collected: 110 against a baseline of 110
- Kills: 64 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_failed_only_by_a_track_refused_for_good_runs_the_tail_on_the_rest`
  - `tests/test_label_sync_go.py::test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run`
  - `tests/test_label_sync_go.py::test_a_download_landed_while_the_fresh_go_downloaded_refuses_its_tail`
  - `tests/test_label_sync_go.py::test_a_download_that_ended_half_failed_is_retried_by_the_next_go_and_only_its_failures`
  - `tests/test_label_sync_go.py::test_a_download_that_finished_during_the_tail_is_not_kept_as_the_gos`
  - `tests/test_label_sync_go.py::test_a_download_that_finished_while_a_go_resumed_another_refuses_the_resumes_tail`
  - `tests/test_label_sync_go.py::test_a_download_whose_every_track_failed_for_good_runs_no_tail_and_says_so`
  - `tests/test_label_sync_go.py::test_a_file_under_a_name_the_tail_left_but_not_the_same_file_is_not_the_gos`
  - `tests/test_label_sync_go.py::test_a_fresh_go_that_landed_another_runs_download_records_it_on_that_run`
  - `tests/test_label_sync_go.py::test_a_fresh_go_with_nothing_new_names_an_unlanded_download_rather_than_end_quietly`
  - `tests/test_label_sync_go.py::test_a_go_job_whose_track_was_refused_for_good_is_not_resumed`
  - `tests/test_label_sync_go.py::test_a_go_killed_between_its_queue_and_its_record_never_asks_for_a_track_twice`
  - `tests/test_label_sync_go.py::test_a_go_parked_by_a_rate_limit_names_its_own_go_for_after_the_park`
  - `tests/test_label_sync_go.py::test_a_go_resumed_under_another_run_names_the_run_that_queued_it_to_continue`
  - `tests/test_label_sync_go.py::test_a_go_resuming_an_earlier_download_lands_it_under_that_gos_manifest_and_pass`
  - ... and 49 more, see the JSON sidecar

Old text:

```
                        extra={
                            ORIGIN_KEY: {"run": run_id, "manifest": str(written.manifest_path)},
                            RUN_KEY: run_id,
                        },
```

New text:

```
                        extra={
                            RUN_KEY: run_id,
                        },
```

### `u108-d.G11_waited_go_refuses_again`

go.go: a go that waited for the record's lock while another queued goes on to list and queue

- File: `src/cratekit/label/go.py`
- Source: `u108-d.json`, row `G11_waited_go_refuses_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`
- Collected: 110 against a baseline of 110
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_second_go_that_waited_for_the_first_refuses_rather_than_queue_its_tracks_again`

Old text:

```
        if held.resume:
            raise refuse(
```

New text:

```
        if False:
            raise refuse(
```

### `u108-d.G14_retryable_cause_only_again`

go.resumable: a job whose cause says no retry can succeed is resumed anyway

- File: `src/cratekit/label/go.py`
- Source: `u108-d.json`, row `G14_retryable_cause_only_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`
- Collected: 110 against a baseline of 110
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_job_whose_failures_cannot_succeed_on_a_retry_is_not_resumed`

Old text:

```
    return job.cause is None or job.cause.retryable
```

New text:

```
    return True
```

### `u110-c.C4_go_tail`

The label go tail prints --name RUN again

- File: `src/cratekit/label/go.py`
- Source: `u110-c.json`, row `C4_go_tail`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_names.py`, `tests/test_label_sync_go.py`
- Collected: 135 against a baseline of 135
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_the_label_go_tail_hands_the_run_as_the_pass_and_names_no_batch`
  - `tests/test_label_sync_go.py::test_the_download_lands_as_an_intake_under_the_runs_one_batch`

Old text:

```
"--pass", default_name(run_id)]
```

New text:

```
"--name", default_name(run_id)]
```

### `u239-composites.M11b_land_only_landed_after_its_test`

M11 measured again after its test: name the landing whatever the download read

- File: `src/cratekit/label/go.py`
- Source: `u239-composites.json`, row `M11b_land_only_landed_after_its_test`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_whose_every_track_failed_for_good_runs_no_tail_and_says_so`
  - `tests/test_label_sync_go.py::test_a_go_under_its_run_over_a_download_that_refused_every_track_runs_no_tail`
  - `tests/test_label_sync_go.py::test_a_go_whose_every_track_was_refused_runs_no_tail_and_says_so`

Old text:

```
    if read.landed and manifest is not None:
```

New text:

```
    if manifest is not None:
```

### `u239.M01_own_needs_apply`

_own: take the run's job on whatever answer is recorded, so an abort recorded after the stop downloads and lands

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M01_own_needs_apply`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_an_abort_recorded_after_the_stop_is_not_taken_on`

Old text:

```
    if recorded is None or recorded.option != APPLY:
```

New text:

```
    if recorded is None:
```

### `u239.M04_go_takes_own_on`

go: never take the run's own download on, so the go asks the gate again as before U239

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M04_go_takes_own_on`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 19 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run`
  - `tests/test_label_sync_go.py::test_a_download_that_finished_during_the_tail_is_not_kept_as_the_gos`
  - `tests/test_label_sync_go.py::test_a_file_under_a_name_the_tail_left_but_not_the_same_file_is_not_the_gos`
  - `tests/test_label_sync_go.py::test_a_fresh_go_that_landed_another_runs_download_records_it_on_that_run`
  - `tests/test_label_sync_go.py::test_a_go_stopped_at_the_ceiling_finishes_and_lands_on_the_next_go_under_its_run`
  - `tests/test_label_sync_go.py::test_a_go_that_ran_its_tail_once_names_its_landing_when_run_again`
  - `tests/test_label_sync_go.py::test_a_go_under_its_run_over_a_download_that_refused_every_track_runs_no_tail`
  - `tests/test_label_sync_go.py::test_a_go_whose_job_was_finished_by_hand_lands_on_the_next_go_with_no_new_decision`
  - `tests/test_label_sync_go.py::test_a_go_whose_tail_reached_its_landing_names_that_landing_and_runs_nothing_again`
  - `tests/test_label_sync_go.py::test_a_go_whose_tail_renamed_its_tracks_and_stopped_runs_its_tail_again_under_its_run`
  - `tests/test_label_sync_go.py::test_a_landing_recorded_for_one_download_never_answers_for_the_runs_next_one`
  - `tests/test_label_sync_go.py::test_a_later_go_parked_before_it_downloaded_anything_still_refuses_the_tail`
  - `tests/test_label_sync_go.py::test_a_later_gos_download_in_the_same_folder_refuses_the_tail_and_names_its_commands`
  - `tests/test_label_sync_go.py::test_a_plain_download_into_the_folder_refuses_the_runs_own_tail`
  - `tests/test_label_sync_go.py::test_a_runs_own_tail_refused_beside_a_download_names_its_tracks_refused_for_good`
  - ... and 4 more, see the JSON sidecar

Old text:

```
    if own is not None:
```

New text:

```
    if False:
```

### `u239.M06_beside_open`

_beside: count only a later go job that downloaded, so one parked before any track is ignored

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M06_beside_open`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_later_go_parked_before_it_downloaded_anything_still_refuses_the_tail`

Old text:

```
        if other.is_open() or any(
```

New text:

```
        if any(
```

### `u239.M09_named_landing`

_carry_on: ignore the recorded landing, so the tail runs a second time

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M09_named_landing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_fresh_go_that_landed_another_runs_download_records_it_on_that_run`
  - `tests/test_label_sync_go.py::test_a_go_that_ran_its_tail_once_names_its_landing_when_run_again`
  - `tests/test_label_sync_go.py::test_a_go_whose_tail_reached_its_landing_names_that_landing_and_runs_nothing_again`
  - `tests/test_label_sync_go.py::test_a_walk_under_a_landed_run_that_records_an_answer_is_not_a_no_op`

Old text:

```
        if named:
```

New text:

```
        if False:
```

### `u239.M14_ceiling_fresh`

_carried: drop fresh, so the continue keeps the command line's own --run

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M14_ceiling_fresh`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_resumed_under_another_run_names_the_run_that_queued_it_to_continue`

Old text:

```
        detail.update({"job": job.job_id, "run_id": run, "fresh": True})
```

New text:

```
        detail.update({"job": job.job_id, "run_id": run})
```

### `u239.M15_ceiling_job_id`

_carried: keep job_id on the ceiling cause, so the continue is job resume again

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M15_ceiling_job_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_resumed_under_another_run_names_the_run_that_queued_it_to_continue`
  - `tests/test_label_sync_go.py::test_a_go_stopped_at_the_ceiling_names_its_own_go_to_continue_not_the_job`

Old text:

```
        detail = {key: value for key, value in (cause.detail or {}).items() if key != "job_id"}
```

New text:

```
        detail = dict(cause.detail or {})
```

### `u239.M16_other_stop_step`

_carried: add no step to a park or a retryable failure, so it names no way to the landing

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M16_other_stop_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run`
  - `tests/test_label_sync_go.py::test_a_go_parked_by_a_rate_limit_names_its_own_go_for_after_the_park`

Old text:

```
    if job.state is jobs.JobState.BLOCKED or (
```

New text:

```
    if False and (
```

### `u120.P1_live_plain_attribute`

_live_plain: a folder or a smart playlist counts as plain

- File: `src/cratekit/favorites/placement.py`
- Source: `u120.json`, row `P1_live_plain_attribute`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`
- Collected: 67 against a baseline of 67
- Kills: 4 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_a_smart_playlist_of_the_months_name_is_not_written_to_and_a_plain_one_is_made`
  - `tests/test_favorites_placement.py::test_no_source_or_two_or_the_wrong_kind_refuses_under_u119s_reason[folder]`
  - `tests/test_favorites_placement.py::test_no_source_or_two_or_the_wrong_kind_refuses_under_u119s_reason[smart]`
  - `tests/test_favorites_placement.py::test_the_home_is_the_one_plain_live_source_its_folder_and_the_months_there`

Old text:

```
if int(getattr(row, "Attribute", -1) or 0) == 0 and not rb_writer.node_removed(row)
```

New text:

```
if int(getattr(row, "Attribute", -1) or 0) >= 0 and not rb_writer.node_removed(row)
```

### `u120.P2_two_sources_accepted`

resolve_home: two live sources are accepted and the first chosen

- File: `src/cratekit/favorites/placement.py`
- Source: `u120.json`, row `P2_two_sources_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`
- Collected: 67 against a baseline of 67
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_a_playlist_of_the_sources_name_inside_deadca7s_folder_is_not_a_second_source`
  - `tests/test_favorites_placement.py::test_no_source_or_two_or_the_wrong_kind_refuses_under_u119s_reason[two]`

Old text:

```
    if len(live) != 1:
        count =
```

New text:

```
    if len(live) < 1:
        count =
```

### `u120.P4_into_source_always`

plan_placements: every heart is planned into the source whether it is there or not

- File: `src/cratekit/favorites/placement.py`
- Source: `u120.json`, row `P4_into_source_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`
- Collected: 67 against a baseline of 67
- Kills: 3 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_a_plan_over_a_library_already_placed_writes_nothing`
  - `tests/test_favorites_placement.py::test_the_plan_names_each_uncoloured_heart_for_pink_and_holds_a_coloured_one`
  - `tests/test_favorites_placement.py::test_the_plan_reads_what_each_heart_already_has_and_what_it_would_make`

Old text:

```
                into_source=key not in in_source,
```

New text:

```
                into_source=True,
```

### `u120.P7_bypass_only_when_absent`

place: the source memberships are inserted directly rather than through add_memberships

- File: `src/cratekit/favorites/placement.py`
- Source: `u120.json`, row `P7_bypass_only_when_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`
- Collected: 67 against a baseline of 67
- Kills: 3 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_a_members_marked_removedhip_in_the_month_is_added_again_live`
  - `tests/test_favorites_placement.py::test_place_adds_to_the_source_and_to_each_month_making_an_absent_one`
  - `tests/test_favorites_placement.py::test_placing_the_same_heart_twice_adds_nothing_twice`

Old text:

```
    added_source = len(rb_writer.add_memberships(db, source, ordered))
```

New text:

```
    added_source = 0
    for content_id in ordered:
        db.add_to_playlist(source, content_id)
        added_source += 1
```

### `u120.P8_source_name_default`

source_name: the outbound default is answered whatever the class declares

- File: `src/cratekit/favorites/placement.py`
- Source: `u120.json`, row `P8_source_name_default`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_the_source_is_the_classs_playlist_else_the_outbound_default`

Old text:

```
    if sub is not None and sub.signal_playlist:
        return sub.signal_playlist
    return outbound_source.DEFAULT_FAVORITES_PLAYLIST
```

New text:

```
    del sub
    return outbound_source.DEFAULT_FAVORITES_PLAYLIST
```

### `u145.M2_placement_undated`

plan_placements: every heart is planned into Undated, its date ignored

- File: `src/cratekit/favorites/placement.py`
- Source: `u145.json`, row `M2_placement_undated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_backfill.py`
- Collected: 98 against a baseline of 98
- Kills: 21 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_carried_heart_whose_row_sits_deep_is_placed_now_the_path_rule_is_gone`
  - `tests/test_favorites_backfill.py::test_a_date_the_job_froze_wins_over_the_accounts`
  - `tests/test_favorites_backfill.py::test_a_heart_a_short_listing_did_not_date_is_held_back_not_filed_undated`
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_at_the_root_beside_another_playlist_still_takes_its_month`
  - `tests/test_favorites_backfill.py::test_a_heart_put_back_by_hand_after_a_removal_takes_its_month_and_is_not_taken_back`
  - `tests/test_favorites_backfill.py::test_a_heart_the_landing_placed_without_a_month_takes_it_from_the_backfill`
  - `tests/test_favorites_backfill.py::test_a_heart_two_jobs_carried_is_one_heart_with_the_dated_jobs_date`
  - `tests/test_favorites_backfill.py::test_a_hearts_job_whose_reports_cannot_be_read_is_skipped_and_named`
  - `tests/test_favorites_backfill.py::test_a_listing_with_no_published_count_holds_back_a_heart_it_lacks`
  - `tests/test_favorites_backfill.py::test_a_month_playlist_deleted_between_the_plan_and_the_write_is_another_plan`
  - `tests/test_favorites_backfill.py::test_a_second_run_finds_the_same_hearts_and_writes_nothing`
  - `tests/test_favorites_backfill.py::test_an_owned_heart_in_a_batch_folder_is_placed_beside_a_downloaded_one`
  - `tests/test_favorites_backfill.py::test_an_owned_heart_the_source_system_filed_is_placed_and_one_with_no_row_is_not`
  - `tests/test_favorites_backfill.py::test_owned_hearts_not_in_all_favorites_are_planned_by_month_and_those_taken_back_are_named`
  - `tests/test_favorites_backfill.py::test_the_plan_lists_exactly_the_landed_hearts_and_the_approval_places_them`
  - ... and 6 more, see the JSON sidecar

Old text:

```
        month = placeholders.month_label(hearted)
```

New text:

```
        month = placeholders.month_label(None)
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

### `u153.P3_writes_colours`

PlacementPlan.writes: ignore the colour count, so a colour-only plan reports no write and ends NO_OP

- File: `src/cratekit/favorites/placement.py`
- Source: `u153.json`, row `P3_writes_colours`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_backfill.py`
- Collected: 98 against a baseline of 98
- Kills: 4 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_and_undated_holds_is_not_given_a_month`
  - `tests/test_favorites_backfill.py::test_the_backfill_colours_the_members_placed_before_it_and_holds_a_coloured_one`
  - `tests/test_favorites_placement.py::test_a_recolour_row_takes_pink_and_no_membership`
  - `tests/test_favorites_placement.py::test_the_plan_names_each_uncoloured_heart_for_pink_and_holds_a_coloured_one`

Old text:

```
        return self.adds > 0 or self.colours > 0
```

New text:

```
        return self.adds > 0
```

### `u153.P4_identity_pink`

identity: drop the Pink row from the digest, so a colour change between plan and write is not caught

- File: `src/cratekit/favorites/placement.py`
- Source: `u153.json`, row `P4_identity_pink`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_backfill.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_the_plan_names_each_uncoloured_heart_for_pink_and_holds_a_coloured_one`

Old text:

```
            "pink": self.pink,
```

New text:

```
            "pink": "",
```

### `u153.P5_recolour_dedup`

plan_placements recolour: drop the not-in-seen check, so a heart also named as a recolour is listed twice

- File: `src/cratekit/favorites/placement.py`
- Source: `u153.json`, row `P5_recolour_dedup`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_backfill.py`
- Collected: 98 against a baseline of 98
- Kills: 3 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_at_the_root_beside_another_playlist_still_takes_its_month`
  - `tests/test_favorites_backfill.py::test_a_heart_put_back_by_hand_after_a_removal_takes_its_month_and_is_not_taken_back`
  - `tests/test_favorites_placement.py::test_a_heart_named_as_a_heart_is_not_listed_again_as_a_recolour`

Old text:

```
            if row in titles and row not in seen
```

New text:

```
            if row in titles
```

### `u153.P6_place_pink_guard`

place: colour even with no Pink id, so write_pink blanks a colour by setting it to the empty id

- File: `src/cratekit/favorites/placement.py`
- Source: `u153.json`, row `P6_place_pink_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_backfill.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 117 against a baseline of 117
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_with_no_pink_row_the_plan_places_and_colours_nothing_and_says_why`
  - `tests/test_intake_land_hearts_native.py::test_with_no_pink_row_the_landing_places_the_heart_and_warns`

Old text:

```
    if pink and to_colour:
```

New text:

```
    if to_colour:
```

### `u180.M11_new_month_seated`

month_row: a month made under the folder is left at the end, the behaviour before U180

- File: `src/cratekit/favorites/placement.py`
- Source: `u180.json`, row `M11_new_month_seated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_order.py`, `tests/test_favorites_split.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_favorites_backfill.py`
- Collected: 185 against a baseline of 185
- Kills: 6 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_a_landing_that_makes_a_new_month_puts_it_directly_under_all_favorites`
  - `tests/test_favorites_order.py::test_the_splits_months_land_in_order`
  - `tests/test_favorites_placement.py::test_a_month_is_never_seated_above_all_favorites`
  - `tests/test_favorites_placement.py::test_a_month_made_in_a_folder_out_of_order_lands_above_every_older_month`
  - `tests/test_favorites_placement.py::test_a_removed_sibling_keeps_its_position_when_a_month_is_seated`
  - `tests/test_favorites_placement.py::test_place_makes_a_new_month_directly_under_all_favorites_in_an_ordered_folder`

Old text:

```
    if parent is not None:
        _seat_new(db, made, parent_id, source_id)
```

New text:

```
    if False:
        _seat_new(db, made, parent_id, source_id)
```

### `u180.M12_new_month_knows_the_source`

_seat_new: the month just made is ranked as any other playlist, so it is seated at the end of the folder

- File: `src/cratekit/favorites/placement.py`
- Source: `u180.json`, row `M12_new_month_knows_the_source`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_order.py`, `tests/test_favorites_split.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_favorites_backfill.py`
- Collected: 185 against a baseline of 185
- Kills: 5 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_a_landing_that_makes_a_new_month_puts_it_directly_under_all_favorites`
  - `tests/test_favorites_order.py::test_the_splits_months_land_in_order`
  - `tests/test_favorites_placement.py::test_a_month_made_in_a_folder_out_of_order_lands_above_every_older_month`
  - `tests/test_favorites_placement.py::test_a_removed_sibling_keeps_its_position_when_a_month_is_seated`
  - `tests/test_favorites_placement.py::test_place_makes_a_new_month_directly_under_all_favorites_in_an_ordered_folder`

Old text:

```
    mine = rank(made, source_id)
```

New text:

```
    mine = (placeholders.RANK_OTHER, 0)
```

### `u180.M13_never_above_all_favorites`

_seat_new: the slot is looked for from the top of the folder, so a month can be seated above All Favorites, the round one finding

- File: `src/cratekit/favorites/placement.py`
- Source: `u180.json`, row `M13_never_above_all_favorites`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_order.py`, `tests/test_favorites_split.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_favorites_backfill.py`
- Collected: 185 against a baseline of 185
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_a_month_is_never_seated_above_all_favorites`

Old text:

```
        (n for n, row in enumerate(others) if n >= floor and rank(row, source_id) > mine),
```

New text:

```
        (n for n, row in enumerate(others) if rank(row, source_id) > mine),
```

### `u180.M7_children_live_only`

children: a soft deleted child is read, ranked and moved like a live one

- File: `src/cratekit/favorites/placement.py`
- Source: `u180.json`, row `M7_children_live_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_order.py`
- Collected: 102 against a baseline of 102
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
- Collected: 102 against a baseline of 102
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
- Collected: 102 against a baseline of 102
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

### `u185.R3_favorites_home`

resolve_home: count a playlist of the source's name inside the folder

- File: `src/cratekit/favorites/placement.py`
- Source: `u185.json`, row `R3_favorites_home`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_a_playlist_of_the_sources_name_inside_deadca7s_folder_is_not_a_second_source`

Old text:

```
    live = foreign_tree.outside(
        _live_plain(list(db.get_playlist(Name=name))), list(db.get_playlist())
    )
```

New text:

```
    live = _live_plain(list(db.get_playlist(Name=name)))
```

### `r1091.K10_available_dropped`

_row: keep every track as playable, so a track the provider will not play is asked for from a kept read

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K10_available_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_kept_read_keeps_a_track_the_provider_will_not_play_out_of_the_year`

Old text:

```
        "available": getattr(track, "available", True) is not False,
```

New text:

```
        "available": True,
```

### `r1091.K12_periodic_write_off`

_hold: never write mid run, so a killed build keeps nothing it read

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K12_periodic_write_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_periodic_write_that_fails_does_not_stop_the_read`
  - `tests/test_label_playlists_kept.py::test_reads_are_written_every_flush_and_not_only_at_the_end`

Old text:

```
        if self._since >= FLUSH_EVERY:
```

New text:

```
        if False:
```

### `r1091.K13_write_error_raised`

flush: let a write the filesystem refuses raise, the round 1 blocking finding

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K13_write_error_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_file_where_the_labels_directory_belongs_still_shows_the_plan`
  - `tests/test_label_playlists_kept.py::test_a_periodic_write_that_fails_does_not_stop_the_read`
  - `tests/test_label_playlists_kept.py::test_a_resumed_run_that_cannot_write_says_both_the_reuse_and_the_loss`
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_written_still_shows_the_plan_and_says_so`
  - `tests/test_label_playlists_kept.py::test_a_write_that_succeeds_after_one_failed_clears_what_was_said`
  - `tests/test_label_playlists_kept.py::test_an_abort_after_a_failed_write_still_warns_the_reads_were_not_kept`

Old text:

```
        except OSError as exc:
            self.unkept = f"{type(exc).__name__}: {exc}"
            return
```

New text:

```
        except OSError as exc:
            raise
```

### `r1091.K14_unkept_never_cleared`

flush: leave the failure said after a later write succeeds

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K14_unkept_never_cleared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_write_that_succeeds_after_one_failed_clears_what_was_said`

Old text:

```
        self._unwritten = 0
        self.unkept = ""
```

New text:

```
        self._unwritten = 0
```

### `r1091.K15_reuse_uncounted`

fresh: count no reuse, so the screen says every read was made by this run

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K15_reuse_uncounted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_build_parked_part_way_resumes_and_reads_only_what_it_had_not`
  - `tests/test_label_playlists_kept.py::test_a_read_just_inside_the_age_is_reused_and_named_as_old`
  - `tests/test_label_playlists_kept.py::test_a_resumed_run_that_cannot_write_says_both_the_reuse_and_the_loss`

Old text:

```
        self.reused += 1
```

New text:

```
        self.reused += 0
```

### `r1091.K1_age_never_expires`

_is_fresh: drop the upper bound, so a read is kept for ever and a changed release is planned from old tracks

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K1_age_never_expires`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_read_exactly_the_age_old_is_read_again`
  - `tests/test_label_playlists_kept.py::test_a_read_older_than_the_age_is_read_again`

Old text:

```
        return timedelta(0) <= age < KEPT_FOR
```

New text:

```
        return timedelta(0) <= age
```

### `r1091.K2_future_is_fresh`

_is_fresh: drop the lower bound, so a read dated in the future is kept for as long as the clock is wrong

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K2_future_is_fresh`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_read_dated_in_the_future_is_read_again`

Old text:

```
        return timedelta(0) <= age < KEPT_FOR
```

New text:

```
        return age < KEPT_FOR
```

### `r1091.K3_age_boundary`

_is_fresh: a read exactly the age old is still fresh

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K3_age_boundary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_read_exactly_the_age_old_is_read_again`

Old text:

```
        return timedelta(0) <= age < KEPT_FOR
```

New text:

```
        return timedelta(0) <= age <= KEPT_FOR
```

### `r1091.K4_age_coefficient`

KEPT_FOR: eight days instead of seven, a realistic nearby value

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K4_age_coefficient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_first_build_says_its_reads_are_kept_for_the_apply_run`
  - `tests/test_label_playlists_kept.py::test_a_read_just_inside_the_age_is_reused_and_named_as_old`
  - `tests/test_label_playlists_kept.py::test_the_age_is_seven_days`
  - `tests/test_label_playlists_kept.py::test_the_crawl_gate_counts_the_kept_reads_and_estimates_only_the_rest`

Old text:

```
KEPT_FOR = timedelta(days=7)
```

New text:

```
KEPT_FOR = timedelta(days=8)
```

### `r1091.K6_label_unchecked`

load: read another label's document as this label's reads

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K6_label_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_read_refuses_before_any_release_is_read[{"version": 1, "label_id": "another", "reads": {}}-it names the label]`

Old text:

```
        if raw.get("label_id") != label_id:
```

New text:

```
        if False:
```

### `r1091.K7_gone_shape_unchecked`

_entry: accept a gone flag that is not a bool, so a string reads as gone

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K7_gone_shape_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_read_refuses_before_any_release_is_read[written8-says gone]`

Old text:

```
    if not isinstance(gone, bool):
```

New text:

```
    if False:
```

### `r1091.K8_year_shape_unchecked`

_entry: accept a year of any type, so a string or bool year reaches the plan

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K8_year_shape_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_read_refuses_before_any_release_is_read[written7-carries the year]`
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_read_refuses_before_any_release_is_read[written9-carries the year]`

Old text:

```
    if year is not None and (isinstance(year, bool) or not isinstance(year, int)):
```

New text:

```
    if False:
```

### `r1091.K9_track_shape_unchecked`

_entry: accept a malformed track entry

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K9_track_shape_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_read_refuses_before_any_release_is_read[written6-is malformed]`

Old text:

```
            not isinstance(track, Mapping)
            or not isinstance(track.get("id"), str)
            or not isinstance(track.get("available"), bool)
```

New text:

```
            not isinstance(track, Mapping)
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

### `r840-c.C5_the_judging_stamp_is_made_on_the_payload_as_it_stands`

judge_cli._stamp: keep the fields of the item as it was read before the catalogue was asked, so an artist repaired in that time reads its address again

- File: `src/cratekit/label/judge_cli.py`
- Source: `r840-c.json`, row `C5_the_judging_stamp_is_made_on_the_payload_as_it_stands`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`, `tests/test_label_genre_gate.py`
- Collected: 214 against a baseline of 214
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_judge.py::test_an_artist_put_right_while_a_release_was_being_judged_is_kept_by_the_stamp`

Old text:

```
        kept = {field: value for field, value in current.items() if field not in _STAMP_FIELDS}
```

New text:

```
        kept = {field: value for field, value in item.payload.items() if field not in _STAMP_FIELDS}
```

### `u217.K11_asked_now_counted_as_reused`

_fresh: drop the short circuit for an answer this run asked, so it counts as reused

- File: `src/cratekit/label/kept_listing.py`
- Source: `u217.json`, row `K11_asked_now_counted_as_reused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`
- Collected: 38 against a baseline of 38
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_a_label_entry_that_changed_reads_the_kept_listing_as_empty[changed0]`
  - `tests/test_label_kept_listing.py::test_a_label_entry_that_changed_reads_the_kept_listing_as_empty[changed1]`
  - `tests/test_label_kept_listing.py::test_a_listing_older_than_the_kept_life_is_asked_again`
  - `tests/test_label_kept_listing.py::test_the_first_listing_says_none_was_kept`

Old text:

```
        if (section, key) in self._asked_now:
            return held

```

New text:

```
(empty)
```

### `u217.K12_flush_batch`

_keep: flush at twice the batch, a coefficient

- File: `src/cratekit/label/kept_listing.py`
- Source: `u217.json`, row `K12_flush_batch`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_the_store_writes_every_flush_batch_as_it_goes`

Old text:

```
        if self._since >= FLUSH_EVERY:
```

New text:

```
        if self._since >= FLUSH_EVERY * 2:
```

### `u217.K1_life_boundary`

_young: keep an answer exactly the kept life old, so a seven day old listing still answers

- File: `src/cratekit/label/kept_listing.py`
- Source: `u217.json`, row `K1_life_boundary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_a_listing_older_than_the_kept_life_is_asked_again`

Old text:

```
    return timedelta(0) <= _now() - held.read_at < kept_for()
```

New text:

```
    return timedelta(0) <= _now() - held.read_at <= kept_for()
```

### `u217.K2_future_is_fresh`

_young: drop the lower bound, so an answer from the future is fresh

- File: `src/cratekit/label/kept_listing.py`
- Source: `u217.json`, row `K2_future_is_fresh`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_a_listing_kept_in_the_future_is_not_fresh`

Old text:

```
    return timedelta(0) <= _now() - held.read_at < kept_for()
```

New text:

```
    return _now() - held.read_at < kept_for()
```

### `u217.K3_life_coefficient`

kept_for: double the kept life, the one number shared with R-1091

- File: `src/cratekit/label/kept_listing.py`
- Source: `u217.json`, row `K3_life_coefficient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_a_listing_older_than_the_kept_life_is_asked_again`

Old text:

```
    return kept_reads.KEPT_FOR
```

New text:

```
    return kept_reads.KEPT_FOR * 2
```

### `u217.K4_changed_entry`

load: read a document kept for another name, match or seeds as this label's listing

- File: `src/cratekit/label/kept_listing.py`
- Source: `u217.json`, row `K4_changed_entry`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`
- Collected: 38 against a baseline of 38
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_a_label_entry_that_changed_reads_the_kept_listing_as_empty[changed0]`
  - `tests/test_label_kept_listing.py::test_a_label_entry_that_changed_reads_the_kept_listing_as_empty[changed1]`

Old text:

```
        if dict(raw["asked_for"]) != asked:
```

New text:

```
        if False:
```

### `u217.K5_seeds_not_asked_for`

asked_for: leave the seeds out, so a changed seed list reuses the old roster

- File: `src/cratekit/label/kept_listing.py`
- Source: `u217.json`, row `K5_seeds_not_asked_for`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_a_label_entry_that_changed_reads_the_kept_listing_as_empty[changed1]`

Old text:

```
        "seeds": [str(seed) for seed in entry.seed_artists],
```

New text:

```
        "seeds": [],
```

### `u217.K6_match_not_asked_for`

asked_for: leave the match out, so discovery's answers for another needle are reused

- File: `src/cratekit/label/kept_listing.py`
- Source: `u217.json`, row `K6_match_not_asked_for`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_a_label_entry_that_changed_reads_the_kept_listing_as_empty[changed0]`

Old text:

```
        "match": str(entry.match or ""),
```

New text:

```
        "match": "",
```

### `u217.K9_release_shape`

_valid: accept any list as a kept listing, whatever its releases hold

- File: `src/cratekit/label/kept_listing.py`
- Source: `u217.json`, row `K9_release_shape`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_a_kept_listing_that_cannot_be_read_refuses_before_any_call[written7]`

Old text:

```
    return isinstance(value, list) and all(_valid_release(one) for one in value)
```

New text:

```
    return isinstance(value, list)
```

### `r888.C1_probe_ignores_held`

crawl.can_list: a held roster is probed for paging methods, finds none, and the sweep refuses a readable label

- File: `src/cratekit/label/crawl.py`
- Source: `r888.json`, row `C1_probe_ignores_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 578 against a baseline of 578
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_crawl_that_read_everything_still_succeeds`
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_during_discovery_fails_the_sweep_and_names_the_artist`
  - `tests/test_label_tidal_catalogue.py::test_a_roster_member_missing_one_listing_fails_the_sweep_and_names_it`
  - `tests/test_label_tidal_catalogue.py::test_a_various_compilation_the_credited_artists_do_not_list_is_not_offered`
  - `tests/test_label_tidal_catalogue.py::test_discovery_from_a_copyright_matching_compilation_offers_the_credited_artist`
  - `tests/test_label_tidal_catalogue.py::test_the_crawl_probe_asks_a_held_object_what_it_holds`
  - `tests/test_label_tidal_catalogue.py::test_the_roster_crawls_the_label_page_and_every_seed_through_the_listing`

Old text:

```
    if isinstance(artist, listing.HeldReleases):
        return any(artist.held(method) is not None for method in LISTING_METHODS)

```

New text:

```
(empty)
```

### `r888.C2_probe_trusts_held`

crawl.can_list: a held object holding no listing is read as listable, so its empty read passes as a quiet label

- File: `src/cratekit/label/crawl.py`
- Source: `r888.json`, row `C2_probe_trusts_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 578 against a baseline of 578
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_the_crawl_probe_asks_a_held_object_what_it_holds`

Old text:

```
        return any(artist.held(method) is not None for method in LISTING_METHODS)
```

New text:

```
        return True
```

### `u52-item-derivation.C1_can_list_always_true`

Answer yes for every object, which is what makes the refusal above unreachable from the other side

- File: `src/cratekit/label/crawl.py`
- Source: `u52-item-derivation.json`, row `C1_can_list_always_true`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`
- Collected: 180 against a baseline of 180
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_an_artist_exposing_no_listing_method_raises_rather_than_crawling_nothing`

Old text:

```
    return any(getattr(artist, method, None) is not None for method in LISTING_METHODS)
```

New text:

```
    return True
```

### `u52-item-derivation.C2_can_list_requires_all`

Require EVERY listing method rather than any, so a client exposing one of two is refused instead of half read

- File: `src/cratekit/label/crawl.py`
- Source: `u52-item-derivation.json`, row `C2_can_list_requires_all`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`
- Collected: 180 against a baseline of 180
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_listing_that_cannot_be_paged_raises_instead_of_reporting_empty`
  - `tests/modules/test_labels.py::test_a_provider_error_out_of_the_crawl_is_not_an_empty_catalogue`
  - `tests/modules/test_labels.py::test_one_working_listing_with_no_releases_still_reports_empty`

Old text:

```
    return any(getattr(artist, method, None) is not None for method in LISTING_METHODS)
```

New text:

```
    return all(getattr(artist, method, None) is not None for method in LISTING_METHODS)
```

### `r259.L1_job_cache_read`

The worker never reuses the job's library view, one walk per label

- File: `src/cratekit/label/cli.py`
- Source: `r259.json`, row `L1_job_cache_read`
- Moved: The job library view is kept by the _kept_for helper the asking shares; the mutation hands it a fresh holder each time, so the held view is never read again, one walk per label.
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_sync_all.py`
- Collected: 551 against a baseline of 551
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_sweep_of_two_labels_walks_the_library_once`

Old text:

```
    return lambda: _kept_for(_JOB_LIBRARY, key, lambda: match_cli.library_view(cfg))

```

New text:

```
    return lambda: _kept_for({}, key, lambda: match_cli.library_view(cfg))

```

### `r261.W1_worker_refuses`

The worker returns success over a sweep that left something unread

- File: `src/cratekit/label/cli.py`
- Source: `r261.json`, row `W1_worker_refuses`
- Moved: The _refuse_unread helper had one caller and is now inline under the same unread check; the mutation never raises it.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/modules/test_labels.py`
- Collected: 522 against a baseline of 522
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_during_discovery_fails_the_sweep_and_names_the_artist`
  - `tests/test_label_tidal_catalogue.py::test_a_roster_member_missing_one_listing_fails_the_sweep_and_names_it`

Old text:

```
    if source.unread:
        # A crawl that skipped part of the label
```

New text:

```
    if False:
        # A crawl that skipped part of the label
```

### `r790-b.L3_set_passes_offer`

registry_cmd set: drop --offer on the way to the store, so set reports an edit it never wrote

- File: `src/cratekit/label/cli.py`
- Source: `r790-b.json`, row `L3_set_passes_offer`
- Moved: The offer reaches edit through the shared field mapping; the mutation overrides it with None for the set call alone, so set reports an offer it never wrote.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_label_registry_verbs.py`
- Collected: 332 against a baseline of 332
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_raising_a_label_offer_after_a_sweep_files_the_difference`

Old text:

```
        edited = store.edit(name, seed_artists=seeds, **fields)

```

New text:

```
        edited = store.edit(name, seed_artists=seeds, **{**fields, "offer": None})

```

### `u109-b.B4_resume_dropped`

sync labels refuses even with --job, so a sweep queued before U109 can never run

- File: `src/cratekit/label/cli.py`
- Source: `u109-b.json`, row `B4_resume_dropped`
- Moved: The retired refusal is raised through the module helper _refused, which passes the steps the same way; the mutation drops the resume branch ahead of it as before.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_workers.py`
- Collected: 82 against a baseline of 82
- Kills: 47 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_catalogue_that_cannot_be_listed_fails_the_item_and_the_job`
  - `tests/test_label_workers.py::test_a_job_carrying_no_items_refuses_on_resume_and_is_left_open`
  - `tests/test_label_workers.py::test_a_label_the_registry_no_longer_holds_refuses_rather_than_sweeping_nothing`
  - `tests/test_label_workers.py::test_a_label_verb_will_not_drive_a_job_queued_for_another_verb`
  - `tests/test_label_workers.py::test_a_label_whose_catalogue_the_library_already_holds_offers_nothing`
  - `tests/test_label_workers.py::test_a_label_whose_crawl_listed_nothing_at_all_still_succeeds`
  - `tests/test_label_workers.py::test_a_label_whose_every_release_is_tombstoned_still_succeeds`
  - `tests/test_label_workers.py::test_a_listing_failure_that_is_not_a_rate_limit_stays_permanent`
  - `tests/test_label_workers.py::test_a_mixed_listing_of_tombstoned_and_unconfirmed_releases_is_a_label_with_nothing_new`
  - `tests/test_label_workers.py::test_a_rate_limit_at_every_other_sweep_boundary_is_retryable[artist-resolve]`
  - `tests/test_label_workers.py::test_a_rate_limit_at_every_other_sweep_boundary_is_retryable[listing-probe]`
  - `tests/test_label_workers.py::test_a_rate_limited_listing_fails_its_item_as_retryable_and_the_job_says_resume`
  - `tests/test_label_workers.py::test_a_rate_limited_verification_is_retryable_too`
  - `tests/test_label_workers.py::test_a_refusal_the_artist_lookup_raises_in_kind_keeps_its_own_reason`
  - `tests/test_label_workers.py::test_a_refusal_the_sweep_verifier_raises_in_kind_keeps_its_own_reason`
  - ... and 32 more, see the JSON sidecar

Old text:

```
    if ctx.args.job:
        return _resume(ctx, ctx.args.job)
    raise _refused(
        "verb-retired",

```

New text:

```
    raise _refused(
        "verb-retired",

```

### `u109-b.B5_refusal_reason`

Refuse with the old empty registry slug instead of verb-retired

- File: `src/cratekit/label/cli.py`
- Source: `u109-b.json`, row `B5_refusal_reason`
- Moved: The retired refusal is raised through the module helper _refused rather than refuse with an origin; the mutation swaps the reason as before.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_workers.py`, `tests/test_cli_contract.py`
- Collected: 1079 against a baseline of 1079
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_workers.py::test_sync_labels_refuses_to_queue_and_names_the_guided_verb`
  - `tests/test_label_workers.py::test_the_retired_refusal_reads_nothing_so_a_fresh_install_gets_it_too`

Old text:

```
    raise _refused(
        "verb-retired",

```

New text:

```
    raise _refused(
        "label-registry-empty",

```

### `u109-b.B7_step_drops_verb`

Drop the step that names the guided verb from the retired refusal

- File: `src/cratekit/label/cli.py`
- Source: `u109-b.json`, row `B7_step_drops_verb`
- Moved: The steps are now positional arguments of _refused, one indent shallower than the steps tuple they were in; the mutation drops the step that names the guided verb.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_workers.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_sync_labels_refuses_to_queue_and_names_the_guided_verb`

Old text:

```
        f"take label releases with: {GUIDED_VERB}",
        "a sweep queued before this change still runs with: crate sync labels "

```

New text:

```
        "a sweep queued before this change still runs with: crate sync labels "

```

### `u109-b.B8_itemless_branch`

The itemless refusal tells a sweep job to queue the import again, never naming the guided verb

- File: `src/cratekit/label/cli.py`
- Source: `u109-b.json`, row `B8_itemless_branch`
- Moved: The itemless refusal passes its steps positionally to _refused, so the conditional step sits one indent shallower; the mutation always takes the import branch as before.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_workers.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_the_itemless_refusal_names_the_cancel_that_gets_a_person_out`

Old text:

```
            if job.handler_key == sweep.HANDLER_KEY

```

New text:

```
            if False

```

### `u109-b.B9_queue_again`

The retired verb queues a sweep again: the refusal is replaced by a legacy enqueue over the registry

- File: `src/cratekit/label/cli.py`
- Source: `u109-b.json`, row `B9_queue_again`
- Moved: The retired refusal is raised through the module helper _refused; the mutation inserts the same legacy enqueue over the registry ahead of it.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_workers.py`, `tests/test_cli_contract.py`
- Collected: 1079 against a baseline of 1079
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_refused_sweep_carries_no_warning_because_nothing_was_queued`
  - `tests/test_label_workers.py::test_sync_labels_refuses_to_queue_and_names_the_guided_verb`

Old text:

```
    if ctx.args.job:
        return _resume(ctx, ctx.args.job)
    raise _refused(
        "verb-retired",

```

New text:

```
    if ctx.args.job:
        return _resume(ctx, ctx.args.job)
    held = labels.RegistryStore().load()
    if held.labels:
        return _queue(
            ctx,
            payload={"source_id": "labels", "run_id": ctx.run.run_id},
            item_ids=tuple(entry.label_id for entry in held.labels.values()),
        )
    raise _refused(
        "verb-retired",

```

### `u177.A9_add_drops_account`

registry_cmd add: pass no account to the store, so add --bandcamp is accepted and never written

- File: `src/cratekit/label/cli.py`
- Source: `u177.json`, row `A9_add_drops_account`
- Moved: The fields add and set share are one mapping handed to the store, and the add answer follows the call; the mutation hands add no account, which is the same guard as passing bandcamp=None in the inline call.
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
        label_id = store.add(name, seed_artists=tuple(seeds or ()), **fields)
        return _answer(ctx, store, {"added": label_id}, label_id, route)

```

New text:

```
        label_id = store.add(name, seed_artists=tuple(seeds or ()), **{**fields, "bandcamp": None})
        return _answer(ctx, store, {"added": label_id}, label_id, route)

```

### `u52-item-derivation.H2_listing_passthrough_gone`

REMOVE THE LAYER ALONE: an adapter's own CratekitError refusal is rewritten as an unreadable playlist

- File: `src/cratekit/label/cli.py`
- Source: `u52-item-derivation.json`, row `H2_listing_passthrough_gone`
- Moved: The listing boundary is catalogue.translated, whose passing types (a CratekitError by default) are re-raised unchanged; the mutation passes nothing through at this site alone, so an adapter refusal is rewritten as an unreadable playlist.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 262 against a baseline of 262
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_cratekit_refusal_from_below_is_not_flattened_into_an_unreadable_playlist`

Old text:

```
        detail={"playlist": reference, "kind": type(exc).__name__},
    )):
        playlist = found.playlist_for(reference)

```

New text:

```
        detail={"playlist": reference, "kind": type(exc).__name__},
    ), passing=()):
        playlist = found.playlist_for(reference)

```

### `u52-item-derivation.H7_unresolved_drops_nameless`

Count only the names a catalogue refused, so a playlist whose tracks carry no copyright string at all reports a clean zero unresolved

- File: `src/cratekit/label/cli.py`
- Source: `u52-item-derivation.json`, row `H7_unresolved_drops_nameless`
- Moved: The nameless count now comes back on the harvest report, counted by from_tracks as the closure did, and the sum is inline in the envelope; the mutation counts only the refused names.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 262 against a baseline of 262
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_track_with_no_copyright_string_is_counted_rather_than_dropped_silently`

Old text:

```
            "unresolved": len(report.dropped) + report.nameless,

```

New text:

```
            "unresolved": len(report.dropped),

```

### `u52-item-derivation.S1_errors_branch_gone`

A sweep that could not offer some of the releases it listed exits 0 and reports the job done

- File: `src/cratekit/label/cli.py`
- Source: `u52-item-derivation.json`, row `S1_errors_branch_gone`
- Moved: The errors refusal is raised through the module helper _refused, which adds the same origin; the mutation never raises it.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 262 against a baseline of 262
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_an_increment_that_could_not_offer_every_release_fails_the_item`

Old text:

```
    if result.errors:
        raise _refused(
            "label-sweep-incomplete",

```

New text:

```
    if False:
        raise _refused(
            "label-sweep-incomplete",

```

### `u52-zero-rows.H5_verifier_passthrough_gone`

REMOVE THE LAYER ALONE: the verification boundary swallows an adapter's own refusal into label-playlist-unreadable

- File: `src/cratekit/label/cli.py`
- Source: `u52-zero-rows.json`, row `H5_verifier_passthrough_gone`
- Moved: The verification boundary is catalogue.translated, whose default passing type is CratekitError; the mutation passes nothing through at this site, so an adapter refusal is swallowed into label-playlist-unreadable as before.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 262 against a baseline of 262
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_refusal_the_harvest_verifier_raises_in_kind_keeps_its_own_reason`

Old text:

```
    )):
            verdict = found.check_label(name)

```

New text:

```
    ), passing=()):
            verdict = found.check_label(name)

```

### `u99-b.B5_add_drops_seeds`

registry_cmd add: pass no seeds to the store, so --seed on add is accepted and never written

- File: `src/cratekit/label/cli.py`
- Source: `u99-b.json`, row `B5_add_drops_seeds`
- Moved: The add call now takes the shared field mapping, and its seeds are still passed by keyword; the mutation passes no seeds to add.
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
        label_id = store.add(name, seed_artists=tuple(seeds or ()), **fields)

```

New text:

```
        label_id = store.add(name, seed_artists=(), **fields)

```

### `u99-b.B6_add_drops_limit`

registry_cmd add: pass no track limit to the store, so --track-limit on add is accepted and never written

- File: `src/cratekit/label/cli.py`
- Source: `u99-b.json`, row `B6_add_drops_limit`
- Moved: The track limit reaches add through the shared field mapping; the mutation overrides it with None for the add call alone, so --track-limit on add is never written, as before.
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
        label_id = store.add(name, seed_artists=tuple(seeds or ()), **fields)

```

New text:

```
        label_id = store.add(name, seed_artists=tuple(seeds or ()), **{**fields, "track_limit": None})

```

### `u99-b.B7_set_drops_seeds`

registry_cmd set: pass no seeds to edit, so set --seed reports an edit and writes nothing

- File: `src/cratekit/label/cli.py`
- Source: `u99-b.json`, row `B7_set_drops_seeds`
- Moved: The set call now takes the shared field mapping and passes its seeds by keyword; the mutation passes no seeds to edit.
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
        edited = store.edit(name, seed_artists=seeds, **fields)

```

New text:

```
        edited = store.edit(name, seed_artists=None, **fields)

```

### `u99-b.B8_list_json_empty`

registry_cmd list: report an empty summary.labels, so a reader that is not a person sees no fields

- File: `src/cratekit/label/cli.py`
- Source: `u99-b.json`, row `B8_list_json_empty`
- Moved: The one use of the _labels_json helper is now inline in _answer: a listing reports every held field under labels, and the mutation reports an empty list there as before.
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
        summary["labels"] = [entry.to_json() for entry in held.labels.values()]

```

New text:

```
        summary["labels"] = []

```

### `r1115.G10_resume_every_refused_fails`

go _resume: the resumed check is ok over a resumed download whose every track was refused

- File: `src/cratekit/label/go.py`
- Source: `r1115.json`, row `G10_resume_every_refused_fails`
- Moved: the resumed, downloaded and continued checks are all built by one helper, _driven, whose status line is this one guard
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`
- Collected: 205 against a baseline of 205
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_whose_every_track_failed_for_good_runs_no_tail_and_says_so`
  - `tests/test_label_sync_go.py::test_a_go_under_its_run_over_a_download_that_refused_every_track_runs_no_tail`
  - `tests/test_label_sync_go.py::test_a_go_whose_every_track_was_refused_runs_no_tail_and_says_so`
  - `tests/test_label_sync_go.py::test_a_resumed_download_whose_every_track_was_refused_runs_no_tail_and_says_so`

Old text:

```
    status = "fail" if nothing and read.refused else "ok"
```

New text:

```
    status = "ok"
```

### `r1115.G3_warn_each_failed_track`

go _drive: raise no warning for a track that failed for good

- File: `src/cratekit/label/go.py`
- Source: `r1115.json`, row `G3_warn_each_failed_track`
- Moved: _drive builds the refused warnings as a generator over read.failed; emptying it raises no warning, as the loop did
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`
- Collected: 205 against a baseline of 205
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_failed_only_by_a_track_refused_for_good_runs_the_tail_on_the_rest`
  - `tests/test_label_sync_go.py::test_a_resumed_download_failed_only_by_a_refusal_lands_under_the_first_gos_manifest`

Old text:

```
        for item_id in read.failed

```

New text:

```
        for item_id in ()

```

### `r1115.G5_every_refused_fails_the_check`

go: the downloaded check is ok over a go whose every track was refused

- File: `src/cratekit/label/go.py`
- Source: `r1115.json`, row `G5_every_refused_fails_the_check`
- Moved: the downloaded check of a fresh go is now built by the shared helper _driven, whose status line is this same guard
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`
- Collected: 205 against a baseline of 205
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_whose_every_track_failed_for_good_runs_no_tail_and_says_so`
  - `tests/test_label_sync_go.py::test_a_go_under_its_run_over_a_download_that_refused_every_track_runs_no_tail`
  - `tests/test_label_sync_go.py::test_a_go_whose_every_track_was_refused_runs_no_tail_and_says_so`
  - `tests/test_label_sync_go.py::test_a_resumed_download_whose_every_track_was_refused_runs_no_tail_and_says_so`

Old text:

```
    status = "fail" if nothing and read.refused else "ok"
```

New text:

```
    status = "ok"
```

### `r1115.G6_no_commands_over_nothing`

go: name the tail's commands over a folder nothing landed in

- File: `src/cratekit/label/go.py`
- Source: `r1115.json`, row `G6_no_commands_over_nothing`
- Moved: the fresh go and the carry on name their tail through one helper, _tail_of, whose not nothing test is this guard
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`
- Collected: 205 against a baseline of 205
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_under_its_run_over_a_download_that_refused_every_track_runs_no_tail`
  - `tests/test_label_sync_go.py::test_a_go_whose_every_track_was_refused_runs_no_tail_and_says_so`

Old text:

```
    landed = tail(staging, manifest, run_of) if manifest is not None and not nothing else []
```

New text:

```
    landed = tail(staging, manifest, run_of) if manifest is not None else []
```

### `r1467.M03_fresh_tail_checks_after_drive`

go: run the fresh go's tail without reading the folder after its drive, so a download that finished meanwhile lands with it

- File: `src/cratekit/label/go.py`
- Source: `r1467.json`, row `M03_fresh_tail_checks_after_drive`
- Moved: the fresh go's beside check after its drive is now the one _refuse_beside call in _tail_of
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 14 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_landed_while_the_fresh_go_downloaded_refuses_its_tail`
  - `tests/test_label_sync_go.py::test_a_download_that_finished_during_the_tail_is_not_kept_as_the_gos`
  - `tests/test_label_sync_go.py::test_a_file_under_a_name_the_tail_left_but_not_the_same_file_is_not_the_gos`
  - `tests/test_label_sync_go.py::test_a_go_whose_pass_landed_reads_nothing_by_its_tails_record`
  - `tests/test_label_sync_go.py::test_a_go_whose_tail_ran_still_refuses_a_file_more_than_its_own_renamed`
  - `tests/test_label_sync_go.py::test_a_go_whose_tracks_another_tail_renamed_does_not_read_them_as_its_own`
  - `tests/test_label_sync_go.py::test_a_go_whose_tracks_left_reads_no_file_put_there_since_as_its_own`
  - `tests/test_label_sync_go.py::test_a_later_go_parked_before_it_downloaded_anything_still_refuses_the_tail`
  - `tests/test_label_sync_go.py::test_a_later_gos_download_in_the_same_folder_refuses_the_tail_and_names_its_commands`
  - `tests/test_label_sync_go.py::test_a_plain_download_a_tail_renamed_refuses_the_runs_own_tail`
  - `tests/test_label_sync_go.py::test_a_plain_download_into_the_folder_refuses_the_runs_own_tail`
  - `tests/test_label_sync_go.py::test_a_runs_own_tail_refused_beside_a_download_names_its_tracks_refused_for_good`
  - `tests/test_label_sync_go.py::test_a_tail_refused_beside_a_download_still_names_the_tracks_refused_for_good`
  - `tests/test_label_sync_go.py::test_a_tails_record_that_cannot_be_read_reads_nothing_as_the_gos_own`

Old text:

```
        _refuse_beside(
            cfg, store, job, staging, manifest, run_of, landed, own={job.job_id},
```

New text:

```
        (lambda *_a, **_k: None)(
            cfg, store, job, staging, manifest, run_of, landed, own={job.job_id},
```

### `r1467.M05_carry_on_checks`

_carry_on: run the run's own tail without reading the folder, so a plain download beside it lands under its pass

- File: `src/cratekit/label/go.py`
- Source: `r1467.json`, row `M05_carry_on_checks`
- Moved: the carry on's beside check moved into _tail_of, which the carry on calls; the same read.landed test guards it
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 14 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_landed_while_the_fresh_go_downloaded_refuses_its_tail`
  - `tests/test_label_sync_go.py::test_a_download_that_finished_during_the_tail_is_not_kept_as_the_gos`
  - `tests/test_label_sync_go.py::test_a_file_under_a_name_the_tail_left_but_not_the_same_file_is_not_the_gos`
  - `tests/test_label_sync_go.py::test_a_go_whose_pass_landed_reads_nothing_by_its_tails_record`
  - `tests/test_label_sync_go.py::test_a_go_whose_tail_ran_still_refuses_a_file_more_than_its_own_renamed`
  - `tests/test_label_sync_go.py::test_a_go_whose_tracks_another_tail_renamed_does_not_read_them_as_its_own`
  - `tests/test_label_sync_go.py::test_a_go_whose_tracks_left_reads_no_file_put_there_since_as_its_own`
  - `tests/test_label_sync_go.py::test_a_later_go_parked_before_it_downloaded_anything_still_refuses_the_tail`
  - `tests/test_label_sync_go.py::test_a_later_gos_download_in_the_same_folder_refuses_the_tail_and_names_its_commands`
  - `tests/test_label_sync_go.py::test_a_plain_download_a_tail_renamed_refuses_the_runs_own_tail`
  - `tests/test_label_sync_go.py::test_a_plain_download_into_the_folder_refuses_the_runs_own_tail`
  - `tests/test_label_sync_go.py::test_a_runs_own_tail_refused_beside_a_download_names_its_tracks_refused_for_good`
  - `tests/test_label_sync_go.py::test_a_tail_refused_beside_a_download_still_names_the_tracks_refused_for_good`
  - `tests/test_label_sync_go.py::test_a_tails_record_that_cannot_be_read_reads_nothing_as_the_gos_own`

Old text:

```
    if read.landed:
        _refuse_beside(
```

New text:

```
    if False:
        _refuse_beside(
```

### `r1467.M14_carry_on_reads_the_record`

_carry_on: never read what the run's own tail left, so its renamed tracks refuse its own go

- File: `src/cratekit/label/go.py`
- Source: `r1467.json`, row `M14_carry_on_reads_the_record`
- Moved: the carry on asks _tail_of with own_tail, which reads what its own tail left; dropping the read is the same mutant
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_file_under_a_name_the_tail_left_but_not_the_same_file_is_not_the_gos`
  - `tests/test_label_sync_go.py::test_a_go_whose_tail_renamed_its_tracks_and_stopped_runs_its_tail_again_under_its_run`

Old text:

```
            kept=kept_tail(cfg, job.job_id) if own_tail else frozenset(), refused=read.refused,
```

New text:

```
            kept=frozenset(), refused=read.refused,
```

### `r1467.M17_walk_answers_kept`

_waiting_refusal: drop what the walk answered from the refusal

- File: `src/cratekit/label/go.py`
- Source: `r1467.json`, row `M17_walk_answers_kept`
- Moved: the walk answers are now merged into the detail from this local; an empty one drops them as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_the_walk_refused_beside_a_download_keeps_what_it_answered`

Old text:

```
    answered = {"answered_this_run": list(walk)} if walk is not None else {}
```

New text:

```
    answered = {}
```

### `u108-a.G04_digest_covers_releases`

Summary.plan: the digest leaves out the releases, so an answer saved after the decision does not make it stale

- File: `src/cratekit/label/go.py`
- Source: `u108-a.json`, row `G04_digest_covers_releases`
- Moved: the digest literal is now opened on the digest_of line, so the same key stands four spaces shallower
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`
- Collected: 110 against a baseline of 110
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_an_answer_saved_after_the_decision_makes_the_decision_stale`

Old text:

```
                "releases": [[one.label_id, one.identity] for one in self.taken],
```

New text:

```
                "releases": [],
```

### `u108-a.G05_digest_covers_resume`

Summary.plan: the digest leaves out the jobs a go would resume

- File: `src/cratekit/label/go.py`
- Source: `u108-a.json`, row `G05_digest_covers_resume`
- Moved: the digest literal is now opened on the digest_of line, so the same key stands shallower and closes with it
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`
- Collected: 22942 against a baseline of 22942
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                "resume": [job_id for job_id, _left in self.open_jobs],
            }),
```

New text:

```
                "resume": [],
            }),
```

### `u108-b.G13_closed_job_retried`

go._resume: a job that ended half failed is driven without being re-armed, so its failed tracks are never asked for again

- File: `src/cratekit/label/go.py`
- Source: `u108-b.json`, row `G13_closed_job_retried`
- Moved: the once used job local of _resume was inlined, so the re-arm turns on the same is_open read
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`
- Collected: 110 against a baseline of 110
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_that_ended_half_failed_is_retried_by_the_next_go_and_only_its_failures`

Old text:

```
            if not jobs.get(store, job_id).is_open():
                # STOPPED BY A SIGNAL
```

New text:

```
            if False:
                # STOPPED BY A SIGNAL
```

### `u108-b.G17_done_tracks_held`

go.held_by_goes: a track a finished go job downloaded is not held, so a later go asks for it again

- File: `src/cratekit/label/go.py`
- Source: `u108-b.json`, row `G17_done_tracks_held`
- Moved: held_by_goes adds the held tracks with one update over a generator; its filter is the same done or resumed test
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`
- Collected: 110 against a baseline of 110
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_killed_between_its_queue_and_its_record_never_asks_for_a_track_twice`
  - `tests/test_label_sync_go.py::test_an_answer_holding_a_release_the_provider_did_not_answer_for_is_kept_for_the_next_go`

Old text:

```
        tracks.update(item.item_id for item in items if item.state is jobs.ItemState.DONE or (
            again and item.state is not jobs.ItemState.SKIPPED
        ))
```

New text:

```
        tracks.update(item.item_id for item in items if (
            again and item.state is not jobs.ItemState.SKIPPED
        ))
```

### `u108-d.G16_origin_marker_filter_again`

go.held_by_goes: every acquire download job counts as a go's, so a download queued by hand is resumed and its tracks held by the go

- File: `src/cratekit/label/go.py`
- Source: `u108-d.json`, row `G16_origin_marker_filter_again`
- Moved: held_by_goes now asks _goes_job whether a job is a go's; the origin marker test moved there unchanged
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`
- Collected: 110 against a baseline of 110
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_queued_by_hand_is_not_resumed_or_held_by_a_go`
  - `tests/test_label_sync_go.py::test_a_download_that_finished_during_the_tail_is_not_kept_as_the_gos`
  - `tests/test_label_sync_go.py::test_a_go_whose_tracks_left_reads_no_file_put_there_since_as_its_own`
  - `tests/test_label_sync_go.py::test_a_plain_download_a_tail_renamed_refuses_the_runs_own_tail`
  - `tests/test_label_sync_go.py::test_a_plain_download_already_landed_refuses_nothing`
  - `tests/test_label_sync_go.py::test_a_plain_download_into_the_folder_refuses_the_runs_own_tail`
  - `tests/test_label_sync_go.py::test_a_runs_own_tail_refused_beside_a_download_names_its_tracks_refused_for_good`

Old text:

```
    return job.handler_key == DOWNLOAD and isinstance((job.payload or {}).get(ORIGIN_KEY), Mapping)
```

New text:

```
    return job.handler_key == DOWNLOAD
```

### `u239.M02_own_skips_cancelled`

_own: take a cancelled job on too, so a person's cancel is resumed and landed with no question

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M02_own_skips_cancelled`
- Moved: _own returns through one conditional; the cancelled test is the same clause of it
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_whose_job_was_cancelled_still_refuses_and_lands_nothing`

Old text:

```
    return None if job is None or job.state is jobs.JobState.CANCELLED else job.job_id
```

New text:

```
    return None if job is None else job.job_id
```

### `u239.M03_own_job_by_run`

own_job: take any go job on, not only the one this run's go queued

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M03_own_job_by_run`
- Moved: own_job asks _goes_job for the origin marker; the run match is the same comparison after it
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 13 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_killed_between_its_queue_and_its_record_never_asks_for_a_track_twice`
  - `tests/test_label_sync_go.py::test_a_go_with_an_earlier_download_to_resume_resumes_it_and_queues_nothing_new`
  - `tests/test_label_sync_go.py::test_a_job_stopped_halfway_resumes_and_downloads_only_the_rest`
  - `tests/test_label_sync_go.py::test_a_landing_recorded_for_one_download_never_answers_for_the_runs_next_one`
  - `tests/test_label_sync_go.py::test_a_later_go_parked_before_it_downloaded_anything_still_refuses_the_tail`
  - `tests/test_label_sync_go.py::test_a_later_gos_download_in_the_same_folder_refuses_the_tail_and_names_its_commands`
  - `tests/test_label_sync_go.py::test_a_resumed_download_whose_every_track_was_refused_runs_no_tail_and_says_so`
  - `tests/test_label_sync_go.py::test_a_second_go_that_waited_for_the_first_refuses_rather_than_queue_its_tracks_again`
  - `tests/test_label_sync_go.py::test_an_answer_holding_a_release_the_provider_did_not_answer_for_is_kept_for_the_next_go`
  - `tests/test_label_sync_go.py::test_an_earlier_gos_download_once_landed_lets_the_fresh_go_ask_and_download[bridge]`
  - `tests/test_label_sync_go.py::test_an_earlier_gos_download_once_landed_lets_the_fresh_go_ask_and_download[native]`
  - `tests/test_label_sync_go.py::test_an_earlier_gos_landed_download_does_not_refuse_a_later_runs_tail`
  - `tests/test_label_sync_go.py::test_answers_saved_beside_a_finished_go_wait_and_are_not_landed_with_it`

Old text:

```
        if _goes_job(job) and job.payload[ORIGIN_KEY].get("run") == run_id:
```

New text:

```
        if _goes_job(job) and True:
```

### `u239.M05_beside_later_only`

_beside: count earlier go jobs too, so a later run's tail is refused over an earlier landed go

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M05_beside_later_only`
- Moved: _beside folds its two skips into one test; the earlier job clause is the same comparison
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 8 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_with_an_earlier_download_to_resume_resumes_it_and_queues_nothing_new`
  - `tests/test_label_sync_go.py::test_a_landing_recorded_for_one_download_never_answers_for_the_runs_next_one`
  - `tests/test_label_sync_go.py::test_a_later_gos_download_in_the_same_folder_refuses_the_tail_and_names_its_commands`
  - `tests/test_label_sync_go.py::test_an_answer_holding_a_release_the_provider_did_not_answer_for_is_kept_for_the_next_go`
  - `tests/test_label_sync_go.py::test_an_earlier_gos_download_once_landed_lets_the_fresh_go_ask_and_download[bridge]`
  - `tests/test_label_sync_go.py::test_an_earlier_gos_download_once_landed_lets_the_fresh_go_ask_and_download[native]`
  - `tests/test_label_sync_go.py::test_an_earlier_gos_landed_download_does_not_refuse_a_later_runs_tail`
  - `tests/test_label_sync_go.py::test_answers_saved_beside_a_finished_go_wait_and_are_not_landed_with_it`

Old text:

```
        if other.job_id == job.job_id or other.created < job.created or not _goes_job(other):
```

New text:

```
        if other.job_id == job.job_id or not _goes_job(other):
```

### `u239.M08_retry_half_failed`

_carry_on: never re-arm a half failed own job, so a transient failure ends every go under the run

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M08_retry_half_failed`
- Moved: _carry_on reads the job's items once, so the left count is passed inline to the same resumable test
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run`

Old text:

```
        if not job.is_open() and resumable(job, _left(items)):
```

New text:

```
        if False:
```

### `u239.M17_wrote`

_carry_on: a walk that wrote answers under a landed run reports no_op

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M17_wrote`
- Moved: the named landing branch of _carry_on returns through the shared _ended helper with the same wrote outcome
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_walk_under_a_landed_run_that_records_an_answer_is_not_a_no_op`

Old text:

```
            return _ended(ctx, checks, report, Outcome.OK if wrote else Outcome.NO_OP)
        items
```

New text:

```
            return _ended(ctx, checks, report, Outcome.NO_OP)
        items
```

### `u153.P1_into_colour_flag`

plan_placements: never mark a placement for colour, so no heart takes Pink

- File: `src/cratekit/favorites/placement.py`
- Source: `u153.json`, row `P1_into_colour_flag`
- Moved: The placements are rebuilt with dataclasses.replace rather than field by field; the same into_colour flag from the rows the colour read says take Pink, set False the same way.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_backfill.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 117 against a baseline of 117
- Kills: 11 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_the_author_took_out_of_all_favorites_is_never_put_back`
  - `tests/test_favorites_backfill.py::test_a_member_coloured_by_hand_between_the_two_acts_is_refused_by_the_write`
  - `tests/test_favorites_backfill.py::test_a_second_run_finds_the_same_hearts_and_writes_nothing`
  - `tests/test_favorites_backfill.py::test_an_unreadable_account_refuses_only_when_a_heart_needs_placing`
  - `tests/test_favorites_backfill.py::test_owned_hearts_not_in_all_favorites_are_planned_by_month_and_those_taken_back_are_named`
  - `tests/test_favorites_backfill.py::test_the_backfill_colours_the_members_placed_before_it_and_holds_a_coloured_one`
  - `tests/test_favorites_placement.py::test_a_heart_named_as_a_heart_is_not_listed_again_as_a_recolour`
  - `tests/test_favorites_placement.py::test_a_row_coloured_by_hand_between_two_plans_moves_the_digest`
  - `tests/test_favorites_placement.py::test_the_plan_names_each_uncoloured_heart_for_pink_and_holds_a_coloured_one`
  - `tests/test_favorites_placement.py::test_the_write_colours_the_planned_rows_and_only_those`
  - `tests/test_favorites_placement.py::test_the_write_leaves_a_row_coloured_by_hand_after_the_plan`

Old text:

```
replace(one, into_colour=one.content_id in takes)
```

New text:

```
replace(one, into_colour=False)
```

### `r1091.K11_year_dropped`

keep: store no year, so a release the provider dates is planned under its listed year from a kept read

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K11_year_dropped`
- Moved: The same stated year kept on a release read; the Kept is now built on one line with its tracks named first, so the year keyword sits inside the _hold call rather than on a line of its own.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_kept_read_keeps_the_year_the_provider_stated_over_the_listed_one`

Old text:

```
        self._hold(release_id, Kept(read_at=clock(), gone=False, tracks=tracks, year=stated))
```

New text:

```
        self._hold(release_id, Kept(read_at=clock(), gone=False, tracks=tracks, year=None))
```

### `r1091.K5_version_unchecked`

load: read a document of another version as if it were this one

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K5_version_unchecked`
- Moved: the same version check, now in the shared store's header read, compared against the store's own version, which is still 1
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_read_refuses_before_any_release_is_read[{"version": 99, "label_id": "kompakt", "reads": {}}-it says version 99]`

Old text:

```
        if version != cls.version:
```

New text:

```
        if False:
```

### `r815-b.J2_an_unread_catalogue_ends_the_run`

_asked: never stop on the gate's bound of unread releases

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-b.json`, row `J2_an_unread_catalogue_ends_the_run`
- Moved: _asked raises the refused and the given up stops through one refusal; the given up clause is this guard
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_catalogue_unread_three_times_in_a_row_stops_the_run_and_says_how_many_were_left`

Old text:

```
    if tools.refused is not None or tools.asking.given_up:
```

New text:

```
    if tools.refused is not None or False:
```

### `r815-b.J3_a_failing_provider_ends_the_run`

_asked: never stop on the reader's bound of failed reads

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-b.json`, row `J3_a_failing_provider_ends_the_run`
- Moved: the refusal is raised through _refuse, refuse with this module's origin bound, behind the same guard
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
        raise _refuse(
```

New text:

```
    if False:
        raise _refuse(
```

### `r815-c.J9_a_park_drops_the_jobs_tools`

_parked: keep the job's tools across a park

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-c.json`, row `J9_a_park_drops_the_jobs_tools`
- Moved: _parked returns through one conditional after the same pop of the job tools
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
    return error if
```

New text:

```
    return error if
```

### `u217.K13_unkept_said`

flush: swallow a refused write without saying it

- File: `src/cratekit/label/kept_reads.py`
- Source: `u217.json`, row `K13_unkept_said`
- Moved: the kept listing's flush and the kept reads' flush were the same code and are now one, kept_reads._Store.flush, which KeptListing inherits; the same line that records a refused write
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_a_write_the_filesystem_refuses_is_said_and_the_listing_still_made`

Old text:

```
            self.unkept = f"{type(exc).__name__}: {exc}"
```

New text:

```
            self.unkept = ""
```

### `u180-m25.M25_read_back_asserted`

favorites_order: a read back that disagrees with the plan is not refused, measured again once a test drove the verb's refusal

- File: `src/cratekit/favorites/spine.py`
- Source: `u180-m25.json`, row `M25_read_back_asserted`
- Moved: The verb's read back refusal moved into spine.run, which calls the engine's assert_read_back on the write's result; for the order verb that engine is favorites.order.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_the_verb_refuses_an_answer_the_read_back_does_not_hold`

Old text:

```
    engine.assert_read_back(result)
```

New text:

```
    pass
```

### `u180.M23_in_order_asks_nothing`

favorites_order: a folder already in order opens the gate rather than ending NO_OP

- File: `src/cratekit/favorites/spine.py`
- Source: `u180.json`, row `M23_in_order_asks_nothing`
- Moved: The order verb's nothing to write check before the gate is spine.run's first check, taken for every verb that does not ask the gate first; disabling it opens a gate over a folder already in order.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`, `tests/test_cli_contract.py`
- Collected: 1032 against a baseline of 1032
- Kills: 5 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[favorites.order]`
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[favorites.split]`
  - `tests/test_favorites_order.py::test_a_folder_already_in_order_plans_no_writes_and_opens_no_gate`
  - `tests/test_favorites_order.py::test_a_landing_that_makes_a_new_month_puts_it_directly_under_all_favorites`
  - `tests/test_favorites_order.py::test_a_second_run_after_the_order_asks_nothing`

Old text:

```
    if not (gate_first or plan.writes):
```

New text:

```
    if False:
```

### `u180.M24_backup_acknowledged_first`

favorites_order: the backup acknowledgment is not read before the plan and the gate

- File: `src/cratekit/favorites/spine.py`
- Source: `u180.json`, row `M24_backup_acknowledged_first`
- Moved: the four favourites verbs share one body, spine.run, which reads the acknowledgment before the plan; order_cli calls it, so this is the same line for the order verb
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`, `tests/test_cli_contract.py`
- Collected: 1032 against a baseline of 1032
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    session.assert_backup_acknowledged(cfg)

    plan = planned()
```

New text:

```
    plan = planned()
```

### `u119.V1_ack_after_plan`

favorites_refresh: the backup acknowledgment is not read before the gate

- File: `src/cratekit/favorites/spine.py`
- Source: `u119.json`, row `V1_ack_after_plan`
- Moved: The refresh verb runs through spine.run, which reads the backup acknowledgment before it builds the plan; the same line ahead of the plan, removed the same way.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 45 against a baseline of 45
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    session.assert_backup_acknowledged(cfg)

    plan = planned()
```

New text:

```
    plan = planned()
```

