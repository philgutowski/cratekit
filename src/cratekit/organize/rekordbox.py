"""The database area of ``crate organize`` (U112): every step through its own verb.

THE BACKUP ACKNOWLEDGMENT IS READ BEFORE THE AREA IS PLANNED (R-733), as ``inbox
rotate`` reads it before its plan. With none, the area is refused as a whole,
its gate is not asked since nothing it could write would run, and the account
area is planned and asked as if this one were not there. ``--report`` writes
nothing, so it plans the area anyway and says the acknowledgment is missing.

THE STEPS, each the owning verb's plan:

* ADOPTION, ``adopt apply``'s :func:`current_plan` and its own screen. On
  approval its job is queued under that verb's handler key, with the person
  who answered this area's gate as its approving actor, and driven here
  through the worker ``adopt apply`` runs, which rebuilds the plan and refuses
  ``decision-stale`` when it moved. A plan with something to file over a
  routing tree still on the xml bridge is refused at the plan, naming
  ``tree cutover``, since the worker's membership write refuses that tree and
  a screen should not promise it;
* ROTATION, ``inbox rotate``'s plan and write, read back after;
* THE RECORD LABELS TREE is LISTED: its only writer is the landing of a label
  batch, which writes the tree into its intake file, so no verb places a
  landed batch afterwards and nothing is planned for it;
* A BATCH NAMED FOR ITS RUN, ``..._inboxed``, is a rename SUGGESTED and never
  made, since no verb renames a batch.

WHAT THE AUTHOR MADE is every top level node outside the trees the taxonomy
declares, and every node the rotation leaves alone under INBOX. Each is listed
with a home where :mod:`cratekit.organize.own` finds an obvious one.

Layer: modules.
"""

from __future__ import annotations

from datetime import date
from typing import Any

from cratekit.adopt import apply as apply_engine
from cratekit.adopt import apply_cli
from cratekit.adopt import shell as adopt_shell
from cratekit.core import active_taxonomy, config, jobs, rb_writer, session, tree_registry
from cratekit.core.cause import CratekitError, Remedy, refuse
from cratekit.intake import rotate, rotate_cli
from cratekit.organize import own
from cratekit.organize.steps import LISTED, NOTHING, PLANNED, Area, Step, refused

AREA = "rekordbox"

#: The handler key ``adopt apply`` queues under, whose worker this area drives,
#: and the verb and gate whose resume a job interrupted here goes through.
#: ``tests/test_organize.py`` holds each equal to the registry's.
ADOPT_HANDLER = "adopt.apply"
ADOPT_VERB = "adopt.apply"
ADOPT_GATE = "adopt.apply.approve"

ADOPT = "adopt"
ROTATE = "rotate"
RECORD_LABELS = "record-labels"
YOURS = "yours"

_ORIGIN = ("organize.rekordbox",)


def acknowledgment(cfg: config.Config) -> CratekitError | None:
    """The backup acknowledgment's refusal, or ``None`` when one is in force."""
    try:
        session.assert_backup_acknowledged(cfg)
    except CratekitError as exc:
        return exc
    return None


def _adoption(cfg: config.Config, declared, registry, ctx, gate: str, area: Area) -> Step:
    title = f"file tracks into {declared.tree.display}"
    try:
        plan = apply_cli.current_plan(cfg, declared)
    except CratekitError as exc:
        return refused(ADOPT, title, exc.cause)
    try:
        # WHAT IS STILL OUTSTANDING, by the engine's own rule: an applicable
        # entry the applied ledger does not hold. ``applicable()`` alone counts
        # an entry a finished apply already placed, and ``adopt apply`` itself
        # would queue a pass that applies nothing, so a second organize would
        # plan the adoption for ever.
        pending = apply_engine.outstanding(plan, apply_engine.read(cfg))
    except CratekitError as exc:
        return refused(ADOPT, title, exc.cause)
    screen, _facts = apply_cli.digested(plan)
    applicable = plan.applicable()
    vocal = len(plan.vocal_additions())
    counts = {
        "tracks read": len(plan.entries),
        "placeable": len(applicable),
        "to file": len(pending),
        "vocal memberships to add": vocal,
    }
    if not pending and not vocal:
        return Step(
            key=ADOPT,
            title=title,
            state=NOTHING,
            detail=(
                f"nothing to file: {len(plan.entries)} track(s) read, "
                f"{len(applicable)} already filed by an apply, the rest unplaceable"
            ),
            digest=screen["digest"],
            counts=counts,
        )
    if not registry.is_database_native(declared.tree.id):
        return refused(
            ADOPT,
            title,
            refuse(
                "tree-unconverged",
                f"{len(pending)} track(s) would be filed into {declared.tree.display}, "
                f"which is still on the xml bridge, so its memberships cannot be "
                f"written to the database and nothing is planned",
                remedy=Remedy.COMPLETE_PENDING_ACTION,
                steps=(
                    f"take a Fresh Export from rekordbox, then run `crate tree cutover "
                    f"{declared.tree.id} --export <that file>`, then organize again",
                ),
                origin=_ORIGIN,
                detail={"tree": declared.tree.id, "to_file": len(pending)},
            ).cause,
        )
    step = Step(
        key=ADOPT,
        title=title,
        state=PLANNED,
        detail=(
            f"file {len(pending)} track(s) into {declared.tree.display} and add "
            f"{vocal} vocal membership(s); no file tag is written"
        ),
        digest=screen["digest"],
        counts=counts,
        items=list(screen["items"]),
    )

    def apply() -> dict[str, Any]:
        decision = ctx.run.decisions.get(gate)
        spec = next(one for one in ctx.entry.gates if one.name == gate)
        # A RUN ``adopt apply --job`` CAN LOAD, holding this area's answer
        # over the adoption's own digest. A job that parks or is interrupted
        # here resumes through that verb, whose explicit gate would otherwise
        # meet nothing recorded on every respawn and never be driven.
        gate_run = ctx.gate.hand_off(
            spec, verb=ADOPT_VERB, gate=ADOPT_GATE, part=(area.identity(), step.digest)
        )
        with jobs.open_store() as store:
            job = jobs.enqueue(
                store,
                handler_key=ADOPT_HANDLER,
                payload={
                    "tree": plan.tree,
                    "digest": plan.digest(),
                    # WHO ANSWERED THIS AREA, off the recorded decision, as
                    # ``adopt apply`` freezes the actor of its own gate.
                    apply_cli.ACTOR_KEY: decision.actor if decision is not None else "",
                    jobs.GATE_RUN_KEY: gate_run,
                },
                item_ids=(plan.digest(),),
                cfg=cfg,
            )
            job, warnings = adopt_shell.advance(
                ctx,
                store,
                job,
                origin=_ORIGIN,
                nothing_to_run="report an adoption over a library it never touched",
            )
        step.warnings.extend(warnings)
        return {"job_id": job.job_id, **apply_cli.applied_summary(cfg, job.job_id)}

    step.apply = apply
    return step


def _rotation(cfg: config.Config, declared, today: date, area: Area) -> Step:
    title = f"rotate {declared.intake.display}"
    try:
        plan = rotate_cli.planned(cfg, declared, today)
    except CratekitError as exc:
        return refused(ROTATE, title, exc.cause)
    shown = rotate_cli.plan_payload(plan)
    for node in plan.left:
        area.yours.append(
            {
                "name": node.name,
                "place": f"{declared.intake.display}, {node.place}",
                "kind": node.kind,
                "suggested_home": None,
            }
        )
    for batch in (*plan.moves, *plan.removals, *plan.kept):
        if batch.recognised_by == rotate.BY_SUFFIX:
            area.suggested.append(
                {
                    "name": batch.name,
                    "playlist_id": batch.playlist_id,
                    "suggestion": (
                        f"{batch.name} is named for its run; a readable name starts "
                        f"{batch.landed.isoformat()}, the day it landed, then its "
                        f"source. No verb renames a batch, so nothing is written"
                    ),
                }
            )
    totals = shown["totals"]
    step = Step(
        key=ROTATE,
        title=title,
        state=PLANNED if plan.writes else NOTHING,
        detail=(
            f"move {len(plan.moves)} batch(es) into {plan.old_display} and remove "
            f"{len(plan.removals)} from it, keeping every track"
            if plan.writes
            else f"nothing to rotate: {len(plan.kept)} batch(es) kept"
        ),
        digest=plan.digest,
        counts={key: totals[key] for key in ("move", "remove", "keep", "left alone")},
        items=list(shown["items"]),
    )
    if plan.unreadable_records:
        step.warnings.append(
            {
                "code": rotate_cli.RECORDS_UNREADABLE,
                "message": (
                    f"{plan.unreadable_records} session record(s) could not be read, so a "
                    f"batch one of them names was aged from its playlist's creation date"
                ),
            }
        )
    if plan.writes:

        def apply() -> dict[str, Any]:
            rotated = rotate_cli.written(cfg, declared, plan)
            rotate.assert_read_back(rotated)
            return {
                "moved": len(rotated.moved),
                "removed": len(rotated.removed),
                "memberships removed": rotated.memberships_removed,
                "old created": rotated.old_created,
                "session": rotated.session_id,
            }

        step.apply = apply
    return step


def _record_labels(declared) -> Step:
    catalog = declared.catalog
    if catalog is None:
        detail = "the taxonomy declares no tree a label lands in, so there is nothing to file"
    else:
        detail = (
            f"no verb files a landed label batch into {catalog.display} after its "
            f"landing: the landing writes that tree into its own intake file, so "
            f"nothing is planned here"
        )
    return Step(key=RECORD_LABELS, title="file landed label batches", state=LISTED, detail=detail)


def _declared_roots(declared) -> set[str]:
    roots = {declared.tree.display, declared.intake.display}
    if declared.catalog is not None:
        roots.add(declared.catalog.display)
    long_tracks = getattr(declared, "long_tracks", None)
    if long_tracks is not None and getattr(long_tracks, "display", None):
        roots.add(long_tracks.display)
    return roots


def _kind(row: Any) -> str:
    attribute = int(getattr(row, "Attribute", 0) or 0)
    return {0: "playlist", 1: "folder"}.get(attribute, "smart playlist")


def _yours(cfg: config.Config, declared, labels: tuple[str, ...], area: Area) -> Step:
    """Every top level node outside the declared trees, read through a read handle."""
    title = "list your own playlists"
    try:
        db = rb_writer.open_db(
            rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
        )
    except CratekitError as exc:
        return refused(YOURS, title, exc.cause)
    try:
        rows = [
            row
            for row in list(db.get_playlist())
            if not rb_writer.node_removed(row)
            and str(getattr(row, "ParentID", "")) in rb_writer.ROOT_PARENT_SENTINELS
        ]
    finally:
        rb_writer.close_db(db)
    declared_roots = _declared_roots(declared)
    catalog = declared.catalog.display if declared.catalog is not None else None
    found = 0
    for row in sorted(rows, key=lambda one: (int(getattr(one, "Seq", 0) or 0), str(one.Name))):
        name = str(row.Name)
        if name in declared_roots:
            continue
        found += 1
        area.yours.append(
            {
                "name": name,
                "place": "top level",
                "kind": _kind(row),
                "suggested_home": own.rekordbox_home(name, labels, catalog),
            }
        )
    return Step(
        key=YOURS,
        title=title,
        state=LISTED,
        detail=f"{found} top level node(s) of your own, listed and never moved",
        counts={"top level": found},
    )


def plan_area(
    cfg: config.Config,
    ctx,
    *,
    gate: str,
    today: date,
    labels: tuple[str, ...],
    report: bool,
) -> Area:
    """Plan every database step, or refuse the area before any when no backup is acknowledged."""
    area = Area(name=AREA)
    unacknowledged = acknowledgment(cfg)
    if unacknowledged is not None:
        if not report:
            area.cause = unacknowledged.cause
            return area
        area.facts["backup acknowledgment"] = (
            f"missing, so applying this area would be refused: {unacknowledged.cause.message}"
        )
    try:
        declared = active_taxonomy.load(cfg)
        registry = tree_registry.read(cfg)
    except CratekitError as exc:
        area.cause = exc.cause
        return area
    area.steps.append(_adoption(cfg, declared, registry, ctx, gate, area))
    area.steps.append(_rotation(cfg, declared, today, area))
    area.steps.append(_record_labels(declared))
    area.steps.append(_yours(cfg, declared, labels, area))
    area.facts["rehearse"] = (
        "every write here is a database write: rehearse it on a copy of the "
        "database first, with library state redirected, and compare the digest"
    )
    return area


__all__ = [
    "ADOPT",
    "ADOPT_GATE",
    "ADOPT_HANDLER",
    "ADOPT_VERB",
    "AREA",
    "RECORD_LABELS",
    "ROTATE",
    "YOURS",
    "acknowledgment",
    "plan_area",
]

