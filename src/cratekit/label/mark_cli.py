"""``label.mark``: a landed label batch records its year playlists as taken (R-835, U242).

Behind one explicit gate, each year playlist ``label playlists`` built, and the
landed batch filed, is held as taken in ``sync mark``'s record under the pass,
so ``sync unmark --pass`` lets it go. No title changes (U242); the account's
folder is read, never written, and rechecked before the record is written.
The proof is the intake file ``intake land`` wrote, whose tree names the years
filed, or on a database native intake tree (R-1056) ``--pass`` and its
landings' records, which the digest binds. Only a playlist still titled as
built is marked; a batch that filed none of the built years says so.

Layer: modules. The builder's parameters are unannotated so this file does not
import the CLI registry (KTD23).
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from cratekit.cli.output import Envelope, digest_of, timestamp
from cratekit.core import session
from cratekit.core.cause import CratekitError, Outcome, Scope, refuse
from cratekit.intake import label_filing
from cratekit.label import cli as label_cli
from cratekit.label import dated, playlists_cli
from cratekit.label import registry as labels
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

if TYPE_CHECKING:
    from cratekit.modules.outbound import ledger

_ORIGIN = ("label.mark",)

#: A year playlist somebody retitled since it was built, left alone.
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
#: The verb a native proof's refusal names, and where the pass name comes from.
_VERB = "crate label mark"
_NAMED = "the pass name crate label sync --go printed for the batch"


def build_mark(parser, entry) -> None:
    del entry
    playlists_cli.label_argument(parser)
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
    return marks.blocked(_ORIGIN, message, *steps, **detail)


def batch_years(xml: Path, label: str) -> frozenset[str]:
    """The years the batch's file holds a ``<Label> <year>`` playlist with a track
    in, directly under a ``<Label>`` folder, compared exactly."""
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


def native_years(cfg, proof: marks.NativeLanding, label: str) -> frozenset[str]:
    """The years every landing the proof names filed under ``label``; a record this
    build cannot read is refused, never read as filing nothing (pattern 1)."""
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
    """One year playlist, decided against the batch and the folder's titles now,
    ``listed`` ``None`` when the folder is gone."""
    current = None if listed is None else listed.get(year.remote_id)
    base = {"id": year.remote_id, "year": year.year, "name": current or "", "built_as": year.name}

    def skip(reason: str, why: str) -> dict[str, Any]:
        return {**base, "action": SKIP, "reason": reason, "why": why}

    if year.year not in filed:
        return skip(NOT_IN_BATCH, "the landed batch filed no track of this year under the label")
    if current is None:
        return skip(
            NOT_LISTED,
            "the label's folder is no longer on the account"
            if listed is None
            else "the label's folder no longer holds it, so there is nothing to record",
        )
    if playlists.is_taken(year.remote_id, current, taken):
        return skip(ALREADY_MARKED, "Cratekit already holds it as taken")
    if current != year.name:
        return skip(
            RETITLED, f"it was retitled since it was built as {year.name!r}, so its title is left"
        )
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
        # THE TREE AND THE LANDINGS THAT PROVE THE PASS bind the plan.
        identity["tree"] = native.tree_id
        identity["landings"] = list(native.landings)
    actions = [item["action"] for item in items]
    return dated.gate_plan(
        digest_of(identity), items, {MARK: actions.count(MARK), SKIP: actions.count(SKIP)}
    )


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
    """The failure, with what was taken named in it, ``sync mark``'s rule."""
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
    if isinstance(exc, OSError):
        return refuse(
            "sync-mark-record-unusable",
            f"{said}. The record could not be written ({type(exc).__name__}: {exc})",
            steps=("make the library's state directory writable by this account", again),
            scope=Scope.SOURCE,
            origin=_ORIGIN,
            detail={**detail, "kind": type(exc).__name__},
        )
    return dated.refused_part_way(
        exc, said, again, detail, failed="The mark", origin=_ORIGIN, scope=Scope.SOURCE,
        steps=False,
    )


def label_mark(ctx) -> Envelope:
    from cratekit.modules.outbound import ledger

    cfg = label_cli._load()
    # THE PROOF FIRST, before the ledger, the account or a credential.
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
        # THE FOLDER IS ASKED FOR FIRST: one deleted is gone, not a failure.
        listed = (
            remote.folder_playlists(shape.folder_id)
            if shape.folder_id in remote.folders()
            else None
        )
        taken = playlists.taken_ids(cfg)
        items = [_item(year, listed, filed, taken) for year in built]
    elif built:
        # Nothing filed is recorded, or no folder: listed, the account unread.
        items = [_item(year, {}, filed) for year in built]
    payload = _payload(items, label=label, pass_name=pass_name, native=native)
    # THE PLAN ITSELF, for the reason ``label playlists`` gives (R-693).
    option = ctx.gate.require(
        ctx.entry.gates[0],
        plan=payload,
        context=_shown(payload, label=label, pass_name=pass_name, native=native),
    )
    if entry is None:
        # NOT FOLLOWED is said as such, not as never built.
        return playlists_cli.not_followed(ctx, payload, name)
    if not items:
        warning = {"code": "label-mark-nothing-built", "message": f"{label}: {NOTHING_BUILT_SAID}"}
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP, warnings=[warning])
    said: list[dict[str, str]] = []
    if not filed & {year.year for year in built}:
        said = [{"code": "label-mark-nothing-filed", "message": f"{label}: {NOTHING_FILED_SAID}"}]
    planned = [item["id"] for item in items if item["action"] == MARK]
    if option != "apply" or not planned or remote is None:
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP, warnings=said)

    if native is not None and native_proof(cfg, pass_name, verb=_VERB, named=_NAMED) != native:
        # THE PROOF AGAIN, before the first rename.
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
        # THE RECHECK: each year still titled as built is held as taken (U242).
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
            why = (
                "its title in the folder changed since the plan was shown, so it "
                "was not recorded as taken"
            )
            done.append({**item, "action": SKIP, "reason": CHANGED_SINCE, "why": why})
            message = (
                f"{item['built_as']} changed since the plan was shown and "
                f"was not recorded as taken"
            )
            warnings.append({"code": "label-mark-changed-since-plan", "message": message})
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
