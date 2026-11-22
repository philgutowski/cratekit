# Mutation table: u301-replay-after

Measured by `scripts/mutate.py` on 2026-11-22 21:45 UTC, branch `cloud/858-rest-of-core` at `9781ec04`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22918 collected. pytest invocations for this batch: 78.

Full baseline: measured by this driver (the battery's verdict was not read: no battery verdict at `.cloud-battery/verdict.json`).

Subset baselines: 76, each measured by this driver.

Known failures: 249 node ids whose failure is this machine's and not the tree's, read from `/home/user/cratekit/.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard. 324 row(s) were reused from a prior sidecar and were measured by an earlier process, whose children this run did not watch.

Null control `NULL_CONTROL`: killed 0, collected 22918 against 22918. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u260.D1_decodes_always` | `src/cratekit/core/art.py` | user | 4 file(s) | 269 | 2 | killed |
| `u260.E10_encode_memory_unbounded` | `src/cratekit/core/art.py` | maintainer | 4 file(s) | 269 | 1 | killed |
| `u260.E11_reset_forgets_nothing` | `src/cratekit/core/art.py` | maintainer | 4 file(s) | 269 | 13 | killed |
| `u260.E12_key_digest_of_64_kb` | `src/cratekit/core/art.py` | user | 4 file(s) | 269 | 1 | killed |
| `u260.E2_key_drops_size` | `src/cratekit/core/art.py` | user | 4 file(s) | 269 | 1 | killed |
| `u260.E3_key_drops_cap` | `src/cratekit/core/art.py` | user | 4 file(s) | 269 | 1 | killed |
| `u260.E4_key_by_length_only` | `src/cratekit/core/art.py` | user | 4 file(s) | 269 | 2 | killed |
| `u260.E5_key_digest_of_a_prefix` | `src/cratekit/core/art.py` | user | 4 file(s) | 269 | 1 | killed |
| `u260.E6_encode_never_remembered` | `src/cratekit/core/art.py` | user | 4 file(s) | 269 | 11 | killed |
| `u260.E7_encode_bound_off_by_one` | `src/cratekit/core/art.py` | maintainer | 4 file(s) | 269 | 1 | killed |
| `u260.E8_encode_hit_not_refreshed` | `src/cratekit/core/art.py` | maintainer | 4 file(s) | 269 | 1 | killed |
| `u260.E9_encode_evicts_newest` | `src/cratekit/core/art.py` | maintainer | 4 file(s) | 269 | 1 | killed |
| `u83-a.E10_reported_dimensions` | `src/cratekit/core/art.py` | maintainer | 1 file(s) | 73 | 1 | killed |
| `u83-a.E1_baseline_flag` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 3 | killed |
| `u83-a.E2_quality_floor` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 1 | killed |
| `u83-a.E3_ladder_ends_on_floor` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 1 | killed |
| `u83-a.E4_cap_inclusive` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 1 | killed |
| `u83-a.E5_over_cap_refusal` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 2 | killed |
| `u83-a.E7_flatten_transparency` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 3 | killed |
| `u83-a.E9_resize` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 2 | killed |
| `u83-a.R1_flac_declared_dimensions` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 1 | killed |
| `u83-a.R2_unreadable_is_not_art_error` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 1 | killed |
| `u83-a.R3_unknown_depth_default` | `src/cratekit/core/art.py` | maintainer | 1 file(s) | 73 | 1 | killed |
| `u83-a.R4_full_decode` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 1 | killed |
| `u83-b.W10_id3_add_tags` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 9 | killed |
| `u83-b.W12_container_refusal` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 5 | killed |
| `u83-b.W1_undecodable_guard` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 5 | killed |
| `u83-b.W2_format_guard` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 1 | killed |
| `u83-b.W3_progressive_guard` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 1 | killed |
| `u83-b.W4_rgb_guard` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 2 | killed |
| `u83-b.W5_cap_guard` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 2 | killed |
| `u83-b.W5b_cap_inclusive` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 1 | killed |
| `u83-b.W6_flac_block_width` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 2 | killed |
| `u83-b.W8_flac_clear_pictures` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 2 | killed |
| `u83-b.W9_id3_delall` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 3 | killed |
| `u84-a.A10_native_resolution` | `src/cratekit/core/art.py` | user | 3 file(s) | 245 | 12 | killed |
| `u84-a.A11_dimensions_from_new_bytes` | `src/cratekit/core/art.py` | user | 3 file(s) | 245 | 10 | killed |
| `u84-a.A12_all_or_nothing` | `src/cratekit/core/art.py` | user | 3 file(s) | 245 | 6 | killed |
| `u84-a.A13_read_failure_never_raises` | `src/cratekit/core/art.py` | user | 3 file(s) | 245 | 1 | killed |
| `u84-a.A1_zero_width` | `src/cratekit/core/art.py` | user | 3 file(s) | 245 | 1 | killed |
| `u84-a.A2_zero_height` | `src/cratekit/core/art.py` | user | 3 file(s) | 245 | 1 | killed |
| `u84-a.A5_not_jpeg_is_broken` | `src/cratekit/core/art.py` | user | 3 file(s) | 245 | 1 | killed |
| `u84-a.A6_progressive_is_broken` | `src/cratekit/core/art.py` | user | 3 file(s) | 245 | 1 | killed |
| `u84-a.A7_sound_art_not_written` | `src/cratekit/core/art.py` | user | 3 file(s) | 245 | 1 | killed |
| `u84-a.A8_no_picture_is_none` | `src/cratekit/core/art.py` | user | 3 file(s) | 245 | 2 | killed |
| `u84-a.A9_non_flac_unchecked` | `src/cratekit/core/art.py` | user | 3 file(s) | 245 | 1 | killed |
| `u84-a4.A4_undecodable_is_broken` | `src/cratekit/core/art.py` | user | 3 file(s) | 245 | 2 | killed |
| `u84-b.A14_save_failure_never_raises` | `src/cratekit/core/art.py` | user | 3 file(s) | 245 | 1 | killed |
| `u84-b.A15_sound_blocks_kept` | `src/cratekit/core/art.py` | user | 3 file(s) | 245 | 1 | killed |
| `u84-b.A16_shrink_fallback` | `src/cratekit/core/art.py` | user | 3 file(s) | 245 | 2 | killed |
| `u84-b.A17_too_small_to_shrink` | `src/cratekit/core/art.py` | maintainer | 3 file(s) | 245 | 1 | killed |
| `u84-b.A18_shrink_keeps_shape` | `src/cratekit/core/art.py` | user | 3 file(s) | 245 | 1 | killed |
| `u84-b.A19_mime_rewritten` | `src/cratekit/core/art.py` | user | 3 file(s) | 245 | 1 | killed |
| `example-binaries-five-row.B1_broken_override_falls_through` | `src/cratekit/core/binaries.py` | user | 1 file(s) | 18 | 1 | killed |
| `example-binaries-five-row.B3_platform_binary_remedy` | `src/cratekit/core/binaries.py` | maintainer | 1 file(s) | 18 | 1 | killed |
| `example-binaries-five-row.B4_unknown_source_remedy` | `src/cratekit/core/binaries.py` | maintainer | 1 file(s) | 18 | 1 | killed |
| `example-binaries-five-row.B5_credential_strip` | `src/cratekit/core/binaries.py` | user | 1 file(s) | 18 | 1 | killed |
| `u104-e.E5_install_hint_steps` | `src/cratekit/core/binary_refusal.py` | user | 3 file(s) | 118 | 4 | killed |
| `u241.M09_ceiling_ignores_the_reserve` | `src/cratekit/core/cores.py` | user | 2 file(s) | 314 | 14 | killed |
| `u93-recursive-analysis.D10_sorted_items` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 67 | 1 | killed |
| `u93-recursive-analysis.D11_absolute_id` | `src/cratekit/core/discovery.py` | maintainer | 2 file(s) | 67 | 1 | killed |
| `u93-recursive-analysis.D12_parent_id` | `src/cratekit/core/discovery.py` | maintainer | 2 file(s) | 67 | 3 | killed |
| `u93-recursive-analysis.D13_singular` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 67 | 2 | killed |
| `u93-recursive-analysis.D15_unreadable_empty` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 67 | 8 | killed |
| `u93-recursive-analysis.D16_none_filter` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 67 | 29 | killed |
| `u93-recursive-analysis.D17_and_more` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 67 | 1 | killed |
| `u93-recursive-analysis.D18_strings_shape` | `src/cratekit/core/discovery.py` | maintainer | 2 file(s) | 67 | 1 | killed |
| `u93-recursive-analysis.D19_resume_half` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 67 | 1 | killed |
| `u93-recursive-analysis.D1_dotfile` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 67 | 2 | killed |
| `u93-recursive-analysis.D20_frozen_links` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 67 | 2 | killed |
| `u93-recursive-analysis.D2_is_file` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 67 | 1 | killed |
| `u93-recursive-analysis.D3_suffix` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 67 | 1 | killed |
| `u93-recursive-analysis.D4_default_mode` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 67 | 3 | killed |
| `u93-recursive-analysis.D5_dot_directory` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 67 | 2 | killed |
| `u93-recursive-analysis.D6_link_declined` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 67 | 6 | killed |
| `u93-recursive-analysis.D7_prune_in_place` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 67 | 2 | killed |
| `u94-b.W9_walk_warning_says_queued` | `src/cratekit/core/discovery.py` | user | 1 file(s) | 172 | 1 | killed |
| `u185.F11_difference_memberships` | `src/cratekit/core/foreign_tree.py` | user | 1 file(s) | 31 | 1 | killed |
| `u185.F12_difference_appeared` | `src/cratekit/core/foreign_tree.py` | user | 1 file(s) | 31 | 1 | killed |
| `u185.F1_root_must_be_a_folder` | `src/cratekit/core/foreign_tree.py` | user | 1 file(s) | 31 | 4 | killed |
| `u185.F2_root_must_be_at_the_top` | `src/cratekit/core/foreign_tree.py` | user | 2 file(s) | 97 | 4 | killed |
| `u185.F3_descendants_walked` | `src/cratekit/core/foreign_tree.py` | user | 3 file(s) | 142 | 9 | killed |
| `u185.F4_create_inside` | `src/cratekit/core/foreign_tree.py` | user | 1 file(s) | 31 | 1 | killed |
| `u185.F5_second_root` | `src/cratekit/core/foreign_tree.py` | user | 1 file(s) | 31 | 1 | killed |
| `u185.F7_modify_inside` | `src/cratekit/core/foreign_tree.py` | user | 1 file(s) | 31 | 1 | killed |
| `u185.F8_moved_in` | `src/cratekit/core/foreign_tree.py` | user | 1 file(s) | 31 | 1 | killed |
| `u185.F9_membership` | `src/cratekit/core/foreign_tree.py` | user | 1 file(s) | 31 | 1 | killed |
| `r289-b.D1_no_chunking` | `src/cratekit/core/jobs.py` | user | 30 file(s) | 2553 | 1 | killed |
| `r289-b.D3_unknown_name_gets_a_state` | `src/cratekit/core/jobs.py` | user | 30 file(s) | 2553 | 2 | killed |
| `r290-author.J1_blocked_branch_removed` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 2679 | 49 | killed |
| `r290-author.J2_blocked_raises_the_plain_type` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 2679 | 48 | killed |
| `r290-author.J3_closed_branch_removed` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 2679 | 112 | killed |
| `r290-author.J4_predicate_narrowed_to_failed` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 2679 | 31 | killed |
| `r290-author.J5_causeless_block_returns` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 2679 | 1 | killed |
| `r290-author.J6_causeless_block_raises_the_plain_type` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 2679 | 1 | killed |
| `r290-author.J7_cancelled_raises_the_plain_type` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 2679 | 26 | killed |
| `r380.G3_retryable_requires_every_item` | `src/cratekit/core/jobs_drive.py` | user | 1 file(s) | 83 | 1 | killed |
| `r380.G5_permanent_failures_still_offer_resume` | `src/cratekit/core/jobs_drive.py` | user | 2 file(s) | 165 | 6 | killed |
| `r390-a.A2_retry_refuses_any_closed_job_with_a_cause` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 307 | 9 | killed |
| `r390-a.A3_a_failed_job_with_no_cause_is_refused` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 83 | 1 | killed |
| `r390-a.A4_refusal_drops_the_permanent_reasons` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 83 | 1 | killed |
| `r390-a.A5_refusal_drops_the_inner_cause` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 225 | 4 | killed |
| `r390-b.B1_last_reason_restored` | `src/cratekit/core/jobs_drive.py` | user | 1 file(s) | 83 | 1 | killed |
| `r390-b.B2_reasons_in_reverse_order` | `src/cratekit/core/jobs_drive.py` | user | 1 file(s) | 83 | 1 | killed |
| `r390-b.B3_message_does_not_name_the_reasons` | `src/cratekit/core/jobs_drive.py` | user | 1 file(s) | 83 | 1 | killed |
| `r390-b.B4_detail_drops_permanent_reasons` | `src/cratekit/core/jobs_drive.py` | user | 1 file(s) | 83 | 1 | killed |
| `r390-b.B5_one_shared_reason_is_also_mixed` | `src/cratekit/core/jobs_drive.py` | user | 1 file(s) | 83 | 3 | killed |
| `r390-b.B6_envelope_drops_the_reasons` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 83 | 1 | killed |
| `r390-b.B7_drive_passes_no_reasons_to_the_envelope` | `src/cratekit/core/jobs_drive.py` | user | 1 file(s) | 83 | 1 | killed |
| `r704-a.E2_job_verdict_needs_every_item_retryable` | `src/cratekit/core/jobs_drive.py` | user | 33 file(s) | 2851 | 1 | killed |
| `u140.B3_refreeze_any_state` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 29 | 1 | killed |
| `u140.B4_refreeze_writes_nothing_new` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 29 | 7 | killed |
| `u169.E1_declined_accepts_retryable` | `src/cratekit/core/jobs_drive.py` | user | 2 file(s) | 152 | 2 | killed |
| `u169.E2_drive_fails_a_decline` | `src/cratekit/core/jobs_drive.py` | user | 2 file(s) | 152 | 11 | killed |
| `u169.E3_decline_writes_failed` | `src/cratekit/core/jobs_drive.py` | user | 2 file(s) | 152 | 10 | killed |
| `u169.E4_decline_drops_cause` | `src/cratekit/core/jobs_drive.py` | user | 2 file(s) | 152 | 10 | killed |
| `u169.E6_failed_cause_hides_declines` | `src/cratekit/core/jobs_drive.py` | user | 2 file(s) | 152 | 1 | killed |
| `u193.M14_park_job_id_dropped` | `src/cratekit/core/jobs_drive.py` | user | 5 file(s) | 509 | 1 | killed |
| `u193.M15_park_job_id_overwrites` | `src/cratekit/core/jobs_drive.py` | maintainer | 5 file(s) | 509 | 1 | killed |
| `u227.R16_join_state` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 129 | 5 | killed |
| `u227.R17_join_held` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 129 | 1 | killed |
| `u227.R18_join_blank` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 129 | 1 | killed |
| `u235.S1_enqueue_ignores_a_given_job_id` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 83 | 26 | killed |
| `u270.J1_claim_batch_size_floor` | `src/cratekit/core/jobs.py` | maintainer | 3 file(s) | 135 | 1 | killed |
| `u270.J2_claim_batch_order` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 167 | 22 | killed |
| `u270.J3_park_releases_the_batch` | `src/cratekit/core/jobs_drive.py` | user | 3 file(s) | 167 | 4 | killed |
| `u270.J4_signal_releases_the_batch` | `src/cratekit/core/jobs_drive.py` | user | 3 file(s) | 167 | 1 | killed |
| `u270.J5_declined_outcome` | `src/cratekit/core/jobs_drive.py` | user | 1 file(s) | 20 | 1 | killed |
| `u270.J6_missing_outcome_fails` | `src/cratekit/core/jobs_drive.py` | user | 2 file(s) | 145 | 1 | killed |
| `u270.J7_raise_is_every_outcome` | `src/cratekit/core/jobs_drive.py` | user | 3 file(s) | 167 | 3 | killed |
| `u270.J8_stop_is_the_signal` | `src/cratekit/core/jobs_drive.py` | user | 2 file(s) | 52 | 1 | killed |
| `u270.J9_outcome_type_check` | `src/cratekit/core/jobs_drive.py` | maintainer | 1 file(s) | 20 | 1 | killed |
| `u298.H16_reported_extra_under_progress` | `src/cratekit/core/jobs.py` | user | 18 file(s) | 1525 | 129 | killed |
| `u298.H17_reported_cause` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 102 | 1 | killed |
| `u298.H18_staged_path_cleared` | `src/cratekit/core/jobs.py` | user | 2 file(s) | 183 | 1 | killed |
| `u298.H19_by_ordinal_numeric` | `src/cratekit/core/jobs.py` | user | 2 file(s) | 183 | 1 | killed |
| `u298.H20_by_ordinal_filters` | `src/cratekit/core/jobs.py` | user | 2 file(s) | 183 | 1 | killed |
| `u298.H21_advance_refuses_empty` | `src/cratekit/core/jobs.py` | user | 2 file(s) | 156 | 3 | killed |
| `u298.H22_resumed_raises_state` | `src/cratekit/core/jobs.py` | user | 2 file(s) | 183 | 2 | killed |
| `u298.H23_artifacts_names_differ` | `src/cratekit/core/jobs.py` | maintainer | 1 file(s) | 100 | 1 | killed |
| `u12-independent-round-6.C2_reserve_halved` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 2 | killed |
| `u12-independent-round-6.C4_darwin_headroom` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 4 | killed |
| `u12-independent-round-6.C5_swap_threshold` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 4 | killed |
| `u12-independent-round-6.C6_used_percent_ceiling` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 2 | killed |
| `u12-independent-round-6.C7_max_tasks_per_child` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 3 | killed |
| `u12-independent-round-6.C8_probe_deadline` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.C9_reap_budget` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.G1_dotdot_not_refused` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.G2_containment_dropped` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 2 | killed |
| `u12-independent-round-6.G3_headroom_can_go_negative` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.G4_controller_substring_match` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 2 | killed |
| `u12-independent-round-6.G5_loosest_cap_wins` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.G6_cgroup_cap_ignored` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 3 | killed |
| `u12-independent-round-6.G7_valueerror_escapes_the_reader` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.M1_measurement_below_the_floor` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.M2_nonsense_measurement_accepted` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 2 | killed |
| `u12-independent-round-6.M3_zero_deadline_allowed` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.M4_model_freed_before_the_reading` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.M5_terminate_rung_removed` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 3 | killed |
| `u12-independent-round-6.M6_kill_rung_removed` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.M7_parent_keeps_the_write_end` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.M8_no_reap_after_the_probe` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.P10_recycle_reported_for_in_process` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 2 | killed |
| `u12-independent-round-6.P12_unreadable_falls_back_to_ceiling` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 8 | killed |
| `u12-independent-round-6.P1_reserve_not_applied` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 14 | killed |
| `u12-independent-round-6.P2_order_reversed` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 6 | killed |
| `u12-independent-round-6.P3_budget_can_go_negative` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 2 | killed |
| `u12-independent-round-6.P4_no_floor_of_one_worker` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 11 | killed |
| `u12-independent-round-6.P5_tie_goes_to_the_ceiling` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.P6_no_insufficient_memory_bound` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 5 | killed |
| `u12-independent-round-6.R1_available_type_check` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 5 | killed |
| `u12-independent-round-6.R2_available_never_raises` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 2 | killed |
| `u12-independent-round-6.R3_pressure_percent_range` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.R4_pressure_type_check` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 2 | killed |
| `u12-independent-round-6.X1_pool_of_one_built` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.X3_generation_boundary_removed` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.X4_initargs_not_refused` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.X5_in_process_path_removed` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.X7_generation_size_drops_the_width` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 9 | killed |
| `u241.M01_worker_takes_the_interrupt` | `src/cratekit/core/pool.py` | user | 1 file(s) | 26 | 1 | killed |
| `u241.M02_worker_outlives_its_parent` | `src/cratekit/core/pool.py` | user | 1 file(s) | 26 | 1 | killed |
| `u241.M03_close_waits_for_unread_work` | `src/cratekit/core/pool.py` | user | 1 file(s) | 26 | 1 | killed |
| `u241.M07_used_percent_gate_is_strict` | `src/cratekit/core/pool.py` | user | 2 file(s) | 295 | 3 | killed |
| `u241.M08_plan_forgets_which_gate` | `src/cratekit/core/pool.py` | user | 2 file(s) | 298 | 6 | killed |
| `r83-round-2.I1_fold_case` | `src/cratekit/core/preflight.py` | user | 15 file(s) | 2840 | 19 | killed |
| `r83-round-2.I3_configured_compare_exact` | `src/cratekit/core/preflight.py` | user | 15 file(s) | 2840 | 2 | killed |
| `r83-round-2.I4_elsewhere_compare_exact` | `src/cratekit/core/preflight.py` | user | 15 file(s) | 2840 | 1 | killed |
| `u27-round-8-independent.E4_path_missing_reads_ok` | `src/cratekit/core/preflight.py` | user | 5 file(s) | 740 | 4 | killed |
| `u27-round-8-independent.E5_unmounted_reads_foreign` | `src/cratekit/core/preflight.py` | user | 5 file(s) | 740 | 5 | killed |
| `u27-round-8-independent.E6_write_table_shares_read` | `src/cratekit/core/preflight.py` | user | 5 file(s) | 740 | 3 | killed |
| `u173.M20_agent_process` | `src/cratekit/core/processes.py` | user | 1 file(s) | 33 | 1 | killed |
| `u211.P10_read_rekordbox_is_running` | `src/cratekit/core/processes.py` | user | 2 file(s) | 58 | 5 | killed |
| `u211.P11_unconfirmed_is_not_absent` | `src/cratekit/core/processes.py` | user | 3 file(s) | 109 | 11 | killed |
| `u211.P12_careful_pid_refuses` | `src/cratekit/core/processes.py` | user | 2 file(s) | 58 | 8 | killed |
| `u211.P1_denied_is_skipped` | `src/cratekit/core/processes.py` | user | 2 file(s) | 58 | 1 | killed |
| `u211.P2_gone_is_skipped` | `src/cratekit/core/processes.py` | user | 2 file(s) | 58 | 1 | killed |
| `u211.P3_recheck_before_refusing` | `src/cratekit/core/processes.py` | user | 2 file(s) | 58 | 9 | killed |
| `u211.P4_zombie_status_reads_zombie` | `src/cratekit/core/processes.py` | user | 2 file(s) | 58 | 8 | killed |
| `u211.P5_gone_on_status_read` | `src/cratekit/core/processes.py` | user | 2 file(s) | 58 | 1 | killed |
| `u211.P6_unreadable_status_is_not_gone` | `src/cratekit/core/processes.py` | user | 2 file(s) | 58 | 2 | killed |
| `u211.P7_unreadable_refuses` | `src/cratekit/core/processes.py` | user | 3 file(s) | 109 | 17 | killed |
| `u211.P8_unreadable_pid_list_refuses` | `src/cratekit/core/processes.py` | user | 2 file(s) | 58 | 1 | killed |
| `u211.P9_whole_list_walked` | `src/cratekit/core/processes.py` | user | 2 file(s) | 58 | 3 | killed |
| `r705-a.G10_long_wait_under_the_lock` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 117 | 1 | killed |
| `r705-a.G11_lock_limit_without_the_interval` | `src/cratekit/core/provider_gate.py` | maintainer | 1 file(s) | 117 | 1 | killed |
| `r705-a.G12_park_forgotten` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 117 | 2 | killed |
| `r705-a.G13_process_calls_not_counted` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 117 | 19 | killed |
| `r705-a.G1_interval_halved` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 117 | 9 | killed |
| `r705-a.G2_last_call_ignored` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 117 | 9 | killed |
| `r705-a.G3_retry_after_ignored` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 117 | 3 | killed |
| `r705-a.G4_trip_after_off_by_one` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 117 | 3 | killed |
| `r705-a.G5_no_trip_on_long_retry_after` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 117 | 5 | killed |
| `r705-a.G6_cooldown_not_recorded` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 117 | 7 | killed |
| `r705-a.G7_success_keeps_the_run` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 117 | 1 | killed |
| `r705-a.G8_call_ignores_the_cooldown` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 117 | 2 | killed |
| `r705-a.G9_assert_open_ignores_the_cooldown` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 117 | 4 | killed |
| `r759-b.P4_lock_removed_r01` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 1 | 1 | killed |
| `r759.P1_interval_dropped` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 1 | 1 | killed |
| `r759.P5_lock_shared` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 1 | 1 | killed |
| `r759.P6_wait_skipped_stamp_kept` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 1 | 1 | killed |
| `u193.M10_config_not_read` | `src/cratekit/core/provider_gate.py` | user | 5 file(s) | 509 | 4 | killed |
| `u193.M1_ceiling_check_removed` | `src/cratekit/core/provider_gate.py` | user | 5 file(s) | 509 | 13 | killed |
| `u193.M2_ceiling_off_by_one` | `src/cratekit/core/provider_gate.py` | user | 5 file(s) | 509 | 13 | killed |
| `u193.M3_spent_from_process_start` | `src/cratekit/core/provider_gate.py` | user | 5 file(s) | 509 | 13 | killed |
| `u193.M8_raised_ignored` | `src/cratekit/core/provider_gate.py` | user | 5 file(s) | 509 | 7 | killed |
| `u205.G1_app_call_not_counted` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 183 | 5 | killed |
| `u205.G2_app_rate_limit_not_counted` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 183 | 1 | killed |
| `u205.G3_attach_drops_identity` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 183 | 6 | killed |
| `u205.G5_app_share_unclamped` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 183 | 1 | killed |
| `u205.G6_file_account_share_is_the_total` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 183 | 2 | killed |
| `u205.G7_process_spend_drops_app` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 183 | 1 | killed |
| `u205.G8_since_keeps_earlier_app_calls` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 183 | 1 | killed |
| `u217.G1_ceiling_says_kept` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 117 | 1 | killed |
| `u278.M10_window_short` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 177 | 5 | killed |
| `u278.M11_window_dropped_on_read` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 177 | 23 | killed |
| `u278.M12_no_over_the_line_in_call` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 177 | 1 | killed |
| `u278.M13_over_the_line_loosened` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 177 | 3 | killed |
| `u278.M14_hour_raise_ignored` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 177 | 2 | killed |
| `u278.M15_hour_not_exported` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 177 | 1 | killed |
| `u278.M16_nested_class_kept` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 177 | 2 | killed |
| `u278.M17_spending_widens` | `src/cratekit/core/provider_gate.py` | user | 3 file(s) | 287 | 1 | killed |
| `u278.M18_reading_noop` | `src/cratekit/core/provider_gate.py` | user | 3 file(s) | 271 | 3 | killed |
| `u278.M2_future_minute_not_settled` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 177 | 2 | killed |
| `u278.M4_no_budget_check` | `src/cratekit/core/provider_gate.py` | user | 3 file(s) | 271 | 17 | killed |
| `u278.M5_budget_off_by_one` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 177 | 16 | killed |
| `u278.M6_count_not_written` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 177 | 25 | killed |
| `u278.M7_identities_merged` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 177 | 2 | killed |
| `u278.M8_no_reserve` | `src/cratekit/core/provider_gate.py` | user | 3 file(s) | 271 | 23 | killed |
| `u278.M9_continue_names_no_hour` | `src/cratekit/core/provider_gate.py` | user | 4 file(s) | 247 | 3 | killed |
| `u293.G1_night_line_asked` | `src/cratekit/core/provider_gate.py` | user | 4 file(s) | 280 | 6 | killed |
| `u293.G2_night_line_off_by_one` | `src/cratekit/core/provider_gate.py` | user | 4 file(s) | 280 | 5 | killed |
| `u293.G3_total_below_mark` | `src/cratekit/core/provider_gate.py` | user | 4 file(s) | 280 | 1 | killed |
| `u293.G4_child_reads_no_line` | `src/cratekit/core/provider_gate.py` | user | 4 file(s) | 280 | 2 | killed |
| `u293.G5_line_held_to_ceiling` | `src/cratekit/core/provider_gate.py` | user | 4 file(s) | 280 | 5 | killed |
| `u293.G6_nested_lower_line` | `src/cratekit/core/provider_gate.py` | maintainer | 4 file(s) | 280 | 1 | killed |
| `u293.G7_hour_never_raised` | `src/cratekit/core/provider_gate.py` | user | 4 file(s) | 280 | 1 | killed |
| `u293.G8_line_exported` | `src/cratekit/core/provider_gate.py` | user | 4 file(s) | 280 | 2 | killed |
| `r431-a.A6_a_standing_companion_is_rewritten` | `src/cratekit/core/review.py` | maintainer | 20 file(s) | 3057 | 1 | killed |
| `r431-a.A7_beside_written_when_the_record_stood` | `src/cratekit/core/review.py` | user | 20 file(s) | 3057 | 2 | killed |
| `r431-a.A8_also_is_never_asked` | `src/cratekit/core/review.py` | user | 20 file(s) | 3057 | 6 | killed |
| `r431-a.A9_an_already_lifted_record_is_lifted_again` | `src/cratekit/core/review.py` | maintainer | 20 file(s) | 3057 | 1 | killed |
| `r679-a.A1_supersede_guard_both_layers` | `src/cratekit/core/review.py` | user | 3 file(s) | 870 | 5 | killed |
| `r679-a.A3_supersede_readers_predicate` | `src/cratekit/core/review.py` | user | 3 file(s) | 870 | 1 | killed |
| `r679-a.A4_resolve_admits_the_machines_verdict` | `src/cratekit/core/review.py` | user | 3 file(s) | 870 | 1 | killed |
| `r679-a.A5_import_routes_through_resolve` | `src/cratekit/core/review_exchange.py` | user | 3 file(s) | 870 | 2 | killed |
| `r679-a.A6_empty_rule_admitted` | `src/cratekit/core/review.py` | user | 3 file(s) | 870 | 2 | killed |
| `r679-a.A7_person_verdicts_are_all_verdicts` | `src/cratekit/core/review.py` | user | 3 file(s) | 870 | 2 | killed |
| `r679-a.A8_actor_is_not_the_rule` | `src/cratekit/core/review.py` | user | 3 file(s) | 870 | 11 | killed |
| `r790-d.R1_grouping_kinds` | `src/cratekit/core/review_groups.py` | user | 2 file(s) | 192 | 1 | killed |
| `r790-d.R2_label_beyond` | `src/cratekit/core/review_groups.py` | user | 2 file(s) | 192 | 7 | killed |
| `r798-c.H2_only_a_hold_in_force_is_dropped` | `src/cratekit/core/review_holds.py` | user | 4 file(s) | 387 | 1 | killed |
| `r815-a.W1_withhold_only_an_open_item` | `src/cratekit/core/review_holds.py` | user | 2 file(s) | 214 | 5 | killed |
| `r815-a.W2_a_returned_hold_is_not_withheld` | `src/cratekit/core/review_holds.py` | user | 2 file(s) | 214 | 1 | killed |
| `r815-a.W3_the_floor_is_never_lowered` | `src/cratekit/core/review_holds.py` | user | 2 file(s) | 214 | 1 | killed |
| `r815-a.W4_the_next_ordinal_is_past_the_floor` | `src/cratekit/core/review.py` | user | 3 file(s) | 367 | 2 | killed |
| `r815-a.W5_a_refresh_keeps_the_withheld_word` | `src/cratekit/core/review_holds.py` | user | 2 file(s) | 214 | 1 | killed |
| `r815-a.W6_redescribe_only_an_open_item` | `src/cratekit/core/review.py` | user | 2 file(s) | 214 | 2 | killed |
| `r840-c.C1_the_function_is_handed_the_payload_as_it_stands` | `src/cratekit/core/review.py` | user | 2 file(s) | 137 | 34 | killed |
| `r840-c.C2_the_function_is_only_handed_an_open_item` | `src/cratekit/core/review.py` | user | 2 file(s) | 137 | 4 | killed |
| `r650-a.A1_tier_five_sets_nothing` | `src/cratekit/core/routing.py` | user | 8 file(s) | 1562 | 6 | killed |
| `r650-a.A2_tier_five_flags_everything` | `src/cratekit/core/routing.py` | user | 8 file(s) | 1562 | 2 | killed |
| `r650-a.A3_suppression_widens_to_the_vocabulary` | `src/cratekit/core/routing.py` | user | 8 file(s) | 1562 | 1 | killed |
| `r650-a.A4_suppression_ignores_case` | `src/cratekit/core/routing.py` | user | 8 file(s) | 1562 | 1 | killed |
| `r650-a.A6_declared_literal_rule_flagged` | `src/cratekit/core/routing.py` | user | 8 file(s) | 1460 | collection error | collect-error |
| `r731-b.M21_sink_does_not_compete` | `src/cratekit/core/routing.py` | user | 2 file(s) | 95 | 11 | killed |
| `r731-b.M22_single_sub_does_not_compete` | `src/cratekit/core/routing.py` | maintainer | 2 file(s) | 95 | 1 | killed |
| `r797-a.T7_competes_in_a_style_bucket` | `src/cratekit/core/routing.py` | user | 4 file(s) | 1063 | 13 | killed |
| `r797-a.T8_competes_in_a_band_bucket` | `src/cratekit/core/routing.py` | user | 4 file(s) | 1063 | 30 | killed |
| `r797-c.G6_the_fallback_is_no_folder` | `src/cratekit/core/routing.py` | user | 1 file(s) | 30 | 11 | killed |
| `r797-c.G7_a_folders_own_name_has_that_folder` | `src/cratekit/core/routing.py` | user | 1 file(s) | 30 | 1 | killed |
| `r797-c.G8_a_map_row_is_a_style_sub` | `src/cratekit/core/routing.py` | user | 1 file(s) | 30 | 3 | killed |
| `r798-a.K1_the_first_rule_that_matches_wins` | `src/cratekit/core/routing.py` | user | 3 file(s) | 1115 | 3 | killed |
| `r798-a.K2_one_word_of_the_labels_kind_passes` | `src/cratekit/core/routing.py` | user | 3 file(s) | 1115 | 3 | killed |
| `r798-a.K3_a_hold_needs_a_known_word` | `src/cratekit/core/routing.py` | user | 3 file(s) | 1115 | 1 | killed |
| `r798-a.K4_a_label_of_any_kind_passes` | `src/cratekit/core/routing.py` | user | 3 file(s) | 1115 | 3 | killed |
| `r798-a.K5_a_kind_nothing_names_is_not_judged` | `src/cratekit/core/routing.py` | user | 3 file(s) | 1115 | 1 | killed |
| `r798-d.K11_the_shared_matcher_reads_a_substring_needle` | `src/cratekit/core/routing.py` | user | 3 file(s) | 1115 | 101 | killed |
| `r799-a.R1_a_table_is_read_only_for_its_source` | `src/cratekit/core/routing.py` | user | 3 file(s) | 511 | 2 | killed |
| `u118-b.R1_split_competes` | `src/cratekit/core/routing.py` | user | 2 file(s) | 103 | 20 | killed |
| `u118-b.R2_split_lookup` | `src/cratekit/core/routing.py` | user | 2 file(s) | 103 | 15 | killed |
| `u155.R1_exact_match` | `src/cratekit/core/routing.py` | user | 20 file(s) | 2554 | 2 | killed |
| `u155.R2_tagger_branch` | `src/cratekit/core/routing.py` | user | 20 file(s) | 2554 | 4 | killed |
| `u155.R3_tagger_spelling` | `src/cratekit/core/routing.py` | user | 20 file(s) | 2554 | 1 | killed |
| `u155.R4_genre_sub_named` | `src/cratekit/core/routing.py` | user | 1 file(s) | 197 | 3 | killed |
| `u87-b.S1_curve_boundary` | `src/cratekit/core/routing.py` | user | 6 file(s) | 1410 | 6 | killed |
| `r722-b.T6_field_failure_swallowed` | `src/cratekit/core/tags.py` | user | 27 file(s) | 3054 | 1 | killed |
| `r722-b.T7_lenient_field_raises` | `src/cratekit/core/tags.py` | user | 27 file(s) | 3054 | 1 | killed |
| `r722.T1_checked_is_lenient` | `src/cratekit/core/tags.py` | user | 27 file(s) | 3054 | 5 | killed |
| `r722.T3_open_failure_is_absent` | `src/cratekit/core/tags.py` | user | 27 file(s) | 3054 | 3 | killed |
| `r722.T8_lenient_energy_raises` | `src/cratekit/core/tags.py` | user | 27 file(s) | 3054 | 1 | killed |
| `r722.T9_lenient_open_raises` | `src/cratekit/core/tags.py` | user | 27 file(s) | 3054 | 305 | killed |
| `u23-round-8-independent-hunt.HUNT_a_container_leaves_the_writers_table` | `src/cratekit/core/tags.py` | user | 2 file(s) | 625 | collection error | collect-error |
| `u23-round-8-independent.X15_save_drops_the_id3v1_trailer` | `src/cratekit/core/tags.py` | user | 3 file(s) | 872 | 1 | killed |
| `u240.M25_copyright_key_wrong` | `src/cratekit/core/tags.py` | user | 5 file(s) | 334 | 1 | killed |
| `u249.M15_noting_reader_drops_field_failure` | `src/cratekit/core/tags.py` | user | 3 file(s) | 686 | 1 | killed |
| `u249.M16_noting_reader_drops_open_failure` | `src/cratekit/core/tags.py` | user | 3 file(s) | 686 | 2 | killed |
| `u249.M17_noting_reader_drops_unrecognised` | `src/cratekit/core/tags.py` | user | 3 file(s) | 686 | 3 | killed |
| `u249.M18_noting_reader_drops_unsupported` | `src/cratekit/core/tags.py` | maintainer | 3 file(s) | 686 | 1 | killed |
| `u249.M19_noting_reader_inverted` | `src/cratekit/core/tags.py` | user | 3 file(s) | 686 | 6 | killed |
| `u250.M5_word_reads_zero` | `src/cratekit/core/tags.py` | user | 3 file(s) | 207 | 1 | killed |
| `u250.M6_absent_raises` | `src/cratekit/core/tags.py` | user | 3 file(s) | 207 | 20 | killed |
| `u250.M7_energy_word_reads_absent` | `src/cratekit/core/tags.py` | user | 4 file(s) | 123 | 2 | killed |
| `u250.M8_conversion_learns_decimals` | `src/cratekit/core/tags.py` | user | 3 file(s) | 207 | 1 | killed |
| `u81-fetch-b.S1_strip_does_nothing` | `src/cratekit/core/tags.py` | user | 1 file(s) | 35 | 2 | killed |

## Row definitions

### `u260.D1_decodes_always`

decodes: answer True for any bytes, so the shipped admission admits what is not a picture

- File: `src/cratekit/core/art.py`
- Source: `u260.json`, row `D1_decodes_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_art.py`
- Collected: 269 against a baseline of 269
- Kills: 2 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_an_answer_the_admission_refuses_is_handed_on_and_not_remembered`
  - `tests/test_album_cover_once.py::test_bytes_that_are_not_a_picture_are_asked_again_and_fail_as_they_did`

Old text:

```
    return _measure(data) is not None
```

New text:

```
    return True
```

### `u260.E10_encode_memory_unbounded`

COVER_MEMORY: a hundred entries

- File: `src/cratekit/core/art.py`
- Source: `u260.json`, row `E10_encode_memory_unbounded`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_art.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_the_shipped_encode_memory_is_bounded`

Old text:

```
COVER_MEMORY = 4
```

New text:

```
COVER_MEMORY = 100
```

### `u260.E11_reset_forgets_nothing`

reset_cache: clear nothing, so one test's encode answers the next test's

- File: `src/cratekit/core/art.py`
- Source: `u260.json`, row `E11_reset_forgets_nothing`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_art.py`
- Collected: 269 against a baseline of 269
- Kills: 13 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[a refusal]`
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[a transport failure]`
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[an empty answer]`
  - `tests/test_album_cover_once.py::test_different_bytes_are_encoded_apart`
  - `tests/test_album_cover_once.py::test_every_file_carries_byte_for_byte_what_it_carried_before`
  - `tests/test_album_cover_once.py::test_the_encode_memory_drops_the_least_recently_used`
  - `tests/test_album_cover_once.py::test_the_encode_memory_keeps_a_few_pictures_and_forgets_the_oldest`
  - `tests/test_album_cover_once.py::test_the_encode_reset_forgets`
  - `tests/test_album_cover_once.py::test_the_same_bytes_at_another_size_or_cap_are_encoded_again`
  - `tests/test_album_cover_once.py::test_two_addresses_serving_the_same_bytes_make_two_requests_and_one_encode`
  - `tests/test_album_cover_once.py::test_two_albums_in_one_folder_make_two_requests_and_two_encodes`
  - `tests/test_album_cover_once.py::test_two_pictures_of_one_length_are_encoded_apart`
  - `tests/test_tag_workers.py::test_an_albums_cover_is_asked_for_and_encoded_once_across_the_queued_sweep`

Old text:

```
    with _remembered_lock:
        _remembered.clear()
```

New text:

```
    with _remembered_lock:
        pass
```

### `u260.E12_key_digest_of_64_kb`

to_cdj_jpeg_remembered: digest only the first 64 KB, the prefix round two found surviving the first header test

- File: `src/cratekit/core/art.py`
- Source: `u260.json`, row `E12_key_digest_of_64_kb`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_art.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_two_covers_sharing_a_long_header_are_encoded_apart`

Old text:

```
    key = (hashlib.sha256(data).digest(), len(data), size, max_bytes)
```

New text:

```
    key = (hashlib.sha256(data[:65536]).digest(), len(data), size, max_bytes)
```

### `u260.E2_key_drops_size`

to_cdj_jpeg_remembered: key without the edge, so a picture asked for at another size is the first size's

- File: `src/cratekit/core/art.py`
- Source: `u260.json`, row `E2_key_drops_size`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_art.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_the_same_bytes_at_another_size_or_cap_are_encoded_again`

Old text:

```
    key = (hashlib.sha256(data).digest(), len(data), size, max_bytes)
```

New text:

```
    key = (hashlib.sha256(data).digest(), len(data), None, max_bytes)
```

### `u260.E3_key_drops_cap`

to_cdj_jpeg_remembered: key without the byte cap

- File: `src/cratekit/core/art.py`
- Source: `u260.json`, row `E3_key_drops_cap`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_art.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_the_same_bytes_at_another_size_or_cap_are_encoded_again`

Old text:

```
    key = (hashlib.sha256(data).digest(), len(data), size, max_bytes)
```

New text:

```
    key = (hashlib.sha256(data).digest(), len(data), size, 0)
```

### `u260.E4_key_by_length_only`

to_cdj_jpeg_remembered: key on the length without the digest, so two pictures of one length share an encode

- File: `src/cratekit/core/art.py`
- Source: `u260.json`, row `E4_key_by_length_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_art.py`
- Collected: 269 against a baseline of 269
- Kills: 2 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_two_covers_sharing_a_long_header_are_encoded_apart`
  - `tests/test_album_cover_once.py::test_two_pictures_of_one_length_are_encoded_apart`

Old text:

```
    key = (hashlib.sha256(data).digest(), len(data), size, max_bytes)
```

New text:

```
    key = (b"", len(data), size, max_bytes)
```

### `u260.E5_key_digest_of_a_prefix`

to_cdj_jpeg_remembered: digest only the first kilobyte, so two pictures sharing a header share an encode

- File: `src/cratekit/core/art.py`
- Source: `u260.json`, row `E5_key_digest_of_a_prefix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_art.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_two_covers_sharing_a_long_header_are_encoded_apart`

Old text:

```
    key = (hashlib.sha256(data).digest(), len(data), size, max_bytes)
```

New text:

```
    key = (hashlib.sha256(data[:1024]).digest(), len(data), size, max_bytes)
```

### `u260.E6_encode_never_remembered`

to_cdj_jpeg_remembered: never answer from memory

- File: `src/cratekit/core/art.py`
- Source: `u260.json`, row `E6_encode_never_remembered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_art.py`
- Collected: 269 against a baseline of 269
- Kills: 11 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[a refusal]`
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[a transport failure]`
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[an empty answer]`
  - `tests/test_album_cover_once.py::test_different_bytes_are_encoded_apart`
  - `tests/test_album_cover_once.py::test_every_file_carries_byte_for_byte_what_it_carried_before`
  - `tests/test_album_cover_once.py::test_ten_files_naming_one_address_make_one_request_one_wait_and_one_encode`
  - `tests/test_album_cover_once.py::test_the_encode_memory_drops_the_least_recently_used`
  - `tests/test_album_cover_once.py::test_the_same_bytes_at_another_size_or_cap_are_encoded_again`
  - `tests/test_album_cover_once.py::test_two_addresses_serving_the_same_bytes_make_two_requests_and_one_encode`
  - `tests/test_album_cover_once.py::test_two_albums_in_one_folder_make_two_requests_and_two_encodes`
  - `tests/test_tag_workers.py::test_an_albums_cover_is_asked_for_and_encoded_once_across_the_queued_sweep`

Old text:

```
        made = _remembered.get(key)
        if made is not None:
```

New text:

```
        made = None
        if made is not None:
```

### `u260.E7_encode_bound_off_by_one`

to_cdj_jpeg_remembered: keep one entry more than the bound

- File: `src/cratekit/core/art.py`
- Source: `u260.json`, row `E7_encode_bound_off_by_one`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_art.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_the_encode_memory_keeps_a_few_pictures_and_forgets_the_oldest`

Old text:

```
        while len(_remembered) > COVER_MEMORY:
```

New text:

```
        while len(_remembered) > COVER_MEMORY + 1:
```

### `u260.E8_encode_hit_not_refreshed`

to_cdj_jpeg_remembered: a hit no longer refreshes its entry, so the memory is first in first out

- File: `src/cratekit/core/art.py`
- Source: `u260.json`, row `E8_encode_hit_not_refreshed`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_art.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_the_encode_memory_drops_the_least_recently_used`

Old text:

```
        if made is not None:
            _remembered.move_to_end(key)
            return made
```

New text:

```
        if made is not None:
            return made
```

### `u260.E9_encode_evicts_newest`

to_cdj_jpeg_remembered: evict the newest entry instead of the least recently used

- File: `src/cratekit/core/art.py`
- Source: `u260.json`, row `E9_encode_evicts_newest`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_art.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_the_encode_memory_keeps_a_few_pictures_and_forgets_the_oldest`

Old text:

```
            _remembered.popitem(last=False)
```

New text:

```
            _remembered.popitem(last=True)
```

### `u83-a.E10_reported_dimensions`

The encoder reports width and height transposed

- File: `src/cratekit/core/art.py`
- Source: `u83-a.json`, row `E10_reported_dimensions`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_art.py::test_size_none_keeps_the_native_resolution`

Old text:

```
return CdjJpeg(encoded, measured.width, measured.height, measured.depth)
```

New text:

```
return CdjJpeg(encoded, measured.height, measured.width, measured.depth)
```

### `u83-a.E1_baseline_flag`

The encoder emits a progressive JPEG, the kind a Pioneer player renders blank

- File: `src/cratekit/core/art.py`
- Source: `u83-a.json`, row `E1_baseline_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 3 (killed)
- Killed:
  - `tests/test_art.py::test_a_progressive_jpeg_input_comes_out_baseline`
  - `tests/test_art.py::test_a_progressive_rgba_png_comes_out_a_baseline_rgb_jpeg_under_the_cap`
  - `tests/test_art.py::test_the_encoder_never_goes_below_the_quality_floor`

Old text:

```
quality=quality, optimize=True, progressive=False)
```

New text:

```
quality=quality, optimize=True, progressive=True)
```

### `u83-a.E2_quality_floor`

Lower the quality floor from 50 to 45, a realistic nearby value

- File: `src/cratekit/core/art.py`
- Source: `u83-a.json`, row `E2_quality_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_art.py::test_the_encoder_never_goes_below_the_quality_floor`

Old text:

```
ART_MIN_QUALITY = 50
```

New text:

```
ART_MIN_QUALITY = 45
```

### `u83-a.E3_ladder_ends_on_floor`

The ladder loses its last rung, so quality 50 is never tried, the defect the suite caught while building

- File: `src/cratekit/core/art.py`
- Source: `u83-a.json`, row `E3_ladder_ends_on_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_art.py::test_the_encoder_never_goes_below_the_quality_floor`

Old text:

```
    return [*rungs, ART_MIN_QUALITY]
```

New text:

```
    return rungs
```

### `u83-a.E4_cap_inclusive`

The encoder's cap comparison becomes exclusive

- File: `src/cratekit/core/art.py`
- Source: `u83-a.json`, row `E4_cap_inclusive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_art.py::test_the_encoder_never_goes_below_the_quality_floor`

Old text:

```
        if len(encoded) <= max_bytes:
```

New text:

```
        if len(encoded) < max_bytes:
```

### `u83-a.E5_over_cap_refusal`

A picture that cannot fit comes back over the cap, as the source system returned it, instead of raising

- File: `src/cratekit/core/art.py`
- Source: `u83-a.json`, row `E5_over_cap_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 2 (killed)
- Killed:
  - `tests/test_art.py::test_a_picture_that_cannot_fit_raises_rather_than_exceeding_the_cap`
  - `tests/test_art.py::test_the_encoder_never_goes_below_the_quality_floor`

Old text:

```
    raise ArtError(
        f"the image does not fit
```

New text:

```
    return CdjJpeg(encoded, img.size[0], img.size[1], 24)
    raise ArtError(
        f"the image does not fit
```

### `u83-a.E7_flatten_transparency`

Transparency is no longer composited, a plain mode conversion exposes what lies under it

- File: `src/cratekit/core/art.py`
- Source: `u83-a.json`, row `E7_flatten_transparency`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 3 (killed)
- Killed:
  - `tests/test_art.py::test_transparency_is_flattened_onto_white_not_onto_what_lies_under_it[LA]`
  - `tests/test_art.py::test_transparency_is_flattened_onto_white_not_onto_what_lies_under_it[P]`
  - `tests/test_art.py::test_transparency_is_flattened_onto_white_not_onto_what_lies_under_it[RGBA]`

Old text:

```
    if not has_alpha:
```

New text:

```
    if True:
```

### `u83-a.E9_resize`

New art is no longer resized to the 800 pixel square

- File: `src/cratekit/core/art.py`
- Source: `u83-a.json`, row `E9_resize`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 2 (killed)
- Killed:
  - `tests/test_art.py::test_a_progressive_rgba_png_comes_out_a_baseline_rgb_jpeg_under_the_cap`
  - `tests/test_art.py::test_the_reported_dimensions_match_what_pillow_reads_back`

Old text:

```
    if size is not None and img.size != (size, size):
```

New text:

```
    if False:
```

### `u83-a.R1_flac_declared_dimensions`

The reader reports a FLAC picture's decoded size instead of what the block declares, hiding a zeroed block

- File: `src/cratekit/core/art.py`
- Source: `u83-a.json`, row `R1_flac_declared_dimensions`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_art.py::test_a_zeroed_flac_block_reads_as_zeroes_not_as_the_decoded_size`

Old text:

```
_picture(pic.mime, bytes(pic.data), (pic.width, pic.height, pic.depth))
```

New text:

```
_picture(pic.mime, bytes(pic.data), None)
```

### `u83-a.R2_unreadable_is_not_art_error`

A file that could not be read raises the image verdict again instead of its own class

- File: `src/cratekit/core/art.py`
- Source: `u83-a.json`, row `R2_unreadable_is_not_art_error`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_art.py::test_a_file_that_cannot_be_read_raises_rather_than_reading_as_no_art`

Old text:

```
        raise UnreadableFile(f"could not read
```

New text:

```
        raise ArtError(f"could not read
```

### `u83-a.R3_unknown_depth_default`

An unlisted Pillow mode measures as a guessed 24 again instead of 0

- File: `src/cratekit/core/art.py`
- Source: `u83-a.json`, row `R3_unknown_depth_default`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_art.py::test_a_mode_with_no_known_depth_reads_as_zero_not_as_a_guess`

Old text:

```
depth=_DEPTH_BY_MODE.get(img.mode, 0),
```

New text:

```
depth=_DEPTH_BY_MODE.get(img.mode, 24),
```

### `u83-a.R4_full_decode`

The measure drops its full decode, so a truncated picture that opens cleanly reads as decoded

- File: `src/cratekit/core/art.py`
- Source: `u83-a.json`, row `R4_full_decode`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_art.py::test_a_truncated_picture_does_not_read_as_decoded`

Old text:

```
            img.load()

```

New text:

```
(empty)
```

### `u83-b.W10_id3_add_tags`

The ID3 branch skips add_tags on a file with no tag yet, the step whose absence pushes a caller toward a bare ID3 object

- File: `src/cratekit/core/art.py`
- Source: `u83-b.json`, row `W10_id3_add_tags`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 9 (killed)
- Killed:
  - `tests/test_art.py::test_a_chunk_container_never_receives_a_bare_id3_stream[.aiff-FORM]`
  - `tests/test_art.py::test_a_chunk_container_never_receives_a_bare_id3_stream[.wav-RIFF]`
  - `tests/test_art.py::test_a_picture_over_the_cap_is_refused_and_the_file_untouched`
  - `tests/test_art.py::test_a_written_cover_is_the_bytes_given_reads_back_measured_and_is_replaced_by_the_next[.aiff]`
  - `tests/test_art.py::test_a_written_cover_is_the_bytes_given_reads_back_measured_and_is_replaced_by_the_next[.wav]`
  - `tests/test_art.py::test_an_art_write_leaves_the_decoded_audio_unchanged[.aiff]`
  - `tests/test_art.py::test_an_art_write_leaves_the_decoded_audio_unchanged[.wav]`
  - `tests/test_art.py::test_the_id3_frame_is_a_front_cover_jpeg[.aiff]`
  - `tests/test_art.py::test_the_id3_frame_is_a_front_cover_jpeg[.wav]`

Old text:

```
                # and saved against them. add_tags() is the container's own way.
                handle.add_tags()
```

New text:

```
                # and saved against them. add_tags() is the container's own way.
                pass
```

### `u83-b.W12_container_refusal`

A container with no verified picture handling is no longer refused

- File: `src/cratekit/core/art.py`
- Source: `u83-b.json`, row `W12_container_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 5 (killed)
- Killed:
  - `tests/test_art.py::test_a_container_without_verified_picture_handling_raises[.ogg]`
  - `tests/test_art.py::test_a_container_without_verified_picture_handling_raises[.opus]`
  - `tests/test_art.py::test_a_container_without_verified_picture_handling_raises[.xyz]`
  - `tests/test_art.py::test_a_container_without_verified_picture_handling_raises[]`
  - `tests/test_art.py::test_the_container_check_comes_before_the_image_check`

Old text:

```
    if suffix not in ART_SUFFIXES:
```

New text:

```
    if False:
```

### `u83-b.W1_undecodable_guard`

The writer's refusal of undecodable bytes is dropped, so they go on toward the file

- File: `src/cratekit/core/art.py`
- Source: `u83-b.json`, row `W1_undecodable_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 5 (killed)
- Killed:
  - `tests/test_art.py::test_a_refused_picture_fails_and_leaves_the_file_untouched[unreadable.aiff]`
  - `tests/test_art.py::test_a_refused_picture_fails_and_leaves_the_file_untouched[unreadable.flac]`
  - `tests/test_art.py::test_a_refused_picture_fails_and_leaves_the_file_untouched[unreadable.m4a]`
  - `tests/test_art.py::test_a_refused_picture_fails_and_leaves_the_file_untouched[unreadable.mp3]`
  - `tests/test_art.py::test_a_refused_picture_fails_and_leaves_the_file_untouched[unreadable.wav]`

Old text:

```
    if measured is None:
        raise ArtError("the picture bytes could not be decoded, so nothing was written")

```

New text:

```
(empty)
```

### `u83-b.W2_format_guard`

The writer accepts a picture that is not a JPEG

- File: `src/cratekit/core/art.py`
- Source: `u83-b.json`, row `W2_format_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_art.py::test_a_refused_picture_fails_and_leaves_the_file_untouched[png]`

Old text:

```
    if measured.format != "JPEG":
```

New text:

```
    if False:
```

### `u83-b.W3_progressive_guard`

The writer accepts a progressive JPEG

- File: `src/cratekit/core/art.py`
- Source: `u83-b.json`, row `W3_progressive_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_art.py::test_a_refused_picture_fails_and_leaves_the_file_untouched[progressive]`

Old text:

```
    if measured.progressive:
```

New text:

```
    if False:
```

### `u83-b.W4_rgb_guard`

The writer accepts a greyscale or CMYK JPEG

- File: `src/cratekit/core/art.py`
- Source: `u83-b.json`, row `W4_rgb_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 2 (killed)
- Killed:
  - `tests/test_art.py::test_a_refused_picture_fails_and_leaves_the_file_untouched[jpeg-CMYK]`
  - `tests/test_art.py::test_a_refused_picture_fails_and_leaves_the_file_untouched[jpeg-L]`

Old text:

```
    if measured.mode != "RGB":
```

New text:

```
    if False:
```

### `u83-b.W5_cap_guard`

The writer accepts a picture over the byte cap

- File: `src/cratekit/core/art.py`
- Source: `u83-b.json`, row `W5_cap_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 2 (killed)
- Killed:
  - `tests/test_art.py::test_a_picture_over_the_cap_is_refused_and_the_file_untouched`
  - `tests/test_art.py::test_the_writer_default_cap_is_the_encoder_default_cap`

Old text:

```
    if len(jpeg) > max_bytes:
```

New text:

```
    if False:
```

### `u83-b.W5b_cap_inclusive`

The writer's cap becomes exclusive while the encoder's stays inclusive, so a picture encoded exactly to the cap is refused

- File: `src/cratekit/core/art.py`
- Source: `u83-b.json`, row `W5b_cap_inclusive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_art.py::test_a_picture_over_the_cap_is_refused_and_the_file_untouched`

Old text:

```
    if len(jpeg) > max_bytes:
```

New text:

```
    if len(jpeg) >= max_bytes:
```

### `u83-b.W6_flac_block_width`

The FLAC block declares width zero, the vendored downloader's defect

- File: `src/cratekit/core/art.py`
- Source: `u83-b.json`, row `W6_flac_block_width`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 2 (killed)
- Killed:
  - `tests/test_art.py::test_a_written_cover_is_the_bytes_given_reads_back_measured_and_is_replaced_by_the_next[.flac]`
  - `tests/test_art.py::test_the_flac_block_carries_nonzero_width_height_and_depth`

Old text:

```
            block.width = measured.width
```

New text:

```
            block.width = 0
```

### `u83-b.W8_flac_clear_pictures`

The FLAC writer appends instead of replacing

- File: `src/cratekit/core/art.py`
- Source: `u83-b.json`, row `W8_flac_clear_pictures`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 2 (killed)
- Killed:
  - `tests/test_art.py::test_a_flac_picture_of_another_type_is_replaced_too`
  - `tests/test_art.py::test_a_written_cover_is_the_bytes_given_reads_back_measured_and_is_replaced_by_the_next[.flac]`

Old text:

```
            handle.clear_pictures()

```

New text:

```
(empty)
```

### `u83-b.W9_id3_delall`

The ID3 writer stops clearing pictures other tools embedded under another description

- File: `src/cratekit/core/art.py`
- Source: `u83-b.json`, row `W9_id3_delall`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 3 (killed)
- Killed:
  - `tests/test_art.py::test_an_id3_picture_another_tool_embedded_is_replaced_too[.aiff]`
  - `tests/test_art.py::test_an_id3_picture_another_tool_embedded_is_replaced_too[.mp3]`
  - `tests/test_art.py::test_an_id3_picture_another_tool_embedded_is_replaced_too[.wav]`

Old text:

```
            handle.tags.delall("APIC")

```

New text:

```
(empty)
```

### `u84-a.A10_native_resolution`

The repair re-encodes to the 800 square new art edge, which upscales a 320 by 200 cover and stretches it

- File: `src/cratekit/core/art.py`
- Source: `u84-a.json`, row `A10_native_resolution`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_art.py`
- Collected: 245 against a baseline of 245
- Kills: 12 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_art_repair_reaches_the_artifact_and_the_summary_counts_every_status`
  - `tests/test_tagging_engine.py::test_a_file_that_already_has_a_genre_is_still_repaired`
  - `tests/test_tagging_engine.py::test_a_picture_too_large_for_the_cap_at_native_size_is_shrunk_not_left_blank`
  - `tests/test_tagging_engine.py::test_a_png_in_a_filled_block_is_re_encoded_as_a_baseline_jpeg`
  - `tests/test_tagging_engine.py::test_a_progressive_jpeg_with_sound_dimensions_becomes_baseline`
  - `tests/test_tagging_engine.py::test_a_sound_block_beside_a_broken_one_is_kept_as_it_was_and_in_order`
  - `tests/test_tagging_engine.py::test_a_tagged_file_with_zeroed_art_is_repaired_and_never_fetched`
  - `tests/test_tagging_engine.py::test_a_vendored_zeroed_block_ends_with_real_dimensions_and_the_same_image`
  - `tests/test_tagging_engine.py::test_an_untagged_file_with_zeroed_art_gets_its_genre_and_keeps_its_picture`
  - `tests/test_tagging_engine.py::test_any_one_zeroed_dimension_is_broken[dims0]`
  - `tests/test_tagging_engine.py::test_any_one_zeroed_dimension_is_broken[dims1]`
  - `tests/test_tagging_engine.py::test_any_one_zeroed_dimension_is_broken[dims2]`

Old text:

```
        return to_cdj_jpeg(data, size=None), False
```

New text:

```
        return to_cdj_jpeg(data, size=ART_SIZE), False
```

### `u84-a.A11_dimensions_from_new_bytes`

The repaired block's width, height and depth are not written, so the zeroes stay

- File: `src/cratekit/core/art.py`
- Source: `u84-a.json`, row `A11_dimensions_from_new_bytes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_art.py`
- Collected: 245 against a baseline of 245
- Kills: 10 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_art_repair_reaches_the_artifact_and_the_summary_counts_every_status`
  - `tests/test_tagging_engine.py::test_a_file_that_already_has_a_genre_is_still_repaired`
  - `tests/test_tagging_engine.py::test_a_picture_too_large_for_the_cap_at_native_size_is_shrunk_not_left_blank`
  - `tests/test_tagging_engine.py::test_a_sound_block_beside_a_broken_one_is_kept_as_it_was_and_in_order`
  - `tests/test_tagging_engine.py::test_a_tagged_file_with_zeroed_art_is_repaired_and_never_fetched`
  - `tests/test_tagging_engine.py::test_a_vendored_zeroed_block_ends_with_real_dimensions_and_the_same_image`
  - `tests/test_tagging_engine.py::test_an_untagged_file_with_zeroed_art_gets_its_genre_and_keeps_its_picture`
  - `tests/test_tagging_engine.py::test_any_one_zeroed_dimension_is_broken[dims0]`
  - `tests/test_tagging_engine.py::test_any_one_zeroed_dimension_is_broken[dims1]`
  - `tests/test_tagging_engine.py::test_any_one_zeroed_dimension_is_broken[dims2]`

Old text:

```
            block.width, block.height, block.depth = cdj.width, cdj.height, cdj.depth
```

New text:

```
            pass
```

### `u84-a.A12_all_or_nothing`

A block that cannot be repaired is passed over and the rest are saved and reported fixed

- File: `src/cratekit/core/art.py`
- Source: `u84-a.json`, row `A12_all_or_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_art.py`
- Collected: 245 against a baseline of 245
- Kills: 6 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_corrupt_image_reports_an_error_and_the_genre_flow_still_proceeds`
  - `tests/test_tagging_engine.py::test_a_picture_inside_the_box_that_cannot_fit_is_an_error_and_is_never_enlarged`
  - `tests/test_tagging_engine.py::test_an_encoder_failure_that_is_not_an_art_error_is_still_an_error`
  - `tests/test_tagging_engine.py::test_an_undecodable_image_in_a_filled_block_is_an_error_not_ok[not-an-image]`
  - `tests/test_tagging_engine.py::test_an_undecodable_image_in_a_filled_block_is_an_error_not_ok[truncated-jpeg]`
  - `tests/test_tagging_engine.py::test_one_unrepairable_block_leaves_every_block_as_it_was`

Old text:

```
        return ArtRepair(REPAIR_ERROR, f"a picture could not be repaired: {exc}")
```

New text:

```
        log.debug("a picture could not be repaired: %s", exc)
```

### `u84-a.A13_read_failure_never_raises`

A FLAC mutagen cannot open raises out of the repair, which aborts the item

- File: `src/cratekit/core/art.py`
- Source: `u84-a.json`, row `A13_read_failure_never_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_art.py`
- Collected: 245 against a baseline of 245
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_an_unreadable_flac_is_an_error_and_never_raises`

Old text:

```
        return ArtRepair(REPAIR_ERROR, f"could not read {path.name}: {exc}")
```

New text:

```
        raise
```

### `u84-a.A1_zero_width`

A block declaring a zero width is no longer broken, so a vendored block with only its width zeroed would stay blank

- File: `src/cratekit/core/art.py`
- Source: `u84-a.json`, row `A1_zero_width`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_art.py`
- Collected: 245 against a baseline of 245
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_any_one_zeroed_dimension_is_broken[dims0]`

Old text:

```
    if block.width == 0 or block.height == 0 or block.depth == 0:
```

New text:

```
    if block.height == 0 or block.depth == 0:
```

### `u84-a.A2_zero_height`

A block declaring a zero height is no longer broken

- File: `src/cratekit/core/art.py`
- Source: `u84-a.json`, row `A2_zero_height`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_art.py`
- Collected: 245 against a baseline of 245
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_any_one_zeroed_dimension_is_broken[dims1]`

Old text:

```
    if block.width == 0 or block.height == 0 or block.depth == 0:
```

New text:

```
    if block.width == 0 or block.depth == 0:
```

### `u84-a.A5_not_jpeg_is_broken`

A PNG in a filled block is left as it is

- File: `src/cratekit/core/art.py`
- Source: `u84-a.json`, row `A5_not_jpeg_is_broken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_art.py`
- Collected: 245 against a baseline of 245
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_png_in_a_filled_block_is_re_encoded_as_a_baseline_jpeg`

Old text:

```
    return measured is None or measured.format != "JPEG" or measured.progressive
```

New text:

```
    return measured is None or measured.progressive
```

### `u84-a.A6_progressive_is_broken`

A progressive JPEG in a filled block is left as it is, the other way a Pioneer player renders blank

- File: `src/cratekit/core/art.py`
- Source: `u84-a.json`, row `A6_progressive_is_broken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_art.py`
- Collected: 245 against a baseline of 245
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_progressive_jpeg_with_sound_dimensions_becomes_baseline`

Old text:

```
    return measured is None or measured.format != "JPEG" or measured.progressive
```

New text:

```
    return measured is None or measured.format != "JPEG"
```

### `u84-a.A7_sound_art_not_written`

A file whose art is sound is saved anyway and reported fixed, so its mtime moves

- File: `src/cratekit/core/art.py`
- Source: `u84-a.json`, row `A7_sound_art_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_art.py`
- Collected: 245 against a baseline of 245
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_sound_art_is_not_rewritten_and_its_mtime_is_unchanged`

Old text:

```
    if not broken:
        return ArtRepair(REPAIR_OK)
```

New text:

```
    if False:
        return ArtRepair(REPAIR_OK)
```

### `u84-a.A8_no_picture_is_none`

A file with no picture reports ok rather than none

- File: `src/cratekit/core/art.py`
- Source: `u84-a.json`, row `A8_no_picture_is_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_art.py`
- Collected: 245 against a baseline of 245
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_art_repair_reaches_the_artifact_and_the_summary_counts_every_status`
  - `tests/test_tagging_engine.py::test_a_file_with_no_picture_reports_none_and_is_not_written`

Old text:

```
    if not blocks:
        return ArtRepair(REPAIR_NONE)
```

New text:

```
    if False:
        return ArtRepair(REPAIR_NONE)
```

### `u84-a.A9_non_flac_unchecked`

A container that is not FLAC reports none, which says it has no art when nothing looked

- File: `src/cratekit/core/art.py`
- Source: `u84-a.json`, row `A9_non_flac_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_art.py`
- Collected: 245 against a baseline of 245
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_container_that_is_not_flac_is_unchecked_rather_than_none`

Old text:

```
        return ArtRepair(REPAIR_UNCHECKED, f"{path.suffix or 'no suffix'} is not repaired")
```

New text:

```
        return ArtRepair(REPAIR_NONE, f"{path.suffix or 'no suffix'} is not repaired")
```

### `u84-a4.A4_undecodable_is_broken`

Re-measure after the fix commit. Data that does not decode is read as sound, absence read as evidence of absence

- File: `src/cratekit/core/art.py`
- Source: `u84-a4.json`, row `A4_undecodable_is_broken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_art.py`
- Collected: 245 against a baseline of 245
- Kills: 2 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_an_undecodable_image_in_a_filled_block_is_an_error_not_ok[not-an-image]`
  - `tests/test_tagging_engine.py::test_an_undecodable_image_in_a_filled_block_is_an_error_not_ok[truncated-jpeg]`

Old text:

```
    return measured is None or measured.format != "JPEG" or measured.progressive
```

New text:

```
    return measured is not None and (measured.format != "JPEG" or measured.progressive)
```

### `u84-b.A14_save_failure_never_raises`

A save that fails raises out of the repair, which aborts the item

- File: `src/cratekit/core/art.py`
- Source: `u84-b.json`, row `A14_save_failure_never_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_art.py`
- Collected: 245 against a baseline of 245
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_save_that_fails_is_an_error_and_never_raises`

Old text:

```
        return ArtRepair(REPAIR_ERROR, f"the repaired art could not be saved: {exc}")
```

New text:

```
        raise
```

### `u84-b.A15_sound_blocks_kept`

Only the repaired blocks are written back, so a sound back cover beside a broken front one is deleted

- File: `src/cratekit/core/art.py`
- Source: `u84-b.json`, row `A15_sound_blocks_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_art.py`
- Collected: 245 against a baseline of 245
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_sound_block_beside_a_broken_one_is_kept_as_it_was_and_in_order`

Old text:

```
        for block in blocks:
            handle.add_picture(block)
```

New text:

```
        for block in broken:
            handle.add_picture(block)
```

### `u84-b.A16_shrink_fallback`

A picture over the cap at native size is refused again, the review's finding, leaving it blank

- File: `src/cratekit/core/art.py`
- Source: `u84-b.json`, row `A16_shrink_fallback`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_art.py`
- Collected: 245 against a baseline of 245
- Kills: 2 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_picture_inside_the_box_that_cannot_fit_is_an_error_and_is_never_enlarged`
  - `tests/test_tagging_engine.py::test_a_picture_too_large_for_the_cap_at_native_size_is_shrunk_not_left_blank`

Old text:

```
        if _measure(data) is None:
            raise
```

New text:

```
        raise
```

### `u84-b.A17_too_small_to_shrink`

The guard that refuses to shrink a picture already inside the box is removed

- File: `src/cratekit/core/art.py`
- Source: `u84-b.json`, row `A17_too_small_to_shrink`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_art.py`
- Collected: 245 against a baseline of 245
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_picture_inside_the_box_that_cannot_fit_is_an_error_and_is_never_enlarged`

Old text:

```
    if max(img.size) <= ART_SIZE:
```

New text:

```
    if max(img.size) < 0:
```

### `u84-b.A18_shrink_keeps_shape`

The shrink squares the picture instead of fitting it in the box, stretching a non square cover

- File: `src/cratekit/core/art.py`
- Source: `u84-b.json`, row `A18_shrink_keeps_shape`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_art.py`
- Collected: 245 against a baseline of 245
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_picture_too_large_for_the_cap_at_native_size_is_shrunk_not_left_blank`

Old text:

```
    img.thumbnail((ART_SIZE, ART_SIZE), Image.LANCZOS)
```

New text:

```
    img = img.resize((ART_SIZE, ART_SIZE), Image.LANCZOS)
```

### `u84-b.A19_mime_rewritten`

A repaired PNG block keeps claiming image/png over JPEG bytes

- File: `src/cratekit/core/art.py`
- Source: `u84-b.json`, row `A19_mime_rewritten`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_art.py`
- Collected: 245 against a baseline of 245
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_png_in_a_filled_block_is_re_encoded_as_a_baseline_jpeg`

Old text:

```
            block.mime = JPEG_MIME
            block.width, block.height
```

New text:

```
            block.width, block.height
```

### `example-binaries-five-row.B1_broken_override_falls_through`

find() returns a broken per-binary override as if it worked, instead of None. The guard exists so a set-but-broken override never falls through to a different binary.

- File: `src/cratekit/core/binaries.py`
- Source: `example-binaries-five-row.json`, row `B1_broken_override_falls_through`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_binaries.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_binaries.py::test_find_never_raises_because_doctor_reports_on_all_of_them`

Old text:

```
        return override if _executable(Path(override)) else None

```

New text:

```
        return override

```

### `example-binaries-five-row.B3_platform_binary_remedy`

A platform-provided binary reports INSTALL_BINARY instead of UNSUPPORTED_PLATFORM, so the CLI would tell a user to install something the operating system ships.

- File: `src/cratekit/core/binaries.py`
- Source: `example-binaries-five-row.json`, row `B3_platform_binary_remedy`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_binaries.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_binaries.py::test_the_binary_failures_carry_four_different_remedies`

Old text:

```
            remedy=Remedy.UNSUPPORTED_PLATFORM,

```

New text:

```
            remedy=Remedy.INSTALL_BINARY,

```

### `example-binaries-five-row.B4_unknown_source_remedy`

Collapse the two None-hint cases onto one remedy token, which is the exact distinction the docstring says must not live in a None-check on a second attribute.

- File: `src/cratekit/core/binaries.py`
- Source: `example-binaries-five-row.json`, row `B4_unknown_source_remedy`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_binaries.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_binaries.py::test_the_binary_failures_carry_four_different_remedies`

Old text:

```
        remedy=Remedy.INSTALL_BINARY if hint is not None else Remedy.INSTALL_BINARY_SOURCE_UNKNOWN,

```

New text:

```
        remedy=Remedy.INSTALL_BINARY,

```

### `example-binaries-five-row.B5_credential_strip`

subprocess_env() stops stripping Cratekit credentials, so every spawned third-party binary receives a copy and the credential reaches a process listing.

- File: `src/cratekit/core/binaries.py`
- Source: `example-binaries-five-row.json`, row `B5_credential_strip`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_binaries.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_binaries.py::test_a_spawned_process_does_not_inherit_an_opted_in_credential`

Old text:

```
        if not key.startswith(secrets.ENV_CREDENTIAL_PREFIX)

```

New text:

```
        if True

```

### `u104-e.E5_install_hint_steps`

Drop the install step from the yt-dlp-missing refusal, so a missing binary refuses without saying how to get it

- File: `src/cratekit/core/binary_refusal.py`
- Source: `u104-e.json`, row `E5_install_hint_steps`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`
- Collected: 118 against a baseline of 118
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_missing_yt_dlp_refuses_a_url_with_the_install_hint`
  - `tests/test_acquire_fallback.py::test_a_broken_override_is_its_own_refusal`
  - `tests/test_acquire_fallback.py::test_a_missing_binary_refuses_with_the_install_hint`
  - `tests/test_acquire_fallback_fetch.py::test_a_missing_yt_dlp_parks_the_job_rather_than_failing_every_item`

Old text:

```
            if hint is not None
            else ()
        ),
        scope=Scope.RUN,
```

New text:

```
            if hint is None
            else ()
        ),
        scope=Scope.RUN,
```

### `u241.M09_ceiling_ignores_the_reserve`

worker_ceiling: every core, nothing kept back for the driver

- File: `src/cratekit/core/cores.py`
- Source: `u241.json`, row `M09_ceiling_ignores_the_reserve`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cores.py`, `tests/test_analysis_ahead.py`
- Collected: 314 against a baseline of 314
- Kills: 14 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_healthy_machine_says_how_many_workers_and_that_the_ceiling_held_it`
  - `tests/test_analysis_ahead.py::test_a_machine_deep_in_swap_runs_one_worker_and_names_the_swap_gate`
  - `tests/test_analysis_ahead.py::test_a_machine_using_most_of_its_memory_names_the_used_percent_gate`
  - `tests/test_analysis_ahead.py::test_memory_overrules_a_wide_core_count`
  - `tests/test_analysis_ahead.py::test_the_cost_is_set_by_the_costliest_track_in_the_batch`
  - `tests/test_analysis_ahead.py::test_the_light_pool_is_refused_by_the_gates_whatever_the_cores_say`
  - `tests/test_analysis_ahead.py::test_two_cores_leave_no_ceiling_for_a_pool`
  - `tests/test_cores.py::test_a_ceiling_from_many_cores_never_widens_what_memory_affords`
  - `tests/test_cores.py::test_the_ceiling_is_the_cores_less_what_is_kept_back_and_never_under_one[11-2-9]`
  - `tests/test_cores.py::test_the_ceiling_is_the_cores_less_what_is_kept_back_and_never_under_one[2-2-1]`
  - `tests/test_cores.py::test_the_ceiling_is_the_cores_less_what_is_kept_back_and_never_under_one[3-2-1]`
  - `tests/test_cores.py::test_the_ceiling_is_the_cores_less_what_is_kept_back_and_never_under_one[4-2-2]`
  - `tests/test_cores.py::test_the_ceiling_is_the_cores_less_what_is_kept_back_and_never_under_one[8-1-7]`
  - `tests/test_cores.py::test_the_reader_is_looked_up_when_called_so_a_test_can_stand_in`

Old text:

```
    return max(1, cores - reserved)

```

New text:

```
    return max(1, cores)

```

### `u93-recursive-analysis.D10_sorted_items`

Return the items in walk order rather than sorted

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D10_sorted_items`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_scan_holds_exactly_the_audio_files_it_should[nested-every-file-once-sorted]`

Old text:

```
        items=tuple(sorted(items)),
```

New text:

```
        items=tuple(items),
```

### `u93-recursive-analysis.D11_absolute_id`

Drop the absolute clause from item_path, so an absolute id discards the frozen folder

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D11_absolute_id`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_discovery.py::test_an_absolute_id_is_refused_rather_than_discarding_the_folder`

Old text:

```
    if candidate.is_absolute() or ".." in candidate.parts:
```

New text:

```
    if ".." in candidate.parts:
```

### `u93-recursive-analysis.D12_parent_id`

Drop the dot dot clause from item_path, so an id walks out of the frozen folder

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D12_parent_id`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 3 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_parent_segment_is_refused`
  - `tests/test_discovery.py::test_the_refusal_names_the_folder_it_was_leaving`
  - `tests/test_vocals_cli.py::test_a_vocals_item_that_would_leave_the_frozen_folder_is_refused`

Old text:

```
    if candidate.is_absolute() or ".." in candidate.parts:
        raise _escapes(folder, item_id)
```

New text:

```
    if candidate.is_absolute():
        raise _escapes(folder, item_id)
```

### `u93-recursive-analysis.D13_singular`

Drop the singular branch, so one declined folder reads as 1 folders

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D13_singular`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 2 (killed)
- Killed:
  - `tests/test_discovery.py::test_one_declined_link_reads_as_one_folder_and_not_as_one_folders`
  - `tests/test_discovery.py::test_the_unreadable_warning_is_its_own_code_with_its_own_remedy`

Old text:

```
    return f"{count} folder" if count == 1 else f"{count} folders"
```

New text:

```
    return f"{count} folders"
```

### `u93-recursive-analysis.D15_unreadable_empty`

unreadable_warning reports over an empty list, the same false omission on the other code

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D15_unreadable_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 8 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_payload_from_a_build_that_never_walked_a_tree_says_nothing`
  - `tests/test_discovery.py::test_a_payload_whose_lists_are_the_wrong_shape_says_nothing_rather_than_raising`
  - `tests/test_discovery.py::test_a_resume_says_what_the_queue_said_from_the_payload_alone`
  - `tests/test_discovery.py::test_one_declined_link_reads_as_one_folder_and_not_as_one_folders`
  - `tests/test_discovery.py::test_the_warning_names_the_links_and_counts_the_rest`
  - `tests/test_discovery.py::test_there_is_nothing_to_say_when_no_link_was_declined`
  - `tests/test_vocals_cli.py::test_a_one_level_vocals_resume_says_nothing_about_a_walk_it_never_did`
  - `tests/test_vocals_cli.py::test_an_oversize_track_is_refused_by_the_restamp_verb_and_keeps_its_tags`

Old text:

```
    """What a recursive walk could not list, phrased for an envelope."""
    if not paths:
        return None

```

New text:

```
    """What a recursive walk could not list, phrased for an envelope."""

```

### `u93-recursive-analysis.D16_none_filter`

walk_warnings stops dropping the Nones, so an envelope carries a null warning

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D16_none_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 29 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_payload_from_a_build_that_never_walked_a_tree_says_nothing`
  - `tests/test_discovery.py::test_a_payload_whose_lists_are_the_wrong_shape_says_nothing_rather_than_raising`
  - `tests/test_discovery.py::test_a_resume_repeats_the_unreadable_half_and_not_only_the_links`
  - `tests/test_discovery.py::test_a_resume_says_what_the_queue_said_from_the_payload_alone`
  - `tests/test_discovery.py::test_an_error_carrying_no_filename_is_still_reported`
  - `tests/test_discovery.py::test_one_declined_link_reads_as_one_folder_and_not_as_one_folders`
  - `tests/test_discovery.py::test_the_unreadable_warning_is_its_own_code_with_its_own_remedy`
  - `tests/test_discovery.py::test_the_warning_names_the_links_and_counts_the_rest`
  - `tests/test_discovery.py::test_there_is_nothing_to_say_when_no_link_was_declined`
  - `tests/test_vocals_cli.py::test_a_file_finalized_with_no_voxlevel_is_scored_once_the_model_is_bound`
  - `tests/test_vocals_cli.py::test_a_folder_with_no_audio_queues_nothing`
  - `tests/test_vocals_cli.py::test_a_nested_file_deleted_after_the_vocals_queue_refuses_that_item_only`
  - `tests/test_vocals_cli.py::test_a_nested_sidecar_and_a_dot_directory_are_not_vocals_items`
  - `tests/test_vocals_cli.py::test_a_one_level_vocals_resume_says_nothing_about_a_walk_it_never_did`
  - `tests/test_vocals_cli.py::test_a_prefixed_file_is_scored_by_analyze_vocals_and_not_skipped`
  - ... and 14 more, see the JSON sidecar

Old text:

```
    return tuple(one for one in said if one is not None)
```

New text:

```
    return said
```

### `u93-recursive-analysis.D17_and_more`

Drop the and N more tail, so a warning names five and silently omits the rest

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D17_and_more`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_discovery.py::test_the_warning_names_the_links_and_counts_the_rest`

Old text:

```
    return ", ".join(shown) + (f", and {rest} more" if rest else "")
```

New text:

```
    return ", ".join(shown)
```

### `u93-recursive-analysis.D18_strings_shape`

Drop the shape check on a frozen payload list, so a string payload is read character by character

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D18_strings_shape`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_payload_whose_lists_are_the_wrong_shape_says_nothing_rather_than_raising`

Old text:

```
    if not isinstance(value, (list, tuple)):
        return ()
    return tuple(str(one) for one in value)
```

New text:

```
    return tuple(str(one) for one in value or ())
```

### `u93-recursive-analysis.D19_resume_half`

warnings_of reads only the links, so an unreadable folder is on the queue and never on the resume

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D19_resume_half`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_resume_repeats_the_unreadable_half_and_not_only_the_links`

Old text:

```
    return walk_warnings(
        _strings(held.get(PAYLOAD_SKIPPED_LINKS)),
        _strings(held.get(PAYLOAD_UNREADABLE)),
    )
```

New text:

```
    return walk_warnings(_strings(held.get(PAYLOAD_SKIPPED_LINKS)))
```

### `u93-recursive-analysis.D1_dotfile`

Drop the dotfile clause from _is_audio, which is what lets an AppleDouble sidecar become an item

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D1_dotfile`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 2 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_scan_holds_exactly_the_audio_files_it_should[appledouble-sidecar-skipped]`
  - `tests/test_vocals_cli.py::test_a_nested_sidecar_and_a_dot_directory_are_not_vocals_items`

Old text:

```
        path.is_file()
        and not path.name.startswith(".")
        and path.suffix.lower() in AUDIO_EXTS
```

New text:

```
        path.is_file()
        and path.suffix.lower() in AUDIO_EXTS
```

### `u93-recursive-analysis.D20_frozen_links`

frozen stops recording the declined links, so the resume has nothing to read back

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D20_frozen_links`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 2 (killed)
- Killed:
  - `tests/test_discovery.py::test_the_frozen_payload_carries_the_mode_and_both_omissions`
  - `tests/test_vocals_cli.py::test_the_vocals_resume_repeats_what_the_walk_left_out`

Old text:

```
        PAYLOAD_SKIPPED_LINKS: list(scan.skipped_links),
```

New text:

```
        PAYLOAD_SKIPPED_LINKS: [],
```

### `u93-recursive-analysis.D2_is_file`

is_file becomes exists, so a directory named track.flac becomes an item

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D2_is_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_directory_carrying_an_audio_suffix_is_not_an_item`

Old text:

```
        path.is_file()
        and not path.name.startswith(".")
```

New text:

```
        path.exists()
        and not path.name.startswith(".")
```

### `u93-recursive-analysis.D3_suffix`

Drop the audio suffix clause, so cover art and text files become items

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D3_suffix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_scan_holds_exactly_the_audio_files_it_should[non-audio-suffix]`

Old text:

```
        and not path.name.startswith(".")
        and path.suffix.lower() in AUDIO_EXTS
    )
```

New text:

```
        and not path.name.startswith(".")
    )
```

### `u93-recursive-analysis.D4_default_mode`

Drop the one level early return, so every caller walks the tree whether it asked or not

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D4_default_mode`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 3 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_one_level_scan_reports_no_links_even_when_one_is_there`
  - `tests/test_discovery.py::test_a_scan_holds_exactly_the_audio_files_it_should[one-level-default-skips-a-subfolder]`
  - `tests/test_vocals_cli.py::test_a_vocals_pass_without_the_flag_stays_one_level`

Old text:

```
    if not recursive:
        return Scan(
            items=tuple(sorted(path.name for path in folder.iterdir() if _is_audio(path))),
            skipped_links=(),
            unreadable=(),
        )

```

New text:

```
(empty)
```

### `u93-recursive-analysis.D5_dot_directory`

Stop pruning dot directories, so .Trashes and .Spotlight-V100 are walked

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D5_dot_directory`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 2 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_scan_holds_exactly_the_audio_files_it_should[dot-directory-not-descended]`
  - `tests/test_vocals_cli.py::test_a_nested_sidecar_and_a_dot_directory_are_not_vocals_items`

Old text:

```
            if name.startswith("."):
                continue
            if (here / name).is_symlink():
```

New text:

```
            if (here / name).is_symlink():
```

### `u93-recursive-analysis.D6_link_declined`

Walk a directory symlink and report nothing, which is the loop hazard and the silent skip at once

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D6_link_declined`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 6 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_symlinked_directory_is_not_walked_and_is_reported`
  - `tests/test_discovery.py::test_one_declined_link_reads_as_one_folder_and_not_as_one_folders`
  - `tests/test_discovery.py::test_the_frozen_payload_carries_the_mode_and_both_omissions`
  - `tests/test_discovery.py::test_the_warning_names_the_links_and_counts_the_rest`
  - `tests/test_vocals_cli.py::test_a_recursive_vocals_pass_says_which_linked_folders_it_did_not_walk`
  - `tests/test_vocals_cli.py::test_the_vocals_resume_repeats_what_the_walk_left_out`

Old text:

```
            if (here / name).is_symlink():
                skipped.append(_relative(folder, here / name))
                continue
            kept.append(name)
```

New text:

```
            kept.append(name)
```

### `u93-recursive-analysis.D7_prune_in_place`

Assign the filtered list to a new name instead of the slice, which leaves os.walk descending everything

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D7_prune_in_place`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 2 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_scan_holds_exactly_the_audio_files_it_should[dot-directory-not-descended]`
  - `tests/test_vocals_cli.py::test_a_nested_sidecar_and_a_dot_directory_are_not_vocals_items`

Old text:

```
        dirnames[:] = kept
```

New text:

```
        dirnames = kept  # noqa: F841
```

### `u94-b.W9_walk_warning_says_queued`

discovery.walk_warnings: ignore the verb for a declined link, so calibrate tells a person about a queue it does not have

- File: `src/cratekit/core/discovery.py`
- Source: `u94-b.json`, row `W9_walk_warning_says_queued`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_walk_that_left_a_folder_out_is_not_the_library`

Old text:

```
        link_warning(tuple(skipped_links), verb),
```

New text:

```
        link_warning(tuple(skipped_links)),
```

### `u185.F11_difference_memberships`

differences: compare no membership rows, so raw SQL on a pushed membership passes

- File: `src/cratekit/core/foreign_tree.py`
- Source: `u185.json`, row `F11_difference_memberships`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_foreign_tree.py::test_raw_sql_into_the_folder_is_seen_by_the_reading_again_from_sql`

Old text:

```
        if old == new:
            continue
```

New text:

```
        if True:
            continue
```

### `u185.F12_difference_appeared`

differences: read a row that appeared in the folder since open as nothing

- File: `src/cratekit/core/foreign_tree.py`
- Source: `u185.json`, row `F12_difference_appeared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_foreign_tree.py::test_a_push_that_lands_while_a_handle_is_open_refuses_that_handles_commit`

Old text:

```
            found.append(f"the {_PLAYLISTS} row {key!r} appeared under {OWNER}'s folder")
```

New text:

```
            pass
```

### `u185.F1_root_must_be_a_folder`

is_foreign_root: drop the folder test, so a plain playlist named DEADCA7 at the top is foreign

- File: `src/cratekit/core/foreign_tree.py`
- Source: `u185.json`, row `F1_root_must_be_a_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`
- Collected: 31 against a baseline of 31
- Kills: 4 (killed)
- Killed:
  - `tests/test_foreign_tree.py::test_nothing_else_is_a_foreign_root[DEADCA7-root-0-a plain playlist of the name is not the shape the push writes]`
  - `tests/test_foreign_tree.py::test_nothing_else_is_a_foreign_root[DEADCA7-root-4-a smart playlist of the name is not either]`
  - `tests/test_foreign_tree.py::test_nothing_else_is_a_foreign_root[DEADCA7-root-None-a row that cannot say it is a folder is not one]`
  - `tests/test_foreign_tree.py::test_nothing_else_is_a_foreign_root[DEADCA7-root-x-nor one whose kind is not a number]`

Old text:

```
    return folder and str(name) in FOREIGN_ROOT_NAMES and parent in _root_parents()
```

New text:

```
    return str(name) in FOREIGN_ROOT_NAMES and parent in _root_parents()
```

### `u185.F2_root_must_be_at_the_top`

is_foreign_root: drop the root parent test, so a namesake folder below the top is foreign

- File: `src/cratekit/core/foreign_tree.py`
- Source: `u185.json`, row `F2_root_must_be_at_the_top`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`, `tests/test_favorites_placement.py`
- Collected: 97 against a baseline of 97
- Kills: 4 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_a_playlist_of_the_sources_name_inside_deadca7s_folder_is_not_a_second_source`
  - `tests/test_foreign_tree.py::test_every_node_under_the_root_is_foreign_at_any_depth_and_nothing_beside_it`
  - `tests/test_foreign_tree.py::test_nothing_else_is_a_foreign_root[DEADCA7-12-1-a folder of the name below the top is a namesake]`
  - `tests/test_foreign_tree.py::test_the_reading_at_open_names_the_push_and_not_a_namesake_below_the_top`

Old text:

```
    return folder and str(name) in FOREIGN_ROOT_NAMES and parent in _root_parents()
```

New text:

```
    return folder and str(name) in FOREIGN_ROOT_NAMES
```

### `u185.F3_descendants_walked`

ids_of: walk no children, so only the root row is foreign and its playlists are anyone's

- File: `src/cratekit/core/foreign_tree.py`
- Source: `u185.json`, row `F3_descendants_walked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`, `tests/test_favorites_placement.py`, `tests/test_genre_favorites.py`
- Collected: 142 against a baseline of 142
- Kills: 9 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_a_playlist_of_the_sources_name_inside_deadca7s_folder_is_not_a_second_source`
  - `tests/test_foreign_tree.py::test_a_cycle_ends_the_walk_rather_than_looping`
  - `tests/test_foreign_tree.py::test_a_pushed_playlist_moved_out_of_the_folder_is_refused`
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[membership-added]`
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[membership-rewritten-to-another-owner]`
  - `tests/test_foreign_tree.py::test_every_node_under_the_root_is_foreign_at_any_depth_and_nothing_beside_it`
  - `tests/test_foreign_tree.py::test_raw_sql_into_the_folder_is_seen_by_the_reading_again_from_sql`
  - `tests/test_foreign_tree.py::test_the_reading_at_open_names_the_push_and_not_a_namesake_below_the_top`
  - `tests/test_genre_favorites.py::test_a_source_namesake_inside_deadca7s_folder_is_not_a_second_source`

Old text:

```
        queue.extend(children.get(node, ()))
```

New text:

```
        pass
```

### `u185.F4_create_inside`

pending_touches: admit a playlist created inside the folder

- File: `src/cratekit/core/foreign_tree.py`
- Source: `u185.json`, row `F4_create_inside`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[playlist-made-inside]`

Old text:

```
            if op == "create" and parent in ids:
```

New text:

```
            if op == "create" and parent in ids and False:
```

### `u185.F5_second_root`

pending_touches: admit a second DEADCA7 folder created at the top

- File: `src/cratekit/core/foreign_tree.py`
- Source: `u185.json`, row `F5_second_root`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_foreign_tree.py::test_a_second_folder_of_the_name_at_the_top_is_refused`

Old text:

```
            elif op == "create" and is_foreign_root(
```

New text:

```
            elif op == "create" and False and is_foreign_root(
```

### `u185.F7_modify_inside`

pending_touches: admit any change to a row of the folder

- File: `src/cratekit/core/foreign_tree.py`
- Source: `u185.json`, row `F7_modify_inside`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[folder-renamed]`

Old text:

```
            elif op == "modify" and key in ids:
```

New text:

```
            elif op == "modify" and key in ids and False:
```

### `u185.F8_moved_in`

pending_touches: admit a node of one's own moved into the folder

- File: `src/cratekit/core/foreign_tree.py`
- Source: `u185.json`, row `F8_moved_in`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_foreign_tree.py::test_a_playlist_of_ones_own_moved_into_the_folder_is_refused`

Old text:

```
            elif op == "modify" and parent in ids:
```

New text:

```
            elif op == "modify" and parent in ids and False:
```

### `u185.F9_membership`

pending_touches: read a membership by its owner alone, so one rewritten to another playlist passes

- File: `src/cratekit/core/foreign_tree.py`
- Source: `u185.json`, row `F9_membership`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[membership-rewritten-to-another-owner]`

Old text:

```
            if owner in ids or str(getattr(obj, "ID", "")) in reading.memberships:
```

New text:

```
            if owner in ids:
```

### `r289-b.D1_no_chunking`

Ask about every name in one statement, past the parameter limit

- File: `src/cratekit/core/jobs.py`
- Source: `r289-b.json`, row `D1_no_chunking`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 2553 against a baseline of 2553
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
- Collected: 2553 against a baseline of 2553
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

### `r290-author.J1_blocked_branch_removed`

Skip the blocked branch of raise_for_state, so a parked job falls through to the closed predicate that cannot see it, which is R-290 itself

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `J1_blocked_branch_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_outcome.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 2679 against a baseline of 2679
- Kills: 49 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_provider_block_parks_the_job_and_makes_no_further_request`
  - `tests/test_acquire_workers.py::test_an_authentication_failure_parks_the_run_and_names_the_replacement_path`
  - `tests/test_adopt_workers.py::test_a_parked_adoption_leaves_blocked_and_non_zero`
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
  - `tests/test_job_outcome.py::test_a_blocked_job_raises_the_blocked_type_carrying_the_jobs_own_cause`
  - `tests/test_job_outcome.py::test_a_blocked_job_recording_no_reason_is_still_not_a_success`
  - `tests/test_job_outcome.py::test_a_park_on_a_gate_coded_cause_is_still_not_resumable_through_the_run`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.bandcamp-fetch]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.download]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.fallback-fetch]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[adopt.scan]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[analyze.restamp]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[analyze.run]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[analyze.vocals]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[backup.run]`
  - ... and 34 more, see the JSON sidecar

Old text:

```
    if job.state is JobState.BLOCKED:
        # ``transition`` refuses
```

New text:

```
    if False and job.state is JobState.BLOCKED:
        # ``transition`` refuses
```

### `r290-author.J2_blocked_raises_the_plain_type`

Raise a plain CratekitError for a parked job, so the verb exits non zero and the outcome word says failed

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `J2_blocked_raises_the_plain_type`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_outcome.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 2679 against a baseline of 2679
- Kills: 48 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_provider_block_parks_the_job_and_makes_no_further_request`
  - `tests/test_acquire_workers.py::test_an_authentication_failure_parks_the_run_and_names_the_replacement_path`
  - `tests/test_adopt_workers.py::test_a_parked_adoption_leaves_blocked_and_non_zero`
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
  - `tests/test_job_outcome.py::test_a_blocked_job_raises_the_blocked_type_carrying_the_jobs_own_cause`
  - `tests/test_job_outcome.py::test_a_park_on_a_gate_coded_cause_is_still_not_resumable_through_the_run`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.bandcamp-fetch]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.download]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.fallback-fetch]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[adopt.scan]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[analyze.restamp]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[analyze.run]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[analyze.vocals]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[backup.run]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[export.playlist]`
  - ... and 33 more, see the JSON sidecar

Old text:

```
        raise JobBlocked(job.cause)
```

New text:

```
        raise CratekitError(job.cause)
```

### `r290-author.J3_closed_branch_removed`

Drop the closed and carrying a cause branch, so a half failed or cancelled job is reported, which is R-225 in every verb at once

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `J3_closed_branch_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_outcome.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 2679 against a baseline of 2679
- Kills: 112 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_failure_mid_set_fails_that_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/test_acquire_workers.py::test_a_mid_batch_defect_fails_that_item_and_the_resume_the_job_refuses_fetches_nothing`
  - `tests/test_acquire_workers.py::test_a_refusal_beside_a_network_failure_fails_and_keeps_the_refusal_skipped`
  - `tests/test_acquire_workers.py::test_three_landed_and_one_network_failure_still_fails`
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item`
  - `tests/test_adopt_workers.py::test_a_row_tombstoned_between_queueing_and_driving_fails_its_own_item`
  - `tests/test_adopt_workers.py::test_an_interrupted_job_exits_with_its_own_cause_and_not_ok[adopt.apply]`
  - `tests/test_adopt_workers.py::test_an_interrupted_job_exits_with_its_own_cause_and_not_ok[adopt.scan]`
  - `tests/test_analysis_workers.py::test_a_deleted_source_beside_an_unrelated_twin_is_refused_not_reported_analysed`
  - `tests/test_analysis_workers.py::test_a_job_the_shipped_code_left_with_no_intent_resumes_from_its_staged_report`
  - `tests/test_analysis_workers.py::test_a_nested_file_deleted_after_the_queue_refuses_that_item_only`
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - `tests/test_analysis_workers.py::test_a_taken_target_name_fails_the_item_and_keeps_the_written_head_in_the_title`
  - `tests/test_analysis_workers.py::test_an_interrupt_after_a_renamed_items_report_is_staged_resumes_by_the_printed_command`
  - `tests/test_analysis_workers.py::test_an_interrupted_restamp_names_its_job_command_and_that_command_finishes_it`
  - ... and 97 more, see the JSON sidecar

Old text:

```
    if not job.is_open() and job.cause is not None:
        if job.state is JobState.CANCELLED:
```

New text:

```
    if False and not job.is_open() and job.cause is not None:
        if job.state is JobState.CANCELLED:
```

### `r290-author.J4_predicate_narrowed_to_failed`

Narrow the closed predicate to FAILED alone, so a run stopped by a signal is reported through a normal envelope

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `J4_predicate_narrowed_to_failed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_outcome.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 2679 against a baseline of 2679
- Kills: 31 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_an_interrupted_job_exits_with_its_own_cause_and_not_ok[adopt.apply]`
  - `tests/test_adopt_workers.py::test_an_interrupted_job_exits_with_its_own_cause_and_not_ok[adopt.scan]`
  - `tests/test_analysis_workers.py::test_a_job_the_shipped_code_left_with_no_intent_resumes_from_its_staged_report`
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - `tests/test_analysis_workers.py::test_an_interrupt_after_a_renamed_items_report_is_staged_resumes_by_the_printed_command`
  - `tests/test_analysis_workers.py::test_an_interrupted_restamp_names_its_job_command_and_that_command_finishes_it`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.bandcamp-fetch]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.download]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.fallback-fetch]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[adopt.scan]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[analyze.restamp]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[analyze.run]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[analyze.vocals]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[backup.run]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[export.playlist]`
  - ... and 16 more, see the JSON sidecar

Old text:

```
    if not job.is_open() and job.cause is not None:
        if job.state is JobState.CANCELLED:
```

New text:

```
    if job.state is JobState.FAILED and job.cause is not None:
        if job.state is JobState.CANCELLED:
```

### `r290-author.J5_causeless_block_returns`

Return for a blocked job that records no reason, reading a missing reason as a missing problem

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `J5_causeless_block_returns`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_outcome.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 2679 against a baseline of 2679
- Kills: 1 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_blocked_job_recording_no_reason_is_still_not_a_success`

Old text:

```
        if job.cause is None:
            raise JobBlocked(
                refuse(
```

New text:

```
        if job.cause is None:
            return
            raise JobBlocked(
                refuse(
```

### `r290-author.J6_causeless_block_raises_the_plain_type`

Refuse a blocked job that records no reason as a plain error, so the envelope says failed over a row the job listing calls blocked

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `J6_causeless_block_raises_the_plain_type`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_outcome.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 2679 against a baseline of 2679
- Kills: 1 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_blocked_job_recording_no_reason_is_still_not_a_success`

Old text:

```
        if job.cause is None:
            raise JobBlocked(
                refuse(
```

New text:

```
        if job.cause is None:
            raise CratekitError(
                refuse(
```

### `r290-author.J7_cancelled_raises_the_plain_type`

Raise a plain CratekitError for a cancelled job, so a person who stopped a run is told it failed

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `J7_cancelled_raises_the_plain_type`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_outcome.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 2679 against a baseline of 2679
- Kills: 26 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_job_the_shipped_code_left_with_no_intent_resumes_from_its_staged_report`
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - `tests/test_analysis_workers.py::test_an_interrupt_after_a_renamed_items_report_is_staged_resumes_by_the_printed_command`
  - `tests/test_analysis_workers.py::test_an_interrupted_restamp_names_its_job_command_and_that_command_finishes_it`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.bandcamp-fetch]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.download]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.fallback-fetch]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[adopt.scan]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[analyze.restamp]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[analyze.run]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[analyze.vocals]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[backup.run]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[export.playlist]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[intake.playlist]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[intake.set]`
  - ... and 11 more, see the JSON sidecar

Old text:

```
            raise JobCancelled(job.cause)
```

New text:

```
            raise CratekitError(job.cause)
```

### `r380.G3_retryable_requires_every_item`

a mixed job is non retryable unless every failure is retryable

- File: `src/cratekit/core/jobs_drive.py`
- Source: `r380.json`, row `G3_retryable_requires_every_item`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 83 against a baseline of 83
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

### `r380.G5_permanent_failures_still_offer_resume`

the permanent branch still carries the resume-job remedy

- File: `src/cratekit/core/jobs_drive.py`
- Source: `r380.json`, row `G5_permanent_failures_still_offer_resume`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_label_workers.py`
- Collected: 165 against a baseline of 165
- Kills: 6 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_job_whose_every_item_failed_permanently_reports_itself_non_retryable[three-items]`
  - `tests/test_jobs.py::test_a_job_whose_every_item_failed_permanently_reports_itself_non_retryable[two-items]`
  - `tests/test_jobs.py::test_a_partial_failure_whose_failures_are_permanent_is_not_resumable`
  - `tests/test_jobs.py::test_two_distinct_permanent_reasons_name_both_whichever_failed_last`
  - `tests/test_label_workers.py::test_a_second_resume_of_a_failed_sweep_still_does_not_exit_ok`
  - `tests/test_label_workers.py::test_a_sweep_whose_failures_are_permanent_does_not_tell_the_person_to_resume`

Old text:

```
        Remediation(
            steps=(
                "the failed items cannot succeed on resume; inspect each item's cause",
            )
        ),

```

New text:

```
        Remediation(remedy=Remedy.RESUME_JOB),

```

### `r390-a.A2_retry_refuses_any_closed_job_with_a_cause`

the flag is not read: a cancelled job and a retryable failure are refused too

- File: `src/cratekit/core/jobs.py`
- Source: `r390-a.json`, row `A2_retry_refuses_any_closed_job_with_a_cause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_backup_cli.py`, `tests/test_outbound_workers.py`
- Collected: 307 against a baseline of 307
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

### `r390-a.A3_a_failed_job_with_no_cause_is_refused`

a missing verdict is read as a permanent one

- File: `src/cratekit/core/jobs.py`
- Source: `r390-a.json`, row `A3_a_failed_job_with_no_cause_is_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 83 against a baseline of 83
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
- Collected: 83 against a baseline of 83
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

### `r390-a.A5_refusal_drops_the_inner_cause`

the refusal no longer nests the job's own cause, so the item's reason is unreachable

- File: `src/cratekit/core/jobs.py`
- Source: `r390-a.json`, row `A5_refusal_drops_the_inner_cause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_master_cli.py`, `tests/test_acquire_workers.py`
- Collected: 225 against a baseline of 225
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

### `r390-b.B1_last_reason_restored`

the original defect: several permanent reasons take the last item's reason

- File: `src/cratekit/core/jobs_drive.py`
- Source: `r390-b.json`, row `B1_last_reason_restored`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 83 against a baseline of 83
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

- File: `src/cratekit/core/jobs_drive.py`
- Source: `r390-b.json`, row `B2_reasons_in_reverse_order`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 83 against a baseline of 83
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

- File: `src/cratekit/core/jobs_drive.py`
- Source: `r390-b.json`, row `B3_message_does_not_name_the_reasons`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 83 against a baseline of 83
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

- File: `src/cratekit/core/jobs_drive.py`
- Source: `r390-b.json`, row `B4_detail_drops_permanent_reasons`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 83 against a baseline of 83
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

- File: `src/cratekit/core/jobs_drive.py`
- Source: `r390-b.json`, row `B5_one_shared_reason_is_also_mixed`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 83 against a baseline of 83
- Kills: 3 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_job_whose_every_item_failed_permanently_reports_itself_non_retryable[three-items]`
  - `tests/test_jobs.py::test_a_job_whose_every_item_failed_permanently_reports_itself_non_retryable[two-items]`
  - `tests/test_jobs.py::test_a_partial_failure_whose_failures_are_permanent_is_not_resumable`

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
- Collected: 83 against a baseline of 83
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

- File: `src/cratekit/core/jobs_drive.py`
- Source: `r390-b.json`, row `B7_drive_passes_no_reasons_to_the_envelope`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 83 against a baseline of 83
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

### `r704-a.E2_job_verdict_needs_every_item_retryable`

existing guard sample: the job verdict is transient only when every failure is, so a mixed job reads permanent

- File: `src/cratekit/core/jobs_drive.py`
- Source: `r704-a.json`, row `E2_job_verdict_needs_every_item_retryable`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_outcome.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_provider_gate.py`, `tests/test_queued_resume_contract.py`, `tests/test_render_payloads.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 2851 against a baseline of 2851
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

### `u140.B3_refreeze_any_state`

jobs.refreeze drops the succeeded state check, so a job that may still run is rewritten

- File: `src/cratekit/core/jobs.py`
- Source: `u140.json`, row `B3_refreeze_any_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_refreeze_refuses_a_job_that_has_not_succeeded`

Old text:

```
        if current.state is not JobState.SUCCEEDED:
            raise refuse(
                "internal-error",
                f"job {job_id} is {current.state}, and only a succeeded job's frozen "

```

New text:

```
        if False:
            raise refuse(
                "internal-error",
                f"job {job_id} is {current.state}, and only a succeeded job's frozen "

```

### `u140.B4_refreeze_writes_nothing_new`

jobs.refreeze writes the payload back without the new value

- File: `src/cratekit/core/jobs.py`
- Source: `u140.json`, row `B4_refreeze_writes_nothing_new`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 7 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_job_whose_page_words_differ_renames_by_the_name_its_landing_recorded`
  - `tests/test_export_set_rename.py::test_a_job_with_no_frozen_name_is_found_by_the_queued_day_and_refrozen`
  - `tests/test_export_set_rename.py::test_a_ledger_left_under_the_old_key_is_moved_on_the_next_run`
  - `tests/test_export_set_rename.py::test_a_name_with_a_slash_freezes_as_the_library_spells_it`
  - `tests/test_export_set_rename.py::test_a_rename_that_failed_after_the_account_finishes_on_the_next_run`
  - `tests/test_export_set_rename.py::test_a_renamed_inspiration_playlist_renames_the_account_playlist_ledger_and_job`
  - `tests/test_export_set_rename.py::test_a_second_rename_is_a_no_op`

Old text:

```
        payload[key] = str(value)

```

New text:

```
        payload.setdefault(key, str(value))

```

### `u169.E1_declined_accepts_retryable`

Declined: drop the refusal of a retryable cause, so a transient failure can be skipped and never retried

- File: `src/cratekit/core/jobs_drive.py`
- Source: `u169.json`, row `E1_declined_accepts_retryable`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_acquire_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 2 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_handler_that_declines_a_retryable_cause_fails_the_item_rather_than_skipping_it`
  - `tests/test_jobs.py::test_a_retryable_cause_cannot_decline_an_item`

Old text:

```
        if cause.retryable:
            raise ValueError(
```

New text:

```
        if False:
            raise ValueError(
```

### `u169.E2_drive_fails_a_decline`

drive: no Declined clause, so a declined item falls to the failure boundary and fails the job

- File: `src/cratekit/core/jobs_drive.py`
- Source: `u169.json`, row `E2_drive_fails_a_decline`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_acquire_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 11 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_lossy_landing_under_strict_policy_is_refused_at_the_item_with_the_codec_named`
  - `tests/test_acquire_workers.py::test_a_refusal_beside_a_network_failure_fails_and_keeps_the_refusal_skipped`
  - `tests/test_acquire_workers.py::test_a_track_the_provider_no_longer_has_is_declined_as_well`
  - `tests/test_acquire_workers.py::test_the_declined_warnings_name_skipped_tracks_and_never_a_failed_one`
  - `tests/test_acquire_workers.py::test_the_human_output_says_ok_and_names_the_refused_track`
  - `tests/test_acquire_workers.py::test_the_warning_is_the_same_when_the_finished_job_is_asked_about_again`
  - `tests/test_acquire_workers.py::test_three_landed_and_one_refused_by_policy_ends_ok_with_a_warning_naming_it`
  - `tests/test_jobs.py::test_a_declined_item_is_skipped_with_its_cause_and_the_job_succeeds`
  - `tests/test_jobs.py::test_a_job_every_item_of_which_was_declined_succeeds_rather_than_failing`
  - `tests/test_jobs.py::test_a_real_failure_beside_a_declined_item_still_fails_the_job_and_names_both`
  - `tests/test_jobs.py::test_a_retry_re_arms_the_failure_and_leaves_the_declined_item_settled`

Old text:

```
                except Declined as exc:
```

New text:

```
                except Parked as exc:
```

### `u169.E3_decline_writes_failed`

decline_item: record the item failed rather than skipped

- File: `src/cratekit/core/jobs_drive.py`
- Source: `u169.json`, row `E3_decline_writes_failed`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_acquire_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 10 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_lossy_landing_under_strict_policy_is_refused_at_the_item_with_the_codec_named`
  - `tests/test_acquire_workers.py::test_a_refusal_beside_a_network_failure_fails_and_keeps_the_refusal_skipped`
  - `tests/test_acquire_workers.py::test_a_track_the_provider_no_longer_has_is_declined_as_well`
  - `tests/test_acquire_workers.py::test_the_declined_warnings_name_skipped_tracks_and_never_a_failed_one`
  - `tests/test_acquire_workers.py::test_the_human_output_says_ok_and_names_the_refused_track`
  - `tests/test_acquire_workers.py::test_the_warning_is_the_same_when_the_finished_job_is_asked_about_again`
  - `tests/test_acquire_workers.py::test_three_landed_and_one_refused_by_policy_ends_ok_with_a_warning_naming_it`
  - `tests/test_jobs.py::test_a_declined_item_is_skipped_with_its_cause_and_the_job_succeeds`
  - `tests/test_jobs.py::test_a_real_failure_beside_a_declined_item_still_fails_the_job_and_names_both`
  - `tests/test_jobs.py::test_a_retry_re_arms_the_failure_and_leaves_the_declined_item_settled`

Old text:

```
            (str(ItemState.SKIPPED), json.dumps(cause.to_json()), job_id, item_id),
```

New text:

```
            (str(ItemState.FAILED), json.dumps(cause.to_json()), job_id, item_id),
```

### `u169.E4_decline_drops_cause`

decline_item: keep no cause on the skipped item, so nothing can name why

- File: `src/cratekit/core/jobs_drive.py`
- Source: `u169.json`, row `E4_decline_drops_cause`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_acquire_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 10 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_lossy_landing_under_strict_policy_is_refused_at_the_item_with_the_codec_named`
  - `tests/test_acquire_workers.py::test_a_lossy_offer_under_strict_policy_is_refused_before_anything_is_fetched`
  - `tests/test_acquire_workers.py::test_a_track_the_provider_does_not_have_is_permanent_and_carries_no_remedy`
  - `tests/test_acquire_workers.py::test_a_track_the_provider_no_longer_has_is_declined_as_well`
  - `tests/test_acquire_workers.py::test_the_declined_warnings_name_skipped_tracks_and_never_a_failed_one`
  - `tests/test_acquire_workers.py::test_the_frozen_policy_reaches_the_worker_not_the_live_one`
  - `tests/test_acquire_workers.py::test_the_human_output_says_ok_and_names_the_refused_track`
  - `tests/test_acquire_workers.py::test_the_warning_is_the_same_when_the_finished_job_is_asked_about_again`
  - `tests/test_acquire_workers.py::test_three_landed_and_one_refused_by_policy_ends_ok_with_a_warning_naming_it`
  - `tests/test_jobs.py::test_a_declined_item_is_skipped_with_its_cause_and_the_job_succeeds`

Old text:

```
            (str(ItemState.SKIPPED), json.dumps(cause.to_json()), job_id, item_id),
```

New text:

```
            (str(ItemState.SKIPPED), None, job_id, item_id),
```

### `u169.E6_failed_cause_hides_declines`

partial failure cause: say nothing of the declined items beside the failures

- File: `src/cratekit/core/jobs_drive.py`
- Source: `u169.json`, row `E6_failed_cause_hides_declines`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_acquire_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_real_failure_beside_a_declined_item_still_fails_the_job_and_names_both`

Old text:

```
    if result.declined:
```

New text:

```
    if False:
```

### `u193.M14_park_job_id_dropped`

jobs._parked_cause: do not name the job, so the continue command cannot resume it

- File: `src/cratekit/core/jobs_drive.py`
- Source: `u193.json`, row `M14_park_job_id_dropped`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 509 against a baseline of 509
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_the_ceiling_parks_a_job_and_the_resumed_job_continues`

Old text:

```
    if "job_id" in (cause.detail or {}):
        return cause
```

New text:

```
    if True:
        return cause
```

### `u193.M15_park_job_id_overwrites`

jobs._parked_cause: overwrite a job id the cause already carries

- File: `src/cratekit/core/jobs_drive.py`
- Source: `u193.json`, row `M15_park_job_id_overwrites`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 509 against a baseline of 509
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_park_that_names_its_job_keeps_its_own_job_id`

Old text:

```
    if "job_id" in (cause.detail or {}):
        return cause
```

New text:

```
    if False:
        return cause
```

### `u227.R16_join_state`

join_run: write a job in any state, so a running or finished job is moved into a pass

- File: `src/cratekit/core/jobs.py`
- Source: `u227.json`, row `R16_join_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_mirror_downloads.py`, `tests/test_jobs.py`, `tests/test_export_set_rename.py`
- Collected: 129 against a baseline of 129
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
- Collected: 129 against a baseline of 129
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
- Collected: 129 against a baseline of 129
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

### `u235.S1_enqueue_ignores_a_given_job_id`

jobs.enqueue: a job id the caller names is ignored and a fresh identifier minted, a sample of the guard that hands new_run_id to every job

- File: `src/cratekit/core/jobs.py`
- Source: `u235.json`, row `S1_enqueue_ignores_a_given_job_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 83 against a baseline of 83
- Kills: 26 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_bad_stale_cancel_is_the_parsers_usage_error_and_cancels_nothing[job-id-beside-stale-days]`
  - `tests/test_jobs.py::test_a_bad_stale_cancel_is_the_parsers_usage_error_and_cancels_nothing[negative-days]`
  - `tests/test_jobs.py::test_a_bad_stale_cancel_is_the_parsers_usage_error_and_cancels_nothing[zero-days]`
  - `tests/test_jobs.py::test_a_blocked_job_or_another_librarys_is_left_by_the_stale_cancel`
  - `tests/test_jobs.py::test_a_cancelled_stale_job_reports_cancelled_and_resumes_by_its_own_command`
  - `tests/test_jobs.py::test_a_dry_run_lists_a_queued_job_a_live_driver_holds_as_left`
  - `tests/test_jobs.py::test_a_dry_run_lists_three_stale_jobs_and_names_the_keeper_of_the_identical_two`
  - `tests/test_jobs.py::test_a_dry_run_of_one_job_cancels_nothing`
  - `tests/test_jobs.py::test_a_job_whose_queued_time_cannot_be_read_is_never_stale`
  - `tests/test_jobs.py::test_a_running_job_is_never_listed_for_cancel_however_old`
  - `tests/test_jobs.py::test_a_stale_cancel_says_what_it_frees[another-open-job-holds-it]`
  - `tests/test_jobs.py::test_a_stale_cancel_says_what_it_frees[unparseable-url]`
  - `tests/test_jobs.py::test_a_stale_cancel_says_what_it_frees[url-typed-by-hand-holds-the-swept-id]`
  - `tests/test_jobs.py::test_a_stale_set_or_hearts_job_names_no_playlist_and_says_what_it_frees[hearts-job]`
  - `tests/test_jobs.py::test_a_stale_set_or_hearts_job_names_no_playlist_and_says_what_it_frees[set-job]`
  - ... and 11 more, see the JSON sidecar

Old text:

```
    identifier = job_id or new_run_id()
```

New text:

```
    identifier = new_run_id()
```

### `u270.J1_claim_batch_size_floor`

claim_batch: accept a batch of zero items, so a size the binding never checks claims nothing and the job reads as finished

- File: `src/cratekit/core/jobs.py`
- Source: `u270.json`, row `J1_claim_batch_size_floor`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_jobs_batch.py`, `tests/test_jobs.py`, `tests/test_handlers.py`
- Collected: 135 against a baseline of 135
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

### `u270.J2_claim_batch_order`

claim_batch: claim the highest ordinals first, so a batch writes its tracks in the reverse of the crate's order

- File: `src/cratekit/core/jobs.py`
- Source: `u270.json`, row `J2_claim_batch_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs_batch.py`, `tests/test_outbound_export_batches.py`, `tests/test_outbound_workers.py`
- Collected: 167 against a baseline of 167
- Kills: 22 (killed)
- Killed:
  - `tests/test_jobs_batch.py::test_a_batch_answered_under_a_signal_is_released_whole_and_the_job_cancelled`
  - `tests/test_jobs_batch.py::test_a_batch_is_claimed_in_ordinal_order_up_to_its_size`
  - `tests/test_jobs_batch.py::test_a_park_raised_by_the_batch_releases_it_whole_and_blocks_the_job`
  - `tests/test_jobs_batch.py::test_a_parked_batch_is_driven_again_from_its_first_item`
  - `tests/test_jobs_batch.py::test_a_raise_out_of_the_batch_handler_is_every_items_outcome`
  - `tests/test_jobs_batch.py::test_a_signal_after_one_batch_keeps_it_done_and_claims_no_other`
  - `tests/test_jobs_batch.py::test_claim_batch_takes_only_pending_items_and_none_when_nothing_is_left`
  - `tests/test_jobs_batch.py::test_every_item_of_a_batch_is_held_claimed_while_its_handler_runs`
  - `tests/test_outbound_export_batches.py::test_a_created_playlist_is_said_once_for_the_batch`
  - `tests/test_outbound_export_batches.py::test_a_job_of_two_hundred_and_fifty_tracks_makes_fifteen_requests`
  - `tests/test_outbound_export_batches.py::test_a_park_between_the_request_and_the_record_blocks_and_the_resume_adds_nothing_twice`
  - `tests/test_outbound_export_batches.py::test_one_refused_read_after_a_landed_add_through_the_driver_finishes_the_job`
  - `tests/test_outbound_workers.py::test_a_crate_dragged_into_a_folder_updates_its_remote_playlist`
  - `tests/test_outbound_workers.py::test_a_failed_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/test_outbound_workers.py::test_a_filing_failure_is_a_warning_on_a_finished_export`
  - ... and 7 more, see the JSON sidecar

Old text:

```
            "ORDER BY ordinal LIMIT ?",
```

New text:

```
            "ORDER BY ordinal DESC LIMIT ?",
```

### `u270.J3_park_releases_the_batch`

drive: ignore a Parked among a batch's outcomes, so the batch is settled as failed and the next batch is the second request into a block

- File: `src/cratekit/core/jobs_drive.py`
- Source: `u270.json`, row `J3_park_releases_the_batch`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs_batch.py`, `tests/test_outbound_export_batches.py`, `tests/test_outbound_workers.py`
- Collected: 167 against a baseline of 167
- Kills: 4 (killed)
- Killed:
  - `tests/test_jobs_batch.py::test_a_park_answered_for_one_item_releases_the_whole_batch`
  - `tests/test_jobs_batch.py::test_a_park_raised_by_the_batch_releases_it_whole_and_blocks_the_job`
  - `tests/test_jobs_batch.py::test_a_parked_batch_is_driven_again_from_its_first_item`
  - `tests/test_outbound_export_batches.py::test_a_park_between_the_request_and_the_record_blocks_and_the_resume_adds_nothing_twice`

Old text:

```
                if parked is not None:
                    release_claims(store, job_id, driver=driver)
```

New text:

```
                if False:
                    release_claims(store, job_id, driver=driver)
```

### `u270.J4_signal_releases_the_batch`

drive: commit a batch answered under a signal, so a stop part way settles what the handler cut short

- File: `src/cratekit/core/jobs_drive.py`
- Source: `u270.json`, row `J4_signal_releases_the_batch`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs_batch.py`, `tests/test_outbound_export_batches.py`, `tests/test_outbound_workers.py`
- Collected: 167 against a baseline of 167
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs_batch.py::test_a_batch_answered_under_a_signal_is_released_whole_and_the_job_cancelled`

Old text:

```
                    return result
                if interrupt.signalled:
                    release_claims(store, job_id, driver=driver)
                    result.interrupted = True
                    break
                for item in claimed:
```

New text:

```
                    return result
                for item in claimed:
```

### `u270.J5_declined_outcome`

drive: settle a declined outcome as failed, so a batch item the worker declined fails the job

- File: `src/cratekit/core/jobs_drive.py`
- Source: `u270.json`, row `J5_declined_outcome`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs_batch.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs_batch.py::test_each_outcome_settles_its_own_item`

Old text:

```
                    if isinstance(outcome, Declined):
```

New text:

```
                    if False:
```

### `u270.J6_missing_outcome_fails`

_batch_outcomes: read an item the handler gave no outcome for as done

- File: `src/cratekit/core/jobs_drive.py`
- Source: `u270.json`, row `J6_missing_outcome_fails`
- Moved: _batch_outcomes moved whole from core/jobs.py to core/jobs_drive.py with the drive loop (U301); the test that killed it, test_an_item_the_handler_answered_nothing_for_is_failed_not_done, is now the no-answer case of test_an_item_without_a_usable_outcome_is_failed_not_done in the same file, the same input and the same check
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs_batch.py`, `tests/test_outbound_workers.py`
- Collected: 145 against a baseline of 145
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs_batch.py::test_an_item_without_a_usable_outcome_is_failed_not_done[no-answer]`

Old text:

```
            outcomes[item.item_id] = _no_outcome(item)
```

New text:

```
            outcomes[item.item_id] = None
```

### `u270.J7_raise_is_every_outcome`

_batch_outcomes: a raise out of the batch handler fails only the first item, and the rest have no outcome

- File: `src/cratekit/core/jobs_drive.py`
- Source: `u270.json`, row `J7_raise_is_every_outcome`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs_batch.py`, `tests/test_outbound_workers.py`, `tests/test_outbound_export_batches.py`
- Collected: 167 against a baseline of 167
- Kills: 3 (killed)
- Killed:
  - `tests/test_jobs_batch.py::test_a_batch_that_fails_every_item_records_the_job_failed_then_raises`
  - `tests/test_jobs_batch.py::test_a_raise_out_of_the_batch_handler_is_every_items_outcome`
  - `tests/test_outbound_workers.py::test_a_job_driven_with_no_adapter_fails_rather_than_reporting_success`

Old text:

```
        return {item.item_id: exc for item in claimed}
```

New text:

```
        return {claimed[0].item_id: exc}
```

### `u270.J8_stop_is_the_signal`

drive: hand the batch handler a stop that never answers true, so a signal waits for a whole batch's matching

- File: `src/cratekit/core/jobs_drive.py`
- Source: `u270.json`, row `J8_stop_is_the_signal`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
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

### `u270.J9_outcome_type_check`

_batch_outcomes: pass an outcome that is neither produced nor an exception through to the commit

- File: `src/cratekit/core/jobs_drive.py`
- Source: `u270.json`, row `J9_outcome_type_check`
- Moved: _batch_outcomes moved whole from core/jobs.py to core/jobs_drive.py with the drive loop (U301); the test that killed it, test_an_outcome_that_is_neither_produced_nor_an_exception_fails_its_item, is now the neither-produced-nor-an-exception case of test_an_item_without_a_usable_outcome_is_failed_not_done in the same file, now also asserting the message
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_jobs_batch.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs_batch.py::test_an_item_without_a_usable_outcome_is_failed_not_done[neither-produced-nor-an-exception]`

Old text:

```
        if outcome is not None and not isinstance(outcome, (Produced, Exception)):
```

New text:

```
        if False:
```

### `u298.H16_reported_extra_under_progress`

reported: a verb's own detail is dropped from progress

- File: `src/cratekit/core/jobs.py`
- Source: `u298.json`, row `H16_reported_extra_under_progress`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_set_progress.py`, `tests/intake/test_workers.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_ahead.py`, `tests/test_analysis_workers.py`, `tests/test_genre_favorites_adoption.py`, `tests/test_intake_missing.py`, `tests/test_label_genre.py`, `tests/test_label_judge.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_refused.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_vocals_cli.py`
- Collected: 1525 against a baseline of 1525
- Kills: 129 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_mix_url_runs_the_ordinary_set_pipeline_over_the_fetched_file`
  - `tests/intake/test_set_progress.py::test_json_output_carries_no_progress_and_stays_one_document`
  - `tests/intake/test_workers.py::test_a_playlist_job_runs_pending_to_done_through_the_resume_path`
  - `tests/intake/test_workers.py::test_a_resolution_with_nothing_missing_names_no_next_command`
  - `tests/intake/test_workers.py::test_a_resumed_set_writes_no_tracklist`
  - `tests/intake/test_workers.py::test_a_set_identified_over_incomplete_coverage_queues_with_a_warning_and_freezes_the_gap`
  - `tests/intake/test_workers.py::test_a_set_job_runs_pending_to_done_and_reports_owned_offered_and_missing`
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`
  - `tests/intake/test_workers.py::test_a_set_that_fits_one_run_carries_no_parts_note`
  - `tests/intake/test_workers.py::test_a_set_whose_tracklist_cannot_be_written_is_queued_and_says_where_to_read_it`
  - `tests/intake/test_workers.py::test_a_set_writes_its_tracklist_where_out_says`
  - `tests/intake/test_workers.py::test_a_set_writes_the_tracklist_identify_writes_for_the_same_rows`
  - `tests/intake/test_workers.py::test_a_stray_file_beside_the_reports_does_not_take_the_summary_down`
  - `tests/intake/test_workers.py::test_each_resolution_count_is_followed_by_its_reasons`
  - `tests/intake/test_workers.py::test_favorites_resolves_each_heart_owned_offered_or_missing`
  - ... and 114 more, see the JSON sidecar

Old text:

```
    if extra:
        counted.update(extra)
```

New text:

```
(empty)
```

### `u298.H17_reported_cause`

reported: a job closed on a cause reports no cause

- File: `src/cratekit/core/jobs.py`
- Source: `u298.json`, row `H17_reported_cause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_job_carrying_a_cause_reports_it_as_the_declared_object`

Old text:

```
        "cause": job.cause.to_json() if job.cause is not None else None,
        "progress": counted,
```

New text:

```
        "cause": None,
        "progress": counted,
```

### `u298.H18_staged_path_cleared`

Artifacts.staged_path: a half written report from an attempt that died is left in staging

- File: `src/cratekit/core/jobs.py`
- Source: `u298.json`, row `H18_staged_path_cleared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`, `tests/test_jobs.py`
- Collected: 183 against a baseline of 183
- Kills: 1 (killed)
- Killed:
  - `tests/test_shared_homes.py::test_a_staging_directory_is_cleared_of_the_attempt_before_it`

Old text:

```
        directory = self.staging_dir(cfg, job_id) / str(ordinal)
        if directory.exists():
            shutil.rmtree(directory)
```

New text:

```
        directory = self.staging_dir(cfg, job_id) / str(ordinal)
```

### `u298.H19_by_ordinal_numeric`

by_ordinal: reports sorted as text, so the ten thousandth comes before the second

- File: `src/cratekit/core/jobs.py`
- Source: `u298.json`, row `H19_by_ordinal_numeric`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`, `tests/test_jobs.py`
- Collected: 183 against a baseline of 183
- Kills: 1 (killed)
- Killed:
  - `tests/test_shared_homes.py::test_committed_reports_are_read_back_in_item_order_as_numbers`

Old text:

```
    return sorted((path for path in paths if path.stem.isdigit()), key=lambda item: int(item.stem))
```

New text:

```
    return sorted((path for path in paths if path.stem.isdigit()), key=lambda item: item.stem)
```

### `u298.H20_by_ordinal_filters`

by_ordinal: a stray non ordinal file reaches the sort key and raises

- File: `src/cratekit/core/jobs.py`
- Source: `u298.json`, row `H20_by_ordinal_filters`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`, `tests/test_jobs.py`
- Collected: 183 against a baseline of 183
- Kills: 1 (killed)
- Killed:
  - `tests/test_shared_homes.py::test_a_file_that_is_named_for_no_ordinal_is_no_report`

Old text:

```
    return sorted((path for path in paths if path.stem.isdigit()), key=lambda item: int(item.stem))
```

New text:

```
    return sorted((path for path in paths), key=lambda item: int(item.stem))
```

### `u298.H21_advance_refuses_empty`

advance: a job with no items is driven straight to succeeded

- File: `src/cratekit/core/jobs.py`
- Source: `u298.json`, row `H21_advance_refuses_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`, `tests/test_tag_workers.py`
- Collected: 156 against a baseline of 156
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_job_queued_with_no_items_refuses_rather_than_reporting_success`
  - `tests/test_adopt_workers.py::test_an_apply_job_queued_with_no_items_refuses_rather_than_driving`
  - `tests/test_tag_workers.py::test_a_job_with_no_items_is_refused_rather_than_driven`

Old text:

```
    if job.is_open() and not items(store, job.job_id):
```

New text:

```
    if False:
```

### `u298.H22_resumed_raises_state`

resumed: a job that did not end cleanly is an ok exit

- File: `src/cratekit/core/jobs.py`
- Source: `u298.json`, row `H22_resumed_raises_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`, `tests/test_jobs.py`
- Collected: 183 against a baseline of 183
- Kills: 2 (killed)
- Killed:
  - `tests/test_shared_homes.py::test_a_job_already_closed_is_judged_without_being_driven`
  - `tests/test_shared_homes.py::test_a_job_still_open_is_driven_once_and_read_again_before_it_is_judged`

Old text:

```
        job = get(store, job.job_id)
    raise_for_state(job)
    return job, warnings
```

New text:

```
        job = get(store, job.job_id)
    return job, warnings
```

### `u298.H23_artifacts_names_differ`

Artifacts: a staging name equal to the final name is accepted

- File: `src/cratekit/core/jobs.py`
- Source: `u298.json`, row `H23_artifacts_names_differ`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`
- Collected: 100 against a baseline of 100
- Kills: 1 (killed)
- Killed:
  - `tests/test_shared_homes.py::test_a_report_location_is_two_different_directory_names[same-same]`

Old text:

```
        if self.final == self.staging:
```

New text:

```
        if False:
```

### `u12-independent-round-6.C2_reserve_halved`

Halve the absolute memory reserve coefficient, two gibibytes to one. A reserve that can be halved with a green suite is a reserve nothing pins.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `C2_reserve_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 2 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_capped_service_on_a_huge_host_is_sized_by_the_service`
  - `tests/test_pool_sizing.py::test_the_absolute_reserve_is_two_gibibytes_of_the_reading_that_was_never_ours`

Old text:

```
DEFAULT_MEMORY_RESERVE_BYTES = 2 * 1024**3
```

New text:

```
DEFAULT_MEMORY_RESERVE_BYTES = 1 * 1024**3
```

### `u12-independent-round-6.C4_darwin_headroom`

Raise the darwin headroom share from half to three quarters, which is the value the measured inactive-queue split says is too optimistic.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `C4_darwin_headroom`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 4 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_the_darwin_headroom_claims_half_because_half_is_what_was_measured`
  - `tests/test_pool_sizing.py::test_the_headroom_share_is_lower_where_the_reading_is_measurably_worse[darwin-50]`
  - `tests/test_pool_sizing.py::test_the_headroom_share_is_lower_where_the_reading_is_measurably_worse[linux-75]`
  - `tests/test_pool_sizing.py::test_the_headroom_share_is_lower_where_the_reading_is_measurably_worse[win32-75]`

Old text:

```
DARWIN_HEADROOM_PERCENT = 50
```

New text:

```
DARWIN_HEADROOM_PERCENT = 75
```

### `u12-independent-round-6.C5_swap_threshold`

Raise the swap pressure threshold from one gibibyte to four, so the machine the documented kill happened on is no longer refused a pool.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `C5_swap_threshold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 4 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_gated_plan_still_reports_the_reading_it_was_gated_despite`
  - `tests/test_pool_sizing.py::test_the_machine_the_kill_happened_on_gets_no_pool_under_the_shipped_rule`
  - `tests/test_pool_sizing.py::test_the_pressure_gate_bites_at_its_two_lines_and_nowhere_else[swap-at-the-line]`
  - `tests/test_pool_sizing.py::test_the_swap_threshold_is_a_gibibyte_and_the_gibibyte_is_load_bearing[a-full-gibibyte]`

Old text:

```
DEFAULT_SWAP_PRESSURE_BYTES = 1 * 1024**3
```

New text:

```
DEFAULT_SWAP_PRESSURE_BYTES = 4 * 1024**3
```

### `u12-independent-round-6.C6_used_percent_ceiling`

Raise the used-percent ceiling from eighty five to ninety five.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `C6_used_percent_ceiling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 2 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_the_pressure_gate_bites_at_its_two_lines_and_nowhere_else[percent-at-the-line]`
  - `tests/test_pool_sizing.py::test_the_used_percent_ceiling_is_eighty_five_and_the_number_is_load_bearing[at-the-line]`

Old text:

```
DEFAULT_USED_PERCENT_CEILING = 85
```

New text:

```
DEFAULT_USED_PERCENT_CEILING = 95
```

### `u12-independent-round-6.C7_max_tasks_per_child`

Two and a half times the recycle budget, one hundred to two hundred fifty, so a child holds an allocator two and a half times longer before retiring.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `C7_max_tasks_per_child`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 3 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_recycling_is_on_by_default_for_any_pool_wider_than_one`
  - `tests/test_pool_sizing.py::test_the_recycle_budget_retires_a_child_occasionally_rather_than_constantly[a-ten-thousand-track-folder]`
  - `tests/test_pool_sizing.py::test_the_recycle_budget_retires_a_child_occasionally_rather_than_constantly[an-ordinary-folder]`

Old text:

```
DEFAULT_MAX_TASKS_PER_CHILD = 100
```

New text:

```
DEFAULT_MAX_TASKS_PER_CHILD = 250
```

### `u12-independent-round-6.C8_probe_deadline`

Cut the probe deadline from two minutes to forty five seconds, below the twice-the-reference floor the docstring claims the suite states.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `C8_probe_deadline`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_the_probe_deadline_the_module_ships_outlasts_the_load_it_waits_for`

Old text:

```
DEFAULT_PROBE_TIMEOUT_SECONDS = 120.0
```

New text:

```
DEFAULT_PROBE_TIMEOUT_SECONDS = 45.0
```

### `u12-independent-round-6.C9_reap_budget`

Halve the reaping budget, one second to half a second, which the round six docstring names as the value that makes the terminate rung a race.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `C9_reap_budget`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_the_reaping_budget_is_a_band_around_what_a_release_costs`

Old text:

```
_PROBE_REAP_SECONDS = 1.0
```

New text:

```
_PROBE_REAP_SECONDS = 0.5
```

### `u12-independent-round-6.G1_dotdot_not_refused`

Drop the refusal of a cgroup path containing dot dot, so a climbing path is rewritten into a real sibling cgroup and its tighter cap binds.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `G1_dotdot_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_climb_that_lands_on_a_real_cgroup_inside_the_mount_is_refused_too[a-climb-in-the-middle]`

Old text:

```
    if ".." in fields:
        candidates = [mount]
    else:

```

New text:

```
    if False:
        candidates = [mount]
    else:

```

### `u12-independent-round-6.G2_containment_dropped`

Stop checking that a resolved level is still inside the mount, so a symlink out of the mount is read as a level of this process's cgroup.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `G2_containment_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 2 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_component_that_symlinks_out_of_the_mount_is_not_read`
  - `tests/test_pool_sizing.py::test_a_limit_file_that_symlinks_out_of_the_mount_is_not_read`

Old text:

```
    if resolved is None or not resolved.is_relative_to(anchor):
        return None

```

New text:

```
    if resolved is None:
        return None

```

### `u12-independent-round-6.G3_headroom_can_go_negative`

Report a negative headroom for a cgroup already over its cap.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `G3_headroom_can_go_negative`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_cgroup_already_over_its_cap_has_no_headroom_rather_than_negative`

Old text:

```
    return max(0, limit - used)

```

New text:

```
    return limit - used

```

### `u12-independent-round-6.G4_controller_substring_match`

Match the memory controller by substring, so a controller named memoryfoo sends the walk to an unrelated cgroup.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `G4_controller_substring_match`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 2 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_controller_field_that_merely_contains_the_word_memory_is_not_it[a-name-that-contains-it]`
  - `tests/test_pool_sizing.py::test_a_controller_field_that_merely_contains_the_word_memory_is_not_it[a-name-that-starts-with-it]`

Old text:

```
        elif "memory" in controllers.split(","):

```

New text:

```
        elif "memory" in controllers:

```

### `u12-independent-round-6.G5_loosest_cap_wins`

Take the loosest cap on the chain rather than the tightest, so a generous unit inside a tight slice reports the unit's number.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `G5_loosest_cap_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_the_tightest_cap_on_the_chain_is_the_one_that_binds`

Old text:

```
    return min(found) if found else None

```

New text:

```
    return max(found) if found else None

```

### `u12-independent-round-6.G6_cgroup_cap_ignored`

Ignore the cgroup cap entirely and return the host reading, which is the defect that sizes a container by its host.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `G6_cgroup_cap_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 3 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_capped_service_on_a_huge_host_is_sized_by_the_service`
  - `tests/test_pool_sizing.py::test_a_container_capped_below_its_host_is_sized_by_the_cap`
  - `tests/test_pool_sizing.py::test_a_large_container_on_a_larger_host_is_still_sized_by_the_container`

Old text:

```
    return reading if capped is None else min(reading, capped)

```

New text:

```
    return reading

```

### `u12-independent-round-6.G7_valueerror_escapes_the_reader`

Narrow the kernel-file reader back to OSError, so undecodable bytes and an embedded null byte raise out of a function that promises a number.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `G7_valueerror_escapes_the_reader`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_kernel_file_that_is_not_readable_as_text_is_an_absent_reading[not-text-at-all]`

Old text:

```
    except (OSError, ValueError):
        return None

```

New text:

```
    except OSError:
        return None

```

### `u12-independent-round-6.M1_measurement_below_the_floor`

Return the measurement even when it is below the declared floor, so the floor becomes a fallback rather than a floor.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `M1_measurement_below_the_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_the_probe_never_reports_below_the_declared_floor`

Old text:

```
    return max(measured, floor_bytes)

```

New text:

```
    return measured

```

### `u12-independent-round-6.M2_nonsense_measurement_accepted`

Accept a boolean, a float or a zero from the probe as a byte count.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `M2_nonsense_measurement_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 2 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_probe_that_answers_with_nonsense_returns_the_floor[none]`
  - `tests/test_pool_sizing.py::test_a_probe_that_answers_with_nonsense_returns_the_floor[text]`

Old text:

```
    if not isinstance(measured, int) or isinstance(measured, bool) or measured < 1:
        return floor_bytes

```

New text:

```
(empty)
```

### `u12-independent-round-6.M3_zero_deadline_allowed`

Allow a probe deadline of zero or less, which is a probe that can never answer reporting the floor as though it had measured.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `M3_zero_deadline_allowed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_probe_with_no_time_to_answer_refuses_rather_than_reporting_the_floor`

Old text:

```
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must leave the probe some time to answer")

```

New text:

```
(empty)
```

### `u12-independent-round-6.M4_model_freed_before_the_reading`

Free the loaded object before the resident set is read, the allocator retention defect the probe was rewritten to fix.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `M4_model_freed_before_the_reading`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_the_real_probe_measures_a_freshly_spawned_child`

Old text:

```
        model = loader()
        try:
            measured = resident_bytes()
        finally:

```

New text:

```
        loader()
        try:
            measured = resident_bytes()
        finally:

```

### `u12-independent-round-6.M5_terminate_rung_removed`

Remove the terminate rung alone, so every abandoned probe child meets an unconditional kill with no chance to unwind.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `M5_terminate_rung_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 3 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_probe_child_that_can_unwind_is_asked_to_before_it_is_killed`
  - `tests/test_pool_sizing.py::test_a_probe_child_that_refuses_to_unwind_meets_the_kill_backstop`
  - `tests/test_pool_sizing.py::test_the_release_the_fixture_declares_is_what_the_ladder_was_timed_paying`

Old text:

```
    if worker.is_alive():
        worker.terminate()
        worker.join(_PROBE_REAP_SECONDS)

```

New text:

```
(empty)
```

### `u12-independent-round-6.M6_kill_rung_removed`

Remove the kill backstop alone, so a child that ignores its terminate is left running and still allocating.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `M6_kill_rung_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_probe_child_that_refuses_to_unwind_meets_the_kill_backstop`

Old text:

```
    if worker.is_alive():
        worker.kill()
        worker.join(_PROBE_REAP_SECONDS)

```

New text:

```
(empty)
```

### `u12-independent-round-6.M7_parent_keeps_the_write_end`

Leave the parent's copy of the pipe write end open, so a child that dies without answering is indistinguishable from a slow one.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `M7_parent_keeps_the_write_end`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_probe_child_that_dies_without_answering_gives_up_at_once`

Old text:

```
    # exactly like a slow one until the timeout expired.
    writer.close()

```

New text:

```
    # exactly like a slow one until the timeout expired.

```

### `u12-independent-round-6.M8_no_reap_after_the_probe`

Remove the reap from the probe's finally, so an abandoned child keeps its allocation on a machine already declared tight.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `M8_no_reap_after_the_probe`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_probe_that_gave_up_leaves_no_child_still_allocating`

Old text:

```
        reader.close()
        _reap(worker)

```

New text:

```
        reader.close()

```

### `u12-independent-round-6.P10_recycle_reported_for_in_process`

Report a recycle count on a plan that runs in the calling process and has no child to retire.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `P10_recycle_reported_for_in_process`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 2 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_an_in_process_plan_runs_no_generations_at_all`
  - `tests/test_pool_sizing.py::test_two_gigabytes_against_a_one_gigabyte_worker_runs_in_process`

Old text:

```
        max_tasks_per_child=None if workers == 1 else max_tasks_per_child,

```

New text:

```
        max_tasks_per_child=max_tasks_per_child,

```

### `u12-independent-round-6.P12_unreadable_falls_back_to_ceiling`

Make the unreadable-memory fallback the declared ceiling rather than one worker, which is the exact fallback the brief forbids.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `P12_unreadable_falls_back_to_ceiling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 8 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_memory_read_failure_falls_back_to_one_worker_rather_than_raising`
  - `tests/test_pool_sizing.py::test_a_reading_that_is_not_a_byte_count_is_treated_as_unreadable[bool]`
  - `tests/test_pool_sizing.py::test_a_reading_that_is_not_a_byte_count_is_treated_as_unreadable[float]`
  - `tests/test_pool_sizing.py::test_a_reading_that_is_not_a_byte_count_is_treated_as_unreadable[negative]`
  - `tests/test_pool_sizing.py::test_a_reading_that_is_not_a_byte_count_is_treated_as_unreadable[none]`
  - `tests/test_pool_sizing.py::test_a_reading_that_is_not_a_byte_count_is_treated_as_unreadable[text]`
  - `tests/test_pool_sizing.py::test_a_reading_that_is_not_a_byte_count_is_treated_as_unreadable[very-negative]`
  - `tests/test_pool_sizing.py::test_the_fallback_is_never_the_ceiling_or_the_item_count`

Old text:

```
        return PoolPlan(
            workers=1,
            items=items,
            bound=Bound.MEMORY_UNREADABLE,

```

New text:

```
        return PoolPlan(
            workers=ceiling,
            items=items,
            bound=Bound.MEMORY_UNREADABLE,

```

### `u12-independent-round-6.P1_reserve_not_applied`

Drop the absolute reserve from the budget entirely, so the whole reading is claimable before the percent scales it.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `P1_reserve_not_applied`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 14 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_capped_service_on_a_huge_host_is_sized_by_the_service`
  - `tests/test_pool_sizing.py::test_a_machine_that_affords_exactly_one_worker_says_so`
  - `tests/test_pool_sizing.py::test_a_machine_that_affords_none_is_not_the_same_machine_and_does_not_say_it_is`
  - `tests/test_pool_sizing.py::test_a_measured_worker_size_flows_into_the_plan_it_was_taken_for`
  - `tests/test_pool_sizing.py::test_a_platform_with_no_limit_contributes_nothing_to_the_arithmetic`
  - `tests/test_pool_sizing.py::test_sixteen_gigabytes_is_bound_by_the_headroom_once_the_ceiling_is_raised`
  - `tests/test_pool_sizing.py::test_the_absolute_reserve_is_two_gibibytes_of_the_reading_that_was_never_ours`
  - `tests/test_pool_sizing.py::test_the_core_count_does_not_change_the_computed_cap`
  - `tests/test_pool_sizing.py::test_the_hard_ceiling_and_the_headroom_agree_at_the_point_they_cross`
  - `tests/test_pool_sizing.py::test_the_reserve_comes_off_the_reading_before_the_percent_scales_it`
  - `tests/test_pool_sizing.py::test_the_worker_count_flips_exactly_at_the_affordable_boundary[2]`
  - `tests/test_pool_sizing.py::test_the_worker_count_flips_exactly_at_the_affordable_boundary[3]`
  - `tests/test_pool_sizing.py::test_the_worker_count_flips_exactly_at_the_affordable_boundary[4]`
  - `tests/test_pool_sizing.py::test_two_gigabytes_against_a_one_gigabyte_worker_runs_in_process`

Old text:

```
    budget = max(0, available - reserve_bytes)

```

New text:

```
    budget = max(0, available)

```

### `u12-independent-round-6.P2_order_reversed`

Reverse the last two steps: divide into workers first and then scale the count, which the docstring says differs only at the boundaries.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `P2_order_reversed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 6 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_machine_that_affords_exactly_one_worker_says_so`
  - `tests/test_pool_sizing.py::test_a_machine_that_affords_none_is_not_the_same_machine_and_does_not_say_it_is`
  - `tests/test_pool_sizing.py::test_the_hard_ceiling_and_the_headroom_agree_at_the_point_they_cross`
  - `tests/test_pool_sizing.py::test_the_headroom_is_applied_to_the_bytes_before_they_are_divided_into_workers`
  - `tests/test_pool_sizing.py::test_the_worker_count_flips_exactly_at_the_affordable_boundary[2]`
  - `tests/test_pool_sizing.py::test_the_worker_count_flips_exactly_at_the_affordable_boundary[4]`

Old text:

```
    affordable = budget * headroom_percent // 100 // worker_bytes

```

New text:

```
    affordable = budget // worker_bytes * headroom_percent // 100

```

### `u12-independent-round-6.P3_budget_can_go_negative`

Remove the floor at zero so a reading smaller than the reserve produces a negative budget and a negative affordable count.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `P3_budget_can_go_negative`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 2 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_container_capped_below_its_host_is_sized_by_the_cap`
  - `tests/test_pool_sizing.py::test_a_reading_smaller_than_the_reserve_affords_nothing_rather_than_going_negative`

Old text:

```
    budget = max(0, available - reserve_bytes)

```

New text:

```
    budget = available - reserve_bytes

```

### `u12-independent-round-6.P4_no_floor_of_one_worker`

Remove the floor of one worker, so a machine that affords none plans a pool of zero.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `P4_no_floor_of_one_worker`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 11 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_container_capped_below_its_host_is_sized_by_the_cap`
  - `tests/test_pool_sizing.py::test_a_function_no_child_could_receive_is_refused_before_anything_runs`
  - `tests/test_pool_sizing.py::test_a_machine_that_affords_none_is_not_the_same_machine_and_does_not_say_it_is`
  - `tests/test_pool_sizing.py::test_a_plan_of_one_worker_explains_itself_as_in_process`
  - `tests/test_pool_sizing.py::test_a_plan_of_one_worker_runs_the_work_in_this_process`
  - `tests/test_pool_sizing.py::test_a_reading_smaller_than_the_reserve_affords_nothing_rather_than_going_negative`
  - `tests/test_pool_sizing.py::test_an_in_process_plan_refuses_to_hand_back_pool_arguments`
  - `tests/test_pool_sizing.py::test_an_in_process_plan_runs_no_generations_at_all`
  - `tests/test_pool_sizing.py::test_an_initializer_argument_no_child_could_receive_is_refused_on_the_same_terms`
  - `tests/test_pool_sizing.py::test_no_work_at_all_plans_one_in_process_worker_rather_than_zero`
  - `tests/test_pool_sizing.py::test_two_gigabytes_against_a_one_gigabyte_worker_runs_in_process`

Old text:

```
    workers = max(1, smallest)

```

New text:

```
    workers = smallest

```

### `u12-independent-round-6.P5_tie_goes_to_the_ceiling`

Put the ceiling ahead of available memory in the precedence list, so a tie is reported as the ceiling rather than as memory.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `P5_tie_goes_to_the_ceiling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_the_hard_ceiling_and_the_headroom_agree_at_the_point_they_cross`

Old text:

```
        (Bound.AVAILABLE_MEMORY, affordable),
        (Bound.CEILING, ceiling),

```

New text:

```
        (Bound.CEILING, ceiling),
        (Bound.AVAILABLE_MEMORY, affordable),

```

### `u12-independent-round-6.P6_no_insufficient_memory_bound`

Remove the reclassification that tells a machine affording exactly one from a machine affording none.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `P6_no_insufficient_memory_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 5 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_container_capped_below_its_host_is_sized_by_the_cap`
  - `tests/test_pool_sizing.py::test_a_machine_that_affords_none_is_not_the_same_machine_and_does_not_say_it_is`
  - `tests/test_pool_sizing.py::test_a_reading_smaller_than_the_reserve_affords_nothing_rather_than_going_negative`
  - `tests/test_pool_sizing.py::test_the_absolute_reserve_is_two_gibibytes_of_the_reading_that_was_never_ours`
  - `tests/test_pool_sizing.py::test_two_gigabytes_against_a_one_gigabyte_worker_runs_in_process`

Old text:

```
        bound = Bound.INSUFFICIENT_MEMORY

```

New text:

```
        bound = Bound.AVAILABLE_MEMORY

```

### `u12-independent-round-6.R1_available_type_check`

Accept a non-integer or negative available reading as a real reading.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `R1_available_type_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 5 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_reading_that_is_not_a_byte_count_is_treated_as_unreadable[bool]`
  - `tests/test_pool_sizing.py::test_a_reading_that_is_not_a_byte_count_is_treated_as_unreadable[float]`
  - `tests/test_pool_sizing.py::test_a_reading_that_is_not_a_byte_count_is_treated_as_unreadable[negative]`
  - `tests/test_pool_sizing.py::test_a_reading_that_is_not_a_byte_count_is_treated_as_unreadable[text]`
  - `tests/test_pool_sizing.py::test_a_reading_that_is_not_a_byte_count_is_treated_as_unreadable[very-negative]`

Old text:

```
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        return None
    return value

```

New text:

```
    return value

```

### `u12-independent-round-6.R2_available_never_raises`

Remove the catch around the injected available reader, so a reader that raises raises out of plan_pool.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `R2_available_never_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 2 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_memory_read_failure_falls_back_to_one_worker_rather_than_raising`
  - `tests/test_pool_sizing.py::test_the_fallback_is_never_the_ceiling_or_the_item_count`

Old text:

```
    try:
        value = reader()
    except Exception:
        return None
    if not isinstance(value, int)
```

New text:

```
    value = reader()
    if not isinstance(value, int)
```

### `u12-independent-round-6.R3_pressure_percent_range`

Accept a used-percent outside zero to one hundred as a real reading.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `R3_pressure_percent_range`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_an_unreadable_pressure_reading_does_not_collapse_the_pool[impossible-percent]`

Old text:

```
    if not 0 <= used <= 100:
        return None
    return value

```

New text:

```
    return value

```

### `u12-independent-round-6.R4_pressure_type_check`

Accept anything at all as a pressure reading, not only a Pressure.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `R4_pressure_type_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 2 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_an_unreadable_pressure_reading_does_not_collapse_the_pool[none]`
  - `tests/test_pool_sizing.py::test_an_unreadable_pressure_reading_does_not_collapse_the_pool[text]`

Old text:

```
    if not isinstance(value, Pressure):
        return None

```

New text:

```
(empty)
```

### `u12-independent-round-6.X1_pool_of_one_built`

Let executor_arguments build a pool for a plan of one worker instead of refusing at the seam.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `X1_pool_of_one_built`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_an_in_process_plan_refuses_to_hand_back_pool_arguments`

Old text:

```
    if plan.in_process:
        raise ValueError(
            "a plan of one worker runs in the calling process; there is no pool "
            "to build. Branch on plan.in_process before asking for a pool."
        )

```

New text:

```
(empty)
```

### `u12-independent-round-6.X3_generation_boundary_removed`

Give one executor all of the work rather than one generation of it, which is the deadlock the generation boundary exists to prevent.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `X3_generation_boundary_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_no_child_survives_a_generation_boundary_and_every_one_reloads_its_model`

Old text:

```
    generation = plan.tasks_per_generation or len(ordered) or 1

```

New text:

```
    generation = len(ordered) or 1

```

### `u12-independent-round-6.X4_initargs_not_refused`

Stop holding initializer arguments to the picklability rule, so the same call means two things on two machines again.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `X4_initargs_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_an_initializer_argument_no_child_could_receive_is_refused_on_the_same_terms`

Old text:

```
    for position, argument in enumerate(initargs):
        _refuse_what_no_child_could_receive(argument, f"initializer argument {position}")

```

New text:

```
(empty)
```

### `u12-independent-round-6.X5_in_process_path_removed`

Build a pool even for a plan of one worker, which is the brief's third requirement inverted.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `X5_in_process_path_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_plan_of_one_worker_runs_the_work_in_this_process`

Old text:

```
    if plan.in_process:
        if initializer is not None:
            initializer(*initargs)
        return [function(item) for item in ordered]

```

New text:

```
(empty)
```

### `u12-independent-round-6.X7_generation_size_drops_the_width`

Size a generation by one child's budget rather than by the whole set of children, so the executor is rebuilt workers times too often.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `X7_generation_size_drops_the_width`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 9 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_child_that_dies_mid_generation_ends_the_run_rather_than_hanging`
  - `tests/test_pool_sizing.py::test_a_plan_carries_the_item_count_it_was_decided_for`
  - `tests/test_pool_sizing.py::test_a_plan_says_how_many_generations_of_children_its_work_takes[16-2]`
  - `tests/test_pool_sizing.py::test_a_plan_says_how_many_generations_of_children_its_work_takes[17-3]`
  - `tests/test_pool_sizing.py::test_a_plan_says_how_many_generations_of_children_its_work_takes[8-1]`
  - `tests/test_pool_sizing.py::test_a_plan_says_how_many_generations_of_children_its_work_takes[9-2]`
  - `tests/test_pool_sizing.py::test_no_child_survives_a_generation_boundary_and_every_one_reloads_its_model`
  - `tests/test_pool_sizing.py::test_the_recycle_budget_retires_a_child_occasionally_rather_than_constantly[a-ten-thousand-track-folder]`
  - `tests/test_pool_sizing.py::test_the_recycle_budget_retires_a_child_occasionally_rather_than_constantly[an-ordinary-folder]`

Old text:

```
        return self.workers * self.max_tasks_per_child

```

New text:

```
        return self.max_tasks_per_child

```

### `u241.M01_worker_takes_the_interrupt`

stream worker: no longer ignore the terminal's interrupt, so Ctrl-C kills a worker mid item

- File: `src/cratekit/core/pool.py`
- Source: `u241.json`, row `M01_worker_takes_the_interrupt`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_stream.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_stream.py::test_the_terminals_interrupt_does_not_kill_a_stream_worker`

Old text:

```
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    _leave_when_the_parent_does()

```

New text:

```
    _leave_when_the_parent_does()

```

### `u241.M02_worker_outlives_its_parent`

stream worker: do not watch the parent, so a killed driver leaves its workers holding their memory

- File: `src/cratekit/core/pool.py`
- Source: `u241.json`, row `M02_worker_outlives_its_parent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_stream.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_stream.py::test_workers_leave_when_their_parent_is_killed_outright`

Old text:

```
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    _leave_when_the_parent_does()

```

New text:

```
    signal.signal(signal.SIGINT, signal.SIG_IGN)

```

### `u241.M03_close_waits_for_unread_work`

WorkStream._stop: do not end the workers, so a close waits for every item nobody will read

- File: `src/cratekit/core/pool.py`
- Source: `u241.json`, row `M03_close_waits_for_unread_work`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_stream.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_stream.py::test_a_close_ends_the_workers_without_waiting_for_work_nobody_will_read`

Old text:

```
        _end_workers(executor)
        executor.shutdown(wait=True, cancel_futures=True)

```

New text:

```
        executor.shutdown(wait=True, cancel_futures=True)

```

### `u241.M07_used_percent_gate_is_strict`

_gates_refusing: the used percent gate refuses only above its limit, not at it

- File: `src/cratekit/core/pool.py`
- Source: `u241.json`, row `M07_used_percent_gate_is_strict`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_stream.py`, `tests/test_pool_sizing.py`
- Collected: 295 against a baseline of 295
- Kills: 3 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_the_pressure_gate_bites_at_its_two_lines_and_nowhere_else[percent-at-the-line]`
  - `tests/test_pool_sizing.py::test_the_used_percent_ceiling_is_eighty_five_and_the_number_is_load_bearing[at-the-line]`
  - `tests/test_pool_stream.py::test_a_plan_refused_by_both_gates_names_both_swap_first`

Old text:

```
    if pressure.used_percent >= used_percent_ceiling:
        refused.append(

```

New text:

```
    if pressure.used_percent > used_percent_ceiling:
        refused.append(

```

### `u241.M08_plan_forgets_which_gate`

plan_pool: a plan refused by pressure no longer carries which gate refused it

- File: `src/cratekit/core/pool.py`
- Source: `u241.json`, row `M08_plan_forgets_which_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_stream.py`, `tests/test_analysis_ahead.py`
- Collected: 298 against a baseline of 298
- Kills: 6 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_machine_deep_in_swap_runs_one_worker_and_names_the_swap_gate`
  - `tests/test_analysis_ahead.py::test_a_machine_using_most_of_its_memory_names_the_used_percent_gate`
  - `tests/test_analysis_ahead.py::test_a_run_that_fails_part_way_says_its_pool_on_the_refusal_and_matches_the_serial_run`
  - `tests/test_pool_stream.py::test_a_plan_refused_by_both_gates_names_both_swap_first`
  - `tests/test_pool_stream.py::test_a_plan_refused_by_swap_names_the_gate_the_reading_and_the_limit`
  - `tests/test_pool_stream.py::test_a_plan_refused_by_the_used_percent_names_that_gate`

Old text:

```
            ceiling=ceiling,
            refused_by=refused,

```

New text:

```
            ceiling=ceiling,

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

### `u27-round-8-independent.E4_path_missing_reads_ok`

A matching identity with an absent root resolves to OK instead of LIBRARY_PATH_MISSING

- File: `src/cratekit/core/preflight.py`
- Source: `u27-round-8-independent.json`, row `E4_path_missing_reads_ok`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_preflight.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 740 against a baseline of 740
- Kills: 4 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_unresolved_session_is_never_reported_clean_because_its_disk_is_gone`
  - `tests/test_doctor.py::test_no_acknowledgment_is_claimed_absent_off_a_volume_nobody_read`
  - `tests/test_preflight.py::test_the_right_volume_with_a_missing_library_subdirectory_is_its_own_cause`
  - `tests/test_write_session.py::test_a_matched_volume_with_the_directory_absent_is_left_to_the_pass_that_follows_the_rule`

Old text:

```
            MountState.OK if root_exists else MountState.LIBRARY_PATH_MISSING,
```

New text:

```
            MountState.OK,
```

### `u27-round-8-independent.E5_unmounted_reads_foreign`

An absent volume resolves to FOREIGN_VOLUME instead of NOT_MOUNTED

- File: `src/cratekit/core/preflight.py`
- Source: `u27-round-8-independent.json`, row `E5_unmounted_reads_foreign`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_preflight.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 740 against a baseline of 740
- Kills: 5 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_unmounted_volume_and_a_moved_volume_produce_different_messages`
  - `tests/test_doctor.py::test_the_wizard_refuses_to_write_when_the_volume_is_not_mounted_at_all`
  - `tests/test_preflight.py::test_a_volume_that_is_not_mounted_refuses_with_its_own_cause`
  - `tests/test_preflight.py::test_the_three_refusals_are_distinguishable_from_each_other`
  - `tests/test_write_session.py::test_a_recorded_volume_that_is_not_mounted_anywhere_has_its_own_slug`

Old text:

```
        MountState.NOT_MOUNTED if not root_exists else MountState.FOREIGN_VOLUME,
```

New text:

```
        MountState.FOREIGN_VOLUME,
```

### `u27-round-8-independent.E6_write_table_shares_read`

Make the write table refuse LIBRARY_PATH_MISSING, the row it differs from the read table on

- File: `src/cratekit/core/preflight.py`
- Source: `u27-round-8-independent.json`, row `E6_write_table_shares_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_preflight.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 740 against a baseline of 740
- Kills: 3 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_renamed_library_folder_on_the_right_volume_is_written_not_refused`
  - `tests/test_doctor.py::test_every_mount_outcome_permits_exactly_what_it_is_declared_to[_STATE_WRITABLE-expected1]`
  - `tests/test_doctor.py::test_the_two_tables_differ_in_three_rows_and_every_one_is_a_read_signal_removed`

Old text:

```
    MountState.LIBRARY_PATH_MISSING: Reach.ALWAYS,
```

New text:

```
    MountState.LIBRARY_PATH_MISSING: Reach.NEVER,
```

### `u173.M20_agent_process`

processes: the agent's process name spelled otherwise, so the skill's pgrep waits on the wrong name

- File: `src/cratekit/core/processes.py`
- Source: `u173.json`, row `M20_agent_process`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rekordbox_visit_skill.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_rekordbox_visit_skill.py::test_it_waits_on_the_processes_the_product_watches`

Old text:

```
REKORDBOX_PROCESSES: tuple[str, ...] = ("rekordbox", "rekordboxAgent")
```

New text:

```
REKORDBOX_PROCESSES: tuple[str, ...] = ("rekordbox", "rekordbox_agent")
```

### `u211.P10_read_rekordbox_is_running`

rekordbox_processes_running: refuse as unconfirmed even when the scan read a rekordbox process

- File: `src/cratekit/core/processes.py`
- Source: `u211.json`, row `P10_read_rekordbox_is_running`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`
- Collected: 58 against a baseline of 58
- Kills: 5 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_process_that_is_dead_or_dying_is_skipped[rekordbox-read-beside-an-unreadable-process]`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[agent]`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[both]`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[rekordbox]`
  - `tests/test_process_scan.py::test_doctor_still_fails_a_running_rekordbox_beside_an_unreadable_process`

Old text:

```
        if not seen.intersection(REKORDBOX_PROCESSES):
            raise
```

New text:

```
        if True:
            raise
```

### `u211.P11_unconfirmed_is_not_absent`

rekordbox_processes_running: swallow the refusal when no rekordbox was read, so absence is read out of an unreadable process

- File: `src/cratekit/core/processes.py`
- Source: `u211.json`, row `P11_unconfirmed_is_not_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`, `tests/test_paths_resolved.py`
- Collected: 109 against a baseline of 109
- Kills: 11 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_backup_refuses_the_database_portion_alone_and_still_mirrors`
  - `tests/test_process_scan.py::test_a_process_list_that_cannot_be_read_refuses_with_no_pid`
  - `tests/test_process_scan.py::test_a_system_error_on_a_live_process_refuses_naming_the_pid`
  - `tests/test_process_scan.py::test_any_error_on_a_live_process_refuses_rather_than_reading_absent[cannot-even-be-built]`
  - `tests/test_process_scan.py::test_any_error_on_a_live_process_refuses_rather_than_reading_absent[os-error]`
  - `tests/test_process_scan.py::test_any_error_on_a_live_process_refuses_rather_than_reading_absent[runtime-error]`
  - `tests/test_process_scan.py::test_any_error_on_a_live_process_refuses_rather_than_reading_absent[status-unreadable-too]`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[none]`
  - `tests/test_process_scan.py::test_doctor_names_an_unreadable_live_process_as_a_note`
  - `tests/test_process_scan.py::test_many_unreadable_pids_are_counted_past_the_named_ones`
  - `tests/test_process_scan.py::test_the_whole_list_is_walked_and_every_unreadable_pid_is_named`

Old text:

```
        if not seen.intersection(REKORDBOX_PROCESSES):
            raise
```

New text:

```
        if False:
            raise
```

### `u211.P12_careful_pid_refuses`

rekordbox_pid: answer zero over an unreadable live process when the name was not read

- File: `src/cratekit/core/processes.py`
- Source: `u211.json`, row `P12_careful_pid_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`
- Collected: 58 against a baseline of 58
- Kills: 8 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[none]`
  - `tests/test_process_scan.py::test_the_binding_probe_is_put_back_after_a_refusal`
  - `tests/test_process_scan.py::test_the_binding_probe_refuses_a_live_unreadable_process_at_commit`
  - `tests/test_process_scan.py::test_the_careful_pid_names_a_rekordbox_it_read_beside_an_unreadable_process`
  - `tests/test_process_scan.py::test_the_careful_pid_refuses_over_an_unreadable_live_process`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`
  - `tests/test_process_scan.py::test_the_writer_refuses_a_live_unreadable_process_by_name_not_as_internal`

Old text:

```
        if not any(executable_stem(found) == name for _pid, found in listed):
            raise
```

New text:

```
        if False:
            raise
```

### `u211.P1_denied_is_skipped`

running_processes: drop AccessDenied from the skip tuple, so a denied process is re-checked and refuses as unreadable

- File: `src/cratekit/core/processes.py`
- Source: `u211.json`, row `P1_denied_is_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_process_psutil_reports_gone_denied_or_zombie_is_skipped[denied]`

Old text:

```
        except (table.NoSuchProcess, table.ZombieProcess, table.AccessDenied):
```

New text:

```
        except (table.NoSuchProcess, table.ZombieProcess):
```

### `u211.P2_gone_is_skipped`

running_processes: skip only ZombieProcess and AccessDenied, so a process psutil reports gone falls to the re-check

- File: `src/cratekit/core/processes.py`
- Source: `u211.json`, row `P2_gone_is_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_process_psutil_reports_gone_denied_or_zombie_is_skipped[gone]`

Old text:

```
        except (table.NoSuchProcess, table.ZombieProcess, table.AccessDenied):
```

New text:

```
        except (table.ZombieProcess, table.AccessDenied):
```

### `u211.P3_recheck_before_refusing`

running_processes: refuse every process whose read raised, without asking whether it is now gone or a zombie

- File: `src/cratekit/core/processes.py`
- Source: `u211.json`, row `P3_recheck_before_refusing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`
- Collected: 58 against a baseline of 58
- Kills: 9 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_a_process_that_is_dead_or_dying_is_skipped[fails-to-build-then-gone]`
  - `tests/test_process_scan.py::test_a_process_that_is_dead_or_dying_is_skipped[system-error-then-status-zombie]`
  - `tests/test_process_scan.py::test_doctor_reads_a_skipped_zombie_as_nothing`
  - `tests/test_process_scan.py::test_the_binding_probe_skips_a_zombie_at_commit`
  - `tests/test_process_scan.py::test_the_careful_pid_answers_as_pyrekordbox_does`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`
  - `tests/test_process_scan.py::test_the_whole_list_is_walked_and_every_unreadable_pid_is_named`
  - `tests/test_process_scan.py::test_the_writer_skips_a_zombie_pyrekordbox_could_not_read`

Old text:

```
            if _gone_or_zombie(table, pid, process):
                continue
```

New text:

```
            if False:
                continue
```

### `u211.P4_zombie_status_reads_zombie`

_gone_or_zombie: never read the status as zombie, so the sitting's dying daemon refuses

- File: `src/cratekit/core/processes.py`
- Source: `u211.json`, row `P4_zombie_status_reads_zombie`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`
- Collected: 58 against a baseline of 58
- Kills: 8 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_a_process_that_is_dead_or_dying_is_skipped[system-error-then-status-zombie]`
  - `tests/test_process_scan.py::test_doctor_reads_a_skipped_zombie_as_nothing`
  - `tests/test_process_scan.py::test_the_binding_probe_skips_a_zombie_at_commit`
  - `tests/test_process_scan.py::test_the_careful_pid_answers_as_pyrekordbox_does`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`
  - `tests/test_process_scan.py::test_the_whole_list_is_walked_and_every_unreadable_pid_is_named`
  - `tests/test_process_scan.py::test_the_writer_skips_a_zombie_pyrekordbox_could_not_read`

Old text:

```
        return target.status() == platform.STATUS_ZOMBIE
```

New text:

```
        return target.status() == platform.STATUS_DEAD
```

### `u211.P5_gone_on_status_read`

_gone_or_zombie: a status read that says no such process answers not gone

- File: `src/cratekit/core/processes.py`
- Source: `u211.json`, row `P5_gone_on_status_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_process_that_is_dead_or_dying_is_skipped[fails-to-build-then-gone]`

Old text:

```
        # ``ZombieProcess`` is a subclass, so a status read that says zombie
        # by raising lands here too.
        return True
```

New text:

```
        # ``ZombieProcess`` is a subclass, so a status read that says zombie
        # by raising lands here too.
        return False
```

### `u211.P6_unreadable_status_is_not_gone`

_gone_or_zombie: an unreadable status answers gone, so a live process neither readable nor known gone is skipped

- File: `src/cratekit/core/processes.py`
- Source: `u211.json`, row `P6_unreadable_status_is_not_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`
- Collected: 58 against a baseline of 58
- Kills: 2 (killed)
- Killed:
  - `tests/test_process_scan.py::test_any_error_on_a_live_process_refuses_rather_than_reading_absent[cannot-even-be-built]`
  - `tests/test_process_scan.py::test_any_error_on_a_live_process_refuses_rather_than_reading_absent[status-unreadable-too]`

Old text:

```
    except Exception:  # noqa: BLE001 - an unreadable status confirms nothing
        return False
```

New text:

```
    except Exception:  # noqa: BLE001 - an unreadable status confirms nothing
        return True
```

### `u211.P7_unreadable_refuses`

running_processes: answer the processes it read and drop the refusal, so an unreadable live process reads as absent

- File: `src/cratekit/core/processes.py`
- Source: `u211.json`, row `P7_unreadable_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`, `tests/test_paths_resolved.py`
- Collected: 109 against a baseline of 109
- Kills: 17 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_backup_refuses_the_database_portion_alone_and_still_mirrors`
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_a_system_error_on_a_live_process_refuses_naming_the_pid`
  - `tests/test_process_scan.py::test_any_error_on_a_live_process_refuses_rather_than_reading_absent[cannot-even-be-built]`
  - `tests/test_process_scan.py::test_any_error_on_a_live_process_refuses_rather_than_reading_absent[os-error]`
  - `tests/test_process_scan.py::test_any_error_on_a_live_process_refuses_rather_than_reading_absent[runtime-error]`
  - `tests/test_process_scan.py::test_any_error_on_a_live_process_refuses_rather_than_reading_absent[status-unreadable-too]`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[none]`
  - `tests/test_process_scan.py::test_doctor_names_an_unreadable_live_process_as_a_note`
  - `tests/test_process_scan.py::test_many_unreadable_pids_are_counted_past_the_named_ones`
  - `tests/test_process_scan.py::test_the_binding_probe_is_put_back_after_a_refusal`
  - `tests/test_process_scan.py::test_the_binding_probe_refuses_a_live_unreadable_process_at_commit`
  - `tests/test_process_scan.py::test_the_careful_pid_names_a_rekordbox_it_read_beside_an_unreadable_process`
  - `tests/test_process_scan.py::test_the_careful_pid_refuses_over_an_unreadable_live_process`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`
  - ... and 2 more, see the JSON sidecar

Old text:

```
    if unreadable:
        raise _unconfirmed(unreadable, found) from first
```

New text:

```
    if False:
        raise _unconfirmed(unreadable, found) from first
```

### `u211.P8_unreadable_pid_list_refuses`

running_processes: a pid list that cannot be read is read as an empty machine

- File: `src/cratekit/core/processes.py`
- Source: `u211.json`, row `P8_unreadable_pid_list_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_process_list_that_cannot_be_read_refuses_with_no_pid`

Old text:

```
        raise _unconfirmed([(None, _spelled(exc))]) from exc
```

New text:

```
        pids = []
```

### `u211.P9_whole_list_walked`

running_processes: stop at the first unreadable process, so later pids, rekordbox among them, are never read or named

- File: `src/cratekit/core/processes.py`
- Source: `u211.json`, row `P9_whole_list_walked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`
- Collected: 58 against a baseline of 58
- Kills: 3 (killed)
- Killed:
  - `tests/test_process_scan.py::test_many_unreadable_pids_are_counted_past_the_named_ones`
  - `tests/test_process_scan.py::test_the_careful_pid_names_a_rekordbox_it_read_beside_an_unreadable_process`
  - `tests/test_process_scan.py::test_the_whole_list_is_walked_and_every_unreadable_pid_is_named`

Old text:

```
            first = first or exc
            continue
```

New text:

```
            first = first or exc
            break
```

### `r705-a.G10_long_wait_under_the_lock`

a Retry-After wait is slept holding the lock, so a second driver waits on the holder

- File: `src/cratekit/core/provider_gate.py`
- Source: `r705-a.json`, row `G10_long_wait_under_the_lock`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 117 against a baseline of 117
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_wait_the_provider_asked_for_is_taken_with_the_lock_released`

Old text:

```
                if due - now > self.settings.min_interval_s:

```

New text:

```
                if False:

```

### `r705-a.G11_lock_limit_without_the_interval`

the lock wait limit drops the one interval a holder may sleep under it

- File: `src/cratekit/core/provider_gate.py`
- Source: `r705-a.json`, row `G11_lock_limit_without_the_interval`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 117 against a baseline of 117
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_lock_held_past_the_wait_is_refused_with_the_holder_named`

Old text:

```
                limit = LOCK_WAIT_S + self.settings.min_interval_s

```

New text:

```
                limit = LOCK_WAIT_S

```

### `r705-a.G12_park_forgotten`

a park the tool swallowed is not remembered, so the vendored adapter reads it as no file

- File: `src/cratekit/core/provider_gate.py`
- Source: `r705-a.json`, row `G12_park_forgotten`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 117 against a baseline of 117
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_held_lock_the_tool_swallowed_during_a_download_comes_out_of_fetch`
  - `tests/test_provider_gate.py::test_the_stop_is_remembered_so_a_swallowing_tool_still_parks`

Old text:

```
        if self._last_park is not None:
            raise self._last_park

```

New text:

```
        if False:
            raise self._last_park

```

### `r705-a.G13_process_calls_not_counted`

this process's call counter never moves, so the spend line reports nothing

- File: `src/cratekit/core/provider_gate.py`
- Source: `r705-a.json`, row `G13_process_calls_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 117 against a baseline of 117
- Kills: 19 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_ceiling_stop_a_verb_swallowed_is_still_said`
  - `tests/test_provider_gate.py::test_a_command_is_charged_only_for_its_own_calls`
  - `tests/test_provider_gate.py::test_a_command_stops_before_the_call_past_its_ceiling_with_the_count_at_the_ceiling`
  - `tests/test_provider_gate.py::test_a_nested_dispatch_keeps_the_outer_commands_count`
  - `tests/test_provider_gate.py::test_a_raised_ceiling_lasts_one_run_and_the_next_is_back_at_the_configured_one`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[excludes-another-processs-calls]`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[names-rate-limit-answers]`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[reports-its-calls]`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[survives-a-refusal]`
  - `tests/test_provider_gate.py::test_a_separate_session_such_as_the_media_segment_fetch_is_not_counted`
  - `tests/test_provider_gate.py::test_a_verb_at_its_line_is_blocked_and_the_call_past_it_is_not_sent[its-ceiling-names-the-exact-command-that-continues]`
  - `tests/test_provider_gate.py::test_calls_on_the_command_line_lets_one_run_pass_and_the_next_is_back_at_the_ceiling`
  - `tests/test_provider_gate.py::test_process_spend_is_this_process_alone`
  - `tests/test_provider_gate.py::test_the_ceiling_never_says_kept_over_work_a_continue_does_again`
  - `tests/test_provider_gate.py::test_the_ceiling_parks_a_job_and_the_resumed_job_continues`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        _PROCESS_CALLS += 1

```

New text:

```
        _PROCESS_CALLS += 0

```

### `r705-a.G1_interval_halved`

the shared interval is halved, so consecutive calls wait half of what the configuration says

- File: `src/cratekit/core/provider_gate.py`
- Source: `r705-a.json`, row `G1_interval_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 117 against a baseline of 117
- Kills: 9 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_retry_after_holds_the_next_call_at_least_that_long[shorter-keeps-the-interval]`
  - `tests/test_provider_gate.py::test_a_retry_after_holds_the_next_call_at_least_that_long[unreadable-is-zero]`
  - `tests/test_provider_gate.py::test_a_wait_the_provider_asked_for_is_taken_with_the_lock_released`
  - `tests/test_provider_gate.py::test_attach_routes_every_request_of_a_real_session_through_the_gate_once`
  - `tests/test_provider_gate.py::test_consecutive_calls_wait_out_the_interval`
  - `tests/test_provider_gate.py::test_the_interval_is_measured_from_the_last_call_by_any_gate`
  - `tests/test_provider_gate.py::test_the_interval_is_the_configured_one`
  - `tests/test_provider_gate.py::test_the_vendored_adapter_attaches_the_gate_to_an_injected_session`
  - `tests/test_provider_gate.py::test_two_processes_keep_the_interval_between_every_call`

Old text:

```
                due = max(state.last_call + self.settings.min_interval_s, state.not_before)

```

New text:

```
                due = max(state.last_call + self.settings.min_interval_s / 2, state.not_before)

```

### `r705-a.G2_last_call_ignored`

the interval is measured from now rather than from the last call any process made, so a second gate never waits on the first

- File: `src/cratekit/core/provider_gate.py`
- Source: `r705-a.json`, row `G2_last_call_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 117 against a baseline of 117
- Kills: 9 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_retry_after_holds_the_next_call_at_least_that_long[shorter-keeps-the-interval]`
  - `tests/test_provider_gate.py::test_a_retry_after_holds_the_next_call_at_least_that_long[unreadable-is-zero]`
  - `tests/test_provider_gate.py::test_a_wait_the_provider_asked_for_is_taken_with_the_lock_released`
  - `tests/test_provider_gate.py::test_attach_routes_every_request_of_a_real_session_through_the_gate_once`
  - `tests/test_provider_gate.py::test_consecutive_calls_wait_out_the_interval`
  - `tests/test_provider_gate.py::test_the_interval_is_measured_from_the_last_call_by_any_gate`
  - `tests/test_provider_gate.py::test_the_interval_is_the_configured_one`
  - `tests/test_provider_gate.py::test_the_vendored_adapter_attaches_the_gate_to_an_injected_session`
  - `tests/test_provider_gate.py::test_two_processes_keep_the_interval_between_every_call`

Old text:

```
                due = max(state.last_call + self.settings.min_interval_s, state.not_before)

```

New text:

```
                due = max(now, state.not_before)

```

### `r705-a.G3_retry_after_ignored`

a Retry-After the provider sends no longer holds the next call

- File: `src/cratekit/core/provider_gate.py`
- Source: `r705-a.json`, row `G3_retry_after_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 117 against a baseline of 117
- Kills: 3 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_retry_after_holds_the_next_call_at_least_that_long[http-date-honoured]`
  - `tests/test_provider_gate.py::test_a_retry_after_holds_the_next_call_at_least_that_long[seconds-hold-the-next-call]`
  - `tests/test_provider_gate.py::test_a_wait_the_provider_asked_for_is_taken_with_the_lock_released`

Old text:

```
                state.not_before = max(state.not_before, now + retry_after)

```

New text:

```
                state.not_before = state.not_before

```

### `r705-a.G4_trip_after_off_by_one`

the breaker trips one answer late, after seven rather than the six a spent ladder costs

- File: `src/cratekit/core/provider_gate.py`
- Source: `r705-a.json`, row `G4_trip_after_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 117 against a baseline of 117
- Kills: 3 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_spent_ladder_through_the_gate_comes_out_as_the_park`
  - `tests/test_provider_gate.py::test_the_breaker_stops_a_sweep_at_the_first_surviving_rate_limit_with_the_rest_pending`
  - `tests/test_provider_gate.py::test_the_trip_count_is_one_spent_ladder`

Old text:

```
TRIP_AFTER = 6

```

New text:

```
TRIP_AFTER = 7

```

### `r705-a.G5_no_trip_on_long_retry_after`

a Retry-After at or above the cooldown no longer trips at once

- File: `src/cratekit/core/provider_gate.py`
- Source: `r705-a.json`, row `G5_no_trip_on_long_retry_after`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 117 against a baseline of 117
- Kills: 5 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_rate_limited_login_comes_out_of_client_session_as_the_park`
  - `tests/test_provider_gate.py::test_a_rate_limited_login_comes_out_of_the_vendored_adapter_as_the_park`
  - `tests/test_provider_gate.py::test_a_retry_after_at_or_above_the_cooldown_trips_at_once[at-the-cooldown]`
  - `tests/test_provider_gate.py::test_a_retry_after_at_or_above_the_cooldown_trips_at_once[longer-than-the-cooldown]`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[survives-a-refusal]`

Old text:

```
            if state.consecutive >= TRIP_AFTER or retry_after >= self.settings.cooldown_s:

```

New text:

```
            if state.consecutive >= TRIP_AFTER:

```

### `r705-a.G6_cooldown_not_recorded`

the trip lifts at once, so no later verb is refused

- File: `src/cratekit/core/provider_gate.py`
- Source: `r705-a.json`, row `G6_cooldown_not_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 117 against a baseline of 117
- Kills: 7 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_retry_after_at_or_above_the_cooldown_trips_at_once[at-the-cooldown]`
  - `tests/test_provider_gate.py::test_a_retry_after_at_or_above_the_cooldown_trips_at_once[longer-than-the-cooldown]`
  - `tests/test_provider_gate.py::test_client_session_refuses_inside_the_cooldown_before_building_a_client`
  - `tests/test_provider_gate.py::test_inside_the_cooldown_assert_open_refuses_naming_the_lift_time`
  - `tests/test_provider_gate.py::test_the_cooldown_refuses_a_call_until_it_lifts[inside-a-call-is-refused-before-it-is-sent]`
  - `tests/test_provider_gate.py::test_the_sixth_consecutive_rate_limit_answer_trips_and_records_the_cooldown`
  - `tests/test_provider_gate.py::test_the_vendored_adapter_refuses_inside_the_cooldown_before_touching_the_tool`

Old text:

```
                state.lifts_at = now + max(self.settings.cooldown_s, retry_after)

```

New text:

```
                state.lifts_at = now

```

### `r705-a.G7_success_keeps_the_run`

a successful answer no longer breaks the run of rate limit answers, so six spread over a day trip the breaker

- File: `src/cratekit/core/provider_gate.py`
- Source: `r705-a.json`, row `G7_success_keeps_the_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 117 against a baseline of 117
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_success_breaks_the_run_of_rate_limit_answers`

Old text:

```
        state.consecutive = 0
        state.not_before = 0.0
        self._last_park = None

```

New text:

```
        state.not_before = 0.0
        self._last_park = None

```

### `r705-a.G8_call_ignores_the_cooldown`

a call inside the cooldown is made anyway

- File: `src/cratekit/core/provider_gate.py`
- Source: `r705-a.json`, row `G8_call_ignores_the_cooldown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 117 against a baseline of 117
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_cooldown_written_by_one_process_refuses_a_verb_started_in_another`
  - `tests/test_provider_gate.py::test_the_cooldown_refuses_a_call_until_it_lifts[inside-a-call-is-refused-before-it-is-sent]`

Old text:

```
                if state.cooling(now):
                    raise self._stopped(self._cooldown_cause(state, now, tripped_now=False))

```

New text:

```
                if False:
                    raise self._stopped(self._cooldown_cause(state, now, tripped_now=False))

```

### `r705-a.G9_assert_open_ignores_the_cooldown`

an opener asking the gate inside the cooldown is told to go ahead

- File: `src/cratekit/core/provider_gate.py`
- Source: `r705-a.json`, row `G9_assert_open_ignores_the_cooldown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 117 against a baseline of 117
- Kills: 4 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_cooldown_written_by_one_process_refuses_a_verb_started_in_another`
  - `tests/test_provider_gate.py::test_client_session_refuses_inside_the_cooldown_before_building_a_client`
  - `tests/test_provider_gate.py::test_inside_the_cooldown_assert_open_refuses_naming_the_lift_time`
  - `tests/test_provider_gate.py::test_the_vendored_adapter_refuses_inside_the_cooldown_before_touching_the_tool`

Old text:

```
        if state.cooling(now):
            raise self._stopped(self._cooldown_cause(state, now, tripped_now=False))

```

New text:

```
        if False:
            raise self._stopped(self._cooldown_cause(state, now, tripped_now=False))

```

### `r759-b.P4_lock_removed_r01`

the one call at a time lock is never taken, so two processes can have a request in flight together, repeat 1 of 10

- File: `src/cratekit/core/provider_gate.py`
- Source: `r759-b.json`, row `P4_lock_removed_r01`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py::test_two_processes_never_have_a_call_in_flight_together`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_two_processes_never_have_a_call_in_flight_together`

Old text:

```
                        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)

```

New text:

```
                        pass

```

### `r759.P1_interval_dropped`

the interval is dropped from the due time, so a call waits on nothing but a Retry-After and two processes call back to back

- File: `src/cratekit/core/provider_gate.py`
- Source: `r759.json`, row `P1_interval_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py::test_two_processes_keep_the_interval_between_every_call`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_two_processes_keep_the_interval_between_every_call`

Old text:

```
                due = max(state.last_call + self.settings.min_interval_s, state.not_before)

```

New text:

```
                due = max(state.last_call, state.not_before)

```

### `r759.P5_lock_shared`

the lock is taken shared rather than exclusive, so every process holds it at once

- File: `src/cratekit/core/provider_gate.py`
- Source: `r759.json`, row `P5_lock_shared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py::test_two_processes_never_have_a_call_in_flight_together`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_two_processes_never_have_a_call_in_flight_together`

Old text:

```
                        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)

```

New text:

```
                        fcntl.flock(fd, fcntl.LOCK_SH | fcntl.LOCK_NB)

```

### `r759.P6_wait_skipped_stamp_kept`

the wait before a call is skipped while its stamp still reads the due time, so the stamps stay spaced and the requests go out back to back

- File: `src/cratekit/core/provider_gate.py`
- Source: `r759.json`, row `P6_wait_skipped_stamp_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py::test_two_processes_keep_the_interval_between_every_call`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_two_processes_keep_the_interval_between_every_call`

Old text:

```
        if due > now:
            self._sleep(due - now)
            now = max(self._clock(), due)

```

New text:

```
        if due > now:
            now = max(self._clock(), due)

```

### `u193.M10_config_not_read`

GateSettings.from_config: drop the configured ceiling, so the default always holds

- File: `src/cratekit/core/provider_gate.py`
- Source: `u193.json`, row `M10_config_not_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 509 against a baseline of 509
- Kills: 4 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_ceiling_stop_a_verb_swallowed_is_still_said`
  - `tests/test_provider_gate.py::test_a_verb_at_its_line_is_blocked_and_the_call_past_it_is_not_sent[its-ceiling-names-the-exact-command-that-continues]`
  - `tests/test_provider_gate.py::test_calls_on_the_command_line_lets_one_run_pass_and_the_next_is_back_at_the_ceiling`
  - `tests/test_provider_gate.py::test_the_ceiling_defaults_to_five_hundred_and_round_trips`

Old text:

```
            calls_per_command=int(provider.calls_per_command),
```

New text:

```
(empty)
```

### `u193.M1_ceiling_check_removed`

Gate.call: never ask the ceiling, so a command spends past it

- File: `src/cratekit/core/provider_gate.py`
- Source: `u193.json`, row `M1_ceiling_check_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 509 against a baseline of 509
- Kills: 13 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_ceiling_stop_a_verb_swallowed_is_still_said`
  - `tests/test_provider_gate.py::test_a_command_is_charged_only_for_its_own_calls`
  - `tests/test_provider_gate.py::test_a_command_stops_before_the_call_past_its_ceiling_with_the_count_at_the_ceiling`
  - `tests/test_provider_gate.py::test_a_nested_dispatch_keeps_the_outer_commands_count`
  - `tests/test_provider_gate.py::test_a_raised_ceiling_lasts_one_run_and_the_next_is_back_at_the_configured_one`
  - `tests/test_provider_gate.py::test_a_separate_session_such_as_the_media_segment_fetch_is_not_counted`
  - `tests/test_provider_gate.py::test_a_verb_at_its_line_is_blocked_and_the_call_past_it_is_not_sent[its-ceiling-names-the-exact-command-that-continues]`
  - `tests/test_provider_gate.py::test_calls_on_the_command_line_lets_one_run_pass_and_the_next_is_back_at_the_ceiling`
  - `tests/test_provider_gate.py::test_the_ceiling_never_says_kept_over_work_a_continue_does_again`
  - `tests/test_provider_gate.py::test_the_ceiling_parks_a_job_and_the_resumed_job_continues`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_calls_already_given[joined]`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_calls_already_given[spaced]`
  - `tests/test_provider_gate.py::test_the_stop_is_remembered_so_a_swallowing_tool_still_parks`

Old text:

```
                    if scope.spent() >= line:
```

New text:

```
                    if False:
```

### `u193.M2_ceiling_off_by_one`

Gate.call: stop only past the ceiling, so one call more than the line is sent

- File: `src/cratekit/core/provider_gate.py`
- Source: `u193.json`, row `M2_ceiling_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 509 against a baseline of 509
- Kills: 13 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_ceiling_stop_a_verb_swallowed_is_still_said`
  - `tests/test_provider_gate.py::test_a_command_is_charged_only_for_its_own_calls`
  - `tests/test_provider_gate.py::test_a_command_stops_before_the_call_past_its_ceiling_with_the_count_at_the_ceiling`
  - `tests/test_provider_gate.py::test_a_nested_dispatch_keeps_the_outer_commands_count`
  - `tests/test_provider_gate.py::test_a_raised_ceiling_lasts_one_run_and_the_next_is_back_at_the_configured_one`
  - `tests/test_provider_gate.py::test_a_separate_session_such_as_the_media_segment_fetch_is_not_counted`
  - `tests/test_provider_gate.py::test_a_verb_at_its_line_is_blocked_and_the_call_past_it_is_not_sent[its-ceiling-names-the-exact-command-that-continues]`
  - `tests/test_provider_gate.py::test_calls_on_the_command_line_lets_one_run_pass_and_the_next_is_back_at_the_ceiling`
  - `tests/test_provider_gate.py::test_the_ceiling_never_says_kept_over_work_a_continue_does_again`
  - `tests/test_provider_gate.py::test_the_ceiling_parks_a_job_and_the_resumed_job_continues`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_calls_already_given[joined]`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_calls_already_given[spaced]`
  - `tests/test_provider_gate.py::test_the_stop_is_remembered_so_a_swallowing_tool_still_parks`

Old text:

```
                    if scope.spent() >= line:
```

New text:

```
                    if scope.spent() > line:
```

### `u193.M3_spent_from_process_start`

Command.spent: count from process start, so a command is charged for calls before it

- File: `src/cratekit/core/provider_gate.py`
- Source: `u193.json`, row `M3_spent_from_process_start`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 509 against a baseline of 509
- Kills: 13 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_ceiling_stop_a_verb_swallowed_is_still_said`
  - `tests/test_provider_gate.py::test_a_command_is_charged_only_for_its_own_calls`
  - `tests/test_provider_gate.py::test_a_command_stops_before_the_call_past_its_ceiling_with_the_count_at_the_ceiling`
  - `tests/test_provider_gate.py::test_a_nested_dispatch_keeps_the_outer_commands_count`
  - `tests/test_provider_gate.py::test_a_raised_ceiling_lasts_one_run_and_the_next_is_back_at_the_configured_one`
  - `tests/test_provider_gate.py::test_a_separate_session_such_as_the_media_segment_fetch_is_not_counted`
  - `tests/test_provider_gate.py::test_a_verb_at_its_line_is_blocked_and_the_call_past_it_is_not_sent[its-ceiling-names-the-exact-command-that-continues]`
  - `tests/test_provider_gate.py::test_calls_on_the_command_line_lets_one_run_pass_and_the_next_is_back_at_the_ceiling`
  - `tests/test_provider_gate.py::test_the_ceiling_never_says_kept_over_work_a_continue_does_again`
  - `tests/test_provider_gate.py::test_the_ceiling_parks_a_job_and_the_resumed_job_continues`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_calls_already_given[joined]`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_calls_already_given[spaced]`
  - `tests/test_provider_gate.py::test_the_stop_is_remembered_so_a_swallowing_tool_still_parks`

Old text:

```
        return max(0, _PROCESS_CALLS - self.started)
```

New text:

```
        return max(0, _PROCESS_CALLS)
```

### `u193.M8_raised_ignored`

ceiling: ignore the raised ceiling, so --calls never lifts the line

- File: `src/cratekit/core/provider_gate.py`
- Source: `u193.json`, row `M8_raised_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 509 against a baseline of 509
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_playlists_releases.py::test_a_ceiling_raised_low_for_the_run_is_said_at_the_crawl_gate`
  - `tests/test_provider_gate.py::test_a_detached_child_reads_the_raised_ceiling_off_the_environment[700-700]`
  - `tests/test_provider_gate.py::test_a_raised_ceiling_lasts_one_run_and_the_next_is_back_at_the_configured_one`
  - `tests/test_provider_gate.py::test_calls_on_the_command_line_lets_one_run_pass_and_the_next_is_back_at_the_ceiling`
  - `tests/test_provider_gate.py::test_the_ceiling_parks_a_job_and_the_resumed_job_continues`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_calls_already_given[joined]`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_calls_already_given[spaced]`

Old text:

```
    if scope is not None and scope.raised is not None:
        return scope.raised
```

New text:

```
    if False:
        return scope.raised
```

### `u205.G1_app_call_not_counted`

gate: a call under the app identity is counted in the totals and not under the app, so every report reads it as the account's

- File: `src/cratekit/core/provider_gate.py`
- Source: `u205.json`, row `G1_app_call_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_provider_gate.py`
- Collected: 183 against a baseline of 183
- Kills: 5 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_a_state_file_written_before_the_identities_loads_with_every_call_the_accounts`
  - `tests/test_catalogue_app.py::test_an_isrc_catalogue_lookup_goes_to_the_app_and_intake_missing_with_it`
  - `tests/test_catalogue_app.py::test_an_isrc_match_with_the_app_recorded_makes_no_account_call`
  - `tests/test_catalogue_app.py::test_process_spend_carries_the_apps_share`
  - `tests/test_catalogue_app.py::test_the_opener_attaches_the_app_client_under_the_app_identity`

Old text:

```
        if app:
            state.app_calls += 1
            _PROCESS_APP_CALLS += 1
```

New text:

```
        if False:
            state.app_calls += 1
            _PROCESS_APP_CALLS += 1
```

### `u205.G2_app_rate_limit_not_counted`

gate: a rate limit answer to the app is counted as the account's

- File: `src/cratekit/core/provider_gate.py`
- Source: `u205.json`, row `G2_app_rate_limit_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_provider_gate.py`
- Collected: 183 against a baseline of 183
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_a_rate_limit_on_the_app_trips_the_shared_gate_and_refuses_the_account_too`

Old text:

```
            if app:
                state.app_rate_limited += 1
```

New text:

```
            if False:
                state.app_rate_limited += 1
```

### `u205.G3_attach_drops_identity`

gate attach: the wrapped transport counts every call under the account whatever identity it was attached under

- File: `src/cratekit/core/provider_gate.py`
- Source: `u205.json`, row `G3_attach_drops_identity`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_provider_gate.py`
- Collected: 183 against a baseline of 183
- Kills: 6 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_a_rate_limit_on_the_app_trips_the_shared_gate_and_refuses_the_account_too`
  - `tests/test_catalogue_app.py::test_a_state_file_written_before_the_identities_loads_with_every_call_the_accounts`
  - `tests/test_catalogue_app.py::test_an_isrc_catalogue_lookup_goes_to_the_app_and_intake_missing_with_it`
  - `tests/test_catalogue_app.py::test_an_isrc_match_with_the_app_recorded_makes_no_account_call`
  - `tests/test_catalogue_app.py::test_process_spend_carries_the_apps_share`
  - `tests/test_catalogue_app.py::test_the_opener_attaches_the_app_client_under_the_app_identity`

Old text:

```
            return self.call(lambda: original(method, url, *args, **kwargs), identity=identity)
```

New text:

```
            return self.call(lambda: original(method, url, *args, **kwargs), identity=ACCOUNT)
```

### `u205.G5_app_share_unclamped`

gate state load: an app share above the total is kept, so the account's share reads negative and is shown as zero

- File: `src/cratekit/core/provider_gate.py`
- Source: `u205.json`, row `G5_app_share_unclamped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_provider_gate.py`
- Collected: 183 against a baseline of 183
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_an_app_share_larger_than_the_total_is_clamped_to_it`

Old text:

```
            state.app_calls = min(_as_int(app.get("calls")), state.calls)
```

New text:

```
            state.app_calls = _as_int(app.get("calls"))
```

### `u205.G6_file_account_share_is_the_total`

gate state write: the account's entry under identities is written as the total, the app's calls in it

- File: `src/cratekit/core/provider_gate.py`
- Source: `u205.json`, row `G6_file_account_share_is_the_total`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_provider_gate.py`
- Collected: 183 against a baseline of 183
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_a_state_file_written_before_the_identities_loads_with_every_call_the_accounts`
  - `tests/test_catalogue_app.py::test_an_isrc_match_with_the_app_recorded_makes_no_account_call`

Old text:

```
                    "calls": max(0, self.calls - self.app_calls),
```

New text:

```
                    "calls": self.calls,
```

### `u205.G7_process_spend_drops_app`

process spend: the app's share of this process's calls is not reported, so the spend line says every call was the account's

- File: `src/cratekit/core/provider_gate.py`
- Source: `u205.json`, row `G7_process_spend_drops_app`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_provider_gate.py`
- Collected: 183 against a baseline of 183
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_process_spend_carries_the_apps_share`

Old text:

```
        app_calls=_PROCESS_APP_CALLS,
```

New text:

```
        app_calls=0,
```

### `u205.G8_since_keeps_earlier_app_calls`

spend since: the app's share is not differenced, so a run is charged the app calls made before it

- File: `src/cratekit/core/provider_gate.py`
- Source: `u205.json`, row `G8_since_keeps_earlier_app_calls`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_provider_gate.py`
- Collected: 183 against a baseline of 183
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_process_spend_carries_the_apps_share`

Old text:

```
            app_calls=max(0, self.app_calls - earlier.app_calls),
```

New text:

```
            app_calls=self.app_calls,
```

### `u217.G1_ceiling_says_kept`

_ceiling_cause: say what it did is kept again, the words the card was filed over

- File: `src/cratekit/core/provider_gate.py`
- Source: `u217.json`, row `G1_ceiling_says_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 117 against a baseline of 117
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_the_ceiling_never_says_kept_over_work_a_continue_does_again`

Old text:

```
                f"stay queued; what it read and did not keep is read again when it "
                f"continues"
```

New text:

```
                f"stay queued; what it did is kept"
```

### `u278.M10_window_short`

_expires: a minute leaves the window an hour after it STARTS, sixty seconds early

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M10_window_short`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`
- Collected: 177 against a baseline of 177
- Kills: 5 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_call_at_the_line_is_not_sent_and_names_the_spend_and_when_it_frees`
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer[account]`
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer[app-credentials]`
  - `tests/test_provider_budget.py::test_doctor_names_an_identity_at_its_read_line_and_when_it_frees`
  - `tests/test_provider_budget.py::test_the_window_frees_as_its_oldest_minute_ages_out`

Old text:

```
    return float(bucket + BUCKET_S + WINDOW_S)
```

New text:

```
    return float(bucket + WINDOW_S)
```

### `u278.M11_window_dropped_on_read`

_State.from_json: drop the window on read, so every reader sees an empty hour

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M11_window_dropped_on_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`
- Collected: 177 against a baseline of 177
- Kills: 23 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_call_at_the_line_is_not_sent_and_names_the_spend_and_when_it_frees`
  - `tests/test_provider_budget.py::test_a_call_made_under_a_redirected_state_directory_is_counted_by_the_live_gate`
  - `tests/test_provider_budget.py::test_a_cooldown_still_refuses_first_and_keeps_its_own_reason`
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer[account]`
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer[app-credentials]`
  - `tests/test_provider_budget.py::test_a_read_dispatched_inside_a_write_runs_under_the_read_line`
  - `tests/test_provider_budget.py::test_a_read_is_held_to_the_read_line[a-raised-ceiling-never-spends-the-reserve]`
  - `tests/test_provider_budget.py::test_a_read_is_held_to_the_read_line[a-write-verb-running-a-read-mode]`
  - `tests/test_provider_budget.py::test_a_read_is_held_to_the_read_line[calls-up-to-the-budget-on-a-read]`
  - `tests/test_provider_budget.py::test_a_read_stops_at_the_reserve_while_a_go_still_runs`
  - `tests/test_provider_budget.py::test_a_sweep_whose_estimate_crosses_into_the_reserve_refuses_before_its_first_call`
  - `tests/test_provider_budget.py::test_a_verb_dispatched_again_inside_a_scope_runs_under_its_own_class`
  - `tests/test_provider_budget.py::test_an_hour_raised_in_the_environment_reaches_a_call_outside_any_scope`
  - `tests/test_provider_budget.py::test_doctor_shows_each_identitys_spend_against_its_line_and_the_reserve`
  - `tests/test_provider_budget.py::test_next_counts_no_label_past_the_first_saved_question`
  - ... and 8 more, see the JSON sidecar

Old text:

```
        state.window = _window_from_json(data.get("window"))

```

New text:

```
(empty)
```

### `u278.M12_no_over_the_line_in_call`

Gate.call: drop the --calls past the line refusal

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M12_no_over_the_line_in_call`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`
- Collected: 177 against a baseline of 177
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_calls_above_the_hours_budget_is_refused_before_any_call`

Old text:

```
                over = over_the_line(self.settings)
                if over is not None:
```

New text:

```
                over = over_the_line(self.settings)
                if False:
```

### `u278.M13_over_the_line_loosened`

over_the_line: let a --calls up to twice the hour's budget through

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M13_over_the_line_loosened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`
- Collected: 177 against a baseline of 177
- Kills: 3 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_calls_above_the_hours_budget_is_refused_before_any_call`
  - `tests/test_provider_budget.py::test_calls_past_the_budget_is_refused_before_the_verb_runs[refused-before-a-verb-that-makes-no-call-runs]`
  - `tests/test_provider_budget.py::test_calls_past_the_budget_is_refused_before_the_verb_runs[the-continue-a-parked-job-prints-is-not-refused-by-its-own-calls]`

Old text:

```
    if scope.raised <= budget:
```

New text:

```
    if scope.raised <= budget * 2:
```

### `u278.M14_hour_raise_ignored`

hourly: ignore the hour raised for this run

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M14_hour_raise_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`
- Collected: 177 against a baseline of 177
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_parked_jobs_continue_carries_the_hour_its_ceiling_needs`
  - `tests/test_provider_budget.py::test_the_hour_raised_for_one_run_lasts_that_run_and_reaches_a_child`

Old text:

```
    if scope is not None and scope.hourly is not None:
```

New text:

```
    if False:
```

### `u278.M15_hour_not_exported`

command: the raised hour never reaches a detached child

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M15_hour_not_exported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`
- Collected: 177 against a baseline of 177
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_the_hour_raised_for_one_run_lasts_that_run_and_reaches_a_child`

Old text:

```
_exported(BUDGET_ENV, calls_per_hour)
```

New text:

```
_exported(BUDGET_ENV, None)
```

### `u278.M16_nested_class_kept`

command: a nested dispatch keeps the outer class

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M16_nested_class_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`
- Collected: 177 against a baseline of 177
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_read_dispatched_inside_a_write_runs_under_the_read_line`
  - `tests/test_provider_budget.py::test_a_verb_dispatched_again_inside_a_scope_runs_under_its_own_class`

Old text:

```
        outer.reserve = outer.declared = bool(reserve)

```

New text:

```
(empty)
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

### `u278.M18_reading_noop`

reading: never narrow the command

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M18_reading_noop`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_label_sync.py`
- Collected: 271 against a baseline of 271
- Kills: 3 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_read_is_held_to_the_read_line[a-write-verb-running-a-read-mode]`
  - `tests/test_provider_budget.py::test_a_sweep_whose_estimate_crosses_into_the_reserve_refuses_before_its_first_call`
  - `tests/test_provider_budget.py::test_spending_never_reaches_past_the_class_the_verb_declared`

Old text:

```
    scope.reserve = False
    if settings is not None:
```

New text:

```
    if settings is not None:
```

### `u278.M2_future_minute_not_settled`

Gate.call: never write the settled window, so a minute stamped ahead slides with the clock and holds the line

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M2_future_minute_not_settled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`
- Collected: 177 against a baseline of 177
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer[account]`
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer[app-credentials]`

Old text:

```
                if state.settle(now):
                    try:
```

New text:

```
                if False:
                    try:
```

### `u278.M4_no_budget_check`

Gate.call: drop the hour's line, so a call past it is sent

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M4_no_budget_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_label_sync.py`
- Collected: 271 against a baseline of 271
- Kills: 17 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_call_at_the_line_is_not_sent_and_names_the_spend_and_when_it_frees`
  - `tests/test_provider_budget.py::test_a_cooldown_still_refuses_first_and_keeps_its_own_reason`
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer[account]`
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer[app-credentials]`
  - `tests/test_provider_budget.py::test_a_read_dispatched_inside_a_write_runs_under_the_read_line`
  - `tests/test_provider_budget.py::test_a_read_is_held_to_the_read_line[a-raised-ceiling-never-spends-the-reserve]`
  - `tests/test_provider_budget.py::test_a_read_is_held_to_the_read_line[a-write-verb-running-a-read-mode]`
  - `tests/test_provider_budget.py::test_a_read_is_held_to_the_read_line[calls-up-to-the-budget-on-a-read]`
  - `tests/test_provider_budget.py::test_a_read_stops_at_the_reserve_while_a_go_still_runs`
  - `tests/test_provider_budget.py::test_a_verb_dispatched_again_inside_a_scope_runs_under_its_own_class`
  - `tests/test_provider_budget.py::test_an_hour_raised_in_the_environment_reaches_a_call_outside_any_scope`
  - `tests/test_provider_budget.py::test_one_identity_at_its_line_leaves_the_other_open`
  - `tests/test_provider_budget.py::test_spending_never_reaches_past_the_class_the_verb_declared`
  - `tests/test_provider_budget.py::test_the_budget_counts_every_command_and_every_gate_on_the_file`
  - `tests/test_provider_budget.py::test_the_hour_raised_for_one_run_lasts_that_run_and_reaches_a_child`
  - ... and 2 more, see the JSON sidecar

Old text:

```
                if spent >= hour_line:
```

New text:

```
                if False:
```

### `u278.M5_budget_off_by_one`

Gate.call: let one call past the line

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M5_budget_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`
- Collected: 177 against a baseline of 177
- Kills: 16 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_call_at_the_line_is_not_sent_and_names_the_spend_and_when_it_frees`
  - `tests/test_provider_budget.py::test_a_cooldown_still_refuses_first_and_keeps_its_own_reason`
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer[account]`
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer[app-credentials]`
  - `tests/test_provider_budget.py::test_a_read_dispatched_inside_a_write_runs_under_the_read_line`
  - `tests/test_provider_budget.py::test_a_read_is_held_to_the_read_line[a-raised-ceiling-never-spends-the-reserve]`
  - `tests/test_provider_budget.py::test_a_read_is_held_to_the_read_line[a-write-verb-running-a-read-mode]`
  - `tests/test_provider_budget.py::test_a_read_is_held_to_the_read_line[calls-up-to-the-budget-on-a-read]`
  - `tests/test_provider_budget.py::test_a_read_stops_at_the_reserve_while_a_go_still_runs`
  - `tests/test_provider_budget.py::test_an_hour_raised_in_the_environment_reaches_a_call_outside_any_scope`
  - `tests/test_provider_budget.py::test_one_identity_at_its_line_leaves_the_other_open`
  - `tests/test_provider_budget.py::test_spending_never_reaches_past_the_class_the_verb_declared`
  - `tests/test_provider_budget.py::test_the_budget_counts_every_command_and_every_gate_on_the_file`
  - `tests/test_provider_budget.py::test_the_hour_raised_for_one_run_lasts_that_run_and_reaches_a_child`
  - `tests/test_provider_budget.py::test_the_window_frees_as_its_oldest_minute_ages_out`
  - ... and 1 more, see the JSON sidecar

Old text:

```
                if spent >= hour_line:
```

New text:

```
                if spent > hour_line:
```

### `u278.M6_count_not_written`

_send_now: stop counting calls in the window

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M6_count_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`
- Collected: 177 against a baseline of 177
- Kills: 25 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_call_at_the_line_is_not_sent_and_names_the_spend_and_when_it_frees`
  - `tests/test_provider_budget.py::test_a_call_made_under_a_redirected_state_directory_is_counted_by_the_live_gate`
  - `tests/test_provider_budget.py::test_a_cooldown_still_refuses_first_and_keeps_its_own_reason`
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer[account]`
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer[app-credentials]`
  - `tests/test_provider_budget.py::test_a_read_dispatched_inside_a_write_runs_under_the_read_line`
  - `tests/test_provider_budget.py::test_a_read_is_held_to_the_read_line[a-raised-ceiling-never-spends-the-reserve]`
  - `tests/test_provider_budget.py::test_a_read_is_held_to_the_read_line[a-write-verb-running-a-read-mode]`
  - `tests/test_provider_budget.py::test_a_read_is_held_to_the_read_line[calls-up-to-the-budget-on-a-read]`
  - `tests/test_provider_budget.py::test_a_read_stops_at_the_reserve_while_a_go_still_runs`
  - `tests/test_provider_budget.py::test_a_sweep_whose_estimate_crosses_into_the_reserve_refuses_before_its_first_call`
  - `tests/test_provider_budget.py::test_a_verb_dispatched_again_inside_a_scope_runs_under_its_own_class`
  - `tests/test_provider_budget.py::test_an_hour_raised_in_the_environment_reaches_a_call_outside_any_scope`
  - `tests/test_provider_budget.py::test_doctor_shows_each_identitys_spend_against_its_line_and_the_reserve`
  - `tests/test_provider_budget.py::test_minutes_older_than_the_window_are_pruned_from_the_file`
  - ... and 10 more, see the JSON sidecar

Old text:

```
        state.count(identity, now)

```

New text:

```
(empty)
```

### `u278.M7_identities_merged`

Gate.call: read the account's window for every identity

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M7_identities_merged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`
- Collected: 177 against a baseline of 177
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer[app-credentials]`
  - `tests/test_provider_budget.py::test_one_identity_at_its_line_leaves_the_other_open`

Old text:

```
                spent = state.spent(identity, now)
```

New text:

```
                spent = state.spent(ACCOUNT, now)
```

### `u278.M8_no_reserve`

line_for: a read reaches the whole budget

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M8_no_reserve`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_label_sync.py`
- Collected: 271 against a baseline of 271
- Kills: 23 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_call_at_the_line_is_not_sent_and_names_the_spend_and_when_it_frees`
  - `tests/test_provider_budget.py::test_a_cooldown_still_refuses_first_and_keeps_its_own_reason`
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer[account]`
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer[app-credentials]`
  - `tests/test_provider_budget.py::test_a_read_dispatched_inside_a_write_runs_under_the_read_line`
  - `tests/test_provider_budget.py::test_a_read_is_held_to_the_read_line[a-raised-ceiling-never-spends-the-reserve]`
  - `tests/test_provider_budget.py::test_a_read_is_held_to_the_read_line[a-write-verb-running-a-read-mode]`
  - `tests/test_provider_budget.py::test_a_read_is_held_to_the_read_line[calls-up-to-the-budget-on-a-read]`
  - `tests/test_provider_budget.py::test_a_read_stops_at_the_reserve_while_a_go_still_runs`
  - `tests/test_provider_budget.py::test_a_sweep_whose_estimate_crosses_into_the_reserve_refuses_before_its_first_call`
  - `tests/test_provider_budget.py::test_a_verb_dispatched_again_inside_a_scope_runs_under_its_own_class`
  - `tests/test_provider_budget.py::test_an_hour_raised_in_the_environment_reaches_a_call_outside_any_scope`
  - `tests/test_provider_budget.py::test_doctor_names_an_identity_at_its_read_line_and_when_it_frees`
  - `tests/test_provider_budget.py::test_doctor_shows_each_identitys_spend_against_its_line_and_the_reserve`
  - `tests/test_provider_budget.py::test_one_identity_at_its_line_leaves_the_other_open`
  - ... and 8 more, see the JSON sidecar

Old text:

```
    return budget - reserve_of(budget, settings.reserve_share)
```

New text:

```
    return budget
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

### `u293.G1_night_line_asked`

Gate.call: never ask the night's line, so a night pass spends past its budget

- File: `src/cratekit/core/provider_gate.py`
- Source: `u293.json`, row `G1_night_line_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_provider_gate.py`, `tests/test_provider_budget.py`, `tests/test_sync_night.py`
- Collected: 280 against a baseline of 280
- Kills: 6 (killed)
- Killed:
  - `tests/test_provider_gate_night.py::test_a_total_below_the_mark_is_a_spend_nobody_can_read_and_stops`
  - `tests/test_provider_gate_night.py::test_an_inherited_night_line_stops_a_child_at_the_nights_remainder`
  - `tests/test_provider_gate_night.py::test_another_processs_calls_count_against_the_night`
  - `tests/test_provider_gate_night.py::test_outside_any_command_a_line_off_the_environment_holds_the_call`
  - `tests/test_provider_gate_night.py::test_the_call_past_the_nights_line_is_never_sent_and_parks_naming_the_night`
  - `tests/test_provider_gate_night.py::test_the_nights_line_is_held_to_what_is_left_of_the_command_ceiling`

Old text:

```
                if held_night is not None and (
```

New text:

```
                if False and (
```

### `u293.G2_night_line_off_by_one`

Gate.call: stop only past the line, so one call beyond the night's budget is sent

- File: `src/cratekit/core/provider_gate.py`
- Source: `u293.json`, row `G2_night_line_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_provider_gate.py`, `tests/test_provider_budget.py`, `tests/test_sync_night.py`
- Collected: 280 against a baseline of 280
- Kills: 5 (killed)
- Killed:
  - `tests/test_provider_gate_night.py::test_an_inherited_night_line_stops_a_child_at_the_nights_remainder`
  - `tests/test_provider_gate_night.py::test_another_processs_calls_count_against_the_night`
  - `tests/test_provider_gate_night.py::test_outside_any_command_a_line_off_the_environment_holds_the_call`
  - `tests/test_provider_gate_night.py::test_the_call_past_the_nights_line_is_never_sent_and_parks_naming_the_night`
  - `tests/test_provider_gate_night.py::test_the_nights_line_is_held_to_what_is_left_of_the_command_ceiling`

Old text:

```
                    state.calls - held_night.start >= held_night.budget
```

New text:

```
                    state.calls - held_night.start > held_night.budget
```

### `u293.G3_total_below_mark`

Gate.call: a total below the night's mark reads as nothing spent rather than stopping

- File: `src/cratekit/core/provider_gate.py`
- Source: `u293.json`, row `G3_total_below_mark`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_provider_gate.py`, `tests/test_provider_budget.py`, `tests/test_sync_night.py`
- Collected: 280 against a baseline of 280
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate_night.py::test_a_total_below_the_mark_is_a_spend_nobody_can_read_and_stops`

Old text:

```
                    or state.calls < held_night.start
```

New text:

```
                    or False
```

### `u293.G4_child_reads_no_line`

command: a scope opened in a child reads no night line off the environment

- File: `src/cratekit/core/provider_gate.py`
- Source: `u293.json`, row `G4_child_reads_no_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_provider_gate.py`, `tests/test_provider_budget.py`, `tests/test_sync_night.py`
- Collected: 280 against a baseline of 280
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_gate_night.py::test_a_line_read_off_the_environment_is_held_beside_the_ceiling`
  - `tests/test_provider_gate_night.py::test_an_inherited_night_line_stops_a_child_at_the_nights_remainder`

Old text:

```
        night=_night_from_env(),
```

New text:

```
        night=None,
```

### `u293.G5_line_held_to_ceiling`

night: the firing's line is the night's remainder alone, past one command's ceiling

- File: `src/cratekit/core/provider_gate.py`
- Source: `u293.json`, row `G5_line_held_to_ceiling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_provider_gate.py`, `tests/test_provider_budget.py`, `tests/test_sync_night.py`
- Collected: 280 against a baseline of 280
- Kills: 5 (killed)
- Killed:
  - `tests/test_provider_gate_night.py::test_a_ceiling_raised_through_the_environment_never_widens_a_firing`
  - `tests/test_provider_gate_night.py::test_the_line_is_held_to_what_the_command_has_left_of_its_ceiling`
  - `tests/test_provider_gate_night.py::test_the_nights_line_is_held_to_what_is_left_of_the_command_ceiling`
  - `tests/test_sync_night.py::test_a_firing_that_died_is_charged_to_the_next_of_the_same_night`
  - `tests/test_sync_night.py::test_the_pass_runs_under_the_nights_line_and_hour`

Old text:

```
budget=max(0, min(int(calls), left_of_ceiling))
```

New text:

```
budget=max(0, int(calls))
```

### `u293.G6_nested_lower_line`

night: a nested line widens the outer night's remainder

- File: `src/cratekit/core/provider_gate.py`
- Source: `u293.json`, row `G6_nested_lower_line`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_provider_gate.py`, `tests/test_provider_budget.py`, `tests/test_sync_night.py`
- Collected: 280 against a baseline of 280
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate_night.py::test_a_nested_night_keeps_the_lower_line`

Old text:

```
        if left < held.budget:
```

New text:

```
        if False:
```

### `u293.G7_hour_never_raised`

night: the night's hour replaces the configured one, raising it when set higher

- File: `src/cratekit/core/provider_gate.py`
- Source: `u293.json`, row `G7_hour_never_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_provider_gate.py`, `tests/test_provider_budget.py`, `tests/test_sync_night.py`
- Collected: 280 against a baseline of 280
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate_night.py::test_the_night_lowers_the_hour_and_never_raises_it`

Old text:

```
    hour = min(hourly(settings), max(1, int(calls_per_hour)))
```

New text:

```
    hour = max(1, int(calls_per_hour))
```

### `u293.G8_line_exported`

night: the line is not exported, so a detached child runs without it

- File: `src/cratekit/core/provider_gate.py`
- Source: `u293.json`, row `G8_line_exported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_provider_gate.py`, `tests/test_provider_budget.py`, `tests/test_sync_night.py`
- Collected: 280 against a baseline of 280
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_gate_night.py::test_the_line_reaches_a_child_through_the_environment_and_is_put_back`
  - `tests/test_sync_night.py::test_the_pass_runs_under_the_nights_line_and_hour`

Old text:

```
        with _exported(NIGHT_ENV, held.to_env()), _exported(BUDGET_ENV, hour):
```

New text:

```
        with _exported(NIGHT_ENV, None), _exported(BUDGET_ENV, hour):
```

### `r431-a.A6_a_standing_companion_is_rewritten`

beside overwrites a companion that already stands, so a second guest's deletion restamps the shared one

- File: `src/cratekit/core/review.py`
- Source: `r431-a.json`, row `A6_a_standing_companion_is_rewritten`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair.py`, `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/modules/test_reports.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_adoption.py`, `tests/test_deletion.py`, `tests/test_genre_retag.py`, `tests/test_intake_missing_search.py`, `tests/test_label_approved.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_match_states.py`, `tests/test_reports_cli.py`, `tests/test_review_queue.py`, `tests/test_tag_workers.py`, `tests/test_tombstones.py`, `tests/test_uncredited_tombstone.py`
- Collected: 3057 against a baseline of 3057
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
- Collected: 3057 against a baseline of 3057
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
- Collected: 3057 against a baseline of 3057
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
- Collected: 3057 against a baseline of 3057
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

### `r679-a.A1_supersede_guard_both_layers`

supersede: drop the empty column condition from the read and the write together, so a person's verdict is overwritten

- File: `src/cratekit/core/review.py`
- Source: `r679-a.json`, row `A1_supersede_guard_both_layers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_review_queue.py`, `tests/test_match_states.py`, `tests/intake/test_workers.py`
- Collected: 870 against a baseline of 870
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
- Collected: 870 against a baseline of 870
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
- Collected: 870 against a baseline of 870
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

- File: `src/cratekit/core/review_exchange.py`
- Source: `r679-a.json`, row `A5_import_routes_through_resolve`
- Moved: the same text, now in src/cratekit/core/review_exchange.py, was in src/cratekit/core/review.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_review_queue.py`, `tests/test_match_states.py`, `tests/intake/test_workers.py`
- Collected: 870 against a baseline of 870
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
- Collected: 870 against a baseline of 870
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
- Collected: 870 against a baseline of 870
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
- Collected: 870 against a baseline of 870
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

### `r790-d.R1_grouping_kinds`

grouped: count every kind in the queue, harvested label names included

- File: `src/cratekit/core/review_groups.py`
- Source: `r790-d.json`, row `R1_grouping_kinds`
- Moved: the same text, now in src/cratekit/core/review_groups.py, was in src/cratekit/core/review.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`, `tests/test_review_queue.py`
- Collected: 192 against a baseline of 192
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_harvested_label_name_is_not_counted_as_a_label_release`

Old text:

```
    kinds = kinds or GROUPED_KINDS.get(declared)
```

New text:

```
    kinds = kinds
```

### `r790-d.R2_label_beyond`

grouped by label: report no recorded beyond

- File: `src/cratekit/core/review_groups.py`
- Source: `r790-d.json`, row `R2_label_beyond`
- Moved: the same text, now in src/cratekit/core/review_groups.py, was in src/cratekit/core/review.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`, `tests/test_review_queue.py`
- Collected: 192 against a baseline of 192
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_first_sweep_files_the_default_ten_and_counts_the_other_forty`
  - `tests/test_label_offer_window.py::test_a_label_whose_offer_is_raised_to_thirty_files_thirty`
  - `tests/test_label_offer_window.py::test_a_round_records_the_most_the_label_could_still_offer`
  - `tests/test_label_offer_window.py::test_a_run_over_two_labels_counts_what_both_left_beyond`
  - `tests/test_label_offer_window.py::test_a_second_sweep_files_only_the_new_release_and_refiles_nothing`
  - `tests/test_label_offer_window.py::test_a_track_limit_below_the_offer_bounds_it_and_the_rest_is_still_counted`
  - `tests/test_label_offer_window.py::test_the_configured_offer_is_the_default_for_every_label`

Old text:

```
                "beyond": latest[key].beyond if key in latest else None,
```

New text:

```
                "beyond": None,
```

### `r798-c.H2_only_a_hold_in_force_is_dropped`

review.release_hold: drop a hold in any state, so the record that a person returned a release is lost and it can be held again

- File: `src/cratekit/core/review_holds.py`
- Source: `r798-c.json`, row `H2_only_a_hold_in_force_is_dropped`
- Moved: the same text, now in src/cratekit/core/review_holds.py, was in src/cratekit/core/review.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`, `tests/test_review_queue.py`, `tests/test_label_offer_window.py`, `tests/test_label_approved.py`
- Collected: 387 against a baseline of 387
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_releasing_drops_a_hold_in_force_and_keeps_a_returned_one`

Old text:

```
            "DELETE FROM held_offers WHERE queue = ? AND item_id = ? AND state = ?",
            (_assert_declared_queue(queue), item_id, HOLD_HELD),
```

New text:

```
            "DELETE FROM held_offers WHERE queue = ? AND item_id = ?",
            (_assert_declared_queue(queue), item_id),
```

### `r815-a.W1_withhold_only_an_open_item`

withhold: move an item whatever its verdict column says

- File: `src/cratekit/core/review_holds.py`
- Source: `r815-a.json`, row `W1_withhold_only_an_open_item`
- Moved: the same text, now in src/cratekit/core/review_holds.py, was in src/cratekit/core/review.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`, `tests/test_label_genre_gate.py`
- Collected: 214 against a baseline of 214
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_decided_item_is_not_withheld_and_stays_exactly_as_it_was[accepted]`
  - `tests/test_label_judge.py::test_a_decided_item_is_not_withheld_and_stays_exactly_as_it_was[rejected]`
  - `tests/test_label_judge.py::test_a_release_decided_while_it_was_being_judged_is_not_held`
  - `tests/test_label_judge.py::test_a_superseded_item_is_not_withheld`
  - `tests/test_label_judge.py::test_an_item_carrying_a_verdict_this_build_cannot_read_is_not_withheld`

Old text:

```
        if row is None or row["verdict"] is not None:
            return None
        queue = row["queue"]
```

New text:

```
        if row is None:
            return None
        queue = row["queue"]
```

### `r815-a.W2_a_returned_hold_is_not_withheld`

withhold: take back a release a person returned

- File: `src/cratekit/core/review_holds.py`
- Source: `r815-a.json`, row `W2_a_returned_hold_is_not_withheld`
- Moved: the same text, now in src/cratekit/core/review_holds.py, was in src/cratekit/core/review.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`, `tests/test_label_genre_gate.py`
- Collected: 214 against a baseline of 214
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_release_a_person_returned_is_never_withheld_again`

Old text:

```
        if standing is not None and standing["state"] == HOLD_RETURNED:
            return None
        try:
```

New text:

```
        if False:
            return None
        try:
```

### `r815-a.W3_the_floor_is_never_lowered`

withhold: let a lower ordinal replace the floor

- File: `src/cratekit/core/review_holds.py`
- Source: `r815-a.json`, row `W3_the_floor_is_never_lowered`
- Moved: the same text, now in src/cratekit/core/review_holds.py, was in src/cratekit/core/review.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`, `tests/test_label_genre_gate.py`
- Collected: 214 against a baseline of 214
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_judge.py::test_the_floor_is_raised_and_never_lowered`

Old text:

```
"ON CONFLICT(id) DO UPDATE SET ordinal = MAX(ordinal, excluded.ordinal)",
```

New text:

```
"ON CONFLICT(id) DO UPDATE SET ordinal = excluded.ordinal",
```

### `r815-a.W4_the_next_ordinal_is_past_the_floor`

_NEXT_ORDINAL: allocate one past the highest item alone, as before

- File: `src/cratekit/core/review.py`
- Source: `r815-a.json`, row `W4_the_next_ordinal_is_past_the_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`, `tests/test_label_genre_gate.py`, `tests/test_review_queue.py`
- Collected: 367 against a baseline of 367
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_judge.py::test_an_ordinal_a_withheld_item_held_is_never_given_to_a_later_one`
  - `tests/test_label_judge.py::test_the_floor_is_raised_and_never_lowered`

Old text:

```
    "(SELECT MAX(COALESCE((SELECT MAX(ordinal) FROM review_items), 0), "
    "COALESCE((SELECT MAX(ordinal) FROM ordinal_floor), 0)) + 1)"
```

New text:

```
    "(SELECT COALESCE((SELECT MAX(ordinal) FROM review_items), 0) + 1)"
```

### `r815-a.W5_a_refresh_keeps_the_withheld_word`

_CARRIED_ACROSS_A_REFRESH: carry the filing run and drop the withheld word

- File: `src/cratekit/core/review_holds.py`
- Source: `r815-a.json`, row `W5_a_refresh_keeps_the_withheld_word`
- Moved: the same text, now in src/cratekit/core/review_holds.py, was in src/cratekit/core/review.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`, `tests/test_label_genre_gate.py`
- Collected: 214 against a baseline of 214
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_refreshed_hold_keeps_the_run_its_release_was_filed_under`

Old text:

```
_CARRIED_ACROSS_A_REFRESH: tuple[str, ...] = (RUN_FIELD, WITHHELD_FIELD)
```

New text:

```
_CARRIED_ACROSS_A_REFRESH: tuple[str, ...] = (RUN_FIELD,)
```

### `r815-a.W6_redescribe_only_an_open_item`

redescribe: rewrite an item whatever its verdict column says

- File: `src/cratekit/core/review.py`
- Source: `r815-a.json`, row `W6_redescribe_only_an_open_item`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`, `tests/test_label_genre_gate.py`
- Collected: 214 against a baseline of 214
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_judge.py::test_redescribing_a_decided_item_changes_nothing`
  - `tests/test_label_judge.py::test_redescribing_an_item_with_an_unreadable_verdict_changes_nothing`

Old text:

```
            "UPDATE review_items SET payload = ?, updated = ? "
            "WHERE item_id = ? AND verdict IS NULL",
```

New text:

```
            "UPDATE review_items SET payload = ?, updated = ? "
            "WHERE item_id = ?",
```

### `r840-c.C1_the_function_is_handed_the_payload_as_it_stands`

review.redescribe: hand the function an empty payload and not the stored one, so a caller changing one field writes that field alone

- File: `src/cratekit/core/review.py`
- Source: `r840-c.json`, row `C1_the_function_is_handed_the_payload_as_it_stands`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`, `tests/test_label_judge.py`
- Collected: 137 against a baseline of 137
- Kills: 34 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_person_reads_each_release_without_asking_for_json`
  - `tests/test_label_artists.py::test_a_rewrite_given_a_function_is_handed_the_payload_and_writes_what_it_returns`
  - `tests/test_label_artists.py::test_a_second_run_asks_about_nothing_the_first_repaired`
  - `tests/test_label_artists.py::test_an_answer_between_failures_keeps_the_run_going`
  - `tests/test_label_artists.py::test_an_imported_item_is_read_by_the_identifier_its_payload_carries`
  - `tests/test_label_artists.py::test_an_open_item_reading_an_address_is_given_the_name_and_nothing_else_moves`
  - `tests/test_label_artists.py::test_the_counts_always_sum_to_the_addresses_and_the_items_left_alone`
  - `tests/test_label_artists.py::test_the_provider_is_asked_once_for_each_repaired_item_and_never_for_the_others`
  - `tests/test_label_artists.py::test_the_seams_own_refusal_stops_the_run_and_carries_what_was_repaired`
  - `tests/test_label_artists.py::test_two_items_naming_one_release_are_two_lines_under_two_keys`
  - `tests/test_label_artists.py::test_what_a_judging_job_stamped_meanwhile_is_kept`
  - `tests/test_label_judge.py::test_a_catalogue_that_refuses_stops_the_run_at_once_and_says_how_many_were_left`
  - `tests/test_label_judge.py::test_a_catalogue_unread_three_times_in_a_row_stops_the_run_and_says_how_many_were_left`
  - `tests/test_label_judge.py::test_a_fresh_answer_with_no_word_takes_the_old_words_off_the_item`
  - `tests/test_label_judge.py::test_a_label_marked_any_has_nothing_held_and_nobody_is_asked`
  - ... and 19 more, see the JSON sidecar

Old text:

```
            wanted = payload(_payload_of(held["payload"]))
```

New text:

```
            wanted = payload({})
```

### `r840-c.C2_the_function_is_only_handed_an_open_item`

review.redescribe: read the payload of any item, so the function is called for one that is decided or carries a verdict this build cannot read

- File: `src/cratekit/core/review.py`
- Source: `r840-c.json`, row `C2_the_function_is_only_handed_an_open_item`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`, `tests/test_label_judge.py`
- Collected: 137 against a baseline of 137
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_release_decided_while_it_was_being_read_is_not_rewritten`
  - `tests/test_label_artists.py::test_a_rewrite_is_not_handed_the_payload_of_a_decided_item[accepted]`
  - `tests/test_label_artists.py::test_a_rewrite_is_not_handed_the_payload_of_a_decided_item[rejected]`
  - `tests/test_label_artists.py::test_a_rewrite_is_not_handed_the_payload_of_an_item_with_an_unreadable_verdict`

Old text:

```
                "SELECT payload FROM review_items WHERE item_id = ? AND verdict IS NULL",
                (item_id,),
            ).fetchone()
            if held is None:
                return None
            wanted = payload(
```

New text:

```
                "SELECT payload FROM review_items WHERE item_id = ?",
                (item_id,),
            ).fetchone()
            if held is None:
                return None
            wanted = payload(
```

### `r650-a.A1_tier_five_sets_nothing`

The last tier stops flagging its pass through, which is the state before this unit

- File: `src/cratekit/core/routing.py`
- Source: `r650-a.json`, row `A1_tier_five_sets_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_catalogue_searcher.py`, `tests/test_deferred_routing.py`, `tests/test_genre_retag.py`, `tests/test_rebuild.py`, `tests/test_routing_parity.py`, `tests/test_tag_workers.py`, `tests/test_taxonomy.py`
- Collected: 1562 against a baseline of 1562
- Kills: 6 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_source_genre_nothing_in_the_table_knows_is_written_and_flagged`
  - `tests/test_catalogue_searcher.py::test_an_unknown_source_genre_a_taxonomy_calls_too_coarse_is_a_plain_decline`
  - `tests/test_routing_parity.py::test_a_declared_tag_with_no_bucket_is_not_off_taxonomy`
  - `tests/test_routing_parity.py::test_tagging_never_falls_back_to_a_bucket`
  - `tests/test_taxonomy.py::test_a_sub_display_and_a_changed_case_are_both_reported`
  - `tests/test_taxonomy.py::test_an_off_taxonomy_word_can_still_route_to_a_real_bucket`

Old text:

```
    return Suggestion(tag=value, off_taxonomy=taxonomy.bucket_for_display(value) is None)
```

New text:

```
    return Suggestion(tag=value)
```

### `r650-a.A2_tier_five_flags_everything`

The last tier flags a bucket's own display, which routing places where the template says

- File: `src/cratekit/core/routing.py`
- Source: `r650-a.json`, row `A2_tier_five_flags_everything`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_catalogue_searcher.py`, `tests/test_deferred_routing.py`, `tests/test_genre_retag.py`, `tests/test_rebuild.py`, `tests/test_routing_parity.py`, `tests/test_tag_workers.py`, `tests/test_taxonomy.py`
- Collected: 1562 against a baseline of 1562
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_the_correction_verb_cannot_write_a_genre_off_the_declared_taxonomy`
  - `tests/test_taxonomy.py::test_a_buckets_own_display_name_is_never_reported_off_taxonomy`

Old text:

```
    return Suggestion(tag=value, off_taxonomy=taxonomy.bucket_for_display(value) is None)
```

New text:

```
    return Suggestion(tag=value, off_taxonomy=True)
```

### `r650-a.A3_suppression_widens_to_the_vocabulary`

The review's first shape: suppress on any declared display, so a sub display and a changed case go unreported

- File: `src/cratekit/core/routing.py`
- Source: `r650-a.json`, row `A3_suppression_widens_to_the_vocabulary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_catalogue_searcher.py`, `tests/test_deferred_routing.py`, `tests/test_genre_retag.py`, `tests/test_rebuild.py`, `tests/test_routing_parity.py`, `tests/test_tag_workers.py`, `tests/test_taxonomy.py`
- Collected: 1562 against a baseline of 1562
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy.py::test_a_sub_display_and_a_changed_case_are_both_reported`

Old text:

```
    return Suggestion(tag=value, off_taxonomy=taxonomy.bucket_for_display(value) is None)
```

New text:

```
    declared = {b.display for b in taxonomy.buckets} | {
        sub.display for b in taxonomy.buckets for sub in b.subs
    }
    return Suggestion(tag=value, off_taxonomy=value not in declared)
```

### `r650-a.A4_suppression_ignores_case`

Suppress case insensitively, so a lowercased Bandcamp tag routing leaves in the catch-all reads as declared

- File: `src/cratekit/core/routing.py`
- Source: `r650-a.json`, row `A4_suppression_ignores_case`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_catalogue_searcher.py`, `tests/test_deferred_routing.py`, `tests/test_genre_retag.py`, `tests/test_rebuild.py`, `tests/test_routing_parity.py`, `tests/test_tag_workers.py`, `tests/test_taxonomy.py`
- Collected: 1562 against a baseline of 1562
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy.py::test_a_sub_display_and_a_changed_case_are_both_reported`

Old text:

```
    return Suggestion(tag=value, off_taxonomy=taxonomy.bucket_for_display(value) is None)
```

New text:

```
    lowered_displays = {b.display.lower() for b in taxonomy.buckets}
    return Suggestion(tag=value, off_taxonomy=lowered not in lowered_displays)
```

### `r650-a.A6_declared_literal_rule_flagged`

A declared rule carrying a literal tag and no bucket is reported as off taxonomy too

- File: `src/cratekit/core/routing.py`
- Source: `r650-a.json`, row `A6_declared_literal_rule_flagged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_catalogue_searcher.py`, `tests/test_deferred_routing.py`, `tests/test_genre_retag.py`, `tests/test_rebuild.py`, `tests/test_routing_parity.py`, `tests/test_tag_workers.py`, `tests/test_taxonomy.py`
- Collected: 1460 against a baseline of 1562
- Kills: 3 (collect-error)
- Note: collection changed: 1460 collected against a baseline of 1562. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_declared_tag_with_no_bucket_reaches_the_file_without_the_flag`
  - `tests/test_routing_parity.py::test_a_declared_tag_with_no_bucket_is_not_off_taxonomy`
  - `tests/test_routing_parity.py::test_only_the_last_tier_is_off_taxonomy`
- Collection errors: `tests/test_tag_workers.py`, `tests/test_tag_workers.py`, `tests/test_tag_workers.py`, `tests/test_tag_workers.py`

Old text:

```
    return Suggestion(tag=rule.tag)
```

New text:

```
    return Suggestion(tag=rule.tag, off_taxonomy=True)
```

### `r731-b.M21_sink_does_not_compete`

the no reading sub no longer competes with a band

- File: `src/cratekit/core/routing.py`
- Source: `r731-b.json`, row `M21_sink_does_not_compete`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_placements.py`, `tests/test_adopt_workers.py`
- Collected: 95 against a baseline of 95
- Kills: 11 (killed)
- Killed:
  - `tests/test_adopt_placements.py::test_a_sub_class_is_removed_from_the_bands_by_identifier`
  - `tests/test_adopt_placements.py::test_a_track_in_a_band_whose_file_has_no_reading_is_withheld_from_the_sink`
  - `tests/test_adopt_placements.py::test_a_track_in_the_no_reading_sub_whose_file_now_reads_is_withheld`
  - `tests/test_adopt_placements.py::test_every_sub_routing_can_name_is_one_of_its_buckets_competing_subs`
  - `tests/test_adopt_placements.py::test_the_bands_and_the_no_reading_sub_compete_in_an_energy_bucket`
  - `tests/test_adopt_workers.py::test_a_second_approved_apply_adds_nothing_and_withholds_the_same`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`
  - `tests/test_adopt_workers.py::test_an_approved_apply_leaves_a_withheld_track_where_it_sat`
  - `tests/test_adopt_workers.py::test_the_gate_counts_the_withheld_by_kind_and_lists_every_one`
  - `tests/test_adopt_workers.py::test_the_gate_names_the_vocal_count_and_lists_every_membership`
  - `tests/test_adopt_workers.py::test_the_plan_reads_the_tree_the_census_database_holds`

Old text:

```
    if taxonomy.energy.no_energy_sub is not None:
        found.add(taxonomy.energy.no_energy_sub.id)
    return Competing.BAND
```

New text:

```
    return Competing.BAND
```

### `r731-b.M22_single_sub_does_not_compete`

a bucket's single sub is left out of its competing subs

- File: `src/cratekit/core/routing.py`
- Source: `r731-b.json`, row `M22_single_sub_does_not_compete`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_placements.py`, `tests/test_adopt_workers.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_placements.py::test_every_sub_routing_can_name_is_one_of_its_buckets_competing_subs`

Old text:

```
        if bucket.single_sub is not None:
            found.add(bucket.single_sub.id)
        return Competing.STYLE
```

New text:

```
        return Competing.STYLE
```

### `r797-a.T7_competes_in_a_style_bucket`

competing_subs: leave former places out of a bucket split by style, so the folder holding the old playlist no longer sees it

- File: `src/cratekit/core/routing.py`
- Source: `r797-a.json`, row `T7_competes_in_a_style_bucket`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_placements.py`, `tests/test_routing_parity.py`
- Collected: 1063 against a baseline of 1063
- Kills: 13 (killed)
- Killed:
  - `tests/test_adopt_former_place.py::test_a_former_place_competes_where_it_is_declared_and_where_it_sits_and_nowhere_else`
  - `tests/test_adopt_former_place.py::test_a_former_place_held_twice_is_not_listed_beside_the_move_that_leaves_it`
  - `tests/test_adopt_former_place.py::test_a_place_the_holding_bucket_settles_is_not_asked_about_in_the_declaring_one[another-band]`
  - `tests/test_adopt_former_place.py::test_a_place_the_holding_bucket_settles_is_not_asked_about_in_the_declaring_one[its-reading]`
  - `tests/test_adopt_former_place.py::test_a_renamed_old_playlist_is_found_through_the_node_recorded_under_the_old_sub`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_holds_the_former_place_in_both_buckets`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_whose_genre_names_another_style_moves_to_that_style`
  - `tests/test_adopt_former_place.py::test_a_track_whose_genre_lands_in_the_old_folders_default_is_withheld_and_left`
  - `tests/test_adopt_former_place.py::test_adoption_over_the_same_library_files_none_of_them_a_second_time`
  - `tests/test_adopt_former_place.py::test_an_approved_move_files_each_track_in_its_band_and_none_is_left_in_both`
  - `tests/test_adopt_former_place.py::test_the_gate_shows_every_track_leaving_the_old_playlist_and_every_one_left`
  - `tests/test_adopt_former_place.py::test_the_writer_is_told_to_leave_the_old_playlist_by_its_own_names`
  - `tests/test_adopt_placements.py::test_the_style_subs_compete_where_a_bucket_has_no_energy_dimension`

Old text:

```
        return Competing.STYLE, frozenset((found | former) - classes)
```

New text:

```
        return Competing.STYLE, frozenset(found - classes)
```

### `r797-a.T8_competes_in_a_band_bucket`

competing_subs: leave former places out of a bucket split by energy, so adoption files a band beside the old playlist

- File: `src/cratekit/core/routing.py`
- Source: `r797-a.json`, row `T8_competes_in_a_band_bucket`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_placements.py`, `tests/test_routing_parity.py`
- Collected: 1063 against a baseline of 1063
- Kills: 30 (killed)
- Killed:
  - `tests/test_adopt_former_place.py::test_a_file_the_census_could_not_read_is_listed_under_no_reading`
  - `tests/test_adopt_former_place.py::test_a_former_place_competes_where_it_is_declared_and_where_it_sits_and_nowhere_else`
  - `tests/test_adopt_former_place.py::test_a_genre_only_the_fallback_tier_lands_is_not_read_as_naming_the_bucket`
  - `tests/test_adopt_former_place.py::test_a_genre_that_left_the_promoted_bucket_since_the_approval_is_a_stale_decision[Afrobeat]`
  - `tests/test_adopt_former_place.py::test_a_genre_that_left_the_promoted_bucket_since_the_approval_is_a_stale_decision[Deep House]`
  - `tests/test_adopt_former_place.py::test_a_genre_that_left_the_promoted_bucket_since_the_approval_is_a_stale_decision[]`
  - `tests/test_adopt_former_place.py::test_a_move_whose_target_is_a_former_place_is_refused_and_nothing_is_written`
  - `tests/test_adopt_former_place.py::test_a_renamed_old_playlist_is_found_through_the_node_recorded_under_the_old_sub`
  - `tests/test_adopt_former_place.py::test_a_second_run_after_the_move_plans_nothing_and_writes_nothing`
  - `tests/test_adopt_former_place.py::test_a_track_a_verdict_withheld_is_listed_under_the_verdict`
  - `tests/test_adopt_former_place.py::test_a_track_already_in_its_band_only_leaves_the_old_playlist`
  - `tests/test_adopt_former_place.py::test_a_track_held_in_a_renamed_old_playlist_is_left_since_the_writer_cannot_see_it`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_and_a_stale_band_leaves_both`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_holds_the_former_place_in_both_buckets`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_is_added_to_its_band_and_leaves_the_playlist`
  - ... and 15 more, see the JSON sidecar

Old text:

```
    return Competing.BAND, frozenset((found | former) - classes)
```

New text:

```
    return Competing.BAND, frozenset(found - classes)
```

### `r797-c.G6_the_fallback_is_no_folder`

folder_of: read the fallback tier as a folder, so a genre nothing claims is never counted

- File: `src/cratekit/core/routing.py`
- Source: `r797-c.json`, row `G6_the_fallback_is_no_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_report_genres.py`
- Collected: 30 against a baseline of 30
- Kills: 11 (killed)
- Killed:
  - `tests/test_report_genres.py::test_a_genre_at_49_is_counted_and_not_named_and_one_at_50_is_named`
  - `tests/test_report_genres.py::test_a_genre_no_folder_claims_at_all_is_counted_under_its_own_word`
  - `tests/test_report_genres.py::test_a_style_sub_nothing_routes_a_lowercase_spelling_to_is_still_its_genre`
  - `tests/test_report_genres.py::test_a_word_nothing_declared_claims_has_no_folder_at_all`
  - `tests/test_report_genres.py::test_ae8_the_verb_names_the_genre_with_its_count_and_the_library_is_unchanged`
  - `tests/test_report_genres.py::test_another_spelling_of_a_source_string_is_counted_with_its_sub`
  - `tests/test_report_genres.py::test_every_live_track_is_counted_exactly_once`
  - `tests/test_report_genres.py::test_the_boundary_is_the_same_on_both_sides_of_one_genre`
  - `tests/test_report_genres.py::test_the_order_is_largest_first_then_by_name`
  - `tests/test_report_genres.py::test_two_spellings_of_one_unclaimed_word_are_one_genre`
  - `tests/test_report_genres.py::test_with_nothing_at_the_threshold_the_report_says_so_in_a_row`

Old text:

```
    if resolution.match is Match.FALLBACK:
```

New text:

```
    if False:
```

### `r797-c.G7_a_folders_own_name_has_that_folder`

folder_of: count a track tagged with the source routed folder's own name as a word in its default sub

- File: `src/cratekit/core/routing.py`
- Source: `r797-c.json`, row `G7_a_folders_own_name_has_that_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_report_genres.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_report_genres.py::test_the_source_routed_folders_own_name_has_that_folder`

Old text:

```
    if by_source is None or resolution.match is Match.PASSTHROUGH:
```

New text:

```
    if by_source is None:
```

### `r797-c.G8_a_map_row_is_a_style_sub`

folder_of: read every source string of a source routed folder as landing in its default

- File: `src/cratekit/core/routing.py`
- Source: `r797-c.json`, row `G8_a_map_row_is_a_style_sub`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_report_genres.py`
- Collected: 30 against a baseline of 30
- Kills: 3 (killed)
- Killed:
  - `tests/test_report_genres.py::test_a_genre_filed_whole_in_its_sub_names_no_other_spelling`
  - `tests/test_report_genres.py::test_a_source_string_filed_in_a_style_sub_has_no_folder_of_its_own`
  - `tests/test_report_genres.py::test_another_spelling_of_a_style_subs_own_name_is_counted_with_it`

Old text:

```
    if value in by_source.map:
```

New text:

```
    if False:
```

### `r798-a.K1_the_first_rule_that_matches_wins`

published_kind: read the published rules last first, so a word two rules could claim is given the later one's kind

- File: `src/cratekit/core/routing.py`
- Source: `r798-a.json`, row `K1_the_first_rule_that_matches_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`, `tests/test_taxonomy.py`, `tests/test_routing_parity.py`
- Collected: 1115 against a baseline of 1115
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_every_measured_word_of_the_general_catalogue_is_a_kind`
  - `tests/test_label_genre_gate.py::test_the_first_rule_that_matches_wins`
  - `tests/test_label_genre_gate.py::test_the_long_spelling_of_rnb_is_rnb_and_not_the_blues_it_contains`

Old text:

```
    for rule in taxonomy.label_gate.published:
```

New text:

```
    for rule in reversed(taxonomy.label_gate.published):
```

### `r798-a.K2_one_word_of_the_labels_kind_passes`

kind_verdict: pass only when every known word is the label's kind, so a crossover album listing a dance word beside a pop one is held

- File: `src/cratekit/core/routing.py`
- Source: `r798-a.json`, row `K2_one_word_of_the_labels_kind_passes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`, `tests/test_taxonomy.py`, `tests/test_routing_parity.py`
- Collected: 1115 against a baseline of 1115
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_filed_release_says_the_gate_passed_it_and_on_which_words`
  - `tests/test_label_genre_gate.py::test_a_release_that_would_be_held_is_asked_about_again_before_it_is`
  - `tests/test_label_genre_gate.py::test_one_word_of_the_labels_kind_passes_a_release_listing_another_kind_too`

Old text:

```
    if any(found == judged_as for _word, found in placed):
```

New text:

```
    if placed and all(found == judged_as for _word, found in placed):
```

### `r798-a.K3_a_hold_needs_a_known_word`

kind_verdict: hold a release on words no rule knows, so absence of a verdict becomes a hold

- File: `src/cratekit/core/routing.py`
- Source: `r798-a.json`, row `K3_a_hold_needs_a_known_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`, `tests/test_taxonomy.py`, `tests/test_routing_parity.py`
- Collected: 1115 against a baseline of 1115
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_word_no_rule_knows_is_not_judged_and_never_held`

Old text:

```
    if placed:
        others = ", ".join(dict.fromkeys(found for _word, found in placed))
```

New text:

```
    if words:
        others = ", ".join(dict.fromkeys(found for _word, found in placed))
```

### `r798-a.K4_a_label_of_any_kind_passes`

kind_settled: stop passing a label followed for any kind, so it is judged as a kind no rule names

- File: `src/cratekit/core/routing.py`
- Source: `r798-a.json`, row `K4_a_label_of_any_kind_passes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`, `tests/test_taxonomy.py`, `tests/test_routing_parity.py`
- Collected: 1115 against a baseline of 1115
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_label_followed_for_any_kind_files_everything_and_asks_nothing`
  - `tests/test_label_genre_gate.py::test_a_label_followed_for_any_kind_passes_without_a_word`
  - `tests/test_label_genre_gate.py::test_a_label_of_any_kind_reads_no_track_and_asks_nothing`

Old text:

```
    if judged_as == ANY_KIND:
        return KindJudgment(
```

New text:

```
    if False:
        return KindJudgment(
```

### `r798-a.K5_a_kind_nothing_names_is_not_judged`

kind_settled: judge a label marked with a kind the taxonomy does not name, so every release of it with a known word is held

- File: `src/cratekit/core/routing.py`
- Source: `r798-a.json`, row `K5_a_kind_nothing_names_is_not_judged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`, `tests/test_taxonomy.py`, `tests/test_routing_parity.py`
- Collected: 1115 against a baseline of 1115
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_kind_the_taxonomy_does_not_name_is_not_judged_and_says_which`

Old text:

```
    if judged_as not in gate.kinds:
```

New text:

```
    if False:
```

### `r798-d.K11_the_shared_matcher_reads_a_substring_needle`

_rule_matches: drop the any_of arm of the matcher the second review made one function of, so no rule of either table that names a substring claims a word

- File: `src/cratekit/core/routing.py`
- Source: `r798-d.json`, row `K11_the_shared_matcher_reads_a_substring_needle`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`, `tests/test_taxonomy.py`, `tests/test_routing_parity.py`
- Collected: 1115 against a baseline of 1115
- Kills: 101 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[African Music]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Alternative]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Asian Music]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Blues]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Brazilian Music]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Christian]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Classical]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Country]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Cumbia]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Dance]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Electro]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Films/Games]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Folk]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Indian Music]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Jazz]`
  - ... and 86 more, see the JSON sidecar

Old text:

```
        or (rule.any_of and any(needle in value for needle in rule.any_of))
    )


def gate_decisions(
```

New text:

```
    )


def gate_decisions(
```

### `r799-a.R1_a_table_is_read_only_for_its_source`

resolver: read the general catalogue's table for every caller, a record shop's included

- File: `src/cratekit/core/routing.py`
- Source: `r799-a.json`, row `R1_a_table_is_read_only_for_its_source`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocabulary.py`, `tests/test_published_genre.py`, `tests/test_tag_remap.py`
- Collected: 511 against a baseline of 511
- Kills: 2 (killed)
- Killed:
  - `tests/test_vocabulary.py::test_a_record_shops_pop_goes_where_it_went_before[None]`
  - `tests/test_vocabulary.py::test_the_record_shops_searcher_names_no_source_to_the_resolver`

Old text:

```
    table = taxonomy.vocabulary(source) if source is not None else None
```

New text:

```
    table = taxonomy.vocabulary(source or "deezer")
```

### `u118-b.R1_split_competes`

A split place no longer competes in the bucket that declares it

- File: `src/cratekit/core/routing.py`
- Source: `u118-b.json`, row `R1_split_competes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`
- Collected: 103 against a baseline of 103
- Kills: 20 (killed)
- Killed:
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_holds_the_former_place_in_both_buckets`
  - `tests/test_adopt_split_place.py::test_a_soul_track_already_in_its_soul_band_only_leaves_r_and_b`
  - `tests/test_adopt_split_place.py::test_a_soul_track_in_a_renamed_r_and_b_band_is_left_since_the_writer_cannot_see_it`
  - `tests/test_adopt_split_place.py::test_a_soul_track_in_r_and_b_med_moves_to_the_soul_band_its_reading_names[another-band]`
  - `tests/test_adopt_split_place.py::test_a_soul_track_in_r_and_b_med_moves_to_the_soul_band_its_reading_names[low]`
  - `tests/test_adopt_split_place.py::test_a_soul_track_in_r_and_b_med_moves_to_the_soul_band_its_reading_names[same-band]`
  - `tests/test_adopt_split_place.py::test_a_soul_track_in_the_old_soul_r_and_b_playlist_moves_to_soul_and_is_withheld_until`
  - `tests/test_adopt_split_place.py::test_a_soul_track_in_two_r_and_b_bands_leaves_both_in_one_move_and_r_and_b_plans_none`
  - `tests/test_adopt_split_place.py::test_a_soul_track_with_no_reading_leaves_r_and_b_for_soul_unsorted`
  - `tests/test_adopt_split_place.py::test_a_split_place_competes_in_soul_and_nowhere_else`
  - `tests/test_adopt_split_place.py::test_a_track_in_an_r_and_b_band_holds_it_in_r_and_b_and_the_split_place_in_soul`
  - `tests/test_adopt_split_place.py::test_a_track_retagged_out_of_soul_since_the_approval_is_a_stale_decision[Deep House]`
  - `tests/test_adopt_split_place.py::test_a_track_retagged_out_of_soul_since_the_approval_is_a_stale_decision[R&B]`
  - `tests/test_adopt_split_place.py::test_a_track_retagged_out_of_soul_since_the_approval_is_a_stale_decision[]`
  - `tests/test_adopt_split_place.py::test_adoption_withholds_a_soul_track_still_in_an_r_and_b_band`
  - ... and 5 more, see the JSON sidecar

Old text:

```
        | {place.id for place in taxonomy.bucket(bucket_id).split_from}

```

New text:

```
(empty)
```

### `u118-b.R2_split_lookup`

split_place finds nothing, so a split place resolves as an ordinary sub

- File: `src/cratekit/core/routing.py`
- Source: `u118-b.json`, row `R2_split_lookup`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`
- Collected: 103 against a baseline of 103
- Kills: 15 (killed)
- Killed:
  - `tests/test_adopt_former_place.py::test_a_renamed_old_playlist_is_found_through_the_node_recorded_under_the_old_sub`
  - `tests/test_adopt_former_place.py::test_a_second_run_after_the_move_plans_nothing_and_writes_nothing`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_holds_the_former_place_in_both_buckets`
  - `tests/test_adopt_former_place.py::test_adoption_over_the_same_library_files_none_of_them_a_second_time`
  - `tests/test_adopt_former_place.py::test_an_approved_move_files_each_track_in_its_band_and_none_is_left_in_both`
  - `tests/test_adopt_former_place.py::test_the_gate_shows_every_track_leaving_the_old_playlist_and_every_one_left`
  - `tests/test_adopt_split_place.py::test_a_soul_track_in_the_old_soul_r_and_b_playlist_moves_to_soul_and_is_withheld_until`
  - `tests/test_adopt_split_place.py::test_a_split_place_competes_in_soul_and_nowhere_else`
  - `tests/test_adopt_split_place.py::test_a_split_place_is_found_as_the_r_and_b_place_it_is`
  - `tests/test_adopt_split_place.py::test_a_track_in_an_r_and_b_band_holds_it_in_r_and_b_and_the_split_place_in_soul`
  - `tests/test_adopt_split_place.py::test_a_track_in_the_old_hip_hop_playlist_holds_its_former_place_in_both_buckets`
  - `tests/test_adopt_split_place.py::test_adoption_after_the_move_files_none_of_them_a_second_time`
  - `tests/test_adopt_split_place.py::test_an_approved_move_files_soul_and_hip_hop_in_their_folders_and_keeps_r_and_b`
  - `tests/test_adopt_split_place.py::test_the_gate_shows_every_soul_and_hip_hop_track_moving_and_no_r_and_b_track`
  - `tests/test_adopt_split_place.py::test_the_writer_is_told_to_add_the_soul_band_and_leave_the_r_and_b_band_by_name`

Old text:

```
    for place in taxonomy.bucket(bucket_id).split_from:
```

New text:

```
    for place in ():
```

### `u155.R1_exact_match`

routing.genre_sub: match a source case insensitively, so rominimal reaches the sub

- File: `src/cratekit/core/routing.py`
- Source: `u155.json`, row `R1_exact_match`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_energy.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_jazz_folder.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_split_place.py`, `tests/test_analysis_workers.py`, `tests/test_catalogue_searcher.py`, `tests/test_deferred_routing.py`, `tests/test_genre_retag.py`, `tests/test_genre_sub.py`, `tests/test_label_genre_gate.py`, `tests/test_published_genre.py`, `tests/test_rebuild.py`, `tests/test_report_genres.py`, `tests/test_routing_parity.py`, `tests/test_tag_workers.py`, `tests/test_taxonomy.py`, `tests/test_taxonomy_upgrade.py`, `tests/test_vocabulary.py`
- Collected: 2554 against a baseline of 2554
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_sub.py::test_only_the_exact_source_reaches_the_genre_sub[ROMINIMAL]`
  - `tests/test_genre_sub.py::test_only_the_exact_source_reaches_the_genre_sub[rominimal]`

Old text:

```
        if value in genre.sources:
```

New text:

```
        if value.lower() in {source.lower() for source in genre.sources}:
```

### `u155.R2_tagger_branch`

suggest_tag: answer a genre sub hit with the bucket's display, as before the unit

- File: `src/cratekit/core/routing.py`
- Source: `u155.json`, row `R2_tagger_branch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_energy.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_jazz_folder.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_split_place.py`, `tests/test_analysis_workers.py`, `tests/test_catalogue_searcher.py`, `tests/test_deferred_routing.py`, `tests/test_genre_retag.py`, `tests/test_genre_sub.py`, `tests/test_label_genre_gate.py`, `tests/test_published_genre.py`, `tests/test_rebuild.py`, `tests/test_report_genres.py`, `tests/test_routing_parity.py`, `tests/test_tag_workers.py`, `tests/test_taxonomy.py`, `tests/test_taxonomy_upgrade.py`, `tests/test_vocabulary.py`
- Collected: 2554 against a baseline of 2554
- Kills: 4 (killed)
- Killed:
  - `tests/test_genre_sub.py::test_the_tagger_writes_rominimal_rather_than_the_buckets_name[ROMINIMAL]`
  - `tests/test_genre_sub.py::test_the_tagger_writes_rominimal_rather_than_the_buckets_name[Rominimal]`
  - `tests/test_genre_sub.py::test_the_tagger_writes_rominimal_rather_than_the_buckets_name[rominimal]`
  - `tests/test_genre_sub.py::test_the_tagger_writes_the_source_it_matched_when_a_sub_has_two`

Old text:

```
        genre = _genre_sub_by_id(taxonomy.bucket(bucket_id), sub_id)
        if genre is not None:
```

New text:

```
        genre = _genre_sub_by_id(taxonomy.bucket(bucket_id), sub_id)
        if False:
```

### `u155.R3_tagger_spelling`

suggest_tag: always write the first source, not the one the word matched

- File: `src/cratekit/core/routing.py`
- Source: `u155.json`, row `R3_tagger_spelling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_energy.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_jazz_folder.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_split_place.py`, `tests/test_analysis_workers.py`, `tests/test_catalogue_searcher.py`, `tests/test_deferred_routing.py`, `tests/test_genre_retag.py`, `tests/test_genre_sub.py`, `tests/test_label_genre_gate.py`, `tests/test_published_genre.py`, `tests/test_rebuild.py`, `tests/test_report_genres.py`, `tests/test_routing_parity.py`, `tests/test_tag_workers.py`, `tests/test_taxonomy.py`, `tests/test_taxonomy_upgrade.py`, `tests/test_vocabulary.py`
- Collected: 2554 against a baseline of 2554
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_sub.py::test_the_tagger_writes_the_source_it_matched_when_a_sub_has_two`

Old text:

```
            spelled = next(
                (source for source in genre.sources if source.lower().strip() == lowered),
                genre.sources[0],
            )
```

New text:

```
            spelled = genre.sources[0]
```

### `u155.R4_genre_sub_named`

genre_sub_named: answer False, so a gate shows the genre sub as the energy sub

- File: `src/cratekit/core/routing.py`
- Source: `u155.json`, row `R4_genre_sub_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 3 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_database_inbox_gate_shows_a_genre_sub_beside_the_band_and_files_both`
  - `tests/test_routing_workers.py::test_the_export_gate_shows_a_genre_sub_beside_the_band_and_files_both`
  - `tests/test_routing_workers.py::test_the_unplaced_export_names_a_genre_sub_beside_the_band_and_files_both`

Old text:

```
    return _genre_sub_by_id(taxonomy.bucket(bucket_id), sub_id) is not None
```

New text:

```
    return False
```

### `u87-b.S1_curve_boundary`

Existing: routing.energy_rating reads a cut's max as exclusive

- File: `src/cratekit/core/routing.py`
- Source: `u87-b.json`, row `S1_curve_boundary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_catalogue_searcher.py`, `tests/test_deferred_routing.py`, `tests/test_rebuild.py`, `tests/test_routing_parity.py`, `tests/test_taxonomy.py`
- Collected: 1410 against a baseline of 1410
- Kills: 6 (killed)
- Killed:
  - `tests/test_routing_parity.py::test_energy_level_four_follows_the_tree_rule_not_the_dashboard_rule`
  - `tests/test_routing_parity.py::test_the_star_curve_is_unchanged[2]`
  - `tests/test_routing_parity.py::test_the_star_curve_is_unchanged[4]`
  - `tests/test_routing_parity.py::test_the_star_curve_is_unchanged[6]`
  - `tests/test_routing_parity.py::test_the_star_curve_is_unchanged[8]`
  - `tests/test_taxonomy.py::test_a_custom_taxonomy_uses_its_own_rating_curve`

Old text:

```
        if level <= cut.max:
            return cut.rating
```

New text:

```
        if level < cut.max:
            return cut.rating
```

### `r722-b.T6_field_failure_swallowed`

An undecodable field reads as absent in the checked reader, rerun after the fix round

- File: `src/cratekit/core/tags.py`
- Source: `r722-b.json`, row `T6_field_failure_swallowed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`, `tests/test_analysis_workers.py`, `tests/test_art.py`, `tests/test_genre_retag.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_match_states.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`, `tests/test_setbuilder_cli.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`, `tests/test_vocals_cli.py`
- Collected: 3054 against a baseline of 3054
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_an_undecodable_field_fails_the_checked_read`

Old text:

```
            if strict:
                raise TagReadFailed(f"{key}: {type(exc).__name__}: {exc}") from exc
            log.debug("tag read failed for %s %s: %s", path, key, exc)
```

New text:

```
            log.debug("tag read failed for %s %s: %s", path, key, exc)
```

### `r722-b.T7_lenient_field_raises`

The lenient reader raises on one undecodable field instead of reading it as None, rerun after the fix round

- File: `src/cratekit/core/tags.py`
- Source: `r722-b.json`, row `T7_lenient_field_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`, `tests/test_analysis_workers.py`, `tests/test_art.py`, `tests/test_genre_retag.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_match_states.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`, `tests/test_setbuilder_cli.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`, `tests/test_vocals_cli.py`
- Collected: 3054 against a baseline of 3054
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_an_undecodable_field_reads_as_none_beside_its_neighbours`

Old text:

```
            if strict:
                raise TagReadFailed(f"{key}: {type(exc).__name__}: {exc}") from exc
            log.debug("tag read failed for %s %s: %s", path, key, exc)
```

New text:

```
            raise TagReadFailed(f"{key}: {type(exc).__name__}: {exc}") from exc
```

### `r722.T1_checked_is_lenient`

read_tags_checked runs the lenient body

- File: `src/cratekit/core/tags.py`
- Source: `r722.json`, row `T1_checked_is_lenient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`, `tests/test_analysis_workers.py`, `tests/test_art.py`, `tests/test_genre_retag.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_match_states.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`, `tests/test_setbuilder_cli.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`, `tests/test_vocals_cli.py`
- Collected: 3054 against a baseline of 3054
- Kills: 5 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_a_container_the_tag_library_does_not_recognise_is_unreadable`
  - `tests/test_adopt_energy.py::test_a_file_whose_tags_cannot_be_read_is_reported`
  - `tests/test_adopt_energy.py::test_an_undecodable_field_fails_the_checked_read`
  - `tests/test_adopt_energy.py::test_an_unreadable_file_and_an_untagged_one_are_different_plans`
  - `tests/test_adopt_energy.py::test_the_checked_reader_tells_absent_from_unreadable`

Old text:

```
    return _read_tags(path, fields, strict=True)
```

New text:

```
    return _read_tags(path, fields, strict=False)
```

### `r722.T3_open_failure_is_absent`

A mutagen open failure reads as absent in the checked reader

- File: `src/cratekit/core/tags.py`
- Source: `r722.json`, row `T3_open_failure_is_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`, `tests/test_analysis_workers.py`, `tests/test_art.py`, `tests/test_genre_retag.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_match_states.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`, `tests/test_setbuilder_cli.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`, `tests/test_vocals_cli.py`
- Collected: 3054 against a baseline of 3054
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_a_file_whose_tags_cannot_be_read_is_reported`
  - `tests/test_adopt_energy.py::test_an_unreadable_file_and_an_untagged_one_are_different_plans`
  - `tests/test_adopt_energy.py::test_the_checked_reader_tells_absent_from_unreadable`

Old text:

```
        if strict:
            raise TagReadFailed(f"{type(exc).__name__}: {exc}") from exc
        log.debug("tag read failed for %s: %s", path, exc)
```

New text:

```
        log.debug("tag read failed for %s: %s", path, exc)
```

### `r722.T8_lenient_energy_raises`

read_energy_from_file stops folding a failed read into None

- File: `src/cratekit/core/tags.py`
- Source: `r722.json`, row `T8_lenient_energy_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`, `tests/test_analysis_workers.py`, `tests/test_art.py`, `tests/test_genre_retag.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_match_states.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`, `tests/test_setbuilder_cli.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`, `tests/test_vocals_cli.py`
- Collected: 3054 against a baseline of 3054
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_the_checked_reader_tells_absent_from_unreadable`

Old text:

```
    try:
        return read_energy_checked(path)
    except TagReadFailed as exc:
        log.debug("energy read failed for %s: %s", path, exc)
        return None
```

New text:

```
    return read_energy_checked(path)
```

### `r722.T9_lenient_open_raises`

The lenient reader raises when mutagen cannot open a file

- File: `src/cratekit/core/tags.py`
- Source: `r722.json`, row `T9_lenient_open_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`, `tests/test_analysis_workers.py`, `tests/test_art.py`, `tests/test_genre_retag.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_match_states.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`, `tests/test_setbuilder_cli.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`, `tests/test_vocals_cli.py`
- Collected: 3054 against a baseline of 3054
- Kills: 305 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_a_row_the_library_already_holds_is_not_fetched`
  - `tests/test_match_states.py::test_a_candidate_shows_a_key_that_is_true_of_every_path_it_carries`
  - `tests/test_match_states.py::test_a_candidate_whose_title_folds_to_something_keeps_its_identifier`
  - `tests/test_match_states.py::test_a_file_whose_artist_and_title_are_the_rows_swapped_is_still_offered`
  - `tests/test_match_states.py::test_a_held_emoji_row_does_not_retire_another_emoji_rows_question`
  - `tests/test_match_states.py::test_a_held_file_crediting_somebody_else_never_calls_the_companion_stale`
  - `tests/test_match_states.py::test_a_key_question_answered_elsewhere_does_not_settle_a_version_question`
  - `tests/test_match_states.py::test_a_key_that_disagrees_outright_is_a_different_answer`
  - `tests/test_match_states.py::test_a_list_line_that_names_a_key_is_a_different_question_from_one_that_does_not`
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_lossy_marker_the_template_declares_is_stripped_from_the_recording`
  - `tests/test_match_states.py::test_a_one_letter_title_is_judged_by_the_same_rule`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Acoustic]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Demo]`
  - ... and 290 more, see the JSON sidecar

Old text:

```
        if strict:
            raise TagReadFailed(f"{type(exc).__name__}: {exc}") from exc
        log.debug("tag read failed for %s: %s", path, exc)
```

New text:

```
        raise TagReadFailed(f"{type(exc).__name__}: {exc}") from exc
```

### `u23-round-8-independent-hunt.HUNT_a_container_leaves_the_writers_table`

Drop .aifc from AIFF_SUFFIXES, so it leaves tags._DIALECT_BY_SUFFIX and LEDGER_CONTAINERS with it

- File: `src/cratekit/core/tags.py`
- Source: `u23-round-8-independent-hunt.json`, row `HUNT_a_container_leaves_the_writers_table`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`, `tests/test_tags.py`
- Collected: 625 against a baseline of 663
- Kills: 1 (collect-error)
- Note: collection changed: 625 collected against a baseline of 663. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_tags.py::test_each_container_is_classified_once[.aifc-Dialect.ID3]`

Old text:

```
AIFF_SUFFIXES = (".aiff", ".aif", ".aifc")
```

New text:

```
AIFF_SUFFIXES = (".aiff", ".aif")
```

### `u23-round-8-independent.X15_save_drops_the_id3v1_trailer`

A tag write destroys an mp3's legacy ID3v1 trailer

- File: `src/cratekit/core/tags.py`
- Source: `u23-round-8-independent.json`, row `X15_save_drops_the_id3v1_trailer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_adoption.py`, `tests/test_tags.py`
- Collected: 872 against a baseline of 872
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_an_mp3s_legacy_id3v1_genre_survives_a_write_and_a_revert[.mp3]`

Old text:

```
    trailer = _id3v1_trailer(path)
    handle.save()
    if trailer is not None:
        _restore_id3v1_trailer(path, trailer)

```

New text:

```
    handle.save()

```

### `u240.M25_copyright_key_wrong`

FIELDS: read the MP4 copyright line from a key the downloader never writes

- File: `src/cratekit/core/tags.py`
- Source: `u240.json`, row `M25_copyright_key_wrong`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 334 against a baseline of 334
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_the_copyright_line_is_read_from_the_key_the_downloader_writes[.m4a]`

Old text:

```
    "copyright": TagSpec("copyright", "TCOP", "cprt"),
```

New text:

```
    "copyright": TagSpec("copyright", "TCOP", "\xa9cpy"),
```

### `u249.M15_noting_reader_drops_field_failure`

_read_tags: note no failure for one undecodable field, so a partly failed read is remembered

- File: `src/cratekit/core/tags.py`
- Source: `u249.json`, row `M15_noting_reader_drops_field_failure`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_tags.py`, `tests/test_match_states.py`
- Collected: 686 against a baseline of 686
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_the_noting_reader_answers_what_the_lenient_reader_answers_and_says_what_failed`

Old text:

```
            if failed is not None:
                failed.append(f"{key}: {type(exc).__name__}: {exc}")
            values[field] = None
```

New text:

```
            values[field] = None
```

### `u249.M16_noting_reader_drops_open_failure`

_read_tags: note no failure for a container mutagen could not open, so a moment's I/O error is remembered

- File: `src/cratekit/core/tags.py`
- Source: `u249.json`, row `M16_noting_reader_drops_open_failure`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_tags.py`, `tests/test_match_states.py`
- Collected: 686 against a baseline of 686
- Kills: 2 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_read_that_failed_is_not_remembered`
  - `tests/test_library_reads_remembered.py::test_the_noting_reader_answers_what_the_lenient_reader_answers_and_says_what_failed`

Old text:

```
        if failed is not None:
            failed.append(f"{type(exc).__name__}: {exc}")
        return absent
```

New text:

```
        return absent
```

### `u249.M17_noting_reader_drops_unrecognised`

_read_tags: note no failure for a container mutagen did not recognise

- File: `src/cratekit/core/tags.py`
- Source: `u249.json`, row `M17_noting_reader_drops_unrecognised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_tags.py`, `tests/test_match_states.py`
- Collected: 686 against a baseline of 686
- Kills: 3 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_container_the_reader_cannot_take_is_absent_and_not_whole[empty.m4a]`
  - `tests/test_library_reads_remembered.py::test_a_container_the_reader_cannot_take_is_absent_and_not_whole[empty.ogg]`
  - `tests/test_library_reads_remembered.py::test_a_container_the_reader_cannot_take_is_absent_and_not_whole[zeros.opus]`

Old text:

```
        if failed is not None:
            failed.append("not a container the tag library recognises")
        return absent
```

New text:

```
        return absent
```

### `u249.M18_noting_reader_drops_unsupported`

_read_tags: note no failure for a container this module does not read

- File: `src/cratekit/core/tags.py`
- Source: `u249.json`, row `M18_noting_reader_drops_unsupported`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_tags.py`, `tests/test_match_states.py`
- Collected: 686 against a baseline of 686
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_container_the_reader_cannot_take_is_absent_and_not_whole[short.aac]`

Old text:

```
        if failed is not None:
            failed.append(str(exc))
        return absent
```

New text:

```
        return absent
```

### `u249.M19_noting_reader_inverted`

read_tags_noting: report a failed read as whole

- File: `src/cratekit/core/tags.py`
- Source: `u249.json`, row `M19_noting_reader_inverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_tags.py`, `tests/test_match_states.py`
- Collected: 686 against a baseline of 686
- Kills: 6 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_container_the_reader_cannot_take_is_absent_and_not_whole[empty.m4a]`
  - `tests/test_library_reads_remembered.py::test_a_container_the_reader_cannot_take_is_absent_and_not_whole[empty.ogg]`
  - `tests/test_library_reads_remembered.py::test_a_container_the_reader_cannot_take_is_absent_and_not_whole[short.aac]`
  - `tests/test_library_reads_remembered.py::test_a_container_the_reader_cannot_take_is_absent_and_not_whole[zeros.opus]`
  - `tests/test_library_reads_remembered.py::test_a_read_that_failed_is_not_remembered`
  - `tests/test_library_reads_remembered.py::test_the_noting_reader_answers_what_the_lenient_reader_answers_and_says_what_failed`

Old text:

```
    return values, not failed
```

New text:

```
    return values, True
```

### `u250.M5_word_reads_zero`

whole_number: read a stored value that is not a number as 0 rather than None, so a word files in the lowest band

- File: `src/cratekit/core/tags.py`
- Source: `u250.json`, row `M5_word_reads_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild_one_open.py`, `tests/test_tags.py`, `tests/test_rebuild.py`
- Collected: 207 against a baseline of 207
- Kills: 1 (killed)
- Killed:
  - `tests/test_rebuild_one_open.py::test_a_numeric_reading_converts_the_way_the_single_readers_convert`

Old text:

```
    except ValueError:
        log.debug("non-numeric %s tag on %s: %r", field, path, value)
        return None
```

New text:

```
    except ValueError:
        log.debug("non-numeric %s tag on %s: %r", field, path, value)
        return 0
```

### `u250.M6_absent_raises`

whole_number: drop the absent check, so an untagged file raises out of read_truth and abandons the derivation

- File: `src/cratekit/core/tags.py`
- Source: `u250.json`, row `M6_absent_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild_one_open.py`, `tests/test_tags.py`, `tests/test_rebuild.py`
- Collected: 207 against a baseline of 207
- Kills: 20 (killed)
- Killed:
  - `tests/test_rebuild_one_open.py::test_a_derivation_over_n_files_makes_n_opens`
  - `tests/test_rebuild_one_open.py::test_a_file_no_open_can_read_reads_three_absent_values[empty.flac-]`
  - `tests/test_rebuild_one_open.py::test_a_file_no_open_can_read_reads_three_absent_values[garbage.aiff-FORM\x00\x00\x00\x04AIFX]`
  - `tests/test_rebuild_one_open.py::test_a_file_no_open_can_read_reads_three_absent_values[garbage.m4a-\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk]`
  - `tests/test_rebuild_one_open.py::test_a_file_no_open_can_read_reads_three_absent_values[garbage.mp3-content1]`
  - `tests/test_rebuild_one_open.py::test_a_file_no_open_can_read_reads_three_absent_values[truncated.wav-RIFF$\x00\x00\x00WAVEfmt ]`
  - `tests/test_rebuild_one_open.py::test_an_undecodable_field_reads_none_and_its_neighbours_still_read`
  - `tests/test_rebuild_one_open.py::test_an_unsupported_suffix_reads_absent_and_opens_nothing`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[genre-only-.aiff]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[genre-only-.flac]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[genre-only-.m4a]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[genre-only-.mp3]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[genre-only-.ogg]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[genre-only-.wav]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[untagged-.aiff]`
  - ... and 5 more, see the JSON sidecar

Old text:

```
    if value is None:
        return None
    try:
        return int(value)
```

New text:

```
    try:
        return int(value)
```

### `u250.M7_energy_word_reads_absent`

read_energy_checked: answer None for a stored energy that is not a number instead of raising, so a damaged file reads as untagged

- File: `src/cratekit/core/tags.py`
- Source: `u250.json`, row `M7_energy_word_reads_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_energy.py`, `tests/test_tags.py`, `tests/test_rebuild_one_open.py`, `tests/test_organize_mirror_edits_u227.py`
- Collected: 123 against a baseline of 123
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_a_value_that_is_not_a_number_is_reported_as_unreadable`
  - `tests/test_adopt_energy.py::test_the_checked_reader_tells_absent_from_unreadable`

Old text:

```
    if number is None:
        raise TagReadFailed(f"energylevel is not a number: {value!r}")
```

New text:

```
    if number is None:
        return None
```

### `u250.M8_conversion_learns_decimals`

whole_number: read a decimal as its whole part, so 7.0 files at energy 7 where today it reads None

- File: `src/cratekit/core/tags.py`
- Source: `u250.json`, row `M8_conversion_learns_decimals`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild_one_open.py`, `tests/test_tags.py`, `tests/test_rebuild.py`
- Collected: 207 against a baseline of 207
- Kills: 1 (killed)
- Killed:
  - `tests/test_rebuild_one_open.py::test_a_numeric_reading_converts_the_way_the_single_readers_convert`

Old text:

```
    try:
        return int(value)
    except ValueError:
        log.debug("non-numeric %s tag on %s: %r", field, path, value)
```

New text:

```
    try:
        return int(float(value))
    except ValueError:
        log.debug("non-numeric %s tag on %s: %r", field, path, value)
```

### `u81-fetch-b.S1_strip_does_nothing`

strip_tags reports success and removes nothing, so an upload's tempo frame survives

- File: `src/cratekit/core/tags.py`
- Source: `u81-fetch-b.json`, row `S1_strip_does_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_a_tempo_the_upload_carried_is_never_committed`
  - `tests/test_acquire_fallback_fetch.py::test_strip_tags_empties_an_id3_chunk_inside_a_container_and_keeps_the_audio`

Old text:

```
        handle.delete()
        return True
```

New text:

```
        return True
```

