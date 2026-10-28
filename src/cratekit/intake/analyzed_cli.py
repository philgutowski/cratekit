"""``crate inbox analyzed``: take every analysed row out of INBOX / Analyze (U166).

The engine is :mod:`cratekit.intake.analyzed`, and its docstring says what
analysed means and what the removal touches. This module is the order a person
meets it in, which is ``inbox refill``'s:

* the backup acknowledgment is read before the plan and before the gate
  (R-733);
* the plan is made on a handle opened to READ and closed before the gate, and
  a library whose intake tree is still on the bridge refuses there, naming
  ``tree cutover``;
* the explicit gate is asked over the digested plan, AND AN EMPTY PLAN STILL
  ASKS, so a run after a visit that analysed nothing is a question answered
  and ends ``no_op``;
* only ``apply`` over a plan that clears a row opens the database with write
  intent, and the engine takes the plan again on that handle and refuses
  ``decision-stale`` when anything moved in between.

THE ITEMS ARE EVERY ROW THE PLAYLIST HOLDS, the ones it clears and the ones it
leaves with why, so the screen a person approves names what stays as well as
what goes.

Layer: modules. It names :mod:`cratekit.cli.output` and nothing else from the
command-line layer, for the reason ``adopt.apply_cli`` gives.
"""

from __future__ import annotations

from collections import Counter
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
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation
from cratekit.core.exit_codes import Remedy
from cratekit.intake import analyzed, land_cli

#: The explicit gate the clear is asked behind.
APPROVE_GATE = "inbox.analyzed.approve"

#: The plan clears no row.
NOTHING = "analyzed-nothing-planned"

#: What the apply removed, read back.
CLEARED = "analyzed-cleared"

#: Rows that stay because rekordbox has not finished with them.
WAITING = "analyzed-rows-waiting"


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
                origin=("intake.analyzed_cli",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def build(parser, entry) -> None:
    """Declare the verb. THERE IS NO ``--yes``: the gate is the only answer."""
    del entry
    parser.set_defaults(_handler=inbox_analyzed)


def payload(plan: analyzed.AnalyzedPlan) -> dict[str, Any]:
    """The plan as the gate digests it and the envelope carries it."""
    items = [{"playlist": plan.name, **one.identity()} for one in plan.members]
    counted = Counter(item["action"] for item in items)
    return {
        "digest": plan.digest,
        "items": items,
        "totals": {
            "count": len(items),
            "clear": counted[analyzed.CLEAR],
            "wait": counted[analyzed.WAIT],
        },
        "chunk": None,
    }


def facts(plan: analyzed.AnalyzedPlan) -> dict[str, Any]:
    """What the gate puts in front of the items."""
    return {
        "playlist": (
            f"{plan.name} (row {plan.playlist_id})"
            if plan.playlist_id
            else f"{plan.name}, which the intake folder does not hold"
        ),
        "intake folder": f"{plan.root_name} ({plan.root_id})",
        "clears": f"{len(plan.clears())} row(s) rekordbox has analysed",
        "keeps": f"{len(plan.waits())} row(s) still waiting, each named with why",
        "writes": "memberships of this one playlist only: no track, no file, no other playlist",
    }


def warnings_of(plan: analyzed.AnalyzedPlan) -> list[dict[str, str]]:
    """Each row the clear leaves, named with why."""
    waits = plan.waits()
    if not waits:
        return []
    named = "; ".join(f"{one.title or one.content_id} ({one.why})" for one in waits)
    return [
        {
            "code": WAITING,
            "message": (
                f"{len(waits)} row(s) stay in {plan.name} for the next rekordbox visit: "
                f"{named}"
            ),
        }
    ]


def planned(cfg: config.Config, declared) -> analyzed.AnalyzedPlan:
    """The plan over the playlist as it stands, through a handle opened to read and closed."""
    db = rb_writer.open_db(
        rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
    )
    try:
        return analyzed.plan_clear(cfg, db, declared=declared, registry=tree_registry.read(cfg))
    finally:
        rb_writer.close_db(db)


def written(cfg: config.Config, declared, plan: analyzed.AnalyzedPlan) -> analyzed.Cleared:
    """Apply the plan through a handle of this function's own, opened to write."""
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        return analyzed.apply_clear(
            cfg, db, plan, declared=declared, analysis_roots=analysis_store.watch_roots(cfg)
        )
    finally:
        rb_writer.close_db(db)


def inbox_analyzed(ctx) -> Envelope:
    """Plan the clear, ask, then remove what rekordbox analysed and read it back."""
    cfg = _load()
    declared = active_taxonomy.load(cfg)
    spec = land_cli.gate_named(ctx.entry, APPROVE_GATE)
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).
    session.assert_backup_acknowledged(cfg)

    plan = planned(cfg, declared)
    data = payload(plan)
    warnings = warnings_of(plan)
    if ctx.gate.require(spec, plan=data, context=facts(plan)) != "apply":
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=warnings)
    if not plan.clears():
        return ctx.envelope(
            data=data,
            outcome=Outcome.NO_OP,
            warnings=[
                *warnings,
                {
                    "code": NOTHING,
                    "message": (
                        f"{plan.name} holds no row rekordbox has analysed, so nothing "
                        f"was written"
                    ),
                },
            ],
        )

    cleared = written(cfg, declared, plan)
    analyzed.assert_read_back(plan, cleared)
    data["totals"] = {
        **data["totals"],
        "removed": len(cleared.removed),
        "read back": len(cleared.read_back),
    }
    return ctx.envelope(
        data=data,
        warnings=[
            *warnings,
            {
                "code": CLEARED,
                "message": (
                    f"{len(cleared.removed)} analysed row(s) left {plan.name}, which now "
                    f"holds {len(cleared.read_back)}, read back from the database; every "
                    f"track stays in the collection and in every other playlist; undo "
                    f"with a restore of session {cleared.session_id}"
                ),
            },
        ],
    )


__all__ = [
    "APPROVE_GATE",
    "CLEARED",
    "NOTHING",
    "WAITING",
    "build",
    "facts",
    "inbox_analyzed",
    "payload",
    "planned",
    "warnings_of",
    "written",
]
