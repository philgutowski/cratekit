"""The four ``intake.*`` verbs: set, identify, playlist, file.

Builders take unannotated parameters on purpose. ``entry`` is a registry
Entry, and naming that type here would be this layer importing the one
above it.

Long work is queued. Identification-only runs inline because it is the
spend gate plus a tracklist, not a download. A file already on disk is a
plan, not a job: there is no remote work.
"""

from __future__ import annotations

from pathlib import Path

from cratekit.cli.output import Envelope, digest_of
from cratekit.core import config, jobs
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation
from cratekit.core.exit_codes import Remedy
from cratekit.intake import normalize, pipeline, recognize


def _load() -> config.Config:
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=("intake.cli",),
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


def _plan(items: list[dict[str, str]], *, kind: str) -> dict:
    return {
        "digest": digest_of({"kind": kind, "items": items}),
        "items": items,
        "totals": {"count": len(items)},
        "chunk": None,
    }


def build_set(parser, entry) -> None:
    parser.add_argument("source", help="set recording path or mix URL")
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="continue the intake job already queued under this identifier",
    )
    parser.set_defaults(_handler=intake_set)


def build_identify(parser, entry) -> None:
    parser.add_argument("source", help="set recording path or mix URL")
    parser.set_defaults(_handler=intake_identify)


def build_playlist(parser, entry) -> None:
    parser.add_argument("source", help="streaming playlist URL")
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="continue the playlist job already queued under this identifier",
    )
    parser.set_defaults(_handler=intake_playlist)


def build_file(parser, entry) -> None:
    parser.add_argument("source", help="audio file already on this machine")
    parser.add_argument(
        "--export",
        default=None,
        metavar="XML",
        help="Fresh Export to splice into; required to write",
    )
    parser.set_defaults(_handler=intake_file)


def set_argv(job) -> list[str]:
    source = job.payload.get("source", "")
    return ["intake", "set", source, "--job", job.job_id]


def playlist_argv(job) -> list[str]:
    source = job.payload.get("source", "")
    return ["intake", "playlist", source, "--job", job.job_id]


def intake_set(ctx) -> Envelope:
    cfg = _load()
    with jobs.open_store() as store:
        if ctx.args.job:
            return ctx.envelope(data=_reported(store, jobs.reconcile(store, ctx.args.job)))
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={"source": ctx.args.source},
            cfg=cfg,
        )
        return ctx.envelope(data=_reported(store, job))


def intake_identify(ctx) -> Envelope:
    recognize.assert_recognition_ready()
    source = Path(ctx.args.source)
    result = pipeline.identify_only(source)
    return ctx.envelope(
        data={
            "matched": [],
            "needs_review": [],
            "missing": [
                {"artist": row.artist, "title": row.title, "ref": row.ref}
                for row in result.rows
            ],
        }
    )


def intake_playlist(ctx) -> Envelope:
    cfg = _load()
    with jobs.open_store() as store:
        if ctx.args.job:
            return ctx.envelope(data=_reported(store, jobs.reconcile(store, ctx.args.job)))
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={"source": ctx.args.source},
            cfg=cfg,
        )
        return ctx.envelope(data=_reported(store, job))


def intake_file(ctx) -> Envelope:
    cfg = _load()
    path = Path(ctx.args.source)
    rows = normalize.from_audio_file(path)
    items = [{"path": str(path), "artist": row.artist, "title": row.title} for row in rows]
    plan = _plan(items, kind="file")
    export = ctx.args.export
    if export:
        destination = path.with_name(path.stem + "_inboxed.xml")
        pipeline.ingest_file(
            path,
            cfg=cfg,
            export=Path(export),
            destination=destination,
        )
        plan["items"][0]["destination"] = str(destination)
    return ctx.envelope(data=plan, outcome=Outcome.OK)
