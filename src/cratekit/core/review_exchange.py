"""The review queue's export and import, for anyone who genuinely wants a file.

A transport, not an editing surface: an import goes through the same checks
as every other write, and never overwrites a local decision. Imported back
into ``core.review`` at its foot, and only from there.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from cratekit.cli.output import timestamp
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.core.review import (
    _NEXT_ORDINAL,
    EXPORT_VERSION,
    Option,
    Predicate,
    ReviewStore,
    Verdict,
    _assert_declared_queue,
    _coerce_verdict,
    _item_from_row,
    iter_items,
    normalize_kind,
    resolve,
    supersede,
)


def export_document(store: ReviewStore, *, queue: str | None = None) -> dict[str, Any]:
    """Every item, resolved ones included, as a versioned JSON document.

    JSON rather than comma separated text, where a stray column break silently
    changes what somebody decided.
    """
    predicate = Predicate(queue=queue) if queue is not None else None
    return {
        "export": EXPORT_VERSION,
        "queue": str(queue) if queue is not None else "",
        "exported": timestamp(),
        "items": [
            item.to_json() for item in iter_items(store, predicate=predicate, include_resolved=True)
        ],
    }


#: Why one item in a document was not applied. Four conditions with four
#: remedies, so none is reported as "somebody decided differently".
CONFLICT_LOCAL_VERDICT_STANDS = "local-verdict-stands"
CONFLICT_VERDICT_UNREADABLE = "verdict-unreadable"
CONFLICT_ITEM_UNUSABLE = "item-unusable"
CONFLICT_NOT_APPLIED = "verdict-not-applied"


@dataclass(frozen=True, slots=True)
class ImportResult:
    """What an import did, per item, so a caller can report rather than guess.

    ``reasons`` has one entry per conflict. An identifier may be in both
    ``inserted`` and ``conflicts``: the row was taken in, its verdict was not.
    """

    inserted: tuple[str, ...] = ()
    resolved: tuple[str, ...] = ()
    unchanged: tuple[str, ...] = ()
    conflicts: tuple[str, ...] = ()
    reasons: Mapping[str, str] = MappingProxyType({})

    @property
    def applied(self) -> tuple[str, ...]:
        """Everything that CHANGED here, in document order, each one once."""
        return tuple(dict.fromkeys((*self.inserted, *self.resolved)))


def import_document(
    store: ReviewStore, document: Mapping[str, Any], *, actor: str
) -> ImportResult:
    """Take items and verdicts back in, refusing to overwrite a local decision.

    A CONFLICT is reported and not applied, so a losing decision never vanishes
    silently. An unseen item is inserted whole, and a verdict on a locally open
    item is recorded. TOTAL: every item is attempted, and one that cannot be
    applied joins the conflicts rather than aborting the run.
    """
    version = document.get("export")
    if version != EXPORT_VERSION:
        raise refuse(
            "review-file-unusable",
            f"this export says version {version!r} and this build reads "
            f"{EXPORT_VERSION}; importing across versions would guess at what the "
            f"other one meant by a verdict",
            steps=("export again from the build that wrote this file",),
            scope=Scope.RUN, origin=("review",),
            detail={"found": version, "expected": EXPORT_VERSION},
        )
    inserted: list[str] = []
    applied: list[str] = []
    unchanged: list[str] = []
    reasons: dict[str, str] = {}
    for raw in document.get("items") or ():
        if not isinstance(raw, Mapping) or not raw.get("id"):
            continue
        item_id = str(raw["id"])
        incoming = _coerce_verdict(raw.get("verdict"))
        if raw.get("verdict") and incoming is None:
            # A verdict this build cannot represent: reported, never read as none.
            reasons[item_id] = CONFLICT_VERDICT_UNREADABLE
            continue
        unusable = _unusable_reason(raw)
        if unusable is not None:
            # Checked before anything is written, so a bad shape is reported.
            reasons[item_id] = CONFLICT_ITEM_UNUSABLE
            continue
        row = store.conn.execute(
            "SELECT * FROM review_items WHERE item_id = ?", (item_id,)
        ).fetchone()
        if row is None:
            try:
                _insert_imported(store, raw)
            except CratekitError:
                reasons[item_id] = CONFLICT_ITEM_UNUSABLE
                continue
            inserted.append(item_id)
            if incoming is not None and not _apply_incoming(store, item_id, raw, incoming, actor):
                reasons[item_id] = CONFLICT_NOT_APPLIED
            continue
        local = _item_from_row(row)
        if local.stored_verdict is not None and local.verdict is None:
            # A local verdict this build cannot read is a decision; it stands.
            reasons[item_id] = CONFLICT_LOCAL_VERDICT_STANDS
            continue
        if incoming is None or local.verdict is incoming:
            unchanged.append(item_id)
            continue
        if local.resolved:
            reasons[item_id] = CONFLICT_LOCAL_VERDICT_STANDS
            continue
        if _apply_incoming(store, item_id, raw, incoming, actor):
            applied.append(item_id)
        else:
            reasons[item_id] = CONFLICT_NOT_APPLIED
    return ImportResult(
        inserted=tuple(inserted), resolved=tuple(applied), unchanged=tuple(unchanged),
        conflicts=tuple(reasons), reasons=MappingProxyType(dict(reasons)),
    )


def _unusable_reason(raw: Mapping[str, Any]) -> str | None:
    """The field that makes this document item unusable, or None.

    Asked up front by positive type checks, so a malformed item is reported
    rather than raised out of a total import.
    """
    payload = raw.get("payload")
    if payload is not None and not isinstance(payload, Mapping):
        return "payload"
    options = raw.get("options")
    if options is not None:
        if not isinstance(options, (list, tuple)):
            return "options"
        for option in options:
            if not isinstance(option, Mapping):
                return "options"
            if not option.get("option_id"):
                # A candidate with no identifier cannot be chosen.
                return "option_id"
            detail = option.get("detail")
            if detail is not None and not isinstance(detail, Mapping):
                return "option detail"
    return None


def _apply_incoming(
    store: ReviewStore,
    item_id: str,
    raw: Mapping[str, Any],
    verdict: Verdict,
    actor: str,
) -> bool:
    """Record an incoming verdict, reporting rather than raising when it cannot be.

    The refusals of ``resolve`` are about this item alone, so none ends the import.
    """
    try:
        if verdict is Verdict.SUPERSEDED:
            # The machine's verdict travels under the machine's rules: the
            # document's actor is the rule, an option is dropped, and an empty
            # rule is refused by the writer and reported as not applied.
            return bool(supersede(store, (item_id,), rule=str(raw.get("actor") or "")))
        resolve(store, item_id, verdict, option=raw.get("option"),
                actor=str(raw.get("actor") or actor))
    except CratekitError:
        return False
    return True


def _insert_imported(store: ReviewStore, raw: Mapping[str, Any]) -> None:
    """Insert an item that arrived from a file, at this queue's own next ordinal.

    The document's ordinal is a position in another queue, so it is not carried.
    """
    queue = _assert_declared_queue(str(raw.get("queue", "")))
    now = timestamp()
    options = [
        Option.from_json(option).to_json()
        for option in raw.get("options") or () if isinstance(option, Mapping)
    ]
    with store.immediate() as conn:
        conn.execute(
            "INSERT INTO review_items (item_id, queue, kind, payload, options, "
            "handler_key, ordinal, verdict, option, actor, created, updated, decided) "
            "VALUES (?, ?, ?, ?, ?, ?, "
            f"{_NEXT_ORDINAL}, "
            "NULL, NULL, NULL, ?, ?, NULL)",
            (str(raw["id"]), queue, normalize_kind(str(raw.get("kind", ""))),
             json.dumps(dict(raw.get("payload") or {}), sort_keys=True), json.dumps(options),
             str(raw.get("handler_key") or ""), str(raw.get("created") or now), now),
        )
