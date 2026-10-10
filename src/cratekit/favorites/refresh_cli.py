"""``crate favorites refresh``: every genre folder's Favorites made to mirror All Favorites (U119).

The one path that REMOVES a genre Favorites membership, behind its own
explicit gate, the way every writer in this product that takes a membership
away stands behind one. It plans every folder against the library as it
stands, shows each folder's adds and removes, asks, and writes both halves
through the genre favorites engine, the additions in one commit and the
removals in a second. The additive half also runs at the end of an adoption
that files a track, and the rebuild files the same placements, so this verb
is where a favourite that left All Favorites, or a track added to a genre
Favorites by hand, is taken out.

THE ORDER IS THE MEMBERSHIP MOVE'S: the backup acknowledgment before the plan
(R-733), the plan on a handle opened to read and closed, the gate over the
digested plan, the write on a handle opened with write intent that takes the
plan again and refuses a digest that moved. Database native routing trees
only; the bridge's writers emit an export, and the engine refuses a tree on
the bridge by name.

Layer: modules.
"""

from __future__ import annotations

from typing import Any

from cratekit.cli.output import Envelope
from cratekit.core import (
    active_taxonomy,
    analysis_store,
    config,
    rb_writer,
    session,
    tree_registry,
)
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, Remedy, refuse
from cratekit.write import genre_favorites

#: The gate, explicit: a removal is the one write that takes something away.
APPROVE_GATE = "favorites.refresh.approve"

#: The notes the verb carries on its warnings channel.
NOTHING_TO_REFRESH = "favorites-nothing-to-refresh"
REFRESHED = "favorites-refreshed"
LEFT_ALONE = "favorites-folders-left-alone"

_ORIGIN = ("favorites", "refresh_cli")


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
                origin=_ORIGIN,
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def build(parser, entry) -> None:
    parser.set_defaults(_handler=favorites_refresh)


def _approve_gate(entry):
    for spec in entry.gates:
        if spec.name == APPROVE_GATE:
            return spec
    raise RuntimeError(f"registry entry {entry.name!r} declares no gate {APPROVE_GATE!r}")


def planned(
    cfg: config.Config, declared, registry: tree_registry.Registry
) -> genre_favorites.RefreshPlan:
    """The plan over the tree as it stands, through a handle opened to read and closed."""
    db = rb_writer.open_db(
        rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
    )
    try:
        return genre_favorites.plan_refresh(cfg, db, declared, registry)
    finally:
        rb_writer.close_db(db)


def written(
    cfg: config.Config,
    declared,
    registry: tree_registry.Registry,
    plan: genre_favorites.RefreshPlan,
) -> genre_favorites.Refreshed:
    """Apply the plan, both halves, through a handle of this function's own, opened to write."""
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        return genre_favorites.apply_refresh(
            cfg,
            db,
            plan,
            declared=declared,
            registry=registry,
            analysis_roots=analysis_store.watch_roots(cfg),
            remove=True,
        )
    finally:
        rb_writer.close_db(db)


def _left_alone(plan: genre_favorites.RefreshPlan) -> list[dict[str, str]]:
    if not plan.unclaimed:
        return []
    return [
        {
            "code": LEFT_ALONE,
            "message": (
                f"{len(plan.unclaimed)} folder(s) under the tree are nobody's declared "
                f"bucket, or two folders carry one bucket's name, and were left alone: "
                + ", ".join(plan.unclaimed)
            ),
        }
    ]


def favorites_refresh(ctx) -> Envelope:
    """Plan every folder's Favorites, ask, then add and remove and read back."""
    cfg = _load()
    declared = active_taxonomy.load(cfg)
    registry = tree_registry.read(cfg)
    spec = _approve_gate(ctx.entry)
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).
    session.assert_backup_acknowledged(cfg)

    plan = planned(cfg, declared, registry)
    data = genre_favorites.payload(plan)
    warnings = _left_alone(plan)
    if ctx.gate.require(spec, plan=data, context=genre_favorites.facts(plan)) != "approve":
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=warnings)
    if not plan.writes:
        return ctx.envelope(
            data=data,
            outcome=Outcome.NO_OP,
            warnings=[
                *warnings,
                {
                    "code": NOTHING_TO_REFRESH,
                    "message": (
                        f"every genre Favorites already mirrors {plan.source_name!r}: "
                        f"{len(plan.folders)} folder(s) checked, {plan.favourites} "
                        f"favourite(s), nothing to add or remove"
                    ),
                },
            ],
        )

    try:
        refreshed = written(cfg, declared, registry, plan)
    except genre_favorites.RefreshInterrupted as exc:
        # THE ADDITIONS LANDED. Said with the count and the session, and the
        # failure that stopped the removals beside it, keeping its own reason
        # when it has one.
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
    genre_favorites.assert_read_back(refreshed)
    totals: dict[str, Any] = {
        **data["totals"],
        "added": refreshed.added,
        "removed": refreshed.removed,
        "created": len(refreshed.created),
    }
    return ctx.envelope(
        data={**data, "totals": totals},
        warnings=[
            *warnings,
            {
                "code": REFRESHED,
                "message": (
                    f"{refreshed.added} membership(s) added and {refreshed.removed} removed "
                    f"across {len(plan.folders)} genre folder(s), "
                    f"{len(refreshed.created)} Favorites playlist(s) created; every folder "
                    f"read back from the database as its plan, and no track left the "
                    f"collection; undo with a restore of session {refreshed.session_id}"
                ),
            },
        ],
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
