# Mutation table: u300-replay-before-c

Measured by `scripts/mutate.py` on 2026-11-22 16:55 UTC, branch `HEAD` at `8b809bd2`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 107.

Full baseline: measured by this driver (the battery's verdict was not read: no battery verdict at `.cloud-battery/verdict.json`).

Subset baselines: 13, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `/tmp/claude-0/-home-user-cratekit/1ecf30c5-f7fd-5fce-ae99-6064133b5c9c/scratchpad/known-failures-replay.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r1665.R1_log_not_restored` | `src/cratekit/core/restore.py` | user | 7 file(s) | 327 | 4 | killed |
| `r592-a.A1_occupancy_guard_removed` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 3 | killed |
| `r592-a.A2_database_dropped_from_fileset` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 3 | killed |
| `r592-a.A3_companions_dropped_from_fileset` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 2 | killed |
| `r592-a.A4_fileset_not_rebased` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 4 | killed |
| `r592-a.A5_replacing_existing_inverted` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 8 | killed |
| `r592-a.A6_old_suffix_rule_restored` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 2 | killed |
| `r592-a.A7_companion_suffix_wrong` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 2 | killed |
| `r592-a.A8_sample_stub_check_beside` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 2 | killed |
| `u27-restore-cli-independent.X6_the_rekordbox_guard_itself_is_neutered` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 1 | killed |
| `u95-a.A1_never_rerooted` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 7 | killed |
| `u95-a.A2_library_sessions_rerooted_too` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 2 | killed |
| `u95-a.A3_database_not_carried` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 4 | killed |
| `u95-a.A4_outside_database_refusal_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 1 | killed |
| `u95-a.A5_capture_path_not_rebased` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 2 | killed |
| `u95-a.A6_manifest_not_rebased_in_plan` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 3 | killed |
| `u95-a.A7_manifest_not_rebased_in_preflight` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 1 | killed |
| `u95-a.A8_run_not_rooted` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 1 | killed |
| `u95-b.B2_manifest_database_not_moved` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 2 | killed |
| `u95-b.B3_sources_not_moved` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 3 | killed |
| `u95-b.B4_captured_not_moved` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 2 | killed |
| `u95-b.B5_not_idempotent` | `src/cratekit/core/restore.py` | maintainer | 3 file(s) | 498 | 1 | killed |
| `u95-b.B6_recorded_path_not_normalised` | `src/cratekit/core/restore.py` | maintainer | 3 file(s) | 498 | 1 | killed |
| `u95-b.B8_outside_path_moved_anyway` | `src/cratekit/core/restore.py` | maintainer | 3 file(s) | 498 | 2 | killed |
| `u95-b1.B1_manifest_root_not_moved` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 1 | killed |
| `u95-c.C1_plan_side_guard_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 1 | killed |
| `u95-c.C2_run_side_guard_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 7 | killed |
| `u95-c.C3_step_authorisation_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 2 | killed |
| `u95-c.C4_restorable_membership_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 1 | killed |
| `u95-c.C5_staging_authorisation_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 2 | killed |
| `u95-c.C6_staging_store_rule_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 3 | killed |
| `u95-c.C7_staging_store_itself_admitted` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 1 | killed |
| `u95-c.C8_plan_root_assertion_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 1 | killed |
| `u95-c.S1_authorises_everything` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 7 | killed |
| `u95-c.S2_issued_terms_not_compared` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 1 | killed |
| `u96-b.C1_engine_terminal` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 2 | killed |
| `u96-b.C2_engine_acknowledged` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 3 | killed |
| `u96-b.C3_engine_occupied_target` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 3 | killed |
| `u96-b.C4_engine_stub` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 5 | killed |
| `u96-b.C5_engine_library_is_mounted` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 3 | killed |
| `r1665-b.S14_sources_unchecked_again` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 327 | 1 | killed |
| `r1665.S10_walk_before_empty` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 327 | 1 | killed |
| `r1665.S11_walk_skips_unreadable` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 327 | 1 | killed |
| `r1665.S12_verify_raises_passes` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 327 | 1 | killed |
| `r1665.S13_flush_before_check` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 327 | 10 | killed |
| `r1665.S15_recorded_before_the_copy_lands` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 327 | 66 | killed |
| `r1665.S1_guard_removed` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 327 | 8 | killed |
| `r1665.S2_guard_ignored` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 327 | 8 | killed |
| `r1665.S3_removal_unseen` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 327 | 4 | killed |
| `r1665.S4_rewrite_unseen` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 327 | 3 | killed |
| `r1665.S5_size_not_identity` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 327 | 1 | killed |
| `r1665.S6_mtime_not_identity` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 327 | 1 | killed |
| `r1665.S7_directories_unwalked` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 327 | 1 | killed |
| `r1665.S8_walk_after_fails_open` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 327 | 1 | killed |
| `r1665.S9_walk_before_fails_open` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 327 | 1 | killed |
| `r1677-b.C11_database_only` | `src/cratekit/core/snapshot.py` | user | 2 file(s) | 50 | 1 | killed |
| `r1677.C10_unreadable_passes` | `src/cratekit/core/snapshot.py` | user | 2 file(s) | 50 | 1 | killed |
| `r1677.C12_always_shared` | `src/cratekit/core/snapshot.py` | user | 3 file(s) | 73 | 1 | killed |
| `r1677.C13_no_temporary_directory_passes` | `src/cratekit/core/snapshot.py` | user | 2 file(s) | 50 | 1 | killed |
| `r1677.C1_no_measure` | `src/cratekit/core/snapshot.py` | user | 6 file(s) | 293 | 8 | killed |
| `r1677.C3_store_not_passed` | `src/cratekit/core/snapshot.py` | user | 4 file(s) | 109 | 2 | killed |
| `r1677.C4_sum_dropped` | `src/cratekit/core/snapshot.py` | user | 4 file(s) | 109 | 1 | killed |
| `r1677.C5_never_shared` | `src/cratekit/core/snapshot.py` | user | 4 file(s) | 109 | 3 | killed |
| `r1677.C6_unknown_is_separate` | `src/cratekit/core/snapshot.py` | user | 2 file(s) | 50 | 1 | killed |
| `r1677.C7_no_ancestor_walk` | `src/cratekit/core/snapshot.py` | user | 3 file(s) | 73 | 1 | killed |
| `r1677.C8_no_headroom` | `src/cratekit/core/snapshot.py` | user | 2 file(s) | 50 | 4 | killed |
| `r1677.C9_boundary` | `src/cratekit/core/snapshot.py` | user | 2 file(s) | 50 | 2 | killed |
| `r1677.K1_room_path_unrecorded` | `src/cratekit/core/snapshot.py` | user | 5 file(s) | 257 | 2 | killed |
| `r1677.K2_room_path_silent` | `src/cratekit/core/snapshot.py` | user | 5 file(s) | 257 | 3 | killed |
| `r1677.K3_other_copy_failure_verified` | `src/cratekit/core/snapshot.py` | user | 5 file(s) | 257 | 1 | killed |
| `r1677.N1_every_failure_is_room` | `src/cratekit/core/snapshot.py` | user | 2 file(s) | 67 | 4 | killed |
| `r1677.N2_quota_dropped` | `src/cratekit/core/snapshot.py` | user | 2 file(s) | 67 | 2 | killed |
| `r1677.V1_verify_swallows` | `src/cratekit/core/snapshot.py` | user | 4 file(s) | 98 | 3 | killed |
| `r1677.V2_verify_does_not_ask` | `src/cratekit/core/snapshot.py` | user | 4 file(s) | 98 | 2 | killed |
| `u272.E1_verified_ignores_verdict` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 630 | 11 | killed |
| `u272.E2_gate_trusts_manifest` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 630 | 9 | killed |
| `u272.S10_files_not_flushed` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 630 | 8 | killed |
| `u272.S11_directories_not_flushed` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 630 | 5 | killed |
| `u272.S12_store_not_flushed_first` | `src/cratekit/core/snapshot.py` | maintainer | 7 file(s) | 630 | 2 | killed |
| `u272.S13_parents_before_children` | `src/cratekit/core/snapshot.py` | maintainer | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u272.S14_wrong_slug` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 630 | 7 | killed |
| `u272.S15_wrong_remedy` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 630 | 5 | killed |
| `u272.S1_no_capture_flush` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 630 | 10 | killed |
| `u272.S2_manifest_before_flush` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 630 | 5 | killed |
| `u272.S3_swallow_early_failure` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 630 | 4 | killed |
| `u272.S4_swallow_late_failure` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 630 | 1 | killed |
| `u272.S5_no_late_flush` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 630 | 2 | killed |
| `u272.S6_failure_recorded_verified` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 630 | 6 | killed |
| `u272.S7_failure_not_recorded` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 630 | 6 | killed |
| `u272.S8_manifest_error_hides_refusal` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 630 | 1 | killed |
| `u272.S9_walk_skips_unreadable` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 630 | 1 | killed |

## Zero rows and what they owe

- `u272.S13_parents_before_children` (maintainer facing): maintainer facing, composite not required

## Row definitions

### `r1665.R1_log_not_restored`

restore._file_steps: never write back a restored companion, so the log's rows are lost

- File: `src/cratekit/core/restore.py`
- Source: `r1665.json`, row `R1_log_not_restored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 327 against a baseline of 327
- Kills: 4 (killed)
- Killed:
  - `tests/test_restore.py::test_only_the_companion_the_inventory_declares_restored_is_written_back`
  - `tests/test_restore.py::test_round3_a_staged_log_is_counted_as_permanent_growth`
  - `tests/test_restore.py::test_round3_a_volume_between_the_two_rules_is_refused`
  - `tests/test_snapshot_wal_r1665.py::test_a_capture_taken_while_a_handle_holds_the_log_restores_what_it_recorded`

Old text:

```
        if entry.source in restored_companions:
            if entry.captured is not None:
```

New text:

```
        if entry.source in restored_companions:
            if False:
```

### `r592-a.A1_occupancy_guard_removed`

assert_recovery_target: find nothing occupied whatever the target holds, so a library whose database sits where this one lands is replaced unasked

- File: `src/cratekit/core/restore.py`
- Source: `r592-a.json`, row `A1_occupancy_guard_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 257 against a baseline of 257
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_holding_a_library_in_a_subdirectory`
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_that_already_holds_a_library`
  - `tests/test_restore_cli.py::test_a_target_that_already_holds_a_database_is_refused_with_no_way_to_name_it`

Old text:

```
    existing = [entry for entry in recovered_database_fileset(cfg, where) if entry.exists()]
```

New text:

```
    existing = []
```

### `r592-a.A2_database_dropped_from_fileset`

recovered_database_fileset: return the companions only, so a database already at the landing path is not an occupied target

- File: `src/cratekit/core/restore.py`
- Source: `r592-a.json`, row `A2_database_dropped_from_fileset`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 257 against a baseline of 257
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_holding_a_library_in_a_subdirectory`
  - `tests/test_restore.py::test_the_occupancy_fileset_is_the_one_the_restore_plan_writes`
  - `tests/test_restore_cli.py::test_a_target_that_already_holds_a_database_is_refused_with_no_way_to_name_it`

Old text:

```
    return (landing, *companions)
```

New text:

```
    return companions
```

### `r592-a.A3_companions_dropped_from_fileset`

recovered_database_fileset: return the database only, so a lone write-ahead log the database half would clear is not an occupied target

- File: `src/cratekit/core/restore.py`
- Source: `r592-a.json`, row `A3_companions_dropped_from_fileset`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 257 against a baseline of 257
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_that_already_holds_a_library`
  - `tests/test_restore.py::test_the_occupancy_fileset_is_the_one_the_restore_plan_writes`

Old text:

```
    return (landing, *companions)
```

New text:

```
    return (landing,)
```

### `r592-a.A4_fileset_not_rebased`

recovered_database_fileset: land the database at its bare name at the top of the target for every layout, so the guard tests a path the transfer never writes

- File: `src/cratekit/core/restore.py`
- Source: `r592-a.json`, row `A4_fileset_not_rebased`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 257 against a baseline of 257
- Kills: 4 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_holding_a_library_in_a_subdirectory`
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_that_already_holds_a_library`
  - `tests/test_restore.py::test_the_occupancy_fileset_is_the_one_the_restore_plan_writes`
  - `tests/test_restore_cli.py::test_a_target_that_already_holds_a_database_is_refused_with_no_way_to_name_it`

Old text:

```
        landing = target / database.relative_to(cfg.library.root)
    except ValueError:
```

New text:

```
        landing = target / database.name
    except ValueError:
```

### `r592-a.A5_replacing_existing_inverted`

assert_recovery_target: refuse an occupied target only when it WAS named for replacement

- File: `src/cratekit/core/restore.py`
- Source: `r592-a.json`, row `A5_replacing_existing_inverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 257 against a baseline of 257
- Kills: 8 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_holding_a_library_in_a_subdirectory`
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_that_already_holds_a_library`
  - `tests/test_restore.py::test_u95_a_bare_metal_plan_is_the_library_plan_moved_and_nothing_else`
  - `tests/test_restore.py::test_u95_a_bare_metal_plan_never_reads_the_capture_the_refused_library_holds`
  - `tests/test_restore.py::test_u95_a_bare_metal_session_plans_and_runs_entirely_under_its_target`
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_library_is_refused_under_a_bare_metal_session`
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_target_is_refused_under_a_library_session`
  - `tests/test_restore_cli.py::test_a_target_that_already_holds_a_database_is_refused_with_no_way_to_name_it`

Old text:

```
    if existing and not replacing_existing:
```

New text:

```
    if existing and replacing_existing:
```

### `r592-a.A6_old_suffix_rule_restored`

assert_recovery_target: put the recursive any-database rule back, the behaviour R-592 records, so every interrupted recovery is refused on rerun

- File: `src/cratekit/core/restore.py`
- Source: `r592-a.json`, row `A6_old_suffix_rule_restored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 257 against a baseline of 257
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_opens_over_databases_it_would_not_replace`
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_that_already_holds_a_library`

Old text:

```
    existing = [entry for entry in recovered_database_fileset(cfg, where) if entry.exists()]
```

New text:

```
    existing = sorted(entry for entry in where.rglob("*.db") if entry.is_file())
```

### `r592-a.A7_companion_suffix_wrong`

recovered_database_fileset: name each companion with a dot before its suffix, master.db.-wal, so no real companion is ever found

- File: `src/cratekit/core/restore.py`
- Source: `r592-a.json`, row `A7_companion_suffix_wrong`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 257 against a baseline of 257
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_that_already_holds_a_library`
  - `tests/test_restore.py::test_the_occupancy_fileset_is_the_one_the_restore_plan_writes`

Old text:

```
        landing.with_name(landing.name + sidecar.suffix)
        for sidecar in config.state_file("rekordbox_db").sidecars
    )
    return (landing, *companions)
```

New text:

```
        landing.with_name(landing.name + "." + sidecar.suffix)
        for sidecar in config.state_file("rekordbox_db").sidecars
    )
    return (landing, *companions)
```

### `r592-a.A8_sample_stub_check_beside`

SAMPLE, existing guard: assert_recovery_target refuses only a stub at or under the configured root, not the suffixed name beside it

- File: `src/cratekit/core/restore.py`
- Source: `r592-a.json`, row `A8_sample_stub_check_beside`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 257 against a baseline of 257
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_the_stubs_beside_and_beneath_the_mount_point[library 1-why1]`
  - `tests/test_restore.py::test_round2_the_real_mount_probe_is_armed_by_default`

Old text:

```
    if (inside_configured or beside_configured) and not probe(where):
```

New text:

```
    if inside_configured and not probe(where):
```

### `u27-restore-cli-independent.X6_the_rekordbox_guard_itself_is_neutered`

What the process-lister zeros DO leave held: make the restore engine's rekordbox-closed assertion return without asking. Paired with I_A6 and I_A7, which stopped threading that guard's injected seam and killed nothing

- File: `src/cratekit/core/restore.py`
- Source: `u27-restore-cli-independent.json`, row `X6_the_rekordbox_guard_itself_is_neutered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 257 against a baseline of 257
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_a_restore_refuses_while_rekordbox_holds_the_database`

Old text:

```
    running = processes.rekordbox_processes_running(lister=process_lister)
    if not running:
        return
```

New text:

```
    running = processes.rekordbox_processes_running(lister=process_lister)
    if running or not running:
        return
```

### `u95-a.A1_never_rerooted`

_rooted hands every session its configuration back unchanged, which is main's state: a bare-metal session resolves from the configured root again

- File: `src/cratekit/core/restore.py`
- Source: `u95-a.json`, row `A1_never_rerooted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 7 (killed)
- Killed:
  - `tests/test_restore.py::test_blocking_1_a_bare_metal_session_cannot_be_spent_on_the_library_it_refused`
  - `tests/test_restore.py::test_u95_a_bare_metal_plan_is_the_library_plan_moved_and_nothing_else`
  - `tests/test_restore.py::test_u95_a_bare_metal_plan_never_reads_the_capture_the_refused_library_holds`
  - `tests/test_restore.py::test_u95_a_bare_metal_session_plans_and_runs_entirely_under_its_target`
  - `tests/test_restore.py::test_u95_a_bare_metal_session_roots_the_configuration_at_its_target`
  - `tests/test_restore.py::test_u95_a_database_outside_the_library_refuses_a_bare_metal_plan_by_name`
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_target_is_refused_under_a_library_session`

Old text:

```
    if held.issued_by is not Guard.BARE_METAL:
        return cfg
    target = Path(held.authorises)
```

New text:

```
    if held.issued_by is not None:
        return cfg
    target = Path(held.authorises)
```

### `u95-a.A2_library_sessions_rerooted_too`

Drop the guard test in _rooted, so a library session handed a configuration for ANOTHER library is quietly re-aimed at what it authorises instead of refused

- File: `src/cratekit/core/restore.py`
- Source: `u95-a.json`, row `A2_library_sessions_rerooted_too`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_library_session_still_refuses_a_configuration_for_another_library`
  - `tests/test_restore.py::test_u95_a_live_recovery_session_plan_is_unchanged_by_golden`

Old text:

```
    if held.issued_by is not Guard.BARE_METAL:
        return cfg
    target = Path(held.authorises)
```

New text:

```
    target = Path(held.authorises)
```

### `u95-a.A3_database_not_carried`

The relocated root no longer carries its database: db_path stays at the configured root while the root moves to the target

- File: `src/cratekit/core/restore.py`
- Source: `u95-a.json`, row `A3_database_not_carried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 4 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_bare_metal_plan_is_the_library_plan_moved_and_nothing_else`
  - `tests/test_restore.py::test_u95_a_bare_metal_session_plans_and_runs_entirely_under_its_target`
  - `tests/test_restore.py::test_u95_a_bare_metal_session_roots_the_configuration_at_its_target`
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_target_is_refused_under_a_library_session`

Old text:

```
    return replace(cfg, library=replace(cfg.library, root=target, db_path=database))
```

New text:

```
    return replace(cfg, library=replace(cfg.library, root=target))
```

### `u95-a.A4_outside_database_refusal_removed`

Delete the by-name refusal for a database kept outside the library, leaving the defect-flavoured authorisation refusal to catch it later

- File: `src/cratekit/core/restore.py`
- Source: `u95-a.json`, row `A4_outside_database_refusal_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_database_outside_the_library_refuses_a_bare_metal_plan_by_name`

Old text:

```
    if not held.authorises_path(database):
        raise _refuse_target(
```

New text:

```
    if False:
        raise _refuse_target(
```

### `u95-a.A5_capture_path_not_rebased`

plan reads the session record's capture path as written, so the capture is taken from the configured root, the volume the identity gate refused

- File: `src/cratekit/core/restore.py`
- Source: `u95-a.json`, row `A5_capture_path_not_rebased`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_bare_metal_plan_is_the_library_plan_moved_and_nothing_else`
  - `tests/test_restore.py::test_u95_a_bare_metal_session_plans_and_runs_entirely_under_its_target`

Old text:

```
    root = capture_root_of(_rebased(record.snapshot_path, recorded_root, rooted_at))
```

New text:

```
    root = capture_root_of(record.snapshot_path)
```

### `u95-a.A6_manifest_not_rebased_in_plan`

plan uses the manifest as read from disk, every path in it still naming the dead root

- File: `src/cratekit/core/restore.py`
- Source: `u95-a.json`, row `A6_manifest_not_rebased_in_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_bare_metal_plan_is_the_library_plan_moved_and_nothing_else`
  - `tests/test_restore.py::test_u95_a_bare_metal_session_plans_and_runs_entirely_under_its_target`
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_target_is_refused_under_a_library_session`

Old text:

```
    captured = _rebased_capture(snapshot.read_manifest(root), recorded_root, rooted_at)
```

New text:

```
    captured = snapshot.read_manifest(root)
```

### `u95-a.A7_manifest_not_rebased_in_preflight`

The run's preflight re-reads the manifest and checks it un-rebased, so it asks the DEAD volume whether the capture is still whole

- File: `src/cratekit/core/restore.py`
- Source: `u95-a.json`, row `A7_manifest_not_rebased_in_preflight`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_bare_metal_session_plans_and_runs_entirely_under_its_target`

Old text:

```
    captured = _rebased_capture(
        snapshot.read_manifest(decided.capture_root),
        recorded_root,
        Path(cfg.library.root),
    )
```

New text:

```
    captured = snapshot.read_manifest(decided.capture_root)
```

### `u95-a.A8_run_not_rooted`

run resolves from the caller's configuration while plan resolves from the session, the two sources for one answer R-20 forbids

- File: `src/cratekit/core/restore.py`
- Source: `u95-a.json`, row `A8_run_not_rooted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_bare_metal_session_plans_and_runs_entirely_under_its_target`

Old text:

```
    cfg = _rooted(configured, held)
    assert_gates_are_open(held, writing=cfg.library.root)
    _assert_rekordbox_closed(process_lister)
    _preflight(
```

New text:

```
    cfg = configured
    assert_gates_are_open(held, writing=cfg.library.root)
    _assert_rekordbox_closed(process_lister)
    _preflight(
```

### `u95-b.B2_manifest_database_not_moved`

_rebased_capture leaves Capture.database at the dead root, the file assert_verified asks the disk about

- File: `src/cratekit/core/restore.py`
- Source: `u95-b.json`, row `B2_manifest_database_not_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_bare_metal_plan_is_the_library_plan_moved_and_nothing_else`
  - `tests/test_restore.py::test_u95_a_bare_metal_session_plans_and_runs_entirely_under_its_target`

Old text:

```
        database=moved(captured.database),
```

New text:

```
        database=captured.database,
```

### `u95-b.B3_sources_not_moved`

The WRITE side is not re-based: every manifest source still names the configured root

- File: `src/cratekit/core/restore.py`
- Source: `u95-b.json`, row `B3_sources_not_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_bare_metal_plan_is_the_library_plan_moved_and_nothing_else`
  - `tests/test_restore.py::test_u95_a_bare_metal_session_plans_and_runs_entirely_under_its_target`
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_target_is_refused_under_a_library_session`

Old text:

```
                source=_rebased(entry.source, recorded_root, root),
```

New text:

```
                source=entry.source,
```

### `u95-b.B4_captured_not_moved`

The READ side is not re-based: writes aim at the target while the bytes come from the dead volume, the bypass run the other way

- File: `src/cratekit/core/restore.py`
- Source: `u95-b.json`, row `B4_captured_not_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_bare_metal_plan_is_the_library_plan_moved_and_nothing_else`
  - `tests/test_restore.py::test_u95_a_bare_metal_session_plans_and_runs_entirely_under_its_target`

Old text:

```
                captured=moved(entry.captured),
```

New text:

```
                captured=entry.captured,
```

### `u95-b.B5_not_idempotent`

Drop the already-under-the-new-root clause, so a path naming a target mounted inside the configured root is moved twice

- File: `src/cratekit/core/restore.py`
- Source: `u95-b.json`, row `B5_not_idempotent`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_recorded_path_is_moved_by_the_rule_config_uses_and_only_once`

Old text:

```
    if parts[: len(here)] == here or parts[: len(there)] != there:
```

New text:

```
    if parts[: len(there)] != there:
```

### `u95-b.B6_recorded_path_not_normalised`

Compare the recorded path's raw parts, so a dotted spelling config calls inside is left unmoved and one it calls outside is moved

- File: `src/cratekit/core/restore.py`
- Source: `u95-b.json`, row `B6_recorded_path_not_normalised`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_recorded_path_is_moved_by_the_rule_config_uses_and_only_once`

Old text:

```
    parts = Path(os.path.normpath(str(recorded))).parts
```

New text:

```
    parts = recorded.parts
```

### `u95-b.B8_outside_path_moved_anyway`

A path under NEITHER root is joined onto the target instead of left where it says it is

- File: `src/cratekit/core/restore.py`
- Source: `u95-b.json`, row `B8_outside_path_moved_anyway`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_database_outside_the_library_refuses_a_bare_metal_plan_by_name`
  - `tests/test_restore.py::test_u95_a_recorded_path_is_moved_by_the_rule_config_uses_and_only_once`

Old text:

```
    if parts[: len(here)] == here or parts[: len(there)] != there:
        return recorded
    return Path(root).joinpath(*parts[len(there) :])
```

New text:

```
    if parts[: len(here)] == here:
        return recorded
    return Path(root).joinpath(*parts[len(there) :])
```

### `u95-b1.B1_manifest_root_not_moved`

RE-MEASURED after test_u95_a_bare_metal_plan_is_the_library_plan_moved_and_nothing_else learned to compare decisions. _rebased_capture leaves Capture.root at the dead root, which is what _captured_by_key composes coupled entries from

- File: `src/cratekit/core/restore.py`
- Source: `u95-b1.json`, row `B1_manifest_root_not_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_bare_metal_plan_is_the_library_plan_moved_and_nothing_else`

Old text:

```
        root=_rebased(captured.root, recorded_root, root),
```

New text:

```
        root=captured.root,
```

### `u95-c.C1_plan_side_guard_removed`

plan no longer checks its own answer, so only a run would find a plan naming an outside path

- File: `src/cratekit/core/restore.py`
- Source: `u95-c.json`, row `C1_plan_side_guard_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_plan_checks_its_own_answer_rather_than_trusting_the_derivation`

Old text:

```
    _assert_plan_is_authorised(steps, pre_restore_root, cfg, held)

```

New text:

```
(empty)
```

### `u95-c.C2_run_side_guard_removed`

The preflight no longer asks the session about a plan value, so a plan built for one directory runs under a session for another

- File: `src/cratekit/core/restore.py`
- Source: `u95-c.json`, row `C2_run_side_guard_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 7 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_library_is_refused_under_a_bare_metal_session`
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_target_is_refused_under_a_library_session`
  - `tests/test_restore.py::test_u95_a_step_aimed_at_the_authorised_directory_itself_is_refused`
  - `tests/test_restore.py::test_u95_staging_inside_the_library_but_not_under_its_store_is_refused[a-directory-in-the-library]`
  - `tests/test_restore.py::test_u95_staging_inside_the_library_but_not_under_its_store_is_refused[the-library-root]`
  - `tests/test_restore.py::test_u95_staging_inside_the_library_but_not_under_its_store_is_refused[the-staging-store-itself]`
  - `tests/test_restore.py::test_u95_the_staging_directory_is_a_write_location_and_is_authorised_too`

Old text:

```
    _assert_plan_is_authorised(decided.steps, decided.pre_restore_root, cfg, held)

```

New text:

```
(empty)
```

### `u95-c.C3_step_authorisation_removed`

Inside the guard, drop the per step authorisation and leave only the membership test

- File: `src/cratekit/core/restore.py`
- Source: `u95-c.json`, row `C3_step_authorisation_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_library_is_refused_under_a_bare_metal_session`
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_target_is_refused_under_a_library_session`

Old text:

```
        assert_gates_are_open(held, writing=step.target)
        if step.target not in allowed:
```

New text:

```
        if step.target not in allowed:
```

### `u95-c.C4_restorable_membership_removed`

Inside the guard, drop the re-derived membership test, so a step aimed at the authorised directory itself is admitted

- File: `src/cratekit/core/restore.py`
- Source: `u95-c.json`, row `C4_restorable_membership_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_step_aimed_at_the_authorised_directory_itself_is_refused`

Old text:

```
        if step.target not in allowed:
            raise refuse(
```

New text:

```
        if False:
            raise refuse(
```

### `u95-c.C5_staging_authorisation_removed`

Inside the guard, drop the authorisation of the staging directory and leave only the store rule

- File: `src/cratekit/core/restore.py`
- Source: `u95-c.json`, row `C5_staging_authorisation_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_plan_checks_its_own_answer_rather_than_trusting_the_derivation`
  - `tests/test_restore.py::test_u95_the_staging_directory_is_a_write_location_and_is_authorised_too`

Old text:

```
    assert_gates_are_open(held, writing=pre_restore_root)
    store = _pre_restore_root(cfg).parent
```

New text:

```
    store = _pre_restore_root(cfg).parent
```

### `u95-c.C6_staging_store_rule_removed`

Inside the guard, drop the store rule, so an authorised staging directory such as the library root hands the closing prune the directory ABOVE the library

- File: `src/cratekit/core/restore.py`
- Source: `u95-c.json`, row `C6_staging_store_rule_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_staging_inside_the_library_but_not_under_its_store_is_refused[a-directory-in-the-library]`
  - `tests/test_restore.py::test_u95_staging_inside_the_library_but_not_under_its_store_is_refused[the-library-root]`
  - `tests/test_restore.py::test_u95_staging_inside_the_library_but_not_under_its_store_is_refused[the-staging-store-itself]`

Old text:

```
    if pre_restore_root.parent != store:
```

New text:

```
    if False:
```

### `u95-c.C7_staging_store_itself_admitted`

A nearby value: admit the store itself as the staging directory, which makes the prune run one level up, inside the database directory

- File: `src/cratekit/core/restore.py`
- Source: `u95-c.json`, row `C7_staging_store_itself_admitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_staging_inside_the_library_but_not_under_its_store_is_refused[the-staging-store-itself]`

Old text:

```
    if pre_restore_root.parent != store:
```

New text:

```
    if pre_restore_root.parent != store and pre_restore_root != store:
```

### `u95-c.C8_plan_root_assertion_removed`

plan drops its assertion on the rooted root, which is also where it asks whether the session is still open and is a recovery

- File: `src/cratekit/core/restore.py`
- Source: `u95-c.json`, row `C8_plan_root_assertion_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_library_session_still_refuses_a_configuration_for_another_library`

Old text:

```
    assert_gates_are_open(held, writing=cfg.library.root)
    _assert_rekordbox_closed(process_lister)
    record = session.read_record(session_id, cfg)
```

New text:

```
    _assert_rekordbox_closed(process_lister)
    record = session.read_record(session_id, cfg)
```

### `u95-c.S1_authorises_everything`

EXISTING GUARD, fixed sample: Held.authorises_path answers yes to every path, which is the original bypass

- File: `src/cratekit/core/restore.py`
- Source: `u95-c.json`, row `S1_authorises_everything`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 7 (killed)
- Killed:
  - `tests/test_restore.py::test_blocking_1_a_bare_metal_session_cannot_be_spent_on_the_library_it_refused`
  - `tests/test_restore.py::test_u95_a_database_outside_the_library_refuses_a_bare_metal_plan_by_name`
  - `tests/test_restore.py::test_u95_a_library_session_still_refuses_a_configuration_for_another_library`
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_library_is_refused_under_a_bare_metal_session`
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_target_is_refused_under_a_library_session`
  - `tests/test_restore.py::test_u95_plan_checks_its_own_answer_rather_than_trusting_the_derivation`
  - `tests/test_restore.py::test_u95_the_staging_directory_is_a_write_location_and_is_authorised_too`

Old text:

```
        return where == root or root in where.parents
```

New text:

```
        return True
```

### `u95-c.S2_issued_terms_not_compared`

EXISTING GUARD, fixed sample: still_open stops comparing the claim to what the guard issued, so a live token can be rebuilt around another directory

- File: `src/cratekit/core/restore.py`
- Source: `u95-c.json`, row `S2_issued_terms_not_compared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_round2_a_held_rebuilt_around_a_live_token_is_refused`

Old text:

```
        if terms != (self.issued_by, str(self.authorises), str(self.lock.absolute())):
            return False
```

New text:

```
(empty)
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

### `r1665-b.S14_sources_unchecked_again`

assert_sources_present: never refuse, measured again after the zero in r1665.md was given its test, so a restore accepts a capture missing files

- File: `src/cratekit/core/snapshot.py`
- Source: `r1665-b.json`, row `S14_sources_unchecked_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 327 against a baseline of 327
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
- Collected: 327 against a baseline of 327
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
- Collected: 327 against a baseline of 327
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
- Collected: 327 against a baseline of 327
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
- Collected: 327 against a baseline of 327
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
- Collected: 327 against a baseline of 327
- Kills: 66 (killed)
- Killed:
  - `tests/test_restore.py::test_a_capture_whose_manifest_names_a_path_outside_the_set_is_refused`
  - `tests/test_restore.py::test_a_coupled_file_the_capture_records_as_absent_is_removed_again`
  - `tests/test_restore.py::test_a_dry_run_and_a_real_run_walk_the_same_list_in_the_same_order`
  - `tests/test_restore.py::test_a_held_session_used_after_its_block_is_refused`
  - `tests/test_restore.py::test_a_later_session_that_committed_nothing_does_not_need_an_override`
  - `tests/test_restore.py::test_a_plan_built_before_a_later_commit_is_refused_at_run`
  - `tests/test_restore.py::test_a_pre_cutover_restore_leaves_the_next_session_refused`
  - `tests/test_restore.py::test_a_rehearsal_reports_what_is_outstanding_rather_than_what_it_recorded`
  - `tests/test_restore.py::test_a_restore_lists_every_effect_it_cannot_undo_and_blocks_convergence`
  - `tests/test_restore.py::test_a_restore_predating_a_cutover_marks_that_tree_unconverged`
  - `tests/test_restore.py::test_a_restore_refuses_while_rekordbox_holds_the_database`
  - `tests/test_restore.py::test_a_restore_replaces_exactly_the_derived_coupled_set`
  - `tests/test_restore.py::test_a_restore_returns_a_modified_database_to_its_pre_session_bytes`
  - `tests/test_restore.py::test_a_restore_returns_the_coupled_state_with_the_database`
  - `tests/test_restore.py::test_a_restore_taken_after_the_cutover_marks_nothing`
  - ... and 51 more, see the JSON sidecar

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
- Collected: 327 against a baseline of 327
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
- Collected: 327 against a baseline of 327
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
- Collected: 327 against a baseline of 327
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
- Collected: 327 against a baseline of 327
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
- Collected: 327 against a baseline of 327
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
- Collected: 327 against a baseline of 327
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
- Collected: 327 against a baseline of 327
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
- Collected: 327 against a baseline of 327
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
- Collected: 327 against a baseline of 327
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
- Collected: 293 against a baseline of 293
- Kills: 8 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_temporary_volume_with_no_room_for_the_rehearsal_check_refuses_before_its_copy`
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
- Collected: 109 against a baseline of 109
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_temporary_volume_with_no_room_for_the_rehearsal_check_refuses_before_its_copy`
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
- Collected: 109 against a baseline of 109
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
- Collected: 109 against a baseline of 109
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
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_check_room_r1677.py::test_a_store_not_yet_made_is_read_as_the_volume_of_its_nearest_parent`

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
- Collected: 67 against a baseline of 67
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_check_whose_copy_fails_otherwise_is_still_a_failed_check`
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
- Collected: 67 against a baseline of 67
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
        # No verdict at all, which the capture names rather than folding into a
        # failed one (R-1677); it still records the capture unverified.
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
- Collected: 630 against a baseline of 630
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
- Collected: 630 against a baseline of 630
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
- Collected: 630 against a baseline of 630
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
- Collected: 630 against a baseline of 630
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
- Collected: 630 against a baseline of 630
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

### `u272.S13_parents_before_children`

_flush: walk top down, so a directory is flushed before the files in it

- File: `src/cratekit/core/snapshot.py`
- Source: `u272.json`, row `S13_parents_before_children`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
capture_root, topdown=False, onerror=_raise_walk_error
```

New text:

```
capture_root, topdown=True, onerror=_raise_walk_error
```

### `u272.S14_wrong_slug`

_not_flushed: refuse under internal-error rather than the integrity slug the gate uses

- File: `src/cratekit/core/snapshot.py`
- Source: `u272.json`, row `S14_wrong_slug`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 630 against a baseline of 630
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
- Collected: 630 against a baseline of 630
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
- Collected: 630 against a baseline of 630
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
- Collected: 630 against a baseline of 630
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
- Collected: 630 against a baseline of 630
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
- Collected: 630 against a baseline of 630
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
- Collected: 630 against a baseline of 630
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
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 630 against a baseline of 630
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
        integrity_verified=False,
        sources=record.sources,
    )
    try:
```

New text:

```
        integrity_verified=record.integrity_verified,
        sources=record.sources,
    )
    try:
```

### `u272.S7_failure_not_recorded`

_not_flushed: refuse without writing the unverified manifest

- File: `src/cratekit/core/snapshot.py`
- Source: `u272.json`, row `S7_failure_not_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 630 against a baseline of 630
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
        _write_manifest(unverified, manifest)
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
- Collected: 630 against a baseline of 630
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
- Collected: 630 against a baseline of 630
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

