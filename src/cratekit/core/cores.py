"""How many cores this process may run on: a ceiling for a pool, never its size.

The one place a core count is read (U241). ``cratekit.core.pool`` sizes a pool
from memory alone; the count here is only the planner's ``ceiling``, the number
of workers worth starting. A ceiling can only lower a plan, so a wrong count
costs speed, never memory. Unknown is one worker. A container's processor
quota is not read, so such a process sees the host's width.

Layer: infrastructure.
"""

from __future__ import annotations

import os
from typing import Callable

#: A reading of how many cores this process may run on, or None; tests inject one.
CoreReader = Callable[[], "int | None"]


def usable_cores() -> int | None:
    """The cores this process may be scheduled on, or None when nothing will say.

    The process's affinity where published, else the machine's count. An empty
    set, a zero or a refusal falls through to the next reading.
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

    ``reserved`` has no default: what else runs is the caller's knowledge. A
    reading that fails or is not a count is one worker. ``read`` None is
    :func:`usable_cores`, looked up at call time so a test can replace it.
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
