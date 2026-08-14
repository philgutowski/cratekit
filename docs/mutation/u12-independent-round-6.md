# Mutation table: u12-independent-round-6

Measured by `scripts/mutate.py` on 2026-08-14 22:36 UTC, branch `unit/u12-memory-derived-worker-sizing` at `fc73b82`. Pass kind: full.

Baseline: green, 3448 collected. pytest invocations for this batch: 8.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 3448 against 3448. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `C2_reserve_halved` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 5 | killed |
| `C4_darwin_headroom` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 8 | killed |
| `C5_swap_threshold` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 4 | killed |
| `C6_used_percent_ceiling` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 2 | killed |
| `C7_max_tasks_per_child` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 3 | killed |
| `C8_probe_deadline` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 1 | killed |
| `C9_reap_budget` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 1 | killed |
| `P1_reserve_not_applied` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 18 | killed |
| `P2_order_reversed` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 1 | killed |
| `P3_budget_can_go_negative` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 2 | killed |
| `P4_no_floor_of_one_worker` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 11 | killed |
| `P5_tie_goes_to_the_ceiling` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 1 | killed |
| `P6_no_insufficient_memory_bound` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 5 | killed |
| `P7_swap_gate_strict` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 2 | killed |
| `P8_used_gate_strict` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 2 | killed |
| `P9_pressure_gate_needs_both` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 8 | killed |
| `P10_recycle_reported_for_in_process` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 2 | killed |
| `P12_unreadable_falls_back_to_ceiling` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 8 | killed |
| `R1_available_type_check` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 5 | killed |
| `R2_available_never_raises` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 2 | killed |
| `R3_pressure_percent_range` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 1 | killed |
| `R4_pressure_type_check` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 2 | killed |
| `M1_measurement_below_the_floor` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 1 | killed |
| `M2_nonsense_measurement_accepted` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 2 | killed |
| `M3_zero_deadline_allowed` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 1 | killed |
| `M4_model_freed_before_the_reading` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 1 | killed |
| `M5_terminate_rung_removed` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 3 | killed |
| `M6_kill_rung_removed` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 1 | killed |
| `M7_parent_keeps_the_write_end` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 1 | killed |
| `M8_no_reap_after_the_probe` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 1 | killed |
| `G1_dotdot_not_refused` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 1 | killed |
| `G2_containment_dropped` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 2 | killed |
| `G3_headroom_can_go_negative` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 1 | killed |
| `G4_controller_substring_match` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 2 | killed |
| `G5_loosest_cap_wins` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 1 | killed |
| `G6_cgroup_cap_ignored` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 7 | killed |
| `G7_valueerror_escapes_the_reader` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 1 | killed |
| `X1_pool_of_one_built` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 1 | killed |
| `X3_generation_boundary_removed` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 1 | killed |
| `X4_initargs_not_refused` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 1 | killed |
| `X5_in_process_path_removed` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 1 | killed |
| `X7_generation_size_drops_the_width` | `src/cratekit/core/pool.py` | user | 1 file(s) | 267 | 9 | killed |
| `S1_relative_climb_past_the_top` | `tests/_source_guards.py` | maintainer | 3 file(s) | 3448 | 0 (promoted) | zero |
| `S2_package_never_resolved` | `tests/_source_guards.py` | maintainer | 3 file(s) | 831 | 7 | killed |
| `S3_only_the_module_itself_counts` | `tests/_source_guards.py` | maintainer | 3 file(s) | 831 | 6 | killed |

## Zero rows and what they owe

- `S1_relative_climb_past_the_top` (maintainer facing): maintainer facing, composite not required

## Considered and dropped

METHOD caps a full pass at 45 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `C1_worker_ceiling`: Raise DEFAULT_WORKER_CEILING from two to three Dropped because: ranked below the cap: the file names a dedicated literal pin, test_the_default_ceiling_is_two_because_two_is_what_survived_a_real_run, so the outcome is known before the row runs and the row buys no information. The same constant family is sampled by C2 and C4.
- `C3_general_headroom`: Raise GENERAL_HEADROOM_PERCENT from seventy five to eighty five Dropped because: ranked below the cap for the same reason as C1: a named literal pin exists, and the darwin share this machine actually runs on is measured instead as C4.
- `C10_cgroup_unlimited_sentinel`: Lower _CGROUP_UNLIMITED_ABOVE from 1<<62 to 1<<40 Dropped because: ranked below the cap: a parametrized test names two large caps against the sentinel, and the cgroup family already has seven rows.
- `P11_unreadable_bound_collapsed`: Report MEMORY_UNREADABLE as INSUFFICIENT_MEMORY Dropped because: ranked below the cap: P12 mutates the same branch on the axis that has a user facing cost, the worker count, rather than on the label.
- `R5_negative_swap_accepted`: Accept a negative swap figure as a real pressure reading Dropped because: ranked below the cap: the reader family already has four rows and this is the narrowest of its validations.
- `G8_limit_file_containment`: Stop resolving the limit file itself against the mount Dropped because: ranked below the cap: G2 mutates the one helper both the directory check and the file check go through, so the containment property is measured once at its seam.
- `X2_fork_context`: Build the executor with a fork context rather than spawn Dropped because: ranked below the cap: a source guard, test_every_context_this_module_builds_is_written_as_spawn_in_the_source, reads the literal out of the source, so the outcome is known.
- `X6_generations_floor_division`: Round generations down rather than up Dropped because: ranked below the cap: a parametrized test enumerates the items-to-generations mapping including a partial last generation.
- `X8_in_process_predicate`: Change PoolPlan.in_process from workers == 1 to workers < 1 Dropped because: ranked below the cap: X1 and X5 both drive the in_process seam from the two sides that have a cost.
- `S4_empty_candidate_tail`: Drop the empty-candidate guard in _dotted_tail_of Dropped because: ranked below the cap: reachable only through the tail fallback S2 already forces on, and its cost is a maintainer facing false positive.
- `S5_pool_constructor_set`: Drop 'Pool' from _POOL_CONSTRUCTORS in tests/test_pool_sizing.py Dropped because: ranked below the cap: a guard's own fixture list is mutated by the guard's own parametrized evasion suite, so this measures the fixture rather than the shipped tree.

## Row definitions

### `C2_reserve_halved`

Halve the absolute memory reserve coefficient, two gibibytes to one. A reserve that can be halved with a green suite is a reserve nothing pins.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
- Kills: 5 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_line_this_reader_cannot_parse_is_skipped_rather_than_raised_out_of[a-leading-blank]`
  - `tests/test_pool_sizing.py::test_a_line_this_reader_cannot_parse_is_skipped_rather_than_raised_out_of[a-line-with-no-colon]`
  - `tests/test_pool_sizing.py::test_a_line_this_reader_cannot_parse_is_skipped_rather_than_raised_out_of[a-short-read]`
  - `tests/test_pool_sizing.py::test_a_line_this_reader_cannot_parse_is_skipped_rather_than_raised_out_of[a-trailing-blank-line]`
  - `tests/test_pool_sizing.py::test_the_absolute_reserve_is_two_gibibytes_of_the_reading_that_was_never_ours`

Old text:

```
DEFAULT_MEMORY_RESERVE_BYTES = 2 * 1024**3
```

New text:

```
DEFAULT_MEMORY_RESERVE_BYTES = 1 * 1024**3
```

### `C4_darwin_headroom`

Raise the darwin headroom share from half to three quarters, which is the value the measured inactive-queue split says is too optimistic.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
- Kills: 8 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_line_this_reader_cannot_parse_is_skipped_rather_than_raised_out_of[a-leading-blank]`
  - `tests/test_pool_sizing.py::test_a_line_this_reader_cannot_parse_is_skipped_rather_than_raised_out_of[a-line-with-no-colon]`
  - `tests/test_pool_sizing.py::test_a_line_this_reader_cannot_parse_is_skipped_rather_than_raised_out_of[a-short-read]`
  - `tests/test_pool_sizing.py::test_a_line_this_reader_cannot_parse_is_skipped_rather_than_raised_out_of[a-trailing-blank-line]`
  - `tests/test_pool_sizing.py::test_the_darwin_headroom_claims_half_because_half_is_what_was_measured`
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

### `C5_swap_threshold`

Raise the swap pressure threshold from one gibibyte to four, so the machine the documented kill happened on is no longer refused a pool.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
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

### `C6_used_percent_ceiling`

Raise the used-percent ceiling from eighty five to ninety five.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
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

### `C7_max_tasks_per_child`

Two and a half times the recycle budget, one hundred to two hundred fifty, so a child holds an allocator two and a half times longer before retiring.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
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

### `C8_probe_deadline`

Cut the probe deadline from two minutes to forty five seconds, below the twice-the-reference floor the docstring claims the suite states.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
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

### `C9_reap_budget`

Halve the reaping budget, one second to half a second, which the round six docstring names as the value that makes the terminate rung a race.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
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

### `P1_reserve_not_applied`

Drop the absolute reserve from the budget entirely, so the whole reading is claimable before the percent scales it.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
- Kills: 18 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_capped_service_on_a_huge_host_is_sized_by_the_service`
  - `tests/test_pool_sizing.py::test_a_line_this_reader_cannot_parse_is_skipped_rather_than_raised_out_of[a-leading-blank]`
  - `tests/test_pool_sizing.py::test_a_line_this_reader_cannot_parse_is_skipped_rather_than_raised_out_of[a-line-with-no-colon]`
  - `tests/test_pool_sizing.py::test_a_line_this_reader_cannot_parse_is_skipped_rather_than_raised_out_of[a-short-read]`
  - `tests/test_pool_sizing.py::test_a_line_this_reader_cannot_parse_is_skipped_rather_than_raised_out_of[a-trailing-blank-line]`
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
  - ... and 3 more, see the JSON sidecar

Old text:

```
    budget = max(0, available - reserve_bytes)

```

New text:

```
    budget = max(0, available)

```

### `P2_order_reversed`

Reverse the last two steps: divide into workers first and then scale the count, which the docstring says differs only at the boundaries.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_the_headroom_is_applied_to_the_bytes_before_they_are_divided_into_workers`

Old text:

```
    affordable = budget * headroom_percent // 100 // worker_bytes

```

New text:

```
    affordable = budget // worker_bytes * headroom_percent // 100

```

### `P3_budget_can_go_negative`

Remove the floor at zero so a reading smaller than the reserve produces a negative budget and a negative affordable count.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
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

### `P4_no_floor_of_one_worker`

Remove the floor of one worker, so a machine that affords none plans a pool of zero.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
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

### `P5_tie_goes_to_the_ceiling`

Put the ceiling ahead of available memory in the precedence list, so a tie is reported as the ceiling rather than as memory.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
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

### `P6_no_insufficient_memory_bound`

Remove the reclassification that tells a machine affording exactly one from a machine affording none.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
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

### `P7_swap_gate_strict`

Turn the swap gate from at-or-above into strictly above, so a machine exactly on the line is given a pool.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
- Kills: 2 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_the_pressure_gate_bites_at_its_two_lines_and_nowhere_else[swap-at-the-line]`
  - `tests/test_pool_sizing.py::test_the_swap_threshold_is_a_gibibyte_and_the_gibibyte_is_load_bearing[a-full-gibibyte]`

Old text:

```
        pressure.swap_used_bytes >= swap_pressure_bytes

```

New text:

```
        pressure.swap_used_bytes > swap_pressure_bytes

```

### `P8_used_gate_strict`

The same one line over: the used-percent gate becomes strictly above.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
- Kills: 2 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_the_pressure_gate_bites_at_its_two_lines_and_nowhere_else[percent-at-the-line]`
  - `tests/test_pool_sizing.py::test_the_used_percent_ceiling_is_eighty_five_and_the_number_is_load_bearing[at-the-line]`

Old text:

```
        or pressure.used_percent >= used_percent_ceiling

```

New text:

```
        or pressure.used_percent > used_percent_ceiling

```

### `P9_pressure_gate_needs_both`

Require BOTH pressure signals before refusing a pool, so either one alone no longer gates.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
- Kills: 8 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_gated_plan_still_reports_the_reading_it_was_gated_despite`
  - `tests/test_pool_sizing.py::test_the_machine_the_kill_happened_on_gets_no_pool_under_the_shipped_rule`
  - `tests/test_pool_sizing.py::test_the_pressure_gate_bites_at_its_two_lines_and_nowhere_else[percent-at-the-line]`
  - `tests/test_pool_sizing.py::test_the_pressure_gate_bites_at_its_two_lines_and_nowhere_else[swap-at-the-line]`
  - `tests/test_pool_sizing.py::test_the_swap_threshold_is_a_gibibyte_and_the_gibibyte_is_load_bearing[a-full-gibibyte]`
  - `tests/test_pool_sizing.py::test_the_swap_threshold_is_a_gibibyte_and_the_gibibyte_is_load_bearing[deep-in-swap]`
  - `tests/test_pool_sizing.py::test_the_used_percent_ceiling_is_eighty_five_and_the_number_is_load_bearing[at-the-line]`
  - `tests/test_pool_sizing.py::test_the_used_percent_ceiling_is_eighty_five_and_the_number_is_load_bearing[reclaiming-hard]`

Old text:

```
        pressure.swap_used_bytes >= swap_pressure_bytes
        or pressure.used_percent >= used_percent_ceiling

```

New text:

```
        pressure.swap_used_bytes >= swap_pressure_bytes
        and pressure.used_percent >= used_percent_ceiling

```

### `P10_recycle_reported_for_in_process`

Report a recycle count on a plan that runs in the calling process and has no child to retire.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
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

### `P12_unreadable_falls_back_to_ceiling`

Make the unreadable-memory fallback the declared ceiling rather than one worker, which is the exact fallback the brief forbids.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
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

### `R1_available_type_check`

Accept a non-integer or negative available reading as a real reading.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
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

### `R2_available_never_raises`

Remove the catch around the injected available reader, so a reader that raises raises out of plan_pool.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
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

### `R3_pressure_percent_range`

Accept a used-percent outside zero to one hundred as a real reading.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
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

### `R4_pressure_type_check`

Accept anything at all as a pressure reading, not only a Pressure.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
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

### `M1_measurement_below_the_floor`

Return the measurement even when it is below the declared floor, so the floor becomes a fallback rather than a floor.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_the_probe_never_reports_below_the_declared_floor`

Old text:

```
    return max(measured, floor_bytes)

```

New text:

```
    return measured

```

### `M2_nonsense_measurement_accepted`

Accept a boolean, a float or a zero from the probe as a byte count.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
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

### `M3_zero_deadline_allowed`

Allow a probe deadline of zero or less, which is a probe that can never answer reporting the floor as though it had measured.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
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

### `M4_model_freed_before_the_reading`

Free the loaded object before the resident set is read, the allocator retention defect the probe was rewritten to fix.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
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

### `M5_terminate_rung_removed`

Remove the terminate rung alone, so every abandoned probe child meets an unconditional kill with no chance to unwind.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
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

### `M6_kill_rung_removed`

Remove the kill backstop alone, so a child that ignores its terminate is left running and still allocating.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
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

### `M7_parent_keeps_the_write_end`

Leave the parent's copy of the pipe write end open, so a child that dies without answering is indistinguishable from a slow one.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_probe_child_that_dies_without_answering_gives_up_at_once`

Old text:

```
    # exactly like a slow one until the timeout expired.
    writer.close()

```

New text:

```
    # exactly like a slow one until the timeout expired.

```

### `M8_no_reap_after_the_probe`

Remove the reap from the probe's finally, so an abandoned child keeps its allocation on a machine already declared tight.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
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

### `G1_dotdot_not_refused`

Drop the refusal of a cgroup path containing dot dot, so a climbing path is rewritten into a real sibling cgroup and its tighter cap binds.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
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

### `G2_containment_dropped`

Stop checking that a resolved level is still inside the mount, so a symlink out of the mount is read as a level of this process's cgroup.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
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

### `G3_headroom_can_go_negative`

Report a negative headroom for a cgroup already over its cap.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_cgroup_already_over_its_cap_has_no_headroom_rather_than_negative`

Old text:

```
    return max(0, limit - used)

```

New text:

```
    return limit - used

```

### `G4_controller_substring_match`

Match the memory controller by substring, so a controller named memoryfoo sends the walk to an unrelated cgroup.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
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

### `G5_loosest_cap_wins`

Take the loosest cap on the chain rather than the tightest, so a generous unit inside a tight slice reports the unit's number.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
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

### `G6_cgroup_cap_ignored`

Ignore the cgroup cap entirely and return the host reading, which is the defect that sizes a container by its host.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
- Kills: 7 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_capped_service_on_a_huge_host_is_sized_by_the_service`
  - `tests/test_pool_sizing.py::test_a_container_capped_below_its_host_is_sized_by_the_cap`
  - `tests/test_pool_sizing.py::test_a_large_container_on_a_larger_host_is_still_sized_by_the_container`
  - `tests/test_pool_sizing.py::test_a_line_this_reader_cannot_parse_is_skipped_rather_than_raised_out_of[a-leading-blank]`
  - `tests/test_pool_sizing.py::test_a_line_this_reader_cannot_parse_is_skipped_rather_than_raised_out_of[a-line-with-no-colon]`
  - `tests/test_pool_sizing.py::test_a_line_this_reader_cannot_parse_is_skipped_rather_than_raised_out_of[a-short-read]`
  - `tests/test_pool_sizing.py::test_a_line_this_reader_cannot_parse_is_skipped_rather_than_raised_out_of[a-trailing-blank-line]`

Old text:

```
    return reading if capped is None else min(reading, capped)

```

New text:

```
    return reading

```

### `G7_valueerror_escapes_the_reader`

Narrow the kernel-file reader back to OSError, so undecodable bytes and an embedded null byte raise out of a function that promises a number.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
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

### `X1_pool_of_one_built`

Let executor_arguments build a pool for a plan of one worker instead of refusing at the seam.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
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

### `X3_generation_boundary_removed`

Give one executor all of the work rather than one generation of it, which is the deadlock the generation boundary exists to prevent.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
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

### `X4_initargs_not_refused`

Stop holding initializer arguments to the picklability rule, so the same call means two things on two machines again.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
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

### `X5_in_process_path_removed`

Build a pool even for a plan of one worker, which is the brief's third requirement inverted.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
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

### `X7_generation_size_drops_the_width`

Size a generation by one child's budget rather than by the whole set of children, so the executor is rebuilt workers times too often.

- File: `src/cratekit/core/pool.py`
- Surface: user
- Subset: test files importing cratekit.core.pool
- Ran: `tests/test_pool_sizing.py`
- Collected: 267 against a baseline of 267
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

### `S1_relative_climb_past_the_top`

Let a relative import climb past the top of the package tree and resolve to something the interpreter itself refuses.

- File: `tests/_source_guards.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`, `tests/test_review_queue.py`, `tests/test_cli_contract.py`
- Collected: 3448 against a baseline of 3448
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if level - 1 > len(parts):
        return None

```

New text:

```
(empty)
```

### `S2_package_never_resolved`

Always fall back to the dotted-tail heuristic even when the importing file's package is known, which is the false direction the round closed.

- File: `tests/_source_guards.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`, `tests/test_review_queue.py`, `tests/test_cli_contract.py`
- Collected: 831 against a baseline of 831
- Kills: 7 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_relative_import_in_an_unrelated_package_is_not_this_module[0]`
  - `tests/test_pool_sizing.py::test_a_relative_import_in_an_unrelated_package_is_not_this_module[1]`
  - `tests/test_pool_sizing.py::test_a_relative_import_in_an_unrelated_package_is_not_this_module[2]`
  - `tests/test_pool_sizing.py::test_a_relative_import_in_an_unrelated_package_is_not_this_module[3]`
  - `tests/test_pool_sizing.py::test_a_relative_import_in_an_unrelated_package_is_not_this_module[4]`
  - `tests/test_pool_sizing.py::test_the_analysis_countdown_stays_silent_on_correctly_sized_modules[a-sibling-of-its-own-named-pool]`
  - `tests/test_pool_sizing.py::test_the_walk_credits_a_relative_import_only_to_the_package_that_owns_it`

Old text:

```
                if node.level:
                    if package is None:

```

New text:

```
                if node.level:
                    if True:

```

### `S3_only_the_module_itself_counts`

Recognize only the module's own dotted name and none of its ancestor packages, the hole that let a fabricated plan through.

- File: `tests/_source_guards.py`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`, `tests/test_review_queue.py`, `tests/test_cli_contract.py`
- Collected: 831 against a baseline of 831
- Kills: 6 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_the_analysis_countdown_bites_the_evasions_that_used_to_pass_it[hand-built-plan-through-an-ancestor]`
  - `tests/test_pool_sizing.py::test_the_analysis_countdown_stays_silent_on_correctly_sized_modules[ancestor-package]`
  - `tests/test_pool_sizing.py::test_the_plan_provenance_guard_bites_a_plan_somebody_typed[4]`
  - `tests/test_pool_sizing.py::test_the_plan_provenance_guard_bites_a_plan_somebody_typed[5]`
  - `tests/test_pool_sizing.py::test_the_plan_provenance_guard_bites_a_plan_somebody_typed[6]`
  - `tests/test_pool_sizing.py::test_the_same_relative_shapes_still_bite_from_the_package_that_owns_them[2]`

Old text:

```
            for size in range(1, len(parts) + 1)

```

New text:

```
            for size in range(len(parts), len(parts) + 1)

```


---

## Independent verifier's appendix, 2026-08-14

This table was measured by an agent that did not write U12. It is the unit's
first independent pass; rounds 1 to 6 were all author tables. The rows above are
the driver's own output and nothing in them has been edited. What follows is
what the numbers mean, plus the two measurements that are not mutations.

`scripts/mutate.py` is on `main` and not on this branch, which forked 156
commits before it landed. It was run out of `main` at the worktree's own
`scripts/` path so its `REPO_ROOT` resolved here, and removed afterwards, so
this branch's own diff is unchanged by the measurement.

### Scope and how the 45 were chosen

Scoped to the whole unit diff rather than to round 6 alone, because round 6
touched `src/cratekit/core/pool.py` only in comments and the unit had never been
measured by anybody else. Rows were ranked by blast radius: the arithmetic and
gates in `plan_pool` first, then the two readers, then the probe and its reaping
ladder, then the cgroup walk, then the run path, then the shared source guard
that `cratekit.analysis` will be held to. Constants were mutated as coefficients
rather than to absurd values.

Total pytest invocations across both sittings of this batch: 51 on the first,
which measured 45 rows, and 8 on the second, which re-measured four of them.

### Why four rows were measured twice

Three rows, `C2_reserve_halved`, `C4_darwin_headroom` and `C5_swap_threshold`,
were re-measured because the verifier wrote to `src/cratekit/core/pool.py` by
hand while the first sitting's null control was still running. The write was a
restore to HEAD bytes, made after a `ps` invocation that omitted `command` from
its output format and so matched nothing, which was read as the driver being
dead when it was alive and four minutes in. The three rows reproduced exactly,
5, 8 and 4, so nothing measured was wrong; the re-run is what establishes that
rather than an argument that the timing could not have overlapped.

`M7_parent_keeps_the_write_end` was re-measured because its first form was a
bad mutation rather than a bad result. It bound a second name to the pipe's
write end and left `writer.close()` in place, which is semantically a no-op, so
its zero was a second null control wearing a guard's name. The corrected row
deletes the parent's `writer.close()` and kills 1. A zero row whose mutation
does not mutate anything is the failure mode a driver cannot catch for you: the
driver verified the substitution was applied exactly once, and it was.

### The one genuine zero

`S1_relative_climb_past_the_top`, maintainer facing, promoted to the full suite
and confirmed at 0 against 3448 collected.

Driven rather than read. Without the guard, `_absolute_module` slices with a
negative index: for a package of `cratekit.analysis` at level 4, which is
`from .... import pool`, `parts[: 2 - 3]` is `parts[:-1]`, so the function
returns `cratekit.pool` where the guard returns None. At level 3 and at level 5
the existing `if not base` check catches it and both forms agree, which is why
the hole is narrow. Every input that reaches it is an import the interpreter
itself refuses, so no importable file in this repository or in `cratekit.analysis`
can produce one. Recorded, not fixed, and it gets one line rather than a
composite because METHOD's severity floor says a maintainer facing zero cannot
block.

### The timing rows, with a repeat count and a pass rate

The harness the brief names, `tests/_hardware.py` with `time_repeated` and
`threshold_seconds`, is on `main` and NOT on this branch: the branch forked 156
commits ago. Both were loaded out of `main` into the verifier's scratch
directory and used unmodified, against `main`'s stored calibration for this
machine, median 0.068019s over 25 repeats, spread 0.0976, python 3.12.5, 11
CPUs.

| what was timed | repeats | threshold | pass rate | median | worst |
| --- | --- | --- | --- | --- | --- |
| the cooperative reap's terminate-to-exit leg | 25 | 0.5000s, the suite's own `_RELEASE_CEILING_IN_DECLARED * _RELEASE_SECONDS` | 25/25 | 0.4122s | 0.4152s |
| a probe of a child that dies without answering | 25 | 15.0000s, the branch's own literal, `threshold_seconds(220.5)` | 25/25 | 0.0860s | 0.1205s |
| a reap of a child holding a REAL 300MB resident allocation | 15 | 3.0000s, three shipped budgets | 15/15 | 1.0901s whole reap | 1.0944s |

The reaping ladder ran in the correct rung order on 25 of 25 reaps and reported
the cooperative exit code on 25 of 25. The five disjoint minima of five that the
suite's own calibration reads sat at 0.4025, 0.4128, 0.4058, 0.4043 and 0.4112,
all five inside the stated [0.3600, 0.5000] window. The band is not flaky on
this machine.

The third row is the one that is not a confirmation. See the residual titled
"The reaping band's reference is a sleep, and the real release it stands in for
is twenty four times cheaper".

### What a green suite cannot see, swept separately

- An AST walk over every `assert` in `tests/` found no assertion whose expected
  value comes from the code under test in a way that reduces it to X equals X.
  Two comparisons read the module on both sides,
  `pool.DEFAULT_HEADROOM_PERCENT == pool.default_headroom_percent(sys.platform)`
  at `tests/test_pool_sizing.py:497` and `set(pool.BOUND_PHRASES) == set(pool.Bound)`
  at line 1219. Both are deliberate and both are paired with a literal pin one
  test away, at lines 478 and 1222 respectively.
- An AST walk over every dict literal in `src`, `tests` and `scripts` found no
  duplicate key anywhere in the repository. `BOUND_PHRASES` already has its own
  guard.
- A walk over every top level name in `src` found no symbol U12 introduced that
  means something else in another module. Sixty pre-existing collisions exist
  and none of them is U12's.
- One test does forbid an implementation rather than a feature. See the residual
  titled "The in-module deadlock guard sees only a bare constructor name".
