"""The ``repair.rows`` verb: give a content row rekordbox's own defaults where it lacks them.

WHY THIS IS A VERB (R-923). A row the native landing created before the landing
set these columns will not load to a deck, and the only other way back is to
remove it from the collection and import the file again in rekordbox, which
drops every membership adoption gave it. This fills the columns in place.

THE ORDER IS ``tag rows``'S, and the plan is made on a read handle:

* the backup acknowledgment is read before the plan is built and before the
  gate (R-733);
* the plan is made on a handle opened to read and closed before the gate;
* the gate is asked over the digested plan, AND AN EMPTY PLAN STILL ASKS: every
  declared gate has to fire, and a plan that writes nothing is then a no op;
* only ``apply`` over a plan that writes opens the database with write intent,
  so that is where a running rekordbox or its agent refuses, and the engine
  checks each row is still as the plan read it before the session is entered.

THE SECOND INVOCATION REBUILDS THE PLAN from the database and the gate compares
its digest with the one the answer was recorded against, so a row rekordbox
filled in between moves the digest and the run refuses ``decision-stale``.

THE GATE TAKES NO INLINE ANSWER. It is answered by a separate recorded act with
an actor, the way every write to a live library's rows is (R34).

Layer: write, as ``metadata_cli`` is. It names :mod:`cratekit.cli.output` and
nothing else from the command-line layer.
"""

from __future__ import annotations

from typing import Any

from cratekit.cli.output import Envelope
from cratekit.core import analysis_store, config, rb_writer, session
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.write import row_defaults

#: The explicit gate a write is asked behind.
CONFIRM_GATE = "repair.rows.confirm"

#: The plan writes nothing.
NOTHING_TO_WRITE = "rows-defaults-nothing-to-write"

#: What the apply wrote and read back.
DEFAULTS_WRITTEN = "rows-defaults-written"

_ORIGIN = ("write", "row_defaults_cli")


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
                origin=("write.row_defaults_cli",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def build(parser, entry) -> None:
    """Declare the verb. It takes no argument: the plan is every live row lacking a default."""
    del entry
    parser.set_defaults(_handler=repair_rows)


def _confirm_gate(entry):
    """The verb's own gate by name, never by position."""
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


def _payload(plan: row_defaults.DefaultsPlan) -> dict[str, Any]:
    """The plan as the gate digests it and the envelope carries it."""
    return {
        "digest": plan.digest,
        "items": [item.to_json() for item in plan.items],
        "totals": {
            "count": len(plan.items),
            "rows": plan.rows,
            "fills": plan.fills,
            "written": 0,
            "read_back": 0,
        },
        "chunk": None,
    }


def _facts(plan: row_defaults.DefaultsPlan) -> dict[str, Any]:
    """What the gate puts in front of the items: the counts and what is written."""
    return {
        "live rows read": plan.rows,
        "rows to fill": len(plan.items),
        "columns filled, by rows": {
            column: count for column, count in plan.by_column().items() if count
        },
        "values written": {
            column: repr(value) for column, value in rb_writer.CONTENT_ROW_DEFAULTS.items()
        },
        "only into": "a column that is NULL; a value already present is never listed",
    }


def _nothing(plan: row_defaults.DefaultsPlan) -> dict[str, str]:
    return {
        "code": NOTHING_TO_WRITE,
        "message": (
            f"no row lacks a default: all {plan.rows} live row(s) carry every "
            f"column rekordbox fills on a row it makes"
        ),
    }


def _written(written: row_defaults.Written) -> dict[str, str]:
    return {
        "code": DEFAULTS_WRITTEN,
        "message": (
            f"{written.written} row(s) now carry rekordbox's defaults and "
            f"{written.read_back} read back from the database as written, those "
            f"columns and no other; undo with a restore of session {written.session_id}"
        ),
    }


def _plan(cfg: config.Config) -> row_defaults.DefaultsPlan:
    """The plan over the library as it stands, through a handle opened to read."""
    db = rb_writer.open_db(
        rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
    )
    try:
        return row_defaults.plan_rows(db)
    finally:
        rb_writer.close_db(db)


def _write(cfg: config.Config, plan: row_defaults.DefaultsPlan) -> row_defaults.Written:
    """Apply the plan through a handle of this function's own, opened to write."""
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        return row_defaults.apply_rows(
            cfg, db, plan, analysis_roots=analysis_store.watch_roots(cfg)
        )
    finally:
        rb_writer.close_db(db)


def repair_rows(ctx) -> Envelope:
    """Plan every live row lacking a default, ask, then fill them and read them back."""
    cfg = _load()
    spec = _confirm_gate(ctx.entry)
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).
    session.assert_backup_acknowledged(cfg)

    plan = _plan(cfg)
    data = _payload(plan)
    if ctx.gate.require(spec, plan=data, context=_facts(plan)) != "apply":
        return ctx.envelope(data=data, outcome=Outcome.NO_OP)
    if not plan.items:
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=[_nothing(plan)])

    written = _write(cfg, plan)
    row_defaults.assert_read_back(written)
    data["totals"] = {
        **data["totals"],
        "written": written.written,
        "read_back": written.read_back,
    }
    return ctx.envelope(data=data, warnings=[_written(written)])


__all__ = [
    "CONFIRM_GATE",
    "DEFAULTS_WRITTEN",
    "NOTHING_TO_WRITE",
    "build",
    "repair_rows",
]
