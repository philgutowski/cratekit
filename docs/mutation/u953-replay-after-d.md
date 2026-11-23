# Mutation table: u953-replay-after-d

Measured by `scripts/mutate.py` on 2026-11-23 10:12 UTC, branch `HEAD` at `f8c593d5`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22473 collected. pytest invocations for this batch: 113.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-23 10:12 UTC for commit `f8c593d5f2a3`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 19, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22473 against 22473. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r647-a.B12_cross_boot_never_judged` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 4 | killed |
| `r647-a.B13_current_holder_names_no_machine` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 3 | killed |
| `r647-a.B14_machine_not_read_back` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 5 | killed |
| `r647-a.B15_machine_not_written` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 5 | killed |
| `r647-a.B1_unknown_machine_not_refused` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 1 | killed |
| `r647-a.B2_machine_equality_dropped` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 3 | killed |
| `r647-a.B3_unparsable_boot_read_as_gone` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 1 | killed |
| `r647-a.B4_infinite_boot_accepted` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 1 | killed |
| `r647-a.B5_drift_margin_halved` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 2 | killed |
| `r647-a.B6_drift_margin_doubled` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 1 | killed |
| `r647-a.B7_margin_boundary_exclusive` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 1 | killed |
| `r647-a.B8_direction_ignored` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 1 | killed |
| `r647-a.B9_platform_silence_read_as_gone` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 1 | killed |
| `u300.S13_process_exists_local` | `src/cratekit/core/session_holders.py` | maintainer | 2 file(s) | 185 | 1 | killed |
| `u49-author.L4_a_malformed_holder_raises_again` | `src/cratekit/core/session_holders.py` | user | 13 file(s) | 2567 | 1 | killed |
| `r44-a.S10_default_slug` | `src/cratekit/core/session_volumes.py` | maintainer | 2 file(s) | 479 | 1 | killed |
| `r44-a.S1_empty_slot` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 479 | 2 | killed |
| `r44-a.S2_proved_widened` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 479 | 4 | killed |
| `r44-a.S3_default_to_library` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 479 | 2 | killed |
| `r44-a.S4_inside_root_unheld` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 479 | 6 | killed |
| `r44-a.S5_not_destructive` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 479 | 5 | killed |
| `r44-a.S6_oserror_escapes` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 479 | 2 | killed |
| `r44-a.S7_probe_the_target` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 479 | 3 | killed |
| `r44-a.S8_wording_held_to` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 479 | 1 | killed |
| `r44-a.S9_offer_to_record_nested` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 479 | 1 | killed |
| `u300.S17_mapped_reasons_local` | `src/cratekit/core/session_volumes.py` | maintainer | 1 file(s) | 148 | 1 | killed |
| `r1665-b.S14_sources_unchecked_again` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 316 | 1 | killed |
| `r1665.S10_walk_before_empty` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 316 | 1 | killed |
| `r1665.S11_walk_skips_unreadable` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 316 | 1 | killed |
| `r1665.S12_verify_raises_passes` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 316 | 1 | killed |
| `r1665.S13_flush_before_check` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 316 | 10 | killed |
| `r1665.S15_recorded_before_the_copy_lands` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 316 | 72 | killed |
| `r1665.S1_guard_removed` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 316 | 8 | killed |
| `r1665.S2_guard_ignored` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 316 | 8 | killed |
| `r1665.S3_removal_unseen` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 316 | 4 | killed |
| `r1665.S4_rewrite_unseen` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 316 | 3 | killed |
| `r1665.S5_size_not_identity` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 316 | 1 | killed |
| `r1665.S6_mtime_not_identity` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 316 | 1 | killed |
| `r1665.S7_directories_unwalked` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 316 | 1 | killed |
| `r1665.S8_walk_after_fails_open` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 316 | 1 | killed |
| `r1665.S9_walk_before_fails_open` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 316 | 1 | killed |
| `r1677-b.C11_database_only` | `src/cratekit/core/snapshot.py` | user | 2 file(s) | 50 | 1 | killed |
| `r1677.C10_unreadable_passes` | `src/cratekit/core/snapshot.py` | user | 2 file(s) | 50 | 1 | killed |
| `r1677.C12_always_shared` | `src/cratekit/core/snapshot.py` | user | 3 file(s) | 73 | 1 | killed |
| `r1677.C13_no_temporary_directory_passes` | `src/cratekit/core/snapshot.py` | user | 2 file(s) | 50 | 1 | killed |
| `r1677.C1_no_measure` | `src/cratekit/core/snapshot.py` | user | 6 file(s) | 282 | 8 | killed |
| `r1677.C3_store_not_passed` | `src/cratekit/core/snapshot.py` | user | 4 file(s) | 98 | 2 | killed |
| `r1677.C4_sum_dropped` | `src/cratekit/core/snapshot.py` | user | 4 file(s) | 98 | 1 | killed |
| `r1677.C5_never_shared` | `src/cratekit/core/snapshot.py` | user | 4 file(s) | 98 | 3 | killed |
| `r1677.C6_unknown_is_separate` | `src/cratekit/core/snapshot.py` | user | 2 file(s) | 50 | 1 | killed |
| `r1677.C7_no_ancestor_walk` | `src/cratekit/core/snapshot.py` | user | 3 file(s) | 73 | 46 | killed |
| `r1677.C8_no_headroom` | `src/cratekit/core/snapshot.py` | user | 2 file(s) | 50 | 4 | killed |
| `r1677.C9_boundary` | `src/cratekit/core/snapshot.py` | user | 2 file(s) | 50 | 2 | killed |
| `r1677.K1_room_path_unrecorded` | `src/cratekit/core/snapshot.py` | user | 5 file(s) | 257 | 2 | killed |
| `r1677.K2_room_path_silent` | `src/cratekit/core/snapshot.py` | user | 5 file(s) | 257 | 3 | killed |
| `r1677.K3_other_copy_failure_verified` | `src/cratekit/core/snapshot.py` | user | 5 file(s) | 257 | 1 | killed |
| `r1677.N1_every_failure_is_room` | `src/cratekit/core/snapshot.py` | user | 2 file(s) | 56 | 4 | killed |
| `r1677.N2_quota_dropped` | `src/cratekit/core/snapshot.py` | user | 2 file(s) | 56 | 2 | killed |
| `r1677.V1_verify_swallows` | `src/cratekit/core/snapshot.py` | user | 4 file(s) | 98 | 3 | killed |
| `r1677.V2_verify_does_not_ask` | `src/cratekit/core/snapshot.py` | user | 4 file(s) | 98 | 2 | killed |
| `u272.E1_verified_ignores_verdict` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 641 | 11 | killed |
| `u272.E2_gate_trusts_manifest` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 641 | 9 | killed |
| `u272.S10_files_not_flushed` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 641 | 8 | killed |
| `u272.S11_directories_not_flushed` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 641 | 5 | killed |
| `u272.S12_store_not_flushed_first` | `src/cratekit/core/snapshot.py` | maintainer | 7 file(s) | 641 | 2 | killed |
| `u272.S14_wrong_slug` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 641 | 7 | killed |
| `u272.S15_wrong_remedy` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 641 | 5 | killed |
| `u272.S1_no_capture_flush` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 641 | 10 | killed |
| `u272.S2_manifest_before_flush` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 641 | 5 | killed |
| `u272.S3_swallow_early_failure` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 641 | 4 | killed |
| `u272.S4_swallow_late_failure` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 641 | 1 | killed |
| `u272.S5_no_late_flush` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 641 | 2 | killed |
| `u272.S6_failure_recorded_verified` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 641 | 6 | killed |
| `u272.S7_failure_not_recorded` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 641 | 6 | killed |
| `u272.S8_manifest_error_hides_refusal` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 641 | 1 | killed |
| `u272.S9_walk_skips_unreadable` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 641 | 1 | killed |
| `r431-a.A1_a_plain_row_gains_a_companion` | `src/cratekit/core/tombstone.py` | user | 6 file(s) | 1277 | 21 | killed |
| `r431-a.A2_one_kind_for_both` | `src/cratekit/core/tombstone.py` | user | 6 file(s) | 1277 | 17 | killed |
| `r1255.T1_tree_registry_clause` | `src/cratekit/core/tree_registry.py` | user | 3 file(s) | 119 | 2 | killed |
| `r235-a.M12_second_record_replaces` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 1 | killed |
| `r235-a.M13_snapshot_check_dropped` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 11 | killed |
| `r235-a.M1_unreadable_log_skipped` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 2 | killed |
| `r235-a.M2_margin_zero` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 1 | killed |
| `r235-a.M3_margin_two_days` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 1 | killed |
| `r235-a.M4_unparseable_start_predates` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 1 | killed |
| `r235-a.M5_updates_not_counted` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 1 | killed |
| `r235-a.M6_any_tree_counts` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 2 | killed |
| `r235-a.M7_zero_count_counts` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 2 | killed |
| `r235-a.M8_open_run_reverts` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 1 | killed |
| `r235-a.M9_library_guard_removed` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 4 | killed |
| `r235-b.M14_empty_export_accepted` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 1 | killed |
| `r501-a.T1_precheck_excusal` | `src/cratekit/core/tree_registry.py` | user | 5 file(s) | 134 | 4 | killed |
| `r787.S1_set_drops_intake` | `src/cratekit/core/tree_registry.py` | user | 20 file(s) | 2594 | 7 | killed |

## Row definitions

### `r647-a.B12_cross_boot_never_judged`

holder_alive: every other boot judged alive again, the state before this unit, so a power loss stays a dead end

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B12_cross_boot_never_judged`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[power-loss]`
  - `tests/test_write_session.py::test_a_boot_just_past_the_drift_margin_is_gone`
  - `tests/test_write_session.py::test_a_holder_from_an_earlier_boot_of_this_machine_is_gone`
  - `tests/test_write_session.py::test_the_lock_left_by_this_machines_earlier_boot_is_releasable`

Old text:

```
    if holder.boot != reference.boot:
        return not _gone_since_an_earlier_boot(holder, reference)
```

New text:

```
    if holder.boot != reference.boot:
        return True
```

### `r647-a.B13_current_holder_names_no_machine`

current_holder: record the declared unknown instead of the machine identity, so no holder is ever provably this machine's

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B13_current_holder_names_no_machine`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 3 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[power-loss]`
  - `tests/test_write_session.py::test_the_lock_left_by_this_machines_earlier_boot_is_releasable`
  - `tests/test_write_session.py::test_this_platform_names_its_machine_as_a_digest_not_the_serial`

Old text:

```
        machine=_session().machine_identity(),
```

New text:

```
        machine=UNKNOWN_IDENTITY,
```

### `r647-a.B14_machine_not_read_back`

Holder.from_json: ignore the recorded machine, so a record or lock read from disk never names one

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B14_machine_not_read_back`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 5 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[power-loss]`
  - `tests/test_session_cli.py::test_a_live_holders_claim_is_refused_and_the_lock_file_is_untouched`
  - `tests/test_write_session.py::test_the_holder_carries_all_five_identifying_fields`
  - `tests/test_write_session.py::test_the_lock_left_by_this_machines_earlier_boot_is_releasable`
  - `tests/test_write_session.py::test_the_record_names_the_holder_the_lock_names`

Old text:

```
            machine=str(data.get("machine", UNKNOWN_IDENTITY)),
```

New text:

```
            machine=UNKNOWN_IDENTITY,
```

### `r647-a.B15_machine_not_written`

Holder.to_json: omit the machine, so nothing on disk carries it

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B15_machine_not_written`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 5 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[power-loss]`
  - `tests/test_session_cli.py::test_a_live_holders_claim_is_refused_and_the_lock_file_is_untouched`
  - `tests/test_write_session.py::test_the_holder_carries_all_five_identifying_fields`
  - `tests/test_write_session.py::test_the_lock_left_by_this_machines_earlier_boot_is_releasable`
  - `tests/test_write_session.py::test_the_record_names_the_holder_the_lock_names`

Old text:

```
            "machine": self.machine,

```

New text:

```
(empty)
```

### `r647-a.B1_unknown_machine_not_refused`

_gone_since_an_earlier_boot: drop the unknown machine check, so two holders that both name no machine compare equal as text and a holder recorded before the field existed is cleared on a machine that cannot name itself

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B1_unknown_machine_not_refused`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_two_unknown_machine_identities_are_not_one_machine`

Old text:

```
    if UNKNOWN_IDENTITY in (holder.machine, reference.machine):
        return False
    if holder.machine != reference.machine:
```

New text:

```
    if holder.machine != reference.machine:
```

### `r647-a.B2_machine_equality_dropped`

_gone_since_an_earlier_boot: stop comparing machine identities, so another machine sharing the host name and the library drive has its claim cleared on the host name alone

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B2_machine_equality_dropped`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 3 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_record_not_proven_dead_on_this_machine_is_kept[another-machine-with-this-host-name]`
  - `tests/test_write_session.py::test_a_holder_from_another_boot_is_kept_without_proof_it_was_this_machine[another machine with this host name-changes0]`
  - `tests/test_write_session.py::test_the_lock_left_by_another_machine_with_this_host_name_is_not_releasable`

Old text:

```
    if holder.machine != reference.machine:
        return False
```

New text:

```
    if holder.machine is None:
        return False
```

### `r647-a.B3_unparsable_boot_read_as_gone`

_gone_since_an_earlier_boot: judge a boot that is not a number as proof of an earlier boot rather than as no proof

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B3_unparsable_boot_read_as_gone`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_holder_from_another_boot_is_kept_without_proof_it_was_this_machine[a boot that is not a number-changes5]`

Old text:

```
    except ValueError:
        return False
    if not math.isfinite(earlier_by)
```

New text:

```
    except ValueError:
        return process_exists(holder.pid) is False
    if not math.isfinite(earlier_by)
```

### `r647-a.B4_infinite_boot_accepted`

_gone_since_an_earlier_boot: drop the finiteness check, so a boot recorded as minus infinity reads as infinitely earlier

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B4_infinite_boot_accepted`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_holder_from_another_boot_is_kept_without_proof_it_was_this_machine[a boot that is not finite-changes6]`

Old text:

```
    if not math.isfinite(earlier_by) or earlier_by <= BOOT_DRIFT_SECONDS:
```

New text:

```
    if earlier_by <= BOOT_DRIFT_SECONDS:
```

### `r647-a.B5_drift_margin_halved`

BOOT_DRIFT_SECONDS: 60 to 30, a realistic nearby value, so a clock adjustment of forty seconds reads as a restart

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B5_drift_margin_halved`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 2 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_boot_just_past_the_drift_margin_is_gone`
  - `tests/test_write_session.py::test_a_holder_from_another_boot_is_kept_without_proof_it_was_this_machine[a boot exactly at the drift margin-changes3]`

Old text:

```
BOOT_DRIFT_SECONDS = 60.0
```

New text:

```
BOOT_DRIFT_SECONDS = 30.0
```

### `r647-a.B6_drift_margin_doubled`

BOOT_DRIFT_SECONDS: 60 to 120, so a restart a minute and a half apart is kept for no reason

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B6_drift_margin_doubled`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_boot_just_past_the_drift_margin_is_gone`

Old text:

```
BOOT_DRIFT_SECONDS = 60.0
```

New text:

```
BOOT_DRIFT_SECONDS = 120.0
```

### `r647-a.B7_margin_boundary_exclusive`

_gone_since_an_earlier_boot: less than instead of less than or equal, so a boot exactly at the margin is judged earlier

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B7_margin_boundary_exclusive`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_holder_from_another_boot_is_kept_without_proof_it_was_this_machine[a boot exactly at the drift margin-changes3]`

Old text:

```
earlier_by <= BOOT_DRIFT_SECONDS:
```

New text:

```
earlier_by < BOOT_DRIFT_SECONDS:
```

### `r647-a.B8_direction_ignored`

_gone_since_an_earlier_boot: take the distance between the boots rather than which came first, so a LATER boot reading reads as an earlier boot

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B8_direction_ignored`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_holder_from_another_boot_is_kept_without_proof_it_was_this_machine[a later boot-changes4]`

Old text:

```
        earlier_by = float(reference.boot) - float(holder.boot)
```

New text:

```
        earlier_by = abs(float(reference.boot) - float(holder.boot))
```

### `r647-a.B9_platform_silence_read_as_gone`

_gone_since_an_earlier_boot: read a platform declining to say whether the process exists as gone

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B9_platform_silence_read_as_gone`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_platform_that_cannot_say_whether_the_process_exists_keeps_it`

Old text:

```
    return _session().process_exists(holder.pid) is False
```

New text:

```
    return _session().process_exists(holder.pid) is not True
```

### `u300.S13_process_exists_local`

a holder's death since an earlier boot is judged by the part's own process_exists

- File: `src/cratekit/core/session_holders.py`
- Source: `u300.json`, row `S13_process_exists_local`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`
- Collected: 185 against a baseline of 185
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_platform_that_cannot_say_whether_the_process_exists_keeps_it`

Old text:

```
    return _session().process_exists(holder.pid) is False
```

New text:

```
    return process_exists(holder.pid) is False
```

### `u49-author.L4_a_malformed_holder_raises_again`

Remove the coercion guard from read_lock_holder, so a lock record with a non numeric pid escapes as a traceback rather than a typed refusal

- File: `src/cratekit/core/session_holders.py`
- Source: `u49-author.json`, row `L4_a_malformed_holder_raises_again`
- Moved: U953 merged read_lock_holder's JSON parse and holder coercion under one try, so narrowing its except to the parse error alone is the same removed coercion guard, the parse still answering None
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_session_cli.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 2567 against a baseline of 2567
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_lock_record_that_cannot_be_understood_refuses_by_name`

Old text:

```
    except (TypeError, ValueError, AttributeError):
```

New text:

```
    except json.JSONDecodeError:
```

### `r44-a.S10_default_slug`

Look the slug up with a default, so a verdict in neither table wears the mismatch slug

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S10_default_slug`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_volumes.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 479 against a baseline of 479
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_verdict_in_neither_table_fails_rather_than_wearing_the_mismatch_slug`

Old text:

```
            reason = _session()._MAPPED_REASONS[status.state]
```

New text:

```
            reason = _session()._MAPPED_REASONS.get(status.state, "mapped-volume-mismatch")
```

### `r44-a.S1_empty_slot`

Never refuse an empty mount slot, so an identity read through an ejected drive's leftover directory is compared and can match

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S1_empty_slot`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_volumes.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 479 against a baseline of 479
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

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S2_proved_widened`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_volumes.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 479 against a baseline of 479
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

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S3_default_to_library`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_volumes.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 479 against a baseline of 479
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

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S4_inside_root_unheld`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_volumes.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 479 against a baseline of 479
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

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S5_not_destructive`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_volumes.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 479 against a baseline of 479
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

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S6_oserror_escapes`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_volumes.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 479 against a baseline of 479
- Kills: 2 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_provider_that_cannot_read_the_identity_to_hand_over_is_a_refusal_too`
  - `tests/test_write_session.py::test_a_way_to_the_target_this_account_cannot_walk_is_a_refusal_and_not_a_traceback`

Old text:

```
    except OSError as exc:
        # Could not look is its own refusal, not an internal defect.
```

New text:

```
    except KeyboardInterrupt as exc:
        # Could not look is its own refusal, not an internal defect.
```

### `r44-a.S7_probe_the_target`

Probe the rule's target for a file instead of the file's own directory, so a volume nested under the target is never seen

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S7_probe_the_target`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_volumes.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 479 against a baseline of 479
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

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S8_wording_held_to`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_volumes.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 479 against a baseline of 479
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

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S9_offer_to_record_nested`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_volumes.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 479 against a baseline of 479
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

### `u300.S17_mapped_reasons_local`

the mapped volume gate reads the part's own reason table, so a patched table is not read

- File: `src/cratekit/core/session_volumes.py`
- Source: `u300.json`, row `S17_mapped_reasons_local`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`
- Collected: 148 against a baseline of 148
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_verdict_in_neither_table_fails_rather_than_wearing_the_mismatch_slug`

Old text:

```
            reason = _session()._MAPPED_REASONS[status.state]
```

New text:

```
            reason = _MAPPED_REASONS[status.state]
```

### `r1665-b.S14_sources_unchecked_again`

assert_sources_present: never refuse, measured again after the zero in r1665.md was given its test, so a restore accepts a capture missing files

- File: `src/cratekit/core/snapshot.py`
- Source: `r1665-b.json`, row `S14_sources_unchecked_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_wal_r1665.py::test_a_capture_that_lost_its_log_after_the_verdict_is_refused_by_the_plan[-wal]`

Old text:

```
    if not absent:
        return
    raise refuse(
```

New text:

```
    if True:
        return
    raise refuse(
```

### `r1665.S10_walk_before_empty`

capture: a walk before the check that fails answers an empty capture

- File: `src/cratekit/core/snapshot.py`
- Source: `r1665.json`, row `S10_walk_before_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_wal_r1665.py::test_a_capture_that_cannot_be_walked_around_its_check_is_not_recorded_verified[before]`

Old text:

```
        copied = None

```

New text:

```
        copied = {}

```

### `r1665.S11_walk_skips_unreadable`

_walked: let os.walk skip a directory it cannot read

- File: `src/cratekit/core/snapshot.py`
- Source: `r1665.json`, row `S11_walk_skips_unreadable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_wal_r1665.py::test_the_walk_raises_on_a_directory_it_cannot_read`

Old text:

```
    for current, directories, files in os.walk(capture_root, onerror=_raise_walk_error):
```

New text:

```
    for current, directories, files in os.walk(capture_root):
```

### `r1665.S12_verify_raises_passes`

_verify: a check that raises counts as passed

- File: `src/cratekit/core/snapshot.py`
- Source: `r1665.json`, row `S12_verify_raises_passes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot.py::test_a_verifier_that_raises_counts_as_not_having_verified`

Old text:

```
        logger.warning("the capture integrity check could not run, so it did not pass: %s", exc)
        return False
```

New text:

```
        logger.warning("the capture integrity check could not run, so it did not pass: %s", exc)
        return True
```

### `r1665.S13_flush_before_check`

capture: flush nothing after the check, the U272 order

- File: `src/cratekit/core/snapshot.py`
- Source: `r1665.json`, row `S13_flush_before_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 10 (killed)
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_a_capture_outside_the_configured_store_is_flushed_too`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[a companion file]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[a coupled file]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[the database]`
  - `tests/test_snapshot_flush_u272.py::test_a_flush_that_fails_after_the_manifest_leaves_it_saying_not_verified`
  - `tests/test_snapshot_flush_u272.py::test_a_manifest_that_cannot_be_written_after_a_failed_flush_still_refuses`
  - `tests/test_snapshot_flush_u272.py::test_an_unverified_capture_is_flushed_in_the_same_order`
  - `tests/test_snapshot_flush_u272.py::test_every_file_a_capture_holds_is_flushed_before_its_manifest_by_walking`
  - `tests/test_snapshot_flush_u272.py::test_the_copy_its_companions_and_its_directories_reach_the_disk_before_the_manifest`
  - `tests/test_snapshot_flush_u272.py::test_the_flush_follows_the_check_so_what_the_check_leaves_is_flushed`

Old text:

```
    try:
        _flush(destination, destination_root)
    except OSError as exc:
        raise _not_flushed(record, manifest, exc) from exc

    _write_manifest(record, manifest)
```

New text:

```
    _write_manifest(record, manifest)
```

### `r1665.S15_recorded_before_the_copy_lands`

capture: record a companion as captured whether or not it landed

- File: `src/cratekit/core/snapshot.py`
- Source: `r1665.json`, row `S15_recorded_before_the_copy_lands`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 72 (killed)
- Killed:
  - `tests/test_restore.py::test_a_capture_whose_manifest_names_a_path_outside_the_set_is_refused`
  - `tests/test_restore.py::test_a_coupled_file_the_capture_records_as_absent_is_removed_again`
  - `tests/test_restore.py::test_a_dry_run_and_a_real_run_walk_the_same_list_in_the_same_order`
  - `tests/test_restore.py::test_a_held_session_used_after_its_block_is_refused`
  - `tests/test_restore.py::test_a_later_session_that_committed_nothing_does_not_need_an_override`
  - `tests/test_restore.py::test_a_plan_built_before_a_later_commit_is_refused_at_run`
  - `tests/test_restore.py::test_a_pre_cutover_restore_leaves_the_next_session_refused`
  - `tests/test_restore.py::test_a_rehearsal_never_clears_the_live_companion_files`
  - `tests/test_restore.py::test_a_rehearsal_reports_what_is_outstanding_rather_than_what_it_recorded`
  - `tests/test_restore.py::test_a_restore_lists_every_effect_it_cannot_undo_and_blocks_convergence`
  - `tests/test_restore.py::test_a_restore_predating_a_cutover_marks_that_tree_unconverged`
  - `tests/test_restore.py::test_a_restore_refuses_while_rekordbox_holds_the_database`
  - `tests/test_restore.py::test_a_restore_replaces_exactly_the_derived_coupled_set`
  - `tests/test_restore.py::test_a_restore_returns_a_modified_database_to_its_pre_session_bytes`
  - `tests/test_restore.py::test_a_restore_returns_the_coupled_state_with_the_database`
  - ... and 57 more, see the JSON sidecar

Old text:

```
                source=path, captured=landed if landed.exists() else None, directory=False
```

New text:

```
                source=path, captured=landed, directory=False
```

### `r1665.S1_guard_removed`

capture: never ask whether the check changed the capture

- File: `src/cratekit/core/snapshot.py`
- Source: `r1665.json`, row `S1_guard_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 8 (killed)
- Killed:
  - `tests/test_snapshot_wal_r1665.py::test_a_capture_that_cannot_be_walked_around_its_check_is_not_recorded_verified[after]`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_removes_a_captured_companion_is_not_recorded_verified[-shm]`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_removes_a_captured_companion_is_not_recorded_verified[-wal]`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_removes_a_captured_coupled_file_is_not_recorded_verified`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_removes_an_empty_captured_directory_is_not_recorded_verified`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_resizes_the_database_at_its_own_time_is_not_recorded_verified`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_rewrites_the_captured_database_is_not_recorded_verified`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_rewrites_the_database_at_its_own_size_is_not_recorded_verified`

Old text:

```
    if verdict and copied is not None:
        changed
```

New text:

```
    if False:
        changed
```

### `r1665.S2_guard_ignored`

capture: log what the check changed and keep the verdict

- File: `src/cratekit/core/snapshot.py`
- Source: `r1665.json`, row `S2_guard_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 8 (killed)
- Killed:
  - `tests/test_snapshot_wal_r1665.py::test_a_capture_that_cannot_be_walked_around_its_check_is_not_recorded_verified[after]`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_removes_a_captured_companion_is_not_recorded_verified[-shm]`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_removes_a_captured_companion_is_not_recorded_verified[-wal]`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_removes_a_captured_coupled_file_is_not_recorded_verified`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_removes_an_empty_captured_directory_is_not_recorded_verified`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_resizes_the_database_at_its_own_time_is_not_recorded_verified`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_rewrites_the_captured_database_is_not_recorded_verified`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_rewrites_the_database_at_its_own_size_is_not_recorded_verified`

Old text:

```
                "; ".join(changed[:20]),
            )
            verdict = False
```

New text:

```
                "; ".join(changed[:20]),
            )
            verdict = verdict
```

### `r1665.S3_removal_unseen`

_changed_by_the_check: a removed entry is not a change

- File: `src/cratekit/core/snapshot.py`
- Source: `r1665.json`, row `S3_removal_unseen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 4 (killed)
- Killed:
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_removes_a_captured_companion_is_not_recorded_verified[-shm]`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_removes_a_captured_companion_is_not_recorded_verified[-wal]`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_removes_a_captured_coupled_file_is_not_recorded_verified`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_removes_an_empty_captured_directory_is_not_recorded_verified`

Old text:

```
            changed.append(f"{path} was removed")
```

New text:

```
            pass
```

### `r1665.S4_rewrite_unseen`

_changed_by_the_check: a rewritten entry is not a change

- File: `src/cratekit/core/snapshot.py`
- Source: `r1665.json`, row `S4_rewrite_unseen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 3 (killed)
- Killed:
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_resizes_the_database_at_its_own_time_is_not_recorded_verified`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_rewrites_the_captured_database_is_not_recorded_verified`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_rewrites_the_database_at_its_own_size_is_not_recorded_verified`

Old text:

```
        elif after[path] != identity:
```

New text:

```
        elif False:
```

### `r1665.S5_size_not_identity`

_walked: identify a file by its modification time alone

- File: `src/cratekit/core/snapshot.py`
- Source: `r1665.json`, row `S5_size_not_identity`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_resizes_the_database_at_its_own_time_is_not_recorded_verified`

Old text:

```
(status.st_size, status.st_mtime_ns)
```

New text:

```
(0, status.st_mtime_ns)
```

### `r1665.S6_mtime_not_identity`

_walked: identify a file by its size alone

- File: `src/cratekit/core/snapshot.py`
- Source: `r1665.json`, row `S6_mtime_not_identity`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_rewrites_the_database_at_its_own_size_is_not_recorded_verified`

Old text:

```
(status.st_size, status.st_mtime_ns)
```

New text:

```
(status.st_size, 0)
```

### `r1665.S7_directories_unwalked`

_walked: record no directory

- File: `src/cratekit/core/snapshot.py`
- Source: `r1665.json`, row `S7_directories_unwalked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_removes_an_empty_captured_directory_is_not_recorded_verified`

Old text:

```
            found[here / name] = None

```

New text:

```
            pass

```

### `r1665.S8_walk_after_fails_open`

_changed_by_the_check: a walk after the check that fails answers no change

- File: `src/cratekit/core/snapshot.py`
- Source: `r1665.json`, row `S8_walk_after_fails_open`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_wal_r1665.py::test_a_capture_that_cannot_be_walked_around_its_check_is_not_recorded_verified[after]`

Old text:

```
        return [f"the capture could not be walked again: {exc}"]
```

New text:

```
        return []
```

### `r1665.S9_walk_before_fails_open`

capture: verify although the walk before the check failed

- File: `src/cratekit/core/snapshot.py`
- Source: `r1665.json`, row `S9_walk_before_fails_open`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_wal_r1665.py::test_a_capture_that_cannot_be_walked_around_its_check_is_not_recorded_verified[before]`

Old text:

```
        if record.database is not None and copied is not None

```

New text:

```
        if record.database is not None

```

### `r1677-b.C11_database_only`

assert_room_for_check: measure the database alone, leaving out its companions and the playlist file the copy takes

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677-b.json`, row `C11_database_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_check_room_r1677.py::test_the_measure_counts_every_file_the_check_copies_not_the_database_alone`

Old text:

```
    needed = sum(_allocated_size(member) for member in rb_writer.file_set(database))
```

New text:

```
    needed = _allocated_size(Path(database))
```

### `r1677.C10_unreadable_passes`

assert_room_for_check: a volume that will not report its room passes rather than refusing

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677.json`, row `C10_unreadable_passes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_check_room_r1677.py::test_a_temporary_volume_that_will_not_report_its_room_refuses`

Old text:

```
    if available is None:
        raise refuse(
            "snapshot-check-temp-full",
            f"the free space on the volume holding the temporary directory {scratch} "
```

New text:

```
    if available is None:
        return needed
        raise refuse(
            "snapshot-check-temp-full",
            f"the free space on the volume holding the temporary directory {scratch} "
```

### `r1677.C12_always_shared`

_same_volume: answer shared for any two paths, so a separate temporary volume is asked for the capture's room too

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677.json`, row `C12_always_shared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot.py`, `tests/test_snapshot_wal_r1665.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_check_room_r1677.py::test_two_volumes_with_different_devices_are_separate`

Old text:

```
        return _device(Path(first)) == _device(Path(second))
```

New text:

```
        return True
```

### `r1677.C13_no_temporary_directory_passes`

assert_room_for_check: no temporary directory at all passes the measure, so the capture is taken and left unverified

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677.json`, row `C13_no_temporary_directory_passes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_check_room_r1677.py::test_no_temporary_directory_at_all_refuses_before_anything_is_written`

Old text:

```
        scratch = rb_writer.disposable_root()
    except OSError as exc:
        raise refuse(
```

New text:

```
        scratch = rb_writer.disposable_root()
    except OSError as exc:
        return 0
        raise refuse(
```

### `r1677.C1_no_measure`

capture: never measure the throwaway's room, so a full temporary volume reads as a failed check again (the card's defect)

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677.json`, row `C1_no_measure`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_restore.py`, `tests/test_intake_land_rehearse.py`
- Collected: 282 against a baseline of 282
- Kills: 8 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_no_room_for_the_check_refuses_before_its_copy`
  - `tests/test_snapshot_check_room_r1677.py::test_a_temporary_volume_shared_with_the_store_must_hold_both`
  - `tests/test_snapshot_check_room_r1677.py::test_a_temporary_volume_that_will_not_report_its_room_refuses`
  - `tests/test_snapshot_check_room_r1677.py::test_a_temporary_volume_too_small_for_the_check_refuses_before_anything_is_written`
  - `tests/test_snapshot_check_room_r1677.py::test_no_temporary_directory_at_all_refuses_before_anything_is_written`
  - `tests/test_snapshot_check_room_r1677.py::test_one_byte_short_on_the_temporary_volume_refuses`
  - `tests/test_snapshot_check_room_r1677.py::test_the_measure_counts_every_file_the_check_copies_not_the_database_alone`
  - `tests/test_snapshot_check_room_r1677.py::test_the_room_refusal_is_a_precondition_not_a_defect`

Old text:

```
    if verifier is None:
        assert_room_for_check(database_paths(cfg)[0], store=(destination_root, estimate))
```

New text:

```
    if False:
        assert_room_for_check(database_paths(cfg)[0], store=(destination_root, estimate))
```

### `r1677.C3_store_not_passed`

capture: measure the throwaway without the store, so a shared volume is asked for the throwaway alone

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677.json`, row `C3_store_not_passed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_intake_land_rehearse.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_no_room_for_the_check_refuses_before_its_copy`
  - `tests/test_snapshot_check_room_r1677.py::test_a_temporary_volume_shared_with_the_store_must_hold_both`

Old text:

```
        assert_room_for_check(database_paths(cfg)[0], store=(destination_root, estimate))
```

New text:

```
        assert_room_for_check(database_paths(cfg)[0], store=None)
```

### `r1677.C4_sum_dropped`

assert_room_for_check: never add the capture's estimate on a shared volume

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677.json`, row `C4_sum_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_intake_land_rehearse.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_check_room_r1677.py::test_a_temporary_volume_shared_with_the_store_must_hold_both`

Old text:

```
    total = needed + (store[1] if store is not None and shared else 0)
```

New text:

```
    total = needed
```

### `r1677.C5_never_shared`

_same_volume: answer separate for any two paths

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677.json`, row `C5_never_shared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_intake_land_rehearse.py`
- Collected: 98 against a baseline of 98
- Kills: 3 (killed)
- Killed:
  - `tests/test_snapshot_check_room_r1677.py::test_a_volume_whose_device_cannot_be_read_counts_as_shared`
  - `tests/test_snapshot_check_room_r1677.py::test_the_store_and_the_temporary_directory_on_this_disk_are_one_volume`
  - `tests/test_snapshot_check_room_r1677.py::test_two_volumes_with_different_devices_are_separate`

Old text:

```
        return _device(Path(first)) == _device(Path(second))
```

New text:

```
        return False
```

### `r1677.C6_unknown_is_separate`

_same_volume: an unreadable device counts as separate, the direction that asks for less room

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677.json`, row `C6_unknown_is_separate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_check_room_r1677.py::test_a_volume_whose_device_cannot_be_read_counts_as_shared`

Old text:

```
        return _device(Path(first)) == _device(Path(second))
    except OSError:
        return True
```

New text:

```
        return _device(Path(first)) == _device(Path(second))
    except OSError:
        return False
```

### `r1677.C7_no_ancestor_walk`

_device: stat the path itself, so a store not yet made has no device and counts as shared

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677.json`, row `C7_no_ancestor_walk`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot.py`, `tests/test_snapshot_wal_r1665.py`
- Collected: 73 against a baseline of 73
- Kills: 46 (killed)
- Killed:
  - `tests/test_snapshot.py::test_a_capture_is_a_snapshot_directory_as_far_as_pruning_is_concerned`
  - `tests/test_snapshot.py::test_a_capture_that_verifies_is_the_only_one_anything_may_commit_behind`
  - `tests/test_snapshot.py::test_a_manifest_from_a_later_build_is_refused_rather_than_guessed_at`
  - `tests/test_snapshot.py::test_a_missing_database_refuses_in_the_library_class_rather_than_crashing`
  - `tests/test_snapshot.py::test_a_verifier_that_raises_counts_as_not_having_verified`
  - `tests/test_snapshot.py::test_a_world_readable_source_does_not_produce_a_world_readable_capture`
  - `tests/test_snapshot.py::test_an_absent_source_is_recorded_as_absent_rather_than_failing`
  - `tests/test_snapshot.py::test_an_unreadable_manifest_refuses_rather_than_reporting_an_empty_capture`
  - `tests/test_snapshot.py::test_every_declared_source_appears_in_the_capture_record`
  - `tests/test_snapshot.py::test_every_file_and_directory_in_a_capture_is_private_under_any_umask`
  - `tests/test_snapshot.py::test_the_capture_store_is_never_captured_by_a_capture`
  - `tests/test_snapshot.py::test_the_database_and_the_coupled_directory_land_under_one_stamp`
  - `tests/test_snapshot.py::test_the_files_the_engine_keeps_beside_the_database_travel_with_it`
  - `tests/test_snapshot.py::test_the_verdict_survives_a_round_trip_through_the_manifest`
  - `tests/test_snapshot.py::test_writing_a_second_capture_into_an_existing_stamp_refuses`
  - ... and 31 more, see the JSON sidecar

Old text:

```
    while not probe.exists() and probe.parent != probe:
```

New text:

```
    while False:
```

### `r1677.C8_no_headroom`

assert_room_for_check: require the bare estimate, without the capture's headroom

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677.json`, row `C8_no_headroom`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot.py`
- Collected: 50 against a baseline of 50
- Kills: 4 (killed)
- Killed:
  - `tests/test_snapshot_check_room_r1677.py::test_a_temporary_volume_shared_with_the_store_must_hold_both`
  - `tests/test_snapshot_check_room_r1677.py::test_a_temporary_volume_too_small_for_the_check_refuses_before_anything_is_written`
  - `tests/test_snapshot_check_room_r1677.py::test_one_byte_short_on_the_temporary_volume_refuses`
  - `tests/test_snapshot_check_room_r1677.py::test_the_measure_counts_every_file_the_check_copies_not_the_database_alone`

Old text:

```
    available = free_bytes if free_bytes is not None else _free_bytes(scratch)
    required = int(total * headroom)
```

New text:

```
    available = free_bytes if free_bytes is not None else _free_bytes(scratch)
    required = int(total)
```

### `r1677.C9_boundary`

assert_room_for_check: refuse exactly enough room, the boundary moved by one

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677.json`, row `C9_boundary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot.py`
- Collected: 50 against a baseline of 50
- Kills: 2 (killed)
- Killed:
  - `tests/test_snapshot_check_room_r1677.py::test_a_shared_volume_with_room_for_both_captures_verified`
  - `tests/test_snapshot_check_room_r1677.py::test_exactly_enough_room_on_the_temporary_volume_captures_verified`

Old text:

```
    if available >= required:
        return needed
    sharing = (
```

New text:

```
    if available > required:
        return needed
    sharing = (
```

### `r1677.K1_room_path_unrecorded`

capture: refuse for no room without first rewriting the manifest unverified

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677.json`, row `K1_room_path_unrecorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_restore.py`
- Collected: 257 against a baseline of 257
- Kills: 2 (killed)
- Killed:
  - `tests/test_snapshot_check_room_r1677.py::test_a_check_whose_copy_runs_out_of_room_is_refused_and_recorded_unverified[no-space]`
  - `tests/test_snapshot_check_room_r1677.py::test_a_check_whose_copy_runs_out_of_room_is_refused_and_recorded_unverified[quota]`

Old text:

```
            _record_unverified(record, manifest)
            raise no_room from failed
```

New text:

```
            raise no_room from failed
```

### `r1677.K2_room_path_silent`

capture: a copy with no room is a plain unverified capture, not refused under the room slug

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677.json`, row `K2_room_path_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_restore.py`
- Collected: 257 against a baseline of 257
- Kills: 3 (killed)
- Killed:
  - `tests/test_snapshot_check_room_r1677.py::test_a_check_whose_copy_runs_out_of_room_is_refused_and_recorded_unverified[no-space]`
  - `tests/test_snapshot_check_room_r1677.py::test_a_check_whose_copy_runs_out_of_room_is_refused_and_recorded_unverified[quota]`
  - `tests/test_snapshot_check_room_r1677.py::test_a_stand_in_verifier_raising_the_copy_failure_is_refused_under_the_room_slug`

Old text:

```
            _record_unverified(record, manifest)
            raise no_room from failed
```

New text:

```
            verdict = False
```

### `r1677.K3_other_copy_failure_verified`

capture: a copy that failed for another reason is recorded VERIFIED, the merge blocker the card names

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677.json`, row `K3_other_copy_failure_verified`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_restore.py`
- Collected: 257 against a baseline of 257
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_check_room_r1677.py::test_a_check_whose_copy_fails_for_another_reason_is_unverified_not_a_room_message`

Old text:

```
        logger.warning("the capture integrity check could not run, so it did not pass: %s", failed)
        verdict = False
```

New text:

```
        logger.warning("the capture integrity check could not run, so it did not pass: %s", failed)
        verdict = True
```

### `r1677.N1_every_failure_is_room`

check_had_no_room: read every copy failure as no room, so a permission error is told as a full volume

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677.json`, row `N1_every_failure_is_room`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_intake_land_rehearse.py`
- Collected: 56 against a baseline of 56
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_failed_integrity_check_is_refused_naming_the_area[its copy otherwise]`
  - `tests/test_snapshot_check_room_r1677.py::test_a_check_whose_copy_fails_for_another_reason_is_unverified_not_a_room_message`
  - `tests/test_snapshot_check_room_r1677.py::test_only_a_full_volume_or_quota_is_read_as_no_room[13-False]`
  - `tests/test_snapshot_check_room_r1677.py::test_only_a_full_volume_or_quota_is_read_as_no_room[5-False]`

Old text:

```
    if code not in _NO_ROOM_ERRNOS:
        return None
```

New text:

```
    if False:
        return None
```

### `r1677.N2_quota_dropped`

_NO_ROOM_ERRNOS: leave out a reached quota, so it is a plain unverified capture

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677.json`, row `N2_quota_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_intake_land_rehearse.py`
- Collected: 56 against a baseline of 56
- Kills: 2 (killed)
- Killed:
  - `tests/test_snapshot_check_room_r1677.py::test_a_check_whose_copy_runs_out_of_room_is_refused_and_recorded_unverified[quota]`
  - `tests/test_snapshot_check_room_r1677.py::test_only_a_full_volume_or_quota_is_read_as_no_room[122-True]`

Old text:

```
    code for code in (errno.ENOSPC, getattr(errno, "EDQUOT", None)) if code is not None
```

New text:

```
    code for code in (errno.ENOSPC,) if code is not None
```

### `r1677.V1_verify_swallows`

_verify: let the copy failure fall into the catch all, so it is a plain unverified capture again

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677.json`, row `V1_verify_swallows`
- Moved: Text anchored again by U300, which replayed it as written here and kept the kill in u300-replay-after-c.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`
- Collected: 98 against a baseline of 98
- Kills: 3 (killed)
- Killed:
  - `tests/test_snapshot_check_room_r1677.py::test_a_check_whose_copy_runs_out_of_room_is_refused_and_recorded_unverified[no-space]`
  - `tests/test_snapshot_check_room_r1677.py::test_a_check_whose_copy_runs_out_of_room_is_refused_and_recorded_unverified[quota]`
  - `tests/test_snapshot_check_room_r1677.py::test_a_stand_in_verifier_raising_the_copy_failure_is_refused_under_the_room_slug`

Old text:

```
    except rb_writer.IntegrityCheckCopyFailed:
        # No verdict at all, which the capture names (R-1677).
        raise
```

New text:

```
    except rb_writer.IntegrityCheckCopyFailed:
        return False
```

### `r1677.V2_verify_does_not_ask`

_verify: call the real check without asking for the copy failure, so a full volume answers False

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677.json`, row `V2_verify_does_not_ask`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_snapshot_check_room_r1677.py::test_a_check_whose_copy_runs_out_of_room_is_refused_and_recorded_unverified[no-space]`
  - `tests/test_snapshot_check_room_r1677.py::test_a_check_whose_copy_runs_out_of_room_is_refused_and_recorded_unverified[quota]`

Old text:

```
            return bool(rb_writer.integrity_ok(database, raise_copy_failure=True))
```

New text:

```
            return bool(rb_writer.integrity_ok(database, raise_copy_failure=False))
```

### `u272.E1_verified_ignores_verdict`

existing guard sample, Capture.verified: true whenever a database was captured, whatever the verdict

- File: `src/cratekit/core/snapshot.py`
- Source: `u272.json`, row `E1_verified_ignores_verdict`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 641 against a baseline of 641
- Kills: 11 (killed)
- Killed:
  - `tests/test_restore.py::test_a_capture_that_failed_its_integrity_check_is_never_restored_from`
  - `tests/test_snapshot.py::test_a_capture_that_verifies_is_the_only_one_anything_may_commit_behind`
  - `tests/test_snapshot.py::test_a_verifier_that_raises_counts_as_not_having_verified`
  - `tests/test_snapshot.py::test_the_verdict_survives_a_round_trip_through_the_manifest`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[a companion file]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[a coupled file]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[the capture directory]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[the database]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[the store]`
  - `tests/test_snapshot_flush_u272.py::test_an_unverified_capture_is_flushed_in_the_same_order`
  - `tests/test_write_session.py::test_a_capture_that_failed_its_check_blocks_the_commit_behind_it`

Old text:

```
        return self.database is not None and self.integrity_verified
```

New text:

```
        return self.database is not None
```

### `u272.E2_gate_trusts_manifest`

existing guard sample, assert_verified: pass whenever the database file is there

- File: `src/cratekit/core/snapshot.py`
- Source: `u272.json`, row `E2_gate_trusts_manifest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 641 against a baseline of 641
- Kills: 9 (killed)
- Killed:
  - `tests/test_restore.py::test_a_capture_that_failed_its_integrity_check_is_never_restored_from`
  - `tests/test_snapshot.py::test_a_capture_that_verifies_is_the_only_one_anything_may_commit_behind`
  - `tests/test_snapshot.py::test_a_verifier_that_raises_counts_as_not_having_verified`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[a companion file]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[a coupled file]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[the capture directory]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[the database]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[the store]`
  - `tests/test_write_session.py::test_a_capture_that_failed_its_check_blocks_the_commit_behind_it`

Old text:

```
    if record.verified and record.database is not None and record.database.exists():
```

New text:

```
    if record.database is not None and record.database.exists():
```

### `u272.S10_files_not_flushed`

_flush: flush the directories and none of the files

- File: `src/cratekit/core/snapshot.py`
- Source: `u272.json`, row `S10_files_not_flushed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 641 against a baseline of 641
- Kills: 8 (killed)
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_a_capture_outside_the_configured_store_is_flushed_too`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[a companion file]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[a coupled file]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[the database]`
  - `tests/test_snapshot_flush_u272.py::test_an_unverified_capture_is_flushed_in_the_same_order`
  - `tests/test_snapshot_flush_u272.py::test_every_file_a_capture_holds_is_flushed_before_its_manifest_by_walking`
  - `tests/test_snapshot_flush_u272.py::test_the_copy_its_companions_and_its_directories_reach_the_disk_before_the_manifest`
  - `tests/test_snapshot_flush_u272.py::test_the_flush_follows_the_check_so_what_the_check_leaves_is_flushed`

Old text:

```
        for name in files:
            config.flush_to_disk(here / name)
```

New text:

```
        for name in files:
            pass
```

### `u272.S11_directories_not_flushed`

_flush: flush the files and none of the directories under the store

- File: `src/cratekit/core/snapshot.py`
- Source: `u272.json`, row `S11_directories_not_flushed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 641 against a baseline of 641
- Kills: 5 (killed)
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_a_flush_that_fails_after_the_manifest_leaves_it_saying_not_verified`
  - `tests/test_snapshot_flush_u272.py::test_a_manifest_that_cannot_be_written_after_a_failed_flush_still_refuses`
  - `tests/test_snapshot_flush_u272.py::test_an_unverified_capture_is_flushed_in_the_same_order`
  - `tests/test_snapshot_flush_u272.py::test_every_file_a_capture_holds_is_flushed_before_its_manifest_by_walking`
  - `tests/test_snapshot_flush_u272.py::test_the_copy_its_companions_and_its_directories_reach_the_disk_before_the_manifest`

Old text:

```
            config.flush_to_disk(here / name)
        config.flush_to_disk(here)
```

New text:

```
            config.flush_to_disk(here / name)
```

### `u272.S12_store_not_flushed_first`

_flush: leave the store out of the flush before the manifest

- File: `src/cratekit/core/snapshot.py`
- Source: `u272.json`, row `S12_store_not_flushed_first`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 641 against a baseline of 641
- Kills: 2 (killed)
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_a_capture_outside_the_configured_store_is_flushed_too`
  - `tests/test_snapshot_flush_u272.py::test_the_copy_its_companions_and_its_directories_reach_the_disk_before_the_manifest`

Old text:

```
        config.flush_to_disk(here)
    config.flush_to_disk(store)
```

New text:

```
        config.flush_to_disk(here)
```

### `u272.S14_wrong_slug`

_not_flushed: refuse under internal-error rather than the integrity slug the gate uses

- File: `src/cratekit/core/snapshot.py`
- Source: `u272.json`, row `S14_wrong_slug`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 641 against a baseline of 641
- Kills: 7 (killed)
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[a companion file]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[a coupled file]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[the capture directory]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[the database]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[the store]`
  - `tests/test_snapshot_flush_u272.py::test_a_flush_that_fails_after_the_manifest_leaves_it_saying_not_verified`
  - `tests/test_snapshot_flush_u272.py::test_a_manifest_that_cannot_be_written_after_a_failed_flush_still_refuses`

Old text:

```
    return refuse(
        "snapshot-integrity-failed",
        f"the capture at {record.root} could not be flushed
```

New text:

```
    return refuse(
        "internal-error",
        f"the capture at {record.root} could not be flushed
```

### `u272.S15_wrong_remedy`

_not_flushed: tell the person to report a defect rather than to check the library drive

- File: `src/cratekit/core/snapshot.py`
- Source: `u272.json`, row `S15_wrong_remedy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 641 against a baseline of 641
- Kills: 5 (killed)
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[a companion file]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[a coupled file]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[the capture directory]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[the database]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[the store]`

Old text:

```
        remedy=Remedy.MOUNT_LIBRARY_VOLUME,
        scope=Scope.SESSION,
        detail={
            "stamp": record.stamp,
            "root": str(record.root),
            "path"
```

New text:

```
        remedy=Remedy.REPORT_DEFECT,
        scope=Scope.SESSION,
        detail={
            "stamp": record.stamp,
            "root": str(record.root),
            "path"
```

### `u272.S1_no_capture_flush`

capture: skip the walk and flush before the manifest

- File: `src/cratekit/core/snapshot.py`
- Source: `u272.json`, row `S1_no_capture_flush`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 641 against a baseline of 641
- Kills: 10 (killed)
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_a_capture_outside_the_configured_store_is_flushed_too`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[a companion file]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[a coupled file]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[the database]`
  - `tests/test_snapshot_flush_u272.py::test_a_flush_that_fails_after_the_manifest_leaves_it_saying_not_verified`
  - `tests/test_snapshot_flush_u272.py::test_a_manifest_that_cannot_be_written_after_a_failed_flush_still_refuses`
  - `tests/test_snapshot_flush_u272.py::test_an_unverified_capture_is_flushed_in_the_same_order`
  - `tests/test_snapshot_flush_u272.py::test_every_file_a_capture_holds_is_flushed_before_its_manifest_by_walking`
  - `tests/test_snapshot_flush_u272.py::test_the_copy_its_companions_and_its_directories_reach_the_disk_before_the_manifest`
  - `tests/test_snapshot_flush_u272.py::test_the_flush_follows_the_check_so_what_the_check_leaves_is_flushed`

Old text:

```
        _flush(destination, destination_root)
    except OSError as exc:
```

New text:

```
        pass
    except OSError as exc:
```

### `u272.S2_manifest_before_flush`

capture: write the manifest before the copy is flushed

- File: `src/cratekit/core/snapshot.py`
- Source: `u272.json`, row `S2_manifest_before_flush`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 641 against a baseline of 641
- Kills: 5 (killed)
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_a_capture_outside_the_configured_store_is_flushed_too`
  - `tests/test_snapshot_flush_u272.py::test_an_unverified_capture_is_flushed_in_the_same_order`
  - `tests/test_snapshot_flush_u272.py::test_every_file_a_capture_holds_is_flushed_before_its_manifest_by_walking`
  - `tests/test_snapshot_flush_u272.py::test_the_copy_its_companions_and_its_directories_reach_the_disk_before_the_manifest`
  - `tests/test_snapshot_flush_u272.py::test_the_flush_follows_the_check_so_what_the_check_leaves_is_flushed`

Old text:

```
        _flush(destination, destination_root)
    except OSError as exc:
        raise _not_flushed(record, manifest, exc) from exc

    _write_manifest(record, manifest)
```

New text:

```
        _write_manifest(record, manifest)
        _flush(destination, destination_root)
    except OSError as exc:
        raise _not_flushed(record, manifest, exc) from exc
```

### `u272.S3_swallow_early_failure`

capture: swallow a flush failure before the manifest and record the verdict as it stood

- File: `src/cratekit/core/snapshot.py`
- Source: `u272.json`, row `S3_swallow_early_failure`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 641 against a baseline of 641
- Kills: 4 (killed)
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[a companion file]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[a coupled file]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[the database]`
  - `tests/test_snapshot_flush_u272.py::test_a_manifest_that_cannot_be_written_after_a_failed_flush_still_refuses`

Old text:

```
        _flush(destination, destination_root)
    except OSError as exc:
        raise _not_flushed(record, manifest, exc) from exc
```

New text:

```
        _flush(destination, destination_root)
    except OSError as exc:
        pass
```

### `u272.S4_swallow_late_failure`

capture: swallow a flush failure after the manifest

- File: `src/cratekit/core/snapshot.py`
- Source: `u272.json`, row `S4_swallow_late_failure`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 641 against a baseline of 641
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_a_flush_that_fails_after_the_manifest_leaves_it_saying_not_verified`

Old text:

```
        config.flush_to_disk(destination_root)
    except OSError as exc:
        raise _not_flushed(record, manifest, exc) from exc
```

New text:

```
        config.flush_to_disk(destination_root)
    except OSError as exc:
        pass
```

### `u272.S5_no_late_flush`

capture: drop the flush of the capture directory and the store after the manifest

- File: `src/cratekit/core/snapshot.py`
- Source: `u272.json`, row `S5_no_late_flush`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 641 against a baseline of 641
- Kills: 2 (killed)
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_a_flush_that_fails_after_the_manifest_leaves_it_saying_not_verified`
  - `tests/test_snapshot_flush_u272.py::test_the_manifest_is_followed_by_a_flush_of_the_directory_that_holds_it`

Old text:

```
    try:
        config.flush_to_disk(destination)
        config.flush_to_disk(destination_root)
    except
```

New text:

```
    try:
        pass
    except
```

### `u272.S6_failure_recorded_verified`

_not_flushed: rewrite the manifest with the verdict as it stood, so a failed flush can say verified

- File: `src/cratekit/core/snapshot.py`
- Source: `u272.json`, row `S6_failure_recorded_verified`
- Moved: U953 built _record_unverified's manifest with replace on the record, so keeping its own verdict there is the same failed flush written as it stood
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 641 against a baseline of 641
- Kills: 6 (killed)
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[a companion file]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[a coupled file]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[the capture directory]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[the database]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[the store]`
  - `tests/test_snapshot_flush_u272.py::test_a_flush_that_fails_after_the_manifest_leaves_it_saying_not_verified`

Old text:

```
        _write_manifest(replace(record, integrity_verified=False), manifest)
```

New text:

```
        _write_manifest(replace(record, integrity_verified=record.integrity_verified), manifest)
```

### `u272.S7_failure_not_recorded`

_not_flushed: refuse without writing the unverified manifest

- File: `src/cratekit/core/snapshot.py`
- Source: `u272.json`, row `S7_failure_not_recorded`
- Moved: U953 built _record_unverified's manifest with replace inside the write call, so replacing that call with pass is the same unverified manifest never written
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 641 against a baseline of 641
- Kills: 6 (killed)
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[a companion file]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[a coupled file]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[the capture directory]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[the database]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[the store]`
  - `tests/test_snapshot_flush_u272.py::test_a_flush_that_fails_after_the_manifest_leaves_it_saying_not_verified`

Old text:

```
        _write_manifest(replace(record, integrity_verified=False), manifest)
    except OSError as written:
```

New text:

```
        pass
    except OSError as written:
```

### `u272.S8_manifest_error_hides_refusal`

_not_flushed: let a failed manifest write escape in place of the refusal

- File: `src/cratekit/core/snapshot.py`
- Source: `u272.json`, row `S8_manifest_error_hides_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 641 against a baseline of 641
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_a_manifest_that_cannot_be_written_after_a_failed_flush_still_refuses`

Old text:

```
    except OSError as written:
        logger.warning(
```

New text:

```
    except OSError as written:
        raise
        logger.warning(
```

### `u272.S9_walk_skips_unreadable`

_flush: let os.walk skip a directory it cannot read

- File: `src/cratekit/core/snapshot.py`
- Source: `u272.json`, row `S9_walk_skips_unreadable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 641 against a baseline of 641
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_a_capture_directory_the_walk_cannot_read_raises_rather_than_being_skipped`

Old text:

```
capture_root, topdown=False, onerror=_raise_walk_error
```

New text:

```
capture_root, topdown=False, onerror=None
```

### `r431-a.A1_a_plain_row_gains_a_companion`

uncredited_title answers the stripped title even when nothing was stripped, so a plain deletion writes a companion

- File: `src/cratekit/core/tombstone.py`
- Source: `r431-a.json`, row `A1_a_plain_row_gains_a_companion`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_deletion.py`, `tests/test_label_workers.py`, `tests/test_match_states.py`, `tests/test_tombstones.py`, `tests/test_uncredited_tombstone.py`
- Collected: 1277 against a baseline of 1277
- Kills: 21 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_confirmed_removal_the_person_deleted_in_the_finder_does_not_block_the_next_one`
  - `tests/test_deletion.py::test_a_file_moved_by_hand_after_the_confirmation_is_recorded_rather_than_retired_silently`
  - `tests/test_deletion.py::test_a_listing_says_which_suppressions_moved_no_file`
  - `tests/test_deletion.py::test_a_run_interrupted_after_trashing_resumes_without_re_offering`
  - `tests/test_deletion.py::test_a_tombstone_that_cannot_be_written_puts_the_file_back`
  - `tests/test_deletion.py::test_an_interrupt_during_the_store_write_still_puts_the_file_back[ctrl-c]`
  - `tests/test_deletion.py::test_an_interrupt_during_the_store_write_still_puts_the_file_back[sigterm]`
  - `tests/test_deletion.py::test_one_file_deleted_by_hand_under_a_healthy_anchor_is_still_settled`
  - `tests/test_deletion.py::test_the_listing_carries_the_column_value_a_missed_tombstone_was_built_from`
  - `tests/test_deletion.py::test_tombstone_list_revokes_and_then_shows_the_lifted_record`
  - `tests/test_deletion.py::test_tombstone_list_shows_what_the_deletion_pass_suppressed`
  - `tests/test_match_states.py::test_a_deletion_of_the_plain_record_writes_no_companion`
  - `tests/test_match_states.py::test_the_two_copies_of_the_tombstone_identity_agree_once_both_exist`
  - `tests/test_tombstones.py::test_a_revoked_tombstone_stays_listable_so_the_two_cases_can_be_told_apart`
  - `tests/test_uncredited_tombstone.py::test_a_credited_deletion_is_two_records_and_a_plain_one_is_one`
  - ... and 6 more, see the JSON sidecar

Old text:

```
    return stripped if dropped else ""
```

New text:

```
    return stripped
```

### `r431-a.A2_one_kind_for_both`

The companion is recorded under the tombstone's own kind, where every verbatim lookup lands on it

- File: `src/cratekit/core/tombstone.py`
- Source: `r431-a.json`, row `A2_one_kind_for_both`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_deletion.py`, `tests/test_label_workers.py`, `tests/test_match_states.py`, `tests/test_tombstones.py`, `tests/test_uncredited_tombstone.py`
- Collected: 1277 against a baseline of 1277
- Kills: 17 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_held_file_crediting_somebody_else_never_calls_the_companion_stale`
  - `tests/test_match_states.py::test_the_two_copies_of_the_tombstone_identity_agree_once_both_exist`
  - `tests/test_uncredited_tombstone.py::test_a_companion_already_lifted_keeps_the_lift_it_was_given`
  - `tests/test_uncredited_tombstone.py::test_a_companion_is_never_the_answer_to_a_verbatim_lookup`
  - `tests/test_uncredited_tombstone.py::test_a_companion_lifted_alone_does_not_come_back_behind_a_persons_back`
  - `tests/test_uncredited_tombstone.py::test_a_companion_never_says_a_run_recorded_a_different_rows_deletion`
  - `tests/test_uncredited_tombstone.py::test_a_companion_two_deletions_share_outlives_the_first_lift_and_not_the_second`
  - `tests/test_uncredited_tombstone.py::test_a_credited_deletion_is_two_records_and_a_plain_one_is_one`
  - `tests/test_uncredited_tombstone.py::test_a_second_deletion_leaves_the_shared_companion_exactly_as_it_stood`
  - `tests/test_uncredited_tombstone.py::test_a_shared_companion_survives_a_lift_even_when_the_stripping_rule_has_moved`
  - `tests/test_uncredited_tombstone.py::test_a_tombstone_with_no_pointer_still_accounts_for_the_companion_it_strips_to`
  - `tests/test_uncredited_tombstone.py::test_deleting_again_after_a_full_lift_suppresses_both_halves_again`
  - `tests/test_uncredited_tombstone.py::test_lifting_a_credited_tombstone_lifts_its_companion`
  - `tests/test_uncredited_tombstone.py::test_lifting_a_plain_tombstone_touches_no_companion_it_does_not_own`
  - `tests/test_uncredited_tombstone.py::test_lifting_the_companion_alone_leaves_the_tombstone_standing`
  - ... and 2 more, see the JSON sidecar

Old text:

```
KIND_VERSION_UNCREDITED = "version-uncredited"
```

New text:

```
KIND_VERSION_UNCREDITED = "version"
```

### `r1255.T1_tree_registry_clause`

tree_registry._whole_log: word the refusal with the old count, not the clause

- File: `src/cratekit/core/tree_registry.py`
- Source: `r1255.json`, row `T1_tree_registry_clause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_tree_registry.py`, `tests/test_cutover_precheck.py`
- Collected: 119 against a baseline of 119
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_an_unreadable_record_keeps_its_own_refusal`
  - `tests/test_session_log_unlisted.py::test_every_gate_refuses_a_log_it_cannot_list[open-None-<lambda>-readable2-so whether a run is still open was not established]`

Old text:

```
            f"{session.unread_clause(unreadable, cfg)}, so {so}; refusing rather than "
```

New text:

```
            f"the session log holds {len(unreadable)} entries this build cannot read, so {so}; refusing rather than "
```

### `r235-a.M12_second_record_replaces`

record_cutover replaces a tree already recorded native instead of refusing

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M12_second_record_replaces`
- Moved: Text anchored again by U300, which replayed it as written here and kept the kill in u300-replay-after-d.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_a_tree_already_recorded_is_not_recorded_again`

Old text:

```
        if standing is not None and standing.mode == Mode.DATABASE:
            # Asked under the lock, so two cutovers of one tree cannot both pass.
```

New text:

```
        if False:
            # Asked under the lock, so two cutovers of one tree cannot both pass.
```

### `r235-a.M13_snapshot_check_dropped`

the verified snapshot check is no longer in the precheck table

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M13_snapshot_check_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 11 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_each_precheck_failure_refuses_before_anything_is_recorded[_leave_intake_xml-cutover-xml-pending-no-pending-intake-xml]`
  - `tests/test_cutover_cli.py::test_each_precheck_failure_refuses_before_anything_is_recorded[_open_a_run-cutover-open-run-no-open-run]`
  - `tests/test_cutover_cli.py::test_each_precheck_failure_refuses_before_anything_is_recorded[_remove_the_export-cutover-export-missing-fresh-export]`
  - `tests/test_cutover_cli.py::test_each_precheck_failure_refuses_before_anything_is_recorded[_remove_the_snapshot-cutover-snapshot-missing-verified-snapshot]`
  - `tests/test_cutover_cli.py::test_the_plan_names_the_root_and_approval_records_that_tree_alone`
  - `tests/test_cutover_cli.py::test_two_failing_prechecks_are_both_named_on_one_run`
  - `tests/test_cutover_precheck.py::test_a_missing_snapshot_blocks_the_flip`
  - `tests/test_cutover_precheck.py::test_an_unverified_capture_does_not_count_as_a_snapshot`
  - `tests/test_cutover_precheck.py::test_the_report_and_the_assertion_refuse_with_one_cause`
  - `tests/test_cutover_precheck.py::test_the_report_carries_each_refusal_and_does_not_stop_at_the_first`
  - `tests/test_cutover_precheck.py::test_the_report_names_every_check_in_the_order_the_assertion_refuses`

Old text:

```
    ("fresh-export", _export_refusal),
    ("verified-snapshot", _snapshot_refusal),
)
```

New text:

```
    ("fresh-export", _export_refusal),
)
```

### `r235-a.M1_unreadable_log_skipped`

the registry gates no longer refuse on a session record they cannot read, so a torn record reads as no open run and no native write

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M1_unreadable_log_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 2 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_a_record_nobody_can_read_refuses_the_flip_rather_than_reading_as_no_open_run`
  - `tests/test_cutover_precheck.py::test_a_record_nobody_can_read_refuses_the_revert_rather_than_reading_as_no_write`

Old text:

```
    parsed, unreadable = session.scan_log(cfg)
    if unreadable:
```

New text:

```
    parsed, unreadable = session.scan_log(cfg)
    if False:
```

### `r235-a.M2_margin_zero`

the native write margin is no days, so a write whose universal time date is the day before the cutover day is left out

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M2_margin_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_a_write_that_cannot_be_shown_to_predate_the_cutover_counts[2026-07-31T23:50:00Z]`

Old text:

```
NATIVE_WRITE_MARGIN = timedelta(days=1)
```

New text:

```
NATIVE_WRITE_MARGIN = timedelta(days=0)
```

### `r235-a.M3_margin_two_days`

the native write margin is two days, so a write two days before the cutover day still counts

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M3_margin_two_days`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_the_day_before_the_margin_is_the_first_day_left_out`

Old text:

```
NATIVE_WRITE_MARGIN = timedelta(days=1)
```

New text:

```
NATIVE_WRITE_MARGIN = timedelta(days=2)
```

### `r235-a.M4_unparseable_start_predates`

a session start nothing can parse is read as before the cutover, so its write does not count

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M4_unparseable_start_predates`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_a_write_that_cannot_be_shown_to_predate_the_cutover_counts[not a timestamp]`

Old text:

```
    except ValueError:
        return False
    return began < cutover_on - NATIVE_WRITE_MARGIN
```

New text:

```
    except ValueError:
        return True
    return began < cutover_on - NATIVE_WRITE_MARGIN
```

### `r235-a.M5_updates_not_counted`

only a creation counts as a native write, an update does not

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M5_updates_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_an_update_counts_as_a_native_write_as_a_creation_does`

Old text:

```
            change.tree == tree_id and (change.created > 0 or change.updated > 0)
```

New text:

```
            change.tree == tree_id and change.created > 0
```

### `r235-a.M6_any_tree_counts`

a write to any tree counts as a write to this one

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M6_any_tree_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 2 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_a_write_to_another_tree_does_not_close_this_trees_door`
  - `tests/test_cutover_precheck.py::test_a_session_that_wrote_nothing_to_this_tree_leaves_the_revert_open`

Old text:

```
            change.tree == tree_id and (change.created > 0 or change.updated > 0)
```

New text:

```
            (change.created > 0 or change.updated > 0)
```

### `r235-a.M7_zero_count_counts`

a record naming the tree with nothing added counts as a native write

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M7_zero_count_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 2 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_a_write_to_another_tree_does_not_close_this_trees_door`
  - `tests/test_cutover_precheck.py::test_a_session_that_wrote_nothing_to_this_tree_leaves_the_revert_open`

Old text:

```
            change.tree == tree_id and (change.created > 0 or change.updated > 0)
```

New text:

```
            change.tree == tree_id
```

### `r235-a.M8_open_run_reverts`

a revert no longer refuses over an open run

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M8_open_run_reverts`
- Moved: U953 folded this module's refuse calls into the _refuse builder, so the open run test of assert_revertible now guards raise _refuse and disabling it is the same revert over an open run
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_an_open_run_refuses_the_revert_because_it_may_have_written`

Old text:

```
    if open_runs:
        raise _refuse(
            "cutover-open-run",
```

New text:

```
    if False:
        raise _refuse(
            "cutover-open-run",
```

### `r235-a.M9_library_guard_removed`

revert_cutover no longer asserts the tree is revertible, leaving only the verb's own check

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M9_library_guard_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 4 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_a_record_nobody_can_read_refuses_the_revert_rather_than_reading_as_no_write`
  - `tests/test_cutover_precheck.py::test_a_revert_after_a_native_write_is_refused_by_the_library_itself`
  - `tests/test_cutover_precheck.py::test_an_open_run_refuses_the_revert_because_it_may_have_written`
  - `tests/test_cutover_precheck.py::test_the_revert_holds_the_session_lock_while_it_asks_and_writes`

Old text:

```
        assert_revertible(cfg, tree_id)
        updated = read(cfg).without_record(tree_id)
```

New text:

```
        updated = read(cfg).without_record(tree_id)
```

### `r235-b.M14_empty_export_accepted`

an export of no bytes passes the fresh export check

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-b.json`, row `M14_empty_export_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_an_empty_export_is_no_export`

Old text:

```
    if export_path.is_file() and export_path.stat().st_size != 0:
```

New text:

```
    if export_path.is_file():
```

### `r501-a.T1_precheck_excusal`

tree_registry.assert_cutover_ready: drop the excusal, so a proven landing refuses the cutover for ever, which is R-501 itself

- File: `src/cratekit/core/tree_registry.py`
- Source: `r501-a.json`, row `T1_precheck_excusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 134 against a baseline of 134
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

### `r787.S1_set_drops_intake`

cutover_trees returns the routing tree alone, the list doctor held before R-787

- File: `src/cratekit/core/tree_registry.py`
- Source: `r787.json`, row `S1_set_drops_intake`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_intake_imported.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_landing_labels.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_tree_registry.py`, `tests/test_tree_writer.py`, `tests/test_xml_import_coexistence.py`, `tests/test_xml_splice_golden.py`
- Collected: 2594 against a baseline of 2594
- Kills: 7 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_a_tree_the_taxonomy_does_not_declare_is_refused`
  - `tests/test_cutover_cli.py::test_doctor_and_the_verb_read_one_set_of_cutover_trees`
  - `tests/test_cutover_cli.py::test_doctor_fails_on_a_native_record_the_cutover_would_refuse_to_create`
  - `tests/test_cutover_cli.py::test_doctor_reads_a_native_inbox_record_as_ok`
  - `tests/test_cutover_cli.py::test_doctor_reads_an_inbox_the_verb_cut_over_as_ok`
  - `tests/test_cutover_cli.py::test_the_catalogue_tree_is_refused_as_not_rebuildable`
  - `tests/test_cutover_cli.py::test_the_intake_tree_cuts_over_on_the_same_answer_as_the_routing_tree`

Old text:

```
    return frozenset({declared.tree.id, declared.intake.id})
```

New text:

```
    return frozenset({declared.tree.id})
```

