"""``crate inbox rotate``: keep INBOX short without removing a track (U111).

The engine is :mod:`cratekit.intake.rotate`, and its docstring says what a
batch is, how one is aged and what each band does. This module is the order a
person meets it in, which is ``tag rows``'s and ``adopt move``'s:

* the backup acknowledgment is read before the plan and before the gate
  (R-733), so a person with none is refused before they read a plan;
* the plan is made on a handle opened to READ and closed before the gate, and
  a library whose intake tree is still on the bridge refuses there, naming
  ``tree cutover``;
* the explicit gate is asked over the digested plan, AND AN EMPTY PLAN STILL
  ASKS: every declared gate has to fire, and a second run that plans nothing
  is a question answered, not a question skipped;
* only ``apply`` over a plan that writes opens the database with write
  intent, and the engine takes the plan again on that handle and refuses
  ``decision-stale`` when INBOX moved in between.

THE GATE TAKES NO INLINE ANSWER. A removal takes something out of the library,
so it is answered by a separate recorded act with an actor (R34).

THE ITEMS ARE EVERY NODE THE ROTATION LOOKED AT, the moves and the removals
first, then the batches it keeps and the nodes it leaves alone with the reason,
so the screen a person approves names what stays as well as what goes.

Layer: modules. It names :mod:`cratekit.cli.output` and nothing else from the
command-line layer, for the reason ``adopt.apply_cli`` gives.
"""

from __future__ import annotations

from datetime import date
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
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.intake import rotate

#: The explicit gate the rotation is asked behind.
APPROVE_GATE = "inbox.rotate.approve"

#: The plan moves and removes nothing.
NOTHING_TO_ROTATE = "rotate-nothing-planned"

#: What the apply moved and removed, read back.
ROTATED = "rotate-applied"

#: Session records that could not be read, so some batches aged from the row.
RECORDS_UNREADABLE = "rotate-records-unreadable"

#: What a node the rotation leaves alone is marked on the screen.
LEAVE = "leave alone"

_ORIGIN = ("intake", "rotate_cli")


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
                origin=("intake.rotate_cli",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def build(parser, entry) -> None:
    """Declare the verb. THERE IS NO ``--yes``: the gate is the only answer."""
    del entry
    parser.add_argument(
        "--as-of",
        dest="as_of",
        default=None,
        metavar="DATE",
        help=(
            "the ISO date to age batches against; today by default. Give the "
            "same date on the run that applies, or the plan is a different one"
        ),
    )
    parser.set_defaults(_handler=inbox_rotate)


def _as_of(ctx) -> date:
    """The day batches are aged against: the local calendar's, as a batch is named.

    ``is None`` and not falsiness, for the aging report's reason: an empty
    string is something a person typed. The aging report's slug, since the
    flag and the mistake are the same one.
    """
    raw = getattr(ctx.args, "as_of", None)
    if raw is None:
        return date.today()
    try:
        return date.fromisoformat(str(raw))
    except ValueError as exc:
        raise refuse(
            "report-as-of-invalid",
            f"{raw!r} is not a date; a rotation run for a day nobody can name "
            f"would age every batch against a value this verb invented",
            remedy=Remedy.FIX_COMMAND_LINE,
            steps=("pass --as-of as an ISO date, for example 2026-10-03",),
            origin=_ORIGIN,
            detail={"as_of": str(raw)},
        ) from exc


def _approve_gate(entry):
    """The verb's own gate by name, never by position, for ``tag rows``'s reason."""
    for spec in entry.gates:
        if spec.name == APPROVE_GATE:
            return spec
    raise refuse(
        "internal-error",
        f"{entry.name} declares no gate named {APPROVE_GATE!r}, so there is no "
        f"question to ask before it moves or removes anything",
        remedy=Remedy.REPORT_DEFECT,
        origin=_ORIGIN,
        detail={"verb": entry.name, "gate": APPROVE_GATE},
    )


def _payload(plan: rotate.RotationPlan) -> dict[str, Any]:
    """The plan as the gate digests it and the envelope carries it."""
    items = [batch.to_json() for batch in (*plan.moves, *plan.removals, *plan.kept)]
    items += [{"action": LEAVE, **node.to_json()} for node in plan.left]
    return {
        "digest": plan.digest,
        "items": items,
        "totals": {
            "count": len(items),
            "move": len(plan.moves),
            "remove": len(plan.removals),
            "keep": len(plan.kept),
            "left alone": len(plan.left),
            "tracks in removed playlists": sum(batch.tracks for batch in plan.removals),
        },
        "chunk": None,
    }


def _facts(plan: rotate.RotationPlan) -> dict[str, Any]:
    """What the gate puts in front of the items."""
    return {
        "intake folder": f"{plan.root_name} ({plan.root_id})",
        "old folder": (
            f"{plan.root_name} / {plan.old_display} ({plan.old_id})"
            if plan.old_id is not None
            else f"{plan.root_name} / {plan.old_display}, created by this run"
            if plan.moves
            else f"{plan.root_name} / {plan.old_display}, absent and not needed"
        ),
        "as of": plan.as_of.isoformat(),
        "moves into old after": f"{plan.stale_days} days",
        "removed from old after": f"{plan.expired_days} days",
        "tracks": "never removed: a removal takes the playlist and its own "
        "memberships only, every track stays in the collection and every other playlist",
    }


def _warnings(plan: rotate.RotationPlan) -> list[dict[str, str]]:
    if not plan.unreadable_records:
        return []
    return [
        {
            "code": RECORDS_UNREADABLE,
            "message": (
                f"{plan.unreadable_records} session record(s) could not be read, so a "
                f"batch one of them names was aged from its playlist's creation date"
            ),
        }
    ]


def _plan(cfg: config.Config, declared, today: date) -> rotate.RotationPlan:
    """The plan over INBOX as it stands, through a handle opened to read and closed."""
    db = rb_writer.open_db(
        rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
    )
    try:
        return rotate.plan_rotation(
            cfg, db, declared=declared, registry=tree_registry.read(cfg), today=today
        )
    finally:
        rb_writer.close_db(db)


def _write(cfg: config.Config, declared, plan: rotate.RotationPlan) -> rotate.Rotated:
    """Apply the plan through a handle of this function's own, opened to write."""
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        return rotate.apply_rotation(
            cfg, db, plan, declared=declared, analysis_roots=analysis_store.watch_roots(cfg)
        )
    finally:
        rb_writer.close_db(db)


def inbox_rotate(ctx) -> Envelope:
    """Plan the rotation, ask, then move and remove and read it back."""
    cfg = _load()
    declared = active_taxonomy.load(cfg)
    spec = _approve_gate(ctx.entry)
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).
    session.assert_backup_acknowledged(cfg)

    plan = _plan(cfg, declared, _as_of(ctx))
    data = _payload(plan)
    warnings = _warnings(plan)
    if ctx.gate.require(spec, plan=data, context=_facts(plan)) != "approve":
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=warnings)
    if not plan.writes:
        return ctx.envelope(
            data=data,
            outcome=Outcome.NO_OP,
            warnings=[
                *warnings,
                {
                    "code": NOTHING_TO_ROTATE,
                    "message": (
                        f"no batch is old enough to move or remove: {len(plan.kept)} "
                        f"kept and {len(plan.left)} node(s) left alone, each listed"
                    ),
                },
            ],
        )

    rotated = _write(cfg, declared, plan)
    rotate.assert_read_back(rotated)
    data["totals"] = {
        **data["totals"],
        "moved": len(rotated.moved),
        "removed": len(rotated.removed),
        "memberships removed": rotated.memberships_removed,
        "old created": rotated.old_created,
    }
    return ctx.envelope(
        data=data,
        warnings=[
            *warnings,
            {
                "code": ROTATED,
                "message": (
                    f"{len(rotated.moved)} batch playlist(s) moved into "
                    f"{plan.old_display} and {len(rotated.removed)} removed with their "
                    f"{rotated.memberships_removed} membership(s), read back from the "
                    f"database; no track left the collection; undo with a restore of "
                    f"session {rotated.session_id}"
                ),
            },
        ],
    )


__all__ = [
    "APPROVE_GATE",
    "LEAVE",
    "NOTHING_TO_ROTATE",
    "RECORDS_UNREADABLE",
    "ROTATED",
    "build",
    "inbox_rotate",
]
