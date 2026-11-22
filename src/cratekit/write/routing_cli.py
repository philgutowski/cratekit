"""The four ``route.*`` verbs: inbox, unplaced, resort, pending (U20).

The registry names ``cratekit.write.routing_cli`` and ``tests/_pending.py``
keys on that string, so the module stays here; the export path lives in
:mod:`cratekit.write.routing_export`. It imports :mod:`cratekit.cli.output`
alone, never ``cratekit.cli.registry``, which would be an upward import.

EVERY CLOSE GOES THROUGH :func:`cratekit.write.routing_pass.close_run`;
``session.close_session`` bypasses the gates that refuse a run still holding a
track nowhere, and a call of that name here is what the armed guard waits for.

Nothing about where a track goes is decided here: the placements come from
:func:`cratekit.write.rebuild.declared_membership`, the destinations from
``plan_destinations`` through the node map U36 recorded, so a re-run after a
rename converges, and the write from
:func:`cratekit.write.trees.write_tree_membership`. Every verb does the work it
reports (U53), and the database path plans before its gate (R-691).

Layer: write.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

from cratekit.cli.output import Envelope, load_config, no_job
from cratekit.core import (
    active_taxonomy,
    analysis_store,
    config,
    convergence,
    jobs,
    locations,
    rb_writer,
    session,
    taxonomy,
    tree_registry,
)
from cratekit.core.cause import CratekitError, Outcome, rebuilt, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.write import metadata_cli, rebuild, routing_pass, trees
from cratekit.write.routing_export import (
    UNPLACED_EXPORT_REMEDY,
    _column,
    _native_trees,
    _placed_counts,
    _plan,
    export_remedy,
    route_inbox_export,
    route_unplaced_export,
    unplaced_items,
)

#: The session log's name for a write this verb performed, one per verb and
#: none shared with the rebuild, so the log can say which act touched a library.
INBOX_WORKFLOW = "route-inbox"
RESORT_WORKFLOW = "route-resort"

#: Where a resort's job freezes the adds its gate showed and a person approved
#: (U219), and the database file that answer was pinned to (U161). Spelled
#: once, since the enqueue writes them and the resume and the worker read them.
RESORT_ADDS_KEY = "adds"
RESORT_DATABASE_KEY = "database"
RESORT_FACTS_KEY = "facts"

#: The digest source of the resort's gate, found by it and never by position.
RESORT_PLAN = "plan"

#: The warning a sweep over every native tree carries for a tree it left
#: alone because the taxonomy does not derive it (U219).
TREE_NOT_DERIVED = "tree-not-derived"

#: Where each resorted tree's report is committed, under the queue root beside
#: the job's lock and log (R-312). ONE REPORT PER ITEM, MADE DURABLE BY THE
#: DRIVER before the item flips to done, so what the engine measured survives a
#: killed process and reaches a resume that ends in a refusal.
RESORT_ARTIFACTS = jobs.Artifacts(final="resort-artifacts", staging="resort-staging")



def _routed_trees(
    entries: tree_registry.Registry, declared: taxonomy.Taxonomy
) -> tuple[str, ...]:
    """Every native tree the taxonomy derivation describes, in a stable order (U219).

    The items of a resort and the trees an inbox files into. A native tree the
    declaration names as something else, the intake flow above all, is left out.
    """
    return tuple(t for t in _native_trees(entries) if rebuild.derivable(declared, t))


def _passed_over(
    entries: tree_registry.Registry, declared: taxonomy.Taxonomy
) -> list[dict[str, str]]:
    """The warning naming each native tree a sweep left alone, and why (U219).

    Said rather than silent, so a person reads that the resort skipped it on purpose.
    """
    others = rebuild.other_declared_trees(declared)
    skipped = [t for t in _native_trees(entries) if t in others]
    if not skipped:
        return []
    named = ", ".join(f"{others[t]} ({t})" for t in skipped)
    return [
        {
            "code": TREE_NOT_DERIVED,
            "message": f"left alone: {named}, which holds what the verbs that "
            f"write it put there and not anything a tag decides, so the "
            f"taxonomy derives nothing for it",
        }
    ]


def _inbox_files(folder: Path) -> list[Path]:
    """Every file in the intake folder, sorted, dotfiles left out."""
    if not folder.is_dir():
        return []
    return [
        path
        for path in sorted(folder.iterdir())
        if path.is_file() and not path.name.startswith(".")
    ]


@dataclass(frozen=True)
class InboxPlan:
    """Where the database path puts each intake file, decided BEFORE the gate (R-691).

    ``items`` is what the digest covers and the person is shown, as display
    names. ``placements`` is the same decision in the engine's terms, one tuple
    per native tree, and is what the write consumes, so it cannot decide
    differently from the screen. ``declared`` and ``entries`` are carried so the
    write reads neither again; ``warnings`` are the planner's.
    """

    folder: Path
    items: list[dict[str, str]]
    entries: tree_registry.Registry
    native: tuple[str, ...]
    declared: taxonomy.Taxonomy
    placements: dict[str, tuple[rebuild.DeclaredPlacement, ...]]
    gaps: tuple[str, ...]
    warnings: list[dict[str, str]]


def plan_inbox(cfg: config.Config, declared: taxonomy.Taxonomy) -> InboxPlan:
    """Decide where every intake file goes, without opening the database.

    The readings, the derivation and the display names are taken here by the
    calls the write makes, so the screen and the write, and the two media, cannot
    disagree (R-691). The calibrated cut is read here so a corrupt one refuses
    before any write (U89), and only when something will be derived. A library
    with nothing native reads no file and carries the export remedy; an empty
    folder derives nothing either. One derivation per registry source.
    """
    folder = Path(cfg.library.root) / declared.intake.display
    files = _inbox_files(folder)
    entries = tree_registry.read(cfg)
    # THE ROUTED TREES, NOT EVERY NATIVE ONE (U219): filing into the native
    # intake tree put the routing tree's genre folders under INBOX.
    native = _routed_trees(entries, declared)
    placements: dict[str, tuple[rebuild.DeclaredPlacement, ...]] = {
        tree_id: () for tree_id in native
    }
    gaps: set[str] = set()
    warnings: list[dict[str, str]] = []
    if not native:
        warnings.append({"code": "no-native-tree", "message": export_remedy(declared)})
    elif files:
        threshold = metadata_cli.load_vocal_threshold(cfg)
        readings = [rebuild.read_truth(path) for path in files]
        derived: dict[
            tree_registry.DerivationSource | None,
            tuple[tuple[rebuild.DeclaredPlacement, ...], tuple[str, ...]],
        ] = {}
        for tree_id in native:
            source = entries.derivation_source(tree_id)
            if source not in derived:
                derived[source] = rebuild.declared_membership(
                    cfg, declared, tree_id=tree_id, source=source, vocal_threshold=threshold,
                    truth=readings,
                )
            placements[tree_id], not_derived = derived[source]
            gaps.update(not_derived)
    destined: dict[str, str] = {}
    vocal: dict[str, str] = {}
    genre: dict[str, str] = {}
    for placed in placements.values():
        for placement in placed:
            folder_name, sub = routing_pass.destination(declared, placement.bucket, placement.sub)
            named = _column(declared, placement, destined=destined, vocal=vocal, genre=genre)
            named.setdefault(placement.location, f"{folder_name}/{sub}")
    items = [
        {
            "path": str(path),
            "name": path.name,
            "destination": destined.get(str(path), ""),
            "vocal": vocal.get(str(path), ""),
            "genre": genre.get(str(path), ""),
        }
        for path in files
    ]
    return InboxPlan(
        folder=folder, items=items, entries=entries, native=native, declared=declared,
        placements=placements, gaps=tuple(sorted(gaps)), warnings=warnings,
    )


def _inbox_facts(plan: InboxPlan) -> dict[str, Any]:
    """The database gate's totals, counted off the items it lists (R-691).

    The same shape as the export gate's, naming the trees written, the dimensions
    not derived and the planner's warnings, so a total cannot disagree with the
    list under it.
    """
    return {
        "intake": str(plan.folder),
        "tracks": len(plan.items),
        **_placed_counts(plan.items),
        "trees": list(plan.native),
        "not derived": list(plan.gaps),
        "warnings": [warning["message"] for warning in plan.warnings],
    }



def _apply_gate(ctx, plan: dict, facts: dict[str, Any]) -> str:
    """Ask the apply gate over ``plan``, showing it whole (R-686).

    The gate shows the facts, the digest, the count and EVERY item the digest
    covers, unbounded, rendered by :func:`cratekit.cli.gates.shown_plan` through
    the run's resolver (R-693). The export gate's items also lead with artist and
    title (R-692). The export route asks this through the module, which tests patch.
    """
    spec = ctx.entry.gates[0]
    return ctx.gate.require(spec, plan=plan, context=facts)


def _close_run(record, cfg: config.Config):
    """The one close this surface may perform.

    Named so the AST walk that forbids ``close_session`` finds this call.
    """
    return routing_pass.close_run(record, cfg)


#: The evidence recorded when the routing pass proved an import. It names no
#: verb, since the record outlives one, and claims no row for an acknowledged track.
PLACED_EVIDENCE = (
    "the routing pass reached a row for every track this run landed that nobody "
    "acknowledged as gone"
)


def _close_if_settled(cfg: config.Config, session_id: str) -> None:
    for record in session.records(cfg):
        if record.session_id != session_id or record.terminal:
            continue
        if record.state is session.SessionState.AWAITING_IMPORT and _all_settled(
            cfg, session_id
        ):
            # AN INTAKE RUN ENDS ``awaiting-import`` (R-501), which the gated
            # close refuses. A row reached for every recorded track is stronger
            # proof than any export, so it is recorded; a run with no ROUTED
            # track proves nothing and is left for the close to refuse.
            session.mark_import_verified(record, cfg, evidence=PLACED_EVIDENCE)
        _close_run(record, cfg)
        return


def _all_settled(cfg: config.Config, session_id: str) -> bool:
    """True when nothing is outstanding for this run AND the pass reached a row for it.

    SETTLED IS NOT IMPORTED: an acknowledged track settles with no row, so at
    least one routed track is required before the pass proves an import.
    """
    ledger = routing_pass.read(cfg)
    routed = [
        entry
        for entry in ledger.intents
        if entry.session_id == session_id and entry.state is routing_pass.TrackState.ROUTED
    ]
    return bool(routed) and not ledger.outstanding(session_id)


def build_inbox(parser, entry) -> None:
    parser.add_argument(
        "--export",
        default=None,
        metavar="PATH",
        help="route the INBOX playlist of this fresh export and write "
        "<name>_routed.xml beside it, for a tree that has not cut over",
    )
    parser.set_defaults(_handler=route_inbox)


def build_unplaced(parser, entry) -> None:
    parser.add_argument(
        "--export",
        default=None,
        metavar="PATH",
        help="place every track the routing tree of this fresh export does not "
        "hold and write <name>_placed.xml beside it, for a tree that has not cut over",
    )
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
    """The command line that continues one queued resort.

    It carries ``--run`` (U219): the resort's gate is explicit, so the spawned
    child must name the run the answer was recorded against or it stalls, as
    ``tests/test_queued_resume_contract.py`` guards. The flag goes before the verb
    path, since it belongs to the root parser.
    """
    gate_run = (job.payload or {}).get(jobs.GATE_RUN_KEY)
    resume = ["--run", str(gate_run)] if gate_run else []
    return [*resume, "route", "resort", "--job", job.job_id]


#: The warning a confirmed apply carries for the files it could not file: the
#: code every routing write uses for "a write the tree could not take".
SKIPPED_WARNING = "route-write-skipped"

#: How many file names one skip warning spells out; the count is always whole.
SKIPPED_NAMED = 10

#: Why a file was not filed and what a person does about it, in the deferred
#: pass's vocabulary (R-318). Each sentence follows "was not filed because".
SKIP_NEXT_ACT: dict[routing_pass.Placement, str] = {
    routing_pass.Placement.NOT_IMPORTED: (
        "rekordbox holds no row for it yet. Import it into rekordbox, then run "
        "route inbox again"
    ),
    routing_pass.Placement.WITHDRAWN: (
        "it was imported and then removed in rekordbox. Import it again if it "
        "belongs in the library, or take it out of the intake folder"
    ),
    routing_pass.Placement.AMBIGUOUS: (
        "two or more collection rows claim its location. Remove the duplicate in "
        "rekordbox, then run route inbox again"
    ),
    routing_pass.Placement.UNRESOLVED: (
        "its location maps to no path this machine can read. Check the library "
        "root and the prefix map with crate doctor, then run route inbox again"
    ),
}


def _skipped_files(
    cfg: config.Config,
    rows: list[trees.ContentRow],
    skipped: dict[str, tuple[trees.RowMatch, list[str]]],
) -> list[dict[str, Any]]:
    """One record per file the write skipped, with the reason and the rows named.

    The writer's matcher sees live rows only, so its ``absent`` is two states:
    never imported and imported then removed. The rows are indexed again here,
    both halves, and the placement comes from :func:`routing_pass.row_placement`,
    the deferred pass's rule. One record per file, since every tree matches the
    same rows; ``trees`` says which ones it was declared into.
    """
    if not skipped:
        return []
    rules = [locations.PrefixRule(source, target) for source, target in cfg.resolved_prefix_map()]
    index = routing_pass.index_rows(rows, root=cfg.library.root, prefix_map=rules)
    paths = sorted(skipped)
    removed = trees.match_indexed_rows(
        paths, index.by_tombstoned_location, root=cfg.library.root, prefix_map=rules
    )
    out: list[dict[str, Any]] = []
    for path, dead in zip(paths, removed):
        alive, tree_ids = skipped[path]
        placement = routing_pass.row_placement(alive, dead)
        if placement is routing_pass.Placement.AMBIGUOUS:
            ids = alive.content_ids
        elif placement is routing_pass.Placement.WITHDRAWN:
            ids = dead.content_ids or ((dead.content_id,) if dead.content_id else ())
        else:
            ids = ()
        out.append(
            {
                "path": path,
                "reason": str(placement),
                # A SET: an additive sub-class files one file twice in one tree.
                "trees": sorted(set(tree_ids)),
                "content_ids": list(ids),
            }
        )
    return out


def skipped_warnings(records: list[dict[str, Any]]) -> list[dict[str, str]]:
    """The envelope warnings over ``skipped_files``, one per reason.

    The warnings are the human surface, since the default renderer prints no
    totals. Files are named by file name, sorted.
    """
    by_reason: dict[str, list[str]] = {}
    for record in records:
        by_reason.setdefault(record["reason"], []).append(Path(record["path"]).name)
    warnings: list[dict[str, str]] = []
    for reason in sorted(by_reason):
        names = sorted(by_reason[reason])
        named = names[:SKIPPED_NAMED]
        rest = len(names) - len(named)
        why = SKIP_NEXT_ACT[routing_pass.Placement(reason)]
        warnings.append(
            {
                "code": SKIPPED_WARNING,
                "message": (
                    f"{len(names)} file(s) in the intake folder were not filed because "
                    f"{why}. Not filed ({reason}): {'; '.join(named)}"
                    + (f"; and {rest} more" if rest else "")
                ),
            }
        )
    return warnings


def apply_inbox(cfg: config.Config, planned: InboxPlan) -> dict[str, Any]:
    """File the intake folder into every tree that has cut over.

    The placements are the ones :func:`plan_inbox` derived and the gate showed,
    consumed rather than remade (R-691); the destinations come from
    ``plan_destinations`` and the write from ``write_tree_membership``, which owns
    the session gates. A library with nothing native writes nothing and answers
    ``no-native-tree``: membership written for a tree on the XML bridge is
    overwritten by the next import.
    """
    entries = planned.entries
    native = planned.native
    if not native:
        return {
            "applied": False,
            "reason": "no-native-tree",
            "added": 0,
            "skipped": 0,
            "skipped_files": [],
        }
    declared = planned.declared
    added = 0
    skipped = 0
    # WHICH FILES, AND WHY, kept rather than counted (R-318).
    missed: dict[str, tuple[trees.RowMatch, list[str]]] = {}
    handle = rb_writer.open_db(cfg=cfg)
    try:
        known = {str(row.ID) for row in handle.get_playlist()}
        rows = list(routing_pass.content_rows(handle))
        for tree_id in native:
            placements = planned.placements[tree_id]
            root_id = tree_registry.anchored_root(
                tree_id, entries, root_exists=lambda root: root in known
            )
            standing = rebuild.read_tree(handle, root_id)
            # THE NODE MAP U36 RECORDED, so a re-run after a rename converges.
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
                # THE LIBRARY ROOT, as ``route_pending`` names it: ANLZ files
                # do not sit beside the audio, so a narrower root watches nothing.
                analysis_roots=analysis_store.watch_roots(cfg),
                workflow=INBOX_WORKFLOW,
            )
            added += report.added
            skipped += len(report.skipped)
            for match in report.skipped:
                missed.setdefault(match.requested, (match, []))[1].append(tree_id)
    finally:
        rb_writer.close_db(handle)
    return {
        "applied": True,
        "reason": None,
        "added": added,
        "skipped": skipped,
        "skipped_files": _skipped_files(cfg, rows, missed),
        "trees": len(native),
        # WHAT THE ENGINE DID NOT COMPARE, kept rather than dropped (R-316).
        "not_compared": planned.gaps,
    }


#: The no native tree warning for the deferred placements, which wait for a cutover.
PENDING_REMEDY = (
    "no tree has cut over, so no deferred placement can be made and none was "
    "read: these tracks are placed once a tree is database native. An import is "
    "proven by intake imported --export with a Fresh Export, not by this verb"
)


def route_inbox(ctx) -> Envelope:
    """Offer a plan for the intake folder, then apply it if the person says so.

    Written as "not apply" rather than "is abort", so only the one answer that
    means yes may write. With ``--export`` the intake is the export's and the
    write is a new file: see :func:`route_inbox_export`.
    """
    cfg = load_config(("routing_cli",))
    if ctx.args.export:
        return route_inbox_export(ctx, cfg, Path(ctx.args.export))
    # ONE READ PER VERB (R-685): the write files by the plan's declaration.
    planned = plan_inbox(cfg, active_taxonomy.load(cfg))
    items = planned.items
    plan = _plan(items, kind="inbox")
    option = _apply_gate(ctx, plan, _inbox_facts(planned))
    # THE PLANNER'S WARNINGS RIDE ON EVERY ANSWER, declined included.
    if option != "apply":
        return ctx.envelope(
            data=_plan(items, kind="inbox", applied=False),
            outcome=Outcome.NO_OP,
            warnings=planned.warnings,
        )
    if not items:
        # AN EMPTY FOLDER IS NOT A WRITE.
        return ctx.envelope(
            data=_plan(items, kind="inbox", applied=False, reason="inbox-empty"),
            outcome=Outcome.NO_OP,
            warnings=planned.warnings,
        )
    result = apply_inbox(cfg, planned)
    # THE GAPS RIDE AS A WARNING, NOT IN THE TOTALS, in the engine's words.
    not_compared = result.pop("not_compared", ())
    return ctx.envelope(
        data=_plan(items, kind="inbox", **result),
        outcome=Outcome.OK if result["applied"] else Outcome.NO_OP,
        warnings=(
            [{"code": "no-native-tree", "message": export_remedy(planned.declared)}]
            if result["reason"] == "no-native-tree"
            else [
                *rebuild.not_compared_warnings(not_compared),
                *skipped_warnings(result["skipped_files"]),
            ]
        ),
    )


def route_unplaced(ctx) -> Envelope:
    """Report tracks no governed tree places, or write a review of where they go.

    Without ``--export`` it is read only (R-313): no write intent and no session,
    so it is safe with rekordbox open. With ``--export`` it writes a review (U91,
    R-694): see :func:`route_unplaced_export`.
    """
    cfg = load_config(("routing_cli",))
    if ctx.args.export:
        return route_unplaced_export(ctx, cfg, Path(ctx.args.export))
    items, totals = unplaced_items(cfg)
    return ctx.envelope(
        data=_plan(items, kind="unplaced", **totals),
        outcome=Outcome.OK if totals["compared"] else Outcome.NO_OP,
        warnings=(
            [{"code": "no-native-tree", "message": UNPLACED_EXPORT_REMEDY}]
            if totals["reason"] == "no-native-tree"
            else []
        ),
    )


def _resume(ctx, store, job_id: str) -> Envelope:
    """Reconcile, refuse a foreign or itemless job, drive it, and report how it ended.

    Reconcile first, since a dead driver may have left a claim. The job has to be
    a resort, since ``handlers.run_job`` resolves the worker from the job row. A
    resort queued before U53 carries no items and would be walked to SUCCEEDED, so
    it refuses. A job that ended badly is not an ok exit (R-225), caught outside
    the ``is_open`` branch so a job failed on entry is caught too.
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
    # THE GATE IS ANSWERED FROM THE FROZEN PLAN (U219), never a fresh read: the
    # first tree may already hold its adds, and a fresh digest would stall.
    payload = job.payload or {}
    if job.is_open() and RESORT_ADDS_KEY not in payload:
        raise refuse(
            "resort-plan-stale",
            f"job {job.job_id} was queued by a build that showed no plan before "
            f"it, so there is nothing a person approved for it to write",
            remedy=Remedy.REPLAN_THEN_DECIDE,
            steps=(
                f"cancel it with: crate job cancel {job.job_id}",
                "then run the resort again, read its plan, and answer its gate",
            ),
            origin=("routing_cli",),
            detail={"job_id": job.job_id},
        )
    adds = [dict(row) for row in payload.get(RESORT_ADDS_KEY) or ()]
    option = ctx.gate.require(
        _resort_gate(ctx),
        plan=_plan(adds, kind="resort"),
        context=_resort_facts(adds, payload.get(RESORT_FACTS_KEY) or {}),
        pinned=_resort_pin(payload),
    )
    if option != "apply":
        return ctx.envelope(data=no_job("declined"), outcome=Outcome.NO_OP)
    warnings: tuple[dict[str, str], ...] = ()
    frozen: config.Config | None = None
    try:
        if job.is_open():
            if not jobs.items(store, job.job_id):
                raise refuse(
                    "internal-error",
                    f"job {job.job_id} has no tree to resort, so driving it would "
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
            # THE CUT THE WORKER WILL READ, read first (U89), so a corrupt
            # calibration refuses before any item is claimed.
            threshold = metadata_cli.load_vocal_threshold(jobs.frozen_config(job))
            declared = active_taxonomy.load(jobs.frozen_config(job))
            # FROM HERE THIS RUN DROVE, so from here a refusal owes the leftovers.
            frozen = jobs.frozen_config(job)
            # THE TREES THIS RUN DRIVES, read before the drive.
            driven = [
                i.item_id for i in jobs.items(store, job.job_id) if i.state != jobs.ItemState.DONE
            ]
            _, warnings = ctx.run_job(store, job)
            job = jobs.get(store, job.job_id)
            # THE SAME ENGINE AS THE REBUILD, SO THE SAME GAP (R-316), and the
            # leftovers (R-312), only on the branch that drove.
            records, listed_in = _left_behind(frozen, job.job_id)
            warnings = (
                *warnings,
                *rebuild.not_compared_warnings(
                    rebuild.governed_not_compared(threshold, declared)
                ),
                # The rebuild's engine, so the rebuild's skipped step (U132).
                *rebuild.favorites_skipped_warnings(declared, driven),
                *rebuild.left_behind_warnings(records, listed_in=listed_in),
                *_due_again_warnings(frozen, job.job_id),
            )
        jobs.raise_for_state(job)
    except CratekitError as failed:
        # BOTH EXITS carry the leftovers, once this run drove.
        if frozen is None:
            raise
        raise _with_left_behind(failed, frozen, job.job_id) from failed
    return ctx.envelope(data=jobs.reported(store, job), warnings=warnings)


def _resort_gate(ctx):
    """The resort's declared gate over its plan, found by digest source (U219).

    Refuses rather than defaulting: a resort whose entry lost its gate would queue
    writes nobody was shown.
    """
    for spec in ctx.entry.gates:
        if spec.digest_source == RESORT_PLAN:
            return spec
    raise refuse(
        "refused-by-policy",
        "route resort writes the routing tree and its registry entry declares no "
        "decision made against its plan, so there is nothing for a person to approve",
        remedy=Remedy.REPORT_DEFECT,
        origin=("routing_cli",),
        detail={"verb": ctx.entry.name},
    )


def _resort_pin(payload: dict[str, Any]) -> dict[str, str] | None:
    """The database file the answer is pinned to, when the plan read one."""
    opened = payload.get(RESORT_DATABASE_KEY)
    return {RESORT_DATABASE_KEY: str(opened)} if opened else None


def _resort_facts(adds: list[dict[str, str]], facts: dict[str, Any]) -> dict[str, Any]:
    """What the gate shows in front of the adds, counted off them (R-691's rule).

    The trees, the count, and the memberships the additive resort leaves where
    they are.
    """
    return {
        "trees": sorted({row["tree"] for row in adds}) or list(facts.get("trees") or ()),
        "adds": len(adds),
        "left behind": int(facts.get("left_behind") or 0),
        "not derived": list(facts.get("not_derived") or ()),
        "left alone": list(facts.get("left_alone") or ()),
    }


def route_resort(ctx) -> Envelope:
    """Show every add, ask, then queue the resort. Long work is a job, never an inline sweep.

    THE GATE FIRST (U219): the verb reads without writing, runs the rebuild's
    derivation and check, and shows every add by tree, folder, playlist and file,
    with the count it leaves behind. The answer is pinned to the database file
    read (U161), the adds are frozen in the job, and the worker refuses if they
    moved. Only the routed trees; another native tree is named in a warning
    (R-789). An empty plan still asks, then queues nothing.
    """
    cfg = load_config(("routing_cli",))
    if ctx.args.job:
        with jobs.open_store() as store:
            return _resume(ctx, store, ctx.args.job)
    declared = active_taxonomy.load(cfg)
    entries = tree_registry.read(cfg)
    routed = _routed_trees(entries, declared)
    warnings = _passed_over(entries, declared)
    adds: list[dict[str, str]] = []
    facts: dict[str, Any] = {"trees": list(routed)}
    opened: str | None = None
    if routed:
        threshold = metadata_cli.load_vocal_threshold(cfg)
        reports, opened = rebuild.preview_governed_trees(
            cfg, tree_ids=routed, vocal_threshold=threshold
        )
        for report in reports:
            adds.extend(rebuild.additions(report))
        facts["left_behind"] = sum(len(report.unexpected) for report in reports)
        facts["not_derived"] = sorted(
            {gap for report in reports for gap in report.not_compared}
        )
    facts["left_alone"] = [row["message"] for row in warnings]
    payload: dict[str, Any] = {RESORT_DATABASE_KEY: opened} if opened else {}
    option = ctx.gate.require(
        _resort_gate(ctx),
        plan=_plan(adds, kind="resort"),
        context=_resort_facts(adds, facts),
        pinned=_resort_pin(payload),
    )
    if option != "apply":
        return ctx.envelope(data=no_job("declined"), outcome=Outcome.NO_OP, warnings=warnings)
    if not routed:
        native = _native_trees(entries)
        return ctx.envelope(
            # A NATIVE TREE THE TAXONOMY DOES NOT DERIVE IS STILL NATIVE.
            data=no_job("no-derivable-tree" if native else "no-native-tree", native=len(native)),
            outcome=Outcome.NO_OP,
            warnings=warnings,
        )
    if not adds:
        return ctx.envelope(
            data=no_job("nothing-to-add", trees=len(routed)),
            outcome=Outcome.NO_OP,
            warnings=warnings,
        )
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={
                **payload,
                # THE APPROVED ADDS, FROZEN, for the resume's gate and the worker.
                RESORT_ADDS_KEY: adds,
                # And the facts the screen showed in front of them.
                RESORT_FACTS_KEY: facts,
                # THE GATE RUN, so the respawned child names it. See resort_argv.
                jobs.GATE_RUN_KEY: ctx.run.run_id,
            },
            # ONE TREE IS ONE ITEM, and only a tree with something to add.
            item_ids=tuple(sorted({row["tree"] for row in adds})),
            cfg=cfg,
        )
        return ctx.envelope(data=jobs.reported(store, job), warnings=warnings)


def handle_resort(job, item, cfg) -> None:
    """Re-place one governed tree from the declaration. The ``route.resort`` worker.

    It is the rebuild engine, additive by construction: a track moved by a genre
    or energy change stays in its old sub too, and the resume names what was left
    (R-312). The engine's own ``after`` check is kept as this item's report, the
    durable channel the driver owns. ``cfg`` is the job's frozen configuration
    (KTD9).
    """
    tree_id = str(item.item_id)
    report = rebuild.rebuild_governed_tree(
        cfg,
        tree_id=tree_id,
        workflow=RESORT_WORKFLOW,
        # THE CALIBRATED CUT, through the one loader, at the path the frozen
        # configuration names. None on a library never calibrated (U89, D7).
        vocal_threshold=metadata_cli.load_vocal_threshold(cfg),
        # THIS TREE'S APPROVED ADDS (U219), beyond which the engine refuses.
        approved=[
            dict(row)
            for row in (job.payload or {}).get(RESORT_ADDS_KEY) or ()
            if row.get("tree") == tree_id
        ],
    )
    left = rebuild.left_behind(report.after, active_taxonomy.load(cfg))
    return RESORT_ARTIFACTS.produced(
        cfg,
        job,
        item,
        {
            "tree_id": str(item.item_id),
            "left_behind": [rebuild.left_behind_record(entry) for entry in left],
            # WHAT CAME DUE ONLY FROM THIS RESORT'S OWN WRITES (U219).
            "due_again": len(report.after.missing),
        },
    )


def _left_behind(cfg: config.Config, job_id: str) -> tuple[list[dict[str, Any]], str]:
    """Every leftover this job's committed reports name, and where they are kept.

    Read back rather than accumulated, so a job continued by a second process
    names what the first one's trees left.
    """
    records = [
        entry
        for report in RESORT_ARTIFACTS.committed(cfg, job_id)
        for entry in report.get("left_behind") or ()
    ]
    return records, str(jobs.store_dir(cfg) / RESORT_ARTIFACTS.final / job_id)


#: The warning a resort carries when its own writes made adds due that its
#: plan could not show (U219).
DUE_AGAIN = "resort-again"


def _due_again_warnings(cfg: config.Config, job_id: str) -> list[dict[str, str]]:
    """Say that a second resort has more to show, and what stands until it runs.

    A resort writes only what its gate showed, so a favourite whose track it filed
    into a new folder waits for the next plan, and a tree a restore marked stays
    unconverged until then.
    """
    due: dict[str, int] = {}
    for report in RESORT_ARTIFACTS.committed(cfg, job_id):
        count = int(report.get("due_again") or 0)
        if count:
            due[str(report.get("tree_id"))] = due.get(str(report.get("tree_id")), 0) + count
    if not due:
        return []
    recorded = convergence.read(cfg)
    held = sorted(
        tree for tree in due if (record := recorded.tree(tree)) is not None and record.blocking
    )
    message = (
        f"{sum(due.values())} add(s) came due only from this resort's own writes, "
        f"a favourite whose track it filed into a new folder, so they were not on "
        f"its plan and were not written; run the resort again to see and file them"
    )
    if held:
        message += (
            f". Until then {', '.join(held)} stays unconverged and its writes refuse"
        )
    return [{"code": DUE_AGAIN, "message": message}]


def _with_left_behind(error: CratekitError, cfg: config.Config, job_id: str) -> CratekitError:
    """The same refusal, carrying what the trees that DID finish left behind.

    A partial failure is a resort's ordinary bad ending and leaves with no
    warnings, so the step is appended, through ``rebuilt`` so the cause keeps its
    type.
    """
    records, listed_in = _left_behind(cfg, job_id)
    message = rebuild.left_behind_message(records, listed_in=listed_in)
    if message is None:
        return error
    cause = error.cause
    return rebuilt(
        error,
        replace(
            cause,
            remediation=replace(
                cause.remediation, steps=(*cause.remediation.steps, message)
            ),
        ),
    )


def route_pending(ctx) -> Envelope:
    """Place tracks whose routing was decided before the library held a row.

    On a library with no outstanding intents this is a no-op: nothing is
    opened and no session is closed. On a library with no database native
    tree it is a no-op too, and says so. When a named session's outstanding
    set becomes empty, the run closes through :func:`_close_run`.
    """
    cfg = load_config(("routing_cli",))
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
    if not _native_trees(entries):
        # NOTHING WAS READ, SO NOTHING IS CLAIMED (R-436, R-501).
        return ctx.envelope(
            data=_plan(items, kind="pending"),
            outcome=Outcome.NO_OP,
            warnings=[{"code": "no-native-tree", "message": PENDING_REMEDY}],
        )

    declared = active_taxonomy.load(cfg)
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
