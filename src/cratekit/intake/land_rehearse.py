"""``intake land --rehearse``: the native landing applied on a scratch area of its own (U162).

Split out of :mod:`cratekit.intake.land_cli`, which re-exports the names its
callers read there and keeps :func:`land_cli.rehearsal_facts`, the live gate
screen's lines naming the rehearsal a plan is compared against.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Callable

from cratekit.cli.output import Envelope
from cratekit.core import config, rb_writer, rehearsal, session, snapshot
from cratekit.core.cause import CratekitError, refuse
from cratekit.intake import batch_name, landing, native, shelve
from cratekit.intake.land_report import _folder, _native_identity

_ORIGIN = ("intake.land_cli",)


#: The verb a rehearsal record names, so a live landing reads only its own (U162).
REHEARSAL_VERB = "intake land"

#: The warning a set landing's rehearsal carries: its account archive was not rehearsed.
REHEARSAL_ARCHIVE_SKIPPED = "intake-rehearsal-archive-skipped"

#: At most this many differing lines on a live gate screen; the rest are counted.
REHEARSAL_LINES_SHOWN = 40


def rehearsal_key(planned: landing.Plan) -> dict[str, str]:
    """What a live landing and its rehearsal share: the staging folder and the batch."""
    return {"folder": str(planned.folder.resolve()), "batch": planned.batch}


def plan_lines(
    planned: landing.Plan, rows: native.NativePlan, *, target: Path, archived=None
) -> list[str]:
    """The native plan as ``path = value`` lines: the gate's identity and the engine's."""
    return rehearsal.lines(plan_identity(planned, rows, target=target, archived=archived))


def plan_identity(
    planned: landing.Plan, rows: native.NativePlan, *, target: Path, archived=None
) -> dict[str, Any]:
    """What :func:`plan_lines` prints, as values, so a rehearsal maps them before they are text.

    MAPPED AS VALUES, NEVER AS LINES (U188). Each line is a JSON value, which
    escapes every character outside ASCII and every quote, so a path with an
    accent in it is spelled in a line as no pair of real paths is, and a
    rehearsal of a batch named with one refused on every path it held.
    """
    # NOT THE ENGINE'S OWN DIGEST, which is a hash of the plan lines below and
    # so names every path in a form no mapping back can reach.
    gate = {
        key: value
        for key, value in _native_identity(planned, rows, target=target).items()
        if key != "collection"
    }
    if archived is not None:
        gate = {**gate, "archive": archived.payload["digest"]}
    return {"gate": gate, "plan": native.identity(rows)}


def _filed_watch(cfg: config.Config, planned: landing.Plan) -> tuple[Path, ...]:
    """The live folders a native landing could file its batch in, which a rehearsal watches.

    The year folder the batch name or today names, where a new folder would
    appear, and for a batch landed into again by its name the folder recorded
    for it and that folder's own year folder, which may be another year's.
    """
    when, _said = shelve.filed_parts(planned.batch, on=batch_name.today())
    watched = [shelve.processed_root(cfg) / f"{when.year}"]
    again = batch_name.filed_folders(cfg).get(planned.batch)
    if again is not None:
        watched.extend((Path(again).parent, Path(again)))
    return tuple(dict.fromkeys(watched))


def _active_rows(db) -> int:
    from sqlalchemy import text

    return int(
        db.session.execute(
            text("SELECT COUNT(*) FROM djmdContent WHERE rb_local_deleted = 0")
        ).scalar()
    )


def _rehearse_native(
    ctx,
    cfg: config.Config,
    planned: landing.Plan,
    *,
    planner: Callable[..., Callable[[Any], native.NativePlan]],
    payload_of: Callable[[native.NativePlan], dict],
    archived,
    declared,
) -> Envelope:
    """Rehearse the landing on a scratch area of this run's own, then remove it (U162).

    THE LIVE PLAN IS MADE FIRST, over the live staging folder and music folder
    and against the database copy, so its digest is the one the live landing
    will show; it is what the rehearsal reports and records. THEN THE SAME
    FILES ARE PLANNED AGAIN AT THE AREA, over their clones and the area's music
    folder, and applied there. The area's plan with every scratch path mapped
    back to its live one must read line for line as the live plan, or nothing
    is applied and the lines that differ are named: what the rehearsal applied
    is the plan the live run will be asked, not a plan like it.

    NOTHING LIVE IS WRITTEN OR MOVED. The live database file set is hashed and
    the live staging and music folders listed before and after, and a change
    is refused as the defect it would be. The account archive of a set
    landing is account side and is never rehearsed; the report says so.

    A FAILURE KEEPS THE AREA AND NAMES IT, so whoever reads the refusal can
    look at what the rehearsal saw. A rehearsal that ends removes it.
    """
    before = rehearsal.witness(
        cfg,
        (
            planned.folder,
            Path(cfg.library.root) / cfg.library.music_dir,
            *_filed_watch(cfg, planned),
        ),
    )
    area = rehearsal.open_area(cfg, ctx.run.run_id, files=planned.items, staging=planned.folder)
    try:
        facts, payload, lines = _rehearse_in(
            cfg,
            planned,
            area=area,
            planner=planner,
            payload_of=payload_of,
            archived=archived,
            declared=declared,
        )
    except CratekitError as exc:
        rehearsal.assert_untouched(before, kept=area.paths)
        inner = exc.cause
        raise refuse(
            inner.reason,
            f"{inner.message}; the rehearsal area is kept at "
            f"{', '.join(str(path) for path in area.paths)}",
            remedy=inner.remediation.remedy,
            steps=inner.remediation.steps,
            origin=_ORIGIN,
            detail={**dict(inner.detail), "rehearsal_area": [str(path) for path in area.paths]},
            inner=inner,
        ) from exc
    except KeyboardInterrupt as exc:
        rehearsal.assert_untouched(before, kept=area.paths)
        raise refuse(
            "cancelled",
            f"the rehearsal was interrupted; the rehearsal area is kept at "
            f"{', '.join(str(path) for path in area.paths)}",
            origin=_ORIGIN,
            detail={"rehearsal_area": [str(path) for path in area.paths]},
        ) from exc
    except Exception as exc:
        rehearsal.assert_untouched(before, kept=area.paths)
        raise refuse(
            "internal-error",
            f"the rehearsal failed ({exc}); the rehearsal area is kept at "
            f"{', '.join(str(path) for path in area.paths)}",
            origin=_ORIGIN,
            detail={"rehearsal_area": [str(path) for path in area.paths]},
        ) from exc
    rehearsal.assert_untouched(before, kept=area.paths)
    rehearsal.remove(area)
    facts["area removed"] = True
    recorded = rehearsal.record(
        ctx.run.run_id,
        verb=REHEARSAL_VERB,
        key=rehearsal_key(planned),
        digest=payload["digest"],
        plan=lines,
        facts=facts,
    )
    facts["record"] = str(recorded)
    data = {**payload, "totals": {**payload["totals"], "rehearsal": facts}}
    warnings = []
    if archived is not None:
        warnings.append(
            {
                "code": REHEARSAL_ARCHIVE_SKIPPED,
                "message": "the account archive this set landing would rename was planned "
                "and digested and not rehearsed, since it is a write to the account",
            }
        )
    return ctx.envelope(data=data, warnings=warnings)


def _rehearse_in(
    cfg: config.Config,
    planned: landing.Plan,
    *,
    area: rehearsal.Area,
    planner,
    payload_of,
    archived,
    declared,
) -> tuple[dict[str, Any], dict, list[str]]:
    """Plan live, plan at the area, compare, apply at the area, read back. Answers the facts."""
    db = rb_writer.open_db(area.database, require_closed=True, cfg=area.cfg)
    try:
        rows = planner(cfg, planned)(db)
        target = _folder(rows)
        payload = payload_of(rows)
        lines = plan_lines(planned, rows, target=target, archived=archived)
        # THE AREA'S PLAN IS MADE OUTSIDE THE REDIRECTION, reading the same
        # installation state the live plan read (a pass's jobs, a set's job),
        # so the only difference between the two plans is where the files are.
        staged = landing.plan(area.staging, area.cfg, planned.batch)
        scratch_rows = planner(area.cfg, staged)(db)
        scratch_target = _folder(scratch_rows)
        pairs = _mapped_back(
            area,
            planned,
            target=target,
            scratch_target=scratch_target,
            rows=rows,
            scratch_rows=scratch_rows,
        )
        back = rehearsal.lines(
            rehearsal.mapped(
                plan_identity(staged, scratch_rows, target=scratch_target, archived=archived),
                pairs,
            )
        )
        differ = rehearsal.differing(back, lines)
        if differ:
            raise refuse(
                "decision-stale",
                f"the plan made at the rehearsal area is not the live plan in "
                f"{len(differ)} line(s), in {', '.join(_fields_of(differ))}, so nothing "
                f"was applied there; the area's paths were compared after mapping "
                + ", ".join(f"{scratch} to {live}" for scratch, live in pairs)
                + "; a line only the area's plan has is marked -, one only the live plan has +: "
                + "; ".join(differ[:REHEARSAL_LINES_SHOWN]),
                origin=_ORIGIN,
                detail={"differs": differ, "mapped": [list(pair) for pair in pairs]},
            )
        # A NAME THE LIVE BATCH FOLDER ALREADY HOLDS IS HELD AT THE AREA TOO,
        # by an empty file of that name, so the area's move refuses the same
        # files the live move will and the facts say so. Occupancy is asked at
        # the move and not in the plan, so the plans alone cannot see it.
        for item in staged.items:
            if (target / item.name).exists() or (target / item.name).is_symlink():
                scratch_target.mkdir(parents=True, exist_ok=True)
                (scratch_target / item.name).touch()
        with rehearsal.redirected(area):
            session.assert_backup_acknowledged(area.cfg)
            rows_before = _active_rows(db)
            with landing.batch_lock(planned.batch):
                landed = landing.apply_native(
                    staged, cfg=area.cfg, db=db, rows=scratch_rows, declared=declared
                )
            native.assert_rows_gridless(landed.collection)
            native.assert_rows_identified(landed.collection)
            rows_after = _active_rows(db)
    finally:
        rb_writer.close_db(db)
    # The check reads a throwaway copy on the temporary volume, so that room is
    # measured first and a copy that still finds none is named as that, never
    # as a database that failed its check (R-1677).
    snapshot.assert_room_for_check(area.database)
    try:
        sound = rb_writer.integrity_ok(area.database, raise_copy_failure=True)
    except rb_writer.IntegrityCheckCopyFailed as failed:
        no_room = snapshot.check_had_no_room(failed, origin=_ORIGIN)
        if no_room is not None:
            raise no_room from failed
        sound = False
    if not sound:
        raise refuse(
            "snapshot-integrity-failed",
            f"the database copy {area.database} fails SQLite's integrity check after "
            f"the rehearsal's landing",
            origin=_ORIGIN,
            detail={"database": str(area.database)},
        )
    facts: dict[str, Any] = {
        "run": area.run_id,
        "landed": len(landed.moved),
        "refused": len(landed.refused),
        "added": len(landed.collection.added),
        "already present": len(landed.collection.present),
        "memberships": landed.collection.memberships_added,
        "active rows before": rows_before,
        "active rows after": rows_after,
        "landed rows gridless": True,
        "integrity": "ok",
    }
    return facts, payload, lines


def _mapped_back(
    area: rehearsal.Area,
    planned: landing.Plan,
    *,
    target: Path,
    scratch_target: Path,
    rows: native.NativePlan,
    scratch_rows: native.NativePlan,
) -> tuple[tuple[str, str], ...]:
    """Each scratch spelling in the area's plan and the live spelling it stands for.

    The area's staging and its batch folder in the MOUNTED spelling, the one
    every ``from`` and ``to`` is written in, and the batch folder again in the
    STORED spelling rekordbox keeps ``FolderPath`` under (U188). On a library
    whose base drive is not its mount, the live one, a row's path is stored
    under the base drive, so neither mounted pair occurs in it and every row
    differed by the area's prefix alone. The stored pair is spelled by the
    writer's own :func:`native.stored_folder_path`, with the drives each plan
    read off its database, so the comparison can never use a spelling rule
    the rows were not written by. A library whose drive never moved stores the
    mounted spelling, and the stored pair is the mounted one, dropped as a
    repeat.
    """
    stored = (
        native.stored_folder_path(
            scratch_target,
            base_drive=scratch_rows.base_drive,
            current_drive=scratch_rows.current_drive,
        ),
        native.stored_folder_path(
            target, base_drive=rows.base_drive, current_drive=rows.current_drive
        ),
    )
    return tuple(
        dict.fromkeys(
            (
                (str(area.staging), str(planned.folder)),
                (str(scratch_target), str(target)),
                stored,
            )
        )
    )


def _fields_of(differ: list[str]) -> list[str]:
    """The fields the differing lines are in, each once, ``rows.columns.FolderPath`` for a row's path.

    The line's path with every index taken out and its first part, ``gate``
    or ``plan``, left off, so a field is named as the identity spells it and
    a leaf that is one entry of a list is named by the list it is in.
    """
    names = []
    for line in differ:
        path = re.sub(r"\[\d+\]", "", line[2:].split(" = ", 1)[0])
        names.append(path.split(".", 1)[-1])
    return list(dict.fromkeys(names))
