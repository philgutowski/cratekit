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
    """The command line that continues one queued export.

    IT CARRIES ``--run``, AND WITHOUT IT THIS JOB COULD NEVER BE DRIVEN. The
    confirm gate is ``explicit``, so R34 makes it answerable only by a separate
    act recorded against a run. The child :mod:`cratekit.core.jobs` spawns is a
    fresh process, and ``cli.run`` mints a NEW run whenever ``--run`` is absent,
    so a resume naming only the job met the gate with nothing recorded and exited
    DECISION_REQUIRED. Every respawn did the same, so a confirmed export sat in
    the queue for ever. Measured by driving this function's own output through
    the dispatcher on 2026-08-23.

    The flag goes BEFORE the verb path because ``--run`` belongs to the root
    parser: a decision belongs to the invocation rather than to the subcommand.

    A job frozen by a build older than this one carries no gate run and resumes
    without the flag, which returns it to the refusal it was already in rather
    than crashing the driver on a missing key.
    """
    payload = job.payload or {}
    playlist = str(payload.get("playlist") or "")
    gate_run = payload.get(jobs.GATE_RUN_KEY)
    resume = ["--run", str(gate_run)] if gate_run else []
    return [*resume, "export", "playlist", playlist, "--job", job.job_id]


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
            # THE GATE RUN IS FROZEN so the respawned child can name the run
            # the confirmation was recorded against. See ``export_argv``.
            payload={"playlist": playlist, jobs.GATE_RUN_KEY: ctx.run.run_id},
            cfg=cfg,
        )
        return ctx.envelope(data=_reported(store, job))


__all__ = ["build", "export_argv", "export_playlist"]
