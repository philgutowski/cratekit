"""What the two tagging verbs share, so a rule has one owner rather than two.

``crate tag folder`` and ``crate tag retag`` disagree about what an item is, about
where the answer comes from, and about whether a person has to confirm anything
first. They agree completely about the three things here: how a queued job is
resumed, what a job with no items means, and what shape the payload they report
takes. Written twice, those three drift, and the one that drifts is whichever
verb the next change does not touch.

**THE RESUME IS WHY THIS MODULE IS WORTH ITS OWN FILE.** It carries the R-225
rule, that a job which did not finish must leave through its own cause rather
than through a normal envelope. A person whose folder was half tagged must not be
told the sweep succeeded, and the only place that can be enforced is the one
function both resumes go through.

**THE PREDICATE IS "CLOSED AND CARRYING A CAUSE", NOT "FAILED".** A run stopped
with a signal closes as CANCELLED, not FAILED, and it carries the cause
:func:`cratekit.core.jobs.cancel` builds. So a predicate that asks about FAILED
hands an interrupted sweep back as a payload and the dispatcher exits 0 over it.
SUCCEEDED carries no cause at all, which is what keeps the wider predicate from
catching the case it must not catch.

**THIS IS THE THIRD COPY, AND THAT IS RECORDED RATHER THAN HIDDEN** (KTD9x).
:mod:`cratekit.adopt.shell` and :mod:`cratekit.modules.outbound.shell` are the
first two. Reaching into ``adopt`` from here would put an adoption name on a
tagging rule, and the honest home, one module in ``core`` taking the differences
as arguments, is another unit's files. The residual sits beside R-240.

**WHAT IS DELIBERATELY NOT HERE.** Each verb's own summary of what it did, and
the gate ``tag retag`` answers. A summary function over both verbs would branch
on which one called it, which is a shared function that is really two functions
sharing a name.

``ctx`` is untyped, for the reason every builder in this package takes an untyped
``entry`` (KTD23): this is modules-ranked and :mod:`cratekit.cli` is above it, so
naming that type would be reaching upward and ``tests/test_layering.py`` refuses
it.

Layer: modules.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from cratekit.core import jobs
from cratekit.core.cause import refuse
from cratekit.core.exit_codes import Remedy


def reported(store, job, extra: Mapping[str, Any] | None = None) -> dict:
    """One job as the ``job_state`` payload both tagging verbs emit.

    ``extra`` RIDES UNDER ``progress``, NEVER BESIDE IT. Both verbs declare
    ``output_schema="job_state/1"`` in :mod:`cratekit.cli.registry`, and
    ``cli.output`` closes that surface with ``additionalProperties: false``, so a
    per verb detail placed at the top level is an undeclared field and a consumer
    generated from the committed schema rejects every envelope these verbs send.
    ``progress`` is declared as an object with no inner constraint, which is
    exactly where a detail that varies by verb belongs. U51 paid for that
    distinction on two outbound verbs and its suite stayed green while it did.
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
    fails the verb's own schema, and a folder with nothing to tag is a common
    enough outcome that the failure would be reached often. That defect shipped
    once as R-234. Spelling the payload here is what stops each of the zero paths
    the two tagging verbs have from reintroducing it separately, since a folder
    holding no audio files, a retag with an empty selection, and a declined gate
    are three different places one person could get it wrong.
    """
    return {"job_id": "", "state": state, "cause": None, "progress": {}}


def advance(ctx, store, job, *, origin: Sequence[str], nothing_to_run: str):
    """Reconcile, refuse an empty job, drive it, and raise if it did not finish.

    NOT CALLED ``drive``, and the name is load bearing rather than a preference.
    ``tests/test_handlers.py`` asserts that exactly one place in the package calls
    the job driver, and it counts every ``ast.Call`` whose callee is NAMED
    ``drive``. A function of that name here would read to that guard as a second
    caller of :func:`cratekit.core.jobs.drive`, so the guard would fail in a file
    that has nothing to do with tagging and the next author would have to work out
    why.

    RECONCILE FIRST. A resume arrives after something stopped, and a claim left
    behind by a driver that was killed is state the queue cannot see for itself.

    A JOB WITH NO ITEMS IS REFUSED RATHER THAN DRIVEN. ``core.jobs`` treats
    attempting nothing as a genuine no-op, so that an up-to-date source does not
    look broken, which means a job frozen by a build that recorded no items would
    drive straight to SUCCEEDED over work it never did. Neither tagging verb can
    queue one now; ``nothing_to_run`` is what a person is told about one queued by
    an older build.

    Returns the job as it stands after the drive, along with the warnings the
    driver produced. Raises rather than returning when the job closed carrying a
    cause.
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
