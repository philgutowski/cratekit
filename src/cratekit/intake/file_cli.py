"""``intake.file``: one audio file already on disk joins the library's intake.

TWO MEDIA, CHOSEN BY THE INTAKE TREE'S MODE (R-770), through
:func:`cratekit.intake.ingest.intake_medium`, read before the plan is shown.
On the xml bridge, with ``--export`` the file is spliced through
``place_files`` and the verb ends waiting on the import; without, it shows its
plan and writes nothing. On a native intake tree it plans one content row and
one batch playlist through :mod:`cratekit.intake.native`, asks
``intake.file.native`` with no inline answer (R34), in the landing's order
(``land_cli.ask_then_write``), and refuses ``--export`` by name.

THE FILE NEVER MOVES. A file under download staging is refused on both media.
On the native medium it must be in the library, since a row is matched by
resolving its path under the root, and it is spelled under the root as
configured, as the native landing spells its targets. The native playlist is
the bare stem, as the native landing names its own batch.

Layer: modules. The builder's parameters are unannotated so this file does not
import the CLI registry (KTD23).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from cratekit.cli.output import Envelope, digest_of
from cratekit.core import analysis_store, config, rb_writer
from cratekit.core.cause import Outcome, Remedy, refuse
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import cli as intake_cli
from cratekit.intake import ingest, land_cli, landing, native, normalize, pipeline

#: The gate the native medium asks, looked up by name. Not ``NATIVE_GATE``,
#: which is the landing's own gate.
FILE_GATE = "intake.file.native"

#: What a row this run added is marked on the report; a row already held keeps
#: the engine's ``native.PRESENT``.
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


def intake_file(ctx) -> Envelope:
    cfg = intake_cli._load()
    path = Path(ctx.args.source)
    rows = normalize.from_audio_file(path)
    items = [{"path": str(path), "artist": row.artist, "title": row.title} for row in rows]
    plan = intake_cli._plan(items, kind="file")
    # What the switch read is handed to the writer: one read for check and write.
    medium = ingest.intake_medium(cfg)
    if medium.native:
        return _file_native(ctx, cfg, path, plan, medium)
    export = ctx.args.export
    if not export:
        return ctx.envelope(data=plan, outcome=Outcome.OK)
    destination = path.with_name(path.stem + land_cli.INTAKE_SUFFIX)
    result = pipeline.ingest_file(
        path,
        cfg=cfg,
        export=Path(export),
        destination=destination,
        declared=medium.declared,
        registry=medium.registry,
    )
    plan["items"][0]["destination"] = str(destination)
    # THE SAME ENDING A LANDING HAS (R-501), the action read back from the session.
    return ctx.envelope(
        data=plan,
        outcome=Outcome.PENDING,
        code=ExitCode.PENDING_HUMAN,
        pending=ingest.persisted_pending(cfg, result.placed),
    )


def _in_the_library(path: Path, cfg: config.Config) -> Path:
    """``path`` spelled under the library root AS CONFIGURED, as the native landing spells one."""
    root = Path(cfg.library.root)
    try:
        return root / path.resolve().relative_to(root.resolve())
    except ValueError:
        raise refuse(
            "intake-list-unusable",
            f"{path.name} is outside the library at {root}, so the collection could "
            f"not be asked again whether it holds that file and a row added for it "
            f"would name a file the library does not own; move it into the "
            f"library's music folder and ingest it again, nothing was written",
            origin=_ORIGIN,
            detail={"source": str(path), "root": str(root)},
        ) from None


def _native_payload(plan: dict, rows: native.NativePlan) -> dict:
    """The plan as the approval gate shows it: the file, with the row it becomes.

    The digest covers the file as read and the engine's plan digest, so an
    answer for one file or library is stale for another; the database's path
    is shown, not digested (U161).
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
            "row": {
                **item["row"],
                "Title": row.title,
                "FolderPath": row.folder_path,
                rb_writer.FILE_ID_COLUMN: row.file_id,
                rb_writer.CONTENT_LINK_COLUMN: row.content_link,
            },
            "left_empty": sorted(row.empty),
        }
    else:
        # A row already held: the membership is all this run wrote.
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
    """Plan the row against the database, ask, then write it; other refusals come first."""
    declared, registry = medium.declared, medium.registry
    tree_id = declared.intake.id
    if ctx.args.export is not None:
        raise refuse(
            "intake-list-unusable",
            f"the intake tree {tree_id!r} is database native, so {path.name} joins "
            f"the collection through the database and there is no export to "
            f"splice; drop --export, nothing was written",
            remedy=Remedy.FIX_COMMAND_LINE,
            origin=_ORIGIN,
            detail={"tree_id": tree_id, "export": str(ctx.args.export)},
        )
    # STAGING FIRST: usually outside the library too, and its sentence says more.
    ingest.assert_not_staging(path, cfg)
    target = _in_the_library(path, cfg)
    meta = ingest.read_meta(target, cfg=cfg)
    if ingest.decide_placement(meta, declared) is None:
        raise refuse(
            "intake-list-unusable",
            f"{path.name} resolves to a bucket with no declared sub, so a row "
            f"added for it would sit in the intake with nowhere to route; run "
            f"crate tag folder over it and ingest it again, nothing was written",
            origin=_ORIGIN,
            detail={"source": str(path)},
        )
    if native.file_type_of(target) is None:
        raise refuse(
            "intake-list-unusable",
            f"{path.name} has a suffix rekordbox's database has no file type for, "
            f"so no content row can name it and nothing was written; convert it "
            f"and ingest it again",
            origin=_ORIGIN,
            detail={"source": str(path)},
        )

    def write(db, rows: native.NativePlan) -> native.NativeLanded:
        try:
            return native.apply_rows(
                cfg, db, rows, analysis_roots=analysis_store.watch_roots(cfg)
            )
        except Exception as exc:
            # The database is all or nothing and the file never moved.
            raise landing.refuse_past(
                exc,
                "the collection could not be written",
                f"no row was added and {path.name} is where it was",
                origin=_ORIGIN,
                detail={"source": str(target)},
            ) from exc

    payload, landed = land_cli.ask_then_write(
        ctx,
        cfg,
        land_cli.gate_named(ctx.entry, FILE_GATE),
        plan=lambda db: native.plan_rows(
            cfg,
            db,
            tree_id=tree_id,
            registry=registry,
            batch=path.stem,
            files=[(target, target)],
        ),
        payload=lambda rows: _native_payload(plan, rows),
        shown=lambda rows: {"file": str(target), **land_cli.collection_facts(rows)},
        write=write,
    )
    if landed is None:
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP)
    native.assert_rows_gridless(landed)
    native.assert_rows_identified(landed)
    return ctx.envelope(
        data=_native_reported(payload, landed),
        warnings=[
            *land_cli.awaiting_analysis(landed),
            *land_cli.vox_warnings(landed),
            *land_cli.dyn_warnings(landed),
        ],
    )
