# U12 mutation rows

Every guard, assertion and constant this unit added or changed, reverted ALONE
against the full suite, with the death count and the exact revert. A count with
no row definition beside it is not evidence, so each row spells out the edit that
produced it.

Measured 2026-08-04 on branch `unit/u12-memory-derived-worker-sizing`, worktree
`.worktrees/u12`, its own `.venv`, darwin, eleven cores. Baseline for this round:
**3430 passed, 17 skipped**, about 85 seconds. Every count below is a full suite
run, foreground, one mutation at a time, restored from a scratch snapshot rather
than from git.

A ZERO ROW IS ONLY ADMISSIBLE WITH A COMPOSITE BESIDE IT. Every zero here is
paired with a mutation that shows what the thing holds, and the pair is written
out rather than asserted.

## Round 5, the new material

### The reaping budget, now a band against a MEASURED release

| id | revert | deaths |
| --- | --- | --- |
| R1 | `pool.py` `_PROBE_REAP_SECONDS = 1.0` to `0.81` | 1 |
| R2 | `pool.py` `_PROBE_REAP_SECONDS = 1.0` to `2.0` | 1 |
| R3 | `pool.py` `_PROBE_REAP_SECONDS = 1.0` to `1.2`, inside the stated band | 0 |
| R4 | `pool.py` `_PROBE_REAP_SECONDS = 1.0` to `1.3`, one step above the ceiling | 1 |
| R21 | `pool.py` `_PROBE_REAP_SECONDS = 1.0` to `0.45` | 1 |
| R24 | `pool.py` `_PROBE_REAP_SECONDS = 1.0` to `4.0` | 1 |
| R19 | `tests` `_BUDGET_FLOOR_IN_RELEASES = 2.0` to `1.0`, alone | 0 |
| R20 | COMPOSITE R19 plus `_PROBE_REAP_SECONDS = 0.45` | 0 |
| R22 | `tests` `_BUDGET_CEILING_IN_RELEASES = 3.0` to `10.0`, alone | 0 |
| R23 | COMPOSITE R22 plus `_PROBE_REAP_SECONDS = 4.0` | 0 |
| R25 | `tests` `_RELEASE_SECONDS = 0.4` to `0.3` | 1 |
| R26 | `tests` `_RELEASE_SECONDS = 0.4` to `0.6` | 1 |

R1 and R2 are the round 4 defect. The old bound read
`_PROBE_REAP_SECONDS >= 2 * _RELEASE_SECONDS`, both sides literals typed into the
test file, so the shipped budget moved freely over `[0.8, unbounded)`. It is now
a band against the terminate-to-exit leg that the reap in front of it TIMED, so
`0.81` and `2.0` both fail.

R19 and R22 are zero because a WEAKENED bound cannot fail on its own; that is
arithmetic, not evidence of a free coefficient. R20 and R23 are what the
coefficients hold. With the floor halved, a budget of `0.45` passes, and `0.45`
is a budget with under forty milliseconds of slack over a leg measured at `0.41`,
which is a race rather than a rung. With the ceiling loosened to ten, a budget of
`4.0` passes, and `4.0` is four seconds of stalling per rung in the `finally` of
a probe that already failed. R21 and R24 are the same two budgets without the
coefficient change, and both die.

R25 and R26 make `_RELEASE_SECONDS` two-sided as a consequence of the band: a
cheaper stand-in drops the ceiling under the shipped budget and a dearer one
lifts the floor over it.

### The probe deadline, now two edges in the same units

| id | revert | deaths |
| --- | --- | --- |
| R5 | `pool.py` `DEFAULT_PROBE_TIMEOUT_SECONDS = 120.0` to `90.0` | 1 |
| R6 | `pool.py` `DEFAULT_PROBE_TIMEOUT_SECONDS = 120.0` to `599.0` | 1 |
| R7 | `pool.py` `DEFAULT_PROBE_TIMEOUT_SECONDS = 120.0` to `119.0` | 1 |
| R8 | `pool.py` `DEFAULT_PROBE_TIMEOUT_SECONDS = 120.0` to `301.0` | 1 |
| R9 | `pool.py` `DEFAULT_PROBE_TIMEOUT_SECONDS = 120.0` to `200.0`, inside the band | 0 |
| R15 | `pool.py` `DEFAULT_PROBE_TIMEOUT_SECONDS = 120.0` to `60.0` | 1 |
| R18 | `pool.py` `DEFAULT_PROBE_TIMEOUT_SECONDS = 120.0` to `3000.0` | 1 |
| R10 | `tests` `_A_COLD_MODEL_LOAD_SECONDS = 60.0` to `1.0` | 1 |
| R11 | `tests` `_A_COLD_MODEL_LOAD_SECONDS = 60.0` to `70.0` | 1 |
| R12 | `tests` `_A_COLD_MODEL_LOAD_SECONDS = 60.0` to `20.0` | 1 |
| R13 | `tests` `_DEADLINE_FLOOR_IN_LOADS = 2.0` to `1.0`, alone | 0 |
| R14 | COMPOSITE R13 plus `DEFAULT_PROBE_TIMEOUT_SECONDS = 60.0` | 0 |
| R16 | `tests` `_DEADLINE_CEILING_IN_LOADS = 5.0` to `50.0`, alone | 0 |
| R17 | COMPOSITE R16 plus `DEFAULT_PROBE_TIMEOUT_SECONDS = 3000.0` | 0 |

The band was `[1.5 * _A_COLD_MODEL_LOAD_SECONDS, 600.0]`, one derived edge and one
literal, and the literal is what let `599.0` pass while the reference load itself
could be driven to `1.0`. Both edges are now multiples of the same reference load,
so R10 kills through the CEILING and R11 kills through the FLOOR. The reference
load is pinned to `[24, 60]` by the shipped deadline; R11 and R12 are the nearest
realistic steps outside it.

R13 and R16 are weakened bounds and cannot fail alone. R14 shows the halved floor
admits a deadline set AT the cold load, which is the coin flip that pays out as
the floor and sizes the whole run wrong; R15 is that same deadline without the
coefficient change and it dies. R17 shows the loosened ceiling admits a fifty
minute wait; R18 is that wait alone and it dies.

### The identity assertion, made able to fail

| id | revert | deaths |
| --- | --- | --- |
| R27 | `tests` delete `assert given[0] == pool.DEFAULT_PROBE_TIMEOUT_SECONDS, (...)`, alone | 0 |
| R28 | `pool.py` `measure_worker_bytes` default `timeout_seconds: float = DEFAULT_PROBE_TIMEOUT_SECONDS` to `= 200.0` | 2 |
| R29 | same, to `= 120.0`, the SAME value the constant holds today | 1 |
| R30 | COMPOSITE R29 plus `checked = {"measure_worker_bytes", "_spawned_probe"}` to `checked = set()` | 0 |
| R31 | COMPOSITE R28 plus that same neutering | 1 |

The runtime identity assertion compares the deadline the probe received against
the constant it came from, and there is one number in play, so it cannot fail on
its own: R27 is zero. R28 is what it does hold, a call site frozen at a DIFFERENT
value, and R31 isolates it by neutering the new source guard, leaving exactly one
death.

R29 is the case the runtime assertion cannot see at all: a default argument is
bound once at import, so a signature that repeats today's value is
indistinguishable at runtime from one that names the constant. The source guard
`test_every_probe_deadline_default_names_the_constant_rather_than_repeating_it`
kills it, and R30 shows that guard is the sole killer.

### The controller field guard, armed on both sides

| id | revert | deaths |
| --- | --- | --- |
| R32 | `pool.py` `elif "memory" in controllers.split(","):` to `elif "memory" in controllers:` | 2 |
| R33 | `pool.py` same line to `elif controllers == "memory":` | 1 |

R32 was zero before this round, which is the whole finding: round 3 fixed the
loose direction and then measured only the tight one. Two parametrized cases now
drive it, `7:memoryfoo:/sneaky` and `9:blkio,memory_hotplug:/sneaky`. R33 confirms
the tight direction still dies, unchanged.

### The walk really staying inside the mount

| id | revert | deaths |
| --- | --- | --- |
| R34 | `pool.py` `_cgroup_directories` returns `candidates` unfiltered, dropping the resolve-and-contain filter | 0 |
| R35 | `pool.py` `_headroom_in` reads `directory / limit_file` and `directory / used_file` without `_contained` | 1 |
| R36 | COMPOSITE R34 plus R35, which is the walk exactly as round 4 shipped it | 2 |

R34 is zero because the FILE level check subsumes the directory level one when
both are present: a directory that resolves outside the mount also puts its
`memory.max` outside it. R36 is what the directory check holds on its own. Named,
because the counts alone would not say it:

- R35 kills `test_a_limit_file_that_symlinks_out_of_the_mount_is_not_read`.
- R36 kills that one AND `test_a_component_that_symlinks_out_of_the_mount_is_not_read`.

The second is the concrete input from the review: a mount publishing
`memory.max=max`, `<mount>/sneaky` symlinked to a directory outside it publishing
a four mebibyte version two cap, and `/proc/self/cgroup` reading `0::/sneaky`.
Before this round that returned `4194304`, a cap from outside the mount, while
the test named for the invariant and the docstring asserting it both passed.

`test_a_symlink_that_stays_inside_the_mount_is_still_read` drives the other
direction, so the containment is not a ban on symlinks.

### The unlimited sentinel, a width row

| id | revert | deaths |
| --- | --- | --- |
| R37 | `pool.py` `_CGROUP_UNLIMITED_ABOVE = 1 << 62` to `1 << 50` | 0 |
| R39 | `pool.py` `_CGROUP_UNLIMITED_ABOVE = 1 << 62` to `1 << 47` | 0 |
| R38 | `pool.py` `_CGROUP_UNLIMITED_ABOVE = 1 << 62` to `1 << 44` | 1 |

Recorded rather than fixed, under the residual entry titled "The unlimited
sentinel is a benign zero row, and the commit that said otherwise was wrong".
R37 and R39 bracket the top of the zero range and R38 brackets its bottom, so the
edge sits between sixteen and one hundred and twenty eight tebibytes. Round 4's
entry offered `1 << 62`, the shipped value, as one of its two measurements, which
is a no-op restated as evidence; that line is deleted and these three replace it.
This is the only width-shaped constant in the module: there is no digest, hash or
identifier width in `pool.py`.

## Confirm rows, still dying after this round's changes

| id | revert | expected | measured |
| --- | --- | --- | --- |
| R42 | `pool.py` `_read_available` drops `if not isinstance(value, int) or isinstance(value, bool) or value < 0: return None` | 5 | 5 |
| R41 | `pool.py` the whole body of `_reap` replaced with `return` | 3 | 4 |
| R40 | `pool.py` `DEFAULT_SWAP_PRESSURE_BYTES = 1 * 1024**3` to `1` | 3 | 3 |
| R43 | `pool.py` `range(len(parts), -1, -1)` to `range(len(parts), 0, -1)`, so the mount's own level is never read | 12 | 12 |

R41 gained a death rather than losing one. The new budget-band test consumes the
same module-scoped reap fixture as the rung-order test, so a `_reap` that does
nothing now fails both. That is coverage added, not coverage moved.

The round 4 report labelled nine further confirm rows M01, M42, M43, M44, M53,
M60, M61, M62 and M67 with counts and no definitions, and that numbering exists
in no file in this repository, so the rows cannot be re-run as written. That is
the reason this file exists. In their place every inherited tuning constant in
the module was re-mutated in BOTH directions at realistic nearby values, by
substance, and every one still dies:

| id | revert | deaths |
| --- | --- | --- |
| R45 | `pool.py` `DEFAULT_WORKER_CEILING = 2` to `3` | 3 |
| R51 | `pool.py` `DEFAULT_WORKER_CEILING = 2` to `1` | 3 |
| R46 | `pool.py` `DEFAULT_MEMORY_RESERVE_BYTES = 2 * 1024**3` to `1 * 1024**3` | 5 |
| R47 | `pool.py` `DEFAULT_USED_PERCENT_CEILING = 85` to `90` | 2 |
| R52 | `pool.py` `DEFAULT_USED_PERCENT_CEILING = 85` to `80` | 2 |
| R48 | `pool.py` `DEFAULT_MAX_TASKS_PER_CHILD = 100` to `200` | 3 |
| R49 | `pool.py` `DARWIN_HEADROOM_PERCENT = 50` to `60` | 2 |
| R50 | `pool.py` `GENERAL_HEADROOM_PERCENT = 75` to `80` | 3 |
| R44 | `pool.py` `range(len(parts), -1, -1)` to `range(len(parts), len(parts) - 1, -1)`, deepest level only | 1 |

## The one bound that reads a clock, and why it is not a flake

`test_the_reaping_budget_is_a_band_around_what_a_release_was_measured_to_cost`
compares the shipped budget against a timed leg rather than against a literal.
That is the only way the coefficient in it can mean anything, and it makes one
assertion depend on wall clock.

Measured on this machine: forty direct samples of the terminate-to-exit leg, twenty
idle and twenty under twenty two `nice -n 19` spinners with load average rising
from 6.1 to 17.9, gave 0.4014 to 0.4114 seconds, a spread of 9.8 milliseconds.
The band admits `[0.3333, 0.5000]`, so the nearest edge is 68 milliseconds away,
about seven times the observed spread. Two further full suite runs under the same
spinners, at load average 20.6 rising to 38.6, were green in 175 and 158 seconds.
Fifteen more full green runs came from the mutation batches above.

The fixture the leg models is a `time.sleep(0.4)`, which is faithful in COST and
not in KIND: a real probe child releasing a 300 megabyte model does allocator and
kernel work that would dilate under contention, and a sleep does not. The sleep
is the deliberate trade, recorded beside the constant. A fixture that really
allocated and freed three hundred megabytes would make the one number these tests
assert on a function of what every other process on the machine is doing, and
this repository has no conditional skip to hide the resulting flake behind.
