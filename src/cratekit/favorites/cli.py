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
    """The command line that continues one queued favourites increment.

    TWO RUNS TRAVEL HERE AND THEY ARE NOT THE SAME RUN. ``--run-id`` is this
    verb's own argument and carries the INTAKE run shared with the other sources
    in a sync. ``--run`` is the root parser's flag and carries the GATE run, the
    one the confirm decision was recorded against. They defaulted to the same
    value, which is exactly why emitting only the first looked like carrying the
    run and restored no gate state at all: ``cli._run_state_for`` reads
    ``args.run`` and never ``args.run_id``.

    So this builder emitted ``--run-id`` and the child still minted a fresh run,
    met the explicit confirm gate with nothing recorded, and exited
    DECISION_REQUIRED on every respawn. The queue held a confirmed sync nothing
    could advance. Measured by driving this function's own output through the
    dispatcher on 2026-08-23. A predicate that searched the source for the
    substring ``--run`` reported this verb CLEAN, because ``--run-id`` contains
    it, which is the other half of why it survived.

    A job frozen by a build older than this one carries no gate run and resumes
    without the flag, which returns it to the refusal it was already in.
    """
    payload = job.payload or {}
    argv = ["sync", "favorites", "--job", job.job_id]
    run_id = payload.get("run_id")
    if run_id:
        argv.extend(["--run-id", str(run_id)])
    gate_run = payload.get(jobs.GATE_RUN_KEY)
    resume = ["--run", str(gate_run)] if gate_run else []
    return [*resume, *argv]


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
            # TWO RUNS, TWO KEYS, on purpose. ``run_id`` is the intake run this
            # sync shares across its sources. The gate run is the one the
            # confirm decision was recorded against, and conflating them is the
            # defect ``sync_favorites_argv`` describes.
            payload={
                "source_id": "favorites",
                "run_id": run_id,
                jobs.GATE_RUN_KEY: ctx.run.run_id,
            },
            cfg=cfg,
        )
        return ctx.envelope(data=_reported(store, job))


__all__ = ["build_sync", "sync_favorites", "sync_favorites_argv"]
