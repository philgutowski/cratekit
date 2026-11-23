# Mutation table: u325-after-l-13

Measured by `scripts/mutate.py` on 2026-11-22 23:38 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 116.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:22 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 9, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r705-a.G4_trip_after_off_by_one` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 117 | 3 | killed |
| `r705-a.G5_no_trip_on_long_retry_after` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 117 | 5 | killed |
| `r705-a.G6_cooldown_not_recorded` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 117 | 8 | killed |
| `r705-a.G7_success_keeps_the_run` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 117 | 1 | killed |
| `r705-a.G8_call_ignores_the_cooldown` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 117 | 2 | killed |
| `r705-a.G9_assert_open_ignores_the_cooldown` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 117 | 4 | killed |
| `u217.G1_ceiling_says_kept` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 117 | 1 | killed |
| `r706-a.A1_ceiling_dropped` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 312 | 6 | killed |
| `r706-a.A2_ceiling_one_part_wider` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 312 | 4 | killed |
| `r706-a.A3_max_parts_four` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 312 | 5 | killed |
| `r706-a.A4_month_asked_of_one_run` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 312 | 1 | killed |
| `r706-a.A5_run_guard_dropped` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 312 | 2 | killed |
| `r706-a.A6_run_message_reworded` | `src/cratekit/intake/acrcloud.py` | maintainer | 5 file(s) | 312 | 2 | killed |
| `r706-a.A7_ceiling_message_reworded` | `src/cratekit/intake/acrcloud.py` | maintainer | 5 file(s) | 312 | 1 | killed |
| `r706-b.B1_partition_front_loads_the_remainder` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 312 | 1 | killed |
| `r706-b.B2_parts_needed_floors` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 312 | 8 | killed |
| `r706-b.B3_partition_drops_the_remainder` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 312 | 5 | killed |
| `r706-b.B4_parts_reported_as_one` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 312 | 7 | killed |
| `r706-b.B5_chunks_count_the_first_part` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 312 | 6 | killed |
| `r706-b.B6_grid_not_partitioned` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 312 | 7 | killed |
| `r816-a.A1_too_coarse_protection` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 6 | killed |
| `r816-a.A2_held_out` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 2 | killed |
| `r816-a.A3_multi_valued` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 2 | killed |
| `r816-a.A4_agreement` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 12 | killed |
| `r816-a.A5_unreadable_is_blank` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 2 | killed |
| `r816-a.A6_first_value` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 2 | killed |
| `r816-a.A7_digest_counts` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 1 | killed |
| `r816-a.A8_leave_unmatched` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 2 | killed |
| `r816-b.B1_stale_check` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 2 | killed |
| `r816-b.B2_stale_tombstone` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 5 | killed |
| `r816-b.B3_blank_spellings` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 3 | killed |
| `r816-b.B4_restore_detection` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 1 | killed |
| `r816-c.B6_bookkeeping_exempt` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 10 | killed |
| `r816-c.B7_read_back_word` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 2 | killed |
| `r816-c.B8_read_back_columns` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 1 | killed |
| `r816-c.B9_cache_reset` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 1 | killed |
| `r816-d.C1_acknowledgment` | `src/cratekit/tagging/rows_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `r816-d.C2_empty_plan` | `src/cratekit/tagging/rows_cli.py` | user | 1 file(s) | 72 | 2 | killed |
| `r816-d.C3_majority_unmapped` | `src/cratekit/tagging/rows_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `r816-d.C4_only_apply_writes` | `src/cratekit/tagging/rows_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `r816-d.C5_leave_reaches_the_plan` | `src/cratekit/tagging/rows_cli.py` | user | 1 file(s) | 72 | 2 | killed |
| `r44-a.S10_default_slug` | `src/cratekit/core/session.py` | maintainer | 2 file(s) | 475 | 1 | killed |
| `r44-a.S1_empty_slot` | `src/cratekit/core/session.py` | user | 2 file(s) | 475 | 2 | killed |
| `r44-a.S2_proved_widened` | `src/cratekit/core/session.py` | user | 2 file(s) | 475 | 4 | killed |
| `r44-a.S3_default_to_library` | `src/cratekit/core/session.py` | user | 2 file(s) | 475 | 2 | killed |
| `r44-a.S4_inside_root_unheld` | `src/cratekit/core/session.py` | user | 2 file(s) | 475 | 6 | killed |
| `r44-a.S5_not_destructive` | `src/cratekit/core/session.py` | user | 2 file(s) | 475 | 5 | killed |
| `r44-a.S6_oserror_escapes` | `src/cratekit/core/session.py` | user | 2 file(s) | 475 | 2 | killed |
| `r44-a.S7_probe_the_target` | `src/cratekit/core/session.py` | user | 2 file(s) | 475 | 3 | killed |
| `r44-a.S8_wording_held_to` | `src/cratekit/core/session.py` | user | 2 file(s) | 475 | 1 | killed |
| `r44-a.S9_offer_to_record_nested` | `src/cratekit/core/session.py` | user | 2 file(s) | 475 | 1 | killed |
| `u71-b.B10_occupied_at_move` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 2 | killed |
| `u71-b.B11_nothing_moved` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 1 | killed |
| `u71-b.B12_take_back_folder` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 1 | killed |
| `u71-b.B13_unlink_destination` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u71-b.B1_target_under_staging` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 1 | killed |
| `u71-b.B2_device` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 1 | killed |
| `u71-b.B3_destination_exists` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 1 | killed |
| `u71-b.B4_export_missing` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 1 | killed |
| `u71-b.B5_trial_splice` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 1 | killed |
| `u71-b.B6_trial_playlist` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 1 | killed |
| `u71-c.C1_nothing_movable_rerun` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 1 | killed |
| `u71.A10_root_absent` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 1 | killed |
| `u71.A11_owned_folder` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 1 | killed |
| `u71.A12_staging_inside_library` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 2 | killed |
| `u71.A1_listing_dotfile` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 1 | killed |
| `u71.A2_listing_suffix` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 2 | killed |
| `u71.A3_listing_regular_file` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 1 | killed |
| `u71.A4_digest_names_only` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 2 | killed |
| `u71.A5_digest_no_mtime` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 2 | killed |
| `u71.A6_stale_refusal` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 3 | killed |
| `u71.A7_stale_listing_only` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 2 | killed |
| `u71.A9_plan_empty` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 1 | killed |
| `r375-a.S10_commit_not_persisted_at_once` | `src/cratekit/core/session.py` | user | 4 file(s) | 394 | 1 | killed |
| `r375-a.S11_commit_replaces_the_summary` | `src/cratekit/core/session.py` | user | 4 file(s) | 394 | 2 | killed |
| `r375-a.S1_keep_is_ignored` | `src/cratekit/core/session.py` | user | 4 file(s) | 394 | 38 | killed |
| `r375-a.S2_record_inside_the_watch` | `src/cratekit/core/session.py` | user | 4 file(s) | 394 | 3 | killed |
| `r375-a.S3_a_raise_is_not_abandoned` | `src/cratekit/core/session.py` | user | 4 file(s) | 394 | 13 | killed |
| `r375-a.S4_abandon_failure_replaces_the_error` | `src/cratekit/core/session.py` | user | 4 file(s) | 394 | 1 | killed |
| `r375-a.S5_clean_close_refusal_leaves_it_open` | `src/cratekit/core/session.py` | user | 4 file(s) | 394 | 1 | killed |
| `r375-a.S6_close_ignores_the_intent` | `src/cratekit/core/session.py` | user | 4 file(s) | 394 | 11 | killed |
| `r375-a.S7_close_drops_the_identity_seam` | `src/cratekit/core/session.py` | maintainer | 4 file(s) | 394 | 4 | killed |
| `r375-a.S8_record_names_no_actor` | `src/cratekit/core/session.py` | user | 4 file(s) | 394 | 2 | killed |
| `r375-a.S9_record_names_no_acknowledgment` | `src/cratekit/core/session.py` | user | 4 file(s) | 394 | 2 | killed |
| `r83.D1_offer_defect` | `src/cratekit/acquire/adapter.py` | user | 6 file(s) | 755 | 8 | killed |
| `r83.D2_fetch_defect` | `src/cratekit/acquire/adapter.py` | user | 6 file(s) | 755 | 2 | killed |
| `r83.D3_drop_attribute_error` | `src/cratekit/acquire/adapter.py` | user | 6 file(s) | 755 | 6 | killed |
| `r83.D4_drop_type_error` | `src/cratekit/acquire/adapter.py` | user | 6 file(s) | 755 | 2 | killed |
| `r83.D5_drop_name_error` | `src/cratekit/acquire/adapter.py` | user | 6 file(s) | 755 | 4 | killed |
| `r83.D6_remedy` | `src/cratekit/acquire/adapter.py` | user | 6 file(s) | 755 | 11 | killed |
| `r83.D7_detail_names_class` | `src/cratekit/acquire/adapter.py` | maintainer | 6 file(s) | 755 | 9 | killed |
| `u274.P1_gone_never` | `src/cratekit/acquire/provider_session.py` | user | 6 file(s) | 449 | 1 | killed |
| `u274.P2_gone_overflow` | `src/cratekit/acquire/provider_session.py` | user | 6 file(s) | 449 | 1 | killed |
| `u274.P3_gone_permission` | `src/cratekit/acquire/provider_session.py` | user | 6 file(s) | 449 | 2 | killed |
| `u274.P4_sweep_live` | `src/cratekit/acquire/provider_session.py` | user | 6 file(s) | 449 | 4 | killed |
| `u274.P5_sweep_not_dir` | `src/cratekit/acquire/provider_session.py` | user | 6 file(s) | 449 | 2 | killed |
| `u274.P6_sweep_other_account` | `src/cratekit/acquire/provider_session.py` | user | 6 file(s) | 449 | 1 | killed |
| `u274.P7_no_sweep` | `src/cratekit/acquire/provider_session.py` | user | 6 file(s) | 449 | 1 | killed |
| `u274.P8_captured_always` | `src/cratekit/acquire/provider_session.py` | user | 6 file(s) | 449 | 3 | killed |
| `u274.P9_captured_nothing` | `src/cratekit/acquire/provider_session.py` | user | 6 file(s) | 449 | 6 | killed |
| `u274.C1_worker_names_no_drive` | `src/cratekit/acquire/cli.py` | user | 6 file(s) | 449 | 17 | killed |
| `u102-a.P1_root_boundary` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `u102-a.P2_root_casefold` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `u102-a.P3_root_filter` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 2 | killed |
| `u102-a.P4_unchanged` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 1 | killed |

## Zero rows and what they owe

- `u71-b.B13_unlink_destination` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

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
  - `tests/test_provider_gate.py::test_a_retry_after_at_or_above_the_cooldown_trips_at_once`
  - `tests/test_provider_gate.py::test_a_retry_after_longer_than_the_cooldown_sets_the_lift_time`
  - `tests/test_provider_gate.py::test_the_spend_line_survives_a_refusal`

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
- Kills: 8 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_cooldown_written_by_one_process_refuses_a_verb_started_in_another`
  - `tests/test_provider_gate.py::test_a_retry_after_at_or_above_the_cooldown_trips_at_once`
  - `tests/test_provider_gate.py::test_a_retry_after_longer_than_the_cooldown_sets_the_lift_time`
  - `tests/test_provider_gate.py::test_client_session_refuses_inside_the_cooldown_before_building_a_client`
  - `tests/test_provider_gate.py::test_inside_the_cooldown_a_call_is_refused_before_it_is_sent`
  - `tests/test_provider_gate.py::test_inside_the_cooldown_assert_open_refuses_naming_the_lift_time`
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
  - `tests/test_provider_gate.py::test_inside_the_cooldown_a_call_is_refused_before_it_is_sent`

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

### `r706-a.A1_ceiling_dropped`

Drop the parts ceiling, so a file of any length is cut into as many parts as it takes

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-a.json`, row `A1_ceiling_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 6 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_nonsense_duration_is_refused_by_the_bound_before_any_grid_exists`
  - `tests/intake/test_recognition.py::test_a_recording_over_the_parts_ceiling_is_refused_before_any_carve_call_or_credential`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_reads_what_is_owed_and_the_parts_ceiling_reads_the_grid`
  - `tests/intake/test_recognition.py::test_the_per_run_bound_refuses_before_any_carve_call_or_credential`
  - `tests/intake/test_recognition.py::test_the_two_spend_refusals_and_a_miss_are_three_different_things`
  - `tests/intake/test_workers.py::test_a_recording_over_the_parts_ceiling_is_refused_at_the_queue_and_queues_nothing`

Old text:

```
    assert_one_set(spend, planned=planned)
    offsets = sample_offsets(duration_s)
```

New text:

```
    offsets = sample_offsets(duration_s)
```

### `r706-a.A2_ceiling_one_part_wider`

The ceiling admits one part more than MAX_PARTS, a coefficient row on the bound

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-a.json`, row `A2_ceiling_one_part_wider`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_recording_over_the_parts_ceiling_is_refused_before_any_carve_call_or_credential`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_reads_what_is_owed_and_the_parts_ceiling_reads_the_grid`
  - `tests/intake/test_recognition.py::test_the_two_spend_refusals_and_a_miss_are_three_different_things`
  - `tests/intake/test_workers.py::test_a_recording_over_the_parts_ceiling_is_refused_at_the_queue_and_queues_nothing`

Old text:

```
    ceiling = budget.per_run * MAX_PARTS
```

New text:

```
    ceiling = budget.per_run * (MAX_PARTS + 1)
```

### `r706-a.A3_max_parts_four`

MAX_PARTS moves from three to four, the decision's Part A, B and C plus one

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-a.json`, row `A3_max_parts_four`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 5 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_recording_over_the_parts_ceiling_is_refused_before_any_carve_call_or_credential`
  - `tests/intake/test_recognition.py::test_a_two_hour_set_is_one_run_a_five_hour_mix_is_two_parts_and_nine_hours_is_over_the_ceiling`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_reads_what_is_owed_and_the_parts_ceiling_reads_the_grid`
  - `tests/intake/test_recognition.py::test_the_two_spend_refusals_and_a_miss_are_three_different_things`
  - `tests/intake/test_workers.py::test_a_recording_over_the_parts_ceiling_is_refused_at_the_queue_and_queues_nothing`

Old text:

```
MAX_PARTS = 3
```

New text:

```
MAX_PARTS = 4
```

### `r706-a.A4_month_asked_of_one_run`

The month is asked about one run's worth rather than the whole set, so a set the month cannot afford spends its first part

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-a.json`, row `A4_month_asked_of_one_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_the_month_is_asked_once_over_the_whole_set_before_the_first_part`

Old text:

```
        assert_month_within(spend, planned=len(owed), used_this_month=counter.used(month))
```

New text:

```
        assert_month_within(
            spend, planned=min(len(owed), spend.per_run), used_this_month=counter.used(month)
        )
```

### `r706-a.A5_run_guard_dropped`

Drop the per part run guard, so an oversize part is paid for

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-a.json`, row `A5_run_guard_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_partition_that_hands_back_an_oversize_part_is_refused_before_any_call[one-oversize-part]`
  - `tests/intake/test_recognition.py::test_a_partition_that_hands_back_an_oversize_part_is_refused_before_any_call[oversize-second-part]`

Old text:

```
    for part in parts:
        assert_run_within(spend, planned=sum(1 for offset in part if offset in still_owed))
    keys = ("", "")
```

New text:

```
    keys = ("", "")
```

### `r706-a.A6_run_message_reworded`

Reword the per part run refusal, do not append to it

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-a.json`, row `A6_run_message_reworded`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_partition_that_hands_back_an_oversize_part_is_refused_before_any_call[one-oversize-part]`
  - `tests/intake/test_recognition.py::test_a_partition_that_hands_back_an_oversize_part_is_refused_before_any_call[oversize-second-part]`

Old text:

```
            f"this run would take {planned} recognition calls and the per run "
```

New text:

```
            f"this part needs {planned} recognition calls and the per run "
```

### `r706-a.A7_ceiling_message_reworded`

Reword the ceiling refusal so it no longer says the file is not one set

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-a.json`, row `A7_ceiling_message_reworded`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_recording_over_the_parts_ceiling_is_refused_before_any_carve_call_or_credential`

Old text:

```
            f"nothing was sent. A file this long is not one set, so split it "
```

New text:

```
            f"nothing was sent. A file this long is too long, so split it "
```

### `r706-b.B1_partition_front_loads_the_remainder`

The remainder goes to the first part whole instead of one chunk to each of the first parts, so a cut is uneven and can exceed the bound

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-b.json`, row `B1_partition_front_loads_the_remainder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_partition_cuts_the_grid_into_the_fewest_even_parts_under_the_bound[5-2-sizes6]`

Old text:

```
        size = base + (1 if index < extra else 0)
```

New text:

```
        size = base + (extra if index == 0 else 0)
```

### `r706-b.B2_parts_needed_floors`

parts_needed floors instead of ceiling, so 732 chunks is one part of 732

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-b.json`, row `B2_parts_needed_floors`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 8 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_five_hour_mix_is_identified_in_two_even_parts_as_one_set`
  - `tests/intake/test_recognition.py::test_a_two_hour_set_is_one_run_a_five_hour_mix_is_two_parts_and_nine_hours_is_over_the_ceiling`
  - `tests/intake/test_recognition.py::test_partition_cuts_the_grid_into_the_fewest_even_parts_under_the_bound[401-400-sizes3]`
  - `tests/intake/test_recognition.py::test_partition_cuts_the_grid_into_the_fewest_even_parts_under_the_bound[5-2-sizes6]`
  - `tests/intake/test_recognition.py::test_partition_cuts_the_grid_into_the_fewest_even_parts_under_the_bound[7-3-sizes7]`
  - `tests/intake/test_recognition.py::test_partition_cuts_the_grid_into_the_fewest_even_parts_under_the_bound[732-400-sizes4]`
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`
  - `tests/intake/test_workers.py::test_identify_only_says_the_same_parts_note`

Old text:

```
    return -(-planned // per_run)
```

New text:

```
    return max(1, planned // per_run)
```

### `r706-b.B3_partition_drops_the_remainder`

Every part is cut to the base size, so the remainder chunks fall out of the grid

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-b.json`, row `B3_partition_drops_the_remainder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 5 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_partition_cuts_the_grid_into_the_fewest_even_parts_under_the_bound[401-400-sizes3]`
  - `tests/intake/test_recognition.py::test_partition_cuts_the_grid_into_the_fewest_even_parts_under_the_bound[5-2-sizes6]`
  - `tests/intake/test_recognition.py::test_partition_cuts_the_grid_into_the_fewest_even_parts_under_the_bound[7-3-sizes7]`
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`
  - `tests/intake/test_workers.py::test_identify_only_says_the_same_parts_note`

Old text:

```
        parts.append(tuple(offsets[start : start + size]))
```

New text:

```
        parts.append(tuple(offsets[start : start + base]))
```

### `r706-b.B4_parts_reported_as_one`

The result says one part whatever the cut

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-b.json`, row `B4_parts_reported_as_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 7 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_five_hour_mix_is_identified_in_two_even_parts_as_one_set`
  - `tests/intake/test_recognition.py::test_a_split_set_is_served_from_the_cache_as_one_plan`
  - `tests/intake/test_recognition.py::test_a_split_set_that_owes_only_a_gap_meets_the_run_bound_on_what_is_owed`
  - `tests/intake/test_recognition.py::test_the_month_is_asked_once_over_the_whole_set_before_the_first_part`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_reads_what_is_owed_and_the_parts_ceiling_reads_the_grid`
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`
  - `tests/intake/test_workers.py::test_identify_only_says_the_same_parts_note`

Old text:

```
        parts=len(parts),
```

New text:

```
        parts=1,
```

### `r706-b.B5_chunks_count_the_first_part`

The walked grid is rebuilt from the first part only, so chunks and cached count one part

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-b.json`, row `B5_chunks_count_the_first_part`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 6 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_five_hour_mix_is_identified_in_two_even_parts_as_one_set`
  - `tests/intake/test_recognition.py::test_a_split_set_is_served_from_the_cache_as_one_plan`
  - `tests/intake/test_recognition.py::test_a_split_set_that_owes_only_a_gap_meets_the_run_bound_on_what_is_owed`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_reads_what_is_owed_and_the_parts_ceiling_reads_the_grid`
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`
  - `tests/intake/test_workers.py::test_identify_only_says_the_same_parts_note`

Old text:

```
    offsets = tuple(offset for part in parts for offset in part)
```

New text:

```
    offsets = tuple(parts[0]) if parts else ()
```

### `r706-b.B6_grid_not_partitioned`

identify hands the whole grid over as one part, so the run guard meets a 5 hour mix

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-b.json`, row `B6_grid_not_partitioned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 7 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_five_hour_mix_is_identified_in_two_even_parts_as_one_set`
  - `tests/intake/test_recognition.py::test_a_split_set_is_served_from_the_cache_as_one_plan`
  - `tests/intake/test_recognition.py::test_a_split_set_that_owes_only_a_gap_meets_the_run_bound_on_what_is_owed`
  - `tests/intake/test_recognition.py::test_the_month_is_asked_once_over_the_whole_set_before_the_first_part`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_reads_what_is_owed_and_the_parts_ceiling_reads_the_grid`
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`
  - `tests/intake/test_workers.py::test_identify_only_says_the_same_parts_note`

Old text:

```
    parts = partition(offsets, per_run=spend.per_run)
```

New text:

```
    parts = (offsets,)
```

### `r816-a.A1_too_coarse_protection`

plan_rows: drop the rule that a too coarse file word does not replace a specific row word

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-a.json`, row `A1_too_coarse_protection`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 6 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_second_run_after_a_clean_one_asks_and_is_a_no_op`
  - `tests/test_tag_rows.py::test_a_too_coarse_file_does_not_replace_a_specific_row`
  - `tests/test_tag_rows.py::test_every_live_row_is_counted_exactly_once_and_items_are_in_identifier_order`
  - `tests/test_tag_rows.py::test_planned_written_and_read_back_through_the_two_acts`
  - `tests/test_tag_rows.py::test_the_apply_writes_the_genre_and_no_other_column_of_any_row`
  - `tests/test_tag_rows.py::test_the_pairs_are_the_writes_counted_largest_first`

Old text:

```
        elif _protected(declared, row_word, file_word):
```

New text:

```
        elif False:
```

### `r816-a.A2_held_out`

plan_rows: ignore the rows a person held out, so a hand set genre is planned as a write

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-a.json`, row `A2_held_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_held_row_survives_the_write_and_the_apply_must_name_it_again`
  - `tests/test_tag_rows.py::test_a_row_a_person_holds_out_is_listed_and_left`

Old text:

```
        if content_id in held_out:
```

New text:

```
        if False:
```

### `r816-a.A3_multi_valued`

plan_rows: write a row from a file holding more than one genre

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-a.json`, row `A3_multi_valued`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_file_holding_two_genres_is_left_alone_and_both_are_shown`
  - `tests/test_tag_rows.py::test_two_genres_in_an_id3_frame_read_as_they_do_in_a_list_container`

Old text:

```
            if several:
```

New text:

```
            if False:
```

### `r816-a.A4_agreement`

plan_rows: stop reading equal words as agreement, so every row with a file genre is a write

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-a.json`, row `A4_agreement`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 12 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_file_holding_two_genres_is_left_alone_and_both_are_shown`
  - `tests/test_tag_rows.py::test_a_row_and_file_that_agree_are_not_in_the_plan`
  - `tests/test_tag_rows.py::test_a_second_apply_plans_nothing_and_writes_nothing`
  - `tests/test_tag_rows.py::test_a_second_run_after_a_clean_one_asks_and_is_a_no_op`
  - `tests/test_tag_rows.py::test_an_empty_plan_still_asks_and_opens_nothing_to_write`
  - `tests/test_tag_rows.py::test_an_empty_second_value_is_not_a_second_genre_and_not_an_unknown_word`
  - `tests/test_tag_rows.py::test_an_identifier_held_out_that_names_no_differing_row_is_carried_and_digested`
  - `tests/test_tag_rows.py::test_every_live_row_is_counted_exactly_once_and_items_are_in_identifier_order`
  - `tests/test_tag_rows.py::test_planned_written_and_read_back_through_the_two_acts`
  - `tests/test_tag_rows.py::test_the_apply_writes_the_genre_and_no_other_column_of_any_row`
  - `tests/test_tag_rows.py::test_the_digest_moves_when_only_a_count_moves`
  - `tests/test_tag_rows.py::test_two_genres_in_an_id3_frame_read_as_they_do_in_a_list_container`

Old text:

```
        if row_word == file_word:
```

New text:

```
        if False:
```

### `r816-a.A5_unreadable_is_blank`

_file_word: count a file whose tags would not open as a file with no genre

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-a.json`, row `A5_unreadable_is_blank`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_file_no_tag_library_opens_is_unreadable_and_not_blank`
  - `tests/test_tag_rows.py::test_every_live_row_is_counted_exactly_once_and_items_are_in_identifier_order`

Old text:

```
        return "", FILE_UNREADABLE
```

New text:

```
        return "", FILE_BLANK
```

### `r816-a.A6_first_value`

_file_word: compare the checked reader's text as it came, null bytes and all

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-a.json`, row `A6_first_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_an_empty_second_value_is_not_a_second_genre_and_not_an_unknown_word`
  - `tests/test_tag_rows.py::test_two_genres_in_an_id3_frame_read_as_they_do_in_a_list_container`

Old text:

```
    word = next((part.strip() for part in text.split("\x00") if part.strip()), "")
```

New text:

```
    word = text.strip()
```

### `r816-a.A7_digest_counts`

RowsPlan.digest: leave the outcome counts out of the digest

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-a.json`, row `A7_digest_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_the_digest_moves_when_only_a_count_moves`

Old text:

```
                "counts": dict(self.counts),

```

New text:

```
(empty)
```

### `r816-a.A8_leave_unmatched`

plan_rows: drop the identifiers held out that name no differing row

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-a.json`, row `A8_leave_unmatched`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_mistyped_identifier_is_shown_at_the_gate_and_warned_about`
  - `tests/test_tag_rows.py::test_an_identifier_held_out_that_names_no_differing_row_is_carried_and_digested`

Old text:

```
        leave_unmatched=tuple(sorted(held_out - listed)),
```

New text:

```
        leave_unmatched=(),
```

### `r816-b.B1_stale_check`

apply_rows: write without asking whether each row is still as the plan read it

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-b.json`, row `B1_stale_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_row_removed_since_the_plan_refuses_and_nothing_is_written`
  - `tests/test_tag_rows.py::test_a_row_whose_genre_moved_since_the_plan_refuses_and_nothing_is_written`

Old text:

```
    assert_rows_as_planned(plan, mapped)

```

New text:

```
(empty)
```

### `r816-b.B2_stale_tombstone`

assert_rows_as_planned: write a row removed since the plan

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-b.json`, row `B2_stale_tombstone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 5 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_blank_row_is_as_planned_however_the_database_spells_blank[0_0]`
  - `tests/test_tag_rows.py::test_a_blank_row_is_as_planned_however_the_database_spells_blank[0_1]`
  - `tests/test_tag_rows.py::test_a_blank_row_is_as_planned_however_the_database_spells_blank[None]`
  - `tests/test_tag_rows.py::test_a_blank_row_is_as_planned_however_the_database_spells_blank[]`
  - `tests/test_tag_rows.py::test_a_row_removed_since_the_plan_refuses_and_nothing_is_written`

Old text:

```
        if row is None or trees.soft_delete_marker(row):
```

New text:

```
        if row is None:
```

### `r816-b.B3_blank_spellings`

assert_rows_as_planned: read two spellings of a blank genre as a change

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-b.json`, row `B3_blank_spellings`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_blank_row_is_as_planned_however_the_database_spells_blank[0_0]`
  - `tests/test_tag_rows.py::test_a_blank_row_is_as_planned_however_the_database_spells_blank[0_1]`
  - `tests/test_tag_rows.py::test_a_blank_row_is_as_planned_however_the_database_spells_blank[]`

Old text:

```
        if (_empty(held) and _empty(planned)) or str(held) == str(planned):
```

New text:

```
        if str(held) == str(planned):
```

### `r816-b.B4_restore_detection`

apply_rows: record a fingerprint without first looking for an out of band restore

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-b.json`, row `B4_restore_detection`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_restore_out_of_band_is_marked_before_this_write_replaces_the_evidence`

Old text:

```
    convergence.detect_out_of_band_restore(cfg, db, tree_registry.read(cfg))

```

New text:

```
(empty)
```

### `r816-c.B6_bookkeeping_exempt`

judge: stop exempting the binding's bookkeeping columns, so every clean write reads as moved

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-c.json`, row `B6_bookkeeping_exempt`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 10 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_file_on_a_volume_that_is_not_mounted_is_counted_and_the_run_does_not_fail`
  - `tests/test_tag_rows.py::test_a_held_row_survives_the_write_and_the_apply_must_name_it_again`
  - `tests/test_tag_rows.py::test_a_mistyped_identifier_is_shown_at_the_gate_and_warned_about`
  - `tests/test_tag_rows.py::test_a_person_reads_the_counts_and_the_pairs_at_the_gate_and_after_the_write`
  - `tests/test_tag_rows.py::test_a_second_run_after_a_clean_one_asks_and_is_a_no_op`
  - `tests/test_tag_rows.py::test_a_word_the_library_has_no_row_for_names_the_act_on_a_run_that_wrote`
  - `tests/test_tag_rows.py::test_planned_written_and_read_back_through_the_two_acts`
  - `tests/test_tag_rows.py::test_the_apply_writes_the_genre_and_no_other_column_of_any_row`
  - `tests/test_tag_rows.py::test_the_genre_report_stops_naming_the_old_word_after_the_run`
  - `tests/test_tag_rows.py::test_the_read_back_passes_a_row_whose_genre_and_bookkeeping_alone_moved`

Old text:

```
            and column not in rb_writer.BOOKKEEPING_COLUMNS

```

New text:

```
(empty)
```

### `r816-c.B7_read_back_word`

judge: stop comparing the genre read back with the file's word

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-c.json`, row `B7_read_back_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_the_read_back_names_a_row_that_does_not_carry_its_files_word`
  - `tests/test_tag_rows.py::test_the_read_back_names_a_row_whose_genre_points_at_no_lookup_row`

Old text:

```
        if word != item.file:
```

New text:

```
        if False:
```

### `r816-c.B8_read_back_columns`

judge: stop reporting another column that moved

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-c.json`, row `B8_read_back_columns`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_the_read_back_names_every_other_column_that_moved`

Old text:

```
        if changed:
```

New text:

```
        if False:
```

### `r816-c.B9_cache_reset`

apply_rows: leave the collection cache holding the words as they were

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-c.json`, row `B9_cache_reset`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_the_genre_report_stops_naming_the_old_word_after_the_run`

Old text:

```
    collection.reset_cache()

```

New text:

```
(empty)
```

### `r816-d.C1_acknowledgment`

tag_rows: ask the gate without reading the backup acknowledgment first

- File: `src/cratekit/tagging/rows_cli.py`
- Source: `r816-d.json`, row `C1_acknowledgment`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    session.assert_backup_acknowledged(cfg)

```

New text:

```
(empty)
```

### `r816-d.C2_empty_plan`

tag_rows: open the database to write for a plan that writes nothing

- File: `src/cratekit/tagging/rows_cli.py`
- Source: `r816-d.json`, row `C2_empty_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_second_run_after_a_clean_one_asks_and_is_a_no_op`
  - `tests/test_tag_rows.py::test_an_empty_plan_still_asks_and_opens_nothing_to_write`

Old text:

```
    if not plan.writes:
```

New text:

```
    if False:
```

### `r816-d.C3_majority_unmapped`

_plan: plan over a library most of whose rows are under no prefix rule

- File: `src/cratekit/tagging/rows_cli.py`
- Source: `r816-d.json`, row `C3_majority_unmapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_library_most_of_whose_rows_are_unmapped_refuses_before_the_gate`

Old text:

```
        if totals.majority_unmapped:
```

New text:

```
        if False:
```

### `r816-d.C4_only_apply_writes`

tag_rows: write on any answer

- File: `src/cratekit/tagging/rows_cli.py`
- Source: `r816-d.json`, row `C4_only_apply_writes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_the_plan_refusal_writes_nothing_and_a_declined_gate_writes_nothing`

Old text:

```
    if ctx.gate.require(spec, plan=data, context=_facts(plan)) != "apply":
```

New text:

```
    if ctx.gate.require(spec, plan=data, context=_facts(plan)) == "never":
```

### `r816-d.C5_leave_reaches_the_plan`

_plan: drop the rows held out on the command line

- File: `src/cratekit/tagging/rows_cli.py`
- Source: `r816-d.json`, row `C5_leave_reaches_the_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_held_row_survives_the_write_and_the_apply_must_name_it_again`
  - `tests/test_tag_rows.py::test_a_mistyped_identifier_is_shown_at_the_gate_and_warned_about`

Old text:

```
        return rows.plan_rows(cfg, db, declared, leave=leave)
```

New text:

```
        return rows.plan_rows(cfg, db, declared, leave=())
```

### `r44-a.S10_default_slug`

Look the slug up with a default, so a verdict in neither table wears the mismatch slug

- File: `src/cratekit/core/session.py`
- Source: `r44-a.json`, row `S10_default_slug`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 475 against a baseline of 475
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_verdict_in_neither_table_fails_rather_than_wearing_the_mismatch_slug`

Old text:

```
            reason = _MAPPED_REASONS[status.state]
```

New text:

```
            reason = _MAPPED_REASONS.get(status.state, "mapped-volume-mismatch")
```

### `r44-a.S1_empty_slot`

Never refuse an empty mount slot, so an identity read through an ejected drive's leftover directory is compared and can match

- File: `src/cratekit/core/session.py`
- Source: `r44-a.json`, row `S1_empty_slot`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 475 against a baseline of 475
- Kills: 2 (killed)
- Killed:
  - `tests/test_write_session.py::test_an_ejected_drive_is_never_offered_the_boot_disks_identity_to_record`
  - `tests/test_write_session.py::test_an_empty_mount_slot_refuses_even_when_the_recorded_identity_matches_it`

Old text:

```
        source = preflight.identity_source(probe)
        if source is None:
```

New text:

```
        source = preflight.identity_source(probe)
        if False:
```

### `r44-a.S2_proved_widened`

Let NOT_MOUNTED count as a proved identity, which is the pass set widening by one verdict

- File: `src/cratekit/core/session.py`
- Source: `r44-a.json`, row `S2_proved_widened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 475 against a baseline of 475
- Kills: 4 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_drive_ejected_mid_queue_is_not_settled_as_a_queue_of_deletions`
  - `tests/test_write_session.py::test_a_recorded_volume_that_is_not_mounted_anywhere_has_its_own_slug`
  - `tests/test_write_session.py::test_every_mount_verdict_about_a_rule_target_was_decided_exactly_once[MountState.NOT_MOUNTED]`
  - `tests/test_write_session.py::test_the_verdicts_that_prove_a_rule_target_are_spelled_out`

Old text:

```
    {preflight.MountState.OK, preflight.MountState.LIBRARY_PATH_MISSING}
)
```

New text:

```
    {
        preflight.MountState.OK,
        preflight.MountState.LIBRARY_PATH_MISSING,
        preflight.MountState.NOT_MOUNTED,
    }
)
```

### `r44-a.S3_default_to_library`

Hold a rule outside the library root with nothing recorded to the LIBRARY'S identity instead of refusing it

- File: `src/cratekit/core/session.py`
- Source: `r44-a.json`, row `S3_default_to_library`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 475 against a baseline of 475
- Kills: 2 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_rule_is_held_to_its_own_identity_then_the_librarys_then_to_nothing`
  - `tests/test_write_session.py::test_a_target_outside_the_root_with_nothing_recorded_refuses_and_hands_over_the_identity`

Old text:

```
    if inside.resolution is locations.Resolution.UNDER_ROOT:
        return cfg.library.volume_id
    return None
```

New text:

```
    if inside.resolution is locations.Resolution.UNDER_ROOT:
        return cfg.library.volume_id
    return cfg.library.volume_id
```

### `r44-a.S4_inside_root_unheld`

Hold a rule inside the library root to nothing of the library's, so a nested foreign volume is judged as unrecorded rather than foreign

- File: `src/cratekit/core/session.py`
- Source: `r44-a.json`, row `S4_inside_root_unheld`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 475 against a baseline of 475
- Kills: 6 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_rule_onto_the_wrong_volume_refuses_rather_than_trashing_the_only_copy`
  - `tests/test_write_session.py::test_a_different_disk_at_a_rules_target_refuses_and_names_the_rule`
  - `tests/test_write_session.py::test_a_foreign_volume_under_a_rule_that_recorded_nothing_offers_nothing_to_record`
  - `tests/test_write_session.py::test_a_rule_is_held_to_its_own_identity_then_the_librarys_then_to_nothing`
  - `tests/test_write_session.py::test_a_volume_nested_under_the_library_root_is_not_the_library`
  - `tests/test_write_session.py::test_the_file_is_proved_where_the_file_is_and_not_where_the_rule_points`

Old text:

```
    if inside.resolution is locations.Resolution.UNDER_ROOT:
        return cfg.library.volume_id
    return None
```

New text:

```
    return None
```

### `r44-a.S5_not_destructive`

Assert a rule target at read strength, where an unreadable or unrecorded identity is tolerated

- File: `src/cratekit/core/session.py`
- Source: `r44-a.json`, row `S5_not_destructive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 475 against a baseline of 475
- Kills: 5 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_rule_onto_the_wrong_volume_refuses_rather_than_trashing_the_only_copy`
  - `tests/test_write_session.py::test_a_provider_that_cannot_read_the_identity_to_hand_over_is_a_refusal_too`
  - `tests/test_write_session.py::test_a_rule_target_whose_identity_cannot_be_read_refuses`
  - `tests/test_write_session.py::test_a_target_outside_the_root_with_nothing_recorded_refuses_and_hands_over_the_identity`
  - `tests/test_write_session.py::test_the_seams_handed_in_are_the_seams_used`

Old text:

```
                expected_rule_identity(cfg, rule),
                destructive=True,
```

New text:

```
                expected_rule_identity(cfg, rule),
                destructive=False,
```

### `r44-a.S6_oserror_escapes`

Let an OSError from the walk or the identity read escape the gate instead of becoming a refusal

- File: `src/cratekit/core/session.py`
- Source: `r44-a.json`, row `S6_oserror_escapes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 475 against a baseline of 475
- Kills: 2 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_provider_that_cannot_read_the_identity_to_hand_over_is_a_refusal_too`
  - `tests/test_write_session.py::test_a_way_to_the_target_this_account_cannot_walk_is_a_refusal_and_not_a_traceback`

Old text:

```
    except OSError as exc:
        # "I COULD NOT LOOK" IS ITS OWN ANSWER.
```

New text:

```
    except KeyboardInterrupt as exc:
        # "I COULD NOT LOOK" IS ITS OWN ANSWER.
```

### `r44-a.S7_probe_the_target`

Probe the rule's target for a file instead of the file's own directory, so a volume nested under the target is never seen

- File: `src/cratekit/core/session.py`
- Source: `r44-a.json`, row `S7_probe_the_target`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 475 against a baseline of 475
- Kills: 3 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_drive_ejected_mid_queue_is_not_settled_as_a_queue_of_deletions`
  - `tests/test_deletion.py::test_a_file_in_a_volume_nested_under_the_rules_target_is_not_moved`
  - `tests/test_write_session.py::test_the_file_is_proved_where_the_file_is_and_not_where_the_rule_points`

Old text:

```
        rules[index],
        Path(path).parent,
```

New text:

```
        rules[index],
        Path(rules[index].target or "/"),
```

### `r44-a.S8_wording_held_to`

Say the volume was recorded on the rule when the identity compared was the library's

- File: `src/cratekit/core/session.py`
- Source: `r44-a.json`, row `S8_wording_held_to`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 475 against a baseline of 475
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_foreign_volume_under_a_rule_that_recorded_nothing_offers_nothing_to_record`

Old text:

```
    return "the library's volume, which a target inside the library root is held to"
```

New text:

```
    return "the volume recorded on that rule"
```

### `r44-a.S9_offer_to_record_nested`

Offer to record the foreign volume's identity on a rule that recorded none

- File: `src/cratekit/core/session.py`
- Source: `r44-a.json`, row `S9_offer_to_record_nested`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 475 against a baseline of 475
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_foreign_volume_under_a_rule_that_recorded_nothing_offers_nothing_to_record`

Old text:

```
        if rule.volume_id and observed:
```

New text:

```
        if observed:
```

### `u71-b.B10_occupied_at_move`

Drop the occupied check at the move, so os.replace can take a file's place

- File: `src/cratekit/intake/landing.py`
- Source: `u71-b.json`, row `B10_occupied_at_move`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 2 (killed)
- Killed:
  - `tests/test_landing.py::test_a_file_arriving_between_the_passes_is_not_replaced`
  - `tests/test_landing.py::test_every_file_taken_at_the_move_writes_no_intake_file`

Old text:

```
        occupied = _occupied(item, final)
```

New text:

```
        occupied = None
```

### `u71-b.B11_nothing_moved`

Drop the refusal after the move loop when nothing moved

- File: `src/cratekit/intake/landing.py`
- Source: `u71-b.json`, row `B11_nothing_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_every_file_taken_at_the_move_writes_no_intake_file`

Old text:

```
    if not moved:
        if made:
```

New text:

```
    if False:
        if made:
```

### `u71-b.B12_take_back_folder`

Keep the batch folder this call made when the first move fails

- File: `src/cratekit/intake/landing.py`
- Source: `u71-b.json`, row `B12_take_back_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_a_first_move_that_fails_leaves_no_batch_folder`

Old text:

```
            if made and not moved:
                _remove_if_empty(target)

```

New text:

```
(empty)
```

### `u71-b.B13_unlink_destination`

Leave the intake file behind when place_files fails after writing it

- File: `src/cratekit/intake/landing.py`
- Source: `u71-b.json`, row `B13_unlink_destination`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        destination.unlink(missing_ok=True)

```

New text:

```
(empty)
```

### `u71-b.B1_target_under_staging`

Drop the refusal of a landing target under download staging

- File: `src/cratekit/intake/landing.py`
- Source: `u71-b.json`, row `B1_target_under_staging`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_a_landing_target_under_staging_is_refused`

Old text:

```
    if resolved == staging or staging in resolved.parents:
```

New text:

```
    if False:
```

### `u71-b.B2_device`

Drop the cross device refusal, so a move across devices is attempted

- File: `src/cratekit/intake/landing.py`
- Source: `u71-b.json`, row `B2_device`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_a_staging_folder_on_another_device_is_refused_by_name`

Old text:

```
    if here is None or there is None or here != there:
```

New text:

```
    if False:
```

### `u71-b.B3_destination_exists`

Drop the refusal of an intake file that already exists

- File: `src/cratekit/intake/landing.py`
- Source: `u71-b.json`, row `B3_destination_exists`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_an_existing_intake_file_is_never_overwritten`

Old text:

```
    if destination.exists():
```

New text:

```
    if False:
```

### `u71-b.B4_export_missing`

Drop the missing export refusal before any move

- File: `src/cratekit/intake/landing.py`
- Source: `u71-b.json`, row `B4_export_missing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_a_missing_export_is_refused_before_any_move`

Old text:

```
    if not export.is_file():
```

New text:

```
    if False:
```

### `u71-b.B5_trial_splice`

Drop the trial splice on a copy, so a stub is met only after the moves

- File: `src/cratekit/intake/landing.py`
- Source: `u71-b.json`, row `B5_trial_splice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_a_stub_export_is_refused_before_any_move`

Old text:

```
    collection_xml.splice_tracks(trial, [])

```

New text:

```
(empty)
```

### `u71-b.B6_trial_playlist`

Drop the refusal of an export whose intake playlist cannot be written

- File: `src/cratekit/intake/landing.py`
- Source: `u71-b.json`, row `B6_trial_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_an_export_with_no_intake_folder_is_refused_before_any_move`

Old text:

```
    if error:
```

New text:

```
    if False:
```

### `u71-c.C1_nothing_movable_rerun`

Drop the refusal before the batch folder is made when nothing can move

- File: `src/cratekit/intake/landing.py`
- Source: `u71-c.json`, row `C1_nothing_movable_rerun`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_a_batch_where_nothing_lands_leaves_no_batch_folder`

Old text:

```
    if not movable:
```

New text:

```
    if False:
```

### `u71.A10_root_absent`

Drop the refusal of an absent library root before the device probe

- File: `src/cratekit/intake/landing.py`
- Source: `u71.json`, row `A10_root_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_an_absent_library_root_is_refused_before_the_device_probe`

Old text:

```
    if not root.is_dir():
```

New text:

```
    if False:
```

### `u71.A11_owned_folder`

Drop the refusal of a source folder the library already owns

- File: `src/cratekit/intake/landing.py`
- Source: `u71.json`, row `A11_owned_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_a_folder_the_library_already_owns_is_refused`

Old text:

```
    if not in_staging and (source == owned or owned in source.parents):
```

New text:

```
    if False:
```

### `u71.A12_staging_inside_library`

Drop the exemption for staging configured inside the library root

- File: `src/cratekit/intake/landing.py`
- Source: `u71.json`, row `A12_staging_inside_library`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 2 (killed)
- Killed:
  - `tests/test_landing.py::test_a_landing_target_under_staging_is_refused`
  - `tests/test_landing.py::test_staging_configured_inside_the_library_still_lands`

Old text:

```
    in_staging = source == staging or staging in source.parents
```

New text:

```
    in_staging = False
```

### `u71.A1_listing_dotfile`

Drop the dotfile skip in the listing, so a hidden file is planned

- File: `src/cratekit/intake/landing.py`
- Source: `u71.json`, row `A1_listing_dotfile`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_the_listing_is_flat_audio_only_and_skips_dotfiles`

Old text:

```
    if name.startswith(".") or name == ACQUIRE_STAGING_DIRNAME:
```

New text:

```
    if name == ACQUIRE_STAGING_DIRNAME:
```

### `u71.A2_listing_suffix`

Drop the audio suffix filter, so a text file is planned and moved

- File: `src/cratekit/intake/landing.py`
- Source: `u71.json`, row `A2_listing_suffix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 2 (killed)
- Killed:
  - `tests/test_landing.py::test_an_empty_folder_is_refused_at_plan`
  - `tests/test_landing.py::test_the_listing_is_flat_audio_only_and_skips_dotfiles`

Old text:

```
    if entry.suffix.lower() not in AUDIO_EXTS:
```

New text:

```
    if False:
```

### `u71.A3_listing_regular_file`

Drop the regular file check, so a directory named like audio is planned

- File: `src/cratekit/intake/landing.py`
- Source: `u71.json`, row `A3_listing_regular_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_a_directory_named_like_audio_is_not_listed`

Old text:

```
    return entry.is_file() and not entry.is_symlink()
```

New text:

```
    return not entry.is_symlink()
```

### `u71.A4_digest_names_only`

Fingerprint names alone, so a file replaced under its name is not stale

- File: `src/cratekit/intake/landing.py`
- Source: `u71.json`, row `A4_digest_names_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 2 (killed)
- Killed:
  - `tests/test_landing.py::test_a_file_replaced_under_the_same_name_makes_the_plan_stale`
  - `tests/test_landing.py::test_a_touched_file_of_the_same_size_makes_the_plan_stale`

Old text:

```
        hasher.update(f"{item.name}\0{stat.st_size}\0{stat.st_mtime_ns}\n".encode())
```

New text:

```
        hasher.update(f"{item.name}\n".encode())
```

### `u71.A5_digest_no_mtime`

Drop the modification time from the fingerprint, keeping name and size

- File: `src/cratekit/intake/landing.py`
- Source: `u71.json`, row `A5_digest_no_mtime`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 2 (killed)
- Killed:
  - `tests/test_landing.py::test_a_file_replaced_under_the_same_name_makes_the_plan_stale`
  - `tests/test_landing.py::test_a_touched_file_of_the_same_size_makes_the_plan_stale`

Old text:

```
        hasher.update(f"{item.name}\0{stat.st_size}\0{stat.st_mtime_ns}\n".encode())
```

New text:

```
        hasher.update(f"{item.name}\0{stat.st_size}\n".encode())
```

### `u71.A6_stale_refusal`

Drop the stale plan refusal whole

- File: `src/cratekit/intake/landing.py`
- Source: `u71.json`, row `A6_stale_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 3 (killed)
- Killed:
  - `tests/test_landing.py::test_a_file_replaced_under_the_same_name_makes_the_plan_stale`
  - `tests/test_landing.py::test_a_touched_file_of_the_same_size_makes_the_plan_stale`
  - `tests/test_landing.py::test_an_added_file_makes_the_plan_stale`

Old text:

```
    if items != plan.items or _digest(items) != plan.digest:
```

New text:

```
    if False:
```

### `u71.A7_stale_listing_only`

Compare the relisting by path only, dropping the digest half

- File: `src/cratekit/intake/landing.py`
- Source: `u71.json`, row `A7_stale_listing_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 2 (killed)
- Killed:
  - `tests/test_landing.py::test_a_file_replaced_under_the_same_name_makes_the_plan_stale`
  - `tests/test_landing.py::test_a_touched_file_of_the_same_size_makes_the_plan_stale`

Old text:

```
    if items != plan.items or _digest(items) != plan.digest:
```

New text:

```
    if items != plan.items:
```

### `u71.A9_plan_empty`

Drop the refusal of a folder with nothing to land

- File: `src/cratekit/intake/landing.py`
- Source: `u71.json`, row `A9_plan_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_an_empty_folder_is_refused_at_plan`

Old text:

```
    if not items:
```

New text:

```
    if False:
```

### `r375-a.S10_commit_not_persisted_at_once`

record_commit: mark the source in memory and leave the write to the close, so a hard kill after the commit leaves a record that claims none

- File: `src/cratekit/core/session.py`
- Source: `r375-a.json`, row `S10_commit_not_persisted_at_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`, `tests/test_restore.py`
- Collected: 394 against a baseline of 394
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_recorded_commit_is_on_disk_before_the_session_ends`

Old text:

```
    record.sources[source] = str(SourceState.COMMITTED)
    record.change = record.change.merged(change)
    write_record(record, cfg)
```

New text:

```
    record.sources[source] = str(SourceState.COMMITTED)
    record.change = record.change.merged(change)
```

### `r375-a.S11_commit_replaces_the_summary`

record_commit: replace the change summary instead of merging into it, so a second source erases the first one's counts

- File: `src/cratekit/core/session.py`
- Source: `r375-a.json`, row `S11_commit_replaces_the_summary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`, `tests/test_restore.py`
- Collected: 394 against a baseline of 394
- Kills: 2 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_recorded_commit_is_on_disk_before_the_session_ends`
  - `tests/test_write_session.py::test_a_resume_skips_a_committed_source_and_finishes_the_rest`

Old text:

```
    record.sources[source] = str(SourceState.COMMITTED)
    record.change = record.change.merged(change)
```

New text:

```
    record.sources[source] = str(SourceState.COMMITTED)
    record.change = change
```

### `r375-a.S1_keep_is_ignored`

assert_gates: keep a record for nobody, so Keep.RECORD yields Gates.record None

- File: `src/cratekit/core/session.py`
- Source: `r375-a.json`, row `S1_keep_is_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`, `tests/test_restore.py`
- Collected: 394 against a baseline of 394
- Kills: 38 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_a_library_with_no_tag_category_refuses_through_the_verb`
  - `tests/test_metadata_cli.py::test_a_second_apply_is_idempotent`
  - `tests/test_metadata_cli.py::test_a_second_apply_writes_nothing_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_apply_is_listed_by_restore_list_as_a_restorable_session`
  - `tests/test_metadata_cli.py::test_an_apply_that_refuses_mid_write_is_abandoned_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_apply_whose_commit_lands_and_then_raises_is_recorded_as_committed`
  - `tests/test_metadata_cli.py::test_apply_writes_my_tags_and_does_not_write_a_content_column`
  - `tests/test_metadata_cli.py::test_the_capture_is_protected_while_the_apply_is_in_flight`
  - `tests/test_restore.py::test_a_restore_the_analysis_watch_refuses_is_not_on_record_as_finished`
  - `tests/test_restore.py::test_the_recovery_session_closes_its_own_record_on_both_paths`
  - `tests/test_tree_writer.py::test_a_capture_that_did_not_verify_is_recorded_before_the_refusal`
  - `tests/test_tree_writer.py::test_a_commit_that_lands_and_then_raises_is_still_recorded_as_committed`
  - `tests/test_tree_writer.py::test_a_failure_after_the_commit_still_reads_as_committed_work`
  - `tests/test_tree_writer.py::test_a_failure_mid_loop_leaves_nothing_pending_on_the_handle`
  - `tests/test_tree_writer.py::test_a_grid_rewritten_during_a_membership_write_refuses_the_session`
  - ... and 23 more, see the JSON sidecar

Old text:

```
            if keep is Keep.RECORD
            else nullcontext()
```

New text:

```
            if keep is Keep.NOTHING
            else nullcontext()
```

### `r375-a.S2_record_inside_the_watch`

assert_gates: open the record INSIDE the analysis watch, the ordering fault the review found, so it closes CLOSED before the watch judges

- File: `src/cratekit/core/session.py`
- Source: `r375-a.json`, row `S2_record_inside_the_watch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`, `tests/test_restore.py`
- Collected: 394 against a baseline of 394
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore.py::test_a_restore_the_analysis_watch_refuses_is_not_on_record_as_finished`
  - `tests/test_tree_writer.py::test_a_grid_rewritten_during_a_membership_write_refuses_the_session`
  - `tests/test_write_session.py::test_the_record_closes_after_the_analysis_watch_has_judged_the_session`

Old text:

```
        with keeping as record:
            with analysis_files_unmoved(watched) if watched else nullcontext():
                yield Gates(
```

New text:

```
        with analysis_files_unmoved(watched) if watched else nullcontext():
            with keeping as record:
                yield Gates(
```

### `r375-a.S3_a_raise_is_not_abandoned`

_recorded: drop the abandoning close, so a body that raised leaves its record OPEN

- File: `src/cratekit/core/session.py`
- Source: `r375-a.json`, row `S3_a_raise_is_not_abandoned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`, `tests/test_restore.py`
- Collected: 394 against a baseline of 394
- Kills: 13 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_an_apply_that_refuses_mid_write_is_abandoned_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_apply_whose_commit_lands_and_then_raises_is_recorded_as_committed`
  - `tests/test_restore.py::test_a_restore_the_analysis_watch_refuses_is_not_on_record_as_finished`
  - `tests/test_restore.py::test_the_recovery_session_closes_its_own_record_on_both_paths`
  - `tests/test_tree_writer.py::test_a_capture_that_did_not_verify_is_recorded_before_the_refusal`
  - `tests/test_tree_writer.py::test_a_commit_that_lands_and_then_raises_is_still_recorded_as_committed`
  - `tests/test_tree_writer.py::test_a_failure_after_the_commit_still_reads_as_committed_work`
  - `tests/test_tree_writer.py::test_a_grid_rewritten_during_a_membership_write_refuses_the_session`
  - `tests/test_tree_writer.py::test_a_membership_write_that_fails_is_abandoned_and_claims_no_commit`
  - `tests/test_tree_writer.py::test_a_write_that_fails_after_counting_a_membership_still_claims_no_commit`
  - `tests/test_write_session.py::test_a_body_that_raises_closes_abandoned_and_its_own_error_surfaces`
  - `tests/test_write_session.py::test_a_clean_close_that_refuses_ends_abandoned_rather_than_open`
  - `tests/test_write_session.py::test_the_record_closes_after_the_analysis_watch_has_judged_the_session`

Old text:

```
            close_session(record, cfg, state=SessionState.ABANDONED, now=now)
        except Exception:  # noqa: BLE001 - the session's own error is the one to surface
```

New text:

```
            pass
        except Exception:  # noqa: BLE001 - the session's own error is the one to surface
```

### `r375-a.S4_abandon_failure_replaces_the_error`

_recorded: re-raise a failed abandonment instead of logging it, so it replaces the error that ended the session

- File: `src/cratekit/core/session.py`
- Source: `r375-a.json`, row `S4_abandon_failure_replaces_the_error`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`, `tests/test_restore.py`
- Collected: 394 against a baseline of 394
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_log_that_cannot_record_the_abandonment_does_not_replace_the_error`

Old text:

```
            logger.warning(
                "session %s could not be recorded as abandoned", record.session_id, exc_info=True
            )
        raise
```

New text:

```
            raise
        raise
```

### `r375-a.S5_clean_close_refusal_leaves_it_open`

_recorded: move the clean close out of the try, so a close that refuses leaves the record OPEN with no verb to abandon it

- File: `src/cratekit/core/session.py`
- Source: `r375-a.json`, row `S5_clean_close_refusal_leaves_it_open`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`, `tests/test_restore.py`
- Collected: 394 against a baseline of 394
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_clean_close_that_refuses_ends_abandoned_rather_than_open`

Old text:

```
    try:
        yield record
        close_session(
            record,
            cfg,
            state=SessionState.CLOSED,
            intent=intent,
            identity_provider=identity_provider,
            mount_enumerator=mount_enumerator,
            now=now,
        )
    except BaseException:
        try:
            close_session(record, cfg, state=SessionState.ABANDONED, now=now)
        except Exception:  # noqa: BLE001 - the session's own error is the one to surface
            logger.warning(
                "session %s could not be recorded as abandoned", record.session_id, exc_info=True
            )
        raise

```

New text:

```
    try:
        yield record
    except BaseException:
        try:
            close_session(record, cfg, state=SessionState.ABANDONED, now=now)
        except Exception:  # noqa: BLE001 - the session's own error is the one to surface
            logger.warning(
                "session %s could not be recorded as abandoned", record.session_id, exc_info=True
            )
        raise
    close_session(
        record,
        cfg,
        state=SessionState.CLOSED,
        intent=intent,
        identity_provider=identity_provider,
        mount_enumerator=mount_enumerator,
        now=now,
    )

```

### `r375-a.S6_close_ignores_the_intent`

_recorded: close every record as an ordinary WRITE, so a recovery's close is gated by the latch it is the remedy for

- File: `src/cratekit/core/session.py`
- Source: `r375-a.json`, row `S6_close_ignores_the_intent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`, `tests/test_restore.py`
- Collected: 394 against a baseline of 394
- Kills: 11 (killed)
- Killed:
  - `tests/test_restore.py::test_a_coupled_file_the_capture_records_as_absent_is_removed_again`
  - `tests/test_restore.py::test_a_recovery_is_not_refused_by_the_latch_whose_remedy_it_is`
  - `tests/test_restore.py::test_a_rehearsal_reports_what_is_outstanding_rather_than_what_it_recorded`
  - `tests/test_restore.py::test_a_restore_returns_the_coupled_state_with_the_database`
  - `tests/test_restore.py::test_blocking_2_a_failure_mid_restore_is_a_structured_refusal`
  - `tests/test_restore.py::test_blocking_5_an_interrupted_restore_in_a_none_effect_window_latches`
  - `tests/test_restore.py::test_round2_a_completed_restore_discharges_an_earlier_interrupted_one`
  - `tests/test_restore.py::test_round2_repeating_a_failing_restore_does_not_accumulate_latches`
  - `tests/test_restore.py::test_round2_three_attempts_stage_their_logs_side_by_side`
  - `tests/test_restore.py::test_round6_the_performing_backstop_names_what_it_already_moved`
  - `tests/test_write_session.py::test_a_recovery_closes_as_a_recovery`

Old text:

```
            state=SessionState.CLOSED,
            intent=intent,
            identity_provider=identity_provider,
```

New text:

```
            state=SessionState.CLOSED,
            intent=Intent.WRITE,
            identity_provider=identity_provider,
```

### `r375-a.S7_close_drops_the_identity_seam`

_recorded: do not forward the identity provider to the gated close, so it asserts the volume through this machine's default

- File: `src/cratekit/core/session.py`
- Source: `r375-a.json`, row `S7_close_drops_the_identity_seam`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`, `tests/test_restore.py`
- Collected: 394 against a baseline of 394
- Kills: 4 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_recorded_commit_is_on_disk_before_the_session_ends`
  - `tests/test_write_session.py::test_a_supplied_holder_reaches_the_record_as_well_as_the_lock`
  - `tests/test_write_session.py::test_the_record_is_the_gates_own_workflow_actor_and_acknowledgment`
  - `tests/test_write_session.py::test_the_record_names_the_holder_the_lock_names`

Old text:

```
            intent=intent,
            identity_provider=identity_provider,
            mount_enumerator=mount_enumerator,
            now=now,
        )
    except BaseException:
```

New text:

```
            intent=intent,
            mount_enumerator=mount_enumerator,
            now=now,
        )
    except BaseException:
```

### `r375-a.S8_record_names_no_actor`

_recorded: record no actor, so the log cannot say who acknowledged the backup this write ran behind

- File: `src/cratekit/core/session.py`
- Source: `r375-a.json`, row `S8_record_names_no_actor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`, `tests/test_restore.py`
- Collected: 394 against a baseline of 394
- Kills: 2 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_a_membership_write_is_listed_as_restorable_with_its_per_tree_counts`
  - `tests/test_write_session.py::test_the_record_is_the_gates_own_workflow_actor_and_acknowledgment`

Old text:

```
        actor=acknowledgment.actor,
```

New text:

```
        actor=None,
```

### `r375-a.S9_record_names_no_acknowledgment`

_recorded: record no acknowledgment instant

- File: `src/cratekit/core/session.py`
- Source: `r375-a.json`, row `S9_record_names_no_acknowledgment`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`, `tests/test_restore.py`
- Collected: 394 against a baseline of 394
- Kills: 2 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_a_membership_write_is_listed_as_restorable_with_its_per_tree_counts`
  - `tests/test_write_session.py::test_the_record_is_the_gates_own_workflow_actor_and_acknowledgment`

Old text:

```
        acknowledged_at=acknowledgment.recorded_at.isoformat(),
```

New text:

```
        acknowledged_at=None,
```

### `r83.D1_offer_defect`

R-348: acquire_one no longer asks the defect question after a failed offer

- File: `src/cratekit/acquire/adapter.py`
- Source: `r83.json`, row `D1_offer_defect`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_doctor.py`, `tests/test_pacing.py`
- Collected: 755 against a baseline of 755
- Kills: 8 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[streamrip-AttributeError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[streamrip-NameError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[streamrip-TypeError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[streamrip-UnboundLocalError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[vendored-AttributeError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[vendored-NameError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[vendored-TypeError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[vendored-UnboundLocalError]`

Old text:

```
    except Exception as exc:  # noqa: BLE001 - one dead track never sinks the run
        raise_if_defect(exc)

```

New text:

```
    except Exception as exc:  # noqa: BLE001 - one dead track never sinks the run

```

### `r83.D2_fetch_defect`

R-348: acquire_one no longer asks the defect question after a failed fetch

- File: `src/cratekit/acquire/adapter.py`
- Source: `r83.json`, row `D2_fetch_defect`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_doctor.py`, `tests/test_pacing.py`
- Collected: 755 against a baseline of 755
- Kills: 2 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_download_breaks_the_adapter_the_same_way`
  - `tests/test_adapter_contract.py::test_a_defect_stops_the_paced_pool_rather_than_being_retried`

Old text:

```
    except Exception as exc:  # noqa: BLE001 - same rule as the lookup above
        raise_if_defect(exc)

```

New text:

```
    except Exception as exc:  # noqa: BLE001 - same rule as the lookup above

```

### `r83.D3_drop_attribute_error`

R-348: AttributeError leaves the defect classes, the class the sitting found

- File: `src/cratekit/acquire/adapter.py`
- Source: `r83.json`, row `D3_drop_attribute_error`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_doctor.py`, `tests/test_pacing.py`
- Collected: 755 against a baseline of 755
- Kills: 6 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_download_breaks_the_adapter_the_same_way`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[streamrip-AttributeError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[vendored-AttributeError]`
  - `tests/test_adapter_contract.py::test_a_defect_stops_the_paced_pool_rather_than_being_retried`
  - `tests/test_adapter_contract.py::test_a_defect_the_tool_swallowed_breaks_the_adapter`
  - `tests/test_adapter_contract.py::test_the_vendored_source_reads_a_defect_naming_a_token_as_a_defect`

Old text:

```
DEFECT_ERRORS: tuple[type[BaseException], ...] = (AttributeError, TypeError, NameError)
```

New text:

```
DEFECT_ERRORS: tuple[type[BaseException], ...] = (TypeError, NameError)
```

### `r83.D4_drop_type_error`

R-348: TypeError leaves the defect classes

- File: `src/cratekit/acquire/adapter.py`
- Source: `r83.json`, row `D4_drop_type_error`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_doctor.py`, `tests/test_pacing.py`
- Collected: 755 against a baseline of 755
- Kills: 2 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[streamrip-TypeError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[vendored-TypeError]`

Old text:

```
DEFECT_ERRORS: tuple[type[BaseException], ...] = (AttributeError, TypeError, NameError)
```

New text:

```
DEFECT_ERRORS: tuple[type[BaseException], ...] = (AttributeError, NameError)
```

### `r83.D5_drop_name_error`

R-348: NameError, and with it UnboundLocalError, leaves the defect classes

- File: `src/cratekit/acquire/adapter.py`
- Source: `r83.json`, row `D5_drop_name_error`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_doctor.py`, `tests/test_pacing.py`
- Collected: 755 against a baseline of 755
- Kills: 4 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[streamrip-NameError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[streamrip-UnboundLocalError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[vendored-NameError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[vendored-UnboundLocalError]`

Old text:

```
DEFECT_ERRORS: tuple[type[BaseException], ...] = (AttributeError, TypeError, NameError)
```

New text:

```
DEFECT_ERRORS: tuple[type[BaseException], ...] = (AttributeError, TypeError)
```

### `r83.D6_remedy`

R-348: the defect carries switch-adapter instead of report-defect

- File: `src/cratekit/acquire/adapter.py`
- Source: `r83.json`, row `D6_remedy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_doctor.py`, `tests/test_pacing.py`
- Collected: 755 against a baseline of 755
- Kills: 11 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_download_breaks_the_adapter_the_same_way`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[streamrip-AttributeError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[streamrip-NameError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[streamrip-TypeError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[streamrip-UnboundLocalError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[vendored-AttributeError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[vendored-NameError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[vendored-TypeError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[vendored-UnboundLocalError]`
  - `tests/test_adapter_contract.py::test_a_defect_stops_the_paced_pool_rather_than_being_retried`
  - `tests/test_adapter_contract.py::test_the_vendored_source_reads_a_defect_naming_a_token_as_a_defect`

Old text:

```
            remedy=Remedy.REPORT_DEFECT,
        ) from exc
```

New text:

```
            remedy=Remedy.SWITCH_ADAPTER,
        ) from exc
```

### `r83.D7_detail_names_class`

R-348: the detail no longer names the exception class

- File: `src/cratekit/acquire/adapter.py`
- Source: `r83.json`, row `D7_detail_names_class`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_doctor.py`, `tests/test_pacing.py`
- Collected: 755 against a baseline of 755
- Kills: 9 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[streamrip-AttributeError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[streamrip-NameError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[streamrip-TypeError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[streamrip-UnboundLocalError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[vendored-AttributeError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[vendored-NameError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[vendored-TypeError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[vendored-UnboundLocalError]`
  - `tests/test_adapter_contract.py::test_a_defect_the_tool_swallowed_breaks_the_adapter`

Old text:

```
            f"({type(exc).__name__}: {exc})",
```

New text:

```
            f"({exc})",
```

### `u274.P1_gone_never`

_gone: read a process that is gone as alive, so a hard killed drive's token directory is never swept

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u274.json`, row `P1_gone_never`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 449 against a baseline of 449
- Kills: 1 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_drive_killed_outright_leaves_a_directory_the_next_one_sweeps`

Old text:

```
    except ProcessLookupError:
        return True

```

New text:

```
    except ProcessLookupError:
        return False

```

### `u274.P2_gone_overflow`

_gone: let OverflowError and ValueError escape, so a directory named for an impossible process id fails every materialise

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u274.json`, row `P2_gone_overflow`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 449 against a baseline of 449
- Kills: 1 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_process_id_no_process_can_have_is_left_and_does_not_raise`

Old text:

```
    except (OSError, OverflowError, ValueError):

```

New text:

```
    except OSError:

```

### `u274.P3_gone_permission`

_gone: read another account's process (a permission refusal) as gone, so its live directory is swept

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u274.json`, row `P3_gone_permission`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 449 against a baseline of 449
- Kills: 2 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_process_id_no_process_can_have_is_left_and_does_not_raise`
  - `tests/test_vendored_drive.py::test_the_sweep_leaves_a_directory_whose_process_it_cannot_see`

Old text:

```
    except (OSError, OverflowError, ValueError):
        # Another account's process, or an id no process can have, which only
        # a directory someone else named could carry: never proven gone.
        return False

```

New text:

```
    except (OSError, OverflowError, ValueError):
        # Another account's process, or an id no process can have, which only
        # a directory someone else named could carry: never proven gone.
        return True

```

### `u274.P4_sweep_live`

sweep_orphans: drop the process check, so every directory of the form is removed, a live drive's token included

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u274.json`, row `P4_sweep_live`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 449 against a baseline of 449
- Kills: 4 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_drive_killed_outright_leaves_a_directory_the_next_one_sweeps`
  - `tests/test_vendored_drive.py::test_a_process_id_no_process_can_have_is_left_and_does_not_raise`
  - `tests/test_vendored_drive.py::test_the_sweep_leaves_a_directory_whose_process_it_cannot_see`
  - `tests/test_vendored_drive.py::test_the_sweep_leaves_alone_what_it_cannot_prove_is_an_orphan[own-process]`

Old text:

```
        if owned is None or not _gone(int(owned.group(1))):

```

New text:

```
        if owned is None:

```

### `u274.P5_sweep_not_dir`

sweep_orphans: drop the directory check, so a file or a link of the name is reported removed

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u274.json`, row `P5_sweep_not_dir`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 449 against a baseline of 449
- Kills: 2 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_the_sweep_reports_only_what_it_removed[file]`
  - `tests/test_vendored_drive.py::test_the_sweep_reports_only_what_it_removed[symlink]`

Old text:

```
        if not stat.S_ISDIR(info.st_mode) or info.st_uid != account:

```

New text:

```
        if info.st_uid != account:

```

### `u274.P6_sweep_other_account`

sweep_orphans: drop the owner check, so another account's directory is removed

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u274.json`, row `P6_sweep_other_account`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 449 against a baseline of 449
- Kills: 1 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_the_sweep_leaves_another_accounts_directory_alone`

Old text:

```
        if not stat.S_ISDIR(info.st_mode) or info.st_uid != account:

```

New text:

```
        if not stat.S_ISDIR(info.st_mode):

```

### `u274.P7_no_sweep`

materialised_session: never sweep, so a hard killed drive's token file stays in the temporary directory

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u274.json`, row `P7_no_sweep`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 449 against a baseline of 449
- Kills: 1 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_drive_killed_outright_leaves_a_directory_the_next_one_sweeps`

Old text:

```
    sweep_orphans()
    # mkdtemp
```

New text:

```
    # mkdtemp
```

### `u274.P8_captured_always`

captured: take every field the client holds, so a float expiry read back from an int one writes the keychain on every drive

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u274.json`, row `P8_captured_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 449 against a baseline of 449
- Kills: 3 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_drive_reads_the_keychain_as_a_one_track_drive_does_and_writes_nothing`
  - `tests/test_vendored_drive.py::test_a_session_withdrawn_mid_drive_parks_and_a_resume_lands_the_rest`
  - `tests/test_vendored_drive.py::test_an_unchanged_session_needs_no_keychain_write_at_all`

Old text:

```
        if value != stored.get(name):
            refreshed[name] = value

```

New text:

```
        refreshed[name] = value

```

### `u274.P9_captured_nothing`

captured: take no field, so a token the provider refreshed during the drive never reaches the keychain

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u274.json`, row `P9_captured_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 449 against a baseline of 449
- Kills: 6 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_refresh_before_a_withdrawal_still_reaches_the_keychain`
  - `tests/test_vendored_drive.py::test_a_refresh_in_a_drive_where_every_item_failed_still_reaches_the_keychain`
  - `tests/test_vendored_drive.py::test_a_refresh_the_keychain_cannot_take_is_a_warning_on_a_finished_download`
  - `tests/test_vendored_drive.py::test_a_token_file_that_cannot_be_written_at_the_close_is_a_warning`
  - `tests/test_vendored_drive.py::test_a_token_refreshed_during_the_drive_is_stored_once`
  - `tests/test_vendored_drive.py::test_an_index_that_refuses_after_the_keychain_took_the_session_is_a_warning`

Old text:

```
        if value != stored.get(name):
            refreshed[name] = value

```

New text:

```
        if False:
            refreshed[name] = value

```

### `u274.C1_worker_names_no_drive`

acquire.cli: the download worker names no per drive holder, so a download logs in once a track

- File: `src/cratekit/acquire/cli.py`
- Source: `u274.json`, row `C1_worker_names_no_drive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 449 against a baseline of 449
- Kills: 17 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_broken_item_fails_alone_and_the_job_stays_resumable`
  - `tests/test_vendored_drive.py::test_a_defect_at_the_close_of_a_finished_drive_is_raised`
  - `tests/test_vendored_drive.py::test_a_drive_reads_the_keychain_as_a_one_track_drive_does_and_writes_nothing`
  - `tests/test_vendored_drive.py::test_a_drive_signalled_mid_track_leaves_no_token_file`
  - `tests/test_vendored_drive.py::test_a_drive_torn_down_mid_track_leaves_no_token_file`
  - `tests/test_vendored_drive.py::test_a_refresh_before_a_withdrawal_still_reaches_the_keychain`
  - `tests/test_vendored_drive.py::test_a_refresh_in_a_drive_where_every_item_failed_still_reaches_the_keychain`
  - `tests/test_vendored_drive.py::test_a_refresh_the_keychain_cannot_take_is_a_warning_on_a_finished_download`
  - `tests/test_vendored_drive.py::test_a_session_withdrawn_mid_drive_parks_and_a_resume_lands_the_rest`
  - `tests/test_vendored_drive.py::test_a_ten_track_job_logs_in_once_and_spends_four_calls_a_track`
  - `tests/test_vendored_drive.py::test_a_token_file_that_cannot_be_written_at_the_close_is_a_warning`
  - `tests/test_vendored_drive.py::test_a_token_refreshed_during_the_drive_is_stored_once`
  - `tests/test_vendored_drive.py::test_an_index_that_refuses_after_the_keychain_took_the_session_is_a_warning`
  - `tests/test_vendored_drive.py::test_every_call_of_the_drive_goes_through_the_gate`
  - `tests/test_vendored_drive.py::test_the_download_worker_names_the_vendored_drive`
  - ... and 2 more, see the JSON sidecar

Old text:

```
handle.per_drive = vendored.drive  # type: ignore[attr-defined]

```

New text:

```
(empty)
```

### `u102-a.P1_root_boundary`

_under: match the root as a bare prefix, without the separator, so a sibling folder sharing the prefix is inside it

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `P1_root_boundary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_root_that_only_shares_a_prefix_is_not_the_folder`

Old text:

```
    return held == wanted or held.startswith(wanted + "/")
```

New text:

```
    return held == wanted or held.startswith(wanted)
```

### `u102-a.P2_root_casefold`

_key: compare the root exactly instead of casefolded

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `P2_root_casefold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_root_typed_in_another_case_still_names_the_folder`

Old text:

```
    return locations.norm_for_compare(path).casefold()
```

New text:

```
    return locations.norm_for_compare(path)
```

### `u102-a.P3_root_filter`

_plan_for: ignore the root, so an accepted item outside it is applied

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `P3_root_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_root_limits_the_apply_and_counts_what_it_left_out`
  - `tests/intake/test_repair_apply.py::test_a_root_that_only_shares_a_prefix_is_not_the_folder`

Old text:

```
        if accepted.path is not None and not _under(accepted.path, root):
```

New text:

```
        if False:
```

### `u102-a.P4_unchanged`

_plan_for: stop setting aside a proposal that names the file's own name, so it is planned as a rename

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `P4_unchanged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_proposal_that_asked_for_no_change_is_listed_with_its_reason`

Old text:

```
        if path.name == accepted.proposed:
```

New text:

```
        if False:
```

