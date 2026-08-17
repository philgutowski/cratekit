"""``crate analyze``: queue the heavy passes, never run them inline.

Long work is a job (KTD26, R22). The shell freezes the folder and the
item list. A killed driver resumes by trusting DONE rows and the
Camelot-prefixed names those rows left behind.
"""

from __future__ import annotations

from pathlib import Path

from cratekit.cli.output import Envelope
from cratekit.core import config, jobs
from cratekit.core.cause import Cause, CratekitError, Remediation
from cratekit.core.exit_codes import Remedy
from cratekit.core.naming import AUDIO_EXTS


def _load() -> config.Config:
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=("analysis.cli",),
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


def _audio_in(folder: Path) -> list[str]:
    if not folder.is_dir():
        return []
    return sorted(
        str(path)
        for path in folder.iterdir()
        if path.is_file() and path.suffix.lower() in AUDIO_EXTS
    )


def build(parser, entry) -> None:
    parser.add_argument("folder", help="folder of audio to analyse")
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="continue the analysis job already queued under this identifier",
    )
    parser.set_defaults(_handler=analyze_run)


def build_calibrate(parser, entry) -> None:
    parser.add_argument(
        "folder", nargs="?", default=None, help="labelled folder used as ground truth"
    )
    parser.set_defaults(_handler=analyze_calibrate)


def build_validate(parser, entry) -> None:
    parser.add_argument(
        "folder", nargs="?", default=None, help="labelled folder to score against"
    )
    parser.set_defaults(_handler=analyze_validate)


def build_restamp(parser, entry) -> None:
    parser.add_argument("folder", help="folder whose analysed values should be restamped")
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="continue the restamp job already queued under this identifier",
    )
    parser.set_defaults(_handler=analyze_restamp)


def analyze_argv(job) -> list[str]:
    folder = job.payload.get("folder", "")
    return ["analyze", "run", folder, "--job", job.job_id]


def restamp_argv(job) -> list[str]:
    folder = job.payload.get("folder", "")
    return ["analyze", "restamp", folder, "--job", job.job_id]


def analyze_run(ctx) -> Envelope:
    cfg = _load()
    folder = Path(ctx.args.folder)
    with jobs.open_store() as store:
        if ctx.args.job:
            return ctx.envelope(data=_reported(store, jobs.reconcile(store, ctx.args.job)))
        items = _audio_in(folder)
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={"folder": str(folder)},
            cfg=cfg,
            item_ids=items,
        )
        return ctx.envelope(data=_reported(store, job))


def analyze_calibrate(ctx) -> Envelope:
    return ctx.envelope(
        data={
            "checks": [
                {
                    "key": "calibrate.labels",
                    "title": "labelled ground truth",
                    "status": "awaiting",
                    "detail": ctx.args.folder or "no folder given",
                    "remedy": str(Remedy.REPORT_DEFECT),
                }
            ],
            "summary": {"folder": ctx.args.folder},
        }
    )


def analyze_validate(ctx) -> Envelope:
    return ctx.envelope(
        data={
            "checks": [
                {
                    "key": "validate.labels",
                    "title": "labelled ground truth",
                    "status": "awaiting",
                    "detail": ctx.args.folder or "no folder given",
                    "remedy": str(Remedy.REPORT_DEFECT),
                }
            ],
            "summary": {"folder": ctx.args.folder},
        }
    )


def analyze_restamp(ctx) -> Envelope:
    cfg = _load()
    folder = Path(ctx.args.folder)
    with jobs.open_store() as store:
        if ctx.args.job:
            return ctx.envelope(data=_reported(store, jobs.reconcile(store, ctx.args.job)))
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={"folder": str(folder)},
            cfg=cfg,
            item_ids=_audio_in(folder),
        )
        return ctx.envelope(data=_reported(store, job))
