"""What the two adoption verbs share: how a queued job is resumed and reported.

``crate adopt scan`` and ``crate adopt apply`` differ in what an item is, in
what they write and in whether a gate stands in front of them. They do not
differ in how a queued job is resumed, in what a job with no items means, or in
the shape of the payload they report. Those three were written here, again in
``tagging.shell`` and again in the verbs that queue a job, until U298 gave each
one home: :func:`cratekit.core.jobs.advance`, :func:`cratekit.core.jobs.reported`
and :func:`cratekit.cli.output.no_job`. This module keeps the names its package
imports them by.

Each verb's summary stays its own, and the gate stays with the verb that
declares one.

Layer: modules.
"""

from __future__ import annotations

from cratekit.cli.output import no_job as no_op
from cratekit.core.jobs import advance, reported

__all__ = ["advance", "no_op", "reported"]
