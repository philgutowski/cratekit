"""Heavy DSP: tempo, drift, energy, and vocals, sized by memory not cores.

Both passes plan through ``cratekit.core.pool.plan_pool`` and run through its
workers; neither may invent a worker count. ``crate analyze run`` is a job and
measures its heads ahead through ``analysis.ahead`` (U241) rather than the
batch below. A vocal model that fails to load degrades to vocal inactive and
keeps tempo, drift and energy. No key is measured (U343), since a head's key
comes from rekordbox through ``analyze adopt``. Tempo is computed, never written as a grid, a BPM
tag or an AverageBpm field. The detectors import the extra lazily, so a slim
install imports this package.
"""

from cratekit.analysis.run import Result, run_batch

__all__ = ["Result", "run_batch"]
