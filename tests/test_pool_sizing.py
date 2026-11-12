"""U12: the worker count is decided by memory, and the arithmetic is tested at the edges.

R23 says no default-configuration run exhausts memory, on any pool. The source
system sizes its pool as ``cpu_count() - 2``, which is nine on the machine that
runs it, and each worker of the heavy pass loads its own model. Nine copies of a
model on an 18 gigabyte machine already in swap is the documented kill. So the
count has to come from the resource that runs out.

WHAT THIS FILE IS ORGANIZED AROUND. Most of it is arithmetic with an injected
memory reading, because sizing must be decidable without allocating anything: a
test that had to reserve twelve gigabytes to check the twelve-worker case would
never run. The few tests that spawn real processes are the ones asserting
something no arithmetic can prove, which is that a recycled child re-runs its
initializer, that a plan of one worker starts no child at all, and that a run
above the recycle threshold FINISHES.

THAT LAST ONE IS RUN IN A CHILD WITH A WATCHDOG, and the reason is the defect it
covers. ``ProcessPoolExecutor(max_tasks_per_child=N)`` does not fail above
``workers * N`` tasks, it hangs, with no timeout and no exception, so a test
written the ordinary way would not go red. It would take the suite with it and
report nothing. A guard against a hang has to be able to survive the hang.

FOUR GUARDS HERE ARE STRUCTURAL AND ARMED TODAY, over the source rather than
over behaviour, because each names a defect that a passing suite cannot see:

* the memory reading is ``available`` and never ``free``, which are two different
  numbers and only one of them answers the question being asked;
* nothing in the sizing module reads a core count, in any of four spellings, so
  the defect it exists to prevent cannot come back through the module named
  after it;
* no module anywhere in this repository builds a process pool for itself, so a
  later unit cannot acquire its own private copy of this decision;
* no module outside the sizing module builds a :class:`PoolPlan` for itself,
  which is the same escape one level up. Routing through the right seam while
  handing it a plan somebody typed by hand is a nine-worker pool that satisfies
  every question about seams, and it was a live evasion of the first version of
  the countdown at the bottom of this file.

All of them walk the syntax tree rather than the text. The module documents at
length why it does not do these things, so a text search would fire on its own
explanation, and a guard that fires on correct code is a guard people route
around (P7). Every one of them ships fixtures in BOTH directions.
"""

from __future__ import annotations

import ast
import multiprocessing
import os
import signal
import subprocess
import sys
import time
from concurrent.futures import process as _process_pool
from pathlib import Path
from types import SimpleNamespace

import pytest

from cratekit.core import pool
from tests._parse_memo import parsed
from tests._source_guards import ImportsOf, calls_attribute, package_modules, package_of

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"
PACKAGE_ROOT = SRC_ROOT / "cratekit"
POOL_PATH = PACKAGE_ROOT / "core" / "pool.py"

#: The module every question below is asked about, named once.
POOL_MODULE = "cratekit.core.pool"
POOL_SOURCE = POOL_PATH.read_text()

MIB = 1024**2
GIB = 1024**3

#: A stand-in for the per-worker cost of a pass that loads a model. One gibibyte
#: is the source system's own declared budget for its vocal worker, so the
#: scenarios below are the plan's scenarios in the plan's own units.
WORKER = 1 * GIB

#: The four ways to ask the machine how many cores it has. Named ONCE, and used
#: by both the armed guard over the sizing module and the countdown holding U25
#: to the same rule. Two copies of this list is how one file came to give two
#: different answers to one question: the armed guard checked four spellings and
#: the countdown checked two, so ``len(os.sched_getaffinity(0)) - 2`` inside a
#: hand-built plan passed the countdown while failing the guard beside it.
CORE_COUNT_SPELLINGS = (
    "cpu_count",
    "process_cpu_count",
    "sched_getaffinity",
    "cpu_affinity",
)


@pytest.fixture(autouse=True)
def _a_machine_that_is_not_under_pressure(monkeypatch):
    """Every sizing test decides against an idle machine unless it says otherwise.

    The pressure gate reads what THIS machine is doing, and this machine is the
    one the documented kill happened on: it sits on gigabytes of swap most of the
    time. Left live, every arithmetic test below would be answering a question
    about the developer's laptop instead of about the rule, and the suite would
    pass or fail depending on how many browser tabs were open.

    So the default here is a calm machine, injected, and the tests that are ABOUT
    the gate pass their own reading explicitly, which takes precedence.
    """
    monkeypatch.setattr(
        pool, "memory_pressure", lambda: pool.Pressure(swap_used_bytes=0, used_percent=10.0)
    )


def reader(value: int):
    """A memory reading that always answers ``value``. Never touches the machine."""
    return lambda: value


def pressure(*, swap_used_bytes: int = 0, used_percent: float = 10.0):
    """A pressure reading that always answers these two numbers."""
    return lambda: pool.Pressure(swap_used_bytes=swap_used_bytes, used_percent=used_percent)


# NEITHER OF THE TWO HELPERS BELOW IS A PIN, AND THAT IS SAID HERE BECAUSE THEY
# READ LIKE ONE. Both take the shipped percent and the shipped reserve when they
# are not given one, so every boundary they derive MOVES with the number it looks
# like it is checking. That is the exact shape that let six constants travel to
# absurd values with the suite green. They are kept because a test about where
# the count flips reads better as "the rule's boundary" than as a byte count, and
# a flip is a different property from a value.
#
# The constants themselves are pinned by literals, elsewhere, and those are the
# tests that must never be deleted as duplicates of these:
#
#   * the two headroom shares: test_the_headroom_share_is_lower_where_the_reading
#     _is_measurably_worse, test_the_general_headroom_claims_three_quarters_of
#     _what_is_left, test_the_darwin_headroom_claims_half_because_half_is_what
#     _was_measured
#   * the absolute reserve: test_the_absolute_reserve_is_two_gibibytes_of_the
#     _reading_that_was_never_ours
#   * the worker ceiling: test_the_default_ceiling_is_two_because_two_is_what
#     _survived_a_real_run
#
# Every call site below that derives a number from a constant carries a one line
# reminder pointing back here, so a reader cannot mistake a derivation for a
# check.


def affordable_for(
    available: int,
    *,
    worker_bytes: int = WORKER,
    percent: int | None = None,
    reserve: int | None = None,
) -> int:
    """How many workers the RULE affords at this reading. NOT A PIN, see above.

    Derived from the three numbers the module combines, rather than copied out of
    a run of it, so this expresses the intended rule and can disagree with the
    implementation. A constant pasted from the output would agree with a defect.
    """
    percent = pool.DEFAULT_HEADROOM_PERCENT if percent is None else percent
    reserve = pool.DEFAULT_MEMORY_RESERVE_BYTES if reserve is None else reserve
    return max(0, available - reserve) * percent // 100 // worker_bytes


def threshold_for(
    workers: int,
    *,
    worker_bytes: int = WORKER,
    percent: int,
    reserve: int | None = None,
) -> int:
    """The smallest available-byte reading that affords ``workers`` workers. NOT A PIN.

    The inverse of :func:`affordable_for`, derived the same way and for the same
    reason. The reserve is added back on rather than scaled, because it comes off
    the reading before the percent touches it.
    """
    reserve = pool.DEFAULT_MEMORY_RESERVE_BYTES if reserve is None else reserve
    return reserve + -(-workers * worker_bytes * 100 // percent)


# ---------------------------------------------------------------------------
# The plan's own scenarios
# ---------------------------------------------------------------------------


def test_two_gigabytes_against_a_one_gigabyte_worker_runs_in_process():
    """The plan's first scenario: the cap is one, and one skips the pool.

    Two gigabytes divided by a one gigabyte worker looks like two workers to
    anybody dividing without headroom, and two workers is exactly the run that
    dies: the reading is optimistic, the parent is still resident, and the second
    child pays for the model in full. Under the shipped reserve the same reading
    does not afford even one, which is a different fact from affording exactly
    one and is reported as one.
    """
    plan = pool.plan_pool(worker_bytes=WORKER, items=500, read_available=reader(2 * GIB))
    assert plan.workers == 1
    assert plan.in_process is True
    assert plan.bound is pool.Bound.INSUFFICIENT_MEMORY
    assert plan.max_tasks_per_child is None


def test_sixteen_gigabytes_is_bound_by_the_hard_ceiling_at_the_default():
    """The plan's second scenario, ceiling half.

    Memory affords several here. The ceiling is what stops it, and the ceiling is
    the brake that covers the per-worker estimate being wrong rather than the
    machine being small.
    """
    # The guard is derived and is not the pin, see the note above affordable_for.
    # The count is a literal, so this test disagrees with a ceiling that moves.
    assert affordable_for(16 * GIB) > 2, (
        "the fixture no longer leaves the ceiling as the binding constraint"
    )
    plan = pool.plan_pool(worker_bytes=WORKER, items=500, read_available=reader(16 * GIB))
    assert plan.workers == 2
    assert plan.bound is pool.Bound.CEILING


def test_sixteen_gigabytes_is_bound_by_the_headroom_once_the_ceiling_is_raised():
    """The plan's second scenario, headroom half.

    With the ceiling out of the way the reserve and the headroom are the only
    things between the reading and the count, and they must actually bite:
    sixteen gigabytes never affords sixteen one gigabyte workers, at any setting
    this module ships.
    """
    plan = pool.plan_pool(
        worker_bytes=WORKER, items=500, ceiling=64, read_available=reader(16 * GIB)
    )
    assert plan.workers == affordable_for(16 * GIB)
    assert plan.workers < 16
    assert plan.bound is pool.Bound.AVAILABLE_MEMORY


def test_a_memory_read_failure_falls_back_to_one_worker_rather_than_raising():
    """The plan's third scenario. A machine that cannot be measured gets one worker."""

    def broken() -> int:
        raise OSError("no memory statistics on this platform")

    plan = pool.plan_pool(worker_bytes=WORKER, items=500, read_available=broken)
    assert plan.workers == 1
    assert plan.in_process is True
    assert plan.bound is pool.Bound.MEMORY_UNREADABLE
    assert plan.available_bytes is None


def test_the_fallback_is_never_the_ceiling_or_the_item_count():
    """A fallback larger than what memory allows is not a fallback.

    The failure this guards is the natural one: a memory read that fails, caught,
    and answered with the count the caller would have used anyway. The wrong
    answers are all present here as arguments, so the test can tell one worker
    chosen deliberately from one worker that happened to be the smallest input.
    """

    def broken() -> int:
        raise RuntimeError("psutil is not installed")

    plan = pool.plan_pool(
        worker_bytes=1,
        items=10_000,
        ceiling=64,
        max_tasks_per_child=50,
        read_available=broken,
    )
    assert plan.workers == 1
    assert plan.max_tasks_per_child is None


@pytest.mark.parametrize(
    "value",
    [-1, -(2**40), None, "lots of memory", 3.5, True],
    ids=["negative", "very-negative", "none", "text", "float", "bool"],
)
def test_a_reading_that_is_not_a_byte_count_is_treated_as_unreadable(value):
    """A nonsense reading is no more usable than an exception, so it lands the same.

    ``True`` is in the list on purpose. It is an integer in this language, it is
    equal to one, and a byte count of one would size every pool at one worker
    while reporting that memory was read successfully.
    """
    plan = pool.plan_pool(worker_bytes=WORKER, items=500, read_available=lambda: value)
    assert plan.workers == 1
    assert plan.bound is pool.Bound.MEMORY_UNREADABLE
    assert plan.available_bytes is None


def test_the_core_count_does_not_change_the_computed_cap():
    """The plan's fourth scenario, driven at the two spellings that could leak in.

    Both are patched at once because the assertion is about the ANSWER, not about
    which function was called: a cap that moved under either patch would mean the
    count is derived from cores somewhere, which is the defect this unit exists
    to end.
    """
    made = []
    for cores in (1, 64):
        with pytest.MonkeyPatch.context() as patch:
            patch.setattr(os, "cpu_count", lambda cores=cores: cores)
            patch.setattr(multiprocessing, "cpu_count", lambda cores=cores: cores)
            made.append(
                pool.plan_pool(
                    worker_bytes=WORKER,
                    items=500,
                    ceiling=64,
                    read_available=reader(16 * GIB),
                )
            )
    assert made[0] == made[1]
    assert made[0].workers == affordable_for(16 * GIB)


# ---------------------------------------------------------------------------
# The edges, which is where a headroom factor and a hard ceiling disagree
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("workers", [2, 3, 4])
def test_the_worker_count_flips_exactly_at_the_affordable_boundary(workers):
    """One byte below the boundary is one fewer worker. Test the edges, not the middle.

    A sizing rule tested at sixteen gigabytes and two gigabytes is tested where
    every plausible implementation agrees. Every implementation that is WRONG is
    wrong within one byte of a boundary, which is why the boundary is derived
    here from the rule rather than read off a run.
    """
    # Derived, and NOT the pin on the headroom share, see the note above
    # affordable_for. What is under test here is the flip, not the number.
    edge = threshold_for(workers, percent=pool.DEFAULT_HEADROOM_PERCENT)
    below = pool.plan_pool(
        worker_bytes=WORKER, items=500, ceiling=64, read_available=reader(edge - 1)
    )
    at = pool.plan_pool(
        worker_bytes=WORKER, items=500, ceiling=64, read_available=reader(edge)
    )
    assert below.workers == workers - 1
    assert at.workers == workers


def test_the_headroom_is_applied_to_the_bytes_before_they_are_divided_into_workers():
    """The order of two integer operations, which disagree only at the edges.

    With 2900 mebibytes available and a 1024 mebibyte worker, scaling the byte
    budget first affords two workers and scaling the worker COUNT afterwards
    affords one. Both readings sit in the middle of the range and both orders
    look like "apply the headroom", which is why this is asserted against the
    reversed calculation rather than against a number.

    THE RESERVE AND THE PERCENT ARE PINNED HERE rather than taken from the
    defaults, because this fixture only distinguishes the two orders at some
    settings, and a test whose whole subject is a distinction has to be run where
    the distinction exists. The assertion below fails loudly if that stops being
    true rather than passing vacuously.
    """
    available = 2900 * MIB
    percent = 75

    shipped = available * percent // 100 // WORKER
    reversed_order = available // WORKER * percent // 100
    assert shipped != reversed_order, "the fixture no longer distinguishes the two orders"

    plan = pool.plan_pool(
        worker_bytes=WORKER,
        items=500,
        ceiling=64,
        headroom_percent=percent,
        reserve_bytes=0,
        read_available=reader(available),
    )
    assert plan.workers == shipped == 2
    assert plan.workers != reversed_order


def test_the_reserve_comes_off_the_reading_before_the_percent_scales_it():
    """The other order question, and the one the reserve was added to answer.

    Taking a fixed reserve out of the SHARE rather than out of the reading gives
    a reserve that shrinks exactly when the machine is tightest, which is
    backwards: the operating system needs the same room on a small machine as on
    a large one. The two orders are asserted against each other rather than
    against a number, so the fixture cannot drift into agreeing with either.
    """
    available = 8 * GIB
    reserve = 2 * GIB
    percent = 50

    shipped = (available - reserve) * percent // 100 // WORKER
    reserve_after = (available * percent // 100 - reserve) // WORKER
    assert shipped != reserve_after, "the fixture no longer distinguishes the two orders"

    plan = pool.plan_pool(
        worker_bytes=WORKER,
        items=500,
        ceiling=64,
        headroom_percent=percent,
        reserve_bytes=reserve,
        read_available=reader(available),
    )
    assert plan.workers == shipped == 3
    assert plan.workers != reserve_after


def test_a_reading_smaller_than_the_reserve_affords_nothing_rather_than_going_negative():
    """The reserve is a subtraction, and a subtraction is where a byte count goes negative.

    A negative budget scaled by a percent is a negative count, and a negative
    count fed to ``min`` wins every comparison. The clamp is at the budget rather
    than at the count so the reason survives: this machine did not afford a
    worker, which is not the same as the ceiling being one.
    """
    plan = pool.plan_pool(
        worker_bytes=WORKER,
        items=500,
        ceiling=64,
        reserve_bytes=4 * GIB,
        read_available=reader(1 * GIB),
    )
    assert plan.workers == 1
    assert plan.bound is pool.Bound.INSUFFICIENT_MEMORY


def test_the_hard_ceiling_and_the_headroom_agree_at_the_point_they_cross():
    """Where the two brakes meet, whichever is smaller wins and the tie names memory.

    A tie has to resolve one way and be documented, because a caller logging the
    reason gets one answer per run and two answers is a bug report nobody can
    reproduce. Memory wins, since it is the input that changes tomorrow.
    """
    # Derived, and NOT the pin on the headroom share, see the note above
    # affordable_for. What is under test here is the tie, not the number.
    edge = threshold_for(2, percent=pool.DEFAULT_HEADROOM_PERCENT)
    tied = pool.plan_pool(
        worker_bytes=WORKER, items=500, ceiling=2, read_available=reader(edge)
    )
    assert tied.workers == 2
    assert tied.bound is pool.Bound.AVAILABLE_MEMORY

    memory_wins = pool.plan_pool(
        worker_bytes=WORKER, items=500, ceiling=2, read_available=reader(edge - 1)
    )
    assert memory_wins.workers == 1
    assert memory_wins.bound is pool.Bound.AVAILABLE_MEMORY


@pytest.mark.parametrize("percent", [1, 25, 50, 75, 99, 100])
def test_no_headroom_setting_ever_affords_more_than_the_reading_itself(percent):
    """A whole-range sweep, because a percentage is the argument somebody changes.

    The property is not the count. It is that the bytes the pool claims never
    exceed the bytes the machine said were available, at any setting, which is
    the invariant a rounding error in either direction would break.
    """
    available = 10 * GIB
    plan = pool.plan_pool(
        worker_bytes=WORKER,
        items=500,
        ceiling=1024,
        headroom_percent=percent,
        read_available=reader(available),
    )
    assert plan.workers * WORKER <= available
    assert plan.workers * WORKER <= max(WORKER, available * percent // 100)


# ---------------------------------------------------------------------------
# The headroom judgement, recorded as a measurement rather than as an opinion
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "platform,expected",
    [("darwin", 50), ("linux", 75), ("win32", 75)],
)
def test_the_headroom_share_is_lower_where_the_reading_is_measurably_worse(platform, expected):
    """Both branches are checked from here, which is why this is a function.

    A conditional expression at module level has an arm that can only run on the
    other machine, and an arm no test can reach is an arm that is wrong the day
    somebody edits it. On darwin the available reading was measured at 91 percent
    inactive queue, which is not all cheaply reclaimable, so the share it is safe
    to claim is lower there than on a platform whose reading means what it says.

    THE EXPECTATIONS ARE LITERALS, which they were not. Both were spelled as the
    constant they were checking, so this test agreed with either share at any
    value and the only real claim in it was the ordering on the last line, which
    every number above fifty satisfies.
    """
    assert pool.default_headroom_percent(platform) == expected
    assert pool.DARWIN_HEADROOM_PERCENT < pool.GENERAL_HEADROOM_PERCENT


def test_the_shipped_default_is_the_one_this_platform_earns():
    assert pool.DEFAULT_HEADROOM_PERCENT == pool.default_headroom_percent(sys.platform)


def test_the_machine_the_kill_happened_on_gets_no_pool_under_the_shipped_rule():
    """The whole judgement, driven at a reading taken off the real machine.

    Measured on the 18 gibibyte machine this product is built on: 5.25 gibibytes
    reported available, of which 4.80 was the inactive queue, while 2.21
    gibibytes of swap were already in use. The old rule, seventy five percent of
    available with no reserve and no gate, turns that into three workers at a one
    gibibyte model, which is the documented kill arriving through new arithmetic.
    The assertion is written against BOTH rules so the test says what changed
    rather than merely what is.
    """
    measured_available = 5 * GIB + 256 * MIB
    measured_swap = 2 * GIB + 215 * MIB
    measured_used_percent = 70.8

    old_rule = measured_available * 75 // 100 // WORKER
    assert old_rule == 3, "the recorded reading no longer reproduces the old rule's answer"

    plan = pool.plan_pool(
        worker_bytes=WORKER,
        items=500,
        ceiling=64,
        read_available=reader(measured_available),
        read_pressure=pressure(
            swap_used_bytes=measured_swap, used_percent=measured_used_percent
        ),
    )
    assert plan.workers == 1
    assert plan.in_process is True
    assert plan.bound is pool.Bound.MEMORY_PRESSURE


@pytest.mark.parametrize(
    "reading,gated",
    [
        (dict(swap_used_bytes=1 * GIB, used_percent=5.0), True),
        (dict(swap_used_bytes=1 * GIB - 1, used_percent=5.0), False),
        (dict(swap_used_bytes=0, used_percent=85.0), True),
        (dict(swap_used_bytes=0, used_percent=84.0), False),
    ],
    ids=["swap-at-the-line", "swap-below", "percent-at-the-line", "percent-below"],
)
def test_the_pressure_gate_bites_at_its_two_lines_and_nowhere_else(reading, gated):
    """Two inputs, two lines, and the edges rather than the middle.

    Either signal alone is enough, because they fail in different directions: the
    swap counter is history the percentage cannot show, and the percentage is a
    present tense the swap counter is slow to reach.

    THE READINGS ARE LITERALS, AND THIS TEST IS THE REASON THEY HAVE TO BE. It
    used to spell them ``DEFAULT_SWAP_PRESSURE_BYTES`` and that minus one, so at
    a threshold of one byte a reading of one byte was still "at the line" and a
    reading of zero was still "below" it, and both cases passed while every
    machine on earth was being refused a pool. That is the self reference that
    let six constants travel. It reads as the more thorough of the two tests of
    this gate and it was covering nothing. What each number means is pinned
    beside its constant, in test_the_swap_threshold_is_a_gibibyte_and_the
    _gibibyte_is_load_bearing and test_the_used_percent_ceiling_is_eighty_five
    _and_the_number_is_load_bearing, and neither of those may be deleted as a
    duplicate of this one.
    """
    plan = pool.plan_pool(
        worker_bytes=WORKER,
        items=500,
        ceiling=64,
        read_available=reader(64 * GIB),
        read_pressure=pressure(**reading),
    )
    if gated:
        assert plan.workers == 1
        assert plan.bound is pool.Bound.MEMORY_PRESSURE
        assert plan.max_tasks_per_child is None
    else:
        assert plan.workers > 1
        assert plan.bound is not pool.Bound.MEMORY_PRESSURE


def test_a_gated_plan_still_reports_the_reading_it_was_gated_despite():
    """The available bytes are not the reason, but they are still the evidence.

    A plan that reported nothing would leave "why did this run go in process on a
    machine with five gigabytes free" unanswerable from the log, which is the
    exact question the gate exists to make answerable.
    """
    plan = pool.plan_pool(
        worker_bytes=WORKER,
        items=500,
        ceiling=64,
        read_available=reader(6 * GIB),
        read_pressure=pressure(swap_used_bytes=3 * GIB),
    )
    assert plan.available_bytes == 6 * GIB
    assert plan.bound is pool.Bound.MEMORY_PRESSURE


@pytest.mark.parametrize(
    "broken_reader",
    [
        lambda: (_ for _ in ()).throw(OSError("no swap statistics on this platform")),
        lambda: None,
        lambda: "under pressure",
        lambda: pool.Pressure(swap_used_bytes=-1, used_percent=5.0),
        lambda: pool.Pressure(swap_used_bytes=True, used_percent=5.0),
        lambda: pool.Pressure(swap_used_bytes=0, used_percent=180.0),
        lambda: pool.Pressure(swap_used_bytes=0, used_percent="busy"),
    ],
    ids=["raises", "none", "text", "negative", "bool", "impossible-percent", "percent-text"],
)
def test_an_unreadable_pressure_reading_does_not_collapse_the_pool(broken_reader):
    """The opposite rule from the available reading, and the difference is deliberate.

    Not knowing how much room there is means not knowing anything, so the answer
    is one worker. Not knowing what the machine is PAYING, while knowing exactly
    how much room there is, still leaves three brakes standing. Collapsing every
    plan to one worker because a secondary signal is unavailable would retire the
    feature to fix a machine nobody has described.
    """
    plan = pool.plan_pool(
        worker_bytes=WORKER,
        items=500,
        ceiling=64,
        read_available=reader(64 * GIB),
        read_pressure=broken_reader,
    )
    assert plan.workers > 1
    assert plan.bound is not pool.Bound.MEMORY_PRESSURE


def test_the_real_pressure_reading_answers_with_two_believable_numbers():
    """The seam is only worth having if the reading behind it is a reading.

    Not asserted against a value, because the value is a property of whatever
    this machine is doing while the suite runs. Asserted against the SHAPE, which
    is what the gate consumes and what a platform returning something else would
    break.
    """
    taken = pool.memory_pressure()
    assert isinstance(taken, pool.Pressure)
    assert isinstance(taken.swap_used_bytes, int) and taken.swap_used_bytes >= 0
    assert 0 <= taken.used_percent <= 100


# ---------------------------------------------------------------------------
# The tuning constants, pinned by what they DO
# ---------------------------------------------------------------------------
#
# EVERY CONSTANT IN THE SIZING MODULE SURVIVED BEING MOVED. The whole set was
# swept one at a time against this suite as it stood after the first fix round,
# and the swap threshold went from a gibibyte to a SINGLE BYTE, the absolute
# reserve went from two gibibytes to one byte, the general headroom went from
# three quarters to all of it, the darwin headroom went from a half to nearly
# three quarters, the used-percent ceiling went from eighty five to a hundred,
# and the recycle budget went from a hundred tasks to one. Every one of those
# left the suite green.
#
# ONE SHAPE PRODUCED ALL OF THEM. The test that looked like it covered a
# constant computed what it expected BY READING THE CONSTANT, so it restated the
# source instead of checking it. ``affordable_for`` and ``threshold_for`` take
# the shipped percent and the shipped reserve, so every boundary they derive
# moves with the number it was supposed to pin. The pressure gate's parameters
# were spelled ``DEFAULT_SWAP_PRESSURE_BYTES`` and ``DEFAULT_SWAP_PRESSURE_BYTES
# - 1``, so at one byte a reading of one byte is still "at the line" and a
# reading of zero is still "below" it, and both cases passed while every machine
# on earth was being refused a pool.
#
# TWO CONSTANTS COULD NOT BE COVERED AT ALL FROM HERE, and that is a second
# shape rather than the same one: ``GENERAL_HEADROOM_PERCENT`` and the windows
# pool limit are both on the arm this platform never executes. A number nothing
# on this machine can reach is a number nothing on this machine can check, so
# both are driven through an argument and through a named platform instead.
#
# So every test below puts a machine on each side of a number and asserts the
# DECISION differs. None of them names a constant on both sides of an equals.


def _workers_for(percent: int) -> int:
    """The pool a hundred gibibytes affords at this headroom, in workers.

    THE FIXTURE IS CHOSEN SO THE COUNT IS THE PERCENT. A hundred gibibytes, no
    reserve and a one gibibyte worker means the count comes out equal to the
    share, so a percent moved by one moves the answer by one and the assertion
    can be a literal. The platform limit is taken out of the way because this
    question is about the arithmetic and windows would otherwise cap it at 61.
    """
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(pool, "platform_worker_ceiling", lambda: None)
        plan = pool.plan_pool(
            worker_bytes=1 * GIB,
            items=10_000,
            ceiling=10_000,
            headroom_percent=percent,
            reserve_bytes=0,
            read_available=reader(100 * GIB),
        )
    return plan.workers


def test_the_general_headroom_claims_three_quarters_of_what_is_left():
    """Seventy five, pinned by the pool it produces rather than by its spelling.

    THE ARM THIS MACHINE NEVER RUNS. On darwin the shipped default is the darwin
    number and the general one is never reached by any default-configuration
    call, so it moved from seventy five to a hundred with the whole suite green.
    The only thing asserted about it was that it was LARGER than the darwin
    share, which every number above fifty satisfies.
    """
    assert _workers_for(pool.GENERAL_HEADROOM_PERCENT) == 75


def test_the_darwin_headroom_claims_half_because_half_is_what_was_measured():
    """Fifty, pinned the same way. It moved to seventy four with the suite green.

    Half is the share that survives the measured split between the inactive
    queue and free memory being as bad as it was measured to be. "Smaller than
    the general share" is not that claim, it is a fact about two numbers, and it
    was the only thing under test.
    """
    assert _workers_for(pool.DARWIN_HEADROOM_PERCENT) == 50


def test_the_absolute_reserve_is_two_gibibytes_of_the_reading_that_was_never_ours():
    """The reserve, pinned at the reading where a machine starts affording anything.

    Two gibibytes is the working set of a desktop with a browser and an editor
    open, measured rather than guessed. Driven at a hundred percent headroom so
    the percent is out of the way and the subtraction is the only thing being
    measured: a machine holding exactly one worker's worth beyond the reserve
    affords that worker, and one byte short of it affords none. At one byte of
    reserve the first case affords two, and at a petabyte the second case is the
    only case there is.
    """
    common = dict(
        worker_bytes=WORKER,
        items=500,
        ceiling=64,
        headroom_percent=100,
        reserve_bytes=pool.DEFAULT_MEMORY_RESERVE_BYTES,
    )
    affords_one = pool.plan_pool(**common, read_available=reader(2 * GIB + WORKER))
    affords_none = pool.plan_pool(**common, read_available=reader(2 * GIB + WORKER - 1))
    assert affords_one.workers == 1
    assert affords_one.bound is pool.Bound.AVAILABLE_MEMORY
    assert affords_none.bound is pool.Bound.INSUFFICIENT_MEMORY


def test_the_default_ceiling_is_two_because_two_is_what_survived_a_real_run():
    """The shipped ceiling, pinned by the pool a roomy machine actually gets.

    The test beside this one asserts the count EQUALS the constant, which it
    does at any value, so the ceiling moved to 1024 with only two deaths and
    neither of them was that one.
    """
    assert affordable_for(64 * GIB) > 2, "the reading no longer leaves the ceiling binding"
    plan = pool.plan_pool(worker_bytes=WORKER, items=500, read_available=reader(64 * GIB))
    assert plan.workers == 2
    assert plan.bound is pool.Bound.CEILING


@pytest.mark.parametrize(
    "swap,gated",
    [
        (512 * MIB, False),
        (1 * GIB - 1, False),
        (1 * GIB, True),
        (4 * GIB, True),
    ],
    ids=["stale-swap", "one-byte-under", "a-full-gibibyte", "deep-in-swap"],
)
def test_the_swap_threshold_is_a_gibibyte_and_the_gibibyte_is_load_bearing(swap, gated):
    """THE RECORDED DEFECT. This number moved to ONE BYTE with the suite green.

    The readings here are literals rather than the constant and its predecessor,
    which is the whole difference. Half a gibibyte is an ordinary darwin machine
    that was briefly busy last week: the platform's swap counter is sticky, so
    pages counted once stay counted after they are read back, and such a machine
    must still get a pool or the feature is retired on every machine that has
    ever been busy. A full gibibyte is a machine that has already been asked for
    more memory than it has, and it must not.
    """
    plan = pool.plan_pool(
        worker_bytes=WORKER,
        items=500,
        ceiling=64,
        read_available=reader(64 * GIB),
        read_pressure=pressure(swap_used_bytes=swap),
    )
    assert (plan.bound is pool.Bound.MEMORY_PRESSURE) is gated
    assert (plan.workers == 1) is gated


@pytest.mark.parametrize(
    "used,gated",
    [(60.0, False), (84.9, False), (85.0, True), (99.0, True)],
    ids=["a-working-machine", "just-under", "at-the-line", "reclaiming-hard"],
)
def test_the_used_percent_ceiling_is_eighty_five_and_the_number_is_load_bearing(used, gated):
    """Eighty five is where the platform reclaims to serve ordinary allocations.

    It moved to a hundred with the suite green, for the same reason the swap
    threshold moved to one byte: the only test of it took both of its readings
    from the constant, so the constant could not disagree with them. Above this
    line the next worker's model is paid for out of somebody else's resident
    pages rather than out of room.
    """
    plan = pool.plan_pool(
        worker_bytes=WORKER,
        items=500,
        ceiling=64,
        read_available=reader(64 * GIB),
        read_pressure=pressure(used_percent=used),
    )
    assert (plan.bound is pool.Bound.MEMORY_PRESSURE) is gated


@pytest.mark.parametrize(
    "items,generations",
    [(10_000, 50), (500, 3)],
    ids=["a-ten-thousand-track-folder", "an-ordinary-folder"],
)
def test_the_recycle_budget_retires_a_child_occasionally_rather_than_constantly(
    items, generations
):
    """A hundred tasks per child, pinned by how often a real folder retires one.

    Each retirement buys a fresh interpreter and a fresh model load, so this
    number is a trade rather than a preference. At one task per child a ten
    thousand track folder pays five thousand model loads, and at a million it
    pays none at all and the allocator is bounded by nothing. The counts here
    are literals, which is what the test beside them was missing: it asserted
    that the plan CARRIES the constant, which the plan does at any value.
    """
    plan = pool.plan_pool(
        worker_bytes=WORKER, items=items, ceiling=2, read_available=reader(64 * GIB)
    )
    assert plan.workers == 2
    assert plan.generations == generations


#: What the load this deadline waits for costs on the machine it was written for.
#:
#: The 300 megabyte model named in ``_probe_entry``, read off a cold and
#: fragmented spinning platter at the few megabytes a second one of those
#: sustains, is about a minute of reading before the spawn, the interpreter, the
#: framework import and the deserialization are paid on top. Written here rather
#: than read out of the module, because a bound that reads its own subject out of
#: the thing it is bounding is not a bound.
#:
#: USED IN BOTH DIRECTIONS BELOW, and that is the whole reason this number is not
#: free. A reference cost that only ever sets a floor can be driven to nothing
#: with the suite green: measured, this constant moved from 60 to 1 and killed
#: nothing, which took the shipped deadline's entire lower bound to one and a
#: half seconds. It now sets the ceiling as well, so shrinking it collapses the
#: band under the deadline the module ships and growing it lifts the floor over
#: the same number. There is exactly one narrow range of reference loads that
#: admits a hundred and twenty seconds, and this sits in it.
_A_COLD_MODEL_LOAD_SECONDS = 60.0

#: The least generous a deadline may be, as a multiple of the load it waits for.
#: At exactly the load it is a coin flip that pays out as the floor, and the
#: floor sizes the whole run; at twice it a machine twice as slow as a cold
#: fragmented platter still answers.
_DEADLINE_FLOOR_IN_LOADS = 2.0

#: The most generous it may be, in the same units. Past this the wait has stopped
#: buying a slow machine anything, because nothing is that slow, and what it buys
#: instead is a caller who cannot tell a deadline from the hang it exists to end.
_DEADLINE_CEILING_IN_LOADS = 5.0


def test_the_probe_deadline_the_module_ships_outlasts_the_load_it_waits_for():
    """A hundred and twenty seconds, pinned as a band because a wait cannot be waited.

    The lower half of this is already covered by the probe that really spawns: a
    deadline under a spawn and an import reports the floor for a machine that
    would have answered. The upper half cannot be driven end to end without a
    test that waits the deadline out, so what is pinned instead is the promise
    the docstring makes, that every failure returns the floor and a loader that
    never returns is a failure. That promise is only kept if the wait is finite
    and short enough that a run survives it.

    THE LOWER EDGE WAS HALF A MINUTE AND THAT WAS NOT A BOUND, it was a formality.
    Measured: the shipped 120 moved to 60 and killed nothing in the suite, so a
    deadline set at exactly what a cold load costs passed as readily as one set
    at twice it. That is the failure this constant has: a probe cut off mid load
    reports the floor, the floor sizes the whole run, and the run looks fine.

    BOTH EDGES ARE MULTIPLES OF THE SAME REFERENCE LOAD, which is what the
    version before this one got wrong in a subtler way. It bounded the deadline
    below by a multiple and above by the literal 600, so the reference load
    carried the floor alone and could be driven to one second with the suite
    green, and the literal ceiling could be driven to six thousand with the same
    result. Two edges in the same units leave no such move: shrink the reference
    and the ceiling falls under the shipped deadline, grow it and the floor rises
    over it, loosen the deadline in either direction and it leaves the band.
    """
    given: list[float] = []

    def capture(loader, *, timeout_seconds):
        given.append(timeout_seconds)
        raise RuntimeError("the probe was not run here; only its deadline was read")

    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(pool, "_spawned_probe", capture)
        assert pool.measure_worker_bytes(_nothing, floor_bytes=7) == 7
    assert given, "measure_worker_bytes did not reach the probe at all"
    assert given[0] == pool.DEFAULT_PROBE_TIMEOUT_SECONDS, (
        "the deadline the probe was given is not the one the module ships"
    )
    assert given[0] >= _DEADLINE_FLOOR_IN_LOADS * _A_COLD_MODEL_LOAD_SECONDS, (
        f"the shipped probe deadline is {given[0]} seconds against a cold model load "
        f"that costs about {_A_COLD_MODEL_LOAD_SECONDS}; a deadline that close to the "
        f"thing it waits for reports the floor for every machine on the slow side of "
        f"ordinary, and the floor sizes the whole run"
    )
    assert given[0] <= _DEADLINE_CEILING_IN_LOADS * _A_COLD_MODEL_LOAD_SECONDS, (
        f"the shipped probe deadline is {given[0]} seconds against a cold model load "
        f"that costs about {_A_COLD_MODEL_LOAD_SECONDS}; past five times what it waits "
        f"for the wait has stopped buying a slow machine anything and become a hang a "
        f"caller cannot tell from one"
    )


def test_every_probe_deadline_default_names_the_constant_rather_than_repeating_it():
    """The identity assertion above, made able to fail, over the source that decides it.

    ``given[0] == pool.DEFAULT_PROBE_TIMEOUT_SECONDS`` compares the deadline the
    probe received against the constant it came from, and there is exactly one
    number in play. It holds at any value, and it holds equally if a signature
    stops naming the constant and writes today's value as a literal instead.
    Measured: that assertion removed on its own killed nothing.

    A DEFAULT ARGUMENT IS BOUND ONCE, AT IMPORT, which is why this is a guard over
    the source and not a monkeypatch. Moving the module constant at runtime moves
    nothing, in either spelling, so the runtime assertion cannot tell a signature
    that reads the constant from one that froze its value. The syntax tree can:
    the default is either the NAME or it is a number somebody typed, and a number
    somebody typed is a second deadline that stops following the first the day it
    changes, with the whole band above still green.

    A SWEEP AND NOT A LIST OF NAMES, which is what the version before this one
    got wrong at the exact object it was added to close. It asserted over
    ``{"measure_worker_bytes", "_spawned_probe"}``, two names it was handed, so a
    THIRD entry point was invisible to it. Measured: adding

        def measure_worker_bytes_quickly(
            loader, *, floor_bytes, timeout_seconds: float = 120.0,
        ) -> int:

    to this module gave a full green suite and killed nothing, and that signature
    is the precise defect the paragraph above names. A guard that reports on the
    names it was given reports absence as evidence of absence. Every function in
    the module is walked instead, and the only thing this test is told is which
    two must still be found.

    FOUR WAYS TO SPELL A SECOND DEADLINE, and all four are refused. The default
    can be a literal; it can be an alias, an arithmetic no-op or a conversion
    wrapped around the constant, none of which a runtime comparison can see; the
    parameter can lose its default so every caller spells the number instead; or
    it can leave keyword only, where a positional deadline is set by accident.
    The CALL SITES are swept for the same reason: the module ships 120.0 today,
    so a call passing the literal 120.0 would satisfy every runtime assertion in
    this file while being a second deadline that stops following the first.
    """
    documented = "DEFAULT_PROBE_TIMEOUT_SECONDS"
    parameter = "timeout_seconds"
    must_carry_it = {"measure_worker_bytes", "_spawned_probe"}
    tree = ast.parse(POOL_SOURCE)
    defaults: dict[str, str] = {}
    without_a_default: set[str] = set()
    not_keyword_only: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            continue
        arguments = node.args
        for name, default in zip(
            [argument.arg for argument in arguments.kwonlyargs],
            arguments.kw_defaults,
            strict=True,
        ):
            if name != parameter:
                continue
            if default is None:
                without_a_default.add(node.name)
            else:
                defaults[node.name] = ast.unparse(default)
        positional = [*arguments.posonlyargs, *arguments.args]
        if any(argument.arg == parameter for argument in positional):
            not_keyword_only.add(node.name)
    carrying = set(defaults) | without_a_default | not_keyword_only
    assert must_carry_it <= carrying, (
        f"{sorted(must_carry_it - carrying)} no longer takes a {parameter} at all, so "
        f"this guard now sweeps a module with nothing in it to find; a deadline that "
        f"left the signature did not stop existing, it moved somewhere this cannot see"
    )
    assert not_keyword_only == set(), (
        f"{sorted(not_keyword_only)} takes {parameter} positionally; a deadline that "
        f"can be passed by position is one a caller sets by counting arguments, and "
        f"the constant it should have named is then never mentioned at the call at all"
    )
    assert without_a_default == set(), (
        f"{sorted(without_a_default)} takes {parameter} with no default, so every "
        f"caller now spells the deadline itself; that is more places for a frozen "
        f"number to live rather than fewer, and none of them is this constant"
    )
    wrong = {name: spelling for name, spelling in defaults.items() if spelling != documented}
    assert wrong == {}, (
        f"a probe deadline default is {wrong} rather than the module constant "
        f"{documented}; a signature that repeats the value instead of naming it is a "
        f"second deadline, and a default argument is bound once at import, so nothing "
        f"at runtime can tell the two apart"
    )
    passed_in: list[tuple[str, str]] = [
        (ast.unparse(node.func), ast.unparse(keyword.value))
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        for keyword in node.keywords
        if keyword.arg == parameter
    ]
    assert passed_in, (
        f"no call in this module passes {parameter} to anything, so the sweep over "
        f"call sites has nothing to check; the probe that runs the deadline is reached "
        f"through one, and a sweep that finds none is measuring the wrong module"
    )
    frozen = [pair for pair in passed_in if pair[1] not in {documented, parameter}]
    assert frozen == [], (
        f"a call passes {frozen} as its deadline rather than forwarding {parameter} or "
        f"naming {documented}; the module ships 120.0 today, so a literal here matches "
        f"the constant at runtime and stops following it the day the constant moves"
    )


def test_the_windows_pool_limit_is_the_interpreters_own_and_falls_back_to_sixty_one():
    """Both arms of a function neither of which runs on the machine that ships it.

    The literal in the fallback is unreachable on every machine this product is
    developed on, so it moved to one with the suite green while the test beside
    it asserted only that the answer is None off windows. Driven by naming the
    platform and by taking the interpreter's own number away.
    """
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(sys, "platform", "win32")
        patch.setattr(_process_pool, "_MAX_WINDOWS_WORKERS", 32, raising=False)
        assert pool.platform_worker_ceiling() == 32
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(sys, "platform", "win32")
        patch.delattr(_process_pool, "_MAX_WINDOWS_WORKERS", raising=False)
        assert pool.platform_worker_ceiling() == 61
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(sys, "platform", "win32")
        patch.setattr(_process_pool, "_MAX_WINDOWS_WORKERS", 0, raising=False)
        assert pool.platform_worker_ceiling() == 61


# ---------------------------------------------------------------------------
# Affording exactly one, and affording none, which are two different machines
# ---------------------------------------------------------------------------


def test_a_machine_that_affords_exactly_one_worker_says_so():
    # Derived, and NOT the pin on the headroom share, see the note above
    # affordable_for. What is under test here is the bound, not the number.
    edge = threshold_for(1, percent=pool.DEFAULT_HEADROOM_PERCENT)
    plan = pool.plan_pool(
        worker_bytes=WORKER, items=500, ceiling=64, read_available=reader(edge)
    )
    assert plan.workers == 1
    assert plan.bound is pool.Bound.AVAILABLE_MEMORY


def test_a_machine_that_affords_none_is_not_the_same_machine_and_does_not_say_it_is():
    """The argument the module makes for MEMORY_UNREADABLE, applied where it was not.

    A machine that affords exactly one worker is a plan working. A machine that
    affords none and is getting one anyway is R23 unenforceable: the work still
    runs here and still allocates the full per-worker cost, and nothing can stop
    it. Folding those into one value hides the second one exactly as thoroughly
    as folding an unreadable machine into a tight one would have, which is the
    reason this module gives for keeping that one separate.
    """
    # Derived, and NOT the pin on the headroom share, see the note above
    # affordable_for. What is under test here is the two bounds, not the number.
    edge = threshold_for(1, percent=pool.DEFAULT_HEADROOM_PERCENT)
    affords_one = pool.plan_pool(
        worker_bytes=WORKER, items=500, ceiling=64, read_available=reader(edge)
    )
    affords_none = pool.plan_pool(
        worker_bytes=WORKER, items=500, ceiling=64, read_available=reader(edge - 1)
    )
    assert affords_one.workers == affords_none.workers == 1
    assert affords_one.bound is not affords_none.bound
    assert affords_none.bound is pool.Bound.INSUFFICIENT_MEMORY
    assert affords_one.explain() != affords_none.explain()


# ---------------------------------------------------------------------------
# The other two bounds, and the refusals
# ---------------------------------------------------------------------------


def test_the_item_count_bounds_the_pool_so_no_child_is_started_with_nothing_to_do():
    plan = pool.plan_pool(
        worker_bytes=WORKER, items=3, ceiling=64, read_available=reader(64 * GIB)
    )
    assert plan.workers == 3
    assert plan.bound is pool.Bound.WORK_ITEMS


def test_no_work_at_all_plans_one_in_process_worker_rather_than_zero():
    """Zero items must not become zero workers. A pool of zero never returns."""
    plan = pool.plan_pool(
        worker_bytes=WORKER, items=0, ceiling=64, read_available=reader(64 * GIB)
    )
    assert plan.workers == 1
    assert plan.in_process is True
    assert plan.bound is pool.Bound.WORK_ITEMS


def test_one_item_runs_in_process():
    plan = pool.plan_pool(
        worker_bytes=WORKER, items=1, ceiling=64, read_available=reader(64 * GIB)
    )
    assert plan.in_process is True


def test_the_platform_limit_bounds_the_pool_where_the_platform_has_one():
    """Windows refuses a pool above a fixed width, and it refuses by raising.

    That makes it a sizing question rather than a runtime one. The machine that
    computes a width above the limit is a large one with plenty of memory and a
    raised ceiling, which is exactly where an unexplained ValueError out of the
    executor's constructor is least expected and hardest to read.

    Driven at the seam rather than by pretending to be another operating system,
    because what is being asserted is that the limit REACHES the arithmetic.
    """
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(pool, "platform_worker_ceiling", lambda: 61)
        plan = pool.plan_pool(
            worker_bytes=1 * MIB,
            items=10_000,
            ceiling=1024,
            read_available=reader(64 * GIB),
        )
    assert plan.workers == 61
    assert plan.bound is pool.Bound.PLATFORM_LIMIT


def test_a_platform_with_no_limit_contributes_nothing_to_the_arithmetic():
    """Absent, never a huge sentinel. A sentinel that always loses is never checked."""
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(pool, "platform_worker_ceiling", lambda: None)
        plan = pool.plan_pool(
            worker_bytes=1 * GIB, items=10_000, ceiling=1024, read_available=reader(64 * GIB)
        )
    assert plan.workers == affordable_for(64 * GIB)
    assert plan.bound is pool.Bound.AVAILABLE_MEMORY


def test_the_platform_limit_is_the_real_one_for_the_platform_running_this():
    """The seam is only worth having if the value behind it is right.

    Read from the interpreter where it publishes one, so a build that lowers the
    number lowers this with it rather than leaving a stale literal that is wrong
    in the direction that raises.
    """
    limit = pool.platform_worker_ceiling()
    if sys.platform == "win32":
        assert limit == 61
    else:
        assert limit is None


@pytest.mark.parametrize(
    "arguments",
    [
        {"worker_bytes": 0},
        {"worker_bytes": -1},
        {"ceiling": 0},
        {"ceiling": -4},
        {"headroom_percent": 0},
        {"headroom_percent": 101},
        {"reserve_bytes": -1},
        {"swap_pressure_bytes": -1},
        {"used_percent_ceiling": 0},
        {"used_percent_ceiling": 101},
        {"items": -1},
        {"max_tasks_per_child": 0},
        {"max_tasks_per_child": -10},
    ],
)
def test_an_impossible_request_refuses_rather_than_being_repaired(arguments):
    """Clamping a bad argument hides the caller that produced it.

    A ceiling of zero silently becoming one is a configuration nobody ever
    notices is wrong, and a headroom of one hundred and ten percent silently
    becoming one hundred is a machine sized against memory it does not have.
    """
    request = {"worker_bytes": WORKER, "items": 10, "read_available": reader(8 * GIB)}
    request.update(arguments)
    with pytest.raises(ValueError):
        pool.plan_pool(**request)


def test_a_plan_reports_what_it_measured_and_what_decided_it():
    plan = pool.plan_pool(worker_bytes=WORKER, items=500, read_available=reader(16 * GIB))
    assert plan.available_bytes == 16 * GIB
    assert plan.worker_bytes == WORKER
    assert plan.items == 500
    assert "2 workers" in plan.explain()
    assert pool.BOUND_PHRASES[pool.Bound.CEILING] in plan.explain()


def test_a_plan_of_one_worker_explains_itself_as_in_process():
    plan = pool.plan_pool(worker_bytes=WORKER, items=500, read_available=reader(2 * GIB))
    assert plan.explain().startswith("in process")


def test_every_bound_has_a_phrase():
    """Derived by iterating the enum, so the next bound cannot arrive unexplained (P3)."""
    assert set(pool.BOUND_PHRASES) == set(pool.Bound)


def test_the_bound_phrase_table_has_no_duplicate_key():
    """A key written twice collapses at parse time and every runtime test is blind to it.

    This repository has already shipped that shape once with a green suite. The
    literal is parsed and counted against the runtime mapping, which is the only
    check that can see it.
    """
    literal = None
    for node in ast.walk(ast.parse(POOL_SOURCE)):
        if isinstance(node, ast.AnnAssign) and getattr(node.target, "id", "") == "BOUND_PHRASES":
            literal = node.value
    assert literal is not None, "BOUND_PHRASES is no longer a module-level annotated assignment"
    written = [ast.unparse(key) for key in literal.args[0].keys]
    duplicates = sorted({key for key in written if written.count(key) > 1})
    assert not duplicates, f"written twice and collapsed at parse time: {duplicates}"
    assert len(written) == len(pool.BOUND_PHRASES)


# ---------------------------------------------------------------------------
# The plan carries the item count, which is what made the deadlock unseeable
# ---------------------------------------------------------------------------


def test_a_plan_carries_the_item_count_it_was_decided_for():
    """The field whose absence made the ratio impossible to check from a plan.

    The dangerous ratio for any recycling pool is items against workers times
    tasks per child. A plan that recorded two of those three numbers could not be
    checked by anybody holding it, which included every test in this file and
    every future caller. It is a field now.
    """
    plan = pool.plan_pool(
        worker_bytes=WORKER, items=4321, ceiling=4, read_available=reader(64 * GIB)
    )
    assert plan.items == 4321
    assert plan.tasks_per_generation == plan.workers * plan.max_tasks_per_child


@pytest.mark.parametrize(
    "items,generations",
    [(0, 0), (1, 0), (2, 1), (8, 1), (9, 2), (16, 2), (17, 3)],
)
def test_a_plan_says_how_many_generations_of_children_its_work_takes(items, generations):
    """Eight items per generation here: four workers spending two tasks each.

    The item count is also one of the three bounds, so a small enough count
    plans a narrower pool and a generation is smaller with it. That is the point
    rather than a complication: the number of generations is a property of the
    plan as a whole, not of a constant somebody has to keep in step with it.
    """
    plan = pool.plan_pool(
        worker_bytes=WORKER,
        items=items,
        ceiling=4,
        max_tasks_per_child=2,
        read_available=reader(64 * GIB),
    )
    assert plan.generations == generations


def test_an_in_process_plan_runs_no_generations_at_all():
    plan = pool.plan_pool(worker_bytes=WORKER, items=500, read_available=reader(2 * GIB))
    assert plan.in_process is True
    assert plan.tasks_per_generation is None
    assert plan.generations == 0


def test_a_pool_that_never_retires_a_child_is_one_generation():
    plan = pool.plan_pool(
        worker_bytes=WORKER,
        items=10_000,
        ceiling=4,
        max_tasks_per_child=None,
        read_available=reader(64 * GIB),
    )
    assert plan.tasks_per_generation is None
    assert plan.generations == 1


# ---------------------------------------------------------------------------
# The probe
# ---------------------------------------------------------------------------


def test_the_probe_reports_what_it_measured_when_that_is_larger_than_the_floor():
    measured = pool.measure_worker_bytes(
        lambda: None, floor_bytes=1 * GIB, runner=lambda _loader: 3 * GIB
    )
    assert measured == 3 * GIB


def test_the_probe_never_reports_below_the_declared_floor():
    """The floor is a floor, not a fallback, and conflating the two undersizes.

    A probe reads resident set the instant loading finishes. The worker then
    decodes, infers and builds results, and every one of those allocates. Trusting
    the measurement alone means sizing a pool against a worker that has not
    started working yet.
    """
    measured = pool.measure_worker_bytes(
        lambda: None, floor_bytes=1 * GIB, runner=lambda _loader: 300 * MIB
    )
    assert measured == 1 * GIB


@pytest.mark.parametrize(
    "outcome",
    [0, -1, None, "300MB", 2.5, True],
    ids=["zero", "negative", "none", "text", "float", "bool"],
)
def test_a_probe_that_answers_with_nonsense_returns_the_floor(outcome):
    measured = pool.measure_worker_bytes(
        lambda: None, floor_bytes=512 * MIB, runner=lambda _loader: outcome
    )
    assert measured == 512 * MIB


def test_a_probe_that_fails_returns_the_floor_rather_than_propagating():
    """A machine with no model installed must still get a plan, not a traceback.

    The loader is the caller's code and it can fail for reasons that have nothing
    to do with memory. None of them is a reason to guess high on the count.
    """

    def broken(_loader):
        raise RuntimeError("no checkpoint on this machine")

    assert pool.measure_worker_bytes(lambda: None, floor_bytes=777, runner=broken) == 777


def test_a_probe_floor_below_one_byte_refuses():
    with pytest.raises(ValueError):
        pool.measure_worker_bytes(lambda: None, floor_bytes=0, runner=lambda _loader: 1)


def test_a_probe_with_no_time_to_answer_refuses_rather_than_reporting_the_floor():
    """A timeout of zero is a caller mistake, not a machine that failed.

    Repairing it to something small would run a probe nobody asked for, and
    returning the floor would report a measurement that was never attempted.
    """
    with pytest.raises(ValueError):
        pool.measure_worker_bytes(lambda: None, floor_bytes=1, timeout_seconds=0)


def test_a_measured_worker_size_flows_into_the_plan_it_was_taken_for():
    """The two halves are one decision, so they are exercised as one.

    Measuring and then sizing against a different number is a defect that neither
    half's own test can see.
    """
    worker_bytes = pool.measure_worker_bytes(
        lambda: None, floor_bytes=512 * MIB, runner=lambda _loader: 2 * GIB
    )
    plan = pool.plan_pool(
        worker_bytes=worker_bytes, items=500, ceiling=64, read_available=reader(16 * GIB)
    )
    assert plan.worker_bytes == 2 * GIB
    assert plan.workers == affordable_for(16 * GIB, worker_bytes=2 * GIB)


# ---------------------------------------------------------------------------
# Real processes. Only where nothing else can answer the question.
# ---------------------------------------------------------------------------

#: Set by the initializer in whichever process is doing the work. The module
#: global IS the pattern a real pool uses for a loaded model, so the recycle test
#: below exercises the shape it will actually be used in.
_LOADED: dict[str, str] = {}


def _load(tag: str) -> None:
    """A stand-in for loading a model, cheap enough to run in a test.

    The identity recorded beside the tag is what makes "this child was replaced"
    provable rather than probable. A process identifier alone is not an identity:
    the platform is free to hand a retired child's number to its replacement, and
    a test that read a pid twice could not tell a reused number from a surviving
    worker. This value is written ONCE per interpreter, by this initializer, so
    two readings that match came from one process that was never replaced.
    """
    _LOADED["tag"] = tag
    _LOADED["identity"] = f"{os.getpid()}:{time.monotonic_ns()}"


def _report(index: int) -> tuple[int, int, str, str]:
    """Which item, which process, what it was initialized with, and which life it was."""
    return (
        index,
        os.getpid(),
        _LOADED.get("tag", "uninitialized"),
        _LOADED.get("identity", "uninitialized"),
    )


def _raise_on_the_third_item(index: int) -> int:
    """Raises on two of six items, so which exception surfaces is a real question."""
    if index in (2, 4):
        raise ValueError(f"item {index} could not be analysed")
    return index


#: WELL ABOVE THE ALLOCATOR CLIFF, and the number is the whole point of the
#: fixture. Measured on this machine: a child that allocated 32, 96 or 112
#: mebibytes and freed it before the reading still showed the whole allocation,
#: because libmalloc retains freed blocks up to about 112 mebibytes. At 128 and
#: above it returns them to the kernel immediately, and the same measurement read
#: about zero. The earlier fixture was 96 mebibytes, which is under the cliff, so
#: the probe's own test passed on the one side of the boundary where a broken
#: probe still looks like a working one.
_PROBE_FIXTURE_BYTES = 256 * MIB


def _allocate_the_probe_fixture() -> object:
    """A stand-in for a model: memory that is genuinely resident, not just reserved."""
    return bytearray(_PROBE_FIXTURE_BYTES)


def test_the_probe_fixture_sits_above_the_allocator_retention_cliff():
    """The fixture size is the only reason the probe's own test is able to fail.

    Stated as an assertion rather than left in a comment, because the size is a
    tuning constant of this file and it moved to a single mebibyte with the
    suite green: the test that uses it derives its threshold BY READING IT, so
    it agrees with any value at all. What the size actually buys is that the
    probe's own test can tell a probe that holds the model across the reading
    from one that frees it first, and under the cliff it cannot.

    The literal here is a measurement rather than a second tuning constant.
    Measured on this machine, the platform allocator retains freed blocks up to
    about 112 mebibytes and hands anything from 128 upwards straight back to the
    kernel, which is why a 96 mebibyte fixture passed over a probe that measured
    nothing at all for every model this module exists to size.
    """
    assert _PROBE_FIXTURE_BYTES >= 128 * MIB


def _nothing() -> None:
    """A loader that loads nothing, for the baseline half of the probe measurement."""
    return None


def _still_running_when_the_deadline_passes() -> object:
    """A loader that has not finished when the probe gives up on it.

    EIGHT SECONDS RATHER THAN AN HOUR, and the difference is not cosmetic. The
    deadline this is driven at is one second, so any sleep past that exercises
    exactly the same path. What the length changes is what a REGRESSION costs:
    if the reaping ever stops working, this child is what is left behind, and a
    child left behind is joined by the interpreter's own shutdown, so an hour
    long loader turns one failing assertion into a suite that never exits. That
    is the same shape as the deadlock this unit already had to test around,
    arrived at from the test side.
    """
    time.sleep(8)
    return None


#: The exit code a child of this file's own making reports when it unwound on a
#: terminate. An arbitrary number, and the arbitrariness is the point: no signal
#: produces it, so a child that reports it got there through its own handler and
#: a child that was killed outright cannot fake it.
_TERMINATED_CLEANLY = 77

#: How long this file's cooperative child spends releasing what it holds before
#: it reports that it unwound.
#:
#: THE ONE NUMBER THAT MAKES THE REAPING BUDGET MEAN ANYTHING. This child used to
#: call ``os._exit`` on the first line of its handler, which is a release that
#: costs nothing, and a release that costs nothing cannot tell a one second
#: budget from a one millisecond one. Measured: with an instant handler,
#: ``_PROBE_REAP_SECONDS`` moved from 1.0 to 0.001 and the whole suite stayed
#: green, so the ladder's order was pinned and the budget that gives its first
#: rung any chance to work was not.
#:
#: A real probe child is one that has just finished loading a model, and letting
#: go of one is not instant. Four tenths of a second stands in for that: long
#: enough that a budget a tidier would plausibly pick cannot cover it, and small
#: enough against the shipped budget that the assertion has more slack than it
#: needs on a loaded machine.
#:
#: FAITHFUL IN COST AND NOT IN KIND, and the difference is worth writing down
#: rather than leaving for somebody to discover. A real release of a 300 megabyte
#: model is allocator and kernel work, and work DILATES under contention. A sleep
#: does not, and that half is measured rather than assumed: over 330 timed legs
#: in five load regimes, forty spinners at load average 49.8 moved a single
#: sample's maximum from 0.4111 to 0.4112 seconds and two gibibytes of churn
#: moved it to 0.4121. So this fixture reproduces the DURATION a release costs
#: and not its sensitivity to load.
#:
#: THE MEASUREMENT IS LOAD SENSITIVE EVEN THOUGH THE SLEEP IS NOT, and an earlier
#: version of this note claimed otherwise. The parent has to be SCHEDULED to
#: observe the child's exit, and it is not always scheduled promptly. Measured
#: across those same five regimes, per regime standard deviation rose from 0.0033
#: seconds idle to 0.0118 with the sampler itself at ``nice -n 19`` behind thirty
#: two spinners, and that one regime produced a leg of 0.4926 against a minimum
#: of 0.4013, a spread of 91.3 milliseconds rather than the 9.8 the earlier note
#: recorded. Nothing about the child changed; the sampler simply did not run when
#: the child died.
#:
#: SO THE BOUND IS NOT STATED AGAINST A SINGLE SAMPLE. That excursion is exactly
#: what put the old form seven milliseconds from a red suite while its own note
#: claimed sixty eight. See ``_RELEASE_SAMPLES``: the leg is timed several times
#: and read as a MINIMUM, which drops the parent's wakeup term, and the tolerance
#: around it is forty one milliseconds below and ninety one above against an
#: eight millisecond envelope.
#:
#: THE SLEEP IS STILL THE RIGHT TRADE, chosen rather than settled for. A fixture
#: that really allocated and freed three hundred megabytes would model the kind as
#: well as the cost, and it would do it by making the one number these tests
#: assert on a function of what every other process on the machine is doing. The
#: bound would then fail on a busy runner while the shipped budget was fine, which
#: is a flaky suite bought with realism, and this repository has no conditional
#: skip to hide it behind.
_RELEASE_SECONDS = 0.4


def _unwinds_on_a_terminate(ready) -> None:
    """A probe child that exits cleanly when it is ASKED to stop, and takes time to.

    The first rung of the reaping ladder is a terminate, and a terminate is only
    worth having if a child can act on one. This is that child. It installs a
    handler, says it is armed, and then sleeps well past every deadline the
    reaping uses, so the ONLY thing that can end it is the ladder and the exit
    code says which rung did.

    THE HANDLER SPENDS TIME BEFORE IT REPORTS, and that is not decoration. The
    exit code alone proves the handler ran; it proves nothing about whether the
    child was given long enough to finish. Sleeping the release out first means
    the exit code now answers both, because a budget too short to cover the
    release turns this child's 77 into a negative signal number.
    """

    def unwind(_signal, _frame) -> None:
        # Standing in for releasing a loaded model: the child is not gone until
        # it has finished letting go, and only then is the exit code earned.
        time.sleep(_RELEASE_SECONDS)
        os._exit(_TERMINATED_CLEANLY)

    signal.signal(signal.SIGTERM, unwind)
    ready.send(True)
    ready.close()
    time.sleep(8)


def _ignores_a_terminate(ready) -> None:
    """A probe child that will not unwind, which is the case the backstop exists for.

    A worker deep inside a native model load does not run Python's signal handler
    until it comes back up, and one that is wedged does not come back up. This is
    that child made deterministic: the terminate is ignored outright, so the only
    thing left that can end it is the kill.
    """
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    ready.send(True)
    ready.close()
    time.sleep(8)


class _WatchedChild:
    """One probe child, wrapped so each rung of the reaping ladder is visible.

    ``_reap`` takes anything that answers the four calls, so a wrapper is the
    honest way to watch it. The escalation is a SEQUENCE, and a sequence cannot
    be read off the process table after the fact: by the time the call returns
    the child is gone either way.

    THE EXIT CODE IS TAKEN AT THE MOMENT OF CLOSING, because a closed process
    object refuses to report one and closing is the last thing the ladder does.
    That also makes the close itself observable, which nothing else here would.
    """

    def __init__(self, process) -> None:
        self.process = process
        self.rungs: list[str] = []
        self.join_seconds: list[float] = []
        self.exitcode: int | None = None
        self.closed = False

    def join(self, timeout=None) -> None:
        self.rungs.append("join")
        started = time.monotonic()
        self.process.join(timeout)
        self.join_seconds.append(time.monotonic() - started)

    @property
    def release_seconds(self) -> float:
        """How long the join AFTER the terminate really took, in seconds.

        THE ONE NUMBER THAT PINS ``_RELEASE_SECONDS`` TO SOMETHING REAL. That
        constant is a sleep this file chose, and a sleep this file chose can stop
        being paid without anything noticing: the handler once exited on its
        first line while the constant still said four tenths of a second. This is
        the wall clock cost of the leg the budget is bounded against, terminate
        to exit, so the constant can be checked against what the ladder pays.

        IT IS NOT COMPARED TO THE BUDGET DIRECTLY, and that is deliberate. A
        verdict multiplied straight out of this reading carries the reading's
        jitter into the verdict, and this reading's jitter is a parent wakeup
        that reached eighty five milliseconds under load. It calibrates a literal
        with a wide tolerance instead, and the literal carries the exact band.

        WHAT A BROKEN READING DOES, measured rather than reasoned. This is a
        ``monotonic`` delta and so cannot go negative. Forced to zero it fails the
        calibration; forced to saturate at 2.0 it pins at the join timeout and
        fails the calibration and the rung test both. A degenerate reading here
        produces a false RED and never a false green, which is the safe direction
        for a value nothing else validates.

        The second join is that leg for every child here: the first join is the
        one that expires because the child is sleeping past every deadline, and
        the terminate is delivered between them. The rung sequence is asserted
        beside every use, so the index is checked rather than assumed.
        """
        assert self.rungs[:3] == ["join", "terminate", "join"], (
            f"the ladder ran {self.rungs}, so there is no terminate-to-exit leg to read"
        )
        return self.join_seconds[1]

    def is_alive(self) -> bool:
        return self.process.is_alive()

    def terminate(self) -> None:
        self.rungs.append("terminate")
        self.process.terminate()

    def kill(self) -> None:
        self.rungs.append("kill")
        self.process.kill()

    def close(self) -> None:
        self.rungs.append("close")
        self.exitcode = self.process.exitcode
        self.process.close()
        self.closed = True


def _reap_a_child(target) -> _WatchedChild:
    """Start one child of this shape, wait until it is armed, and reap it.

    The child says when its handler is installed rather than the parent guessing
    from a sleep, because a terminate that arrives before the handler is a
    different test than the one being written.
    """
    context = multiprocessing.get_context("spawn")
    reader, writer = context.Pipe(duplex=False)
    process = context.Process(target=target, args=(writer,))
    process.start()
    writer.close()
    try:
        assert reader.poll(60), "the child never reported that its handler was installed"
        reader.recv()
    finally:
        reader.close()
    watched = _WatchedChild(process)
    try:
        pool._reap(watched)
    finally:
        if not watched.closed:
            # The ladder did not finish, which is what a broken rung looks like.
            # This test does not get to leave a child running either.
            process.kill()
            process.join(10)
            process.close()
    return watched


def _raises_in_the_worker() -> object:
    """A loader failing the way a machine with no model installed fails."""
    raise RuntimeError("no checkpoint on this machine")


def _dies_without_answering() -> object:
    """A loader that takes its whole worker down, the way a segmentation fault does."""
    os._exit(70)


def test_a_plan_of_one_worker_runs_the_work_in_this_process():
    """The off-by-one this whole module turns on, asserted against the process table.

    A pool of one is a second interpreter, a second copy of the model, and a
    pickle of every item and result, to run the work slower than doing it here.
    It is also what a tight machine plans, which is the machine that can least
    afford it.
    """
    plan = pool.plan_pool(worker_bytes=WORKER, items=4, read_available=reader(2 * GIB))
    assert plan.in_process is True
    results = pool.map_workers(plan, _report, range(4), initializer=_load, initargs=("here",))
    assert [index for index, _pid, _tag, _life in results] == [0, 1, 2, 3]
    assert {pid for _index, pid, _tag, _life in results} == {os.getpid()}
    assert {tag for _index, _pid, tag, _life in results} == {"here"}


def test_an_in_process_plan_refuses_to_hand_back_pool_arguments():
    """The seam fails loudly rather than building the pool of one it was told not to."""
    plan = pool.plan_pool(worker_bytes=WORKER, items=4, read_available=reader(2 * GIB))
    with pytest.raises(ValueError):
        pool.executor_arguments(plan)


def test_pool_arguments_carry_a_spawn_context_and_never_the_platform_recycle_counter():
    """Spawn is not a preference here, and the recycle counter is not an omission.

    The sizing above assumes a child shares nothing with its parent, which is
    true under spawn and false under fork. Reading the start method off the
    context rather than trusting the keyword is the difference between asserting
    the argument was passed and asserting what it means.

    ``max_tasks_per_child`` is asserted ABSENT, which is the opposite of what
    this test used to say. Handing the executor its own recycle counter is what
    deadlocks a run one item past ``workers * counter``, and this function is a
    public seam: anything it returns is something a caller may hand straight to
    an executor.
    """
    plan = pool.plan_pool(
        worker_bytes=WORKER, items=500, ceiling=4, read_available=reader(16 * GIB)
    )
    arguments = pool.executor_arguments(plan, initializer=_load, initargs=("x",))
    assert arguments["max_workers"] == 4
    # THE LINE BELOW IS NOT THE PIN ON SPAWN, and reading it as one is how the
    # start method stayed unchecked. Darwin's own default start method IS spawn,
    # so this passes on this machine whether the module names spawn or asks for
    # whatever the platform hands out, and on linux the same unnamed context is
    # a fork and every per-worker number in the module is wrong. What pins it is
    # test_every_context_this_module_builds_is_written_as_spawn_in_the_source,
    # which reads the source and therefore answers for every platform from here.
    assert arguments["mp_context"].get_start_method() == "spawn"
    assert arguments["initargs"] == ("x",)
    assert "max_tasks_per_child" not in arguments, (
        "the platform's own recycle counter is back in the executor arguments; it "
        "deadlocks above workers times the counter, which is why this module "
        "retires a whole generation of children instead"
    )


@pytest.mark.parametrize("max_tasks_per_child", [1, 2, 100, None])
def test_no_plan_at_any_recycle_setting_hands_the_counter_to_an_executor(max_tasks_per_child):
    """Swept rather than sampled, because the deadlock is conditional on the value.

    The defect needed a counter of two or more, so a single case at one is the
    one value that cannot show it, and that is exactly the value the only
    recycling test used to run at.
    """
    plan = pool.plan_pool(
        worker_bytes=WORKER,
        items=10_000,
        ceiling=4,
        max_tasks_per_child=max_tasks_per_child,
        read_available=reader(64 * GIB),
    )
    assert "max_tasks_per_child" not in pool.executor_arguments(plan)


def test_the_executor_constructor_is_never_written_with_a_recycle_counter():
    """The source half of the same question, for the call this module makes itself.

    The runtime check above reads what one function returns. This one reads what
    the module WRITES, so a second executor built somewhere in here with the
    keyword spelled out would be caught even though it never passes through
    ``executor_arguments``.
    """
    for node in ast.walk(ast.parse(POOL_SOURCE)):
        if not isinstance(node, ast.Call):
            continue
        if getattr(node.func, "id", "") != "ProcessPoolExecutor":
            continue
        written = {keyword.arg for keyword in node.keywords}
        assert "max_tasks_per_child" not in written, (
            f"line {node.lineno} builds an executor with the platform's own recycle "
            f"counter, which deadlocks above workers times the counter"
        )


def test_every_context_this_module_builds_is_written_as_spawn_in_the_source():
    """The start method, pinned for every platform from the one that ships it.

    THE RUNTIME CHECK CANNOT ASK THIS QUESTION FROM HERE, and that is the whole
    reason this exists. Darwin's default start method is spawn, so
    ``get_context()`` with no argument returns a spawn context on this machine
    and the assertion that reads the start method off it passes FOR THE WRONG
    REASON. Both call sites were changed to the unnamed form and nothing died.
    On linux the same unnamed call is a fork today and a forkserver in a later
    interpreter, and a forked child shares its parent's pages, so a model loaded
    before the fork costs almost nothing per child and every per-worker number
    in this module is measuring something that is not happening.

    This is the same shape the general headroom share and the windows fallback
    are driven for: an arm this platform never executes cannot be checked by
    running it. It is checked by reading it, which is what the walk beside this
    one already does for the recycle counter.
    """
    written: list[tuple[int, list[str]]] = []
    for node in ast.walk(ast.parse(POOL_SOURCE)):
        if not isinstance(node, ast.Call):
            continue
        named = (
            node.func.attr
            if isinstance(node.func, ast.Attribute)
            else getattr(node.func, "id", "")
        )
        if named != "get_context":
            continue
        written.append((node.lineno, [ast.unparse(argument) for argument in node.args]))
    assert len(written) >= 2, (
        f"the sizing module builds {len(written)} start-method contexts; the probe "
        f"builds one and the executor builds another, so a walk that finds fewer "
        f"than two has stopped seeing them and is asserting nothing"
    )
    for lineno, arguments in written:
        assert arguments == ["'spawn'"], (
            f"line {lineno} builds a start-method context without naming spawn. The "
            f"per-worker arithmetic in this module assumes a child shares nothing "
            f"with its parent, which is true under spawn and false under fork, and "
            f"the platform default is spawn here and fork on linux, so an unnamed "
            f"context is right on this machine and wrong on the one it ships to"
        )


def test_recycling_is_on_by_default_for_any_pool_wider_than_one():
    """The literal is the point. This used to assert the plan CARRIES the constant,
    which it does at any value, so it was silent while the budget moved to one."""
    plan = pool.plan_pool(
        worker_bytes=WORKER, items=500, ceiling=4, read_available=reader(16 * GIB)
    )
    assert plan.max_tasks_per_child == 100


def test_no_child_survives_a_generation_boundary_and_every_one_reloads_its_model():
    """Real spawned children, because recycling cannot be observed any other way.

    Two properties in one pool, and they are one property in practice: a child
    that is retired must come back initialized, or recycling silently trades a
    bounded allocator for a worker running without its model.

    ASSERTED ACROSS THE BOUNDARY RATHER THAN AS A HEADCOUNT, which is what an
    earlier version of this test got wrong in a way that only showed up
    intermittently. Counting distinct processes assumes every worker in a
    generation takes work, and none of them is obliged to: children become ready
    at different times and the first one ready can drain a small queue before the
    second has finished importing. Two generations served by one child each is
    correct recycling and a headcount reads it as none. What recycling actually
    promises is that nothing crosses the line, so that is what is checked.
    """
    plan = pool.plan_pool(
        worker_bytes=WORKER,
        items=4,
        ceiling=2,
        max_tasks_per_child=1,
        read_available=reader(16 * GIB),
    )
    assert plan.workers == 2
    assert plan.tasks_per_generation == 2
    assert plan.generations == 2
    results = pool.map_workers(
        plan, _report, range(4), initializer=_load, initargs=("reloaded",)
    )
    assert [index for index, _pid, _tag, _life in results] == [0, 1, 2, 3]
    assert os.getpid() not in {pid for _index, pid, _tag, _life in results}, (
        "the work ran in the calling process, not in a pool"
    )
    first = {life for index, _pid, _tag, life in results if index < 2}
    second = {life for index, _pid, _tag, life in results if index >= 2}
    assert first and second
    assert not first & second, (
        f"a worker served items on both sides of a generation boundary ({first & second}); "
        f"nothing was retired and the allocator is bounded by nothing"
    )
    assert {tag for _index, _pid, tag, _life in results} == {"reloaded"}


# --- the deadlock, run where a hang cannot take the suite with it ------------
#
# THE SHAPE OF THIS TEST IS DICTATED BY THE SHAPE OF THE DEFECT. The executor's
# own ``max_tasks_per_child`` does not raise above ``workers * N``, and does not
# time out, and does not return partial results. It blocks in ``future.result()``
# forever with zero workers alive. A test written in process would therefore not
# fail; it would hang, and a hung suite reports nothing at all. So the run
# happens in a child with a watchdog on it, and the watchdog firing IS the
# failure.

_REPRODUCTION = '''\
"""A run above the recycle threshold, at a width and a counter given on the command line."""

import sys

from cratekit.core import pool


def double(value):
    return value * 2


def calm():
    return pool.Pressure(swap_used_bytes=0, used_percent=1.0)


def main():
    workers, tasks, items = (int(argument) for argument in sys.argv[1:4])
    plan = pool.plan_pool(
        worker_bytes=1,
        items=items,
        ceiling=workers,
        max_tasks_per_child=tasks,
        read_available=lambda: 64 * 1024 ** 3,
        read_pressure=calm,
    )
    assert plan.workers == workers, plan
    assert plan.max_tasks_per_child == tasks, plan
    assert items > workers * tasks, "the fixture is below the threshold it exists to cross"
    results = pool.map_workers(plan, double, range(items))
    assert results == [value * 2 for value in range(items)], "wrong results or wrong order"
    print(len(results))


if __name__ == "__main__":
    main()
'''

#: Generous by two orders of magnitude. The healthy run of the worst case below
#: takes about a tenth of a second, and the broken one takes forever, so anything
#: between those two numbers separates them. Large enough that a loaded build
#: machine cannot fail this by being slow.
_WATCHDOG_SECONDS = 90


@pytest.mark.parametrize(
    "workers,tasks,items",
    [
        (2, 100, 201),
        (2, 2, 5),
        (3, 2, 7),
        (2, 100, 1001),
    ],
    ids=["the-shipped-default", "smallest-that-can-hang", "three-wide", "five-generations"],
)
def test_work_above_the_recycle_threshold_finishes(tmp_path, workers, tasks, items):
    """The defect, at the configuration this module ships and three more.

    Measured before the fix, at the shipped default of two workers and a hundred
    tasks per child: 200 items finished in 0.07 seconds and 201 items never
    finished. The rule was exact, ``items > workers * counter`` with a counter of
    two or more, and a counter of one was the single value that could not trigger
    it. The only recycling test in this file ran at a counter of one with four
    items across two workers, which is below the threshold in any case, so the
    suite was green over a default configuration that could not complete an
    ordinary folder.

    EVERY CASE HERE CROSSES THE THRESHOLD AT A COUNTER OF AT LEAST TWO, and the
    reproduction asserts that it does, so a fixture that drifts back under the
    line fails rather than passing for the wrong reason.
    """
    script = tmp_path / "run_above_the_threshold.py"
    script.write_text(_REPRODUCTION)
    finished = subprocess.run(
        [sys.executable, str(script), str(workers), str(tasks), str(items)],
        capture_output=True,
        text=True,
        timeout=_WATCHDOG_SECONDS,
        cwd=tmp_path,
    )
    assert finished.returncode == 0, (
        f"the run failed rather than completing: {finished.stderr.strip()}"
    )
    assert finished.stdout.strip() == str(items)


_A_CHILD_THAT_DIES = '''\
"""A run in which one child is taken down mid task, above the generation boundary."""

from cratekit.core import pool


def double_but_die_on_the_fourth(value):
    if value == 3:
        import os

        os._exit(70)
    return value * 2


def calm():
    return pool.Pressure(swap_used_bytes=0, used_percent=1.0)


def main():
    plan = pool.plan_pool(
        worker_bytes=1,
        items=8,
        ceiling=2,
        max_tasks_per_child=2,
        read_available=lambda: 64 * 1024 ** 3,
        read_pressure=calm,
    )
    assert plan.workers == 2, plan
    assert plan.generations == 2, plan
    try:
        pool.map_workers(plan, double_but_die_on_the_fourth, range(8))
    except BaseException as failure:
        print(type(failure).__name__)
        return
    print("returned")


if __name__ == "__main__":
    main()
'''


def test_a_child_that_dies_mid_generation_ends_the_run_rather_than_hanging(tmp_path):
    """The other half of "a recycle that finishes", and the half nothing drove.

    THE PLATFORM RECYCLE COULD LEAVE A POOL SHORT A WORKER FOREVER, which is the
    defect this module replaced it for: a child was retired one at a time and its
    replacement was skipped, and the queue was left with no consumer. A GENERATION
    IS TORN DOWN AND REBUILT AS A UNIT, so there is no partial replacement to
    skip, and the failure a dead child can produce is bounded: the generation ends
    with an exception rather than with a queue nobody is reading.

    The child is killed outright rather than made to raise, because those are two
    different things to an executor. A task that raises returns an exception
    through the result channel and the pool is intact; a task that takes its
    process down leaves the pool broken with work outstanding, which is the shape
    that hangs if the teardown is waiting on a worker that is gone.

    RUN IN A CHILD WITH A WATCHDOG, for the reason the deadlock test is: what is
    being guarded against is a hang, and a hung test does not go red, it takes
    the suite with it and reports nothing.
    """
    script = tmp_path / "a_child_that_dies.py"
    script.write_text(_A_CHILD_THAT_DIES)
    finished = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
        timeout=_WATCHDOG_SECONDS,
        cwd=tmp_path,
    )
    assert finished.returncode == 0, (
        f"the reproduction itself failed: {finished.stderr.strip()}"
    )
    raised = finished.stdout.strip()
    assert raised and raised != "returned", (
        f"a run whose child was killed mid generation came back with results "
        f"({raised!r}); the death of a worker was not surfaced to the caller"
    )


# --- the contract that used to depend on how much memory the machine had -----


def test_a_function_no_child_could_receive_is_refused_before_anything_runs():
    """The same call must not mean two different things on two different machines.

    A plan of one worker calls the function here, where a lambda is ordinary; a
    plan of two pickles it to a child, where it cannot go. Before this refusal,
    the identical call returned results on a busy laptop and raised an
    AttributeError about a local object on a quiet server, and nothing in the
    module or its tests said so.
    """
    tight = pool.plan_pool(worker_bytes=WORKER, items=4, read_available=reader(2 * GIB))
    roomy = pool.plan_pool(
        worker_bytes=WORKER, items=4, ceiling=2, read_available=reader(64 * GIB)
    )
    assert tight.in_process is True
    assert roomy.in_process is False

    for plan in (tight, roomy):
        with pytest.raises(ValueError) as refusal:
            pool.map_workers(plan, lambda item: item * 2, range(4))
        assert "map_workers" in str(refusal.value)


def test_an_initializer_no_child_could_receive_is_refused_on_the_same_terms():
    plan = pool.plan_pool(worker_bytes=WORKER, items=4, read_available=reader(2 * GIB))

    def loads_here(tag):
        _LOADED["tag"] = tag

    with pytest.raises(ValueError) as refusal:
        pool.map_workers(plan, _report, range(4), initializer=loads_here, initargs=("x",))
    assert "initializer" in str(refusal.value)


def test_an_initializer_argument_no_child_could_receive_is_refused_on_the_same_terms():
    """One argument over from the refusal that was written, and the same defect.

    The function and the initializer were both refused and the VALUES handed to
    the initializer were not, so the same call still meant two different things
    on two different machines: a plan of one worker calls the initializer here
    with whatever it was given, and a plan of two pickles those values to a
    child. A closure is exactly the sort of thing that arrives as an initializer
    argument, since the argument is where a caller puts the thing the
    initializer needs.
    """
    tight = pool.plan_pool(worker_bytes=WORKER, items=4, read_available=reader(2 * GIB))
    roomy = pool.plan_pool(
        worker_bytes=WORKER, items=4, ceiling=2, read_available=reader(64 * GIB)
    )
    assert tight.in_process is True
    assert roomy.in_process is False

    for plan in (tight, roomy):
        with pytest.raises(ValueError) as refusal:
            pool.map_workers(
                plan, _report, range(4), initializer=_load, initargs=(lambda: None,)
            )
        assert "initializer argument 0" in str(refusal.value)


def test_one_raising_item_discards_every_completed_result():
    """Recorded rather than repaired, because repairing it is a decision U25 owns.

    Six items, two of which raise, and nothing comes back: not the four that
    succeeded, not a partial list, nothing. The exception that surfaces is the
    first in ITEM order rather than the first raised in time, so which error a
    caller is shown depends on the order the items went in. Both of those are the
    ordinary contract of a mapped executor and both are invisible from the call
    site, which is why they are written down here and in the module.
    """
    plan = pool.plan_pool(
        worker_bytes=WORKER, items=6, ceiling=2, read_available=reader(64 * GIB)
    )
    assert plan.in_process is False
    with pytest.raises(ValueError) as failure:
        pool.map_workers(plan, _raise_on_the_third_item, range(6))
    assert "item 2" in str(failure.value), (
        "the exception surfaced was not the first in item order"
    )


def test_no_work_at_all_starts_no_child(tmp_path):
    """An empty list must not cost a spawn, and must not cost a hang either."""
    plan = pool.plan_pool(
        worker_bytes=WORKER, items=500, ceiling=2, read_available=reader(64 * GIB)
    )
    assert plan.in_process is False
    assert pool.map_workers(plan, _report, []) == []


def test_the_real_probe_measures_a_freshly_spawned_child():
    """The one test of the probe that actually spawns. It costs two interpreters.

    Asserted as a DIFFERENCE between two loaders rather than as an absolute
    number, because an absolute number is a property of the machine and of every
    import the child happened to make. The difference is the loader's, and it is
    the thing the probe claims to measure.

    RUN ABOVE THE ALLOCATOR CLIFF, which is the whole reason this test now
    passes for the right reason. The probe used to call the loader and discard
    its result on the same line, so the object was freed before the resident set
    was read. Under about 112 mebibytes the allocator retains the freed blocks
    and the measurement still showed them, which is why a 96 mebibyte fixture
    passed. At 128 and above the blocks go straight back to the kernel and the
    measurement showed nothing, which is every model this module exists to size.
    """
    empty = pool.measure_worker_bytes(_nothing, floor_bytes=1)
    loaded = pool.measure_worker_bytes(_allocate_the_probe_fixture, floor_bytes=1)
    assert empty > 0
    assert loaded - empty >= _PROBE_FIXTURE_BYTES * 3 // 4, (
        f"a child that allocated {_PROBE_FIXTURE_BYTES // MIB} mebibytes measured "
        f"{loaded} against an empty child's {empty}; the probe is reading a process "
        f"that has already freed the thing it was asked to measure"
    )


def test_a_loader_that_never_returns_lands_on_the_floor_like_every_other_failure():
    """The one failure that used to hang instead of falling back.

    A crash, a kill, a segmentation fault, an unpicklable loader and a raising
    loader all returned the floor already. A loader that simply never finishes
    blocked, with a docstring above it promising that every failure returns the
    floor, and the promise held only because nothing had tested it.
    """
    started = time.monotonic()
    measured = pool.measure_worker_bytes(
        _still_running_when_the_deadline_passes, floor_bytes=4242, timeout_seconds=1.0
    )
    elapsed = time.monotonic() - started
    assert measured == 4242
    assert elapsed < 60, f"the probe took {elapsed:.1f} seconds to give up on a hung loader"


def test_a_probe_that_gave_up_leaves_no_child_still_allocating():
    """The escalation, which nothing exercised. A timed out probe is still loading.

    A probe that gave up is a probe whose child is still allocating the very
    thing the machine already said it could not afford, and abandoning it leaves
    exactly the allocation this module exists to refuse. The reaping code says
    so in its own docstring, and made a no-op the whole suite stayed green,
    because the one test of a loader past its deadline asserts only that the
    PARENT came back quickly, and the parent comes back quickly either way.

    Asserted against the process table rather than against elapsed time, because
    what is wrong in the broken case is not the parent's timing. It is that a
    child of this process is still running after the call has returned.
    """
    before = set(multiprocessing.active_children())
    started = time.monotonic()
    measured = pool.measure_worker_bytes(
        _still_running_when_the_deadline_passes, floor_bytes=4242, timeout_seconds=2.0
    )
    elapsed = time.monotonic() - started
    assert measured == 4242
    assert elapsed < 8, "the probe waited out a loader it had already abandoned"
    left = [child for child in multiprocessing.active_children() if child not in before]
    assert not left, (
        f"a probe child outlived the probe that started it: {left}. It is still "
        f"holding whatever its loader had allocated when the deadline passed."
    )


# --- the ladder itself, one rung at a time -----------------------------------
#
# THE TEST ABOVE COVERS THE EXISTENCE OF REAPING AND NOTHING ABOUT ITS SHAPE. Its
# loader sleeps for eight seconds, so after the first join the child is alive and
# EITHER rung ends it on its own. Measured against that suite: removing the
# terminate rung killed nothing, removing the kill rung killed nothing, and
# swapping them so the kill runs first killed nothing. Only deleting the whole
# function body registered at all.
#
# WHAT IS ACTUALLY LOAD BEARING IS THE ORDER. Terminate first, so a child gets
# the chance to unwind and release what it holds; kill second, as the backstop
# for a child that cannot. Somebody deleting the terminate rung as redundant
# ships green and turns every abandoned probe into an unconditional SIGKILL, on a
# machine this module had already decided was tight.
#
# Two children distinguish the rungs, and neither can be answered by the other:
# one exits cleanly on a terminate and reports a number no signal produces, and
# one ignores the terminate entirely and can only be ended by the kill.
#
# THE ORDER IS HALF OF IT AND THE BUDGET IS THE OTHER HALF, which the first
# version of this section missed entirely. A terminate that is not given long
# enough to be acted on is a terminate in name only: the join after it expires,
# the kill lands anyway, and every abandoned probe meets the unconditional
# SIGKILL this ladder was written to prevent, with the rungs still in the right
# order and the suite still green. Measured against the first version of this
# section: ``_PROBE_REAP_SECONDS`` dropped from 1.0 to 0.001 and killed nothing,
# because both children reached their exit on the first line of their handler
# and neither could tell the two budgets apart. The cooperative child now spends
# ``_RELEASE_SECONDS`` letting go before it reports, so its exit code is a
# reading of the budget as well as of the order.
#
# THE MEASUREMENT AND THE BAND ARE TWO ASSERTIONS AND NOT ONE, which is what the
# version before this one got wrong. It compared the shipped budget against a leg
# TIMED in the same run, ``budget >= 2 * timed_leg``, which put a tenth of a
# second of jitter inside a verdict that mutants sit one hundredth of a second
# away from. Measured over twenty five consecutive runs of the subset: a budget
# of 0.81 failed on nineteen of them and passed on six. A seventy six percent
# kill is not a kill, and no bound drawn from one clock reading can be tighter
# than that reading's jitter.
#
# So the chain is split, and each half is asserted where it can be decided
# outright. The reaps below TIME the terminate-to-exit leg and calibrate
# ``_RELEASE_SECONDS`` against it, over several samples and with a tolerance
# measured to be wider than any jitter this machine produces. The band then
# compares the shipped budget against that calibrated literal in exact
# arithmetic, with no clock in it at all. The measurement still pins the
# reference, which is the only reason it was ever taken, and the verdict on the
# budget is a fixed number rather than a race.


#: How many reaps the release measurement is taken over, and why more than one.
#:
#: ONE SAMPLE IS NOT A MEASUREMENT ON A LEG THAT JITTERS. Measured over 330 legs
#: in five load regimes, a single sample ran 0.4007 to 0.4926 seconds, and the
#: widest excursion came from the PARENT not being scheduled promptly rather than
#: from the leg costing more. Five, because the statistic below is a minimum and
#: a minimum stops improving quickly: measured here over eighty further legs,
#: disjoint blocks of five put that minimum in [0.4010, 0.4090] both idle and
#: under thirty two spinners at load average thirty four, an eight millisecond
#: envelope against a single sample's eleven idle and ninety two starved. Each
#: reap costs about a second and a half of wall clock, nearly all of it the first
#: join expiring, so five is also what the suite can afford.
_RELEASE_SAMPLES = 5


@pytest.fixture(scope="module")
def cooperative_reaps() -> list[_WatchedChild]:
    """``_RELEASE_SAMPLES`` reaps of the child that unwinds, read by two tests.

    Module scoped because two questions are being asked of the same events, the
    rung order and what the leg cost, and a second wave of spawns to ask the
    second one would pay the whole wall clock again to watch the same ladder
    twice.
    """
    return [_reap_a_child(_unwinds_on_a_terminate) for _ in range(_RELEASE_SAMPLES)]


def test_a_probe_child_that_can_unwind_is_asked_to_before_it_is_killed(cooperative_reaps):
    """The first rung, the ORDER, and the BUDGET the first rung is worth nothing without.

    A child that handles a terminate exits with its own code. A child that was
    killed outright reports the negative of the signal that killed it and never
    ran a line of its own. Those are two different numbers, so this test can say
    which rung ended the child rather than only that something did.

    THE CHILD TAKES TIME TO LET GO, so the same exit code also says the ladder
    waited. A budget below ``_RELEASE_SECONDS`` expires mid release, the kill
    lands on a child that was in the middle of doing what it was asked, and the
    77 below becomes a negative number.

    POSIX SIGNAL SEMANTICS, ASSERTED UNCONDITIONALLY. Windows has no handleable
    terminate and its kill IS its terminate, so there would be nothing to
    distinguish there, and this repository allows no conditional skip outside the
    pending register. The battery runs on darwin and continuous integration runs
    on linux, which are the two machines this has to be true on.

    EVERY REAP IN THE WAVE, not the first one. The measurement beside this takes
    several samples anyway, and a ladder that ran correctly once and wrongly on
    the fourth spawn is a rung that works most of the time, which is the thing
    this whole section refuses to accept elsewhere.
    """
    for index, watched in enumerate(cooperative_reaps):
        assert watched.exitcode == _TERMINATED_CLEANLY, (
            f"reap {index} of {len(cooperative_reaps)}: the child reported "
            f"{watched.exitcode} rather than unwinding on a terminate; a negative "
            f"number here is a SIGKILL, which means either the backstop ran first or "
            f"the terminate was not given the {_RELEASE_SECONDS} seconds this child "
            f"needs to let go, and no probe child ever gets to release what it is "
            f"holding"
        )
        assert watched.rungs == ["join", "terminate", "join", "close"]


#: The least the timed leg may be, as a multiple of the cost the fixture DECLARES.
#:
#: The honest floor is one. A leg that contains a ``time.sleep(_RELEASE_SECONDS)``
#: cannot return sooner than that sleep, and every other term in it, signal
#: delivery, the child's exit, the parent's wakeup, only adds. Nine tenths is one
#: with room under it, because measured over eighty legs the minimum of five ran
#: 0.4010 to 0.4090 against a declared 0.4, so an exact floor would have shipped
#: with one millisecond of clearance and one millisecond of clearance is the
#: intermittent red this section exists to remove. Nine tenths has forty one.
_RELEASE_FLOOR_IN_DECLARED = 0.9

#: The most it may be, in the same units. Past this the declared cost is not what
#: the ladder pays, and the band below is then exact arithmetic over a number
#: that has stopped describing anything. Measured: the minimum of five sat ninety
#: one milliseconds under this edge idle and under thirty two spinners alike, and
#: of the 330 single legs the review timed across five load regimes, the dearest
#: was 0.4926 and not one reached it.
_RELEASE_CEILING_IN_DECLARED = 1.25


def test_the_release_the_fixture_declares_is_what_the_ladder_was_timed_paying(
    cooperative_reaps,
):
    """``_RELEASE_SECONDS`` is a literal, and this is the mechanism that pins it.

    The band below is exact arithmetic over two constants, which is only worth
    having while one of them still describes something real. This is what keeps
    it real: the terminate-to-exit leg is TIMED, and the literal that band
    multiplies has to agree with what was timed.

    WHAT IT CATCHES, and it is the defect this whole section was written for.
    This child once called ``os._exit`` on the first line of its handler, a
    release that costs nothing, while the constant beside it still said four
    tenths of a second. Nothing in the suite could tell, and so
    ``_PROBE_REAP_SECONDS`` moved from 1.0 to 0.001 with everything green. Under
    this, the minimum over five reaps reads about five milliseconds against a
    declared 0.4 and the floor fails at once.

    WHY THE MINIMUM AND NOT THE MEAN OR THE MAXIMUM. The noise on this leg is one
    sided. The child's handler sleeps, a sleep is a kernel timer, and the parent
    times from before its join to after it returns, so every error term ADDS.
    Measured: forty spinners at load average fifty moved a single sample's
    maximum by a tenth of a millisecond and two gibibytes of churn moved it by
    one, while a sampler that was not scheduled promptly moved it by eighty. The
    excursion is the PARENT'S WAKEUP and not the leg. A minimum drops exactly
    that term and keeps the one the fixture controls, which is why it reads the
    same idle and starved while a maximum does not.

    THE TOLERANCE IS WIDER THAN THE JITTER BY DESIGN AND BY MEASUREMENT. This
    admits [0.36, 0.50] against a statistic measured to sit in [0.4010, 0.4090],
    so the nearest edge is forty one milliseconds away and the envelope is eight.
    That is the whole difference from the version before it, which put the
    nearest edge seven milliseconds from a statistic whose own spread was
    ninety one.
    """
    measured = min(watched.release_seconds for watched in cooperative_reaps)
    assert measured >= _RELEASE_FLOOR_IN_DECLARED * _RELEASE_SECONDS, (
        f"the cheapest of {len(cooperative_reaps)} timed terminate-to-exit legs was "
        f"{measured:.4f} seconds against a fixture that declares {_RELEASE_SECONDS}; "
        f"a leg cannot cost less than the sleep inside it, so this is a child that no "
        f"longer pays what it says it pays, and the band below is then arithmetic "
        f"over a number that describes nothing"
    )
    assert measured <= _RELEASE_CEILING_IN_DECLARED * _RELEASE_SECONDS, (
        f"the cheapest of {len(cooperative_reaps)} timed terminate-to-exit legs was "
        f"{measured:.4f} seconds against a fixture that declares {_RELEASE_SECONDS}; "
        f"letting go costs materially more than this file claims, so every budget "
        f"bounded against that claim is bounded against the wrong number"
    )


#: The least the budget may be, as a multiple of what a release costs. At one
#: times it the budget is racing the release rather than covering it, which does
#: not fail, it fails sometimes, and a rung that works most of the time is how an
#: intermittent red suite gets blamed on the runner.
_BUDGET_FLOOR_IN_RELEASES = 2.0

#: The most it may be, in the same units. Past this the first rung has stopped
#: being a chance to unwind and become a stall in front of a kill that was always
#: going to land, paid on every abandoned probe on a machine already too tight to
#: run the pool it asked for.
_BUDGET_CEILING_IN_RELEASES = 3.0


def test_the_reaping_budget_is_a_band_around_what_a_release_costs():
    """The margin, so a budget that would merely make the test above FLAKY fails outright.

    The test above dies at any budget under four tenths of a second, which is the
    far half of this. The near half is worse and it is what a bound is for: at a
    budget of half a second that test still passes, with a tenth of a second of
    slack on a leg whose spread this machine measures in milliseconds. It passes
    most of the time, and most of the time is not a rung.

    NO CLOCK IN THIS ASSERTION, DELIBERATELY, and that is the correction. The
    version before this multiplied a leg timed in the same run, so the edge moved
    with the scheduler: measured, the floor landed anywhere in [0.8014, 0.8242],
    which put 0.81 and 0.82 inside their own jitter window and made the verdict
    on them a coin flip, nineteen red and six green over twenty five runs. Both
    edges are now exact. The floor is 0.8000 and the ceiling is 1.2000, on every
    run, on every machine, and the reference they multiply is pinned to the clock
    by the test above rather than by this one.

    WHAT THAT COSTS AND WHAT IT BUYS, stated rather than left to be discovered.
    The ceiling TIGHTENS, from a fuzzy [1.2021, 1.2363] to an exact 1.2000, so
    1.21 and 1.22 now fail every time where they used to pass or flip. The floor
    LOOSENS, from a fuzzy [0.8014, 0.8242] to an exact 0.8000, so 0.81 and 0.82
    now pass every time. That is the trade: one edge value given up, two gained,
    and no verdict anywhere that depends on what else the machine was doing.

    A BAND RATHER THAN A FLOOR, because too long is a real failure and not merely
    an inelegance. ``_reap`` spends this budget up to three times on a wedged
    child, in the ``finally`` of a probe that has already failed, on a machine
    this module has already decided cannot afford what it was asked for.

    THE MULTIPLIERS ARE JUDGEMENTS AND THE REFERENCE IS NOT. Two and three are
    chosen and written down; what they multiply is a number the test above will
    not let drift from the ladder's real cost. Halving either multiplier alone
    weakens a bound and cannot fail on its own, which is arithmetic rather than
    evidence, so the pairs that show what they hold are recorded in
    ``docs/mutation-u12.md`` beside them.
    """
    assert pool._PROBE_REAP_SECONDS >= _BUDGET_FLOOR_IN_RELEASES * _RELEASE_SECONDS, (
        f"the reaping budget is {pool._PROBE_REAP_SECONDS} seconds against a release "
        f"that costs {_RELEASE_SECONDS}; a child that is asked to stop has to be given "
        f"comfortably longer than stopping costs, or the terminate rung is a race and "
        f"every abandoned probe meets the kill on the runs it loses"
    )
    assert pool._PROBE_REAP_SECONDS <= _BUDGET_CEILING_IN_RELEASES * _RELEASE_SECONDS, (
        f"the reaping budget is {pool._PROBE_REAP_SECONDS} seconds against a release "
        f"that costs {_RELEASE_SECONDS}; a budget that far above what letting go costs "
        f"is not patience, it is a stall in front of a kill that was always going to "
        f"land, and it is paid on every abandoned probe"
    )


def test_a_probe_child_that_refuses_to_unwind_meets_the_kill_backstop():
    """The second rung, which is the one that makes the promise absolute.

    A terminate is a request and a wedged child is entitled to ignore it. Without
    the backstop the ladder is a suggestion, and the child left behind is holding
    the allocation this module exists to refuse.
    """
    watched = _reap_a_child(_ignores_a_terminate)
    assert watched.closed, (
        "the reaping gave up on a child that ignored its terminate; it is still "
        "running and still holding whatever its loader had allocated"
    )
    assert watched.exitcode == -signal.SIGKILL
    assert watched.rungs == ["join", "terminate", "join", "kill", "join", "close"]


def test_a_probe_child_that_dies_without_answering_gives_up_at_once():
    """The pipe is what tells a dead child from a slow one, and nothing tested it.

    The parent closes its own copy of the write end so the pipe reaches end of
    file the moment the child's copy does. Left open, a child that died looks
    exactly like a child that is still loading, and the run waits out the whole
    deadline for an answer that can never come, which at the shipped deadline is
    two minutes of nothing per probe. Removed, the suite stayed green, because
    every other probe failure sends a value back BEFORE it fails and only a
    worker that dies outright sends nothing at all.

    Driven at a deadline long enough that waiting it out is unmistakable and
    short enough that a failure here costs half a minute rather than the run.
    """
    started = time.monotonic()
    measured = pool.measure_worker_bytes(
        _dies_without_answering, floor_bytes=4242, timeout_seconds=30.0
    )
    elapsed = time.monotonic() - started
    assert measured == 4242
    assert elapsed < 15, (
        f"the probe waited {elapsed:.1f} seconds for a child that was already gone; "
        f"the parent is holding the write end of the pipe open, so end of file "
        f"never arrives and a dead child is indistinguishable from a slow one"
    )


def test_a_real_loader_that_raises_lands_on_the_floor_without_printing_anything(capfd):
    """A machine with no model is an ordinary case, and it must not look like a crash.

    The floor is returned either way, so the only thing at stake is what the run
    LOOKS like, and that is worth a test: the failure is caught inside the worker
    and sent back as a value, because a traceback printed by a child's default
    exception hook while the parent quietly carries on is a run that reads as
    broken and is not. Captured at the file descriptor rather than at ``sys.stderr``
    because the noise, if there were any, would come from another process.
    """
    measured = pool.measure_worker_bytes(_raises_in_the_worker, floor_bytes=4242)
    printed = capfd.readouterr()
    assert measured == 4242
    assert "Traceback" not in printed.err, (
        f"a probe failure printed out of its worker: {printed.err}"
    )


# ---------------------------------------------------------------------------
# A container, where the machine's reading is not this process's reading
# ---------------------------------------------------------------------------
#
# THE ONE WAY THE READING LIES THAT NO BRAKE ABOVE CAN SEE. The reserve, the
# headroom and the pressure gate all answer "the number is optimistic". A
# container answers "the number belongs to a different machine": psutil reads the
# host's counters, so a process capped at half a gibibyte on a sixty four
# gibibyte host is told it has sixty four, and the pressure gate cannot help
# because the host's swap and the host's used percent are both fine.
#
# This is the same blindness the core count is refused for. The guard below
# forbids ``sched_getaffinity`` and ``cpu_affinity`` by name, and the reason
# written beside them is that those are what somebody reaches for on reading
# that a core count ignores cgroup limits. A module that refused cores for being
# cgroup blind while reading memory cgroup blind had moved the defect rather
# than ended it.


def _version_two(root: Path, *, limit: str, current: str | None = "0") -> Path:
    """A cgroup version two directory: one file for the cap, one for the usage."""
    (root / "memory.max").write_text(limit)
    if current is not None:
        (root / "memory.current").write_text(current)
    return root


def _version_one(root: Path, *, limit: str, usage: str = "0") -> Path:
    """The older layout, which is still what a good many hosts publish."""
    memory = root / "memory"
    memory.mkdir()
    (memory / "memory.limit_in_bytes").write_text(limit)
    (memory / "memory.usage_in_bytes").write_text(usage)
    return root


def _hierarchy(tmp_path: Path) -> Path:
    """An empty cgroup mount point, kept apart from the other files a test writes."""
    root = tmp_path / "cgroup"
    root.mkdir()
    return root


def _self_cgroup(tmp_path: Path, text: str) -> Path:
    """A ``/proc/self/cgroup`` this process could have been given.

    Written rather than read, for the same reason the mount point is: this
    machine has neither file, so the only way to execute either branch of the
    reader is to hand it both.
    """
    path = tmp_path / "self-cgroup"
    path.write_text(text)
    return path


def test_a_cgroup_with_a_cap_reports_what_is_left_inside_it(tmp_path):
    _version_two(tmp_path, limit=str(512 * MIB), current=str(64 * MIB))
    assert pool.cgroup_memory_headroom_bytes(tmp_path) == 448 * MIB


def test_the_older_cgroup_layout_is_read_too(tmp_path):
    _version_one(tmp_path, limit=str(2 * GIB), usage=str(512 * MIB))
    assert pool.cgroup_memory_headroom_bytes(tmp_path) == 1536 * MIB


def test_a_cap_whose_usage_cannot_be_read_is_still_a_cap(tmp_path):
    """A ceiling that is certainly not too small beats no ceiling at all.

    Throwing the limit away because the usage file was unreadable would report
    the host's sixty four gibibytes for a process that can never have more than
    half of one, which is the whole defect back again.
    """
    _version_two(tmp_path, limit=str(512 * MIB), current=None)
    assert pool.cgroup_memory_headroom_bytes(tmp_path) == 512 * MIB


def test_a_cgroup_already_over_its_cap_has_no_headroom_rather_than_negative(tmp_path):
    """A subtraction is where a byte count goes negative, and a negative reading
    is treated as unreadable one layer up, which would silently restore the host
    number on the tightest machine there is."""
    _version_two(tmp_path, limit=str(512 * MIB), current=str(600 * MIB))
    assert pool.cgroup_memory_headroom_bytes(tmp_path) == 0


@pytest.mark.parametrize(
    "contents",
    ["max", "", "not a number", "-1", str(1 << 62), "9223372036854771712"],
    ids=["v2-unlimited", "empty", "text", "negative", "at-the-sentinel", "v1-unlimited"],
)
def test_a_cgroup_that_declares_no_limit_reports_none(tmp_path, contents):
    """Every way of not having a cap is one answer, and the answer is not a guess.

    ``max`` is what version two writes for a group with no limit. The very large
    numbers are what version one writes instead, and it has written two different
    ones across kernel versions, which is why the test here is "absurdly large"
    rather than equality with either.
    """
    _version_two(tmp_path, limit=contents)
    assert pool.cgroup_memory_headroom_bytes(tmp_path) is None


def test_a_machine_with_no_cgroups_at_all_reports_none(tmp_path):
    """P7's other half. This is every developer machine this product is built on."""
    assert pool.cgroup_memory_headroom_bytes(tmp_path / "nothing here") is None
    assert pool.cgroup_memory_headroom_bytes(tmp_path) is None


@pytest.mark.parametrize(
    "limit",
    [32 * GIB, 256 * GIB, 1024 * GIB, 65536 * GIB],
    ids=["a-large-container", "a-large-host", "a-terabyte-host", "larger-than-anything-sold"],
)
def test_a_large_cap_is_still_a_cap_and_the_sentinel_never_swallows_one(tmp_path, limit):
    """The sentinel from the side that reintroduces the defect this unit closes.

    "Absurdly large" has to stay absurd, and nothing was checking that it did.
    Lowered from four exbibytes to thirty two gibibytes, a container published
    with a thirty two gibibyte cap reads as having NO cap at all, the host's five
    hundred gibibyte reading stands, and the plan is the full ceiling of model
    loading children inside a cgroup that holds a sixteenth of it. The suite
    stayed green at that value and at a tebibyte.

    NEITHER EXISTING CASE COULD SEE IT. The one at the sentinel uses a number
    above every candidate, and the one where the host is tighter than the cap
    puts a one gibibyte host against a thirty two gibibyte cap, so the host is
    the minimum either way and the cap is never the answer being checked.

    Sixty four tebibytes is past the largest machine anybody sells, and it is
    still a cap rather than a way of saying there is not one.
    """
    _version_two(tmp_path, limit=str(limit), current="0")
    assert pool.cgroup_memory_headroom_bytes(tmp_path) == limit


def test_a_large_container_on_a_larger_host_is_still_sized_by_the_container(
    tmp_path, monkeypatch
):
    """The same sentinel, driven to the number a pool would be built from.

    A thirty two gibibyte cap on a five hundred and twelve gibibyte host is a
    real deployment rather than a corner: it is what a large container on a large
    host looks like. The reading has to be the container's.
    """
    import psutil

    _version_two(tmp_path, limit=str(32 * GIB), current=str(2 * GIB))
    monkeypatch.setattr(
        psutil, "virtual_memory", lambda: SimpleNamespace(available=512 * GIB)
    )
    assert pool.available_bytes(cgroup_root=tmp_path) == 30 * GIB


def test_a_cgroup_file_this_process_may_not_read_is_no_cap_rather_than_a_crash(
    tmp_path, monkeypatch
):
    """The second of the three reasons the reader's own docstring names.

    Only the first was driven. Narrowed from ``OSError`` to ``FileNotFoundError``
    the suite stayed green, and on a host where the cgroup file is mode 000 the
    narrowed version raises ``PermissionError`` out of :func:`available_bytes`,
    which is a public function that promises a number. Inside ``plan_pool`` that
    is swallowed and lands on MEMORY_UNREADABLE, so it degrades QUIETLY rather
    than crashing, which is what makes it hard to notice.

    REFUSED AT THE CALL RATHER THAN STAGED WITH A FILE MODE, for two reasons that
    point the same way. A file at mode 000 is readable by root, so a staged
    version would pass vacuously wherever the suite runs privileged, and this
    repository allows no conditional skip outside the pending register, which is
    the only other way to handle that. The refusal is raised at the one call the
    reader makes, which is exactly where the operating system would raise it.
    """
    import psutil

    _version_two(tmp_path, limit=str(512 * MIB), current="0")
    refused = tmp_path / "memory.max"
    readable = Path.read_text

    def refuse(self, *arguments, **keywords):
        if self == refused:
            raise PermissionError(13, "Permission denied", str(self))
        return readable(self, *arguments, **keywords)

    monkeypatch.setattr(Path, "read_text", refuse)
    assert pool.cgroup_memory_headroom_bytes(tmp_path) is None
    monkeypatch.setattr(psutil, "virtual_memory", lambda: SimpleNamespace(available=7 * GIB))
    assert pool.available_bytes(cgroup_root=tmp_path) == 7 * GIB


def test_a_cgroup_path_that_is_a_directory_is_no_cap_rather_than_a_crash(
    tmp_path, monkeypatch
):
    """The third reason, and the one that survives narrowing to PermissionError.

    The breadth was covered on one side only: narrowing the catch the other way
    kills nine tests, and narrowing it to the file simply not existing kills
    none. A path that resolves to a directory is neither.
    """
    import psutil

    (tmp_path / "memory.max").mkdir()
    assert pool.cgroup_memory_headroom_bytes(tmp_path) is None
    monkeypatch.setattr(psutil, "virtual_memory", lambda: SimpleNamespace(available=7 * GIB))
    assert pool.available_bytes(cgroup_root=tmp_path) == 7 * GIB


# --- which cgroup is THIS process in --------------------------------------
#
# READING THE ROOT OF THE HIERARCHY IS RIGHT IN ONE DEPLOYMENT AND WRONG IN THE
# OTHER. Inside a cgroup namespaced container, which is the ordinary Docker case,
# this process sits at "/" and the cap is published at the root. On a host it is
# not: a systemd unit with MemoryMax= lives at system.slice/something.service and
# the root publishes no cap at all, so a reader that stopped at the root reports
# no limit for a four gibibyte service on a five hundred gibibyte machine, and
# the reserve and the percent then scale a number a hundred times the truth.


def test_a_cap_on_a_nested_cgroup_is_read_rather_than_the_empty_root(tmp_path):
    """The systemd shape, which reading the root alone cannot see at all."""
    root = _hierarchy(tmp_path)
    unit = root / "system.slice" / "cratekit.service"
    unit.mkdir(parents=True)
    _version_two(unit, limit=str(4 * GIB), current=str(1 * GIB))
    where = _self_cgroup(tmp_path, "0::/system.slice/cratekit.service\n")
    assert pool.cgroup_memory_headroom_bytes(root, self_cgroup=where) == 3 * GIB


def test_the_tightest_cap_on_the_chain_is_the_one_that_binds(tmp_path):
    """A cgroup nested inside another is held by both, and the smaller runs out first.

    Taking the deepest cap instead reports the unit's own generous number while a
    tighter slice above it is the real ceiling, which is the same mistake as
    taking the host's number over the container's.
    """
    root = _hierarchy(tmp_path)
    unit = root / "system.slice" / "cratekit.service"
    unit.mkdir(parents=True)
    _version_two(unit.parent, limit=str(2 * GIB), current="0")
    _version_two(unit, limit=str(8 * GIB), current="0")
    where = _self_cgroup(tmp_path, "0::/system.slice/cratekit.service\n")
    assert pool.cgroup_memory_headroom_bytes(root, self_cgroup=where) == 2 * GIB


def test_a_namespaced_container_sits_at_the_root_and_reads_what_it_always_read(tmp_path):
    """The common Docker case, unchanged, which is the half a walk could break."""
    root = _hierarchy(tmp_path)
    _version_two(root, limit=str(512 * MIB), current=str(64 * MIB))
    where = _self_cgroup(tmp_path, "0::/\n")
    assert pool.cgroup_memory_headroom_bytes(root, self_cgroup=where) == 448 * MIB


def test_the_older_layout_is_walked_from_this_processs_own_path_too(tmp_path):
    """Version one names its controllers, and the memory one shares a line with others.

    The controller field is comma separated, so a reader matching the whole field
    against "memory" misses every host that grouped the controllers, which is
    most of them.
    """
    root = _hierarchy(tmp_path)
    unit = root / "memory" / "system.slice" / "cratekit.service"
    unit.mkdir(parents=True)
    (unit / "memory.limit_in_bytes").write_text(str(2 * GIB))
    (unit / "memory.usage_in_bytes").write_text(str(512 * MIB))
    where = _self_cgroup(
        tmp_path, "9:cpu,memory:/system.slice/cratekit.service\n12:pids:/\n"
    )
    assert pool.cgroup_memory_headroom_bytes(root, self_cgroup=where) == 1536 * MIB


@pytest.mark.parametrize(
    "line",
    ["7:memoryfoo:/sneaky\n", "9:blkio,memory_hotplug:/sneaky\n"],
    ids=["a-name-that-starts-with-it", "a-name-that-contains-it"],
)
def test_a_controller_field_that_merely_contains_the_word_memory_is_not_it(tmp_path, line):
    """The direction the first fix of this line did not test, and the only one that can happen.

    The controller field is a comma separated LIST, so it is split and matched
    whole. The commit that made it so drove the tight direction, a whole field
    test against "memory" missing "cpu,memory", which is a real host and is
    covered above. The loose direction was left armed: a plain ``"memory" in
    controllers`` accepts any name with the word inside it, and every existing
    test agreed, because none of them wrote such a name. Measured against that
    suite, relaxing the split to a substring test killed nothing.

    What it buys the loose reader is a path from an unrelated hierarchy walked as
    though it were this process's memory cgroup, and because the tightest cap
    binds, a stranger's tight number narrows every pool on the machine.
    """
    root = _hierarchy(tmp_path)
    stranger = root / "memory" / "sneaky"
    stranger.mkdir(parents=True)
    (stranger / "memory.limit_in_bytes").write_text(str(64 * MIB))
    (stranger / "memory.usage_in_bytes").write_text("0")
    where = _self_cgroup(tmp_path, line)
    assert pool.cgroup_memory_headroom_bytes(root, self_cgroup=where) is None, (
        "a hierarchy whose controller name merely contains the word memory was read "
        "as the memory controller, and the cgroup it named is not this process's"
    )


def test_a_machine_with_no_proc_file_at_all_reads_the_root_it_was_given(tmp_path):
    """Every darwin machine this product is built on, and every one with no cgroups."""
    root = _hierarchy(tmp_path)
    _version_two(root, limit=str(512 * MIB), current="0")
    assert (
        pool.cgroup_memory_headroom_bytes(root, self_cgroup=tmp_path / "no such file")
        == 512 * MIB
    )


def test_a_cgroup_path_that_climbs_out_of_the_mount_is_not_followed(tmp_path):
    """A path this reader does not understand is not a licence to read elsewhere.

    The only way ``..`` reaches here is a kernel writing something unexpected,
    and walking out of the mount to read whatever file happens to be there is not
    a reading of this process's cgroup.
    """
    root = _hierarchy(tmp_path)
    outside = tmp_path / "outside"
    outside.mkdir()
    _version_two(outside, limit=str(64 * MIB), current="0")
    where = _self_cgroup(tmp_path, "0::/../outside\n")
    assert pool.cgroup_memory_headroom_bytes(root, self_cgroup=where) is None


@pytest.mark.parametrize(
    "line",
    ["0::/../sibling\n", "0::/service/../sibling\n"],
    ids=["a-climb-at-the-top", "a-climb-in-the-middle"],
)
def test_a_climb_that_lands_on_a_real_cgroup_inside_the_mount_is_refused_too(tmp_path, line):
    """The half the test above cannot see, and the half that has consequences.

    That one writes its bait OUTSIDE the mount, so all it proves is that the walk
    does not escape. It never proved the line was REFUSED, and it was not: the
    ``..`` was dropped and the rest was walked, which rewrites ``/../sibling``
    into a directory that can exist, can publish a cap, and belongs to a cgroup
    this process is not in. That is identity that is not unique, and the tightest
    cap wins, so a stranger's tight number narrows every pool on the machine
    while the walk stays neatly inside the mount and every existing test agrees.

    A path with ``..`` in it does not name this process's cgroup, at the top or
    anywhere else along it, so no level it names is read.
    """
    root = _hierarchy(tmp_path)
    sibling = root / "sibling"
    sibling.mkdir()
    _version_two(sibling, limit=str(64 * MIB), current="0")
    where = _self_cgroup(tmp_path, line)
    assert pool.cgroup_memory_headroom_bytes(root, self_cgroup=where) is None, (
        "a cgroup this process is not in was read as though it were, and because "
        "the tightest cap binds it would have narrowed every pool on the machine"
    )


def test_a_climb_still_leaves_the_mounts_own_cap_readable(tmp_path):
    """Refusing the path is not refusing the hierarchy, and the difference is safety.

    Whatever cgroup this process is really in, it is somewhere under this mount,
    so a cap published at the mount is an ancestor's cap and an ancestor's cap
    binds. Discarding that along with the path answers an unparsable line with
    "no cap at all" on a machine that publishes one, which is looser than the
    code being replaced rather than safer, and looser is the direction this
    module cannot afford.
    """
    root = _hierarchy(tmp_path)
    _version_two(root, limit=str(512 * MIB), current=str(64 * MIB))
    sibling = root / "sibling"
    sibling.mkdir()
    _version_two(sibling, limit=str(64 * MIB), current="0")
    where = _self_cgroup(tmp_path, "0::/../sibling\n")
    assert pool.cgroup_memory_headroom_bytes(root, self_cgroup=where) == 448 * MIB


# --- the walk really staying inside the mount, rather than spelling it --------
#
# THE TEST ABOVE IS NAMED FOR AN INVARIANT THE CODE DID NOT HOLD, which is the
# recurring shape this unit keeps finding: a claim kept up by spelling. ``..`` is
# refused textually, and text is not the way out. ``Path.read_text`` FOLLOWS
# SYMLINKS, so a component under the mount pointing anywhere on the filesystem
# was read as a level of this process's cgroup, and the docstring on
# ``_cgroup_directories`` said no level outside the mount is read while the
# concrete input below returned a four mebibyte cap from a directory that was
# not under the mount at all.
#
# Not reachable through a real cgroupfs, which permits no symlinks. Reachable
# through the mount point, which is an INJECTED ARGUMENT by this module's own
# design and whose location the residual finding titled "The cgroup mount point
# is read at an assumed location" already records as assumed rather than read.
# Cited by title, because residual numbers are per branch and collide on merge.


def test_a_component_that_symlinks_out_of_the_mount_is_not_read(tmp_path):
    """The escape the ``..`` refusal cannot see, because it is not in the spelling.

    Every level of this path is under the mount as written. One of them is a
    symlink, and what is read is what it points at, which is a cap belonging to
    nothing this process is in. The tightest cap binds, so four mebibytes here
    would size every pool on the machine at zero workers.
    """
    root = _hierarchy(tmp_path)
    _version_two(root, limit="max", current="0")
    outside = tmp_path / "outside"
    outside.mkdir()
    _version_two(outside, limit=str(4 * MIB), current="0")
    (root / "sneaky").symlink_to(outside, target_is_directory=True)
    where = _self_cgroup(tmp_path, "0::/sneaky\n")
    assert pool.cgroup_memory_headroom_bytes(root, self_cgroup=where) is None, (
        "a cap published outside the mount was read as this process's own, through a "
        "path that never spells a climb; containment is decided by the spelling rather "
        "than by where the filesystem actually goes"
    )


def test_a_limit_file_that_symlinks_out_of_the_mount_is_not_read(tmp_path):
    """The same escape one component later, which is where a fix aimed at directories lands.

    Checking every DIRECTORY and then reading ``<directory>/memory.max`` moves the
    hole rather than closing it: that last name is a symlink as readily as the
    ones above it. Same anchor, same test, one component later.
    """
    root = _hierarchy(tmp_path)
    _version_two(root, limit="max", current="0")
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "memory.max").write_text(str(4 * MIB))
    unit = root / "cratekit.service"
    unit.mkdir()
    (unit / "memory.max").symlink_to(outside / "memory.max")
    (unit / "memory.current").write_text("0")
    where = _self_cgroup(tmp_path, "0::/cratekit.service\n")
    assert pool.cgroup_memory_headroom_bytes(root, self_cgroup=where) is None, (
        "a cap file outside the mount was read through a directory that was inside it"
    )


def test_a_symlink_that_stays_inside_the_mount_is_still_read(tmp_path):
    """The other direction, so the containment is not a ban on symlinks.

    What is refused is a level that LANDS outside the mount, not a level that
    happens to be a link. Refusing links outright would answer a machine whose
    cgroup path happens to run through one with "no cap at all", which is looser
    than reading it and is the direction this module cannot afford.
    """
    root = _hierarchy(tmp_path)
    _version_two(root, limit="max", current="0")
    real = root / "real.service"
    real.mkdir()
    _version_two(real, limit=str(512 * MIB), current=str(64 * MIB))
    (root / "link.service").symlink_to(real, target_is_directory=True)
    where = _self_cgroup(tmp_path, "0::/link.service\n")
    assert pool.cgroup_memory_headroom_bytes(root, self_cgroup=where) == 448 * MIB


@pytest.mark.parametrize(
    "text",
    [
        "0::/system.slice/cratekit.service\n\n",
        "0::/system.slice/cratekit.service\n0:",
        "overlayfs\n0::/system.slice/cratekit.service\n",
        "\n0::/system.slice/cratekit.service\n",
    ],
    ids=["a-trailing-blank-line", "a-short-read", "a-line-with-no-colon", "a-leading-blank"],
)
def test_a_line_this_reader_cannot_parse_is_skipped_rather_than_raised_out_of(
    tmp_path, monkeypatch, text
):
    """A parse failure in our own reader must not arrive as "this machine is unreadable".

    ``/proc/self/cgroup`` is one line per hierarchy and every line is meant to be
    ``id:controllers:path``. A trailing blank line, a read that caught the file
    mid write, and a line from a hierarchy that names no path are none of them
    that shape, and unpacking three names out of them raises ``ValueError`` from
    inside :func:`available_bytes`, which is a public function whose docstring
    promises a number.

    WHAT MAKES IT WORSE THAN A CRASH IS WHERE IT LANDS. ``plan_pool`` catches
    everything its reader raises, deliberately and correctly, because that reader
    is an injected seam and a caller's own reader blowing up is not this module's
    crash to take. So a bug in OUR reader arrives as ``MEMORY_UNREADABLE``, which
    is a real answer meaning "this machine could not be measured", and the run
    quietly plans one worker on a four gibibyte service it could read perfectly
    well. Absence read as evidence of absence, and it hides the bug forever.

    The seam's broad catch stays. What is asserted here is the other side of it:
    this module's own reader is TOTAL, so nothing it does ever needs catching.
    """
    import psutil

    root = _hierarchy(tmp_path)
    unit = root / "system.slice" / "cratekit.service"
    unit.mkdir(parents=True)
    _version_two(unit, limit=str(4 * GIB), current="0")
    where = _self_cgroup(tmp_path, text)
    monkeypatch.setattr(
        psutil, "virtual_memory", lambda: SimpleNamespace(available=512 * GIB)
    )

    assert pool.available_bytes(cgroup_root=root, cgroup_self=where) == 4 * GIB
    plan = pool.plan_pool(
        worker_bytes=256 * MIB,
        items=500,
        ceiling=64,
        read_available=lambda: pool.available_bytes(cgroup_root=root, cgroup_self=where),
    )
    assert plan.bound is pool.Bound.AVAILABLE_MEMORY, (
        f"one unparsable line turned a readable four gibibyte cap into "
        f"{plan.bound}, which is what this module says when a machine cannot be "
        f"measured at all"
    )
    assert plan.available_bytes == 4 * GIB
    assert plan.workers == 4


@pytest.mark.parametrize(
    "contents",
    [b"\xff\xfe\x00\x01\n", "0::/a\x00b\n".encode()],
    ids=["not-text-at-all", "a-path-with-a-null-byte"],
)
def test_a_kernel_file_that_is_not_readable_as_text_is_an_absent_reading(
    tmp_path, monkeypatch, contents
):
    """The same shape as the line above, one function earlier, and it is not OSError.

    :func:`_cgroup_text` said in its own docstring that every way of failing to
    read one of these files arrives as ``OSError``. Two do not. Bytes that are
    not valid text raise ``UnicodeDecodeError``, and a path field carrying an
    embedded null byte, which is a thing this walk will happily join onto the
    mount and hand to ``read_text``, raises a bare ``ValueError`` out of the open
    itself. Both escaped the reader, both reached :func:`available_bytes`, and
    both landed in the same place as everything else this module cannot parse:
    reported as a machine that could not be measured.

    There is no reading here, which is an answer this module already has. The
    host's own number stands, exactly as it does on every machine with no cgroups
    at all.
    """
    import psutil

    root = _hierarchy(tmp_path)
    where = tmp_path / "self-cgroup-bytes"
    where.write_bytes(contents)
    monkeypatch.setattr(
        psutil, "virtual_memory", lambda: SimpleNamespace(available=8 * GIB)
    )

    assert pool.cgroup_memory_headroom_bytes(root, self_cgroup=where) is None
    assert pool.available_bytes(cgroup_root=root, cgroup_self=where) == 8 * GIB
    plan = pool.plan_pool(
        worker_bytes=256 * MIB,
        items=500,
        ceiling=64,
        read_available=lambda: pool.available_bytes(cgroup_root=root, cgroup_self=where),
    )
    assert plan.bound is pool.Bound.AVAILABLE_MEMORY


def test_a_capped_service_on_a_huge_host_is_sized_by_the_service(tmp_path, monkeypatch):
    """The failure scenario end to end, and the reason the walk exists.

    Four gibibytes of MemoryMax on a five hundred and twelve gibibyte host. Under
    the host's own reading the plan is the full ceiling, sixty four children each
    holding a model, inside a unit that holds one of them.
    """
    import psutil

    root = _hierarchy(tmp_path)
    unit = root / "system.slice" / "cratekit.service"
    unit.mkdir(parents=True)
    _version_two(unit, limit=str(4 * GIB), current="0")
    where = _self_cgroup(tmp_path, "0::/system.slice/cratekit.service\n")
    monkeypatch.setattr(
        psutil, "virtual_memory", lambda: SimpleNamespace(available=512 * GIB)
    )

    assert pool.available_bytes(cgroup_root=root, cgroup_self=where) == 4 * GIB
    inside = pool.plan_pool(
        worker_bytes=WORKER,
        items=500,
        ceiling=64,
        read_available=lambda: pool.available_bytes(cgroup_root=root, cgroup_self=where),
    )
    host = pool.plan_pool(
        worker_bytes=WORKER, items=500, ceiling=64, read_available=reader(512 * GIB)
    )
    assert host.workers == 64, "the fixture no longer distinguishes the two readings"
    assert inside.workers == 1
    assert inside.in_process is True


def test_the_two_kernel_paths_the_reader_defaults_to_are_the_ones_the_kernel_uses():
    """Two defaults that no test above can execute, spelled out here instead.

    Every cgroup test points the reader at files it wrote itself, which is the
    only way this machine can reach either branch. That leaves the DEFAULTS
    unchecked, and pointed at the wrong place every test above still passes while
    every real container on earth reads as having no cap. The literals are the
    kernel's own documented locations, written here rather than read out of the
    module.
    """
    assert pool.CGROUP_ROOT == Path("/sys/fs/cgroup")
    assert pool.CGROUP_SELF == Path("/proc/self/cgroup")


def test_a_container_capped_below_its_host_is_sized_by_the_cap(tmp_path, monkeypatch):
    """The whole point, driven end to end: the cap decides, and the pool is one.

    Sixty four gibibytes on the host, half a gibibyte for this process. Under
    the host reading alone the plan is the full ceiling, two children each
    holding a model, inside a cgroup that cannot hold one of them.
    """
    import psutil

    _version_two(tmp_path, limit=str(512 * MIB), current=str(64 * MIB))
    monkeypatch.setattr(
        psutil, "virtual_memory", lambda: SimpleNamespace(available=64 * GIB, percent=10.0)
    )

    host_only = pool.plan_pool(
        worker_bytes=WORKER, items=500, ceiling=64, read_available=reader(64 * GIB)
    )
    assert host_only.workers > 1, "the fixture no longer distinguishes the two readings"

    inside = pool.available_bytes(cgroup_root=tmp_path)
    assert inside == 448 * MIB
    capped = pool.plan_pool(
        worker_bytes=WORKER, items=500, ceiling=64, read_available=lambda: inside
    )
    assert capped.workers == 1
    assert capped.in_process is True
    assert capped.bound is pool.Bound.INSUFFICIENT_MEMORY


def test_an_uncapped_machine_reads_exactly_what_the_platform_reports(tmp_path, monkeypatch):
    """The half that gets skipped (P7), and the one that would break every laptop.

    A cgroup guess on a machine that never had one narrows every pool everywhere
    to fix a container nobody is running, which is what a fix that is too
    restrictive looks like from the inside.
    """
    import psutil

    monkeypatch.setattr(psutil, "virtual_memory", lambda: SimpleNamespace(available=7 * GIB))
    assert pool.available_bytes(cgroup_root=tmp_path / "nothing here") == 7 * GIB
    _version_two(tmp_path, limit="max")
    assert pool.available_bytes(cgroup_root=tmp_path) == 7 * GIB


def test_a_host_tighter_than_the_container_cap_still_wins(tmp_path, monkeypatch):
    """The minimum is taken in both directions, because either can be the smaller.

    A generous cap on a busy host is as real as a tight cap on an idle one, and a
    reading that took the cgroup number whenever there was one would size against
    memory the host has already handed to somebody else.
    """
    import psutil

    _version_two(tmp_path, limit=str(32 * GIB), current="0")
    monkeypatch.setattr(psutil, "virtual_memory", lambda: SimpleNamespace(available=1 * GIB))
    assert pool.available_bytes(cgroup_root=tmp_path) == 1 * GIB


def test_the_real_available_reading_is_a_believable_byte_count():
    """The seam is only worth having if the reading behind it is a reading.

    Asserted against the SHAPE rather than a value, for the same reason the
    pressure reading is: the value is a property of whatever this machine is
    doing while the suite runs. What this pins is that the cgroup lookup does
    not break the reader on a machine that has no cgroups, which is this one.
    """
    taken = pool.available_bytes()
    assert isinstance(taken, int) and taken > 0


# ---------------------------------------------------------------------------
# Structural guards, armed today
# ---------------------------------------------------------------------------


def _attributes_read(source: str) -> set[str]:
    """Every attribute name this source reads, from the tree rather than the text."""
    return {
        node.attr for node in ast.walk(parsed(source)) if isinstance(node, ast.Attribute)
    }


def _names_used(source: str) -> set[str]:
    """Every bare name and attribute name in this source, prose excluded."""
    used: set[str] = set()
    for node in ast.walk(parsed(source)):
        if isinstance(node, ast.Attribute):
            used.add(node.attr)
        elif isinstance(node, ast.Name):
            used.add(node.id)
        elif isinstance(node, ast.alias):
            used.add(node.asname or node.name.split(".")[-1])
    return used


def test_the_memory_reading_is_available_and_never_free():
    """Two different numbers, and only one of them answers the question.

    Free memory is what nobody holds at all. Available memory is what a new
    process can obtain, including cache the kernel would evict for it, and on a
    machine that has been doing work those two numbers are nowhere near each
    other. Sizing against free starves every pool on a warm machine.

    Walked rather than grepped: the module explains this distinction in prose, so
    a text search for the wrong word fires on the explanation of why it is wrong.
    """
    read = _attributes_read(POOL_SOURCE)
    assert "available" in read, "the sizing module no longer reads available memory"
    assert "free" not in read, "the sizing module reads FREE memory, which is a different number"
    assert "total" not in read, (
        "the sizing module reads TOTAL memory, which ignores everything already "
        "resident and is the largest wrong answer available"
    )


@pytest.mark.parametrize("spelling", CORE_COUNT_SPELLINGS)
def test_the_sizing_module_never_reads_a_core_count(spelling):
    """The defect this unit exists to end cannot return through the module that ends it.

    Not one spelling: four. ``os.cpu_count`` is the one the source system uses,
    ``os.process_cpu_count`` is its modern replacement, and the two affinity calls
    are what somebody reaches for when they read that the first two ignore
    cgroup limits. All four answer a question about cores, and cores are not the
    resource that runs out.

    The list is a module constant rather than a literal here, because the
    countdown at the bottom of this file asks the same question and used to ask
    it of two spellings while this one asked it of four. One file, one answer.
    """
    assert spelling not in _names_used(POOL_SOURCE)


# --- no module builds its own process pool -----------------------------------
#
# THREAD POOLS ARE LEFT ALONE, DELIBERATELY. Threads share one address space, so
# a second thread does not cost a second model, and acquisition's bounded thread
# pool is paced against a provider rather than against memory. A guard that
# refused it would be refusing correct code, which is how a guard gets routed
# around (P7).
#
# WHAT THIS CANNOT SEE, said out loud so nobody reads the claim as wider than it
# is: a constructor reached through ``getattr`` or ``importlib.import_module``, a
# pool built by a third party such as joblib or torch.multiprocessing, a bare
# ``os.fork``, and a fan out through subprocess. Those are all out of scope here.
# Every one of them is a different question about a different mechanism, and a
# guard that pretended to cover them would be a guard whose silence meant nothing.

_POOL_CONSTRUCTORS = frozenset({"ProcessPoolExecutor", "Pool"})
_POOL_MODULES = frozenset(
    {
        "concurrent.futures",
        "concurrent.futures.process",
        "multiprocessing",
        "multiprocessing.context",
        "multiprocessing.pool",
    }
)
#: The classes whose instances hand out processes. ``SpawnContext().Pool(...)``
#: is a pool built without ever naming ``get_context``.
_CONTEXT_CLASSES = frozenset(
    {"BaseContext", "DefaultContext", "SpawnContext", "ForkContext", "ForkServerContext"}
)
#: Parameter names that say "this is a start-method context" in ordinary code. A
#: context that arrives as an argument cannot be traced to its import, so the
#: receiver is judged by what it is called and by what it is annotated as. Both
#: are weak signals on their own, which is why a module that imports
#: multiprocessing at all is judged on any parameter receiver instead.
_CONTEXT_PARAMETER_NAMES = frozenset({"context", "ctx", "mp_context", "spawn_context"})


def _dotted(node: ast.AST) -> str | None:
    """``a.b.c`` as text, or None when the expression is not a plain name chain."""
    parts: list[str] = []
    current: ast.AST = node
    while isinstance(current, ast.Attribute):
        parts.append(current.attr)
        current = current.value
    if isinstance(current, ast.Name):
        parts.append(current.id)
        return ".".join(reversed(parts))
    return None


def _unwrap(node: ast.AST) -> ast.AST:
    """A walrus is an assignment wearing an expression's clothes. Take the clothes off."""
    while isinstance(node, ast.NamedExpr):
        node = node.value
    return node


def _bindings(tree: ast.AST) -> list[tuple[str, ast.AST]]:
    """Every ``name = value``, in the three forms this language spells it.

    The walrus is here because a context assigned inside an expression is still a
    context, and an earlier version of this walk understood only ``ast.Assign``,
    which made ``(ctx := get_context("spawn")).Pool(9)`` invisible.
    """
    found: list[tuple[str, ast.AST]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                name = _dotted(target)
                if name is not None:
                    found.append((name, _unwrap(node.value)))
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            name = _dotted(node.target)
            if name is not None:
                found.append((name, _unwrap(node.value)))
        elif isinstance(node, ast.NamedExpr):
            name = _dotted(node.target)
            if name is not None:
                found.append((name, _unwrap(node.value)))
    return found


def process_pool_constructions(source: str) -> list[str]:
    """Every place this source builds a process pool, in each import shape it can use.

    Bound to the module the name came from, never to the bare name. ``Pool`` on
    its own is an ordinary word for an ordinary thing, and a guard that fired on
    a connection pool would be muted rather than obeyed.

    THE IMPORT SHAPES ARE DERIVED RATHER THAN LISTED. An earlier version held a
    set of module strings and matched ``node.module`` against it, which meant
    ``from concurrent import futures`` slipped past because that node's module is
    ``concurrent``, and ``from concurrent.futures import process`` slipped past
    because the branch that recognized a submodule was hardcoded to the name
    ``pool``. Both are ordinary idiom, and the second is the exact shape the
    sizing module itself writes. The rule here is one rule: an imported name is a
    pool module if the dotted path it names is one.

    Four more shapes are followed, and every one of them was executed against
    this guard and found silent before it was closed::

        class Wide(ProcessPoolExecutor): pass       # then Wide(...)
        SpawnContext().Pool(...)                    # a context class, not get_context
        def make(): return get_context("spawn")     # then make().Pool(...)
        mp = multiprocessing                        # then mp.Pool(...)

    A context that arrives as a function PARAMETER cannot be traced to an import
    at all, so it is judged by two weaker signals instead: any module that
    imports multiprocessing in any shape, and anywhere else a parameter named or
    annotated as a context. That is deliberately the loosest rule here, and it is
    the one place this guard trades a little precision for the shape that would
    otherwise be trivial to write on purpose.
    """
    tree = parsed(source)
    module_names: set[str] = set()
    imported_modules: set[str] = set()
    symbols: set[str] = set()
    context_classes: set[str] = set()
    context_factories: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in _POOL_MODULES:
                    module_names.add(alias.asname or alias.name)
                    imported_modules.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                submodule = f"{module}.{alias.name}"
                if submodule in _POOL_MODULES:
                    module_names.add(alias.asname or alias.name)
                    imported_modules.add(submodule)
                elif module not in _POOL_MODULES:
                    continue
                elif alias.name in _POOL_CONSTRUCTORS:
                    symbols.add(alias.asname or alias.name)
                    imported_modules.add(module)
                elif alias.name in _CONTEXT_CLASSES:
                    context_classes.add(alias.asname or alias.name)
                    imported_modules.add(module)
                elif alias.name == "get_context":
                    context_factories.add(alias.asname or alias.name)
                    imported_modules.add(module)

    def is_context(node: ast.AST) -> bool:
        """Whether this expression evaluates to a start-method context."""
        node = _unwrap(node)
        if not isinstance(node, ast.Call):
            return False
        func = node.func
        if isinstance(func, ast.Attribute):
            owner = _dotted(func.value)
            if owner not in module_names:
                return False
            return func.attr == "get_context" or func.attr in _CONTEXT_CLASSES
        if isinstance(func, ast.Name):
            return func.id in context_classes or func.id in context_factories
        return False

    functions = [
        node
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    bindings = _bindings(tree)
    contexts: set[str] = set()

    def base_is_a_pool(base: ast.AST) -> bool:
        if isinstance(base, ast.Name):
            return base.id in symbols
        if isinstance(base, ast.Attribute):
            return base.attr in _POOL_CONSTRUCTORS and _dotted(base.value) in module_names
        return False

    # Everything below can name everything else, in either order, so it settles
    # rather than running once: a helper returning a context may be defined after
    # its caller, and a subclass of a subclass is two passes deep.
    settling = True
    while settling:
        settling = False
        for function in functions:
            if function.name in context_factories:
                continue
            returns = [
                node
                for node in ast.walk(function)
                if isinstance(node, ast.Return) and node.value is not None
            ]
            if any(is_context(node.value) for node in returns):
                context_factories.add(function.name)
                settling = True
        for klass in classes:
            if klass.name not in symbols and any(base_is_a_pool(base) for base in klass.bases):
                symbols.add(klass.name)
                settling = True
        for name, value in bindings:
            alias = _dotted(value)
            for known in (module_names, symbols, context_classes, context_factories, contexts):
                if alias in known and name not in known:
                    known.add(name)
                    settling = True
            if is_context(value) and name not in contexts:
                contexts.add(name)
                settling = True

    parameters: dict[str, str | None] = {}
    for function in functions:
        arguments = function.args
        for argument in (
            arguments.posonlyargs + arguments.args + arguments.kwonlyargs
        ):
            parameters[argument.arg] = (
                _dotted(argument.annotation) if argument.annotation is not None else None
            )

    touches_multiprocessing = any(
        name.startswith("multiprocessing") for name in imported_modules
    )

    def receiver_looks_like_a_context(owner: str | None) -> bool:
        if owner is None or owner not in parameters:
            return False
        if touches_multiprocessing:
            return True
        annotation = parameters[owner]
        if annotation is not None and annotation.split(".")[-1] in _CONTEXT_CLASSES:
            return True
        return owner in _CONTEXT_PARAMETER_NAMES

    found: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = _unwrap(node.func)
        if isinstance(func, ast.Name) and func.id in symbols:
            found.append(f"line {node.lineno}: {func.id}")
        elif isinstance(func, ast.Attribute) and func.attr in _POOL_CONSTRUCTORS:
            receiver = _unwrap(func.value)
            owner = _dotted(receiver)
            if (
                owner in module_names
                or owner in contexts
                or is_context(receiver)
                or (func.attr == "Pool" and receiver_looks_like_a_context(owner))
            ):
                found.append(f"line {node.lineno}: {ast.unparse(func)}")
    return sorted(set(found))


CORRECT_SOURCES = (
    # A thread pool is a different question and stays legal.
    "from concurrent.futures import ThreadPoolExecutor\n"
    "with ThreadPoolExecutor(max_workers=4) as pool:\n    pass\n",
    # The ordinary word, used for something that is not this.
    "class ConnectionPool:\n    def Pool(self):\n        return None\n"
    "def make(db):\n    return db.Pool()\n",
    # Routing through the sizing module, which is the shape every caller wants.
    "from cratekit.core import pool\n"
    "def run(plan, work, items):\n    return pool.map_workers(plan, work, items)\n",
    # Naming the start method without building anything.
    "import multiprocessing\n"
    "def method():\n    return multiprocessing.get_context('spawn').get_start_method()\n",
    # A context used for the things that are not pools. This is what the write
    # session's own cross-process test does, and it must stay silent.
    "import multiprocessing as mp\n"
    "def two_processes(target):\n"
    "    ctx = mp.get_context('spawn')\n"
    "    ready = ctx.Event()\n"
    "    return ctx.Process(target=target, args=(ready,))\n",
    # A thread pool built through a subclass, which is still a thread pool.
    "from concurrent.futures import ThreadPoolExecutor\n"
    "class Bounded(ThreadPoolExecutor):\n    pass\n"
    "def run():\n    return Bounded(max_workers=4)\n",
    # Somebody else's connection pool, arriving as an argument with a name that
    # is not a start-method context, in a module that never imports one.
    "def open_store(database):\n    return database.Pool(size=9)\n",
)

EVASIONS = (
    "from concurrent.futures import ProcessPoolExecutor\n"
    "def run():\n    return ProcessPoolExecutor(max_workers=9)\n",
    "from concurrent.futures import ProcessPoolExecutor as PPE\n"
    "def run():\n    return PPE(max_workers=9)\n",
    "import concurrent.futures as futures\n"
    "def run():\n    return futures.ProcessPoolExecutor(max_workers=9)\n",
    "import concurrent.futures\n"
    "def run():\n    return concurrent.futures.ProcessPoolExecutor(max_workers=9)\n",
    "from multiprocessing import Pool\ndef run():\n    return Pool(9)\n",
    "import multiprocessing\ndef run():\n    return multiprocessing.Pool(9)\n",
    "from multiprocessing import pool as mp_pool\ndef run():\n    return mp_pool.Pool(9)\n",
    "import multiprocessing\n"
    "def run():\n"
    "    context = multiprocessing.get_context('spawn')\n"
    "    return context.Pool(9)\n",
    "import multiprocessing\n"
    "def run():\n    return multiprocessing.get_context('spawn').Pool(9)\n",
    # 1. The package imported by its parent. ``node.module`` is ``concurrent``.
    "from concurrent import futures\n"
    "def run():\n    return futures.ProcessPoolExecutor(max_workers=9)\n",
    # 2. The submodule under another name. The old branch matched only "pool".
    "from concurrent.futures import process as _process_pool\n"
    "def run():\n    return _process_pool.ProcessPoolExecutor(max_workers=9)\n",
    # 3. The submodule named outright, in both spellings.
    "from concurrent.futures.process import ProcessPoolExecutor\n"
    "def run():\n    return ProcessPoolExecutor(max_workers=9)\n",
    "import concurrent.futures.process as pp\n"
    "def run():\n    return pp.ProcessPoolExecutor(max_workers=9)\n",
    # 4. A subclass, which is the same pool wearing a local name.
    "from concurrent.futures import ProcessPoolExecutor\n"
    "class WidePool(ProcessPoolExecutor):\n    pass\n"
    "def run():\n    return WidePool(max_workers=9)\n",
    "import multiprocessing.pool\n"
    "class WidePool(multiprocessing.pool.Pool):\n    pass\n"
    "def run():\n    return WidePool(9)\n",
    "from concurrent.futures import ProcessPoolExecutor\n"
    "class Wide(ProcessPoolExecutor):\n    pass\n"
    "class Wider(Wide):\n    pass\n"
    "def run():\n    return Wider(max_workers=9)\n",
    # 5. A context class, never naming get_context.
    "from multiprocessing.context import SpawnContext\n"
    "def run():\n    return SpawnContext().Pool(9)\n",
    "import multiprocessing.context\n"
    "def run():\n    return multiprocessing.context.SpawnContext().Pool(9)\n",
    # 6. A context that never passes through a plain assignment.
    "import multiprocessing\n"
    "def spawned():\n    return multiprocessing.get_context('spawn')\n"
    "def run():\n    return spawned().Pool(9)\n",
    "import multiprocessing\n"
    "def spawned():\n    return multiprocessing.get_context('spawn')\n"
    "def run():\n    context = spawned()\n    return context.Pool(9)\n",
    "import multiprocessing\n"
    "def run():\n"
    "    return (context := multiprocessing.get_context('spawn')).Pool(9)\n",
    "from multiprocessing import get_context\n"
    "def run():\n    return get_context('spawn').Pool(9)\n",
    "import multiprocessing\n"
    "def run(context):\n    return context.Pool(9)\n",
    "def run(context):\n    return context.Pool(9)\n",
    "from multiprocessing.context import BaseContext\n"
    "def run(where: BaseContext):\n    return where.Pool(9)\n",
    # 7. The module rebound to a local name.
    "import multiprocessing\nmp = multiprocessing\n"
    "def run():\n    return mp.Pool(9)\n",
    "import multiprocessing\nmp = multiprocessing\nlibrary = mp\n"
    "def run():\n    return library.Pool(9)\n",
)


@pytest.mark.parametrize("source", CORRECT_SOURCES, ids=range(len(CORRECT_SOURCES)))
def test_the_pool_construction_guard_stays_silent_on_correct_code(source):
    """Half the job. The other half is the half that keeps getting skipped (P7)."""
    assert process_pool_constructions(source) == []


@pytest.mark.parametrize("source", EVASIONS, ids=range(len(EVASIONS)))
def test_the_pool_construction_guard_bites_every_import_shape(source):
    """An aliased import defeated the armed guard in an earlier unit. Not this one.

    Seven more shapes joined this list after a reviewer executed them against the
    guard and found every one of them silent. Two of the seven are ordinary
    idiom rather than anything anybody would write to evade a check, and one of
    those is the exact import shape the sizing module itself uses.
    """
    assert process_pool_constructions(source) != []


#: Every tree in this repository that is this product's own Python. The walk used
#: to be the package alone while the claim above it said "no module anywhere",
#: which left ``scripts/`` and every test helper outside a sentence that said
#: they were inside. A guard whose promise is wider than its walk is a promise
#: somebody relies on.
WALK_ROOTS = (PACKAGE_ROOT, REPO_ROOT / "scripts", REPO_ROOT / "tests")


def repository_modules(roots=WALK_ROOTS) -> list[Path]:
    """Every module under the walked trees, minus the vendored one and the sizing one.

    The vendored tree is out of scope: it is code this product did not write and
    does not restyle, and its pools are threads in any case. The sizing module is
    out of scope because it is the one place a process pool is allowed to exist.
    """
    return [
        path
        for root in roots
        for path in sorted(root.rglob("*.py"))
        if "_vendor" not in path.parts and path != POOL_PATH
    ]


def package_for(
    path: Path, *, source_root: Path = SRC_ROOT, repo_root: Path = REPO_ROOT
) -> str | None:
    """The dotted package a walked file sits in, for the relative import question.

    THE PIECE THE WALK ALREADY HAD AND DID NOT PASS ON. ``repository_modules``
    yields paths and every caller threw the path away at ``read_text()``, so
    ``ImportsOf`` was given source text and a target module name and nothing
    else, and could only match a relative import by its dotted tail. Passing this
    makes that half exact.

    The shipped package is measured from ``src`` so a module comes out as
    ``cratekit.core``; anything else is measured from the repository root, which
    gives ``scripts`` and ``tests``. Neither of those is an importable package,
    and a file in one cannot legally write a relative import at all, so what they
    resolve to matters less than that they are not ``cratekit.anything``.

    Both roots are arguments so the walk below can be driven over a tree a test
    wrote. There are no relative imports anywhere under ``src/cratekit`` today,
    so on the real tree this argument changes no answer at all, and a wire that
    changes no answer is a wire somebody unplugs while tidying.
    """
    return package_of(path, source_root if source_root in path.parents else repo_root)


def plans_built_outside_the_sizing_module(
    paths: list[Path], *, source_root: Path = SRC_ROOT, repo_root: Path = REPO_ROOT
) -> dict[str, list[str]]:
    """Every walked file that builds a :class:`PoolPlan`, keyed by where it sits.

    A function rather than a loop inside the test, so the same code that runs
    over the shipped tree can be run over a tree written for the purpose. The
    real tree cannot exercise the package argument, because it holds no relative
    import to resolve.
    """
    offenders: dict[str, list[str]] = {}
    for path in paths:
        found = pool_plan_constructions(
            path.read_text(),
            package=package_for(path, source_root=source_root, repo_root=repo_root),
        )
        if found:
            offenders[str(path.relative_to(repo_root))] = found
    return offenders


def test_no_module_outside_the_sizing_module_builds_a_process_pool():
    """Armed today, over every tree this repository writes, so the shape cannot arrive quietly.

    Every process pool in this product is sized by one decision. A module that
    builds its own gets its own copy of that decision, the copies drift, and the
    one that drifts is the one nobody is looking at. Scripts and test helpers are
    walked too: a nine-wide pool started by a maintenance script is nine copies
    of a model on the same machine, and the machine does not care which directory
    the file was in.
    """
    offenders: dict[str, list[str]] = {}
    for path in repository_modules():
        found = process_pool_constructions(path.read_text())
        if found:
            offenders[str(path.relative_to(REPO_ROOT))] = found
    assert not offenders, (
        f"process pools built outside the sizing module: {offenders}. Route them "
        f"through cratekit.core.pool so one memory decision governs every pool (R23)."
    )


def test_the_sizing_module_would_fail_its_own_guard():
    """The guard is only worth running if it can still see the thing it looks for.

    Every path above is an exclusion, and an exclusion list is how a guard ends
    up walking a tree in which nothing is detectable any more. The one module
    that legitimately builds a pool is asserted to be detected, so a refactor
    that quietly stops the walk from recognizing an executor fails here rather
    than passing everywhere.
    """
    assert process_pool_constructions(POOL_SOURCE) != []


# --- no module fabricates a plan ---------------------------------------------


def pool_plan_constructions(source: str, *, package: str | None = None) -> list[str]:
    """Every place this source builds a :class:`PoolPlan` of its own.

    THE ESCAPE ONE LEVEL UP FROM A PRIVATE POOL, and the one that was live. A
    module can route through the right seam, call the right function to run the
    work, and still choose nine workers, because ``map_workers`` accepts any plan
    and asks nothing about where it came from. That satisfies every question
    about seams while spawning nine model-loading children.

    Bound through the import graph rather than to the bare name, so somebody
    else's class called ``PoolPlan`` is not this and does not fire. ``package``
    is where the source sits, and it is what stops a relative import in an
    unrelated package from being read as a relative import of this one.
    """
    tree = parsed(source)
    imports = ImportsOf(tree, POOL_MODULE, package)
    if not imports.reaches:
        return []
    return sorted(
        f"line {node.lineno}: {ast.unparse(node.func)}"
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and imports.resolves(node.func, "PoolPlan")
    )


PLAN_PROVENANCE_CORRECT = (
    # The shape every caller wants: measured, planned, run.
    "from cratekit.core import pool\n"
    "def run(items, cost):\n"
    "    plan = pool.plan_pool(worker_bytes=cost, items=len(items))\n"
    "    return pool.map_workers(plan, analyse, items)\n"
    "def analyse(item):\n    return item\n",
    # A plan that arrived from a caller. Legitimate, and safe precisely because
    # nothing in the package is allowed to have built it by hand.
    "from cratekit.core import pool\n"
    "def run(plan, items):\n    return pool.map_workers(plan, analyse, items)\n"
    "def analyse(item):\n    return item\n",
    # Naming the type without building one.
    "from cratekit.core.pool import PoolPlan\n"
    "def describe(plan: PoolPlan) -> str:\n    return plan.explain()\n",
    # Somebody else's class of the same name, which is not this one.
    "from elsewhere import PoolPlan\n"
    "def run():\n    return PoolPlan(workers=9)\n",
    # A SIBLING INSIDE cratekit/core, in the relative shape such a module writes.
    # The walk was blind to this one in BOTH directions, and the false negative
    # is the cheaper half: it could not see a fabricated plan written this way,
    # and it could not see this correct call either, so the countdown would have
    # reported a correctly sized package as having no planner at all.
    "from . import pool\n"
    "def run(items, cost):\n"
    "    plan = pool.plan_pool(worker_bytes=cost, items=len(items))\n"
    "    return pool.map_workers(plan, analyse, items)\n"
    "def analyse(item):\n    return item\n",
    # The same through an ancestor package, which is ordinary idiom.
    "from cratekit import core\n"
    "def run(items, cost):\n"
    "    plan = core.pool.plan_pool(worker_bytes=cost, items=len(items))\n"
    "    return core.pool.map_workers(plan, analyse, items)\n"
    "def analyse(item):\n    return item\n",
)

PLAN_PROVENANCE_EVASIONS = (
    # The reviewer's evasion, verbatim in shape: the right seam, the wrong number.
    "from cratekit.core import pool\n"
    "def run(items):\n"
    "    plan = pool.PoolPlan(workers=9, items=len(items), bound=pool.Bound.CEILING,\n"
    "                         worker_bytes=1024 ** 3, available_bytes=None,\n"
    "                         max_tasks_per_child=100)\n"
    "    return pool.map_workers(plan, analyse, items)\n"
    "def analyse(item):\n    return item\n",
    # The same thing with the count taken from the cores, which is the whole
    # defect wearing this module's name.
    "import os\n"
    "from cratekit.core import pool\n"
    "def run(items):\n"
    "    plan = pool.PoolPlan(workers=len(os.sched_getaffinity(0)) - 2, items=len(items),\n"
    "                         bound=pool.Bound.CEILING, worker_bytes=1024 ** 3,\n"
    "                         available_bytes=None, max_tasks_per_child=100)\n"
    "    return pool.map_workers(plan, analyse, items)\n"
    "def analyse(item):\n    return item\n",
    # Every import shape, because one of them defeated a guard once already.
    "from cratekit.core.pool import PoolPlan, map_workers\n"
    "def run(items):\n"
    "    return map_workers(PoolPlan(workers=9, items=1, bound=None, worker_bytes=1,\n"
    "                                available_bytes=None, max_tasks_per_child=None),\n"
    "                       analyse, items)\n"
    "def analyse(item):\n    return item\n",
    "import cratekit.core.pool as sizing\n"
    "def run(items):\n"
    "    return sizing.PoolPlan(workers=9, items=1, bound=None, worker_bytes=1,\n"
    "                           available_bytes=None, max_tasks_per_child=None)\n",
    # FIVE SHAPES THAT REACH THE MODULE THROUGH AN ANCESTOR PACKAGE, every one of
    # them executed against this guard and found silent. The walk was keyed on
    # the module's own dotted path, so a source that never spells that path was
    # not merely allowed, it was not examined: the guard returned an empty list
    # before looking at a single call. The pool construction guard above had
    # already closed exactly this shape for its own question, by deriving the
    # import shapes rather than listing them, and the two walks sat in one file
    # giving two different answers.
    "import cratekit.core\n"
    "def run(items):\n"
    "    return cratekit.core.pool.PoolPlan(workers=9, items=1, bound=None,\n"
    "                                       worker_bytes=1, available_bytes=None,\n"
    "                                       max_tasks_per_child=None)\n",
    "from cratekit import core\n"
    "def run(items):\n"
    "    return core.pool.PoolPlan(workers=9, items=1, bound=None, worker_bytes=1,\n"
    "                              available_bytes=None, max_tasks_per_child=None)\n",
    "import cratekit\n"
    "def run(items):\n"
    "    return cratekit.core.pool.PoolPlan(workers=9, items=1, bound=None,\n"
    "                                       worker_bytes=1, available_bytes=None,\n"
    "                                       max_tasks_per_child=None)\n",
    # The two a sibling inside cratekit/core writes, which is the package the
    # sizing module itself lives in and therefore the likeliest place of all.
    "from . import pool\n"
    "def run(items):\n"
    "    return pool.PoolPlan(workers=9, items=1, bound=None, worker_bytes=1,\n"
    "                         available_bytes=None, max_tasks_per_child=None)\n",
    "from .pool import PoolPlan\n"
    "def run(items):\n"
    "    return PoolPlan(workers=9, items=1, bound=None, worker_bytes=1,\n"
    "                    available_bytes=None, max_tasks_per_child=None)\n",
)


@pytest.mark.parametrize(
    "source", PLAN_PROVENANCE_CORRECT, ids=range(len(PLAN_PROVENANCE_CORRECT))
)
def test_the_plan_provenance_guard_stays_silent_on_correct_code(source):
    assert pool_plan_constructions(source) == []


@pytest.mark.parametrize(
    "source", PLAN_PROVENANCE_EVASIONS, ids=range(len(PLAN_PROVENANCE_EVASIONS))
)
def test_the_plan_provenance_guard_bites_a_plan_somebody_typed(source):
    assert pool_plan_constructions(source) != []


# --- the relative half, which was the guard's one false direction ------------
#
# THE WALK HANDLES EVERY ABSOLUTE SHAPE AND PRODUCES NO FALSE POSITIVE ON ANY OF
# THEM, because it DERIVES the shapes from the module's own name rather than
# listing them. The relative shapes were the exception and they were matched by
# dotted tail, which cannot be right: given source text and a target module name
# and nothing else, the walk could not know which package the importing file sat
# in, so a file in an unrelated package writing any of the five shapes below
# fired. All five were executed against it and all five were false positives.
#
# Harmless in this repository today, and verified so: there are no relative
# imports anywhere under src/cratekit. Not harmless in the walk, which three
# files ask questions of and which is the one every guard is meant to collapse
# onto.
#
# The fix is small and the data was already there. Every caller walking real
# files holds a Path and threw it away at read_text(). Passing the package makes
# the resolution exact: the dots are counted against the package's own parts and
# the result is compared like any absolute name.

#: A package that has nothing to do with this one, which is the entire point.
UNRELATED_PACKAGE = "somewhere.else"

#: The five relative shapes, each paired with the package it genuinely reaches
#: the sizing module FROM, or None where no package reaches it at all.
#:
#: The last one is None on purpose and is the clearest of the five: relative
#: imports cannot climb above the top of a package tree, so ``from .. import
#: cratekit`` can never name the top level ``cratekit`` from anywhere. It ended
#: the same way as an ancestor of the target and that was the whole of the old
#: match.
RELATIVE_SHAPES = (
    (
        "from .pool import PoolPlan\n"
        "def run():\n"
        "    return PoolPlan(workers=9, items=1, bound=None, worker_bytes=1,\n"
        "                    available_bytes=None, max_tasks_per_child=None)\n",
        "cratekit.core",
    ),
    (
        "from . import pool\n"
        "def run():\n"
        "    return pool.PoolPlan(workers=9, items=1, bound=None, worker_bytes=1,\n"
        "                         available_bytes=None, max_tasks_per_child=None)\n",
        "cratekit.core",
    ),
    (
        "from . import core\n"
        "def run():\n"
        "    return core.pool.PoolPlan(workers=9, items=1, bound=None, worker_bytes=1,\n"
        "                              available_bytes=None, max_tasks_per_child=None)\n",
        "cratekit",
    ),
    (
        "from .core.pool import PoolPlan\n"
        "def run():\n"
        "    return PoolPlan(workers=9, items=1, bound=None, worker_bytes=1,\n"
        "                    available_bytes=None, max_tasks_per_child=None)\n",
        "cratekit",
    ),
    (
        "from .. import cratekit\n"
        "def run():\n"
        "    return cratekit.core.pool.PoolPlan(workers=9, items=1, bound=None,\n"
        "                                       worker_bytes=1, available_bytes=None,\n"
        "                                       max_tasks_per_child=None)\n",
        None,
    ),
)

REACHING_RELATIVE_SHAPES = tuple(pair for pair in RELATIVE_SHAPES if pair[1] is not None)


@pytest.mark.parametrize(
    "source,_reaches_from", RELATIVE_SHAPES, ids=range(len(RELATIVE_SHAPES))
)
def test_a_relative_import_in_an_unrelated_package_is_not_this_module(source, _reaches_from):
    """Five false positives, silent now, and the guard is armed over the shipped tree.

    A guard that fires on correct code is a guard people route around (P7), and
    this one fires on a file that has never heard of this product.
    """
    assert pool_plan_constructions(source, package=UNRELATED_PACKAGE) == []


@pytest.mark.parametrize(
    "source,reaches_from",
    REACHING_RELATIVE_SHAPES,
    ids=range(len(REACHING_RELATIVE_SHAPES)),
)
def test_the_same_relative_shapes_still_bite_from_the_package_that_owns_them(
    source, reaches_from
):
    """The other direction, which is the one that must not be lost to the fix.

    The same four lines, written where they really do name the sizing module, are
    a hand built plan of nine children reaching the right seam. Exactness has to
    cut both ways or this is a guard that was switched off rather than corrected.
    """
    assert pool_plan_constructions(source, package=reaches_from) != []


@pytest.mark.parametrize(
    "path,root,expected",
    [
        (SRC_ROOT / "cratekit" / "core" / "pool.py", SRC_ROOT, "cratekit.core"),
        (SRC_ROOT / "cratekit" / "__init__.py", SRC_ROOT, "cratekit"),
        (REPO_ROOT / "scripts" / "board.py", REPO_ROOT, "scripts"),
        (REPO_ROOT / "noxfile.py", REPO_ROOT, None),
        (Path("/elsewhere/thing.py"), SRC_ROOT, None),
    ],
    ids=["a-nested-module", "a-package-root", "a-script", "a-loose-file", "outside-the-tree"],
)
def test_the_package_a_walked_file_sits_in_is_read_off_its_path(path, root, expected):
    """The one piece of information the walk needed and was never handed."""
    assert package_of(path, root) == expected


#: The trees where a fabricated plan is a defect. TESTS ARE NOT HERE, and the
#: exclusion is a decision rather than an oversight: a test that wants to drive
#: ``map_workers`` at a width no reading produces has to build a plan by hand,
#: and a guard that refused it would be refusing the only way to test the seam.
#: The claim this guard makes is about what SHIPS.
PRODUCTION_ROOTS = (PACKAGE_ROOT, REPO_ROOT / "scripts")


def test_no_shipped_module_outside_the_sizing_module_builds_its_own_plan():
    """Armed today, so the escape cannot arrive with the unit that needs it.

    ``map_workers`` accepts any plan and validates nothing about where it came
    from, which is what makes this worth asserting from outside rather than
    inside: a runtime check would have to be told what a legitimate origin looks
    like, and the origin is a fact about the source rather than about the object.
    """
    offenders = plans_built_outside_the_sizing_module(repository_modules(PRODUCTION_ROOTS))
    assert not offenders, (
        f"plans built outside the sizing module: {offenders}. A plan that did not "
        f"come from plan_pool is a worker count nobody derived from memory (R23)."
    )


def test_the_walk_credits_a_relative_import_only_to_the_package_that_owns_it(tmp_path):
    """The threading itself, driven on a tree where a relative import exists.

    ONE LINE, TWO FILES, TWO ANSWERS. Both spell the identical relative import
    and build the identical plan of nine. One of them sits inside the package
    that owns the sizing module, where the line really does name it; the other
    sits in a package that has never heard of this product, where the same line
    names something else entirely.

    Without the package the walk matched a relative import by its dotted tail and
    reported both, which is a guard firing on code it has no business reading and
    is how a guard gets routed around (P7). The real tree cannot show this: there
    are no relative imports under src/cratekit at all, so the argument changes
    nothing there and reverting it kills nothing there either.
    """
    source = tmp_path / "src"
    inside = source / "cratekit" / "core" / "sibling.py"
    outside = source / "unrelated" / "thing.py"
    for path in (inside, outside):
        path.parent.mkdir(parents=True)
        path.write_text(
            "from .pool import PoolPlan\n"
            "def run():\n"
            "    return PoolPlan(workers=9, items=1, bound=None, worker_bytes=1,\n"
            "                    available_bytes=None, max_tasks_per_child=None)\n"
        )
    offenders = plans_built_outside_the_sizing_module(
        [inside, outside], source_root=source, repo_root=tmp_path
    )
    assert sorted(offenders) == ["src/cratekit/core/sibling.py"]


# ---------------------------------------------------------------------------
# The countdown against the unit that owes the first real pools
# ---------------------------------------------------------------------------


#: Every seam of the sizing module that runs work on a plan. ``map_workers`` was
#: the only one until U241 added the stream, and a guard that named one runner
#: would have let a hand built plan of nine through the other.
PLAN_RUNNERS = ("map_workers", "stream_workers", "WorkStream")


def unplanned_map_workers(source: str, *, package: str | None = None) -> list[str]:
    """Every runner call, :data:`PLAN_RUNNERS`, on a plan this source built for itself.

    The call-site half of the provenance question, and the one that reads at the
    place the damage happens. A plan that arrives as a parameter or off an
    attribute is accepted here, because the guard above forbids any module in the
    shipped tree from having constructed one, which is what makes accepting it
    sound rather than generous.
    """
    tree = parsed(source)
    imports = ImportsOf(tree, POOL_MODULE, package)
    if not imports.reaches:
        return []
    fabricated = {
        name
        for name, value in _bindings(tree)
        if isinstance(value, ast.Call) and imports.resolves(value.func, "PoolPlan")
    }
    found: list[str] = []
    for node in ast.walk(tree):
        if not (
            isinstance(node, ast.Call)
            and any(imports.resolves(node.func, runner) for runner in PLAN_RUNNERS)
        ):
            continue
        given = next(
            (keyword.value for keyword in node.keywords if keyword.arg == "plan"),
            node.args[0] if node.args else None,
        )
        if given is None:
            continue
        given = _unwrap(given)
        if isinstance(given, ast.Call) and imports.resolves(given.func, "PoolPlan"):
            found.append(f"line {node.lineno}: a plan built inline")
        elif _dotted(given) in fabricated:
            found.append(f"line {node.lineno}: a plan built at {_dotted(given)}")
    return found


#: The package the countdown below is about, named once. It is also the package
#: every module in that countdown is treated as sitting in, which is what turns
#: its two relative fixtures from tail matches into resolved imports.
ANALYSIS_PACKAGE = "cratekit.analysis"


def analysis_sizing_violations(
    modules: list[tuple[str, str]], package: str | None = ANALYSIS_PACKAGE
) -> list[str]:
    """Every way a set of modules fails to be sized by this module and by nothing else.

    THE WHOLE COUNTDOWN LIVES HERE rather than in the test body, so the fixtures
    below run the same code the real package will be run through. A guard proved
    against a paraphrase of itself is proved against nothing.

    The claim being enforced, in full, because an earlier version of this
    countdown claimed all of it and checked two thirds of one part of it: the
    package plans through :func:`plan_pool`, runs through :func:`map_workers`
    or the stream beside it, builds no pool of its own in any import shape,
    builds no plan of its own in any import shape, hands no runner a plan it
    fabricated, and reads no core count in any of the four spellings. Since
    U241 the light pass takes a CEILING from the cores, through
    ``cratekit.core.cores``; ``tests/test_cores.py`` holds that reader to being
    the only one and its answer to reaching the planner's ceiling alone.
    """
    if not modules:
        return ["the analysis package landed with no modules in it"]

    problems: list[str] = []
    if not any(
        calls_attribute(source, POOL_MODULE, "plan_pool", package=package)
        for _name, source in modules
    ):
        problems.append(
            "no module in the analysis package calls cratekit.core.pool.plan_pool; a "
            "pool sized anywhere else is a second answer to R23"
        )
    if not any(
        calls_attribute(source, POOL_MODULE, runner, package=package)
        for _name, source in modules
        for runner in ("map_workers", "stream_workers")
    ):
        problems.append(
            "the analysis package plans a pool and never runs work through "
            "cratekit.core.pool.map_workers or stream_workers, so the branch that "
            "keeps a cap of one in process is the caller's own copy"
        )
    for name, source in modules:
        for where in process_pool_constructions(source):
            problems.append(f"{name} builds its own process pool at {where}")
        for where in pool_plan_constructions(source, package=package):
            problems.append(
                f"{name} builds its own PoolPlan at {where}, which is a worker count "
                f"nobody derived from memory reaching map_workers through the right seam"
            )
        for where in unplanned_map_workers(source, package=package):
            problems.append(f"{name} runs a pool on a plan it built itself, at {where}")
        leaked = sorted(set(CORE_COUNT_SPELLINGS) & _names_used(source))
        if leaked:
            problems.append(
                f"{name} reads a core count ({', '.join(leaked)}), which is the "
                f"nine-worker spike this unit exists to end"
            )
    return problems


_ANALYSIS_LIGHT = (
    "light.py",
    "from cratekit.core import pool\n"
    "def run(items, cost):\n"
    "    plan = pool.plan_pool(worker_bytes=cost, items=len(items))\n"
    "    return pool.map_workers(plan, analyse, items)\n"
    "def analyse(item):\n    return item\n",
)

ANALYSIS_CORRECT = (
    # Two passes, each sizing itself through the seam.
    [
        _ANALYSIS_LIGHT,
        (
            "vocals.py",
            "from cratekit.core import pool\n"
            "def run(items, cost):\n"
            "    plan = pool.plan_pool(worker_bytes=cost, items=len(items), ceiling=2)\n"
            "    return pool.map_workers(plan, analyse, items)\n"
            "def analyse(item):\n    return item\n",
        ),
    ],
    # One pass plans, a shared runner runs. Split across modules and still correct.
    [
        _ANALYSIS_LIGHT,
        (
            "shared.py",
            "from cratekit.core import pool\n"
            "def run(plan, items, analyse):\n"
            "    return pool.map_workers(plan, analyse, items)\n",
        ),
    ],
    # Correctly sized through an ancestor package, which the walk could not see.
    # This one is the false ACCUSATION rather than the missed evasion: before the
    # walk was widened the countdown reported this package as calling neither the
    # planner nor the runner, and a guard that fires on correct code is a guard
    # somebody routes around (P7).
    [
        (
            "light.py",
            "from cratekit import core\n"
            "def run(items, cost):\n"
            "    plan = core.pool.plan_pool(worker_bytes=cost, items=len(items))\n"
            "    return core.pool.map_workers(plan, analyse, items)\n"
            "def analyse(item):\n    return item\n",
        ),
    ],
    # The same false accusation through a relative import, which is what a module
    # inside the package one level over actually writes.
    #
    # THE TWO RELATIVE SHAPES ARE TWO PACKAGES HERE, NOT TWO MODULES IN ONE, and
    # that is the whole reason they discriminate. The countdown asks whether ANY
    # module in the package calls the planner, so a package holding both shapes
    # covers for itself: break the walk's handling of either one and the other
    # still answers, and the fixture passes while half the walk is dead.
    [
        (
            "light.py",
            "from ..core import pool\n"
            "def run(items, cost):\n"
            "    plan = pool.plan_pool(worker_bytes=cost, items=len(items))\n"
            "    return pool.map_workers(plan, analyse, items)\n"
            "def analyse(item):\n    return item\n",
        ),
    ],
    [
        (
            "light.py",
            "from ..core.pool import map_workers, plan_pool\n"
            "def run(items, cost):\n"
            "    plan = plan_pool(worker_bytes=cost, items=len(items), ceiling=2)\n"
            "    return map_workers(plan, analyse, items)\n"
            "def analyse(item):\n    return item\n",
        ),
    ],
    # U241's shape: the plan from the planner under a ceiling from the one core
    # reader, the work run through the stream, results read by position.
    [
        (
            "ahead.py",
            "from cratekit.core import cores, pool\n"
            "def run(items, cost):\n"
            "    plan = pool.plan_pool(worker_bytes=cost, items=len(items),\n"
            "                          ceiling=cores.worker_ceiling(reserved=2))\n"
            "    with pool.stream_workers(plan, analyse, items) as stream:\n"
            "        return [stream.result(at) for at in range(len(items))]\n"
            "def analyse(item):\n    return item\n",
        ),
    ],
    # A SIBLING OF THE ANALYSIS PACKAGE'S OWN, spelled the same way the sizing
    # module would be. ``from .pool import PoolPlan`` inside cratekit.analysis
    # names cratekit.analysis.pool, which is not this module and not this class,
    # and the countdown must not accuse the package of building its own plan for
    # it. Matched by dotted tail it was read as the sizing module and the package
    # was accused. This is the one fixture here that the package argument decides,
    # and the collision it turns on is exactly the one this repository already
    # hunts: one word meaning two things in two modules.
    [
        _ANALYSIS_LIGHT,
        (
            "grouping.py",
            "from .pool import PoolPlan\n"
            "def group(tracks):\n    return PoolPlan(tracks)\n",
        ),
    ],
)

ANALYSIS_EVASIONS = (
    # THE VERIFIED EVASION. light.py is sized correctly, vocals.py hands the same
    # seam a plan of nine, and the old countdown passed because SOME module
    # called plan_pool and SOME module called map_workers.
    [
        _ANALYSIS_LIGHT,
        (
            "vocals.py",
            "from cratekit.core import pool\n"
            "def run(items):\n"
            "    plan = pool.PoolPlan(workers=9, items=len(items), bound=pool.Bound.CEILING,\n"
            "                         worker_bytes=1024 ** 3, available_bytes=None,\n"
            "                         max_tasks_per_child=100)\n"
            "    return pool.map_workers(plan, analyse, items)\n"
            "def analyse(item):\n    return item\n",
        ),
    ],
    # The same evasion with the count taken from the cores, at the spelling the
    # countdown did not check while the guard beside it did.
    [
        _ANALYSIS_LIGHT,
        (
            "vocals.py",
            "import os\n"
            "from cratekit.core import pool\n"
            "def run(items):\n"
            "    plan = pool.PoolPlan(workers=len(os.sched_getaffinity(0)) - 2,\n"
            "                         items=len(items), bound=pool.Bound.CEILING,\n"
            "                         worker_bytes=1024 ** 3, available_bytes=None,\n"
            "                         max_tasks_per_child=100)\n"
            "    return pool.map_workers(plan, analyse, items)\n"
            "def analyse(item):\n    return item\n",
        ),
    ],
    # A private pool, which is the shape the repository-wide guard already covers
    # and which the countdown must not be blind to inside its own package.
    [
        _ANALYSIS_LIGHT,
        (
            "vocals.py",
            "from concurrent.futures import ProcessPoolExecutor\n"
            "def run(items):\n"
            "    with ProcessPoolExecutor(max_workers=9) as workers:\n"
            "        return list(workers.map(analyse, items))\n"
            "def analyse(item):\n    return item\n",
        ),
    ],
    # The hand built plan again, through an ancestor package. Nine children, one
    # import line different, and invisible to the countdown until the walk under
    # it learned the shape.
    [
        _ANALYSIS_LIGHT,
        (
            "vocals.py",
            "from cratekit import core\n"
            "def run(items):\n"
            "    plan = core.pool.PoolPlan(workers=9, items=len(items),\n"
            "                              bound=core.pool.Bound.CEILING,\n"
            "                              worker_bytes=1024 ** 3, available_bytes=None,\n"
            "                              max_tasks_per_child=100)\n"
            "    return core.pool.map_workers(plan, analyse, items)\n"
            "def analyse(item):\n    return item\n",
        ),
    ],
    # The hand built plan again, through the seam U241 added. A guard that named
    # only map_workers let these nine children through the stream.
    [
        _ANALYSIS_LIGHT,
        (
            "ahead.py",
            "from cratekit.core import pool\n"
            "def run(items):\n"
            "    plan = pool.PoolPlan(workers=9, items=len(items), bound=pool.Bound.CEILING,\n"
            "                         worker_bytes=1024 ** 3, available_bytes=None,\n"
            "                         max_tasks_per_child=100)\n"
            "    return pool.stream_workers(plan, analyse, items)\n"
            "def analyse(item):\n    return item\n",
        ),
    ],
    # Nothing sizes anything.
    [
        (
            "light.py",
            "def run(items):\n    return [analyse(item) for item in items]\n"
            "def analyse(item):\n    return item\n",
        )
    ],
    # The package landed empty.
    [],
)


@pytest.mark.parametrize(
    "modules",
    ANALYSIS_CORRECT,
    ids=[
        "two-passes",
        "split-planner",
        "ancestor-package",
        "relative-package-import",
        "relative-symbol-import",
        "the-stream-under-a-core-ceiling",
        "a-sibling-of-its-own-named-pool",
    ],
)
def test_the_analysis_countdown_stays_silent_on_correctly_sized_modules(modules):
    """The half that gets skipped, run before the half that does not (P7)."""
    assert analysis_sizing_violations(modules) == []


@pytest.mark.parametrize(
    "modules",
    ANALYSIS_EVASIONS,
    ids=[
        "hand-built-plan",
        "core-count-in-a-hand-built-plan",
        "private-pool",
        "hand-built-plan-through-an-ancestor",
        "hand-built-plan-through-the-stream",
        "no-sizing",
        "empty",
    ],
)
def test_the_analysis_countdown_bites_the_evasions_that_used_to_pass_it(modules):
    """Two of these passed the countdown as first written, and both spawn nine children."""
    assert analysis_sizing_violations(modules) != []


def test_the_analysis_pools_are_sized_here_and_never_by_the_core_count():
    """U25's obligation, registered because U12 is the unit it would silently undo.

    This unit ships the mechanism and nothing that uses it, so R23 is a claim
    about a module rather than about a run until the first heavy pass lands.
    U25 ports the two-pass split, and the source system sizes BOTH of its passes
    from the core count. A port that carries that arithmetic across satisfies
    every arithmetic test in this file while reproducing the exact kill the unit
    exists to prevent.

    THE FIRST VERSION OF THIS TEST CLAIMED MORE THAN IT CHECKED. It asserted that
    both pools were sized here and by nothing else, and it checked that SOME
    module called the planner and SOME module called the runner. A package whose
    light pass was sized correctly and whose vocal pass handed the same runner a
    plan of nine passed it. The body is now :func:`analysis_sizing_violations`,
    which is proved in both directions against fixtures above, and the register
    entry says what that function enforces rather than what it was hoped to.
    """
    problems = analysis_sizing_violations(
        package_modules(PACKAGE_ROOT / "analysis")
    )
    assert not problems, "the analysis package is not sized here:\n" + "\n".join(problems)
