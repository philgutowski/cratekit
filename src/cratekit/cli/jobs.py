"""The four job verbs, and the one place a handler key becomes a command line.

The engine below deliberately knows no verb: KTD23 puts verb strings in this
layer, and KTD26 needs the engine to re-invoke the product without importing the
module that does the work. Both are satisfied by the same seam. A job stores a
HANDLER KEY, this file resolves that key against the registry, imports the owning
module only at the moment it is actually needed, and hands the assembled argument
list back to the engine to spawn.

Resolving the key does not import anything, which is the property the conformance
suite asserts directly: the engine validates a queued job's handler before it
spawns, and validating by import would pull every feature module into the
supervising process and walk straight around the lazy-import stubs.

Two smaller decisions worth stating.

**Reporting a job never fails because the job failed.** ``job show`` on a broken
job exits 0 and carries the job's cause in its PAYLOAD, where ``job_state``
already reserves a field for it. Making the verb's status mirror the job's status
would leave a caller unable to tell "this job failed" from "I could not read this
job", which is the same collapse KTD25 is about, one level up.

**Resuming reconciles first.** A row that still says running while nobody holds
the job's lock describes a driver that was killed, and believing that row would
either refuse a resume forever or double-drive a job whose lock is genuinely
held. Disk truth is the lock, not the row.
"""

from __future__ import annotations

import argparse
import importlib
from typing import TYPE_CHECKING, Any, Sequence

from cratekit.cli import handlers, registry
from cratekit.cli.output import Envelope
from cratekit.core import config, jobs
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation
from cratekit.core.exit_codes import ExitCode, Remedy

if TYPE_CHECKING:  # pragma: no cover - typing only, and a cycle if imported for real
    from cratekit.cli import Context

#: What a listing puts in the payload's single-job field. ``job_state`` is a
#: per-job surface and a listing is not about one job, so the field is empty
#: rather than carrying the first row's identifier, which a consumer would
#: reasonably read as "this envelope describes that job".
NO_SINGLE_JOB = ""


def _summary(store: jobs.JobStore, job: jobs.Job) -> dict[str, Any]:
    """One job flattened for the payload, progress and worker state included.

    ``worker`` is the honest half of an unfinished cutover. Most queued verbs
    still have no function behind their handler key, so their jobs sit for ever
    while reporting cleanly. Before anything was bound that was at least uniform,
    and a person could learn that queues do not run; with one verb working and the
    rest silent the same report invites the opposite conclusion. The question is
    answered from the declaration tables alone, which is what keeps a listing from
    importing every feature module (KTD26).
    """
    unbound = handlers.unbound_reason(job.handler_key)
    return {
        "job_id": job.job_id,
        "handler": job.handler_key,
        "worker": "bound" if handlers.is_known(job.handler_key) else "none",
        "worker_reason": unbound,
        "state": str(job.state),
        "stage": job.stage,
        "attempts": job.attempts,
        "created": job.created,
        "updated": job.updated,
        "library_id": job.library_id,
        "progress": jobs.progress(store, job.job_id),
        "cause": job.cause.to_json() if job.cause is not None else None,
    }


def _parse_states(values: Sequence[str]) -> tuple[jobs.JobState, ...]:
    """Turn ``--state`` arguments into states, refusing an unknown one.

    Refusing rather than ignoring, for the reason a dropped decision is refused
    upstream: a filter that silently matches nothing looks exactly like a queue
    that is empty, and the user's next move is to conclude their job vanished.
    """
    parsed: list[jobs.JobState] = []
    for value in values:
        try:
            parsed.append(jobs.JobState(value))
        except ValueError:
            raise CratekitError(
                Cause(
                    reason="job-unknown",
                    message=(
                        f"{value!r} is not a job state; the declared states are "
                        f"{', '.join(str(state) for state in jobs.JobState)}"
                    ),
                    remediation=Remediation(
                        steps=("filter on one of the declared job states",)
                    ),
                    origin=("cli.jobs",),
                    detail={"state": value},
                )
            ) from None
    return tuple(parsed)


# ---------------------------------------------------------------------------
# job list
# ---------------------------------------------------------------------------


def build_list(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    parser.add_argument(
        "--state",
        action="append",
        default=[],
        metavar="STATE",
        help="show only jobs in this state; repeatable",
    )
    parser.set_defaults(_handler=list_jobs)


def list_jobs(ctx: "Context") -> Envelope:
    states = _parse_states(ctx.args.state)
    with jobs.open_store() as store:
        rows = [_summary(store, job) for job in jobs.list_jobs(store, states=states or None)]
    counts: dict[str, int] = {str(state): 0 for state in jobs.JobState}
    for row in rows:
        counts[row["state"]] += 1
    return ctx.envelope(
        data={
            "job_id": NO_SINGLE_JOB,
            "state": ",".join(str(state) for state in states) if states else "all",
            "cause": None,
            "progress": {"jobs": rows, "counts": counts},
        },
        outcome=Outcome.OK if rows else Outcome.NO_OP,
    )


# ---------------------------------------------------------------------------
# job show
# ---------------------------------------------------------------------------


def build_show(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    parser.add_argument("job_id", help="the job to describe")
    parser.set_defaults(_handler=show)


def show(ctx: "Context") -> Envelope:
    with jobs.open_store() as store:
        job = jobs.reconcile(store, ctx.args.job_id)
        summary = _summary(store, job)
        drifted = _drift_warning(job)
    return ctx.envelope(
        data={
            "job_id": job.job_id,
            "state": str(job.state),
            "cause": summary["cause"],
            "progress": summary,
        },
        warnings=drifted,
    )


def _drift_warning(job: jobs.Job) -> tuple[dict[str, str], ...]:
    """Name what moved in the configuration since the job was queued (KTD9).

    A warning rather than a refusal. The job runs against its frozen inputs
    whatever this says; what the user needs is to know that the setting they just
    edited is not the setting this run is using, which is the half the recorded
    resume bug had no way to surface at all.
    """
    try:
        current = config.load()
    except config.ConfigError:
        return ()
    return handlers.drift_warnings(jobs.drift(job, current))


# ---------------------------------------------------------------------------
# job cancel
# ---------------------------------------------------------------------------


def build_cancel(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    parser.add_argument("job_id", help="the job to cancel")
    parser.set_defaults(_handler=cancel)


def cancel(ctx: "Context") -> Envelope:
    with jobs.open_store() as store:
        job = jobs.reconcile(store, ctx.args.job_id)
        job = jobs.cancel(store, job.job_id, stage=job.stage)
        summary = _summary(store, job)
    # Cancelling SUCCEEDS. The job is reported as cancelled in the payload, and
    # that is the whole point of R22's distinction: a cancel that exited non-zero
    # would be indistinguishable from a cancel that did not work.
    return ctx.envelope(
        data={
            "job_id": job.job_id,
            "state": str(job.state),
            "cause": summary["cause"],
            "progress": summary,
        }
    )


# ---------------------------------------------------------------------------
# job resume
# ---------------------------------------------------------------------------


def build_resume(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    parser.add_argument("job_id", help="the job to resume")
    parser.set_defaults(_handler=resume)


def argv_for(job: jobs.Job) -> list[str]:
    """Turn a stored handler key and frozen payload back into a command line.

    The registry lookup comes FIRST and imports nothing, so an unknown handler
    fails before any module is loaded. The import happens only after the key is
    known to be real, and only for the one module that owns it, which is what
    keeps a queued analysis job from pulling the analysis dependencies into a
    process that is merely listing jobs.
    """
    try:
        entry = registry.by_handler_key(job.handler_key)
    except KeyError:
        raise CratekitError(
            Cause(
                reason="internal-error",
                message=(
                    f"job {job.job_id} was queued for the handler "
                    f"{job.handler_key!r}, which this build does not register"
                ),
                remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
                origin=("cli.jobs",),
                detail={"job_id": job.job_id, "handler": job.handler_key},
            )
        ) from None
    if not entry.landed or not entry.argv_builder:
        raise CratekitError(
            Cause(
                reason="internal-error",
                message=(
                    f"{entry.name} cannot be re-invoked: it declares no way to turn "
                    f"a frozen payload back into a command line"
                ),
                remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
                origin=("cli.jobs",),
                detail={"job_id": job.job_id, "handler": job.handler_key},
            )
        )
    module = importlib.import_module(entry.module)
    return list(getattr(module, entry.argv_builder)(job))


def resume_argv(job: jobs.Job) -> list[str]:
    """The argument list that re-invokes a resume for one job.

    The identity case of the contract every long-running verb owes: given the
    frozen job, return the command line that continues it. It is written out here
    rather than special-cased inside ``argv_for`` so that the registry's claim
    that every long-running verb has a builder is true of this one too, and so the
    test that walks the registry and looks each builder up finds a real function.
    """
    return ["job", "resume", job.job_id]


def resume(ctx: "Context") -> Envelope:
    with jobs.open_store() as store:
        job = jobs.reconcile(store, ctx.args.job_id)
        # Checked here so a user who resumes a job that is already running sees
        # the refusal, rather than spawning a child that discovers the same thing
        # and writes it into a log nobody is watching.
        jobs.assert_free(job.job_id)
        if not job.is_open():
            job = jobs.retry(store, job.job_id)
        pid = jobs.spawn(store, job, argv_for(job))
        summary = _summary(store, job)
        summary["pid"] = pid
        drifted = _drift_warning(job)
    return ctx.envelope(
        data={
            "job_id": job.job_id,
            "state": str(job.state),
            "cause": summary["cause"],
            "progress": summary,
        },
        code=ExitCode.OK,
        warnings=drifted,
    )


__all__ = [
    "NO_SINGLE_JOB",
    "argv_for",
    "build_cancel",
    "build_list",
    "build_resume",
    "build_show",
    "cancel",
    "list_jobs",
    "resume",
    "resume_argv",
    "show",
]
