"""The ``repair.link`` verb: write chosen values into the row probe columns of
chosen live content rows, the experiment that asks which column keeps a binding
row off a deck (A32, R-928).

A verb because a write to the live database outside a gated verb is
forbidden. It takes any number of ``--set ROW:COLUMN=VALUE`` triples, so one
reading of rekordbox's context menus at an attended sitting answers them all.

The order is ``repair rows``'s: the backup acknowledgment before the plan and
the gate (R-733); the triples parsed and the plan made on a read handle closed
before the gate, refusing a malformed triple, a column the probe may not
write, an unknown row, an unheld value and a minority value by name; the gate
asked over the digested plan even when nothing would be written; only
``apply`` opens the database to write. The gate takes no inline answer (R34).

Layer: write. It names :mod:`cratekit.cli.output` and nothing else from the
command-line layer.
"""

from __future__ import annotations

from typing import Any

from cratekit.cli.output import Envelope, confirm_gate, load_config
from cratekit.core import analysis_store, config, rb_writer, session
from cratekit.core.cause import Outcome
from cratekit.write import row_link

#: The explicit gate the write is asked behind.
CONFIRM_GATE = "repair.link.confirm"

#: The plan writes nothing: every row already holds its value.
NOTHING_TO_WRITE = "rows-link-nothing-to-write"

#: What the apply wrote and read back.
LINK_WRITTEN = "rows-link-written"

_ORIGIN = ("write", "row_link_cli")


def build(parser, entry) -> None:
    """Declare the verb: one ``--set`` per triple, at least one."""
    del entry
    parser.add_argument(
        "--set",
        dest="probes",
        action="append",
        default=[],
        metavar="ROW:COLUMN=VALUE",
        help=(
            "write VALUE into COLUMN of the live content row ROW; COLUMN is one of "
            f"{', '.join(rb_writer.ROW_PROBE_COLUMNS)}; an empty VALUE is the empty "
            "text; give one --set per probe"
        ),
    )
    parser.set_defaults(_handler=repair_link)


def _payload(plan: row_link.ProbePlan) -> dict[str, Any]:
    """The plan as the gate digests it and the envelope carries it."""
    return {
        "digest": plan.digest,
        "items": [probe.to_json() for probe in plan.probes],
        "totals": {
            "count": plan.writes,
            "probes": len(plan.probes),
            "rows": plan.rows,
            "rows_written": 0,
            "written": 0,
            "read_back": 0,
        },
        "chunk": None,
    }


def _facts(plan: row_link.ProbePlan) -> dict[str, Any]:
    """What the gate puts in front of the items: the counts and every write."""
    return {
        "live rows read": plan.rows,
        "probes": len(plan.probes),
        "values to write": plan.writes,
        "rows to write": len(plan.content_ids),
        "columns the probe may write": list(rb_writer.ROW_PROBE_COLUMNS),
        "each write, with who else carries each value": [
            {
                "row": probe.content_id,
                "title": probe.title,
                "column": probe.column,
                "from": "NULL" if probe.was is None else probe.was,
                "to": str(probe.value),
                "other rows carrying the value written": probe.carriers,
                "other rows carrying the value replaced": probe.fellows,
                "writes": probe.writes,
            }
            for probe in plan.probes
        ],
        "what is learned": (
            "which of these rows rekordbox loads to a deck once they carry the "
            "values rows rekordbox made carry; open rekordbox after the write and "
            "read each row's context menu"
        ),
    }


def _nothing(plan: row_link.ProbePlan) -> dict[str, str]:
    return {
        "code": NOTHING_TO_WRITE,
        "message": (
            f"all {len(plan.probes)} probe(s) name a row that already holds the "
            f"value asked for, so there is nothing to write and nothing to learn "
            f"from writing it"
        ),
    }


def _written(written: row_link.Written) -> dict[str, str]:
    return {
        "code": LINK_WRITTEN,
        "message": (
            f"{written.written} value(s) written on {written.rows} row(s), "
            f"{written.read_back} read back from the database as written, those "
            f"columns and no other; undo with a restore of session "
            f"{written.session_id}"
        ),
    }


def _plan(cfg: config.Config, args) -> row_link.ProbePlan:
    """The plan through a handle opened to read, the triples parsed first so a
    malformed one refuses before the database is opened.
    """
    triples = [row_link.parse_triple(spec) for spec in args.probes]
    db = rb_writer.open_db(
        rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
    )
    try:
        return row_link.plan_probes(db, triples)
    finally:
        rb_writer.close_db(db)


def _write(cfg: config.Config, plan: row_link.ProbePlan) -> row_link.Written:
    """Apply the plan through a handle of this function's own, opened to write."""
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        return row_link.apply_probes(
            cfg, db, plan, analysis_roots=analysis_store.watch_roots(cfg)
        )
    finally:
        rb_writer.close_db(db)


def repair_link(ctx) -> Envelope:
    """Plan every triple, ask, then write them and read the rows back."""
    cfg = load_config(_ORIGIN)
    spec = confirm_gate(ctx.entry, CONFIRM_GATE, origin=_ORIGIN)
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).
    session.assert_backup_acknowledged(cfg)

    plan = _plan(cfg, ctx.args)
    data = _payload(plan)
    if ctx.gate.require(spec, plan=data, context=_facts(plan)) != "apply":
        return ctx.envelope(data=data, outcome=Outcome.NO_OP)
    if not plan.writes:
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=[_nothing(plan)])

    written = _write(cfg, plan)
    row_link.assert_read_back(written)
    data["totals"] = {
        **data["totals"],
        "rows_written": written.rows,
        "written": written.written,
        "read_back": written.read_back,
    }
    return ctx.envelope(data=data, warnings=[_written(written)])


__all__ = [
    "CONFIRM_GATE",
    "LINK_WRITTEN",
    "NOTHING_TO_WRITE",
    "build",
    "repair_link",
]
