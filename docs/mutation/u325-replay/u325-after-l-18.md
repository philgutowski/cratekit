# Mutation table: u325-after-l-18

Measured by `scripts/mutate.py` on 2026-11-22 22:24 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 124.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:23 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 12, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r1115.M1_failed_needs_a_failure` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 368 | 1 | killed |
| `r1115.M2_every_failure_for_good` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 368 | 5 | killed |
| `r1115.M3_nothing_left_to_run` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 368 | 1 | killed |
| `r1115.M4_retryable_is_not_for_good` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 368 | 4 | killed |
| `r1115.M5_declined_is_refused` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 368 | 8 | killed |
| `r1115.M6_landed_needs_a_track` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 368 | 3 | killed |
| `r1115.M7_done_counts_done` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 368 | 8 | killed |
| `r1115.M8_failed_names_the_failures` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 368 | 2 | killed |
| `u178.G6_fallback_refusal` | `src/cratekit/label/cli.py` | user | 3 file(s) | 284 | 1 | killed |
| `u178.G7_fallback_confirm_ignored` | `src/cratekit/label/cli.py` | user | 3 file(s) | 284 | 1 | killed |
| `u178.G8_clear_word_case` | `src/cratekit/label/cli.py` | user | 3 file(s) | 284 | 1 | killed |
| `u178.G9_accept_without_genre` | `src/cratekit/label/cli.py` | user | 3 file(s) | 284 | 1 | killed |
| `u178.G1_genre_length_bound` | `src/cratekit/label/registry.py` | user | 3 file(s) | 284 | 1 | killed |
| `u178.G2_genre_needs_a_letter` | `src/cratekit/label/registry.py` | user | 3 file(s) | 284 | 1 | killed |
| `u178.G3_genre_one_line` | `src/cratekit/label/registry.py` | user | 3 file(s) | 284 | 1 | killed |
| `u178.G4_edit_clear_genre` | `src/cratekit/label/registry.py` | user | 3 file(s) | 284 | 1 | killed |
| `u178.G5_edit_none_keeps_genre` | `src/cratekit/label/registry.py` | user | 3 file(s) | 284 | 1 | killed |
| `u278.M10_window_short` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 177 | 4 | killed |
| `u278.M11_window_dropped_on_read` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 177 | 21 | killed |
| `u278.M12_no_over_the_line_in_call` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 177 | 1 | killed |
| `u278.M13_over_the_line_loosened` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 177 | 3 | killed |
| `u278.M14_hour_raise_ignored` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 177 | 2 | killed |
| `u278.M15_hour_not_exported` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 177 | 1 | killed |
| `u278.M16_nested_class_kept` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 177 | 2 | killed |
| `u278.M2_future_minute_not_settled` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 177 | 2 | killed |
| `u278.M5_budget_off_by_one` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 177 | 16 | killed |
| `u278.M6_count_not_written` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 177 | 23 | killed |
| `u278.M7_identities_merged` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 177 | 2 | killed |
| `u119-b.G12r_removed_namesake_written_into` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 45 | 1 | killed |
| `u119-b.G5r_favorites_counted_as_members` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 45 | 1 | killed |
| `u119-c.C2_torn_bucket_bound_anyway` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 45 | 1 | killed |
| `u119-c.C5_interruption_unreported` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 45 | 3 | killed |
| `u119.G10_placements_no_gap` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 45 | 2 | killed |
| `u119.G11_stale_digest` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 45 | 2 | killed |
| `u119.G13_removals_when_not_asked` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 45 | 2 | killed |
| `u119.G15_removal_commit_admits_nothing` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 45 | 5 | killed |
| `u119.G1_class_undeclared` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 45 | 2 | killed |
| `u119.G4_removed_membership_live` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 45 | 1 | killed |
| `u119.G6_wanted_is_members` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 45 | 13 | killed |
| `u119.G7_twin_folders_first_taken` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 45 | 1 | killed |
| `u119.G9_digest_over_adds` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 45 | 1 | killed |
| `u185.R4_genre_source` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 45 | 1 | killed |
| `u119.V1_ack_after_plan` | `src/cratekit/favorites/refresh_cli.py` | user | 1 file(s) | 45 | 1 | killed |
| `u239.L01_remember_land_only` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 275 | 1 | killed |
| `u239.L02_remember_owner` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 275 | 2 | killed |
| `u239.L03_remember_called` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 275 | 6 | killed |
| `u239.L05_commands_added` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 275 | 3 | killed |
| `u239.L06_unrecorded_warning` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 275 | 1 | killed |
| `r1467.M19_root_unreadable_refuses` | `src/cratekit/intake/land_cli.py` | user | 3 file(s) | 275 | 1 | killed |
| `r1467.M20_retired_file_proves` | `src/cratekit/intake/land_cli.py` | user | 3 file(s) | 275 | 1 | killed |
| `r1467.M21_native_record_proves` | `src/cratekit/intake/land_cli.py` | user | 3 file(s) | 275 | 1 | killed |
| `r1467.M22_proof_is_a_file` | `src/cratekit/intake/land_cli.py` | user | 3 file(s) | 275 | 1 | killed |
| `r799-c.V1_the_gate_is_asked_before_the_write` | `src/cratekit/tagging/remap_cli.py` | user | 1 file(s) | 93 | 15 | killed |
| `r799-c.V2_a_file_that_did_not_take_refuses` | `src/cratekit/tagging/remap_cli.py` | user | 1 file(s) | 93 | 7 | killed |
| `r799-b.P1_a_file_is_planned_only_while_it_carries_what_a_record_wrote` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 15 | killed |
| `r799-b.P2_two_explanations_are_ambiguous` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 4 | killed |
| `r799-b.P3_a_shops_genre_is_the_shops` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 1 | killed |
| `r799-b.P4_a_rewrite_retires_the_record_it_replaced` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 2 | killed |
| `r799-b.P5_only_a_file_under_the_library_is_opened` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 4 | killed |
| `r799-b.P6_one_file_is_one_group` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `r799-b.W2_the_writers_answer_is_kept` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 3 | killed |
| `r799-c.P11_blank_is_not_agreement` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 1 | killed |
| `r799-c.V3_an_unrecorded_rewrite_is_not_clean` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 2 | killed |
| `r799-c.W4_a_rewrite_is_recorded` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 5 | killed |
| `r799-c.W5_a_rewrites_record_is_one_generation_on` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 4 | killed |
| `u52-item-derivation.H2_listing_passthrough_gone` | `src/cratekit/label/cli.py` | user | 2 file(s) | 262 | 1 | killed |
| `u52-item-derivation.H4_verification_boundary_gone` | `src/cratekit/label/cli.py` | user | 2 file(s) | 262 | 2 | killed |
| `u52-item-derivation.H6_empty_playlist_reports_ok` | `src/cratekit/label/cli.py` | user | 2 file(s) | 262 | 2 | killed |
| `u52-item-derivation.H7_unresolved_drops_nameless` | `src/cratekit/label/cli.py` | user | 2 file(s) | 262 | 1 | killed |
| `u52-item-derivation.I5_import_queues_no_item` | `src/cratekit/label/cli.py` | user | 2 file(s) | 262 | 4 | killed |
| `u52-item-derivation.I6_import_item_keyed_on_name` | `src/cratekit/label/cli.py` | user | 2 file(s) | 262 | 2 | killed |
| `u52-item-derivation.R1_itemless_job_drives` | `src/cratekit/label/cli.py` | user | 2 file(s) | 262 | 3 | killed |
| `u52-item-derivation.S1_errors_branch_gone` | `src/cratekit/label/cli.py` | user | 2 file(s) | 262 | 1 | killed |
| `u52-zero-rows.H5_verifier_passthrough_gone` | `src/cratekit/label/cli.py` | user | 2 file(s) | 262 | 1 | killed |
| `r662-a.M2_spelled_path_compared_whole` | `src/cratekit/core/config.py` | user | 2 file(s) | 658 | 2 | killed |
| `r662-a.M4_validator_drops_disagreement` | `src/cratekit/core/config.py` | user | 2 file(s) | 658 | 7 | killed |
| `r662-a.M5_validator_message_loses_flag` | `src/cratekit/core/config.py` | user | 2 file(s) | 658 | 1 | killed |
| `r662-b.M1b_several_remotes_compared` | `src/cratekit/core/config.py` | user | 2 file(s) | 658 | 1 | killed |
| `r662-b.M3b_blank_remote_disagrees` | `src/cratekit/core/config.py` | maintainer | 2 file(s) | 658 | 1 | killed |
| `r838-c.R1_library_bound` | `src/cratekit/sync/mark_record.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-c.R2_remark_clears` | `src/cratekit/sync/mark_record.py` | maintainer | 1 file(s) | 32 | 1 | killed |
| `r838-d.R3b_stamp_target` | `src/cratekit/sync/mark_record.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-a.U1_refuse_stranger` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-a.U3_pass_filter` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 2 | killed |
| `r838-a.U4_already_unmarked_stamp` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-a.U5_marked_again` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-a.U6_later_order` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-a.U8_title_already_back` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-b.U10_digest_names` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-b.U13_recheck` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-b.U15_rename_target` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 8 | killed |
| `r838-b.U16_part_way_names` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-b.U9_renamed_since` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-c.U7b_not_listed_rerun` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r289-b.B1_reclaim_rmtree` | `src/cratekit/acquire/cli.py` | user | 6 file(s) | 398 | 2 | killed |
| `r289-b.B3_terminal_filter_gone` | `src/cratekit/acquire/cli.py` | user | 6 file(s) | 398 | 2 | killed |
| `r289-b.B4_unknown_job_read_as_terminal` | `src/cratekit/acquire/cli.py` | user | 6 file(s) | 398 | 1 | killed |
| `r289-b.B5_job_directory_before_its_items` | `src/cratekit/acquire/cli.py` | user | 6 file(s) | 398 | 2 | killed |
| `r289-b.B6_job_directory_never_reclaimed` | `src/cratekit/acquire/cli.py` | user | 6 file(s) | 398 | 2 | killed |
| `r289-b.C1_download_call_site` | `src/cratekit/acquire/cli.py` | user | 6 file(s) | 398 | 1 | killed |
| `r289-c.B2r_reclaim_reports_a_failure_as_a_removal` | `src/cratekit/acquire/cli.py` | maintainer | 6 file(s) | 398 | 1 | killed |
| `u219.G2_nothing_to_add` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 309 | 1 | killed |
| `u219.G3_adds_frozen` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 309 | 21 | killed |
| `u219.G4_worker_own_tree` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 309 | 1 | killed |
| `u219.G5_resume_run` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 309 | 1 | killed |
| `u219.M3_due_again_said` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 309 | 1 | killed |
| `u219.R1_routed_trees` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 309 | 12 | killed |
| `u219.R2_inbox_routed_only` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 309 | 1 | killed |
| `u219.R3_left_alone_named` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 309 | 1 | killed |
| `u149.T2_two_folders_not_refused` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 1 | killed |

## Zero rows and what they owe

- `r799-b.P6_one_file_is_one_group` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `r1115.M1_failed_needs_a_failure`

read_download: drop the rule that a FAILED job settles only with a failed track, so a FAILED job holding none reads as settled

- File: `src/cratekit/acquire/cli.py`
- Source: `r1115.json`, row `M1_failed_needs_a_failure`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`, `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 368 against a baseline of 368
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_settles_only_when_nothing_it_did_not_land_could_land_on_a_retry[failed-with-no-failed-track]`

Old text:

```
        and bool(failed)

```

New text:

```
        and True

```

### `r1115.M2_every_failure_for_good`

read_download: drop the rule that every failed track is refused for good, so a transient failure settles and the go lands over it

- File: `src/cratekit/acquire/cli.py`
- Source: `r1115.json`, row `M2_every_failure_for_good`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`, `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 368 against a baseline of 368
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run`
  - `tests/test_label_sync_go.py::test_a_download_settles_only_when_nothing_it_did_not_land_could_land_on_a_retry[a-failure-a-retry-could-clear]`
  - `tests/test_label_sync_go.py::test_a_download_settles_only_when_nothing_it_did_not_land_could_land_on_a_retry[a-failure-recording-no-cause]`
  - `tests/test_label_sync_go.py::test_a_transient_failure_still_ends_the_go_on_its_refusal_with_no_tail`
  - `tests/test_sync_land.py::test_a_transient_download_failure_ends_the_pass_and_lands_nothing`

Old text:

```
        and len(for_good) == len(failed)

```

New text:

```
        and len(for_good) >= 0

```

### `r1115.M3_nothing_left_to_run`

read_download: drop the rule that no track is still to run, so a FAILED job with a track never attempted settles

- File: `src/cratekit/acquire/cli.py`
- Source: `r1115.json`, row `M3_nothing_left_to_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`, `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 368 against a baseline of 368
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_settles_only_when_nothing_it_did_not_land_could_land_on_a_retry[a-track-never-attempted]`

Old text:

```
        and all(item.state in finished for item in held)

```

New text:

```
        and any(item.state in finished for item in held)

```

### `r1115.M4_retryable_is_not_for_good`

read_download: read every failure with a cause as refused for good, retryable or not

- File: `src/cratekit/acquire/cli.py`
- Source: `r1115.json`, row `M4_retryable_is_not_for_good`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`, `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 368 against a baseline of 368
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run`
  - `tests/test_label_sync_go.py::test_a_download_settles_only_when_nothing_it_did_not_land_could_land_on_a_retry[a-failure-a-retry-could-clear]`
  - `tests/test_label_sync_go.py::test_a_transient_failure_still_ends_the_go_on_its_refusal_with_no_tail`
  - `tests/test_sync_land.py::test_a_transient_download_failure_ends_the_pass_and_lands_nothing`

Old text:

```
        item.item_id for item in failed if item.cause is not None and not item.cause.retryable

```

New text:

```
        item.item_id for item in failed if item.cause is not None

```

### `r1115.M5_declined_is_refused`

read_download: leave a declined track out of the refused rows, so a lossy only track is named nowhere on the go's check

- File: `src/cratekit/acquire/cli.py`
- Source: `r1115.json`, row `M5_declined_is_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`, `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 368 against a baseline of 368
- Kills: 8 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_settles_only_when_nothing_it_did_not_land_could_land_on_a_retry[succeeded-with-a-declined-track]`
  - `tests/test_label_sync_go.py::test_a_go_under_its_run_over_a_download_that_refused_every_track_runs_no_tail`
  - `tests/test_label_sync_go.py::test_a_go_whose_every_track_was_refused_runs_no_tail_and_says_so`
  - `tests/test_label_sync_go.py::test_a_release_whose_second_track_lands_lossy_runs_the_tail_on_the_first_and_names_it`
  - `tests/test_label_sync_go.py::test_a_runs_own_tail_refused_beside_a_download_names_its_tracks_refused_for_good`
  - `tests/test_label_sync_go.py::test_a_tail_refused_beside_a_download_still_names_the_tracks_refused_for_good`
  - `tests/test_sync_land.py::test_every_download_refused_lands_nothing_on_a_failing_row`
  - `tests/test_sync_land.py::test_one_lossy_refusal_among_eight_downloads_lands_seven_and_reports_one`

Old text:

```
        and (item.item_id in for_good or item.state is jobs.ItemState.SKIPPED)

```

New text:

```
        and (item.item_id in for_good)

```

### `r1115.M6_landed_needs_a_track`

DownloadRead.landed: read a settled download with no track done as landed, so a tail is set over an empty folder

- File: `src/cratekit/acquire/cli.py`
- Source: `r1115.json`, row `M6_landed_needs_a_track`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`, `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 368 against a baseline of 368
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_whose_every_track_failed_for_good_runs_no_tail_and_says_so`
  - `tests/test_label_sync_go.py::test_a_go_under_its_run_over_a_download_that_refused_every_track_runs_no_tail`
  - `tests/test_label_sync_go.py::test_a_go_whose_every_track_was_refused_runs_no_tail_and_says_so`

Old text:

```
        return self.settled and self.done > 0

```

New text:

```
        return self.settled

```

### `r1115.M7_done_counts_done`

read_download: count a skipped track as done too

- File: `src/cratekit/acquire/cli.py`
- Source: `r1115.json`, row `M7_done_counts_done`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`, `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 368 against a baseline of 368
- Kills: 8 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_settles_only_when_nothing_it_did_not_land_could_land_on_a_retry[failed-with-no-failed-track]`
  - `tests/test_label_sync_go.py::test_a_download_settles_only_when_nothing_it_did_not_land_could_land_on_a_retry[succeeded-with-a-declined-track]`
  - `tests/test_label_sync_go.py::test_a_go_under_its_run_over_a_download_that_refused_every_track_runs_no_tail`
  - `tests/test_label_sync_go.py::test_a_go_whose_every_track_was_refused_runs_no_tail_and_says_so`
  - `tests/test_label_sync_go.py::test_a_release_whose_second_track_lands_lossy_runs_the_tail_on_the_first_and_names_it`
  - `tests/test_sync_land.py::test_every_download_refused_lands_nothing_on_a_failing_row`
  - `tests/test_sync_land.py::test_one_lossy_refusal_among_eight_downloads_lands_seven_and_reports_one`
  - `tests/test_sync_land.py::test_the_newest_download_over_the_list_is_the_one_the_pass_reads`

Old text:

```
        done=sum(1 for item in held if item.state is jobs.ItemState.DONE),

```

New text:

```
        done=sum(1 for item in held if item.state in (jobs.ItemState.DONE, jobs.ItemState.SKIPPED)),

```

### `r1115.M8_failed_names_the_failures`

read_download: name no failed track, so the go's own warning for one is never raised

- File: `src/cratekit/acquire/cli.py`
- Source: `r1115.json`, row `M8_failed_names_the_failures`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`, `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 368 against a baseline of 368
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_failed_only_by_a_track_refused_for_good_runs_the_tail_on_the_rest`
  - `tests/test_label_sync_go.py::test_a_resumed_download_failed_only_by_a_refusal_lands_under_the_first_gos_manifest`

Old text:

```
        failed=tuple(item.item_id for item in failed if item.item_id in for_good),

```

New text:

```
        failed=(),

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

### `u178.G1_genre_length_bound`

check_genre: the bound read one past GENRE_MAX, so a 65 character genre is stored

- File: `src/cratekit/label/registry.py`
- Source: `u178.json`, row `G1_genre_length_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_label_genre_gate.py`, `tests/test_label_workers.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_genre_that_could_never_be_one_refuses_at_the_store[xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx]`

Old text:

```
        or len(text) > GENRE_MAX

```

New text:

```
        or len(text) > GENRE_MAX + 1

```

### `u178.G2_genre_needs_a_letter`

check_genre: drop the letter or digit rule, so a punctuation only genre is stored

- File: `src/cratekit/label/registry.py`
- Source: `u178.json`, row `G2_genre_needs_a_letter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_label_genre_gate.py`, `tests/test_label_workers.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_genre_that_could_never_be_one_refuses_at_the_store[---]`

Old text:

```
        or not any(char.isalnum() for char in text)

```

New text:

```
(empty)
```

### `u178.G3_genre_one_line`

check_genre: drop the control character rule, so a genre with a newline is stored

- File: `src/cratekit/label/registry.py`
- Source: `u178.json`, row `G3_genre_one_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_label_genre_gate.py`, `tests/test_label_workers.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_genre_that_could_never_be_one_refuses_at_the_store[Romi\nnimal]`

Old text:

```
        or any(unicodedata.category(char).startswith("C") for char in text)

```

New text:

```
(empty)
```

### `u178.G4_edit_clear_genre`

edit: ignore clear_genre, so --genre default on set keeps the genre

- File: `src/cratekit/label/registry.py`
- Source: `u178.json`, row `G4_edit_clear_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_label_genre_gate.py`, `tests/test_label_workers.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_the_word_default_clears_a_genre_and_none_keeps_it`

Old text:

```
                genre=None if clear_genre else (genre if genre is not None else existing.genre),
```

New text:

```
                genre=genre if genre is not None else existing.genre,
```

### `u178.G5_edit_none_keeps_genre`

edit: a genre of None drops the held genre, so an unrelated edit clears it

- File: `src/cratekit/label/registry.py`
- Source: `u178.json`, row `G5_edit_none_keeps_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_label_genre_gate.py`, `tests/test_label_workers.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_the_word_default_clears_a_genre_and_none_keeps_it`

Old text:

```
                genre=None if clear_genre else (genre if genre is not None else existing.genre),
```

New text:

```
                genre=None if clear_genre else genre,
```

### `u278.M10_window_short`

_expires: a minute leaves the window an hour after it STARTS, sixty seconds early

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M10_window_short`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`
- Collected: 177 against a baseline of 177
- Kills: 4 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_call_at_the_line_is_not_sent_and_names_the_spend_and_when_it_frees`
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer`
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
- Kills: 21 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_call_at_the_line_is_not_sent_and_names_the_spend_and_when_it_frees`
  - `tests/test_provider_budget.py::test_a_call_made_under_a_redirected_state_directory_is_counted_by_the_live_gate`
  - `tests/test_provider_budget.py::test_a_cooldown_still_refuses_first_and_keeps_its_own_reason`
  - `tests/test_provider_budget.py::test_a_minute_from_the_future_on_the_app_credentials_is_settled_too`
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer`
  - `tests/test_provider_budget.py::test_a_raised_ceiling_never_spends_the_reserve`
  - `tests/test_provider_budget.py::test_a_read_dispatched_inside_a_write_runs_under_the_read_line`
  - `tests/test_provider_budget.py::test_a_read_stops_at_the_reserve_while_a_go_still_runs`
  - `tests/test_provider_budget.py::test_a_sweep_whose_estimate_crosses_into_the_reserve_refuses_before_its_first_call`
  - `tests/test_provider_budget.py::test_a_verb_dispatched_again_inside_a_scope_runs_under_its_own_class`
  - `tests/test_provider_budget.py::test_a_write_verb_running_a_read_mode_is_held_to_the_read_line`
  - `tests/test_provider_budget.py::test_an_hour_raised_in_the_environment_reaches_a_call_outside_any_scope`
  - `tests/test_provider_budget.py::test_calls_up_to_the_budget_on_a_read_still_stops_at_the_reserve`
  - `tests/test_provider_budget.py::test_doctor_shows_each_identitys_spend_against_its_line_and_the_reserve`
  - `tests/test_provider_budget.py::test_one_identity_at_its_line_leaves_the_other_open`
  - ... and 6 more, see the JSON sidecar

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
  - `tests/test_provider_budget.py::test_calls_past_the_budget_is_refused_before_a_verb_that_makes_no_call_runs`
  - `tests/test_provider_budget.py::test_the_continue_a_parked_job_prints_is_not_refused_by_its_own_calls`

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
  - `tests/test_provider_budget.py::test_a_minute_from_the_future_on_the_app_credentials_is_settled_too`
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer`

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
  - `tests/test_provider_budget.py::test_a_minute_from_the_future_on_the_app_credentials_is_settled_too`
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer`
  - `tests/test_provider_budget.py::test_a_raised_ceiling_never_spends_the_reserve`
  - `tests/test_provider_budget.py::test_a_read_dispatched_inside_a_write_runs_under_the_read_line`
  - `tests/test_provider_budget.py::test_a_read_stops_at_the_reserve_while_a_go_still_runs`
  - `tests/test_provider_budget.py::test_a_write_verb_running_a_read_mode_is_held_to_the_read_line`
  - `tests/test_provider_budget.py::test_an_hour_raised_in_the_environment_reaches_a_call_outside_any_scope`
  - `tests/test_provider_budget.py::test_calls_up_to_the_budget_on_a_read_still_stops_at_the_reserve`
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
- Kills: 23 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_call_at_the_line_is_not_sent_and_names_the_spend_and_when_it_frees`
  - `tests/test_provider_budget.py::test_a_call_made_under_a_redirected_state_directory_is_counted_by_the_live_gate`
  - `tests/test_provider_budget.py::test_a_cooldown_still_refuses_first_and_keeps_its_own_reason`
  - `tests/test_provider_budget.py::test_a_minute_from_the_future_on_the_app_credentials_is_settled_too`
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer`
  - `tests/test_provider_budget.py::test_a_raised_ceiling_never_spends_the_reserve`
  - `tests/test_provider_budget.py::test_a_read_dispatched_inside_a_write_runs_under_the_read_line`
  - `tests/test_provider_budget.py::test_a_read_stops_at_the_reserve_while_a_go_still_runs`
  - `tests/test_provider_budget.py::test_a_sweep_whose_estimate_crosses_into_the_reserve_refuses_before_its_first_call`
  - `tests/test_provider_budget.py::test_a_verb_dispatched_again_inside_a_scope_runs_under_its_own_class`
  - `tests/test_provider_budget.py::test_a_write_verb_running_a_read_mode_is_held_to_the_read_line`
  - `tests/test_provider_budget.py::test_an_hour_raised_in_the_environment_reaches_a_call_outside_any_scope`
  - `tests/test_provider_budget.py::test_calls_up_to_the_budget_on_a_read_still_stops_at_the_reserve`
  - `tests/test_provider_budget.py::test_doctor_shows_each_identitys_spend_against_its_line_and_the_reserve`
  - `tests/test_provider_budget.py::test_minutes_older_than_the_window_are_pruned_from_the_file`
  - ... and 8 more, see the JSON sidecar

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
  - `tests/test_provider_budget.py::test_a_minute_from_the_future_on_the_app_credentials_is_settled_too`
  - `tests/test_provider_budget.py::test_one_identity_at_its_line_leaves_the_other_open`

Old text:

```
                spent = state.spent(identity, now)
```

New text:

```
                spent = state.spent(ACCOUNT, now)
```

### `u119-b.G12r_removed_namesake_written_into`

_playlist_row: a removed Favorites of the name under the folder is written into

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119-b.json`, row `G12r_removed_namesake_written_into`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 45 against a baseline of 45
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_removed_favorites_under_the_folder_is_not_written_into`

Old text:

```
    for row in list(db.get_playlist(Name=folder.playlist_display)):
        if rb_writer.is_folder(row) or rb_writer.node_removed(row):
            continue
```

New text:

```
    for row in list(db.get_playlist(Name=folder.playlist_display)):
        if rb_writer.is_folder(row):
            continue
```

### `u119-b.G5r_favorites_counted_as_members`

plan_refresh: the folder's own Favorites counts among the folder's members

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119-b.json`, row `G5r_favorites_counted_as_members`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 45 against a baseline of 45
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_favourite_sitting_only_in_favorites_after_leaving_its_band_is_removed`

Old text:

```
            if favorites_node is not None and node.playlist_id == favorites_node.playlist_id:
                continue
            members.update(node.content_ids)
```

New text:

```
            members.update(node.content_ids)
```

### `u119-c.C2_torn_bucket_bound_anyway`

plan_refresh: a bucket whose record names two live folders is bound to the first

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119-c.json`, row `C2_torn_bucket_bound_anyway`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 45 against a baseline of 45
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_bucket_is_bound_by_its_band_entries_before_its_favorites_entry`

Old text:

```
        if bucket.id in recorded_folder and bucket.id not in torn
    }
```

New text:

```
        if bucket.id in recorded_folder
    }
```

### `u119-c.C5_interruption_unreported`

apply_refresh: a failure after the additions landed is raised bare, the additions unreported

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119-c.json`, row `C5_interruption_unreported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 45 against a baseline of 45
- Kills: 3 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_removal_that_fails_after_the_additions_landed_says_what_landed`
  - `tests/test_genre_favorites.py::test_the_additive_half_carries_the_additions_when_interrupted_past_them`
  - `tests/test_genre_favorites.py::test_the_verb_reports_an_interrupted_refresh_with_the_additions_that_committed`

Old text:

```
        except Exception as exc:
            raise RefreshInterrupted(landed) from exc
```

New text:

```
        except Exception:
            raise
```

### `u119.G10_placements_no_gap`

placements: a source that cannot be read names no dimension as not compared

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G10_placements_no_gap`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 45 against a baseline of 45
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_check_with_no_source_leaves_the_recorded_favorites_out_and_names_the_gap`
  - `tests/test_genre_favorites.py::test_the_favourites_become_declared_placements_and_a_missing_source_a_gap`

Old text:

```
        return (), (FAVORITES_DIMENSION,)
```

New text:

```
        return (), ()
```

### `u119.G11_stale_digest`

apply_refresh: a plan whose digest moved since the approval is written anyway

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G11_stale_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 45 against a baseline of 45
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_plan_that_moved_between_the_approval_and_the_write_is_refused`
  - `tests/test_genre_favorites.py::test_the_digest_moves_when_a_track_is_dragged_into_favorites_between_the_acts`

Old text:

```
    if again.digest != plan.digest:
        raise refuse(
            "decision-stale",
            "the genre Favorites are not as the approved plan read them
```

New text:

```
    if False:
        raise refuse(
            "decision-stale",
            "the genre Favorites are not as the approved plan read them
```

### `u119.G13_removals_when_not_asked`

apply_refresh: the removals are made whether or not the caller was approved for them

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G13_removals_when_not_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 45 against a baseline of 45
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_the_additive_half_adds_and_counts_what_it_leaves_owed`
  - `tests/test_genre_favorites.py::test_the_digest_covers_the_target_and_stands_still_across_a_partial_apply`

Old text:

```
        if remove and owed:
```

New text:

```
        if owed:
```

### `u119.G15_removal_commit_admits_nothing`

apply_refresh: the second commit does not admit the membership table

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G15_removal_commit_admits_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 45 against a baseline of 45
- Kills: 5 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_favourite_sitting_only_in_favorites_after_leaving_its_band_is_removed`
  - `tests/test_genre_favorites.py::test_a_hand_added_track_not_in_all_favorites_is_removed_at_the_refresh`
  - `tests/test_genre_favorites.py::test_a_track_that_leaves_all_favorites_leaves_its_genre_favorites_and_keeps_its_band`
  - `tests/test_genre_favorites.py::test_no_content_row_tempo_or_rating_is_written`
  - `tests/test_genre_favorites.py::test_the_verb_asks_its_explicit_gate_then_adds_and_removes_and_reads_back`

Old text:

```
                    rb_writer.commit_guarded(db, removals=(rb_writer.MEMBERSHIP_TABLE,))
```

New text:

```
                    rb_writer.commit_guarded(db)
```

### `u119.G1_class_undeclared`

require_class: a taxonomy with no playlist class is not refused

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G1_class_undeclared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 45 against a baseline of 45
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_taxonomy_declaring_no_playlist_class_refuses_by_name`
  - `tests/test_genre_favorites.py::test_the_verb_refuses_an_undeclared_class_by_name`

Old text:

```
    found = favorites_class(declared)
    if found is None:
        raise refuse(
            CLASS_UNDECLARED,
```

New text:

```
    found = favorites_class(declared)
    if False:
        raise refuse(
            CLASS_UNDECLARED,
```

### `u119.G4_removed_membership_live`

_live_members: a membership rekordbox removed still counts as held

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G4_removed_membership_live`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 45 against a baseline of 45
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_track_that_leaves_all_favorites_leaves_its_genre_favorites_and_keeps_its_band`

Old text:

```
        if not rb_writer.membership_removed(song)
    )
```

New text:

```
    )
```

### `u119.G6_wanted_is_members`

plan_refresh: every member of the folder is wanted, favourite or not

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G6_wanted_is_members`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 45 against a baseline of 45
- Kills: 13 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_hand_added_track_not_in_all_favorites_is_removed_at_the_refresh`
  - `tests/test_genre_favorites.py::test_a_plan_that_moved_between_the_approval_and_the_write_is_refused`
  - `tests/test_genre_favorites.py::test_a_removal_that_fails_after_the_additions_landed_says_what_landed`
  - `tests/test_genre_favorites.py::test_a_source_that_went_between_the_two_acts_is_refused_by_the_gate`
  - `tests/test_genre_favorites.py::test_a_track_that_leaves_all_favorites_leaves_its_genre_favorites_and_keeps_its_band`
  - `tests/test_genre_favorites.py::test_a_vocal_favourite_is_in_its_band_with_vox_and_favorites_under_one_genre`
  - `tests/test_genre_favorites.py::test_the_additive_half_adds_and_counts_what_it_leaves_owed`
  - `tests/test_genre_favorites.py::test_the_check_reports_a_favourite_missing_from_its_favorites_and_not_a_hand_added_one_as_foreign`
  - `tests/test_genre_favorites.py::test_the_digest_covers_the_target_and_stands_still_across_a_partial_apply`
  - `tests/test_genre_favorites.py::test_the_digest_moves_when_a_track_is_dragged_into_favorites_between_the_acts`
  - `tests/test_genre_favorites.py::test_the_favourites_become_declared_placements_and_a_missing_source_a_gap`
  - `tests/test_genre_favorites.py::test_the_verb_asks_its_explicit_gate_then_adds_and_removes_and_reads_back`
  - `tests/test_genre_favorites.py::test_the_verb_reports_an_interrupted_refresh_with_the_additions_that_committed`

Old text:

```
                wanted=tuple(sorted(members & favourites)),
```

New text:

```
                wanted=tuple(sorted(members)),
```

### `u119.G7_twin_folders_first_taken`

plan_refresh: two folders of one bucket's name, the first is taken

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G7_twin_folders_first_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 45 against a baseline of 45
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_folder_nobody_declares_and_a_name_two_folders_carry_are_left_alone`

Old text:

```
        if len(named) > 1:
            unclaimed.extend(
```

New text:

```
        if len(named) > 9:
            unclaimed.extend(
```

### `u119.G9_digest_over_adds`

identity: the digest covers the adds rather than the target

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G9_digest_over_adds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 45 against a baseline of 45
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_the_digest_covers_the_target_and_stands_still_across_a_partial_apply`

Old text:

```
            "wanted": list(self.wanted),
            "removes": list(self.removes),
```

New text:

```
            "wanted": list(self.adds),
            "removes": list(self.removes),
```

### `u185.R4_genre_source`

source_playlist: count a playlist of the source's name inside the folder

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u185.json`, row `R4_genre_source`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 45 against a baseline of 45
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_source_namesake_inside_deadca7s_folder_is_not_a_second_source`

Old text:

```
    live = foreign_tree.outside(live, list(db.get_playlist()))
```

New text:

```
    live = list(live)
```

### `u119.V1_ack_after_plan`

favorites_refresh: the backup acknowledgment is not read before the gate

- File: `src/cratekit/favorites/refresh_cli.py`
- Source: `u119.json`, row `V1_ack_after_plan`
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

    plan = planned(cfg, declared, registry)
```

New text:

```
    plan = planned(cfg, declared, registry)
```

### `u239.L01_remember_land_only`

_remember: record a gate stop at any step as the landing, so a restamp gate is taken for it

- File: `src/cratekit/cli/label_sync.py`
- Source: `u239.json`, row `L01_remember_land_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 275 against a baseline of 275
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_stop_at_a_gate_before_the_landing_records_no_landing_and_the_next_go_runs_the_tail`

Old text:

```
    if not (stop.step == tail.LAND and stop.cause.reason == tail.GATE_STOP and landed):
```

New text:

```
    if not (stop.cause.reason == tail.GATE_STOP and landed):
```

### `u239.L02_remember_owner`

_remember: record on whichever run ran the tail, the round one blocking shape

- File: `src/cratekit/cli/label_sync.py`
- Source: `u239.json`, row `L02_remember_owner`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 275 against a baseline of 275
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_fresh_go_that_landed_another_runs_download_records_it_on_that_run`
  - `tests/test_label_sync_go.py::test_a_landing_another_runs_record_cannot_keep_is_a_warning_and_the_go_still_ends_at_it`

Old text:

```
    if owner == ctx.run.run_id:
```

New text:

```
    if True:
```

### `u239.L03_remember_called`

label_sync: never record the landing, so a later go runs the tail again

- File: `src/cratekit/cli/label_sync.py`
- Source: `u239.json`, row `L03_remember_called`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 275 against a baseline of 275
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_fresh_go_that_landed_another_runs_download_records_it_on_that_run`
  - `tests/test_label_sync_go.py::test_a_go_that_ran_its_tail_once_names_its_landing_when_run_again`
  - `tests/test_label_sync_go.py::test_a_go_whose_tail_reached_its_landing_names_that_landing_and_runs_nothing_again`
  - `tests/test_label_sync_go.py::test_a_landing_another_runs_record_cannot_keep_is_a_warning_and_the_go_still_ends_at_it`
  - `tests/test_label_sync_go.py::test_a_stop_at_a_gate_before_the_landing_records_no_landing_and_the_next_go_runs_the_tail`
  - `tests/test_label_sync_go.py::test_a_walk_under_a_landed_run_that_records_an_answer_is_not_a_no_op`

Old text:

```
        warnings.extend(_remember(ctx, stop, land))
```

New text:

```
        pass
```

### `u239.L05_commands_added`

_with_commands: never name the tail commands on the go's refusal

- File: `src/cratekit/cli/label_sync.py`
- Source: `u239.json`, row `L05_commands_added`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 275 against a baseline of 275
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_landed_while_the_fresh_go_downloaded_refuses_its_tail`
  - `tests/test_label_sync_go.py::test_a_later_gos_download_in_the_same_folder_refuses_the_tail_and_names_its_commands`
  - `tests/test_label_sync_go.py::test_a_plain_download_into_the_folder_refuses_the_runs_own_tail`

Old text:

```
    land = _land_in(cause.detail) if _GO_ORIGIN in cause.origin else None
```

New text:

```
    land = None
```

### `u239.L06_unrecorded_warning`

_remember: drop the warning when another run's record cannot keep the landing

- File: `src/cratekit/cli/label_sync.py`
- Source: `u239.json`, row `L06_unrecorded_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 275 against a baseline of 275
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_landing_another_runs_record_cannot_keep_is_a_warning_and_the_go_still_ends_at_it`

Old text:

```
    except Exception as exc:  # noqa: BLE001 - see below
```

New text:

```
    except ZeroDivisionError as exc:  # noqa: BLE001 - see below
```

### `r1467.M19_root_unreadable_refuses`

pass_landed: read a library root that cannot be read as a pass that never landed

- File: `src/cratekit/intake/land_cli.py`
- Source: `r1467.json`, row `M19_root_unreadable_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 275 against a baseline of 275
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_an_unreadable_library_root_refuses_rather_than_read_the_pass_as_landed`

Old text:

```
    except OSError as exc:
        raise refuse(
            "library-root-unreachable",
```

New text:

```
    except OSError as exc:
        return False
        raise refuse(
            "library-root-unreachable",
```

### `r1467.M20_retired_file_proves`

pass_landed: read only a pending intake file, so a retired one proves nothing

- File: `src/cratekit/intake/land_cli.py`
- Source: `r1467.json`, row `M20_retired_file_proves`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 275 against a baseline of 275
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_retired_intake_file_proves_the_pass`

Old text:

```
            if unretired_name(entry.name) == wanted and entry.is_file():
```

New text:

```
            if entry.name == wanted and entry.is_file():
```

### `r1467.M21_native_record_proves`

pass_landed: never read the native landing's record

- File: `src/cratekit/intake/land_cli.py`
- Source: `r1467.json`, row `M21_native_record_proves`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 275 against a baseline of 275
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_track_no_download_names_refuses_the_fresh_go_and_only_an_unproven_go_is_named[native]`

Old text:

```
    return bool(native.landings_of_pass(cfg, name))
```

New text:

```
    return False
```

### `r1467.M22_proof_is_a_file`

pass_landed: a directory named as the intake file proves the pass

- File: `src/cratekit/intake/land_cli.py`
- Source: `r1467.json`, row `M22_proof_is_a_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 275 against a baseline of 275
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_landing_proof_of_another_pass_proves_nothing`

Old text:

```
            if unretired_name(entry.name) == wanted and entry.is_file():
```

New text:

```
            if unretired_name(entry.name) == wanted:
```

### `r799-c.V1_the_gate_is_asked_before_the_write`

verb: apply the plan whatever the gate answers

- File: `src/cratekit/tagging/remap_cli.py`
- Source: `r799-c.json`, row `V1_the_gate_is_asked_before_the_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 15 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_file_changed_after_the_answer_makes_the_decision_stale`
  - `tests/test_tag_remap.py::test_a_file_outside_the_library_is_said_and_not_listed`
  - `tests/test_tag_remap.py::test_a_person_reads_the_counts_and_the_pairs_at_the_gate`
  - `tests/test_tag_remap.py::test_a_record_that_could_not_be_parsed_is_said`
  - `tests/test_tag_remap.py::test_a_refusal_that_rewrote_nothing_does_not_send_a_person_to_the_row_verb`
  - `tests/test_tag_remap.py::test_a_run_that_leaves_a_file_says_how_many_and_why_on_every_path`
  - `tests/test_tag_remap.py::test_a_run_that_wrote_still_says_what_it_left`
  - `tests/test_tag_remap.py::test_a_write_that_does_not_take_refuses_after_the_rest_were_written`
  - `tests/test_tag_remap.py::test_an_abort_writes_nothing`
  - `tests/test_tag_remap.py::test_an_active_taxonomy_with_no_table_says_so_and_plans_nothing`
  - `tests/test_tag_remap.py::test_an_approved_plan_is_written_and_the_run_names_the_verb_the_rows_follow_by`
  - `tests/test_tag_remap.py::test_an_empty_plan_still_asks_and_then_writes_nothing`
  - `tests/test_tag_remap.py::test_the_gate_takes_no_inline_answer`
  - `tests/test_tag_remap.py::test_the_shipped_template_declares_the_table_so_the_warning_is_not_given`
  - `tests/test_tag_remap.py::test_the_verb_asks_before_it_writes_and_the_gate_shows_the_plan`

Old text:

```
    if ctx.gate.require(spec, plan=data, context=_facts(plan)) != "apply":
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=_advisories(plan))
```

New text:

```
(empty)
```

### `r799-c.V2_a_file_that_did_not_take_refuses`

verb: answer a clean run over a file that did not take its genre

- File: `src/cratekit/tagging/remap_cli.py`
- Source: `r799-c.json`, row `V2_a_file_that_did_not_take_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 7 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_refusal_that_rewrote_nothing_does_not_send_a_person_to_the_row_verb`
  - `tests/test_tag_remap.py::test_a_write_that_does_not_take_refuses_after_the_rest_were_written`
  - `tests/test_tag_remap.py::test_each_way_a_file_did_not_take_its_genre_refuses_and_says_which[failed-could not be written and are untouched]`
  - `tests/test_tag_remap.py::test_each_way_a_file_did_not_take_its_genre_refuses_and_says_which[moved-carried something else]`
  - `tests/test_tag_remap.py::test_each_way_a_file_did_not_take_its_genre_refuses_and_says_which[unrecorded-no record of the rewrite could be committed]`
  - `tests/test_tag_remap.py::test_each_way_a_file_did_not_take_its_genre_refuses_and_says_which[wrong-do not read back]`
  - `tests/test_tag_remap.py::test_the_refusal_names_a_few_files_and_carries_them_all`

Old text:

```
    if written.clean:
        return
    parts = []
```

New text:

```
    if True:
        return
    parts = []
```

### `r799-b.P1_a_file_is_planned_only_while_it_carries_what_a_record_wrote`

plan: take every record in force as explaining the file, whatever the file carries

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-b.json`, row `P1_a_file_is_planned_only_while_it_carries_what_a_record_wrote`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 15 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_blank_file_whose_word_is_now_declined_is_not_read_as_agreeing`
  - `tests/test_tag_remap.py::test_a_file_holding_a_second_genre_is_left_alone_and_both_are_shown`
  - `tests/test_tag_remap.py::test_a_file_whose_genre_was_cleared_is_left_alone_and_not_read_as_agreeing`
  - `tests/test_tag_remap.py::test_a_genre_a_record_shop_wrote_later_on_a_path_the_catalogue_once_wrote_agrees`
  - `tests/test_tag_remap.py::test_a_genre_frame_holding_two_values_is_two_values_on_an_id3_container`
  - `tests/test_tag_remap.py::test_a_genre_nobody_recorded_writing_is_left_alone_and_listed[Deep House]`
  - `tests/test_tag_remap.py::test_a_genre_nobody_recorded_writing_is_left_alone_and_listed[Pop]`
  - `tests/test_tag_remap.py::test_a_genre_nobody_recorded_writing_is_left_alone_and_listed[dance / pop]`
  - `tests/test_tag_remap.py::test_a_genre_put_back_by_hand_after_a_rewrite_is_left_alone`
  - `tests/test_tag_remap.py::test_a_record_shops_genre_is_never_resolved_as_the_catalogues_word`
  - `tests/test_tag_remap.py::test_a_run_that_leaves_a_file_says_how_many_and_why_on_every_path`
  - `tests/test_tag_remap.py::test_a_run_that_wrote_still_says_what_it_left`
  - `tests/test_tag_remap.py::test_every_file_is_counted_once_and_the_items_are_in_path_order`
  - `tests/test_tag_remap.py::test_only_a_planned_write_is_written`
  - `tests/test_tag_remap.py::test_the_apply_writes_the_planned_genre_and_no_other_file`

Old text:

```
    explaining = [record for record in in_force if values == (record.written,)]
```

New text:

```
    explaining = list(in_force)
```

### `r799-b.P2_two_explanations_are_ambiguous`

plan: settle a genre two records explain differently by the first of them

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-b.json`, row `P2_two_explanations_are_ambiguous`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_file_reached_through_a_link_is_the_file`
  - `tests/test_tag_remap.py::test_a_genre_two_records_explain_with_different_sources_is_left`
  - `tests/test_tag_remap.py::test_a_genre_two_records_explain_with_different_words_is_left`
  - `tests/test_tag_remap.py::test_one_file_recorded_under_two_spellings_is_one_file`

Old text:

```
    if len({(record.source, record.word) for record in explaining}) > 1:
```

New text:

```
    if False:
```

### `r799-b.P3_a_shops_genre_is_the_shops`

plan: resolve a record shop's word as the general catalogue's

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-b.json`, row `P3_a_shops_genre_is_the_shops`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_record_shops_genre_is_never_resolved_as_the_catalogues_word`

Old text:

```
    if wrote.source != SOURCE:
```

New text:

```
    if False:
```

### `r799-b.P4_a_rewrite_retires_the_record_it_replaced`

plan: keep every record of the source in force, whatever its generation

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-b.json`, row `P4_a_rewrite_retires_the_record_it_replaced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_genre_put_back_by_hand_after_a_rewrite_is_left_alone`
  - `tests/test_tag_remap.py::test_a_word_given_its_first_genre_back_is_still_followed`

Old text:

```
        if record.source == SOURCE and record.generation == newest
    ]
```

New text:

```
        if record.source == SOURCE
    ]
```

### `r799-b.P5_only_a_file_under_the_library_is_opened`

plan: settle a recorded path wherever it is

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-b.json`, row `P5_only_a_file_under_the_library_is_opened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_file_outside_the_library_is_said_and_not_listed`
  - `tests/test_tag_remap.py::test_a_file_outside_this_librarys_root_is_counted_and_never_opened`
  - `tests/test_tag_remap.py::test_a_folder_named_in_another_case_on_a_volume_that_folds_case_is_inside`
  - `tests/test_tag_remap.py::test_a_path_that_climbs_out_of_the_library_is_outside_it`

Old text:

```
        if resolved is None or not _inside(resolved, library):
```

New text:

```
        if resolved is None:
```

### `r799-b.P6_one_file_is_one_group`

plan: key a file under the library by its resolved name and not by the file itself

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-b.json`, row `P6_one_file_is_one_group`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    try:
        stat = resolved.stat()
    except OSError:
        return ("name", str(resolved))
    return ("file", stat.st_dev, stat.st_ino)
```

New text:

```
    return ("name", str(resolved))
```

### `r799-b.W2_the_writers_answer_is_kept`

apply: count a file the writer could not write as written

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-b.json`, row `W2_the_writers_answer_is_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_file_the_writer_could_not_write_is_named_as_untouched_and_the_rest_are_written`
  - `tests/test_tag_remap.py::test_a_refusal_that_rewrote_nothing_does_not_send_a_person_to_the_row_verb`
  - `tests/test_tag_remap.py::test_a_write_that_does_not_take_refuses_after_the_rest_were_written`

Old text:

```
        if not tags.write_genre(target, item.wanted):
            failed.append(item.path)
            continue
```

New text:

```
        tags.write_genre(target, item.wanted)
```

### `r799-c.P11_blank_is_not_agreement`

plan: read a blank file whose word is given nothing as agreeing

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-c.json`, row `P11_blank_is_not_agreement`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_blank_file_whose_word_is_now_declined_is_not_read_as_agreeing`

Old text:

```
        if any(current and current == _wanted(declared, record.word) for record in mine):
```

New text:

```
        if any(current == _wanted(declared, record.word) for record in mine):
```

### `r799-c.V3_an_unrecorded_rewrite_is_not_clean`

verb: call a run clean whose rewrite could not be recorded

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-c.json`, row `V3_an_unrecorded_rewrite_is_not_clean`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_record_that_cannot_be_committed_is_named_and_the_file_stays_rewritten`
  - `tests/test_tag_remap.py::test_each_way_a_file_did_not_take_its_genre_refuses_and_says_which[unrecorded-no record of the rewrite could be committed]`

Old text:

```
        return not (self.wrong or self.moved or self.failed or self.unrecorded)
```

New text:

```
        return not (self.wrong or self.moved or self.failed)
```

### `r799-c.W4_a_rewrite_is_recorded`

apply: commit no record of a rewrite, so the verb's own write reads as a hand edit

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-c.json`, row `W4_a_rewrite_is_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 5 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_file_this_verb_rewrote_is_corrected_again_when_the_word_moves_again`
  - `tests/test_tag_remap.py::test_a_genre_put_back_by_hand_after_a_rewrite_is_left_alone`
  - `tests/test_tag_remap.py::test_a_record_that_cannot_be_committed_is_named_and_the_file_stays_rewritten`
  - `tests/test_tag_remap.py::test_a_rewrite_is_recorded_as_a_tagging_record_of_its_own`
  - `tests/test_tag_remap.py::test_a_word_given_its_first_genre_back_is_still_followed`

Old text:

```
        if not _record(cfg, name, ordinal, item):
            unrecorded.append(item.path)
```

New text:

```
(empty)
```

### `r799-c.W5_a_rewrites_record_is_one_generation_on`

apply: record a rewrite at the generation of the record it replaced

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-c.json`, row `W5_a_rewrites_record_is_one_generation_on`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_file_this_verb_rewrote_is_corrected_again_when_the_word_moves_again`
  - `tests/test_tag_remap.py::test_a_genre_put_back_by_hand_after_a_rewrite_is_left_alone`
  - `tests/test_tag_remap.py::test_a_rewrite_is_recorded_as_a_tagging_record_of_its_own`
  - `tests/test_tag_remap.py::test_a_word_given_its_first_genre_back_is_still_followed`

Old text:

```
                "generation": item.generation + 1,
```

New text:

```
                "generation": item.generation,
```

### `u52-item-derivation.H2_listing_passthrough_gone`

REMOVE THE LAYER ALONE: an adapter's own CratekitError refusal is rewritten as an unreadable playlist

- File: `src/cratekit/label/cli.py`
- Source: `u52-item-derivation.json`, row `H2_listing_passthrough_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 262 against a baseline of 262
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_cratekit_refusal_from_below_is_not_flattened_into_an_unreadable_playlist`

Old text:

```
    except CratekitError:
        raise
    except Exception as exc:
        raise refuse(
            "label-playlist-unreadable",
            f"the playlist {reference!r} could not be listed by the provider "
```

New text:

```
    except Exception as exc:
        raise refuse(
            "label-playlist-unreadable",
            f"the playlist {reference!r} could not be listed by the provider "
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

### `u52-item-derivation.H7_unresolved_drops_nameless`

Count only the names a catalogue refused, so a playlist whose tracks carry no copyright string at all reports a clean zero unresolved

- File: `src/cratekit/label/cli.py`
- Source: `u52-item-derivation.json`, row `H7_unresolved_drops_nameless`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 262 against a baseline of 262
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_track_with_no_copyright_string_is_counted_rather_than_dropped_silently`

Old text:

```
    unresolved = len(report.dropped) + nameless
```

New text:

```
    unresolved = len(report.dropped)
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

### `u52-item-derivation.S1_errors_branch_gone`

A sweep that could not offer some of the releases it listed exits 0 and reports the job done

- File: `src/cratekit/label/cli.py`
- Source: `u52-item-derivation.json`, row `S1_errors_branch_gone`
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
        raise refuse(
            "label-sweep-incomplete",
```

New text:

```
    if False:
        raise refuse(
            "label-sweep-incomplete",
```

### `u52-zero-rows.H5_verifier_passthrough_gone`

REMOVE THE LAYER ALONE: the verification boundary swallows an adapter's own refusal into label-playlist-unreadable

- File: `src/cratekit/label/cli.py`
- Source: `u52-zero-rows.json`, row `H5_verifier_passthrough_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 262 against a baseline of 262
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_refusal_the_harvest_verifier_raises_in_kind_keeps_its_own_reason`

Old text:

```
        except CratekitError:
            raise
        except Exception as exc:
```

New text:

```
        except Exception as exc:
```

### `r662-a.M2_spelled_path_compared_whole`

the spelled remote is compared whole rather than by its name, so gdrive: beside gdrive destinations reads as a disagreement

- File: `src/cratekit/core/config.py`
- Source: `r662-a.json`, row `M2_spelled_path_compared_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`
- Collected: 658 against a baseline of 658
- Kills: 2 (killed)
- Killed:
  - `tests/test_config.py::test_a_spelled_backup_remote_that_matches_the_destinations_is_kept[gdrive:]`
  - `tests/test_config.py::test_a_spelled_backup_remote_that_matches_the_destinations_is_kept[gdrive:bucket]`

Old text:

```
    if remote.split(":", 1)[0] == expected:
        return None
    return remote, expected
```

New text:

```
    if remote == expected:
        return None
    return remote, expected
```

### `r662-a.M4_validator_drops_disagreement`

the validator no longer reports a spelled remote the destinations disagree with

- File: `src/cratekit/core/config.py`
- Source: `r662-a.json`, row `M4_validator_drops_disagreement`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`
- Collected: 658 against a baseline of 658
- Kills: 7 (killed)
- Killed:
  - `tests/test_config.py::test_a_spelled_backup_remote_that_names_another_remote_is_refused`
  - `tests/test_doctor.py::test_a_spelled_remote_is_kept_unless_rclone_was_read_and_lacks_it[rclone-absent]`
  - `tests/test_doctor.py::test_a_spelled_remote_is_kept_unless_rclone_was_read_and_lacks_it[rclone-knows-it]`
  - `tests/test_doctor.py::test_a_spelled_remote_is_kept_unless_rclone_was_read_and_lacks_it[rclone-knows-neither]`
  - `tests/test_doctor.py::test_a_spelled_remote_is_kept_unless_rclone_was_read_and_lacks_it[rclone-unreadable]`
  - `tests/test_doctor.py::test_the_disagreeing_remote_refusal_names_the_flag_and_the_flag_repairs_it`
  - `tests/test_doctor.py::test_the_setup_token_stays_when_the_disagreement_is_not_the_only_problem`

Old text:

```
    disagreement = backup_remote_disagreement(data)
    if disagreement is not None:
```

New text:

```
    disagreement = backup_remote_disagreement(data)
    if False:
```

### `r662-a.M5_validator_message_loses_flag`

the validator's problem text no longer names the flag, reworded rather than truncated

- File: `src/cratekit/core/config.py`
- Source: `r662-a.json`, row `M5_validator_message_loses_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`
- Collected: 658 against a baseline of 658
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_disagreeing_remote_refusal_names_the_flag_and_the_flag_repairs_it`

Old text:

```
Setup's --backup-remote replaces the "
            f"spelled one (R-662)."
```

New text:

```
Setup can be run again to "
            f"change it (R-662)."
```

### `r662-b.M1b_several_remotes_compared`

M1 again after the round's test: destinations naming several remotes are compared against the spelled remote anyway

- File: `src/cratekit/core/config.py`
- Source: `r662-b.json`, row `M1b_several_remotes_compared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`
- Collected: 658 against a baseline of 658
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_no_disagreement_is_read_where_there_is_nothing_to_compare`

Old text:

```
    if len(named) != 1:
        return None
    expected = next(iter(named))
```

New text:

```
    if not named:
        return None
    expected = next(iter(named))
```

### `r662-b.M3b_blank_remote_disagrees`

M3 again after the round's test: a blank spelled remote is no longer treated as unset

- File: `src/cratekit/core/config.py`
- Source: `r662-b.json`, row `M3b_blank_remote_disagrees`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`
- Collected: 658 against a baseline of 658
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_no_disagreement_is_read_where_there_is_nothing_to_compare`

Old text:

```
    if not isinstance(remote, str) or not remote.strip():
        return None
    named = {
```

New text:

```
    if not isinstance(remote, str):
        return None
    named = {
```

### `r838-c.R1_library_bound`

mark_record._recognize: accept a record written for another library

- File: `src/cratekit/sync/mark_record.py`
- Source: `r838-c.json`, row `R1_library_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_an_unreadable_record_refuses_rather_than_reading_as_empty[{"version": 1, "library_id": "another-library", "marks": []}]`

Old text:

```
        if library_id != self.cfg.library.volume_id:
```

New text:

```
        if False:
```

### `r838-c.R2_remark_clears`

mark_record.record_marked: append a second entry for a re-mark by the same pass rather than replacing the first

- File: `src/cratekit/sync/mark_record.py`
- Source: `r838-c.json`, row `R2_remark_clears`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_mark_after_an_unmark_clears_the_stamp`

Old text:

```
                    if (entry.pass_name, entry.playlist_id) == (pass_name, playlist_id):
                        entries[index] = fresh
                        break
```

New text:

```
                    if False:
                        entries[index] = fresh
                        break
```

### `r838-d.R3b_stamp_target`

mark_record.record_unmarked: stamp the playlist's mark under any pass, so another pass's mark reads as put back

- File: `src/cratekit/sync/mark_record.py`
- Source: `r838-d.json`, row `R3b_stamp_target`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_later_mark_by_another_pass_owns_the_prefix`

Old text:

```
                if (entry.pass_name, entry.playlist_id) == (pass_name, playlist_id):
                    entries[index] = replace(entry, unmarked=when)
```

New text:

```
                if entry.playlist_id == playlist_id:
                    entries[index] = replace(entry, unmarked=when)
```

### `r838-a.U1_refuse_stranger`

unmark._narrowed: drop the refusal, so a playlist the pass never marked is silently passed over rather than refused

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-a.json`, row `U1_refuse_stranger`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_playlist_the_pass_never_marked_is_refused_whatever_its_title`

Old text:

```
    if strangers:
        raise _blocked(
```

New text:

```
    if False:
        raise _blocked(
```

### `r838-a.U3_pass_filter`

unmark: take every pass's marks as the named pass's, so a playlist the pass never marked is planned

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-a.json`, row `U3_pass_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_later_mark_by_another_pass_owns_the_prefix`
  - `tests/test_sync_unmark.py::test_a_pass_the_record_holds_nothing_for_is_a_gated_plan_of_nothing`

Old text:

```
        tuple(entry for entry in every if entry.pass_name == name),
```

New text:

```
        tuple(entry for entry in every),
```

### `r838-a.U4_already_unmarked_stamp`

unmark._item: ignore the unmarked stamp, so a second run is decided by the title alone

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-a.json`, row `U4_already_unmarked_stamp`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_second_run_plans_nothing_and_still_asks`

Old text:

```
    if entry.unmarked:
        return {
```

New text:

```
    if False:
        return {
```

### `r838-a.U5_marked_again`

unmark._item: ignore a later mark by another pass, so this pass's unmark takes off that pass's prefix

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-a.json`, row `U5_marked_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_later_mark_by_another_pass_owns_the_prefix`

Old text:

```
    later = _later(entry, every)
    if later:
```

New text:

```
    later = _later(entry, every)
    if False:
```

### `r838-a.U6_later_order`

unmark._later: an EARLIER mark by another pass also supersedes, so the latest pass's own unmark is refused

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-a.json`, row `U6_later_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_later_mark_by_another_pass_owns_the_prefix`

Old text:

```
        and other.marked > entry.marked
```

New text:

```
        and other.marked != entry.marked
```

### `r838-a.U8_title_already_back`

unmark._item: no already-put-back branch, so a title already restored is reported as retitled by hand

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-a.json`, row `U8_title_already_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_title_already_put_back_is_skipped_without_a_stamp`

Old text:

```
    if current == entry.name:
```

New text:

```
    if False:
```

### `r838-b.U10_digest_names`

unmark._payload: the digest omits the planned renames, so an answer to one plan carries out another

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-b.json`, row `U10_digest_names`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_an_answer_is_stale_once_the_account_moves`

Old text:

```
            (item["id"], item["marked_as"], item["to"])
            for item in items
            if item["action"] == UNMARK
```

New text:

```
            (item["id"], item["marked_as"], item["to"])
            for item in items
            if False
```

### `r838-b.U13_recheck`

unmark: no recheck against the second listing, so a title changed after the answer is renamed anyway

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-b.json`, row `U13_recheck`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_playlist_that_changes_between_the_plan_and_the_rename_is_said`

Old text:

```
            if now.get(identity) != entry.to:
```

New text:

```
            if False:
```

### `r838-b.U15_rename_target`

unmark: rename to the title the mark wrote rather than the one before it

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-b.json`, row `U15_rename_target`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_later_mark_by_another_pass_owns_the_prefix`
  - `tests/test_sync_unmark.py::test_a_pass_that_marked_three_plans_three_renames_back_and_applies_them`
  - `tests/test_sync_unmark.py::test_a_playlist_retitled_by_hand_since_the_mark_is_listed_and_left`
  - `tests/test_sync_unmark.py::test_a_playlist_that_changes_between_the_plan_and_the_rename_is_said`
  - `tests/test_sync_unmark.py::test_a_playlist_the_account_no_longer_lists_is_said_and_left`
  - `tests/test_sync_unmark.py::test_a_title_already_put_back_is_skipped_without_a_stamp`
  - `tests/test_sync_unmark.py::test_playlist_given_twice_narrows_to_both_marks_named`
  - `tests/test_sync_unmark.py::test_playlist_narrows_to_the_marks_named`

Old text:

```
            remote.rename_playlist(identity, entry.name)
```

New text:

```
            remote.rename_playlist(identity, entry.to)
```

### `r838-b.U16_part_way_names`

unmark._failed_part_way: report nothing put back, so a partial failure loses what landed

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-b.json`, row `U16_part_way_names`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_failure_part_way_names_what_was_put_back`

Old text:

```
        "unmarked": list(landed),
```

New text:

```
        "unmarked": [],
```

### `r838-b.U9_renamed_since`

unmark._item: plan any title carrying the prefix, so a playlist retitled by hand with the prefix kept is renamed

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-b.json`, row `U9_renamed_since`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_playlist_retitled_by_hand_since_the_mark_is_listed_and_left`

Old text:

```
    if current != entry.to:
        how =
```

New text:

```
    if not playlists.is_swept_name(current):
        how =
```

### `r838-c.U7b_not_listed_rerun`

U7 measured again after the not-listed test was added: no NOT_LISTED branch, so a playlist the account dropped falls through to the title comparison

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-c.json`, row `U7b_not_listed_rerun`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_playlist_the_account_no_longer_lists_is_said_and_left`

Old text:

```
    if current is None:
        return {
            **base,
            "action": SKIP,
            "reason": NOT_LISTED,
```

New text:

```
    if current is None and False:
        return {
            **base,
            "action": SKIP,
            "reason": NOT_LISTED,
```

### `r289-b.B1_reclaim_rmtree`

Reclaim with rmtree, so a refused landing kept as evidence is deleted

- File: `src/cratekit/acquire/cli.py`
- Source: `r289-b.json`, row `B1_reclaim_rmtree`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_intake_missing.py`, `tests/test_listdoc.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 398 against a baseline of 398
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_the_refused_landing_left_as_evidence_survives_the_sweep`
  - `tests/test_acquire_workers.py::test_the_sweep_does_not_report_a_directory_it_could_not_remove`

Old text:

```
    try:
        directory.rmdir()
    except OSError:
        return
    removed.append(directory)
```

New text:

```
    try:
        shutil.rmtree(directory)
    except OSError:
        return
    removed.append(directory)
```

### `r289-b.B3_terminal_filter_gone`

Sweep every job's staging, open ones included

- File: `src/cratekit/acquire/cli.py`
- Source: `r289-b.json`, row `B3_terminal_filter_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_intake_missing.py`, `tests/test_listdoc.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 398 against a baseline of 398
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_directory_naming_a_job_this_queue_does_not_hold_is_left_alone`
  - `tests/test_acquire_workers.py::test_an_open_jobs_staging_survives_the_sweep`

Old text:

```
        if states.get(job_dir.name) not in jobs.TERMINAL_STATES:
```

New text:

```
        if False:
```

### `r289-b.B4_unknown_job_read_as_terminal`

Read a directory naming a job this queue does not hold as finished

- File: `src/cratekit/acquire/cli.py`
- Source: `r289-b.json`, row `B4_unknown_job_read_as_terminal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_intake_missing.py`, `tests/test_listdoc.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 398 against a baseline of 398
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_directory_naming_a_job_this_queue_does_not_hold_is_left_alone`

Old text:

```
        if states.get(job_dir.name) not in jobs.TERMINAL_STATES:
```

New text:

```
        if states.get(job_dir.name, jobs.JobState.SUCCEEDED) not in jobs.TERMINAL_STATES:
```

### `r289-b.B5_job_directory_before_its_items`

Reclaim the job directory first, so its item directories never go

- File: `src/cratekit/acquire/cli.py`
- Source: `r289-b.json`, row `B5_job_directory_before_its_items`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_intake_missing.py`, `tests/test_listdoc.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 398 against a baseline of 398
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_the_emptied_staging_of_a_finished_job_is_reclaimed_by_the_next_run`
  - `tests/test_acquire_workers.py::test_the_sweep_reports_what_it_removed_deepest_first`

Old text:

```
        for item_dir in _children(job_dir):
            if item_dir.is_dir():
                _reclaim(item_dir, removed)
        _reclaim(job_dir, removed)
```

New text:

```
        _reclaim(job_dir, removed)
        for item_dir in _children(job_dir):
            if item_dir.is_dir():
                _reclaim(item_dir, removed)
```

### `r289-b.B6_job_directory_never_reclaimed`

Reclaim the item directories and leave the job directory behind

- File: `src/cratekit/acquire/cli.py`
- Source: `r289-b.json`, row `B6_job_directory_never_reclaimed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_intake_missing.py`, `tests/test_listdoc.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 398 against a baseline of 398
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_the_emptied_staging_of_a_finished_job_is_reclaimed_by_the_next_run`
  - `tests/test_acquire_workers.py::test_the_sweep_reports_what_it_removed_deepest_first`

Old text:

```
                _reclaim(item_dir, removed)
        _reclaim(job_dir, removed)
```

New text:

```
                _reclaim(item_dir, removed)
```

### `r289-b.C1_download_call_site`

Drop the sweep at the head of acquire download

- File: `src/cratekit/acquire/cli.py`
- Source: `r289-b.json`, row `C1_download_call_site`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_intake_missing.py`, `tests/test_listdoc.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 398 against a baseline of 398
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_the_emptied_staging_of_a_finished_job_is_reclaimed_by_the_next_run`

Old text:

```
        sweep_staging(Path(cfg.paths.download_staging), store)

```

New text:

```
(empty)
```

### `r289-c.B2r_reclaim_reports_a_failure_as_a_removal`

Report a directory that could not be removed as one that was

- File: `src/cratekit/acquire/cli.py`
- Source: `r289-c.json`, row `B2r_reclaim_reports_a_failure_as_a_removal`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_intake_missing.py`, `tests/test_listdoc.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 398 against a baseline of 398
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_the_sweep_does_not_report_a_directory_it_could_not_remove`

Old text:

```
    try:
        directory.rmdir()
    except OSError:
        return
    removed.append(directory)
```

New text:

```
    try:
        directory.rmdir()
    except OSError:
        pass
    removed.append(directory)
```

### `u219.G2_nothing_to_add`

route resort: queue a job over a plan with nothing to add

- File: `src/cratekit/write/routing_cli.py`
- Source: `u219.json`, row `G2_nothing_to_add`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_organize_mirror_edits.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 309 against a baseline of 309
- Kills: 1 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_resort_with_no_change_plans_nothing_and_queues_nothing`

Old text:

```
    if not adds:
        return ctx.envelope(
```

New text:

```
    if False:
        return ctx.envelope(
```

### `u219.G3_adds_frozen`

route resort: freeze an empty plan in the job, so the worker holds its write to nothing the gate showed

- File: `src/cratekit/write/routing_cli.py`
- Source: `u219.json`, row `G3_adds_frozen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_organize_mirror_edits.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 309 against a baseline of 309
- Kills: 21 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_library_that_moved_after_the_gate_refuses_before_writing`
  - `tests/test_resort_scope.py::test_a_resort_after_a_genre_sub_writes_nothing_under_the_intake_root`
  - `tests/test_resort_scope.py::test_a_resort_that_left_a_favourite_for_later_says_so`
  - `tests/test_resort_scope.py::test_a_resort_with_no_change_plans_nothing_and_queues_nothing`
  - `tests/test_resort_scope.py::test_a_resort_writes_no_favourite_its_gate_did_not_show`
  - `tests/test_resort_scope.py::test_the_favourite_a_resort_left_is_shown_and_filed_by_the_next`
  - `tests/test_resort_scope.py::test_two_files_that_swap_places_after_the_gate_refuse_by_their_paths`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[above-resort]`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[below-resort]`
  - `tests/test_routing_workers.py::test_a_driven_resume_over_no_favorites_class_names_the_skipped_step[resort]`
  - `tests/test_routing_workers.py::test_a_driven_resume_over_the_declared_class_says_nothing_of_it[resort]`
  - `tests/test_routing_workers.py::test_a_driven_resume_says_the_vocal_dimension_was_not_compared_beside_drift[resort]`
  - `tests/test_routing_workers.py::test_a_queued_rebuild_and_resort_run_on_an_encrypted_library[resort]`
  - `tests/test_routing_workers.py::test_a_queued_resort_runs_its_item_and_the_tree_holds_the_track`
  - `tests/test_routing_workers.py::test_a_rebuild_of_another_tree_says_nothing_of_the_routing_trees_favorites[resort]`
  - ... and 6 more, see the JSON sidecar

Old text:

```
                RESORT_ADDS_KEY: adds,
```

New text:

```
                RESORT_ADDS_KEY: [],
```

### `u219.G4_worker_own_tree`

handle_resort: hand the engine every tree's approved adds, not its own tree's

- File: `src/cratekit/write/routing_cli.py`
- Source: `u219.json`, row `G4_worker_own_tree`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_organize_mirror_edits.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 309 against a baseline of 309
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_each_worker_names_its_own_verb_and_rebuilds_the_item_it_was_handed`

Old text:

```
            if row.get("tree") == tree_id
```

New text:

```
            if row.get("tree") is not None
```

### `u219.G5_resume_run`

resort_argv: drop --run, so the spawned child meets the explicit gate with nothing recorded

- File: `src/cratekit/write/routing_cli.py`
- Source: `u219.json`, row `G5_resume_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_organize_mirror_edits.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 309 against a baseline of 309
- Kills: 1 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_the_resume_argv_names_the_gate_run`

Old text:

```
    resume = ["--run", str(gate_run)] if gate_run else []
    return [*resume, "route", "resort", "--job", job.job_id]
```

New text:

```
    resume = []
    return [*resume, "route", "resort", "--job", job.job_id]
```

### `u219.M3_due_again_said`

_due_again_warnings: count nothing due, so a resort that left a favourite for later reports a clean success (round two's third hold)

- File: `src/cratekit/write/routing_cli.py`
- Source: `u219.json`, row `M3_due_again_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_organize_mirror_edits.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 309 against a baseline of 309
- Kills: 1 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_resort_that_left_a_favourite_for_later_says_so`

Old text:

```
        count = int(report.get("due_again") or 0)
```

New text:

```
        count = 0
```

### `u219.R1_routed_trees`

_routed_trees: every native tree, so the resort queues the intake tree again

- File: `src/cratekit/write/routing_cli.py`
- Source: `u219.json`, row `R1_routed_trees`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_organize_mirror_edits.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 309 against a baseline of 309
- Kills: 12 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_library_that_moved_after_the_gate_refuses_before_writing`
  - `tests/test_resort_scope.py::test_a_resort_after_a_genre_sub_writes_nothing_under_the_intake_root`
  - `tests/test_resort_scope.py::test_a_resort_that_left_a_favourite_for_later_says_so`
  - `tests/test_resort_scope.py::test_a_resort_with_no_change_plans_nothing_and_queues_nothing`
  - `tests/test_resort_scope.py::test_a_resort_writes_no_favourite_its_gate_did_not_show`
  - `tests/test_resort_scope.py::test_an_abort_queues_nothing_and_writes_nothing`
  - `tests/test_resort_scope.py::test_an_answer_over_one_database_file_does_not_approve_another`
  - `tests/test_resort_scope.py::test_route_inbox_files_into_the_routing_tree_only`
  - `tests/test_resort_scope.py::test_the_digest_is_the_same_over_one_unchanged_library`
  - `tests/test_resort_scope.py::test_the_favourite_a_resort_left_is_shown_and_filed_by_the_next`
  - `tests/test_resort_scope.py::test_the_gate_shows_every_add_and_only_the_routing_trees`
  - `tests/test_resort_scope.py::test_two_files_that_swap_places_after_the_gate_refuse_by_their_paths`

Old text:

```
    return tuple(t for t in _native_trees(entries) if rebuild.derivable(declared, t))
```

New text:

```
    return _native_trees(entries)
```

### `u219.R2_inbox_routed_only`

plan_inbox: file the intake folder into every native tree, INBOX included

- File: `src/cratekit/write/routing_cli.py`
- Source: `u219.json`, row `R2_inbox_routed_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_organize_mirror_edits.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 309 against a baseline of 309
- Kills: 1 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_route_inbox_files_into_the_routing_tree_only`

Old text:

```
    native = _routed_trees(entries, declared)
```

New text:

```
    native = _native_trees(entries)
```

### `u219.R3_left_alone_named`

_passed_over: name no tree the resort left alone

- File: `src/cratekit/write/routing_cli.py`
- Source: `u219.json`, row `R3_left_alone_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_organize_mirror_edits.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 309 against a baseline of 309
- Kills: 1 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_the_gate_shows_every_add_and_only_the_routing_trees`

Old text:

```
    skipped = [t for t in _native_trees(entries) if t in others]
    if not skipped:
        return []
    named = ", ".join(f"{others[t]} ({t})" for t in skipped)
    return [
        {
            "code": TREE_NOT_DERIVED,
```

New text:

```
    skipped = [t for t in _native_trees(entries) if t in others]
    if skipped:
        return []
    named = ", ".join(f"{others[t]} ({t})" for t in skipped)
    return [
        {
            "code": TREE_NOT_DERIVED,
```

### `u149.T2_two_folders_not_refused`

find_folder: drop the refusal of two live top level folders of one year, so the first is written to

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T2_two_folders_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_an_existing_folder_is_reused_and_two_of_one_year_place_nothing`

Old text:

```
    if len(found) > 1:
```

New text:

```
    if len(found) > 2:
```

