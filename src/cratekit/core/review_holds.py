"""Held offers: what a producer withheld from a review queue, and can return (R-798, R-815).

Split from ``core.review`` to keep each module readable; every name here is
imported back into ``core.review`` and used from there, and only
``core.review`` imports this module, at its foot.
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
    item_id_for,
    normalize_identity,
    normalize_kind,
)

# ---------------------------------------------------------------------------
# Held offers: what a producer withheld from a queue, and can be returned
# ---------------------------------------------------------------------------

#: A hold in force. The producer judges it again on every round that reaches it.
HOLD_HELD = "held"
#: A hold a person returned to the queue. Kept, so nothing holds it a second time.
HOLD_RETURNED = "returned"
HOLD_STATES: tuple[str, ...] = (HOLD_HELD, HOLD_RETURNED)


@dataclass(frozen=True, slots=True)
class Hold:
    """One candidate a producer withheld from a queue, with what it would have filed.

    ``item_id`` is the identifier the candidate would carry as an item, so a
    hold and the item it becomes are addressed by one value. ``reason`` is the
    sentence a person reads and ``detail`` is what the producer judged on, kept
    so it can judge again without asking anybody.
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
    def decoded(text: str) -> dict[str, Any]:
        # A COLUMN THIS BUILD CANNOT READ IS AN EMPTY MAP, NEVER A CRASH. The
        # row still names the release and says it is held, which is what a
        # listing needs, and a producer that finds no recorded words judges
        # nothing from it rather than releasing the hold.
        try:
            found = json.loads(text)
        except ValueError:
            return {}
        return found if isinstance(found, dict) else {}

    return Hold(
        queue=row["queue"],
        item_id=row["item_id"],
        kind=row["kind"],
        identity=decoded(row["identity"]),
        payload=decoded(row["payload"]),
        group=row["group_key"],
        name=row["group_name"],
        reason=row["reason"],
        detail=decoded(row["detail"]),
        state=row["state"],
        run_id=row["run_id"],
        created=row["created"],
        updated=row["updated"],
    )


def _held_row(store: ReviewStore, queue: str, item_id: str) -> sqlite3.Row | None:
    return store.conn.execute(
        "SELECT * FROM held_offers WHERE queue = ? AND item_id = ?", (queue, item_id)
    ).fetchone()


#: The payload field a hold carries when its candidate was TAKEN BACK OUT OF THE
#: QUEUE by :func:`withhold`, where a hold a producer made on a candidate it
#: never filed carries none (R-815). The difference matters to whoever would
#: drop a hold: a candidate never filed goes back to being unexamined, and one
#: that was in front of a person must not vanish from both places.
WITHHELD_FIELD = "withheld_from_review"

#: The payload fields a refresh carries over from the hold it replaces, when
#: the new payload does not name them. Both are facts about the candidate's
#: history that the producer refreshing a hold does not know: it describes
#: every hold as a candidate it never filed.
_CARRIED_ACROSS_A_REFRESH: tuple[str, ...] = (RUN_FIELD, WITHHELD_FIELD)


def _put_hold(
    store: ReviewStore,
    conn: sqlite3.Connection,
    *,
    queue: str,
    item_id: str,
    kind: str,
    identity: str,
    payload: Mapping[str, Any],
    group: str,
    name: str,
    reason: str,
    detail: Mapping[str, Any],
    run_id: str,
    state: str,
) -> None:
    """Write one hold row inside the caller's transaction. THE ONE WRITER.

    :func:`hold` and :func:`withhold` both make a hold, and two spellings of
    one row are how the two come to disagree about a column.

    No row yet: it is inserted in ``state``. A hold IN FORCE is refreshed: what
    the producer knows now replaces the payload, the reason and what it judged
    on, and the run and the time it was first made are kept. A hold a person
    RETURNED is left exactly as it is.
    """
    now = timestamp()
    encoded_detail = json.dumps(dict(detail), sort_keys=True)
    row = _held_row(store, queue, item_id)
    if row is None:
        conn.execute(
            "INSERT INTO held_offers (queue, item_id, kind, identity, payload, "
            "group_key, group_name, reason, detail, state, run_id, created, updated) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                queue,
                item_id,
                kind,
                identity,
                json.dumps(dict(payload), sort_keys=True),
                group,
                name,
                reason,
                encoded_detail,
                state,
                run_id,
                now,
                now,
            ),
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
            (
                json.dumps(refreshed, sort_keys=True),
                group,
                name,
                reason,
                encoded_detail,
                now,
                queue,
                item_id,
            ),
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

    ``returned`` RECORDS A PERSON'S ANSWER WHERE NO HOLD EXISTS YET: the row is
    made already returned, in one write, for a candidate that is in the queue
    and that a later judgment must not hold. It changes nothing about a row
    that is already there.

    A HOLD A PERSON RETURNED IS NEVER HELD AGAIN. Its row is handed back as it
    stands, state and all, so the producer that asked can see its hold did not
    take. Returning is the person overruling the producer, and a later round
    that overruled them back would undo an answer nobody asked it to revisit.

    THE FIRST ROUND STAYS THE HOLDING ROUND. A refresh rewrites what the
    producer knows now, the payload, the reason and what it judged on, and
    keeps the run and the time the hold was first made, so a count of what one
    round held does not move when a later round looks at the same release.

    A REFRESH KEEPS WHAT THE REPLACED PAYLOAD SAID OF THE CANDIDATE'S HISTORY,
    when the new payload does not say it (R-815): the run it was filed under,
    and that it was taken back out of the queue. A candidate :func:`withhold`
    took back carries both, and the producer that refreshes its hold describes
    it as a candidate never filed. Dropped, a return would file it under the
    round that held it, which filed nothing, and nothing could tell it from a
    candidate no person was ever shown.
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

    R-815. A producer that judges a candidate ALREADY FILED, and finds it would
    not have filed it, takes it back: the item's row is deleted and a hold is
    written carrying what the item carried, so returning it files the same
    thing. Not a verdict. A superseded item would still be an item, and the
    producer that reads "is there an item" to decide whether a candidate was
    offered would read this one as offered and drop its hold.

    ONE TRANSACTION, BOTH WRITES. A hold written beside an item still in the
    queue is a candidate a person can decide while a listing says it is held,
    and an item deleted with no hold written is a candidate nothing offers and
    nothing holds.

    ONLY OVER AN EMPTY VERDICT COLUMN, on the rule :func:`supersede` states. An
    accepted, a rejected and a superseded item stand, and so does one carrying
    a verdict this build cannot read: on a queue two builds share, that is a
    decision somebody made. The check is inside the transaction, so an item a
    person decides while a producer is judging it is theirs.

    A HOLD A PERSON RETURNED IS NEVER HELD AGAIN, the rule :func:`hold` keeps.
    The item stays where it is and None is the answer.

    None for an identifier nothing answers to, too. Each None means the same
    thing to a caller: nothing was moved.

    THE HOLD SAYS IT WAS TAKEN BACK, under :data:`WITHHELD_FIELD` on its
    payload, and a refresh keeps the word. A hold beside an open item, the
    state two writes of an earlier build can leave, is refreshed and keeps the
    run that first held it.

    AN ITEM THAT ARRIVED BY IMPORT CARRIES NO IDENTITY, and its hold then
    carries an empty one. The hold is still found by the item's identifier,
    which is all a return asks, and its payload still names the candidate.
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
        # THE FLOOR BEFORE THE DELETE, so the ordinal this row held is never
        # handed to a later item. See ``ordinal_floor`` in the schema.
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
    """Every hold on ``queue`` in one of ``states``, oldest first.

    ``group`` narrows it to one group's, a label's for the label-release queue.
    """
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

    True when a row was dropped. A returned hold is kept: it is the record that
    a person overruled the producer, and the only thing that stops a later
    round, or a later verb reading the same judgment, from holding it again.
    """
    with store.immediate() as conn:
        dropped = conn.execute(
            "DELETE FROM held_offers WHERE queue = ? AND item_id = ? AND state = ?",
            (_assert_declared_queue(queue), item_id, HOLD_HELD),
        )
        return dropped.rowcount > 0


def return_hold(store: ReviewStore, *, queue: str, item_id: str) -> Hold | None:
    """Mark a hold returned by a person, and hand it back, or None for no such hold.

    THE MARK ONLY. Filing the candidate is the caller's, through :func:`offer`
    and the producer's own key, and it comes FIRST: a hold marked returned whose
    item was never filed would be a release nothing holds and nothing offers.
    A hold already returned is handed back unchanged, so a second ask is the
    same answer.
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
