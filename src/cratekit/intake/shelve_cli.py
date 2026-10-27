"""``intake.shelve``: an imported batch is filed into the processed tree behind one gate (U154).

The engine is :mod:`cratekit.intake.shelve`, and this shell owns the plan as
the gate shows it, the gate, and what a person is told afterwards.

THE PLAN IS SHOWN BEFORE ANYTHING MOVES, and the order around the gate is the
landing's own, ``land_cli.ask_then_write``: the database is opened with write
intent before the plan, so a running rekordbox refuses before anything is
shown; the backup acknowledgment is read before the gate; the gate is asked
over the digested plan; only ``apply`` writes. The gate takes no inline answer,
for the landing's reason: a path write on the collection is answered by a
separate recorded act with an actor (R34).

``--report`` PLANS AGAINST A READ ONLY COPY AND WRITES NOTHING, so a person
can see what a shelve would do with no acknowledgment standing and no gate
asked. rekordbox still has to be closed, since the copy is taken by the
guarded writer's own opener. Its plan carries the same digest the gate would
show.

``--as`` NAMES ONE BATCH'S SUBJECT. It replaces the words the batch name
carries, which is what a batch named for its run needs, and is refused with
more than one batch or with ``--all``, since one subject for many batches is a
guess about all but one of them.

Layer: modules. The builder's parameters are unannotated so this file does not
import the CLI registry (KTD23).
"""

from __future__ import annotations

from typing import Any

from cratekit.cli.output import Envelope
from cratekit.core import analysis_store, rb_writer
from cratekit.core.cause import Outcome, Remedy, refuse
from cratekit.intake import cli as intake_cli
from cratekit.intake import land_cli, landing, shelve

#: The gate the verb asks. Looked up by name, as the landing's are.
SHELVE_GATE = "intake.shelve.native"

#: What an item on the plan is marked, and what it becomes on the report.
SHELVE = "shelve"
SHELVED = "shelved"
SKIPPED = "skipped"

#: The warning a plan carries for each batch it left where it was.
BATCH_SKIPPED = "batch-skipped"

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
    items = []
    for item in payload["items"]:
        if item["action"] != SHELVE:
            items.append(item)
            continue
        items.append(
            {
                **item,
                "action": SHELVED,
                "rows": [
                    {
                        **row,
                        "to": read[row["content_id"]].folder_path,
                        **read[row["content_id"]].kept,
                    }
                    for row in item["rows"]
                ],
            }
        )
    return {
        **payload,
        "items": items,
        "totals": {
            **payload["totals"],
            "shelved": len(shelved.batches),
            "session": shelved.session_id,
        },
    }


def _warnings(planned: shelve.ShelfPlan) -> list[dict[str, str]]:
    return [
        {"code": BATCH_SKIPPED, "message": f"{one.batch!r} was left where it is: {one.why}"}
        for one in planned.skipped
    ]


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


def intake_shelve(ctx) -> Envelope:
    cfg = intake_cli._load()
    names: list[str] = list(ctx.args.batch)
    everything: bool = bool(ctx.args.all)
    subject: str | None = ctx.args.subject
    if everything and names:
        raise refuse(
            "intake-list-unusable",
            "--all shelves every batch under the music folder, so a batch is not also "
            "named; give one or the other",
            remedy=Remedy.FIX_COMMAND_LINE,
            origin=_ORIGIN,
            detail={"batches": names},
        )
    if not everything and not names:
        raise refuse(
            "intake-list-unusable",
            "name a batch folder under the music folder, or give --all",
            remedy=Remedy.FIX_COMMAND_LINE,
            origin=_ORIGIN,
        )
    if subject is not None and (everything or len(names) != 1):
        raise refuse(
            "intake-list-unusable",
            "--as names one batch's subject, so it goes with exactly one batch and not with --all",
            remedy=Remedy.FIX_COMMAND_LINE,
            origin=_ORIGIN,
            detail={"batches": names, "subject": subject},
        )
    if subject is not None and not subject.strip():
        raise refuse(
            "intake-list-unusable",
            "--as was given no words; a subject is the words after the date in the "
            "filed folder's name",
            remedy=Remedy.FIX_COMMAND_LINE,
            origin=_ORIGIN,
        )
    if subject is not None and not landing.plain_name(subject.strip()):
        raise refuse(
            "intake-list-unusable",
            f"--as {subject!r} is not one plain folder name; a slash or a path part "
            f"would file the batch somewhere other than its year folder",
            remedy=Remedy.FIX_COMMAND_LINE,
            origin=_ORIGIN,
            detail={"subject": subject},
        )

    def make_plan(db) -> shelve.ShelfPlan:
        return shelve.plan(cfg, db, names, subject=subject, everything=everything)

    if ctx.args.report:
        with rb_writer.read_only_copy(rb_writer.live_db_path(cfg), cfg=cfg) as db:
            planned = make_plan(db)
        return ctx.envelope(data=_payload(planned), outcome=Outcome.OK, warnings=_warnings(planned))

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
    planned_warnings = [
        {"code": BATCH_SKIPPED, "message": f"{item['batch']!r} was left where it is: {item['why']}"}
        for item in payload["items"]
        if item["action"] == SKIPPED
    ]
    if shelved is None:
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP, warnings=planned_warnings)
    return ctx.envelope(data=_reported(payload, shelved), warnings=planned_warnings)


__all__ = [
    "BATCH_SKIPPED",
    "SHELVE",
    "SHELVED",
    "SHELVE_GATE",
    "SKIPPED",
    "build_shelve",
    "intake_shelve",
]
