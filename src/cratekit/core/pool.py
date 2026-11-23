"""How many worker processes may run at once, decided by memory rather than by cores.

R23 in one sentence: no default-configuration run exhausts memory, on any pool.

**Cores are not the scarce thing.** Sizing a pool as ``cpu_count() - 2`` gave
nine workers each loading a 300 megabyte model on an 18 gigabyte machine
already in swap, and the kernel killed the run. Nothing here reads the core
count, not to bound, floor or break a tie, and the test that checks it walks
the tree. A ceiling from the cores comes from outside (U241): a caller passes
``ceiling`` from :func:`cratekit.core.cores.worker_ceiling`, the one place a
core count is read, and it can only lower a plan.

**Every pool is spawned**, so each worker pays the full per-worker cost and the
arithmetic is the same on every platform. Spawn makes the function, the
initializer and its arguments a contract: they must pickle. :func:`map_workers`
and :func:`stream_workers` refuse what does not on every path, the in-process
one included, so a call means one thing on every machine.

**Five brakes, and none of them is redundant:**

1. *The available-memory reading* adapts to what the machine is doing now.
   Available, never free: free excludes evictable cache and starves a warm
   machine. ``test_pool_sizing.py`` fails if ``free`` is ever read.
2. *The absolute reserve* comes off BEFORE the percent and is the one brake
   that does not shrink with the reading.
3. *The headroom percent* covers an optimistic reading, and is lower on darwin,
   where available is mostly the inactive queue.
4. *The pressure gate* refuses a pool to a machine already in swap or nearly
   full, which the same available reading cannot tell from an idle one.
5. *The hard ceiling* covers the per-worker estimate, which a probe measures
   at load time and so is a LOWER bound on a working worker.

**The reading is the smaller of the host's and this process's own memory
cgroup's**, read from ``/proc/self/cgroup`` and every ancestor, so a container
or a capped systemd unit is not sized by its host. With no cgroup the reading
is exactly the host's.

**The recycle is done here, because the platform's deadlocks.**
``ProcessPoolExecutor(max_tasks_per_child=N)`` hangs, with no timeout and no
exception, once given more than ``workers * N`` tasks with ``N`` of two or
more: each child leaves ``N - 1`` stale idle-worker tokens, which absorb every
replacement spawn. So :func:`map_workers` gives one executor one GENERATION of
``workers * N`` items and builds a fresh one for the next. A pool may start
fewer children than its width, so one child may serve up to a whole
generation: the per-child bound is ``workers * N`` at worst and ``N``
ordinarily.

**Results one at a time (U241).** :func:`stream_workers` runs the same plan the
same way and hands back each result when asked for by position, while the
workers run ahead; everything that writes stays with the caller. Its children
ignore the terminal's interrupt, so the caller chooses where to stop, and
leave when their parent dies, so they never hold their memory for ever.

**Thread pools are out of scope.** Threads share one address space, so a second
thread does not cost a second model.

**Where R23 stops being enforceable.** A machine that affords no worker still
gets one, in this process. :attr:`Bound.INSUFFICIENT_MEMORY` is separate from
:attr:`Bound.AVAILABLE_MEMORY` so a caller that would rather refuse can branch.

Layer note: INFRASTRUCTURE. It reads the machine and builds processes, and it
names no verb, no feature module, and no taxonomy.
"""

from __future__ import annotations

import contextlib
import multiprocessing
import os
import pickle
import signal
import sys
import threading
from concurrent.futures import Future, ProcessPoolExecutor
from concurrent.futures import process as _process_pool
from dataclasses import dataclass
from enum import StrEnum
from multiprocessing import connection as _connection
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable, Generic, Iterable, Mapping, TypeVar

# The ceiling a caller passes is read in ``core.cores`` and never here. It is
# re-exported for the feature package that sizes a pool, which may import this
# module and not that one (U331), so a spawned worker loads nothing more for
# it; nothing in this module calls it.
from cratekit.core.cores import worker_ceiling as worker_ceiling

#: The hard ceiling on workers for a pool whose children each hold a model: two
#: is the survival-tested count. A caller with a cheaper worker raises it.
DEFAULT_WORKER_CEILING = 2

#: Bytes taken off the top of the reading before any percentage is applied.
#: Absolute, because the system and whatever the user has open need the same
#: room on a tight machine as on a roomy one; two gibibytes is a measured
#: desktop working set. Subtracted before the percent, never instead of it.
DEFAULT_MEMORY_RESERVE_BYTES = 2 * 1024**3

#: The share of what is left that a pool may claim, off darwin. An integer
#: percent, so the boundary between two worker counts is exact arithmetic.
GENERAL_HEADROOM_PERCENT = 75

#: The same share on darwin, where available measured 91 percent inactive queue
#: (4.80 gibibytes inactive against 0.28 free), much of it costly to reclaim.
DARWIN_HEADROOM_PERCENT = 50


def default_headroom_percent(platform: str = sys.platform) -> int:
    """The headroom share for one platform, defaulting to the running one.

    A function, so both answers are checkable from any machine.
    """
    return DARWIN_HEADROOM_PERCENT if platform == "darwin" else GENERAL_HEADROOM_PERCENT


#: The share this machine gets, resolved once at import.
DEFAULT_HEADROOM_PERCENT = default_headroom_percent()

#: Swap in use at or above which no pool is planned at all. A gibibyte rather
#: than a byte because darwin's swap use is sticky after a busy spell.
DEFAULT_SWAP_PRESSURE_BYTES = 1 * 1024**3

#: Physical memory in use, as a percent, at or above which no pool is planned:
#: past it the platform reclaims to serve ordinary allocations.
DEFAULT_USED_PERCENT_CEILING = 85

#: How many tasks one child may serve before it is retired, bounding allocator
#: growth. Spent as a generation by :func:`map_workers`, never handed to the
#: executor's own ``max_tasks_per_child``, which deadlocks at this default.
DEFAULT_MAX_TASKS_PER_CHILD = 100

#: How long a probe may take before its answer is abandoned and the floor
#: stands. Twice the reference load, a cold 300 megabyte model off a slow
#: spinning disk at about a minute; the suite holds it between twice and five
#: times that reference, and the shipped value sits on the floor.
DEFAULT_PROBE_TIMEOUT_SECONDS = 120.0

#: How long a probe child is given to die at each escalation of :func:`_reap`.
#: Long enough that the terminate rung lets a child unwind rather than racing
#: its release, short enough not to stall in front of the kill. The suite holds
#: it inside a band calibrated against a timed release.
_PROBE_REAP_SECONDS = 1.0

#: The two tags a probe child sends back, so a refusal is a value the parent reads.
_PROBE_MEASURED = "measured"
_PROBE_FAILED = "failed"

#: A reading of how much memory a new process could obtain, in bytes. Injected
#: by every test, so no test depends on what the machine is doing.
AvailableReader = Callable[[], int]

#: A run of one probe worker, returning its resident bytes once its loader has
#: finished. Injected the same way.
ProbeRunner = Callable[[Callable[[], object]], int]

_Item = TypeVar("_Item")
_Result = TypeVar("_Result")


class Bound(StrEnum):
    """Which constraint decided the worker count.

    ``MEMORY_UNREADABLE``, ``INSUFFICIENT_MEMORY`` and ``MEMORY_PRESSURE`` are
    their own values because each is a different situation, with a different
    fix, from a machine that is merely tight.
    """

    AVAILABLE_MEMORY = "available_memory"
    INSUFFICIENT_MEMORY = "insufficient_memory"
    MEMORY_PRESSURE = "memory_pressure"
    CEILING = "ceiling"
    WORK_ITEMS = "work_items"
    PLATFORM_LIMIT = "platform_limit"
    MEMORY_UNREADABLE = "memory_unreadable"


#: One phrase per bound, for the line a caller logs. The literal is parsed for a
#: duplicate key, which collapses silently at parse time.
BOUND_PHRASES: Mapping[Bound, str] = MappingProxyType(
    {
        Bound.AVAILABLE_MEMORY: "available memory",
        Bound.INSUFFICIENT_MEMORY: "memory that does not afford even one worker",
        Bound.MEMORY_PRESSURE: "a machine already under memory pressure",
        Bound.CEILING: "the declared worker ceiling",
        Bound.WORK_ITEMS: "the number of work items",
        Bound.PLATFORM_LIMIT: "this platform's own limit on pool width",
        Bound.MEMORY_UNREADABLE: "a memory reading that could not be taken",
    }
)


@dataclass(frozen=True)
class Pressure:
    """What the machine is already paying to hold what it is currently holding.

    The signal that tells an idle machine from one deep in swap when both report
    the same available bytes.
    """

    swap_used_bytes: int
    used_percent: float


class PressureGate(StrEnum):
    """Which of the two pressure gates refused a pool (U241).

    Swap in use is history, sticky on darwin until a restart; the used percent
    is the present, cleared by closing something.
    """

    SWAP = "swap"
    USED_PERCENT = "used_percent"


@dataclass(frozen=True)
class GateReading:
    """One pressure gate that refused, with the reading it saw and the limit it held.

    Bytes for the swap gate, a percent for the used percent gate.
    """

    gate: PressureGate
    reading: float
    limit: float

    def sentence(self) -> str:
        """The refusal in words a person can act on."""
        if self.gate is PressureGate.SWAP:
            return (
                f"{shown_bytes(int(self.reading))} of swap is in use, at or over "
                f"the {shown_bytes(int(self.limit))} gate"
            )
        return (
            f"memory is {self.reading:.0f} percent in use, at or over "
            f"the {self.limit:.0f} percent gate"
        )


def shown_bytes(count: int) -> str:
    """A byte count as a person reads it: megabytes under a gigabyte, else gigabytes."""
    if count >= 1024**3:
        return f"{count / 1024**3:.1f} GB"
    return f"{count / 1024**2:.0f} MB"


@dataclass(frozen=True)
class PoolPlan:
    """The decided shape of one pool: how wide, why, over how much, and in what generations.

    ``in_process`` is a property, so it cannot disagree with ``workers``: a plan
    of one runs in the calling process and never starts a pool of one. ``items``
    is carried so :attr:`generations` is a question the plan answers itself.
    """

    workers: int
    items: int
    bound: Bound
    worker_bytes: int
    available_bytes: int | None
    max_tasks_per_child: int | None
    #: The ceiling the plan was decided under (U241); None on a plan built by hand.
    ceiling: int | None = None
    #: Every pressure gate that refused a pool, in the order checked, else empty.
    refused_by: tuple[GateReading, ...] = ()

    @property
    def in_process(self) -> bool:
        """True when the work runs in the calling process and no pool is built."""
        return self.workers == 1

    @property
    def tasks_per_generation(self) -> int | None:
        """The most work one executor may be given, or None when it may have all of it.

        Exactly what one generation of children can serve, and the line the
        platform's own recycle deadlocks one item past.
        """
        if self.max_tasks_per_child is None:
            return None
        return self.workers * self.max_tasks_per_child

    @property
    def generations(self) -> int:
        """How many times a fresh set of children is built for this much work."""
        size = self.tasks_per_generation
        if self.in_process or self.items == 0:
            return 0
        if size is None:
            return 1
        return -(-self.items // size)

    def explain(self) -> str:
        """One line saying what the count is and what decided it."""
        where = "in process" if self.in_process else f"{self.workers} workers"
        return f"{where}, bound by {BOUND_PHRASES[self.bound]}"

    def account(self) -> str:
        """The numbers behind :meth:`explain`, for a person deciding what to do (U241).

        A plan with no numbers to give says only what :meth:`explain` does,
        never an invented number.
        """
        ceiling = "" if self.ceiling is None else f", under a ceiling of {self.ceiling}"
        cost = shown_bytes(self.worker_bytes)
        if self.bound is Bound.MEMORY_PRESSURE and self.refused_by:
            gates = " and ".join(reading.sentence() for reading in self.refused_by)
            return f"{gates}, so no pool was planned{ceiling}"
        if self.available_bytes is not None and self.bound in (
            Bound.AVAILABLE_MEMORY,
            Bound.INSUFFICIENT_MEMORY,
        ):
            had = shown_bytes(self.available_bytes)
            if self.bound is Bound.INSUFFICIENT_MEMORY:
                return (
                    f"{had} available does not afford one worker at {cost} after "
                    f"the reserve and the headroom{ceiling}"
                )
            return (
                f"{had} available affords {self.workers} at {cost} a worker after "
                f"the reserve and the headroom{ceiling}"
            )
        if self.bound is Bound.CEILING and self.ceiling is not None:
            return f"the ceiling of {self.ceiling} is what held it, at {cost} a worker"
        if self.bound is Bound.WORK_ITEMS:
            return f"{self.items} item(s) to run{ceiling}"
        return BOUND_PHRASES[self.bound]


#: Where the kernel publishes cgroup memory limits. Also an argument, so every
#: test points the reader at a directory it wrote itself.
CGROUP_ROOT = Path("/sys/fs/cgroup")

#: Where the kernel publishes WHICH cgroup this process is in, so a capped
#: systemd unit below an uncapped root is found.
CGROUP_SELF = Path("/proc/self/cgroup")

#: A published limit at least this large means "no limit": version one writes
#: a huge page-aligned value that has changed across kernels.
_CGROUP_UNLIMITED_ABOVE = 1 << 62


def _cgroup_text(path: Path) -> str | None:
    """One file the kernel publishes, as text, or None when it cannot be read.

    Broad on purpose: missing, unreadable or a directory (``OSError``), and
    undecodable bytes or an embedded null byte (``ValueError``) all mean no
    reading, never an exception out of :func:`available_bytes`.
    """
    try:
        return path.read_text()
    except (OSError, ValueError):
        return None


def _cgroup_number(path: Path) -> int | None:
    """One byte count the kernel published, or None, including ``max`` for no limit."""
    text = _cgroup_text(path)
    if text is None:
        return None
    try:
        value = int(text.strip())
    except ValueError:
        return None
    return value if value >= 0 else None


def _cgroup_self_paths(text: str | None) -> tuple[str, str]:
    """Where this process sits, as (unified path, memory controller path).

    Each line is ``id:controllers:path``; version two leaves the controllers
    empty, version one comma separates them. The field is split and matched
    whole, so ``cpu,memory`` matches and ``memoryfoo`` does not. No file, as on
    darwin, means the root of both.
    """
    unified = controller = ""
    for line in (text or "").splitlines():
        fields = line.split(":", 2)
        if len(fields) != 3:
            continue
        _hierarchy, controllers, path = fields
        if not controllers:
            unified = path
        elif "memory" in controllers.split(","):
            controller = path
    return unified, controller


def _cgroup_directories(mount: Path, relative: str) -> list[Path]:
    """This process's own cgroup directory and every ancestor up to the mount.

    A cap on an ancestor binds this process, so every level is read. A path with
    ``..`` names no cgroup this process is in, so only the mount, which binds
    regardless, is read. Each level is resolved and kept only if it is still
    inside the resolved mount, since the mount is injected and reads follow
    symlinks.
    """
    fields = relative.split("/")
    if ".." in fields:
        candidates = [mount]
    else:
        parts = [part for part in fields if part]
        candidates = [mount.joinpath(*parts[:depth]) for depth in range(len(parts), -1, -1)]
    anchor = _resolved(mount)
    if anchor is None:
        return []
    return [inside for inside in (_contained(anchor, c) for c in candidates) if inside is not None]


def _resolved(path: Path) -> Path | None:
    """``path`` with every symlink followed, or None, so it is not read."""
    try:
        return path.resolve()
    except (OSError, RuntimeError, ValueError):
        return None


def _contained(anchor: Path, path: Path) -> Path | None:
    """``path`` resolved, or None when that lands outside ``anchor``; read what was checked."""
    resolved = _resolved(path)
    if resolved is None or not resolved.is_relative_to(anchor):
        return None
    return resolved


def _headroom_in(directory: Path, *, anchor: Path, limit_file: str, used_file: str) -> int | None:
    """Room left in ONE cgroup directory, or None when it publishes no cap.

    A cap with no readable usage is still a cap, so the limit is returned. The
    files are contained too, not only the directory.
    """
    limit_path = _contained(anchor, directory / limit_file)
    limit = None if limit_path is None else _cgroup_number(limit_path)
    if limit is None or limit >= _CGROUP_UNLIMITED_ABOVE:
        return None
    used_path = _contained(anchor, directory / used_file)
    used = None if used_path is None else _cgroup_number(used_path)
    if used is None:
        return limit
    return max(0, limit - used)


def cgroup_memory_headroom_bytes(
    root: Path = CGROUP_ROOT, *, self_cgroup: Path = CGROUP_SELF
) -> int | None:
    """Room left inside this process's own memory cgroup, or None when uncapped.

    None also means no cap could be read: a guessed limit would narrow every
    pool on machines that have none. The walk starts at this process's own
    cgroup rather than the root, and the tightest cap on the chain binds.
    """
    unified, controller = _cgroup_self_paths(_cgroup_text(self_cgroup))
    layouts = (
        (root, unified, "memory.max", "memory.current"),
        (root / "memory", controller, "memory.limit_in_bytes", "memory.usage_in_bytes"),
    )
    found: list[int] = []
    for mount, relative, limit_file, used_file in layouts:
        anchor = _resolved(mount)
        if anchor is None:
            continue
        for directory in _cgroup_directories(mount, relative):
            headroom = _headroom_in(
                directory, anchor=anchor, limit_file=limit_file, used_file=used_file
            )
            if headroom is not None:
                found.append(headroom)
    return min(found) if found else None


def available_bytes(*, cgroup_root: Path = CGROUP_ROOT, cgroup_self: Path = CGROUP_SELF) -> int:
    """Memory a new process could obtain right now, in bytes: available, never free.

    The smaller of the host reading and this process's cgroup headroom. The
    keyword arguments exist for tests, so this is still the zero argument
    :data:`AvailableReader`. psutil is imported lazily, so an injected reader
    never loads it.
    """
    import psutil

    reading = int(psutil.virtual_memory().available)
    capped = cgroup_memory_headroom_bytes(cgroup_root, self_cgroup=cgroup_self)
    return reading if capped is None else min(reading, capped)


def memory_pressure() -> Pressure:
    """What the machine is already paying, right now: swap in use and used percent."""
    import psutil

    return Pressure(
        swap_used_bytes=int(psutil.swap_memory().used),
        used_percent=float(psutil.virtual_memory().percent),
    )


#: A reading of what the machine is already paying. Injected by every sizing test.
PressureReader = Callable[[], Pressure]


def resident_bytes() -> int:
    """This process's resident set, in bytes; read inside a probe, one worker's cost."""
    import psutil

    return int(psutil.Process().memory_info().rss)


def platform_worker_ceiling() -> int | None:
    """The widest process pool this platform will build, or None where it does not care.

    Windows raises out of the executor's constructor above a fixed width. The
    interpreter's own number is read where published, else the current literal.
    """
    if sys.platform != "win32":
        return None
    limit = getattr(_process_pool, "_MAX_WINDOWS_WORKERS", 61)
    return int(limit) if isinstance(limit, int) and limit > 0 else 61


def _probe_entry(loader: Callable[[], object], writer: Any) -> None:
    """Run the caller's loader in this worker, then report what the worker costs.

    The model is held across the reading: freed first, darwin's allocator hands
    large blocks straight back and the probe reads about zero. A loader that
    raises is sent back as a tagged reason in text, since its exception may not
    pickle.
    """
    try:
        model = loader()
        try:
            measured = resident_bytes()
        finally:
            del model
    except Exception as failure:
        writer.send((_PROBE_FAILED, f"{type(failure).__name__}: {failure}"))
    else:
        writer.send((_PROBE_MEASURED, measured))
    finally:
        writer.close()


def _reap(worker: Any) -> None:
    """Make sure one probe child is gone, escalating, since a live one is still allocating."""
    worker.join(_PROBE_REAP_SECONDS)
    if worker.is_alive():
        worker.terminate()
        worker.join(_PROBE_REAP_SECONDS)
    if worker.is_alive():
        worker.kill()
        worker.join(_PROBE_REAP_SECONDS)
    if not worker.is_alive():
        worker.close()


def _spawned_probe(
    loader: Callable[[], object],
    *,
    timeout_seconds: float = DEFAULT_PROBE_TIMEOUT_SECONDS,
) -> int:
    """Run one real spawned worker and return its resident bytes after loading.

    A bare process and a pipe rather than an executor: a child that dies closes
    the pipe and wakes the parent at once, and one that hangs meets the timeout.
    """
    context = multiprocessing.get_context("spawn")
    reader, writer = context.Pipe(duplex=False)
    worker = context.Process(target=_probe_entry, args=(loader, writer))
    worker.start()
    # The parent's copy of the write end is closed so the pipe reaches end of
    # file the moment the child's copy does. Left open, a dead child would look
    # exactly like a slow one until the timeout expired.
    writer.close()
    try:
        if not reader.poll(timeout_seconds):
            raise TimeoutError(f"the probe loader did not finish within {timeout_seconds} seconds")
        outcome, answer = reader.recv()
    finally:
        reader.close()
        _reap(worker)
    # Redundant with int() below, kept so the loader's reason reaches the message.
    if outcome != _PROBE_MEASURED:
        raise RuntimeError(f"the probe loader failed in its worker: {answer}")
    return int(answer)


def measure_worker_bytes(
    loader: Callable[[], object],
    *,
    floor_bytes: int,
    timeout_seconds: float = DEFAULT_PROBE_TIMEOUT_SECONDS,
    runner: ProbeRunner | None = None,
) -> int:
    """What one worker of this shape costs, measured, never below ``floor_bytes``.

    A floor, not a fallback: the probe reads resident set when loading finishes,
    a lower bound on a working worker. Every failure returns the floor, a loader
    that never returns included. ``timeout_seconds`` governs the real probe
    only; an injected ``runner`` is called synchronously.
    """
    if floor_bytes < 1:
        raise ValueError("floor_bytes must be at least one byte per worker")
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must leave the probe some time to answer")
    try:
        if runner is not None:
            measured = runner(loader)
        else:
            measured = _spawned_probe(loader, timeout_seconds=timeout_seconds)
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
    reserve_bytes: int = DEFAULT_MEMORY_RESERVE_BYTES,
    max_tasks_per_child: int | None = DEFAULT_MAX_TASKS_PER_CHILD,
    swap_pressure_bytes: int = DEFAULT_SWAP_PRESSURE_BYTES,
    used_percent_ceiling: int = DEFAULT_USED_PERCENT_CEILING,
    read_available: AvailableReader | None = None,
    read_pressure: PressureReader | None = None,
) -> PoolPlan:
    """Decide the pool for work whose every worker costs ``worker_bytes``.

    ``worker_bytes`` has no default: a guessed cost that is too low is the
    failure this module prevents. THE ORDER OF THE ARITHMETIC IS THE UNIT::

        affordable = (available - reserve) * percent // 100 // worker_bytes

    Reserving after the percent underfunds the tight machine, and dividing
    before scaling differs at the boundaries: 2900 mebibytes, no reserve and a
    1024 mebibyte worker afford two here and one reversed.

    A machine under pressure is refused a pool before any of that. An
    unreadable memory reading falls back to ONE worker, never a core count or
    the ceiling; an unreadable PRESSURE reading counts as no pressure, since
    three brakes still apply. Ties resolve to :attr:`Bound.AVAILABLE_MEMORY`,
    the bound that changes when somebody opens something else.
    """
    if worker_bytes < 1:
        raise ValueError("worker_bytes must be at least one byte per worker")
    if ceiling < 1:
        raise ValueError("ceiling must allow at least one worker")
    if not 1 <= headroom_percent <= 100:
        raise ValueError("headroom_percent must be a percentage between 1 and 100")
    if reserve_bytes < 0:
        raise ValueError("reserve_bytes must be a number of bytes, so never negative")
    if swap_pressure_bytes < 0:
        raise ValueError("swap_pressure_bytes must be a number of bytes, so never negative")
    if not 1 <= used_percent_ceiling <= 100:
        raise ValueError("used_percent_ceiling must be a percentage between 1 and 100")
    if items < 0:
        raise ValueError("items must be a count of work items, so never negative")
    if max_tasks_per_child is not None and max_tasks_per_child < 1:
        raise ValueError("max_tasks_per_child must be at least one task per child")

    available = _read_available(read_available or available_bytes)
    if available is None:
        return PoolPlan(
            workers=1,
            items=items,
            bound=Bound.MEMORY_UNREADABLE,
            worker_bytes=worker_bytes,
            available_bytes=None,
            max_tasks_per_child=None,
            ceiling=ceiling,
        )

    pressure = _read_pressure(read_pressure or memory_pressure)
    refused = _gates_refusing(
        pressure,
        swap_pressure_bytes=swap_pressure_bytes,
        used_percent_ceiling=used_percent_ceiling,
    )
    if refused:
        return PoolPlan(
            workers=1,
            items=items,
            bound=Bound.MEMORY_PRESSURE,
            worker_bytes=worker_bytes,
            available_bytes=available,
            max_tasks_per_child=None,
            ceiling=ceiling,
            refused_by=refused,
        )

    budget = max(0, available - reserve_bytes)
    affordable = budget * headroom_percent // 100 // worker_bytes
    # In precedence order: ``min`` returns the FIRST smallest, which makes the
    # tie rule true. The platform limit is absent rather than a huge sentinel.
    limits: list[tuple[Bound, int]] = [
        (Bound.AVAILABLE_MEMORY, affordable),
        (Bound.CEILING, ceiling),
        (Bound.WORK_ITEMS, items),
    ]
    platform_limit = platform_worker_ceiling()
    if platform_limit is not None:
        limits.append((Bound.PLATFORM_LIMIT, platform_limit))
    bound, smallest = min(limits, key=lambda limit: limit[1])
    if bound is Bound.AVAILABLE_MEMORY and smallest == 0:
        # Same count, different reason: affording none is R23 unenforceable.
        bound = Bound.INSUFFICIENT_MEMORY
    workers = max(1, smallest)
    return PoolPlan(
        workers=workers,
        items=items,
        bound=bound,
        worker_bytes=worker_bytes,
        available_bytes=available,
        # An in process plan has no child to retire.
        max_tasks_per_child=None if workers == 1 else max_tasks_per_child,
        ceiling=ceiling,
    )


def _gates_refusing(
    pressure: Pressure | None, *, swap_pressure_bytes: int, used_percent_ceiling: int
) -> tuple[GateReading, ...]:
    """Every pressure gate this reading meets, swap first, or none (U241)."""
    if pressure is None:
        return ()
    refused: list[GateReading] = []
    if pressure.swap_used_bytes >= swap_pressure_bytes:
        refused.append(
            GateReading(PressureGate.SWAP, float(pressure.swap_used_bytes), float(swap_pressure_bytes))
        )
    if pressure.used_percent >= used_percent_ceiling:
        refused.append(
            GateReading(
                PressureGate.USED_PERCENT, float(pressure.used_percent), float(used_percent_ceiling)
            )
        )
    return tuple(refused)


def _read_available(reader: AvailableReader) -> int | None:
    """The reading, or None when it raised or is not a non-negative integer."""
    try:
        value = reader()
    except Exception:
        return None
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        return None
    return value


def _read_pressure(reader: PressureReader) -> Pressure | None:
    """What the machine is paying, or None when the reading raised or is malformed."""
    try:
        value = reader()
    except Exception:
        return None
    if not isinstance(value, Pressure):
        return None
    swap, used = value.swap_used_bytes, value.used_percent
    if not isinstance(swap, int) or isinstance(swap, bool) or swap < 0:
        return None
    if isinstance(used, bool) or not isinstance(used, (int, float)):
        return None
    if not 0 <= used <= 100:
        return None
    return value


def executor_arguments(
    plan: PoolPlan,
    *,
    initializer: Callable[..., None] | None = None,
    initargs: tuple[Any, ...] = (),
) -> dict[str, Any]:
    """The keyword arguments for ONE GENERATION of the pool ``plan`` describes.

    Refuses a plan of one worker, so a caller that skipped the in-process branch
    fails at the seam. The spawn context is what the sizing assumes.
    ``max_tasks_per_child`` is deliberately absent: the executor's own recycle
    deadlocks, so the recycle is :func:`map_workers`'s generation boundary.
    """
    if plan.in_process:
        raise ValueError(
            "a plan of one worker runs in the calling process; there is no pool "
            "to build. Branch on plan.in_process before asking for a pool."
        )
    return {
        "max_workers": plan.workers,
        "mp_context": multiprocessing.get_context("spawn"),
        "initializer": initializer,
        "initargs": initargs,
    }


def _refuse_what_no_child_could_receive(value: object, role: str) -> None:
    """Refuse a value no spawned child could receive, on every path.

    Otherwise a closure runs on an in-process plan and fails on a pooled one,
    and the same call changes its contract with the machine's memory.
    """
    try:
        pickle.dumps(value)
    except Exception as failure:
        raise ValueError(
            f"the {role} passed to map_workers cannot be sent to a worker "
            f"process ({failure}). Pools here are spawned, so a child imports it "
            f"by name: use a module-level function rather than a lambda, a local "
            f"function, or a closure. This is refused on every path, including "
            f"the in-process one, so a run does not change its contract with the "
            f"amount of memory the machine happened to have."
        ) from failure


def _refuse_unsendable(
    function: object, initializer: object | None, initargs: tuple[Any, ...]
) -> None:
    """Hold the function, the initializer and every initializer argument to the rule.

    The arguments are checked even with no initializer, so it is one rule.
    """
    _refuse_what_no_child_could_receive(function, "function")
    if initializer is not None:
        _refuse_what_no_child_could_receive(initializer, "initializer")
    for position, argument in enumerate(initargs):
        _refuse_what_no_child_could_receive(argument, f"initializer argument {position}")


def map_workers(
    plan: PoolPlan,
    function: Callable[[_Item], _Result],
    items: Iterable[_Item],
    *,
    initializer: Callable[..., None] | None = None,
    initargs: tuple[Any, ...] = (),
) -> list[_Result]:
    """Run ``function`` over ``items`` at the width ``plan`` decided.

    Results come back in item order at every width. A plan of one calls the
    initializer and does the work in THIS process. A wider plan runs in
    generations of ``workers * max_tasks_per_child`` items, one executor each,
    which is the recycle. All or nothing: one item that raises discards every
    result, and the exception raised is the first in item order.
    """
    _refuse_unsendable(function, initializer, initargs)
    ordered = list(items)
    if plan.in_process:
        if initializer is not None:
            initializer(*initargs)
        return [function(item) for item in ordered]
    generation = plan.tasks_per_generation or len(ordered) or 1
    results: list[_Result] = []
    for start in range(0, len(ordered), generation):
        with ProcessPoolExecutor(
            **executor_arguments(plan, initializer=initializer, initargs=initargs)
        ) as executor:
            results.extend(executor.map(function, ordered[start : start + generation]))
    return results


class StreamBroken(RuntimeError):
    """The stream's workers are gone, so no further result will come from them.

    The POOL failed, not the item, which is unmeasured. An exception the work
    itself raised arrives as itself.
    """


def _leave_when_the_parent_does() -> None:
    """Exit this worker the moment the process that spawned it is gone.

    A worker holds its own call queue's write end, so a killed parent never
    closes it; the parent's sentinel is what ends with the parent.
    """
    parent = multiprocessing.parent_process()
    if parent is None:
        return

    def watch() -> None:
        try:
            _connection.wait([parent.sentinel])
        except Exception:
            return
        os._exit(0)

    threading.Thread(target=watch, name="cratekit-pool-parent-watch", daemon=True).start()


def _enter_stream_worker(
    initializer: Callable[..., None] | None, initargs: tuple[Any, ...]
) -> None:
    """What every stream worker runs first: the two rules, then the caller's own.

    The terminal's interrupt is ignored, so Ctrl-C does not break the pool
    mid item; the caller owns the stop and closes the stream.
    """
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    _leave_when_the_parent_does()
    if initializer is not None:
        initializer(*initargs)


def _end_workers(executor: ProcessPoolExecutor) -> None:
    """Stop an executor's children now rather than after the work nobody will read.

    The interpreter's own way where it exists, else the process table; with
    neither, the shutdown that follows waits, slower and still correct.
    """
    terminate = getattr(executor, "terminate_workers", None)
    if callable(terminate):
        with contextlib.suppress(Exception):  # the waiting shutdown still follows
            terminate()
        return
    for process in list((getattr(executor, "_processes", None) or {}).values()):
        with contextlib.suppress(Exception):  # one already gone is not a failure
            process.terminate()


class WorkStream(Generic[_Item, _Result]):
    """``function`` over ``items`` at the plan's width, one result asked for at a time.

    The contract of :func:`map_workers`, for a caller that settles one item
    before it wants the next:

    * a plan of one runs each item in THIS process when its result is asked
      for, after calling the initializer here once;
    * a wider plan spawns one generation of children at a time, hands it its
      items at once, and the children run ahead of the caller;
    * anything unsendable is refused at construction, on both paths.

    Each position is read once, on both paths, and a second read raises. What
    the work raised is raised to the reader of that position; a pool that died
    is :class:`StreamBroken`. :meth:`close` ends the children without waiting
    and is safe to call twice; use the stream as a context manager.
    """

    def __init__(
        self,
        plan: PoolPlan,
        function: Callable[[_Item], _Result],
        items: Iterable[_Item],
        *,
        initializer: Callable[..., None] | None = None,
        initargs: tuple[Any, ...] = (),
    ) -> None:
        _refuse_unsendable(function, initializer, initargs)
        self.plan = plan
        self._function = function
        self._items: list[_Item] = list(items)
        self._initializer = initializer
        self._initargs = initargs
        self._initialized_here = False
        self._executor: ProcessPoolExecutor | None = None
        self._generation: int | None = None
        self._futures: dict[int, Future[_Result]] = {}
        self._read: set[int] = set()
        self._closed = False

    def __len__(self) -> int:
        return len(self._items)

    def __enter__(self) -> WorkStream[_Item, _Result]:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    @property
    def closed(self) -> bool:
        return self._closed

    def result(self, position: int) -> _Result:
        """The result of the item at ``position``, waiting for it if it is not in yet."""
        if self._closed:
            raise ValueError("this stream is closed, so it has no further results")
        if isinstance(position, bool) or not isinstance(position, int):
            raise TypeError("a position is a whole number")
        if not 0 <= position < len(self._items):
            raise IndexError(f"position {position} is outside the {len(self._items)} item(s)")
        if position in self._read:
            raise ValueError(f"position {position} was already read, and each is read once")
        if self.plan.in_process:
            self._read.add(position)
            if not self._initialized_here:
                self._initialized_here = True
                if self._initializer is not None:
                    self._initializer(*self._initargs)
            return self._function(self._items[position])
        size = self.plan.tasks_per_generation or len(self._items) or 1
        generation = position // size
        try:
            if generation != self._generation:
                self._stop()
                self._start(generation, size)
            self._read.add(position)
            return self._futures.pop(position).result()
        except _process_pool.BrokenProcessPool as broken:
            # Wherever it broke, handing out the work (a child dying in its
            # initializer) or waiting on it: one closed stream, never a rebuild.
            self.close()
            raise StreamBroken(
                f"the pool's workers ended before item {position} was measured ({broken})"
            ) from broken

    def _start(self, generation: int, size: int) -> None:
        """Build one generation's executor and hand it every item not yet read."""
        executor = ProcessPoolExecutor(
            **executor_arguments(
                self.plan,
                initializer=_enter_stream_worker,
                initargs=(self._initializer, self._initargs),
            )
        )
        self._executor = executor
        self._generation = generation
        first = generation * size
        try:
            for position in range(first, min(first + size, len(self._items))):
                if position not in self._read:
                    self._futures[position] = executor.submit(self._function, self._items[position])
        except BaseException:
            self._stop()
            raise

    def _stop(self) -> None:
        """End the current generation: nothing queued starts, nothing running is waited for."""
        executor, self._executor = self._executor, None
        futures, self._futures = self._futures, {}
        self._generation = None
        if executor is None:
            return
        for future in futures.values():
            future.cancel()
        _end_workers(executor)
        executor.shutdown(wait=True, cancel_futures=True)

    def close(self) -> None:
        """End the stream. Idempotent, and never waits for work nobody will read."""
        if self._closed:
            return
        self._closed = True
        self._stop()


def stream_workers(
    plan: PoolPlan,
    function: Callable[[_Item], _Result],
    items: Iterable[_Item],
    *,
    initializer: Callable[..., None] | None = None,
    initargs: tuple[Any, ...] = (),
) -> WorkStream[_Item, _Result]:
    """Run ``function`` over ``items`` at the plan's width, results read by position.

    Nothing is spawned until the first result is asked for. See
    :class:`WorkStream` for the contract, and close what this returns.
    """
    return WorkStream(plan, function, items, initializer=initializer, initargs=initargs)


__all__ = [
    "AvailableReader",
    "BOUND_PHRASES",
    "Bound",
    "CGROUP_ROOT",
    "CGROUP_SELF",
    "DARWIN_HEADROOM_PERCENT",
    "DEFAULT_HEADROOM_PERCENT",
    "DEFAULT_MAX_TASKS_PER_CHILD",
    "DEFAULT_MEMORY_RESERVE_BYTES",
    "DEFAULT_PROBE_TIMEOUT_SECONDS",
    "DEFAULT_SWAP_PRESSURE_BYTES",
    "DEFAULT_USED_PERCENT_CEILING",
    "DEFAULT_WORKER_CEILING",
    "GENERAL_HEADROOM_PERCENT",
    "GateReading",
    "PoolPlan",
    "Pressure",
    "PressureGate",
    "PressureReader",
    "ProbeRunner",
    "StreamBroken",
    "WorkStream",
    "available_bytes",
    "cgroup_memory_headroom_bytes",
    "default_headroom_percent",
    "executor_arguments",
    "map_workers",
    "measure_worker_bytes",
    "memory_pressure",
    "plan_pool",
    "platform_worker_ceiling",
    "resident_bytes",
    "shown_bytes",
    "stream_workers",
    "worker_ceiling",
]
