"""``crate tag folder``: queue genre and album-art tagging.

Long work is a job. The worker that walks a real folder binds a live
searcher; this shell freezes the folder and reports the job.
"""

from __future__ import annotations

from cratekit.cli.output import Envelope
from cratekit.core import config, jobs
from cratekit.core.cause import Cause, CratekitError, Remediation
from cratekit.core.exit_codes import Remedy


def _load() -> config.Config:
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=("tagging.cli",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def _reported(store, job) -> dict:
    return {
        "job_id": job.job_id,
        "state": str(job.state),
        "cause": job.cause.to_json() if job.cause is not None else None,
        "progress": jobs.progress(store, job.job_id),
    }


def build(parser, entry) -> None:
    parser.add_argument("folder", help="folder of audio to tag")
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="continue the tagging job already queued under this identifier",
    )
    parser.set_defaults(_handler=tag_folder)


def tag_argv(job) -> list[str]:
    folder = job.payload.get("folder", "")
    return ["tag", "folder", folder, "--job", job.job_id]


def tag_folder(ctx) -> Envelope:
    cfg = _load()
    with jobs.open_store() as store:
        if ctx.args.job:
            return ctx.envelope(data=_reported(store, jobs.reconcile(store, ctx.args.job)))
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={"folder": ctx.args.folder},
            cfg=cfg,
        )
        return ctx.envelope(data=_reported(store, job))
