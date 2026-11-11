"""Heavy DSP: key, tempo, energy, and vocals, sized by memory not cores.

U12 shipped the pool. This package is the first work that uses it. Both
passes plan through cratekit.core.pool.plan_pool and run through
cratekit.core.pool.map_workers. Neither pass may invent a worker count.

``crate analyze run`` is a job and settles one file at a time, so it does not
run the batch below: its driver scores vocals and writes, and the light heads
are measured ahead of it through the pool's work stream, ``analysis.ahead``
(U241). The light pass's ceiling comes from the cores, as a ceiling handed to
the planner; memory still decides the count.

The two-pass split is the source system's, kept because it already works:
a wide librosa-only head, then a capped vocal finalize. A vocal model that
fails to load degrades to vocal-inactive and still returns key, tempo, and
energy. Tempo is computed. It is never written as a grid, a BPM tag, or an
AverageBpm field.

The extras group is the slim-install gate. Importing this package on a
machine without librosa is allowed for the CLI stub; the detectors import
the extra lazily inside the functions that need it.
"""

from cratekit.analysis.run import Result, run_batch

__all__ = ["Result", "run_batch"]
