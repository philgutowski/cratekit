"""``crate favorites backfill``: the hearts this product landed, put where a landing now puts them (U120).

The attended half of U120. A heart the favourites sync landed before this
unit sits in its INBOX batch and nowhere else; this verb finds every such
heart, shows each one with the quarter it goes to, asks, and adds it to All
Favorites and its quarter playlist in one guarded commit. It removes nothing
and moves nothing, so a second run over a placed library asks and writes
nothing.

THE ORDER IS THE REFRESH VERB'S: the backup acknowledgment before anything
is gathered (R-733), the plan on a handle opened to read and closed, the gate
over the digested plan, the write on a handle opened with write intent that
takes the plan again and refuses a digest that moved. The hearts themselves
are gathered once, since finding them walks the library.

Layer: modules.
"""

from __future__ import annotations

from typing import Any

from cratekit.cli.output import Envelope
from cratekit.core import active_taxonomy, analysis_store, config, rb_writer, session
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, Remedy
from cratekit.favorites import backfill, placement

#: The gate, explicit: a write to the live library's playlists.
APPROVE_GATE = "favorites.backfill.approve"

#: The notes the verb carries on its warnings channel.
NOTHING_TO_PLACE = "favorites-nothing-to-place"
PLACED = "favorites-backfilled"
UNDATED = "favorites-hearts-undated"

_ORIGIN = ("favorites", "backfill_cli")


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
    parser.set_defaults(_handler=favorites_backfill)


def _approve_gate(entry):
    for spec in entry.gates:
        if spec.name == APPROVE_GATE:
            return spec
    raise RuntimeError(f"registry entry {entry.name!r} declares no gate {APPROVE_GATE!r}")


def planned(cfg: config.Config, *, source: str) -> backfill.BackfillPlan:
    """The plan over the library as it stands, through a handle opened to read and closed."""
    db = rb_writer.open_db(
        rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
    )
    try:
        return backfill.plan(cfg, db, source=source)
    finally:
        rb_writer.close_db(db)


def written(
    cfg: config.Config, approved: backfill.BackfillPlan, *, source: str
) -> backfill.Backfilled:
    """Apply the plan through a handle of this function's own, opened to write."""
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        return backfill.apply(
            cfg, db, approved, source=source, analysis_roots=analysis_store.watch_roots(cfg)
        )
    finally:
        rb_writer.close_db(db)


def _undated_note(plan: backfill.BackfillPlan) -> list[dict[str, str]]:
    if not plan.undated:
        return []
    return [
        {
            "code": UNDATED,
            "message": (
                f"{plan.undated} heart(s) carry no date on their job and the account "
                f"dates them nowhere, so they go to {placement.placeholders.UNDATED!r} "
                f"and stay there; nothing moves a heart to its quarter later"
            ),
        }
    ]


def favorites_backfill(ctx) -> Envelope:
    """Find the landed hearts, ask, then place them and read them back."""
    cfg = _load()
    source = placement.source_name(active_taxonomy.load(cfg))
    spec = _approve_gate(ctx.entry)
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).
    session.assert_backup_acknowledged(cfg)

    plan = planned(cfg, source=source)
    data = backfill.payload(plan, cfg)
    warnings = _undated_note(plan)
    if ctx.gate.require(spec, plan=data, context=backfill.facts(plan)) != "approve":
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=warnings)
    if not plan.writes:
        return ctx.envelope(
            data=data,
            outcome=Outcome.NO_OP,
            warnings=[
                *warnings,
                {
                    "code": NOTHING_TO_PLACE,
                    "message": (
                        f"{len(plan.hearts)} landed heart(s) found and every one is already "
                        f"in {source!r} and its quarter playlist, so nothing was written"
                    ),
                },
            ],
        )

    done = written(cfg, plan, source=source)
    backfill.assert_read_back(done)
    placed = done.placed
    totals: dict[str, Any] = {
        **data["totals"],
        "added": placed.added,
        "created": len(placed.created),
    }
    quarters = ", ".join(
        f"{name}{' (made)' if name in placed.created else ''}" for name, _row, _n in placed.quarters
    )
    return ctx.envelope(
        data={**data, "totals": totals},
        warnings=[
            *warnings,
            {
                "code": PLACED,
                "message": (
                    f"{placed.added} membership(s) added for {len(plan.hearts)} landed "
                    f"heart(s): {placed.added_source} into {source!r} and the rest into "
                    f"{quarters}; every playlist read back from the database holds its "
                    f"hearts, and no track left the collection; undo with a restore of "
                    f"session {done.session_id}"
                ),
            },
        ],
    )


__all__ = [
    "APPROVE_GATE",
    "NOTHING_TO_PLACE",
    "PLACED",
    "UNDATED",
    "build",
    "favorites_backfill",
    "planned",
    "written",
]
