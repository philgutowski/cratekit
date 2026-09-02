"""What the two outbound verbs share, so a rule has one owner rather than two.

``crate export playlist`` and ``crate sync favorites`` differ in what they write
and in what an item is. They do NOT differ in how a queued job is resumed, how a
frozen configuration is loaded, or in what a person is warned about before they
confirm, and until this module existed each of those was written out twice.

**THE RESUME BRANCH IS THE ONE THAT MATTERED.** It carries the R-225 fix: a job
that half failed must exit with its own cause rather than through a normal
envelope, because a person whose export wrote nothing must not be told it
finished. Two copies of a fix is one copy that gets updated. ``master/cli.py``
still has the unfixed shape and this module is deliberately not reaching into
it: that verb is another unit's file, and changing its exit code from here would
be a second opinion about a surface this unit does not own.

**WHAT IS DELIBERATELY NOT HERE.** ``confirm_digest`` stays one function per
shell, because the two verbs digest different key sets and a single digest
builder would have to branch on which verb called it. Each shell's ``summary``
stays its own, because the export engine reports an unmatched row as a mapping
and the hearts engine reports it as a string, and one function over both would
reintroduce the shape branch. Both are passed in rather than merged.

``ctx`` is untyped here for the reason every builder in this package takes an
untyped ``entry`` (KTD23): this is modules-ranked and ``cratekit.cli`` is above
it, so naming that type would be reaching upward.

Layer: modules.
"""

from __future__ import annotations

from typing import Any, Callable, Mapping, Sequence

from cratekit.core import config, jobs
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation
from cratekit.core.exit_codes import Remedy
from cratekit.modules.outbound import account
from cratekit.modules.outbound.source import ResolvedPlaylist

#: The two payload keys both verbs freeze, spelled once. A key one shell reads
#: and the other spells differently is a resume that quietly does different work
#: from the run it continues, and the confirm digest is taken over both of them.
PLAYLIST = "playlist"
EXPORT = "export"


def load_config(origin: str) -> config.Config:
    """The current configuration, or the refusal a person can act on.

    ``origin`` names the shell for the cause, which is the only thing that
    differed between the two copies this replaces.

    THE SAME BODY EXISTS IN ``master/cli.py`` AND ``backup/cli.py`` and is NOT
    consolidated with them here. Those are other units' files and the shared home
    for all four would be ``core.config``, which is a wider change than this unit
    owns. Recorded rather than silently left at four copies.
    """
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=(origin,),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def reported(
    store,
    job,
    cfg: config.Config,
    summary: Callable[[config.Config, str], Mapping[str, Sequence[str]]],
) -> dict[str, Any]:
    """One queued job, flattened for the envelope, with what it actually wrote.

    ``summary`` is a parameter rather than a branch because the two verbs report
    different sets: added, already and unmatched for an export; hearted, already
    and unmatched for a sweep.
    """
    return {
        "job_id": job.job_id,
        "state": str(job.state),
        "cause": job.cause.to_json() if job.cause is not None else None,
        "progress": jobs.progress(store, job.job_id),
        "outbound": dict(summary(cfg, job.job_id)),
    }


def queue_warnings(
    resolved: ResolvedPlaylist, *, noun: str
) -> tuple[dict[str, str], ...]:
    """What the person should know at the moment they are asked to confirm.

    THE UNBOUND PROVIDER WARNING IS HERE RATHER THAN AT THE REFUSAL, and that is
    the honest half of deferring the refusal to the worker. Deferring is right
    for an input that can appear between queueing and running, which is the case
    ``master`` argues for a recording that may exist later. A missing adapter
    cannot appear later without a new build, so a person who is only told at
    drive time was told at the one moment they could do nothing with it.

    The dangling and repeated rows are reported rather than dropped for the
    reason ``source.resolve`` collects them: somebody whose export is short a
    track needs to know which one, and a count alone is not something to act on.
    """
    warnings: list[dict[str, str]] = []
    if not account.bound():
        warnings.append(
            {
                "code": "outbound-account-unbound",
                "message": (
                    "this build has no streaming provider adapter, so this job "
                    "will queue and then fail at the provider seam"
                ),
            }
        )
    if resolved.dangling:
        warnings.append(
            {
                "code": "playlist-track-missing",
                "message": (
                    f"{len(resolved.dangling)} {noun}(s) this playlist names are "
                    f"not in the export's collection and are not queued: "
                    f"{', '.join(resolved.dangling)}"
                ),
            }
        )
    if resolved.repeated:
        warnings.append(
            {
                "code": "playlist-track-repeated",
                "message": (
                    f"{len(resolved.repeated)} {noun}(s) appear more than once in "
                    f"this playlist and are queued once: "
                    f"{', '.join(resolved.repeated)}"
                ),
            }
        )
    return tuple(warnings)


def resume(
    ctx,
    spec,
    job_id: str,
    *,
    digest: Callable[[str, str], str],
    summary: Callable[[config.Config, str], Mapping[str, Sequence[str]]],
):
    """Answer the gate from the frozen payload, then drive the job's items.

    THIS BRANCH READS NOTHING FROM THE EXPORT DOCUMENT. The job's items are
    already in the queue and its identity is already frozen, so re-deriving here
    would make a resume refuse over a file the person has since moved, and would
    let a regenerated document silently change what a confirmed job does.

    THE DIGEST COMES OFF THE PAYLOAD for the same reason and for one more: the
    child ``jobs.spawn`` starts rebuilds its command line from that payload, so
    the two sides of the comparison have to be built from the same values or the
    job meets ``DecisionStale`` on every respawn.

    RECONCILE BEFORE DRIVING. A resume arrives after something stopped, and a
    claim left behind by a driver that died is state the queue cannot see for
    itself.

    IT RAISES ON A FAILED JOB RATHER THAN REPORTING ONE. That is R-225:
    ``master/cli.py``'s resume branch returns a normal envelope for a job that
    half failed and exits OK, so a person whose work did not happen is told it
    finished. U50 fixed it for ``backup.run`` by re-raising the job's own cause,
    and this is that fix with one owner instead of two.
    """
    with jobs.open_store() as store:
        queued = jobs.get(store, job_id)
        payload = queued.payload or {}
        option = ctx.gate.require(
            spec,
            digest=digest(
                str(payload.get(PLAYLIST) or ""), str(payload.get(EXPORT) or "")
            ),
        )
        if option == "abort":
            return ctx.envelope(
                data={"job_id": queued.job_id, "summary": {"queued": False}},
                outcome=Outcome.NO_OP,
            )
        frozen = jobs.frozen_config(queued)
        job = jobs.reconcile(store, job_id)
        warnings: tuple[dict[str, str], ...] = ()
        if job.is_open():
            _, warnings = ctx.run_job(store, job)
            job = jobs.get(store, job.job_id)
        if job.state is jobs.JobState.FAILED and job.cause is not None:
            raise CratekitError(job.cause)
        return ctx.envelope(
            data=reported(store, job, frozen, summary), warnings=warnings
        )


__all__ = [
    "EXPORT",
    "PLAYLIST",
    "load_config",
    "queue_warnings",
    "reported",
    "resume",
]
