"""``crate sync all``: queue one increment job per enabled source.

The verb does not run a gated monolith. It freezes the configuration (KTD9),
queues one job per source the active profile enables, and reports them. Each
job carries the source id in its payload so a resume re-invokes this verb
against that one source rather than queueing the set again.

Layer: modules. The builder's parameters are unannotated so this file does not
import the CLI registry (KTD23).
"""

from __future__ import annotations

from cratekit.cli.output import Envelope, new_run_id
from cratekit.core import config, jobs, profiles
from cratekit.core.cause import Cause, CratekitError, Remediation
from cratekit.core.exit_codes import Remedy
from cratekit.sync import sources


def _load() -> config.Config:
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=("sync.cli",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def build_all(parser, entry) -> None:
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help=(
            "continue the increment already queued under this identifier rather "
            "than queueing a new set"
        ),
    )
    parser.set_defaults(_handler=all_sources)


def sync_argv(job) -> list[str]:
    """The command line that continues one queued increment."""
    return ["sync", "all", "--job", job.job_id]


def _check(job) -> dict:
    source_id = str(job.payload.get("source_id") or "")
    return {
        "key": f"sync.{source_id or job.job_id}",
        "title": source_id or job.handler_key,
        "status": "ok",
        "detail": f"queued as {job.job_id}",
        "remedy": None,
    }


def _diagnostic(queued) -> dict:
    source_ids = [str(job.payload.get("source_id") or "") for job in queued]
    return {
        "checks": [_check(job) for job in queued],
        "summary": {
            "queued": len(queued),
            "sources": source_ids,
        },
    }


def queue_all(ctx) -> dict:
    """Queue one job per enabled source, or reconcile the one already queued."""
    cfg = _load()
    with jobs.open_store() as store:
        if ctx.args.job:
            return _diagnostic([jobs.reconcile(store, ctx.args.job)])
        membership = profiles.resolve(cfg.profile.name, cfg.modules.explicit)
        shared_run = new_run_id()
        queued = [
            jobs.enqueue(
                store,
                handler_key=ctx.entry.handler_key,
                payload={"source_id": source_id, "run_id": shared_run},
                cfg=cfg,
            )
            for source_id in sources.enabled(membership)
        ]
        return _diagnostic(queued)


def all_sources(ctx) -> Envelope:
    """Queue the increments, or reconcile one already queued.

    WHAT THIS SHELL DOES NOT YET DO. It queues one job per enabled source and
    reports them, sharing one run id so later workers write one intake file
    (R29). Labels land the first worker in ``cratekit.label.cli``. Favorites
    still have no module. Playlists ride the same engine once a listing
    exists. ``cratekit.sync.run.increment`` is the engine those workers call.
    """
    data = queue_all(ctx)
    return ctx.envelope(data=data)
