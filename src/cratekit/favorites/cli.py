"""``crate sync favorites``: confirm the remote half, then queue.

The outbound confirm is a separate gate from any local colour or tag write
this verb may later accompany. The engine in
``cratekit.modules.outbound.hearts`` is add-only. This shell never hearts
and never colours; it freezes the run id so a resume cannot invent a
second pass.
"""

from __future__ import annotations

from cratekit.cli.output import Envelope, digest_of
from cratekit.core import config, jobs
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation
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
                origin=("favorites.cli",),
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


def build_sync(parser, entry) -> None:
    """Declare the surface. ``entry`` is untyped so this layer does not name it."""
    del entry
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="continue the favourites increment already queued under this identifier",
    )
    parser.add_argument(
        "--run-id",
        default=None,
        dest="run_id",
        help="intake run shared with the other sources in this sync",
    )
    parser.set_defaults(_handler=sync_favorites)


def sync_favorites_argv(job) -> list[str]:
    argv = ["sync", "favorites", "--job", job.job_id]
    run_id = (job.payload or {}).get("run_id")
    if run_id:
        argv.extend(["--run-id", str(run_id)])
    return argv


def sync_favorites(ctx) -> Envelope:
    """Confirm the remote heart-back, then queue. Add-only, never a remove."""
    spec = next(gate for gate in ctx.entry.gates if gate.name.endswith(".confirm"))
    option = ctx.gate.require(
        spec,
        digest=digest_of({"kind": "sync.favorites", "direction": "heartback"}),
    )
    if option == "abort":
        return ctx.envelope(
            data={"summary": {"queued": False}},
            outcome=Outcome.NO_OP,
        )
    cfg = _load()
    run_id = getattr(ctx.args, "run_id", None) or ctx.run.run_id
    with jobs.open_store() as store:
        if ctx.args.job:
            return ctx.envelope(data=_reported(store, jobs.reconcile(store, ctx.args.job)))
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={"source_id": "favorites", "run_id": run_id},
            cfg=cfg,
        )
        return ctx.envelope(data=_reported(store, job))


__all__ = ["build_sync", "sync_favorites", "sync_favorites_argv"]
