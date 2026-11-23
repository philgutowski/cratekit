# Mutation table: u300-replay-after-b

Measured by `scripts/mutate.py` on 2026-11-22 23:57 UTC, branch `HEAD` at `24710234`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 91.

Full baseline: measured by this driver (the battery's verdict was not read: no battery verdict at `.cloud-battery/verdict.json`).

Subset baselines: 16, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `/tmp/claude-0/-home-user-cratekit/1ecf30c5-f7fd-5fce-ae99-6064133b5c9c/scratchpad/known-failures-replay.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r1255.S1_scan_unlisted_as_empty` | `src/cratekit/core/session.py` | user | 7 file(s) | 893 | 16 | killed |
| `r1255.S2_absent_log_unread` | `src/cratekit/core/session.py` | user | 7 file(s) | 893 | 63 | killed |
| `r1255.S3_log_file_absent` | `src/cratekit/core/session.py` | user | 2 file(s) | 438 | 1 | killed |
| `r1255.S4_under_a_file_unread` | `src/cratekit/core/session.py` | user | 2 file(s) | 438 | 1 | killed |
| `r1255.S5_json_filter` | `src/cratekit/core/session.py` | user | 7 file(s) | 893 | 1 | killed |
| `r1255.S6_records_refuses_unlisted` | `src/cratekit/core/session.py` | user | 4 file(s) | 634 | 5 | killed |
| `r1255.S7_log_unlisted_predicate` | `src/cratekit/core/session.py` | user | 4 file(s) | 169 | 13 | killed |
| `r1255.S8_clause_listing_wording` | `src/cratekit/core/session.py` | user | 3 file(s) | 142 | 9 | killed |
| `r1255.S9_gate_unlisted_detail` | `src/cratekit/core/session.py` | maintainer | 3 file(s) | 328 | 2 | killed |
| `r239-b.S11_readback_key_on` | `src/cratekit/core/session.py` | user | 7 file(s) | 733 | 1 | killed |
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
| `r44-a.S1_empty_slot` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 475 | 2 | killed |
| `r44-a.S2_proved_widened` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 475 | 4 | killed |
| `r44-a.S3_default_to_library` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 475 | 2 | killed |
| `r44-a.S4_inside_root_unheld` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 475 | 6 | killed |
| `r44-a.S5_not_destructive` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 475 | 5 | killed |
| `r44-a.S7_probe_the_target` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 475 | 3 | killed |
| `r44-a.S8_wording_held_to` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 475 | 1 | killed |
| `r44-a.S9_offer_to_record_nested` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 475 | 1 | killed |
| `r501-a.S1_verify_state_guard` | `src/cratekit/core/session.py` | maintainer | 5 file(s) | 175 | 1 | killed |
| `r501-a.S2_excusal_capture` | `src/cratekit/core/session.py` | user | 5 file(s) | 175 | 1 | killed |
| `r501-a.S3_excusal_proof` | `src/cratekit/core/session.py` | user | 5 file(s) | 175 | 5 | killed |
| `r501-a.S4_excusal_state` | `src/cratekit/core/session.py` | user | 5 file(s) | 175 | 1 | killed |
| `r598-a.A2_no_holder_read_as_gone` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 3 | killed |
| `r598-a.A3_liveness_not_consulted` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 8 | killed |
| `r598-a.A4_unreadable_holder_read_as_gone` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 1 | killed |
| `r598-a.A5_holder_never_recorded` | `src/cratekit/core/session.py` | user | 3 file(s) | 602 | 8 | killed |
| `r598-a.A6_record_holder_is_a_second_lookup` | `src/cratekit/core/session.py` | maintainer | 2 file(s) | 185 | 1 | killed |
| `r598-a.A7_sweep_ignores_the_shown_list` | `src/cratekit/core/session_holders.py` | user | 2 file(s) | 185 | 1 | killed |
| `r598-b.B7_sample_live_holder_released` | `src/cratekit/core/session_holders.py` | user | 2 file(s) | 185 | 4 | killed |
| `r647-a.B12_cross_boot_never_judged` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 4 | killed |
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
| `u138-rerun.S5_bound_exclusive` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4220 | 1 | killed |
| `u138.E1_terminal_check` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4220 | 4 | killed |
| `u138.S10_older_record_reads_as_session` | `src/cratekit/core/session_ack.py` | maintainer | 43 file(s) | 4220 | 1 | killed |
| `u138.S11_rule_not_written` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4220 | 4 | killed |
| `u138.S12_message_names_the_portion` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4220 | 4 | killed |
| `u138.S13_remedy_points_back_at_ack` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4220 | 8 | killed |
| `u138.S1_session_rule_gone` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4220 | 20 | killed |
| `u138.S2_any_answer_gets_the_age_rule` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4220 | 13 | killed |
| `u138.S6_bound_six_days` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4220 | 5 | killed |
| `u138.S8_rule_not_recorded` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4220 | 6 | killed |
| `u138.S9_answer_not_recorded` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4220 | 4 | killed |
| `u49-author.L4_a_malformed_holder_raises_again` | `src/cratekit/core/session_holders.py` | user | 13 file(s) | 2589 | 1 | killed |
| `r44-a.S10_default_slug` | `src/cratekit/core/session_volumes.py` | maintainer | 2 file(s) | 475 | 1 | killed |
| `r44-a.S6_oserror_escapes` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 475 | 2 | killed |
| `r598-a.A1_state_check_widened_to_non_terminal` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 4 | killed |
| `r647-a.B10_live_identifier_not_asked` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 3 | killed |
| `r647-a.B11_start_time_compared_again` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 1 | killed |
| `r647-a.B13_current_holder_names_no_machine` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 3 | killed |
| `r647-a.B9_platform_silence_read_as_gone` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 1 | killed |
| `u138.S3_stale_not_refused` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4220 | 10 | killed |
| `u48-author.S1_remedy_fixed_at_repair` | `src/cratekit/core/session_ack.py` | user | 11 file(s) | 1555 | 1 | killed |
| `u48-author.S2_remedy_fixed_at_grant` | `src/cratekit/core/session_ack.py` | user | 11 file(s) | 1555 | 2 | killed |

## Row definitions

### `r1255.S1_scan_unlisted_as_empty`

scan_log: answer a log it is refused as no record and none unread, the defect itself

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S1_scan_unlisted_as_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_unmirrored.py`, `tests/test_intake_shelve.py`, `tests/test_tree_registry.py`, `tests/test_doctor.py`, `tests/test_restore.py`, `tests/test_write_session.py`
- Collected: 893 against a baseline of 893
- Kills: 16 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_session_log_this_account_cannot_list_is_failed_by_its_own_check`
  - `tests/test_doctor.py::test_status_names_a_session_log_it_cannot_list_and_still_reports_the_rest`
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`
  - `tests/test_session_log_unlisted.py::test_a_log_path_that_is_a_file_is_there_and_unread`
  - `tests/test_session_log_unlisted.py::test_a_log_that_cannot_be_listed_is_returned_as_the_one_unread_entry`
  - `tests/test_session_log_unlisted.py::test_every_destructive_session_is_refused_at_its_gate`
  - `tests/test_session_log_unlisted.py::test_restore_list_refuses_a_log_it_cannot_list_rather_than_list_nothing`
  - `tests/test_session_log_unlisted.py::test_restore_run_refuses_naming_the_listing_not_an_unrecorded_session`
  - `tests/test_session_log_unlisted.py::test_the_batch_name_rule_refuses_rather_than_call_a_name_free`
  - `tests/test_session_log_unlisted.py::test_the_check_refuses_an_unknown_landing_naming_the_listing`
  - `tests/test_session_log_unlisted.py::test_the_clause_names_the_listing_and_not_an_entry`
  - `tests/test_session_log_unlisted.py::test_the_native_landing_lookups_refuse_a_log_they_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_reporting_reader_refuses_a_log_it_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_rotation_reads_the_listing_from_the_scan`
  - `tests/test_session_log_unlisted.py::test_the_tree_registry_refuses_rather_than_read_no_open_run`
  - ... and 1 more, see the JSON sidecar

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
- Collected: 893 against a baseline of 893
- Kills: 63 (killed)
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
  - `tests/test_intake_shelve.py::test_a_batch_named_twice_is_planned_once`
  - ... and 48 more, see the JSON sidecar

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
- Collected: 438 against a baseline of 438
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_a_log_path_that_is_a_file_is_there_and_unread`

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
- Collected: 438 against a baseline of 438
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_a_log_under_a_file_is_not_there`

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
- Collected: 893 against a baseline of 893
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_a_listed_log_is_read_and_names_nothing_unlisted`

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
- Collected: 634 against a baseline of 634
- Kills: 5 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_session_log_that_cannot_be_listed_refuses_the_release_before_its_question`
  - `tests/test_session_log_unlisted.py::test_restore_list_refuses_a_log_it_cannot_list_rather_than_list_nothing`
  - `tests/test_session_log_unlisted.py::test_restore_run_refuses_naming_the_listing_not_an_unrecorded_session`
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
- Collected: 169 against a baseline of 169
- Kills: 13 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`
  - `tests/test_session_log_unlisted.py::test_a_log_that_cannot_be_listed_is_returned_as_the_one_unread_entry`
  - `tests/test_session_log_unlisted.py::test_every_destructive_session_is_refused_at_its_gate`
  - `tests/test_session_log_unlisted.py::test_restore_list_refuses_a_log_it_cannot_list_rather_than_list_nothing`
  - `tests/test_session_log_unlisted.py::test_restore_run_refuses_naming_the_listing_not_an_unrecorded_session`
  - `tests/test_session_log_unlisted.py::test_the_batch_name_rule_refuses_rather_than_call_a_name_free`
  - `tests/test_session_log_unlisted.py::test_the_check_refuses_an_unknown_landing_naming_the_listing`
  - `tests/test_session_log_unlisted.py::test_the_clause_names_the_listing_and_not_an_entry`
  - `tests/test_session_log_unlisted.py::test_the_native_landing_lookups_refuse_a_log_they_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_reporting_reader_refuses_a_log_it_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_rotation_reads_the_listing_from_the_scan`
  - `tests/test_session_log_unlisted.py::test_the_tree_registry_refuses_rather_than_read_no_open_run`
  - `tests/test_session_log_unlisted.py::test_the_unresolved_session_gate_refuses_over_a_log_it_cannot_list`

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
- Collected: 142 against a baseline of 142
- Kills: 9 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_every_destructive_session_is_refused_at_its_gate`
  - `tests/test_session_log_unlisted.py::test_restore_list_refuses_a_log_it_cannot_list_rather_than_list_nothing`
  - `tests/test_session_log_unlisted.py::test_restore_run_refuses_naming_the_listing_not_an_unrecorded_session`
  - `tests/test_session_log_unlisted.py::test_the_batch_name_rule_refuses_rather_than_call_a_name_free`
  - `tests/test_session_log_unlisted.py::test_the_clause_names_the_listing_and_not_an_entry`
  - `tests/test_session_log_unlisted.py::test_the_native_landing_lookups_refuse_a_log_they_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_reporting_reader_refuses_a_log_it_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_tree_registry_refuses_rather_than_read_no_open_run`
  - `tests/test_session_log_unlisted.py::test_the_unresolved_session_gate_refuses_over_a_log_it_cannot_list`

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
- Collected: 328 against a baseline of 328
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_an_unreadable_record_keeps_its_own_refusal`
  - `tests/test_session_log_unlisted.py::test_the_unresolved_session_gate_refuses_over_a_log_it_cannot_list`

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
- Collected: 733 against a baseline of 733
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

### `r44-a.S1_empty_slot`

Never refuse an empty mount slot, so an identity read through an ejected drive's leftover directory is compared and can match

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S1_empty_slot`
- Moved: the same text, now in src/cratekit/core/session_volumes.py, was in src/cratekit/core/session.py
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

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S2_proved_widened`
- Moved: the same text, now in src/cratekit/core/session_volumes.py, was in src/cratekit/core/session.py
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

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S3_default_to_library`
- Moved: the same text, now in src/cratekit/core/session_volumes.py, was in src/cratekit/core/session.py
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

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S4_inside_root_unheld`
- Moved: the same text, now in src/cratekit/core/session_volumes.py, was in src/cratekit/core/session.py
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

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S5_not_destructive`
- Moved: the same text, now in src/cratekit/core/session_volumes.py, was in src/cratekit/core/session.py
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

### `r44-a.S7_probe_the_target`

Probe the rule's target for a file instead of the file's own directory, so a volume nested under the target is never seen

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S7_probe_the_target`
- Moved: the same text, now in src/cratekit/core/session_volumes.py, was in src/cratekit/core/session.py
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

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S8_wording_held_to`
- Moved: the same text, now in src/cratekit/core/session_volumes.py, was in src/cratekit/core/session.py
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

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S9_offer_to_record_nested`
- Moved: the same text, now in src/cratekit/core/session_volumes.py, was in src/cratekit/core/session.py
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

### `r501-a.S1_verify_state_guard`

session.mark_import_verified: drop the refusal of any state but awaiting-import, so any record can be marked proven

- File: `src/cratekit/core/session.py`
- Source: `r501-a.json`, row `S1_verify_state_guard`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 175 against a baseline of 175
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
- Collected: 175 against a baseline of 175
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_the_precheck_refuses_a_verified_run_that_holds_a_capture`

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
- Collected: 175 against a baseline of 175
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
- Collected: 175 against a baseline of 175
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_the_precheck_refuses_a_verified_run_that_is_not_open`

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

### `r598-a.A2_no_holder_read_as_gone`

orphaned: read a record with no recorded holder as orphaned, so every intake landing left open for a deferred placement is abandoned

- File: `src/cratekit/core/session_holders.py`
- Source: `r598-a.json`, row `A2_no_holder_read_as_gone`
- Moved: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
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
- Moved: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 8 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_open_session_whose_process_is_gone_names_the_verb_that_ends_it`
  - `tests/test_session_cli.py::test_a_record_from_another_boot_not_proven_this_machines_is_kept[another-machine-with-this-host-name]`
  - `tests/test_session_cli.py::test_a_record_from_another_boot_not_proven_this_machines_is_kept[recorded-before-the-machine-identity]`
  - `tests/test_session_cli.py::test_a_record_whose_holder_is_alive_is_kept_open`
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
- Moved: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
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
  - `tests/test_session_cli.py::test_a_hard_killed_gated_write_blocks_cutover_until_release_abandons_it`
  - `tests/test_session_cli.py::test_a_power_loss_blocks_cutover_until_release_abandons_it`
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

### `r598-a.A7_sweep_ignores_the_shown_list`

abandon_orphaned_sessions: end every orphan rather than only those shown, so one answer ends records the question never listed

- File: `src/cratekit/core/session_holders.py`
- Source: `r598-a.json`, row `A7_sweep_ignores_the_shown_list`
- Moved: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
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
- Moved: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`, `tests/test_write_session.py`
- Collected: 185 against a baseline of 185
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_live_holders_claim_is_refused_and_the_lock_file_is_untouched`
  - `tests/test_session_cli.py::test_a_live_lock_holder_refuses_and_abandons_nothing`
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

### `r647-a.B12_cross_boot_never_judged`

holder_alive: every other boot judged alive again, the state before this unit, so a power loss stays a dead end

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B12_cross_boot_never_judged`
- Moved: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_power_loss_blocks_cutover_until_release_abandons_it`
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

### `r647-a.B14_machine_not_read_back`

Holder.from_json: ignore the recorded machine, so a record or lock read from disk never names one

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B14_machine_not_read_back`
- Moved: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 5 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_live_holders_claim_is_refused_and_the_lock_file_is_untouched`
  - `tests/test_session_cli.py::test_a_power_loss_blocks_cutover_until_release_abandons_it`
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
- Moved: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 5 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_live_holders_claim_is_refused_and_the_lock_file_is_untouched`
  - `tests/test_session_cli.py::test_a_power_loss_blocks_cutover_until_release_abandons_it`
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
- Moved: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
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
- Moved: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 3 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_record_from_another_boot_not_proven_this_machines_is_kept[another-machine-with-this-host-name]`
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
- Moved: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
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
- Moved: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
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
- Moved: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
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
- Moved: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
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
- Moved: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
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
- Moved: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
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

### `u138-rerun.S5_bound_exclusive`

A portion exactly five days old is under the bound

- File: `src/cratekit/core/session_ack.py`
- Source: `u138-rerun.json`, row `S5_bound_exclusive`
- Moved: the same text, now in src/cratekit/core/session_ack.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4220 against a baseline of 4220
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
- Moved: the same text, now in src/cratekit/core/session_ack.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4220 against a baseline of 4220
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
- Moved: the same text, now in src/cratekit/core/session_ack.py, was in src/cratekit/core/session.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4220 against a baseline of 4220
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
- Moved: the same text, now in src/cratekit/core/session_ack.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4220 against a baseline of 4220
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
- Moved: the same text, now in src/cratekit/core/session_ack.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4220 against a baseline of 4220
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
- Moved: the same text, now in src/cratekit/core/session_ack.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4220 against a baseline of 4220
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
- Moved: the same text, now in src/cratekit/core/session_ack.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4220 against a baseline of 4220
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
- Moved: the same text, now in src/cratekit/core/session_ack.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4220 against a baseline of 4220
- Kills: 13 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[session.ack]`
  - `tests/test_session_ack_by_session.py::test_a_person_at_a_terminal_mints_by_the_terminal_rule_and_the_record_says_so`
  - `tests/test_session_ack_by_session.py::test_a_person_without_a_terminal_is_still_refused_over_fresh_backups`
  - `tests/test_session_ack_by_session.py::test_a_valid_acknowledgment_a_person_minted_is_reported_over_old_backups`
  - `tests/test_session_cli.py::test_a_damaged_acknowledgment_record_can_still_be_replaced`
  - `tests/test_session_cli.py::test_a_hard_killed_gated_write_blocks_cutover_until_release_abandons_it`
  - `tests/test_session_cli.py::test_a_power_loss_blocks_cutover_until_release_abandons_it`
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

### `u138.S6_bound_six_days`

The bound is six days rather than five

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S6_bound_six_days`
- Moved: the same text, now in src/cratekit/core/session_ack.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4220 against a baseline of 4220
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
- Moved: the same text, now in src/cratekit/core/session_ack.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4220 against a baseline of 4220
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
- Moved: the same text, now in src/cratekit/core/session_ack.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4220 against a baseline of 4220
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

### `u49-author.L4_a_malformed_holder_raises_again`

Remove the coercion guard from read_lock_holder, so a lock record with a non numeric pid escapes as a traceback rather than a typed refusal

- File: `src/cratekit/core/session_holders.py`
- Source: `u49-author.json`, row `L4_a_malformed_holder_raises_again`
- Moved: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_session_cli.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 2589 against a baseline of 2589
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_lock_record_that_cannot_be_understood_refuses_by_name`

Old text:

```
    try:
        return Holder.from_json(data["holder"])
    except (TypeError, ValueError, AttributeError):
```

New text:

```
    if True:
        return Holder.from_json(data["holder"])
    if False:
```

### `r44-a.S10_default_slug`

Look the slug up with a default, so a verdict in neither table wears the mismatch slug

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S10_default_slug`
- Moved: moved by U300's split from src/cratekit/core/session.py to session_volumes.py, the same lookup read through the module as every name of it in a part is
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 475 against a baseline of 475
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

### `r44-a.S6_oserror_escapes`

Let an OSError from the walk or the identity read escape the gate instead of becoming a refusal

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S6_oserror_escapes`
- Moved: moved by U300's split from src/cratekit/core/session.py to session_volumes.py, the same handler with its comment cut to its rule and reason by the prose pass
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
        # Could not look is its own refusal, not an internal defect.
```

New text:

```
    except KeyboardInterrupt as exc:
        # Could not look is its own refusal, not an internal defect.
```

### `r598-a.A1_state_check_widened_to_non_terminal`

orphaned: accept any non terminal record rather than only open, so awaiting-import and committed-unverified records with a dead holder are abandoned and their own remedies hidden

- File: `src/cratekit/core/session_holders.py`
- Source: `r598-a.json`, row `A1_state_check_widened_to_non_terminal`
- Moved: moved by U300's split from src/cratekit/core/session.py to session_holders.py, the same check in orphaned, its names read through the module
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

### `r647-a.B10_live_identifier_not_asked`

_gone_since_an_earlier_boot: skip the live process check, so a live holder read through a moved clock has its claim cleared mid write

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B10_live_identifier_not_asked`
- Moved: moved by U300's split from src/cratekit/core/session.py to session_holders.py, the same return in _gone_since_an_earlier_boot, its probe read through the module
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
- Moved: moved by U300's split from src/cratekit/core/session.py to session_holders.py, the same return in _gone_since_an_earlier_boot, its probes read through the module
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

### `r647-a.B13_current_holder_names_no_machine`

current_holder: record the declared unknown instead of the machine identity, so no holder is ever provably this machine's

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B13_current_holder_names_no_machine`
- Moved: moved by U300's split from src/cratekit/core/session.py to session_holders.py, the same field in current_holder, its probe read through the module
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 3 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_power_loss_blocks_cutover_until_release_abandons_it`
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

### `r647-a.B9_platform_silence_read_as_gone`

_gone_since_an_earlier_boot: read a platform declining to say whether the process exists as gone

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B9_platform_silence_read_as_gone`
- Moved: moved by U300's split from src/cratekit/core/session.py to session_holders.py, the same return in _gone_since_an_earlier_boot, its probe read through the module
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

### `u138.S3_stale_not_refused`

The session mints over a portion five days old or of unknown age

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S3_stale_not_refused`
- Moved: moved by U300's split from src/cratekit/core/session.py to session_ack.py, the same refusal of a stale portion in the acknowledgment
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4220 against a baseline of 4220
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

### `u48-author.S1_remedy_fixed_at_repair`

The session names the repair token again, which is the defect this unit closed

- File: `src/cratekit/core/session_ack.py`
- Source: `u48-author.json`, row `S1_remedy_fixed_at_repair`
- Moved: moved by U300's split from src/cratekit/core/session.py to session_ack.py, the same remedy carried from the backup facts refusal
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_backup_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 1555 against a baseline of 1555
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
- Moved: moved by U300's split from src/cratekit/core/session.py to session_ack.py, the same remedy carried from the backup facts refusal
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_backup_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 1555 against a baseline of 1555
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

