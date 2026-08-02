"""How many worker processes may run at once, decided by memory rather than by cores.

R23 in one sentence: no default-configuration run exhausts memory, on any pool.

**The defect this module exists to not inherit.** The source system sizes its
worker pool as ``cpu_count() - 2``, which is nine on the machine it runs on. One
of its two passes loads a roughly 300 megabyte model per worker, so nine workers
claim nine copies of it, and the run is killed by the kernel on an 18 gigabyte
machine that is already deep in swap. The count is derived from a number that has
nothing to do with the resource that runs out. Cores are not the scarce thing.

**Why the per-worker cost is the FULL cost, and why this module pins the spawn
start method to make that true.** A forked child shares its parent's pages until
one side writes, so a model loaded before the fork costs almost nothing per
child. A spawned child imports everything again in a fresh interpreter and shares
nothing, so each worker pays for the model in full. macOS spawns by default,
Linux forks today and moves to a forkserver in a later interpreter, and a sizing
rule whose arithmetic silently depends on which of those you got is a rule that
is right on one machine. Every pool built here is spawned, deliberately, so the
arithmetic below and the behaviour on the machine agree everywhere. Recycling a
child after a fixed number of tasks needs a spawned context anyway; asking for it
under fork raises.

**Three brakes, and none of them is redundant.** Each one covers a failure of the
other two:

1. *The available-memory reading* adapts to what the machine is doing right now,
   which neither of the other two can see.
2. *The headroom percent* covers the reading being optimistic. On macOS the
   platform counts inactive file cache as available, so the number is a ceiling
   on what a new process can really get rather than a promise.
3. *The hard ceiling* covers the per-worker estimate being wrong. A probe
   measures resident set at the moment the model finishes loading, which is a
   LOWER bound on what the worker holds while it is actually working.

**Available, never free.** They are different numbers. Free is memory nobody
holds at all; available is what a new process can obtain without pushing the
machine into swap, and it includes cache the kernel would evict. A pool sized
against free memory starves on a healthy machine whose cache is warm, which is
every machine that has been doing work. ``test_pool_sizing.py`` walks this
module's syntax tree and fails if ``free`` is ever read.

**Nothing here reads the core count.** Not to bound the answer, not to floor it,
not as a tiebreak. That is asserted rather than intended: a sizing rule that
depends on cores anywhere downstream is the defect above wearing this module's
name, and the test that checks it walks the tree rather than reading this
paragraph.

**Thread pools are a different question and are deliberately out of scope.**
Threads share one address space, so a second thread does not cost a second model.
The bound on a thread pool is what the far end tolerates, which is why acquisition
paces itself against its own configured concurrency instead of coming through
here.

Layer note: INFRASTRUCTURE. It reads the machine and builds processes, and it
names no verb, no feature module, and no taxonomy.
"""

from __future__ import annotations

import multiprocessing
import sys
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import process as _process_pool
from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Callable, Iterable, Mapping, TypeVar

#: The hard ceiling on workers for a pool whose children each hold a model.
#: Ported as the number it is: two is the count survival-tested on a real run of
#: the source system, and the default is the survival-tested number rather than
#: the aspirational one. A caller with a cheaper worker raises it explicitly,
#: which is a decision in a diff rather than a default nobody chose.
DEFAULT_WORKER_CEILING = 2

#: The share of available memory a pool may claim, as an integer percent.
#:
#: An INTEGER PERCENT rather than a float factor, because the whole job of this
#: number is to be exact at a boundary and 0.8 is not representable in binary.
#: A float factor makes the boundary between two and three workers land on
#: whichever side the last bit of a rounding error fell, and the boundary is
#: precisely where a memory rule is tested and precisely where it fails.
#:
#: Seventy five, because the reading is optimistic rather than wrong: the
#: platform counts reclaimable cache as available, and the parent process, the
#: operating system, and whatever else the user has open all still need room.
DEFAULT_HEADROOM_PERCENT = 75

#: Recycle a child after this many tasks, so an allocator that grows over a long
#: run is bounded rather than merely observed. Each recycle pays for a fresh
#: interpreter and a fresh model load, so this is high enough that an ordinary
#: folder recycles once or twice per child rather than constantly.
DEFAULT_MAX_TASKS_PER_CHILD = 100

#: A reading of how much memory a new process could obtain, in bytes. Injected by
#: every test, so sizing is decided without allocating anything and no test
#: depends on what the machine happens to be doing.
AvailableReader = Callable[[], int]

#: A run of one probe worker, returning that worker's resident bytes once its
#: loader has finished. Injected the same way and for the same reason.
ProbeRunner = Callable[[Callable[[], object]], int]

_Item = TypeVar("_Item")
_Result = TypeVar("_Result")


class Bound(StrEnum):
    """Which constraint decided the worker count.

    Carried on the plan rather than recomputed by a caller that wants to log it,
    because two answers to "why is this run using one worker" is one answer too
    many. ``MEMORY_UNREADABLE`` is a first-class value for the same reason the
    job engine keeps ``cancelled`` separate from ``failed``: a machine that is
    genuinely tight and a machine this process could not measure are two
    different situations with two different fixes, and collapsing them hides the
    second one forever.
    """

    AVAILABLE_MEMORY = "available_memory"
    CEILING = "ceiling"
    WORK_ITEMS = "work_items"
    PLATFORM_LIMIT = "platform_limit"
    MEMORY_UNREADABLE = "memory_unreadable"


#: One phrase per bound, for the line a caller logs. Derived coverage is asserted
#: by iterating :class:`Bound`, and the literal is parsed for a duplicate key,
#: because a mapping that several branches append to is where this repository has
#: already shipped a collapsed entry with the whole suite green.
BOUND_PHRASES: Mapping[Bound, str] = MappingProxyType(
    {
        Bound.AVAILABLE_MEMORY: "available memory",
        Bound.CEILING: "the declared worker ceiling",
        Bound.WORK_ITEMS: "the number of work items",
        Bound.PLATFORM_LIMIT: "this platform's own limit on pool width",
        Bound.MEMORY_UNREADABLE: "a memory reading that could not be taken",
    }
)


@dataclass(frozen=True)
class PoolPlan:
    """The decided shape of one pool: how wide, why, and what it recycles at.

    ``in_process`` is a PROPERTY rather than a field, and that is load bearing. A
    stored flag can disagree with the count it was derived from, and the one
    place this arithmetic has an off-by-one is exactly there: a computed cap of
    one must run the work in the calling process, never start a pool of one. A
    pool of one is a whole second interpreter, a second copy of the model, and a
    pickle of every item and every result, to run the work strictly slower than
    doing it here. It is also the case a tight machine lands on, which is the
    machine that can least afford it.
    """

    workers: int
    bound: Bound
    worker_bytes: int
    available_bytes: int | None
    max_tasks_per_child: int | None

    @property
    def in_process(self) -> bool:
        """True when the work runs in the calling process and no pool is built."""
        return self.workers == 1

    def explain(self) -> str:
        """One line saying what the count is and what decided it."""
        where = "in process" if self.in_process else f"{self.workers} workers"
        return f"{where}, bound by {BOUND_PHRASES[self.bound]}"


def available_bytes() -> int:
    """Memory a new process could obtain right now, in bytes.

    AVAILABLE, never free. See the module docstring for why the two are not
    interchangeable and why this one is the right question.

    psutil is imported lazily so a caller that injects its own reader, which
    every sizing test does, never loads the extension module at all.
    """
    import psutil

    return int(psutil.virtual_memory().available)


def resident_bytes() -> int:
    """This process's resident set, in bytes.

    Called INSIDE a probe worker, where the interpreter, the imports and the
    loaded model are all already paid for, so the number returned is what one
    worker of this shape costs. Reading the parent's resident set instead would
    measure whatever the caller happened to be holding, which is a different
    program's memory.
    """
    import psutil

    return int(psutil.Process().memory_info().rss)


def platform_worker_ceiling() -> int | None:
    """The widest process pool this platform will build, or None where it does not care.

    Windows refuses a pool above a fixed width, and it refuses by raising out of
    the executor's constructor rather than by giving back a narrower pool. That
    makes it a sizing question rather than a runtime one: the machine most likely
    to compute a width above the limit is a large one with plenty of memory and a
    caller that raised the ceiling, which is precisely the machine where a
    refusal is least expected.

    The interpreter's own number is read where it is available, so a build that
    lowers it lowers this too. The literal is the fallback for a build that stops
    publishing it, and it is the current value rather than a guess.
    """
    if sys.platform != "win32":
        return None
    limit = getattr(_process_pool, "_MAX_WINDOWS_WORKERS", 61)
    return int(limit) if isinstance(limit, int) and limit > 0 else 61


def _probe_entry(loader: Callable[[], object]) -> int:
    """Run the caller's loader in this worker, then report what the worker costs.

    Module level and picklable because a spawned child has to import it by name.
    The loader's return value is deliberately discarded: what is being measured
    is the process, not the object.
    """
    loader()
    return resident_bytes()


def _spawned_probe(loader: Callable[[], object]) -> int:
    """Run one real spawned worker and return its resident bytes after loading."""
    with ProcessPoolExecutor(
        max_workers=1, mp_context=multiprocessing.get_context("spawn")
    ) as probe:
        return int(probe.submit(_probe_entry, loader).result())


def measure_worker_bytes(
    loader: Callable[[], object],
    *,
    floor_bytes: int,
    runner: ProbeRunner | None = None,
) -> int:
    """What one worker of this shape costs, measured, never below ``floor_bytes``.

    ``floor_bytes`` is a FLOOR and not merely a fallback, and conflating the two
    is the quiet way this returns a number that is too small. A probe measures
    resident set at the moment loading finishes. A worker then decodes a track,
    runs inference, and builds results, all of which allocate, so the measurement
    is a lower bound on the working set rather than the working set. The caller
    declares what it knows a worker of its kind costs at work, and the
    measurement raises that number when the machine says the model is bigger than
    expected. It never lowers it.

    Every failure returns the floor. A probe can fail because psutil is missing,
    because the platform refuses the reading, or because the loader itself raised
    on a machine with no model installed, and none of those is a reason to guess
    high on the worker count.
    """
    if floor_bytes < 1:
        raise ValueError("floor_bytes must be at least one byte per worker")
    try:
        measured = (runner or _spawned_probe)(loader)
    except Exception:
        return floor_bytes
    if not isinstance(measured, int) or isinstance(measured, bool) or measured < 1:
        return floor_bytes
    return max(measured, floor_bytes)


def plan_pool(
    *,
    worker_bytes: int,
    items: int,
    ceiling: int = DEFAULT_WORKER_CEILING,
    headroom_percent: int = DEFAULT_HEADROOM_PERCENT,
    max_tasks_per_child: int | None = DEFAULT_MAX_TASKS_PER_CHILD,
    read_available: AvailableReader | None = None,
) -> PoolPlan:
    """Decide the pool for work whose every worker costs ``worker_bytes``.

    ``worker_bytes`` has no default on purpose. A default per-worker cost is a
    guess about somebody else's model, and a guess that is too low is the whole
    failure this module exists to prevent. A caller that cannot measure declares
    what it knows.

    THE ORDER OF THE ARITHMETIC IS THE UNIT. Headroom is applied to the byte
    budget BEFORE it is divided into workers::

        affordable = available * percent // 100 // worker_bytes

    Reversing those two steps, dividing into workers first and then scaling the
    count, gives a different answer at the boundaries and only at the boundaries.
    With 2900 mebibytes available and a 1024 mebibyte worker, this order affords
    two workers and the reversed order affords one. Both orders agree in the
    middle of the range, which is where a test not written to hunt for this
    happens to sit, and both read as "apply the headroom" to somebody skimming.

    A memory reading that cannot be taken falls back to ONE worker. It never
    falls back to a core count, a configured count, or the ceiling: every one of
    those can be larger than what the machine can carry, and a fallback that can
    be larger than the thing it is standing in for is not a fallback.

    Ties resolve to :attr:`Bound.AVAILABLE_MEMORY`, because when memory and the
    ceiling agree it is memory that will disagree tomorrow, on a machine where
    somebody opened something else.
    """
    if worker_bytes < 1:
        raise ValueError("worker_bytes must be at least one byte per worker")
    if ceiling < 1:
        raise ValueError("ceiling must allow at least one worker")
    if not 1 <= headroom_percent <= 100:
        raise ValueError("headroom_percent must be a percentage between 1 and 100")
    if items < 0:
        raise ValueError("items must be a count of work items, so never negative")
    if max_tasks_per_child is not None and max_tasks_per_child < 1:
        raise ValueError("max_tasks_per_child must be at least one task per child")

    available = _read_available(read_available or available_bytes)
    if available is None:
        return PoolPlan(
            workers=1,
            bound=Bound.MEMORY_UNREADABLE,
            worker_bytes=worker_bytes,
            available_bytes=None,
            max_tasks_per_child=None,
        )

    affordable = available * headroom_percent // 100 // worker_bytes
    # Declared in precedence order, and ``min`` returns the FIRST smallest, which
    # is what makes the tie rule above true rather than incidental. The platform
    # limit is last because it is the least informative answer to "why is this
    # run narrow", and it is absent entirely rather than standing in as a huge
    # number, because a sentinel that is nearly always the largest value is a
    # sentinel nobody checks.
    limits: list[tuple[Bound, int]] = [
        (Bound.AVAILABLE_MEMORY, affordable),
        (Bound.CEILING, ceiling),
        (Bound.WORK_ITEMS, items),
    ]
    platform_limit = platform_worker_ceiling()
    if platform_limit is not None:
        limits.append((Bound.PLATFORM_LIMIT, platform_limit))
    bound, smallest = min(limits, key=lambda limit: limit[1])
    workers = max(1, smallest)
    return PoolPlan(
        workers=workers,
        bound=bound,
        worker_bytes=worker_bytes,
        available_bytes=available,
        # A plan that runs in the calling process has no child to recycle, and
        # reporting a recycle count for a pool that does not exist is a number
        # somebody eventually acts on.
        max_tasks_per_child=None if workers == 1 else max_tasks_per_child,
    )


def _read_available(reader: AvailableReader) -> int | None:
    """The reading, or None when it could not be taken or cannot be believed.

    Broad by design. psutil may be absent, the platform may refuse, and a reading
    that arrives as a negative number or as something that is not an integer is
    no more usable than an exception. Every one of those means the same thing to
    the caller, which is that this process does not know how much room it has,
    and the answer to not knowing is one worker.
    """
    try:
        value = reader()
    except Exception:
        return None
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        return None
    return value


def executor_arguments(
    plan: PoolPlan,
    *,
    initializer: Callable[..., None] | None = None,
    initargs: tuple[Any, ...] = (),
) -> dict[str, Any]:
    """The keyword arguments for the pool ``plan`` describes.

    Refuses a plan of one worker rather than building a pool of one. The refusal
    is the point: a caller that reaches here with an in-process plan has skipped
    the branch that was supposed to keep the work in this process, and failing
    loudly at the seam is how that is caught in the unit that introduced it.

    The spawn context is not a preference. Sizing above assumes a child shares
    nothing with its parent, and recycling a child after a fixed number of tasks
    is unsupported under fork, so both the arithmetic and the recycle depend on
    this one argument being here.
    """
    if plan.in_process:
        raise ValueError(
            "a plan of one worker runs in the calling process; there is no pool "
            "to build. Branch on plan.in_process before asking for a pool."
        )
    arguments: dict[str, Any] = {
        "max_workers": plan.workers,
        "mp_context": multiprocessing.get_context("spawn"),
        "initializer": initializer,
        "initargs": initargs,
    }
    if plan.max_tasks_per_child is not None:
        arguments["max_tasks_per_child"] = plan.max_tasks_per_child
    return arguments


def map_workers(
    plan: PoolPlan,
    function: Callable[[_Item], _Result],
    items: Iterable[_Item],
    *,
    initializer: Callable[..., None] | None = None,
    initargs: tuple[Any, ...] = (),
) -> list[_Result]:
    """Run ``function`` over ``items`` at the width ``plan`` decided.

    Results come back in the order the items went in, at every width, so a caller
    never has to sort to be deterministic and a run at one worker and a run at
    four produce the same output rather than nearly the same output.

    A plan of one worker calls the initializer in THIS process and then does the
    work here. That is the same contract a pool gives, once per process, and it
    means an initializer must be safe to call in a process that is going on to do
    other things.

    Exists so that "a cap of one skips the pool" is true by construction rather
    than by every caller remembering. A call site that builds its own executor
    keeps its own copy of that branch, and the copies drift.
    """
    ordered = list(items)
    if plan.in_process:
        if initializer is not None:
            initializer(*initargs)
        return [function(item) for item in ordered]
    # Named ``executor`` rather than ``pool``, which is this module's own name and
    # is the shape of the naming collision this repository keeps recording: one
    # word meaning two things, here inside one file.
    with ProcessPoolExecutor(
        **executor_arguments(plan, initializer=initializer, initargs=initargs)
    ) as executor:
        return list(executor.map(function, ordered))


__all__ = [
    "AvailableReader",
    "BOUND_PHRASES",
    "Bound",
    "DEFAULT_HEADROOM_PERCENT",
    "DEFAULT_MAX_TASKS_PER_CHILD",
    "DEFAULT_WORKER_CEILING",
    "PoolPlan",
    "ProbeRunner",
    "available_bytes",
    "executor_arguments",
    "map_workers",
    "measure_worker_bytes",
    "plan_pool",
    "platform_worker_ceiling",
    "resident_bytes",
]
