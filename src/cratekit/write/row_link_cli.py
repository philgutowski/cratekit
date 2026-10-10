"""The ``repair.link`` verb: write a chosen ``ContentLink`` onto one live content
row, the experiment that asks whether that column keeps a binding row off a
deck (A32, R-928).

WHY THIS IS A VERB. A one row write to the live database outside a gated verb
is forbidden, and the question is worth one row: after the defaults (R-923)
and the file id (U115) were ruled out at sitting 36, ``ContentLink`` is the one
content column left that differs between a row the native landing made and a
row rekordbox made. The verb takes the row and the value on its command line,
plans that one row on a read handle, asks, writes through the guard and reads
the row back. What rekordbox then shows on the row's context menu is the
answer, and is read at an attended sitting.

THE ORDER IS ``repair rows``'S:

* the backup acknowledgment is read before the plan is built and before the
  gate (R-733);
* the plan is made on a handle opened to read and closed before the gate, and
  refuses by name an unknown row and a value no other live row carries;
* the gate is asked over the digested plan, AND A PLAN THAT WRITES NOTHING
  STILL ASKS, a row already at the value: every declared gate has to fire,
  and the apply is then a no op;
* only ``apply`` opens the database with write intent, so that is where a
  running rekordbox or its agent refuses, and the engine checks the row is
  still as the plan read it before the session is entered.

THE SECOND INVOCATION REBUILDS THE PLAN and the gate compares its digest with
the one the answer was recorded against, so a row changed in between moves the
digest and the run refuses ``decision-stale``.

THE GATE TAKES NO INLINE ANSWER. It is answered by a separate recorded act with
an actor, the way every write to a live library's rows is (R34).

Layer: write, as ``row_defaults_cli`` is. It names :mod:`cratekit.cli.output`
and nothing else from the command-line layer.
"""

from __future__ import annotations

from typing import Any

from cratekit.cli.output import Envelope
from cratekit.core import analysis_store, config, rb_writer, session
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation
from cratekit.core.exit_codes import Remedy
from cratekit.write import row_link

#: The explicit gate the write is asked behind.
CONFIRM_GATE = "repair.link.confirm"

#: The plan writes nothing: the row already carries the value.
NOTHING_TO_WRITE = "rows-link-nothing-to-write"

#: What the apply wrote and read back.
LINK_WRITTEN = "rows-link-written"

_ORIGIN = ("write", "row_link_cli")


def _load() -> config.Config:
    """Read config, turning a configuration failure into a typed cause."""
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=("write.row_link_cli",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def build(parser, entry) -> None:
    """Declare the verb: the one row and the one value, both on the command line."""
    del entry
    parser.add_argument(
        "content_id",
        help="the identifier of the live content row to write, as the collection "
        "export or SQL shows it",
    )
    parser.add_argument(
        "value",
        type=int,
        help=f"the {row_link.LINK} to write, a value other live rows carry",
    )
    parser.set_defaults(_handler=repair_link)


def _confirm_gate(entry):
    """The verb's own gate by name, never by position."""
    from cratekit.core.cause import refuse

    for spec in entry.gates:
        if spec.name == CONFIRM_GATE:
            return spec
    raise refuse(
        "internal-error",
        f"{entry.name} declares no gate named {CONFIRM_GATE!r}, so there is no "
        f"question to ask before it writes",
        remedy=Remedy.REPORT_DEFECT,
        origin=_ORIGIN,
        detail={"verb": entry.name, "gate": CONFIRM_GATE},
    )


def _payload(plan: row_link.LinkPlan) -> dict[str, Any]:
    """The plan as the gate digests it and the envelope carries it."""
    return {
        "digest": plan.digest,
        "items": [plan.to_json()],
        "totals": {
            "count": 1 if plan.writes else 0,
            "rows": plan.rows,
            "carriers": plan.carriers,
            "fellows": plan.fellows,
            "written": 0,
            "read_back": 0,
        },
        "chunk": None,
    }


def _facts(plan: row_link.LinkPlan) -> dict[str, Any]:
    """What the gate puts in front of the item: the counts and what is written."""
    return {
        "live rows read": plan.rows,
        "rows to write": 1 if plan.writes else 0,
        "column written": row_link.LINK,
        "value written": plan.value,
        "value replaced": plan.was or "NULL",
        "other live rows carrying the value written": plan.carriers,
        "other live rows carrying the value replaced": plan.fellows,
        "what is learned": (
            "whether rekordbox loads this row to a deck once it carries the value "
            "rows rekordbox made carry; open rekordbox after the write and read "
            "the row's context menu"
        ),
    }


def _nothing(plan: row_link.LinkPlan) -> dict[str, str]:
    return {
        "code": NOTHING_TO_WRITE,
        "message": (
            f"the row {plan.content_id} already carries {row_link.LINK} {plan.value}, "
            f"so there is nothing to write and nothing to learn from writing it"
        ),
    }


def _written(written: row_link.Written) -> dict[str, str]:
    return {
        "code": LINK_WRITTEN,
        "message": (
            f"{written.written} row now carries the {row_link.LINK} asked for, "
            f"{written.read_back} read back from the database as written, that "
            f"column and no other; undo with a restore of session "
            f"{written.session_id}"
        ),
    }


def _plan(cfg: config.Config, args) -> row_link.LinkPlan:
    """The plan over the library as it stands, through a handle opened to read."""
    db = rb_writer.open_db(
        rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
    )
    try:
        return row_link.plan_link(db, content_id=str(args.content_id), value=int(args.value))
    finally:
        rb_writer.close_db(db)


def _write(cfg: config.Config, plan: row_link.LinkPlan) -> row_link.Written:
    """Apply the plan through a handle of this function's own, opened to write."""
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        return row_link.apply_link(cfg, db, plan, analysis_roots=analysis_store.watch_roots(cfg))
    finally:
        rb_writer.close_db(db)


def repair_link(ctx) -> Envelope:
    """Plan the one row, ask, then write it and read it back."""
    cfg = _load()
    spec = _confirm_gate(ctx.entry)
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
        "written": written.written,
        "read_back": written.read_back,
    }
    return ctx.envelope(data=data, warnings=[_written(written)])
