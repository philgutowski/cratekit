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
file rekordbox has not seen. The envelope carries a ``rekordbox_import``
pending action naming it, verified by ``route pending``, which is the verb that
closes the intake session :func:`cratekit.intake.ingest.place_files` opens once
the imported rows exist. It BLOCKS NOTHING. A blocking action makes every verb
it names refuse, and no consequence of an unimported landing was driven that
would justify that.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from cratekit.cli.output import Envelope, PendingHumanAction, digest_of, new_pending_id
from cratekit.core import config
from cratekit.core.cause import Outcome
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import cli as intake_cli
from cratekit.intake import landing

#: The action every planned file carries until the apply reports on it.
LAND = "land"
LANDED = "landed"
REFUSED = "refused"

#: The verb that proves an intake file imported. Named here and not in the
#: engine, because a layer below the command line must not spell a verb.
VERIFY_VERB = "route.pending"

INTAKE_SUFFIX = "_inboxed.xml"


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
        required=True,
        metavar="XML",
        help="a Fresh Export of the collection to splice the landed files into",
    )
    parser.add_argument(
        "--name",
        default=None,
        metavar="NAME",
        help="the batch folder under the music folder (default: this run's identifier)",
    )
    parser.set_defaults(_handler=intake_land)


def _payload(
    planned: landing.Plan, *, target: Path, destination: Path, export: Path
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
    return {
        "digest": digest_of(identity),
        "items": items,
        "totals": {"count": len(items)},
        "chunk": None,
    }


def _shown(
    planned: landing.Plan, *, target: Path, destination: Path
) -> dict[str, Any]:
    """What the gate screen puts in front of the person, one line per fact."""
    return {
        "folder": str(planned.folder),
        "lands in": str(target),
        "intake file": str(destination),
        "count": len(planned.items),
        "files": [item.name for item in planned.items],
    }


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
    items: list[dict[str, str]] = []
    for item in payload["items"]:
        entry = refused.get(item["from"])
        if entry is None:
            items.append({**item, "action": LANDED})
        else:
            items.append(
                {**item, "action": REFUSED, "reason": entry.reason, "why": entry.sentence}
            )
    return {
        **payload,
        "items": items,
        "totals": {
            "count": payload["totals"]["count"],
            "landed": len(landed.moved),
            "refused": len(landed.refused),
        },
    }


def _pending(run_id: str, landed: landing.Landed, target: Path) -> PendingHumanAction:
    destination = landed.destination
    return PendingHumanAction(
        kind="rekordbox_import",
        id=new_pending_id(run_id),
        summary=(
            f"{len(landed.moved)} file(s) landed in {target} and are named in "
            f"{destination.name}, which rekordbox has not imported yet"
        ),
        verify_verb=VERIFY_VERB,
        artifact=str(destination),
        steps=(
            f"import {destination} into rekordbox as a rekordbox xml library",
            "then run crate route pending so the imported tracks are filed",
        ),
    )


def intake_land(ctx) -> Envelope:
    cfg = intake_cli._load()
    folder = Path(ctx.args.folder) if ctx.args.folder else Path(cfg.paths.download_staging)
    batch = ctx.args.name if ctx.args.name is not None else default_name(ctx.run.run_id)
    export = Path(ctx.args.export)
    planned = _planned(folder, cfg, batch)
    target = landing.target_dir(cfg, batch)
    destination = intake_file(cfg, batch)
    payload = _payload(planned, target=target, destination=destination, export=export)
    spec = ctx.entry.gates[0]
    option = ctx.gate.require(
        spec,
        digest=payload["digest"],
        context=_shown(planned, target=target, destination=destination),
    )
    if option != "apply" or not planned.items:
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP)
    # The engine lists the folder again and refuses a fingerprint that moved,
    # so the gap between this plan and the moves is its to close, not this
    # shell's. What the gate compared is what the person was shown.
    landed = landing.apply(planned, cfg=cfg, export=export, destination=destination)
    return ctx.envelope(
        data=_reported(payload, landed),
        outcome=Outcome.PENDING,
        code=ExitCode.PENDING_HUMAN,
        pending=_pending(ctx.run.run_id, landed, target),
        warnings=[
            {"code": entry.reason, "message": entry.sentence} for entry in landed.refused
        ],
    )


__all__ = [
    "INTAKE_SUFFIX",
    "VERIFY_VERB",
    "build_land",
    "default_name",
    "intake_file",
    "intake_land",
]
