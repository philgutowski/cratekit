"""The review queue's export and import, for anyone who genuinely wants a file.

Split from ``core.review`` to keep each module readable; every name here is
imported back into ``core.review`` and used from there, and only
``core.review`` imports this module, at its foot.
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

# ---------------------------------------------------------------------------
# Export and import, for anyone who genuinely wants a file
# ---------------------------------------------------------------------------


def export_document(store: ReviewStore, *, queue: str | None = None) -> dict[str, Any]:
    """Every item, resolved ones included, as a versioned document.

    JSON rather than a comma separated file, and the difference is the point: the
    thing being replaced is a format a person edits by hand and a program reads
    back, where a stray column break silently changes what somebody decided. This
    is a transport, not an editing surface, and importing it goes through the same
    validation every other write does.
    """
    predicate = Predicate(queue=queue) if queue is not None else None
    return {
        "export": EXPORT_VERSION,
        "queue": str(queue) if queue is not None else "",
        "exported": timestamp(),
        "items": [
            item.to_json()
            for item in iter_items(store, predicate=predicate, include_resolved=True)
        ],
    }


#: Why one item in a document was not applied. A conflict is FOUR conditions
#: wearing one name, and a caller that reports them all as "somebody else decided
#: this differently" is lying about three of them. The remedy differs for each:
#: re-export from the build that wrote it, fix the file, resolve the disagreement
#: by hand, or simply run it again.
CONFLICT_LOCAL_VERDICT_STANDS = "local-verdict-stands"
CONFLICT_VERDICT_UNREADABLE = "verdict-unreadable"
CONFLICT_ITEM_UNUSABLE = "item-unusable"
CONFLICT_NOT_APPLIED = "verdict-not-applied"


@dataclass(frozen=True, slots=True)
class ImportResult:
    """What an import did, per item, so a caller can report rather than guess.

    ``reasons`` carries one entry per conflict, and every conflict has one. A
    caller that had only the identifiers had to invent a sentence, and the
    sentence it invented was true of one case in four.

    An identifier may appear in ``inserted`` AND in ``conflicts``: the row was
    taken in and the verdict on it was not. Both are facts, and a caller showing
    the concatenation shows one item twice, so the reporting layer folds them.
    """

    inserted: tuple[str, ...] = ()
    resolved: tuple[str, ...] = ()
    unchanged: tuple[str, ...] = ()
    conflicts: tuple[str, ...] = ()
    reasons: Mapping[str, str] = MappingProxyType({})

    @property
    def applied(self) -> tuple[str, ...]:
        """Everything that CHANGED here, in document order, each one once."""
        seen: dict[str, None] = {}
        for item_id in (*self.inserted, *self.resolved):
            seen[item_id] = None
        return tuple(seen)


def import_document(
    store: ReviewStore, document: Mapping[str, Any], *, actor: str
) -> ImportResult:
    """Take items and verdicts back in, refusing to overwrite a local decision.

    A CONFLICT is reported and not applied. Two people who both resolved the same
    item differently is a real situation, and picking one silently is how the
    losing decision disappears with nobody told. Everything else applies: an item
    the local queue has never seen is inserted whole, and a verdict on an item
    that is locally still open is recorded.

    THE IMPORT IS TOTAL. Every item the document carries is attempted, and one
    that cannot be applied joins the conflicts rather than aborting the run. A
    partial import that stopped at item forty would leave the queue in a state
    nobody asked for and report nothing about it, which is the same shape as a
    refusal that has already written something.
    """
    version = document.get("export")
    if version != EXPORT_VERSION:
        raise refuse(
            "review-file-unusable",
            f"this export says version {version!r} and this build reads "
            f"{EXPORT_VERSION}; importing across versions would guess at what the "
            f"other one meant by a verdict",
            steps=("export again from the build that wrote this file",),
            scope=Scope.RUN,
            origin=("review",),
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
            # A verdict this build has no representation for. Reported rather
            # than dropped: reading it as "no verdict" would silently discard a
            # decision somebody made, and the file would look imported.
            reasons[item_id] = CONFLICT_VERDICT_UNREADABLE
            continue
        unusable = _unusable_reason(raw)
        if unusable is not None:
            # Checked BEFORE anything is written. Two of these shapes used to
            # leave as a type error and a key error, out of the middle of the
            # loop, after earlier items had already landed: an import that
            # cannot say what it did, and cannot be re-run because the good half
            # is already in.
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
            # A local verdict this build cannot READ, which is not the same as no
            # verdict at all. Applying over it would discard a decision somebody
            # made on a build that could represent it, with nobody told.
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
        inserted=tuple(inserted),
        resolved=tuple(applied),
        unchanged=tuple(unchanged),
        conflicts=tuple(reasons),
        reasons=MappingProxyType(dict(reasons)),
    )


def _unusable_reason(raw: Mapping[str, Any]) -> str | None:
    """Whether this document item is a shape the queue can take in at all.

    Asked once, up front, so a malformed item is REPORTED rather than raised out
    of the middle of a total import. Every check here is a positive recognition
    of a field's type rather than a guess at what a wrong one might do, because
    the two failures this replaces were both an ordinary Python builtin raising
    on input it was never given a rule for.
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
                # A candidate with no identifier cannot be chosen, and a verdict
                # naming one is a decision about something nobody can address.
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

    The refusals ``resolve`` raises are about THIS item: a candidate the item
    does not offer, or a race with another process. Neither says anything about
    the ninety-nine items after it in the file, so neither may end the import.
    """
    try:
        if verdict is Verdict.SUPERSEDED:
            # The machine's verdict travels under the machine's rules: the
            # document's actor is the rule, an option it carries is dropped
            # since a rule chooses no candidate, and an empty rule is refused
            # by the writer and reported here as not applied.
            return bool(supersede(store, (item_id,), rule=str(raw.get("actor") or "")))
        resolve(
            store,
            item_id,
            verdict,
            option=raw.get("option"),
            actor=str(raw.get("actor") or actor),
        )
    except CratekitError:
        return False
    return True


def _insert_imported(store: ReviewStore, raw: Mapping[str, Any]) -> None:
    """Insert an item that arrived from a file, at this queue's own ordinal.

    The ordinal is re-allocated rather than carried across, because it is a
    position in THIS queue. Importing somebody else's positions would interleave
    two orderings and make paging skip items on both sides of the join.
    """
    queue = _assert_declared_queue(str(raw.get("queue", "")))
    now = timestamp()
    options = [
        Option.from_json(option).to_json()
        for option in raw.get("options") or ()
        if isinstance(option, Mapping)
    ]
    with store.immediate() as conn:
        conn.execute(
            "INSERT INTO review_items (item_id, queue, kind, payload, options, "
            "handler_key, ordinal, verdict, option, actor, created, updated, decided) "
            "VALUES (?, ?, ?, ?, ?, ?, "
            f"{_NEXT_ORDINAL}, "
            "NULL, NULL, NULL, ?, ?, NULL)",
            (
                str(raw["id"]),
                queue,
                normalize_kind(str(raw.get("kind", ""))),
                json.dumps(dict(raw.get("payload") or {}), sort_keys=True),
                json.dumps(options),
                str(raw.get("handler_key") or ""),
                str(raw.get("created") or now),
                now,
            ),
        )
