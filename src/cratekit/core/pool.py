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
arithmetic below and the behaviour on the machine agree everywhere.

**Spawn is also a contract on the caller, and it is enforced rather than
implied.** A spawned child imports the work by name, so the function and the
initializer have to be importable: a lambda, a closure, or a function defined
inside another function cannot go. That was true before and was never said, which
made it worse than a restriction. It made the SAME call mean two different things
depending on the machine: an in-process plan runs the closure happily and a
pooled plan raises about a local object, so a caller could develop against a busy
laptop and discover the rule on a quiet server. :func:`map_workers` now refuses an
unsendable callable, and an unsendable initializer argument, on both paths
before either runs.

**Five brakes, and none of them is redundant.** Each one covers a failure of the
others:

1. *The available-memory reading* adapts to what the machine is doing right now,
   which none of the others can see.
2. *The absolute reserve* is the only brake whose size does not shrink with the
   reading. A percentage of a small number is a small number, and the machine
   still owes the operating system, this process, and whatever the user has open
   the same fixed amount it owed when the reading was large.
3. *The headroom percent* covers the reading being optimistic. On macOS the
   platform counts the inactive queue as available, so the number is a ceiling on
   what a new process can really get rather than a promise.
4. *The pressure gate* covers the reading being optimistic in a way arithmetic
   cannot see at all. Four and three quarter gibibytes available on an idle
   machine and the same reading on a machine already two gibibytes into swap are
   the same number describing two different machines, and only one of them can
   carry a second worker.
5. *The hard ceiling* covers the per-worker estimate being wrong. A probe
   measures resident set at the moment the model finishes loading, which is a
   LOWER bound on what the worker holds while it is actually working.

**Available, never free.** They are different numbers. Free is memory nobody
holds at all; available is what a new process can obtain without pushing the
machine into swap, and it includes cache the kernel would evict. A pool sized
against free memory starves on a healthy machine whose cache is warm, which is
every machine that has been doing work. ``test_pool_sizing.py`` walks this
module's syntax tree and fails if ``free`` is ever read.

**Available is not a promise, and on darwin it is barely a hint.** Measured on
the 18 gibibyte machine this product is built on, with nothing unusual running:
psutil computes darwin's ``available`` as the inactive queue plus free memory,
and the split was 4.80 gibibytes inactive against 0.28 free. Ninety one percent
of "available" was the inactive queue, which is not all cheaply reclaimable and
includes dirty anonymous pages whose reclamation means compressing or writing to
swap. At the same instant the machine reported 2.21 gibibytes of swap already in
use. Seventy five percent of that reading turns into three workers at a one
gibibyte model and twelve at the 300 megabyte model named above, on a machine
that was already paying to hold what it had. That is the documented kill
reproduced through new arithmetic, so the arithmetic changed: an absolute reserve
comes off the top BEFORE the percent, the percent itself is lower on darwin than
elsewhere, and a machine already in swap is refused a pool outright. Those are
three separate answers to three separate ways the reading lies, which is why none
of them replaced another.

**A container is a sixth way the reading lies, and the only one where the
number belongs to a different machine rather than merely being optimistic.**
psutil answers out of the host's own counters. A process capped at half a
gibibyte inside a container on a sixty four gibibyte host is told it has sixty
four gibibytes, and every brake above then does its arithmetic on a number a
hundred times the truth: the reserve comes off it, the percent scales what is
left, and the pressure gate reads the host's swap and the host's used percent,
both of which are fine. So the reading is the SMALLER of what the machine says
and what this process's own memory cgroup allows, and a machine with no cgroup
at all reads exactly what it read before. "This process's own" is read from
``/proc/self/cgroup`` rather than assumed to be the top of the hierarchy,
because that assumption holds only inside a cgroup namespaced container: a
capped systemd unit sits several levels down and the root publishes no cap at
all, so a reader that stopped at the root would report no limit for a service
that has one. This is the same blindness the core
count is refused for: the four spellings forbidden below include the two
affinity calls precisely because somebody reaches for them on reading that a
core count ignores cgroup limits, and a module that refused cores for that
reason while reading memory the same way would have moved the defect rather
than ended it.

**A recycle this module performs itself, because the platform's own deadlocks.**
``ProcessPoolExecutor(max_tasks_per_child=N)`` hangs forever, with no timeout and
no exception, whenever it is given more than ``workers * N`` tasks and ``N`` is
two or more. The mechanism is in the executor's own bookkeeping: a worker that
finishes a task without exiting releases a token onto an idle-worker semaphore,
and a worker that exits at its task limit is replaced through a path that first
tries to acquire one of those tokens and returns early when it succeeds. Each
child leaves ``N - 1`` stale tokens behind it, so every recycle is absorbed by a
token from a worker that is already dead and no replacement is ever spawned. The
queued items then have no consumer. At this module's own defaults, two workers
and a hundred tasks per child, 200 items finish in under a tenth of a second and
201 items never finish at all. It reproduces on every interpreter this product
supports. So :func:`map_workers` hands one executor no more work than one
GENERATION of children can serve, and builds a fresh executor for the next
generation. The generation boundary IS the recycle: fresh interpreters, fresh
imports, fresh model, bounded allocator, and no dependence on a mechanism that
deadlocks.

**A nearer miss, recorded because it rules out the obvious half fix.** Keeping
the platform's counter and merely capping each executor at ``workers * N`` items
looks equivalent to the above and is not, because a pool does not reliably start
as many children as it was sized for. The executor spawns lazily, one child per
submitted item, and skips the spawn whenever an idle-worker token is already
waiting, so a generation sized against the FULL width can be served by fewer
children than that. Observed directly while building this: two workers given two
items were repeatedly served by one child, because the first child to finish
importing drained the queue before the second was ready. Under the platform's
counter that is a generation whose real capacity is half its size, which is the
deadlock again, arrived at from the other direction. With the counter gone the
same observation is harmless, since a child that never exits mid-generation is
always still there to consume what is queued. The cost of doing it this way is
one line of honesty: a single child may serve up to a whole generation rather
than exactly ``N`` tasks, so the per-child bound is ``workers * N`` in the worst
case and ``N`` in the ordinary one. A looser bound that always holds beats a
tighter one that hangs.

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

**Where R23 stops being enforceable, said out loud.** A machine whose reading
does not afford even one worker gets one worker anyway, in this process, because
there is no smaller answer available and refusing the work is not this module's
call to make. The count is honest about it: :attr:`Bound.INSUFFICIENT_MEMORY` is
a separate value from :attr:`Bound.AVAILABLE_MEMORY` precisely so that "the
machine affords exactly one" and "the machine affords none and got one" are two
readable situations rather than one. In the second, the work still runs and still
allocates the full per-worker cost, so R23 is unenforced there rather than
satisfied, and a caller that wants to refuse rather than proceed has the value it
needs to branch on.

Layer note: INFRASTRUCTURE. It reads the machine and builds processes, and it
names no verb, no feature module, and no taxonomy.
"""

from __future__ import annotations

import multiprocessing
import pickle
import sys
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import process as _process_pool
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable, Iterable, Mapping, TypeVar

#: The hard ceiling on workers for a pool whose children each hold a model.
#: Ported as the number it is: two is the count survival-tested on a real run of
#: the source system, and the default is the survival-tested number rather than
#: the aspirational one. A caller with a cheaper worker raises it explicitly,
#: which is a decision in a diff rather than a default nobody chose.
DEFAULT_WORKER_CEILING = 2

#: Bytes taken off the top of the reading before any percentage is applied.
#:
#: AN ABSOLUTE NUMBER, and it is the one brake here that does not shrink with the
#: reading. A percentage of a small reading is a small reserve, and that is
#: backwards: the operating system, this process, and whatever the user has open
#: need the same fixed room on a tight machine as on a roomy one, and the tight
#: machine is where getting it wrong kills the run. Two gibibytes is the working
#: set of a desktop with a browser and an editor open, measured rather than
#: guessed, on the machine this product is built on.
#:
#: SUBTRACTED BEFORE THE PERCENT, never instead of it. The reserve answers "how
#: much of this reading is not really mine", and the percent answers "how much of
#: what is left do I dare claim". Those are different questions and either one
#: alone leaves the other unanswered.
DEFAULT_MEMORY_RESERVE_BYTES = 2 * 1024**3

#: The share of what is left that a pool may claim, as an integer percent, on a
#: platform whose available reading is not dominated by a reclaim queue.
#:
#: An INTEGER PERCENT rather than a float factor, because the whole job of this
#: number is to be exact at a boundary and 0.8 is not representable in binary.
#: A float factor makes the boundary between two and three workers land on
#: whichever side the last bit of a rounding error fell, and the boundary is
#: precisely where a memory rule is tested and precisely where it fails.
GENERAL_HEADROOM_PERCENT = 75

#: The same share on darwin, where the reading is optimistic by a measured margin
#: rather than by a judgement.
#:
#: On the 18 gibibyte machine this product is built on, psutil computes darwin's
#: available as inactive plus free, and the split read 4.80 gibibytes inactive
#: against 0.28 free. Ninety one percent of the number was the inactive queue,
#: which includes dirty anonymous pages whose reclamation is a compression or a
#: write to swap rather than a free. Half is the share that survives that split
#: being as bad as it was measured to be. The number is recorded here with its
#: measurement rather than argued from first principles, so the next person to
#: doubt it knows exactly which observation to re-take.
DARWIN_HEADROOM_PERCENT = 50


def default_headroom_percent(platform: str = sys.platform) -> int:
    """The headroom share for one platform, defaulting to the running one.

    A FUNCTION rather than a conditional expression at module level, because a
    conditional expression has a branch that can only ever be executed on the
    other machine, and a branch no test can reach is a branch that is wrong the
    day somebody edits it. Taking the platform as an argument makes both answers
    checkable from here.
    """
    return DARWIN_HEADROOM_PERCENT if platform == "darwin" else GENERAL_HEADROOM_PERCENT


#: The share this machine gets, resolved once at import.
DEFAULT_HEADROOM_PERCENT = default_headroom_percent()

#: Swap already in use, above which no pool is planned at all.
#:
#: The one input that tells two identical available readings apart. A machine
#: reporting four and three quarter gibibytes available while sitting on two
#: gibibytes of swap has already been asked for more memory than it has, and the
#: kill this module exists to prevent happened on exactly that machine. The
#: threshold is a gibibyte rather than a single byte because darwin's swap use is
#: sticky: pages counted once stay counted after they are read back, so a machine
#: that was briefly busy last Tuesday would otherwise be refused a pool forever.
DEFAULT_SWAP_PRESSURE_BYTES = 1 * 1024**3

#: Physical memory in use, as a percent, above which no pool is planned at all.
#: Eighty five is the point where the platform is reclaiming to serve ordinary
#: allocations, so the next worker's model is paid for out of somebody else's
#: resident pages rather than out of room.
DEFAULT_USED_PERCENT_CEILING = 85

#: How many tasks one child may serve before it is retired. Bounding an allocator
#: that grows over a long run rather than merely observing it. Each retirement
#: pays for a fresh interpreter and a fresh model load, so this is high enough
#: that an ordinary folder retires a child once or twice rather than constantly.
#:
#: SPENT AS A GENERATION, not handed to the platform. See the module docstring:
#: the executor's own ``max_tasks_per_child`` deadlocks at exactly this default,
#: so :func:`map_workers` multiplies this by the worker count and gives one
#: executor that many items, then builds the next one.
DEFAULT_MAX_TASKS_PER_CHILD = 100

#: How long a probe may take before its answer is abandoned and the floor stands.
#: Generous, because a cold model load off a spinning disk is slow and a probe
#: that gives up early reports the floor for a machine that would have answered.
#: Finite, because the docstring on :func:`measure_worker_bytes` promises that
#: every failure returns the floor, and a loader that never returns is a failure
#: that was keeping that promise only by never being tested.
DEFAULT_PROBE_TIMEOUT_SECONDS = 120.0

#: How long a probe child is given to die once it is no longer wanted, at each of
#: the two escalations. Short, because by this point the answer is already in
#: hand or already abandoned.
_PROBE_REAP_SECONDS = 1.0

#: The two things a probe child can send back down its pipe. Tagged rather than
#: bare, so a refusal is a value the parent reads rather than a traceback the
#: child prints while the parent carries on as though nothing happened.
_PROBE_MEASURED = "measured"
_PROBE_FAILED = "failed"

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

    ``INSUFFICIENT_MEMORY`` is here because that argument was made and then not
    applied. A machine that affords exactly one worker and a machine that affords
    none both run the work in this process, and folding them together hides the
    second one exactly as thoroughly as folding an unreadable machine into a
    tight one would have. ``MEMORY_PRESSURE`` is separate for the same reason:
    the reading was fine and the machine was not.
    """

    AVAILABLE_MEMORY = "available_memory"
    INSUFFICIENT_MEMORY = "insufficient_memory"
    MEMORY_PRESSURE = "memory_pressure"
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

    A reading of available memory says how much room a new process could take. It
    says nothing about what taking it would cost, and those come apart exactly
    where this module has to be right: a machine two gibibytes into swap and an
    idle machine can report the same available bytes, and only one of them can
    carry a second copy of a model. These two numbers are the cheapest signal
    that tells them apart.
    """

    swap_used_bytes: int
    used_percent: float


@dataclass(frozen=True)
class PoolPlan:
    """The decided shape of one pool: how wide, why, over how much, and in what generations.

    ``in_process`` is a PROPERTY rather than a field, and that is load bearing. A
    stored flag can disagree with the count it was derived from, and the one
    place this arithmetic has an off-by-one is exactly there: a computed cap of
    one must run the work in the calling process, never start a pool of one. A
    pool of one is a whole second interpreter, a second copy of the model, and a
    pickle of every item and every result, to run the work strictly slower than
    doing it here. It is also the case a tight machine lands on, which is the
    machine that can least afford it.

    ``items`` is CARRIED rather than consumed and dropped, and it was the missing
    field that made a deadlock impossible to see from a plan. The dangerous ratio
    for any recycling pool is items against workers times tasks per child, and a
    plan that recorded two of those three numbers could not be checked by anybody
    holding it, including a test. It is on the plan so :attr:`generations` is a
    question the plan can answer about itself.
    """

    workers: int
    items: int
    bound: Bound
    worker_bytes: int
    available_bytes: int | None
    max_tasks_per_child: int | None

    @property
    def in_process(self) -> bool:
        """True when the work runs in the calling process and no pool is built."""
        return self.workers == 1

    @property
    def tasks_per_generation(self) -> int | None:
        """The most work one executor may be given, or None when it may have all of it.

        ``workers * max_tasks_per_child`` is not a comfort margin. It is the
        exact number of tasks one generation of children can serve before every
        one of them has spent its budget, and it is the line the platform's own
        recycle deadlocks one item past. See the module docstring.
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


#: Where the kernel publishes a container's own memory limit.
#:
#: A CONSTANT AND AN ARGUMENT, because a machine with no cgroups cannot execute
#: either branch of the reader below, and a branch no test can reach is a branch
#: that is wrong the day somebody edits it. Every test here points the reader at
#: a directory it wrote itself.
CGROUP_ROOT = Path("/sys/fs/cgroup")

#: Where the kernel publishes WHICH cgroup this process is actually in.
#:
#: A constant and an argument for the same reason as the root above, and it is
#: the file that makes the root usable. Reading the root's own limit answers
#: "what is capped at the top of this hierarchy", which is the right question
#: inside a cgroup namespaced container and the wrong one on a host: a systemd
#: unit with a memory cap lives at ``system.slice/something.service`` and the
#: root publishes no cap at all.
CGROUP_SELF = Path("/proc/self/cgroup")

#: A published limit at least this large is the kernel saying "no limit".
#:
#: Version one writes the largest page-aligned value it can rather than a
#: sentinel word, and that value has been two different numbers across kernel
#: versions, so the test here is "absurdly large" rather than equality with
#: either of them. Four exbibytes is far above any cap a machine could enforce
#: and below both of the numbers the kernel has used.
_CGROUP_UNLIMITED_ABOVE = 1 << 62


def _cgroup_text(path: Path) -> str | None:
    """One file the kernel publishes, as text, or None when it cannot be read.

    BROAD ON PURPOSE, AND THE BREADTH IS THE ARM THAT CARRIES THE WEIGHT. The
    file may not exist, this process may not be allowed to read it, and the path
    may be a directory rather than a file. Every one of those arrives as
    ``OSError`` and every one of them means the same thing here, which is that
    there is no reading. Narrowing this to ``FileNotFoundError`` while tidying
    would let a cgroup file with mode 000, or a path that resolved to a
    directory, raise out of :func:`available_bytes`, which is a public function
    that promises a number.
    """
    try:
        return path.read_text()
    except OSError:
        return None


def _cgroup_number(path: Path) -> int | None:
    """One byte count the kernel published, or None when there is not one there.

    Every way of not getting a number is the same answer. There may be no
    reading at all, for any of the reasons above, and version two writes the
    word ``max`` where a number would go on a group with no limit. Neither is a
    limit, and neither is a reason to invent one.
    """
    text = _cgroup_text(path)
    if text is None:
        return None
    try:
        # The strip is REDUNDANT and is kept as documentation rather than as a
        # guard: int() already tolerates surrounding whitespace and the trailing
        # newline the kernel writes, so removing it changes no answer and kills
        # no test. It says out loud that the file ends in a newline.
        value = int(text.strip())
    except ValueError:
        return None
    return value if value >= 0 else None


def _cgroup_self_paths(text: str | None) -> tuple[str, str]:
    """Where this process sits, as (unified path, memory controller path).

    ``/proc/self/cgroup`` is one line per hierarchy, each of them
    ``id:controllers:path``. Version two writes a single line whose controller
    field is EMPTY, and version one writes one line per hierarchy with the
    controller names comma separated, so the memory controller may share its
    line with others. A machine with no such file at all, which is every darwin
    machine this product is built on, sits at the root of both, which is what
    the empty strings mean.
    """
    unified = ""
    controller = ""
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

    A CAP ON AN ANCESTOR IS A CAP ON THIS PROCESS. Nesting is the ordinary shape
    on a host that is not a container: the slice publishes one number and the
    unit inside it publishes another, and a process in the unit is bound by
    both. Every level is read rather than only the deepest.

    ``..`` is dropped rather than followed. The only way it can appear here is a
    kernel writing something this function does not understand, and walking out
    of the mount to read whatever file is there is not a reading of this
    process's cgroup.
    """
    parts = [part for part in relative.split("/") if part and part != ".."]
    return [mount.joinpath(*parts[:depth]) for depth in range(len(parts), -1, -1)]


def _headroom_in(directory: Path, *, limit_file: str, used_file: str) -> int | None:
    """Room left in ONE cgroup directory, or None when it publishes no cap.

    A CAP WITH NO USAGE READING IS STILL A CAP. Version two publishes the limit
    and the current usage as two files, and a process that can read one but not
    the other still knows a ceiling it can never exceed. Reporting the limit
    there is not optimism, because it is certainly not smaller than the truth,
    and the machine's own reading is still taken as the other half of the
    minimum in :func:`available_bytes`.
    """
    limit = _cgroup_number(directory / limit_file)
    if limit is None or limit >= _CGROUP_UNLIMITED_ABOVE:
        return None
    used = _cgroup_number(directory / used_file)
    if used is None:
        return limit
    return max(0, limit - used)


def cgroup_memory_headroom_bytes(
    root: Path = CGROUP_ROOT, *, self_cgroup: Path = CGROUP_SELF
) -> int | None:
    """Room left inside this process's own memory cgroup, or None when uncapped.

    NONE MEANS NO CAP, and it also means no cap this process could read. Those
    are deliberately the same answer. A guess at a limit is a number that is too
    small on every machine that never had one, and narrowing every pool on every
    developer's laptop to fix a container nobody is running is what a fix that
    is too restrictive looks like from the inside.

    THIS PROCESS'S OWN CGROUP, NOT THE ROOT OF THE HIERARCHY, and the difference
    is a whole class of host. Inside a cgroup namespaced container, which is the
    ordinary Docker case, the process sits at ``/`` and the cap is published at
    the root, so reading the root is exactly right. On a host it is not: a
    systemd unit with ``MemoryMax=`` lives at ``system.slice/something.service``
    and the root publishes no cap at all, so a reader that looked only at the
    root would report NO LIMIT for a four gibibyte service on a five hundred
    gibibyte machine, the host's reading would stand, and every brake above
    would do its arithmetic on a number a hundred times the truth. So
    ``/proc/self/cgroup`` says where this process is, and the walk starts there.

    THE TIGHTEST CAP ON THE CHAIN IS THE ONE THAT BINDS. A cgroup nested inside
    another is held by both, and whichever is smaller is what runs out first.
    Taking the deepest cap instead would report a unit's own generous number
    while a tighter slice above it was the real ceiling, which is the same
    mistake as taking the host's number over the container's.
    """
    unified, controller = _cgroup_self_paths(_cgroup_text(self_cgroup))
    layouts = (
        (_cgroup_directories(root, unified), "memory.max", "memory.current"),
        (
            _cgroup_directories(root / "memory", controller),
            "memory.limit_in_bytes",
            "memory.usage_in_bytes",
        ),
    )
    found: list[int] = []
    for directories, limit_file, used_file in layouts:
        for directory in directories:
            headroom = _headroom_in(directory, limit_file=limit_file, used_file=used_file)
            if headroom is not None:
                found.append(headroom)
    return min(found) if found else None


def available_bytes(
    *, cgroup_root: Path = CGROUP_ROOT, cgroup_self: Path = CGROUP_SELF
) -> int:
    """Memory a new process could obtain right now, in bytes.

    AVAILABLE, never free. See the module docstring for why the two are not
    interchangeable and why this one is the right question.

    THE SMALLER OF TWO CEILINGS, because the machine imposes one and a container
    imposes the other and neither knows about the other. The platform reading is
    a HOST reading, and a cgroup's headroom says nothing about whether the host
    can actually serve it, so only the minimum is bounded by both. On a machine
    with no cgroup the second ceiling is absent and this returns exactly what it
    always returned.

    Both cgroup arguments are keyword-only and defaulted, so this is still the
    zero argument reader :data:`AvailableReader` describes. They exist because a
    machine with no cgroups cannot execute either branch of the reader below
    them, and a branch no test can reach is a branch that is wrong the day
    somebody edits it.

    psutil is imported lazily so a caller that injects its own reader, which
    every sizing test does, never loads the extension module at all.
    """
    import psutil

    reading = int(psutil.virtual_memory().available)
    capped = cgroup_memory_headroom_bytes(cgroup_root, self_cgroup=cgroup_self)
    return reading if capped is None else min(reading, capped)


def memory_pressure() -> Pressure:
    """What the machine is already paying, right now.

    Two numbers rather than one, because they fail in different directions. Swap
    in use says the machine has already been asked for more than it has, which is
    history a percentage cannot show. The used percent says it is being asked
    right now, which is a present tense the swap counter is slow to reach.

    psutil is imported lazily for the same reason as above: a caller that injects
    its own reading never loads the extension module.
    """
    import psutil

    return Pressure(
        swap_used_bytes=int(psutil.swap_memory().used),
        used_percent=float(psutil.virtual_memory().percent),
    )


#: A reading of what the machine is already paying. Injected by every sizing
#: test, so no test's answer depends on what this machine happens to be doing.
PressureReader = Callable[[], Pressure]


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


def _probe_entry(loader: Callable[[], object], writer: Any) -> None:
    """Run the caller's loader in this worker, then report what the worker costs.

    Module level and picklable because a spawned child has to import it by name.

    THE MODEL IS HELD ACROSS THE READING, and that single reference is the whole
    correctness of this function. An earlier version called the loader and threw
    the result away on the same line, which reads as "the object does not matter,
    the process does" and is wrong in the one direction that matters: the object
    is freed before the resident set is read, and darwin's allocator returns
    large blocks to the kernel immediately rather than retaining them. Measured
    on this machine, a loader returning 32, 96 or 112 mebibytes showed the whole
    allocation, and one returning 128 mebibytes or more showed a delta of about
    zero. The 300 megabyte model this module exists to size for measured one
    mebibyte. A probe that reads as a no-op for exactly the case it was built for
    is worse than no probe, because it reports the floor while looking measured.

    A LOADER THAT RAISES IS AN ANSWER, NOT AN ACCIDENT, so it is caught here and
    sent back as one rather than left to the child's default exception hook. A
    machine with no model installed is the ordinary case this module already
    promises to handle by returning the floor, and printing a traceback out of a
    worker while the parent quietly carries on is a run that looks broken and is
    not. The reason travels with the refusal, as text rather than as an object,
    because an exception raised by somebody else's loader is not guaranteed to
    survive a pickle and the reason is worth more than the type.
    """
    try:
        model = loader()
        try:
            measured = resident_bytes()
        finally:
            # Released before the answer is sent, so the child does not hold a
            # model for the length of a pipe write it does not need it for.
            del model
    except Exception as failure:
        writer.send((_PROBE_FAILED, f"{type(failure).__name__}: {failure}"))
    else:
        writer.send((_PROBE_MEASURED, measured))
    finally:
        writer.close()


def _reap(worker: Any) -> None:
    """Make sure one probe child is gone, escalating, and never leave it running.

    A probe that timed out is a probe whose child is still loading, and a child
    still loading is still allocating. Abandoning it would leave the very
    allocation this module refuses to allow on a machine that already said no.
    """
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

    A BARE PROCESS AND A PIPE rather than an executor, because the question this
    has to answer is "did the loader finish, or die, or neither", and a pool
    answers only the first two. The pipe distinguishes the other two for free: a
    child that dies closes the write end, so the parent wakes immediately and
    raises rather than waiting out a timeout it did not need, and a child that
    hangs writes nothing and the timeout is the only thing that can end it.
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
            raise TimeoutError(
                f"the probe loader did not finish within {timeout_seconds} seconds"
            )
        outcome, answer = reader.recv()
    finally:
        reader.close()
        _reap(worker)
    # THIS TAG CHECK IS REDUNDANT AND IS KEPT FOR ITS MESSAGE. A failure sends
    # back the reason as text, so ``int(answer)`` on the line below would raise
    # on it anyway and the caller would land on the floor either way: removing
    # this branch changes no answer and kills no test. What it buys is the
    # reason travelling into the exception instead of a ValueError about a
    # string nobody can trace back to a loader.
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

    ``floor_bytes`` is a FLOOR and not merely a fallback, and conflating the two
    is the quiet way this returns a number that is too small. A probe measures
    resident set at the moment loading finishes. A worker then decodes a track,
    runs inference, and builds results, all of which allocate, so the measurement
    is a lower bound on the working set rather than the working set. The caller
    declares what it knows a worker of its kind costs at work, and the
    measurement raises that number when the machine says the model is bigger than
    expected. It never lowers it.

    Every failure returns the floor, and A LOADER THAT NEVER RETURNS IS A
    FAILURE. A crash, a kill, a segmentation fault, an unpicklable loader and a
    raising loader all landed on the floor before ``timeout_seconds`` existed;
    a hang did not, and a hang is the failure that costs the whole run rather
    than one number. The timeout governs the probe this module runs. An injected
    ``runner`` is the caller's own code called synchronously, and nothing here
    can interrupt it, so a test that wants to exercise the timeout drives the
    real probe.
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

    ``worker_bytes`` has no default on purpose. A default per-worker cost is a
    guess about somebody else's model, and a guess that is too low is the whole
    failure this module exists to prevent. A caller that cannot measure declares
    what it knows.

    THE ORDER OF THE ARITHMETIC IS THE UNIT. The absolute reserve comes off the
    reading first, then the headroom scales what is left, and only then is the
    result divided into workers::

        affordable = (available - reserve) * percent // 100 // worker_bytes

    Every one of those three steps is in that position for a reason. Reserving
    after the percent reserves a share of a share and leaves the fixed costs
    underfunded on exactly the tight machine that cannot absorb the error.
    Reversing the last two, dividing into workers first and then scaling the
    count, gives a different answer at the boundaries and only at the boundaries:
    with 2900 mebibytes available, no reserve, and a 1024 mebibyte worker, this
    order affords two workers and the reversed order affords one. Both orders
    agree in the middle of the range, which is where a test not written to hunt
    for this happens to sit, and both read as "apply the headroom" to somebody
    skimming.

    A MACHINE ALREADY IN TROUBLE IS REFUSED A POOL BEFORE ANY OF THAT RUNS. The
    pressure reading is checked first because it answers a question the byte
    arithmetic cannot ask: not how much room there is, but what the machine is
    already paying to hold what it has. Those come apart precisely on the machine
    the documented kill happened on, which reported nearly five gibibytes
    available while sitting on more than two gibibytes of swap.

    A memory reading that cannot be taken falls back to ONE worker. It never
    falls back to a core count, a configured count, or the ceiling: every one of
    those can be larger than what the machine can carry, and a fallback that can
    be larger than the thing it is standing in for is not a fallback. A PRESSURE
    reading that cannot be taken is treated as no pressure, which is the opposite
    rule and is deliberate: the available reading already succeeded, three brakes
    still apply, and collapsing every plan to one worker because a secondary
    signal is unavailable on some platform would retire the feature to fix a
    machine nobody has described.

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
        )

    pressure = _read_pressure(read_pressure or memory_pressure)
    if pressure is not None and (
        pressure.swap_used_bytes >= swap_pressure_bytes
        or pressure.used_percent >= used_percent_ceiling
    ):
        return PoolPlan(
            workers=1,
            items=items,
            bound=Bound.MEMORY_PRESSURE,
            worker_bytes=worker_bytes,
            available_bytes=available,
            max_tasks_per_child=None,
        )

    budget = max(0, available - reserve_bytes)
    affordable = budget * headroom_percent // 100 // worker_bytes
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
    if bound is Bound.AVAILABLE_MEMORY and smallest == 0:
        # The count is the same one either way. The REASON is not, and that is
        # the whole point of separating them: "this machine affords exactly one"
        # is a plan working, and "this machine affords none and is getting one
        # anyway" is R23 unenforceable, reported rather than hidden.
        bound = Bound.INSUFFICIENT_MEMORY
    workers = max(1, smallest)
    return PoolPlan(
        workers=workers,
        items=items,
        bound=bound,
        worker_bytes=worker_bytes,
        available_bytes=available,
        # A plan that runs in the calling process has no child to retire, and
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


def _read_pressure(reader: PressureReader) -> Pressure | None:
    """What the machine is paying, or None when that could not be established.

    Held to the same standard as the available reading and for the same reason.
    A pressure reading that arrives as text, as a bare number, or with a swap
    figure that is negative is not a measurement, and treating it as one would
    let a broken reader decide the width of every pool on the machine.
    """
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

    Refuses a plan of one worker rather than building a pool of one. The refusal
    is the point: a caller that reaches here with an in-process plan has skipped
    the branch that was supposed to keep the work in this process, and failing
    loudly at the seam is how that is caught in the unit that introduced it.

    The spawn context is not a preference. Sizing above assumes a child shares
    nothing with its parent, which is true under spawn and false under fork, so
    the arithmetic depends on this one argument being here.

    ``max_tasks_per_child`` IS DELIBERATELY ABSENT, and its absence is the fix
    for a deadlock rather than an omission. Handing the executor its own recycle
    counter is what hangs a run at this module's own defaults, for the reason the
    module docstring sets out, and this function is a public seam: a caller that
    built an executor from what it returns would inherit the hang. The recycle
    still happens. It happens at the generation boundary :func:`map_workers`
    enforces, and :attr:`PoolPlan.tasks_per_generation` is where the plan's
    per-child budget is actually spent.
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
    """Refuse now what a wider machine would refuse later, and a tight one never would.

    Without this, the SAME call has two different contracts depending on how much
    memory the machine had at the moment it ran. A plan of one worker calls the
    function here, where a closure or a lambda is perfectly ordinary; a plan of
    two pickles it to a child, where neither can go. A caller that developed
    against a busy laptop and shipped to a quiet server would find out from an
    AttributeError about a local object, at the far end of a run, on the machine
    it had never failed on.

    So the stricter of the two contracts is the only contract. It is checked on
    both paths, before either one runs, and the cost is one pickle of a function
    reference.

    THE INITIALIZER'S ARGUMENTS ARE HELD TO IT TOO, and leaving them out was the
    same defect one argument over. A plan of one worker calls the initializer
    here with whatever it was handed and a plan of two pickles those values to a
    child, so a closure passed as an initializer argument was still a call that
    meant two different things on two different machines. A value that cannot be
    sent to a child is refused wherever it appears rather than only where it was
    first noticed.
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

    THE WORK IS RUN IN GENERATIONS, and the size of a generation is the fix for a
    deadlock rather than a tuning choice. One executor is given at most
    ``workers * max_tasks_per_child`` items, which is exactly what one generation
    of children can serve, and then it is shut down and the next one is built.
    See the module docstring for what happens one item past that line when the
    platform's own recycle counter is used instead. Each boundary costs a fresh
    interpreter and a fresh model load per worker, which is the same cost the
    recycle was always going to pay, spent in one place rather than per child.

    THIS IS ALL OR NOTHING, AND THE EXCEPTION YOU SEE DEPENDS ON INPUT ORDER.
    One item that raises discards every result that completed, including results
    from earlier generations that finished successfully, and the exception that
    surfaces is the first in ITEM order rather than the first to be raised. Six
    items where the third raises return nothing, not five results and one error.
    That is the ordinary contract of a mapped executor and it is recorded here
    because it is invisible from the call site: a caller that wants the successes
    of a partial run needs per-item isolation this function does not provide, and
    U25 is the unit that will find out whether it needs it.

    Exists so that "a cap of one skips the pool" is true by construction rather
    than by every caller remembering. A call site that builds its own executor
    keeps its own copy of that branch, and the copies drift.
    """
    _refuse_what_no_child_could_receive(function, "function")
    if initializer is not None:
        _refuse_what_no_child_could_receive(initializer, "initializer")
    # THE ARGUMENTS ARE HELD TO THE RULE EVEN WITH NO INITIALIZER TO RECEIVE
    # THEM, which is over strict by a hair and is the deliberate choice. The
    # ordinary empty tuple is not refused by it at all, so what it costs is a
    # caller who passed arguments that will never be called with them, and what
    # it buys is one rule rather than a rule that changes with a second
    # argument. It is the same on both paths, which is the property this whole
    # function exists for.
    for position, argument in enumerate(initargs):
        _refuse_what_no_child_could_receive(argument, f"initializer argument {position}")
    ordered = list(items)
    if plan.in_process:
        if initializer is not None:
            initializer(*initargs)
        return [function(item) for item in ordered]
    generation = plan.tasks_per_generation or len(ordered) or 1
    results: list[_Result] = []
    for start in range(0, len(ordered), generation):
        # Named ``executor`` rather than ``pool``, which is this module's own name
        # and is the shape of the naming collision this repository keeps
        # recording: one word meaning two things, here inside one file.
        with ProcessPoolExecutor(
            **executor_arguments(plan, initializer=initializer, initargs=initargs)
        ) as executor:
            results.extend(executor.map(function, ordered[start : start + generation]))
    return results


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
    "PoolPlan",
    "Pressure",
    "PressureReader",
    "ProbeRunner",
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
]
