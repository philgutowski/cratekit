"""How many cores this process may run on: a ceiling for a pool, never its size.

THE ONE PLACE A CORE COUNT IS READ (U241). ``cratekit.core.pool`` decides how
many workers a machine can CARRY, from memory, and reads no core count at
all, because the source system sized its pool as the cores less two and was
killed on a machine whose memory could not hold that many workers. That rule
stands. What this module answers is a different question, how many workers
are worth STARTING: past the number of cores a further worker only waits its
turn. So the count read here is handed to the planner as its ``ceiling``
argument and to nothing else, and the planner's own arithmetic, the reserve,
the headroom, the swap and used percent gates, still decides underneath it.

A CEILING CAN ONLY LOWER A PLAN. ``plan_pool`` takes the smallest of what
memory affords, the ceiling and the item count, so a core count that is wrong
high costs nothing memory did not already allow, and one that is wrong low
costs speed. That asymmetry is why reading it is safe here and was not safe
as the source system used it.

NOT KNOWING IS ONE WORKER. A platform that will not say how many cores it
has gets a ceiling of one, the answer the planner gives for a memory reading
it could not take.

WHAT THIS CANNOT SEE. A container's processor quota is a share of time
rather than a set of cores, and nothing here reads it, so a process held to
two cores' worth of time on a wide host is told the host's width. The cost is
workers taking turns, never memory, since the planner reads the container's
memory limit itself.

Layer note: INFRASTRUCTURE. It names no verb and no feature module.
"""

from __future__ import annotations

import os
from typing import Callable

#: A reading of how many cores this process may run on, or None for unknown.
#: Injected by every test, so no test's answer depends on the machine it runs on.
CoreReader = Callable[[], "int | None"]


def usable_cores() -> int | None:
    """The cores this process may be scheduled on, or None when nothing will say.

    The process's own allowance where the platform publishes one, a
    ``taskset`` or a cpuset on Linux, and the machine's count otherwise. Each
    reading is checked rather than trusted: an empty set, a zero and a refusal
    all fall through to the next, and to None at the end.
    """
    affinity = getattr(os, "sched_getaffinity", None)
    if affinity is not None:
        try:
            allowed = len(affinity(0))
        except OSError:
            allowed = 0
        if allowed > 0:
            return allowed
    for name in ("process_cpu_count", "cpu_count"):
        reader = getattr(os, name, None)
        if reader is None:
            continue
        count = reader()
        if isinstance(count, int) and not isinstance(count, bool) and count > 0:
            return count
    return None


def worker_ceiling(*, reserved: int, read: CoreReader | None = None) -> int:
    """The most workers worth starting: the cores less ``reserved``, never under one.

    ``reserved`` is how many cores the caller keeps for work that is not the
    pool's, the process driving it above all, and has no default, because how
    much else is running is the caller's knowledge. A reading that cannot be
    taken, or is not a count, is one worker. ``read`` None is
    :func:`usable_cores`, looked up when called so a test can stand in for it.
    """
    if isinstance(reserved, bool) or not isinstance(reserved, int) or reserved < 0:
        raise ValueError("reserved must be a count of cores, so a whole number never negative")
    try:
        cores = (read or usable_cores)()
    except Exception:
        return 1
    if isinstance(cores, bool) or not isinstance(cores, int) or cores < 1:
        return 1
    return max(1, cores - reserved)


__all__ = ["CoreReader", "usable_cores", "worker_ceiling"]
