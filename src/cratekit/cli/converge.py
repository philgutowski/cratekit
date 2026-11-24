"""``crate converge``: what each governed tree's standing is, without writing (U36).

It is read only, opening no session, lock or acknowledgment, since it is what
a person runs when a tree already refuses every write; it is a module apart
from ``rebuild`` so the destructive verb never parks it. It never reports a
tree converged that it could not compare: each check is matching, differing,
or not compared and why, a comparison that ran but could not tie a playlist
to one destination included (R-1991).
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterator

from cratekit.cli import registry
from cratekit.cli.output import Envelope
from cratekit.core import active_taxonomy, config, convergence, rb_writer, taxonomy, tree_registry
from cratekit.core.cause import CratekitError, Outcome
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.write import metadata_cli, rebuild, routing_pass

if TYPE_CHECKING:  # pragma: no cover - import cycle avoidance for typing only
    from cratekit.cli import Context

#: The three answers a per-tree check can carry, named once.
MATCHING = "matching"
DIFFERING = "differing"
NOT_COMPARED = "not-compared"

#: How many playlists not compared a differing line names before its differences.
UNREAD_SHOWN = 5

def build(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    parser.add_argument(
        "--tree",
        default=None,
        help=(
            "one tree's stable identifier, to report on that tree alone; "
            "every governed tree by default"
        ),
    )
    parser.set_defaults(_handler=converge)


def _library_rows(db: Any) -> Iterator[Any]:
    """Every collection row, through the one producer that reads the soft-delete marker."""
    return routing_pass.content_rows(db)


def _standing(record: convergence.TreeConvergence | None) -> dict[str, Any]:
    """What the record says about a tree, which needs no database, so it always answers."""
    if record is None:
        return {"unconverged": False, "reason": None, "since": None, "disposed_by": None}
    return {
        "unconverged": record.unconverged,
        "reason": record.reason,
        "since": record.since,
        "disposed_by": None if record.disposition is None else record.disposition.actor,
    }


def _compare(
    cfg: config.Config,
    db: Any,
    *,
    tree_id: str,
    entries: tree_registry.Registry,
    declared: taxonomy.Taxonomy,
) -> tuple[str, str]:
    """Run the live comparison for one native tree, or say why it did not run.

    Returns a status and a detail line. An engine refusal becomes this tree's
    ``NOT_COMPARED`` rather than ending the report for the others.
    """
    rows = list(_library_rows(db))
    known = {str(row.ID) for row in db.get_playlist()}
    try:
        report = rebuild.report_convergence(
            cfg,
            db,
            tree_id=tree_id,
            registry=entries,
            declared=declared,
            rows=rows,
            root_exists=lambda root_id: root_id in known,
            # The calibrated cut, through the workers' loader (U89, D7). None
            # when never calibrated; a corrupt one refuses inside this try, so
            # it is this tree's NOT_COMPARED.
            vocal_threshold=metadata_cli.load_vocal_threshold(cfg),
        )
    except CratekitError as exc:
        return NOT_COMPARED, exc.cause.message
    unread = tuple(f"{NOT_COMPARED}:{entry}" for entry in report.unidentified)
    if not report.converged:
        # At most five playlists not compared go first, so the cut at twenty
        # drops neither kind (R-1991); the count says how many there are.
        shown = "; ".join((*unread[:UNREAD_SHOWN], *report.summaries())[:20])
        if len(unread) > UNREAD_SHOWN:
            shown += f"; {len(unread)} playlist(s) not compared in all"
        return DIFFERING, shown
    detail = f"{report.derived} declared placement(s) all present"
    if report.not_compared:
        detail += f"; not compared: {', '.join(report.not_compared)}"
    if not report.unidentified:
        return MATCHING, detail
    return NOT_COMPARED, f"{detail}; {'; '.join(unread)}{rebuild.UNIDENTIFIED}"


def converge(ctx: "Context") -> Envelope:
    """Report, per governed tree, whether the declaration and the database agree."""
    cfg = config.load()
    entries = tree_registry.read(cfg)
    # An unreadable record is a finding here, not the end of the run, since this
    # diagnostic writes nothing; every check then reads not compared.
    unreadable: str | None = None
    try:
        recorded = convergence.read(cfg)
    except convergence.ConvergenceStateUnreadable as exc:
        unreadable = exc.cause.message
        recorded = convergence.EMPTY
    wanted = (
        entries.tree_ids()
        if ctx.args.tree is None
        else tuple(t for t in entries.tree_ids() if t == ctx.args.tree)
    )
    if ctx.args.tree is not None and not wanted:
        # A tree the registry does not govern is refused, so "no such tree"
        # never reads as "that tree is fine".
        return ctx.envelope(
            data={
                "checks": [
                    {
                        "key": f"tree.{ctx.args.tree}",
                        "title": ctx.args.tree,
                        "status": NOT_COMPARED,
                        "detail": "this library's registry holds no record for that tree",
                        "remedy": str(Remedy.FIX_COMMAND_LINE),
                    }
                ],
                "summary": {"trees": 0, "blocking": list(recorded.blocking_trees())},
            },
            outcome=Outcome.REFUSED,
            code=ExitCode.LIBRARY_PREREQUISITE,
        )

    native = [t for t in wanted if entries.is_database_native(t)]
    checks: list[dict[str, Any]] = []
    live: dict[str, tuple[str, str]] = {}

    if native:
        # The database is opened only once a tree has cut over. A failure to
        # open, or to read the declaration first, is NOT COMPARED for each
        # native tree; read after the open, a refusal escaped holding the
        # database (R-685).
        handle = declared = None
        try:
            declared = active_taxonomy.load(cfg)
            handle = rb_writer.open_db(cfg=cfg)
        except CratekitError as exc:
            for tree_id in native:
                live[tree_id] = (NOT_COMPARED, exc.cause.message)
        if handle is not None and declared is not None:
            try:
                for tree_id in native:
                    live[tree_id] = _compare(
                        cfg, handle, tree_id=tree_id, entries=entries, declared=declared
                    )
            finally:
                rb_writer.close_db(handle)

    if unreadable is not None:
        checks.append(
            {
                "key": "record.unreadable",
                "title": convergence.STATE_KEY,
                "status": NOT_COMPARED,
                "detail": (
                    f"{unreadable} Nothing below can say whether a tree is "
                    f"refusing writes, because the record that holds that answer "
                    f"could not be read."
                ),
                "remedy": str(Remedy.RUN_DOCTOR),
            }
        )

    for tree_id in wanted:
        standing = _standing(recorded.tree(tree_id))
        status, detail = live.get(
            tree_id,
            (
                NOT_COMPARED,
                "this tree is still on the XML bridge, so its membership is the "
                "export's and there is nothing here to compare",
            ),
        )
        if unreadable is not None:
            # The comparison reads the same record, so it cannot have run either.
            status, detail = NOT_COMPARED, f"{detail} (the convergence record is unreadable)"
        if standing["unconverged"]:
            detail = (
                f"unconverged since {standing['since']} ({standing['reason']}); "
                f"{detail}"
            )
        checks.append(
            {
                "key": f"tree.{tree_id}",
                "title": tree_id,
                "status": status,
                "detail": detail,
                "remedy": (
                    str(Remedy.REBUILD_TREE)
                    if status is DIFFERING or standing["unconverged"]
                    else None
                ),
            }
        )

    blocking = [t for t in recorded.blocking_trees() if t in wanted]
    return ctx.envelope(
        data={
            "checks": checks,
            "summary": {
                "trees": len(wanted),
                "database_native": len(native),
                "blocking": blocking,
                "record_readable": unreadable is None,
                "library": str(Path(cfg.library.root)),
            },
        }
    )


__all__ = ["DIFFERING", "MATCHING", "NOT_COMPARED", "build", "converge"]
