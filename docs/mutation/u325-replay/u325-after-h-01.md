# Mutation table: u325-after-h-01

Measured by `scripts/mutate.py` on 2026-11-22 22:31 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 72.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 16:29 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 4, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u295.S10_stuck_accepted` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 4 | killed |
| `u295.S11_no_read_back` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 1 | killed |
| `u295.S12_cleanup_ignores_launchd` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 1 | killed |
| `u295.S13_cleanup_keeps_plist` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 3 | killed |
| `u295.S14_dirs_not_resolved` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 11 | killed |
| `u295.S15_override_relative` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 1 | killed |
| `u295.S16_any_bin_prefix` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 1 | killed |
| `u295.S17_plist_mode` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 1 | killed |
| `u295.S18_crate_exec_bit` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 1 | killed |
| `u295.S19_keys_unchecked` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 1 | killed |
| `u295.S1_platform_guard` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 6 | killed |
| `u295.S20_gone_crate_unchecked` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 1 | killed |
| `u295.S21_run_at_load_unchecked` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 1 | killed |
| `u295.S22_env_names_unchecked` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 2 | killed |
| `u295.S23_show_always_clean` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 26 | killed |
| `u295.S24_loaded_without_plist` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 1 | killed |
| `u295.S25_install_lockless` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 2 | killed |
| `u295.S2_root_guard` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 3 | killed |
| `u295.S3_argv_widened` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 7 | killed |
| `u295.S4_run_at_load` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 7 | killed |
| `u295.S5_read_words_after_night` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 2 | killed |
| `u295.S6_daemons_directory` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 2 | killed |
| `u295.S7_user_domain` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 63 | killed |
| `u295.S8_unknown_read_absent` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 2 | killed |
| `u295.S9_skip_bootout_on_unknown` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 1 | killed |
| `u265.M10_empty_index_scored` | `src/cratekit/acquire/match.py` | maintainer | 24 file(s) | 2835 | 1 | killed |
| `u265.M1_narrow_split_everywhere` | `src/cratekit/acquire/match.py` | user | 24 file(s) | 2835 | 2 | killed |
| `u265.M2_python_split_everywhere` | `src/cratekit/acquire/match.py` | user | 24 file(s) | 2835 | 2 | killed |
| `u265.M2b_width_off_by_one` | `src/cratekit/acquire/match.py` | user | 24 file(s) | 2835 | 1 | killed |
| `u265.M3_words_not_sorted` | `src/cratekit/acquire/match.py` | user | 24 file(s) | 2835 | 18 | killed |
| `u265.M4_query_not_sorted` | `src/cratekit/acquire/match.py` | user | 24 file(s) | 2835 | 42 | killed |
| `u265.M5_hit_named_by_its_sorted_form` | `src/cratekit/acquire/match.py` | user | 24 file(s) | 2835 | 61 | killed |
| `u265.M6_cache_misaligned` | `src/cratekit/acquire/match.py` | user | 24 file(s) | 2835 | 15 | killed |
| `u265.M7_cache_never_kept` | `src/cratekit/acquire/match.py` | maintainer | 24 file(s) | 2835 | 1 | killed |
| `u265.M8_other_scorer` | `src/cratekit/acquire/match.py` | user | 24 file(s) | 2835 | 39 | killed |
| `u206-b.M10b_day_coefficient_halved` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1135 | 3 | killed |
| `u206-b.M2b_disabled_recall_composite` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1135 | 8 | killed |
| `u206.M11_unreadable_answer_kept` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1135 | 4 | killed |
| `u206.M12_corrupt_file_not_set_aside` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1135 | 3 | killed |
| `u206.M13_write_without_merge` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1135 | 5 | killed |
| `u206.M16_said_not_found_widened` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1135 | 3 | killed |
| `u206.M1_recall_never_hits` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1135 | 19 | killed |
| `u206.M21_override_ignored` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1135 | 1 | killed |
| `u206.M3_disabled_still_remembers` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1135 | 1 | killed |
| `u206.M4_unfolded_spelling_kept` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1135 | 1 | killed |
| `u206.M5_country_ignored` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1135 | 5 | killed |
| `u206.M6_not_found_lives_as_found` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1135 | 1 | killed |
| `u206.M7_not_found_ignores_shorter_setting` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1135 | 1 | killed |
| `u206.M8_expiry_off_by_one` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1135 | 5 | killed |
| `u206.M9_future_stamp_trusted` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1135 | 1 | killed |
| `u206.M18_catalogue_keeps_any_gone` | `src/cratekit/label/tidal_catalogue.py` | user | 9 file(s) | 1135 | 2 | killed |
| `u206.M14_account_keeps_invalid_isrc` | `src/cratekit/modules/outbound/tidal_account.py` | user | 9 file(s) | 1135 | 2 | killed |
| `u206.M17_account_hit_ignored` | `src/cratekit/modules/outbound/tidal_account.py` | user | 9 file(s) | 1135 | 13 | killed |
| `u206.M22_days_validation_dropped` | `src/cratekit/core/config.py` | user | 9 file(s) | 1135 | 1 | killed |
| `r1394.A1_recorder_never_told` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 5 | killed |
| `r1394.A2_sent_one_short` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 5 | killed |
| `r1394.A3_landed_overstated` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 4 | killed |
| `r1394.A4_412_not_brought_down` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 2 | killed |
| `r1394.A5_any_failure_brought_down` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 3 | killed |
| `r1411.A1_agreed_order_always_stands` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 11 | killed |
| `r1411.A2_removed_tracks_asked_of_the_reading` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 3 | killed |
| `r1411.A3_added_tracks_asked_of_the_agreed_order` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 7 | killed |
| `r1411.A5_duplicates_counted_twice` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 1 | killed |
| `r1411.E1_expect_compared_as_membership` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 1 | killed |
| `r1411.E4_membership_always_agrees` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 2 | killed |
| `r1411.S1_settled_ignores_agreed` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 2 | killed |
| `r1411.S2_agreed_stands_in_for_membership` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 1 | killed |

## Row definitions

### `u295.S10_stuck_accepted`

_boot_out: accept an agent still loaded after its bootout

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S10_stuck_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 4 (killed)
- Killed:
  - `tests/test_schedule.py::test_a_bootout_launchd_ignores_is_said_in_words_a_person_reads`
  - `tests/test_schedule.py::test_a_remove_launchd_does_not_confirm_keeps_the_plist[bootout fails]`
  - `tests/test_schedule.py::test_a_remove_launchd_does_not_confirm_keeps_the_plist[stuck]`
  - `tests/test_schedule.py::test_an_agent_launchd_will_not_let_go_of_is_not_replaced`

Old text:

```
    after, check = loaded()
    if after != NOT_LOADED:
        if not out.ok:
```

New text:

```
    after, check = loaded()
    if after == UNKNOWN:
        if not out.ok:
```

### `u295.S11_no_read_back`

_install: trust bootstrap's exit and never read launchd back

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S11_no_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 1 (killed)
- Killed:
  - `tests/test_schedule.py::test_a_bootstrap_launchd_does_not_then_hold_is_refused_and_leaves_nothing`

Old text:

```
    state, check = loaded() if answer.ok else (UNKNOWN, answer)
```

New text:

```
    state, check = (LOADED, answer) if answer.ok else (UNKNOWN, answer)
```

### `u295.S12_cleanup_ignores_launchd`

_install: delete the plist on a failed load whatever launchd still holds

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S12_cleanup_ignores_launchd`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 1 (killed)
- Killed:
  - `tests/test_schedule.py::test_a_failed_load_launchd_may_still_hold_keeps_its_plist`

Old text:

```
        failed = answer if not answer.ok else check
        if after != NOT_LOADED:
```

New text:

```
        failed = answer if not answer.ok else check
        if False:
```

### `u295.S13_cleanup_keeps_plist`

_install: keep the plist written for a failed load, leaving an agent half installed

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S13_cleanup_keeps_plist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 3 (killed)
- Killed:
  - `tests/test_schedule.py::test_a_bootstrap_launchd_does_not_then_hold_is_refused_and_leaves_nothing`
  - `tests/test_schedule.py::test_a_bootstrap_that_fails_is_refused_in_its_words_and_leaves_nothing`
  - `tests/test_schedule.py::test_a_failed_replace_says_the_earlier_schedule_is_gone_too`

Old text:

```
        _remove_plist(target)
        earlier = 
```

New text:

```
        pass
        earlier = 
```

### `u295.S14_dirs_not_resolved`

environment: carry no resolved directory, so an XDG install's night reads another installation

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S14_dirs_not_resolved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 11 (killed)
- Killed:
  - `tests/test_schedule.py::test_a_relative_override_is_carried_absolute`
  - `tests/test_schedule.py::test_an_installation_found_through_xdg_alone_is_the_one_the_agent_reads`
  - `tests/test_schedule.py::test_install_and_show_agree_on_the_environment_shape`
  - `tests/test_schedule.py::test_show_fails_over_an_agent_that_reads_another_installation_or_more_words[no config]`
  - `tests/test_schedule.py::test_show_fails_over_an_agent_that_reads_another_installation_or_more_words[no state]`
  - `tests/test_schedule.py::test_show_never_reads_launchd_it_cannot_read_as_not_loaded`
  - `tests/test_schedule.py::test_show_reads_an_installed_agent_launchd_does_not_hold`
  - `tests/test_schedule.py::test_show_reads_an_installed_loaded_agent`
  - `tests/test_schedule.py::test_show_reads_the_night_line_from_the_state_the_agent_carries`
  - `tests/test_schedule.py::test_show_writes_nothing_and_asks_launchd_only_to_print`
  - `tests/test_schedule.py::test_the_agent_carries_a_fixed_path_the_resolved_directories_and_nothing_else`

Old text:

```
        carried[name] = str(_absolute(directory))
```

New text:

```
        pass
```

### `u295.S15_override_relative`

environment: carry an override as set, so a relative one names another place for launchd

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S15_override_relative`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 1 (killed)
- Killed:
  - `tests/test_schedule.py::test_a_relative_override_is_carried_absolute`

Old text:

```
            carried[name] = str(_absolute(value))
```

New text:

```
            carried[name] = value
```

### `u295.S16_any_bin_prefix`

environment: carry every CRATEKIT_BIN_ name set, not only the binaries this build runs

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S16_any_bin_prefix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 1 (killed)
- Killed:
  - `tests/test_schedule.py::test_the_agent_carries_a_fixed_path_the_resolved_directories_and_nothing_else`

Old text:

```
    for name in (*override_names(), *binary_names()):
```

New text:

```
    for name in (*override_names(), *(n for n in source if n.startswith(binaries.ENV_PREFIX))):
```

### `u295.S17_plist_mode`

PLIST_MODE: the plist readable by everyone on the Mac

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S17_plist_mode`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 1 (killed)
- Killed:
  - `tests/test_schedule.py::test_install_writes_one_agent_that_runs_the_night_alone_and_loads_it`

Old text:

```
PLIST_MODE = 0o600
```

New text:

```
PLIST_MODE = 0o644
```

### `u295.S18_crate_exec_bit`

crate_runs: never ask whether the crate is executable

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S18_crate_exec_bit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 1 (killed)
- Killed:
  - `tests/test_schedule.py::test_a_crate_that_cannot_run_is_refused_and_nothing_is_written[not executable]`

Old text:

```
    return found.is_absolute() and found.is_file() and os.access(found, os.X_OK)
```

New text:

```
    return found.is_absolute() and found.is_file()
```

### `u295.S19_keys_unchecked`

read_agent: never compare the plist's keys, so a Program key passes

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S19_keys_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 1 (killed)
- Killed:
  - `tests/test_schedule.py::test_show_fails_over_an_agent_edited_to_be_anything_but_the_nights[a program key]`

Old text:

```
    if keys != PLIST_KEYS:

```

New text:

```
    if False:

```

### `u295.S1_platform_guard`

_macos_only: never refuse another platform, so a schedule is attempted where there is no launchd

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S1_platform_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 6 (killed)
- Killed:
  - `tests/test_schedule.py::test_any_platform_but_macos_refuses_naming_it[linux-install]`
  - `tests/test_schedule.py::test_any_platform_but_macos_refuses_naming_it[linux-remove]`
  - `tests/test_schedule.py::test_any_platform_but_macos_refuses_naming_it[linux-show]`
  - `tests/test_schedule.py::test_any_platform_but_macos_refuses_naming_it[win32-install]`
  - `tests/test_schedule.py::test_any_platform_but_macos_refuses_naming_it[win32-remove]`
  - `tests/test_schedule.py::test_any_platform_but_macos_refuses_naming_it[win32-show]`

Old text:

```
    if running != MACOS:

```

New text:

```
    if False:

```

### `u295.S20_gone_crate_unchecked`

read_agent: never ask whether the crate it runs can run

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S20_gone_crate_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 1 (killed)
- Killed:
  - `tests/test_schedule.py::test_show_fails_over_an_agent_whose_crate_is_gone`

Old text:

```
    if crate is not None and not crate_runs(crate):

```

New text:

```
    if False:

```

### `u295.S21_run_at_load_unchecked`

read_agent: accept an agent that runs at load

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S21_run_at_load_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 1 (killed)
- Killed:
  - `tests/test_schedule.py::test_show_fails_over_an_agent_edited_to_be_anything_but_the_nights[run at load]`

Old text:

```
    if document.get("RunAtLoad") is not False:

```

New text:

```
    if False:

```

### `u295.S22_env_names_unchecked`

read_agent: accept an environment name this build never carries

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S22_env_names_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 2 (killed)
- Killed:
  - `tests/test_schedule.py::test_show_fails_over_an_agent_edited_to_be_anything_but_the_nights[a raised limit]`
  - `tests/test_schedule.py::test_show_never_prints_a_value_this_build_would_not_carry`

Old text:

```
    unknown = sorted(set(env) - allowed_names())
```

New text:

```
    unknown = []
```

### `u295.S23_show_always_clean`

show: exit clean whatever problems were read

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S23_show_always_clean`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 26 (killed)
- Killed:
  - `tests/test_schedule.py::test_show_fails_over_an_agent_edited_to_be_anything_but_the_nights[a program key]`
  - `tests/test_schedule.py::test_show_fails_over_an_agent_edited_to_be_anything_but_the_nights[a raised limit]`
  - `tests/test_schedule.py::test_show_fails_over_an_agent_edited_to_be_anything_but_the_nights[another program]`
  - `tests/test_schedule.py::test_show_fails_over_an_agent_edited_to_be_anything_but_the_nights[every hour]`
  - `tests/test_schedule.py::test_show_fails_over_an_agent_edited_to_be_anything_but_the_nights[hour 99]`
  - `tests/test_schedule.py::test_show_fails_over_an_agent_edited_to_be_anything_but_the_nights[no calendar]`
  - `tests/test_schedule.py::test_show_fails_over_an_agent_edited_to_be_anything_but_the_nights[one weekday]`
  - `tests/test_schedule.py::test_show_fails_over_an_agent_edited_to_be_anything_but_the_nights[run at load]`
  - `tests/test_schedule.py::test_show_fails_over_an_agent_edited_to_be_anything_but_the_nights[split log]`
  - `tests/test_schedule.py::test_show_fails_over_an_agent_edited_to_be_anything_but_the_nights[two times]`
  - `tests/test_schedule.py::test_show_fails_over_an_agent_launchd_holds_with_no_plist`
  - `tests/test_schedule.py::test_show_fails_over_an_agent_that_reads_another_installation_or_more_words[a true hour]`
  - `tests/test_schedule.py::test_show_fails_over_an_agent_that_reads_another_installation_or_more_words[an answer]`
  - `tests/test_schedule.py::test_show_fails_over_an_agent_that_reads_another_installation_or_more_words[an empty word]`
  - `tests/test_schedule.py::test_show_fails_over_an_agent_that_reads_another_installation_or_more_words[log outside its state]`
  - ... and 11 more, see the JSON sidecar

Old text:

```
    if not problems:
        return ctx.envelope(data=data, outcome=Outcome.NO_OP)
```

New text:

```
    if True:
        return ctx.envelope(data=data, outcome=Outcome.NO_OP)
```

### `u295.S24_loaded_without_plist`

show: a loaded agent with no plist reads as a clean report

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S24_loaded_without_plist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 1 (killed)
- Killed:
  - `tests/test_schedule.py::test_show_fails_over_an_agent_launchd_holds_with_no_plist`

Old text:

```
        if found is None and unreadable is None:

```

New text:

```
        if False:

```

### `u295.S25_install_lockless`

install: boot the agent out without the staging lock, so a night in progress is ended

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S25_install_lockless`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 2 (killed)
- Killed:
  - `tests/test_schedule.py::test_a_night_in_progress_is_never_booted_out[install]`
  - `tests/test_schedule.py::test_only_the_one_seam_starts_a_process`

Old text:

```
    with staging_lock.held("crate schedule install", run_id=ctx.run.run_id):
```

New text:

```
    with open(os.devnull):
```

### `u295.S2_root_guard`

_as_the_person: never refuse root, so the agent is bootstrapped into gui/0

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S2_root_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 3 (killed)
- Killed:
  - `tests/test_schedule.py::test_root_is_refused_and_launchd_is_never_asked[install]`
  - `tests/test_schedule.py::test_root_is_refused_and_launchd_is_never_asked[remove]`
  - `tests/test_schedule.py::test_root_is_refused_and_launchd_is_never_asked[show]`

Old text:

```
    if uid() == 0:

```

New text:

```
    if False:

```

### `u295.S3_argv_widened`

agent: the plist's program arguments carry an answer after sync night

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S3_argv_widened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 7 (killed)
- Killed:
  - `tests/test_schedule.py::test_install_and_show_agree_on_the_environment_shape`
  - `tests/test_schedule.py::test_install_writes_one_agent_that_runs_the_night_alone_and_loads_it`
  - `tests/test_schedule.py::test_show_never_reads_launchd_it_cannot_read_as_not_loaded`
  - `tests/test_schedule.py::test_show_reads_an_installed_agent_launchd_does_not_hold`
  - `tests/test_schedule.py::test_show_reads_an_installed_loaded_agent`
  - `tests/test_schedule.py::test_show_reads_the_night_line_from_the_state_the_agent_carries`
  - `tests/test_schedule.py::test_show_writes_nothing_and_asks_launchd_only_to_print`

Old text:

```
        "ProgramArguments": [str(crate), *NIGHT_ARGV],
```

New text:

```
        "ProgramArguments": [str(crate), *NIGHT_ARGV, "-d", "intake.land.native=go"],
```

### `u295.S4_run_at_load`

agent: the plist runs the night at load, so an install starts a pass at once

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S4_run_at_load`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 7 (killed)
- Killed:
  - `tests/test_schedule.py::test_install_and_show_agree_on_the_environment_shape`
  - `tests/test_schedule.py::test_install_writes_one_agent_that_runs_the_night_alone_and_loads_it`
  - `tests/test_schedule.py::test_show_never_reads_launchd_it_cannot_read_as_not_loaded`
  - `tests/test_schedule.py::test_show_reads_an_installed_agent_launchd_does_not_hold`
  - `tests/test_schedule.py::test_show_reads_an_installed_loaded_agent`
  - `tests/test_schedule.py::test_show_reads_the_night_line_from_the_state_the_agent_carries`
  - `tests/test_schedule.py::test_show_writes_nothing_and_asks_launchd_only_to_print`

Old text:

```
        "RunAtLoad": False,
    }
```

New text:

```
        "RunAtLoad": True,
    }
```

### `u295.S5_read_words_after_night`

read_agent: accept words after sync night, so show reads clean over an agent given an answer

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S5_read_words_after_night`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 2 (killed)
- Killed:
  - `tests/test_schedule.py::test_show_fails_over_an_agent_that_reads_another_installation_or_more_words[an answer]`
  - `tests/test_schedule.py::test_show_fails_over_an_agent_that_reads_another_installation_or_more_words[an empty word]`

Old text:

```
        and program[1:] == NIGHT_ARGV

```

New text:

```
        and program[1:3] == NIGHT_ARGV

```

### `u295.S6_daemons_directory`

launch_agents_dir: the plist goes beside the system's daemons instead of the person's agents

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S6_daemons_directory`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 2 (killed)
- Killed:
  - `tests/test_schedule.py::test_the_default_directory_is_the_persons_own_launch_agents`
  - `tests/test_schedule.py::test_the_module_names_no_system_domain_and_no_system_directory`

Old text:

```
    return Path.home() / "Library" / "LaunchAgents"
```

New text:

```
    return Path.home() / "Library" / "LaunchDaemons"
```

### `u295.S7_user_domain`

_domain: load into user/<uid> instead of the person's GUI login

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S7_user_domain`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 63 (killed)
- Killed:
  - `tests/test_schedule.py::test_a_binary_the_install_finds_on_its_path_alone_is_on_the_agents_path`
  - `tests/test_schedule.py::test_a_bootout_launchd_ignores_is_said_in_words_a_person_reads`
  - `tests/test_schedule.py::test_a_bootout_refused_over_an_agent_then_absent_boots_out_nothing`
  - `tests/test_schedule.py::test_a_bootstrap_launchd_does_not_then_hold_is_refused_and_leaves_nothing`
  - `tests/test_schedule.py::test_a_bootstrap_that_fails_is_refused_in_its_words_and_leaves_nothing`
  - `tests/test_schedule.py::test_a_failed_load_launchd_may_still_hold_keeps_its_plist`
  - `tests/test_schedule.py::test_a_failed_replace_says_the_earlier_schedule_is_gone_too`
  - `tests/test_schedule.py::test_a_night_in_progress_is_never_booted_out[install]`
  - `tests/test_schedule.py::test_a_night_in_progress_is_never_booted_out[remove]`
  - `tests/test_schedule.py::test_a_plist_left_without_launchd_holding_it_is_replaced`
  - `tests/test_schedule.py::test_a_relative_override_is_carried_absolute`
  - `tests/test_schedule.py::test_a_remove_launchd_does_not_confirm_keeps_the_plist[bootout fails]`
  - `tests/test_schedule.py::test_a_remove_launchd_does_not_confirm_keeps_the_plist[print unreadable]`
  - `tests/test_schedule.py::test_a_remove_launchd_does_not_confirm_keeps_the_plist[stuck]`
  - `tests/test_schedule.py::test_a_replace_whose_write_fails_says_the_earlier_schedule_is_off`
  - ... and 48 more, see the JSON sidecar

Old text:

```
    return f"gui/{uid()}"
```

New text:

```
    return f"user/{uid()}"
```

### `u295.S8_unknown_read_absent`

loaded: any print failure reads as not loaded, absence read as evidence of absence

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S8_unknown_read_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 2 (killed)
- Killed:
  - `tests/test_schedule.py::test_a_remove_launchd_does_not_confirm_keeps_the_plist[print unreadable]`
  - `tests/test_schedule.py::test_show_never_reads_launchd_it_cannot_read_as_not_loaded`

Old text:

```
    if answer.code == NOT_LOADED_CODE:

```

New text:

```
    if True:

```

### `u295.S9_skip_bootout_on_unknown`

_boot_out: skip the bootout when launchd cannot be read

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S9_skip_bootout_on_unknown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 1 (killed)
- Killed:
  - `tests/test_schedule.py::test_a_remove_launchd_does_not_confirm_keeps_the_plist[print unreadable]`

Old text:

```
    if state == NOT_LOADED:
        return False
    out = launchctl(
```

New text:

```
    if state != LOADED:
        return False
    out = launchctl(
```

### `u265.M10_empty_index_scored`

_approximate: drop the early return on an empty index (an existing guard, sampled), so an empty library sorts the wanted token and asks the scorer

- File: `src/cratekit/acquire/match.py`
- Source: `u265.json`, row `M10_empty_index_scored`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`
- Collected: 2835 against a baseline of 2835
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_each_name_is_sorted_once_for_the_index_and_each_row_once_a_call`

Old text:

```
    if not index.by_recording:
        return ()
    from rapidfuzz import fuzz, process

    recordings, sorted_choices
```

New text:

```
    from rapidfuzz import fuzz, process

    recordings, sorted_choices
```

### `u265.M1_narrow_split_everywhere`

_sorted_words: split every string on the narrow set, so a wide string keeps U+0085 and U+00A0 inside a word where the scorer splits

- File: `src/cratekit/acquire/match.py`
- Source: `u265.json`, row `M1_narrow_split_everywhere`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`
- Collected: 2835 against a baseline of 2835
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_every_pair_scores_the_same_through_the_sorted_form`
  - `tests/test_match_states.py::test_the_word_sort_splits_on_exactly_the_whitespace_the_scorer_splits_on`

Old text:

```
    if token and max(token) > "\xff":
        words = token.split()
```

New text:

```
    if False:
        words = token.split()
```

### `u265.M2_python_split_everywhere`

_sorted_words: split every string on Python whitespace, so a narrow string splits on U+0085 and U+00A0 where the scorer does not

- File: `src/cratekit/acquire/match.py`
- Source: `u265.json`, row `M2_python_split_everywhere`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`
- Collected: 2835 against a baseline of 2835
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_every_pair_scores_the_same_through_the_sorted_form`
  - `tests/test_match_states.py::test_the_word_sort_splits_on_exactly_the_whitespace_the_scorer_splits_on`

Old text:

```
    if token and max(token) > "\xff":
        words = token.split()
```

New text:

```
    if True:
        words = token.split()
```

### `u265.M2b_width_off_by_one`

_sorted_words: read a string as wide from U+00FF rather than U+0100, so a narrow name ending in y with a diaeresis splits on U+00A0 where the scorer does not (review round one's finding)

- File: `src/cratekit/acquire/match.py`
- Source: `u265.json`, row `M2b_width_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`
- Collected: 2835 against a baseline of 2835
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_the_word_sort_splits_on_exactly_the_whitespace_the_scorer_splits_on`

Old text:

```
    if token and max(token) > "\xff":
```

New text:

```
    if token and max(token) >= "\xff":
```

### `u265.M3_words_not_sorted`

_sorted_words: join the words in their own order, so the pass scores plain ratio and an artist and title swap no longer matches

- File: `src/cratekit/acquire/match.py`
- Source: `u265.json`, row `M3_words_not_sorted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`
- Collected: 2835 against a baseline of 2835
- Kills: 18 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_file_whose_artist_and_title_are_the_rows_swapped_is_still_offered`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Lights Midnight-Midnight Lights]`
  - `tests/test_match_states.py::test_a_spelled_number_is_not_read_as_a_numeral[Four Tune-Fortune]`
  - `tests/test_match_states.py::test_a_swapped_listing_split_differently_is_still_offered[Aurora Bloom - Every Day-Everyday - Aurora Bloom]`
  - `tests/test_match_states.py::test_a_swapped_listing_split_differently_is_still_offered[Aurora Bloom - Goodbye-Good Bye - Aurora Bloom]`
  - `tests/test_match_states.py::test_a_swapped_listing_split_differently_is_still_offered[Aurora Bloom - OK-O.K. - Aurora Bloom]`
  - `tests/test_match_states.py::test_a_swapped_listing_split_differently_is_still_offered[M.I.A. - Paper Planes-Paper Planes - MIA]`
  - `tests/test_match_states.py::test_every_pair_scores_the_same_through_the_sorted_form`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[265-5]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[265-None]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[2650-5]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[2650-None]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[26500-5]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[26500-None]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - ... and 3 more, see the JSON sidecar

Old text:

```
    return " ".join(sorted(words))
```

New text:

```
    return " ".join(words)
```

### `u265.M4_query_not_sorted`

_approximate: score the wanted token unsorted against the sorted library names

- File: `src/cratekit/acquire/match.py`
- Source: `u265.json`, row `M4_query_not_sorted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`
- Collected: 2835 against a baseline of 2835
- Kills: 42 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_rewritten_between_two_jobs_is_read_again_and_the_second_job_matches_its_new_tags`
  - `tests/test_match_states.py::test_a_file_whose_artist_and_title_are_the_rows_swapped_is_still_offered`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[2-Tom]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[4-Fort]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[B-Bee]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Cos-Because]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Luv-Lover]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[N-Ant]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[U-Yo]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Wot-What]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Midnight Harbour Lights-Midnight Harbor Lights]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Midnight Harbour Lights-Midnight Harbour Light]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Midnight Harbour Lights-Midnight Harbour Lighte]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Midnight Harbour Lights-Midnight Lights]`
  - ... and 27 more, see the JSON sidecar

Old text:

```
        _sorted_words(wanted.recording),
        sorted_choices,
```

New text:

```
        wanted.recording,
        sorted_choices,
```

### `u265.M5_hit_named_by_its_sorted_form`

_approximate: look a hit up by its sorted string rather than its position, so any recording whose words were not already in order loses its files

- File: `src/cratekit/acquire/match.py`
- Source: `u265.json`, row `M5_hit_named_by_its_sorted_form`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`
- Collected: 2835 against a baseline of 2835
- Kills: 61 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_rewritten_between_two_jobs_is_read_again_and_the_second_job_matches_its_new_tags`
  - `tests/test_match_states.py::test_a_file_whose_artist_and_title_are_the_rows_swapped_is_still_offered`
  - `tests/test_match_states.py::test_a_former_identifier_is_carried_only_with_one_fit_and_its_title`
  - `tests/test_match_states.py::test_a_held_emoji_row_does_not_retire_another_emoji_rows_question`
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[2-Tom]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[4-Fort]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[B-Bee]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Cos-Because]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Luv-Lover]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[N-Ant]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[U-Yo]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Wot-What]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[DNA-D.N.A.]`
  - ... and 46 more, see the JSON sidecar

Old text:

```
        held for _sorted, _score, position in found for held in index.versions(recordings[position])
```

New text:

```
        held for _sorted, _score, position in found for held in index.versions(_sorted)
```

### `u265.M6_cache_misaligned`

sorted_recordings: build the sorted names in reverse, so a position the scorer returns names a different recording

- File: `src/cratekit/acquire/match.py`
- Source: `u265.json`, row `M6_cache_misaligned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`
- Collected: 2835 against a baseline of 2835
- Kills: 15 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_rewritten_between_two_jobs_is_read_again_and_the_second_job_matches_its_new_tags`
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[265-5]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[265-None]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[2650-5]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[2650-None]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[26500-5]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[26500-None]`
  - `tests/test_match_states.py::test_the_floor_is_pinned_from_both_sides_by_the_nearest_score_either_way`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`
  - `tests/test_match_states.py::test_the_offer_limit_keeps_the_best_scoring_answers_and_says_what_it_kept_back`

Old text:

```
            cached = (recordings, tuple(_sorted_words(token) for token in recordings))
```

New text:

```
            cached = (recordings, tuple(_sorted_words(token) for token in reversed(recordings)))
```

### `u265.M7_cache_never_kept`

sorted_recordings: never store the sorted names, so every wanted row sorts the whole library again (answers unchanged, cost back to per pair)

- File: `src/cratekit/acquire/match.py`
- Source: `u265.json`, row `M7_cache_never_kept`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`
- Collected: 2835 against a baseline of 2835
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_each_name_is_sorted_once_for_the_index_and_each_row_once_a_call`

Old text:

```
            object.__setattr__(self, "_sorted", cached)
```

New text:

```
            pass
```

### `u265.M8_other_scorer`

_approximate: score the sorted forms with WRatio instead of ratio, so scores and the floor's cut move

- File: `src/cratekit/acquire/match.py`
- Source: `u265.json`, row `M8_other_scorer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`
- Collected: 2835 against a baseline of 2835
- Kills: 39 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_rerun_after_acquiring_reports_the_heart_owned_with_no_cursor`
  - `tests/intake/test_workers.py::test_each_resolution_count_is_followed_by_its_reasons`
  - `tests/intake/test_workers.py::test_favorites_resolves_each_heart_owned_offered_or_missing`
  - `tests/intake/test_workers.py::test_the_missing_hearts_carry_the_provider_id_acquisition_reads`
  - `tests/intake/test_workers.py::test_the_reasons_are_read_back_from_the_reports_on_every_resume`
  - `tests/intake/test_workers.py::test_the_resolution_names_owned_offered_and_missing_and_the_next_command`
  - `tests/test_intake_missing.py::test_a_mixed_job_writes_only_the_missing_rows`
  - `tests/test_intake_missing.py::test_a_rejected_row_under_a_tombstone_is_suppressed_not_listed`
  - `tests/test_intake_missing.py::test_a_rejection_after_a_listing_refuses_over_the_earlier_list_and_says_why`
  - `tests/test_intake_missing.py::test_a_row_held_in_another_version_since_is_offered_not_listed`
  - `tests/test_intake_missing.py::test_a_row_tombstoned_since_the_job_is_not_listed_and_counted_suppressed`
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_a_second_run_is_the_same_list_and_not_a_refusal`
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_a_shorter_rerun_over_the_jobs_earlier_list_refuses_and_says_why`
  - ... and 24 more, see the JSON sidecar

Old text:

```
        scorer=fuzz.ratio,
```

New text:

```
        scorer=fuzz.WRatio,
```

### `u206-b.M10b_day_coefficient_halved`

DAY_S halved, measured again once the tests write a day out as 86 400 seconds

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206-b.json`, row `M10b_day_coefficient_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 3 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_found_answer_is_asked_again_after_the_configured_days`
  - `tests/test_isrc_cache.py::test_a_found_answer_lives_thirty_days_unless_set`
  - `tests/test_isrc_cache.py::test_a_not_found_is_kept_and_asked_again_after_seven_days`

Old text:

```
DAY_S = 86_400
```

New text:

```
DAY_S = 43_200
```

### `u206-b.M2b_disabled_recall_composite`

Composite: drop recall's days 0 guard AND give every entry at least a day's life, so answers kept before the cache was turned off still answer

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206-b.json`, row `M2b_disabled_recall_composite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 8 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_answers_kept_before_the_cache_was_turned_off_answer_nothing`
  - `tests/test_isrc_cache.py::test_zero_days_asks_every_time_and_writes_nothing`
  - `tests/test_outbound_tidal_account.py::test_a_lone_release_a_lone_heart_or_a_lone_album_is_never_a_broken_tie`
  - `tests/test_outbound_tidal_account.py::test_a_release_that_does_not_agree_is_never_taken`
  - `tests/test_outbound_tidal_account.py::test_a_tie_with_any_agreeing_takes_the_lowest_identifier_whatever_the_listing_order`
  - `tests/test_outbound_tidal_account.py::test_a_title_that_reads_two_ways_agrees_under_either_and_still_needs_one`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_or_an_album_naming_two_is_a_broken_tie`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[cache-off]`

Old text:

```
        global _PROCESS_HITS
        if not self.enabled:
            return None
```

New text:

```
        global _PROCESS_HITS
        self.days = max(self.days, 1)
```

### `u206.M11_unreadable_answer_kept`

Cache.remember: keep an answer holding a track that cannot be read

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M11_unreadable_answer_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 4 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_an_answer_holding_a_track_that_cannot_be_read_is_asked_again[no-artist]`
  - `tests/test_isrc_cache.py::test_an_answer_holding_a_track_that_cannot_be_read_is_asked_again[no-identifier]`
  - `tests/test_isrc_cache.py::test_an_answer_holding_a_track_that_cannot_be_read_is_asked_again[no-title]`
  - `tests/test_organize_mirror_tie.py::test_a_tie_beside_a_release_that_cannot_be_read_is_left_out_and_asked_again`

Old text:

```
        if not all(_readable(track) for track in tracks):
            return False
```

New text:

```
        if False:
            return False
```

### `u206.M12_corrupt_file_not_set_aside`

Cache._entries: a file that does not parse is read as empty and overwritten, never set aside

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M12_corrupt_file_not_set_aside`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 3 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_corrupt_file_is_set_aside_and_the_lookup_succeeds`
  - `tests/test_isrc_cache.py::test_a_file_of_another_shape_is_set_aside_too`
  - `tests/test_isrc_cache.py::test_doctor_names_a_set_aside_file_and_never_fails`

Old text:

```
        if entries is None:
            if locked:
                self._set_aside_held()
            else:
                self._set_aside()
            return {}
```

New text:

```
        if entries is None:
            return {}
```

### `u206.M13_write_without_merge`

Cache.remember: write only this entry, dropping what another process wrote since

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M13_write_without_merge`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_a_second_run_over_the_same_set_asks_the_provider_no_isrc_again`
  - `tests/test_isrc_cache.py::test_a_different_country_is_a_different_key`
  - `tests/test_isrc_cache.py::test_another_processs_answer_written_since_this_one_read_survives`
  - `tests/test_isrc_cache.py::test_two_writer_processes_leave_one_readable_file_holding_both`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[kept]`

Old text:

```
            merged = {
                name: entry for name, entry in entries.items() if self._fresh(entry, now) is not None
            }
```

New text:

```
            merged = {}
```

### `u206.M16_said_not_found_widened`

said_not_found: read InvalidISRC as a said not found too

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M16_said_not_found_widened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 3 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_an_invalid_isrc_the_account_reads_as_no_match_is_never_kept`
  - `tests/test_isrc_cache.py::test_an_outage_then_an_invalid_isrc_on_the_retry_keeps_nothing`
  - `tests/test_isrc_cache.py::test_said_not_found_is_the_clients_own_class_or_a_404_and_nothing_else[invalid-isrc]`

Old text:

```
    if type(exc).__name__ == "ObjectNotFound":
```

New text:

```
    if type(exc).__name__ in ("ObjectNotFound", "InvalidISRC"):
```

### `u206.M1_recall_never_hits`

Cache.recall: never answer from the file, so every lookup asks the provider again

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M1_recall_never_hits`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 19 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_a_second_run_over_the_same_set_asks_the_provider_no_isrc_again`
  - `tests/test_isrc_cache.py::test_a_404_status_is_kept_as_a_not_found_at_either_seam[account]`
  - `tests/test_isrc_cache.py::test_a_404_status_is_kept_as_a_not_found_at_either_seam[catalogue]`
  - `tests/test_isrc_cache.py::test_a_choice_among_several_releases_is_made_from_a_remembered_answer_with_no_call`
  - `tests/test_isrc_cache.py::test_a_copy_run_redirecting_installation_state_shares_answers_through_the_override`
  - `tests/test_isrc_cache.py::test_a_found_answer_is_asked_again_after_the_configured_days`
  - `tests/test_isrc_cache.py::test_a_found_answer_lives_thirty_days_unless_set`
  - `tests/test_isrc_cache.py::test_a_not_found_is_kept_and_asked_again_after_seven_days`
  - `tests/test_isrc_cache.py::test_a_remembered_client_track_reads_as_the_client_track_does[streamable]`
  - `tests/test_isrc_cache.py::test_a_remembered_client_track_reads_as_the_client_track_does[withdrawn]`
  - `tests/test_isrc_cache.py::test_a_second_account_over_a_fresh_client_asks_nothing_for_an_answered_isrc`
  - `tests/test_isrc_cache.py::test_a_tie_remembered_is_still_refused_with_its_reason`
  - `tests/test_isrc_cache.py::test_an_expired_answer_is_replaced_by_the_new_one`
  - `tests/test_isrc_cache.py::test_an_outage_then_a_not_found_on_the_retry_keeps_the_not_found`
  - `tests/test_isrc_cache.py::test_the_catalogue_and_the_account_share_one_answer`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        held = self._fresh(entries.get(key), self.clock())
```

New text:

```
        held = None
```

### `u206.M21_override_ignored`

_resolved: ignore CRATEKIT_ISRC_CACHE_DIR, so a hand copy run cannot share the live answers

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M21_override_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_rehearsal_keeps_the_live_isrc_cache_and_restores_the_environment`

Old text:

```
    if override:
        return Path(override) / config.state_file(key).relative
```

New text:

```
    if False:
        return Path(override) / config.state_file(key).relative
```

### `u206.M3_disabled_still_remembers`

Cache.remember: drop the days 0 guard, so a cache turned off still writes the file

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M3_disabled_still_remembers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_zero_days_asks_every_time_and_writes_nothing`

Old text:

```
        if not self.enabled:
            return False
        key = _key(isrc, country)
        if key is None:
            return False
        tracks = list(tracks)
```

New text:

```
        key = _key(isrc, country)
        if key is None:
            return False
        tracks = list(tracks)
```

### `u206.M4_unfolded_spelling_kept`

_key: keep a spelling that is not its own fold under the folded key

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M4_unfolded_spelling_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_spelling_that_is_not_its_own_fold_is_asked_and_never_kept`

Old text:

```
    if not folded or folded != isrc:
```

New text:

```
    if not folded:
```

### `u206.M5_country_ignored`

_key: leave the country out, so an answer in one country answers another

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M5_country_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 5 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_404_status_is_kept_as_a_not_found_at_either_seam[account]`
  - `tests/test_isrc_cache.py::test_a_404_status_is_kept_as_a_not_found_at_either_seam[catalogue]`
  - `tests/test_isrc_cache.py::test_a_corrupt_file_is_set_aside_and_the_lookup_succeeds`
  - `tests/test_isrc_cache.py::test_a_different_country_is_a_different_key`
  - `tests/test_isrc_cache.py::test_another_processs_answer_written_since_this_one_read_survives`

Old text:

```
    return f"{folded}|{country}"
```

New text:

```
    return f"{folded}|"
```

### `u206.M6_not_found_lives_as_found`

_fresh: a not found lives as long as a found answer

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M6_not_found_lives_as_found`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_not_found_is_kept_and_asked_again_after_seven_days`

Old text:

```
        days = self.days if tracks else min(NOT_FOUND_DAYS, self.days)
```

New text:

```
        days = self.days
```

### `u206.M7_not_found_ignores_shorter_setting`

_fresh: a not found lives a week even when the setting is shorter

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M7_not_found_ignores_shorter_setting`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_not_found_lives_no_longer_than_a_shorter_setting`

Old text:

```
        days = self.days if tracks else min(NOT_FOUND_DAYS, self.days)
```

New text:

```
        days = self.days if tracks else NOT_FOUND_DAYS
```

### `u206.M8_expiry_off_by_one`

_fresh: an entry exactly its lifetime old is still used

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M8_expiry_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 5 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_found_answer_is_asked_again_after_the_configured_days`
  - `tests/test_isrc_cache.py::test_a_found_answer_lives_thirty_days_unless_set`
  - `tests/test_isrc_cache.py::test_a_not_found_is_kept_and_asked_again_after_seven_days`
  - `tests/test_isrc_cache.py::test_a_not_found_lives_no_longer_than_a_shorter_setting`
  - `tests/test_isrc_cache.py::test_an_expired_answer_is_replaced_by_the_new_one`

Old text:

```
        if age < 0 or age >= days * DAY_S:
```

New text:

```
        if age < 0 or age > days * DAY_S:
```

### `u206.M9_future_stamp_trusted`

_fresh: an entry stamped later than now is used

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M9_future_stamp_trusted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_an_answer_stamped_later_than_now_is_asked_again`

Old text:

```
        if age < 0 or age >= days * DAY_S:
```

New text:

```
        if age >= days * DAY_S:
```

### `u206.M18_catalogue_keeps_any_gone`

TidalCatalogue.tracks_for_isrc: keep every failure _gone reads as a not found, a FileNotFoundError among them

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u206.json`, row `M18_catalogue_keeps_any_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 2 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_the_catalogue_answers_a_class_named_not_found_as_before_and_keeps_nothing[file]`
  - `tests/test_isrc_cache.py::test_the_catalogue_answers_a_class_named_not_found_as_before_and_keeps_nothing[module]`

Old text:

```
                    if isrc_cache.said_not_found(exc):
                        answered.append(())
```

New text:

```
                    if True:
                        answered.append(())
```

### `u206.M14_account_keeps_invalid_isrc`

TidalAccount._isrc_tracks: keep any no match as a not found, InvalidISRC included

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u206.json`, row `M14_account_keeps_invalid_isrc`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 2 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_an_invalid_isrc_the_account_reads_as_no_match_is_never_kept`
  - `tests/test_isrc_cache.py::test_an_outage_then_an_invalid_isrc_on_the_retry_keeps_nothing`

Old text:

```
            if last["said_not_found"]:
                self._cache.remember(wanted, country, ())
```

New text:

```
            if True:
                self._cache.remember(wanted, country, ())
```

### `u206.M17_account_hit_ignored`

TidalAccount._isrc_tracks: never use a remembered answer

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u206.json`, row `M17_account_hit_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 13 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_404_status_is_kept_as_a_not_found_at_either_seam[account]`
  - `tests/test_isrc_cache.py::test_a_choice_among_several_releases_is_made_from_a_remembered_answer_with_no_call`
  - `tests/test_isrc_cache.py::test_a_copy_run_redirecting_installation_state_shares_answers_through_the_override`
  - `tests/test_isrc_cache.py::test_a_found_answer_is_asked_again_after_the_configured_days`
  - `tests/test_isrc_cache.py::test_a_found_answer_lives_thirty_days_unless_set`
  - `tests/test_isrc_cache.py::test_a_not_found_is_kept_and_asked_again_after_seven_days`
  - `tests/test_isrc_cache.py::test_a_second_account_over_a_fresh_client_asks_nothing_for_an_answered_isrc`
  - `tests/test_isrc_cache.py::test_a_tie_remembered_is_still_refused_with_its_reason`
  - `tests/test_isrc_cache.py::test_an_expired_answer_is_replaced_by_the_new_one`
  - `tests/test_isrc_cache.py::test_an_outage_then_a_not_found_on_the_retry_keeps_the_not_found`
  - `tests/test_isrc_cache.py::test_the_catalogue_and_the_account_share_one_answer`
  - `tests/test_isrc_cache.py::test_the_process_counts_say_what_the_cache_settled_and_what_was_asked`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[kept]`

Old text:

```
        if held is not None:
            return held if held else _ABSENT
        # What the LAST attempt said
```

New text:

```
        if False:
            return held if held else _ABSENT
        # What the LAST attempt said
```

### `u206.M22_days_validation_dropped`

_validate_provider: accept a negative isrc_cache_days

- File: `src/cratekit/core/config.py`
- Source: `u206.json`, row `M22_days_validation_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_days_value_that_is_not_a_whole_number_of_days_is_refused[-1]`

Old text:

```
    if days is not None and (not isinstance(days, int) or isinstance(days, bool) or days < 0):
```

New text:

```
    if days is not None and (not isinstance(days, int) or isinstance(days, bool)):
```

### `r1394.A1_recorder_never_told`

adapter order: the recorder begun answers is never told before a move, so the record keeps sent and landed at 0 while moves land

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1394.json`, row `A1_recorder_never_told`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1311 against a baseline of 1311
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_move_spent_on_its_412s_is_told_as_not_landed`
  - `tests/test_outbound_order.py::test_a_move_that_failed_another_way_is_left_as_maybe_landed`
  - `tests/test_outbound_order.py::test_a_recorder_that_cannot_record_has_no_further_move_sent`
  - `tests/test_outbound_order.py::test_a_stop_in_the_pause_after_a_412_is_recorded_as_no_move_in_flight`
  - `tests/test_outbound_order.py::test_the_caller_is_told_before_each_move_how_many_may_have_landed`

Old text:

```
                if told is not None:
                    told(number, number - 1)
```

New text:

```
                if False:
                    told(number, number - 1)
```

### `r1394.A2_sent_one_short`

adapter order: the recorder is told one move fewer sent than is about to go, so a move in flight is read as known not to have landed

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1394.json`, row `A2_sent_one_short`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1311 against a baseline of 1311
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_move_spent_on_its_412s_is_told_as_not_landed`
  - `tests/test_outbound_order.py::test_a_move_that_failed_another_way_is_left_as_maybe_landed`
  - `tests/test_outbound_order.py::test_a_recorder_that_cannot_record_has_no_further_move_sent`
  - `tests/test_outbound_order.py::test_a_stop_in_the_pause_after_a_412_is_recorded_as_no_move_in_flight`
  - `tests/test_outbound_order.py::test_the_caller_is_told_before_each_move_how_many_may_have_landed`

Old text:

```
                    told(number, number - 1)
```

New text:

```
                    told(number - 1, number - 1)
```

### `r1394.A3_landed_overstated`

adapter order: the recorder is told the move about to go has already landed

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1394.json`, row `A3_landed_overstated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1311 against a baseline of 1311
- Kills: 4 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_move_spent_on_its_412s_is_told_as_not_landed`
  - `tests/test_outbound_order.py::test_a_move_that_failed_another_way_is_left_as_maybe_landed`
  - `tests/test_outbound_order.py::test_a_stop_in_the_pause_after_a_412_is_recorded_as_no_move_in_flight`
  - `tests/test_outbound_order.py::test_the_caller_is_told_before_each_move_how_many_may_have_landed`

Old text:

```
                    told(number, number - 1)
```

New text:

```
                    told(number, number)
```

### `r1394.A4_412_not_brought_down`

adapter order: a move spent on its 412s is left as maybe landed, its sent count never brought back down

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1394.json`, row `A4_412_not_brought_down`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1311 against a baseline of 1311
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_move_spent_on_its_412s_is_told_as_not_landed`
  - `tests/test_outbound_order.py::test_a_stop_in_the_pause_after_a_412_is_recorded_as_no_move_in_flight`

Old text:

```
                        told(number - 1, number - 1)
```

New text:

```
                        pass
```

### `r1394.A5_any_failure_brought_down`

adapter order: a move that failed any way, a dropped connection included, is told as not landed

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1394.json`, row `A5_any_failure_brought_down`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1311 against a baseline of 1311
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_move_spent_on_its_412s_is_told_as_not_landed`
  - `tests/test_outbound_order.py::test_a_move_that_failed_another_way_is_left_as_maybe_landed`
  - `tests/test_outbound_order.py::test_a_stop_in_the_pause_after_a_412_is_recorded_as_no_move_in_flight`

Old text:

```
                    if not _stale_tag(exc):
                        raise
                    if told is not None:
```

New text:

```
                    if told is not None:
                        told(number - 1, number - 1)
                    if not _stale_tag(exc):
                        raise
                    if told is not None:
```

### `r1411.A1_agreed_order_always_stands`

the agreed order check passes every reading, so a reading in the order from before the stopped moves is planned from

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `A1_agreed_order_always_stands`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1311 against a baseline of 1311
- Kills: 11 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_agreed_order_after_an_add_refuses_with_nothing_moved`
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_agreed_order_once_is_read_again_and_takes_the_order`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading1-agreed1-False]`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading5-agreed5-False]`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading7-agreed7-False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_planned_again_in_the_writing_command_is_held_to_its_own_reading`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_removes_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`

Old text:

```
    return [one for one in dict.fromkeys(reading) if one in named] == [
        one for one in dict.fromkeys(str(one) for one in agreed) if one in held
    ]
```

New text:

```
    return bool(named or held or True)
```

### `r1411.A2_removed_tracks_asked_of_the_reading`

the agreed order check asks every agreed track of the reading, so a track this write took off refuses the finish

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `A2_removed_tracks_asked_of_the_reading`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1311 against a baseline of 1311
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_track_this_write_took_off_is_not_asked_of_the_reading`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading6-agreed6-True]`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading9-agreed9-True]`

Old text:

```
        one for one in dict.fromkeys(str(one) for one in agreed) if one in held
```

New text:

```
        one for one in dict.fromkeys(str(one) for one in agreed)
```

### `r1411.A3_added_tracks_asked_of_the_agreed_order`

the agreed order check reads every track of the reading, so a track this write added refuses the finish

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `A3_added_tracks_asked_of_the_agreed_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1311 against a baseline of 1311
- Kills: 7 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_agreed_order_once_is_read_again_and_takes_the_order`
  - `tests/test_outbound_order.py::test_an_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading10-agreed10-True]`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading2-agreed2-True]`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading3-agreed3-True]`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading4-agreed4-True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_added_track_the_provider_placed_elsewhere_is_not_refused`

Old text:

```
    return [one for one in dict.fromkeys(reading) if one in named] == [
```

New text:

```
    return [one for one in dict.fromkeys(reading)] == [
```

### `r1411.A5_duplicates_counted_twice`

the agreed order check reads a track the reading holds twice at both places

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `A5_duplicates_counted_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1311 against a baseline of 1311
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading8-agreed8-True]`

Old text:

```
    return [one for one in dict.fromkeys(reading) if one in named] == [
```

New text:

```
    return [one for one in reading if one in named] == [
```

### `r1411.E1_expect_compared_as_membership`

existing guard, U220: an expected reading is compared by the tracks it holds, not their order

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `E1_expect_compared_as_membership`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1311 against a baseline of 1311
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_reading_that_never_agrees_with_the_expected_one_refuses_with_nothing_moved`

Old text:

```
                return list(dict.fromkeys(reading)) == list(dict.fromkeys(known))
```

New text:

```
                return sorted(dict.fromkeys(reading)) == sorted(dict.fromkeys(known))
```

### `r1411.E4_membership_always_agrees`

existing guard, U220: a reading after this command's own writes is taken whatever it holds

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `E4_membership_always_agrees`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1311 against a baseline of 1311
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_the_agreed_order_does_not_stand_in_for_what_the_write_left`
  - `tests/test_outbound_remove_lag.py::test_a_pairs_removal_add_and_order_all_land_over_a_read_that_lags_each_write[whole]`

Old text:

```
            return sorted(reading) == sorted(known)
```

New text:

```
            return bool(reading) or True
```

### `r1411.S1_settled_ignores_agreed`

the judged reading never asks the agreed order, so only what it holds is checked

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `S1_settled_ignores_agreed`
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
            if agreed is not None and not _in_agreed_order(reading, agreed):
                return False
```

New text:

```
            if False:
                return False
```

### `r1411.S2_agreed_stands_in_for_membership`

a reading in the agreed order is taken without the check of what it holds

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `S2_agreed_stands_in_for_membership`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1311 against a baseline of 1311
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_the_agreed_order_does_not_stand_in_for_what_the_write_left`

Old text:

```
            if agreed is not None and not _in_agreed_order(reading, agreed):
                return False
```

New text:

```
            if agreed is not None:
                return _in_agreed_order(reading, agreed)
```

