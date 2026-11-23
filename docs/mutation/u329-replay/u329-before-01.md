# Mutation table: u329-before-01

Measured by `scripts/mutate.py` on 2026-11-23 17:23 UTC, branch `HEAD` at `36dadb92`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22622 collected. pytest invocations for this batch: 105.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-23 17:23 UTC for commit `36dadb92a615`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 30, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22622 against 22622. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r1917.V_r926_G1_first` | `src/cratekit/core/config.py` | maintainer | 4 file(s) | 310 | 12 | killed |
| `r301.F1_section_not_built` | `src/cratekit/core/config.py` | user | 2 file(s) | 319 | 5 | killed |
| `r345.A9_derive_on_load` | `src/cratekit/core/config.py` | user | 3 file(s) | 758 | 9 | killed |
| `r44-a.C4_identity_not_read` | `src/cratekit/core/config.py` | user | 2 file(s) | 583 | 2 | killed |
| `r790-c.C2_config_built` | `src/cratekit/core/config.py` | user | 2 file(s) | 291 | 1 | killed |
| `r926.G10_no_temporary_allowance` | `src/cratekit/core/config.py` | maintainer | 2 file(s) | 135 | 17 | killed |
| `r926.G11_mkdir_before_check` | `src/cratekit/core/config.py` | maintainer | 4 file(s) | 310 | 3 | killed |
| `r926.G12_message_drops_path` | `src/cratekit/core/config.py` | maintainer | 1 file(s) | 17 | 5 | killed |
| `r926.G2_checks_the_shipped_tool` | `src/cratekit/core/config.py` | user | 4 file(s) | 310 | 2 | killed |
| `r926.G3_document_check_dropped` | `src/cratekit/core/config.py` | maintainer | 4 file(s) | 310 | 4 | killed |
| `r926.G4_document_gets_temporary` | `src/cratekit/core/config.py` | maintainer | 4 file(s) | 310 | 4 | killed |
| `r926.G5_atomic_write_unchecked` | `src/cratekit/core/config.py` | maintainer | 4 file(s) | 310 | 2 | killed |
| `r926.G6_lock_unchecked` | `src/cratekit/core/config.py` | maintainer | 4 file(s) | 310 | 1 | killed |
| `r926.G7_no_root_allows_all` | `src/cratekit/core/config.py` | maintainer | 4 file(s) | 310 | 6 | killed |
| `r926.G8_target_unresolved` | `src/cratekit/core/config.py` | maintainer | 4 file(s) | 310 | 1 | killed |
| `r926.G9_temporary_unresolved` | `src/cratekit/core/config.py` | maintainer | 2 file(s) | 22622 | 0 (promoted) | zero |
| `u107-a.S01_record_not_json` | `src/cratekit/core/config.py` | user | 1 file(s) | 95 | 2 | killed |
| `u206.M25_lock_skipped` | `src/cratekit/core/config.py` | maintainer | 9 file(s) | 1130 | 1 | killed |
| `u254.C1_append_unsynced` | `src/cratekit/core/config.py` | user | 4 file(s) | 963 | 1 | killed |
| `u254.C2_append_one_write` | `src/cratekit/core/config.py` | user | 4 file(s) | 963 | 1 | killed |
| `u254.C3_append_test_root` | `src/cratekit/core/config.py` | maintainer | 4 file(s) | 963 | 2 | killed |
| `u254.C4_append_not_append` | `src/cratekit/core/config.py` | user | 4 file(s) | 963 | 54 | killed |
| `u272.C1_no_flush` | `src/cratekit/core/config.py` | user | 7 file(s) | 641 | 14 | killed |
| `u272.C2_full_flush_error_swallowed` | `src/cratekit/core/config.py` | user | 7 file(s) | 641 | 1 | killed |
| `u272.C3_full_flush_then_sync` | `src/cratekit/core/config.py` | maintainer | 7 file(s) | 641 | 1 | killed |
| `u272.C4_full_flush_never_asked` | `src/cratekit/core/config.py` | user | 7 file(s) | 641 | 5 | killed |
| `u272.C5_eio_counts_as_unsupported` | `src/cratekit/core/config.py` | user | 7 file(s) | 641 | 1 | killed |
| `u272.C6_no_plain_sync` | `src/cratekit/core/config.py` | user | 7 file(s) | 641 | 12 | killed |
| `u272.C7_error_names_no_path` | `src/cratekit/core/config.py` | user | 7 file(s) | 641 | 1 | killed |
| `u298.H10_flock_exclusive_hardens` | `src/cratekit/core/config.py` | maintainer | 2 file(s) | 352 | 3 | killed |
| `u298.H11_read_json_refuses_garbage` | `src/cratekit/core/config.py` | user | 2 file(s) | 352 | 4 | killed |
| `u298.H12_read_json_map_shape` | `src/cratekit/core/config.py` | user | 2 file(s) | 352 | 4 | killed |
| `u298.H7_held_translates_acquisition` | `src/cratekit/core/config.py` | user | 2 file(s) | 352 | 1 | killed |
| `u298.H8_lock_within_takes_lock` | `src/cratekit/core/config.py` | maintainer | 2 file(s) | 352 | 3 | killed |
| `u299.U13_from_dict_applies_overrides` | `src/cratekit/core/config.py` | user | 2 file(s) | 269 | 4 | killed |
| `r746-a.G1_asking_for_any_table_is_not_refused` | `src/cratekit/core/rb_changes.py` | user | 2 file(s) | 235 | 5 | killed |
| `r746-a.G2_admitted_row_judged_without_the_column_policy` | `src/cratekit/core/rb_changes.py` | user | 2 file(s) | 235 | 11 | killed |
| `r746-a.G3_content_row_admitted_without_asking` | `src/cratekit/core/rb_changes.py` | user | 3 file(s) | 279 | 5 | killed |
| `r758-a.W1_marker_not_judged` | `src/cratekit/core/rb_changes.py` | user | 2 file(s) | 300 | 74 | killed |
| `r758-a.W2_asked_table_not_held_to_the_set` | `src/cratekit/core/rb_changes.py` | user | 2 file(s) | 300 | 33 | killed |
| `r758-a.W3_ask_outside_the_set_not_refused` | `src/cratekit/core/rb_changes.py` | user | 2 file(s) | 300 | 33 | killed |
| `u163.W15_lookup_policy` | `src/cratekit/core/rb_changes.py` | user | 3 file(s) | 275 | 5 | killed |
| `u288.M1_delete_admitted_by_any_name` | `src/cratekit/core/rb_changes.py` | user | 2 file(s) | 287 | 2 | killed |
| `u288.M2_deletable_set_unbounded` | `src/cratekit/core/rb_changes.py` | user | 2 file(s) | 287 | 1 | killed |
| `u300.S11_registry_changes_local` | `src/cratekit/core/rb_changes.py` | maintainer | 1 file(s) | 22 | 4 | killed |
| `u953.M6_admission_loop_skips_the_refusal` | `src/cratekit/core/rb_changes.py` | user | 3 file(s) | 331 | 39 | killed |
| `u953.M7_admission_loop_keeps_the_unadmitted` | `src/cratekit/core/rb_changes.py` | user | 3 file(s) | 331 | 34 | killed |
| `r1665-b.C1_w5_composite` | `src/cratekit/core/rb_copies.py` | user | 7 file(s) | 316 | 2 | killed |
| `r1665.W1_check_opens_the_capture` | `src/cratekit/core/rb_copies.py` | user | 7 file(s) | 316 | 18 | killed |
| `r1665.W2_failed_copy_passes` | `src/cratekit/core/rb_copies.py` | user | 7 file(s) | 316 | 1 | killed |
| `r1665.W3_no_release_of_the_copy` | `src/cratekit/core/rb_copies.py` | maintainer | 1 file(s) | 14 | 1 | killed |
| `r1665.W4_quick_check_ignored` | `src/cratekit/core/rb_copies.py` | user | 7 file(s) | 316 | 1 | killed |
| `r1665.W6_refused_open_passes` | `src/cratekit/core/rb_copies.py` | user | 7 file(s) | 316 | 2 | killed |
| `r1677.R1_raise_after_copy` | `src/cratekit/core/rb_copies.py` | user | 4 file(s) | 123 | 1 | killed |
| `r1677.R3_copied_never_set` | `src/cratekit/core/rb_copies.py` | user | 4 file(s) | 123 | 1 | killed |
| `r1677.R5_file_set_drops_playlist` | `src/cratekit/core/rb_copies.py` | user | 5 file(s) | 278 | 2 | killed |
| `r1890.P7_permissive_marker_read_through_an_alias_of_the_accessor` | `src/cratekit/core/rb_copies.py` | user | 2 file(s) | 222 | 2 | killed |
| `r372-a.A10_copy_left_behind` | `src/cratekit/core/rb_copies.py` | maintainer | 3 file(s) | 494 | 15 | killed |
| `r372-a.A11_copy_under_a_running_application` | `src/cratekit/core/rb_copies.py` | maintainer | 3 file(s) | 494 | 1 | killed |
| `r372-a.A12_separator_kept` | `src/cratekit/core/rb_copies.py` | user | 3 file(s) | 494 | 7 | killed |
| `r663-a.M1_empty_not_refused_before_open` | `src/cratekit/core/rb_copies.py` | user | 1 file(s) | 51 | 4 | killed |
| `r663-a.M5_failed_listing_returns_empty_set` | `src/cratekit/core/rb_copies.py` | user | 1 file(s) | 51 | 2 | killed |
| `r663-a.M6_listing_opened_with_the_key_always` | `src/cratekit/core/rb_copies.py` | user | 1 file(s) | 51 | 2 | killed |
| `r663-b.M2_every_open_refusal_classified` | `src/cratekit/core/rb_copies.py` | user | 1 file(s) | 51 | 1 | killed |
| `r1890.P3_unreserved_slug_in_rb_nodes` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 222 | 1 | killed |
| `r1890.P4_unreadable_slug_in_rb_nodes` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 222 | 1 | killed |
| `r1890.P5_gate_name_in_rb_nodes` | `src/cratekit/core/rb_nodes.py` | maintainer | 1 file(s) | 1005 | 1 | killed |
| `r1890.P6_permissive_marker_read_through_the_accessor` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 222 | 2 | killed |
| `r235-b.M22_nested_namesake_is_a_root` | `src/cratekit/core/rb_nodes.py` | user | 1 file(s) | 40 | 2 | killed |
| `r235-b.M23_playlist_is_a_root` | `src/cratekit/core/rb_nodes.py` | user | 1 file(s) | 40 | 1 | killed |
| `r758-a.W7_removed_row_marked_again` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 300 | 1 | killed |
| `u111-a.A1_folder_refused` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 243 | 1 | killed |
| `u111-a.A3_parent_not_folder` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 243 | 1 | killed |

## Zero rows and what they owe

- `r926.G9_temporary_unresolved` (maintainer facing): maintainer facing, composite not required

## Row definitions

### `r1917.V_r926_G1_first`

The brief's verification, r926.G1_never_checks replayed (first of two in a row on one container): the guard returns at once, so every write the file aims outside lands, and the file must remove it

- File: `src/cratekit/core/config.py`
- Source: `r1917.json`, row `V_r926_G1_first`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_config_migration.py`
- Collected: 310 against a baseline of 310
- Kills: 12 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_link_inside_the_root_aimed_outside_it_is_refused`
  - `tests/test_config_test_root.py::test_a_lock_outside_every_temporary_folder_is_refused`
  - `tests/test_config_test_root.py::test_a_path_outside_the_root_is_refused_with_the_isolation_in_place`
  - `tests/test_config_test_root.py::test_a_path_resolution_that_leaves_the_root_is_refused`
  - `tests/test_config_test_root.py::test_a_state_write_outside_every_temporary_folder_is_refused[atomic-write]`
  - `tests/test_config_test_root.py::test_a_state_write_outside_every_temporary_folder_is_refused[durable-append]`
  - `tests/test_config_test_root.py::test_a_state_write_outside_the_root_is_refused_with_the_isolation_in_place[atomic-write]`
  - `tests/test_config_test_root.py::test_a_state_write_outside_the_root_is_refused_with_the_isolation_in_place[durable-append]`
  - `tests/test_config_test_root.py::test_the_configuration_is_not_allowed_the_system_temporary_folder`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_migration_write_back_is_refused`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_save_is_refused_and_names_the_path`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_an_update_is_refused_and_writes_nothing`

Old text:

```
    if "pytest" not in sys.modules:
        return
    root = _TEST_WRITE_ROOT
```

New text:

```
    if True:
        return
    root = _TEST_WRITE_ROOT
```

### `r301.F1_section_not_built`

The recognition section is never read from the file, so every install gets the default

- File: `src/cratekit/core/config.py`
- Source: `r301.json`, row `F1_section_not_built`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/intake/test_workers.py`
- Collected: 319 against a baseline of 319
- Kills: 5 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_the_configured_host_and_month_are_the_ones_every_paid_call_meets[identify]`
  - `tests/intake/test_workers.py::test_the_configured_host_and_month_are_the_ones_every_paid_call_meets[set]`
  - `tests/test_config.py::test_the_fingerprint_changes_when_any_value_changes[recognition-host-identify-eu-west-1.acrcloud.com]`
  - `tests/test_config.py::test_the_fingerprint_changes_when_any_value_changes[recognition-monthly_calls-250]`
  - `tests/test_config.py::test_the_recognition_defaults_bound_the_month_and_name_one_region`

Old text:

```
        recognition=_build(RecognitionConfig, data.get("recognition") or {}),
```

New text:

```
        recognition=RecognitionConfig(),
```

### `r345.A9_derive_on_load`

from_dict: do not derive backup.remote from the destinations

- File: `src/cratekit/core/config.py`
- Source: `r345.json`, row `A9_derive_on_load`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_backup_cli.py`
- Collected: 758 against a baseline of 758
- Kills: 9 (killed)
- Killed:
  - `tests/test_config.py::test_a_backup_destination_naming_an_rclone_remote_is_accepted`
  - `tests/test_config.py::test_an_unset_backup_destination_stays_allowed[full]`
  - `tests/test_config.py::test_an_unset_backup_destination_stays_allowed[slim]`
  - `tests/test_config.py::test_every_name_rclone_can_store_is_accepted_as_a_remote[Sicherung_\xfc]`
  - `tests/test_config.py::test_every_name_rclone_can_store_is_accepted_as_a_remote[b2]`
  - `tests/test_config.py::test_every_name_rclone_can_store_is_accepted_as_a_remote[gdrive-2.old]`
  - `tests/test_config.py::test_every_name_rclone_can_store_is_accepted_as_a_remote[me@gdrive]`
  - `tests/test_config.py::test_every_name_rclone_can_store_is_accepted_as_a_remote[my drive]`
  - `tests/test_config.py::test_every_name_rclone_can_store_is_accepted_as_a_remote[work+home]`

Old text:

```
            overrides={"remote": derived_backup_remote(data)},
```

New text:

```
            overrides=None,
```

### `r44-a.C4_identity_not_read`

Never read a rule's identity in, so every configured rule arrives unrecorded

- File: `src/cratekit/core/config.py`
- Source: `r44-a.json`, row `C4_identity_not_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_deletion.py`
- Collected: 583 against a baseline of 583
- Kills: 2 (killed)
- Killed:
  - `tests/test_config.py::test_a_prefix_rule_carries_the_identity_of_the_volume_it_points_at`
  - `tests/test_deletion.py::test_the_rules_the_pass_builds_from_configuration_carry_each_recorded_identity`

Old text:

```
                    volume_id=entry.get(PREFIX_VOLUME_IDENTITY_KEY),
```

New text:

```
                    volume_id=None,
```

### `r790-c.C2_config_built`

from_dict: ignore the labels section and always take the default

- File: `src/cratekit/core/config.py`
- Source: `r790-c.json`, row `C2_config_built`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`, `tests/test_config.py`
- Collected: 291 against a baseline of 291
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_the_configured_offer_is_the_default_for_every_label`

Old text:

```
        labels=_build(LabelsConfig, data.get("labels") or {}),
```

New text:

```
        labels=LabelsConfig(),
```

### `r926.G10_no_temporary_allowance`

The primitives lose the system temporary allowance, the strict rule the review round measured at 101 refusals

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G10_no_temporary_allowance`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_provider_gate.py`
- Collected: 135 against a baseline of 135
- Kills: 17 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_scratch_write_in_the_system_temporary_folder_lands_without_a_root`
  - `tests/test_provider_gate.py::test_a_ceiling_stop_a_verb_swallowed_is_still_said`
  - `tests/test_provider_gate.py::test_a_rate_limited_login_comes_out_of_client_session_as_the_park`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[excludes-another-processs-calls]`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[names-rate-limit-answers]`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[reports-its-calls]`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[survives-a-refusal]`
  - `tests/test_provider_gate.py::test_a_verb_at_its_line_is_blocked_and_the_call_past_it_is_not_sent[its-ceiling-names-the-exact-command-that-continues]`
  - `tests/test_provider_gate.py::test_a_verb_at_its_line_is_blocked_and_the_call_past_it_is_not_sent[the-hours-line-U278]`
  - `tests/test_provider_gate.py::test_calls_on_the_command_line_lets_one_run_pass_and_the_next_is_back_at_the_ceiling`
  - `tests/test_provider_gate.py::test_client_session_attaches_the_gate_before_the_login_goes_out`
  - `tests/test_provider_gate.py::test_client_session_with_no_gate_still_paces_at_the_defaults`
  - `tests/test_provider_gate.py::test_each_opener_paces_with_the_frozen_configuration[account]`
  - `tests/test_provider_gate.py::test_each_opener_paces_with_the_frozen_configuration[catalogue]`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_calls_already_given[joined]`
  - ... and 2 more, see the JSON sidecar

Old text:

```
    if system_temporary:
        allowed.append(
```

New text:

```
    if False:
        allowed.append(
```

### `r926.G11_mkdir_before_check`

save creates the configuration directory before the lock is built, so a refused write leaves a directory behind

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G11_mkdir_before_check`
- Moved: Same lines in save; U298 renamed _mkdir_private to the public mkdir_private
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_config_migration.py`
- Collected: 310 against a baseline of 310
- Kills: 3 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_path_outside_the_root_is_refused_with_the_isolation_in_place`
  - `tests/test_config_test_root.py::test_a_path_resolution_that_leaves_the_root_is_refused`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_save_is_refused_and_names_the_path`

Old text:

```
    with _write_lock(target):
        mkdir_private(target.parent)
        atomic_write_bytes(config.to_toml_bytes(), target)
```

New text:

```
    mkdir_private(target.parent)
    with _write_lock(target):
        atomic_write_bytes(config.to_toml_bytes(), target)
```

### `r926.G12_message_drops_path`

The no root refusal stops naming the path it refused

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G12_message_drops_path`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`
- Collected: 17 against a baseline of 17
- Kills: 5 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_state_write_outside_every_temporary_folder_is_refused[atomic-write]`
  - `tests/test_config_test_root.py::test_a_state_write_outside_every_temporary_folder_is_refused[durable-append]`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_migration_write_back_is_refused`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_save_is_refused_and_names_the_path`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_an_update_is_refused_and_writes_nothing`

Old text:

```
            f"refused to write {path}: this process is "
            f"running under pytest and no test root is registered, so the "
```

New text:

```
            f"refused to write the file: this process is "
            f"running under pytest and no test root is registered, so the "
```

### `r926.G2_checks_the_shipped_tool`

The guard runs in a process without pytest too, so the shipped tool refuses every configuration save

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G2_checks_the_shipped_tool`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_config_migration.py`
- Collected: 310 against a baseline of 310
- Kills: 2 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_process_without_pytest_loaded_is_never_checked`
  - `tests/test_config_update.py::test_three_real_processes_writing_at_once_all_keep_their_answers`

Old text:

```
    if "pytest" not in sys.modules:
        return
    root = _TEST_WRITE_ROOT
```

New text:

```
    if False:
        return
    root = _TEST_WRITE_ROOT
```

### `r926.G3_document_check_dropped`

_write_lock no longer checks, so the configuration document is held only by the primitives' temporary allowance

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G3_document_check_dropped`
- Moved: Same lines in _write_lock; U298 renamed _exclusive_lock to the public exclusive_lock
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_config_migration.py`
- Collected: 310 against a baseline of 310
- Kills: 4 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_the_configuration_is_not_allowed_the_system_temporary_folder`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_migration_write_back_is_refused`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_save_is_refused_and_names_the_path`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_an_update_is_refused_and_writes_nothing`

Old text:

```
    _refuse_write_outside_test_root(path)
    return exclusive_lock(path.with_name(path.name + ".migrate.lock"))
```

New text:

```
    return exclusive_lock(path.with_name(path.name + ".migrate.lock"))
```

### `r926.G4_document_gets_temporary`

The configuration document is given the system temporary allowance the primitives have

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G4_document_gets_temporary`
- Moved: Same lines in _write_lock; U298 renamed _exclusive_lock to the public exclusive_lock
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_config_migration.py`
- Collected: 310 against a baseline of 310
- Kills: 4 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_the_configuration_is_not_allowed_the_system_temporary_folder`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_migration_write_back_is_refused`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_save_is_refused_and_names_the_path`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_an_update_is_refused_and_writes_nothing`

Old text:

```
    _refuse_write_outside_test_root(path)
    return exclusive_lock(path.with_name(path.name + ".migrate.lock"))
```

New text:

```
    _refuse_write_outside_test_root(path, system_temporary=True)
    return exclusive_lock(path.with_name(path.name + ".migrate.lock"))
```

### `r926.G5_atomic_write_unchecked`

atomic_write_bytes no longer checks, so a ledger or token write from an unisolated test lands anywhere

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G5_atomic_write_unchecked`
- Moved: Same lines in atomic_write_bytes; U298 renamed _mkdir_private to the public mkdir_private
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_config_migration.py`
- Collected: 310 against a baseline of 310
- Kills: 2 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_state_write_outside_every_temporary_folder_is_refused[atomic-write]`
  - `tests/test_config_test_root.py::test_a_state_write_outside_the_root_is_refused_with_the_isolation_in_place[atomic-write]`

Old text:

```
    _refuse_write_outside_test_root(path, system_temporary=True)
    mkdir_private(path.parent)
    fd, tmp = tempfile.mkstemp(
```

New text:

```
    mkdir_private(path.parent)
    fd, tmp = tempfile.mkstemp(
```

### `r926.G6_lock_unchecked`

_exclusive_lock no longer checks, so a session lock from an unisolated test is created anywhere

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G6_lock_unchecked`
- Moved: Same lines in the lock's __enter__; U298 renamed the class to exclusive_lock and _mkdir_private to mkdir_private
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_config_migration.py`
- Collected: 310 against a baseline of 310
- Kills: 1 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_lock_outside_every_temporary_folder_is_refused`

Old text:

```
        _refuse_write_outside_test_root(self.path, system_temporary=True)
        mkdir_private(self.path.parent)
```

New text:

```
        mkdir_private(self.path.parent)
```

### `r926.G7_no_root_allows_all`

With no root registered the allowed set is the filesystem root, so the R-926 probe writes the live config again

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G7_no_root_allows_all`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_config_migration.py`
- Collected: 310 against a baseline of 310
- Kills: 6 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_lock_outside_every_temporary_folder_is_refused`
  - `tests/test_config_test_root.py::test_a_state_write_outside_every_temporary_folder_is_refused[atomic-write]`
  - `tests/test_config_test_root.py::test_a_state_write_outside_every_temporary_folder_is_refused[durable-append]`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_migration_write_back_is_refused`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_save_is_refused_and_names_the_path`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_an_update_is_refused_and_writes_nothing`

Old text:

```
    allowed = [] if root is None else [root.resolve()]
```

New text:

```
    allowed = [Path(os.sep)] if root is None else [root.resolve()]
```

### `r926.G8_target_unresolved`

The target is compared as spelled, so a link inside the root aimed outside it passes

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G8_target_unresolved`
- Moved: Same lines in _refuse_write_outside_test_root; U298 renamed _is_inside to the public is_inside
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_config_migration.py`
- Collected: 310 against a baseline of 310
- Kills: 1 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_link_inside_the_root_aimed_outside_it_is_refused`

Old text:

```
    target = path.resolve()
    if any(is_inside(target, each) for each in allowed):
```

New text:

```
    target = path
    if any(is_inside(target, each) for each in allowed):
```

### `r926.G9_temporary_unresolved`

The system temporary directory is compared as spelled, /var against /private/var on macOS, so every scratch write is refused

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G9_temporary_unresolved`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_provider_gate.py`
- Collected: 22622 against a baseline of 22622
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        allowed.append(Path(tempfile.gettempdir()).resolve())
```

New text:

```
        allowed.append(Path(tempfile.gettempdir()))
```

### `u107-a.S01_record_not_json`

sync_cli.load_record: read a record that is not JSON as an empty one, so every question is asked again and every answer is lost

- File: `src/cratekit/core/config.py`
- Source: `u107-a.json`, row `S01_record_not_json`
- Moved: U298 replaced label/sync_cli.load_record's own JSON read with config.read_json_map over config.read_json; the not JSON refusal is read_json's, and answering absent there makes load_record return its empty record, the same outcome the original return of _empty gave
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 95 against a baseline of 95
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_record_that_cannot_be_read_refuses_rather_than_asking_everything_again`
  - `tests/test_label_sync.py::test_the_labels_sweep_refuses_an_unreadable_record_before_any_login`

Old text:

```
    except ValueError as exc:
        raise unusable("it is not JSON") from exc


def read_json_map(
```

New text:

```
    except ValueError as exc:
        return False, None


def read_json_map(
```

### `u206.M25_lock_skipped`

Cache._locked: yield as held without taking the lock

- File: `src/cratekit/core/config.py`
- Source: `u206.json`, row `M25_lock_skipped`
- Moved: U298 replaced isrc_cache.Cache._locked's body with config.lock_within, which _locked now returns; the same non blocking flock in the same poll loop, so dropping it yields held without the lock
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1130 against a baseline of 1130
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_two_writer_processes_leave_one_readable_file_holding_both`

Old text:

```
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                had = True
```

New text:

```
            try:
                had = True
```

### `u254.C1_append_unsynced`

append_durable_bytes: return without syncing the appended record

- File: `src/cratekit/core/config.py`
- Source: `u254.json`, row `C1_append_unsynced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_adoption.py`
- Collected: 963 against a baseline of 963
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_every_append_is_synced_before_the_mark_returns`

Old text:

```
            view = view[os.write(fd, view) :]
        os.fsync(fd)
```

New text:

```
            view = view[os.write(fd, view) :]
```

### `u254.C2_append_one_write`

append_durable_bytes: make one write call and drop what it did not take

- File: `src/cratekit/core/config.py`
- Source: `u254.json`, row `C2_append_one_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_adoption.py`
- Collected: 963 against a baseline of 963
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_the_system_writes_in_pieces_still_lands_whole`

Old text:

```
        while view:
            view = view[os.write(fd, view) :]
```

New text:

```
        if view:
            view = view[os.write(fd, view) :]
```

### `u254.C3_append_test_root`

append_durable_bytes: drop the test root refusal

- File: `src/cratekit/core/config.py`
- Source: `u254.json`, row `C3_append_test_root`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_adoption.py`
- Collected: 963 against a baseline of 963
- Kills: 2 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_state_write_outside_every_temporary_folder_is_refused[durable-append]`
  - `tests/test_config_test_root.py::test_a_state_write_outside_the_root_is_refused_with_the_isolation_in_place[durable-append]`

Old text:

```
    _refuse_write_outside_test_root(path, system_temporary=True)
    fd = os.open(path, os.O_WRONLY | os.O_APPEND)
```

New text:

```
    fd = os.open(path, os.O_WRONLY | os.O_APPEND)
```

### `u254.C4_append_not_append`

append_durable_bytes: open for writing at the start of the file rather than its end

- File: `src/cratekit/core/config.py`
- Source: `u254.json`, row `C4_append_not_append`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_adoption.py`
- Collected: 963 against a baseline of 963
- Kills: 54 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_file_put_in_place_with_the_same_size_and_time_is_read_again`
  - `tests/test_adopt_apply_journal_u254.py::test_a_file_rewritten_in_place_at_the_same_size_is_read_again`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[1]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[2]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[3]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[4]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_mark_does_not_parse_the_ledger_it_appends_to`
  - `tests/test_adopt_apply_journal_u254.py::test_a_mark_on_a_journal_this_process_never_wrote_appends`
  - `tests/test_adopt_apply_journal_u254.py::test_a_mark_on_a_ledger_written_before_u254_keeps_every_record`
  - `tests/test_adopt_apply_journal_u254.py::test_a_re_mark_replaces_the_earlier_record_as_the_document_did`
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_another_process_appended_is_kept`
  - `tests/test_adopt_apply_journal_u254.py::test_a_revert_after_a_partial_apply_restores_what_it_wrote`
  - `tests/test_adopt_apply_journal_u254.py::test_a_torn_tail_left_inside_one_clock_tick_is_still_cut`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_the_system_writes_in_pieces_still_lands_whole`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-newline-1]`
  - ... and 39 more, see the JSON sidecar

Old text:

```
    fd = os.open(path, os.O_WRONLY | os.O_APPEND)
```

New text:

```
    fd = os.open(path, os.O_WRONLY)
```

### `u272.C1_no_flush`

flush_to_disk: open and close the path and flush nothing

- File: `src/cratekit/core/config.py`
- Source: `u272.json`, row `C1_no_flush`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 641 against a baseline of 641
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
- Collected: 641 against a baseline of 641
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
- Collected: 641 against a baseline of 641
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
- Collected: 641 against a baseline of 641
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
- Collected: 641 against a baseline of 641
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
- Collected: 641 against a baseline of 641
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
- Collected: 641 against a baseline of 641
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

### `u298.H10_flock_exclusive_hardens`

flock_exclusive: a lock file left at another mode is never hardened

- File: `src/cratekit/core/config.py`
- Source: `u298.json`, row `H10_flock_exclusive_hardens`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`, `tests/test_config.py`
- Collected: 352 against a baseline of 352
- Kills: 3 (killed)
- Killed:
  - `tests/test_shared_homes.py::test_a_waiting_lock_that_fails_closes_its_handle_and_leaves_as_itself[failure0]`
  - `tests/test_shared_homes.py::test_a_waiting_lock_that_fails_closes_its_handle_and_leaves_as_itself[failure1]`
  - `tests/test_shared_homes.py::test_the_waiting_lock_hardens_its_file_before_it_locks_and_returns_the_holder`

Old text:

```
        handle = os.fdopen(descriptor, "r+b")
        harden(target)
```

New text:

```
        handle = os.fdopen(descriptor, "r+b")
```

### `u298.H11_read_json_refuses_garbage`

read_json: a document that is not JSON reads as an empty record

- File: `src/cratekit/core/config.py`
- Source: `u298.json`, row `H11_read_json_refuses_garbage`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`, `tests/test_config.py`
- Collected: 352 against a baseline of 352
- Kills: 4 (killed)
- Killed:
  - `tests/test_shared_homes.py::test_a_document_that_does_not_parse_is_refused_and_never_read_as_empty[\xff\xfe\x00]`
  - `tests/test_shared_homes.py::test_a_document_that_does_not_parse_is_refused_and_never_read_as_empty[]`
  - `tests/test_shared_homes.py::test_a_document_that_does_not_parse_is_refused_and_never_read_as_empty[{not json]`
  - `tests/test_shared_homes.py::test_bytes_that_are_not_text_leave_the_platform_read_as_the_decoding_failure_they_are`

Old text:

```
        return True, json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise unusable("it could not be opened") from exc
    except ValueError as exc:
        raise unusable("it is not JSON") from exc
```

New text:

```
        return True, json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise unusable("it could not be opened") from exc
    except ValueError:
        return True, {}
```

### `u298.H12_read_json_map_shape`

read_json_map: a list at the top level is handed on as a record

- File: `src/cratekit/core/config.py`
- Source: `u298.json`, row `H12_read_json_map_shape`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`, `tests/test_config.py`
- Collected: 352 against a baseline of 352
- Kills: 4 (killed)
- Killed:
  - `tests/test_shared_homes.py::test_a_document_that_is_no_map_is_refused_by_what_it_is["words"-str]`
  - `tests/test_shared_homes.py::test_a_document_that_is_no_map_is_refused_by_what_it_is[3-int]`
  - `tests/test_shared_homes.py::test_a_document_that_is_no_map_is_refused_by_what_it_is[[]-list]`
  - `tests/test_shared_homes.py::test_a_document_that_is_no_map_is_refused_by_what_it_is[null-NoneType]`

Old text:

```
    if not isinstance(raw, Mapping):
        raise unusable(f"the document is a {type(raw).__name__}, not a map")
```

New text:

```
(empty)
```

### `u298.H7_held_translates_acquisition`

held: a lock another holder has leaves as the lock error, not the store's own refusal

- File: `src/cratekit/core/config.py`
- Source: `u298.json`, row `H7_held_translates_acquisition`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`, `tests/test_config.py`
- Collected: 352 against a baseline of 352
- Kills: 1 (killed)
- Killed:
  - `tests/test_shared_homes.py::test_a_lock_that_cannot_be_taken_is_refused_in_the_stores_own_words`

Old text:

```
    except ConfigLockUnavailable as exc:
        raise refused(exc) from exc
```

New text:

```
    except ConfigLockUnavailable:
        raise
```

### `u298.H8_lock_within_takes_lock`

lock_within: reads the lock as had without taking it, so two writers interleave

- File: `src/cratekit/core/config.py`
- Source: `u298.json`, row `H8_lock_within_takes_lock`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`, `tests/test_config.py`
- Collected: 352 against a baseline of 352
- Kills: 3 (killed)
- Killed:
  - `tests/test_shared_homes.py::test_a_lock_another_holds_is_asked_for_until_the_wait_is_spent_and_then_given_up`
  - `tests/test_shared_homes.py::test_a_lock_freed_during_the_wait_is_had_at_the_next_look`
  - `tests/test_shared_homes.py::test_a_lock_had_in_time_is_yielded_as_had_and_its_file_is_private_and_stays`

Old text:

```
        had = fcntl is None
```

New text:

```
        had = True
```

### `u299.U13_from_dict_applies_overrides`

config.from_dict: the overrides are left to validation, so the built config keeps the file's root

- File: `src/cratekit/core/config.py`
- Source: `u299.json`, row `U13_from_dict_applies_overrides`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_config_test_root.py`
- Collected: 269 against a baseline of 269
- Kills: 4 (killed)
- Killed:
  - `tests/test_config.py::test_a_relocated_root_carries_the_database_that_sat_under_it`
  - `tests/test_config.py::test_a_save_under_a_relocation_writes_a_file_that_loads_again`
  - `tests/test_config.py::test_the_backup_destination_check_reads_the_effective_mapping`
  - `tests/test_config.py::test_the_prefix_map_survives_a_remount_because_it_interpolates`

Old text:

```
    data = _apply_env_overrides(data)
    problems = validate(data)
```

New text:

```
    problems = validate(data)
```

### `r746-a.G1_asking_for_any_table_is_not_refused`

guard_violations: a creation asked for in a table outside ADMITTABLE_ROW_TABLES is no longer itself a violation

- File: `src/cratekit/core/rb_changes.py`
- Source: `r746-a.json`, row `G1_asking_for_any_table_is_not_refused`
- Moved: U953 folded the three admission loops of guard_violations into one loop over data, so emptying the refusal loop for the creation entry alone is the same dropped refusal of a creation outside ADMITTABLE_ROW_TABLES
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_write_guard_completeness.py`
- Collected: 235 against a baseline of 235
- Kills: 5 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_creation_naming_the_key_table_is_refused`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_creation_in_any_other_table_is_itself_refused[djmdBeatGrid]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_creation_in_any_other_table_is_itself_refused[djmdColor]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_creation_in_any_other_table_is_itself_refused[djmdCue]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_creation_in_any_other_table_is_itself_refused[djmdLabel]`

Old text:

```
        for table in sorted(asked - allowed):

```

New text:

```
        for table in (sorted(asked - allowed) if verb != "create" else ()):

```

### `r746-a.G2_admitted_row_judged_without_the_column_policy`

guard_violations: an admitted content row may declare any column, the ten included

- File: `src/cratekit/core/rb_changes.py`
- Source: `r746-a.json`, row `G2_admitted_row_judged_without_the_column_policy`
- Moved: U953 made the content row branch choose the columns a shared declared check judges, so choosing no columns there is the same empty declared set for an admitted content row
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_write_guard_completeness.py`
- Collected: 235 against a baseline of 235
- Kills: 11 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_an_admitted_content_row_declaring_an_analysis_column_is_refused[Analysed]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_content_row_declaring_an_analysis_column_is_refused[AnalysisDataPath]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_content_row_declaring_an_analysis_column_is_refused[AnalysisUpdated]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_content_row_declaring_an_analysis_column_is_refused[BPM]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_content_row_declaring_an_analysis_column_is_refused[BitDepth]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_content_row_declaring_an_analysis_column_is_refused[BitRate]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_content_row_declaring_an_analysis_column_is_refused[CueUpdated]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_content_row_declaring_an_analysis_column_is_refused[ImagePath]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_content_row_declaring_an_analysis_column_is_refused[KeyID]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_content_row_declaring_an_analysis_column_is_refused[SampleRate]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_creation_still_refuses_a_second_content_row_nobody_asked_about`

Old text:

```
            empties, made = CONTENT_ROW_EMPTY_COLUMNS, f"a {CONTENT_TABLE} row"
```

New text:

```
            empties, made = frozenset(), f"a {CONTENT_TABLE} row"
```

### `r746-a.G3_content_row_admitted_without_asking`

guard_violations: every commit admits a content row, whether or not it named the table

- File: `src/cratekit/core/rb_changes.py`
- Source: `r746-a.json`, row `G3_content_row_admitted_without_asking`
- Moved: the same text, now in src/cratekit/core/rb_changes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_write_guard_completeness.py`, `tests/test_intake_land_native.py`
- Collected: 279 against a baseline of 279
- Kills: 5 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_commit_that_asks_may_create_a_content_row_carrying_what_the_file_says`
  - `tests/test_rb_writer_guard.py::test_an_admitted_delete_admits_no_soft_delete_no_creation_and_no_modification`
  - `tests/test_rb_writer_guard.py::test_creating_a_track_row_is_forbidden`
  - `tests/test_rb_writer_guard.py::test_mixed_session_reports_every_violation`
  - `tests/test_write_guard_completeness.py::test_a_content_creation_flushed_away_is_still_refused`

Old text:

```
        if table == CONTENT_TABLE and table in creatable:
```

New text:

```
        if table == CONTENT_TABLE:
```

### `r758-a.W1_marker_not_judged`

the guard stops judging a changed soft delete marker, so any writer removes a row in any table with the guard saying nothing

- File: `src/cratekit/core/rb_changes.py`
- Source: `r758-a.json`, row `W1_marker_not_judged`
- Moved: U953 replaced the local rb_writer name with a _writer() call on the marker line, so the same impossible extra condition silences the same marker judgment
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_adopt_move.py`
- Collected: 300 against a baseline of 300
- Kills: 74 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_an_admitted_commit_refuses_a_removed_collection_row_or_a_hard_delete`
  - `tests/test_adopt_move.py::test_an_ordinary_guarded_commit_refuses_a_removal_and_rolls_it_back`
  - `tests/test_adopt_move.py::test_the_additive_membership_writer_refuses_a_removal_in_its_session`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[cloudAgentRegistry]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[contentActiveCensor]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[contentCue]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[contentFile]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[djmdActiveCensor]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[djmdAlbum]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[djmdArtist]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[djmdCategory]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[djmdColor]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[djmdContent]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[djmdCue]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[djmdDevice]`
  - ... and 59 more, see the JSON sidecar

Old text:

```
        if _writer().SOFT_DELETE_COLUMN in columns and table not in admitted:
```

New text:

```
        if _writer().SOFT_DELETE_COLUMN in columns and table not in admitted and table == "":
```

### `r758-a.W2_asked_table_not_held_to_the_set`

a commit that asks for a removal in any table is admitted it, the refusal of the ask left standing

- File: `src/cratekit/core/rb_changes.py`
- Source: `r758-a.json`, row `W2_asked_table_not_held_to_the_set`
- Moved: U953 folded the three intersections of guard_violations into one append inside a loop over data, so skipping the intersection for the removal entry alone is the same deleted admitted &= REMOVABLE_TABLES
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_adopt_move.py`
- Collected: 300 against a baseline of 300
- Kills: 33 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[cloudAgentRegistry]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[contentActiveCensor]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[contentCue]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[contentFile]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdActiveCensor]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdAlbum]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdArtist]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdCategory]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdColor]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdContent]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdCue]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdDevice]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdGenre]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdHistory]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdHotCueBanklist]`
  - ... and 18 more, see the JSON sidecar

Old text:

```
        admissions.append(asked & allowed)
```

New text:

```
        admissions.append(asked if verb == "remove" else asked & allowed)
```

### `r758-a.W3_ask_outside_the_set_not_refused`

asking for a removal outside the removable set is no longer itself a violation, the intersection left standing

- File: `src/cratekit/core/rb_changes.py`
- Source: `r758-a.json`, row `W3_ask_outside_the_set_not_refused`
- Moved: U953 folded the three admission loops of guard_violations into one loop over data, so emptying the refusal loop for the removal entry alone is the same dropped refusal of a removal outside REMOVABLE_TABLES
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_adopt_move.py`
- Collected: 300 against a baseline of 300
- Kills: 33 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[cloudAgentRegistry]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[contentActiveCensor]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[contentCue]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[contentFile]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdActiveCensor]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdAlbum]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdArtist]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdCategory]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdColor]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdContent]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdCue]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdDevice]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdGenre]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdHistory]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdHotCueBanklist]`
  - ... and 18 more, see the JSON sidecar

Old text:

```
        for table in sorted(asked - allowed):

```

New text:

```
        for table in (sorted(asked - allowed) if verb != "remove" else ()):

```

### `u163.W15_lookup_policy`

guard_violations: wave an admitted lookup row through without the creation policy

- File: `src/cratekit/core/rb_changes.py`
- Source: `u163.json`, row `W15_lookup_policy`
- Moved: U953 merged the admitted lookup branch into the permitted table branch that picks the columns a shared check judges, so picking no columns for an admitted lookup row is the same wave through
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 275 against a baseline of 275
- Kills: 5 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_an_admitted_lookup_row_declaring_an_analysis_column_is_refused[Analysed]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_lookup_row_declaring_an_analysis_column_is_refused[AnalysisDataPath]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_lookup_row_declaring_an_analysis_column_is_refused[AnalysisUpdated]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_lookup_row_declaring_an_analysis_column_is_refused[BPM]`
  - `tests/test_rb_writer_guard.py::test_an_admitted_lookup_row_declaring_an_analysis_column_is_refused[CueUpdated]`

Old text:

```
            empties, made = GRIDLESS_ON_CREATE_COLUMNS, f"a row in {table!r}"
```

New text:

```
            empties, made = (frozenset() if table in LOOKUP_TABLES and table in creatable else GRIDLESS_ON_CREATE_COLUMNS), f"a row in {table!r}"
```

### `u288.M1_delete_admitted_by_any_name`

guard_violations: admit a delete in any table once any table is named, not only the named one

- File: `src/cratekit/core/rb_changes.py`
- Source: `u288.json`, row `M1_delete_admitted_by_any_name`
- Moved: the same text, now in src/cratekit/core/rb_changes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 287 against a baseline of 287
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_delete_is_admitted_only_in_a_table_the_commit_names`
  - `tests/test_sync_removed.py::test_another_writer_deleting_a_content_row_through_the_binding_is_refused_at_its_commit`

Old text:

```
        if table in deletable:
            continue
```

New text:

```
        if deletable:
            continue
```

### `u288.M2_deletable_set_unbounded`

guard_violations: stop holding the named tables to DELETABLE_TABLES, so a commit can ask to delete anywhere

- File: `src/cratekit/core/rb_changes.py`
- Source: `u288.json`, row `M2_deletable_set_unbounded`
- Moved: U953 folded the three intersections of guard_violations into one append inside a loop over data, so skipping the intersection for the delete entry alone is the same unbounded deletable set
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 287 against a baseline of 287
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_delete_outside_the_removal_set_is_refused_even_when_asked_for`

Old text:

```
        admissions.append(asked & allowed)
```

New text:

```
        admissions.append(asked if verb == "delete" else asked & allowed)
```

### `u300.S11_registry_changes_local`

pending_objects reads the buffer through the part's own _registry_changes

- File: `src/cratekit/core/rb_changes.py`
- Source: `u300.json`, row `S11_registry_changes_local`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_guard_completeness.py`
- Collected: 22 against a baseline of 22
- Kills: 4 (killed)
- Killed:
  - `tests/test_write_guard_completeness.py::test_a_content_creation_flushed_away_is_still_refused`
  - `tests/test_write_guard_completeness.py::test_a_creation_flushed_out_of_the_session_is_still_judged`
  - `tests/test_write_guard_completeness.py::test_one_instance_created_then_updated_is_reported_once_as_a_creation`
  - `tests/test_write_guard_completeness.py::test_the_two_sources_are_unioned_rather_than_either_being_trusted_alone`

Old text:

```
    r_created, r_modified, r_removed = _writer()._registry_changes(db)
```

New text:

```
    r_created, r_modified, r_removed = _registry_changes(db)
```

### `u953.M6_admission_loop_skips_the_refusal`

guard_violations' admission loop admits every asked table, so a removal, creation or delete outside its set is no violation

- File: `src/cratekit/core/rb_changes.py`
- Source: `u953.json`, row `M6_admission_loop_skips_the_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_rb_writer_db.py`, `tests/test_sync_removed.py`
- Collected: 331 against a baseline of 331
- Kills: 39 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_creation_naming_the_key_table_is_refused`
  - `tests/test_rb_writer_guard.py::test_a_delete_outside_the_removal_set_is_refused_even_when_asked_for`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_creation_in_any_other_table_is_itself_refused[djmdBeatGrid]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_creation_in_any_other_table_is_itself_refused[djmdColor]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_creation_in_any_other_table_is_itself_refused[djmdCue]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_creation_in_any_other_table_is_itself_refused[djmdLabel]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[cloudAgentRegistry]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[contentActiveCensor]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[contentCue]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[contentFile]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdActiveCensor]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdAlbum]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdArtist]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdCategory]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdColor]`
  - ... and 24 more, see the JSON sidecar

Old text:

```
        for table in sorted(asked - allowed):
```

New text:

```
        for table in sorted(asked - allowed - asked):
```

### `u953.M7_admission_loop_keeps_the_unadmitted`

guard_violations hands on what was asked rather than what was asked and allowed, so a table outside the set is admitted downstream

- File: `src/cratekit/core/rb_changes.py`
- Source: `u953.json`, row `M7_admission_loop_keeps_the_unadmitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_rb_writer_db.py`, `tests/test_sync_removed.py`
- Collected: 331 against a baseline of 331
- Kills: 34 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_delete_outside_the_removal_set_is_refused_even_when_asked_for`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[cloudAgentRegistry]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[contentActiveCensor]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[contentCue]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[contentFile]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdActiveCensor]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdAlbum]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdArtist]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdCategory]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdColor]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdContent]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdCue]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdDevice]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdGenre]`
  - `tests/test_rb_writer_guard.py::test_asking_for_a_removal_in_any_other_table_is_itself_refused[djmdHistory]`
  - ... and 19 more, see the JSON sidecar

Old text:

```
        admissions.append(asked & allowed)
```

New text:

```
        admissions.append(asked)
```

### `r1665-b.C1_w5_composite`

The composite for the zero W5_unreadable_check_passes in r1665.md, what it holds with the open refusal: an open the gate refuses and a consistency check that raises both answer True

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1665-b.json`, row `C1_w5_composite`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_copies.py, the same guard in integrity_ok, the module's names now read through the module
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_a_damaged_snapshot_fails_its_integrity_check`
  - `tests/test_snapshot_wal_r1665.py::test_a_damaged_copy_still_fails_the_check`

Old text:

```
            except _writer().RekordboxUnavailable:
                return False
            try:
                result = db.session.execute(text("PRAGMA quick_check")).scalar()
                return str(result).lower() == "ok"
            except Exception:  # noqa: BLE001 - an unreadable snapshot is a failed snapshot
                return False
```

New text:

```
            except _writer().RekordboxUnavailable:
                return True
            try:
                result = db.session.execute(text("PRAGMA quick_check")).scalar()
                return str(result).lower() == "ok"
            except Exception:  # noqa: BLE001 - an unreadable snapshot is a failed snapshot
                return True
```

### `r1665.W1_check_opens_the_capture`

integrity_ok: open the file it is given rather than its throwaway copy, the defect itself

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1665.json`, row `W1_check_opens_the_capture`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_copies.py, the same guard in integrity_ok, the module's names now read through the module
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 18 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_base_drive_not_the_mount_rehearses_equal`
  - `tests/test_intake_land_rehearse.py::test_a_failed_integrity_check_is_refused_naming_the_area[no room]`
  - `tests/test_intake_land_rehearse.py::test_a_landed_row_the_read_back_refuses_is_refused[assert_rows_gridless-a landed row carries an analysis value]`
  - `tests/test_intake_land_rehearse.py::test_a_landed_row_the_read_back_refuses_is_refused[assert_rows_identified-a landed row has no file id]`
  - `tests/test_intake_land_rehearse.py::test_a_live_plan_names_its_own_batch_s_rehearsal_and_the_lines`
  - `tests/test_intake_land_rehearse.py::test_a_name_the_live_folder_holds_is_refused_at_the_area`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_leaves_another_runs_area_alone`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_leaves_staging_music_and_database_as_they_were`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_another_year_s_batch_is_refused`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_the_live_library_is_refused`
  - `tests/test_intake_land_rehearse.py::test_no_room_for_the_check_refuses_before_its_copy`
  - `tests/test_intake_land_rehearse.py::test_on_a_drive_recorded_as_its_mount_it_is_as_it_was`
  - `tests/test_snapshot_wal_r1665.py::test_a_capture_taken_through_the_callers_own_handle_restores`
  - `tests/test_snapshot_wal_r1665.py::test_a_capture_taken_while_a_handle_holds_the_log_restores_what_it_recorded`
  - `tests/test_snapshot_wal_r1665.py::test_a_capture_that_lost_its_log_after_the_verdict_is_refused_by_the_plan[-wal]`
  - ... and 3 more, see the JSON sidecar

Old text:

```
                db = _writer().open_db(checked, check_app_version=False, unlock=unlock)
```

New text:

```
                db = _writer().open_db(snapshot_database, check_app_version=False, unlock=unlock)
```

### `r1665.W2_failed_copy_passes`

integrity_ok: a throwaway copy that cannot be made answers True

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1665.json`, row `W2_failed_copy_passes`
- Moved: the same text, now in src/cratekit/core/rb_copies.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_wal_r1665.py::test_a_check_whose_copy_cannot_be_made_has_not_passed`

Old text:

```
            exc,
        )
        return False
```

New text:

```
            exc,
        )
        return True
```

### `r1665.W3_no_release_of_the_copy`

integrity_ok: release only the session, leaving the pooled connection on the throwaway copy open while it is removed

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1665.json`, row `W3_no_release_of_the_copy`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_copies.py, the same guard in integrity_ok, its comment cut to its rule by the prose pass,, the module's names now read through the module
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`
- Collected: 14 against a baseline of 14
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_the_applying_run_opens_exactly_as_it_did`

Old text:

```
                # The full release: the throwaway directory is removed next.
                _writer().close_db(db)
```

New text:

```
                # The full release: the throwaway directory is removed next.
                db.close()
```

### `r1665.W4_quick_check_ignored`

integrity_ok: answer True whatever quick_check says

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1665.json`, row `W4_quick_check_ignored`
- Moved: the same text, now in src/cratekit/core/rb_copies.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_wal_r1665.py::test_damage_only_the_consistency_check_sees_fails_the_check`

Old text:

```
                return str(result).lower() == "ok"
```

New text:

```
                return True
```

### `r1665.W6_refused_open_passes`

integrity_ok: an open the gate refuses answers True

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1665.json`, row `W6_refused_open_passes`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_copies.py, the same guard in integrity_ok, the module's names now read through the module
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_a_damaged_snapshot_fails_its_integrity_check`
  - `tests/test_snapshot_wal_r1665.py::test_a_damaged_copy_still_fails_the_check`

Old text:

```
            except _writer().RekordboxUnavailable:
                return False
```

New text:

```
            except _writer().RekordboxUnavailable:
                return True
```

### `r1677.R1_raise_after_copy`

integrity_ok: raise the copy failure for any OSError, after the copy too, so an open that fails is told as no room

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1677.json`, row `R1_raise_after_copy`
- Moved: the same text, now in src/cratekit/core/rb_copies.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot_wal_r1665.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_check_room_r1677.py::test_an_open_that_fails_after_the_copy_is_a_failed_check_not_a_copy_failure`

Old text:

```
        if raise_copy_failure and not copied:
```

New text:

```
        if raise_copy_failure:
```

### `r1677.R3_copied_never_set`

integrity_ok: never mark the copy made, so an error after it raises as a copy failure

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1677.json`, row `R3_copied_never_set`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_copies.py, the same guard in integrity_ok, the module's names now read through the module
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot_wal_r1665.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_check_room_r1677.py::test_an_open_that_fails_after_the_copy_is_a_failed_check_not_a_copy_failure`

Old text:

```
        with _writer().disposable_copy(snapshot_database) as checked:
            copied = True
```

New text:

```
        with _writer().disposable_copy(snapshot_database) as checked:
            copied = False
```

### `r1677.R5_file_set_drops_playlist`

_copy_file_set: copy the companions but not the playlist file, so the measured list and the copied list drift

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1677.json`, row `R5_file_set_drops_playlist`
- Moved: the same text, now in src/cratekit/core/rb_copies.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot_wal_r1665.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`
- Collected: 278 against a baseline of 278
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_snapshot.py::test_the_legacy_playlist_file_travels_with_the_database`
  - `tests/test_snapshot_check_room_r1677.py::test_the_file_set_measured_is_the_one_the_check_copies`

Old text:

```
    for companion in companions:
        if companion.exists():
```

New text:

```
    for companion in companions[:-1]:
        if companion.exists():
```

### `r1890.P7_permissive_marker_read_through_an_alias_of_the_accessor`

rb_copies, a part, binds _writer() to a local name and reads the marker through it with a default of False

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1890.json`, row `P7_permissive_marker_read_through_an_alias_of_the_accessor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_parts_guard.py`, `tests/test_rb_writer_guard.py`
- Collected: 222 against a baseline of 222
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_no_module_in_the_package_reads_the_soft_delete_marker_permissively`
  - `tests/test_rb_writer_guard.py::test_only_the_declared_modules_read_the_soft_delete_marker_at_all`

Old text:

```
def _writer():
    """``rb_writer`` at call time: its seams are patched there, and it imports this module."""
    from cratekit.core import rb_writer

    return rb_writer

```

New text:

```
def _writer():
    """``rb_writer`` at call time: its seams are patched there, and it imports this module."""
    from cratekit.core import rb_writer

    return rb_writer


def _gone(row):
    w = _writer()
    return row.get(w.SOFT_DELETE_COLUMN, False)

```

### `r372-a.A10_copy_left_behind`

disposable_copy: leave the temporary directory and the copy in it

- File: `src/cratekit/core/rb_copies.py`
- Source: `r372-a.json`, row `A10_copy_left_behind`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_copies.py, the same guard in disposable_copy, the module's names now read through the module
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 15 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_doctor_fails_paths_resolved_over_a_majority_off_a_copy`
  - `tests/test_paths_resolved.py::test_doctor_reports_a_copy_it_could_not_open_as_unknown_rather_than_good`
  - `tests/test_paths_resolved.py::test_doctor_reports_a_minority_as_a_note_and_a_clean_collection_as_ok`
  - `tests/test_paths_resolved.py::test_setup_end_to_end_writes_the_rule_and_ends_on_a_doctor_that_reads_it`
  - `tests/test_paths_resolved.py::test_setup_leaves_a_damaged_library_to_the_notes_and_doctor`
  - `tests/test_paths_resolved.py::test_setup_notes_a_copy_it_could_not_open_and_leaves_the_verdict_to_doctor`
  - `tests/test_paths_resolved.py::test_setup_offers_nothing_when_the_root_sits_under_the_recorded_drive`
  - `tests/test_paths_resolved.py::test_setup_offers_nothing_when_the_two_drive_names_agree`
  - `tests/test_paths_resolved.py::test_setup_offers_the_root_when_rekordbox_still_records_the_old_name_twice`
  - `tests/test_paths_resolved.py::test_setup_offers_the_rule_from_the_databases_own_drive_names_off_a_copy`
  - `tests/test_paths_resolved.py::test_setup_records_a_current_drive_that_is_not_the_root_literally`
  - `tests/test_paths_resolved.py::test_setup_records_nothing_when_the_offer_goes_unanswered`
  - `tests/test_paths_resolved.py::test_the_copy_names_a_file_holding_none_of_the_canary_tables`
  - `tests/test_paths_resolved.py::test_the_copy_names_an_empty_file_by_its_size_and_its_configured_path`
  - `tests/test_paths_resolved.py::test_the_disposable_copy_is_private_and_gone_afterwards`

Old text:

```
        shutil.rmtree(directory, ignore_errors=True)
```

New text:

```
        pass
```

### `r372-a.A11_copy_under_a_running_application`

read_only_copy: drop its own closed assertion, the layer beneath doctor and setup

- File: `src/cratekit/core/rb_copies.py`
- Source: `r372-a.json`, row `A11_copy_under_a_running_application`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_copies.py, the same guard in read_only_copy, the module's names now read through the module
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 1 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_the_read_only_copy_refuses_under_a_running_application_on_its_own`

Old text:

```
    _writer().assert_rekordbox_closed("copying the database for a read only look")
```

New text:

```
    pass
```

### `r372-a.A12_separator_kept`

recorded_db_drives: keep the trailing separator rekordbox stores, so the rule never matches

- File: `src/cratekit/core/rb_copies.py`
- Source: `r372-a.json`, row `A12_separator_kept`
- Moved: the same text, now in src/cratekit/core/rb_copies.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 7 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_recorded_drives_strip_the_separator_rekordbox_stores_and_blank_is_none`
  - `tests/test_paths_resolved.py::test_setup_end_to_end_writes_the_rule_and_ends_on_a_doctor_that_reads_it`
  - `tests/test_paths_resolved.py::test_setup_offers_nothing_when_the_root_sits_under_the_recorded_drive`
  - `tests/test_paths_resolved.py::test_setup_offers_nothing_when_the_two_drive_names_agree`
  - `tests/test_paths_resolved.py::test_setup_offers_the_root_when_rekordbox_still_records_the_old_name_twice`
  - `tests/test_paths_resolved.py::test_setup_offers_the_rule_from_the_databases_own_drive_names_off_a_copy`
  - `tests/test_paths_resolved.py::test_setup_records_a_current_drive_that_is_not_the_root_literally`

Old text:

```
        stripped = value.strip().rstrip("/\\")
```

New text:

```
        stripped = value.strip()
```

### `r663-a.M1_empty_not_refused_before_open`

the size of the copy is no longer asked before the open, so an empty copy reaches the binding and is classified only if the canary is what fails

- File: `src/cratekit/core/rb_copies.py`
- Source: `r663-a.json`, row `M1_empty_not_refused_before_open`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_copies.py, the same guard in read_only_copy, the module's names now read through the module
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`
- Collected: 51 against a baseline of 51
- Kills: 4 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_doctor_reports_an_empty_database_path_under_the_same_cause`
  - `tests/test_paths_resolved.py::test_setup_refuses_a_database_path_that_is_not_a_library_and_records_nothing[empty]`
  - `tests/test_paths_resolved.py::test_the_copy_names_an_empty_file_by_its_size_and_its_configured_path`
  - `tests/test_paths_resolved.py::test_the_file_whose_tables_are_listed_is_only_ever_a_copy[empty]`

Old text:

```
        refusal = None if copied.stat().st_size else _writer()._not_a_library(Path(source), copied)
```

New text:

```
        refusal = None
```

### `r663-a.M5_failed_listing_returns_empty_set`

a table listing whose query fails answers an empty set rather than None, so a file that could not be read is reported as holding nothing

- File: `src/cratekit/core/rb_copies.py`
- Source: `r663-a.json`, row `M5_failed_listing_returns_empty_set`
- Moved: the same text, now in src/cratekit/core/rb_copies.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`
- Collected: 51 against a baseline of 51
- Kills: 2 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_a_file_that_is_not_sqlite_at_all_keeps_the_canarys_refusal`
  - `tests/test_paths_resolved.py::test_setup_leaves_a_damaged_library_to_the_notes_and_doctor`

Old text:

```
        return {str(row[0]) for row in rows}
    except Exception:  # noqa: BLE001 - an unlistable file keeps the canary's refusal
        return None
```

New text:

```
        return {str(row[0]) for row in rows}
    except Exception:  # noqa: BLE001 - an unlistable file keeps the canary's refusal
        return set()
```

### `r663-a.M6_listing_opened_with_the_key_always`

the table listing opens every copy with the key rather than asking the header, so a plain foreign file cannot be listed

- File: `src/cratekit/core/rb_copies.py`
- Source: `r663-a.json`, row `M6_listing_opened_with_the_key_always`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_copies.py, the same guard in _copy_tables, the module's names now read through the module
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`
- Collected: 51 against a baseline of 51
- Kills: 2 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_setup_refuses_a_database_path_that_is_not_a_library_and_records_nothing[foreign]`
  - `tests/test_paths_resolved.py::test_the_copy_names_a_file_holding_none_of_the_canary_tables`

Old text:

```
            db = Rekordbox6Database(path=str(copied), unlock=_writer().unlock_needed(copied))
```

New text:

```
            db = Rekordbox6Database(path=str(copied), unlock=True)
```

### `r663-b.M2_every_open_refusal_classified`

the canary reason gate is removed, so any refusal on the way in, a pin or a failed open, is also asked whether the copy is a library

- File: `src/cratekit/core/rb_copies.py`
- Source: `r663-b.json`, row `M2_every_open_refusal_classified`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_copies.py, the same guard in read_only_copy, the module's names now read through the module
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`
- Collected: 51 against a baseline of 51
- Kills: 1 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_a_refusal_on_the_way_in_is_not_reclassified_as_a_wrong_path`

Old text:

```
            if exc.cause.reason != "canary-read-failed":
                raise
            refusal = _writer()._not_a_library(Path(source), copied)
```

New text:

```
            refusal = _writer()._not_a_library(Path(source), copied)
```

### `r1890.P3_unreserved_slug_in_rb_nodes`

rb_nodes, a part, raises the node move's confinement refusal under a slug with no reserved code

- File: `src/cratekit/core/rb_nodes.py`
- Source: `r1890.json`, row `P3_unreserved_slug_in_rb_nodes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_parts_guard.py`, `tests/test_rb_writer_guard.py`
- Collected: 222 against a baseline of 222
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_parts_guard.py::test_every_refusal_the_writer_or_a_part_raises_through_a_factory_is_reserved`

Old text:

```
        raise _writer()._unavailable(
            "whitelist-violation",
            "the node change reached rows it did not plan
```

New text:

```
        raise _writer()._unavailable(
            "node-change-unconfined",
            "the node change reached rows it did not plan
```

### `r1890.P4_unreadable_slug_in_rb_nodes`

rb_nodes, a part, raises the confinement refusal with its slug held in a name, which no scan reads

- File: `src/cratekit/core/rb_nodes.py`
- Source: `r1890.json`, row `P4_unreadable_slug_in_rb_nodes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_parts_guard.py`, `tests/test_rb_writer_guard.py`
- Collected: 222 against a baseline of 222
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_parts_guard.py::test_every_refusal_names_its_reason_as_a_literal_the_scan_can_read`

Old text:

```
        raise _writer()._unavailable(
            "whitelist-violation",
            "the node change reached rows it did not plan
```

New text:

```
        reason = "node-change-unconfined"
        raise _writer()._unavailable(
            reason,
            "the node change reached rows it did not plan
```

### `r1890.P5_gate_name_in_rb_nodes`

rb_nodes, a part, names the cloud sync gate and its flag, the command vocabulary the core may not learn

- File: `src/cratekit/core/rb_nodes.py`
- Source: `r1890.json`, row `P5_gate_name_in_rb_nodes`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 1005 against a baseline of 1005
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_the_core_writer_never_learns_the_gates_name_or_any_flag_string`

Old text:

```
def _writer():
    """``rb_writer`` at call time: its seams are patched there, and it imports this module."""
    from cratekit.core import rb_writer

    return rb_writer

```

New text:

```
def _writer():
    """``rb_writer`` at call time: its seams are patched there, and it imports this module."""
    from cratekit.core import rb_writer

    return rb_writer


_GATE = ("write.cloudsync.unreadable", "--decision")

```

### `r1890.P6_permissive_marker_read_through_the_accessor`

rb_nodes, a part, reads the soft delete marker through _writer() with a default of 0, so a removed row reads as active

- File: `src/cratekit/core/rb_nodes.py`
- Source: `r1890.json`, row `P6_permissive_marker_read_through_the_accessor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_parts_guard.py`, `tests/test_rb_writer_guard.py`
- Collected: 222 against a baseline of 222
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_no_module_in_the_package_reads_the_soft_delete_marker_permissively`
  - `tests/test_rb_writer_guard.py::test_only_the_declared_modules_read_the_soft_delete_marker_at_all`

Old text:

```
def _writer():
    """``rb_writer`` at call time: its seams are patched there, and it imports this module."""
    from cratekit.core import rb_writer

    return rb_writer

```

New text:

```
def _writer():
    """``rb_writer`` at call time: its seams are patched there, and it imports this module."""
    from cratekit.core import rb_writer

    return rb_writer


def _gone(row):
    return getattr(row, _writer().SOFT_DELETE_COLUMN, 0)

```

### `r235-b.M22_nested_namesake_is_a_root`

a folder of the tree's name anywhere in the library is a candidate root

- File: `src/cratekit/core/rb_nodes.py`
- Source: `r235-b.json`, row `M22_nested_namesake_is_a_root`
- Moved: U953 inlined _is_folder into is_folder, so the condition now reads is_folder; dropping its parent clause is the same unbounded root
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_a_namesake_nested_under_another_folder_is_not_a_root`
  - `tests/test_cutover_cli.py::test_a_nested_namesake_alone_is_no_root_at_all`

Old text:

```
        if is_folder(playlist)
        and str(getattr(playlist, "ParentID", "")) in ROOT_PARENT_SENTINELS
```

New text:

```
        if is_folder(playlist)
```

### `r235-b.M23_playlist_is_a_root`

a playlist of the tree's name under the playlist root is a candidate root

- File: `src/cratekit/core/rb_nodes.py`
- Source: `r235-b.json`, row `M23_playlist_is_a_root`
- Moved: U953 inlined _is_folder into is_folder, so the condition now reads is_folder; dropping that folder clause is the same playlist taken as a root
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_a_playlist_of_the_trees_name_is_not_a_root`

Old text:

```
        if is_folder(playlist)
        and str(getattr(playlist, "ParentID", "")) in ROOT_PARENT_SENTINELS
```

New text:

```
        if str(getattr(playlist, "ParentID", "")) in ROOT_PARENT_SENTINELS
```

### `r758-a.W7_removed_row_marked_again`

remove_memberships marks a row that is already removed and reports it, so a second removal counts a row it did not remove

- File: `src/cratekit/core/rb_nodes.py`
- Source: `r758-a.json`, row `W7_removed_row_marked_again`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_nodes.py, the same guard in remove_memberships, the module's names now read through the module
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_adopt_move.py`
- Collected: 300 against a baseline of 300
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_removed_membership_is_not_held_and_not_present`

Old text:

```
        if key not in wanted or _writer().membership_removed(song):
```

New text:

```
        if key not in wanted:
```

### `u111-a.A1_folder_refused`

The writer no longer refuses a folder or smart playlist as the node it moves or removes

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u111-a.json`, row `A1_folder_refused`
- Moved: the same text, now in src/cratekit/core/rb_nodes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_rb_writer_guard.py`
- Collected: 243 against a baseline of 243
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_the_writer_refuses_a_folder_a_parent_not_a_folder_and_a_removed_playlist`

Old text:

```
    if int(getattr(playlist, "Attribute", -1)) != 0:
        raise _node_refusal(
```

New text:

```
    if False:
        raise _node_refusal(
```

### `u111-a.A3_parent_not_folder`

move_playlist_node no longer refuses a parent that is not a live folder

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u111-a.json`, row `A3_parent_not_folder`
- Moved: U953 inlined _is_folder into is_folder, so the parent check of move_playlist_node now reads is_folder and disabling it is the same dropped refusal
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_rb_writer_guard.py`
- Collected: 243 against a baseline of 243
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_the_writer_refuses_a_folder_a_parent_not_a_folder_and_a_removed_playlist`

Old text:

```
    if not is_folder(parent) or _writer().node_removed(parent):
```

New text:

```
    if False:
```

