"""``crate tree cutover`` and ``crate tree revert``: the verbs over the registry (R-235).

A tree with no registry record is on the XML bridge and every database
membership writer refuses it, so these verbs record and undo a cutover through
:mod:`cratekit.core.tree_registry`. The root is found, never created: a created
folder would anchor the tree to an empty twin beside the real one, so none or
several refuse. The database is read through a disposable copy. Both gates are
explicit (R34), an unready library refuses before the question, and the
approving run rebuilds the plan so a moved library is refused as stale. A
cutover is the one way door: a revert undoes it only until the first native
write. The plan names both the registry file and the database, since a
rehearsal can point them at two different libraries.
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

    The totals are not in the digest, since the report writes them after the
    decision was recorded against it.
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

    No ``--root``, ``--source`` or ``--approve``: the root is found, the source
    read off the taxonomy, and the approval is the explicit gate's answer (R34).
    ``--export`` is required with no default, since a hunt for the newest XML
    would pick the pending intake file the precheck refuses.
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

    Off the taxonomy, never a flag, so nobody types "yes, this can be rebuilt"
    about a tree nobody checked. Trees that answer taxonomy are
    ``tree_registry.cutover_trees``'s, the set doctor also judges by (R-787);
    the intake tree is among them (R-746). The catalogue tree is named with its
    real source and refused by ``assert_rebuildable``. An undeclared tree is
    refused, naming the accepted identifiers, since it is most often a typo.
    """
    accepted = tree_registry.cutover_trees(declared)
    if tree_id in accepted:
        return tree_registry.DerivationSource.TAXONOMY
    if declared.catalog is not None and tree_id == declared.catalog.id:
        return tree_registry.DerivationSource.CATALOGUE_CRAWL
    named = sorted(accepted)
    raise refuse(
        "cutover-tree-undeclared",
        f"this library's taxonomy declares no tree {tree_id!r}, so nothing can "
        f"say where its membership would be rebuilt from and it cannot cut over",
        steps=(
            f"name a tree a cutover records, which this library declares as "
            f"{', '.join(repr(t) for t in named)}",
        ),
        origin=("cli.cutover",),
        detail={"tree_id": tree_id, "cutover_trees": named},
    )


def _display(declared: taxonomy.Taxonomy, tree_id: str) -> str:
    """The display name the taxonomy gives ``tree_id``'s root folder."""
    if declared.catalog is not None and tree_id == declared.catalog.id:
        return declared.catalog.display
    if tree_id == declared.intake.id:
        return declared.intake.display
    return declared.tree.display


def find_roots(db: Any, display: str) -> tuple[Root, ...]:
    """Every folder named ``display`` sitting directly under the playlist root.

    Through ``rb_writer.top_level_folders``, which owns what a top level folder
    is. The soft delete marker is not read, that module's rule, with its cost
    recorded in the ledger.
    """
    found = [
        Root(root_id=str(row.ID), name=str(row.Name))
        for row in rb_writer.top_level_folders(db, display)
    ]
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

    The refusal is the precheck's own, with every result added so a person with
    two things to fix hears of both on one run.
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

    Cheapest refusal first: the database copy is read last, only for a library
    otherwise ready. A tree already database native records and asks nothing,
    since recording over it could move its date and anchor after writes.
    """
    cfg = config.load()
    declared = active_taxonomy.load(cfg)
    tree_id = ctx.args.tree
    export = Path(ctx.args.export).expanduser().resolve()

    source = derivation_source(declared, tree_id)
    try:
        tree_registry.assert_rebuildable(tree_id, source)
    except tree_registry.TreeModeRefused as exc:
        # The registry's own refusal, with the set a cutover does accept.
        cause = exc.cause
        raise rebuilt(
            exc,
            replace(
                cause,
                origin=(*cause.origin, "cli.cutover"),
                detail={
                    **cause.detail,
                    "cutover_trees": sorted(tree_registry.cutover_trees(declared)),
                },
            ),
        ) from exc

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

    # Flat, so the gate shows each value as a field, the same values the digest
    # covers.
    item = {
        "tree": tree_id,
        "display": display,
        "root_id": root.root_id,
        "root_name": root.name,
        "source": str(source),
        "export": str(export),
        "registry": str(tree_registry.path_for(cfg)),
        "database": str(rb_writer.live_db_path(cfg)),
        "precheck_passed": " ".join(result.check for result in results),
    }
    offered = _digested("tree.cutover", item, {"recorded": False})
    option = ctx.gate.require(
        _plan_gate(ctx.entry),
        plan=offered,
        context={
            "tree": tree_id,
            "anchors_to": f"{root.name}, row {root.root_id}",
            "rebuilt_from": str(source),
            "fresh_export": str(export),
            "reads": item["database"],
            "writes": item["registry"],
            "precheck": {result.check: "passed" for result in results},
        },
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

    The tree is not checked against the taxonomy, since a dropped tree's record
    is exactly one somebody needs to remove. The native write guard is asked
    here to refuse before the question, and ``revert_cutover`` asserts it again
    under the registry lock, which is the check that holds.
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
