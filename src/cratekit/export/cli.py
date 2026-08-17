"""``crate export playlist``: confirm, then queue the outbound write.

Builders take an untyped ``entry`` so this file does not import the CLI
registry (KTD23). Long-running work queues a job. The engine in
``cratekit.modules.outbound.export`` is what a worker calls; this shell
freezes the playlist key so a resume cannot invent a second remote
playlist.
"""

from __future__ import annotations

from cratekit.cli.output import Envelope, digest_of
from cratekit.core import config, jobs
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, refuse
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
                origin=("export.cli",),
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
    """Declare the surface. ``entry`` is untyped so this layer does not name it."""
    del entry
    parser.add_argument("playlist", help="stable identifier of the library playlist")
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="continue the export already queued under this identifier",
    )
    parser.set_defaults(_handler=export_playlist)


def export_argv(job) -> list[str]:
    playlist = str((job.payload or {}).get("playlist") or "")
    argv = ["export", "playlist", playlist, "--job", job.job_id]
    return argv


def export_playlist(ctx) -> Envelope:
    """Confirm this playlist, then queue. The write itself is the worker."""
    playlist = str(ctx.args.playlist or "")
    if not playlist:
        raise refuse(
            "export-playlist-unknown",
            "export playlist needs the library playlist identifier",
            steps=("pass the playlist identifier after the verb",),
            origin=("export.cli",),
        )
    spec = ctx.entry.gates[0]
    option = ctx.gate.require(
        spec,
        digest=digest_of({"kind": "export.playlist", "playlist": playlist}),
    )
    if option == "abort":
        return ctx.envelope(
            data={"playlist": playlist, "summary": {"queued": False}},
            outcome=Outcome.NO_OP,
        )
    cfg = _load()
    with jobs.open_store() as store:
        if ctx.args.job:
            return ctx.envelope(data=_reported(store, jobs.reconcile(store, ctx.args.job)))
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={"playlist": playlist},
            cfg=cfg,
        )
        return ctx.envelope(data=_reported(store, job))


__all__ = ["build", "export_argv", "export_playlist"]
