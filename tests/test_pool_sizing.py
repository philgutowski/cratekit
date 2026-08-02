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
initializer and that a plan of one worker starts no child at all.

THREE GUARDS HERE ARE STRUCTURAL AND ARMED TODAY, over the source rather than
over behaviour, because each names a defect that a passing suite cannot see:

* the memory reading is ``available`` and never ``free``, which are two different
  numbers and only one of them answers the question being asked;
* nothing in the sizing module reads a core count, in any spelling, so the
  defect it exists to prevent cannot come back through the module named after it;
* no module anywhere in the package builds a process pool for itself, so a later
  unit cannot acquire its own private copy of this decision.

All three walk the syntax tree rather than the text. The module documents at
length why it does not do these things, so a text search would fire on its own
explanation, and a guard that fires on correct code is a guard people route
around (P7).
"""

from __future__ import annotations

import ast
import multiprocessing
import os
import sys
from pathlib import Path

import pytest

from cratekit.core import pool
from tests._pending import requires
from tests._source_guards import calls_attribute, package_modules

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"

#: The module every question below is asked about, named once.
POOL_MODULE = "cratekit.core.pool"
POOL_SOURCE = (SRC_ROOT / "cratekit" / "core" / "pool.py").read_text()

MIB = 1024**2
GIB = 1024**3

#: A stand-in for the per-worker cost of a pass that loads a model. One gibibyte
#: is the source system's own declared budget for its vocal worker, so the
#: scenarios below are the plan's scenarios in the plan's own units.
WORKER = 1 * GIB


def reader(value: int):
    """A memory reading that always answers ``value``. Never touches the machine."""
    return lambda: value


def threshold_for(workers: int, *, worker_bytes: int = WORKER, percent: int) -> int:
    """The smallest available-byte reading that affords ``workers`` workers.

    Derived from the same two numbers the module divides, rather than copied out
    of a run of it, so this expresses the intended rule and can disagree with the
    implementation. A constant pasted from the output would agree with a defect.
    """
    return -(-workers * worker_bytes * 100 // percent)


# ---------------------------------------------------------------------------
# The plan's own scenarios
# ---------------------------------------------------------------------------


def test_two_gigabytes_against_a_one_gigabyte_worker_runs_in_process():
    """The plan's first scenario: the cap is one, and one skips the pool.

    Two gigabytes divided by a one gigabyte worker looks like two workers to
    anybody dividing without headroom, and two workers is exactly the run that
    dies: the reading is optimistic, the parent is still resident, and the second
    child pays for the model in full.
    """
    plan = pool.plan_pool(worker_bytes=WORKER, items=500, read_available=reader(2 * GIB))
    assert plan.workers == 1
    assert plan.in_process is True
    assert plan.bound is pool.Bound.AVAILABLE_MEMORY
    assert plan.max_tasks_per_child is None


def test_sixteen_gigabytes_is_bound_by_the_hard_ceiling_at_the_default():
    """The plan's second scenario, ceiling half.

    Memory affords twelve here. The ceiling is what stops it, and the ceiling is
    the brake that covers the per-worker estimate being wrong rather than the
    machine being small.
    """
    plan = pool.plan_pool(worker_bytes=WORKER, items=500, read_available=reader(16 * GIB))
    assert plan.workers == pool.DEFAULT_WORKER_CEILING
    assert plan.bound is pool.Bound.CEILING


def test_sixteen_gigabytes_is_bound_by_the_headroom_once_the_ceiling_is_raised():
    """The plan's second scenario, headroom half.

    With the ceiling out of the way the headroom is the only thing between the
    reading and the count, and it must actually bite: sixteen gigabytes affords
    twelve one gigabyte workers at seventy five percent, never sixteen.
    """
    plan = pool.plan_pool(
        worker_bytes=WORKER, items=500, ceiling=64, read_available=reader(16 * GIB)
    )
    assert plan.workers == 12
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
    assert made[0].workers == 12


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
    """
    available = 2900 * MIB
    percent = pool.DEFAULT_HEADROOM_PERCENT

    shipped = available * percent // 100 // WORKER
    reversed_order = available // WORKER * percent // 100
    assert shipped != reversed_order, "the fixture no longer distinguishes the two orders"

    plan = pool.plan_pool(
        worker_bytes=WORKER, items=500, ceiling=64, read_available=reader(available)
    )
    assert plan.workers == shipped == 2
    assert plan.workers != reversed_order


def test_the_hard_ceiling_and_the_headroom_agree_at_the_point_they_cross():
    """Where the two brakes meet, whichever is smaller wins and the tie names memory.

    A tie has to resolve one way and be documented, because a caller logging the
    reason gets one answer per run and two answers is a bug report nobody can
    reproduce. Memory wins, since it is the input that changes tomorrow.
    """
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
    assert plan.workers == 48
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
    assert plan.workers == 6


# ---------------------------------------------------------------------------
# Real processes. Only where nothing else can answer the question.
# ---------------------------------------------------------------------------

#: Set by the initializer in whichever process is doing the work. The module
#: global IS the pattern a real pool uses for a loaded model, so the recycle test
#: below exercises the shape it will actually be used in.
_LOADED: dict[str, str] = {}


def _load(tag: str) -> None:
    """A stand-in for loading a model, cheap enough to run in a test."""
    _LOADED["tag"] = tag


def _report(index: int) -> tuple[int, int, str]:
    """Which item, which process, and what that process was initialized with."""
    return index, os.getpid(), _LOADED.get("tag", "uninitialized")


def _allocate_96_mebibytes() -> object:
    """A stand-in for a model: memory that is genuinely resident, not just reserved."""
    return bytearray(96 * MIB)


def _nothing() -> None:
    """A loader that loads nothing, for the baseline half of the probe measurement."""
    return None


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
    assert [index for index, _pid, _tag in results] == [0, 1, 2, 3]
    assert {pid for _index, pid, _tag in results} == {os.getpid()}
    assert {tag for _index, _pid, tag in results} == {"here"}


def test_an_in_process_plan_refuses_to_hand_back_pool_arguments():
    """The seam fails loudly rather than building the pool of one it was told not to."""
    plan = pool.plan_pool(worker_bytes=WORKER, items=4, read_available=reader(2 * GIB))
    with pytest.raises(ValueError):
        pool.executor_arguments(plan)


def test_pool_arguments_carry_a_spawn_context_and_the_recycle_count():
    """Spawn is not a preference here. Two things depend on it.

    The sizing above assumes a child shares nothing with its parent, which is
    true under spawn and false under fork, and recycling a child after a fixed
    number of tasks is unsupported under fork outright. Reading the start method
    off the context rather than trusting the keyword is the difference between
    asserting the argument was passed and asserting what it means.
    """
    plan = pool.plan_pool(
        worker_bytes=WORKER, items=500, ceiling=4, read_available=reader(16 * GIB)
    )
    arguments = pool.executor_arguments(plan, initializer=_load, initargs=("x",))
    assert arguments["max_workers"] == 4
    assert arguments["mp_context"].get_start_method() == "spawn"
    assert arguments["max_tasks_per_child"] == pool.DEFAULT_MAX_TASKS_PER_CHILD
    assert arguments["initargs"] == ("x",)


def test_recycling_is_on_by_default_for_any_pool_wider_than_one():
    plan = pool.plan_pool(
        worker_bytes=WORKER, items=500, ceiling=4, read_available=reader(16 * GIB)
    )
    assert plan.max_tasks_per_child == pool.DEFAULT_MAX_TASKS_PER_CHILD


def test_a_child_is_replaced_at_the_configured_task_count_and_reloads_its_model():
    """Real spawned children, because recycling cannot be observed any other way.

    Three properties in one pool, and they are one property in practice: a child
    that is replaced must come back initialized, or recycling silently trades a
    bounded allocator for a worker running without its model. Four items across
    two workers recycling every task must touch more than two processes; without
    recycling it would touch exactly two.
    """
    plan = pool.plan_pool(
        worker_bytes=WORKER,
        items=4,
        ceiling=2,
        max_tasks_per_child=1,
        read_available=reader(16 * GIB),
    )
    assert plan.workers == 2
    results = pool.map_workers(
        plan, _report, range(4), initializer=_load, initargs=("reloaded",)
    )
    assert [index for index, _pid, _tag in results] == [0, 1, 2, 3]
    pids = {pid for _index, pid, _tag in results}
    assert os.getpid() not in pids, "the work ran in the calling process, not in a pool"
    assert len(pids) > plan.workers, (
        f"{len(pids)} processes served 4 tasks across {plan.workers} workers recycling "
        f"every task; without recycling that number is exactly the worker count"
    )
    assert {tag for _index, _pid, tag in results} == {"reloaded"}


def test_the_real_probe_measures_a_freshly_spawned_child():
    """The one test of the probe that actually spawns. It costs two interpreters.

    Asserted as a DIFFERENCE between two loaders rather than as an absolute
    number, because an absolute number is a property of the machine and of every
    import the child happened to make. The difference is the loader's, and it is
    the thing the probe claims to measure.
    """
    empty = pool.measure_worker_bytes(_nothing, floor_bytes=1)
    loaded = pool.measure_worker_bytes(_allocate_96_mebibytes, floor_bytes=1)
    assert empty > 0
    assert loaded - empty >= 64 * MIB, (
        f"a child that allocated 96 mebibytes measured {loaded} against an empty "
        f"child's {empty}; the probe is not reading the loaded child"
    )


# ---------------------------------------------------------------------------
# Structural guards, armed today
# ---------------------------------------------------------------------------


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


@pytest.mark.parametrize(
    "spelling", ["cpu_count", "process_cpu_count", "sched_getaffinity", "cpu_affinity"]
)
def test_the_sizing_module_never_reads_a_core_count(spelling):
    """The defect this unit exists to end cannot return through the module that ends it.

    Not one spelling: four. ``os.cpu_count`` is the one the source system uses,
    ``os.process_cpu_count`` is its modern replacement, and the two affinity calls
    are what somebody reaches for when they read that the first two ignore
    cgroup limits. All four answer a question about cores, and cores are not the
    resource that runs out.
    """
    assert spelling not in _names_used(POOL_SOURCE)


# --- no module builds its own process pool -----------------------------------
#
# THREAD POOLS ARE LEFT ALONE, DELIBERATELY. Threads share one address space, so
# a second thread does not cost a second model, and acquisition's bounded thread
# pool is paced against a provider rather than against memory. A guard that
# refused it would be refusing correct code, which is how a guard gets routed
# around (P7).

_POOL_CONSTRUCTORS = frozenset({"ProcessPoolExecutor", "Pool"})
_POOL_MODULES = frozenset({"concurrent.futures", "multiprocessing", "multiprocessing.pool"})


def process_pool_constructions(source: str) -> list[str]:
    """Every place this source builds a process pool, in each import shape it can use.

    Bound to the module the name came from, never to the bare name. ``Pool`` on
    its own is an ordinary word for an ordinary thing, and a guard that fired on
    a connection pool would be muted rather than obeyed.

    The shapes covered are the ones a real module writes::

        from concurrent.futures import ProcessPoolExecutor
        import concurrent.futures as futures            # futures.ProcessPoolExecutor
        from multiprocessing import Pool
        import multiprocessing                          # multiprocessing.Pool
        context = multiprocessing.get_context("spawn")  # context.Pool
    """
    tree = ast.parse(source)
    module_names: set[str] = set()
    symbols: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in _POOL_MODULES:
                    module_names.add(alias.asname or alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module in _POOL_MODULES:
                for alias in node.names:
                    if alias.name in _POOL_CONSTRUCTORS:
                        symbols.add(alias.asname or alias.name)
                    elif alias.name == "pool":
                        module_names.add(alias.asname or "pool")

    def dotted(node: ast.AST) -> str | None:
        parts: list[str] = []
        current: ast.AST = node
        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value
        if isinstance(current, ast.Name):
            parts.append(current.id)
            return ".".join(reversed(parts))
        return None

    def is_context(node: ast.AST) -> bool:
        return (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "get_context"
            and dotted(node.func.value) in module_names
        )

    contexts = {
        name
        for node in ast.walk(tree)
        if isinstance(node, ast.Assign) and is_context(node.value)
        for target in node.targets
        if (name := dotted(target)) is not None
    }

    found: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Name) and func.id in symbols:
            found.append(f"line {node.lineno}: {func.id}")
        elif isinstance(func, ast.Attribute) and func.attr in _POOL_CONSTRUCTORS:
            owner = dotted(func.value)
            if owner in module_names or owner in contexts or is_context(func.value):
                found.append(f"line {node.lineno}: {ast.unparse(func)}")
    return found


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
)


@pytest.mark.parametrize("source", CORRECT_SOURCES, ids=range(len(CORRECT_SOURCES)))
def test_the_pool_construction_guard_stays_silent_on_correct_code(source):
    """Half the job. The other half is the half that keeps getting skipped (P7)."""
    assert process_pool_constructions(source) == []


@pytest.mark.parametrize("source", EVASIONS, ids=range(len(EVASIONS)))
def test_the_pool_construction_guard_bites_every_import_shape(source):
    """An aliased import defeated the armed guard in an earlier unit. Not this one."""
    assert process_pool_constructions(source) != []


def test_no_module_outside_the_sizing_module_builds_a_process_pool():
    """Armed today, over the whole package, so the shape cannot arrive quietly.

    Every process pool in this product is sized by one decision. A module that
    builds its own gets its own copy of that decision, the copies drift, and the
    one that drifts is the one nobody is looking at. The vendored tree is out of
    scope: it is code this product did not write and does not restyle, and its
    pools are threads in any case.
    """
    offenders: dict[str, list[str]] = {}
    for path in sorted((SRC_ROOT / "cratekit").rglob("*.py")):
        if "_vendor" in path.parts:
            continue
        if path == SRC_ROOT / "cratekit" / "core" / "pool.py":
            continue
        found = process_pool_constructions(path.read_text())
        if found:
            offenders[str(path.relative_to(SRC_ROOT))] = found
    assert not offenders, (
        f"process pools built outside the sizing module: {offenders}. Route them "
        f"through cratekit.core.pool so one memory decision governs every pool (R23)."
    )


# ---------------------------------------------------------------------------
# The countdown against the unit that owes the first real pools
# ---------------------------------------------------------------------------


@requires("cratekit.analysis")
def test_the_analysis_pools_are_sized_here_and_never_by_the_core_count():
    """U25's obligation, registered because U12 is the unit it would silently undo.

    This unit ships the mechanism and nothing that uses it, so R23 is a claim
    about a module rather than about a run until the first heavy pass lands.
    U25 ports the two-pass split, and the source system sizes BOTH of its passes
    from the core count. A port that carries that arithmetic across satisfies
    every test in this file while reproducing the exact kill the unit exists to
    prevent, and the guard against building a private pool would not catch it:
    routing through this module while handing it a core count is a pool that is
    sized wrong through the right seam.

    So the assertion is positive and specific. The package must call the planner,
    and the call must be bound to THIS module rather than to anything that
    happens to have a function of the same name, which is the lesson from the
    countdown that a dead reference and an unrelated method call satisfied.
    """
    modules = package_modules(SRC_ROOT / "cratekit" / "analysis")
    assert modules, "the analysis package landed with no modules in it"

    plans = [name for name, source in modules if calls_attribute(source, POOL_MODULE, "plan_pool")]
    assert plans, (
        "no module in the analysis package calls cratekit.core.pool.plan_pool; a "
        "pool sized anywhere else is a second answer to R23"
    )
    runs = [name for name, source in modules if calls_attribute(source, POOL_MODULE, "map_workers")]
    assert runs, (
        "the analysis package plans a pool and never runs work through "
        "cratekit.core.pool.map_workers, so the branch that keeps a cap of one in "
        "process is the caller's own copy"
    )
    for name, source in modules:
        used = _names_used(source)
        assert "cpu_count" not in used and "process_cpu_count" not in used, (
            f"cratekit/analysis/{name} derives a worker count from the core count, "
            f"which is the nine-worker spike this unit exists to end"
        )
