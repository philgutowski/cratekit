"""How a queued adoption job is resumed and reported, under its older names.

``adopt.move_cli`` and ``organize`` import these; each has one home since U298,
:func:`cratekit.core.jobs.advance`, :func:`cratekit.core.jobs.reported` and
:func:`cratekit.cli.output.no_job`, which the scan and apply verbs call directly.

Layer: modules.
"""

from __future__ import annotations

from cratekit.cli.output import no_job as no_op
from cratekit.core.jobs import advance, reported

__all__ = ["advance", "no_op", "reported"]
