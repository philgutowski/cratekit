"""What the two adoption verbs share: how a queued job is resumed and reported.

The names its package imports them by, each with one home since U298:
:func:`cratekit.core.jobs.advance`, :func:`cratekit.core.jobs.reported` and
:func:`cratekit.cli.output.no_job`. Each verb's summary and gate stay its own.

Layer: modules.
"""

from __future__ import annotations

from cratekit.cli.output import no_job as no_op
from cratekit.core.jobs import advance, reported

__all__ = ["advance", "no_op", "reported"]
