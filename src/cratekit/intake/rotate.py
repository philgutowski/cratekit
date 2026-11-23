"""Rotate INBOX: a stale batch moves into Old, an expired one in Old is removed (U111).

Every landing adds one batch playlist to INBOX, so the rotation keeps it short:

* a batch directly under INBOX older than ``reports.intake_stale_days`` moves
  into the folder ``[intake_old]`` declares, ``INBOX / Old``;
* a batch directly under Old older than ``reports.intake_expired_days`` is
  removed.

TRACKS ARE NEVER REMOVED. A move changes the node's parent and position only;
a removal soft deletes the node and its own memberships, as rekordbox removes
a playlist, so every track stays in the collection and every other playlist.
Both are asserted from SQL before the commit through
:func:`cratekit.core.rb_writer.assert_node_changes_confined`.

WHAT A BATCH IS, decided here and nowhere else, and the plan says which rule:
a native landing's ``run record`` names it by identifier; its name ends
``_inboxed`` (a run's name before U110); an intake file's record whose import
``intake imported`` PROVED names it and its batch folder is still there
(``recorded name``, the LATEST proven landing winning); or its name is U110's
``2026-10-03 Tidal playlists`` shape and a batch folder of that name is there
(``dated name``). An unproven import made no playlist, so one of that name
made later is a person's.

EVERYTHING ELSE IS LEFT ALONE AND LISTED with its kind and reason; the account
mirror reads this one classifier (U214). A BATCH'S AGE is its landing date from
the run record, else the row's ``created_at``; with neither, or dated after the
day asked, it is left alone rather than guessed at. A batch past expiry still
in INBOX moves, so every batch is seen in Old by one plan before one removes it.

Layer: modules. It opens no database of its own: the verb hands it a handle.
"""

from __future__ import annotations

import os
import stat
from dataclasses import dataclass, replace
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping

from cratekit.cli.output import digest_of
from cratekit.core import config, convergence, rb_writer, session, taxonomy, tree_registry
from cratekit.core.cause import Remedy, refuse
from cratekit.intake import batch_name, ingest, landing, native
from cratekit.write import trees
from cratekit.write.row_defaults import watched_roots

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
BY_RECORDED_NAME = "recorded name"

#: What a batch's age was read from.
AGED_FROM_RECORD = "run record"
AGED_FROM_CREATED = "playlist created"

#: Each kind of node left alone, and what a person reads beside its name (U214).
LEFT_OLD = "old"
LEFT_FOLDER = "folder"
LEFT_SMART = "smart playlist"
LEFT_ANALYZE = "analyze"
LEFT_UNRECOGNISED = "playlist"
LEFT_UNDATED = "batch"
LEFT_SHOWN: Mapping[str, str] = {
    LEFT_OLD: "the Old folder",
    LEFT_FOLDER: "a folder",
    LEFT_SMART: "a smart playlist",
    LEFT_ANALYZE: "the Analyze playlist",
    LEFT_UNRECOGNISED: "not recognised as a batch",
    LEFT_UNDATED: "a batch with no age",
}

#: The suffix a batch named for its run carried before U110.
INBOXED_SUFFIX = "_inboxed"

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
    #: The live rows a plain playlist holds, ``None`` for a folder or a smart playlist.
    tracks: int | None = None

    def identity(self) -> dict[str, Any]:
        """What the digest takes: all but the row count, which nothing here writes."""
        return {
            "id": self.playlist_id,
            "playlist": self.name,
            "in": self.place,
            "kind": self.kind,
            "reason": self.reason,
        }

    def to_json(self) -> dict[str, Any]:
        shown = self.identity()
        if self.tracks is not None:
            shown["tracks"] = self.tracks
        return shown

    def label(self) -> str:
        """The node as one line names it: ``2026-10-08 Labels (36 row(s)), not recognised as a batch``."""
        rows = f" ({self.tracks} row(s))" if self.tracks is not None else ""
        return f"{self.name}{rows}, {LEFT_SHOWN.get(self.kind, self.kind)}"


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
    #: Session records that could not be read, an unlisted log counting as one.
    unreadable_records: int
    digest: str
    #: The session log could not be listed, so the warning names no count (R-1255).
    log_unlisted: bool = False

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
    #: The membership rows the removal marked, as the writer returned them.
    memberships_removed: int
    session_id: str
    #: Every way the read back disagrees with the plan, empty when it agrees.
    disagreements: tuple[str, ...]


def identity(plan: RotationPlan) -> dict[str, Any]:
    """What the digest covers: every fact shown and acted on, but a left node's row count."""
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
        "left": [node.identity() for node in plan.left],
    }


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


def anchored_root(
    db: Any,
    tree_id: str,
    registry: tree_registry.Registry,
    *,
    holds: str = "batches",
    act: str = "move",
    origin: tuple[str, ...] = _ORIGIN,
) -> str:
    """The intake tree's adopted root, or the refusal that names ``tree cutover``.

    One home for every INBOX writer: ``holds`` and ``act`` say what the
    caller would have done to the tree's nodes.
    """
    try:
        return tree_registry.anchored_root(
            tree_id, registry, root_exists=lambda root_id: db.get_playlist(ID=root_id) is not None
        )
    except tree_registry.TreeModeRefused as exc:
        if exc.cause.reason != "tree-unconverged" or exc.mode != tree_registry.Mode.XML:
            raise
        raise refuse(
            "tree-unconverged",
            f"the intake tree {tree_id!r} is still on the xml bridge, so its {holds} "
            f"are not this product's to {act} in the database; cut the intake tree "
            f"over first, nothing was read or written",
            remedy=Remedy.COMPLETE_PENDING_ACTION,
            steps=(
                f"run crate tree cutover {tree_id} --export with a Fresh Export to "
                f"move the intake tree to the database",
            ),
            origin=origin,
            detail={"tree_id": tree_id, "mode": str(exc.mode)},
            inner=exc.cause,
        ) from exc


def _local_date(stamp: str) -> date | None:
    try:
        moment = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    return (moment.astimezone() if moment.tzinfo is not None else moment).date()


def _named_ids(record: session.SessionRecord) -> list[str]:
    """Every playlist identifier a native landing record names, batch and account playlists."""
    ids: list[str] = []
    batch = record.detail.get(native.BATCH_PLAYLIST_KEY)
    if isinstance(batch, Mapping) and batch.get("id"):
        ids.append(str(batch["id"]))
    accounts = record.detail.get(native.INBOX_PLAYLISTS_KEY)
    if isinstance(accounts, list):
        ids.extend(
            str(entry["id"]) for entry in accounts if isinstance(entry, Mapping) and entry.get("id")
        )
    return ids


def _named_without_id(record: session.SessionRecord) -> list[tuple[str, str]]:
    """Each account playlist an intake file's record names, with the batch folder it landed in."""
    accounts = record.detail.get(ingest.INBOX_PLAYLISTS_KEY)
    if not isinstance(accounts, list):
        return []
    return [
        (str(entry["name"]), str(entry["batch"]))
        for entry in accounts
        if isinstance(entry, Mapping)
        and not entry.get("id")
        and entry.get("name")
        and entry.get("batch")
    ]


@dataclass(frozen=True, slots=True)
class Landings:
    """What the landing records say about the batches they made."""

    #: Each playlist a native landing named by identifier, and the day it first landed.
    by_id: dict[str, date]
    #: Each account playlist an intake file named, its latest landing day and batch folder.
    by_name: dict[str, tuple[date, str]]
    #: How many records could not be read.
    unreadable: int
    #: The session log could not be listed, so no record was read at all (U214).
    unlisted: bool = False

    def unread(self) -> str:
        """Why a record may name a playlist none read names, ``""`` when every one was read."""
        if self.unlisted:
            return "the session log could not be listed, and a record in it may"
        if self.unreadable:
            return f"{self.unreadable} session record(s) could not be read, and one of them may"
        return ""


def _batch_folder(path: str) -> bool | None:
    """Whether a batch folder is there, ``None`` when the music folder cannot be read.

    ``os.path.isdir`` answers a refused folder as absent, which would call a
    batch whose folder is there no batch at all.
    """
    try:
        return stat.S_ISDIR(os.stat(path).st_mode)
    except (FileNotFoundError, NotADirectoryError):
        return False
    except OSError:
        return None


def landings(cfg: config.Config) -> Landings:
    """Every batch the landing records name, by identifier and by recorded name.

    A native record that committed nothing landed nothing, and the EARLIEST
    landing of an identifier wins: a batch is as old as its first tracks. An
    intake file's record counts once its import was proved, and the LATEST
    naming a name wins, for the reason the module gives.
    """
    records, unreadable = session.scan_log(cfg)
    unlisted = session.log_unlisted(unreadable, cfg)
    by_id: dict[str, date] = {}
    by_name: dict[str, tuple[date, str]] = {}
    for record in records:
        if record.workflow != native.WORKFLOW:
            continue
        landed = _local_date(record.started)
        if landed is None:
            continue
        if session.IMPORT_VERIFIED_KEY in record.detail:
            for name, batch in _named_without_id(record):
                if name not in by_name or landed >= by_name[name][0]:
                    by_name[name] = (landed, batch)
        ids = _named_ids(record)
        if not ids:
            continue
        if str(session.SourceState.COMMITTED) not in {str(v) for v in record.sources.values()}:
            continue
        for key in ids:
            if key not in by_id or landed < by_id[key]:
                by_id[key] = landed
    return Landings(
        by_id=by_id, by_name=by_name, unreadable=len(unreadable), unlisted=unlisted
    )


def _live_children(db: Any, parent_id: str) -> list[Any]:
    rows = db.get_playlist(ParentID=str(parent_id))
    return [row for row in list(rows) if not rb_writer.node_removed(row)]


def _track_count(db: Any, playlist: Any) -> int:
    songs = db.get_playlist_songs(PlaylistID=str(playlist.ID))
    return sum(1 for song in songs if not rb_writer.membership_removed(song))


def _recognised(cfg: config.Config, row: Any, found: Landings) -> tuple[str | None, bool]:
    """How the row is recognised as a batch, and whether a batch folder could not be read.

    The second half keeps an unrecognised playlist from being said to have no
    batch folder while the music folder refused the look (U214).
    """
    name = str(getattr(row, "Name", "") or "")
    if str(row.ID) in found.by_id:
        return BY_RECORD, False
    unread = False
    if name in found.by_name:
        present = _batch_folder(landing.target_dir(cfg, found.by_name[name][1]))
        if present:
            return BY_RECORDED_NAME, False
        unread = unread or present is None
    if name.endswith(INBOXED_SUFFIX):
        return BY_SUFFIX, False
    if batch_name.is_default_shape(name):
        present = _batch_folder(landing.target_dir(cfg, name))
        if present:
            return BY_NAME, False
        unread = unread or present is None
    return None, unread


def _created_date(row: Any) -> date | None:
    """The LOCAL day the row was created, as a batch is named for the local day.

    pyrekordbox 0.4.4 hands the UTC column back naive and already local; an
    aware value is converted the same way rather than read on the UTC calendar.
    """
    created = getattr(row, "created_at", None)
    if isinstance(created, datetime):
        return (created.astimezone() if created.tzinfo is not None else created).date()
    return created if isinstance(created, date) else None


def _classify(
    cfg: config.Config,
    db: Any,
    row: Any,
    *,
    place: str,
    found: Landings,
    today: date,
    in_old: bool = False,
    old_display: str | None = None,
) -> Batch | Left:
    """One node as a batch, or as left alone with its kind and reason.

    ``old_display`` names the folder of that name directly under INBOX as Old,
    ``None`` when no Old is declared. An unread record or music folder is said
    as such, never as no record or no batch folder (U214).
    """
    playlist_id, name = str(row.ID), str(getattr(row, "Name", "") or "")

    def left(kind: str, reason: str, *, counted: bool = True) -> Left:
        tracks = _track_count(db, row) if counted else None
        return Left(playlist_id, name, place, kind, reason, tracks)

    if rb_writer.is_folder(row):
        if not in_old and old_display is not None and name == old_display:
            return left(
                LEFT_OLD,
                "the folder a stale batch moves into is never a batch, and a batch "
                "in it has left INBOX",
                counted=False,
            )
        return left(
            LEFT_FOLDER,
            "a folder is never a batch, and nothing inside it is rotated",
            counted=False,
        )
    if int(getattr(row, "Attribute", -1)) != 0:
        return left(LEFT_SMART, "a smart playlist is never a batch", counted=False)
    # INBOX / ANALYZE IS NEVER A BATCH (U166), whatever an old record says: it
    # holds the rows awaiting analysis, and Old would take them out of the visit.
    if not in_old and name == native.ANALYZE:
        return left(
            LEFT_ANALYZE,
            "the playlist every landing fills with the rows awaiting analysis is "
            "never a batch; crate inbox analyzed takes out what rekordbox analysed",
        )
    recognised_by, folder_unread = _recognised(cfg, row, found)
    if recognised_by is None:
        unread = found.unread()
        records = (
            f"no readable landing record names it ({unread})"
            if unread
            else "no landing record names it"
        )
        folders = (
            "and the music folder could not be read to look for a batch folder of "
            "its name, which may be there"
            if folder_unread
            else "and no batch folder under the music folder carries its name"
        )
        return left(LEFT_UNRECOGNISED, f"{records}, its name does not end _inboxed, {folders}")
    if playlist_id in found.by_id:
        landed, aged_from = found.by_id[playlist_id], AGED_FROM_RECORD
    elif recognised_by == BY_RECORDED_NAME:
        landed, aged_from = found.by_name[name][0], AGED_FROM_RECORD
    else:
        landed, aged_from = _created_date(row), AGED_FROM_CREATED
    if landed is None:
        return left(LEFT_UNDATED, "no landing record and no creation date to age it from")
    if landed > today:
        return left(
            LEFT_UNDATED, f"dated {landed.isoformat()}, after {today.isoformat()}, so its age is unknown"
        )
    age = (today - landed).days
    stale_days, expired_days = cfg.reports.intake_stale_days, cfg.reports.intake_expired_days
    if in_old:
        action = REMOVE if age > expired_days else KEEP
    else:
        action = MOVE if age > stale_days else KEEP
    return Batch(
        playlist_id,
        name,
        place,
        recognised_by,
        landed,
        aged_from,
        age,
        _track_count(db, row),
        action,
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

    The thresholds are configuration's, ``today`` has no default, and ONLY THE
    DIRECT CHILDREN OF INBOX AND OF OLD ARE ASKED: a playlist a person filed
    inside a folder of their own has been organised, not forgotten.
    """
    old = old_node(declared)
    tree_id = declared.intake.id
    root_id = anchored_root(db, tree_id, registry)
    found = landings(cfg)
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
    # WHERE A ROW SITS IS READ OFF THE TREE, never off the two taxonomy ids,
    # which a hand edited template could make equal.
    nodes = [(row, tree_id, False) for row in children]
    if old_row is not None:
        nodes += [(row, old.id, True) for row in _live_children(db, str(old_row.ID))]
    batches: list[Batch] = []
    left: list[Left] = []
    for row, place, in_old in nodes:
        classified = _classify(
            cfg,
            db,
            row,
            place=place,
            in_old=in_old,
            found=found,
            today=today,
            old_display=old.display,
        )
        (batches if isinstance(classified, Batch) else left).append(classified)

    def oldest_first(action: str) -> tuple[Batch, ...]:
        chosen = (batch for batch in batches if batch.action == action)
        return tuple(sorted(chosen, key=lambda one: (-one.age_days, one.name, one.playlist_id)))

    planned = RotationPlan(
        tree_id=tree_id,
        root_id=str(root_id),
        root_name=str(getattr(db.get_playlist(ID=root_id), "Name", "") or ""),
        old_place=old.id,
        old_display=old.display,
        old_id=str(old_row.ID) if old_row is not None else None,
        as_of=today,
        stale_days=cfg.reports.intake_stale_days,
        expired_days=cfg.reports.intake_expired_days,
        moves=oldest_first(MOVE),
        removals=oldest_first(REMOVE),
        kept=oldest_first(KEEP),
        left=tuple(sorted(left, key=lambda node: (node.place, node.name, node.playlist_id))),
        unreadable_records=found.unreadable,
        digest="",
        log_unlisted=found.unlisted,
    )
    return replace(planned, digest=digest_of(identity(planned)))


@dataclass(frozen=True, slots=True)
class Live:
    """The batches directly under INBOX now, what the account mirror copies (U150)."""

    root_id: str
    root_name: str
    #: Each live batch, ``(playlist id, name)``, ordered by name then id.
    batches: tuple[tuple[str, str], ...]
    #: The name of every live node directly under INBOX, so a mirror tells a
    #: batch that LEFT INBOX from one that no longer reads as a batch.
    present: frozenset[str]
    #: Every other live node directly under INBOX with its kind and reason (U214).
    left: tuple[Left, ...] = ()


def live_batches(
    cfg: config.Config,
    db: Any,
    *,
    declared: taxonomy.Taxonomy,
    registry: tree_registry.Registry,
    today: date,
) -> Live:
    """Every batch directly under INBOX, by this module's one rule of what a batch is.

    The same classifier as :func:`plan_rotation`, so the mirror and the
    rotation never disagree. A BATCH IS LIVE WHILE IT SITS UNDER INBOX, stale,
    undated or not, since whether a rotation moves it this run is not known
    when the mirror is planned. Everything else directly under INBOX is in
    ``left`` with its reason. Needs no ``[intake_old]``; refuses as
    :func:`anchored_root` does.
    """
    tree_id = declared.intake.id
    root_id = anchored_root(db, tree_id, registry)
    found = landings(cfg)
    children = _live_children(db, root_id)
    old_display = declared.intake_old.display if declared.intake_old is not None else None
    batches: list[tuple[str, str]] = []
    left: list[Left] = []
    for row in children:
        classified = _classify(
            cfg, db, row, place=tree_id, found=found, today=today, old_display=old_display
        )
        if isinstance(classified, Batch) or classified.kind == LEFT_UNDATED:
            batches.append((classified.playlist_id, classified.name))
        else:
            left.append(classified)
    return Live(
        root_id=str(root_id),
        root_name=str(getattr(db.get_playlist(ID=root_id), "Name", "") or ""),
        batches=tuple(sorted(batches, key=lambda one: (one[1], one[0]))),
        present=frozenset(str(getattr(row, "Name", "") or "") for row in children),
        left=tuple(sorted(left, key=lambda node: (node.name, node.playlist_id))),
    )


def _record_rotation_commit(
    record: session.SessionRecord, plan: RotationPlan, created: int, changed: int, cfg: config.Config
) -> None:
    """Record the commit under the intake tree: the folder it made, the nodes it changed.

    ``updated`` for a move and a removal alike: each node is still there, and a
    restore that discards the session discards that change to it.
    """
    if created <= 0 and changed <= 0:
        return
    change = session.TreeChange(tree=plan.tree_id, created=created, updated=changed)
    session.record_commit(record, plan.tree_id, session.ChangeSummary((change,)), cfg)


def _read_back(db: Any, plan: RotationPlan, old_id: str) -> list[str]:
    """Where every planned node sits now, read from SQL after the commit."""
    from sqlalchemy import text

    def run(sql: str, playlist_id: str) -> Any:
        return db.session.execute(text(sql), {"id": playlist_id})

    node = (
        f"SELECT ParentID, {rb_writer.SOFT_DELETE_COLUMN} FROM {rb_writer.PLAYLIST_TABLE} "
        f"WHERE ID = :id"
    )
    live = (
        f"SELECT COUNT(*) FROM {rb_writer.MEMBERSHIP_TABLE} WHERE PlaylistID = :id "
        f"AND COALESCE({rb_writer.SOFT_DELETE_COLUMN}, 0) = 0"
    )
    problems: list[str] = []
    for batch in plan.moves:
        row = run(node, batch.playlist_id).first()
        if row is None or str(row[0]) != old_id or row[1]:
            problems.append(f"{batch.name!r} ({batch.playlist_id}) is not live under Old")
    for batch in plan.removals:
        row = run(node, batch.playlist_id).first()
        if row is None or not row[1]:
            problems.append(f"{batch.name!r} ({batch.playlist_id}) is not marked removed")
        held = run(live, batch.playlist_id).scalar()
        if held:
            problems.append(
                f"{batch.name!r} ({batch.playlist_id}) still holds {held} live membership(s)"
            )
    return problems


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
    refuses with nothing written: the approved plan was read on a handle since
    closed. The session spine is called as every tree writer calls it, and the
    guarded commit admits removals in ``REMOVALS`` only. CONFINED BEFORE IT
    COMMITS: SQL readings before and after the writes must show no change the
    plan does not name and every change it does, or everything rolls back.
    """
    watched = watched_roots(analysis_roots)
    registry = tree_registry.read(cfg)
    again = plan_rotation(cfg, db, declared=declared, registry=registry, today=plan.as_of)
    if again.digest != plan.digest:
        raise refuse(
            "decision-stale",
            "INBOX is not as the approved plan read it, so nothing was written",
            steps=("run `crate inbox rotate` again and approve the plan as it is now",),
            origin=_ORIGIN,
            detail={"approved": plan.digest, "now": again.digest},
        )
    convergence.assert_tree_writable(cfg, db, plan.tree_id, registry)

    created: list[str] = []
    moved: dict[str, str] = {}
    marked = 0
    with (
        session.assert_gates(
            cfg, workflow=WORKFLOW, analysis_roots=watched, keep=session.Keep.RECORD
        ) as gates,
        rb_writer.commit_witness(db) as witness,
    ):
        record, capture = trees.attached_capture(gates, cfg, db)
        changed = len(plan.moves) + len(plan.removals)
        try:
            before = rb_writer.node_tables(db)
            old = db.get_playlist(ID=plan.old_id) if plan.old_id else None
            if plan.moves and old is None:
                old = db.create_playlist_folder(
                    plan.old_display, parent=db.get_playlist(ID=plan.root_id)
                )
                created.append(str(old.ID))
            for batch in plan.moves:
                rb_writer.move_playlist_node(db, db.get_playlist(ID=batch.playlist_id), old)
                moved[batch.playlist_id] = str(old.ID)
            for batch in plan.removals:
                marked += len(
                    rb_writer.remove_playlist_node(db, db.get_playlist(ID=batch.playlist_id))
                )
            removed = [batch.playlist_id for batch in plan.removals]
            rb_writer.assert_node_changes_confined(
                db, before, moved=moved, removed=removed, created=created
            )
            rb_writer.commit_guarded(db, removals=REMOVALS)
        except BaseException:
            trees.rollback_quietly(db)
            if witness.landed:
                _record_rotation_commit(record, plan, len(created), changed, cfg)
            raise

        _record_rotation_commit(record, plan, len(created), changed, cfg)
        convergence.record_fingerprint(cfg, db)
        old_id = str(old.ID) if old is not None else (plan.old_id or "")
        problems = _read_back(db, plan, old_id)
        session_id = record.session_id

    return Rotated(
        moved=tuple(batch.playlist_id for batch in plan.moves),
        removed=tuple(removed),
        old_id=old_id,
        old_created=bool(created),
        memberships_removed=marked,
        session_id=session_id,
        disagreements=tuple(problems),
    )


def assert_read_back(rotated: Rotated) -> None:
    """Refuse when the committed database is not what the plan said, as a defect.

    The confinement check holds this before the commit, so reaching here is one.
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
