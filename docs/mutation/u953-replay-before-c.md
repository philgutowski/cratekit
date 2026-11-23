# Mutation table: u953-replay-before-c

Measured by `scripts/mutate.py` on 2026-11-23 07:33 UTC, branch `HEAD` at `5113ee10`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22473 collected. pytest invocations for this batch: 114.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-23 07:33 UTC for commit `5113ee10f744`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 19, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22473 against 22473. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u95-a.A1_never_rerooted` | `src/cratekit/core/restore.py` | user | 3 file(s) | 505 | 7 | killed |
| `u95-a.A2_library_sessions_rerooted_too` | `src/cratekit/core/restore.py` | user | 3 file(s) | 505 | 2 | killed |
| `u95-a.A3_database_not_carried` | `src/cratekit/core/restore.py` | user | 3 file(s) | 505 | 4 | killed |
| `u95-a.A4_outside_database_refusal_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 505 | 1 | killed |
| `u95-a.A5_capture_path_not_rebased` | `src/cratekit/core/restore.py` | user | 3 file(s) | 505 | 2 | killed |
| `u95-a.A6_manifest_not_rebased_in_plan` | `src/cratekit/core/restore.py` | user | 3 file(s) | 505 | 3 | killed |
| `u95-a.A7_manifest_not_rebased_in_preflight` | `src/cratekit/core/restore.py` | user | 3 file(s) | 505 | 1 | killed |
| `u95-a.A8_run_not_rooted` | `src/cratekit/core/restore.py` | user | 3 file(s) | 505 | 1 | killed |
| `u95-b.B2_manifest_database_not_moved` | `src/cratekit/core/restore.py` | user | 3 file(s) | 505 | 2 | killed |
| `u95-b.B3_sources_not_moved` | `src/cratekit/core/restore.py` | user | 3 file(s) | 505 | 3 | killed |
| `u95-b.B4_captured_not_moved` | `src/cratekit/core/restore.py` | user | 3 file(s) | 505 | 2 | killed |
| `u95-b.B5_not_idempotent` | `src/cratekit/core/restore.py` | maintainer | 3 file(s) | 505 | 1 | killed |
| `u95-b.B6_recorded_path_not_normalised` | `src/cratekit/core/restore.py` | maintainer | 3 file(s) | 505 | 1 | killed |
| `u95-b.B8_outside_path_moved_anyway` | `src/cratekit/core/restore.py` | maintainer | 3 file(s) | 505 | 2 | killed |
| `u95-b1.B1_manifest_root_not_moved` | `src/cratekit/core/restore.py` | user | 3 file(s) | 505 | 1 | killed |
| `u95-c.C1_plan_side_guard_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 505 | 1 | killed |
| `u95-c.C2_run_side_guard_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 505 | 7 | killed |
| `u95-c.C3_step_authorisation_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 505 | 2 | killed |
| `u95-c.C4_restorable_membership_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 505 | 1 | killed |
| `u95-c.C5_staging_authorisation_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 505 | 2 | killed |
| `u95-c.C6_staging_store_rule_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 505 | 3 | killed |
| `u95-c.C7_staging_store_itself_admitted` | `src/cratekit/core/restore.py` | user | 3 file(s) | 505 | 1 | killed |
| `u95-c.C8_plan_root_assertion_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 505 | 1 | killed |
| `u95-c.S1_authorises_everything` | `src/cratekit/core/restore.py` | user | 3 file(s) | 505 | 7 | killed |
| `u95-c.S2_issued_terms_not_compared` | `src/cratekit/core/restore.py` | user | 3 file(s) | 505 | 1 | killed |
| `r1890.P13_convergence_fallback_filter_in_restore_perform` | `src/cratekit/core/restore_perform.py` | maintainer | 1 file(s) | 159 | 1 | killed |
| `r1890.P9_sidecar_suffix_typed_in_restore_perform` | `src/cratekit/core/restore_perform.py` | user | 1 file(s) | 252 | 1 | killed |
| `u300.S19_replace_file_local` | `src/cratekit/core/restore_perform.py` | maintainer | 2 file(s) | 253 | 2 | killed |
| `u300.S20_stage_aside_local` | `src/cratekit/core/restore_perform.py` | maintainer | 2 file(s) | 253 | 1 | killed |
| `r592-a.A1_occupancy_guard_removed` | `src/cratekit/core/restore_recovery.py` | user | 2 file(s) | 253 | 3 | killed |
| `r592-a.A2_database_dropped_from_fileset` | `src/cratekit/core/restore_recovery.py` | user | 2 file(s) | 253 | 3 | killed |
| `r592-a.A3_companions_dropped_from_fileset` | `src/cratekit/core/restore_recovery.py` | user | 2 file(s) | 253 | 2 | killed |
| `r592-a.A4_fileset_not_rebased` | `src/cratekit/core/restore_recovery.py` | user | 2 file(s) | 253 | 4 | killed |
| `r592-a.A5_replacing_existing_inverted` | `src/cratekit/core/restore_recovery.py` | user | 2 file(s) | 253 | 8 | killed |
| `r592-a.A6_old_suffix_rule_restored` | `src/cratekit/core/restore_recovery.py` | user | 2 file(s) | 253 | 2 | killed |
| `r592-a.A7_companion_suffix_wrong` | `src/cratekit/core/restore_recovery.py` | user | 2 file(s) | 253 | 2 | killed |
| `r592-a.A8_sample_stub_check_beside` | `src/cratekit/core/restore_recovery.py` | user | 2 file(s) | 253 | 2 | killed |
| `u300.S21_mount_probe_local` | `src/cratekit/core/restore_recovery.py` | maintainer | 2 file(s) | 253 | 2 | killed |
| `u96-b.C1_engine_terminal` | `src/cratekit/core/restore_recovery.py` | user | 2 file(s) | 253 | 2 | killed |
| `u96-b.C2_engine_acknowledged` | `src/cratekit/core/restore_recovery.py` | user | 2 file(s) | 253 | 3 | killed |
| `u96-b.C3_engine_occupied_target` | `src/cratekit/core/restore_recovery.py` | user | 2 file(s) | 253 | 3 | killed |
| `u96-b.C4_engine_stub` | `src/cratekit/core/restore_recovery.py` | user | 2 file(s) | 253 | 5 | killed |
| `u96-b.C5_engine_library_is_mounted` | `src/cratekit/core/restore_recovery.py` | user | 2 file(s) | 253 | 3 | killed |
| `r1255.S1_scan_unlisted_as_empty` | `src/cratekit/core/session.py` | user | 7 file(s) | 867 | 14 | killed |
| `r1255.S2_absent_log_unread` | `src/cratekit/core/session.py` | user | 7 file(s) | 867 | 46 | killed |
| `r1255.S3_log_file_absent` | `src/cratekit/core/session.py` | user | 2 file(s) | 432 | 1 | killed |
| `r1255.S4_under_a_file_unread` | `src/cratekit/core/session.py` | user | 2 file(s) | 432 | 1 | killed |
| `r1255.S5_json_filter` | `src/cratekit/core/session.py` | user | 7 file(s) | 867 | 1 | killed |
| `r1255.S6_records_refuses_unlisted` | `src/cratekit/core/session.py` | user | 4 file(s) | 628 | 4 | killed |
| `r1255.S7_log_unlisted_predicate` | `src/cratekit/core/session.py` | user | 4 file(s) | 143 | 11 | killed |
| `r1255.S8_clause_listing_wording` | `src/cratekit/core/session.py` | user | 3 file(s) | 116 | 8 | killed |
| `r1255.S9_gate_unlisted_detail` | `src/cratekit/core/session.py` | maintainer | 3 file(s) | 322 | 2 | killed |
| `r239-b.S11_readback_key_on` | `src/cratekit/core/session.py` | user | 7 file(s) | 723 | 1 | killed |
| `r375-a.S10_commit_not_persisted_at_once` | `src/cratekit/core/session.py` | user | 4 file(s) | 393 | 1 | killed |
| `r375-a.S11_commit_replaces_the_summary` | `src/cratekit/core/session.py` | user | 4 file(s) | 393 | 3 | killed |
| `r375-a.S1_keep_is_ignored` | `src/cratekit/core/session.py` | user | 4 file(s) | 393 | 38 | killed |
| `r375-a.S2_record_inside_the_watch` | `src/cratekit/core/session.py` | user | 4 file(s) | 393 | 3 | killed |
| `r375-a.S3_a_raise_is_not_abandoned` | `src/cratekit/core/session.py` | user | 4 file(s) | 393 | 13 | killed |
| `r375-a.S4_abandon_failure_replaces_the_error` | `src/cratekit/core/session.py` | user | 4 file(s) | 393 | 1 | killed |
| `r375-a.S5_clean_close_refusal_leaves_it_open` | `src/cratekit/core/session.py` | user | 4 file(s) | 393 | 1 | killed |
| `r375-a.S6_close_ignores_the_intent` | `src/cratekit/core/session.py` | user | 4 file(s) | 393 | 11 | killed |
| `r375-a.S7_close_drops_the_identity_seam` | `src/cratekit/core/session.py` | maintainer | 4 file(s) | 393 | 4 | killed |
| `r375-a.S8_record_names_no_actor` | `src/cratekit/core/session.py` | user | 4 file(s) | 393 | 2 | killed |
| `r375-a.S9_record_names_no_acknowledgment` | `src/cratekit/core/session.py` | user | 4 file(s) | 393 | 2 | killed |
| `r501-a.S1_verify_state_guard` | `src/cratekit/core/session.py` | maintainer | 5 file(s) | 134 | 1 | killed |
| `r501-a.S2_excusal_capture` | `src/cratekit/core/session.py` | user | 5 file(s) | 134 | 1 | killed |
| `r501-a.S3_excusal_proof` | `src/cratekit/core/session.py` | user | 5 file(s) | 134 | 5 | killed |
| `r501-a.S4_excusal_state` | `src/cratekit/core/session.py` | user | 5 file(s) | 134 | 1 | killed |
| `r598-a.A5_holder_never_recorded` | `src/cratekit/core/session.py` | user | 3 file(s) | 602 | 8 | killed |
| `r598-a.A6_record_holder_is_a_second_lookup` | `src/cratekit/core/session.py` | maintainer | 2 file(s) | 185 | 1 | killed |
| `u138-rerun.S5_bound_exclusive` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4023 | 1 | killed |
| `u138.E1_terminal_check` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4023 | 4 | killed |
| `u138.S10_older_record_reads_as_session` | `src/cratekit/core/session_ack.py` | maintainer | 43 file(s) | 4023 | 1 | killed |
| `u138.S11_rule_not_written` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4023 | 4 | killed |
| `u138.S12_message_names_the_portion` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4023 | 4 | killed |
| `u138.S13_remedy_points_back_at_ack` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4023 | 8 | killed |
| `u138.S1_session_rule_gone` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4023 | 20 | killed |
| `u138.S2_any_answer_gets_the_age_rule` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4023 | 13 | killed |
| `u138.S3_stale_not_refused` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4023 | 10 | killed |
| `u138.S6_bound_six_days` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4023 | 5 | killed |
| `u138.S8_rule_not_recorded` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4023 | 6 | killed |
| `u138.S9_answer_not_recorded` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4023 | 4 | killed |
| `u300.S15_terminal_probe_local` | `src/cratekit/core/session_ack.py` | maintainer | 2 file(s) | 185 | 10 | killed |
| `u300.S16_derive_actor_local` | `src/cratekit/core/session_ack.py` | maintainer | 2 file(s) | 185 | 1 | killed |
| `u48-author.S1_remedy_fixed_at_repair` | `src/cratekit/core/session_ack.py` | user | 11 file(s) | 1533 | 1 | killed |
| `u48-author.S2_remedy_fixed_at_grant` | `src/cratekit/core/session_ack.py` | user | 11 file(s) | 1533 | 2 | killed |
| `r598-a.A1_state_check_widened_to_non_terminal` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 4 | killed |
| `r598-a.A2_no_holder_read_as_gone` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 3 | killed |
| `r598-a.A3_liveness_not_consulted` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 8 | killed |
| `r598-a.A4_unreadable_holder_read_as_gone` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 1 | killed |
| `r598-a.A7_sweep_ignores_the_shown_list` | `src/cratekit/core/session_holders.py` | user | 2 file(s) | 185 | 1 | killed |
| `r598-b.B7_sample_live_holder_released` | `src/cratekit/core/session_holders.py` | user | 2 file(s) | 185 | 4 | killed |
| `r647-a.B10_live_identifier_not_asked` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 3 | killed |
| `r647-a.B11_start_time_compared_again` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 1 | killed |

## Row definitions

### `u95-a.A1_never_rerooted`

_rooted hands every session its configuration back unchanged, which is main's state: a bare-metal session resolves from the configured root again

- File: `src/cratekit/core/restore.py`
- Source: `u95-a.json`, row `A1_never_rerooted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 505 against a baseline of 505
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
- Collected: 505 against a baseline of 505
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
- Collected: 505 against a baseline of 505
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
- Collected: 505 against a baseline of 505
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
- Collected: 505 against a baseline of 505
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
- Collected: 505 against a baseline of 505
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
- Collected: 505 against a baseline of 505
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
- Collected: 505 against a baseline of 505
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
- Collected: 505 against a baseline of 505
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
- Collected: 505 against a baseline of 505
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
- Collected: 505 against a baseline of 505
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
- Collected: 505 against a baseline of 505
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
- Collected: 505 against a baseline of 505
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
- Collected: 505 against a baseline of 505
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
- Collected: 505 against a baseline of 505
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
- Collected: 505 against a baseline of 505
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
- Collected: 505 against a baseline of 505
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
- Collected: 505 against a baseline of 505
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
- Collected: 505 against a baseline of 505
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
- Collected: 505 against a baseline of 505
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
- Collected: 505 against a baseline of 505
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
- Collected: 505 against a baseline of 505
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
- Collected: 505 against a baseline of 505
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
- Collected: 505 against a baseline of 505
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
- Collected: 505 against a baseline of 505
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

### `r1890.P13_convergence_fallback_filter_in_restore_perform`

restore_perform, where the tree shortness handoff now lives, filters the unconverged tree kind core.convergence owns, the fallback the build must have deleted

- File: `src/cratekit/core/restore_perform.py`
- Source: `r1890.json`, row `P13_convergence_fallback_filter_in_restore_perform`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`
- Collected: 159 against a baseline of 159
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_the_convergence_fallback_expires_the_moment_both_modules_share_a_build`

Old text:

```
def _restore():
    """``restore`` at call time: its seams are patched there, and it imports this module."""
    from cratekit.core import restore

    return restore

```

New text:

```
def _restore():
    """``restore`` at call time: its seams are patched there, and it imports this module."""
    from cratekit.core import restore

    return restore


_SKIPPED = ("Kind.UNCONVERGED_TREE",)

```

### `r1890.P9_sidecar_suffix_typed_in_restore_perform`

restore_perform, a part, types a SQLite companion suffix instead of reading which sidecars come back from the declaration

- File: `src/cratekit/core/restore_perform.py`
- Source: `r1890.json`, row `P9_sidecar_suffix_typed_in_restore_perform`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 252 against a baseline of 252
- Kills: 1 (killed)
- Killed:
  - `tests/test_config.py::test_the_restore_unit_derives_its_target_set_rather_than_listing_it`

Old text:

```
def _restore():
    """``restore`` at call time: its seams are patched there, and it imports this module."""
    from cratekit.core import restore

    return restore

```

New text:

```
def _restore():
    """``restore`` at call time: its seams are patched there, and it imports this module."""
    from cratekit.core import restore

    return restore


_COMPANION = "master.db-wal"

```

### `u300.S19_replace_file_local`

the perform step replaces a file through the part's own _replace_file

- File: `src/cratekit/core/restore_perform.py`
- Source: `u300.json`, row `S19_replace_file_local`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 253 against a baseline of 253
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_blocking_2_a_failure_mid_restore_is_a_structured_refusal`
  - `tests/test_restore.py::test_round6_a_retry_after_a_partial_failure_still_runs`

Old text:

```
            _restore()._replace_file(step.source, step.target)
```

New text:

```
            _replace_file(step.source, step.target)
```

### `u300.S20_stage_aside_local`

the perform step stages a companion aside through the part's own helper

- File: `src/cratekit/core/restore_perform.py`
- Source: `u300.json`, row `S20_stage_aside_local`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_round6_the_performing_backstop_names_what_it_already_moved`

Old text:

```
            _restore()._stage_companion_aside(step.target, decided.pre_restore_root)
```

New text:

```
            _stage_companion_aside(step.target, decided.pre_restore_root)
```

### `r592-a.A1_occupancy_guard_removed`

assert_recovery_target: find nothing occupied whatever the target holds, so a library whose database sits where this one lands is replaced unasked

- File: `src/cratekit/core/restore_recovery.py`
- Source: `r592-a.json`, row `A1_occupancy_guard_removed`
- Moved: Moved from src/cratekit/core/restore.py to src/cratekit/core/restore_recovery.py by U300, which replayed this text there and kept the kill in u300-replay-after-c.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 253 against a baseline of 253
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

- File: `src/cratekit/core/restore_recovery.py`
- Source: `r592-a.json`, row `A2_database_dropped_from_fileset`
- Moved: Moved from src/cratekit/core/restore.py to src/cratekit/core/restore_recovery.py by U300, which replayed this text there and kept the kill in u300-replay-after-c.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 253 against a baseline of 253
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

- File: `src/cratekit/core/restore_recovery.py`
- Source: `r592-a.json`, row `A3_companions_dropped_from_fileset`
- Moved: Moved from src/cratekit/core/restore.py to src/cratekit/core/restore_recovery.py by U300, which replayed this text there and kept the kill in u300-replay-after-c.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 253 against a baseline of 253
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

- File: `src/cratekit/core/restore_recovery.py`
- Source: `r592-a.json`, row `A4_fileset_not_rebased`
- Moved: Moved from src/cratekit/core/restore.py to src/cratekit/core/restore_recovery.py by U300, which replayed this text there and kept the kill in u300-replay-after-c.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 253 against a baseline of 253
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

- File: `src/cratekit/core/restore_recovery.py`
- Source: `r592-a.json`, row `A5_replacing_existing_inverted`
- Moved: Moved from src/cratekit/core/restore.py to src/cratekit/core/restore_recovery.py by U300, which replayed this text there and kept the kill in u300-replay-after-c.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 253 against a baseline of 253
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

- File: `src/cratekit/core/restore_recovery.py`
- Source: `r592-a.json`, row `A6_old_suffix_rule_restored`
- Moved: Moved from src/cratekit/core/restore.py to src/cratekit/core/restore_recovery.py by U300, which replayed this text there and kept the kill in u300-replay-after-c.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 253 against a baseline of 253
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

- File: `src/cratekit/core/restore_recovery.py`
- Source: `r592-a.json`, row `A7_companion_suffix_wrong`
- Moved: Moved from src/cratekit/core/restore.py to src/cratekit/core/restore_recovery.py by U300, which replayed this text there and kept the kill in u300-replay-after-c.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 253 against a baseline of 253
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

- File: `src/cratekit/core/restore_recovery.py`
- Source: `r592-a.json`, row `A8_sample_stub_check_beside`
- Moved: Moved from src/cratekit/core/restore.py to src/cratekit/core/restore_recovery.py by U300, which replayed this text there and kept the kill in u300-replay-after-c.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 253 against a baseline of 253
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

### `u300.S21_mount_probe_local`

assert_library_volume_is_gone asks the part's own mount probe, so a patched probe is not asked

- File: `src/cratekit/core/restore_recovery.py`
- Source: `u300.json`, row `S21_mount_probe_local`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 253 against a baseline of 253
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_the_verb_recovers_both_halves_and_reports_them_apart`
  - `tests/test_restore_cli.py::test_the_verb_refuses_without_the_acceptance_flag`

Old text:

```
    probe = mount_probe or _restore()._is_mount_point
```

New text:

```
    probe = mount_probe or _is_mount_point
```

### `u96-b.C1_engine_terminal`

SAMPLE of the engine's guards, now reachable from a verb. bare_metal_session: disarm the controlling terminal refusal

- File: `src/cratekit/core/restore_recovery.py`
- Source: `u96-b.json`, row `C1_engine_terminal`
- Moved: Moved from src/cratekit/core/restore.py to src/cratekit/core/restore_recovery.py by U300, which replayed this text there and kept the kill in u300-replay-after-c.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`
- Collected: 253 against a baseline of 253
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

- File: `src/cratekit/core/restore_recovery.py`
- Source: `u96-b.json`, row `C2_engine_acknowledged`
- Moved: Moved from src/cratekit/core/restore.py to src/cratekit/core/restore_recovery.py by U300, which replayed this text there and kept the kill in u300-replay-after-c.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`
- Collected: 253 against a baseline of 253
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

- File: `src/cratekit/core/restore_recovery.py`
- Source: `u96-b.json`, row `C3_engine_occupied_target`
- Moved: Moved from src/cratekit/core/restore.py to src/cratekit/core/restore_recovery.py by U300, which replayed this text there and kept the kill in u300-replay-after-c.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`
- Collected: 253 against a baseline of 253
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

- File: `src/cratekit/core/restore_recovery.py`
- Source: `u96-b.json`, row `C4_engine_stub`
- Moved: Moved from src/cratekit/core/restore.py to src/cratekit/core/restore_recovery.py by U300, which replayed this text there and kept the kill in u300-replay-after-c.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`
- Collected: 253 against a baseline of 253
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

- File: `src/cratekit/core/restore_recovery.py`
- Source: `u96-b.json`, row `C5_engine_library_is_mounted`
- Moved: Moved from src/cratekit/core/restore.py to src/cratekit/core/restore_recovery.py by U300, which replayed this text there and kept the kill in u300-replay-after-c.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`
- Collected: 253 against a baseline of 253
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

### `r1255.S1_scan_unlisted_as_empty`

scan_log: answer a log it is refused as no record and none unread, the defect itself

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S1_scan_unlisted_as_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_unmirrored.py`, `tests/test_intake_shelve.py`, `tests/test_tree_registry.py`, `tests/test_doctor.py`, `tests/test_restore.py`, `tests/test_write_session.py`
- Collected: 867 against a baseline of 867
- Kills: 14 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_session_log_this_account_cannot_list_is_failed_by_its_own_check`
  - `tests/test_doctor.py::test_status_names_a_session_log_it_cannot_list_and_still_reports_the_rest`
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`
  - `tests/test_session_log_unlisted.py::test_a_listed_log_is_read_a_missing_one_is_no_record_and_a_file_in_its_place_is_unread`
  - `tests/test_session_log_unlisted.py::test_a_log_that_cannot_be_listed_is_the_one_unread_entry_and_its_clause_says_so`
  - `tests/test_session_log_unlisted.py::test_every_destructive_session_is_refused_at_its_gate`
  - `tests/test_session_log_unlisted.py::test_every_gate_refuses_a_log_it_cannot_list[closed-detail1-<lambda>-2026-10-20 Tidal playlists 2-so no batch name can be called free]`
  - `tests/test_session_log_unlisted.py::test_every_gate_refuses_a_log_it_cannot_list[committed-unverified-None-<lambda>-session-committed-unverified-cannot vouch that no session ended unresolved]`
  - `tests/test_session_log_unlisted.py::test_every_gate_refuses_a_log_it_cannot_list[open-None-<lambda>-readable2-so whether a run is still open was not established]`
  - `tests/test_session_log_unlisted.py::test_restore_list_and_run_refuse_a_log_they_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_check_refuses_an_unknown_landing_naming_the_listing`
  - `tests/test_session_log_unlisted.py::test_the_native_landing_lookups_refuse_a_log_they_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_reporting_reader_refuses_a_log_it_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_rotation_reads_the_listing_from_the_scan`

Old text:

```
        logger.debug("session log %s could not be listed: %s", directory, exc)
        return (), (directory,)
```

New text:

```
        logger.debug("session log %s could not be listed: %s", directory, exc)
        return (), ()
```

### `r1255.S2_absent_log_unread`

_listed: read a log that is not there as refused, so a library with no session refuses every write

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S2_absent_log_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_unmirrored.py`, `tests/test_intake_shelve.py`, `tests/test_tree_registry.py`, `tests/test_doctor.py`, `tests/test_restore.py`, `tests/test_write_session.py`
- Collected: 867 against a baseline of 867
- Kills: 46 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_green_doctor_exits_zero`
  - `tests/test_doctor.py::test_a_headless_machine_that_opted_into_the_environment_fallback_is_not_red`
  - `tests/test_doctor.py::test_a_library_with_no_sessions_still_reports_a_clean_log`
  - `tests/test_doctor.py::test_a_re_run_repairs_a_spelled_remote_rclone_does_not_know`
  - `tests/test_doctor.py::test_a_second_setup_run_asks_nothing_and_changes_nothing_it_was_not_asked_to`
  - `tests/test_doctor.py::test_an_empty_credential_leaves_the_exit_code_to_doctor`
  - `tests/test_doctor.py::test_no_ok_detail_claims_a_volume_the_run_never_identified`
  - `tests/test_doctor.py::test_the_backup_flags_are_recorded_without_a_question`
  - `tests/test_doctor.py::test_the_disagreeing_remote_refusal_names_the_flag_and_the_flag_repairs_it`
  - `tests/test_doctor.py::test_the_strong_claim_survives_where_the_identity_really_was_compared`
  - `tests/test_doctor.py::test_the_wizard_on_a_clean_machine_produces_a_valid_config_and_a_green_doctor`
  - `tests/test_inbox_unmirrored.py::test_a_dated_playlist_with_no_batch_folder_still_says_so`
  - `tests/test_inbox_unmirrored.py::test_an_absent_session_log_is_no_record_at_all`
  - `tests/test_inbox_unmirrored.py::test_the_live_batches_name_every_other_node_under_inbox_with_its_kind`
  - `tests/test_intake_shelve.py::test_a_library_whose_drive_was_renamed_stores_and_confines_under_the_base_drive`
  - ... and 31 more, see the JSON sidecar

Old text:

```
        return os.listdir(directory)
    except FileNotFoundError:
        return None
```

New text:

```
        return os.listdir(directory)
    except FileNotFoundError:
        raise
```

### `r1255.S3_log_file_absent`

_listed: read a log path that is itself a file as not there, so it is no record

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S3_log_file_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_doctor.py`
- Collected: 432 against a baseline of 432
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_a_listed_log_is_read_a_missing_one_is_no_record_and_a_file_in_its_place_is_unread`

Old text:

```
        if os.path.lexists(directory):
            raise
        return None
```

New text:

```
        return None
```

### `r1255.S4_under_a_file_unread`

_listed: read a log under a file as there and refused, rather than not there

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S4_under_a_file_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_doctor.py`
- Collected: 432 against a baseline of 432
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_a_listed_log_is_read_a_missing_one_is_no_record_and_a_file_in_its_place_is_unread`

Old text:

```
        if os.path.lexists(directory):
            raise
        return None
```

New text:

```
        raise
```

### `r1255.S5_json_filter`

scan_log: read every name in the log as a record, so a stray file reads as an unreadable record

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S5_json_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_unmirrored.py`, `tests/test_intake_shelve.py`, `tests/test_tree_registry.py`, `tests/test_doctor.py`, `tests/test_restore.py`, `tests/test_write_session.py`
- Collected: 867 against a baseline of 867
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_a_listed_log_is_read_a_missing_one_is_no_record_and_a_file_in_its_place_is_unread`

Old text:

```
    entries = sorted(directory / name for name in names if fnmatch.fnmatchcase(name, "*.json"))
```

New text:

```
    entries = sorted(directory / name for name in names)
```

### `r1255.S6_records_refuses_unlisted`

records: answer an unlisted log as no session again, so restore list, restore run and session release read it as empty

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S6_records_refuses_unlisted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_session_cli.py`, `tests/test_restore.py`, `tests/test_doctor.py`
- Collected: 628 against a baseline of 628
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_session_log_that_cannot_be_listed_refuses_the_release_before_its_question`
  - `tests/test_session_log_unlisted.py::test_restore_list_and_run_refuse_a_log_they_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_native_landing_lookups_refuse_a_log_they_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_reporting_reader_refuses_a_log_it_cannot_list`

Old text:

```
    if log_unlisted(unreadable, cfg):
        raise refuse(
```

New text:

```
    if False:
        raise refuse(
```

### `r1255.S7_log_unlisted_predicate`

log_unlisted: never name the unread half as the log, so every refusal counts it as one entry

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S7_log_unlisted_predicate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_unmirrored.py`, `tests/test_intake_shelve.py`, `tests/test_tree_registry.py`
- Collected: 143 against a baseline of 143
- Kills: 11 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`
  - `tests/test_session_log_unlisted.py::test_a_log_that_cannot_be_listed_is_the_one_unread_entry_and_its_clause_says_so`
  - `tests/test_session_log_unlisted.py::test_every_destructive_session_is_refused_at_its_gate`
  - `tests/test_session_log_unlisted.py::test_every_gate_refuses_a_log_it_cannot_list[closed-detail1-<lambda>-2026-10-20 Tidal playlists 2-so no batch name can be called free]`
  - `tests/test_session_log_unlisted.py::test_every_gate_refuses_a_log_it_cannot_list[committed-unverified-None-<lambda>-session-committed-unverified-cannot vouch that no session ended unresolved]`
  - `tests/test_session_log_unlisted.py::test_every_gate_refuses_a_log_it_cannot_list[open-None-<lambda>-readable2-so whether a run is still open was not established]`
  - `tests/test_session_log_unlisted.py::test_restore_list_and_run_refuse_a_log_they_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_check_refuses_an_unknown_landing_naming_the_listing`
  - `tests/test_session_log_unlisted.py::test_the_native_landing_lookups_refuse_a_log_they_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_reporting_reader_refuses_a_log_it_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_rotation_reads_the_listing_from_the_scan`

Old text:

```
    return log_dir(cfg) in unreadable
```

New text:

```
    return False
```

### `r1255.S8_clause_listing_wording`

unread_clause: word an unlisted log as the count of entries, so a gate sends a person to a damaged file

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S8_clause_listing_wording`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_intake_shelve.py`, `tests/test_tree_registry.py`
- Collected: 116 against a baseline of 116
- Kills: 8 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_a_log_that_cannot_be_listed_is_the_one_unread_entry_and_its_clause_says_so`
  - `tests/test_session_log_unlisted.py::test_every_destructive_session_is_refused_at_its_gate`
  - `tests/test_session_log_unlisted.py::test_every_gate_refuses_a_log_it_cannot_list[closed-detail1-<lambda>-2026-10-20 Tidal playlists 2-so no batch name can be called free]`
  - `tests/test_session_log_unlisted.py::test_every_gate_refuses_a_log_it_cannot_list[committed-unverified-None-<lambda>-session-committed-unverified-cannot vouch that no session ended unresolved]`
  - `tests/test_session_log_unlisted.py::test_every_gate_refuses_a_log_it_cannot_list[open-None-<lambda>-readable2-so whether a run is still open was not established]`
  - `tests/test_session_log_unlisted.py::test_restore_list_and_run_refuse_a_log_they_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_native_landing_lookups_refuse_a_log_they_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_reporting_reader_refuses_a_log_it_cannot_list`

Old text:

```
        return "the session log exists and cannot be listed by this account"
```

New text:

```
        return "the session log holds 1 entry this build cannot read"
```

### `r1255.S9_gate_unlisted_detail`

assert_no_unresolved_session: drop the unlisted flag from the refusal's detail

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S9_gate_unlisted_detail`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_restore.py`, `tests/test_write_session.py`
- Collected: 322 against a baseline of 322
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_an_unreadable_record_keeps_its_own_refusal`
  - `tests/test_session_log_unlisted.py::test_every_gate_refuses_a_log_it_cannot_list[committed-unverified-None-<lambda>-session-committed-unverified-cannot vouch that no session ended unresolved]`

Old text:

```
                "unreadable": [str(path) for path in unreadable],
                "unlisted": log_unlisted(unreadable, cfg),
            },
        )


def resolve_unverified_session(
```

New text:

```
                "unreadable": [str(path) for path in unreadable],
            },
        )


def resolve_unverified_session(
```

### `r239-b.S11_readback_key_on`

the session read-back pins the old True default, which a plain database cannot open under

- File: `src/cratekit/core/session.py`
- Source: `r239-b.json`, row `S11_readback_key_on`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_adopt_apply_cli.py`
- Collected: 723 against a baseline of 723
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_no_caller_in_src_answers_the_key_question_for_itself`

Old text:

```
    open_fresh = reopen or (lambda: rb_writer.open_db(cfg=cfg))
```

New text:

```
    open_fresh = reopen or (lambda: rb_writer.open_db(cfg=cfg, unlock=True))
```

### `r375-a.S10_commit_not_persisted_at_once`

record_commit: mark the source in memory and leave the write to the close, so a hard kill after the commit leaves a record that claims none

- File: `src/cratekit/core/session.py`
- Source: `r375-a.json`, row `S10_commit_not_persisted_at_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`, `tests/test_restore.py`
- Collected: 393 against a baseline of 393
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
- Collected: 393 against a baseline of 393
- Kills: 3 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_a_moves_removal_commit_that_lands_and_then_raises_is_still_recorded`
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
- Collected: 393 against a baseline of 393
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
  - `tests/test_tree_writer.py::test_a_commit_that_lands_and_then_raises_is_still_recorded_as_committed`
  - `tests/test_tree_writer.py::test_a_failure_after_the_commit_still_reads_as_committed_work`
  - `tests/test_tree_writer.py::test_a_failure_mid_loop_leaves_nothing_pending_on_the_handle`
  - `tests/test_tree_writer.py::test_a_grid_rewritten_during_a_membership_write_refuses_the_session`
  - `tests/test_tree_writer.py::test_a_membership_write_is_listed_as_restorable_with_its_per_tree_counts`
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
- Collected: 393 against a baseline of 393
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
- Collected: 393 against a baseline of 393
- Kills: 13 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_an_apply_that_refuses_mid_write_is_abandoned_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_apply_whose_commit_lands_and_then_raises_is_recorded_as_committed`
  - `tests/test_restore.py::test_a_restore_the_analysis_watch_refuses_is_not_on_record_as_finished`
  - `tests/test_restore.py::test_the_recovery_session_closes_its_own_record_on_both_paths`
  - `tests/test_tree_writer.py::test_a_commit_that_lands_and_then_raises_is_still_recorded_as_committed`
  - `tests/test_tree_writer.py::test_a_failure_after_the_commit_still_reads_as_committed_work`
  - `tests/test_tree_writer.py::test_a_grid_rewritten_during_a_membership_write_refuses_the_session`
  - `tests/test_tree_writer.py::test_a_membership_write_that_fails_is_abandoned_and_claims_no_commit`
  - `tests/test_tree_writer.py::test_a_write_that_fails_after_counting_a_membership_still_claims_no_commit`
  - `tests/test_tree_writer.py::test_the_write_commits_behind_a_verified_capture`
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
- Collected: 393 against a baseline of 393
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
- Collected: 393 against a baseline of 393
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
- Collected: 393 against a baseline of 393
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
- Collected: 393 against a baseline of 393
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
- Collected: 393 against a baseline of 393
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
- Collected: 393 against a baseline of 393
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

### `r501-a.S1_verify_state_guard`

session.mark_import_verified: drop the refusal of any state but awaiting-import, so any record can be marked proven

- File: `src/cratekit/core/session.py`
- Source: `r501-a.json`, row `S1_verify_state_guard`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 134 against a baseline of 134
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_only_a_run_waiting_on_an_import_has_one_to_verify`

Old text:

```
    if record.state is not SessionState.AWAITING_IMPORT:
        raise refuse(
            "internal-error",
            f"session {record.session_id} is {str(record.state)!r}, not "
            f"{str(SessionState.AWAITING_IMPORT)!r}; only a session waiting on an "
            f"import has one to verify",
```

New text:

```
    if False:
        raise refuse(
            "internal-error",
            f"session {record.session_id} is {str(record.state)!r}, not "
            f"{str(SessionState.AWAITING_IMPORT)!r}; only a session waiting on an "
            f"import has one to verify",
```

### `r501-a.S2_excusal_capture`

session.owes_only_deferred_routing: drop the no capture condition, so a run holding a capture is excused from the cutover precheck

- File: `src/cratekit/core/session.py`
- Source: `r501-a.json`, row `S2_excusal_capture`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 134 against a baseline of 134
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_the_precheck_refuses_a_verified_run_that_holds_a_capture[holding-a-capture]`

Old text:

```
        record.state is SessionState.OPEN
        and record.snapshot_path is None
        and IMPORT_VERIFIED_KEY in record.detail
```

New text:

```
        record.state is SessionState.OPEN
        and IMPORT_VERIFIED_KEY in record.detail
```

### `r501-a.S3_excusal_proof`

session.owes_only_deferred_routing: drop the proof condition, so any open run with no capture is excused, a crashed landing included

- File: `src/cratekit/core/session.py`
- Source: `r501-a.json`, row `S3_excusal_proof`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 134 against a baseline of 134
- Kills: 5 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_an_open_run_blocks_the_flip`
  - `tests/test_cutover_precheck.py::test_an_open_run_refuses_the_revert_because_it_may_have_written`
  - `tests/test_intake_imported.py::test_a_run_landed_before_the_fix_is_settled_too`
  - `tests/test_intake_imported.py::test_doctor_reads_a_proven_run_as_proven_and_not_as_in_progress`
  - `tests/test_intake_imported.py::test_the_precheck_refuses_an_open_run_with_no_proof_recorded`

Old text:

```
        record.state is SessionState.OPEN
        and record.snapshot_path is None
        and IMPORT_VERIFIED_KEY in record.detail
```

New text:

```
        record.state is SessionState.OPEN
        and record.snapshot_path is None
```

### `r501-a.S4_excusal_state`

session.owes_only_deferred_routing: drop the open state condition, so a committed-unverified run carrying the key is excused

- File: `src/cratekit/core/session.py`
- Source: `r501-a.json`, row `S4_excusal_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 134 against a baseline of 134
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_the_precheck_refuses_a_verified_run_that_holds_a_capture[not-open]`

Old text:

```
        record.state is SessionState.OPEN
        and record.snapshot_path is None
        and IMPORT_VERIFIED_KEY in record.detail
```

New text:

```
        record.snapshot_path is None
        and IMPORT_VERIFIED_KEY in record.detail
```

### `r598-a.A5_holder_never_recorded`

open_session: drop the holder instead of recording it, so no record is ever provably orphaned and a hard kill is a dead end again

- File: `src/cratekit/core/session.py`
- Source: `r598-a.json`, row `A5_holder_never_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 8 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_open_session_whose_process_is_gone_names_the_verb_that_ends_it`
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[hard-kill]`
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[power-loss]`
  - `tests/test_session_cli.py::test_a_release_that_only_abandons_is_a_change_and_passes_the_contract`
  - `tests/test_write_session.py::test_a_supplied_holder_reaches_the_record_as_well_as_the_lock`
  - `tests/test_write_session.py::test_abandon_orphaned_sessions_ends_only_the_orphans`
  - `tests/test_write_session.py::test_the_record_names_the_holder_the_lock_names`
  - `tests/test_write_session.py::test_the_sweep_ends_only_the_orphans_it_was_shown`

Old text:

```
        detail={HOLDER_KEY: holder.to_json()} if holder is not None else {},
```

New text:

```
        detail={},
```

### `r598-a.A6_record_holder_is_a_second_lookup`

assert_gates: record current_holder() in the record rather than the claimant the lock took, so a supplied holder splits the two copies

- File: `src/cratekit/core/session.py`
- Source: `r598-a.json`, row `A6_record_holder_is_a_second_lookup`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`
- Collected: 185 against a baseline of 185
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_supplied_holder_reaches_the_record_as_well_as_the_lock`

Old text:

```
                holder=claimant,
                intent=intent,
```

New text:

```
                holder=current_holder(),
                intent=intent,
```

### `u138-rerun.S5_bound_exclusive`

A portion exactly five days old is under the bound

- File: `src/cratekit/core/session_ack.py`
- Source: `u138-rerun.json`, row `S5_bound_exclusive`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_ack.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4023 against a baseline of 4023
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_the_bound_is_strict_at_exactly_five_days[exactly-five-days]`

Old text:

```
        elif entry.age_seconds >= limit:

```

New text:

```
        elif entry.age_seconds > limit:

```

### `u138.E1_terminal_check`

Existing guard sample: the terminal check on a person's answer

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `E1_terminal_check`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_ack.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4023 against a baseline of 4023
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_a_person_without_a_terminal_is_still_refused_over_fresh_backups`
  - `tests/test_session_cli.py::test_the_answering_invocation_refuses_when_nobody_is_there`
  - `tests/test_write_session.py::test_an_agent_shaped_invocation_cannot_mint_the_acknowledgment`
  - `tests/test_write_session.py::test_the_terminal_probe_the_mint_uses_by_default_is_the_real_one`

Old text:

```
        if not probe():

```

New text:

```
        if False:

```

### `u138.S10_older_record_reads_as_session`

A record from before U138 reads as minted by the session's rule

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S10_older_record_reads_as_session`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_ack.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4023 against a baseline of 4023
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_a_record_written_before_u138_reads_as_the_terminal_rule`

Old text:

```
            rule=str(data.get("rule") or RULE_TERMINAL),

```

New text:

```
            rule=str(data.get("rule") or RULE_SESSION_AGES),

```

### `u138.S11_rule_not_written`

The record's rule key is not written to the file

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S11_rule_not_written`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_ack.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4023 against a baseline of 4023
- Kills: 4 (killed)
- Killed:
  - `tests/test_doctor.py::test_doctor_shows_the_acknowledgments_expiry_beside_the_two_backup_ages`
  - `tests/test_session_ack_by_session.py::test_an_unreadable_acknowledgment_is_replaced_by_one_command`
  - `tests/test_session_ack_by_session.py::test_one_command_mints_as_the_session_when_both_ages_are_four_days`
  - `tests/test_session_ack_by_session.py::test_the_session_mints_with_no_terminal_when_both_ages_are_under_five_days`

Old text:

```
            "rule": self.rule,

```

New text:

```
(empty)
```

### `u138.S12_message_names_the_portion`

Reword the refusal so it no longer names the portion's age

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S12_message_names_the_portion`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_ack.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4023 against a baseline of 4023
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[files-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-exactly-five]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[files-six-days]`

Old text:

```
                f"the {entry.portion} portion is {entry.age_seconds / 86400:.1f} days old"

```

New text:

```
                f"a backup portion is too old ({entry.portion})"

```

### `u138.S13_remedy_points_back_at_ack`

The too old refusal tells a person to acknowledge again rather than to run a backup

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S13_remedy_points_back_at_ack`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_ack.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4023 against a baseline of 4023
- Kills: 8 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[both-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[files-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-exactly-five]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-never-recorded]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-recorded-in-the-future]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[files-six-days]`

Old text:

```
                remedy=Remedy.RUN_BACKUP,

```

New text:

```
                remedy=Remedy.ACKNOWLEDGE_BACKUP,

```

### `u138.S1_session_rule_gone`

A session's answer falls to the terminal check, as before U138

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S1_session_rule_gone`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_ack.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4023 against a baseline of 4023
- Kills: 20 (killed)
- Killed:
  - `tests/test_doctor.py::test_doctor_names_when_an_acknowledgment_lapsed`
  - `tests/test_doctor.py::test_doctor_shows_the_acknowledgments_expiry_beside_the_two_backup_ages`
  - `tests/test_doctor.py::test_no_acknowledgment_is_claimed_absent_off_a_volume_nobody_read`
  - `tests/test_session_ack_by_session.py::test_a_session_with_a_terminal_is_still_held_to_the_ages`
  - `tests/test_session_ack_by_session.py::test_an_expired_acknowledgment_is_replaced_by_one_command`
  - `tests/test_session_ack_by_session.py::test_an_unreadable_acknowledgment_is_replaced_by_one_command`
  - `tests/test_session_ack_by_session.py::test_one_command_mints_as_the_session_when_both_ages_are_four_days`
  - `tests/test_session_ack_by_session.py::test_one_command_prints_the_expiry_a_person_reads`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[both-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[files-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_reports_a_valid_acknowledgment_and_does_not_mint_again`
  - `tests/test_session_ack_by_session.py::test_the_bound_is_strict_at_exactly_five_days[a-second-under-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_bound_is_strict_at_exactly_five_days[exactly-five-days]`
  - ... and 5 more, see the JSON sidecar

Old text:

```
    if decided_by == SESSION_ACTOR:

```

New text:

```
    if False:

```

### `u138.S2_any_answer_gets_the_age_rule`

Any recorded answer, a person's included, mints without a terminal on young backups

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S2_any_answer_gets_the_age_rule`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_ack.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4023 against a baseline of 4023
- Kills: 13 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[session.ack]`
  - `tests/test_session_ack_by_session.py::test_a_person_at_a_terminal_mints_by_the_terminal_rule_and_the_record_says_so`
  - `tests/test_session_ack_by_session.py::test_a_person_without_a_terminal_is_still_refused_over_fresh_backups`
  - `tests/test_session_ack_by_session.py::test_a_valid_acknowledgment_a_person_minted_is_reported_over_old_backups`
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[hard-kill]`
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[power-loss]`
  - `tests/test_session_cli.py::test_a_damaged_acknowledgment_record_can_still_be_replaced`
  - `tests/test_session_cli.py::test_a_second_mint_replaces_the_record_and_moves_the_window`
  - `tests/test_session_cli.py::test_a_spent_acknowledgment_decision_cannot_be_replayed`
  - `tests/test_session_cli.py::test_the_answering_invocation_refuses_when_nobody_is_there`
  - `tests/test_session_cli.py::test_the_check_rows_a_person_reads_name_the_portion`
  - `tests/test_session_cli.py::test_the_cli_mints_an_acknowledgment_a_real_destructive_verb_then_spends`
  - `tests/test_session_cli.py::test_the_refusal_names_the_acknowledgment_on_record_in_all_three_states`

Old text:

```
    if decided_by == SESSION_ACTOR:

```

New text:

```
    if decided_by is not None:

```

### `u138.S3_stale_not_refused`

The session mints over a portion five days old or of unknown age

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S3_stale_not_refused`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_ack.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4023 against a baseline of 4023
- Kills: 10 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_a_session_with_a_terminal_is_still_held_to_the_ages`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[both-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[files-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_bound_is_strict_at_exactly_five_days[exactly-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-exactly-five]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-never-recorded]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-recorded-in-the-future]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[files-six-days]`

Old text:

```
        if stale:
```

New text:

```
        if False:
```

### `u138.S6_bound_six_days`

The bound is six days rather than five

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S6_bound_six_days`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_ack.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4023 against a baseline of 4023
- Kills: 5 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[files-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_bound_is_five_days_as_the_author_set_it`
  - `tests/test_session_ack_by_session.py::test_the_bound_is_strict_at_exactly_five_days[exactly-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-exactly-five]`

Old text:

```
SESSION_MAX_BACKUP_AGE = timedelta(days=5)

```

New text:

```
SESSION_MAX_BACKUP_AGE = timedelta(days=6)

```

### `u138.S8_rule_not_recorded`

The record always says the terminal rule minted it

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S8_rule_not_recorded`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_ack.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4023 against a baseline of 4023
- Kills: 6 (killed)
- Killed:
  - `tests/test_doctor.py::test_doctor_shows_the_acknowledgments_expiry_beside_the_two_backup_ages`
  - `tests/test_session_ack_by_session.py::test_an_unreadable_acknowledgment_is_replaced_by_one_command`
  - `tests/test_session_ack_by_session.py::test_one_command_mints_as_the_session_when_both_ages_are_four_days`
  - `tests/test_session_ack_by_session.py::test_one_command_prints_the_expiry_a_person_reads`
  - `tests/test_session_ack_by_session.py::test_the_bound_is_strict_at_exactly_five_days[a-second-under-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_session_mints_with_no_terminal_when_both_ages_are_under_five_days`

Old text:

```
        shown=shown,
        rule=rule,

```

New text:

```
        shown=shown,
        rule=RULE_TERMINAL,

```

### `u138.S9_answer_not_recorded`

The record never says who answered the gate

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S9_answer_not_recorded`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_ack.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4023 against a baseline of 4023
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_a_person_at_a_terminal_mints_by_the_terminal_rule_and_the_record_says_so`
  - `tests/test_session_ack_by_session.py::test_one_command_mints_as_the_session_when_both_ages_are_four_days`
  - `tests/test_session_ack_by_session.py::test_the_bound_is_strict_at_exactly_five_days[a-second-under-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_session_mints_with_no_terminal_when_both_ages_are_under_five_days`

Old text:

```
        rule=rule,
        decided_by=decided_by,

```

New text:

```
        rule=rule,
        decided_by=None,

```

### `u300.S15_terminal_probe_local`

record_acknowledgment asks the part's own terminal probe, so a patched probe is not asked

- File: `src/cratekit/core/session_ack.py`
- Source: `u300.json`, row `S15_terminal_probe_local`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`
- Collected: 185 against a baseline of 185
- Kills: 10 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[hard-kill]`
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[power-loss]`
  - `tests/test_session_cli.py::test_a_damaged_acknowledgment_record_can_still_be_replaced`
  - `tests/test_session_cli.py::test_a_second_mint_replaces_the_record_and_moves_the_window`
  - `tests/test_session_cli.py::test_a_spent_acknowledgment_decision_cannot_be_replayed`
  - `tests/test_session_cli.py::test_the_answering_invocation_refuses_when_nobody_is_there`
  - `tests/test_session_cli.py::test_the_check_rows_a_person_reads_name_the_portion`
  - `tests/test_session_cli.py::test_the_cli_mints_an_acknowledgment_a_real_destructive_verb_then_spends`
  - `tests/test_session_cli.py::test_the_refusal_names_the_acknowledgment_on_record_in_all_three_states`
  - `tests/test_write_session.py::test_the_terminal_probe_the_mint_uses_by_default_is_the_real_one`

Old text:

```
        probe = terminal or _session().has_controlling_terminal
```

New text:

```
        probe = terminal or has_controlling_terminal
```

### `u300.S16_derive_actor_local`

record_acknowledgment names its actor with the part's own derive_actor

- File: `src/cratekit/core/session_ack.py`
- Source: `u300.json`, row `S16_derive_actor_local`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`
- Collected: 185 against a baseline of 185
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_the_recorded_actor_is_the_derived_one_and_not_a_name_from_anywhere_else`

Old text:

```
        actor=_session().derive_actor(),
```

New text:

```
        actor=derive_actor(),
```

### `u48-author.S1_remedy_fixed_at_repair`

The session names the repair token again, which is the defect this unit closed

- File: `src/cratekit/core/session_ack.py`
- Source: `u48-author.json`, row `S1_remedy_fixed_at_repair`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_ack.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_backup_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 1533 against a baseline of 1533
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_fact_file_from_a_newer_build_asks_for_an_upgrade`

Old text:

```
            remedy=Remedy(str(exc.remedy)),
```

New text:

```
            remedy=Remedy.REPAIR_BACKUP_FACTS,
```

### `u48-author.S2_remedy_fixed_at_grant`

The same defect mirrored: hard code the permission token over every condition

- File: `src/cratekit/core/session_ack.py`
- Source: `u48-author.json`, row `S2_remedy_fixed_at_grant`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_ack.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_backup_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 1533 against a baseline of 1533
- Kills: 2 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_fact_file_from_a_newer_build_asks_for_an_upgrade`
  - `tests/test_write_session.py::test_an_unreadable_backup_fact_file_refuses_the_mint`

Old text:

```
            remedy=Remedy(str(exc.remedy)),
```

New text:

```
            remedy=Remedy.GRANT_PATH_ACCESS,
```

### `r598-a.A1_state_check_widened_to_non_terminal`

orphaned: accept any non terminal record rather than only open, so awaiting-import and committed-unverified records with a dead holder are abandoned and their own remedies hidden

- File: `src/cratekit/core/session_holders.py`
- Source: `r598-a.json`, row `A1_state_check_widened_to_non_terminal`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_cli.py::test_the_two_states_with_their_own_remedy_are_never_abandoned[awaiting-import]`
  - `tests/test_session_cli.py::test_the_two_states_with_their_own_remedy_are_never_abandoned[committed-unverified]`
  - `tests/test_write_session.py::test_orphaned_needs_open_a_recorded_holder_and_proof_it_is_gone[awaiting-import-gone-False]`
  - `tests/test_write_session.py::test_orphaned_needs_open_a_recorded_holder_and_proof_it_is_gone[committed-unverified-gone-False]`

Old text:

```
    if record.state is not _session().SessionState.OPEN:
        return False
    recorded = record.detail.get(_session().HOLDER_KEY)
```

New text:

```
    if record.terminal:
        return False
    recorded = record.detail.get(_session().HOLDER_KEY)
```

### `r598-a.A2_no_holder_read_as_gone`

orphaned: read a record with no recorded holder as orphaned, so every intake landing left open for a deferred placement is abandoned

- File: `src/cratekit/core/session_holders.py`
- Source: `r598-a.json`, row `A2_no_holder_read_as_gone`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 3 (killed)
- Killed:
  - `tests/test_session_cli.py::test_an_open_record_that_names_no_holder_is_never_abandoned`
  - `tests/test_write_session.py::test_abandon_orphaned_sessions_ends_only_the_orphans`
  - `tests/test_write_session.py::test_orphaned_needs_open_a_recorded_holder_and_proof_it_is_gone[open-None-False]`

Old text:

```
    if not isinstance(recorded, Mapping):
        return False
```

New text:

```
    if not isinstance(recorded, Mapping):
        return True
```

### `r598-a.A3_liveness_not_consulted`

orphaned: skip holder_alive and judge every open record with a holder orphaned, so a running write's record is ended behind it

- File: `src/cratekit/core/session_holders.py`
- Source: `r598-a.json`, row `A3_liveness_not_consulted`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 8 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_open_session_whose_process_is_gone_names_the_verb_that_ends_it`
  - `tests/test_session_cli.py::test_a_record_not_proven_dead_on_this_machine_is_kept[alive]`
  - `tests/test_session_cli.py::test_a_record_not_proven_dead_on_this_machine_is_kept[another-machine-with-this-host-name]`
  - `tests/test_session_cli.py::test_a_record_not_proven_dead_on_this_machine_is_kept[recorded-before-the-machine-identity]`
  - `tests/test_write_session.py::test_abandon_orphaned_sessions_ends_only_the_orphans`
  - `tests/test_write_session.py::test_orphaned_needs_open_a_recorded_holder_and_proof_it_is_gone[open-here-False]`
  - `tests/test_write_session.py::test_orphaned_needs_open_a_recorded_holder_and_proof_it_is_gone[open-other-host-False]`
  - `tests/test_write_session.py::test_the_record_names_the_holder_the_lock_names`

Old text:

```
    return not holder_alive(holder, here=here)
```

New text:

```
    return True
```

### `r598-a.A4_unreadable_holder_read_as_gone`

orphaned: judge a holder this build cannot parse as gone rather than alive

- File: `src/cratekit/core/session_holders.py`
- Source: `r598-a.json`, row `A4_unreadable_holder_read_as_gone`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_orphaned_needs_open_a_recorded_holder_and_proof_it_is_gone[open-unreadable-False]`

Old text:

```
    except (TypeError, ValueError):
        return False
    return not holder_alive(holder, here=here)
```

New text:

```
    except (TypeError, ValueError):
        return True
    return not holder_alive(holder, here=here)
```

### `r598-a.A7_sweep_ignores_the_shown_list`

abandon_orphaned_sessions: end every orphan rather than only those shown, so one answer ends records the question never listed

- File: `src/cratekit/core/session_holders.py`
- Source: `r598-a.json`, row `A7_sweep_ignores_the_shown_list`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`
- Collected: 185 against a baseline of 185
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_the_sweep_ends_only_the_orphans_it_was_shown`

Old text:

```
        if (shown is None or record.session_id in shown) and orphaned(record, here=here)
```

New text:

```
        if orphaned(record, here=here)
```

### `r598-b.B7_sample_live_holder_released`

release_stale_lock: skip the live holder refusal (existing guard, sampled because the sweep now sits behind it)

- File: `src/cratekit/core/session_holders.py`
- Source: `r598-b.json`, row `B7_sample_live_holder_released`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`, `tests/test_write_session.py`
- Collected: 185 against a baseline of 185
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_live_holders_claim_is_refused_and_the_lock_file_is_untouched`
  - `tests/test_session_cli.py::test_a_refused_or_aborted_release_abandons_nothing[live-lock-holder]`
  - `tests/test_write_session.py::test_a_live_holder_this_platform_will_not_describe_is_assumed_alive`
  - `tests/test_write_session.py::test_the_lock_left_by_another_machine_with_this_host_name_is_not_releasable`

Old text:

```
    if holder_alive(recorded):
        raise refuse(
```

New text:

```
    if False:
        raise refuse(
```

### `r647-a.B10_live_identifier_not_asked`

_gone_since_an_earlier_boot: skip the live process check, so a live holder read through a moved clock has its claim cleared mid write

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B10_live_identifier_not_asked`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 3 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_live_process_read_through_a_moved_clock_is_kept`
  - `tests/test_write_session.py::test_a_live_process_whose_start_time_moved_with_the_clock_is_kept`
  - `tests/test_write_session.py::test_a_platform_that_cannot_say_whether_the_process_exists_keeps_it`

Old text:

```
    return _session().process_exists(holder.pid) is False
```

New text:

```
    return True
```

### `r647-a.B11_start_time_compared_again`

_gone_since_an_earlier_boot: the review's defect restored, a live identifier keeps the claim only when its start time matches, so the Linux shape of a stepped clock clears a live claim

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B11_start_time_compared_again`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_live_process_whose_start_time_moved_with_the_clock_is_kept`

Old text:

```
    return _session().process_exists(holder.pid) is False
```

New text:

```
    exists = _session().process_exists(holder.pid)
    if exists is None:
        return False
    return not (exists and _session().process_started(holder.pid) == holder.started)
```

