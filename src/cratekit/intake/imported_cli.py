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

import contextlib
import os
from pathlib import Path
from typing import Any

from cratekit.cli.output import Envelope
from cratekit.core import config, naming, session, tree_registry
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
        default=None,
        metavar="XML",
        help=(
            "a Fresh Export of the collection, taken after the import; needed "
            "whenever a run is waiting on one"
        ),
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
    try:
        content = export.read_bytes()
    except OSError as exc:
        raise _refuse_export(
            f"{export.name} could not be read ({exc.strerror or exc})", export
        ) from exc
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
        try:
            location = rbxml.attributes(content, track).get("Location", "")
            if location:
                held.add(routing_pass.track_id(location))
        except ValueError:
            # A row whose bytes or Location this build cannot decode, and both
            # refusals are a ``ValueError``. SKIPPING IT CAN ONLY WITHHOLD A
            # PROOF, never grant one: a landed track named by such a row reads
            # as missing, and the run stays waiting.
            continue
    return held


def _waiting(record: session.SessionRecord) -> bool:
    """True for a run that still owes a proof of its import.

    TWO SHAPES, AND THE SECOND IS EVERY LANDING MADE BEFORE R-501. Those runs
    were left ``open`` with no pending action and nothing recorded, and they are
    the population the finding was about. Such a run is told apart from a
    destructive session in flight by holding no capture, and from a landing that
    crashed by what the ledger holds for it, which :func:`settle` asks.
    """
    if record.state is session.SessionState.AWAITING_IMPORT:
        return True
    return (
        record.state is session.SessionState.OPEN
        and record.snapshot_path is None
        and record.pending is None
        and session.IMPORT_VERIFIED_KEY not in record.detail
    )


def _considered(
    cfg: config.Config, wanted: str | None
) -> tuple[list[session.SessionRecord], list[session.SessionRecord]]:
    """The runs that owe a proof, and the proven ones with something left to do."""
    waiting: list[session.SessionRecord] = []
    proven: list[session.SessionRecord] = []
    for record in session.records(cfg):
        if record.workflow != ingest.INTAKE_WORKFLOW:
            continue
        if wanted is not None and record.session_id != wanted:
            continue
        if _waiting(record):
            waiting.append(record)
        elif session.IMPORT_VERIFIED_KEY in record.detail:
            proven.append(record)
    if wanted is not None and not waiting and not proven:
        raise refuse(
            "intake-list-unusable",
            f"no intake run {wanted} is waiting on an import or was proven imported",
            origin=_ORIGIN,
            detail={"session_id": wanted},
        )
    return waiting, proven


def _proven_artifact(record: session.SessionRecord) -> Path | None:
    """The intake file of a run whose import was proven, while it is still there."""
    proven = record.detail.get(session.IMPORT_VERIFIED_KEY)
    if not isinstance(proven, dict) or not proven.get("artifact"):
        return None
    path = Path(str(proven["artifact"]))
    return path if path.is_file() and not path.is_symlink() else None


def retire(artifact: Path) -> Path | None:
    """Rename one intake file out of the pending scan. None when it is not there.

    ONLY A FILE THIS PRODUCT NAMED, and only a plain file. The path comes from a
    session record, which is a file on disk somebody could have edited, so the
    name is checked against the suffixes the product writes before anything is
    renamed, and a link is refused rather than followed.

    NEVER OVER ANOTHER FILE, AND THAT IS CLAIMED, NOT CHECKED. A batch name can
    be used again once its first intake file is retired, so a second retirement
    takes the next free name. ``exists()`` and then ``rename`` is a race POSIX
    loses silently, so the target is reserved with an exclusive create first
    (:func:`cratekit.core.naming.claim_target`) and the rename lands on this
    call's own empty claim.
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
    try:
        count = 1
        while not naming.claim_target(target):
            count += 1
            target = artifact.with_name(f"{artifact.name}{RETIRED_SUFFIX}-{count}")
        try:
            os.replace(artifact, target)
        except OSError:
            with contextlib.suppress(OSError):
                target.unlink()
            raise
    except OSError as exc:
        raise refuse(
            "path-permission-denied" if isinstance(exc, PermissionError) else "intake-list-unusable",
            f"{artifact.name} could not be renamed out of the way "
            f"({exc.strerror or exc}), so nothing about its run was changed",
            origin=_ORIGIN,
            detail={"artifact": str(artifact)},
        ) from exc
    return target


def _close_if_nothing_is_owed(
    record: session.SessionRecord, cfg: config.Config, ledger: routing_pass.Ledger
) -> dict[str, Any]:
    """Close a proven run that holds no deferred placement, and report a refusal.

    A REFUSAL HERE IS REPORTED, NOT RAISED. By now the file is retired and the
    proof recorded, both true, and the gated close can still refuse for a reason
    of its own, the library volume or an open reconciliation. Raising would end
    the verb over the runs it had not looked at yet and say nothing of what it
    did. The run stays proven and open, and the next run of this verb tries the
    close again.
    """
    if ledger.outstanding(record.session_id):
        return {"closed": False}
    try:
        routing_pass.close_run(record, cfg)
    except CratekitError as exc:
        return {"closed": False, "close_refused": exc.cause.reason, "why": exc.cause.message}
    return {"closed": True}


def settle(
    record: session.SessionRecord, cfg: config.Config, held: set[str], export: Path
) -> dict[str, Any]:
    """Look at one waiting run, and do what the export proves can be done."""
    item: dict[str, Any] = {"session_id": record.session_id}
    artifact = record.pending.artifact if record.pending is not None else None
    if artifact:
        item["intake_file"] = artifact
    ledger = routing_pass.read(cfg)
    landed = tuple(entry for entry in ledger.intents if entry.session_id == record.session_id)
    if not landed:
        # NOTHING RECORDED IS NOT NOTHING OWED. With no Location to look for,
        # an export proves nothing about this run, so it is left as it is. A
        # landing that crashed before it recorded anything is this shape too.
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
    if record.state is not session.SessionState.AWAITING_IMPORT:
        # A run landed before R-501. It goes through the state it should have
        # been left in, so there is one way out of waiting and not two. It
        # recorded no intake file, so none is retired here: several intake files
        # can name the same tracks, and which one was this run's is not known.
        session.mark_awaiting_import(
            record,
            session.pending_import(
                record,
                artifact="",
                summary="landed before its intake file was recorded",
                verify_verb=ingest.VERIFY_VERB,
            ),
            cfg,
        )
    session.mark_import_verified(record, cfg, evidence=f"fresh export {export.name}")
    return {
        **item,
        "action": IMPORTED,
        "count": len(landed),
        "retired_to": str(retired) if retired is not None else None,
        **_close_if_nothing_is_owed(record, cfg, ledger),
    }


def finish(record: session.SessionRecord, cfg: config.Config) -> dict[str, Any] | None:
    """What is left of a run proven earlier: its file, and its close. None for nothing.

    PROVEN ELSEWHERE OR EARLIER. The routing pass reaching every row is stronger
    evidence than an export, and it closes the run and leaves the file. A close
    this verb was refused last time leaves the run open with nothing owed.
    """
    done: dict[str, Any] = {}
    artifact = _proven_artifact(record)
    retired = retire(artifact) if artifact is not None else None
    if retired is not None:
        done.update({"intake_file": str(artifact), "retired_to": str(retired)})
    if not record.terminal:
        closing = _close_if_nothing_is_owed(record, cfg, routing_pass.read(cfg))
        if closing != {"closed": False}:
            done.update(closing)
    if not done:
        return None
    return {"session_id": record.session_id, "action": RETIRED, **done}


def _no_export(waiting: list[session.SessionRecord]) -> CratekitError:
    return refuse(
        "library-export-unusable",
        f"{len(waiting)} intake run(s) are waiting on an import, and proving one "
        f"takes a collection export taken after it",
        steps=(
            "take a Fresh Export of the collection from rekordbox",
            "run this again with --export and that file",
        ),
        origin=_ORIGIN,
        detail={"sessions": [record.session_id for record in waiting]},
    )


def intake_imported(ctx) -> Envelope:
    cfg = intake_cli._load()
    export = Path(ctx.args.export) if ctx.args.export else None
    if export is not None and not export.is_file():
        # WHETHER OR NOT ANYTHING WILL READ IT. A mistyped path answered "nothing
        # to do", which a person cannot tell from an export that was checked.
        raise _refuse_export(f"no collection export at {export}", export)
    waiting, proven = _considered(cfg, ctx.args.session)
    if waiting and export is None:
        raise _no_export(waiting)
    items: list[dict[str, Any]] = []
    if waiting and export is not None:
        held = read_export(export, waiting)
        items.extend(settle(record, cfg, held, export) for record in waiting)
    owed = [
        record
        for record, item in zip(waiting, items, strict=True)
        if item["action"] in (NOT_IMPORTED, UNVERIFIABLE)
    ]
    items.extend(item for item in (finish(record, cfg) for record in proven) if item is not None)
    plan = intake_cli._plan(items, kind="imported")
    plan["totals"] = {
        "count": len(items),
        **{
            action: sum(1 for item in items if item["action"] == action)
            for action in (IMPORTED, NOT_IMPORTED, UNVERIFIABLE, RETIRED)
        },
    }
    warnings = [
        {
            "code": item["action"],
            "message": (
                f"run {item['session_id']}: {item['missing']} of {item['count']} "
                f"landed track(s) are not in {export.name if export else 'the export'}"
                if item["action"] == NOT_IMPORTED
                else f"run {item['session_id']}: {item['why']}"
            ),
        }
        for item in items
        if item["action"] in (NOT_IMPORTED, UNVERIFIABLE)
    ] + [
        {
            "code": item["close_refused"],
            "message": f"run {item['session_id']} is proven and was not closed: {item['why']}",
        }
        for item in items
        if "close_refused" in item
    ]
    if not items:
        return ctx.envelope(data=plan, outcome=Outcome.NO_OP)
    if not owed:
        return ctx.envelope(data=plan, outcome=Outcome.OK, warnings=warnings)
    first = owed[0]
    # The run's own action, persisted when it landed. A run landed before R-501
    # is waiting with none, and the envelope still has to say what is owed.
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
    "finish",
    "intake_imported",
    "read_export",
    "retire",
    "settle",
]
