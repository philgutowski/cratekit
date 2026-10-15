"""``crate favorites split``: the quarter playlists under Favorites split into months and retired (U145).

A one time verb. Until U145 a landed heart went into its quarter's playlist,
``2026-Q4``; since U145 it goes into its month's, ``2026-10``. This verb
finds every quarter playlist beside All Favorites, dates each member, shows
each month playlist it will fill or make with its count and each quarter it
will retire, asks, and then adds the memberships in one commit and retires
the emptied quarters in a second. A member dated nowhere goes to ``Undated``
and is named.

A LIBRARY WITH NO QUARTER LEFT ASKS NOTHING. Once the quarters are retired
there is nothing to plan, so a second run reads the folder, opens no gate and
ends NO_OP. A run stopped between its two commits plans the same split again,
is approved against the same digest, and finishes.

THE ORDER IS THE BACKFILL'S: the backup acknowledgment before anything is
read (R-733), the plan on a handle opened to read and closed, the gate over
the digested plan, the write on a handle opened with write intent that takes
the plan again and refuses a digest that moved.

Layer: modules.
"""

from __future__ import annotations

from typing import Any

from cratekit.cli.output import Envelope
from cratekit.core import active_taxonomy, analysis_store, config, rb_writer, session
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, Remedy
from cratekit.favorites import placeholders, placement, split

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
    parser.set_defaults(_handler=favorites_split)


def _approve_gate(entry):
    for spec in entry.gates:
        if spec.name == APPROVE_GATE:
            return spec
    raise RuntimeError(f"registry entry {entry.name!r} declares no gate {APPROVE_GATE!r}")


def planned(cfg: config.Config, *, source: str) -> split.SplitPlan:
    """The plan over the library as it stands, through a handle opened to read and closed."""
    db = rb_writer.open_db(
        rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
    )
    try:
        return split.plan(cfg, db, source=source)
    finally:
        rb_writer.close_db(db)


def written(cfg: config.Config, approved: split.SplitPlan, *, source: str) -> split.Split:
    """Apply the plan through a handle of this function's own, opened to write."""
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        return split.apply(
            cfg, db, approved, source=source, analysis_roots=analysis_store.watch_roots(cfg)
        )
    finally:
        rb_writer.close_db(db)


def _notes(plan: split.SplitPlan) -> list[dict[str, str]]:
    """What a person reads about the plan beside its counts, whatever the answer."""
    notes: list[dict[str, str]] = []
    if plan.undated:
        notes.append(
            {
                "code": UNDATED,
                "message": (
                    f"{len(plan.undated)} member(s) carry no date on any hearts job and the "
                    f"account dates them nowhere, so they go to {placeholders.UNDATED!r} "
                    f"and stay there: "
                    + "; ".join(
                        f"{one.title or 'row ' + one.content_id} (from {', '.join(one.quarters)})"
                        for one in plan.undated
                    )
                ),
            }
        )
    if plan.taken_back:
        notes.append(
            {
                "code": TAKEN_BACK,
                "message": (
                    f"{len(plan.taken_back)} member(s) the author took out of "
                    f"{plan.home.source_name!r} by hand go to no month, and their quarter "
                    f"is retired all the same: "
                    + "; ".join(
                        f"{one.title or 'row ' + one.content_id} (from {', '.join(one.quarters)})"
                        for one in plan.taken_back
                    )
                ),
            }
        )
    if plan.withheld:
        notes.append(
            {
                "code": WITHHELD,
                "message": (
                    f"the account's hearts listed short, {plan.withheld} withheld by the "
                    f"provider, which does not say which; a member undated here may be one"
                ),
            }
        )
    if plan.unreadable:
        notes.append(
            {
                "code": JOBS_UNREAD,
                "message": (
                    f"{len(plan.unreadable)} hearts job(s) could not be read and were "
                    f"skipped: {', '.join(plan.unreadable)}; a date only such a job froze "
                    f"was not read"
                ),
            }
        )
    return notes


def favorites_split(ctx) -> Envelope:
    """Find the quarter playlists, ask, then split them into months and retire them."""
    cfg = _load()
    source = placement.source_name(active_taxonomy.load(cfg))
    spec = _approve_gate(ctx.entry)
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).
    session.assert_backup_acknowledged(cfg)

    plan = planned(cfg, source=source)
    data = split.payload(plan)
    if not plan.writes:
        # NO QUARTER, NO QUESTION: there is nothing to approve, so a second
        # run over a split library opens no gate.
        return ctx.envelope(
            data=data,
            outcome=Outcome.NO_OP,
            warnings=[
                {
                    "code": NOTHING_TO_SPLIT,
                    "message": (
                        f"no quarter playlist sits beside {source!r}, so there is "
                        f"nothing to split and nothing was written"
                    ),
                }
            ],
        )
    warnings = _notes(plan)
    if ctx.gate.require(spec, plan=data, context=split.facts(plan)) != "approve":
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=warnings)

    done = written(cfg, plan, source=source)
    split.assert_read_back(done)
    totals: dict[str, Any] = {
        **data["totals"],
        "added": done.added,
        "created": len(done.created),
        "retired": len(done.retired),
    }
    months = ", ".join(
        f"{name} {count}{' (made)' if name in done.created else ''}"
        for name, _row, count in done.months
    )
    return ctx.envelope(
        data={**data, "totals": totals},
        warnings=[
            *warnings,
            {
                "code": SPLIT,
                "message": (
                    f"{done.added} membership(s) added for {len(plan.members)} member(s) "
                    f"of {len(done.retired)} quarter playlist(s), into {months}; "
                    f"{', '.join(done.retired)} retired; every month read back from the "
                    f"database holds its members, and no track left the collection; undo "
                    f"with a restore of session {done.session_id}"
                ),
            },
        ],
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
