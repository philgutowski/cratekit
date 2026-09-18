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
    parser.add_argument(
        "--job",
        required=True,
        metavar="JOB_ID",
        help="the finished intake job whose missing tracks to list",
    )
    parser.add_argument(
        "--out",
        default=None,
        metavar="DIR",
        help="folder to write the list into (default: the lists folder under download staging)",
    )
    parser.set_defaults(_handler=intake_missing)


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
        resume = intake_cli.playlist_argv if job.handler_key == "intake.playlist" else intake_cli.set_argv
        argv = shlex.join(resume(job))
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


def _out_dir(ctx, job: jobs.Job) -> Path:
    given = ctx.args.out
    if given:
        out = Path(str(given)).expanduser().absolute()
    else:
        out = intake_cli._load().paths.download_staging / LISTS_DIR
    if out.exists() and not out.is_dir():
        raise _unusable(
            f"{out} exists and is not a folder, so no list can be written into it",
            "name a folder with --out",
            job_id=job.job_id,
            out=str(out),
        )
    return out


def _check(key: str, status: str, detail: str) -> dict[str, Any]:
    return {"key": f"intake.missing.{key}", "title": key, "status": status,
            "detail": detail, "remedy": None}


def intake_missing(ctx) -> Envelope:
    """List the missing tracks of one finished intake job, or say why not."""
    with jobs.open_store() as store:
        job = _finished_or_refuse(store, str(ctx.args.job))
        reports = _reports_or_refuse(store, job)
    counts = {word: 0 for word in _WORDS}
    for report in reports:
        counts[report["state"]] += 1
    missing = [
        intake_cli.thawed(report["track"]) for report in reports if report["state"] == "missing"
    ]
    source_ref = str((job.payload or {}).get(intake_cli.SOURCE) or "") or None
    written = listdoc.Written(None, None, (), ())
    if missing:
        out = _out_dir(ctx, job)
        try:
            written = listdoc.write(
                out,
                f"intake-{job.job_id}",
                listdoc.rows_of(missing),
                listdoc.Provenance(
                    source=PROVENANCE_SOURCE[job.handler_key], source_ref=source_ref
                ),
            )
        except listdoc.ListDocRefused as exc:
            raise _unusable(
                str(exc), "move the file aside or name another folder with --out",
                job_id=job.job_id,
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
            job_id=job.job_id,
            unlisted_tracks=[
                {"artist": row.artist, "title": row.title} for row in written.unlisted
            ],
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
            f"{listed} missing track(s) written to {written.list_path}; next: {command}"
            if listed
            else "nothing listed: no track in this job is missing",
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
    ]
    summary = {
        "job_id": job.job_id,
        "source": source_ref,
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


__all__ = ["LISTS_DIR", "PROVENANCE_SOURCE", "build_missing", "intake_missing"]
