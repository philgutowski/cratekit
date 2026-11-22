"""Held offers: what a producer withheld from a review queue, and can return (R-798, R-815).

A hold is neither an item nor a suppression: it is never decided, a person can
return it, and a returned hold is kept so nothing holds that candidate again.
Imported back into ``core.review`` at its foot, and only from there.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from cratekit.cli.output import canonical_json, timestamp
from cratekit.core.review import (
    RUN_FIELD,
    ReviewStore,
    _assert_declared_queue,
    _payload_of,
    item_id_for,
    normalize_identity,
    normalize_kind,
)

#: A hold in force. The producer judges it again on every round that reaches it.
HOLD_HELD = "held"
#: A hold a person returned to the queue. Kept, so nothing holds it a second time.
HOLD_RETURNED = "returned"
HOLD_STATES: tuple[str, ...] = (HOLD_HELD, HOLD_RETURNED)


@dataclass(frozen=True, slots=True)
class Hold:
    """One candidate a producer withheld from a queue, with what it would have filed.

    ``item_id`` is the identifier the candidate would carry as an item.
    ``reason`` is the sentence a person reads, and ``detail`` what the producer
    judged on, kept so it can judge again.
    """

    queue: str
    item_id: str
    kind: str
    identity: dict[str, Any]
    payload: dict[str, Any]
    group: str
    name: str
    reason: str
    detail: dict[str, Any]
    state: str
    run_id: str
    created: str
    updated: str

    def to_json(self) -> dict[str, Any]:
        return {
            "queue": self.queue,
            "item_id": self.item_id,
            "kind": self.kind,
            "identity": dict(self.identity),
            "payload": dict(self.payload),
            "group": self.group,
            "name": self.name,
            "reason": self.reason,
            "detail": dict(self.detail),
            "state": self.state,
            "run": self.run_id,
            "created": self.created,
            "updated": self.updated,
        }


def _hold_of(row: sqlite3.Row) -> Hold:
    # A column this build cannot read is an empty map, never a crash: the row
    # still names the release, and a producer judges nothing from no words.
    return Hold(
        queue=row["queue"],
        item_id=row["item_id"],
        kind=row["kind"],
        identity=_payload_of(row["identity"]),
        payload=_payload_of(row["payload"]),
        group=row["group_key"],
        name=row["group_name"],
        reason=row["reason"],
        detail=_payload_of(row["detail"]),
        state=row["state"],
        run_id=row["run_id"],
        created=row["created"],
        updated=row["updated"],
    )


def _held_row(store: ReviewStore, queue: str, item_id: str) -> sqlite3.Row | None:
    return store.conn.execute(
        "SELECT * FROM held_offers WHERE queue = ? AND item_id = ?", (queue, item_id)
    ).fetchone()


#: The payload field marking a hold whose candidate :func:`withhold` took back
#: out of the queue (R-815). Dropping such a hold must not make a candidate a
#: person was shown vanish from both places.
WITHHELD_FIELD = "withheld_from_review"

#: The payload fields a refresh carries over from the hold it replaces when the
#: new payload does not name them: history the refreshing producer cannot know.
_CARRIED_ACROSS_A_REFRESH: tuple[str, ...] = (RUN_FIELD, WITHHELD_FIELD)


def _put_hold(
    store: ReviewStore, conn: sqlite3.Connection, *, queue: str, item_id: str, kind: str,
    identity: str, payload: Mapping[str, Any], group: str, name: str, reason: str,
    detail: Mapping[str, Any], run_id: str, state: str,
) -> None:
    """Write one hold row inside the caller's transaction. THE ONE WRITER.

    No row yet: inserted in ``state``. A hold IN FORCE is refreshed: payload,
    reason and detail replaced, run and creation kept. A RETURNED hold is left
    exactly as it is.
    """
    now = timestamp()
    encoded_detail = json.dumps(dict(detail), sort_keys=True)
    row = _held_row(store, queue, item_id)
    if row is None:
        conn.execute(
            "INSERT INTO held_offers (queue, item_id, kind, identity, payload, "
            "group_key, group_name, reason, detail, state, run_id, created, updated) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (queue, item_id, kind, identity, json.dumps(dict(payload), sort_keys=True),
             group, name, reason, encoded_detail, state, run_id, now, now),
        )
    elif row["state"] == HOLD_HELD:
        refreshed = dict(payload)
        replaced = _hold_of(row).payload
        for carried in _CARRIED_ACROSS_A_REFRESH:
            if replaced.get(carried) and not refreshed.get(carried):
                refreshed[carried] = replaced[carried]
        conn.execute(
            "UPDATE held_offers SET payload = ?, group_key = ?, group_name = ?, "
            "reason = ?, detail = ?, updated = ? WHERE queue = ? AND item_id = ?",
            (json.dumps(refreshed, sort_keys=True), group, name, reason, encoded_detail,
             now, queue, item_id),
        )


def hold(
    store: ReviewStore,
    *,
    queue: str,
    kind: str,
    identity: Mapping[str, Any],
    payload: Mapping[str, Any],
    group: str,
    name: str,
    reason: str,
    detail: Mapping[str, Any],
    run_id: str,
    returned: bool = False,
) -> Hold:
    """Withhold one candidate from ``queue``, or refresh the hold already there.

    ``returned`` makes a NEW row already returned, recording a person's answer
    for a candidate in the queue; it changes nothing about an existing row.

    A HOLD A PERSON RETURNED IS NEVER HELD AGAIN: it is handed back as it
    stands, so the producer sees its hold did not take. A refresh keeps the
    first round's run and time, so a round's count of holds does not move, and
    keeps the replaced payload's history fields when the new one lacks them
    (R-815), so a returned candidate is filed under the run that filed it.
    """
    declared = _assert_declared_queue(queue)
    item_id = item_id_for(declared, kind, identity)
    with store.immediate() as conn:
        _put_hold(
            store,
            conn,
            queue=declared,
            item_id=item_id,
            kind=normalize_kind(kind),
            identity=canonical_json(normalize_identity(identity)),
            payload=payload,
            group=group,
            name=name,
            reason=reason,
            detail=detail,
            run_id=run_id,
            state=HOLD_RETURNED if returned else HOLD_HELD,
        )
    return _hold_of(_held_row(store, declared, item_id))


def withhold(
    store: ReviewStore,
    item_id: str,
    *,
    group: str,
    name: str,
    reason: str,
    detail: Mapping[str, Any],
    run_id: str,
) -> Hold | None:
    """Move one OPEN item out of its queue and into a hold, or None when it may not.

    R-815. The item's row is deleted and a hold carrying its payload, marked
    with :data:`WITHHELD_FIELD`, is written in ONE TRANSACTION, so the candidate
    is never both decidable and held, nor neither. Not a verdict: a superseded
    item would still read as offered.

    Only over an empty verdict column, checked inside the transaction, on the
    rule :func:`supersede` states. None too for a hold a person returned and
    for an unknown identifier: each None means nothing was moved. An imported
    item carries no identity, so its hold carries an empty one.
    """
    with store.immediate() as conn:
        row = conn.execute(
            "SELECT queue, kind, identity, payload, verdict, ordinal FROM review_items "
            "WHERE item_id = ?",
            (item_id,),
        ).fetchone()
        if row is None or row["verdict"] is not None:
            return None
        queue = row["queue"]
        standing = _held_row(store, queue, item_id)
        if standing is not None and standing["state"] == HOLD_RETURNED:
            return None
        try:
            carried = json.loads(row["payload"])
        except ValueError:
            carried = {}
        _put_hold(
            store,
            conn,
            queue=queue,
            item_id=item_id,
            kind=row["kind"],
            identity=row["identity"] if row["identity"] is not None else "{}",
            payload={**(carried if isinstance(carried, dict) else {}), WITHHELD_FIELD: True},
            group=group,
            name=name,
            reason=reason,
            detail=detail,
            run_id=run_id,
            state=HOLD_HELD,
        )
        # The floor before the delete, so this ordinal is never reused (``ordinal_floor``).
        conn.execute(
            "INSERT INTO ordinal_floor (id, ordinal) VALUES (1, ?) "
            "ON CONFLICT(id) DO UPDATE SET ordinal = MAX(ordinal, excluded.ordinal)",
            (int(row["ordinal"]),),
        )
        conn.execute(
            "DELETE FROM review_items WHERE item_id = ? AND verdict IS NULL", (item_id,)
        )
    return _hold_of(_held_row(store, queue, item_id))


def find_hold(store: ReviewStore, *, queue: str, item_id: str) -> Hold | None:
    """The hold on ``item_id`` in any state, or None when nothing ever held it."""
    row = _held_row(store, _assert_declared_queue(queue), item_id)
    return _hold_of(row) if row is not None else None


def holds(
    store: ReviewStore,
    *,
    queue: str,
    states: Sequence[str] = (HOLD_HELD,),
    group: str | None = None,
) -> tuple[Hold, ...]:
    """Every hold on ``queue`` in one of ``states``, oldest first, optionally one ``group``'s."""
    wanted = tuple(states)
    marks = ", ".join("?" for _ in wanted)
    narrowed = " AND group_key = ?" if group is not None else ""
    rows = store.conn.execute(
        f"SELECT * FROM held_offers WHERE queue = ? AND state IN ({marks}){narrowed} "
        f"ORDER BY created, item_id",
        (_assert_declared_queue(queue), *wanted, *((group,) if group is not None else ())),
    ).fetchall()
    return tuple(_hold_of(row) for row in rows)


def release_hold(store: ReviewStore, *, queue: str, item_id: str) -> bool:
    """Drop a hold IN FORCE, because its producer filed the candidate after all.

    True when a row was dropped. A returned hold is kept, the record that stops
    anything holding it again.
    """
    with store.immediate() as conn:
        dropped = conn.execute(
            "DELETE FROM held_offers WHERE queue = ? AND item_id = ? AND state = ?",
            (_assert_declared_queue(queue), item_id, HOLD_HELD),
        )
        return dropped.rowcount > 0


def return_hold(store: ReviewStore, *, queue: str, item_id: str) -> Hold | None:
    """Mark a hold returned by a person, and hand it back, or None for no such hold.

    The mark only. The caller files the candidate FIRST, through :func:`offer`,
    so no returned hold lacks its item. An already returned hold comes back
    unchanged.
    """
    declared = _assert_declared_queue(queue)
    with store.immediate() as conn:
        row = _held_row(store, declared, item_id)
        if row is None:
            return None
        if row["state"] != HOLD_RETURNED:
            conn.execute(
                "UPDATE held_offers SET state = ?, updated = ? WHERE queue = ? AND item_id = ?",
                (HOLD_RETURNED, timestamp(), declared, item_id),
            )
    return _hold_of(_held_row(store, declared, item_id))
