"""``crate favorites split``: the quarter playlists under Favorites split into months and retired (U145).

A one time verb: each month it fills or makes and each quarter it retires is
shown, and on approval the memberships go in one commit and the emptied
quarters are retired in a second. A member dated nowhere goes to ``Undated``.
A library with no quarter left asks nothing, and a run stopped between its two
commits plans the same split again and finishes. The order is :func:`spine.run`'s.

Layer: modules.
"""

from __future__ import annotations

from cratekit.cli.output import Envelope, load_config
from cratekit.core import active_taxonomy
from cratekit.favorites import placeholders, placement, spine, split

#: The gate, explicit: a write that retires playlists of the live library.
APPROVE_GATE = "favorites.split.approve"

#: The notes the verb carries on its warnings channel.
NOTHING_TO_SPLIT = "favorites-no-quarter-left"
SPLIT = "favorites-quarters-split"
UNDATED = "favorites-split-undated"
JOBS_UNREAD = "favorites-split-jobs-unread"
WITHHELD = "favorites-split-hearts-withheld"
TAKEN_BACK = "favorites-split-hearts-taken-back"

_ORIGIN = ("favorites", "split_cli")


def build(parser, entry) -> None:
    parser.set_defaults(_handler=favorites_split)


#: The plan on a handle opened to read and closed, and the write on its own write handle.
planned, written = spine.handles(split)


def _members(said: tuple[split.Member, ...]) -> str:
    return "; ".join(
        f"{one.title or 'row ' + one.content_id} (from {', '.join(one.quarters)})" for one in said
    )


def _notes(plan: split.SplitPlan) -> list[dict[str, str]]:
    """What a person reads about the plan beside its counts, whatever the answer."""
    return spine.notes(
        (
            plan.undated,
            UNDATED,
            f"{len(plan.undated)} member(s) carry no date on any hearts job and the "
            f"account dates them nowhere, so they go to {placeholders.UNDATED!r} "
            f"and stay there: " + _members(plan.undated),
        ),
        (
            plan.taken_back,
            TAKEN_BACK,
            f"{len(plan.taken_back)} member(s) the author took out of "
            f"{plan.home.source_name!r} by hand go to no month, and their quarter "
            f"is retired all the same: " + _members(plan.taken_back),
        ),
        (
            plan.withheld,
            WITHHELD,
            f"the account's hearts listed short, {plan.withheld} withheld by the "
            f"provider, which does not say which; a member undated here may be one",
        ),
        (
            plan.unreadable,
            JOBS_UNREAD,
            f"{len(plan.unreadable)} hearts job(s) could not be read and were "
            f"skipped: {', '.join(plan.unreadable)}; a date only such a job froze "
            f"was not read",
        ),
    )


def _done(plan: split.SplitPlan, done: split.Split) -> tuple[dict, dict[str, str]]:
    months = ", ".join(
        f"{name} {count}{' (made)' if name in done.created else ''}"
        for name, _row, count in done.months
    )
    totals = {"added": done.added, "created": len(done.created), "retired": len(done.retired)}
    return totals, spine.note(
        SPLIT,
        f"{done.added} membership(s) added for {len(plan.members)} member(s) "
        f"of {len(done.retired)} quarter playlist(s), into {months}; "
        f"{', '.join(done.retired)} retired; every month read back from the "
        f"database holds its members, and no track left the collection; undo "
        f"with a restore of session {done.session_id}",
    )


def favorites_split(ctx) -> Envelope:
    """Find the quarter playlists, ask, then split them into months and retire them."""
    cfg = load_config(_ORIGIN)
    source = placement.source_name(active_taxonomy.load(cfg))
    return spine.run(
        ctx, cfg, APPROVE_GATE, split,
        planned=lambda: planned(cfg, source=source),
        written=lambda plan: written(cfg, plan, source=source),
        idle=lambda plan: spine.note(
            NOTHING_TO_SPLIT,
            f"no quarter playlist sits beside {source!r}, so there is "
            f"nothing to split and nothing was written",
        ),
        told=_notes,
        done=_done,
    )


__all__ = [
    "APPROVE_GATE",
    "JOBS_UNREAD",
    "NOTHING_TO_SPLIT",
    "SPLIT",
    "TAKEN_BACK",
    "UNDATED",
    "WITHHELD",
    "build",
    "favorites_split",
    "planned",
    "written",
]
