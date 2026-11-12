"""``label.mark``: a landed label batch records its year playlists as taken (R-835, U242).

After a label batch lands, the source system prefixed the label's year
playlists ``DOWNLOADED ``, the same mark a swept playlist carried. This verb is
that step for the year playlists ``label playlists`` built, behind one explicit
gate. SINCE U242 NO TITLE CHANGES: the prefix is retired, decided by Phillip on
2026-11-11, and a marked year playlist is held as taken in Cratekit's own
record, which the root step reads to know a label's tracks are downloaded. The
account's folder is read and never written. Where the rules below say rename,
they now mean that record.

THE INTAKE FILE IS THE PROOF THE BATCH LANDED, and it names the pass. The file
``intake land`` wrote, retired or not, must exist and hold something, which is
``sync/marks.py``'s rule for every irreversible mark: a title is changed only
after the importable file is on disk. The pass's name is read off the file's
name, as ``sync mark`` reads it.

ONLY A YEAR THE BATCH FILED IS MARKED. ``intake land`` writes the batch's
``Record Labels / <Label> / <Label> <year>`` tree into the intake file, so the
file itself says which label and which years it carried, and a year playlist
whose year it did not file under this label is listed and left. Without that a
file from any landing marked every year of any label.

ONLY A PLAYLIST THIS PRODUCT BUILT IS MARKED. The year playlists are the ones
the outbound ledger records for the label, and each is planned only while its
title in the label's folder is still exactly the one it was built under. One
already prefixed, one retitled since, and one no longer in the folder are
listed and left, and so is every year when the folder itself is gone.

EVERY MARK IS A TAKEN ENTRY UNDER THE PASS, in ``sync mark``'s record. That
is what ``sync unmark --pass`` lets go, so a label mark made by mistake is
taken off by the same verb that takes off a sync's.

A DATABASE NATIVE INTAKE TREE WRITES NO INTAKE FILE (R-1056), so there the
pass is named with ``--pass`` instead of ``--xml``, proved the way ``sync mark
--pass`` proves it: the intake tree reads native and a closed native landing
committed under that name. The label and the years filed are read off those
landings' session records, the ``labels`` entries the commit wrote, in place
of the file's tree, and every other rule above holds unchanged. The landings
are in the plan's digest, so a landing of the pass after the answer is
another plan, and the proof is read again before the first rename.

A BATCH THAT FILED NONE OF THE BUILT YEARS SAYS SO, on either proof, with a
warning beside each year's own reason, so a mark of the wrong pass or label
is not read as a mark with nothing left to do.

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

from cratekit.cli.output import Envelope, digest_of, timestamp
from cratekit.core import session
from cratekit.core.cause import CratekitError, Outcome, Scope, refuse
from cratekit.intake import label_filing
from cratekit.label import cli as label_cli
from cratekit.label import registry as labels
from cratekit.label.playlists_cli import NOT_FOLLOWED_SAID
from cratekit.modules.outbound import ledger
from cratekit.sync import mark_record, marks, playlists
from cratekit.sync.mark_cli import (
    ALREADY_MARKED,
    CHANGED_SINCE,
    MARK,
    MARKED,
    NOT_LISTED,
    SKIP,
    native_proof,
    pass_name_of,
)
from cratekit.write import rbxml

_ORIGIN = ("label.mark",)

#: A year playlist whose title is neither the one it was built under nor that
#: title marked, so somebody chose another and it is left alone.
RETITLED = "retitled-since-built"
#: A year the landed batch filed no track of under this label.
NOT_IN_BATCH = "not-in-batch"

#: What the gate screen and the warning say when there is nothing to mark.
NOTHING_BUILT_SAID = (
    "no year playlist was built for this label on this library, so there is "
    "nothing to mark"
)
#: What the warning says when the batch filed none of the built years.
NOTHING_FILED_SAID = (
    "the landed batch filed no track under this label in any year built for it, "
    "so no year playlist is marked"
)
#: The verb a native proof's refusal tells the person to run again, and where
#: a label batch's pass name comes from.
_VERB = "crate label mark"
_NAMED = "the pass name crate label sync --go printed for the batch"


def build_mark(parser, entry) -> None:
    del entry
    parser.add_argument(
        "name",
        metavar="LABEL",
        help="a followed label, by its name or its registry identifier",
    )
    proof = parser.add_mutually_exclusive_group(required=True)
    proof.add_argument(
        "--xml",
        metavar="XML",
        help="the intake file crate intake land wrote for the landed label batch",
    )
    proof.add_argument(
        "--pass",
        dest="pass_name",
        metavar="NAME",
        help=(
            "the pass the label batch was landed with, on a database native intake "
            "tree, which writes no intake file"
        ),
    )
    parser.set_defaults(_handler=label_mark)


def _blocked(message: str, *steps: str, **detail: Any) -> CratekitError:
    return refuse(
        "sync-marks-blocked", message, steps=steps, scope=Scope.SOURCE, origin=_ORIGIN, detail=detail
    )


def batch_years(xml: Path, label: str) -> frozenset[str]:
    """The years the landed batch filed tracks under ``label``, read off its file.

    THE TREE ``intake land`` WROTE, and nothing else: a ``<Label> <year>``
    playlist holding at least one track, directly under a ``<Label>`` folder.
    The landing names both from the manifest's label, which is the registry's
    name for it, so they are compared exactly.
    """
    try:
        content = xml.read_bytes()
    except OSError as exc:
        raise _blocked(
            f"{xml.name} could not be read ({exc.strerror or exc}), so which label "
            f"and years it landed is unknown and nothing was marked",
            "pass the intake file crate intake land wrote for the batch",
            path=str(xml),
        ) from exc
    root = rbxml.root_node(content)
    if root is None:
        return frozenset()
    prefix = f"{label} "
    years: set[str] = set()
    for path, node in rbxml.walk_nodes(content, root):
        if len(path) < 2 or path[-2] != label or not path[-1].startswith(prefix):
            continue
        year = path[-1][len(prefix) :]
        if len(year) == 4 and year.isdigit() and rbxml.track_keys(content, node):
            years.add(year)
    return frozenset(years)


def native_years(
    cfg, proof: marks.NativeLanding, label: str
) -> frozenset[str]:
    """The years the pass's native landings filed tracks under ``label``, read off their records.

    EVERY LANDING THE PROOF NAMES, and nothing else: a pass landed twice filed
    what either landing filed, and a landing abandoned or refused is in no
    proof. A record whose ``labels`` entries this build cannot read is refused
    by name, never read as a batch that filed nothing (pattern 1).
    """
    years: set[str] = set()
    for session_id in proof.landings:
        filed = label_filing.years_filed(session.read_record(session_id, cfg), label)
        if filed is None:
            raise _blocked(
                f"the record of landing {session_id} names what it filed under "
                f"{label_filing.RECORD_KEY!r} in a form this build cannot read, so which "
                f"years the pass filed is unknown and nothing was marked",
                "mark the pass with the build that landed it",
                session=session_id,
                pass_name=proof.pass_name,
            )
        years |= filed
    return frozenset(years)


def _item(
    year: ledger.LabelYear,
    listed: dict[str, str] | None,
    filed: frozenset[str],
    taken: frozenset[str] = frozenset(),
) -> dict[str, Any]:
    """One year playlist, decided against the batch and its folder's titles now.

    ``listed`` is ``None`` when the label's folder is no longer on the account.
    """
    current = None if listed is None else listed.get(year.remote_id)
    base: dict[str, Any] = {
        "id": year.remote_id,
        "year": year.year,
        "name": current or "",
        "built_as": year.name,
    }
    if year.year not in filed:
        return {
            **base,
            "action": SKIP,
            "reason": NOT_IN_BATCH,
            "why": "the landed batch filed no track of this year under the label",
        }
    if current is None:
        return {
            **base,
            "action": SKIP,
            "reason": NOT_LISTED,
            "why": (
                "the label's folder is no longer on the account"
                if listed is None
                else "the label's folder no longer holds it, so there is no title to prefix"
            ),
        }
    if playlists.is_taken(year.remote_id, current, taken):
        return {**base, "action": SKIP, "reason": ALREADY_MARKED, "why": "Cratekit already holds it as taken"}
    if current != year.name:
        return {
            **base,
            "action": SKIP,
            "reason": RETITLED,
            "why": f"it was retitled since it was built as {year.name!r}, so its title is left",
        }
    return {**base, "action": MARK}


def _payload(
    items: list[dict[str, Any]],
    *,
    label: str,
    pass_name: str,
    native: marks.NativeLanding | None = None,
) -> dict[str, Any]:
    identity: dict[str, Any] = {
        "kind": "label-mark",
        "label": label,
        "pass": pass_name,
        "marks": sorted((item["id"], item["built_as"]) for item in items if item["action"] == MARK),
    }
    if native is not None:
        # THE TREE AND THE LANDINGS THAT PROVE THE PASS, as ``sync mark --pass``
        # binds them, so a landing of the pass since the plan is another plan.
        identity["tree"] = native.tree_id
        identity["landings"] = list(native.landings)
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


def _shown(
    payload: dict[str, Any],
    *,
    label: str,
    pass_name: str,
    native: marks.NativeLanding | None = None,
) -> dict[str, Any]:
    shown: dict[str, Any] = {
        "label": label,
        "pass": (
            pass_name
            if native is None
            else f"{pass_name}, landed on the database native {native.tree_id!r} tree"
        ),
        "recorded as taken": [
            item["built_as"] for item in payload["items"] if item["action"] == MARK
        ],
        "on the account": "nothing is renamed; the record is Cratekit's own",
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
    """The failure, with what was taken named in it.

    ``sync mark``'s rule: a refusal the account or the record raised keeps its
    reason and remedy, and anything else is this build's own defect and says so.
    """
    said = (
        f"{len(landed)} year playlist(s) were recorded as taken before this failed, "
        f"and stay taken"
        if landed
        else "no year playlist was recorded as taken before this failed"
    )
    detail = {
        "marked": list(landed),
        "still_unmarked": [one for one in planned if one not in landed],
    }
    again = "run crate label mark again; a playlist already taken is skipped"
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
    if isinstance(exc, OSError):
        return refuse(
            "sync-mark-record-unusable",
            f"{said}. The record could not be written ({type(exc).__name__}: {exc})",
            steps=("make the library's state directory writable by this account", again),
            scope=Scope.SOURCE,
            origin=_ORIGIN,
            detail={**detail, "kind": type(exc).__name__},
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
    # THE PROOF FIRST, before the ledger, the account or a credential: the
    # intake file on the bridge, the native landings by the pass's name.
    xml: Path | None = None
    native: marks.NativeLanding | None = None
    if ctx.args.xml is not None:
        xml = Path(str(ctx.args.xml))
        pass_name = pass_name_of(xml)
        marks.require_output(xml)
    else:
        native = native_proof(cfg, str(ctx.args.pass_name), verb=_VERB, named=_NAMED)
        pass_name = native.pass_name
    name = str(ctx.args.name)
    entry = labels.RegistryStore().load().resolve(name)
    shape = ledger.label_shape(cfg, entry.label_id) if entry is not None else None
    built = sorted((shape.years.values() if shape is not None else ()), key=lambda one: one.year)
    label = entry.name if entry is not None else name
    filed: frozenset[str] = frozenset()
    if built:
        filed = batch_years(xml, label) if xml is not None else native_years(cfg, native, label)
    remote = None
    items: list[dict[str, Any]] = []
    if built and shape is not None and shape.folder_id and filed & {y.year for y in built}:
        from cratekit.modules.outbound import account

        remote = account.resolve(cfg)
        # THE FOLDER IS ASKED FOR FIRST. One deleted on the account is listed
        # as gone for every year, rather than a provider failure on every run.
        listed = (
            remote.folder_playlists(shape.folder_id)
            if shape.folder_id in remote.folders()
            else None
        )
        taken = playlists.taken_ids(cfg)
        items = [_item(year, listed, filed, taken) for year in built]
    elif built:
        # Nothing the batch filed is recorded here, or no folder is: no year
        # can be marked, so each is listed and left and the account is not read.
        items = [_item(year, {}, filed) for year in built]
    payload = _payload(items, label=label, pass_name=pass_name, native=native)
    # THE PLAN ITSELF, for the reason ``label playlists`` gives (R-693).
    option = ctx.gate.require(
        ctx.entry.gates[0],
        plan=payload,
        context=_shown(payload, label=label, pass_name=pass_name, native=native),
    )
    if entry is None:
        # NOT FOLLOWED is said as such, the build verb's warning, so a misspelled
        # label is not read as one whose playlists were never built.
        return ctx.envelope(
            data=payload,
            outcome=Outcome.NO_OP,
            warnings=[{"code": "label-playlists-not-followed", "message": f"{name}: {NOT_FOLLOWED_SAID}"}],
        )
    if not items:
        return ctx.envelope(
            data=payload,
            outcome=Outcome.NO_OP,
            warnings=[{"code": "label-mark-nothing-built", "message": f"{label}: {NOTHING_BUILT_SAID}"}],
        )
    said: list[dict[str, str]] = []
    if not filed & {year.year for year in built}:
        said.append({"code": "label-mark-nothing-filed", "message": f"{label}: {NOTHING_FILED_SAID}"})
    planned = [item["id"] for item in items if item["action"] == MARK]
    if option != "apply" or not planned or remote is None:
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP, warnings=said)

    if native is not None and native_proof(cfg, pass_name, verb=_VERB, named=_NAMED) != native:
        # THE PROOF AGAIN, before the first rename, as ``sync mark --pass``
        # reads it: a tree reverted to the bridge or a landing since the plan
        # is not what the answer covered.
        raise _blocked(
            f"the intake tree or the landings of {pass_name!r} changed since the plan "
            f"was shown, so the answer does not cover them and nothing was marked",
            "run crate label mark again and answer the new plan",
            pass_name=pass_name,
        )
    record = mark_record.MarkRecord(cfg)
    # THE RECORD IS LOCKABLE BEFORE THE FIRST MARK, as ``sync mark`` asks.
    record.ready()
    by_id = {item["id"]: item for item in items}
    landed: list[str] = []
    changed: list[str] = []
    try:
        # THE RECHECK, on the folder read again after the answer. NOTHING IS
        # RENAMED (U242): each year still titled as built is held as taken.
        now = remote.folder_playlists(shape.folder_id)
        for identity in planned:
            item = by_id[identity]
            if now.get(identity) != item["built_as"]:
                changed.append(identity)
                continue
            record.take(
                [
                    mark_record.Taken(
                        playlist_id=identity,
                        name=item["built_as"],
                        by=pass_name,
                        how=mark_record.BY_LABEL,
                        at=timestamp(),
                    )
                ]
            )
            landed.append(identity)
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
                    "why": (
                        "its title in the folder changed since the plan was shown, so it "
                        "was not recorded as taken"
                    ),
                }
            )
            warnings.append(
                {
                    "code": "label-mark-changed-since-plan",
                    "message": f"{item['built_as']} changed since the plan was shown and "
                    f"was not recorded as taken",
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


__all__ = ["build_mark", "label_mark", "native_years"]
