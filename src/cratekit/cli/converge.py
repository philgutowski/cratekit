"""``crate converge``: what each governed tree's standing is, without writing (U36).

WHY THIS IS A SEPARATE MODULE FROM THE REBUILD'S SURFACE. The two verbs are not
alike in the one way that decides where a verb can land. ``rebuild`` writes
``db_tree``, is destructive, and cannot exit OK on a machine with no rekordbox
database, so it sits behind the conformance wall with the other destructive
database verbs. ``converge`` declares no gates, writes nothing, and is exactly
what a person is told to run when a tree is already refusing every write. Both
were declared against ONE module, and because the countdown in
``tests/_pending.py`` keys on the module rather than on the verb, the read-only
one was parked behind the destructive one. Parking it parks the remedy: both
refusals in this unit name it as step one.

TWO PROPERTIES, AND THE SECOND ONE IS THE UNIT'S OWN LESSON APPLIED HERE.

**It is read only and stays that way.** It opens no session, takes no lock,
writes no state and asks for no acknowledgment. A diagnostic that needed the
gates the unconverged flag is holding shut would be a diagnostic nobody can
reach, and the person reaching for it is by definition somebody whose library is
refusing writes.

**It never reports a tree converged that it could not compare.** Every check
below is one of three answers: compared and matching, compared and differing, or
NOT COMPARED and why. There is no fourth answer that looks like the first. That
is the same sentence the rebuild's derivation refuses on, said at the surface: a
library whose volume is not mounted, or whose database this build cannot open,
produces no comparison at all, and reporting an empty comparison as a clean one
is how a run tells somebody their damaged tree is fine.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterator

from cratekit.cli import registry
from cratekit.cli.output import Envelope
from cratekit.core import config, convergence, rb_writer, taxonomy, tree_registry
from cratekit.core.cause import CratekitError, Outcome
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.write import metadata_cli, rebuild, routing_pass

if TYPE_CHECKING:  # pragma: no cover - import cycle avoidance for typing only
    from cratekit.cli import Context

#: The three answers a per-tree check can carry, named once so the renderer and
#: the tests cannot disagree about the spelling.
MATCHING = "matching"
DIFFERING = "differing"
NOT_COMPARED = "not-compared"


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
    """Every collection row, through the ONE producer that reads the marker.

    Not a second walk written here. ``routing_pass.content_rows`` refuses a row
    that cannot report its soft-delete marker rather than defaulting it, and a
    copy of that walk in a diagnostic would be a second answer to which rows are
    live, reached by the one command somebody runs to find out what is true.
    """
    return routing_pass.content_rows(db)


def _standing(record: convergence.TreeConvergence | None) -> dict[str, Any]:
    """What the RECORD says about a tree, which needs no database at all.

    This half always answers, and that is the point: the record is what survives
    the process that discovered the damage, so a person on a machine where the
    volume is not mounted can still be told which trees are refusing and why.
    """
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

    Returns a status and a detail line. A refusal from the engine is turned into
    ``NOT_COMPARED`` with its own message rather than being allowed to end the
    whole report: a library with three governed trees and one unreadable
    taxonomy should still be told the truth about the other two.
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
            # THE CALIBRATED CUT, through the one loader the routing passes and
            # the workers use (U89), so this report compares the vocal sub the
            # same way they fill it. The threshold is a value the caller
            # supplies (D7). None on a library never calibrated, and the engine
            # then names the dimension it did not compare. A corrupt calibration
            # refuses inside this try, so it is this tree's NOT_COMPARED with
            # the loader's own message rather than the end of the report.
            vocal_threshold=metadata_cli.load_vocal_threshold(cfg),
        )
    except CratekitError as exc:
        return NOT_COMPARED, exc.cause.message
    if report.converged:
        detail = f"{report.derived} declared placement(s) all present"
        if report.not_compared:
            detail += f"; not compared: {', '.join(report.not_compared)}"
        return MATCHING, detail
    return DIFFERING, "; ".join(report.summaries()[:20])


def converge(ctx: "Context") -> Envelope:
    """Report, per governed tree, whether the declaration and the database agree."""
    cfg = config.load()
    entries = tree_registry.read(cfg)
    # AN UNREADABLE RECORD IS A FINDING HERE, NOT THE END OF THE RUN. Every other
    # reader of that document refuses on it, correctly, because acting on a
    # record nobody can parse is acting on nothing. This is the one caller that
    # must survive it: it writes nothing, and it is what a person is told to run
    # when something is wrong, so a diagnostic that died with the document would
    # leave them with no way to see what the document says. The standing half of
    # each check then reads "not compared", never "matching".
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
        # Named a tree the registry does not govern. Reported rather than
        # answered, because "no such tree" and "that tree is fine" are the two
        # sentences this whole unit exists to keep apart.
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
        # THE DATABASE IS OPENED ONLY WHEN A TREE HAS ACTUALLY CUT OVER, so this
        # verb runs on every library that has never flipped one, which is every
        # library until the first cutover, without a rekordbox database existing
        # at all. A failure to open is a NOT COMPARED answer for each native
        # tree, never an absent one.
        handle = None
        try:
            handle = rb_writer.open_db(cfg=cfg)
        except CratekitError as exc:
            for tree_id in native:
                live[tree_id] = (NOT_COMPARED, exc.cause.message)
        if handle is not None:
            declared = taxonomy.default_taxonomy()
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
            # The live comparison reads the same record to resolve destinations,
            # so it cannot have run either. Forced to NOT COMPARED rather than
            # left at whatever the comparison happened to answer, because the one
            # thing this verb may never do is report a tree it could not compare.
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
