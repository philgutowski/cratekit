"""The folder that holds All Favorites, put in order newest first (U180).

``crate favorites order`` asks once; a month is made in its own slot since.
**THE ORDER IS ONE RULE**, :func:`placement.rank`: All Favorites, the months
newest first, ``Undated``, then the rest in their relative order; a soft
deleted child is never read or written. **POSITIONS ARE SLOTS**: the ``Seq``
values the live children hold are given out again in the target order, never
the binding's ``move_playlist(seq=)``, and only a row whose ``Seq`` changes is
written, confined from SQL and read back. **THE DIGEST IS THE TARGET ORDER**.

Layer: modules.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Mapping

from cratekit.core import config, convergence, rb_writer, session
from cratekit.core.cause import Remedy, refuse
from cratekit.favorites import placeholders, placement, spine
from cratekit.write import trees

#: The session workflow the order is recorded under, and its plan's kind.
WORKFLOW = "favorites-order"

#: A child's place in the rule, by the first element of its rank.
KINDS = {
    placeholders.RANK_SOURCE: "source",
    placeholders.RANK_MONTH: "month",
    placeholders.RANK_UNDATED: "undated",
    placeholders.RANK_OTHER: "other",
}

_ORIGIN = ("favorites", "order")


@dataclass(frozen=True, slots=True)
class Child:
    """One live child of the folder: where it reads now and where it will read."""

    row: str
    name: str
    kind: str
    #: Its ``Seq`` now, and the ``Seq`` it takes.
    seq: int
    slot: int
    #: Its position among the live children, from 1, now and after.
    at: int
    to: int

    @property
    def moves(self) -> bool:
        """Whether the write touches this row, which is whether its ``Seq`` changes."""
        return self.seq != self.slot


@dataclass(frozen=True, slots=True)
class OrderPlan:
    """The folder's live children in the order they will read, and what moves."""

    home: placement.Home
    #: In the target order.
    children: tuple[Child, ...]
    digest: str = ""

    @property
    def moves(self) -> tuple[Child, ...]:
        return tuple(one for one in self.children if one.moves)

    @property
    def writes(self) -> bool:
        return bool(self.moves)

    @property
    def now(self) -> tuple[Child, ...]:
        """The children in the order they read now."""
        return tuple(sorted(self.children, key=lambda one: one.at))

    def identity(self) -> dict[str, Any]:
        """What the digest covers: the home's rows and the target order, never where a row reads now."""
        return {
            "kind": WORKFLOW,
            **self.home.identity(),
            "order": [one.row for one in self.children],
        }


def plan(db: Any, *, source: str) -> OrderPlan:
    """The folder's order against the rule, planned on this handle.

    REFUSED BY NAME as :func:`placement.resolve_home` refuses, and for an All
    Favorites at the playlist root, whose order is every playlist's.
    """
    home = placement.resolve_home(db, source)
    if not home.folder_id:
        raise refuse(
            placement.SOURCE_MISSING,
            f"{source!r} sits at the playlist root rather than in a Favorites folder, so "
            f"there is no folder of the favourites to put in order and nothing was "
            f"written; put {source!r} in a folder in rekordbox and run it again",
            remedy=Remedy.FIX_CONFIG_VALUES,
            origin=_ORIGIN,
            detail={"playlist": source, "row": home.source_id, "folder": None},
        )
    here = placement.children(db, home.folder_id)
    ranked = sorted(here, key=lambda row: placement.rank(row, home.source_id))
    at = {str(row.ID): n for n, row in enumerate(here, start=1)}
    children = tuple(
        Child(
            row=str(row.ID),
            name=str(getattr(row, "Name", "") or ""),
            kind=KINDS[placement.rank(row, home.source_id)[0]],
            seq=placement.seq_of(row),
            slot=slot,
            at=at[str(row.ID)],
            to=n,
        )
        for n, (row, slot) in enumerate(zip(ranked, placement.slots(ranked)), start=1)
    )
    return spine.digested(OrderPlan(home=home, children=children))


def payload(planned: OrderPlan) -> dict[str, Any]:
    """The plan as the gate shows it: one item per child, its position now and after."""
    items = [
        {
            "action": "move" if one.moves else "stay",
            "playlist": one.name,
            "row": one.row,
            "kind": one.kind,
            "from": one.at,
            "to": one.to,
        }
        for one in planned.children
    ]
    count = Counter(one.kind for one in planned.children)
    return spine.shown(planned, items, {
        "count": len(items),
        "moves": len(planned.moves),
        "months": count["month"],
        "undated": count["undated"],
        "others": count["other"],
    })


def facts(planned: OrderPlan) -> dict[str, Any]:
    """The facts beside the items on the gate screen, one line per fact."""
    home = planned.home
    return {
        "folder": f"{home.folder_name!r} (row {home.folder_id}), holding "
        f"{home.source_name!r} (row {home.source_id})",
        "order now": [one.name for one in planned.now],
        "order after": [one.name for one in planned.children],
        "playlists to move": len(planned.moves),
    }


def order_violations(
    before: rb_writer.NodeTables,
    after: rb_writer.NodeTables,
    *,
    folder_id: str,
    seated: Mapping[str, int],
) -> list[str]:
    """Every difference between two readings that the planned order does not explain.

    ``seated`` maps each row the write moves to the ``Seq`` it takes. PURE. No
    content, membership or playlist row is added, removed or changed but a
    seated row, which is live under the folder at its planned ``Seq``, ASKED
    WHETHER IT CHANGED OR NOT so a move that never happened is refused, and
    changed its position and bookkeeping only.
    """
    planned = {str(key): int(value) for key, value in seated.items()}
    p_cols = before.playlist_columns
    marker_at = p_cols.index(rb_writer.SOFT_DELETE_COLUMN)
    parent_at = p_cols.index("ParentID")
    seq_at = p_cols.index("Seq")
    unseated = [
        f"the {rb_writer.PLAYLIST_TABLE} row {key!r} is not live under the folder "
        f"{folder_id!r} at the planned position {slot}"
        for key, slot in sorted(planned.items())
        if (row := after.playlists.get(key)) is None
        or str(row[parent_at]) != str(folder_id)
        or row[marker_at]
        or int(row[seq_at] or 0) != slot
    ]
    violations = spine.drift(
        before,
        after,
        touches="an order",
        made=(),
        written=unseated,
        moves=lambda key: key in planned,
        explains="the planned order does not explain",
    )
    for key in sorted(set(before.memberships) ^ set(after.memberships)):
        violations.append(f"the {rb_writer.MEMBERSHIP_TABLE} row {key!r} was added or disappeared")
    for key in sorted(set(before.memberships) & set(after.memberships)):
        if before.memberships[key] != after.memberships[key]:
            violations.append(
                f"the {rb_writer.MEMBERSHIP_TABLE} row {key!r} changed, and an order "
                f"changes no membership"
            )
    return violations


@dataclass(frozen=True, slots=True)
class Ordered:
    """What one order wrote, and the folder read back after its commit."""

    #: The names of the rows whose position was written, in the target order.
    moved: tuple[str, ...]
    #: The folder's live children by name, read back in the order they read.
    order: tuple[str, ...]
    session_id: str
    disagreements: tuple[str, ...] = ()


def _record_order_commit(record: session.SessionRecord, *, moved: int, cfg: config.Config) -> None:
    """Record the commit on the session, as rows changed under the favourites key."""
    if moved > 0:
        session.record_commit(record, placement.RECORD_KEY, spine.change(0, moved), cfg)


def _read_back(db: Any, planned: OrderPlan) -> tuple[str, ...]:
    """What the folder reads that the plan did not, read on this handle after the commit."""
    found = [str(row.ID) for row in placement.children(db, planned.home.folder_id)]
    wanted = [one.row for one in planned.children]
    if found == wanted:
        return ()
    names = {one.row: one.name for one in planned.children}
    return (
        "the folder reads "
        + ", ".join(names.get(row, f"row {row}") for row in found)
        + " and the plan was "
        + ", ".join(one.name for one in planned.children),
    )


def apply(
    cfg: config.Config,
    db: Any,
    approved: OrderPlan,
    *,
    source: str,
    analysis_roots: Iterable[Path | str],
) -> Ordered:
    """Seat every child of the folder in the approved order, in one commit, and read it back.

    THE PLAN IS TAKEN AGAIN ON THIS HANDLE FIRST and a digest that moved
    refuses; the commit is confined from SQL by :func:`order_violations`.
    """
    watched, planned = spine.prepared(
        cfg, db, analysis_roots, lambda: plan(db, source=source), approved,
        "the Favorites folder is not as the approved plan read it, so nothing was written",
        _ORIGIN,
    )
    folder_id = planned.home.folder_id
    moved: tuple[str, ...] = ()
    with session.assert_gates(
        cfg, workflow=WORKFLOW, analysis_roots=watched, keep=session.Keep.RECORD
    ) as gates:
        record, capture = trees.attached_capture(gates, cfg, db)
        with spine.witnessed(db, lambda: _record_order_commit(record, moved=len(moved), cfg=cfg)):
            before = rb_writer.node_tables(db)
            rows = [db.get_playlist(ID=one.row) for one in planned.children]
            moved = placement.seat(db, rows, when=datetime.now())
            seated = {one.row: one.slot for one in planned.moves}
            spine.confined(
                db,
                lambda after: order_violations(before, after, folder_id=folder_id, seated=seated),
                "the order reached rows it did not plan, or did not make a move it planned",
                _ORIGIN,
            )
            if moved:
                rb_writer.commit_guarded(db)
        if moved:
            convergence.record_fingerprint(cfg, db)
        disagreements = _read_back(db, planned)
        order = tuple(
            str(getattr(row, "Name", "") or "") for row in placement.children(db, folder_id)
        )
        return Ordered(
            moved=tuple(one.name for one in planned.children if one.row in moved),
            order=order,
            session_id=record.session_id,
            disagreements=disagreements,
        )


def assert_read_back(done: Ordered) -> None:
    """Refuse an answer the database does not hold."""
    spine.verified(
        done,
        "the Favorites folder read back from the database is not in the planned order",
        _ORIGIN,
    )


__all__ = [
    "Child",
    "KINDS",
    "OrderPlan",
    "Ordered",
    "WORKFLOW",
    "apply",
    "assert_read_back",
    "facts",
    "order_violations",
    "payload",
    "plan",
]
