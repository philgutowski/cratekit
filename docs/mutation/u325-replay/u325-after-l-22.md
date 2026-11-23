# Mutation table: u325-after-l-22

Measured by `scripts/mutate.py` on 2026-11-22 23:33 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 144.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:21 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 17, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
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
| `r1394.S10_later_unsent_write_hides_the_pending` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 3 | killed |
| `r1394.S1_counts_beyond_the_moves_trusted` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 1 | killed |
| `r1394.S2_missing_counts_read_as_none_sent` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 7 | killed |
| `r1394.S6_counts_not_wired` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 14 | killed |
| `r1394.S8_positions_first_only` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 2 | killed |
| `r1394.S9_moving_step_counts_dropped` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 19 | killed |
| `u234.O15_reordered_counts_additions` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 1 | killed |
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
| `r1694.L1_login_no_tolerance` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 164 | 7 | killed |
| `r1694.L2_token_file_uncaught` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 164 | 1 | killed |
| `r1694.L3_token_file_catches_defect` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 164 | 1 | killed |
| `r1694.L4_rewrite_unchanged` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 164 | 2 | killed |
| `r1694.L5_hold_the_refresh` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 164 | 2 | killed |
| `r1694.L6_no_note` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 164 | 8 | killed |
| `r1694.L7_note_the_words` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 164 | 7 | killed |
| `u62.S1_device_flow_login` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 331 | 1 | killed |
| `u62.S2_401_not_rejected` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 331 | 2 | killed |
| `u62.S4_every_failure_rejected` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 331 | 4 | killed |
| `u62.S5_blob_without_token_logged_in` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 331 | 1 | killed |
| `u62.S6_refresh_not_written_back` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 331 | 1 | killed |
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
| `u238.M10_question_drops_the_split` | `src/cratekit/label/sync_cli.py` | user | 3 file(s) | 319 | 3 | killed |
| `u238.M11_saved_question_drops_the_split` | `src/cratekit/label/sync_cli.py` | user | 3 file(s) | 319 | 3 | killed |
| `u238.M7_old_question_read_as_count` | `src/cratekit/label/sync_cli.py` | user | 3 file(s) | 319 | 5 | killed |
| `u238.M8_bound_said_as_the_labels` | `src/cratekit/label/sync_cli.py` | user | 3 file(s) | 319 | 8 | killed |
| `u238.M9_nothing_line_loses_the_split` | `src/cratekit/label/sync_cli.py` | user | 3 file(s) | 319 | 2 | killed |
| `u104-d.C2_refusal_named_for_the_address` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 154 | 1 | killed |
| `u104-d.C3_detail_renamed` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 154 | 1 | killed |
| `u104-d.C4_scratch_left_said` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 154 | 1 | killed |
| `u104-d.C5_no_digest_token_is_the_address` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 154 | 1 | killed |
| `u104-e.E2_timeout_is_retryable` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 154 | 1 | killed |
| `u104-e.E3_honest_zero_names_the_address` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 154 | 1 | killed |
| `u104-e.E4_identify_library_before_fetch` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 154 | 2 | killed |
| `r668-a.M1_list_required_again` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 39 | killed |
| `r668-a.M2_resume_argv_carries_the_list` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 2 | killed |
| `r668-a.M3_no_empty_job_guard` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `r668-a.M4_no_missing_list_guard` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 2 | killed |
| `r668-a.M6_no_list_check_on_resume` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 3 | killed |
| `r668-a.M9_other_verbs_job_read` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `r668-b.M12_home_expansion_raises` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `r668-b.M8_named_not_absolutised` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `r318.P1_withdrawn_branch_removed` | `src/cratekit/write/routing_pass.py` | user | 4 file(s) | 437 | 5 | killed |
| `r318.P2_withdrawn_on_single_tombstone_only` | `src/cratekit/write/routing_pass.py` | user | 4 file(s) | 437 | 1 | killed |
| `r318.P3_unresolved_branch_removed` | `src/cratekit/write/routing_pass.py` | user | 4 file(s) | 437 | 3 | killed |
| `r318.P4_ambiguous_reads_not_imported` | `src/cratekit/write/routing_pass.py` | user | 4 file(s) | 437 | 3 | killed |
| `u51-item-derivation.A2_default_favorites_playlist` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 145 | 27 | killed |
| `u51-item-derivation.D1_unknown_playlist` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 145 | 2 | killed |
| `u51-item-derivation.D2_ambiguous_playlist` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 145 | 1 | killed |
| `u51-item-derivation.D3_empty_playlist` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 145 | 1 | killed |
| `u51-item-derivation.D4_dangling_reported` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 145 | 2 | killed |
| `u51-item-derivation.D5_repeated_deduped` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 145 | 2 | killed |
| `u51-item-derivation.D6_export_required` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 145 | 2 | killed |
| `u100-b.C10_added_message` | `src/cratekit/label/cli.py` | user | 2 file(s) | 47 | 1 | killed |
| `u100-b.C1_name_accepted` | `src/cratekit/label/cli.py` | user | 2 file(s) | 47 | 1 | killed |
| `u100-b.C2_to_accepted` | `src/cratekit/label/cli.py` | user | 2 file(s) | 47 | 1 | killed |
| `u100-b.C3_outcome_always_ok` | `src/cratekit/label/cli.py` | user | 2 file(s) | 47 | 2 | killed |
| `u100-b.C4_empty_says_nothing` | `src/cratekit/label/cli.py` | user | 2 file(s) | 47 | 1 | killed |
| `u100-b.C5_nameless_unreported` | `src/cratekit/label/cli.py` | user | 2 file(s) | 47 | 1 | killed |
| `u100-b.C6_held_name_hidden` | `src/cratekit/label/cli.py` | user | 2 file(s) | 47 | 1 | killed |
| `u100-b.C7_refused_reads_as_note` | `src/cratekit/label/cli.py` | user | 2 file(s) | 47 | 1 | killed |
| `u100-b.C9_dispatch` | `src/cratekit/label/cli.py` | user | 2 file(s) | 47 | 12 | killed |
| `u149.T10_any_year_folder` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 46 | 1 | killed |
| `u149.T11_excluded_read` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 46 | 1 | killed |
| `u149.T13_paired_planned_again` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 46 | 1 | killed |
| `u149.T15_unplanned_membership` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 46 | 1 | killed |
| `u149.T16_unplanned_playlist_row` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 46 | 2 | killed |

## Row definitions

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

### `r1394.S10_later_unsent_write_hides_the_pending`

stopped writes: the latest record is read whether or not it sent a move, so a refused finish hides the pending write it was finishing, round two's BLOCKING row

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1394.json`, row `S10_later_unsent_write_hides_the_pending`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`
- Collected: 177 against a baseline of 177
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_the_adapter_refuses_leaves_the_stopped_write_pending`
  - `tests/test_sync_pair_stopped.py::test_a_later_write_that_sent_no_move_does_not_hide_a_pending_one`

Old text:

```
            if held is None or (write.pending, write.at) > (held[1].pending, held[1].at):
```

New text:

```
            if held is None or write.at > held[1].at:
```

### `r1394.S1_counts_beyond_the_moves_trusted`

stopped write: counts larger than the write's moves are trusted rather than read as nothing known

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1394.json`, row `S1_counts_beyond_the_moves_trusted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`
- Collected: 177 against a baseline of 177
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts3]`

Old text:

```
    if sent is None or landed is None or not landed <= sent <= total:
```

New text:

```
    if sent is None or landed is None or not landed <= sent:
```

### `r1394.S2_missing_counts_read_as_none_sent`

stopped write: a moving step with no counts reads as no move sent, so any agreed path reading finishes it, as before R-1394

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1394.json`, row `S2_missing_counts_read_as_none_sent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`
- Collected: 177 against a baseline of 177
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_stopped_write_recorded_with_no_counts_is_finished_only_from_the_order_it_leaves`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts0]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts1]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts2]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts3]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts4]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts5]`

Old text:

```
        return 0, total
    return landed, sent
```

New text:

```
        return 0, 0
    return landed, sent
```

### `r1394.S6_counts_not_wired`

stopped write: the counts read back never reach the stopped write, which keeps none landed and none sent

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1394.json`, row `S6_counts_not_wired`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`
- Collected: 177 against a baseline of 177
- Kills: 14 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_the_adapter_refuses_leaves_the_stopped_write_pending`
  - `tests/test_sync_pair_settle.py::test_a_move_whose_fate_is_unknown_holds_the_order_before_it_and_finishes_the_one_after`
  - `tests/test_sync_pair_settle.py::test_a_stop_after_one_of_three_moves_read_as_the_old_order_is_held_however_long_it_agrees`
  - `tests/test_sync_pair_settle.py::test_a_stopped_write_recorded_with_no_counts_is_finished_only_from_the_order_it_leaves`
  - `tests/test_sync_pair_settle.py::test_a_stopped_writes_counts_are_carried_past_its_runs_steps`
  - `tests/test_sync_pair_settle.py::test_every_move_accepted_and_an_agreed_reading_short_of_their_end_is_still_a_lag`
  - `tests/test_sync_pair_stopped.py::test_a_moving_step_reads_back_its_counts`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts0]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts1]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts2]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts3]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts4]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts5]`
  - `tests/test_sync_pair_stopped.py::test_every_move_accepted_reads_as_every_move_landed_whatever_the_counts`

Old text:

```
        landed=landed,
        sent=reached_by,
```

New text:

```
        landed=0,
        sent=0,
```

### `r1394.S8_positions_first_only`

positions: only the first count on the path that leaves the order is answered, so a track taken off since hides a later one

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1394.json`, row `S8_positions_first_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`
- Collected: 177 against a baseline of 177
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_an_unread_track_taken_off_the_account_after_the_stop_is_never_put_back`
  - `tests/test_sync_pair_stopped.py::test_orders_on_the_path_that_differ_only_by_a_track_taken_off_all_count`

Old text:

```
    return tuple(
        index
        for index, state in enumerate(passed(start, target))
        if [one for one in dict.fromkeys(state) if one in common] == shown
    )
```

New text:

```
    return tuple(
        index
        for index, state in enumerate(passed(start, target))
        if [one for one in dict.fromkeys(state) if one in common] == shown
    )[:1]
```

### `r1394.S9_moving_step_counts_dropped`

moving step: the record written carries a sent count of 0 whatever it is told

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1394.json`, row `S9_moving_step_counts_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`
- Collected: 177 against a baseline of 177
- Kills: 19 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_keeps_an_unread_track_the_stopped_write_did_not_move_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_finish_planned_again_in_the_writing_command_is_held_to_its_own_reading`
  - `tests/test_sync_pair_settle.py::test_a_finish_puts_an_unread_track_the_stopped_move_put_in_front_where_the_write_was_taking_it`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_served_as_the_moves_left_it_finishes`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_removes_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_the_adapter_refuses_leaves_the_stopped_write_pending`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_finish_with_no_unread_track_is_put_in_rekordboxs_order`
  - `tests/test_sync_pair_settle.py::test_a_move_whose_fate_is_unknown_holds_the_order_before_it_and_finishes_the_one_after`
  - `tests/test_sync_pair_settle.py::test_a_stop_after_one_of_three_moves_read_as_that_move_leaves_it_is_finished`
  - `tests/test_sync_pair_settle.py::test_a_stop_after_one_of_three_moves_read_as_the_old_order_is_held_however_long_it_agrees`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        SENT: int(sent),
```

New text:

```
        SENT: 0,
```

### `u234.O15_reordered_counts_additions`

reordered compares the readings whole, so a track added between them is read as a reorder

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `u234.json`, row `O15_reordered_counts_additions`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`
- Collected: 177 against a baseline of 177
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_track_added_or_taken_off_between_two_readings_is_no_reorder`

Old text:

```
    return [one for one in current if one in common] != [
        one for one in dict.fromkeys(kept) if one in common
    ]


__all__
```

New text:

```
    return current != list(dict.fromkeys(kept))


__all__
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

### `r1694.L1_login_no_tolerance`

_login: open the scope with no tolerance, so the login fails as it did before R-1694

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `L1_login_no_tolerance`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`
- Collected: 164 against a baseline of 164
- Kills: 7 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_a_refreshed_login_the_keychain_cannot_take_returns_the_client`
  - `tests/test_provider_session_unstored.py::test_a_verb_whose_login_refreshed_on_the_opt_in_answers_as_before_and_warns`
  - `tests/test_provider_session_unstored.py::test_an_index_that_cannot_be_locked_is_noted_and_the_keychain_is_untouched`
  - `tests/test_provider_session_unstored.py::test_an_index_that_refuses_after_the_keychain_took_the_refresh_is_noted`
  - `tests/test_provider_session_unstored.py::test_the_held_session_is_the_stored_one_so_a_reuse_neither_logs_in_nor_warns_again`
  - `tests/test_provider_session_unstored.py::test_the_warning_is_this_verbs_alone`
  - `tests/test_provider_session_unstored.py::test_two_failed_stores_in_one_verb_make_one_warning_naming_the_class_once`

Old text:

```
    with materialised_session(name, unstored=failed.append) as scope:
```

New text:

```
    with materialised_session(name) as scope:
```

### `r1694.L2_token_file_uncaught`

_login: let a token file the refresh cannot be written to raise, so a full temporary disk fails the login

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `L2_token_file_uncaught`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`
- Collected: 164 against a baseline of 164
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_a_token_file_that_cannot_take_the_refresh_is_noted`

Old text:

```
            except OSError as exc:
                failed.append(exc)
    if failed:
```

New text:

```
            except ArithmeticError as exc:
                failed.append(exc)
    if failed:
```

### `r1694.L3_token_file_catches_defect`

_login: catch every exception at the token file write, so a field the file cannot encode is a warning rather than a defect

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `L3_token_file_catches_defect`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`
- Collected: 164 against a baseline of 164
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_a_defect_in_the_capture_still_raises`

Old text:

```
            except OSError as exc:
                failed.append(exc)
    if failed:
```

New text:

```
            except Exception as exc:
                failed.append(exc)
    if failed:
```

### `r1694.L4_rewrite_unchanged`

_login: rewrite the token file for an unchanged session too, so a file that cannot be written is reported over a session with nothing to store

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `L4_rewrite_unchanged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`
- Collected: 164 against a baseline of 164
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_a_defect_in_the_capture_still_raises`
  - `tests/test_provider_session_unstored.py::test_an_unchanged_session_never_rewrites_the_token_file`

Old text:

```
        if _canonical(refreshed) != _canonical(stored):
```

New text:

```
        if _canonical(refreshed) is not None:
```

### `r1694.L5_hold_the_refresh`

_login: return the refresh as what the keychain holds after a store failure, so every later resolve logs in again and fails to store again

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `L5_hold_the_refresh`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`
- Collected: 164 against a baseline of 164
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_the_held_session_is_the_stored_one_so_a_reuse_neither_logs_in_nor_warns_again`
  - `tests/test_provider_session_unstored.py::test_the_warning_is_this_verbs_alone`

Old text:

```
        return client, stored
    return client, refreshed
```

New text:

```
        return client, refreshed
    return client, refreshed
```

### `r1694.L6_no_note`

_login: note nothing on a store failure, so the verb never says the session was not stored

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `L6_no_note`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`
- Collected: 164 against a baseline of 164
- Kills: 8 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_a_refreshed_login_the_keychain_cannot_take_returns_the_client`
  - `tests/test_provider_session_unstored.py::test_a_token_file_that_cannot_take_the_refresh_is_noted`
  - `tests/test_provider_session_unstored.py::test_a_verb_whose_login_refreshed_on_the_opt_in_answers_as_before_and_warns`
  - `tests/test_provider_session_unstored.py::test_an_index_that_cannot_be_locked_is_noted_and_the_keychain_is_untouched`
  - `tests/test_provider_session_unstored.py::test_an_index_that_refuses_after_the_keychain_took_the_refresh_is_noted`
  - `tests/test_provider_session_unstored.py::test_the_held_session_is_the_stored_one_so_a_reuse_neither_logs_in_nor_warns_again`
  - `tests/test_provider_session_unstored.py::test_the_warning_is_this_verbs_alone`
  - `tests/test_provider_session_unstored.py::test_two_failed_stores_in_one_verb_make_one_warning_naming_the_class_once`

Old text:

```
        _UNSTORED.extend(type(exc).__name__ for exc in failed)
```

New text:

```
        pass
```

### `r1694.L7_note_the_words`

_login: note the failure's words rather than its class, so a credential refusal's setup advice reaches the warning

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `L7_note_the_words`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`
- Collected: 164 against a baseline of 164
- Kills: 7 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_a_refreshed_login_the_keychain_cannot_take_returns_the_client`
  - `tests/test_provider_session_unstored.py::test_a_token_file_that_cannot_take_the_refresh_is_noted`
  - `tests/test_provider_session_unstored.py::test_a_verb_whose_login_refreshed_on_the_opt_in_answers_as_before_and_warns`
  - `tests/test_provider_session_unstored.py::test_an_index_that_cannot_be_locked_is_noted_and_the_keychain_is_untouched`
  - `tests/test_provider_session_unstored.py::test_an_index_that_refuses_after_the_keychain_took_the_refresh_is_noted`
  - `tests/test_provider_session_unstored.py::test_the_held_session_is_the_stored_one_so_a_reuse_neither_logs_in_nor_warns_again`
  - `tests/test_provider_session_unstored.py::test_two_failed_stores_in_one_verb_make_one_warning_naming_the_class_once`

Old text:

```
        _UNSTORED.extend(type(exc).__name__ for exc in failed)
```

New text:

```
        _UNSTORED.extend(str(exc) for exc in failed)
```

### `u62.S1_device_flow_login`

Log in as a device flow session rather than PKCE

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u62.json`, row `S1_device_flow_login`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/test_adapter_contract.py`
- Collected: 331 against a baseline of 331
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_recorded_session_resolves_the_adapter_over_a_pkce_login`

Old text:

```
                is_pkce=True,
```

New text:

```
                is_pkce=False,
```

### `u62.S2_401_not_rejected`

Drop 401 from the statuses read as a rejected session

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u62.json`, row `S2_401_not_rejected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/test_adapter_contract.py`
- Collected: 331 against a baseline of 331
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_session_the_provider_rejects_asks_for_a_new_login_not_a_first_one[401]`
  - `tests/test_label_tidal_catalogue.py::test_a_session_the_provider_rejects_asks_for_a_new_login_not_a_first_one[chained-401]`

Old text:

```
REJECTED_STATUSES = frozenset({400, 401, 403})
```

New text:

```
REJECTED_STATUSES = frozenset({400, 403})
```

### `u62.S4_every_failure_rejected`

Read every login failure as a rejected session, the pre review behaviour

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u62.json`, row `S4_every_failure_rejected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/test_adapter_contract.py`
- Collected: 331 against a baseline of 331
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_provider_that_cannot_be_reached_is_a_wait_not_a_new_login[connection]`
  - `tests/test_label_tidal_catalogue.py::test_a_provider_that_cannot_be_reached_is_a_wait_not_a_new_login[server-error]`
  - `tests/test_label_tidal_catalogue.py::test_a_provider_that_cannot_be_reached_is_a_wait_not_a_new_login[timeout]`
  - `tests/test_label_tidal_catalogue.py::test_a_provider_that_cannot_be_reached_is_a_wait_not_a_new_login[unparseable-page]`

Old text:

```
            if _rejected(exc):
```

New text:

```
            if True:
```

### `u62.S5_blob_without_token_logged_in`

Hand a blob with no access token to the provider

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u62.json`, row `S5_blob_without_token_logged_in`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/test_adapter_contract.py`
- Collected: 331 against a baseline of 331
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_stored_blob_with_no_access_token_never_reaches_the_provider`

Old text:

```
        if not isinstance(stored, dict) or not stored.get("access_token"):
```

New text:

```
        if not isinstance(stored, dict):
```

### `u62.S6_refresh_not_written_back`

Write the stored blob back unchanged instead of the refreshed tokens

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u62.json`, row `S6_refresh_not_written_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/test_adapter_contract.py`
- Collected: 331 against a baseline of 331
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_refresh_during_login_is_written_back_to_the_keychain`

Old text:

```
            if value is not None:
                refreshed[field] = _epoch(value)
```

New text:

```
            if value is not None and False:
                refreshed[field] = _epoch(value)
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

### `u238.M10_question_drops_the_split`

_question_for: build the question without the listing's unchecked count

- File: `src/cratekit/label/sync_cli.py`
- Source: `u238.json`, row `M10_question_drops_the_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`, `tests/test_sync_all.py`
- Collected: 319 against a baseline of 319
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_newly_followed_label_is_offered_at_most_its_offer_per_sweep_newest`
  - `tests/test_label_sync.py::test_a_question_counts_only_the_labels_own_releases_past_its_window`
  - `tests/test_label_sync.py::test_an_unread_listing_still_says_so_beside_the_count_past_the_window`

Old text:

```
            beyond_unchecked=listing.beyond_unchecked,

```

New text:

```
(empty)
```

### `u238.M11_saved_question_drops_the_split`

Question.to_json: save no unchecked count, so a saved question reread says its own as a bound

- File: `src/cratekit/label/sync_cli.py`
- Source: `u238.json`, row `M11_saved_question_drops_the_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`, `tests/test_sync_all.py`
- Collected: 319 against a baseline of 319
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_newly_followed_label_is_offered_at_most_its_offer_per_sweep_newest`
  - `tests/test_label_sync.py::test_a_question_counts_only_the_labels_own_releases_past_its_window`
  - `tests/test_label_sync.py::test_an_unread_listing_still_says_so_beside_the_count_past_the_window`

Old text:

```
            "beyond_unchecked": self.beyond_unchecked,

```

New text:

```
(empty)
```

### `u238.M7_old_question_read_as_count`

Question.from_json: a question saved before the split reads none as unchecked, so 414 is said as the label's

- File: `src/cratekit/label/sync_cli.py`
- Source: `u238.json`, row `M7_old_question_read_as_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`, `tests/test_sync_all.py`
- Collected: 319 against a baseline of 319
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_question_saved_before_the_count_was_split_reads_as_a_bound`
  - `tests/test_label_sync.py::test_a_saved_split_that_cannot_be_read_reads_as_a_bound[-1]`
  - `tests/test_label_sync.py::test_a_saved_split_that_cannot_be_read_reads_as_a_bound[9]`
  - `tests/test_label_sync.py::test_a_saved_split_that_cannot_be_read_reads_as_a_bound[None]`
  - `tests/test_label_sync.py::test_a_saved_split_that_cannot_be_read_reads_as_a_bound[True]`

Old text:

```
            beyond_unchecked=beyond if unchecked is None else min(beyond, unchecked),
```

New text:

```
            beyond_unchecked=0 if unchecked is None else min(beyond, unchecked),
```

### `u238.M8_bound_said_as_the_labels`

sync_cli._past_window: say the unchecked alone as the label's releases rather than as a bound

- File: `src/cratekit/label/sync_cli.py`
- Source: `u238.json`, row `M8_bound_said_as_the_labels`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`, `tests/test_sync_all.py`
- Collected: 319 against a baseline of 319
- Kills: 8 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_newly_followed_label_is_offered_at_most_its_offer_per_sweep_newest`
  - `tests/test_label_sync.py::test_a_question_saved_before_the_count_was_split_reads_as_a_bound`
  - `tests/test_label_sync.py::test_a_saved_split_larger_than_its_figure_is_held_to_the_figure`
  - `tests/test_label_sync.py::test_a_saved_split_that_cannot_be_read_reads_as_a_bound[-1]`
  - `tests/test_label_sync.py::test_a_saved_split_that_cannot_be_read_reads_as_a_bound[9]`
  - `tests/test_label_sync.py::test_a_saved_split_that_cannot_be_read_reads_as_a_bound[None]`
  - `tests/test_label_sync.py::test_a_saved_split_that_cannot_be_read_reads_as_a_bound[True]`
  - `tests/test_label_sync.py::test_the_phrase_past_the_window_is_a_count_or_a_bound_and_never_zero`

Old text:

```
        said = f"up to {unchecked} more past this run's window, not yet checked"
```

New text:

```
        said = f"{unchecked} more of the label's release(s) past this run's window"
```

### `u238.M9_nothing_line_loses_the_split`

sync_cli._nothing_check: pass no unchecked count, so the nothing new line says every release as the label's

- File: `src/cratekit/label/sync_cli.py`
- Source: `u238.json`, row `M9_nothing_line_loses_the_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`, `tests/test_sync_all.py`
- Collected: 319 against a baseline of 319
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync.py::test_nothing_new_after_an_answer_says_the_count_past_the_window`
  - `tests/test_label_sync.py::test_nothing_new_says_the_count_past_the_window_the_same_way`

Old text:

```
        past = _past_window(listed.listing.beyond, listed.listing.beyond_unchecked)
```

New text:

```
        past = _past_window(listed.listing.beyond, 0)
```

### `u104-d.C2_refusal_named_for_the_address`

Let a refusal raised inside the identifier through as it is, naming the scratch file in its message and detail

- File: `src/cratekit/intake/cli.py`
- Source: `u104-d.json`, row `C2_refusal_named_for_the_address`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`
- Collected: 154 against a baseline of 154
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_refusal_from_inside_the_identifier_names_the_address_and_not_the_scratch_file`

Old text:

```
                raise _named_for_the_address(exc, held) from exc.__cause__
```

New text:

```
                raise
```

### `u104-d.C3_detail_renamed`

Rename the message only and leave the scratch path in the refusal's detail

- File: `src/cratekit/intake/cli.py`
- Source: `u104-d.json`, row `C3_detail_renamed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`
- Collected: 154 against a baseline of 154
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_refusal_from_inside_the_identifier_names_the_address_and_not_the_scratch_file`

Old text:

```
        key: held.ref if value == str(held.path) else value
```

New text:

```
        key: value
```

### `u104-d.C4_scratch_left_said`

Never say that a scratch folder outlived its pass

- File: `src/cratekit/intake/cli.py`
- Source: `u104-d.json`, row `C4_scratch_left_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`
- Collected: 154 against a baseline of 154
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_scratch_folder_that_cannot_be_removed_is_said_on_the_envelope`

Old text:

```
    if held.leftover is None:
        return ()
```

New text:

```
    if held.leftover is None or True:
        return ()
```

### `u104-d.C5_no_digest_token_is_the_address`

Take a digestless tracklist's token from the scratch path, which every fetched mix shares, instead of from the address

- File: `src/cratekit/intake/cli.py`
- Source: `u104-d.json`, row `C5_no_digest_token_is_the_address`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`
- Collected: 154 against a baseline of 154
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_fetched_mix_with_no_digest_is_named_by_its_address_and_not_its_scratch_file`

Old text:

```
    token = digest or digest_of({"path": held.ref})
```

New text:

```
    token = digest or digest_of({"path": str(held.path)})
```

### `u104-e.E2_timeout_is_retryable`

Stop calling a timed out download retryable, the one fetch failure known to be worth running again

- File: `src/cratekit/intake/cli.py`
- Source: `u104-e.json`, row `E2_timeout_is_retryable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`
- Collected: 154 against a baseline of 154
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_download_that_timed_out_is_the_one_fetch_failure_called_retryable`

Old text:

```
            remedy=Remedy.RETRY_LATER,
            retryable=True,
            steps=(
                "run it again later",
```

New text:

```
            remedy=Remedy.RETRY_LATER,
            retryable=False,
            steps=(
                "run it again later",
```

### `u104-e.E3_honest_zero_names_the_address`

Report the scratch file's path as the source of a mix nobody recognised

- File: `src/cratekit/intake/cli.py`
- Source: `u104-e.json`, row `E3_honest_zero_names_the_address`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`
- Collected: 154 against a baseline of 154
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_mix_nobody_recognised_is_an_honest_zero_that_names_the_address`

Old text:

```
                    chunks=result.chunks,
                    source=held.ref,
```

New text:

```
                    chunks=result.chunks,
                    source=str(held.path),
```

### `u104-e.E4_identify_library_before_fetch`

Drop intake identify's check that the library is there to be asked, which runs before anything is fetched or sent

- File: `src/cratekit/intake/cli.py`
- Source: `u104-e.json`, row `E4_identify_library_before_fetch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`
- Collected: 154 against a baseline of 154
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_identify_over_a_url_refuses_an_absent_library_before_anything_is_fetched`
  - `tests/intake/test_workers.py::test_an_absent_library_is_refused_before_the_spend_and_never_read_as_an_empty_one`

Old text:

```
    _library_or_refuse(cfg, shown)

```

New text:

```
(empty)
```

### `r668-a.M1_list_required_again`

the list positional is required again, so --job alone is argparse's usage error, the defect sitting 7 hit

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-a.json`, row `M1_list_required_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 93 against a baseline of 93
- Kills: 39 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_broken_adapter_fails_the_item_and_does_not_park_the_run`
  - `tests/test_acquire_workers.py::test_a_command_naming_nothing_is_refused_before_the_configuration_is_read`
  - `tests/test_acquire_workers.py::test_a_configuration_naming_an_unknown_adapter_fails_the_item_by_name`
  - `tests/test_acquire_workers.py::test_a_dead_session_logs_in_once_and_not_once_per_track`
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
  - ... and 24 more, see the JSON sidecar

Old text:

```
        "list",
        nargs="?",
        default=None,

```

New text:

```
        "list",

```

### `r668-a.M2_resume_argv_carries_the_list`

the resume argv and the drive it with line name the frozen list again

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-a.json`, row `M2_resume_argv_carries_the_list`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 93 against a baseline of 93
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_download_argv_round_trips_the_frozen_payload_and_carries_no_run`
  - `tests/test_acquire_workers.py::test_queueing_a_download_names_the_job_and_the_command_that_drives_it`

Old text:

```
    return ["acquire", "download", "--job", job.job_id]
```

New text:

```
    return ["acquire", "download", str((job.payload or {}).get(LIST) or ""), "--job", job.job_id]
```

### `r668-a.M3_no_empty_job_guard`

an empty --job identifier is not refused, so it falls through to the queueing path and queues the list a second time

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-a.json`, row `M3_no_empty_job_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_an_empty_job_identifier_is_refused_rather_than_queueing_the_list_again`

Old text:

```
    if ctx.args.job is not None and not ctx.args.job.strip():
        raise _unusable(
```

New text:

```
    if False:
        raise _unusable(
```

### `r668-a.M4_no_missing_list_guard`

a command naming neither a list nor a job is not refused by the verb, and reads a list called None

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-a.json`, row `M4_no_missing_list_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 93 against a baseline of 93
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_command_naming_nothing_is_refused_before_the_configuration_is_read`
  - `tests/test_acquire_workers.py::test_neither_a_list_nor_a_job_is_refused_by_the_verb_and_queues_nothing`

Old text:

```
    if ctx.args.list is None and ctx.args.job is None:
        raise _unusable(
```

New text:

```
    if False:
        raise _unusable(
```

### `r668-a.M6_no_list_check_on_resume`

a list named beside --job is never compared with the frozen one, so a different list is silently ignored and the job driven

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-a.json`, row `M6_no_list_check_on_resume`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 93 against a baseline of 93
- Kills: 3 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_different_list_named_beside_the_job_is_refused_and_nothing_is_fetched`
  - `tests/test_acquire_workers.py::test_a_list_under_a_home_that_cannot_be_expanded_is_refused_by_name`
  - `tests/test_acquire_workers.py::test_a_refused_list_leaves_a_dead_drivers_claim_for_the_resume_to_reconcile`

Old text:

```
            _same_list_or_refuse(
                ctx.args.list, jobs.get(store, ctx.args.job), ctx.entry.handler_key
            )

```

New text:

```
            pass

```

### `r668-a.M9_other_verbs_job_read`

another verb's job payload is read as a frozen download list

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-a.json`, row `M9_other_verbs_job_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_another_verbs_job_is_not_read_as_a_frozen_download_list`

Old text:

```
    if named is None or job.handler_key != handler_key:
```

New text:

```
    if named is None:
```

### `r668-b.M12_home_expansion_raises`

a named list under a home directory that cannot be expanded raises instead of being compared as typed

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-b.json`, row `M12_home_expansion_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_list_under_a_home_that_cannot_be_expanded_is_refused_by_name`

Old text:

```
    except RuntimeError:
        given = Path(named).absolute()
```

New text:

```
    except RuntimeError:
        raise
```

### `r668-b.M8_named_not_absolutised`

the named list is compared without the freeze's absolutising, so a relative spelling from the queueing directory is refused

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-b.json`, row `M8_named_not_absolutised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_deleted_frozen_list_named_relative_from_where_it_was_queued_still_drives`

Old text:

```
        given = Path(named).expanduser().absolute()
    except RuntimeError:
```

New text:

```
        given = Path(named).expanduser()
    except RuntimeError:
```

### `r318.P1_withdrawn_branch_removed`

row_placement: never answer withdrawn, so a track imported then removed in rekordbox is reported as never imported and the person is sent to import it again

- File: `src/cratekit/write/routing_pass.py`
- Source: `r318.json`, row `P1_withdrawn_branch_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`, `tests/test_intake_imported.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 437 against a baseline of 437
- Kills: 5 (killed)
- Killed:
  - `tests/test_deferred_routing.py::test_a_location_reaching_only_soft_deleted_rows_is_withdrawn`
  - `tests/test_deferred_routing.py::test_a_track_deleted_after_import_is_surfaced`
  - `tests/test_routing_workers.py::test_a_row_rekordbox_removed_is_reported_withdrawn_not_unimported`
  - `tests/test_routing_workers.py::test_the_placement_of_a_row_answer_is_one_rule[withdrawn-twice]`
  - `tests/test_routing_workers.py::test_the_placement_of_a_row_answer_is_one_rule[withdrawn]`

Old text:

```
    if removed.outcome in (trees.MatchOutcome.MATCHED, trees.MatchOutcome.AMBIGUOUS):
        # A row exists and every one of them is a tombstone: imported once, then
```

New text:

```
    if False:
        # A row exists and every one of them is a tombstone: imported once, then
```

### `r318.P2_withdrawn_on_single_tombstone_only`

row_placement: withdrawn only when exactly one tombstone claims the location, two tombstones read as not imported

- File: `src/cratekit/write/routing_pass.py`
- Source: `r318.json`, row `P2_withdrawn_on_single_tombstone_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`, `tests/test_intake_imported.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 437 against a baseline of 437
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_placement_of_a_row_answer_is_one_rule[withdrawn-twice]`

Old text:

```
    if removed.outcome in (trees.MatchOutcome.MATCHED, trees.MatchOutcome.AMBIGUOUS):
        # A row exists and every one of them is a tombstone: imported once, then
```

New text:

```
    if removed.outcome in (trees.MatchOutcome.MATCHED,):
        # A row exists and every one of them is a tombstone: imported once, then
```

### `r318.P3_unresolved_branch_removed`

row_placement: drop the unresolved answer, so a location no prefix maps falls through to not imported, a configuration failure reported as a missing import

- File: `src/cratekit/write/routing_pass.py`
- Source: `r318.json`, row `P3_unresolved_branch_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`, `tests/test_intake_imported.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 437 against a baseline of 437
- Kills: 3 (killed)
- Killed:
  - `tests/test_deferred_routing.py::test_a_location_that_resolves_to_no_path_is_not_reported_as_a_missing_import`
  - `tests/test_deferred_routing.py::test_a_run_whose_locations_all_resolve_to_nothing_is_not_told_to_import`
  - `tests/test_routing_workers.py::test_the_placement_of_a_row_answer_is_one_rule[unresolved]`

Old text:

```
    if alive.outcome is trees.MatchOutcome.UNRESOLVED:
        return Placement.UNRESOLVED

```

New text:

```
(empty)
```

### `r318.P4_ambiguous_reads_not_imported`

row_placement: two live rows claiming a location answer not imported instead of ambiguous

- File: `src/cratekit/write/routing_pass.py`
- Source: `r318.json`, row `P4_ambiguous_reads_not_imported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`, `tests/test_intake_imported.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 437 against a baseline of 437
- Kills: 3 (killed)
- Killed:
  - `tests/test_deferred_routing.py::test_two_active_rows_on_one_location_are_ambiguous_and_never_written`
  - `tests/test_routing_workers.py::test_a_file_two_rows_claim_is_reported_ambiguous_with_both_rows`
  - `tests/test_routing_workers.py::test_the_placement_of_a_row_answer_is_one_rule[ambiguous]`

Old text:

```
    if alive.outcome is trees.MatchOutcome.AMBIGUOUS:
        return Placement.AMBIGUOUS
```

New text:

```
    if alive.outcome is trees.MatchOutcome.AMBIGUOUS:
        return Placement.NOT_IMPORTED
```

### `u51-item-derivation.A2_default_favorites_playlist`

Default the sweep to the FOLDER name the live library uses

- File: `src/cratekit/modules/outbound/source.py`
- Source: `u51-item-derivation.json`, row `A2_default_favorites_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 145 against a baseline of 145
- Kills: 27 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_failed_favourite_leaves_the_sweep_resumable`
  - `tests/test_outbound_workers.py::test_a_favourite_whose_isrc_names_several_tracks_is_listed_with_that_reason`
  - `tests/test_outbound_workers.py::test_a_favourites_sweep_runs_to_done_and_hearts_every_matched_row`
  - `tests/test_outbound_workers.py::test_a_fresh_export_shows_its_date_and_warns_of_nothing[sync.favorites]`
  - `tests/test_outbound_workers.py::test_a_month_old_export_is_called_old_in_the_plan_the_gate_shows[sync.favorites]`
  - `tests/test_outbound_workers.py::test_a_provider_that_already_hearts_a_row_is_reported_rather_than_written`
  - `tests/test_outbound_workers.py::test_a_second_sweep_writes_nothing_because_the_ledger_remembers`
  - `tests/test_outbound_workers.py::test_a_sweep_runs_with_rekordbox_open_and_never_opens_the_database`
  - `tests/test_outbound_workers.py::test_a_sweep_where_every_favourite_matches_answers_with_no_unmatched_line`
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`
  - `tests/test_outbound_workers.py::test_an_empty_playlist_refuses_distinguishably_from_an_absent_one`
  - `tests/test_outbound_workers.py::test_an_item_report_carries_no_empty_colored_list`
  - `tests/test_outbound_workers.py::test_an_unmatched_favourite_is_reported_and_does_not_fail_its_item`
  - `tests/test_outbound_workers.py::test_job_show_reports_the_bound_worker_for_a_queued_sweep`
  - `tests/test_outbound_workers.py::test_no_colour_writer_reaches_the_engine_from_a_queued_sweep`
  - ... and 12 more, see the JSON sidecar

Old text:

```
DEFAULT_FAVORITES_PLAYLIST = "All Favorites"
```

New text:

```
DEFAULT_FAVORITES_PLAYLIST = "Favorites"
```

### `u51-item-derivation.D1_unknown_playlist`

Drop the refusal for a playlist name the document does not carry

- File: `src/cratekit/modules/outbound/source.py`
- Source: `u51-item-derivation.json`, row `D1_unknown_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 145 against a baseline of 145
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_name_that_is_a_folder_refuses_rather_than_resolving`
  - `tests/test_outbound_workers.py::test_an_export_naming_a_playlist_the_document_lacks_queues_nothing`

Old text:

```
    if not matched:
        raise refuse(
            "export-playlist-unknown",
            f"no playlist in {library.path.name} is named {wanted!r}. A folder "
            f"of that name is not a match either, because a folder holds "
            f"playlists rather than tracks",
            steps=(
                "name the playlist by its display name, or by its full path "
                "joined with /",
            ),
            scope=Scope.RUN,
            origin=("outbound", "source"),
            detail={"playlist": wanted},
        )

```

New text:

```
(empty)
```

### `u51-item-derivation.D2_ambiguous_playlist`

Take the first match instead of refusing when several carry the name

- File: `src/cratekit/modules/outbound/source.py`
- Source: `u51-item-derivation.json`, row `D2_ambiguous_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 145 against a baseline of 145
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_name_two_playlists_carry_refuses_and_names_both_paths`

Old text:

```
    if len(matched) > 1:
```

New text:

```
    if False:
```

### `u51-item-derivation.D3_empty_playlist`

THE ZERO ITEM RULE: let a playlist with no writable track queue

- File: `src/cratekit/modules/outbound/source.py`
- Source: `u51-item-derivation.json`, row `D3_empty_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 145 against a baseline of 145
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_an_empty_playlist_refuses_distinguishably_from_an_absent_one`

Old text:

```
    if not kept:
```

New text:

```
    if False:
```

### `u51-item-derivation.D4_dangling_reported`

Stop reporting a TrackID the playlist names and the collection lacks

- File: `src/cratekit/modules/outbound/source.py`
- Source: `u51-item-derivation.json`, row `D4_dangling_reported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 145 against a baseline of 145
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_dangling_track_id_is_reported_and_not_queued`
  - `tests/test_outbound_workers.py::test_the_queued_envelope_names_a_missing_and_a_repeated_track`

Old text:

```
            dangling.append(track_id)
            continue
```

New text:

```
            continue
```

### `u51-item-derivation.D5_repeated_deduped`

Queue a repeated identifier twice instead of once

- File: `src/cratekit/modules/outbound/source.py`
- Source: `u51-item-derivation.json`, row `D5_repeated_deduped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 145 against a baseline of 145
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_repeated_track_id_becomes_one_item`
  - `tests/test_outbound_workers.py::test_the_queued_envelope_names_a_missing_and_a_repeated_track`

Old text:

```
        if track_id in seen:
```

New text:

```
        if False:
```

### `u51-item-derivation.D6_export_required`

Let a verb queue with no export document named

- File: `src/cratekit/modules/outbound/source.py`
- Source: `u51-item-derivation.json`, row `D6_export_required`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 145 against a baseline of 145
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_neither_verb_queues_anything_without_an_export[export.playlist]`
  - `tests/test_outbound_workers.py::test_neither_verb_queues_anything_without_an_export[sync.favorites]`

Old text:

```
    if not text:
```

New text:

```
    if False:
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

### `u149.T10_any_year_folder`

candidates: read every root folder, not only one titled as a year

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T10_any_year_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_only_downloaded_own_playlists_in_a_year_folder_are_read`

Old text:

```
        if not YEAR.fullmatch(year):
            continue
```

New text:

```
        if False:
            continue
```

### `u149.T11_excluded_read`

candidates: drop the label, set and mirror exclusion

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T11_excluded_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_set_playlist_in_a_year_folder_gets_no_twin`

Old text:

```
            if name is None or playlist_id in kept or playlist_id in seen:
```

New text:

```
            if name is None or playlist_id in seen:
```

### `u149.T13_paired_planned_again`

plan_backfill: plan a twin for an already paired playlist, so a second run plans again

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T13_paired_planned_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_an_existing_folder_is_reused_and_two_of_one_year_place_nothing`

Old text:

```
    wanted = [one for one in listed if one[1] not in held]
```

New text:

```
    wanted = list(listed)
```

### `u149.T15_unplanned_membership`

addition_violations: admit a membership no twin planned

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T15_unplanned_membership`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_the_confinement_refuses_what_no_twin_explains[changes4]`

Old text:

```
        if row[m_marker] or wanted is None or content_id not in wanted[2]:
```

New text:

```
        if row[m_marker] or wanted is None:
```

### `u149.T16_unplanned_playlist_row`

addition_violations: admit a playlist row no twin made

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T16_unplanned_playlist_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_the_confinement_refuses_an_unplanned_playlist_read_from_sql`
  - `tests/test_sync_twins.py::test_the_confinement_refuses_what_no_twin_explains[changes0]`

Old text:

```
    for key in sorted(set(after.playlists) - set(before.playlists) - set(made)):
```

New text:

```
    for key in sorted(set()):
```

