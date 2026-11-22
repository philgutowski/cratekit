"""``crate favorites refresh``: every genre folder's Favorites made to mirror All Favorites (U119).

The one path that REMOVES a genre Favorites membership, behind its own
explicit gate, as every writer that takes a membership away stands behind
one. Every folder is planned against the library as it stands, its adds and
removes shown, and on approval both halves are written through the genre
favorites engine, the additions in one commit and the removals in a second.
The additive half also runs after an adoption that files a track and in the
rebuild, so this verb is where a favourite that left All Favorites, or a
track added to a genre Favorites by hand, is taken out.

The order is :func:`spine.run`'s, the gate asked before the nothing to
refresh check. Database native routing trees only; the engine refuses a tree
on the bridge by name.

Layer: modules.
"""

from __future__ import annotations

from cratekit.cli.output import Envelope, load_config
from cratekit.core import active_taxonomy, analysis_store, config, tree_registry
from cratekit.core.cause import CratekitError, Remedy, refuse
from cratekit.favorites import spine
from cratekit.write import genre_favorites

#: The gate, explicit: a removal is the one write that takes something away.
APPROVE_GATE = "favorites.refresh.approve"

#: The notes the verb carries on its warnings channel.
NOTHING_TO_REFRESH = "favorites-nothing-to-refresh"
REFRESHED = "favorites-refreshed"
LEFT_ALONE = "favorites-folders-left-alone"

_ORIGIN = ("favorites", "refresh_cli")


def build(parser, entry) -> None:
    parser.set_defaults(_handler=favorites_refresh)


def planned(
    cfg: config.Config, declared, registry: tree_registry.Registry
) -> genre_favorites.RefreshPlan:
    """The plan over the tree as it stands, through a handle opened to read and closed."""
    with spine.handle(cfg) as db:
        return genre_favorites.plan_refresh(cfg, db, declared, registry)


def written(
    cfg: config.Config,
    declared,
    registry: tree_registry.Registry,
    plan: genre_favorites.RefreshPlan,
) -> genre_favorites.Refreshed:
    """Apply the plan, both halves, through a handle of this function's own, opened to write."""
    with spine.handle(cfg, write=True) as db:
        return genre_favorites.apply_refresh(
            cfg,
            db,
            plan,
            declared=declared,
            registry=registry,
            analysis_roots=analysis_store.watch_roots(cfg),
            remove=True,
        )


def _left_alone(plan: genre_favorites.RefreshPlan) -> list[dict[str, str]]:
    return spine.notes(
        (
            plan.unclaimed,
            LEFT_ALONE,
            f"{len(plan.unclaimed)} folder(s) under the tree are nobody's declared "
            f"bucket, or two folders carry one bucket's name, and were left alone: "
            + ", ".join(plan.unclaimed),
        )
    )


def _written(cfg, declared, registry, plan) -> genre_favorites.Refreshed:
    """The write, an interruption between its two commits said with what landed."""
    try:
        return written(cfg, declared, registry, plan)
    except genre_favorites.RefreshInterrupted as exc:
        # THE ADDITIONS LANDED: said with the count and the session, and the
        # failure that stopped the removals, keeping its own reason when it has one.
        inner = exc.__cause__
        cause = inner.cause if isinstance(inner, CratekitError) else None
        raise refuse(
            cause.reason if cause is not None else "internal-error",
            f"the refresh added {exc.partial.added} membership(s), committed in session "
            f"{exc.partial.session_id}, and then stopped before the removals were made "
            f"({cause.message if cause is not None else inner}); every favourite is in "
            f"its genre Favorites and nothing was taken out, so run it again to finish",
            remedy=cause.remediation.remedy if cause is not None else Remedy.REPORT_DEFECT,
            steps=cause.remediation.steps if cause is not None else (),
            origin=_ORIGIN,
            detail={"added": exc.partial.added, "session": exc.partial.session_id},
            inner=cause,
        ) from exc


def _done(
    plan: genre_favorites.RefreshPlan, done: genre_favorites.Refreshed
) -> tuple[dict, dict[str, str]]:
    totals = {"added": done.added, "removed": done.removed, "created": len(done.created)}
    return totals, spine.note(
        REFRESHED,
        f"{done.added} membership(s) added and {done.removed} removed "
        f"across {len(plan.folders)} genre folder(s), "
        f"{len(done.created)} Favorites playlist(s) created; every folder "
        f"read back from the database as its plan, and no track left the "
        f"collection; undo with a restore of session {done.session_id}",
    )


def favorites_refresh(ctx) -> Envelope:
    """Plan every folder's Favorites, ask, then add and remove and read back."""
    cfg = load_config(_ORIGIN)
    declared = active_taxonomy.load(cfg)
    registry = tree_registry.read(cfg)
    return spine.run(
        ctx, cfg, APPROVE_GATE, genre_favorites,
        planned=lambda: planned(cfg, declared, registry),
        written=lambda plan: _written(cfg, declared, registry, plan),
        idle=lambda plan: spine.note(
            NOTHING_TO_REFRESH,
            f"every genre Favorites already mirrors {plan.source_name!r}: "
            f"{len(plan.folders)} folder(s) checked, {plan.favourites} "
            f"favourite(s), nothing to add or remove",
        ),
        told=_left_alone,
        done=_done,
        gate_first=True,
    )


__all__ = [
    "APPROVE_GATE",
    "LEFT_ALONE",
    "NOTHING_TO_REFRESH",
    "REFRESHED",
    "build",
    "favorites_refresh",
    "planned",
    "written",
]
