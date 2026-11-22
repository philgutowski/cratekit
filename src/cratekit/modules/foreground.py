"""A queued verb run by hand drives its own job before it returns.

``crate tag folder``, ``crate analyze run`` and ``crate analyze restamp`` run
their own ``--job`` path in this process on the job they just queued, and
answer with the settled job. A verb hands :func:`settle` the function its
``--job`` path already calls, so the reconcile, the drive and the mapping of
how the job ended stay written once, in the verb.

AN INTERRUPT LEAVES THE JOB QUEUED, AND SAYS THE COMMAND. The engine records a
signalled run as CANCELLED, which is closed, so the job is re-armed with
:func:`cratekit.core.jobs.retry` (items that settled stay settled) and the
refusal carries the ``--job`` command that finishes it in the foreground.

``--queue-only`` keeps the queue and return answer for a caller that drives the
job itself, as ``crate sync land`` does. It is mutually exclusive with
``--job``, since a resume queues nothing.

Layer: modules. Below it a command is a token the CLI renders (D2), and only
the verb that queued the job can build its exact ``--job`` command.
"""

from __future__ import annotations

import dataclasses
import shlex
from collections.abc import Callable, Sequence
from typing import TypeVar

from cratekit.core import jobs
from cratekit.core.cause import JobCancelled, rebuilt

#: The flag, spelled once for the three builders and for ``sync land``.
QUEUE_ONLY = "--queue-only"

_T = TypeVar("_T")


def add_job_options(parser, *, what: str) -> None:
    """Declare ``--job`` and ``--queue-only`` on a queueing verb, one or the other.

    ``what`` names the work in the help text, "tagging" or "restamp". The
    ``--job`` dest stays ``job``, which every resume already reads.
    """
    chosen = parser.add_mutually_exclusive_group()
    chosen.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help=f"continue the {what} job already queued under this identifier",
    )
    chosen.add_argument(
        QUEUE_ONLY,
        action="store_true",
        dest="queue_only",
        help=(
            f"queue the {what} job and return without driving it, printing the "
            f"--job command that drives it; for a caller that drives the job itself"
        ),
    )


def queue_only(args) -> bool:
    """Whether this invocation asked to queue and return."""
    return bool(getattr(args, "queue_only", False))


def settle(
    job_id: str,
    settled: Callable[[], _T],
    *,
    argv: Sequence[str],
    origin: str,
) -> _T:
    """Run the verb's ``--job`` path on the job it just queued; re-arm it if interrupted.

    ``settled`` is that path, closed over the job identifier; ``argv`` is the
    command line that resumes the job, named on the refusal when the drive is
    interrupted. Every other ending leaves exactly as the ``--job`` path does.
    """
    try:
        return settled()
    except JobCancelled as exc:
        raise _resumable(exc, job_id, argv, origin) from exc


def _resumable(exc: JobCancelled, job_id: str, argv: Sequence[str], origin: str) -> Exception:
    """The cancelled refusal, with the job queued again and its command first."""
    # No state check before ``retry``: it re-arms a cancelled job and hands an
    # open one back untouched.
    with jobs.open_store() as store:
        job = jobs.retry(store, job_id)
        progress = jobs.progress(store, job_id)
    command = shlex.join(["crate", *argv])
    cause = exc.cause
    steps = (
        f"resume it with: {command}",
        f"the job is queued again with {progress['settled']} of {progress['total']} "
        f"items settled, and the resume does not redo them",
    )
    # THE TOKEN IS DROPPED: it renders as ``crate job resume <id>``, which spawns
    # a detached worker where the person asked for the foreground.
    remediation = dataclasses.replace(cause.remediation, remedy=None, steps=steps)
    detail = {**cause.detail, "job_id": job_id, "state": str(job.state), "resume": list(argv)}
    return rebuilt(
        exc,
        dataclasses.replace(cause, remediation=remediation, detail=detail).at(origin),
    )
