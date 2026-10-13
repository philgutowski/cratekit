"""``crate inbox refill``: rebuild an INBOX account playlist from its recorded pass (U134).

The engine is :mod:`cratekit.intake.refill`, and its docstring says how a
playlist is found and how each row is resolved. This module is the order a
person meets it in, which is ``inbox rotate``'s:

* the backup acknowledgment is read before the plan and before the gate
  (R-733);
* the plan is made on a handle opened to READ and closed before the gate, and
  a library whose intake tree is still on the bridge refuses there, naming
  ``tree cutover``;
* the explicit gate is asked over the digested plan, AND AN EMPTY PLAN STILL
  ASKS, so a second run that plans nothing is a question answered and ends
  ``no_op``;
* only ``apply`` over a plan that adds a membership opens the database with
  write intent, and the engine takes the plan again on that handle and
  refuses ``decision-stale`` when anything moved in between.

THE ITEMS ARE EVERY ROW OF EVERY PLAYLIST, the ones it adds, the ones it
already holds and the ones it leaves with why, then each account playlist no
INBOX playlist answers, so the screen a person approves names what stays out
as well as what goes in.

Layer: modules. It names :mod:`cratekit.cli.output` and nothing else from the
command-line layer, for the reason ``adopt.apply_cli`` gives.
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
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation
from cratekit.core.exit_codes import Remedy
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
                origin=("intake.refill_cli",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


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
    return {
        "digest": plan.digest,
        "items": items,
        "totals": {
            "count": len(items),
            "playlists": len(plan.targets),
            "add": plan.adds,
            "held": sum(len(one.members) for one in plan.targets) - plan.adds,
            "left": sum(len(one.left) for one in plan.targets),
            "unfound": len(plan.unfound),
        },
        "chunk": None,
    }


def facts(plan: refill.RefillPlan) -> dict[str, Any]:
    """What the gate puts in front of the items, one line per playlist."""
    return {
        "pass": plan.pass_name,
        "intake folder": f"{plan.root_name} ({plan.root_id})",
        "playlists": [
            f"{one.name} (row {one.playlist_id}, {one.found_by}): {len(one.members)} "
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
        found.append(
            {
                "code": LEFT_OUT,
                "message": (
                    f"{len(left)} track(s) of the account playlists are not in their "
                    f"INBOX playlist, each named with why: {named}"
                ),
            }
        )
    if plan.unfound:
        named = "; ".join(f"{one.account_name} ({one.why})" for one in plan.unfound)
        found.append(
            {
                "code": UNFOUND,
                "message": (
                    f"{len(plan.unfound)} account playlist(s) of the pass were not "
                    f"refilled: {named}"
                ),
            }
        )
    return found


def planned(cfg: config.Config, declared, pass_name: str) -> refill.RefillPlan:
    """The plan over INBOX as it stands, through a handle opened to read and closed."""
    db = rb_writer.open_db(
        rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
    )
    try:
        return refill.plan_refill(
            cfg, db, declared=declared, registry=tree_registry.read(cfg), pass_name=pass_name
        )
    finally:
        rb_writer.close_db(db)


def written(cfg: config.Config, declared, plan: refill.RefillPlan) -> refill.Refilled:
    """Apply the plan through a handle of this function's own, opened to write."""
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        return refill.apply_refill(
            cfg, db, plan, declared=declared, analysis_roots=analysis_store.watch_roots(cfg)
        )
    finally:
        rb_writer.close_db(db)


def inbox_refill(ctx) -> Envelope:
    """Plan the refill, ask, then add what each playlist lacks and read it back."""
    cfg = _load()
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
        return ctx.envelope(
            data=data,
            outcome=Outcome.NO_OP,
            warnings=[
                *warnings,
                {
                    "code": NOTHING,
                    "message": (
                        f"every track the library owns of the pass's {len(plan.targets)} "
                        f"INBOX playlist(s) is in its playlist already, so nothing was "
                        f"written"
                    ),
                },
            ],
        )

    refilled = written(cfg, declared, plan)
    refill.assert_read_back(refilled)
    data["totals"] = {
        **data["totals"],
        "added": refilled.added,
        "read back": sum(len(one.read_back) for one in refilled.filled),
    }
    return ctx.envelope(
        data=data,
        warnings=[
            *warnings,
            {
                "code": REFILLED,
                "message": (
                    f"{refilled.added} membership(s) added across "
                    + ", ".join(
                        f"{one.name} ({len(one.added)}, now {len(one.read_back)})"
                        for one in refilled.filled
                    )
                    + f"; every one read back from the database, and no content row "
                    f"was written; undo with a restore of session {refilled.session_id}"
                ),
            },
        ],
    )


__all__ = [
    "APPROVE_GATE",
    "LEFT_OUT",
    "NOTHING",
    "REFILLED",
    "UNFOUND",
    "build",
    "facts",
    "inbox_refill",
    "payload",
    "planned",
    "warnings_of",
    "written",
]
