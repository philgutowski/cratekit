"""``intake.shelve``: an imported batch is filed into the processed tree behind one gate (U154).

The order is the landing's, ``land_cli.ask_then_write``: opened to write before
the plan, so a running rekordbox refuses first; no inline answer (R34).
``--report`` plans on a read only copy and writes nothing. ``--as`` names ONE
batch's subject, since one subject for many would be a guess.

Layer: modules. The builder's parameters are unannotated so this file does not
import the CLI registry (KTD23).
"""

from __future__ import annotations

import os
from typing import Any

from cratekit.cli.output import Envelope, digest_of
from cratekit.core import analysis_store, rb_writer
from cratekit.core.cause import Outcome, Remedy, refuse
from cratekit.intake import batch_name, land_cli, landing, shelve
from cratekit.intake import cli as intake_cli

#: The gate the verb asks. Looked up by name, as the landing's are.
SHELVE_GATE = "intake.shelve.native"

#: What an item on the plan is marked, and what it becomes on the report.
SHELVE = "shelve"
SHELVED = "shelved"
SKIPPED = "skipped"

#: The warning a plan carries for each batch it left where it was.
BATCH_SKIPPED = "batch-skipped"
#: What a named batch a native landing already filed is marked (U164), and
#: the warning a plan carries for it beside batches that are shelved.
ALREADY_FILED = "already-filed"
BATCH_ALREADY_FILED = "batch-already-filed"

_ORIGIN = ("intake.shelve_cli",)


def build_shelve(parser, entry) -> None:
    parser.add_argument(
        "batch",
        nargs="*",
        metavar="BATCH",
        help="the name of a batch folder directly under the music folder; repeat for more",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="every batch folder under the music folder that can be shelved",
    )
    parser.add_argument(
        "--as",
        dest="subject",
        default=None,
        metavar="SUBJECT",
        help="the words after the date in the filed folder's name, for one batch",
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="show the plan against a read only copy and write nothing; no question is asked",
    )
    parser.set_defaults(_handler=intake_shelve)


def _payload(planned: shelve.ShelfPlan) -> dict:
    """The plan as the gate shows it: every batch, where it goes, every row it moves."""
    items: list[dict[str, Any]] = [
        {
            "action": SHELVE,
            "batch": one.batch,
            "from": str(one.source),
            "to": str(one.target),
            "filed_on": one.filed_on.isoformat(),
            "subject": one.subject,
            "rows": [
                {
                    "content_id": row.content_id,
                    "file": row.file_name,
                    "from": row.recorded,
                    "to": row.folder_path,
                }
                for row in one.rows
            ],
        }
        for one in planned.batches
    ]
    items.extend({"action": SKIPPED, "batch": one.batch, "why": one.why} for one in planned.skipped)
    return {
        "digest": planned.digest,
        "items": items,
        "totals": {
            "count": len(planned.batches) + len(planned.skipped),
            "batches": len(planned.batches),
            "rows": planned.rows(),
            "skipped": len(planned.skipped),
        },
        "chunk": None,
    }


def _shown(planned: shelve.ShelfPlan) -> dict[str, Any]:
    return {
        "batches": len(planned.batches),
        "rows": planned.rows(),
        "skipped": len(planned.skipped),
        "to": [str(one.target) for one in planned.batches],
    }


def _reported(payload: dict, shelved: shelve.Shelved) -> dict:
    """The plan, each moved item marked with what the commit did and read back."""
    read = {row.content_id: row for row in shelved.rows}

    def done(row: dict) -> dict:
        back = read[row["content_id"]]
        return {**row, "to": back.folder_path, **back.kept}

    items = [
        item
        if item["action"] != SHELVE
        else {**item, "action": SHELVED, "rows": [done(row) for row in item["rows"]]}
        for item in payload["items"]
    ]
    return {
        **payload,
        "items": items,
        "totals": {
            **payload["totals"],
            "shelved": len(shelved.batches),
            "session": shelved.session_id,
        },
    }


def _skipped(batch: str, why: str) -> dict[str, str]:
    return {"code": BATCH_SKIPPED, "message": f"{batch!r} was left where it is: {why}"}


def _assert_nothing_to_ask(planned: shelve.ShelfPlan) -> None:
    """Refuse a plan of nothing before a gate is asked over it."""
    if planned.batches:
        return
    raise refuse(
        "intake-list-unusable",
        "no batch under the music folder can be shelved, so nothing was moved: "
        + "; ".join(f"{one.batch!r}: {one.why}" for one in planned.skipped),
        origin=_ORIGIN,
        detail={"skipped": [[one.batch, one.why] for one in planned.skipped]},
    )


def _already_filed(cfg, names: list[str]) -> dict[str, str]:
    """Each named batch a native landing filed and the music folder holds no folder of, by its folder."""
    if not names:
        return {}
    folders = batch_name.filed_folders(cfg)
    return {
        name: folders[name]
        for name in dict.fromkeys(names)
        if name in folders and not os.path.lexists(landing.target_dir(cfg, name))
    }


def _misused(message: str, **detail: Any):
    """A command line that names no shelve, refused before anything is read."""
    return refuse(
        "intake-list-unusable",
        message,
        remedy=Remedy.FIX_COMMAND_LINE,
        origin=_ORIGIN,
        detail=detail,
    )


def intake_shelve(ctx) -> Envelope:
    cfg = intake_cli._load()
    names: list[str] = list(ctx.args.batch)
    everything: bool = bool(ctx.args.all)
    subject: str | None = ctx.args.subject
    if everything and names:
        raise _misused(
            "--all shelves every batch under the music folder, so a batch is not also "
            "named; give one or the other",
            batches=names,
        )
    if not everything and not names:
        raise _misused("name a batch folder under the music folder, or give --all")
    if subject is not None and (everything or len(names) != 1):
        raise _misused(
            "--as names one batch's subject, so it goes with exactly one batch and not with --all",
            batches=names,
            subject=subject,
        )
    if subject is not None and not subject.strip():
        raise _misused(
            "--as was given no words; a subject is the words after the date in the "
            "filed folder's name"
        )
    if subject is not None and not landing.plain_name(subject.strip()):
        raise _misused(
            f"--as {subject!r} is not one plain folder name; a slash or a path part "
            f"would file the batch somewhere other than its year folder",
            subject=subject,
        )

    # A BATCH LANDED STRAIGHT INTO THE PROCESSED TREE HAS NOTHING TO SHELVE
    # (U164), which is said, never refused as a missing folder.
    filed = _already_filed(cfg, names)
    names = [name for name in names if name not in filed]
    filed_warnings = [
        {
            "code": BATCH_ALREADY_FILED,
            "message": f"{name!r} was landed straight into {folder}, so there is nothing to shelve",
        }
        for name, folder in filed.items()
    ]
    if filed and not names:
        return ctx.envelope(
            data={
                "digest": digest_of({"kind": "shelve", "already_filed": sorted(filed.items())}),
                "items": [
                    {"action": ALREADY_FILED, "batch": name, "folder": folder}
                    for name, folder in filed.items()
                ],
                "totals": {"count": len(filed), "batches": 0, "rows": 0, "already filed": len(filed)},
                "chunk": None,
            },
            outcome=Outcome.NO_OP,
            warnings=filed_warnings,
        )

    def make_plan(db) -> shelve.ShelfPlan:
        return shelve.plan(cfg, db, names, subject=subject, everything=everything)

    if ctx.args.report:
        with rb_writer.read_only_copy(rb_writer.live_db_path(cfg), cfg=cfg) as db:
            planned = make_plan(db)
        return ctx.envelope(
            data=_payload(planned),
            outcome=Outcome.OK,
            warnings=[*filed_warnings, *(_skipped(one.batch, one.why) for one in planned.skipped)],
        )

    def plan_then_check(db) -> shelve.ShelfPlan:
        planned = make_plan(db)
        _assert_nothing_to_ask(planned)
        return planned

    def write(db, planned: shelve.ShelfPlan) -> shelve.Shelved:
        return shelve.apply(cfg, db, planned, analysis_roots=analysis_store.watch_roots(cfg))

    payload, shelved = land_cli.ask_then_write(
        ctx,
        cfg,
        land_cli.gate_named(ctx.entry, SHELVE_GATE),
        plan=plan_then_check,
        payload=_payload,
        shown=_shown,
        write=write,
    )
    skips = [
        _skipped(item["batch"], item["why"])
        for item in payload["items"]
        if item["action"] == SKIPPED
    ]
    planned_warnings = [*filed_warnings, *skips]
    if shelved is None:
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP, warnings=planned_warnings)
    return ctx.envelope(data=_reported(payload, shelved), warnings=planned_warnings)
