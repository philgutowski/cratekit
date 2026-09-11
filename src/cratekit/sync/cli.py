"""``crate sync all``: compose each enabled source's own increment, in one pass.

A COMPOSER, NOT A QUEUE OF ITS OWN (U61). Until U61 this verb queued one job
per enabled source under its own handler key, ``sync.all``, with no items and
no worker behind that key, so the verb that replaces ``dj-sync`` filed work the
product never ran and reported success over it. Now it calls each source's own
queueing path, under that source's own handler key, and the workers that
already run ``sync labels`` and ``sync favorites`` run what it queues. Nothing
is ever queued under ``sync.all``, so there is nothing to resume and the entry
declares no ``argv_builder``.

THE ORDER IS PLAN, ASK, QUEUE. Every enabled source is planned first, which is
where a source's own precondition refuses: an empty label registry, a missing
export. Then the one question favourites needs is asked. Only then is anything
queued. A refusal at the gate has therefore queued nothing, and answering it and
running again cannot queue the labels sweep twice.

ONE INTAKE RUN (R29). Every job carries ``ctx.run.run_id`` as its intake run,
which is the value each source's own verb uses when run alone, so the workers of
one pass write one intake file.

Layer: modules. The builder's parameters are unannotated so this file does not
import the CLI registry (KTD23), and each source's module is imported only when
the profile enables it.
"""

from __future__ import annotations

import dataclasses
from collections.abc import Callable
from typing import Any

from cratekit.cli.output import Envelope
from cratekit.core import config, jobs, profiles
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation
from cratekit.core.exit_codes import Remedy
from cratekit.modules.outbound import source as outbound_source
from cratekit.sync import sources

#: The gate this verb declares. Looked up on ``ctx.entry.gates`` by this name,
#: since the registry that declares it is above this layer.
CONFIRM = "sync.all.favorites.confirm"

#: The verb whose resume runs a favourites job, and the gate that resume asks.
#: ``Gates.hand_off`` answers the second on a run owned by the first.
FAVORITES_VERB = "sync.favorites"
FAVORITES_CONFIRM = "sync.favorites.confirm"

#: Why a source was not queued, when the reason is not a refusal's own slug.
NOT_BUILT = "not-built"
DECLINED = "declined"


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
    """Declare the surface. The two flags are the favourites source's inputs."""
    del entry
    parser.add_argument(
        "--export",
        default=None,
        metavar="EXPORT",
        help=(
            "the rekordbox collection export the favourites source reads; the "
            "live database is never read"
        ),
    )
    parser.add_argument(
        "--favorites-playlist",
        default=outbound_source.DEFAULT_FAVORITES_PLAYLIST,
        dest="favorites_playlist",
        metavar="NAME",
        help="the playlist whose members the favourites source sweeps",
    )
    parser.set_defaults(_handler=all_sources)


#: How a planned source is queued once the pass may proceed. A forward
#: reference, because ``tests/test_config.py`` refuses any module-level binding
#: that reaches into ``config`` and cannot tell an annotation from a snapshot.
Queue = Callable[[Any, "config.Config", str], "jobs.Job"]


@dataclasses.dataclass
class _Plan:
    """One enabled source, as far as the pass got with it."""

    spec: sources.SourceSpec
    queue: Queue | None = None
    warnings: tuple[dict[str, str], ...] = ()
    refused: Cause | None = None
    not_queued: str | None = None
    job: jobs.Job | None = None
    #: The question this source needs answered before it may queue, asked after
    #: every source is planned so the refusal can say what the pass would do.
    ask: Callable[[list[_Plan]], None] | None = None


def _plan_labels(spec: sources.SourceSpec, ctx) -> _Plan:
    from cratekit.label import cli as label_cli

    items = label_cli.sweep_items_or_refuse()

    def queue(store, cfg: config.Config, run_id: str) -> jobs.Job:
        return label_cli.queue_sweep(
            store, cfg, handler_key=str(spec.handler_key), run_id=run_id, item_ids=items
        )

    return _Plan(spec=spec, queue=queue, warnings=label_cli.queue_warnings())


def _plan_favorites(spec: sources.SourceSpec, ctx) -> _Plan:
    """Resolve the sweep, and leave the queueing to wait on the one question."""
    from cratekit.favorites import cli as favorites_cli
    from cratekit.modules.outbound import shell

    exported, resolved = favorites_cli.resolve_sweep(
        getattr(ctx.args, "export", None), getattr(ctx.args, "favorites_playlist", None)
    )
    plan = _Plan(spec=spec, warnings=shell.queue_warnings(resolved, noun="favourite"))

    def ask(plans: list[_Plan]) -> None:
        gate = next(g for g in ctx.entry.gates if g.name == CONFIRM)
        option = ctx.gate.require(
            gate,
            digest=favorites_cli.sweep_digest(exported, resolved),
            context=_awaiting(plans),
        )
        if option == "abort":
            plan.not_queued = DECLINED
            return
        gate_run = ctx.gate.hand_off(gate, verb=FAVORITES_VERB, gate=FAVORITES_CONFIRM)

        def queue(store, cfg: config.Config, run_id: str) -> jobs.Job:
            return favorites_cli.queue_sweep(
                store,
                cfg,
                handler_key=str(spec.handler_key),
                run_id=run_id,
                gate_run=gate_run,
                exported=exported,
                resolved=resolved,
            )

        plan.queue = queue

    plan.ask = ask
    return plan


#: One planner per source that has a worker. ``tests/test_sync_all.py`` pins
#: these keys to the sources ``cratekit.sync.sources`` declares a handler for,
#: so a source given a worker there without a planner here fails the suite.
PLANNERS: dict[str, Callable[[sources.SourceSpec, Any], _Plan]] = {
    "favorites": _plan_favorites,
    "labels": _plan_labels,
}


def _plan(spec: sources.SourceSpec, ctx) -> _Plan:
    if spec.handler_key is None:
        return _Plan(spec=spec, not_queued=NOT_BUILT)
    try:
        return PLANNERS[spec.source_id](spec, ctx)
    except CratekitError as exc:
        # A SOURCE'S OWN PRECONDITION, reported for that source rather than
        # ending the pass. ``dj-sync`` ran every source in one pass, and an empty
        # label registry is no reason not to sweep favourites.
        return _Plan(spec=spec, refused=exc.cause, not_queued=exc.cause.reason)


def _awaiting(plans: list[_Plan]) -> dict[str, Any]:
    """What a person is shown at the gate: nothing queued yet, and why not."""
    return {
        "queued": [],
        "would_queue": [p.spec.source_id for p in plans if p.not_queued is None],
        "not_queued": {
            p.spec.source_id: p.not_queued for p in plans if p.not_queued is not None
        },
    }


def _check(plan: _Plan) -> dict[str, Any]:
    source_id = plan.spec.source_id
    check: dict[str, Any] = {
        "key": f"sync.{source_id}",
        "title": source_id,
        "status": "ok",
        "detail": "",
        "remedy": None,
    }
    if plan.job is not None:
        check["detail"] = f"queued as {plan.job.job_id} under {plan.job.handler_key}"
    elif plan.refused is not None:
        check["status"] = "fail"
        check["detail"] = f"not queued: {plan.refused.message}"
        check["remedy"] = str(plan.refused.remediation.remedy)
    elif plan.not_queued == NOT_BUILT:
        check["status"] = "info"
        check["detail"] = (
            "not built: this source has no listing and no worker yet, so nothing "
            "was queued for it"
        )
    else:
        check["status"] = "info"
        check["detail"] = (
            "not queued: the confirmation was answered abort; the source's own "
            "verb asks the same question on its own"
        )
    return check


def _report(plans: list[_Plan], run_id: str) -> dict[str, Any]:
    queued = [p for p in plans if p.job is not None]
    return {
        "checks": [_check(p) for p in plans],
        "summary": {
            "run_id": run_id,
            "queued": len(queued),
            "sources": [p.spec.source_id for p in queued],
            "jobs": [
                {
                    "source": p.spec.source_id,
                    "job_id": p.job.job_id,
                    "handler_key": p.job.handler_key,
                }
                for p in queued
                if p.job is not None
            ],
            "not_queued": {
                p.spec.source_id: p.not_queued for p in plans if p.not_queued is not None
            },
        },
    }


def compose(ctx) -> tuple[dict[str, Any], Outcome, tuple[dict[str, str], ...]]:
    """Plan every enabled source, ask the one question, then queue. See the module doc."""
    cfg = _load()
    membership = profiles.resolve(cfg.profile.name, cfg.modules.explicit)
    run_id = ctx.run.run_id
    plans = [_plan(spec, ctx) for spec in sources.enabled_specs(membership)]

    for plan in plans:
        if plan.ask is not None:
            plan.ask(plans)

    ready = [(p, p.queue) for p in plans if p.queue is not None]
    if ready:
        with jobs.open_store() as store:
            for plan, queue in ready:
                plan.job = queue(store, cfg, run_id)

    data = _report(plans, run_id)
    refused = [p.refused for p in plans if p.refused is not None]
    if not ready and refused:
        # NOTHING QUEUED AND A SOURCE REFUSED. Not a no-op: a person who ran a
        # sync and got nothing because of something they can fix is told so
        # with that source's own remedy, and the whole pass rides the detail.
        first = refused[0]
        raise CratekitError(
            dataclasses.replace(first, detail={**dict(first.detail or {}), "sources": data})
        )

    warnings: list[dict[str, str]] = []
    for plan in plans:
        if plan.job is not None:
            warnings.extend(plan.warnings)
        elif plan.refused is not None:
            warnings.append(
                {
                    "code": "sync-source-not-queued",
                    "message": f"{plan.spec.source_id}: {plan.refused.message}",
                }
            )
    # THE HONEST ZERO. Nothing refused and nothing queued is the slim profile's
    # every run, or a declined confirmation, and it is a no-op rather than an ok.
    outcome = Outcome.OK if ready else Outcome.NO_OP
    return data, outcome, tuple(warnings)


def all_sources(ctx) -> Envelope:
    """Queue each enabled source's own increment and report every source."""
    data, outcome, warnings = compose(ctx)
    return ctx.envelope(data=data, outcome=outcome, warnings=warnings)
