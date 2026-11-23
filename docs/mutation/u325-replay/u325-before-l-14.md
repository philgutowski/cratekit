# Mutation table: u325-before-l-14

Measured by `scripts/mutate.py` on 2026-11-22 22:15 UTC, branch `HEAD` at `539638eb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22663 collected. pytest invocations for this batch: 138.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:15 UTC for commit `539638ebe629`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 17, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22663 against 22663. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u72.M1_abort_applies` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 48 | 3 | killed |
| `u72.M2_empty_plan_applied` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 48 | 2 | killed |
| `u72.M3_digest_drops_where` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 48 | 1 | killed |
| `u72.M5_digest_drops_export` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 48 | 2 | killed |
| `u72.M9_default_name_colons` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 48 | 1 | killed |
| `u72-b.M23_listing_unfiltered` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 48 | 1 | killed |
| `r791-b.C1_artifact_answers` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 240 | 15 | killed |
| `r791-b.C2_artifact_unread` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 240 | 6 | killed |
| `r791-b.C3_summary_counts_answers` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 240 | 15 | killed |
| `r791-b.C6_not_asked_excluded` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 240 | 1 | killed |
| `r791-b.C7_parse_break_said` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 240 | 1 | killed |
| `r791-b.C8_one_file` | `src/cratekit/tagging/cli.py` | maintainer | 3 file(s) | 240 | 1 | killed |
| `r791-b.C9_unread_skip_zero_filled` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 240 | 11 | killed |
| `r263.W1_no_unrecorded_state` | `src/cratekit/sync/watermarks.py` | user | 5 file(s) | 569 | 4 | killed |
| `r263.W2_state_word` | `src/cratekit/sync/watermarks.py` | user | 5 file(s) | 569 | 3 | killed |
| `r263.W3_stale_record_as_completion` | `src/cratekit/sync/watermarks.py` | user | 5 file(s) | 569 | 1 | killed |
| `r263.W4_stale_suffix` | `src/cratekit/sync/watermarks.py` | user | 5 file(s) | 569 | 1 | killed |
| `u284-composite.C3x_unread_discogs_and_outage_named` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 227 | 2 | killed |
| `u284.C1_tagged_file_named_refused` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 227 | 1 | killed |
| `u284.C2_outage_named_refused` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 227 | 2 | killed |
| `u284.C4_stop_never_collected` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 227 | 2 | killed |
| `u284.C5_sweep_stop_unsaid` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 227 | 1 | killed |
| `u284.C6_token_unsaid` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 227 | 3 | killed |
| `u284.C7_rejected_token_told_to_wait` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 227 | 1 | killed |
| `u217.K10_naive_instant` | `src/cratekit/label/kept_listing.py` | maintainer | 1 file(s) | 38 | 1 | killed |
| `u217.K11_asked_now_counted_as_reused` | `src/cratekit/label/kept_listing.py` | user | 1 file(s) | 38 | 4 | killed |
| `u217.K12_flush_batch` | `src/cratekit/label/kept_listing.py` | maintainer | 1 file(s) | 38 | 1 | killed |
| `u217.K13_unkept_said` | `src/cratekit/label/kept_listing.py` | user | 1 file(s) | 38 | 1 | killed |
| `u217.K1_life_boundary` | `src/cratekit/label/kept_listing.py` | user | 1 file(s) | 38 | 1 | killed |
| `u217.K2_future_is_fresh` | `src/cratekit/label/kept_listing.py` | maintainer | 1 file(s) | 38 | 1 | killed |
| `u217.K3_life_coefficient` | `src/cratekit/label/kept_listing.py` | user | 1 file(s) | 38 | 1 | killed |
| `u217.K4_changed_entry` | `src/cratekit/label/kept_listing.py` | user | 1 file(s) | 38 | 2 | killed |
| `u217.K5_seeds_not_asked_for` | `src/cratekit/label/kept_listing.py` | user | 1 file(s) | 38 | 1 | killed |
| `u217.K6_match_not_asked_for` | `src/cratekit/label/kept_listing.py` | user | 1 file(s) | 38 | 1 | killed |
| `u217.K9_release_shape` | `src/cratekit/label/kept_listing.py` | user | 1 file(s) | 38 | 1 | killed |
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
| `r815-a.W1_withhold_only_an_open_item` | `src/cratekit/core/review.py` | user | 2 file(s) | 214 | 5 | killed |
| `r815-a.W2_a_returned_hold_is_not_withheld` | `src/cratekit/core/review.py` | user | 2 file(s) | 214 | 1 | killed |
| `r815-a.W3_the_floor_is_never_lowered` | `src/cratekit/core/review.py` | user | 2 file(s) | 214 | 1 | killed |
| `r815-a.W5_a_refresh_keeps_the_withheld_word` | `src/cratekit/core/review.py` | user | 2 file(s) | 214 | 1 | killed |
| `r815-a.W6_redescribe_only_an_open_item` | `src/cratekit/core/review.py` | user | 2 file(s) | 214 | 2 | killed |
| `r815-a.G2_forgetting_keeps_the_failure_count` | `src/cratekit/label/catalogue.py` | user | 2 file(s) | 214 | 2 | killed |
| `r840-c.C5_the_judging_stamp_is_made_on_the_payload_as_it_stands` | `src/cratekit/label/judge_cli.py` | user | 2 file(s) | 214 | 1 | killed |
| `u27-round-8-independent.E4_path_missing_reads_ok` | `src/cratekit/core/preflight.py` | user | 5 file(s) | 738 | 4 | killed |
| `u27-round-8-independent.E5_unmounted_reads_foreign` | `src/cratekit/core/preflight.py` | user | 5 file(s) | 738 | 5 | killed |
| `u27-round-8-independent.E6_write_table_shares_read` | `src/cratekit/core/preflight.py` | user | 5 file(s) | 738 | 3 | killed |
| `u279.M10_tilde_not_expanded` | `src/cratekit/setbuilder/cli.py` | user | 4 file(s) | 366 | 1 | killed |
| `u279.M11_excluded_anchor_not_refused` | `src/cratekit/setbuilder/cli.py` | user | 4 file(s) | 366 | 2 | killed |
| `u279.M13_wrong_folder_named` | `src/cratekit/setbuilder/cli.py` | user | 4 file(s) | 366 | 1 | killed |
| `u279.M8_index_call_unexcluded` | `src/cratekit/setbuilder/cli.py` | user | 4 file(s) | 366 | 6 | killed |
| `u279.M9_staging_not_excluded` | `src/cratekit/setbuilder/cli.py` | user | 4 file(s) | 366 | 4 | killed |
| `u96-b.C1_engine_terminal` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 2 | killed |
| `u96-b.C2_engine_acknowledged` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 3 | killed |
| `u96-b.C3_engine_occupied_target` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 3 | killed |
| `u96-b.C4_engine_stub` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 5 | killed |
| `u96-b.C5_engine_library_is_mounted` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 3 | killed |
| `u27-restore-cli-author.S1_plan_takes_its_own_lock` | `src/cratekit/session/restore_cli.py` | user | 2 file(s) | 257 | 10 | killed |
| `r432-a.A1_key_casefold` | `src/cratekit/intake/landing.py` | user | 3 file(s) | 119 | 3 | killed |
| `r432-a.A2_key_normalization` | `src/cratekit/intake/landing.py` | user | 3 file(s) | 119 | 1 | killed |
| `r432-a.A3_lock_never_taken` | `src/cratekit/intake/landing.py` | user | 3 file(s) | 119 | 30 | killed |
| `r432-a.A5_not_retryable` | `src/cratekit/intake/landing.py` | user | 3 file(s) | 119 | 2 | killed |
| `r432-a.A7_holder_unreadable_name` | `src/cratekit/intake/landing.py` | user | 3 file(s) | 119 | 1 | killed |
| `r432-a.A8_holder_left_out` | `src/cratekit/intake/landing.py` | user | 3 file(s) | 119 | 2 | killed |
| `r432-a.A9_body_refusal_translated` | `src/cratekit/intake/landing.py` | maintainer | 3 file(s) | 119 | 1 | killed |
| `r432-b.A4c_lock_outlives_its_with` | `src/cratekit/intake/landing.py` | user | 3 file(s) | 119 | 7 | killed |
| `u128-b.A6b_abandoned_counts` | `src/cratekit/intake/account_playlists.py` | user | 3 file(s) | 71 | 1 | killed |
| `u128-b.A8b_ambiguous_is_an_answer` | `src/cratekit/intake/account_playlists.py` | user | 3 file(s) | 71 | 1 | killed |
| `u128-b.A9b_emptied_left_lost` | `src/cratekit/intake/account_playlists.py` | user | 3 file(s) | 71 | 1 | killed |
| `u128.A10_no_warning` | `src/cratekit/intake/account_playlists.py` | user | 3 file(s) | 71 | 5 | killed |
| `u128.A1_owned_not_mirrored` | `src/cratekit/intake/account_playlists.py` | user | 3 file(s) | 71 | 13 | killed |
| `u128.A2_rerun_unseen` | `src/cratekit/intake/account_playlists.py` | user | 3 file(s) | 71 | 2 | killed |
| `u128.A3_rerun_keeps_owned` | `src/cratekit/intake/account_playlists.py` | user | 3 file(s) | 71 | 1 | killed |
| `u128.A4_untied_carried_silent` | `src/cratekit/intake/account_playlists.py` | user | 3 file(s) | 71 | 2 | killed |
| `u128.A7_any_pass_counts` | `src/cratekit/intake/account_playlists.py` | user | 3 file(s) | 71 | 2 | killed |
| `u82-b.B5_not_listed_is_skipped` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 69 | 1 | killed |
| `u82-b.B6_a_failed_job_is_skipped` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 69 | 2 | killed |
| `u82-b.B7_unread_reports_hold_the_playlist` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 69 | 2 | killed |
| `u82-b.B8_an_offered_track_is_owed` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 69 | 1 | killed |
| `u82-c.C1_a_tombstoned_track_is_settled` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 69 | 1 | killed |
| `u82-c.C2_one_outstanding_track_holds_the_playlist` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 69 | 9 | killed |
| `u82-c.C3_landed_is_told_from_owned` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 69 | 2 | killed |
| `u82-c.C9_the_accounts_reason_is_kept` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 69 | 1 | killed |
| `u82-d.B2_paths_compared_resolved_again` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 69 | 1 | killed |
| `u180.M14_root_refused` | `src/cratekit/favorites/order.py` | user | 1 file(s) | 30 | 1 | killed |
| `u180.M15_digest_is_the_target_order` | `src/cratekit/favorites/order.py` | user | 1 file(s) | 30 | 1 | killed |
| `u180.M16_stale_digest_refused` | `src/cratekit/favorites/order.py` | user | 1 file(s) | 30 | 1 | killed |
| `u180.M17_confined_seated_position` | `src/cratekit/favorites/order.py` | user | 1 file(s) | 30 | 1 | killed |
| `u180.M18_confined_unplanned_rows` | `src/cratekit/favorites/order.py` | user | 1 file(s) | 30 | 2 | killed |
| `u180.M19_confined_memberships` | `src/cratekit/favorites/order.py` | user | 1 file(s) | 30 | 1 | killed |
| `u180.M20_confined_content` | `src/cratekit/favorites/order.py` | user | 1 file(s) | 30 | 1 | killed |
| `u180.M21_confinement_called` | `src/cratekit/favorites/order.py` | user | 1 file(s) | 30 | 1 | killed |
| `u180.M22_read_back_compares` | `src/cratekit/favorites/order.py` | user | 1 file(s) | 30 | 1 | killed |
| `u180-m25.M25_read_back_asserted` | `src/cratekit/favorites/order_cli.py` | user | 1 file(s) | 30 | 1 | killed |
| `u138.S7_verb_drops_the_answer` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 7 | killed |
| `u184.A10_summary_always_recorded` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `u184.A11_wording_swapped` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 2 | killed |
| `u184.A3_engine_rule_not_selected` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 9 | killed |
| `u184.A4_valid_record_minted_again` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 2 | killed |
| `u184.A5_expired_reported_valid` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `u184.A6_unreadable_record_refuses` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `u184.A7_already_valid_says_ok` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `u184.A8_expiry_row_dropped` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `u184.A9_expiry_row_names_the_mint` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `u204.O2_unfavourite_leaves_months` | `src/cratekit/organize/mirror_edits.py` | user | 6 file(s) | 233 | 1 | killed |
| `u204.O3_quarter_refused` | `src/cratekit/organize/mirror_edits.py` | user | 6 file(s) | 233 | 1 | killed |
| `u204.O4_colour` | `src/cratekit/organize/mirror_edits.py` | user | 6 file(s) | 233 | 1 | killed |
| `u204.O5_batch_live` | `src/cratekit/organize/mirror_edits.py` | user | 6 file(s) | 233 | 1 | killed |
| `u204.O6_inbox_latch` | `src/cratekit/organize/mirror_edits.py` | user | 6 file(s) | 233 | 1 | killed |
| `u204.O7_restore_detected` | `src/cratekit/organize/mirror_edits.py` | user | 6 file(s) | 233 | 1 | killed |
| `u161.L1_landing_pins_nothing` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 59 | 1 | killed |

## Row definitions

### `u72.M1_abort_applies`

An abort no longer stops the verb: only an empty plan returns NO_OP

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72.json`, row `M1_abort_applies`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 48 against a baseline of 48
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_recorded_abort_is_honored_over_a_library_that_went_missing`
  - `tests/test_intake_land.py::test_a_recorded_abort_is_honored_over_an_export_that_went_missing`
  - `tests/test_intake_land.py::test_an_abort_is_no_op_and_moves_nothing`

Old text:

```
    if option != "apply" or not planned.items:
```

New text:

```
    if not planned.items:
```

### `u72.M2_empty_plan_applied`

An empty plan is handed to the engine after the answer instead of returning NO_OP

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72.json`, row `M2_empty_plan_applied`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 48 against a baseline of 48
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land.py::test_an_empty_staging_folder_is_a_plan_of_nothing_and_makes_nothing`
  - `tests/test_intake_land.py::test_staging_holding_only_lists_and_dotfiles_is_a_plan_of_nothing`

Old text:

```
    if option != "apply" or not planned.items:
```

New text:

```
    if option != "apply":
```

### `u72.M3_digest_drops_where`

The digest drops the batch, the target and the intake file, so an answer for one name applies under another

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72.json`, row `M3_digest_drops_where`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_an_answer_given_for_one_batch_name_is_stale_for_another`

Old text:

```
        "batch": planned.batch,
        "target": str(target),
        "destination": str(destination),

```

New text:

```
(empty)
```

### `u72.M5_digest_drops_export`

The digest drops the export path

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72.json`, row `M5_digest_drops_export`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 48 against a baseline of 48
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_stale_answer_stays_stale_over_an_export_that_is_not_there`
  - `tests/test_intake_land.py::test_an_answer_given_against_one_export_is_stale_for_another`

Old text:

```
        "export": str(export),

```

New text:

```
(empty)
```

### `u72.M9_default_name_colons`

The default batch name keeps the run id's colons

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72.json`, row `M9_default_name_colons`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_the_folder_defaults_to_staging_the_batch_to_the_date_and_the_file_to_the_run`

Old text:

```
    return run_id.replace(":", "")
```

New text:

```
    return run_id
```

### `u72-b.M23_listing_unfiltered`

The engine's public listing returns every entry, not only audio

- File: `src/cratekit/intake/landing.py`
- Source: `u72-b.json`, row `M23_listing_unfiltered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_staging_holding_only_lists_and_dotfiles_is_a_plan_of_nothing`

Old text:

```
    return _list(folder)


def _digest(
```

New text:

```
    return tuple(folder.iterdir())


def _digest(
```

### `r791-b.C1_artifact_answers`

handle: the artifact records only the first source's answer

- File: `src/cratekit/tagging/cli.py`
- Source: `r791-b.json`, row `C1_artifact_answers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 240 against a baseline of 240
- Kills: 15 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`
  - `tests/test_tag_workers.py::test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_some_files_says_how_many_of_how_many`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`
  - `tests/test_tag_workers.py::test_a_published_genre_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_a_sweep_beatport_matched_whole_names_no_fallback_as_blocked`
  - `tests/test_tag_workers.py::test_a_sweep_discogs_decides_asks_beatport_only_for_missing_covers_and_counts_discogs_first`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_an_outage_keeps_its_own_word_in_the_sweeps_warning`
  - `tests/test_tag_workers.py::test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit`
  - `tests/test_tag_workers.py::test_files_with_no_isrc_are_counted_and_warned_about_whatever_their_skip_reason`
  - `tests/test_tag_workers.py::test_four_real_misses_are_no_hit_and_carry_no_unread_warning`
  - `tests/test_tag_workers.py::test_one_unread_file_beside_a_parse_break_is_counted_and_the_defect_is_said`
  - `tests/test_tag_workers.py::test_the_sweeps_unread_warning_names_discogs_first`

Old text:

```
                for said in result.answers
            ],
```

New text:

```
                for said in result.answers[:1]
            ],
```

### `r791-b.C2_artifact_unread`

handle: the artifact's unread map is always empty

- File: `src/cratekit/tagging/cli.py`
- Source: `r791-b.json`, row `C2_artifact_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 240 against a baseline of 240
- Kills: 6 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit`
  - `tests/test_tag_workers.py::test_one_unread_file_beside_a_parse_break_is_counted_and_the_defect_is_said`
  - `tests/test_tag_workers.py::test_the_sweeps_unread_warning_names_discogs_first`

Old text:

```
                if said.source in result.unread
```

New text:

```
                if False
```

### `r791-b.C3_summary_counts_answers`

_summary: count no answers

- File: `src/cratekit/tagging/cli.py`
- Source: `r791-b.json`, row `C3_summary_counts_answers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 240 against a baseline of 240
- Kills: 15 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_some_files_says_how_many_of_how_many`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`
  - `tests/test_tag_workers.py::test_a_published_genre_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_a_sweep_beatport_matched_whole_names_no_fallback_as_blocked`
  - `tests/test_tag_workers.py::test_a_sweep_discogs_decides_asks_beatport_only_for_missing_covers_and_counts_discogs_first`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_an_outage_keeps_its_own_word_in_the_sweeps_warning`
  - `tests/test_tag_workers.py::test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit`
  - `tests/test_tag_workers.py::test_files_with_no_isrc_are_counted_and_warned_about_whatever_their_skip_reason`
  - `tests/test_tag_workers.py::test_one_unread_file_beside_a_parse_break_is_counted_and_the_defect_is_said`
  - `tests/test_tag_workers.py::test_the_sweeps_unread_warning_names_discogs_first`

Old text:

```
                counted[word] += 1
```

New text:

```
                counted[word] += 0
```

### `r791-b.C6_not_asked_excluded`

_unread_warnings: count not-asked as asked, so a Beatport match hides a blocked fallback

- File: `src/cratekit/tagging/cli.py`
- Source: `r791-b.json`, row `C6_not_asked_excluded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 240 against a baseline of 240
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning`

Old text:

```
        asked = sum(count for word, count in counted.items() if word != searchers.NOT_ASKED)
```

New text:

```
        asked = sum(count for word, count in counted.items())
```

### `r791-b.C7_parse_break_said`

_unread_warnings: never say a parse break is a defect a rerun will not move

- File: `src/cratekit/tagging/cli.py`
- Source: `r791-b.json`, row `C7_parse_break_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 240 against a baseline of 240
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_one_unread_file_beside_a_parse_break_is_counted_and_the_defect_is_said`

Old text:

```
                        if broken
                        else ""
```

New text:

```
                        if False
                        else ""
```

### `r791-b.C8_one_file`

_files: say 1 files were

- File: `src/cratekit/tagging/cli.py`
- Source: `r791-b.json`, row `C8_one_file`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 240 against a baseline of 240
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_one_unread_file_beside_a_parse_break_is_counted_and_the_defect_is_said`

Old text:

```
    return "1 file was" if count == 1 else f"{count} files were"
```

New text:

```
    return f"{count} files were"
```

### `r791-b.C9_unread_skip_zero_filled`

_summary: count only the three skip reasons that predate R-791

- File: `src/cratekit/tagging/cli.py`
- Source: `r791-b.json`, row `C9_unread_skip_zero_filled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 240 against a baseline of 240
- Kills: 11 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_a_sweep_with_no_discogs_token_says_so_and_reads_no_file_as_no_hit`
  - `tests/test_tag_workers.py::test_an_outage_keeps_its_own_word_in_the_sweeps_warning`
  - `tests/test_tag_workers.py::test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit`
  - `tests/test_tag_workers.py::test_files_with_no_isrc_are_counted_and_warned_about_whatever_their_skip_reason`
  - `tests/test_tag_workers.py::test_one_unread_file_beside_a_parse_break_is_counted_and_the_defect_is_said`
  - `tests/test_tag_workers.py::test_the_skip_reason_reaches_the_report_and_not_only_the_artifact`
  - `tests/test_tag_workers.py::test_the_sweeps_unread_warning_names_discogs_first`

Old text:

```
    skipped = dict.fromkeys(tag_engine.SKIP_REASONS, 0)
```

New text:

```
    skipped = dict.fromkeys(tag_engine.SKIP_REASONS[:3], 0)
```

### `r263.W1_no_unrecorded_state`

status_rows ignores the declared no_cursor reason, so every absent record reads as never

- File: `src/cratekit/sync/watermarks.py`
- Source: `r263.json`, row `W1_no_unrecorded_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 569 against a baseline of 569
- Kills: 4 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_clean_labels_sweep_is_not_reported_as_never_having_run`
  - `tests/test_incremental_sync.py::test_a_stale_cursor_on_a_source_that_records_none_is_not_a_live_completion`
  - `tests/test_incremental_sync.py::test_doctor_prints_the_labels_row_it_is_given`
  - `tests/test_incremental_sync.py::test_favorites_is_not_reported_as_never_having_run`

Old text:

```
        reason = no_cursor.get(source_id)
```

New text:

```
        reason = None
```

### `r263.W2_state_word`

A cursorless source is reported with state never, detail unchanged

- File: `src/cratekit/sync/watermarks.py`
- Source: `r263.json`, row `W2_state_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 569 against a baseline of 569
- Kills: 3 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_clean_labels_sweep_is_not_reported_as_never_having_run`
  - `tests/test_incremental_sync.py::test_a_stale_cursor_on_a_source_that_records_none_is_not_a_live_completion`
  - `tests/test_incremental_sync.py::test_favorites_is_not_reported_as_never_having_run`

Old text:

```
"state": "unrecorded"
```

New text:

```
"state": "never"
```

### `r263.W3_stale_record_as_completion`

A stale record on a cursorless source is reported as its last completion again

- File: `src/cratekit/sync/watermarks.py`
- Source: `r263.json`, row `W3_stale_record_as_completion`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 569 against a baseline of 569
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_stale_cursor_on_a_source_that_records_none_is_not_a_live_completion`

Old text:

```
        if reason is not None:
```

New text:

```
        if reason is not None and mark is None:
```

### `r263.W4_stale_suffix`

Drop the note that an earlier build's cursor no longer moves

- File: `src/cratekit/sync/watermarks.py`
- Source: `r263.json`, row `W4_stale_suffix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 569 against a baseline of 569
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_stale_cursor_on_a_source_that_records_none_is_not_a_live_completion`

Old text:

```
            if mark is not None:
                detail += (
```

New text:

```
            if False:
                detail += (
```

### `u284-composite.C3x_unread_discogs_and_outage_named`

tagging.cli._refused_out: the composite for C3's zero, both the Discogs was read guard and the every other catalogue refused guard removed, so any file left with no genre is named as one the catalogues refused

- File: `src/cratekit/tagging/cli.py`
- Source: `u284-composite.json`, row `C3x_unread_discogs_and_outage_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_tag_workers.py`, `tests/test_tag_folder_copyright.py`, `tests/test_discogs_first.py`
- Collected: 227 against a baseline of 227
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_pass_whose_catalogues_answered_says_nothing_of_refusals`
  - `tests/test_sync_refused.py::test_a_sweep_beatport_never_refused_names_nothing`

Old text:

```
    if said.get(searchers.DISCOGS) not in (searchers.Answer.MISS.value, searchers.Answer.MATCHED.value):
        return ()
    others = [
        source
        for source in searchers.SOURCES
        if source != searchers.DISCOGS and source in said and said[source] != searchers.NOT_ASKED
    ]
    if not others or any(said[source] != searchers.Answer.BLOCKED.value for source in others):
        return ()
```

New text:

```
    others = [
        source
        for source in searchers.SOURCES
        if source != searchers.DISCOGS and source in said and said[source] != searchers.NOT_ASKED
    ]
    if not others:
        return ()
```

### `u284.C1_tagged_file_named_refused`

tagging.cli._refused_out: a file with a genre written is named among those left with none

- File: `src/cratekit/tagging/cli.py`
- Source: `u284.json`, row `C1_tagged_file_named_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_tag_workers.py`, `tests/test_tag_folder_copyright.py`, `tests/test_discogs_first.py`
- Collected: 227 against a baseline of 227
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_file_discogs_tagged_while_beatport_refused_its_picture_is_not_named`

Old text:

```
    if reason not in (tag_engine.SOURCES_UNREAD, tag_engine.UNMAPPED_GENRE):
        return ()
```

New text:

```
    if False:
        return ()
```

### `u284.C2_outage_named_refused`

tagging.cli._refused_out: a file another catalogue was down for is named as refused

- File: `src/cratekit/tagging/cli.py`
- Source: `u284.json`, row `C2_outage_named_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_tag_workers.py`, `tests/test_tag_folder_copyright.py`, `tests/test_discogs_first.py`
- Collected: 227 against a baseline of 227
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_pass_whose_catalogues_answered_says_nothing_of_refusals`
  - `tests/test_sync_refused.py::test_a_sweep_beatport_never_refused_names_nothing`

Old text:

```
    if not others or any(said[source] != searchers.Answer.BLOCKED.value for source in others):
```

New text:

```
    if not others:
```

### `u284.C4_stop_never_collected`

tagging.cli._summary: no failed file is read as one every catalogue refused

- File: `src/cratekit/tagging/cli.py`
- Source: `u284.json`, row `C4_stop_never_collected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_tag_workers.py`, `tests/test_tag_folder_copyright.py`, `tests/test_discogs_first.py`
- Collected: 227 against a baseline of 227
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_sweep_with_no_token_fails_each_file_and_says_who_refused_and_the_token`
  - `tests/test_sync_refused.py::test_with_no_token_the_pass_stops_at_its_tag_step_saying_who_refused_and_the_token`

Old text:

```
        if cause is not None and isinstance((cause.detail or {}).get(searchers.REFUSED_DETAIL), dict):
```

New text:

```
        if False:
```

### `u284.C5_sweep_stop_unsaid`

tagging.cli._with_report: the sweep's own refusal says nothing of who refused

- File: `src/cratekit/tagging/cli.py`
- Source: `u284.json`, row `C5_sweep_stop_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_tag_workers.py`, `tests/test_tag_folder_copyright.py`, `tests/test_discogs_first.py`
- Collected: 227 against a baseline of 227
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_sweep_with_no_token_fails_each_file_and_says_who_refused_and_the_token`

Old text:

```
    if stop:
        # WHO REFUSED
```

New text:

```
    if False:
        # WHO REFUSED
```

### `u284.C6_token_unsaid`

tagging.cli._refusal_stop: Discogs unasked is never said and its token step never given

- File: `src/cratekit/tagging/cli.py`
- Source: `u284.json`, row `C6_token_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_tag_workers.py`, `tests/test_tag_folder_copyright.py`, `tests/test_discogs_first.py`
- Collected: 227 against a baseline of 227
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_stop_over_a_token_discogs_refused_never_says_waiting_mends_it`
  - `tests/test_sync_refused.py::test_a_sweep_with_no_token_fails_each_file_and_says_who_refused_and_the_token`
  - `tests/test_sync_refused.py::test_with_no_token_the_pass_stops_at_its_tag_step_saying_who_refused_and_the_token`

Old text:

```
    if unasked:
        why = 
```

New text:

```
    if False:
        why = 
```

### `u284.C7_rejected_token_told_to_wait`

tagging.cli._refusal_stop: a stop over a rejected token says waiting mends it

- File: `src/cratekit/tagging/cli.py`
- Source: `u284.json`, row `C7_rejected_token_told_to_wait`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_tag_workers.py`, `tests/test_tag_folder_copyright.py`, `tests/test_discogs_first.py`
- Collected: 227 against a baseline of 227
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_stop_over_a_token_discogs_refused_never_says_waiting_mends_it`

Old text:

```
    if unasked != searchers.DISCOGS_TOKEN_REFUSED:
```

New text:

```
    if True:
```

### `u217.K10_naive_instant`

_instant: accept an instant with no zone

- File: `src/cratekit/label/kept_listing.py`
- Source: `u217.json`, row `K10_naive_instant`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_a_kept_listing_that_cannot_be_read_refuses_before_any_call[written5]`

Old text:

```
    return moment if moment.tzinfo is not None else None
```

New text:

```
    return moment
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

### `u217.K13_unkept_said`

flush: swallow a refused write without saying it

- File: `src/cratekit/label/kept_listing.py`
- Source: `u217.json`, row `K13_unkept_said`
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

### `r815-a.W1_withhold_only_an_open_item`

withhold: move an item whatever its verdict column says

- File: `src/cratekit/core/review.py`
- Source: `r815-a.json`, row `W1_withhold_only_an_open_item`
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

- File: `src/cratekit/core/review.py`
- Source: `r815-a.json`, row `W2_a_returned_hold_is_not_withheld`
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

- File: `src/cratekit/core/review.py`
- Source: `r815-a.json`, row `W3_the_floor_is_never_lowered`
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

### `r815-a.W5_a_refresh_keeps_the_withheld_word`

_CARRIED_ACROSS_A_REFRESH: carry the filing run and drop the withheld word

- File: `src/cratekit/core/review.py`
- Source: `r815-a.json`, row `W5_a_refresh_keeps_the_withheld_word`
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

### `r815-a.G2_forgetting_keeps_the_failure_count`

ReleaseTracks.forget: forget the failures in a row as well

- File: `src/cratekit/label/catalogue.py`
- Source: `r815-a.json`, row `G2_forgetting_keeps_the_failure_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`, `tests/test_label_genre_gate.py`
- Collected: 214 against a baseline of 214
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_judge.py::test_the_reader_forgets_each_release_and_keeps_its_count_of_failures`
  - `tests/test_label_judge.py::test_three_provider_reads_failing_in_a_row_stop_the_run`

Old text:

```
        self._read.clear()

    def release_tracks
```

New text:

```
        self._read.clear()
        self._failed_in_a_row = 0

    def release_tracks
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

### `u27-round-8-independent.E4_path_missing_reads_ok`

A matching identity with an absent root resolves to OK instead of LIBRARY_PATH_MISSING

- File: `src/cratekit/core/preflight.py`
- Source: `u27-round-8-independent.json`, row `E4_path_missing_reads_ok`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_preflight.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 738 against a baseline of 738
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
- Collected: 738 against a baseline of 738
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
- Collected: 738 against a baseline of 738
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

### `u279.M10_tilde_not_expanded`

excluded_folders: read the staging path without expanding a tilde, round one's finding

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u279.json`, row `M10_tilde_not_expanded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 366 against a baseline of 366
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[tilde-staging]`

Old text:

```
Path(cfg.paths.download_staging).expanduser())
```

New text:

```
Path(cfg.paths.download_staging))
```

### `u279.M11_excluded_anchor_not_refused`

set_build: drop the excluded anchor refusal, so an anchor in staging gets the generic not indexed wording

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u279.json`, row `M11_excluded_anchor_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 366 against a baseline of 366
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_an_anchor_inside_an_excluded_folder_is_refused_naming_the_folder[staging]`
  - `tests/test_setbuilder_excluded.py::test_an_anchor_inside_an_excluded_folder_is_refused_naming_the_folder[state]`

Old text:

```
    _refuse_if_excluded(candidate, cfg, root)

```

New text:

```
(empty)
```

### `u279.M13_wrong_folder_named`

_refuse_if_excluded: say the state folder whichever folder holds the anchor

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u279.json`, row `M13_wrong_folder_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 366 against a baseline of 366
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_an_anchor_inside_an_excluded_folder_is_refused_naming_the_folder[staging]`

Old text:

```
    if holder == folders[0]:
```

New text:

```
    if True:
```

### `u279.M8_index_call_unexcluded`

setbuild _index: drop exclude, so the verb's index walks the state and staging folders again

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u279.json`, row `M8_index_call_unexcluded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 366 against a baseline of 366
- Kills: 6 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_a_companion_held_only_in_staging_is_left_out_of_the_set`
  - `tests/test_setbuilder_excluded.py::test_a_name_held_only_in_staging_is_not_indexed_and_says_what_is`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[download-staging]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[renamed-state-folder]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[state-folder]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[tilde-staging]`

Old text:

```
        exclude=excluded_folders(cfg),

```

New text:

```
(empty)
```

### `u279.M9_staging_not_excluded`

excluded_folders: leave download staging out of the exclusion, the state folder only

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u279.json`, row `M9_staging_not_excluded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 366 against a baseline of 366
- Kills: 4 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_a_name_held_only_in_staging_is_not_indexed_and_says_what_is`
  - `tests/test_setbuilder_excluded.py::test_an_anchor_inside_an_excluded_folder_is_refused_naming_the_folder[staging]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[download-staging]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[tilde-staging]`

Old text:

```
    return (config.library_state_dir(cfg), Path(cfg.paths.download_staging).expanduser())
```

New text:

```
    return (config.library_state_dir(cfg), config.library_state_dir(cfg))
```

### `u96-b.C1_engine_terminal`

SAMPLE of the engine's guards, now reachable from a verb. bare_metal_session: disarm the controlling terminal refusal

- File: `src/cratekit/core/restore.py`
- Source: `u96-b.json`, row `C1_engine_terminal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`
- Collected: 257 against a baseline of 257
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_needs_a_terminal_and_an_explicit_decision`
  - `tests/test_restore_cli.py::test_a_refusal_before_the_lock_leaves_the_disk_untouched[nobody is at a terminal]`

Old text:

```
    if not probe():
        raise _refuse_target(
            "this invocation has no controlling terminal
```

New text:

```
    if False:
        raise _refuse_target(
            "this invocation has no controlling terminal
```

### `u96-b.C2_engine_acknowledged`

SAMPLE. bare_metal_session: disarm the acknowledgment refusal

- File: `src/cratekit/core/restore.py`
- Source: `u96-b.json`, row `C2_engine_acknowledged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`
- Collected: 257 against a baseline of 257
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_needs_a_terminal_and_an_explicit_decision`
  - `tests/test_restore_cli.py::test_a_refusal_before_the_lock_leaves_the_disk_untouched[the replacement was not accepted]`
  - `tests/test_restore_cli.py::test_the_verb_refuses_without_the_acceptance_flag`

Old text:

```
    if not acknowledged:
```

New text:

```
    if False:
```

### `u96-b.C3_engine_occupied_target`

SAMPLE. assert_recovery_target: disarm the refusal of a target that already holds a database

- File: `src/cratekit/core/restore.py`
- Source: `u96-b.json`, row `C3_engine_occupied_target`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`
- Collected: 257 against a baseline of 257
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_holding_a_library_in_a_subdirectory`
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_that_already_holds_a_library`
  - `tests/test_restore_cli.py::test_a_target_that_already_holds_a_database_is_refused_with_no_way_to_name_it`

Old text:

```
    if existing and not replacing_existing:
```

New text:

```
    if False:
```

### `u96-b.C4_engine_stub`

SAMPLE. assert_recovery_target: disarm the refusal of the stub an unmounted volume leaves on the internal disk

- File: `src/cratekit/core/restore.py`
- Source: `u96-b.json`, row `C4_engine_stub`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`
- Collected: 257 against a baseline of 257
- Kills: 5 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_the_stub_an_unmounted_volume_leaves_behind`
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_the_stubs_beside_and_beneath_the_mount_point[library 1-why1]`
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_the_stubs_beside_and_beneath_the_mount_point[library/Music-why0]`
  - `tests/test_restore.py::test_round2_the_real_mount_probe_is_armed_by_default`
  - `tests/test_restore_cli.py::test_a_refusal_before_the_lock_leaves_the_disk_untouched[the target is the stub on the internal disk]`

Old text:

```
    if (inside_configured or beside_configured) and not probe(where):
```

New text:

```
    if False:
```

### `u96-b.C5_engine_library_is_mounted`

SAMPLE. assert_library_volume_is_gone: answer gone when the library is mounted and is the recorded volume

- File: `src/cratekit/core/restore.py`
- Source: `u96-b.json`, row `C5_engine_library_is_mounted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`
- Collected: 257 against a baseline of 257
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_is_refused_while_the_library_is_reachable`
  - `tests/test_restore_cli.py::test_a_refusal_before_the_lock_leaves_the_disk_untouched[the library is still mounted]`
  - `tests/test_restore_cli.py::test_the_verb_refuses_while_the_library_is_mounted`

Old text:

```
    raise _refuse_target(
        f"the library at {cfg.library.root} is mounted and is the volume this "
```

New text:

```
    return preflight.MountState.NOT_MOUNTED
    raise _refuse_target(
        f"the library at {cfg.library.root} is mounted and is the volume this "
```

### `u27-restore-cli-author.S1_plan_takes_its_own_lock`

Let the off-machine PLAN acquire the library lock itself instead of taking the open guard

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-author.json`, row `S1_plan_takes_its_own_lock`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`
- Collected: 257 against a baseline of 257
- Kills: 10 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_backup_landing_after_the_approval_does_not_change_what_is_pulled`
  - `tests/test_restore_cli.py::test_a_rehearsal_is_still_refused_while_rekordbox_is_running`
  - `tests/test_restore_cli.py::test_a_target_directory_that_does_not_exist_is_still_the_absent_refusal`
  - `tests/test_restore_cli.py::test_a_target_restores_the_database_into_the_directory_it_names`
  - `tests/test_restore_cli.py::test_a_target_run_rolls_no_session_back_even_by_default`
  - `tests/test_restore_cli.py::test_an_unmarked_newest_snapshot_is_refused_and_a_named_one_is_pulled`
  - `tests/test_restore_cli.py::test_the_from_backup_flag_reaches_the_off_machine_half_through_the_dispatcher`
  - `tests/test_restore_cli.py::test_the_replaced_drive_flag_reaches_the_engine_and_the_digest`
  - `tests/test_restore_cli.py::test_the_report_names_the_snapshot_that_arrived`
  - `tests/test_restore_cli.py::test_what_is_offered_is_what_is_pulled`

Old text:

```
                    include_mirror=include_mirror,
                    gates=held.guard,
```

New text:

```
                    include_mirror=include_mirror,
```

### `r432-a.A1_key_casefold`

lock_key: drop the casefold, so two spellings of one folder on a case insensitive volume each get their own lock

- File: `src/cratekit/intake/landing.py`
- Source: `r432-a.json`, row `A1_key_casefold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_landing_labels.py`
- Collected: 119 against a baseline of 119
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land.py::test_another_spelling_of_a_held_batch_folder_is_refused`
  - `tests/test_landing.py::test_two_spellings_of_one_folder_share_one_lock[2026-09-18_ACQUIRED0]`
  - `tests/test_landing.py::test_two_spellings_of_one_folder_share_one_lock[2026-09-18_ACQUIRED1]`

Old text:

```
    folded = unicodedata.normalize("NFC", batch.casefold())
```

New text:

```
    folded = unicodedata.normalize("NFC", batch)
```

### `r432-a.A2_key_normalization`

lock_key: drop the normalization, so the composed and decomposed spellings of an accented name each get their own lock

- File: `src/cratekit/intake/landing.py`
- Source: `r432-a.json`, row `A2_key_normalization`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_landing_labels.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_composed_and_decomposed_spellings_share_one_lock`

Old text:

```
    folded = unicodedata.normalize("NFC", batch.casefold())
```

New text:

```
    folded = batch.casefold()
```

### `r432-a.A3_lock_never_taken`

batch_lock: hand back the lock's path without taking it, so nothing is excluded

- File: `src/cratekit/intake/landing.py`
- Source: `r432-a.json`, row `A3_lock_never_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_landing_labels.py`
- Collected: 119 against a baseline of 119
- Kills: 30 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_held_batch_name_does_not_stop_anybody_reading_the_plan`
  - `tests/test_intake_land.py::test_a_landing_in_another_process_refuses_this_one_until_it_ends`
  - `tests/test_intake_land.py::test_a_landing_under_another_batch_name_lands_while_one_is_held`
  - `tests/test_intake_land.py::test_a_landing_without_a_manifest_reports_nothing_about_labels`
  - `tests/test_intake_land.py::test_a_manifest_is_on_the_gate_screen_and_its_labels_are_in_the_envelope`
  - `tests/test_intake_land.py::test_a_manifest_whose_only_row_matched_nothing_still_reports_it`
  - `tests/test_intake_land.py::test_a_recorded_apply_over_an_export_that_went_missing_is_the_engine_s_refusal`
  - `tests/test_intake_land.py::test_a_refused_file_is_a_warning_a_person_reads`
  - `tests/test_intake_land.py::test_a_second_landing_under_a_held_batch_name_refuses_and_moves_nothing`
  - `tests/test_intake_land.py::test_an_answered_run_lands_the_batch_and_names_the_xml_in_human_output`
  - `tests/test_intake_land.py::test_another_spelling_of_a_held_batch_folder_is_refused`
  - `tests/test_intake_land.py::test_the_engine_is_handed_the_fingerprint_of_the_bytes_the_gate_compared`
  - `tests/test_intake_land.py::test_the_folder_defaults_to_staging_the_batch_to_the_date_and_the_file_to_the_run`
  - `tests/test_intake_land.py::test_the_landed_envelope_carries_an_import_that_blocks_nothing`
  - `tests/test_intake_land.py::test_the_lock_is_held_for_the_whole_of_the_apply`
  - ... and 15 more, see the JSON sidecar

Old text:

```
        path = lock.__enter__()
```

New text:

```
        path = jobs.lock_path(key, root=root)
```

### `r432-a.A5_not_retryable`

batch_lock: mark the held refusal as not retryable, though the holder ending is exactly what a retry waits for

- File: `src/cratekit/intake/landing.py`
- Source: `r432-a.json`, row `A5_not_retryable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_landing_labels.py`
- Collected: 119 against a baseline of 119
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_second_landing_under_a_held_batch_name_refuses_and_moves_nothing`
  - `tests/test_landing.py::test_a_held_batch_name_refuses_a_second_holder_and_names_the_batch`

Old text:

```
            retryable=True,
            origin=_ORIGIN,
            detail={"batch": batch, "lock": str(held), "holder": who},
```

New text:

```
            retryable=False,
            origin=_ORIGIN,
            detail={"batch": batch, "lock": str(held), "holder": who},
```

### `r432-a.A7_holder_unreadable_name`

_holder: stop treating a lock file with no readable name in it as an unknown holder, so the refusal dies on a parse error instead

- File: `src/cratekit/intake/landing.py`
- Source: `r432-a.json`, row `A7_holder_unreadable_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_landing_labels.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_a_holder_that_has_not_written_its_name_yet_is_unknown`

Old text:

```
    except (OSError, ValueError, TypeError, KeyError):
        return "holder unknown"
```

New text:

```
    except (OSError, TypeError, KeyError):
        return "holder unknown"
```

### `r432-a.A8_holder_left_out`

batch_lock: leave the holder out of the message, so a person is told a landing is running and not which

- File: `src/cratekit/intake/landing.py`
- Source: `r432-a.json`, row `A8_holder_left_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_landing_labels.py`
- Collected: 119 against a baseline of 119
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_landing_in_another_process_refuses_this_one_until_it_ends`
  - `tests/test_landing.py::test_a_held_batch_name_refuses_a_second_holder_and_names_the_batch`

Old text:

```
            f"another landing under the batch name {batch!r} is running ({who}), "
```

New text:

```
            f"another landing under the batch name {batch!r} is running, "
```

### `r432-a.A9_body_refusal_translated`

batch_lock: translate a held job lock raised by the body as well as by the taking, so an unrelated refusal is reported as a second landing

- File: `src/cratekit/intake/landing.py`
- Source: `r432-a.json`, row `A9_body_refusal_translated`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_landing_labels.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_a_held_job_lock_raised_under_the_batch_lock_is_not_called_a_landing`

Old text:

```
    try:
        yield path
    finally:
```

New text:

```
    try:
        try:
            yield path
        except jobs.DriverHeld:
            raise refuse("job-driver-held", "a second landing", origin=_ORIGIN) from None
    finally:
```

### `r432-b.A4c_lock_outlives_its_with`

What the release tests do hold: drop the release AND keep the lock object alive, which is what a leaked lock is once the collector cannot free it

- File: `src/cratekit/intake/landing.py`
- Source: `r432-b.json`, row `A4c_lock_outlives_its_with`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_landing_labels.py`
- Collected: 119 against a baseline of 119
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_land.py::test_the_lock_is_released_after_a_landing`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal_and_the_name_can_land_after[_an_export_that_is_not_there]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal_and_the_name_can_land_after[_an_intake_file_already_there]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal_and_the_name_can_land_after[_every_target_taken]`
  - `tests/test_intake_land.py::test_the_lock_is_released_when_the_engine_fails_with_no_refusal`
  - `tests/test_landing.py::test_a_refusal_inside_the_batch_lock_releases_it`
  - `tests/test_landing.py::test_a_released_batch_lock_leaves_its_file_and_can_be_taken_again`

Old text:

```
        lock.__exit__(None, None, None)
```

New text:

```
        globals().setdefault("_LEAKED", []).append(lock)
```

### `u128-b.A6b_abandoned_counts`

Rerun of A6 after its test: count every landing record as standing

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u128-b.json`, row `A6b_abandoned_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_an_abandoned_landing_is_not_read_as_mirrored`

Old text:

```
        if record.workflow == ingest.INTAKE_WORKFLOW and record.state in standing
```

New text:

```
        if record.workflow == ingest.INTAKE_WORKFLOW
```

### `u128-b.A8b_ambiguous_is_an_answer`

Rerun of A8 after its test: take the first of two active rows as the owned row

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u128-b.json`, row `A8b_ambiguous_is_an_answer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_file_two_active_rows_claim_is_no_owned_row`

Old text:

```
                if matched.outcome is trees.MatchOutcome.AMBIGUOUS:
                    answer = ("", AMBIGUOUS_ROWS)
                    continue
```

New text:

```
                if matched.outcome is trees.MatchOutcome.AMBIGUOUS:
                    answer = (str(matched.content_ids[0]), "")
                    break
```

### `u128-b.A9b_emptied_left_lost`

Rerun of A9 after its test: drop the left rows of a claim left holding nothing

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u128-b.json`, row `A9b_emptied_left_lost`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_claim_left_holding_nothing_still_answers_its_left_rows`

Old text:

```
            emptied.extend((one.name, row) for row in left)
```

New text:

```
            pass
```

### `u128.A10_no_warning`

Give no left out warning however many rows were left

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u128.json`, row `A10_no_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 71 against a baseline of 71
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_track_neither_owned_nor_brought_is_named_in_the_warnings`
  - `tests/test_intake_land_account_playlists.py::test_an_export_entry_on_another_machine_is_no_owned_row`
  - `tests/test_intake_land_account_playlists.py::test_an_owned_track_whose_row_the_export_does_not_hold_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`

Old text:

```
    if not left:
        return []
    named_rows
```

New text:

```
    if True:
        return []
    named_rows
```

### `u128.A1_owned_not_mirrored`

Drop every owned member from the claim, U113's new tracks only rule

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u128.json`, row `A1_owned_not_mirrored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 71 against a baseline of 71
- Kills: 13 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists.py::test_an_export_entry_on_another_machine_is_no_owned_row`
  - `tests/test_intake_land_account_playlists.py::test_an_export_rewritten_after_the_gate_moves_nothing`
  - `tests/test_intake_land_account_playlists.py::test_an_owned_track_in_two_account_playlists_is_in_both`
  - `tests/test_intake_land_account_playlists.py::test_an_owned_track_whose_row_the_export_does_not_hold_is_warned`
  - `tests/test_intake_land_account_playlists.py::test_the_engine_reads_the_owned_entries_again_before_the_first_move`
  - `tests/test_intake_land_account_playlists.py::test_the_gate_screen_counts_the_owned_tracks_beside_the_new`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_in_two_account_playlists_is_in_both`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_the_gate_screen_counts_the_owned_rows_beside_the_new`

Old text:

```
            if row.paths not in seen:
                seen.add(row.paths)
                members.append(_member(row))
```

New text:

```
            if row.paths not in seen:
                seen.add(row.paths)
```

### `u128.A2_rerun_unseen`

Never read a playlist as already mirrored by this pass, so a rerun mirrors the owned tracks again

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u128.json`, row `A2_rerun_unseen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 71 against a baseline of 71
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_bridge_landing_is_what_a_rerun_of_its_pass_reads_as_mirrored`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`

Old text:

```
        rerun = source.playlist_id in again
```

New text:

```
        rerun = False
```

### `u128.A3_rerun_keeps_owned`

On a rerun, keep the owned members and the left rows instead of the new files alone

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u128.json`, row `A3_rerun_keeps_owned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`

Old text:

```
            if rerun:
                continue
            if row.state != OWNED:
```

New text:

```
            if row.state != OWNED:
```

### `u128.A4_untied_carried_silent`

A carried row no planned file answers is silently absent rather than left

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u128.json`, row `A4_untied_carried_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 71 against a baseline of 71
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_track_neither_owned_nor_brought_is_named_in_the_warnings`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`

Old text:

```
                if not tied:
                    left.append(_left(row, NOT_BROUGHT))
```

New text:

```
                if not tied:
                    pass
```

### `u128.A7_any_pass_counts`

Read a playlist as mirrored when any pass landed it, not only this one

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u128.json`, row `A7_any_pass_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 71 against a baseline of 71
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_bridge_landing_is_what_a_rerun_of_its_pass_reads_as_mirrored`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`

Old text:

```
        and entry.get(PASS_KEY) == pass_name
```

New text:

```
        and entry.get(PASS_KEY) is not None
```

### `u82-b.B5_not_listed_is_skipped`

_decided: drop the not listed reason, so the plan declares a rename of a playlist the account no longer has

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u82-b.json`, row `B5_not_listed_is_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_playlist_the_account_no_longer_lists_is_said_and_not_planned`

Old text:

```
        if not entry.name:
            entry.reason = NOT_LISTED
```

New text:

```
        if False:
            entry.reason = NOT_LISTED
```

### `u82-b.B6_a_failed_job_is_skipped`

_decided: drop the unfinished job reason, so a playlist whose tracks were never all resolved is read from whatever reports it has

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u82-b.json`, row `B6_a_failed_job_is_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`
- Collected: 69 against a baseline of 69
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_named_playlist_whose_job_failed_is_refused_by_name`
  - `tests/test_sync_mark.py::test_a_playlist_whose_job_failed_is_said_and_not_planned`

Old text:

```
        elif job.state is not jobs.JobState.SUCCEEDED:
```

New text:

```
        elif False:
```

### `u82-b.B7_unread_reports_hold_the_playlist`

_decided: stop catching the report reader's refusal, so one damaged report refuses the whole verb and the whole playlists beside it are never marked

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u82-b.json`, row `B7_unread_reports_hold_the_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`
- Collected: 69 against a baseline of 69
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_named_playlist_whose_reports_cannot_be_read_is_refused_by_name`
  - `tests/test_sync_mark.py::test_a_playlist_whose_reports_cannot_be_read_is_left_alone`

Old text:

```
        except CratekitError as exc:
            # UNREAD IS NOT NOTHING OWED.
```

New text:

```
        except ZeroDivisionError as exc:
            # UNREAD IS NOT NOTHING OWED.
```

### `u82-b.B8_an_offered_track_is_owed`

_NOT_FOUND: count only missing reports, which is what the manifest carried, so a playlist holding a track the pass offered for review is marked over it

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u82-b.json`, row `B8_an_offered_track_is_owed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_track_the_pass_offered_for_review_holds_its_playlist_back`

Old text:

```
_NOT_FOUND = frozenset({"missing", "offered"})
```

New text:

```
_NOT_FOUND = frozenset({"missing"})
```

### `u82-c.C1_a_tombstoned_track_is_settled`

_settle: drop the suppressed branch, so a track deleted on purpose since the pass holds its playlist back for ever

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u82-c.json`, row `C1_a_tombstoned_track_is_settled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_track_deleted_on_purpose_since_the_pass_is_not_owed`

Old text:

```
            elif found.state is match.MatchState.SUPPRESSED:
```

New text:

```
            elif False:
```

### `u82-c.C2_one_outstanding_track_holds_the_playlist`

_settle: never set the outstanding reason, so a playlist with a track still not in the library is planned for the prefix

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u82-c.json`, row `C2_one_outstanding_track_holds_the_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`
- Collected: 69 against a baseline of 69
- Kills: 9 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_named_playlist_the_pass_did_not_complete_is_refused_by_name`
  - `tests/test_sync_mark.py::test_a_native_answer_is_stale_once_another_playlist_becomes_whole`
  - `tests/test_sync_mark.py::test_a_native_pass_with_one_track_not_held_leaves_that_playlist_alone`
  - `tests/test_sync_mark.py::test_a_playlist_with_one_row_not_landed_is_not_marked`
  - `tests/test_sync_mark.py::test_a_track_deleted_on_purpose_since_the_pass_is_not_owed`
  - `tests/test_sync_mark.py::test_a_track_the_pass_offered_for_review_holds_its_playlist_back`
  - `tests/test_sync_mark.py::test_a_track_two_playlists_share_holds_both_back_until_it_lands`
  - `tests/test_sync_mark.py::test_an_answer_to_one_plan_does_not_carry_out_another`
  - `tests/test_sync_mark.py::test_the_pass_is_decided_without_its_manifest`

Old text:

```
        if entry.outstanding:
            entry.reason = ROWS_OUTSTANDING
```

New text:

```
        if False:
            entry.reason = ROWS_OUTSTANDING
```

### `u82-c.C3_landed_is_told_from_owned`

_settle: call every matched track landed, so the screen credits this landing with files it did not bring

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u82-c.json`, row `C3_landed_is_told_from_owned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`
- Collected: 69 against a baseline of 69
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_native_pass_whose_tracks_the_library_holds_is_marked_after_the_answer`
  - `tests/test_sync_mark.py::test_a_row_the_library_holds_and_the_file_does_not_name_is_owned`

Old text:

```
                entry.settled[LANDED if held & named else OWNED] += 1
```

New text:

```
                entry.settled[LANDED] += 1
```

### `u82-c.C9_the_accounts_reason_is_kept`

_failed_part_way: treat a refusal the account raised as a defect, so a provider timeout is reported as internal-error

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u82-c.json`, row `C9_the_accounts_reason_is_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_refusal_the_record_raised_keeps_its_reason_and_names_what_was_marked`

Old text:

```
    if isinstance(exc, CratekitError):
        cause = exc.cause
```

New text:

```
    if False:
        cause = exc.cause
```

### `u82-d.B2_paths_compared_resolved_again`

The zero of u82-b re-measured after test_a_library_reached_through_a_link_still_reads_its_files_as_landed. _comparable: compare the spelled path and not the resolved one

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u82-d.json`, row `B2_paths_compared_resolved_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_library_reached_through_a_link_still_reads_its_files_as_landed`

Old text:

```
    return locations.norm_for_compare(str(Path(path).resolve()))
```

New text:

```
    return locations.norm_for_compare(str(path))
```

### `u180.M14_root_refused`

plan: an All Favorites at the playlist root is not refused, so the verb answers over no folder

- File: `src/cratekit/favorites/order.py`
- Source: `u180.json`, row `M14_root_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_no_favorites_folder_refuses_by_name_and_writes_nothing`

Old text:

```
    if not home.folder_id:
        raise refuse(
```

New text:

```
    if False:
        raise refuse(
```

### `u180.M15_digest_is_the_target_order`

identity: the digest covers the set of rows and not their order, so a target that moved keeps its digest

- File: `src/cratekit/favorites/order.py`
- Source: `u180.json`, row `M15_digest_is_the_target_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_the_digest_moves_when_the_target_order_moves_and_not_otherwise`

Old text:

```
            "order": [one.row for one in self.children],
```

New text:

```
            "order": sorted(one.row for one in self.children),
```

### `u180.M16_stale_digest_refused`

apply: a digest that moved since the approval is not refused, so an order nobody approved is written

- File: `src/cratekit/favorites/order.py`
- Source: `u180.json`, row `M16_stale_digest_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_a_folder_that_changed_after_the_approval_is_refused_and_nothing_is_written`

Old text:

```
    if again.digest != approved.digest:
```

New text:

```
    if False:
```

### `u180.M17_confined_seated_position`

order_violations: a seated row is not asked whether it took its planned position

- File: `src/cratekit/favorites/order.py`
- Source: `u180.json`, row `M17_confined_seated_position`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_an_order_reaching_what_it_did_not_plan_is_a_violation[not-made]`

Old text:

```
            or int(row[seq_at] or 0) != slot
        ):
```

New text:

```
        ):
```

### `u180.M18_confined_unplanned_rows`

order_violations: any playlist row may change its position and bookkeeping, planned or not

- File: `src/cratekit/favorites/order.py`
- Source: `u180.json`, row `M18_confined_unplanned_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 30 against a baseline of 30
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_an_order_reaching_what_it_did_not_plan_is_a_violation[source-moved]`
  - `tests/test_favorites_order.py::test_an_order_reaching_what_it_did_not_plan_is_a_violation[unplanned-move]`

Old text:

```
        allowed = _SEATED_COLUMNS if key in planned else frozenset()
```

New text:

```
        allowed = _SEATED_COLUMNS
```

### `u180.M19_confined_memberships`

order_violations: a membership that changed is not a violation

- File: `src/cratekit/favorites/order.py`
- Source: `u180.json`, row `M19_confined_memberships`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_an_order_reaching_what_it_did_not_plan_is_a_violation[membership-changed]`

Old text:

```
        if before.memberships[key] != after.memberships[key]:
```

New text:

```
        if False:
```

### `u180.M20_confined_content`

order_violations: a content row that changed is not a violation

- File: `src/cratekit/favorites/order.py`
- Source: `u180.json`, row `M20_confined_content`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_an_order_reaching_what_it_did_not_plan_is_a_violation[content-changed]`

Old text:

```
    if before.content != after.content:
        violations.append(
            f"a {rb_writer.CONTENT_TABLE} row changed, and an order touches no track"
```

New text:

```
    if False:
        violations.append(
            f"a {rb_writer.CONTENT_TABLE} row changed, and an order touches no track"
```

### `u180.M21_confinement_called`

apply: the commit is not confined from SQL, so a write beyond the positions lands

- File: `src/cratekit/favorites/order.py`
- Source: `u180.json`, row `M21_confinement_called`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_the_writer_refuses_an_order_that_reached_a_name`

Old text:

```
                assert_order_confined(
                    db,
                    before,
```

New text:

```
                (lambda *a, **k: None)(
                    db,
                    before,
```

### `u180.M22_read_back_compares`

_read_back: the folder read back is never compared with the plan, so a clean answer is given over any order

- File: `src/cratekit/favorites/order.py`
- Source: `u180.json`, row `M22_read_back_compares`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_the_read_back_names_a_folder_that_does_not_read_in_the_planned_order`

Old text:

```
    if found == wanted:
        return ()
```

New text:

```
    if True:
        return ()
```

### `u180-m25.M25_read_back_asserted`

favorites_order: a read back that disagrees with the plan is not refused, measured again once a test drove the verb's refusal

- File: `src/cratekit/favorites/order_cli.py`
- Source: `u180-m25.json`, row `M25_read_back_asserted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_the_verb_refuses_an_answer_the_read_back_does_not_hold`

Old text:

```
    order.assert_read_back(done)
```

New text:

```
    pass
```

### `u138.S7_verb_drops_the_answer`

The verb never hands down who answered the gate

- File: `src/cratekit/session/cli.py`
- Source: `u138.json`, row `S7_verb_drops_the_answer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 7 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_a_person_at_a_terminal_mints_by_the_terminal_rule_and_the_record_says_so`
  - `tests/test_session_ack_by_session.py::test_a_session_with_a_terminal_is_still_held_to_the_ages`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-exactly-five]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-never-recorded]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-recorded-in-the-future]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[files-six-days]`
  - `tests/test_session_ack_by_session.py::test_the_session_mints_with_no_terminal_when_both_ages_are_under_five_days`

Old text:

```
        cfg, now=now, decided_by=answered.actor if answered is not None else None

```

New text:

```
        cfg, now=now, decided_by=None

```

### `u184.A10_summary_always_recorded`

_summary: say recorded whether or not this call minted

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A10_summary_always_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_one_command_reports_a_valid_acknowledgment_and_does_not_mint_again`

Old text:

```
        "recorded": minted,
```

New text:

```
        "recorded": True,
```

### `u184.A11_wording_swapped`

_expiry_row: swap the two phrasings, so a mint reads as already on record

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A11_wording_swapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_one_command_prints_the_expiry_a_person_reads`
  - `tests/test_session_ack_by_session.py::test_one_command_reports_a_valid_acknowledgment_and_does_not_mint_again`

Old text:

```
    said = "recorded now" if minted else "already on record, not minted again"
```

New text:

```
    said = "already on record, not minted again" if minted else "recorded now"
```

### `u184.A3_engine_rule_not_selected`

_mint_as_session: hand no actor to the engine, so the terminal rule decides and the ages are not judged

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A3_engine_rule_not_selected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 9 (killed)
- Killed:
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
        cfg, now=now, decided_by=session.SESSION_ACTOR
    )
```

New text:

```
        cfg, now=now, decided_by=None
    )
```

### `u184.A4_valid_record_minted_again`

_mint_as_session: never report a valid acknowledgment, so every call mints a fresh one

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A4_valid_record_minted_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_a_valid_acknowledgment_a_person_minted_is_reported_over_old_backups`
  - `tests/test_session_ack_by_session.py::test_one_command_reports_a_valid_acknowledgment_and_does_not_mint_again`

Old text:

```
    if recorded is not None and recorded.valid_at(now):
```

New text:

```
    if False:
```

### `u184.A5_expired_reported_valid`

_mint_as_session: drop the window check, so an expired acknowledgment is reported as on record

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A5_expired_reported_valid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_an_expired_acknowledgment_is_replaced_by_one_command`

Old text:

```
    if recorded is not None and recorded.valid_at(now):
```

New text:

```
    if recorded is not None:
```

### `u184.A6_unreadable_record_refuses`

_mint_as_session: let an unreadable record raise, so a damaged file can never be replaced by the session

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A6_unreadable_record_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_an_unreadable_acknowledgment_is_replaced_by_one_command`

Old text:

```
    except CratekitError:
        recorded = None
```

New text:

```
    except CratekitError:
        raise
```

### `u184.A7_already_valid_says_ok`

_mint_as_session: report an existing acknowledgment as an ok run rather than a no op

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A7_already_valid_says_ok`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_one_command_reports_a_valid_acknowledgment_and_does_not_mint_again`

Old text:

```
                "summary": _summary(recorded, minted=False),
            },
            outcome=Outcome.NO_OP,
```

New text:

```
                "summary": _summary(recorded, minted=False),
            },
            outcome=Outcome.OK,
```

### `u184.A8_expiry_row_dropped`

_mint_as_session: leave the expiry row out of a mint, so a person at a terminal is never shown it

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A8_expiry_row_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_one_command_prints_the_expiry_a_person_reads`

Old text:

```
                _expiry_row(acknowledgment, minted=True),
```

New text:

```
(empty)
```

### `u184.A9_expiry_row_names_the_mint`

_expiry_row: name the moment recorded where the expiry belongs

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A9_expiry_row_names_the_mint`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_one_command_prints_the_expiry_a_person_reads`

Old text:

```
            f"{acknowledgment.expires_at.isoformat()}"
```

New text:

```
            f"{acknowledgment.recorded_at.isoformat()}"
```

### `u204.O2_unfavourite_leaves_months`

_plan_favourites: an unfavourite leaves All Favorites alone and stays in its months

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u204.json`, row `O2_unfavourite_leaves_months`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 233 against a baseline of 233
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_track_removed_from_all_favorites_leaves_the_favorites_folder`

Old text:

```
            leave += [(pid, folder, name) for name, pid in filing if pid in held]
```

New text:

```
            leave += []
```

### `u204.O3_quarter_refused`

_plan_favourites: a favourite put in a quarter is filed into it

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u204.json`, row `O3_quarter_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 233 against a baseline of 233
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_track_put_in_a_quarter_is_named_and_not_filed`

Old text:

```
            if placeholders.MONTH_LABEL.fullmatch(month) is None and month != placeholders.UNDATED:
```

New text:

```
            if False:
```

### `u204.O4_colour`

_plan_favourites: a favourite with no colour is not coloured Pink

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u204.json`, row `O4_colour`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 233 against a baseline of 233
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_track_added_to_all_favorites_is_favourited_in_its_month_and_coloured`

Old text:

```
        takes = bool(pink) and decision.content_id in colour.sort_rows(db, pink, [decision.content_id]).to_colour
```

New text:

```
        takes = False
```

### `u204.O5_batch_live`

_plan_inbox: a batch no longer directly under INBOX is written as if it were

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u204.json`, row `O5_batch_live`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 233 against a baseline of 233
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_batch_moved_into_old_since_the_plan_is_never_touched`

Old text:

```
        if len(found) != 1:
```

New text:

```
        if False:
```

### `u204.O6_inbox_latch`

write: an INBOX edit asks no intake tree latch

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u204.json`, row `O6_inbox_latch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 233 against a baseline of 233
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_an_inbox_edit_over_a_latched_intake_tree_writes_nothing`

Old text:

```
    if edits.INBOX in touched:
```

New text:

```
    if False:
```

### `u204.O7_restore_detected`

write: a favourites only write detects no out of band restore

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u204.json`, row `O7_restore_detected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 233 against a baseline of 233
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_favourites_only_write_detects_an_out_of_band_restore_and_asks_no_tree_latch`

Old text:

```
    if touched and not touched & {edits.GENRE, edits.INBOX}:
```

New text:

```
    if False:
```

### `u161.L1_landing_pins_nothing`

ask_then_write: pin nothing, so every native write's answer is free of the file again

- File: `src/cratekit/intake/land_cli.py`
- Source: `u161.json`, row `L1_landing_pins_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_an_answer_given_over_one_file_is_stale_when_the_continuation_opens_another`

Old text:

```
            spec, plan=data, context=shown(rows), pinned={DATABASE_PIN: str(opened)}
```

New text:

```
            spec, plan=data, context=shown(rows), pinned={}
```

