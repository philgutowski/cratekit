"""The four ``route.*`` verbs: inbox, unplaced, resort, pending (U20).

WHY THIS MODULE LIVES UNDER WRITE. The registry names
``cratekit.write.routing_cli``, and the countdown in ``tests/_pending.py``
keys on that string. A second path would leave the register armed over a
module that exists, which is a green countdown.

WHAT IT MUST NOT IMPORT. ``cratekit.cli.registry`` is the CLI layer. Naming
that type here is an upward import. The legal shape is the one
``cratekit.adopt.scan_cli`` uses: :mod:`cratekit.cli.output` alone, which is
foundation-ranked, and unannotated builder parameters.

EVERY CLOSE GOES THROUGH :func:`cratekit.write.routing_pass.close_run`.
``session.close_session`` is exported and bypasses the two gates that refuse
a run still holding a track nowhere or an export nobody has imported. A
call of that name in this file is the defect the armed guard is waiting for.

A RE-RUN AFTER A DESTINATION RENAME CONVERGES. The engine reads the node
map U36 recorded, through :func:`cratekit.write.rebuild.resolve_destinations`.
This surface does not build a second map.

THREE OF THE FOUR VERBS REPORTED WORK THEY HAD NOT DONE, until U53. ``inbox``
built a plan, asked its apply gate and returned the same plan whichever way
the person answered, so somebody who confirmed saw a plan and believed it had
happened. ``unplaced`` was the constant empty plan, which reads as "your
library is fully filed" on a library nobody had looked at. ``resort`` queued a
job with no items, which the driver walks in one empty pass and transitions
straight to succeeded. All three are the same failure wearing three faces: a
green report over an act nobody performed.

WHAT THE APPLY WRITES IS NOT A SECOND ROUTER. The intake files are read for
their tags, the placements come from
:func:`cratekit.write.rebuild.declared_membership` through the derivation the
REGISTRY records for the tree, the destinations resolve through
:func:`cratekit.write.rebuild.plan_destinations`, and the write goes through
:func:`cratekit.write.trees.write_tree_membership`, which owns the session
gates. Nothing about where a track goes is decided in this file.

Layer: write.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from cratekit.cli.output import Envelope, digest_of
from cratekit.core import (
    analysis_store,
    config,
    convergence,
    jobs,
    rb_writer,
    session,
    taxonomy,
    tree_registry,
)
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.write import rebuild, routing_pass, trees

#: The session log's name for a write this verb performed, one per verb, so a
#: person reading the log can tell which act touched their library. Not shared
#: with the rebuild's own workflow: two verbs writing under one name is a log
#: that cannot answer the only question anybody asks it.
INBOX_WORKFLOW = "route-inbox"
RESORT_WORKFLOW = "route-resort"


def _load() -> config.Config:
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=("routing_cli",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def _plan(items: list[dict[str, str]], *, kind: str, **totals: Any) -> dict:
    """The plan envelope, with the digest taken over the ITEMS alone.

    THE EXTRA TOTALS ARE OUTSIDE THE DIGEST ON PURPOSE. A decision is bound to
    the digest of the plan it was made against, and the totals carry what this
    run did or could not do rather than what it offered, so folding them in would
    make an answer stale for a reason that has nothing to do with the offer.

    ``plan/1`` forbids properties it does not name, so anything a caller needs
    beyond the item list rides here rather than beside it.
    """
    digest = digest_of({"kind": kind, "items": items})
    return {
        "digest": digest,
        "items": items,
        "totals": {"count": len(items), **totals},
        "chunk": None,
    }


def _native_trees(entries: tree_registry.Registry) -> tuple[str, ...]:
    """Every tree that has cut over, in a stable order. The items of a resort."""
    return tuple(sorted(t for t in entries.tree_ids() if entries.is_database_native(t)))


def _no_op(state: str, **progress: Any) -> dict[str, Any]:
    """A run that correctly queued nothing. ``job_id`` is "" because the schema
    types it as a string (R-234)."""
    return {"job_id": "", "state": state, "cause": None, "progress": dict(progress)}


def _inbox_items(cfg: config.Config) -> list[dict[str, str]]:
    declared = taxonomy.default_taxonomy()
    folder = Path(cfg.library.root) / declared.intake.display
    if not folder.is_dir():
        return []
    items: list[dict[str, str]] = []
    for path in sorted(folder.iterdir()):
        if path.is_file() and not path.name.startswith("."):
            items.append({"path": str(path), "name": path.name})
    return items


def _apply_gate(ctx, plan: dict) -> str:
    spec = ctx.entry.gates[0]
    return ctx.gate.require(spec, digest=plan["digest"])


def _close_run(record, cfg: config.Config):
    """The one close this surface may perform.

    Named so the AST walk that forbids ``close_session`` finds this call and
    not a bypass.
    """
    return routing_pass.close_run(record, cfg)


def _close_if_settled(cfg: config.Config, session_id: str) -> None:
    for record in session.records(cfg):
        if record.session_id != session_id or record.terminal:
            continue
        _close_run(record, cfg)
        return


def _reported(store, job) -> dict:
    return {
        "job_id": job.job_id,
        "state": str(job.state),
        "cause": job.cause.to_json() if job.cause is not None else None,
        "progress": jobs.progress(store, job.job_id),
    }


def build_inbox(parser, entry) -> None:
    parser.set_defaults(_handler=route_inbox)


def build_unplaced(parser, entry) -> None:
    parser.set_defaults(_handler=route_unplaced)


def build_resort(parser, entry) -> None:
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="continue the resort already queued under this identifier",
    )
    parser.set_defaults(_handler=route_resort)


def build_pending(parser, entry) -> None:
    parser.add_argument(
        "--session",
        default=None,
        metavar="SESSION_ID",
        help="place outstanding tracks for this run only; every open run by default",
    )
    parser.set_defaults(_handler=route_pending)


def resort_argv(job) -> list[str]:
    return ["route", "resort", "--job", job.job_id]


def apply_inbox(cfg: config.Config, items: list[dict[str, str]]) -> dict[str, Any]:
    """File the intake folder into every tree that has cut over.

    THE ONE THING THIS FUNCTION EXISTS FOR is that it is the call the confirmed
    branch was missing. Everything it does is a call into an engine that already
    owns the rule: the tag readings come from
    :func:`cratekit.write.rebuild.read_truth`, the placements from
    ``declared_membership`` through the derivation the registry records, the
    destinations from ``plan_destinations``, and the write from
    ``write_tree_membership``, which takes the acknowledgment, the volume
    identity, the session lock, the verified capture and the analysis watch.

    A LIBRARY WITH NOTHING NATIVE WRITES NOTHING AND SAYS SO. Every tree is on
    the XML bridge until its cutover, and membership written into the database
    for one of those is membership the next import overwrites. Reported as its
    own answer rather than as an empty success, because "nothing needed doing"
    and "there is nowhere to put this yet" are different sentences with different
    remedies.

    THE READINGS ARE TAKEN ONCE AND REUSED FOR EVERY TREE. ``read_truth`` never
    raises for an unreadable file, so a stray file in the intake folder routes to
    the declared fallback and is visible in the result rather than abandoning the
    run.
    """
    entries = tree_registry.read(cfg)
    native = _native_trees(entries)
    if not native:
        return {"applied": False, "reason": "no-native-tree", "added": 0, "skipped": 0}
    readings = [rebuild.read_truth(Path(item["path"])) for item in items]
    declared = taxonomy.default_taxonomy()
    added = 0
    skipped = 0
    handle = rb_writer.open_db(cfg=cfg)
    try:
        known = {str(row.ID) for row in handle.get_playlist()}
        rows = list(routing_pass.content_rows(handle))
        for tree_id in native:
            placements, _gaps = rebuild.declared_membership(
                cfg,
                declared,
                source=entries.derivation_source(tree_id),
                # NO CALIBRATION IS READ HERE, the same answer the convergence
                # report gives: nothing in this build reads the calibration file,
                # and a number picked here would be this surface answering a
                # question about somebody's library on their behalf.
                vocal_threshold=None,
                truth=readings,
            )
            root_id = tree_registry.anchored_root(
                tree_id, entries, root_exists=lambda root: root in known
            )
            standing = rebuild.read_tree(handle, root_id)
            # THE NODE MAP U36 RECORDED, read rather than rebuilt, which is what
            # makes a re-run after a destination rename converge on the same
            # playlist instead of creating a second one.
            record = convergence.read(cfg).tree(tree_id)
            _destinations, plan = rebuild.plan_destinations(
                declared, placements, standing, record, tree_id=tree_id
            )
            report = trees.write_tree_membership(
                cfg,
                handle,
                tree_id=tree_id,
                registry=entries,
                plan=plan,
                rows=rows,
                root_exists=lambda root: root in known,
                # THE LIBRARY ROOT, which is what ``route_pending`` twelve
                # functions below already names and for the same reason: the
                # watch walks for ANLZ files by name and those do not sit beside
                # the audio, so naming a narrower directory arms a watch over
                # nothing and reports a clean session whatever happened to the
                # grids. The empty-list refusal cannot catch that, because a
                # barren list is not an empty one.
                analysis_roots=analysis_store.watch_roots(cfg),
                workflow=INBOX_WORKFLOW,
            )
            added += report.added
            skipped += len(report.skipped)
    finally:
        rb_writer.close_db(handle)
    return {
        "applied": True,
        "reason": None,
        "added": added,
        "skipped": skipped,
        "trees": len(native),
    }


def route_inbox(ctx) -> Envelope:
    """Offer a plan for the intake folder, then apply it if the person says so.

    THE BRANCH IS WRITTEN AS "not apply" RATHER THAN AS "is abort", which is the
    same direction the readiness answers in :mod:`cratekit.write.routing_pass`
    are derived in and for the same reason: only the one answer that means yes
    may write, so an option added to this gate later cannot acquire the writing
    behaviour by nobody having classified it.
    """
    cfg = _load()
    items = _inbox_items(cfg)
    plan = _plan(items, kind="inbox")
    option = _apply_gate(ctx, plan)
    if option != "apply":
        return ctx.envelope(data=_plan(items, kind="inbox", applied=False), outcome=Outcome.NO_OP)
    if not items:
        # AN EMPTY FOLDER IS NOT A WRITE. Nothing is opened, no session is taken
        # and the declaration is never derived, which is what makes this true on
        # the disk rather than approximately true.
        return ctx.envelope(
            data=_plan(items, kind="inbox", applied=False, reason="inbox-empty"),
            outcome=Outcome.NO_OP,
        )
    result = apply_inbox(cfg, items)
    return ctx.envelope(
        data=_plan(items, kind="inbox", **result),
        outcome=Outcome.OK if result["applied"] else Outcome.NO_OP,
    )


def unplaced_items(cfg: config.Config) -> tuple[list[dict[str, str]], dict[str, Any]]:
    """Every active collection row that no governed tree holds, and the totals.

    THE QUESTION IS ASKED OF THE DATABASE, not answered with a constant. Until
    U53 this was ``_plan([], ...)``, which reports "your library is fully filed"
    for a library nobody looked at, and no green suite can tell that apart from a
    library that really is filed.

    COVERAGE IS MEMBERSHIP UNDER THE GOVERNED ROOT, read by walking DOWN from the
    adopted root identifier through :func:`cratekit.write.rebuild.read_tree`,
    never by finding a folder with the declared name. A walk by name finds a
    namesake anywhere in the library and reports on that instead.

    A LIBRARY WITH NOTHING NATIVE IS NOT COMPARED, and the totals say so. An
    empty answer there would be the constant defect arriving by a different
    route: nothing was read, so nothing about the tree was learned.
    """
    entries = tree_registry.read(cfg)
    native = _native_trees(entries)
    if not native:
        return [], {"compared": False, "reason": "no-native-tree", "collection": 0}
    handle = rb_writer.open_db(cfg=cfg)
    try:
        known = {str(row.ID) for row in handle.get_playlist()}
        rows = list(routing_pass.content_rows(handle))
        held: set[str] = set()
        for tree_id in native:
            root_id = tree_registry.anchored_root(
                tree_id, entries, root_exists=lambda root: root in known
            )
            for node in rebuild.read_tree(handle, root_id):
                held |= set(node.content_ids)
    finally:
        rb_writer.close_db(handle)
    # THE TOMBSTONED HALF IS NOT UNPLACED. A row rekordbox has soft-deleted is
    # not a track waiting to be filed, and reporting one would send somebody to
    # place something they removed on purpose.
    active = [row for row in rows if not row.deleted]
    items = [
        {"content_id": row.content_id, "path": row.recorded}
        for row in active
        if row.content_id not in held
    ]
    return items, {
        "compared": True,
        "reason": None,
        "collection": len(active),
        "trees": len(native),
    }


def route_unplaced(ctx) -> Envelope:
    """Report tracks no governed tree places, read off the library."""
    cfg = _load()
    items, totals = unplaced_items(cfg)
    return ctx.envelope(
        data=_plan(items, kind="unplaced", **totals),
        outcome=Outcome.OK if totals["compared"] else Outcome.NO_OP,
    )


def _resume(ctx, store, job_id: str) -> Envelope:
    """Reconcile, refuse a foreign or itemless job, drive it, and report how it ended.

    RECONCILE FIRST, because a resume arrives after something stopped and a claim
    a dead driver left behind is state the queue cannot see for itself.

    THE JOB HAS TO BE A RESORT. ``handlers.run_job`` resolves the worker from the
    JOB ROW rather than from this verb, and this verb takes no other required
    input, so without this line any queued job of any verb could be driven
    through it, under this envelope and without that verb's own resume checks.

    THE ZERO ITEM RULE ON THE RESUME SIDE. A resort queued by any build before
    U53 carries no items, and ``jobs.drive`` walks an itemless job in one empty
    pass and records it SUCCEEDED, which is the defect this unit closed arriving
    through the one door that predates the fix.

    A JOB THAT ENDED BADLY IS NOT AN OK EXIT, which is R-225. ``drive`` raises
    only when EVERY attempted item failed, and this verb queues one item per
    governed tree, so a partial failure is the ordinary shape here rather than
    the edge one: without this an exit of 0 covers a sweep that finished half a
    library. It sits outside the ``is_open`` branch so a job already failed on
    entry is caught too.
    """
    job = jobs.reconcile(store, job_id)
    if job.handler_key != ctx.entry.handler_key:
        raise refuse(
            "job-unknown",
            f"job {job.job_id} was queued for {job.handler_key!r}, which is not a "
            f"resort, so this verb will not drive it",
            remedy=Remedy.FIX_COMMAND_LINE,
            steps=("resume this job through the verb that queued it, or through the "
                   "job resume verb, which reads the worker off the job itself",),
            origin=("routing_cli",),
            detail={"job_id": job.job_id, "handler": job.handler_key},
        )
    warnings: tuple[dict[str, str], ...] = ()
    if job.is_open():
        if not jobs.items(store, job.job_id):
            raise refuse(
                "internal-error",
                f"job {job.job_id} has no tree to re-place, so driving it would "
                f"report a resort that swept a library nothing read. It was queued "
                f"by a build that did not record its items",
                remedy=Remedy.REPORT_DEFECT,
                steps=(
                    "cancel this job, then queue the resort again, which records "
                    "one item per governed tree",
                ),
                origin=("routing_cli",),
                detail={"job_id": job.job_id},
            )
        _, warnings = ctx.run_job(store, job)
        job = jobs.get(store, job.job_id)
    if not job.is_open() and job.cause is not None:
        raise CratekitError(job.cause)
    return ctx.envelope(data=_reported(store, job), warnings=warnings)


def route_resort(ctx) -> Envelope:
    """Queue a resort. Long work is a job, never an inline sweep.

    ONE TREE IS ONE ITEM, and until U53 this queued none. A job with nothing to
    claim is walked by the driver in a single empty pass and transitioned to
    succeeded, so the queue reported a resort that swept a library nothing read.

    A LIBRARY WITH NOTHING NATIVE FILES NO JOB AT ALL, and that is not a refusal:
    a library that has never flipped a tree has nothing to re-place, which is
    ordinary rather than wrong.
    """
    cfg = _load()
    with jobs.open_store() as store:
        if ctx.args.job:
            return _resume(ctx, store, ctx.args.job)
        items = _native_trees(tree_registry.read(cfg))
        if not items:
            return ctx.envelope(
                data=_no_op("no-native-tree", native=0),
                outcome=Outcome.NO_OP,
            )
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={},
            item_ids=items,
            cfg=cfg,
        )
        return ctx.envelope(data=_reported(store, job))


def handle_resort(job, item, cfg) -> None:
    """Re-place one governed tree from the declaration. The ``route.resort`` worker.

    IT IS THE REBUILD ENGINE, and calling it anything else would be this file
    claiming a second router. A genre or an energy change moves where the
    declaration puts a track, and re-deriving the declaration and writing back
    what the database lacks is exactly what that costs on the additive side.

    WHAT IT DOES NOT DO IS TAKE THE TRACK OUT OF WHERE IT WAS. The membership
    writer is additive by construction, so after a genre change the track is in
    its new sub AND still in its old one until somebody removes it. The engine's
    report names those as unexpected differences, so the state is visible rather
    than silent, and this build has no database removal path to offer.

    ``cfg`` is the configuration this job was FROZEN against (KTD9). Nothing here
    loads one.
    """
    del job
    rebuild.rebuild_governed_tree(cfg, tree_id=str(item.item_id), workflow=RESORT_WORKFLOW)
    return None


def route_pending(ctx) -> Envelope:
    """Place tracks whose routing was decided before the library held a row.

    On a library with no outstanding intents this is a no-op: nothing is
    opened and no session is closed. When a named session's outstanding
    set becomes empty, the run closes through :func:`_close_run`.
    """
    cfg = _load()
    ledger = routing_pass.read(cfg)
    wanted = ctx.args.session
    session_ids = (
        (wanted,)
        if wanted
        else tuple(sorted({entry.session_id for entry in ledger.outstanding()}))
    )
    if not session_ids:
        return ctx.envelope(data=_plan([], kind="pending"), outcome=Outcome.NO_OP)

    items = [{"session_id": session_id} for session_id in session_ids]
    entries = tree_registry.read(cfg)
    native = [
        tree_id for tree_id in entries.tree_ids() if entries.is_database_native(tree_id)
    ]
    if not native:
        return ctx.envelope(data=_plan(items, kind="pending"), outcome=Outcome.OK)

    declared = taxonomy.default_taxonomy()
    handle = rb_writer.open_db(cfg=cfg)
    try:
        known = {str(row.ID) for row in handle.get_playlist()}
        rows = list(routing_pass.content_rows(handle))
        for session_id in session_ids:
            if not routing_pass.read(cfg).outstanding(session_id):
                _close_if_settled(cfg, session_id)
                continue
            routing_pass.route(
                cfg,
                handle,
                session_id=session_id,
                registry=entries,
                declared=declared,
                rows=rows,
                root_exists=lambda root_id: root_id in known,
                analysis_roots=analysis_store.watch_roots(cfg),
            )
            if not routing_pass.read(cfg).outstanding(session_id):
                _close_if_settled(cfg, session_id)
    finally:
        rb_writer.close_db(handle)
    return ctx.envelope(data=_plan(items, kind="pending"), outcome=Outcome.OK)
