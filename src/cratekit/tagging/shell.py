"""The names the tagging verbs import the shared resume shell by.

How a queued job is resumed and reported, and the payload of a run that
queued nothing, have one home each since U298:
:func:`cratekit.core.jobs.advance`, :func:`cratekit.core.jobs.reported` and
:func:`cratekit.cli.output.no_job`.

Layer: modules.
"""

from __future__ import annotations

from cratekit.cli.output import no_job as no_op
from cratekit.core.jobs import advance, reported

__all__ = ["advance", "no_op", "reported"]
