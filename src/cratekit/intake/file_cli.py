"""``intake.file``: one audio file already on disk joins the library's intake.

A file already on disk is a plan, not a job: there is no remote work. The verb
lived beside its three queued siblings in :mod:`cratekit.intake.cli` until it
gained a second medium, and it is here for the reason the landing has a module
of its own.

TWO MEDIA, CHOSEN BY THE INTAKE TREE'S MODE (R-770), through the one switch the
landing reads, :func:`cratekit.intake.ingest.intake_medium`.

* On the xml bridge the verb writes what it always wrote. With no ``--export``
  it shows its plan and writes nothing; with one it splices the file into that
  export through ``place_files`` and ends waiting on the import, as a landing
  does.
* On a library whose intake tree has cut over there is no export to splice.
  Before this unit the verb reached the emitter guard and was refused as a
  defect, over a cutover the person chose. Now it plans one content row and one
  batch playlist under the adopted intake root through the engine the landing
  uses, :mod:`cratekit.intake.native`, reads the backup acknowledgment, and asks
  ``intake.file.native``. ``--export`` is refused by name, as the landing
  refuses it.

THE FILE STAYS WHERE IT IS ON BOTH MEDIA. This verb has never moved a file. A
file still under download staging is refused on both, because a path stamped
from staging dies when staging is cleaned. ON THE NATIVE MEDIUM THE FILE HAS TO
BE IN THE LIBRARY, which the bridge never asked: a row is matched against the
collection by resolving its path under the library root, so a file outside it
could not be asked about again, and its row would be dropped by every reader
that resolves against the root. The row is planned for the path spelled under
the configured root, as the native landing spells its targets, so a root
reached through a link still matches the rows the collection already holds.

THE NATIVE GATE TAKES NO INLINE ANSWER, for the landing's reason: a content row
in the collection is answered by a separate recorded act with an actor (R34).
The order around it is the landing's own, ``land_cli.ask_then_write``. The row
carries a title, a path, a name, a size and a type, and every column an
analysis pass fills is left for rekordbox. That policy is the engine's and the
guarded writer's, asserted from SQL before the commit and read back after it.

THE NATIVE PLAYLIST IS NAMED AS THE NATIVE LANDING NAMES ITS OWN, by the bare
batch, which for one file is the file's stem. On the bridge this verb still
names the playlist after its intake file, stem and suffix, while a landing
names it for its batch alone since U110; the native medium has no intake file
and neither verb adds the suffix there, so a cut over library has one naming
rule and not one per verb.

THE MEDIUM IS READ BEFORE THE PLAN IS SHOWN, on the bridge too. Which medium
the verb is on decides whether there is a gate to ask, and that is the
library's taxonomy and its tree registry, so either one unreadable refuses
with its own cause where the plan only path used to need the file alone.

Layer: modules. The builder's parameters are unannotated so this file does not
import the CLI registry (KTD23).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from cratekit.cli.output import Envelope, digest_of
from cratekit.core import analysis_store, config, rb_writer
from cratekit.core.cause import CratekitError, Outcome, Remedy, refuse
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import cli as intake_cli
from cratekit.intake import ingest, land_cli, native, normalize, pipeline

#: The gate the native medium asks. Explicit, and looked up by name. NOT
#: ``NATIVE_GATE``: the landing shell exports that name for its own gate, and
#: one symbol holding two gates in two modules is how a test comes to decide
#: the wrong one.
FILE_GATE = "intake.file.native"

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


def _in_the_library(path: Path, cfg: config.Config) -> Path:
    """``path`` spelled under the configured library root, or the refusal.

    Both sides are resolved to compare them and the answer is rebuilt under the
    root AS CONFIGURED, which is how the native landing spells a target and how
    the collection's own rows are matched.
    """
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
            "row": {
                **item["row"],
                "Title": row.title,
                "FolderPath": row.folder_path,
                rb_writer.FILE_ID_COLUMN: row.file_id,
            },
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
    OPENED: an export named for a medium that has none, a file outside the
    library, a file under staging, a file no declared sub would take, a suffix
    the database has no type for. The order from there is the landing's.
    """
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
    # STAGING FIRST, since staging is usually outside the library too and the
    # sentence that names it is the more useful of the two.
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
            # EVERY FAILURE PAST THE GATE SAYS WHAT IT LEAVES, as the landing's
            # does: the database is all or nothing and the file was never
            # moved. A cause this product raised keeps its reason and remedy;
            # anything else is the defect it is, with the same sentence.
            inner = exc.cause if isinstance(exc, CratekitError) else None
            raise refuse(
                inner.reason if inner is not None else "internal-error",
                f"the collection could not be written "
                f"({inner.message if inner is not None else exc}); no row was added "
                f"and {path.name} is where it was",
                remedy=inner.remediation.remedy if inner is not None else None,
                steps=inner.remediation.steps if inner is not None else (),
                origin=_ORIGIN,
                detail={
                    "source": str(target),
                    **(dict(inner.detail) if inner is not None else {}),
                },
                inner=inner,
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
        warnings=land_cli.awaiting_analysis(landed),
    )


__all__ = [
    "ADDED",
    "FILE_GATE",
    "build_file",
    "intake_file",
]
