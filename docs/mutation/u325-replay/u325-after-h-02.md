# Mutation table: u325-after-h-02

Measured by `scripts/mutate.py` on 2026-11-22 23:36 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 64.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 16:29 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 6, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r1411.S3_order_does_not_pass_agreed` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 2 | killed |
| `u231.M4_resend_with_the_stale_tag` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 6 | killed |
| `u231.M5_positions_not_advanced` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 38 | killed |
| `u231.M6_settle_lag_taken` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 4 | killed |
| `r118-a.A10_forget_uses_the_record_sentence` | `src/cratekit/core/secrets.py` | user | 9 file(s) | 1649 | 1 | killed |
| `r118-a.A11_record_sentence_reworded` | `src/cratekit/core/secrets.py` | user | 9 file(s) | 1649 | 1 | killed |
| `r118-a.A12_env_override_no_longer_short_circuits` | `src/cratekit/core/secrets.py` | user | 9 file(s) | 1649 | 1 | killed |
| `r118-a.A1_blanket_returns_empty` | `src/cratekit/core/secrets.py` | user | 9 file(s) | 1649 | 11 | killed |
| `r118-a.A2_enoent_refuses_too` | `src/cratekit/core/secrets.py` | user | 9 file(s) | 1649 | 196 | killed |
| `r118-a.A3_unparseable_returns_empty` | `src/cratekit/core/secrets.py` | user | 9 file(s) | 1649 | 2 | killed |
| `r118-a.A4_wrong_shape_returns_empty` | `src/cratekit/core/secrets.py` | user | 9 file(s) | 1649 | 1 | killed |
| `r118-a.A5_refusal_drops_the_path` | `src/cratekit/core/secrets.py` | user | 9 file(s) | 1649 | 4 | killed |
| `r118-a.A6_refusal_not_raised_from` | `src/cratekit/core/secrets.py` | user | 9 file(s) | 1649 | 3 | killed |
| `r118-a.A8_damaged_reports_as_unreadable` | `src/cratekit/core/secrets.py` | maintainer | 9 file(s) | 1649 | 1 | killed |
| `r118-a.A9_record_uses_the_read_sentence` | `src/cratekit/core/secrets.py` | user | 9 file(s) | 1649 | 1 | killed |
| `r118-b.D1_index_written_before_the_read_back` | `src/cratekit/core/secrets.py` | user | 9 file(s) | 1649 | 1 | killed |
| `r118-b.D2_keychain_removed_before_the_index` | `src/cratekit/core/secrets.py` | user | 9 file(s) | 1649 | 6 | killed |
| `r118-c.A7_unreadable_remedy_is_set_credential` | `src/cratekit/core/secrets.py` | user | 9 file(s) | 1649 | 1 | killed |
| `u41-author-full.D1_dedupe_disabled` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1600 | 9 | killed |
| `u41-author-full.D2_dedupe_structural_rule_widened` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1600 | 8 | killed |
| `u41-naming-independent.D3_endswith_widened_to_containment` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1600 | 4 | killed |
| `u41-naming-independent.D6_repeat_widened_to_prefix` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1600 | 2 | killed |
| `u41-naming-independent.E1_budget_bypassed` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1600 | 4 | killed |
| `u41-naming-independent.E3_budget_min_becomes_max` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1600 | 8 | killed |
| `u41-naming-independent.E4_path_separator_byte_dropped` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1600 | 3 | killed |
| `u41-naming-independent.E5_truncation_tail_not_reserved` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1600 | 5 | killed |
| `u41-naming-independent.F3_body_tag_preference_flipped` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1600 | 29 | killed |
| `u41-naming-independent.F4_body_tag_fallback_dropped` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1600 | 52 | killed |
| `u41-naming-independent.F6_filename_prefers_the_title_body` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1600 | 49 | killed |
| `u41-naming-independent.F7_library_name_split_from_the_tag` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1600 | 1 | killed |
| `u39-author-full.D1_default_pad_reverted` | `src/cratekit/core/naming.py` | user | 9 file(s) | 1502 | 17 | killed |
| `u39-author-full.D2_pad_unguarded` | `src/cratekit/core/naming.py` | user | 9 file(s) | 1502 | 2 | killed |
| `u39-author-full.D3_pad_never_runs` | `src/cratekit/core/naming.py` | user | 9 file(s) | 1502 | 18 | killed |
| `u39-author-full.E1_budget_ordering_dropped` | `src/cratekit/core/naming.py` | maintainer | 9 file(s) | 1502 | 1 | killed |
| `u39-author-full.E2_wheel_bound_widened` | `src/cratekit/core/naming.py` | user | 9 file(s) | 1502 | 10 | killed |
| `u39-author-full.M1_refusal_reworded` | `src/cratekit/core/naming.py` | user | 9 file(s) | 1502 | 2 | killed |
| `u39-naming-independent.D2_pad_condition_inverted` | `src/cratekit/core/naming.py` | user | 9 file(s) | 1502 | 20 | killed |
| `u39-naming-independent.D3_pad_condition_unreachable` | `src/cratekit/core/naming.py` | user | 9 file(s) | 1502 | 18 | killed |
| `u39-naming-independent.D4_fake_pad_no_zero_fill` | `src/cratekit/core/naming.py` | user | 9 file(s) | 1502 | 18 | killed |
| `u39-naming-independent.E1_budget_ordering_inverted` | `src/cratekit/core/naming.py` | maintainer | 9 file(s) | 1502 | 2 | killed |
| `u39-naming-independent.E2_wheel_letter_widened` | `src/cratekit/core/naming.py` | user | 9 file(s) | 1502 | 1 | killed |
| `u39-naming-independent.M1_refusal_reworded` | `src/cratekit/core/naming.py` | user | 9 file(s) | 1502 | 2 | killed |
| `r290-author.J1_blocked_branch_removed` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 2678 | 49 | killed |
| `r290-author.J2_blocked_raises_the_plain_type` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 2678 | 48 | killed |
| `r290-author.J3_closed_branch_removed` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 2678 | 112 | killed |
| `r290-author.J4_predicate_narrowed_to_failed` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 2678 | 31 | killed |
| `r290-author.J5_causeless_block_returns` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 2678 | 1 | killed |
| `r290-author.J6_causeless_block_raises_the_plain_type` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 2678 | 1 | killed |
| `r290-author.J7_cancelled_raises_the_plain_type` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 2678 | 26 | killed |
| `r431-b.B1_a_wanted_built_by_hand_asks` | `src/cratekit/acquire/match.py` | user | 10 file(s) | 1298 | 2 | killed |
| `r431-b.B2_a_row_billing_a_guest_asks` | `src/cratekit/acquire/match.py` | user | 10 file(s) | 1298 | 2 | killed |
| `r431-b.B3_a_listing_that_spelled_a_credit_asks` | `src/cratekit/acquire/match.py` | user | 10 file(s) | 1298 | 7 | killed |
| `r431-b.B4_the_engine_never_asks` | `src/cratekit/acquire/match.py` | user | 10 file(s) | 1298 | 7 | killed |
| `r431-b.B5_the_engine_ignores_companions_false` | `src/cratekit/acquire/match.py` | user | 10 file(s) | 1298 | 1 | killed |
| `r431-b.B7_the_engine_asks_under_the_tombstones_kind` | `src/cratekit/acquire/match.py` | user | 10 file(s) | 1298 | 8 | killed |
| `r431-b.B8_the_reader_never_counts_the_artists` | `src/cratekit/acquire/match.py` | user | 10 file(s) | 1298 | 2 | killed |
| `r664.E1_stem_head_kept` | `src/cratekit/acquire/match.py` | user | 10 file(s) | 1298 | 149 | killed |

## Row definitions

### `r1411.S3_order_does_not_pass_agreed`

order_tracks takes agreed and never hands it to the judged reading

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `S3_order_does_not_pass_agreed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1311 against a baseline of 1311
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_agreed_order_after_an_add_refuses_with_nothing_moved`
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_agreed_order_once_is_read_again_and_takes_the_order`

Old text:

```
            agreed=tuple(str(one) for one in agreed) if agreed is not None else None,
```

New text:

```
            agreed=None,
```

### `u231.M4_resend_with_the_stale_tag`

adapter order: a 412's move is sent again without opening the playlist for its current tag

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u231.json`, row `M4_resend_with_the_stale_tag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1311 against a baseline of 1311
- Kills: 6 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_412_on_a_stale_tag_is_read_again_and_the_move_made_on_the_new_reading`
  - `tests/test_outbound_order.py::test_a_412_on_the_third_move_resends_that_move_once_and_no_other`
  - `tests/test_outbound_order.py::test_the_pauses_after_a_412_start_again_for_each_move`
  - `tests/test_outbound_order.py::test_the_reading_after_a_412_is_held_to_what_the_adds_left[False]`
  - `tests/test_outbound_order.py::test_the_reading_after_a_412_is_held_to_what_the_adds_left[True]`
  - `tests/test_outbound_window_lag.py::test_the_pause_after_a_412_is_counted_in_the_moves_record`

Old text:

```
                    playlist = self._playlist(identifier)
                    continue
```

New text:

```
                    continue
```

### `u231.M5_positions_not_advanced`

adapter order: each move's position is read off the reading as it was, not with the moves before it applied

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u231.json`, row `M5_positions_not_advanced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1311 against a baseline of 1311
- Kills: 38 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_412_on_a_stale_tag_is_read_again_and_the_move_made_on_the_new_reading`
  - `tests/test_outbound_order.py::test_a_412_on_the_third_move_resends_that_move_once_and_no_other`
  - `tests/test_outbound_order.py::test_a_move_that_lands_anywhere_else_is_not_read_back_and_the_settle_reading_shows_it`
  - `tests/test_outbound_order.py::test_a_provider_whose_move_to_the_length_lands_one_short_still_takes_the_order`
  - `tests/test_outbound_order.py::test_a_read_that_lags_every_move_does_not_stop_the_order`
  - `tests/test_outbound_order.py::test_a_reading_holding_what_the_adds_left_in_another_order_is_not_stale`
  - `tests/test_outbound_order.py::test_a_reading_that_agrees_with_the_expected_one_takes_the_order`
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_agreed_order_once_is_read_again_and_takes_the_order`
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_expected_one_is_read_again`
  - `tests/test_outbound_order.py::test_a_track_this_write_took_off_is_not_asked_of_the_reading`
  - `tests/test_outbound_order.py::test_an_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_outbound_order.py::test_every_move_is_planned_from_one_reading_and_sent_with_no_read_between`
  - `tests/test_outbound_order.py::test_the_caller_is_told_before_each_move_how_many_may_have_landed`
  - `tests/test_outbound_order.py::test_the_fake_account_orders_by_the_adapters_rule[before0-order0]`
  - `tests/test_outbound_order.py::test_the_fake_account_orders_by_the_adapters_rule[before1-order1]`
  - ... and 23 more, see the JSON sidecar

Old text:

```
            now = _fronted(now, one)
            note["moved"] += 1
```

New text:

```
            note["moved"] += 1
```

### `u231.M6_settle_lag_taken`

adapter settle: a reading whose window lags is answered as the order

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u231.json`, row `M6_settle_lag_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1311 against a baseline of 1311
- Kills: 4 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_the_settle_reading_waits_then_reads_once_and_names_a_lag`
  - `tests/test_outbound_window_lag.py::test_a_window_that_catches_up_beside_a_first_page_settles_as_done`
  - `tests/test_outbound_window_lag.py::test_a_window_that_lags_beside_a_first_page_is_not_read_back_between_moves`
  - `tests/test_outbound_window_lag.py::test_every_judged_reading_records_its_readings_and_wait`

Old text:

```
        if window == listing.WINDOW_LAGS:
            note["window_lagged"] += 1
            note["outcome"] = "lags"
            return None
```

New text:

```
        if False:
            return None
```

### `r118-a.A10_forget_uses_the_record_sentence`

A refusal from the remove half says the value is in the keychain because of this call, which is a claim about a write that never happened

- File: `src/cratekit/core/secrets.py`
- Source: `r118-a.json`, row `A10_forget_uses_the_record_sentence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/test_adapter_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 1649 against a baseline of 1649
- Kills: 1 (killed)
- Killed:
  - `tests/test_config.py::test_a_refusal_from_the_remove_half_says_neither_store_was_touched`

Old text:

```
    names = _index_read(REMOVE_NOTHING_TOUCHED)
```

New text:

```
    names = _index_read(RECORD_ALREADY_IN_THE_KEYCHAIN)
```

### `r118-a.A11_record_sentence_reworded`

The record sentence no longer says the value reached the keychain, only that the index could not be updated

- File: `src/cratekit/core/secrets.py`
- Source: `r118-a.json`, row `A11_record_sentence_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/test_adapter_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 1649 against a baseline of 1649
- Kills: 1 (killed)
- Killed:
  - `tests/test_config.py::test_a_refusal_from_the_record_half_says_the_value_reached_the_keychain`

Old text:

```
    "THE VALUE IS IN THE KEYCHAIN. It was stored and read back before this index "
```

New text:

```
    "The index could not be updated. It was opened after the keychain write "
```

### `r118-a.A12_env_override_no_longer_short_circuits`

exists consults the index even when the opted-in environment fallback is supplying the value, so a machine that has no index by design is refused

- File: `src/cratekit/core/secrets.py`
- Source: `r118-a.json`, row `A12_env_override_no_longer_short_circuits`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/test_adapter_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 1649 against a baseline of 1649
- Kills: 1 (killed)
- Killed:
  - `tests/test_config.py::test_the_environment_fallback_answers_presence_without_reading_the_index`

Old text:

```
    if _env_override(str(name)):
        return True
    return str(name) in _index_read()
```

New text:

```
    return str(name) in _index_read()
```

### `r118-a.A1_blanket_returns_empty`

The whole three-state reader reverts to the old blanket, so OSError and ValueError alike answer nothing recorded

- File: `src/cratekit/core/secrets.py`
- Source: `r118-a.json`, row `A1_blanket_returns_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/test_adapter_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 1649 against a baseline of 1649
- Kills: 11 (killed)
- Killed:
  - `tests/test_config.py::test_a_damaged_presence_index_refuses_and_says_it_was_read`
  - `tests/test_config.py::test_a_presence_index_that_could_not_be_read_is_not_answered_as_not_recorded`
  - `tests/test_config.py::test_a_presence_index_without_a_list_of_names_refuses_rather_than_answering`
  - `tests/test_config.py::test_a_refusal_from_the_record_half_says_the_value_reached_the_keychain`
  - `tests/test_config.py::test_a_refusal_from_the_remove_half_says_neither_store_was_touched`
  - `tests/test_config.py::test_an_index_refused_for_something_other_than_a_permission_keeps_its_own_act`
  - `tests/test_config.py::test_recording_a_credential_does_not_truncate_an_index_it_could_not_read`
  - `tests/test_config.py::test_removing_a_credential_does_not_truncate_an_index_it_could_not_read`
  - `tests/test_doctor.py::test_an_unreadable_credential_index_is_reported_as_unread_not_as_unrecorded`
  - `tests/test_doctor.py::test_the_wizard_notes_an_index_that_refuses_the_write_rather_than_dying`
  - `tests/test_doctor.py::test_the_wizard_notes_an_unreadable_credential_index_rather_than_dying`

Old text:

```
    path = _index_path()
    try:
        raw = path.read_text()
    except FileNotFoundError:
        return frozenset()
    except OSError as exc:
        raise refuse(
            "credential-index-unreadable",
            f"the credential presence index at {path} is present and could not "
            f"be read ({type(exc).__name__}), so this installation cannot say "
            f"which credentials it has recorded. {left}",
            remedy=ProductRemedy.REPAIR_CREDENTIAL_STORE,
            origin=("core", "secrets"),
            detail={"path": str(path), "index": "unreadable"},
        ) from exc
    try:
        payload = json.loads(raw)
    except ValueError as exc:
        raise _damaged(
            path, f"is not readable as JSON ({type(exc).__name__})", left
        ) from exc
    names = payload.get("recorded") if isinstance(payload, dict) else None
    if not isinstance(names, Iterable) or isinstance(names, str):
        raise _damaged(path, "does not carry a list of recorded credential names", left)
    return frozenset(str(n) for n in names)
```

New text:

```
    del left
    path = _index_path()
    try:
        payload = json.loads(path.read_text())
    except (OSError, ValueError):
        return frozenset()
    names = payload.get("recorded") if isinstance(payload, dict) else None
    if not isinstance(names, Iterable) or isinstance(names, str):
        return frozenset()
    return frozenset(str(n) for n in names)
```

### `r118-a.A2_enoent_refuses_too`

A fresh installation with no index refuses instead of answering nothing recorded, so the product cannot be set up

- File: `src/cratekit/core/secrets.py`
- Source: `r118-a.json`, row `A2_enoent_refuses_too`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/test_adapter_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 1649 against a baseline of 1649
- Kills: 196 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_credential_missing_after_the_gate_is_credential_missing_with_its_own_remedy`
  - `tests/intake/test_recognition.py::test_the_bound_identifier_hands_the_cache_through`
  - `tests/intake/test_recognition.py::test_the_bound_identifier_resolves_its_seams_at_call_time`
  - `tests/intake/test_recognition.py::test_the_gate_names_both_binaries_and_both_keys`
  - `tests/intake/test_recognition.py::test_the_gate_still_refuses_with_no_credentials_before_the_seam_is_touched`
  - `tests/intake/test_recognition.py::test_the_keychain_credentials_are_read_by_name_after_the_gate`
  - `tests/intake/test_recognition.py::test_the_paid_path_will_not_run_without_the_recognition_section`
  - `tests/intake/test_recognition.py::test_the_seam_binds_this_identifier_when_none_is_injected`
  - `tests/intake/test_workers.py::test_a_changed_recording_misses_the_cache_and_is_paid_for`
  - `tests/intake/test_workers.py::test_a_failure_mid_set_fails_that_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/intake/test_workers.py::test_a_gap_is_paid_for_again_and_nothing_else_is`
  - `tests/intake/test_workers.py::test_a_missing_recording_is_refused_by_name`
  - `tests/intake/test_workers.py::test_a_month_within_the_configured_bound_is_paid_for`
  - `tests/intake/test_workers.py::test_a_queued_set_freezes_the_recognition_section_it_was_identified_under`
  - `tests/intake/test_workers.py::test_a_recording_over_the_parts_ceiling_is_refused_at_the_queue_and_queues_nothing`
  - ... and 181 more, see the JSON sidecar

Old text:

```
    except FileNotFoundError:
        return frozenset()
    except OSError as exc:
```

New text:

```
    except OSError as exc:
```

### `r118-a.A3_unparseable_returns_empty`

Bytes that are not JSON answer nothing recorded again, the ValueError half of the old blanket

- File: `src/cratekit/core/secrets.py`
- Source: `r118-a.json`, row `A3_unparseable_returns_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/test_adapter_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 1649 against a baseline of 1649
- Kills: 2 (killed)
- Killed:
  - `tests/test_config.py::test_a_damaged_presence_index_refuses_and_says_it_was_read`
  - `tests/test_doctor.py::test_the_wizard_notes_an_index_that_refuses_the_write_rather_than_dying`

Old text:

```
    except ValueError as exc:
        raise _damaged(
            path, f"is not readable as JSON ({type(exc).__name__})", left
        ) from exc
```

New text:

```
    except ValueError:
        return frozenset()
```

### `r118-a.A4_wrong_shape_returns_empty`

A payload whose recorded key is not a list of names answers nothing recorded

- File: `src/cratekit/core/secrets.py`
- Source: `r118-a.json`, row `A4_wrong_shape_returns_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/test_adapter_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 1649 against a baseline of 1649
- Kills: 1 (killed)
- Killed:
  - `tests/test_config.py::test_a_presence_index_without_a_list_of_names_refuses_rather_than_answering`

Old text:

```
    if not isinstance(names, Iterable) or isinstance(names, str):
        raise _damaged(path, "does not carry a list of recorded credential names", left)
```

New text:

```
    if not isinstance(names, Iterable) or isinstance(names, str):
        return frozenset()
```

### `r118-a.A5_refusal_drops_the_path`

The unreadable refusal names the exception type and not the file it could not read

- File: `src/cratekit/core/secrets.py`
- Source: `r118-a.json`, row `A5_refusal_drops_the_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/test_adapter_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 1649 against a baseline of 1649
- Kills: 4 (killed)
- Killed:
  - `tests/test_config.py::test_a_presence_index_that_could_not_be_read_is_not_answered_as_not_recorded`
  - `tests/test_config.py::test_an_index_refused_for_something_other_than_a_permission_keeps_its_own_act`
  - `tests/test_doctor.py::test_an_unreadable_credential_index_is_reported_as_unread_not_as_unrecorded`
  - `tests/test_doctor.py::test_the_wizard_notes_an_unreadable_credential_index_rather_than_dying`

Old text:

```
            f"the credential presence index at {path} is present and could not "
            f"be read ({type(exc).__name__}), so this installation cannot say "
```

New text:

```
            f"the credential presence index is present and could not "
            f"be read ({type(exc).__name__}), so this installation cannot say "
```

### `r118-a.A6_refusal_not_raised_from`

The unreadable refusal is raised without from, so cause.classified cannot see the kernel's own refusal and a permission stays repair-credential-store

- File: `src/cratekit/core/secrets.py`
- Source: `r118-a.json`, row `A6_refusal_not_raised_from`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/test_adapter_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 1649 against a baseline of 1649
- Kills: 3 (killed)
- Killed:
  - `tests/test_config.py::test_a_presence_index_that_could_not_be_read_is_not_answered_as_not_recorded`
  - `tests/test_doctor.py::test_an_unreadable_credential_index_is_reported_as_unread_not_as_unrecorded`
  - `tests/test_doctor.py::test_the_wizard_notes_an_unreadable_credential_index_rather_than_dying`

Old text:

```
            detail={"path": str(path), "index": "unreadable"},
        ) from exc
```

New text:

```
            detail={"path": str(path), "index": "unreadable"},
        )
```

### `r118-a.A8_damaged_reports_as_unreadable`

Both states report index unreadable in detail, so a machine consumer cannot tell a file it could not open from one it read and could not use

- File: `src/cratekit/core/secrets.py`
- Source: `r118-a.json`, row `A8_damaged_reports_as_unreadable`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/test_adapter_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 1649 against a baseline of 1649
- Kills: 1 (killed)
- Killed:
  - `tests/test_config.py::test_a_damaged_presence_index_refuses_and_says_it_was_read`

Old text:

```
        detail={"path": str(path), "index": "damaged"},
```

New text:

```
        detail={"path": str(path), "index": "unreadable"},
```

### `r118-a.A9_record_uses_the_read_sentence`

A refusal from the record half says nothing was stored, over a value the keychain already holds

- File: `src/cratekit/core/secrets.py`
- Source: `r118-a.json`, row `A9_record_uses_the_read_sentence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/test_adapter_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 1649 against a baseline of 1649
- Kills: 1 (killed)
- Killed:
  - `tests/test_config.py::test_a_refusal_from_the_record_half_says_the_value_reached_the_keychain`

Old text:

```
    names = _index_read(RECORD_ALREADY_IN_THE_KEYCHAIN)
```

New text:

```
    names = _index_read()
```

### `r118-b.D1_index_written_before_the_read_back`

set notes the name in the index before the keychain write is read back, so a null backend records a credential it discarded

- File: `src/cratekit/core/secrets.py`
- Source: `r118-b.json`, row `D1_index_written_before_the_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/test_adapter_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 1649 against a baseline of 1649
- Kills: 1 (killed)
- Killed:
  - `tests/test_config.py::test_a_backend_that_accepts_a_write_and_stores_nothing_refuses`

Old text:

```
        if stored != value:
            raise _unavailable(
```

New text:

```
        _record_name(str(name))
        if stored != value:
            raise _unavailable(
```

### `r118-b.D2_keychain_removed_before_the_index`

delete removes the keychain entry before the index entry, the order that made exists answer True for a credential that was gone

- File: `src/cratekit/core/secrets.py`
- Source: `r118-b.json`, row `D2_keychain_removed_before_the_index`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/test_adapter_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 1649 against a baseline of 1649
- Kills: 6 (killed)
- Killed:
  - `tests/test_config.py::test_a_refusal_from_the_remove_half_says_neither_store_was_touched`
  - `tests/test_config.py::test_deleting_a_credential_clears_it_from_the_presence_index`
  - `tests/test_config.py::test_removing_a_credential_does_not_truncate_an_index_it_could_not_read`
  - `tests/test_config.py::test_the_presence_index_cycle_is_held_under_an_exclusive_lock`
  - `tests/test_doctor.py::test_a_delete_that_fails_between_the_two_stores_never_reports_green`
  - `tests/test_doctor.py::test_recording_and_removing_still_work_when_the_lock_is_available`

Old text:

```
        _forget_name(str(name))
        try:
            keyring.delete_password(SERVICE, str(name))
```

New text:

```
        try:
            keyring.delete_password(SERVICE, str(name))
```

### `r118-c.A7_unreadable_remedy_is_set_credential`

The unreadable refusal carries set-credential, which is the advice the finding exists to stop

- File: `src/cratekit/core/secrets.py`
- Source: `r118-c.json`, row `A7_unreadable_remedy_is_set_credential`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/test_adapter_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 1649 against a baseline of 1649
- Kills: 1 (killed)
- Killed:
  - `tests/test_config.py::test_an_index_refused_for_something_other_than_a_permission_keeps_its_own_act`

Old text:

```
            remedy=ProductRemedy.REPAIR_CREDENTIAL_STORE,
            origin=("core", "secrets"),
            detail={"path": str(path), "index": "unreadable"},
```

New text:

```
            remedy=ProductRemedy.SET_CREDENTIAL,
            origin=("core", "secrets"),
            detail={"path": str(path), "index": "unreadable"},
```

### `u41-author-full.D1_dedupe_disabled`

dedupe_stem stops dropping a trailing segment that repeats the lead; an existing guard this unit switched on for real input

- File: `src/cratekit/core/naming.py`
- Source: `u41-author-full.json`, row `D1_dedupe_disabled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1600 against a baseline of 1600
- Kills: 9 (killed)
- Killed:
  - `tests/test_naming.py::TestBudgetInteraction::test_dedupe_runs_before_the_fit_and_the_hash_uses_the_original`
  - `tests/test_naming_apply_cli.py::test_a_collision_answers_with_the_files_that_stayed_put`
  - `tests/test_naming_apply_cli.py::test_a_deduping_rename_converges_on_one_pass`
  - `tests/test_naming_apply_cli.py::test_a_target_a_collider_holds_is_held_back_too`
  - `tests/test_naming_apply_cli.py::test_a_target_another_mover_still_holds_is_promised_and_then_reported`
  - `tests/test_naming_apply_cli.py::test_a_trailing_segment_repeating_the_lead_is_still_deduped`
  - `tests/test_naming_apply_cli.py::test_the_remediation_only_names_a_hand_rename_over_a_real_collision`
  - `tests/test_naming_apply_cli.py::test_two_files_rendering_to_one_name_are_not_promised_two_renames`
  - `tests/test_naming_apply_cli.py::test_two_targets_differing_only_in_case_are_one_name`

Old text:

```
    deduped = dedupe_stem(spec.stem, spec.title, spec.album, sep=template.segment_sep)

```

New text:

```
    deduped = spec.stem

```

### `u41-author-full.D2_dedupe_structural_rule_widened`

The structural dedupe rule drops its exact trailing match, so an unrelated trailing segment is mutilated

- File: `src/cratekit/core/naming.py`
- Source: `u41-author-full.json`, row `D2_dedupe_structural_rule_widened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1600 against a baseline of 1600
- Kills: 8 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_name_with_no_parseable_head_is_left_as_it_arrives`
  - `tests/test_naming_apply_cli.py::test_a_rename_never_replaces_the_body_with_the_title_tag`
  - `tests/test_naming_apply_cli.py::test_a_trailing_segment_that_only_starts_with_the_lead_survives`
  - `tests/test_naming_apply_cli.py::test_both_library_grammars_survive_a_rename`
  - `tests/test_naming_budget.py::TestDedupeStem::test_identity_on_near_match_album`
  - `tests/test_naming_budget.py::TestDedupeStem::test_identity_when_segments_differ`
  - `tests/test_naming_budget.py::TestDedupeStem::test_title_containing_the_separator_is_ambiguous_structurally`
  - `tests/test_naming_budget.py::TestDedupeStem::test_title_containing_the_separator_is_deduped_via_tags`

Old text:

```
        if lead and stem.endswith(sep + lead):

```

New text:

```
        if lead:

```

### `u41-naming-independent.D3_endswith_widened_to_containment`

The repeat test becomes containment rather than a trailing match, so a lead appearing mid name triggers a cut

- File: `src/cratekit/core/naming.py`
- Source: `u41-naming-independent.json`, row `D3_endswith_widened_to_containment`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1600 against a baseline of 1600
- Kills: 4 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_trailing_segment_that_only_starts_with_the_lead_survives`
  - `tests/test_naming_budget.py::TestDedupeStem::test_identity_on_near_match_album`
  - `tests/test_naming_budget.py::TestDedupeStem::test_title_containing_the_separator_is_ambiguous_structurally`
  - `tests/test_naming_budget.py::TestDedupeStem::test_title_containing_the_separator_is_deduped_via_tags`

Old text:

```
        if lead and stem.endswith(sep + lead):

```

New text:

```
        if lead and (sep + lead) in stem:

```

### `u41-naming-independent.D6_repeat_widened_to_prefix`

AMBIGUITY MEANS IDENTITY is inverted: a trailing segment that merely BEGINS with the lead counts as a repeat

- File: `src/cratekit/core/naming.py`
- Source: `u41-naming-independent.json`, row `D6_repeat_widened_to_prefix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1600 against a baseline of 1600
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_trailing_segment_that_only_starts_with_the_lead_survives`
  - `tests/test_naming_budget.py::TestDedupeStem::test_identity_on_near_match_album`

Old text:

```
        if lead and stem.endswith(sep + lead):

```

New text:

```
        if lead and parts[-1].startswith(lead):

```

### `u41-naming-independent.E1_budget_bypassed`

The fitted stem is discarded and the deduped one is returned, so nothing is ever shortened to the path ceiling

- File: `src/cratekit/core/naming.py`
- Source: `u41-naming-independent.json`, row `E1_budget_bypassed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1600 against a baseline of 1600
- Kills: 4 (killed)
- Killed:
  - `tests/test_naming.py::TestBudgetInteraction::test_an_absent_field_contributes_zero_bytes_including_its_separator`
  - `tests/test_naming.py::TestBudgetInteraction::test_build_fits_and_its_result_is_already_in_the_padded_form`
  - `tests/test_naming_apply_cli.py::test_a_composed_body_over_the_ceiling_is_fitted_not_left_as_a_number`
  - `tests/test_naming_apply_cli.py::test_a_name_over_the_byte_ceiling_is_truncated_not_rebuilt`

Old text:

```
    return replace(spec, stem=fitted)

```

New text:

```
    return replace(spec, stem=deduped)

```

### `u41-naming-independent.E3_budget_min_becomes_max`

The two ceilings are combined with max rather than min, so the looser one wins

- File: `src/cratekit/core/naming.py`
- Source: `u41-naming-independent.json`, row `E3_budget_min_becomes_max`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1600 against a baseline of 1600
- Kills: 8 (killed)
- Killed:
  - `tests/test_naming.py::TestBudgetInteraction::test_build_fits_and_its_result_is_already_in_the_padded_form`
  - `tests/test_naming_apply_cli.py::test_a_name_over_the_byte_ceiling_is_truncated_not_rebuilt`
  - `tests/test_naming_budget.py::TestFitStemToBudget::test_a_character_count_would_have_passed_this_and_the_byte_count_does_not`
  - `tests/test_naming_budget.py::TestFitStemToBudget::test_an_unsatisfiable_budget_raises_rather_than_emitting`
  - `tests/test_naming_budget.py::TestFitStemToBudget::test_multibyte_never_splits_a_codepoint`
  - `tests/test_naming_budget.py::TestFitStemToBudget::test_over_budget_truncates_and_the_assembled_path_fits`
  - `tests/test_naming_budget.py::TestFitStemToBudget::test_padding_a_single_digit_key_cannot_push_a_fitted_name_over`
  - `tests/test_naming_budget.py::TestFitStemToBudget::test_two_budgets_in_one_process_give_two_answers`

Old text:

```
    max_stem = min(

```

New text:

```
    max_stem = max(

```

### `u41-naming-independent.E4_path_separator_byte_dropped`

The path separator's byte is no longer counted against the path budget

- File: `src/cratekit/core/naming.py`
- Source: `u41-naming-independent.json`, row `E4_path_separator_byte_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1600 against a baseline of 1600
- Kills: 3 (killed)
- Killed:
  - `tests/test_naming.py::TestBudgetInteraction::test_build_fits_and_its_result_is_already_in_the_padded_form`
  - `tests/test_naming_budget.py::TestFitStemToBudget::test_over_budget_truncates_and_the_assembled_path_fits`
  - `tests/test_naming_budget.py::TestFitStemToBudget::test_padding_a_single_digit_key_cannot_push_a_fitted_name_over`

Old text:

```
        + 1  # the path separator

```

New text:

```
        + 0  # the path separator

```

### `u41-naming-independent.E5_truncation_tail_not_reserved`

The disambiguating tail's bytes are not reserved, so the assembled name overshoots the ceiling by its length

- File: `src/cratekit/core/naming.py`
- Source: `u41-naming-independent.json`, row `E5_truncation_tail_not_reserved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1600 against a baseline of 1600
- Kills: 5 (killed)
- Killed:
  - `tests/test_naming.py::TestBudgetInteraction::test_build_fits_and_its_result_is_already_in_the_padded_form`
  - `tests/test_naming_budget.py::TestFitStemToBudget::test_a_character_count_would_have_passed_this_and_the_byte_count_does_not`
  - `tests/test_naming_budget.py::TestFitStemToBudget::test_multibyte_never_splits_a_codepoint`
  - `tests/test_naming_budget.py::TestFitStemToBudget::test_over_budget_truncates_and_the_assembled_path_fits`
  - `tests/test_naming_budget.py::TestFitStemToBudget::test_padding_a_single_digit_key_cannot_push_a_fitted_name_over`

Old text:

```
    avail = max_stem - len(tail)

```

New text:

```
    avail = max_stem

```

### `u41-naming-independent.F3_body_tag_preference_flipped`

The tag body prefers the filename's stem over the title, which is A2 reproduced inside the engine

- File: `src/cratekit/core/naming.py`
- Source: `u41-naming-independent.json`, row `F3_body_tag_preference_flipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1600 against a baseline of 1600
- Kills: 29 (killed)
- Killed:
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_marker_in_the_body_marks_nothing`
  - `tests/test_naming.py::TestRender::test_lossless_carries_no_marker`
  - `tests/test_naming.py::TestRender::test_lossy_marks_right_after_the_head`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-124-Title Tag-False-custom]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-124-Title Tag-False-default]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-124-Title Tag-False-optional-bpm]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-124-Title Tag-True-custom]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-124-Title Tag-True-default]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-124-Title Tag-True-optional-bpm]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-None-Title Tag-False-custom]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-None-Title Tag-False-default]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-None-Title Tag-False-optional-bpm]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-None-Title Tag-True-custom]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-None-Title Tag-True-default]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-None-Title Tag-True-optional-bpm]`
  - ... and 14 more, see the JSON sidecar

Old text:

```
    body_tag = spec.title if spec.title else spec.stem

```

New text:

```
    body_tag = spec.stem if spec.stem else spec.title

```

### `u41-naming-independent.F4_body_tag_fallback_dropped`

The tag body has no fallback at all, so a spec with no title renders None into the tag

- File: `src/cratekit/core/naming.py`
- Source: `u41-naming-independent.json`, row `F4_body_tag_fallback_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1600 against a baseline of 1600
- Kills: 52 (killed)
- Killed:
  - `tests/test_naming.py::TestAnalysisOff::test_a_lossy_file_is_still_marked_with_analysis_off`
  - `tests/test_naming.py::TestAnalysisOff::test_a_tempo_without_a_key_renders_no_head_at_all`
  - `tests/test_naming.py::TestAnalysisOff::test_absent_fields_are_omitted_not_rendered_empty`
  - `tests/test_naming.py::TestAnalysisOff::test_it_round_trips_through_the_parser`
  - `tests/test_naming.py::TestAnalysisOff::test_no_key_and_no_tempo_renders_the_body_alone`
  - `tests/test_naming.py::TestBudgetInteraction::test_build_fits_and_its_result_is_already_in_the_padded_form`
  - `tests/test_naming.py::TestBudgetInteraction::test_the_budget_head_equals_the_written_head_since_the_pad_moved_in`
  - `tests/test_naming.py::TestBudgetInteraction::test_the_same_input_twice_yields_the_same_path`
  - `tests/test_naming.py::TestMarkerCoupling::test_a_lossless_file_renders_fine_under_the_same_template`
  - `tests/test_naming.py::TestMarkerCoupling::test_all_three_surfaces_or_none[None-8A-124-False]`
  - `tests/test_naming.py::TestMarkerCoupling::test_all_three_surfaces_or_none[None-8A-124-True]`
  - `tests/test_naming.py::TestMarkerCoupling::test_all_three_surfaces_or_none[None-8A-None-False]`
  - `tests/test_naming.py::TestMarkerCoupling::test_all_three_surfaces_or_none[None-8A-None-True]`
  - `tests/test_naming.py::TestMarkerCoupling::test_all_three_surfaces_or_none[None-None-None-False]`
  - `tests/test_naming.py::TestMarkerCoupling::test_all_three_surfaces_or_none[None-None-None-True]`
  - ... and 37 more, see the JSON sidecar

Old text:

```
    body_tag = spec.title if spec.title else spec.stem

```

New text:

```
    body_tag = spec.title

```

### `u41-naming-independent.F6_filename_prefers_the_title_body`

R-168 reproduced one file over: the FILENAME is rendered from the title body when there is one, inside the engine rather than in the shell

- File: `src/cratekit/core/naming.py`
- Source: `u41-naming-independent.json`, row `F6_filename_prefers_the_title_body`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1600 against a baseline of 1600
- Kills: 49 (killed)
- Killed:
  - `tests/test_naming.py::TestRender::test_lossless_carries_no_marker`
  - `tests/test_naming.py::TestRender::test_lossy_marks_right_after_the_head`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-124-Title Tag-False-custom]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-124-Title Tag-False-default]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-124-Title Tag-False-optional-bpm]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-124-Title Tag-True-custom]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-124-Title Tag-True-default]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-124-Title Tag-True-optional-bpm]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-None-Title Tag-False-custom]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-None-Title Tag-False-default]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-None-Title Tag-False-optional-bpm]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-None-Title Tag-True-custom]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-None-Title Tag-True-default]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-None-Title Tag-True-optional-bpm]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[None-124-Title Tag-False-custom]`
  - ... and 34 more, see the JSON sidecar

Old text:

```
        filename=head + spec.stem + spec.suffix,

```

New text:

```
        filename=head + (spec.title or spec.stem) + spec.suffix,

```

### `u41-naming-independent.F7_library_name_split_from_the_tag`

The library name is derived from the stem rather than from the rendered title tag, so the marker can go missing from one surface only

- File: `src/cratekit/core/naming.py`
- Source: `u41-naming-independent.json`, row `F7_library_name_split_from_the_tag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1600 against a baseline of 1600
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming.py::TestRender::test_lossless_carries_no_marker`

Old text:

```
        library_name=title_tag,

```

New text:

```
        library_name=head + spec.stem,

```

### `u39-author-full.D1_default_pad_reverted`

Revert the key_pad default to none, the pre U39 written form

- File: `src/cratekit/core/naming.py`
- Source: `u39-author-full.json`, row `D1_default_pad_reverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1502 against a baseline of 1502
- Kills: 17 (killed)
- Killed:
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_disagreeing_title_head_leaves_the_stem_head_to_agree`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_key_only_spec_over_a_headed_title_keeps_the_whole_head`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_spec_with_no_fields_takes_both_from_the_head`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_value_the_spec_supplies_wins_over_the_head`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_an_unpadded_or_lowercase_key_agrees_with_its_padded_head`
  - `tests/test_naming.py::TestBudgetInteraction::test_build_fits_and_its_result_is_already_in_the_padded_form`
  - `tests/test_naming.py::TestBudgetInteraction::test_the_budget_head_equals_the_written_head_since_the_pad_moved_in`
  - `tests/test_naming.py::TestRender::test_an_already_fitted_stem_passes_through_verbatim`
  - `tests/test_naming.py::TestRender::test_lossless_carries_no_marker`
  - `tests/test_naming.py::TestRender::test_lossy_marks_right_after_the_head`
  - `tests/test_naming.py::TestRender::test_the_key_is_written_and_measured_in_the_same_padded_form`
  - `tests/test_naming.py::TestRender::test_the_stem_is_the_fallback_when_there_is_no_title_tag`
  - `tests/test_naming.py::TestWriteTimePadding::test_a_code_read_as_data_is_normalized_by_the_padding_stage`
  - `tests/test_naming.py::TestWriteTimePadding::test_rendering_the_padded_output_again_changes_nothing`
  - `tests/test_naming.py::TestWriteTimePadding::test_the_default_template_writes_the_padded_form`
  - ... and 2 more, see the JSON sidecar

Old text:

```
    key_pad: str = "camelot2"

```

New text:

```
    key_pad: str = "none"

```

### `u39-author-full.D2_pad_unguarded`

Pad unconditionally, so an off wheel key raises from pad_camelot instead of the one refusal path

- File: `src/cratekit/core/naming.py`
- Source: `u39-author-full.json`, row `D2_pad_unguarded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1502 against a baseline of 1502
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming.py::TestRender::test_an_unwritable_key_is_refused_rather_than_emitted`
  - `tests/test_naming.py::TestWriteTimePadding::test_an_off_wheel_key_is_still_refused_not_padded`

Old text:

```
        if key_pad == "camelot2" and parse_camelot(rendered) is not None:

```

New text:

```
        if key_pad == "camelot2":

```

### `u39-author-full.D3_pad_never_runs`

Padding stage disabled entirely, even for explicit camelot2 templates

- File: `src/cratekit/core/naming.py`
- Source: `u39-author-full.json`, row `D3_pad_never_runs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1502 against a baseline of 1502
- Kills: 18 (killed)
- Killed:
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_disagreeing_title_head_leaves_the_stem_head_to_agree`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_key_only_spec_over_a_headed_title_keeps_the_whole_head`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_spec_with_no_fields_takes_both_from_the_head`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_value_the_spec_supplies_wins_over_the_head`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_an_unpadded_or_lowercase_key_agrees_with_its_padded_head`
  - `tests/test_naming.py::TestBudgetInteraction::test_build_fits_and_its_result_is_already_in_the_padded_form`
  - `tests/test_naming.py::TestBudgetInteraction::test_the_marker_is_paid_for_in_the_budget_head`
  - `tests/test_naming.py::TestMarkerCoupling::test_the_marker_text_is_a_parameter`
  - `tests/test_naming.py::TestRender::test_an_already_fitted_stem_passes_through_verbatim`
  - `tests/test_naming.py::TestRender::test_lossless_carries_no_marker`
  - `tests/test_naming.py::TestRender::test_lossy_marks_right_after_the_head`
  - `tests/test_naming.py::TestRender::test_the_key_is_written_and_measured_in_the_same_padded_form`
  - `tests/test_naming.py::TestRender::test_the_stem_is_the_fallback_when_there_is_no_title_tag`
  - `tests/test_naming.py::TestWriteTimePadding::test_a_code_read_as_data_is_normalized_by_the_padding_stage`
  - `tests/test_naming.py::TestWriteTimePadding::test_rendering_the_padded_output_again_changes_nothing`
  - ... and 3 more, see the JSON sidecar

Old text:

```
        if key_pad == "camelot2" and parse_camelot(rendered) is not None:

```

New text:

```
        if False:

```

### `u39-author-full.E1_budget_ordering_dropped`

Existing guard sample: the budget narrower than written refusal is disabled

- File: `src/cratekit/core/naming.py`
- Source: `u39-author-full.json`, row `E1_budget_ordering_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1502 against a baseline of 1502
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming.py::TestTemplateValidation::test_measuring_narrower_than_writing_is_refused`

Old text:

```
        if KEY_PADS.index(self.budget_key_pad) < KEY_PADS.index(self.key_pad):

```

New text:

```
        if False:

```

### `u39-author-full.E2_wheel_bound_widened`

Existing guard sample: the Camelot number bound admits 13 through 19

- File: `src/cratekit/core/naming.py`
- Source: `u39-author-full.json`, row `E2_wheel_bound_widened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1502 against a baseline of 1502
- Kills: 10 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_an_off_wheel_key_is_rejected_rather_than_normalized[13A]`
  - `tests/test_naming.py::TestRender::test_an_unwritable_key_is_refused_rather_than_emitted`
  - `tests/test_naming.py::TestSplitAndPadHead::test_split_refuses_a_head_the_engine_could_not_have_written`
  - `tests/test_naming.py::TestTheDeletedDuplicate::test_it_accepted_keys_that_are_not_on_the_wheel[13A - 124 - Off Wheel]`
  - `tests/test_naming.py::TestTrailingHead::test_the_trailing_form_holds_the_same_bound_as_the_leading_form[Cola - 13A - 124]`
  - `tests/test_naming.py::TestWriteTimePadding::test_an_off_wheel_key_is_still_refused_not_padded`
  - `tests/test_naming.py::test_is_camelot_agrees_with_parse_camelot`
  - `tests/test_naming.py::test_pad_camelot_normalizes_and_refuses`
  - `tests/test_naming.py::test_parse_and_strip_head[13 is off the wheel]`
  - `tests/test_naming.py::test_parse_camelot[13A]`

Old text:

```
_CAMELOT_NUMBER = r"(?:[1-9]|1[0-2])"

```

New text:

```
_CAMELOT_NUMBER = r"(?:[1-9]|1[0-9])"

```

### `u39-author-full.M1_refusal_reworded`

Reword the unwritable key refusal, do not append to it

- File: `src/cratekit/core/naming.py`
- Source: `u39-author-full.json`, row `M1_refusal_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1502 against a baseline of 1502
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming.py::TestRender::test_an_unwritable_key_is_refused_rather_than_emitted`
  - `tests/test_naming.py::TestWriteTimePadding::test_an_off_wheel_key_is_still_refused_not_padded`

Old text:

```
            f"{name}={value!r} renders as {rendered!r}, which this engine cannot "

```

New text:

```
            f"{name}={value!r} renders as {rendered!r}, which this engine declines to "

```

### `u39-naming-independent.D2_pad_condition_inverted`

Invert the padding condition: pad exactly the off-wheel values and leave real Camelot codes alone

- File: `src/cratekit/core/naming.py`
- Source: `u39-naming-independent.json`, row `D2_pad_condition_inverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1502 against a baseline of 1502
- Kills: 20 (killed)
- Killed:
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_disagreeing_title_head_leaves_the_stem_head_to_agree`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_key_only_spec_over_a_headed_title_keeps_the_whole_head`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_spec_with_no_fields_takes_both_from_the_head`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_value_the_spec_supplies_wins_over_the_head`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_an_unpadded_or_lowercase_key_agrees_with_its_padded_head`
  - `tests/test_naming.py::TestBudgetInteraction::test_build_fits_and_its_result_is_already_in_the_padded_form`
  - `tests/test_naming.py::TestBudgetInteraction::test_the_marker_is_paid_for_in_the_budget_head`
  - `tests/test_naming.py::TestMarkerCoupling::test_the_marker_text_is_a_parameter`
  - `tests/test_naming.py::TestRender::test_an_already_fitted_stem_passes_through_verbatim`
  - `tests/test_naming.py::TestRender::test_an_unwritable_key_is_refused_rather_than_emitted`
  - `tests/test_naming.py::TestRender::test_lossless_carries_no_marker`
  - `tests/test_naming.py::TestRender::test_lossy_marks_right_after_the_head`
  - `tests/test_naming.py::TestRender::test_the_key_is_written_and_measured_in_the_same_padded_form`
  - `tests/test_naming.py::TestRender::test_the_stem_is_the_fallback_when_there_is_no_title_tag`
  - `tests/test_naming.py::TestWriteTimePadding::test_a_code_read_as_data_is_normalized_by_the_padding_stage`
  - ... and 5 more, see the JSON sidecar

Old text:

```
        if key_pad == "camelot2" and parse_camelot(rendered) is not None:

```

New text:

```
        if key_pad == "camelot2" and parse_camelot(rendered) is None:

```

### `u39-naming-independent.D3_pad_condition_unreachable`

The padding stage never fires for any key_pad value, including camelot2

- File: `src/cratekit/core/naming.py`
- Source: `u39-naming-independent.json`, row `D3_pad_condition_unreachable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1502 against a baseline of 1502
- Kills: 18 (killed)
- Killed:
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_disagreeing_title_head_leaves_the_stem_head_to_agree`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_key_only_spec_over_a_headed_title_keeps_the_whole_head`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_spec_with_no_fields_takes_both_from_the_head`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_value_the_spec_supplies_wins_over_the_head`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_an_unpadded_or_lowercase_key_agrees_with_its_padded_head`
  - `tests/test_naming.py::TestBudgetInteraction::test_build_fits_and_its_result_is_already_in_the_padded_form`
  - `tests/test_naming.py::TestBudgetInteraction::test_the_marker_is_paid_for_in_the_budget_head`
  - `tests/test_naming.py::TestMarkerCoupling::test_the_marker_text_is_a_parameter`
  - `tests/test_naming.py::TestRender::test_an_already_fitted_stem_passes_through_verbatim`
  - `tests/test_naming.py::TestRender::test_lossless_carries_no_marker`
  - `tests/test_naming.py::TestRender::test_lossy_marks_right_after_the_head`
  - `tests/test_naming.py::TestRender::test_the_key_is_written_and_measured_in_the_same_padded_form`
  - `tests/test_naming.py::TestRender::test_the_stem_is_the_fallback_when_there_is_no_title_tag`
  - `tests/test_naming.py::TestWriteTimePadding::test_a_code_read_as_data_is_normalized_by_the_padding_stage`
  - `tests/test_naming.py::TestWriteTimePadding::test_rendering_the_padded_output_again_changes_nothing`
  - ... and 3 more, see the JSON sidecar

Old text:

```
        if key_pad == "camelot2" and parse_camelot(rendered) is not None:

```

New text:

```
        if key_pad == "impossible-sentinel":

```

### `u39-naming-independent.D4_fake_pad_no_zero_fill`

Padding uppercases but does not zero-fill, a plausible-looking near miss

- File: `src/cratekit/core/naming.py`
- Source: `u39-naming-independent.json`, row `D4_fake_pad_no_zero_fill`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1502 against a baseline of 1502
- Kills: 18 (killed)
- Killed:
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_disagreeing_title_head_leaves_the_stem_head_to_agree`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_key_only_spec_over_a_headed_title_keeps_the_whole_head`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_spec_with_no_fields_takes_both_from_the_head`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_a_value_the_spec_supplies_wins_over_the_head`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_an_unpadded_or_lowercase_key_agrees_with_its_padded_head`
  - `tests/test_naming.py::TestBudgetInteraction::test_build_fits_and_its_result_is_already_in_the_padded_form`
  - `tests/test_naming.py::TestBudgetInteraction::test_the_marker_is_paid_for_in_the_budget_head`
  - `tests/test_naming.py::TestMarkerCoupling::test_the_marker_text_is_a_parameter`
  - `tests/test_naming.py::TestRender::test_an_already_fitted_stem_passes_through_verbatim`
  - `tests/test_naming.py::TestRender::test_lossless_carries_no_marker`
  - `tests/test_naming.py::TestRender::test_lossy_marks_right_after_the_head`
  - `tests/test_naming.py::TestRender::test_the_key_is_written_and_measured_in_the_same_padded_form`
  - `tests/test_naming.py::TestRender::test_the_stem_is_the_fallback_when_there_is_no_title_tag`
  - `tests/test_naming.py::TestWriteTimePadding::test_a_code_read_as_data_is_normalized_by_the_padding_stage`
  - `tests/test_naming.py::TestWriteTimePadding::test_rendering_the_padded_output_again_changes_nothing`
  - ... and 3 more, see the JSON sidecar

Old text:

```
            rendered = pad_camelot(rendered)

```

New text:

```
            rendered = rendered.upper()

```

### `u39-naming-independent.E1_budget_ordering_inverted`

Existing guard sample: the budget-narrower-than-written refusal is inverted rather than disabled outright

- File: `src/cratekit/core/naming.py`
- Source: `u39-naming-independent.json`, row `E1_budget_ordering_inverted`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1502 against a baseline of 1502
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming.py::TestRender::test_the_key_is_written_and_measured_in_the_same_padded_form`
  - `tests/test_naming.py::TestTemplateValidation::test_measuring_narrower_than_writing_is_refused`

Old text:

```
        if KEY_PADS.index(self.budget_key_pad) < KEY_PADS.index(self.key_pad):

```

New text:

```
        if KEY_PADS.index(self.budget_key_pad) > KEY_PADS.index(self.key_pad):

```

### `u39-naming-independent.E2_wheel_letter_widened`

Existing guard sample: the Camelot letter class admits C, not just A/B

- File: `src/cratekit/core/naming.py`
- Source: `u39-naming-independent.json`, row `E2_wheel_letter_widened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1502 against a baseline of 1502
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_an_off_wheel_key_is_rejected_rather_than_normalized[8C]`

Old text:

```
_CAMELOT_LETTER = r"[AB]"

```

New text:

```
_CAMELOT_LETTER = r"[ABC]"

```

### `u39-naming-independent.M1_refusal_reworded`

Reword the unwritable-key refusal instead of appending to it, so an `in` assertion cannot see the change

- File: `src/cratekit/core/naming.py`
- Source: `u39-naming-independent.json`, row `M1_refusal_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1502 against a baseline of 1502
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming.py::TestRender::test_an_unwritable_key_is_refused_rather_than_emitted`
  - `tests/test_naming.py::TestWriteTimePadding::test_an_off_wheel_key_is_still_refused_not_padded`

Old text:

```
            f"{name}={value!r} renders as {rendered!r}, which this engine cannot "

```

New text:

```
            f"{name}={value!r} is not something this template can round trip: "

```

### `r290-author.J1_blocked_branch_removed`

Skip the blocked branch of raise_for_state, so a parked job falls through to the closed predicate that cannot see it, which is R-290 itself

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `J1_blocked_branch_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_outcome.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 2678 against a baseline of 2678
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
- Collected: 2678 against a baseline of 2678
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
- Collected: 2678 against a baseline of 2678
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
- Collected: 2678 against a baseline of 2678
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
- Collected: 2678 against a baseline of 2678
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
- Collected: 2678 against a baseline of 2678
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
- Collected: 2678 against a baseline of 2678
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

### `r431-b.B1_a_wanted_built_by_hand_asks`

uncredited_spellings no longer requires a spelled title, so a Wanted built from a held file asks for a companion

- File: `src/cratekit/acquire/match.py`
- Source: `r431-b.json`, row `B1_a_wanted_built_by_hand_asks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1298 against a baseline of 1298
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_held_file_crediting_somebody_else_never_calls_the_companion_stale`
  - `tests/test_match_states.py::test_a_wanted_nobody_read_from_a_listing_never_asks_for_a_companion`

Old text:

```
        if not self.spelled or self.several_artists or _credits_in(self.spelled):
```

New text:

```
        if self.several_artists or _credits_in(self.listed):
```

### `r431-b.B2_a_row_billing_a_guest_asks`

uncredited_spellings ignores several_artists, so a row crediting a guest in its artists list asks

- File: `src/cratekit/acquire/match.py`
- Source: `r431-b.json`, row `B2_a_row_billing_a_guest_asks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1298 against a baseline of 1298
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_billed_guest_survives_the_freeze_the_worker_resolves_from`
  - `tests/test_match_states.py::test_a_provider_row_billing_a_guest_in_its_artists_never_asks_for_a_companion`

Old text:

```
        if not self.spelled or self.several_artists or _credits_in(self.spelled):
```

New text:

```
        if not self.spelled or _credits_in(self.spelled):
```

### `r431-b.B3_a_listing_that_spelled_a_credit_asks`

uncredited_spellings ignores a bracketed credit, so a listing crediting Zed reaches Mira's companion

- File: `src/cratekit/acquire/match.py`
- Source: `r431-b.json`, row `B3_a_listing_that_spelled_a_credit_asks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1298 against a baseline of 1298
- Kills: 7 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_rows_suppression_spellings_are_unchanged[Sun Path (Nightwave Remix) (ft Mira)-addresses1]`
  - `tests/test_match_states.py::test_a_credited_rows_suppression_spellings_are_unchanged[Sun Path (feat. Mira) (Nightwave Remix)-addresses0]`
  - `tests/test_match_states.py::test_a_credited_rows_suppression_spellings_are_unchanged[Sun Path (with Mira)-addresses2]`
  - `tests/test_match_states.py::test_a_listing_that_spelled_a_credit_never_asks_for_a_companion[Sun Path (Nightwave Remix) (feat. Zed)]`
  - `tests/test_match_states.py::test_a_listing_that_spelled_a_credit_never_asks_for_a_companion[Sun Path (feat. Zed) (Nightwave Remix)]`
  - `tests/test_match_states.py::test_a_listing_that_spelled_a_credit_never_asks_for_a_companion[Sun Path (with Zed) - Nightwave Remix]`
  - `tests/test_match_states.py::test_a_listing_that_spelled_a_credit_never_asks_for_a_companion[Sun Path [ft. Zed] [Nightwave Remix]]`

Old text:

```
        if not self.spelled or self.several_artists or _credits_in(self.spelled):
```

New text:

```
        if not self.spelled or self.several_artists:
```

### `r431-b.B4_the_engine_never_asks`

standing_tombstone asks under the companion kind for nothing, which is the defect the unit closes

- File: `src/cratekit/acquire/match.py`
- Source: `r431-b.json`, row `B4_the_engine_never_asks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1298 against a baseline of 1298
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_deleted_track_whose_row_kept_a_credit_is_suppressed_and_not_listed`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (Nightwave Remix) (feat. Mira)-]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (feat. Mira) (Nightwave Remix)-]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (feat. Mira)-Nightwave Remix]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path [ft. Mira] [Nightwave Remix]-]`
  - `tests/test_match_states.py::test_a_provider_row_crediting_somebody_else_is_not_withheld`
  - `tests/test_match_states.py::test_the_companion_reaches_exactly_what_ownership_reached`

Old text:

```
    for identity in wanted.uncredited_spellings:
        if suppresses(UNCREDITED_KIND, identity):
```

New text:

```
    for identity in ():
        if suppresses(UNCREDITED_KIND, identity):
```

### `r431-b.B5_the_engine_ignores_companions_false`

standing_tombstone asks for a companion even when the caller said not to

- File: `src/cratekit/acquire/match.py`
- Source: `r431-b.json`, row `B5_the_engine_ignores_companions_false`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1298 against a baseline of 1298
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_held_file_crediting_somebody_else_never_calls_the_companion_stale`

Old text:

```
    if not companions:
        return None
    for identity in wanted.uncredited_spellings:
```

New text:

```
    for identity in wanted.uncredited_spellings:
```

### `r431-b.B7_the_engine_asks_under_the_tombstones_kind`

The engine's copy of the companion kind drifts onto the tombstone's own

- File: `src/cratekit/acquire/match.py`
- Source: `r431-b.json`, row `B7_the_engine_asks_under_the_tombstones_kind`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1298 against a baseline of 1298
- Kills: 8 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_deleted_track_whose_row_kept_a_credit_is_suppressed_and_not_listed`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (Nightwave Remix) (feat. Mira)-]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (feat. Mira) (Nightwave Remix)-]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (feat. Mira)-Nightwave Remix]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path [ft. Mira] [Nightwave Remix]-]`
  - `tests/test_match_states.py::test_a_provider_row_crediting_somebody_else_is_not_withheld`
  - `tests/test_match_states.py::test_the_companion_reaches_exactly_what_ownership_reached`
  - `tests/test_match_states.py::test_the_two_copies_of_the_tombstone_identity_agree_once_both_exist`

Old text:

```
UNCREDITED_KIND = "version-uncredited"
```

New text:

```
UNCREDITED_KIND = "version"
```

### `r431-b.B8_the_reader_never_counts_the_artists`

_from_row stops setting several_artists, so every provider row reads as billing one

- File: `src/cratekit/acquire/match.py`
- Source: `r431-b.json`, row `B8_the_reader_never_counts_the_artists`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1298 against a baseline of 1298
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_billed_guest_survives_the_freeze_the_worker_resolves_from`
  - `tests/test_match_states.py::test_a_provider_row_billing_a_guest_in_its_artists_never_asks_for_a_companion`

Old text:

```
        several_artists=_bills_several(row),
```

New text:

```
        several_artists=False,
```

### `r664.E1_stem_head_kept`

Stop stripping the head from the stem, the filename half of the same rule

- File: `src/cratekit/acquire/match.py`
- Source: `r664.json`, row `E1_stem_head_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1298 against a baseline of 1298
- Kills: 149 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_an_intake_job_that_owns_a_row_by_isrc_retires_the_question_an_earlier_job_asked`
  - `tests/test_match_states.py::test_a_candidate_whose_title_folds_to_something_keeps_its_identifier`
  - `tests/test_match_states.py::test_a_file_whose_artist_and_title_are_the_rows_swapped_is_still_offered`
  - `tests/test_match_states.py::test_a_half_tagged_file_does_not_get_an_identity_matching_neither_source`
  - `tests/test_match_states.py::test_a_held_emoji_row_does_not_retire_another_emoji_rows_question`
  - `tests/test_match_states.py::test_a_held_file_crediting_somebody_else_never_calls_the_companion_stale`
  - `tests/test_match_states.py::test_a_key_question_answered_elsewhere_does_not_settle_a_version_question`
  - `tests/test_match_states.py::test_a_key_that_disagrees_outright_is_a_different_answer`
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_lossy_marker_the_template_declares_is_stripped_from_the_recording`
  - `tests/test_match_states.py::test_a_one_letter_title_is_judged_by_the_same_rule`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Acoustic]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Demo]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Dub]`
  - ... and 134 more, see the JSON sidecar

Old text:

```
    body = naming.strip_heads(stem, template=template)

```

New text:

```
    body = stem

```

