"""What the two adoption verbs share, so a rule has one owner rather than two.

``crate adopt scan`` and ``crate adopt apply`` differ in what an item is, in what
they write, and in whether a gate stands in front of them. They do NOT differ in
how a queued job is resumed, in what a job with no items means, or in the shape
of the payload they report, and until this module existed each of those was
written out twice.

**THE RESUME IS THE ONE THAT MATTERED.** It carries the R-225 fix: a job that did
not finish must exit with its own cause rather than through a normal envelope,
because a person whose adoption wrote nothing must not be told it finished. Two
copies of a fix is one copy that gets updated, which is the argument
:mod:`cratekit.modules.outbound.shell` already makes for the two outbound verbs.
That module is not reached across for: its resume digests the outbound payload
keys and answers an outbound gate, so sharing it would mean widening a function
that is correct as it is.

**THE PREDICATE IS "CLOSED AND CARRYING A CAUSE", NOT "FAILED".** A run stopped
with a signal is CANCELLED and carries the cause :func:`cratekit.core.jobs.cancel`
builds, so the narrower predicate reports an interrupted adoption through a normal
envelope and exits 0. Measured on the two outbound verbs on 2026-09-02 as exit 0
over a job with none of its items done. SUCCEEDED carries no cause, so it is
unaffected.

**WHAT IS DELIBERATELY NOT HERE.** Each verb's summary stays its own, because a
census reports category and disposition counts and an apply reports what it
placed, and one function over both would branch on which verb called it. The gate
stays with the verb that declares one. Both are passed in or done outside rather
than merged.

``ctx`` is untyped here for the reason every builder in this package takes an
untyped ``entry`` (KTD23): this is modules-ranked and :mod:`cratekit.cli` is above
it, so naming that type would be reaching upward.

Layer: modules.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from cratekit.core import jobs
from cratekit.core.cause import refuse
from cratekit.core.exit_codes import Remedy


def reported(store, job, extra: Mapping[str, Any] | None = None) -> dict:
    """One job as the ``job_state`` payload both verbs emit.

    ``extra`` rides UNDER ``progress``, never beside it. The registry declares
    both verbs as ``job_state/1`` and ``cli.output`` closes that surface with
    ``additionalProperties: false``, so a top level key is an undeclared field and
    a consumer generated from the committed schema rejects every envelope these
    verbs emit. ``progress`` is declared ``object`` with no inner constraint,
    which is where a per verb detail belongs. U51 paid for that distinction on the
    two outbound verbs.
    """
    progress = dict(jobs.progress(store, job.job_id))
    if extra:
        progress.update(extra)
    return {
        "job_id": job.job_id,
        "state": str(job.state),
        "cause": job.cause.to_json() if job.cause is not None else None,
        "progress": progress,
    }


def no_op(state: str) -> dict:
    """The ``job_state`` payload for a run that correctly queued nothing.

    ``job_id`` IS THE EMPTY STRING RATHER THAN ``None``. ``cli.output`` requires
    every field of the declared surface and types this one as a string, so a null
    fails the verb's own schema. ``adopt.apply`` shipped that defect and it was
    recorded as R-234; spelling the payload once here is what stops the three
    zero paths these two verbs now have from each reintroducing it separately.
    """
    return {"job_id": "", "state": state, "cause": None, "progress": {}}


def advance(ctx, store, job, *, origin: Sequence[str], nothing_to_run: str):
    """Reconcile, refuse an empty job, drive it, and raise if it did not finish.

    NOT CALLED ``drive``, and the name is load bearing rather than a preference.
    ``tests/test_handlers.py`` asserts that exactly one place in the package calls
    the job driver, and it counts every ``ast.Call`` whose callee is NAMED
    ``drive``. A function of that name here would read as a second caller of
    :func:`cratekit.core.jobs.drive` to a guard that cannot see the difference,
    which is one symbol meaning two things arriving through the module that exists
    to stop exactly that.

    RECONCILE FIRST. A resume arrives after something stopped, and a claim left
    behind by a driver that died is state the queue cannot see for itself.

    A JOB WITH NO ITEMS IS REFUSED RATHER THAN DRIVEN. ``core.jobs`` treats
    attempting nothing as a genuine no-op so an up-to-date source does not look
    broken, so a job frozen by a build that recorded no items would drive straight
    to SUCCEEDED over work it never did. Neither verb can queue one now;
    ``nothing_to_run`` is what a person is told about one queued by an older
    build.

    Returns the job as it stands after the drive, and the warnings the driver
    produced. Raises rather than returning when the job closed carrying a cause.
    """
    job = jobs.reconcile(store, job.job_id)
    warnings: tuple[dict[str, str], ...] = ()
    if job.is_open():
        if not jobs.items(store, job.job_id):
            raise refuse(
                "internal-error",
                f"job {job.job_id} has no items to run, so driving it would "
                f"{nothing_to_run}. It was queued by a build that did not record "
                f"what its items were",
                remedy=Remedy.REPORT_DEFECT,
                origin=tuple(origin),
                detail={"job_id": job.job_id},
            )
        _result, warnings = ctx.run_job(store, job)
        job = jobs.get(store, job.job_id)
    jobs.raise_for_state(job)
    return job, warnings


__all__ = ["advance", "no_op", "reported"]
