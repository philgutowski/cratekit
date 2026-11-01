"""The folder that holds All Favorites, put in order newest first (U180).

Until U180 a month playlist was made at the end of the folder, so the folder
read oldest first and every new month landed at the bottom. The author asked
on 2026-10-28 for the opposite: All Favorites on top, then the months newest
first, then ``Undated``. ``crate favorites order`` asks once; this module plans
and writes. From then on a month is made in its own slot, by
:func:`placement.month_row`, so the folder stays in order without the verb.

**THE ORDER IS ONE RULE**, :func:`placement.rank`: All Favorites, by its row;
each live plain playlist named as a month, newest first; a live plain playlist
named ``Undated``; then everything else the folder holds, a quarter, a folder,
a smart list or any other name, in its current relative order. A playlist
whose name is not a month is never moved between the months, and a soft
deleted child is never read, ranked or written.

**POSITIONS ARE SLOTS, NOT A COUNT.** The write gives the ``Seq`` values the
live children hold now, sorted, out again in the target order, through
:func:`placement.seat`. It does not use the binding's ``move_playlist(seq=)``,
which counts live and removed rows together as one run from 1 and shifts the
removed ones with it: how the live library numbers removed siblings was never
measured, and this rule does not need to know. Only a row whose ``Seq``
changes is written.

**POSITIONS AND NOTHING ELSE.** No membership, no content row, no name, no
parent, no removal. The commit is confined from SQL before it lands by
:func:`assert_order_confined`, and the folder is read back in order before
the session closes.

**THE DIGEST IS THE TARGET ORDER**, the home's rows and the children's rows in
the order they will read, so it moves when the target moves and not otherwise.
A folder shuffled by hand between the approval and the write still writes the
order that was approved; a month made or removed in between is another plan.

Layer: modules.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Mapping

from cratekit.cli.output import digest_of
from cratekit.core import config, convergence, rb_writer, session, snapshot, tree_registry
from cratekit.core.cause import Remedy, refuse
from cratekit.favorites import placement
from cratekit.write import trees

#: The session workflow the order is recorded under, and its plan's kind.
WORKFLOW = "favorites-order"

#: What a seated row may change on its own playlist row: its position and the
#: bookkeeping stamped beside it. Nothing else changes on any row.
_SEATED_COLUMNS = frozenset({"Seq", "updated_at", "usn", "rb_local_usn"})

#: A child's place in the rule, by the first element of its rank.
KINDS = {0: "source", 1: "month", 2: "undated", 3: "other"}

_ORIGIN = ("favorites", "order")


# ---------------------------------------------------------------------------
# The plan
# ---------------------------------------------------------------------------


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


def _kind(rank: tuple[int, int]) -> str:
    return KINDS[rank[0]]


def plan(db: Any, *, source: str) -> OrderPlan:
    """The folder's order against the rule, planned on this handle.

    REFUSED, BY NAME, AS :func:`placement.resolve_home` REFUSES: no live All
    Favorites or two of them, and an All Favorites at the playlist root, which
    has no folder of its own to order. The root is every playlist's, and its
    order is not this verb's.
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
            kind=_kind(placement.rank(row, home.source_id)),
            seq=placement.seq_of(row),
            slot=slot,
            at=at[str(row.ID)],
            to=n,
        )
        for n, (row, slot) in enumerate(zip(ranked, placement.slots(ranked)), start=1)
    )
    planned = OrderPlan(home=home, children=children)
    return replace(planned, digest=digest_of(planned.identity()))


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
    count = {kind: 0 for kind in KINDS.values()}
    for one in planned.children:
        count[one.kind] += 1
    return {
        "digest": planned.digest,
        "items": items,
        "totals": {
            "count": len(items),
            "moves": len(planned.moves),
            "months": count["month"],
            "undated": count["undated"],
            "others": count["other"],
        },
        "chunk": None,
    }


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


# ---------------------------------------------------------------------------
# The confinement, from SQL
# ---------------------------------------------------------------------------


def order_violations(
    before: rb_writer.NodeTables,
    after: rb_writer.NodeTables,
    *,
    folder_id: str,
    seated: Mapping[str, int],
) -> list[str]:
    """Every difference between two readings that the planned order does not explain.

    ``seated`` maps each row the write moves to the ``Seq`` it takes. Empty
    means the order was confined, AND that it was made.

    PURE, as :func:`rb_writer.node_change_violations` is, so every branch is
    reachable with literal readings. What it explains, and nothing more:

    * no content row differs, is added or disappears;
    * no membership row differs, is added or disappears;
    * no playlist row is added or disappears;
    * a seated row is live under the folder at its planned ``Seq``, ASKED
      WHETHER IT CHANGED OR NOT, so a planned move that never happened is
      refused here, and it changed its position and bookkeeping only;
    * every other playlist row is exactly as it was.
    """
    violations: list[str] = []
    planned = {str(key): int(value) for key, value in seated.items()}
    if before.content != after.content:
        violations.append(
            f"a {rb_writer.CONTENT_TABLE} row changed, and an order touches no track"
        )

    p_cols = before.playlist_columns
    marker_at = p_cols.index(rb_writer.SOFT_DELETE_COLUMN)
    parent_at = p_cols.index("ParentID")
    seq_at = p_cols.index("Seq")
    for key in sorted(set(before.playlists) - set(after.playlists)):
        violations.append(f"the {rb_writer.PLAYLIST_TABLE} row {key!r} disappeared")
    for key in sorted(set(after.playlists) - set(before.playlists)):
        violations.append(f"an unplanned {rb_writer.PLAYLIST_TABLE} row {key!r} was added")
    for key, slot in sorted(planned.items()):
        row = after.playlists.get(key)
        if (
            row is None
            or str(row[parent_at]) != str(folder_id)
            or row[marker_at]
            or int(row[seq_at] or 0) != slot
        ):
            violations.append(
                f"the {rb_writer.PLAYLIST_TABLE} row {key!r} is not live under the folder "
                f"{folder_id!r} at the planned position {slot}"
            )
    for key in sorted(set(before.playlists) & set(after.playlists)):
        changed = {
            name
            for name, old, new in zip(p_cols, before.playlists[key], after.playlists[key])
            if old != new
        }
        allowed = _SEATED_COLUMNS if key in planned else frozenset()
        if changed - allowed:
            violations.append(
                f"the {rb_writer.PLAYLIST_TABLE} row {key!r} changed "
                f"{sorted(changed - allowed)}, which the planned order does not explain"
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


def assert_order_confined(
    db: Any,
    before: rb_writer.NodeTables,
    *,
    folder_id: str,
    seated: Mapping[str, int],
) -> None:
    """Refuse, before the commit, an order that reached anything it did not plan, read from SQL.

    The pending work is flushed DELIBERATELY, inside the transaction, so the
    second reading sees it and a refusal still rolls back, as
    :func:`rb_writer.assert_node_changes_confined` does for the same reason.
    """
    db.session.flush()
    violations = order_violations(
        before, rb_writer.node_tables(db), folder_id=folder_id, seated=seated
    )
    if violations:
        db.rollback()
        raise refuse(
            "whitelist-violation",
            "the order reached rows it did not plan, or did not make a move it "
            "planned, read from SQL before the commit, so nothing was written:\n  - "
            + "\n  - ".join(violations),
            origin=_ORIGIN,
            detail={"violations": violations},
        )


# ---------------------------------------------------------------------------
# The write
# ---------------------------------------------------------------------------


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
    if moved <= 0:
        return
    session.record_commit(
        record,
        placement.RECORD_KEY,
        session.ChangeSummary(
            (session.TreeChange(tree=placement.RECORD_KEY, created=0, updated=moved),)
        ),
        cfg,
    )


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
    refuses, since the approved one was read on a handle that has since
    closed. THE SESSION SPINE IS CALLED, NOT REBUILT, as the split calls it:
    the gates with a record kept, one capture verified before anything is
    written, the analysis watch over the roots named, a commit witness, the
    commit confined from SQL by :func:`assert_order_confined`, and the
    guarded commit. The folder is read back in order before the session
    closes.
    """
    watched = [Path(root) for root in analysis_roots]
    if not watched:
        raise ValueError(
            "analysis_roots is empty, so the analysis-file watch would watch nothing "
            "and this session would report itself clean whatever happened to the "
            "library's grids; name the roots this write could touch"
        )
    again = plan(db, source=source)
    if again.digest != approved.digest:
        raise refuse(
            "decision-stale",
            "the Favorites folder is not as the approved plan read it, so nothing was "
            "written; run it again and approve what it shows now",
            origin=_ORIGIN,
            detail={"approved": approved.digest, "now": again.digest},
        )
    planned = again
    folder_id = planned.home.folder_id
    # THE OUT OF BAND RESTORE IS DETECTED BEFORE THE FINGERPRINT IS TOUCHED,
    # as the split does: the Favorites folder is no tree, so the detection
    # marks and never refuses here.
    convergence.detect_out_of_band_restore(cfg, db, tree_registry.read(cfg))

    moved: tuple[str, ...] = ()
    with session.assert_gates(
        cfg, workflow=WORKFLOW, analysis_roots=watched, keep=session.Keep.RECORD
    ) as gates:
        record = gates.record
        capture = snapshot.capture(cfg, db=db)
        session.attach_capture(record, capture.root, cfg)
        snapshot.assert_verified(capture)

        with rb_writer.commit_witness(db) as witness:
            try:
                before = rb_writer.node_tables(db)
                rows = [db.get_playlist(ID=one.row) for one in planned.children]
                moved = placement.seat(db, rows, when=datetime.now())
                assert_order_confined(
                    db,
                    before,
                    folder_id=folder_id,
                    seated={one.row: one.slot for one in planned.moves},
                )
                if moved:
                    rb_writer.commit_guarded(db)
            except BaseException:
                trees._rollback_quietly(db)
                if witness.landed:
                    _record_order_commit(record, moved=len(moved), cfg=cfg)
                raise
        _record_order_commit(record, moved=len(moved), cfg=cfg)
        if moved:
            convergence.record_fingerprint(cfg, db)
        disagreements = _read_back(db, planned)
        order = tuple(
            str(getattr(row, "Name", "") or "") for row in placement.children(db, folder_id)
        )
        session_id = record.session_id
    names = {one.row: one.name for one in planned.children}
    return Ordered(
        moved=tuple(names[row] for row in moved),
        order=order,
        session_id=session_id,
        disagreements=disagreements,
    )


def assert_read_back(done: Ordered) -> None:
    """Refuse an answer the database does not hold."""
    if done.disagreements:
        raise refuse(
            "session-committed-unverified",
            "the Favorites folder read back from the database is not in the planned "
            "order: " + "; ".join(done.disagreements) + "; the commit landed and this "
            "answer cannot be vouched for",
            origin=_ORIGIN,
            detail={"disagreements": list(done.disagreements), "session": done.session_id},
        )


__all__ = [
    "Child",
    "KINDS",
    "OrderPlan",
    "Ordered",
    "WORKFLOW",
    "apply",
    "assert_order_confined",
    "assert_read_back",
    "facts",
    "order_violations",
    "payload",
    "plan",
]
