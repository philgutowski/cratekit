"""``crate tree cutover`` and ``crate tree revert``: the verbs over the registry (R-235).

WHAT WAS MISSING. :mod:`cratekit.core.tree_registry` has held the precheck, the
record and the revert since U20, and nothing under ``src`` called any of them.
Every database membership writer asserts ``anchored_root`` first, which refuses
a tree still on the bridge, and a tree with no record IS on the bridge. So an
approved adoption refused on every real library and named a remedy no shipped
verb could perform. These two verbs are that remedy.

THE ROOT IS FOUND, NEVER CREATED, and that is the whole difference between a
cutover and a duplication. The tree's root folder is the one the XML bridge
wrote, under the display name the taxonomy declares, and the tracks already in
it stay in it because the identifier recorded here is that folder's. A verb that
created the folder when it found none would anchor the registry to an empty
twin beside the real tree, which is the silent parallel tree ``anchored_root``
exists to refuse, arriving through the verb meant to prevent it. None refuses.
More than one refuses too, because choosing between two is a guess every later
write would be parented to.

THE DATABASE IS READ THROUGH A DISPOSABLE COPY. The live file is protected by
standing constraint and this verb wants one fact off it, which rows are folders
of one name directly under the playlist root. ``rb_writer.read_only_copy``
copies, opens the copy, and refuses while rekordbox or its agent is running.

PLAN, THEN APPROVE, AND AN UNREADY LIBRARY IS NEVER ASKED. Both gates are
``explicit``, so R34 makes them answerable only by a separate recorded act. The
plan names the tree, the root row it would anchor, the derivation source, the
registry file it would write, the database it read, and each precheck result. A
library that is not ready refuses BEFORE the question, with the refusal the
precheck itself gives: asking a person to approve a cutover that cannot be
performed spends the one deliberate act they have on nothing. The approving
invocation rebuilds the whole plan, so a library that moved between the offer
and the answer moves the digest and the decision is refused as stale, and
``tree_registry.flip`` asserts the precheck again at the moment it records.

APPROVING A CUTOVER IS THE ONE WAY DOOR. A revert is a complete undo only until
the tree takes its first native write. After that the database holds rows the
last export never held, and the revert refuses.

THE PLAN NAMES THE REGISTRY FILE AND THE DATABASE, both, because they can be
two different libraries' and that was paid for at sitting 13. The registry is
LIBRARY state, beside the library root, and a rehearsal that redirects the
configuration and the database and leaves the library root alone records a
cutover in the real library's registry, anchored to a root identifier read off
the copy. Nothing here can tell a rehearsal from the real thing, so the two
paths are put in front of the person who can.

Layer: cli, beside ``converge`` and ``rebuild``.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
from datetime import date
from pathlib import Path
from typing import TYPE_CHECKING, Any

from cratekit.cli import registry
from cratekit.cli.output import Envelope, digest_of
from cratekit.core import active_taxonomy, config, rb_writer, taxonomy, tree_registry
from cratekit.core.cause import (
    Cause,
    CratekitError,
    Outcome,
    Remediation,
    rebuilt,
    refuse,
)
from cratekit.core.exit_codes import Remedy

if TYPE_CHECKING:  # pragma: no cover - import cycle avoidance for typing only
    from cratekit.cli import Context


def _today() -> date:
    """The day a cutover is recorded on. A seam, so a test can name the day."""
    return date.today()


# ---------------------------------------------------------------------------
# Shared
# ---------------------------------------------------------------------------


def _plan_gate(entry: registry.Entry) -> registry.GateSpec:
    """The approval gate off the entry, found by digest source, never by position."""
    for spec in entry.gates:
        if spec.digest_source == "plan":
            return spec
    raise CratekitError(
        Cause(
            reason="internal-error",
            message=(
                f"{entry.name} declares no gate digested against the plan, so "
                f"there is no question to ask before writing the registry"
            ),
            remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
            origin=("cli.cutover",),
            detail={"verb": entry.name},
        )
    )


def _digested(kind: str, item: dict[str, Any], totals: dict[str, Any]) -> dict[str, Any]:
    """One item as a ``plan/1`` payload, digested over what a person is shown.

    THE TOTALS ARE NOT IN THE DIGEST. They are where the report says what was
    recorded and on which day, and a digest that moved when the report was
    written would differ from the one the decision was recorded against.
    """
    return {
        "digest": digest_of({"kind": kind, "items": [item]}),
        "items": [item],
        "totals": totals,
        "chunk": None,
    }


def _recorded(record: tree_registry.TreeRecord) -> dict[str, Any]:
    """One registry record as the report shows it."""
    return {
        "tree": record.tree_id,
        "mode": str(record.mode),
        "root": record.root_id,
        "cutover_on": None if record.cutover_on is None else record.cutover_on.isoformat(),
        "source": None if record.source is None else str(record.source),
    }


# ---------------------------------------------------------------------------
# tree cutover
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Root:
    """One candidate root row: a folder of the tree's name under the playlist root."""

    root_id: str
    name: str


def build(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    """Declare the cutover's arguments.

    THERE IS NO ``--root``, NO ``--source`` AND NO ``--approve``. The root is
    found in the database, the source comes off the taxonomy, and the approval
    is the recorded answer to the explicit gate (R34). A flag for any of them
    would be a second opinion about a value this verb exists to establish.

    ``--export`` IS REQUIRED AND HAS NO DEFAULT, which is the precheck's own
    rule carried to the surface: a hunt for the newest XML would pick the
    pending intake file the same precheck refuses.
    """
    del entry
    parser.add_argument(
        "tree",
        help="the stable identifier of the tree to cut over, as the taxonomy declares it",
    )
    parser.add_argument(
        "--export",
        required=True,
        metavar="FILE",
        help=(
            "the Fresh Export taken from rekordbox before this cutover, which "
            "is the copy of the tree a revert walks back to"
        ),
    )
    parser.set_defaults(_handler=cutover)


def derivation_source(
    declared: taxonomy.Taxonomy, tree_id: str
) -> tree_registry.DerivationSource:
    """Where a rebuild of ``tree_id`` would come from, read off the declaration.

    OFF THE TAXONOMY AND NEVER OFF A FLAG. ``record_cutover`` takes the source
    with no default so that nobody answers "yes, this can be rebuilt" about a
    tree nobody checked, and a flag a person types is that answer typed. The
    routing tree is the one tree the declared taxonomy reproduces from what is
    on disk. The catalogue tree is declared and is NOT reproducible, so it is
    named with its real source and ``assert_rebuildable`` refuses it. The intake
    tree is refused by ``assert_not_intake`` before its source is ever read.

    A TREE THE TAXONOMY DOES NOT DECLARE IS REFUSED rather than called curated.
    An identifier nobody declared is far more often a misspelling than a
    playlist a person keeps by hand, and both end in a refusal, so the refusal
    names the identifiers that would have been accepted.
    """
    if tree_id in (declared.tree.id, declared.intake.id):
        return tree_registry.DerivationSource.TAXONOMY
    if declared.catalog is not None and tree_id == declared.catalog.id:
        return tree_registry.DerivationSource.CATALOGUE_CRAWL
    raise refuse(
        "cutover-tree-undeclared",
        f"this library's taxonomy declares no tree {tree_id!r}, so nothing can "
        f"say where its membership would be rebuilt from and it cannot cut over",
        steps=(f"name the routing tree, which this library declares as {declared.tree.id!r}",),
        origin=("cli.cutover",),
        detail={"tree_id": tree_id, "routing_tree": declared.tree.id},
    )


def _display(declared: taxonomy.Taxonomy, tree_id: str) -> str:
    """The display name the taxonomy gives ``tree_id``'s root folder."""
    if declared.catalog is not None and tree_id == declared.catalog.id:
        return declared.catalog.display
    if tree_id == declared.intake.id:
        return declared.intake.display
    return declared.tree.display


def find_roots(db: Any, display: str) -> tuple[Root, ...]:
    """Every live folder named ``display`` sitting directly under the playlist root.

    DIRECTLY UNDER THE PLAYLIST ROOT, because that is where a tree's root is. A
    folder of the same name nested somewhere else is a namesake and not a
    candidate, and counting it would refuse a library whose one real root is
    unambiguous.

    THE SOFT DELETE MARKER IS NOT READ, and that is the writer's rule rather
    than an omission. Every playlist lookup the membership writers make is by
    name and parent with no marker filter, so a reader here that skipped a
    marked row would count one root where the writer it anchors for sees two.
    The cost, a marked namesake a person cannot see in rekordbox refusing the
    cutover, is recorded in the ledger with its reachability unmeasured.

    MATERIALIZED before it is filtered, for the reason ``rebuild.read_tree``
    gives: the query is not iterated while anything else is asked of the handle.
    """
    found: list[Root] = []
    for row in list(db.get_playlist(Name=display)):
        if not rb_writer._is_folder(row):
            continue
        if str(getattr(row, "ParentID", "")) not in rb_writer.ROOT_PARENT_SENTINELS:
            continue
        found.append(Root(root_id=str(row.ID), name=str(row.Name)))
    return tuple(sorted(found, key=lambda root: root.root_id))


def _one_root(cfg: config.Config, tree_id: str, display: str) -> Root:
    """The one root this tree would anchor to, or a refusal naming the count."""
    database = rb_writer.live_db_path(cfg)
    with rb_writer.read_only_copy(database, cfg=cfg) as db:
        roots = find_roots(db, display)
    if len(roots) == 1:
        return roots[0]
    if not roots:
        message = (
            f"the database holds no folder named {display!r} directly under "
            f"the playlist root, so the tree {tree_id!r} has no root to adopt; "
            f"creating one here would anchor the tree to an empty folder "
            f"beside wherever its tracks really are"
        )
        steps: tuple[str, ...] = (
            f"import the export that carries the {display!r} tree into "
            f"rekordbox, or create the folder there, so the root exists before "
            f"the cutover adopts it",
        )
    else:
        message = (
            f"the database holds {len(roots)} folders named {display!r} "
            f"directly under the playlist root, so the tree {tree_id!r} has no "
            f"one root to adopt; choosing between them would parent every "
            f"later write to a guess"
        )
        steps = (
            f"in rekordbox, merge or rename the {display!r} folders until "
            f"exactly one sits at the top level",
        )
    raise refuse(
        "cutover-root-unresolved",
        message,
        steps=steps,
        origin=("cli.cutover",),
        detail={
            "tree_id": tree_id,
            "display": display,
            "found": len(roots),
            "roots": [root.root_id for root in roots],
            "database": str(database),
        },
    )


def _precheck_rows(results: tuple[tree_registry.PrecheckResult, ...]) -> list[dict[str, Any]]:
    """Each precheck result as the plan shows it."""
    return [
        {
            "check": result.check,
            "passed": result.passed,
            "reason": None if result.cause is None else result.cause.reason,
            "message": None if result.cause is None else result.cause.message,
        }
        for result in results
    ]


def _refuse_unready(results: tuple[tree_registry.PrecheckResult, ...]) -> None:
    """Raise the first precheck refusal, carrying every result beside it.

    THE REFUSAL IS THE PRECHECK'S OWN, slug, sentence and steps, which is what
    ``tree_registry.flip`` would have raised. What is added is the rest of the
    table, so a person with two things to fix is told about both on one run
    rather than one per attempt.
    """
    for result in results:
        if result.refusal is None:
            continue
        cause = result.refusal.cause
        raise rebuilt(
            result.refusal,
            replace(
                cause,
                origin=(*cause.origin, "cli.cutover"),
                detail={**cause.detail, "precheck": _precheck_rows(results)},
            ),
        )


def cutover(ctx: "Context") -> Envelope:
    """Plan one tree's cutover, ask, and record it through ``tree_registry.flip``.

    THE ORDER IS CHEAPEST REFUSAL FIRST. What the taxonomy says about the tree
    needs no disk beyond the template. The registry and the precheck read this
    product's own state. The root needs a copy of the database, which is the
    expensive read and the one that refuses while rekordbox is open, so it is
    asked last and only of a library that is otherwise ready.

    A TREE ALREADY DATABASE NATIVE RECORDS NOTHING AND ASKS NOTHING. Recording
    over it would move its cutover date and could move its anchor, on a tree
    that may already have taken writes under the first one.
    """
    cfg = config.load()
    declared = active_taxonomy.load(cfg)
    tree_id = ctx.args.tree
    export = Path(ctx.args.export).expanduser().resolve()

    source = derivation_source(declared, tree_id)
    tree_registry.assert_not_intake(tree_id, declared)
    tree_registry.assert_rebuildable(tree_id, source)

    standing = tree_registry.read(cfg).record(tree_id)
    if standing is not None and standing.mode == tree_registry.Mode.DATABASE:
        return ctx.envelope(
            data=_digested("tree.cutover", _recorded(standing), {"recorded": False}),
            outcome=Outcome.NO_OP,
            warnings=(
                {
                    "code": "cutover-already-recorded",
                    "message": (
                        f"the tree {tree_id!r} is already database native, "
                        f"anchored to root {standing.root_id} since "
                        f"{standing.cutover_on}, so nothing was recorded"
                    ),
                },
            ),
        )

    results = tree_registry.cutover_precheck(cfg, export=export)
    _refuse_unready(results)
    display = _display(declared, tree_id)
    root = _one_root(cfg, tree_id, display)

    item = {
        "tree": tree_id,
        "display": display,
        "root": {"id": root.root_id, "name": root.name},
        "source": str(source),
        "export": str(export),
        "registry": str(tree_registry.path_for(cfg)),
        "database": str(rb_writer.live_db_path(cfg)),
        "precheck": _precheck_rows(results),
    }
    offered = _digested("tree.cutover", item, {"recorded": False})
    option = ctx.gate.require(
        _plan_gate(ctx.entry),
        plan=offered,
        context={"tree": tree_id, "anchors_to": root.root_id, "writes": item["registry"]},
    )
    if option == "abort":
        return ctx.envelope(data=offered, outcome=Outcome.NO_OP)

    on = _today()
    tree_registry.flip(
        cfg, tree_id, root_id=root.root_id, on=on, source=source, export=export
    )
    return ctx.envelope(
        data={**offered, "totals": {"recorded": True, "cutover_on": on.isoformat()}}
    )


# ---------------------------------------------------------------------------
# tree revert
# ---------------------------------------------------------------------------


def build_revert(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    """Declare the revert's one argument. The approval is the recorded decision."""
    del entry
    parser.add_argument(
        "tree",
        help="the stable identifier of the tree to put back on the XML bridge",
    )
    parser.set_defaults(_handler=revert)


def revert(ctx: "Context") -> Envelope:
    """Plan one tree's revert, ask, and perform it through ``revert_cutover``.

    THE TREE IS NOT CHECKED AGAINST THE TAXONOMY. A record for a tree the
    declaration has since dropped is exactly the record somebody needs to be
    able to remove, and the registry is what says whether there is one.

    THE NATIVE WRITE GUARD IS ASKED TWICE AND OWNED ONCE. It is asked here so a
    tree that cannot revert refuses before the question, and
    ``tree_registry.revert_cutover`` asserts it again under the registry lock,
    which is the one that holds.
    """
    cfg = config.load()
    tree_id = ctx.args.tree
    standing = tree_registry.read(cfg).record(tree_id)
    if standing is None or standing.mode != tree_registry.Mode.DATABASE:
        return ctx.envelope(
            data=_digested(
                "tree.revert",
                {"tree": tree_id, "mode": str(tree_registry.DEFAULT_MODE)},
                {"reverted": False},
            ),
            outcome=Outcome.NO_OP,
            warnings=(
                {
                    "code": "revert-nothing-recorded",
                    "message": (
                        f"the tree {tree_id!r} is on the XML bridge, so there "
                        f"is no cutover to revert and nothing was written"
                    ),
                },
            ),
        )

    tree_registry.assert_revertible(cfg, tree_id)
    item = {**_recorded(standing), "registry": str(tree_registry.path_for(cfg))}
    offered = _digested("tree.revert", item, {"reverted": False})
    option = ctx.gate.require(
        _plan_gate(ctx.entry),
        plan=offered,
        context={"tree": tree_id, "releases": standing.root_id, "writes": item["registry"]},
    )
    if option == "abort":
        return ctx.envelope(data=offered, outcome=Outcome.NO_OP)

    tree_registry.revert_cutover(cfg, tree_id)
    return ctx.envelope(data={**offered, "totals": {"reverted": True}})


__all__ = [
    "Root",
    "build",
    "build_revert",
    "cutover",
    "derivation_source",
    "find_roots",
    "revert",
]
