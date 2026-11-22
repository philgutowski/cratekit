"""``intake land --rehearse``: the native landing applied on a scratch area of its own (U162).

:mod:`land_cli` re-exports the names callers read there and keeps
:func:`land_cli.rehearsal_facts`, the live screen's lines naming the rehearsal.
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

    MAPPED AS VALUES, NEVER AS LINES (U188): a line is JSON, which escapes an
    accented path into a spelling no pair of real paths maps.
    """
    # NOT THE ENGINE'S OWN DIGEST, a hash no mapping back can reach.
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

    The year folder the batch name or today names, and for a batch landed into
    again the folder recorded for it and that folder's own year folder.
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

    THE LIVE PLAN IS MADE FIRST, against the database copy, so its digest is
    the one the live landing will show. THEN THE SAME FILES ARE PLANNED AT THE
    AREA, and applied there only when that plan, mapped back, reads line for
    line as the live one: what is rehearsed is the plan the live run will ask.

    NOTHING LIVE IS WRITTEN OR MOVED: the live database and folders are
    witnessed before and after. The account archive is never rehearsed, and
    the report says so. A FAILURE KEEPS THE AREA AND NAMES IT.
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
        # OUTSIDE THE REDIRECTION, reading the installation state the live
        # plan read, so the two plans differ only in where the files are.
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
        # A NAME THE LIVE BATCH FOLDER HOLDS IS HELD AT THE AREA TOO, so the
        # area's move refuses what the live move will; plans cannot see it.
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
    # The check copies to the temporary volume, so its room is measured first
    # and no room is never named a failed check (R-1677).
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

    The staging and batch folder in the MOUNTED spelling of ``from`` and
    ``to``, and the batch folder in the STORED spelling of ``FolderPath``
    (U188), which on a library whose base drive is not its mount differs.
    Spelled by the writer's own :func:`native.stored_folder_path`; a repeat
    pair is dropped.
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

    The line's path without indices or its ``gate`` or ``plan`` part, so a
    leaf in a list is named by the list.
    """
    names = []
    for line in differ:
        path = re.sub(r"\[\d+\]", "", line[2:].split(" = ", 1)[0])
        names.append(path.split(".", 1)[-1])
    return list(dict.fromkeys(names))
