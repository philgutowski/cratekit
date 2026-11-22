"""What the two tagging verbs share: how a queued job is resumed and reported.

``crate tag folder`` and ``crate tag retag`` disagree about what an item is,
about where the answer comes from and about whether a person has to confirm
anything first. They agree about how a queued job is resumed, what a job with
no items means, and what shape the payload they report takes. Those three have
one home each since U298, :func:`cratekit.core.jobs.advance`,
:func:`cratekit.core.jobs.reported` and :func:`cratekit.cli.output.no_job`,
and this module keeps the names its package imports them by.

Each verb's own summary of what it did, and the gate ``tag retag`` answers,
are deliberately not here.

Layer: modules.
"""

from __future__ import annotations

from cratekit.cli.output import no_job as no_op
from cratekit.core.jobs import advance, reported

__all__ = ["advance", "no_op", "reported"]
