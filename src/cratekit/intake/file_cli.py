"""``intake.file``: one audio file already on disk joins the library's intake.

A file already on disk is a plan, not a job: there is no remote work. The verb
lived beside its three queued siblings in :mod:`cratekit.intake.cli` until it
gained a second medium, and it is here for the reason the landing has a module
of its own.

TWO MEDIA, CHOSEN BY THE INTAKE TREE'S MODE (R-770), through the one switch the
landing reads, :func:`cratekit.intake.ingest.intake_medium`.

* On the xml bridge nothing changed. With no ``--export`` the verb shows its
  plan and writes nothing; with one it splices the file into that export
  through ``place_files`` and ends waiting on the import, as a landing does.
* On a library whose intake tree has cut over there is no export to splice.
  Before this unit the verb reached the emitter guard and was refused as a
  defect, over a cutover the person chose. Now it plans one content row and one
  batch playlist under the adopted intake root through the engine the landing
  uses, :mod:`cratekit.intake.native`, reads the backup acknowledgment, and asks
  ``intake.file.native``. ``--export`` is refused by name, as the landing
  refuses it.

THE FILE STAYS WHERE IT IS ON BOTH MEDIA. This verb has never moved a file, so
the row is planned for the path the file is at, resolved, which is the path the
bridge stamps as its Location. A file still under download staging is refused
on both, because a path stamped from staging dies when staging is cleaned.

THE NATIVE GATE TAKES NO INLINE ANSWER, for the landing's reason: a content row
in the collection is answered by a separate recorded act with an actor (R34).
The row carries a title, a path, a name, a size and a type, and every column an
analysis pass fills is left for rekordbox. That policy is the engine's and the
guarded writer's, asserted from SQL before the commit and read back after it.

THE PLAYLIST HAS THE NAME THE BRIDGE GIVES IT. The bridge writes the file's
batch playlist under the stem of its intake file, ``<stem>_inboxed``, and the
native medium writes the same name, so a library that cuts over does not start
naming its single file batches by a second rule.

Layer: modules. The builder's parameters are unannotated so this file does not
import the CLI registry (KTD23).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from cratekit.cli.output import Envelope, digest_of
from cratekit.core import analysis_store, config, rb_writer, session
from cratekit.core.cause import Outcome, Remedy, refuse
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import cli as intake_cli
from cratekit.intake import ingest, land_cli, native, normalize, pipeline

#: The gate the native medium asks. Explicit, and looked up by name.
NATIVE_GATE = "intake.file.native"

#: What a row this run added is marked on the report. The plan's own word for
#: it is the engine's, ``native.ADD``, and a row the collection already held
#: keeps the engine's ``native.PRESENT`` on both.
ADDED = "added"

_ORIGIN = ("intake.file_cli",)


def build_file(parser, entry) -> None:
    parser.add_argument("source", help="audio file already on this machine")
    parser.add_argument(
        "--export",
        default=None,
        metavar="XML",
        help=(
            "Fresh Export to splice into; required to write while the intake "
            "tree is on the xml bridge, and refused once it is database native, "
            "where the file joins the collection through the database"
        ),
    )
    parser.set_defaults(_handler=intake_file)


def batch_name(path: Path) -> str:
    """The batch playlist one file is filed under, on either medium.

    The stem of the intake file the bridge writes beside the track. Spelled
    once, because the native medium has no such file and would otherwise have
    to guess the name the bridge gives the same batch.
    """
    return path.stem + land_cli.INTAKE_SUFFIX[: -len(".xml")]


def intake_file(ctx) -> Envelope:
    cfg = intake_cli._load()
    path = Path(ctx.args.source)
    rows = normalize.from_audio_file(path)
    items = [{"path": str(path), "artist": row.artist, "title": row.title} for row in rows]
    plan = intake_cli._plan(items, kind="file")
    # THE MEDIUM IS THE INTAKE TREE'S MODE, read through the landing's own
    # switch (R-770). What it read is handed to the writer, so the check and
    # the write are asked of one read.
    medium = ingest.intake_medium(cfg)
    if medium.native:
        return _file_native(ctx, cfg, path, plan, medium)
    export = ctx.args.export
    if not export:
        return ctx.envelope(data=plan, outcome=Outcome.OK)
    destination = path.with_name(batch_name(path) + ".xml")
    result = pipeline.ingest_file(
        path,
        cfg=cfg,
        export=Path(export),
        destination=destination,
        declared=medium.declared,
        registry=medium.registry,
    )
    plan["items"][0]["destination"] = str(destination)
    # THE SAME ENDING A LANDING HAS, because it is the same ``place_files``
    # (R-501). This used to answer OK over an intake file nobody had imported
    # and a session nothing would close. The action is the one persisted on the
    # intake session, read back so the two cannot differ.
    return ctx.envelope(
        data=plan,
        outcome=Outcome.PENDING,
        code=ExitCode.PENDING_HUMAN,
        pending=ingest.persisted_pending(cfg, result.placed),
    )


# ---------------------------------------------------------------------------
# The native medium (R-770)
# ---------------------------------------------------------------------------


def _unusable(message: str, *, remedy: Remedy | None = None, **detail: Any):
    return refuse(
        "intake-list-unusable",
        message,
        remedy=remedy,
        origin=_ORIGIN,
        detail=detail,
    )


def _native_payload(plan: dict, rows: native.NativePlan) -> dict:
    """The plan as the approval gate shows it: the file, with the row it becomes.

    EVERY COLUMN THE ROW WOULD CARRY IS ON THE ITEM, and the digest is taken
    over the file as the verb read it and the collection plan together. The
    engine's own digest covers the row's columns, the root, the playlist, the
    device and the database, so an answer given for one file, one title, one
    size or one library is stale for another.
    """
    (row,) = rows.rows
    item: dict[str, Any] = {
        **plan["items"][0],
        "action": row.action,
        "to": str(row.target),
        "row": row.columns(),
    }
    if row.content_id is not None:
        item["content_id"] = row.content_id
    identity = {"kind": "file", "file": plan["digest"], "collection": rows.digest}
    return {
        "digest": digest_of(identity),
        "items": [item],
        "totals": {"count": 1},
        "chunk": None,
    }


def _native_reported(payload: dict, landed: native.NativeLanded) -> dict:
    """The plan, its item marked with what the commit actually did."""
    (item,) = payload["items"]
    if landed.added:
        (row,) = landed.added
        item = {
            **item,
            "action": ADDED,
            "content_id": row.content_id,
            "row": {**item["row"], "Title": row.title, "FolderPath": row.folder_path},
            "left_empty": sorted(row.empty),
        }
    else:
        # A row the collection already held, at the plan or since it: nothing
        # was added, and the membership is the whole of what this run wrote.
        held = landed.present[0].content_id if landed.present else item.get("content_id")
        item = {**item, "action": native.PRESENT, "content_id": held}
    totals = {
        "count": 1,
        "added": len(landed.added),
        "already present": len(landed.present),
        "memberships": landed.memberships_added,
    }
    return {**payload, "items": [item, land_cli.playlist_item(landed)], "totals": totals}


def _file_native(ctx, cfg: config.Config, path: Path, plan: dict, medium) -> Envelope:
    """Plan the row against the database, ask, then write it.

    EVERYTHING THAT CAN REFUSE WITHOUT THE DATABASE REFUSES BEFORE IT IS
    OPENED: an export named for a medium that has none, a file under staging,
    a file no declared sub would take, a suffix the database has no type for.
    THE DATABASE IS THEN OPENED WITH WRITE INTENT BEFORE THE PLAN, so a running
    rekordbox refuses before anything is shown, and THE ACKNOWLEDGMENT IS READ
    BEFORE THE GATE (R-733), so nobody answers a plan the verb could have known
    it would not run.
    """
    declared, registry = medium.declared, medium.registry
    tree_id = declared.intake.id
    if ctx.args.export is not None:
        raise _unusable(
            f"the intake tree {tree_id!r} is database native, so {path.name} joins "
            f"the collection through the database and there is no export to "
            f"splice; drop --export, nothing was written",
            remedy=Remedy.FIX_COMMAND_LINE,
            tree_id=tree_id,
            export=str(ctx.args.export),
        )
    target = path.resolve()
    meta = ingest.read_meta(target, cfg=cfg)
    if ingest.decide_placement(meta, declared) is None:
        raise _unusable(
            f"{path.name} resolves to a bucket with no declared sub, so a row "
            f"added for it would sit in the intake with nowhere to route; run "
            f"crate tag folder over it and ingest it again, nothing was written",
            source=str(path),
        )
    if native.file_type_of(target) is None:
        raise _unusable(
            f"{path.name} has a suffix rekordbox's database has no file type for, "
            f"so no content row can name it and nothing was written; convert it "
            f"and ingest it again",
            source=str(path),
        )
    spec = land_cli.gate_named(ctx.entry, NATIVE_GATE)
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        rows = native.plan_rows(
            cfg,
            db,
            tree_id=tree_id,
            registry=registry,
            batch=batch_name(path),
            files=[(target, target)],
        )
        payload = _native_payload(plan, rows)
        session.assert_backup_acknowledged(cfg)
        option = ctx.gate.require(
            spec,
            plan=payload,
            context={"file": str(target), **land_cli.collection_facts(rows)},
        )
        if option != "apply":
            return ctx.envelope(data=payload, outcome=Outcome.NO_OP)
        landed = native.apply_rows(
            cfg, db, rows, analysis_roots=analysis_store.watch_roots(cfg)
        )
    finally:
        rb_writer.close_db(db)
    native.assert_rows_gridless(landed)
    return ctx.envelope(
        data=_native_reported(payload, landed),
        warnings=land_cli.awaiting_analysis(landed),
    )


__all__ = [
    "ADDED",
    "NATIVE_GATE",
    "batch_name",
    "build_file",
    "intake_file",
]
