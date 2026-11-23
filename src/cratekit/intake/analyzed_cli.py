"""``crate inbox analyzed``: take every analysed row out of INBOX / Analyze (U166).

The engine is :mod:`cratekit.intake.analyzed`. The order a person meets it in
is ``inbox rotate``'s, AN EMPTY PLAN STILL ASKS and ends ``no_op``, and only
``apply`` over a plan that clears a row opens the database to write. The items
are every row the playlist holds, cleared or left with why.

Layer: modules. It names :mod:`cratekit.cli.output` and nothing else from the
command-line layer, for the reason ``adopt.apply_cli`` gives.
"""

from __future__ import annotations

from collections import Counter
from typing import Any

from cratekit.cli.output import Envelope, load_config
from cratekit.core import active_taxonomy, config, session, tree_registry
from cratekit.core.cause import Outcome
from cratekit.intake import analyzed, land_cli, refill_cli

#: The explicit gate the clear is asked behind.
APPROVE_GATE = "inbox.analyzed.approve"

#: The plan clears no row.
NOTHING = "analyzed-nothing-planned"

#: What the apply removed, read back.
CLEARED = "analyzed-cleared"

#: Rows that stay because rekordbox has not finished with them.
WAITING = "analyzed-rows-waiting"


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
    message = f"{len(waits)} row(s) stay in {plan.name} for the next rekordbox visit: {named}"
    return [{"code": WAITING, "message": message}]


def planned(cfg: config.Config, declared) -> analyzed.AnalyzedPlan:
    """The plan over the playlist as it stands, through a handle opened to read and closed."""
    return refill_cli.reading(
        cfg,
        lambda db: analyzed.plan_clear(
            cfg, db, declared=declared, registry=tree_registry.read(cfg)
        ),
    )


def written(cfg: config.Config, declared, plan: analyzed.AnalyzedPlan) -> analyzed.Cleared:
    """Apply the plan through a handle of this function's own, opened to write."""
    return refill_cli.writing(
        cfg,
        lambda db, roots: analyzed.apply_clear(
            cfg, db, plan, declared=declared, analysis_roots=roots
        ),
    )


def inbox_analyzed(ctx) -> Envelope:
    """Plan the clear, ask, then remove what rekordbox analysed and read it back."""
    cfg = load_config(("intake.analyzed_cli",))
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
        nothing = f"{plan.name} holds no row rekordbox has analysed, so nothing was written"
        warnings.append({"code": NOTHING, "message": nothing})
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=warnings)

    cleared = written(cfg, declared, plan)
    analyzed.assert_read_back(plan, cleared)
    data["totals"] = {
        **data["totals"],
        "removed": len(cleared.removed),
        "read back": len(cleared.read_back),
    }
    done = (
        f"{len(cleared.removed)} analysed row(s) left {plan.name}, which now "
        f"holds {len(cleared.read_back)}, read back from the database; every "
        f"track stays in the collection and in every other playlist; undo "
        f"with a restore of session {cleared.session_id}"
    )
    return ctx.envelope(data=data, warnings=[*warnings, {"code": CLEARED, "message": done}])
