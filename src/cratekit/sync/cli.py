"""``crate sync all``: compose each enabled source's own increment, in one pass.

A COMPOSER, NOT A QUEUE OF ITS OWN (U61). It calls each source's own queueing
path under that source's handler key, so existing workers run the jobs.
Nothing is queued under ``sync.all``, so the entry declares no
``argv_builder``.

LABELS ARE NOT SWEPT HERE (U109). A guided source is never planned, called or
queued; the report names its verb instead.

THE ORDER IS PLAN, ASK, QUEUE. Sources are planned first, where their own
preconditions refuse, then favourites' one question is asked, then anything is
queued, so a refusal at the gate has queued nothing and a rerun cannot queue
twice.

ONE INTAKE RUN (R29). Every job carries ``ctx.run.run_id``, so one pass writes
one intake file. One source may file several jobs (U64), so a plan carries a
list and a refusal part way keeps the filed ones named.

THE PASS NAMES ITS NEXT STEP (U73), a ``sync.next`` check naming ``crate
intake missing --run RUN_ID`` when it queued an intake job.

A READ NEEDS NO CONSENT A WRITE DOES (U74). Favourites' inbound half (listing
the account's hearts) is queued whatever the question's answer and whether or
not the export was found, but never beside an open job already listing them.

Layer: modules. The builder's parameters are unannotated so this file does not
import the CLI registry (KTD23), and each source's module is imported only when
the profile enables it.
"""

from __future__ import annotations

import dataclasses
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from cratekit.cli.output import Envelope, load_config
from cratekit.core import config, jobs
from cratekit.core.cause import Cause, CratekitError, Outcome
from cratekit.sync import sources

if TYPE_CHECKING:
    # A NAME FOR THE ANNOTATION ONLY, so the label package is imported lazily.
    from cratekit.label.catalogue import HeartsShortfall

#: The gate this verb declares, looked up by name since the registry is above this layer.
CONFIRM = "sync.all.favorites.confirm"

#: The verb whose resume runs a favourites job, and the gate it asks (via ``Gates.hand_off``).
FAVORITES_VERB = "sync.favorites"
FAVORITES_CONFIRM = "sync.favorites.confirm"

#: Why a source was not queued, when the reason is not a refusal's own slug.
NOT_BUILT = "not-built"
DECLINED = "declined"
#: Listed and found nothing new; the check says why each playlist was excluded.
NOTHING_NEW = "nothing-new"


def _load() -> config.Config:
    """Read config, turning a configuration failure into a typed cause."""
    return load_config(("sync.cli",))


def build_all(parser, entry) -> None:
    """Declare the surface. The two flags are the favourites source's inputs.

    ``--favorites-playlist`` defaults to None (the outbound default), so
    building the verb imports no toggleable package (U304).
    """
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
        default=None,
        dest="favorites_playlist",
        metavar="NAME",
        help="the playlist whose members the favourites source sweeps",
    )
    parser.set_defaults(_handler=all_sources)


#: How a planned source is queued, appending each job AS IT IS FILED. String
#: references, since ``tests/test_config.py`` refuses a module level binding
#: that reaches into ``config``.
Queue = Callable[[Any, "config.Config", str, "list[jobs.Job]"], None]


@dataclasses.dataclass
class _Inbound:
    """A source's read only half (U74), queued whatever its write half's answer.

    Its refusal, reason and jobs are its own, independent of the write half.
    """

    handler_key: str
    #: The second queue callable. None when the half has nothing to queue.
    queue: Queue | None = None
    filed: list[jobs.Job] = dataclasses.field(default_factory=list)
    refused: Cause | None = None
    not_queued: str | None = None
    #: How many hearts the listing held, or None when nothing was listed.
    hearts: int | None = None
    #: The open jobs already listing the hearts, when that is why none was queued.
    open_jobs: tuple[str, ...] = ()
    #: What the provider declared and did not serve (R-504), or None.
    shortfall: HeartsShortfall | None = None

    def block(self) -> dict[str, Any]:
        return {
            "handler_key": self.handler_key,
            "hearts": self.hearts,
            "job_ids": [job.job_id for job in self.filed],
            "not_queued": self.not_queued,
            "open_jobs": list(self.open_jobs),
            "shortfall": self.shortfall.block() if self.shortfall is not None else None,
        }


@dataclasses.dataclass
class _Plan:
    """One enabled source, as far as the pass got with it."""

    spec: sources.SourceSpec
    queue: Queue | None = None
    warnings: tuple[dict[str, str], ...] = ()
    refused: Cause | None = None
    not_queued: str | None = None
    filed: list[jobs.Job] = dataclasses.field(default_factory=list)
    #: A source's own block for the summary, keyed by its identifier there.
    detail: dict[str, Any] | None = None
    #: Rebuilds ``detail`` from what was filed, once queueing is over.
    describe: Callable[[list[jobs.Job]], dict[str, Any]] | None = None
    #: The question this source needs answered, asked after every source is planned.
    ask: Callable[[list[_Plan], tuple[sources.SourceSpec, ...]], None] | None = None
    #: Words the source's check carries whatever its status, since the human
    #: output prints only check details.
    note: Callable[[dict[str, Any]], str | None] | None = None
    #: The source's read only half, when its spec declares one.
    inbound: _Inbound | None = None


def _filed(plan: _Plan) -> list[jobs.Job]:
    """Every job the source filed, its read only half's included."""
    return [*plan.filed, *(plan.inbound.filed if plan.inbound is not None else ())]


def _hearts_jobs(store, cfg: config.Config, *, handler_key: str) -> tuple[jobs.Job, ...]:
    """Every job listing the account's hearts for THIS library, however it was queued.

    A hand run ``crate intake playlist favorites`` carries the same key and
    ``source_id``; the library filter is because the queue is installation scoped.
    """
    from cratekit.intake import cli as intake_cli

    return tuple(
        job
        for job in jobs.list_jobs(store)
        if job.handler_key == handler_key
        and (job.payload or {}).get("source_id") == intake_cli.FAVORITES_SOURCE_ID
        and job.library_id == cfg.library.volume_id
    )


def _plan_inbound(spec: sources.SourceSpec, cfg: config.Config) -> _Inbound:
    """List the account's hearts as ``crate intake playlist favorites`` lists them.

    NEVER RAISES A REFUSAL; a failure is recorded against this half so the rest
    still runs. Listed at plan time, queued with the pass.
    """
    from cratekit.intake import cli as intake_cli
    from cratekit.label import catalogue
    from cratekit.sync import playlists

    handler_key = str(spec.inbound_key)
    inbound = _Inbound(handler_key=handler_key)
    try:
        with jobs.open_store() as store:
            in_flight = tuple(
                job.job_id
                for job in _hearts_jobs(store, cfg, handler_key=handler_key)
                if job.is_open()
            )
        if in_flight:
            inbound.not_queued, inbound.open_jobs = playlists.Excluded.IN_FLIGHT, in_flight
            return inbound
        tracks, short = intake_cli.list_favorites(catalogue.resolve(cfg))
    except CratekitError as exc:
        inbound.refused, inbound.not_queued = exc.cause, exc.cause.reason
        return inbound
    inbound.hearts = len(tracks)
    inbound.shortfall = short
    if not tracks:
        inbound.not_queued = playlists.Excluded.EMPTY
        return inbound

    def queue(store, cfg: config.Config, run_id: str, filed: list[jobs.Job]) -> None:
        filed.append(
            intake_cli.queue_playlist(
                store,
                cfg,
                handler_key=handler_key,
                reference=intake_cli.FAVORITES,
                tracks=tracks,
                run_id=run_id,
                source_id=intake_cli.FAVORITES_SOURCE_ID,
            )
        )

    inbound.queue = queue
    return inbound


def _plan_favorites(spec: sources.SourceSpec, ctx) -> _Plan:
    """Plan the read only half, resolve the sweep, and leave its queueing to the question."""
    from cratekit.favorites import cli as favorites_cli
    from cratekit.modules.outbound import shell, source

    plan = _Plan(spec=spec)
    # LOADED ONCE, for both halves (R-227), so one pass has one answer. Raising
    # here drops nothing, since the read half is not planned yet.
    cfg = _load()
    if spec.inbound_key is not None:
        plan.inbound = _plan_inbound(spec, cfg)
    try:
        exported, resolved = favorites_cli.resolve_sweep(
            getattr(ctx.args, "export", None),
            getattr(ctx.args, "favorites_playlist", None),
            cfg=cfg,
        )
    except CratekitError as exc:
        # THE WRITE HALF'S OWN PRECONDITION, recorded rather than raised, since
        # ``_plan`` would build a fresh plan and drop the read half.
        plan.refused, plan.not_queued = exc.cause, exc.cause.reason
        return plan
    # THE FAVOURITES VERB'S STANDING WARNING TRAVELS WITH THE COMPOSITION
    # (R-424), since this builds the plan itself; only plans that filed carry
    # it. THE EXPORT'S AGE is read once and goes to the question and the
    # warnings alike (R-227).
    age = source.export_age(exported, limit_days=cfg.outbound.export_stale_days)
    plan.warnings = (
        *shell.queue_warnings(resolved, noun="favourite", age=age),
        *favorites_cli.local_write_warning(),
    )

    def ask(plans: list[_Plan], guided: tuple[sources.SourceSpec, ...]) -> None:
        gate = next(g for g in ctx.entry.gates if g.name == CONFIRM)
        # THE TRACKS THE SWEEP'S DIGEST COVERS ARE SHOWN (R-693).
        option = ctx.gate.require(
            gate,
            plan={
                "digest": favorites_cli.sweep_digest(exported, resolved),
                "items": list(resolved.track_ids),
            },
            context={
                **_awaiting(plans, guided),
                shell.PLAYLIST: resolved.key,
                shell.EXPORT_PATH: str(exported),
                **shell.shown_export(age),
                **favorites_cli.sweep_source_facts(resolved),
            },
        )
        if option == "abort":
            plan.not_queued = DECLINED
            return
        gate_run = ctx.gate.hand_off(gate, verb=FAVORITES_VERB, gate=FAVORITES_CONFIRM)

        def queue(store, cfg: config.Config, run_id: str, filed: list[jobs.Job]) -> None:
            filed.append(
                favorites_cli.queue_sweep(
                    store,
                    cfg,
                    handler_key=str(spec.handler_key),
                    run_id=run_id,
                    gate_run=gate_run,
                    exported=exported,
                    resolved=resolved,
                )
            )

        plan.queue = queue

    plan.ask = ask
    return plan


def _plan_playlists(spec: sources.SourceSpec, ctx) -> _Plan:
    """List the account and decide every playlist. Queueing waits for the pass.

    THE CATALOGUE IS LOOKED UP AT CALL TIME, so a missing credential refuses
    only this source.
    """
    from cratekit.label import catalogue
    from cratekit.sync import playlists

    cfg = _load()
    handler_key = str(spec.handler_key)
    found = catalogue.resolve(cfg)
    # THE YEAR PLAYLISTS ``label playlists`` BUILT ARE NEVER INTAKE (R-835),
    # read first so an unreadable ledger refuses this source.
    from cratekit.modules.outbound import ledger

    label_built = ledger.label_playlist_ids(cfg)
    # NOR ARE THE SET PLAYLISTS ``export set`` MADE (R-837).
    set_built = ledger.set_playlist_ids(cfg)
    # NOR ARE THE PLAYLISTS ``sync pair`` KEEPS (U130).
    from cratekit.modules.outbound import pairs

    paired = pairs.paired_ids(cfg)
    # NOR ARE THE PLAYLISTS ``crate organize`` MIRRORS (U147).
    mirrored = ledger.mirror_playlist_ids(cfg)
    with jobs.open_store() as store:
        sweep = playlists.plan(
            store,
            cfg,
            found,
            handler_key=handler_key,
            label_built=label_built,
            set_built=set_built,
            paired=paired,
            mirrored=mirrored,
        )

    def describe(filed: list[jobs.Job]) -> dict[str, Any]:
        return playlists.report(sweep, filed)

    plan = _Plan(spec=spec, describe=describe, detail=describe([]), note=playlists.said)
    warnings: list[dict[str, str]] = []
    if sweep.unreadable:
        warnings.append(
            {
                "code": "sync-playlists-unreadable",
                "message": (
                    f"{len(sweep.unreadable)} account playlist(s) could not be "
                    f"listed and were not queued; the next sync offers them again"
                ),
            }
        )
    # EACH UNREAD TRACK OF A QUEUED PLAYLIST IS NAMED (R-1289), since the
    # playlist is recorded once its job succeeds and is not offered again.
    left = {
        identity: tracks for identity, tracks in sweep.unread.items() if identity in sweep.ready
    }
    if left:
        names = sweep.names()
        warnings.append(
            {
                "code": "sync-playlists-unread",
                "message": (
                    f"{sum(len(tracks) for tracks in left.values())} track(s) on "
                    f"{len(left)} queued account playlist(s) were not queued: "
                    + "; ".join(
                        f"{names.get(identity) or identity}: "
                        + ", ".join(f"{ref} ({one['why']})" for ref, one in tracks.items())
                        for identity, tracks in left.items()
                    )
                    + ". Every other track on those playlists is queued, and once a "
                    "playlist's intake job succeeds no later sync offers it again, so "
                    "a track named here is brought in by hand once the account names it"
                ),
            }
        )
    if sweep.short:
        # A SHORT LISTING IS SAID PER PLAYLIST (R-515).
        names = sweep.names()
        warnings.append(
            {
                "code": "sync-playlists-withheld",
                "message": (
                    f"{len(sweep.short)} account playlist(s) listed short of the "
                    f"count the provider declares: "
                    + "; ".join(
                        f"{names.get(identity) or identity}: {block['declared']} "
                        f"declared, {block['listed']} listed, {block['withheld']} "
                        f"withheld by the provider"
                        for identity, block in sweep.short.items()
                    )
                    + ". The withheld tracks are in no report this pass makes"
                ),
            }
        )
    if warnings:
        plan.warnings = tuple(warnings)
    if not sweep.ready:
        plan.not_queued = NOTHING_NEW
        return plan

    def queue(store, cfg: config.Config, run_id: str, filed: list[jobs.Job]) -> None:
        playlists.queue(
            store, cfg, sweep, handler_key=handler_key, run_id=run_id, filed=filed
        )

    plan.queue = queue
    return plan


#: One planner per source with a worker, pinned to ``sources`` by ``tests/test_sync_all.py``.
PLANNERS: dict[str, Callable[[sources.SourceSpec, Any], _Plan]] = {
    "favorites": _plan_favorites,
    "playlists": _plan_playlists,
}


def _guided(guided: tuple[sources.SourceSpec, ...]) -> dict[str, str | None]:
    """Each guided source, keyed by identifier, and the command that takes it."""
    return {spec.source_id: spec.command() for spec in guided}


def _guided_step(spec: sources.SourceSpec) -> str:
    """The guided row's words as a refusal step, for a pass that queued nothing."""
    return f"{spec.source_id} are not swept by sync all; take them with: {spec.command()}"


def _guided_check(spec: sources.SourceSpec) -> dict[str, Any]:
    """The one row naming the verb that takes a guided source instead (U109).

    A check, since the default human output prints only checks.
    """
    return {
        "key": f"sync.{spec.source_id}",
        "title": spec.source_id,
        "status": "info",
        "detail": (
            f"not swept by sync all; {spec.command()} takes this source on its "
            "own, and asks before it downloads anything"
        ),
        "remedy": None,
    }


def _plan(spec: sources.SourceSpec, ctx) -> _Plan:
    if spec.handler_key is None:
        return _Plan(spec=spec, not_queued=NOT_BUILT)
    try:
        return PLANNERS[spec.source_id](spec, ctx)
    except CratekitError as exc:
        # A SOURCE'S OWN PRECONDITION, reported for that source rather than
        # ending the pass.
        return _Plan(spec=spec, refused=exc.cause, not_queued=exc.cause.reason)


def _awaiting(
    plans: list[_Plan], guided: tuple[sources.SourceSpec, ...]
) -> dict[str, Any]:
    """What a person is shown at the gate: nothing queued yet, and why not.

    ``inbound`` says what each read only half does WHATEVER the answer;
    ``guided`` names each guided source's verb (U109).
    """
    return {
        "queued": [],
        "would_queue": [p.spec.source_id for p in plans if p.not_queued is None],
        "not_queued": {
            p.spec.source_id: p.not_queued for p in plans if p.not_queued is not None
        },
        "inbound": {
            p.spec.source_id: {
                "queued_whatever_the_answer": p.inbound.queue is not None,
                "not_queued": p.inbound.not_queued,
            }
            for p in plans
            if p.inbound is not None
        },
        "guided": _guided(guided),
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
    if plan.filed:
        check["detail"] = "queued as " + ", ".join(
            f"{job.job_id} under {job.handler_key}" for job in plan.filed
        )
        if plan.refused is not None:
            check["status"] = "fail"
            check["detail"] += f"; then not queued: {plan.refused.message}"
            check["remedy"] = str(plan.refused.remediation.remedy)
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
    elif plan.not_queued == NOTHING_NEW:
        check["status"] = "info"
        excluded = (plan.detail or {}).get("excluded") or {}
        tally: dict[str, int] = {}
        for said in excluded.values():
            tally[said["reason"]] = tally.get(said["reason"], 0) + 1
        listed = (plan.detail or {}).get("listed", 0)
        check["detail"] = (
            f"nothing new: {listed} playlist(s) listed and none queued"
            + (
                " (" + ", ".join(f"{n} {why}" for why, n in sorted(tally.items())) + ")"
                if tally
                else ""
            )
        )
    else:
        check["status"] = "info"
        check["detail"] = (
            "not queued: the confirmation was answered abort; the source's own "
            "verb asks the same question on its own"
        )
    # NOT ``said``, which the nothing new branch above binds as its loop name.
    noted = plan.note(plan.detail or {}) if plan.note is not None else None
    if noted:
        check["detail"] += f"; {noted}"
    return check


def _inbound_check(plan: _Plan, inbound: _Inbound) -> dict[str, Any]:
    """The read only half's own row, since the default output prints only checks."""
    from cratekit.sync import playlists

    source_id = plan.spec.source_id
    check: dict[str, Any] = {
        "key": f"sync.{source_id}.inbound",
        "title": f"{source_id} inbound",
        "status": "ok",
        "detail": "",
        "remedy": None,
    }
    if inbound.filed:
        check["detail"] = (
            "queued as "
            + ", ".join(f"{job.job_id} under {job.handler_key}" for job in inbound.filed)
            + f": the account's {inbound.hearts} heart(s), each resolved against the "
            "library whatever the confirmation's answer"
        )
    elif inbound.refused is not None:
        check["status"] = "fail"
        # LISTED AND THEN REFUSED AT THE QUEUE is a different fault from no listing.
        said = (
            "the account's hearts were not listed"
            if inbound.hearts is None
            else f"the account's {inbound.hearts} heart(s) were listed and not queued"
        )
        check["detail"] = f"{said}: {inbound.refused.message}"
        check["remedy"] = str(inbound.refused.remediation.remedy)
    elif inbound.not_queued == playlists.Excluded.IN_FLIGHT:
        check["status"] = "info"
        check["detail"] = (
            "not queued: the account's hearts are already being listed by "
            + ", ".join(inbound.open_jobs)
            + "; that job is resumed rather than a second one queued"
        )
    else:
        check["status"] = "info"
        check["detail"] = "not queued: the account lists no hearts"
    short = inbound.shortfall
    if short is not None:
        # A SHORT LISTING FAILS THE CHECK WHATEVER WAS QUEUED (R-504), the one
        # place a person learns the listing is not the whole account.
        check["status"] = "fail"
        if inbound.not_queued == playlists.Excluded.EMPTY:
            check["detail"] = "not queued: the provider served none of the account's hearts"
        check["detail"] += (
            f"; the listing came back short, {short.summary()}, which does not say which"
        )
    return check


def _report(
    plans: list[_Plan], run_id: str, guided: tuple[sources.SourceSpec, ...]
) -> dict[str, Any]:
    queued = [p for p in plans if _filed(p)]
    summary: dict[str, Any] = {
        "run_id": run_id,
        "queued": sum(len(_filed(p)) for p in queued),
        "sources": [p.spec.source_id for p in queued],
        "jobs": [
            {
                "source": p.spec.source_id,
                "job_id": job.job_id,
                "handler_key": job.handler_key,
            }
            for p in queued
            for job in _filed(p)
        ],
        "not_queued": {
            p.spec.source_id: p.not_queued for p in plans if p.not_queued is not None
        },
        # A GUIDED SOURCE IS NOT A SOURCE THAT FAILED TO QUEUE, so not ``not_queued``.
        "guided": _guided(guided),
    }
    for plan in plans:
        if plan.describe is not None:
            plan.detail = plan.describe(plan.filed)
        if plan.inbound is not None:
            plan.detail = {**(plan.detail or {}), "inbound": plan.inbound.block()}
        if plan.detail is not None:
            summary[plan.spec.source_id] = plan.detail
    checks: list[dict[str, Any]] = []
    for plan in plans:
        checks.append(_check(plan))
        if plan.inbound is not None:
            checks.append(_inbound_check(plan, plan.inbound))
    checks.extend(_guided_check(spec) for spec in guided)
    step = _next_step(plans, run_id)
    summary["next"] = step["command"] if step is not None else None
    if step is not None:
        checks.append(step["check"])
    return {"checks": checks, "summary": summary}


def _next_step(plans: list[_Plan], run_id: str) -> dict[str, Any] | None:
    """The one command that turns this pass's intake jobs into one list (U73).

    Named only when an intake job was filed, since ``intake missing --run``
    refuses a run with none. A check row, since the human output prints only checks.
    """
    from cratekit.intake import cli as intake_cli

    filed = [job for p in plans for job in _filed(p) if job.handler_key in intake_cli.INTAKE_KEYS]
    if not filed:
        return None
    command = f"crate intake missing --run {run_id}"
    return {
        "command": command,
        "check": {
            "key": "sync.next",
            "title": "next",
            "status": "info",
            "detail": (
                f"once the {len(filed)} intake job(s) this pass queued have finished, "
                f"write every track they found missing as one list with: {command}"
            ),
            "remedy": None,
        },
    }


def compose(ctx) -> tuple[dict[str, Any], Outcome, tuple[dict[str, str], ...]]:
    """Plan every enabled source, ask the one question, then queue. See the module doc."""
    cfg = _load()
    membership = cfg.membership()
    run_id = ctx.run.run_id
    enabled = sources.enabled_specs(membership)
    # A GUIDED SOURCE IS NEVER PLANNED (U109), so no provider is called for it.
    plans = [_plan(spec, ctx) for spec in enabled if spec.guided_by is None]
    guided = tuple(spec for spec in enabled if spec.guided_by is not None)

    for plan in plans:
        if plan.ask is not None:
            plan.ask(plans, guided)

    # THE READ ONLY HALF IS QUEUED BESIDE ITS SOURCE, not after the question,
    # so a declined or refused write half leaves it queued.
    ready: list[tuple[_Plan | _Inbound, Queue, list[jobs.Job]]] = []
    for p in plans:
        if p.queue is not None:
            ready.append((p, p.queue, p.filed))
        if p.inbound is not None and p.inbound.queue is not None:
            ready.append((p.inbound, p.inbound.queue, p.inbound.filed))
    if ready:
        with jobs.open_store() as store:
            for half, queue, filed in ready:
                # EACH ENQUEUE IS ITS OWN TRANSACTION. A refusal is recorded, not
                # raised, so filed jobs are named and a rerun does not duplicate them.
                try:
                    queue(store, cfg, run_id, filed)
                except CratekitError as exc:
                    half.refused, half.not_queued = exc.cause, exc.cause.reason

    data = _report(plans, run_id, guided)
    queued_any = any(_filed(p) for p in plans)
    refused = [
        cause
        for p in plans
        for cause in (p.refused, p.inbound.refused if p.inbound else None)
        if cause is not None
    ]
    if not queued_any and refused:
        # NOTHING QUEUED AND A SOURCE REFUSED. Not a no-op: the first source's
        # remedy is raised, with the whole pass in the detail.
        first = refused[0]
        # THE GUIDED LINE RIDES THE REFUSAL AS A LAST STEP (U109), since a
        # refusal carries no check rows; last, so the first step stays the fix.
        remediation = dataclasses.replace(
            first.remediation,
            steps=(*first.remediation.steps, *(_guided_step(spec) for spec in guided)),
        )
        raise CratekitError(
            dataclasses.replace(
                first,
                remediation=remediation,
                detail={**dict(first.detail or {}), "sources": data},
            )
        )

    warnings: list[dict[str, str]] = []
    for plan in plans:
        if plan.filed or plan.not_queued == NOTHING_NEW:
            warnings.extend(plan.warnings)
        if plan.refused is not None:
            warnings.append(
                {
                    "code": "sync-source-not-queued",
                    "message": f"{plan.spec.source_id}: {plan.refused.message}",
                }
            )
        if plan.inbound is not None and plan.inbound.refused is not None:
            warnings.append(
                {
                    "code": "sync-source-not-queued",
                    "message": (
                        f"{plan.spec.source_id} inbound: {plan.inbound.refused.message}"
                    ),
                }
            )
    # THE HONEST ZERO. Nothing refused and nothing queued is a no-op, not an ok.
    outcome = Outcome.OK if queued_any else Outcome.NO_OP
    return data, outcome, tuple(warnings)


def all_sources(ctx) -> Envelope:
    """Queue each enabled source's own increment and report every source."""
    data, outcome, warnings = compose(ctx)
    return ctx.envelope(data=data, outcome=outcome, warnings=warnings)
