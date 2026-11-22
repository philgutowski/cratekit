"""The ``repair.rows`` verb: give a content row rekordbox's own defaults where it
lacks them, and its file's inode where the binding numbered it at random.

A verb (R-923, U115) because the only other way back for such a row is to
remove it in rekordbox and import again, dropping every membership. The
order is ``tag rows``'s: the backup acknowledgment before the plan and the
gate (R-733), the plan made on a read handle closed before the gate, the gate
asked even over an empty plan, and only ``apply`` over a plan that writes
opens the database to write. The second invocation rebuilds the plan, so a
row filled in between refuses ``decision-stale``. The gate takes no inline
answer (R34). Layer: write; it names :mod:`cratekit.cli.output` and nothing
else from the command-line layer.
"""

from __future__ import annotations

from typing import Any

from cratekit.cli.output import Envelope, confirm_gate, load_config
from cratekit.core import analysis_store, config, locations, rb_writer, session
from cratekit.core.cause import Outcome
from cratekit.write import row_defaults

#: The explicit gate a write is asked behind.
CONFIRM_GATE = "repair.rows.confirm"

#: The plan writes nothing.
NOTHING_TO_WRITE = "rows-defaults-nothing-to-write"

#: What the apply wrote and read back.
DEFAULTS_WRITTEN = "rows-defaults-written"

#: The bound decides nothing (off APFS, or the inode counter past the binding's
#: range), so no file id is renumbered (U115).
BOUND_UNDECIDABLE = "rows-file-id-undecidable"

#: Rows above the bound whose file could not be read, so they keep their id.
UNRENUMBERED = "rows-file-id-unrenumbered"

_ORIGIN = ("write", "row_defaults_cli")


def build(parser, entry) -> None:
    """Declare the verb. It takes no argument: the plan is every live row lacking a default."""
    del entry
    parser.set_defaults(_handler=repair_rows)


def _payload(plan: row_defaults.DefaultsPlan) -> dict[str, Any]:
    """The plan as the gate digests it and the envelope carries it."""
    # ``plan/1`` IS CLOSED, so what is not an item lives inside ``totals``: the
    # bound the file ids were judged against and the rows left unrenumbered.
    return {
        "digest": plan.digest,
        "items": [item.to_json() for item in plan.items],
        "totals": {
            "count": len(plan.items),
            "rows": plan.rows,
            "fills": plan.fills,
            "renumbers": plan.renumbers,
            "written": 0,
            "read_back": 0,
            "renumbered": 0,
            "bound": plan.bound,
            "unrenumbered": [one.to_json() for one in plan.unrenumbered],
        },
        "chunk": None,
    }


def _facts(plan: row_defaults.DefaultsPlan) -> dict[str, Any]:
    """What the gate puts in front of the items: the counts and what is written."""
    facts: dict[str, Any] = {
        "live rows read": plan.rows,
        "rows to write": len(plan.items),
        "columns filled, by rows": {
            column: count for column, count in plan.by_column().items() if count
        },
        "value per column, when filled": {
            column: repr(value) for column, value in rb_writer.CONTENT_ROW_DEFAULTS.items()
        },
        "only into": "a column that is NULL; a value already present is never listed",
        f"rows given their file's inode as {row_defaults.FILE_ID}": plan.renumbers,
        "the volume's inode bound": plan.bound,
        "the volume's filesystem": plan.filesystem or "unknown",
        "file ids at or under the bound, left as they are": plan.within_bound,
        "file ids above the bound that are their file's inode, left as they are": (
            plan.matched
        ),
        "file ids of zero, left as they are": plan.zero,
        "file ids above the bound whose file cannot be read, left as they are": len(
            plan.unrenumbered
        ),
    }
    if plan.why_undecidable:
        facts["why no file id is renumbered"] = plan.why_undecidable
    return facts


def _nothing(plan: row_defaults.DefaultsPlan) -> dict[str, str]:
    return {
        "code": NOTHING_TO_WRITE,
        "message": (
            f"no row lacks a default and none carries a random file id: all "
            f"{plan.rows} live row(s) carry every column rekordbox fills on a row "
            f"it makes, and a file id at or under the volume's inode bound"
        ),
    }


def _undecidable(plan: row_defaults.DefaultsPlan) -> dict[str, str]:
    return {
        "code": BOUND_UNDECIDABLE,
        "message": f"no file id was judged random: {plan.why_undecidable}",
    }


def _unrenumbered(plan: row_defaults.DefaultsPlan) -> dict[str, str]:
    shown = row_defaults.named([f"{one.content_id} ({one.why})" for one in plan.unrenumbered])
    return {
        "code": UNRENUMBERED,
        "message": (
            f"{len(plan.unrenumbered)} row(s) carry a file id above the volume's "
            f"inode bound and keep it, since their file could not be read for an "
            f"inode on that volume: {shown}"
        ),
    }


def _notes(plan: row_defaults.DefaultsPlan) -> list[dict[str, str]]:
    """What the plan could not do, said on every envelope that carries it."""
    notes: list[dict[str, str]] = []
    if plan.undecidable:
        notes.append(_undecidable(plan))
    if plan.unrenumbered:
        notes.append(_unrenumbered(plan))
    return notes


def _written(written: row_defaults.Written) -> dict[str, str]:
    return {
        "code": DEFAULTS_WRITTEN,
        "message": (
            f"{written.written} row(s) now carry rekordbox's defaults, "
            f"{written.renumbered} of them their file's inode as "
            f"{row_defaults.FILE_ID}, and {written.read_back} read back from the "
            f"database as written, those columns and no other; undo with a restore "
            f"of session {written.session_id}"
        ),
    }


def _plan(cfg: config.Config) -> row_defaults.DefaultsPlan:
    """The plan over the library as it stands, through a handle opened to read.

    The bound is measured first, so the file it creates and removes is never
    inside a handle's lifetime.
    """
    bound = row_defaults.inode_bound(cfg)
    db = rb_writer.open_db(
        rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
    )
    try:
        return row_defaults.plan_rows(
            db,
            root=cfg.library.root,
            prefix_map=locations.prefix_rules(cfg.resolved_prefix_map()),
            bound=bound,
        )
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
    cfg = load_config(("write.row_defaults_cli",))
    spec = confirm_gate(ctx.entry, CONFIRM_GATE, origin=_ORIGIN)
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).
    session.assert_backup_acknowledged(cfg)

    plan = _plan(cfg)
    data = _payload(plan)
    if ctx.gate.require(spec, plan=data, context=_facts(plan)) != "apply":
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=_notes(plan))
    if not plan.items:
        return ctx.envelope(
            data=data, outcome=Outcome.NO_OP, warnings=[_nothing(plan), *_notes(plan)]
        )

    written = _write(cfg, plan)
    row_defaults.assert_read_back(written)
    data["totals"] = {
        **data["totals"],
        "written": written.written,
        "read_back": written.read_back,
        "renumbered": written.renumbered,
    }
    return ctx.envelope(data=data, warnings=[_written(written), *_notes(plan)])


__all__ = [
    "BOUND_UNDECIDABLE", "CONFIRM_GATE", "DEFAULTS_WRITTEN", "NOTHING_TO_WRITE", "UNRENUMBERED",
    "build", "repair_rows",
]
