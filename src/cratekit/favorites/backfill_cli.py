"""``crate favorites backfill``: every owned heart, put where a landing now puts them (U120, U146).

Each heart a hearts job reported whose track the library holds and All
Favorites lacks is shown with its month, and on approval added to All
Favorites and its month in one guarded commit; nothing is removed or moved.
The order is :func:`spine.run`'s, the gate asked before the nothing to place check.

Layer: modules.
"""

from __future__ import annotations

from cratekit.cli.output import Envelope, load_config
from cratekit.core import active_taxonomy
from cratekit.favorites import backfill, colour, placement, spine

#: The gate, explicit: a write to the live library's playlists.
APPROVE_GATE = "favorites.backfill.approve"

#: The notes the verb carries on its warnings channel.
NOTHING_TO_PLACE = "favorites-nothing-to-place"
PLACED = "favorites-backfilled"
UNDATED = "favorites-hearts-undated"
HELD_BACK = "favorites-hearts-held-back"
JOBS_UNREAD = "favorites-jobs-unread"
TAKEN_BACK = "favorites-hearts-taken-back"
#: A row a person coloured otherwise, left as it is and named (U153).
COLOUR_HELD = "favorites-colour-held"
#: No live Pink row, so the memberships are placed and nothing is coloured (U153).
PINK_MISSING = colour.PINK_COLOUR_MISSING

_ORIGIN = ("favorites", "backfill_cli")


def build(parser, entry) -> None:
    parser.set_defaults(_handler=favorites_backfill)


#: The plan on a handle opened to read and closed, and the write on its own write handle.
planned, written = spine.handles(backfill)


def _notes(plan: backfill.BackfillPlan) -> list[dict[str, str]]:
    """What a person reads about the plan beside its counts, whatever the answer."""
    why = (
        f"the account's hearts listed short, {plan.withheld} withheld by the provider"
        if plan.withheld
        else "the account's hearts listed with no published count"
    )
    shown = plan.placements
    return spine.notes(
        (
            plan.undated,
            UNDATED,
            f"{plan.undated} heart(s) carry no date on their job or on the account, "
            f"so they go to {placement.placeholders.UNDATED!r} "
            f"and stay there; nothing moves a heart to its month later",
        ),
        (
            plan.held_back,
            HELD_BACK,
            f"{len(plan.held_back)} heart(s) were held back unplaced: "
            f"{why}, so a heart the listing lacks cannot be told from one "
            f"withheld; run again when the listing is whole",
        ),
        (
            plan.taken_back,
            TAKEN_BACK,
            f"{len(plan.taken_back)} heart(s) the author took back were not placed: "
            + "; ".join(f"{one.title} ({one.dated_by})" for one in plan.taken_back),
        ),
        (
            plan.unreadable,
            JOBS_UNREAD,
            f"{len(plan.unreadable)} hearts job(s) could not be read and were "
            f"skipped: {', '.join(plan.unreadable)}; a heart only such a job "
            f"carried is not placed",
        ),
        (
            shown.colour_skipped,
            PINK_MISSING,
            f"no row is coloured: {shown.colour_skipped}; the "
            f"memberships are placed all the same, and a later run colours "
            f"them once the library carries Pink again",
        ),
        (
            shown.held,
            COLOUR_HELD,
            f"{len(shown.held)} row(s) carry a colour a person chose "
            f"and keep it: " + "; ".join(one.said() for one in shown.held),
        ),
    )


def _done(plan: backfill.BackfillPlan, done: backfill.Backfilled) -> tuple[dict, dict[str, str]]:
    placed = done.placed
    totals = {
        "added": placed.added,
        "created": len(placed.created),
        "coloured": len(placed.coloured),
    }
    return totals, spine.note(
        PLACED,
        f"{placed.said()}, for {len(plan.hearts)} owned heart(s) and "
        f"{len(plan.placements.recolour)} placed row(s); every "
        f"playlist read back from the database holds its hearts, every "
        f"coloured row reads Pink, and no track left the collection; undo "
        f"with a restore of session {done.session_id}",
    )


def favorites_backfill(ctx) -> Envelope:
    """Find the owned hearts to place, ask, then place them and read them back."""
    cfg = load_config(_ORIGIN)
    source = placement.source_name(active_taxonomy.load(cfg))
    return spine.run(
        ctx, cfg, APPROVE_GATE, backfill,
        planned=lambda: planned(cfg, source=source),
        written=lambda plan: written(cfg, plan, source=source),
        payload=lambda plan: backfill.payload(plan, cfg),
        idle=lambda plan: spine.note(
            NOTHING_TO_PLACE,
            f"no owned heart needs placing, {plan.already} already in "
            f"{source!r} and a month playlist, and every member of "
            f"{source!r} is coloured or held, so nothing was written",
        ),
        told=_notes,
        done=_done,
        gate_first=True,
    )


__all__ = [
    "APPROVE_GATE",
    "COLOUR_HELD",
    "HELD_BACK",
    "JOBS_UNREAD",
    "NOTHING_TO_PLACE",
    "PINK_MISSING",
    "PLACED",
    "TAKEN_BACK",
    "UNDATED",
    "build",
    "favorites_backfill",
    "planned",
    "written",
]
