"""U12: the worker count is decided by memory, tested at the edges (R23).

Mostly arithmetic on injected readings; real processes only where nothing else can
answer. The structural guards walk the syntax tree, with fixtures both ways (P7).
"""

from __future__ import annotations

import ast
import multiprocessing
import os
import signal
import subprocess
import sys
import time
import unicodedata
from concurrent.futures import process as _process_pool
from pathlib import Path
from types import SimpleNamespace

import pytest

from cratekit.core import pool
from tests._source_guards import ImportsOf, calls_attribute, package_modules, package_of

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"
PACKAGE_ROOT = SRC_ROOT / "cratekit"
POOL_PATH = PACKAGE_ROOT / "core" / "pool.py"

#: The module every question below is asked about, named once.
POOL_MODULE = "cratekit.core.pool"
#: The two doors to it (U331). A feature package may import only the named
#: interface, so the analysis package reaches the planner through ``core.jobs``,
#: which answers for the sizing names; a use through either door is a use of
#: the planner, and a plan built by hand through either is a plan built by hand.
POOL_DOORS = (POOL_MODULE, "cratekit.core.jobs")
POOL_SOURCE = POOL_PATH.read_text()

MIB = 1024**2
GIB = 1024**3

#: A stand-in for one model-loading worker: the source system's vocal worker budget.
WORKER = 1 * GIB

#: The four ways to ask for a core count, named once for the guard and the U25 countdown.
CORE_COUNT_SPELLINGS = ("cpu_count", "process_cpu_count", "sched_getaffinity", "cpu_affinity")


@pytest.fixture(autouse=True)
def _a_machine_that_is_not_under_pressure(monkeypatch):
    """Every test sees an idle machine unless it passes its own pressure reading."""
    monkeypatch.setattr(
        pool, "memory_pressure", lambda: pool.Pressure(swap_used_bytes=0, used_percent=10.0)
    )


def reader(value: int):
    """A memory reading that always answers ``value``. Never touches the machine."""
    return lambda: value


def pressure(*, swap_used_bytes: int = 0, used_percent: float = 10.0):
    """A pressure reading that always answers these two numbers."""
    return lambda: pool.Pressure(swap_used_bytes=swap_used_bytes, used_percent=used_percent)


# NEITHER HELPER BELOW IS A PIN; the literal pins on the constants are not duplicates.


def affordable_for(
    available: int, *, worker_bytes: int = WORKER, percent: int | None = None,
    reserve: int | None = None,
) -> int:
    """How many workers the RULE affords at this reading, derived from the rule. NOT A PIN."""
    percent = pool.DEFAULT_HEADROOM_PERCENT if percent is None else percent
    reserve = pool.DEFAULT_MEMORY_RESERVE_BYTES if reserve is None else reserve
    return max(0, available - reserve) * percent // 100 // worker_bytes


def threshold_for(
    workers: int, *, worker_bytes: int = WORKER, percent: int, reserve: int | None = None
) -> int:
    """The smallest reading that affords ``workers``; the reserve is added back. NOT A PIN."""
    reserve = pool.DEFAULT_MEMORY_RESERVE_BYTES if reserve is None else reserve
    return reserve + -(-workers * worker_bytes * 100 // percent)


def _plan(available: int, **arguments) -> pool.PoolPlan:
    """``plan_pool`` at this reading, for a one GiB worker and 500 items unless told."""
    arguments = {"worker_bytes": WORKER, "items": 500, **arguments}
    return pool.plan_pool(**arguments, read_available=reader(available))


# The plan's own scenarios


def test_two_gigabytes_against_a_one_gigabyte_worker_runs_in_process():
    """First scenario: 2 GiB affords none under the reserve, so one worker in process."""
    plan = _plan(2 * GIB)
    assert plan.workers == 1
    assert plan.in_process is True
    assert plan.bound is pool.Bound.INSUFFICIENT_MEMORY
    assert plan.max_tasks_per_child is None


@pytest.mark.parametrize(
    "available", [16 * GIB, 64 * GIB], ids=["the-plans-second-scenario", "a-roomy-machine"]
)
def test_the_default_ceiling_of_two_binds_where_memory_affords_several(available):
    """The shipped ceiling is two, pinned by the pool such a machine gets."""
    # The guard is derived, NOT a pin (see affordable_for); the count is a literal.
    assert affordable_for(available) > 2, (
        "the fixture no longer leaves the ceiling as the binding constraint"
    )
    plan = _plan(available)
    assert plan.workers == 2
    assert plan.bound is pool.Bound.CEILING


def test_sixteen_gigabytes_is_bound_by_the_headroom_once_the_ceiling_is_raised():
    """With the ceiling raised, the reserve and headroom bind: never sixteen workers from 16 GiB."""
    plan = _plan(16 * GIB, ceiling=64)
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
    """An unreadable machine gets one worker, never the ceiling, items or recycle count given."""
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
    """A nonsense reading lands like an exception. ``True`` equals one and must not size a pool."""
    plan = pool.plan_pool(worker_bytes=WORKER, items=500, read_available=lambda: value)
    assert plan.workers == 1
    assert plan.bound is pool.Bound.MEMORY_UNREADABLE
    assert plan.available_bytes is None


def test_the_core_count_does_not_change_the_computed_cap():
    """The plan's fourth scenario: the cap is the same at one core and at sixty four."""
    made = []
    for cores in (1, 64):
        with pytest.MonkeyPatch.context() as patch:
            patch.setattr(os, "cpu_count", lambda cores=cores: cores)
            patch.setattr(multiprocessing, "cpu_count", lambda cores=cores: cores)
            made.append(_plan(16 * GIB, ceiling=64))
    assert made[0] == made[1]
    assert made[0].workers == affordable_for(16 * GIB)


# The edges, which is where a headroom factor and a hard ceiling disagree


@pytest.mark.parametrize("workers", [2, 3, 4])
def test_the_worker_count_flips_exactly_at_the_affordable_boundary(workers):
    """One byte below the derived boundary is one fewer worker. Test the edges, not the middle."""
    # Derived, NOT a pin (see affordable_for): the flip is under test.
    edge = threshold_for(workers, percent=pool.DEFAULT_HEADROOM_PERCENT)
    below = _plan(edge - 1, ceiling=64)
    at = _plan(edge, ceiling=64)
    assert below.workers == workers - 1
    assert at.workers == workers


def test_the_headroom_is_applied_to_the_bytes_before_they_are_divided_into_workers():
    """The headroom scales the bytes before they are divided into workers, not the count."""
    available = 2900 * MIB
    percent = 75
    shipped = available * percent // 100 // WORKER
    reversed_order = available // WORKER * percent // 100
    assert shipped != reversed_order, "the fixture no longer distinguishes the two orders"
    plan = _plan(available, ceiling=64, headroom_percent=percent, reserve_bytes=0)
    assert plan.workers == shipped == 2
    assert plan.workers != reversed_order


def test_the_reserve_comes_off_the_reading_before_the_percent_scales_it():
    """The reserve comes off the reading, not the share, so it does not shrink when tight."""
    available = 8 * GIB
    reserve = 2 * GIB
    percent = 50
    shipped = (available - reserve) * percent // 100 // WORKER
    reserve_after = (available * percent // 100 - reserve) // WORKER
    assert shipped != reserve_after, "the fixture no longer distinguishes the two orders"
    plan = _plan(available, ceiling=64, headroom_percent=percent, reserve_bytes=reserve)
    assert plan.workers == shipped == 3
    assert plan.workers != reserve_after


def test_a_reading_smaller_than_the_reserve_affords_nothing_rather_than_going_negative():
    """A reading below the reserve clamps to zero: INSUFFICIENT_MEMORY, never negative."""
    plan = _plan(1 * GIB, ceiling=64, reserve_bytes=4 * GIB)
    assert plan.workers == 1
    assert plan.bound is pool.Bound.INSUFFICIENT_MEMORY


def test_the_hard_ceiling_and_the_headroom_agree_at_the_point_they_cross():
    """Where ceiling and memory tie, the smaller wins and the tie names memory."""
    # Derived, NOT a pin (see affordable_for): the tie is under test.
    edge = threshold_for(2, percent=pool.DEFAULT_HEADROOM_PERCENT)
    tied = _plan(edge, ceiling=2)
    assert tied.workers == 2
    assert tied.bound is pool.Bound.AVAILABLE_MEMORY
    memory_wins = _plan(edge - 1, ceiling=2)
    assert memory_wins.workers == 1
    assert memory_wins.bound is pool.Bound.AVAILABLE_MEMORY


@pytest.mark.parametrize("percent", [1, 25, 50, 75, 99, 100])
def test_no_headroom_setting_ever_affords_more_than_the_reading_itself(percent):
    """At any headroom setting the pool never claims more bytes than the reading."""
    available = 10 * GIB
    plan = _plan(available, ceiling=1024, headroom_percent=percent)
    assert plan.workers * WORKER <= available
    assert plan.workers * WORKER <= max(WORKER, available * percent // 100)


# The headroom judgement, recorded as a measurement rather than as an opinion


@pytest.mark.parametrize(
    "platform,expected",
    [("darwin", 50), ("linux", 75), ("win32", 75)],
)
def test_the_headroom_share_is_lower_where_the_reading_is_measurably_worse(platform, expected):
    """Both platform branches, as literals: darwin's reading is 91 percent inactive queue."""
    assert pool.default_headroom_percent(platform) == expected
    assert pool.DARWIN_HEADROOM_PERCENT < pool.GENERAL_HEADROOM_PERCENT


def test_the_shipped_default_is_the_one_this_platform_earns():
    assert pool.DEFAULT_HEADROOM_PERCENT == pool.default_headroom_percent(sys.platform)


def test_the_machine_the_kill_happened_on_gets_no_pool_under_the_shipped_rule():
    """A reading off the real 18 GiB machine gets one worker where the old rule gave three."""
    measured_available = 5 * GIB + 256 * MIB
    measured_swap = 2 * GIB + 215 * MIB
    measured_used_percent = 70.8

    old_rule = measured_available * 75 // 100 // WORKER
    assert old_rule == 3, "the recorded reading no longer reproduces the old rule's answer"

    plan = _plan(
        measured_available,
        ceiling=64,
        read_pressure=pressure(swap_used_bytes=measured_swap, used_percent=measured_used_percent),
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
    """Either pressure signal gates at its literal line and not one below."""
    plan = _plan(64 * GIB, ceiling=64, read_pressure=pressure(**reading))
    if gated:
        assert plan.workers == 1
        assert plan.bound is pool.Bound.MEMORY_PRESSURE
        assert plan.max_tasks_per_child is None
    else:
        assert plan.workers > 1
        assert plan.bound is not pool.Bound.MEMORY_PRESSURE


def test_a_gated_plan_still_reports_the_reading_it_was_gated_despite():
    """A gated plan still reports the available bytes, so the log can say why it went in process."""
    plan = _plan(6 * GIB, ceiling=64, read_pressure=pressure(swap_used_bytes=3 * GIB))
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
    """An unreadable pressure reading leaves the other brakes standing, unlike available memory."""
    plan = _plan(64 * GIB, ceiling=64, read_pressure=broken_reader)
    assert plan.workers > 1
    assert plan.bound is not pool.Bound.MEMORY_PRESSURE


def test_the_real_pressure_reading_answers_with_two_believable_numbers():
    """The real pressure reading has the shape the gate consumes; its value is the machine's."""
    taken = pool.memory_pressure()
    assert isinstance(taken, pool.Pressure)
    assert isinstance(taken.swap_used_bytes, int) and taken.swap_used_bytes >= 0
    assert 0 <= taken.used_percent <= 100


# The tuning constants, pinned by what they DO
# Each test puts a machine on each side of a number with literals, never reading the
# constant; arms this platform never runs are driven through an argument.


def _workers_for(percent: int) -> int:
    """The pool 100 GiB affords at this headroom: the count equals the percent."""
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(pool, "platform_worker_ceiling", lambda: None)
        plan = _plan(
            100 * GIB,
            worker_bytes=1 * GIB,
            items=10_000,
            ceiling=10_000,
            headroom_percent=percent,
            reserve_bytes=0,
        )
    return plan.workers


@pytest.mark.parametrize(
    "percent,workers",
    [(pool.GENERAL_HEADROOM_PERCENT, 75), (pool.DARWIN_HEADROOM_PERCENT, 50)],
    ids=["general-three-quarters", "darwin-half-as-measured"],
)
def test_each_headroom_share_is_pinned_by_the_pool_it_produces(percent, workers):
    """Both shares, pinned by the pool they produce; darwin's arm never runs here by default."""
    assert _workers_for(percent) == workers


def test_the_absolute_reserve_is_two_gibibytes_of_the_reading_that_was_never_ours():
    """Two GiB of reserve: one worker past it affords one, one byte short affords none."""
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


@pytest.mark.parametrize(
    "swap,gated",
    [(512 * MIB, False), (1 * GIB - 1, False), (1 * GIB, True), (4 * GIB, True)],
    ids=["stale-swap", "one-byte-under", "a-full-gibibyte", "deep-in-swap"],
)
def test_the_swap_threshold_is_a_gibibyte_and_the_gibibyte_is_load_bearing(swap, gated):
    """The swap threshold is a gibibyte; stale darwin swap below it keeps its pool."""
    plan = _plan(64 * GIB, ceiling=64, read_pressure=pressure(swap_used_bytes=swap))
    assert (plan.bound is pool.Bound.MEMORY_PRESSURE) is gated
    assert (plan.workers == 1) is gated


@pytest.mark.parametrize(
    "used,gated",
    [(60.0, False), (84.9, False), (85.0, True), (99.0, True)],
    ids=["a-working-machine", "just-under", "at-the-line", "reclaiming-hard"],
)
def test_the_used_percent_ceiling_is_eighty_five_and_the_number_is_load_bearing(used, gated):
    """Eighty five percent used is where the platform reclaims for ordinary allocations."""
    plan = _plan(64 * GIB, ceiling=64, read_pressure=pressure(used_percent=used))
    assert (plan.bound is pool.Bound.MEMORY_PRESSURE) is gated


@pytest.mark.parametrize(
    "items,generations",
    [(10_000, 50), (500, 3)],
    ids=["a-ten-thousand-track-folder", "an-ordinary-folder"],
)
def test_the_recycle_budget_retires_a_child_occasionally_rather_than_constantly(
    items, generations
):
    """A hundred tasks per child, pinned by how many generations a real folder takes."""
    plan = _plan(64 * GIB, items=items, ceiling=2)
    assert plan.workers == 2
    assert plan.generations == generations


#: A cold load of the 300 MB model in ``_probe_entry`` off a slow platter, written here and
#: used for both edges, so moving it either way pushes the deadline out of the band.
_A_COLD_MODEL_LOAD_SECONDS = 60.0

#: The least generous deadline, in loads: at twice the load a machine twice as slow answers.
_DEADLINE_FLOOR_IN_LOADS = 2.0

#: The most generous, in loads: past this a caller cannot tell the deadline from a hang.
_DEADLINE_CEILING_IN_LOADS = 5.0


def test_the_probe_deadline_the_module_ships_outlasts_the_load_it_waits_for():
    """The shipped probe deadline sits in a band of two to five cold model loads."""
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
        f"deadline {given[0]} is under two cold loads; a slow machine reports the floor"
    )
    assert given[0] <= _DEADLINE_CEILING_IN_LOADS * _A_COLD_MODEL_LOAD_SECONDS, (
        f"deadline {given[0]} is over five cold loads, a hang a caller cannot tell apart"
    )


def test_every_probe_deadline_default_names_the_constant_rather_than_repeating_it():
    """Every ``timeout_seconds`` defaults to the constant, keyword only, forwarded by name."""
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
        f"{sorted(must_carry_it - carrying)} no longer takes {parameter}"
    )
    assert not_keyword_only == set(), f"{sorted(not_keyword_only)} takes {parameter} positionally"
    assert without_a_default == set(), (
        f"{sorted(without_a_default)} takes {parameter} with no default"
    )
    wrong = {name: spelling for name, spelling in defaults.items() if spelling != documented}
    assert wrong == {}, f"a probe deadline default is {wrong}, not {documented}: a second deadline"
    passed_in: list[tuple[str, str]] = [
        (ast.unparse(node.func), ast.unparse(keyword.value))
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        for keyword in node.keywords
        if keyword.arg == parameter
    ]
    assert passed_in, f"no call passes {parameter}, so the call site sweep has nothing to check"
    frozen = [pair for pair in passed_in if pair[1] not in {documented, parameter}]
    assert frozen == [], (
        f"a call passes {frozen} rather than forwarding {parameter} or {documented}"
    )


def test_the_windows_pool_limit_is_the_interpreters_own_and_falls_back_to_sixty_one():
    """Both arms of the windows limit, which never run here: the interpreter's value, else 61."""
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


# Affording exactly one, and affording none, which are two different machines


def test_a_machine_that_affords_exactly_one_worker_says_so():
    # Derived, NOT a pin (see affordable_for): the bound is under test.
    edge = threshold_for(1, percent=pool.DEFAULT_HEADROOM_PERCENT)
    plan = _plan(edge, ceiling=64)
    assert plan.workers == 1
    assert plan.bound is pool.Bound.AVAILABLE_MEMORY


def test_a_machine_that_affords_none_is_not_the_same_machine_and_does_not_say_it_is():
    """Affording one and affording none both run one worker but report different bounds."""
    # Derived, NOT a pin (see affordable_for): the two bounds are under test.
    edge = threshold_for(1, percent=pool.DEFAULT_HEADROOM_PERCENT)
    affords_one = _plan(edge, ceiling=64)
    affords_none = _plan(edge - 1, ceiling=64)
    assert affords_one.workers == affords_none.workers == 1
    assert affords_one.bound is not affords_none.bound
    assert affords_none.bound is pool.Bound.INSUFFICIENT_MEMORY
    assert affords_one.explain() != affords_none.explain()


# The other two bounds, and the refusals


def test_the_item_count_bounds_the_pool_so_no_child_is_started_with_nothing_to_do():
    plan = _plan(64 * GIB, items=3, ceiling=64)
    assert plan.workers == 3
    assert plan.bound is pool.Bound.WORK_ITEMS


def test_no_work_at_all_plans_one_in_process_worker_rather_than_zero():
    """Zero items must not become zero workers. A pool of zero never returns."""
    plan = _plan(64 * GIB, items=0, ceiling=64)
    assert plan.workers == 1
    assert plan.in_process is True
    assert plan.bound is pool.Bound.WORK_ITEMS


def test_one_item_runs_in_process():
    plan = _plan(64 * GIB, items=1, ceiling=64)
    assert plan.in_process is True


def test_the_platform_limit_bounds_the_pool_where_the_platform_has_one():
    """A platform limit reaches the arithmetic, since windows raises above a fixed width."""
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(pool, "platform_worker_ceiling", lambda: 61)
        plan = _plan(64 * GIB, worker_bytes=1 * MIB, items=10_000, ceiling=1024)
    assert plan.workers == 61
    assert plan.bound is pool.Bound.PLATFORM_LIMIT


def test_a_platform_with_no_limit_contributes_nothing_to_the_arithmetic():
    """Absent, never a huge sentinel. A sentinel that always loses is never checked."""
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(pool, "platform_worker_ceiling", lambda: None)
        plan = _plan(64 * GIB, worker_bytes=1 * GIB, items=10_000, ceiling=1024)
    assert plan.workers == affordable_for(64 * GIB)
    assert plan.bound is pool.Bound.AVAILABLE_MEMORY


def test_the_platform_limit_is_the_real_one_for_the_platform_running_this():
    """The real platform limit: 61 on windows, none elsewhere."""
    limit = pool.platform_worker_ceiling()
    if sys.platform == "win32":
        assert limit == 61
    else:
        assert limit is None


@pytest.mark.parametrize(
    "arguments",
    [
        {"worker_bytes": 0}, {"worker_bytes": -1}, {"ceiling": 0}, {"ceiling": -4},
        {"headroom_percent": 0}, {"headroom_percent": 101}, {"reserve_bytes": -1},
        {"swap_pressure_bytes": -1}, {"used_percent_ceiling": 0},
        {"used_percent_ceiling": 101}, {"items": -1}, {"max_tasks_per_child": 0},
        {"max_tasks_per_child": -10},
    ],
)
def test_an_impossible_request_refuses_rather_than_being_repaired(arguments):
    """A bad argument raises rather than being clamped, which would hide the caller."""
    request = {"worker_bytes": WORKER, "items": 10, "read_available": reader(8 * GIB)}
    request.update(arguments)
    with pytest.raises(ValueError):
        pool.plan_pool(**request)


def test_a_plan_reports_what_it_measured_and_what_decided_it():
    plan = _plan(16 * GIB)
    assert plan.available_bytes == 16 * GIB
    assert plan.worker_bytes == WORKER
    assert plan.items == 500
    assert "2 workers" in plan.explain()
    assert pool.BOUND_PHRASES[pool.Bound.CEILING] in plan.explain()


def test_a_plan_of_one_worker_explains_itself_as_in_process():
    plan = _plan(2 * GIB)
    assert plan.explain().startswith("in process")


def test_every_bound_has_a_phrase():
    """Derived by iterating the enum, so the next bound cannot arrive unexplained (P3)."""
    assert set(pool.BOUND_PHRASES) == set(pool.Bound)


def test_the_bound_phrase_table_has_no_duplicate_key():
    """A key written twice collapses at parse time, so the literal is counted from the source."""
    literal = None
    for node in ast.walk(ast.parse(POOL_SOURCE)):
        if isinstance(node, ast.AnnAssign) and getattr(node.target, "id", "") == "BOUND_PHRASES":
            literal = node.value
    assert literal is not None, "BOUND_PHRASES is no longer a module-level annotated assignment"
    written = [ast.unparse(key) for key in literal.args[0].keys]
    duplicates = sorted({key for key in written if written.count(key) > 1})
    assert not duplicates, f"written twice and collapsed at parse time: {duplicates}"
    assert len(written) == len(pool.BOUND_PHRASES)


# The plan carries the item count, which is what made the deadlock unseeable


def test_a_plan_carries_the_item_count_it_was_decided_for():
    """A plan carries its item count, so items against workers times tasks can be checked."""
    plan = _plan(64 * GIB, items=4321, ceiling=4)
    assert plan.items == 4321
    assert plan.tasks_per_generation == plan.workers * plan.max_tasks_per_child


@pytest.mark.parametrize(
    "items,generations",
    [(0, 0), (1, 0), (2, 1), (8, 1), (9, 2), (16, 2), (17, 3)],
)
def test_a_plan_says_how_many_generations_of_children_its_work_takes(items, generations):
    """Eight items per generation here (four workers, two tasks each); few items narrow the pool."""
    plan = _plan(64 * GIB, items=items, ceiling=4, max_tasks_per_child=2)
    assert plan.generations == generations


def test_an_in_process_plan_runs_no_generations_at_all():
    plan = _plan(2 * GIB)
    assert plan.in_process is True
    assert plan.tasks_per_generation is None
    assert plan.generations == 0


def test_a_pool_that_never_retires_a_child_is_one_generation():
    plan = _plan(64 * GIB, items=10_000, ceiling=4, max_tasks_per_child=None)
    assert plan.tasks_per_generation is None
    assert plan.generations == 1


# The probe


@pytest.mark.parametrize(
    "answered,reported",
    [(3 * GIB, 3 * GIB), (300 * MIB, 1 * GIB)],
    ids=["above-the-floor-is-reported", "never-below-the-floor"],
)
def test_the_probe_reports_its_measure_and_never_below_the_floor(answered, reported):
    """The floor is a floor, not a fallback: a working worker allocates past its load."""
    measured = pool.measure_worker_bytes(
        lambda: None, floor_bytes=1 * GIB, runner=lambda _loader: answered
    )
    assert measured == reported


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
    """A loader that raises returns the floor rather than a traceback."""
    def broken(_loader):
        raise RuntimeError("no checkpoint on this machine")
    assert pool.measure_worker_bytes(lambda: None, floor_bytes=777, runner=broken) == 777


def test_a_probe_floor_below_one_byte_refuses():
    with pytest.raises(ValueError):
        pool.measure_worker_bytes(lambda: None, floor_bytes=0, runner=lambda _loader: 1)


def test_a_probe_with_no_time_to_answer_refuses_rather_than_reporting_the_floor():
    """A timeout of zero is a caller mistake and raises, rather than reporting the floor."""
    with pytest.raises(ValueError):
        pool.measure_worker_bytes(lambda: None, floor_bytes=1, timeout_seconds=0)


def test_a_measured_worker_size_flows_into_the_plan_it_was_taken_for():
    """Measuring and planning are one decision: the measured size is the one planned against."""
    worker_bytes = pool.measure_worker_bytes(
        lambda: None, floor_bytes=512 * MIB, runner=lambda _loader: 2 * GIB
    )
    plan = _plan(16 * GIB, worker_bytes=worker_bytes, ceiling=64)
    assert plan.worker_bytes == 2 * GIB
    assert plan.workers == affordable_for(16 * GIB, worker_bytes=2 * GIB)


# Real processes. Only where nothing else can answer the question.

#: Set by the initializer in whichever process does the work, as a loaded model would be.
_LOADED: dict[str, str] = {}


def _load(tag: str) -> None:
    """A stand-in model load: the tag, and an identity a reused pid cannot fake."""
    _LOADED["tag"] = tag
    _LOADED["identity"] = f"{os.getpid()}:{time.monotonic_ns()}"


def _report(index: int) -> tuple[int, int, str, str]:
    """Which item, which process, what it was initialized with, and which life it was."""
    tag, life = _LOADED.get("tag", "uninitialized"), _LOADED.get("identity", "uninitialized")
    return (index, os.getpid(), tag, life)


def _raise_on_the_third_item(index: int) -> int:
    """Raises on two of six items, so which exception surfaces is a real question."""
    if index in (2, 4):
        raise ValueError(f"item {index} could not be analysed")
    return index


#: Above the measured allocator cliff: freed blocks to about 112 MiB stay resident, from
#: 128 MiB they return to the kernel, so only here can a probe that frees first fail.
_PROBE_FIXTURE_BYTES = 256 * MIB


def _allocate_the_probe_fixture() -> object:
    """A stand-in for a model: memory that is genuinely resident, not just reserved."""
    return bytearray(_PROBE_FIXTURE_BYTES)


def test_the_probe_fixture_sits_above_the_allocator_retention_cliff():
    """The fixture sits above the allocator's measured retention cliff of about 112 MiB."""
    assert _PROBE_FIXTURE_BYTES >= 128 * MIB


def _nothing() -> None:
    """A loader that loads nothing, for the baseline half of the probe measurement."""
    return None


def _still_running_when_the_deadline_passes() -> object:
    """A loader still running at the deadline; eight seconds so a leak cannot hang exit."""
    time.sleep(8)
    return None


#: The exit code of a child that unwound on a terminate; no signal produces it.
_TERMINATED_CLEANLY = 77

#: The cooperative child's release before it exits; with an instant handler the budget
#: moved from 1.0 to 0.001 unnoticed. A sleep is flat under load (330 legs, five regimes)
#: but the parent's wakeup is not, so the leg is read as a minimum of ``_RELEASE_SAMPLES``.
_RELEASE_SECONDS = 0.4


def _unwinds_on_a_terminate(ready) -> None:
    """A child that exits 77 on a terminate after spending ``_RELEASE_SECONDS``."""
    def unwind(_signal, _frame) -> None:
        # Standing in for releasing a loaded model; only then is the exit code earned.
        time.sleep(_RELEASE_SECONDS)
        os._exit(_TERMINATED_CLEANLY)
    signal.signal(signal.SIGTERM, unwind)
    ready.send(True)
    ready.close()
    time.sleep(8)


def _ignores_a_terminate(ready) -> None:
    """A probe child that ignores the terminate, so only the kill can end it."""
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    ready.send(True)
    ready.close()
    time.sleep(8)


class _WatchedChild:
    """One probe child, recording each rung of the reaping ladder and its exit code."""

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
        """The wall clock of the join after the terminate; the rung order is checked first."""
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
    """Start one child of this shape, wait until its handler is installed, and reap it."""
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
            # The ladder did not finish; this test does not leave a child running either.
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
    """A plan of one runs here, asserted against the process table."""
    plan = _plan(2 * GIB, items=4)
    assert plan.in_process is True
    results = pool.map_workers(plan, _report, range(4), initializer=_load, initargs=("here",))
    assert [index for index, _pid, _tag, _life in results] == [0, 1, 2, 3]
    assert {pid for _index, pid, _tag, _life in results} == {os.getpid()}
    assert {tag for _index, _pid, tag, _life in results} == {"here"}


def test_an_in_process_plan_refuses_to_hand_back_pool_arguments():
    """The seam fails loudly rather than building the pool of one it was told not to."""
    plan = _plan(2 * GIB, items=4)
    with pytest.raises(ValueError):
        pool.executor_arguments(plan)


def test_pool_arguments_carry_a_spawn_context_and_never_the_platform_recycle_counter():
    """Pool arguments carry spawn and never ``max_tasks_per_child``, which deadlocks."""
    plan = _plan(16 * GIB, ceiling=4)
    arguments = pool.executor_arguments(plan, initializer=_load, initargs=("x",))
    assert arguments["max_workers"] == 4
    # Not the pin on spawn (darwin defaults to it); the source walk test below pins it.
    assert arguments["mp_context"].get_start_method() == "spawn"
    assert arguments["initargs"] == ("x",)
    assert "max_tasks_per_child" not in arguments, (
        "the platform recycle counter, which deadlocks, is back in the arguments"
    )


@pytest.mark.parametrize("max_tasks_per_child", [1, 2, 100, None])
def test_no_plan_at_any_recycle_setting_hands_the_counter_to_an_executor(max_tasks_per_child):
    """Swept across counters: the deadlock needs two or more, so one alone cannot show it."""
    plan = _plan(64 * GIB, items=10_000, ceiling=4, max_tasks_per_child=max_tasks_per_child)
    assert "max_tasks_per_child" not in pool.executor_arguments(plan)


def test_the_executor_constructor_is_never_written_with_a_recycle_counter():
    """The source half: no executor in the module is written with a recycle counter."""
    for node in ast.walk(ast.parse(POOL_SOURCE)):
        if not isinstance(node, ast.Call):
            continue
        if getattr(node.func, "id", "") != "ProcessPoolExecutor":
            continue
        written = {keyword.arg for keyword in node.keywords}
        assert "max_tasks_per_child" not in written, (
            f"line {node.lineno} builds an executor with the deadlocking recycle counter"
        )


def test_every_context_this_module_builds_is_written_as_spawn_in_the_source():
    """Every context names spawn in the source; linux's default would fork."""
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
        f"found {len(written)} start-method contexts; the walk stopped seeing them"
    )
    for lineno, arguments in written:
        assert arguments == ["'spawn'"], (
            f"line {lineno} builds a context without naming spawn; linux would fork"
        )


def test_recycling_is_on_by_default_for_any_pool_wider_than_one():
    """The recycle budget is the literal hundred for any pool wider than one."""
    plan = _plan(16 * GIB, ceiling=4)
    assert plan.max_tasks_per_child == 100


def test_no_child_survives_a_generation_boundary_and_every_one_reloads_its_model():
    """No worker crosses a generation boundary, and every one is initialized."""
    plan = _plan(16 * GIB, items=4, ceiling=2, max_tasks_per_child=1)
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
        f"a worker served both sides of a generation boundary: {first & second}"
    )
    assert {tag for _index, _pid, tag, _life in results} == {"reloaded"}


# the deadlock, run where a hang cannot take the suite with it
# The executor's own counter blocks forever, so a watchdog firing IS the failure.

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

#: Generous by two orders of magnitude: the healthy worst case takes a tenth of a second.
_WATCHDOG_SECONDS = 90


def _run_watched(tmp_path: Path, name: str, source: str, *arguments: object):
    """Run ``source`` as a script in a child, under the watchdog."""
    script = tmp_path / name
    script.write_text(source)
    return subprocess.run(
        [sys.executable, str(script), *map(str, arguments)],
        capture_output=True,
        text=True,
        timeout=_WATCHDOG_SECONDS,
        cwd=tmp_path,
    )


@pytest.mark.parametrize(
    "workers,tasks,items",
    [(2, 100, 201), (2, 2, 5), (3, 2, 7), (2, 100, 1001)],
    ids=["the-shipped-default", "smallest-that-can-hang", "three-wide", "five-generations"],
)
def test_work_above_the_recycle_threshold_finishes(tmp_path, workers, tasks, items):
    """A run above ``workers * counter`` finishes, at a counter of at least two."""
    finished = _run_watched(
        tmp_path, "run_above_the_threshold.py", _REPRODUCTION, workers, tasks, items
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
    """A child killed mid generation ends the run with an exception, not a hang."""
    finished = _run_watched(tmp_path, "a_child_that_dies.py", _A_CHILD_THAT_DIES)
    assert finished.returncode == 0, f"the reproduction itself failed: {finished.stderr.strip()}"
    raised = finished.stdout.strip()
    assert raised and raised != "returned", (
        f"a run whose child was killed came back with {raised!r}, not an exception"
    )


# the contract that used to depend on how much memory the machine had


def _one_plan_in_process_and_one_not() -> tuple[pool.PoolPlan, pool.PoolPlan]:
    """A tight plan that runs here and a roomy one that pickles to children."""
    tight = _plan(2 * GIB, items=4)
    roomy = _plan(64 * GIB, items=4, ceiling=2)
    assert tight.in_process is True
    assert roomy.in_process is False
    return tight, roomy


def test_a_function_no_child_could_receive_is_refused_before_anything_runs():
    """An unpicklable function is refused on a plan of one and of two alike."""
    for plan in _one_plan_in_process_and_one_not():
        with pytest.raises(ValueError) as refusal:
            pool.map_workers(plan, lambda item: item * 2, range(4))
        assert "map_workers" in str(refusal.value)


def test_an_initializer_no_child_could_receive_is_refused_on_the_same_terms():
    plan = _plan(2 * GIB, items=4)
    def loads_here(tag):
        _LOADED["tag"] = tag
    with pytest.raises(ValueError) as refusal:
        pool.map_workers(plan, _report, range(4), initializer=loads_here, initargs=("x",))
    assert "initializer" in str(refusal.value)


def test_an_initializer_argument_no_child_could_receive_is_refused_on_the_same_terms():
    """An unpicklable initializer argument is refused on a plan of one and of two alike."""
    for plan in _one_plan_in_process_and_one_not():
        with pytest.raises(ValueError) as refusal:
            pool.map_workers(
                plan, _report, range(4), initializer=_load, initargs=(lambda: None,)
            )
        assert "initializer argument 0" in str(refusal.value)


def test_one_raising_item_discards_every_completed_result():
    """One raising item discards every result, and the first in item order surfaces (U25)."""
    plan = _plan(64 * GIB, items=6, ceiling=2)
    assert plan.in_process is False
    with pytest.raises(ValueError) as failure:
        pool.map_workers(plan, _raise_on_the_third_item, range(6))
    assert "item 2" in str(failure.value), "the exception surfaced was not the first in item order"


def test_no_work_at_all_starts_no_child(tmp_path):
    """An empty list must not cost a spawn, and must not cost a hang either."""
    plan = _plan(64 * GIB, ceiling=2)
    assert plan.in_process is False
    assert pool.map_workers(plan, _report, []) == []


def test_the_real_probe_measures_a_freshly_spawned_child():
    """The real probe sees a loader's allocation against an empty loader."""
    empty = pool.measure_worker_bytes(_nothing, floor_bytes=1)
    loaded = pool.measure_worker_bytes(_allocate_the_probe_fixture, floor_bytes=1)
    assert empty > 0
    assert loaded - empty >= _PROBE_FIXTURE_BYTES * 3 // 4, (
        f"loaded {loaded} against empty {empty}; the probe reads after the free"
    )


@pytest.mark.parametrize(
    "loader,timeout,limit,why",
    [
        (_still_running_when_the_deadline_passes, 1.0, 60, "to give up on a hung loader"),
        (_dies_without_answering, 30.0, 15, "for a dead child; the write end is still open"),
    ],
    ids=["a-loader-that-never-returns", "a-child-that-dies-without-answering"],
)
def test_a_probe_that_gets_no_answer_lands_on_the_floor_in_time(loader, timeout, limit, why):
    """A hung loader lands on the floor like every other failure; a dead child at end of file."""
    started = time.monotonic()
    measured = pool.measure_worker_bytes(loader, floor_bytes=4242, timeout_seconds=timeout)
    elapsed = time.monotonic() - started
    assert measured == 4242
    assert elapsed < limit, f"the probe waited {elapsed:.1f}s {why}"


def test_a_probe_that_gave_up_leaves_no_child_still_allocating():
    """A probe that gave up leaves no child running, asserted against the process table."""
    before = set(multiprocessing.active_children())
    started = time.monotonic()
    measured = pool.measure_worker_bytes(
        _still_running_when_the_deadline_passes, floor_bytes=4242, timeout_seconds=2.0
    )
    elapsed = time.monotonic() - started
    assert measured == 4242
    assert elapsed < 8, "the probe waited out a loader it had already abandoned"
    left = [child for child in multiprocessing.active_children() if child not in before]
    assert not left, f"a probe child outlived its probe, still allocating: {left}"


# the ladder itself, one rung at a time
# The ORDER (terminate, then kill as backstop) and the BUDGET both bear load. The reaps
# calibrate ``_RELEASE_SECONDS`` with a wide tolerance; the band then judges the budget in
# exact arithmetic, since a same-run timed verdict flipped (0.81 failed 19 of 25 runs).


#: Reaps per measurement: one leg ran 0.4007 to 0.4926 s over 330 legs; the minimum of five
#: sat in [0.4010, 0.4090] idle and loaded, at about 1.5 s per reap.
_RELEASE_SAMPLES = 5


@pytest.fixture(scope="module")
def cooperative_reaps() -> list[_WatchedChild]:
    """``_RELEASE_SAMPLES`` reaps of the child that unwinds, shared by two tests."""
    return [_reap_a_child(_unwinds_on_a_terminate) for _ in range(_RELEASE_SAMPLES)]


def test_a_probe_child_that_can_unwind_is_asked_to_before_it_is_killed(cooperative_reaps):
    """Every reap terminates first and waits out the release: exit 77, not SIGKILL."""
    for index, watched in enumerate(cooperative_reaps):
        assert watched.exitcode == _TERMINATED_CLEANLY, (
            f"reap {index} exited {watched.exitcode}, not 77: a SIGKILL, so the kill ran first "
            f"or the terminate was not given the {_RELEASE_SECONDS}s release"
        )
        assert watched.rungs == ["join", "terminate", "join", "close"]


#: Floor in declared releases: no leg beats its own sleep; 41 ms under the minimum of five.
_RELEASE_FLOOR_IN_DECLARED = 0.9

#: Ceiling: the minimum of five sat 91 ms under it, and none of the 330 legs reached it.
_RELEASE_CEILING_IN_DECLARED = 1.25


def test_the_release_the_fixture_declares_is_what_the_ladder_was_timed_paying(
    cooperative_reaps,
):
    """The minimum timed release leg agrees with ``_RELEASE_SECONDS``."""
    measured = min(watched.release_seconds for watched in cooperative_reaps)
    assert measured >= _RELEASE_FLOOR_IN_DECLARED * _RELEASE_SECONDS, (
        f"cheapest leg {measured:.4f}s is under the declared {_RELEASE_SECONDS}s"
    )
    assert measured <= _RELEASE_CEILING_IN_DECLARED * _RELEASE_SECONDS, (
        f"cheapest leg {measured:.4f}s is well over the declared {_RELEASE_SECONDS}s"
    )


#: The least the budget may be, in releases: at one it races the release.
_BUDGET_FLOOR_IN_RELEASES = 2.0

#: The most, in releases: past this the first rung is a stall before a certain kill.
_BUDGET_CEILING_IN_RELEASES = 3.0


def test_the_reaping_budget_is_a_band_around_what_a_release_costs():
    """The reaping budget is two to three declared releases, with no clock in it."""
    assert pool._PROBE_REAP_SECONDS >= _BUDGET_FLOOR_IN_RELEASES * _RELEASE_SECONDS, (
        f"budget {pool._PROBE_REAP_SECONDS}s is under two releases: the terminate races"
    )
    assert pool._PROBE_REAP_SECONDS <= _BUDGET_CEILING_IN_RELEASES * _RELEASE_SECONDS, (
        f"budget {pool._PROBE_REAP_SECONDS}s is over three releases: a stall before a kill"
    )


def test_a_probe_child_that_refuses_to_unwind_meets_the_kill_backstop():
    """A child that ignores its terminate meets the kill backstop."""
    watched = _reap_a_child(_ignores_a_terminate)
    assert watched.closed, (
        "the reaping gave up on a child that ignored its terminate; it is still running"
    )
    assert watched.exitcode == -signal.SIGKILL
    assert watched.rungs == ["join", "terminate", "join", "kill", "join", "close"]


def test_a_real_loader_that_raises_lands_on_the_floor_without_printing_anything(capfd):
    """A raising loader lands on the floor without a traceback from the child's stderr."""
    measured = pool.measure_worker_bytes(_raises_in_the_worker, floor_bytes=4242)
    printed = capfd.readouterr()
    assert measured == 4242
    assert "Traceback" not in printed.err, (
        f"a probe failure printed out of its worker: {printed.err}"
    )


# A container, where the machine's reading is not this process's reading
# psutil reads the host's counters, so a capped process is told the host's number.


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
    """A ``/proc/self/cgroup`` this process could have been given."""
    path = tmp_path / "self-cgroup"
    path.write_text(text)
    return path


def _host_reads(monkeypatch, available: int, **more) -> None:
    """Make psutil report this host reading."""
    import psutil
    monkeypatch.setattr(
        psutil, "virtual_memory", lambda: SimpleNamespace(available=available, **more)
    )


@pytest.mark.parametrize(
    "layout,written,headroom",
    [
        (_version_two, dict(limit=str(512 * MIB), current=str(64 * MIB)), 448 * MIB),
        (_version_one, dict(limit=str(2 * GIB), usage=str(512 * MIB)), 1536 * MIB),
        (_version_two, dict(limit=str(512 * MIB), current=None), 512 * MIB),
        (_version_two, dict(limit=str(512 * MIB), current=str(600 * MIB)), 0),
    ],
    ids=["a-cap-reports-what-is-left", "the-older-layout", "unreadable-usage-is-still-a-cap",
         "over-the-cap-is-zero-never-negative"],
)
def test_a_cgroup_cap_reports_what_is_left_inside_it(tmp_path, layout, written, headroom):
    """A cap reads what is left in it in either layout, never negative, unreadable usage or not."""
    layout(tmp_path, **written)
    assert pool.cgroup_memory_headroom_bytes(tmp_path) == headroom


@pytest.mark.parametrize(
    "contents",
    ["max", "", "not a number", "-1", str(1 << 62), "9223372036854771712"],
    ids=["v2-unlimited", "empty", "text", "negative", "at-the-sentinel", "v1-unlimited"],
)
def test_a_cgroup_that_declares_no_limit_reports_none(tmp_path, contents):
    """Every way of declaring no cap reports None; version one has written two sentinels."""
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
    """A large but real cap is never read as the no-limit sentinel."""
    _version_two(tmp_path, limit=str(limit), current="0")
    assert pool.cgroup_memory_headroom_bytes(tmp_path) == limit


def test_a_large_container_on_a_larger_host_is_still_sized_by_the_container(
    tmp_path, monkeypatch
):
    """A 32 GiB cap on a 512 GiB host reads the container's number."""
    _version_two(tmp_path, limit=str(32 * GIB), current=str(2 * GIB))
    _host_reads(monkeypatch, available=512 * GIB)
    assert pool.available_bytes(cgroup_root=tmp_path) == 30 * GIB


def test_a_cgroup_file_this_process_may_not_read_is_no_cap_rather_than_a_crash(
    tmp_path, monkeypatch
):
    """A cgroup file refused with PermissionError is no cap; refused at the call for root."""
    _version_two(tmp_path, limit=str(512 * MIB), current="0")
    refused = tmp_path / "memory.max"
    readable = Path.read_text

    def refuse(self, *arguments, **keywords):
        if self == refused:
            raise PermissionError(13, "Permission denied", str(self))
        return readable(self, *arguments, **keywords)

    monkeypatch.setattr(Path, "read_text", refuse)
    assert pool.cgroup_memory_headroom_bytes(tmp_path) is None
    _host_reads(monkeypatch, available=7 * GIB)
    assert pool.available_bytes(cgroup_root=tmp_path) == 7 * GIB


def test_a_cgroup_path_that_is_a_directory_is_no_cap_rather_than_a_crash(
    tmp_path, monkeypatch
):
    """A cgroup file that is a directory is no cap, not a crash."""
    (tmp_path / "memory.max").mkdir()
    assert pool.cgroup_memory_headroom_bytes(tmp_path) is None
    _host_reads(monkeypatch, available=7 * GIB)
    assert pool.available_bytes(cgroup_root=tmp_path) == 7 * GIB


# which cgroup is THIS process in
# A namespaced container sits at "/"; a systemd unit's cap is at its own slice path.


def test_a_cap_on_a_nested_cgroup_is_read_rather_than_the_empty_root(tmp_path):
    """The systemd shape, which reading the root alone cannot see at all."""
    root = _hierarchy(tmp_path)
    unit = root / "system.slice" / "cratekit.service"
    unit.mkdir(parents=True)
    _version_two(unit, limit=str(4 * GIB), current=str(1 * GIB))
    where = _self_cgroup(tmp_path, "0::/system.slice/cratekit.service\n")
    assert pool.cgroup_memory_headroom_bytes(root, self_cgroup=where) == 3 * GIB


def test_the_tightest_cap_on_the_chain_is_the_one_that_binds(tmp_path):
    """A cgroup nested inside another is held by both, and the tightest cap binds."""
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
    """Version one is walked from this process's path, with a comma separated controller field."""
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
    """A controller name that merely contains ``memory`` is not the memory controller."""
    root = _hierarchy(tmp_path)
    stranger = root / "memory" / "sneaky"
    stranger.mkdir(parents=True)
    (stranger / "memory.limit_in_bytes").write_text(str(64 * MIB))
    (stranger / "memory.usage_in_bytes").write_text("0")
    where = _self_cgroup(tmp_path, line)
    assert pool.cgroup_memory_headroom_bytes(root, self_cgroup=where) is None, (
        "a controller name merely containing memory was read as the memory controller"
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
    """A cgroup path with ``..`` is not followed out of the mount."""
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
    """A path with ``..`` is refused even when it lands on a real cgroup inside the mount."""
    root = _hierarchy(tmp_path)
    sibling = root / "sibling"
    sibling.mkdir()
    _version_two(sibling, limit=str(64 * MIB), current="0")
    where = _self_cgroup(tmp_path, line)
    assert pool.cgroup_memory_headroom_bytes(root, self_cgroup=where) is None, (
        "a cgroup this process is not in was read as its own"
    )


def test_a_climb_still_leaves_the_mounts_own_cap_readable(tmp_path):
    """Refusing a climbing path still reads the mount's own cap, an ancestor's cap that binds."""
    root = _hierarchy(tmp_path)
    _version_two(root, limit=str(512 * MIB), current=str(64 * MIB))
    sibling = root / "sibling"
    sibling.mkdir()
    _version_two(sibling, limit=str(64 * MIB), current="0")
    where = _self_cgroup(tmp_path, "0::/../sibling\n")
    assert pool.cgroup_memory_headroom_bytes(root, self_cgroup=where) == 448 * MIB


# the walk really staying inside the mount, rather than spelling it
# ``Path.read_text`` follows symlinks, so a level must land inside the mount; the
# residual finding titled "The cgroup mount point
# is read at an assumed location" records the mount point as assumed.


def test_a_component_that_symlinks_out_of_the_mount_is_not_read(tmp_path):
    """A path component that symlinks out of the mount is not read as a level."""
    root = _hierarchy(tmp_path)
    _version_two(root, limit="max", current="0")
    outside = tmp_path / "outside"
    outside.mkdir()
    _version_two(outside, limit=str(4 * MIB), current="0")
    (root / "sneaky").symlink_to(outside, target_is_directory=True)
    where = _self_cgroup(tmp_path, "0::/sneaky\n")
    assert pool.cgroup_memory_headroom_bytes(root, self_cgroup=where) is None, (
        "a cap outside the mount was read through a path that never spells a climb"
    )


def test_a_limit_file_that_symlinks_out_of_the_mount_is_not_read(tmp_path):
    """A limit file that symlinks out of the mount is not read either."""
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
    """A symlink that lands inside the mount is still read; containment is not a link ban."""
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
    """An unparsable cgroup line is skipped, not raised into MEMORY_UNREADABLE."""
    root = _hierarchy(tmp_path)
    unit = root / "system.slice" / "cratekit.service"
    unit.mkdir(parents=True)
    _version_two(unit, limit=str(4 * GIB), current="0")
    where = _self_cgroup(tmp_path, text)
    _host_reads(monkeypatch, available=512 * GIB)

    assert pool.available_bytes(cgroup_root=root, cgroup_self=where) == 4 * GIB
    plan = pool.plan_pool(
        worker_bytes=256 * MIB,
        items=500,
        ceiling=64,
        read_available=lambda: pool.available_bytes(cgroup_root=root, cgroup_self=where),
    )
    assert plan.bound is pool.Bound.AVAILABLE_MEMORY, (
        f"one unparsable line turned a readable 4 GiB cap into {plan.bound}"
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
    """Undecodable bytes or a null byte in a kernel file are an absent reading, not a raise."""
    root = _hierarchy(tmp_path)
    where = tmp_path / "self-cgroup-bytes"
    where.write_bytes(contents)
    _host_reads(monkeypatch, available=8 * GIB)

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
    """A 4 GiB service on a 512 GiB host is sized by the service, end to end."""
    root = _hierarchy(tmp_path)
    unit = root / "system.slice" / "cratekit.service"
    unit.mkdir(parents=True)
    _version_two(unit, limit=str(4 * GIB), current="0")
    where = _self_cgroup(tmp_path, "0::/system.slice/cratekit.service\n")
    _host_reads(monkeypatch, available=512 * GIB)

    assert pool.available_bytes(cgroup_root=root, cgroup_self=where) == 4 * GIB
    inside = pool.plan_pool(
        worker_bytes=WORKER,
        items=500,
        ceiling=64,
        read_available=lambda: pool.available_bytes(cgroup_root=root, cgroup_self=where),
    )
    host = _plan(512 * GIB, ceiling=64)
    assert host.workers == 64, "the fixture no longer distinguishes the two readings"
    assert inside.workers == 1
    assert inside.in_process is True


def test_the_two_kernel_paths_the_reader_defaults_to_are_the_ones_the_kernel_uses():
    """The reader's two default paths are the kernel's documented locations."""
    assert pool.CGROUP_ROOT == Path("/sys/fs/cgroup")
    assert pool.CGROUP_SELF == Path("/proc/self/cgroup")


def test_a_container_capped_below_its_host_is_sized_by_the_cap(tmp_path, monkeypatch):
    """A container capped below its host is sized by the cap, end to end."""
    _version_two(tmp_path, limit=str(512 * MIB), current=str(64 * MIB))
    _host_reads(monkeypatch, available=64 * GIB, percent=10.0)
    host_only = _plan(64 * GIB, ceiling=64)
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
    """An uncapped machine reads exactly what the platform reports (P7)."""
    _host_reads(monkeypatch, available=7 * GIB)
    assert pool.available_bytes(cgroup_root=tmp_path / "nothing here") == 7 * GIB
    _version_two(tmp_path, limit="max")
    assert pool.available_bytes(cgroup_root=tmp_path) == 7 * GIB


def test_a_host_tighter_than_the_container_cap_still_wins(tmp_path, monkeypatch):
    """The minimum is taken both ways: a host tighter than the cap wins."""
    _version_two(tmp_path, limit=str(32 * GIB), current="0")
    _host_reads(monkeypatch, available=1 * GIB)
    assert pool.available_bytes(cgroup_root=tmp_path) == 1 * GIB


def test_the_real_available_reading_is_a_believable_byte_count():
    """The real available reading is a positive byte count on a machine without cgroups."""
    taken = pool.available_bytes()
    assert isinstance(taken, int) and taken > 0


# Structural guards, armed today


def _attributes_read(source: str) -> set[str]:
    """Every attribute name this source reads, from the tree rather than the text."""
    return {
        node.attr for node in ast.walk(ast.parse(source)) if isinstance(node, ast.Attribute)
    }


def _names_used(source: str) -> set[str]:
    """Every bare name and attribute name in this source, prose excluded."""
    used: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Attribute):
            used.add(node.attr)
        elif isinstance(node, ast.Name):
            used.add(node.id)
        elif isinstance(node, ast.alias):
            used.add(node.asname or node.name.split(".")[-1])
    return used


def test_the_memory_reading_is_available_and_never_free():
    """The module reads ``available`` memory, never ``free`` or ``total``, walked not grepped."""
    read = _attributes_read(POOL_SOURCE)
    assert "available" in read, "the sizing module no longer reads available memory"
    assert "free" not in read, "the sizing module reads FREE memory, which is a different number"
    assert "total" not in read, (
        "the sizing module reads TOTAL memory, the largest wrong answer available"
    )


@pytest.mark.parametrize("spelling", CORE_COUNT_SPELLINGS)
def test_the_sizing_module_never_reads_a_core_count(spelling):
    """The sizing module reads no core count, in any of the four spellings."""
    assert spelling not in _names_used(POOL_SOURCE)


# no module builds its own process pool
# Thread pools stay legal (P7); getattr, third party pools, fork and subprocess are out.

_POOL_CONSTRUCTORS = frozenset({"ProcessPoolExecutor", "Pool"})
_POOL_MODULES = frozenset(
    {"concurrent.futures", "concurrent.futures.process", "multiprocessing",
     "multiprocessing.context", "multiprocessing.pool"}
)
#: Classes whose instances hand out processes, as in ``SpawnContext().Pool(...)``.
_CONTEXT_CLASSES = frozenset(
    {"BaseContext", "DefaultContext", "SpawnContext", "ForkContext", "ForkServerContext"}
)
#: Parameter names marking a context; weak, so multiprocessing importers judge any receiver.
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
    """Every ``name = value``: assignment, annotated assignment and walrus."""
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


def _could_name(source: str, word: str) -> bool:
    """Whether ``word`` can occur in an identifier of ``source`` (NFKC); never wrong when False."""
    return word in source or (
        not source.isascii() and word in unicodedata.normalize("NFKC", source)
    )


def process_pool_constructions(source: str) -> list[str]:
    """Every process pool this source builds, bound through its imports in every shape."""
    # Every finding is a call rooted in a ``Pool`` or ``ProcessPoolExecutor`` name.
    if not _could_name(source, "Pool"):
        return []
    tree = ast.parse(source)
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

    # Settles: a helper may follow its caller, and subclasses nest.
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
    # A context used for things that are not pools, as the write session's test does.
    "import multiprocessing as mp\n"
    "def two_processes(target):\n"
    "    ctx = mp.get_context('spawn')\n"
    "    ready = ctx.Event()\n"
    "    return ctx.Process(target=target, args=(ready,))\n",
    # A thread pool built through a subclass, which is still a thread pool.
    "from concurrent.futures import ThreadPoolExecutor\n"
    "class Bounded(ThreadPoolExecutor):\n    pass\n"
    "def run():\n    return Bounded(max_workers=4)\n",
    # Somebody else's connection pool, from an argument not named as a context.
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
    """Every import shape bites, including two ordinary idioms the sizing module itself uses."""
    assert process_pool_constructions(source) != []


#: Every tree of this product's own Python, so the walk is as wide as its claim.
WALK_ROOTS = (PACKAGE_ROOT, REPO_ROOT / "scripts", REPO_ROOT / "tests")


def repository_modules(roots=WALK_ROOTS) -> list[Path]:
    """Every module under the walked trees, minus the vendored one and the sizing one."""
    return [
        path
        for root in roots
        for path in sorted(root.rglob("*.py"))
        if "_vendor" not in path.parts and path != POOL_PATH
    ]


def package_for(
    path: Path, *, source_root: Path = SRC_ROOT, repo_root: Path = REPO_ROOT
) -> str | None:
    """The dotted package a walked file sits in, measured from ``src`` or the repo root."""
    return package_of(path, source_root if source_root in path.parents else repo_root)


def plans_built_outside_the_sizing_module(
    paths: list[Path], *, source_root: Path = SRC_ROOT, repo_root: Path = REPO_ROOT
) -> dict[str, list[str]]:
    """Every walked file that builds a :class:`PoolPlan`, keyed by where it sits."""
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
    """No module in src, scripts or tests builds a process pool outside the sizing module."""
    offenders: dict[str, list[str]] = {}
    for path in repository_modules():
        found = process_pool_constructions(path.read_text())
        if found:
            offenders[str(path.relative_to(REPO_ROOT))] = found
    assert not offenders, f"process pools built outside the sizing module: {offenders} (R23)"


def test_the_sizing_module_would_fail_its_own_guard():
    """The guard still detects the one module that legitimately builds a pool."""
    assert process_pool_constructions(POOL_SOURCE) != []


# no module fabricates a plan


def pool_plan_constructions(source: str, *, package: str | None = None) -> list[str]:
    """Every :class:`PoolPlan` this source builds itself, bound through its imports."""
    # Every finding resolves a call through an identifier spelled ``PoolPlan``.
    if not _could_name(source, "PoolPlan"):
        return []
    tree = ast.parse(source)
    doors = _doors(tree, package)
    return sorted(
        f"line {node.lineno}: {ast.unparse(node.func)}"
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and _through(doors, node.func, "PoolPlan")
    )


def _doors(tree: ast.AST, package: str | None) -> list[ImportsOf]:
    """How this source reaches the planner, one reading per door it reaches it through."""
    reached = [ImportsOf(tree, door, package) for door in POOL_DOORS]
    return [imports for imports in reached if imports.reaches]


def _through(doors: list[ImportsOf], node: ast.AST, name: str) -> bool:
    """Whether ``node`` is the planner's ``name``, reached through any door."""
    return any(imports.resolves(node, name) for imports in doors)


PLAN_PROVENANCE_CORRECT = (
    # The shape every caller wants: measured, planned, run.
    "from cratekit.core import pool\n"
    "def run(items, cost):\n"
    "    plan = pool.plan_pool(worker_bytes=cost, items=len(items))\n"
    "    return pool.map_workers(plan, analyse, items)\n"
    "def analyse(item):\n    return item\n",
    # A plan from a caller, safe because no shipped module may build one.
    "from cratekit.core import pool\n"
    "def run(plan, items):\n    return pool.map_workers(plan, analyse, items)\n"
    "def analyse(item):\n    return item\n",
    # Naming the type without building one.
    "from cratekit.core.pool import PoolPlan\n"
    "def describe(plan: PoolPlan) -> str:\n    return plan.explain()\n",
    # Somebody else's class of the same name, which is not this one.
    "from elsewhere import PoolPlan\n"
    "def run():\n    return PoolPlan(workers=9)\n",
    # A sibling inside cratekit/core, in the relative shape such a module writes.
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

def _typed_plan(imports: str, constructor: str, run: str = "run(items)") -> str:
    """A source that imports as given and returns a plan of nine typed by hand."""
    return (
        f"{imports}\ndef {run}:\n    return {constructor}(workers=9, items=1, bound=None, "
        "worker_bytes=1, available_bytes=None, max_tasks_per_child=None)\n"
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
    # The same with the count taken from the cores.
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
    _typed_plan("import cratekit.core.pool as sizing", "sizing.PoolPlan"),
    # Five shapes through an ancestor package, each once silent.
    _typed_plan("import cratekit.core", "cratekit.core.pool.PoolPlan"),
    _typed_plan("from cratekit import core", "core.pool.PoolPlan"),
    _typed_plan("import cratekit", "cratekit.core.pool.PoolPlan"),
    # The two a sibling inside cratekit/core writes.
    _typed_plan("from . import pool", "pool.PoolPlan"),
    _typed_plan("from .pool import PoolPlan", "PoolPlan"),
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


# the relative half, which was the guard's one false direction
# Relative shapes once matched by dotted tail; the file's package makes them exact.

#: A package that has nothing to do with this one, which is the entire point.
UNRELATED_PACKAGE = "somewhere.else"

#: Each shape with the package it reaches the sizing module from, or None for ``..``.
RELATIVE_SHAPES = (
    (_typed_plan("from .pool import PoolPlan", "PoolPlan", "run()"), "cratekit.core"),
    (_typed_plan("from . import pool", "pool.PoolPlan", "run()"), "cratekit.core"),
    (_typed_plan("from . import core", "core.pool.PoolPlan", "run()"), "cratekit"),
    (_typed_plan("from .core.pool import PoolPlan", "PoolPlan", "run()"), "cratekit"),
    (_typed_plan("from .. import cratekit", "cratekit.core.pool.PoolPlan", "run()"), None),
)

REACHING_RELATIVE_SHAPES = tuple(pair for pair in RELATIVE_SHAPES if pair[1] is not None)


@pytest.mark.parametrize(
    "source,_reaches_from", RELATIVE_SHAPES, ids=range(len(RELATIVE_SHAPES))
)
def test_a_relative_import_in_an_unrelated_package_is_not_this_module(source, _reaches_from):
    """The relative shapes are silent from an unrelated package (P7)."""
    assert pool_plan_constructions(source, package=UNRELATED_PACKAGE) == []


@pytest.mark.parametrize(
    "source,reaches_from",
    REACHING_RELATIVE_SHAPES,
    ids=range(len(REACHING_RELATIVE_SHAPES)),
)
def test_the_same_relative_shapes_still_bite_from_the_package_that_owns_them(
    source, reaches_from
):
    """The same relative shapes bite from the package where they name the sizing module."""
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


#: Where a fabricated plan is a defect; tests may build plans by hand to drive the seam.
PRODUCTION_ROOTS = (PACKAGE_ROOT, REPO_ROOT / "scripts")


def test_no_shipped_module_outside_the_sizing_module_builds_its_own_plan():
    """No shipped module outside the sizing module builds its own plan."""
    offenders = plans_built_outside_the_sizing_module(repository_modules(PRODUCTION_ROOTS))
    assert not offenders, f"plans built outside the sizing module: {offenders} (R23)"


def test_the_walk_credits_a_relative_import_only_to_the_package_that_owns_it(tmp_path):
    """One relative import line in two packages: only the owning package is reported (P7)."""
    source = tmp_path / "src"
    inside = source / "cratekit" / "core" / "sibling.py"
    outside = source / "unrelated" / "thing.py"
    for path in (inside, outside):
        path.parent.mkdir(parents=True)
        path.write_text(_typed_plan("from .pool import PoolPlan", "PoolPlan", "run()"))
    offenders = plans_built_outside_the_sizing_module(
        [inside, outside], source_root=source, repo_root=tmp_path
    )
    assert sorted(offenders) == ["src/cratekit/core/sibling.py"]


# The countdown against the unit that owes the first real pools


#: Every seam that runs work on a plan; U241 added the stream beside ``map_workers``.
PLAN_RUNNERS = ("map_workers", "stream_workers", "WorkStream")


def unplanned_map_workers(source: str, *, package: str | None = None) -> list[str]:
    """Every runner call, :data:`PLAN_RUNNERS`, on a plan this source built itself."""
    tree = ast.parse(source)
    doors = _doors(tree, package)
    if not doors:
        return []
    fabricated = {
        name
        for name, value in _bindings(tree)
        if isinstance(value, ast.Call) and _through(doors, value.func, "PoolPlan")
    }
    found: list[str] = []
    for node in ast.walk(tree):
        if not (
            isinstance(node, ast.Call)
            and any(_through(doors, node.func, runner) for runner in PLAN_RUNNERS)
        ):
            continue
        given = next(
            (keyword.value for keyword in node.keywords if keyword.arg == "plan"),
            node.args[0] if node.args else None,
        )
        if given is None:
            continue
        given = _unwrap(given)
        if isinstance(given, ast.Call) and _through(doors, given.func, "PoolPlan"):
            found.append(f"line {node.lineno}: a plan built inline")
        elif _dotted(given) in fabricated:
            found.append(f"line {node.lineno}: a plan built at {_dotted(given)}")
    return found


#: The package the countdown is about, and the package its modules are read as sitting in.
ANALYSIS_PACKAGE = "cratekit.analysis"


def analysis_sizing_violations(
    modules: list[tuple[str, str]], package: str | None = ANALYSIS_PACKAGE
) -> list[str]:
    """Every way a set of modules fails to be sized by this module and nothing else (U241)."""
    if not modules:
        return ["the analysis package landed with no modules in it"]

    problems: list[str] = []
    if not any(
        calls_attribute(source, door, "plan_pool", package=package)
        for _name, source in modules
        for door in POOL_DOORS
    ):
        problems.append(
            "no module in the analysis package calls cratekit.core.pool.plan_pool; a "
            "pool sized anywhere else is a second answer to R23"
        )
    if not any(
        calls_attribute(source, door, runner, package=package)
        for _name, source in modules
        for runner in ("map_workers", "stream_workers")
        for door in POOL_DOORS
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


def _light_and(name: str, source: str) -> list[tuple[str, str]]:
    """A package of the correctly sized light pass beside one more module."""
    return [_ANALYSIS_LIGHT, (name, source)]


ANALYSIS_CORRECT = (
    # Two passes, each sizing itself through the seam.
    _light_and(
        "vocals.py",
        "from cratekit.core import pool\n"
        "def run(items, cost):\n"
        "    plan = pool.plan_pool(worker_bytes=cost, items=len(items), ceiling=2)\n"
        "    return pool.map_workers(plan, analyse, items)\n"
        "def analyse(item):\n    return item\n",
    ),
    # One pass plans, a shared runner runs. Split across modules and still correct.
    _light_and(
        "shared.py",
        "from cratekit.core import pool\n"
        "def run(plan, items, analyse):\n"
        "    return pool.map_workers(plan, analyse, items)\n",
    ),
    # Correctly sized through an ancestor package, once falsely accused (P7).
    [("light.py",
      "from cratekit import core\n"
      "def run(items, cost):\n"
      "    plan = core.pool.plan_pool(worker_bytes=cost, items=len(items))\n"
      "    return core.pool.map_workers(plan, analyse, items)\n"
      "def analyse(item):\n    return item\n")],
    # The same relatively, as two packages so neither shape covers for the other.
    [("light.py",
      "from ..core import pool\n"
      "def run(items, cost):\n"
      "    plan = pool.plan_pool(worker_bytes=cost, items=len(items))\n"
      "    return pool.map_workers(plan, analyse, items)\n"
      "def analyse(item):\n    return item\n")],
    [("light.py",
      "from ..core.pool import map_workers, plan_pool\n"
      "def run(items, cost):\n"
      "    plan = plan_pool(worker_bytes=cost, items=len(items), ceiling=2)\n"
      "    return map_workers(plan, analyse, items)\n"
      "def analyse(item):\n    return item\n")],
    # U241's shape: a ceiling from the one core reader, the work run through the stream.
    [("ahead.py",
      "from cratekit.core import cores, pool\n"
      "def run(items, cost):\n"
      "    plan = pool.plan_pool(worker_bytes=cost, items=len(items),\n"
      "                          ceiling=cores.worker_ceiling(reserved=2))\n"
      "    with pool.stream_workers(plan, analyse, items) as stream:\n"
      "        return [stream.result(at) for at in range(len(items))]\n"
      "def analyse(item):\n    return item\n")],
    # A sibling named pool in cratekit.analysis, decided by the package argument alone.
    _light_and(
        "grouping.py",
        "from .pool import PoolPlan\n"
        "def group(tracks):\n    return PoolPlan(tracks)\n",
    ),
    # U331's shape, the tree's own: the planner and the core reader through ``core.jobs``.
    [("light.py",
      "from cratekit.core import jobs\n"
      "def run(items, cost):\n"
      "    plan = jobs.plan_pool(worker_bytes=cost, items=len(items),\n"
      "                          ceiling=jobs.worker_ceiling(reserved=2))\n"
      "    return jobs.map_workers(plan, analyse, items)\n"
      "def analyse(item):\n    return item\n")],
)

ANALYSIS_EVASIONS = (
    # The verified evasion: one module sized, another hands the seam a plan of nine.
    _light_and(
        "vocals.py",
        "from cratekit.core import pool\n"
        "def run(items):\n"
        "    plan = pool.PoolPlan(workers=9, items=len(items), bound=pool.Bound.CEILING,\n"
        "                         worker_bytes=1024 ** 3, available_bytes=None,\n"
        "                         max_tasks_per_child=100)\n"
        "    return pool.map_workers(plan, analyse, items)\n"
        "def analyse(item):\n    return item\n",
    ),
    # The same with the count taken from the cores, at a spelling once unchecked here.
    _light_and(
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
    # A private pool inside the package.
    _light_and(
        "vocals.py",
        "from concurrent.futures import ProcessPoolExecutor\n"
        "def run(items):\n"
        "    with ProcessPoolExecutor(max_workers=9) as workers:\n"
        "        return list(workers.map(analyse, items))\n"
        "def analyse(item):\n    return item\n",
    ),
    # The hand built plan again, through an ancestor package.
    _light_and(
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
    # The hand built plan again, through the stream U241 added.
    _light_and(
        "ahead.py",
        "from cratekit.core import pool\n"
        "def run(items):\n"
        "    plan = pool.PoolPlan(workers=9, items=len(items), bound=pool.Bound.CEILING,\n"
        "                         worker_bytes=1024 ** 3, available_bytes=None,\n"
        "                         max_tasks_per_child=100)\n"
        "    return pool.stream_workers(plan, analyse, items)\n"
        "def analyse(item):\n    return item\n",
    ),
    # Nothing sizes anything.
    [("light.py",
      "def run(items):\n    return [analyse(item) for item in items]\n"
      "def analyse(item):\n    return item\n")],
    # The package landed empty.
    [],
    # A plan of nine built by hand through the listed module (U331): the door the
    # tree uses must be read, or the countdown is silent on its own package.
    _light_and(
        "vocals.py",
        "from cratekit.core import jobs\n"
        "def run(items):\n"
        "    plan = jobs.PoolPlan(workers=9, items=len(items), bound=jobs.Bound.CEILING,\n"
        "                         worker_bytes=1024 ** 3, available_bytes=None,\n"
        "                         max_tasks_per_child=100)\n"
        "    return jobs.map_workers(plan, analyse, items)\n"
        "def analyse(item):\n    return item\n",
    ),
    # Sized by nothing, the listed module imported for its queue alone.
    [("light.py",
      "from cratekit.core import jobs\n"
      "def run(items):\n    return [jobs.item_path(item, item) for item in items]\n")],
)

CORRECT_IDS = [
    "two-passes", "split-planner", "ancestor-package", "relative-package-import",
    "relative-symbol-import", "the-stream-under-a-core-ceiling", "a-sibling-of-its-own-named-pool",
    "through-the-listed-module",
]
EVASION_IDS = [
    "hand-built-plan", "core-count-in-a-hand-built-plan", "private-pool",
    "hand-built-plan-through-an-ancestor", "hand-built-plan-through-the-stream", "no-sizing",
    "empty", "hand-built-plan-through-the-listed-module", "the-listed-module-and-no-sizing",
]


@pytest.mark.parametrize("modules", ANALYSIS_CORRECT, ids=CORRECT_IDS)
def test_the_analysis_countdown_stays_silent_on_correctly_sized_modules(modules):
    """The half that gets skipped, run before the half that does not (P7)."""
    assert analysis_sizing_violations(modules) == []


@pytest.mark.parametrize("modules", ANALYSIS_EVASIONS, ids=EVASION_IDS)
def test_the_analysis_countdown_bites_the_evasions_that_used_to_pass_it(modules):
    """Two of these passed the countdown as first written, and both spawn nine children."""
    assert analysis_sizing_violations(modules) != []


def test_the_analysis_pools_are_sized_here_and_never_by_the_core_count():
    """U25's obligation: the analysis package passes the countdown (R23)."""
    problems = analysis_sizing_violations(
        package_modules(PACKAGE_ROOT / "analysis")
    )
    assert not problems, "the analysis package is not sized here:\n" + "\n".join(problems)
