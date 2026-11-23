"""The database area of ``crate organize`` (U112): every step through its own verb.

THE BACKUP ACKNOWLEDGMENT IS READ BEFORE THE AREA IS PLANNED (R-733): with none
the area is refused whole and its gate not asked, but ``--report`` plans it
anyway and says it is missing.

The steps: adoption (``adopt apply``'s plan and worker, refused over a tree
still on the xml bridge), rotation (``inbox rotate``), the Record Labels tree
listed, INSPIRATION brought level with the account (U144), and an account
edit to a mirrored playlist taken (U201, U204) with any track it adds queued
for download, the last two off the run's one account mirror reading. A batch
named for its run is a rename suggested, never made.

WHAT THE AUTHOR MADE, every top level node outside the declared trees and
every node the rotation leaves under INBOX, is listed with a home where one
is obvious. Another app's folder at the top (U185) is named once as a fact.

Layer: modules.
"""

from __future__ import annotations

from contextlib import contextmanager
from datetime import date
from typing import Any

from cratekit.adopt import apply as apply_engine
from cratekit.adopt import apply_cli
from cratekit.adopt import shell as adopt_shell
from cratekit.core import (
    active_taxonomy,
    config,
    jobs,
    rb_writer,
    session,
    tree_registry,
)
from cratekit.core.cause import CratekitError, Remedy, refuse
from cratekit.intake import rotate, rotate_cli
from cratekit.organize import account as account_area
from cratekit.organize import inspiration, mirror_downloads, mirror_edits, own
from cratekit.organize.steps import LISTED, Area, Step, planned_step, refused, selection

AREA = "rekordbox"

#: The fact naming another app's folder at the top of the tree (U185).
FOREIGN_FACT = "foreign"

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
INSPIRATION = "inspiration"
MIRROR_EDITS = mirror_edits.KIND
MIRROR_DOWNLOADS = mirror_downloads.KIND

#: Every step kind this area plans, in its order, each one ``--only`` may name.
#: The mirror edits (U201) run after adoption, whose worker plans again and
#: would refuse a tree moved under it.
STEPS = (ADOPT, ROTATE, RECORD_LABELS, INSPIRATION, MIRROR_EDITS, MIRROR_DOWNLOADS, YOURS)

#: The module that archives sets, whose sets the INSPIRATION step reads.
EXPORT_MODULE = account_area.EXPORT_MODULE

_ORIGIN = ("organize.rekordbox",)


def acknowledgment(cfg: config.Config) -> CratekitError | None:
    """The backup acknowledgment's refusal, or ``None`` when one is in force."""
    try:
        session.assert_backup_acknowledged(cfg)
    except CratekitError as exc:
        return exc
    return None


def _adoption(
    cfg: config.Config, declared, registry, ctx, gate: str, area: Area,
    one_read: rb_writer.SharedRead | None = None,
) -> Step:
    title = f"file tracks into {declared.tree.display}"
    try:
        plan = apply_cli.current_plan(cfg, declared, one_read=one_read)
        # WHAT IS STILL OUTSTANDING, by the engine's own rule: ``applicable()``
        # alone counts what a finished apply placed, and would plan for ever.
        pending = apply_engine.outstanding(plan, apply_engine.read(cfg))
    except CratekitError as exc:
        return refused(ADOPT, title, exc.cause)
    screen, _facts = apply_cli.digested(plan)
    applicable = plan.applicable()
    vocal = len(plan.vocal_additions())
    counts = {
        "tracks read": len(plan.firsts()), "placeable": len(applicable),
        "to file": len(pending), "vocal memberships to add": vocal,
    }
    if not pending and not vocal:
        detail = (
            f"nothing to file: {len(plan.firsts())} track(s) read, "
            f"{len(applicable)} placement(s) already filed by an apply, the rest "
            f"unplaceable; a track with a second genre has a placement in each folder"
        )
        return planned_step(ADOPT, title, False, detail, digest=screen["digest"], counts=counts)
    if not registry.is_database_native(declared.tree.id):
        return refused(
            ADOPT,
            title,
            refuse(
                "tree-unconverged",
                f"{len(pending)} placement(s) would be filed into {declared.tree.display}, "
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

    def apply(step: Step) -> dict[str, Any]:
        decision = ctx.run.decisions.get(gate)
        spec = next(one for one in ctx.entry.gates if one.name == gate)
        # A RUN ``adopt apply --job`` CAN LOAD, holding this area's answer over
        # the adoption's own digest, so a job parked here resumes through that verb.
        gate_run = ctx.gate.hand_off(
            spec, verb=ADOPT_VERB, gate=ADOPT_GATE, part=(area.identity(), step.digest)
        )
        with jobs.open_store() as store:
            job = jobs.enqueue(
                store,
                handler_key=ADOPT_HANDLER,
                payload={
                    "tree": plan.tree, "digest": plan.digest(),
                    # WHO ANSWERED THIS AREA, as ``adopt apply`` freezes its own actor.
                    apply_cli.ACTOR_KEY: decision.actor if decision is not None else "",
                    jobs.GATE_RUN_KEY: gate_run,
                },
                item_ids=(plan.digest(),),
                cfg=cfg,
            )
            job, warnings = adopt_shell.advance(
                ctx, store, job, origin=_ORIGIN,
                nothing_to_run="report an adoption over a library it never touched",
            )
        step.warnings.extend(warnings)
        return {"job_id": job.job_id, **apply_cli.applied_summary(cfg, job.job_id)}

    detail = (
        f"file {len(pending)} placement(s) into {declared.tree.display}, one per "
        f"genre folder of a track, and add {vocal} vocal membership(s); no file tag "
        f"is written"
    )
    return planned_step(
        ADOPT, title, True, detail,
        digest=screen["digest"], counts=counts, items=screen["items"], apply=apply,
    )


def _rotation(
    cfg: config.Config, declared, today: date, area: Area,
    one_read: rb_writer.SharedRead | None = None,
) -> Step:
    title = f"rotate {declared.intake.display}"
    try:
        plan = rotate_cli.planned(cfg, declared, today, one_read=one_read)
    except CratekitError as exc:
        return refused(ROTATE, title, exc.cause)
    shown = rotate_cli.plan_payload(plan)
    for node in plan.left:
        # OLD IS THE ROTATION'S OWN FOLDER, not one of the author's (U214).
        if node.kind == rotate.LEFT_OLD:
            continue
        place = f"{declared.intake.display}, {node.place}"
        area.yours.append(
            {"name": node.name, "place": place, "kind": node.kind, "suggested_home": None}
        )
    for batch in (*plan.moves, *plan.removals, *plan.kept):
        if batch.recognised_by == rotate.BY_SUFFIX:
            suggestion = (
                f"{batch.name} is named for its run; a readable name starts "
                f"{batch.landed.isoformat()}, the day it landed, then its "
                f"source. No verb renames a batch, so nothing is written"
            )
            area.suggested.append(
                {"name": batch.name, "playlist_id": batch.playlist_id, "suggestion": suggestion}
            )

    def apply(_step: Step) -> dict[str, Any]:
        rotated = rotate_cli.written(cfg, declared, plan)
        rotate.assert_read_back(rotated)
        return {
            "moved": len(rotated.moved), "removed": len(rotated.removed),
            "memberships removed": rotated.memberships_removed,
            "old created": rotated.old_created, "session": rotated.session_id,
        }

    totals = shown["totals"]
    step = planned_step(
        ROTATE, title, plan.writes,
        f"move {len(plan.moves)} batch(es) into {plan.old_display} and remove "
        f"{len(plan.removals)} from it, keeping every track"
        if plan.writes
        else f"nothing to rotate: {len(plan.kept)} batch(es) kept",
        digest=plan.digest, items=shown["items"], apply=apply,
        counts={key: totals[key] for key in ("move", "remove", "keep", "left alone")},
    )
    step.warnings.extend(rotate_cli.records_warnings(plan))
    return step


def _record_labels(declared) -> Step:
    catalog = declared.catalog
    if catalog is None:
        detail = "the taxonomy declares no tree a label lands in, so there is nothing to file"
    else:
        detail = (
            f"no verb files a landed label batch into {catalog.display} after its "
            f"landing: a landing files it there itself, from its manifest into "
            f"its intake file on the xml bridge, and from its manifest or --label "
            f"through the database on a native intake tree, so nothing is planned here"
        )
    return Step(RECORD_LABELS, "file landed label batches", LISTED, detail)


def _inspiration(
    cfg: config.Config, declared, available: frozenset[str] | None,
    one_read: rb_writer.SharedRead | None = None,
) -> Step:
    """Every downloaded set on the account given its INSPIRATION playlist (U144).

    Planned through read handles, so it plans while rekordbox runs, and no read
    is held across a provider call (U267). The write opens its own handle and
    needs rekordbox closed. Any refusal refuses this step alone.
    """
    title = "give every downloaded set its INSPIRATION playlist"
    if available is not None and EXPORT_MODULE not in available:
        return Step(
            INSPIRATION, title, LISTED, "the export module is off in this profile, so no set is read"
        )
    from cratekit.intake import ingest, set_playlist
    from cratekit.label import catalogue
    from cratekit.modules.outbound import account

    @contextmanager
    def reading():
        db = (
            one_read.handle()
            if one_read is not None
            else rb_writer.open_db(
                rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
            )
        )
        try:
            yield db
        finally:
            rb_writer.done_reading(db, one_read)

    try:
        set_playlist.assert_native(ingest.intake_medium(cfg), landing=False)
        planned = inspiration.plan(
            cfg, declared, remote=account.resolve(cfg), found=catalogue.resolve(cfg),
            reading=reading,
        )
    except CratekitError as exc:
        return refused(INSPIRATION, title, exc.cause)
    step = planned_step(
        INSPIRATION, title, planned.writes, planned.detail(),
        digest=planned.digest(), counts=planned.counts(), items=planned.items(),
        apply=lambda _step: inspiration.apply(cfg, declared, planned).totals(),
    )
    # UNREAD IS NOT NONE: a set whose tracks could not be listed is named on
    # the screen and in the warnings, never folded into the sets with no match.
    step.warnings.extend(
        {
            "code": "organize-inspiration-unread",
            "message": (
                f"the downloaded set {row.name!r} was not read: {row.why}"
                if row.action == inspiration.UNREAD
                else f"the account folder {row.folder!r} was not read: {row.why}"
            ),
        }
        for row in planned.rows
        if row.action in (inspiration.UNREAD, inspiration.FOLDER_UNREAD)
    )
    return step


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


def _yours(
    cfg: config.Config, declared, labels: tuple[str, ...], area: Area,
    one_read: rb_writer.SharedRead | None = None,
) -> Step:
    """Every top level node outside the declared trees, read through a read handle."""
    title = "list your own playlists"
    try:
        db = (
            one_read.handle()
            if one_read is not None
            else rb_writer.open_db(
                rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
            )
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
        rb_writer.done_reading(db, one_read)
    declared_roots = _declared_roots(declared)
    catalog = declared.catalog.display if declared.catalog is not None else None
    # U185. ANOTHER APP'S FOLDER IS NAMED ONCE, as a fact, and is not yours.
    foreign = {str(row.ID) for row in active_taxonomy.foreign_roots_in(rows)}
    if foreign:
        area.facts[FOREIGN_FACT] = (
            f"{active_taxonomy.FOREIGN_OWNER} at the top level, {active_taxonomy.FOREIGN_LEFT_AS_IT_IS}"
        )
    found = 0
    for row in sorted(rows, key=lambda one: (int(getattr(one, "Seq", 0) or 0), str(one.Name))):
        name = str(row.Name)
        if name in declared_roots or str(row.ID) in foreign:
            continue
        found += 1
        home = own.rekordbox_home(name, labels, catalog)
        area.yours.append(
            {"name": name, "place": "top level", "kind": _kind(row), "suggested_home": home}
        )
    detail = f"{found} top level node(s) of your own, listed and never moved"
    return Step(YOURS, title, LISTED, detail, counts={"top level": found})


def plan_area(
    cfg: config.Config, ctx, *, gate: str, today: date, labels: tuple[str, ...], report: bool,
    only: frozenset[str] | None = None, available: frozenset[str] | None = None, shared=None,
    one_read: rb_writer.SharedRead | None = None,
) -> Area:
    """Plan every database step, or refuse the area before any when no backup is acknowledged.

    ``only`` is ``--only``'s selection (U137). ``available`` is the profile's
    modules, ``None`` for every one. ``shared`` is the run's one account mirror
    reading (U201); with none the mirror steps are listed, not planned.
    ``one_read`` is ``--report``'s one read handle (U267), which every step
    reads the database through; the run that answers a gate passes none.
    """
    area = Area(name=AREA, only=selection(STEPS, only))
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
    if area.wants(ADOPT):
        area.steps.append(_adoption(cfg, declared, registry, ctx, gate, area, one_read))
    # THE ROTATION IS PLANNED FOR ``yours`` TOO, since what it leaves under INBOX
    # is the author's; its step is shown when selected, or when it refused,
    # since a refusal is why that listing is short.
    if area.wants(ROTATE) or area.wants(YOURS):
        rotation = _rotation(cfg, declared, today, area, one_read)
        if area.wants(ROTATE) or rotation.cause is not None:
            area.steps.append(rotation)
    if area.wants(RECORD_LABELS):
        area.steps.append(_record_labels(declared))
    if area.wants(INSPIRATION):
        area.steps.append(_inspiration(cfg, declared, available, one_read))
    if area.wants(MIRROR_EDITS):
        if shared is None:
            said = "no account mirror was read on this run, so no edit is taken"
            area.steps.append(Step(MIRROR_EDITS, mirror_edits.TITLE, LISTED, said))
        else:
            edited = mirror_edits.add_step(cfg, declared, registry, shared, one_read=one_read)
            area.deletes.extend(mirror_edits.deletes(edited.items))
            area.steps.append(edited)
    if area.wants(MIRROR_DOWNLOADS):
        if shared is None:
            said = "no account mirror was read on this run, so nothing is queued"
            area.steps.append(Step(MIRROR_DOWNLOADS, mirror_downloads.TITLE, LISTED, said))
        else:
            area.steps.append(mirror_downloads.add_step(cfg, shared, one_read=one_read))
    if area.wants(YOURS):
        area.steps.append(_yours(cfg, declared, labels, area, one_read))
    area.facts["rehearse"] = (
        "every write here is a database write: rehearse it on a copy of the "
        "database first, with library state redirected, and compare the digest"
    )
    return area


__all__ = [
    "ADOPT", "ADOPT_GATE", "ADOPT_HANDLER", "ADOPT_VERB", "AREA", "EXPORT_MODULE",
    "INSPIRATION", "MIRROR_DOWNLOADS", "MIRROR_EDITS", "RECORD_LABELS", "ROTATE", "STEPS",
    "YOURS", "acknowledgment", "plan_area",
]
