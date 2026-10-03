"""``label.mark``: a landed label batch prefixes its year playlists (R-835).

After a label batch lands, the source system prefixes the label's year
playlists ``DOWNLOADED ``, the same mark a swept playlist carries. This verb is
that step for the year playlists ``label playlists`` built, behind one explicit
gate.

THE INTAKE FILE IS THE PROOF THE BATCH LANDED, and it names the pass. The file
``intake land`` wrote, retired or not, must exist and hold something, which is
``sync/marks.py``'s rule for every irreversible mark: a title is changed only
after the importable file is on disk. The pass's name is read off the file's
name, as ``sync mark`` reads it.

ONLY A PLAYLIST THIS PRODUCT BUILT IS MARKED. The year playlists are the ones
the outbound ledger records for the label, and each is planned only while its
title in the label's folder is still exactly the one it was built under. One
already prefixed, one retitled since, and one no longer in the folder are
listed and left.

EVERY RENAME IS RECORDED AS IT LANDS, in ``sync mark``'s record, under the
pass, with the title before and the title written. That is what ``sync unmark
--pass`` reads, so a label mark made by mistake is taken off by the same verb
that takes off a sync's.

THE FOLDER IS READ, NOT THE ACCOUNT. The year playlists live in one folder, and
listing it is one short read where listing every playlist on the account cost
hundreds of provider calls when ``sync unmark`` was run live. The run that
carries out the answer reads the folder again and rechecks each title first.

Layer: modules. The builder's parameters are unannotated so this file does not
import the CLI registry (KTD23).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from cratekit.cli.output import Envelope, digest_of
from cratekit.core.cause import CratekitError, Outcome, Scope, refuse
from cratekit.intake import land_cli
from cratekit.label import cli as label_cli
from cratekit.label import registry as labels
from cratekit.modules.outbound import folders, ledger
from cratekit.sync import mark_record, marks
from cratekit.sync.mark_cli import ALREADY_MARKED, CHANGED_SINCE, MARK, MARKED, NOT_LISTED, SKIP

_ORIGIN = ("label.mark",)

#: A year playlist whose title is neither the one it was built under nor that
#: title marked, so somebody chose another and it is left alone.
RETITLED = "retitled-since-built"

#: What the gate screen and the warning say when there is nothing to mark.
NOTHING_BUILT_SAID = (
    "no year playlist was built for this label on this library, so there is "
    "nothing to mark"
)


def build_mark(parser, entry) -> None:
    del entry
    parser.add_argument(
        "name",
        metavar="LABEL",
        help="a followed label, by its name or its registry identifier",
    )
    parser.add_argument(
        "--xml",
        required=True,
        metavar="XML",
        help="the intake file crate intake land wrote for the landed label batch",
    )
    parser.set_defaults(_handler=label_mark)


def _blocked(message: str, *steps: str, **detail: Any) -> CratekitError:
    return refuse(
        "sync-marks-blocked", message, steps=steps, scope=Scope.SOURCE, origin=_ORIGIN, detail=detail
    )


def _pass_name(xml: Path) -> str:
    """The pass's name, read off the intake file's, retired or not."""
    written = land_cli.unretired_name(xml.name)
    if not written.endswith(land_cli.INTAKE_SUFFIX) or written == land_cli.INTAKE_SUFFIX:
        raise _blocked(
            f"{xml.name} is not named as an intake file, so it does not say which "
            f"batch landed and nothing can be marked from it",
            f"pass the file ending in {land_cli.INTAKE_SUFFIX} that crate intake land wrote",
            path=str(xml),
        )
    return written[: -len(land_cli.INTAKE_SUFFIX)]


def _item(year: ledger.LabelYear, listed: dict[str, str]) -> dict[str, Any]:
    """One year playlist, decided against the titles its folder shows now."""
    current = listed.get(year.remote_id)
    to = folders.MARK_PREFIX + year.name
    base: dict[str, Any] = {
        "id": year.remote_id,
        "year": year.year,
        "name": current or "",
        "built_as": year.name,
        "to": to,
    }
    if current is None:
        return {
            **base,
            "action": SKIP,
            "reason": NOT_LISTED,
            "why": "the label's folder no longer holds it, so there is no title to prefix",
        }
    if current.startswith(folders.MARK_PREFIX):
        return {**base, "action": SKIP, "reason": ALREADY_MARKED, "why": "its name already carries the prefix"}
    if current != year.name:
        return {
            **base,
            "action": SKIP,
            "reason": RETITLED,
            "why": f"it was retitled since it was built as {year.name!r}, so its title is left",
        }
    return {**base, "action": MARK}


def _payload(items: list[dict[str, Any]], *, label: str, pass_name: str) -> dict[str, Any]:
    identity = {
        "kind": "label-mark",
        "label": label,
        "pass": pass_name,
        "marks": sorted((item["id"], item["built_as"], item["to"]) for item in items if item["action"] == MARK),
    }
    return {
        "digest": digest_of(identity),
        "items": items,
        "totals": {
            "count": len(items),
            MARK: sum(1 for item in items if item["action"] == MARK),
            SKIP: sum(1 for item in items if item["action"] == SKIP),
        },
        "chunk": None,
    }


def _shown(payload: dict[str, Any], *, label: str, pass_name: str) -> dict[str, Any]:
    shown: dict[str, Any] = {
        "label": label,
        "pass": pass_name,
        "renamed on the account": [
            f"{item['built_as']} -> {item['to']}" for item in payload["items"] if item["action"] == MARK
        ],
        "left alone": [
            f"{item['name'] or item['built_as']}: {item['why']}"
            for item in payload["items"]
            if item["action"] == SKIP
        ],
        "undone by": f"crate sync unmark --pass {pass_name}",
    }
    if not payload["items"]:
        shown["nothing to mark"] = NOTHING_BUILT_SAID
    return shown


def _failed_part_way(exc: Exception, landed: list[str], planned: list[str]) -> CratekitError:
    said = (
        f"{len(landed)} year playlist(s) were marked before this failed, and each is "
        f"recorded for sync unmark"
        if landed
        else "no year playlist was marked before this failed"
    )
    detail = {"marked": list(landed), "still_unmarked": [one for one in planned if one not in landed]}
    again = "run crate label mark again; a playlist already marked is skipped"
    if isinstance(exc, CratekitError):
        cause = exc.cause
        return refuse(
            cause.reason,
            f"{said}. {cause.message}",
            remedy=cause.remediation.remedy,
            steps=(*cause.remediation.steps, again),
            scope=Scope.SOURCE,
            retryable=cause.retryable,
            origin=_ORIGIN,
            detail={**dict(cause.detail), **detail},
            inner=cause,
        )
    return refuse(
        "internal-error",
        f"{said}. The mark failed in a way this build does not expect "
        f"({type(exc).__name__}: {exc})",
        scope=Scope.SOURCE,
        origin=_ORIGIN,
        detail={**detail, "kind": type(exc).__name__},
    )


def label_mark(ctx) -> Envelope:
    cfg = label_cli._load()
    xml = Path(str(ctx.args.xml))
    pass_name = _pass_name(xml)
    # THE PROOF FIRST, before the ledger, the account or a credential.
    marks.require_output(xml)
    name = str(ctx.args.name)
    entry = labels.RegistryStore().load().resolve(name)
    shape = ledger.label_shape(cfg, entry.label_id) if entry is not None else None
    built = sorted((shape.years.values() if shape is not None else ()), key=lambda one: one.year)
    label = entry.name if entry is not None else name
    remote = None
    items: list[dict[str, Any]] = []
    if built and shape is not None and shape.folder_id:
        from cratekit.modules.outbound import account

        remote = account.resolve(cfg)
        listed = remote.folder_playlists(shape.folder_id)
        items = [_item(year, listed) for year in built]
    elif built:
        # Year playlists recorded and no folder: none can be read where they
        # are kept, so each is listed and left rather than renamed unseen.
        items = [_item(year, {}) for year in built]
    payload = _payload(items, label=label, pass_name=pass_name)
    option = ctx.gate.require(
        ctx.entry.gates[0],
        digest=payload["digest"],
        context=_shown(payload, label=label, pass_name=pass_name),
    )
    if not items:
        return ctx.envelope(
            data=payload,
            outcome=Outcome.NO_OP,
            warnings=[{"code": "label-mark-nothing-built", "message": f"{label}: {NOTHING_BUILT_SAID}"}],
        )
    planned = [item["id"] for item in items if item["action"] == MARK]
    if option != "apply" or not planned or remote is None:
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP)

    record = mark_record.MarkRecord(cfg)
    # THE RECORD IS LOCKABLE BEFORE THE FIRST RENAME, as ``sync mark`` asks.
    record.ready()
    by_id = {item["id"]: item for item in items}
    landed: list[str] = []
    changed: list[str] = []
    try:
        now = remote.folder_playlists(shape.folder_id)
        for identity in planned:
            item = by_id[identity]
            if now.get(identity) != item["built_as"]:
                changed.append(identity)
                continue
            remote.rename_playlist(identity, item["to"])
            landed.append(identity)
            record.record_marked(pass_name, {identity: (item["built_as"], item["to"])})
    except Exception as exc:
        raise _failed_part_way(exc, landed, planned) from exc

    done: list[dict[str, Any]] = []
    warnings: list[dict[str, str]] = []
    for item in items:
        if item["id"] in landed:
            done.append({**item, "action": MARKED})
        elif item["id"] in changed:
            done.append(
                {
                    **item,
                    "action": SKIP,
                    "reason": CHANGED_SINCE,
                    "why": "its title in the folder changed since the plan was shown, so it was not renamed",
                }
            )
            warnings.append(
                {
                    "code": "label-mark-changed-since-plan",
                    "message": f"{item['built_as']} changed since the plan was shown and was not renamed",
                }
            )
        else:
            done.append(item)
    totals = {
        "count": len(done),
        MARKED: len(landed),
        SKIP: sum(1 for item in done if item["action"] == SKIP),
    }
    return ctx.envelope(
        data={**payload, "items": done, "totals": totals},
        outcome=Outcome.OK if landed else Outcome.NO_OP,
        warnings=warnings,
    )


__all__ = ["build_mark", "label_mark"]
