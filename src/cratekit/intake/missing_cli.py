"""``intake.missing``: the list document for a finished playlist intake.

R-400's verb half, for the intake entrance. ``intake playlist`` resolves every
track to OWNED, OFFERED, SUPPRESSED or MISSING and stops, and ``acquire
download`` reads a list document nothing in the product wrote. This verb reads
the finished job's committed reports and hands the missing rows to the one
emitter, :func:`cratekit.acquire.listdoc.write`, so a person gets a file the
download verb accepts without retyping a track.

ONLY MISSING IS LISTED. An owned track is held, an offered one is a question a
person has not answered, and a suppressed one is a track somebody deleted on
purpose. Listing any of those would spend a download on an answer nobody gave.

A PARTIAL LIST THAT READS AS COMPLETE IS THE DEFECT THIS FILE IS SHAPED
AGAINST. A job that is still open, failed or was cancelled has not resolved
every track, so it is refused rather than listed. A succeeded job is listed only
when every one of its items has exactly one readable report, compared by item
identifier and not by count, because ``artifacts.committed`` skips a report it
cannot parse and a count that happened to match would hide which one it
skipped. A missing row the provider cannot be asked for comes back unlisted and
the report says how many, as a failing check rather than a quiet omission, and a
job whose missing rows are ALL like that is refused, because a no-op there reads
exactly like a job where everything was owned.

``--run RUN_ID`` is the same list for a whole ``crate sync all`` pass (U73). A
pass queues one intake job per new playlist under one run, and R29 says a run
ends in one intake file, so it ends in one list too, named for the run, which
downloads and lands as one batch. The jobs are the intake jobs carrying the run
AND queued for this library, because the queue is installation scoped and the
run alone would merge two libraries' passes. Every rule above holds per job, and
the run adds two: one open job refuses the whole run, since the list would read
as the pass, and a failed or cancelled job is named and refused unless
``--skip-failed`` says to leave it out, in which case it is reported as a failing
check. A track two playlists share is one row, taken from the first job, and the
manifest keeps every playlist it came from.

Not gated and not destructive: it writes two new files, and
:func:`listdoc.write` refuses rather than replaces a file that holds anything
else, so it cannot overwrite somebody's list. Nothing here composes ``acquire
download``, so nothing here can spend a download.
"""

from __future__ import annotations

import shlex
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from cratekit.acquire import listdoc
from cratekit.cli.output import Envelope
from cratekit.core import artifacts, jobs
from cratekit.core.cause import Outcome, refuse
from cratekit.intake import cli as intake_cli
from cratekit.intake import land_cli

#: The payload key ``crate sync all`` stamps each job it queues with.
RUN_ID = "run_id"

#: What a run's list and its landed batch are named after the run, so the list,
#: the download and the landing read as one pass.
SYNCED_SUFFIX = "_synced"

#: What the provenance sidecar says a listed row came from, by the job's key.
#: A set job never reaches the sidecar today, because a recognised track carries
#: no provider identifier and so is never listed, but it is not a playlist.
PROVENANCE_SOURCE: Mapping[str, str] = {"intake.playlist": "playlist", "intake.set": "set"}

#: The folder under download staging a list lands in when ``--out`` is not given.
LISTS_DIR = "lists"

#: The four words a committed intake report may carry. A report carrying any
#: other is refused, because a state this verb cannot read is a track it cannot
#: say is or is not missing.
_WORDS = frozenset({"owned", "offered", "suppressed", "missing"})


def build_missing(parser, entry) -> None:
    chosen = parser.add_mutually_exclusive_group(required=True)
    chosen.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="the finished intake job whose missing tracks to list",
    )
    # ITS OWN DEST, NOT ``run``. The dispatcher's global ``--run`` continues a
    # run stopped at a gate and reads ``args.run``; a subcommand flag writing
    # the same name would hand a sync pass's identifier to the gate loader.
    chosen.add_argument(
        "--run",
        dest="sync_run",
        default=None,
        metavar="RUN_ID",
        help="the sync all pass whose intake jobs to list as one",
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
    resume = intake_cli.playlist_argv if job.handler_key == "intake.playlist" else intake_cli.set_argv
    return shlex.join(resume(job))


def _unusable(message: str, *steps: str, inner=None, **detail: Any):
    return refuse(
        "intake-list-unusable",
        message,
        steps=steps,
        origin=("intake.missing",),
        detail=detail,
        inner=inner,
    )


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
            f"finish it with: crate {argv}" if job.is_open() else
            "queue the playlist again, let it finish, then list that job",
            inner=job.cause,
            job_id=job.job_id,
            state=str(job.state),
        )
    return job


def _reports_or_refuse(store, job: jobs.Job) -> tuple[dict[str, Any], ...]:
    """One readable report per item, read with the configuration the job froze.

    BY IDENTIFIER, NOT BY COUNT. A report the reader skipped and a stray report
    for an item the job never had would leave the count right and the list
    wrong.
    """
    wanted = [item.item_id for item in jobs.items(store, job.job_id)]
    if not wanted:
        # A JOB WITH NO ITEMS IS NOT A JOB WITH NOTHING MISSING. A build before
        # U57 queued intake jobs with no items, and one that was driven reads
        # succeeded over a listing nothing resolved; zero reports against zero
        # items would pass the comparison below and report a clean empty list.
        raise _unusable(
            f"job {job.job_id} has no items, so it never resolved a track; it was "
            f"queued by a build that did not record what its tracks were",
            "queue the playlist again and list the new job",
            job_id=job.job_id,
        )
    reports = artifacts.committed(intake_cli.ARTIFACTS, jobs.frozen_config(job), job.job_id)
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


def _out_dir(ctx, subject: Mapping[str, Any]) -> Path:
    given = ctx.args.out
    if given:
        out = Path(str(given)).expanduser().absolute()
    else:
        out = intake_cli._load().paths.download_staging / LISTS_DIR
    if out.exists() and not out.is_dir():
        raise _unusable(
            f"{out} exists and is not a folder, so no list can be written into it",
            "name a folder with --out",
            out=str(out),
            **subject,
        )
    return out


def _check(key: str, status: str, detail: str) -> dict[str, Any]:
    return {"key": f"intake.missing.{key}", "title": key, "status": status,
            "detail": detail, "remedy": None}


def _source_ref(job: jobs.Job) -> str | None:
    return str((job.payload or {}).get(intake_cli.SOURCE) or "") or None




def _run_jobs_or_refuse(
    store, run_id: str, *, skip_failed: bool
) -> tuple[list[jobs.Job], list[jobs.Job]]:
    """The run's finished intake jobs for THIS library, oldest first, and the skipped.

    THE LIBRARY AS WELL AS THE RUN. The queue is installation scoped, and a run
    identifier alone would list another library's jobs into this one's download.
    Oldest first, the identifier breaking a tie, so a second run writes the same
    bytes and is recognised as the same list rather than refused.
    """
    if not run_id.strip():
        # A BLANK RUN IS NOT A RUN. Compared as it stands it would match nothing
        # today, and a job queued with an empty run would be listed as a pass.
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
        # ONE OPEN JOB REFUSES THE RUN. A list of the finished ones would read as
        # the whole pass, and the open job's tracks would never be listed.
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
        # EVERY JOB SKIPPED IS NOT NOTHING MISSING. A no-op here would read like
        # a pass where the library already held everything.
        raise _unusable(
            f"every intake job in run {run_id} failed or was cancelled, so no track "
            f"of the pass was resolved and there is nothing to list",
            "queue those playlists again with crate sync all and list that run",
            run_id=run_id,
            failed=[job.job_id for job in unfinished],
        )
    return kept, unfinished


def _provenance(
    rows: tuple[listdoc.Row, ...], origins: list[jobs.Job]
) -> dict[str, listdoc.Provenance]:
    """Each listed id's provenance: the first job it came from, and every one.

    FIRST SOURCE WINS, as the list document's own row does, and the rest are
    kept rather than dropped, so a track two playlists share still says both.
    """
    first: dict[str, jobs.Job] = {}
    every: dict[str, list[str]] = {}
    for row, job in zip(rows, origins, strict=True):
        ref = str(row.ref or "").strip()
        if not ref:
            continue
        first.setdefault(ref, job)
        refs = every.setdefault(ref, [])
        said = _source_ref(job)
        if said is not None and said not in refs:
            refs.append(said)
    return {
        ref: listdoc.Provenance(
            source=PROVENANCE_SOURCE[job.handler_key],
            source_ref=_source_ref(job),
            source_refs=tuple(every[ref]),
        )
        for ref, job in first.items()
    }


def _listed(
    ctx,
    found: list[tuple[jobs.Job, tuple[dict[str, Any], ...]]],
    *,
    name: str,
    subject: dict[str, Any],
    checks: list[dict[str, Any]],
    after: str = "",
) -> Envelope:
    """Write one list from every missing report of ``found``, in order, and report it.

    ``subject`` identifies what was listed, a job or a run, on every refusal
    and at the head of the summary. ``checks`` are the caller's own rows,
    reported after the ones every listing carries.
    """
    counts = {word: 0 for word in _WORDS}
    missing = []
    origins: list[jobs.Job] = []
    for job, reports in found:
        for report in reports:
            counts[report["state"]] += 1
            if report["state"] == "missing":
                missing.append(intake_cli.thawed(report["track"]))
                origins.append(job)
    written = listdoc.Written(None, None, (), ())
    if missing:
        out = _out_dir(ctx, subject)
        rows = listdoc.rows_of(missing)
        try:
            written = listdoc.write(out, name, rows, _provenance(rows, origins))
        except listdoc.ListDocRefused as exc:
            raise _unusable(
                str(exc), "move the file aside or name another folder with --out",
                **subject,
            ) from exc
    listed = len(written.listed)
    unlisted = len(written.unlisted)
    if missing and not listed:
        # MISSING TRACKS AND NOTHING TO LIST IS NOT NOTHING TO DO. Reported as a
        # no-op it would read, to a person and to a script, exactly like a job
        # where everything was owned, and the tracks would be dropped.
        raise _unusable(
            f"{unlisted} missing track(s) and none carries a provider identifier, so "
            f"there is nothing acquire download could be asked for; nothing was written",
            "acquire download refuses a row with no provider id, so find these "
            "tracks on the provider, add them to a playlist, and run intake "
            "playlist on it",
            unlisted_tracks=[
                {"artist": row.artist, "title": row.title} for row in written.unlisted
            ],
            **subject,
        )
    command = (
        shlex.join(["crate", "acquire", "download", str(written.list_path)])
        if written.list_path is not None
        else None
    )
    checks = [
        _check(
            "written",
            "ok" if listed else "info",
            f"{listed} missing track(s) written to {written.list_path}; next: {command}{after}"
            if listed
            else f"nothing listed: no track in this {'run' if 'run_id' in subject else 'job'} is missing",
        ),
        _check("owned", "info", f"{counts['owned']} already in the library, not listed"),
        _check(
            "offered",
            "info",
            f"{counts['offered']} offered for review and not listed until answered; "
            f"see: crate review list",
        ),
        _check("suppressed", "info", f"{counts['suppressed']} deleted on purpose, not listed"),
        _check(
            "unlisted",
            "fail" if unlisted else "ok",
            f"{unlisted} missing track(s) carry no provider identifier and are NOT in the list"
            if unlisted
            else "every missing track is in the list",
        ),
        *checks,
    ]
    summary = {
        **subject,
        "list": str(written.list_path) if written.list_path is not None else None,
        "manifest": str(written.manifest_path) if written.manifest_path is not None else None,
        "next": command,
        "written": listed,
        "missing": counts["missing"],
        "owned": counts["owned"],
        "offered": counts["offered"],
        "suppressed": counts["suppressed"],
        "unlisted": unlisted,
        "unlisted_tracks": [
            {"artist": row.artist, "title": row.title} for row in written.unlisted
        ],
    }
    return ctx.envelope(
        data={"checks": checks, "summary": summary},
        outcome=Outcome.OK if listed else Outcome.NO_OP,
    )


def synced_name(run_id: str) -> str:
    """The name a run's list and its landed batch share, colons removed."""
    return f"{land_cli.default_name(run_id)}{SYNCED_SUFFIX}"


def _missing_for_run(ctx, run_id: str) -> Envelope:
    with jobs.open_store() as store:
        kept, skipped = _run_jobs_or_refuse(
            store, run_id, skip_failed=bool(ctx.args.skip_failed)
        )
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
            f"in the list: "
            + ", ".join(f"{job.job_id} ({_source_ref(job)})" for job in skipped)
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
        after=f"; land what it downloads as one batch with: crate intake land --name {name}",
    )


def intake_missing(ctx) -> Envelope:
    """List the missing tracks of one finished intake job or one sync pass, or say why not."""
    if ctx.args.sync_run is not None:
        return _missing_for_run(ctx, str(ctx.args.sync_run))
    if ctx.args.skip_failed:
        # A FLAG THAT WOULD MEAN NOTHING IS REFUSED, not ignored. One job that
        # failed is refused either way, and a person who asked to skip it would
        # otherwise read that refusal as the flag not working.
        raise _unusable(
            "--skip-failed leaves failed jobs out of a run's list and means nothing "
            "for one job",
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
    "PROVENANCE_SOURCE",
    "RUN_ID",
    "SYNCED_SUFFIX",
    "build_missing",
    "intake_missing",
    "synced_name",
]
