"""``crate inbox refill``: rebuild an INBOX account playlist from its recorded pass (U134).

The engine is :mod:`cratekit.intake.refill`. The order a person meets it in is
``inbox rotate``'s, AN EMPTY PLAN STILL ASKS and ends ``no_op``, and only
``apply`` over a plan that adds a membership opens the database to write. The
items are every row of every playlist, added, held or left with why, then each
account playlist no INBOX playlist answers.

Layer: modules. It names :mod:`cratekit.cli.output` and nothing else from the
command-line layer, for the reason ``adopt.apply_cli`` gives.
"""

from __future__ import annotations

from collections import Counter
from typing import Any, Callable, TypeVar

from cratekit.cli.output import Envelope, load_config
from cratekit.core import active_taxonomy, analysis_store, config, rb_writer, session, tree_registry
from cratekit.core.cause import Outcome
from cratekit.intake import land_cli, refill

#: The explicit gate the refill is asked behind.
APPROVE_GATE = "inbox.refill.approve"

#: The plan adds no membership.
NOTHING = "refill-nothing-planned"

#: What the apply added, read back.
REFILLED = "refill-applied"

#: Rows of an account playlist its INBOX playlist will not hold.
LEFT_OUT = "refill-left-out"

#: Account playlists of the pass no single INBOX playlist answers.
UNFOUND = "refill-playlist-unfound"

#: Session records that could not be read, so no playlist was found by name.
RECORDS_UNREADABLE = "refill-records-unreadable"

_T = TypeVar("_T")


def build(parser, entry) -> None:
    """Declare the verb. THERE IS NO ``--yes``: the gate is the only answer."""
    del entry
    parser.add_argument(
        "--pass",
        dest="pass_name",
        required=True,
        metavar="PASS",
        help=(
            "the pass whose account playlists are refilled, as crate intake missing "
            "--run printed it, for example 2026-10-08T141649Z-d4ce_synced"
        ),
    )
    parser.set_defaults(_handler=inbox_refill)


def payload(plan: refill.RefillPlan) -> dict[str, Any]:
    """The plan as the gate digests it and the envelope carries it."""
    items: list[dict[str, Any]] = []
    for target in plan.targets:
        items.extend(
            {"playlist": target.name, "playlist_id": target.playlist_id, **row}
            for row in target.rows()
        )
    items.extend({"action": "unfound", **one.identity()} for one in plan.unfound)
    counted = Counter(item["action"] for item in items)
    return {
        "digest": plan.digest,
        "items": items,
        "totals": {
            "count": len(items),
            "playlists": len(plan.targets),
            "add": counted[refill.ADD],
            "held": counted[refill.HELD],
            "again": counted[refill.AGAIN],
            "left": counted["leave"],
            "unfound": counted["unfound"],
        },
        "chunk": None,
    }


def facts(plan: refill.RefillPlan) -> dict[str, Any]:
    """What the gate puts in front of the items, one line per playlist."""
    return {
        "pass": plan.pass_name,
        "intake folder": f"{plan.root_name} ({plan.root_id})",
        "playlists": [
            f"{one.name} (row {one.playlist_id}, {one.found_by}): {len(one.distinct)} "
            f"track(s) the library owns, {len(one.adds)} to add, {len(one.left)} left out"
            for one in plan.targets
        ],
        "writes": "memberships only: no content row, no playlist row, no file",
    }


def warnings_of(plan: refill.RefillPlan) -> list[dict[str, str]]:
    """The left rows and the unanswered account playlists, each named."""
    found: list[dict[str, str]] = []
    left = [(one.name, row) for one in plan.targets for row in one.left]
    if left:
        named = "; ".join(
            f"{playlist} {row.position}. {row.artist} - {row.title} ({row.why})"
            for playlist, row in left
        )
        message = (
            f"{len(left)} track(s) of the account playlists are not in their "
            f"INBOX playlist, each named with why: {named}"
        )
        found.append({"code": LEFT_OUT, "message": message})
    if plan.unfound:
        named = "; ".join(f"{one.account_name} ({one.why})" for one in plan.unfound)
        message = f"{len(plan.unfound)} account playlist(s) of the pass were not refilled: {named}"
        found.append({"code": UNFOUND, "message": message})
    if plan.unreadable:
        found.append(
            {
                "code": RECORDS_UNREADABLE,
                "message": (
                    (
                        "the session log could not be listed"
                        if plan.log_unlisted
                        else f"{plan.unreadable} session record(s) could not be read"
                    )
                    + ", so no account playlist without a readable landing record was "
                    "found by its name"
                ),
            }
        )
    return found


def reading(cfg: config.Config, plan: Callable[[Any], _T]) -> _T:
    """``plan(db)`` over a handle opened to read and closed, as every INBOX verb plans."""
    db = rb_writer.open_db(
        rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
    )
    try:
        return plan(db)
    finally:
        rb_writer.close_db(db)


def writing(cfg: config.Config, apply: Callable[[Any, Any], _T]) -> _T:
    """``apply(db, analysis_roots)`` through a handle of its own, opened to write and closed."""
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        return apply(db, analysis_store.watch_roots(cfg))
    finally:
        rb_writer.close_db(db)


def planned(cfg: config.Config, declared, pass_name: str) -> refill.RefillPlan:
    """The plan over INBOX as it stands, through a handle opened to read and closed."""
    return reading(
        cfg,
        lambda db: refill.plan_refill(
            cfg, db, declared=declared, registry=tree_registry.read(cfg), pass_name=pass_name
        ),
    )


def written(cfg: config.Config, declared, plan: refill.RefillPlan) -> refill.Refilled:
    """Apply the plan through a handle of this function's own, opened to write."""
    return writing(
        cfg,
        lambda db, roots: refill.apply_refill(
            cfg, db, plan, declared=declared, analysis_roots=roots
        ),
    )


def inbox_refill(ctx) -> Envelope:
    """Plan the refill, ask, then add what each playlist lacks and read it back."""
    cfg = load_config(("intake.refill_cli",))
    declared = active_taxonomy.load(cfg)
    spec = land_cli.gate_named(ctx.entry, APPROVE_GATE)
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).
    session.assert_backup_acknowledged(cfg)

    plan = planned(cfg, declared, str(ctx.args.pass_name))
    data = payload(plan)
    warnings = warnings_of(plan)
    if ctx.gate.require(spec, plan=data, context=facts(plan)) != "apply":
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=warnings)
    if not plan.writes:
        nothing = (
            f"every track the library owns of the pass's {len(plan.targets)} "
            f"INBOX playlist(s) is in its playlist already, so nothing was written"
        )
        warnings.append({"code": NOTHING, "message": nothing})
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=warnings)

    refilled = written(cfg, declared, plan)
    refill.assert_read_back(refilled)
    data["totals"] = {
        **data["totals"],
        "added": refilled.added,
        "read back": sum(len(one.read_back) for one in refilled.filled),
    }
    across = ", ".join(
        f"{one.name} ({len(one.added)}, now {len(one.read_back)})" for one in refilled.filled
    )
    done = (
        f"{refilled.added} membership(s) added across {across}; every one read back from "
        f"the database, and no content row was written; undo with a restore of session "
        f"{refilled.session_id}"
    )
    return ctx.envelope(data=data, warnings=[*warnings, {"code": REFILLED, "message": done}])
