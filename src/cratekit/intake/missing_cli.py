"""``intake.missing``: the list document for a finished playlist intake (R-400).

``intake playlist`` resolves every track and stops; this verb reads the
finished job's committed reports and hands the missing rows to the one emitter,
:func:`cratekit.acquire.listdoc.write`, so a person gets a file ``acquire
download`` accepts without retyping a track.

ONLY MISSING IS LISTED. An owned track is held, an offered one is a question
nobody answered, and a suppressed one was deleted on purpose; listing any of
those would spend a download on an answer nobody gave. A report's state was
fixed when the job ran, so each row is asked again at listing time, and an
offered row a person has answered since is decided by that answer
(:mod:`cratekit.intake.missing_listed`). A row a download already staged is
not listed again (:mod:`cratekit.intake.missing_staged`).

A PARTIAL LIST THAT READS AS COMPLETE IS THE DEFECT THIS FILE IS SHAPED
AGAINST. A job still open, failed or cancelled is refused. A succeeded job is
listed only when every item has exactly one readable report, compared by item
identifier and not by count, because ``artifacts.committed`` skips a report it
cannot parse. A missing row the provider cannot name is handed on to a text
list on a failing check, never dropped (:mod:`cratekit.intake.missing_common`).

``--run RUN_ID`` lists a whole ``crate sync all`` pass as one (U73): the intake
jobs carrying the run AND queued for this library, since the queue is
installation scoped. One open job refuses the run, a failed or cancelled one is
refused unless ``--skip-failed`` leaves it out on a failing check, and a track
two playlists share is one row whose manifest keeps both.

``--list PATH`` names what a text list's missing rows can be named as and
offers the rest for review (:mod:`cratekit.intake.missing_found`).

Not gated and not destructive: :func:`listdoc.write` refuses rather than
replaces a file that holds anything else, and nothing here composes ``acquire
download``, so nothing here can spend a download.
"""

from __future__ import annotations

import shlex
from collections.abc import Mapping
from typing import Any

from cratekit.cli.output import Envelope
from cratekit.core import jobs
from cratekit.core.cause import refuse
from cratekit.intake import cli as intake_cli
from cratekit.intake import land_cli
from cratekit.intake.missing_common import (
    _WORDS,
    LISTS_DIR,
    MALFORMED,
    NO_ISRC,
    SEVERAL,
    UNKNOWN,
    UNREADABLE,
    _check,
    _unusable,
    provider_ref,
)
from cratekit.intake.missing_common import _named_by_isrc as _named_by_isrc
from cratekit.intake.missing_found import LIST_SOURCE, _missing_for_list, found_name
from cratekit.intake.missing_listed import _listed, _source_ref
from cratekit.intake.missing_listed import _staged as _staged

#: The payload key ``crate sync all`` stamps each job it queues with.
RUN_ID = "run_id"

#: What a run's list and its landing's intake file are named after the run, so
#: the list, the download and the landing read as one pass. ``land_name`` in the
#: listing's subject is this pass, handed to the landing as ``--pass``.
SYNCED_SUFFIX = "_synced"


def build_missing(parser, entry) -> None:
    chosen = parser.add_mutually_exclusive_group(required=True)
    chosen.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="the finished intake job whose missing tracks to list",
    )
    # ITS OWN DEST, NOT ``run``: the dispatcher's global ``--run`` reads
    # ``args.run`` and would hand a sync pass's identifier to the gate loader.
    chosen.add_argument(
        "--run",
        dest="sync_run",
        default=None,
        metavar="RUN_ID",
        help="the sync all pass whose intake jobs to list as one",
    )
    chosen.add_argument(
        "--list",
        dest="text_list",
        default=None,
        metavar="PATH",
        help=(
            "a text list, the unlisted list of an earlier run or any tracklist, "
            "whose missing tracks to find on the provider and list"
        ),
    )
    parser.add_argument(
        "--skip-failed",
        action="store_true",
        dest="skip_failed",
        help="with --run, leave out a job that failed or was cancelled and say so",
    )
    parser.add_argument(
        "--out",
        default=None,
        metavar="DIR",
        help="folder to write the list into (default: the lists folder under download staging)",
    )
    parser.set_defaults(_handler=intake_missing)


def _resume_argv(job: jobs.Job) -> str:
    resume = (
        intake_cli.playlist_argv if job.handler_key == "intake.playlist" else intake_cli.set_argv
    )
    return shlex.join(resume(job))


def _finished_or_refuse(store, job_id: str) -> jobs.Job:
    """The job, if it is an intake job that ran every track to the end."""
    job = jobs.get(store, job_id)
    if job.handler_key not in intake_cli.INTAKE_KEYS:
        raise refuse(
            "job-unknown",
            f"job {job.job_id} was queued for {job.handler_key!r}, which is not an "
            f"intake job, so there are no intake reports to list",
            steps=("name the job an intake playlist or intake set run printed",),
            origin=("intake.missing",),
            detail={"job_id": job.job_id, "handler": job.handler_key},
        )
    if job.state is not jobs.JobState.SUCCEEDED:
        argv = _resume_argv(job)
        raise _unusable(
            f"job {job.job_id} is {job.state}, not succeeded, so some of its tracks "
            f"may not be resolved and a list of the rest would read as complete",
            f"finish it with: crate {argv}"
            if job.is_open()
            else "queue the playlist again, let it finish, then list that job",
            inner=job.cause,
            job_id=job.job_id,
            state=str(job.state),
        )
    return job


def _reports_or_refuse(store, job: jobs.Job) -> tuple[dict[str, Any], ...]:
    """One readable report per item, read with the configuration the job froze.

    BY IDENTIFIER, NOT BY COUNT: a skipped report and a stray one would leave
    the count right and the list wrong.
    """
    wanted = [item.item_id for item in jobs.items(store, job.job_id)]
    if not wanted:
        # A JOB WITH NO ITEMS IS NOT A JOB WITH NOTHING MISSING (pre U57 builds):
        # zero reports against zero items would pass the comparison below.
        raise _unusable(
            f"job {job.job_id} has no items, so it never resolved a track; it was "
            f"queued by a build that did not record what its tracks were",
            "queue the playlist again and list the new job",
            job_id=job.job_id,
        )
    reports = intake_cli.ARTIFACTS.committed(jobs.frozen_config(job), job.job_id)
    reported = [str(report.get("item_id")) for report in reports]
    if sorted(reported) != sorted(wanted):
        absent = sorted(set(wanted) - set(reported))
        raise _unusable(
            f"job {job.job_id} has {len(wanted)} item(s) and {len(reports)} readable "
            f"report(s), so a list from them would leave tracks out without saying so",
            "the reports under the job's artifacts folder are damaged or missing; "
            "queue the playlist again and list the new job",
            job_id=job.job_id,
            items=len(wanted),
            reports=len(reports),
            unreported=absent,
        )
    for report in reports:
        if report.get("state") not in _WORDS or not isinstance(report.get("track"), Mapping):
            raise _unusable(
                f"the report for item {report.get('item_id')!r} of job {job.job_id} "
                f"does not say whether the track is missing, so the job cannot be listed",
                "queue the playlist again and list the new job",
                job_id=job.job_id,
                item_id=str(report.get("item_id")),
            )
    return reports


def job_reports(store, job: jobs.Job) -> tuple[dict[str, Any], ...]:
    """A finished intake job's committed reports, one per item, or the refusal."""
    return _reports_or_refuse(store, job)


def _run_jobs_or_refuse(
    store, run_id: str, *, skip_failed: bool
) -> tuple[list[jobs.Job], list[jobs.Job]]:
    """The run's finished intake jobs for THIS library, oldest first, and the skipped.

    THE LIBRARY AS WELL AS THE RUN, since the queue is installation scoped.
    Oldest first, the identifier breaking a tie, so a second run writes the
    same bytes and is recognised rather than refused.
    """
    if not run_id.strip():
        # A BLANK RUN IS NOT A RUN: a job queued with an empty run would match.
        raise _unusable(
            "--run was given no run identifier",
            "name the run a crate sync all pass printed",
            run_id=run_id,
        )
    library_id = intake_cli._load().library.volume_id
    found = sorted(
        (
            job
            for job in jobs.list_jobs(store)
            if job.handler_key in intake_cli.INTAKE_KEYS
            and (job.payload or {}).get(RUN_ID) == run_id
            and job.library_id == library_id
        ),
        key=lambda job: (job.created, job.job_id),
    )
    if not found:
        raise refuse(
            "job-unknown",
            f"no intake job queued for this library carries the run {run_id!r}, so "
            f"there is nothing to list for it",
            steps=(
                "name the run a crate sync all pass printed on this library",
                "a pass that queued no playlist has no intake jobs to list",
            ),
            origin=("intake.missing",),
            detail={"run_id": run_id, "library_id": library_id},
        )
    still_open = [job for job in found if job.is_open()]
    if still_open:
        # ONE OPEN JOB REFUSES THE RUN: the rest would read as the whole pass.
        raise _unusable(
            f"{len(still_open)} of the {len(found)} intake job(s) in run {run_id} "
            f"are still open, so a list of the rest would read as the whole pass: "
            + ", ".join(f"{job.job_id} ({job.state})" for job in still_open),
            *(f"finish job {job.job_id} with: crate {_resume_argv(job)}" for job in still_open),
            "then list the run again",
            run_id=run_id,
            open=[job.job_id for job in still_open],
        )
    unfinished = [job for job in found if job.state is not jobs.JobState.SUCCEEDED]
    if unfinished and not skip_failed:
        raise _unusable(
            f"{len(unfinished)} of the {len(found)} intake job(s) in run {run_id} "
            f"failed or were cancelled, so their tracks are unresolved and a list "
            f"without them would read as the whole pass: "
            + ", ".join(f"{job.job_id} ({job.state})" for job in unfinished),
            "pass --skip-failed to list the rest and name these as left out",
            "or queue those playlists again with crate sync all and list that run",
            inner=unfinished[0].cause,
            run_id=run_id,
            failed=[job.job_id for job in unfinished],
        )
    kept = [job for job in found if job.state is jobs.JobState.SUCCEEDED]
    if not kept:
        # EVERY JOB SKIPPED IS NOT NOTHING MISSING, which a no-op would read as.
        raise _unusable(
            f"every intake job in run {run_id} failed or was cancelled, so no track "
            f"of the pass was resolved and there is nothing to list",
            "queue those playlists again with crate sync all and list that run",
            run_id=run_id,
            failed=[job.job_id for job in unfinished],
        )
    return kept, unfinished


def synced_name(run_id: str) -> str:
    """The pass a run's list and its landing's intake file share, colons removed."""
    return f"{land_cli.default_name(run_id)}{SYNCED_SUFFIX}"


def in_pass(job: jobs.Job, pass_name: str) -> bool:
    """Whether ``job`` was queued by the run the pass ``pass_name`` is named for.

    ONE COMPARISON FOR EVERY READER OF A PASS (U110), made in the direction the
    name was built, so nothing puts the colons back. No run is no pass.
    """
    run_id = str((job.payload or {}).get(RUN_ID) or "")
    return bool(run_id) and synced_name(run_id) == pass_name


def _missing_for_run(ctx, run_id: str) -> Envelope:
    with jobs.open_store() as store:
        kept, skipped = _run_jobs_or_refuse(store, run_id, skip_failed=bool(ctx.args.skip_failed))
        found = [(job, _reports_or_refuse(store, job)) for job in kept]
    name = synced_name(run_id)
    checks = [
        _check(
            "jobs",
            "info",
            f"{len(kept)} finished intake job(s) of run {run_id} listed as one: "
            + ", ".join(job.job_id for job in kept),
        ),
        _check(
            "skipped",
            "fail" if skipped else "ok",
            f"{len(skipped)} job(s) failed or were cancelled and their tracks are NOT "
            f"in the list: " + ", ".join(f"{job.job_id} ({_source_ref(job)})" for job in skipped)
            if skipped
            else "every intake job in the run succeeded",
        ),
    ]
    return _listed(
        ctx,
        found,
        name=name,
        subject={
            "run_id": run_id,
            "jobs": [job.job_id for job in kept],
            "skipped": [job.job_id for job in skipped],
            "sources": [_source_ref(job) for job in kept],
            "land_name": name,
        },
        checks=checks,
        # TRUE ON BOTH MEDIA, AND READS NEITHER (R-770): a hint must not be one
        # more thing that can refuse a listing. ``--pass``, not ``--name``
        # (U110): the pass names the intake file ``sync mark`` finds jobs by.
        after=(
            f"; land what it downloads as one batch with: crate intake land "
            f"--pass {name}, adding --export XML, a Fresh Export of the collection, "
            f"while the intake tree is on the xml bridge, and no export once the "
            f"intake tree is database native"
        ),
        left_out=tuple(skipped),
    )


def intake_missing(ctx) -> Envelope:
    """List the missing tracks of one finished intake job or one sync pass, or say why not."""
    if ctx.args.sync_run is not None:
        return _missing_for_run(ctx, str(ctx.args.sync_run))
    if ctx.args.text_list is not None:
        if ctx.args.skip_failed:
            raise _unusable(
                "--skip-failed leaves failed jobs out of a run's list and means "
                "nothing for a text list",
                "drop --skip-failed",
                list=str(ctx.args.text_list),
            )
        return _missing_for_list(ctx, str(ctx.args.text_list))
    if ctx.args.skip_failed:
        # A FLAG THAT WOULD MEAN NOTHING IS REFUSED, not ignored, or a failed
        # job's refusal would read as the flag not working.
        raise _unusable(
            "--skip-failed leaves failed jobs out of a run's list and means nothing for one job",
            "drop --skip-failed, or list the whole pass with --run",
            job_id=str(ctx.args.job),
        )
    with jobs.open_store() as store:
        job = _finished_or_refuse(store, str(ctx.args.job))
        reports = _reports_or_refuse(store, job)
    return _listed(
        ctx,
        [(job, reports)],
        name=f"intake-{job.job_id}",
        subject={"job_id": job.job_id, "source": _source_ref(job)},
        checks=[],
    )


__all__ = [
    "LISTS_DIR",
    "LIST_SOURCE",
    "MALFORMED",
    "NO_ISRC",
    "RUN_ID",
    "SEVERAL",
    "SYNCED_SUFFIX",
    "UNKNOWN",
    "UNREADABLE",
    "build_missing",
    "found_name",
    "intake_missing",
    "job_reports",
    "provider_ref",
    "synced_name",
]
