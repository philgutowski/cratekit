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

THE DATABASE PATH PLANS BEFORE ITS GATE, since R-691. :func:`plan_inbox`
takes the readings and the placements first, the gate shows each file's
destination, the digest binds those destinations, and :func:`apply_inbox`
writes the plan it was handed rather than deriving a second one after the
answer.

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

#: The session log's name for a write this verb performed, one per verb, so a
#: person reading the log can tell which act touched their library. Not shared
#: with the rebuild's own workflow: two verbs writing under one name is a log
#: that cannot answer the only question anybody asks it.
INBOX_WORKFLOW = "route-inbox"
RESORT_WORKFLOW = "route-resort"

#: Where a resort's job freezes the adds its gate showed and a person approved
#: (U219), and the database file that answer was pinned to (U161). Spelled
#: once, because the enqueue writes them and the resume and the worker read
#: them, and a key one side spells differently is a plan nobody can match.
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
#: killed process and reaches a resume that ends in a refusal. The first version
#: of this kept it in a dict in memory, and the built in review named the two
#: runs that loses: the one a partial failure ends, and the one that died.
RESORT_ARTIFACTS = jobs.Artifacts(final="resort-artifacts", staging="resort-staging")



def _routed_trees(
    entries: tree_registry.Registry, declared: taxonomy.Taxonomy
) -> tuple[str, ...]:
    """Every native tree the taxonomy derivation describes, in a stable order (U219).

    THE ITEMS OF A RESORT AND THE TREES AN INBOX FILES INTO. A native tree the
    declaration names as something else, the intake flow above all, is left
    out: its membership is what the verbs that write it put there, and the
    derivation refuses it by name (:func:`cratekit.write.rebuild.assert_derivable`).
    """
    return tuple(t for t in _native_trees(entries) if rebuild.derivable(declared, t))


def _passed_over(
    entries: tree_registry.Registry, declared: taxonomy.Taxonomy
) -> list[dict[str, str]]:
    """The warning naming each native tree a sweep left alone, and why (U219).

    Said rather than silent, so a person whose intake tree has cut over reads
    that the resort did not touch it on purpose, and not that it forgot.
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

    ``items`` is what the digest is taken over and what the person is shown:
    each file's path and name, the folder and sub it files into, and the vocal
    sub it also files into, as display names. ``placements`` is the same
    decision in the engine's own terms, one tuple per tree that has cut over,
    every native tree present even when the folder is empty, and it is what
    the write consumes, so the write cannot decide differently from what the
    screen said. ``declared`` and ``entries`` are the declaration and the
    registry the decision was made against, carried so the write reads neither
    a second time. ``warnings`` are what the planner knew before the question
    was asked.
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

    THE PLAN USED TO BE THE FILE LIST, and the routing was decided inside the
    apply after the gate, so a person answered a placement they could not read
    (R-691). Now the readings, the derivation and the display names are all
    taken here, by the calls the write makes: the readings come from
    :func:`cratekit.write.rebuild.read_truth`, the placements from
    ``declared_membership`` through the derivation the REGISTRY records for
    each tree that has cut over, and the display names from
    :func:`cratekit.write.routing_pass.destination`, which is what the export
    path's :func:`_decide` names its destinations with. So the two media, and
    the screen and the write, cannot disagree about where a track goes.

    THE CALIBRATED CUT IS READ HERE, before the database is opened, so a
    corrupt calibration refuses before anything is written (U89). None on a
    library never calibrated, and the derivation then names the dimension it
    left out in ``gaps``. It is read only when something will be derived, so
    a library with nothing native still gets the export remedy, the answer
    that applies to it, and not a calibration refusal over a cut it cannot
    use.

    A LIBRARY WITH NOTHING NATIVE DERIVES NOTHING, AND READS NO FILE. There is
    no registry source to derive by and no tree the write would take, so
    every file is listed with no destination and the export remedy rides as a
    warning, on the screen before the answer rather than in the envelope after
    it. The apply still answers ``no-native-tree`` for it, as it always did.

    AN EMPTY FOLDER DERIVES NOTHING EITHER. The derivation refuses an empty
    result as evidence of nothing, and an empty folder is not that: it is the
    ``inbox-empty`` answer the verb gives after the gate, with nothing opened.

    ONE DERIVATION PER SOURCE. Two trees that cut over on the same registry
    source derive the same placements from the same readings, so the rules
    run once per source and each tree is mapped to its source's tuple.
    """
    folder = Path(cfg.library.root) / declared.intake.display
    files = _inbox_files(folder)
    entries = tree_registry.read(cfg)
    # THE ROUTED TREES, NOT EVERY NATIVE ONE (U219). The intake tree is native
    # on a library whose landings write it, and filing the intake folder into
    # it put the routing tree's genre folders under INBOX, the shape sitting
    # 61 found through the resort. The derivation refuses that tree by name;
    # this is where the verb stops asking it to.
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
                    cfg,
                    declared,
                    tree_id=tree_id,
                    source=source,
                    vocal_threshold=threshold,
                    truth=readings,
                )
            placements[tree_id], not_derived = derived[source]
            gaps.update(not_derived)
    destined: dict[str, str] = {}
    vocal: dict[str, str] = {}
    genre: dict[str, str] = {}
    for placed in placements.values():
        for placement in placed:
            folder_name, sub = routing_pass.destination(
                declared, placement.bucket, placement.sub
            )
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
        folder=folder,
        items=items,
        entries=entries,
        native=native,
        declared=declared,
        placements=placements,
        gaps=tuple(sorted(gaps)),
        warnings=warnings,
    )


def _inbox_facts(plan: InboxPlan) -> dict[str, Any]:
    """The database gate's totals, counted off the items it lists (R-691).

    The same shape as :func:`_export_facts`, for the same reason: a total
    counted from the list cannot disagree with the list printed under it. The
    trees the write goes into are named, since on this medium the destination
    is a playlist in the database and not a file. ``not derived`` and the
    warnings ride for the reason the export's do: an empty vocal column on an
    uncalibrated library means the dimension was not read, and a file with no
    destination on a library with nothing native has its reason on the same
    screen as the question.
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

    The gate layer shows the facts, then the digest, the count and EVERY ITEM
    the digest was taken over, so the screen is the plan a person approves and
    a JSON reader can compare it with the declined run's items, which this
    verb returns as its no-op's data. The export
    gate hands in its plan through :func:`_named`, so each of its items also
    leads with the track's artist and title, which a reader drops to compare
    (R-692). Without this the gate carried the question and the options and
    not one item, and a person answered a routing plan they could not read.
    There is no bound: the digest covers every item, and a list cut short
    would ask for approval of items nobody was shown. The body that renders
    it is :func:`cratekit.cli.gates.shown_plan`, shared with every other
    digest bound gate since R-693, and reached through the run's gate
    resolver because this layer may not import the CLI's.
    """
    spec = ctx.entry.gates[0]
    return ctx.gate.require(spec, plan=plan, context=facts)


def _close_run(record, cfg: config.Config):
    """The one close this surface may perform.

    Named so the AST walk that forbids ``close_session`` finds this call and
    not a bypass.
    """
    return routing_pass.close_run(record, cfg)


#: What is recorded as the evidence when the routing pass is what proved an
#: import. No verb is named, because the record outlives any one verb's name.
#: It says what was seen and no more: a track a person acknowledged as gone
#: reached no row, and the sentence does not claim it did.
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
            # AN INTAKE RUN NOW ENDS ``awaiting-import`` (R-501), and the gated
            # close refuses that state. Here the pass has reached a row for
            # every track the run recorded, which is stronger proof of the
            # import than any export, so the proof is recorded and the close
            # goes ahead. A run with no ROUTED track proves nothing, and is
            # left for the close to refuse.
            session.mark_import_verified(record, cfg, evidence=PLACED_EVIDENCE)
        _close_run(record, cfg)
        return


def _all_settled(cfg: config.Config, session_id: str) -> bool:
    """True when nothing is outstanding for this run AND the pass reached a row for it.

    SETTLED IS NOT IMPORTED. A track settles by being routed, which takes a
    row, or by a person acknowledging it is gone, which takes none. A run whose
    every track was acknowledged settled without any import, so at least one
    routed track is required before the pass counts as proof of one.
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

    IT CARRIES ``--run`` (U219). The resort's gate is explicit, so the child
    the job engine spawns has to name the run the answer was recorded against,
    or it meets the gate with nothing recorded and stalls for ever, which is
    the shape ``tests/test_queued_resume_contract.py`` guards. The flag goes
    before the verb path because ``--run`` belongs to the root parser. A job
    an older build queued carries no gate run and resumes without it.
    """
    gate_run = (job.payload or {}).get(jobs.GATE_RUN_KEY)
    resume = ["--run", str(gate_run)] if gate_run else []
    return [*resume, "route", "resort", "--job", job.job_id]


#: The warning a confirmed apply carries for the files it could not file. The
#: code every other routing write already uses for "a write the tree could not
#: take", so a consumer filtering on it sees this one too.
SKIPPED_WARNING = "route-write-skipped"

#: How many file names one skip warning spells out. The count is always the
#: whole set, and the payload's ``skipped_files`` lists every one.
SKIPPED_NAMED = 10

#: Why a file was not filed and what a person does about it, one per placement a
#: skip can carry. The vocabulary is the deferred pass's own (R-318), so the two
#: surfaces say one thing about one state. Each sentence follows "was not filed
#: because".
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

    THE WRITER'S MATCHER SEES LIVE ROWS ONLY, so its ``absent`` is two different
    states: a file never imported and a file imported then removed. The rows are
    indexed again here, both halves, with the root and the prefix map the writer
    used, and the placement comes from :func:`routing_pass.row_placement`, the
    rule the deferred pass reports with.

    ONE RECORD PER FILE, NOT PER TREE. Every tree matches against the same rows,
    so a file's reason cannot differ between trees; ``trees`` says which ones it
    was declared into.
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
                # A SET, because an additive sub-class declares one file into
                # two playlists of one tree and the writer skips it twice.
                "trees": sorted(set(tree_ids)),
                "content_ids": list(ids),
            }
        )
    return out


def skipped_warnings(records: list[dict[str, Any]]) -> list[dict[str, str]]:
    """The envelope warnings over ``skipped_files``, one per reason.

    THE WARNINGS ARE THE HUMAN SURFACE. The default renderer prints warnings and
    no totals, so a reason carried only in the payload reaches a script and never
    the person who confirmed the apply. Files are named by their file name, which
    is what a person looks for in the intake folder, and the full path is in the
    payload. Sorted, so two runs over one state say one thing.
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

    THE ONE THING THIS FUNCTION EXISTS FOR is that it is the call the confirmed
    branch was missing. Everything it does is a call into an engine that already
    owns the rule: the placements are the ones :func:`plan_inbox` derived and
    the gate showed, the destinations come from ``plan_destinations``, and the
    write from ``write_tree_membership``, which takes the acknowledgment, the
    volume identity, the session lock, the verified capture and the analysis
    watch.

    THE PLAN IS CONSUMED, NOT REMADE (R-691). The readings, the declaration,
    the cut and the placements are the plan's, so what is written is what the
    digest bound and the person read. Deriving again here would be a second
    decision that agrees with the first until the folder or the declaration
    moves between the two, at which point the screen and the write would part.

    A LIBRARY WITH NOTHING NATIVE WRITES NOTHING AND SAYS SO. Every tree is on
    the XML bridge until its cutover, and membership written into the database
    for one of those is membership the next import overwrites. Reported as its
    own answer rather than as an empty success, because "nothing needed doing"
    and "there is nowhere to put this yet" are different sentences with different
    remedies.
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
    # WHICH FILES, AND WHY, kept rather than counted (R-318). A confirmed apply
    # over an intake folder nobody had imported answered ``skipped: 20`` and named
    # no file, which reads as a failed verb rather than as a step not yet taken.
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
        # WHAT THE ENGINE SAID IT DID NOT COMPARE, kept rather than dropped
        # (R-316). Dropping it is how a confirmed apply over a taxonomy that
        # declares a vocal sub-playlist reported an ordinary write while filing
        # nothing into it. The plan's, since the plan made the derivation.
        "not_compared": planned.gaps,
    }


#: The same, for the deferred placements. They wait for a cutover, and what a
#: person can settle before one is the import itself.
PENDING_REMEDY = (
    "no tree has cut over, so no deferred placement can be made and none was "
    "read: these tracks are placed once a tree is database native. An import is "
    "proven by intake imported --export with a Fresh Export, not by this verb"
)

def route_inbox(ctx) -> Envelope:
    """Offer a plan for the intake folder, then apply it if the person says so.

    THE BRANCH IS WRITTEN AS "not apply" RATHER THAN AS "is abort", which is the
    same direction the readiness answers in :mod:`cratekit.write.routing_pass`
    are derived in and for the same reason: only the one answer that means yes
    may write, so an option added to this gate later cannot acquire the writing
    behaviour by nobody having classified it.

    WITH ``--export`` THE INTAKE IS THE EXPORT'S, not the disk folder, and the
    write is a new file rather than the database. See :func:`route_inbox_export`.
    """
    cfg = load_config(("routing_cli",))
    if ctx.args.export:
        return route_inbox_export(ctx, cfg, Path(ctx.args.export))
    # ONE READ PER VERB (R-685): the declaration the plan is derived from is
    # the one the write files by, carried on the plan rather than read again.
    planned = plan_inbox(cfg, active_taxonomy.load(cfg))
    items = planned.items
    plan = _plan(items, kind="inbox")
    option = _apply_gate(ctx, plan, _inbox_facts(planned))
    # THE PLANNER'S WARNINGS RIDE ON EVERY ANSWER, as the export path's do,
    # so a reader of the declined envelope learns why every destination is
    # empty without the screen.
    if option != "apply":
        return ctx.envelope(
            data=_plan(items, kind="inbox", applied=False),
            outcome=Outcome.NO_OP,
            warnings=planned.warnings,
        )
    if not items:
        # AN EMPTY FOLDER IS NOT A WRITE. Nothing is opened, no session is taken
        # and the declaration is never derived, which is what makes this true on
        # the disk rather than approximately true.
        return ctx.envelope(
            data=_plan(items, kind="inbox", applied=False, reason="inbox-empty"),
            outcome=Outcome.NO_OP,
            warnings=planned.warnings,
        )
    result = apply_inbox(cfg, planned)
    # THE GAPS RIDE AS A WARNING, NOT IN THE TOTALS. They are what this run did
    # not compare rather than a count of what it did, and the warning is the one
    # place every surface over this engine says so in the same words.
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

    WITHOUT ``--export`` IT IS READ ONLY (R-313). The open carries no write
    intent and no session is entered, so the report is safe with rekordbox
    open. On a library with nothing native it compares nothing and says what
    the export medium delivers, :data:`UNPLACED_EXPORT_REMEDY`.

    WITH ``--export`` IT WRITES A REVIEW (U91, R-694), on the medium that needs
    no database write. Its placements are nested membership in a new file, which
    no import lands. See :func:`route_unplaced_export`.
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
    # THE GATE IS ANSWERED FROM THE FROZEN PLAN (U219), the rows the answer was
    # recorded against and the file it was pinned to, never from a fresh read:
    # by now the first tree may already hold its adds, so a fresh plan would
    # digest differently from the one approved and stall every respawn.
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
            # THE CUT THE WORKER WILL READ, read the same way first (U89): the one
            # loader, at the path the frozen configuration names. The file itself
            # is read as it stands, not frozen with the job. A corrupt calibration
            # refuses here before any item is claimed.
            threshold = metadata_cli.load_vocal_threshold(jobs.frozen_config(job))
            declared = active_taxonomy.load(jobs.frozen_config(job))
            # FROM HERE THIS RUN DROVE, so from here a refusal owes the leftovers.
            frozen = jobs.frozen_config(job)
            # THE TREES THIS RUN DRIVES, read before the drive: an item already
            # done was driven by an earlier run and is not this run's to report.
            driven = [
                i.item_id for i in jobs.items(store, job.job_id) if i.state != jobs.ItemState.DONE
            ]
            _, warnings = ctx.run_job(store, job)
            job = jobs.get(store, job.job_id)
            # THE SAME ENGINE AS THE REBUILD, SO THE SAME GAP (R-316). Only on the
            # branch that drove, because a job finished on entry was compared by
            # an earlier run and this one compared nothing at all. The leftovers
            # sit on the same branch for the same reason (R-312).
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
        # BOTH EXITS, which is the rule a queued verb's advisory owes. Only when
        # this run drove: a refusal raised before the drive wrote nothing.
        if frozen is None:
            raise
        raise _with_left_behind(failed, frozen, job.job_id) from failed
    return ctx.envelope(data=jobs.reported(store, job), warnings=warnings)


def _resort_gate(ctx):
    """The resort's declared gate over its plan, found by digest source (U219).

    Refuses rather than defaulting when there is none: a resort whose entry
    lost its gate would queue writes nobody was shown, and the conformance
    suite reads the registry, so it would call the verb clean.
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

    The trees the adds go into, how many, and the memberships the resort will
    leave where they are, since it is additive and a person approving it
    should know what it will not take away.
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

    THE GATE FIRST (U219). Sitting 61 rehearsed a resort on a disposable copy
    and it ran as a job with nothing to compare, so the rehearsal rule had no
    digest to hold the live run to. Now the verb reads the library without
    writing, runs the same derivation and check the rebuild runs before its
    write, and shows every add, by tree, folder, playlist and file, with the
    count it will leave where it is. The answer is pinned to the database file
    the plan read (U161), the adds are frozen in the job, and the worker
    refuses before writing if what it would add has moved.

    ONLY THE ROUTED TREES. A native tree the declaration names as something
    else, the intake flow above all, is left alone and named in a warning:
    its rebuild derived the routing tree's placements and wrote
    ``INBOX / Minimal / Deep Tech`` at sitting 61 (R-789).

    AN EMPTY PLAN STILL ASKS, then queues nothing, which is the rule
    ``tag retag`` argues: every declared gate fires, and a job with no work
    would be walked to SUCCEEDED over a library nothing changed. A library
    with no routed native tree reads nothing and asks over nothing.
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
            # A NATIVE TREE THE TAXONOMY DOES NOT DERIVE IS STILL NATIVE, so the
            # count is read and the state says which zero.
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
                # THE APPROVED ADDS, FROZEN, which the resume answers its gate
                # from and the worker holds its write to.
                RESORT_ADDS_KEY: adds,
                # And what the screen said in front of them, so the resume
                # shows the same facts over the same rows.
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

    IT IS THE REBUILD ENGINE, and calling it anything else would be this file
    claiming a second router. A genre or an energy change moves where the
    declaration puts a track, and re-deriving the declaration and writing back
    what the database lacks is exactly what that costs on the additive side.

    WHAT IT DOES NOT DO IS TAKE THE TRACK OUT OF WHERE IT WAS. The membership
    writer is additive by construction, so after a genre change the track is in
    its new sub AND still in its old one until somebody removes it. This build
    has no database removal path to offer, so the verb's summary says additive
    and the resume NAMES what was left, which is R-312.

    THE ENGINE'S OWN MEASUREMENT IS WHAT GETS NAMED. ``after`` is the check the
    engine ran on the handle it had just written through, so keeping it costs
    no second walk of the library and cannot refuse after a job that succeeded.
    It is returned as this item's report, the durable channel the driver already
    owns, so the resume reads it back whichever way the job ended.

    ``cfg`` is the configuration this job was FROZEN against (KTD9). Nothing here
    loads one.
    """
    tree_id = str(item.item_id)
    report = rebuild.rebuild_governed_tree(
        cfg,
        tree_id=tree_id,
        workflow=RESORT_WORKFLOW,
        # THE CALIBRATED CUT, through the one loader, at the path the frozen
        # configuration names. None on a library never calibrated (U89, D7).
        vocal_threshold=metadata_cli.load_vocal_threshold(cfg),
        # THIS TREE'S APPROVED ADDS (U219). The engine refuses before writing
        # if its own before check would add anything else.
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
            # WHAT CAME DUE ONLY FROM THIS RESORT'S OWN WRITES (U219, round
            # two): a favourite whose track it filed into a new folder, which
            # no plan before the write could show and so it did not write.
            "due_again": len(report.after.missing),
        },
    )


def _left_behind(cfg: config.Config, job_id: str) -> tuple[list[dict[str, Any]], str]:
    """Every leftover this job's committed reports name, and where they are kept.

    READ BACK RATHER THAN ACCUMULATED, so a job continued by a second process
    names what the first one's trees left as well as its own.
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

    A RESORT WRITES ONLY WHAT ITS GATE SHOWED, so a favourite whose track this
    run filed into a new folder is left for the next resort's plan. Said here
    rather than only logged, because the tree still differs after a run that
    succeeded: on a tree a restore marked, its flag stays set and its writes
    keep refusing until the next resort files the rest.
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

    A RESORT QUEUES ONE ITEM PER TREE, so a partial failure is its ordinary bad
    ending, and that ending leaves through the job's cause with no warnings at
    all. The trees that finished were written to all the same. The step is
    appended and the cause is otherwise untouched, through ``rebuilt`` so a
    blocked or cancelled job keeps the type the dispatcher reads.
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
    native = [
        tree_id for tree_id in entries.tree_ids() if entries.is_database_native(tree_id)
    ]
    if not native:
        # NOTHING WAS READ, SO NOTHING IS CLAIMED (R-436, R-501). This answered
        # OK over runs it had not opened, and a landing named it as the proof
        # of an import. With no native tree there is nowhere to place a track,
        # so it is a no-op that says why and names what does work today.
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
