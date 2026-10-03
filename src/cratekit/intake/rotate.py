"""Rotate INBOX: a stale batch moves into Old, an expired one in Old is removed (U111).

INBOX is a listening queue, and every landing adds one batch playlist to it, so
it only ever grows. The source system's ``dj-inbox-rotation`` reported which
lists to drag and left the dragging to a person, and ``report intake-aging``
copies that report. This is the rotation as a write, on a library whose intake
tree is database native:

* a batch playlist directly under INBOX older than ``reports.intake_stale_days``
  moves into the folder ``[intake_old]`` declares, ``INBOX / Old``;
* a batch playlist directly under Old older than ``reports.intake_expired_days``
  is removed.

TRACKS ARE NEVER REMOVED. A move changes the playlist node's parent and its
position and nothing it holds. A removal soft deletes the node and its own
memberships, the way rekordbox removes a playlist, so every track stays in the
collection and in every other playlist it sits in, its BY GENRE + ENERGY places
included. Both are asserted from SQL before the commit, row by row, through
:func:`cratekit.core.rb_writer.assert_node_changes_confined`.

WHAT A BATCH IS, decided here and nowhere else. A playlist directly under INBOX
or Old is a batch when ANY of these holds, and the plan says which:

==============================  ===============================================
``run record``                  a native landing's session record names this
                                playlist by identifier (``native.BATCH_PLAYLIST_KEY``)
``_inboxed suffix``             the name ends ``_inboxed``, a batch named for
                                its run before U110
``dated name``                  the name is U110's ``2026-10-03 Tidal playlists``
                                shape AND a batch folder of exactly that name
                                sits under the music folder, which both media
                                make for every landing
==============================  ===============================================

EVERYTHING ELSE IS LEFT ALONE AND LISTED: a folder, a smart playlist, and an
ordinary playlist no rule recognises. A dated name with no batch folder is a
playlist somebody named that way, and the folder test is what keeps it out.

A BATCH'S AGE is its landing date from the run record when one names it, else
the playlist row's own ``created_at``, which for a batch rekordbox imported from
an intake file is the day it was imported. Each batch says which it was aged
from. A batch with neither, or dated after the day the rotation is run for, is
left alone rather than guessed at.

A BATCH PAST EXPIRY THAT IS STILL IN INBOX MOVES, it is not removed. Removal is
the second stage and happens only in Old, so a batch is always seen in Old by
at least one plan before one removes it. The cost is that the run after such a
move removes it, recorded as a residual.

Layer: modules. It opens no database of its own: the verb hands it a handle.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, replace
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping

from cratekit.cli.output import digest_of
from cratekit.core import (
    config,
    convergence,
    rb_writer,
    session,
    snapshot,
    taxonomy,
    tree_registry,
)
from cratekit.core.cause import Remedy, refuse
from cratekit.intake import landing, native
from cratekit.write import trees

#: The session workflow a rotation is recorded under.
WORKFLOW = "inbox-rotate"

#: What a planned batch will do, and the band of one that stays.
MOVE = "move"
REMOVE = "remove"
KEEP = "keep"

#: How a playlist was recognised as a batch.
BY_RECORD = "run record"
BY_SUFFIX = "_inboxed suffix"
BY_NAME = "dated name"

#: What a batch's age was read from.
AGED_FROM_RECORD = "run record"
AGED_FROM_CREATED = "playlist created"

#: The suffix a batch named for its run carried before U110.
INBOXED_SUFFIX = "_inboxed"

#: U110's default batch name: an ISO date, one space, then the source words.
_DATED_NAME = re.compile(r"^\d{4}-\d{2}-\d{2} \S")

#: The tables the rotation's one commit admits a removal in, and only it.
REMOVALS: tuple[str, ...] = (rb_writer.PLAYLIST_TABLE, rb_writer.MEMBERSHIP_TABLE)

_ORIGIN = ("intake.rotate",)


@dataclass(frozen=True, slots=True)
class Batch:
    """One batch playlist, where it sits, how old it is, and what happens to it."""

    playlist_id: str
    name: str
    #: The taxonomy id of the node it sits under, the intake's or Old's.
    place: str
    recognised_by: str
    landed: date
    aged_from: str
    age_days: int
    tracks: int
    action: str

    def to_json(self) -> dict[str, Any]:
        return {
            "action": self.action,
            "id": self.playlist_id,
            "playlist": self.name,
            "in": self.place,
            "recognised by": self.recognised_by,
            "landed": self.landed.isoformat(),
            "aged from": self.aged_from,
            "age_days": self.age_days,
            "tracks": self.tracks,
        }


@dataclass(frozen=True, slots=True)
class Left:
    """One node under INBOX or Old the rotation does not touch, and why."""

    playlist_id: str
    name: str
    place: str
    kind: str
    reason: str

    def to_json(self) -> dict[str, Any]:
        return {
            "id": self.playlist_id,
            "playlist": self.name,
            "in": self.place,
            "kind": self.kind,
            "reason": self.reason,
        }


@dataclass(frozen=True, slots=True)
class RotationPlan:
    """Everything the rotation would write, what it keeps, and what it leaves alone."""

    tree_id: str
    root_id: str
    root_name: str
    old_place: str
    old_display: str
    #: The live Old folder's identifier, or None when the write would create it.
    old_id: str | None
    as_of: date
    stale_days: int
    expired_days: int
    moves: tuple[Batch, ...]
    removals: tuple[Batch, ...]
    kept: tuple[Batch, ...]
    left: tuple[Left, ...]
    #: Session records that could not be read, so their batches aged from the row.
    unreadable_records: int
    digest: str

    @property
    def writes(self) -> bool:
        return bool(self.moves or self.removals)

    @property
    def creates_old(self) -> bool:
        return bool(self.moves) and self.old_id is None


@dataclass(frozen=True, slots=True)
class Rotated:
    """What the commit landed, read back from SQL after it."""

    moved: tuple[str, ...]
    removed: tuple[str, ...]
    old_id: str
    old_created: bool
    memberships_removed: int
    session_id: str
    #: Every way the read back disagrees with the plan. Empty when it agrees.
    disagreements: tuple[str, ...]


def identity(plan: RotationPlan) -> dict[str, Any]:
    """What the digest covers: every fact the screen shows and the write acts on."""
    return {
        "kind": "inbox-rotate",
        "tree": plan.tree_id,
        "root": plan.root_id,
        "old": {"id": plan.old_id, "display": plan.old_display},
        "as_of": plan.as_of.isoformat(),
        "stale_days": plan.stale_days,
        "expired_days": plan.expired_days,
        "moves": [batch.to_json() for batch in plan.moves],
        "removals": [batch.to_json() for batch in plan.removals],
        "kept": [batch.to_json() for batch in plan.kept],
        "left": [node.to_json() for node in plan.left],
    }


# ---------------------------------------------------------------------------
# Reading
# ---------------------------------------------------------------------------


def old_node(declared: taxonomy.Taxonomy) -> taxonomy.Node:
    """The declared Old folder, or the refusal that says to declare it."""
    if declared.intake_old is None:
        raise refuse(
            "intake-old-undeclared",
            "this library's taxonomy declares no [intake_old] folder, so there is "
            "nowhere to rotate a stale batch into; the folder is declared beside "
            "the intake flow and this verb will not invent one",
            remedy=Remedy.FIX_CONFIG_VALUES,
            steps=(
                "add an [intake_old] section with an id and a display to the "
                "library's active taxonomy, as the shipped template carries",
            ),
            origin=_ORIGIN,
            detail={"intake": declared.intake.id},
        )
    return declared.intake_old


def anchored_root(db: Any, tree_id: str, registry: tree_registry.Registry) -> str:
    """The intake tree's adopted root, or the refusal that names ``tree cutover``."""
    try:
        return tree_registry.anchored_root(
            tree_id, registry, root_exists=lambda root_id: db.get_playlist(ID=root_id) is not None
        )
    except tree_registry.TreeModeRefused as exc:
        if exc.cause.reason != "tree-unconverged" or exc.mode != tree_registry.Mode.XML:
            raise
        raise refuse(
            "tree-unconverged",
            f"the intake tree {tree_id!r} is still on the xml bridge, so its batches "
            f"are not this product's to move in the database; cut the intake tree "
            f"over first, nothing was read or written",
            remedy=Remedy.COMPLETE_PENDING_ACTION,
            steps=(
                f"run crate tree cutover {tree_id} --export with a Fresh Export to "
                f"move the intake tree to the database",
            ),
            origin=_ORIGIN,
            detail={"tree_id": tree_id, "mode": str(exc.mode)},
            inner=exc.cause,
        ) from exc


def _local_date(stamp: str) -> date | None:
    try:
        moment = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    if moment.tzinfo is not None:
        moment = moment.astimezone()
    return moment.date()


def landing_dates(cfg: config.Config) -> tuple[dict[str, date], int]:
    """Each batch playlist a native landing recorded, and the day it first landed.

    Answers the mapping and how many records could not be read. A record that
    names a playlist and committed nothing landed nothing, so it dates nothing.
    The EARLIEST landing wins: a batch is as old as its first tracks.
    """
    records, unreadable = session.scan_log(cfg)
    found: dict[str, date] = {}
    for record in records:
        if record.workflow != native.WORKFLOW:
            continue
        named = record.detail.get(native.BATCH_PLAYLIST_KEY)
        if not isinstance(named, Mapping) or not named.get("id"):
            continue
        if str(session.SourceState.COMMITTED) not in {str(v) for v in record.sources.values()}:
            continue
        landed = _local_date(record.started)
        if landed is None:
            continue
        key = str(named["id"])
        if key not in found or landed < found[key]:
            found[key] = landed
    return found, len(unreadable)


def _live_children(db: Any, parent_id: str) -> list[Any]:
    return [
        row
        for row in list(db.get_playlist(ParentID=str(parent_id)))
        if not rb_writer.node_removed(row)
    ]


def _track_count(db: Any, playlist: Any) -> int:
    return sum(
        1
        for song in db.get_playlist_songs(PlaylistID=str(playlist.ID))
        if not rb_writer.membership_removed(song)
    )


def _recognised(cfg: config.Config, row: Any, recorded: Mapping[str, date]) -> str | None:
    name = str(getattr(row, "Name", "") or "")
    if str(row.ID) in recorded:
        return BY_RECORD
    if name.endswith(INBOXED_SUFFIX):
        return BY_SUFFIX
    if _DATED_NAME.match(name) and os.path.isdir(landing.target_dir(cfg, name)):
        return BY_NAME
    return None


def _created_date(row: Any) -> date | None:
    created = getattr(row, "created_at", None)
    if isinstance(created, datetime):
        return created.date()
    if isinstance(created, date):
        return created
    return None


def _classify(
    cfg: config.Config,
    db: Any,
    row: Any,
    *,
    place: str,
    old_place: str,
    recorded: Mapping[str, date],
    today: date,
    stale_days: int,
    expired_days: int,
) -> Batch | Left:
    playlist_id, name = str(row.ID), str(getattr(row, "Name", "") or "")

    def left(kind: str, reason: str) -> Left:
        return Left(playlist_id, name, place, kind, reason)

    if rb_writer.is_folder(row):
        return left("folder", "a folder is never a batch, and nothing inside it is rotated")
    if int(getattr(row, "Attribute", -1)) != 0:
        return left("smart playlist", "a smart playlist is never a batch")
    recognised_by = _recognised(cfg, row, recorded)
    if recognised_by is None:
        return left(
            "playlist",
            "no landing record names it, its name does not end _inboxed, and no "
            "batch folder under the music folder carries its name",
        )
    if playlist_id in recorded:
        landed, aged_from = recorded[playlist_id], AGED_FROM_RECORD
    else:
        landed, aged_from = _created_date(row), AGED_FROM_CREATED
    if landed is None:
        return left("batch", "no landing record and no creation date to age it from")
    if landed > today:
        return left(
            "batch", f"dated {landed.isoformat()}, after {today.isoformat()}, so its age is unknown"
        )
    age = (today - landed).days
    if place == old_place:
        action = REMOVE if age > expired_days else KEEP
    else:
        action = MOVE if age > stale_days else KEEP
    return Batch(
        playlist_id=playlist_id,
        name=name,
        place=place,
        recognised_by=recognised_by,
        landed=landed,
        aged_from=aged_from,
        age_days=age,
        tracks=_track_count(db, row),
        action=action,
    )


def plan_rotation(
    cfg: config.Config,
    db: Any,
    *,
    declared: taxonomy.Taxonomy,
    registry: tree_registry.Registry,
    today: date,
) -> RotationPlan:
    """Plan the rotation against an open handle. Reads, writes nothing.

    THE THRESHOLDS ARE CONFIGURATION'S, ``reports.intake_stale_days`` and
    ``reports.intake_expired_days``, the two ``report intake-aging`` bands by.
    ``today`` has no default, for that report's reason.

    ONLY THE DIRECT CHILDREN OF INBOX AND OF OLD ARE ASKED. A batch is a
    playlist the landing hangs from the intake root, and a playlist a person
    filed inside a folder of their own has been organised, not forgotten.
    """
    old = old_node(declared)
    tree_id = declared.intake.id
    root_id = anchored_root(db, tree_id, registry)
    root = db.get_playlist(ID=root_id)
    recorded, unreadable = landing_dates(cfg)

    children = _live_children(db, root_id)
    olds = [row for row in children if rb_writer.is_folder(row) and row.Name == old.display]
    if len(olds) > 1:
        raise refuse(
            "intake-old-undeclared",
            f"the intake folder holds {len(olds)} live folders named "
            f"{old.display!r}, and a rotation that targets the folder by name "
            f"cannot tell them apart; merge them in rekordbox, nothing was written",
            remedy=Remedy.COMPLETE_PENDING_ACTION,
            origin=_ORIGIN,
            detail={"folders": [str(row.ID) for row in olds]},
        )
    old_row = olds[0] if olds else None
    nodes = [(row, tree_id) for row in children if row is not old_row]
    if old_row is not None:
        nodes += [(row, old.id) for row in _live_children(db, str(old_row.ID))]

    stale_days = cfg.reports.intake_stale_days
    expired_days = cfg.reports.intake_expired_days
    batches: list[Batch] = []
    left: list[Left] = []
    for row, place in nodes:
        found = _classify(
            cfg,
            db,
            row,
            place=place,
            old_place=old.id,
            recorded=recorded,
            today=today,
            stale_days=stale_days,
            expired_days=expired_days,
        )
        (batches if isinstance(found, Batch) else left).append(found)

    def oldest_first(action: str) -> tuple[Batch, ...]:
        return tuple(
            sorted(
                (batch for batch in batches if batch.action == action),
                key=lambda batch: (-batch.age_days, batch.name, batch.playlist_id),
            )
        )

    planned = RotationPlan(
        tree_id=tree_id,
        root_id=str(root_id),
        root_name=str(getattr(root, "Name", "") or ""),
        old_place=old.id,
        old_display=old.display,
        old_id=str(old_row.ID) if old_row is not None else None,
        as_of=today,
        stale_days=stale_days,
        expired_days=expired_days,
        moves=oldest_first(MOVE),
        removals=oldest_first(REMOVE),
        kept=oldest_first(KEEP),
        left=tuple(sorted(left, key=lambda node: (node.place, node.name, node.playlist_id))),
        unreadable_records=unreadable,
        digest="",
    )
    return replace(planned, digest=digest_of(identity(planned)))


# ---------------------------------------------------------------------------
# Writing
# ---------------------------------------------------------------------------


def _stale(message: str, **detail: Any):
    return refuse(
        "decision-stale",
        message,
        steps=("run `crate inbox rotate` again and approve the plan as it is now",),
        origin=_ORIGIN,
        detail=detail,
    )


def _record_rotation_commit(
    record: session.SessionRecord, plan: RotationPlan, created: int, changed: int, cfg: config.Config
) -> None:
    """Record the commit under the intake tree: the folder it made, the nodes it changed.

    ``updated`` for a move and a removal alike, since each node is still there
    and a restore that discards the session discards that change to it.
    """
    if created <= 0 and changed <= 0:
        return
    session.record_commit(
        record,
        plan.tree_id,
        session.ChangeSummary(
            (session.TreeChange(tree=plan.tree_id, created=created, updated=changed),)
        ),
        cfg,
    )


def _read_back(db: Any, plan: RotationPlan, old_id: str) -> tuple[list[str], int]:
    """Where every planned node sits now, read from SQL after the commit."""
    from sqlalchemy import text

    problems: list[str] = []
    for batch in plan.moves:
        row = db.session.execute(
            text(
                f"SELECT ParentID, {rb_writer.SOFT_DELETE_COLUMN} FROM "
                f"{rb_writer.PLAYLIST_TABLE} WHERE ID = :id"
            ),
            {"id": batch.playlist_id},
        ).first()
        if row is None or str(row[0]) != old_id or row[1]:
            problems.append(f"{batch.name!r} ({batch.playlist_id}) is not live under Old")
    removed = 0
    for batch in plan.removals:
        row = db.session.execute(
            text(
                f"SELECT {rb_writer.SOFT_DELETE_COLUMN} FROM {rb_writer.PLAYLIST_TABLE} "
                f"WHERE ID = :id"
            ),
            {"id": batch.playlist_id},
        ).first()
        if row is None or not row[0]:
            problems.append(f"{batch.name!r} ({batch.playlist_id}) is not marked removed")
        live = db.session.execute(
            text(
                f"SELECT COUNT(*) FROM {rb_writer.MEMBERSHIP_TABLE} WHERE PlaylistID = :id "
                f"AND COALESCE({rb_writer.SOFT_DELETE_COLUMN}, 0) = 0"
            ),
            {"id": batch.playlist_id},
        ).scalar()
        if live:
            problems.append(
                f"{batch.name!r} ({batch.playlist_id}) still holds {live} live membership(s)"
            )
        removed += batch.tracks
    return problems, removed


def apply_rotation(
    cfg: config.Config,
    db: Any,
    plan: RotationPlan,
    *,
    declared: taxonomy.Taxonomy,
    analysis_roots: Iterable[Path | str],
) -> Rotated:
    """Write the approved plan: Old if absent, the moves, the removals. One commit.

    THE PLAN IS TAKEN AGAIN ON THIS HANDLE FIRST, and a digest that moved
    refuses with nothing written. The plan the person approved was read on a
    handle that has since closed, and rekordbox or another verb may have
    changed INBOX in between.

    THE SESSION SPINE IS CALLED, NOT REBUILT, as every database tree writer
    calls it: the three gates with a record kept, a capture verified before
    anything is written, the analysis watch over the roots named, the commit
    witness, and the guarded commit, which here names the playlist and the
    membership tables in ``removals`` and nothing else.

    CONFINED BEFORE IT COMMITS. The whitelist judges the pending session, and
    then :func:`rb_writer.assert_node_changes_confined` compares SQL readings
    taken before and after the writes: no content row, no membership of any
    playlist the plan does not remove, and no playlist row beyond what the
    plan names may have changed. Either refusal rolls everything back.
    """
    watched = [Path(root) for root in analysis_roots]
    if not watched:
        raise ValueError(
            "analysis_roots is empty, so the analysis-file watch would watch nothing "
            "and this session would report itself clean whatever happened to the "
            "library's grids; name the roots this write could touch"
        )
    registry = tree_registry.read(cfg)
    again = plan_rotation(cfg, db, declared=declared, registry=registry, today=plan.as_of)
    if again.digest != plan.digest:
        raise _stale(
            "INBOX is not as the approved plan read it, so nothing was written",
            approved=plan.digest,
            now=again.digest,
        )
    convergence.assert_tree_writable(cfg, db, plan.tree_id, registry)

    created: list[str] = []
    moved: dict[str, str] = {}
    with (
        session.assert_gates(
            cfg, workflow=WORKFLOW, analysis_roots=watched, keep=session.Keep.RECORD
        ) as gates,
        rb_writer.commit_witness(db) as witness,
    ):
        record = gates.record
        capture = snapshot.capture(cfg, db=db)
        session.attach_capture(record, capture.root, cfg)
        snapshot.assert_verified(capture)

        changed = len(plan.moves) + len(plan.removals)
        try:
            before = rb_writer.node_tables(db)
            root = db.get_playlist(ID=plan.root_id)
            old = db.get_playlist(ID=plan.old_id) if plan.old_id else None
            if plan.moves and old is None:
                old = db.create_playlist_folder(plan.old_display, parent=root)
                created.append(str(old.ID))
            for batch in plan.moves:
                rb_writer.move_playlist_node(db, db.get_playlist(ID=batch.playlist_id), old)
                moved[batch.playlist_id] = str(old.ID)
            for batch in plan.removals:
                rb_writer.remove_playlist_node(db, db.get_playlist(ID=batch.playlist_id))
            # JUDGED BEFORE THE FLUSH the confinement check makes, so nothing
            # pending has left the collections the whitelist reads.
            rb_writer.assert_session_whitelisted(db.session, db, removals=REMOVALS)
            rb_writer.assert_node_changes_confined(
                db,
                before,
                moved=moved,
                removed=[batch.playlist_id for batch in plan.removals],
                created=created,
            )
            rb_writer.commit_guarded(db, removals=REMOVALS)
        except BaseException:
            trees._rollback_quietly(db)
            if witness.landed:
                _record_rotation_commit(record, plan, len(created), changed, cfg)
            raise

        _record_rotation_commit(record, plan, len(created), changed, cfg)
        convergence.record_fingerprint(cfg, db)
        old_id = str(old.ID) if old is not None else (plan.old_id or "")
        problems, memberships = _read_back(db, plan, old_id)
        session_id = record.session_id

    return Rotated(
        moved=tuple(batch.playlist_id for batch in plan.moves),
        removed=tuple(batch.playlist_id for batch in plan.removals),
        old_id=old_id,
        old_created=bool(created),
        memberships_removed=memberships,
        session_id=session_id,
        disagreements=tuple(problems),
    )


def assert_read_back(rotated: Rotated) -> None:
    """Refuse when the committed database is not what the plan said it would be.

    The confinement check holds this before the commit, so reaching here is a
    defect, and it is reported as one with every disagreement named.
    """
    if rotated.disagreements:
        raise refuse(
            "internal-error",
            "the rotation committed and the database read back does not agree "
            "with the approved plan: " + "; ".join(rotated.disagreements),
            remedy=Remedy.REPORT_DEFECT,
            origin=_ORIGIN,
            detail={"disagreements": list(rotated.disagreements)},
        )


__all__ = [
    "AGED_FROM_CREATED",
    "AGED_FROM_RECORD",
    "BY_NAME",
    "BY_RECORD",
    "BY_SUFFIX",
    "INBOXED_SUFFIX",
    "KEEP",
    "MOVE",
    "REMOVALS",
    "REMOVE",
    "WORKFLOW",
    "Batch",
    "Left",
    "Rotated",
    "RotationPlan",
    "anchored_root",
    "apply_rotation",
    "assert_read_back",
    "identity",
    "landing_dates",
    "old_node",
    "plan_rotation",
]
