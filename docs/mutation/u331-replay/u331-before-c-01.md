# Mutation table: u331-before-c-01

Measured by `scripts/mutate.py` on 2026-11-24 00:03 UTC, branch `HEAD` at `9a043b2a`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22808 collected. pytest invocations for this batch: 75.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 00:03 UTC for commit `9a043b2ac018`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 9, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22808 against 22808. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u12-independent-round-6.C2_reserve_halved` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 2 | killed |
| `u12-independent-round-6.C4_darwin_headroom` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 4 | killed |
| `u12-independent-round-6.C5_swap_threshold` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 4 | killed |
| `u12-independent-round-6.C6_used_percent_ceiling` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 2 | killed |
| `u12-independent-round-6.C7_max_tasks_per_child` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 3 | killed |
| `u12-independent-round-6.C8_probe_deadline` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.C9_reap_budget` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.G1_dotdot_not_refused` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.G2_containment_dropped` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 2 | killed |
| `u12-independent-round-6.G3_headroom_can_go_negative` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.G4_controller_substring_match` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 2 | killed |
| `u12-independent-round-6.G5_loosest_cap_wins` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.G6_cgroup_cap_ignored` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 3 | killed |
| `u12-independent-round-6.G7_valueerror_escapes_the_reader` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.M1_measurement_below_the_floor` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.M2_nonsense_measurement_accepted` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 2 | killed |
| `u12-independent-round-6.M3_zero_deadline_allowed` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.M4_model_freed_before_the_reading` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.M5_terminate_rung_removed` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 3 | killed |
| `u12-independent-round-6.M6_kill_rung_removed` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.M7_parent_keeps_the_write_end` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.M8_no_reap_after_the_probe` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.P10_recycle_reported_for_in_process` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 2 | killed |
| `u12-independent-round-6.P12_unreadable_falls_back_to_ceiling` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 8 | killed |
| `u12-independent-round-6.P1_reserve_not_applied` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 14 | killed |
| `u12-independent-round-6.P2_order_reversed` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 6 | killed |
| `u12-independent-round-6.P3_budget_can_go_negative` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 2 | killed |
| `u12-independent-round-6.P4_no_floor_of_one_worker` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 11 | killed |
| `u12-independent-round-6.P5_tie_goes_to_the_ceiling` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.P6_no_insufficient_memory_bound` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 5 | killed |
| `u12-independent-round-6.R1_available_type_check` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 5 | killed |
| `u12-independent-round-6.R2_available_never_raises` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 2 | killed |
| `u12-independent-round-6.R3_pressure_percent_range` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.R4_pressure_type_check` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 2 | killed |
| `u12-independent-round-6.X1_pool_of_one_built` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.X3_generation_boundary_removed` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.X4_initargs_not_refused` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.X5_in_process_path_removed` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.X7_generation_size_drops_the_width` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 9 | killed |
| `u241.M01_worker_takes_the_interrupt` | `src/cratekit/core/pool.py` | user | 1 file(s) | 26 | 1 | killed |
| `u241.M02_worker_outlives_its_parent` | `src/cratekit/core/pool.py` | user | 1 file(s) | 26 | 1 | killed |
| `u241.M03_close_waits_for_unread_work` | `src/cratekit/core/pool.py` | user | 1 file(s) | 26 | 1 | killed |
| `u241.M07_used_percent_gate_is_strict` | `src/cratekit/core/pool.py` | user | 2 file(s) | 295 | 3 | killed |
| `u241.M08_plan_forgets_which_gate` | `src/cratekit/core/pool.py` | user | 2 file(s) | 298 | 6 | killed |
| `u301.P1_initargs_refused_without_an_initializer` | `src/cratekit/core/pool.py` | user | 2 file(s) | 295 | 2 | killed |
| `u301.P2_initializer_held_to_the_rule` | `src/cratekit/core/pool.py` | user | 2 file(s) | 295 | 1 | killed |
| `r1372.K19_passed_by_strict` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 1 | killed |
| `r1372.K20_passed_by_any_pair` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 1 | killed |
| `r1372.K21_made_pair_unmapped` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 2 | killed |
| `r1376.F14_finished_filter_gone` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 1 | killed |
| `r1394.S10_later_unsent_write_hides_the_pending` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 3 | killed |
| `r1394.S1_counts_beyond_the_moves_trusted` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 1 | killed |
| `r1394.S2_missing_counts_read_as_none_sent` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 7 | killed |
| `r1394.S5_sent_read_as_landed` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 6 | killed |
| `r1394.S6_counts_not_wired` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 14 | killed |
| `r1394.S8_positions_first_only` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 2 | killed |
| `r1394.S9_moving_step_counts_dropped` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 19 | killed |
| `r1418.F7_composite_ordering_start_unread` | `src/cratekit/sync/pair_stopped.py` | user | 10 file(s) | 394 | 20 | killed |
| `r1434.S2_positions_compare_every_track_listed` | `src/cratekit/sync/pair_stopped.py` | user | 10 file(s) | 394 | 2 | killed |
| `u220.A3_keep_head` | `src/cratekit/sync/pair_stopped.py` | user | 6 file(s) | 283 | 26 | killed |
| `u220.A4_first_first` | `src/cratekit/sync/pair_stopped.py` | user | 6 file(s) | 283 | 14 | killed |
| `u225.M6_front_keeps_nothing` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 1 | killed |
| `u225.M8_reached_strict_membership` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 3 | killed |
| `u225.M9_finish_ignored` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 3 | killed |
| `u234.O15_reordered_counts_additions` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 1 | killed |

## Row definitions

### `u12-independent-round-6.C2_reserve_halved`

Halve the absolute memory reserve coefficient, two gibibytes to one. A reserve that can be halved with a green suite is a reserve nothing pins.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `C2_reserve_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 2 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_capped_service_on_a_huge_host_is_sized_by_the_service`
  - `tests/test_pool_sizing.py::test_the_absolute_reserve_is_two_gibibytes_of_the_reading_that_was_never_ours`

Old text:

```
DEFAULT_MEMORY_RESERVE_BYTES = 2 * 1024**3
```

New text:

```
DEFAULT_MEMORY_RESERVE_BYTES = 1 * 1024**3
```

### `u12-independent-round-6.C4_darwin_headroom`

Raise the darwin headroom share from half to three quarters, which is the value the measured inactive-queue split says is too optimistic.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `C4_darwin_headroom`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 4 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_each_headroom_share_is_pinned_by_the_pool_it_produces[darwin-half-as-measured]`
  - `tests/test_pool_sizing.py::test_the_headroom_share_is_lower_where_the_reading_is_measurably_worse[darwin-50]`
  - `tests/test_pool_sizing.py::test_the_headroom_share_is_lower_where_the_reading_is_measurably_worse[linux-75]`
  - `tests/test_pool_sizing.py::test_the_headroom_share_is_lower_where_the_reading_is_measurably_worse[win32-75]`

Old text:

```
DARWIN_HEADROOM_PERCENT = 50
```

New text:

```
DARWIN_HEADROOM_PERCENT = 75
```

### `u12-independent-round-6.C5_swap_threshold`

Raise the swap pressure threshold from one gibibyte to four, so the machine the documented kill happened on is no longer refused a pool.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `C5_swap_threshold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 4 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_gated_plan_still_reports_the_reading_it_was_gated_despite`
  - `tests/test_pool_sizing.py::test_the_machine_the_kill_happened_on_gets_no_pool_under_the_shipped_rule`
  - `tests/test_pool_sizing.py::test_the_pressure_gate_bites_at_its_two_lines_and_nowhere_else[swap-at-the-line]`
  - `tests/test_pool_sizing.py::test_the_swap_threshold_is_a_gibibyte_and_the_gibibyte_is_load_bearing[a-full-gibibyte]`

Old text:

```
DEFAULT_SWAP_PRESSURE_BYTES = 1 * 1024**3
```

New text:

```
DEFAULT_SWAP_PRESSURE_BYTES = 4 * 1024**3
```

### `u12-independent-round-6.C6_used_percent_ceiling`

Raise the used-percent ceiling from eighty five to ninety five.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `C6_used_percent_ceiling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 2 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_the_pressure_gate_bites_at_its_two_lines_and_nowhere_else[percent-at-the-line]`
  - `tests/test_pool_sizing.py::test_the_used_percent_ceiling_is_eighty_five_and_the_number_is_load_bearing[at-the-line]`

Old text:

```
DEFAULT_USED_PERCENT_CEILING = 85
```

New text:

```
DEFAULT_USED_PERCENT_CEILING = 95
```

### `u12-independent-round-6.C7_max_tasks_per_child`

Two and a half times the recycle budget, one hundred to two hundred fifty, so a child holds an allocator two and a half times longer before retiring.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `C7_max_tasks_per_child`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 3 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_recycling_is_on_by_default_for_any_pool_wider_than_one`
  - `tests/test_pool_sizing.py::test_the_recycle_budget_retires_a_child_occasionally_rather_than_constantly[a-ten-thousand-track-folder]`
  - `tests/test_pool_sizing.py::test_the_recycle_budget_retires_a_child_occasionally_rather_than_constantly[an-ordinary-folder]`

Old text:

```
DEFAULT_MAX_TASKS_PER_CHILD = 100
```

New text:

```
DEFAULT_MAX_TASKS_PER_CHILD = 250
```

### `u12-independent-round-6.C8_probe_deadline`

Cut the probe deadline from two minutes to forty five seconds, below the twice-the-reference floor the docstring claims the suite states.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `C8_probe_deadline`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_the_probe_deadline_the_module_ships_outlasts_the_load_it_waits_for`

Old text:

```
DEFAULT_PROBE_TIMEOUT_SECONDS = 120.0
```

New text:

```
DEFAULT_PROBE_TIMEOUT_SECONDS = 45.0
```

### `u12-independent-round-6.C9_reap_budget`

Halve the reaping budget, one second to half a second, which the round six docstring names as the value that makes the terminate rung a race.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `C9_reap_budget`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_the_reaping_budget_is_a_band_around_what_a_release_costs`

Old text:

```
_PROBE_REAP_SECONDS = 1.0
```

New text:

```
_PROBE_REAP_SECONDS = 0.5
```

### `u12-independent-round-6.G1_dotdot_not_refused`

Drop the refusal of a cgroup path containing dot dot, so a climbing path is rewritten into a real sibling cgroup and its tighter cap binds.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `G1_dotdot_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_climb_that_lands_on_a_real_cgroup_inside_the_mount_is_refused_too[a-climb-in-the-middle]`

Old text:

```
    if ".." in fields:
        candidates = [mount]
    else:

```

New text:

```
    if False:
        candidates = [mount]
    else:

```

### `u12-independent-round-6.G2_containment_dropped`

Stop checking that a resolved level is still inside the mount, so a symlink out of the mount is read as a level of this process's cgroup.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `G2_containment_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 2 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_component_that_symlinks_out_of_the_mount_is_not_read`
  - `tests/test_pool_sizing.py::test_a_limit_file_that_symlinks_out_of_the_mount_is_not_read`

Old text:

```
    if resolved is None or not resolved.is_relative_to(anchor):
        return None

```

New text:

```
    if resolved is None:
        return None

```

### `u12-independent-round-6.G3_headroom_can_go_negative`

Report a negative headroom for a cgroup already over its cap.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `G3_headroom_can_go_negative`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_cgroup_cap_reports_what_is_left_inside_it[over-the-cap-is-zero-never-negative]`

Old text:

```
    return max(0, limit - used)

```

New text:

```
    return limit - used

```

### `u12-independent-round-6.G4_controller_substring_match`

Match the memory controller by substring, so a controller named memoryfoo sends the walk to an unrelated cgroup.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `G4_controller_substring_match`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 2 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_controller_field_that_merely_contains_the_word_memory_is_not_it[a-name-that-contains-it]`
  - `tests/test_pool_sizing.py::test_a_controller_field_that_merely_contains_the_word_memory_is_not_it[a-name-that-starts-with-it]`

Old text:

```
        elif "memory" in controllers.split(","):

```

New text:

```
        elif "memory" in controllers:

```

### `u12-independent-round-6.G5_loosest_cap_wins`

Take the loosest cap on the chain rather than the tightest, so a generous unit inside a tight slice reports the unit's number.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `G5_loosest_cap_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_the_tightest_cap_on_the_chain_is_the_one_that_binds`

Old text:

```
    return min(found) if found else None

```

New text:

```
    return max(found) if found else None

```

### `u12-independent-round-6.G6_cgroup_cap_ignored`

Ignore the cgroup cap entirely and return the host reading, which is the defect that sizes a container by its host.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `G6_cgroup_cap_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 3 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_capped_service_on_a_huge_host_is_sized_by_the_service`
  - `tests/test_pool_sizing.py::test_a_container_capped_below_its_host_is_sized_by_the_cap`
  - `tests/test_pool_sizing.py::test_a_large_container_on_a_larger_host_is_still_sized_by_the_container`

Old text:

```
    return reading if capped is None else min(reading, capped)

```

New text:

```
    return reading

```

### `u12-independent-round-6.G7_valueerror_escapes_the_reader`

Narrow the kernel-file reader back to OSError, so undecodable bytes and an embedded null byte raise out of a function that promises a number.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `G7_valueerror_escapes_the_reader`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_kernel_file_that_is_not_readable_as_text_is_an_absent_reading[not-text-at-all]`

Old text:

```
    except (OSError, ValueError):
        return None

```

New text:

```
    except OSError:
        return None

```

### `u12-independent-round-6.M1_measurement_below_the_floor`

Return the measurement even when it is below the declared floor, so the floor becomes a fallback rather than a floor.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `M1_measurement_below_the_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_the_probe_reports_its_measure_and_never_below_the_floor[never-below-the-floor]`

Old text:

```
    return max(measured, floor_bytes)

```

New text:

```
    return measured

```

### `u12-independent-round-6.M2_nonsense_measurement_accepted`

Accept a boolean, a float or a zero from the probe as a byte count.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `M2_nonsense_measurement_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 2 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_probe_that_answers_with_nonsense_returns_the_floor[none]`
  - `tests/test_pool_sizing.py::test_a_probe_that_answers_with_nonsense_returns_the_floor[text]`

Old text:

```
    if not isinstance(measured, int) or isinstance(measured, bool) or measured < 1:
        return floor_bytes

```

New text:

```
(empty)
```

### `u12-independent-round-6.M3_zero_deadline_allowed`

Allow a probe deadline of zero or less, which is a probe that can never answer reporting the floor as though it had measured.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `M3_zero_deadline_allowed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_probe_with_no_time_to_answer_refuses_rather_than_reporting_the_floor`

Old text:

```
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must leave the probe some time to answer")

```

New text:

```
(empty)
```

### `u12-independent-round-6.M4_model_freed_before_the_reading`

Free the loaded object before the resident set is read, the allocator retention defect the probe was rewritten to fix.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `M4_model_freed_before_the_reading`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_the_real_probe_measures_a_freshly_spawned_child`

Old text:

```
        model = loader()
        try:
            measured = resident_bytes()
        finally:

```

New text:

```
        loader()
        try:
            measured = resident_bytes()
        finally:

```

### `u12-independent-round-6.M5_terminate_rung_removed`

Remove the terminate rung alone, so every abandoned probe child meets an unconditional kill with no chance to unwind.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `M5_terminate_rung_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 3 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_probe_child_that_can_unwind_is_asked_to_before_it_is_killed`
  - `tests/test_pool_sizing.py::test_a_probe_child_that_refuses_to_unwind_meets_the_kill_backstop`
  - `tests/test_pool_sizing.py::test_the_release_the_fixture_declares_is_what_the_ladder_was_timed_paying`

Old text:

```
    if worker.is_alive():
        worker.terminate()
        worker.join(_PROBE_REAP_SECONDS)

```

New text:

```
(empty)
```

### `u12-independent-round-6.M6_kill_rung_removed`

Remove the kill backstop alone, so a child that ignores its terminate is left running and still allocating.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `M6_kill_rung_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_probe_child_that_refuses_to_unwind_meets_the_kill_backstop`

Old text:

```
    if worker.is_alive():
        worker.kill()
        worker.join(_PROBE_REAP_SECONDS)

```

New text:

```
(empty)
```

### `u12-independent-round-6.M7_parent_keeps_the_write_end`

Leave the parent's copy of the pipe write end open, so a child that dies without answering is indistinguishable from a slow one.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `M7_parent_keeps_the_write_end`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_probe_that_gets_no_answer_lands_on_the_floor_in_time[a-child-that-dies-without-answering]`

Old text:

```
    # exactly like a slow one until the timeout expired.
    writer.close()

```

New text:

```
    # exactly like a slow one until the timeout expired.

```

### `u12-independent-round-6.M8_no_reap_after_the_probe`

Remove the reap from the probe's finally, so an abandoned child keeps its allocation on a machine already declared tight.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `M8_no_reap_after_the_probe`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_probe_that_gave_up_leaves_no_child_still_allocating`

Old text:

```
        reader.close()
        _reap(worker)

```

New text:

```
        reader.close()

```

### `u12-independent-round-6.P10_recycle_reported_for_in_process`

Report a recycle count on a plan that runs in the calling process and has no child to retire.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `P10_recycle_reported_for_in_process`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 2 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_an_in_process_plan_runs_no_generations_at_all`
  - `tests/test_pool_sizing.py::test_two_gigabytes_against_a_one_gigabyte_worker_runs_in_process`

Old text:

```
        max_tasks_per_child=None if workers == 1 else max_tasks_per_child,

```

New text:

```
        max_tasks_per_child=max_tasks_per_child,

```

### `u12-independent-round-6.P12_unreadable_falls_back_to_ceiling`

Make the unreadable-memory fallback the declared ceiling rather than one worker, which is the exact fallback the brief forbids.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `P12_unreadable_falls_back_to_ceiling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 8 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_memory_read_failure_falls_back_to_one_worker_rather_than_raising`
  - `tests/test_pool_sizing.py::test_a_reading_that_is_not_a_byte_count_is_treated_as_unreadable[bool]`
  - `tests/test_pool_sizing.py::test_a_reading_that_is_not_a_byte_count_is_treated_as_unreadable[float]`
  - `tests/test_pool_sizing.py::test_a_reading_that_is_not_a_byte_count_is_treated_as_unreadable[negative]`
  - `tests/test_pool_sizing.py::test_a_reading_that_is_not_a_byte_count_is_treated_as_unreadable[none]`
  - `tests/test_pool_sizing.py::test_a_reading_that_is_not_a_byte_count_is_treated_as_unreadable[text]`
  - `tests/test_pool_sizing.py::test_a_reading_that_is_not_a_byte_count_is_treated_as_unreadable[very-negative]`
  - `tests/test_pool_sizing.py::test_the_fallback_is_never_the_ceiling_or_the_item_count`

Old text:

```
        return PoolPlan(
            workers=1,
            items=items,
            bound=Bound.MEMORY_UNREADABLE,

```

New text:

```
        return PoolPlan(
            workers=ceiling,
            items=items,
            bound=Bound.MEMORY_UNREADABLE,

```

### `u12-independent-round-6.P1_reserve_not_applied`

Drop the absolute reserve from the budget entirely, so the whole reading is claimable before the percent scales it.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `P1_reserve_not_applied`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 14 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_capped_service_on_a_huge_host_is_sized_by_the_service`
  - `tests/test_pool_sizing.py::test_a_machine_that_affords_exactly_one_worker_says_so`
  - `tests/test_pool_sizing.py::test_a_machine_that_affords_none_is_not_the_same_machine_and_does_not_say_it_is`
  - `tests/test_pool_sizing.py::test_a_measured_worker_size_flows_into_the_plan_it_was_taken_for`
  - `tests/test_pool_sizing.py::test_a_platform_with_no_limit_contributes_nothing_to_the_arithmetic`
  - `tests/test_pool_sizing.py::test_sixteen_gigabytes_is_bound_by_the_headroom_once_the_ceiling_is_raised`
  - `tests/test_pool_sizing.py::test_the_absolute_reserve_is_two_gibibytes_of_the_reading_that_was_never_ours`
  - `tests/test_pool_sizing.py::test_the_core_count_does_not_change_the_computed_cap`
  - `tests/test_pool_sizing.py::test_the_hard_ceiling_and_the_headroom_agree_at_the_point_they_cross`
  - `tests/test_pool_sizing.py::test_the_reserve_comes_off_the_reading_before_the_percent_scales_it`
  - `tests/test_pool_sizing.py::test_the_worker_count_flips_exactly_at_the_affordable_boundary[2]`
  - `tests/test_pool_sizing.py::test_the_worker_count_flips_exactly_at_the_affordable_boundary[3]`
  - `tests/test_pool_sizing.py::test_the_worker_count_flips_exactly_at_the_affordable_boundary[4]`
  - `tests/test_pool_sizing.py::test_two_gigabytes_against_a_one_gigabyte_worker_runs_in_process`

Old text:

```
    budget = max(0, available - reserve_bytes)

```

New text:

```
    budget = max(0, available)

```

### `u12-independent-round-6.P2_order_reversed`

Reverse the last two steps: divide into workers first and then scale the count, which the docstring says differs only at the boundaries.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `P2_order_reversed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 6 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_machine_that_affords_exactly_one_worker_says_so`
  - `tests/test_pool_sizing.py::test_a_machine_that_affords_none_is_not_the_same_machine_and_does_not_say_it_is`
  - `tests/test_pool_sizing.py::test_the_hard_ceiling_and_the_headroom_agree_at_the_point_they_cross`
  - `tests/test_pool_sizing.py::test_the_headroom_is_applied_to_the_bytes_before_they_are_divided_into_workers`
  - `tests/test_pool_sizing.py::test_the_worker_count_flips_exactly_at_the_affordable_boundary[2]`
  - `tests/test_pool_sizing.py::test_the_worker_count_flips_exactly_at_the_affordable_boundary[4]`

Old text:

```
    affordable = budget * headroom_percent // 100 // worker_bytes

```

New text:

```
    affordable = budget // worker_bytes * headroom_percent // 100

```

### `u12-independent-round-6.P3_budget_can_go_negative`

Remove the floor at zero so a reading smaller than the reserve produces a negative budget and a negative affordable count.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `P3_budget_can_go_negative`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 2 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_container_capped_below_its_host_is_sized_by_the_cap`
  - `tests/test_pool_sizing.py::test_a_reading_smaller_than_the_reserve_affords_nothing_rather_than_going_negative`

Old text:

```
    budget = max(0, available - reserve_bytes)

```

New text:

```
    budget = available - reserve_bytes

```

### `u12-independent-round-6.P4_no_floor_of_one_worker`

Remove the floor of one worker, so a machine that affords none plans a pool of zero.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `P4_no_floor_of_one_worker`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 11 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_container_capped_below_its_host_is_sized_by_the_cap`
  - `tests/test_pool_sizing.py::test_a_function_no_child_could_receive_is_refused_before_anything_runs`
  - `tests/test_pool_sizing.py::test_a_machine_that_affords_none_is_not_the_same_machine_and_does_not_say_it_is`
  - `tests/test_pool_sizing.py::test_a_plan_of_one_worker_explains_itself_as_in_process`
  - `tests/test_pool_sizing.py::test_a_plan_of_one_worker_runs_the_work_in_this_process`
  - `tests/test_pool_sizing.py::test_a_reading_smaller_than_the_reserve_affords_nothing_rather_than_going_negative`
  - `tests/test_pool_sizing.py::test_an_in_process_plan_refuses_to_hand_back_pool_arguments`
  - `tests/test_pool_sizing.py::test_an_in_process_plan_runs_no_generations_at_all`
  - `tests/test_pool_sizing.py::test_an_initializer_argument_no_child_could_receive_is_refused_on_the_same_terms`
  - `tests/test_pool_sizing.py::test_no_work_at_all_plans_one_in_process_worker_rather_than_zero`
  - `tests/test_pool_sizing.py::test_two_gigabytes_against_a_one_gigabyte_worker_runs_in_process`

Old text:

```
    workers = max(1, smallest)

```

New text:

```
    workers = smallest

```

### `u12-independent-round-6.P5_tie_goes_to_the_ceiling`

Put the ceiling ahead of available memory in the precedence list, so a tie is reported as the ceiling rather than as memory.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `P5_tie_goes_to_the_ceiling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_the_hard_ceiling_and_the_headroom_agree_at_the_point_they_cross`

Old text:

```
        (Bound.AVAILABLE_MEMORY, affordable),
        (Bound.CEILING, ceiling),

```

New text:

```
        (Bound.CEILING, ceiling),
        (Bound.AVAILABLE_MEMORY, affordable),

```

### `u12-independent-round-6.P6_no_insufficient_memory_bound`

Remove the reclassification that tells a machine affording exactly one from a machine affording none.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `P6_no_insufficient_memory_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 5 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_container_capped_below_its_host_is_sized_by_the_cap`
  - `tests/test_pool_sizing.py::test_a_machine_that_affords_none_is_not_the_same_machine_and_does_not_say_it_is`
  - `tests/test_pool_sizing.py::test_a_reading_smaller_than_the_reserve_affords_nothing_rather_than_going_negative`
  - `tests/test_pool_sizing.py::test_the_absolute_reserve_is_two_gibibytes_of_the_reading_that_was_never_ours`
  - `tests/test_pool_sizing.py::test_two_gigabytes_against_a_one_gigabyte_worker_runs_in_process`

Old text:

```
        bound = Bound.INSUFFICIENT_MEMORY

```

New text:

```
        bound = Bound.AVAILABLE_MEMORY

```

### `u12-independent-round-6.R1_available_type_check`

Accept a non-integer or negative available reading as a real reading.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `R1_available_type_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 5 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_reading_that_is_not_a_byte_count_is_treated_as_unreadable[bool]`
  - `tests/test_pool_sizing.py::test_a_reading_that_is_not_a_byte_count_is_treated_as_unreadable[float]`
  - `tests/test_pool_sizing.py::test_a_reading_that_is_not_a_byte_count_is_treated_as_unreadable[negative]`
  - `tests/test_pool_sizing.py::test_a_reading_that_is_not_a_byte_count_is_treated_as_unreadable[text]`
  - `tests/test_pool_sizing.py::test_a_reading_that_is_not_a_byte_count_is_treated_as_unreadable[very-negative]`

Old text:

```
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        return None
    return value

```

New text:

```
    return value

```

### `u12-independent-round-6.R2_available_never_raises`

Remove the catch around the injected available reader, so a reader that raises raises out of plan_pool.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `R2_available_never_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 2 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_memory_read_failure_falls_back_to_one_worker_rather_than_raising`
  - `tests/test_pool_sizing.py::test_the_fallback_is_never_the_ceiling_or_the_item_count`

Old text:

```
    try:
        value = reader()
    except Exception:
        return None
    if not isinstance(value, int)
```

New text:

```
    value = reader()
    if not isinstance(value, int)
```

### `u12-independent-round-6.R3_pressure_percent_range`

Accept a used-percent outside zero to one hundred as a real reading.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `R3_pressure_percent_range`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_an_unreadable_pressure_reading_does_not_collapse_the_pool[impossible-percent]`

Old text:

```
    if not 0 <= used <= 100:
        return None
    return value

```

New text:

```
    return value

```

### `u12-independent-round-6.R4_pressure_type_check`

Accept anything at all as a pressure reading, not only a Pressure.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `R4_pressure_type_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 2 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_an_unreadable_pressure_reading_does_not_collapse_the_pool[none]`
  - `tests/test_pool_sizing.py::test_an_unreadable_pressure_reading_does_not_collapse_the_pool[text]`

Old text:

```
    if not isinstance(value, Pressure):
        return None

```

New text:

```
(empty)
```

### `u12-independent-round-6.X1_pool_of_one_built`

Let executor_arguments build a pool for a plan of one worker instead of refusing at the seam.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `X1_pool_of_one_built`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_an_in_process_plan_refuses_to_hand_back_pool_arguments`

Old text:

```
    if plan.in_process:
        raise ValueError(
            "a plan of one worker runs in the calling process; there is no pool "
            "to build. Branch on plan.in_process before asking for a pool."
        )

```

New text:

```
(empty)
```

### `u12-independent-round-6.X3_generation_boundary_removed`

Give one executor all of the work rather than one generation of it, which is the deadlock the generation boundary exists to prevent.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `X3_generation_boundary_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_no_child_survives_a_generation_boundary_and_every_one_reloads_its_model`

Old text:

```
    generation = plan.tasks_per_generation or len(ordered) or 1

```

New text:

```
    generation = len(ordered) or 1

```

### `u12-independent-round-6.X4_initargs_not_refused`

Stop holding initializer arguments to the picklability rule, so the same call means two things on two machines again.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `X4_initargs_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_an_initializer_argument_no_child_could_receive_is_refused_on_the_same_terms`

Old text:

```
    for position, argument in enumerate(initargs):
        _refuse_what_no_child_could_receive(argument, f"initializer argument {position}")

```

New text:

```
(empty)
```

### `u12-independent-round-6.X5_in_process_path_removed`

Build a pool even for a plan of one worker, which is the brief's third requirement inverted.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `X5_in_process_path_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_plan_of_one_worker_runs_the_work_in_this_process`

Old text:

```
    if plan.in_process:
        if initializer is not None:
            initializer(*initargs)
        return [function(item) for item in ordered]

```

New text:

```
(empty)
```

### `u12-independent-round-6.X7_generation_size_drops_the_width`

Size a generation by one child's budget rather than by the whole set of children, so the executor is rebuilt workers times too often.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `X7_generation_size_drops_the_width`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 9 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_child_that_dies_mid_generation_ends_the_run_rather_than_hanging`
  - `tests/test_pool_sizing.py::test_a_plan_carries_the_item_count_it_was_decided_for`
  - `tests/test_pool_sizing.py::test_a_plan_says_how_many_generations_of_children_its_work_takes[16-2]`
  - `tests/test_pool_sizing.py::test_a_plan_says_how_many_generations_of_children_its_work_takes[17-3]`
  - `tests/test_pool_sizing.py::test_a_plan_says_how_many_generations_of_children_its_work_takes[8-1]`
  - `tests/test_pool_sizing.py::test_a_plan_says_how_many_generations_of_children_its_work_takes[9-2]`
  - `tests/test_pool_sizing.py::test_no_child_survives_a_generation_boundary_and_every_one_reloads_its_model`
  - `tests/test_pool_sizing.py::test_the_recycle_budget_retires_a_child_occasionally_rather_than_constantly[a-ten-thousand-track-folder]`
  - `tests/test_pool_sizing.py::test_the_recycle_budget_retires_a_child_occasionally_rather_than_constantly[an-ordinary-folder]`

Old text:

```
        return self.workers * self.max_tasks_per_child

```

New text:

```
        return self.max_tasks_per_child

```

### `u241.M01_worker_takes_the_interrupt`

stream worker: no longer ignore the terminal's interrupt, so Ctrl-C kills a worker mid item

- File: `src/cratekit/core/pool.py`
- Source: `u241.json`, row `M01_worker_takes_the_interrupt`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_stream.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_stream.py::test_the_terminals_interrupt_does_not_kill_a_stream_worker`

Old text:

```
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    _leave_when_the_parent_does()

```

New text:

```
    _leave_when_the_parent_does()

```

### `u241.M02_worker_outlives_its_parent`

stream worker: do not watch the parent, so a killed driver leaves its workers holding their memory

- File: `src/cratekit/core/pool.py`
- Source: `u241.json`, row `M02_worker_outlives_its_parent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_stream.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_stream.py::test_workers_leave_when_their_parent_is_killed_outright`

Old text:

```
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    _leave_when_the_parent_does()

```

New text:

```
    signal.signal(signal.SIGINT, signal.SIG_IGN)

```

### `u241.M03_close_waits_for_unread_work`

WorkStream._stop: do not end the workers, so a close waits for every item nobody will read

- File: `src/cratekit/core/pool.py`
- Source: `u241.json`, row `M03_close_waits_for_unread_work`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_stream.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_stream.py::test_a_close_ends_the_workers_without_waiting_for_work_nobody_will_read`

Old text:

```
        _end_workers(executor)
        executor.shutdown(wait=True, cancel_futures=True)

```

New text:

```
        executor.shutdown(wait=True, cancel_futures=True)

```

### `u241.M07_used_percent_gate_is_strict`

_gates_refusing: the used percent gate refuses only above its limit, not at it

- File: `src/cratekit/core/pool.py`
- Source: `u241.json`, row `M07_used_percent_gate_is_strict`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_stream.py`, `tests/test_pool_sizing.py`
- Collected: 295 against a baseline of 295
- Kills: 3 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_the_pressure_gate_bites_at_its_two_lines_and_nowhere_else[percent-at-the-line]`
  - `tests/test_pool_sizing.py::test_the_used_percent_ceiling_is_eighty_five_and_the_number_is_load_bearing[at-the-line]`
  - `tests/test_pool_stream.py::test_a_plan_refused_by_both_gates_names_both_swap_first`

Old text:

```
    if pressure.used_percent >= used_percent_ceiling:
        refused.append(

```

New text:

```
    if pressure.used_percent > used_percent_ceiling:
        refused.append(

```

### `u241.M08_plan_forgets_which_gate`

plan_pool: a plan refused by pressure no longer carries which gate refused it

- File: `src/cratekit/core/pool.py`
- Source: `u241.json`, row `M08_plan_forgets_which_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_stream.py`, `tests/test_analysis_ahead.py`
- Collected: 298 against a baseline of 298
- Kills: 6 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_machine_deep_in_swap_runs_one_worker_and_names_the_swap_gate`
  - `tests/test_analysis_ahead.py::test_a_machine_using_most_of_its_memory_names_the_used_percent_gate`
  - `tests/test_analysis_ahead.py::test_a_run_that_fails_part_way_says_its_pool_on_the_refusal_and_matches_the_serial_run`
  - `tests/test_pool_stream.py::test_a_plan_refused_by_both_gates_names_both_swap_first`
  - `tests/test_pool_stream.py::test_a_plan_refused_by_swap_names_the_gate_the_reading_and_the_limit`
  - `tests/test_pool_stream.py::test_a_plan_refused_by_the_used_percent_names_that_gate`

Old text:

```
            ceiling=ceiling,
            refused_by=refused,

```

New text:

```
            ceiling=ceiling,

```

### `u301.P1_initargs_refused_without_an_initializer`

_refuse_unsendable: check the initializer's arguments only when there is an initializer, so map_workers and WorkStream pass a lambda argument on an in process plan

- File: `src/cratekit/core/pool.py`
- Source: `u301.json`, row `P1_initargs_refused_without_an_initializer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`, `tests/test_pool_stream.py`
- Collected: 295 against a baseline of 295
- Kills: 2 (killed)
- Killed:
  - `tests/test_pool_stream.py::test_an_unsendable_function_is_refused_at_construction_on_both_paths[in-process]`
  - `tests/test_pool_stream.py::test_an_unsendable_function_is_refused_at_construction_on_both_paths[pooled]`

Old text:

```
    for position, argument in enumerate(initargs):
        _refuse_what_no_child_could_receive(argument, f"initializer argument {position}")

```

New text:

```
    for position, argument in enumerate(initargs if initializer is not None else ()):
        _refuse_what_no_child_could_receive(argument, f"initializer argument {position}")

```

### `u301.P2_initializer_held_to_the_rule`

_refuse_unsendable: never check the initializer, so an unpicklable one passes an in process plan and fails a pooled one

- File: `src/cratekit/core/pool.py`
- Source: `u301.json`, row `P2_initializer_held_to_the_rule`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`, `tests/test_pool_stream.py`
- Collected: 295 against a baseline of 295
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_an_initializer_no_child_could_receive_is_refused_on_the_same_terms`

Old text:

```
    if initializer is not None:
        _refuse_what_no_child_could_receive(initializer, "initializer")
    for position, argument in enumerate(initargs):
```

New text:

```
    for position, argument in enumerate(initargs):
```

### `r1372.K19_passed_by_strict`

passed_by: a write that began at the snapshot's very moment is not passed

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1372.json`, row `K19_passed_by_strict`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_snapshot_passes_the_carried_records_of_its_pair_that_began_before_it`

Old text:

```
            if began is not None and not began > moment:
```

New text:

```
            if began is not None and began < moment:
```

### `r1372.K20_passed_by_any_pair`

passed_by: a snapshot lets go of every pair's carried records, not its own

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1372.json`, row `K20_passed_by_any_pair`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_snapshot_passes_the_carried_records_of_its_pair_that_began_before_it`

Old text:

```
            if _account_of(key, steps, new=new, made=made) != account_id:
                continue
            began = placeholders.parse_hearted(steps.get(account))
            if began is not None
```

New text:

```
            began = placeholders.parse_hearted(steps.get(account))
            if began is not None
```

### `r1372.K21_made_pair_unmapped`

_account_of: a made pair is read under its key, not the account playlist it was made as

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1372.json`, row `K21_made_pair_unmapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`
- Collected: 89 against a baseline of 89
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_made_pair_is_read_under_the_account_playlist_it_was_made_as`
  - `tests/test_sync_pair_stopped.py::test_a_snapshot_passes_the_carried_records_of_its_pair_that_began_before_it`

Old text:

```
    if key.startswith(new):
        return steps.get(made) if isinstance(steps.get(made), str) else ""
    return key
```

New text:

```
    return key
```

### `r1376.F14_finished_filter_gone`

stopped_writes (sample, U225): a stop a later run finished is still read, by a first sync among others

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1376.json`, row `F14_finished_filter_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_later_run_that_finished_the_pair_hides_the_stopped_write_in_either_order`

Old text:

```
        if account_id not in finished or not finished[account_id] > began
```

New text:

```
        if True
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

### `r1394.S5_sent_read_as_landed`

stopped write: the sent count is read from the landed field, so a move in flight reads as known not sent

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1394.json`, row `S5_sent_read_as_landed`
- Moved: Same return in _moving; U298 replaced the module's _count with cli.output.count_of
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`
- Collected: 177 against a baseline of 177
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_move_whose_fate_is_unknown_holds_the_order_before_it_and_finishes_the_one_after`
  - `tests/test_sync_pair_stopped.py::test_a_moving_step_reads_back_its_counts`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts1]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts2]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts3]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts5]`

Old text:

```
    return at, start, end, count_of(value.get(SENT)), count_of(value.get(LANDED))
```

New text:

```
    return at, start, end, count_of(value.get(LANDED)), count_of(value.get(LANDED))
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

### `r1418.F7_composite_ordering_start_unread`

what F7 holds: a stopped write with no moving step reads no start from its ordering step, so the start F7 narrows is never read

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1418.json`, row `F7_composite_ordering_start_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 20 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_holds_a_reorder_made_on_the_account_since`
  - `tests/test_sync_pair_settle.py::test_a_drag_to_the_top_after_a_write_that_sent_no_move_leads[all-read]`
  - `tests/test_sync_pair_settle.py::test_a_drag_to_the_top_after_a_write_that_sent_no_move_leads[t9-unread]`
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - `tests/test_sync_pair_settle.py::test_a_reorder_after_a_finish_stopped_before_its_first_send_leads`
  - `tests/test_sync_pair_settle.py::test_a_reorder_after_a_track_read_at_the_stop_turned_unread_leads`
  - `tests/test_sync_pair_settle.py::test_a_track_unread_at_the_stop_and_read_since_is_read_as_the_persons_when_moved`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_before_the_first_send_is_kept_where_it_was_put`
  - `tests/test_sync_pair_stopped.py::test_a_write_begun_ordered_and_not_finished_is_read_back_whole`
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_that_moves_again_before_it_settles_is_held_again`
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_waits_the_agreement_window`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_off_the_path_no_sync_read_before_is_not_read_as_the_persons`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_the_person_made_on_the_account_after_a_sync_read_it_still_leads`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_that_moved_before_it_settled_starts_again`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_read_off_the_path_on_its_first_sync_keeps_rekordboxs_order`
  - ... and 5 more, see the JSON sidecar

Old text:

```
    begin = sent[1] if sent is not None else start
```

New text:

```
    begin = sent[1] if sent is not None else ()
```

### `r1434.S2_positions_compare_every_track_listed`

existing guard, U225: the path compares every track listed now, a track added since included, so an addition reads the account off the path

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1434.json`, row `S2_positions_compare_every_track_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_track_added_or_taken_off_since_is_left_out_of_the_comparison`
  - `tests/test_sync_pair_stopped.py::test_positions_counts_the_moves_that_leave_each_order_on_the_path`

Old text:

```
    common = set(current) & set(start)
```

New text:

```
    common = set(current)
```

### `u220.A3_keep_head`

_to_the_front: match the asked order's head rather than its tail, the old to the end rule

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `u220.json`, row `A3_keep_head`
- Moved: U298 replaced tidal_account._to_the_front's body with sync.pair_stopped.front_moves, its copy until then, which the adapter now returns; the same tail match
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 283 against a baseline of 283
- Kills: 26 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_412_on_the_third_move_resends_that_move_once_and_no_other`
  - `tests/test_outbound_order.py::test_a_move_that_failed_another_way_is_left_as_maybe_landed`
  - `tests/test_outbound_order.py::test_a_move_that_lands_anywhere_else_is_not_read_back_and_the_settle_reading_shows_it`
  - `tests/test_outbound_order.py::test_a_provider_whose_move_to_the_length_lands_one_short_still_takes_the_order`
  - `tests/test_outbound_order.py::test_a_read_that_lags_every_move_does_not_stop_the_order`
  - `tests/test_outbound_order.py::test_a_recorder_that_cannot_record_has_no_further_move_sent`
  - `tests/test_outbound_order.py::test_an_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_outbound_order.py::test_every_move_is_planned_from_one_reading_and_sent_with_no_read_between`
  - `tests/test_outbound_order.py::test_every_move_is_to_the_front_where_both_ways_of_counting_agree`
  - `tests/test_outbound_order.py::test_nothing_to_move_tells_the_caller_nothing`
  - `tests/test_outbound_order.py::test_the_caller_is_told_before_each_move_how_many_may_have_landed`
  - `tests/test_outbound_order.py::test_the_fake_account_orders_by_the_adapters_rule[before1-order1]`
  - `tests/test_outbound_order.py::test_the_fake_account_orders_by_the_adapters_rule[before2-order2]`
  - `tests/test_outbound_order.py::test_the_fake_account_orders_by_the_adapters_rule[before3-order3]`
  - `tests/test_outbound_order.py::test_the_pauses_after_a_412_start_again_for_each_move`
  - ... and 11 more, see the JSON sidecar

Old text:

```
one == wanted[len(wanted) - 1 - keep]
```

New text:

```
one == wanted[keep]
```

### `u220.A4_first_first`

_to_the_front: move the tracks first first rather than last first, so the moved ones land reversed

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `u220.json`, row `A4_first_first`
- Moved: U298 replaced tidal_account._to_the_front's body with sync.pair_stopped.front_moves, its copy until then, which the adapter now returns; the same reversal of the moves
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 283 against a baseline of 283
- Kills: 14 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_412_on_the_third_move_resends_that_move_once_and_no_other`
  - `tests/test_outbound_order.py::test_a_provider_whose_move_to_the_length_lands_one_short_still_takes_the_order`
  - `tests/test_outbound_order.py::test_a_read_that_lags_every_move_does_not_stop_the_order`
  - `tests/test_outbound_order.py::test_a_reading_holding_what_the_adds_left_in_another_order_is_not_stale`
  - `tests/test_outbound_order.py::test_an_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_outbound_order.py::test_every_move_is_planned_from_one_reading_and_sent_with_no_read_between`
  - `tests/test_outbound_order.py::test_the_caller_is_told_before_each_move_how_many_may_have_landed`
  - `tests/test_outbound_order.py::test_the_fake_account_orders_by_the_adapters_rule[before2-order2]`
  - `tests/test_outbound_order.py::test_the_pauses_after_a_412_start_again_for_each_move`
  - `tests/test_outbound_order.py::test_the_reading_after_a_412_is_held_to_what_the_adds_left[False]`
  - `tests/test_outbound_order.py::test_the_reading_after_a_412_is_held_to_what_the_adds_left[True]`
  - `tests/test_outbound_order.py::test_the_tracks_before_the_kept_tail_are_moved_last_first`
  - `tests/test_sync_pair_account.py::test_a_move_that_landed_elsewhere_is_left_to_the_settle_reading_with_every_track_kept`
  - `tests/test_sync_pair_account.py::test_the_order_moves_each_track_to_the_front_and_reads_back`

Old text:

```
    return list(reversed(wanted[: len(wanted) - keep]))
```

New text:

```
    return wanted[: len(wanted) - keep]
```

### `u225.M6_front_keeps_nothing`

front_moves: no tail is kept, every asked track is moved

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `u225.json`, row `M6_front_keeps_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_orders_on_the_path_that_differ_only_by_a_track_taken_off_all_count`

Old text:

```
            keep += 1
    return list(reversed(wanted[: len(wanted) - keep]))
```

New text:

```
            keep += 0
    return list(reversed(wanted[: len(wanted) - keep]))
```

### `u225.M8_reached_strict_membership`

reached: a track added or taken off since is compared too

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `u225.json`, row `M8_reached_strict_membership`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`
- Collected: 89 against a baseline of 89
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_track_added_or_taken_off_since_is_left_out_of_the_comparison`
  - `tests/test_sync_pair_stopped.py::test_orders_on_the_path_that_differ_only_by_a_track_taken_off_all_count`
  - `tests/test_sync_pair_stopped.py::test_positions_counts_the_moves_that_leave_each_order_on_the_path`

Old text:

```
    common = set(current) & set(start)
```

New text:

```
    common = set(current) | set(start)
```

### `u225.M9_finish_ignored`

stopped_writes: a later run that finished the pair does not hide the stopped write

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `u225.json`, row `M9_finish_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`
- Collected: 89 against a baseline of 89
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_carried_copy_gives_way_to_its_own_runs_steps_kept_under_the_same_plan`
  - `tests/test_sync_pair_stopped.py::test_a_finished_or_unordered_write_is_no_stopped_one`
  - `tests/test_sync_pair_stopped.py::test_a_later_run_that_finished_the_pair_hides_the_stopped_write_in_either_order`

Old text:

```
            if done in steps:
                if account_id not in finished
```

New text:

```
            if False:
                if account_id not in finished
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

