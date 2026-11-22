"""``crate favorites order``: the Favorites folder put in order newest first (U180).

A one time verb. Until U180 a month playlist was made at the end of the
folder that holds All Favorites, so the folder read oldest first. This verb
reads the folder, shows each playlist's position now and after, asks, and
then writes the positions in one commit: All Favorites on top, the months
newest first, ``Undated``, then everything else in its current relative
order. From then on a month is made in its own slot by every landing, the
backfill and the split, so the verb need not run again.

A FOLDER ALREADY IN ORDER ASKS NOTHING. Its plan writes nothing, so the verb
reads the folder, opens no gate and ends NO_OP.

THE ORDER IS THE SPLIT'S: the backup acknowledgment before anything is read
(R-733), the plan on a handle opened to read and closed, the gate over the
digested plan, the write on a handle opened with write intent that takes the
plan again and refuses a digest that moved.

Layer: modules.
"""

from __future__ import annotations

from cratekit.cli.output import Envelope, declared_gate, load_config
from cratekit.core import active_taxonomy, analysis_store, config, rb_writer, session
from cratekit.core.cause import Outcome
from cratekit.favorites import order, placement

#: The gate, explicit: a write to the positions of the live library's playlists.
APPROVE_GATE = "favorites.order.approve"

#: The notes the verb carries on its warnings channel.
IN_ORDER = "favorites-in-order"
ORDERED = "favorites-ordered"

_ORIGIN = ("favorites", "order_cli")


def build(parser, entry) -> None:
    parser.set_defaults(_handler=favorites_order)


def planned(cfg: config.Config, *, source: str) -> order.OrderPlan:
    """The plan over the library as it stands, through a handle opened to read and closed."""
    db = rb_writer.open_db(
        rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
    )
    try:
        return order.plan(db, source=source)
    finally:
        rb_writer.close_db(db)


def written(cfg: config.Config, approved: order.OrderPlan, *, source: str) -> order.Ordered:
    """Apply the plan through a handle of this function's own, opened to write."""
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        return order.apply(
            cfg, db, approved, source=source, analysis_roots=analysis_store.watch_roots(cfg)
        )
    finally:
        rb_writer.close_db(db)


def favorites_order(ctx) -> Envelope:
    """Read the Favorites folder, ask, then put it in order newest first."""
    cfg = load_config(_ORIGIN)
    source = placement.source_name(active_taxonomy.load(cfg))
    spec = declared_gate(ctx.entry, APPROVE_GATE)
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).
    session.assert_backup_acknowledged(cfg)

    plan = planned(cfg, source=source)
    data = order.payload(plan)
    if not plan.writes:
        # IN ORDER, NO QUESTION: there is nothing to approve, so a run over a
        # folder already in order opens no gate.
        return ctx.envelope(
            data=data,
            outcome=Outcome.NO_OP,
            warnings=[
                {
                    "code": IN_ORDER,
                    "message": (
                        f"the folder {plan.home.folder_name!r} already reads {source!r} "
                        f"first and its months newest first, so nothing was written"
                    ),
                }
            ],
        )
    if ctx.gate.require(spec, plan=data, context=order.facts(plan)) != "approve":
        return ctx.envelope(data=data, outcome=Outcome.NO_OP)

    done = written(cfg, plan, source=source)
    order.assert_read_back(done)
    totals = {**data["totals"], "moved": len(done.moved)}
    return ctx.envelope(
        data={**data, "totals": totals},
        warnings=[
            {
                "code": ORDERED,
                "message": (
                    f"{len(done.moved)} playlist(s) moved in {plan.home.folder_name!r}, "
                    f"which now reads {', '.join(done.order)}; read back from the "
                    f"database in that order, and no membership changed; undo with a "
                    f"restore of session {done.session_id}"
                ),
            },
        ],
    )


__all__ = [
    "APPROVE_GATE",
    "IN_ORDER",
    "ORDERED",
    "build",
    "favorites_order",
    "planned",
    "written",
]
