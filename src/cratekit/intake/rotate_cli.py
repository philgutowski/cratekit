"""``crate inbox rotate``: keep INBOX short without removing a track (U111).

The engine is :mod:`cratekit.intake.rotate`. This is the order a person meets
it in, ``tag rows``'s: the backup acknowledgment before the plan and the gate
(R-733); the plan on a handle opened to READ and closed before the gate; the
explicit gate over the digested plan, AND AN EMPTY PLAN STILL ASKS, since every
declared gate fires; only ``apply`` over a plan that writes opens the database
to write, where the engine takes the plan again and refuses ``decision-stale``.

THE GATE TAKES NO INLINE ANSWER: a removal takes something out of the library,
so it is answered by a separate recorded act with an actor (R34). The items are
every node looked at, what stays as well as what goes.

Layer: modules. It names :mod:`cratekit.cli.output` and nothing else from the
command-line layer, for the reason ``adopt.apply_cli`` gives.
"""

from __future__ import annotations

from datetime import date
from typing import Any

from cratekit.cli.output import Envelope, load_config
from cratekit.core import active_taxonomy, analysis_store, config, rb_writer, session, tree_registry
from cratekit.core.cause import Outcome, refuse
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


def as_of(ctx) -> date:
    """The day batches are aged against, the local calendar's, as a batch is named.

    ``is None`` and not falsiness: an empty string is something a person typed.
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


def plan_payload(plan: rotate.RotationPlan) -> dict[str, Any]:
    """The plan as the gate digests it and the envelope carries it, public for ``crate organize``."""
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
    folder = f"{plan.root_name} / {plan.old_display}"
    return {
        "intake folder": f"{plan.root_name} ({plan.root_id})",
        "old folder": (
            f"{folder} ({plan.old_id})"
            if plan.old_id is not None
            else f"{folder}, created by this run"
            if plan.moves
            else f"{folder}, absent and not needed"
        ),
        "as of": plan.as_of.isoformat(),
        "moves into old after": f"{plan.stale_days} days",
        "removed from old after": f"{plan.expired_days} days",
        "tracks": "never removed: a removal takes the playlist and its own "
        "memberships only, every track stays in the collection and every other playlist",
    }


def records_warnings(plan: rotate.RotationPlan) -> list[dict[str, str]]:
    """The warning a plan over unread session records carries, empty when every one was read.

    Public for ``crate organize``, which warns exactly as this verb does. An
    unlisted log is named as one, not as a count (R-1255).
    """
    if not plan.unreadable_records:
        return []
    unread = (
        "the session log could not be listed, so a batch a record in it names"
        if plan.log_unlisted
        else f"{plan.unreadable_records} session record(s) could not be read, so a "
        f"batch one of them names"
    )
    message = f"{unread} was aged from its playlist's creation date"
    return [{"code": RECORDS_UNREADABLE, "message": message}]


def planned(
    cfg: config.Config,
    declared,
    today: date,
    *,
    one_read: rb_writer.SharedRead | None = None,
) -> rotate.RotationPlan:
    """The plan over INBOX as it stands, through a handle opened to read and closed.

    Public for ``crate organize`` (U112), which plans exactly as this verb
    does; its ``--report`` passes ``one_read``, its one read handle (U267).
    """
    db = (
        one_read.handle()
        if one_read is not None
        else rb_writer.open_db(
            rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
        )
    )
    try:
        return rotate.plan_rotation(
            cfg, db, declared=declared, registry=tree_registry.read(cfg), today=today
        )
    finally:
        rb_writer.done_reading(db, one_read)


def written(cfg: config.Config, declared, plan: rotate.RotationPlan) -> rotate.Rotated:
    """Apply the plan through a handle of its own, public for ``crate organize`` (U112)."""
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        return rotate.apply_rotation(
            cfg, db, plan, declared=declared, analysis_roots=analysis_store.watch_roots(cfg)
        )
    finally:
        rb_writer.close_db(db)


def inbox_rotate(ctx) -> Envelope:
    """Plan the rotation, ask, then move and remove and read it back."""
    cfg = load_config(("intake.rotate_cli",))
    declared = active_taxonomy.load(cfg)
    spec = _approve_gate(ctx.entry)
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).
    session.assert_backup_acknowledged(cfg)

    plan = planned(cfg, declared, as_of(ctx))
    data = plan_payload(plan)
    warnings = records_warnings(plan)
    if ctx.gate.require(spec, plan=data, context=_facts(plan)) != "approve":
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=warnings)
    if not plan.writes:
        nothing = (
            f"no batch is old enough to move or remove: {len(plan.kept)} "
            f"kept and {len(plan.left)} node(s) left alone, each listed"
        )
        warnings.append({"code": NOTHING_TO_ROTATE, "message": nothing})
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=warnings)

    rotated = written(cfg, declared, plan)
    rotate.assert_read_back(rotated)
    data["totals"] = {
        **data["totals"],
        "moved": len(rotated.moved),
        "removed": len(rotated.removed),
        "memberships removed": rotated.memberships_removed,
        "old created": rotated.old_created,
    }
    done = (
        f"{len(rotated.moved)} batch playlist(s) moved into "
        f"{plan.old_display} and {len(rotated.removed)} removed, "
        f"{rotated.memberships_removed} membership(s) marked with them; "
        f"every node read back from the database where the plan put it, "
        f"and no track left the collection; undo with a restore of "
        f"session {rotated.session_id}"
    )
    return ctx.envelope(data=data, warnings=[*warnings, {"code": ROTATED, "message": done}])
