"""``intake.imported``: prove an intake file imported, retire it, settle its run.

R-501's verb. Every landing ends ``awaiting-import``, holding one intake file
rekordbox has not seen. A person imports it, and until this verb nothing could
be told that they had: the session stayed open, the file stayed at the library
root, and each of them refused the cutover precheck with no verb able to clear
either.

THE PROOF IS A FRESH EXPORT, READ, NEVER A PERSON'S SAY SO. Every file a run
placed is recorded in the routing ledger by its Location. A run's import is
proven when the collection export names every one of them, compared by
:func:`cratekit.write.routing_pass.track_id`, the digest of the decoded path,
because rekordbox spells a Location its own way on the way out. A Fresh Export
is the evidence the XML era already runs on, it needs no database open, and it
is the import check R-436 recorded as missing.

AN INTAKE FILE CANNOT BE ITS OWN PROOF. It names every landed track whether or
not anybody imported it, so a file carrying one of the names this product
writes is refused as the export, and so is any file a waiting run names.

RETIRING IS A RENAME, NOT A DELETE. The file leaves the pending scan by losing
the ``.xml`` ending, and stays where it was for a person to remove. Nobody
answers a gate here, so nothing is deleted here.

THE RUN IS SETTLED AS FAR AS IT CAN BE. A proven run leaves ``awaiting-import``.
It closes here, through the gated close, only when it holds no deferred
placement. Before a cutover it always holds one, since only a database native
tree can place it, so it stays open holding nothing a cutover needs, and the
precheck excuses exactly that (:func:`cratekit.core.session.owes_only_deferred_routing`).
After a cutover ``route pending`` places the tracks and closes it.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from cratekit.cli.output import Envelope
from cratekit.core import config, locations, session, tree_registry
from cratekit.core.cause import CratekitError, Outcome, refuse
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import cli as intake_cli
from cratekit.intake import collection_xml, ingest
from cratekit.intake.land_cli import RETIRED_SUFFIX
from cratekit.write import rbxml, routing_pass

#: What each run is marked with once this verb has looked at it.
IMPORTED = "imported"
NOT_IMPORTED = "not-imported"
UNVERIFIABLE = "unverifiable"
RETIRED = "retired"

#: How many missing tracks one run's item names. The count is always whole.
MISSING_SHOWN = 10

_ORIGIN = ("intake.imported",)


def build_imported(parser, entry) -> None:
    parser.add_argument(
        "--export",
        required=True,
        metavar="XML",
        help="a Fresh Export of the collection, taken after the import",
    )
    parser.add_argument(
        "--session",
        default=None,
        metavar="ID",
        help="look at this intake run only (default: every run waiting on an import)",
    )
    parser.set_defaults(_handler=intake_imported)


def _refuse_export(message: str, export: Path, **extra: Any) -> CratekitError:
    return refuse(
        "library-export-unusable",
        message,
        steps=("take a Fresh Export of the collection from rekordbox and pass that file",),
        origin=_ORIGIN,
        detail={"export": str(export), **extra},
    )


def _same_file(left: Path, right: Path) -> bool:
    try:
        return left.resolve() == right.resolve()
    except OSError:
        return False


def read_export(export: Path, waiting: list[session.SessionRecord]) -> set[str]:
    """The identifier of every track the export's collection names.

    Refuses anything that could prove an import that never happened. See the
    module docstring: an intake file names its own tracks.
    """
    if not export.is_file():
        raise _refuse_export(f"no collection export at {export}", export)
    if any(export.name.endswith(suffix) for suffix in tree_registry.PENDING_XML_SUFFIXES):
        raise _refuse_export(
            f"{export.name} carries a name this product gives the intake files it "
            f"writes, and an intake file names every landed track whether or not "
            f"rekordbox imported it, so it proves nothing",
            export,
        )
    for record in waiting:
        artifact = record.pending.artifact if record.pending is not None else None
        if artifact and _same_file(export, Path(artifact)):
            raise _refuse_export(
                f"{export.name} is the intake file run {record.session_id} is "
                f"waiting on, so every track it names is in it whether or not "
                f"rekordbox imported it",
                export,
                session_id=record.session_id,
            )
    content = export.read_bytes()
    if collection_xml.is_stub_listing(content):
        raise refuse(
            "intake-export-is-stub",
            f"{export.name} is a stub listing, not a Fresh Export, so it says "
            f"nothing about what rekordbox holds",
            steps=("take a Fresh Export of the collection from rekordbox and pass that file",),
            origin=_ORIGIN,
            detail={"export": str(export)},
        )
    if rbxml.collection_span(content) is None:
        raise _refuse_export(
            f"{export.name} has no collection section, so it is not a collection export",
            export,
        )
    held: set[str] = set()
    for track in rbxml.collection_tracks(content):
        location = rbxml.attributes(content, track).get("Location", "")
        if not location:
            continue
        try:
            held.add(routing_pass.track_id(location))
        except locations.LocationDecodeError:
            # A row this build cannot decode names no file a run could have
            # placed, since every placed Location was encoded by this build.
            continue
    return held


def _considered(
    cfg: config.Config, wanted: str | None
) -> tuple[list[session.SessionRecord], list[session.SessionRecord]]:
    """The runs waiting on an import, and the proven ones whose file is still here."""
    waiting: list[session.SessionRecord] = []
    unretired: list[session.SessionRecord] = []
    for record in session.records(cfg):
        if record.workflow != ingest.INTAKE_WORKFLOW:
            continue
        if wanted is not None and record.session_id != wanted:
            continue
        if record.state is session.SessionState.AWAITING_IMPORT:
            waiting.append(record)
        elif _proven_artifact(record) is not None:
            unretired.append(record)
    if wanted is not None and not waiting and not unretired:
        raise refuse(
            "intake-list-unusable",
            f"no intake run {wanted} is waiting on an import or holds an intake "
            f"file still to retire",
            origin=_ORIGIN,
            detail={"session_id": wanted},
        )
    return waiting, unretired


def _proven_artifact(record: session.SessionRecord) -> Path | None:
    """The intake file of a run whose import was proven, while it is still there."""
    proven = record.detail.get(session.IMPORT_VERIFIED_KEY)
    if not isinstance(proven, dict) or not proven.get("artifact"):
        return None
    path = Path(str(proven["artifact"]))
    return path if path.is_file() else None


def retire(artifact: Path) -> Path | None:
    """Rename one intake file out of the pending scan. None when it is not there.

    ONLY A FILE THIS PRODUCT NAMED, and only a plain file. The path comes from a
    session record, which is a file on disk somebody could have edited, so the
    name is checked against the suffixes the product writes before anything is
    renamed, and a link is refused rather than followed.

    Never over another file: a batch name can be used again once its first
    intake file is retired, so the second retirement takes the next free name.
    """
    if artifact.is_symlink() or not artifact.is_file():
        return None
    if not any(artifact.name.endswith(suffix) for suffix in tree_registry.PENDING_XML_SUFFIXES):
        raise refuse(
            "internal-error",
            f"{artifact} does not carry a name this product gives an intake file, "
            f"so it is not renamed",
            origin=_ORIGIN,
            detail={"artifact": str(artifact)},
        )
    target = artifact.with_name(artifact.name + RETIRED_SUFFIX)
    count = 1
    while target.exists() or target.is_symlink():
        count += 1
        target = artifact.with_name(f"{artifact.name}{RETIRED_SUFFIX}-{count}")
    artifact.rename(target)
    return target


def _landed(cfg: config.Config, session_id: str) -> tuple[routing_pass.RoutingIntent, ...]:
    return tuple(
        entry for entry in routing_pass.read(cfg).intents if entry.session_id == session_id
    )


def settle(
    record: session.SessionRecord, cfg: config.Config, held: set[str], export: Path
) -> dict[str, Any]:
    """Look at one waiting run, and do what the export proves can be done."""
    item: dict[str, Any] = {"session_id": record.session_id}
    artifact = record.pending.artifact if record.pending is not None else None
    if artifact:
        item["intake_file"] = artifact
    landed = _landed(cfg, record.session_id)
    if not landed:
        # NOTHING RECORDED IS NOT NOTHING OWED. With no Location to look for,
        # an export proves nothing about this run, so it is left as it is.
        return {
            **item,
            "action": UNVERIFIABLE,
            "why": "the routing ledger names no file this run placed, so no export "
            "can prove its import",
        }
    missing = [entry for entry in landed if entry.track not in held]
    if missing:
        return {
            **item,
            "action": NOT_IMPORTED,
            "count": len(landed),
            "missing": len(missing),
            "missing_locations": [entry.location for entry in missing[:MISSING_SHOWN]],
        }
    # THE FILE FIRST, THEN THE RECORD. A rename that fails leaves the run still
    # waiting, so running this again does the whole thing again. The other order
    # would leave a proven run whose file nothing looks for any more.
    retired = retire(Path(artifact)) if artifact else None
    session.mark_import_verified(record, cfg, evidence=f"fresh export {export.name}")
    closed = False
    if not routing_pass.read(cfg).outstanding(record.session_id):
        routing_pass.close_run(record, cfg)
        closed = True
    return {
        **item,
        "action": IMPORTED,
        "count": len(landed),
        "retired_to": str(retired) if retired is not None else None,
        "closed": closed,
    }


def intake_imported(ctx) -> Envelope:
    cfg = intake_cli._load()
    export = Path(ctx.args.export)
    waiting, unretired = _considered(cfg, ctx.args.session)
    items: list[dict[str, Any]] = []
    if waiting:
        held = read_export(export, waiting)
        items.extend(settle(record, cfg, held, export) for record in waiting)
    for record in unretired:
        # PROVEN ELSEWHERE, by the routing pass reaching every row, which is
        # stronger evidence than an export. Only the file is left to deal with.
        artifact = _proven_artifact(record)
        retired = retire(artifact) if artifact is not None else None
        if retired is not None:
            items.append(
                {
                    "session_id": record.session_id,
                    "action": RETIRED,
                    "intake_file": str(artifact),
                    "retired_to": str(retired),
                }
            )
    plan = intake_cli._plan(items, kind="imported")
    plan["totals"] = {
        "count": len(items),
        **{
            action: sum(1 for item in items if item["action"] == action)
            for action in (IMPORTED, NOT_IMPORTED, UNVERIFIABLE, RETIRED)
        },
    }
    if not items:
        return ctx.envelope(data=plan, outcome=Outcome.NO_OP)
    owed = [
        record
        for record, item in zip(waiting, items, strict=False)
        if item["action"] in (NOT_IMPORTED, UNVERIFIABLE)
    ]
    if not owed:
        return ctx.envelope(data=plan, outcome=Outcome.OK)
    warnings = [
        {
            "code": item["action"],
            "message": (
                f"run {item['session_id']}: {item['missing']} of {item['count']} "
                f"landed track(s) are not in {export.name}"
                if item["action"] == NOT_IMPORTED
                else f"run {item['session_id']}: {item['why']}"
            ),
        }
        for item in items
        if item["action"] in (NOT_IMPORTED, UNVERIFIABLE)
    ]
    first = owed[0]
    # The run's own action, persisted when it landed. A record somebody edited
    # can be waiting with none, and the envelope still has to say what is owed.
    pending = next(
        (record.pending for record in owed if record.pending is not None),
        None,
    ) or session.pending_import(
        first,
        artifact="",
        summary=f"run {first.session_id} is waiting on an import this export does not show",
        verify_verb=ingest.VERIFY_VERB,
    )
    return ctx.envelope(
        data=plan,
        outcome=Outcome.PENDING,
        code=ExitCode.PENDING_HUMAN,
        pending=pending,
        warnings=warnings,
    )


__all__ = [
    "IMPORTED",
    "NOT_IMPORTED",
    "RETIRED",
    "RETIRED_SUFFIX",
    "UNVERIFIABLE",
    "build_imported",
    "intake_imported",
    "read_export",
    "retire",
    "settle",
]
