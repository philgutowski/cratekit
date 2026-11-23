# Mutation table: u325-after-l-14

Measured by `scripts/mutate.py` on 2026-11-22 22:23 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 130.

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
| `u102-a.P5_missing` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 2 | killed |
| `u102-a.P6_missing_says_what_exists` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `u102-a.U1_no_stored_path` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `u102-a.U2_bare_filename` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 2 | killed |
| `u102-a.U3_empty_name` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `u102-a.U4_same_suffix` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `u102-a.U5_linked_file` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `u102-b.G1_plan_referenced` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `u102-b.G2_post_gate_referenced` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `u102-b.G4_plan_collisions` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 2 | killed |
| `u102-b.G5_claim` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 2 | killed |
| `u102-b.G6_abort` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 2 | killed |
| `u102-b.G7_referenced_is_owed` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `u102-b.G8_collision_is_owed` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 2 | killed |
| `u102-b.G9_post_gate_missing` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `u102-b.R1_retryable_seed` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 2 | killed |
| `u102-b.R2_retryable_after_gate` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `u102-b.S1_stub_removed` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 2 | killed |
| `u126.F1_read_always` | `src/cratekit/intake/native.py` | user | 7 file(s) | 260 | 1 | killed |
| `u126.F3_counts_undigested` | `src/cratekit/intake/native.py` | user | 7 file(s) | 260 | 1 | killed |
| `u126.P1_no_read` | `src/cratekit/intake/native.py` | user | 7 file(s) | 260 | 9 | killed |
| `u126.P2_not_shown` | `src/cratekit/intake/native.py` | user | 7 file(s) | 260 | 4 | killed |
| `u126.R1_binding_value_kept` | `src/cratekit/intake/native.py` | user | 7 file(s) | 260 | 52 | killed |
| `u126.R2_fill_if_null` | `src/cratekit/intake/native.py` | user | 7 file(s) | 260 | 52 | killed |
| `u126.R3_check_skipped` | `src/cratekit/intake/native.py` | user | 7 file(s) | 260 | 2 | killed |
| `u126.R5_read_back_file_id` | `src/cratekit/intake/native.py` | user | 7 file(s) | 260 | 52 | killed |
| `u126.S1_file_id_kept` | `src/cratekit/intake/native.py` | user | 7 file(s) | 260 | 53 | killed |
| `u126.S2_defaults_left_null` | `src/cratekit/intake/native.py` | user | 7 file(s) | 260 | 1 | killed |
| `u128-b.N1_native_owned_unwritten` | `src/cratekit/intake/native.py` | user | 7 file(s) | 260 | 4 | killed |
| `u128-b.N2_native_record_no_pass` | `src/cratekit/intake/native.py` | user | 7 file(s) | 260 | 2 | killed |
| `u128-b.N4_native_dropped_left_lost` | `src/cratekit/intake/native.py` | user | 7 file(s) | 260 | 1 | killed |
| `r239-a.A1_probe_to_true` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 706 | 124 | killed |
| `r239-a.A2_probe_to_false` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 706 | 7 | killed |
| `r239-a.A3_probe_removed` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 706 | 7 | killed |
| `r239-a.A4_open_default_true` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 706 | 123 | killed |
| `r239-a.A7_needed_always_true` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 706 | 124 | killed |
| `r239-a.A8_needed_always_false` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 706 | 8 | killed |
| `r239-a.A9_header_nearby_value` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 706 | 124 | killed |
| `u145-s2.S2b_removed_member_read_live` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.C1_unplanned_membership_admitted` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 3 | killed |
| `u145.C2_unplanned_playlist_admitted` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.C3_parent_unchecked` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.C4_changed_membership_admitted` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.C5_content_unchecked` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.C6_existing_playlist_change_admitted` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.S10_unemptied_retired` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.S11_unemptied_asks_taken_back` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.S12_retirement_admits_memberships_only` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 13 | killed |
| `u145.S13_retirement_confined_to_nothing` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 13 | killed |
| `u145.S1_any_name_is_a_quarter` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 8 | killed |
| `u145.S3_last_dated_mention_wins` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.S4_account_never_asked` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.S5_job_dates_ignored` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 11 | killed |
| `u145.S6_rehearted_is_taken_back` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.S7_taken_back_placed` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.S8_stale_digest_accepted` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.S9_digest_covers_the_months_state` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.V1_gate_on_nothing` | `src/cratekit/favorites/split_cli.py` | user | 1 file(s) | 33 | 2 | killed |
| `u145.V2_no_ack` | `src/cratekit/favorites/split_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `r1677.L1_rehearsal_unmeasured` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 95 | 1 | killed |
| `r1677.L2_rehearsal_room_silent` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 95 | 1 | killed |
| `r1677.L3_rehearsal_other_failure_sound` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 95 | 1 | killed |
| `u162.L10_interrupt_cancel` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 95 | 1 | killed |
| `u162.L12_rehearsal_equal` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 95 | 1 | killed |
| `u162.L1_bridge_refusal` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 95 | 1 | killed |
| `u162.L2_area_plan_compare` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 95 | 2 | killed |
| `u162.L4_occupied_hold` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 95 | 1 | killed |
| `u162.L6_gridless_read_back` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 95 | 1 | killed |
| `u162.L7_identified_read_back` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 95 | 1 | killed |
| `u162.L8_success_witness` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 95 | 2 | killed |
| `u162.L9_kept_area_named` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 95 | 4 | killed |
| `u188.M1_stored_pair_dropped` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 95 | 3 | killed |
| `u188.M2_scratch_stored_under_the_mount` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 95 | 3 | killed |
| `u188.M3_live_stored_under_the_mount` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 95 | 3 | killed |
| `u188.M4_staging_pair_dropped` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 95 | 20 | killed |
| `u188.M6_mapped_as_lines` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 95 | 2 | killed |
| `u226.M10_settle_lag_known_only` | `src/cratekit/modules/outbound/tidal_account.py` | user | 9 file(s) | 441 | 5 | killed |
| `u226.M11_settle_kept_ignored` | `src/cratekit/modules/outbound/tidal_account.py` | user | 9 file(s) | 441 | 1 | killed |
| `u226.M13_removal_window_wrong` | `src/cratekit/modules/outbound/tidal_account.py` | user | 9 file(s) | 441 | 2 | killed |
| `u226.M15_wait_uncounted` | `src/cratekit/modules/outbound/tidal_account.py` | user | 9 file(s) | 441 | 2 | killed |
| `u226.M17_removal_positions_unsettled` | `src/cratekit/modules/outbound/tidal_account.py` | user | 9 file(s) | 441 | 3 | killed |
| `u226.M18_waited_unformatted` | `src/cratekit/modules/outbound/tidal_account.py` | maintainer | 9 file(s) | 22933 | 0 (promoted) | zero |
| `u226.M7_reading_takes_window` | `src/cratekit/modules/outbound/tidal_account.py` | user | 9 file(s) | 441 | 5 | killed |
| `u226.M8_unpaged_first` | `src/cratekit/modules/outbound/tidal_account.py` | user | 9 file(s) | 441 | 3 | killed |
| `u226.M9_positions_no_lag_refusal` | `src/cratekit/modules/outbound/tidal_account.py` | user | 9 file(s) | 441 | 5 | killed |
| `u272.C1_no_flush` | `src/cratekit/core/config.py` | user | 7 file(s) | 630 | 14 | killed |
| `u272.C2_full_flush_error_swallowed` | `src/cratekit/core/config.py` | user | 7 file(s) | 630 | 1 | killed |
| `u272.C3_full_flush_then_sync` | `src/cratekit/core/config.py` | maintainer | 7 file(s) | 630 | 1 | killed |
| `u272.C4_full_flush_never_asked` | `src/cratekit/core/config.py` | user | 7 file(s) | 630 | 5 | killed |
| `u272.C5_eio_counts_as_unsupported` | `src/cratekit/core/config.py` | user | 7 file(s) | 630 | 1 | killed |
| `u272.C6_no_plain_sync` | `src/cratekit/core/config.py` | user | 7 file(s) | 630 | 12 | killed |
| `u272.C7_error_names_no_path` | `src/cratekit/core/config.py` | user | 7 file(s) | 630 | 1 | killed |
| `r758-b.C1_gate_asked_before_the_acknowledgment` | `src/cratekit/adopt/move_cli.py` | user | 1 file(s) | 112 | 3 | killed |
| `r758-b.C3_rows_not_proven_against_the_digest` | `src/cratekit/adopt/move_cli.py` | user | 1 file(s) | 112 | 1 | killed |
| `r758-b.C5_a_sub_nobody_was_shown_is_removed` | `src/cratekit/adopt/move_cli.py` | user | 1 file(s) | 112 | 1 | killed |
| `r758-b.C6_left_target_is_added_back` | `src/cratekit/adopt/move_cli.py` | user | 1 file(s) | 112 | 1 | killed |
| `r758-b.C9_read_back_is_not_the_verdict` | `src/cratekit/adopt/move_cli.py` | user | 1 file(s) | 112 | 1 | killed |
| `r780-b.B1_reading_not_rechecked` | `src/cratekit/adopt/move_cli.py` | user | 1 file(s) | 112 | 2 | killed |
| `r780-b.B2_worker_asks_the_entry_bucket` | `src/cratekit/adopt/move_cli.py` | user | 1 file(s) | 112 | 18 | killed |
| `r780-b.B3_renamed_target_reads_as_done` | `src/cratekit/adopt/move_cli.py` | user | 1 file(s) | 112 | 1 | killed |
| `r780-b.B4_gone_named_once_per_move` | `src/cratekit/adopt/move_cli.py` | user | 1 file(s) | 112 | 1 | killed |
| `r780-b.B5_verdicts_not_handed_to_the_worker` | `src/cratekit/adopt/move_cli.py` | user | 1 file(s) | 112 | 1 | killed |
| `r758-a.T2_first_commit_admits_a_removal` | `src/cratekit/write/trees.py` | user | 1 file(s) | 112 | 1 | killed |
| `r758-a.T3_target_not_proven` | `src/cratekit/write/trees.py` | user | 1 file(s) | 112 | 1 | killed |
| `r758-a.T4_target_can_be_removed_from` | `src/cratekit/write/trees.py` | user | 1 file(s) | 112 | 1 | killed |
| `r758-a.T5_dead_track_moved` | `src/cratekit/write/trees.py` | user | 1 file(s) | 112 | 1 | killed |
| `r758-a.T6_removed_playlist_is_a_destination` | `src/cratekit/write/trees.py` | user | 1 file(s) | 112 | 2 | killed |
| `r758-b.T7_refusal_read_as_an_interruption` | `src/cratekit/write/trees.py` | user | 1 file(s) | 112 | 1 | killed |
| `u154.G10_read_back_path_unchecked` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 43 | 1 | killed |
| `u154.G11_kept_columns_unchecked` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 43 | 1 | killed |
| `u154.G14_reserved_folders_are_candidates` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 43 | 1 | killed |
| `u154.G15_stored_target_under_mounted_path` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 43 | 1 | killed |
| `u154.G17_refusal_before_rename_rewrapped` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 43 | 1 | killed |
| `u154.G1_policy_not_registered` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 43 | 11 | killed |
| `u154.G2_confinement_dropped` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 43 | 1 | killed |
| `u154.G3_rename_back_dropped` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 43 | 2 | killed |
| `u154.G4_stale_target_check_dropped` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 43 | 1 | killed |
| `u154.G5_unmatched_file_shelved_anyway` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 43 | 1 | killed |
| `u154.G6_subfolder_check_dropped` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 43 | 1 | killed |

## Zero rows and what they owe

- `u226.M18_waited_unformatted` (maintainer facing): maintainer facing, composite not required

## Row definitions

### `u102-a.P5_missing`

_plan_for: stop setting aside an accepted item whose file is gone, so the run after an apply plans it again

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `P5_missing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_second_apply_converges_and_claims_only_what_it_observed`
  - `tests/intake/test_repair_apply.py::test_an_accepted_file_that_is_gone_says_no_file_carries_the_name`

Old text:

```
        if not path.is_file():
            # ONE CLASS
```

New text:

```
        if False:
            # ONE CLASS
```

### `u102-a.P6_missing_says_what_exists`

_plan_for: always word a missing file as a rename already carried out, whether or not any file carries the proposed name

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `P6_missing_says_what_exists`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_an_accepted_file_that_is_gone_says_no_file_carries_the_name`

Old text:

```
            if target.is_file():
                why = (
```

New text:

```
            if True:
                why = (
```

### `u102-a.U1_no_stored_path`

_unusable_why: drop the refusal over an item the queue holds no path for

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `U1_no_stored_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_an_item_with_no_stored_path_is_held_and_never_guessed_at`

Old text:

```
    if accepted.path is None:
        return (
```

New text:

```
    if False:
        return (
```

### `u102-a.U2_bare_filename`

_unusable_why: stop requiring the proposed name to be a bare filename, so a path with a separator is applied

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `U2_bare_filename`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_proposed_name_that_is_not_a_same_suffix_filename_is_never_applied[../escaped.flac-not a bare filename]`
  - `tests/intake/test_repair_apply.py::test_a_proposed_name_that_is_not_a_same_suffix_filename_is_never_applied[nested/inside.flac-not a bare filename]`

Old text:

```
    if not proposed or proposed in {".", ".."} or Path(proposed).name != proposed:
```

New text:

```
    if not proposed or proposed in {".", ".."}:
```

### `u102-a.U3_empty_name`

_unusable_why: stop refusing an empty proposed name

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `U3_empty_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_proposed_name_that_is_not_a_same_suffix_filename_is_never_applied[-not a bare filename]`

Old text:

```
    if not proposed or proposed in {".", ".."} or Path(proposed).name != proposed:
```

New text:

```
    if proposed in {".", ".."} or Path(proposed).name != proposed:
```

### `u102-a.U4_same_suffix`

_unusable_why: drop the check that the proposed name keeps the file's extension

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `U4_same_suffix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_proposed_name_that_is_not_a_same_suffix_filename_is_never_applied[04A - 124 - Song - Artist.txt-change the file's extension]`

Old text:

```
    if Path(proposed).suffix.lower() != Path(accepted.path).suffix.lower():
```

New text:

```
    if False:
```

### `u102-a.U5_linked_file`

_unusable_why: drop the check that the stored path names the file the proposal was shown for, so a link's target is renamed

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `U5_linked_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_linked_file_is_never_renamed_through_its_link`

Old text:

```
    if accepted.recorded and Path(accepted.path).name != accepted.recorded:
```

New text:

```
    if False:
```

### `u102-b.G1_plan_referenced`

_plan_for: treat no candidate as referenced, leaving only the post gate check to hold the file

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `G1_plan_referenced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_proposal_for_a_referenced_file_refuses_and_its_sibling_is_renamed`

Old text:

```
        if not naming_cli.is_referenced(path, referenced)
    ]
```

New text:

```
        if True
    ]
```

### `u102-b.G2_post_gate_referenced`

_apply: drop the referenced check made after the gate

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `G2_post_gate_referenced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_row_that_appears_after_the_gate_holds_the_file`

Old text:

```
        if naming_cli.is_referenced(path, referenced):
            _owed(
```

New text:

```
        if False:
            _owed(
```

### `u102-b.G4_plan_collisions`

_plan_for: detect no collision while the plan is built, leaving it to the claim

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `G4_plan_collisions`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_collision_refuses_that_file_and_names_it`
  - `tests/intake/test_repair_apply.py::test_two_accepted_proposals_for_one_name_rename_neither`

Old text:

```
    collides = naming_cli.held_collisions([(path, acc.proposed) for acc, path in free])
```

New text:

```
    collides: dict[str, str] = {}
```

### `u102-b.G5_claim`

_apply: skip the atomic claim, so a name taken after the gate is overwritten by the rename

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `G5_claim`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_name_taken_after_the_gate_is_never_overwritten`
  - `tests/intake/test_repair_apply.py::test_a_name_the_filesystem_refuses_to_claim_is_named`

Old text:

```
            claimed = naming.claim_target(target)
```

New text:

```
            claimed = True
```

### `u102-b.G6_abort`

_apply: carry on past an abort answer

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `G6_abort`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_the_gate_refuses_unanswered_and_an_abort_touches_nothing`
  - `tests/intake/test_repair_apply.py::test_the_gate_shows_every_item_the_digest_was_taken_over`

Old text:

```
    if option == "abort":
```

New text:

```
    if False:
```

### `u102-b.G7_referenced_is_owed`

_HELD: stop counting a referenced file as an accepted rename that did not happen, so the run answers ok over it

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `G7_referenced_is_owed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_proposal_for_a_referenced_file_refuses_and_its_sibling_is_renamed`

Old text:

```
_HELD = (REFERENCED, COLLIDES, UNUSABLE)
```

New text:

```
_HELD = (COLLIDES, UNUSABLE)
```

### `u102-b.G8_collision_is_owed`

_HELD: stop counting a collision as owed, which is R-172 itself, a skipped collision reported as ok

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `G8_collision_is_owed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_collision_refuses_that_file_and_names_it`
  - `tests/intake/test_repair_apply.py::test_two_accepted_proposals_for_one_name_rename_neither`

Old text:

```
_HELD = (REFERENCED, COLLIDES, UNUSABLE)
```

New text:

```
_HELD = (REFERENCED, UNUSABLE)
```

### `u102-b.G9_post_gate_missing`

_apply: drop the check that the file is still there after the gate

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `G9_post_gate_missing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_file_deleted_after_the_gate_is_named_and_not_called_renamed`

Old text:

```
        if not path.is_file():
            _owed(item, "the file is no longer there")
            continue
```

New text:

```
(empty)
```

### `u102-b.R1_retryable_seed`

_apply: call a run retryable when all it holds is a file only a person can release

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `R1_retryable_seed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_proposal_for_a_referenced_file_refuses_and_its_sibling_is_renamed`
  - `tests/intake/test_repair_apply.py::test_an_item_with_no_stored_path_is_held_and_never_guessed_at`

Old text:

```
        item["action"] in _HELD and item["action"] not in _NEEDS_A_PERSON
```

New text:

```
        item["action"] in _HELD
```

### `u102-b.R2_retryable_after_gate`

_owed: stop marking the run retryable when a rename fails after the gate

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `R2_retryable_after_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_refused_rename_is_named_and_leaves_no_stub`

Old text:

```
        nonlocal retryable
        retryable = True
```

New text:

```
        nonlocal retryable
```

### `u102-b.S1_stub_removed`

_apply: leave the zero byte claim behind when the rename did not happen

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `S1_stub_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_refused_rename_is_named_and_leaves_no_stub`
  - `tests/intake/test_repair_apply.py::test_an_interrupt_between_the_claim_and_the_rename_leaves_no_stub`

Old text:

```
            if not moved:
                target.unlink(missing_ok=True)
```

New text:

```
            if not moved:
                pass
```

### `u126.F1_read_always`

Read the library's link whatever the plan adds, so a landing of held files refuses on a split library

- File: `src/cratekit/intake/native.py`
- Source: `u126.json`, row `F1_read_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 260 against a baseline of 260
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_landing_that_adds_no_row_needs_no_majority`

Old text:

```
        row_link.library_link(db) if any(row.action == ADD for row in rows) else None
```

New text:

```
        row_link.library_link(db)
```

### `u126.F3_counts_undigested`

Digest the value alone, so the counts the screen shows can change under an approval

- File: `src/cratekit/intake/native.py`
- Source: `u126.json`, row `F3_counts_undigested`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 260 against a baseline of 260
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_content_link_counts_move_the_digest`

Old text:

```
            {"value": plan.link.value, "carriers": plan.link.carriers, "rows": plan.link.rows}
```

New text:

```
            {"value": plan.link.value}
```

### `u126.P1_no_read`

Skip the library read and plan a fixed value, the binding's shape of a guess

- File: `src/cratekit/intake/native.py`
- Source: `u126.json`, row `P1_no_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 260 against a baseline of 260
- Kills: 9 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_library_with_no_majority_content_link_refuses_before_the_gate`
  - `tests/test_intake_land_native.py::test_a_row_whose_content_link_did_not_take_is_refused_after_the_commit`
  - `tests/test_intake_land_native.py::test_an_approval_taken_at_one_content_link_is_not_applied_at_another`
  - `tests/test_intake_land_native.py::test_the_content_link_counts_move_the_digest`
  - `tests/test_intake_land_native.py::test_the_content_link_moves_the_digest`
  - `tests/test_intake_land_native.py::test_the_gate_screen_names_every_row_its_columns_the_playlist_and_the_database`
  - `tests/test_intake_land_native.py::test_the_rows_carry_the_librarys_content_link_and_not_the_bindings`
  - `tests/test_intake_writers_native.py::test_the_gate_screen_names_the_row_its_columns_the_playlist_and_the_database`

Old text:

```
        row_link.library_link(db) if any(row.action == ADD for row in rows) else None
```

New text:

```
        row_link.LibraryLink(value=7, carriers=0, rows=0)
        if any(row.action == ADD for row in rows)
        else None
```

### `u126.P2_not_shown`

Drop ContentLink from a row's columns, so the screen and the row's part of the digest omit it

- File: `src/cratekit/intake/native.py`
- Source: `u126.json`, row `P2_not_shown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 260 against a baseline of 260
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_the_content_link_moves_the_digest`
  - `tests/test_intake_land_native.py::test_the_gate_screen_names_every_row_its_columns_the_playlist_and_the_database`
  - `tests/test_intake_writers_native.py::test_the_gate_screen_names_the_row_its_columns_the_playlist_and_the_database`

Old text:

```
            **(
                {rb_writer.CONTENT_LINK_COLUMN: self.content_link}
                if self.content_link is not None
                else {}
            ),
```

New text:

```
(empty)
```

### `u126.R1_binding_value_kept`

Drop the restamp of ContentLink, so the row keeps the binding's value

- File: `src/cratekit/intake/native.py`
- Source: `u126.json`, row `R1_binding_value_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 260 against a baseline of 260
- Kills: 52 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists_native.py::test_a_job_queued_with_no_name_lands_in_the_batch_playlist_as_before`
  - `tests/test_intake_land_account_playlists_native.py::test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists_native.py::test_a_track_both_playlists_brought_in_is_a_member_of_both`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_in_two_account_playlists_is_in_both`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_an_undated_playlist_from_before_u175_is_left_as_it_is`
  - `tests/test_intake_land_account_playlists_native.py::test_the_gate_screen_counts_the_owned_rows_beside_the_new`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_the_rotation_ages_an_account_playlist_by_its_landing_date`
  - ... and 37 more, see the JSON sidecar

Old text:

```
    setattr(content, rb_writer.CONTENT_LINK_COLUMN, row.content_link)
```

New text:

```
    pass
```

### `u126.R2_fill_if_null`

Set ContentLink only when the binding left it NULL, which it never does

- File: `src/cratekit/intake/native.py`
- Source: `u126.json`, row `R2_fill_if_null`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 260 against a baseline of 260
- Kills: 52 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists_native.py::test_a_job_queued_with_no_name_lands_in_the_batch_playlist_as_before`
  - `tests/test_intake_land_account_playlists_native.py::test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists_native.py::test_a_track_both_playlists_brought_in_is_a_member_of_both`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_in_two_account_playlists_is_in_both`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_an_undated_playlist_from_before_u175_is_left_as_it_is`
  - `tests/test_intake_land_account_playlists_native.py::test_the_gate_screen_counts_the_owned_rows_beside_the_new`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_the_rotation_ages_an_account_playlist_by_its_landing_date`
  - ... and 37 more, see the JSON sidecar

Old text:

```
    setattr(content, rb_writer.CONTENT_LINK_COLUMN, row.content_link)
```

New text:

```
    if getattr(content, rb_writer.CONTENT_LINK_COLUMN, None) is None:
        setattr(content, rb_writer.CONTENT_LINK_COLUMN, row.content_link)
```

### `u126.R3_check_skipped`

Skip the read back's ContentLink check

- File: `src/cratekit/intake/native.py`
- Source: `u126.json`, row `R3_check_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 260 against a baseline of 260
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_row_whose_content_link_did_not_take_is_refused_after_the_commit`
  - `tests/test_intake_land_native.py::test_assert_rows_identified_holds_the_link_to_the_one_planned`

Old text:

```
        if landed.content_link is None or row.content_link != landed.content_link
```

New text:

```
        if False
```

### `u126.R5_read_back_file_id`

Read back the file id column where the link should be

- File: `src/cratekit/intake/native.py`
- Source: `u126.json`, row `R5_read_back_file_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 260 against a baseline of 260
- Kills: 52 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists_native.py::test_a_job_queued_with_no_name_lands_in_the_batch_playlist_as_before`
  - `tests/test_intake_land_account_playlists_native.py::test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists_native.py::test_a_track_both_playlists_brought_in_is_a_member_of_both`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_in_two_account_playlists_is_in_both`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_an_undated_playlist_from_before_u175_is_left_as_it_is`
  - `tests/test_intake_land_account_playlists_native.py::test_the_gate_screen_counts_the_owned_rows_beside_the_new`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_the_rotation_ages_an_account_playlist_by_its_landing_date`
  - ... and 37 more, see the JSON sidecar

Old text:

```
        None if row[3] is None else int(row[3]),
```

New text:

```
        None if row[2] is None else int(row[2]),
```

### `u126.S1_file_id_kept`

Sample, U115: drop the file id restamp, so the row keeps the binding's random id

- File: `src/cratekit/intake/native.py`
- Source: `u126.json`, row `S1_file_id_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 260 against a baseline of 260
- Kills: 53 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists_native.py::test_a_job_queued_with_no_name_lands_in_the_batch_playlist_as_before`
  - `tests/test_intake_land_account_playlists_native.py::test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists_native.py::test_a_track_both_playlists_brought_in_is_a_member_of_both`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_in_two_account_playlists_is_in_both`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_an_undated_playlist_from_before_u175_is_left_as_it_is`
  - `tests/test_intake_land_account_playlists_native.py::test_the_gate_screen_counts_the_owned_rows_beside_the_new`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_the_rotation_ages_an_account_playlist_by_its_landing_date`
  - ... and 38 more, see the JSON sidecar

Old text:

```
    setattr(content, rb_writer.FILE_ID_COLUMN, file_id_of(row.target))
```

New text:

```
    pass
```

### `u126.S2_defaults_left_null`

Sample, R-923: drop the defaults fill, so the binding's NULLs stay

- File: `src/cratekit/intake/native.py`
- Source: `u126.json`, row `S2_defaults_left_null`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 260 against a baseline of 260
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_rows_carry_every_default_rekordbox_writes_on_a_row_it_makes`

Old text:

```
        if getattr(content, column, None) is None:
            setattr(content, column, value)
```

New text:

```
        pass
```

### `u128-b.N1_native_owned_unwritten`

The native commit joins no owned row to its playlist, the new rows alone

- File: `src/cratekit/intake/native.py`
- Source: `u128-b.json`, row `N1_native_owned_unwritten`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 260 against a baseline of 260
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_in_two_account_playlists_is_in_both`

Old text:

```
                        member.content_id
                        if member.target is None
```

New text:

```
                        ""
                        if member.target is None
```

### `u128-b.N2_native_record_no_pass`

The native landing's record names no pass, so a rerun cannot find what it mirrored

- File: `src/cratekit/intake/native.py`
- Source: `u128-b.json`, row `N2_native_record_no_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 260 against a baseline of 260
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`

Old text:

```
                ingest.INBOX_PASS_KEY: plan.pass_name or "",
```

New text:

```
                ingest.INBOX_PASS_KEY: "",
```

### `u128-b.N4_native_dropped_left_lost`

A native playlist holding nothing writable drops its left rows

- File: `src/cratekit/intake/native.py`
- Source: `u128-b.json`, row `N4_native_dropped_left_lost`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 260 against a baseline of 260
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_whose_only_file_is_unsupported_still_names_it_as_left`

Old text:

```
            dropped.extend((one.name, row) for row in left)
```

New text:

```
            pass
```

### `r239-a.A1_probe_to_true`

open_db answers every unnamed open with the key on, the old default, instead of asking the file

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A1_probe_to_true`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`
- Collected: 706 against a baseline of 706
- Kills: 124 (killed)
- Killed:
  - `tests/test_adopt_collection.py::test_a_dangling_genre_reference_reads_as_no_genre`
  - `tests/test_adopt_collection.py::test_a_row_whose_file_is_absent_is_still_a_row`
  - `tests/test_adopt_collection.py::test_both_composition_forms_come_back_exactly_as_recorded`
  - `tests/test_adopt_collection.py::test_the_database_file_is_byte_identical_after_a_full_read`
  - `tests/test_adopt_collection.py::test_the_reader_never_opens_the_database_for_writing`
  - `tests/test_adopt_collection.py::test_the_reader_yields_the_rows_the_database_holds`
  - `tests/test_adopt_collection.py::test_two_reads_in_one_process_open_the_database_once`
  - `tests/test_deletion.py::test_delete_review_abort_moves_nothing`
  - `tests/test_deletion.py::test_delete_review_exits_ok_after_the_recorded_decision`
  - `tests/test_deletion.py::test_delete_review_first_run_confirmed_reports_ok_and_trashes_nothing`
  - `tests/test_deletion.py::test_delete_review_prints_the_baseline_to_a_person_not_only_to_json`
  - `tests/test_deletion.py::test_delete_review_refuses_an_inline_answer_and_does_not_record_it`
  - `tests/test_deletion.py::test_delete_review_refuses_at_its_explicit_gate`
  - `tests/test_deletion.py::test_delete_review_says_on_the_refusal_that_a_first_run_accepted_history`
  - `tests/test_metadata_cli.py::test_a_corrupt_vocal_calibration_refuses_through_the_verb_and_writes_nothing`
  - ... and 109 more, see the JSON sidecar

Old text:

```
    if unlock is None:
        unlock = unlock_needed(target)

```

New text:

```
    if unlock is None:
        unlock = True

```

### `r239-a.A2_probe_to_false`

open_db answers every unnamed open with the key off, the constant the five verb sites used to pass

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A2_probe_to_false`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`
- Collected: 706 against a baseline of 706
- Kills: 7 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_a_snapshot_check_that_names_no_key_verifies_either_kind[encrypted]`
  - `tests/test_rb_writer_db.py::test_an_open_that_names_no_key_opens_either_kind_of_database[encrypted]`
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_applies_on_an_encrypted_library`
  - `tests/test_routing_workers.py::test_a_queued_rebuild_and_resort_run_on_an_encrypted_library[rebuild]`
  - `tests/test_routing_workers.py::test_a_queued_rebuild_and_resort_run_on_an_encrypted_library[resort]`
  - `tests/test_routing_workers.py::test_converge_compares_a_native_tree_on_an_encrypted_library`
  - `tests/test_routing_workers.py::test_unplaced_compares_on_an_encrypted_library`

Old text:

```
    if unlock is None:
        unlock = unlock_needed(target)

```

New text:

```
    if unlock is None:
        unlock = False

```

### `r239-a.A3_probe_removed`

Delete the probe block, so None reaches the binding, which reads it as no key

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A3_probe_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`
- Collected: 706 against a baseline of 706
- Kills: 7 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_a_snapshot_check_that_names_no_key_verifies_either_kind[encrypted]`
  - `tests/test_rb_writer_db.py::test_an_open_that_names_no_key_opens_either_kind_of_database[encrypted]`
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_applies_on_an_encrypted_library`
  - `tests/test_routing_workers.py::test_a_queued_rebuild_and_resort_run_on_an_encrypted_library[rebuild]`
  - `tests/test_routing_workers.py::test_a_queued_rebuild_and_resort_run_on_an_encrypted_library[resort]`
  - `tests/test_routing_workers.py::test_converge_compares_a_native_tree_on_an_encrypted_library`
  - `tests/test_routing_workers.py::test_unplaced_compares_on_an_encrypted_library`

Old text:

```
    if unlock is None:
        unlock = unlock_needed(target)

```

New text:

```
(empty)
```

### `r239-a.A4_open_default_true`

open_db's unlock default back to True, so the probe branch never fires for an unnamed open

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A4_open_default_true`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`
- Collected: 706 against a baseline of 706
- Kills: 123 (killed)
- Killed:
  - `tests/test_adopt_collection.py::test_a_dangling_genre_reference_reads_as_no_genre`
  - `tests/test_adopt_collection.py::test_a_row_whose_file_is_absent_is_still_a_row`
  - `tests/test_adopt_collection.py::test_both_composition_forms_come_back_exactly_as_recorded`
  - `tests/test_adopt_collection.py::test_the_database_file_is_byte_identical_after_a_full_read`
  - `tests/test_adopt_collection.py::test_the_reader_never_opens_the_database_for_writing`
  - `tests/test_adopt_collection.py::test_the_reader_yields_the_rows_the_database_holds`
  - `tests/test_adopt_collection.py::test_two_reads_in_one_process_open_the_database_once`
  - `tests/test_deletion.py::test_delete_review_abort_moves_nothing`
  - `tests/test_deletion.py::test_delete_review_exits_ok_after_the_recorded_decision`
  - `tests/test_deletion.py::test_delete_review_first_run_confirmed_reports_ok_and_trashes_nothing`
  - `tests/test_deletion.py::test_delete_review_prints_the_baseline_to_a_person_not_only_to_json`
  - `tests/test_deletion.py::test_delete_review_refuses_an_inline_answer_and_does_not_record_it`
  - `tests/test_deletion.py::test_delete_review_refuses_at_its_explicit_gate`
  - `tests/test_deletion.py::test_delete_review_says_on_the_refusal_that_a_first_run_accepted_history`
  - `tests/test_metadata_cli.py::test_a_corrupt_vocal_calibration_refuses_through_the_verb_and_writes_nothing`
  - ... and 108 more, see the JSON sidecar

Old text:

```
    force_cloud_canary: bool = False,
    unlock: bool | None = None,

```

New text:

```
    force_cloud_canary: bool = False,
    unlock: bool | None = True,

```

### `r239-a.A7_needed_always_true`

unlock_needed answers encrypted for every readable file, the U55 row that read zero with no encrypted input

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A7_needed_always_true`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`
- Collected: 706 against a baseline of 706
- Kills: 124 (killed)
- Killed:
  - `tests/test_adopt_collection.py::test_a_dangling_genre_reference_reads_as_no_genre`
  - `tests/test_adopt_collection.py::test_a_row_whose_file_is_absent_is_still_a_row`
  - `tests/test_adopt_collection.py::test_both_composition_forms_come_back_exactly_as_recorded`
  - `tests/test_adopt_collection.py::test_the_database_file_is_byte_identical_after_a_full_read`
  - `tests/test_adopt_collection.py::test_the_reader_never_opens_the_database_for_writing`
  - `tests/test_adopt_collection.py::test_the_reader_yields_the_rows_the_database_holds`
  - `tests/test_adopt_collection.py::test_two_reads_in_one_process_open_the_database_once`
  - `tests/test_deletion.py::test_delete_review_abort_moves_nothing`
  - `tests/test_deletion.py::test_delete_review_exits_ok_after_the_recorded_decision`
  - `tests/test_deletion.py::test_delete_review_first_run_confirmed_reports_ok_and_trashes_nothing`
  - `tests/test_deletion.py::test_delete_review_prints_the_baseline_to_a_person_not_only_to_json`
  - `tests/test_deletion.py::test_delete_review_refuses_an_inline_answer_and_does_not_record_it`
  - `tests/test_deletion.py::test_delete_review_refuses_at_its_explicit_gate`
  - `tests/test_deletion.py::test_delete_review_says_on_the_refusal_that_a_first_run_accepted_history`
  - `tests/test_metadata_cli.py::test_a_corrupt_vocal_calibration_refuses_through_the_verb_and_writes_nothing`
  - ... and 109 more, see the JSON sidecar

Old text:

```
            return not handle.read(len(SQLITE_HEADER)).startswith(SQLITE_HEADER)
```

New text:

```
            return True
```

### `r239-a.A8_needed_always_false`

unlock_needed answers plain for every readable file, the other U55 zero row, now with an encrypted input to fail on

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A8_needed_always_false`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`
- Collected: 706 against a baseline of 706
- Kills: 8 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_a_snapshot_check_that_names_no_key_verifies_either_kind[encrypted]`
  - `tests/test_rb_writer_db.py::test_an_encrypted_database_does_not_open_with_the_key_withheld`
  - `tests/test_rb_writer_db.py::test_an_open_that_names_no_key_opens_either_kind_of_database[encrypted]`
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_applies_on_an_encrypted_library`
  - `tests/test_routing_workers.py::test_a_queued_rebuild_and_resort_run_on_an_encrypted_library[rebuild]`
  - `tests/test_routing_workers.py::test_a_queued_rebuild_and_resort_run_on_an_encrypted_library[resort]`
  - `tests/test_routing_workers.py::test_converge_compares_a_native_tree_on_an_encrypted_library`
  - `tests/test_routing_workers.py::test_unplaced_compares_on_an_encrypted_library`

Old text:

```
            return not handle.read(len(SQLITE_HEADER)).startswith(SQLITE_HEADER)
```

New text:

```
            return False
```

### `r239-a.A9_header_nearby_value`

The plain header constant to a realistic nearby value, SQLite format 4, so no plain file matches it

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A9_header_nearby_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`
- Collected: 706 against a baseline of 706
- Kills: 124 (killed)
- Killed:
  - `tests/test_adopt_collection.py::test_a_dangling_genre_reference_reads_as_no_genre`
  - `tests/test_adopt_collection.py::test_a_row_whose_file_is_absent_is_still_a_row`
  - `tests/test_adopt_collection.py::test_both_composition_forms_come_back_exactly_as_recorded`
  - `tests/test_adopt_collection.py::test_the_database_file_is_byte_identical_after_a_full_read`
  - `tests/test_adopt_collection.py::test_the_reader_never_opens_the_database_for_writing`
  - `tests/test_adopt_collection.py::test_the_reader_yields_the_rows_the_database_holds`
  - `tests/test_adopt_collection.py::test_two_reads_in_one_process_open_the_database_once`
  - `tests/test_deletion.py::test_delete_review_abort_moves_nothing`
  - `tests/test_deletion.py::test_delete_review_exits_ok_after_the_recorded_decision`
  - `tests/test_deletion.py::test_delete_review_first_run_confirmed_reports_ok_and_trashes_nothing`
  - `tests/test_deletion.py::test_delete_review_prints_the_baseline_to_a_person_not_only_to_json`
  - `tests/test_deletion.py::test_delete_review_refuses_an_inline_answer_and_does_not_record_it`
  - `tests/test_deletion.py::test_delete_review_refuses_at_its_explicit_gate`
  - `tests/test_deletion.py::test_delete_review_says_on_the_refusal_that_a_first_run_accepted_history`
  - `tests/test_metadata_cli.py::test_a_corrupt_vocal_calibration_refuses_through_the_verb_and_writes_nothing`
  - ... and 109 more, see the JSON sidecar

Old text:

```
SQLITE_HEADER = b"SQLite format 3"
```

New text:

```
SQLITE_HEADER = b"SQLite format 4"
```

### `u145-s2.S2b_removed_member_read_live`

quarters: a membership rekordbox marked removed counts as a member

- File: `src/cratekit/favorites/split.py`
- Source: `u145-s2.json`, row `S2b_removed_member_read_live`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_track_taken_out_of_a_quarter_by_hand_goes_to_no_month`

Old text:

```
            if not rb_writer.membership_removed(song)
        ]
        found.append(Quarter(
```

New text:

```
            if True
        ]
        found.append(Quarter(
```

### `u145.C1_unplanned_membership_admitted`

addition_violations: a membership added into a month for a row the plan did not name is admitted

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `C1_unplanned_membership_admitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 3 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_an_addition_the_plan_did_not_name_is_a_violation[unplanned row-puts row '2']`
  - `tests/test_favorites_split.py::test_an_addition_the_plan_did_not_name_is_a_violation[wrong playlist-puts row '1' in playlist 'q']`
  - `tests/test_favorites_split.py::test_the_writer_refuses_a_membership_the_plan_did_not_name`

Old text:

```
        if row[m_marker] or content_id not in wanted.get(owner, set()):
```

New text:

```
        if row[m_marker]:
```

### `u145.C2_unplanned_playlist_admitted`

addition_violations: a playlist row the plan did not make is admitted

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `C2_unplanned_playlist_admitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_an_addition_the_plan_did_not_name_is_a_violation[unplanned playlist-unplanned djmdPlaylist row 'x']`

Old text:

```
    for key in sorted(added - set(created)):
```

New text:

```
    for key in sorted(set()):
```

### `u145.C3_parent_unchecked`

addition_violations: a made month under another parent is admitted

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `C3_parent_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_an_addition_the_plan_did_not_name_is_a_violation[wrong parent-not a live plain playlist named '2026-10' under 'f']`

Old text:

```
            or str(row[parent_at]) != str(parent)
```

New text:

```
            or False
```

### `u145.C4_changed_membership_admitted`

addition_violations: an existing membership that changed is admitted

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `C4_changed_membership_admitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_an_addition_the_plan_did_not_name_is_a_violation[changed membership-row 's1' changed]`

Old text:

```
        if before.memberships[key] != after.memberships[key]:
```

New text:

```
        if False:
```

### `u145.C5_content_unchecked`

addition_violations: a changed content row is admitted

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `C5_content_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_an_addition_the_plan_did_not_name_is_a_violation[content-djmdContent row changed]`

Old text:

```
    if before.content != after.content:
```

New text:

```
    if False:
```

### `u145.C6_existing_playlist_change_admitted`

addition_violations: an existing playlist row that changed beyond its bookkeeping is admitted

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `C6_existing_playlist_change_admitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_an_addition_the_plan_did_not_name_is_a_violation[quarter renamed-row 'q' changed ['Name']]`

Old text:

```
        if changed - allowed:
```

New text:

```
        if False:
```

### `u145.S10_unemptied_retired`

apply: a quarter whose member its month lacks is retired all the same

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `S10_unemptied_retired`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_quarter_whose_member_its_month_lacks_is_not_retired`

Old text:

```
        unemptied = _unemptied(db, planned, rows)
        if unemptied:
```

New text:

```
        unemptied = _unemptied(db, planned, rows)
        if False:
```

### `u145.S11_unemptied_asks_taken_back`

_unemptied: a taken back member is asked of a month it has none in

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `S11_unemptied_asks_taken_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_member_taken_out_of_all_favorites_goes_to_no_month_and_its_quarter_still_retires`

Old text:

```
            if content_id in month_of
            and content_id not in held.get(month_of[content_id], frozenset())
```

New text:

```
            if content_id not in held.get(month_of[content_id], frozenset())
```

### `u145.S12_retirement_admits_memberships_only`

apply: the retirement's commit admits a removed membership and no removed playlist

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `S12_retirement_admits_memberships_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 13 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_heart_every_sync_froze_again_is_resolved_once_with_its_first_dated_mention`
  - `tests/test_favorites_split.py::test_a_heart_taken_back_and_hearted_again_is_not_taken_back`
  - `tests/test_favorites_split.py::test_a_job_row_owned_when_its_job_ran_still_dates_the_member`
  - `tests/test_favorites_split.py::test_a_member_no_job_dates_takes_the_accounts_date_and_one_dated_nowhere_goes_to_undated`
  - `tests/test_favorites_split.py::test_a_member_taken_out_of_all_favorites_goes_to_no_month_and_its_quarter_still_retires`
  - `tests/test_favorites_split.py::test_a_member_two_quarters_hold_is_one_member_and_both_quarters_retire`
  - `tests/test_favorites_split.py::test_a_month_already_there_is_added_to_and_a_member_it_holds_is_not_added_twice`
  - `tests/test_favorites_split.py::test_a_quarter_of_seventeen_splits_into_fifteen_and_two_and_is_retired`
  - `tests/test_favorites_split.py::test_a_run_stopped_after_its_additions_replans_to_the_same_digest_and_finishes`
  - `tests/test_favorites_split.py::test_a_second_run_plans_nothing_and_opens_no_gate`
  - `tests/test_favorites_split.py::test_a_track_taken_out_of_a_quarter_by_hand_goes_to_no_month`
  - `tests/test_favorites_split.py::test_no_content_row_tempo_or_grid_is_written`
  - `tests/test_favorites_split.py::test_the_record_carries_both_commits_under_the_favourites_key`

Old text:

```
                rb_writer.commit_guarded(db, removals=REMOVALS)
```

New text:

```
                rb_writer.commit_guarded(db, removals=(rb_writer.MEMBERSHIP_TABLE,))
```

### `u145.S13_retirement_confined_to_nothing`

apply: the node confinement is told no quarter is removed

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `S13_retirement_confined_to_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 13 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_heart_every_sync_froze_again_is_resolved_once_with_its_first_dated_mention`
  - `tests/test_favorites_split.py::test_a_heart_taken_back_and_hearted_again_is_not_taken_back`
  - `tests/test_favorites_split.py::test_a_job_row_owned_when_its_job_ran_still_dates_the_member`
  - `tests/test_favorites_split.py::test_a_member_no_job_dates_takes_the_accounts_date_and_one_dated_nowhere_goes_to_undated`
  - `tests/test_favorites_split.py::test_a_member_taken_out_of_all_favorites_goes_to_no_month_and_its_quarter_still_retires`
  - `tests/test_favorites_split.py::test_a_member_two_quarters_hold_is_one_member_and_both_quarters_retire`
  - `tests/test_favorites_split.py::test_a_month_already_there_is_added_to_and_a_member_it_holds_is_not_added_twice`
  - `tests/test_favorites_split.py::test_a_quarter_of_seventeen_splits_into_fifteen_and_two_and_is_retired`
  - `tests/test_favorites_split.py::test_a_run_stopped_after_its_additions_replans_to_the_same_digest_and_finishes`
  - `tests/test_favorites_split.py::test_a_second_run_plans_nothing_and_opens_no_gate`
  - `tests/test_favorites_split.py::test_a_track_taken_out_of_a_quarter_by_hand_goes_to_no_month`
  - `tests/test_favorites_split.py::test_no_content_row_tempo_or_grid_is_written`
  - `tests/test_favorites_split.py::test_the_record_carries_both_commits_under_the_favourites_key`

Old text:

```
                    removed=[one.playlist_id for one in planned.quarters],
```

New text:

```
                    removed=[],
```

### `u145.S1_any_name_is_a_quarter`

quarters: every playlist beside the source but Undated is a quarter, All Favorites and the months included

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `S1_any_name_is_a_quarter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 8 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_library_with_no_quarter_never_walks_the_library_or_asks_the_account`
  - `tests/test_favorites_split.py::test_a_member_two_quarters_hold_is_one_member_and_both_quarters_retire`
  - `tests/test_favorites_split.py::test_a_month_already_there_is_added_to_and_a_member_it_holds_is_not_added_twice`
  - `tests/test_favorites_split.py::test_a_quarter_of_seventeen_splits_into_fifteen_and_two_and_is_retired`
  - `tests/test_favorites_split.py::test_a_run_stopped_after_its_additions_replans_to_the_same_digest_and_finishes`
  - `tests/test_favorites_split.py::test_a_second_run_plans_nothing_and_opens_no_gate`
  - `tests/test_favorites_split.py::test_a_track_taken_out_of_a_quarter_by_hand_goes_to_no_month`
  - `tests/test_favorites_split.py::test_the_record_carries_both_commits_under_the_favourites_key`

Old text:

```
        if not placeholders.QUARTER_LABEL.fullmatch(name):
```

New text:

```
        if name == placeholders.UNDATED:
```

### `u145.S3_last_dated_mention_wins`

_job_rows: a heart's last dated mention wins over its first

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `S3_last_dated_mention_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_heart_every_sync_froze_again_is_resolved_once_with_its_first_dated_mention`

Old text:

```
                if row.hearted is not None and row.ref not in found:
```

New text:

```
                if row.hearted is not None:
```

### `u145.S4_account_never_asked`

date_members: a member no job dates is never looked for on the account

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `S4_account_never_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_member_no_job_dates_takes_the_accounts_date_and_one_dated_nowhere_goes_to_undated`

Old text:

```
    rest = wanted - set(by_row)
    if rest:
```

New text:

```
    rest = wanted - set(by_row)
    if False:
```

### `u145.S5_job_dates_ignored`

_job_rows: no hearts job row is read, so every date comes from the account

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `S5_job_dates_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 11 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_heart_every_sync_froze_again_is_resolved_once_with_its_first_dated_mention`
  - `tests/test_favorites_split.py::test_a_heart_taken_back_and_hearted_again_is_not_taken_back`
  - `tests/test_favorites_split.py::test_a_job_row_owned_when_its_job_ran_still_dates_the_member`
  - `tests/test_favorites_split.py::test_a_member_no_job_dates_takes_the_accounts_date_and_one_dated_nowhere_goes_to_undated`
  - `tests/test_favorites_split.py::test_a_member_taken_out_of_all_favorites_goes_to_no_month_and_its_quarter_still_retires`
  - `tests/test_favorites_split.py::test_a_member_two_quarters_hold_is_one_member_and_both_quarters_retire`
  - `tests/test_favorites_split.py::test_a_month_already_there_is_added_to_and_a_member_it_holds_is_not_added_twice`
  - `tests/test_favorites_split.py::test_a_quarter_of_seventeen_splits_into_fifteen_and_two_and_is_retired`
  - `tests/test_favorites_split.py::test_a_run_stopped_after_its_additions_replans_to_the_same_digest_and_finishes`
  - `tests/test_favorites_split.py::test_a_second_run_plans_nothing_and_opens_no_gate`
  - `tests/test_favorites_split.py::test_a_track_taken_out_of_a_quarter_by_hand_goes_to_no_month`

Old text:

```
                if row.hearted is not None and row.ref not in found:
```

New text:

```
                if row.hearted is None and row.ref not in found:
```

### `u145.S6_rehearted_is_taken_back`

taken_back: a heart removed and added back live is still taken back

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `S6_rehearted_is_taken_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_heart_taken_back_and_hearted_again_is_not_taken_back`

Old text:

```
    return frozenset(removed - placement.members(db, home.source_id))
```

New text:

```
    return frozenset(removed)
```

### `u145.S7_taken_back_placed`

_planned: a member the author took back is put in its month all the same

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `S7_taken_back_placed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_member_taken_out_of_all_favorites_goes_to_no_month_and_its_quarter_still_retires`

Old text:

```
    members = tuple(one for one in every if one.content_id not in gone)
```

New text:

```
    members = tuple(one for one in every)
```

### `u145.S8_stale_digest_accepted`

apply: a digest that moved between the approval and the write is written anyway

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `S8_stale_digest_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_quarter_that_changed_after_the_approval_is_refused_and_nothing_is_written`

Old text:

```
    if again.digest != approved.digest:
```

New text:

```
    if False:
```

### `u145.S9_digest_covers_the_months_state`

identity: the digest covers what the months hold, so a run stopped after its additions plans another digest

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `S9_digest_covers_the_months_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_run_stopped_after_its_additions_replans_to_the_same_digest_and_finishes`

Old text:

```
            "taken_back": [one.content_id for one in self.taken_back],
        }
```

New text:

```
            "taken_back": [one.content_id for one in self.taken_back],
            "held": {name: sorted(ids) for name, ids in self.held.items()},
        }
```

### `u145.V1_gate_on_nothing`

favorites_split: a library with no quarter is still put to the gate

- File: `src/cratekit/favorites/split_cli.py`
- Source: `u145.json`, row `V1_gate_on_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_library_with_no_quarter_never_walks_the_library_or_asks_the_account`
  - `tests/test_favorites_split.py::test_a_second_run_plans_nothing_and_opens_no_gate`

Old text:

```
    if not plan.writes:
```

New text:

```
    if False:
```

### `u145.V2_no_ack`

favorites_split: the backup acknowledgment is not read before the plan

- File: `src/cratekit/favorites/split_cli.py`
- Source: `u145.json`, row `V2_no_ack`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    session.assert_backup_acknowledged(cfg)
```

New text:

```
    pass
```

### `r1677.L1_rehearsal_unmeasured`

land_cli: the rehearsal's own check is not measured before its copy

- File: `src/cratekit/intake/land_cli.py`
- Source: `r1677.json`, row `L1_rehearsal_unmeasured`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_temporary_volume_with_no_room_for_the_rehearsal_check_refuses_before_its_copy`

Old text:

```
    snapshot.assert_room_for_check(area.database)
    try:
```

New text:

```
    try:
```

### `r1677.L2_rehearsal_room_silent`

land_cli: a rehearsal check whose copy found no room is told as a failed integrity check

- File: `src/cratekit/intake/land_cli.py`
- Source: `r1677.json`, row `L2_rehearsal_room_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_check_whose_copy_finds_no_room_is_refused_under_the_room_slug`

Old text:

```
        if no_room is not None:
            raise no_room from failed
        sound = False
```

New text:

```
        sound = False
```

### `r1677.L3_rehearsal_other_failure_sound`

land_cli: a rehearsal check whose copy failed for another reason is reported sound, integrity ok without a check

- File: `src/cratekit/intake/land_cli.py`
- Source: `r1677.json`, row `L3_rehearsal_other_failure_sound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_check_whose_copy_fails_otherwise_is_still_a_failed_check`

Old text:

```
            raise no_room from failed
        sound = False
```

New text:

```
            raise no_room from failed
        sound = True
```

### `u162.L10_interrupt_cancel`

_rehearse_native: an interrupt reported as internal-error rather than cancelled

- File: `src/cratekit/intake/land_cli.py`
- Source: `u162.json`, row `L10_interrupt_cancel`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_an_interrupted_rehearsal_is_a_cancel_that_names_its_area`

Old text:

```
            "cancelled",
```

New text:

```
            "internal-error",
```

### `u162.L12_rehearsal_equal`

rehearsal_facts: report every rehearsal as equal to the live plan

- File: `src/cratekit/intake/land_cli.py`
- Source: `u162.json`, row `L12_rehearsal_equal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_live_plan_that_differs_names_the_rehearsal_and_prints_the_differing_lines`

Old text:

```
    equal = found.get("digest") == digest
```

New text:

```
    equal = True
```

### `u162.L1_bridge_refusal`

intake_land: drop the refusal of --rehearse on an intake tree on the xml bridge

- File: `src/cratekit/intake/land_cli.py`
- Source: `u162.json`, row `L1_bridge_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_on_the_bridge_is_refused`

Old text:

```
    if rehearse and not medium.native:
```

New text:

```
    if False:
```

### `u162.L2_area_plan_compare`

_rehearse_in: drop the refusal of an area plan that is not the live plan, so a differing plan is applied

- File: `src/cratekit/intake/land_cli.py`
- Source: `u162.json`, row `L2_area_plan_compare`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 95 against a baseline of 95
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_scratch_plan_that_is_not_the_live_plan_applies_nothing`
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_file_name_that_differs_still_refuses_and_names_the_line`

Old text:

```
        if differ:
            raise refuse(
```

New text:

```
        if False:
            raise refuse(
```

### `u162.L4_occupied_hold`

_rehearse_in: drop the hold of the live batch folder's names at the area (round one's fix)

- File: `src/cratekit/intake/land_cli.py`
- Source: `u162.json`, row `L4_occupied_hold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_name_the_live_batch_folder_holds_is_refused_at_the_area_as_it_will_be_live`

Old text:

```
            if (target / item.name).exists() or (target / item.name).is_symlink():
```

New text:

```
            if False:
```

### `u162.L6_gridless_read_back`

_rehearse_in: drop the gridless read back of the landed rows

- File: `src/cratekit/intake/land_cli.py`
- Source: `u162.json`, row `L6_gridless_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_landed_row_read_back_with_a_grid_is_refused_and_never_reported_gridless`

Old text:

```
            native.assert_rows_gridless(landed.collection)
            native.assert_rows_identified(landed.collection)
            rows_after
```

New text:

```
            native.assert_rows_identified(landed.collection)
            rows_after
```

### `u162.L7_identified_read_back`

_rehearse_in: drop the file id read back of the landed rows

- File: `src/cratekit/intake/land_cli.py`
- Source: `u162.json`, row `L7_identified_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_landed_row_whose_file_id_did_not_take_is_refused_in_the_rehearsal`

Old text:

```
            native.assert_rows_gridless(landed.collection)
            native.assert_rows_identified(landed.collection)
            rows_after
```

New text:

```
            native.assert_rows_gridless(landed.collection)
            rows_after
```

### `u162.L8_success_witness`

_rehearse_native: drop the witness on the success path, so a rehearsal that touched the live library reports clean

- File: `src/cratekit/intake/land_cli.py`
- Source: `u162.json`, row `L8_success_witness`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 95 against a baseline of 95
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_a_batch_filed_in_another_year_is_refused`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_the_live_library_is_refused_as_a_defect`

Old text:

```
    rehearsal.assert_untouched(before, kept=area.paths)
    rehearsal.remove(area)
```

New text:

```
    rehearsal.remove(area)
```

### `u162.L9_kept_area_named`

_rehearse_native: a refusal inside the rehearsal no longer carries the kept area in its detail

- File: `src/cratekit/intake/land_cli.py`
- Source: `u162.json`, row `L9_kept_area_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 95 against a baseline of 95
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_refusal_inside_the_rehearsal_keeps_its_reason_and_names_the_area`
  - `tests/test_intake_land_rehearse.py::test_a_scratch_plan_that_is_not_the_live_plan_applies_nothing`
  - `tests/test_intake_land_rehearse.py::test_an_interrupted_rehearsal_keeps_its_area_and_names_it`
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_file_name_that_differs_still_refuses_and_names_the_line`

Old text:

```
            detail={**dict(inner.detail), "rehearsal_area": [str(path) for path in area.paths]},
```

New text:

```
            detail=dict(inner.detail),
```

### `u188.M1_stored_pair_dropped`

_mapped_back: leave the stored spelling pair out, so FolderPath on a renamed drive is never mapped back (the defect)

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M1_stored_pair_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 95 against a baseline of 95
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_batch_whose_name_is_not_ascii_rehearses_equal_and_the_gate_says_so`
  - `tests/test_intake_land_rehearse.py::test_a_library_whose_base_drive_is_not_its_mount_rehearses_equal_and_the_gate_says_so`
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_file_name_that_differs_still_refuses_and_names_the_line`

Old text:

```
                (str(scratch_target), str(target)),
                stored,
            )
```

New text:

```
                (str(scratch_target), str(target)),
            )
```

### `u188.M2_scratch_stored_under_the_mount`

_mapped_back: spell the area's folder with no base drive, so the scratch side of the stored pair is the mounted spelling

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M2_scratch_stored_under_the_mount`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 95 against a baseline of 95
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_batch_whose_name_is_not_ascii_rehearses_equal_and_the_gate_says_so`
  - `tests/test_intake_land_rehearse.py::test_a_library_whose_base_drive_is_not_its_mount_rehearses_equal_and_the_gate_says_so`
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_file_name_that_differs_still_refuses_and_names_the_line`

Old text:

```
            base_drive=scratch_rows.base_drive,
            current_drive=scratch_rows.current_drive,
```

New text:

```
            base_drive=None,
            current_drive=scratch_rows.current_drive,
```

### `u188.M3_live_stored_under_the_mount`

_mapped_back: spell the live folder with no base drive, so the area's FolderPath maps to the mounted spelling the live rows do not carry

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M3_live_stored_under_the_mount`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 95 against a baseline of 95
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_batch_whose_name_is_not_ascii_rehearses_equal_and_the_gate_says_so`
  - `tests/test_intake_land_rehearse.py::test_a_library_whose_base_drive_is_not_its_mount_rehearses_equal_and_the_gate_says_so`
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_file_name_that_differs_still_refuses_and_names_the_line`

Old text:

```
            target, base_drive=rows.base_drive, current_drive=rows.current_drive
```

New text:

```
            target, base_drive=None, current_drive=rows.current_drive
```

### `u188.M4_staging_pair_dropped`

_mapped_back: leave the staging pair out, so every from line keeps the area's staging

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M4_staging_pair_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 95 against a baseline of 95
- Kills: 20 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_batch_whose_name_is_not_ascii_rehearses_equal_and_the_gate_says_so`
  - `tests/test_intake_land_rehearse.py::test_a_copy_that_fails_its_integrity_check_is_refused_naming_the_area`
  - `tests/test_intake_land_rehearse.py::test_a_landed_row_read_back_with_a_grid_is_refused_and_never_reported_gridless`
  - `tests/test_intake_land_rehearse.py::test_a_landed_row_whose_file_id_did_not_take_is_refused_in_the_rehearsal`
  - `tests/test_intake_land_rehearse.py::test_a_library_whose_base_drive_is_not_its_mount_rehearses_equal_and_the_gate_says_so`
  - `tests/test_intake_land_rehearse.py::test_a_live_plan_that_differs_names_the_rehearsal_and_prints_the_differing_lines`
  - `tests/test_intake_land_rehearse.py::test_a_name_the_live_batch_folder_holds_is_refused_at_the_area_as_it_will_be_live`
  - `tests/test_intake_land_rehearse.py::test_a_refusal_inside_the_rehearsal_keeps_its_reason_and_names_the_area`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_beside_another_runs_area_lands_and_leaves_that_area_alone`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_check_whose_copy_fails_otherwise_is_still_a_failed_check`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_check_whose_copy_finds_no_room_is_refused_under_the_room_slug`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_leaves_staging_the_music_folder_and_the_database_as_they_were`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_of_another_batch_is_not_the_one_compared`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_a_batch_filed_in_another_year_is_refused`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_the_live_library_is_refused_as_a_defect`
  - ... and 5 more, see the JSON sidecar

Old text:

```
                (str(area.staging), str(planned.folder)),
                (str(scratch_target), str(target)),
```

New text:

```
                (str(scratch_target), str(target)),
```

### `u188.M6_mapped_as_lines`

_rehearse_in: map the area's plan after it is printed, so a JSON escaped accent or quote is never mapped (the review's round one)

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M6_mapped_as_lines`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 95 against a baseline of 95
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_batch_whose_name_is_not_ascii_rehearses_equal_and_the_gate_says_so`
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_file_name_that_differs_still_refuses_and_names_the_line`

Old text:

```
        back = rehearsal.lines(
            rehearsal.mapped(
                plan_identity(staged, scratch_rows, target=scratch_target, archived=archived),
                pairs,
            )
        )
```

New text:

```
        back = rehearsal.mapped(
            plan_lines(staged, scratch_rows, target=scratch_target, archived=archived), pairs
        )
```

### `u226.M10_settle_lag_known_only`

_settled: a lagging window is read again only when something is known

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u226.json`, row `M10_settle_lag_known_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`
- Collected: 441 against a baseline of 441
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_first_reading_whose_window_lags_is_read_again_before_any_move`
  - `tests/test_outbound_window_lag.py::test_a_first_reading_whose_window_never_catches_up_refuses_with_nothing_moved`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_beside_a_first_page_sends_nothing`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_once_is_read_again_and_lands`
  - `tests/test_outbound_window_lag.py::test_an_order_whose_later_pages_lag_too_is_held_with_nothing_moved`

Old text:

```
                if problem == "window-lags":

```

New text:

```
                if problem == "window-lags" and known is not None:

```

### `u226.M11_settle_kept_ignored`

_settled: a caller's kept wording is ignored for the order's

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u226.json`, row `M11_settle_kept_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`
- Collected: 441 against a baseline of 441
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_beside_a_first_page_sends_nothing`

Old text:

```
        if kept is None:
            kept = (
```

New text:

```
        if True:
            kept = (
```

### `u226.M13_removal_window_wrong`

_removal_read_back: a lagging window is read as a wrong track gone, refused at once

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u226.json`, row `M13_removal_window_wrong`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`
- Collected: 441 against a baseline of 441
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_window_lags_beside_a_first_page_refuses_after_the_bound`
  - `tests/test_outbound_window_lag.py::test_every_judged_reading_records_its_readings_and_wait`

Old text:

```
                tracks = "window"

```

New text:

```
                tracks = None

```

### `u226.M15_wait_uncounted`

_paused: the pause is taken and not counted in the record

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u226.json`, row `M15_wait_uncounted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`
- Collected: 441 against a baseline of 441
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_every_judged_reading_records_its_readings_and_wait`
  - `tests/test_outbound_window_lag.py::test_the_pause_after_a_412_is_counted_in_the_moves_record`

Old text:

```
        self._sleep(seconds)
        note["waited"] += seconds

```

New text:

```
        self._sleep(seconds)

```

### `u226.M17_removal_positions_unsettled`

remove_tracks: the positions read once with no reread of a lag, as before round one's fix

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u226.json`, row `M17_removal_positions_unsettled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`
- Collected: 441 against a baseline of 441
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_beside_a_first_page_sends_nothing`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_once_is_read_again_and_lands`
  - `tests/test_outbound_window_lag.py::test_every_judged_reading_records_its_readings_and_wait`

Old text:

```
            playlist, before = self._settled(
                identifier,
                None,
                exact=False,
                after="removal positions",
                kept="nothing was taken off it",
            )
```

New text:

```
            playlist = self._playlist(identifier)
            before = self._positions(identifier, playlist)
```

### `u226.M18_waited_unformatted`

_waited: seconds named as 7.0 rather than 7

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u226.json`, row `M18_waited_unformatted`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return f"{seconds:g}"
```

New text:

```
    return f"{seconds}"
```

### `u226.M7_reading_takes_window`

_reading: the window read is the reading even when the unpaged read is whole

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u226.json`, row `M7_reading_takes_window`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`
- Collected: 441 against a baseline of 441
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_removal_past_the_first_hundred_takes_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_a_removal_planned_from_a_lagging_window_takes_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_window_lags_and_unpaged_read_does_not_is_taken_as_done`
  - `tests/test_outbound_window_lag.py::test_an_order_past_the_first_hundred_moves_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_an_order_planned_after_a_lagging_window_is_planned_from_the_unpaged_read`

Old text:

```
            unpaged if window == listing.WINDOW_UNPAGED else paged,
```

New text:

```
            paged,
```

### `u226.M8_unpaged_first`

_reading: the unpaged read taken before the window, so the window's tag is carried

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u226.json`, row `M8_unpaged_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`
- Collected: 441 against a baseline of 441
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_removal_past_the_first_hundred_takes_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_a_removal_planned_from_a_lagging_window_takes_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_an_order_past_the_first_hundred_moves_the_track_where_it_stands`

Old text:

```
        tracks = self._listed(playlist_id, playlist)
        paged = [listing.row_id(track) for track in tracks]
        unpaged = [
            listing.row_id(track)
            for track in self._read(
                f"read the playlist {playlist_id}",
                lambda: listing.playlist_tracks_unpaged(playlist),
            )
        ]
```

New text:

```
        unpaged = [
            listing.row_id(track)
            for track in self._read(
                f"read the playlist {playlist_id}",
                lambda: listing.playlist_tracks_unpaged(playlist),
            )
        ]
        tracks = self._listed(playlist_id, playlist)
        paged = [listing.row_id(track) for track in tracks]
```

### `u226.M9_positions_no_lag_refusal`

_positions: a lagging window is not refused, its positions taken

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u226.json`, row `M9_positions_no_lag_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`
- Collected: 441 against a baseline of 441
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_first_reading_whose_window_never_catches_up_refuses_with_nothing_moved`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_beside_a_first_page_sends_nothing`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_once_is_read_again_and_lands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_later_pages_lag_too_is_held_with_nothing_taken_off`
  - `tests/test_outbound_window_lag.py::test_an_order_whose_later_pages_lag_too_is_held_with_nothing_moved`

Old text:

```
        if window == listing.WINDOW_LAGS:
            raise _window_lags(str(playlist_id), "nothing was sent on that reading")
```

New text:

```
        if False:
            raise _window_lags(str(playlist_id), "nothing was sent on that reading")
```

### `u272.C1_no_flush`

flush_to_disk: open and close the path and flush nothing

- File: `src/cratekit/core/config.py`
- Source: `u272.json`, row `C1_no_flush`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 630 against a baseline of 630
- Kills: 14 (killed)
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_a_capture_outside_the_configured_store_is_flushed_too`
  - `tests/test_snapshot_flush_u272.py::test_a_directory_is_flushed_through_the_same_call`
  - `tests/test_snapshot_flush_u272.py::test_a_filesystem_without_the_full_flush_gets_the_plain_sync[EINVAL]`
  - `tests/test_snapshot_flush_u272.py::test_a_filesystem_without_the_full_flush_gets_the_plain_sync[ENOTSUP]`
  - `tests/test_snapshot_flush_u272.py::test_a_filesystem_without_the_full_flush_gets_the_plain_sync[ENOTTY]`
  - `tests/test_snapshot_flush_u272.py::test_a_full_flush_that_fails_on_the_device_raises_rather_than_falling_back`
  - `tests/test_snapshot_flush_u272.py::test_a_plain_sync_that_fails_raises`
  - `tests/test_snapshot_flush_u272.py::test_an_unverified_capture_is_flushed_in_the_same_order`
  - `tests/test_snapshot_flush_u272.py::test_every_file_a_capture_holds_is_flushed_before_its_manifest_by_walking`
  - `tests/test_snapshot_flush_u272.py::test_the_copy_its_companions_and_its_directories_reach_the_disk_before_the_manifest`
  - `tests/test_snapshot_flush_u272.py::test_the_flush_follows_the_check_so_what_the_check_leaves_is_flushed`
  - `tests/test_snapshot_flush_u272.py::test_the_full_flush_is_asked_for_where_the_platform_offers_one`
  - `tests/test_snapshot_flush_u272.py::test_the_manifest_is_followed_by_a_flush_of_the_directory_that_holds_it`
  - `tests/test_snapshot_flush_u272.py::test_where_no_full_flush_exists_the_plain_sync_is_the_flush`

Old text:

```
    try:
        _flush_descriptor(fd)
    except OSError as exc:
```

New text:

```
    try:
        pass
    except OSError as exc:
```

### `u272.C2_full_flush_error_swallowed`

_flush_descriptor: fall back to the plain sync on every error of the full flush, an I/O error included

- File: `src/cratekit/core/config.py`
- Source: `u272.json`, row `C2_full_flush_error_swallowed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 630 against a baseline of 630
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_a_full_flush_that_fails_on_the_device_raises_rather_than_falling_back`

Old text:

```
            if exc.errno not in _FULL_FLUSH_UNSUPPORTED:
                raise
```

New text:

```
            if False:
                raise
```

### `u272.C3_full_flush_then_sync`

_flush_descriptor: drop the return after a full flush, so the plain sync runs as well

- File: `src/cratekit/core/config.py`
- Source: `u272.json`, row `C3_full_flush_then_sync`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 630 against a baseline of 630
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_the_full_flush_is_asked_for_where_the_platform_offers_one`

Old text:

```
            _full_flush(fd, _FULL_FLUSH)
            return
```

New text:

```
            _full_flush(fd, _FULL_FLUSH)
```

### `u272.C4_full_flush_never_asked`

_flush_descriptor: never ask for the full flush, the plain sync on every platform

- File: `src/cratekit/core/config.py`
- Source: `u272.json`, row `C4_full_flush_never_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 630 against a baseline of 630
- Kills: 5 (killed)
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_a_filesystem_without_the_full_flush_gets_the_plain_sync[EINVAL]`
  - `tests/test_snapshot_flush_u272.py::test_a_filesystem_without_the_full_flush_gets_the_plain_sync[ENOTSUP]`
  - `tests/test_snapshot_flush_u272.py::test_a_filesystem_without_the_full_flush_gets_the_plain_sync[ENOTTY]`
  - `tests/test_snapshot_flush_u272.py::test_a_full_flush_that_fails_on_the_device_raises_rather_than_falling_back`
  - `tests/test_snapshot_flush_u272.py::test_the_full_flush_is_asked_for_where_the_platform_offers_one`

Old text:

```
    if _FULL_FLUSH is not None:
        try:
```

New text:

```
    if False:
        try:
```

### `u272.C5_eio_counts_as_unsupported`

_FULL_FLUSH_UNSUPPORTED: count an I/O error as a filesystem without the full flush

- File: `src/cratekit/core/config.py`
- Source: `u272.json`, row `C5_eio_counts_as_unsupported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 630 against a baseline of 630
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_a_full_flush_that_fails_on_the_device_raises_rather_than_falling_back`

Old text:

```
frozenset({errno.ENOTSUP, errno.EOPNOTSUPP, errno.EINVAL, errno.ENOTTY})
```

New text:

```
frozenset({errno.ENOTSUP, errno.EOPNOTSUPP, errno.EINVAL, errno.ENOTTY, errno.EIO})
```

### `u272.C6_no_plain_sync`

_flush_descriptor: drop the plain sync, so a platform without the full flush flushes nothing

- File: `src/cratekit/core/config.py`
- Source: `u272.json`, row `C6_no_plain_sync`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 630 against a baseline of 630
- Kills: 12 (killed)
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_a_capture_outside_the_configured_store_is_flushed_too`
  - `tests/test_snapshot_flush_u272.py::test_a_directory_is_flushed_through_the_same_call`
  - `tests/test_snapshot_flush_u272.py::test_a_filesystem_without_the_full_flush_gets_the_plain_sync[EINVAL]`
  - `tests/test_snapshot_flush_u272.py::test_a_filesystem_without_the_full_flush_gets_the_plain_sync[ENOTSUP]`
  - `tests/test_snapshot_flush_u272.py::test_a_filesystem_without_the_full_flush_gets_the_plain_sync[ENOTTY]`
  - `tests/test_snapshot_flush_u272.py::test_a_plain_sync_that_fails_raises`
  - `tests/test_snapshot_flush_u272.py::test_an_unverified_capture_is_flushed_in_the_same_order`
  - `tests/test_snapshot_flush_u272.py::test_every_file_a_capture_holds_is_flushed_before_its_manifest_by_walking`
  - `tests/test_snapshot_flush_u272.py::test_the_copy_its_companions_and_its_directories_reach_the_disk_before_the_manifest`
  - `tests/test_snapshot_flush_u272.py::test_the_flush_follows_the_check_so_what_the_check_leaves_is_flushed`
  - `tests/test_snapshot_flush_u272.py::test_the_manifest_is_followed_by_a_flush_of_the_directory_that_holds_it`
  - `tests/test_snapshot_flush_u272.py::test_where_no_full_flush_exists_the_plain_sync_is_the_flush`

Old text:

```
                raise
    os.fsync(fd)

```

New text:

```
                raise

```

### `u272.C7_error_names_no_path`

flush_to_disk: raise a flush error as it came, naming no file

- File: `src/cratekit/core/config.py`
- Source: `u272.json`, row `C7_error_names_no_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 630 against a baseline of 630
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_a_plain_sync_that_fails_raises`

Old text:

```
        if exc.filename is not None:
            raise
        raise OSError(exc.errno, exc.strerror or str(exc), str(path)) from exc
```

New text:

```
        raise
```

### `r758-b.C1_gate_asked_before_the_acknowledgment`

the verb asks its gate without reading the backup acknowledgment first

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r758-b.json`, row `C1_gate_asked_before_the_acknowledgment`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 112 against a baseline of 112
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_resume_with_no_acknowledgment_refuses_before_anything_is_driven`
  - `tests/test_adopt_move.py::test_an_acknowledgment_out_of_its_window_refuses_before_the_gate`
  - `tests/test_adopt_move.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).
    session.assert_backup_acknowledged(cfg)

```

New text:

```
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).

```

### `r758-b.C3_rows_not_proven_against_the_digest`

the digest of the frozen rows is not taken again, so edited rows are shown and performed under the approved digest

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r758-b.json`, row `C3_rows_not_proven_against_the_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 112 against a baseline of 112
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_rows_under_a_digest_that_does_not_describe_them_are_never_shown`

Old text:

```
    if not (taken == stated == queued_under):
```

New text:

```
    if not (stated == queued_under):
```

### `r758-b.C5_a_sub_nobody_was_shown_is_removed`

a track filed in a further sub since the approval has that sub removed as well

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r758-b.json`, row `C5_a_sub_nobody_was_shown_is_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 112 against a baseline of 112
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_track_filed_somewhere_nobody_was_shown_is_a_stale_decision`

Old text:

```
        if set(now.remove) - set(move.remove):
            stale[move.content_id] = "it holds a sub nobody was shown"
            continue

```

New text:

```
(empty)
```

### `r758-b.C6_left_target_is_added_back`

a track approved as already in its target that has left it is added back and its other sub removed

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r758-b.json`, row `C6_left_target_is_added_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 112 against a baseline of 112
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_track_approved_as_in_its_target_that_left_it_is_a_stale_decision`

Old text:

```
        if now.add and not move.add:
            stale[move.content_id] = "it has left the sub it was approved as holding"
            continue

```

New text:

```
(empty)
```

### `r758-b.C9_read_back_is_not_the_verdict`

the job fails only when the writer raised, so tracks still in both subs drive it to succeeded

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r758-b.json`, row `C9_read_back_is_not_the_verdict`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 112 against a baseline of 112
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_removal_that_did_not_take_fails_the_job_though_nothing_raised`

Old text:

```
    if interrupted is not None or unfinished:
```

New text:

```
    if interrupted is not None:
```

### `r780-b.B1_reading_not_rechecked`

the worker does not ask whether the reading still names the approved target, so a track retagged since the approval is moved to a sub its file no longer names

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r780-b.json`, row `B1_reading_not_rechecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 112 against a baseline of 112
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_reading_that_changed_after_the_approval_is_a_stale_decision`
  - `tests/test_adopt_move.py::test_a_tree_path_move_is_checked_by_the_worker_in_the_bucket_it_names`

Old text:

```
        if move_engine.reading_target(entry, move.bucket, declared) != move.target:
            stale[move.content_id] = "its reading names another place"
            continue

```

New text:

```
(empty)
```

### `r780-b.B2_worker_asks_the_entry_bucket`

the worker asks the plan's rule of the entry's own bucket rather than the bucket the move names, so every tree path move is refused as one the plan does not make

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r780-b.json`, row `B2_worker_asks_the_entry_bucket`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 112 against a baseline of 112
- Kills: 18 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_failure_after_the_add_leaves_the_track_in_both_and_a_resume_finishes`
  - `tests/test_adopt_move.py::test_a_moved_track_can_be_moved_back_and_gets_a_live_row`
  - `tests/test_adopt_move.py::test_a_refusal_at_the_second_commit_keeps_its_own_cause_and_the_job_says_in_both`
  - `tests/test_adopt_move.py::test_a_removal_that_did_not_take_fails_the_job_though_nothing_raised`
  - `tests/test_adopt_move.py::test_a_removed_row_changes_its_marker_and_its_stamp_and_nothing_else`
  - `tests/test_adopt_move.py::test_a_second_approved_run_plans_nothing_and_writes_nothing`
  - `tests/test_adopt_move.py::test_a_track_filed_somewhere_nobody_was_shown_is_a_stale_decision`
  - `tests/test_adopt_move.py::test_a_tree_path_move_is_checked_by_the_worker_in_the_bucket_it_names`
  - `tests/test_adopt_move.py::test_a_verdict_on_another_bucket_keeps_the_tree_path_out_of_its_folder`
  - `tests/test_adopt_move.py::test_after_the_move_adoption_withholds_none_of_the_moved_tracks`
  - `tests/test_adopt_move.py::test_an_addition_never_lands_in_a_playlist_rekordbox_removed`
  - `tests/test_adopt_move.py::test_an_approved_move_adds_the_new_sub_and_removes_the_old`
  - `tests/test_adopt_move.py::test_an_approved_move_reads_no_vocals_in_its_gate_or_in_its_worker`
  - `tests/test_adopt_move.py::test_no_content_row_and_no_grid_column_is_written`
  - `tests/test_adopt_move.py::test_no_tempo_grid_cue_or_rating_value_differs_column_by_column`
  - ... and 3 more, see the JSON sidecar

Old text:

```
        now = move_engine.standing_in(
            entry, move.bucket, current.placements, declared, tree=current.tree, refused=refused
        )
```

New text:

```
        now = move_engine.standing(entry, current.placements, declared, tree=current.tree)
```

### `r780-b.B3_renamed_target_reads_as_done`

a track whose one place is its target through a renamed playlist reads as finished, which nobody was shown

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r780-b.json`, row `B3_renamed_target_reads_as_done`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 112 against a baseline of 112
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_target_held_only_under_another_name_is_not_done`

Old text:

```
            if held == {move.target} and not unnamed & held:
                continue
```

New text:

```
            if held == {move.target}:
                continue
```

### `r780-b.B4_gone_named_once_per_move`

a track gone from the collection is named once per move it carried, so the report lists it twice

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r780-b.json`, row `B4_gone_named_once_per_move`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 112 against a baseline of 112
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_one_track_carries_a_move_in_each_bucket_it_doubles_in`

Old text:

```
    return tuple(todo), tuple(sorted(gone))
```

New text:

```
    return tuple(todo), tuple(
        sorted(move.content_id for move in approved if move.content_id in gone)
    )
```

### `r780-b.B5_verdicts_not_handed_to_the_worker`

the worker asks the plan's rule with no refused bucket, so a move approved before a verdict landed is performed into the refused folder

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r780-b.json`, row `B5_verdicts_not_handed_to_the_worker`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 112 against a baseline of 112
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_verdict_on_another_bucket_keeps_the_tree_path_out_of_its_folder`

Old text:

```
    refused = move_engine.refused_buckets(current.entries)
```

New text:

```
    refused = frozenset()
```

### `r758-a.T2_first_commit_admits_a_removal`

the move's first commit admits a removal, so one slipped into the additions lands

- File: `src/cratekit/write/trees.py`
- Source: `r758-a.json`, row `T2_first_commit_admits_a_removal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 112 against a baseline of 112
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_the_moves_own_first_commit_refuses_a_removal`

Old text:

```
                    already_present += len(content_ids) - len(inserted)
                rb_writer.commit_guarded(db)
```

New text:

```
                    already_present += len(content_ids) - len(inserted)
                rb_writer.commit_guarded(db, removals=rb_writer.REMOVABLE_TABLES)
```

### `r758-a.T3_target_not_proven`

a removal is made whether or not the track sits in its target, so a track can end in neither

- File: `src/cratekit/write/trees.py`
- Source: `r758-a.json`, row `T3_target_not_proven`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 112 against a baseline of 112
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_track_not_in_its_target_has_nothing_removed`

Old text:

```
            if not places.holds(move.target, move.content_id):
                held_back.append(move.content_id)
                continue
```

New text:

```
(empty)
```

### `r758-a.T4_target_can_be_removed_from`

a move that names its own target among its removals takes the track out of the target

- File: `src/cratekit/write/trees.py`
- Source: `r758-a.json`, row `T4_target_can_be_removed_from`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 112 against a baseline of 112
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_the_target_is_never_removed_from_even_when_a_move_names_it`

Old text:

```
                if destination != move.target:
                    leaving.setdefault(destination, []).append(move.content_id)
```

New text:

```
                leaving.setdefault(destination, []).append(move.content_id)
```

### `r758-a.T5_dead_track_moved`

a track with no live collection row is moved like any other

- File: `src/cratekit/write/trees.py`
- Source: `r758-a.json`, row `T5_dead_track_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 112 against a baseline of 112
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_track_with_no_live_collection_row_is_skipped_whole`

Old text:

```
        live = [move for move in moves if _live_content(db, move.content_id)]
```

New text:

```
        live = list(moves)
```

### `r758-a.T6_removed_playlist_is_a_destination`

a playlist rekordbox removed answers for a destination, so an addition lands where nobody can see it

- File: `src/cratekit/write/trees.py`
- Source: `r758-a.json`, row `T6_removed_playlist_is_a_destination`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 112 against a baseline of 112
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_sub_held_only_through_a_removed_playlist_is_not_planned_for_removal`
  - `tests/test_adopt_move.py::test_an_addition_never_lands_in_a_playlist_rekordbox_removed`

Old text:

```
        and str(getattr(playlist, "ParentID", "")) in parents
        and not rb_writer.node_removed(playlist)
```

New text:

```
        and str(getattr(playlist, "ParentID", "")) in parents
```

### `r758-b.T7_refusal_read_as_an_interruption`

a refusal in the removals is raised as an interrupted move and loses its own cause and remedy

- File: `src/cratekit/write/trees.py`
- Source: `r758-b.json`, row `T7_refusal_read_as_an_interruption`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 112 against a baseline of 112
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_refusal_at_the_second_commit_keeps_its_own_cause_and_the_job_says_in_both`

Old text:

```
                if isinstance(exc, cause.CratekitError):
                    raise

```

New text:

```
(empty)
```

### `u154.G10_read_back_path_unchecked`

a row committed with a path other than the planned one is reported as shelved

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G10_read_back_path_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 43 against a baseline of 43
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_the_read_back_refuses_a_row_that_did_not_take_or_lost_a_column[path]`

Old text:

```
            if str(stored or "") != row.folder_path:

```

New text:

```
            if False:

```

### `u154.G11_kept_columns_unchecked`

a column the shelve does not own may change without the read back saying so

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G11_kept_columns_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 43 against a baseline of 43
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_the_read_back_refuses_a_row_that_did_not_take_or_lost_a_column[kept-column]`

Old text:

```
            if before.get(row.content_id) != after.get(row.content_id):

```

New text:

```
            if False:

```

### `u154.G14_reserved_folders_are_candidates`

the processed tree and the sets folder are planned as batches under --all

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G14_reserved_folders_are_candidates`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 43 against a baseline of 43
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_two_batches_filing_to_one_name_get_two_and_a_taken_target_is_passed_over`

Old text:

```
        if entry.name.startswith(".") or entry.name in reserved:

```

New text:

```
        if entry.name.startswith("."):

```

### `u154.G15_stored_target_under_mounted_path`

the confinement check reads under the mounted target and not the stored one

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G15_stored_target_under_mounted_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 43 against a baseline of 43
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_library_whose_drive_was_renamed_stores_and_confines_under_the_base_drive`

Old text:

```
            {"prefix": _like_prefix(one.stored_target)},

```

New text:

```
            {"prefix": _like_prefix(str(one.target))},

```

### `u154.G17_refusal_before_rename_rewrapped`

a stale plan refusal before any rename is rewrapped as a write failure

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G17_refusal_before_rename_rewrapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 43 against a baseline of 43
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_the_engine_refuses_a_target_made_between_its_plan_and_its_apply_in_its_own_words`

Old text:

```
            if not moved and isinstance(exc, CratekitError):

```

New text:

```
            if False:

```

### `u154.G1_policy_not_registered`

the path column is written with no field policy registered for the commit

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G1_policy_not_registered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 43 against a baseline of 43
- Kills: 11 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_batch_named_twice_is_planned_once`
  - `tests/test_intake_shelve.py::test_a_library_whose_drive_was_renamed_stores_and_confines_under_the_base_drive`
  - `tests/test_intake_shelve.py::test_a_row_under_a_folder_differing_only_in_case_is_not_this_plans_business`
  - `tests/test_intake_shelve.py::test_a_shelved_batch_name_stays_taken_so_a_landing_that_day_takes_the_next`
  - `tests/test_intake_shelve.py::test_a_target_free_on_disk_but_holding_rows_in_the_collection_is_passed_over`
  - `tests/test_intake_shelve.py::test_an_unreadable_session_record_makes_the_name_rule_refuse_rather_than_read_a_name_free`
  - `tests/test_intake_shelve.py::test_apply_moves_the_folder_rewrites_the_paths_and_keeps_every_other_column`
  - `tests/test_intake_shelve.py::test_nothing_under_the_processed_tree_is_touched_by_a_shelve`
  - `tests/test_intake_shelve.py::test_the_grid_suites_still_see_no_tempo_on_the_moved_rows`
  - `tests/test_intake_shelve.py::test_the_read_back_refuses_a_row_that_did_not_take_or_lost_a_column[kept-column]`
  - `tests/test_intake_shelve.py::test_the_read_back_refuses_a_row_that_did_not_take_or_lost_a_column[path]`

Old text:

```
            with rb_writer.field_policies_for_commit(rb_writer.SHELVE_POLICY):
                _assert_confined(db, plan)
                rb_writer.commit_guarded(db)

```

New text:

```
            if True:
                _assert_confined(db, plan)
                rb_writer.commit_guarded(db)

```

### `u154.G2_confinement_dropped`

the SQL confinement check is skipped before the commit

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G2_confinement_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 43 against a baseline of 43
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_row_under_the_target_that_the_plan_did_not_put_there_refuses_the_commit`

Old text:

```
                _assert_confined(db, plan)
                rb_writer.commit_guarded(db)

```

New text:

```
                rb_writer.commit_guarded(db)

```

### `u154.G3_rename_back_dropped`

a failure past the rename leaves the folder at its new name

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G3_rename_back_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 43 against a baseline of 43
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_commit_that_fails_after_the_rename_puts_the_folder_back`
  - `tests/test_intake_shelve.py::test_a_row_under_the_target_that_the_plan_did_not_put_there_refuses_the_commit`

Old text:

```
            failed = _rename_back(moved)

```

New text:

```
            failed: list[str] = []

```

### `u154.G4_stale_target_check_dropped`

a target made after the plan is renamed over at apply

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G4_stale_target_check_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 43 against a baseline of 43
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_the_engine_refuses_a_target_made_between_its_plan_and_its_apply_in_its_own_words`

Old text:

```
    if os.path.lexists(one.target):
        raise refuse(
            "decision-stale",
            f"{one.target} exists now and did not when the plan was made, so nothing "

```

New text:

```
    if False:
        raise refuse(
            "decision-stale",
            f"{one.target} exists now and did not when the plan was made, so nothing "

```

### `u154.G5_unmatched_file_shelved_anyway`

a batch with a file the collection does not hold is moved anyway

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G5_unmatched_file_shelved_anyway`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 43 against a baseline of 43
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_batch_whose_file_has_no_row_is_refused_whole_and_nothing_moves`

Old text:

```
        if unmatched is not None:
            leave(batch, _why_unmatched(*unmatched))
            continue

```

New text:

```
        if False:
            leave(batch, _why_unmatched(*unmatched))
            continue

```

### `u154.G6_subfolder_check_dropped`

a batch folder holding a subfolder is planned

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G6_subfolder_check_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 43 against a baseline of 43
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_folder_with_a_subfolder_and_a_name_of_neither_shape_are_skipped_under_all`

Old text:

```
        if any(entry.is_dir() for entry in folder.iterdir()):

```

New text:

```
        if False:

```

