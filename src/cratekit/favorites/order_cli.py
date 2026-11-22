"""``crate favorites order``: the Favorites folder put in order newest first (U180).

A one time verb: the folder that holds All Favorites is read, each
playlist's position now and after shown, and on approval the positions are
written in one commit: All Favorites on top, the months newest first,
``Undated``, then everything else in its current relative order. Every
landing, the backfill and the split make a month in its own slot since, so
the verb need not run again.

A FOLDER ALREADY IN ORDER ASKS NOTHING: it opens no gate and ends NO_OP. The
order is :func:`spine.run`'s.

Layer: modules.
"""

from __future__ import annotations

from cratekit.cli.output import Envelope, load_config
from cratekit.core import active_taxonomy, analysis_store, config
from cratekit.favorites import order, placement, spine

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
    with spine.handle(cfg) as db:
        return order.plan(db, source=source)


def written(cfg: config.Config, approved: order.OrderPlan, *, source: str) -> order.Ordered:
    """Apply the plan through a handle of this function's own, opened to write."""
    with spine.handle(cfg, write=True) as db:
        return order.apply(
            cfg, db, approved, source=source, analysis_roots=analysis_store.watch_roots(cfg)
        )


def _done(plan: order.OrderPlan, done: order.Ordered) -> tuple[dict, dict[str, str]]:
    return {"moved": len(done.moved)}, spine.note(
        ORDERED,
        f"{len(done.moved)} playlist(s) moved in {plan.home.folder_name!r}, "
        f"which now reads {', '.join(done.order)}; read back from the "
        f"database in that order, and no membership changed; undo with a "
        f"restore of session {done.session_id}",
    )


def favorites_order(ctx) -> Envelope:
    """Read the Favorites folder, ask, then put it in order newest first."""
    cfg = load_config(_ORIGIN)
    source = placement.source_name(active_taxonomy.load(cfg))
    return spine.run(
        ctx, cfg, APPROVE_GATE, order,
        planned=lambda: planned(cfg, source=source),
        written=lambda plan: written(cfg, plan, source=source),
        idle=lambda plan: spine.note(
            IN_ORDER,
            f"the folder {plan.home.folder_name!r} already reads {source!r} "
            f"first and its months newest first, so nothing was written",
        ),
        done=_done,
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
