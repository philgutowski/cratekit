"""A queued verb run by hand drives its own job before it returns (U192).

``crate tag folder``, ``crate analyze run`` and ``crate analyze restamp`` queued
a job and returned, printing the ``--job`` command that drives it, so every step
of a tail was two commands with an identifier copied between them. Each now
runs its own ``--job`` path in this process on the job it just queued, and
answers with the settled job.

THE DRIVE IS THE VERB'S OWN RESUME, NOT A SECOND ONE. A verb hands
:func:`settle` the function its ``--job`` path already calls, so the
reconcile, the empty job refusal, the drive and the mapping of how the job
ended stay written once, in the verb. This module owns only what is new: the
flag that keeps the old behaviour, and what an interrupt leaves behind.

AN INTERRUPT LEAVES THE JOB QUEUED, AND SAYS THE COMMAND. The engine records a
run stopped by a signal as CANCELLED, which is closed, and a closed job's
``--job`` command reports it rather than driving it. So the job is re-armed
with :func:`cratekit.core.jobs.retry`, the step ``crate job resume`` takes
before it spawns its worker, and the cancelled refusal leaves carrying the
``--job`` command that finishes it in the foreground. Items that settled stay
settled: ``retry`` re-arms only what is pending, claimed or failed.

``--queue-only`` KEEPS TODAY'S ANSWER, for a caller that drives the job itself.
``crate sync land`` is that caller: it queues each tail step and settles it
through the ``--job`` command, so the pass reports one command per step and no
job is driven twice. The flag shares a mutually exclusive group with ``--job``,
because a resume queues nothing and the flag would mean nothing there.

Layer: modules. Below it a command is a token the CLI renders (D2), and this
module names the exact `--job` command a person resumes with, which only the
verb that queued the job can build.
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

    ``settled`` is that path, closed over the job identifier. ``argv`` is the
    command line that resumes the job, the one the verb's ``argv_builder``
    returns, named on the refusal when the drive is interrupted. Every other
    ending, blocked, failed or succeeded, leaves exactly as the ``--job`` path
    leaves it.
    """
    try:
        return settled()
    except JobCancelled as exc:
        raise _resumable(exc, job_id, argv, origin) from exc


def _resumable(
    exc: JobCancelled, job_id: str, argv: Sequence[str], origin: str
) -> Exception:
    """The cancelled refusal, with the job queued again and its command first."""
    with jobs.open_store() as store:
        job = jobs.get(store, job_id)
        if job.state is jobs.JobState.CANCELLED:
            job = jobs.retry(store, job_id)
        progress = jobs.progress(store, job_id)
    command = shlex.join(["crate", *argv])
    cause = exc.cause
    steps = (
        f"resume it with: {command}",
        f"the job is queued again with {progress['settled']} of {progress['total']} "
        f"items settled, and the resume does not redo them",
    )
    # THE TOKEN IS DROPPED, NOT KEPT BESIDE THE STEPS. It renders as ``crate job
    # resume <id>`` on the fix line, ahead of the steps, and that command spawns
    # a detached worker where the person asked for the foreground.
    remediation = dataclasses.replace(cause.remediation, remedy=None, steps=steps)
    detail = {**cause.detail, "job_id": job_id, "state": str(job.state), "resume": list(argv)}
    return rebuilt(
        exc,
        dataclasses.replace(cause, remediation=remediation, detail=detail).at(origin),
    )


__all__ = ["QUEUE_ONLY", "add_job_options", "queue_only", "settle"]
