"""``intake.land``: a staged batch moves into the library behind one gate.

R-413's verb half. ``acquire download`` commits files to download staging,
``tag folder`` and ``name apply`` work on them there, and nothing moved them
out, so no downloaded track ever reached an importable file. The engine is
:mod:`cratekit.intake.landing`, and this shell owns the plan, the gate and
what a person is told afterwards.

THE PLAN IS SHOWN BEFORE ANYTHING MOVES. The first run lists the folder, puts
the list, the batch folder and the intake file in front of the person on the
gate screen, and stops. An answer recorded against that plan is refused as
stale if the folder, the batch or the intake file changed since, because the
digest covers all of them and not only the files.

THE IMPORT IS THE PERSON'S, AND THE RUN SAYS SO. A landed batch is one intake
file rekordbox has not seen. :func:`cratekit.intake.ingest.place_files` leaves
its intake session ``awaiting-import`` with a ``rekordbox_import`` pending
action PERSISTED ON THAT RECORD, and the envelope carries that same action, not
a second one built here, so what the screen said and what the session log holds
cannot differ. Its steps run end to end: import the file, import the batch
playlist on its own and drag it from the playlist root into the intake folder
(R-687), take a Fresh Export, run ``intake imported``, which proves the import,
retires the file and settles the run (R-501). It BLOCKS NOTHING. A blocking
action makes every verb it names refuse, and no consequence of an unimported
landing was driven that would justify that.

THE SESSION RECORD IS WHERE IT IS REMEMBERED, NOT THE RUN RECORD. The action is
not put on this run's own state, because nothing would ever clear it there and
doctor would report the run as waiting for ever. Doctor's session check names
every run still ``awaiting-import``.

``--manifest`` FILES LABEL TRACKS IN THE SAME FILE. The manifest is the
provenance ``label approved`` wrote beside its list. Its bytes are part of what
the gate compares, so an answer given against one manifest is stale for
another. A label row that no landed file matches is a warning that names the
track, never a failure: the file, if there is one, is in the intake playlist.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from cratekit.cli.output import Envelope, digest_of
from cratekit.core import config, rb_writer, session
from cratekit.core.cause import CratekitError, Outcome, Remedy, refuse
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import cli as intake_cli
from cratekit.intake import ingest, landing, native

#: The action every planned file carries until the apply reports on it.
LAND = "land"
LANDED = "landed"
REFUSED = "refused"
#: The one item a native landing appends for the batch playlist it wrote.
PLAYLIST = "playlist"

#: The two gates, one per medium. The xml one answers inline as it always has;
#: the native one is explicit, because a content row in the collection is a
#: new kind of write and R34 forbids a blanket answer for it.
XML_GATE = "intake.land.confirm"
NATIVE_GATE = "intake.land.native"

#: The warning a native landing carries: the rows are in the collection and
#: rekordbox has not analysed them, which it does on request and not on sight.
AWAITING_ANALYSIS = "rows-await-analysis"

_ORIGIN = ("intake.land_cli",)

#: What a label playlist written, and a label row filed under none, are marked.
FILED = "filed"
UNFILED = "unfiled"

#: The verb that proves an intake file imported. One spelling, beside the
#: session it is persisted on, and named here for the callers that read it.
VERIFY_VERB = ingest.VERIFY_VERB

INTAKE_SUFFIX = "_inboxed.xml"

#: What an intake file's name gains once its import is proven (R-501). It ends
#: the name, so the cutover precheck's scan, which walks ``*.xml``, stops seeing
#: the file. A second file retired under a name already taken gains ``-2``.
RETIRED_SUFFIX = ".imported"

_RETIRED_TAIL = re.compile(re.escape(RETIRED_SUFFIX) + r"(-[0-9]+)?$")


def unretired_name(name: str) -> str:
    """An intake file's name as it was written, retired or not.

    ONE PLACE KNOWS BOTH SPELLINGS. A verb that finds its pass from an intake
    file's name is handed the retired name by anybody who proved the import
    first, and it must read the same pass off it.
    """
    return _RETIRED_TAIL.sub("", name)


def default_name(run_id: str) -> str:
    """The batch name a run gets when ``--name`` is not given.

    The run's own identifier WITHOUT ITS COLONS. A run id spells the time as
    ``19:34:38``, and a colon cannot be in a folder name on the exFAT volumes a
    library commonly sits on, and reads as a slash in Finder on the others.
    """
    return run_id.replace(":", "")


def intake_file(cfg: config.Config, batch: str) -> Path:
    """Where a batch's intake file is written, beside the library, not in staging.

    Staging is the folder a person cleans, and the file has to outlive that
    until rekordbox has imported it. The suffix is one the pending intake scan
    already walks, so an unimported landing is visible to the cutover check.
    """
    return Path(cfg.library.root) / f"{batch}{INTAKE_SUFFIX}"


def build_land(parser, entry) -> None:
    parser.add_argument(
        "folder",
        nargs="?",
        default=None,
        metavar="FOLDER",
        help="the folder of acquired files to land (default: download staging)",
    )
    parser.add_argument(
        "--export",
        default=None,
        metavar="XML",
        help=(
            "a Fresh Export of the collection to splice the landed files into; "
            "required while the intake tree is on the xml bridge, and refused "
            "once it is database native, where the files join the collection "
            "through the database"
        ),
    )
    parser.add_argument(
        "--name",
        default=None,
        metavar="NAME",
        help="the batch folder under the music folder (default: this run's identifier)",
    )
    parser.add_argument(
        "--manifest",
        default=None,
        metavar="JSON",
        help=(
            "the manifest written beside the list these files were acquired "
            "from; its label rows are filed under the record labels tree"
        ),
    )
    parser.set_defaults(_handler=intake_land)


def _payload(
    planned: landing.Plan,
    *,
    target: Path,
    destination: Path,
    export: Path,
    manifest: landing.LabelManifest | None = None,
) -> dict:
    items = [
        {"action": LAND, "from": str(item), "to": str(target / item.name)}
        for item in planned.items
    ]
    identity = {
        "kind": "land",
        "folder": str(planned.folder),
        "batch": planned.batch,
        "target": str(target),
        "destination": str(destination),
        "export": str(export),
        "files": planned.digest,
    }
    if manifest is not None:
        # Only when one is given, so a landing without a manifest is compared
        # exactly as it was before the manifest existed.
        # The bytes and not only the path: a manifest rewritten under the same
        # name files other tracks under other labels, and a digest of the name
        # would call that the plan the person saw.
        identity["manifest"] = str(manifest.path)
        identity["manifest_bytes"] = manifest.digest
    return {
        "digest": digest_of(identity),
        "items": items,
        "totals": {"count": len(items)},
        "chunk": None,
    }


def _shown(
    planned: landing.Plan,
    *,
    target: Path,
    destination: Path,
    manifest: landing.LabelManifest | None = None,
) -> dict[str, Any]:
    """What the gate screen puts in front of the person, one line per fact."""
    shown: dict[str, Any] = {
        "folder": str(planned.folder),
        "lands in": str(target),
        "intake file": str(destination),
        "count": len(planned.items),
        "files": [item.name for item in planned.items],
    }
    if manifest is not None:
        # What the manifest ASKS for, since which rows have a file in this
        # batch is known only once the batch folder can be indexed.
        shown["labels filed from"] = str(manifest.path)
        shown["label playlists named"] = [
            f"{name} ({count} listed)" for name, count in sorted(manifest.playlists().items())
        ]
    return shown


def _planned(folder: Path, cfg: config.Config, batch: str) -> landing.Plan:
    """The engine's plan, or a plan of nothing for a folder with nothing in it.

    AN EMPTY FOLDER IS A PLAN, NOT A REFUSAL, on the precedent ``name apply``
    and ``route inbox`` set: download staging is empty on a fresh install and
    after every landing, and a person running the step then is told there is
    nothing to move, not that something failed. The empty plan is never handed
    to :func:`landing.apply`, so no folder and no intake file is made for it.
    Anything that is not a folder still goes to the engine, which refuses it.
    """
    if folder.is_dir() and not landing.listing(folder):
        return landing.Plan(folder=folder, batch=batch, items=(), digest="")
    return landing.plan(folder, cfg, batch)


def _reported(payload: dict, landed: landing.Landed) -> dict:
    """The plan, each item marked with what the apply actually did to it."""
    refused = {str(entry.path): entry for entry in landed.refused}
    items: list[dict[str, Any]] = []
    for item in payload["items"]:
        entry = refused.get(item["from"])
        if entry is None:
            items.append({**item, "action": LANDED})
        else:
            items.append(
                {**item, "action": REFUSED, "reason": entry.reason, "why": entry.sentence}
            )
    totals = {
        "count": payload["totals"]["count"],
        "landed": len(landed.moved),
        "refused": len(landed.refused),
    }
    if landed.labelled or landed.unlabelled:
        # IN ``items`` AND ``totals``, because the plan surface is closed at
        # four fields and a fifth is a schema break for every consumer. A label
        # playlist written and a label row left out are both things this run
        # did to the plan it was shown, which is what an item is.
        items.extend(
            {
                "action": FILED,
                "label": entry.label,
                "year": entry.year,
                "playlist": entry.playlist,
                "count": len(entry.track_ids),
            }
            for entry in landed.labelled
        )
        items.extend(
            {
                "action": UNFILED,
                "id": entry.ref,
                "artist": entry.artist,
                "title": entry.title,
                "label": entry.label,
                "year": entry.year,
                "reason": entry.reason,
                "why": entry.sentence,
            }
            for entry in landed.unlabelled
        )
        totals["filed"] = len(landed.labelled)
        totals["unfiled"] = len(landed.unlabelled)
    return {**payload, "items": items, "totals": totals}


def gate_named(entry, name: str):
    """One of a verb's gates by name, never by position.

    Two gates on the landing since R-746, one per medium, and the shared cloud
    sync one is raised by the guarded writer rather than asked by a verb, so
    indexing would bind a medium to the order the gates happen to be written
    in. ``intake file`` looks its native gate up the same way (R-770).
    """
    for spec in entry.gates:
        if spec.name == name:
            return spec
    raise refuse(
        "internal-error",
        f"{entry.name} declares no gate named {name!r}, so there is no question "
        f"to ask before it writes",
        remedy=Remedy.REPORT_DEFECT,
        origin=_ORIGIN,
        detail={"verb": entry.name, "gate": name},
    )


def intake_land(ctx) -> Envelope:
    cfg = intake_cli._load()
    folder = Path(ctx.args.folder) if ctx.args.folder else Path(cfg.paths.download_staging)
    batch = ctx.args.name if ctx.args.name is not None else default_name(ctx.run.run_id)
    # READ BEFORE THE GATE, so a file that is not a manifest refuses before
    # anybody spends an answer on it, and the screen can say what it names.
    manifest = (
        landing.read_label_manifest(Path(ctx.args.manifest)) if ctx.args.manifest else None
    )
    planned = _planned(folder, cfg, batch)
    target = landing.target_dir(cfg, batch)
    # THE MEDIUM IS THE INTAKE TREE'S MODE, the way the routing verbs choose
    # theirs (R-746). A tree the database owns takes the files into the
    # collection through the guarded writer and no export is involved; a tree
    # on the bridge is spliced into the export it always was. The registry
    # lives under the library root, so an unreachable root decides nothing
    # here: the xml path is taken as it was before the medium existed, and
    # its preflight names the library, before the gate, under the R-677
    # contract that a recorded abort is still honoured over it. THE SWITCH IS
    # ``ingest.intake_medium`` AND NO COPY OF IT (R-770): ``intake file`` reads
    # the same one, so the two verbs cannot choose by two rules.
    medium = ingest.intake_medium(cfg)
    declared, registry = medium.declared, medium.registry
    if medium.native:
        return _land_native(
            ctx,
            cfg,
            planned,
            target=target,
            declared=declared,
            registry=registry,
            manifest=manifest,
        )
    if ctx.args.export is None and declared is not None:
        raise refuse(
            "library-export-unusable",
            f"the intake tree {declared.intake.id!r} is on the xml bridge, so a "
            f"landing splices the batch into a Fresh Export and --export has to name "
            f"one; nothing was moved",
            remedy=Remedy.FIX_COMMAND_LINE,
            steps=(
                "export the collection from rekordbox and pass that file as --export",
                f"or run crate tree cutover {declared.intake.id} --export with it, after "
                f"which a landing adds the files to the collection directly",
            ),
            origin=_ORIGIN,
            detail={"tree_id": declared.intake.id},
        )
    # With no export named and no library to read, the engine's preflight
    # below refuses on the library first, so the name here is never opened.
    export = (
        Path(ctx.args.export)
        if ctx.args.export is not None
        else Path(cfg.library.root) / "collection.xml"
    )
    destination = intake_file(cfg, batch)
    # THE ENGINE'S PRE-MOVE CHECKS ARE ASKED BEFORE THE GATE TOO (R-677), for
    # the manifest's reason. A plan over an export that is not there, or not a
    # collection, or a library that is not mounted, could never run, and the
    # engine says so without moving anything. Only when something would move,
    # since a plan of nothing splices nothing.
    unusable: CratekitError | None = None
    if planned.items:
        try:
            landing.preflight(
                planned,
                cfg=cfg,
                export=export,
                destination=destination,
                label_rows=manifest.rows if manifest is not None else (),
            )
        except CratekitError as exc:
            unusable = exc
    payload = _payload(
        planned, target=target, destination=destination, export=export, manifest=manifest
    )
    spec = gate_named(ctx.entry, XML_GATE)
    try:
        option = ctx.gate.require(
            spec,
            digest=payload["digest"],
            context=_shown(planned, target=target, destination=destination, manifest=manifest),
        )
    except CratekitError as exc:
        # THE REFUSAL TAKES THE PLACE OF AN UNANSWERED GATE ONLY, the refusal
        # whose remedy is to answer it. An answer already given is honored
        # exactly as it was before the check existed, so an abort still ends in
        # nothing done, and an apply reaches the engine, which asks the same
        # checks again before its first move. Read off the remedy because this
        # layer cannot import the gate's own class.
        if unusable is not None and exc.cause.remediation.remedy is Remedy.ANSWER_DECISION:
            raise unusable from None
        raise
    if option != "apply" or not planned.items:
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP)
    # The engine lists the folder again and refuses a fingerprint that moved,
    # so the gap between this plan and the moves is its to close, not this
    # shell's. What the gate compared is what the person was shown.
    #
    # ONE LANDING PER BATCH NAME, HELD ACROSS THE WHOLE APPLY (R-432). The
    # engine checks a target free and then renames over it, and checks the
    # intake file absent long before it is written, so a second landing into
    # the same batch folder is refused at the door rather than waited for. Only
    # here, after the answer: a plan and a gate screen move nothing and a held
    # name does not stop anybody reading one.
    with landing.batch_lock(batch):
        landed = landing.apply(
            planned,
            cfg=cfg,
            export=export,
            destination=destination,
            manifest=manifest.path if manifest is not None else None,
            manifest_digest=manifest.digest if manifest is not None else None,
        )
    return ctx.envelope(
        data=_reported(payload, landed),
        outcome=Outcome.PENDING,
        code=ExitCode.PENDING_HUMAN,
        pending=ingest.persisted_pending(cfg, landed.placed),
        warnings=[
            {"code": entry.reason, "message": entry.sentence}
            for entry in (*landed.refused, *landed.unlabelled)
        ],
    )


# ---------------------------------------------------------------------------
# The native medium (R-746)
# ---------------------------------------------------------------------------


def _native_payload(planned: landing.Plan, rows: native.NativePlan, *, target: Path) -> dict:
    """The plan as the approval gate shows it: one item per file, with its row.

    EVERY COLUMN THE ROW WOULD CARRY IS ON THE ITEM, and the digest is taken
    over the files, the folder, the batch and the collection plan together, so
    an answer given for one folder, one batch name, one database or one set of
    rows is stale for another. The engine's own digest already covers the rows
    and the root; the files' fingerprint covers what is on disk.
    """
    by_target = {str(row.target): row for row in rows.rows}
    items = []
    for item in planned.items:
        row = by_target[str(target / item.name)]
        entry: dict[str, Any] = {
            "action": row.action,
            "from": str(item),
            "to": str(row.target),
            "row": row.columns(),
        }
        if row.content_id is not None:
            entry["content_id"] = row.content_id
        if row.why:
            entry["why"] = row.why
        items.append(entry)
    identity = {
        "kind": "land-native",
        "folder": str(planned.folder),
        "batch": planned.batch,
        "target": str(target),
        "files": planned.digest,
        "collection": rows.digest,
    }
    return {
        "digest": digest_of(identity),
        "items": items,
        "totals": {"count": len(items)},
        "chunk": None,
    }


def collection_facts(rows: native.NativePlan) -> dict[str, Any]:
    """What a native plan writes, one line per fact, for any verb's gate screen.

    SHARED WITH ``intake file`` (R-770), which asks the same kind of question
    over the same engine's plan: where the playlist hangs, which database is
    written, which device the rows are stamped with, how the path is stored,
    and what is left for rekordbox.
    """
    stored = (
        f"under the base drive {rows.base_drive}, which rekordbox maps to {rows.current_drive}"
        if rows.base_drive and rows.current_drive and rows.base_drive != rows.current_drive
        else "under the mounted path"
    )
    return {
        "playlist": f"{rows.playlist} under {rows.root_name} (row {rows.root_id})",
        "reads and writes": str(rows.database),
        "device": f"{rows.device_id} (master {rows.master_db_id})",
        "paths stored": stored,
        "left empty for rekordbox": list(native.LEFT_EMPTY),
        "adds": len(rows.to_add()),
        "already present": len(rows.present()),
    }


def playlist_item(collection: native.NativeLanded) -> dict[str, Any]:
    """The one item a native write appends for the batch playlist it wrote."""
    return {
        "action": PLAYLIST,
        "playlist": collection.playlist,
        "id": collection.playlist_id,
        "tree": collection.tree_id,
        "session": collection.session_id,
    }


def _native_shown(rows: native.NativePlan, *, folder: Path, target: Path) -> dict[str, Any]:
    """The facts beside the items on the gate screen, one line per fact."""
    return {
        "folder": str(folder),
        "lands in": str(target),
        **collection_facts(rows),
        "left in staging": len(rows.unsupported()),
    }


def _native_reported(payload: dict, landed: landing.LandedNative) -> dict:
    """The plan, each item marked with what the apply actually did to it."""
    refused = {str(entry.path): entry for entry in landed.refused}
    added = {str(row.target): row for row in landed.collection.added}
    present = {str(row.target): row for row in landed.collection.present}
    items: list[dict[str, Any]] = []
    for item in payload["items"]:
        entry = refused.get(item["from"])
        if entry is not None:
            items.append(
                {**item, "action": REFUSED, "reason": entry.reason, "why": entry.sentence}
            )
            continue
        row = added.get(item["to"])
        if row is not None:
            items.append(
                {
                    **item,
                    "action": LANDED,
                    "content_id": row.content_id,
                    "row": {**item["row"], "Title": row.title, "FolderPath": row.folder_path},
                    "left_empty": sorted(row.empty),
                }
            )
            continue
        held = present.get(item["to"])
        items.append(
            {
                **item,
                "action": LANDED,
                "content_id": held.content_id if held is not None else item.get("content_id"),
                "already_present": True,
            }
        )
    totals = {
        "count": payload["totals"]["count"],
        "landed": len(landed.moved),
        "refused": len(landed.refused),
        "added": len(landed.collection.added),
        "already present": len(landed.collection.present),
        "memberships": landed.collection.memberships_added,
    }
    items.append(playlist_item(landed.collection))
    return {**payload, "items": items, "totals": totals}


def _land_native(
    ctx,
    cfg: config.Config,
    planned: landing.Plan,
    *,
    target: Path,
    declared,
    registry,
    manifest: landing.LabelManifest | None,
) -> Envelope:
    """Plan the rows against the database, ask, then move and write.

    THE DATABASE IS OPENED WITH WRITE INTENT BEFORE THE PLAN, so a running
    rekordbox or its agent refuses before anything is shown, and the plan is
    made against the database the apply will write. THE ACKNOWLEDGMENT IS READ
    BEFORE THE GATE (R-733): an approval is the one way door on a live library,
    and a person who reads the whole plan and answers should not then be
    refused by something the verb could have read first. A PLAN OF NOTHING IS
    NOT ASKED: download staging is empty after every landing, and an explicit
    gate, which takes a separate recorded act, is the price of a new kind of
    write and not of learning there is nothing to move. Nothing is written
    for it, so the envelope says so and stops.

    THE GATE TAKES NO INLINE ANSWER. This is a new kind of write, content rows
    in the collection, and it is answered by a separate recorded act with an
    actor, the way the adoption is (R34).
    """
    tree_id = declared.intake.id
    if ctx.args.export is not None:
        raise refuse(
            "intake-list-unusable",
            f"the intake tree {tree_id!r} is database native, so a landing adds the "
            f"files to the collection through the database and there is no export "
            f"to splice; drop --export, nothing was moved",
            remedy=Remedy.FIX_COMMAND_LINE,
            origin=_ORIGIN,
            detail={"tree_id": tree_id, "export": str(ctx.args.export)},
        )
    if manifest is not None:
        raise refuse(
            "intake-list-unusable",
            f"the intake tree {tree_id!r} is database native and label filing from a "
            f"manifest is written into an intake file, which this medium does not "
            f"make; land without --manifest, nothing was moved",
            remedy=Remedy.FIX_COMMAND_LINE,
            origin=_ORIGIN,
            detail={"tree_id": tree_id, "manifest": str(manifest.path)},
        )
    spec = gate_named(ctx.entry, NATIVE_GATE)
    if not planned.items:
        identity = {"kind": "land-native", "folder": str(planned.folder), "batch": planned.batch}
        empty = {"digest": digest_of(identity), "items": [], "totals": {"count": 0}, "chunk": None}
        return ctx.envelope(data=empty, outcome=Outcome.NO_OP)

    # THE LIBRARY CHECKS BEFORE THE DATABASE IS OPENED, so an unmounted volume
    # is named as the volume and a staging folder on another device refuses
    # without a snapshot copy of anything. Once here, and again by the engine
    # before its first move, as the xml landing's preflight is.
    landing.preflight_native(planned, cfg=cfg)
    files = [(item, target / item.name) for item in planned.items]
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        rows = native.plan_rows(
            cfg, db, tree_id=tree_id, registry=registry, batch=planned.batch, files=files
        )
        payload = _native_payload(planned, rows, target=target)
        session.assert_backup_acknowledged(cfg)
        option = ctx.gate.require(
            spec,
            plan=payload,
            context=_native_shown(rows, folder=planned.folder, target=target),
        )
        if option != "apply":
            return ctx.envelope(data=payload, outcome=Outcome.NO_OP)
        # ONE LANDING PER BATCH NAME, HELD ACROSS THE WHOLE APPLY (R-432), as on
        # the bridge: the engine checks a target free and then renames over it.
        with landing.batch_lock(planned.batch):
            landed = landing.apply_native(
                planned, cfg=cfg, db=db, rows=rows, declared=declared
            )
    finally:
        rb_writer.close_db(db)
    native.assert_rows_gridless(landed.collection)
    warnings = [{"code": entry.reason, "message": entry.sentence} for entry in landed.refused]
    warnings.extend(awaiting_analysis(landed.collection))
    return ctx.envelope(data=_native_reported(payload, landed), warnings=warnings)


def awaiting_analysis(collection: native.NativeLanded) -> list[dict[str, str]]:
    """The warning a native write carries when rows joined the collection, else none.

    ONE SENTENCE FOR EVERY VERB THAT ADDS A ROW (R-770). ``intake file`` adds
    one through the same engine and owes the person the same next step, and a
    second wording of it is how one of the two goes stale.
    """
    if not collection.added:
        return []
    return [
        {
            "code": AWAITING_ANALYSIS,
            "message": (
                f"{len(collection.added)} row(s) joined the collection with no "
                f"tempo, grid, key or waveform, and rekordbox analyses nothing on its "
                f"own with Auto Analysis off; open rekordbox, select the "
                f"{collection.playlist} playlist under the intake folder and "
                f"run Analyze Track"
            ),
        }
    ]


__all__ = [
    "AWAITING_ANALYSIS",
    "INTAKE_SUFFIX",
    "NATIVE_GATE",
    "RETIRED_SUFFIX",
    "VERIFY_VERB",
    "XML_GATE",
    "awaiting_analysis",
    "build_land",
    "collection_facts",
    "default_name",
    "gate_named",
    "intake_file",
    "intake_land",
    "playlist_item",
    "unretired_name",
]
